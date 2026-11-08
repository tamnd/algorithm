---
title: The Kirkpatrick-Seidel algorithm runs in O(n log h) time
proves: [time.worst]
status: full
---

**Claim.** On the real RAM, KIRKPATRICK-SEIDEL runs in $O(n \log h)$ time in the worst case on $n$ input points with $h \ge 2$ hull vertices, and in $O(n)$ time when $h \le 2$.

**Notation.** $n = |P|$, $h$ is the number of vertices of $\operatorname{conv} P$. For one call of LOWER-HULL, $t_0 = |T| \le n$ is the size of the set of line L4, and $h_0$ is the number of vertices of the lower hull it returns; $h_0 \le h$. All selections use the linear-time [median of medians](/median-of-medians/) method, so selecting from $k$ values costs $O(k)$.

**Step 1: BRIDGE$(C, m)$ takes $O(|C|)$ time.** A round with $c = |C|$ points costs $O(c)$: pairing and slopes, one selection among $\lfloor c/2 \rfloor$ slopes, one pass for $M$, and one pass for the new $C$. By the termination argument of the correctness proof, a round with $c \ge 3$ removes at least $(c - 1)/4$ points, so the next round has at most $(3c + 1)/4 \le 5c/6$ points. The sizes of the rounds are therefore bounded by a geometric series with ratio $5/6$, and the total is $O(|C|)$.

**Step 2: one call of CONNECT costs $O(|T|)$ besides its two recursive calls.** Line L8 is one selection, line L9 is $O(|T|)$ by Step 1, and line L10 is one pass.

**Step 3: the recursion tree.** Give the first call depth 0 and its children depth $k + 1$ when the parent has depth $k$.

- *Sizes halve.* With $t = |T|$ and $m$ the $\lceil t/2 \rceil$-th smallest $x$, we have $l_x \le m < r_x$, so $|T_l| \le \lceil t/2 \rceil$ and $|T_r| \le t - \lceil t/2 \rceil = \lfloor t/2 \rfloor$. By induction, a call at depth $k$ has $|T| \le \lceil t_0 / 2^k \rceil$. A call with $a \ne b$ has $|T| \ge 2$, so it exists only at depths with $t_0 / 2^k > 1$, and there $|T| \le \lceil t_0/2^k \rceil < 2 t_0 / 2^k$.
- *Disjoint sets on one level.* The two children of a call get $T_l$ and $T_r$, which are disjoint because $l_x < r_x$. By induction the sets of all calls at one depth are disjoint, so their sizes add up to at most $t_0$.
- *Few calls with work.* Each call with $a \ne b$ finds one bridge, an edge of the lower hull, and different calls find different edges (their sets are disjoint or nested with the bridge of the parent excluded from the children's $x$-ranges). So there are at most $h_0 - 1$ such calls in the whole tree. Calls with $a = b$ cost $O(1)$, and each outputs one vertex, so there are $h_0$ of them.

**Step 4: summing by levels.** Let $W_k$ be the sum of $|T|$ over the calls with $a \ne b$ at depth $k$. By Step 3, $W_k \le t_0$, and $W_k \le h_0 \cdot 2 t_0 / 2^k$. By Step 2 the total time of CONNECT is $O\left(h_0 + \sum_k W_k\right)$. Split the sum at $k_0 = \lceil \log_2 h_0 \rceil$:

$$\sum_{k < k_0} W_k \le k_0\, t_0, \qquad \sum_{k \ge k_0} W_k \le 2 h_0 t_0 \sum_{k \ge k_0} 2^{-k} \le 4 h_0 t_0 2^{-k_0} \le 4 t_0.$$

So the calls of CONNECT in one call of LOWER-HULL take $O(t_0 \log h_0 + t_0) = O(n \log h + n)$ time. Line L5 is one pass. Line L4 groups the points by $x$, in $O(n)$ expected time with a hash table (see the remark below).

**Step 5: total.** Line L1 removes duplicates, in $O(n)$ expected time with a hash set, and line L3 joins two lists in $O(n)$ time. Line L2 calls LOWER-HULL twice. For $h \ge 2$, $\log h \ge 1$ and the total is $O(n \log h)$. For $h \le 2$ every lower hull has at most two vertices, $k_0 \le 1$, and the total is $O(n)$. $\blacksquare$

**Remark on the model.** Kirkpatrick and Seidel assume that no two points have the same $x$-coordinate, and then every step is a comparison, an orientation test or a slope comparison, so the bound $O(n \log h)$ holds in the worst case and in the [algebraic decision tree](/algebraic-decision-tree/) model, matching their $\Omega(n \log h)$ lower bound. Grouping points by equal $x$ in a comparison model would be as hard as element uniqueness, $\Omega(n \log n)$, so a comparison-only version must break ties by a symbolic perturbation instead of grouping. The implementation of this page uses a hash set and a hash table in lines L1 and L4, so its bound is $O(n \log h)$ in the worst case plus $O(n)$ expected time for these two lines.
