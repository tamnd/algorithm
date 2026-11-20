---
title: The Van Cittert iterate is a spectral filter, and it converges exactly where |1 - beta H| < 1
proves: [correctness]
status: full
---

**Setting.** Signals have length $n$ (an image is the same with a 2D index and the 2D DFT). The blur is periodic convolution $Ax = h \ast x$ with the PSF stored with its center at index $0$. The DFT is $\hat x_k = \sum_j x_j e^{-2\pi i jk/n}$, and $H_k = \hat h_k$. By the convolution theorem for the DFT, $\widehat{Ax}_k = H_k \hat x_k$, so $A$ is diagonal in the Fourier basis. The step size $\beta > 0$ is real. The iteration is lines L1 to L4:

$$x_0 = 0, \qquad x_{K+1} = x_K + \beta\,(y - A x_K).$$

**Claim 1 (closed form).** For every $K \ge 0$,

$$x_K = \beta \sum_{j=0}^{K-1} (I - \beta A)^j\, y, \qquad \hat x_{K,k} = \begin{cases} \dfrac{1 - (1 - \beta H_k)^K}{H_k}\, \hat y_k & H_k \ne 0, \\[2mm] K \beta\, \hat y_k & H_k = 0. \end{cases}$$

*Proof.* By induction on $K$. For $K = 0$ both sides are $0$. If the formula holds for $K$, then $x_{K+1} = (I - \beta A) x_K + \beta y = \beta \sum_{j=1}^{K} (I - \beta A)^j y + \beta y$, which is the formula for $K + 1$. In the Fourier basis $I - \beta A$ is multiplication by $1 - \beta H_k$, and the geometric sum is $\beta \sum_{j<K} (1 - \beta H_k)^j = (1 - (1 - \beta H_k)^K)/H_k$ for $H_k \ne 0$, and $K\beta$ for $H_k = 0$. $\square$

So $x_K$ is a spectral filter of the naive inverse $\hat y_k / H_k$ with the filter factors $f_k = 1 - (1 - \beta H_k)^K$, the Landweber form with $\beta$ in place of $\omega$ and $H_k$ in place of $\sigma^2$. The identity in Claim 1 is exact in rational arithmetic; the test compares the code with the matrix series.

**Claim 2 (exact data).** Let $y = A x^\dagger$, and let $P$ be the orthogonal projection onto the frequencies with $H_k \ne 0$, so that $Px^\dagger$ is the minimum norm solution of $Ax = y$. Then

$$\widehat{(x_K - P x^\dagger)}_k = \begin{cases} -(1 - \beta H_k)^K\, \hat x^\dagger_k & H_k \ne 0, \\ 0 & H_k = 0. \end{cases}$$

Hence $x_K \to P x^\dagger$ for every $x^\dagger$ if and only if $|1 - \beta H_k| < 1$ for every $k$ with $H_k \ne 0$.

*Proof.* $\hat y_k = H_k \hat x^\dagger_k$. For $H_k \ne 0$, Claim 1 gives $\hat x_{K,k} = (1 - (1 - \beta H_k)^K)\hat x^\dagger_k$, and $\widehat{(Px^\dagger)}_k = \hat x^\dagger_k$. For $H_k = 0$, $\hat y_k = 0$, so $\hat x_{K,k} = 0 = \widehat{(Px^\dagger)}_k$. The sequence $(1 - \beta H_k)^K$ tends to $0$ if $|1 - \beta H_k| < 1$. If $|1 - \beta H_k| \ge 1$ for some $k$ with $H_k \ne 0$, take $x^\dagger$ with only the frequency $k$ (and $-k$ for a real signal); then the error has modulus $|1 - \beta H_k|^K |\hat x^\dagger_k| \ge |\hat x^\dagger_k| > 0$ at every $K$, and it grows geometrically if $|1 - \beta H_k| > 1$. $\square$

**Claim 3 (the error never grows).** If $|1 - \beta H_k| \le 1$ for every $k$ and $y = Ax^\dagger$, then $\|x_{K+1} - Px^\dagger\| \le \|x_K - Px^\dagger\|$.

*Proof.* By Claim 2 each Fourier coefficient of the error is multiplied by $1 - \beta H_k$ in each step, or stays $0$. Its modulus does not grow. By Parseval, $\|v\|^2 = \frac1n \sum_k |\hat v_k|^2$, so the norm does not grow. $\square$

**Claim 4 (real symmetric PSF).** If $h_j = h_{-j}$ is real, then every $H_k$ is real, and the condition of Claim 2 is $0 < \beta H_k < 2$ for every $k$ with $H_k \ne 0$. If $H$ takes values of both signs, no $\beta > 0$ satisfies it.

*Proof.* $H_k = h_0 + \sum_{j \ge 1} h_j (e^{-2\pi i jk/n} + e^{2\pi i jk/n})$ is real. For real $t = \beta H_k$, $|1 - t| < 1$ if and only if $0 < t < 2$. A negative $H_k$ gives $1 - \beta H_k > 1$ for every $\beta > 0$. $\square$

For the box of width 5 on 16 points, $H_4 = -1/5$, and the error at frequency 4 is multiplied by $1.2$ in each step for $\beta = 1$.

**Claim 5 (the Landweber variant).** The iteration $x_{K+1} = x_K + \beta A^\ast (y - Ax_K)$, with $A^\ast$ the correlation with $h$, multiplies the error at frequency $k$ by $1 - \beta |H_k|^2$. For $0 < \beta < 2/\max_k |H_k|^2$ it converges to $Px^\dagger$ for every PSF and exact data, and its error never grows.

*Proof.* $\widehat{A^\ast v}_k = \overline{H_k}\, \hat v_k$, because the adjoint of a diagonal operator in an orthogonal basis has the conjugate diagonal. So the step is the one of Claim 2 with $\overline{H_k} H_k = |H_k|^2$ in place of $H_k$, and $0 < \beta |H_k|^2 < 2$ for every $H_k \ne 0$. Claims 2 and 3 apply. $\square$

**Noisy data.** If $y = Ax^\dagger + e$, Claim 1 gives $\hat x_{K,k} = f_k \hat x^\dagger_k + f_k \hat e_k / H_k$ for $H_k \ne 0$. Under the condition of Claim 2, $f_k \to 1$, and $x_K$ tends to $Px^\dagger + A^{+} e$, whose noise term is $\hat e_k / H_k$ and is large where $|H_k|$ is small. For $H_k = 0$ and $\hat e_k \ne 0$ the coefficient $K\beta\hat e_k$ grows without bound. So with noise the iteration must be stopped early. $\blacksquare$
