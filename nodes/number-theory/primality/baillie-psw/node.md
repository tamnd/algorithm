---
tag: 33QWDT
kind: algorithm
slug: baillie-psw
name: Baillie-PSW primality test
aliases:
- BPSW test
- Baillie-Pomerance-Selfridge-Wagstaff test
area: number-theory/primality
level: advanced
summary: A strong probable prime test with the base 2 followed by a strong Lucas test. Every prime passes; no composite that passes is known, and there is none below 2^64.
solves: [primality-testing]
model: multitape-turing-machine
complexity:
  vars: {n: the number tested}
  time: {worst: O((log n)^4), expected: O((log n)^3), best: O(1)}
  space: {extra: O(log n)}
properties: {deterministic: true, recursive: false, certifying: false}
history:
  year: 1980
  people: [Robert Baillie, Carl Pomerance, John Selfridge, Samuel S. Wagstaff Jr.]
  note: Baillie and Wagstaff, and Pomerance, Selfridge and Wagstaff, proposed the combination of a base-2 strong test and a Lucas test in two papers of 1980.
prereqs: [miller-rabin, strong-pseudoprime, jacobi-symbol]
see_also: [miller-rabin, lucas-primality-test, frobenius-test, deterministic-miller-rabin-bases, strong-pseudoprime, ecpp, fibonacci-numbers, primality-testing]
sources:
  - paper: doi:10.1090/S0025-5718-1980-0583518-6
    title: Robert Baillie and Samuel S. Wagstaff Jr., Lucas pseudoprimes, Mathematics of Computation 35 (1980)
    locator: pages 1391 to 1417 (strong Lucas pseudoprimes, Selfridge's choice of D, and the combined test)
  - paper: doi:10.1090/S0025-5718-1980-0572872-7
    title: Carl Pomerance, J. L. Selfridge and Samuel S. Wagstaff Jr., The pseudoprimes to 25·10^9, Mathematics of Computation 35 (1980)
    locator: pages 1003 to 1026 (the proposal to combine the base-2 strong test with a Lucas test)
  - paper: doi:10.1090/mcom/3616
    title: Robert Baillie, Andrew Fiori and Samuel S. Wagstaff Jr., Strengthening the Baillie-PSW primality test, Mathematics of Computation 90 (2021)
    locator: pages 1931 to 1955 (the history of the test, the check below 2^64, and extra congruences)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.6, Lucas pseudoprimes (including the strong Lucas test and the combined test)
  - url: https://en.wikipedia.org/wiki/Baillie%E2%80%93PSW_primality_test
    title: Baillie-PSW primality test, Wikipedia
    locator: sections The test, Checking for perfect squares, and Applications
---

The Baillie-PSW test decides whether an integer $n$ is a probable [prime](/prime-number/) by running two tests that fail in different ways: a strong probable prime test with the base 2, as in one round of [Miller-Rabin](/miller-rabin/), and a strong Lucas probable prime test whose parameters depend on $n$. Every prime passes, so the answer "composite" is always right. No composite that passes is known, and a computer check has shown that there is none below $2^{64}$. The test costs a few modular exponentiations and is the default probable prime test in many computer algebra systems.

## In plain words

Many fast primality tests have rare composite numbers that fool them. The trick of this test is to combine two tests whose fooling numbers look very different. The first checks powers of 2, as in the Miller-Rabin test. The second computes a sequence of numbers similar to the Fibonacci numbers, again keeping only remainders.

A prime always passes both. A composite would need to fool both at once, and nobody has ever found one that does, although many people have looked and no proof says none exists. All numbers below about eighteen billion billion have been checked. So the test gives a sure "not prime", or a "prime" that has never been wrong.

## The problem

The input is an integer $n$. The output is false when $n$ is not prime and true when $n$ is a probable prime. The answer false is always right. The answer true is right for every $n < 2^{64}$; for larger $n$ it is right in every case ever checked, but this is not proved.

**Cost model.** The integers are of arbitrary precision, with $\ell = \lfloor \lg n \rfloor + 1$ binary digits. Costs are in bit operations, as on a [multitape Turing machine](/multitape-turing-machine/). One product modulo $n$ costs $O(\ell^2)$ with [schoolbook multiplication](/schoolbook-multiplication/), or $O(M(\ell))$ with fast multiplication and division. For $n < 2^w$ on a word RAM, with a product modulo $n$ in $O(1)$ steps, the bounds below drop by a factor $\ell^2$.

**Error.** The error is one-sided: a wrong answer can only be true on a composite. The test uses no randomness, so the error depends only on $n$: each composite either fools the test or not, and repeating the test does not help. No bound on the number of such composites is proved. A heuristic of Pomerance suggests that there are infinitely many, but none is known.

## The algorithm

Write $U_k$ and $V_k$ for the Lucas sequences of $(P, Q)$: $U_0 = 0$, $U_1 = 1$, $V_0 = 2$, $V_1 = P$, and $X_{k+1} = P X_k - Q X_{k-1}$ for both. With $P = 1$ and $Q = -1$ they are the [Fibonacci numbers](/fibonacci-numbers/) and the Lucas numbers.

```pseudo id=main
BAILLIE-PSW(n)                              ▷ false: composite; true: probable prime
L1  if n < 2 then return false
L2  for each prime p ≤ 97 do if p divides n then return n = p
L3  if not STRONG-PROBABLE-PRIME(n, 2) then return false
L4  if n is a perfect square then return false
L5  D ← 5
L6  while JACOBI(D, n) ≠ −1 do
L7      if JACOBI(D, n) = 0 and |D| < n then return false
L8      D ← next value of 5, −7, 9, −11, 13, …
L9  P ← 1; Q ← (1 − D)/4
L10 write n + 1 = 2^s · d with d odd
L11 (U, V, W) ← (U_d mod n, V_d mod n, Q^d mod n)
L12 if U = 0 or V = 0 then return true
L13 repeat s − 1 times
L14     V ← (V² − 2W) mod n; W ← W² mod n
L15     if V = 0 then return true
L16 return false
```

**The strong test (L3).** Write $n - 1 = 2^t e$ with $e$ odd; $n$ passes if $2^e \equiv 1$ or $2^{2^r e} \equiv -1 \pmod n$ for some $0 \le r < t$. This is one round of Miller-Rabin with the fixed base 2.

**The perfect square check (L4).** For a square $n$, every $D$ has $\left(\frac{D}{n}\right) \in \{0, 1\}$, so the search of lines L5 to L8 would never end. An [integer square root](/integer-square-root/) by [Newton's method](/newton-integer-root/) settles it.

**Selfridge's choice of $D$ (L5 to L9).** The values $5, -7, 9, -11, 13, \ldots$ are all $D \equiv 1 \pmod 4$ with $|D| \ge 5$, so $Q = (1 - D)/4$ is an integer and $P^2 - 4Q = D$. The loop stops at the first $D$ with [Jacobi symbol](/jacobi-symbol/) $\left(\frac{D}{n}\right) = -1$. A value 0 means $\gcd(|D|, n) > 1$, and when $|D| < n$ that is a proper factor, so line L7 returns false. For primes the search takes about 2 tries on average.

**The strong Lucas test (L10 to L16).** It is the analogue of the strong test with $n + 1$ in place of $n - 1$: $n$ passes if $U_d \equiv 0$ or $V_{2^r d} \equiv 0 \pmod n$ for some $0 \le r < s$. Line L14 uses $V_{2k} = V_k^2 - 2Q^k$, with $W = Q^k$.

**Computing $U_d$ and $V_d$ (L11).** Read the binary digits of $d$ from the top, starting from $(U_1, V_1, Q^1) = (1, P, Q)$. A doubling step uses $U_{2k} = U_k V_k$, $V_{2k} = V_k^2 - 2Q^k$ and $Q^{2k} = (Q^k)^2$. A digit 1 adds the step $U_{k+1} = (P U_k + V_k)/2$ and $V_{k+1} = (D U_k + P V_k)/2$, where the halving is multiplication by the inverse $(n + 1)/2$ of 2 modulo $n$. This is the same idea as [fast doubling](/fibonacci-fast-doubling/) for Fibonacci numbers.

## Example

**$n = 127$, a prime.** Trial division by the primes up to 97 finds no factor. For the strong test, $126 = 2 \cdot 63$ and $2^{63} = (2^7)^9 \equiv 1$, so 127 passes. It is not a square. Since $127 \equiv 2 \pmod 5$, $\left(\frac{5}{127}\right) = \left(\frac{127}{5}\right) = \left(\frac{2}{5}\right) = -1$, so $D = 5$, $P = 1$, $Q = -1$, and the sequences are the Fibonacci and Lucas numbers. Here $n + 1 = 128 = 2^7$, so $d = 1$ and $s = 7$. Then $U_1 = 1$, $V_1 = 1$, and line L14 gives

| $r$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $V_{2^r} \bmod 127$ | $1$ | $3$ | $7$ | $47$ | $48$ | $16$ | $0$ |

For example $V_{16} = 47^2 - 2 = 2207 = 17 \cdot 127 + 48$. Since $V_{64} \equiv 0$ with $6 < s$, the answer is true.

**$n = 2047 = 23 \cdot 89$, a strong pseudoprime to the base 2.** Here $2046 = 2 \cdot 1023$ and $2^{1023} = (2^{11})^{93} \equiv 1$, so the strong test passes. Again $2047 \equiv 2 \pmod 5$ gives $D = 5$, $P = 1$, $Q = -1$, and $2048 = 2^{11}$ gives $d = 1$, $s = 11$. The values $V_{2^r} \bmod 2047$ for $r = 0, \ldots, 10$ are $1, 3, 7, 47, 160, 1034, 620, 1609, 1471, 160, 1034$, and $U_1 = 1$. None is 0, so the answer is false.

**$n = 5459 = 53 \cdot 103$**, the smallest strong Lucas pseudoprime with Selfridge's parameters ($D = -7$, $P = 1$, $Q = 2$). It fails at line L3: $5458 = 2 \cdot 2729$ and $2^{2729} \equiv 450 \pmod{5459}$.

## Correctness

**Primes pass.** Let $n$ be prime. Lines L1 and L2 are right by inspection. If $n > 97$, then $n$ passes the strong test of line L3, as in the [Miller-Rabin](/miller-rabin/) page, and line L4 does not fire. In the loop of lines L6 to L8, $\left(\frac{D}{n}\right) = 0$ means $n \mid D$, so $|D| \ge n$ and line L7 does not fire. When the loop stops, $D$ is a quadratic non-residue modulo $n$, and $n \nmid Q$, since $n \mid Q$ would give $D \equiv 1$, a square. Let $\alpha, \beta = (1 \pm \sqrt D)/2$ be the roots of $x^2 - Px + Q$ in the field $\mathbb{F}_{n^2} = \mathbb{F}_n(\sqrt D)$. The Frobenius map $z \mapsto z^n$ sends $\sqrt D$ to $D^{(n-1)/2} \sqrt D = -\sqrt D$, so $\alpha^n = \beta$ and $\alpha^{n+1} = \alpha\beta = Q$. Put $\gamma = \alpha / \beta$. Then $\gamma^{n+1} = \alpha^{n+1} / \beta^{n+1} = Q / Q = 1$. Now $U_k \equiv 0$ if and only if $\gamma^k = 1$, and $V_k \equiv 0$ if and only if $\gamma^k = -1$. In the sequence $\gamma^d, \gamma^{2d}, \ldots, \gamma^{2^s d} = 1$, either the first term is 1, or the term before the first 1 is a square root of 1 other than 1 in a field, so $-1$. Hence line L12 or line L15 returns true.

**False is always right.** Lines L1, L2, L4 and L7 return false only on composites, by inspection. Line L3 returns false only when the strong test fails, which no prime does. Line L16 is reached only when the strong Lucas test fails, which no prime does once lines L5 to L9 have found $D$.

**Termination.** For a non-square $n$, some $D \equiv 1 \pmod 4$ has $\left(\frac{D}{n}\right) = -1$, so the loop of lines L6 to L8 ends. The proof is in the proofs, together with the full argument above.

**What is not proved.** That a composite never passes. The two tests tend to fail on different composites: for $n = pq$ to pass both, the orders of 2 must be tied to $p - 1$ and $q - 1$ while the Lucas condition, with $\left(\frac{D}{n}\right) = -1$, ties the Lucas sequences to $p + 1$ and $q + 1$, and these conditions rarely hold together. This is a heuristic only.

## Complexity

**The two tests.** The strong test of line L3 is one [modular exponentiation](/modular-exponentiation/): $O(\ell)$ products modulo $n$. Line L11 handles one binary digit of $d$ with three products for the doubling and a few more, by the small numbers $P$ and $D$, for a digit 1; lines L13 to L15 add two products per pass. So the Lucas test is also $O(\ell)$ products modulo $n$, about two to three times the strong test. Together: $O(\ell^3) = O((\log n)^3)$ bit operations with schoolbook arithmetic, and $O(\ell \, M(\ell))$ with fast arithmetic.

**The other steps.** Line L2 costs $O(\ell)$ bit operations for each of the 25 small primes. The square test of line L4 costs $O(M(\ell))$ with Newton's method. Each Jacobi symbol in lines L6 and L7 costs $O(\ell^2)$, or $O(\ell \log |D|)$ when computed as $\left(\frac{n \bmod |D|}{|D|}\right)$ with a sign.

**The number of $D$ values.** For a random input the expected number of tries is a constant, so the expected cost is $O((\log n)^3)$. In the worst case it is not known to be small without a hypothesis: under the generalized Riemann hypothesis the first $D$ with $\left(\frac{D}{n}\right) = -1$ has $|D| = O((\log n)^2)$, which gives the worst-case bound $O((\log n)^4)$ in the front matter. Without it only bounds that are a power of $n$ are proved. No input is known that needs more than a few tries, so in practice the cost is $O((\log n)^3)$.

**Space.** $O(\log n)$ binary digits for $U$, $V$, $W$ and the exponents.

**The best case** is $n < 2$ or $n$ with a small prime factor, in $O(\ell)$ or $O(1)$.

## Properties

- **Deterministic, with one-sided error.** False proves compositeness; true is not a proof of primality, except for $n < 2^{64}$, where it has been checked against a list of all base-2 pseudoprimes.
- **No known counterexample.** Unlike Miller-Rabin with fixed bases, for which [strong pseudoprimes](/strong-pseudoprime/) to any finite set of bases exist, no composite is known to pass. Prizes have been offered for a counterexample.
- **Stronger than its parts.** There are 46 strong pseudoprimes to the base 2 below $10^6$ and 12 strong Lucas pseudoprimes (with Selfridge's parameters) below $10^5$; no number is in both lists, and none passes both tests below $2^{64}$.
- **No factor.** The test does not give a factor, except by chance in lines L2 and L7.
- **Related to Frobenius tests.** The Lucas part is a test in the ring $\mathbb{Z}_n[x]/(x^2 - x + Q)$; the [Frobenius test](/frobenius-test/) generalizes this.

## Variants and improvements

- **Extra checks at no cost.** Every prime with $\left(\frac{D}{n}\right) = -1$ also satisfies $V_{n+1} \equiv 2Q$ and $Q^{(n+1)/2} \equiv Q \left(\frac{Q}{n}\right) \pmod n$. The values needed are nearly free after line L15, and Baillie, Fiori and Wagstaff recommend adding such checks.
- **Other choices of $P$ and $Q$.** Selfridge's method B, or $Q = 1$ and the smallest $P$ with $\left(\frac{P^2 - 4}{n}\right) = -1$, which is the setting of the *extra strong* Lucas test; it is somewhat faster since $Q^k = 1$.
- **More Miller-Rabin bases.** Some systems add strong tests with a few more bases, fixed or random, before or after the Lucas test. This costs little and changes nothing below $2^{64}$.
- **Exact for 64-digit binary numbers.** For $n < 2^{64}$, the test is exact, and so are the [fixed base sets](/deterministic-miller-rabin-bases/) of Miller-Rabin; the base sets are faster for word-sized $n$.
- **Proving primality.** For a certificate, follow a true answer with [ECPP](/ecpp/), [APR-CL](/apr-cl-primality-test/), or, when $n - 1$ factors, the [Lucas primality test](/lucas-primality-test/).

## When to use it

Use Baillie-PSW when you need a fast primality decision for numbers above the 64-digit binary range and can accept a test that is not proved correct but has never failed, for example in computer algebra, cryptographic key generation together with random-base Miller-Rabin rounds, and number theory searches. Below $2^{64}$ either it or a fixed set of Miller-Rabin bases gives the exact answer. If the input may be chosen by an adversary, add random-base Miller-Rabin rounds, which have a proved bound. If a proof is needed, use a primality proving method.

## Pitfalls

- **Perfect squares.** Without line L4 the search for $D$ never ends on a square, for example on $n = 101^2$.
- **The value $\left(\frac{D}{n}\right) = 0$.** It means a common factor. Skip it only when $|D| \ge n$; otherwise $n$ is composite. Treating it as $-1$ breaks the test.
- **Halving modulo $n$.** The step to $k + 1$ divides by 2. Multiply by $(n + 1)/2$, or add $n$ to an odd value before shifting; do not use integer division of an odd number.
- **Negative $Q$ and $D$.** Reduce them modulo $n$ before use, and keep $V^2 - 2W$ non-negative before the reduction in languages with a signed remainder.
- **Using a plain Lucas test.** The weaker test, $U_{n+1} \equiv 0$ only, has more pseudoprimes; the strong form is the one with no known joint counterexample.
- **Small $n$.** The Lucas part assumes $n$ odd and coprime to $2QD$; the trial division of line L2 and the check in line L7 take care of this.

## Implementations

## History

In 1980 Carl Pomerance, John Selfridge and Samuel Wagstaff computed all pseudoprimes below $25 \cdot 10^9$, and Robert Baillie and Wagstaff studied Lucas pseudoprimes. Both papers proposed combining a base-2 strong test with a Lucas test, with Selfridge's rule for choosing $D$. In 1984 Pomerance gave a heuristic argument that counterexamples exist, in fact infinitely many, though no method to find one. Jan Feitsma's list of all base-2 Fermat pseudoprimes below $2^{64}$ later allowed a full check that no counterexample lies below $2^{64}$. In 2021 Baillie, Andrew Fiori and Wagstaff reviewed the test and its variants and proposed extra congruences.

## References
