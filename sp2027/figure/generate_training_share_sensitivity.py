"""Generate six training-share sensitivity PDFs from the frozen result table.

The parameters near the top control the manuscript visual style.  The script
reads the source Markdown directly so its plotted median p-values remain
aligned with the experiment record.
"""

from __future__ import annotations

import math
import re
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


# ---------------------------------------------------------------------------
# Editable visual parameters
# ---------------------------------------------------------------------------
COLORS = {
    "Mistral-24B": "#E0795F",
    "GLM-4.7-Flash": "#F5B783",
    "Qwen3-14B": "#86BAD4",
    "Qwen3-32B": "#34669A",
}
MARKERS = {
    "Mistral-24B": "o",
    "GLM-4.7-Flash": "s",
    "Qwen3-14B": "^",
    "Qwen3-32B": "D",
}
FONT_SIZES = {
    "axis_label": 10.5,
    "tick": 9.5,
}
FIGURE_SIZE = (2.20, 1.78)  # width, height of each PDF in inches
LINE_WIDTH = 2.25
MARKER_SIZE = 4.6
THRESHOLD_COLOR = "#8C8C8C"
GRID_ALPHA = 0.25


# Shown from the observed C0/W50 anchor toward more severe dilution.
SHARES = [50, 40, 30, 20, 10]
AVAILABLE_SHARES = {5, 10, 15, 20, 25, 30, 35, 40, 45, 50}
MODEL_ORDER = ["Mistral-24B", "GLM-4.7-Flash", "Qwen3-14B", "Qwen3-32B"]
COHORT_ORDER = [
    "BFCL-GPT",
    "SWEbench-GPT",
    "Telecom-GPT",
    "BFCL-Kimi",
    "SWEbench-Kimi",
    "Telecom-Kimi",
]
OUTPUT_NAMES = {
    "BFCL-GPT": "training_share_bfcl_gpt.pdf",
    "SWEbench-GPT": "training_share_swe_bench_gpt.pdf",
    "Telecom-GPT": "training_share_telecom_gpt.pdf",
    "BFCL-Kimi": "training_share_bfcl_kimi.pdf",
    "SWEbench-Kimi": "training_share_swe_bench_kimi.pdf",
    "Telecom-Kimi": "training_share_telecom_kimi.pdf",
}
DISPLAY_MODELS = {"GLM-4-7-Flash": "GLM-4.7-Flash"}


def load_median_p_values(source_path: Path) -> dict[str, dict[str, dict[int, float]]]:
    """Extract the median-p column from the Markdown long table."""
    rows: dict[str, dict[str, dict[int, float]]] = defaultdict(
        lambda: defaultdict(dict)
    )
    in_table = False
    for raw_line in source_path.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith("| Cohort | 学生模型 | 训练 trace"):
            in_table = True
            continue
        if in_table and not raw_line.startswith("|"):
            break
        if not in_table or raw_line.startswith("|---"):
            continue

        cells = [cell.strip() for cell in raw_line.strip().strip("|").split("|")]
        # The compact table has nine columns; older snapshots also included
        # two interval columns. The fields used here have stable positions.
        if len(cells) not in {9, 11}:
            continue
        cohort, model = cells[0], DISPLAY_MODELS.get(cells[1], cells[1])
        share_match = re.fullmatch(r"(\d+)%", cells[3])
        p_value = cells[6]
        if share_match is None or not re.fullmatch(r"[0-9.]+e-[0-9]+", p_value):
            continue
        rows[cohort][model][int(share_match.group(1))] = float(p_value)

    expected = {
        (cohort, model)
        for cohort in COHORT_ORDER
        for model in MODEL_ORDER
    }
    found = {(cohort, model) for cohort, values in rows.items() for model in values}
    if expected != found:
        missing = sorted(expected - found)
        extra = sorted(found - expected)
        raise ValueError(f"Unexpected training-share table entries; missing={missing}, extra={extra}")
    for cohort, model in expected:
        if set(rows[cohort][model]) != AVAILABLE_SHARES:
            raise ValueError(f"Missing training shares for {cohort}/{model}")
    return rows


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.linewidth": 0.7,
        }
    )
    root = Path(__file__).resolve().parents[1]
    data = load_median_p_values(root / "抗蒸馏水印.md")

    for cohort in COHORT_ORDER:
        fig, axis = plt.subplots(figsize=FIGURE_SIZE)
        plotted_evidence: list[float] = []
        for model in MODEL_ORDER:
            p_values = [data[cohort][model][share] for share in SHARES]
            log_evidence = [-math.log10(value) for value in p_values]
            plotted_evidence.extend(log_evidence)
            axis.plot(
                SHARES,
                log_evidence,
                color=COLORS[model],
                marker=MARKERS[model],
                linewidth=LINE_WIDTH,
                markersize=MARKER_SIZE,
                markerfacecolor="white",
                markeredgewidth=0.9,
            )

        axis.axhline(
            -math.log10(0.05),
            color=THRESHOLD_COLOR,
            linestyle=":",
            linewidth=1.1,
            zorder=0,
        )
        axis.text(
            50.2,
            -math.log10(0.05) + 0.12,
            "$p=0.05$",
            color=THRESHOLD_COLOR,
            fontsize=FONT_SIZES["tick"],
            ha="left",
            va="bottom",
        )
        maximum = max(plotted_evidence)
        tick_step = 1 if maximum < 10 else 2
        upper_limit = tick_step * math.ceil((maximum + 0.35) / tick_step)
        axis.set_xlim(51, 9)
        axis.set_xticks(SHARES)
        axis.set_ylim(0, upper_limit)
        axis.yaxis.set_major_locator(MultipleLocator(tick_step))
        axis.tick_params(axis="both", labelsize=FONT_SIZES["tick"], length=3, pad=1)
        axis.grid(axis="y", linestyle="--", linewidth=0.55, alpha=GRID_ALPHA)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.set_xlabel("Training share (\\%)", fontsize=FONT_SIZES["axis_label"], labelpad=2)
        axis.set_ylabel("$-\\log_{10} p$", fontsize=FONT_SIZES["axis_label"], labelpad=2)
        fig.subplots_adjust(left=0.26, right=0.985, bottom=0.26, top=0.975)

        output_path = Path(__file__).resolve().parent / OUTPUT_NAMES[cohort]
        fig.savefig(output_path, bbox_inches="tight", pad_inches=0.02)
        plt.close(fig)
        print(output_path)


if __name__ == "__main__":
    main()
