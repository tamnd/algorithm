---
tag: JQ9G2T
kind: technique
slug: training-data-extraction
name: Training data extraction from language models
aliases:
- memorized text extraction
area: security-and-privacy/adversarial-machine-learning
level: research
summary: "Samples many outputs from a language model and ranks them by perplexity relative to a reference, to find verbatim training text."
prereqs: [language-model, perplexity, membership-inference-attack]
see_also: [membership-inference-attack, likelihood-ratio-membership-attack, dp-sgd, approximate-differential-privacy, model-inversion-attack, machine-unlearning, minhash, perplexity]
sources:
  - url: https://arxiv.org/abs/2012.07805
    title: Nicholas Carlini, Florian Tramer, Eric Wallace, Matthew Jagielski, Ariel Herbert-Voss, Katherine Lee, Adam Roberts, Tom Brown, Dawn Song, Ulfar Erlingsson, Alina Oprea and Colin Raffel, Extracting training data from large language models, USENIX Security 2021, pages 2633 to 2650
    locator: the abstract, the threat model, the result that hundreds of verbatim sequences were recovered from GPT-2 by queries alone, that larger models were more vulnerable, and the discussion of safeguards
  - url: https://arxiv.org/abs/1802.08232
    title: Nicholas Carlini, Chang Liu, Ulfar Erlingsson, Jernej Kos and Dawn Song, The secret sharer, evaluating and testing unintended memorization in neural networks, USENIX Security 2019, pages 267 to 284
    locator: canaries, the exposure metric, and the effect of differentially private training on exposure
  - url: https://arxiv.org/abs/2202.06539
    title: Nikhil Kandpal, Eric Wallace and Colin Raffel, Deduplicating training data mitigates privacy risks in language models, ICML 2022
    locator: the link between the number of copies of a sequence in the training data and how often the model generates it, and deduplication as a defense
---

Training data extraction is the attack in which an adversary who can only query a language model recovers text that the model saw in training, word for word. Carlini et al. (2021) showed it on GPT-2: by querying the model, they recovered hundreds of verbatim sequences of its training data, among them personal contact details that were public on the web, code and unique identifiers, some of which appeared in only one document of the training set. Larger models were more vulnerable than smaller ones. The attack works because a model that fits its training data assigns an unusually high likelihood to some training sequences, so a sequence that the model finds much more likely than a reference model does is probably memorized. This page describes the attack only at the level of the paper's abstract. It gives no prompts, no ranking rules and no extracted data, and it spends most of its length on the threat model, the conditions the attack needs, the measurement of memorization and the defenses.

**Threat model.** The goal is to learn training data, especially rare sequences that identify a person or hold a secret. The knowledge is black box: the adversary can sample text from the model and, in the paper, read the probabilities it assigns to tokens; it does not see the weights or the training set. The capability is a large number of queries. The defender controls the training data, the training procedure and the interface.

## In plain words

A language model learns by reading a huge amount of text. Most of what it learns is general, but some rare pieces of text, such as an address or a key, can be stored almost exactly.

An attacker cannot look inside the model, but can ask it to write a lot of text. Most of that text is new. A small part of it is copied from the training text, and the model is unusually confident about exactly those parts, more than a model that never saw them. That difference points to the copies.

The defenses remove the cause: train on fewer copies of each text, keep secrets out of the training data, or train with differential privacy, which limits how much any one document can change the model.

## When it applies

- **Memorization.** The model must assign a much higher likelihood to some training sequences than to similar sequences it did not see. This happens more for sequences repeated many times in the training data, for larger models, and for longer training.
- **Sampling access.** The adversary must be able to draw many outputs. Access to the token probabilities helps the ranking stage; with text only, the attack is weaker.
- **A reference.** The ranking compares the model with something that did not memorize the same text, such as a smaller model or a general measure of how compressible the text is. This is the same signal as in [membership inference](/membership-inference-attack/).
- **No confirmation for an outsider.** Only someone with the training set can confirm that an output is verbatim training text. In the paper the authors confirmed candidates with the help of the data owner; an outside attacker has candidates, not proofs.

## The template

The stages of the published method at the level of its abstract, with the point where each defense acts. None of the holes is a prompt, a parameter or a threshold.

```pseudo id=main
EXTRACTION-THREAT-MODEL(model M, reference R)
L1  draw ⟨many samples⟩ from M                          ▷ defense: rate limits, query monitoring
L2  score each sample by ⟨how much more likely it is under M than under R⟩
                                                         ▷ the membership signal; defense: DP training bounds it
L3  keep ⟨the samples with the highest scores⟩
L4  check them against ⟨the training data⟩               ▷ only the data owner can confirm
L5  the cause in the data: ⟨repeated or secret text⟩      ▷ defense: deduplication, removing secrets before training
```

Line L5 is not a step of the attack; it names the condition in the training data that the attack exploits, and the defenses that act on it before any query. Line L2 is the only stage that uses knowledge of the model, and it is the stage that [differential privacy](/differential-privacy-definition/) controls.

**The defense points.**
- **Deduplication (line L5).** Kandpal, Wallace and Raffel (2022) measured that the rate at which a model generates a training sequence grows quickly with the number of copies of that sequence in the training data, and that removing duplicates greatly reduced the regeneration of training text (a measurement). Near-duplicate detection, for example with [MinHash](/minhash/), makes this practical at scale.
- **Removing secrets (line L5).** Filter keys, identifiers and personal data from the corpus before training. This is a heuristic with no guarantee, since a filter misses what it does not recognize.
- **Differentially private training (line L2).** Train with [DP-SGD](/dp-sgd/). If training is $(\epsilon, \delta)$-differentially private with respect to one document, then any test of whether a given document was in the training set has a true positive rate at most $e^\epsilon$ times its false positive rate plus $\delta$, a theorem from the definition of [approximate differential privacy](/approximate-differential-privacy/). This bounds the signal of line L2 for every document, at a cost in accuracy.
- **Interface limits (line L1).** Rate limits, hiding token probabilities and filters that block long verbatim matches with known training text raise the cost. They are heuristics: the model still holds the text.
- **Unlearning.** If a sequence must be removed after training, [machine unlearning](/machine-unlearning/) addresses it; exact unlearning by retraining is the only method with a full guarantee.

## Classic examples

- **Canaries and exposure.** Carlini et al. (2019) measured memorization by inserting a random secret of a known format, a canary, into the training data and computing its exposure: $\log_2 |\mathcal R| - \log_2 \mathrm{rank}$, where $\mathcal R$ is the set of possible secrets and the rank is the position of the true canary when all candidates are sorted by the model's likelihood. A model that did not memorize gives the canary a random rank. In an abstract model with a made-up alphabet of 10 symbols and secrets of 4 symbols, $|\mathcal R| = 10^4$; if the canary ranks third, the exposure is $\log_2 10^4 - \log_2 3 = 13.29 - 1.58 = 11.70$ bits, close to the maximum $13.29$, so the model has memorized it. This is an audit that the data owner runs, not an attack.
- **Membership inference.** The ranking stage is a [membership inference attack](/membership-inference-attack/) applied to text that the model wrote. The calibrated tests of the [likelihood ratio attack](/likelihood-ratio-membership-attack/) are the stronger form of the same signal.
- **Model inversion.** [Model inversion](/model-inversion-attack/) recovers typical features of a class from a classifier; extraction recovers exact training records, which is a stronger privacy failure.
- **The GPT-2 study.** Carlini et al. (2021) used a model trained on public web text, so the recovered text was public, and they worked with the model's developers to confirm candidates. The study was a measurement of the risk, not a release of data.

## Variations

- **Targeted extraction.** Ask whether a specific known prefix leads the model to complete a specific secret; this is closer to the canary audit and needs a guess of the prefix.
- **Measuring memorization at scale.** Later work prompts models with prefixes from the known training set and counts exact continuations. Done by the data owner, this measures memorization without an adversary.
- **Fine-tuned models.** Models fine-tuned on small private datasets can memorize those datasets faster than large pretrained models memorize the web; the same defenses apply.
- **Other modalities.** The same risk exists for image generation models that reproduce training images.

## Pitfalls

These are pitfalls for defenders and auditors.
- **Equating "public" with "harmless".** The recovered text in the GPT-2 study was public on the web, but a model can spread it in new contexts and long after its source is removed. The condition at line L5 applies to public text too.
- **Relying on interface filters alone.** Filters at line L1 make queries costlier but do not remove the text from the model; an attacker with the weights skips them.
- **Reporting DP without the parameters.** A guarantee at line L2 means little without $\epsilon$, $\delta$ and the unit of privacy (a token, a document or a user). A sequence that appears in many documents is not protected by a bound per document.
- **Deduplicating only exact copies.** Near duplicates with small changes still count as repetition for the model; use near-duplicate detection at line L5.
- **Auditing with too few canaries.** Exposure from one canary has high variance; insert several and report the distribution.

## Exercises

1. In the canary audit, suppose the model's likelihood is independent of which candidate was inserted. Show that the rank of the canary is uniform on $\{1, \dots, |\mathcal R|\}$ and that the expected exposure is at most about $1/\ln 2$ bits.
2. A training procedure is $(\epsilon, 0)$-differentially private with respect to one document. A test decides whether a document $D$ was in the training set and has false positive rate $0.01$. Show that its true positive rate is at most $0.01 e^\epsilon$, and compute the bound for $\epsilon = 1$ and $\epsilon = 8$.
3. Explain why a sequence that appears in $k$ different documents can be memorized even when training is differentially private with respect to one document, and what unit of privacy would protect it.

## References
