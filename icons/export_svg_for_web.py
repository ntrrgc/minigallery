#!/usr/bin/env python3
from argparse import ArgumentParser
import os
from pathlib import Path
import subprocess
import typing
from lxml import etree

USAGE = """
export_svg_for_web.py icons-source.svg icons.svg
"""

DESCRIPTION = """
Given an Inkscape SVG with labeled pages, this tool invokes Inkscape to export
a plain SVG version, then patches it to add a <view> element for each page with
an id matching its label.

This allows to refer to the contents of a page in a URL via hash.

Page with label "enter_fullscreen" becomes accessible as output.svg#page-enter-fullscreen.
"""

def main():
    parser = ArgumentParser(usage=USAGE, description=DESCRIPTION)
    parser.add_argument("input", type=Path, help="Input Inkscape SVG")
    parser.add_argument("output", type=Path, help="Output plain SVG that will be used in the web page")

    args = parser.parse_args()
    export_svg_for_web(args.input, args.output)

def export_svg_for_web(input_path: Path, output_path: Path):
    INKSCAPE = os.environ.get("INKSCAPE", "inkscape")
    subprocess.check_call([INKSCAPE, "--export-plain-svg", f"--export-filename={output_path}", "--", input_path])
    patch_svg(input_path, output_path)

@typing.no_type_check
def patch_svg(input_path: Path, output_path: Path):
    input_tree = etree.parse(input_path)
    output_tree = etree.parse(output_path)
    ns = {
        "": "http://www.w3.org/2000/svg",
        "svg": "http://www.w3.org/2000/svg",
        "inkscape": "http://www.inkscape.org/namespaces/inkscape",
        "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
    }
    pages = input_tree.findall("./sodipodi:namedview/inkscape:page", ns)
    views = [view_from_page(page) for page in pages]
    output_tree.getroot().extend(views)
    output_tree.write(output_path)

@typing.no_type_check
def view_from_page(page):
    a = page.attrib
    label = a["{http://www.inkscape.org/namespaces/inkscape}label"]
    return etree.Element("view", {
        "id": f"page-{label.replace('_', '-')}",
        "viewBox": f"{a['x']} {a['y']} {a['width']} {a['height']}",
    })

if __name__ == '__main__':
    main()