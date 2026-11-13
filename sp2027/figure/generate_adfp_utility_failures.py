"""Generate a blog-style ADFP utility limitation infographic."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


COLORS = {
    "canvas": "#F3F1E7",
    "card": "#FBFAF6",
    "header": "#F6F4EC",
    "border": "#C9C7BC",
    "ink": "#252525",
    "muted": "#686960",
    "blue": "#4F83C2",
    "blue_fill": "#DCE8F6",
    "blue_bar": "#89B8D1",
    "blue_bar_light": "#C8E1EB",
    "coral": "#D36C4F",
    "coral_light": "#E7B19D",
    "grid": "#D7D5CC",
}


# ======================== 常用版式调节区 ========================
# 所有字号统一在这里修改，数值单位为 pt。
# 如果论文中整张图缩放后仍显得太小，优先整体增大这些数值。
FONT_SIZES = {
    "panel_title": 15,      # 每个面板下方的 (a) Example 1 等标题
    "status": 15,           # Clean - valid / ADFP - invalid
    "tool": 14,             # 工具名
    "arguments": 13.5,        # 工具参数
    "reason": 13.5,            # 红框底部的错误原因
    "bar_value": 14.0,        # 柱状图顶部的百分比
    "bar_label": 11.8,        # 柱状图底部的 Control / ADFP
}

# 四个面板的相对宽度，依次对应：Example 1、Example 2、Example 3、柱状图。
# 增大某个数会让该面板更宽，同时会相对压缩其他面板。
# 例如第三个案例内容最长，所以这里给它更大的 1.42。
PANEL_WIDTH_RATIOS = [0.96, 0.96, 1.06, 0.80]

# 面板之间的水平距离；数值越小，四个面板越靠近。
PANEL_GAP = 0.045

# 整张原始图的宽和高（英寸）。LaTeX 中使用 width=\textwidth 时，
# 调高第二个数会增加图的纵向空间；第一个数通常保持不变。
FIGURE_SIZE = (15.0, 4.0)

# 蓝框和红框在各案例面板内部的左右位置与宽度，均为相对比例。
# BOX_X 越小、BOX_WIDTH 越大，框就越靠近面板左右边缘并且越宽。
CASE_BOX_X = 0.045
CASE_BOX_WIDTH = 0.91

# 蓝框的底部位置和高度。增大 CONTROL_BOX_HEIGHT 会主要向上扩展蓝框，
# 当前设置充分利用了外框顶部空白，同时不改变蓝红框之间的距离。
CONTROL_BOX_Y = 0.60
CONTROL_BOX_HEIGHT = 0.32


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.monospace": ["DejaVu Sans Mono", "Consolas", "Courier New"],
            "mathtext.fontset": "stixsans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def rounded(
    axis: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    face: str,
    edge: str,
    linewidth: float = 1.0,
    radius: float = 0.03,
    linestyle: str = "solid",
) -> FancyBboxPatch:
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        facecolor=face,
        edgecolor=edge,
        linewidth=linewidth,
        linestyle=linestyle,
        transform=axis.transAxes,
        clip_on=False,
    )
    axis.add_patch(patch)
    return patch


def draw_outer_card(axis: plt.Axes, panel: str, label: str) -> None:
    axis.set_axis_off()
    rounded(
        axis,
        (0.015, 0.13),
        0.97,
        0.81,
        face=COLORS["card"],
        edge=COLORS["border"],
        linewidth=1.15,
        radius=0.035,
    )
    axis.text(
        0.5,
        0.06,
        f"({panel}) {label}",
        transform=axis.transAxes,
        fontsize=FONT_SIZES["panel_title"],
        fontweight="bold",
        color=COLORS["ink"],
        ha="center",
        va="center",
    )


def draw_case(
    axis: plt.Axes,
    *,
    panel: str,
    label: str,
    control_tool: str,
    control_args: str,
    adfp_tool: str,
    adfp_args: str,
    reason: str,
) -> None:
    draw_outer_card(axis, panel, label)

    rounded(
        axis,
        (CASE_BOX_X, CONTROL_BOX_Y),
        CASE_BOX_WIDTH,
        CONTROL_BOX_HEIGHT,
        face=COLORS["blue_fill"],
        edge=COLORS["blue"],
        linewidth=1.15,
        radius=0.035,
    )
    axis.text(
        0.080,
        0.880,
        "Clean - valid",
        transform=axis.transAxes,
        fontsize=FONT_SIZES["status"],
        fontweight="bold",
        color=COLORS["blue"],
        va="top",
    )
    axis.text(
        0.080,
        0.785,
        control_tool,
        transform=axis.transAxes,
        fontsize=FONT_SIZES["tool"],
        family="sans-serif",
        fontweight="medium",
        fontstretch="condensed",
        color=COLORS["ink"],
        va="top",
        linespacing=1.05,
    )
    axis.text(
        0.080,
        0.705,
        control_args,
        transform=axis.transAxes,
        fontsize=FONT_SIZES["arguments"],
        family="sans-serif",
        fontstretch="condensed",
        color=COLORS["ink"],
        va="top",
        linespacing=1.05,
    )

    rounded(
        axis,
        (CASE_BOX_X, 0.15),
        CASE_BOX_WIDTH,
        0.40,
        face="#FBE9E2",
        edge=COLORS["coral"],
        linewidth=1.15,
        radius=0.035,
    )
    axis.text(
        0.080,
        0.495,
        "ADFP - invalid",
        transform=axis.transAxes,
        fontsize=FONT_SIZES["status"],
        fontweight="bold",
        color=COLORS["coral"],
        va="top",
    )
    axis.text(
        0.080,
        0.395,
        adfp_tool,
        transform=axis.transAxes,
        fontsize=FONT_SIZES["tool"],
        family="sans-serif",
        fontweight="medium",
        fontstretch="condensed",
        color=COLORS["ink"],
        va="top",
        linespacing=1.05,
    )
    axis.text(
        0.080,
        0.300,
        adfp_args,
        transform=axis.transAxes,
        fontsize=FONT_SIZES["arguments"],
        family="sans-serif",
        fontstretch="condensed",
        color=COLORS["ink"],
        va="top",
        linespacing=1.05,
    )
    axis.text(
        0.080,
        0.175,
        "Reason: " + reason,
        transform=axis.transAxes,
        fontsize=FONT_SIZES["reason"],
        family="sans-serif",
        fontstretch="condensed",
        color=COLORS["coral"],
        fontweight="semibold",
        va="bottom",
    )


def draw_error_card(axis: plt.Axes) -> None:
    draw_outer_card(axis, "d", "Overall error rate")

    base_y = 0.25
    top_y = 0.79
    max_value = 30.0
    values = [16.5, 23.7]
    centers = [0.34, 0.70]
    fills = [COLORS["blue_bar"], COLORS["blue_bar_light"]]
    width = 0.23
    tops: list[float] = []
    axis.plot(
        [0.15, 0.89],
        [base_y, base_y],
        transform=axis.transAxes,
        color=COLORS["border"],
        linewidth=1.0,
        zorder=0,
    )
    for center, value, fill in zip(centers, values, fills):
        height = (top_y - base_y) * value / max_value
        rounded(
            axis,
            (center - width / 2, base_y),
            width,
            height,
            face=fill,
            edge="#FFFFFF",
            linewidth=1.1,
            radius=0.035,
        )
        top = base_y + height
        tops.append(top)
        axis.text(
            center,
            top + 0.035,
            f"{value:.1f}%",
            transform=axis.transAxes,
            fontsize=FONT_SIZES["bar_value"],
            color=COLORS["ink"],
            fontweight="bold",
            ha="center",
            va="bottom",
        )
    axis.text(
        centers[0],
        0.19,
        "Clean",
        transform=axis.transAxes,
        fontsize=FONT_SIZES["bar_label"],
        color=COLORS["ink"],
        ha="center",
    )
    axis.text(
        centers[1],
        0.19,
        "ADFP",
        transform=axis.transAxes,
        fontsize=FONT_SIZES["bar_label"],
        color=COLORS["ink"],
        ha="center",
    )


def build_figure() -> plt.Figure:
    configure_style()
    figure = plt.figure(figsize=FIGURE_SIZE, facecolor=COLORS["canvas"])
    grid = figure.add_gridspec(
        1,
        4,
        width_ratios=PANEL_WIDTH_RATIOS,
        left=0.018,
        right=0.985,
        bottom=0.06,
        top=0.97,
        wspace=PANEL_GAP,
    )
    case_a = figure.add_subplot(grid[0, 0])
    case_b = figure.add_subplot(grid[0, 1])
    case_c = figure.add_subplot(grid[0, 2])
    chart = figure.add_subplot(grid[0, 3])

    draw_case(
        case_a,
        panel="a",
        label="Example 1",
        control_tool="get_details_by_id",
        control_args='id="L1002"',
        adfp_tool="check_apn_settings",
        adfp_args='customer_id="C1001", line_id="L1001"',
        reason="invalid tool name and arguments",
    )
    draw_case(
        case_b,
        panel="b",
        label="Example 2",
        control_tool="get_details_by_id",
        control_args='id="L1002"',
        adfp_tool="run_speed_test",
        adfp_args='phone_number="555-123-2002"',
        reason="invalid tool name",
    )
    draw_case(
        case_c,
        panel="c",
        label="Example 3",
        control_tool="KB_search",
        control_args='query="Silver Rewards Card cash\n back calculation issues"',
        adfp_tool="submit_cash_back_dispute_0589",
        adfp_args='user_id="user123", transaction_id="trans456"',
        reason="invalid tool name and placeholder IDs",
    )
    draw_error_card(chart)
    return figure


def main() -> None:
    parser = argparse.ArgumentParser()
    # 直接运行脚本时，默认把 PDF 输出到当前脚本所在的 figure 文件夹。
    # 如需指定其他位置，仍可使用：--output "你的输出路径.pdf"
    default_output = Path(__file__).resolve().with_name("adfp_agent_utility_failures.pdf")
    parser.add_argument("--output", type=Path, default=default_output)
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure = build_figure()
    figure.savefig(args.output, bbox_inches="tight", pad_inches=0.03)
    if args.preview:
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(args.preview, dpi=180, bbox_inches="tight", pad_inches=0.03)
    plt.close(figure)
    print(f"Saved PDF: {args.output.resolve()}")
    if args.preview:
        print(f"Saved preview: {args.preview.resolve()}")


if __name__ == "__main__":
    main()
