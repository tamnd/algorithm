---
tag: G3YHYE
kind: algorithm
slug: stochastic-beam-search
name: Stochastic beam search
aliases:
- Gumbel-top-k beam search
area: natural-language-and-speech/text-generation-and-decoding
level: research
summary: Beam search on Gumbel-perturbed log-probabilities that draws k sequences without replacement exactly from a sequence model.
solves: [autoregressive-decoding]
model: word-ram
complexity:
  vars: {n: the most output tokens, k: the beam width and the number of samples, V: "the vocabulary size |V|", M: the cost of one call of the model}
  time: {worst: "O(n k (M + V))"}
  space: {extra: "O(n k + k V)"}
properties: {deterministic: false, exact: true, online: false, recursive: false}
history:
  year: 2019
  people: [Wouter Kool, Herke van Hoof, Max Welling]
  note: Kool, van Hoof and Welling extended the Gumbel-top-k trick from a flat list to the tree of a sequence model at ICML 2019.
prereqs: [beam-search, gumbel-max-trick, autoregressive-decoding]
see_also: [weighted-reservoir-sampling, diverse-beam-search, ancestral-sampling, temperature-sampling, minimum-bayes-risk-decoding, top-k-selection, log-sum-exp-trick, importance-sampling]
sources:
  - url: https://proceedings.mlr.press/v97/kool19a.html
    title: Wouter Kool, Herke van Hoof and Max Welling, Stochastic beams and where to find them, the Gumbel-top-k trick for sampling sequences without replacement, ICML 2019, PMLR 97, pages 3499 to 3508
    locator: "the Gumbel-top-k trick, the top-down sampling of perturbed log probabilities with truncated Gumbels, Algorithm 1 (stochastic beam search), and Appendix B (the numerically stable form of the truncation)"
---

Stochastic beam search draws $k$ different outputs from an autoregressive model, as if you drew one output, removed it, renormalized, and drew again, $k$ times. It does this exactly, with one beam search of width $k$ and no rejection. The idea is the [Gumbel-max trick](/gumbel-max-trick/) applied to every complete output at once: add an independent Gumbel noise to the log probability of each output, and the $k$ outputs with the largest perturbed values are a sample without replacement. There are too many outputs to perturb one by one, so the method samples the perturbed values top down, from the root of the tree of prefixes, and a [beam search](/beam-search/) on those values finds the $k$ largest. Kool, van Hoof and Welling introduced it in 2019.

## In plain words

Think of all possible texts as the leaves of a tree, where each branch adds one word. Give each text a random ticket: its log probability plus some noise of a special kind. The texts with the $k$ best tickets are a fair draw of $k$ different texts. You cannot write a ticket for every text, but you do not need to. The best ticket below a branch has a known random law, so you can draw it for the branch first and then split it among the children so that they agree with it. Then keep the $k$ branches with the best tickets at each level, as a beam search does. The best ticket of a kept text can never lose to a dropped branch.

## The problem

The model gives $\log p(w \mid y)$ for every prefix $y$ and token $w$ of the vocabulary $V$, which contains `</s>`; all logs are natural logs. Every output ends with `</s>` within $n$ tokens. A sample of $k$ outputs without replacement is a sequence $y^{(1)}, \ldots, y^{(k)}$ of distinct outputs with probability

$$P\big(y^{(1)}, \ldots, y^{(k)}\big) = \prod_{i=1}^{k} \frac{p(y^{(i)})}{1 - \sum_{j < i} p(y^{(j)})}.$$

The task is to draw from this law with a cost close to that of a beam search of width $k$. If the model has fewer than $k$ outputs, the sample is all of them.

A random variable $G$ has the Gumbel law with location $\phi$, written $G \sim \text{Gumbel}(\phi)$, if $P(G \le x) = \exp(-\exp(\phi - x))$. Draw it as $\phi - \log(-\log U)$ with $U$ uniform on $(0, 1)$. Three facts are used, and the proof file proves them. If $G_i \sim \text{Gumbel}(\phi_i)$ are independent, then $\max_i G_i \sim \text{Gumbel}(\log \sum_i e^{\phi_i})$ (max-stability). The argmax is $i$ with probability $e^{\phi_i} / \sum_j e^{\phi_j}$ (the Gumbel-max trick). And the indices of the $k$ largest $G_i$, in order, are a sample of $k$ without replacement from that distribution (the Gumbel-top-k trick).

## The algorithm

For a prefix $y$, let $\phi_y = \log p(y)$, the sum of the token log probabilities; for a finished output it is the log probability of the output. The perturbed value of a prefix is $G_y$, the largest perturbed value of the outputs below it. The root has $\phi = 0$ and, by convention, $G = 0$; a constant shift of all values does not change their order.

```pseudo id=main
STOCHASTIC-BEAM-SEARCH(model, n, k, rng)
L1  beam ← { (empty prefix, φ = 0, G = 0) }
L2  for t ← 1 to n do                               ▷ stop early when every node of the beam is finished
L3      C ← empty list
L4      for each node (y, φ_y, G_y) in the beam do   ▷ a finished node goes to C unchanged
L5          children y w with φ_{yw} = φ_y + log p(w | y), for each w with p(w | y) > 0
L6          draw g_w ~ Gumbel(φ_{yw}) independently;  Z ← max over w of g_w
L7          G_{yw} ← -log( exp(-G_y) - exp(-Z) + exp(-g_w) )   ▷ stable form below
L8      sort C by G, largest first                     ▷ ties: the first generated
L9      beam ← the first k nodes of C
L10 return the finished nodes of the beam, in order of G
```

Line L7 is the truncation: it maps the independent Gumbels $g_w$ to values whose maximum is exactly $G_y$, keeping their order. Computed as written, $\exp(-G)$ overflows or loses all its digits. The code uses the stable form of Kool et al. (Appendix B): with $v = G_y - g_w + \log(1 - \exp(g_w - Z))$,

$$G_{yw} = G_y - \log(1 + e^{v}) = G_y - \max(0, v) - \log(1 + e^{-|v|}),$$

where $\log(1 - e^{a})$ for $a \le 0$ is computed with expm1 for $a > -\ln 2$ and with log1p otherwise, the usual way to keep the digits (see the [log-sum-exp trick](/log-sum-exp-trick/)).

## Example

Take the model M1 of [greedy decoding](/greedy-decoding/): at the empty prefix $p(a) = 0.5$, $p(b) = 0.4$, $p(\text{</s>}) = 0.1$; after a, $0.4, 0.3, 0.3$; after b, $0.05, 0.05, 0.9$; after two tokens, `</s>` has probability 1. Its seven outputs and their probabilities are `</s>` 0.1, a`</s>` 0.15, aa`</s>` 0.2, ab`</s>` 0.15, b`</s>` 0.36, ba`</s>` 0.02 and bb`</s>` 0.02. Run $k = 2$ with random.Random(3).

| step | parent ($G$) | child | $\phi$ | Gumbel $g$ | $G$ after line L7 |
|---|---|---|---|---|---|
| 1 | root (0) | a | $-0.693$ | $-1.055$ | $-0.855$ |
| 1 | root (0) | b | $-0.916$ | $-0.419$ | $0.000$ |
| 1 | root (0) | `</s>` | $-2.303$ | $-2.297$ | $-2.243$ |
| 2 | b (0) | ba | $-3.912$ | $-3.227$ | $-2.926$ |
| 2 | b (0) | bb | $-3.912$ | $-3.155$ | $-2.826$ |
| 2 | b (0) | b`</s>` | $-1.022$ | $-2.024$ | $0.000$ |
| 2 | a ($-0.855$) | aa | $-1.609$ | $-3.075$ | $-3.128$ |
| 2 | a ($-0.855$) | ab | $-1.897$ | $-0.168$ | $-0.855$ |
| 2 | a ($-0.855$) | a`</s>` | $-1.897$ | $-2.197$ | $-2.319$ |

At step 1 the largest Gumbel, b's, is shifted to the root's value 0, and the others move with it; the beam keeps b (0) and a ($-0.855$). At step 2 each parent's largest child takes the parent's value: b`</s>` gets 0 and ab gets $-0.855$. The beam keeps b`</s>` (finished) and ab. At step 3 ab gets its only child ab`</s>`, with $G = -0.855$. The sample is b`</s>`, then ab`</s>`.

For this model, the exact probability that the ordered sample is (b`</s>`, aa`</s>`) is $0.36 \cdot 0.2 / 0.64 = 0.1125$, and the probability of the set {b`</s>`, aa`</s>`} is $0.1125 + 0.2 \cdot 0.36 / 0.8 = 0.2025$. The tests draw 20000 samples of size 1 and 2 and compare the frequencies with these exact values, with a tolerance of 0.01, and 10000 samples of size 3 on a random model with a tolerance of 0.015.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It has four steps. First, the Gumbel-top-k trick on a flat list, proved with exponential races. Second, the truncation lemma: if $g_w$ are independent Gumbels with maximum $Z$, then the values of line L7 have the law of independent $\text{Gumbel}(\phi_{yw})$ variables conditioned on their maximum being $G_y$. Third, by induction down the tree, the values that the algorithm draws for any set of nodes have the same joint law as the maxima of independent Gumbel perturbations of all outputs. Fourth, the beam never drops an ancestor of one of the $k$ largest outputs: if it did, $k$ other nodes at that depth would each have an output below them with a larger value. So the returned outputs are the $k$ largest perturbed outputs, and by the first step they are an exact sample without replacement.

This is a theorem about the algorithm with exact real arithmetic and exact Gumbel draws. The code uses floating point; the tests check the sampling frequencies, and check that the shift keeps the order and puts the maximum exactly on the parent's value.

## Complexity

Each step expands at most $k$ nodes. Each expansion makes one model call and draws and shifts at most $|V|$ Gumbels. Selecting the $k$ largest of at most $k |V|$ candidates takes $O(k |V|)$ time with [top-k selection](/top-k-selection/); the code sorts, for clarity. Over $n$ steps the time is $O(n k (M + |V|))$, the same order as a [beam search](/beam-search/) of width $k$. The beam holds $k$ prefixes of at most $n$ tokens, and the candidates of one step take $O(k |V|)$ space.

Compare drawing $k$ distinct outputs by repeated [ancestral sampling](/ancestral-sampling/) and throwing away repeats. When a few outputs hold most of the probability, almost every new draw is a repeat, and the number of draws needed has no bound in terms of $k$. Stochastic beam search always makes $n k$ calls at most.

## Properties

- **Exact sampling without replacement** (a theorem), in the order of the draws.
- **Width 1 is ancestral sampling.** With $k = 1$ each step keeps the child with the largest value, which by the Gumbel-max trick is a draw from $p(w \mid y)$.
- **No repeats, no rejection.** The $k$ outputs are distinct by construction, and no draw is thrown away.
- **A threshold for estimators.** The $(k+1)$-th largest value $\kappa$, which the search sees but does not keep, makes $q(y) = 1 - \exp(-\exp(\phi_y - \kappa))$ the inclusion probability of an output; Kool et al. use it in an estimator of expectations that is unbiased for sampling without replacement.

## Variants and improvements

- **Temperature.** Divide the log probabilities by a temperature before perturbing to sample from a sharper or flatter model ([temperature sampling](/temperature-sampling/)); the sampler stays exact for the new model.
- **Flat lists.** On a single categorical distribution the method reduces to the Gumbel-top-k trick, which is the same as [weighted reservoir sampling](/weighted-reservoir-sampling/) with keys $u^{1/w}$, up to a monotone change of variable.
- **Estimators.** Use the sample with the threshold $\kappa$ for low variance estimates of an expected reward or loss, for example in [minimum Bayes risk decoding](/minimum-bayes-risk-decoding/), or with [importance sampling](/importance-sampling/) weights.
- **Diverse search.** [Diverse beam search](/diverse-beam-search/) also returns different outputs, but by a penalty and without a probabilistic meaning.

## When to use it

Use stochastic beam search when you need $k$ distinct outputs and their sampling probabilities matter: low variance estimates of an expectation over outputs, training with sampled sequences, or a candidate set for reranking that is still a fair sample. Use ordinary sampling when repeats are fine, and plain beam search when you want the most probable outputs.

## Pitfalls

- **Overflow in the shift.** The formula of line L7 overflows for large values; use the stable form.
- **$\log(1 - e^a)$ near $a = 0$.** A naive log1p(-exp(a)) loses the digits for $a$ near 0, and log(-expm1(a)) loses them for very negative $a$; switch at $a = -\ln 2$.
- **Open nodes at the limit.** An output that is still open after $n$ tokens is not a leaf of the model. If the model can run past $n$, the sampler is exact only for the model conditioned on finishing in time. Make the model end within $n$ tokens.
- **Reusing the noise.** Every expansion needs fresh independent Gumbels. Reusing a seed across calls correlates the samples.
- **Order matters.** The values are a ranking: the $i$-th output is the $i$-th draw. Sorting the outputs by probability afterwards loses that, which matters for the estimators.

## Implementations

The code takes the log probabilities of the model as given, as a function of the prefix, and implements the sampler around them; it does not run or train a network.

## History

The Gumbel-max trick goes back to the study of choice models and to extreme value theory; it was popular in machine learning by the 2010s. Kool, van Hoof and Welling 2019 observed that the top-down sampling of perturbed values, used before for single samples, can be pruned by a beam, and that the beam then returns an exact sample without replacement. They applied it to translation and to estimators of sentence-level quantities.

## References
