from datetime import date
import os
from fpdf import FPDF
from PIL import Image, ImageDraw
import requests

GOWN_STYLES = {
    "Classic Navy": {"gown": (25, 45, 90), "trim": (218, 165, 32)},
    "Crimson Scholar": {"gown": (140, 20, 40), "trim": (240, 240, 240)},
    "Emerald Honors": {"gown": (20, 95, 65), "trim": (255, 215, 0)},
    "Royal Purple": {"gown": (75, 35, 115), "trim": (218, 165, 32)},
}

HONORS_LIST = [
    "Cum Laude",
    "Magna Cum Laude",
    "Summa Cum Laude",
    "With Distinction",
]


class Graduate:
    def __init__(
        self,
        name: str,
        degree: str,
        gown_style: str = "Classic Navy",
        honors: str = "Summa Cum Laude",
    ):
        if not name or not name.strip():
            raise ValueError("Graduate name cannot be empty")
        if gown_style not in GOWN_STYLES:
            raise ValueError(f"Unknown gown style: {gown_style}")
        self.name = name.strip()
        self.degree = degree.strip() or "Bachelor of Science in Computer Science"
        self.gown_style = gown_style
        self.honors = honors if honors in HONORS_LIST else HONORS_LIST[0]
        self.colors = GOWN_STYLES[gown_style]

    def summary(self) -> dict:
        return {
            "name": self.name,
            "degree": self.degree,
            "gown_style": self.gown_style,
            "honors": self.honors,
        }


def fetch_quote() -> str:
    """Fetches an inspirational graduation quote from a public API with a safe fallback."""
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=4)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data and "q" in data[0] and "a" in data[0]:
            return f'"{data[0]["q"]}" - {data[0]["a"]}'
    except Exception:
        pass
    return '"The future belongs to those who believe in the beauty of their dreams." - Eleanor Roosevelt'


def generate_regalia_gif(grad: Graduate, output_path: str = "regalia.gif") -> str:
    """Generates a multi-frame animated GIF showing gown changes and a cap toss."""
    frames = []
    style_keys = list(GOWN_STYLES.keys())
    sequence = [GOWN_STYLES[k] for k in style_keys] + [grad.colors] * 4

    for idx, palette in enumerate(sequence):
        img = Image.new("RGB", (320, 320), (248, 250, 252))
        draw = ImageDraw.Draw(img)

        gown_color = palette["gown"]
        trim_color = palette["trim"]

        if idx >= len(style_keys):
            confetti_y = 20 + (idx - len(style_keys)) * 12
            for cx in range(40, 290, 45):
                draw.ellipse([cx, confetti_y, cx + 8, confetti_y + 8], fill=trim_color)

        draw.polygon([(115, 145), (205, 145), (235, 290), (85, 290)], fill=gown_color)
        draw.polygon([(115, 145), (75, 235), (100, 245), (125, 180)], fill=gown_color)
        draw.polygon([(205, 145), (245, 235), (220, 245), (195, 180)], fill=gown_color)
        draw.polygon(
            [(135, 145), (160, 215), (185, 145), (173, 145), (160, 190), (147, 145)],
            fill=trim_color,
        )
        draw.ellipse([130, 82, 190, 142], fill=(242, 205, 175))

        cap_lift = max(0, (idx - len(style_keys) + 1) * 14)
        cap_y = 75 - cap_lift
        draw.polygon(
            [(160, cap_y - 18), (215, cap_y), (160, cap_y + 18), (105, cap_y)],
            fill=gown_color,
        )
        draw.line([(160, cap_y), (205, cap_y + 22)], fill=trim_color, width=3)

        frames.append(img)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=350,
        loop=0,
    )
    return output_path


def create_diploma_pdf(
    grad: Graduate, quote: str, gif_path: str, output_path: str = "diploma.pdf"
) -> str:
    """Creates a formatted graduation diploma PDF using fpdf2 HTML rendering and copyright footer."""
    safe_quote = (
        quote.replace("—", "-")
        .replace("–", "-")
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
    )

    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()

    r, g, b = grad.colors["gown"]
    tr, tg, tb = grad.colors["trim"]
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(3)
    pdf.rect(10, 10, 277, 190)
    pdf.set_draw_color(tr, tg, tb)
    pdf.set_line_width(1)
    pdf.rect(14, 14, 269, 182)

    today_str = date.today().strftime("%B %d, %Y")
    html_content = f"""
    <h1 align="center">CERTIFICATE OF GRADUATION</h1>
    <p align="center"><i>This certifies that</i></p>
    <h2 align="center">{grad.name}</h2>
    <p align="center">has fulfilled all requirements and is hereby awarded the degree of</p>
    <h3 align="center">{grad.degree}</h3>
    <p align="center"><b>Honors Distinction:</b> {grad.honors} &nbsp;|&nbsp; <b>Regalia:</b> {grad.gown_style}</p>
    <p align="center">Conferred on {today_str}</p>
    <br>
    <p align="center"><i>{safe_quote}</i></p>
    """
    pdf.set_y(24)
    pdf.set_font("helvetica", size=13)
    pdf.write_html(html_content)

    if os.path.exists(gif_path):
        pdf.image(gif_path, x=128, y=132, w=40)

    pdf.set_y(178)
    pdf.set_font("helvetica", size=9)
    pdf.write_html('<p align="center">&copy; 2026 Sabina Dovlati. All rights reserved.</p>')

    pdf.output(output_path)
    return output_path


def main():
    name = input("Enter graduate's full name: ")
    degree = input("Enter degree title: ")
    print("Available gown styles:", ", ".join(GOWN_STYLES.keys()))
    gown = input("Choose gown style (or press Enter for Classic Navy): ").strip() or "Classic Navy"
    honors = input("Choose honors (or press Enter for Summa Cum Laude): ").strip() or "Summa Cum Laude"

    grad = Graduate(name=name, degree=degree, gown_style=gown, honors=honors)
    quote = fetch_quote()
    gif_file = generate_regalia_gif(grad, "regalia.gif")
    pdf_file = create_diploma_pdf(grad, quote, gif_file, "diploma.pdf")
    print(f"Generated {gif_file} and {pdf_file} for {grad.name}!")


if __name__ == "__main__":
    main()