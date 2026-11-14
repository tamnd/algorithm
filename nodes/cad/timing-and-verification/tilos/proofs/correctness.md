---
title: TILOS returns only sizings that meet the target, stops after a bounded number of steps, and is not optimal
proves: [soundness, termination, complexity, posynomial delay, non-optimality]
status: full
---

**Model.** The circuit is a DAG of gates $0, \dots, n - 1$ in topological order, with $m$ edges. Gate $i$ has a size $x_i$ from a finite increasing list $\mathcal S_i$, and constants $p_i \ge 0$, $r_i, c_i, a_i > 0$ and $f_i \ge 0$. Its delay is
$$ D_i(x) = p_i + \frac{r_i}{x_i} \Big( f_i + \sum_{j \in \mathrm{out}(i)} c_j x_j \Big). $$
The arrival time is $A_i = D_i$ for a gate without fanins and $A_i = \max_{k \in \mathrm{in}(i)} A_k + D_i$ otherwise. The circuit delay is $\Delta(x) = \max_i A_i$ and the area is $\sum_i a_i x_i$. Given a target $T$, the problem is to find sizes with $\Delta(x) \le T$ and least area. TILOS starts at the smallest sizes. While $\Delta(x) > T$, it takes a critical path $P$, and over the gates $g \in P$ that are not at their largest size it computes the gain $G_g = \sum_{h \in P} D_h(x) - \sum_{h \in P} D_h(x')$, where $x'$ moves $g$ one step up its list. It moves up the gate with the largest positive ratio $G_g / (a_g (x'_g - x_g))$, and it stops with failure if no gain is positive.

**Lemma 1 (critical path).** Let $P = (g_1, \dots, g_\ell)$ be found by starting at a gate of largest arrival and following, from each gate, the fanin that sets its arrival time, until a gate without fanins. Then $P$ is a path of the DAG from a gate without fanins, and $\sum_{h \in P} D_h(x) = \Delta(x)$.

*Proof.* By the recurrence, $A_{g_{k+1}} = A_{g_k} + D_{g_{k+1}}$ for each step and $A_{g_1} = D_{g_1}$. Summing gives $A_{g_\ell} = \sum_k D_{g_k}$, and $A_{g_\ell} = \Delta(x)$ by the choice of $g_\ell$. $\square$

**Lemma 2 (the gain is local).** Moving gate $g$ up changes only $D_g$ and the delays $D_k$ of the fanins $k$ of $g$. So $G_g$ is the change of $D_g$ plus the change of $D_k$ over the fanins $k$ of $g$ that lie on $P$, and with a mark on the gates of $P$ it is computed in $O(1 + |\mathrm{in}(g)|)$ time.

*Proof.* $x_g$ appears in $D_g$ through $r_g / x_g$ and in $D_k$ for $k \in \mathrm{in}(g)$ through the load term $c_g x_g$, and nowhere else. The other terms of the path sum do not change. The predecessor of $g$ on $P$ is one such fanin, but an earlier gate of $P$ can also be a fanin of $g$, so all fanins on $P$ must be counted. $\square$

**Theorem 1 (soundness).** If TILOS returns sizes $x$, then $x_i \in \mathcal S_i$ for all $i$ and $\Delta(x) \le T$. If no assignment meets $T$, TILOS returns failure.

*Proof.* Each move takes the next entry of $\mathcal S_g$, so all sizes stay in their lists. TILOS returns sizes only when the test $\Delta(x) \le T$ holds. If no assignment meets $T$, that test never holds, and by Theorem 2 the loop ends, so it ends with failure. $\square$

**Theorem 2 (termination and time).** TILOS makes at most $K = \sum_i (|\mathcal S_i| - 1)$ moves, and runs in $O(K (n + m))$ time.

*Proof.* Each move raises the position of one gate in its list by one, and no move lowers a position, so the sum of the positions grows by one per move and is at most $K$. Each round computes all arrival times in $O(n + m)$, traces the path in $O(n)$, and by Lemma 2 computes all gains on the path in $O(n + m)$ in total. $\square$

**Lemma 3 (the delay is a posynomial).** For continuous sizes $x > 0$, each $D_i$ is a posynomial, and with $x_i = e^{y_i}$ every $\log D_i$ is a convex function of $y$. So the continuous problem with path constraints $\sum_{h \in Q} D_h \le T$ for all paths $Q$ is a geometric program, and every local minimum of it is global.

*Proof.* $D_i$ is a sum of monomials $p_i$, $r_i f_i x_i^{-1}$ and $r_i c_j x_j x_i^{-1}$ with positive coefficients. A monomial $\kappa \prod x_k^{\alpha_k}$ is $\exp(\log \kappa + \alpha \cdot y)$, and the log of a sum of exponentials of affine functions is convex. Sums of posynomials are posynomials, so each path constraint is a posynomial at most $T$, and the area $\sum a_i e^{y_i}$ is convex. A convex problem has no local minimum that is not global. $\square$

Lemma 3 is the fact that Fishburn and Dunlop used. It does not make TILOS optimal, because TILOS only moves sizes up, one step and one gate at a time, along the current critical path.

**Theorem 3 (not optimal).** There are instances where TILOS returns sizes whose area exceeds the least area over the discrete sizes.

*Proof.* The chain of the page, with $r = (3, 1, 2, 3)$, $a = (2, 1, 3, 1)$, all $p_i = c_i = 1$, $f_3 = 12$, gate 0 fixed at size 1, sizes $\{1, 2, 3, 4\}$ for the others and $T = 24$. TILOS returns $(1, 1, 2, 4)$ with area 13 and delay 22. The sizes $(1, 1, 2, 3)$ have delay $4 + 3 + 4 + 13 = 24$ and area 12. $\square$

**Theorem 4 (not complete).** There are instances where TILOS fails although some sizing meets the target.

*Proof.* The same chain with $r = (1, 3, 3, 1)$, all $a_i = 1$, $f_3 = 6$ and $T = 16$. At the smallest sizes the delays are $D_0 = 2$, $D_1 = 4$, $D_2 = 4$ and $D_3 = 7$, so $\Delta = 17$. Moving gate 1 up gains $1/2$, gate 2 gains $-3/2$ and gate 3 gains 0, so TILOS moves gate 1, which gives $\Delta = 33/2$. Now each move on the path has gain at most 0, and TILOS fails. The sizes $(1, 2, 2, 2)$ have delays $3, 4, 4, 4$ and $\Delta = 15 \le 16$. $\square$
