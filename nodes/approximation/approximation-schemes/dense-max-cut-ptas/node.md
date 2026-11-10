---
tag: SEQDJG
kind: algorithm
slug: dense-max-cut-ptas
name: Arora-Karger-Karpinski PTAS for dense max-cut
aliases:
- AKK PTAS
- dense graph max-cut PTAS
- exhaustive sampling for dense max-cut
- Fernandez de la Vega max-cut scheme
area: approximation/approximation-schemes
level: research
summary: Sampling-based approximation scheme for max-cut in dense graphs, running in polynomial time for each fixed ε.
solves: [maximum-cut]
model: word-ram
complexity:
  vars: {n: the number of vertices, ε: the accuracy parameter, δ: "the density (the graph has at least δn^2 edges)", c: an absolute constant}
  time: {worst: "O(2^(c/(ε^3 δ^3)) n^2)", average: "O(2^(c/(ε^3 δ^3)) n^2)", best: "O(2^(c/(ε^3 δ^3)) n^2)"}
  space: {extra: "O(n + 1/(ε^3 δ^3))"}
properties: {online: false, deterministic: false, recursive: false}
history:
  year: 1995
  people: [Sanjeev Arora, David Karger, Marek Karpinski, Wenceslas Fernandez de la Vega]
  note: Arora, Karger and Karpinski gave approximation schemes for dense instances of max-cut and other problems by exhaustive sampling; Fernandez de la Vega gave a direct sampling scheme for dense max-cut.
prereqs: [maximum-cut, dense-graph, ptas, linearity-of-expectation, variance, markov-inequality]
see_also: [max-cut-ugc-hardness, semidefinite-programming, randomized-rounding, max-2-sat, monte-carlo-algorithm, random-sampling, chebyshev-inequality, eptas]
sources:
  - paper: "S. Arora, D. Karger and M. Karpinski, Polynomial time approximation schemes for dense instances of NP-hard problems, Journal of Computer and System Sciences 58(1), 1999, pp. 193-210"
    title: Arora, Karger and Karpinski 1999
    locator: exhaustive sampling, the estimates of neighbour counts, and the scheme for dense max-cut
  - paper: "W. Fernandez de la Vega, MAX-CUT has a randomized approximation scheme in dense graphs, Random Structures and Algorithms 8(3), 1996, pp. 187-198"
    title: Fernandez de la Vega 1996
    locator: the sampling scheme without linear programming
  - paper: "O. Goldreich, S. Goldwasser and D. Ron, Property testing and its connection to learning and approximation, Journal of the ACM 45(4), 1998, pp. 653-750"
    title: Goldreich, Goldwasser and Ron 1998
    locator: the max-cut algorithm that splits the vertices into parts and samples outside each part
  - paper: "A. Frieze and R. Kannan, Quick approximation to matrices and applications, Combinatorica 19(2), 1999, pp. 175-220"
    title: Frieze and Kannan 1999
    locator: dense max-cut through a weak regularity decomposition
---

The approximation scheme of Arora, Karger and Karpinski (1995, journal version 1999) solves [max-cut](/maximum-cut/) within a factor $1 - \varepsilon$ on [dense graphs](/dense-graph/), the graphs with at least $\delta n^2$ edges for a fixed $\delta > 0$. Max-cut has no [PTAS](/ptas/) on general graphs unless P = NP, so density is what makes the scheme possible. The key idea is *exhaustive sampling*: take a sample of constant size, try every way to split the sample, and for each split put every other vertex on the side opposite to most of its sampled neighbours. In a dense graph the optimum cut has order $n^2$ edges, and the error of the sample estimates is a small part of that. This page gives the direct sampling form of the idea, close to Fernandez de la Vega (1996) and to Goldreich, Goldwasser and Ron (1998). It runs in time $2^{O(1/(\varepsilon\delta)^3)} n^2$.

## In plain words

We want to split the people of a crowded network into two teams so that as many friendships as possible join the two teams. Each person should join the team opposite to most of their friends. But we do not know the teams of their friends yet.

So we ask a few people chosen at random, and we guess their teams. We try every possible guess, since a few people have only a few. For each guess, every other person counts their friends among the asked people and joins the team where fewer of them are. One of the guesses is the true best split of the asked people, and for that guess the counts are good estimates. When everybody has many friends, a small estimation error changes few friendships compared with the large total.

## The problem

The input is a simple graph $G = (V, E)$ with $n$ vertices and $|E| \ge \delta n^2$ edges, and an accuracy $\varepsilon > 0$. A *cut* is a map $\sigma : V \to \{0, 1\}$, and its value $\mathrm{cut}(\sigma)$ is the number of edges whose ends are on different sides. The goal is a cut with $\mathrm{cut}(\sigma) \ge (1 - \varepsilon)\,\mathrm{OPT}$, where $\mathrm{OPT}$ is the largest cut value.

Every graph has a cut with at least $|E|/2$ edges, so $\mathrm{OPT} \ge \delta n^2/2$ on a dense graph. An additive error of $\varepsilon\delta n^2/2$ is therefore a relative error of at most $\varepsilon$. The scheme below has additive error $n^2(1/\sqrt t + 1/(2\ell))$ in expectation on every graph, and the density turns it into a relative bound.

## The algorithm

The algorithm has two integer parameters: the number of parts $\ell \ge 2$ and the sample size $t$. For the guarantee, set $\ell = \lceil 2/(\varepsilon\delta) \rceil$ and $t = \lceil 16/(\varepsilon\delta)^2 \rceil$.

```pseudo id=main
DENSE-MAX-CUT(G, ℓ, t)
L1  split V into parts V_1, ..., V_ℓ of sizes ⌊n/ℓ⌋ or ⌈n/ℓ⌉
L2  for each j, draw t vertices u_{j,1}, ..., u_{j,t} uniformly and independently from V \ V_j
L3  for each labelling s of all ℓt sample slots with labels in {0, 1}:
L4      for each part V_j and each vertex v in V_j:
L5          a_b(v) ← the number of slots i with u_{j,i} adjacent to v and s_{j,i} = b, for b = 0, 1
L6          put v on side 1 if a_0(v) ≥ a_1(v), else on side 0
L7      compute the value of this cut
L8      keep the cut if its value is the largest so far
L9  return the kept cut
```

A vertex that is drawn twice has two slots and may get two different labels in line L3. Such labellings are harmless: the proof needs only that the one labelling it uses is tried.

The vertices of $V_j$ are placed from samples outside $V_j$. This is what makes the analysis simple: the placement of $V_j$ does not change the samples it uses.

## Example

Take the graph on the vertices $0, \ldots, 7$ formed by the complete bipartite graph between $A = \{0, 3, 4, 7\}$ and $B = \{1, 2, 5, 6\}$, plus the two edges $\{0, 3\}$ and $\{4, 7\}$. It has $n = 8$ and 18 edges, and $\mathrm{OPT} = 16$, given by the split $A$ against $B$. Run the algorithm with $\ell = 2$ and $t = 2$, so $V_1 = \{0, 1, 2, 3\}$ and $V_2 = \{4, 5, 6, 7\}$.

One draw gives the samples $(7, 7)$ for $V_1$ and $(0, 2)$ for $V_2$. Line L3 tries $2^4 = 16$ labellings. Take the labelling $7 \mapsto 1$ (both slots), $0 \mapsto 1$ and $2 \mapsto 0$.

| vertex | sampled neighbours and labels | $a_0, a_1$ | side |
|---|---|---|---|
| 0 | none | 0, 0 | 1 |
| 1 | 7, 7 (label 1) | 0, 2 | 0 |
| 2 | 7, 7 (label 1) | 0, 2 | 0 |
| 3 | none | 0, 0 | 1 |
| 4 | 2 (label 0) | 1, 0 | 1 |
| 5 | 0 (label 1) | 0, 1 | 0 |
| 6 | 0 (label 1) | 0, 1 | 0 |
| 7 | 2 (label 0) | 1, 0 | 1 |

Side 1 is $\{0, 3, 4, 7\} = A$, so this guess gives a cut of value 16, and the algorithm returns an optimal cut. Another draw gives the samples $(5, 6)$ for $V_1$ and $(0, 3)$ for $V_2$. Vertices 1 and 2 have no neighbour among 5 and 6, so in every labelling they tie and go to side 1, together with one of 0 and 3 or both. The best of the 16 cuts then has value 8. With $t = 2$ such failures are common; the parameters of the guarantee are much larger.

## Correctness

The proof compares the output with a chain of hybrid cuts. Let $\sigma^*$ be a maximum cut, and let $H_j$ place $V_1, \ldots, V_j$ by lines L5 and L6, with the samples of part $i$ labelled by their sides in $H_{i-1}$, and place the other parts as $\sigma^*$. So $H_0 = \sigma^*$, and $H_\ell$ is one of the cuts that line L3 tries.

1. **One step.** $H_j$ and $H_{j-1}$ differ only on $V_j$. A vertex $v \in V_j$ gains $g_v = d^0(v) - d^1(v)$ cut edges to $V \setminus V_j$ by being on side 1 instead of side 0, where $d^b(v)$ counts its neighbours outside $V_j$ on side $b$ of $H_{j-1}$. Line L6 uses the estimate $\hat g_v = (N/t)(a_0(v) - a_1(v))$ with $N = |V \setminus V_j|$, and it loses at most $|\hat g_v - g_v|$ against the better side. Edges inside $V_j$ lose at most $e(V_j)$.
2. **Sampling.** $\hat g_v$ is an average of $t$ independent terms in $[-N, N]$ with mean $g_v$, so $\mathbb{E}|\hat g_v - g_v| \le N/\sqrt t \le n/\sqrt t$.
3. **Sum.** Over all steps, $\mathbb{E}[\mathrm{OPT} - \mathrm{ALG}] \le n^2/\sqrt t + \sum_j e(V_j) \le n^2/\sqrt t + n^2/(2\ell)$.

With the chosen $\ell$ and $t$ this is at most $\varepsilon\delta n^2/2 \le \varepsilon\,\mathrm{OPT}$. Repeating the algorithm $r$ times with the parameters for $\varepsilon/2$ and keeping the best cut gives $(1 - \varepsilon)\,\mathrm{OPT}$ with probability at least $1 - 2^{-r}$, by [Markov's inequality](/markov-inequality/). The full proof is below.

## Complexity

- **Time.** There are $2^{\ell t}$ labellings. For each, the placement costs $O(nt)$ with an adjacency matrix and the cut value costs $O(n^2)$. The total is $O(2^{\ell t}(nt + n^2))$. With $\ell t = O(1/(\varepsilon\delta)^3)$ this is $2^{O(1/(\varepsilon\delta)^3)} n^2$, which is linear in the size of the adjacency matrix for fixed $\varepsilon$ and $\delta$. The model is the [word RAM](/word-ram/).
- **Space.** $O(n)$ for the current and best cut and $O(\ell t)$ for the samples, besides the graph.

## Properties

| claim | statement | status |
|---|---|---|
| expected loss | $\mathbb{E}[\mathrm{OPT} - \mathrm{ALG}] \le n^2/\sqrt t + n^2/(2\ell)$ on every graph | proved below |
| guarantee | $(1 - \varepsilon)\,\mathrm{OPT}$ with probability at least $1 - 2^{-r}$ after $r$ runs, if $\lvert E \rvert \ge \delta n^2$ | proved below |
| time | $2^{O(1/(\varepsilon\delta)^3)} n^2$ | proved below |
| general graphs | no PTAS for max-cut unless P = NP; the best ratio is about 0.878 under the Unique Games Conjecture | [UGC hardness](/max-cut-ugc-hardness/) |

## Variants and improvements

- **Sampling with linear programming.** Arora, Karger and Karpinski sample $O(\log n/\varepsilon^2)$ vertices and try all $n^{O(1/\varepsilon^2)}$ labellings. For each labelling they estimate the neighbour counts of every vertex, write a linear program whose constraints keep these counts close to the estimates, and round its solution by [randomized rounding](/randomized-rounding/). The method applies to all problems that can be written as dense smooth integer programs, such as dense max-$k$-SAT, dense bisection and dense $k$-colourability for fixed $k$. Their algorithm can be made deterministic.
- **Weak regularity.** Frieze and Kannan approximate the adjacency matrix by a sum of few cut matrices and get an additive error of $\varepsilon n^2$ for max-cut and other dense problems.
- **Constant time estimates.** Goldreich, Goldwasser and Ron estimate the max-cut value of a dense graph to within $\varepsilon n^2$ from a sample whose size depends on $\varepsilon$ alone, and they find a cut with that value in time linear in $n$ for fixed $\varepsilon$.
- **Other dense problems.** The same sampling idea gives schemes for dense [max-2-SAT](/max-2-sat/) and for dense instances of other constraint problems whose objective counts satisfied pairs.

## When to use it

The scheme matters as a theorem: it shows that the hardness of max-cut sits in sparse graphs. For a graph with $\Theta(n^2)$ edges and any fixed $\varepsilon$, it gives a cut within $1 - \varepsilon$ of the optimum in time $O(n^2)$. The constants are huge: for $\varepsilon = \delta = \frac12$ the guarantee already needs $\ell t = 2048$ sample slots. On real inputs, local search or the [semidefinite programming](/semidefinite-programming/) relaxation does better. The analysis, a hybrid argument over parts with samples taken outside each part, is the standard template for sampling schemes on dense instances.

## Pitfalls

- **Additive, not relative, error.** On every graph the loss is $O(n^2)$ times a small factor. On a sparse graph $\mathrm{OPT}$ is $o(n^2)$ and this bound says nothing.
- **Samples from inside the part.** If a part used samples from itself, the estimate of $g_v$ would depend on the placement of the same part, and the hybrid argument breaks.
- **Small samples.** With a small $t$, many vertices have no sampled neighbour and line L6 sends them all to the same side, as in the example. The bound needs $t$ of order $1/(\varepsilon\delta)^2$.
- **One run is not enough.** The bound is on the expected loss. A single run can be far worse; the high-probability guarantee needs independent repetitions.

## Implementations

## History

Arora, Karger and Karpinski presented their approximation schemes for dense instances at STOC 1995, with the journal version in 1999. They introduced exhaustive sampling with linear programming and covered max-cut, max-$k$-SAT, bisection and other problems. Fernandez de la Vega (1996) gave a randomized scheme for dense max-cut by sampling alone. Goldreich, Goldwasser and Ron (1998) gave the partition into parts with samples from outside each part, as a by-product of property testing. Frieze and Kannan (1999) gave a third route through a weak form of the regularity lemma.

## References
