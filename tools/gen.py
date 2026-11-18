#!/usr/bin/env python3
import base64
import json
import random
import sys
from math import cos, pi, sin
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

CONFIG = {
    "name": "Mederich",
    "avatar": ROOT / "assets" / "garfield.jpg",
    "description": [
        "I'm a full stack development student and I try a bit of",
        "everything, whenever something looks interesting to me.",
        "I don't have one single field: I dive into whatever I feel",
        "like, I test, I build, and I learn by doing.",
    ],
    "skills": [
        "Rust", "JavaScript", "TypeScript",
        "Python", "React", "Node.js",
        "PostgreSQL", "Git", "Docker",
    ],
    "achievements": [
        ("Full Stack Developer", "From front to back, in training", True),
        ("DevFest", "Attended the DevFest conference", True),
        ("Member since 2022", "Joined GitHub on April 18, 2022", True),
        ("863 contributions", "A growing activity history", True),
    ],
    "projects": [
        ("RODIN", "Personal library + social network", "Status: in development"),
        ("LLM", "Building my own language model", "Status: in development"),
        ("SERVER", "My own server with full CI/CD", "Status: in development"),
    ],
    "contributions": 863,
    "joined": "APRIL 18, 2022",
    "roadmap": [
        ("Rodin online", "Publish the application"),
        ("My own LLM", "Build my own model"),
        ("Google Certification", "Validate my skills"),
        ("AWS Certification", "Validate my skills"),
    ],
    "links": ["LinkedIn", "Portfolio"],
    "sections": {
        "vitrine": "Technologies",
        "succes": "Achievements",
        "projets": "Current Projects",
        "stats": "Statistics",
        "roadmap": "Roadmap",
    },
}

BG0, BG1, PANEL, LINE = "#0a0a09", "#121211", "#171715", "#2b2a27"
G1, G2, G3, CREAM = "#3a3732", "#6b665c", "#a39d8f", "#e9e0cc"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "'Segoe UI', Helvetica, Arial, sans-serif"
WIDTH = 830
ROUGH = 'filter="url(#rough2)"'


def head(w, h, extra=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
<filter id="rough" filterUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">
  <feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves="3" seed="3" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="12" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="rough2" filterUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">
  <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="9" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="4" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="dry" filterUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">
  <feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves="3" seed="3" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="12" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feTurbulence type="fractalNoise" baseFrequency="0.004 0.5" numOctaves="2" seed="4" result="t"/>
  <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  5 0 0 0 -1.7" result="m"/>
  <feComposite in="d" in2="m" operator="in"/>
</filter>
<filter id="grain" filterUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">
  <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0.91  0 0 0 0 0.88  0 0 0 0 0.8  9 0 0 0 -5.3"/>
</filter>
{extra}
</defs>
'''


def text(x, y, content, size, fill, font=SANS, weight=None, style=None, spacing=None, anchor=None, filt=False):
    attrs = [f'x="{x}"', f'y="{y}"']
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    attrs += [f'font-family="{font}"', f'font-size="{size}"']
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if style:
        attrs.append(f'font-style="{style}"')
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    attrs.append(f'fill="{fill}"')
    if filt:
        attrs.append(ROUGH)
    return f'<text {" ".join(attrs)}>{escape(str(content))}</text>'


def rough_rect(x, y, w, h, fill, stroke=None, stroke_width=None):
    border = f' stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ""
    return f'<g {ROUGH}><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{border}/></g>'


def fade_in(delay):
    return f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="{delay:.2f}s" fill="freeze"/>'


def grid(count, cols, gap, th):
    rows = -(-count // cols)
    tw = (WIDTH - gap * (cols - 1)) / cols
    return tw, rows * th + (rows - 1) * gap + 4


def splatter(rng, x0, x1, y0, y1, n, cols=(CREAM, G3, G2)):
    out = []
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        r = rng.choice([0.8, 1, 1.3, 1.8, 2.5, 3.4])
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{rng.choice(cols)}" opacity="{rng.uniform(.35, .9):.2f}"/>')
    return "".join(out)


def painted_planes(rng, w, h, light="right", strength=1.0):
    s = []
    if light == "right":
        s.append(f'<g filter="url(#rough)"><polygon points="0,0 {w*.62:.0f},0 {w*.45:.0f},{h} 0,{h}" fill="#141412"/>'
                 f'<polygon points="{w*.62:.0f},0 {w},0 {w},{h} {w*.36:.0f},{h}" fill="#1d1c19"/>'
                 f'<polygon points="{w*.72:.0f},0 {w},0 {w},{h} {w*.6:.0f},{h}" fill="#282622"/></g>')
        s.append(f'<g filter="url(#dry)" opacity="{.9*strength:.2f}"><polygon points="{w*.8:.0f},{h*.08:.0f} {w},{h*.02:.0f} {w},{h*.85:.0f} {w*.74:.0f},{h*.95:.0f}" fill="#4b473f"/>'
                 f'<polygon points="{w*.9:.0f},0 {w},0 {w},{h*.5:.0f} {w*.86:.0f},{h*.6:.0f}" fill="#8d8675"/></g>')
    else:
        s.append(f'<g filter="url(#rough)"><polygon points="0,0 {w},0 {w},{h} 0,{h}" fill="#141412"/>'
                 f'<polygon points="0,0 {w*.55:.0f},0 {w*.3:.0f},{h} 0,{h}" fill="#25231f"/></g>')
        s.append(f'<g filter="url(#dry)" opacity="{.9*strength:.2f}"><polygon points="0,{h*.1:.0f} {w*.25:.0f},{h*.05:.0f} {w*.2:.0f},{h*.9:.0f} 0,{h}" fill="#4b473f"/></g>')
    strokes = []
    for _ in range(9):
        y = rng.uniform(0, h)
        x1 = rng.uniform(0, w * .6)
        x2 = x1 + rng.uniform(w * .25, w * .6)
        width = rng.uniform(14, 44)
        color = rng.choice([G1, G1, G2, G3])
        strokes.append(f'<line x1="{x1:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y + rng.uniform(-24, 24):.0f}" stroke="{color}" stroke-width="{width:.0f}" opacity="{rng.uniform(.25, .6):.2f}"/>')
    s.append(f'<g filter="url(#dry)">{"".join(strokes)}</g>')
    s.append(splatter(rng, w * .45, w, 0, h, 46))
    s.append(f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity=".42"/>')
    return "".join(s)


def banner(c):
    w, h = WIDTH, 250
    rng = random.Random(11)
    fade = (f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG0}" stop-opacity=".92"/>'
            f'<stop offset=".55" stop-color="{BG0}" stop-opacity=".55"/><stop offset="1" stop-color="{BG0}" stop-opacity="0"/></linearGradient>')
    ax, ay, size, tx = 34, 55, 140, 214
    avatar = base64.b64encode(c["avatar"].read_bytes()).decode()
    s = head(w, h, fade)
    s += f'<rect width="{w}" height="{h}" fill="{BG0}"/>'
    s += painted_planes(rng, w, h, "right")
    s += f'<rect width="{w}" height="{h}" fill="url(#fade)"/>'
    s += f'<rect x="{ax-5}" y="{ay-5}" width="{size+10}" height="{size+10}" fill="{BG1}" stroke="{CREAM}" stroke-width="2.5"/>'
    s += f'<image x="{ax}" y="{ay}" width="{size}" height="{size}" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{avatar}"/>'
    s += text(tx, 98, c["name"], 44, CREAM, font=SERIF, weight="bold", filt=True)
    for i, line in enumerate(c["description"]):
        s += text(tx, 128 + i * 22, line, 14, G3)
    return s + "</svg>"


def section(title):
    w, h = WIDTH, 46
    s = head(w, h)
    s += rough_rect(0, 12, 7, 22, CREAM)
    s += text(20, 30, title.upper(), 15, CREAM, weight="700", spacing="3.5")
    s += f'<g filter="url(#dry)"><line x1="0" y1="41" x2="{w}" y2="41" stroke="{G2}" stroke-width="5" opacity=".9"/></g>'
    s += f'<g filter="url(#dry)"><line x1="0" y1="41" x2="190" y2="41" stroke="{CREAM}" stroke-width="5"/></g>'
    return s + "</svg>"


def skills(c):
    icons = json.loads((Path(__file__).resolve().parent / "icons.json").read_text())
    cols, gap, th, scale = 3, 12, 80, 1.9
    tw, h = grid(len(c["skills"]), cols, gap, th)
    s = head(WIDTH, h)
    for i, name in enumerate(c["skills"]):
        x = (i % cols) * (tw + gap)
        y = (i // cols) * (th + gap)
        s += fade_in(0.12 * i)
        s += f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="{th}" fill="{PANEL}" stroke="{LINE}"/>'
        s += rough_rect(f"{x:.1f}", y, 4, th, CREAM)
        s += rough_rect(f"{x+18:.1f}", y + 12, 56, 56, BG1, G1, 2)
        if name in icons:
            s += f'<path transform="translate({x+46-12*scale:.1f} {y+40-12*scale:.1f}) scale({scale})" fill="{CREAM}" d="{icons[name]}"/>'
        s += text(f"{x+92:.1f}", f"{y+th/2+6:.0f}", name, 19, CREAM, weight="700")
        s += "</g>"
    return s + "</svg>"


def glyph(kind, cx, cy, col):
    if kind == 0:
        points = []
        for k in range(10):
            r = 15 if k % 2 == 0 else 6.5
            a = -pi / 2 + k * pi / 5
            points.append(f"{cx + r*cos(a):.1f},{cy + r*sin(a):.1f}")
        return f'<polygon points="{" ".join(points)}" fill="{col}"/>'
    if kind == 1:
        return (f'<g stroke="{col}" stroke-width="3.5" fill="none"><line x1="{cx-8}" y1="{cy-14}" x2="{cx-8}" y2="{cy+14}"/>'
                f'<path d="M{cx-8} {cy+4} C{cx-8} {cy-6} {cx+8} {cy-2} {cx+8} {cy-10}"/></g>'
                f'<circle cx="{cx-8}" cy="{cy-14}" r="4" fill="{col}"/><circle cx="{cx-8}" cy="{cy+14}" r="4" fill="{col}"/><circle cx="{cx+8}" cy="{cy-12}" r="4" fill="{col}"/>')
    if kind == 2:
        return f'<polygon points="{cx+3},{cy-16} {cx-10},{cy+2} {cx-1},{cy+2} {cx-4},{cy+16} {cx+10},{cy-4} {cx+1},{cy-4}" fill="{col}"/>'
    if kind == 3:
        return f'<circle cx="{cx}" cy="{cy}" r="12" fill="none" stroke="{col}" stroke-width="4"/><circle cx="{cx+12}" cy="{cy-2}" r="4" fill="{col}"/>'
    if kind == 4:
        return f'<polygon points="{cx},{cy-17} {cx+9},{cy+8} {cx},{cy+3} {cx-9},{cy+8}" fill="{col}"/><rect x="{cx-3}" y="{cy+9}" width="6" height="7" fill="{col}"/>'
    return f'<polygon points="{cx},{cy-16} {cx+15},{cy} {cx},{cy+16} {cx-15},{cy}" fill="none" stroke="{col}" stroke-width="4"/>'


def achievements(c):
    cols, gap, th = 2, 12, 72
    tw, h = grid(len(c["achievements"]), cols, gap, th)
    s = head(WIDTH, h)
    for i, (title, desc, unlocked) in enumerate(c["achievements"]):
        x = (i % cols) * (tw + gap)
        y = (i // cols) * (th + gap)
        ink = CREAM if unlocked else G2
        s += f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="{th}" fill="{PANEL}" stroke="{LINE}" opacity="{1 if unlocked else .75}"/>'
        s += rough_rect(f"{x+10:.1f}", y + 10, 52, 52, G1 if unlocked else BG1, CREAM if unlocked else G1, 2)
        s += f'<g {ROUGH}>{glyph(i, x+36, y+36, ink)}</g>'
        s += text(f"{x+78:.1f}", y + 30, title, 15, CREAM if unlocked else G3, weight="700")
        s += text(f"{x+78:.1f}", y + 51, desc, 12.5, G2)
        s += text(f"{x+tw-14:.1f}", y + 20, "UNLOCKED" if unlocked else "LOCKED", 10.5, G3 if unlocked else G2, spacing="1.5", anchor="end")
    return s + "</svg>"


def project(idx, x, title, line1, line2):
    w, h, art = 270, 250, 104
    rng = random.Random(100 + idx)
    s = f'<svg x="{x}" y="0" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
    s += f'<rect width="{w}" height="{h}" fill="{PANEL}" stroke="{LINE}"/>'
    s += f'<svg x="0" y="0" width="{w}" height="{art}" viewBox="0 0 {w} {art}">{painted_planes(rng, w, art, "right" if idx % 2 == 0 else "left", .8)}</svg>'
    s += f'<rect x="0" y="{art}" width="{w}" height="2" fill="{CREAM}" opacity=".8"/>'
    s += text(22, 140, title, 17, CREAM, weight="700", spacing="1.4")
    s += text(22, 166, line1, 14.5, G3)
    s += text(22, 188, line2, 13, G2)
    s += rough_rect(22, 204, 134, 30, CREAM)
    s += text(89, 224, "IN PROGRESS", 12.5, BG0, weight="700", spacing="1.5", anchor="middle")
    return s + "</svg>"


def projects(c):
    gap = 10
    s = head(WIDTH, 250)
    for i, (title, line1, line2) in enumerate(c["projects"]):
        s += project(i, i * (270 + gap), title, line1, line2)
    return s + "</svg>"


def button(label):
    w, h = 150, 38
    s = head(w, h)
    s += f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" fill="{PANEL}" stroke="{LINE}"/>'
    s += rough_rect(0, 0, 5, h, CREAM)
    s += text(w / 2 + 3, 24, label.upper(), 12.5, CREAM, weight="700", spacing="2", anchor="middle")
    return s + "</svg>"


def footer():
    w, h = WIDTH, 90
    rng = random.Random(77)
    s = head(w, h)
    s += f'<rect width="{w}" height="{h}" fill="{BG0}"/>'
    s += painted_planes(rng, w, h, "left", .7)
    s += f'<rect width="{w}" height="{h}" fill="{BG0}" opacity=".5"/>'
    s += text(w / 2, 52, "Feel free to contact me.", 20, CREAM, font=SERIF, style="italic", anchor="middle", filt=True)
    return s + "</svg>"


def contributions(c):
    w, h = 495, 165
    total = f"{c['contributions']:,}".replace(",", " ")
    s = head(w, h)
    s += f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="{BG1}" stroke="{LINE}"/>'
    s += rough_rect(0, 0, 5, h, CREAM)
    s += text(32, 38, "CONTRIBUTIONS", 12, G2, spacing="3")
    s += text(32, 98, total, 60, CREAM, font=SERIF.replace(",", " "), weight="bold", filt=True)
    s += f'<line x1="32" y1="118" x2="{w-32}" y2="118" stroke="{LINE}"/>'
    s += text(32, 143, "MEMBER SINCE", 12, G2, spacing="2.5")
    s += text(w - 32, 143, c["joined"], 14, CREAM, weight="700", spacing="1.5", anchor="end")
    return s + "</svg>"


def roadmap(c):
    gap, th = 12, 118
    n = len(c["roadmap"])
    tw = (WIDTH - gap * (n - 1)) / n
    s = head(WIDTH, th + 4)
    s += f'<g filter="url(#dry)"><line x1="0" y1="22" x2="{WIDTH}" y2="22" stroke="{G1}" stroke-width="4"/></g>'
    for i, (title, desc) in enumerate(c["roadmap"]):
        x = i * (tw + gap)
        s += fade_in(0.18 * i)
        s += f'<circle cx="{x+20:.1f}" cy="22" r="9" fill="{BG0}" stroke="{CREAM}" stroke-width="2.5"/>'
        s += f'<circle cx="{x+20:.1f}" cy="22" r="3" fill="{G3}"/>'
        s += f'<rect x="{x:.1f}" y="44" width="{tw:.1f}" height="{th-44}" fill="{PANEL}" stroke="{LINE}"/>'
        s += rough_rect(f"{x:.1f}", 44, 4, th - 44, G3)
        s += text(f"{x+18:.1f}", 66, "UPCOMING", 10.5, G2, spacing="2")
        s += text(f"{x+18:.1f}", 90, title, 15, CREAM, weight="700")
        s += text(f"{x+18:.1f}", 109, desc, 12.5, G2)
        s += "</g>"
    return s + "</svg>"


def main(out):
    c = CONFIG
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    files = {"banner": banner(c), "skills": skills(c), "roadmap": roadmap(c),
             "contributions": contributions(c), "projects": projects(c), "achievements": achievements(c), "footer": footer()}
    files.update({f"h-{key}": section(label) for key, label in c["sections"].items()})
    files.update({f"btn-{label.lower()}": button(label) for label in c["links"]})
    for name, svg in files.items():
        (out / f"{name}.svg").write_text(svg, encoding="utf-8")
    print("ok ->", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT / "assets")
