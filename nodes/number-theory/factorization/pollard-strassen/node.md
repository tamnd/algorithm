---
tag: CC5JPW
kind: algorithm
slug: pollard-strassen
name: Pollard-Strassen algorithm
aliases:
- Pollard-Strassen deterministic factoring
area: number-theory/factorization
level: research
summary: Finds the least prime factor of N deterministically by computing the products of B = ceil(N^(1/4)) blocks of B consecutive integers modulo N with fast multipoint evaluation. Proved bound N^(1/4+o(1)).
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, B: the block length ceil(N^(1/4))}
  time: {worst: N^(1/4+o(1))}
  space: {extra: O(N^(1/4) n)}
  ring_operations: {worst: O(N^(1/4) n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [trial-division, factorial, greatest-common-divisor, fast-multipoint-evaluation, subproduct-tree, polynomial-multiplication]
see_also: [lehman-factorization, pollard-rho, pollard-p-minus-1, wilsons-theorem, kronecker-substitution, newton-power-series-inversion, fast-polynomial-division, integer-factorization]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 5.5, Polynomial evaluation method, pages 238 to 239 (the blocks, the cost O(n^(1/4) ln^2 n) arithmetic operations); Section 6.3, pages 301 to 302 (the fastest rigorously analyzed deterministic method, and Shanks' n^(1/5+o(1)) under the ERH); Algorithm 9.6.7 for the multipoint evaluation
  - paper: doi:10.1017/S0305004100049252
    title: J. M. Pollard, Theorems on factorization and primality testing, Mathematical Proceedings of the Cambridge Philosophical Society 76(3) (1974)
    locator: pages 521 to 528
  - paper: "Volker Strassen, Einige Resultate über Berechnungskomplexität, Jahresbericht der Deutschen Mathematiker-Vereinigung 78, 1976/77"
    locator: pages 1 to 8
  - paper: doi:10.1137/S0097539704443793
    title: Alin Bostan, Pierrick Gaudry and Éric Schost, Linear recurrences with polynomial coefficients and application to integer factorization and Cartier-Manin operator, SIAM Journal on Computing 36(6) (2007)
    locator: pages 1777 to 1806
  - paper: doi:10.1090/S0025-5718-2013-02707-X
    title: Edgar Costa and David Harvey, Faster deterministic integer factorization, Mathematics of Computation 83(285) (2014)
    locator: pages 339 to 345
  - paper: doi:10.1090/mcom/3313
    title: Markus Hittmeir, A babystep-giantstep method for faster deterministic integer factorization, Mathematics of Computation 87(314) (2018)
    locator: pages 2915 to 2935
  - paper: doi:10.1090/mcom/3658
    title: David Harvey, An exponent one-fifth algorithm for deterministic integer factorisation, Mathematics of Computation 90(332) (2021)
    locator: pages 2937 to 2950
---

The Pollard-Strassen algorithm finds the least prime factor of an integer $N$ deterministically in $N^{1/4 + o(1)}$ bit operations, a bound that is proved with no hypothesis. It splits the range $[1, B^2]$, with $B = \lceil N^{1/4} \rceil$, into $B$ blocks of $B$ consecutive integers, and computes the product of each block modulo $N$ at once, by [fast multipoint evaluation](/fast-multipoint-evaluation/) of the polynomial $f(x) = (x + 1)(x + 2) \cdots (x + B)$. The first block whose product shares a factor with $N$ contains the least prime factor, and a scan of that block finds it. For more than forty years this was the best proved deterministic bound for [integer factorization](/integer-factorization/).

## In plain words

[Trial division](/trial-division/) tests the numbers $2, 3, 4, \dots$ one at a time, up to the square root of $N$. You can test many of them at once: multiply a block of consecutive numbers together, reduce modulo $N$, and take one gcd with $N$. The gcd is larger than $1$ exactly when some number in the block shares a factor with $N$.

That alone saves nothing, because each product still needs one multiplication per number. The trick is that all the block products are values of one polynomial at evenly spaced points. Fast polynomial arithmetic computes all these values together in little more time than it takes to write the polynomial down. With blocks of length $N^{1/4}$ and $N^{1/4}$ blocks, the work drops from about $N^{1/2}$ to about $N^{1/4}$.

## The problem

**Input.** An integer $N \ge 2$.

**Output.** The least prime factor $p$ of $N$. So $p = N$ exactly when $N$ is [prime](/prime-number/), and the method is also a deterministic primality test. Applied again to $N/p$, it gives the full factorization.

**Cost model.** The algorithm works in the ring $\mathbb{Z}/N\mathbb{Z}$. An addition or a multiplication modulo $N$ is one ring operation. On the [word RAM](/word-ram/) with $N < 2^w$ a ring operation costs $O(1)$. For an arbitrary-precision $N$ with $n$ binary digits, a ring operation costs $O(n^2)$ bit operations with schoolbook arithmetic and $O(n \log n)$ with the fastest known integer multiplication. The cost of the method depends on the polynomial multiplication used: write $\mathsf M(d)$ for the number of ring operations to multiply two polynomials of degree $d$ over $\mathbb{Z}/N\mathbb{Z}$. FFT-based methods give $\mathsf M(d) = O(d \log d \log \log d)$ over any commutative ring.

## The algorithm

Write $I_j = \{jB + 1, \dots, jB + B\}$ for the $j$-th block, $j = 0, 1, \dots, B - 1$. Then $f(jB) = \prod_{k \in I_j} k$.

```pseudo id=main
POLLARD-STRASSEN(N)                       ▷ N ≥ 2; returns the least prime factor of N
L1  B ← ⌈N^(1/4)⌉                         ▷ the least integer with B⁴ ≥ N
L2  f(x) ← (x + 1)(x + 2) ⋯ (x + B) mod N ▷ by a subproduct tree
L3  v_j ← f(jB) mod N for j = 0, 1, …, B − 1 ▷ by fast multipoint evaluation
L4  for j = 0, 1, …, B − 1 do
L5      if gcd(v_j, N) > 1 then
L6          return the least d in I_j with d ≥ 2 and d | N
L7  return N
```

Line L1 chooses the block length. Since $B^4 \ge N$, the blocks cover all integers up to $B^2 \ge \sqrt N$, which is far enough to reach the least prime factor of a composite $N$. Line L2 builds the coefficients of $f$, a monic polynomial of degree $B$, as the root of a [subproduct tree](/subproduct-tree/) of the linear factors $x + i$. Line L3 evaluates $f$ at the $B$ points $0, B, 2B, \dots, (B - 1)B$; the result $v_j$ is the product of block $I_j$ modulo $N$. Lines L4 and L5 find the first block whose product shares a factor with $N$. Line L6 scans that block by trial division; it does not return the gcd, which may be a product of several primes, or $N$ itself. If no block shares a factor, line L7 reports that $N$ is prime.

**Fast multipoint evaluation.** Build the subproduct tree of the moduli $x - jB$: the leaves are these linear polynomials, and each inner node is the product of its two children. Then go down the tree with remainders: reduce $f$ modulo the root, and reduce the remainder of each node modulo each of its children. At the leaves the remainders are $f(jB)$, because $f \bmod (x - a) = f(a)$. All the moduli are monic, so [polynomial division](/fast-polynomial-division/) needs no inverses modulo $N$, even though $N$ may be composite. With [Newton inversion](/newton-power-series-inversion/) of power series, each division costs $O(\mathsf M(d))$, and the tree costs $O(\mathsf M(B) \log B)$ ring operations in total.

## Example

Let $N = 200633$. Then $B = 22$, because $21^4 = 194481 < N \le 22^4 = 234256$, and the $22$ blocks cover $1$ to $484$, past $\sqrt N \approx 447.9$. The polynomial $f(x) = (x + 1) \cdots (x + 22)$ modulo $N$ has the constant term $22! \bmod N = 119722$ and the coefficient $1 + 2 + \dots + 22 = 253$ at $x^{21}$. The multipoint evaluation gives:

| $j$ | block $I_j$ | $v_j = f(22j) \bmod N$ | $\gcd(v_j, N)$ |
|---|---|---|---|
| 0 | 1 to 22 | 119722 | 1 |
| 1 | 23 to 44 | 88821 | 1 |
| 2 | 45 to 66 | 83241 | 1 |
| 3 | 67 to 88 | 173552 | 1 |
| 4 | 89 to 110 | 79619 | 1 |
| 5 | 111 to 132 | 186275 | 1 |
| 6 | 133 to 154 | 166741 | 1 |
| 7 | 155 to 176 | 126798 | 1 |
| 8 | 177 to 198 | 3308 | 1 |
| 9 | 199 to 220 | 63057 | 1 |
| 10 | 221 to 242 | 199715 | 1 |
| 11 | 243 to 264 | 191445 | 1 |
| 12 | 265 to 286 | 45867 | 1 |
| 13 | 287 to 308 | 128367 | 1 |
| 14 | 309 to 330 | 53210 | 313 |

Each $v_j$ equals the product of the $22$ integers of its block modulo $N$. At $j = 14$, $v_{14} = 53210 = 170 \cdot 313$, so line L6 scans $309, 310, 311, 312, 313$ and returns $313$. Indeed $N = 313 \cdot 641$. The method used $22$ gcds and $5$ trial divisions where plain trial division needs $312$ divisions; the work went into the polynomial arithmetic.

**A gcd equal to $N$.** For $N = 323$, $B = 5$ and the block $I_3 = \{16, \dots, 20\}$ contains both $17$ and $19$. So $v_3 = 0$ and $\gcd(v_3, N) = 323 = N$. Line L6 still returns $17$.

## Correctness

Each $v_j$ is the product of the integers in $I_j$ modulo $N$, because $f(jB) = (jB + 1) \cdots (jB + B)$ is an identity of integers and evaluation commutes with reduction modulo $N$. The gcd of a product with $N$ is larger than $1$ exactly when some factor shares a prime with $N$. Let $p$ be the least prime factor of $N$. No integer $k$ with $2 \le k < p$ shares a prime with $N$, because such a prime would be at most $k < p$. So if $p \le B^2$, the first block with a gcd above $1$ is the block that contains $p$, and the least divisor $d \ge 2$ of $N$ in that block is $p$. If $p > B^2 \ge \sqrt N$, then $N$ has no prime factor up to $\sqrt N$, so $N$ is prime, no block shares a factor with $N$, and line L7 returns $N = p$. The remainder tree is correct because $(f \bmod P) \bmod Q = f \bmod Q$ when $Q$ divides $P$. The full proof is below.

## Complexity

- **Line L2.** The subproduct tree of $B$ linear factors has $\lceil \log_2 B \rceil$ levels, and each level costs at most $\mathsf M(B)$, so $O(\mathsf M(B) \log B)$ ring operations.
- **Line L3.** The tree of the moduli costs the same, and the remainder tree costs $O(\mathsf M(B) \log B)$ more.
- **Lines L4 to L6.** At most $B$ gcds of numbers below $N$, and at most $B$ trial divisions.
- **Total.** With FFT-based polynomial multiplication, $O(B \log^2 B \log \log B)$ ring operations, which Crandall and Pomerance state as $O(N^{1/4} \ln^2 N)$ arithmetic operations with integers of the size of $N$. Each ring operation is $n^{1 + o(1)}$ bit operations, so the total is $N^{1/4 + o(1)}$ bit operations. This is a proved worst-case bound, for every $N$, with no heuristic and no hypothesis.
- **Space.** The subproduct tree holds $O(B \log B) = O(N^{1/4} n)$ residues modulo $N$. Freeing each level after use brings this down to $O(B)$ residues for line L2, but the remainder tree as written keeps the whole tree of moduli.

The implementation below uses schoolbook polynomial arithmetic for short polynomials and [Kronecker substitution](/kronecker-substitution/) for long ones, which turns one polynomial product into one product of large integers. Python multiplies large integers with Karatsuba's method, so the implementation is asymptotically slower than the FFT bound, though still well below the $N^{1/2}$ of trial division.

For comparison, [Pollard's rho](/pollard-rho/) and [SQUFOF](/shanks-squfof/) take about $N^{1/4}$ steps too, but only heuristically, and with $O(1)$ memory. [Lehman's method](/lehman-factorization/) has a proved $O(N^{1/3})$ bound. Under the extended Riemann hypothesis, a method of Shanks with binary quadratic forms runs in $N^{1/5 + o(1)}$ (Crandall and Pomerance, Section 6.3).

## Properties

- **Deterministic and proved.** The output and the cost bound hold for every $N$.
- **Least prime factor.** It returns the least prime factor, not just some factor.
- **A primality test.** For a prime $N$ it returns $N$, in $N^{1/4 + o(1)}$ steps. This is far slower than the polynomial-time [AKS test](/aks-primality-test/) or a probable-prime test, so it is not used for that purpose.
- **Large memory.** It stores about $N^{1/4} \log N$ residues, unlike Pollard's rho with three.
- **Cost independent of the factors.** It does the full polynomial work even when $p$ is small. A real implementation runs trial division first.

## Variants and improvements

- **Wilson's theorem.** The method computes pieces of factorials modulo $N$. If $k! \bmod N$ were cheap, [Wilson's theorem](/wilsons-theorem/) would give a primality test and a binary search on $\gcd(k!, N)$ would give the least prime factor. Pollard-Strassen is the fast way to compute products of consecutive integers modulo $N$ without a factorization of $N$.
- **Linear recurrences.** Bostan, Gaudry and Schost (2007) compute the block products with an algorithm for linear recurrences with polynomial coefficients, which shifts the values of a polynomial instead of using a remainder tree. This lowers the cost to $O(\mathsf M_{\mathrm{int}}(N^{1/4} \log N))$ bit operations, where $\mathsf M_{\mathrm{int}}(k)$ is the cost of multiplying $k$-bit integers.
- **A $\sqrt{\log \log N}$ factor.** Costa and Harvey (2014) improve that bound by a factor of $\sqrt{\log \log N}$.
- **Baby steps and giant steps.** Hittmeir (2018) combines Strassen's method with a [baby-step giant-step](/baby-step-giant-step/) search and gains a factor $\exp(C \log N / \log \log N)$ for a constant $C > 0$.
- **Exponent one-fifth.** Harvey (2021), building on a method of Hittmeir with exponent $2/9$, gives a deterministic algorithm in $O(N^{1/5} (\log N)^{16/5})$ bit operations, the first improvement of the exponent $1/4$ without randomness. Hittmeir's method and Harvey's extension combine ideas from [Lehman's method](/lehman-factorization/) with fast polynomial arithmetic.

## When to use it

In practice, almost never. It is the reference point for the question of how fast factoring can be done with a proof and without randomness, and a classic application of [fast multipoint evaluation](/fast-multipoint-evaluation/). For real numbers, [Pollard's rho](/pollard-rho/), [SQUFOF](/shanks-squfof/) or [Hart's method](/hart-one-line-factorization/) up to about $2^{64}$, and the [elliptic curve method](/elliptic-curve-factorization/) and the [quadratic sieve](/quadratic-sieve/) beyond, are much faster, and their answers can be checked by multiplication.

## Pitfalls

- **Returning the gcd.** The gcd of a block product with $N$ can contain several primes, or be $N$ itself, as for $N = 323$. Scan the block.
- **The block length.** $B = \lfloor N^{1/4} \rfloor$ can be too short: for $N = 323$, $\lfloor 323^{1/4} \rfloor = 4$ and $B^2 = 16 < 17$, so the blocks never reach the least prime factor. Use the least $B$ with $B^4 \ge N$, computed with integers.
- **Division by non-monic polynomials.** Modulo a composite $N$, a leading coefficient may have no inverse. The subproduct tree of $x - a_j$ contains only monic polynomials, so this cannot happen there; keep it that way in variants.
- **The number 1.** Block $I_0$ starts at $1$, which divides every $N$. Start the scan at $2$.
- **Slow multiplication.** With schoolbook polynomial multiplication, $\mathsf M(B) = B^2$, and the whole method costs $O(N^{1/2})$ ring operations, no better than trial division. The gain depends on fast polynomial arithmetic.
- **Memory.** For $N$ near $2^{128}$, $B = 2^{32}$, and the tree needs billions of residues. The method is not practical at sizes where it would beat simpler methods in theory.

## Implementations

## History

John Pollard described the method in his 1974 paper on factorization and primality testing, the same paper that introduced the [$p - 1$ method](/pollard-p-minus-1/), and Volker Strassen gave the same bound in a 1976/77 paper on results in computational complexity. Their $N^{1/4 + o(1)}$ bound remained the best proved deterministic bound for more than forty years. Bostan, Gaudry and Schost (2007) and Costa and Harvey (2014) improved the logarithmic factors. Hittmeir (2018) gave the first superpolynomial improvement, and Harvey (2021) lowered the exponent to $1/5$, after Hittmeir's $2/9$.

## References
