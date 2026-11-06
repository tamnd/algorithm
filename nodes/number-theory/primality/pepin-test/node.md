---
tag: SM5V45
kind: algorithm
slug: pepin-test
name: Pepin's test
aliases:
- Pépin's test
- Pepin test
area: number-theory/primality
level: core
summary: Deterministic test for Fermat numbers F_k = 2^(2^k) + 1. For k ≥ 1, F_k is prime exactly when 3^((F_k - 1)/2) ≡ -1 (mod F_k), which costs 2^k - 1 squarings modulo F_k.
solves: [primality-testing]
model: multitape-turing-machine
complexity:
  vars: {k: the index of the Fermat number F_k = 2^(2^k) + 1}
  time: {worst: O(8^k), best: O(1)}
  space: {extra: O(2^k)}
properties: {deterministic: true, recursive: false, certifying: false}
history:
  year: 1877
  people: [Théophile Pépin]
  note: Pépin published the criterion in the Comptes rendus of the Paris Academy in 1877. Computer runs of the test proved F_20 and F_24 composite although no factor of either is known.
prereqs: [fermat-prime, quadratic-reciprocity, euler-criterion, modular-exponentiation]
see_also: [fermat-prime, lucas-lehmer-test, proth-test, lucas-primality-test, primitive-root, fermat-primality-test, schonhage-strassen-multiplication, primality-testing]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 4.1.1, The Lucas theorem and Pepin test (the statement and proof), and Section 1.3.2 on Fermat numbers
  - paper: doi:10.1090/S0025-5718-1988-0917833-8
    title: Jeff Young and Duncan A. Buell, The twentieth Fermat number is composite, Mathematics of Computation 50 (1988)
    locator: pages 261 to 263
  - paper: doi:10.1090/S0025-5718-1995-1277765-9
    title: Richard Crandall, J. Doenias, C. Norrie and Jeff Young, The twenty-second Fermat number is composite, Mathematics of Computation 64 (1995)
    locator: pages 863 to 868
  - paper: doi:10.1090/S0025-5718-02-01479-5
    title: Richard E. Crandall, Ernst W. Mayer and Jason S. Papadopoulos, The twenty-fourth Fermat number is composite, Mathematics of Computation 72 (2003)
    locator: pages 1555 to 1572
  - url: https://en.wikipedia.org/wiki/P%C3%A9pin%27s_test
    title: Pépin's test, Wikipedia
    locator: Description of the test, Proof of correctness, and the citation of P. Pépin, Sur la formule 2^(2^n) + 1, Comptes rendus 85 (1877), pages 329 to 333
---

Pépin's test decides whether a Fermat number $F_k = 2^{2^k} + 1$ is [prime](/prime-number/). For $k \ge 1$ it computes $3^{(F_k - 1)/2} \bmod F_k$ by $2^k - 1$ squarings, and $F_k$ is prime exactly when the result is $F_k - 1$, that is $-1$. The test is deterministic and always right, and the reduction modulo $F_k$ needs only shifts and a subtraction. It has shown that $F_5$ to $F_{32}$ are not [Fermat primes](/fermat-prime/), and it is the only known proof for $F_{20}$ and $F_{24}$, whose factors nobody has found.

## In plain words

A Fermat number is one more than two raised to a power of two, such as 5, 17, 257 and 65537. To test one, start with the number three. Square it and keep only the remainder after division by the Fermat number. Repeat the squaring a fixed number of times. If the final remainder is one less than the Fermat number, the number is prime; otherwise it is not.

The answer is always right, and the division by a Fermat number is cheap, because it only needs to cut the binary digits into two blocks and subtract. When the test says "not prime", it gives no factor.

## The problem

The input is an integer $k \ge 0$. The output is true if $F_k = 2^{2^k} + 1$ is prime and false otherwise. The answer is always right. Only Fermat numbers can be tested: this is the price of the speed. The test also works as a check of any $n$ that is a Fermat number, after finding $k$ from $n$.

**Cost model.** The integers are of arbitrary precision. Let $N = 2^k + 1$ be the number of binary digits of $F_k$, so $N = \Theta(\log F_k)$. Costs are in bit operations, as on a [multitape Turing machine](/multitape-turing-machine/), and $M(N)$ is the cost of one product of two $N$-digit integers: $O(N^2)$ for [schoolbook multiplication](/schoolbook-multiplication/), $O(N \log N)$ for [Harvey and van der Hoeven](/harvey-van-der-hoeven-multiplication/). The bound $O(8^k)$ in the front matter is the schoolbook bound $O(N^3)$ written in terms of $k$.

## The algorithm

```pseudo id=main
PEPIN(k)                                    ▷ true exactly when 2^(2^k) + 1 is prime
L1  if k = 0 then return true               ▷ F_0 = 3
L2  F ← 2^(2^k) + 1
L3  x ← 3
L4  repeat 2^k − 1 times
L5      x ← x² mod F
L6  return x = F − 1
```

Line L1 handles $k = 0$: there $F_0 = 3$ is a multiple of the base, and the loop would not run. Line L3 sets $x = 3 = 3^{2^0}$. After the $i$-th pass of line L5, $x \equiv 3^{2^i} \pmod F$. After $2^k - 1$ passes, $x \equiv 3^{2^{2^k - 1}} = 3^{(F - 1)/2}$, because $F - 1 = 2^{2^k}$. Line L6 compares this with $-1 \equiv F - 1$.

The loop is [binary exponentiation](/binary-exponentiation/) for an exponent that is a power of two, so it has no multiplications, only squarings.

**Reduction modulo $F$.** Let $e = 2^k$, so $F = 2^e + 1$ and $2^e \equiv -1 \pmod F$. A number $x = h \cdot 2^e + \ell$ with $0 \le \ell < 2^e$ satisfies $x \equiv \ell - h$. So the reduction in line L5 needs a shift, a mask and a subtraction. For $x < F^2$, as in line L5, $h < F$ and one step gives a value in $(-F, F)$; if it is negative, add $F$ once.

**Why 3.** If $F_k$ is prime and $k \ge 1$, then $F_k \equiv 1 \pmod 4$ and $F_k \equiv 2 \pmod 3$. By [quadratic reciprocity](/quadratic-reciprocity/), 3 is then a quadratic non-residue modulo $F_k$, and [Euler's criterion](/euler-criterion/) gives $3^{(F_k - 1)/2} \equiv -1$. In the other direction, $3^{(F_k - 1)/2} \equiv -1$ forces 3 to have [multiplicative order](/multiplicative-order/) $F_k - 1$ modulo every prime factor of $F_k$, and that is possible only if the prime factor is $F_k$ itself.

## Example

**$k = 3$, $F_3 = 257$.** The loop runs $2^3 - 1 = 7$ times, and $x_i = 3^{2^i} \bmod 257$.

| $i$ | $x_{i-1}^2$ | blocks $h, \ell$ | $x_i$ |
|---|---|---|---|
| 0 | | | $3$ |
| 1 | $9$ | $0, 9$ | $9$ |
| 2 | $81$ | $0, 81$ | $81$ |
| 3 | $6561$ | $25, 161$ | $136$ |
| 4 | $18496$ | $72, 64$ | $249$ |
| 5 | $62001$ | $242, 49$ | $64$ |
| 6 | $4096$ | $16, 0$ | $241$ |
| 7 | $58081$ | $226, 225$ | $256$ |

For example, in row 4, $18496 = 72 \cdot 256 + 64$, so $18496 \equiv 64 - 72 = -8 \equiv 249 \pmod{257}$. The last value is $256 = F_3 - 1$, so $257$ is prime.

**$k = 5$, $F_5 = 4294967297$.** After 31 squarings, $3^{(F_5 - 1)/2} \equiv 10324303 \pmod{F_5}$, which is not $F_5 - 1 = 4294967296$. So $F_5$ is composite, as Euler's factor $641$ shows: $F_5 = 641 \cdot 6700417$. The test itself gives no factor.

## Correctness

**Theorem (Pépin).** For each integer $k \ge 1$, $F_k$ is prime if and only if $3^{(F_k - 1)/2} \equiv -1 \pmod{F_k}$. Hence PEPIN$(k)$ returns true if and only if $F_k$ is prime, for every $k \ge 0$.

*If the congruence holds, $F_k$ is prime.* Let $q$ be a prime factor of $F = F_k$. Then $q \ne 3$, since $-1 \not\equiv 0 \pmod 3$. Modulo $q$, $3^{(F-1)/2} \equiv -1$ and $3^{F-1} \equiv 1$. So the order of 3 modulo $q$ divides $F - 1 = 2^{2^k}$ but not $(F - 1)/2$, and it is $F - 1$. By [Fermat's little theorem](/fermat-little-theorem/) the order divides $q - 1$, so $q \ge F$, and $q = F$.

*If $F_k$ is prime, the congruence holds.* As $k \ge 1$, $4 \mid 2^{2^k}$, so $F \equiv 1 \pmod 4$; and $2^{2^k} \equiv 1 \pmod 3$ since the exponent is even, so $F \equiv 2 \pmod 3$. By quadratic reciprocity for the [Legendre symbol](/legendre-symbol/), $\left(\frac{3}{F}\right) = \left(\frac{F}{3}\right) = \left(\frac{2}{3}\right) = -1$. Euler's criterion gives $3^{(F-1)/2} \equiv -1 \pmod F$.

The loop of lines L3 to L5 computes $3^{(F-1)/2} \bmod F$, and line L1 covers $F_0 = 3$. The full proof, with the reduction step, is in the proofs.

## Complexity

**Time.** The loop runs $2^k - 1 = N - 2$ times. Each pass squares a number below $F$, of $N$ binary digits, and reduces the square with one shift, one mask and one subtraction of $O(N)$ bit operations. So the test costs $O(N \, M(N))$ bit operations: $O(N^3) = O(8^k)$ with schoolbook multiplication, and $O(N^2 \log N)$ with the Harvey and van der Hoeven bound. In terms of the number tested, this is $O((\log F_k)^3)$ with schoolbook arithmetic, the cost of one [Miller-Rabin](/miller-rabin/) round on a number of the same size. The best case is $k = 0$, in $O(1)$.

**Space.** The value $x$ and its square need $O(N) = O(2^k)$ binary digits.

**In practice.** Multiplication modulo $2^N + 1$ is a negacyclic convolution, so [fast Fourier transform](/fast-fourier-transform/) multiplication with a weighted transform does the reduction at no extra cost, as in [Schönhage-Strassen multiplication](/schonhage-strassen-multiplication/). The proof that $F_{24}$ is composite needed $2^{24} - 1 \approx 1.7 \cdot 10^7$ squarings of numbers with about $5 \cdot 10^6$ decimal digits.

## Properties

- **Deterministic and exact.** No randomness and no error.
- **Special purpose.** It applies only to Fermat numbers. The [Lucas-Lehmer test](/lucas-lehmer-test/) does the same job for Mersenne numbers $2^p - 1$.
- **No factor.** A result other than $F_k - 1$ proves $F_k$ composite but gives no factor. $F_{20}$ and $F_{24}$ are known to be composite only by this test.
- **An $N - 1$ test.** $F_k - 1 = 2^{2^k}$ is completely factored, and the test is the special case of the [Lucas primality test](/lucas-primality-test/) and of the [Proth test](/proth-test/) with the fixed base 3.
- **3 is a primitive root.** The proof shows that 3 has order $F_k - 1$ modulo each Fermat prime $F_k$ with $k \ge 1$, so 3 is a [primitive root](/primitive-root/) of 5, 17, 257 and 65537.
- **The [Fermat test](/fermat-primality-test/) with base 2 is useless here.** Since $2^{2^{k+1}} \equiv 1 \pmod{F_k}$, every $F_k$ satisfies $2^{F_k - 1} \equiv 1$. Pépin's test uses base 3 for this reason.

## Variants and improvements

- **Other bases.** Any base $a$ with $\left(\frac{a}{F_k}\right) = -1$ works, with the same proof. For $k \ge 2$, $F_k \equiv 2 \pmod 5$ and $F_k \equiv 1 \pmod 8$, so the bases 5 and 10 work too. The base 2 never works for $k \ge 2$: then $2^{(F_k - 1)/2} \equiv 1$ always.
- **Proth's theorem.** For $n = h \cdot 2^m + 1$ with odd $h < 2^m$, $n$ is prime if and only if $a^{(n-1)/2} \equiv -1 \pmod n$ for some $a$; Pépin's test is the case $h = 1$, $m = 2^k$ with $a = 3$.
- **Checking the cofactor.** When some prime factors of $F_k$ are known, the residue that the test computes can be reused to check whether the remaining cofactor is a probable prime. This is how the cofactors of several $F_k$ were shown to be composite.
- **Trial factoring first.** Each prime factor of $F_k$ has the form $j \cdot 2^{k+2} + 1$ for $k \ge 2$ (see [Fermat prime](/fermat-prime/)). Searches for factors of this form are much cheaper than the full test and find most known factors.
- **Double checks.** Long runs were done twice, with different programs or hardware, and the final residues compared.

## When to use it

Use Pépin's test to decide primality of a Fermat number and of nothing else; there it is the method of choice. For $k \le 32$ the answer is already known, so in practice it serves to double-check old results and to test the cofactors of partly factored $F_k$. For general numbers use [Miller-Rabin](/miller-rabin/) or a proving method; for $h \cdot 2^m + 1$ use the [Proth test](/proth-test/), and for $2^p - 1$ the [Lucas-Lehmer test](/lucas-lehmer-test/).

## Pitfalls

- **The case $k = 0$.** $F_0 = 3$ is a multiple of the base 3; the loop runs zero times and $3 \ne 2$, so the prime 3 needs its own line.
- **A base that is a quadratic residue.** With the base 2, or any base $a$ with $\left(\frac{a}{F_k}\right) = 1$, a prime $F_k$ gives $+1$, not $-1$, and the test wrongly says "composite".
- **Off by one in the loop count.** The loop runs $2^k - 1$ times, so that the exponent is $(F_k - 1)/2 = 2^{2^k - 1}$. With $2^k$ passes a prime gives $1$, not $-1$.
- **Negative values in the reduction.** The step $\ell - h$ can be negative. For inputs below $F^2$ one addition of $F$ is enough; for larger inputs, repeating the step and adding $F$ in a loop can take very long, so track the sign instead.
- **Using the Fermat test instead.** The Fermat test with base 2 says "probable prime" for every Fermat number, prime or not.

## Implementations

## History

Théophile Pépin published the test in 1877 in the Comptes rendus of the Paris Academy. François Proth gave the more general theorem for $h \cdot 2^m + 1$ in 1878. For several Fermat numbers the test showed compositeness long before a factor was found; $F_7$, for example, was shown composite by hand early in the twentieth century but factored only in 1970. With computers the test settled $F_{20}$ in 1987 (Young and Buell), $F_{22}$ in 1993 (Crandall, Doenias, Norrie and Young) and $F_{24}$ in 1999 (Crandall, Mayer and Papadopoulos). A factor of $F_{22}$ was found later, but none is known for $F_{20}$ or $F_{24}$.

## References
