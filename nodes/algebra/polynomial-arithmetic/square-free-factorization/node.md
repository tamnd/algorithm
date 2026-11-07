---
tag: G72R9E
kind: problem
slug: square-free-factorization
name: Square-free factorization
aliases:
- square-free decomposition
- squarefree factorization
area: algebra/polynomial-arithmetic
level: advanced
summary: Write a polynomial as a product of square-free polynomials with pairwise coprime factors.
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of the input polynomial f, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(M(n) log n)}
prereqs: [square-free-polynomial, polynomial-gcd]
see_also: [yun-square-free-factorization, square-free-polynomial, polynomial-gcd, discriminant, multiplicity-of-roots, distinct-degree-factorization, polynomial-factorization-over-finite-fields, polynomial-factorization-over-integers]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 14.6, Squarefree factorization (p. 393; Yun's algorithm and the case of finite fields)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.2, Factorization of Polynomials (squarefree factorization by gcds with the derivative, and p-th roots over finite fields)
  - paper: doi:10.1145/800205.806320
    title: David Y. Y. Yun, On square-free decomposition algorithms, SYMSAC 1976
    locator: pp. 26 to 35
  - paper: doi:10.1145/321879.321890
    title: David R. Musser, Multivariate polynomial factorization, Journal of the ACM 22(2), 1975
    locator: pp. 291 to 308 (square-free decomposition as the first step of factoring)
  - paper: doi:10.1007/BF01613611
    title: Patrizia Gianni and Barry Trager, Square-free algorithms in positive characteristic, Applicable Algebra in Engineering, Communication and Computing 7(1), 1996
    locator: pp. 1 to 14
---

Square-free factorization writes a nonzero polynomial $f$ over a field as $f = c\, a_1 a_2^2 a_3^3 \cdots a_k^k$, where each $a_i$ is monic and [square-free](/square-free-polynomial/), and the $a_i$ are pairwise coprime. The factor $a_i$ is the product of the irreducible factors of $f$ that occur exactly $i$ times, but it is found with [gcds](/polynomial-gcd/) and derivatives alone, without factoring. In characteristic $0$, [Yun's algorithm](/yun-square-free-factorization/) does it at the cost of a constant number of gcds of degree $n$. It is the first step of almost every factoring and root-finding method, because those methods need square-free inputs.

## In plain words

A polynomial can contain the same factor several times, like a number that contains the same prime twice. Many methods work only when no factor is repeated. Square-free factorization sorts the factors by how many times they occur: one group for the factors that occur once, one for those that occur twice, and so on. It does this without finding the factors themselves.

The tool is the derivative. A factor that occurs several times in a polynomial also occurs in its derivative, one time fewer. So the common part of the polynomial and its derivative holds exactly the repeated factors, and repeated common parts sort them by count. Over finite fields the derivative can be zero, and a different step is needed.

## Definition

Let $F$ be a field and $f \in F[x]$ nonzero of degree $n$.

**Problem.** Find $c \in F$ and monic polynomials $a_1, \ldots, a_k \in F[x]$, with $a_k \ne 1$ when $n \ge 1$, such that

$$f = c\, \prod_{i=1}^{k} a_i^{\,i},$$

each $a_i$ is square-free, and $\gcd(a_i, a_j) = 1$ for $i \ne j$. Some $a_i$ with $i < k$ may be $1$. For a constant $f$, $k = 0$ and $c = f$.

**Existence and uniqueness.** Let $f = c \prod_p p^{e_p}$ be the factorization into monic irreducible polynomials, which exists and is unique in $F[x]$. Then $a_i = \prod_{e_p = i} p$ is a solution, and $c = \operatorname{lc}(f)$. Conversely, in any solution, each monic irreducible $p \mid f$ divides exactly one $a_i$, because the $a_i$ are coprime, and divides it once, because $a_i$ is square-free. So $p$ occurs in $f$ exactly $i$ times, and $a_i$ is the product above. The solution is unique.

**Related quantities.** The *square-free part* of $f$ is $a_1 a_2 \cdots a_k$, the product of the distinct monic irreducible factors. In characteristic $0$, $\gcd(f, f') = \prod_i a_i^{\,i-1}$ and the square-free part is $f / \gcd(f, f')$ up to the constant.

**Cost model.** Costs count field operations at unit cost, in the algebraic model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/). Over a finite field $\mathbb{F}_q$, $q = p^r$, we also allow $p$-th roots of field elements, which cost $O(\log q)$ multiplications as $c^{1/p} = c^{p^{r-1}}$. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$.

## Variants

- **Characteristic $0$**, or characteristic $p > n$. The derivative never vanishes on a factor, and gcds with the derivative suffice.
- **Finite fields.** A factor of multiplicity divisible by $p$ disappears from the derivative information, and $f' = 0$ is possible for $f \ne$ constant: then $f = g(x^p) = h^p$ for some $h$, whose coefficients are $p$-th roots of those of $g$. Knuth, Section 4.6.2, and von zur Gathen and Gerhard, Section 14.6, combine the derivative step with $p$-th roots.
- **Imperfect fields.** Over $\mathbb{F}_p(t)$, $p$-th roots may not exist in the field, and $x^p - t$ is irreducible, so square-free, with derivative $0$. Gianni and Trager (1996) treat square-free decomposition in this setting.
- **Over $\mathbb{Z}$ and $\mathbb{Q}$.** Write $f = \operatorname{cont}(f) \operatorname{pp}(f)$, as on the [primitive polynomial](/primitive-polynomial/) page, and factor the primitive part over $\mathbb{Q}$. By Gauss's lemma the factors can be taken primitive in $\mathbb{Z}[x]$; the integer content is then factored as an integer, if at all.
- **Distinct-degree factorization** is the next stage over finite fields: it splits a square-free polynomial by the degrees of its irreducible factors; see [distinct-degree factorization](/distinct-degree-factorization/).
- **Multivariate polynomials.** The same method works with partial derivatives and multivariate gcds; Musser (1975) uses it as the first step of multivariate factoring.

## Examples

All factorizations below were checked by a script.

- Over $\mathbb{Q}$, $x^5 - x^4 - 2x^3 + 2x^2 + x - 1 = (x - 1)^3 (x + 1)^2$, so $a_1 = 1$, $a_2 = x + 1$, $a_3 = x - 1$.
- Over $\mathbb{Q}$, $x^8 - 2x^7 + 2x^6 - 4x^5 + x^4 - 2x^3 = (x - 2)(x^2 + 1)^2 x^3$, so $a_1 = x - 2$, $a_2 = x^2 + 1$, $a_3 = x$. The factor $x^2 + 1$ is irreducible over $\mathbb{Q}$, but the algorithm does not need to know it.
- Over $\mathbb{Z}$, $2x^3 + 2x^2 - 2x - 2 = 2 (x - 1)(x + 1)^2$: the content $2$ goes into $c$, and $a_1 = x - 1$, $a_2 = x + 1$.
- $x^4$ over any field gives $a_1 = a_2 = a_3 = 1$ and $a_4 = x$.
- **The derivative can vanish.** Over $\mathbb{F}_2$, $f = x^4 + x^2 + 1$ has $f' = 4x^3 + 2x = 0$. Indeed $f = (x^2 + x + 1)^2$, and the square root is found by taking the square root of each coefficient and halving the exponents.
- **A factor whose multiplicity is $p$.** Over $\mathbb{F}_3$, $f = (x + 1)^3 (x + 2) = x^4 + 2x^3 + x + 2$. Then $f' = x^3 + 1 = (x + 1)^3$, so $\gcd(f, f') = (x + 1)^3$, not $(x + 1)^2$: the factor $(x+1)^3$ is a cube, so its derivative $3(x+1)^2$ vanishes. The derivative method alone returns $a_1 = x + 2$ and loses $(x + 1)^3$; the finite-field method takes a cube root of $\gcd(f, f')$ to find it.

## Known algorithms

- **Repeated gcds.** Compute $g_1 = \gcd(f, f')$, then the square-free part $w = f / g_1$, and repeatedly $y = \gcd(w, g)$, $a_i = w / y$, $w \leftarrow y$, $g \leftarrow g / y$. In characteristic $0$ this is correct, and its cost is $O(n^2)$ with the Euclidean algorithm, but its gcd inputs shrink more slowly than in Yun's algorithm. Musser (1975) uses a method of this kind as the first step of factoring.
- **[Yun's algorithm](/yun-square-free-factorization/)** (1976). It uses the gcds $a_i = \gcd(b_i, d_i)$ of smaller and smaller polynomials, with $d_i$ built from derivatives, so that the degrees of all gcd inputs add up to $n$. Its cost is at most a constant times the cost of one gcd of degree $n$: $O(n^2)$ with the Euclidean algorithm and $O(M(n) \log n)$ with a fast gcd.
- **Finite fields.** Apply the characteristic-$0$ method to get the factors whose multiplicity is not divisible by $p$; what remains is a polynomial in $x^p$, so a $p$-th power. Take its $p$-th root and repeat on it with multiplicities multiplied by $p$. This is the algorithm of Knuth, Section 4.6.2, and of von zur Gathen and Gerhard, Section 14.6. Its cost is $O(M(n) \log n)$ operations plus $O(n)$ $p$-th roots.
- **Over $\mathbb{Z}$**, use modular or subresultant gcds, such as [Brown's modular gcd](/brown-modular-gcd/) or the [subresultant algorithm](/subresultant-gcd/), to avoid fractions.

## Bounds

- **Upper bound.** $O(M(n) \log n)$ field operations in characteristic $0$, by Yun's algorithm with a fast Euclidean algorithm. This is a proved bound.
- **Relation to the gcd.** Yun (1976) showed that square-free factorization is not harder than a gcd, up to a constant factor. In characteristic $0$ it costs at most a constant times the cost $G(n)$ of a gcd of two polynomials of degree $n$, if $G(n)/n$ is nondecreasing; the page on [Yun's algorithm](/yun-square-free-factorization/) proves this.
- **Lower bound.** $\Omega(n)$ in general, since the output depends on all coefficients. No better lower bound is known in the algebraic model.

## Reductions

- **Square-free factorization reduces to gcds.** In characteristic $0$, Yun's algorithm uses gcds of total input degree $2n$ and divisions.
- **Square-freeness testing reduces to one gcd.** In characteristic $0$ and over finite fields, $f$ is square-free exactly when $\gcd(f, f') = 1$, or when the [discriminant](/discriminant/) is nonzero.
- **Factoring reduces to the square-free case.** Factor each $a_i$; the irreducible factors of $a_i$ are the factors of multiplicity $i$ in $f$.
- **Root multiplicities.** The roots of $a_i$ are the roots of $f$ of [multiplicity](/multiplicity-of-roots/) exactly $i$.

## Applications

- **Factoring.** Algorithms over finite fields, such as [Berlekamp's](/berlekamp-factorization/) and [Cantor-Zassenhaus](/cantor-zassenhaus-algorithm/), and over the integers, such as the [Zassenhaus algorithm](/zassenhaus-algorithm/), start with a square-free input. See [factorization over finite fields](/polynomial-factorization-over-finite-fields/) and [over the integers](/polynomial-factorization-over-integers/).
- **Real root isolation.** [Sturm sequences](/sturm-sequence/) and the [Vincent-Collins-Akritas method](/vincent-collins-akritas/) count each root once when the input is square-free; the square-free factors also give the multiplicities.
- **Symbolic integration.** Hermite reduction for rational functions uses the square-free factorization of the denominator to find the rational part of the integral without factoring.
- **Partial fractions** and the simplification of algebraic expressions.

## References
