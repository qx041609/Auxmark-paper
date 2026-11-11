# Industry Distillation Reports and Their Implications for AuxMark

These notes examine three provider reports relevant to AuxMark's motivation and access assumptions. The reports describe provider observations and assessments; they are not independently reproduced experiments. The central implication for our paper is that service-side investigation is operationally plausible, while verification of training use remains a separate research objective. Layered defenses are already deployed, so coordination across stages alone should not be our novelty claim.

## OpenAI campaign report

**Source:** [Disrupting a coordinated model-distillation campaign](https://openai.com/index/disrupting-a-coordinated-model-distillation-campaign/), September 30, 2026.

**Problem and mechanism.** OpenAI reports coordinated attempts to expose protected reasoning through model interactions. One technique moved encrypted reasoning between conversations and requested its transcription. The report distinguishes this from breaking encryption or accessing stored user conversations.

**Timeline and scale.** Activity began July 1. July 24–25 spikes involved 16,000 requests from over 4,000 users. Investigation connected related patterns across more than 15,000 users; OpenAI reports disruption by July 28. These counts concern attempted extraction, not necessarily successful extraction.

**Attribution.** OpenAI associates a core cluster with individuals linked to Moonshot AI but does not attribute every observed operator to one actor.

**Response.** Measures combined account restrictions, stronger signup controls, network monitoring, reasoning-isolation protections, streamed-output checks, and coordination with third-party providers.

**Evidential boundary.** The report establishes a provider's account of extraction and disruption. It does not present a calibrated black-box test demonstrating that a particular released student learned from the collected traces. Use it to motivate service-side visibility and intervention; avoid treating campaign attribution as a model-level detection result.

## Anthropic defense deployment report

**Source:** [Strengthening our defenses against distillation attacks](https://www.anthropic.com/news/distillation-defenses), October 12, 2026.

**Objective.** The defenses primarily restrict access to unsummarized reasoning. In Anthropic's training experiment, a student scored 80.4% on SWE-bench Verified using full transcripts and 71.8% using summaries. These are student task scores, not detection rates.

**Mechanisms.** Anthropic combines restrictions on reasoning reuse across contexts, models, and organizations with a two-stage classifier. Repeated extraction attempts trigger stricter limits or bans; selected blocked requests incur charges. Red-teaming and monitoring drive updates.

**Results.** Anthropic reports classifier false positives below 0.1%, 10–100-fold lower estimated reasoning-token extraction on its own platform, and account bans often within two hours of campaign onset. The extraction reduction is not a student-detection true-positive rate.

**Trade-offs.** Some integrations required changes. Benign requests can be blocked and charged. Anthropic says durability remains uncertain and that highly sophisticated, persistent evasion had not yet tested the new defenses.

**Relevance.** This is evidence of deployed layered prevention with measurable trade-offs. It does not evaluate attribution from a suspect student's outputs, and it prevents us from presenting layered defense itself as new.

## Anthropic campaign investigation report

**Source:** [Detecting and preventing distillation attacks](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks), February 23, 2026.

**Scale and scope.** Anthropic attributes campaigns to DeepSeek, Moonshot, and MiniMax, reporting over 16 million exchanges through approximately 24,000 fraudulent accounts. Individual reported volumes exceed 150,000, 3.4 million, and 13 million exchanges, respectively. Distillation itself is distinguished from unauthorized collection and use.

**Evidence.** Investigators used IP correlations, request metadata, infrastructure links, coordinated timing, payment information, and sometimes partner corroboration. Targets included reasoning, tool use, and coding. Anthropic reports observing MiniMax's campaign before model release and a rapid shift toward a newly released teacher.

**Operational difficulty.** Proxy networks replace banned accounts and mix collection with unrelated requests. One network managed over 20,000 accounts. Individual prompts can appear ordinary; repeated, coordinated activity provides the distinguishing pattern.

**Response.** Traffic classifiers and behavioral analysis accompany identity checks, output-side safeguards, and intelligence sharing.

**Evidential boundary.** This supports selecting suspicious accounts or traffic subsets. It supplies no query-level precision/recall estimate or exact mapping from queries to student training records. Its traffic fingerprinting should not be conflated with fingerprinting a released student's behavior.

## What the evidence means for our setting

The following is our research interpretation, rather than a claim that the reports validate AuxMark.

### Separate the questions being answered

| Question | Evidence needed | Role in AuxMark |
| --- | --- | --- |
| Which interactions merit investigation? | Service logs and operational signals | Select a candidate evidence pool |
| Who controlled the querying activity? | Account and infrastructure investigation | Associate collection with an operator where possible |
| Did collection successfully obtain useful outputs? | Returned responses and extraction outcomes | Establish what information was exposed |
| Did a suspect student learn the recorded behavior? | Student probes, controls, and a defined decision rule | AuxMark's principal verification task |
| Which selected traces are likely training examples? | Trace-specific scores and independently evaluated labels | Secondary attribution task |

Success at one stage does not automatically answer the next question. In particular, an account can collect outputs without using them for training, and an unknown student can learn from only part of the collected material. Conversely, failure to detect an extraction attempt does not establish that no exposure occurred.

### State our additional assumptions explicitly

Our construction requires the provider to control the serving process sufficiently to insert auxiliary tool calls and retain private evidence. It also requires access to a candidate student endpoint that accepts the audit contexts. The existence of suspicious traffic does not by itself identify that endpoint.

Let Q be all served trajectories, S the selected suspicious subset, and D the unknown training subset. The provider knows Q and S but not D. Detection depends on usable evidence from the overlap of S and D. It should not assume that S contains every training trajectory or that every selected trajectory was trained on.

Our main evaluation fixes 100 selected trajectories, of which 50 enter training. This is a controlled overlap condition. It is not an empirically measured traffic-detector precision, and it does not measure end-to-end recall from all distillation activity. The lower-overlap resampling experiments should remain labeled as sensitivity analyses.

### Frame the contribution precisely

A suitable question is: **Given an imperfectly selected set of recorded interactions, can a provider obtain reliable black-box evidence that a suspect student learned behavior embedded in those interactions?**

AuxMark creates a provider-controlled association between a preceding action and an auxiliary action. Private records identify that association. Paired probes ask whether the student reproduces it preferentially in the corresponding context. This is the mechanism that should distinguish our contribution from an architecture that merely combines several existing safeguards.

Evidence of watermark inheritance is still conditional on the access and exposure assumptions. It does not alone establish whether the use was contractually authorized, identify the responsible person, or exclude every alternative route by which watermarked material might have reached the student.

### Keep the evaluation claims separate

The relevant AuxMark endpoint is detection under the combined significance and effect-size rule, with false positives measured on controls. Task success measures utility. Interaction steps measure one component of overhead. Neither is a substitute for measuring the candidate-generation, scoring, probe-generation, and storage costs.

A fuller cost evaluation should report additional model calls, tokens, latency, and audit queries. A stronger deployment evaluation would run an actual traffic screener before verification and measure missed collections, evidence overlap, and final detection jointly. These are proposed evaluation extensions, not completed results.

## How to use these reports in the introduction

Use the provider reports to establish the practical setting and motivate access to service-side signals. Describe their results as provider-reported observations. Keep operational investigation distinct from verification of student training use.

The limitation evidence for passive detection should come from our own controlled analyses in the manuscript. The industrial reports do not establish those weaknesses. Likewise, our watermark-transfer and cleaning experiments supply the evidence for AuxMark's effectiveness; the reports do not validate our detector.

Avoid claiming that existing providers use only isolated defenses, that traffic monitoring reveals the exact training set, or that our work introduces layered defense for the first time. Explain the specific additional capability: targeted verification using retained, deliberately embedded behavioral evidence.

## Concrete research questions suggested by this framing

1. How much correctly selected evidence is needed when suspicious-set size, training overlap, and watermark-release frequency vary independently?
2. Can the provider link suspicious traffic to a candidate student endpoint without assuming that association in advance?
3. Does the paired-probe advantage persist under controls trained on related tasks or on independent traces from the same teacher?
4. What is the complete serving and verification cost per detected student, including auxiliary-model calls?
5. How much detection remains after cleaning optimized jointly for watermark removal and retained student capability?

## Additional primary sources for the broader and narrower background

### A concrete authorized distillation example

[DeepSeek-R1 official repository](https://github.com/deepseek-ai/DeepSeek-R1) documents six released models distilled from R1 onto Qwen and Llama bases. This gives the opening paragraph a concrete example of teacher-to-student capability transfer. It is evidence about the developers' disclosed distillation of their own R1 model; it is not evidence for allegations about the provenance of R1 itself.

**Introduction role:** establish distillation as a useful development method before discussing unauthorized use.

### Google campaign report

[GTIG AI Threat Tracker](https://cloud.google.com/blog/topics/threat-intelligence/distillation-experimentation-integration-ai-adversarial-use), February 12, 2026, describes a Gemini reasoning-extraction campaign involving more than 100,000 prompts. Google interprets the breadth of tasks as an attempt to replicate reasoning in non-English languages and reports recognizing and mitigating the activity in real time. The report distinguishes legitimate distillation from unauthorized use of Gemini outputs.

**Introduction role:** add a third provider's observations and show that capability extraction can use normal API access. The prompt count describes the observed campaign; it does not count successful extractions or verified distilled students.

### OpenAI account of the collection and training pipeline

[Updated Stakes for American-Led, Democratic AI](https://cdn.openai.com/pdf/045aa967-ee96-4a09-94ee-3098ddf6db2c/OpenAI-US-House-Select-Cmte-Update-%5B021226%5D.pdf), February 12, 2026, describes activity OpenAI considers consistent with unauthorized distillation. Page 3 discusses obfuscated routers and pipelines combining synthetic-data generation, large-scale cleaning, and reinforcement-style preference optimization. Page 6 describes heuristics, machine learning, manual review, ranking/scoring classifiers, and analysis of scale and prompt diversity across accounts.

**Introduction role:** motivate cleaning robustness and service-side evidence selection. The memo's account associations and assessments should remain attributed to OpenAI. It does not publish a calibrated student-model verification experiment.

### Anthropic follow-up on relaying and extraction

[Detecting and countering misuse of AI: September 2026](https://www.anthropic.com/threat-intelligence-report-september-2026), section 7, expands the campaign reporting. Anthropic reports more than 151 million exchanges associated with Alibaba between May and July 2026. It also describes a Moonshot operation relaying almost 300,000 customer requests over ten days through 5,380 accounts. Anthropic says some relayed exchanges were saved and processed to extract reasoning through cross-session replay.

**Introduction role:** make the collection pipeline concrete. Our inference is that relayed genuine customer tasks can complicate screening based only on unusual prompt content. Treat the campaign attribution as Anthropic's finding; do not equate observed exchanges with independently confirmed training records.

### Source selection for the opening

Use the R1 release only if a concrete legitimate example helps the first paragraph. For the second paragraph, select Google for an additional provider perspective and OpenAI's February memo for preprocessing and service-side observations. The Anthropic follow-up is useful when explaining relaying, rather than merely adding a larger exchange count. The original three reports remain complementary sources. Two or three citations with distinct evidential roles will make a clearer opening than a long chronology.

Read November 11, 2026. These notes retain the publication dates and metric scopes of the linked reports.
