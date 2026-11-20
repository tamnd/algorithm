---
tag: CNGCHZ
kind: algorithm
slug: top-k-sampling
name: Top-k sampling
aliases:
- truncated sampling
area: natural-language-and-speech/text-generation-and-decoding
level: core
summary: "Keep only the k most probable next tokens, renormalize their probabilities and sample from them."
solves: [autoregressive-decoding]
model: real-ram
complexity:
  vars: {V: "the vocabulary size |V|", k: the number of kept tokens}
  time: {worst: "O(V + k log k)"}
  space: {extra: "O(V)"}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 2018
  people: [Angela Fan, Mike Lewis, Yann Dauphin]
  note: "Fan, Lewis and Dauphin sampled from the 10 most likely candidates to generate stories, in place of beam search."
prereqs: [autoregressive-decoding, language-model, top-k-selection]
see_also: [nucleus-sampling, temperature-sampling, typical-sampling, greedy-decoding, ancestral-sampling, contrastive-search, inverse-transform-sampling, beam-search]
sources:
  - paper: doi:10.18653/v1/P18-1082
    title: "Angela Fan, Mike Lewis and Yann Dauphin, Hierarchical neural story generation, ACL 2018, pages 889 to 898"
    locator: "Section 5.4 (Generation), top-k random sampling from the k = 10 most likely candidates, and the note that beam search gives common phrases and repetitive text"
  - url: https://arxiv.org/abs/1904.09751
    title: "Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes and Yejin Choi, The curious case of neural text degeneration, ICLR 2020"
    locator: "Section 3.2 (top-k sampling as the size-k set of largest mass) and Table 1 (top-k = 40 and top-k = 640 against nucleus sampling on GPT-2 Large)"
---

Top-k sampling generates text from an autoregressive [language model](/language-model/) one token at a time. At each step it keeps the $k$ most probable next tokens, sets the probability of every other token to 0, divides the kept probabilities by their sum, and draws the next token from that distribution. With $k = 1$ it is [greedy decoding](/greedy-decoding/); with $k = |V|$ it is plain [ancestral sampling](/ancestral-sampling/) from the model. It is a heuristic method for [autoregressive decoding](/autoregressive-decoding/): it does not look for the most probable text, and it does not sample from the model either. It cuts off the long tail of unlikely tokens, where a single bad draw can derail the text, and keeps the variety of sampling among the likely tokens. The value of $k$ is a setting that people tune by hand.

## In plain words

The model gives a chance to every word that can come next. Most of these words are bad choices, but together they can hold a real share of the chance, so a plain random draw picks one of them now and then. Top-k sampling keeps only the best k words, for example the best 40. It forgets the others and draws at random among the kept ones, in proportion to their chances. Then it adds the word and repeats. A small k gives safe, plain text. A large k gives more varied text with more risk.

## The problem

The model gives a distribution $p = p(\cdot \mid y_{<t})$ over the vocabulary $V$ for the prefix $y_{<t}$. Number the tokens $0, \ldots, |V| - 1$. The task of one step is to choose $y_t$ at random. Top-k sampling draws $y_t$ from the truncated distribution

$$q_k(i) = \frac{p_i \, [i \in K]}{\sum_{j \in K} p_j},$$

where $K$ is a set of $\min(k, |V|)$ tokens of largest probability. On ties at the boundary, the tokens with smaller indices are kept. The whole output is built by repeating the step until the end token `</s>` or a length limit, as in greedy decoding. The output distribution is not the model distribution $p(y)$, and no single sequence is the target; the method is defined by the rule itself.

## The algorithm

The step takes $p$ and a number $u$ drawn uniformly from $[0, 1)$. In practice $p$ comes from the logits $z$ by a softmax, often with a temperature $T$ ([temperature sampling](/temperature-sampling/)); since dividing by $T > 0$ keeps the order of the logits, $K$ is the same for every $T$.

```pseudo id=main
TOP-K-SAMPLE(p, k, u)                 ▷ p = next-token distribution, u uniform in [0, 1)
L1  order ← the tokens sorted by p, from high to low   ▷ ties: the smaller index first
L2  K ← the first min(k, |V|) tokens of order
L3  Z ← sum of p[i] over i in K
L4  r ← u · Z
L5  c ← 0
L6  for each i in K, in the order of L1 do
L7      c ← c + p[i]
L8      if r < c then return i
L9  return the last i in K with p[i] > 0   ▷ only if u · Z rounded up to Z
```

Lines L4 to L8 are [inverse transform sampling](/inverse-transform-sampling/) on the kept tokens. The bound $Z$ multiplies $u$, so the renormalized distribution is never written down and nothing is divided. A token of probability 0 has an empty interval and is never returned.

## Example

Take six next tokens with $p$ = (the 0.40, a 0.25, cat 0.15, dog 0.10, sat 0.06, ran 0.04). They are already sorted.

| $k$ | kept | $Z$ | renormalized |
|---|---|---|---|
| 1 | the | 0.40 | the 1 |
| 2 | the, a | 0.65 | the 8/13 = 0.6154, a 5/13 = 0.3846 |
| 3 | the, a, cat | 0.80 | the 1/2, a 5/16 = 0.3125, cat 3/16 = 0.1875 |
| 6 | all | 1 | $p$ itself |

With $k = 3$ and $u = 0.6$, line L4 gives $r = 0.48$. The running sum is 0.40 after "the", which is not above 0.48, and 0.65 after "a", which is. So the step returns "a". In terms of $u$, the token "the" wins for $u < 0.5$, "a" for $0.5 \le u < 0.8125$, and "cat" for $u \ge 0.8125$.

The weak point shows with $k = 3$ on two other steps. On a peaked step, $p$ = (0.90, 0.05, 0.03, 0.02), top-3 still keeps a token of probability 0.03 and gives it $0.03 / 0.98 = 0.0306$. On a flat step with ten tokens of 0.1 each, top-3 drops 70% of the mass and keeps three tokens that are no better than the other seven. A fixed $k$ is too large for the first step and too small for the second; [nucleus sampling](/nucleus-sampling/) adapts the size of the set to the shape of $p$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that the kept set has the largest total probability of all sets of $\min(k, |V|)$ tokens, by an exchange argument, and that the step returns each kept token $i$ with probability exactly $p_i / Z$ and never returns a dropped token or a token of probability 0. The special cases follow: $k = 1$ returns the first most probable token, and $k \ge |V|$ samples from $p$. The tests check the maximum mass against all subsets on random distributions, and check the draw exactly with Fraction probabilities and $u$ on a fine grid.

## Complexity

One step reads $|V|$ probabilities. A full sort costs $O(|V| \log |V|)$. Only the $k$ largest are needed, in order: a [selection](/top-k-selection/) in linear time followed by a sort of the $k$ kept values costs $O(|V| + k \log k)$, and a min-[heap](/heap/) of size $k$ costs $O(|V| \log k)$. The draw itself is $O(k)$. The extra space is $O(|V|)$ for the scores, or $O(k)$ beyond them with the heap. On a GPU, frameworks use a parallel top-k kernel. For a large model the call of the network costs far more than any of this.

## Properties

- **Randomized.** The same prefix can give different tokens. Fix the seed of the random source to reproduce an output.
- **Not the model distribution.** For $k < |V|$ the output distribution differs from $p(y)$. Tokens outside the top $k$ at some step can never appear there.
- **Maximum mass for its size.** The kept set holds the most probability of any set of $\min(k, |V|)$ tokens.
- **Order only.** The kept set depends only on the order of the probabilities, so it is the same for every temperature and for the logits or the probabilities.
- **Limits.** $k = 1$ is greedy decoding, and $k = |V|$ is ancestral sampling.
- **Online.** Each token is final when it is drawn.

## Variants and improvements

- **Top-k with temperature.** Apply the temperature to the logits, then truncate. Holtzman et al. 2020 report top-k = 40 with $T = 0.7$ as one of their baselines.
- **Nucleus sampling.** Keep the smallest set whose mass reaches $p$ in place of a fixed count ([nucleus sampling](/nucleus-sampling/)). Libraries often apply both: first top-k, then top-p.
- **Typical sampling.** Keep the tokens whose surprisal is closest to the entropy of the step ([typical sampling](/typical-sampling/)).
- **Contrastive search.** Take the top $k$ candidates, but choose among them by a score with a penalty for similarity to the context, without randomness ([contrastive search](/contrastive-search/)).
- **Gumbel top-k.** Adding Gumbel noise to the log probabilities and taking the $k$ largest draws $k$ tokens without replacement ([Gumbel-max trick](/gumbel-max-trick/), [stochastic beam search](/stochastic-beam-search/)). This draws several tokens at once; it is not the same as top-k sampling.

## When to use it

Use top-k sampling for open-ended text, such as stories and dialogue, where varied output is wanted and the most probable text tends to be dull and repetitive. A value of $k$ between 10 and 100 is common. Prefer nucleus sampling when the shape of the distribution changes a lot from step to step, which is the usual case. Use greedy decoding or beam search when a single correct answer is wanted, as in translation or short factual answers.

## Pitfalls

- **One $k$ for all steps.** The same $k$ keeps bad tokens on peaked steps and drops good ones on flat steps (the example above).
- **Ties at the boundary.** With equal probabilities at position $k$, the kept set depends on the tie rule. Fix it if outputs must be reproducible.
- **Order of the filters.** Top-k then top-p is not the same as top-p then top-k with renormalization in between, and libraries differ. State the order.
- **Temperature does not change the set.** People sometimes expect a high temperature to let more tokens in; with top-k it only changes the weights inside the fixed set.
- **Repetition is not fixed.** Truncation lowers the chance of bad tokens but does not stop loops; a [repetition penalty](/repetition-penalty/) is a separate tool.

## Implementations

The code takes the next-token probabilities (or logits) as given and implements the truncation and the draw; it does not run or train a network.

## History

Fan, Lewis and Dauphin 2018 used top-k random sampling with $k = 10$ to generate stories on their WritingPrompts dataset, because beam search tended to produce common phrases and repetitive text. Top-k sampling then became a standard way to generate text with large language models. Holtzman et al. 2020 measured its weak point, the fixed size of the set, and proposed [nucleus sampling](/nucleus-sampling/), which adapts the size to the distribution.

## References
