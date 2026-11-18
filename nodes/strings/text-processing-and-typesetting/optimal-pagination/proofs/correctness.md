---
title: The pagination dynamic program returns a pagination of least cost
proves: [correctness, termination, complexity]
status: full
---

We use the model and the pseudocode of the page. The lines have heights $h_1, \ldots, h_n \ge 0$, the figures have heights $f_1, \ldots, f_m \ge 0$, figure $t$ is referenced from line $r_t$ with $1 \le r_1 \le \cdots \le r_m \le n$, and $R(i)$ is the number of figures with $r_t \le i$. A **state** is a pair $(i, j)$ with $0 \le i \le n$ and $0 \le j \le m$. A pagination with $P$ pages is a sequence of states $(0, 0) = s_0, s_1, \ldots, s_P = (n, m)$ with $s_k = (i_k, j_k)$, $i_{k-1} \le i_k$, $j_{k-1} \le j_k$ and $s_{k-1} \ne s_k$. Page $k$ holds the lines $i_{k-1} + 1, \ldots, i_k$ and the figures $j_{k-1} + 1, \ldots, j_k$, and its height is $u_k$, the sum of their heights. The pagination is **valid** if $u_k \le H$ for every $k$ and every figure is on the page of its reference or later. Its cost is

$$\mathrm{cost} = \sum_{k=1}^{P-1} (H - u_k)^2 + \sum_{x} \pi_x + \alpha \sum_{t=1}^{m} \bigl(p(t) - q(r_t)\bigr),$$

where the middle sum is over the lines $x$ with $1 \le x < n$ such that line $x + 1$ is on a later page than line $x$, $p(t)$ is the page of figure $t$ and $q(x)$ is the page of line $x$.

**Lemma 1 (validity is local).** Every figure is on the page of its reference or later if and only if $j_k \le R(i_k)$ for every $k$.

*Proof.* Since the references are sorted, $R(i) \ge t$ holds exactly when $r_t \le i$. Suppose that $j_k \le R(i_k)$ for all $k$, and let figure $t$ be on page $k$, so $t \le j_k \le R(i_k)$. Then $r_t \le i_k$, so line $r_t$ is on page $k$ or earlier. Conversely, suppose that every figure is on the page of its reference or later, and take $k$ with $j_k \ge 1$. Figure $j_k$ is on a page $k' \le k$, so its reference line is on a page $\le k$, and $r_{j_k} \le i_k$. Hence $R(i_k) \ge j_k$. $\square$

**Lemma 2 (the cost splits over the pages).** For a valid pagination, the cost is $\sum_{k=1}^{P-1} \ell(s_{k-1}, s_k)$, where

$$\ell\bigl((i, j), (i', j')\bigr) = (H - u)^2 + [\, i < i' < n \,]\, \pi_{i'} + \alpha \bigl(R(i') - j'\bigr)$$

and $u$ is the height of the page from $(i, j)$ to $(i', j')$.

*Proof.* The first terms agree by definition. For the penalties: let $1 \le x < n$. Line $x + 1$ is on a later page than line $x$ exactly when line $x$ is the last line of its page $k$, that is, $x = i_k$ and $i_{k-1} < i_k$; then $k < P$, since line $x + 1$ comes later. So each such $x$ is counted once, by the page $k$ with $i_{k-1} < i_k = x < n$, and no other page adds a penalty. For the figures: $p(t) - q(r_t)$ is the number of $k$ with $q(r_t) \le k < p(t)$, which is the number of $k$ with $1 \le k \le P - 1$, $r_t \le i_k$ and $t > j_k$. Summed over $t$, this is $\sum_{k=1}^{P-1} \#\{t : r_t \le i_k,\ t > j_k\}$. By Lemma 1 and the sorted references, every $t \le j_k$ has $r_t \le i_k$, so the set has $R(i_k) - j_k$ elements. $\square$

**The DAG.** Put an edge from the state $s$ to the state $s' \ne s$ when $s \le s'$ in both coordinates, the page from $s$ to $s'$ has height at most $H$, and $j' \le R(i')$. Its weight is $\ell(s, s')$ if $s' \ne (n, m)$ and 0 if $s' = (n, m)$. By Lemmas 1 and 2, the valid paginations are exactly the paths from $(0, 0)$ to $(n, m)$ in this DAG, and the cost of a pagination is the weight of its path: every state on a path other than the last one is not $(n, m)$, since no edge leaves $(n, m)$. Every edge goes to a state that is later in the lexicographic order, so this order is a topological order.

**Lemma 3 (all edges are seen).** When lines L5 to L9 run for the state $(i, j)$, they relax every edge that leaves $(i, j)$, and only such edges.

*Proof.* Heights are $\ge 0$, so the height of the lines $i + 1, \ldots, i'$ does not decrease when $i'$ grows, and the loop of line L5 stops only when no larger $i'$ can give a page that fits. For a fixed $i'$, the height $u$ of the page does not decrease when $j'$ grows and $R(i')$ is fixed, so the loop of line L6 stops only when no larger $j'$ gives an edge. Line L7 skips $s' = s$. Every pair $(i', j')$ that reaches line L8 satisfies the three conditions of an edge, and line L8 adds its weight. $\square$

**Theorem.** The algorithm terminates. It returns the least cost of a valid pagination and a pagination with this cost, or failure when no valid pagination exists.

*Proof.* The loops are finite. The states are processed in lexicographic order, which is topological, and by Lemma 3 each state relaxes all its outgoing edges. By the standard argument for [shortest paths in a DAG](/dag-shortest-paths/), when the state $s$ is processed, $C[s]$ is the least weight of a path from $(0, 0)$ to $s$: all edges into $s$ come from earlier states, which were processed with their final values. So $C[n][m]$ is the least cost of a valid pagination, or $\infty$ when there is none, and then line L10 reports failure. The links $P$ store the last edge of a best path to each state, so line L11 rebuilds a path whose weight is $C[n][m]$. $\square$

**Complexity.** There are $(n + 1)(m + 1)$ states, and each state has at most $(n + 1)(m + 1)$ edges, each relaxed in $O(1)$ time with prefix sums. So the time is $O(n^2 m^2)$ and the space is $O(n m)$. If every page holds at most $a$ lines and $b$ figures, for example because every height is at least 1 and $H$ is fixed, a state has at most $(a + 1)(b + 1)$ edges and the time is $O(n m a b)$.
