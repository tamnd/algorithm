---
title: The sweep for union length returns the measure of the covered set
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, with the test of line L6 written as $count \ge k$ for a fixed integer $k \ge 1$; the page uses $k = 1$. The intervals have end points $l_j \le r_j$, $1 \le j \le n$, and each end point may be open or closed. Let $c(x) = |\{j : x \in I_j\}|$ be the coverage and $S_k = \{x : c(x) \ge k\}$.

**Claim.** SWEEP-UNION-LENGTH returns $\lambda(S_k)$, the Lebesgue measure of $S_k$, for any order of the events with equal coordinates.

*Proof.* Let $e_1, \ldots, e_{2n}$ be the events in the order of line L3, with coordinates $x_1 \le x_2 \le \cdots \le x_{2n}$. If $n = 0$ the loop does not run and the result is $0 = \lambda(\emptyset)$. Assume $n \ge 1$.

**Step 1: the coverage on a gap.** Fix $i$ with $1 \le i < 2n$ and $x_i < x_{i+1}$. Since the events are sorted, the events $e_1, \ldots, e_i$ are exactly the events with coordinate at most $x_i$. So after line L7 has processed $e_i$,
$$ count = |\{j : l_j \le x_i\}| - |\{j : r_j \le x_i\}|. $$
Each $j$ with $r_j \le x_i$ also has $l_j \le r_j \le x_i$, so the difference is $|\{j : l_j \le x_i < r_j\}|$. Let $x \in (x_i, x_{i+1})$. No end point lies in this open gap. An interval $I_j$ contains $x$ if and only if $l_j < x < r_j$ (the end points are not in the gap, so their type does not matter), if and only if $l_j \le x_i$ and $r_j \ge x_{i+1}$, if and only if $l_j \le x_i < r_j$. Hence $c(x) = count$ for every $x$ in the gap.

**Step 2: the invariant.** For $1 \le i \le 2n$ let $T_i = \lambda(S_k \cap (-\infty, x_i])$. We show:

> **(I)** Just before line L6 processes $e_{i+1}$, for $1 \le i < 2n$, and also after the loop for $i = 2n$: $total = T_i$ and $prev = x_i$.

*Initialization.* Before $e_1$, $count = 0 < k$, so line L6 adds nothing, and line L8 sets $prev = x_1$. Every point $x < x_1$ is in no interval, and the point $x_1$ has measure 0, so $T_1 = 0 = total$. So (I) holds for $i = 1$.

*Maintenance.* Assume $total = T_i$ and $prev = x_i$ before line L6 handles $e_{i+1}$.

- If $x_{i+1} = x_i$, line L6 adds $0$ or nothing, so $total = T_i = T_{i+1}$, since $(-\infty, x_{i+1}] = (-\infty, x_i]$.
- If $x_{i+1} > x_i$, then $e_i$ is the last event at $x_i$, and by Step 1 the current $count$ equals $c(x)$ on the whole gap $(x_i, x_{i+1})$. Line L6 adds $x_{i+1} - x_i = \lambda((x_i, x_{i+1}))$ if $count \ge k$, that is, if the gap lies in $S_k$; otherwise the gap is disjoint from $S_k$ and nothing is added. The point $x_{i+1}$ has measure 0. So $total = T_i + \lambda(S_k \cap (x_i, x_{i+1}]) = T_{i+1}$.

Lines L7 and L8 then set $prev = x_{i+1}$.

*Termination.* The loop of line L5 processes each of the $2n$ events once, so it stops after $2n$ steps. Then $total = T_{2n}$. Every point $x > x_{2n}$ is to the right of all end points and lies in no interval, so $S_k \subseteq (-\infty, x_{2n}]$ and $T_{2n} = \lambda(S_k)$. Line L9 returns it. $\blacksquare$

**Tie order.** The proof used the order of events with equal coordinates only through Step 1, which looks at the counter after the last event of a coordinate. That value does not depend on the order within the coordinate. So every tie order gives the same result.

**Cost.** Line L3 sorts $2n$ events; the loop does $2n$ steps of $O(1)$ work each.
