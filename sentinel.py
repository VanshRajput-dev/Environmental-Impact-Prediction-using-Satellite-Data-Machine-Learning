# sentinel.py — Satellite image fetcher using Microsoft Planetary Computer
# FREE, no account needed, no API key, just install the packages:
#   pip install pystac-client planetary-computer odc-stac rioxarray

import os
import math
import numpy as np
from PIL import Image
from datetime import datetime, timedelta

# ── Validate inputs ───────────────────────────────────────────────────────────

def validate_coords(lat: float, lon: float) -> None:
    if not (-90 <= lat <= 90):
        raise ValueError(f"Latitude must be between -90 and 90, got {lat}")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Longitude must be between -180 and 180, got {lon}")

def validate_date(date_str: str) -> None:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Date must be YYYY-MM-DD format, got '{date_str}'")
    if d > datetime.utcnow():
        raise ValueError("Date cannot be in the future.")
    if d < datetime(2017, 3, 28):
        raise ValueError("Sentinel-2 data only available from 2017-03-28 onwards.")

# ── Bounding box helper ───────────────────────────────────────────────────────

def latlon_to_bbox(lat: float, lon: float, size_km: float = 2.5):
    delta_lat = (size_km / 2) / 111.0
    delta_lon = (size_km / 2) / (111.0 * math.cos(math.radians(lat)))
    return [lon - delta_lon, lat - delta_lat, lon + delta_lon, lat + delta_lat]

# ── Main fetch function ───────────────────────────────────────────────────────

def fetch_sentinel_image(
    lat: float,
    lon: float,
    date: str,
    output_path: str,
    size_km: float = 2.5,
) -> str:
    """
    Fetch a true-colour Sentinel-2 tile from Microsoft Planetary Computer.
    No API key or account required.
    Install: pip install pystac-client planetary-computer odc-stac rioxarray
    """
    try:
        import pystac_client
        import planetary_computer
        import odc.stac
    except ImportError:
        raise RuntimeError(
            "Missing packages. Run:\n"
            "pip install pystac-client planetary-computer odc-stac rioxarray"
        )

    bbox_list = latlon_to_bbox(lat, lon, size_km)
    target    = datetime.strptime(date, "%Y-%m-%d")

    # Connect to Planetary Computer STAC catalog — no auth needed
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )

    def search_items(days_window, max_cloud):
        date_from = (target - timedelta(days=days_window)).strftime("%Y-%m-%d")
        date_to   = (target + timedelta(days=days_window)).strftime("%Y-%m-%d")
        s = catalog.search(
            collections=["sentinel-2-l2a"],
            bbox=bbox_list,
            datetime=f"{date_from}/{date_to}",
            query={"eo:cloud_cover": {"lt": max_cloud}},
            sortby="-datetime",
        )
        return list(s.items())

    # Try progressively — narrow + clear first, then widen
    items = (
        search_items(20, 20) or
        search_items(30, 40) or
        search_items(60, 80)
    )

    if not items:
        raise RuntimeError(
            f"No Sentinel-2 imagery found near lat={lat}, lon={lon} "
            f"around {date}. Try a different date."
        )

    # Pick item with lowest cloud cover
    best = min(items, key=lambda i: i.properties.get("eo:cloud_cover", 999))
    cloud = best.properties.get("eo:cloud_cover", "?")
    print(f"[Planetary Computer] Using scene: {best.id}  cloud={cloud}%")

    # Load RGB bands at 10m resolution
    ds = odc.stac.load(
        [best],
        bands=["B04", "B03", "B02"],
        bbox=bbox_list,
        resolution=10,
    )

    red   = ds["B04"].values[0].astype(np.float32)
    green = ds["B03"].values[0].astype(np.float32)
    blue  = ds["B02"].values[0].astype(np.float32)

    rgb = np.stack([red, green, blue], axis=-1)

    # Percentile stretch for natural-looking brightness
    valid = rgb[rgb > 0]
    if valid.size == 0:
        raise RuntimeError("Downloaded image appears to be empty (all zeros).")

    p2, p98 = np.percentile(valid, 2), np.percentile(valid, 98)
    p98 = max(p98, p2 + 1)
    rgb = np.clip((rgb - p2) / (p98 - p2), 0, 1)
    rgb = (rgb * 255).astype(np.uint8)

    img = Image.fromarray(rgb, mode="RGB")
    img = img.resize((224, 224), Image.LANCZOS)
    img.save(output_path, "JPEG", quality=92)

    return output_path