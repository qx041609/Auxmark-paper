# AuxMark Introduction Structure

The introduction should connect two contributions: a systematic assessment of existing defenses with new evidence of limitations, and a method for verifying training use through deliberately embedded behavior. The connection is the need for evidence specific to recorded provider interactions. Recommended length: about 850–1,000 words. Use four opening paragraphs for background and the research gap, followed by five paragraphs under `\subsection{Our Contributions}` (Section 1.1). Keep our systematization findings, construction, and experimental results within Section 1.1.

## Technical basis for the narrative

The systematization in `08_appendix.tex` distinguishes traffic screening, prevention, proactive watermarking, and passive fingerprinting. Its useful comparison axes are the evidence each method supplies, the required access, operational cost, and behavior under data processing. A compact taxonomy should explain these differences without treating passive detection and all post-hoc verification as synonymous.

The new evidence has three distinct strengths. First, the answer-overlap experiments show sensitivity to alternative prefixes, conventional solutions, formatting, and sampling in selected examples. Second, the dependency metric has an exact counterexample: an eleven-node graph with one edge and a ten-edge chain have proportional feature vectors and receive identical cosine similarity. Third, the reasoning-distillation experiment finds increased aggregate similarity toward multiple comparison models alongside improved task performance. These findings question the specificity of the measured signals. They do not establish that every similarity detector fails or settle the provenance of any commercial model.

AuxMark's construction addresses the evidence question through a recorded association between core and auxiliary actions. A keyed schedule and release budget control insertion opportunities. Candidates use permitted tools and context-bound arguments; scoring favors plausible and repeatable action pairs. Successful releases create private evidence cards. Screening later selects which cards to audit. Paired probes retain the target auxiliary behavior while changing the preceding execution mechanism. Detection aggregates variants per card and requires both a one-sided sign-test threshold and a minimum mean full-hit gap. Trace ranking is a secondary use of the same evidence.

## Section 1 Introduction — Background and research gap

### Paragraph 1 — Model distillation as the broader background

Open directly with model distillation: teacher-generated outputs provide supervision for transferring capabilities to students. Explain its practical value and acknowledge authorized uses. A concrete example is DeepSeek's release of six models distilled from R1 onto Qwen and Llama bases ([official repository](https://github.com/deepseek-ai/DeepSeek-R1)). Then narrow toward output-based distillation through model services, where the provider may not authorize subsequent training. Introduce reasoning and tool-use trajectories as valuable supervision without beginning with a general history of language model agents.

**Main-message draft:** Model distillation transfers capabilities by training students on teacher-generated outputs. Its practical value also creates an incentive to collect proprietary model outputs for training without the provider's permission.

### Paragraph 2 — Provider observations as the narrower background

Use two or three concrete details from the provider reports to show what the collection process looks like. Prefer details that explain our setting: coordinated requests, third-party routing, retained reasoning traces, and preprocessing before training. Use one scale statistic at most. Google provides an additional provider perspective; OpenAI's February memorandum directly motivates data cleaning as part of the distillation pipeline. Attribute campaign findings to the reporting provider. Avoid a catalogue of company allegations.

End by distinguishing suspicious collection from verification of training use in a student. Introduce the need for reliable evidence under black-box student access. The operational requirements can conclude the subsequent discussion of existing defenses.

**Main-message draft:** Provider investigations reveal organized collection pipelines that target useful model capabilities and adapt to service-side defenses. These observations motivate a verification problem: given suspicious interactions, how can the provider determine whether a student learned from them?

### Paragraph 3 — Existing approaches

Explain how the existing technical routes work and what they are intended to establish. Traffic screening examines collection behavior. Output-side defenses either reduce the usefulness of collected data or embed signals for later verification. Passive fingerprinting compares naturally occurring model behavior. Keep this paragraph about established approaches; reserve our systematic comparison and newly discovered weaknesses for Section 1.1.

**Main-message draft:** Existing defenses address different parts of the distillation process and provide different forms of evidence. Their assumptions determine what a provider can conclude from a traffic alert, a watermark, or a behavioral match.

### Paragraph 4 — The research gap

State the detection problem and its operational requirements. Explain that identifying suspicious collection and verifying training use are separate tasks. Introduce black-box student access and the need to tolerate processing of the collected data. End with the question that our work addresses, without describing our method or reporting our experiments yet.

**Main-message draft:** A practical defense must reliably detect distillation and provide evidence tied to the provider's outputs. It must do so with limited overhead and remain effective after data processing. How can a provider meet these requirements when the student's training data are unknown?

## Section 1.1 Our Contributions

Open with a brief signpost: “Our contributions are twofold.” The following paragraphs develop the two contributions; a second, repetitive contribution list at the end is unnecessary.

### Paragraph 5 — Systematization and new evidence of limitations

Present the systematic comparison as our first contribution. Then explain what the new analytical and empirical evidence adds. Briefly preview the answer-overlap controls and the execution-graph counterexample. The main message is ambiguity in attributing observed behavior to a particular training source. Keep the full taxonomy and experimental details in the main-body systematization section.

**Main-message draft:** We systematize existing anti-distillation techniques and examine the evidence they provide under different access assumptions. We also provide new analytical and empirical evidence of limitations in prominent detection methods, showing how their signals can arise without uniquely identifying the claimed training source.

### Paragraph 6 — The setting and main insight of the new approach

Introduce the second contribution through the provider's capabilities across serving and auditing. The provider inserts and records behavioral evidence, uses service-side signals to select interactions, and later probes a suspect student. State that the selected set need not coincide with the actual training set. Position the contribution as targeted verification from retained behavioral evidence; coordination of defenses itself already exists in deployments.

**Main-message draft:** We study a setting that connects interventions during model serving with later verification of a suspect student. Our main insight is to create and retain behavioral evidence that supports targeted testing even when the provider does not know which interactions entered training.

### Paragraph 7 — AuxMark's embedding insight

Introduce AuxMark and explain why auxiliary behavior is a useful signal. Agent training supervises action sequences, so context-dependent tool calls can become learned behavior. Explain briefly how nonessential, permitted calls and sparse insertion balance learnability with task utility. Keep scheduling equations, candidate weights, and budget values in the construction section.

**Main-message draft:** AuxMark embeds learnable behavior through safe auxiliary tool calls in teacher trajectories. The provider records the associated contexts privately, preserving evidence for later verification while retaining the core task actions.

### Paragraph 8 — Verification and the role of controls

Explain why reproduction of an auxiliary action alone is insufficient: an untrained model may naturally choose it. Describe paired contexts and the preferential-reproduction signal. Mention aggregation of related probes in one sentence if space permits. Trace ranking is an additional capability within this contribution, not a separate main claim. A serving-and-audit diagram can accompany paragraphs 6–8.

**Main-message draft:** The provider selects suspicious interactions and tests whether the student preferentially reproduces the embedded behavior in the corresponding contexts. Paired controls help distinguish this learned association from ordinary tool-use preferences.

### Paragraph 9 — Empirical support for the new approach

Report the 24/24 detections and 0/48 control outcomes, with the three benchmarks and eight teacher–student pairs. State the main experiment's uncertain-membership setting: 100 selected trajectories with 50 used for training. Summarize utility and robustness in separate sentences. Use observed utility effects rather than claiming comprehensive cost savings. Keep lower-overlap resampling labeled as sensitivity analysis.

**Main-message draft:** Our evaluation measures whether AuxMark detects distilled students while avoiding false positives under imperfect knowledge of training membership. The results support its effectiveness across the evaluated model pairs and its resilience to the tested data-processing procedures.

## Claims to keep precise while drafting

The existing notes and manuscript differ on some probe-generation and matching details. The notes retain the recorded observation in the counterfactual probe and permit extra predicted argument keys; the manuscript describes altered observation notation and exact argument equivalence. Resolve these against the implementation before making fine-grained technical claims. The introduction can safely describe paired contexts and matching of the target tool and required arguments.

Card aggregation addresses dependence among variants from one release. It does not by itself prove independence among releases from the same trajectory or perfect real/control symmetry under the null. Avoid the current introduction's unqualified “strong statistical guarantees.”

The reported baseline tests use different native decision statistics. Their failures under the evaluated configurations motivate the design, but do not support an unrestricted ranking at a common false-positive rate. Similarly, selected answer-overlap examples and one graph-score counterexample should retain their actual scope.

For industry context and citation boundaries, see `industry_distillation_reports_reading_notes.md`. No manuscript text has been changed by this outline.
