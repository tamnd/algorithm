---
title: The SIV tests are exact, the delta test keeps every solution, and the result is exact when no MIV subscript remains
proves: [correctness]
status: full
---

## Setting

The nest has depth $k$; loop $l$ runs over the integers $L_l, \dots, U_l$ and $N_l = U_l - L_l$. A pair of references gives one equation per dimension,

$$\sum_{l=1}^{k} (A_l i_l - B_l j_l) = c, \qquad c = b_0 - a_0,$$

where the source subscript is $a_0 + \sum_l A_l i_l$ and the sink subscript is $b_0 + \sum_l B_l j_l$. The **solution set** is the set $\Sigma$ of integer pairs $(\vec{i}, \vec{j})$ in the box $\prod_l [L_l, U_l]^2$ that solve all the equations. A level $l$ is *used* by an equation if $A_l \ne 0$ or $B_l \ne 0$. An equation is ZIV, SIV or MIV if it uses zero, one, or more levels.

A **level state** $S_l$ is a set of integer pairs $(x, y) \in [L_l, U_l]^2$, kept in one of four forms: all pairs (*free*), no pair (*empty*), one pair (*point*), or the pairs $(x_0 + p t, y_0 + q t)$ for the integers $t$ with $t_{lo} \le t \le t_{hi}$ (*line*), with $(p, q) \ne (0, 0)$.

We write $\Sigma(E, \vec{S})$ for the set of $(\vec{i}, \vec{j})$ with $(i_l, j_l) \in S_l$ for each $l$ that solve every equation of the list $E$. At the start $E$ is the list of the subscript equations and every $S_l$ is free, so $\Sigma(E, \vec{S}) = \Sigma$.

## Lemma 1 (the line in the box)

`line_in_box(x0, y0, p, q, L, U)` returns the state whose pairs are exactly the points $(x_0 + pt, y_0 + qt)$, $t \in \mathbb{Z}$, that lie in $[L, U]^2$.

*Proof.* For $p > 0$, $L \le x_0 + p t \le U$ holds exactly for $\lceil (L - x_0)/p \rceil \le t \le \lfloor (U - x_0)/p \rfloor$; for $p < 0$ the division by $p$ turns the inequalities around, which gives the bounds of `axis_range`; for $p = 0$ the condition does not depend on $t$, and it holds for all $t$ or for none. The same holds for $y$ and $q$. The set of good $t$ is the intersection of the two ranges. It is empty, one value (a point), or an interval with at least two values (a line). $\square$

## Theorem 1 (exactness of the strong SIV test)

Let $a \ne 0$. The equation $a i + c_1 = a j + c_2$ has an integer solution $(i, j) \in [L, U]^2$ if and only if $a$ divides $c_1 - c_2$ and $|d| \le U - L$ for $d = (c_1 - c_2)/a$. All its solutions then have the distance $j - i = d$, and they are the pairs $(t, t + d)$ for $\max(L, L - d) \le t \le \min(U, U - d)$.

*Proof.* The equation is $a(j - i) = c_1 - c_2$. If $(i, j)$ is a solution, then $a$ divides $c_1 - c_2$ and $j - i = d$. Both $i$ and $j$ lie in $[L, U]$, so $|d| = |j - i| \le U - L$. Conversely, let $a$ divide $c_1 - c_2$ and $|d| \le U - L$. A pair $(t, t + d)$ solves the equation, and it lies in the box if and only if $L \le t \le U$ and $L - d \le t \le U - d$, that is, $\max(L, L - d) \le t \le \min(U, U - d)$. This interval is nonempty: if $d \ge 0$ it is $[L, U - d]$ and $U - d \ge L$; if $d < 0$ it is $[L - d, U]$ and $L - d \le U$. So a solution exists. Every solution has $j - i = d$, so it is of the form $(t, t + d)$. $\square$

In the code, the equation is written $a i - a j = c$ with $c = c_2 - c_1$, so $d = -c/a$, and the line $(0 + t, d + t)$ is cut to the box by Lemma 1, which gives the interval above.

## Theorem 2 (exactness of the other SIV tests)

For $(a, b) \ne (0, 0)$, `siv_solve(a, b, c, L, U)` returns exactly the set $\{(x, y) \in [L, U]^2 \cap \mathbb{Z}^2 : a x - b y = c\}$.

*Proof.* Theorem 1 covers $a = b$.

- *Weak-zero, $b = 0$.* The equation is $a x = c$. It has a solution only if $a$ divides $c$, and then $x = c/a$ and $y$ is any integer: the line $(c/a, 0) + t(0, 1)$. The case $a = 0$ is the same with the roles of $x$ and $y$ exchanged, $y = -c/b$.
- *Weak-crossing, $b = -a$.* The equation is $a(x + y) = c$. It has a solution only if $a$ divides $c$, and then the solutions are the pairs with $x + y = c/a$: the line $(0, c/a) + t(1, -1)$.
- *Exact SIV.* Here $a$ and $b$ are both nonzero. Let $g = \gcd(a, -b) > 0$ and $a x_1 - b y_1 = g$ from the extended Euclidean algorithm. If $g$ does not divide $c$, there is no solution (Bezout). Otherwise $(x_0, y_0) = (c/g)(x_1, y_1)$ is a solution. If $(x, y)$ is another, then $a(x - x_0) = b(y - y_0)$; dividing by $g$, $(a/g)(x - x_0) = (b/g)(y - y_0)$ with $\gcd(a/g, b/g) = 1$, so $b/g$ divides $x - x_0$. Writing $x - x_0 = (b/g) t$ and dividing by $b/g \ne 0$ gives $y - y_0 = (a/g) t$. Conversely every such point is a solution. So the solutions are the line $(x_0, y_0) + t(p, q)$ with $(p, q) = \pm(b/g, a/g)$.

In each case Lemma 1 cuts the line to the box exactly. $\square$

## Lemma 2 (meet)

`meet(S, a, b, c, L, U)` returns $\{(x, y) \in S : a x - b y = c\}$.

*Proof.* If $a = b = 0$, the equation is $0 = c$, true for all pairs or for none. For a free state this is Theorem 2. For an empty state the result is empty. For a point, the code checks the equation. For a line, substitute: $a(x_0 + pt) - b(y_0 + qt) = c$ is $(ap - bq) t = c - a x_0 + b y_0$. If $ap - bq = 0$, either every $t$ or no $t$ solves it. Otherwise it has at most one solution $t$, which must be an integer in $[t_{lo}, t_{hi}]$. $\square$

## Lemma 3 (the delta step keeps the solution set)

Let $(A', B', c')$ be the result of `propagate` on an equation $(A, B, c)$ with the states $\vec{S}$. For every $(\vec{i}, \vec{j})$ with $(i_l, j_l) \in S_l$ for all $l$, the two equations have the same truth value.

*Proof.* `propagate` changes the terms of one level at a time, and each change replaces the term $A_l i_l - B_l j_l$ by an expression equal to it on every pair of $S_l$:

- $S_l$ is the point $(x^*, y^*)$: on $S_l$ the term is the constant $A_l x^* - B_l y^*$, which moves to the right side.
- $S_l$ is a line with $p = 0$: every pair of $S_l$ has $i_l = x_0$, so $A_l i_l = A_l x_0$ moves to the right side.
- $S_l$ is a line with $q = 0$: every pair has $j_l = y_0$, and $-B_l j_l = -B_l y_0$ moves to the right side.
- $S_l$ is a line with $p = q$: every pair has $j_l - i_l = (y_0 - x_0) + (q - p)t = y_0 - x_0 =: \delta$. Then $A_l i_l - B_l j_l = (A_l - B_l) i_l - B_l \delta$, and $B_l \delta$ moves to the right side.

Other states are left alone. The sum of the terms is unchanged on the pairs of the states, so the two equations agree there. $\square$

## Theorem 3 (the delta test keeps every solution, and ends)

During `delta_test`, the value of $\Sigma(E, \vec{S})$, with $E$ the list of pending equations plus the equations that were moved into states, never changes. So it is always equal to $\Sigma$. The loop ends.

*Proof.* Each step does one of four things to a pending equation.

1. *Rewrite it* by Lemma 3. On the pairs of the states the new equation is equivalent to the old one, so $\Sigma(E, \vec{S})$ does not change.
2. *Drop it* when it uses no level and $c = 0$: the equation $0 = 0$ holds everywhere.
3. *Stop with "independent"* when it uses no level and $c \ne 0$: the equation $0 = c$ never holds, so $\Sigma(E, \vec{S}) = \Sigma$ is empty.
4. *Move it into $S_l$* when it uses only level $l$: by Lemma 2 the new state is the set of pairs of $S_l$ that satisfy it, so keeping it in the state is the same as keeping it in the list. If the state becomes empty, $\Sigma$ is empty, and the test stops with "independent".

So every answer "independent" is correct, and when the loop ends, $\Sigma = \Sigma(E_{MIV}, \vec{S})$ where $E_{MIV}$ is the list of the remaining equations, each with at least two levels.

The loop ends: a pass that changes nothing ends it, and each pass that changes something removes at least one equation from the pending list, which starts with $m$ equations. So there are at most $m + 1$ passes. $\square$

The coupled groups do not change this: two equations of different groups use disjoint sets of levels, so running the delta test on each group alone gives the same states and the same remaining equations as running it on all equations together, and $\Sigma$ is the product of the solution sets of the groups, together with all pairs of the levels that no equation uses.

## Theorem 4 (soundness)

If $\Sigma$ is not empty, `dependence` does not answer "independent", and the direction vector $\psi(\vec{i}, \vec{j}) = (\mathrm{sign}(i_l, j_l))_l$ of each $(\vec{i}, \vec{j}) \in \Sigma$ is in the returned set. Every distance it reports is the distance of every solution at that level.

*Proof.* A ZIV equation that the code rejects has $a_0 \ne b_0$ and no index, so it has no solution. By Theorem 3, the delta test answers "independent" only when $\Sigma$ is empty. Take $(\vec{i}, \vec{j}) \in \Sigma$ and a group. By Theorem 3, $(i_l, j_l) \in S_l$ for each level of the group, and the pair has the direction $\psi_l$, so it is in the part of $S_l$ with that direction. `level_view` returns exactly this part (for a line, the condition $\mathrm{sign}(x - y)$ on $x - y = e_0 + e_1 t$ is a linear condition on $t$, solved with floor and ceiling), so the direction $\psi_l$ is among the options of the level. Each remaining MIV equation holds at $(\vec{i}, \vec{j})$. `term_values` gives, for each level, an interval and a lattice $\text{offset} + \text{step}\,\mathbb{Z}$ that contain every value of $A_l i_l - B_l j_l$ on that part (the Banerjee bounds for a free level, and the exact endpoints and step of the parametrization for a point or a line). So the value $c$ is in the sum of the intervals and in the sum of the lattices, and `miv_allows` accepts. The vector restricted to the group is therefore in the group set, and the product over the groups and the unused levels contains $\psi(\vec{i}, \vec{j})$. Finally, a distance is reported only for a state in which all pairs have the same difference $y - x$, and every solution lies in its state. $\square$

## Theorem 5 (exactness without MIV equations)

If no MIV equation remains in any group, the returned answer is exact: "independent" if and only if $\Sigma$ is empty, and the set of direction vectors is exactly $\{\psi(\vec{i}, \vec{j}) : (\vec{i}, \vec{j}) \in \Sigma\}$.

*Proof.* With no MIV equation left, Theorem 3 gives $\Sigma = \prod_l S_l$: a tuple of pairs, one from each state, with no further condition. For a vector $\vec{\psi}$ in the returned set, each level option was kept because the part of $S_l$ with direction $\psi_l$ is not empty (Lemma 1 and the exactness of `level_view`). Choosing one pair from each part gives an element of $\Sigma$ with direction $\vec{\psi}$. With Theorem 4, the two sets are equal. If $\Sigma$ were empty, some $S_l$ would be empty, and the test would have answered "independent". $\square$

When MIV equations remain, the flag `exact` is false, and only Theorem 4 holds: the set can contain a direction vector without a solution. This is the one-sided promise of all conservative tests.

## Cost

Let $m$ be the number of subscripts. The classification and the union-find take $O(mk)$ time. The delta test makes at most $m + 1$ passes; each pass rewrites at most $m$ equations in $O(k)$ time and calls `meet`, whose cost is a few divisions and one extended gcd, $O(\log C)$ for coefficients up to $C$. So the delta test costs $O(m^2 k + m \log C)$. The MIV filter tests at most $3^k$ direction vectors against at most $m$ equations at $O(k)$ each, $O(3^k m k)$; it runs only when MIV equations remain.
