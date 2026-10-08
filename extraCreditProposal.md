# Project Proposal: Understanding and Reducing Hallucination in Speech Recognition

## 1. Summary

Speech recognition systems such as Whisper sometimes write words or sentences that were never spoken. This is called hallucination. In health care, legal work and driving, an invented sentence can misrepresent what a person said and cause harm. I propose a research project that measures when Whisper hallucinates, finds out why, and tests a model-level fix that reduces invented words without deleting real speech.

## 2. Motivation

- Measured (from prior work): hallucinated text in Whisper output is not rare and can include harmful content (Koenecke et al., FAccT 2024).
- Measured (from prior work): word error rate alone does not describe hallucination well, especially under distribution shift (Atwany et al., ACL Findings 2025).
- Gap: a system that outputs fewer words will hallucinate less but also lose genuine speech. Mitigation therefore has to be judged as a trade-off between removing unsupported content and keeping spoken content.
- Gap: most existing fixes work before or after the model (silence filtering, removing repeated phrases) or only target non-speech audio (Barański et al., ICASSP 2025; Calm-Whisper, Interspeech 2025). Fewer studies address hallucination that happens while real speech is present.

## 3. Goal and research questions

Goal: reduce speech-induced Whisper hallucination through changes inside the model, while keeping genuine speech.

1. How do model size, dataset and acoustic noise change the hallucination rate?
2. What internal behavior of the model produces a hallucination in each setting?
3. Can a learned decoder gate, which balances audio evidence against prior text context, lower hallucination without raising omission of real words?

## 4. Method

Stage 1: Characterize.
- Models: Whisper-small, Whisper-medium, Whisper-large-v3.
- Data: HALAS (3,611 real earnings-call segments with human hallucination labels) and LibriSpeech (read English speech, no hallucination labels).
- Conditions: clean audio and controlled noise levels.
- Metrics: word error rate, character error rate, insertion error rate, perplexity, hallucination rate, and a new hallucination metric designed in this project that also counts omitted speech.

Stage 2: Explain.
- Label hallucinations by type using audio-grounded review.
- Study the model's internal states (for example, linear probes on hidden states) to see whether a hallucination can be detected before it is written.
- Test local interventions on decoder and encoder components to see which ones change the outcome.

Stage 3: Mitigate.
- Add a learnable gate in the decoder that weighs acoustic evidence against prior context at each token.
- Baselines: greedy search, beam search, temperature fallback, and voice-activity-detection filtering.
- Compare every method on both hallucination and omission, not hallucination alone.

## 5. Deliverables

These are proposed deliverables. They are not done work.

- D1. Characterization report: hallucination and omission rates across models, datasets and noise levels.
- D2. The new hallucination metric, with code and a check against human labels.
- D3. Mechanism analysis: which internal signals relate to hallucination, with the evidence.
- D4. The gated decoder and its comparison against the baselines.
- D5. Final written report and code repository.

## 6. Scope boundaries

In scope:
- Whisper-small, Whisper-medium and Whisper-large-v3.
- English speech from HALAS and LibriSpeech, clean and with controlled noise.
- Hallucination that happens while real speech is present.
- A new hallucination metric, a mechanism analysis, and a learnable decoder gate.

Out of scope:
- Training a new speech recognition model from scratch.
- Other languages and other model families.
- Hallucination on non-speech audio as the main target (prior work covers it).
- Fixes that only filter input or clean up output. These are used as baselines, not as the contribution.
- Building a product or a deployed system.

## 7. Constraints and assumptions

- Time: all work finishes by early December.
- People: one researcher, so the three stages run in sequence.
- Data: HALAS has 2,866 training and 745 test segments with human hallucination labels. LibriSpeech has no hallucination labels, so labels there come from a hand-audited sample.
- Compute: assumed sufficient to run all three Whisper sizes end to end.
- Assumption: the Whisper weights and both datasets are available for research use. I have not checked the licenses.

## 8. Success criteria

- Each comparative number is the mean and spread over repeated runs, or is labeled "single run".
- The new metric is checked against the human labels in HALAS, and its failure cases are shown, not only its agreement.
- The gate is judged successful only if hallucination falls without a matching rise in omitted speech. A drop in hallucination alone does not count.
- A negative result is reported in full. If the gate does not help, D1 to D3 still stand.
- Every number in the report is produced by a script from saved outputs, not typed by hand.

## 9. Intended outcome by December

- A measured picture of when Whisper hallucinates across model size, dataset and noise (D1).
- A hallucination metric that counts both invented and omitted speech (D2).
- Evidence on which internal signals relate to hallucination (D3).
- A tested decoder gate, compared with the baselines on both hallucination and omission (D4).
- A final report and code repository (D5).

Minimum outcome if the gate does not work: D1, D2, D3 and D5, with the negative result for D4 reported in full.

## 10. Expected results (hypotheses, not findings)

- Plausible: larger Whisper models may hallucinate more on the same data. I have not tested this.
- Plausible: the decoder gate lowers the hallucination rate. I have not tested this.

## 11. Timeline (proposed)

- October: set up models and data, run Stage 1, define the new metric.
- November: Stage 2 analysis, first Stage 3 experiments, mid-point review.
- Early December: finish experiments, write the final report.

## 12. Risks

- Scope: three stages is ambitious. If Stage 1 takes longer than planned, Stage 3 is cut first and the report states that.
- Data: HALAS has 3,611 segments and LibriSpeech has no hallucination labels, so human-labeled test data is limited. Fallback: label a smaller audited sample by hand.

## References

1. A. Koenecke et al., "Careless Whisper: Speech-to-Text Hallucination Harms," FAccT 2024.
2. H. Atwany et al., "Lost in Transcription, Found in Distribution Shift: Demystifying Hallucination in Speech Foundation Models," Findings of ACL 2025.
3. M. Barański et al., "Investigation of Whisper ASR Hallucinations Induced by Non-Speech Audio," ICASSP 2025.
4. Y. Wang et al., "Calm-Whisper: Reduce Whisper Hallucination On Non-Speech By Calming Crazy Heads Down," Interspeech 2025.
5. HALAS dataset, Hugging Face (MatBar99/HALAS).
6. LibriSpeech ASR corpus, OpenSLR (resource 12).
