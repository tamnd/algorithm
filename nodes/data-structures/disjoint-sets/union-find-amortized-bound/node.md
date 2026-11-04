---
tag: 5XSYZ5
kind: theorem
slug: union-find-amortized-bound
name: Tarjan's union-find bound
aliases:
- union-find amortized analysis
- O(m alpha(m,n)) bound
area: data-structures/disjoint-sets
level: core
summary: A sequence of m operations on n elements with union by rank and path compression takes O(m alpha(m,n)) time.
prereqs: [disjoint-set-forest, union-by-rank, path-compression, inverse-ackermann-function, potential-method]
see_also: [union-find-lower-bound, hopcroft-ullman-log-star-bound, fredman-saks-lower-bound, ackermann-function, path-halving, path-splitting, amortized-cost]
sources:
  - paper: doi:10.1145/321879.321884
    title: "Robert Endre Tarjan, Efficiency of a Good But Not Linear Set Union Algorithm, Journal of the ACM 22(2) (1975), 215-225"
    locator: the main theorem (upper bound O(m alpha(m, n))) and the matching lower bound for this algorithm
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.4, Analysis of union by rank with path compression (the functions A_k, level, iter, the potential function and the amortized costs)
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: the bounds for linking by rank or size with compression, splitting and halving
  - paper: doi:10.1137/S0097539703439088
    title: "Raimund Seidel and Micha Sharir, Top-down analysis of path compression, SIAM Journal on Computing 34(3) (2005), 515-525"
    locator: the top-down proof of the O(m alpha(m, n)) bound
---

Tarjan's union-find bound states that a [disjoint-set forest](/disjoint-set-forest/) with [union by rank](/union-by-rank/) and [path compression](/path-compression/) runs any sequence of $m$ operations on $n$ elements in $O(m\,\alpha(m, n))$ time, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). Since $\alpha(n) \le 4$ for every $n$ up to $2^{2048}$, the amortized cost of one operation is a small constant in practice, but it is not constant in theory. Tarjan proved it in 1975, together with a matching lower bound for this algorithm. The CLRS form $O(m\,\alpha(n))$ has a short proof by the [potential method](/potential-method/), which this page gives in full.

## Statement

Let a [disjoint-set forest](/disjoint-set-forest/) use [union by rank](/union-by-rank/) and full [path compression](/path-compression/), and start empty.

**Theorem (CLRS, Section 19.4).** A sequence of $m$ operations MAKE-SET, UNION and FIND, of which $n$ are MAKE-SET, takes $O(m\,\alpha(n))$ time in the worst case. So each operation costs $O(\alpha(n))$ amortized time.

**Theorem (Tarjan, 1975).** For $n$ elements, at most $n - 1$ unions and $m \ge n$ finds, the total time is $O(m\,\alpha(m, n))$, with the two-argument inverse $\alpha(m, n)$ of the inverse Ackermann page. There are sequences of this shape on which the algorithm takes $\Omega(m\,\alpha(m, n))$ time.

The model is the [word RAM](/word-ram/), or the [pointer machine](/pointer-machine/): each step reads or writes one parent or rank field. The bound is amortized: one find can still cost $\Theta(\log n)$.

The two-argument form is sharper. Since $\alpha(m, n)$ falls as $m/n$ grows, with the definition of the inverse Ackermann page it equals 1 when $m \ge n(\lg\lg n + 1)$, and the bound is then $O(m)$, while $\alpha(n)$ does not depend on $m$. Tarjan and van Leeuwen (1984) proved the same bound for [union by size](/union-by-size/) in place of rank and for [path halving](/path-halving/) or [path splitting](/path-splitting/) in place of compression.

## In plain words

A find walks from a node to the root of its tree. The walk may be long, but each walk also gives each node it passes a shortcut to the root.

The proof gives each node a store of credit, and a walk pays for most of its steps out of these stores. A node's credit depends on how far its parent is above it, measured on a scale that grows faster than any tower of powers. Each shortcut moves a node's parent much higher on that scale, so the node spends some credit. Only a handful of nodes on each walk cannot pay: at most one for each step of the scale, plus two. The scale has so few steps for any real input that each walk costs only a few steps of its own, and the credit pays for the rest.

## Proof

The full proof is in [the proof of the bound](proofs/main.md). It is the argument of CLRS, Section 19.4, and it proves the form $O(m\,\alpha(n))$. Here is its outline.

1. **Reduce to three operations.** A UNION is two FINDs and one LINK of two roots. So $m$ operations become at most $3m$ operations MAKE-SET, LINK and FIND.
2. **Facts about ranks.** Ranks increase strictly along each path, a rank changes only at a root, each rank is at most $\lfloor \lg n \rfloor$, and the rank of the parent of a node never falls.
3. **Level and iterate.** For a non-root $x$ of rank at least 1, $\mathrm{level}(x)$ is the largest $k$ with $x.p.rank \ge A_k(x.rank)$, and $\mathrm{iter}(x)$ is the largest $i$ with $x.p.rank \ge A_{\mathrm{level}(x)}^{(i)}(x.rank)$. Then $0 \le \mathrm{level}(x) < \alpha(n)$ and $1 \le \mathrm{iter}(x) \le x.rank$.
4. **Potential.** A root, or a node of rank 0, has potential $\alpha(n) \cdot rank$. Any other node has potential $(\alpha(n) - \mathrm{level}) \cdot rank - \mathrm{iter}$. Each potential is between 0 and $\alpha(n) \cdot rank$, and the potential of a non-root never grows. It falls by at least 1 when its level or its iterate changes.
5. **Amortized costs.** MAKE-SET costs $O(1)$. LINK raises the potential of the new root by at most $\alpha(n)$, so it costs $O(\alpha(n))$. In a FIND on a path of $s$ nodes, each node $x$ that has a later non-root node of the same level gets a new parent of rank at least $A_k^{(\mathrm{iter}(x) + 1)}(x.rank)$, so its potential falls. Only the root, a node of rank 0 and the last node of each level fail this, at most $\alpha(n) + 2$ nodes. So a FIND costs $O(\alpha(n))$ amortized.
6. **Sum.** The total potential starts at 0 and stays non-negative, so the total time is at most the sum of the amortized costs, $O(m\,\alpha(n))$. $\blacksquare$

**A potential in numbers.** Let $n \le 2047$, so $\alpha(n) \le 3$, and take $\alpha(n) = 3$. Let $x$ have rank 2 and its parent rank 5. Then $A_0(2) = 3 \le 5$, $A_1(2) = 5 \le 5$ and $A_2(2) = 23 > 5$, so $\mathrm{level}(x) = 1$. Next $A_1^{(1)}(2) = 5 \le 5$ and $A_1^{(2)}(2) = A_1(5) = 11 > 5$, so $\mathrm{iter}(x) = 1$. The potential is $(3 - 1) \cdot 2 - 1 = 3$. If a find gives $x$ a parent of rank 11 or more, its iterate becomes 2 and the potential falls to 2; a parent of rank 23 or more raises its level to 2, and the potential falls to $1 \cdot 2 - 1 = 1$ or less.

Tarjan's original proof of the two-argument form, and of the lower bound for this algorithm, uses a different decomposition. Seidel and Sharir (2005) gave a short top-down proof of the $O(m\,\alpha(m, n))$ bound, which splits the forest by rank into a top and a bottom part and recurses on both.

## Consequences

- **Union-find is almost linear.** Each algorithm that does $O(m)$ union-find operations runs in $O(m\,\alpha(n))$ time for them. This covers [Kruskal's algorithm](/kruskal/), whose total time is then dominated by the sort of the edges, [connected components](/connected-components/) of a graph given as a stream of edges, [incremental connectivity](/incremental-connectivity/), [Tarjan's offline LCA algorithm](/tarjan-offline-lca/), [offline minimum](/offline-minimum/) and [connected component labeling](/connected-component-labeling/).
- **The bound is optimal.** The [union-find lower bound](/union-find-lower-bound/) of Fredman and Saks shows that every structure in the cell-probe model with words of $O(\log n)$ bits needs $\Omega(m\,\alpha(m, n))$ time on some sequence. So the forest is optimal up to a constant factor. The method behind that proof is on the [Fredman-Saks lower bound](/fredman-saks-lower-bound/) page.
- **Earlier bounds.** The [Hopcroft-Ullman bound](/hopcroft-ullman-log-star-bound/) $O(m \lg^* n)$ follows from the same kind of argument with a coarser scale, and it is weaker: $\lg^* n$ grows faster than $\alpha(n)$.
- **Amortized only.** The bound does not hold after an undo. Structures that roll back unions, such as [union-find with rollback](/union-find-with-rollback/), drop path compression and pay $O(\log n)$ per find.

## Tightness

**For this algorithm.** Tarjan (1975) built sequences of $n - 1$ unions and $m \ge n$ finds on which union by rank with path compression takes $\Omega(m\,\alpha(m, n))$ time. So the analysis cannot be improved for this algorithm, and Tarjan's title calls it "good but not linear".

**For each algorithm.** The [union-find lower bound](/union-find-lower-bound/) extends this to all data structures in the cell-probe model.

**One operation.** The amortized bound does not bound one operation. The tournament of unions on $2^k$ elements of the [union by rank](/union-by-rank/) page builds a tree with a leaf at depth $k$, and the first find of that leaf takes $k = \lg n$ steps. A sequence that keeps building such trees and finds each deep leaf once has finds of cost $\Theta(\log n)$, but the many unions that build each tree pay for them in the sum.

**Each rule alone is worse.** Union by rank alone costs $\Theta(m \log n)$ in the worst case, by the same tournament with repeated finds of the deep leaf. Path compression alone costs $\Theta(n + f \log_{2 + f/n} n)$ for $f$ finds, which is $\Theta(n \log n)$ for $f = n$ (Tarjan and van Leeuwen; CLRS, Section 19.3).

## History

Galler and Fischer (1964) introduced the forest of parent pointers. Union by rank or size and path compression were in use by the early 1970s. Hopcroft and Ullman (1973) proved the bound $O(m \lg^* n)$. Tarjan (1975) proved the upper bound $O(m\,\alpha(m, n))$ and a matching lower bound for this algorithm. Tarjan and van Leeuwen (1984) extended the bounds to the other linking and compaction rules. CLRS gives the potential proof of this page, and the history of the analysis in the notes of Chapter 19. Seidel and Sharir (2005) gave a top-down proof. Fredman and Saks (1989) proved that no data structure does better.

## References
