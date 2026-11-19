---
tag: C12QAQ
kind: technique
slug: causal-language-modeling
name: Causal language modeling
aliases:
- next-token prediction
- autoregressive language modeling
area: natural-language-and-speech/language-modeling
level: core
summary: "Train a network to predict each token from the tokens before it, with a triangular attention mask so no position sees the future."
prereqs: [language-model, cross-entropy-loss, scaled-dot-product-attention]
see_also: [masked-language-modeling, generative-pretrained-transformer, transformer, perplexity, teacher-forcing, exposure-bias, key-value-cache, n-gram-language-model]
sources:
  - paper: "Yoshua Bengio, Réjean Ducharme, Pascal Vincent and Christian Jauvin, A neural probabilistic language model, Journal of Machine Learning Research 3 (2003) 1137-1155"
    title: Bengio et al. 2003
    locator: the factorization of the joint probability into next-word conditionals and the training by log-likelihood
  - paper: "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser and Illia Polosukhin, Attention is all you need, Advances in Neural Information Processing Systems 30 (NIPS 2017)"
    title: Vaswani et al. 2017
    locator: Section 3.2.3 (masking the illegal connections in the decoder by setting them to minus infinity before the softmax)
  - paper: "Alec Radford, Karthik Narasimhan, Tim Salimans and Ilya Sutskever, Improving language understanding by generative pre-training, OpenAI technical report, 2018"
    title: Radford et al. 2018
    locator: the unsupervised pre-training objective with a decoder-only transformer, followed by supervised fine-tuning
  - paper: "Mohammad Bavarian, Heewoo Jun, Nikolas Tezak, John Schulman, Christine McLeavey, Jerry Tworek and Mark Chen, Efficient training of language models to fill in the middle, arXiv:2207.14255, 2022"
    title: Bavarian et al. 2022
    locator: the transformation that moves a middle span to the end, so a causal model learns to fill in text
  - paper: "Claude E. Shannon, Prediction and entropy of printed English, Bell System Technical Journal 30(1):50-64, 1951"
    title: Shannon 1951
    locator: the estimate of the entropy of English from the next-letter predictions of people
---

Causal language modeling trains a network to give, at every position of a text, a probability distribution over the next token given only the tokens before it. By the chain rule, $P(x_1, \ldots, x_n) = \prod_t P(x_t \mid x_{<t})$, so a model of these next-token distributions is a full [language model](/language-model/), and one that can generate text by sampling one token at a time. The loss is the [cross-entropy](/cross-entropy-loss/) of the true next tokens, which is the negative log-likelihood of the text. In a [transformer](/transformer/) decoder, a triangular mask in [attention](/scaled-dot-product-attention/) stops each position from seeing later positions, so one forward pass over a sequence of $n$ tokens gives all $n$ predictions at once. This is the training objective of [GPT](/generative-pretrained-transformer/) and of most large language models.

## In plain words

Cover a text with a card and slide the card to the right one word at a time. At each step, guess the next word from what you can see. The model learns by making these guesses on a very large amount of text and being scored by how much probability it gave to the word that really came next.

A model trained this way can write: guess a word, add it to the text, and guess again.

In training, all the guesses for one text are made at the same time. Each position is blocked from looking at the words to its right, so no guess can copy the answer.

## When it applies

- Any model that must generate text left to right: chat models, code completion, translation decoders, speech recognition decoders.
- Pre-training on raw text with no labels: every token is a target, so there are about as many training signals as tokens.
- Scoring text: the summed log-probability of a sentence gives its likelihood, and the mean loss gives its [perplexity](/perplexity/).
- When a bidirectional representation of a fixed input is the goal, as in classification of sentences, [masked language modeling](/masked-language-modeling/) uses context from both sides and is often a better fit.

## The template

Given a text $x_1, \ldots, x_n$ and a model with parameters $\theta$ that outputs logits $z_t \in \mathbb{R}^V$ at each position:

1. **Shift.** The input is $x_1, \ldots, x_{n-1}$ and the target at position $t$ is $x_{t+1}$.
2. **Mask.** In every self-attention layer, add to the score of query $i$ and key $j$ the mask $M_{ij} = 0$ if $j \le i$ and $M_{ij} = -\infty$ if $j > i$, before the softmax.
3. **Predict.** $P_\theta(\cdot \mid x_{\le t}) = \mathrm{softmax}(z_t)$.
4. **Loss.** The mean cross-entropy
$$\mathcal{L}(\theta) = -\frac{1}{n-1} \sum_{t=1}^{n-1} \log P_\theta(x_{t+1} \mid x_{\le t}),$$
averaged over a batch and minimized by [backpropagation](/backpropagation/) and a gradient method such as [Adam](/adam/).
5. **Generate.** At test time, feed the tokens so far, pick the next token from $\mathrm{softmax}(z_t)$ by [greedy decoding](/greedy-decoding/), sampling or [beam search](/beam-search/), append it and repeat. A [key-value cache](/key-value-cache/) keeps the keys and values of past positions so each step processes one new token.

Feeding the true tokens as input in step 1, and not the model's own guesses, is [teacher forcing](/teacher-forcing/).

**The mask gives valid conditionals (theorem).** With the mask in every attention layer, and all other layers acting on each position alone, the output at position $t$ depends only on $x_1, \ldots, x_t$. By induction on the layers: the input at $t$ depends on $x_t$ alone; a position-wise layer keeps the set of inputs it depends on; and masked attention at $t$ mixes only positions $j \le t$, each of which depends on $x_{\le j} \subseteq x_{\le t}$. So $\mathrm{softmax}(z_t)$ is a function of $x_{\le t}$, a proper conditional, and the summed loss is exactly $-\log P_\theta(x_2, \ldots, x_n \mid x_1)$.

**The minimizer is the true conditional (theorem).** For a fixed context $c$, the expected loss $-\sum_w p(w \mid c) \log q(w)$ over distributions $q$ equals the entropy of $p(\cdot \mid c)$ plus the [Kullback-Leibler divergence](/kullback-leibler-divergence/) $D(p \,\|\, q)$, which is zero only at $q = p$. So with enough capacity and data, minimizing the loss recovers the next-token distribution of the source, and the lowest possible mean loss is its entropy rate.

## Classic examples

**A three-word step.** A model with vocabulary $\{a, b, c\}$ outputs the logits $(2, 1, 0)$. The softmax gives $(0.665241, 0.244728, 0.090031)$. If the true next token is $a$ the loss is $-\ln 0.665241 = 0.407606$ nats; if it is $b$ the loss is $1.407606$.

**Perplexity of a short text.** A model gives the four true next tokens of a text the probabilities $\tfrac12, \tfrac14, \tfrac18, \tfrac18$. The losses are 1, 2, 3 and 3 bits, with mean 2.25 bits $= 1.559581$ nats, and the [perplexity](/perplexity/) is $2^{2.25} = 4.756828$: the model is as unsure as a uniform choice among about 4.76 tokens.

**N-gram models.** An [n-gram language model](/n-gram-language-model/) is a causal language model that keeps only the last $n - 1$ tokens of the context and estimates the conditionals by counting, with smoothing for unseen n-grams.

**Neural language models.** The [neural probabilistic language model](/neural-probabilistic-language-model/) of Bengio and colleagues learned the conditionals with word embeddings and a fixed window; the [recurrent language model](/recurrent-neural-network-language-model/) used the whole prefix through a hidden state.

**GPT.** [GPT](/generative-pretrained-transformer/) pre-trains a decoder-only transformer with this objective on raw text and then adapts it to tasks. Larger models of this kind show [in-context learning](/in-context-learning/), and their loss follows [neural scaling laws](/neural-scaling-law/) in model size, data and compute (a measurement).

**Human prediction.** Shannon estimated the entropy of English by asking people to guess the next letter of a text, the same task with a person as the model.

## Variations

- **Prefix language modeling.** The first part of the input is seen with full attention, and only the rest is predicted with the causal mask. It mixes an encoder over the prefix with a decoder.
- **Fill in the middle.** Cut a document into prefix, middle and suffix, move the middle to the end with marker tokens, and train with the plain causal objective. The model can then fill a gap given text on both sides, as Bavarian and colleagues showed for code and text.
- **Packing.** Short documents are joined with a separator token into sequences of fixed length to avoid padding. The attention mask may also be cut at document boundaries.
- **Other causal models.** The objective does not need attention: [recurrent networks](/recurrent-neural-network-language-model/) and [selective state space models](/selective-state-space-model/) are causal by construction.
- **Label smoothing.** Mixing the one-hot target with a uniform distribution, as in [label smoothing](/label-smoothing/), was used in the original transformer for translation.

## Pitfalls

- **Off-by-one shift.** Predicting $x_t$ from a position that already sees $x_t$ gives a near-zero loss and a useless model. Check that the target at position $t$ is $x_{t+1}$ and that the mask allows $j \le t$ only.
- **Leaks through other paths.** A bidirectional layer, a normalization over the time axis, or a convolution that is not causal lets the future into position $t$ even with a correct attention mask.
- **Loss on padding.** Padding positions must be left out of the loss and of the mean; otherwise short sequences change the scale of the loss.
- **Comparing perplexities.** Perplexity per token depends on the tokenizer. Compare models with different [subword tokenizations](/subword-tokenization/) by bits per character or per byte instead.
- **Exposure bias.** In training the model always sees true prefixes, but in generation it sees its own outputs, and early errors can push it to contexts it never saw; see [exposure bias](/exposure-bias/).
- **Not a bidirectional encoder.** The representation at position $t$ knows nothing of the words after $t$, which hurts tasks such as tagging the first word of a sentence.

## Exercises

1. Prove by induction on the layers that, with the causal mask, the output at position $t$ of a transformer decoder does not depend on $x_{t+1}, \ldots, x_n$.
2. Show that $-\sum_w p(w) \log q(w) = H(p) + D(p \,\|\, q)$ and conclude that the expected loss is minimized at $q = p$.
3. A model gives the true tokens of a text of 5 tokens the probabilities $0.5, 0.5, 0.25, 0.25, 0.125$. Compute the mean loss in bits and the perplexity.
4. Show that a bigram model is a causal language model whose conditionals depend on $x_{t-1}$ alone, and write its maximum-likelihood estimate.
5. With a key-value cache, count the attention operations needed to generate $T$ tokens after a prompt of $P$ tokens, and compare with running the full model again at every step.

## References
