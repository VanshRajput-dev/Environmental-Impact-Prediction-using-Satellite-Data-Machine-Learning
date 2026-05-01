const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

// Color palette - Forest & Tech inspired
const C = {
  dark: "0D2137",       // Deep navy
  primary: "1A6B3C",    // Forest green
  accent: "2ECC71",     // Bright green
  light: "E8F5EE",      // Light mint
  white: "FFFFFF",
  gray: "64748B",
  lightgray: "F1F5F9",
  text: "1E293B",
  muted: "94A3B8",
  teal: "0F766E",
  gold: "F59E0B",
};

// Icon rendering
const { FaLeaf, FaBrain, FaChartBar, FaMobileAlt, FaDatabase, FaCog, FaCheckCircle, FaLightbulb, FaFlask, FaCalendarAlt, FaBook, FaBullseye } = require("react-icons/fa");
const { MdOutlineScience, MdSevereCold } = require("react-icons/md");

function renderIconSvg(IconComponent, color = "#FFFFFF", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color = "#FFFFFF", size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.title = "Crop Disease Detection using Transfer Learning";

  // ─────────────────────────────────────────
  // SLIDE 1: TITLE SLIDE
  // ─────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.dark };

    // Left accent bar
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 5.625,
      fill: { color: C.accent }, line: { color: C.accent }
    });

    // Top institution band
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.08, y: 0, w: 9.92, h: 0.75,
      fill: { color: "0A1A2E" }, line: { color: "0A1A2E" }
    });

    slide.addText("SRM INSTITUTE OF SCIENCE AND TECHNOLOGY  |  SCHOOL OF COMPUTING  |  DEPT. OF COMPUTING TECHNOLOGIES  |  21CSP302L - MINOR PROJECT", {
      x: 0.3, y: 0.05, w: 9.4, h: 0.65,
      fontSize: 9, color: C.muted, bold: false, align: "left", valign: "middle",
      fontFace: "Calibri", margin: 0
    });

    // Main title
    slide.addText("Crop Disease Detection", {
      x: 0.6, y: 1.05, w: 8.5, h: 0.9,
      fontSize: 46, color: C.white, bold: true, fontFace: "Calibri",
      margin: 0
    });
    slide.addText("using Transfer Learning", {
      x: 0.6, y: 1.85, w: 8.5, h: 0.75,
      fontSize: 36, color: C.accent, bold: false, fontFace: "Calibri",
      margin: 0
    });

    // Divider line
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y: 2.72, w: 5.5, h: 0.04,
      fill: { color: C.teal }, line: { color: C.teal }
    });

    // Batch & Authors section
    slide.addText("Batch ID: B677", {
      x: 0.6, y: 2.9, w: 4, h: 0.35,
      fontSize: 13, color: C.muted, fontFace: "Calibri", margin: 0
    });

    slide.addText([
      { text: "RA2311003010167  ", options: { bold: true, color: C.white } },
      { text: "Vaibhav Singh", options: { color: C.light } }
    ], { x: 0.6, y: 3.25, w: 5, h: 0.3, fontSize: 13, fontFace: "Calibri", margin: 0 });

    slide.addText([
      { text: "RA2311003010168  ", options: { bold: true, color: C.white } },
      { text: "Smyan Arora", options: { color: C.light } }
    ], { x: 0.6, y: 3.55, w: 5, h: 0.3, fontSize: 13, fontFace: "Calibri", margin: 0 });

    // Guide box
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y: 4.05, w: 4, h: 0.95,
      fill: { color: "132D4A" }, line: { color: C.teal, pt: 1 }
    });
    slide.addText("Guide", {
      x: 0.7, y: 4.1, w: 3.8, h: 0.25,
      fontSize: 9, color: C.muted, fontFace: "Calibri", margin: 0
    });
    slide.addText("Dr. A Arulmurugan", {
      x: 0.7, y: 4.3, w: 3.8, h: 0.3,
      fontSize: 13, color: C.white, bold: true, fontFace: "Calibri", margin: 0
    });
    slide.addText("Assistant Professor  |  CTECH", {
      x: 0.7, y: 4.6, w: 3.8, h: 0.25,
      fontSize: 10, color: C.muted, fontFace: "Calibri", margin: 0
    });

    // Right decorative circles
    slide.addShape(pres.shapes.OVAL, {
      x: 7.2, y: 1.0, w: 2.8, h: 2.8,
      fill: { color: C.primary, transparency: 70 }, line: { color: C.accent, pt: 1 }
    });
    slide.addShape(pres.shapes.OVAL, {
      x: 7.7, y: 1.5, w: 2.2, h: 2.2,
      fill: { color: C.primary, transparency: 50 }, line: { color: "FFFFFF", pt: 0 }
    });

    const leafIcon = await iconToBase64Png(FaLeaf, "#2ECC71", 256);
    slide.addImage({ data: leafIcon, x: 8.2, y: 2.0, w: 1.2, h: 1.2 });

    // Date
    slide.addText("28 February 2026", {
      x: 7.5, y: 5.1, w: 2.3, h: 0.3,
      fontSize: 10, color: C.muted, align: "right", fontFace: "Calibri", margin: 0
    });
  }

  // ─────────────────────────────────────────
  // SLIDE 2: PROBLEM STATEMENT
  // ─────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.white };

    // Header band
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 1.0,
      fill: { color: C.dark }, line: { color: C.dark }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 1.0,
      fill: { color: C.accent }, line: { color: C.accent }
    });
    slide.addText("Problem Statement", {
      x: 0.3, y: 0.1, w: 7, h: 0.8,
      fontSize: 28, color: C.white, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText("02", {
      x: 8.8, y: 0.1, w: 1.0, h: 0.8,
      fontSize: 36, color: C.accent, bold: true, fontFace: "Calibri", align: "center", valign: "middle", margin: 0
    });

    // Big stat
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.4, y: 1.2, w: 2.0, h: 1.6,
      fill: { color: C.primary }, line: { color: C.primary },
      shadow: { type: "outer", blur: 8, offset: 3, angle: 135, color: "000000", opacity: 0.15 }
    });
    slide.addText("40%", {
      x: 0.4, y: 1.3, w: 2.0, h: 0.9,
      fontSize: 42, color: C.accent, bold: true, align: "center", fontFace: "Calibri", margin: 0
    });
    slide.addText("Crops Affected\nAnnually", {
      x: 0.4, y: 2.1, w: 2.0, h: 0.55,
      fontSize: 10, color: C.light, align: "center", fontFace: "Calibri", margin: 0
    });

    // Problem text
    slide.addText("The Challenge", {
      x: 2.8, y: 1.2, w: 6.8, h: 0.35,
      fontSize: 14, color: C.primary, bold: true, fontFace: "Calibri", margin: 0
    });
    slide.addText("Crop diseases cause major agricultural losses worldwide. Traditional detection methods rely on manual inspection — which is slow, subjective, and error-prone. Although AI models can classify diseases, most do not measure infection severity and are not optimized for real-world field conditions.",
      {
        x: 2.8, y: 1.55, w: 6.8, h: 1.2,
        fontSize: 12.5, color: C.text, fontFace: "Calibri", margin: 0
      }
    );

    // Need box
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.4, y: 3.05, w: 9.2, h: 1.9,
      fill: { color: C.light }, line: { color: C.accent, pt: 1.5 }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.4, y: 3.05, w: 0.07, h: 1.9,
      fill: { color: C.accent }, line: { color: C.accent }
    });
    slide.addText("The Need", {
      x: 0.65, y: 3.15, w: 8.8, h: 0.32,
      fontSize: 13, color: C.primary, bold: true, fontFace: "Calibri", margin: 0
    });
    slide.addText("To develop a lightweight, efficient AI system that can accurately detect crop diseases and quantify severity from field images — enabling data-driven, real-time agricultural decisions.",
      {
        x: 0.65, y: 3.5, w: 8.8, h: 1.3,
        fontSize: 12.5, color: C.text, fontFace: "Calibri", margin: 0
      }
    );
  }

  // ─────────────────────────────────────────
  // SLIDE 3: OBJECTIVES
  // ─────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.white };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 1.0,
      fill: { color: C.dark }, line: { color: C.dark }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 1.0,
      fill: { color: C.accent }, line: { color: C.accent }
    });
    slide.addText("Objectives", {
      x: 0.3, y: 0.1, w: 7, h: 0.8,
      fontSize: 28, color: C.white, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText("03", {
      x: 8.8, y: 0.1, w: 1.0, h: 0.8,
      fontSize: 36, color: C.accent, bold: true, fontFace: "Calibri", align: "center", valign: "middle", margin: 0
    });

    const objectives = [
      {
        icon: FaBrain,
        num: "01",
        title: "High-Accuracy Disease Identification",
        desc: "Achieve real-time crop disease identification using transfer learning–based deep learning models with superior accuracy."
      },
      {
        icon: FaChartBar,
        num: "02",
        title: "Pixel-Level Segmentation & DSI",
        desc: "Perform precise pixel-level segmentation for infection area detection and compute the Disease Severity Index (DSI)."
      },
      {
        icon: FaMobileAlt,
        num: "03",
        title: "Lightweight & Field-Ready System",
        desc: "Develop a computationally efficient and lightweight AI system suitable for real-world field conditions and mobile deployment."
      }
    ];

    for (let i = 0; i < objectives.length; i++) {
      const o = objectives[i];
      const x = 0.3 + i * 3.2;
      const y = 1.2;

      // Card background
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: 3.0, h: 4.0,
        fill: { color: C.lightgray }, line: { color: "E2E8F0", pt: 1 },
        shadow: { type: "outer", blur: 6, offset: 3, angle: 135, color: "000000", opacity: 0.1 }
      });

      // Top accent
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: 3.0, h: 0.08,
        fill: { color: C.accent }, line: { color: C.accent }
      });

      // Number
      slide.addText(o.num, {
        x: x + 0.15, y: y + 0.25, w: 0.7, h: 0.55,
        fontSize: 28, color: C.primary, bold: true, fontFace: "Calibri", margin: 0
      });

      const iconData = await iconToBase64Png(o.icon, "#1A6B3C", 256);
      slide.addImage({ data: iconData, x: x + 2.35, y: y + 0.25, w: 0.45, h: 0.45 });

      // Title
      slide.addText(o.title, {
        x: x + 0.15, y: y + 0.85, w: 2.7, h: 0.65,
        fontSize: 13, color: C.text, bold: true, fontFace: "Calibri", margin: 0
      });

      // Desc
      slide.addText(o.desc, {
        x: x + 0.15, y: y + 1.55, w: 2.7, h: 2.2,
        fontSize: 11.5, color: C.gray, fontFace: "Calibri", margin: 0
      });
    }
  }

  // ─────────────────────────────────────────
  // SLIDE 4: LITERATURE REVIEW
  // ─────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.white };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 1.0,
      fill: { color: C.dark }, line: { color: C.dark }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 1.0,
      fill: { color: C.accent }, line: { color: C.accent }
    });
    slide.addText("Literature Review", {
      x: 0.3, y: 0.1, w: 7, h: 0.8,
      fontSize: 28, color: C.white, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText("04", {
      x: 8.8, y: 0.1, w: 1.0, h: 0.8,
      fontSize: 36, color: C.accent, bold: true, fontFace: "Calibri", align: "center", valign: "middle", margin: 0
    });

    // Findings box (left)
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 1.2, w: 4.4, h: 2.4,
      fill: { color: C.light }, line: { color: C.primary, pt: 1 }
    });
    const checkIcon = await iconToBase64Png(FaCheckCircle, "#1A6B3C", 256);
    slide.addImage({ data: checkIcon, x: 0.45, y: 1.28, w: 0.32, h: 0.32 });
    slide.addText("Research Findings", {
      x: 0.85, y: 1.28, w: 3.7, h: 0.35,
      fontSize: 13, color: C.primary, bold: true, fontFace: "Calibri", margin: 0
    });
    slide.addText([
      { text: "• ", options: {} },
      { text: "CNN & Transfer Learning", options: { bold: true } },
      { text: " achieve >95–98% accuracy in disease classification (Shoaib et al., 2023; IEEE Access, 2024)", options: {} },
      { text: "\n• Lightweight models like ", options: { breakLine: true } },
      { text: "MobileNet", options: { bold: true } },
      { text: " have improved computational efficiency for agricultural applications", options: {} }
    ], {
      x: 0.45, y: 1.65, w: 4.15, h: 1.7,
      fontSize: 11.5, color: C.text, fontFace: "Calibri", margin: 0
    });

    // Limitations box (right)
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 5.0, y: 1.2, w: 4.6, h: 2.4,
      fill: { color: "FFF8F0" }, line: { color: C.gold, pt: 1 }
    });
    const warnIcon = await iconToBase64Png(FaLightbulb, "#F59E0B", 256);
    slide.addImage({ data: warnIcon, x: 5.15, y: 1.28, w: 0.32, h: 0.32 });
    slide.addText("Limitations of Existing Work", {
      x: 5.55, y: 1.28, w: 3.8, h: 0.35,
      fontSize: 13, color: C.gold, bold: true, fontFace: "Calibri", margin: 0
    });
    slide.addText([
      { text: "• Most existing systems focus only on ", options: {} },
      { text: "disease classification", options: { bold: true } },
      { text: " and do not provide pixel-level severity estimation", options: {} },
      { text: "\n• Many models are ", options: { breakLine: true } },
      { text: "computationally heavy", options: { bold: true } },
      { text: " and not optimized for real-time field deployment", options: {} }
    ], {
      x: 5.15, y: 1.65, w: 4.2, h: 1.7,
      fontSize: 11.5, color: C.text, fontFace: "Calibri", margin: 0
    });

    // Research gap
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 3.85, w: 9.3, h: 1.5,
      fill: { color: C.dark }, line: { color: C.dark }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 3.85, w: 0.07, h: 1.5,
      fill: { color: C.accent }, line: { color: C.accent }
    });
    slide.addText("Research Gap Identified", {
      x: 0.55, y: 3.95, w: 8.8, h: 0.32,
      fontSize: 13, color: C.accent, bold: true, fontFace: "Calibri", margin: 0
    });
    slide.addText("There is limited work on developing a lightweight, real-time AI system that integrates both accurate disease detection and Disease Severity Index (DSI) calculation for precision agriculture.",
      {
        x: 0.55, y: 4.28, w: 8.8, h: 0.9,
        fontSize: 12, color: C.light, fontFace: "Calibri", margin: 0
      }
    );
  }

  // ─────────────────────────────────────────
  // SLIDE 5: PROPOSED METHODOLOGY
  // ─────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.white };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 1.0,
      fill: { color: C.dark }, line: { color: C.dark }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 1.0,
      fill: { color: C.accent }, line: { color: C.accent }
    });
    slide.addText("Proposed Methodology", {
      x: 0.3, y: 0.1, w: 7, h: 0.8,
      fontSize: 28, color: C.white, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText("05", {
      x: 8.8, y: 0.1, w: 1.0, h: 0.8,
      fontSize: 36, color: C.accent, bold: true, fontFace: "Calibri", align: "center", valign: "middle", margin: 0
    });

    // Subtitle
    slide.addText("Hybrid Deep Learning Framework — integrating disease classification with pixel-level severity estimation", {
      x: 0.3, y: 1.1, w: 9.4, h: 0.4,
      fontSize: 12, color: C.gray, fontFace: "Calibri", italic: true, margin: 0
    });

    const steps = [
      { num: "1", title: "Data Acquisition & Preprocessing", items: ["PlantVillage & field images", "Resize, normalize, denoise", "Augmentation: rotation, flip, brightness"] },
      { num: "2", title: "Transfer Learning Classification", items: ["MobileNetV2 backbone", "Fine-tune for crop diseases", "Reduces training time & complexity"] },
      { num: "3", title: "Pixel-Level Segmentation", items: ["Modified U-Net architecture", "Binary mask generation", "Healthy vs. infected regions"] },
      { num: "4", title: "DSI Computation & Deployment", items: ["DSI = (Infected ÷ Total) × 100", "Model compression & optimization", "Mobile / edge device deployment"] }
    ];

    for (let i = 0; i < 4; i++) {
      const step = steps[i];
      const col = i % 2;
      const row = Math.floor(i / 2);
      const x = 0.3 + col * 4.85;
      const y = 1.65 + row * 1.95;

      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: 4.5, h: 1.75,
        fill: { color: C.lightgray }, line: { color: "CBD5E1", pt: 1 },
        shadow: { type: "outer", blur: 5, offset: 2, angle: 135, color: "000000", opacity: 0.08 }
      });

      // Number circle
      slide.addShape(pres.shapes.OVAL, {
        x: x + 0.15, y: y + 0.1, w: 0.5, h: 0.5,
        fill: { color: C.primary }, line: { color: C.primary }
      });
      slide.addText(step.num, {
        x: x + 0.15, y: y + 0.1, w: 0.5, h: 0.5,
        fontSize: 14, color: C.white, bold: true, align: "center", valign: "middle",
        fontFace: "Calibri", margin: 0
      });

      slide.addText(step.title, {
        x: x + 0.75, y: y + 0.1, w: 3.6, h: 0.5,
        fontSize: 12.5, color: C.text, bold: true, fontFace: "Calibri", margin: 0
      });

      for (let j = 0; j < step.items.length; j++) {
        slide.addText("• " + step.items[j], {
          x: x + 0.15, y: y + 0.68 + j * 0.33,
          w: 4.2, h: 0.3,
          fontSize: 10.5, color: C.gray, fontFace: "Calibri", margin: 0
        });
      }
    }
  }

  // ─────────────────────────────────────────
  // SLIDE 6: DSI FORMULA SLIDE
  // ─────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.white };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 1.0,
      fill: { color: C.dark }, line: { color: C.dark }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 1.0,
      fill: { color: C.accent }, line: { color: C.accent }
    });
    slide.addText("Disease Severity Index (DSI)", {
      x: 0.3, y: 0.1, w: 8, h: 0.8,
      fontSize: 28, color: C.white, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText("06", {
      x: 8.8, y: 0.1, w: 1.0, h: 0.8,
      fontSize: 36, color: C.accent, bold: true, fontFace: "Calibri", align: "center", valign: "middle", margin: 0
    });

    // DSI Formula box
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 1.5, y: 1.1, w: 7.0, h: 1.6,
      fill: { color: C.dark }, line: { color: C.accent, pt: 2 }
    });
    slide.addText("DSI (%) =", {
      x: 1.7, y: 1.2, w: 1.8, h: 1.4,
      fontSize: 20, color: C.white, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText("Infected Pixel Count", {
      x: 3.6, y: 1.3, w: 4.5, h: 0.45,
      fontSize: 18, color: C.accent, bold: true, align: "center", fontFace: "Calibri", margin: 0
    });
    // Fraction line
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 3.6, y: 1.75, w: 4.5, h: 0.04,
      fill: { color: C.white }, line: { color: C.white }
    });
    slide.addText("Total Leaf Pixel Count", {
      x: 3.6, y: 1.82, w: 4.5, h: 0.45,
      fontSize: 18, color: C.light, align: "center", fontFace: "Calibri", margin: 0
    });
    slide.addText("× 100", {
      x: 8.1, y: 1.15, w: 1.2, h: 1.4,
      fontSize: 20, color: C.white, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
    });

    // 3 outcome cards
    const cards = [
      { title: "Accurate Severity %", desc: "Provides exact infection percentage (e.g., 32% affected)", color: C.primary },
      { title: "Data-Driven Decisions", desc: "Enables targeted pesticide application and treatment planning", color: C.teal },
      { title: "Pixel-Level Precision", desc: "Output generated from Modified U-Net binary segmentation mask", color: "6D28D9" }
    ];

    for (let i = 0; i < 3; i++) {
      const x = 0.35 + i * 3.18;
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: 2.95, w: 2.95, h: 2.35,
        fill: { color: C.lightgray }, line: { color: "E2E8F0", pt: 1 }
      });
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: 2.95, w: 2.95, h: 0.06,
        fill: { color: cards[i].color }, line: { color: cards[i].color }
      });
      slide.addText(cards[i].title, {
        x: x + 0.15, y: 3.1, w: 2.65, h: 0.55,
        fontSize: 13, color: C.text, bold: true, fontFace: "Calibri", margin: 0
      });
      slide.addText(cards[i].desc, {
        x: x + 0.15, y: 3.68, w: 2.65, h: 1.45,
        fontSize: 11.5, color: C.gray, fontFace: "Calibri", margin: 0
      });
    }
  }

  // ─────────────────────────────────────────
  // SLIDE 7: WORK PLAN & TIMELINE
  // ─────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.white };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 1.0,
      fill: { color: C.dark }, line: { color: C.dark }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 1.0,
      fill: { color: C.accent }, line: { color: C.accent }
    });
    slide.addText("Work Plan & Timeline", {
      x: 0.3, y: 0.1, w: 7, h: 0.8,
      fontSize: 28, color: C.white, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText("07", {
      x: 8.8, y: 0.1, w: 1.0, h: 0.8,
      fontSize: 36, color: C.accent, bold: true, fontFace: "Calibri", align: "center", valign: "middle", margin: 0
    });

    const phases = [
      { phase: "Phase 1", activity: "Data Collection & Preprocessing", duration: "Week 1–2", items: ["Collect from PlantVillage & field", "Clean, resize, normalize images", "Perform data augmentation"] },
      { phase: "Phase 2", activity: "Model Training & Fine-Tuning", duration: "Week 3–4", items: ["Implement MobileNetV2", "Train & fine-tune classifier", "Develop Modified U-Net"] },
      { phase: "Phase 3", activity: "Segmentation & DSI Calculation", duration: "Week 5–6", items: ["Pixel-level infection detection", "Compute Disease Severity Index", "Integrate modules"] },
      { phase: "Phase 4", activity: "Testing, Optimization & Docs", duration: "Week 7–8", items: ["Validate accuracy & performance", "Optimize for lightweight use", "Prepare documentation"] }
    ];

    const colors = [C.primary, C.teal, "7C3AED", "B45309"];
    for (let i = 0; i < 4; i++) {
      const p = phases[i];
      const x = 0.25 + i * 2.4;

      // Phase column header
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: 1.1, w: 2.2, h: 0.65,
        fill: { color: colors[i] }, line: { color: colors[i] }
      });
      slide.addText(p.phase, {
        x, y: 1.1, w: 2.2, h: 0.32,
        fontSize: 13, color: C.white, bold: true, align: "center", fontFace: "Calibri", margin: 0
      });
      slide.addText(p.duration, {
        x, y: 1.42, w: 2.2, h: 0.3,
        fontSize: 10, color: "D1FAE5", align: "center", fontFace: "Calibri", margin: 0
      });

      // Activity name
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: 1.78, w: 2.2, h: 0.7,
        fill: { color: C.lightgray }, line: { color: "E2E8F0", pt: 1 }
      });
      slide.addText(p.activity, {
        x: x + 0.1, y: 1.82, w: 2.0, h: 0.6,
        fontSize: 11, color: C.text, bold: true, fontFace: "Calibri", margin: 0
      });

      // Items
      for (let j = 0; j < p.items.length; j++) {
        slide.addShape(pres.shapes.RECTANGLE, {
          x, y: 2.55 + j * 0.95, w: 2.2, h: 0.85,
          fill: { color: C.white }, line: { color: "E2E8F0", pt: 1 }
        });
        slide.addShape(pres.shapes.OVAL, {
          x: x + 0.1, y: 2.68 + j * 0.95, w: 0.22, h: 0.22,
          fill: { color: colors[i] }, line: { color: colors[i] }
        });
        slide.addText(p.items[j], {
          x: x + 0.38, y: 2.57 + j * 0.95, w: 1.75, h: 0.75,
          fontSize: 10, color: C.gray, fontFace: "Calibri", margin: 0
        });
      }
    }
  }

  // ─────────────────────────────────────────
  // SLIDE 8: EXPECTED OUTCOME
  // ─────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.white };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 1.0,
      fill: { color: C.dark }, line: { color: C.dark }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 1.0,
      fill: { color: C.accent }, line: { color: C.accent }
    });
    slide.addText("Expected Outcome", {
      x: 0.3, y: 0.1, w: 7, h: 0.8,
      fontSize: 28, color: C.white, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText("08", {
      x: 8.8, y: 0.1, w: 1.0, h: 0.8,
      fontSize: 36, color: C.accent, bold: true, fontFace: "Calibri", align: "center", valign: "middle", margin: 0
    });

    // Product outputs (left col)
    slide.addText("Product / Research Output", {
      x: 0.3, y: 1.1, w: 4.5, h: 0.38,
      fontSize: 14, color: C.primary, bold: true, fontFace: "Calibri", margin: 0
    });

    const outputs = [
      "Lightweight AI system for real-time crop disease identification",
      "Pixel-level segmentation model for infection localization",
      "DSI computation for precise severity percentage",
      "User-friendly prototype for mobile or web deployment"
    ];

    for (let i = 0; i < outputs.length; i++) {
      slide.addShape(pres.shapes.RECTANGLE, {
        x: 0.3, y: 1.55 + i * 0.85, w: 4.7, h: 0.72,
        fill: { color: C.light }, line: { color: C.accent, pt: 1 }
      });
      slide.addShape(pres.shapes.OVAL, {
        x: 0.45, y: 1.68 + i * 0.85, w: 0.28, h: 0.28,
        fill: { color: C.primary }, line: { color: C.primary }
      });
      slide.addText(outputs[i], {
        x: 0.82, y: 1.57 + i * 0.85, w: 4.05, h: 0.65,
        fontSize: 11.5, color: C.text, fontFace: "Calibri", margin: 0
      });
    }

    // SDG mapping (right col)
    slide.addText("SDG Mapping", {
      x: 5.3, y: 1.1, w: 4.3, h: 0.38,
      fontSize: 14, color: C.primary, bold: true, fontFace: "Calibri", margin: 0
    });

    const sdgs = [
      { num: "SDG 2", label: "Zero Hunger", desc: "Supports food security by reducing crop losses through early disease detection.", color: "F59E0B" },
      { num: "SDG 9", label: "Industry, Innovation & Infrastructure", desc: "Promotes technological innovation in digital agriculture.", color: C.teal },
      { num: "SDG 12", label: "Responsible Consumption & Production", desc: "Encourages optimized pesticide usage through severity-based treatment.", color: C.primary }
    ];

    for (let i = 0; i < 3; i++) {
      const sdg = sdgs[i];
      slide.addShape(pres.shapes.RECTANGLE, {
        x: 5.3, y: 1.55 + i * 1.15, w: 4.3, h: 1.0,
        fill: { color: C.lightgray }, line: { color: "E2E8F0", pt: 1 }
      });
      slide.addShape(pres.shapes.RECTANGLE, {
        x: 5.3, y: 1.55 + i * 1.15, w: 0.07, h: 1.0,
        fill: { color: sdg.color }, line: { color: sdg.color }
      });
      slide.addText(sdg.num + " — " + sdg.label, {
        x: 5.5, y: 1.6 + i * 1.15, w: 4.0, h: 0.32,
        fontSize: 11.5, color: sdg.color, bold: true, fontFace: "Calibri", margin: 0
      });
      slide.addText(sdg.desc, {
        x: 5.5, y: 1.92 + i * 1.15, w: 4.0, h: 0.5,
        fontSize: 10.5, color: C.gray, fontFace: "Calibri", margin: 0
      });
    }
  }

  // ─────────────────────────────────────────
  // SLIDE 9: PUBLICATION & PATENT PLAN
  // ─────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.white };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 1.0,
      fill: { color: C.dark }, line: { color: C.dark }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 1.0,
      fill: { color: C.accent }, line: { color: C.accent }
    });
    slide.addText("Publication & Patent Plan", {
      x: 0.3, y: 0.1, w: 8, h: 0.8,
      fontSize: 28, color: C.white, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText("09", {
      x: 8.8, y: 0.1, w: 1.0, h: 0.8,
      fontSize: 36, color: C.accent, bold: true, fontFace: "Calibri", align: "center", valign: "middle", margin: 0
    });

    const plans = [
      {
        icon: FaBook,
        title: "Research Paper Submission",
        desc: "Prepare and submit a research paper to IEEE Access or Springer AI & Agriculture conference tracks, documenting the proposed hybrid framework and experimental results.",
        color: C.primary
      },
      {
        icon: FaFlask,
        title: "Intellectual Property Protection",
        desc: "Explore IP protection for the integrated lightweight DSI-based detection framework, covering the novel segmentation and severity estimation pipeline.",
        color: C.teal
      },
      {
        icon: FaMobileAlt,
        title: "Patent Filing (Future Scope)",
        desc: "Future enhancement of the system may lead to patent filing for the mobile-based real-time crop disease severity estimation system.",
        color: "7C3AED"
      }
    ];

    for (let i = 0; i < 3; i++) {
      const p = plans[i];
      const y = 1.25 + i * 1.38;

      slide.addShape(pres.shapes.RECTANGLE, {
        x: 0.3, y, w: 9.3, h: 1.2,
        fill: { color: C.lightgray }, line: { color: "E2E8F0", pt: 1 },
        shadow: { type: "outer", blur: 4, offset: 2, angle: 135, color: "000000", opacity: 0.08 }
      });
      slide.addShape(pres.shapes.RECTANGLE, {
        x: 0.3, y, w: 0.07, h: 1.2,
        fill: { color: p.color }, line: { color: p.color }
      });

      // Number badge
      slide.addShape(pres.shapes.OVAL, {
        x: 0.5, y: y + 0.08, w: 0.7, h: 0.7,
        fill: { color: p.color }, line: { color: p.color }
      });
      slide.addText(String(i + 1), {
        x: 0.5, y: y + 0.08, w: 0.7, h: 0.7,
        fontSize: 18, color: C.white, bold: true, align: "center", valign: "middle", fontFace: "Calibri", margin: 0
      });

      slide.addText(p.title, {
        x: 1.35, y: y + 0.1, w: 8.1, h: 0.32,
        fontSize: 13, color: C.text, bold: true, fontFace: "Calibri", margin: 0
      });
      slide.addText(p.desc, {
        x: 1.35, y: y + 0.45, w: 8.1, h: 0.65,
        fontSize: 11.5, color: C.gray, fontFace: "Calibri", margin: 0
      });
    }
  }

  // ─────────────────────────────────────────
  // SLIDE 10: CONCLUSION
  // ─────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.dark };

    // Left accent
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 5.625,
      fill: { color: C.accent }, line: { color: C.accent }
    });

    slide.addText("Conclusion", {
      x: 0.4, y: 0.3, w: 9, h: 0.7,
      fontSize: 34, color: C.white, bold: true, fontFace: "Calibri", margin: 0
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.4, y: 1.05, w: 4.5, h: 0.04,
      fill: { color: C.accent }, line: { color: C.accent }
    });

    // Summary box
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.4, y: 1.2, w: 9.2, h: 1.55,
      fill: { color: "0A1A2E" }, line: { color: C.teal, pt: 1 }
    });
    slide.addText("Summary", {
      x: 0.6, y: 1.28, w: 8.8, h: 0.32,
      fontSize: 13, color: C.accent, bold: true, fontFace: "Calibri", margin: 0
    });
    slide.addText("This project presents a computationally efficient, lightweight AI-based system for crop disease detection and severity analysis. By integrating transfer learning–based classification with pixel-level segmentation, the system accurately identifies diseases and computes the Disease Severity Index (DSI). The solution supports real-time deployment and enables precision agriculture through data-driven decision-making.",
      {
        x: 0.6, y: 1.6, w: 8.8, h: 1.0,
        fontSize: 11.5, color: C.light, fontFace: "Calibri", margin: 0
      }
    );

    // Future scope heading
    slide.addText("Future Scope", {
      x: 0.4, y: 2.9, w: 9, h: 0.35,
      fontSize: 14, color: C.accent, bold: true, fontFace: "Calibri", margin: 0
    });

    const futures = [
      "Expansion to support multiple crops and larger real-world datasets",
      "Fully functional mobile application for farmer accessibility",
      "Integration with IoT sensors and cloud-based monitoring systems",
      "AI-based treatment recommendation systems",
      "Field-level testing and large-scale smart farming deployment"
    ];

    for (let i = 0; i < futures.length; i++) {
      const col = i < 3 ? 0 : 1;
      const row = i < 3 ? i : i - 3;
      const x = 0.4 + col * 4.9;
      const y = 3.35 + row * 0.65;
      slide.addShape(pres.shapes.OVAL, {
        x, y: y + 0.07, w: 0.22, h: 0.22,
        fill: { color: C.accent }, line: { color: C.accent }
      });
      slide.addText(futures[i], {
        x: x + 0.32, y, w: 4.4, h: 0.55,
        fontSize: 11, color: C.light, fontFace: "Calibri", margin: 0
      });
    }
  }

  // ─────────────────────────────────────────
  // SLIDE 11: REFERENCES
  // ─────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.white };

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 1.0,
      fill: { color: C.dark }, line: { color: C.dark }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 1.0,
      fill: { color: C.accent }, line: { color: C.accent }
    });
    slide.addText("References", {
      x: 0.3, y: 0.1, w: 7, h: 0.8,
      fontSize: 28, color: C.white, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText("11", {
      x: 8.8, y: 0.1, w: 1.0, h: 0.8,
      fontSize: 36, color: C.accent, bold: true, fontFace: "Calibri", align: "center", valign: "middle", margin: 0
    });

    const refs = [
      { num: "[1]", ref: "Food and Agriculture Organization (FAO), 2024. Global Crop Loss Statistics and Plant Disease Impact Report." },
      { num: "[2]", ref: "Shoaib, M. et al., 2023. \"Deep Learning-Based Crop Disease Classification Using CNN,\" Journal of Agricultural Science." },
      { num: "[3]", ref: "IEEE Access, 2024. \"Transfer Learning Approaches for Plant Disease Detection in Precision Agriculture.\"" },
      { num: "[4]", ref: "World Agri-Tech Report, 2024. Digital Agriculture and Smart Farming Trends." },
      { num: "[5]", ref: "Mohanty, S.P., Hughes, D.P., & Salathé, M., 2016. \"Using Deep Learning for Image-Based Plant Disease Detection,\" Frontiers in Plant Science." }
    ];

    for (let i = 0; i < refs.length; i++) {
      const y = 1.1 + i * 0.88;
      slide.addShape(pres.shapes.RECTANGLE, {
        x: 0.3, y, w: 9.3, h: 0.75,
        fill: { color: i % 2 === 0 ? C.lightgray : C.white }, line: { color: "E2E8F0", pt: 1 }
      });
      slide.addText(refs[i].num, {
        x: 0.4, y: y + 0.05, w: 0.5, h: 0.65,
        fontSize: 13, color: C.primary, bold: true, fontFace: "Calibri", valign: "middle", margin: 0
      });
      slide.addText(refs[i].ref, {
        x: 0.95, y: y + 0.05, w: 8.5, h: 0.65,
        fontSize: 11, color: C.text, fontFace: "Calibri", valign: "middle", margin: 0
      });
    }
  }

  await pres.writeFile({ fileName: "/home/claude/crop_disease_detection.pptx" });
  console.log("Done!");
}

main().catch(console.error);