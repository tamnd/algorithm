---
title: LINEAR-DIOPHANTINE returns a solution exactly when one exists
proves: [correctness]
status: full
---

Let $a$, $b$ and $c$ be integers. We write $A = |a|$ and $B = |b|$, and $\sigma_a$, $\sigma_b$ for the signs used in line L11, so that $a \sigma_a = A$ and $b \sigma_b = B$. We use $\gcd(0, 0) = 0$, and $\gcd(u, v) = \gcd(|u|, |v|)$.

**Lemma 1 (necessity).** If $ax + by = c$ for some integers $x$ and $y$, then $\gcd(a, b) \mid c$.

*Proof.* $g = \gcd(a, b)$ divides $a$ and $b$, so it divides $ax + by$. If $g = 0$ then $a = b = 0$ and $c = 0 = g \cdot 0$. $\square$

**Lemma 2 (the loop).** Assume $(a, b) \ne (0, 0)$. Before each test of line L4, the following invariant holds:

> **(E)** $r_0 = A s_0 + B t_0$, $r_1 = A s_1 + B t_1$, $r_0 \ge 0$, $r_1 \ge 0$, and $\gcd(r_0, r_1) = \gcd(a, b)$.

The loop stops, and after it $r_1 = 0$ and $g = r_0 = \gcd(a, b) \ge 1$.

*Proof.* *Initialization.* Line L3 sets $(r_0, s_0, t_0) = (A, 1, 0)$ and $(r_1, s_1, t_1) = (B, 0, 1)$. Then $A = A \cdot 1 + B \cdot 0$, $B = A \cdot 0 + B \cdot 1$, both are nonnegative, and $\gcd(A, B) = \gcd(a, b)$.

*Maintenance.* Assume (E) and $r_1 \ne 0$, so $r_1 > 0$. Line L5 sets $q = \lfloor r_0 / r_1 \rfloor$, and the new values are $r_0' = r_1$, $r_1' = r_0 - q r_1$, $s_0' = s_1$, $s_1' = s_0 - q s_1$, $t_0' = t_1$, $t_1' = t_0 - q t_1$. The first relation for the new values is the old second relation. For the second,
$$A s_1' + B t_1' = (A s_0 + B t_0) - q (A s_1 + B t_1) = r_0 - q r_1 = r_1'.$$
Also $r_0' = r_1 > 0$ and $r_1' = r_0 \bmod r_1 \in [0, r_1)$. By the GCD recursion theorem, $\gcd(r_1, r_0 - q r_1) = \gcd(r_0, r_1) = \gcd(a, b)$. So (E) holds again.

*Termination.* In each iteration the new $r_1$ is $r_0 \bmod r_1 < r_1$. So $r_1$ is a nonnegative integer that strictly decreases, and the loop stops. When it stops, $r_1 = 0$, and (E) gives $\gcd(r_0, 0) = r_0 = \gcd(a, b)$. Since $(a, b) \ne (0, 0)$, $\gcd(a, b) \ge 1$. Line L9 sets $g = r_0$. $\square$

**Theorem.** LINEAR-DIOPHANTINE$(a, b, c)$ returns a pair $(x, y)$ with $ax + by = c$ if a solution exists, and NONE otherwise.

*Proof.* *Case $a = b = 0$.* Then $ax + by = 0$ for all $x$ and $y$, so a solution exists if and only if $c = 0$. Lines L1 and L2 return $(0, 0)$, which is a solution, when $c = 0$, and NONE otherwise.

*Case $(a, b) \ne (0, 0)$.* By Lemma 2, line L9 sets $g = \gcd(a, b) \ge 1$, and $A s_0 + B t_0 = g$. If $g \nmid c$, then by Lemma 1 there is no solution, and line L10 returns NONE. If $g \mid c$, let $m = c / g$, an integer. Line L11 sets $x = \sigma_a s_0 m$ and $y = \sigma_b t_0 m$, so
$$ax + by = (a \sigma_a) s_0 m + (b \sigma_b) t_0 m = (A s_0 + B t_0)\, m = g m = c,$$
and line L12 returns this solution. $\blacksquare$

**The step.** In the case $(a, b) \ne (0, 0)$, the vector $(s_1, t_1)$ at the end satisfies $A s_1 + B t_1 = r_1 = 0$, and it is nonzero, because the matrix with rows $(s_0, t_0)$ and $(s_1, t_1)$ starts as the identity and each iteration multiplies it on the left by a matrix of determinant $-1$, so its determinant stays $\pm 1$. Hence $s_0 t_1 - s_1 t_0 = \pm 1$, which forces $\gcd(s_1, t_1) = 1$. From $A s_1 = -B t_1$ with $\gcd(s_1, t_1) = 1$ it follows that $(s_1, t_1) = \pm (B/g, -A/g)$, the step between consecutive solutions of the equation with $|a|$ and $|b|$.
