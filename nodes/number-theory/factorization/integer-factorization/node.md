---
tag: PEWPF5
kind: problem
slug: integer-factorization
name: Integer factorization
aliases:
- prime factorization
- factoring
area: number-theory/factorization
level: intro
summary: Given an integer N of n binary digits, find its prime factors. No algorithm in time polynomial in n is known; the security of RSA rests on this.
prereqs: [prime-number, fundamental-theorem-of-arithmetic, divisibility]
see_also: [trial-division, pollard-rho, quadratic-sieve, general-number-field-sieve, elliptic-curve-factorization, primality-testing, rsa-cryptosystem, shor-algorithm]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 1.1.1, Fundamental theorem and fundamental problem; Chapter 5, Exponential factoring algorithms; Chapter 6, Subexponential factoring algorithms (Section 6.3, Rigorous factoring, pages 301 to 302); Section 7.4, Elliptic curve method
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.5.4, Factoring into primes
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Chapter 8, Factoring in the dark ages, and Chapter 10, Modern factoring methods
  - paper: "Carl Pomerance, A tale of two sieves, Notices of the American Mathematical Society 43(12), 1996"
    locator: pages 1473 to 1485 (the history of the quadratic and number field sieves, and the L-notation for their running times)
  - paper: "Arjen K. Lenstra and Hendrik W. Lenstra Jr. (editors), The development of the number field sieve, Lecture Notes in Mathematics 1554, Springer, 1993"
    locator: the introduction and the paper of Buhler, Lenstra and Pomerance (the heuristic bound L_N[1/3, (64/9)^(1/3)])
  - paper: "Hendrik W. Lenstra Jr. and Carl Pomerance, A rigorous time bound for factoring integers, Journal of the American Mathematical Society 5(3), 1992"
    locator: pages 483 to 516 (the expected time L_N[1/2, 1 + o(1)], proved)
  - paper: "David Harvey, An exponent one-fifth algorithm for deterministic integer factorisation, Mathematics of Computation 90(332), 2021"
    locator: the main theorem (deterministic time O(N^(1/5) (log N)^(16/5)), proved); also arXiv 2010.05450
  - paper: "Michael O. Rabin, Digitalized signatures and public-key functions as intractable as factorization, MIT Laboratory for Computer Science, Technical Report MIT/LCS/TR-212, 1979"
    locator: the reduction of factoring to the extraction of square roots modulo N
  - url: https://en.wikipedia.org/wiki/RSA_numbers
    locator: Wikipedia, RSA numbers, the entries RSA-129 and RSA-250 (the dates and methods of the factorizations)
---

Integer factorization is the problem of writing a positive integer $N$ as a product of [prime numbers](/prime-number/). The [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/) says that this product exists and is unique up to the order of the factors, so the problem is to find it. The size of the input is the number of binary digits $n = \lfloor \lg N \rfloor + 1$, and no classical algorithm is known that runs in time polynomial in $n$. The best known method, the [general number field sieve](/general-number-field-sieve/), takes time $\exp\big(O(n^{1/3} (\log n)^{2/3})\big)$ by a heuristic analysis, and the security of the [RSA cryptosystem](/rsa-cryptosystem/) depends on this gap.

## In plain words

Each whole number larger than one is a product of primes, and only one such product gives it. For example, three hundred sixty is two times two times two times three times three times five. The factorization problem asks for this list of primes.

The opposite direction is easy: to multiply two primes of a hundred digits takes a computer much less than a second. To find the two primes from their product is very hard. The best methods known today take years of work on many computers for a product of about two hundred fifty digits.

Testing whether a number is prime is a different problem, and it is easy. A fast test can say that a number is not prime without finding any of its factors.

## Definition

**Input.** An integer $N \ge 1$, written in binary with $n = \lfloor \lg N \rfloor + 1$ digits.

**Output.** The list of primes $p_1 \le p_2 \le \cdots \le p_k$ with

$$N = p_1 p_2 \cdots p_k .$$

For $N = 1$ the list is empty ($k = 0$). By the fundamental theorem of arithmetic the list is unique. We often write it as $N = \prod_{i=1}^{r} q_i^{e_i}$ with distinct primes $q_1 < \cdots < q_r$ and exponents $e_i \ge 1$.

**Cost model.** $N$ is an arbitrary-precision integer. The running time is measured as a function of the bit length $n$, either in bit operations or in arithmetic operations on integers of $O(n)$ bits; one such operation costs $O(n^2)$ bit operations with schoolbook arithmetic and $O(n \log n)$ with the fastest [integer multiplication](/integer-multiplication/). A running time that is polynomial in $N$, such as $N^{1/2}$, is exponential in the input size $n$.

**L-notation.** The running times of the subexponential methods are written with

$$L_N[\alpha, c] = \exp\Big( (c + o(1)) \, (\ln N)^{\alpha} \, (\ln \ln N)^{1 - \alpha} \Big), \qquad 0 \le \alpha \le 1,\ c > 0,$$

where $o(1)$ tends to $0$ as $N \to \infty$. For $\alpha = 0$ it is $(\ln N)^{c + o(1)}$, a polynomial in $n$. For $\alpha = 1$ it is $N^{c + o(1)}$, exponential in $n$. Values of $\alpha$ strictly between give subexponential time. Many texts write $L_n$ for this with $n$ the number itself; here the subscript is the number $N$ and $n$ is its bit length.

## Variants

- **Splitting.** Given a composite $N$, find one divisor $d$ with $1 < d < N$. A complete factorization follows by splitting the parts again, with a [primality test](/primality-testing/) to stop at primes. A composite $N$ has at most $\lg N$ prime factors with multiplicity, so at most $\lg N - 1$ splits are needed, and the complete problem costs at most $O(n)$ times the cost of splitting, plus the primality tests.
- **Decision version.** Given $N$ and $k$, does $N$ have a divisor $d$ with $1 < d \le k$? Binary search on $k$ with this oracle finds the least prime factor with $O(n)$ queries.
- **Smallest prime factor.** Find the least prime factor $p$. Methods such as [trial division](/trial-division/), [Pollard's rho](/pollard-rho/) and the [elliptic curve method](/elliptic-curve-factorization/) have a cost that depends on $p$, not on $N$, so they find small factors of very large numbers.
- **Semiprimes.** $N = pq$ with two primes of about the same size. This is the hard case for most methods and the case of RSA moduli. The [RSA problem](/rsa-problem/) asks for $e$-th roots modulo such an $N$, and factoring $N$ solves it.
- **Special forms.** $N = r^e \pm s$ with small $r$ and $s$, such as the Fermat numbers $2^{2^k} + 1$ and the Mersenne numbers $2^m - 1$. The [special number field sieve](/special-number-field-sieve/) is faster on them.
- **Partial factorization.** Find all prime factors below a bound $B$, or decide whether $N$ is [$B$-smooth](/smooth-number/). The sieve methods need this step many times on small numbers.
- **Factoring with extra information.** Given a multiple of the [Carmichael function](/carmichael-function/) $\lambda(N)$, such as $\varphi(N)$ or $ed - 1$ for an RSA key pair, or given an oracle for square roots modulo $N$, the problem becomes easy for randomized algorithms (see Reductions).

## Examples

| $N$ | factorization | remark |
|---|---|---|
| $1$ | empty product | $k = 0$ |
| $360$ | $2^3 \cdot 3^2 \cdot 5$ | small factors, found by trial division |
| $561$ | $3 \cdot 11 \cdot 17$ | the least [Carmichael number](/carmichael-number/) |
| $1729$ | $7 \cdot 13 \cdot 19$ | a Carmichael number |
| $10403$ | $101 \cdot 103$ | two close primes; [Fermat's method](/fermat-factorization/) finds them in one step |
| $600851475143$ | $71 \cdot 839 \cdot 1471 \cdot 6857$ | all factors below $10^4$ |
| $2^{32} + 1$ | $641 \cdot 6700417$ | the Fermat number $F_5$ |
| $2^{64} + 1$ | $274177 \cdot 67280421310721$ | the Fermat number $F_6$ |
| $2^{67} - 1$ | $193707721 \cdot 761838257287$ | the Mersenne number $M_{67}$ |

Euler found the factor $641$ of $F_5$. Today a laptop finds each of these factorizations in a fraction of a second. The record for a general number is RSA-250, a semiprime of 250 decimal digits (829 bits), factored with the general number field sieve in 2020.

## Known algorithms

Below, $N$ is the input, $n$ its bit length and $p$ its least prime factor. "Proved" means a theorem. "Heuristic" means an analysis that uses unproved assumptions, such as that certain numbers behave like random numbers with respect to smoothness.

- **Exponential, deterministic.** [Trial division](/trial-division/) and [wheel factorization](/wheel-factorization/): $O(\min(p, N^{1/2}))$ divisions, proved. [Fermat's method](/fermat-factorization/): fast when the two factors are close, $O(N^{1/2})$ steps in the worst case. [Lehman's method](/lehman-factorization/): $O(N^{1/3})$ arithmetic operations, proved. [Hart's one line factoring](/hart-one-line-factorization/): about $N^{1/3}$ steps, heuristic. [Pollard-Strassen](/pollard-strassen/): $N^{1/4 + o(1)}$ bit operations, proved. Harvey (2021): $O(N^{1/5} (\log N)^{16/5})$ bit operations, proved.
- **Exponential, randomized or heuristic.** [Pollard's rho](/pollard-rho/) and [Brent's variant](/brent-pollard-rho/): $O(p^{1/2})$ arithmetic operations, heuristic. [SQUFOF](/shanks-squfof/): $O(N^{1/4})$ steps, heuristic. [Pollard's p - 1](/pollard-p-minus-1/) and [Williams' p + 1](/williams-p-plus-1/): fast only when $p - 1$ or $p + 1$ is smooth.
- **Subexponential.** [Dixon's random squares](/dixon-random-squares/): $L_N[1/2, 2\sqrt{2}]$ expected, proved, and $L_N[1/2, \sqrt{4/3}]$ for the improved variant of Vallée. Lenstra and Pomerance (1992): $L_N[1/2, 1]$ expected, proved. [CFRAC](/continued-fraction-factorization/): $L_N[1/2, \sqrt{2}]$, heuristic. The [quadratic sieve](/quadratic-sieve/) and [MPQS](/multiple-polynomial-quadratic-sieve/): $L_N[1/2, 1]$, heuristic. The [elliptic curve method](/elliptic-curve-factorization/): $L_p[1/2, \sqrt{2}]$ arithmetic operations to find $p$, heuristic. The [general number field sieve](/general-number-field-sieve/): $L_N[1/3, (64/9)^{1/3}]$, heuristic, with $(64/9)^{1/3} \approx 1.923$. The [special number field sieve](/special-number-field-sieve/): $L_N[1/3, (32/9)^{1/3}]$, heuristic, on numbers of special form.
- **Quantum.** [Shor's algorithm](/shor-algorithm/) factors $N$ in time polynomial in $n$ on a quantum computer, with bounded error.

The sieve methods share one plan: find a [congruence of squares](/congruence-of-squares/) $x^2 \equiv y^2 \pmod N$ by [relation collection](/relation-collection/) over [smooth numbers](/smooth-number/), then take $\gcd(x - y, N)$.

## Bounds

**Upper bounds.** The best proved deterministic bound is the one of Harvey above, improved by a factor $(\log \log N)^{3/5}$ by Harvey and Hittmeir (2022). The best proved randomized bound is $L_N[1/2, 1]$ expected, by Lenstra and Pomerance. The best heuristic bound is $L_N[1/3, (64/9)^{1/3}]$ for the number field sieve; Coppersmith's variant with several number fields lowers the constant to about $1.902$.

**Lower bounds.** No lower bound better than $\Omega(n)$, the time to read the input, is known for any general model of computation. Factoring is not known to be NP-hard, and it is unlikely to be, by the next fact.

**Complexity class.** The decision version (does $N$ have a divisor $d$ with $1 < d \le k$?) is in $\mathrm{NP} \cap \mathrm{coNP}$. A certificate for both the answer yes and the answer no is the full factorization $N = p_1 \cdots p_k$, together with a proof that each $p_i$ is prime; such proofs exist with size polynomial in $n$ (Pratt certificates), and today the primality of each $p_i$ can also be checked in polynomial time by the AKS test. A verifier multiplies the factors, checks the primes and compares the least of them with $k$. So if the decision version were NP-complete, then $\mathrm{NP} = \mathrm{coNP}$.

## Reductions

- **Square roots modulo $N$ (Rabin).** Assume an oracle that, given a square $a$ modulo $N$, returns some $y$ with $y^2 \equiv a$. Let $N$ be odd and not a prime power, so that it has $r \ge 2$ distinct prime factors. Pick $x$ uniformly in $[1, N - 1]$. If $\gcd(x, N) > 1$, it is a factor. Otherwise each square has exactly $2^r$ square roots, by the [Chinese remainder theorem](/chinese-remainder-theorem/), and the oracle answer $y$ for $a = x^2 \bmod N$ does not depend on which of them $x$ was. So with probability $1 - 2/2^r \ge 1/2$, $y \not\equiv \pm x$, and then $\gcd(x - y, N)$ is a proper factor. The expected number of oracle calls is at most $2$.
- **A multiple of $\lambda(N)$.** Given $M$ with $\lambda(N) \mid M$ (for example $M = \varphi(N)$, or $M = ed - 1$ from an RSA key pair), write $M = 2^s t$ with $t$ odd. For a random $a$, the sequence $a^t, a^{2t}, \dots, a^{2^s t}$ modulo $N$ ends in $1$. If a term before the first $1$ is not $-1$, it is a [nontrivial square root of one](/nontrivial-square-root-of-one/) $b$, and $\gcd(b - 1, N)$ is a proper factor. For odd $N$ that is not a prime power, this happens for at least half of the $a$ coprime to $N$; the argument is the one of the [Miller-Rabin test](/miller-rabin/). So knowing $\varphi(N)$ is as hard as factoring $N$, under randomized reductions.
- **Order finding.** Factoring reduces to finding the [multiplicative order](/multiplicative-order/) of random elements modulo $N$, by the previous reduction. This is the reduction that [Shor's algorithm](/shor-algorithm/) uses ([factoring to order finding](/factoring-to-order-finding/)).
- **From factoring.** Given the factorization, $\varphi(N)$, $\lambda(N)$, square roots modulo $N$ ([Tonelli-Shanks](/tonelli-shanks/) for each prime, then [CRT](/chinese-remainder-theorem/)) and $e$-th roots for RSA are all computed in polynomial time. So these problems are equivalent to factoring, under randomized polynomial-time reductions, except the RSA problem, for which only the direction "factoring solves RSA" is known.

## Applications

- **Cryptography.** RSA and the Rabin cryptosystem are secure only if factoring their modulus is hard. Key sizes follow the running time of the number field sieve: 2048-bit moduli are the common choice today.
- **Arithmetic functions.** The [divisor function](/divisor-function/), [Euler's totient](/euler-totient/) and the [Möbius function](/mobius-function/) are easy to compute from the factorization, and no faster general method is known for them.
- **Group computations.** A [primitive root](/primitive-root/) modulo $p$ and the order of an element are found from the factorization of $p - 1$. [Pohlig-Hellman](/pohlig-hellman/) for discrete logarithms needs the factorization of the group order.
- **Primality proofs.** The [Pocklington test](/pocklington-primality-test/) and the [Lucas test](/lucas-primality-test/) prove $N$ prime from a partial factorization of $N - 1$.
- **Number theory research.** Tables of factorizations of $b^k \pm 1$ (the Cunningham project) and of Fermat numbers have been a test bed for each new method.

## References
