---
title: What charge flipping guarantees, and what it does not
proves: [correctness]
status: partial
---

Charge flipping has no convergence proof. This page proves its structure: the flip is a reflection, the amplitude step is a projection, an atomic density is a fixed point, the iteration stays real, and it treats every translate and the inverse of a start in the same way. The last fact is why the result is found only up to a shift of the origin and an inversion.

**Setting.** The unit cell is an $n_1 \times n_2$ grid, written $\Omega$, with indices taken modulo the grid. A density is a real function $\rho$ on $\Omega$, and its structure factors are the unnormalized DFT $F = \mathcal{D}\rho$, $F(h) = \sum_{x} \rho(x) e^{-2\pi i\, h \cdot x / n}$, where $h \cdot x / n$ means $h_1 x_1/n_1 + h_2 x_2/n_2$. The set $\mathcal{O}$ of observed indices does not contain $0$ (the case where it does is the same with fewer words) and is symmetric, $h \in \mathcal{O} \Rightarrow -h \in \mathcal{O}$. The data are $A(h) = |F_*(h)|$ for $h \in \mathcal{O}$, where $F_*$ belongs to the true density $\rho_*$. Since $\rho_*$ is real, $A(-h) = A(h)$.

One cycle of the algorithm maps $F$ to $F'$ by

- lines L3 to L5: $\rho = \mathcal{D}^{-1} F$, $g = \Phi_\delta(\rho)$ with $\Phi_\delta(\rho)(x) = \rho(x)$ if $\rho(x) > \delta$ and $-\rho(x)$ otherwise, and $G = \mathcal{D} g$;
- lines L6 to L9: $F' = \Pi(G)$, where $\Pi(G)(h) = A(h)\, G(h)/|G(h)|$ for $h \in \mathcal{O}$ (and $A(h)$ if $G(h) = 0$), $\Pi(G)(0) = G(0)$, and $\Pi(G)(h) = 0$ for the other $h$.

**Lemma 1 (the flip is a reflection).** Let $T_\delta(\rho)(x) = \rho(x)$ if $\rho(x) > \delta$ and $0$ otherwise. Then $\Phi_\delta = 2 T_\delta - I$. For $\delta = 0$, $T_0$ is the nearest-point projection onto the convex cone $C_+$ of nonnegative densities, so $\Phi_0 = 2 P_{C_+} - I$ is the reflection through $C_+$, and $\Phi_0(\rho) = |\rho|$.

*Proof.* If $\rho(x) > \delta$, then $2T_\delta(\rho)(x) - \rho(x) = \rho(x)$; otherwise it is $-\rho(x)$. For $\delta = 0$, the nearest nonnegative number to a real $v$ is $\max(v, 0)$, and the squared distance is a sum over the points, so the projection acts point by point. $2\max(v, 0) - v = |v|$. $\square$

For $\delta > 0$, $T_\delta$ is hard thresholding. It is not the projection onto a convex set, and the reflection picture holds only in this loose sense. The flip keeps the large values and changes the sign of the small ones, which pushes weight from the region of low density into the atoms.

**Lemma 2 (the amplitude step is a projection).** Let $M$ be the set of $F$ with $|F(h)| = A(h)$ for $h \in \mathcal{O}$ and $F(h) = 0$ for $h \notin \mathcal{O} \cup \{0\}$, with $F(0)$ free. Then $\Pi(G)$ is a nearest point of $M$ to $G$. By the [Parseval theorem](/parseval-theorem/), $\mathcal{D}^{-1}\Pi\mathcal{D}$ is a nearest-point map onto the densities whose transforms lie in $M$.

*Proof.* The squared distance $\sum_h |G(h) - F(h)|^2$ splits over $h$. At $h \in \mathcal{O}$ the nearest complex number of modulus $A(h)$ is $A(h) G(h)/|G(h)|$, by the triangle inequality, and any such number if $G(h) = 0$. At $h = 0$ the value is free, so $F(0) = G(0)$. At the other $h$ the value must be $0$. The unnormalized DFT scales all distances by the same factor $\sqrt{n_1 n_2}$. $\square$

So one cycle is $\rho \mapsto \mathcal{D}^{-1} \Pi \mathcal{D}\, \Phi_\delta(\rho)$: a projection onto the data after a reflection through the constraint in real space. Error reduction would use $T_\delta$ in place of $\Phi_\delta$. This places charge flipping in the family of reflection methods with [hybrid input-output](/hybrid-input-output/) and the [difference map](/difference-map/).

**Lemma 3 (the density stays real).** If $F(-h) = \overline{F(h)}$ for all $h$ at the start, this holds after every cycle, so every $\rho$ is real.

*Proof.* If $F$ has this symmetry, $\rho$ is real, so $g$ is real and $G(-h) = \overline{G(h)}$. Then $\Pi(G)(-h) = A(-h) G(-h)/|G(-h)| = \overline{A(h) G(h)/|G(h)|}$ for $h \in \mathcal{O}$, since $A(-h) = A(h)$ and $\mathcal{O}$ is symmetric; also $G(0)$ is real, and the zero entries stay zero. $\square$

**Theorem 1 (an atomic density is a fixed point).** Suppose that every value of $\rho_*$ is either $0$ or larger than $\delta$, and that $F_*(h) = 0$ for every $h \notin \mathcal{O} \cup \{0\}$ (for instance, every $h \ne 0$ is observed). Start the iteration at $F = F_*$, the value at $0$ included. Then every cycle returns $F_*$, and $R = 0$.

*Proof.* $\rho = \rho_*$. At points with $\rho_* > \delta$ the flip keeps the value, and at points with $\rho_* = 0$ it gives $-0 = 0$; so $g = \rho_*$ and $G = F_*$. For $h \in \mathcal{O}$, $A(h) G(h)/|G(h)| = F_*(h)$ when $F_*(h) \ne 0$; when $F_*(h) = 0$, $A(h) = 0$ and the step gives $0$. The entry at $0$ is $G(0) = F_*(0)$, and the other entries are $0 = F_*(h)$ by the hypothesis. So $F' = F_*$. The R-value compares $|G| = |F_*|$ with $A$, which agree. $\square$

The theorem does not say that the iteration reaches $F_*$, and a density that is close to atomic but has small nonzero values below $\delta$ is not a fixed point: those values change sign every cycle. In practice the iteration then wanders near the solution, which is why the R-value stays above zero after convergence.

**Theorem 2 (translation and inversion).** Let $F$ obey Friedel symmetry and let $(F_k)$ be the sequence of the iteration from $F_0 = F$, with the densities $\rho_k = \mathcal{D}^{-1} F_k$.

1. For a grid vector $t$, the iteration from $F_0(h) e^{-2\pi i\, h \cdot t/n}$ gives the densities $\rho_k(x - t)$.
2. The iteration from $\overline{F_0}$ gives the densities $\rho_k(-x)$.

*Proof.* (1) Let $S_t \rho(x) = \rho(x - t)$. Then $\mathcal{D} S_t \rho(h) = e^{-2\pi i\, h \cdot t/n} \mathcal{D}\rho(h)$. The flip acts point by point, so $\Phi_\delta S_t = S_t \Phi_\delta$. The step $\Pi$ commutes with multiplication by $e^{-2\pi i\, h \cdot t/n}$, because that factor has modulus $1$, does not change which entries are zero, and is $1$ at $h = 0$. So one cycle maps $S_t \rho_k$ to $S_t \rho_{k+1}$, and induction gives the claim. (2) Let $J\rho(x) = \rho(-x)$. For real $\rho$, $\mathcal{D} J \rho = \overline{\mathcal{D} \rho}$. The flip commutes with $J$, and $\Pi(\overline{G}) = \overline{\Pi(G)}$ because $A$ is real and conjugation keeps moduli. The same induction applies. $\square$

The data are the same for $\rho_*$, its translates and its inverse. By Theorem 2 the algorithm has no way to prefer one of them, so the origin and the hand of the result are arbitrary. In the space group $P1$ every origin is allowed, so this is no loss. For other symmetries, charge flipping works in $P1$ and the symmetry elements and the origin are found from the result afterward.

**What is not proved.** There is no theorem that charge flipping converges, or that a fixed point with a low R-value is the true structure. Theorem 1 is about the truth, not about other fixed points; the tests on the page include a one-dimensional case in which the iteration reaches a dense density with a very low R-value that is not the structure. Success in three-dimensional crystallography is a measurement: Oszlanyi and Suto report that the method solves many structures at atomic resolution, and the Superflip manual treats the R-value as an indicator of convergence, not a proof of a solution.
