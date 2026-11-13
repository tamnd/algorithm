---
tag: BFRDCF
kind: problem
slug: phylogenetic-diversity-maximization
name: Maximizing phylogenetic diversity
aliases:
- maximum phylogenetic diversity
- PD maximization
area: biology/phylogenetics
level: research
summary: Choose k taxa, or taxa within a budget, whose phylogenetic diversity is as large as possible. Greedy is exact for k taxa; costs make it NP-hard.
prereqs: [phylogenetic-diversity, greedy-algorithm, knapsack-problem]
see_also: [greedy-choice-property, exchange-argument, submodular-function, greedy-max-coverage, tree-dynamic-programming, knapsack-dynamic-programming, pseudo-polynomial-time, weak-np-hardness]
sources:
  - paper: doi:10.1080/10635150590947023
    title: Mike Steel, Phylogenetic diversity and the greedy algorithm, Systematic Biology 54(4), 2005
    locator: pp. 527-529 (the greedy algorithm finds a set of k taxa of maximum PD, on rooted and unrooted trees)
  - paper: doi:10.1371/journal.pgen.0010071
    title: Fabio Pardi and Nick Goldman, Species choice for comparative genomics, being greedy works, PLoS Genetics 1(6), 2005
    locator: e71 (the same greedy result, and its use to choose species for genome sequencing)
  - paper: doi:10.1080/10635150701411279
    title: Fabio Pardi and Nick Goldman, Resource-aware taxon selection for maximizing phylogenetic diversity, Systematic Biology 56(3), 2007
    locator: pp. 431-444 (taxa with costs, NP-hardness, and a pseudo-polynomial dynamic program)
  - paper: doi:10.1016/0006-3207(92)91201-3
    title: Daniel P. Faith, Conservation evaluation and phylogenetic diversity, Biological Conservation 61(1), 1992
    locator: pp. 1-10 (PD as the objective of conservation choice)
---

Maximizing phylogenetic diversity asks for a set of taxa, of a given size or within a given budget, whose [phylogenetic diversity](/phylogenetic-diversity/) (PD) is as large as possible. With a size limit $k$, the [greedy algorithm](/greedy-algorithm/) that adds the taxon with the largest gain is exactly optimal, on rooted and on unrooted trees (Steel 2005; Pardi and Goldman 2005). With a cost on each taxon and a total budget, the problem contains the [0/1 knapsack problem](/knapsack-problem/) and is NP-hard, but a dynamic program over the tree solves it in pseudo-polynomial time (Pardi and Goldman 2007).

## In plain words

A group of species lives on a family tree with long and short branches. Money is enough to protect only some of them. Each protected set keeps the branches that lead to its members, and we want to keep as much total branch length as possible.

If each species costs the same, a simple rule works: first take the species with the most branch length of its own, then each time take the species that adds the most new branch length. This rule is never wrong here, which is rare for such simple rules.

If species have different costs, the problem becomes as hard as packing a bag with the most value under a weight limit. Then the simple rule can fail, and a slower table method finds the best set.

## Definition

**Input.** A tree $T$ with taxon set $X$ ($|X| = n$) and edge lengths $\ell(e) \ge 0$, and either

- an integer $k$ with $0 \le k \le n$ (the *size-constrained* problem), or
- a cost $c(x) \ge 0$ for each taxon and a budget $B$ (the *budgeted* problem).

**Output.** A set $S \subseteq X$ with $|S| = k$, or with $\sum_{x \in S} c(x) \le B$, that maximizes $\mathrm{PD}(S)$.

PD is rooted (the subtree spans $S$ and the root) or unrooted (the subtree spans $S$ only). For a rooted tree write $\mathrm{gain}(x \mid A) = \mathrm{PD}(A \cup \{x\}) - \mathrm{PD}(A)$: the length of the part of the root path of $x$ that the root paths of $A$ do not cover.

## Variants

- **Rooted or unrooted.** Both have greedy optimal solutions. In the unrooted case greedy starts from a pair of taxa at maximum distance.
- **Budgeted.** Costs per taxon and a budget (Pardi and Goldman 2007). NP-hard, see below.
- **Expected PD.** Each protected taxon survives with a higher probability than an unprotected one, and the objective is the expected PD of the survivors, as on the [phylogenetic diversity](/phylogenetic-diversity/) page. This is the Noah's Ark form of the problem.
- **Areas instead of taxa.** Choose areas to protect, each area holding several taxa, and maximize the PD of the union. This adds a covering structure on top of the tree.
- **Several trees or networks.** PD on several gene trees or on a [phylogenetic network](/phylogenetic-network/) changes the objective, and greedy is no longer exact in general.

## Examples

Take the rooted tree $((A{:}1, B{:}2){:}3, (C{:}4, (D{:}1, E{:}1){:}2){:}1)$, where the number after a colon is the length of the edge above that node.

**Greedy, rooted.** The root distances are $A = 4$, $B = 5$, $C = 5$, $D = 4$, $E = 4$.

| step | taxon added | gain | PD of the set |
|---|---|---|---|
| 1 | $B$ | 5 | 5 |
| 2 | $C$ | 5 | 10 |
| 3 | $D$ | 3 | 13 |
| 4 | $A$ | 1 | 14 |
| 5 | $E$ | 1 | 15 |

At step 3, $D$ and $E$ tie with gain 3, and at step 4, $A$ and $E$ tie with gain 1. Each prefix of the order is optimal for its size: no pair has rooted PD above 10, and no triple has PD above 13.

**Greedy, unrooted.** The largest distance between two taxa is $d(B, C) = 2 + 3 + 1 + 4 = 10$. Greedy starts from $\{B, C\}$ with PD 10, adds $D$ (distance 3 from the subtree), and then $A$ and $E$ with 1 each.

**Costs break greedy.** Take a star tree with taxa $1, 2, 3, 4$ on edges of lengths $6, 10, 12, 7$, with costs $1, 2, 3, 2$, and budget 4. The ratio of length to cost is $6, 5, 4, 3.5$. Greedy by ratio takes taxa 1 and 2 for PD 16 and then nothing else fits. The optimum is $\{1, 3\}$ with PD 18.

## Known algorithms

**Greedy for $k$ taxa (rooted).**

```pseudo id=main
GREEDY-PD(T, k)
L1  mark only the root as covered
L2  while fewer than k taxa are chosen do
L3      for each node v: gain(v) ← uncovered length on the path from the root to v
L4      x ← an unchosen taxon with the largest gain(x)
L5      add x to the chosen set
L6      mark the edges on the path from x up to the covered part
L7  return the chosen taxa, in order
```

Each round takes $O(n)$ time, so the whole run takes $O(nk)$ time. Greedy gives one order of the taxa, and each prefix is optimal for its size.

*Why greedy is optimal.* Write $B - b$ for $B \setminus \{b\}$.

*Exchange lemma.* If $|A| < |B|$, then some $b \in B \setminus A$ has $\mathrm{gain}(b \mid A) \ge \mathrm{PD}(B) - \mathrm{PD}(B - b)$.

*Proof.* For $b \in B$, let $P_b$ be the set of edges on the root path of $b$ below which no other taxon of $B$ lies. These are the edges that $b$ alone covers in $B$, so $\mathrm{PD}(B) - \mathrm{PD}(B - b) = \ell(P_b)$. The edges of $P_b$ form one segment from $b$ upward; let $u_b$ be the lower end of its top edge, with $u_b = b$ when $P_b$ is empty. The subtree below $u_b$ contains no taxon of $B$ other than $b$. Two subtrees of a rooted tree are nested or disjoint, and two of these subtrees cannot be nested, because the larger one would contain two taxa of $B$. So the $|B|$ subtrees below the nodes $u_b$ are pairwise disjoint. Each taxon of $A$ lies in at most one of them, and $|A| < |B|$, so some subtree below $u_b$ contains no taxon of $A$. Then $b \notin A$, and no edge of $P_b$ lies on a root path of $A$, so $\mathrm{gain}(b \mid A) \ge \ell(P_b)$. $\square$

*Theorem.* For each $k$, the first $k$ taxa $G_k$ chosen by greedy have the maximum rooted PD among all sets of $k$ taxa.

*Proof.* By induction on $k$; $G_0 = \emptyset$ is optimal. Let $G_k$ be optimal and let $B$ be an optimal set of size $k + 1$. The lemma with $A = G_k$ gives $b \notin G_k$ with $\mathrm{PD}(G_k \cup \{b\}) = \mathrm{PD}(G_k) + \mathrm{gain}(b \mid G_k) \ge \mathrm{PD}(G_k) + \mathrm{PD}(B) - \mathrm{PD}(B - b)$. Since $B - b$ has $k$ taxa, $\mathrm{PD}(B - b) \le \mathrm{PD}(G_k)$, so $\mathrm{PD}(G_k \cup \{b\}) \ge \mathrm{PD}(B)$. Greedy adds a taxon with the largest gain, so $\mathrm{PD}(G_{k+1}) \ge \mathrm{PD}(G_k \cup \{b\}) \ge \mathrm{PD}(B)$. $\square$

The lemma is an [exchange argument](/exchange-argument/). It is stronger than [submodularity](/submodular-function/) alone, which only gives the $(1 - 1/e)$ guarantee of greedy [maximum coverage](/greedy-max-coverage/).

**Greedy for $k$ taxa (unrooted).** Choose two taxa $a, b$ at maximum distance, then add taxa by largest gain (Steel 2005; Pardi and Goldman 2005). With $a$ in the set, the unrooted PD of a set is its rooted PD on the tree rooted at $a$, so the steps after the first pair are the rooted algorithm on that tree. Two passes of distance computation find the pair in $O(n)$ time.

**A faster greedy.** For each node, keep the child whose subtree holds the longest downward path, and cut the tree into paths that always follow these children. The greedy gains are the lengths of these paths, each with the edge above its top node, in decreasing order. Sorting the paths gives the whole greedy order in $O(n \log n)$ time.

**Dynamic program for budgets.** For integer costs, process the tree in postorder. For each node $v$ and each budget $b \le B$, store the largest PD of the edges in the subtree of $v$, together with the edge above $v$, over sets of taxa below $v$ with cost at most $b$, and the same value over nonempty sets. A node combines its children with a max-plus convolution over the budget, as in [knapsack DP](/knapsack-dynamic-programming/) on a tree ([tree DP](/tree-dynamic-programming/)), and adds the length of its own edge only for nonempty sets. The time is $O(nB^2)$ (Pardi and Goldman 2007).

## Bounds

- The size-constrained problem needs $\Omega(n)$ time to read the tree, and greedy with the path decomposition is within a $\log n$ factor of that.
- The budgeted problem is NP-hard, so no polynomial-time algorithm exists unless P = NP. Its hardness is weak: the DP is [pseudo-polynomial](/pseudo-polynomial-time/), polynomial when $B$ is bounded by a polynomial in $n$.

## Reductions

**From 0/1 knapsack to budgeted PD.** Given items with values $v_i$, weights $w_i$ and capacity $W$, build a star tree with one taxon per item on an edge of length $v_i$, give the taxon cost $w_i$, and set $B = W$. On a star, the PD of a set is the sum of its edge lengths, rooted or unrooted (for sets of at least two taxa). So a set of taxa within the budget is a packing with the same value, and the reverse also holds. Since the decision form of [knapsack](/knapsack-decision/) is NP-complete, budgeted PD maximization is [weakly NP-hard](/weak-np-hardness/).

**To weighted maximum coverage.** Rooted PD maximization with $k$ taxa is the case of maximum coverage in which the sets are the root paths of the taxa and the elements are the edges with weights $\ell(e)$. Here the sets of taxa below the edges form a laminar family, and this structure is what makes greedy exact.

## Applications

- **Conservation planning.** Choosing species or populations to protect so that the most evolutionary history survives, as proposed by Faith (1992).
- **Choosing species for genome sequencing.** Pardi and Goldman (2005) used greedy PD to choose the next genomes to sequence so that the comparative data cover the tree well.
- **Choosing taxa for a study.** Picking a subset of taxa that spans a large tree, for example to reduce a phylogenomic data set or to select reference sequences.

## References
