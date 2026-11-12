---
tag: GM2NX0
kind: algorithm
slug: parsimony-ratchet
name: Parsimony ratchet
aliases:
- Nixon ratchet
area: biology/phylogenetics
level: research
summary: Iterated tree search for maximum parsimony. Each round doubles the weight of a random subset of characters, swaps branches by TBR, restores the weights and swaps again.
solves: [maximum-parsimony]
model: word-ram
complexity:
  vars: {n: the number of taxa, m: the number of characters, k: the number of iterations}
  time: {worst: O(k n^5 m^2)}
  space: {extra: O(n + m)}
properties: {deterministic: false, randomized: true, exact: false}
history:
  year: 1999
  people: [Kevin C. Nixon]
  note: Nixon published the ratchet in Cladistics in 1999 as a fast way to find shortest trees for data sets of hundreds of taxa, where repeated random addition and TBR swapping stalled.
prereqs: [maximum-parsimony, fitch-algorithm, tree-bisection-and-reconnection]
see_also: [iterated-local-search, simulated-annealing, stepwise-addition, subtree-prune-and-regraft, nearest-neighbor-interchange, maximum-parsimony-np-hard, phylogenetic-bootstrap, local-search]
sources:
  - paper: doi:10.1111/j.1096-0031.1999.tb00277.x
    title: Kevin C. Nixon, The parsimony ratchet, a new method for rapid parsimony analysis, Cladistics 15(4), 1999, 407-414
    locator: the description of the method, a search under randomly reweighted characters followed by a search under the original weights from the tree it found, repeated many times
  - paper: doi:10.1111/j.1096-0031.1999.tb00278.x
    title: Pablo A. Goloboff, Analyzing large data sets in reasonable times, solutions for composite optima, Cladistics 15(4), 1999, 415-428
    locator: sectorial searches, tree drifting and tree fusing, other methods to leave local optima in large parsimony searches
  - paper: doi:10.1080/10635150309330
    title: Rutger A. Vos, Accelerated likelihood surface exploration, the likelihood ratchet, Systematic Biology 52(3), 2003, 368-373
    locator: the ratchet with a likelihood score in place of the parsimony length
---

The parsimony ratchet is a heuristic search for [maximum parsimony](/maximum-parsimony/) trees by Nixon (1999). It holds one tree. Each iteration gives a random subset of the characters weight 2, runs a [TBR](/tree-bisection-and-reconnection/) branch swapping search under these weights, then sets all weights back to 1 and runs a TBR search again from the tree that the first search found. The reweighting changes the score surface, so the first search can leave a local optimum of the true score; the second search climbs down in the true score from a new place. The best tree under the original weights over all iterations is the result. The ratchet is a form of [iterated local search](/iterated-local-search/), with a perturbation of the data instead of a random move on the tree.

## In plain words

A search that only takes steps that make the tree shorter will stop at a tree that no single step improves, even when a much shorter tree exists. The ratchet shakes the search loose by changing the question for a short time.

It picks some of the characters at random and counts them twice. Under this changed count, the current tree is often no longer the best one nearby, so the search moves on. Then the ratchet goes back to the true count and searches again from where it now is. Often it ends in a new valley, and sometimes in a deeper one. It does this many times and keeps the shortest tree it found under the true count.

## The problem

The model has $n \ge 4$ taxa and $m$ characters, each an unordered multistate character such as one DNA site. A tree is an unrooted binary tree with the taxa at its $n$ leaves. A weight vector $w$ gives each character $j$ a positive integer weight $w_j$, and the weighted length of a tree $T$ is

$$L_w(T) = \sum_{j=1}^{m} w_j \, c_j(T),$$

where $c_j(T)$ is the least number of changes of character $j$ on $T$, given by the [Fitch algorithm](/fitch-algorithm/). The goal is a tree that minimizes $L_1$, the length with all weights 1. There are $(2n-5)!!$ trees, and the problem is [NP-hard](/maximum-parsimony-np-hard/). The ratchet is a heuristic over these trees: it returns a tree that is a TBR local optimum of $L_1$, and it gives no bound on the gap to the true minimum.

## The algorithm

TBR-SEARCH$(T, w)$ is steepest descent: it scores every TBR neighbor of $T$ under $L_w$, moves to the shortest one if it is shorter than $T$, and repeats until no neighbor is shorter. It returns the last tree and its length. The parameter $p$ is the chance that a character gets weight 2 in an iteration, and $k$ is the number of iterations.

```pseudo id=main
PARSIMONY-RATCHET(start, k, p, rng)
L1  (T, s) ← TBR-SEARCH(start, all weights 1)
L2  (best, b) ← (T, s)
L3  repeat k times
L4      w' ← for each character j, 2 with probability p and 1 otherwise
L5      T ← TBR-SEARCH(T, w')
L6      (T, s) ← TBR-SEARCH(T, all weights 1)
L7      if s < b then (best, b) ← (T, s)
L8  return (best, b)
```

The start tree is usually a [stepwise addition](/stepwise-addition/) tree with a random order of the taxa. Line L5 starts from the tree of the last line L6, so the iterations form one chain: the ratchet does not restart from scratch. The weights of line L4 are new in each iteration.

## Example

Take seven taxa A to G with ten DNA sites.

| taxon | sites 1 to 10 |
|---|---|
| A | CTAGCTTCGC |
| B | TGGAACTAAT |
| C | ATCCATGTCT |
| D | CAGAACTAGC |
| E | GGCCGAGAAT |
| F | GGGTTCCGAA |
| G | TCCTAAACTC |

An exhaustive count over all 945 trees gives these Fitch lengths.

| length | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 | 41 |
|---|---|---|---|---|---|---|---|---|---|---|
| trees | 1 | 17 | 61 | 113 | 184 | 148 | 157 | 161 | 93 | 10 |

The unique shortest tree is $((A,D),B,(F,(G,(C,E))))$ with length 32. The tree $((A,G),D,((B,F),(C,E)))$ has length 33, and none of its 64 TBR neighbors is shorter, so a TBR search that starts there stops at once. Run the ratchet from this tree with $p = 0.25$ and the generator `random.Random(1)`.

| line | weights of 2 | search result | length under $w'$ | length under 1 |
|---|---|---|---|---|
| L1 | none | $((A,G),D,((B,F),(C,E)))$, no move | | 33 |
| L5, iteration 1 | sites 1, 9, 10 | $((A,D),G,(B,(F,(C,E))))$ | 41 | 33 |
| L6, iteration 1 | none | $((A,D),B,(F,(G,(C,E))))$ | | 32 |
| iteration 2 | sites 4, 7, 10 | the same tree after both searches | 41 | 32 |
| iteration 3 | sites 1, 5, 7, 8 | the same tree after both searches | 46 | 32 |

The first perturbed search moves to a tree of the same true length 33, which is shorter under the new weights. From that tree, a TBR search under unit weights finds the optimum. Iterations 2 and 3 return to it. The test file runs this example and also checks, over random six-taxon data, that the result is never longer than a plain TBR search from the same start and never shorter than the exhaustive optimum.

## Correctness

The [proof](proofs/correctness/) shows four facts. Each TBR search ends, because the weighted length is a nonnegative integer that falls by at least 1 in each round. The pair $(best, b)$ on line L8 satisfies $b = L_1(best)$. The tree $best$ is a TBR local optimum of $L_1$. And $b$ is never more than the length that the plain search of line L1 reaches. Nothing more can be proved in general: the ratchet does not promise a shortest tree, and the shortest tree it finds depends on the random weights.

## Complexity

The costs are for the simple form in the code, with $n$ taxa, $m$ characters and $k$ iterations, in the worst case. One TBR round makes $O(n^3)$ joins. Each join builds a tree in $O(n)$ and scores it by Fitch in $O(nm)$, so a round costs $O(n^4 m)$. A character has at most $n - 1$ changes on any tree, so a weighted length is at most $2m(n-1)$, and a search makes at most $2m(n-1) + 1$ rounds. A search costs $O(n^5 m^2)$, and $k$ iterations cost $O(k n^5 m^2)$. The extra space is $O(n + m)$: one tree, a copy, and the change counts.

These bounds are loose in practice, where a search makes few rounds. With the join score of the TBR page, which reads the Fitch sets of both parts rooted on the two join edges in $O(m)$ after an $O(nm)$ pass per cut, a round costs $O(n^3 m)$.

## Properties

- **Randomized.** Only line L4 uses the generator. With a fixed seed and start tree the run is deterministic.
- **Monotone.** The value $b$ never rises over the iterations, and the result is never worse than the search of line L1 alone.
- **Local optimum.** The result is a TBR local optimum under unit weights, since it is the output of line L1 or of line L6.
- **One tree in memory.** Each search in the code holds one tree, which keeps each iteration fast.

## Variants and improvements

- **Deleting characters.** Give the chosen characters weight 0 instead of 2, a jackknife-style perturbation.
- **Other search moves.** Use SPR or NNI in place of TBR for speed, at the cost of weaker local optima.
- **Likelihood ratchet.** Vos (2003) used the same scheme with a likelihood score.
- **Combined strategies.** Goloboff (1999) gave sectorial searches, tree drifting and tree fusing for large parsimony searches. Programs combine these with the ratchet and with many random addition starts.
- **Keep all ties.** Keep every tree of length $b$ found at line L6, to get a set of shortest trees and not one.

## When to use it

Use the ratchet for large parsimony searches, with many taxa, where random addition plus TBR keeps returning trees of the same length. For data small enough to search all $(2n-5)!!$ trees, or to use branch and bound, use the exact method. For a model-based score, a likelihood search or [Bayesian inference](/bayesian-phylogenetic-inference/) is the usual choice.

## Pitfalls

- **Restoring the weights.** Line L6 must use the original weights. A ratchet that keeps the perturbed weights searches a different problem.
- **Comparing lengths.** Line L7 compares lengths under the original weights only. The length under $w'$ is not comparable across iterations.
- **Too many or too few characters.** With $p$ near 0, line L5 rarely moves. With $p$ near 1, almost all weights double, which scales the score and leaves the surface almost as it was. Choose $p$ between these extremes and test the choice on the data.
- **No proof of optimality.** A long run with no change in $b$ is no proof that $b$ is the minimum.
- **Ties at line L7.** The strict test keeps the first tree of length $b$. Other shortest trees found later are lost unless they are kept on purpose.

## Implementations

## History

Nixon presented the ratchet in 1999, in the same issue of Cladistics as Goloboff's paper on sectorial searches, tree drifting and tree fusing. Both papers addressed the same problem: large parsimony data sets, with hundreds of taxa, where repeated random addition and TBR swapping found trees of the same length many times and did not reach shorter ones. Vos (2003) carried the idea over to likelihood.

## References
