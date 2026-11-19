---
title: The cepstrum of a model voiced signal and when its peak is the pitch period
proves: [correctness]
status: full
---

The cepstral detector is an estimator, so its correctness has two parts. First, lines L1 to L4 compute the real cepstrum. Second, for a model voiced signal, the largest value of the cepstrum in the search range is at the pitch period, under a stated condition. We work in the real RAM. The window of line L1 is not part of the model, and we say below what is lost.

**Lemma 1 (two FFTs give the real cepstrum).** Let $y$ be real of length $M$, $Y$ its DFT and $L[k] = \ln |Y[k]|$. Then the inverse DFT $c[q] = \frac{1}{M} \sum_k L[k] e^{2\pi i k q / M}$ is real, $c[q] = c[M - q]$, and $c[q] = \frac{1}{M} \sum_k L[k] e^{-2\pi i k q / M}$.

*Proof.* Since $y$ is real, $Y[M - k] = \overline{Y[k]}$, so $L[M - k] = L[k]$ (indices mod $M$). Substitute $k \to M - k$ in the sum for $c[q]$: the sum becomes $\frac{1}{M} \sum_k L[k] e^{-2\pi i k q / M}$, which is the forward DFT of $L$ divided by $M$, and also the complex conjugate of the original sum because $L$ is real. A number equal to its conjugate is real. The same substitution with $q \to M - q$ gives $c[M - q] = c[q]$. $\square$

So line L4, which applies the forward FFT to $L$ and divides by $M$, computes $c$, and lines L5 and L6 need only $q < M / 2$.

**The model.** Let $A(z) = \prod_{i=1}^{p} (1 - p_i z^{-1})$ with every $|p_i| < 1$, let $h$ be the impulse response of $1 / A(z)$, and let

$$e[n] = \sum_{j=0}^{K-1} \beta^j \delta[n - jP], \qquad 0 < \beta < 1, \; P \ge 1, \; K \ge 1.$$

The signal is $x = h * e$. We use the transforms on the unit circle, $X(\omega) = H(\omega) E(\omega)$, and the complex cepstrum $\hat x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} \log X(\omega)\, e^{i \omega n}\, d\omega$ with the continuous branch of the logarithm that is 0 at $z = \infty$. The real cepstrum is $c[n] = \frac{1}{2\pi} \int \ln |X(\omega)|\, e^{i\omega n}\, d\omega = (\hat x[n] + \hat x[-n]) / 2$, because $\ln |X| = \operatorname{Re} \log X$.

**Lemma 2 (convolution adds cepstra).** $\hat x = \hat h + \hat e$ and $c_x = c_h + c_e$.

*Proof.* $\log (H E) = \log H + \log E$ for the continuous branches, and $\ln |HE| = \ln |H| + \ln |E|$. The inverse transform is linear. $\square$

**Lemma 3 (the all-pole part).** $\hat h[0] = 0$, $\hat h[n] = \sum_i p_i^n / n$ for $n \ge 1$ and $\hat h[n] = 0$ for $n < 0$. The coefficients of $A(z) = 1 - \sum_k a_k z^{-k}$ give the same values by $\hat h[n] = a_n + \sum_{k=1}^{n-1} (k / n)\, \hat h[k]\, a_{n-k}$, with $a_n = 0$ for $n > p$.

*Proof.* For $|z| \ge 1 > |p_i|$, $-\log(1 - p_i z^{-1}) = \sum_{n \ge 1} p_i^n z^{-n} / n$, a convergent power series in $z^{-1}$. Summing over $i$ gives $\log H(z) = \sum_{n \ge 1} (\sum_i p_i^n / n) z^{-n}$, and the coefficients of this Laurent series are the complex cepstrum. For the recursion, differentiate $\log H = -\log A$: $z\, H'(z) / H(z) = -z A'(z) / A(z)$, so $A(z) \cdot \sum_n n \hat h[n] z^{-n} = \sum_k k a_k z^{-k}$. Comparing the coefficients of $z^{-n}$ gives $n \hat h[n] - \sum_{k=1}^{n-1} a_{n-k}\, k \hat h[k] = n a_n$, which is the recursion. $\square$

**Lemma 4 (the pulse part).** $\hat e[n] = 0$ unless $n = jP$ with $j \ge 1$, and

$$\hat e[jP] = \frac{\beta^j}{j} - [K \mid j]\, \frac{K \beta^j}{j}.$$

*Proof.* $E(z) = \sum_{j=0}^{K-1} \beta^j z^{-jP} = \dfrac{1 - \beta^K z^{-KP}}{1 - \beta z^{-P}}$. Both factors have their zeros at $|z| < 1$. For $|z| \ge 1$, $-\log(1 - \beta z^{-P}) = \sum_{j \ge 1} \beta^j z^{-jP} / j$ and $\log(1 - \beta^K z^{-KP}) = -\sum_{m \ge 1} \beta^{Km} z^{-mKP} / m$. Writing $j = mK$ in the second sum, its coefficient of $z^{-jP}$ is $-\beta^j / (j / K) = -K \beta^j / j$. $\square$

By Lemmas 2 to 4, $\hat x$ is 0 at negative indices, so $c[n] = \hat x[n] / 2$ for $n \ge 1$:

$$c[n] = \tfrac12 \hat h[n] + \tfrac12 \hat e[n].$$

**Theorem.** Let $K \ge 2$ and $1 \le q_{\min} \le P \le q_{\max}$, and let $\rho = \max_{q_{\min} \le n \le q_{\max}} |\hat h[n]|$. If $\beta - \beta^2 / 2 > 2\rho$, then over $q_{\min} \le n \le q_{\max}$ the real cepstrum of the model signal has its unique maximum at $n = P$.

*Proof.* At $n = P$ we have $j = 1$, and $K \ge 2$ does not divide 1, so $\hat e[P] = \beta$ and $c[P] \ge (\beta - \rho) / 2$. (With $K = 1$ there is one pulse and no period: $\hat e[P] = 0$.) At any other $n$ in the range, either $\hat e[n] = 0$, or $n = jP$ with $j \ge 2$ and $\hat e[n] \le \beta^j / j \le \beta^2 / 2$, since $\beta^j / j$ decreases in $j$ for $0 < \beta < 1$. So $c[n] \le (\rho + \beta^2 / 2) / 2$. The condition gives $(\beta - \rho) / 2 > (\rho + \beta^2 / 2) / 2$. $\square$

The value $\rho$ is small when the poles are not close to the unit circle: by Lemma 3, $|\hat h[n]| \le \sum_i |p_i|^n / n \le \sum_i |p_i|^{q_{\min}} / q_{\min}$ for $n \ge q_{\min}$. For one pole pair of radius $0.9$ and $q_{\min} = 20$ the bound is $2 \cdot 0.9^{20} / 20 = 0.0122$, so any $\beta \ge 0.05$ satisfies the condition.

**Finite FFT length.** The DFT of length $M$ samples the transform at $\omega = 2\pi k / M$, and the inverse DFT of the sampled log magnitude is the aliased sum $c_M[q] = \sum_{l} c[q + lM]$. The series converges absolutely, because $|c[n]| \le (\sum_i |p_i|^{|n|} + K \beta^{|n| / P}) / (2|n|)$. So the theorem holds for $c_M$ when $\beta - \beta^2/2 - 2\rho$ is larger than twice $\max_q |c_M[q] - c[q]|$, which tends to 0 as $M$ grows. This is the condition under which the code returns $q^* = P$ for the model; the test of the implementation checks the closed form of Lemmas 3 and 4 to $10^{-9}$ with $M = 4096$.

**What the window changes.** Line L1 multiplies $x$ by a window. The product is not $h * e'$ for a new pulse train $e'$, so the lemmas do not apply exactly. When the window changes little over the length of $h$, $w \cdot (h * e) \approx h * (w \cdot e)$, and $w \cdot e$ is a pulse train with slowly varying amplitudes, whose cepstrum still sits at multiples of $P$. This is an approximation. That the peak stays at $P$ for real frames is a measurement, as in the example on the page. Lines L5 to L8 then return $f_s / q^*$ for the largest peak in the range, as the page states, and the voicing threshold of line L7 is a heuristic.
