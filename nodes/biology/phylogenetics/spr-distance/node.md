---
tag: B2M14X
kind: problem
slug: spr-distance
name: Subtree prune-and-regraft distance
aliases:
- SPR distance
area: biology/phylogenetics
level: research
summary: The least number of SPR moves that turn one phylogenetic tree into another. NP-hard and fixed-parameter tractable; the rooted version equals a maximum agreement forest size minus one.
prereqs: [subtree-prune-and-regraft, phylogenetic-tree]
see_also: [maximum-agreement-forest, rspr-maf-equivalence, tree-bisection-and-reconnection, maximum-agreement-subtree, robinson-foulds-distance, horizontal-gene-transfer, phylogenetic-network, fixed-parameter-tractable]
sources:
  - paper: doi:10.1007/s00026-001-8006-8
    title: B. L. Allen and M. Steel, Subtree transfer operations and their induced metrics on evolutionary trees, Annals of Combinatorics 5, 2001, 1-15
    locator: the TBR distance equals the maximum agreement forest size minus one, the gap with uSPR, and the reduction rules that give a kernel
  - paper: doi:10.1007/s00026-004-0229-z
    title: M. Bordewich and C. Semple, On the computational complexity of the rooted subtree prune and regraft distance, Annals of Combinatorics 8, 2005, 409-423
    locator: the rSPR distance equals the size of a maximum agreement forest with the root leaf minus one, NP-hardness and fixed-parameter tractability
  - paper: doi:10.1016/S0166-218X(96)00062-5
    title: J. Hein, T. Jiang, L. Wang and K. Zhang, On the complexity of comparing evolutionary trees, Discrete Applied Mathematics 71, 1996, 153-169
    locator: agreement forests, NP-hardness of the agreement forest problem and a 3-approximation, and the claim on unrooted SPR that Allen and Steel later refuted
  - paper: doi:10.1137/110845045
    title: C. Whidden, R. G. Beiko and N. Zeh, Fixed-parameter algorithms for maximum agreement forests, SIAM Journal on Computing 42(4), 2013, 1431-1466
    locator: the O(2.42^k n) rSPR algorithm, the O(3^k n) TBR algorithm and the linear-time 3-approximations
  - paper: "G. Hickey, F. Dehne, A. Rau-Chaplin and C. Blouin, SPR distance computation for unrooted trees, Evolutionary Bioinformatics 4, 2008, 17-27"
    title: G. Hickey, F. Dehne, A. Rau-Chaplin and C. Blouin, SPR distance computation for unrooted trees, 2008
    locator: the NP-hardness argument for uSPR distance and an exact search
  - paper: doi:10.1109/TCBB.2008.132
    title: M. L. Bonet and K. St. John, On the complexity of uSPR distance, IEEE/ACM Transactions on Computational Biology and Bioinformatics 7(3), 2010, 572-576
    locator: the completed proof that uSPR distance is NP-hard
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 2, tree rearrangement operations and the metrics they induce
---

The subtree prune-and-regraft distance between two [phylogenetic trees](/phylogenetic-tree/) on the same leaves is the least number of [SPR](/subtree-prune-and-regraft/) moves that turn one tree into the other. The rooted version (rSPR) and the unrooted version (uSPR) are different problems, and the [TBR](/tree-bisection-and-reconnection/) distance is a third, close relative. The rSPR distance equals the size of a [maximum agreement forest](/maximum-agreement-forest/) minus one, provided that a root leaf is added to both trees (Bordewich and Semple 2005, see [the equivalence](/rspr-maf-equivalence/)). The TBR distance equals the unrooted maximum agreement forest size minus one (Allen and Steel 2001). The uSPR distance has no such formula. All three are [NP-hard](/np-hard/), and all three are [fixed-parameter tractable](/fixed-parameter-tractable/) in the distance.

## In plain words

Take two family trees for the same species. One SPR move cuts off a branch together with everything that hangs from it, and glues it back somewhere else on the tree. The SPR distance asks for the fewest such moves that turn the first tree into the second.

The question matters because one move is a simple model of one event in which a gene jumps between lineages, or one event of hybrid origin. A small distance says that the two trees differ by a few such events.

The count is hard to find exactly. No fast method is known for large trees with a large distance. Fast methods exist when the distance is small, because they search over the few moves that can matter. The rooted problem also has a neat restatement: cut both trees into the fewest pieces that match.

## Definition

Let $X$ be a set of $n$ leaf labels.

**Rooted trees.** A rooted binary phylogenetic tree on $X$ has a root of degree 2, internal nodes of degree 3 and leaves labelled bijectively by $X$. An *rSPR move* on $T$ deletes an edge $(u, v)$ with $v$ below $u$, so that $T$ splits into the subtree $T_v$ and the rest. It then adds a new node on an edge of the rest, or a new root above the old root, joins it to $v$, and suppresses $u$, which now has degree 2 (or deletes it if it was the root). The rSPR distance $d_{\mathrm{rSPR}}(T_1, T_2)$ is the least number of rSPR moves that turn $T_1$ into $T_2$.

**Unrooted trees.** An unrooted binary phylogenetic tree on $X$ has internal nodes of degree 3. A *uSPR move* deletes an edge $\{u, v\}$, suppresses $u$, subdivides an edge of the component that holds $u$ with a new node $w$, and adds the edge $\{v, w\}$. The cut end $v$ stays where it was in its own component. A *TBR move* is the same, except that $v$ may also be replaced by a new node on any edge of its component. The distances $d_{\mathrm{uSPR}}$ and $d_{\mathrm{TBR}}$ are defined as before.

**The problem.** Given $T_1$ and $T_2$ on $X$, compute $d(T_1, T_2)$. In the decision version, a bound $k$ is also given, and the question is whether $d(T_1, T_2) \le k$.

Each move can be undone by one move of the same kind, and any tree can be reached from any other. So each distance is a metric on the trees on $X$. Each uSPR move is a TBR move, so $d_{\mathrm{TBR}} \le d_{\mathrm{uSPR}}$. Forget the roots of two rooted trees: each rSPR move becomes a uSPR move or no change, so $d_{\mathrm{uSPR}} \le d_{\mathrm{rSPR}}$.

## Variants

- **Rooted SPR (rSPR).** The main case in work on lateral gene transfer and hybridization, because the root fixes the direction of time.
- **Unrooted SPR (uSPR).** The move set of many tree searches. Every unrooted binary tree on $n \ge 4$ leaves has exactly $2(n-3)(2n-7)$ uSPR neighbors (Allen and Steel 2001).
- **TBR.** A superset of uSPR moves. The number of TBR neighbors depends on the shape of the tree.
- **The hybridization number** asks for the least number of reticulations in a [phylogenetic network](/phylogenetic-network/) that displays both trees. It is at least $d_{\mathrm{rSPR}}$ and can be larger, because it needs an acyclic agreement forest.
- **Many trees.** For more than two trees, one asks for a supertree or network that is close to all of them. These problems are harder still and are mostly solved by heuristics.
- **Nonbinary trees.** With multifurcations, a common choice is the least distance over all binary refinements of the two trees.

## Examples

**Three leaves.** $T_1 = ((a,b),c)$ and $T_2 = ((a,c),b)$. Prune $b$ and regraft it above the root. This gives $((a,c),b)$, so $d_{\mathrm{rSPR}} = 1$.

**The root matters.** Let $T_1 = ((a,(b,c)),d)$ and $T_2 = (((a,d),b),c)$. Two moves suffice.

| step | tree | move |
|---|---|---|
| 0 | $((a,(b,c)),d)$ | |
| 1 | $((a,d),(b,c))$ | prune $d$, regraft on the edge above $a$ |
| 2 | $(((a,d),b),c)$ | prune $c$, regraft above the root |

A breadth-first search over the 15 rooted trees on 4 leaves shows that no single move works, so $d_{\mathrm{rSPR}} = 2$. If the roots are forgotten, both trees are the quartet $ad \mid bc$, so $d_{\mathrm{uSPR}} = d_{\mathrm{TBR}} = 0$. The pair also shows why the root leaf $\rho$ is needed in the agreement forest. The two pieces $\{a, d\}$ and $\{b, c\}$ agree in both trees and are disjoint in both, which would suggest a distance of 1. With $\rho$ added above both roots, the piece that holds $\rho$ must also agree, and a maximum agreement forest is $\{\{a\}, \{b\}, \{c, d, \rho\}\}$, of size 3.

**uSPR is not TBR.** Let $T_1$ be the unrooted caterpillar with cherries $(A, B)$ and $(E, F)$ and the middle leaves $C$, $D$, in that order. Let $T_2$ have cherries $(A, C)$ and $(D, E)$ and the middle leaves $B$, $F$.

$$T_1 = ((A,B),C,(D,(E,F))), \qquad T_2 = ((A,C),B,(F,(D,E))).$$

Both trees have the split $\{A, B, C\} \mid \{D, E, F\}$. Cut this edge. In $T_1$ the edge meets the left side next to $C$ and the right side next to $D$. In $T_2$ it meets the left side next to $B$ and the right side next to $F$. One TBR move changes both ends, so $d_{\mathrm{TBR}} = 1$. A uSPR move keeps one end, and a breadth-first search confirms $d_{\mathrm{uSPR}} = 2$. Hein, Jiang, Wang and Zhang (1996) stated that the uSPR distance equals the agreement forest size minus one. Allen and Steel (2001) showed that this is the TBR distance and that the uSPR distance can be larger, as here.

## Known algorithms

| problem | method | time | source |
|---|---|---|---|
| all three | [breadth-first search](/breadth-first-search/) over tree space | $(2n-3)!!$ trees, each with $O(n^2)$ neighbors | folklore, usable up to about 8 leaves |
| rSPR | subtree and chain reduction, a kernel with $O(k)$ leaves | polynomial kernel, then exhaustive search | Bordewich and Semple 2005 |
| TBR | subtree and chain reduction, a kernel with $O(k)$ leaves | polynomial kernel, then exhaustive search | Allen and Steel 2001 |
| rSPR | [bounded search tree](/bounded-search-tree/) on agreement forests | $O(2.42^k n)$ | Whidden, Beiko and Zeh 2013 |
| TBR | bounded search tree on unrooted agreement forests | $O(3^k n)$ | Whidden, Beiko and Zeh 2013 |
| rSPR, TBR | 3-approximation of the agreement forest size | $O(n)$ | Whidden, Beiko and Zeh 2013 |
| uSPR | exact search with reductions | exponential | Hickey, Dehne, Rau-Chaplin and Blouin 2008 |

Here $k$ is the distance. The bounded search tree methods are the ones used in practice, for example in the rSPR program of Whidden. Their running time grows with $k$ and only linearly with $n$, so large trees are fine when the distance is small.

## Bounds

- **Hardness.** Computing $d_{\mathrm{rSPR}}$ is NP-hard (Bordewich and Semple 2005). Computing $d_{\mathrm{TBR}}$ is NP-hard, because the unrooted agreement forest problem is NP-hard (Hein, Jiang, Wang and Zhang 1996; Allen and Steel 2001). Computing $d_{\mathrm{uSPR}}$ is NP-hard (Hickey, Dehne, Rau-Chaplin and Blouin 2008, with a gap closed by Bonet and St. John 2010).
- **Order.** For trees on the same $n$ leaves, $d_{\mathrm{TBR}} \le d_{\mathrm{uSPR}} \le d_{\mathrm{rSPR}}$ when the unrooted trees are the rooted ones with the root forgotten. The 6-leaf example above has $d_{\mathrm{TBR}} < d_{\mathrm{uSPR}}$.
- **Agreement subtrees.** If $S$ is a [maximum agreement subtree](/maximum-agreement-subtree/) of $T_1$ and $T_2$, then $d_{\mathrm{rSPR}} \le n - |S|$, since the leaves outside $S$ can be moved one at a time. In the same way $d_{\mathrm{TBR}} \le n - 3$, because any 3 leaves agree in two unrooted trees.
- **Against Robinson-Foulds.** One rSPR move that takes a leaf from deep in a caterpillar to the root changes $\Theta(n)$ clusters. So the [Robinson-Foulds distance](/robinson-foulds-distance/) can be large while the SPR distance is 1.
- **Neighborhoods.** The uSPR neighborhood has $2(n-3)(2n-7)$ trees for every shape. The rSPR and TBR neighborhoods depend on the shape. For $n = 6$, a direct count gives between 44 and 52 rSPR neighbors and between 30 and 34 TBR neighbors.

## Reductions

- **rSPR to agreement forests.** $d_{\mathrm{rSPR}}(T_1, T_2)$ is the least number of components of a rooted agreement forest of $T_1^\rho$ and $T_2^\rho$, minus one. Here $T^\rho$ adds a leaf $\rho$ as a sibling of the root. The proof is on [the equivalence page](/rspr-maf-equivalence/).
- **TBR to agreement forests.** $d_{\mathrm{TBR}}(T_1, T_2)$ is the least number of components of an unrooted agreement forest, minus one (Allen and Steel 2001). No root leaf is needed.
- **Kernelization.** Both reductions replace a common pendant subtree by one leaf, and shorten long common chains. After this, an instance at distance $k$ has $O(k)$ leaves. This is a [kernelization](/kernelization/), and it shows fixed-parameter tractability.
- **To the hybridization number.** A maximum acyclic agreement forest gives the hybridization number in the same way that a maximum agreement forest gives $d_{\mathrm{rSPR}}$. Acyclicity is the only added condition.

## Applications

- **Lateral gene transfer.** In bacteria and archaea, a gene tree that differs from the species tree by $k$ rSPR moves is consistent with at most $k$ transfer events. Methods for finding such [transfers](/horizontal-gene-transfer/) compare each gene tree with a reference tree by SPR moves.
- **Hybridization and networks.** The rSPR distance is a lower bound on the hybridization number of two trees, which is a step in building a minimal [phylogenetic network](/phylogenetic-network/).
- **Tree search.** Parsimony and likelihood programs move through tree space by SPR or TBR moves. The distance tells how far apart two local optima are in that move graph.
- **Comparing posterior samples.** The SPR distance between trees sampled by Markov chain Monte Carlo gives a measure of how far the chain moves, and how much the sampled trees differ.

## References
