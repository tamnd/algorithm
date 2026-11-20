---
tag: BGG18W
kind: definition
slug: gold-sequences
name: Gold sequences
aliases:
- Gold codes
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "The 2^n + 1 binary sequences made from a preferred pair of m-sequences u and v: u, v and u plus every shift of v. All their periodic correlations take only the values -1, -t(n) and t(n) - 2."
model: word-ram
prereqs: [maximal-length-sequence]
see_also: [kasami-sequences, welch-bound, code-division-multiple-access, direct-sequence-spread-spectrum, cross-correlation, parallel-code-phase-search, linear-feedback-shift-register, multiuser-detection]
sources:
  - paper: doi:10.1109/TIT.1967.1054048
    title: Robert Gold, Optimal binary sequences for spread spectrum multiplexing, IEEE Transactions on Information Theory 13(4), 1967
    locator: pp. 619 to 621 (the sum of a preferred pair of maximal-length sequences and the three-valued cross-correlation bound t(n))
  - paper: doi:10.1109/PROC.1980.11697
    title: Dilip V. Sarwate and Michael B. Pursley, Crosscorrelation properties of pseudorandom and related sequences, Proceedings of the IEEE 68(5), 1980
    locator: pp. 593 to 619 (the sections on the cross-correlation of m-sequences, preferred pairs and Gold sequences)
  - book: isbn:9780817643904
    title: Kai Borre, Dennis M. Akos, Nicolaj Bertelsen, Peter Rinder and Søren Holdt Jensen, A Software-Defined GPS and Galileo Receiver, a Single-Frequency Approach, Birkhäuser, 2007
    locator: The chapter on the GPS signal (the C/A codes as Gold codes from two 10-cell shift registers)
---

Gold sequences are a family of $2^n + 1$ binary sequences of period $N = 2^n - 1$ whose periodic autocorrelations (off the peak) and cross-correlations all lie in the set $\{-1, -t(n), t(n) - 2\}$, with $t(n) = 1 + 2^{\lfloor (n+2)/2 \rfloor}$. Robert Gold built them in 1967 by adding, bit by bit, one [m-sequence](/maximal-length-sequence/) $u$ to every cyclic shift of a second m-sequence $v$ of the same degree. The pair $(u, v)$ must be a preferred pair, one whose own cross-correlation is three-valued. A single m-sequence has a perfect two-level autocorrelation, but there are few m-sequences of each degree and two of them can correlate badly. Gold sequences give up the perfect autocorrelation and get about $N$ sequences whose largest correlation is near $\sqrt{2N}$ for odd $n$. That is why they are the spreading codes of many [CDMA](/code-division-multiple-access/) systems and the C/A codes of GPS.

## Definition

Write a binary sequence of period $N$ as $s = (s_0, \ldots, s_{N-1})$, its cyclic shift by $\tau$ as $T^\tau s = (s_\tau, s_{\tau+1}, \ldots)$, with indices mod $N$, and its decimation by $q$ as $s[q] = (s_0, s_q, s_{2q}, \ldots)$. The periodic correlation of two bit sequences at shift $\tau$ is

$$\theta_{a,b}(\tau) = \sum_{k=0}^{N-1} (-1)^{a_k \oplus b_{k+\tau}} = N - 2 \, \#\{k : a_k \ne b_{k+\tau}\},$$

the correlation of their $\pm 1$ forms (bit $0$ to $+1$, bit $1$ to $-1$). For a family $\mathcal{F}$, the figure of merit is

$$\theta_{\max}(\mathcal{F}) = \max\{|\theta_{a,b}(\tau)| : a, b \in \mathcal{F}, \ (a, \tau) \ne (b, 0)\},$$

which covers the off-peak autocorrelations and all cross-correlations.

**Preferred pair.** Let $n \not\equiv 0 \pmod 4$ and $t(n) = 1 + 2^{\lfloor (n+2)/2 \rfloor}$, so $t(n) = 1 + 2^{(n+1)/2}$ for odd $n$ and $1 + 2^{(n+2)/2}$ for even $n$. Two m-sequences $u$ and $v$ of degree $n$ are a **preferred pair** if $\theta_{u,v}(\tau)$ takes exactly the three values $-1$, $-t(n)$ and $t(n) - 2$. A standard way to get one: take $v = u[q]$ with $q = 2^k + 1$ or $q = 2^{2k} - 2^k + 1$, where $\gcd(n, k) = 1$ for odd $n$ and $\gcd(n, k) = 2$ for $n \equiv 2 \pmod 4$ (Sarwate and Pursley 1980, the section on m-sequence cross-correlation). For $n$ divisible by $4$ no preferred pair exists.

**Gold family.** For a preferred pair $(u, v)$ the Gold family is

$$\mathcal{G}(u, v) = \{u, \ v\} \cup \{u \oplus T^\tau v : \tau = 0, 1, \ldots, N - 1\},$$

with $N + 2 = 2^n + 1$ sequences of period $N$. **Gold's theorem** (Gold 1967): every off-peak autocorrelation and every cross-correlation in $\mathcal{G}(u, v)$ takes a value in $\{-1, -t(n), t(n) - 2\}$, so $\theta_{\max} = t(n)$. The reason is the shift-and-add property of m-sequences: the correlation of two members reduces to the cross-correlation of $u$ and $v$ at some shift, or to an autocorrelation value $-1$. Each member is a sum of two sequences with linear recurrences of degree $n$, so it satisfies the recurrence of the product polynomial of degree $2n$.

The construction and the computation of $\theta_{\max}$ are below. Building the family costs $O(N^2)$ bit operations in the [word RAM](/word-ram/) model; checking $\theta_{\max}$ by direct sums over all pairs and shifts costs $O(N^4)$, which is fine for $n \le 6$.

```pseudo id=main
GOLD-FAMILY(u, v)            ▷ u, v a preferred pair of period N
L1  F ← [u, v]
L2  for τ ← 0 to N - 1 do
L3      append u ⊕ T^τ v to F       ▷ bitwise XOR with the shifted v
    return F

THETA-MAX(F)
    for each pair a, b in F and each shift τ, except a = b with τ = 0 do
L4      θ ← N - 2 · #{k : a[k] ≠ b[(k + τ) mod N]}
L5      best ← max(best, |θ|)
    return best
```

**Against the Welch bound.** The [Welch bound](/welch-bound/) for $M$ sequences of length $N$ and energy $N$ gives $\theta_{\max} \ge N \sqrt{(M - 1)/(MN - 1)}$, which is close to $\sqrt N$ for $M = N + 2$. For odd $n$, $t(n) = 1 + \sqrt{2(N+1)}$ is about $\sqrt 2$ times the bound; for $n \equiv 2 \pmod 4$ it is about $2$ times. The small set of [Kasami sequences](/kasami-sequences/) has a smaller $\theta_{\max}$, about $\sqrt N$, but only $\sqrt{N + 1}$ sequences.

## Examples and non-examples

**Degree 5 (the check value).** The m-sequences of $u$: $x^5 + x^2 + 1$ and $v$: $x^5 + x^4 + x^3 + x^2 + 1$, both started from $10000$, are a preferred pair. In fact $v = u[3]$, the decimation by $q = 2^1 + 1$. Over the $31$ shifts, $\theta_{u,v}(\tau)$ takes the value $-9$ six times, $-1$ fifteen times and $7$ ten times. Here $t(5) = 1 + 2^3 = 9$, so the values are $-t$, $-1$ and $t - 2$ as stated. The Gold family has $33$ distinct sequences of period $31$ and $\theta_{\max} = 9$. The Welch bound for $M = 33$ and $N = 31$ is $31 \sqrt{32/1022} = 5.49$, so the family is within a factor of $1.64$ of it. In dB, the largest correlation is $20 \log_{10}(9/31) = -10.7$ dB below the peak.

**Degree 6.** $u$ from $x^6 + x + 1$ and $v = u[5]$, which is the sequence of $x^6 + x^5 + x^2 + x + 1$, are a preferred pair with values $-17$, $-1$ and $15$, and $t(6) = 17$. Here $\gcd(6, 2) = 2$ and $q = 2^2 + 1 = 5$. The decimation by $3$ does not work for $n = 6$: $\gcd(3, 63) = 3$, so $u[3]$ is not an m-sequence of degree 6.

**GPS C/A codes.** The C/A code of each GPS satellite is a Gold code of period $1023$ from the two 10-cell registers with polynomials $x^{10} + x^3 + 1$ and $x^{10} + x^9 + x^8 + x^6 + x^3 + x^2 + 1$. Their cross-correlation over the $1023$ shifts takes the value $-65$ at $120$ shifts, $-1$ at $767$ shifts and $63$ at $136$ shifts, which matches $t(10) = 65$. Each satellite uses a different shift of the second register. The largest correlation is $20 \log_{10}(65/1023) = -23.9$ dB below the peak, which is the margin that lets a receiver separate satellites with [parallel code phase search](/parallel-code-phase-search/).

**Non-example: degree 4.** Degree 4 has two primitive polynomials, $x^4 + x + 1$ and $x^4 + x^3 + 1$. The cross-correlation of their m-sequences takes four values, $-5$, $-1$, $3$ and $7$, so they are not a preferred pair, and no other pair of degree 4 is.

**Non-example: a wrong decimation.** For $n = 5$, $u[15]$ is an m-sequence, but $15 = 2^4 - 1$ is not of the form above, and $\theta_{u, u[15]}$ takes six values from $-9$ to $11$. Adding $u$ to the shifts of this sequence does not give a Gold family.

**Non-example: m-sequences alone.** A set of distinct m-sequences of one degree is not a good CDMA family in general: the degree 5 pair $u$ and $u[15]$ above already reaches a correlation of $11$, worse than the Gold bound $9$, and degree 5 has only six m-sequences.

## Related definitions

- [Maximal-length sequences](/maximal-length-sequence/) are the parts of a Gold family. Two of the $N + 2$ members, $u$ and $v$, are m-sequences; the others are not.
- [Kasami sequences](/kasami-sequences/): the small set has fewer sequences ($2^{n/2}$) and a smaller $\theta_{\max}$ ($1 + 2^{n/2}$), and the large set contains a Gold family.
- The [Welch bound](/welch-bound/) is the limit that $\theta_{\max}$ is compared with.
- [Cross-correlation](/cross-correlation/) is the general signal processing notion; here it is periodic and on $\pm 1$ sequences.
- In [code-division multiple access](/code-division-multiple-access/), $\theta_{\max}/N$ sets the interference that one user leaks into the correlator of another, and [multiuser detection](/multiuser-detection/) removes what is left.

## References
