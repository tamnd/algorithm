---
title: The radix-2 fast Hartley transform computes the DHT, is its own inverse up to 1/n, and has a first-order error bound linear in lg n
proves: [correctness, complexity, error-bound]
status: full
---

Let $n = 2^t$, let $x \in \mathbb{R}^n$ be the input and $x'$ the array as the algorithm changes it. For a vector $y$ of length $N$, write $\mathrm{DHT}_N(y)_k = \sum_{m} y_m \, \mathrm{cas}(2\pi mk/N)$, with indices of $\mathrm{DHT}_N(y)$ taken modulo $N$. As in the proof for the [FFT](/fast-fourier-transform/), for $h = 2^q$ and $h \mid s$ let $c(s, h) = \mathrm{rev}_{t-q}(s/h)$ and let $x^{(s,h)}$ be the subsequence $x^{(s,h)}_m = x_{c(s,h) + m n/h}$, $0 \le m < h$.

**Lemma 1 (cas of a sum).** $\mathrm{cas}(a + b) = \cos b \, \mathrm{cas}\,a + \sin b \, \mathrm{cas}(-a)$.

*Proof.* $\cos(a + b) + \sin(a + b) = \cos a \cos b - \sin a \sin b + \sin a \cos b + \cos a \sin b = \cos b (\cos a + \sin a) + \sin b (\cos a - \sin a)$, and $\cos a - \sin a = \mathrm{cas}(-a)$. $\square$

**Lemma 2 (merge).** Let $N = 2h$, $y \in \mathbb{R}^N$, and let $E$ and $O$ be the DHTs of length $h$ of $(y_0, y_2, \ldots)$ and $(y_1, y_3, \ldots)$. Put $\theta_k = 2\pi k/N$. Then for $0 \le k < h$,

$$\mathrm{DHT}_N(y)_k = E_k + \cos\theta_k \, O_k + \sin\theta_k \, O_{h-k}, \qquad \mathrm{DHT}_N(y)_{k+h} = E_k - \cos\theta_k \, O_k - \sin\theta_k \, O_{h-k},$$

with $O_{h-0} = O_0$.

*Proof.* Split the sum by the parity of the index. For any integer $k'$, the even part is $\sum_m y_{2m} \, \mathrm{cas}(2\pi m k'/h) = E_{k'}$, and the odd part is $\sum_m y_{2m+1} \, \mathrm{cas}(2\pi m k'/h + \theta_{k'})$, which by Lemma 1 equals $\cos\theta_{k'} \, O_{k'} + \sin\theta_{k'} \sum_m y_{2m+1} \, \mathrm{cas}(-2\pi m k'/h) = \cos\theta_{k'} \, O_{k'} + \sin\theta_{k'} \, O_{-k'}$. For $k' = k$ this is the first formula. For $k' = k + h$, $E$ and $O$ have period $h$, and $\theta_{k+h} = \theta_k + \pi$ flips the signs of $\cos$ and $\sin$, which gives the second formula. $\square$

**Lemma 3 (the four-point butterfly).** For $1 \le k < h/2$, lines L10 to L13 store the four values of Lemma 2 for the indices $k$, $k + h$, $h - k$ and $2h - k$ of a block, and lines L6 and L7 store those for $k = 0$, $h$, $h/2$ and $3h/2$.

*Proof.* In line L9, $c = \cos\theta_k$ and $\sigma = \sin\theta_k$ with $\theta_k = \pi k/h$. Line L10 reads $a = O_k$ and $b = O_{h-k}$ and sets $t_1 = \cos\theta_k O_k + \sin\theta_k O_{h-k}$. Since $\theta_{h-k} = \pi - \theta_k$, $\cos\theta_{h-k} = -c$ and $\sin\theta_{h-k} = \sigma$, so the odd term of Lemma 2 for the index $h - k$ is $-c \, O_{h-k} + \sigma \, O_k = t_2$. Line L11 saves $E_k$ and $E_{h-k}$, and lines L12 and L13 store $E_k \pm t_1$ and $E_{h-k} \pm t_2$ at the places $k$, $k + h$, $h - k$, $2h - k$, which are the values of Lemma 2. The four cells read are the four cells written, and the sets $\{k, h - k\}$ for $1 \le k < h/2$ are disjoint from each other and from $\{0, h/2\}$, so no value is overwritten before it is read. For $k = 0$, $\theta_0 = 0$ and $O_{h} = O_0$, giving $E_0 \pm O_0$ (line L6); for $k = h/2$, $\theta = \pi/2$ and $O_{h - h/2} = O_{h/2}$, giving $E_{h/2} \pm O_{h/2}$ (line L7). For $h = 1$ only $k = 0$ occurs, and for $h = 2$ only $k = 0$ and $k = 1 = h/2$. $\square$

**Theorem 1 (forward).** FHT$(x)$ replaces $x$ by $\mathrm{DHT}_n(x)$.

*Proof.* The invariant is: when line L4 tests $h = 2^q$, for every block start $s$ with $h \mid s$, $x'[s \ldots s + h - 1] = \mathrm{DHT}_h(x^{(s,h)})$. After line L2, $x'[j] = x_{\mathrm{rev}_t(j)} = x^{(j,1)}_0$, and a DHT of length $1$ is the identity, so the invariant holds for $h = 1$. If it holds for $h < n$, take a block start $s$ with $2h \mid s$. By Lemma 2 of the FFT proof (which concerns only the indices), $x^{(s,h)}$ and $x^{(s+h,h)}$ are the even and the odd entries of $x^{(s,2h)}$, so the two halves of the block hold $E$ and $O$ for $y = x^{(s,2h)}$. By Lemma 3, one pass of lines L6 to L13 writes $\mathrm{DHT}_{2h}(y)$ into the block, and different blocks are disjoint. After line L14 the invariant holds for $2h$. When $h = n$, the only block is $s = 0$ with $x^{(0,n)} = x$. $\square$

**Theorem 2 (inverse).** $\mathcal H_n^2 = n I$, so INVERSE-FHT$(\mathrm{DHT}_n(x)) = x$.

*Proof.* $(\mathcal H_n^2)_{jl} = \sum_k \mathrm{cas}\,\alpha_k \, \mathrm{cas}\,\beta_k$ with $\alpha_k = 2\pi jk/n$ and $\beta_k = 2\pi lk/n$. Expanding, $\mathrm{cas}\,a \, \mathrm{cas}\,b = \cos a \cos b + \sin a \sin b + \sin a \cos b + \cos a \sin b = \cos(a - b) + \sin(a + b)$. Now $\sum_k \cos(2\pi(j - l)k/n) + i \sum_k \sin(2\pi(j - l)k/n) = \sum_k e^{2\pi i (j-l)k/n}$, which is $n$ if $j \equiv l$ and $0$ otherwise, by the [summation lemma](/fft-summation-lemma/); so $\sum_k \cos(\alpha_k - \beta_k) = n [j = l]$. Similarly $\sum_k \sin(2\pi(j + l)k/n)$ is the imaginary part of a sum that is real ($n$ or $0$), so it is $0$. Hence $\mathcal H_n^2 = n I$. By Theorem 1, line L15 computes $\mathcal H_n \mathcal H_n x = n x$, and line L16 divides by $n$. $\square$

**Operation count.** For $h = 1$, each of the $n/2$ blocks does line L6 only: $2$ additions. For $h \ge 2$, each of the $n/(2h)$ blocks does lines L6 and L7 ($4$ additions) and $h/2 - 1$ butterflies of lines L10 to L13, each with $4$ multiplications and $2 + 4 = 6$ additions. So the pass for $h \ge 2$ costs $\frac{n}{2h}(2h - 4) = n - \frac{2n}{h}$ multiplications and $\frac{n}{2h}(3h - 2) = \frac{3n}{2} - \frac{n}{h}$ additions. Summing over $h = 2^q$, $1 \le q \le t - 1$, with $\sum_{q=1}^{t-1} 2^{-q} = 1 - 2^{1-t}$, the total for $n \ge 2$ is

$$n(t - 1) - 2n(1 - 2^{1-t}) = n \lg n - 3n + 4 \text{ multiplications}, \qquad n + \tfrac{3n}{2}(t - 1) - n(1 - 2^{1-t}) = \tfrac{3}{2} n \lg n - \tfrac{3}{2} n + 2 \text{ additions}.$$

**Theorem 3 (rounding error).** Suppose the computed pair $(\hat c, \hat \sigma)$ in line L9 satisfies $\sqrt{(\hat c - c)^2 + (\hat\sigma - \sigma)^2} \le \mu$, and let $u$ be the unit roundoff and $\gamma_2 = 2u/(1 - 2u)$. Then the computed $\hat H$ satisfies $\lVert \hat H - H \rVert_2 \le \lg n \, \eta \, \lVert H \rVert_2 + O(u^2)$, with $\eta = u + \sqrt 2 (\mu + \gamma_2)$.

*Proof.* Write the pass for $h$ as a matrix $S_q$ ($h = 2^{q-1}$) acting on the whole array. On a block it maps $(E, O)$ to $(E + R O, E - R O)$, where $R$ fixes $O_0$ and $O_{h/2}$ and maps each pair $(O_k, O_{h-k})$, $1 \le k < h/2$, by the matrix with rows $(c, \sigma)$ and $(\sigma, -c)$, a reflection. So $R$ is orthogonal, and $S_q^{\mathsf T} S_q = 2I$ block by block: $S_q = \sqrt 2 \, Q_q$ with $Q_q$ orthogonal.

*Local error of one pass.* Let $z$ be the computed array before the pass. For a butterfly with $a = O_k$, $b = O_{h-k}$, the computed $\hat t_1 = \mathrm{fl}(\hat c a + \hat\sigma b)$ satisfies $|\hat t_1 - t_1| \le |(\hat c - c) a + (\hat \sigma - \sigma) b| + \gamma_2 (|\hat c a| + |\hat \sigma b|) \le (\mu + \gamma_2) \sqrt{a^2 + b^2} + O(u^2)$ by the Cauchy-Schwarz inequality, and the same holds for $\hat t_2$. So the errors $\tau$ of all the $t$ values of a block satisfy $\sum \tau^2 \le 2 (\mu + \gamma_2)^2 \lVert O \rVert_2^2 + O(u^3)$. Each $\tau$ enters two outputs, $e \pm \hat t$, and each output addition adds a relative error at most $u$. Hence the error of the pass is $e_q$ with

$$\lVert e_q \rVert_2 \le 2 (\mu + \gamma_2) \lVert z \rVert_2 + u \lVert S_q z \rVert_2 + O(u^2) = \eta \, \lVert S_q z \rVert_2 + O(u^2),$$

using $\lVert S_q z \rVert_2 = \sqrt 2 \lVert z \rVert_2$. Lines L6 and L7 contribute only the term with $u$.

*Accumulation.* Line L2 is exact. With $z_0$ the permuted input and $z_q = S_q z_{q-1} + e_q$, linearity gives $z_t = S_t \cdots S_1 z_0 + \sum_{q=1}^{t} S_t \cdots S_{q+1} e_q$. Since $\lVert S_t \cdots S_{q+1} w \rVert_2 = 2^{(t-q)/2} \lVert w \rVert_2$ and $\lVert S_q z_{q-1} \rVert_2 = 2^{q/2} \lVert x \rVert_2 (1 + O(u))$, each term has norm at most $\eta \, 2^{t/2} \lVert x \rVert_2 + O(u^2) = \eta \lVert H \rVert_2 + O(u^2)$, because $\lVert H \rVert_2 = \sqrt n \lVert x \rVert_2$ by Theorem 2. Summing $t = \lg n$ terms gives the bound. $\blacksquare$
