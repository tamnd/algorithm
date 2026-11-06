---
tag: CE00Z2
kind: problem
slug: random-prime-generation
name: Random prime generation
aliases:
- prime generation
- generating random primes
area: number-theory/primality
level: core
summary: Output a random prime of a given bit length, or below a given bound, with a known bound on the chance that the output is composite.
prereqs: [prime-number, primality-testing, miller-rabin]
see_also: [probable-prime, prime-number-theorem, safe-prime, sophie-germain-prime, primality-certificate, rsa-cryptosystem, trial-division, miller-rabin-error-bound]
sources:
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 9.4 (Algorithm RP) and Section 10.3 (10.3.1 to 10.3.3, inequalities 10.5 to 10.7, Theorems 10.4 and 10.6 and the tables after them)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 4, Section 4.4 (Algorithm 4.44, Notes 4.45, 4.47, 4.49 and 4.51, Algorithms 4.53, 4.56 and 4.62) and Section 4.6.1 (Algorithm 4.86)
  - paper: doi:10.1090/S0025-5718-1993-1189518-9
    title: Ivan Damgard, Peter Landrock and Carl Pomerance, Average case error estimates for the strong probable prime test, Mathematics of Computation 61 (1993)
    locator: pages 177 to 194
  - paper: doi:10.1007/BF00202269
    title: Ueli M. Maurer, Fast generation of prime numbers and secure public-key cryptographic parameters, Journal of Cryptology 8 (1995)
    locator: pages 123 to 155
  - paper: doi:10.1090/S0025-5718-2011-02542-1
    title: Terence Tao, Ernest Croot and Harald Helfgott, Deterministic methods to find primes, Mathematics of Computation 81 (2012)
    locator: pages 1233 to 1246 (abstract, the N^(1/2+o(1)) bound for deterministic search)
---

Random prime generation is the problem of outputting a random [prime](/prime-number/) of a given bit length, or a random prime below a given bound, so that each prime in the range is about equally likely. The standard solution draws random candidates until one passes a [primality test](/primality-testing/). It works because primes are dense: by the [prime number theorem](/prime-number-theorem/), about one $\ell$-bit integer in $\ell \ln 2$ is prime. With the [Miller-Rabin test](/miller-rabin/) the output is a [probable prime](/probable-prime/), and the problem then includes a bound on the chance that the output is composite.

## In plain words

A program needs a large prime that nobody can guess, for example to make an encryption key. Primes are common enough that a random odd number of a few hundred digits is prime about once in a few hundred tries. So the program picks a random odd number of the right size, throws it away if a small prime divides it, and runs a fast probabilistic test on the survivors. The first number that passes is the output. The test never rejects a prime, so the only risk is to output a composite, and a few rounds of the test make that risk far smaller than the risk of a hardware fault. When a proof is needed, a different method builds the prime together with a certificate.

## Definition

The cost model is a bit-operation model: candidates have bit length $\ell$, arithmetic on them costs $O(\ell^2)$ for a multiplication with schoolbook methods, and each random bit costs $O(1)$.

**Uniform prime below a bound.** Input: an integer $m \ge 2$ and an error parameter. Output: a prime $p \le m$. Each prime $p \le m$ should be output with probability close to $1/\pi(m)$, where $\pi$ is the [prime-counting function](/prime-counting-function/).

**Random $\ell$-bit prime.** Input: an integer $\ell \ge 2$ and an error parameter. Output: a prime $p$ with $2^{\ell - 1} \le p < 2^\ell$, each such prime about equally likely.

A Las Vegas solution outputs only primes, and its running time is a random variable. A Monte Carlo solution may output a composite, with probability at most a stated $\varepsilon$; Shoup writes $\gamma(m, k)$ for this probability when the test is $k$ rounds of Miller-Rabin and the range is $\{2, \ldots, m\}$, and $\gamma'(\ell, k)$ for the $\ell$-bit version. The error is one-sided in this sense: a prime is never rejected, so the error only lets a composite through. The distribution of a good generator, conditioned on its output being prime, is uniform over the primes in the range (Shoup, Section 10.3.1).

## Variants

- **Fixed bit length** (Shoup, Section 10.3.3; HAC Algorithm 4.44). Candidates are random odd $\ell$-bit integers, usually with the top bit set so that the product of two such primes has the expected length.
- **Provable primes.** The output comes with a [primality certificate](/primality-certificate/). Maurer's algorithm (HAC Algorithm 4.62) builds a prime $n = 2Rq + 1$ from a smaller random provable prime $q$ with $q > R$ and proves $n$ prime with [Pocklington's theorem](/pocklington-primality-test/). Its cost is close to that of a probable prime (HAC Note 4.64).
- **Primes with side conditions.** [Safe primes](/safe-prime/) $p = 2q + 1$ with $q$ prime (HAC Algorithm 4.86), so that $q$ is a [Sophie Germain prime](/sophie-germain-prime/); "strong primes" for RSA with large prime factors in $p - 1$ and $p + 1$ (Gordon's method, HAC Algorithm 4.53); and [DSA](/dsa/) pairs $p, q$ with $q \mid p - 1$ (HAC Algorithm 4.56).
- **Incremental search** (HAC Note 4.51). Pick one random odd $n_0$ and test $n_0, n_0 + 2, n_0 + 4, \ldots$ in turn. It uses fewer random bits and allows sieving of the whole run of candidates at once, but the output is not uniform: a prime that follows a long gap is more likely.
- **Deterministic construction.** Output a prime larger than a given $N$ with no randomness at all. This is a different problem with no known efficient solution; see Bounds.

## Examples

**Density.** There are $3030$ primes in $[2^{15}, 2^{16})$, among $16384$ odd numbers, so about one odd 16-bit number in $5.4$ is prime. For $\ell = 1024$, about one odd candidate in $1024 \ln 2 / 2 \approx 355$ is prime.

**Trial division first.** The fraction of odd integers with no odd prime factor up to $B$ is about $\prod_{3 \le p \le B} (1 - 1/p)$. For $B = 256$ this product is $0.2007$, so trial division by the odd primes below 256 throws away about 80 percent of the candidates before any exponentiation (HAC, Section 4.4.1). For $B = 2^{16}$ the product is $0.1012$.

**Error bounds.** One Miller-Rabin round on a random $\ell$-bit candidate is much better than the worst case $1/4$. Shoup's table, from Damgard, Landrock and Pomerance, gives these lower bounds on $-\log_2 \gamma'(\ell, k)$:

| $k$ | $\ell = 200$ | $\ell = 300$ | $\ell = 400$ | $\ell = 500$ | $\ell = 600$ |
|---|---|---|---|---|---|
| 1 | 11 | 19 | 37 | 56 | 75 |
| 2 | 25 | 33 | 46 | 63 | 82 |
| 3 | 34 | 44 | 55 | 70 | 88 |
| 4 | 41 | 53 | 63 | 78 | 95 |
| 5 | 47 | 60 | 72 | 85 | 102 |

So one round on a random 600-bit candidate already gives an error below $2^{-75}$. HAC Note 4.49 states that 3 rounds give error at most $2^{-80}$ for 1000-bit candidates.

**Bias of incremental search.** Take $\ell = 8$: the primes in $[129, 255]$ are $131, 137, \ldots, 251$, 23 in all. Start at a uniform odd $n_0$ in $[129, 251]$ (62 choices) and take the first prime $\ge n_0$. Then $211$ and $223$ are each output for 6 starts, because the gaps before them are 12, while $139$, $151$, $181$, $193$, $199$, $229$ and $241$ are each output for only 1 start. A uniform generator gives each of the 23 primes probability $1/23$.

## Known algorithms

**Sample and test** (Shoup, Algorithm RP; HAC Algorithm 4.44).

1. Pick $n$ uniformly from the range (random odd $\ell$-bit integers, or $\{2, \ldots, m\}$).
2. If an odd prime $p \le B$ divides $n$ and $p \ne n$, go to step 1.
3. Run $k$ rounds of Miller-Rabin with random bases. If all pass, output $n$; else go to step 1.

With trial division bound $B$ and $k$ rounds:

- **Error.** Bayes' rule gives $\gamma(m, k) \le 4^{-k} (m - 1)/\pi(m)$ (Shoup, inequality 10.5), which is $O(4^{-k} \ell)$. The bound $4^{-k}$ alone is wrong in general, because it bounds $P[\text{pass} \mid \text{composite}]$ and not $P[\text{composite} \mid \text{pass}]$ (HAC Note 4.47). The average-case bounds of Damgard, Landrock and Pomerance are much stronger (Shoup, Theorem 10.6: $\gamma'(\ell, 1) \le \ell^2 4^{2 - \sqrt \ell}$).
- **Expected time.** $O(\ell)$ candidates on average, by Chebyshev's bound $\pi(m) = \Theta(m / \log m)$. A composite candidate costs $4/3$ rounds on average because each round rejects it with probability at least $3/4$; only the final prime costs all $k$ rounds. The total expected time is $O(\ell^4 + k \ell^3)$ with schoolbook arithmetic, and $O(\ell^4 / \log \ell + k \ell^3)$ with trial division up to a suitable small bound (Shoup, Sections 10.3.1 and 10.3.3).

**Generate and prove.** Run the sample-and-test loop, then prove the output prime with [ECPP](/ecpp/), or build a provable prime directly with Maurer's recursion, whose certificate is a chain of Pocklington steps.

**Special forms.** Search over $k$ for a prime $k \cdot 2^m + 1$ and prove it with the [Proth test](/proth-test/), at the cost of one exponentiation. The output is not random in the cryptographic sense, but it is a proven prime of a chosen size.

## Bounds

- **Density, unconditional.** By Chebyshev's theorem there is a constant $c > 0$ with $\pi(2^\ell) - \pi(2^{\ell - 1}) \ge c 2^{\ell - 1} / \ell$ for all $\ell \ge 2$ (Shoup, Section 10.3.3), so the expected number of candidates is $O(\ell)$ without any conjecture.
- **Randomness.** A generator whose output is uniform over the $\ell$-bit primes must use, on average, at least $\log_2(\pi(2^\ell) - \pi(2^{\ell-1})) = \ell - \log_2 \ell + O(1)$ random bits, the entropy of its output. Sample and test uses $O(\ell^2)$ expected bits for the candidates, plus the bits for the bases.
- **Deterministic search.** Testing $N + 1, N + 2, \ldots$ with the [AKS test](/aks-primality-test/) finds a prime above $N$, but its running time depends on the [gap](/prime-gaps/) after $N$, and the proven bounds on gaps are a power of $N$. The best unconditional deterministic method known runs in time $N^{1/2 + o(1)}$ (Tao, Croot and Helfgott), which is exponential in $\log N$. Whether a prime of $\ell$ bits can be found deterministically in time polynomial in $\ell$ is open.

## Reductions

- **To primality testing.** Sample and test reduces generation to $O(\ell)$ expected calls of a primality test, plus the density bound. A deterministic polynomial test such as AKS gives a Las Vegas generator with no error in the output.
- **From generation to related objects.** A safe prime generator calls a prime generator for $q$ and a test for $2q + 1$; a provable prime generator calls itself on a smaller size (Maurer). The [RSA](/rsa-cryptosystem/) key generator calls the $\ell$-bit generator twice.

## Applications

- [RSA](/rsa-cryptosystem/) key generation, which needs two independent secret primes of the same length.
- [Diffie-Hellman](/diffie-hellman/), [ElGamal](/elgamal-encryption/) and [DSA](/dsa/) parameters, which need primes $p$ with a known large prime factor of $p - 1$, such as safe primes.
- Hashing and fingerprinting modulo a random prime, as in [Rabin-Karp](/rabin-karp/) string matching and [polynomial identity testing](/polynomial-identity-testing/), where a random prime keeps an adversary from choosing inputs that collide.

## References
