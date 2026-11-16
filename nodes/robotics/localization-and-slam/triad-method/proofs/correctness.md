---
title: TRIAD returns a rotation that matches the first pair exactly and recovers the true attitude from noise-free data
proves: [correctness]
status: full
---

**Setting.** The input is two body vectors $b_1, b_2$ and two reference vectors $r_1, r_2$ in $\mathbb{R}^3$. For a pair of vectors $v_1, v_2$, lines L1 to L5 build

$$t_1 = \frac{v_1}{|v_1|}, \qquad t_2 = \frac{v_1 \times v_2}{|v_1 \times v_2|}, \qquad t_3 = t_1 \times t_2,$$

and $T(v_1, v_2)$ is the matrix with columns $t_1, t_2, t_3$. Line L6 returns $A = T_b T_r^T$ with $T_b = T(b_1, b_2)$ and $T_r = T(r_1, r_2)$. The word rotation means an element of $SO(3)$, a real $3 \times 3$ matrix $Q$ with $Q^T Q = I$ and $\det Q = 1$.

**Assumptions.**

- (N) $v_1 \times v_2 \ne 0$ for both pairs, that is, no vector is zero and the two vectors of a pair are not parallel. Line L3 tests this and raises an error otherwise.
- (E) For the third claim only: there is a rotation $A_0$ and scalars $s_1, s_2 > 0$ with $b_i = s_i A_0 r_i$.

**Claim.**

1. $A$ is a rotation.
2. $A r_1 / |r_1| = b_1 / |b_1|$.
3. $A r_2$ lies in the plane spanned by $b_1$ and $b_2$, on the same side of the line of $b_1$ as $b_2$, and the angle from $b_1$ to $A r_2$ equals the angle from $r_1$ to $r_2$.
4. Under (E), $A = A_0$.
5. Without (N), no rotation is determined by the data: if $b_1 \times b_2 = 0$ and $r_1 \times r_2 = 0$ with nonzero vectors, and $A$ maps $r_1$ to the direction of $b_1$, then so does $A$ followed by any rotation about $b_1$.

*Proof.*

*Claim 1.* By (N), $t_1$ and $t_2$ are well defined unit vectors. The vector $v_1 \times v_2$ is orthogonal to $v_1$, so $t_1 \cdot t_2 = 0$. The cross product of two orthogonal unit vectors is a unit vector orthogonal to both, so $t_1, t_2, t_3$ are orthonormal and $T^T T = I$. Also $\det T = t_1 \cdot (t_2 \times t_3)$. By the rule $a \times (b \times c) = b (a \cdot c) - c (a \cdot b)$, $t_2 \times (t_1 \times t_2) = t_1 (t_2 \cdot t_2) - t_2 (t_2 \cdot t_1) = t_1$, so $\det T = t_1 \cdot t_1 = 1$. So $T_b$ and $T_r$ are rotations, and $A = T_b T_r^T$ is a rotation, because $SO(3)$ is closed under products and transposes.

*Claim 2.* Since $T_r$ is orthogonal, $T_r^T t_{r,1} = e_1$, so $A t_{r,1} = T_b e_1 = t_{b,1}$. This is $A r_1 / |r_1| = b_1 / |b_1|$.

*Claim 3.* The same argument gives $A t_{r,k} = t_{b,k}$ for $k = 2, 3$. For any pair, we show that

$$\frac{v_2}{|v_2|} = \cos\theta \, t_1 - \sin\theta \, t_3,$$

where $\theta \in (0, \pi)$ is the angle from $v_1$ to $v_2$. To see this, write $v_2 / |v_2| = \cos\theta \, t_1 + w$ with $w \perp t_1$ and $|w| = \sin\theta$. Then $v_1 \times v_2$ is a positive multiple of $t_1 \times w$, so $t_2 = t_1 \times w / |w|$. By the triple product rule, $t_1 \times (t_1 \times w) = t_1 (t_1 \cdot w) - w = -w$, so $t_3 = -w / |w|$. Apply this to the reference pair, with angle $\theta_r$, and apply $A$:

$$\frac{A r_2}{|r_2|} = \cos\theta_r \, t_{b,1} - \sin\theta_r \, t_{b,3}.$$

The vectors $t_{b,1}$ and $-t_{b,3}$ span the plane of $b_1$ and $b_2$, and $-t_{b,3}$ points to the side of $b_2$. So $A r_2$ is in that plane, on the side of $b_2$, at the angle $\theta_r$ from $b_1$.

*Claim 4.* For a rotation $Q$ and vectors $x, y$, $(Q x) \times (Q y) = Q (x \times y)$, and $|Q x| = |x|$. Under (E), $b_1 \times b_2 = s_1 s_2 A_0 (r_1 \times r_2)$, so each line L1 to L5 for the body pair gives $A_0$ times the result for the reference pair: $t_{b,k} = A_0 t_{r,k}$. So $T_b = A_0 T_r$ and $A = A_0 T_r T_r^T = A_0$. The scalars $s_i$ drop out because each line normalizes.

*Claim 5.* Let $R_\phi$ be the rotation by $\phi$ about the unit vector $u = b_1 / |b_1|$. Then $R_\phi u = u$, so $R_\phi A r_1 / |r_1| = u$. Since $b_2$ is parallel to $b_1$ and $r_2$ is parallel to $r_1$, the second pair is matched by $R_\phi A$ exactly when it is matched by $A$. So every $R_\phi A$ fits the data equally well, and the data do not fix the rotation about $b_1$. $\blacksquare$

**Remarks.**

- Claims 2 and 3 show where the noise goes. All of the error of the pair $(b_2, r_2)$ is put on the second pair: $A r_2$ misses $b_2$ by the angle $|\theta_b - \theta_r|$ inside the plane of $b_1$ and $b_2$, and $A r_1$ is exact. A least-squares solution of [Wahba's problem](/wahba-problem/) shares the error between the pairs, so TRIAD is not its minimizer when $\theta_b \ne \theta_r$. Claim 4 shows that the two agree when the data are exact.
- In floating point, line L3 uses the relative test $|v_1 \times v_2| \le \tau |v_1| |v_2|$ with $\tau = 10^{-12}$. Near that limit, $t_2$ is the normalized difference of nearly equal products, and its relative error grows like $\varepsilon / \sin\theta$ for unit roundoff $\varepsilon$. This is the same loss of accuracy that noise causes, scaled up by $1 / \sin\theta$.
