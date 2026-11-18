---
title: CoR skinning moves each vertex rigidly, keeps the bind pose and common rigid motions, and keeps the distance to a center that the joints fix
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact, the weights of each vertex and of each triangle are nonnegative with the sum 1, and each $C_j x = R_j x + t_j$ is rigid with the unit quaternion $q_j$.
For a vertex $i$, let $m(p) = \sum_j w_{ij} C_j p$, so that lines L8 and L9 give $v_i' = R (v_i - p_i) + m(p_i)$.

## The similarity

**Lemma 1.** $s(w_p, w_v) = s(w_v, w_p) \ge 0$, and $s(w_p, w_v) = 0$ if fewer than two joints have a positive weight in both vectors.

*Proof.*
Swapping $w_p$ and $w_v$ swaps the two products in $w_{pj} w_{vk} - w_{pk} w_{vj}$ and changes only its sign, which the square removes; the factor in front is symmetric.
Every term is a product of nonnegative numbers and an exponential.
A term for the pair $j < k$ is zero unless $w_{pj}, w_{pk}, w_{vj}, w_{vk}$ are all positive. $\square$

## The centers

**Lemma 2.** If $den > 0$ in line L5, then $p_i$ is a convex combination of the centroids $c_t$.
If the rest mesh is moved by a rigid motion $G$ and the weights are kept, the new center is $G p_i$.

*Proof.*
$p_i = \sum_t \lambda_t c_t$ with $\lambda_t = s(w_i, \bar w_t)\, a_t / den \ge 0$ and $\sum_t \lambda_t = 1$.
A rigid motion keeps the areas, maps each centroid $c_t$ to $G c_t$, and does not change the weights, so the $\lambda_t$ stay the same, and $\sum_t \lambda_t G c_t = G \sum_t \lambda_t c_t$ because $G$ is affine and $\sum_t \lambda_t = 1$.
If $den = 0$, the center is $v_i$, which moves to $G v_i$. $\square$

Each centroid lies in the convex hull of the mesh vertices, so $p_i$ does too.

## The rotation

**Lemma 3.** The sum in line L7 has a norm of at least the largest weight $w_{ip} > 0$, so $R$ is a rotation.

*Proof.*
With the pivot $q_p$ and the signs $s_j$ with $q_p \cdot s_j q_j \ge 0$, the sum $b$ satisfies $\lvert b \rvert \ge q_p \cdot b = \sum_j w_{ij}\, q_p \cdot s_j q_j \ge w_{ip}$.
A unit quaternion gives a rotation matrix. $\square$

## Rigid motion of each vertex

**Lemma 4.** For each vertex the frame step is $x \mapsto R x + t$ with a rotation $R$, so $\lvert R n_i \rvert = \lvert n_i \rvert$, and the center goes to $R p_i + t = m(p_i)$, its image under LBS.

*Proof.*
By lines L8 and L9, $R p_i + t = R p_i + m(p_i) - R p_i = m(p_i)$.
$R$ is a rotation by Lemma 3. $\square$

**Lemma 5.** In the bind pose, with all $C_j = I$, $v_i' = v_i$ and $n_i' = n_i$.
If all $C_j = G$ for one rigid $G x = G_R x + g$, then $v_i' = G v_i$ and $n_i' = G_R n_i$.

*Proof.*
If all $C_j = G$, then all $q_j$ are $\pm \gamma$ for the quaternion $\gamma$ of $G_R$, the aligned sum is $\gamma$ times a positive number, and $R = G_R$.
$m(p_i) = G p_i$, so $v_i' = G_R (v_i - p_i) + G p_i = G v_i$.
The bind pose is the case $G = I$. $\square$

**Lemma 6.** If only the joint $j$ has a positive weight for vertex $i$, then $v_i' = C_j v_i$.

*Proof.*
Then $R = R_j$ and $m(p) = C_j p$, so $v_i' = R_j (v_i - p_i) + R_j p_i + t_j = C_j v_i$ for any center. $\square$

By Lemma 1 such a vertex has $den = 0$, and line L5 sets $p_i = v_i$; Lemma 6 shows that the choice does not matter.

## Twist and bend about a fixed center

**Lemma 7.** If $C_j p_i = p_i$ for every joint $j$ of vertex $i$, then $\lvert v_i' - p_i \rvert = \lvert v_i - p_i \rvert$.

*Proof.*
$m(p_i) = p_i$, so $v_i' - p_i = R (v_i - p_i)$, and $R$ keeps lengths. $\square$

In the tube of the example, the twist and the bend fix every point of the joint axis or of the elbow line through $(0, 1, 0)$ for the two joints, and the centers of the middle ring are on that axis or line, so the middle ring keeps its distance to the center.
Linear blend skinning does not keep it: for the weights $\tfrac12, \tfrac12$ and the twist by $\pi$, it maps the vertex $(0.5, 1, 0)$ to $\tfrac12 (0.5, 1, 0) + \tfrac12 (-0.5, 1, 0) = (0, 1, 0)$.
