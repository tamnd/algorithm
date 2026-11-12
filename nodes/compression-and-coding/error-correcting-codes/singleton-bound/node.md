---
tag: HQ6X1P
kind: theorem
slug: singleton-bound
name: Singleton bound
area: compression-and-coding/error-correcting-codes
level: core
summary: A code of length n and minimum distance d over q symbols has at most q^(n - d + 1) words, so k <= n - d + 1 for a linear code. MDS codes such as Reed-Solomon codes meet it.
prereqs: [minimum-distance, linear-code]
see_also: [reed-solomon-code, hamming-bound, plotkin-bound, griesmer-bound, erasure-codes, parity-check-matrix, dual-code]
sources:
  - paper: doi:10.1109/TIT.1964.1053661
    title: R. C. Singleton, Maximum distance q-nary codes, IEEE Transactions on Information Theory 10(2), 1964
    locator: pp. 116 to 118 (the bound and the codes that meet it)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Section 4.1 (the Singleton bound), Chapter 11 (MDS codes) and Section 11.4 (GRS codes and the MDS conjecture)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (the Singleton bound) and Chapter 11 (MDS codes, their weight distribution and the trivial binary MDS codes)
  - paper: doi:10.4171/JEMS/316
    title: Simeon Ball, On sets of vectors of a finite vector space in which every subset of basis size is a basis, Journal of the European Mathematical Society 14(3), 2012
    locator: pp. 733 to 748 (the MDS conjecture for prime q)
  - paper: doi:10.1137/0108018
    title: I. S. Reed and G. Solomon, Polynomial codes over certain finite fields, Journal of the Society for Industrial and Applied Mathematics 8(2), 1960
    locator: pp. 300 to 304 (the codes of evaluations of polynomials of bounded degree)
---

The Singleton bound says that a code of length $n$ and [minimum distance](/minimum-distance/) $d$ over an alphabet of $q$ symbols has at most $q^{n - d + 1}$ words. For a [linear code](/linear-code/) $[n, k, d]_q$ it reads $k \le n - d + 1$: each unit of distance costs at least one check symbol. It holds for all codes, linear or not, and over any alphabet. Codes that meet it are *maximum distance separable* (MDS), and the [Reed-Solomon codes](/reed-solomon-code/) are the main example.

## Statement

Notation. $\Sigma$ is an alphabet of size $q \ge 2$. $A_q(n, d)$ is the largest size of a code $C \subseteq \Sigma^n$ in which any two distinct words differ in at least $d$ positions, linear or not. A linear code over GF($q$) is an $[n, k, d]_q$ code with rate $R = k/n$ and relative distance $\delta = d/n$. Words are rows.

**Theorem (all codes).** For $1 \le d \le n$,

$$A_q(n, d) \le q^{n - d + 1}.$$

**Corollary (linear codes).** A linear $[n, k, d]_q$ code has $k \le n - d + 1$, that is $d \le n - k + 1$.

**Asymptotic form.** A family of codes with relative distance $\delta$ has rate $R \le 1 - \delta + 1/n$, so $R \le 1 - \delta$ in the limit.

**Definition.** A code with $|C| = q^{n - d + 1}$ is maximum distance separable (MDS). A linear MDS code has $d = n - k + 1$.

**Theorem (characterization of linear MDS codes).** For a linear $[n, k, d]_q$ code $C$ with generator matrix $G$ and [parity-check matrix](/parity-check-matrix/) $H$, these are equivalent:

1. $C$ is MDS.
2. Every $n - k$ columns of $H$ are linearly independent.
3. Every $k$ columns of $G$ are linearly independent, so every set of $k$ positions is an information set.
4. The [dual code](/dual-code/) $C^\perp$ is MDS.

## In plain words

Take all codewords and erase the same few positions from each, one fewer than the minimum distance. The shortened words are still all different: two codewords that agreed after the erasure would differ only inside the erased part, which is too small. So there are at most as many codewords as there are words of the shorter length. Each extra unit of distance costs one symbol of the word. Codes that pay exactly this price are the best possible for their length and are called MDS codes.

## Proof

*Bound.* Let $C$ have minimum distance $d$, and let $\pi : \Sigma^n \to \Sigma^{n - d + 1}$ delete the last $d - 1$ positions. If $\pi(x) = \pi(y)$ for distinct $x, y \in C$, then $x$ and $y$ agree on the first $n - d + 1$ positions, so $d(x, y) \le d - 1$, a contradiction. So $\pi$ is injective on $C$ and $|C| \le q^{n - d + 1}$. For a linear code $|C| = q^k$, which gives $k \le n - d + 1$. The asymptotic form follows by dividing by $n$: $R = k/n \le 1 - \delta + 1/n$.

*Characterization.* (1 ⇔ 2) A nonzero codeword $c$ with $H c^T = 0$ and weight $w$ is a nonzero linear relation among $w$ columns of $H$, and back. So $d$ is the least number of linearly dependent columns of $H$. Every $n - k$ columns are independent if and only if $d \ge n - k + 1$, and the bound gives equality. (1 ⇒ 3) If some $k$ columns of $G$ were dependent, the $k \times k$ submatrix $G_S$ on those positions would be singular, so $m G_S = 0$ for some message $m \ne 0$. The codeword $m G$ is nonzero, since $G$ has rank $k$, and it is zero on the $k$ positions of $S$, so its weight is at most $n - k < d$. Contradiction. (3 ⇒ 4) $G$ is a parity-check matrix of $C^\perp$, an $[n, n - k]$ code. By (1 ⇔ 2) applied to $C^\perp$, every $k = n - (n - k)$ columns of $G$ being independent means that $C^\perp$ is MDS. (4 ⇒ 1) Apply (1 ⇒ 4) to $C^\perp$, whose dual is $C$. $\blacksquare$

## Consequences

**MDS codes and erasures.** By item 3, any $k$ symbols of a codeword of an MDS code determine it. So an MDS code recovers from any $n - k$ erasures, the most that any code with $q^k$ words can recover. This is why Reed-Solomon codes are used for [erasure codes](/erasure-codes/) in storage: a $[k + r, k]$ code survives the loss of any $r$ disks.

**Reed-Solomon codes meet it.** The code of the values of all polynomials of degree less than $k$ over GF($q$) at $n \le q$ distinct points has $d = n - k + 1$: a nonzero polynomial of degree at most $k - 1$ has at most $k - 1$ zeros, so its codeword has weight at least $n - k + 1$. Adding one more position with the coefficient of $x^{k-1}$ gives a doubly extended code of length $q + 1$, also MDS. Over GF(7), the code of length 6 and $k = 2$ is a $[6, 2, 5]_7$ code with $49 = 7^{6 - 5 + 1}$ words. The tests enumerate all such codes over GF(5) and GF(7) and find $d = n - k + 1$ in each case.

**Binary codes are almost never MDS.** The only binary MDS codes are the trivial ones: $[n, n, 1]$, the parity code $[n, n - 1, 2]$, and the [repetition code](/repetition-code/) $[n, 1, n]$. Proof: let $C$ be a binary $[n, k, n - k + 1]$ code with $2 \le k \le n - 2$. After a permutation of positions, $G = [I_k \mid P]$. Each row has weight $1 + \mathrm{wt}(P_i) \ge n - k + 1$, so each row of $P$ is all ones. Then the sum of the first two rows has weight 2, but $d = n - k + 1 \ge 3$. The tests confirm this by listing every binary linear code of length at most 6.

**Weak for small alphabets.** For $q = 2$ the [Hamming bound](/hamming-bound/) and the [Plotkin bound](/plotkin-bound/) are much stronger. The asymptotic Hamming bound $1 - h_q(\delta/2)$ tends to $1 - \delta/2$ as $q$ grows, so for large $q$ the Singleton bound is the stronger one:

| $\delta$ | 0.2 | 0.4 | 0.6 |
|---|---|---|---|
| Singleton, $1 - \delta$ | 0.8 | 0.6 | 0.4 |
| Hamming, $q = 2$ | 0.5310 | 0.2781 | 0.1187 |
| Hamming, $q = 4$ | 0.6863 | 0.4805 | 0.3216 |
| Hamming, $q = 16$ | 0.7851 | 0.6242 | 0.4867 |
| Hamming, $q = 256$ | 0.8414 | 0.7099 | 0.5901 |

The $q$-ary [Plotkin bound](/plotkin-bound/) $R \le 1 - \delta/(1 - 1/q)$ improves on the Singleton bound for every $q$, by a factor that tends to 1 as $q$ grows.

**Weight distribution.** The weight distribution of a linear MDS code depends only on $n$, $k$ and $q$ (MacWilliams and Sloane, Chapter 11). It follows from the [MacWilliams identity](/macwilliams-identity/), because both the code and its dual are MDS.

## Tightness

The bound is met for every $n \le q + 1$ and every $k$ by the (extended) Reed-Solomon codes, and for every $n$ by the trivial codes. The open question is how long a nontrivial MDS code can be.

**The MDS conjecture.** Let $q$ be a prime power and $2 \le k \le q$. Every linear $[n, k]$ MDS code over GF($q$) has $n \le q + 1$, except when $q$ is even and $k = 3$ or $k = q - 1$, where $n \le q + 2$ (Roth, Section 11.4). Ball (2012) proved the conjecture when $q$ is a prime $p$: a linear MDS code over GF($p$) of dimension $k \le p$ has length at most $p + 1$. For other prime powers it is proved only in part.

**Nonlinear codes.** For codes that are not linear, an MDS code with $q^2$ words and $d = n - 1$ is the same object as a set of $n - 2$ mutually orthogonal Latin squares of order $q$ (MacWilliams and Sloane, Chapter 11). Over alphabets that are not prime powers, the best lengths are not known.

## History

Singleton (1964) proved the bound for $q$-ary codes and studied the codes that meet it. Reed and Solomon (1960) had already defined the polynomial codes that meet it for every length up to $q$. A linear MDS code of dimension 3 is the same as an arc in a finite projective plane, so the MDS conjecture is also a question of finite geometry (Roth, Chapter 11). Ball proved the prime case in 2012.

## References
