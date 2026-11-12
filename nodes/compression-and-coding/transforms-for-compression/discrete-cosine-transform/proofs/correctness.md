---
title: The DCT-II is orthonormal, Lee's split computes it, and it is the limit of the AR(1) KLT
proves: [correctness]
status: full
---

We write $\theta_{n,k} = \frac{\pi (2n+1) k}{2N}$, $\hat X[k] = \sum_{n=0}^{N-1} x[n] \cos\theta_{n,k}$ for the unnormalized DCT-II, and $X[k] = a_k \hat X[k]$ with $a_0 = \sqrt{1/N}$ and $a_k = \sqrt{2/N}$ for $k \ge 1$. The matrix $C$ has the entries $C_{kn} = a_k \cos\theta_{n,k}$.

**Lemma 1 (cosine sum).** For each integer $p$,

$$S(p) = \sum_{n=0}^{N-1} \cos\frac{\pi(2n+1)p}{2N} = \begin{cases} N(-1)^{p/(2N)} & \text{if } 2N \mid p, \\ 0 & \text{otherwise.} \end{cases}$$

*Proof.* Let $z = e^{i\pi p/(2N)}$, so $S(p) = \operatorname{Re} \sum_{n=0}^{N-1} z^{2n+1}$. If $2N \mid p$, then $z = e^{i\pi p/(2N)} = (-1)^{p/(2N)}$ is real with $z^2 = 1$, and each term is $z^{2n+1} = z$, so $S(p) = Nz$. Otherwise $z^2 = e^{i\pi p/N} \ne 1$, and the geometric sum gives

$$\sum_{n=0}^{N-1} z^{2n+1} = z\,\frac{z^{2N} - 1}{z^2 - 1} = \frac{(-1)^p - 1}{z - z^{-1}} .$$

If $p$ is even the numerator is 0. If $p$ is odd the value is $-2/(z - z^{-1}) = -2/(2i\sin\frac{\pi p}{2N}) = i/\sin\frac{\pi p}{2N}$, which is purely imaginary (the sine is not zero, because $z^2 \ne 1$). In both cases the real part is 0. $\square$

**Lemma 2 (orthonormality).** $C C^{\mathsf T} = C^{\mathsf T} C = I_N$. So DCT computes $X = Cx$ and IDCT computes $C^{\mathsf T} X = x$.

*Proof.* Let $0 \le j, k \le N-1$. From $\cos\alpha\cos\beta = \frac12(\cos(\alpha - \beta) + \cos(\alpha + \beta))$,

$$\sum_{n} \cos\theta_{n,j} \cos\theta_{n,k} = \tfrac12 S(j - k) + \tfrac12 S(j + k).$$

Here $|j - k| \le N - 1 < 2N$ and $0 \le j + k \le 2N - 2 < 2N$, so by Lemma 1 each $S$ term is $N$ if its argument is 0 and 0 otherwise. If $j \ne k$ both arguments are nonzero, and the sum is 0. If $j = k \ge 1$, the sum is $\frac N2 + 0$. If $j = k = 0$, it is $\frac N2 + \frac N2 = N$. Then $(CC^{\mathsf T})_{jk} = a_j a_k \sum_n \cos\theta_{n,j}\cos\theta_{n,k}$ is 0 for $j \ne k$, $\frac1N \cdot N = 1$ for $j = k = 0$, and $\frac2N \cdot \frac N2 = 1$ for $j = k \ge 1$. A square matrix with $CC^{\mathsf T} = I$ is invertible with $C^{-1} = C^{\mathsf T}$, so also $C^{\mathsf T}C = I$. Lines L1 to L4 compute row $k$ of $Cx$ for each $k$; lines L5 to L7 compute entry $n$ of $C^{\mathsf T} X = \sum_k C_{kn} X[k]$. $\square$

**Lemma 3 (Lee's split).** Let $N \ge 2$ be a power of two and $h = N/2$. Define $u$ and $v$ as in lines F3 and F4, and let $U$ and $V$ be the unnormalized DCT-II of length $h$ of $u$ and $v$, with $V[h] = 0$. Then for $0 \le m < h$,

$$\hat X[2m] = U[m], \qquad \hat X[2m+1] = V[m] + V[m+1].$$

*Proof.* The divisor of line F4 is $2\cos\beta_i$ with $\beta_i = \frac{\pi(2i+1)}{2N}$, and $0 < \beta_i \le \frac{\pi(N-1)}{2N} < \frac\pi2$ for $0 \le i < h$, so it is positive.

For $n' = N - 1 - n$ we have $2n' + 1 = 2N - (2n+1)$, so $\theta_{n',k} = \pi k - \theta_{n,k}$ and $\cos\theta_{n',k} = (-1)^k \cos\theta_{n,k}$. Group the terms $n = i$ and $n = N - 1 - i$ for $0 \le i < h$; these pairs cover each index once.

*Even outputs.* For $k = 2m$, $(-1)^k = 1$, so

$$\hat X[2m] = \sum_{i<h} (x[i] + x[N-1-i]) \cos\frac{\pi(2i+1)2m}{2N} = \sum_{i<h} u[i] \cos\frac{\pi(2i+1)m}{2h} = U[m].$$

*Odd outputs.* For $k = 2m+1$, $(-1)^k = -1$, so with $\alpha = \frac{\pi(2i+1)(2m+1)}{2N} = (2m+1)\beta_i$,

$$\hat X[2m+1] = \sum_{i<h} (x[i] - x[N-1-i]) \cos\alpha = \sum_{i<h} v[i] \cdot 2\cos\beta_i \cos\alpha.$$

Now $2\cos\beta_i\cos((2m+1)\beta_i) = \cos(2m\beta_i) + \cos((2m+2)\beta_i)$, and $j\beta_i \cdot 2 = \frac{\pi(2i+1)j}{2h}$, so

$$\hat X[2m+1] = \sum_{i<h} v[i]\left(\cos\frac{\pi(2i+1)m}{2h} + \cos\frac{\pi(2i+1)(m+1)}{2h}\right) = V[m] + V[m+1].$$

For $m + 1 < h$, $V[m+1]$ is the DCT output. For $m + 1 = h$ the second cosine is $\cos\frac{\pi(2i+1)}{2} = 0$ for each $i$, so the sum is 0, which is the value $V[h] = 0$ that line F5 sets. $\square$

**Theorem 1 (LEE is correct).** For $N$ a power of two, LEE$(x)$ returns $\hat X$, and $a_k \cdot$LEE$(x)[k] = X[k]$.

*Proof.* By induction on $\log_2 N$. For $N = 1$, $\hat X[0] = x[0]\cos 0 = x[0]$, which line F1 returns. For $N \ge 2$, the recursive calls of line F5 are on vectors of length $N/2$, a smaller power of two, so by the induction hypothesis they return $U$ and $V$. Lines F6 to F8 then write $\hat X[2m]$ and $\hat X[2m+1]$ for each $m < N/2$ by Lemma 3; these indices cover $0, \dots, N-1$ once each. Each call halves the length, so the recursion has depth $\log_2 N$ and stops. $\square$

**Theorem 2 (inverse of LEE).** The inverse of the page computes $x$ from $\hat X$.

*Proof.* By Lemma 3, $U[m] = \hat X[2m]$, and $V[m] = \hat X[2m+1] - V[m+1]$ with $V[h] = 0$, so the backward loop from $m = h - 1$ to 0 finds each $V[m]$ from values that are already known. By induction the two half-length inverses return $u$ and $v$. With $d_i = 2\cos\beta_i\, v[i] = x[i] - x[N-1-i]$ and $u[i] = x[i] + x[N-1-i]$, we get $x[i] = (u[i] + d_i)/2$ and $x[N-1-i] = (u[i] - d_i)/2$. $\square$

**Lemma 4 (DCT from a DFT of length 2N).** Let $y = (x[0], \dots, x[N-1], x[N-1], \dots, x[0])$ and $Y[k] = \sum_{n=0}^{2N-1} y[n] e^{-2\pi i nk/(2N)}$. Then $e^{-i\pi k/(2N)} Y[k] = 2\hat X[k]$ for $0 \le k < N$.

*Proof.* $y[n] = x[n]$ and $y[2N-1-n] = x[n]$ for $0 \le n < N$, so

$$e^{-i\pi k/(2N)} Y[k] = \sum_{n<N} x[n]\left(e^{-i\pi(2n+1)k/(2N)} + e^{-i\pi(2(2N-1-n)+1)k/(2N)}\right).$$

The second exponent is $-i\pi(4N - (2n+1))k/(2N) = -2\pi i k + i\theta_{n,k}$, and $e^{-2\pi ik} = 1$. So the bracket is $e^{-i\theta_{n,k}} + e^{i\theta_{n,k}} = 2\cos\theta_{n,k}$. $\square$

**Theorem 3 (the 2D transform).** DCT-2D$(B)$ returns $CBC^{\mathsf T}$, and its inverse is $B = C^{\mathsf T} S C$.

*Proof.* Line L8 replaces each row $b$ of $B$ by $Cb$, which gives $BC^{\mathsf T}$. Line L9 replaces each column $r$ of that matrix by $Cr$, which gives $C(BC^{\mathsf T})$. By Lemma 2, $C^{\mathsf T}(CBC^{\mathsf T})C = B$. $\square$

**Theorem 4 (the KLT of AR(1) tends to the DCT-II).** Let $R_\rho$ be the $N \times N$ matrix with entries $\rho^{|i-j|}$, $0 < \rho < 1$. For each $k$, let $v_k(\rho)$ be a unit eigenvector of $R_\rho$ for its $(k+1)$-th largest eigenvalue, and let $c_k$ be row $k$ of $C$. Then $|\langle v_k(\rho), c_k \rangle| \to 1$ as $\rho \to 1$.

*Proof.* *Step 1: the inverse.* Let $Q_\rho$ be the tridiagonal matrix with diagonal $(1, 1+\rho^2, \dots, 1+\rho^2, 1)$ and $-\rho$ on the two off-diagonals. We show $R_\rho Q_\rho = (1-\rho^2) I$. Take a column $j$ with $0 < j < N-1$ and a row $i$, and let $d = |i - j|$. The entry is $(1+\rho^2)\rho^{d} - \rho(\rho^{|i-j+1|} + \rho^{|i-j-1|})$. If $d = 0$ this is $1 + \rho^2 - 2\rho^2 = 1 - \rho^2$. If $d \ge 1$ the two exponents are $d - 1$ and $d + 1$, and the entry is $\rho^d + \rho^{d+2} - \rho^{d} - \rho^{d+2} = 0$. For column $j = 0$ the entry is $\rho^i - \rho \cdot \rho^{|i-1|}$, which is $1 - \rho^2$ for $i = 0$ and $\rho^i - \rho^i = 0$ for $i \ge 1$. Column $N-1$ is the mirror case. So $R_\rho^{-1} = Q_\rho/(1-\rho^2)$, and $R_\rho$ and $Q_\rho$ have the same eigenvectors, with the order of the eigenvalues reversed: the $(k+1)$-th largest eigenvalue of $R_\rho$ belongs to the $(k+1)$-th smallest eigenvalue of $Q_\rho$.

*Step 2: the limit matrix.* $Q_1$ has diagonal $(1, 2, \dots, 2, 1)$ and $-1$ off the diagonal. We show $Q_1 c_k = \mu_k c_k$ with $\mu_k = 2 - 2\cos\frac{\pi k}{N}$. Let $f(n) = \cos\theta_{n,k}$, defined for all integers $n$. For $0 < n < N-1$, $(Q_1 f)(n) = 2f(n) - f(n-1) - f(n+1) = 2f(n) - 2\cos\frac{\pi k}{N} f(n) = \mu_k f(n)$, by $\cos(\alpha - \beta) + \cos(\alpha + \beta) = 2\cos\alpha\cos\beta$ with $\beta = \frac{\pi k}{N}$. At $n = 0$, $f(-1) = \cos(-\frac{\pi k}{2N}) = f(0)$, so $(Q_1 f)(0) = f(0) - f(1) = 2f(0) - f(-1) - f(1) = \mu_k f(0)$. At $n = N-1$, $f(N) = \cos(\pi k + \frac{\pi k}{2N}) = (-1)^k\cos\frac{\pi k}{2N}$ and $f(N-1) = \cos(\pi k - \frac{\pi k}{2N}) = (-1)^k\cos\frac{\pi k}{2N}$, so $f(N) = f(N-1)$ and the same argument works. The values $\mu_0 < \mu_1 < \dots < \mu_{N-1}$ are distinct, because $\cos$ is strictly decreasing on $[0, \pi)$. Let $\delta > 0$ be the smallest gap between two of them.

*Step 3: perturbation.* Let $E = Q_\rho - Q_1$. Its nonzero entries are $-(1-\rho^2)$ on the interior diagonal and $1-\rho$ off the diagonal, so $\|E\|_2 \le \max_i \sum_j |E_{ij}| \le (1-\rho^2) + 2(1-\rho) \le 4(1-\rho)$ (for a symmetric matrix the 2-norm is at most the largest row sum of absolute values). By Weyl's inequality each eigenvalue of $Q_\rho$ is within $\|E\|_2$ of the eigenvalue of $Q_1$ of the same rank. Let $\tilde\mu$ be the $(k+1)$-th smallest eigenvalue of $Q_\rho$, with unit eigenvector $v = v_k(\rho)$. When $\|E\|_2 < \delta/2$, $|\tilde\mu - \mu_k| \le \|E\|_2$, so $|\mu_j - \tilde\mu| \ge \delta - \|E\|_2 > \delta/2$ for each $j \ne k$; in particular $\tilde\mu$ is a simple eigenvalue and $v$ is fixed up to sign. Expand $v = \sum_j \beta_j c_j$ in the orthonormal eigenbasis $c_0, \dots, c_{N-1}$ of $Q_1$ (the rows of $C$, Lemma 2), so $\beta_k = \langle v, c_k\rangle$ and $\sum_j \beta_j^2 = 1$. The residual $r = Q_1 v - \tilde\mu v = (Q_\rho - E)v - \tilde\mu v = -Ev$ has $\|r\| \le \|E\|_2$, and $r = \sum_j \beta_j(\mu_j - \tilde\mu) c_j$, so

$$\|E\|_2^2 \ge \|r\|^2 \ge \sum_{j \ne k} \beta_j^2 (\mu_j - \tilde\mu)^2 \ge \frac{\delta^2}{4}\left(1 - \beta_k^2\right).$$

Hence $1 - \langle v, c_k\rangle^2 \le 4\|E\|_2^2/\delta^2 \le 64(1-\rho)^2/\delta^2$. This tends to 0 as $\rho \to 1$, so $|\langle v_k(\rho), c_k\rangle| \to 1$. $\square$

Step 3 shows that $1 - |\langle v_k, c_k\rangle| = O((1-\rho)^2)$, with a large constant. For $N = 8$ the largest value over $k$ goes from $1.83 \cdot 10^{-5}$ at $\rho = 0.99$ to $1.84 \cdot 10^{-7}$ at $\rho = 0.999$.

$\blacksquare$
