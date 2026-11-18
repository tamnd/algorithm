---
title: Spherical blend skinning moves each vertex rigidly, does not depend on the choice of the center, and is coordinate invariant
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact, the weights of a vertex are nonnegative with the sum 1, and each $C_j x = R_j x + t_j$ is rigid.
Quaternions are in the Hamilton convention, scalar first; $q_j$ is a unit quaternion of $R_j$, and $p \cdot q$ is the dot product in $\mathbb R^4$.
For a vertex with the joint set $J$ and the weights $w_j$, let $m(r) = \sum_j w_j C_j r$ and $S(r) = Q(v - r) + m(r)$, so that line L8 gives $S(r_c)$.

## The center

Let $D_{ab} = R_a - R_b$, $e_{ab} = t_b - t_a$, $N = \sum_{a<b} D_{ab}^\top D_{ab}$ and $g = \sum_{a<b} D_{ab}^\top e_{ab}$.

**Lemma 1.** The minimizers of $f$ are the set $r_0 + K$, where $r_0$ is any solution of $N r = g$ and $K = \{ s : R_a s = R_b s \text{ for all } a, b \in J \}$.
Line L4 returns the unique minimizer in the orthogonal complement of $K$.

*Proof.*
$f(r) = \sum \lvert D_{ab} r - e_{ab} \rvert^2$ is a convex quadratic with the gradient $2(N r - g)$, so its minimizers are the solutions of $N r = g$, which exist because $g$ is in the range of $N$.
Two solutions differ by an element of the null space of $N$.
Since $s^\top N s = \sum \lvert D_{ab} s \rvert^2$ and $N$ is positive semidefinite, $N s = 0$ if and only if $D_{ab} s = 0$ for all pairs, that is $s \in K$.
The code writes $N = \sum_k \lambda_k u_k u_k^\top$ and returns $\sum_{\lambda_k > 0} (u_k \cdot g / \lambda_k)\, u_k$, which solves $N r = g$ and is orthogonal to the null space; such a solution is unique. $\square$

**Lemma 2.** If $C_j c = c$ for all $j \in J$ and $K = \{0\}$, then $r_c = c$.

*Proof.*
$f(c) = 0$, so $c$ is a minimizer, and by Lemma 1 the minimizer is unique. $\square$

## The rotation exists

**Lemma 3.** Let $p$ be the quaternion of the joint with the largest weight $w_p$, and $b = \sum_j w_j s_j q_j$ with $s_j = \pm 1$ chosen so that $p \cdot s_j q_j \ge 0$.
Then $\lvert b \rvert \ge w_p > 0$.

*Proof.*
$\lvert b \rvert \ge p \cdot b = \sum_j w_j\, p \cdot s_j q_j \ge w_p\, p \cdot p = w_p$, since every term is nonnegative and $s_p = 1$.
$w_p > 0$ because the weights sum to 1. $\square$

So $Q = b / \lvert b \rvert$ is a unit quaternion, and line L7 never divides by zero.

## The choice of the center does not matter

**Lemma 4.** If $r$ and $r'$ both minimize $f$, then $S(r) = S(r')$.

*Proof.*
By Lemma 1, $r' = r + s$ with $s \in K$; let $s \ne 0$ and $u = s / \lvert s \rvert$.
Fix $a \in J$.
For every $j$, $R_a^\top R_j u = u$, so $R_a^\top R_j$ is a turn about $u$, and $q_j = \pm q_a (\cos\tfrac{\varphi_j}{2}, \sin\tfrac{\varphi_j}{2}\, u)$ for some angle $\varphi_j$.
Then $b = q_a h$, where $h$ is a sum of quaternions of the form $(\alpha, \beta u)$ and so has this form too.
Hence $Q = q_a h / \lvert h \rvert$ is the rotation $R_a$ after a turn about $u$, and $Q s = R_a s$.
Also $\sum_j w_j R_j s = \sum_j w_j R_a s = R_a s$.
So $S(r + s) - S(r) = -Q s + \sum_j w_j R_j s = -R_a s + R_a s = 0$. $\square$

## Rigid motion per joint set

**Lemma 5.** For a fixed joint set and fixed weights, $v \mapsto S(r_c)$ is a rotation by $Q$ followed by a translation, and $\lvert Q n \rvert = \lvert n \rvert$.

*Proof.*
$S(r_c) = Q v + (m(r_c) - Q r_c)$, and the second term does not depend on $v$.
A unit quaternion rotation keeps lengths. $\square$

So two vertices with the same joints and weights keep their distance, and normals stay unit vectors.

**Lemma 6.** In the bind pose, with $C_j = I$ for all $j$, $S(r_c) = v$ and $Q n = n$.
For a vertex with one joint, $S(r_c) = C_j v$.

*Proof.*
In the bind pose $q_j = (1, 0, 0, 0)$, so $Q$ is the identity and $S(r) = v - r + r = v$.
For one joint, $Q = q_j$ (up to a sign that gives the same rotation), and $S(r) = R_j (v - r) + R_j r + t_j = C_j v$ for any $r$. $\square$

## Coordinate invariance

**Lemma 7.** Let $G x = G_R x + g$ be rigid, and replace $C_j$ by $G C_j G^{-1}$, $v$ by $G v$ and $n$ by $G_R n$.
Then the new result is $G S(r_c)$ and the new normal is $G_R Q n$.

*Proof.*
Let $\gamma$ be the unit quaternion of $G_R$.
The new joint quaternions are $\gamma q_j \gamma^*$, and $x \mapsto \gamma x \gamma^*$ is an orthogonal map of $\mathbb R^4$, so all dot products, and so the signs $s_j$, stay the same, and the new rotation is $\gamma Q \gamma^*$, that is $G_R Q G_R^\top$.
The new objective is $f'(r') = \sum \lvert G C_a G^{-1} r' - G C_b G^{-1} r' \rvert^2 = f(G^{-1} r')$, because $G$ keeps distances, so its minimizers are the images $G r$ of the minimizers $r$ of $f$.
By Lemma 4 we may evaluate the new result at $G r_c$:
$G_R Q G_R^\top (G v - G r_c) + \sum_j w_j G C_j r_c = G_R Q (v - r_c) + G_R\, m(r_c) + g = G S(r_c)$,
since $G v - G r_c = G_R (v - r_c)$ and $\sum_j w_j = 1$.
The normal is $G_R Q G_R^\top G_R n = G_R Q n$. $\square$

## Relation to linear blend skinning

**Lemma 8.** If $Q$ in line L8 is replaced by the matrix $A = \sum_j w_j R_j$, the result is $\sum_j w_j C_j v$ for any $r$.

*Proof.*
$A(v - r) + \sum_j w_j (R_j r + t_j) = \sum_j w_j R_j v - A r + A r + \sum_j w_j t_j = \sum_j w_j C_j v$. $\square$

## The twist check value

**Lemma 9.** Let $C_0 = I$, $C_1$ the turn by $\theta \in (0, \pi]$ about the $x$ axis, and the weights $\tfrac12, \tfrac12$.
Then $r_c = 0$, and SBS turns every vertex by $\theta / 2$ about the $x$ axis.
For $\theta = \pi$ it maps $(0, 1, 0)$ to $(0, 0, 1)$.

*Proof.*
$K$ is the $x$ axis and $g = 0$, so the minimal norm minimizer is $r_c = 0$ by Lemma 1.
$q_0 = (1, 0, 0, 0)$ and $q_1 = (\cos\tfrac\theta2, \sin\tfrac\theta2, 0, 0)$ with $q_0 \cdot q_1 = \cos\tfrac\theta2 \ge 0$, so no sign changes, and $b = \tfrac12 (1 + \cos\tfrac\theta2, \sin\tfrac\theta2, 0, 0)$.
With $1 + \cos\tfrac\theta2 = 2\cos^2\tfrac\theta4$ and $\sin\tfrac\theta2 = 2 \sin\tfrac\theta4 \cos\tfrac\theta4$, $Q = (\cos\tfrac\theta4, \sin\tfrac\theta4, 0, 0)$, the turn by $\theta / 2$.
$m(0) = 0$, so $S(0) = Q v$.
For $\theta = \pi$ this is the turn by $\pi / 2$, which maps $(0, 1, 0)$ to $(0, 0, 1)$. $\square$

Linear blend skinning maps the same vertex to $(0, 0, 0)$ for $\theta = \pi$, by Lemma 8 with $A = \tfrac12 (I + R_x(\pi))$.
