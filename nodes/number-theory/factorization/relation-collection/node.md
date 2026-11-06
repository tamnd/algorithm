---
tag: B1J4S7
kind: concept
slug: relation-collection
name: Relation collection
aliases:
- sieving for relations
- smooth relations
area: number-theory/factorization
level: advanced
summary: The core of sieve factoring. Collect more congruences x^2 ≡ a (mod N) with smooth a than there are primes in the factor base, then find a square product by linear algebra over GF(2).
prereqs: [smooth-number, factor-base, congruence-of-squares, gaussian-elimination]
see_also: [dixon-random-squares, continued-fraction-factorization, quadratic-sieve, general-number-field-sieve, index-calculus, structured-gaussian-elimination, block-lanczos-algorithm, block-wiedemann-algorithm]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 6.1.1, Basic QS, pages 261 to 266 (relations, exponent vectors and the count of relations needed); Section 6.1.3, Fast matrix methods, pages 268 to 270; Section 6.1.4, Large prime variations, pages 270 to 273
  - paper: "Arjen K. Lenstra and Mark S. Manasse, Factoring with two large primes, Mathematics of Computation 63(208), 1994"
    locator: pages 785 to 798 (the double large prime variation and the search for cycles)
  - paper: "Carl Pomerance, A tale of two sieves, Notices of the American Mathematical Society 43(12), 1996"
    locator: pages 1473 to 1485 (the exponent vectors, the linear algebra over GF(2), and the balance between sieving and matrix work)
  - paper: "Peter L. Montgomery, A block Lanczos algorithm for finding dependencies over GF(2), Advances in Cryptology, EUROCRYPT '95, Lecture Notes in Computer Science 921, 1995"
    locator: pages 106 to 120
---

Relation collection is the shared core of the subexponential factoring methods: [Dixon's method](/dixon-random-squares/), [CFRAC](/continued-fraction-factorization/), the [quadratic sieve](/quadratic-sieve/) and the [number field sieve](/general-number-field-sieve/). A relation is a congruence $x^2 \equiv a \pmod N$ in which $a$ is [smooth](/smooth-number/), that is, it factors over a fixed [factor base](/factor-base/) of $K$ small primes. Once more than $K$ relations are known, linear algebra over the field with two elements finds a subset whose right sides multiply to a perfect square, and this gives a [congruence of squares](/congruence-of-squares/) that splits $N$ with probability about $1/2$ or more. The methods differ only in how they produce the values $x$ and how fast they find the smooth ones.

## In plain words

Pick a short list of small primes. Then look for many numbers whose square, after you remove multiples of the number to factor, breaks up completely into primes from the list. Each such number is a relation.

For each relation, write down for every prime in the list whether it appears an odd or an even number of times. That is a row of zeros and ones. When you have more rows than primes in the list, some group of rows must add up to all zeros, if you add without carry. Multiply the relations of that group together: the right side is then a perfect square. This gives two numbers with the same square, and a gcd computation then splits the number with a fair chance.

Almost all of the work is the search for relations. The final step with zeros and ones is short by comparison.

## The idea

Let $N$ be an odd composite number that is not a prime power, and let $F = \{p_1, \dots, p_K\}$ be the factor base: the primes up to a bound $B$ (in the sieve methods, only those for which $N$ is a [quadratic residue](/quadratic-residue/)), often with $p_0 = -1$ added so that negative values can be used.

**Relations and exponent vectors.** A relation is an integer $x$ with
$$x^2 \equiv a \pmod N, \qquad a = \prod_{i=1}^{K} p_i^{e_i},$$
where $a$ is the value that the method computes (for example $a = x^2 - N$ in the quadratic sieve). Its exponent vector is $v(x) = (e_1 \bmod 2, \dots, e_K \bmod 2) \in \mathbb F_2^K$. A product of values $a$ is a square exactly when the sum of their exponent vectors, taken modulo $2$, is the zero vector.

**Enough relations give a square.** $\mathbb F_2^K$ has dimension $K$, so any $K + 1$ vectors in it are linearly dependent: there is a nonempty subset $S$ of the relations with $\sum_{x \in S} v(x) = 0$. Over $\mathbb F_2$ the only nonzero coefficient is $1$, so a dependency is just a subset. Each further relation beyond $K$ gives one more independent dependency, so $K + r$ relations give at least $r$ of them.

**From a dependency to a factor.** For a subset $S$ with $\sum_{x \in S} v(x) = 0$, let $E_i = \sum_{x \in S} e_i(x)$, which is even for every $i$, and put
$$X = \prod_{x \in S} x \bmod N, \qquad Y = \prod_{i=1}^{K} p_i^{E_i/2} \bmod N.$$
Then $X^2 \equiv \prod_{x \in S} a(x) = \prod_i p_i^{E_i} = Y^2 \pmod N$. If $X \not\equiv \pm Y \pmod N$, then $\gcd(X - Y, N)$ is a proper factor of $N$: $N$ divides $(X - Y)(X + Y)$ but neither factor. In Dixon's method, where each $x$ is uniform at random, the value $x$ is independent of the residue class of $x^2$ given $x^2$, and if $N$ has $r \ge 2$ distinct prime factors each class $x^2$ has $2^r$ square roots modulo $N$ that are equally likely. Then $X \equiv \pm Y$ for at most $2$ of the $2^r$ choices, so a dependency fails with probability at most $2^{1 - r} \le 1/2$ (Crandall and Pomerance, Section 6.1.1, and the [congruence of squares](/congruence-of-squares/) page). For the sieve methods, where $x$ is not random, the same rate is a heuristic that matches practice. With $10$ or $20$ spare dependencies, failure on all of them is rare.

**The stages.** A program built on relation collection has the same five stages whatever the method:

1. Choose the factor base: $B$ and the primes $p \le B$ that can divide the values $a$.
2. Collect relations, more than $K$. This is where the methods differ, and it takes nearly all the time.
3. Filter: remove duplicate relations, and remove the relations that contain a prime that occurs in no other relation (a singleton prime can never have an even total exponent). Repeat, since each removal can create new singletons.
4. Find dependencies of the matrix of exponent vectors over $\mathbb F_2$.
5. For each dependency, compute $X$ and $Y$ and try $\gcd(X - Y, N)$.

**The balance of the bound $B$.** A larger $B$ makes smooth values more common, but more relations are needed, about $\pi(B)$, and the matrix grows. If the values $a$ have size about $N^{\theta}$ and $\rho(u)$ with $u = \ln N^{\theta}/\ln B$ is the [Dickman](/dickman-function/) estimate of the chance that one is $B$-smooth, the expected number of values to test is about $\pi(B)/\rho(u)$. The minimum over $B$ falls at $B = L_N[1/2, c]$ for a constant $c$ that depends on $\theta$ and on the cost of one smoothness test, and the total cost is then $L_N[1/2, c']$; see [smooth number](/smooth-number/) for the calculation. In the [quadratic sieve](/quadratic-sieve/), $\theta = 1/2$, sieving makes each test cost $O(\log \log B)$ on average, and the heuristic cost is $L_N[1/2, 1]$ with $B = L_N[1/2, 1/2]$ (Crandall and Pomerance, Section 6.1.1).

**Linear algebra.** The matrix has about $K$ rows and $K$ columns, but only $O(\log N)$ nonzero entries per row.

- [Gaussian elimination](/gaussian-elimination/) over $\mathbb F_2$ costs $O(K^3)$ bit operations, or $O(K^3/w)$ word operations when $w$ entries are packed in a machine word. It is fine for small factorizations.
- [Structured Gaussian elimination](/structured-gaussian-elimination/) first eliminates the sparse columns, which leaves a much smaller dense matrix.
- The [block Lanczos](/block-lanczos-algorithm/) and [block Wiedemann](/block-wiedemann-algorithm/) methods use only products of the sparse matrix with vectors. They cost $O(K \cdot W)$, where $W$ is the number of nonzero entries, so $K^{2 + o(1)}$, which matches the sieving time of the quadratic sieve and keeps the total at $L_N[1/2, 1]$.

**Large prime variations.** Sieving finds, at no extra cost, values that are smooth except for one prime $P$ with $B < P \le B^2$: if the cofactor after removing the primes up to $B$ is greater than $1$ and less than $B^2$, it must be a prime. Such a partial relation is useless alone, but two partial relations $x_1^2 \equiv y_1 P$ and $x_2^2 \equiv y_2 P$ with the same $P$ give $(x_1 x_2)^2 \equiv y_1 y_2 P^2$, a full relation with the exponent vector of $y_1 y_2$. Sorting the partial relations by $P$ finds the matches, and by the [birthday paradox](/birthday-paradox/) the number of matches grows like the square of the number of partials, so they become an important source of rows late in the run. With $k$ partials for the same $P$, one uses the $k - 1$ products $y_1 y_i$. The double large prime variation of Lenstra and Manasse also keeps cofactors that are products of two primes above $B$. Then one builds a graph whose vertices are $1$ and the large primes, with an edge $\{1, P\}$ for each single partial and $\{P_1, P_2\}$ for each double partial; each cycle in this graph is a set of partials whose product has every large prime to an even power, so it is a full relation. A graph with $V$ vertices, $E$ edges and $C$ connected components has exactly $E - V + C$ independent cycles, which a union-find pass counts.

## Examples

**A full run.** Let $N = 87463$ and $B = 30$. The primes $p \le 30$ for which $N$ is a quadratic residue modulo $p$ (and $p = 2$) form the factor base $F = \{2, 3, 13, 17, 19, 29\}$, so $K = 6$. Testing $x = 296, 297, \dots, 355$ with $a = x^2 - N$ gives five full relations.

| $x$ | $x^2 - N$ | factorization | vector over $(2, 3, 13, 17, 19, 29)$ |
|---|---|---|---|
| 296 | 153 | $3^2 \cdot 17$ | $(0, 0, 0, 1, 0, 0)$ |
| 299 | 1938 | $2 \cdot 3 \cdot 17 \cdot 19$ | $(1, 1, 0, 1, 1, 0)$ |
| 307 | 6786 | $2 \cdot 3^2 \cdot 13 \cdot 29$ | $(1, 0, 1, 0, 0, 1)$ |
| 316 | 12393 | $3^6 \cdot 17$ | $(0, 0, 0, 1, 0, 0)$ |
| 347 | 32946 | $2 \cdot 3 \cdot 17^2 \cdot 19$ | $(1, 1, 0, 0, 1, 0)$ |

Five vectors in a space of dimension six need not be dependent, but these are. The rows for $296$ and $316$ are equal, so $153 \cdot 12393 = 3^8 \cdot 17^2$ is a square. Then $X = 296 \cdot 316 \bmod N = 6073$ and $Y = 3^4 \cdot 17 = 1377$, and $\gcd(6073 - 1377, 87463) = \gcd(4696, 87463) = 587$. So $87463 = 149 \cdot 587$.

The rows for $296$, $299$ and $347$ also add to zero. Here the product is $2^2 \cdot 3^4 \cdot 17^4 \cdot 19^2$, so $Y = 2 \cdot 3^2 \cdot 17^2 \cdot 19 = 98838 \equiv 11375$, and $X = 296 \cdot 299 \cdot 347 \bmod N = 11375$. Since $X = Y$, this dependency gives only $\gcd(0, N) = N$. This is the failure case $X \equiv \pm Y$, and it is why one wants several dependencies.

**Single large primes.** In the same range, $302^2 - N = 3741 = 3 \cdot 29 \cdot 43$ and $343^2 - N = 30186 = 2 \cdot 3^3 \cdot 13 \cdot 43$ are smooth except for the same prime $43 > B$. Their product is $43^2 \cdot 2 \cdot 3^4 \cdot 13 \cdot 29$, so the pair is a full relation for $x = 302 \cdot 343 \bmod N = 16123$, with vector $(1, 0, 1, 0, 0, 1)$. In the range $296$ to $355$ there are four such pairs, with large primes $43$, $103$, $127$ and $229$.

**A cycle with two large primes.** For $x = 324$, $x^2 - N = 17513 = 83 \cdot 211$, a double partial. With the single partials $309^2 - N = 8018 = 2 \cdot 19 \cdot 211$ and $423^2 - N = 91466 = 2 \cdot 19 \cdot 29 \cdot 83$, the edges $\{1, 211\}$, $\{211, 83\}$, $\{83, 1\}$ form a cycle. The product of the three values is $(2 \cdot 19 \cdot 83 \cdot 211)^2 \cdot 29$, a full relation with vector $(0, 0, 0, 0, 0, 1)$.

## Where it is used

- **[Dixon's random squares](/dixon-random-squares/).** The $x$ are random, and the smoothness of $x^2 \bmod N$ is tested by [trial division](/trial-division/). This is the version with a proved expected running time, $L_N[1/2, 2\sqrt 2]$ in Dixon's analysis.
- **[CFRAC](/continued-fraction-factorization/).** The $x$ are the numerators of the convergents of $\sqrt{kN}$, whose residues are below $2\sqrt{kN}$.
- **The [quadratic sieve](/quadratic-sieve/) and [MPQS](/multiple-polynomial-quadratic-sieve/).** The values $a$ are the values of quadratic polynomials, and a sieve finds the smooth ones without trial division.
- **The [number field sieve](/general-number-field-sieve/).** A relation is a pair $(a, b)$ such that $a - bm$ is smooth over the integers and $a - b\alpha$ is smooth over prime ideals of a number ring. The exponent vectors have parts for both sides and some quadratic characters, and the matrix step is done with block Lanczos or block Wiedemann on matrices with millions of rows.
- **[Index calculus](/index-calculus/) for discrete logarithms.** The relations are the same, but the linear algebra is modulo the group order instead of modulo $2$, since one needs the exponents, not only their parities.

## References
