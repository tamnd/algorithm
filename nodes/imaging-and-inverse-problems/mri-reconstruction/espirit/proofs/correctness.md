---
title: ESPIRiT returns the normalized coil maps when the coil maps have a finite k-space support and the calibration data are rich enough
proves: [correctness]
status: full
---

The setting is that of the algorithm, in exact arithmetic. There are $c$ coils on an $n \times n$ grid. The coil image is $f_b(p) = s_b(p) \rho(p)$, and its k-space is the unitary DFT

$$x_b(\kappa) = \frac{1}{n} \sum_{p} f_b(p)\, e^{-2\pi i \kappa \cdot p / n}.$$

The patch offsets are $O = \{0, \ldots, k_r - 1\} \times \{0, \ldots, k_c - 1\}$, with $K = k_r k_c$. A vector $v \in \mathbb{C}^{cK}$ has the entries $v(b, d)$ for a coil $b$ and an offset $d \in O$. The row of the calibration matrix $A$ for a patch at $\kappa$ in the ACS block is $(x_b(\kappa + d))_{(b,d)}$. For a vector $v$ and a pixel $p$, define $a_v(p) \in \mathbb{C}^c$ by

$$a_v(p)[b] = \sum_{d \in O} \overline{v(b, d)}\, e^{2\pi i d \cdot p / n},$$

as in line L4. Let $V_\parallel$ be the right singular vectors that line L1 keeps and $V_\perp$ the other right singular vectors, so that $[V_\parallel\ V_\perp]$ is unitary. Line L5 builds $G(p) = \frac{1}{K} \sum_{v \in V_\parallel} a_v(p) a_v(p)^H$.

**Lemma 1 (null vectors in the image domain).** If $\sum_{b, d} x_b(\kappa + d)\, v(b, d) = 0$ for every $\kappa \in \mathbb{Z}_n^2$, then $a_v(p)^H f(p) = 0$ for every pixel $p$, where $f(p) = (f_b(p))_b$.

*Proof.* Insert the DFT:

$$\sum_{b,d} v(b,d)\, x_b(\kappa + d) = \frac{1}{n} \sum_p e^{-2\pi i \kappa \cdot p/n} \sum_b f_b(p) \sum_d v(b,d)\, e^{-2\pi i d \cdot p/n} = \frac{1}{n} \sum_p e^{-2\pi i \kappa \cdot p/n}\, a_v(p)^H f(p).$$

This is the DFT of the function $p \mapsto a_v(p)^H f(p)$. It is 0 for every $\kappa$, and the DFT is invertible, so the function is 0. $\square$

**Lemma 2 (the operator is a part of the identity).** For every $p$, $G(p)$ is Hermitian, $0 \preceq G(p) \preceq I$, and

$$G(p) + \frac{1}{K} \sum_{v \in V_\perp} a_v(p) a_v(p)^H = I.$$

*Proof.* Let $\Phi(p)$ be the $c \times cK$ matrix with $\Phi(p)[a, (b, d)] = \delta_{ab}\, e^{2\pi i d \cdot p/n}$. Then $a_v(p) = \Phi(p) \bar v$, and $\Phi(p) \Phi(p)^H = K I$, because each row has $K$ entries of modulus 1 and different rows have disjoint supports. The conjugate of a unitary matrix is unitary, so $\sum_{\text{all } v} \bar v\, \bar v^H = I$, and

$$\sum_{\text{all } v} a_v(p) a_v(p)^H = \Phi(p) \Big( \sum_{\text{all } v} \bar v\, \bar v^H \Big) \Phi(p)^H = K I.$$

Divide by $K$. Both sums are Hermitian and positive semidefinite, so $0 \preceq G(p) \preceq I$. $\square$

**Model (H1).** As in the [GRAPPA proof](/grappa/), the maps are trigonometric polynomials with image frequencies in a finite set $H$: $s_b(p) = \sum_{e \in H} h_b(e)\, e^{2\pi i e \cdot p/n}$. Then $x_b(\kappa) = \sum_{e \in H} h_b(e)\, X(\kappa - e)$, with $X$ the k-space of $\rho$. Let $U = \{d - e : d \in O,\ e \in H\}$, and let $M$ be the $|U| \times cK$ matrix $M[u, (b, d)] = h_b(d - u)$, with $h_b = 0$ outside $H$. Then

$$\sum_{b,d} x_b(\kappa + d)\, v(b,d) = \sum_{u \in U} X(\kappa + u)\, (M v)_u \quad \text{for every } \kappa. \qquad (1)$$

**Theorem.** Assume (H1), and:
1. (rich calibration) the matrix $P$ whose rows are $(X(\kappa + u))_{u \in U}$, for the patch positions $\kappa$ of the ACS block, has full column rank $|U|$;
2. (threshold) line L1 keeps exactly the right singular vectors with a nonzero singular value.

Then for every pixel $p$, $G(p)\, s(p) = s(p)$, and 1 is the largest eigenvalue of $G(p)$. If moreover
3. (simple eigenvalue) the eigenvalue 1 of $G(p)$ is simple and $s_0(p) \ne 0$,

then the map that lines L6 and L7 return at $p$ is $s(p)/\lVert s(p) \rVert$ times the phase $\overline{s_0(p)}/|s_0(p)|$, for any $t_e \le 1$.

*Proof.* By (1), $A = P M$. Since $P$ has full column rank, $A v = 0$ if and only if $M v = 0$. By assumption 2, the discarded vectors $V_\perp$ span the null space of $A$, so $M v = 0$ for each $v \in V_\perp$, and by (1) the hypothesis of Lemma 1 holds for each of them. The same computation as in Lemma 1, with $s_b$ in place of $f_b$, gives more: by (H1),

$$a_v(p)^H s(p) = \sum_{b,d} v(b,d)\, e^{-2\pi i d \cdot p/n} \sum_{e} h_b(e)\, e^{2\pi i e \cdot p/n} = \sum_{u \in U} e^{-2\pi i u \cdot p/n}\, (M v)_u = 0$$

at every pixel $p$, also where $\rho(p) = 0$. By Lemma 2, $G(p) s(p) = s(p) - \frac{1}{K} \sum_{v \in V_\perp} a_v(p)\, a_v(p)^H s(p) = s(p)$. Since $G(p) \preceq I$, no eigenvalue is larger than 1. If $s(p) \ne 0$ and the eigenvalue 1 is simple, the top eigenvector of line L6 is $u = e^{i\theta} s(p)/\lVert s(p) \rVert$ for some phase $\theta$. Its eigenvalue is $1 \ge t_e$, so line L7 keeps it and divides by $u_0/|u_0| = e^{i\theta} s_0(p)/|s_0(p)|$, which removes $\theta$. $\square$

**Corollary (the maps explain the data).** Under the assumptions 1 to 3 at every pixel, the maps $m(p)$ of the algorithm satisfy $f_b(p) = m_b(p)\, \rho'(p)$ for the image $\rho'(p) = \lVert s(p) \rVert\, \tfrac{s_0(p)}{|s_0(p)|}\, \rho(p)$. So a [SENSE](/sense/) reconstruction with these maps that is exact for the true maps returns $\rho'$, and the coil images $m_b \rho'$ are the true coil images.

*Proof.* Multiply the result of the theorem by $\rho'(p)$. $\square$

**Remarks.**
- Assumption 1 is the rich calibration assumption of the GRAPPA proof. Under it, the rank of $A$ is the rank of $M$, at most $|U|$. For the band maps of the tests ($H = \{0,1\}^2$, a $3 \times 3$ kernel, $|U| = 16$), the tests find 16 large singular values and a gap of more than $10^4$ to the rest (measurement).
- Assumption 3 can fail. If the object is larger than the field of view, or if the coils give fewer independent profiles than needed, the eigenvalue 1 can have a multiplicity above 1, and ESPIRiT then uses several sets of maps (Uecker et al. 2014). The tests check the result for the band maps, not the assumption.
- For maps that are not trigonometric polynomials, (H1) holds only approximately. Then the discarded vectors are only approximately null, $G(p)$ has eigenvalues close to 1 where the object has signal, and the thresholds $t_s$ and $t_e$ are choices. The behavior for the ring maps of the tests is a measurement.
- The theorem says nothing about the eigenvalues outside the object for real data: there the data do not constrain the maps, and line L7 uses $t_e$ to mask such pixels. For (H1) maps, the eigenvalue is 1 everywhere.
