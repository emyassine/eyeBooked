#!/usr/bin/env python3
"""Rebuild standalone EyeBooked brand assets from the colors and SVG mark in index-14.html."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOGOS = ROOT / "logos"
BACKGROUNDS = ROOT / "backgrounds"

THEMES = {
    "green": {
        "i": ["#F0FAF5", "#DDF3E8", "#B5E3CF", "#7CC7A8", "#3FA582", "#14805F", "#0B5D45", "#0A4F3A", "#063A2A", "#04271C"],
        "p": ["#F0FAF5", "#DDF3E8", "#B5E3CF", "#7CC7A8", "#3FA582", "#1E9972", "#14805F", "#0B5D45", "#0A4F3A", "#063A2A"],
        "g1": "#0B5D45", "g2": "#2FA37C", "g1d": "#3FA582", "g2d": "#7CC7A8", "g0": "#04271C",
        "b1": "#DDF3E8", "b2": "#F3FAF6", "b3": "#E1F2E9", "dk": "#063A2A",
        "au1": "#2FA37C", "au1a": 0x88 / 255, "au2": "#0B5D45", "au2a": 0x66 / 255, "au3": "#B5E3CF", "au3a": 0xAA / 255,
    },
    "blue": {
        "i": ["#F1F8FC", "#DCEFF8", "#C5EEF2", "#8FD3E6", "#61C5D8", "#3E93C8", "#2878B5", "#1E5E9A", "#153E75", "#0F2D57"],
        "p": ["#EEF9FC", "#D6F1F7", "#C5EEF2", "#9AE0EC", "#61C5D8", "#4AB0D0", "#3A98C4", "#2878B5", "#1E5E9A", "#153E75"],
        "g1": "#2878B5", "g2": "#61C5D8", "g1d": "#61C5D8", "g2d": "#8FD3E6", "g0": "#153E75",
        "b1": "#C5EEF2", "b2": "#F7FAFC", "b3": "#DCEBF7", "dk": "#153E75",
        "au1": "#61C5D8", "au1a": 0x88 / 255, "au2": "#2878B5", "au2a": 0x66 / 255, "au3": "#C5EEF2", "au3a": 0xAA / 255,
    },
    "violet": {
        "i": ["#EEF2FF", "#E0E7FF", "#C7D2FE", "#A5B4FC", "#818CF8", "#6366F1", "#4F46E5", "#4338CA", "#3730A3", "#312E81"],
        "p": ["#FAF5FF", "#F3E8FF", "#E9D5FF", "#D8B4FE", "#C084FC", "#A855F7", "#9333EA", "#7E22CE", "#6B21A8", "#581C87"],
        "g1": "#4F46E5", "g2": "#A855F7", "g1d": "#818CF8", "g2d": "#D8B4FE", "g0": "#312E81",
        "b1": "#E0E7FF", "b2": "#FCE7F3", "b3": "#D1FAE5", "dk": "#1E1B4B",
        "au1": "#A78BFA", "au1a": 0x88 / 255, "au2": "#22D3EE", "au2a": 0x66 / 255, "au3": "#FB7185", "au3a": 0xAA / 255,
    },
}


def logo_mark(theme: dict, dark: bool) -> str:
    first, second = (theme["g1d"], theme["g2d"]) if dark else (theme["g1"], theme["g2"])
    suffix = "dark" if dark else "light"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 0 120 120" role="img" aria-labelledby="title desc">
<title id="title">EyeBooked logo mark ({suffix} mode)</title><desc id="desc">Eye and location pin combined as a clean, scalable vector mark.</desc>
<defs><linearGradient id="mark-gradient" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{first}"/><stop offset="1" stop-color="{second}"/></linearGradient></defs>
<path d="M16 46C34 18 86 18 104 46" fill="none" stroke="url(#mark-gradient)" stroke-width="10" stroke-linecap="round"/>
<path d="M22 66L60 106L98 66" fill="none" stroke="url(#mark-gradient)" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="60" cy="58" r="22" fill="url(#mark-gradient)"/><circle cx="55" cy="53" r="15" fill="{theme['g0']}" opacity=".85"/><circle cx="68" cy="49" r="5" fill="#fff"/>
</svg>'''


def wordmark(theme: dict, dark: bool) -> str:
    eye = "#E0E7FF" if dark else theme["g0"]
    first, second = (theme["g1d"], theme["g2d"]) if dark else (theme["g1"], theme["g2"])
    mode = "dark" if dark else "light"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="600" viewBox="0 0 560 140" role="img" aria-labelledby="title desc">
<title id="title">EyeBooked wordmark ({mode} mode)</title><desc id="desc">EyeBooked set in Plus Jakarta Sans ExtraBold with the original two-tone brand color treatment.</desc>
<defs><linearGradient id="wordmark-gradient" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{first}"/><stop offset="1" stop-color="{second}"/></linearGradient></defs>
<text x="12" y="105" font-family="Plus Jakarta Sans" font-size="82" font-weight="800" letter-spacing="-3"><tspan fill="{eye}">Eye</tspan><tspan fill="url(#wordmark-gradient)">Booked</tspan></text>
</svg>'''


def lockup(theme: dict, dark: bool, splash: bool = False) -> str:
    first, second = (theme["g1d"], theme["g2d"]) if dark else (theme["g1"], theme["g2"])
    eye = "#E0E7FF" if dark else theme["g0"]
    if splash:
        first, second = theme["i"][6], theme["p"][6]
        eye, word_start, pupil, pupil_opacity, lower_opacity = "#FFFFFF", "#FFFFFF", "#1E1B4B", ".5", ".85"
        eye_markup = '<tspan fill="#FFFFFF">Eye</tspan><tspan fill="#FFFFFF" fill-opacity=".85">Booked</tspan>'
        tagline_color = "#FFFFFF"
        tagline_opacity = ".8"
        mark_arc, mark_lower, mark_iris, iris = "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"
        iris_opacity = ".7"
        bg = f'''<linearGradient id="splash-background" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{theme['i'][6]}"/><stop offset=".55" stop-color="{theme['p'][6]}"/><stop offset="1" stop-color="{theme['g2']}"/></linearGradient>'''
        background = '<rect width="480" height="320" fill="url(#splash-background)"/>'
    else:
        word_start, pupil, pupil_opacity, lower_opacity = eye, theme["g0"], ".85", "1"
        eye_markup = f'<tspan fill="{eye}">Eye</tspan><tspan fill="url(#wordmark-gradient)">Booked</tspan>'
        tagline_color, tagline_opacity = ("#E2E8F0", ".8") if dark else ("#64748B", "1")
        mark_arc = mark_lower = mark_iris = "url(#mark-gradient)"
        iris_opacity = "1"
        bg, background = "", ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="1600" viewBox="0 0 480 320" role="img" aria-labelledby="title desc">
<title id="title">EyeBooked {'splash' if splash else 'logo lockup'} ({'reversed' if splash else ('dark' if dark else 'light')} mode)</title><desc id="desc">The original EyeBooked eye-and-pin symbol, ExtraBold wordmark, and French tagline.</desc>
<defs>{bg}<linearGradient id="mark-gradient" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{first}"/><stop offset="1" stop-color="{second}"/></linearGradient><linearGradient id="wordmark-gradient" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{first}"/><stop offset="1" stop-color="{second}"/></linearGradient></defs>
{background}
<g transform="translate(180 12) scale(1)" fill="none"><path d="M16 46C34 18 86 18 104 46" stroke="{mark_arc}" stroke-width="10" stroke-linecap="round"/><path d="M22 66L60 106L98 66" stroke="{mark_lower}" stroke-opacity="{lower_opacity}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/><circle cx="60" cy="58" r="22" fill="{mark_iris}" fill-opacity="{iris_opacity}"/><circle cx="55" cy="53" r="15" fill="{pupil}" opacity="{pupil_opacity}"/><circle cx="68" cy="49" r="5" fill="#fff"/></g>
<text x="240" y="203" text-anchor="middle" font-family="Plus Jakarta Sans" font-size="43" font-weight="800" letter-spacing="-1.6">{eye_markup}</text>
<text x="240" y="242" text-anchor="middle" font-family="Plus Jakarta Sans" font-size="15" font-weight="400" fill="{tagline_color}" fill-opacity="{tagline_opacity}">Your eye care, booked.</text>
</svg>'''


def background(theme: dict, dark: bool) -> str:
    if dark:
        start, end = "#020617", theme["dk"]
    else:
        start, end = theme["b1"], theme["b3"]
    stops = f'<stop offset="0" stop-color="{start}"/><stop offset=".5" stop-color="{theme["b2"] if not dark else theme["dk"]}"/><stop offset="1" stop-color="{end}"/>'
    overlay = "".join(
        f'<radialGradient id="glow{i}" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{theme[key]}" stop-opacity="{theme[alpha]:.4f}"/><stop offset="1" stop-color="{theme[key]}" stop-opacity="0"/></radialGradient>'
        for i, (key, alpha) in enumerate((("au1", "au1a"), ("au2", "au2a"), ("au3", "au3a")), 1)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="2560" height="1440" viewBox="0 0 2560 1440" role="img" aria-labelledby="title desc">
<title id="title">EyeBooked {'dark' if dark else 'light'} page background</title><desc id="desc">Static 2K export of the original page gradient and softly blurred aurora.</desc>
<defs><linearGradient id="base" x1="0" y1="1" x2="1" y2="0">{stops}</linearGradient>{overlay}<filter id="soften" x="-20%" y="-25%" width="140%" height="150%"><feGaussianBlur stdDeviation="60"/></filter></defs>
<rect width="2560" height="1440" fill="url(#base)"/>
<g filter="url(#soften)"><ellipse cx="205" cy="115" rx="1160" ry="830" fill="url(#glow1)"/><ellipse cx="2355" cy="375" rx="1050" ry="760" fill="url(#glow2)"/><ellipse cx="1280" cy="1525" rx="1200" ry="850" fill="url(#glow3)"/></g>
</svg>'''


def emit_svg_and_png(svg_text: str, stem: str, folder: Path, png_width: int) -> None:
    source = folder / f".{stem}.source.svg"
    svg = folder / f"{stem}.svg"
    png = folder / f"{stem}.png"
    source.write_text(svg_text, encoding="utf-8")
    if "<text" in svg_text:
        subprocess.run(["inkscape", str(source), "--export-text-to-path", f"--export-filename={svg}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        svg.write_text(svg_text, encoding="utf-8")
    subprocess.run(["inkscape", str(svg), f"--export-width={png_width}", f"--export-filename={png}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    source.unlink(missing_ok=True)


def main() -> None:
    logos_only = "--logos-only" in sys.argv
    LOGOS.mkdir(parents=True, exist_ok=True)
    BACKGROUNDS.mkdir(parents=True, exist_ok=True)
    fontconfig = Path(tempfile.gettempdir()) / f"eyebooked-fontconfig-{os.getpid()}.conf"
    old_fontconfig = os.environ.get("FONTCONFIG_FILE")
    fontconfig.write_text(
        '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>'
        '<include>/etc/fonts/fonts.conf</include>'
        f'<dir>{ROOT / "fonts"}</dir></fontconfig>',
        encoding="utf-8",
    )
    os.environ["FONTCONFIG_FILE"] = str(fontconfig)
    try:
        subprocess.run(["fc-cache", "-f", str(ROOT / "fonts")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for theme_name, theme in THEMES.items():
            for dark in (False, True):
                mode = "dark" if dark else "light"
                emit_svg_and_png(logo_mark(theme, dark), f"eyebooked-mark-{theme_name}-{mode}", LOGOS, 2048)
                emit_svg_and_png(wordmark(theme, dark), f"eyebooked-wordmark-{theme_name}-{mode}", LOGOS, 3200)
                emit_svg_and_png(lockup(theme, dark), f"eyebooked-lockup-{theme_name}-{mode}", LOGOS, 2400)
                if not logos_only:
                    bg = BACKGROUNDS / f"eyebooked-background-{theme_name}-{mode}.svg"
                    bg.write_text(background(theme, dark), encoding="utf-8")
                    subprocess.run(["inkscape", str(bg), "--export-width=2560", "--export-height=1440", f"--export-filename={bg.with_suffix('.png')}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            emit_svg_and_png(lockup(theme, False, splash=True), f"eyebooked-splash-{theme_name}-reversed", LOGOS, 2400)
    finally:
        fontconfig.unlink(missing_ok=True)
        if old_fontconfig is None:
            os.environ.pop("FONTCONFIG_FILE", None)
        else:
            os.environ["FONTCONFIG_FILE"] = old_fontconfig

    if not logos_only:
        (ROOT / "palette.json").write_text(json.dumps(THEMES, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
