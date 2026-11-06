---
tag: JR8RT8
kind: algorithm
slug: aks-primality-test
name: AKS primality test
aliases:
- Agrawal-Kayal-Saxena test
- AKS test
area: number-theory/primality
level: advanced
summary: The first unconditional deterministic polynomial-time primality test. It checks (X + a)^n ≡ X^n + a modulo X^r - 1 and n for a few a and one small r.
solves: [primality-testing]
model: multitape-turing-machine
complexity:
  vars: {n: the number tested}
  time: {worst: O((log n)^(15/2) log log n), best: O(1)}
  space: {extra: O((log n)^4)}
properties: {deterministic: true, recursive: false, certifying: false}
history:
  year: 2002
  people: [Manindra Agrawal, Neeraj Kayal, Nitin Saxena]
  note: Agrawal Kayal and Saxena put the test online in August 2002 as PRIMES is in P. The paper appeared in the Annals of Mathematics in 2004.
prereqs: [fermat-little-theorem, multiplicative-order, euler-totient, polynomial-ring, binomial-theorem, modular-exponentiation]
see_also: [miller-rabin, ecpp, apr-cl-primality-test, baillie-psw, polynomial-identity-testing, kronecker-substitution, integer-nth-root, p]
sources:
  - paper: doi:10.4007/annals.2004.160.781
    title: Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160 (2004)
    locator: pages 781 to 793 (Lemma 2.1, the algorithm and Theorem 4.1 in Section 4, Lemma 4.3 on the size of r, Theorems 5.1 and 5.3 on the running time)
  - paper: doi:10.4171/JEMS/861
    title: H. W. Lenstra Jr. and Carl Pomerance, Primality testing with Gaussian periods, Journal of the European Mathematical Society 21 (2019)
    locator: pages 1229 to 1269 (the variant that runs in time (log n)^6 times a power of log log n)
  - paper: doi:10.1090/S0273-0979-04-01037-7
    title: Andrew Granville, It is easy to determine whether a given integer is prime, Bulletin of the American Mathematical Society 42 (2005)
    locator: pages 3 to 38 (a survey of the AKS test, its proof and its variants)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 4.5, The primality test of Agrawal, Kayal and Saxena
  - url: https://en.wikipedia.org/wiki/AKS_primality_test
    title: AKS primality test, Wikipedia
    locator: the algorithm and the history of the result
---

The AKS primality test decides whether an integer $n$ is [prime](/prime-number/) in time polynomial in the number of digits of $n$, with no randomness and no unproved hypothesis. It rests on a polynomial form of [Fermat's little theorem](/fermat-little-theorem/): $n$ is prime exactly when $(X + a)^n \equiv X^n + a \pmod n$. The test checks this identity only modulo a small polynomial $X^r - 1$, for a few values of $a$, and proves that this is enough. It settled an old question in complexity theory, but it is far too slow to replace the tests that are used in practice.

## In plain words

For a prime, a simple rule holds: if you expand a sum of two terms raised to the power of that prime, every middle term of the expansion is a multiple of the prime. For a composite number this fails. But the expansion has as many terms as the number itself, which is far too many to check.

The test therefore wraps the powers around a small circle, so that only a few hundred or a few thousand terms stay, and checks the rule for several small values. The clever part is the proof that a composite number, which is not a power of a smaller number, cannot pass all these small checks. Each step is plain arithmetic, the answer is always right, and the work grows only as a fixed power of the number of digits.

## The problem

The input is an integer $n \ge 0$. The output is true if $n$ is prime and false otherwise. The answer must always be right, and the time must be bounded by a polynomial in $\lg n$, the number of binary digits of $n$, for every input.

**Cost model.** The integers are of arbitrary precision, and costs are in bit operations, as on a [multitape Turing machine](/multitape-turing-machine/). Write $\lg$ for the base 2 logarithm. Polynomials are kept as lists of $r$ coefficients in $[0, n)$, and a product of two of them is done as one product of integers by [Kronecker substitution](/kronecker-substitution/). With the [Harvey-van der Hoeven multiplication](/harvey-van-der-hoeven-multiplication/), two integers of $m$ binary digits are multiplied in $O(m \log m)$ bit operations.

## The algorithm

Here $o_r(n)$ is the [multiplicative order](/multiplicative-order/) of $n$ modulo $r$, the least $k \ge 1$ with $n^k \equiv 1 \pmod r$, and $\varphi$ is [Euler's totient](/euler-totient/).

```pseudo id=main
AKS(n)
L1  if n < 2 then return false
L2  if n = a^b for integers a ≥ 2 and b ≥ 2 then return false
L3  r ← the least r with gcd(r, n) = 1 and o_r(n) > (lg n)^2
L4  if 1 < gcd(a, n) < n for some a ≤ r then return false
L5  if n ≤ r then return true
L6  ℓ ← ⌊√φ(r) · lg n⌋
L7  for a ← 1 to ℓ do
L8      if (X + a)^n ≢ X^n + a (mod X^r − 1, n) then return false
L9  return true
```

Line L2 rejects perfect powers, which the main step cannot catch; it takes an [integer root](/integer-nth-root/) for each exponent $b \le \lg n$. Line L3 tries $r = 2, 3, \ldots$ and, for each, computes $n, n^2, \ldots$ modulo $r$ up to the power $(\lg n)^2$; the first $r$ for which none of these is 1 is kept. Line L4 finds any factor of $n$ up to $r$, and line L5 then accepts small primes, which have no such factor. Lines L7 and L8 are the main work. For each $a$, the power $(X + a)^n$ is computed by square and multiply, with every product reduced modulo $X^r - 1$, by folding the term $X^{r+i}$ onto $X^i$, and every coefficient reduced modulo $n$. The result must be the two-term polynomial $X^{n \bmod r} + a$.

**Why it works.** For a prime $n$, the [binomial theorem](/binomial-theorem/) gives $(X + a)^n = \sum_i \binom{n}{i} X^i a^{n-i}$, and every middle coefficient $\binom{n}{i}$ is divisible by $n$. So $(X + a)^n \equiv X^n + a^n \equiv X^n + a \pmod n$, and line L8 never fires. For a composite $n$ the full identity fails, but the check modulo $X^r - 1$ is weaker, so the main theorem of Agrawal, Kayal and Saxena is needed: if a composite $n$ with no factor up to $r$ passed every check of line L8, then a prime factor $p$ of $n$ would produce more distinct elements in a finite field than that field can hold. The only way out is $n = p^k$, which line L2 rules out.

**Why $r$ is small.** Agrawal, Kayal and Saxena prove that some $r \le \max(3, \lceil (\lg n)^5 \rceil)$ has $o_r(n) > (\lg n)^2$. In practice the least such $r$ is a prime only a little larger than $(\lg n)^2$: for $n = 2^{61} - 1$, $(\lg n)^2 \approx 3721$ and $r = 3733$.

## Example

**$n = 31$, a prime.** Here $\lg 31 \approx 4.954$ and $(\lg 31)^2 \approx 24.54$, so the order must be at least 25. Every $r \le 25$ has $o_r(31) \le r - 1 \le 24$; $r = 26$ and $r = 28$ have $\varphi(r) = 12$ and $r = 27$ has $\varphi(r) = 18$, so their orders are too small. For $r = 29$, $31 \equiv 2 \pmod{29}$ and 2 has order 28 modulo 29, so line L3 gives $r = 29$. Line L4 finds no common factor, and $31 > 29$. Line L6 gives $\ell = \lfloor \sqrt{28} \cdot 4.954 \rfloor = \lfloor 26.22 \rfloor = 26$. For each $a = 1, \ldots, 26$, line L8 checks that $(X + a)^{31} \equiv X^2 + a \pmod{X^{29} - 1, 31}$, since $31 \bmod 29 = 2$. All 26 checks pass, and the test returns true.

**$n = 91 = 7 \cdot 13$.** Line L3 gives $r = 47$, and line L4 finds $\gcd(7, 91) = 7$ and returns false. Most composites stop at line L4.

**$n = 74513 = 269 \cdot 277$.** This is the least composite that reaches line L8: it is not a perfect power and both of its prime factors are larger than its $r$. Here $(\lg n)^2 \approx 261.96$, and line L3 gives the prime $r = 263$, for which $o_{263}(n) = 262$. Line L6 gives $\ell = 261$. For $a = 1$ the target is $X^{84} + 1$, as $74513 \bmod 263 = 84$, but $(X + 1)^{74513} \bmod (X^{263} - 1, 74513)$ has all 263 coefficients nonzero, starting with $54070 + 51917 X + 12374 X^2 + \cdots$. So line L8 returns false at once.

## Correctness

**Lemma (polynomial Fermat).** Let $n \ge 2$ and $\gcd(a, n) = 1$. Then $(X + a)^n \equiv X^n + a \pmod n$ as polynomials if and only if $n$ is prime. For a prime this is the binomial argument above. For a composite $n$, take a prime $q \mid n$ with $q^k$ the exact power of $q$ in $n$; then $q^k \nmid \binom{n}{q}$ and $q \nmid a^{n-q}$, so the coefficient of $X^q$ is not 0 modulo $n$.

**Theorem (Agrawal, Kayal and Saxena).** AKS$(n)$ returns true if and only if $n$ is prime.

*Primes return true.* For a prime, lines L1 and L2 do not fire, line L4 sees only $\gcd(a, n) = 1$ for $a < n$, and line L8 never fires by the lemma. So the test returns true at line L5 or line L9.

*True is right.* If line L5 returns true, $n \le r$ and line L4 found no factor below $n$, so $n$ is prime. Now suppose line L9 returns true for a composite $n$. Since $o_r(n) > 1$, some prime $p \mid n$ has $o_r(p) > 1$, and $p > r$ by line L4. Call $m$ *introspective* for a polynomial $f$ if $f(X)^m \equiv f(X^m) \pmod{X^r - 1, p}$. Both $p$ and $n / p$ are introspective for each $X + a$ with $0 \le a \le \ell$, and products of introspective numbers are introspective for products of these polynomials. Let $t$ be the number of residues modulo $r$ of the numbers $(n/p)^i p^j$; then $(\lg n)^2 < t \le \varphi(r)$. In a finite field built from a factor of the $r$-th cyclotomic polynomial over $\mathbb{F}_p$, the products of the $X + a$ give a group $\mathcal{G}$ with $|\mathcal{G}| \ge \binom{t + \ell}{t - 1} > n^{\sqrt t}$, by counting polynomials of degree below $t$. But if $n$ is not a power of $p$, two of the numbers $(n/p)^i p^j$ with $i, j \le \sqrt t$ agree modulo $r$, and that forces $|\mathcal{G}| \le n^{\sqrt t}$. So $n$ is a power of $p$, which line L2 excludes. The full proof is in the proofs.

**Termination.** Line L3 ends because a prime $r$ that divides neither $n$ nor any $n^i - 1$ with $i \le (\lg n)^2$ has the required order; the bound on $r$ above makes the search short. The other loops are bounded.

## Complexity

Let $r$ be the value found at line L3 and $\ell \le \sqrt{r} \lg n$.

**Line L8.** One check is $O(\log n)$ squarings and products by $X + a$. A product packs $r$ coefficients of $O(\log n)$ binary digits into an integer of $O(r \log n)$ digits, so it costs $O(r \log n \log\log n)$ with Harvey-van der Hoeven multiplication, since $\log(r \log n) = O(\log\log n)$. The $r$ reductions modulo $n$ cost the same. So one check is $O(r (\log n)^2 \log\log n)$, and all $\ell$ checks are $O(r^{3/2} (\log n)^3 \log\log n)$.

**The bound on $r$.** With the elementary bound $r = O((\log n)^5)$ of Lemma 4.3 this is $O((\log n)^{21/2} \log\log n)$, which is Theorem 5.1 of the paper. A sieve result of Fouvry on primes $q$ for which $q - 1$ has a large prime factor gives $r = O((\log n)^3)$, and hence the bound $O((\log n)^{15/2} \log\log n)$ of Theorem 5.3 and of the front matter. If $r = O((\log n)^2)$, as the Sophie Germain prime density conjecture or a strong form of Artin's conjecture would give, the time is $(\log n)^6$ times a power of $\log\log n$.

**The other lines.** Line L2 is $O(\log n)$ integer roots, polynomial in $\log n$ and minor. Line L3 tries at most $r$ values with at most $(\lg n)^2$ products modulo $r$ each, and line L4 is $r$ gcds of numbers of $O(\log n)$ digits. Both are below the cost of line L8.

**Best case.** Inputs below 2 return at once. Even numbers and numbers with a small factor stop at line L4, after lines L2 and L3, in time polynomial in $\log n$ but far below the worst case.

**Space.** One polynomial of $r$ coefficients modulo $n$, $O(r \log n)$ bits, which is $O((\log n)^4)$ with Fouvry's bound.

**In practice.** The constants and the exponent are large. The Python code of this page needs a few seconds for the prime $1000003$, and one check of line L8 for $n = 2^{61} - 1$, with $r = 3733$, takes a few seconds, out of $\ell = 3726$ checks. A [Miller-Rabin](/miller-rabin/) test on the same number takes microseconds.

## Properties

- **Deterministic and exact.** No randomness and no error, in either direction.
- **Unconditional.** The proof uses no unproved hypothesis; earlier deterministic polynomial-time tests, such as Miller's, needed the generalized Riemann hypothesis.
- **Polynomial time.** It places PRIMES in the class [P](/p/) without any condition.
- **No certificate.** A true answer comes with no short proof that another program can check faster than by running the test again. [ECPP](/ecpp/) gives such certificates.
- **Composites are cheap.** A composite almost always fails at line L4 or at the first check of line L8.

## Variants and improvements

- **Lenstra and Pomerance.** Replacing $X^r - 1$ by a polynomial built from Gaussian periods gives a test that provably runs in time $(\log n)^6$ times a power of $\log\log n$.
- **Fouvry's bound.** No change to the algorithm, only to its analysis: the least $r$ is $O((\log n)^3)$, which gives the exponent $15/2$.
- **A conjectured fast form.** Agrawal, Kayal and Saxena state a conjecture of Bhattacharjee and Pandey: for a prime $r$ not dividing $n$, if $(X - 1)^n \equiv X^n - 1 \pmod{X^r - 1, n}$ then $n$ is prime or $n^2 \equiv 1 \pmod r$. It would give a test in time about $(\log n)^3$. Lenstra and Pomerance gave a heuristic argument that it is false as stated.
- **Randomized forms.** Daniel Bernstein, building on ideas of Pedro Berrizbeitia and of Qi Cheng, gave a randomized version that proves primality in expected time about $(\log n)^4$.
- **Agrawal and Biswas.** The earlier randomized test checks the polynomial Fermat identity modulo a random polynomial, as a form of [polynomial identity testing](/polynomial-identity-testing/).

## When to use it

Use the AKS test to understand why primality is in P, or when a proof must not depend on randomness or on an unproved hypothesis and the numbers are small. For real work, use [Baillie-PSW](/baillie-psw/) or [Miller-Rabin](/miller-rabin/) to find probable primes, and [ECPP](/ecpp/) or [APR-CL](/apr-cl-primality-test/) to prove them prime: these are faster by many orders of magnitude, and ECPP also gives a certificate.

## Pitfalls

- **Skipping the perfect power check.** The proof of line L8 ends with $n = p^k$, and only line L2 excludes $k \ge 2$; without it the test has no proof for prime powers.
- **Wrong rounding of $(\lg n)^2$.** The order must be larger than $(\lg n)^2$ itself, not than a rounded value; compute $\lfloor (\lg n)^2 \rfloor$ exactly, for example with enough decimal precision, and require $o_r(n) > \lfloor (\lg n)^2 \rfloor$. For $n$ not a power of 2, $(\lg n)^2$ is never an integer.
- **Too few values of $a$.** The bound $\ell = \lfloor \sqrt{\varphi(r)} \lg n \rfloor$ is part of the proof; using fewer values of $a$ breaks it, even if every composite that is tried in practice fails at $a = 1$.
- **Overflow in the packed product.** With Kronecker substitution, each slot must hold a sum of up to $r$ products of two coefficients, so it needs about $2 \lg n + \lg r$ binary digits.
- **Expecting speed.** Even for the 19-digit prime $2^{61} - 1$ a full run takes hours in Python; tests of large primes must check only a few values of $a$.
- **Recursion.** Write the powering as a loop over the binary digits of $n$, not as a recursive function.

## Implementations

## History

The polynomial identity behind the test is a form of Fermat's little theorem, and Agrawal and Biswas used it in 2003 for a randomized test. Before AKS, Gary Miller's test of 1976 was deterministic and polynomial only under the generalized Riemann hypothesis, the test of Adleman, Pomerance and Rumely of 1983 was deterministic in time $(\log n)^{O(\log\log\log n)}$, and the elliptic curve methods of Goldwasser and Kilian, Atkin, and Adleman and Huang were randomized. Manindra Agrawal and his students Neeraj Kayal and Nitin Saxena, at the Indian Institute of Technology Kanpur, put their test online in August 2002 under the title "PRIMES is in P". The published version uses a counting lemma of Hendrik Lenstra Jr., and the paper appeared in the Annals of Mathematics in 2004. The three authors received the Gödel Prize in 2006.

## References
