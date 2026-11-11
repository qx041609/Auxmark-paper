"""为 robustness 小节生成六个独立子图 PDF。"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


# ---------------------------------------------------------------------------
# 可调节的绘图参数：通常只需要修改本区域
# ---------------------------------------------------------------------------
MODEL_COLORS = {
    "Mistral-24B": "#EAF3E2",  # Mistral 柱子颜色
    "GLM-4.7-Flash": "#B4DEB6",  # GLM 柱子颜色
    "Qwen3-14B": "#7BC6BE",  # Qwen3-14B 柱子颜色
    "Qwen3-32B": "#439CC4",  # Qwen3-32B 柱子颜色
}
MODEL_ORDER = ["Mistral-24B", "GLM-4.7-Flash", "Qwen3-14B", "Qwen3-32B"]
MODEL_TICK_LABELS = ["Mistral", "GLM", "Q14", "Q32"]  # 横轴模型简称

FONT_SIZES = {
    "axis_label": 11.5,  # 纵轴标题字号
    "tick": 9.5,  # 坐标轴刻度字号
    "value": 9.5,  # 柱顶数值字号
    "threshold": 9.0,  # p=0.05 阈值文字字号
}

FIGURE_SIZE = (2.10, 1.85)  # 每张独立 PDF 的宽和高，单位为英寸
BAR_WIDTH = 0.55  # 单根柱子的宽度
BAR_SPACING = 0.70  # 相邻柱子中心之间的距离；必须大于 BAR_WIDTH
X_EDGE_PADDING = 0.1  # 最左和最右柱与横轴边界之间的额外留白

BAR_EDGE_COLOR = "#3F3F3F"  # 柱子边框颜色
BAR_EDGE_WIDTH = 0.75  # 柱子边框线宽
AXIS_LINE_WIDTH = 0.75  # 坐标轴线宽
GRID_LINE_WIDTH = 0.60  # 水平网格线宽
GRID_ALPHA = 0.25  # 水平网格透明度
THRESHOLD_COLOR = "#0F0F0F"  # p=0.05 阈值线颜色
THRESHOLD_LINE_WIDTH = 1.30  # p=0.05 阈值线宽
THRESHOLD_LINE_STYLE = ":"  # p=0.05 阈值线样式
LABEL_OFFSET_RATIO = 0.025  # 柱顶数值与柱顶的距离，占纵轴上限的比例
THRESHOLD_LABEL_X_RATIO = 0.02  # 阈值标签距离绘图区左侧的比例
THRESHOLD_LABEL_Y_RATIO = 0.02  # 阈值标签高出阈值线的比例
SUBPLOT_MARGINS = {
    "left": 0.23,  # 左边距；给纵轴标题留空间
    "right": 0.99,  # 右边距
    "bottom": 0.20,  # 下边距；给横轴标签留空间
    "top": 0.9,  # 上边距；给柱顶数值留空间
}
SAVE_PADDING_INCHES = 0.005  # 导出 PDF 时四周额外留白


# 每个列表元素为：(数据集, 攻击等级, 四个模型的 p 值)。
# 模型顺序固定为 MODEL_ORDER。PDF 内不写标题，标题由 LaTeX 子图 caption 提供。
DATA_FLOODING = [
    ("BFCL", "D1", [5.7e-5, 5.2e-6, 3.3e-5, 5.5e-6]),
    ("BFCL", "D5", [8.5e-3, 1.2e-3, 2.1e-5, 2.5e-5]),
    ("BFCL", "D10", [6.1e-5, 1.1e-3, 2.82377e-06, 5.2e-5]),
    ("SWE-bench", "D1", [4.1e-4, 8.5e-10, 7.5e-13, 1.9e-10]),
    ("SWE-bench", "D5", [5.3e-11, 2.3e-16, 2.5e-17, 1.2e-11]),
    ("SWE-bench", "D10", [4.8e-19, 3.7e-14, 7.1e-14, 5.1e-12]),
]

DATA_FLOODING_PLUS = [
    ("BFCL", "R1", [1.0e-9, 4.2e-6, 5.8e-5, 1.6e-4]),
    ("BFCL", "R2", [1.4e-5, 1.5e-6, 4.7e-3, 3.8e-7]),
    ("BFCL", "R3", [1.4e-4, 0.0113279, 9.6e-5, 9.7e-6]),
    ("SWE-bench", "R1", [1.1e-14, 7.06421e-20, 3.2e-14, 9.1e-10]),
    ("SWE-bench", "R2", [4.8e-19, 2.2e-21, 1.2e-13, 8.8e-11]),
    ("SWE-bench", "R3", [1.3e-20, 6.7e-14, 1.2e-15, 7.5e-13]),
]

TRUNCATION = [
    ("BFCL", "T10", [3.6e-3, 2.3e-7, 5.9e-3, 2.7e-4]),
    ("BFCL", "T15", [1.2e-3, 1.7e-3, 5.9e-3, 0.0113279]),
    ("BFCL", "T20", [2.1e-3, 3.7e-3, 1.4e-4, 2.3e-7]),
    ("SWE-bench", "T10", [4.0e-17, 7.8e-17, 3.6e-7, 4.0e-8]),
    ("SWE-bench", "T15", [1.2e-11, 1.2e-10, 2.2e-14, 2.1e-5]),
    ("SWE-bench", "T20", [8.3e-13, 1.6e-15, 2.2e-12, 5.1e-10]),
]

EXPERIMENTS = {
    "data_flooding": DATA_FLOODING,
    "data_flooding_plus": DATA_FLOODING_PLUS,
    "truncation": TRUNCATION,
}


def configure_style() -> None:
    """设置与论文其他柱状图一致的字体和坐标轴风格。"""
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


def adaptive_y_axis(values: list[float]) -> tuple[float, float]:
    """根据单张子图的 -log10(p) 范围确定纵轴上限和主刻度。"""
    maximum = max(values)
    if maximum <= 3:
        tick_step = 0.5
    elif maximum <= 7:
        tick_step = 1.0
    elif maximum <= 14:
        tick_step = 2.0
    else:
        tick_step = 5.0
    upper = tick_step * math.ceil((maximum + 0.55 * tick_step) / tick_step)
    return upper, tick_step


def draw_panel(p_values: list[float], output_path: Path) -> None:
    """绘制一个数据集和攻击等级下的四模型柱状图。"""
    if BAR_WIDTH <= 0:
        raise ValueError("BAR_WIDTH 必须大于 0。")
    if BAR_SPACING <= BAR_WIDTH:
        raise ValueError("BAR_SPACING 必须大于 BAR_WIDTH，否则柱子会重叠。")

    evidence_values = [-math.log10(p_value) for p_value in p_values]
    upper_limit, tick_step = adaptive_y_axis(evidence_values)
    x_positions = [index * BAR_SPACING for index in range(len(MODEL_ORDER))]

    figure, axis = plt.subplots(figsize=FIGURE_SIZE)
    for x_position, model, evidence in zip(x_positions, MODEL_ORDER, evidence_values):
        axis.bar(
            x_position,
            evidence,
            width=BAR_WIDTH,
            color=MODEL_COLORS[model],
            edgecolor=BAR_EDGE_COLOR,
            linewidth=BAR_EDGE_WIDTH,
            zorder=3,
        )
        axis.text(
            x_position,
            evidence + upper_limit * LABEL_OFFSET_RATIO,
            f"{evidence:.1f}",
            ha="center",
            va="bottom",
            fontsize=FONT_SIZES["value"],
            fontweight="bold",
        )

    threshold = -math.log10(0.05)
    axis.axhline(
        threshold,
        color=THRESHOLD_COLOR,
        linestyle=THRESHOLD_LINE_STYLE,
        linewidth=THRESHOLD_LINE_WIDTH,
        zorder=4,  # 高于柱子的 zorder=3，确保阈值线不会被遮挡
    )

    left_edge = x_positions[0] - BAR_WIDTH / 2 - X_EDGE_PADDING
    right_edge = x_positions[-1] + BAR_WIDTH / 2 + X_EDGE_PADDING
    threshold_label_x = left_edge + (right_edge - left_edge) * THRESHOLD_LABEL_X_RATIO
    axis.text(
        threshold_label_x,
        threshold + upper_limit * THRESHOLD_LABEL_Y_RATIO,
        "$p=0.05$",
        color=THRESHOLD_COLOR,
        fontsize=FONT_SIZES["threshold"],
        ha="left",
        va="bottom",
        zorder=5,
    )

    axis.set_xticks(x_positions, MODEL_TICK_LABELS)
    axis.set_xlim(left_edge, right_edge)
    axis.set_ylim(0, upper_limit)
    axis.yaxis.set_major_locator(MultipleLocator(tick_step))
    axis.set_ylabel("$-\\log_{10} p$", fontsize=FONT_SIZES["axis_label"], labelpad=2)
    axis.tick_params(axis="both", labelsize=FONT_SIZES["tick"], length=3, pad=2)
    axis.grid(
        axis="y",
        linestyle="--",
        linewidth=GRID_LINE_WIDTH,
        alpha=GRID_ALPHA,
        zorder=0,
    )
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)

    figure.subplots_adjust(**SUBPLOT_MARGINS)
    figure.savefig(output_path, bbox_inches="tight", pad_inches=SAVE_PADDING_INCHES)
    plt.close(figure)
    print(output_path)


def main() -> None:
    configure_style()
    output_dir = Path(__file__).resolve().parent
    for experiment_name, settings in EXPERIMENTS.items():
        for benchmark, condition, p_values in settings:
            benchmark_slug = benchmark.lower().replace("-", "_")
            condition_slug = condition.lower()
            output_path = output_dir / (
                f"robustness_{experiment_name}_{benchmark_slug}_{condition_slug}.pdf"
            )
            draw_panel(p_values, output_path)


if __name__ == "__main__":
    main()
