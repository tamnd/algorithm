---
title: The Banerjee bounds are the exact real range of a subscript equation, so the test is sound
proves: [correctness]
status: full
---

## Setting

The loop nest has depth $k$, and loop $l$ runs over the integers $L_l, \dots, U_l$, with $N_l = U_l - L_l$. One subscript pair gives the equation

$$h(\vec{x}, \vec{y}) = \sum_{l=1}^{k} (a_l x_l - b_l y_l) = c, \qquad c = b_0 - a_0,$$

where $\vec{x}$ stands for the source iteration and $\vec{y}$ for the sink iteration. For $t \in \mathbb{R}$ write $t^+ = \max(t, 0)$ and $t^- = \max(-t, 0)$, so $t = t^+ - t^-$ and $t^+, t^- \ge 0$.

For a direction $d \in \{*, =, <, >\}$, the **region** of level $l$ is the set of real pairs

$$R_l(d) = \{(x, y) \in \mathbb{R}^2 : L_l \le x \le U_l,\ L_l \le y \le U_l,\ \rho_d(x, y)\},$$

where $\rho_*$ is no condition, $\rho_=$ is $x = y$, $\rho_<$ is $x + 1 \le y$ and $\rho_>$ is $y + 1 \le x$. For integers, $x < y$ is the same as $x + 1 \le y$, so every integer pair with $x \,d\, y$ in the bounds lies in $R_l(d)$. The region of a direction vector $\vec{\psi}$ is the product $R(\vec{\psi}) = R_1(\psi_1) \times \dots \times R_k(\psi_k)$.

The test computes, for each level, the pair $(lo_l, hi_l)$ of line L5 (the function `level_bounds`, lines L10 to L13), adds them in line L7, and answers "independent" in line L8 if $c < lo$ or $c > hi$, or in line L6 if some region is empty.

## Lemma 1 (each region is the convex hull of its vertices)

Let $V_l(d)$ be the vertex list of the code:

| $d$ | $V_l(d)$ |
|---|---|
| $*$ | $(L, L), (L, U), (U, L), (U, U)$ |
| $=$ | $(L, L), (U, U)$ |
| $<$, if $N \ge 1$ | $(L, L+1), (L, U), (U-1, U)$ |
| $>$, if $N \ge 1$ | $(L+1, L), (U, L), (U, U-1)$ |

(dropping the index $l$). Then $R_l(d)$ is the set of convex combinations of $V_l(d)$. For $d \in \{<, >\}$ and $N < 1$ the region is empty.

*Proof.* Each vertex lies in the region, and the region is convex (it is cut out by linear inequalities), so every convex combination of vertices lies in it. For the other inclusion, take $(x, y)$ in the region.

- $d = *$. Put $s = (x - L)/N$ and $t = (y - L)/N$ if $N > 0$ (if $N = 0$ the region is the one point $(L, L)$). Then $s, t \in [0, 1]$ and $(x, y) = (1-s)(1-t)(L, L) + (1-s)t(L, U) + s(1-t)(U, L) + st(U, U)$. The four weights are nonnegative and sum to $1$.
- $d = {=}$. Then $x = y$ and $(x, x) = (1 - s)(L, L) + s(U, U)$ with $s = (x - L)/N$, or the one point $(L, L)$ if $N = 0$.
- $d = {<}$. The three numbers $p = x - L$, $q = U - y$ and $r = y - x - 1$ are nonnegative in the region, and $p + q + r = N - 1$. If $N < 1$, they cannot all be nonnegative, so the region is empty. If $N = 1$, all three are $0$, and the region is the one point $(L, L + 1) = (L, U)$. If $N \ge 2$, the vertices have $(p, q, r)$ equal to $(0, N-1, 0)$, $(0, 0, N-1)$ and $(N-1, 0, 0)$, in the order of the table. The point $\frac{q}{N-1}(L, L+1) + \frac{r}{N-1}(L, U) + \frac{p}{N-1}(U-1, U)$ has the same $p$, $q$, $r$ as $(x, y)$, because $p$, $q$, $r$ are affine functions and the weights sum to $1$. Two points with the same $p$ and $q$ are equal, so this is $(x, y)$.
- $d = {>}$. Swap the roles of $x$ and $y$ in the previous case. $\square$

## Lemma 2 (a linear function on a convex hull)

Let $V$ be a finite set of points and $\varphi$ a linear function (plus a constant). On the set of convex combinations of $V$, the minimum of $\varphi$ is $\min_{v \in V} \varphi(v)$ and the maximum is $\max_{v \in V} \varphi(v)$.

*Proof.* For $p = \sum_v \lambda_v v$ with $\lambda_v \ge 0$ and $\sum_v \lambda_v = 1$, $\varphi(p) = \sum_v \lambda_v \varphi(v)$, a weighted mean of the values at the vertices. A weighted mean lies between the smallest and the largest of the values. Both are reached, at the vertices themselves. $\square$

## Lemma 3 (the closed forms)

For each level and each direction with a nonempty region, the pair $(lo_l, hi_l)$ returned by `level_bounds` equals the minimum and the maximum of $\varphi(x, y) = a x - b y$ over $R_l(d)$.

*Proof.* By Lemmas 1 and 2 it is enough to compute the extremes of $\varphi$ over $V_l(d)$.

- $d = *$. The term $a x$ over $x \in \{L, U\}$ has the minimum $aL$ if $a \ge 0$ and $aU$ if $a < 0$, which is $a^+ L - a^- U$ in both cases, and the maximum $a^+ U - a^- L$. The term $-b y$ over $y \in \{L, U\}$ has the minimum $-(b^+ U - b^- L)$ and the maximum $-(b^+ L - b^- U)$. The four vertices are all combinations of $x$ and $y$ in $\{L, U\}$, so the two terms reach their extremes on their own. The sums are the bounds of line L10.
- $d = {=}$. On $(L, L)$ and $(U, U)$, $\varphi = (a - b) x$, with extremes $(a-b)^+ L - (a-b)^- U$ and $(a-b)^+ U - (a-b)^- L$, as in line L11.
- $d = {<}$. Let $v_0 = \varphi(L, L+1) = (a - b) L - b$. Direct computation gives $\varphi(L, U) = v_0 - b(N - 1)$ and $\varphi(U-1, U) = v_0 + (a - b)(N - 1)$. As $N - 1 \ge 0$, the minimum is $v_0 - (N-1)\max(0, b, b - a) = v_0 - (N-1)(a^- + b)^+$, and the maximum is $v_0 + (N-1)\max(0, -b, a - b) = v_0 + (N-1)(a^+ - b)^+$. Here $\max(b, b - a) = b + a^-$ and $\max(-b, a - b) = a^+ - b$. These are the bounds of line L12.
- $d = {>}$. Let $v_0 = \varphi(L+1, L) = (a - b) L + a$. Then $\varphi(U, L) = v_0 + a(N-1)$ and $\varphi(U, U-1) = v_0 + (a - b)(N - 1)$. The minimum is $v_0 - (N-1)\max(0, -a, b - a) = v_0 - (N-1)(b^+ - a)^+$ and the maximum is $v_0 + (N-1)\max(0, a, a - b) = v_0 + (N-1)(a + b^-)^+$, as in line L13. $\square$

## Theorem 1 (the Banerjee bounds)

Let $\vec{\psi}$ be a direction vector whose regions are all nonempty, and let $lo = \sum_l lo_l$ and $hi = \sum_l hi_l$ as computed in line L7. Then

$$lo = \min_{R(\vec{\psi})} h, \qquad hi = \max_{R(\vec{\psi})} h,$$

and every value between $lo$ and $hi$ is taken by $h$ on $R(\vec{\psi})$.

*Proof.* The function is a sum $h = \sum_l \varphi_l(x_l, y_l)$ in which the term $\varphi_l$ depends only on the pair of level $l$, and the region is a product of the sets $R_l(\psi_l)$. So a point of $R(\vec{\psi})$ is any choice of one pair from each $R_l(\psi_l)$, and each term can be made as small as possible on its own: $\min h = \sum_l \min \varphi_l = \sum_l lo_l$ by Lemma 3, and the same for the maximum. Both are reached: let $p^{\min}$ be the point that takes, at each level, the vertex where $\varphi_l$ is smallest, and $p^{\max}$ the same with the largest.

For a value $c$ with $lo \le c \le hi$, put $t = (c - lo)/(hi - lo)$ if $hi > lo$ and $t = 0$ otherwise, and $p = p^{\min} + t(p^{\max} - p^{\min})$. Each level pair of $p$ is a convex combination of two points of the convex set $R_l(\psi_l)$, so $p \in R(\vec{\psi})$. As $h$ is linear, $h(p) = lo + t(hi - lo) = c$. $\square$

The function `real_witness` builds exactly this point $p$, with rational coordinates, and the tests check that it lies in the region and solves the equation.

## Theorem 2 (exact over the reals, for one subscript)

For one subscript pair and a direction vector $\vec{\psi}$, the test answers "maybe" if and only if the equation $h = c$ has a real solution in $R(\vec{\psi})$.

*Proof.* If some region is empty, $R(\vec{\psi})$ is empty, there is no solution, and line L6 answers "independent". Otherwise, by Theorem 1, the set of values of $h$ on $R(\vec{\psi})$ is exactly the interval $[lo, hi]$. So a solution exists if and only if $lo \le c \le hi$, which is the negation of the condition of line L8. $\square$

## Theorem 3 (soundness)

If there are integer vectors $\vec{i}$ and $\vec{j}$ in the loop bounds with $i_l \,\psi_l\, j_l$ for all $l$ and with all $m$ subscript pairs equal, the test answers "maybe". So "independent" proves that there is no dependence with direction vector $\vec{\psi}$.

*Proof.* The point $(\vec{i}, \vec{j})$ lies in $R(\vec{\psi})$ (integer $i_l < j_l$ gives $i_l + 1 \le j_l$), and it solves the equation of each subscript. By Theorem 2 each subscript gives "maybe" in line L8, and no region is empty, so line L6 never fires. Line L9 answers "maybe". $\square$

## Theorem 4 (the direction search loses nothing)

The function `direction_vectors` returns a set that contains the direction vector of every integer solution in the bounds, and equals the set of plain vectors $\vec{\psi} \in \{<, =, >\}^k$ for which the test says "maybe".

*Proof.* Each plain $\vec{\psi}$ is reached from $(*, \dots, *)$ by replacing the first $*$ with a symbol, one level at a time, and the search follows this path unless the test says "independent" at a vector $\vec{\psi}'$ on it. Every vector on the path keeps the symbols of $\vec{\psi}$ where it has symbols and has $*$ elsewhere, so $R(\vec{\psi}) \subseteq R(\vec{\psi}')$, because $R_l(d) \subseteq R_l(*)$. A smaller set gives a smaller range of $h$, so if $c$ is outside the range for $\vec{\psi}'$, it is outside for $\vec{\psi}$, and the test also says "independent" for $\vec{\psi}$. So the cut removes only vectors that the test rules out, and the leaves are exactly the plain vectors with "maybe". By Theorem 3, the direction vector of an integer solution gives "maybe", so it is in the set. $\square$

## An example where the test says "maybe" and there is no integer solution

Take `A[2*i] = A[3*i + 2] + 1` for $i = 1, \dots, 3$. The equation is $2x - 3y = 2$ on $1 \le x, y \le 3$, with $a = 2$, $b = 3$, $L = 1$, $U = 3$ and $N = 2$.

- For $*$: $lo = 2 \cdot 1 - 3 \cdot 3 = -7$ and $hi = 2 \cdot 3 - 3 \cdot 1 = 3$. The value $2$ is inside, so the test says "maybe". The GCD test also says "maybe", since $\gcd(2, 3) = 1$.
- Refined: for $<$, $v_0 = -1 - 3 = -4$, so the range is $[-4 - 3, -4 + 0] = [-7, -4]$; for $=$, $a - b = -1$ and the range is $[-3, -1]$; for $>$, $v_0 = -1 + 2 = 1$, and the range is $[1 - 1, 1 + 2] = [0, 3]$. Only $>$ stays "maybe". A real witness is $(x, y) = (2.5, 1)$: it has $y + 1 \le x$, and $2 \cdot 2.5 - 3 \cdot 1 = 2$.
- There is no integer solution in the bounds: $2x = 3y + 2$ forces $y$ to be even, so $y = 2$ and $x = 4 > 3$. The written elements are $A[2], A[4], A[6]$ and the read elements are $A[5], A[8], A[11]$.

So Theorem 2 is the best the test can do: it is exact over the reals, and the gap between real and integer solutions is where it says "maybe" with no dependence.

## Cost

`level_bounds` takes $O(1)$ arithmetic operations, so one subscript and one direction vector cost $O(k)$, and the test of $m$ subscripts costs $O(mk)$. The direction search visits at most $1 + 3 + \dots + 3^k < \tfrac{3}{2} 3^k$ vectors, so it costs $O(3^k m k)$ in the worst case.
