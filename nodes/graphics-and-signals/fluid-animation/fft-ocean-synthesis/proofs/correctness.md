---
title: The FFT, the real height and the statistics of FFT ocean synthesis
proves: [correctness]
status: full
---

We use the notation of the page, with exact arithmetic.
The grid indices are $0 \le n, m < N$ with $N$ a power of 2, and the signed index is $n' = n$ for $n < N/2$ and $n' = n - N$ otherwise, so $n' \equiv n \pmod N$.
The wave vector of $(n, m)$ is $k_{nm} = (2\pi n'/L, 2\pi m'/L)$, and $-k$ means the index $((-n) \bmod N, (-m) \bmod N)$.
For every index pair except the Nyquist row and column ($n = N/2$ or $m = N/2$), $k_{-n,-m} = -k_{nm}$.
On the Nyquist row and column the code sets $h_0 = 0$, so $H = 0$ there by line L3.
The grid points are $x_{ab} = (aL/N, bL/N)$.

## The FFT

**Claim 1.** For $N$ a power of 2, `fft(a)` returns $A_q = \sum_{j<N} a_j \omega_N^{jq}$ with $\omega_N = e^{-2\pi i/N}$, and with $\omega_N = e^{+2\pi i/N}$ for the inverse.

*Proof.*
For $N = 1$ the code returns $a$.
For $N > 1$, split the sum into the even and odd $j$: $A_q = E_q + \omega_N^q O_q$ and $A_{q + N/2} = E_q - \omega_N^q O_q$ for $q < N/2$, where $E$ and $O$ are the DFTs of length $N/2$ of the even and odd entries, because $\omega_N^2 = \omega_{N/2}$ and $\omega_N^{N/2} = -1$.
The bit reversal puts the even entries in the first half and the odd entries in the second half, each half again in bit reversed order.
By induction on the length, after the passes with block sizes up to $N/2$, the two halves hold $E$ and $O$.
The last pass, with block size $N$, computes $E_q \pm w O_q$ with $w = \omega_N^q$ for $q = 0, \dots, N/2 - 1$, which is the split above. $\square$

The 2D transform of the code applies Claim 1 to each row and then to each column, which is the 2D DFT $\sum_{n, m} G_{nm}\, \omega_N^{\pm(na + mb)}$ because the 2D kernel is the product of two 1D kernels.

## The height is real

**Claim 2.** $H(-k, t) = \overline{H(k, t)}$ for every index and every $t$.

*Proof.*
$\omega$ depends on $|k|$ only, and $|k_{-n,-m}| = |k_{nm}|$ on every index.
So $H(-k, t) = h_0(-k) e^{i\omega t} + \overline{h_0(k)}\, e^{-i\omega t}$, and $\overline{H(k, t)} = \overline{h_0(k)}\, e^{-i\omega t} + h_0(-k) e^{i\omega t}$. These are equal. $\square$

**Claim 3.** At the grid points, the inverse 2D DFT of line L4 equals $h(x_{ab}, t) = \sum_k H(k, t) e^{i k\cdot x_{ab}}$, and this value is real.

*Proof.*
$e^{i k_{nm}\cdot x_{ab}} = e^{2\pi i (n'a + m'b)/N} = e^{2\pi i (na + mb)/N}$ because $n' \equiv n$ and $m' \equiv m \pmod N$, so the sum is the inverse DFT of Claim 1 with no factor.
For its conjugate, $\overline{h} = \sum_{n, m} \overline{H_{nm}}\, e^{-2\pi i(na + mb)/N}$.
Put $n \to (-n) \bmod N$ and $m \to (-m) \bmod N$, a bijection of the indices: by Claim 2 the term becomes $H_{nm} e^{2\pi i(na + mb)/N}$, so $\overline h = h$. $\square$

**Claim 4.** The displacement of line L5 is real.

*Proof.*
Let $S(k) = -i\lambda (k/|k|) H(k)$ for $k \ne 0$ and $S(0) = 0$.
Off the Nyquist row and column, $k_{-n,-m} = -k_{nm}$, so $S(-k) = i\lambda (k/|k|)\overline{H(k)} = \overline{S(k)}$ by Claim 2.
On the Nyquist row and column, $H = 0$, so $S = 0$ at both $k$ and $-k$.
So $S$ has the symmetry of Claim 2 in each component, and the argument of Claim 3 makes its inverse DFT real. $\square$

## One wave

**Claim 5.** If $h_0$ is 0 except at one index $k$ off the Nyquist row and column with $k \ne 0$, then $h(x, t) = 2\operatorname{Re}(h_0(k) e^{i(k\cdot x + \omega t)})$, a cosine wave that runs in the direction $-\hat k$ at the speed $\omega/|k| = (g/|k|)^{1/2}$.

*Proof.*
Only $H(k) = h_0(k) e^{i\omega t}$ and $H(-k) = \overline{h_0(k)}\, e^{-i\omega t}$ are not 0.
With $k_{-n,-m} = -k$, the sum is $h_0(k) e^{i(k\cdot x + \omega t)} + \overline{h_0(k) e^{i(k\cdot x + \omega t)}}$, which is twice the real part.
The phase $k\cdot x + \omega t$ is constant on points that move with the velocity $-(\omega/|k|)\hat k$. $\square$

In the same way, each $h_0(k)$ gives a wave in the direction $-\hat k$, and each $\overline{h_0(-k)}$ term gives one in the direction $\hat k$.

## Statistics

**Claim 6.** The mean of $h$ over the grid points is 0, and for every grid point and every $t$, $E[h(x, t)] = 0$ and $E[h(x, t)^2] = \sum_k 2P(k)$, summed over the indices off the Nyquist row and column.

*Proof.*
$P(0) = 0$, so $h_0(0) = 0$ and $H(0) = 0$; the mean over the grid is $N^{-2}\sum_{a, b} h = H(0) = 0$, since $\sum_{a} e^{2\pi i na/N} = 0$ for $n \ne 0$.
The values $h_0(k)$ are independent for different indices, with $E[h_0] = 0$, $E[|h_0|^2] = \frac{P}{2}E[\xi_r^2 + \xi_i^2] = P$ and $E[h_0^2] = \frac P2 E[\xi_r^2 - \xi_i^2 + 2i\xi_r\xi_i] = 0$.
So $E[h] = 0$.
Since $h$ is real, $h^2 = h\overline h = \sum_{k, k'} H(k)\overline{H(k')}\, e^{i(k - k')\cdot x}$.
If $k' \ne \pm k$, $H(k)$ and $H(k')$ depend on disjoint sets of independent values with mean 0, so $E[H(k)\overline{H(k')}] = 0$.
If $k' = k \ne 0$, $E|H(k)|^2 = E|h_0(k)|^2 + E|h_0(-k)|^2 + 2\operatorname{Re}(E[h_0(k) h_0(-k)] e^{2i\omega t}) = P(k) + P(-k) = 2P(k)$, because $h_0(k)$ and $h_0(-k)$ are independent with mean 0 and $P$ is even.
If $k' = -k \ne k$, then $\overline{H(-k)} = H(k)$ and $E[H(k)^2] = E[h_0(k)^2] e^{2i\omega t} + 2E[h_0(k)\overline{h_0(-k)}] + E[\overline{h_0(-k)}^2] e^{-2i\omega t} = 0$.
So only the terms $k' = k$ remain, and they give $\sum_k 2P(k)$, with no dependence on $x$ or $t$. $\square$

## The peak of the spectrum

**Claim 7.** Along the wind ($\hat k = \hat w$), $P$ is largest at $|k| = 1/(\sqrt 2\,\ell)$.

*Proof.*
With $\kappa = |k|$, $\ln P = \ln A - 1/(\kappa\ell)^2 - 4\ln\kappa$, whose derivative $2/(\kappa^3\ell^2) - 4/\kappa$ is positive for $\kappa^2 < 1/(2\ell^2)$ and negative after. $\blacksquare$
