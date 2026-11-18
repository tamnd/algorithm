---
title: The normalized dual quaternion blend is rigid when its real part is not zero, and the pivot alignment keeps the real part away from zero
proves: [correctness]
status: full
---

We use the notation of the page.
Quaternions are in the Hamilton convention, scalar first, and $p \cdot q$ is the dot product in $\mathbb R^4$.
A dual quaternion is $a + \varepsilon b$ with quaternions $a$, $b$ and $\varepsilon^2 = 0$.
For a rotation quaternion $r$ ($|r| = 1$) and a translation $t$, written as the pure quaternion $(0, t)$, the joint has $\sigma = r + \varepsilon d$ with $d = \tfrac12 t r$.
The arithmetic is exact.

## Unit dual quaternions are rigid transforms

**Lemma 1.** For $|r| = 1$ and $d = \tfrac12 t r$ with a pure $t$, $r \cdot d = 0$ and $2 d r^* = t$.

*Proof.*
$2 d r^* = t r r^* = t$.
For quaternions, $p \cdot q$ is the scalar part of $p q^*$, so $r \cdot d$ is the scalar part of $d r^* = \tfrac12 t$, which is 0 because $t$ is pure. $\square$

**Lemma 2.** Let $|c_0| = 1$ and $c_0 \cdot c_\varepsilon = 0$.
Then $t = 2 c_\varepsilon c_0^*$ is a pure quaternion, and the map $v \mapsto c_0 v c_0^* + t$ of line L11 is a rotation followed by a translation.

*Proof.*
The scalar part of $c_\varepsilon c_0^*$ is $c_\varepsilon \cdot c_0 = 0$, so $t$ is pure.
For a unit $c_0$, $v \mapsto c_0 v c_0^*$ is the rotation of [unit quaternion rotation](/unit-quaternion-rotation/), and adding a fixed vector is a translation. $\square$

## The normalization of line L9

**Lemma 3.** If $b_0 \ne 0$, line L9 gives $|c_0| = 1$ and $c_0 \cdot c_\varepsilon = 0$.

*Proof.*
$|c_0| = |b_0| / |b_0| = 1$.
Write $e = b_\varepsilon / |b_0|$.
Then $c_\varepsilon = e - (c_0 \cdot e) c_0$, and $c_0 \cdot c_\varepsilon = c_0 \cdot e - (c_0 \cdot e)(c_0 \cdot c_0) = 0$. $\square$

**Lemma 4.** The removed term does not change the translation: $2 e c_0^*$ and $2 c_\varepsilon c_0^*$ have the same vector part.

*Proof.*
$2 c_\varepsilon c_0^* = 2 e c_0^* - 2 (c_0 \cdot e) c_0 c_0^* = 2 e c_0^* - 2 (c_0 \cdot e)$, and $2(c_0 \cdot e)$ is a real number. $\square$

By Lemmas 2 and 3, every vertex with $b_0 \ne 0$ moves by a rigid transform, and its normal is rotated by $c_0$, so it keeps unit length.

## The real part after the pivot alignment

**Lemma 5.** Let $p = r_m$ be the quaternion of an influence $m$ with weight $w_m > 0$, and let $s_j = -1$ if $p \cdot r_j < 0$ and $s_j = 1$ otherwise, as in line L6.
Then $|b_0| \ge w_m$.

*Proof.*
By lines L6 and L7, $b_0 \cdot p = \sum_j w_j s_j (r_j \cdot p) = \sum_j w_j |r_j \cdot p| \ge w_m |r_m \cdot r_m| = w_m$, because every term is nonnegative.
By the Cauchy-Schwarz inequality and $|p| = 1$, $|b_0| \ge b_0 \cdot p$. $\square$

So line L8 never fails when the pivot is one of the influences, and the code uses the largest weight, which is at least $1/k$.
Without alignment the bound fails: the weights $\tfrac12$ and $\tfrac12$ on $r$ and $-r$, which are the same rotation, give $b_0 = 0$.

## Special cases

**Lemma 6.** If a vertex has one influence $j$ with $w_j = 1$, the result is $P_j v$.

*Proof.*
The pivot is $r_j$ and $s_j = 1$, so $b = \sigma_j$.
By Lemma 1, $|b_0| = 1$ and $b_0 \cdot b_\varepsilon = 0$, so line L9 gives $c = \sigma_j$, and by Lemma 1 line L11 applies the rotation $r_j$ and the translation $t_j$, which is $P_j$. $\square$

In the bind pose every $P_j = I$, so every vertex has $c = 1$ and stays at its rest position.

**Lemma 7.** If every $r_j = 1$, the vertex moves by the translation $\sum_j w_j t_j$.

*Proof.*
All signs are 1 and $b_0 = \sum_j w_j = 1$.
$b_\varepsilon = \sum_j w_j \tfrac12 t_j$ is pure, so $c_\varepsilon = b_\varepsilon$ and $t = 2 c_\varepsilon = \sum_j w_j t_j$. $\square$

**Lemma 8.** Let $G = g_0 + \varepsilon g_\varepsilon$ be a unit dual quaternion.
If every $\sigma_j$ is replaced by $G \sigma_j G^*$ (with the dual quaternion conjugate), the normalized blend is replaced by $G c G^*$.

*Proof.*
The real part of $G \sigma_j G^*$ is $g_0 r_j g_0^*$, and $(g_0 r_j g_0^*) \cdot (g_0 r_m g_0^*) = r_j \cdot r_m$, because a map $q \mapsto g_0 q g_0^*$ is a rotation of $\mathbb R^4$.
So the pivot and the signs are the same.
The map $\sigma \mapsto G \sigma G^*$ is linear, so the blend becomes $G b G^*$, with the real part $g_0 b_0 g_0^*$ of the same length.
Line L9 divides by the dual norm $\lVert b \rVert = |b_0| + \varepsilon\,(b_0 \cdot b_\varepsilon)/|b_0|$, and the dual norm is multiplicative with $\lVert G \rVert = \lVert G^* \rVert = 1$.
So $\lVert G b G^* \rVert = \lVert b \rVert$, and the normalized blend is $G b G^* / \lVert b \rVert = G c G^*$. $\square$

This is the coordinate invariance of Kavan et al. (2008, Lemma 2): skinning in a world frame moved by $G$ gives the same mesh moved by $G$.

## The twist check value

With $r_1 = 1$, $r_2 = (0, 1, 0, 0)$ (the rotation $R_x(\pi)$) and the weights $\tfrac12$ and $\tfrac12$, $r_1 \cdot r_2 = 0$, so the signs are 1, $b_0 = (\tfrac12, \tfrac12, 0, 0)$, and $c_0 = (\cos\frac\pi4, \sin\frac\pi4, 0, 0)$, the rotation by $\pi/2$ about $x$.
It maps $(0, 1, 0)$ to $(0, 0, 1)$, at the distance 1 from the axis.
For a twist by $\theta \in [0, \pi]$, the same computation gives the rotation by $\theta / 2$.
