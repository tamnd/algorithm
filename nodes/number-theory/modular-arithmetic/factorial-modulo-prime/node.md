---
tag: 22Z5XD
kind: problem
slug: factorial-modulo-prime
name: Factorial modulo a prime
aliases:
- Factorial modulo p
area: number-theory/modular-arithmetic
level: core
summary: Compute n factorial modulo a prime p, possibly with powers of p removed, faster than multiplying all terms.
prereqs: [factorial, modular-inverse, wilson-theorem, legendre-formula]
see_also: [lucas-theorem, binomial-coefficient-computation, fast-multipoint-evaluation, subproduct-tree, batch-modular-inverse, wilsons-theorem, binary-exponentiation]
sources:
  - url: https://cp-algorithms.com/algebra/factorial-modulo.html
    title: Factorial modulo p, cp-algorithms
    locator: sections Algorithm, Implementation and Multiplicity of p (the factorial with the factors p removed, its cost O(p + log_p n), and Legendre's formula)
  - paper: doi:10.1137/S0097539704443793
    title: Alin Bostan, Pierrick Gaudry and Éric Schost, Linear recurrences with polynomial coefficients and application to integer factorization and Cartier-Manin operator, SIAM Journal on Computing 36(6), 2007, pages 1777 to 1806
    locator: Section 1, Main algorithmic ideas (the factorial in O(M(N^(1/2)) log N) ring operations by Strassen's blocks), and Section 6, Theorem 14 (one term of a recurrence in O(M(N^(1/2))) operations when small integers are units)
  - url: https://arxiv.org/abs/1209.3436
    title: Edgar Costa, Robert Gerbicz and David Harvey, A search for Wilson primes, Mathematics of Computation 83 (2014)
    locator: abstract and introduction ((p - 1)! mod p^2 for all primes p up to 2 * 10^13, in average polynomial time per prime)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 10, Fast polynomial evaluation and interpolation (subproduct tree and multipoint evaluation), and Section 19.3 (the method of Pollard and Strassen, which evaluates products of blocks of consecutive integers)
---

The problem **factorial modulo a prime** asks for $n! \bmod p$, for an integer $n \ge 0$ and a prime $p$, and in a common variant for $n!$ with all factors $p$ removed. If $n \ge p$, the product contains the factor $p$ and the answer is $0$, so the plain problem has $n < p$. Multiplying $1, 2, \ldots, n$ takes $n$ [modular multiplications](/modular-multiplication/), which is too slow when $p$ has more than about ten decimal digits. [Wilson's theorem](/wilson-theorem/) halves the work, and the blocking method of Pollard and Strassen, with [fast multipoint evaluation](/fast-multipoint-evaluation/), brings the cost down to $O(M(\sqrt{n}) \log n)$ operations modulo $p$; Bostan, Gaudry and Schost remove the factor $\log n$. No algorithm polynomial in $\log p$ is known. The variant with the factors $p$ removed is the basis for [binomial coefficients](/binomial-coefficient-computation/) modulo $p$.

## In plain words

The factorial of a number is the product of all whole numbers from one up to it. These products grow very fast, so we only keep the remainder after division by a fixed prime.

When the number reaches the prime, the prime itself is one of the factors, and the remainder is zero. So the interesting case is a number below a large prime.

The simple method multiplies the numbers one by one and keeps only the remainder. That needs as many steps as the number itself. Faster methods cut the range into blocks of equal length, write the product of one block as a polynomial, and find the values of that polynomial for all blocks at once. This needs only about the square root of the number of steps.

## Definition

**Input.** A prime $p$ and an integer $n \ge 0$.

**Output.** The residue $n! \bmod p$, in $\{0, \ldots, p - 1\}$.

**Variant with the factors $p$ removed.** Let $v_p(n!)$ be the exponent of $p$ in $n!$, given by [Legendre's formula](/legendre-formula/) $v_p(n!) = \sum_{i \ge 1} \lfloor n/p^i \rfloor$. The output is the pair $\bigl(v_p(n!),\ n!_{(p)}\bigr)$, where $n!_{(p)} = n!/p^{v_p(n!)} \bmod p$ is never $0$. The prime $p$ can be small and $n$ can be huge here.

**Representation and cost model.** Residues are integers in $\{0, \ldots, p - 1\}$. On the [word RAM](/word-ram/) with $p < 2^w$, an addition or a multiplication modulo $p$ costs $O(1)$, and costs are counted in these operations. For larger $p$, each operation modulo $p$ costs $O(M(\log p))$ bit operations, where $M(d)$ is the cost of multiplying two $d$-digit numbers. In the bounds below, $M(d)$ also stands for the number of operations in $\mathbb{Z}/p\mathbb{Z}$ that multiply two polynomials of degree less than $d$; it is $O(d \log d \log \log d)$ in any ring and $O(d \log d)$ with a [number theoretic transform](/number-theoretic-transform/).

## Variants

- **Reflection near $p$.** From Wilson's theorem $(p - 1)! \equiv -1 \pmod p$ and $(p - 1)!/n! = \prod_{j=n+1}^{p-1} j \equiv (-1)^{p-1-n} (p - 1 - n)!$, one gets $n! \, (p - 1 - n)! \equiv (-1)^{p - n} \pmod p$. So $n!$ follows from $(p - 1 - n)!$ by one [modular inverse](/modular-inverse/), and only $n \le (p - 1)/2$ needs real work.
- **Factors $p$ removed.** Group $1, \ldots, n$ into the $\lfloor n/p \rfloor$ full blocks of $p$ numbers and a tail of $n \bmod p$ numbers. The parts not divisible by $p$ in each full block multiply to $(p - 1)! \equiv -1$, the tail gives $(n \bmod p)!$, and the multiples $p, 2p, \ldots$ give $p^{\lfloor n/p \rfloor} \lfloor n/p \rfloor!$. So
  $$n!_{(p)} \equiv (-1)^{\lfloor n/p \rfloor} \, (n \bmod p)! \, \lfloor n/p \rfloor!_{(p)} \pmod p,$$
  a loop of $\lfloor \log_p n \rfloor + 1$ steps, each with one factorial of a number below $p$. Legendre's formula also gives $v_p(n!) = (n - s_p(n))/(p - 1)$, with $s_p(n)$ the sum of the digits of $n$ in base $p$.
- **Many queries with one prime.** If $p$ is small enough for a table, compute $k! \bmod p$ for all $k < p$ in $p - 2$ multiplications, and the inverses of all of them with one inversion and $O(p)$ multiplications, as in [batch modular inversion](/batch-modular-inverse/). Every later query costs $O(1)$, or $O(\log_p n)$ with the factors $p$ removed.
- **Many primes with one shape.** The Wilson quotient needs $(p - 1)! \bmod p^2$ for every prime $p$ up to a bound $N$. Costa, Gerbicz and Harvey compute all of them with a remainder tree in average time polynomial in $\log N$ per prime, far below $\sqrt{p}$ each.
- **Prime-power moduli.** For $n!_{(p)} \bmod p^e$, the same idea works with blocks of length $p^e$. The numbers prime to $p$ in a full block multiply to $\pm 1$ modulo $p^e$ (to $-1$ for odd $p$, and for $p = 2$ to $-1$ when $e \le 2$ and to $1$ when $e \ge 3$), the tail is the product of the numbers prime to $p$ up to $n \bmod p^e$, and the multiples of $p$ give $\lfloor n/p \rfloor!_{(p)}$ again. A table of $p^e$ entries makes each step cheap. This is the basis of binomial coefficients modulo $p^e$, and with the Chinese remainder theorem, modulo any $m$.

## Examples

- **Wilson's theorem.** $12! \equiv 12 \equiv -1 \pmod{13}$.
- **Reflection.** For $p = 13$ and $n = 10$: $10! \cdot 2! \equiv (-1)^{3} \pmod{13}$, so $10! \equiv -2^{-1} \equiv -7 \equiv 6 \pmod{13}$, which agrees with $3628800 \bmod 13 = 6$.
- **Blocks.** For $p = 101$, $n = 16$ and block length $s = 4$, let $F(x) = (x + 1)(x + 2)(x + 3)(x + 4)$. Then $F(0), F(4), F(8), F(12) \equiv 24, 64, 63, 48 \pmod{101}$, and their product is $76 \equiv 16! \pmod{101}$.
- **Factors $p$ removed.** $v_5(25!) = 5 + 1 = 6$. The recursion gives $5!_{(5)} \equiv (-1)^1 \cdot 0! \cdot 1! = -1$ and $25!_{(5)} \equiv (-1)^5 \cdot 0! \cdot 5!_{(5)} \equiv 1 \pmod 5$, so $25! = 5^6 \cdot u$ with $u \equiv 1 \pmod 5$. For $100!$ and $p = 7$: $v_7(100!) = 14 + 2 = 16$ and $100!_{(7)} \equiv 4 \pmod 7$.
- **Binomial coefficients.** $\binom{n}{k} = n!/(k!(n - k)!)$ has $p$-exponent $v_p(n!) - v_p(k!) - v_p((n - k)!)$. For $\binom{30}{10}$ and $p = 7$ this exponent is $4 - 1 - 2 = 1$, so $7 \mid \binom{30}{10} = 30045015$. For $\binom{1000}{500}$ it is $0$, and $1000!_{(7)} \cdot (500!_{(7)})^{-2} \equiv 4 \pmod 7$ is the residue, which [Lucas's theorem](/lucas-theorem/) confirms.

## Known algorithms

| algorithm | idea | operations modulo $p$ |
|---|---|---|
| direct product | multiply $1, 2, \ldots, n$ | $n - 1$ |
| direct product with reflection | use $(p - 1 - n)!$ when $n > (p - 1)/2$ | $\min(n, p - 1 - n) + O(\log p)$ |
| Pollard and Strassen | $F(x) = \prod_{j=1}^{s}(x + j)$ with $s = \lfloor \sqrt{n} \rfloor$ by a [subproduct tree](/subproduct-tree/), evaluated at $0, s, \ldots, (s - 1)s$ by [multipoint evaluation](/multipoint-evaluation/), then the remaining $n - s^2$ factors | $O(M(\sqrt{n}) \log n)$ |
| Bostan, Gaudry and Schost | the values of $F$ on an arithmetic progression, computed by doubling $s$ and shifting the progression, without the coefficients of $F$ | $O(M(\sqrt{n}))$ |
| table of all factorials | precompute $k! \bmod p$ for $k < p$ | $O(p)$ once, $O(1)$ per query |
| factors $p$ removed | the recursion above, with any of the methods for the factorials below $p$ | $O(\log_p n)$ factorials of numbers below $p$ |

The method of Bostan, Gaudry and Schost needs the inverses of $1, \ldots, O(\sqrt{n})$ in the ring, which holds modulo $p$ because $n < p$. With an FFT multiplication, both fast methods take $O(\sqrt{p} \log^2 p)$ and $O(\sqrt{p} \log p)$ operations modulo $p$ in the worst case $n \approx p/2$, up to a $\log \log p$ factor in rings without suitable roots of unity.

## Bounds

**Upper bounds.** $O(M(\sqrt{n}))$ operations modulo $p$ for $n < p$, so $O(\sqrt{p} \log p \log \log p)$ in the worst case. With the factors $p$ removed, $O(\log_p n)$ such computations, or $O(p + \log_p n)$ operations with a table.

**Lower bounds.** Every algorithm must read $n$ and $p$, so $\Omega(\log p)$ bit operations are needed. No better lower bound is known, and no algorithm with a cost polynomial in $\log p$ is known. Bostan, Gaudry and Schost note that Chudnovsky and Chudnovsky suggested about $\sqrt{n}$ ring operations as a lower bound for the general problem of one term of a recurrence with polynomial coefficients, of which $n!$ is the simplest case.

**Composite moduli.** For a composite $N$, the factorial modulo $N$ is at least as hard as finding a factor of $N$; see Reductions.

## Reductions

- **To multipoint evaluation.** With $s = \lfloor \sqrt{n} \rfloor$ and $F(x) = (x + 1) \cdots (x + s)$, the product $F(0) F(s) \cdots F((s - 1)s)$ is $(s^2)!$. So the factorial reduces to building one polynomial of degree $s$ and evaluating it at $s$ points, which is [fast multipoint evaluation](/fast-multipoint-evaluation/).
- **Binomial coefficients to factorials.** $\binom{n}{k} \bmod p$ is $0$ when $v_p(n!) - v_p(k!) - v_p((n - k)!) > 0$, and otherwise equals $n!_{(p)} \cdot (k!_{(p)} \, (n - k)!_{(p)})^{-1} \bmod p$. [Lucas's theorem](/lucas-theorem/) is another route for small $p$.
- **Factoring to factorials modulo $N$.** For a composite $N$ with smallest prime factor $q$, $\gcd(k! \bmod N, N) > 1$ exactly when $k \ge q$. A binary search over $k \le \sqrt{N}$ then finds $q$ with $O(\log N)$ factorials modulo $N$. So a method for factorials modulo composite numbers in time polynomial in $\log N$ would factor integers in polynomial time. Strassen's deterministic factoring algorithm uses exactly the blocks of the Pollard and Strassen method, with the gcd taken block by block.
- **Primality to factorials.** By Wilson's theorem and its converse, $n > 1$ is prime if and only if $(n - 1)! \equiv -1 \pmod n$. This test is correct but slower than [Miller-Rabin](/miller-rabin/) or AKS, because no fast factorial algorithm is known.

## Applications

- **Combinatorics modulo a prime.** Counting problems ask for binomial coefficients, multinomial coefficients and Catalan numbers modulo a prime such as $998244353$ or $10^9 + 7$. A table of factorials and inverse factorials up to the largest $n$ answers each query in $O(1)$.
- **Large binomial coefficients.** For $n \ge p$, the version with the factors $p$ removed gives $\binom{n}{k} \bmod p$ and the exact power of $p$ that divides it.
- **Wilson primes.** A prime $p$ is a Wilson prime when $(p - 1)! \equiv -1 \pmod{p^2}$. Only $5$, $13$ and $563$ are known, and the search of Costa, Gerbicz and Harvey found no other below $2 \cdot 10^{13}$.
- **Deterministic factoring.** Strassen's deterministic factoring algorithm evaluates products of blocks of consecutive integers modulo $N$, as in the factorial method. Bostan, Gaudry and Schost reduce its cost to $O(M_{\text{int}}(N^{1/4} \log N))$ bit operations (Theorem 11).

## References
