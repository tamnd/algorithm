---
tag: K6SZXR
kind: algorithm
slug: diverse-beam-search
name: Diverse beam search
aliases:
- grouped diverse beam search
area: natural-language-and-speech/text-generation-and-decoding
level: advanced
summary: Split the beam into groups and penalize each group for tokens chosen by earlier groups at the same step, to return a varied list.
solves: [autoregressive-decoding]
model: word-ram
complexity:
  vars: {n: the number of steps, G: the number of groups, B: "the total beam width G times B'", V: "the vocabulary size |V|", C: the cost of one call of the model}
  time: {worst: "O(n B (C + V))"}
  space: {extra: "O(n B + G V)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Ashwin K. Vijayakumar, Michael Cogswell, Ramprasaath R. Selvaraju, Qing Sun, Stefan Lee, David Crandall, Dhruv Batra]
  note: The method was posted on arXiv in 2016 (1610.02424) and published at AAAI 2018.
prereqs: [beam-search, autoregressive-decoding, hamming-distance]
see_also: [greedy-decoding, stochastic-beam-search, minimum-bayes-risk-decoding, maximal-marginal-relevance, nucleus-sampling, top-k-selection, self-consistency-decoding, inadequacy-of-the-mode]
sources:
  - paper: doi:10.1609/aaai.v32i1.12340
    title: Ashwin K. Vijayakumar, Michael Cogswell, Ramprasaath R. Selvaraju, Qing Sun, Stefan Lee, David Crandall and Dhruv Batra, Diverse beam search for improved description of complex scenes, AAAI 2018, pages 7371 to 7379
    locator: the doubly greedy group by group search, the Hamming diversity term, and the choice of the diversity strength by grid search on held out data
  - url: https://arxiv.org/abs/1610.02424
    title: Ashwin K. Vijayakumar et al., Diverse beam search, decoding diverse solutions from neural sequence models, arXiv 1610.02424, 2016
    locator: the first version of the method
---

Diverse beam search returns a list of outputs that differ from each other, from one autoregressive model. A plain [beam search](/beam-search/) of width $B$ often returns $B$ outputs that differ only in a word or two near the end. Diverse beam search splits the $B$ slots into $G$ groups of $B' = B / G$. The groups advance one after the other at each step, and each group subtracts a penalty $\lambda$ for every time an earlier group chose the same token at this step. The first group is a plain beam search, so the method keeps its best output; the later groups trade a little probability for variety. Like beam search, it is a heuristic: it does not find the most probable outputs, and it gives no guarantee on how different they are.

## In plain words

Plain beam search keeps a few good partial texts and grows them together. They tend to copy each other, so the final list says nearly the same thing several times. Diverse beam search makes small teams. The first team works as usual. Each later team must pay a fee to pick a word that an earlier team picked at the same step. A team then picks a different word when the fee is larger than what it loses. At the end you get one or more texts from each team, and the teams went different ways.

## The problem

The model gives $\log p(w \mid y)$ for every prefix $y$ and every token $w$ of the vocabulary $V$, which contains `</s>`. The score of a prefix is the sum of its token log probabilities; all logs are natural logs. The task is to return a short list of finished outputs, ending with `</s>`, that are probable under the model and not near copies of each other. No single objective defines "diverse", so the method fixes one: at step $t$, group $g$ maximizes

$$\sum_{y \in \text{beam}_g} \Big( s(y) - \lambda \sum_{h < g} \big|\{ y' \in \text{beam}_h : y'_t = y_t \}\big| \Big),$$

where $s(y)$ is the log probability of $y$ and the inner count is the number of times the earlier groups chose the same token $y_t$ at this step. Vijayakumar et al. call this count the Hamming diversity, because it is the number of positions where the new token agrees with the tokens of the earlier groups at the same position (see [Hamming distance](/hamming-distance/)). The diversity term acts on the ranking only; each output keeps its true log probability.

## The algorithm

```pseudo id=main
DIVERSE-BEAM-SEARCH(model, N, G, B', λ)
L1  beam_g ← { empty prefix with score 0 } for g = 1 .. G;  F ← empty list
L2  for t ← 1 to N do
L3      used ← an empty count of tokens            ▷ the tokens chosen at step t so far
L4      for g ← 1 to G do
L5          for each (y, s) in beam_g, for each w with log p(w | y) > -∞ do
L6              candidate (y w) with rank r = s + log p(w | y) - λ · used[w] and score s + log p(w | y)
L7          keep the B' candidates with the largest r     ▷ ties: the first generated
L8          for each kept candidate y w: used[w] ← used[w] + 1
L9          a kept candidate that ends with "</s>" goes to F with its score and g; the others form the new beam_g
        if every beam is empty then stop
L10 return F sorted by score, best first
```

A candidate that ends with `</s>` uses one of the $B'$ slots of its group at the step it finishes, and then leaves the beam. So a group can shrink. This is one of several conventions for finished hypotheses in beam search; the code and the tests use it for both plain and diverse beam search.

## Example

Take the model M1 of [greedy decoding](/greedy-decoding/): at the empty prefix $p(a) = 0.5$, $p(b) = 0.4$, $p(\text{</s>}) = 0.1$; after a, $0.4, 0.3, 0.3$; after b, $0.05, 0.05, 0.9$; after two tokens, `</s>` has probability 1. Its most probable output is b`</s>` (0.36), and greedy decoding returns aa`</s>` (0.2). Run diverse beam search with $G = 2$ groups of $B' = 1$ and $\lambda = 0.5$.

| step | group | candidates, rank (score) | kept |
|---|---|---|---|
| 1 | 1 | a $-0.693$, b $-0.916$, `</s>` $-2.303$ | a |
| 1 | 2 | a $-1.193$ ($-0.693$), b $-0.916$, `</s>` $-2.303$ | b |
| 2 | 1 | aa $-1.609$, ab $-1.897$, a`</s>` $-1.897$ | aa |
| 2 | 2 | ba $-3.912$, bb $-3.912$, b`</s>` $-1.022$ | b`</s>`, finished |
| 3 | 1 | aa`</s>` $-1.609$ | aa`</s>`, finished |

At step 1, group 1 chose a, so group 2 pays 0.5 for a and chooses b. At step 2 nobody has chosen `</s>` before group 2, so b`</s>` pays nothing. The result is b`</s>` ($\log 0.36 = -1.022$, group 2) and aa`</s>` ($\log 0.2 = -1.609$, group 1): two different outputs, and one of them is the mode.

With $\lambda = 0.2$, group 2 ranks a at $-0.893$ above b at $-0.916$, follows group 1, and the result is aa`</s>` twice. Here diverse beam search misses the mode and returns no variety at all. The switch happens at $\lambda = \ln(0.5 / 0.4) = 0.2231$, the gap between a and b at the first step. The test checks both sides.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It proves three theorems. First, the first group is exactly a beam search of width $B'$, because the count `used` is empty when it runs; so its best output is the output of that beam search. Second, with $\lambda = 0$ every group repeats the first group, so the list holds $G$ copies of each output. Third, a group never chooses a candidate whose rank is beaten by $B'$ other candidates; in particular, when $\lambda \cdot c$ is larger than the score gap between a token used $c$ times and an unused token, the group prefers the unused one.

These are statements about the search, not about quality. Diverse beam search is not exact: the M1 example with $\lambda = 0.2$ misses the mode, and the tests compare the output with exhaustive search. With $B'$ at least the number of prefixes of the model, the first group keeps every prefix and finds the best output; the test checks this on small random models.

## Complexity

At each step, group $g$ makes one call of the model for each of its at most $B'$ prefixes, and forms at most $B' |V|$ candidates. The penalty of a candidate is one lookup in a [hash table](/hash-table/) of counts. Over all groups this is $B$ calls and $B |V|$ candidates per step, as for a plain beam of width $B$. Selecting the $B'$ best of $B' |V|$ ranks takes $O(B' |V|)$ time with linear [top-k selection](/top-k-selection/), or $O(B' |V| \log B')$ with a heap; the code sorts, for clarity. Over $n$ steps the time is $O(n B (C + |V|))$ with linear selection. The beams and the finished list take $O(n B)$ tokens, and the candidates of one group $O(B' |V|)$.

The groups at one step run one after the other, because group $g$ needs the choices of groups $1 .. g - 1$. Plain beam search can run all $B$ prefixes in one batch; diverse beam search can batch within a group only. This is a cost in wall time on parallel hardware, not in the operation count.

## Properties

- **The first group is plain beam search** (a theorem). Its output is the output of a beam search of width $B'$, so diverse beam search does not lose that output.
- **Not exact** (a theorem by the example). Neither the mode nor the $B$ most probable outputs are guaranteed.
- **Deterministic.** Given the tie rule, the output is fixed.
- **True scores.** The penalty changes the ranking during search; the returned scores are the true log probabilities.
- **More variety** (a measurement). Vijayakumar et al. measured more distinct n-grams and higher oracle scores on image captioning and other tasks than plain beam search at the same width.

## Variants and improvements

- **Other diversity terms.** The paper also studies n-gram diversity, which penalizes repeated n-grams, and neural embedding diversity; the Hamming term is the cheapest and the one most toolkits ship.
- **Penalties within a group.** A penalty on siblings, children of the same parent, spreads the beam of one group over more parents.
- **Sampling.** [Stochastic beam search](/stochastic-beam-search/) draws $k$ distinct outputs without replacement exactly from the model, and [nucleus sampling](/nucleus-sampling/) draws independent varied outputs. Both give diversity with a probabilistic meaning in place of a penalty.
- **Rerank the list.** The varied list is a good candidate set for [minimum Bayes risk decoding](/minimum-bayes-risk-decoding/) or [maximal marginal relevance](/maximal-marginal-relevance/).

## When to use it

Use diverse beam search when you need several different outputs from a deterministic search, for example caption or reply suggestions, a candidate list for a reranker, or [self-consistency decoding](/self-consistency-decoding/) with a search in place of sampling. If one output is needed, use plain beam search, since the extra groups only cost time. If the outputs must be a fair sample of the model, use sampling or stochastic beam search.

## Pitfalls

- **The strength λ.** Too small, and the groups copy each other (the M1 example at $\lambda = 0.2$); too large, and the later groups choose improbable tokens. Vijayakumar et al. chose $\lambda$ by a grid search on held out data, for oracle accuracy, over values from 0.2 to 0.8. Tune it on your task.
- **Same token, different place.** The Hamming term compares tokens at the same step only. Two outputs can say the same thing shifted by one word and pay no penalty.
- **Group order.** The first group never pays and the last group pays the most. The list is not symmetric across groups, and the later groups have lower scores by design.
- **Finished outputs.** As in beam search, decide how finished outputs leave the beam and how lengths are compared ([length normalization](/length-normalization/)); a group can end early with only short outputs.

## Implementations

The code takes the log probabilities of the model as given, as a function of the prefix, and implements the search around them; it does not run or train a network.

## History

Vijayakumar, Cogswell, Selvaraju, Sun, Lee, Crandall and Batra posted diverse beam search on arXiv in 2016 and published it at AAAI 2018, with experiments on image captioning, machine translation and visual question generation. They described it as doubly greedy: greedy over time, as beam search is, and greedy over groups, since each group fixes its choice before the next one runs.

## References
