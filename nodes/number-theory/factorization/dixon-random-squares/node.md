---
tag: 11JRDA
kind: algorithm
slug: dixon-random-squares
name: Dixon's random squares algorithm
aliases:
- Dixon's factorization method
area: number-theory/factorization
level: advanced
summary: Draws random z, keeps those with z^2 mod N smooth, and combines them by linear algebra mod 2 into a congruence of squares. The first factoring method with a proved subexponential expected time.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, K: the number of primes up to the bound B, I: the limit on draws}
  time: {worst: O(I K + K^3), expected: exp((8^(1/2) + o(1)) (ln N ln ln N)^(1/2)), heuristic: exp((2 + o(1)) (ln N ln ln N)^(1/2))}
  space: {extra: O(K^2)}
properties: {deterministic: false, recursive: false}
prereqs: [congruence-of-squares, relation-collection, smooth-number, gaussian-elimination]
see_also: [continued-fraction-factorization, quadratic-sieve, factor-base, nontrivial-square-root-of-one, subexponential-time, index-calculus, pollard-strassen, integer-factorization]
sources:
  - paper: "John D. Dixon, Asymptotically fast factorization of integers, Mathematics of Computation 36(153), 1981"
    locator: pages 255 to 260 (the random squares algorithm and the proof of its expected subexponential running time)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 6.3, Rigorous factoring, pages 301 to 302 (Dixon's bound with c equal to the square root of 8, the improvements by Pomerance and Vallée to the square root of 4/3, and the class group relations method); Section 6.1.1, pages 261 to 266 (relations and the linear algebra)
  - paper: "Carl Pomerance, A tale of two sieves, Notices of the American Mathematical Society 43(12), 1996"
    locator: pages 1473 to 1485 (the random squares idea as the model for the sieve methods)
---

Dixon's random squares algorithm factors an integer $N$ by drawing random $z$ and keeping those for which $z^2 \bmod N$ is [smooth](/smooth-number/) over the primes up to a bound $B$. When it has more of these [relations](/relation-collection/) than primes, linear algebra over the field with two elements gives a product $X^2 \equiv Y^2 \pmod N$, a [congruence of squares](/congruence-of-squares/), and $\gcd(X - Y, N)$ splits $N$ with probability at least $1/2$. Because the $z$ are truly random, John Dixon could prove in 1981 an expected running time of $\exp((\sqrt 8 + o(1))\sqrt{\ln N \ln \ln N})$, the first proved subexponential bound for factoring. In practice it is much slower than the [quadratic sieve](/quadratic-sieve/), which uses the same plan with smaller residues.

## In plain words

Pick random numbers, square each, and take the remainder after division by the number to factor. Keep only the random numbers whose remainder breaks completely into small primes from a fixed list.

For each kept number, note for each small prime whether it appears an odd or an even number of times. When there are more kept numbers than primes in the list, some group of them has remainders whose product is a perfect square. The product of that group of random numbers then has the same square, modulo the number, as the square root of that product. One gcd then gives a factor with a chance of at least one half.

The method is slow, because a random remainder is large and rarely breaks into small primes. Its value is that its speed can be proved.

## The problem

**Input.** An integer $N \ge 3$, a smoothness bound $B$, a count $E \ge 1$ of extra relations, a limit $I$ on the number of draws, and a source of uniform random numbers.

**Output.** A proper factor $g$ of $N$ (with $1 < g < N$), or $1$ for a failure. A prime $N$ always gives $1$. If $N$ is odd and has at least two distinct prime factors, and the run collects $|F| + E$ relations, the output is a proper factor with probability at least $1/2$.

**The factor base.** $F$ is the set of all primes $p \le B$, with $K = |F|$. Unlike in the [quadratic sieve](/quadratic-sieve/), every prime can divide a value $z^2 \bmod N$, so no prime is left out. A prime of $F$ that divides $N$ never divides $z^2 \bmod N$ for a $z$ prime to $N$.

**Cost model.** On the [word RAM](/word-ram/) with $N < 2^w$, a draw, a square modulo $N$, a gcd and a division by a prime of $F$ each cost $O(1)$, so a draw with its smoothness test costs $O(K)$. For an arbitrary-precision $N$ with $n$ binary digits, each of these operations costs $O(n^2)$ bit operations or less. The proved bound is for the expected time over the random draws, for every $N$; it holds for odd $N$ with at least two distinct prime factors, with a suitable choice of $B$ and no limit $I$.

## The algorithm

$R$ is the list of relations, each a pair of $z$ and the exponent vector of $z^2 \bmod N$ over $F$.

```pseudo id=main
DIXON(N, B, E, I)                 ▷ N ≥ 3; returns a proper factor of N or 1
L1  F ← the primes p ≤ B, R ← empty
L2  while |R| < |F| + E and fewer than I draws were made do
L3      z ← a uniform random integer in [1, N − 1], g ← gcd(z, N)
L4      if g > 1 then return g
L5      if z² mod N factors completely over F then append (z, its exponent vector) to R
L6  for each nonempty subset T of R whose exponent vectors add to 0 mod 2, found by Gaussian elimination over GF(2) do
L7      X ← ∏ of the z in T mod N, e ← the sum of the exponent vectors in T, Y ← ∏ over p in F of p^(e_p/2) mod N
L8      g ← gcd(X − Y, N); if 1 < g < N then return g
L9  return 1
```

Line L1 builds the factor base. Lines L2 to L5 collect relations: a draw that shares a factor with $N$ ends the run at once with a proper factor, since $z < N$. The others are tested for smoothness by trial division. With $|F| + E$ relations the exponent vectors mod 2 have at least $E$ dependencies, and line L6 finds them by [Gaussian elimination](/gaussian-elimination/) with a record of which rows were added. Lines L7 and L8 turn each dependency into $X^2 \equiv Y^2 \pmod N$ and try the gcd.

## Example

Let $N = 91363 = 211 \cdot 433$, $B = 7$, so $F = \{2, 3, 5, 7\}$, and $E = 1$, so the loop needs $5$ relations. With Python's `random.Random(30)` as the source, $145$ draws are needed, none shares a factor with $N$, and $5$ of them are smooth:

| draw | $z$ | $z^2 \bmod N$ | factored | vector mod 2 |
|---|---|---|---|---|
| 31 | 32587 | 420 | $2^2 \cdot 3 \cdot 5 \cdot 7$ | $(0, 1, 1, 1)$ |
| 124 | 4287 | 14406 | $2 \cdot 3 \cdot 7^4$ | $(1, 1, 0, 0)$ |
| 137 | 65076 | 28000 | $2^5 \cdot 5^3 \cdot 7$ | $(1, 0, 1, 1)$ |
| 143 | 18166 | 400 | $2^4 \cdot 5^2$ | $(0, 0, 0, 0)$ |
| 145 | 51078 | 256 | $2^8$ | $(0, 0, 0, 0)$ |

The elimination first finds that the first three vectors add to zero. Their product is $2^8 \cdot 3^2 \cdot 5^4 \cdot 7^6$, so $Y = 2^4 \cdot 3 \cdot 5^2 \cdot 7^3 \bmod N = 46148$. But $X = 32587 \cdot 4287 \cdot 65076 \bmod N = 46148$ as well, so $X = Y$ and the gcd is $N$: a trivial dependency. The next dependency is the fourth relation alone, $18166^2 \equiv 20^2$. Here $X = 18166$, $Y = 20$, and $\gcd(18146, 91363) = 211$. So $91363 = 211 \cdot 433$.

## Correctness

Each relation is $z^2 \equiv \prod_{p \in F} p^{v_p} \pmod N$. For a subset $T$ whose vectors add to $0$ mod 2, all entries of $e$ are even, so $\prod_{z \in T} z^2 \equiv \prod_p p^{e_p} = Y^2$, that is, $X^2 \equiv Y^2 \pmod N$. Every $g$ that the algorithm returns is a gcd with $N$ and is tested to lie strictly between $1$ and $N$ (at line L4, $1 \le z < N$ makes $g < N$). The draws are bounded by $I$ and the subsets by $|R|$, so the algorithm stops.

The success probability is where randomness enters. For a $z$ prime to $N$, the value $z^2 \bmod N$ has exactly $2^r$ square roots among the units, where $r$ is the number of distinct prime factors of an odd $N$, and $z$ is uniform among them. All the choices of the algorithm, the relations, the vectors and the subsets $T$, depend only on the values $z^2 \bmod N$. So for a fixed $T$, the product $X$ is uniform among the $2^r$ square roots of $Y^2$, and $X \equiv \pm Y$, the only case with a trivial gcd, has probability $2^{1-r} \le 1/2$. The full proof is below.

## Complexity

- **Per draw.** $O(1)$ for the draw, the square and the gcd, and $O(K)$ for the trial division by the primes of $F$, on the word RAM.
- **With the limit $I$.** $O(IK)$ for the collection and $O(K^3)$ for the elimination of a $(K + E) \times K$ matrix over GF(2), or $O(K^3/w)$ with rows packed in words. This is a proved bound for given parameters.
- **Proved expected time.** Dixon proved that with $B$ of the form $\exp(c' \sqrt{\ln N \ln \ln N})$ the expected running time to split $N$ is $\exp((c + o(1))\sqrt{\ln N \ln \ln N})$ with $c = \sqrt 8$, for every odd $N$ with at least two distinct prime factors. Pomerance, and later Brigitte Vallée, lowered $c$ to $\sqrt{4/3}$; both improvements use the elliptic curve method as a fast smoothness test (Crandall and Pomerance). The proof needs a lower bound on the number of $z$ with $z^2 \bmod N$ smooth, which Dixon obtains by counting products of small primes.
- **Heuristic time.** If the values $z^2 \bmod N$ are as often smooth as random numbers below $N$, then with $B = L_N[1/2, 1/2]$ the probability of smoothness is $L_N[1/2, -1 + o(1)]$, about $L_N[1/2, 3/2]$ draws are needed, and each costs $O(K) = L_N[1/2, 1/2]$. The total is $L_N[1/2, 2]$.
- **Space.** $O(K^2)$ for the matrix, and $O(K)$ numbers modulo $N$ for the relations.

## Properties

- **Randomized, with a proof.** The analysis needs no unproved hypothesis about smooth numbers in special sequences; it uses only that $z$ is uniform. The heuristic methods, [CFRAC](/continued-fraction-factorization/) and the [quadratic sieve](/quadratic-sieve/), are faster but have no such proof.
- **Large residues.** The values $z^2 \bmod N$ are about as large as $N$, while those of CFRAC are below $2\sqrt{N}$. This is why the method is slow in practice.
- **No sieve.** The values follow no polynomial, so each must be tested by trial division or another smoothness test.
- **Success at least one half.** Each dependency splits an odd $N$ with two or more distinct prime factors with probability at least $1/2$, and more when $N$ has more prime factors. It never splits a prime power $p^j$ with odd $p$, since then $r = 1$.

## Variants and improvements

- **Smaller squares.** Take $z$ near $\sqrt{kN}$ for various $k$, so that $z^2 - kN$ is small. This is the idea that leads to the [quadratic sieve](/quadratic-sieve/), at the price of the proof.
- **Faster smoothness tests.** The [elliptic curve method](/elliptic-curve-factorization/) recognizes most $B$-smooth numbers quickly, and it can be used inside a rigorous algorithm because it needs to work only often enough. This is part of the improvement to $c = \sqrt{4/3}$.
- **Large primes.** As in the sieve methods, values that are smooth except for one larger prime can be paired. See [relation collection](/relation-collection/).
- **The class group relations method.** Lenstra and Pomerance (1992) proved an expected time of $\exp((1 + o(1))\sqrt{\ln N \ln \ln N})$ with relations in class groups, the lowest proved bound for a randomized factoring algorithm.

## When to use it

Dixon's method is a tool for proofs and for teaching. It shows that factoring has a randomized algorithm with a proved subexponential expected time, and it is the simplest form of the relation and linear algebra plan. For actual factoring, use the [quadratic sieve](/quadratic-sieve/) or the [number field sieve](/general-number-field-sieve/) for large $N$, and [Pollard's rho](/pollard-rho/) or [ECM](/elliptic-curve-factorization/) for small factors.

## Pitfalls

- **Prime powers.** For $N = p^j$ with odd $p$, every dependency gives $X \equiv \pm Y$. Test for perfect powers first.
- **Even $N$.** The argument for probability $1/2$ needs $N$ odd. Remove the factors $2$ first.
- **A small factor base for large $N$.** If $B$ is much too small, the values are almost never smooth and the loop runs to the limit. Choose $B$ near $\exp(\frac{1}{2}\sqrt{\ln N \ln \ln N})$.
- **Duplicated draws.** If the same $z$ is drawn twice, the two relations alone form a dependency with $X = Y = z^2 \bmod N$, which is trivial. This is rare for large $N$ and does no harm, since each other dependency is still a fresh try.
- **Too few relations.** With exactly $K$ relations there may be no dependency. Collect $E$ extra so that several dependencies give several tries.

## Implementations

## History

John Dixon published the random squares method in 1981 in "Asymptotically fast factorization of integers". It was the first factoring algorithm with a proved subexponential expected running time; the continued fraction method of Morrison and Brillhart from the early 1970s was faster but only heuristic. Carl Pomerance and Brigitte Vallée later improved the constant in the proved bound. In 1992 Hendrik Lenstra and Pomerance proved the bound $\exp((1 + o(1))\sqrt{\ln N \ln \ln N})$ for a method based on class groups, the same bound that the quadratic sieve has heuristically (Crandall and Pomerance).

## References
