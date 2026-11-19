---
tag: TXBYG6
kind: model
slug: recurrent-neural-network-language-model
name: Recurrent neural network language model
aliases:
- RNN language model
- RNNLM
area: natural-language-and-speech/language-modeling
level: core
summary: "A language model whose recurrent hidden state summarizes the whole history and gives a softmax over the next word at each step."
history:
  year: 2010
  people: [Tomáš Mikolov, Martin Karafiát, Lukáš Burget, Jan Černocký, Sanjeev Khudanpur]
  note: Mikolov and colleagues used the simple recurrent network of Elman (1990) as a language model for speech recognition at Interspeech 2010, and beat a large Kneser-Ney model by a wide margin.
prereqs: [neural-probabilistic-language-model, backpropagation-through-time]
see_also: [neural-probabilistic-language-model, backpropagation-through-time, vanishing-gradient-problem, exploding-gradient-problem, gradient-clipping, cache-language-model, transformer, perplexity]
sources:
  - paper: doi:10.21437/Interspeech.2010-343
    title: Tomáš Mikolov, Martin Karafiát, Lukáš Burget, Jan Černocký and Sanjeev Khudanpur, Recurrent neural network based language model, Proceedings of Interspeech 2010, pages 1045 to 1048
    locator: the model x(t) = [w(t); s(t-1)] with a sigmoid hidden layer and a softmax output, the training with truncated backpropagation through time, the dynamic model, the class for rare words, and the results on Wall Street Journal and NIST RT05
  - paper: doi:10.1207/s15516709cog1402_1
    title: Jeffrey L. Elman, Finding structure in time, Cognitive Science 14(2), 1990, pages 179 to 211
    locator: the simple recurrent network, with context units that hold a copy of the previous hidden state, trained to predict the next element of a sequence
  - paper: doi:10.1162/neco.1997.9.8.1735
    title: Sepp Hochreiter and Jürgen Schmidhuber, Long short-term memory, Neural Computation 9(8), 1997, pages 1735 to 1780
    locator: the gated memory cell that keeps the error signal from vanishing over long time lags
---

A recurrent neural network language model reads a text one word at a time and keeps a hidden state, a vector that is updated from the previous state and the current word. From the state it gives a [softmax](/softmax-regression/) over the next word. So the prediction depends, in principle, on the whole history, not only on the last $n - 1$ words as in an [n-gram model](/n-gram-language-model/) or the [neural probabilistic language model](/neural-probabilistic-language-model/). The network is the simple recurrent network of Elman (1990). Mikolov and colleagues used it as a language model for speech recognition in 2010, and on Wall Street Journal data a mixture of such models had about half the perplexity of a large Kneser-Ney model.

## The machine

**Parameters.** For a vocabulary $V$ and $H$ hidden units:

- $U$, an $H \times |V|$ matrix; column $w$ is the input vector of the word $w$;
- $W$, an $H \times H$ matrix, the recurrent weights;
- $V_o$, a $|V| \times H$ matrix, the output weights.

**The step.** Let $w(t)$ be the one-hot vector of the current word and $s(t-1)$ the previous state. Mikolov and colleagues write the input as the concatenation $x(t) = [w(t); s(t-1)]$. Then

$$s(t) = \sigma\big(U w(t) + W s(t-1)\big), \qquad y(t) = \operatorname{softmax}\big(V_o\, s(t)\big),$$

with the logistic function $\sigma(z) = 1/(1 + e^{-z})$ applied to each unit, and $y_k(t)$ is the probability that the next word is $k$. The state starts as a fixed vector, for example all zeros or all 0.1. Because $w(t)$ is one-hot, $U w(t)$ is just a column of $U$, so the input costs no multiplications.

**Training.** The parameters maximize the log-likelihood of the training text by stochastic gradient descent. The gradient flows back through the recurrence by [backpropagation through time](/backpropagation-through-time/), cut after $\tau$ steps. In the 2010 paper $\tau = 1$, so the error goes back into $s(t-1)$ but not further; the start rate was $0.1$, and the hidden layer had 30 to 500 units. Words below a count threshold share one rare-word output, and a rare word $w$ gets $y_{\text{rare}}(t) / C_{\text{rare}}$, with $C_{\text{rare}}$ the number of rare words.

**The dynamic model.** The *dynamic* version keeps training on the test text as it reads it: after each word it takes one gradient step on that word. Like a [cache](/cache-language-model/), this adapts the model to the current document.

**An example.** Take $V = \{a, b, c\}$, $H = 2$, $W = \frac12 I$, input columns $(1, 0)$ for a, $(-1, 1)$ for b and $(0, -1)$ for c, and output rows $(2, 0)$ for a, $(0, 2)$ for b and $(-1, -1)$ for c, with $s(0) = 0$. After the word a the state is $(\sigma(1), \sigma(0)) = (0.7311, 0.5)$. After "a c" it is $(\sigma(0.3655), \sigma(-0.75)) = (0.5904, 0.3208)$, and the next word has the distribution $(0.5859, 0.3417, 0.0723)$. After "b c" the state is $(0.5336, 0.3465)$ and the distribution is $(0.5463, 0.3758, 0.0779)$. Both histories end in c, so a bigram model would give them the same distribution; the state still remembers the first word.

## What it counts

The model is measured by its [perplexity](/perplexity/) on test text, and in a recognizer by the word error rate after rescoring. The cost of one step is the number of multiply-adds:

- the recurrence, $H^2$, plus $H$ for the input column;
- the output, $H |V|$, and $O(|V|)$ for the softmax.

With $H = 200$ and $|V| = 10{,}000$ that is $40{,}000$ for the recurrence against $2{,}000{,}000$ for the output, so, as in the feedforward model, the output dominates. Truncated backpropagation through time over $\tau$ steps adds about $\tau H^2$ per word for the gradient of the recurrence. Unlike an n-gram model, the state is a continuous vector, so a recognizer cannot merge two hypotheses that end in the same words: a lattice or an n-best list is usually rescored after a first pass with an n-gram model.

## Relation to other models

- **Feedforward neural models.** The [neural probabilistic language model](/neural-probabilistic-language-model/) sees a fixed window of $n - 1$ words. The recurrent model replaces the window by the state, which has a fixed size but depends on all earlier words.
- **n-gram models.** An n-gram model is the special case where the state is the last $n - 1$ words. The recurrent state is learned and can keep some of the earlier context.
- **Hidden Markov models.** Both carry a state from step to step, but the [hidden Markov model](/hidden-markov-model/) state is discrete and random, while the recurrent state is a deterministic real vector.
- **Gated recurrent networks.** Long short-term memory (Hochreiter and Schmidhuber 1997) adds gates and a memory cell to the recurrent unit. It lets the error signal survive over many steps and replaced the simple recurrent unit in later language models.
- **Cache models.** The dynamic model adapts to the test document by training on it, and the neural [cache](/cache-language-model/) of Grave, Joulin and Usunier adds an explicit memory of recent states.
- **Transformers.** A [transformer](/transformer/) language model drops the recurrence: each position looks at all earlier positions through attention, which trains in parallel over the positions.

## Known results in the model

- **Wall Street Journal.** Against a 5-gram Kneser-Ney model with perplexity 221 and word error rate 13.5 percent, a mixture of recurrent models with the 5-gram model reached a perplexity of 112 and a word error rate of 11.1 percent: about 50 percent lower perplexity and about 18 percent fewer errors.
- **NIST RT05.** On meeting speech the word error rate was 24.1 percent with the baseline, 23.3 percent with static recurrent models and 22.8 percent with dynamic ones.
- **Long dependence is hard to learn.** The gradient through $k$ steps is a product of $k$ Jacobians of the step, so it tends to shrink or grow exponentially in $k$: the [vanishing gradient problem](/vanishing-gradient-problem/) and the [exploding gradient problem](/exploding-gradient-problem/). [Gradient clipping](/gradient-clipping/) handles the second, and gated units the first.
- **The output bottleneck.** As for the feedforward model, the softmax over $V$ is the main cost. A factored output through word classes, the [hierarchical softmax](/hierarchical-softmax/) and [noise-contrastive estimation](/noise-contrastive-estimation/) reduce it.
- **Mixing helps.** The recurrent model and the n-gram model make different errors, so a linear mixture of the two is better than either, which is how the 2010 results were obtained.

## References
