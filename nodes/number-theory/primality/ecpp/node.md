---
tag: 5ZT65R
kind: algorithm
slug: ecpp
name: Elliptic curve primality proving
aliases:
- ECPP
- Atkin-Morain ECPP
area: number-theory/primality
level: research
summary: Proves n prime with a chain of elliptic curves of known order, built by complex multiplication. The proof is a certificate that is fast to check; it is the fastest general proof in practice.
solves: [primality-proving]
model: multitape-turing-machine
complexity:
  vars: {n: the number tested}
  time: {heuristic: O((log n)^(5+ε)), best: O(1)}
  verification: {worst: O((log n)^4)}
  space: {extra: O((log n)^2)}
properties: {deterministic: false, recursive: false, certifying: true}
history:
  year: 1986
  people: [Shafi Goldwasser, Joe Kilian, A. O. L. Atkin, François Morain]
  note: Goldwasser and Kilian proved primality with random elliptic curves in 1986. Atkin then used curves with complex multiplication, whose orders are known in advance, and with Morain made the method practical; their paper appeared in 1993.
prereqs: [primality-certificate, pocklington-primality-test, elliptic-curve-cryptography, tonelli-shanks, jacobi-symbol]
see_also: [aks-primality-test, apr-cl-primality-test, pratt-certificate, elliptic-curve-factorization, baillie-psw, miller-rabin, cantor-zassenhaus-algorithm, ideal-class-group]
sources:
  - paper: doi:10.1090/S0025-5718-1993-1199989-X
    title: A. O. L. Atkin and François Morain, Elliptic curves and primality proving, Mathematics of Computation 61 (1993)
    locator: pages 29 to 68 (the method with complex multiplication, the class polynomials and the implementation)
  - paper: doi:10.1145/12130.12162
    title: Shafi Goldwasser and Joe Kilian, Almost all primes can be quickly certified, Proceedings of STOC 1986
    locator: pages 316 to 329 (the elliptic curve analogue of the Pocklington theorem and the first test)
  - paper: doi:10.1145/320211.320213
    title: Shafi Goldwasser and Joe Kilian, Primality testing using elliptic curves, Journal of the ACM 46 (1999)
    locator: pages 450 to 472 (the journal version, with the expected running time for almost all primes)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 7.5 (Algorithms 7.5.8 and 7.5.9), Section 7.6 (Theorem 7.6.1 and Algorithms 7.6.2 and 7.6.3) and Algorithm 2.3.13
  - paper: doi:10.1090/S0025-5718-06-01890-4
    title: François Morain, Implementing the asymptotically fast version of the elliptic curve primality proving algorithm, Mathematics of Computation 76 (2007)
    locator: pages 493 to 505 (fastECPP and its heuristic cost O((log n)^(4+ε)))
  - paper: doi:10.1090/S0025-5718-03-01517-5
    title: Mark Watkins, Class numbers of imaginary quadratic fields, Mathematics of Computation 73 (2004)
    locator: pages 907 to 938 (the complete lists of fields with class number up to 100)
  - url: https://en.wikipedia.org/wiki/Elliptic_curve_primality
    title: Elliptic curve primality, Wikipedia
    locator: the Goldwasser-Kilian theorem and the Atkin-Morain method
---

Elliptic curve primality proving (ECPP) proves that a number $n$ is prime and gives a [primality certificate](/primality-certificate/) that anyone can check quickly. It replaces the group of units modulo $n$ in the [Pocklington test](/pocklington-primality-test/) by the group of points of an elliptic curve modulo $n$. A point whose order has a large prime factor $q$ proves that $n$ is prime if $q$ is prime, so the problem goes down to a smaller number, and the steps repeat until the number is small. The Atkin-Morain form of the method builds curves of known order by complex multiplication; it is the fastest general primality proof in practice, but its running time is only a heuristic estimate.

## In plain words

A fast probable prime test can say that a number is almost surely prime, but it gives no proof. ECPP gives a proof.

The idea is to find a special curve and a point on it, chosen so that the point would behave in a certain way only if the number is prime. The proof needs one more fact: that a second, smaller number is also prime. The method then proves that smaller number in the same way, and so on, until the number is small enough to check directly.

The list of curves, points and numbers is the certificate. Making it is slow, because the method must search for good curves. Checking it is much faster, as each step is only a few calculations on a curve.

## The problem

The input is an integer $n$. The output is "composite", or "prime" together with a certificate: a list of steps that proves $n$ prime with the Goldwasser-Kilian theorem below. The answer must always be right. The method can also stop with no answer, if it finds no suitable curve; with the table of discriminants of this page, that did not occur in the tests.

**Cost model.** The integers are of arbitrary precision, with $\lg n$ binary digits, and costs are in bit operations, as on a [multitape Turing machine](/multitape-turing-machine/). One product or inverse modulo $n$ costs $O((\log n)^2)$ with schoolbook arithmetic, and $O(M(\log n) \log \log n)$ or less with fast multiplication.

**Curves modulo $n$.** For $n$ coprime to 6, a curve is $E: y^2 = x^3 + ax + b$ with $\gcd(4a^3 + 27b^2, n) = 1$. Its points are the pairs $(x, y)$ modulo $n$ on the curve, and the point at infinity $O$. Points are added with the usual chord and tangent formulas, as in [elliptic curve cryptography](/elliptic-curve-cryptography/). If $n$ is composite this is not a group, and a formula can need the inverse of a number that has a common factor with $n$; then $n$ is proved composite. $[k]P$ is $P$ added to itself $k$ times.

**The theorem (Goldwasser and Kilian).** Let $n > 1$ be coprime to 6, $E$ a curve modulo $n$, $P$ a point on it, and $m = kq$ with $q$ prime and $q > (n^{1/4} + 1)^2$. If $[m]P = O$ and $[k]P \ne O$, both computed without a failed inverse, then $n$ is prime. The reason: for a prime $p \mid n$, the point $P$ modulo $p$ has an order divisible by $q$, so the curve modulo $p$ has at least $q$ points. By Hasse's theorem it has at most $(\sqrt p + 1)^2$ points, so $\sqrt p > n^{1/4}$, that is $p > \sqrt n$. A number whose prime factors are all above its square root is prime.

## The algorithm

The method needs, for the current $n$, a curve whose number of points $m$ is known if $n$ is prime, and has the form $m = kq$. Atkin's idea is to take a fundamental discriminant $D < 0$ with $(D/n) = 1$, the [Jacobi symbol](/jacobi-symbol/). If $n$ is prime and $4n = u^2 + |D| v^2$, the curves with complex multiplication by the ring of integers of $\mathbb{Q}(\sqrt D)$ have $n + 1 \pm u$ points; for $D = -4$ also $n + 1 \pm 2v$, and for $D = -3$ also $n + 1 \pm (u + 3v)/2$ and $n + 1 \pm (u - 3v)/2$. Such a curve has a $j$-invariant that is a root modulo $n$ of the Hilbert class polynomial $H_D$, a polynomial with integer coefficients of degree $h(D)$, the class number. So the orders can be tested for a large prime factor before any curve is built.

The pseudocode keeps a list $C$ of steps and a set of numbers to avoid. REJECT$(n)$ means: $n$ is proved composite.

```pseudo id=main
ECPP(N)
L1  C ← empty list; bad ← empty set; n ← N
L2  repeat:
L3      if n < 2^64 then
L4          if n passes the strong test to the bases 2, 3, 5, ..., 37 then return prime with certificate C
L5          REJECT(n)
L6      if gcd(n, 6) ≠ 1 or n is a square or n fails the strong test to the base 2 then REJECT(n)
L7      for each fundamental D < 0 of the table, by increasing h(D), with (D/n) = 1 and 4n = u² + |D|v²:
L8          for each order m of D, if m = kq with k > 1, q ∉ bad, q > (n^(1/4) + 1)² and q a probable prime:
L9              j ← a root of H_D(X) modulo n
L10             for each twist y² = x³ + ax + b of the curve with j-invariant j:
L11                 choose a point P on it with U = [k]P ≠ O
L12                 if [q]U = O then append (n, a, b, P, k, q) to C; n ← q; go to L2
L13             if every twist had a point P with [q]U ≠ O then REJECT(n)
L14     if no D of the table works: if C is empty then stop with no answer, else go to L16
REJECT(n)
L15 if C is empty then return composite
L16 add n to bad; remove the last step of C; n ← the number of that step; go to L2
```

**Lines L3 to L5, the leaf.** Below $2^{64}$ the [strong test](/miller-rabin/) to the first 12 primes is exact: no composite below $2^{64}$ passes it (see [deterministic Miller-Rabin bases](/deterministic-miller-rabin-bases/)). So the chain ends there with a number that is proved prime or proved composite.

**Line L6** removes multiples of 2 and 3, for which the curve formulas do not apply, squares, and almost all composites, by one strong test.

**Line L7** walks a table of discriminants, by increasing class number. For each $D$ with $(D/n) = 1$ it computes a [square root](/tonelli-shanks/) $x_0$ of $D$ modulo $n$ and runs the modified Cornacchia algorithm: a Euclid chain on $2n$ and $x_0$ that stops at the first remainder below $2\sqrt n$, and tests whether the rest is $|D|$ times a square. For a prime $n$ this finds $u, v$ exactly when they exist, which happens for about one $D$ in $2 h(D)$. If no square root of $D$ is found, $n$ is composite.

**Line L8** removes the primes up to $\min(2^{16}, \sqrt n)$ from each order $m$, and keeps $m$ if what is left, $q$, is large enough and passes a probable prime test. The test $q > (n^{1/4} + 1)^2$ is done exactly in integers, as $n < (\sqrt q - 1)^4$.

**Line L9** needs $H_D$. The code computes it once for each $D$, as $\prod (X - j(\tau))$ over the reduced quadratic forms $(a, b, c)$ of discriminant $D$, with $\tau = (-b + \sqrt D)/(2a)$, in decimal arithmetic with enough digits, and rounds the coefficients to integers. Its root modulo $n$ comes from a [Cantor-Zassenhaus](/cantor-zassenhaus-algorithm/) split: first $\gcd(H_D, X^n - X)$, then $\gcd$ with $(X + t)^{(n-1)/2} - 1$ for random $t$.

**Lines L10 to L12.** For $j \ne 0, 1728$, the curve is $y^2 = x^3 - 3cx + 2c$ with $c = j/(j - 1728)$, and its twist uses $a g^2, b g^3$ for a non-residue $g$. For $D = -4$ the twists are $y^2 = x^3 - g^e x$, $e = 0, \ldots, 3$, and for $D = -3$ they are $y^2 = x^3 - g^e$, $e = 0, \ldots, 5$, with $g$ also not a cube. If $n$ is prime, exactly the right twist has $m$ points, so every $P$ on it has $[m]P = O$. A random $P$ comes from a random $x$ with a square right side and a square root. If $[k]P = O$ by chance, another $P$ is tried.

**Line L13.** If $n$ is prime, one of the twists has $m$ points, so no point on it can fail line L12. If every twist has such a point, $n$ is composite.

**Lines L14 to L16, backtracking.** A number $q$ found at line L8 is only a probable prime. If a later step proves it composite, or finds no curve for it, the method goes back one step and looks for another $q$. With the probable prime test of line L8 this almost never happens.

Throughout, a failed inverse, a failed square root, or a gcd with $n$ above 1 proves $n$ composite and calls REJECT$(n)$.

## Example

To keep the numbers small, take $N = 100003$ and stop the chain at 1000 instead of $2^{64}$. The code finds this chain.

**Step 1, $n = 100003$.** As $n \equiv 1 \pmod 3$, $(-3/n) = 1$, and $D = -3$ comes first in the table. Cornacchia gives $4n = 400012 = 632^2 + 3 \cdot 14^2$, so $u = 632$, $v = 14$, $(u + 3v)/2 = 337$ and $(u - 3v)/2 = 295$. The six orders, and what is left after removing the primes up to $\sqrt n \approx 316$, are:

| $m$ | factors | $q$ |
|---|---|---|
| $n + 1 + 632 = 100636$ | $2^2 \cdot 139 \cdot 181$ | 1 |
| $n + 1 - 632 = 99372$ | $2^2 \cdot 3 \cdot 7^2 \cdot 13^2$ | 1 |
| $n + 1 + 337 = 100341$ | $3^2 \cdot 11149$ | 11149 |

The bound is $(n^{1/4} + 1)^2 \approx 352.8$, and $11149 > 352.8$, so $m = 100341$, $k = 9$, $q = 11149$. For $D = -3$, $j = 0$, and the least $g$ that is neither a square nor a cube modulo $n$ is 2. The six twists $y^2 = x^3 - 2^e$ have $100636, 100341, 99709, 99372, 99667, 100299$ points for $e = 0, \ldots, 5$ (counted in the tests). So the twist $e = 0$ fails line L12, and the twist $y^2 = x^3 - 2$ passes: with $P = (55125, 32871)$, $U = [9]P = (31794, 59883) \ne O$ and $[11149]U = O$. So 100003 is prime if 11149 is.

**Step 2, $n = 11149$.** Again $D = -3$: $4n = 44596 = 211^2 + 3 \cdot 5^2$, and the first order, $n + 1 + 211 = 11361 = 3 \cdot 7 \cdot 541$, gives $k = 21$, $q = 541 > 127.1$. Here $g = 10$ and the curve is $y^2 = x^3 - 10^4 \equiv x^3 + 1149$, with $P = (5866, 10392)$, $[21]P = (6858, 3248) \ne O$ and $[541]([21]P) = O$.

**The leaf.** $541 < 1000$ is prime by the strong test. The certificate is the two rows $(100003, 0, 100001, (55125, 32871), 9, 11149)$ and $(11149, 0, 1149, (5866, 10392), 21, 541)$. A checker needs only two scalar products per row and the exact test of $q$ against the bound.

## Correctness

**Prime answers.** The last number of the chain is prime by the exact test below $2^{64}$. Each step $(n, a, b, P, k, q)$ has $\gcd(n, 6) = 1$, a curve with $\gcd(4a^3 + 27b^2, n) = 1$, $q > (n^{1/4} + 1)^2$, $[k]P \ne O$ and $[q]([k]P) = O$. By the Goldwasser-Kilian theorem, if $q$ is prime then $n$ is prime. By induction from the leaf back to $N$, $N$ is prime. This part does not depend on the class polynomial, the orders or any heuristic: a wrong curve can only make line L12 fail.

**Composite answers.** Every REJECT$(n)$ comes with a reason that no prime has: a factor of $n$ from a gcd or a failed inverse, a failed strong test, a square, a square root that a prime would have, or, at line L13, the absence of a twist with $m$ points. The last reason uses the theory of complex multiplication (Deuring): for a prime $n$ with $4n = u^2 + |D| v^2$, the curves with $j$-invariant a root of $H_D$ have exactly the orders listed for $D$, and the twists of lines L10 to L12 cover all of them. Line L15 returns composite only for the input $N$; for a number found at line L8, REJECT only drops it.

**Termination.** Every inner loop is finite: the table, the orders and the point tries are bounded. Each step lowers $n$, as $q \le m/2 < n$, so the chain has $O(\log N)$ steps, and each backtrack adds a new number below $N$ to the set bad. So the method stops. The full proof is in the proofs.

## Complexity

**Heuristic cost.** For a prime $n$, a probable prime test of $q$ costs $O((\log n)^3)$. The chance that an order $m$ has the form $kq$ is about $c / \log n$, and about $(\log n)^2$ discriminants are needed to find one, as the chance that $4n = u^2 + |D|v^2$ is solvable is $1/(2h(D))$. With fast arithmetic this gives $O((\log n)^{5 + \varepsilon})$ for the whole proof, under heuristic assumptions about the factorization of the orders (Atkin and Morain; Crandall and Pomerance, Section 7.6.2). None of this is proved.

**fastECPP.** Shallit's idea, as used by Morain, builds discriminants as products of small prime discriminants, which lowers the heuristic cost to $O((\log n)^{4 + \varepsilon})$.

**Checking a certificate.** This is proved, not heuristic. Each step lowers the number by at least about one binary digit, so there are at most about $\lg n$ steps, and each needs two scalar products of $O(\log n)$ point operations with an inverse each. With schoolbook arithmetic this is $O((\log n)^4)$ bit operations, and in practice far less, as most steps lower $n$ by many digits.

**Best case.** An even $n$, or one that fails the base 2 test, stops at line L6 in $O((\log n)^3)$.

**Space.** The certificate has $O(\log n)$ rows of $O(\log n)$ digits, so $O((\log n)^2)$ bits. The class polynomials of the table are fixed in size and do not grow with $n$.

**In practice.** The Python code of this page proves a 200-digit prime in a few seconds and a 300-digit prime in under a minute. Morain's programs and the program Primo by Marcel Martin prove primes of thousands of digits.

## Properties

- **Certifying.** A prime answer comes with a certificate that can be checked independently, by simpler code, much faster than it was found.
- **Always right, random time.** The answers are never wrong; the randomness and the heuristics affect only the running time.
- **No proved polynomial bound.** The expected running time is polynomial under heuristics, but no bound is proved for the Atkin-Morain method. The [AKS test](/aks-primality-test/) is proved polynomial but far slower in practice.
- **General.** Unlike the [Lucas-Lehmer](/lucas-lehmer-test/) or [Pépin](/pepin-test/) tests, it needs no special form of $n$, and unlike $n - 1$ methods it needs no factorization of $n - 1$.

## Variants and improvements

- **Goldwasser-Kilian.** The first form chooses random curves and counts their points with Schoof's algorithm. It is slower, but Goldwasser and Kilian proved that its expected time is polynomial for all but a tiny fraction of primes.
- **Adleman-Huang.** With Jacobians of curves of genus 2, Adleman and Huang gave a randomized method with a proved expected polynomial time for every prime.
- **Class polynomials.** Weber functions and other class invariants give polynomials with much smaller coefficients than $H_D$, which practical programs use.
- **fastECPP.** Discriminants built from a pool of small prime discriminants, and an order of the steps that reuses square roots, give the heuristic cost $O((\log n)^{4 + \varepsilon})$.
- **Montgomery coordinates.** Point products can use $(X : Z)$ coordinates without $y$, with fewer inverses.
- **Mixed certificates.** If $n - 1$ or $n + 1$ happens to factor well, a [Pocklington](/pocklington-primality-test/) step is cheaper than a curve step, and certificates can mix both kinds.

## When to use it

Use ECPP to prove a large number prime when there is no special form to exploit and a certificate is wanted, for example for primes of hundreds to thousands of digits in cryptography or in records. For numbers below $2^{64}$, a [deterministic Miller-Rabin](/deterministic-miller-rabin-bases/) test is enough. For a probable prime with no proof, use [Baillie-PSW](/baillie-psw/) or [Miller-Rabin](/miller-rabin/). For Mersenne or Fermat numbers, use the special tests. The [APR-CL](/apr-cl-primality-test/) test is a deterministic alternative with no certificate.

## Pitfalls

- **Arithmetic on a composite $n$.** The addition formulas must check every case: equal $x$ with $y_1 = -y_2$ gives $O$, equal points use the tangent, and equal $x$ with $y_1 \ne \pm y_2$ proves $n$ composite. Skipping a case can make a composite look prime.
- **The bound on $q$.** The theorem needs $q > (n^{1/4} + 1)^2$ and $q$ prime. Floating point is not enough near the bound; test $n < (\sqrt q - 1)^4$ in integers.
- **Too little precision for $H_D$.** The coefficients of $H_D$ have about $\pi \sqrt{|D|} \sum 1/a / \ln 10$ decimal digits; with fewer digits the rounding gives a wrong polynomial. A wrong polynomial cannot make a certificate wrong, but it can make line L13 call a prime composite. The code checks that every coefficient is within $10^{-10}$ of an integer.
- **Wrong twist.** Only one twist has $m$ points. Testing one curve and calling $n$ composite when it fails is wrong for $D = -3$ and $D = -4$, which have 6 and 4 twists.
- **Trusting probable primes in the chain.** A $q$ that passes a probable prime test is not proved prime until its own step is done; the chain must end at a number that is proved prime.
- **Recursion.** Write the descent as a loop, as here, not as a recursion of depth $O(\log n)$.

## Implementations

## History

The Pocklington test and its relatives prove $n$ prime from a factorization of $n - 1$, which is often out of reach. In 1986 Shafi Goldwasser and Joe Kilian replaced the group of units modulo $n$ by the group of an elliptic curve, whose order varies with the curve, and proved that their method certifies almost all primes in expected polynomial time. A. O. L. Atkin saw that curves with complex multiplication have orders that are known before the curve is built, which removes the slow point counting, and with François Morain he made this into a practical program; their paper in Mathematics of Computation appeared in 1993. Adleman and Huang gave a proved expected polynomial time for all primes in 1992, with curves of genus 2. Later work, including Shallit's idea and Morain's fastECPP, lowered the heuristic cost; in 2004 fastECPP proved prime a Leyland number of 15071 digits.

## References
