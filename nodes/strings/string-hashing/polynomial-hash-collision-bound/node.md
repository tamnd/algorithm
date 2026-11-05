---
tag: DBSX7N
kind: theorem
slug: polynomial-hash-collision-bound
name: Polynomial hash collision bound
aliases:
- collision probability of polynomial hashing
- random-base polynomial hashing bound
area: strings/string-hashing
level: core
summary: For two fixed distinct strings of length at most n and a base chosen uniformly at random modulo a prime p, the polynomial hashes collide with probability at most (n - 1)/p.
prereqs: [polynomial-rolling-hash, prime-number, polynomial, union-bound]
see_also: [schwartz-zippel-lemma, universal-string-hashing, rabin-karp, anti-hash-tests, string-equality-testing, substring-equality-queries, fingerprinting]
sources:
  - url: https://arxiv.org/abs/1504.06804
    title: Mikkel Thorup, High speed hashing for integers and strings, lecture notes (arXiv 1504.06804)
    locator: Section 5.3, Hashing variable length strings (the bound d/p for strings of degree at most d, and the composition with a universal hash to a smaller range)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Section 1.1, Application, verifying polynomial identities (a nonzero polynomial of degree d has at most d roots, so a random point detects it with probability at least 1 - d/|S|)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 7, Algebraic techniques (Section 7.2 on verifying polynomial identities and the Schwartz-Zippel theorem, and the sections on fingerprinting and string equality)
  - url: https://ioinformatics.org/journal/INFOL119.pdf
    title: Jakub Pachocki and Jakub Radoszewski, Where to use and how not to use polynomial string hashing, Olympiads in Informatics 7 (2013), 90-100
    locator: Section 2.3 (one comparison against many, and the birthday paradox) and Section 2.4 with Theorem 1 (collisions modulo 2^k for every odd base)
---

The polynomial hash collision bound says that two fixed different strings of length at most $n$ get the same [polynomial hash](/polynomial-rolling-hash/) for at most $n - 1$ of the $p$ possible bases modulo a [prime](/prime-number/) $p$. So with a base chosen uniformly at random, they collide with probability at most $(n-1)/p$. It is the one-variable case of the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), and it is the guarantee behind [Rabin-Karp](/rabin-karp/), [string equality testing](/string-equality-testing/) and [substring equality queries](/substring-equality-queries/). The bound holds only when the strings do not depend on the random base, and it says nothing for a modulus that is not prime, such as $2^{64}$.

## Statement

Let $p$ be a prime and $\mathbb{F}_p = \{0, 1, \ldots, p-1\}$ the field of integers modulo $p$. Each character $a$ has an integer code $c(a)$, and distinct characters have distinct codes in $\{0, 1, \ldots, p - 1\}$. For a string $x = x_0 x_1 \cdots x_{\ell-1}$ and a base $r \in \mathbb{F}_p$, the polynomial hash is

$$h_r(x) = \sum_{i=0}^{\ell-1} c(x_i)\, r^{\ell-1-i} \bmod p,$$

the value that Horner's rule computes from left to right.

**Theorem.** Let $x \ne y$ be two strings, fixed before $r$ is chosen, and let $n = \max(|x|, |y|) \ge 1$. Assume that $|x| = |y|$, or that every code is nonzero. If $r$ is chosen uniformly at random from $\mathbb{F}_p$, then

$$\Pr_r[\,h_r(x) = h_r(y)\,] \le \frac{n-1}{p}.$$

If $r$ is chosen uniformly from $\{1, \ldots, p - 1\}$, the bound is $(n-1)/(p-1)$.

**Corollary (many comparisons).** If $q$ pairs of distinct strings, each of length at most $n$, are fixed before $r$ is chosen, then the probability that at least one pair collides is at most $q(n-1)/p$. With $t$ bases chosen independently, one pair collides under all of them with probability at most $((n-1)/p)^t$.

## In plain words

Read the codes of a string as the coefficients of a polynomial, and the hash as the value of this polynomial at one secret point. Two different strings give two different polynomials, and their difference is a polynomial that is not zero.

A polynomial that is not zero has only a few roots, at most as many as its degree. The two hashes are equal only when the secret point is one of these roots. If the point is drawn at random from a large set, after the strings are fixed, it lands on a root only with a small chance: the number of roots divided by the size of the set.

The guarantee is about the random choice, not about the strings. If someone sees the point first and then picks the strings, they can make them collide.

## Proof

Let $D(t) = H_x(t) - H_y(t)$, where $H_x(t) = \sum_{i=0}^{|x|-1} c(x_i)\, t^{|x|-1-i}$ is a polynomial over $\mathbb{F}_p$ in the variable $t$, and $H_y$ likewise. For each $r \in \mathbb{F}_p$, $h_r(x) = h_r(y)$ if and only if $D(r) = 0$ in $\mathbb{F}_p$. Each of $H_x$ and $H_y$ has degree at most $n - 1$, so $D$ has degree at most $n - 1$.

*Step 1: $D$ is not the zero polynomial.*

- Case $|x| = |y| = \ell$. The coefficient of $t^{\ell-1-i}$ in $D$ is $c(x_i) - c(y_i) \bmod p$. Since $x \ne y$, there is an $i$ with $x_i \ne y_i$. The codes are distinct and lie in $\{0, \ldots, p-1\}$, so $c(x_i) - c(y_i)$ is a nonzero integer with absolute value less than $p$, and it is not $0$ modulo $p$.
- Case $|x| \ne |y|$, say $|y| < |x| = n$, with all codes nonzero. The coefficient of $t^{n-1}$ in $H_x$ is $c(x_0) \ne 0$, and $H_y$ has degree at most $|y| - 1 < n - 1$, so it has no term $t^{n-1}$. So the coefficient of $t^{n-1}$ in $D$ is $c(x_0) \ne 0$.

*Step 2: $D$ has at most $n - 1$ roots.* $\mathbb{F}_p$ is a field because $p$ is prime. A nonzero polynomial of degree $d$ over a field has at most $d$ roots: if $D(a) = 0$, polynomial division gives $D(t) = (t - a)Q(t)$ with $\deg Q = d - 1$, and a root $b \ne a$ of $D$ satisfies $(b - a)Q(b) = 0$, so $Q(b) = 0$ because a field has no zero divisors; induction on $d$ finishes the count, and a nonzero constant ($d = 0$) has no root. So $D$ has at most $\deg D \le n - 1$ roots.

*Step 3: the probability.* The base $r$ is uniform on $\mathbb{F}_p$ and independent of $x$ and $y$, so

$$\Pr[h_r(x) = h_r(y)] = \Pr[D(r) = 0] = \frac{|\{a \in \mathbb{F}_p : D(a) = 0\}|}{p} \le \frac{n-1}{p}.$$

For $r$ uniform on the $p - 1$ nonzero elements, the same count of at most $n - 1$ roots gives $(n-1)/(p-1)$.

*The corollary.* Let $E_i$ be the event that pair $i$ collides. Each pair is fixed before $r$ is chosen, so $\Pr[E_i] \le (n-1)/p$, and the [union bound](/union-bound/) gives $\Pr[E_1 \cup \cdots \cup E_q] \le q(n-1)/p$. For $t$ independent bases $r_1, \ldots, r_t$, the events "the pair collides under $r_j$" are independent, each with probability at most $(n-1)/p$, so all of them happen with probability at most $((n-1)/p)^t$. $\blacksquare$

**Where each hypothesis is used.**

- *$p$ prime.* Step 2 needs a field. Modulo $2^{64}$, the nonzero polynomial $2^{63} t$ is zero at every even $t$, and $2^{61}(t^2 - 1)$ is zero at every odd $t$, because $t^2 - 1$ is divisible by 8 for odd $t$; the [Thue-Morse attack](/anti-hash-tests/) builds strings whose difference is such a polynomial.
- *Codes below $p$ and distinct.* If two characters had codes that are equal modulo $p$, every base would make the one-character strings collide.
- *Equal lengths or nonzero codes.* With code 0 for the character a, the strings b and ab have equal hashes for every base, since a leading zero coefficient adds nothing. Hashing the length together with the string, or using codes from 1, removes this case.
- *Strings fixed before $r$.* The probability is over $r$ for a fixed pair. If the pair may depend on $r$, an adversary picks two strings whose difference polynomial has $r$ as a root.

## Consequences

- [Rabin-Karp](/rabin-karp/) compares the hash of the pattern with $n - m + 1$ window hashes. Each comparison of distinct strings of length $m$ is a false match with probability at most $(m-1)/p$, so the expected number of [spurious hits](/spurious-hit/) is at most $(n - m + 1)(m - 1)/p$.
- [String equality testing](/string-equality-testing/) sends one hash of $O(\log p)$ size instead of a whole string, with error at most $(n-1)/p$.
- [Substring equality queries](/substring-equality-queries/) answer $q$ queries on a string of length $n$ with total error probability at most $q(n-1)/p$, if the queries do not depend on $r$.
- **Choosing $p$.** The bound must be small for the number of comparisons that the program makes, not for one comparison. The table gives the per-comparison bound $(n-1)/p$ and the union bound $q(n-1)/p$ for $q$ comparisons.

| $p$ | $n$ | $q$ | $(n-1)/p$ | $q(n-1)/p$ |
|---|---|---|---|---|
| $10^9 + 7$ | $10^3$ | $10^3$ | $9.99 \times 10^{-7}$ | $9.99 \times 10^{-4}$ |
| $10^9 + 7$ | $10^5$ | $10^5$ | $1.00 \times 10^{-4}$ | about 10 (no guarantee) |
| $2^{61} - 1$ | $10^5$ | $10^5$ | $4.34 \times 10^{-14}$ | $4.34 \times 10^{-9}$ |
| $2^{61} - 1$ | $10^6$ | $10^6$ | $4.34 \times 10^{-13}$ | $4.34 \times 10^{-7}$ |

With $p = 10^9 + 7$, $n = q = 10^5$, the union bound exceeds 1 and proves nothing. Two independent bases modulo $10^9 + 7$ bring it down to $q((n-1)/p)^2 \approx 1.0 \times 10^{-3}$, and one base modulo the Mersenne prime $2^{61} - 1$ to about $4 \times 10^{-9}$.

- **All pairs is worse than one pair.** If an algorithm needs all $N$ hashes of a set of distinct strings to be distinct, there are $\binom{N}{2}$ pairs, and the bound is $\binom{N}{2}(n-1)/p$. Even for an ideal random function the chance of some collision is about $1 - e^{-N^2/(2p)}$, by the [birthday paradox](/birthday-paradox/), so $p$ must be much larger than $N^2$.
- [Universal string hashing](/universal-string-hashing/) states the theorem as: the family $\{h_r\}$ is $((n-1)/p)$-almost universal on strings of length at most $n$.

## Tightness

The bound is reached for every $n$ such that $n - 1$ divides $p - 1$. The multiplicative group of $\mathbb{F}_p$ is [cyclic](/cyclic-group/) of order $p - 1$, so for each divisor $d$ of $p - 1$ the equation $t^d = 1$ has exactly $d$ solutions in $\mathbb{F}_p$. Over the alphabet $\{0, 1\}$ with codes 0 and 1, take $x = 1\,0^{d}$ and $y = 0^{d}\,1$, of length $n = d + 1$. Then $D(t) = t^{d} - 1$, and the strings collide for exactly $d = n - 1$ bases.

For $p = 13$ and $d = 4$, the strings $x = 10000$ and $y = 00001$ collide exactly for $r \in \{1, 5, 8, 12\}$, the four fourth roots of unity modulo 13. The probability is $4/13 = (n-1)/p$. With $d = p - 1$ and $n = p$, the strings collide for every nonzero base, by [Fermat's little theorem](/fermat-little-theorem/).

So no better bound holds for all pairs of strings of length $n$, even over a binary alphabet.

## History

The analysis by counting roots is the one-variable case of the lemma on polynomial identities proved by Schwartz (1980) and Zippel (1979), and the one-variable fact is much older. Karp and Rabin (1987) analyzed fingerprints of strings modulo a random prime, a different random choice with a bound from the number of prime factors. Thorup's lecture notes on hashing state the bound $d/p$ for strings that are polynomials of degree at most $d$, credit the method to Dietzfelbinger, Gil, Matias and Pippenger (1992), and show how to compose it with a universal hash into a smaller range. Pachocki and Radoszewski (2013) explained to the programming contest community where the bound applies, why the birthday paradox matters for some uses, and why a modulus $2^{64}$ fails.

## References
