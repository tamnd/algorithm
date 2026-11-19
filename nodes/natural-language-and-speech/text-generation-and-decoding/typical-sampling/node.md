---
tag: T8X2CS
kind: algorithm
slug: typical-sampling
name: Typical sampling
aliases:
- locally typical sampling
area: natural-language-and-speech/text-generation-and-decoding
level: research
summary: "Keep the tokens whose surprisal is closest to the entropy of the next-token distribution, up to mass tau, and sample among them."
solves: [autoregressive-decoding]
model: real-ram
complexity:
  vars: {V: "the vocabulary size |V|"}
  time: {worst: "O(V log V)"}
  space: {extra: "O(V)"}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 2023
  people: [Clara Meister, Tiago Pimentel, Gian Wiher, Ryan Cotterell]
  note: Meister et al. posted locally typical sampling on arXiv in 2022 and published it in the Transactions of the ACL in 2023.
prereqs: [shannon-entropy, nucleus-sampling, autoregressive-decoding]
see_also: [nucleus-sampling, top-k-sampling, temperature-sampling, shannon-entropy, inadequacy-of-the-mode, perplexity, ancestral-sampling, language-model]
sources:
  - paper: doi:10.1162/tacl_a_00536
    title: "Clara Meister, Tiago Pimentel, Gian Wiher and Ryan Cotterell, Locally typical sampling, Transactions of the Association for Computational Linguistics 11, 2023, pages 102 to 121"
    locator: "Section 5 (local typicality and the algorithm: sort by the distance between surprisal and entropy, keep tokens until the mass reaches tau), Section 6.1 (tau = 0.2 for story generation and tau = 0.95 for summarization)"
  - url: https://arxiv.org/abs/2202.00666
    title: "Clara Meister, Tiago Pimentel, Gian Wiher and Ryan Cotterell, Locally typical sampling, arXiv 2202.00666, version 6"
    locator: "the erratum in footnote 18, which notes that the optimization problem of the paper and the greedy algorithm can give different sets"
  - url: https://arxiv.org/abs/1904.09751
    title: "Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes and Yejin Choi, The curious case of neural text degeneration, ICLR 2020"
    locator: "Section 3.1, nucleus sampling, the method that typical sampling changes by ordering the tokens by distance to the entropy"
---

Typical sampling, or locally typical sampling, generates text from an autoregressive [language model](/language-model/) one token at a time. At each step it computes the [entropy](/shannon-entropy/) $H$ of the next-token distribution, which is the expected surprisal of the next token. It then ranks the tokens by how far their surprisal $-\log p$ is from $H$, keeps the closest tokens until their total probability reaches a threshold $\tau$, renormalizes, and draws the next token. It works like [nucleus sampling](/nucleus-sampling/), but with a different order: nucleus sampling keeps the most probable tokens, while typical sampling keeps the tokens whose information content is close to the expected value. So it can drop the most probable token. Meister et al. 2023 motivated the rule by the idea that people choose words whose information content is close to what the listener expects. It is a heuristic for [autoregressive decoding](/autoregressive-decoding/), and its quality gains are measurements on a few models and tasks.

## In plain words

Every word that can come next has a surprise value: rare words are very surprising, common words are not. The model also has an average surprise for this step. Typical sampling keeps the words whose surprise is close to that average, not simply the most likely words. It adds them, closest first, until they hold a set share of the chance, and then draws one of them at random. When one word is far more likely than the rest, that word can be too unsurprising to keep. The idea is that good human text is neither too dull nor too strange.

## The problem

The model gives a distribution $p = p(\cdot \mid y_{<t})$ over the vocabulary $V$. Let $V^+$ be the tokens with $p_i > 0$. The entropy of the step is

$$H = -\sum_{i \in V^+} p_i \log p_i,$$

and the distance of a token $i \in V^+$ is $d_i = |-\log p_i - H|$. Sort $V^+$ by $d_i$, with the smaller index first on ties, and let $K$ be the shortest prefix whose mass is at least $\tau$. One step draws $y_t$ from $q(i) = p_i [i \in K] / \sum_{j \in K} p_j$. All logs here are natural logs; the paper uses bits, and the set $K$ does not depend on the base, because changing the base scales every distance by the same factor.

## The algorithm

The step takes $p$, the threshold $0 < \tau \le 1$, and a number $u$ drawn uniformly from $[0, 1)$.

```pseudo id=main
TYPICAL-SAMPLE(p, τ, u)               ▷ p = next-token distribution, u uniform in [0, 1)
L1  H ← − Σ p[i] log p[i] over the tokens with p[i] > 0
L2  for each token i with p[i] > 0 do d[i] ← |−log p[i] − H|
L3  order ← these tokens sorted by d, smallest first   ▷ ties: the smaller index first
L4  c ← 0,  K ← empty list
L5  for each i in order do  c ← c + p[i],  append i to K
L6      if c ≥ τ then stop the loop
L7  Z ← c,  r ← u · Z
L8  c ← 0;  for each i in K, in order do
L9      c ← c + p[i]
L10     if r < c then return i
L11 return the last i in K             ▷ only after rounding
```

Lines L4 to L11 are those of nucleus sampling; only the order of line L3 is new.

## Example

Take six next tokens with $p$ = (the 0.40, a 0.25, cat 0.15, dog 0.10, sat 0.06, ran 0.04). The entropy is $H = 1.5255$ nats (2.2008 bits).

| token | $p$ | surprisal $-\log p$ | distance $d$ |
|---|---|---|---|
| the | 0.40 | 0.9163 | 0.6092 |
| a | 0.25 | 1.3863 | 0.1392 |
| cat | 0.15 | 1.8971 | 0.3716 |
| dog | 0.10 | 2.3026 | 0.7771 |
| sat | 0.06 | 2.8134 | 1.2879 |
| ran | 0.04 | 3.2189 | 1.6934 |

The order by distance is a, cat, the, dog, sat, ran, with running masses 0.25, 0.40, 0.80, 0.90, 0.96 and 1.

| $\tau$ | kept | mass | renormalized |
|---|---|---|---|
| 0.2 | a | 0.25 | a 1 |
| 0.5 | a, cat, the | 0.80 | a 0.3125, cat 0.1875, the 0.5 |
| 0.9 | a, cat, the, dog | 0.90 | a 0.2778, cat 0.1667, the 0.4444, dog 0.1111 |
| 0.95 | the first five | 0.96 | a 0.2604, cat 0.15625, the 0.4167, dog 0.1042, sat 0.0625 |

With $\tau = 0.2$ the step returns "a" for sure, although "the" is more probable: the surprisal of "the" is too far below the entropy. With $\tau = 0.5$ the kept set is the same as the nucleus for $p = 0.8$, but it is reached in a different order. For large $\tau$, typical sampling and nucleus sampling keep almost the same tokens, because the order matters only at the boundary.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that the kept set is the shortest prefix of the distance order with mass at least $\tau$, that every kept token is at least as close to the entropy as every dropped token, that the set does not depend on the log base, and that the step draws each kept token with probability $p_i / Z$. It also shows that the greedy prefix is not always a solution of the optimization problem in the paper (minimize the total distance subject to mass at least $\tau$): for $p = (0.4, 0.3, 0.2, 0.1)$ and $\tau = 0.35$, the greedy set holds the tokens of probability 0.3 and 0.2, with total distance 0.4055, while the token of probability 0.4 alone has mass 0.4 and distance 0.3636. The tests check these facts against all subsets on small distributions.

## Complexity

One step computes the entropy in $O(|V|)$, the distances in $O(|V|)$, and sorts in $O(|V| \log |V|)$. The prefix sums and the draw are $O(|V|)$. As with nucleus sampling, the size of the kept set is not known in advance, so a selection by mass around a pivot gives expected $O(|V|)$ plus the sort of the kept tokens. The extra space is $O(|V|)$. Meister et al. note that the cost is the same as that of nucleus and top-k sampling, and the call of the network costs far more.

## Properties

- **Randomized.** Fix the seed to reproduce an output.
- **Closest to the entropy.** Every kept token has a surprisal at least as close to $H$ as every dropped token.
- **Can drop the most probable token.** When the largest probability is far above the others, its surprisal is far below $H$. So there is no greedy limit: a small $\tau$ keeps the single token closest to $H$, not the most probable one.
- **Uniform steps.** On a uniform distribution every distance is 0 and every token is equally typical; the tie rule decides the set, and the renormalized distribution is uniform on it.
- **Limit.** $\tau = 1$ keeps every token of positive probability and gives [ancestral sampling](/ancestral-sampling/).
- **Base free.** The set is the same in nats and in bits.

## Variants and improvements

- **With temperature or top-k.** As with nucleus sampling, a temperature can be applied to the logits first, and the kept set can be capped at $k$ tokens.
- **Nucleus sampling.** The same prefix rule with the tokens ordered by probability ([nucleus sampling](/nucleus-sampling/)).
- **The optimization form.** Solving the stated problem exactly (a knapsack-like choice of tokens of minimum total distance and mass at least $\tau$) gives a different set from the greedy rule in some cases. No standard implementation does this; the greedy rule is the method in use.
- **Contrastive search.** A deterministic method that fights repetition with a similarity penalty in place of an entropy rule ([contrastive search](/contrastive-search/)).

## When to use it

Use typical sampling for open-ended generation when nucleus sampling still gives dull or repetitive text, since it can skip the most predictable token. Meister et al. found $\tau = 0.2$ best for story generation with GPT-2 on WritingPrompts and $\tau = 0.95$ for abstractive summarization with BART on CNN/DailyMail, tuned with automatic measures and checked with human ratings. Tune $\tau$ for your own model and task. For tasks with one correct answer, use greedy decoding or beam search.

## Pitfalls

- **Small $\tau$ is not greedy.** People coming from nucleus sampling expect a small threshold to give safe text; here it can give the less probable token.
- **Ties of distance.** A token above the entropy and a token below it can be equally far from it, for example $1/4$ and $1/2$ in $(1/4, 1/4, 1/2)$, where $H = 1.5$ bits and both distances are 0.5 bits. The order between them then depends on rounding.
- **The formula and the algorithm differ.** Code the greedy prefix, not the optimization problem as written in the paper, unless you want a different method.
- **Tokens of probability 0.** Their surprisal is infinite. Leave them out before the sort, or the distance computation fails.
- **Rounding at the threshold.** As with nucleus sampling, a float sum can stop just below $\tau$; with $\tau = 1$ that can keep every positive token, which is the intended result.

## Implementations

The code takes the next-token probabilities (or logits) as given and implements the entropy, the order, the kept set and the draw; it does not run or train a network.

## History

Meister, Pimentel, Wiher and Cotterell posted "Locally typical sampling" on arXiv in February 2022 and published it in the Transactions of the ACL in 2023. They argued, from psycholinguistic work on uniform information density, that human text keeps the information of each word close to its expected value, and that the most probable strings of a model, which have low information, are therefore atypical (see [inadequacy of the mode](/inadequacy-of-the-mode/)). A later arXiv version adds an erratum that the optimization formulation can exclude the tokens closest to the entropy and does not match the greedy algorithm, which is the method that the experiments use.

## References
