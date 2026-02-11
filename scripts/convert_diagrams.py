import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def convert_svg_to_png(svg_path, png_path):
    print(f"Converting {svg_path} to {png_path}...")
    try:
        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, png_path, fmt="PNG")
        print(f"Successfully converted {svg_path}")
    except Exception as e:
        print(f"Error converting {svg_path}: {e}")

diagrams_dir = r"c:\Users\pruth\OneDrive\Desktop\HealthAI Pro\healthcare-ml-project\diagrams"
svg_files = [
    "use-case-diagram.svg",
    "class-diagram.svg",
    "sequence-diagram.svg",
    "system-architecture.svg"
]

for svg_file in svg_files:
    svg_path = os.path.join(diagrams_dir, svg_file)
    png_path = os.path.join(diagrams_dir, svg_file.replace(".svg", ".png"))
    if os.path.exists(svg_path):
        convert_svg_to_png(svg_path, png_path)
    else:
        print(f"File not found: {svg_path}")
