---
title: Knapsack branch and bound returns an optimal packing
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The items are sorted so that $v_1 / w_1 \ge \cdots \ge v_n / w_n$, with items of weight 0 first. For $0 \le k \le n$, a set $Y \subseteq \{1, \ldots, n\}$ *extends* a node $(k, c_w, c_v, X)$ if $Y \cap \{1, \ldots, k\} = X$. A set is *feasible* if its weight is at most $W$. Let $F(k, c_w, c_v)$ be the largest value of $c_v + \sum_{i \in Z} v_i$ over sets $Z \subseteq \{k + 1, \ldots, n\}$ with $c_w + \sum_{i \in Z} w_i \le W$.

**Lemma 1 (the bound is valid).** If $c_w \le W$, then $U(k, c_w, c_v) \ge F(k, c_w, c_v)$, where $U$ is the bound rounded down.

*Proof.* Let $r = W - c_w$. A fractional packing of items $k + 1, \ldots, n$ is a vector $y \in [0, 1]^{n-k}$ with $\sum y_i w_i \le r$. Let $g$ be the greedy vector: $y_i = 1$ for items $k + 1, \ldots, j - 1$, $y_j = (r - \sum_{i < j} w_i) / w_j$ for the first item $j$ that does not fit, and $y_i = 0$ after it (if all items fit, $g$ is all ones). We show that $g$ maximizes $\sum y_i v_i$. Let $y$ be any fractional packing, and let $\rho = v_j / w_j$ (or $\rho = 0$ if all items fit). For $i < j$, $v_i \ge \rho w_i$ and $g_i = 1 \ge y_i$; for $i > j$, $v_i \le \rho w_i$ and $g_i = 0 \le y_i$. So
$$\sum_i (g_i - y_i) v_i \ge \rho \sum_i (g_i - y_i) w_i = \rho \Big(r - \sum_i y_i w_i\Big) \ge 0$$
when $j$ exists, because then $\sum_i g_i w_i = r$; when all items fit, $g_i = 1 \ge y_i$ for all $i$ and the sum is clearly nonnegative. Items of weight 0 are first and have $g_i = 1$. A 0-1 packing $Z$ is a fractional packing, so $c_v + \sum_{i \in Z} v_i \le c_v + \sum g_i v_i$, the unrounded bound. The left side is an integer, so it is also at most the rounded-down bound $U$. $\square$

**Lemma 2 (the take child keeps the bound).** If $c_w + w_{k+1} \le W$, then $U(k + 1, c_w + w_{k+1}, c_v + v_{k+1}) = U(k, c_w, c_v)$.

*Proof.* The greedy fill from item $k + 1$ with room $r$ takes item $k + 1$ whole, because $w_{k+1} \le r$, and then continues on items $k + 2, \ldots$ with room $r - w_{k+1}$. This is the greedy fill of the child, and the value $v_{k+1}$ moves from the fill into $c_v$. $\square$

**Claim 3 (the incumbent is real).** At each point, $best$ is a feasible set of value $z$. *Proof.* Initially $best = \emptyset$ and $z = 0$. Each pushed node has $c_w \le W$ (the root has $c_w = 0$, the leave child keeps $c_w$, and line L9 tests the take child), and $c_w$ and $c_v$ are the weight and value of $X$. Line L5 copies such a node. $\square$

**Claim 4 (invariant).** At the start of each iteration of line L3, every feasible set $Y$ with value greater than $z$ extends some node on $S$.

*Proof.* At the start, $S$ holds the root, which every set extends. Suppose the claim holds at the start of an iteration. Let $N = (k, c_w, c_v, X)$ be the node popped, $z_0$ the incumbent before line L5, and $z_1 \ge z_0$ the incumbent at the end of the iteration. Let $Y$ be feasible with value greater than $z_1$; it extends a node that was on $S$. If that node is not $N$, it is still on $S$. Suppose it is $N$, so $Y \cap \{1, \ldots, k\} = X$, and the value of $Y$ is at most $F(k, c_w, c_v) \le U(k, c_w, c_v)$ by Lemma 1.

- If $k = n$, then $Y = X$, and line L5 gives $z_1 \ge c_v$, the value of $Y$: false.
- If $U(k, c_w, c_v) \le z_1$ at line L6: false, as the value of $Y$ is at most $U$.
- If $k + 1 \notin Y$, then $Y$ extends the leave child; its value is at most $F(k + 1, c_w, c_v) \le U(k + 1, c_w, c_v)$, so this bound is greater than $z_1$ and line L7 pushes the child.
- If $k + 1 \in Y$, then $c_w + w_{k+1} \le$ the weight of $Y \le W$, so line L9 pushes the take child, which $Y$ extends.

So the claim holds at the start of the next iteration. $\square$

**Claim 5 (termination).** Each pushed node has a larger $k$ than its parent, and $k \le n$, so each node of the binary tree of decisions is pushed at most once and the loop runs at most $2^{n+1} - 1$ times. $\square$

**Theorem.** KNAPSACK-BB returns $(z, best)$ where $best$ is an optimal packing and $z$ its value.

*Proof.* The loop ends by Claim 5 with $S$ empty. By Claim 4, no feasible set has value greater than $z$. By Claim 3, $best$ is feasible with value $z$. So $best$ is optimal. The implementation sorts the items first and maps the indices of $best$ back to the input order, which changes neither feasibility nor value. $\blacksquare$
