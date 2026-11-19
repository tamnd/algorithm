---
title: The all-pole fit and the cepstrum of PLP are well defined and correct
proves: [correctness]
status: full
---

We work in the real RAM. Lines L1 to L6 compute the auditory spectrum $\phi[0], \ldots, \phi[M-1]$ by direct formulas, so there is nothing to prove about them beyond the definitions on the page. We prove that lines L7 to L9 are well defined and compute the cepstrum of an all-pole model of $\phi$, and that a gain on the frame changes only $c_0$. Let $n = 2(M - 1)$ and assume $M \ge 2$, $1 \le p < n$ and $\phi[i] > 0$ for every $i$.

Let $\tilde\phi$ be the even extension of $\phi$ to $n$ points: $\tilde\phi[i] = \phi[i]$ for $0 \le i \le M - 1$ and $\tilde\phi[i] = \phi[n - i]$ for $M \le i \le n - 1$. Let $\omega_i = 2\pi i / n$.

**Lemma 1 (line L7 is an inverse DFT).** For $0 \le \tau \le p$, $r[\tau] = \frac{1}{n} \sum_{i=0}^{n-1} \tilde\phi[i]\, e^{j \omega_i \tau}$, and this number is real.

*Proof.* Pair the term $i$ with the term $n - i$ for $1 \le i \le M - 2$. They have the same $\tilde\phi$ and conjugate exponentials, so together they give $2 \phi[i] \cos(\pi \tau i / (M - 1))$. The term $i = 0$ gives $\phi[0]$, and the term $i = M - 1$ gives $\phi[M - 1] e^{j\pi\tau} = \phi[M-1] \cos(\pi \tau)$. Dividing by $n$ gives line L7. $\square$

**Lemma 2 (positive definite).** The $(p+1) \times (p+1)$ Toeplitz matrix $R$ with $R_{s,t} = r[|s - t|]$ is positive definite.

*Proof.* Since $r[-\tau] = r[\tau]$ by Lemma 1 (the sum is real and even in $\tau$), $R_{s,t} = \frac{1}{n} \sum_i \tilde\phi[i] e^{j\omega_i (s - t)}$. For a real vector $v \ne 0$,

$$v^{\mathsf T} R v = \frac{1}{n} \sum_{i=0}^{n-1} \tilde\phi[i]\, \Bigl|\sum_{s=0}^{p} v_s e^{j\omega_i s}\Bigr|^2 \ge 0.$$

Equality would need the polynomial $V(z) = \sum_s v_s z^s$, of degree at most $p$ and not zero, to vanish at the $n$ distinct points $e^{j\omega_i}$, because every $\tilde\phi[i] > 0$. A nonzero polynomial of degree at most $p < n$ has fewer than $n$ roots, so the sum is positive. $\square$

**Lemma 3 (line L8).** On a positive definite Toeplitz matrix, the [Levinson-Durbin recursion](/levinson-durbin-recursion/) never divides by zero, every reflection coefficient satisfies $|k_i| < 1$, every prediction error $e_i$ is positive, and the result $a_1, \ldots, a_p$ solves the normal equations $\sum_{k=1}^{p} a_k r[|i - k|] = r[i]$ for $1 \le i \le p$, with $g = e_p = r[0] - \sum_k a_k r[k] > 0$. The polynomial $A(z) = 1 - \sum_k a_k z^{-k}$ then has all its zeros strictly inside the unit circle.

*Proof.* These are the standard facts about the recursion, proved on the [Levinson-Durbin recursion](/levinson-durbin-recursion/) page: the error after step $i$ is $e_i = \det R_{i+1} / \det R_i$, a ratio of leading principal minors, so it is positive, and $e_i = e_{i-1}(1 - k_i^2)$ forces $|k_i| < 1$. A polynomial built by the recursion from reflection coefficients of modulus below 1 has its zeros inside the unit circle, which is the stability result of the lattice form (the Schur-Cohn test read backwards). $\square$

**Lemma 4 (line L9 is the cepstrum).** Let $A$ have all its zeros inside the unit circle and $g > 0$. Define $c_0 = \ln g$ and $c_m$ for $m \ge 1$ by line L9. Then for every real $\omega$,

$$\ln \frac{g}{|A(e^{j\omega})|^2} = \sum_{m=-\infty}^{\infty} c_{|m|}\, e^{-j\omega m}.$$

*Proof.* Write $A(z) = \prod_{i=1}^{p} (1 - z_i z^{-1})$ with $|z_i| < 1$. For $|z| \ge 1$ each factor has the convergent series $\ln(1 - z_i z^{-1}) = -\sum_{m \ge 1} z_i^m z^{-m} / m$, so $L(z) = -\ln A(z) = \sum_{m \ge 1} \hat c_m z^{-m}$ converges for $|z| \ge 1$, with real $\hat c_m$ because the $a_k$ are real. Differentiate $A(z) e^{L(z)} = 1$, or equivalently $L'(z) A(z) = -A'(z)$, and multiply by $-z$:

$$\Bigl(\sum_{m \ge 1} m \hat c_m z^{-m}\Bigr)\Bigl(1 - \sum_{k=1}^{p} a_k z^{-k}\Bigr) = \sum_{k=1}^{p} k a_k z^{-k}.$$

The coefficient of $z^{-m}$ gives $m \hat c_m - \sum_{k=1}^{m-1} k \hat c_k a_{m-k} = m a_m$, with $a_j = 0$ for $j > p$. Dividing by $m$ gives the recursion of line L9, so $\hat c_m = c_m$ for $m \ge 1$ by induction on $m$. Finally $\ln(g / |A|^2) = \ln g - \ln A(e^{j\omega}) - \overline{\ln A(e^{j\omega})} = \ln g + \sum_{m \ge 1} c_m (e^{-j\omega m} + e^{j\omega m})$. $\square$

**Lemma 5 (a gain moves only $c_0$).** If the frame is multiplied by $s \ne 0$ and every $\phi[i] > 0$, then $a$ is unchanged, $g$ is multiplied by $|s|^{0.66}$, $c_0$ grows by $0.66 \ln |s|$, and $c_m$ for $m \ge 1$ is unchanged.

*Proof.* $P$ scales by $s^2$ in line L1. Lines L3 and L4 are linear, so $\theta$ and $\xi$ scale by $s^2$, and line L5 gives $\phi$ scaled by $(s^2)^{0.33} = |s|^{0.66}$. Line L6 copies values, and line L7 is linear, so $r$ scales by the same factor $\lambda = |s|^{0.66}$. The normal equations of Lemma 3 are unchanged when $r$ is scaled, so $a$ is the same, and $g = r[0] - \sum a_k r[k]$ scales by $\lambda$. In line L9, $c_0 = \ln g$ grows by $\ln \lambda$, and the $c_m$ for $m \ge 1$ depend only on $a$. $\square$

**Theorem.** If the auditory spectrum is positive and $p < 2(M - 1)$, PLP returns the first $K + 1$ cepstral coefficients of a stable all-pole model $g / |A|^2$ whose predictor solves the normal equations of the autocorrelation $r$ of $\phi$, and a gain on the frame changes only $c_0$.

*Proof.* Lemmas 1 to 5. $\square$

The tests check Lemma 1 against a complex inverse DFT, Lemma 3 against a direct solve of the normal equations, Lemma 4 against the inverse DFT of the log model spectrum on 1024 points, and Lemma 5 with a gain of 4.
