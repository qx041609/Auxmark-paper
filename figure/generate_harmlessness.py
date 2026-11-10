"""Generate two accuracy and two interaction-length harmlessness bar charts."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


# ---------------------------------------------------------------------------
# 可调节的绘图参数：通常只需要修改本区域
# ---------------------------------------------------------------------------
COLORS = {
    "Control": "#86BAD4",  # 对照组柱子的填充颜色
    "Watermarked": "#CBE6EF",  # 水印组柱子的填充颜色
}
FONT_SIZES = {
    "axis_label": 13.0,  # 横纵坐标轴标题字号
    "tick": 11.5,  # 坐标轴刻度文字字号
    "value": 10.5,  # 柱顶数值标签字号
}
FIGURE_SIZE = (2, 2.05)  # 每张独立 PDF 的宽和高，单位为英寸
BAR_WIDTH = 0.50  # 单根柱子的宽度；数值越大，柱子越粗
WITHIN_GROUP_GAP = 0.08  # 同组两根柱子之间的净空；须大于或等于 0
GROUP_SPACING = 1.30  # GPT 与 Kimi 两组中心之间的距离
X_EDGE_PADDING = 0.08  # 最左、最右柱子与坐标轴边界之间的额外留白
BAR_EDGE_COLOR = "#333333"  # 柱子边框颜色
BAR_EDGE_WIDTH = 0.75  # 柱子边框线宽
AXIS_LINE_WIDTH = 0.75  # 坐标轴线宽
GRID_LINE_WIDTH = 0.60  # 水平辅助网格线宽
GRID_ALPHA = 0.25  # 水平辅助网格透明度；越小，网格越淡
TICK_LENGTH = 3.0  # 坐标轴刻度线长度

# 四张图各自的纵轴上限和主刻度间隔。
Y_AXIS = {
    "accuracy": {
        "BFCL": {"upper": 80, "tick": 20},  # BFCL 准确率图
        "Telecom": {"upper": 25, "tick": 5},  # Telecom 准确率图
    },
    "steps": {
        "BFCL": {"upper": 12, "tick": 3},  # BFCL 平均步数图
        "Telecom": {"upper": 42, "tick": 10},  # Telecom 平均步数图
    },
}

# 柱顶标签位置，均按当前图纵轴上限的比例计算。
LABEL_NORMAL_OFFSET = 0.025  # 普通标签高出柱顶的距离比例
LABEL_CLOSE_THRESHOLD = 0.1  # 两柱差值低于该比例时启用上下错位
LABEL_CLOSE_LOW_OFFSET = 0.01  # 相近数值中较低标签的柱顶偏移比例
LABEL_CLOSE_HIGH_OFFSET = 0.07  # 相近数值中较高标签的柱顶偏移比例

# 图内边距和导出留白。
SUBPLOT_MARGINS = {
    "left": 0.30,  # 左边距；增大可给纵轴标题留更多空间
    "right": 0.98,  # 右边距
    "bottom": 0.16,  # 下边距；增大可给横轴文字留更多空间
    "top": 0.98,  # 上边距；减小可给柱顶标签留更多空间
}
SAVE_PADDING_INCHES = 0.005  # 导出 PDF 时四周额外留白，单位为英寸

TEACHERS = ["GPT", "Kimi"]  # 横轴教师顺序；交换元素即可交换左右位置

# 本脚本不写标题或子标题；(a)--(d) 的子标题统一由 04_experiment.tex 设置。


RESULTS = {
    # 每个数组顺序固定为 [对照组, 水印组]；accuracy 为百分比，steps 为平均步数。
    "BFCL": {
        "GPT": {"accuracy": [45.5, 48.5], "steps": [8.03, 9.79]},
        "Kimi": {"accuracy": [64.5, 65.5], "steps": [6.93, 8.97]},
    },
    "Telecom": {
        "GPT": {"accuracy": [18.0, 17.0], "steps": [31.60, 30.22]},
        "Kimi": {"accuracy": [15.0, 12.0], "steps": [35.40, 35.38]},
    },
}


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.linewidth": AXIS_LINE_WIDTH,
        }
    )


def grouped_label_offsets(
    control: list[float], watermarked: list[float], upper_limit: float
) -> tuple[list[float], list[float]]:
    """Vertically separate labels when paired values are too close."""
    control_offsets = [upper_limit * LABEL_NORMAL_OFFSET] * len(control)
    watermarked_offsets = [upper_limit * LABEL_NORMAL_OFFSET] * len(watermarked)
    for index, (control_value, watermarked_value) in enumerate(
        zip(control, watermarked)
    ):
        if abs(control_value - watermarked_value) < upper_limit * LABEL_CLOSE_THRESHOLD:
            if control_value >= watermarked_value:
                control_offsets[index] = upper_limit * LABEL_CLOSE_HIGH_OFFSET
                watermarked_offsets[index] = upper_limit * LABEL_CLOSE_LOW_OFFSET
            else:
                control_offsets[index] = upper_limit * LABEL_CLOSE_LOW_OFFSET
                watermarked_offsets[index] = upper_limit * LABEL_CLOSE_HIGH_OFFSET
    return control_offsets, watermarked_offsets


def grouped_bar_positions() -> tuple[list[float], list[float], list[float], tuple[float, float]]:
    """根据组间距、组内间距和柱宽计算坐标，并阻止柱子重叠。"""
    if BAR_WIDTH <= 0:
        raise ValueError("BAR_WIDTH 必须大于 0。")
    if WITHIN_GROUP_GAP < 0:
        raise ValueError("WITHIN_GROUP_GAP 不能小于 0，否则同组柱子会重叠。")
    minimum_group_spacing = 2 * BAR_WIDTH + WITHIN_GROUP_GAP
    if GROUP_SPACING <= minimum_group_spacing:
        raise ValueError(
            "GROUP_SPACING 必须大于 2 * BAR_WIDTH + WITHIN_GROUP_GAP，"
            "否则相邻组的柱子会重叠。"
        )

    group_centers = [index * GROUP_SPACING for index in range(len(TEACHERS))]
    half_pair_spacing = (BAR_WIDTH + WITHIN_GROUP_GAP) / 2
    control_positions = [center - half_pair_spacing for center in group_centers]
    watermarked_positions = [center + half_pair_spacing for center in group_centers]
    x_limits = (
        control_positions[0] - BAR_WIDTH / 2 - X_EDGE_PADDING,
        watermarked_positions[-1] + BAR_WIDTH / 2 + X_EDGE_PADDING,
    )
    return group_centers, control_positions, watermarked_positions, x_limits


def save_accuracy_chart(dataset: str, output_dir: Path) -> None:
    teachers = TEACHERS
    group_centers, control_positions, watermarked_positions, x_limits = (
        grouped_bar_positions()
    )
    control = [RESULTS[dataset][teacher]["accuracy"][0] for teacher in teachers]
    watermarked = [RESULTS[dataset][teacher]["accuracy"][1] for teacher in teachers]
    upper_limit = Y_AXIS["accuracy"][dataset]["upper"]
    tick_interval = Y_AXIS["accuracy"][dataset]["tick"]

    figure, axis = plt.subplots(figsize=FIGURE_SIZE)
    left = axis.bar(
        control_positions,
        control,
        width=BAR_WIDTH,
        color=COLORS["Control"],
        edgecolor=BAR_EDGE_COLOR,
        linewidth=BAR_EDGE_WIDTH,
        zorder=3,
    )
    right = axis.bar(
        watermarked_positions,
        watermarked,
        width=BAR_WIDTH,
        color=COLORS["Watermarked"],
        edgecolor=BAR_EDGE_COLOR,
        linewidth=BAR_EDGE_WIDTH,
        zorder=3,
    )

    control_offsets, watermarked_offsets = grouped_label_offsets(
        control, watermarked, upper_limit
    )
    for bar, value, offset in zip(left, control, control_offsets):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            value + offset,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=FONT_SIZES["value"],
            fontweight="bold",
        )
    for bar, value, offset in zip(right, watermarked, watermarked_offsets):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            value + offset,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=FONT_SIZES["value"],
            fontweight="bold",
        )

    axis.set_ylabel("Task accuracy (\%)", fontsize=FONT_SIZES["axis_label"], labelpad=3)
    axis.set_xticks(group_centers, teachers)
    axis.set_xlim(*x_limits)
    axis.set_ylim(0, upper_limit)
    axis.yaxis.set_major_locator(MultipleLocator(tick_interval))
    finish_axis(axis)
    save_figure(figure, output_dir / f"harmlessness_accuracy_{dataset.lower()}.pdf")


def save_step_chart(dataset: str, output_dir: Path) -> None:
    teachers = TEACHERS
    group_centers, control_positions, watermarked_positions, x_limits = (
        grouped_bar_positions()
    )
    control = [RESULTS[dataset][teacher]["steps"][0] for teacher in teachers]
    watermarked = [RESULTS[dataset][teacher]["steps"][1] for teacher in teachers]
    upper_limit = Y_AXIS["steps"][dataset]["upper"]
    tick_interval = Y_AXIS["steps"][dataset]["tick"]

    figure, axis = plt.subplots(figsize=FIGURE_SIZE)
    left = axis.bar(
        control_positions,
        control,
        width=BAR_WIDTH,
        color=COLORS["Control"],
        edgecolor=BAR_EDGE_COLOR,
        linewidth=BAR_EDGE_WIDTH,
        zorder=3,
    )
    right = axis.bar(
        watermarked_positions,
        watermarked,
        width=BAR_WIDTH,
        color=COLORS["Watermarked"],
        edgecolor=BAR_EDGE_COLOR,
        linewidth=BAR_EDGE_WIDTH,
        zorder=3,
    )

    control_offsets, watermarked_offsets = grouped_label_offsets(
        control, watermarked, upper_limit
    )
    for bar, value, offset in zip(left, control, control_offsets):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            value + offset,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=FONT_SIZES["value"],
            fontweight="bold",
        )
    for bar, value, offset in zip(right, watermarked, watermarked_offsets):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            value + offset,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=FONT_SIZES["value"],
            fontweight="bold",
        )

    axis.set_ylabel("Mean steps", fontsize=FONT_SIZES["axis_label"], labelpad=3)
    axis.set_xticks(group_centers, teachers)
    axis.set_xlim(*x_limits)
    axis.set_ylim(0, upper_limit)
    axis.yaxis.set_major_locator(MultipleLocator(tick_interval))
    finish_axis(axis)
    save_figure(figure, output_dir / f"harmlessness_steps_{dataset.lower()}.pdf")


def finish_axis(axis: plt.Axes) -> None:
    axis.tick_params(
        axis="both", labelsize=FONT_SIZES["tick"], length=TICK_LENGTH
    )
    axis.grid(
        axis="y",
        linestyle="--",
        linewidth=GRID_LINE_WIDTH,
        alpha=GRID_ALPHA,
        zorder=0,
    )
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def save_figure(figure: plt.Figure, output_path: Path) -> None:
    figure.subplots_adjust(**SUBPLOT_MARGINS)
    figure.savefig(
        output_path,
        bbox_inches="tight",
        pad_inches=SAVE_PADDING_INCHES,
    )
    plt.close(figure)
    print(output_path)


def main() -> None:
    configure_style()
    output_dir = Path(__file__).resolve().parent
    for dataset in RESULTS:
        save_accuracy_chart(dataset, output_dir)
    for dataset in RESULTS:
        save_step_chart(dataset, output_dir)


if __name__ == "__main__":
    main()
