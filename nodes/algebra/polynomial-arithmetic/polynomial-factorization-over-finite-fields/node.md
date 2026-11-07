---
tag: 64ET21
kind: problem
slug: polynomial-factorization-over-finite-fields
name: Polynomial factorization over finite fields
aliases:
- factoring over GF(p)
- factoring polynomials over F_q
- univariate factorization over finite fields
area: algebra/polynomial-arithmetic
level: advanced
summary: Factor a univariate polynomial over a finite field into monic irreducible factors. Randomized algorithms do it in expected polynomial time; no deterministic one is known.
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of f, q: the number of elements of the field, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {expected: O(n M(n) log(q n) log n)}
prereqs: [irreducible-polynomial, square-free-factorization, polynomial-gcd]
see_also: [cantor-zassenhaus-algorithm, berlekamp-factorization, distinct-degree-factorization, equal-degree-factorization, square-free-factorization, rabin-irreducibility-test, polynomial-factorization-over-integers, reed-solomon-code]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 14, Factoring polynomials over finite fields (Sections 14.2 to 14.3 distinct-degree and equal-degree factorization, 14.6 squarefree factorization, 14.8 Berlekamp's algorithm)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.2, Factorization of Polynomials (factoring modulo p)
  - paper: doi:10.1002/j.1538-7305.1967.tb03174.x
    title: Elwyn R. Berlekamp, Factoring polynomials over finite fields, Bell System Technical Journal 46(8), 1967
    locator: pp. 1853 to 1859
  - paper: doi:10.1090/S0025-5718-1970-0276200-X
    title: Elwyn R. Berlekamp, Factoring polynomials over large finite fields, Mathematics of Computation 24(111), 1970
    locator: pp. 713 to 735
  - paper: doi:10.1090/S0025-5718-1981-0606517-5
    title: David G. Cantor and Hans Zassenhaus, A new algorithm for factoring polynomials over finite fields, Mathematics of Computation 36(154), 1981
    locator: pp. 587 to 592
  - paper: doi:10.1007/BF01272074
    title: Joachim von zur Gathen and Victor Shoup, Computing Frobenius maps and factoring polynomials, Computational Complexity 2, 1992
    locator: pp. 187 to 224
  - paper: doi:10.1090/S0025-5718-98-00944-2
    title: Erich Kaltofen and Victor Shoup, Subquadratic-time factoring of polynomials over finite fields, Mathematics of Computation 67(223), 1998
    locator: pp. 1179 to 1197
  - paper: doi:10.1137/08073408X
    title: Kiran S. Kedlaya and Christopher Umans, Fast polynomial factorization and modular composition, SIAM Journal on Computing 40(6), 2011
    locator: pp. 1767 to 1802
---

Factoring over a finite field $\mathbb{F}_q$ writes a nonzero polynomial $f$ of degree $n$ as $f = c \prod_i g_i^{e_i}$, with distinct monic [irreducible](/irreducible-polynomial/) $g_i$. The standard method has three stages: [square-free factorization](/square-free-factorization/), [distinct-degree factorization](/distinct-degree-factorization/), and [equal-degree factorization](/equal-degree-factorization/). With the randomized [Cantor-Zassenhaus algorithm](/cantor-zassenhaus-algorithm/) the expected cost is polynomial in $n$ and $\log q$, but no deterministic algorithm with that cost is known. Factoring over finite fields is also the first step of factoring over the integers.

## In plain words

Over a finite field, every polynomial splits in exactly one way into pieces that cannot be split further, as a whole number splits into primes. Finding these pieces is much easier than for whole numbers.

The usual method works in three steps. First it separates repeated pieces from single ones. Next it sorts the pieces by their degree, with one special polynomial for each degree, which collects all pieces of that degree. Last it splits each group of equal degree into its pieces. For this last step it makes random guesses, and each guess splits the group with a good chance. So the method is fast on average but uses random choices. Nobody knows a method that is equally fast and makes no random choices.

## Definition

Let $\mathbb{F}_q$ be a finite field with $q = p^k$ elements, $p$ prime.

**Problem.** Given a nonzero $f \in \mathbb{F}_q[x]$ of degree $n$, find $c \in \mathbb{F}_q$, distinct monic irreducible $g_1, \ldots, g_s \in \mathbb{F}_q[x]$, and integers $e_i \ge 1$ with

$$f = c \prod_{i=1}^{s} g_i^{\,e_i}.$$

The factorization exists and is unique up to order, because $\mathbb{F}_q[x]$ is a Euclidean domain; $c = \operatorname{lc}(f)$.

**Cost model.** We count operations in $\mathbb{F}_q$ at unit cost, in the algebraic model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/), and allow random choices of field elements for randomized algorithms. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$. Some results below count bit operations instead; they say so.

**The key fact.** $x^{q^d} - x$ is the product of all monic irreducible polynomials over $\mathbb{F}_q$ whose degree divides $d$. The page on [Rabin's test](/rabin-irreducibility-test/) proves it. All three stages and Berlekamp's method rest on it.

## Variants

- **Root finding.** Find only the factors of degree $1$, that is, the roots in $\mathbb{F}_q$: take $\gcd(x^q - x, f)$ and split it by equal-degree factorization with $d = 1$. Decoders for [Reed-Solomon](/reed-solomon-code/) and [BCH codes](/bch-code/) use this.
- **Irreducibility testing.** Decide only whether $s = 1$ and $e_1 = 1$; see [irreducibility testing](/polynomial-irreducibility-testing/).
- **Counting factors.** For square-free $f$, the number $s$ of irreducible factors is $n$ minus the rank of $Q - I$ in Berlekamp's method, with no splitting.
- **Small and large fields.** For small $p$, deterministic methods in time polynomial in $n$, $p$ and $\log q$ are known, starting with Berlekamp (1967). For large $p$, all known methods that are polynomial in $\log q$ use random choices.
- **Multivariate polynomials** over $\mathbb{F}_q$ are factored by reduction to the univariate case with Hensel lifting; this is a separate problem.

## Examples

A brute-force script checked every factorization below.

- **All irreducibles at once.** Over $\mathbb{F}_2$, $x^8 - x = x\,(x + 1)(x^3 + x + 1)(x^3 + x^2 + 1)$: the product of the monic irreducibles of degree $1$ and $3$, as the key fact says for $d = 3$.
- **Over $\mathbb{F}_3$,** $x^9 - x = x\,(x + 1)(x + 2)(x^2 + 1)(x^2 + x + 2)(x^2 + 2x + 2)$.
- **The same polynomial over different fields.** $x^4 + 1$ is $(x^2 + x + 2)(x^2 + 2x + 2)$ over $\mathbb{F}_3$, $(x^2 + 2)(x^2 + 3)$ over $\mathbb{F}_5$, and $(x + 2)(x + 8)(x + 9)(x + 15)$ over $\mathbb{F}_{17}$. Over $\mathbb{Q}$ it is irreducible.
- **The three stages.** Over $\mathbb{F}_2$ take $f = x^5 + x + 1$. It is square-free, since $\gcd(f, f') = \gcd(f, x^4 + 1) = 1$. Distinct-degree factorization gives $\gcd(x^2 - x, f) = 1$, so no roots; then $\gcd(x^4 - x, f) = x^2 + x + 1$, the product of the factors of degree $2$; the rest, $x^3 + x^2 + 1$, has degree $3$ and is irreducible. So $f = (x^2 + x + 1)(x^3 + x^2 + 1)$, and no equal-degree splitting is needed.
- **One random split.** Over $\mathbb{F}_5$, $f = x^2 + 1$ has two roots. Equal-degree factorization with $d = 1$ picks a random $a$, here $a = x + 1$, and computes $a^{(q-1)/2} = (x + 1)^2 \equiv 2x \pmod f$. Then $\gcd(2x - 1, f) = x - 3$, a factor: $f = (x - 3)(x - 2)$.
- **Repeated factors.** Over $\mathbb{F}_2$, $x^6 + 1 = (x^3 + 1)^2 = (x + 1)^2 (x^2 + x + 1)^2$, and $f' = 0$; the square-free stage takes a square root first.

## Known algorithms

- **Square-free factorization.** Gcds with the derivative and $p$-th roots, $O(M(n) \log n)$ operations plus $p$-th roots of field elements. See [square-free factorization](/square-free-factorization/) and von zur Gathen and Gerhard, Section 14.6.
- **[Distinct-degree factorization](/distinct-degree-factorization/).** For $d = 1, 2, \ldots$, compute $h_d = x^{q^d} \bmod f$ by raising $h_{d-1}$ to the $q$-th power, take $\gcd(h_d - x, f)$, and divide it out. The gcd for $d$ is the product of the irreducible factors of degree $d$. Cost $O(n\, M(n) \log q)$ for the powers plus $O(n\, M(n) \log n)$ for the gcds.
- **[Equal-degree factorization](/equal-degree-factorization/)** of a product of $r$ irreducibles of degree $d$. The [Cantor-Zassenhaus algorithm](/cantor-zassenhaus-algorithm/) (1981): for odd $q$, take a random $a$ and compute $\gcd(a^{(q^d - 1)/2} - 1, f)$, which is a proper factor with probability at least about $1/2$; for $q = 2^k$, use the trace map $a + a^2 + \cdots + a^{2^{kd - 1}}$ instead. Expected $O(\log r)$ rounds.
- **[Berlekamp's algorithm](/berlekamp-factorization/)** (1967). For square-free $f$, solve the linear system $(Q - I) v = 0$, where $Q$ is the matrix of $g \mapsto g^q \bmod f$. Each solution $v$ gives $g$ with $g^q \equiv g$, and $f = \prod_{c \in \mathbb{F}_q} \gcd(g - c, f)$. Deterministic, with cost polynomial in $n$ and $q$: good for small $q$. Berlekamp (1970) gave a randomized version for large $q$.
- **Fast methods.** Von zur Gathen and Shoup (1992) compute the powers $x^{q^d}$ with modular composition and the iterated Frobenius map. Kaltofen and Shoup (1998) factor over a field of constant size in $O(n^{1.815})$ operations, a subquadratic bound. Kedlaya and Umans (2011) give fast modular composition and factor in $O(n^{1.5 + o(1)} \log^{1 + o(1)} q + n^{1 + o(1)} \log^{2 + o(1)} q)$ bit operations, with a randomized algorithm.

## Bounds

- **Expected time.** The three stages with Cantor-Zassenhaus cost an expected $O(n\, M(n) \log(qn) \log n)$ field operations. This follows from the costs above: $O(n)$ powerings by $q$ and $O(n)$ gcds for the distinct-degree stage, and $O(\log n)$ expected rounds of equal-degree splitting with powerings of degree at most $n$. It is a proved bound for the expected cost, and it is not the best known.
- **Bit complexity.** $O(n^{1.5 + o(1)} \log^{1 + o(1)} q + n^{1 + o(1)} \log^{2 + o(1)} q)$ expected bit operations, by Kedlaya and Umans (2011). This is proved.
- **Deterministic algorithms.** Berlekamp's algorithm is deterministic and polynomial in $n$ and $q$. No deterministic algorithm that is polynomial in $n$ and $\log q$ is known, even for root finding of quadratics; finding a quadratic non-residue modulo $p$ deterministically is a special case of this open problem.
- **Lower bound.** $\Omega(n)$ in general; no better lower bound is known in the algebraic model.

## Reductions

- **Factoring reduces to the square-free case** with gcds and $p$-th roots.
- **Square-free factoring reduces to equal-degree factoring** by distinct-degree factorization, which uses only powers and gcds.
- **Factoring reduces to root finding of split polynomials.** For square-free $f$, take $g$ of degree at least $1$ with $g^q \equiv g \pmod f$, as in Berlekamp's method. Then $f = \prod_c \gcd(g - c, f)$ over the roots $c$ in $\mathbb{F}_q$ of the minimal polynomial of $g$ modulo $f$, and that minimal polynomial is a product of distinct linear factors over $\mathbb{F}_q$. Berlekamp (1970) used this reduction.
- **Root finding over $\mathbb{F}_p$ includes square roots modulo $p$:** the roots of $x^2 - a$ are the square roots of $a$.
- **Factoring over $\mathbb{Z}$ reduces to it.** The [Zassenhaus algorithm](/zassenhaus-algorithm/) and its descendants factor modulo a prime $p$ first; see [factorization over the integers](/polynomial-factorization-over-integers/).

## Applications

- **Coding theory.** Root finding of error-locator polynomials in decoders of [Reed-Solomon](/reed-solomon-code/) and [BCH codes](/bch-code/); factors of $x^n - 1$ give the [cyclic codes](/cyclic-code/) of length $n$.
- **Factoring over $\mathbb{Z}$ and $\mathbb{Q}$,** and over number fields, through Hensel lifting.
- **Cryptography.** Point counting and the construction of extension fields; the [index calculus](/index-calculus/) for discrete logarithms in $\mathbb{F}_{2^n}$ factors many polynomials over $\mathbb{F}_2$ to find smooth ones.
- **Computer algebra systems,** where it is a basic routine.

## References
