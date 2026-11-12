---
title: The FastICA step is an approximate Newton step and converges cubically for kurtosis
proves: [correctness]
status: full
---

We use the pseudocode and notation of the page. The data follow $x = A s$ with $A$ invertible and independent sources $s_i$ with mean 0, variance 1 and fourth cumulant $\kappa_i = E[s_i^4] - 3$. After line L1, $z = Q s$ with $Q$ orthogonal (the whitening lemma on the [ICA page](/independent-component-analysis/)). For a unit vector $w$ put $q = Q^{\top} w$, the same vector in source coordinates; $q$ is also a unit vector and $w^{\top} z = q^{\top} s$. The analysis is for the population, where sample means are replaced by expectations.

**Where the step comes from.** One unit maximizes or minimizes $E[G(w^{\top} z)]$ on the sphere $\lVert w \rVert = 1$, with $g = G'$. The Lagrange condition is $F(w) = E[z\, g(w^{\top} z)] - \beta w = 0$ with $\beta = E[w^{\top} z\, g(w^{\top} z)]$. The Jacobian of $F$ is $E[z z^{\top} g'(w^{\top} z)] - \beta I$. Since the data are white, the approximation $E[z z^{\top} g'(w^{\top} z)] \approx E[z z^{\top}] E[g'(w^{\top} z)] = E[g'(w^{\top} z)] I$ makes the Jacobian diagonal, and the Newton step becomes
$$ w^{+} = w - \frac{E[z\, g(w^{\top} z)] - \beta w}{E[g'(w^{\top} z)] - \beta} . $$
Multiply by $\beta - E[g'(w^{\top} z)]$, which does not change the direction, to get line L5: $w^{+} = E[z\, g(w^{\top} z)] - E[g'(w^{\top} z)]\, w$. Line L7 then projects back to the sphere. At a separating solution $w^{\top} z = \pm s_m$ the approximation is exact on the directions orthogonal to $w$, because there $w^{\top} z$ is independent of the other whitened coordinates. Only those directions matter on the sphere, since line L7 removes the radial part.

**Lemma 1 (the kurtosis step in source coordinates).** For $g(u) = u^3$, the vector computed in line L5 is $Q r$ with $r_i = \kappa_i q_i^3$.

*Proof.* $E[z\, g(w^{\top} z)] = Q E[s (q^{\top} s)^3]$. Expand $(q^{\top} s)^3$ and use independence, mean 0 and variance 1. In $E[s_i (\sum_j q_j s_j)^3]$, the only terms with nonzero expectation are $q_i^3 E[s_i^4]$ and, for each $j \ne i$, the three terms $q_i q_j^2 E[s_i^2] E[s_j^2]$. So
$$ E[s_i (q^{\top} s)^3] = q_i^3 (\kappa_i + 3) + 3 q_i (1 - q_i^2) = \kappa_i q_i^3 + 3 q_i . $$
Also $E[g'(w^{\top} z)] = 3 E[(q^{\top} s)^2] = 3 \lVert q \rVert^2 = 3$. Subtract $3 w = Q (3 q)$. $\square$

So one step of lines L5 and L7 maps $q$ to $\kappa \circ q^3 / \lVert \kappa \circ q^3 \rVert$, where $\circ$ and the cube act on each coordinate.

**Theorem 1 (cubic convergence).** Assume every $\kappa_i \ne 0$, put $u_i = |\kappa_i|^{1/2} |q_i|$, and assume one index $m$ has $u_m > u_i$ for all $i \ne m$ at the start. Let $q^{(t)}$ be the iterate after $t$ steps and $\rho_i = u_i / u_m$ at the start. Then:

1. $u_i^{(t)} / u_m^{(t)} = \rho_i^{\,3^t}$ for every $i$ and $t$.
2. $q^{(t)}$ converges to $\pm e_m$, so $w$ converges to $\pm$ the column of $Q$ that extracts $s_m$, and $w^{\top} z \to \pm s_m$.
3. The error $\varepsilon_t = \bigl(1 - (q_m^{(t)})^2\bigr)^{1/2}$ satisfies $\varepsilon_{t+1} \le C \varepsilon_t^3 / |q_m^{(t)}|^3$ with $C = \max_{i \ne m} |\kappa_i| / |\kappa_m|$. So the convergence is cubic.

*Proof.* (1) Before normalization the step gives $|\kappa_i| |q_i|^3$, so $u_i$ becomes $|\kappa_i|^{1/2} |\kappa_i| |q_i|^3 = u_i^3$, and normalization multiplies every $u_i$ by the same factor. So each ratio $u_i / u_m$ is cubed at each step.

(2) By (1), $q_i^{(t)} / q_m^{(t)} \to 0$ for $i \ne m$, because $\rho_i < 1$. Since $\lVert q^{(t)} \rVert = 1$, $|q_m^{(t)}| \to 1$.

(3) Write $q'$ for the next iterate. Then
$$ \varepsilon_{t+1}^2 = \frac{\sum_{i \ne m} \kappa_i^2 q_i^6}{\sum_i \kappa_i^2 q_i^6} \le \frac{\sum_{i \ne m} \kappa_i^2 q_i^6}{\kappa_m^2 q_m^6} \le C^2 \frac{\bigl(\sum_{i \ne m} q_i^2\bigr)^3}{q_m^6} = C^2 \frac{\varepsilon_t^6}{q_m^6} , $$
using $\sum_i a_i^3 \le (\sum_i a_i)^3$ for $a_i = q_i^2 \ge 0$. Take square roots. As $|q_m^{(t)}| \to 1$, this gives $\varepsilon_{t+1} \le C' \varepsilon_t^3$ for any $C' > C$ once $t$ is large. $\square$

If $\kappa_m < 0$, the sign of the $m$-th coordinate flips at every step, because $\kappa_m q_m^3$ has the opposite sign to $q_m$. This is why line L7 tests $|w^{+\top} w|$ against 1, not $w^{+\top} w$.

The vectors $\pm e_i$ are the only stable fixed points. Any other fixed point has two or more coordinates with equal $u_i$, and by (1) a small change that breaks the tie grows. The set of starting points with a tie has measure zero, so a random start in line L3 converges with probability 1. The source that is found depends on the start through $u_i$, not through $|q_i|$ alone.

**Theorem 2 (deflation finds each source once).** Suppose units $1, \ldots, p - 1$ have converged to $w_j = \pm Q e_{m_j}$ for distinct $m_j$. In unit $p$, line L6 keeps $q_{m_j} = 0$ for all $j < p$, so unit $p$ converges to a source not found before.

*Proof.* Line L6 subtracts the projections of $w^{+}$ on the $w_j$, which in source coordinates sets $q_{m_j} = 0$. By Lemma 1 the step maps a zero coordinate to $\kappa_{m_j} \cdot 0^3 = 0$, so the projection is not even needed in the population; on a sample it removes the small errors. Theorem 1, applied to the remaining coordinates, gives convergence to some $\pm e_m$ with $m \notin \{m_1, \ldots, m_{p-1}\}$. $\square$

**Lemma 2 (symmetric decorrelation).** For a $k \times d$ matrix $W$ of rank $k$, the rows of $W' = (W W^{\top})^{-1/2} W$ are orthonormal, and the map treats the rows alike: for a permutation matrix $\Pi$, $(\Pi W)' = \Pi W'$.

*Proof.* $W' W'^{\top} = (W W^{\top})^{-1/2} W W^{\top} (W W^{\top})^{-1/2} = I$. For the second claim, $(\Pi W W^{\top} \Pi^{\top})^{-1/2} = \Pi (W W^{\top})^{-1/2} \Pi^{\top}$, since conjugation by an orthogonal matrix commutes with the matrix square root. $\square$

So in the symmetric version, errors in one unit do not pass to the units found after it, as they do in deflation. In the population with $g(u) = u^3$, each row follows Lemma 1, and the separated matrix $W = \Pi D Q^{\top}$ (with $D$ a diagonal of signs) is a fixed point of the combined step.

**Cost.** One evaluation of line L5 takes $\Theta(n d)$ operations: one inner product and one update of the sum per observation. Line L6 takes $\Theta(p d)$. With $I_p$ iterations for unit $p$, deflation costs $\Theta(n d^2 + d^3)$ for line L1 plus $\Theta(n d \sum_p I_p)$. One symmetric iteration costs $\Theta(n d k + k^2 d + k^3)$. The extra memory is $\Theta(n d + d^2)$.
