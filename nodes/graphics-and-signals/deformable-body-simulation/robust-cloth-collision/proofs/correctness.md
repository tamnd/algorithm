---
title: The impulses keep the momentum, the cubic finds every contact time, and the impact zones end with no collision
proves: [correctness]
status: full
---

We use the notation of the page. Node $j$ has mass $m_j > 0$, start position $\mathbf x_j$ and mean velocity $\mathbf v_j$ for a step of length $\Delta t$, and moves on $\mathbf x_j(s) = \mathbf x_j + s\, \Delta t\, \mathbf v_j$, $s \in [0, 1]$. A *pair* is a node and a triangle that does not contain it, or two edges with no common node. A *contact* of a pair at time $s$ is a common point of its two parts at that time. All statements are in exact arithmetic, except where the last section says otherwise.

A pair has four nodes $j_1, \dots, j_4$ and weights $c_1, \dots, c_4$ with $\sum_k c_k = 0$: $(1, -w_1, -w_2, -w_3)$ for a node and a triangle with barycentric weights $w$, and $(1 - a, a, -(1 - b), -b)$ for two edges with closest points at $a$ and $b$. The relative position is $\sum_k c_k \mathbf x_{j_k}$ and the relative velocity is $\mathbf u = \sum_k c_k \mathbf v_{j_k}$.

## Impulses

**Lemma 1.** Let $W = \sum_k c_k^2 / m_{j_k}$. The update $\mathbf v_{j_k} \mathrel{+}= c_k\, \Delta\mathbf u / (m_{j_k} W)$ changes the relative velocity by exactly $\Delta \mathbf u$ and does not change the linear momentum $\sum_j m_j \mathbf v_j$. For equal masses $m$, a point-triangle pair and $\Delta\mathbf u = \Delta v_N\, \hat{\mathbf n}$, the point gets $\tilde I/m\, \hat{\mathbf n}$ and triangle node $i$ gets $-w_i \tilde I/m\, \hat{\mathbf n}$ with $\tilde I = 2I/(1 + \sum w_i^2)$ and $I = m\, \Delta v_N / 2$, which is the weighting of Bridson, Fedkiw and Anderson (2002, Section 7.1).

*Proof.* The relative velocity changes by $\sum_k c_k \cdot c_k \Delta\mathbf u/(m_{j_k} W) = \Delta\mathbf u$. The momentum changes by $\sum_k m_{j_k} c_k \Delta\mathbf u/(m_{j_k} W) = (\Delta\mathbf u / W) \sum_k c_k = 0$. For equal masses $W = (1 + \sum w_i^2)/m$, and the point gets $\Delta v_N/(1 + \sum w_i^2) = 2I/(m(1 + \sum w_i^2)) = \tilde I/m$; triangle node $i$ gets $-w_i$ times this. $\square$

Every change of velocity in the method (lines L3, L4, L5, L9) is an update of Lemma 1, and the rigid motion of a zone keeps the momentum of the zone (Lemma 4). So the method keeps the linear momentum exactly.

**Lemma 2.** Take one close pair in isolation, with unit normal $\hat{\mathbf n}$, overlap $d > 0$ and normal relative velocity $v_N$. After lines L3 and L4 the normal relative velocity is

$$v_N' = \begin{cases} \min(\Delta t\, k\, d / m_{\rm eff},\ 0.1 d/\Delta t) & v_N < 0, \\ v_N + \min(\Delta t\, k\, d / m_{\rm eff},\ 0.1 d/\Delta t - v_N) & 0 \le v_N < 0.1 d / \Delta t, \\ v_N & v_N \ge 0.1 d/\Delta t, \end{cases}$$

with $m_{\rm eff} = 1/W$. So $v_N' \ge 0$, and the spring part never makes $v_N'$ larger than $\max(v_N, 0.1 d/\Delta t)$. Line L5 lowers the tangential relative speed $|\mathbf u_T|$ by $\min(\mu\, \Delta v_N, |\mathbf u_T|)$ with $\Delta v_N = v_N' - v_N$, keeps its direction, and does not change $v_N'$.

*Proof.* By Lemma 1, L3 sets $v_N$ to $0$ when it is negative, and L4 adds $\min(\Delta t k d/m_{\rm eff}, 0.1 d/\Delta t - v_N)$ when this is positive; the three cases follow. The friction update of L5 is $\Delta\mathbf u = -\min(\mu \Delta v_N, |\mathbf u_T|)\, \mathbf u_T / |\mathbf u_T|$, which is orthogonal to $\hat{\mathbf n}$, so by Lemma 1 it only changes the tangential part, by that amount. $\square$

The lemma holds for one pair. The code treats the pairs one after the other, so a later pair can change the velocity of an earlier pair again. The page does not claim more for many pairs; the later stages do not depend on it.

## Continuous detection

**Lemma 3.** If a pair has a contact at time $s^\ast \in [0, 1]$, then $s^\ast$ is a root of the cubic $f(s) = (\mathbf x_{21}(s) \times \mathbf x_{31}(s)) \cdot \mathbf x_{41}(s)$, and, if $f$ is not the zero polynomial, the list of candidate times holds $s^\ast$ or, for a root of odd multiplicity inside a monotone piece, the limit of a bisection that brackets $s^\ast$.

*Proof.* At a contact the four nodes lie in one plane, so the volume $f(s^\ast)$ is $0$. The coefficients of `coplanarity_cubic` are those of the product of the three linear vector polynomials (the test compares $f$ with the volume at four times). Between two consecutive points of $\{0, 1\}$ and the roots of $f'$ in $(0, 1)$, $f$ is monotone, so it has at most one root there or is constant. A root at a knot is kept by the test $f = 0$. A root inside a piece where $f$ changes sign is bracketed, and the bisection keeps the bracket. A root inside a piece where $f$ does not change sign would be a local extremum of $f$ inside the piece, which is a root of $f'$, so it is a knot. $\square$

The code then tests proximity at the candidates in increasing order with the tolerance $10^{-6}$ (Section 6 of the paper), so the first candidate that passes is the first contact up to the length of the bracket. The test compares this time with fine sampling of the sign of the volume, bisection and the same proximity test.

## Rigid impact zones in 3D

For a zone $Z$, let $\mathbf x_{cm}$ and $\mathbf v_{cm}$ be the mass-weighted means, $\mathbf r_i = \mathbf x_i - \mathbf x_{cm}$, $\mathbf L = \sum m_i \mathbf r_i \times (\mathbf v_i - \mathbf v_{cm})$, $\mathbf I = \sum m_i (|\mathbf r_i|^2 E - \mathbf r_i \mathbf r_i^{\mathsf T})$ and $\boldsymbol\omega = \mathbf I^{-1}\mathbf L$. With $\theta = \Delta t |\boldsymbol\omega|$ and $R$ the rotation by $\theta$ about $\boldsymbol\omega$, Section 7.5 of the paper sets the end position $\mathbf y_i = \mathbf x_{cm} + \Delta t\, \mathbf v_{cm} + R\, \mathbf r_i$, which is the formula with $\mathbf x_F$ and $\mathbf x_R$. The code uses $\theta = 0$ if $\theta \ge \pi$ or $\mathbf I$ is singular.

**Lemma 4.** (a) If $\mathbf v_i = \mathbf u + \boldsymbol\omega_0 \times (\mathbf x_i - \mathbf c)$ and $\mathbf I$ is invertible, then $\boldsymbol\omega = \boldsymbol\omega_0$. (b) $\sum m_i (\mathbf y_i - \mathbf x_i)/\Delta t = \sum m_i \mathbf v_i$. (c) $\mathbf y_i - \mathbf y_j = R(\mathbf x_i - \mathbf x_j)$. (d) If $\theta < \pi$, the nodes of the zone have no contact among themselves at any $s \in [0, 1]$ when they have none at $s = 0$.

*Proof.* (a) $\mathbf v_i - \mathbf v_{cm} = \boldsymbol\omega_0 \times \mathbf r_i$, and $\mathbf r \times (\boldsymbol\omega_0 \times \mathbf r) = (|\mathbf r|^2 E - \mathbf r \mathbf r^{\mathsf T})\boldsymbol\omega_0$, so $\mathbf L = \mathbf I \boldsymbol\omega_0$. (b) $\sum m_i \mathbf r_i = 0$, so $\sum m_i(\mathbf y_i - \mathbf x_i) = m\, \Delta t\, \mathbf v_{cm} + (R - E)\sum m_i \mathbf r_i = m\, \Delta t\, \mathbf v_{cm}$. (c) is direct. (d) The nodes move on $\mathbf x_i(s) = \mathbf x_{cm} + s\, \Delta t\, \mathbf v_{cm} + T_s \mathbf r_i$ with $T_s = (1 - s)E + sR$, one affine map for all nodes. $R$ is orthogonal, so it is normal with eigenvalues $1$ and $e^{\pm i\theta}$, and $T_s$ is normal with eigenvalues $1$ and $(1 - s) + s e^{\pm i \theta}$. These are $0$ only if $s \sin\theta = 0$ and $(1 - s) + s\cos\theta = 0$, which for $0 \le \theta < \pi$ has no solution. So $T_s$ is invertible. An invertible affine map keeps points, segments and triangles and the incidence between them, so a contact at time $s$ would give a contact at time $0$. $\square$

## Termination and the result

**Theorem 5.** Let the start state have no contact, and let no pair have the zero cubic. The method ends. The failsafe makes at most $n - 1$ passes that find collisions, and at the end no pair has a contact on the paths.

*Proof.* Stage 1 visits each pair once, and stage 2 makes at most $P$ passes. In stage 3, every collision that the code finds has nodes in at least two zones, because pairs with all four nodes in one zone are skipped. Line L13 merges these zones, so each pass with a collision lowers the number of zones by at least one. There are at most $n$ zones, so there are at most $n - 1$ such passes, and the loop stops at the first pass that finds no collision. At that pass, Lemma 3 says that no pair with nodes in two zones has a contact. A pair in one zone is rigid if the zone has more than one node, and by Lemma 4 (d) it has no contact either. $\square$

**Corollary 6.** The end state $\mathbf x_j(1)$ has no edge that meets a triangle with no common node. Whether a segment meets a triangle can change during the step only at a time when an endpoint of the segment lies on the triangle or the segment touches an edge of the triangle. Both are contacts of pairs, and the start state has no intersection, so the end state has none. The tests check this with an exact test in rational arithmetic.

## What is not claimed

- **Plausible motion.** The page does not claim that the result is the motion of real cloth. The stiffness $k$ matched to the stretch springs, the cap $0.1 d/\Delta t$ and the number of passes $P$ are heuristics of Bridson et al. or choices of this code. The impact zones remove all relative motion inside a zone and keep the angular momentum only to $O(\theta^2)$, as in the 2D case.
- **The zero cubic.** If the four nodes of a pair stay in one plane for the whole step, Lemma 3 gives no times, and the code tests 65 evenly spaced times. A short contact between them can be missed.
- **Rounding.** Lemma 3 and Lemma 4 hold in exact arithmetic. In floating point the code accepts a contact within $10^{-6}$ at a coplanar time, and the thickness $h$ of the repulsions keeps most pairs far from this limit. The tests check the result with exact arithmetic, not the proof.
- **Order.** Stages 1 and 2 apply impulses one pair at a time, so their result depends on the order of the pairs. Only stage 3 does not.
