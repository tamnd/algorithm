---
title: Yen's algorithm lists the k shortest simple paths in order
proves: [correctness, termination]
status: full
---

Let $G$ be a directed graph with nonnegative weights (parallel arcs merged to the lightest, self-loops dropped), and $s, t$ vertices. A *path* means a simple path from $s$ to $t$, written as its list of vertices indexed from 0. For a path $p$, $p[0..i]$ is its prefix with $i + 1$ vertices. Line numbers refer to YEN on the main page. Let $\mathcal{A}_k = \{A_1, \ldots, A_k\}$.

**Fact 1 (candidates are new simple paths).** Every path added to $B$ at line L9 is a simple $s$-$t$ path, and when it is added it is not in $A$.

*Proof.* The candidate is the root $A_{k-1}[0..i]$ followed by a spur path $P$ from the spur vertex $A_{k-1}[i]$ to $t$. The root is simple, as a prefix of a simple path. $P$ is a shortest path found by Dijkstra, so it is simple, and by line L7 it avoids the root vertices other than the spur. So the candidate is simple and ends at $t$. Line L9 skips paths that are already in $A$ or $B$. $\square$

**Fact 2 (weights).** The key of a candidate in $B$ is its weight, and Dijkstra at line L8 returns a lightest spur path in the graph with the blocked arcs and vertices removed.

*Proof.* The weights are nonnegative, and Dijkstra is correct on such graphs. The key is the weight of the root plus the weight of the spur path. $\square$

**Lemma 3 (every other path has a cheaper candidate in $B$).** At line L11 in round $k$, for every path $P \notin \mathcal{A}_{k-1}$, the queue $B$ contains a path $C$ with $w(C) \le w(P)$.

*Proof.* For $q \in \mathcal{A}_{k-1}$, let $\ell(q)$ be the number of leading vertices that $q$ and $P$ have in common. Both start with $s$, so $\ell(q) \ge 1$. Let $L = \max_q \ell(q)$, and let $j$ be the largest index with $\ell(A_j) = L$. Set $i = L - 1$, so $P[0..i] = A_j[0..i]$ and $P[i+1] \ne A_j[i+1]$ or one of them ends at index $i$. Neither path can end at index $i$ unless both do: a path that ends there ends at $t$, and the other path, being simple, contains $t$ only as its last vertex, so it would end there too and they would be equal, but $P \ne A_j$. So $i \le |A_j| - 2$ and $P[i+1] \ne A_j[i+1]$.

Spur $i$ of $A_j$ was computed in round $j + 1 \le k$ (rounds $2, \ldots, k$ compute the spurs of $A_1, \ldots, A_{k-1}$). In that round, line L6 blocked the arcs $(P[i], q[i+1])$ for the paths $q \in \mathcal{A}_j$ with $q[0..i] = P[0..i]$. The arc $(P[i], P[i+1])$ is not among them: if $q[i+1] = P[i+1]$ for such a $q$, then $\ell(q) \ge L + 1$, which contradicts the choice of $L$. Line L7 blocked $P[0..i-1]$, and the part $P[i..]$ avoids these vertices, because $P$ is simple. So $P[i..]$ is a spur path in the graph of line L8, and by Fact 2 Dijkstra found a spur path of weight at most $w(P[i..])$. The resulting path $C = P[0..i]$ followed by that spur path has $w(C) \le w(P)$.

$C$ was added to $B$ then, or it was already in $A$ or $B$. It is not in $\mathcal{A}_{k-1}$: since $C[0..i] = P[0..i]$ and $C[i+1]$ is not blocked, $C$ differs from every $q \in \mathcal{A}_j$ with that prefix, and paths in $\mathcal{A}_j$ without that prefix differ from $C$ anyway; and if $C = A_l$ with $j < l \le k - 1$, then $\ell(A_l) \ge L$, so $\ell(A_l) = L$ with $l > j$, against the choice of $j$. Paths leave $B$ only at line L12, into $A$, so $C$ is still in $B$. $\square$

**Theorem.** YEN returns distinct simple $s$-$t$ paths $A_1, \ldots, A_{k'}$, with $k' = \min(K, N)$ where $N$ is the number of simple $s$-$t$ paths, such that for every $j$, $A_j$ is a lightest path outside $\mathcal{A}_{j-1}$. In particular $w(A_1) \le \cdots \le w(A_{k'})$.

*Proof.* If $t$ is not reachable, there is no path, $N = 0$, and line L1 returns the empty list. Otherwise $A_1$ is a shortest $s$-$t$ path from Dijkstra, a simple path of least weight among all walks and so among all paths.

In round $k$, by Fact 1 every element of $B$ is a path outside $\mathcal{A}_{k-1}$. If some path $P$ lies outside $\mathcal{A}_{k-1}$, Lemma 3 says $B$ is not empty, so line L11 does not stop, and line L12 takes $A_k$ with $w(A_k) \le w(C) \le w(P)$. So $A_k$ is a lightest path outside $\mathcal{A}_{k-1}$, and it is new. If no path lies outside $\mathcal{A}_{k-1}$, then $B$ is empty by Fact 1 and line L11 returns, with $k - 1 = N$. Since $A_{j+1}$ is outside $\mathcal{A}_{j}$ and therefore outside $\mathcal{A}_{j-1}$, the minimality of $A_j$ gives $w(A_j) \le w(A_{j+1})$. $\square$

**Termination.** Each round runs at most $n - 1$ spur computations, each a run of Dijkstra, which terminates. There are at most $K - 1$ rounds. $\blacksquare$
