---
title: The iterative radix-2 FFT computes the DFT, and INVERSE-FFT inverts it
proves: [correctness, complexity]
status: full
---

Let $R$ be a commutative ring, $n = 2^t$ with $t \ge 0$, and $\omega \in R$ with $\omega^{n/2} = -1$ if $n \ge 2$. Then $\omega^n = 1$. Write $x$ for the input array and $x'$ for the array as the algorithm changes it. For $h = 2^q$ with $0 \le q \le t$ and a block start $s$ with $h \mid s$, let $c(s, h) = \mathrm{rev}_{t-q}(s/h)$, so $0 \le c(s,h) < n/h$, and define the subsequence $x^{(s,h)} \in R^h$ by $x^{(s,h)}_m = x_{c(s,h) + m n/h}$ for $0 \le m < h$.

**Lemma 1 (split).** Let $N = 2M \ge 2$ and $\zeta \in R$ with $\zeta^M = -1$. For $y \in R^N$, let $E$ and $O$ be the DFTs of length $M$ with the root $\zeta^2$ of $(y_0, y_2, \ldots, y_{N-2})$ and $(y_1, y_3, \ldots, y_{N-1})$. Then for $0 \le k < M$,

$$\sum_{m=0}^{N-1} y_m \zeta^{mk} = E_k + \zeta^k O_k, \qquad \sum_{m=0}^{N-1} y_m \zeta^{m(k+M)} = E_k - \zeta^k O_k.$$

*Proof.* Split the sum by the parity of $m = 2m'$ or $m = 2m' + 1$: $\sum_m y_m \zeta^{mk'} = \sum_{m'} y_{2m'} (\zeta^2)^{m'k'} + \zeta^{k'} \sum_{m'} y_{2m'+1} (\zeta^2)^{m'k'}$ for each $k'$. For $k' = k$ this is $E_k + \zeta^k O_k$. For $k' = k + M$, $(\zeta^2)^{m'(k+M)} = (\zeta^2)^{m'k} (\zeta^{2M})^{m'} = (\zeta^2)^{m'k}$ because $\zeta^{2M} = 1$, and $\zeta^{k+M} = -\zeta^k$. $\square$

**Lemma 2 (indices).** Let $h = 2^q$ with $q < t$ and $2h \mid s$. Then $c(s, h) = c(s, 2h)$ and $c(s + h, h) = c(s, 2h) + n/(2h)$. Hence $x^{(s,h)}$ and $x^{(s+h,h)}$ are the even-indexed and the odd-indexed entries of $x^{(s,2h)}$.

*Proof.* Let $s/(2h) = a$. Then $s/h = 2a$ and $(s + h)/h = 2a + 1$, written with $t - q$ binary digits. Reversing $t - q$ digits moves the lowest digit to the top place $2^{t-q-1} = n/(2h)$ and reverses the other $t - q - 1$ digits, so $\mathrm{rev}_{t-q}(2a + b) = b \cdot n/(2h) + \mathrm{rev}_{t-q-1}(a)$ for $b \in \{0, 1\}$, and $\mathrm{rev}_{t-q-1}(a) = c(s, 2h)$. So $x^{(s,h)}_{m} = x_{c(s,2h) + 2m \cdot n/(2h)} = x^{(s,2h)}_{2m}$ and $x^{(s+h,h)}_{m} = x_{c(s,2h) + (2m+1) n/(2h)} = x^{(s,2h)}_{2m+1}$. $\square$

**Invariant (I).** When line L6 tests $h = 2^q$, for each $s$ with $h \mid s$ and $0 \le k < h$,

$$x'[s + k] = \sum_{m=0}^{h-1} x^{(s,h)}_m \, \left(\omega^{n/h}\right)^{mk}.$$

*Initialization.* Lines L3 and L4 swap each pair $\{j, \mathrm{rev}_t(j)\}$ with $j < \mathrm{rev}_t(j)$ exactly once and leave the fixed points alone. Since $\mathrm{rev}_t$ is an involution, the pairs are disjoint, and afterwards $x'[j] = x_{\mathrm{rev}_t(j)}$ for each $j$. Line L5 sets $h = 1$, and (I) for $h = 1$ says $x'[s] = x^{(s,1)}_0 = x_{\mathrm{rev}_t(s)}$, which holds.

*Maintenance.* Let (I) hold for $h < n$, and fix a block start $s$ with $2h \mid s$. Put $\zeta = \omega^{n/(2h)}$ and $M = h$. Then $\zeta^{M} = \omega^{n/2} = -1$ and $\zeta^2 = \omega^{n/h}$. By (I) and Lemma 2, before the loop of line L8 the cells $x'[s \ldots s + h - 1]$ hold $E$ and the cells $x'[s + h \ldots s + 2h - 1]$ hold $O$, the DFTs with the root $\zeta^2$ of the even and odd entries of $y = x^{(s,2h)}$. For each $k < h$, lines L9 to L12 read only the cells $s + k$ and $s + k + h$, and write only those two cells, so the iterations for different $k$ do not interfere, and blocks for different $s$ are disjoint. The table entry is $W[k \cdot n/(2h)] = \omega^{k n/(2h)} = \zeta^k$ by line L2, and $k \cdot n/(2h) < n/2$, so it is in the table. Line L9 saves $u = E_k$ before line L11 overwrites it, line L10 computes $v = \zeta^k O_k$, and lines L11 and L12 store $E_k + \zeta^k O_k$ and $E_k - \zeta^k O_k$. By Lemma 1 with $N = 2h$, these are the entries $k$ and $k + h$ of the DFT of $x^{(s,2h)}$ with the root $\zeta = \omega^{n/(2h)}$. After line L13 doubles $h$, (I) holds for the new $h$.

*Termination.* The loop ends when $h = n$. Then the only block start is $s = 0$, $c(0, n) = \mathrm{rev}_0(0) = 0$, and $x^{(0,n)} = x$. So by (I), $x'[k] = \sum_m x_m \omega^{mk} = X_k$ for each $k$.

**Theorem 1.** If $n = 2^t$ and $\omega^{n/2} = -1$ (no condition when $n = 1$), FFT$(x, \omega)$ replaces $x$ by $F_n x$, with $(F_n x)_k = \sum_{j} x_j \omega^{jk}$. This holds in particular when $\omega$ is a principal $n$-th root of unity and $n$ is a unit, because then $\omega^{n/2} = -1$ by the [cancellation lemma](/fft-cancellation-lemma/), and for $\omega = e^{\mp 2\pi i/n}$ over $\mathbb{C}$.

*Proof.* The invariant and the termination step above. $\square$

**Theorem 2.** If $\omega$ is a principal $n$-th root of unity and $n$ is a unit of $R$, then INVERSE-FFT$(F_n x, \omega)$ returns $x$.

*Proof.* The element $\omega^{-1} = \omega^{n-1}$ is a principal $n$-th root: $(\omega^{-1})^n = 1$, and for $1 \le k \le n - 1$, $\sum_j \omega^{-jk} = \sum_j \omega^{j(n-k)} = 0$ since $1 \le n - k \le n - 1$. So by Theorem 1, line L14 computes $Y_j = \sum_k X_k \omega^{-jk} = \sum_{l} x_l \sum_k \omega^{(l - j)k}$. By the [summation lemma](/fft-summation-lemma/) in the form of the definition of a principal root, the inner sum is $n$ if $l = j$ and $0$ otherwise, for $0 \le l, j \le n - 1$. So $Y_j = n x_j$, and line L15 returns $x_j$. $\blacksquare$

**Operation count.** Each pass of the loop of line L6 runs $n/(2h)$ blocks of $h$ butterflies, and each butterfly does one multiplication (line L10) and two additions (lines L11 and L12). There are $t$ passes, with $h = 1, 2, \ldots, n/2$. So the butterflies use exactly $\frac{n}{2} t = \frac{n}{2} \lg n$ multiplications and $n \lg n$ additions in $R$. Line L2 needs at most $\max(n/2 - 2, 0)$ multiplications if each power is the previous one times $\omega$, and line L15 needs $n$ more for the inverse.
