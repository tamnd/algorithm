---
title: With ideal feedback, the MMSE-DFE feedback taps are the postcursors of the combined response and the feedforward taps solve a Wiener problem with the feedback columns removed
proves: [correctness]
status: full
---

The channel taps are $h_0, \ldots, h_{L-1}$, not all zero. The received samples are $y[n] = \sum_l h_l\, x[n-l] + w[n]$, where the symbols $x[n]$ are independent with mean zero and $E|x[n]|^2 = E_s$, and the noise samples $w[n] \sim \mathcal{CN}(0, N_0)$ are independent of each other and of the symbols. The feedforward filter has the taps $c_0, \ldots, c_{N_f-1}$ and the output $z[n] = \sum_i c_i\, y[n-i]$. The feedback filter has the taps $b_1, \ldots, b_{N_b}$. The slicer input for the symbol $x[n - \Delta]$ is
$$q[n] = z[n] - \sum_{j=1}^{N_b} b_j\, \hat x[n - \Delta - j],$$
and the decision is the alphabet point nearest to $q[n] / \gamma$ for a fixed gain $\gamma > 0$ (lines L9 to L12).

Let $u = (y[n], \ldots, y[n-N_f+1])^T$ and $s = (x[n], \ldots, x[n - N_f - L + 2])^T$. As for the linear equalizer, $u = Hs + v$ with the $N_f \times (N_f + L - 1)$ matrix $H_{ij} = h_{j-i}$ (line L1) and the noise vector $v$, with $E[ss^H] = E_s I$, $E[vv^H] = N_0 I$ and $E[sv^H] = 0$. Write $f = \bar c$, so $z[n] = f^H u$, and $g = c * h$, so $g_j = \sum_i c_i h_{j-i}$ is the gain from $x[n-j]$ to $z[n]$. Let $B = \{\Delta + 1, \ldots, \Delta + N_b\}$ be the feedback positions and $K$ the other column indices (line L2). Entries of $g$ at indices past its end are 0.

Ideal feedback means $\hat x[n - \Delta - j] = x[n - \Delta - j]$ for $j = 1, \ldots, N_b$. The design (lines L1 to L8) assumes it. Theorem 3 says when the decisions are in fact correct.

**Lemma 1 (the error of any taps).** With ideal feedback, for every $c$ and $b$,
$$J(c, b) = E|q[n] - x[n-\Delta]|^2 = E_s \sum_{j \in K} |g_j - [j = \Delta]|^2 + E_s \sum_{t=1}^{N_b} |g_{\Delta+t} - b_t|^2 + N_0 \|c\|^2 .$$

*Proof.* $q[n] - x[n-\Delta] = \sum_j (g_j - [j = \Delta] - [j \in B]\, b_{j - \Delta})\, x[n-j] + \sum_i c_i\, w[n-i]$. The terms are independent with mean zero, so the variances add. $\square$

**Lemma 2 (the best feedback for fixed feedforward taps).** For a fixed $c$, the unique minimizer of $J(c, \cdot)$ is $b_t = g_{\Delta+t}$ for $t = 1, \ldots, N_b$, and then
$$J(c, b) = E|f^H u_K - x[n - \Delta]|^2,$$
where $u_K = H_K s_K + v$, with $H_K$ the columns of $H$ in $K$ and $s_K$ the entries of $s$ in $K$.

*Proof.* In Lemma 1, $b$ appears only in the middle sum, which is zero exactly when $b_t = g_{\Delta+t}$ for every $t$. The remaining two terms are the error of the filter $f$ against the regressor $u_K$ by the same computation as Lemma 1, because $f^H H_K s_K = \sum_{j \in K} g_j x[n-j]$. $\square$

**Lemma 3 (R is positive definite).** $R = E_s H_K H_K^H + N_0 I$ (line L3) is Hermitian, and it is positive definite if $N_0 > 0$.

*Proof.* For $a \ne 0$, $a^H R a = E_s \|H_K^H a\|^2 + N_0 \|a\|^2 > 0$. $\square$

If $N_0 = 0$, $R$ can be singular, because removing the columns $B$ can make the rows of $H_K$ dependent. The implementation then raises an error.

**Theorem 1 (the MMSE-DFE).** Let $r = E_s H e_\Delta$ (line L4). Since $\Delta \in K$, $r = E_s H_K e'_\Delta$ for the matching unit vector $e'_\Delta$, so $r = E[u_K\, \overline{x[n-\Delta]}]$. If $R$ is positive definite, the taps $c = \bar f$ with $R f = r$ (line L5) and $b_t = g_{\Delta + t}$ (lines L7 and L8) are the unique joint minimizer of $J(c, b)$, and the minimum is $J = E_s - r^H f$ (line L6).

*Proof.* By Lemma 2, $\min_{c, b} J(c, b) = \min_f E|f^H u_K - x[n-\Delta]|^2$, and the minimizing $b$ is unique for each $c$. The right side is a Wiener problem with the covariance $E[u_K u_K^H] = R$ and the cross-correlation $r$. Expanding it gives $f^H R f - 2\,\mathrm{Re}(f^H r) + E_s$, and completing the square gives
$$E_s - r^H R^{-1} r + (f - R^{-1} r)^H R\, (f - R^{-1} r).$$
The last term is positive for $f \ne R^{-1} r$ because $R$ is positive definite. So $f = R^{-1} r$ is the unique minimizer, with the value $E_s - r^H f$. $\square$

**Corollary 1 (the bias).** The cursor of the combined response is $g_\Delta = 1 - J/E_s$, a real number in $(0, 1]$ when $N_0 > 0$.

*Proof.* $g_\Delta = \sum_i c_i h_{\Delta - i} = f^H H e_\Delta = f^H r / E_s = r^H R^{-1} r / E_s$, which is real and nonnegative. By Theorem 1 it equals $(E_s - J)/E_s$. $J > 0$ when $N_0 > 0$ because $N_0 \|c\|^2 > 0$ unless $c = 0$, and $c = 0$ gives $J = E_s$. $\square$

So with ideal feedback $q[n] = (1 - J/E_s)\, x[n - \Delta] + e'[n]$, where $e'[n]$ has mean zero and is uncorrelated with $x[n - \Delta]$, by the orthogonality of the Wiener error. Line L12 divides by $\gamma = 1 - J/E_s$ before the slicer.

**Corollary 2 (more feedback taps never hurt).** For fixed $N_f$ and $\Delta$, the minimum $J$ does not increase with $N_b$. In particular, with $N_b = 0$ it is the error of the linear MMSE equalizer, so the MMSE-DFE with ideal feedback is never worse than the linear MMSE equalizer of the same length.

*Proof.* A DFE with $N_b$ taps and $b_{N_b} = 0$ is a DFE with $N_b - 1$ taps. So the set over which Theorem 1 minimizes grows with $N_b$. $\square$

**Theorem 2 (the zero-forcing DFE).** If $h_0 \ne 0$, $N_f = 1$, $\Delta = 0$ and $N_b \ge L - 1$, the taps $c_0 = 1/h_0$ and $b_t = h_t / h_0$ remove all ISI, and the error is $N_0 / |h_0|^2$.

*Proof.* $g = h / h_0$, so $g_0 = 1$, and $b_t = g_t$ cancels every postcursor in Lemma 1. The only term left is $N_0 |c_0|^2$. $\square$

**Theorem 3 (no error propagation without noise).** Let $d_{\min}$ be the minimum distance of the alphabet, $A = \max |a|$ over the alphabet, and let the taps satisfy $\gamma > 0$ and
$$\rho = A \sum_{j \in K,\, j \ne \Delta} |g_j| + A \sum_{t=1}^{N_b} |g_{\Delta+t} - b_t| < \gamma\, \frac{d_{\min}}{2} - A\, |g_\Delta - \gamma| .$$
If $w = 0$ and the symbols before $x[0]$ are 0 in both the channel and the run, then line L12 decides every symbol correctly.

*Proof.* By induction on $k$. Assume $\hat x[i] = x[i]$ for all $i < k$. Then the feedback at step $k$ equals the ideal feedback, and by the computation of Lemma 1 with $w = 0$, $q - \gamma x[k] = (g_\Delta - \gamma) x[k] + \sum_{j \in K, j \ne \Delta} g_j x[k + \Delta - j] + \sum_t (g_{\Delta+t} - b_t)\, x[k - t]$. Its modulus is at most $A |g_\Delta - \gamma| + \rho < \gamma d_{\min}/2$. So $|q/\gamma - x[k]| < d_{\min}/2$, and $x[k]$ is the unique nearest point. $\square$

For the MMSE taps with $\gamma = 1 - J/E_s$, the term $|g_\Delta - \gamma|$ is 0 by Corollary 1 and the second sum is 0 by Theorem 1. The condition then asks only that the residual precursor and far postcursor ISI is small, which holds for long filters at high SNR.

**Corollary 3 (recovery after errors).** Assume the condition of Theorem 3, let $\mu = \gamma d_{\min}/2 - A|g_\Delta - \gamma| - \rho > 0$ be the margin, and let the noise term $\sum_i c_i w[k + \Delta - i]$ have modulus less than $\mu$ from step $k$ on. If the $N_b$ decisions before step $k$ are correct, every decision from step $k$ on is correct.

*Proof.* The induction step of Theorem 3 uses only the $N_b$ decisions before the current step, because the feedforward filter does not use decisions. With the noise term added, the bound on $|q - \gamma x[k]|$ becomes less than $A|g_\Delta - \gamma| + \rho + \mu = \gamma d_{\min}/2$, and the induction goes through. $\square$

So a wrong decision enters the next $N_b$ slicer inputs with the weights $b_t$ and can cause more errors, but the burst ends after $N_b$ correct decisions in a row when the noise is small.

The size of the error bursts with noise is a property of the channel and the SNR. The page gives a measurement, not a bound.
