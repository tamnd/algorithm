---
tag: H5NT6J
kind: definition
slug: kasami-sequences
name: Kasami sequences
aliases:
- Kasami codes
area: communications/multiple-access-and-spread-spectrum
level: advanced
summary: "Binary sequence families from an m-sequence and its decimations. The small set has 2^(n/2) sequences of period 2^n - 1 and largest correlation 1 + 2^(n/2), the least possible for binary sequences."
model: word-ram
prereqs: [maximal-length-sequence, gold-sequences, welch-bound]
see_also: [code-division-multiple-access, cross-correlation, linear-feedback-shift-register, ovsf-codes, cyclic-code, direct-sequence-spread-spectrum, zadoff-chu-sequence, multiuser-detection]
sources:
  - url: https://hdl.handle.net/2142/74439
    title: Tadao Kasami, Weight Distribution Formula for Some Class of Cyclic Codes, Coordinated Science Laboratory, University of Illinois, Report R-285, April 1966 (doi:10.21236/ad0632574)
    locator: The whole report (the weight distribution of the cyclic codes whose codewords give the Kasami sequences)
  - paper: doi:10.1109/PROC.1980.11697
    title: Dilip V. Sarwate and Michael B. Pursley, Crosscorrelation properties of pseudorandom and related sequences, Proceedings of the IEEE 68(5), 1980
    locator: pp. 593 to 619 (the sections on the small and the large sets of Kasami sequences and their comparison with the Welch bound)
  - paper: doi:10.1109/TIT.1974.1055219
    title: Lloyd R. Welch, Lower bounds on the maximum cross correlation of signals, IEEE Transactions on Information Theory 20(3), 1974
    locator: pp. 397 to 399 (the bound that the small Kasami set is compared with)
---

Kasami sequences are binary sequence families of period $N = 2^n - 1$, for even $n$, made by adding an [m-sequence](/maximal-length-sequence/) $u$ to the shifts of one or two decimations of $u$. The **small set** has $2^{n/2}$ sequences, and every off-peak autocorrelation and every cross-correlation in it takes one of the three values $-1$, $-1 - 2^{n/2}$ and $-1 + 2^{n/2}$, so the largest magnitude is $1 + 2^{n/2}$, about $\sqrt N$. The **large set**, for $n \equiv 2 \pmod 4$, contains a [Gold family](/gold-sequences/) and many more sequences, with the Gold bound $t(n)$ as its largest correlation. The small set is optimal for binary sequences in the sense of Sarwate and Pursley 1980: the [Welch bound](/welch-bound/) and the fact that binary correlations of odd length are odd integers force $\theta_{\max} \ge 1 + 2^{n/2}$ for any $2^{n/2}$ binary sequences of period $N$, and the small set reaches that value. It does not meet the real-valued Welch bound with equality. The construction comes from Kasami's 1966 report on the weight distributions of some cyclic codes.

## Definition

Use the notation of the [Gold sequences](/gold-sequences/) page: bit sequences of period $N$, the shift $T^\tau s$, the decimation $s[q] = (s_{qk \bmod N})_k$, the periodic correlation $\theta_{a,b}(\tau) = \sum_k (-1)^{a_k \oplus b_{k+\tau}}$ and the figure of merit $\theta_{\max}$ over all pairs and shifts except the peaks.

**Small set.** Let $n$ be even, $u$ an m-sequence of degree $n$ and period $N = 2^n - 1$, and $s(n) = 2^{n/2} + 1$. The decimation $w = u[s(n)]$ is not an m-sequence of degree $n$: since $s(n)$ divides $N = (2^{n/2} - 1)(2^{n/2} + 1)$, $w$ has period $2^{n/2} - 1$, and it is an m-sequence of degree $n/2$ repeated $2^{n/2} + 1$ times. The small Kasami set is

$$\mathcal{K}_S(u) = \{u\} \cup \{u \oplus T^\tau w : \tau = 0, 1, \ldots, 2^{n/2} - 2\},$$

with $2^{n/2}$ sequences of period $N$. Every off-peak autocorrelation and every cross-correlation of $\mathcal{K}_S$ takes a value in $\{-1, \ -1 - 2^{n/2}, \ -1 + 2^{n/2}\}$, so $\theta_{\max} = 1 + 2^{n/2}$ (Sarwate and Pursley 1980, the section on Kasami sequences). Each member satisfies a linear recurrence of degree $3n/2$, the product of the polynomials of $u$ and $w$.

**Large set.** For $n \equiv 2 \pmod 4$, let $v = u[t(n)]$ with $t(n) = 1 + 2^{(n+2)/2}$, so that $(u, v)$ is a preferred pair, and $w = u[s(n)]$ as above. The large set is the Gold family $\mathcal{G}(u, v)$ together with the sums $u \oplus T^i v \oplus T^j w$, $u \oplus T^j w$ and $v \oplus T^j w$ for $0 \le i < N$ and $0 \le j < 2^{n/2} - 1$. It has $2^{n/2}(2^n + 1)$ sequences, and its correlations take values in $\{-1, \ -1 \pm 2^{n/2}, \ -1 \pm 2^{(n+2)/2}\}$, so $\theta_{\max} = t(n)$, the same as the Gold family it contains (Sarwate and Pursley 1980).

**Optimality of the small set.** Let $M = 2^{n/2}$, so $N = M^2 - 1$. The sequence form of the Welch bound says that $M$ sequences of length $N$ and energy $N$ have $\theta_{\max} \ge B = N \sqrt{(M-1)/(MN-1)}$. Then $B > M - 1$: squaring and dividing by $M - 1$, this is $(M-1)(M+1)^2 > M^3 - M - 1$, which reduces to $M^2 > 0$. A correlation of two $\pm 1$ sequences of odd length $N$ is $N$ minus twice a count, so it is odd. The odd numbers above $M - 1$ start at $M + 1$, so every binary family of $M$ sequences of period $N$ has $\theta_{\max} \ge M + 1 = 1 + 2^{n/2}$, and the small Kasami set meets this. The real bound $B$ itself is strictly smaller than $M + 1$.

```pseudo id=main
KASAMI-SMALL(u)             ▷ u an m-sequence of even degree n, N = 2^n - 1
L1  w ← u[2^{n/2} + 1]           ▷ decimation: w[k] = u[(2^{n/2} + 1) k mod N]
L2  F ← [u]
L3  for τ ← 0 to 2^{n/2} - 2 do
L4      append u ⊕ T^τ w to F
    return F

THETA-MAX(F)
L5  return the largest |θ_{a,b}(τ)| over a, b in F and τ, except a = b with τ = 0
```

The construction costs $O(N \, 2^{n/2})$ bit operations in the [word RAM](/word-ram/) model, and the direct check of $\theta_{\max}$ costs $O(2^n N^2)$.

## Examples and non-examples

**Degree 4.** With $u$ from $x^4 + x + 1$ ($100010011010111$) and $s(4) = 5$, the decimation $w = u[5]$ has period $3$. The small set has $4$ sequences of period $15$. Over all ordered pairs and shifts except the peaks, the correlation is $-5$ in $68$ cases, $-1$ in $56$ cases and $3$ in $112$ cases. So $\theta_{\max} = 5 = 1 + 2^2$. The Welch bound for $M = 4$ and $N = 15$ is $15 \sqrt{3/59} = 3.38$; the least odd integer at or above it is $5$.

**Degree 6.** With $u$ from $x^6 + x + 1$, $w = u[9]$ has period $7$. The small set has $8$ sequences of period $63$, with correlation values $-9$, $-1$ and $7$ and $\theta_{\max} = 9$. The Welch bound is $63 \sqrt{7/503} = 7.43$, so $9$ is the least possible odd value. A Gold family of degree 6 has $65$ sequences and $\theta_{\max} = 17$. The small Kasami set trades $57$ sequences for half the largest correlation.

**Degree 8.** With $u$ from $x^8 + x^4 + x^3 + x^2 + 1$, the small set has $16$ sequences of period $255$ and $\theta_{\max} = 17$, against a Welch bound of $15.46$. The ratio of $\theta_{\max}$ to the bound is $1.48$, $1.21$ and $1.10$ for $n = 4$, $6$ and $8$; it goes to $1$ as $n$ grows.

**Large set, degree 6.** With $v = u[17]$ and $w = u[9]$, the large set has $8 \cdot 65 = 520$ sequences of period $63$, and its correlations lie in $\{-17, -9, -1, 7, 15\}$, so $\theta_{\max} = 17 = t(6)$.

**Non-example: odd $n$.** For odd $n$, $2^{n/2}$ is not an integer and $2^n - 1$ has no factor $2^{n/2} + 1$. The small set does not exist; use a Gold family.

**Non-example: decimating by a number coprime to $N$.** If $\gcd(q, N) = 1$, then $u[q]$ is again an m-sequence of period $N$, not a short sequence, and adding it to $u$ gives a Gold-like family only for the preferred values of $q$. The Kasami step needs the short period that comes from $\gcd(s(n), N) = s(n)$.

## Related definitions

- [Gold sequences](/gold-sequences/) have about $2^n$ sequences and $\theta_{\max}$ near $\sqrt{2N}$ or $2\sqrt N$. The small Kasami set has about $\sqrt N$ sequences and $\theta_{\max}$ near $\sqrt N$. The large Kasami set has about $N^{3/2}$ sequences with the Gold value of $\theta_{\max}$.
- The [Welch bound](/welch-bound/) is the reference for optimality. Complex sequence families, such as sets of [Zadoff-Chu sequences](/zadoff-chu-sequence/) of prime length, can do better than any binary family.
- The sums $a \oplus T^\tau b$ of members of the small set lie in the [cyclic code](/cyclic-code/) of length $N$ and dimension $3n/2$ spanned by the shifts of $u$ and $w$. A correlation value $\theta$ belongs to a codeword of weight $(N - \theta)/2$, so the three values correspond to the three nonzero weights $2^{n-1}$ and $2^{n-1} \pm 2^{n/2 - 1}$. Kasami's 1966 report found the weight distributions of this class of cyclic codes.
- [Code-division multiple access](/code-division-multiple-access/) uses such families as user signatures. IS-95, for example, uses long m-sequences and Walsh codes instead.

## References
