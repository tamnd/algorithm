---
title: The binary search with Bellman-Ford returns a least period legal retiming
proves: [correctness]
status: full
---

We use the notation of the page. Paths may repeat vertices. For a path $p$ from $u$ to $v$, $w(p)$ is the sum of $w(e)$ over its edges and $d(p)$ is the sum of $d(x)$ over its vertices, with $u$ and $v$ included. The empty path at $v$ has $w = 0$ and $d = d(v)$. Every cycle of $G$ has $w \ge 1$.

**Lemma 1 (paths).** For every retiming $r$ and every path $p$ from $u$ to $v$, $w_r(p) = w(p) + r(v) - r(u)$.

*Proof.* Let $p = x_0 x_1 \cdots x_k$ with $x_0 = u$ and $x_k = v$. Then $w_r(p) = \sum_{i=1}^{k} \big(w(x_{i-1}, x_i) + r(x_i) - r(x_{i-1})\big)$. The sum of the differences telescopes to $r(x_k) - r(x_0)$. For the empty path both sides are 0. $\square$

A consequence: a retiming does not change $w(C)$ for a cycle $C$, so every cycle of $G_r$ still has a register, and $c(G_r)$ is finite.

**Lemma 2 (the matrices).** Lines L1 and L2 compute $W(u, v) = \min \{ w(p) \}$ and $D(u, v) = \max \{ d(p) : w(p) = W(u, v) \}$ over the paths $p$ from $u$ to $v$, for every pair with a path.

*Proof.* Give the edge $e = (x, y)$ the pair $(w(e), -d(x))$. The sum over the edges of a path $p$ from $u$ to $v$ is $(w(p), -(d(p) - d(v)))$, since every vertex of $p$ except $v$ is the tail of exactly one edge of $p$. The empty path gives $(0, 0)$, which is also this formula. In lexicographic order, the least sum has the least $w(p)$ and, among those, the largest $d(p)$. Pairs with lexicographic order form a totally ordered group, and the sum of a cycle is at least $(1, \cdot) > (0, 0)$ because every cycle has a register. So no cycle has a negative sum, a least path sum exists and is reached by a simple path, and Floyd-Warshall computes it, by the same proof as for real weights. Line L2 reads off $W$ and $D$. $\square$

**Lemma 3 (legal).** $r$ is legal exactly when $r(u) - r(v) \le w(e)$ for every edge $e = (u, v)$.

*Proof.* This is the definition $w_r(e) = w(e) + r(v) - r(u) \ge 0$. $\square$

**Theorem 1 (Leiserson and Saxe).** Let $c \ge 0$. A retiming $r$ is legal and has $c(G_r) \le c$ exactly when it satisfies
(a) $r(u) - r(v) \le w(e)$ for every edge $e = (u, v)$, and
(b) $r(u) - r(v) \le W(u, v) - 1$ for every pair $(u, v)$ with $D(u, v) > c$.

*Proof.* Note first that $c(G_r) \le c$ means that every path $p$ with $w_r(p) = 0$ has $d(p) \le c$. Retiming does not change delays.

Assume $r$ is legal with $c(G_r) \le c$. Then (a) holds by Lemma 3. Let $D(u, v) > c$ and let $p$ be a path from $u$ to $v$ with $w(p) = W(u, v)$ and $d(p) = D(u, v)$. Since $d(p) > c$, the path has $w_r(p) \ne 0$. It has $w_r(p) \ge 0$ because $r$ is legal and $w_r(p)$ is a sum of $w_r(e) \ge 0$. So $w_r(p) \ge 1$, and Lemma 1 gives $W(u, v) + r(v) - r(u) \ge 1$, which is (b).

Assume (a) and (b). Then $r$ is legal by Lemma 3. Let $p$ be a path from $u$ to $v$ with $d(p) > c$. We show $w_r(p) \ge 1$. If $D(u, v) > c$, then by Lemma 1 and (b), $w_r(p) = w(p) + r(v) - r(u) \ge W(u, v) + r(v) - r(u) \ge 1$. If $D(u, v) \le c$, then $d(p) > D(u, v)$, so $p$ is not one of the paths with $W(u, v)$ registers, and $w(p) \ge W(u, v) + 1$. Take a path $q$ from $u$ to $v$ with $w(q) = W(u, v)$. Legality gives $w_r(q) \ge 0$, that is $r(u) - r(v) \le W(u, v)$ by Lemma 1. So $w_r(p) = w(p) + r(v) - r(u) \ge W(u, v) + 1 - W(u, v) = 1$. Every path with delay above $c$ has a register in $G_r$, so $c(G_r) \le c$. $\square$

**Lemma 4 (the test).** For a given $c$, lines L7 to L11 return a legal retiming with $r(h) = 0$ and $c(G_r) \le c$ if one exists, and report a negative cycle otherwise.

*Proof.* The system $S$ of lines L7 and L8 is a system of difference constraints with integer bounds. By the theorem on the [difference constraints](/difference-constraints/) page, Bellman-Ford from a virtual source finds a solution when the constraint graph has no negative cycle, and the system has no solution when it has one. All bounds are integers, so the distances, and the solution, are integers. Adding a constant to all $r(x)$ keeps every difference, so $r - r(h)$ is still a solution and has $r(h) = 0$. By Theorem 1, the integer solutions of $S$ with $r(h) = 0$ are exactly the legal retimings with $c(G_r) \le c$. $\square$

**Lemma 5 (candidates).** Let $c^*$ be the least period over all legal retimings. Then $c^* = D(u, v)$ for some pair $(u, v)$. Moreover the set of $c$ for which a legal retiming with period at most $c$ exists is upward closed, and it contains the largest value $c_k$ of $D$.

*Proof.* Let $r$ be legal with $c(G_r) = c^*$, and let $p$ be a path from $u$ to $v$ with $w_r(p) = 0$ and $d(p) = c^*$. For every path $q$ from $u$ to $v$, legality gives $w_r(q) \ge 0 = w_r(p)$, so by Lemma 1, $w(q) \ge w(p)$. Hence $w(p) = W(u, v)$ and $d(p) \le D(u, v)$. Let $q$ be a path from $u$ to $v$ with $w(q) = W(u, v)$ and $d(q) = D(u, v)$. By Lemma 1, $w_r(q) = w_r(p) = 0$, so $d(q) \le c(G_r) = c^*$. So $c^* = d(p) \le D(u, v) = d(q) \le c^*$.

If a retiming has period at most $c$, it has period at most every $c' \ge c$, so the set is upward closed. For $r = 0$, every path $p$ from $u$ to $v$ with $w(p) = 0$ has $W(u, v) = 0$ and $d(p) \le D(u, v) \le c_k$. So $c(G) \le c_k$ and $r = 0$ is a witness for $c_k$. $\square$

**Theorem 2.** MIN-PERIOD-RETIMING returns $c^*$ and a legal retiming $r$ with $r(h) = 0$ and $c(G_r) = c^*$.

*Proof.* Let $j$ be the least index with $c_j$ feasible. By Lemma 5, $j$ exists, $c_j = c^*$ (since $c^*$ is among the values and no smaller value is feasible), and $c_i$ is feasible exactly when $i \ge j$. The loop keeps the invariant $lo \le j \le hi$, and best_r is a legal retiming with $r(h) = 0$ and period at most $c_{hi}$. At the start, $lo = 1$, $hi = k$, and best_r $= 0$ meets $c_k$ by Lemma 5. In a probe, Lemma 4 decides whether $c_{mid}$ is feasible. If not, $mid < j$ and $lo \leftarrow mid + 1$ keeps $lo \le j$. If so, $j \le mid$, and $hi \leftarrow mid$ with the new witness keeps the invariant. Each probe shrinks $hi - lo$, since $lo \le mid < hi$, so the loop stops with $lo = hi = j$. Then best_r is legal with period at most $c_j = c^*$, and no legal retiming has a smaller period, so its period is exactly $c^*$. $\blacksquare$

**Termination.** Floyd-Warshall and Bellman-Ford stop after a fixed number of rounds, and the loop of line L5 runs at most $\lceil \log_2 k \rceil$ times.
