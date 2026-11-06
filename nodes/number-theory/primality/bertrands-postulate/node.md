---
tag: ZDPRG9
kind: theorem
slug: bertrands-postulate
name: Bertrand's postulate
aliases:
- Chebyshev-Erdős theorem
area: number-theory/primality
level: intro
summary: For every integer n ≥ 1 there is a prime p with n < p ≤ 2n.
prereqs: [prime-number, binomial-coefficient, legendre-formula]
see_also: [prime-number-theorem, prime-gaps, prime-counting-function, random-prime-generation, binomial-coefficient-bounds, legendre-formula]
sources:
  - book: isbn:9783662572641
    title: Martin Aigner and Günter M. Ziegler, Proofs from THE BOOK, sixth edition, Springer, 2018
    locator: Chapter 2, Bertrand's postulate (Erdős's proof, with the chain of primes for small n and the bound on the product of the primes up to x)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Section 22.3, Bertrand's postulate and a 'formula' for primes (Theorem 418)
  - paper: "Paul Erdős, Beweis eines Satzes von Tschebyschef, Acta Litterarum ac Scientiarum (Szeged) 5, 1932"
    locator: pages 194 to 198
  - paper: "Srinivasa Ramanujan, A proof of Bertrand's postulate, Journal of the Indian Mathematical Society 11, 1919"
    locator: pages 181 to 182
---

Bertrand's postulate says that for each integer $n \ge 1$ there is a [prime](/prime-number/) $p$ with $n < p \le 2n$. Bertrand conjectured it in 1845, Chebyshev proved it in 1852, and Erdős found in 1932 the short proof below, which uses only the [central binomial coefficient](/binomial-coefficient/) $\binom{2n}{n}$ and [Legendre's formula](/legendre-formula/). In algorithms it is the reason that a prime of a chosen size always exists: there is a prime between $m$ and $2m$ for a hash table, a fingerprint modulus or a [random prime](/random-prime-generation/).

## Statement

**Theorem (Bertrand's postulate; Chebyshev 1852).** For every integer $n \ge 1$ there is a prime $p$ with

$$n < p \le 2n.$$

**Lemma (Erdős).** For every real $x \ge 2$,

$$\prod_{p \le x,\ p \text{ prime}} p \le 4^{x - 1}.$$

The lemma is a bound of [Chebyshev](/prime-counting-function/) type on the product of the primes up to $x$; it gives $\vartheta(x) = \sum_{p \le x} \ln p < x \ln 4$.

## In plain words

Pick any whole number. Double it. Somewhere after the number, up to and including its double, there is always a prime. So primes never thin out so much that one doubling skips all of them.

The proof looks at the middle number of a row of Pascal's triangle, the number of ways to choose half of the items from twice that many. This number is large, about four to the power of the starting number. But if no prime sat between the number and its double, each prime factor of it would be small and appear only a few times, and the product of such factors would be too small. The two estimates clash, so the prime must exist.

## Proof

The proof follows Erdős, as presented by Aigner and Ziegler, with a different split between the small and the large cases.

**Step 1: small $n$.** The numbers $2, 3, 5, 7, 13, 23, 43, 83, 163, 317, 631$ are prime, and each is less than twice the one before it. Let $1 \le n \le 630$, and let $q$ be the first number of this chain with $q > n$. If $q = 2$, then $n = 1$ and $1 < 2 \le 2$. Otherwise the number $q'$ before $q$ in the chain satisfies $q' \le n$, so $q < 2q' \le 2n$. In both cases $n < q \le 2n$. So the theorem holds for $n \le 630$.

**Step 2: proof of the lemma.** It is enough to prove the bound for integers $m \ge 2$, because the product for $x$ is the product for $m = \lfloor x \rfloor$, and $4^{m-1} \le 4^{x-1}$. We use strong induction on $m$. For $m = 2$ the product is $2 \le 4$. For even $m > 2$, $m$ is not prime, so the product equals the product for $m - 1$, which is at most $4^{m-2} < 4^{m-1}$. For odd $m = 2k + 1 \ge 3$, each prime $p$ with $k + 1 < p \le 2k + 1$ divides $(2k+1)!$ but not $k!\,(k+1)!$, so it divides $\binom{2k+1}{k}$. The two equal numbers $\binom{2k+1}{k}$ and $\binom{2k+1}{k+1}$ are terms of the sum $\sum_j \binom{2k+1}{j} = 2^{2k+1}$, so $\binom{2k+1}{k} \le 2^{2k} = 4^k$. Since $2 \le k + 1 < m$, the induction hypothesis gives

$$\prod_{p \le 2k+1} p = \prod_{p \le k+1} p \cdot \prod_{k+1 < p \le 2k+1} p \le 4^{k} \cdot \binom{2k+1}{k} \le 4^{k} \cdot 4^{k} = 4^{m-1}.$$

**Step 3: a lower bound on $\binom{2n}{n}$.** The $2n + 1$ numbers $\binom{2n}{j}$ sum to $4^n$, and $\binom{2n}{n}$ is the largest. Put the two end terms $\binom{2n}{0} + \binom{2n}{2n} = 2$ together; for $n \ge 1$ this is at most $\binom{2n}{n}$, and so is each of the other $2n - 1$ terms. So $4^n \le 2n \binom{2n}{n}$.

**Step 4: the prime factors of $\binom{2n}{n}$.** By Legendre's formula, the exponent of a prime $p$ in $\binom{2n}{n} = (2n)!/(n!)^2$ is

$$e_p = \sum_{i \ge 1} \left( \left\lfloor \frac{2n}{p^i} \right\rfloor - 2 \left\lfloor \frac{n}{p^i} \right\rfloor \right).$$

Each term is 0 or 1, since $\lfloor 2y \rfloor - 2\lfloor y \rfloor \in \{0, 1\}$ for real $y$, and each term with $p^i > 2n$ is 0. So $p^{e_p} \le 2n$, and $e_p \le 1$ when $p > \sqrt{2n}$. Now let $n \ge 5$ and $2n/3 < p \le n$. Then $p^2 > 4n^2/9 > 2n$, so only the term $i = 1$ can count, and it is $\lfloor 2n/p \rfloor - 2\lfloor n/p \rfloor = 2 - 2 = 0$, because $2 \le 2n/p < 3$ and $1 \le n/p < 3/2$. So these primes do not divide $\binom{2n}{n}$.

**Step 5: large $n$.** Let $n \ge 631$ and assume that no prime lies in $(n, 2n]$. By Step 4 each prime factor of $\binom{2n}{n}$ is at most $2n/3$. Split them. There are fewer than $\sqrt{2n}$ primes $p \le \sqrt{2n}$, and each contributes $p^{e_p} \le 2n$. The primes in $(\sqrt{2n}, 2n/3]$ have $e_p \le 1$, so by the lemma they contribute at most $4^{2n/3 - 1} < 4^{2n/3}$. With Step 3,

$$\frac{4^n}{2n} \le \binom{2n}{n} < (2n)^{\sqrt{2n}} \, 4^{2n/3}, \qquad \text{so} \qquad 4^{n/3} < (2n)^{1 + \sqrt{2n}}.$$

Let $f(n) = \frac{n}{3} \ln 4 - (1 + \sqrt{2n}) \ln(2n)$; the last inequality says $f(n) < 0$. At $n = 631$, $\frac{631}{3} \ln 4 > 291.5$, while $\sqrt{1262} < 35.53$ and $\ln 1262 < 7.141$ give $(1 + \sqrt{1262}) \ln 1262 < 260.9$; so $f(631) > 0$. The derivative of $(1 + \sqrt{2n}) \ln(2n)$ is $\ln(2n)/\sqrt{2n} + (1 + \sqrt{2n})/n$. Both terms decrease for $n \ge 631$, because $\ln t / \sqrt t$ decreases for $t > e^2$, and at $n = 631$ their sum is less than $0.202 + 0.058 = 0.26 < \frac{1}{3}\ln 4 \approx 0.462$. So $f$ increases on $[631, \infty)$, and $f(n) > 0$ for each $n \ge 631$. This contradicts $f(n) < 0$. So a prime lies in $(n, 2n]$.

Steps 1 and 5 cover all $n \ge 1$. $\blacksquare$

## Consequences

- **The $k$-th prime.** If $p_k$ is the $k$-th prime, then $p_{k+1} \le 2p_k$, so $p_k \le 2^k$ by induction on $k$. So a number of $k$ binary digits has a prime below it with at most $k$ binary digits, and each range $(2^{k-1}, 2^k]$ holds a prime.
- **Primes of a given size.** For each $m \ge 1$ a prime lies in $(m, 2m]$. A hash table, a [Rabin-Karp](/rabin-karp/) fingerprint or a [universal hash family](/universal-hash-family/) that needs a prime modulus near $m$ can always get one at most twice as large. An algorithm that scans $m + 1, m + 2, \ldots$ with a [primality test](/primality-testing/) stops before $2m$.
- **[Random prime generation](/random-prime-generation/).** Sampling from $(2^{k-1}, 2^k]$ until a prime is found is well defined for each $k \ge 2$, since the range is not empty of primes. The count of primes there, and so the expected number of samples, comes from the [prime number theorem](/prime-number-theorem/), not from this theorem.
- **Chebyshev bounds.** The lemma gives $\vartheta(x) < x \ln 4$, an explicit upper bound of the right order for the [prime-counting function](/prime-counting-function/). Lower bounds of the same order follow from Step 3.
- **[Prime gaps](/prime-gaps/).** The gap after a prime $p$ is less than $p$, since a prime lies in $(p, 2p]$.

## Tightness

The factor 2 cannot be lowered for the statement over all $n \ge 1$: for $n = 1$ the only prime in $(1, 2]$ is $2 = 2n$. For $n = 1, 2, 3, 5$ the interval $(n, 2n]$ holds exactly one prime, and for each other $n$ below $1000$ it holds at least two. For large $n$ the interval holds many primes: $(10^5, 2 \cdot 10^5]$ holds 8392. By the [prime number theorem](/prime-number-theorem/), for each $\varepsilon > 0$ there is a prime in $(n, (1 + \varepsilon) n]$ for all large enough $n$, so only the small cases force the factor 2.

## History

Joseph Bertrand conjectured in 1845 that there is a prime between $n$ and $2n - 2$ for $n > 3$, and checked it for $n$ below three million. Pafnuty Chebyshev proved it in a memoir published in 1852, with analytic estimates of the products of primes. Srinivasa Ramanujan gave a simpler proof in 1919, with the gamma function. Paul Erdős, aged 19, published in 1932 the elementary proof by the central binomial coefficient, which is the proof above. The name "postulate" stayed, although the statement has been a theorem since 1852.

## References
