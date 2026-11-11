---
title: GPV signatures from a gadget trapdoor verify
proves: [correctness]
status: full
---

Let $q = 2^k$, $w = n k$, $m = \bar m + w$, and let $g = (1, 2, \dots, 2^{k-1})$ and $G = I_n \otimes g \in \mathbb{Z}^{n \times w}$. All congruences are modulo $q$.

**Lemma 1 (the gadget lattice).** Let $S_k \in \mathbb{Z}^{k \times k}$ have columns $2 e_j - e_{j+1}$ for $j < k - 1$ and $2 e_{k-1}$, and let $S_G = I_n \otimes S_k$. Then every column of $S_G$ is in $\Lambda^\perp(G)$ and $|\det S_G| = q^n$, so $S_G$ is a basis of $\Lambda^\perp(G)$.

*Proof.* $g (2 e_j - e_{j+1}) = 2 \cdot 2^j - 2^{j+1} = 0$ and $g (2 e_{k-1}) = 2^k = q \equiv 0$. $S_k$ is lower triangular with diagonal entries 2, so $\det S_k = 2^k = q$ and $\det S_G = q^n$. The lattice $\Lambda^\perp(G)$ has index $|\mathbb{Z}_q^n| = q^n$ in $\mathbb{Z}^w$, because $G$ maps $\mathbb{Z}^w$ onto $\mathbb{Z}_q^n$ (the unit vectors $e_{ik}$ map to the unit vectors of $\mathbb{Z}_q^n$). A sublattice of $\Lambda^\perp(G)$ with the same determinant is equal to it. $\square$

**Lemma 2 (the trapdoor basis).** With $A = [\bar A \mid G - \bar A R]$ from line L2, $W$ the matrix of bits of $-\bar A \bmod q$ (so $G W \equiv -\bar A$), and
$$S = \begin{pmatrix} R S_G & I + R W \\ S_G & W \end{pmatrix},$$
every column of $S$ is in $\Lambda^\perp(A)$, and $S$ is a basis of $\Lambda^\perp(A)$.

*Proof.* $A \binom{R S_G}{S_G} = \bar A R S_G + (G - \bar A R) S_G = G S_G \equiv 0$ by Lemma 1, and $A \binom{I + R W}{W} = \bar A + \bar A R W + G W - \bar A R W = \bar A + G W \equiv 0$. Also $S = \begin{pmatrix} I & R \\ 0 & I \end{pmatrix} \begin{pmatrix} 0 & I \\ S_G & W \end{pmatrix}$; the first factor has determinant 1 and the second has determinant $\pm \det S_G = \pm q^n$. Both lattices have the same determinant: $A$ maps $\mathbb{Z}^m$ onto $\mathbb{Z}_q^n$, because the columns of $G$ inside $A T = [\bar A \mid G]$, with the unimodular $T = \begin{pmatrix} I & R \\ 0 & I \end{pmatrix}$, include the unit vectors of $\mathbb{Z}_q^n$. So $\Lambda^\perp(A)$ has index $q^n$ in $\mathbb{Z}^m$, and $|\det S| = q^n$. A full-rank sublattice of $\Lambda^\perp(A)$ with the same determinant is equal to it, so $S$ is a basis. $\square$

**Lemma 3 (the preimage).** For $u \in \mathbb{Z}_q^n$, let $b = G^{-1}(u) \in \{0, 1\}^w$ be the bits of the entries of $u$. Then $G b \equiv u$, and $t = \binom{R b}{b}$ from line L7 satisfies $A t \equiv u$.

*Proof.* Each block of $b$ is the binary expansion of $u_i \in [0, q)$, and $g$ times it is $u_i$. Then $A t = \bar A R b + (G - \bar A R) b = G b \equiv u$. $\square$

**Lemma 4 (the sampler stays in the lattice).** For any basis $B = (b_1, \dots, b_m)$, any center and any parameter, Klein's sampler of line L8 returns an integer combination $\sum_i z_i b_i$.

*Proof.* Each step adds $z_i b_i$ to $v$ with an integer $z_i$ from the one-dimensional sampler, and $v$ starts at $0$. $\square$

**Theorem 1 (verification equation).** For every message and every run of lines L5 to L9, $A x \equiv H(\mathrm{salt} \| \mathrm{msg})$, so the check of line L11 passes.

*Proof.* By Lemma 4 and Lemma 2, $v$ is an integer combination of vectors of $\Lambda^\perp(A)$, so $A v \equiv 0$. By Lemma 3, $A t \equiv u = H(\mathrm{salt} \| \mathrm{msg})$. So $A x = A t + A v \equiv u$. Line L11 recomputes the same $u$ from the same salt and message. $\blacksquare$

**Theorem 2 (the length check).** Assume that the sampler of line L8 outputs $x$ with the distribution $D_{\Lambda_u^\perp(A), s}$, and that $s \ge \eta_\varepsilon(\Lambda^\perp(A))$ for some $\varepsilon \in (0, 1)$. Then line L10 rejects with probability at most $\frac{1 + \varepsilon}{1 - \varepsilon} 2^{-m}$.

*Proof.* $x$ is a sample of $D_{\Lambda + c, s}$ with $\Lambda = \Lambda^\perp(A)$ and $c = t$. The tail bound of Banaszczyk, in the form of Micciancio and Regev (2007, Lemma 4.4), states that for $s \ge \eta_\varepsilon(\Lambda)$ and any coset, $\Pr[\|x\| > s \sqrt m] \le \frac{1 + \varepsilon}{1 - \varepsilon} 2^{-m}$. $\square$

**Remarks.** The assumption of Theorem 2 is the main theorem of GPV about Klein's sampler: if $s \ge \|\tilde S\| \cdot \omega(\sqrt{\log m})$, the output is within negligible statistical distance of $D_{\Lambda_u^\perp(A), s}$; with such $s$, $s \ge \eta_\varepsilon$ also holds because $\eta_\varepsilon(\Lambda) \le \|\tilde S\| \cdot \sqrt{\ln(2m(1 + 1/\varepsilon))/\pi}$ for any basis $S$. So a signature fails verification only with negligible probability, and only through line L10. The code on this page cuts the one-dimensional Gaussian at six standard deviations, which changes the distribution by a negligible amount and makes the length of $x$ bounded.
