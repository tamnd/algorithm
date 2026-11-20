---
title: The Jakes simulator has time-average power Omega, and its time-average autocorrelation is the N-point trapezoid rule for J0
proves: [correctness]
status: full
---

Let $N = 4M + 2$, $\nu_0 = 1$, $\nu_n = \cos(2\pi n/N)$ and $\omega_n = 2\pi f_D \nu_n$ for $n = 1, \ldots, M$, with the gains $a_n, b_n$ of line L4. The output is

$$h(t) = \sqrt{2\Omega/N}\, \sum_{n=0}^{M} (a_n + j b_n) \cos(\omega_n t).$$

For a function $g$, write $\langle g \rangle = \lim_{T \to \infty} \frac{1}{2T} \int_{-T}^{T} g(t)\, dt$ for the time average.

**Lemma 1 (distinct frequencies).** For $f_D > 0$ the frequencies $\omega_0, \ldots, \omega_M$ are distinct and positive.

*Proof.* The angles $2\pi n/N$ for $n = 0, \ldots, M$ lie in $[0, \pi/2)$, because $2\pi M/(4M + 2) < \pi/2$. The cosine is strictly decreasing and positive there. $\square$

**Lemma 2 (time averages of products).** For $\omega, \omega' > 0$, $\langle \cos(\omega (t + \tau)) \cos(\omega' t) \rangle$ is $\frac12 \cos(\omega \tau)$ if $\omega = \omega'$ and $0$ otherwise.

*Proof.* The product is $\frac12 [\cos(\omega \tau + (\omega + \omega') t) + \cos(\omega\tau + (\omega - \omega') t)]$. The time average of $\cos(c + d t)$ is $0$ for $d \ne 0$, because its integral over $[-T, T]$ is bounded by $2/|d|$, and it is $\cos c$ for $d = 0$. $\square$

**Lemma 3 (the gains).** $a_0^2 + b_0^2 = 2$, $a_n^2 + b_n^2 = 4$ for $n \ge 1$, and $\sum_n a_n^2 = \sum_n b_n^2 = N/2$.

*Proof.* The first two follow from $\cos^2 + \sin^2 = 1$. Next, $a_0^2 = 2\cos^2(\pi/4) = 1$, and $\sum_{n=1}^{M} 4\cos^2(\pi n/M) = 2M + 2\sum_{n=1}^{M} \cos(2\pi n/M)$. The last sum is $0$ for $M \ge 2$, because it is the real part of the sum of all $M$-th roots of unity, so $\sum a_n^2 = 1 + 2M = N/2$. For $M = 1$ the sum is $\cos 2\pi = 1$, and $a = (1, -2)$ gives $5 \ne N/2 = 3$; so the equal power holds for $M \ge 2$, and the same computation with sines gives $\sum b_n^2 = N/2$ for $M \ge 2$. $\square$

**Theorem 1 (power and autocorrelation).** For $f_D > 0$, $\langle |h|^2 \rangle = \Omega$, and

$$\frac{1}{\Omega} \langle h(t + \tau)\, \overline{h(t)} \rangle = R(\tau) = \frac{2}{N}\Big[\cos x + 2 \sum_{n=1}^{M} \cos(x \nu_n)\Big], \qquad x = 2\pi f_D \tau.$$

*Proof.* Expand the product into the double sum over $n, k$ of $(a_n + j b_n)(a_k - j b_k) \cos(\omega_n (t+\tau)) \cos(\omega_k t)$. By Lemmas 1 and 2, only $n = k$ survives the time average, and it gives $\frac12 (a_n^2 + b_n^2) \cos(\omega_n \tau)$. With Lemma 3 and the factor $2\Omega/N$ this is $\frac{2\Omega}{N}[\cos(\omega_0 \tau) + 2\sum_{n \ge 1} \cos(\omega_n \tau)]$, which is $\Omega R(\tau)$. At $\tau = 0$, $R(0) = (2/N)(1 + 2M) = 1$. $\square$

**Lemma 4 (folding).** $R(\tau) = \frac{1}{N} \sum_{k=0}^{N-1} \cos(x \cos(2\pi k/N))$.

*Proof.* The term $k = 0$ gives $\cos x$, and so does $k = N/2 = 2M + 1$, because $\cos \pi = -1$ and the cosine is even. The terms $k$ and $N - k$ are equal. For $1 \le k \le M$, the term $k' = 2M + 1 - k$ has $\cos(2\pi k'/N) = \cos(\pi - 2\pi k/N) = -\cos(2\pi k/N)$, so it is equal to the term $k$. So the indices $1, \ldots, N-1$ other than $N/2$ form $M$ groups of four equal terms, and the sum is $2\cos x + 4\sum_{k=1}^{M} \cos(x \nu_k)$. Divide by $N$. $\square$

**Theorem 2 (the error).** $R(\tau) = J_0(x) + 2 \sum_{m \ge 1} (-1)^m J_{mN}(x)$.

*Proof.* The Jacobi-Anger expansion gives $\cos(x\cos\theta) = J_0(x) + 2\sum_{k \ge 1} (-1)^k J_{2k}(x) \cos(2k\theta)$, and the series converges absolutely and uniformly in $\theta$. Average it over $\theta_j = 2\pi j/N$, $j = 0, \ldots, N-1$. The average of $\cos(2k\theta_j)$ is 1 if $N$ divides $2k$ and 0 otherwise. Since $N$ is even, $N \mid 2k$ means $2k = mN$ with $k = m(2M + 1)$, and $(-1)^k = (-1)^m$ because $2M + 1$ is odd. By Lemma 4 the average is $R(\tau)$. $\square$

Since $|J_n(x)| \le (x/2)^n / n!$, the error term is tiny while $x$ is well below $N$: for $M = 8$, the difference from $J_0$ stays below $10^{-5}$ up to $f_D\tau = 3$. When $x$ approaches $N$, $J_N(x)$ is no longer small, and the error is of the size of $J_0$ itself.

**Remark (no stationarity).** $h$ is a fixed function of $t$. A wide-sense stationary process needs $E[h(t + \tau)\overline{h(t)}]$ to be independent of $t$, and here the only expectation is the value itself. For example, $|h(0)|^2/\Omega = (2/N)[(\sum a_n)^2 + (\sum b_n)^2]$, with $\sum a_n = 1 + 2\sum_{n=1}^{M} \cos(\pi n/M) = -1$ and $\sum b_n = 1 + 2\sum_{n=1}^{M} \sin(\pi n /M) = 1 + 2\cot(\pi/(2M))$, which is $7.25$ for $M = 8$, while $\langle |h|^2 \rangle / \Omega = 1$. With independent uniform phases $\phi_n$ added to the oscillators, $E[\cos(\omega_n(t+\tau) + \phi_n)\cos(\omega_k t + \phi_k)]$ is $\frac12 \cos(\omega_n\tau)$ for $n = k$ and 0 otherwise, so the same computation as in Theorem 1 gives the ensemble autocorrelation $\Omega R(\tau)$ for every $t$: this is the variant of Pop and Beaulieu.
