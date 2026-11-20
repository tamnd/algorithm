---
tag: 53J5ZB
kind: theorem
slug: edmonds-pruhs-lower-bound
name: Lower bound for proportional cake cutting
aliases:
- Edmonds-Pruhs lower bound
area: algorithmic-game-theory/fair-division
level: advanced
summary: Every deterministic proportional cake cutting protocol needs Omega(n log n) queries in the Robertson-Webb model, so Even-Paz is optimal.
prereqs: [robertson-webb-query-model, even-paz-algorithm, adversary-argument]
see_also: [proportional-division, cake-cutting-problem, comparison-sort-lower-bound, yao-minimax-principle, decision-tree-model, lower-bound, last-diminisher, stromquist-impossibility-theorem]
sources:
  - paper: doi:10.1145/2000807.2000819
    title: Jeff Edmonds and Kirk Pruhs, Cake cutting really is not a piece of cake, ACM Transactions on Algorithms 7(4) (2011)
    locator: Article 51; Section 2 (the thin-rich game, value trees, Lemma 3 and Theorem 4), Section 3 (the randomized bound with approximate queries)
  - paper: "Jeff Edmonds and Kirk Pruhs, Cake cutting really is not a piece of cake, Proceedings of the 17th ACM-SIAM Symposium on Discrete Algorithms (SODA 2006), 271-278"
    locator: the conference version of the same results
  - paper: doi:10.1016/j.disopt.2006.07.003
    title: Gerhard J. Woeginger and Jiri Sgall, On the complexity of cake cutting, Discrete Optimization 4(2) (2007)
    locator: pp. 213-220 (the Omega(n log n) bound for protocols that give connected pieces)
  - paper: doi:10.1016/0166-218X(84)90005-2
    title: Shimon Even and Azaria Paz, A note on cake cutting, Discrete Applied Mathematics 7(3) (1984)
    locator: pp. 285-296 (the matching O(n log n) protocol)
  - paper: "Stephen Arndt, Benjamin Moseley, Sungjin Im and Kirk Pruhs, No, Cake Cutting Really is a Piece of Cake, arXiv:2606.07238 (preprint, June 2026)"
    locator: the abstract and the open question on protocols with O(n) cut queries
---

The Edmonds-Pruhs lower bound states that every deterministic protocol for [proportional division](/proportional-division/) of a [cake](/cake-cutting-problem/) among $n$ agents makes $\Omega(n \log n)$ queries in the [Robertson-Webb query model](/robertson-webb-query-model/). It holds even if the pieces may be unions of intervals, and even if each agent gets only a fraction of its fair share. So the [Even-Paz algorithm](/even-paz-algorithm/), with $O(n \log n)$ queries, is optimal up to a constant factor. The proof is an [adversary argument](/adversary-argument/): each agent must find a narrow piece of high value, and an adversary hides such pieces deep in a tree.

## Statement

The cake is $[0, 1]$, and agent $i \in \{1, \dots, n\}$ has a nonnegative, additive and nonatomic valuation $V_i$ with $V_i([0, 1]) = 1$. A protocol asks $\mathrm{Eval}_i(x, y) = V_i([x, y])$ and $\mathrm{Cut}_i(x, \alpha)$ queries with exact answers. For $c \ge 1$, a protocol is $c$-fair if it gives each agent $i$ a piece $X_i$, a finite union of intervals, with $V_i(X_i) \ge 1/(cn)$, and the pieces are disjoint.

**Theorem (Edmonds and Pruhs).** Every deterministic $c$-fair protocol makes $\Omega(n(\log n - \log c))$ queries in the worst case.

For $c = 1$ this is the bound $\Omega(n \log n)$ for proportional division. For $c = n^{1 - \delta}$ with a fixed $\delta > 0$, it is still $\Omega(\delta n \log n)$. The bound is Theorem 4 of the journal version.

## In plain words

Think of a long cake. Most agents must get a narrow piece, because the pieces cannot overlap and the cake has only so much room. A narrow piece is fair only if it holds a lot of value for its owner. So each agent must find a narrow and valuable spot in its own cake.

The proof builds cakes in which such spots are well hidden. The value is spread over a tree of nested intervals, and at each split one part gets more value than the others. An adversary decides which part is the rich one only when the protocol looks there. Each question shows only a little of the tree, so the protocol must ask many questions for each agent before it can be sure that a narrow piece is valuable.

## Proof

The proof has three steps: a game for one agent, a family of valuations given by trees, and an adversary for the game. We follow Section 2 of the journal version and assume that $n \ge 6$ and $n/2$ is a power of 3; other values of $n$ change only the constants.

**Step 1. The thin-rich game.** A piece is *thin* if its total width is at most $2/n$, and *rich* for agent $i$ if $V_i$ gives it at least $1/(cn)$. In the thin-rich game, a protocol talks to one agent and must output a thin piece that is rich for it, and it must be correct for every valuation that agrees with the answers.

The game is part of every $c$-fair division. The pieces $X_1, \dots, X_n$ are disjoint in $[0, 1]$, so fewer than $n/2$ of them can have width more than $2/n$; at least $n/2$ agents get thin pieces, and each of these pieces is rich for its owner. So a $c$-fair protocol solves the thin-rich game for at least $n/2$ agents at once.

**Step 2. Value trees.** Take a balanced tree in which each internal node has three children, with $n/2$ leaves and depth $L = \log_3(n/2)$. The leaves, from left to right, stand for the intervals $[2(j-1)/n, 2j/n]$ of width $2/n$, and an internal node stands for the union of the leaves below it. Of the three edges from a node to its children, two are *light* with label $1/4$ and one is *heavy* with label $1/2$. The value of a node is the product of the labels on its path from the root, and the value of a leaf is spread evenly over its interval. Since $1/4 + 1/4 + 1/2 = 1$, this defines a valuation with total 1.

A leaf $u$ whose path has $q(u)$ heavy edges has value $2^{-q(u)} 4^{-(L - q(u))} = 2^{q(u) - 2L}$. With $n = 2 \cdot 3^L$, the leaf is rich exactly when
$$q(u) \ge L \log_2(4/3) - \log_2(2c).$$
So a rich leaf needs a path with a constant fraction of heavy edges, about $0.415 L$, less a term of $\log_2 c$. The value of a thin piece is at most its width $2/n$ times the largest density of a leaf that it meets. So a thin rich piece meets a leaf of density at least $1/(2c)$, and such a leaf has value at least $1/(cn)$, so it is rich. Edmonds and Pruhs show (their Lemma 1) that a protocol can be made, with $O(1)$ more queries, to name such a leaf. So we may assume that a protocol for the game outputs a leaf and must be sure that it is rich.

**Step 3. The adversary.** The adversary fixes the labels of the tree only when it must. When a query touches a point $x$, it reveals the path from the root to the leaf of $x$: every unrevealed edge on that path gets the label light, and at each node of the path one of the other two edges gets heavy and the other light. For a cut query $\mathrm{Cut}(x_1, \alpha)$, it also reveals the path toward the answer $x_2$, and it chooses the labels so that this path, too, uses only light edges. After this, the revealed labels determine the answer to the query (Lemma 2 of the paper).

Each query reveals at most two such forked paths. A root-to-leaf path follows a forked path along light edges and leaves it by at most one edge, which may be heavy. So each query adds at most two revealed heavy edges to any root-to-leaf path, and after $k$ queries every such path has at most $2k$ revealed heavy edges.

Suppose the protocol stops after fewer than $(L \log_2(4/3) - \log_2(2c))/2$ queries and names a leaf $u$. At most $2k$ heavy edges on the path to $u$ are revealed, fewer than a rich leaf needs. The adversary labels every unrevealed edge on this path light, which agrees with all answers so far, and $u$ is not rich. So the protocol was wrong, and the thin-rich game needs $\Omega(L - \log c) = \Omega(\log n - \log c)$ queries. This is Lemma 3 of the paper.

**Putting the steps together.** Give each agent its own value tree and run a separate adversary for each agent, which answers a query to agent $i$ using only the earlier queries to agent $i$. If the protocol stops before at least $n/2$ agents have each received $\Omega(\log n - \log c)$ queries, then by Step 1 some agent with a thin piece got fewer queries than Step 3 needs, and its adversary can make that piece poor. So the protocol makes $\Omega(n(\log n - \log c))$ queries. $\blacksquare$

## Consequences

- **Even-Paz is optimal.** The [Even-Paz algorithm](/even-paz-algorithm/) uses at most $2n \lceil \lg n \rceil - n$ queries, so the deterministic query complexity of proportional division is $\Theta(n \log n)$.
- **The quadratic protocols are not.** The [last diminisher](/last-diminisher/) and the [Dubins-Spanier moving knife](/dubins-spanier-moving-knife/) use $\Theta(n^2)$ queries, which is more than needed.
- **Unions of intervals do not help.** Woeginger and Sgall had proved $\Omega(n \log n)$ only for connected pieces. Here the pieces may be any finite unions of intervals.
- **Approximation does not help much.** Asking only for $1/(cn)$ instead of $1/n$ keeps the bound $\Omega(n \log n)$ for every $c \le n^{1 - \delta}$.
- **Envy-freeness costs at least as much.** An envy-free allocation of the whole cake is proportional, so every envy-free protocol also needs $\Omega(n \log n)$ queries. Procaccia later proved $\Omega(n^2)$ for envy-free protocols.
- **The same shape as sorting.** The bound and its proof by adversary resemble the [comparison sorting lower bound](/comparison-sort-lower-bound/), and Even-Paz plays the role of merge sort.

## Tightness

The bound is tight for deterministic protocols: Even-Paz matches it up to a constant factor, with connected pieces.

It does not hold in the same form for randomized protocols with exact queries. In the thin-rich game, a protocol can choose a random $j$ and ask for the piece between $\mathrm{Cut}(0, j/n)$ and $\mathrm{Cut}(0, (j+1)/n)$; this piece has value $1/n$, and it is thin with probability at least $1/2$, with two queries. Even and Paz gave a randomized proportional protocol with $O(n)$ expected cut queries. In Section 3, Edmonds and Pruhs prove an $\Omega(n \log n)$ lower bound for randomized protocols when the answers are only approximate, by [Yao's principle](/yao-minimax-principle/) and a random value tree.

The bound counts all queries. A 2026 preprint by Arndt, Moseley, Im and Pruhs gives a deterministic proportional protocol with $O(n)$ cut queries and $O(n^2)$ eval queries, so the cuts alone need not grow as $n \log n$. They ask whether every protocol with $O(n)$ cuts must use $\Omega(n^2)$ evals. Another 2026 preprint, by Arndt, Pruhs and Tran (arXiv:2605.21829), proves an $\Omega(n \log n)$ lower bound for randomized protocols that give connected pieces.

## History

Even and Paz (1984) gave the $O(n \log n)$ protocol, and the question of a matching lower bound stayed open for two decades. Woeginger and Sgall proved $\Omega(n \log n)$ for protocols that give connected pieces, in a paper that also stated the Robertson-Webb model formally (Discrete Optimization, 2007). Edmonds and Pruhs presented the general bound at SODA 2006 under the title "Cake cutting really is not a piece of cake", and the journal version appeared in ACM Transactions on Algorithms in 2011. The 2026 preprint "No, Cake Cutting Really is a Piece of Cake" answers this title with its protocol of $O(n)$ cuts.

## References
