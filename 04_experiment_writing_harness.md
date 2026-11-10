# Experiment Writing Harness

## Contract

- **Artifact:** Initial draft of the detection-effectiveness subsection in an IEEE Symposium on Security and Privacy paper.
- **Audience:** ML and security reviewers familiar with agent trajectories, but not necessarily with the three watermark detectors.
- **Scope:** Add the detection-effectiveness overview, true-positive, false-positive, C0-only baseline, trace-level attribution, training-share sensitivity, harmlessness, and four-part robustness results to `04_experiment.tex`. Preserve the existing setup and all bibliography files.
- **Success condition:** State the tested population, decision rule, denominator, and baseline metric for every empirical claim. Do not turn heterogeneous baseline outputs into a numerical ranking.

## Evidence and claim ledger

| Claim | Evidence | Metric / denominator | Status |
|---|---|---|---|
| Tracewm detects all controlled distilled students. | `抗蒸馏水印.md`, C0 table (lines 517--526). | Dual decision rule in Section 3; 24/24 student-model/cohort settings. | Verified. |
| Tracewm has no observed false positives on clean base models. | `抗蒸馏水印.md`, updated Base false-positive table (lines 529--540). | Same dual rule; 0/48 base-model/cohort tests. All p-values are at least 0.062. | Verified. |
| AgentWM results decline as clean traces are mixed in. | `抗蒸馏水印.md`, lines 752--795. | Native metric: detected tool passes / 5 fixed passes; results are not Tracewm TPR. | Verified, not directly comparable. |
| SeqWM has few significant trace-level true-key scores in the available C0 runs. | `抗蒸馏水印.md`, lines 797--810. | Native metric: traces with p<0.05 under the wrong-key calibration; 17/400 BFCL, 35/400 SWE. | Verified, not directly comparable. |

| Tracewm's sign-test evidence persists as the fraction of truly trained traces is reduced in a fixed 100-trace suspicious set. | `抗蒸馏水印.md`, training-share simulation table. | Observed 50% C0/W50 anchor; 2,000 empirical-replay draws per non-anchor setting; fraction with one-sided exact-test p<0.05. Overall frequencies: 97.1% at 30%, 92.8% at 20%, and 82.4% at 10%. | Verified as a sensitivity analysis, not a full detection-rate estimate. |

| Watermarking has limited observed effect on task accuracy and interaction length. | `抗蒸馏水印.md`, harmlessness table, complete 200-task rows. | Four BFCL/Telecom teacher--dataset cohorts; $\Delta Acc$ ranges from -3.0 to +3.0 pp (macro average 0.0 pp). Mean steps average 20.49 for control and 21.09 for watermarked agents; $\Delta L$ ranges from -1.38 to +2.04 steps (macro average +0.60). | Verified as observed differences; SWE-bench is excluded and no equivalence test is available. |
| Tracewm remains detectable after dilution with standard clean answers in every GPT-teacher run. | `抗蒸馏水印.md`, Data flooding D1/D5/D10 tables. | 24/24 BFCL-GPT and SWE-GPT settings satisfy both the 5-pp gap and $p<0.05$ criteria. | Verified. |
| Tracewm remains detectable after dilution with clean traces from up to three alternative teachers. | `抗蒸馏水印.md`, multi-teacher R1/R2/R3 tables. | 24/24 BFCL-GPT and SWE-GPT settings are complete and detected; at R3 the minimum real--fake gap is 9.8 pp and the maximum $p$ is 0.011. | Verified. |
| Tracewm remains detectable after semantic-preserving rewriting in the tested cohorts. | `抗蒸馏水印.md`, semantic rewriting table. | 8/8 BFCL-GPT and Telecom-GPT settings are detected; the weakest setting has a 6.9-pp gap and $p=0.032$. | Verified; evidence covers one rewriting model and two cohorts. |
| Tracewm remains detectable after right truncation in every GPT-teacher run. | `抗蒸馏水印.md`, BFCL-GPT and SWE-GPT 20K T10/T15/T20 tables. | All 24 planned settings are complete and detected. All eight T20 settings are detected. | Verified for the complete GPT-teacher grid. |
| Tracewm remains detectable after a watermark-aware, utility-preserving cleaning attack. | `抗蒸馏水印.md`, 2026-09-16 trajectory-utility-prioritized cleaning experiment. | DeepSeek-V4-Flash cleans 50 GPT-OSS-120B trajectories per cohort; all 8 BFCL/Telecom student settings satisfy the dual criterion. The smallest gap is 7.5 pp and the largest one-sided sign-test p-value is $9.6\times10^{-3}$. | Verified for this sanitizer and the two tested cohorts. |

## Story and paragraph map

1. **Detection success.** Question: Does the decision rule identify distilled students? Answer: all 24 controlled students are detected; table gives cohort-level p-value ranges.
2. **False positives.** Question: Does the detector falsely accuse models without watermarked training data? Answer: none of 48 tests meets the dual decision rule; state this as an observed rate rather than a population guarantee.
3. **Baselines.** Question: What do the available agent-watermark baselines achieve? Answer: report AgentWM and SeqWM in their native units and explain why they cannot support a raw ranking.
4. **Trace attribution.** Question: Can a model-level detection be localized to likely training traces? Answer: report cohort-averaged Precision@K.
5. **Training-share sensitivity.** Question: Does the sign-test signal survive when fewer suspicious traces were truly used for training? Answer: replay the frozen trained/untrained empirical distributions at lower training shares and report significance frequency, with an explicit non-incidence and non-full-detection caveat.

6. **Harmlessness.** Question: Does watermark embedding reduce teacher-agent utility or lengthen interactions? Answer: compare 200-task control and watermarked runs for the four BFCL/Telecom cohorts using two task-accuracy panels and two absolute mean-step panels.
7. **Robustness overview.** Question: Which adversarial preprocessing operations are tested, and how complete is the evidence? Answer: summarize the four attacks using completed/planned coverage, detected/completed outcomes, minimum real--fake gap, and maximum p-value.
8. **Data flooding.** Question: Does adding standard clean answers dilute the learned signal? Answer: all 24 GPT-teacher D1/D5/D10 settings are detected, including all eight 1:10 settings.
9. **Data flooding+.** Question: Does clean data from several independent teachers erase the signal? Answer: all 24 R1/R2/R3 settings are detected, including all eight 1:3 settings.
10. **Semantic rewriting.** Question: Can a semantic-preserving rewrite remove the signal? Answer: all eight tested settings are detected, but the weakest setting is close to both decision thresholds and only one rewrite model is tested.
11. **Truncation.** Question: Does deleting the training suffix remove the signal? Answer: all 24 GPT-teacher T10/T15/T20 settings are detected, including all eight T20 settings.

## Terminology ledger

- **True positive / false positive:** model-level outcome of Tracewm's dual decision rule.
- **Full-hit gap:** macro-averaged real-side strict Full-hit rate minus fake-side rate; retain the 5-percentage-point threshold defined in the construction section.
- **Detected pass:** AgentWM's native JSD-thresholded tool-pass outcome; do not call it a true positive.
- **Significant trace:** SeqWM's native per-trace true-key result with p<0.05; do not call it a model-level detection.
- **Significance frequency:** Fraction of 2,000 simulated empirical-replay draws with one-sided exact-test p<0.05. Do not call it the full dual-criterion detection rate.

- **Harmlessness differences:** $\Delta Acc=Acc_{\mathrm{wm}}-Acc_{\mathrm{ctrl}}$ in percentage points and $\Delta L=L_{\mathrm{wm}}-L_{\mathrm{ctrl}}$ in interaction steps.
- **Data flooding:** Dilution with official or gold clean answers; conditions D1, D5, and D10 denote watermarked:clean trace ratios of 1:1, 1:5, and 1:10.
- **Data flooding+:** Dilution with clean traces generated by one, two, or three alternative teachers; conditions R1, R2, and R3 denote ratios of 1:1, 1:2, and 1:3.
- **Completed setting:** One available cohort--condition--student result. Missing runs are excluded from detection counts and shown in coverage denominators.

## Open issue

AgentWM and SeqWM use different trajectories, sample units, and decision statistics from Tracewm. A strict comparative ranking requires rerunning all methods on the same frozen tasks, student models, training mixtures, and false-positive constraint.

The harmlessness calculation excludes SWE-bench. It also has no uncertainty intervals or prespecified equivalence margins, so the subsection reports observed utility and step differences rather than statistical equivalence.

The robustness subsection reports only GPT-OSS-120B watermark-teacher results. The SWE-bench truncation grid is now complete. Semantic rewriting uses only DeepSeek-V4-Flash and covers BFCL-GPT and Telecom-GPT. The draft must not generalize these results to Kimi-K2.5 as watermark teacher or to untested rewriting models.

## Revision log

- 2026-09-12: Drafted the three requested result paragraphs and one compact model-level outcome table in `04_experiment.tex`.
- 2026-09-12: Replaced the prior Base snapshot after the user updated the data. The draft now reports 0/48 observed false positives and the minimum Base p-value of 0.062.
- 2026-09-12: Compiled `00_main.tex` successfully. Academic lint reports zero strong warnings and two review-level sentence-length warnings in the broader experiment file.
- 2026-09-12: Reorganized the results at the author's request: the true-positive and Base false-positive results are now separate full-width tables with one model evaluation per row; the columns are teacher, benchmark, model, decisive-card count, real-side fullhit, fake-side fullhit, p-value, and significance. The baseline table remains compact.
- 2026-09-12: Set the baseline table in a left-aligned `0.48\textwidth` minipage and stretched its columns to use that half-page width.
- 2026-09-13: Replaced the mixed-condition baseline summary with C0-only native statistics: AgentWM reports visible calls and detected passes, while SeqWM reports median z and median p. Added the Detection Effectiveness overview and a trace-level Precision@K table from the six frozen C0 cohorts.
- 2026-09-13: Recast the consolidated C0 baseline table as a left-side wrapping table, with the baseline discussion flowing first beside and then below it. It retains both methods' significance indicators and their decision statistics (AgentWM passes; SeqWM median p), restores Dataset as a table column, and omits non-decisive workload and z-score columns.
- 2026-09-13: Added the fixed-100-trace training-share sensitivity analysis to Effectiveness. The new model-level table retains the observed 50% C0/W50 anchor and reports per-student sign-test significance frequencies from 2,000 simulated draws at 30%, 20%, and 10%, while explicitly distinguishing this statistic from the complete dual-criterion detection rate.
- 2026-09-13: Replaced the trace-level attribution table with three separately generated PDF line figures (BFCL, SWE-bench, and Telecom), imported side by side as one manuscript figure. Each plot preserves the two teacher-cohort Precision@K series, and the source script exposes colors, fonts, line widths, markers, dimensions, and axis bounds.
- 2026-09-13: Added a fourth, separately generated Overall PDF that macro-averages the three benchmark curves separately for GPT-OSS-120B and Kimi-K2.5. Removed repeated in-panel legends, documented the blue/red encodings in the shared caption, and enlarged plot text, lines, and markers for four-across rendering.
- 2026-09-13: Returned the attribution visualization to three panels. Added (a)--(c) labels and moved the teacher-model legend into the caption using colored line samples, matching the requested caption convention.
- 2026-09-13: Converted the three imported PDFs into true LaTeX subfigures with subcaptions `(a) BFCL`, `(b) SWE-bench`, and `(c) Telecom`; removed benchmark titles from the PDF assets. The shared caption now depicts both line color and the hollow circle/square marker for each teacher.
- 2026-09-13: Replaced the training-share table with six separately generated PDF line plots arranged in two rows of three. The visualizer reads the frozen Markdown long table, shows the median sign-test evidence as $-\log_{10}p$ at 50/40/30/20/10% training shares, uses one colored and hollow-marked curve per student model, and retains a dotted $p=0.05$ reference line with panel-specific vertical ranges.
- 2026-09-13: Retitled this result as ``Impact on identification accuracy.'' Moved all simulation details to the body text; the figure caption now only describes its axes, model legend, and significance threshold.
- 2026-09-13: Recast the large false-positive table as a non-floating minipage table. This prevents LaTeX from assigning it to a float-only page and allows the baseline text to continue directly below Table 2.
- 2026-09-13: Added a left-side $p=0.05$ annotation to each training-share panel and the same grey threshold cue to its caption. Kept the trace-attribution plot's existing blue/red teacher colors while adapting each benchmark panel's vertical range to its observed precision values.
- 2026-09-13: Replaced the trace-attribution figure with the compact full-width Precision@K table at the author's request. The trace-level discussion now references this table directly; the training-share visualization remains the only figure in this result sequence.
- 2026-09-13: Recast the trace-level table using the same `table*`--`caption`--`scriptsize`--`tabular` construction as the earlier main tables, including teacher/dataset grouping, a two-level results header, and matching heavy outer rules.
- 2026-09-13: Kept the grouped main-table styling for trace-level attribution but changed its body to `tabular*{\textwidth}` with elastic intercolumn spacing, so the table spans the full text width instead of shrinking to its natural content width.
- 2026-09-13: Restored the original flat trace-attribution table: one Cohort column followed by P@10--P@30, rendered as a full-width non-floating `tabular*` block.
- 2026-09-13: Split the trace-attribution Cohort field into separate Dataset and Teacher Model columns. Dataset names span the two teacher rows, while the five P@K columns and full-width non-floating layout remain unchanged.
- 2026-09-13: Reordered the trace-attribution identifiers to Teacher Model followed by Dataset, and regrouped the six rows into three-dataset blocks under each teacher.
- 2026-09-14: Replaced the four-cohort harmlessness table with four separately generated PDF bar charts in one row. Each panel compares 200-task control and watermarked accuracy and annotates the corresponding change in mean interaction steps; SWE-bench remains excluded.
- 2026-09-14: Reorganized the harmlessness figure into two task-accuracy panels (BFCL and Telecom) followed by two interaction-length panels. The accuracy panels compare control and watermarked runs for both teachers; the step panels directly plot $\Delta L$ for both teachers.
- 2026-09-14: Updated the SWE-bench/Telecom Mistral C0 results and all dependent attribution and 100-trace dilution summaries. Replaced harmlessness $\Delta L$ bars with control-versus-watermarked absolute mean-step bars from the updated 200-task statistics.
- 2026-09-14: Widened the harmlessness bars and subfigures, reduced unused horizontal axis padding, and added collision-aware vertical offsets for labels on nearly equal paired values.
- 2026-09-14: Separated harmlessness layout controls into explicit within-group gap and between-group spacing parameters, added overlap validation, and kept all panel subtitles in the LaTeX subfigure captions rather than the source PDFs.
- 2026-09-14: Added a robustness subsection organized into the requested four parts: standard-data flooding, multi-teacher data flooding+, semantic rewriting, and right truncation. At the author's request, the subsection reports only GPT-OSS-120B watermark-teacher results; the compact summary table exposes incomplete SWE-bench truncation coverage.
- 2026-09-14: Split the combined robustness summary into four independent, non-floating full-width tables. Each table now stays with its corresponding experiment and retains the same coverage-aware worst-case statistics.
- 2026-09-14: Replaced the four robustness tables with four independent PDF bar charts. The data-flooding, multi-teacher flooding, and truncation figures each contain six condition--benchmark groups with four model-colored bars; semantic rewriting uses two benchmark groups. Bar height is $-\log_{10}p$, the dotted line marks $p=0.05$, and unavailable SWE truncation runs are marked N/A rather than zero.
- 2026-09-14: Reworked the robustness visuals to match the harmlessness small-multiple format. Data flooding, data flooding+, and truncation now each use six independently generated PDFs arranged as two rows of three LaTeX subfigures, with one benchmark--condition setting and four student-model bars per panel. Semantic rewriting is again reported as a detailed result table rather than a plot.
- 2026-09-14: Regenerated all 18 robustness panel PDFs, compiled the 18-page manuscript without LaTeX errors or undefined references, and visually verified Figures 3--5 and the semantic-rewriting table. Fixed figure placement so each result follows its experiment text and later subsections do not overtake pending figures.
- 2026-09-14: Synchronized the completed SWE-bench T10/T15/T20 truncation grid from the updated Markdown, raising truncation coverage to 24/24 and total robustness coverage to 80/80. Compressed the robustness small multiples by reducing each source PDF's height and using an adjustable 0.30-text-width LaTeX panel width.
- 2026-09-14: Recompiled the compact layout to 17 pages and visually verified the robustness pages: both flooding figures now fit consecutively on one page, the truncation figure occupies roughly half a page, and all labels and values remain legible without clipping.
- 2026-09-14: Rebalanced the robustness small multiples after the compact version appeared too squat: increased each source panel's height to a moderate 2.35-by-1.85-inch aspect ratio, widened the LaTeX panels to 0.31 text width to reduce column gaps, and tightened the gap between the two panel rows.
- 2026-09-14: Reorganized each robustness figure into four model-specific panels on one row. Every panel now contains six bars: paired BFCL and SWE-bench results at the experiment's three attack levels. Dataset identity is encoded by a consistent blue/orange color pair, with hatching on SWE-bench bars for grayscale distinction.
- 2026-09-14: Reverted the robustness figures to six benchmark--condition panels in two rows of three. The generated PDFs contain no panel titles; all BFCL/SWE-bench and D/R/T condition titles are supplied by LaTeX subfigure captions, while bar colors again identify the four student models.
- 2026-09-14: Raised the robustness $p=0.05$ dotted reference line above the bars, with its annotation on the topmost drawing layer, so the statistical threshold remains continuously visible across every bar.
- 2026-09-14: Added card-level W/L columns to the true-positive and false-positive Effectiveness tables using the current Markdown results. Updated only the two captions to define W/L as real wins / fake wins; the surrounding body text is unchanged.
- 2026-09-14: Standardized the table notation from W/L to $w/\ell$ to match the sign-test definition, and rebuilt the paraphrasing table header with fixed column spacing so its grouped horizontal rule meets the vertical boundary without extending that boundary through the group title.
- 2026-09-14: Added a half-width wrapped AgentWM data-flooding robustness table and a short Baseline robustness paragraph. The comparison omits SeqWM because it detects no C0 student, reports all BFCL/SWE-bench D1/D5 pass counts, and explains how clean-data mixing dilutes AgentWM's synonymous-tool distribution signal.
- 2026-09-14: Synchronized two updated BFCL truncation results from the Markdown source: T15/GLM-4.7-Flash now uses $p=1.7\times10^{-3}$ and T20/Mistral-24B uses $p=2.1\times10^{-3}$. Regenerated the robustness PDFs; the 24/24 detection conclusion remains unchanged.
- 2026-09-15: Standardized multi-letter mathematical identifiers across the manuscript with `\mathtt{...}`, including named quantities such as `Pr`, `KD`, and `Acc` and semantic subscripts such as `safe`, `core`, `aux`, `real`, and `fake`; standard LaTeX operators remain unchanged.
- 2026-09-15: Centralized the method name as `\newcommand{\name}{Tracewm}` in `00_main.tex` and replaced every literal manuscript occurrence with `\name{}` so future renaming requires one edit.
- 2026-09-16: Added an ``Adaptive Watermark-Removal Attack'' subsection. It defines the black-box, watermark-aware LLM-sanitization protocol and the unchanged verification rule. The source record contains no finalized detection outputs for this setting, so the subsection explicitly makes no empirical robustness claim.
- 2026-09-16: Replaced the pending-result caveat with the completed trajectory-utility-prioritized cleaning experiment. Added an eight-row BFCL/Telecom result table and qualified the conclusion to DeepSeek-V4-Flash, GPT-OSS-120B, and the tested student models.
- 2026-09-17: Restyled the adaptive watermark-removal table to match the paraphrasing-robustness table: grouped Detection Results header, $R^{\mathtt{real}}$/$R^{\mathtt{fake}}$/$w/\ell$/$p$ columns, and a significance indicator. Reduced only this table's intercolumn spacing from 10.8pt to 10.5pt to avoid horizontal overflow; visual PDF inspection passed.
- 2026-09-17: Compressed the paraphrasing and adaptive-attack tables into left-aligned half-width wrapping tables. Removed the real-side rate, fake-side rate, and $w/\ell$ columns at the author's request; each table now reports the student model, one-sided sign-test $p$-value, and significance indicator.
- 2026-09-15: Standardized multi-letter mathematical identifiers across the manuscript with `\mathtt{...}`, including named quantities such as `Pr`, `KD`, and `Acc` and semantic subscripts such as `safe`, `core`, `aux`, `real`, and `fake`; standard LaTeX operators remain unchanged.
- 2026-09-15: Centralized the method name as `\newcommand{\name}{Tracewm}` in `00_main.tex` and replaced every literal manuscript occurrence with `\name{}` so future renaming requires one edit.
- 2026-09-20: Moved datasets, model choices, hyperparameter selection, evaluation metrics, and baselines to Appendix A, `Supplement of Experiments` / `Experimental Details`. Kept the main experimental-setup paragraph and its training and traffic-analysis configuration in the main paper; redirected construction-level hyperparameter references to the appendix.
