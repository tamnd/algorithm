---
tag: QH9B1T
kind: definition
slug: perplexity
name: Perplexity
aliases:
- language model perplexity
area: natural-language-and-speech/language-modeling
level: intro
summary: The exponential of a model's per-token cross-entropy on held-out text, exp(H) in nats or 2^H in bits, which is the inverse geometric mean of the token probabilities. Lower is better.
prereqs: [language-model, shannon-entropy]
see_also: [cross-entropy-loss, entropy-rate, kullback-leibler-divergence, n-gram-language-model, laplace-smoothing, kneser-ney-smoothing, word-error-rate, subword-tokenization]
sources:
  - paper: doi:10.1121/1.2016299
    title: Frederick Jelinek, Robert L. Mercer, Lalit R. Bahl and James K. Baker, Perplexity, a measure of the difficulty of speech recognition tasks, Journal of the Acoustical Society of America 62(S1), S63, 1977
    locator: the abstract of the talk that introduced perplexity as a measure of the difficulty of a recognition task
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: entropy of a source and the entropy per symbol of a sequence
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft
    locator: chapter N-gram Language Models (draft of January 2026), evaluating language models with perplexity
---

Perplexity is the standard number for how well a [language model](/language-model/) predicts a text that it was not trained on. It is the inverse of the geometric mean of the probabilities that the model gives the tokens of the text, so a perplexity of 100 means that the model was, on average, as uncertain as if it chose each token from 100 equally likely ones. Lower is better. It is the exponential of the per-token cross-entropy: $e^{H}$ when the cross-entropy $H$ is in nats, and $2^{H}$ when it is in bits, and the two give the same number. Jelinek, Mercer, Bahl and Baker introduced it in 1977 as a measure of the difficulty of speech recognition tasks, and it is also used for models of DNA, protein and music sequences.

## Definition

Let $P$ be a language model and let $w_1, \ldots, w_N$ be the predicted tokens of a test text, with the end marker `</s>` of each sentence counted as a token and the start markers `<s>` not counted. The **per-token cross-entropy** of $P$ on the text, in nats, is

$$H = -\frac{1}{N} \sum_{i=1}^{N} \ln P(w_i \mid w_1, \ldots, w_{i-1}),$$

where the history of each token goes back to the start of its sentence, or further if the model uses more context. The **perplexity** is

$$\mathrm{PP} = e^{H} = P(w_1, \ldots, w_N)^{-1/N} = \Big( \prod_{i=1}^{N} \frac{1}{P(w_i \mid w_1, \ldots, w_{i-1})} \Big)^{1/N}.$$

With logarithms to base 2 the cross-entropy is $H_2 = H / \ln 2$ bits per token, and $2^{H_2} = e^{H}$. The value of the perplexity does not depend on the base, but the cross-entropy does, so a report of $H$ must state its unit.

Some properties follow at once.

- $\mathrm{PP} \ge 1$, with equality only when every token gets probability 1.
- If one token gets probability 0, then $H = \infty$ and $\mathrm{PP} = \infty$. This is why language models are smoothed.
- If $P$ is uniform on a vocabulary $V$, then $\mathrm{PP} = |V|$ on every text. Perplexity is often read as an effective number of choices per token.
- Minimizing perplexity is the same as maximizing the likelihood of the test text, and the same as minimizing the mean [cross-entropy loss](/cross-entropy-loss/).

Perplexity is a value per token of a stated kind. Per-word, per-subword and per-character perplexities of the same model on the same text are different numbers. Since all of them come from the same total log probability $\ln P(\text{text})$, a perplexity per $N$ tokens converts to one per $C$ characters by $\mathrm{PP}_C = \mathrm{PP}_N^{N/C}$.

## Examples and non-examples

**Uniform over ten.** A model that gives each of 10 tokens probability $1/10$ has $H = \ln 10 = 2.302585$ nats $= 3.321928$ bits per token on any text, and $\mathrm{PP} = 10$.

**Four tokens.** A model gives the four tokens of a text the probabilities $1/2$, $1/4$, $1/8$ and $1/8$. Then $H = \frac14 (\ln 2 + 2\ln 2 + 3 \ln 2 + 3 \ln 2) = \frac94 \ln 2 = 1.559581$ nats, which is $2.25$ bits, and $\mathrm{PP} = 2^{2.25} = e^{1.559581} = 4.756828$. The arithmetic mean of the four probabilities is $1/4$, but the perplexity is not 4: it is set by the geometric mean, which weights the small probabilities more.

**A DNA model.** A model of DNA that gives each base probability $1/4$ has perplexity 4 per base. A model with perplexity 3.6 per base on held-out sequence uses about $\log_2 3.6 = 1.85$ bits per base, against 2 bits for the uniform model.

**Not: perplexity on the training text.** The value on the text used to estimate the model rewards memorization. An unsmoothed maximum likelihood n-gram model has a low training perplexity and an infinite test perplexity as soon as one test n-gram is new.

**Not: comparing different tokenizations by per-token perplexity.** A model over subwords predicts more tokens per sentence than a model over words, so its per-token perplexity is lower for the same total probability of the text. To compare models with different [tokenizations](/subword-tokenization/), use bits per character or bits per byte, the total $-\log_2 P(\text{text})$ divided by the number of characters or bytes.

**Not: comparing different vocabularies.** A closed-vocabulary model that maps rare words to `<unk>` predicts the easy token `<unk>` in place of each rare word. A smaller vocabulary then gives a lower perplexity without a better model. Compare models only on the same vocabulary and the same test tokens.

**Not: the entropy of the language.** A perplexity is a property of one model on one text. It is an upper estimate of the [entropy rate](/entropy-rate/) of the source, in the sense below, not the entropy rate itself.

## Related definitions

- **Cross-entropy.** For a true distribution $p$ and a model $q$ on the same outcomes, $H(p, q) = -\sum_x p(x) \log q(x)$. The per-token $H$ above is the empirical form of the cross-entropy rate on a sample. The [cross-entropy loss](/cross-entropy-loss/) used to train neural language models is the same mean, in nats, so the perplexity is $e^{\text{loss}}$.
- **Entropy and entropy rate.** The [Shannon entropy](/shannon-entropy/) $H(p) = -\sum_x p(x) \log p(x)$ is the cross-entropy of $p$ with itself. For a stationary ergodic source, the [entropy rate](/entropy-rate/) $\lim_{n \to \infty} \frac1n H(X_1, \ldots, X_n)$ is at most the expected cross-entropy rate of any model, so on average no model reaches a perplexity below $e^{H}$ of the true source, with $H$ the entropy rate in nats.
- **KL divergence.** $H(p, q) = H(p) + D(p \,\|\, q)$, where $D$ is the [Kullback-Leibler divergence](/kullback-leibler-divergence/). A lower perplexity on text from $p$ means a model $q$ closer to $p$ in this divergence.
- **Word error rate.** In speech recognition, a lower perplexity of the language model often goes with a lower [word error rate](/word-error-rate/), but not always, since the error rate also depends on which words the acoustic model confuses.
- **Branching factor.** For a grammar that allows a fixed set of next words at each point, the branching factor is the number of allowed words. Perplexity is the corresponding value for a model that gives the next words different probabilities.

## References
