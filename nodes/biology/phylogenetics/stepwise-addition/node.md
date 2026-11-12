---
tag: 3VNTRD
kind: technique
slug: stepwise-addition
name: Stepwise addition
aliases:
- sequential taxon addition
area: biology/phylogenetics
level: advanced
summary: Build a tree by adding taxa one at a time, each at the edge that gives the best score. Step k has 2k - 5 choices, so the choices of all steps index the (2n - 5)!! unrooted trees.
prereqs: [maximum-parsimony, phylogenetic-tree]
see_also: [nearest-neighbor-interchange, subtree-prune-and-regraft, tree-bisection-and-reconnection, greedy-algorithm, depth-first-branch-and-bound, phylogenetic-placement, maximum-likelihood-phylogeny, fitch-algorithm]
sources:
  - paper: doi:10.1007/BF01734359
    title: Joseph Felsenstein, Evolutionary trees from DNA sequences, a maximum likelihood approach, Journal of Molecular Evolution 17(6), 1981, 368-376
    locator: the construction of the maximum likelihood tree by adding species one at a time at the best place, followed by local rearrangements
  - paper: doi:10.2307/2412028
    title: James S. Farris, Methods for computing Wagner trees, Systematic Zoology 19(1), 1970, 83-92
    locator: the Wagner tree built by joining taxa one at a time to the tree at the place of least added length
  - paper: doi:10.1016/0025-5564(82)90027-x
    title: M. D. Hendy and D. Penny, Branch and bound algorithms to determine minimal evolutionary trees, Mathematical Biosciences 59(2), 1982, 277-290
    locator: the search tree of partial trees built by adding taxa in order, and its pruning by the length of a partial tree
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 3, How many trees are there?, the count by adding species one at a time; Chapter 4, Finding the best tree by heuristic search, the sequential addition strategy
---

Stepwise addition builds an unrooted binary [phylogenetic tree](/phylogenetic-tree/) by adding the taxa one at a time. It starts with the only tree on three taxa. At each step it tries the new taxon on every edge of the current tree, scores each result, and keeps the best one, as a [greedy algorithm](/greedy-algorithm/) does. The $k$-th taxon has $2k - 5$ edges to choose from, and every tree on $n$ taxa comes from exactly one sequence of choices, which is why there are $(2n-5)!!$ such trees. Felsenstein (1981) used the method to build [maximum likelihood](/maximum-likelihood-phylogeny/) trees, and it is the usual start tree of a [parsimony](/maximum-parsimony/) search before swapping by [NNI](/nearest-neighbor-interchange/), [SPR](/subtree-prune-and-regraft/) or [TBR](/tree-bisection-and-reconnection/).

## In plain words

Start with three species. There is only one way to join three species in an unrooted tree. Now take the fourth species and try it on each branch of that small tree. Score each try and keep the best. Take the fifth species, try it on each branch of the tree you kept, and keep the best again. Go on until every species is in.

Each step is a small and fast search, so the whole method is fast. But it never takes back a choice. A place that looks best early can force a worse tree later, and the result depends on the order in which the species come. So programs run it many times with the species in random orders, and then improve each result with rearrangements.

## When it applies

The model is $n \ge 3$ taxa with $m$ aligned sites (binary, multistate or DNA characters), unrooted binary trees, and a score defined on trees with any subset of the taxa: a parsimony length, a negative log likelihood, or a minimum evolution length. The search space for the final tree has $(2n-5)!!$ trees, and finding the best one is NP-hard for [parsimony](/maximum-parsimony-np-hard/) and [likelihood](/ml-tree-np-hard/). Stepwise addition is a heuristic: it scores $(n-2)^2 - 1$ trees, a tiny part of the space, and gives no bound on the gap to the optimum.

It needs a score that means something on a partial tree. Parsimony length has this property in a strong form: adding a taxon never lowers the length, so the length of a partial tree is a lower bound on every completion of it. That property is what [branch and bound](/depth-first-branch-and-bound/) uses on the same search tree.

## The template

The order of the taxa is the first hole, and SCORE is the second. A tree is an adjacency map; inserting leaf $\ell$ on edge $\{x, y\}$ replaces the edge by a new vertex $w$ joined to $x$, $y$ and $\ell$.

```pseudo id=main
STEPWISE-ADDITION(order, SCORE)
L1  T ← the tree with one internal vertex joined to order[1], order[2] and order[3]
L2  for each taxon ℓ in order[4..n] do
L3      best ← none
L4      for each edge e of T do
L5          T' ← T with ℓ inserted on e
L6          if best is none or SCORE(T') < SCORE(best) then best ← T'
L7      T ← best
L8  return T and SCORE(T)
```

Ties on line L6 go to the first edge in a fixed order. When taxon $\ell$ is the $k$-th one, $T$ has $k - 1$ leaves and $2(k-1) - 3 = 2k - 5$ edges. Over $k = 4, \ldots, n$ the loop scores
$$\sum_{k=4}^{n} (2k - 5) = 3 + 5 + \cdots + (2n - 5) = (n-2)^2 - 1$$
trees. With the Fitch length computed from scratch in $O(km)$ time for a tree with $k$ leaves, a run costs $O(n^3 m)$ in the worst case. For Fitch parsimony an insertion can be scored in $O(m)$: the length of $T'$ is the length of $T$ plus the number of sites where the state of $\ell$ is not in the Fitch set of $T$ rooted on $e$. With the root sets of all edges computed in $O(km)$ per step, a run costs $O(n^2 m)$.

**Theorem (the count of trees).** For $n \ge 3$, the map that sends a sequence of edge choices $(e_4, \ldots, e_n)$, with $e_k$ one of the $2k - 5$ edges of the current tree, to the final tree is a bijection onto the unrooted binary trees with leaves $1, \ldots, n$. Hence there are $\prod_{k=4}^{n} (2k-5) = (2n-5)!!$ such trees.

*Proof.* By induction on $n$. For $n = 3$ there is one tree and one empty sequence. Let $n \ge 4$ and let $T$ be a binary tree on $1, \ldots, n$. The leaf $n$ hangs from an internal vertex $w$ with two other neighbors $x$ and $y$. Deleting $n$ and suppressing $w$ gives a binary tree $T^-$ on $1, \ldots, n-1$ with an edge $\{x, y\}$, and inserting $n$ on $\{x, y\}$ gives back $T$. So every $T$ comes from some pair ($T^-$, edge). Two different pairs give different trees: deleting $n$ from the result recovers $T^-$, and the neighbors of $w$ recover the edge. So the map from pairs to trees on $n$ leaves is a bijection, and by induction the trees on $n - 1$ leaves are in bijection with the sequences $(e_4, \ldots, e_{n-1})$. Each such tree has $2(n-1) - 3 = 2n - 5$ edges, which gives the product. $\blacksquare$

Running STEPWISE-ADDITION with "try all edges and recurse on each" instead of "keep the best" enumerates all $(2n-5)!!$ trees once each, which is the exhaustive search.

## Classic examples

**A greedy miss on five taxa.** Take the DNA sequences A = CACCCC, B = AACCAA, C = ACCCCA, D = CAACAA and E = CCCACA, with the Fitch length as SCORE and the order A, B, C, D, E.

| step | candidate places and lengths | kept |
|---|---|---|
| start | the star (A, B, C) | length 4 |
| add D | on A's edge 6, on B's edge 6, on C's edge 7 | A's edge (tie, first edge): ((A,D),(B,C)), length 6 |
| add E | on A's edge 8, B's 9, C's 8, D's 8, the inner edge 8 | A's edge: ((A,E),D,(B,C)), length 8 |

The most parsimonious tree is $((B,D),A,(C,E))$ with length 7. It comes from the other choice of the tie: D on B's edge, and then E on C's edge. The greedy tree is not improved by any NNI, whose four neighbors have lengths 8, 9, 8 and 8, but one of its 12 SPR neighbors is the optimum. Over all 120 orders of the five taxa, 96 orders reach length 7 and the other 24 do not. This is why programs repeat the method with random addition orders.

**Maximum likelihood.** Felsenstein (1981) added species one at a time at the place of highest likelihood, with local rearrangements after each addition. The score of each candidate needs [Felsenstein pruning](/felsenstein-pruning/) with branch lengths fitted at the new place.

**Wagner trees.** Farris (1970) built parsimony trees by joining each taxon at the place that adds the least length, the Wagner method.

**Branch and bound.** Hendy and Penny (1982) search the same tree of partial trees, in which a node at depth $k$ has $2k - 5$ children. For parsimony the length of a partial tree is a lower bound on all its completions, so a branch whose partial tree is already longer than the best full tree found so far is cut. This gives the exact optimum, at a cost that is exponential in the worst case.

## Variations

- **Random addition sequences.** Run the method with many random orders and keep the best trees, then swap each with TBR. This is the standard start of a large parsimony search.
- **Closest taxon first.** Choose the next taxon by a rule, such as the one whose best insertion adds least length.
- **Rearrange as you go.** After each addition, apply NNI or SPR swaps to the partial tree, as in Felsenstein's 1981 method.
- **Keep several trees.** Keep the $b$ best partial trees at each step instead of one, a beam search.
- **Placement.** [Phylogenetic placement](/phylogenetic-placement/) is one step of stepwise addition on a fixed reference tree, with each query placed on its own and the tree never updated.

## Pitfalls

- **Order dependence.** The result depends on the addition order, and on the tie rule. In the example above, one tie decides between length 8 and length 7.
- **Partial scores can mislead.** Early taxa are placed with little information, and a later taxon cannot move them.
- **Not a lower bound for likelihood.** The log likelihood of a partial tree is not a bound on the log likelihood of its completions in the way the parsimony length is, so branch and bound with likelihood needs other bounds.
- **Treat it as a start.** The output need not be a local optimum for any move, and in the example it is an NNI optimum but not an SPR optimum. Swap it before using it.

## Exercises

1. Show that adding a taxon never lowers the Fitch length of a tree, so that the length of a partial tree is a lower bound for every completion.
2. Prove the $O(m)$ insertion score: the length of $T'$ is the length of $T$ plus the number of sites where the state of $\ell$ is not in the root set of $T$ on edge $e$.
3. Change STEPWISE-ADDITION into an enumeration of all $(2n-5)!!$ trees, and then into a depth-first branch and bound for parsimony.
4. In the five-taxon example, change the tie rule to keep the last best edge instead of the first, and run the order A, B, C, D, E again.

## References
