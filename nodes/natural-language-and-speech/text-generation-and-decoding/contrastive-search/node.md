---
tag: AYJ2SK
kind: algorithm
slug: contrastive-search
name: Contrastive search
aliases:
- degeneration penalty decoding
area: natural-language-and-speech/text-generation-and-decoding
level: research
summary: Choose among the top-k tokens by probability minus a penalty for the maximum cosine similarity of its hidden state to earlier ones.
solves: [autoregressive-decoding]
model: real-ram
complexity:
  vars: {n: the number of output tokens, L: the length of the prompt, k: the number of candidates, d: the dimension of the hidden states, V: "the vocabulary size |V|", C: the cost of one call of the model}
  time: {worst: "O(n (k C + V + k (L + n) d))"}
  space: {extra: "O((L + n) d + V)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2022
  people: [Yixuan Su, Tian Lan, Yan Wang, Dani Yogatama, Lingpeng Kong, Nigel Collier]
  note: Su et al. proposed contrastive search together with the SimCTG training objective at NeurIPS 2022.
prereqs: [greedy-decoding, top-k-sampling, cosine-similarity, transformer]
see_also: [greedy-decoding, top-k-sampling, nucleus-sampling, repetition-penalty, beam-search, maximal-marginal-relevance, inadequacy-of-the-mode, key-value-cache]
sources:
  - url: https://proceedings.neurips.cc/paper_files/paper/2022/hash/871cae8f599cb8bbfcb0f58fe1af95ad-Abstract-Conference.html
    title: "Yixuan Su, Tian Lan, Yan Wang, Dani Yogatama, Lingpeng Kong and Nigel Collier, A contrastive framework for neural text generation, NeurIPS 2022"
    locator: "Section 3.2, Equation 5 (the score of contrastive search: model confidence minus the degeneration penalty over the top-k candidates), Section 3.1 (the SimCTG objective), and Section 6.4 (decoding speed against beam search)"
  - url: https://arxiv.org/abs/2202.06417
    title: "Yixuan Su, Tian Lan, Yan Wang, Dani Yogatama, Lingpeng Kong and Nigel Collier, A contrastive framework for neural text generation, arXiv 2202.06417"
    locator: "the experiments on Wikitext-103 with k = 8 and alpha = 0.6, and the remark that alpha = 0 gives greedy search"
  - url: https://arxiv.org/abs/1904.09751
    title: "Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes and Yejin Choi, The curious case of neural text degeneration, ICLR 2020"
    locator: "Section 1 and Table 1, the repetition of greedy decoding and beam search that contrastive search aims to avoid"
---

Contrastive search is a deterministic decoder for an autoregressive [language model](/language-model/). At each step it takes the $k$ most probable next tokens as candidates. For each candidate it runs the model one more step to get the hidden state of that token, and it measures how similar that state is to the states of the tokens already in the text, by the largest [cosine similarity](/cosine-similarity/). It picks the candidate with the best score, the probability minus a penalty for that similarity. A token that would make the text say again what it already said gets a high penalty. The aim is to keep the coherence of [greedy decoding](/greedy-decoding/) and avoid its loops, without the randomness of sampling. With weight $\alpha = 0$ on the penalty, or with $k = 1$, it is greedy decoding. It is a heuristic for [autoregressive decoding](/autoregressive-decoding/): Su et al. 2022 reported better human ratings than sampling methods on their tasks, which is a measurement, not a property of the method.

## In plain words

Greedy decoding always takes the most likely next word, and so it often says the same thing again and again. Contrastive search looks at the few most likely words, for example the top five. For each of them, it asks how much the text would look like what is already written if that word came next. It then picks the word that is likely and also brings something new. One setting balances the two. When the setting is zero, it is plain greedy decoding. It uses no random draws, so the same input always gives the same text.

## The problem

The model gives, for a prefix $y_{<t}$, the next-token distribution $p(\cdot \mid y_{<t})$ over the vocabulary $V$ and a hidden-state vector $h_j$ for each position $j < t$ (the last layer of a [transformer](/transformer/), in practice). For a candidate $v$, let $h_v$ be the state of the new last position when $v$ is appended. Contrastive search chooses

$$y_t = \arg\max_{v \in V^{(k)}} \Big\{ (1 - \alpha) \, p(v \mid y_{<t}) - \alpha \max_{1 \le j < t} s(h_v, h_j) \Big\},$$

where $V^{(k)}$ is the set of the $k$ most probable tokens, $s$ is the cosine similarity, and $0 \le \alpha \le 1$. This is Equation 5 of Su et al. 2022. The first term is the model confidence and the second the degeneration penalty. The context includes the prompt. The output is a fixed function of the model and the prompt; no objective over whole sequences is maximized.

## The algorithm

Tokens are numbered, and the tie rules are fixed: among equal probabilities the smaller index comes first in $K$, and among equal scores the first candidate in $K$ wins.

```pseudo id=main
CONTRASTIVE-SEARCH(model, x, N, k, α)   ▷ model(y) = (p, the hidden states of y)
L1  y ← x                                 ▷ the prompt
L2  for t ← 1 to N do
L3      (p, H) ← model(y)                ▷ H = the states of all positions of y
L4      K ← the min(k, |V|) most probable tokens, from high to low
L5      for each v in K do
L6          h_v ← the last state of model(y followed by v)
L7          score[v] ← (1 − α) p[v] − α · max over h in H of cos(h_v, h)
L8      w ← the first v in K with the largest score
L9      append w to y
L10     if w = "</s>" then return y
L11 return y
```

The calls of line L6 can run as one batch of $k$ sequences, and with a [key-value cache](/key-value-cache/) each of them processes one new token only. The states $H$ of earlier positions do not change, because the model is causal, so they can be kept from step to step.

## Example

**One step.** The context has two states, $h_1 = (1, 0)$ and $h_2 = (0.6, 0.8)$. The three candidates are:

| candidate | $p$ | $h_v$ | cos to $h_1$ | cos to $h_2$ | penalty | score, $\alpha = 0.6$ |
|---|---|---|---|---|---|---|
| A | 0.5 | $(1, 0.1)$ | 0.9950 | 0.6766 | 0.9950 | $0.2 - 0.5970 = -0.3970$ |
| B | 0.3 | $(0, 1)$ | 0 | 0.8 | 0.8 | $0.12 - 0.48 = -0.36$ |
| C | 0.2 | $(-0.6, 0.8)$ | $-0.6$ | 0.28 | 0.28 | $0.08 - 0.168 = -0.088$ |

With $\alpha = 0.6$, the step picks C, the least probable candidate, because its state points away from the context. With $\alpha = 0.3$ the scores are 0.0515, $-0.03$ and 0.056, and C still wins by a little. With $\alpha = 0.2$ they are 0.2010, 0.08 and 0.104, and A wins. With $\alpha = 0$ the step is greedy and picks A.

**A loop.** Take a toy model that gives a 0.5, b 0.3, c 0.15 and "</s>" 0.05 after every prefix, and whose state for a token is a one-hot vector of that token. Greedy decoding writes a a a a forever. Contrastive search with $k = 3$ and $\alpha = 0.6$ writes a (no penalty yet), then b (a now has penalty 1 and score $-0.4$, b has $0.12$), then c. At the fourth step all three candidates have penalty 1, the probability decides, and it writes a again. The penalty spreads the text over the candidates; it does not forbid a token.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that each step returns the first candidate of largest score, that the search makes $\min(k, |V|) + 1$ calls of the model per step, and that $\alpha = 0$ or $k = 1$ gives exactly the output of greedy decoding. It also shows that scaling the hidden states by positive numbers changes nothing, and that since the penalty lies between $-1$ and 1, a candidate $v$ beats a candidate $w$ whatever the states when $(1 - \alpha)(p(v) - p(w)) > 2\alpha$. The tests check the steps against a direct computation of all the scores on random toy models, and the greedy limits against a greedy decoder.

## Complexity

Each step makes one call of the model on the prefix and $k$ calls for the candidates, $k + 1$ calls of cost $C$ in all, or one call plus one batched call. The penalties compare $k$ states with the $L + t$ states of the context, each a vector of dimension $d$, so step $t$ costs $O(k (L + t) d)$ for the similarities and $O(|V|)$ for the top $k$ with a selection. For $n$ output tokens this sums to $O(n (k C + |V| + k (L + n) d))$. The extra space holds the states of the context, $O((L + n) d)$, and one row of probabilities. Su et al. measured a decoding time comparable to that of beam search with a similar width.

## Properties

- **Deterministic.** The same model, prompt and settings give the same output.
- **Greedy limits.** $\alpha = 0$ and $k = 1$ both give [greedy decoding](/greedy-decoding/).
- **Not a search for the mode.** The output is usually less probable than the greedy output; the method trades probability for diversity on purpose.
- **Needs hidden states.** Unlike the sampling methods, it needs access to the internal states of the model, not only to the probabilities.
- **Scale free.** Only the directions of the states matter.

## Variants and improvements

- **SimCTG.** Su et al. trained the model with a contrastive objective in addition to the usual likelihood, which pushes the states of different tokens apart (a margin of 0.5 in their experiments), so that the cosine penalty separates tokens better.
- **Other similarity measures.** Any similarity between the candidate and the context fits the template; cosine on the last hidden layer is the published choice.
- **Sampling with a penalty.** A [repetition penalty](/repetition-penalty/) lowers the logits of tokens that already appear, which works on token identity in place of hidden states.
- **Maximal marginal relevance.** The score has the same form as [maximal marginal relevance](/maximal-marginal-relevance/) in retrieval: relevance minus the largest similarity to what is already chosen.

## When to use it

Use contrastive search for open-ended generation, such as continuing a document or a story, when deterministic output is wanted and greedy decoding or beam search repeats itself. Su et al. suggest $k$ from 3 to 10, and used $k = 8$ and $\alpha = 0.6$ on Wikitext-103. It costs about $k$ times more model computation per step than greedy decoding, so it suits settings where a batch of $k$ candidates is cheap. For translation or short answers, use greedy decoding or beam search; for varied outputs from the same prompt, use sampling.

## Pitfalls

- **A large $\alpha$ gives incoherent text.** The example shows the penalty overruling a probability of 0.5 in favor of 0.2. With $\alpha$ near 1 the method picks whatever is least similar to the context.
- **The penalty uses states, not words.** Two different words with similar states are penalized, and a repeated word with a different state is not. The effect depends on the geometry of the states of the model, which is why Su et al. trained it with SimCTG.
- **Cost per step.** The $k$ extra calls are cheap only in a batch with a key-value cache. Without them the method is $k + 1$ times slower than greedy decoding.
- **Zero vectors.** The cosine of a zero vector is undefined. Fix a value (here 0) if states can be zero.

## Implementations

The code takes the next-token probabilities and the hidden states of the model as given, through a function of the prefix, and implements the search around them; it does not run or train a network.

## History

Su, Lan, Wang, Yogatama, Kong and Collier proposed contrastive search with the SimCTG training objective in "A contrastive framework for neural text generation", posted on arXiv in February 2022 and published at NeurIPS 2022. They argued that the repetition of greedy decoding and beam search, documented by Holtzman et al. 2020, comes in part from an anisotropic distribution of the token representations, and attacked it from both sides: a training objective that spreads the representations, and a decoder that penalizes similar ones.

## References
