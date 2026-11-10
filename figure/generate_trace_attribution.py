"""Generate the three-panel trace-level attribution figure used by the paper."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator


# ---------------------------------------------------------------------------
# Editable visual parameters
# ---------------------------------------------------------------------------
COLORS = {
    "GPT-OSS-120B": "#3B6FB6",
    "Kimi-K2.5": "#D65F5F",
}
MARKERS = {
    "GPT-OSS-120B": "o",
    "Kimi-K2.5": "s",
}
FONT_SIZES = {
    "title": 13.0,
    "axis_label": 12.0,
    "tick": 11.0,
}
FIGURE_SIZE = (2.2, 1.85)  # width, height of each PDF in inches
LINE_WIDTH = 2.1
MARKER_SIZE = 5.2
GRID_ALPHA = 0.28


K_VALUES = [10, 15, 20, 25, 30]
RESULTS = {
    "BFCL": {
        "GPT-OSS-120B": [72.5, 80.0, 80.0, 79.0, 81.7],
        "Kimi-K2.5": [82.5, 83.3, 82.5, 84.0, 80.8],
    },
    "SWE-bench": {
        "GPT-OSS-120B": [100.0, 98.3, 96.2, 96.0, 94.2],
        "Kimi-K2.5": [82.5, 83.3, 83.8, 79.0, 78.3],
    },
    "Telecom": {
        "GPT-OSS-120B": [75.0, 78.3, 80.0, 82.0, 84.2],
        "Kimi-K2.5": [77.5, 80.0, 78.8, 74.0, 73.3],
    },
}


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

    output_dir = Path(__file__).resolve().parent
    output_names = {
        "BFCL": "trace_attribution_bfcl.pdf",
        "SWE-bench": "trace_attribution_swe_bench.pdf",
        "Telecom": "trace_attribution_telecom.pdf",
    }
    for benchmark, series in RESULTS.items():
        fig, axis = plt.subplots(figsize=FIGURE_SIZE)
        plotted_values = [value for values in series.values() for value in values]
        for teacher, values in series.items():
            axis.plot(
                K_VALUES,
                values,
                color=COLORS[teacher],
                marker=MARKERS[teacher],
                linewidth=LINE_WIDTH,
                markersize=MARKER_SIZE,
                markerfacecolor="white",
                markeredgewidth=1.0,
                label=teacher,
            )

        axis.set_xlabel("$K$", fontsize=FONT_SIZES["axis_label"], labelpad=2)
        axis.set_xticks(K_VALUES)
        value_range = max(plotted_values) - min(plotted_values)
        padding = max(1.5, 0.15 * value_range)
        lower_limit = 5 * int((min(plotted_values) - padding) // 5)
        upper_limit = max(plotted_values) + padding
        axis.set_ylim(lower_limit, upper_limit)
        axis.yaxis.set_major_locator(MultipleLocator(5))
        axis.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}"))
        axis.tick_params(axis="both", labelsize=FONT_SIZES["tick"], length=3)
        axis.grid(axis="y", linestyle="--", linewidth=0.6, alpha=GRID_ALPHA)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)

        axis.set_ylabel(
            "Precision@$K$ (\%)", fontsize=FONT_SIZES["axis_label"], labelpad=3
        )
        fig.subplots_adjust(left=0.24, right=0.98, bottom=0.24, top=0.97)

        output_path = output_dir / output_names[benchmark]
        fig.savefig(output_path, bbox_inches="tight", pad_inches=0.02)
        plt.close(fig)
        print(output_path)


if __name__ == "__main__":
    main()
