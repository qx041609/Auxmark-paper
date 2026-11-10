# 03_construction Algorithm Rewrite Harness

## Contract
- User request: write the complete method section from `抗蒸馏水印.md`, including watermark embedding, detection, and trace-level attribution.
- Target audience: IEEE Symposium on Security and Privacy reviewers familiar with LLM agents but not this implementation.
- Protected text: preserve the current `Overview` subsection verbatim; replace only the detailed embedding method below it.
- Target section: `03_construction.tex`.
- Main content: watermark embedding, paired-probe detection, card-level statistical testing, and trace-level attribution.
- Style: plain technical English, fewer implementation details, no complex vocabulary, no citation or `.bib` edits.
- Protected file: `09_reference.bib` remains read-only and unchanged.

## Evidence
- Source notes: `抗蒸馏水印.md`.
- Relevant concepts:
  - Core action, Aux action, and release card.
  - Keyed sparse release schedule with probability and budget.
- Candidate Aux action must be natural, argument-bound, and non-disruptive.
- Probe-based detection compares real-Core probes against fake-Core probes.
- Card-level sign test prevents over-counting variants.
- Trace attribution ranks traces using real/counterfactual FullHit and tool-only channels with the fixed $0.26/0.08/0.08$ score.

## Structure
- Watermark Embedding: state, schedule, candidate filtering, scoring, and evidence retention.
- Probe-Based Watermark Detection: paired probes, strict scoring, card aggregation, and an exact sign test.
- Trace-Level Attribution: per-trace quantiles, frozen score, deterministic tie-breaking, and retrospective Precision@K.

## Revision Log
- Replaced the duplicated one-paragraph draft with a complete method section.
- Restored and preserved the user's original overview; the new material begins at `Watermark Embedding Algorithm`.
- Reorganized the method around safe classification, dynamic scheduling and scoring, and private evidence retention; added the source-defined defaults, validation constraints, terminal-command exception, and all state transitions.
- Added paired real/counterfactual probe construction, strict ToolHit/FullHit scoring, card-level aggregation, and the one-sided exact sign test.
- Added the trace-level rank features, frozen score, tie-breaking rule, and the retrospective-validation limitation of its coefficients.
- Kept the keyed schedule and exact candidate score from the source notes.
- Removed low-level API/proxy/header/file/command details while retaining the correctness-critical filtering and state transitions.
- Deferred the detailed statistical detector and trace-attribution score to their dedicated later method/evaluation material; this section exposes only their release-card interface.
