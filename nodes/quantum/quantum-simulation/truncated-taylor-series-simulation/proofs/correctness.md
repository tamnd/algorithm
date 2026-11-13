---
title: Each segment of the truncated Taylor series simulation is within delta + 1.5 delta^2 + 0.5 delta^3 of e^(-iH tau), and r segments are within (1 + e)^r - 1 of e^(-iHt)
proves: [correctness]
status: full
---

We use the pseudocode of the page. $H = \sum_{l=1}^L c_lP_l$ with real $c_l$ and Pauli strings $P_l$, $\sigma_l = \mathrm{sign}(c_l)$, $\lambda = \sum_l |c_l|$ (line L1), and $\tau = t/r$ with $r = \lceil\lambda t/\ln 2\rceil$ (line L2). The norm $\|\cdot\|$ is the spectral norm. Write $U = e^{-iH\tau}$ and $\Pi = |0\rangle\langle 0| \otimes I$, where $|0\rangle$ is the zero index.

**Lemma 1 (the weighted sum).** The pairs of line L3 satisfy $\beta_j > 0$ except for the padding, each $V_j$ is unitary, and
$$\tilde V := \sum_j \beta_jV_j = \sum_{k=0}^K\frac{(-i\tau H)^k}{k!}, \qquad \sum_j \beta_j = 2.$$

*Proof.* Each $\sigma_lP_l$ is a Pauli string times $\pm 1$, so it is unitary, and so is $V_j = (-i)^k\sigma_{l_1}P_{l_1}\cdots\sigma_{l_k}P_{l_k}$. Since $c_lP_l = |c_l|\sigma_lP_l$,
$$H^k = \Big(\sum_l |c_l|\sigma_lP_l\Big)^k = \sum_{l_1, \ldots, l_k}|c_{l_1}|\cdots|c_{l_k}|\,\sigma_{l_1}P_{l_1}\cdots\sigma_{l_k}P_{l_k},$$
and multiplying by $(-i\tau)^k/k!$ gives the terms of order $k$ of line L3. The padding adds $cI + c(-I) = 0$ to the sum. The weights of order $k$ add up to $(\tau^k/k!)\lambda^k$, so before the padding they add up to $s_K = \sum_{k \le K}(\lambda\tau)^k/k! \le e^{\lambda\tau} \le e^{\ln 2} = 2$, because $\lambda\tau = \lambda t/r \le \ln 2$. So $c = (2 - s_K)/2 \ge 0$, and after the padding the weights add up to 2. $\square$

**Lemma 2 (truncation).** $\|\tilde V - U\| \le \delta := \sum_{k > K}(\lambda\tau)^k/k!$.

*Proof.* $U - \tilde V = \sum_{k > K}(-i\tau H)^k/k!$, the series converges absolutely, and $\|H\| \le \sum_l |c_l|\,\|P_l\| = \lambda$. $\square$

**Lemma 3 (the segment).** With $W = (B^\dagger \otimes I)\,\mathrm{SELECT}\,(B \otimes I)$ and $A = -WRW^\dagger RW$, $R = 2\Pi - I$,
$$\Pi A\Pi = |0\rangle\langle 0| \otimes A_0, \qquad A_0 = \tfrac{3}{2}\tilde V - \tfrac{1}{2}\tilde V\tilde V^\dagger\tilde V.$$

*Proof.* First, $\Pi W\Pi = |0\rangle\langle 0| \otimes \tilde V/2$: with $B|0\rangle = \sum_j b_j|j\rangle$ and $b_j = \sqrt{\beta_j/2}$, $(\langle 0| \otimes I)W(|0\rangle \otimes I) = \sum_j b_j^2V_j = \tilde V/2$, since SELECT does not change the index and $B$ is real, so $\langle 0|B^\dagger|j\rangle = b_j$. Let $Z = \Pi W\Pi$. Then $(2\Pi - I)W = 2\Pi W - W$, $W^\dagger(2\Pi W - W) = 2W^\dagger\Pi W - I$, and
$$(2\Pi - I)(2W^\dagger\Pi W - I) = 4\Pi W^\dagger\Pi W - 2W^\dagger\Pi W - 2\Pi + I.$$
Multiplying by $W$ on the left and using $WW^\dagger = I$,
$$WRW^\dagger RW = 4W\Pi W^\dagger\Pi W - 2\Pi W - 2W\Pi + W.$$
Multiply by $\Pi$ on both sides and use $\Pi^2 = \Pi$: $\Pi A\Pi = -4Z Z^\dagger Z + 2Z + 2Z - Z = 3Z - 4ZZ^\dagger Z$, where $\Pi W^\dagger\Pi = Z^\dagger$. With $Z = |0\rangle\langle 0| \otimes \tilde V/2$ this is $|0\rangle\langle 0| \otimes (\tfrac{3}{2}\tilde V - \tfrac{4}{8}\tilde V\tilde V^\dagger\tilde V)$. $\square$

So line L6 followed by the outcome 0 in line L7 maps $|\psi\rangle$ to $A_0|\psi\rangle$, with probability $\|A_0\psi\|^2/\|\psi\|^2$, after normalization.

**Lemma 4 (one segment).** $\|A_0 - U\| \le e := \delta + \tfrac{3}{2}\delta^2 + \tfrac{1}{2}\delta^3$, and $\|A_0\| \le 1 + e$.

*Proof.* Write $\tilde V = U + E$ with $\|E\| \le \delta$ (Lemma 2). Expand, using $UU^\dagger U = U$:
$$\tilde V\tilde V^\dagger\tilde V = U + (2E + UE^\dagger U) + (EE^\dagger U + EU^\dagger E + UE^\dagger E) + EE^\dagger E.$$
Then
$$A_0 - U = \tfrac{3}{2}E - E - \tfrac{1}{2}UE^\dagger U - \tfrac{1}{2}(EE^\dagger U + EU^\dagger E + UE^\dagger E) - \tfrac{1}{2}EE^\dagger E.$$
Since $\|U\| = 1$, the norms of the terms are at most $\tfrac{1}{2}\delta$, $\tfrac{1}{2}\delta$, $\tfrac{3}{2}\delta^2$ and $\tfrac{1}{2}\delta^3$. The triangle inequality gives the first claim, and $\|A_0\| \le \|U\| + e$ the second. $\square$

**Lemma 5 (all segments).** $\|A_0^r - e^{-iHt}\| \le (1 + e)^r - 1$.

*Proof.* $e^{-iHt} = U^r$, and
$$A_0^r - U^r = \sum_{m=0}^{r-1}A_0^{r-1-m}(A_0 - U)U^m.$$
By Lemma 4 the norm of the term $m$ is at most $(1 + e)^{r-1-m}e$, and $\sum_{m=0}^{r-1}(1 + e)^{r-1-m}e = (1 + e)^r - 1$. $\square$

**Theorem.** TAYLOR-SIM returns the system state after outcome 0 in all $r$ segments. This happens with probability $\|A_0^r\psi\|^2$ for a unit $|\psi\rangle$, the unnormalized output $A_0^r|\psi\rangle$ is within $\eta = (1 + e)^r - 1$ of $e^{-iHt}|\psi\rangle$, and the normalized output is within $2\eta$ of it.

*Proof.* By Lemma 3, each segment with outcome 0 applies $A_0$ and then normalizes, and the probability of outcome 0 in segment $m$ is $\|A_0^m\psi\|^2/\|A_0^{m-1}\psi\|^2$. The product of these ratios is $\|A_0^r\psi\|^2$, and the state after the last segment is $v/\|v\|$ with $v = A_0^r|\psi\rangle$. Lemma 5 gives $\|v - u\| \le \eta$ with the unit vector $u = e^{-iHt}|\psi\rangle$. Then $\big|\|v\| - 1\big| \le \eta$, so
$$\Big\|\frac{v}{\|v\|} - u\Big\| \le \Big\|\frac{v}{\|v\|} - v\Big\| + \|v - u\| = \big|1 - \|v\|\big| + \|v - u\| \le 2\eta.$$
The success probability is $\|v\|^2 \ge (1 - \eta)^2$ when $\eta < 1$. $\blacksquare$

**The choice of $K$.** For $x = \lambda\tau \le \ln 2 < 1$ and $k > K$, $x^k/k! \le x^{K+1}/(K+1)! \cdot x^{k-K-1}/(k-K-1)!$, so $\delta \le e^xx^{K+1}/(K+1)! \le 2(\ln 2)^{K+1}/(K+1)!$. If $\delta \le \epsilon/(4r)$ and $\epsilon \le 1$, then $e \le 2\delta$ and $\eta \le e^{re} - 1 \le 2re \le \epsilon$, since $re \le 1/2$. By Stirling's formula, $(K+1)! \ge 8r/\epsilon$ holds for $K = O(\log(r/\epsilon)/\log\log(r/\epsilon))$.
