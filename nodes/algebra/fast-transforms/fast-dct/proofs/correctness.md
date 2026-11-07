---
title: Makhoul's reduction computes the DCT-II, its inverse recovers the input, and the rounding error is O(u log n)
proves: [correctness, complexity, error-bound]
status: full
---

Let $n = 2^t$ with $t \ge 1$ (for $n = 1$ line L2 returns $X_0 = x_0$, which is the DCT-II of length $1$). Let $x \in \mathbb{R}^n$, let $v$ be the vector built by lines L3 to L5, so $v_r = x_{2r}$ and $v_{n-1-r} = x_{2r+1}$ for $0 \le r < n/2$, let $V_k = \sum_r v_r \omega_n^{rk}$ with $\omega_n = e^{-2\pi i/n}$, and let $d_k = e^{-\pi i k/(2n)}$. Write $X_k = \sum_j x_j \cos\frac{\pi(2j+1)k}{2n}$.

**Lemma 1 (reordering).** For $0 \le k \le n - 1$, $X_k = \sum_{r=0}^{n-1} v_r \cos\frac{\pi(4r+1)k}{2n}$.

*Proof.* Lines L3 to L5 define a bijection between the indices $j$ and $r$: the even $j = 2r$ go to $r \in \{0, \ldots, n/2 - 1\}$, and the odd $j = 2r + 1$ go to $r' = n - 1 - r \in \{n/2, \ldots, n - 1\}$. For an even $j = 2r$, $2j + 1 = 4r + 1$. For an odd $j = 2r + 1$ with $r = n - 1 - r'$, $2j + 1 = 4r + 3 = 4n - (4r' + 1)$, so $\cos\frac{\pi(2j+1)k}{2n} = \cos\left(2\pi k - \frac{\pi(4r'+1)k}{2n}\right) = \cos\frac{\pi(4r'+1)k}{2n}$, since $\cos$ is even and has period $2\pi$. Summing over the bijection gives the claim. $\square$

**Theorem 1 (forward).** FAST-DCT$(x)$ returns $X$.

*Proof.* By Theorem 1 of the [FFT proof](/fast-fourier-transform/), line L6 computes $V = F_n v$. Then $d_k V_k = \sum_r v_r e^{-\pi i k/(2n)} e^{-2\pi i rk/n} = \sum_r v_r e^{-\pi i (4r+1)k/(2n)}$. Since each $v_r$ is real, the real part is $\sum_r v_r \cos\frac{\pi(4r+1)k}{2n}$, which is $X_k$ by Lemma 1. Line L8 stores this value for each $k$. $\square$

**Lemma 2 (symmetry).** For $1 \le k \le n - 1$, $\mathrm{Im}(d_k V_k) = -X_{n-k}$, and $V_0 = X_0$.

*Proof.* Since $v$ is real, $V_{n-k} = \sum_r v_r \omega_n^{r(n-k)} = \sum_r v_r \omega_n^{-rk} = \overline{V_k}$. Also $d_{n-k} = e^{-\pi i/2} e^{\pi i k/(2n)} = -i \, \overline{d_k}$. So $d_{n-k} V_{n-k} = -i \, \overline{d_k V_k}$. For $z = a + ib$, $\mathrm{Re}(-i \bar z) = \mathrm{Re}(-ia - b) = -b$. With $z = d_k V_k$ and Theorem 1 applied at $n - k$, $X_{n-k} = \mathrm{Re}(d_{n-k} V_{n-k}) = -\mathrm{Im}(d_k V_k)$. Finally $d_0 = 1$, and $V_0 = \sum_r v_r$ is real, so $V_0 = \mathrm{Re}(d_0 V_0) = X_0$. $\square$

**Theorem 2 (inverse).** INVERSE-FAST-DCT$(X)$ returns $x$.

*Proof.* By Theorem 1 and Lemma 2, $d_k V_k = X_k - i X_{n-k}$ for $1 \le k \le n - 1$, so $V_k = \overline{d_k} (X_k - i X_{n-k}) = e^{\pi i k/(2n)} (X_k - i X_{n-k})$, using $|d_k| = 1$. Together with $V_0 = X_0$, line L10 sets $W = V$. Since $\omega_n$ is a principal $n$-th root of unity in $\mathbb{C}$ and $n$ is invertible, Theorem 2 of the FFT proof shows that line L11 returns $w = v$, which is real. Line L12 undoes the bijection of lines L3 to L5, so it returns $x$. $\square$

**Lemma 3 (row orthogonality).** Let $C_{kj} = \cos\frac{\pi(2j+1)k}{2n}$. Then $C C^{\mathsf T} = D = \mathrm{diag}(n, \frac{n}{2}, \ldots, \frac{n}{2})$, and $\lVert C y \rVert_2 \ge \sqrt{n/2} \, \lVert y \rVert_2$ for every $y \in \mathbb{R}^n$.

*Proof.* First, for an integer $m$ with $0 < |m| < 2n$, $S(m) = \sum_{j=0}^{n-1} \cos\frac{\pi(2j+1)m}{2n} = 0$. Put $\theta = \pi m/n$, so $e^{i\theta} \ne 1$. Then $S(m) = \mathrm{Re}\left(e^{i\theta/2} \sum_j e^{ij\theta}\right) = \mathrm{Re}\left(e^{i\theta/2} \frac{e^{in\theta} - 1}{e^{i\theta} - 1}\right)$. If $m$ is even, $e^{in\theta} = e^{i\pi m} = 1$ and $S(m) = 0$. If $m$ is odd, $e^{in\theta} = -1$ and $e^{i\theta} - 1 = 2i \sin(\theta/2) e^{i\theta/2}$ with $\sin(\theta/2) \ne 0$, so $S(m) = \mathrm{Re}\left(\frac{-2}{2i \sin(\theta/2)}\right) = \mathrm{Re}\left(\frac{i}{\sin(\theta/2)}\right) = 0$. Now by $\cos a \cos b = \frac{1}{2}(\cos(a - b) + \cos(a + b))$, $(C C^{\mathsf T})_{kl} = \frac{1}{2}(S(k - l) + S(k + l))$, with $S(0) = n$. For $k = l = 0$ this is $n$. For $k = l \ge 1$ it is $\frac{1}{2}(n + S(2k)) = \frac{n}{2}$, since $0 < 2k < 2n$. For $k \ne l$, both $k - l$ and $k + l$ are nonzero and less than $2n$ in absolute value, so the entry is $0$. Hence $Q = D^{-1/2} C$ satisfies $Q Q^{\mathsf T} = I$, so $Q$ is orthogonal, and $\lVert C y \rVert_2 = \lVert D^{1/2} Q y \rVert_2 \ge \sqrt{n/2} \, \lVert Q y \rVert_2 = \sqrt{n/2} \, \lVert y \rVert_2$. $\square$

**Theorem 3 (rounding error).** Work in floating point with unit roundoff $u$ and $\gamma_m = mu/(1 - mu)$. Suppose the computed FFT satisfies $\lVert \hat V - V \rVert_2 \le \delta \lVert V \rVert_2$ (Higham, Theorem 24.2, gives such a $\delta = O(u \log n)$ when the twiddle factors are accurate), each computed rotation is $\hat d_k = d_k(1 + \theta_k)$ with $|\theta_k| \le \mu$, and line L8 evaluates $\hat c_k \mathrm{Re} \hat V_k + \hat s_k \mathrm{Im} \hat V_k$ in floating point, with $\hat d_k = \hat c_k - i \hat s_k$. Then

$$\frac{\lVert \hat X - X \rVert_2}{\lVert X \rVert_2} \le \sqrt 2 \, (\delta + \mu + \sqrt 2 \gamma_2) + O(u^2)$$

for $x \ne 0$.

*Proof.* Lines L3 to L5 copy entries, so $v$ is exact and $\lVert v \rVert_2 = \lVert x \rVert_2$. By Parseval for the unnormalized DFT, $\lVert V \rVert_2 = \sqrt n \lVert v \rVert_2 = \sqrt n \lVert x \rVert_2$. The floating-point dot product of length $2$ gives $\hat X_k = \mathrm{Re}(\hat d_k \hat V_k) + e_k$ with $|e_k| \le \gamma_2 (|\hat c_k \mathrm{Re} \hat V_k| + |\hat s_k \mathrm{Im} \hat V_k|) \le \sqrt 2 \gamma_2 |\hat d_k| |\hat V_k|$, by the Cauchy-Schwarz inequality. Hence

$$|\hat X_k - X_k| \le |\hat d_k \hat V_k - d_k V_k| + |e_k| \le |\hat V_k - V_k| + \mu |\hat V_k| + \sqrt 2 \gamma_2 (1 + \mu) |\hat V_k|,$$

using $X_k = \mathrm{Re}(d_k V_k)$, $|d_k| = 1$ and $\hat d_k \hat V_k - d_k V_k = d_k(\hat V_k - V_k) + d_k \theta_k \hat V_k$. Taking 2-norms over $k$ and using $\lVert \hat V \rVert_2 \le (1 + \delta) \lVert V \rVert_2$,

$$\lVert \hat X - X \rVert_2 \le \left(\delta + (\mu + \sqrt 2 \gamma_2)(1 + \delta) + \sqrt 2 \gamma_2 \mu (1 + \delta)\right) \sqrt n \, \lVert x \rVert_2 = (\delta + \mu + \sqrt 2 \gamma_2) \sqrt n \, \lVert x \rVert_2 + O(u^2).$$

By Lemma 3, $\lVert X \rVert_2 = \lVert C x \rVert_2 \ge \sqrt{n/2} \, \lVert x \rVert_2$. Dividing gives the bound. $\square$

**Operation count.** Lines L3 to L5 and L12 only move data. Line L6 is one complex FFT of length $n$: $\frac{n}{2} \lg n$ complex multiplications and $n \lg n$ complex additions, which is $2 n \lg n$ real multiplications and $3 n \lg n$ real additions with the usual $4$ multiplications and $2$ additions per complex product. Lines L7 and L8 use at most $2n$ real multiplications and $n$ real additions, plus the $n$ rotation factors, which can be precomputed once per length. So FAST-DCT uses $5 n \lg n + 3n$ real operations, and $\Theta(n \log n)$ in total. Line L10 uses $O(n)$ operations and line L11 one inverse FFT of length $n$, so the inverse has the same order of cost. $\blacksquare$
