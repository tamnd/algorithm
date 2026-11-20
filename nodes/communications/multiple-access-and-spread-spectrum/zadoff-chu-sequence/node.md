---
tag: MHXFB8
kind: definition
slug: zadoff-chu-sequence
name: Zadoff-Chu sequence
aliases:
- ZC sequence
- CAZAC sequence
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "A complex sequence of constant amplitude whose periodic autocorrelation is zero at every nonzero shift. Used for preambles, random access and synchronization."
model: real-ram
prereqs: [autocorrelation, cross-correlation, discrete-fourier-transform]
see_also: [frank-code, welch-bound, maximal-length-sequence, preamble-correlation-detection, frequency-offset-estimation, sc-fdma, orthogonal-frequency-division-multiplexing, barker-code]
sources:
  - paper: doi:10.1109/TIT.1972.1054840
    title: David C. Chu, Polyphase codes with good periodic correlation properties, IEEE Transactions on Information Theory 18(4), 1972
    locator: pp. 531 to 532 (the construction for every length N and the proof of zero periodic autocorrelation)
  - paper: doi:10.1109/TIT.1962.1057786
    title: R. L. Frank and S. A. Zadoff, Phase shift pulse codes with good periodic correlation properties, IRE Transactions on Information Theory 8(6), 1962
    locator: pp. 381 to 382 (the related codes of length N squared, now called Frank codes)
  - paper: doi:10.1109/TIT.1974.1055219
    title: Lloyd R. Welch, Lower bounds on the maximum cross correlation of signals, IEEE Transactions on Information Theory 20(3), 1974
    locator: pp. 397 to 399 (the bound that a set of Zadoff-Chu sequences of prime length nearly meets)
---

A Zadoff-Chu sequence is a complex sequence of length $N$ whose elements all have magnitude $1$ and whose phases grow as a quadratic in the index. Its periodic [autocorrelation](/autocorrelation/) is $N$ at shift $0$ and exactly $0$ at every other shift, for every length $N$ and every root $u$ coprime to $N$. Its [discrete Fourier transform](/discrete-fourier-transform/) also has constant magnitude, so the sequence is flat in both time and frequency. For prime $N$, two sequences with different roots have a periodic cross-correlation of constant magnitude $\sqrt N$ at every shift. The family is named after Zadoff, who with Frank described the square-length case in 1962 (now the [Frank code](/frank-code/)), and Chu, who gave the construction for every length in 1972.

## Definition

Let $N \ge 1$ and let $u$ be an integer with $\gcd(u, N) = 1$, the **root**. Let $c = N \bmod 2$. The Zadoff-Chu sequence of root $u$ and length $N$ is

$$x_u[n] = \exp\!\left(-\frac{j \pi u \, n (n + c)}{N}\right), \qquad n = 0, 1, \ldots, N - 1.$$

So $x_u[n] = e^{-j\pi u n(n+1)/N}$ for odd $N$ and $x_u[n] = e^{-j\pi u n^2/N}$ for even $N$. The term $c$ makes the formula periodic with period $N$: $x_u[n + N] = x_u[n]$ for every integer $n$, so cyclic shifts are well defined. For odd $N$, the number $n(n+1)/2$ is an integer, and $x_u[n] = e^{-j 2\pi m_n / N}$ with $m_n = u \, n(n+1)/2 \bmod N$; every element is an $N$-th root of unity.

The periodic correlation of two sequences $x$ and $y$ of length $N$ at shift $t$ is

$$C_{x,y}(t) = \sum_{n=0}^{N-1} x[n] \, \overline{y[(n + t) \bmod N]}.$$

**Zero autocorrelation.** Take odd $N$. The exponents give $n(n+1) - (n+t)(n+t+1) = -2nt - t(t+1)$, so

$$C_{x_u,x_u}(t) = e^{j\pi u t(t+1)/N} \sum_{n=0}^{N-1} e^{j 2\pi u t n / N}.$$

The sum is over all $N$-th roots of unity of the form $e^{j2\pi (ut) n/N}$. It is $N$ if $ut \equiv 0 \pmod N$ and $0$ otherwise. Since $\gcd(u, N) = 1$, this is $0$ for every $t \not\equiv 0$. The even case is the same with $n^2 - (n+t)^2 = -2nt - t^2$.

**Cross-correlation for prime $N$.** For two roots $u_1 \ne u_2$, the phase of the term $n$ in $C_{x_{u_1}, x_{u_2}}(t)$ is a quadratic in $n$ with leading coefficient proportional to $u_1 - u_2$. It is a quadratic Gauss sum, and its magnitude is $\sqrt N$ whenever $\gcd(u_1 - u_2, N) = 1$. For prime $N$ this holds for all distinct roots, so the $N - 1$ sequences of one prime length form a family with largest cross-correlation $\sqrt N$. The magnitude follows from the classical evaluation of quadratic Gauss sums.

**Flat spectrum.** The DFT $X_u[k] = \sum_n x_u[n] e^{-j2\pi kn/N}$ satisfies $|X_u[k]| = \sqrt N$ for every $k$. This follows from the zero autocorrelation: $|X_u[k]|^2$ is the DFT of $C_{x_u,x_u}$, which is $N$ at $t = 0$ and $0$ elsewhere, so $|X_u[k]|^2 = N$.

```pseudo id=main
ZADOFF-CHU(u, N)             ▷ gcd(u, N) = 1
L1  c ← N mod 2
L2  return [exp(-jπ u n (n + c) / N) for n ← 0 to N - 1]

CORR(x, y, t)
L3  return Σ_{n=0}^{N-1} x[n] · conj(y[(n + t) mod N])
```

Making the sequence costs $O(N)$ operations in the [real RAM](/real-ram/) model, and one correlation costs $O(N)$. For odd $N$ all of the arithmetic can be done in integers modulo $N$ on the exponents $m_n$.

## Examples and non-examples

**Length 7, root 1.** The exponents $m_n = n(n+1)/2 \bmod 7$ are $0, 1, 3, 6, 3, 1, 0$, so the sequence is $e^{-j 2\pi m_n/7}$: about $1$, $0.6235 - 0.7818j$, $-0.9010 - 0.4339j$, $0.6235 + 0.7818j$, $-0.9010 - 0.4339j$, $0.6235 - 0.7818j$, $1$. At shift $t = 1$, the differences $m_n - m_{n+1} \bmod 7$ take each value $0, 1, \ldots, 6$ exactly once, so the correlation is the sum of all seventh roots of unity, which is $0$. The same holds at every shift from $1$ to $6$.

**Length 7, roots 1 and 3.** For $u = 3$ the exponents are $0, 3, 2, 4, 2, 3, 0$. The cross-correlation with the root-1 sequence has the values $2.5794 - 0.5887j$, $2.0685 + 1.6496j$, $-2.5794 - 0.5887j$, $2.6458j$, $2.6458j$, $-2.5794 - 0.5887j$ and $2.0685 + 1.6496j$ at shifts $0$ to $6$. Each has magnitude $\sqrt 7 = 2.6458$, which is $8.45$ dB below the peak of $7$.

**Even length.** For $N = 8$ and $u = 1$, $x[n] = e^{-j\pi n^2/8}$. The autocorrelation is $8$ at shift $0$ and $0$ at the other seven shifts.

**Comparison with the Welch bound.** For prime $N$ and the $M = N - 1$ roots, the largest cross-correlation is $\sqrt N$. The [Welch bound](/welch-bound/) for $M$ sequences of length $N$ and energy $N$ is $N\sqrt{(M-1)/(MN-1)}$. For $N = 7$, $31$ and $839$ the bound is $2.4445$, $5.4771$ and $28.9482$, against $\sqrt N = 2.6458$, $5.5678$ and $28.9655$. The ratio is $1.0823$, $1.0165$ and $1.0006$. A binary family of the same size cannot come this close, since its correlations are integers of fixed parity.

**Non-example: composite length.** For $N = 63$, the roots $1$ and $2$ differ by $1$, which is coprime to $63$, and their cross-correlation has magnitude $\sqrt{63} = 7.9373$ at every shift. The roots $1$ and $4$ differ by $3$, which divides $63$. Their cross-correlation is $0$ at some shifts and $\sqrt{3 \cdot 63} = 13.7477$ at the others, so the constant magnitude is lost. This is one reason why standards use prime lengths when they need many roots.

**Non-example: root not coprime to $N$.** If $g = \gcd(u, N) > 1$, then $ut \equiv 0 \pmod N$ at $t = N/g$, and the autocorrelation at that shift has magnitude $N$, as large as the peak. The definition excludes such roots.

**Use in LTE.** LTE builds its random-access preambles from Zadoff-Chu sequences of prime length $839$ and makes several preambles from one root by cyclic shifts, since the shifts are orthogonal. The primary synchronization signal uses a length-63 sequence with the middle element removed and one of the roots $25$, $29$ and $34$.

## Related definitions

- The [Frank code](/frank-code/) of length $L^2$ has phases $2\pi \, pq / L$ on an $L \times L$ grid. It has the same zero periodic autocorrelation and belongs to the same family of chirp-like polyphase codes.
- A frequency offset couples with the shift. If the received sequence is multiplied by $e^{j2\pi n/N}$, one bin of the DFT, the correlation peak moves from shift $0$ to the shift $-u^{-1} \bmod N$, where $u^{-1}$ is the inverse of $u$ modulo $N$. With the definition of $C$ above, the peak for $N = 7$ moves to shift $6$ for $u = 1$ and to shift $2$ for $u = 3$; for $N = 839$ and $u = 1$ it moves to shift $838$. A [frequency offset](/frequency-offset-estimation/) of a whole bin can therefore look like a delay, and preamble detectors must allow for it.
- [Maximal-length sequences](/maximal-length-sequence/) are the binary counterpart: their periodic autocorrelation is $-1$ off the peak, not $0$.
- In [SC-FDMA](/sc-fdma/) and [OFDM](/orthogonal-frequency-division-multiplexing/) systems the flat DFT of a Zadoff-Chu sequence makes it a good reference signal: every subcarrier gets the same power, and the time signal has a low peak-to-average ratio.
- [Preamble correlation detection](/preamble-correlation-detection/) uses the zero autocorrelation to find the start of a frame without false peaks at other shifts.

## References
