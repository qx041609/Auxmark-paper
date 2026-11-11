# Repository Guidelines

## Project Structure & Module Organization

This repository contains the AuxMark research manuscript, built with LaTeX using the IEEE conference layout. `00_main.tex` is the entry point; numbered `.tex` files contain the abstract, introduction, preliminaries, construction, experiments, conclusion, and appendix. Inclusion order is defined by `\input` statements, not filenames. `06_similarity_attribution.tex` and `10_related.tex` are currently empty and unused.

`math_commands.tex` holds shared notation; `09_reference.bib` holds references. `figure/` contains artwork, generated PDFs, and four `generate_*.py` plotting scripts. Root Markdown files include research notes and section-specific `*_writing_harness.md` guidance. Read relevant guidance before editing a section.

## Build, Test, and Development Commands

Run commands from the repository root. Install a TeX distribution with `IEEEtran`, BibTeX, and `latexmk`; figure generation also requires Python and Matplotlib.

- `latexmk -pdf -synctex=1 -interaction=nonstopmode -file-line-error 00_main.tex` builds the manuscript and bibliography, matching the VS Code LaTeX Workshop configuration.
- `python3 figure/generate_robustness.py` regenerates robustness figures.
- `python3 figure/generate_harmlessness.py` regenerates harmlessness figures.
- `python3 figure/generate_trace_attribution.py` regenerates attribution figures.
- `python3 figure/generate_training_share_sensitivity.py` regenerates sensitivity figures from the Markdown result table.

## Coding Style & Naming Conventions

Preserve surrounding LaTeX formatting and avoid unrelated paragraph reflow. Reuse existing macros such as `\name{}` and shared mathematical notation. Use descriptive labels with prefixes such as `sec:`, `fig:`, and `equ:`; preserve existing references when renaming labels.

Python scripts use four-space indentation, snake_case functions, and uppercase plotting constants. Keep visual parameters near the top and output files under `figure/`. No formatter or linter configuration is included.

## Validation Guidelines

There is no automated test suite or coverage requirement. Rebuild after manuscript changes; check for unresolved citations, references, and layout warnings. Inspect affected PDF pages for clipped figures, overflowing equations, and table alignment. After plot changes, run the relevant generator and compare values against the source records. Do not change experimental results without supporting evidence.

## Commit & Pull Request Guidelines

The available history contains one imperative commit: `Add IEEE S&P paper source and compiled PDF`. Follow that concise style and keep changes focused. PR descriptions should explain the affected sections, rationale, and validation performed; link relevant issues and include page previews for layout changes. Review tracked PDF and `.bbl` changes deliberately, and keep ignored build intermediates out of commits.
