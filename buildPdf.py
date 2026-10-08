"""Render extraCreditProposal.md to PDF so the Markdown stays the single source of truth.

Run with: eventManagementProject/.venv/bin/python buildPdf.py
"""

import argparse
import subprocess
import tempfile
from pathlib import Path

from markdown_it import MarkdownIt

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
CSS = """
@page { size: Letter; margin: 0.7in; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; line-height: 1.4; color: #111; }
h1 { font-size: 17pt; margin: 0 0 6pt; }
h2 { font-size: 13pt; margin-top: 14pt; padding-bottom: 2pt; border-bottom: 1px solid #999; }
li { margin-bottom: 2pt; }
"""


def renderHtml(markdownText: str, title: str) -> str:
    body = MarkdownIt("commonmark").enable("table").render(markdownText)
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'


def printPdf(html: str, pdfPath: Path, chrome: Path) -> None:
    if not chrome.exists():
        raise FileNotFoundError(f"Chrome not found at {chrome}; pass --chrome")
    with tempfile.TemporaryDirectory() as tmp:
        htmlPath = Path(tmp) / "proposal.html"
        htmlPath.write_text(html, encoding="utf-8")
        pdfPath.unlink(missing_ok=True)
        subprocess.run(
            [str(chrome), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={pdfPath}", htmlPath.as_uri()],
            check=True, capture_output=True,
        )
    if not pdfPath.exists() or pdfPath.stat().st_size == 0:
        raise RuntimeError(f"Chrome wrote no PDF at {pdfPath}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--src", type=Path, default=PROJECT_ROOT / "extraCreditProposal.md")
    parser.add_argument("--chrome", type=Path, default=DEFAULT_CHROME)
    args = parser.parse_args()

    text = args.src.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip()
    pdfPath = args.src.with_suffix(".pdf")
    printPdf(renderHtml(text, title), pdfPath, args.chrome)
    print(f"wrote {pdfPath} ({pdfPath.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
