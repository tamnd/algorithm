---
title: Range-Doppler processing computes the matched filter in fast time and the DFT in slow time, puts a point target at its delay and Doppler bin with gain E_s P, and has the noise gain N0 E_s sum of w^2
proves: [correctness]
status: full
---

The notation is that of the page. $X[p][n]$ is the complex sample $n = 0, \dots, N-1$ (fast time) of pulse $p = 0, \dots, P-1$ (slow time), with $P = 2^\nu$. The pulse is $s[0], \dots, s[L-1]$ with $1 \le L \le N$, and its energy is $E_s = \sum_l |s[l]|^2 > 0$. The slow-time window is $w[0], \dots, w[P-1]$. Lines L1 to L3 compute, for $r = 0, \dots, N - L$,

$$z[p][r] = \sum_{l=0}^{L-1} \overline{s[l]}\, X[p][r + l],$$

and lines L4 to L6 compute, for every $r$, the FFT of $u[p] = w[p]\, z[p][r]$. The claim is that the output is

$$D[k][r] = \sum_{p=0}^{P-1} w[p]\, z[p][r]\, e^{-j 2\pi k p / P}, \qquad k = 0, \dots, P-1.$$

**Lemma 1 (the radix-2 FFT).** For a list $x$ of length $P = 2^\nu$, the function `fft` returns $\hat{x}[k] = \sum_{t=0}^{P-1} x[t]\, e^{-j 2\pi k t / P}$ for every $k$.

*Proof.* Let $\mathrm{rev}(i)$ be the integer whose $\nu$ bits are those of $i$ in reverse order. The first loop is the standard bit reversal permutation, so after it $a[i] = x[\mathrm{rev}(i)]$. If $s = 2^m$ divides $b$ and $0 \le u < s$, the low $m$ bits of $b + u$ are those of $u$, and they become the high bits of the reversed index, so $\mathrm{rev}(b + u) = \mathrm{rev}(b) + \mathrm{rev}_m(u)\, P/s$, with $\mathrm{rev}_m$ the reversal of $m$ bits.

We show by induction on $m$ that after the stages up to block size $s = 2^m$, every block that starts at a multiple $b$ of $s$ holds

$$a[b + k] = \sum_{t=0}^{s-1} x\!\left[\mathrm{rev}(b) + t\, \tfrac{P}{s}\right] e^{-j 2\pi k t / s}, \qquad k = 0, \dots, s - 1.$$

*Base, $s = 1$.* $a[b] = x[\mathrm{rev}(b)]$, the DFT of length 1.

*Step, $s$ to $2s$.* Let $b$ be a multiple of $2s$ and $g[t'] = x[\mathrm{rev}(b) + t' P/(2s)]$ for $t' = 0, \dots, 2s - 1$. Bit $m$ of $b + s$ is set and bit $m$ of $b$ is not, so $\mathrm{rev}(b + s) = \mathrm{rev}(b) + P/(2s)$. By the hypothesis, $a[b + k]$ is the DFT of length $s$ of $g[2t]$ and $a[b + s + k]$ is the DFT of length $s$ of $g[2t + 1]$. Call them $E[k]$ and $O[k]$. Split the DFT of length $2s$ of $g$ into the even and the odd $t'$:

$$\hat{g}[k] = E[k] + e^{-j 2\pi k/(2s)} O[k], \qquad \hat{g}[k + s] = E[k] - e^{-j 2\pi k/(2s)} O[k],$$

for $k = 0, \dots, s - 1$, because $e^{-j 2\pi (k + s)/(2s)} = -e^{-j 2\pi k/(2s)}$ and $e^{-j 2\pi (k+s) 2t/(2s)} = e^{-j 2\pi k t / s}$. The stage of size $2s$ in the code has the twiddle $\mathrm{tw}[k] = e^{-j 2\pi k/(2s)}$ and writes exactly these two values into $a[b + k]$ and $a[b + s + k]$. So the claim holds for $2s$.

At $s = P$ there is one block, $b = 0$, $\mathrm{rev}(0) = 0$, and $a[k] = \hat{x}[k]$. $\square$

**Theorem 1 (the map).** The function returns $D[k][r]$ as defined above, for $k = 0, \dots, P - 1$ and $r = 0, \dots, N - L$.

*Proof.* Lines L1 to L3 visit every pair $(p, r)$ once and form the sum of the definition of $z$. Every index $r + l$ is at most $N - L + L - 1 = N - 1$. Line L5 forms $u[p] = w[p] z[p][r]$ and line L6 applies `fft`, which by Lemma 1 returns $\sum_p u[p] e^{-j 2\pi k p/P}$ in entry $k$. The code stores entry $k$ in $D[k][r]$. $\square$

**Theorem 2 (a point target).** Let $X[p][n] = a\, e^{j 2\pi \phi p}\, s[n - r_0]$, with $s[m] = 0$ outside $0 \le m \le L-1$, a complex amplitude $a \ne 0$, a delay $0 \le r_0 \le N - L$ and the normalized Doppler $\phi = f_d / \mathrm{PRF}$. Then:

1. $|D[k][r]| \le |a|\, E_s \sum_p |w[p]|$ for all $k$ and $r$.
2. $z[p][r_0] = a\, E_s\, e^{j 2\pi \phi p}$, so the bound of part 1 is reached at $r = r_0$ if $w \ge 0$ and $\phi = k_0/P$ for an integer $k_0$, in the bin $k = k_0 \bmod P$.
3. With $w[p] = 1$ for all $p$ and $\phi = k_0/P$, $D[k][r_0] = 0$ for every $k \ne k_0 \bmod P$, and $D[k_0 \bmod P][r_0] = a\, E_s\, P$.
4. $\phi$ and $\phi + 1$ give the same input, so they give the same map.

*Proof.* $z[p][r] = a\, e^{j 2\pi \phi p} \sum_l \overline{s[l]}\, s[l + r - r_0]$. By the Cauchy-Schwarz inequality, the sum has magnitude at most $\sqrt{E_s}\sqrt{E_s} = E_s$, with the value $E_s$ at $r = r_0$. So $|z[p][r]| \le |a| E_s$ and the triangle inequality gives part 1. Part 2 is the case $r = r_0$. At $\phi = k_0/P$ and $w \ge 0$,

$$D[k][r_0] = a\, E_s \sum_p w[p]\, e^{j 2\pi (k_0 - k) p/P},$$

and for $k \equiv k_0 \pmod P$ every exponential is 1, so $|D| = |a| E_s \sum_p w[p]$. For part 3, with $w = 1$ and $k \not\equiv k_0$, the sum is a geometric series with ratio $q = e^{j 2\pi (k_0 - k)/P} \ne 1$ and $q^P = 1$, so it is $(1 - q^P)/(1 - q) = 0$. For part 4, $e^{j 2\pi (\phi + 1) p} = e^{j 2\pi \phi p}$ for every integer $p$. $\square$

**Theorem 3 (the noise gain).** Let $X[p][n]$ be independent $\mathcal{CN}(0, N_0)$ samples. Then $E\, |D[k][r]|^2 = N_0\, E_s \sum_p |w[p]|^2$ for every $k$ and $r$.

*Proof.* $z[p][r]$ is a linear combination of independent zero-mean samples with coefficients $\overline{s[l]}$, so $E|z[p][r]|^2 = N_0 \sum_l |s[l]|^2 = N_0 E_s$. Different pulses use different samples, so $z[0][r], \dots, z[P-1][r]$ are independent with zero mean. $D[k][r]$ is their combination with coefficients $w[p] e^{-j 2\pi k p/P}$, of magnitude $|w[p]|$, which gives the variance $N_0 E_s \sum_p |w[p]|^2$. $\square$

With $w = 1$, a unit-modulus pulse ($E_s = L$) and an on-bin target, Theorems 2 and 3 give the peak signal to noise ratio $|a|^2 L^2 P^2 / (N_0 L P) = L P\, |a|^2 / N_0$: the input ratio per sample times $L P$. $\blacksquare$
