---
tag: G371BC
kind: algorithm
slug: nucleus-sampling
name: Nucleus sampling
aliases:
- top-p sampling
area: natural-language-and-speech/text-generation-and-decoding
level: core
summary: "Sample from the smallest set of most probable next tokens whose total probability reaches p, so the candidate set adapts to the shape."
solves: [autoregressive-decoding]
model: real-ram
complexity:
  vars: {V: "the vocabulary size |V|", m: the number of tokens in the nucleus}
  time: {worst: "O(V log V)"}
  space: {extra: "O(V)"}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 2020
  people: [Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, Yejin Choi]
  note: 'Holtzman et al. introduced nucleus sampling in "The curious case of neural text degeneration", first posted on arXiv in April 2019 and published at ICLR 2020.'
prereqs: [top-k-sampling, autoregressive-decoding, language-model]
see_also: [top-k-sampling, temperature-sampling, typical-sampling, greedy-decoding, ancestral-sampling, contrastive-search, inadequacy-of-the-mode, repetition-penalty]
sources:
  - url: https://arxiv.org/abs/1904.09751
    title: "Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes and Yejin Choi, The curious case of neural text degeneration, ICLR 2020"
    locator: "Section 3.1 (the top-p vocabulary V(p) of Equation 2 and the rescaled distribution of Equation 3), Section 3.2 (top-k), Section 3.3 (temperature), and Table 1 (perplexity, Self-BLEU4, Zipf coefficient, repetition and HUSE of the decoding methods on GPT-2 Large)"
  - paper: doi:10.18653/v1/P18-1082
    title: "Angela Fan, Mike Lewis and Yann Dauphin, Hierarchical neural story generation, ACL 2018, pages 889 to 898"
    locator: "Section 5.4, top-k random sampling, the fixed-size method that nucleus sampling replaces"
---

Nucleus sampling, also called top-p sampling, generates text from an autoregressive [language model](/language-model/) one token at a time. At each step it sorts the next tokens by probability and keeps the shortest list from the top whose total probability is at least a threshold $p$, such as 0.9 or 0.95. This list is the nucleus. It divides the kept probabilities by their sum and draws the next token from them. When the model is sure of the next token the nucleus has one or two tokens, and when the model is unsure it has many. That is the difference from [top-k sampling](/top-k-sampling/), which keeps the same number of tokens at every step. Nucleus sampling is a heuristic method for [autoregressive decoding](/autoregressive-decoding/). Holtzman et al. 2020 found that its output matched human text better than greedy decoding, beam search, pure sampling and top-k sampling on their measures, but that is a measurement on one model and one data set, not a property of the algorithm.

## In plain words

The model gives a chance to every word that can come next. Sort the words from the most likely to the least likely. Walk down the list and add up the chances. Stop as soon as the total reaches a set share, for example 90%. Keep only the words you passed and draw one of them at random, in proportion to their chances. If one word is very likely, you keep only that word. If many words are about equally likely, you keep many. So the list grows and shrinks with the doubt of the model.

## The problem

The model gives a distribution $P = P(\cdot \mid y_{<t})$ over the vocabulary $V$ for the prefix $y_{<t}$. Sort the tokens by probability from high to low, with the smaller index first on ties, and let $M(m)$ be the mass of the first $m$ tokens. The nucleus $V^{(p)}$ is the first $m^*$ tokens, where $m^*$ is the smallest $m$ with $M(m) \ge p$. One step draws $y_t$ from

$$q_p(i) = \frac{P_i \, [i \in V^{(p)}]}{\sum_{j \in V^{(p)}} P_j}.$$

This is Equations 2 and 3 of Holtzman et al. 2020. The full output repeats the step until the end token `</s>` or a length limit. The output distribution is not the model distribution $P(y)$; the method is defined by the rule.

## The algorithm

The step takes $P$, the threshold $0 < p \le 1$, and a number $u$ drawn uniformly from $[0, 1)$.

```pseudo id=main
NUCLEUS-SAMPLE(P, p, u)               ▷ P = next-token distribution, u uniform in [0, 1)
L1  order ← the tokens sorted by P, from high to low   ▷ ties: the smaller index first
L2  c ← 0,  K ← empty list
L3  for each i in order do
L4      c ← c + P[i],  append i to K
L5      if c ≥ p then stop the loop
L6  Z ← c                             ▷ the mass of the nucleus K
L7  r ← u · Z
L8  c ← 0;  for each i in K, in order do
L9      c ← c + P[i]
L10     if r < c then return i
L11 return the last i in K with P[i] > 0   ▷ only after rounding
```

Lines L7 to L10 are [inverse transform sampling](/inverse-transform-sampling/) on the nucleus, with the bound $Z$ moved to the random number so that nothing is divided.

## Example

Take six next tokens with $P$ = (the 0.40, a 0.25, cat 0.15, dog 0.10, sat 0.06, ran 0.04), already sorted. The running masses are 0.40, 0.65, 0.80, 0.90, 0.96 and 1.

| $p$ | nucleus | mass | renormalized |
|---|---|---|---|
| 0.5 | the, a | 0.65 | the 0.6154, a 0.3846 |
| 0.9 | the, a, cat, dog | 0.90 | 0.4444, 0.2778, 0.1667, 0.1111 |
| 0.95 | the, a, cat, dog, sat | 0.96 | 0.4167, 0.2604, 0.15625, 0.1042, 0.0625 |
| 1 | all six | 1 | $P$ itself |

With $p = 0.9$ the mass 0.90 reaches the threshold exactly at "dog", so "dog" is kept and "sat" is not.

Now take $p = 0.9$ on two other steps. On a peaked step, $P$ = (0.90, 0.05, 0.03, 0.02), the first token already has mass 0.90, so the nucleus is that token alone and the step is greedy. On a flat step with ten tokens of 0.1 each, the nucleus has nine tokens. [Top-k sampling](/top-k-sampling/) with $k = 3$ would keep three tokens in both cases.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that the nucleus is a smallest set of tokens with mass at least $p$, that among the sets of that size it has the largest mass, that it holds no token of probability 0, and that the step returns each token of the nucleus with probability exactly $P_i / Z$. The limits follow: for $p$ at most the largest probability the step is greedy, and for $p = 1$ it samples from $P$. The tests check the smallest size against all subsets on random distributions with Fraction probabilities, and check the draw exactly with $u$ on a fine grid.

## Complexity

One step costs $O(|V| \log |V|)$ with a full sort, plus $O(m)$ for the prefix sums and the draw, where $m$ is the size of the nucleus. The size $m$ is not known in advance, so a plain [top-k selection](/top-k-selection/) does not apply directly. A selection that splits the tokens around a pivot and recurses on the side that holds the boundary, as in [quickselect](/quickselect/) but with the mass in place of the count, finds the nucleus in expected $O(|V|)$ time, plus $O(m \log m)$ to sort it. The extra space is $O(|V|)$. On a GPU, frameworks usually sort the whole row; for a large model the call of the network costs far more than the sort.

## Properties

- **Randomized.** Fix the seed of the random source to reproduce an output.
- **Adaptive size.** The nucleus can have any size from 1 to $|V|$, and it changes from step to step with the shape of $P$.
- **Smallest set.** No set of fewer tokens reaches mass $p$, and the nucleus has the largest mass among the sets of its size.
- **Depends on the temperature.** Unlike top-k, the nucleus depends on the values of the probabilities, not only on their order. On the logits (2, 1, 0), the temperature $T = 1$ gives (0.665, 0.245, 0.090) and $p = 0.8$ keeps two tokens, while $T = 0.5$ gives (0.867, 0.117, 0.016) and keeps one.
- **Limits.** A very small $p$ gives greedy decoding, and $p = 1$ gives [ancestral sampling](/ancestral-sampling/).

## Variants and improvements

- **With temperature.** Apply the temperature to the logits, then take the nucleus ([temperature sampling](/temperature-sampling/)). The order of the two operations matters.
- **With top-k.** Many libraries apply top-k first and then top-p, so that the nucleus never has more than $k$ tokens.
- **Typical sampling.** Order the tokens by how close their surprisal is to the entropy of the step, in place of their probability, and keep a prefix of mass $\tau$ ([typical sampling](/typical-sampling/)).
- **A minimum probability.** Keep the tokens with probability at least a fixed share of the largest probability. Like the nucleus, this adapts to the shape of the distribution.
- **Contrastive search.** A deterministic alternative that scores the top candidates with a penalty for similarity to the context ([contrastive search](/contrastive-search/)).

## When to use it

Use nucleus sampling for open-ended generation, such as stories, dialogue and chat, where varied text is wanted. Values of $p$ from 0.9 to 0.95 are common, often with a temperature below 1. It is the default sampler of many systems. For tasks with a single correct answer, such as translation, short factual answers or code that must compile, greedy decoding or beam search is usually better, and for reasoning tasks several samples can be combined by [self-consistency](/self-consistency-decoding/).

## Pitfalls

- **Rounding at the threshold.** With floats, $0.7 + 0.2 = 0.8999999999999999 < 0.9$, so on $P = (0.7, 0.2, 0.1)$ with $p = 0.9$ the code keeps three tokens, while exact arithmetic keeps two. The difference is real but small; do not write tests that depend on an exact boundary in floats.
- **Ties at the boundary.** Equal probabilities at the last position make the nucleus depend on the tie rule. Fix it if outputs must be reproducible.
- **The order of the filters.** Temperature then top-p, top-p then temperature, and top-k then top-p all give different distributions, and libraries differ. State what you use.
- **A long flat tail.** On a very flat step the nucleus can hold thousands of tokens, and some of them are poor. A temperature below 1 or a top-k cap limits this.
- **Quality is measured, not proved.** The claim that nucleus sampling gives better text than top-k is a result of human and automatic evaluations on particular models.

## Implementations

The code takes the next-token probabilities (or logits) as given and implements the nucleus and the draw; it does not run or train a network.

## History

Holtzman, Buys, Du, Forbes and Choi posted "The curious case of neural text degeneration" on arXiv in 2019 and published it at ICLR 2020. They generated 5,000 passages of at most 200 tokens with GPT-2 Large, conditioned on prefixes of held-out web text, and compared the decoding methods with human text. Greedy decoding had 73.66% repeated text and beam search with $b = 16$ had 28.94%, against 0.28% for human text. Pure sampling had a perplexity of 22.73, far above the 12.38 of human text, because it drew too many tokens from the unreliable tail. Nucleus sampling with $p = 0.95$ had a perplexity of 13.13, repetition of 0.36% and the highest HUSE score in their Table 1, 0.97, a measure that combines human judgments of quality with the probability of the text under the model. The paper also named the problem of dull, repetitive and incoherent output "neural text degeneration" (see [inadequacy of the mode](/inadequacy-of-the-mode/)).

## References
