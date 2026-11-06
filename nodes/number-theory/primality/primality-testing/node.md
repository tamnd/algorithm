---
tag: QCSXFP
kind: problem
slug: primality-testing
name: Primality testing
aliases:
- PRIMES problem
- primality test
area: number-theory/primality
level: intro
summary: Decide whether a given integer n is prime.
prereqs: [prime-number, divisibility, modular-exponentiation]
see_also: [trial-division, miller-rabin, solovay-strassen, baillie-psw, aks-primality-test, primality-proving, probable-prime, integer-factorization]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.8, Primality testing (the density of primes, pseudoprimality testing and the Miller-Rabin test)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Chapter 3, Recognizing primes and composites, and Chapter 4, Primality proving (Section 4.5, the test of Agrawal, Kayal and Saxena)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Chapter 10, Probabilistic primality testing (Sections 10.1 and 10.2, and the notes of Section 10.5 on Miller and Bach), and Chapter 21, Deterministic primality testing
  - paper: doi:10.4007/annals.2004.160.781
    title: Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160 (2004)
    locator: pages 781 to 793
  - paper: doi:10.4171/JEMS/861
    title: H. W. Lenstra Jr. and Carl Pomerance, Primality testing with Gaussian periods, Journal of the European Mathematical Society 21(4) (2019)
    locator: pages 1229 to 1269 (the bound (log n)^6 (2 + log log n)^c)
  - paper: doi:10.1137/0204018
    title: Vaughan R. Pratt, Every prime has a succinct certificate, SIAM Journal on Computing 4(3) (1975)
    locator: pages 214 to 220
  - paper: doi:10.1137/0206006
    title: Robert Solovay and Volker Strassen, A fast Monte-Carlo test for primality, SIAM Journal on Computing 6(1) (1977)
    locator: pages 84 to 85
  - paper: doi:10.1016/S0022-0000(76)80043-8
    title: Gary L. Miller, Riemann's hypothesis and tests for primality, Journal of Computer and System Sciences 13 (1976)
    locator: pages 300 to 317
  - paper: doi:10.1016/0022-314X(80)90084-0
    title: Michael O. Rabin, Probabilistic algorithm for testing primality, Journal of Number Theory 12 (1980)
    locator: pages 128 to 138
  - paper: doi:10.1090/S0025-5718-1980-0572872-7
    title: Carl Pomerance, J. L. Selfridge and Samuel S. Wagstaff Jr., The pseudoprimes to 25·10^9, Mathematics of Computation 35 (1980)
    locator: pages 1003 to 1026 (the smallest strong pseudoprimes to several bases, among them 3215031751)
  - paper: "Leonard M. Adleman and Ming-Deh A. Huang, Primality Testing and Abelian Varieties over Finite Fields, Lecture Notes in Mathematics 1512, Springer, 1992"
    locator: the whole monograph (a randomized polynomial-time test that proves primality, so PRIMES is in RP)
---

Primality testing is the problem of deciding whether a given integer $n$ is a [prime number](/prime-number/). The input is the binary form of $n$, so the size of the input is the number of binary digits $\ell \approx \lg n$, not $n$ itself. [Trial division](/trial-division/) takes about $\sqrt n = 2^{\ell/2}$ steps, which is exponential in $\ell$. Randomized tests such as [Miller-Rabin](/miller-rabin/) take $O(\ell^3)$ bit operations per round, and the [AKS test](/aks-primality-test/) of 2002 showed that the problem is in the class [P](/p/) without any assumption.

## In plain words

You are given a whole number and must say whether it is prime: whether no smaller number other than one divides it evenly. The obvious way is to try each possible divisor up to the square root. This is fine for numbers of ten or twelve digits. It is hopeless for numbers of a few hundred digits, the size used in cryptography, because the number of divisors to try has about half as many digits as the number.

The fast methods do not look for a divisor at all. They check a property that every prime has, such as a rule about remainders of powers. A number that breaks the rule is surely not prime, even when nobody knows any of its factors. So deciding primality is much easier than [factoring](/integer-factorization/).

## Definition

**Input.** An integer $n \ge 0$, written in binary with $\ell = \lfloor \lg n \rfloor + 1$ digits (and $\ell = 1$ for $n = 0$).

**Output.** Yes if $n$ is prime, that is, $n \ge 2$ and the only positive divisors of $n$ are $1$ and $n$. No otherwise.

As a language, $\text{PRIMES} = \{\, \langle n \rangle : n \text{ is prime} \,\}$, where $\langle n \rangle$ is the binary form of $n$. Its complement, apart from the strings that do not encode an integer, is the language of the composite numbers together with $0$ and $1$.

**Cost model.** Unless a statement says otherwise, the integers are of arbitrary precision and a cost is a number of bit operations, as on a [multitape Turing machine](/multitape-turing-machine/). A bound "polynomial" means polynomial in $\ell$, which is $\Theta(\log n)$. A test whose cost is polynomial in $n$, such as trial division, is exponential in the size of the input. For $n$ below $2^{64}$, the [word RAM](/word-ram/) with a product modulo $n$ in $O(1)$ steps is the usual model.

## Variants

- **Decision with certainty.** Answer yes or no, always correctly. [AKS](/aks-primality-test/) does this in deterministic polynomial time.
- **Monte Carlo testing.** Answer "composite" or "probably prime", with an error only on the side of "probably prime", and with a bound on the error probability that holds for every input. [Miller-Rabin](/miller-rabin/) and [Solovay-Strassen](/solovay-strassen/) are of this kind. A number that passes is a [probable prime](/probable-prime/).
- **Primality proving.** Answer yes together with a [certificate](/primality-certificate/) that a third party can check faster than the original search. This is the problem of [primality proving](/primality-proving/).
- **Word-size inputs.** For $n < 2^{64}$, a fixed set of bases makes Miller-Rabin deterministic and exact. See [deterministic Miller-Rabin bases](/deterministic-miller-rabin-bases/).
- **Numbers of special form.** For $2^p - 1$ the [Lucas-Lehmer test](/lucas-lehmer-test/), for $2^{2^k} + 1$ the [Pepin test](/pepin-test/), and for $k \cdot 2^m + 1$ with $k < 2^m$ the [Proth test](/proth-test/) decide primality with one long chain of squarings.
- **Many inputs at once.** To list all primes up to $N$, a [sieve of Eratosthenes](/sieve-of-eratosthenes/) is much faster than $N$ separate tests. See [primes up to n](/primes-up-to-n/).
- **Random primes.** Produce a random prime of a given size; see [random prime generation](/random-prime-generation/).

## Examples

| $n$ | answer | how to see it |
|---|---|---|
| $0$, $1$ | no | not at least 2, by the definition |
| $2$ | yes | the only even prime |
| $91$ | no | $91 = 7 \cdot 13$ |
| $561$ | no | $561 = 3 \cdot 11 \cdot 17$, the smallest [Carmichael number](/carmichael-number/), which passes the [Fermat test](/fermat-primality-test/) for every base coprime to it |
| $2^{31} - 1 = 2147483647$ | yes | trial division up to $46340$ finds no divisor |
| $2^{32} + 1 = 4294967297$ | no | $641 \cdot 6700417$ |
| $3215031751$ | no | $151 \cdot 751 \cdot 28351$; it passes the strong test of Miller-Rabin to each of the bases 2, 3, 5 and 7 |
| $2^{67} - 1$ | no | $193707721 \cdot 761838257287$ |
| $2^{521} - 1$ | yes | a [Mersenne prime](/mersenne-prime/) of 157 decimal digits |

The example $3215031751$ shows why a fixed small set of bases is not a proof in general: it is the smallest [strong pseudoprime](/strong-pseudoprime/) to all of the bases 2, 3, 5 and 7. The example $2^{67} - 1$ shows the gap between testing and factoring. One round of Miller-Rabin with the base 3 proves that it is composite, but finding its two factors needs a factoring algorithm. The base 2 does not catch it: each composite $2^p - 1$ with $p$ prime is a strong pseudoprime to the base 2.

**The size of the inputs.** A prime of 1024 binary digits has 308 or 309 decimal digits. Trial division would need about $2^{512}$ divisions, while one round of Miller-Rabin needs about 1024 modular squarings. Near $2^{1024}$, about one integer in $1024 \ln 2 \approx 710$ is prime, by the [prime number theorem](/prime-number-theorem/).

## Known algorithms

With $\ell$ the number of binary digits of $n$, and with schoolbook arithmetic:

- **[Trial division](/trial-division/).** Divide by $2, 3, \ldots, \lfloor \sqrt n \rfloor$. Exact, $O(\sqrt n)$ divisions, which is $2^{\ell/2}$ times a polynomial in $\ell$. Exponential, but the best choice for small $n$ and the usual first filter.
- **[Fermat test](/fermat-primality-test/).** Check $a^{n-1} \equiv 1 \pmod n$ for random bases. $O(k \ell^3)$ for $k$ rounds, but [Carmichael numbers](/carmichael-number/) pass for every coprime base, so there is no error bound that holds for all inputs.
- **[Solovay-Strassen](/solovay-strassen/).** Compare $a^{(n-1)/2}$ with the [Jacobi symbol](/jacobi-symbol/). $O(k \ell^3)$, one-sided error below $2^{-k}$ for every odd composite $n$.
- **[Miller-Rabin](/miller-rabin/).** The strong test. $O(k \ell^3)$, one-sided error at most $4^{-k}$ for every odd composite $n$. Under the generalized Riemann hypothesis, the bases below $2 (\ln n)^2$ suffice, which gives a deterministic $O(\ell^5)$ test (Miller 1976, with the constant of Bach 1990).
- **[Baillie-PSW](/baillie-psw/).** One strong test to the base 2 and one strong Lucas test. A few times the cost of one Miller-Rabin round. No composite that passes it is known, but no proof of correctness exists.
- **[AKS](/aks-primality-test/).** Deterministic and unconditional. The published analysis gives $\tilde O(\ell^{21/2})$; the variant of Lenstra and Pomerance with Gaussian periods gives $\tilde O(\ell^{6})$. Slow in practice.
- **[APR-CL](/apr-cl-primality-test/).** Deterministic, $(\log n)^{O(\log \log \log n)}$, which is not polynomial but practical for numbers of thousands of digits.
- **[ECPP](/ecpp/).** Randomized primality proving with elliptic curves. Its output is a certificate. Its running time is polynomial under heuristic assumptions, and it is the method of choice for proving the primality of large general numbers.
- **Methods based on a factored part of $n - 1$ or $n + 1$.** [Lucas](/lucas-primality-test/), [Pocklington](/pocklington-primality-test/), [Proth](/proth-test/), [Pepin](/pepin-test/) and [Lucas-Lehmer](/lucas-lehmer-test/). They are fast for numbers of special form.

## Bounds

**Upper bounds.** In the bit model, the problem is in [P](/p/): the best proven deterministic bound is $\tilde O(\ell^6)$ (Lenstra and Pomerance). With randomness, a Monte Carlo answer with error at most $4^{-k}$ costs $O(k \ell^3)$, or $O(k \ell \, M(\ell))$ with a multiplication of cost $M(\ell)$. On the word RAM, for $n < 2^{64}$, a fixed set of at most 12 Miller-Rabin bases gives an exact answer in $O(\log n)$ word operations.

**Complexity classes.** The history of the problem runs through the classes of complexity theory:

- $\text{PRIMES} \in$ [co-NP](/co-np/): a nontrivial factor is a short proof that $n$ is composite.
- $\text{PRIMES} \in$ [NP](/np/) (Pratt 1975): the [Pratt certificate](/pratt-certificate/) is a proof of primality of $O(\ell^2)$ binary digits that is checked in polynomial time.
- $\text{PRIMES} \in$ [co-RP](/co-rp/) (Solovay and Strassen 1977, Rabin 1980): the composite numbers have a randomized polynomial-time test with one-sided error.
- $\text{PRIMES} \in$ [RP](/rp/), so in [ZPP](/zpp/) (Adleman and Huang 1992), by a randomized test with abelian varieties.
- $\text{PRIMES} \in$ [P](/p/) (Agrawal, Kayal and Saxena 2002). Under the generalized Riemann hypothesis this was known since Miller (1976).

**Lower bounds.** Each correct algorithm must read the whole input, so $\Omega(\ell)$ is a lower bound. No better lower bound is known for the multitape Turing machine.

## Reductions

- **Primality reduces to factoring.** Given the prime factorization of $n$, the answer is yes exactly when the factorization has one prime with exponent 1. The converse is not known: an efficient test does not give an efficient way to factor.
- **A witness is not a factor.** A Fermat or Euler witness proves that $n$ is composite and in general gives no factor. One exception: when Miller-Rabin finds a [nontrivial square root of 1](/nontrivial-square-root-of-one/) $x$, then $\gcd(x - 1, n)$ is a proper factor of $n$.
- **Generation reduces to testing.** A random prime of $\ell$ binary digits is found by testing random candidates. By the prime number theorem, about $\ell \ln 2 / 2$ odd candidates are needed on average. See [random prime generation](/random-prime-generation/).
- **Testing with a factored $n - 1$.** If a factored part $F$ of $n - 1$ with $F^2 \ge n$ is known, [Pocklington's theorem](/pocklington-primality-test/) turns a few exponentiations into a proof. So proving reduces to partial factoring of $n - 1$, which is easy for numbers built for it.

## Applications

- Key generation for [RSA](/rsa-cryptosystem/), which needs two random primes of 1024 or more binary digits, and parameters for [Diffie-Hellman](/diffie-hellman/) and [DSA](/dsa/), which need primes of special form such as [safe primes](/safe-prime/).
- The sizes of hash tables and the moduli of hash functions, which are often chosen prime.
- Searches for record primes, such as the [Mersenne primes](/mersenne-prime/) found by the GIMPS project with the Lucas-Lehmer test.
- Factoring algorithms, which test each cofactor for primality before they try to split it further.

## References
