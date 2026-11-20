---
title: With correct decisions the DD detector outputs |a|^2 sin(delta), the loop locks with variance B_L T/SNR, and for 16-QAM the decisions stay correct only for errors below 16.87 degrees
proves: [correctness]
status: full
---

The input is $r_k = a_k e^{j\theta} + w_k$, where the $a_k$ are independent and uniform on a constellation $\mathcal{A}$ with $E|a_k|^2 = 1$, and $w_k \sim \mathcal{CN}(0, N_0)$ white, $\mathrm{SNR} = 1/N_0$. Line L4 forms $z_k = r_k e^{-j\phi_k}$, line L5 picks $\hat a_k$, the point of $\mathcal{A}$ nearest to $z_k$ (or the known $a_k$ in the data-aided form), and line L6 outputs $e_k = \operatorname{Im}(z_k \overline{\hat a_k})$. Lines L7 and L8 are the loop filter and oscillator of the [phase-locked loop](/phase-locked-loop/), whose proof gives the linear closed loop, the stability conditions and $B_L T = \frac12 \sum h_k^2$. Write $\Delta = \theta - \phi$.

**Lemma 1 (the detector with a correct decision).** If $\hat a_k = a_k$, then $e_k = |a_k|^2 \sin\Delta_k + \operatorname{Im}(n_k \overline{a_k})$, with $n_k = w_k e^{-j\phi_k} \sim \mathcal{CN}(0, N_0)$ independent of the past. The noise term has mean $0$ and variance $|a_k|^2 N_0/2$.

*Proof.* $z_k \overline{a_k} = |a_k|^2 e^{j\Delta_k} + n_k \overline{a_k}$. The law of $n_k$ follows from the rotation invariance of circular Gaussian noise, as in the PLL proof. $n_k \overline{a_k}$ is circular with variance $|a_k|^2 N_0$, and its imaginary part has half of it. $\square$

**Theorem 1 (the data-aided loop).** With the known symbols in line L5, the mean detector output is $E|a|^2 \sin\Delta = \sin\Delta$, for every $\Delta$. So the only stable lock point modulo $2\pi$ is $\Delta = 0$, and in the linear model the phase error variance is $B_L T/\mathrm{SNR}$.

*Proof.* By Lemma 1 with $\hat a_k = a_k$ always, the mean of $e_k$ over the data is $\sin\Delta$, whose stable zero is $0$ (slope $1$) and unstable zero is $\pi$. Near lock the detector gain is $E|a|^2 = 1$ and the noise is white with variance $E|a|^2 N_0/2 = N_0/2$, so the PLL proof gives the variance $\frac{N_0}{2} \cdot 2B_L T = B_L T/\mathrm{SNR}$. $\square$

For QAM the gain $|a_k|^2$ changes from symbol to symbol. The linear model uses its mean, which is exact for the mean response and adds a small self noise $(|a_k|^2 - 1)\Delta_k$ that is second order near lock.

**Theorem 2 (the decision-directed loop without noise).** Let $\delta^\ast$ be the largest angle such that $a e^{j\Delta}$ lies in the decision region of $a$ for every $a \in \mathcal{A}$ and every $|\Delta| < \delta^\ast$. Then without noise the DD detector equals the data-aided detector for $|\Delta| < \delta^\ast$, and the mean S-curve is $\sin\Delta$ there. For QPSK, $\delta^\ast = 45^\circ$. For 16-QAM, $\delta^\ast = \arccos\!\bigl(\frac{2}{3\sqrt2}\bigr) - 45^\circ = 16.874^\circ$.

*Proof.* Without noise, $z_k = a_k e^{j\Delta}$, and $\hat a_k = a_k$ exactly when $z_k$ is in the decision region of $a_k$. Then Theorem 1 applies. For QPSK, the regions are the quadrants and each point is at $45^\circ$ from both boundaries. For 16-QAM with raw levels $\{\pm1, \pm3\}$, the boundaries are the lines $x = 0, \pm2$ and $y = 0, \pm2$. The inner points $\pm1 \pm j$ have modulus $\sqrt2$ and reach the boundary $x = 0$ or $y = 0$ only after $45^\circ$. A point $3 + j$ has modulus $\sqrt{10}$ and angle $\arctan\frac13 = 18.43^\circ$; it reaches the line $y = 2$ when $\sqrt{10}\sin(18.43^\circ + \Delta) = 2$, at $\Delta = 20.80^\circ$, and when rotated the other way it reaches the line $y = 0$ at $\Delta = -18.43^\circ$. The point $1 + 3j$ is its mirror image, with the angles $-20.80^\circ$ and $+18.43^\circ$. The corner point $3 + 3j$ has modulus $3\sqrt2$ at $45^\circ$; it reaches $x = 2$ when $3\sqrt2 \cos(45^\circ + \Delta) = 2$, at $\Delta = \arccos(\frac{2}{3\sqrt2}) - 45^\circ = 16.874^\circ$, and by symmetry $y = 2$ at $-16.874^\circ$. The smallest of these angles over all points, by the symmetry of the constellation, is $16.874^\circ$. $\square$

Beyond $\delta^\ast$ some decisions are wrong, and the mean S-curve departs from $\sin\Delta$. For 16-QAM, a direct evaluation over the 16 points shows that it drops at $16.874^\circ$, changes sign from positive to negative at $\arctan\frac13 = 18.435^\circ$ (where the points of the type $1 + 3j$ cross an axis into the next quadrant) and changes sign from negative to positive between $25^\circ$ and $30^\circ$. A zero where the S-curve rises is a stable lock point, so the DD loop has a *false lock* there. The tests check these values and show the loop, started at $0.7$ rad, settle with a mean error of $0.487$ rad ($27.9^\circ$).

**Theorem 3 (variance with correct decisions).** If the decisions are correct at lock, the DD loop has the variance $B_L T/\mathrm{SNR}$ of Theorem 1 in the linear model.

*Proof.* With $\hat a_k = a_k$ the recursion is that of the data-aided loop. $\square$

Wrong decisions make the detector output biased toward zero and add noise. At a symbol error rate $P_s$ the effect is of order $P_s$; the tests compare the variance at 10 dB for QPSK ($P_s \approx 1.6 \times 10^{-3}$) and 20 dB for 16-QAM ($P_s \approx 1.2 \times 10^{-5}$) with $B_L T/\mathrm{SNR}$ within a factor of 1.25.
