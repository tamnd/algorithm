---
tag: 33MQ51
kind: definition
slug: fermat-pseudoprime
name: Fermat pseudoprime
aliases:
- Fermat liar composite
area: number-theory/primality
level: intro
summary: Composite n with a^(n-1) ≡ 1 (mod n) for a given base a, so that the Fermat test with the base a takes it for a prime.
prereqs: [fermat-little-theorem, prime-number, congruence]
see_also: [fermat-primality-test, carmichael-number, strong-pseudoprime, euler-jacobi-pseudoprime, pseudoprime, probable-prime, mersenne-prime, fermat-prime]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.8, Primality testing (base-a pseudoprimes and the procedure PSEUDOPRIME)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.4.1, Fermat pseudoprimes
  - paper: doi:10.1090/S0025-5718-1980-0572872-7
    title: Carl Pomerance, J. L. Selfridge and Samuel S. Wagstaff Jr., The pseudoprimes to 25·10^9, Mathematics of Computation 35 (1980)
    locator: pages 1003 to 1026 (the count of base-2 pseudoprimes below 25·10^9)
  - paper: doi:10.1016/0304-3975(80)90007-9
    title: Louis Monier, Evaluation and comparison of two efficient probabilistic primality testing algorithms, Theoretical Computer Science 12 (1980)
    locator: pages 97 to 108 (the number of bases to which a composite is a pseudoprime)
---

A Fermat pseudoprime to the base $a$ is a composite number $n$ that satisfies the congruence $a^{n-1} \equiv 1 \pmod n$ of [Fermat's little theorem](/fermat-little-theorem/), which every [prime](/prime-number/) not dividing $a$ satisfies. Such an $n$ fools the [Fermat primality test](/fermat-primality-test/) with the base $a$, and the base $a$ is then a *Fermat liar* for $n$. The smallest one to the base 2 is $341 = 11 \cdot 31$. A composite that is a pseudoprime to every base coprime to it is a [Carmichael number](/carmichael-number/).

## Definition

Let $a$ be an integer and $n \ge 2$ a composite integer. Then $n$ is a **Fermat pseudoprime to the base $a$** if

$$a^{n-1} \equiv 1 \pmod n.$$

The base $a$ is then a **Fermat liar** for $n$. A base $a$ with $\gcd(a, n) = 1$ and $a^{n-1} \not\equiv 1 \pmod n$ is a **Fermat witness** for $n$; it proves that $n$ is composite.

**The base is coprime to $n$.** If $a^{n-1} \equiv 1 \pmod n$, then $a \cdot a^{n-2} \equiv 1$, so $a$ has an inverse modulo $n$ and $\gcd(a, n) = 1$. So the definition needs no separate coprimality condition. The condition depends only on $a \bmod n$.

**The other form.** Some books, among them Crandall and Pomerance, call a composite $n$ a pseudoprime to the base $a$ when $a^n \equiv a \pmod n$. For $\gcd(a, n) = 1$ the two forms are equivalent, since $a$ can be cancelled. They differ when $\gcd(a, n) > 1$: the even number $161038 = 2 \cdot 73 \cdot 1103$ satisfies $2^{161038} \equiv 2 \pmod{161038}$, but no even number satisfies $2^{n-1} \equiv 1 \pmod n$.

**Trivial bases.** For each odd composite $n$, the bases $a \equiv 1$ and $a \equiv -1 \pmod n$ are liars, because $n - 1$ is even. Most authors call $n$ a pseudoprime to the base $a$ only for $1 < a < n - 1$, or count only bases such as $a = 2$ that are fixed in advance.

**The set of liars.** For an odd composite $n$, the liars form a subgroup of the [multiplicative group](/multiplicative-group-modulo-n/) $(\mathbb{Z}/n\mathbb{Z})^*$. If $n = \prod_i p_i^{e_i}$ with distinct primes $p_i$, the number of liars in $[1, n-1]$ is $\prod_i \gcd(n - 1, p_i - 1)$, by Monier (1980). The proof is on the page of the [Fermat test](/fermat-primality-test/).

## Examples and non-examples

**Examples.**

- $341 = 11 \cdot 31$ is a pseudoprime to the base 2: $2^{10} = 1024 = 3 \cdot 341 + 1$, so $2^{340} = (2^{10})^{34} \equiv 1 \pmod{341}$. It is the smallest composite with this property. It has $\gcd(340, 10) \cdot \gcd(340, 30) = 100$ liars in $[1, 340]$.
- $91 = 7 \cdot 13$ is the smallest pseudoprime to the base 3. It has $\gcd(90, 6) \cdot \gcd(90, 12) = 36$ liars.
- $15$ is a pseudoprime to the base 4: $4^2 = 16 \equiv 1$, so $4^{14} \equiv 1 \pmod{15}$. Its liars are $1, 4, 11, 14$.
- The smallest pseudoprimes to the bases 2 to 10 are $341, 91, 15, 4, 35, 6, 9, 4, 9$. Even and very small composites occur for some bases: $5^3 = 125 \equiv 1 \pmod 4$.
- **Composite Mersenne numbers.** If $p$ is prime and $M = 2^p - 1$ is composite, then $M$ is a pseudoprime to the base 2. Indeed $2^p \equiv 1 \pmod M$, and $p \mid 2^p - 2 = M - 1$ by Fermat's little theorem, so $2^{M-1} \equiv 1$. The first case is $2047 = 2^{11} - 1 = 23 \cdot 89$. See [Mersenne prime](/mersenne-prime/).
- **Composite Fermat numbers.** If $F_k = 2^{2^k} + 1$ with $k \ge 1$ is composite, it is a pseudoprime to the base 2. Indeed $2^{2^{k+1}} \equiv 1 \pmod{F_k}$, and $2^{k+1}$ divides $F_k - 1 = 2^{2^k}$ because $k + 1 \le 2^k$. The first case is $F_5 = 4294967297 = 641 \cdot 6700417$. See [Fermat prime](/fermat-prime/).
- **Carmichael numbers.** $561 = 3 \cdot 11 \cdot 17$ is a pseudoprime to each of the 320 bases in $[1, 560]$ that are coprime to it.

**Non-examples.**

- $341$ is not a pseudoprime to the base 3: $3^{340} \equiv 56 \pmod{341}$.
- A prime is never a pseudoprime, whatever the base: the definition asks for a composite number.
- $561$ is not a pseudoprime to the base 3, because $3 \mid 561$, so $3^{560} \equiv 1$ is impossible.
- No even number is a pseudoprime to an even base, and no even number is a pseudoprime to the base 2 in the form $2^{n-1} \equiv 1$.

**How many there are.** The base-2 pseudoprimes below $10^3, 10^4, 10^5, 10^6, 10^7$ number $3, 22, 78, 245, 750$, while there are $664579$ primes below $10^7$. Pomerance, Selfridge and Wagstaff (1980) counted $21853$ base-2 pseudoprimes below $25 \cdot 10^9$. So they are rare, but there are infinitely many: if $n$ is an odd base-2 pseudoprime, then $m = 2^n - 1$ is another. To see this, write $n = rs$ with $1 < r < n$; then $2^r - 1$ is a proper factor of $m$, so $m$ is composite. Also $m - 1 = 2(2^{n-1} - 1)$ is divisible by $2$ and by $n$, hence by $2n$, as $n$ is odd. Since $2^n \equiv 1 \pmod m$, we get $2^{m-1} = (2^n)^{(m-1)/n} \equiv 1 \pmod m$. Starting from 341 this gives an infinite chain of base-2 pseudoprimes.

## Related definitions

- [Carmichael number](/carmichael-number/): a composite that is a Fermat pseudoprime to every base coprime to it.
- [Euler-Jacobi pseudoprime](/euler-jacobi-pseudoprime/): a stronger condition, $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$ with the [Jacobi symbol](/jacobi-symbol/). Each Euler-Jacobi pseudoprime to the base $a$ is a Fermat pseudoprime to the base $a$.
- [Strong pseudoprime](/strong-pseudoprime/): the condition of [Miller-Rabin](/miller-rabin/). Each strong pseudoprime to the base $a$ is a Fermat pseudoprime to the base $a$; 2047 is the smallest to the base 2.
- [Probable prime](/probable-prime/): a number, prime or not, that passes a given test. A Fermat pseudoprime is a composite Fermat probable prime.
- [Pseudoprime](/pseudoprime/): the general term, for any test.
- [Compositeness witness](/compositeness-witness/): the opposite role of a base.

## References
