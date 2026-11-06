---
tag: J5RM4H
kind: problem
slug: primality-proving
name: Primality proving
aliases:
- certified primality
- deterministic primality proof
area: number-theory/primality
level: advanced
summary: Decide with no error whether n is prime, and for a prime give a proof, ideally a certificate that is fast to check. Methods use factored parts of n - 1 or n + 1, elliptic curves, or AKS.
prereqs: [primality-testing, primality-certificate]
see_also: [pratt-certificate, pocklington-primality-test, proth-test, ecpp, aks-primality-test, apr-cl-primality-test, lucas-lehmer-test, probable-prime]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Chapter 4 (Sections 4.1 to 4.5, in particular Algorithm 4.1.7, Theorems 4.1.5, 4.1.6 and 4.1.9, Algorithm 4.2.7, Algorithm 4.3.4, Section 4.4.2, Algorithm 4.5.1 and Theorem 4.5.7) and Section 7.6 (Theorem 7.6.1, Algorithms 7.6.2 and 7.6.3, Section 7.6.3)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 4, Section 4.3 (Definition 4.34, Sections 4.3.1 to 4.3.4) and the chapter notes on Section 4.3
  - paper: doi:10.4007/annals.2004.160.781
    title: Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160 (2004)
    locator: pages 781 to 793
  - paper: doi:10.1137/0204018
    title: Vaughan R. Pratt, Every prime has a succinct certificate, SIAM Journal on Computing 4 (1975)
    locator: pages 214 to 220
  - paper: doi:10.4171/JEMS/861
    title: H. W. Lenstra Jr. and Carl Pomerance, Primality testing with Gaussian periods, Journal of the European Mathematical Society 21 (2019)
    locator: pages 1229 to 1269
---

Primality proving is the problem of deciding whether an integer $n$ is [prime](/prime-number/) with no chance of error, and of giving, for a prime, a proof of that fact. It differs from [primality testing](/primality-testing/) in the probabilistic sense, where a [probable prime](/probable-prime/) answer can be wrong. The strongest form asks for a [primality certificate](/primality-certificate/) that someone else can check much faster than it was found. Every prime has such a certificate of polynomial size (Pratt 1975), and the [AKS test](/aks-primality-test/) decides primality in deterministic polynomial time, but the methods used in practice are [ECPP](/ecpp/) for general numbers and tests based on $n - 1$ or $n + 1$ for numbers of special form.

## In plain words

A quick test can say that a large number is "almost certainly prime". For many uses that is enough, but sometimes one needs to know for sure. A proof of primality settles the question without any doubt. The best proofs also leave a record, a short list of numbers, that lets anyone check the result again quickly. Finding a proof is harder than running a quick test, and for numbers of a special shape, such as one more than a power of two times a small number, it is almost as easy. For numbers of no special shape the usual tool is a method built on elliptic curves, which can prove numbers with thousands of digits prime.

## Definition

**Input.** An integer $n \ge 2$, written in binary with $\ell = \lfloor \lg n \rfloor + 1$ digits.

**Output.** One of:

- "prime", together with a proof that $n$ is prime;
- "composite", together with a proof that $n$ is composite, such as a proper factor or a [compositeness witness](/compositeness-witness/).

Both answers must be right on every input. A *proof* in the weak sense is the transcript of a deterministic computation whose correctness is a theorem, such as a run of AKS. A proof in the strong sense is a *certificate*: a string $c$ of length polynomial in $\ell$ and a fixed checker $V$ that runs in time polynomial in $\ell$, accepts $(n, c)$ only if $n$ is prime, and accepts some $c$ for every prime $n$. HAC (Definition 4.34) calls a number shown prime by a primality proving algorithm a *provable prime*.

**Cost model.** The integers are of arbitrary precision, and costs are bit operations on a [multitape Turing machine](/multitape-turing-machine/), with schoolbook multiplication unless stated. Several bounds below hold only under heuristic assumptions or conjectures; each one says so.

## Variants

- **General numbers.** Prove a number of no special form prime. ECPP and the cyclotomy test [APR-CL](/apr-cl-primality-test/) are the practical methods; AKS is the one with a proven polynomial bound.
- **Numbers with a factored $n - 1$.** If a large part of $n - 1$ is factored, [Pocklington's test](/pocklington-primality-test/) and its refinements give a proof with a few exponentiations. [Proth's test](/proth-test/) and [Pepin's test](/pepin-test/) are special cases.
- **Numbers with a factored $n + 1$.** Lucas sequences give the analogous $n + 1$ test; the [Lucas-Lehmer test](/lucas-lehmer-test/) for Mersenne numbers $2^p - 1$ is the best known case (Crandall and Pomerance, Algorithm 4.2.7). Combined $n^2 - 1$ tests use factors of both.
- **With or without a certificate.** ECPP, Pratt and Pocklington produce certificates. The Jacobi sum test produces none that can be checked faster than running it again (HAC Section 4.3.3), and AKS is its own check.
- **Proving primes that one builds.** For cryptography, a prime can be built together with its certificate, which is much easier than proving a given number; see [random prime generation](/random-prime-generation/).
- **Zero-error randomized proving.** A Las Vegas algorithm that may run longer on unlucky random choices but never errs, such as the Goldwasser-Kilian and Adleman-Huang methods.

## Examples

| $n$ | answer | proof |
|---|---|---|
| $1279$ | prime | a [Pratt certificate](/pratt-certificate/): $1278 = 2 \cdot 3^2 \cdot 71$, base 3, and certificates for 3 and 71; 48 modular products to check |
| $1000003$ | prime | Pocklington with $F = 166667 > \sqrt n$ and base 2: $2^{n-1} \equiv 1$, $\gcd(2^6 - 1, n) = 1$ |
| $97$ | prime | Proth: $97 = 3 \cdot 2^5 + 1$ and $5^{48} \equiv -1 \pmod{97}$ |
| $65$ | composite | Proth with base 3: $\left(\frac{3}{65}\right) = -1$ but $3^{32} \equiv 61 \not\equiv -1 \pmod{65}$ |
| $2^{89} - 1$ | prime | an ECPP chain through $p_2 = 115836285129447871$ and $p_3 = 567220573$ (Crandall and Pomerance, Section 7.6.2), or the Lucas-Lehmer test |
| $2^{32} + 1$ | composite | the factor $641$; Pepin's test with base 3 also shows it without a factor |
| $3 \cdot 2^{534} + 1$ | prime | Proth's test with one exponentiation; it has 162 decimal digits |

The rows for $1279$, $1000003$, $97$ and $65$ are worked out on the pages of the methods. The last row shows the gap between special and general numbers: a 162-digit Proth number takes one power to prove, while a 162-digit number of no special form needs ECPP or APR-CL.

## Known algorithms

With $\ell$ the bit length of $n$:

- **[Trial division](/trial-division/).** Divides by every $d \le \sqrt n$. A proof, but it takes $2^{\ell/2}$ steps. It is the base case of the recursive methods.
- **Lucas and Pratt.** With the full factorization of $n - 1$, one base of order $n - 1$ proves $n$ prime; the [Lucas primality test](/lucas-primality-test/). Recursing on the factors gives the Pratt certificate, of $O(\ell^2)$ bits, checked with fewer than $2 \lg^2 n$ products (Crandall and Pomerance, Theorem 4.1.9).
- **The $n - 1$ test** (Crandall and Pomerance, Algorithm 4.1.7). A factored part $F \ge n^{1/2}$ suffices (Pocklington); $F \ge n^{1/3}$ with an extra square test (Brillhart, Lehmer and Selfridge, Theorem 4.1.5); and $F \ge n^{3/10}$ (Konyagin and Pomerance, Theorem 4.1.6). The cost is a few exponentiations once $F$ is known.
- **The $n + 1$ and $n^2 - 1$ tests** (Crandall and Pomerance, Section 4.2). The same with Lucas sequences and factors of $n + 1$, or of both.
- **The finite field test** (Crandall and Pomerance, Algorithm 4.3.4). Uses a factored divisor $F \ge n^{1/2}$ of $n^I - 1$ for a suitable $I$, which always exists for a small $I$, and works in an extension ring.
- **Gauss and Jacobi sums: APR-CL** (Crandall and Pomerance, Section 4.4; HAC Section 4.3.3). Deterministic, in time $(\ln n)^{c \ln \ln \ln n}$ for a constant $c$, which is just above polynomial. It gives no short certificate.
- **Goldwasser-Kilian** (Crandall and Pomerance, Algorithm 7.6.2). Elliptic curves with random parameters and point counting; expected polynomial time for most primes, and for all primes under a conjecture on primes in short intervals. HAC (chapter notes on Section 4.3) gives $O((\ln n)^{11})$ expected bit operations for most inputs.
- **Adleman-Huang.** Hyperelliptic curves of genus 2 give expected polynomial time for every prime, so PRIMES is in RP (HAC, chapter notes on Section 4.3).
- **Atkin-Morain ECPP** (Crandall and Pomerance, Algorithm 7.6.3; HAC Section 4.3.4). Curves with complex multiplication, whose orders are known in advance. Heuristic $O((\ln n)^{5+\epsilon})$ bit operations, and $O((\ln n)^{4+\epsilon})$ for the fastECPP variant (Crandall and Pomerance, Section 7.6.3); HAC states a heuristic $O((\ln n)^{6+\epsilon})$. Not proved, but excellent in practice, and it produces a certificate.
- **AKS** (Agrawal, Kayal and Saxena; Crandall and Pomerance, Algorithm 4.5.1). Deterministic and unconditional, with a polynomial bound. The published analysis gives $\tilde O(\ell^{10.5})$, and the Gaussian period version of Lenstra and Pomerance gives $\tilde O(\ell^{6})$. It is much slower than ECPP in practice.

## Bounds

**Existence of short proofs.** Every prime $n$ has a Pratt certificate with fewer than $\lg n$ entries, of $O(\ell^2)$ bits in all, checked in $O(\ell^4)$ bit operations (Pratt 1975; Crandall and Pomerance, Theorem 4.1.9). Pomerance (1987) showed that a proof with only $O(\ell)$ modular products exists, using elliptic curves (Crandall and Pomerance, remark after Theorem 4.1.9). So PRIMES is in [NP](/np/), and with factors as certificates of compositeness, in NP and [co-NP](/co-np/) together.

**Deterministic time.** PRIMES is in [P](/p/) (AKS). The best proven bound is $\tilde O(\ell^6)$, by Lenstra and Pomerance.

**Randomized time with no error.** The Adleman-Huang method and the [Miller-Rabin test](/miller-rabin/) together put PRIMES in RP and co-RP, so in [ZPP](/zpp/): a Las Vegas algorithm proves either answer in expected polynomial time.

**Heuristic time.** The fastest practical general method, fastECPP, runs in heuristic $O((\ln n)^{4+\epsilon})$ bit operations; no proof of this bound is known.

**Lower bound.** Any correct method must read all of $n$, so $\Omega(\ell)$; nothing better is known.

**Finding versus checking.** For a certificate method the cost of finding can far exceed the cost of checking. A Pratt certificate needs the factorization of $n - 1$ and of the numbers below it in the tree, which is not known to be possible in polynomial time; checking it is polynomial.

## Reductions

- **Proving reduces to partial factoring of $n - 1$.** With a factored part $F \ge n^{1/2}$ (or $n^{1/3}$, or $n^{3/10}$) of $n - 1$, a few exponentiations prove $n$ prime or composite (Crandall and Pomerance, Algorithm 4.1.7). The same holds for $n + 1$.
- **ECPP reduces $n$ to a smaller prime.** One step of Theorem 7.6.1 replaces the question "is $n$ prime?" by "is $q$ prime?" for a $q$ between about $\sqrt n$ and $n/2$. About $\ell$ steps bring $q$ down to trial division size.
- **Primality testing reduces to proving.** A proving algorithm answers the decision problem with no error. The converse direction is the practical workflow: a fast probable prime test first, then a proof only for numbers that pass.
- **Not to factoring.** Proving $n$ prime does not need the factorization of $n$, and a proof of compositeness from a witness does not give a factor.

## Applications

- **Records and tables.** Large primes found in searches are proved prime, with ECPP for general numbers and with special tests for forms such as $k \cdot 2^m + 1$ and $2^p - 1$; the certificates let others confirm them.
- **Complete factorizations.** A factorization is complete only when each factor is proved prime. The tables of factorizations of $2^m \pm 1$ needed exactly the $n - 1$ and $n + 1$ criteria of Brillhart, Lehmer and Selfridge.
- **Cryptographic parameters.** Some standards and users want primes that are proved, not only probable; building the prime with its certificate, as in Maurer's method, makes this cheap. See [random prime generation](/random-prime-generation/).
- **Trusted checking.** A short certificate lets a small, simple checker confirm the output of large and complex software.

## References
