---
tag: 3Z4XTB
kind: concept
slug: exposure-bias
name: Exposure bias
aliases:
- train-test discrepancy in sequence generation
area: natural-language-and-speech/text-generation-and-decoding
level: advanced
summary: "A model trained with teacher forcing sees only gold prefixes, but at test time conditions on its own outputs, so errors can compound."
prereqs: [teacher-forcing, autoregressive-decoding, language-model]
see_also: [scheduled-sampling, imitation-learning, dagger, dynamic-oracle, minimum-risk-training, reinforce, inadequacy-of-the-mode, repetition-penalty]
sources:
  - url: https://arxiv.org/abs/1511.06732
    title: "Marc'Aurelio Ranzato, Sumit Chopra, Michael Auli and Wojciech Zaremba, Sequence level training with recurrent neural networks, ICLR 2016"
    locator: "Section 1, which names the problem exposure bias, and Section 3, the MIXER algorithm, which trains on the model's own outputs with a sequence-level reward"
  - url: https://proceedings.mlr.press/v15/ross11a.html
    title: "Stéphane Ross, Geoffrey J. Gordon and J. Andrew Bagnell, A reduction of imitation learning and structured prediction to no-regret online learning, AISTATS 2011, PMLR 15, pages 627 to 635"
    locator: "Section 2, the bound of order T squared times epsilon for a policy trained only on the states of the expert, and the DAgger algorithm with a bound linear in T"
  - paper: doi:10.18653/v1/2021.emnlp-main.415
    title: "Tianxing He, Jingzhao Zhang, Zhiming Zhou and James Glass, Exposure bias versus self-recovery, are distortions really incremental for autoregressive text generation?, EMNLP 2021, pages 5087 to 5102"
    locator: "the measurements of the distortion caused by exposure bias in language models, and the finding that models can recover from errors in the prefix so that the distortion is limited and does not grow step by step"
---

Exposure bias is the mismatch between how an [autoregressive](/autoregressive-decoding/) sequence model is trained and how it is used. With [teacher forcing](/teacher-forcing/), the model learns $p_\theta(y_t \mid y^*_{<t})$, the next token given a correct prefix from the data. At test time it generates, so it conditions on its own earlier outputs $\hat y_{<t}$, and these prefixes can contain mistakes it never saw in training. The model has never been trained to continue such prefixes, so one mistake can lead to more, and the errors can compound over a long output. Ranzato et al. 2016 gave the problem its name. The same effect was known in imitation learning, where Ross, Gordon and Bagnell 2011 proved that a policy trained only on the states of an expert can have a cost that grows with the square of the length of the task. How much exposure bias hurts real text generation is an open question: He et al. 2021 measured it in language models and found that models often recover from bad prefixes, so the distortion stays limited.

## In plain words

A student who only ever practices by continuing perfect examples has never had to recover from their own slips. When they then work alone and make a small mistake, they are in a situation they never practiced, which can lead to a bigger mistake, and so on. A text model trained in the usual way is like that student: in training it always continues correct text, but when it writes, it continues its own text, mistakes included. This mismatch is called exposure bias. It is one possible reason why generated text sometimes drifts off topic or gets stuck in loops. How much harm it does in practice is still argued.

## The idea

**Two distributions of prefixes.** The training loss of teacher forcing is the [cross-entropy](/cross-entropy-loss/) $-\sum_t \log p_\theta(y^*_t \mid y^*_{<t})$, averaged over data sequences $y^*$. It measures the model only on prefixes drawn from the data. At test time the prefixes are drawn from the model itself. If the model were exact, $p_\theta = p_{\text{data}}$, the two distributions would be equal, and [ancestral sampling](/ancestral-sampling/) would produce exactly the data distribution: exposure bias is not a flaw of the factorization or of the loss on its own. It matters because the model is not exact, and its errors on prefixes that the data rarely contains are never trained down.

**Compounding.** Ross, Gordon and Bagnell 2011 made this precise for imitation learning. Let a policy act for $T$ steps and make a mistake with probability at most $\varepsilon$ per step on the states that the expert visits. If each mistake can lead to states where the policy fails from then on, the expected number of mistakes can be of order $T^2 \varepsilon$, not $T \varepsilon$. Their algorithm [DAgger](/dagger/) collects training data on the states that the learned policy itself visits and has a bound linear in $T$. A text decoder is such a policy, with prefixes as states and tokens as actions.

**Self-recovery.** The bound of order $T^2 \varepsilon$ is a worst case. It needs a model that, once it makes an error, keeps failing. A language model that has seen a lot of text may instead treat a bad prefix as a slightly unusual one and continue well. He et al. 2021 measured the distortion caused by feeding a model its own prefixes in place of data prefixes and found that it was limited and did not grow step by step, which suggests that the harm done by exposure bias is smaller than often assumed.

## Examples

**A model that cannot recover.** Let every data sequence be a a a ... a of length $T$, and let the model give the correct token a with probability $1 - \varepsilon$ after any correct prefix, but give only wrong tokens after any prefix with an error, since it never saw one. With teacher forcing every prefix is correct, so the expected number of wrong tokens is $T \varepsilon$. When the model generates, token $t$ is wrong if any of the first $t$ tokens is wrong, which has probability $1 - (1 - \varepsilon)^t$. For $T = 100$ and $\varepsilon = 0.01$, the expected number of wrong tokens is 1 under teacher forcing but $\sum_{t=1}^{100} (1 - 0.99^t) = 37.2$ when the model generates, and only 36.6% of the outputs are fully correct. For $T = 20$ the free-running count is 1.97 against 0.2, so the gap grows with the length.

**A model that recovers.** If the same model instead gives a with probability $1 - \varepsilon$ after any prefix, errors and all, the expected number of wrong tokens is $T \varepsilon = 1$ in both settings. The mismatch of the prefixes is the same, but it does no harm.

**Training only on its own outputs.** Bengio et al. 2015 trained an image captioning model with its own sampled tokens in place of the gold ones from the start of training. It scored 11.2 BLEU-4 on MSCOCO against 28.8 for teacher forcing. A model fed its own early, poor outputs gets little useful signal, which is why [scheduled sampling](/scheduled-sampling/) moves from gold tokens to model tokens slowly.

## Where it is used

- **Scheduled sampling** replaces some gold tokens with the model's own tokens during training, more often as training goes on.
- **Sequence-level training** trains on the model's own outputs with a reward for the whole sequence: MIXER of Ranzato et al. 2016 and other uses of [REINFORCE](/reinforce/), and [minimum risk training](/minimum-risk-training/).
- **Imitation learning** for structured prediction: [DAgger](/dagger/), SEARN and the [dynamic oracles](/dynamic-oracle/) of transition-based parsers, which train the parser on the states that its own errors lead to.
- **Explanations of degeneration.** Exposure bias is often given as one cause of repetition and drift in generated text, together with the [inadequacy of the mode](/inadequacy-of-the-mode/). Decoding fixes such as the [repetition penalty](/repetition-penalty/) treat the symptoms without retraining.

## References
