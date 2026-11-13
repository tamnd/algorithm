---
title: Mirtich's reduction gives the exact volume integrals
proves: [correctness]
status: full
---

Let $V$ be a bounded solid whose boundary is a closed surface made of planar faces $f$, each a simple polygon with its vertices in counterclockwise order seen from outside. For a face, let $n$ be its Newell normal, $\hat n = n/|n|$ the unit outward normal, and $w = -n \cdot p_0$, so that $n \cdot p + w = 0$ on the plane of $f$. We show that lines L1 to L8 return $T_0 = \int_V 1$, $T_1 = (\int_V x, \int_V y, \int_V z)$, $T_2 = (\int_V x^2, \int_V y^2, \int_V z^2)$ and $TP = (\int_V xy, \int_V yz, \int_V zx)$.

**Lemma 1 (Newell normal).** $n$ is a positive multiple of $\hat n$, and for each coordinate $\gamma$ with cyclic successors $\alpha, \beta$, $n_\gamma$ is twice the signed area of the projection of $f$ onto the $(\alpha, \beta)$ plane.

*Proof.* Take $\gamma = z$; the other cases follow by a cyclic shift. Line L3 computes $n_z = \sum_i (x_i - x_{i+1})(y_i + y_{i+1})$, indices mod $k$. Expanding, $n_z = \sum_i (x_i y_{i+1} - x_{i+1} y_i) + \sum_i (x_i y_i - x_{i+1} y_{i+1})$. The second sum telescopes to $0$, and the first is twice the signed area of the projected polygon by the shoelace formula. The signed area of the projection of a planar region onto the $(\alpha, \beta)$ plane is the area of the region times $\hat n_\gamma$, so $n = 2 \operatorname{area}(f) \hat n$. $\square$

**Lemma 2 (divergence step).** $T_0 = \sum_f \hat n_x \int_f x \, dA$, $\int_V x = \frac{1}{2} \sum_f \hat n_x \int_f x^2 \, dA$, $\int_V x^2 = \frac{1}{3} \sum_f \hat n_x \int_f x^3 \, dA$ and $\int_V xy = \frac{1}{2} \sum_f \hat n_x \int_f x^2 y \, dA$, and the same with $x, y, z$ shifted cyclically.

*Proof.* A polyhedron is a bounded domain with a piecewise smooth boundary, so the divergence theorem $\int_V \nabla \cdot F = \int_{\partial V} F \cdot \hat n \, dA$ holds for each polynomial field $F$. The boundary is the union of the faces, which meet only along edges of zero area. Apply it to $F = (x, 0, 0)$, $(x^2/2, 0, 0)$, $(x^3/3, 0, 0)$ and $(x^2 y/2, 0, 0)$, whose divergences are $1$, $x$, $x^2$ and $xy$. $\square$

The code applies Lemma 2 with the axis that fits each face. For the face with projection axes $(a, b, c)$ it adds $n_a \int x_a^2$, $n_b \int x_b^2$, $n_c \int x_c^2$ to $T_1$, and the same pattern of degree 3 to $T_2$ and $TP$. It uses $n$ in place of $\hat n$ and the projection integrals in place of face integrals. Lemma 3 shows that the two changes cancel.

**Lemma 3 (projection step).** Let $\gamma$ be the axis of line L4, so $n_\gamma \ne 0$. For a polynomial $g$, define $\tilde g(\alpha, \beta) = g$ at the point of the plane above $(\alpha, \beta)$, where $\gamma = -(n_\alpha \alpha + n_\beta \beta + w)/n_\gamma$. Let $\Pi$ be the projected polygon and $S(\cdot)$ the signed integral over it (positive when $\Pi$ is counterclockwise). Then for each axis $e$,

$$\hat n_e \int_f g \, dA = \frac{n_e}{n_\gamma} S(\tilde g).$$

*Proof.* The map $(\alpha, \beta) \mapsto$ (the point of the plane above it) is one to one from $\Pi$ onto $f$, since $n_\gamma \ne 0$, and its area factor is $1/|\hat n_\gamma|$. So $\int_f g \, dA = \frac{1}{|\hat n_\gamma|} \int_\Pi \tilde g$. By Lemma 1, $\Pi$ is counterclockwise exactly when $n_\gamma > 0$, so $\int_\Pi \tilde g = \operatorname{sign}(n_\gamma) S(\tilde g)$. Hence $\hat n_e \int_f g = \frac{\hat n_e}{\hat n_\gamma} S(\tilde g) = \frac{n_e}{n_\gamma} S(\tilde g)$, because $n$ and $\hat n$ differ by a positive factor. $\square$

Line L6 forms $\tilde g$ for $g = \gamma$, $\gamma^2$, $\gamma^3$, $\alpha^2 \beta$, $\beta^2 \gamma$ and $\gamma^2 \alpha$ (and the pure powers of $\alpha$ and $\beta$) by expanding the powers of $\gamma = -(n_\alpha \alpha + n_\beta \beta + w)/n_\gamma$ with the binomial theorem. Each $\tilde g$ is then a polynomial in $\alpha$ and $\beta$ of degree at most 3, and $S(\tilde g)$ is a linear combination of the ten integrals $P_{pq} = S(\alpha^p \beta^q)$, $p + q \le 3$. The variable names $F_a, F_{bb}, F_{cca}, \ldots$ in the code are these values divided by $n_\gamma$. The factor $n_e$ of Lemma 3 is the factor $n_a$, $n_b$ or $n_c$ in line L7.

**Lemma 4 (edge step).** For a polygon $\Pi$ with vertices $(\alpha_i, \beta_i)$ in order, and $\Delta \alpha_i = \alpha_{i+1} - \alpha_i$, $\Delta \beta_i = \beta_{i+1} - \beta_i$,

$$S(\alpha^p \beta^q) = \frac{1}{p+1} \sum_i \Delta \beta_i \, E_{p+1, q}(i) = -\frac{1}{q+1} \sum_i \Delta \alpha_i \, E_{p, q+1}(i),$$

$$E_{s, t}(i) = \frac{1}{s + t + 1} \sum_{u=0}^{s} \sum_{v=0}^{t} \frac{\binom{s}{u}\binom{t}{v}}{\binom{s+t}{u+v}} \alpha_i^{s-u} \alpha_{i+1}^{u} \beta_i^{t-v} \beta_{i+1}^{v}.$$

*Proof.* Green's theorem on the polygon gives $S(\partial Q/\partial \alpha - \partial P/\partial \beta) = \oint_{\partial \Pi} P \, d\alpha + Q \, d\beta$, with the boundary taken in vertex order. Take $Q = \alpha^{p+1}\beta^q/(p+1)$, $P = 0$ for the first form, and $P = -\alpha^p \beta^{q+1}/(q+1)$, $Q = 0$ for the second. On edge $i$ write $\alpha = (1 - \tau)\alpha_i + \tau \alpha_{i+1}$ and $\beta = (1 - \tau)\beta_i + \tau \beta_{i+1}$ for $\tau \in [0, 1]$, so $d\beta = \Delta \beta_i \, d\tau$. Expand both powers by the binomial theorem. Each term is a constant times $\tau^{u+v}(1 - \tau)^{s+t-u-v}$, and $\int_0^1 \tau^{j}(1 - \tau)^{N - j} d\tau = \frac{j! (N - j)!}{(N + 1)!} = \frac{1}{(N + 1)\binom{N}{j}}$. This gives $\int_0^1 \alpha^s \beta^t d\tau = E_{s,t}(i)$. $\square$

Line L5 evaluates these sums. $P_{00}$, $P_{10}$, $P_{20}$, $P_{30}$, $P_{11}$ and $P_{21}$ use the first form, and $P_{01}$, $P_{02}$, $P_{03}$ and $P_{12}$ the second, which is why some divisors in the code are negative. For example $E_{1,0}(i) = \frac{1}{2}(\alpha_i + \alpha_{i+1})$ gives $P_{00} = \frac{1}{2} \sum_i \Delta \beta_i (\alpha_i + \alpha_{i+1})$, and $E_{2,0}(i) = \frac{1}{3}(\alpha_i^2 + \alpha_i \alpha_{i+1} + \alpha_{i+1}^2)$ gives $P_{10} = \frac{1}{6} \sum_i \Delta \beta_i (\alpha_i^2 + \alpha_i \alpha_{i+1} + \alpha_{i+1}^2)$, which are the expressions $C_1$ and $C_\alpha$ of the code.

**Theorem.** Lines L1 to L8 return the exact $T_0$, $T_1$, $T_2$ and $TP$ of $V$, and line L9 returns its mass, its center of mass and its inertia tensor about the center of mass.

*Proof.* By Lemma 4, line L5 computes the signed projection integrals exactly. By Lemma 3 and the expansion after it, line L6 and the factors of line L7 give $\hat n_e \int_f g \, dA$ for each face and each term that Lemma 2 needs. Line L7 adds them over all faces, and line L8 applies the factors $\frac{1}{2}$, $\frac{1}{3}$ and $\frac{1}{2}$ of Lemma 2. So $T_0$, $T_1$, $T_2$ and $TP$ are the volume integrals. For line L9, the inertia tensor about a point $r$ is $J_{xx} = \rho \int_V ((y - r_y)^2 + (z - r_z)^2)$ and $J_{xy} = -\rho \int_V (x - r_x)(y - r_y)$. With $r = T_1/T_0$ and $m = \rho T_0$, expanding gives $\rho \int_V (y - r_y)^2 = \rho T_{y^2} - 2 \rho r_y T_y + m r_y^2 = \rho T_{y^2} - m r_y^2$ and $\rho \int_V (x - r_x)(y - r_y) = \rho T_{xy} - m r_x r_y$, which are the formulas of line L9. $\blacksquare$

**Termination and cost.** The loops of lines L2 and L5 run once per face and once per edge of each face, so the algorithm stops after $\Theta(n)$ arithmetic operations, where $n$ is the sum of the face sizes.
