---
title: The pressure iteration converges to the discrete projection, and the explicit step has a step limit
proves: [correctness]
status: full
---

We use the 2D MAC layout and the line numbers of the page, with square cells of side $\Delta x$. All statements are in exact arithmetic. As in the paper, $p$ is the pressure divided by the density. The box walls are free-slip, so the normal velocity on a wall face is 0 and a relax step never changes it. A face of a cell is *open* if it is not on a wall. For a cell $c$, let $n_c \in \{2, 3, 4\}$ be its number of open faces, and let $F_c = \Delta x \, (\nabla \cdot \mathbf u)_c$ be the sum of the outward velocities over its faces. The paper's "missing mass" is $D_c = -F_c / \Delta x$ (its equation 5). We write $E = \frac12 \sum_f w_f^2$ for the kinetic energy of a face field $w$, per unit mass and cell area.

**Lemma 1 (labels, line L1).** After line L1, a FULL cell has no EMPTY neighbor in the grid, and a SURFACE cell has at least one. So the open faces of a FULL cell lead to FULL or SURFACE cells.

*Proof.* Line L1 marks a cell with a marker as SURFACE exactly when a neighbor in the grid has no marker, which is the EMPTY label. $\square$

**Lemma 2 (one cell update, lines L5 and L6).** Let $c$ be a FULL cell and $\omega_c = \beta_0 n_c / 4$. After one update of $c$, its divergence is multiplied by $1 - \omega_c$, and the kinetic energy changes by

$$\Delta E = -\frac{F_c^2}{2 n_c}\, \omega_c (2 - \omega_c).$$

So for $0 \le \beta_0 \le 2$ the energy never increases, and for $\beta_0 = 1$ an interior cell ($n_c = 4$) ends with zero divergence.

*Proof.* Line L5 sets $\delta p = \beta D_c$ with $\beta = \beta_0 \Delta x^2 / (4 \Delta t)$, which is equation 7 of the paper for $\delta x = \delta y = \Delta x$ in 2D. Line L6 adds $\frac{\Delta t}{\Delta x} \delta p$ to the outward velocity of each open face (it adds to $u_{i+1,j}$ and subtracts from $u_{i,j}$, and the outward direction of the left face is $-x$). That amount is $s = \frac{\Delta t}{\Delta x} \cdot \frac{\beta_0 \Delta x^2}{4 \Delta t} \cdot \left(-\frac{F_c}{\Delta x}\right) = -\frac{\beta_0}{4} F_c$. The wall faces do not change. So the new sum of outward velocities is $F_c + n_c s = (1 - \omega_c) F_c$. For the energy, let $w_1, \dots, w_{n_c}$ be the outward velocities of the open faces, with $\sum_k w_k = F_c$ (the wall faces carry 0). Each becomes $w_k - \omega_c F_c / n_c$, and no other face changes. Then

$$\Delta E = \frac12 \sum_k \left[\left(w_k - \frac{\omega_c F_c}{n_c}\right)^2 - w_k^2\right] = \frac12\left[-\frac{2 \omega_c F_c^2}{n_c} + \frac{\omega_c^2 F_c^2}{n_c}\right],$$

which is the formula. With $n_c \le 4$ and $0 \le \beta_0 \le 2$ we have $0 \le \omega_c \le 2$, so $\Delta E \le 0$. $\square$

The update is a step of [successive over-relaxation](/successive-over-relaxation/) on the pressure Poisson system, with the factor $\omega_c$ in place of $\beta_0$. For an interior cell the two are the same. Near a wall $\omega_c < \beta_0$, so a cell with two open faces needs $\beta_0 = 2$ to zero its divergence in one update. The paper's range $1 \le \beta_0 \le 2$ keeps every $\omega_c$ in $[\frac12, 2]$.

**Theorem 1 (the pressure iteration is a projection, lines L4 to L7).** Let $w^0$ be the face field after lines L2 and L3, and let $\mathcal F$ be the set of FULL cells. For each $c \in \mathcal F$ let $g_c$ be the face field that is $+1$ in the outward direction on each open face of $c$ and 0 elsewhere, so that $F_c(w) = \langle g_c, w \rangle$. Let $S$ be the span of the $g_c$. If $0 < \beta_0 < 2$, the sweeps of line L4 converge linearly to

$$w^\ast = w^0 - P_S w^0,$$

the orthogonal projection of $w^0$ onto the fields with zero divergence on every FULL cell. This is the field of least kinetic energy among $w^0 + S$, and it is the same field that `macgrid.project` gives with $\rho = 1$, when FULL cells are FLUID and all other cells are AIR. If every connected group of FULL cells touches a SURFACE cell, the accumulated pressure in the FULL cells also converges to the pressure of the helper.

*Proof.* By Lemma 2, an update of $c$ changes $w$ by a multiple of $g_c$, so every iterate lies in $w^0 + S$. A field $w$ has zero divergence on all FULL cells exactly when $\langle g_c, w \rangle = 0$ for all $c$, that is, when $w \in S^\perp$. The set $(w^0 + S) \cap S^\perp$ has the single point $w^\ast = w^0 - P_S w^0$, and by the Pythagorean rule it has the least norm in $w^0 + S$.

Let $e = w - w^\ast \in S$ be the error. Since $\langle g_c, w^\ast \rangle = 0$ and $\|g_c\|^2 = n_c$, the update of Lemma 2 is $w \leftarrow w - \omega_c \frac{\langle g_c, w \rangle}{n_c} g_c$, so $e \leftarrow (I - \omega_c P_c) e$, where $P_c$ is the orthogonal projection onto $g_c$. Then $\|(I - \omega_c P_c) e\|^2 = \|e\|^2 - \omega_c (2 - \omega_c) \|P_c e\|^2$. For $0 < \beta_0 < 2$ we have $0 < \omega_c < 2$, since $n_c \ge 2$ on a grid of at least 2 by 2 cells. Let $T$ be the product of these maps over one sweep. $T$ maps $S$ into $S$, and $\|T e\| \le \|e\|$. If $\|T e\| = \|e\|$, then each factor keeps the norm, so $P_c e = 0$ at each stage, so no stage changes $e$, and $\langle g_c, e \rangle = 0$ for all $c$. Then $e \in S \cap S^\perp = \{0\}$. The unit sphere of the finite-dimensional space $S$ is compact, so $q = \max \{\|T e\| : e \in S, \|e\| = 1\} < 1$, and $\|e^k\| \le q^k \|e^0\|$ after $k$ sweeps. The divergence of each FULL cell is $\langle g_c, e^k \rangle / \Delta x$, so it goes to 0 and line L7 stops after finitely many sweeps for any $\varepsilon > 0$.

For the helper, write its projection as $w' = w^0 - \frac{\Delta t}{\rho} G p$ with $\rho = 1$. On an open face from a FLUID cell $c$ to a neighbor $n$, the outward component of $G p$ is $(p_n - p_c)/\Delta x$, with $p_n = 0$ for an AIR cell. So $w' = w^0 + \frac{\Delta t}{\Delta x} \sum_c p_c\, g_c \in w^0 + S$, and the helper proves that $w'$ has zero divergence on every FLUID cell, so $w' \in S^\perp$. By Lemma 1 the open faces of a FULL cell go to FULL or SURFACE cells, so the two methods have the same cells, the same faces and the same set $S$. Hence $w' = w^\ast$. Lines L5 and L6 add $\delta p$ to $p_c$ and move $w$ by $\frac{\Delta t}{\Delta x} \delta p \, g_c$, so the iterate is $w^0 + \frac{\Delta t}{\Delta x} \sum_c p_c\, g_c$ with the accumulated $p$, the same form. The Gram matrix $\langle g_c, g_{c'} \rangle$ is the 5-point matrix of the helper: $n_c$ on the diagonal and $-1$ for two FULL neighbors. If each connected group of FULL cells touches a SURFACE cell, that matrix is positive definite, the $g_c$ are linearly independent, and the coefficients of $w^\ast$ in this basis are unique. Then the accumulated $p$ converges to the pressure of the helper. In a closed box the $g_c$ of a closed group sum to zero, and the two pressures can differ by a constant on that group. $\square$

The tests compare the two methods at $\varepsilon = 10^{-10}$: the velocities agree to about $10^{-11}$ in a closed 16 by 16 box and in a 10 by 10 box with a free surface, and the pressures agree to $4.3 \times 10^{-10}$ in the second case.

**Lemma 3 (the free surface rules, line L8).** After line L8, a SURFACE cell with one open face toward an EMPTY cell, or with two such faces, has zero divergence. A cell with three such faces has zero divergence along the axis of the closed face only.

*Proof.* One face (equation 10 of the paper): the rule solves $u_{i+1,j} - u_{i,j} + v_{i,j+1} - v_{i,j} = 0$ for the open face. Two faces on different axes: each open face copies the face opposite it, so $u_{i+1,j} = u_{i,j}$ and $v_{i,j+1} = v_{i,j}$, and both differences are 0. This is the paper's rule $\partial u / \partial x = 0$ and $\partial v / \partial y = 0$ separately. Two faces on the same axis, a case the paper does not state: the code sets them to $m \mp h$ with $2h = -(v_{i,j+1} - v_{i,j})$, so their difference cancels the other axis. Three faces: the face opposite the closed face copies it, so that axis has zero difference. The other two faces keep the values of equation 2, as in the paper, where they follow the body force. $\square$

**Lemma 4 (hydrostatic rest, lines L2 and L3).** Let all velocities be 0, let the FULL cells fill the rows $0, \dots, h-1$ and the SURFACE cells fill row $h$, and let $p_{i,j} = |g_y| (h - j) \Delta x$ in the FULL cells. Then lines L2 to L8 keep every velocity at 0.

*Proof.* With zero velocity, all advection and viscous terms are 0. On a $v$ face between two FULL rows, line L3 gives $\frac{\Delta t}{\Delta x} (p_{i,j-1} - p_{i,j}) + \Delta t\, g_y = \frac{\Delta t}{\Delta x} |g_y| \Delta x - \Delta t |g_y| = 0$. On the face between row $h - 1$ and the SURFACE row, the SURFACE cell has $p = 0$ and the same sum is 0. On a $u$ face both pressures are equal. So $w^0$ is 0 below row $h$. The face between the SURFACE row and the EMPTY row gets $\Delta t\, g_y$. Every FULL cell has zero divergence, so line L7 does no sweep. Each SURFACE cell then has one open face, the top one, and Lemma 3 sets it to $v_{i,h} - 0 = 0$. $\square$

The surface pressure is placed at the center of the SURFACE cell. The test of a still pool runs 40 steps and finds velocities below $10^{-9}$. The paper gives no proof of this property.

**Theorem 2 (the explicit step has a limit).** The paper states the limit $\max(u \delta t / \delta x, v \delta t / \delta y, w \delta t / \delta z) < 1$ of its equation 3. That condition is needed for the markers, but it does not alone make lines L2 and L3 stable. On a periodic grid, linearized about a constant velocity, with $c = u \Delta t / \Delta x$ and $r = \nu \Delta t / \Delta x^2$:

1. The viscous term alone, in 2D, is stable if and only if $r \le \frac14$.
2. In 1D, central advection and the viscous term together are stable if and only if $c^2 \le 2r \le 1$.
3. With $\nu = 0$, central advection is unstable at every $\Delta t > 0$. Over a time $T$, the growth factor is at most $\exp(T u^2 \Delta t / (2 \Delta x^2))$.

*Proof.* Each part is a von Neumann analysis: a Fourier mode $e^{\mathrm i (k_1 a + k_2 b)}$ is multiplied by a factor $G$ per step, and the step is stable if and only if $|G| \le 1$ for all modes.

1. The 5-point update $w \leftarrow w + r(\text{sum of the four neighbors} - 4w)$ has $G = 1 - 4r (\sin^2 \frac{\theta_1}{2} + \sin^2 \frac{\theta_2}{2})$, which takes all values in $[1 - 8r, 1]$. The least is $1 - 8r$, at the checkerboard $\theta_1 = \theta_2 = \pi$. So $|G| \le 1$ if and only if $r \le \frac14$.
2. Central differences give $G = 1 - \mathrm i c \sin \theta - 2 r (1 - \cos \theta)$. Put $\sigma = 1 - \cos \theta \in [0, 2]$, so $\sin^2 \theta = \sigma (2 - \sigma)$. Then $|G|^2 = (1 - 2 r \sigma)^2 + c^2 \sigma (2 - \sigma)$, and
$$|G|^2 - 1 = \sigma \left[(2c^2 - 4r) + \sigma (4 r^2 - c^2)\right].$$
The bracket is linear in $\sigma$, so it is $\le 0$ on $[0, 2]$ exactly when it is $\le 0$ at both ends. As $\sigma \to 0$ the condition is $c^2 \le 2r$, and at $\sigma = 2$ it is $4r(2r - 1) \le 0$, that is $r \le \frac12$.
3. With $r = 0$, $|G|^2 = 1 + c^2 \sin^2 \theta > 1$ for $\sin \theta \ne 0$ and $c \ne 0$. After $N = T / \Delta t$ steps, $|G|^N \le (1 + c^2)^{N/2} \le \exp(N c^2 / 2) = \exp(T u^2 \Delta t / (2 \Delta x^2))$. $\square$

So a small step keeps the growth small even without viscosity, and the second condition, $\Delta t \le 2 \nu / u^2$, can be stronger than equation 3 when $\nu$ is small. These are statements about a linear model problem; the paper's equation 2 is nonlinear and has walls and a free surface. The test file checks the first claim through the full code on a 10 by 10 box: a checkerboard in $u$ falls to $0.002$ of its size after 30 steps at $r = 0.2$, to $0.35$ at $r = 0.25$, and grows by a factor of about $10^4$ at $r = 0.3$.

**Lemma 5 (markers, line L9).** Each marker moves by $\Delta t$ times the bilinear interpolation of the four nearest values of each component, which is the area weighting of the paper. The number of markers does not change, and every marker stays inside the box.

*Proof.* Line L9 calls the helper's `vel_at`, which is bilinear sampling, and then clamps each coordinate to $[10^{-6} \Delta x, \; n \Delta x - 10^{-6} \Delta x]$. No marker is created or removed. $\square$

The markers do not take part in the velocity computation, as the paper says. They only decide the labels at line L1. So the liquid volume is not conserved exactly: it is the number of cells that hold a marker, and it can change when markers bunch up or spread out.
