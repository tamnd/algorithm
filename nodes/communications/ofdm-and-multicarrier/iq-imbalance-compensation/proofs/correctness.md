---
title: "IQ imbalance couples each subcarrier with its mirror, two training symbols identify the coupling, and a 2x2 solve per pair removes it exactly without noise"
proves: [correctness]
status: full
---

Notation. $N$ subcarriers, $j$ the imaginary unit, the unitary DFT pair $Y = F y$ with $F[k, n] = e^{-j 2\pi k n / N} / \sqrt N$, and indices modulo $N$, so $-k$ means $N - k$. The ideal baseband signal in the DFT window is $y$, with $Y[k] = H[k] X[k]$ after a cyclic prefix that covers the channel. The in-phase branch is ideal; the quadrature branch has the gain $g > 0$ and the phase error $\phi$ with $|\phi| < \pi/2$. Let

$$\mu = \frac{1 + g e^{-j\phi}}{2}, \qquad \nu = \frac{1 - g e^{j\phi}}{2}.$$

The used subcarriers are $k \ne 0, N/2$; these two are their own mirrors and carry no data.

**Lemma 1 (the two-branch model).** The receiver output $r = \operatorname{Re}(y) + j g \left( \operatorname{Im}(y) \cos\phi - \operatorname{Re}(y) \sin\phi \right)$ equals $\mu y + \nu y^*$.

*Proof.* Write $y = a + jb$ with real $a$ and $b$. Then

$$\mu y + \nu y^* = \frac{(a + jb) + (a - jb)}{2} + \frac g2 \left( e^{-j\phi} (a + jb) - e^{j\phi} (a - jb) \right) = a + \frac g2 \left( -2j a \sin\phi + 2j b \cos\phi \right),$$

which is $a + j g (b \cos\phi - a \sin\phi)$. $\square$

**Lemma 2 (the mirror).** The DFT of $y^*$ at $k$ is $Y[-k]^*$. Hence

$$R[k] = A[k] X[k] + B[k] X[-k]^*, \qquad A[k] = \mu H[k], \quad B[k] = \nu H[-k]^*.$$

*Proof.* $\frac{1}{\sqrt N} \sum_n y[n]^* e^{-j 2\pi k n / N} = \left( \frac{1}{\sqrt N} \sum_n y[n] e^{-j 2\pi (-k) n / N} \right)^* = Y[-k]^*$. The DFT is linear, so by Lemma 1, $R[k] = \mu Y[k] + \nu Y[-k]^* = \mu H[k] X[k] + \nu H[-k]^* X[-k]^*$. $\square$

**Theorem 1 (training identifies A and B).** Let the training symbols satisfy $T_2[k] = T_1[k]$ for $k < N/2$ and $T_2[k] = -T_1[k]$ for $k \ge N/2$, with $T_1[k] \ne 0$ for all $k$. Without noise, lines L1 and L2 return $A[k]$ and $B[k]$ exactly for every used $k$.

*Proof.* By Lemma 2, the received training symbols give the two linear equations $R_i[k] = A[k] T_i[k] + B[k] T_i[-k]^*$ for $i = 1, 2$, which is the system of lines L1 and L2. Its determinant is $T_1[k] T_2[-k]^* - T_2[k] T_1[-k]^*$. For a used $k$, exactly one of $k$ and $-k$ is below $N/2$, so exactly one of the two training values changes sign, and the determinant is $\pm 2\, T_1[k] T_1[-k]^* \ne 0$. A nonsingular system has the unique solution $A[k]$, $B[k]$. $\square$

**Theorem 2 (the pair solve recovers the data).** For a used $k$ with $m = -k$, the values satisfy

$$\begin{pmatrix} A[k] & B[k] \\ B[m]^* & A[m]^* \end{pmatrix} \begin{pmatrix} X[k] \\ X[m]^* \end{pmatrix} = \begin{pmatrix} R[k] \\ R[m]^* \end{pmatrix},$$

and the determinant is $g \cos\phi\, H[k] H[m]^*$. So if $H[k] \ne 0$ and $H[m] \ne 0$, lines L3 and L4 return $X[k]$ exactly without noise.

*Proof.* The first row is Lemma 2 at $k$. Lemma 2 at $m$ gives $R[m] = A[m] X[m] + B[m] X[k]^*$, because $-m = k$; conjugating gives the second row. The determinant is $A[k] A[m]^* - B[k] B[m]^* = |\mu|^2 H[k] H[m]^* - |\nu|^2 H[m]^* H[k]$, using $B[m] = \nu H[k]^*$. Finally $|\mu|^2 - |\nu|^2 = \frac{(1 + 2g\cos\phi + g^2) - (1 - 2g\cos\phi + g^2)}{4} = g\cos\phi > 0$. $\square$

**Corollary (the error of a one-tap equalizer).** A receiver that ignores the imbalance and divides by $A[k]$ gets $X[k] + \frac{B[k]}{A[k]} X[-k]^*$. For unit-modulus data the image has the power $\frac{|\nu|^2 |H[-k]|^2}{|\mu|^2 |H[k]|^2}$. On a flat channel this is the inverse of the image rejection ratio $|\mu|^2 / |\nu|^2$, which is $23.79$ dB for $g = 1.1$ and $\phi = 5$ degrees. On a subcarrier whose mirror is stronger, the image is stronger by the ratio of the channel powers.

**The time-domain fix (a theorem).** Let $c = \nu / \mu^*$. Then $z = r - c\, r^* = \left( \mu - |\nu|^2 / \mu^* \right) y$, with no term in $y^*$.

*Proof.* $r^* = \mu^* y^* + \nu^* y$, so $c\, r^* = \nu y^* + \frac{|\nu|^2}{\mu^*} y$, and subtracting from $r = \mu y + \nu y^*$ removes $\nu y^*$. $\square$

From the estimates, $B[k] / A[-k]^* = \nu H[-k]^* / (\mu^* H[-k]^*) = \nu / \mu^*$ for every $k$, so the implementation estimates $c$ as the mean of these ratios.
