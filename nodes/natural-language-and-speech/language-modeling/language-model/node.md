---
tag: 5C6W3K
kind: definition
slug: language-model
name: Language model
aliases:
- statistical language model
area: natural-language-and-speech/language-modeling
level: intro
summary: A probability distribution over finite sequences of tokens, written by the chain rule as a product of the probabilities of each token given those before it, with an end marker.
prereqs: [text-tokenization, markov-chain]
see_also: [n-gram-language-model, perplexity, causal-language-modeling, generative-pretrained-transformer, masked-language-modeling, autoregressive-model, neural-probabilistic-language-model, source-channel-speech-recognition]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Part I, the approximations to English by sources that choose each letter or word from the ones before it
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft
    locator: chapter N-gram Language Models (draft of January 2026), the chain rule of probability and the end-of-sentence token
---

A language model gives a probability to every finite sequence of tokens, such as the words of a sentence, the characters of a text or the bases of a DNA read, so that more likely sequences get larger values and all the values sum to 1. Almost every language model is written as a sequence of predictions: the probability of the next token given the tokens before it, with a special end token that ends the sequence. In speech recognition, spelling correction and machine translation it supplies the prior on outputs in a noisy-channel system (see [source-channel speech recognition](/source-channel-speech-recognition/)), and it is the object that [n-gram models](/n-gram-language-model/), neural networks and large pretrained models all estimate.

## Definition

Fix a finite **vocabulary** $V$ of tokens that contains an end marker `</s>`, and let $\Sigma = V \setminus \{ \langle /s \rangle \}$. A **sentence** is a sequence $w_1, \ldots, w_n$ with $n \ge 1$, $w_1, \ldots, w_{n-1} \in \Sigma$ and $w_n = \langle /s \rangle$. Let $S$ be the set of all sentences; it is countably infinite.

A **language model** on $V$ is a probability distribution $P$ on $S$: $P(s) \ge 0$ for every $s \in S$ and $\sum_{s \in S} P(s) = 1$.

For a history $h = w_1, \ldots, w_{i-1}$ in $\Sigma^*$, the conditional probability of the next token is

$$P(w \mid h) = \frac{P(\text{sentences that begin with } h\,w)}{P(\text{sentences that begin with } h)}, \qquad w \in V,$$

where a sentence begins with $h\,\langle /s \rangle$ only if it equals it. By the **chain rule**, for every sentence,

$$P(w_1, \ldots, w_n) = \prod_{i=1}^{n} P(w_i \mid w_1, \ldots, w_{i-1}).$$

In the other direction, choose for every history $h \in \Sigma^*$ a distribution $p(\cdot \mid h)$ on $V$, and set $P(s) = \prod_i p(w_i \mid w_{<i})$. This is how models are built in practice. Then $\sum_{s \in S} P(s) = 1 - q$, where $q$ is the probability that the process of drawing token after token never draws `</s>`. So the products define a language model exactly when $q = 0$; such a model is called **tight**. A sufficient condition is that $p(\langle /s \rangle \mid h) \ge \varepsilon$ for some $\varepsilon > 0$ and every $h$, since then the chance of $m$ steps without `</s>` is at most $(1 - \varepsilon)^m$.

Many systems also pad each sentence with a start marker `<s>`, which is part of every history and never predicted, and a token `<unk>` in $V$ that stands for every word outside the vocabulary.

## Examples and non-examples

**A one-word vocabulary.** Let $V = \{a, \langle /s \rangle\}$ and $p(a \mid h) = p(\langle /s \rangle \mid h) = 1/2$ for every $h$. The sentence of $m$ copies of a, then `</s>`, gets $(1/2)^{m+1}$, and $\sum_{m \ge 0} (1/2)^{m+1} = 1$. The length of a sentence is geometric.

**An n-gram model.** An [n-gram language model](/n-gram-language-model/) sets $p(w \mid h)$ from the last $n - 1$ tokens of $h$ only. It has finitely many distinct conditionals, so if each of them gives `</s>` a positive probability, the condition above holds and the model is tight.

**A neural model.** A recurrent network or a [transformer](/transformer/) computes $p(\cdot \mid h)$ by a softmax over $V$ from a vector that depends on all of $h$. This is the setting of [causal language modeling](/causal-language-modeling/) and of [generative pretrained transformers](/generative-pretrained-transformer/).

**A DNA model.** With $V = \{A, C, G, T, \langle /s \rangle\}$, a model of reads gives each read a probability. Models of DNA, protein and music are language models in this sense, though the field often calls them sequence models.

**Not: no end marker.** If $V$ has no `</s>` and $P(w_1, \ldots, w_n) = \prod_i p(w_i \mid w_{<i})$, then for each length $n$ the values sum to 1 over the sequences of that length. The sum over all lengths is infinite, so this is a family of distributions, one per length, and not a language model on finite sequences. Without the end marker, a model also cannot compare a sentence with a longer one that begins with it.

**Not: a stop probability that falls too fast.** Let $p(\langle /s \rangle \mid h) = 1/(i+2)^2$ for every history $h$ of length $i$. The probability that the process never stops is

$$\prod_{i=0}^{\infty} \Big( 1 - \frac{1}{(i+2)^2} \Big) = \prod_{m=2}^{\infty} \frac{(m-1)(m+1)}{m^2} = \frac12,$$

so the sentences get total probability $1/2$. Each $p(\cdot \mid h)$ is a distribution, but the model is not tight.

**Not: a masked language model.** A model trained by [masked language modeling](/masked-language-modeling/) gives $P(w_i \mid \text{the other tokens})$ for a position in a fixed sequence. It does not by itself give a probability to each sentence, so it is not a language model in this sense.

**Not: a score without normalization.** A grammar that accepts or rejects a sentence, or a score that ranks sentences, is not a language model unless its values are nonnegative and sum to 1.

## Related definitions

- **Causal language modeling.** [Causal language modeling](/causal-language-modeling/) is the training task of predicting each token from the ones before it, with the cross-entropy loss; a model trained this way is a language model in the sense above, if it is tight. The language model is the distribution; causal language modeling is a way to estimate it.
- **Generative pretrained transformer.** A [generative pretrained transformer](/generative-pretrained-transformer/) is one architecture for $p(\cdot \mid h)$, a decoder-only transformer, together with its pretraining. It is a language model; most language models are not transformers.
- **Autoregressive model.** An [autoregressive model](/autoregressive-model/) is any model that writes a joint distribution as a product of conditionals in a fixed order. A language model is the autoregressive model of discrete sequences of variable length.
- **Markov chain.** A model whose next-token distribution depends only on a bounded part of the history is a [Markov chain](/markov-chain/) on the states made of that part. The n-gram model is the classic case.
- **Perplexity.** [Perplexity](/perplexity/) measures how well a language model predicts a held-out text.
- **Conditional language model.** A distribution $P(y \mid x)$ over output sentences $y$ for each input $x$, as in translation or speech recognition, is a family of language models, one for each $x$.

## References
