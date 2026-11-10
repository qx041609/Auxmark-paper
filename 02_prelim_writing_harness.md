# 02_prelim Access and Threat Model Writing Harness

## Contract
- Audience: IEEE Symposium on Security and Privacy reviewers who know LLM agents and model distillation but have not read the Chinese technical notes.
- Artifact: one LaTeX subsection, `Access and Threat Model`, in `02_prelim.tex`.
- Source: `抗蒸馏水印.md`, especially the threat model, trajectory/evidence audit, probe construction, and detection sections.
- Constraint: do not add references or edit `.bib`; only draft the requested subsection.
- Success: define parties, access assumptions, suspicious-set uncertainty, adversary capabilities, and verification access without overclaiming exact knowledge of the adversary's training data.

## Evidence and Claim Ledger
- Claim: the owner operates a teacher-agent API and observes service-side request/metadata/trajectory signals.
  Evidence: `抗蒸馏水印.md` threat model and audit sections.
  Status: supported by source notes.
- Claim: the owner only knows a suspicious set, not the actual distilled subset.
  Evidence: source defines all traces `Q`, suspicious set `S`, and unknown distilled subset `D`.
  Status: supported; mapped to `\mathcal{R}`, `\mathcal{S}`, `\mathcal{D}_{adv}` to avoid notation conflict.
- Claim: the adversary has black-box API access and can clean, rewrite, truncate, and mix data before SFT/KD.
  Evidence: source threat model and robustness experiments.
  Status: supported.
- Claim: verification uses black-box probing of the released student model.
  Evidence: source threat model and detection/probe sections.
  Status: supported.

## Paragraph Map
- P1 answers who the parties are and what the owner can observe.
- P2 formalizes `\mathcal{R}`, `\mathcal{S}`, and `\mathcal{D}_{adv}` and states the partial-set uncertainty.
- P3 states adversary capabilities and transformations.
- P4 states black-box verification access and the statistical attribution goal.

## Release Checks
- No citations added.
- No `.bib` changes.
- No claim that the owner knows exact distilled traces.
- Reuses existing notation for teacher/student models and avoids reusing `\mathcal{D}` for a different object.
