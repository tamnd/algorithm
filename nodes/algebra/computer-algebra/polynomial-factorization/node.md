---
tag: SKJFXT
kind: problem
slug: polynomial-factorization
name: Polynomial factorization
aliases:
- factoring polynomials
- factorization of polynomials
- irreducible factorization
area: algebra/computer-algebra
level: core
summary: Write a polynomial as a product of irreducible polynomials over a given coefficient field or ring.
model: multitape-turing-machine
prereqs: [polynomial-ring, irreducible-polynomial, polynomial-gcd]
see_also: [polynomial-factorization-over-finite-fields, polynomial-factorization-over-integers, square-free-factorization, kronecker-factorization-method, hensel-lifting, lll-algorithm, polynomial-irreducibility-testing, primary-decomposition]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 14, Factoring polynomials over finite fields; Chapter 15, Hensel lifting and factoring polynomials; Chapter 16, Short vectors in lattices (polynomial-time factorization over Q); Section 6.6 (coefficient bounds for factors)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 6, Newton's iteration and the Hensel construction; Chapter 8, Polynomial factorization
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 4.6.2, Factorization of polynomials
  - paper: doi:10.1007/BF01457454
    title: Arjen K. Lenstra, Hendrik W. Lenstra, Jr. and László Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261, 515-534, 1982
    locator: the first polynomial-time algorithm for factoring in Q[x]
  - paper: doi:10.1090/S0025-5718-1981-0606517-5
    title: David G. Cantor and Hans Zassenhaus, A new algorithm for factoring polynomials over finite fields, Mathematics of Computation 36, 587-592, 1981
    locator: the randomized equal-degree splitting
  - paper: "Erich Kaltofen, Polynomial-time reductions from multivariate to bi- and univariate integral polynomial factorization, SIAM Journal on Computing 14(2), 1985"
    locator: the main reduction
---

Polynomial factorization asks for the irreducible factors of a polynomial $f$ over a given coefficient ring: $\mathbb{F}_q$, $\mathbb{Z}$, $\mathbb{Q}$, a number field, or the algebraic closure. Since $R[x_1, \ldots, x_n]$ is a unique factorization domain whenever $R$ is, the answer is unique up to order and unit factors. The problem is easy to state and its difficulty depends strongly on the ring. Over finite fields it is solved in randomized polynomial time by the [Cantor-Zassenhaus algorithm](/cantor-zassenhaus-algorithm/), and deterministically when the field is small by [Berlekamp's algorithm](/berlekamp-factorization/). Over $\mathbb{Q}$, the 1982 LLL algorithm gave the first polynomial-time method. In practice systems reduce modulo a prime, lift with [Hensel lifting](/hensel-lifting/), and recombine the lifted factors. This page states the problem and links to the methods. The pages on [factorization over finite fields](/polynomial-factorization-over-finite-fields/) and [over the integers](/polynomial-factorization-over-integers/) give the details.

## In plain words

Just as $60 = 2^2 \cdot 3 \cdot 5$, a polynomial can be broken into pieces that cannot be broken further, and the pieces are unique. Which pieces count as unbreakable depends on which numbers you allow as coefficients. The polynomial $x^2 - 2$ cannot be split with rational coefficients, but it splits as $(x - \sqrt{2})(x + \sqrt{2})$ if you allow $\sqrt{2}$. A computer can factor polynomials with coefficients modulo a prime very fast, using randomness. For whole-number coefficients, it factors modulo a prime first, then lifts the answer back to whole numbers. The hard part is deciding which of the small pieces belong together.

## Definition

Notation: $R$ is a unique factorization domain, usually a field $K$ (such as $\mathbb{F}_q$, $\mathbb{Q}$ or a number field) or $\mathbb{Z}$. The input is $f \in R[x_1, \ldots, x_n]$ of total degree $d$, with $t$ terms when given in sparse form. Over $\mathbb{Z}$, $\|f\|_\infty$ is the largest absolute value of a coefficient.

**Input.** A nonzero polynomial $f \in R[x_1, \ldots, x_n]$.

**Output.** A unit $u \in R$, pairwise non-associate irreducible polynomials $f_1, \ldots, f_k$ and exponents $e_1, \ldots, e_k \ge 1$ with

$$f = u \, f_1^{e_1} \cdots f_k^{e_k}.$$

Over a field the convention is to make each $f_i$ monic for a fixed [monomial order](/monomial-ordering/), so that the output is unique. Over $\mathbb{Z}$ the content of $f$, the gcd of its coefficients, is usually split off and left unfactored, because factoring it is integer factorization. The problem then concerns the primitive part, which by Gauss's lemma factors over $\mathbb{Z}$ exactly as it factors over $\mathbb{Q}$.

## Variants

- **Square-free factorization.** Write $f = \prod_i g_i^i$ with each $g_i$ square-free and the $g_i$ pairwise coprime. In characteristic $0$ this needs only gcds with derivatives, as in [Yun's algorithm](/yun-square-free-factorization/), and it is the usual first step. See [square-free factorization](/square-free-factorization/).
- **Irreducibility testing.** Decide whether $f$ is irreducible, without finding factors. See [polynomial irreducibility testing](/polynomial-irreducibility-testing/). Over $\mathbb{F}_q$ this is deterministic polynomial time (Rabin's test).
- **Distinct-degree and equal-degree factorization.** Over $\mathbb{F}_q$, first split $f$ into products of irreducible factors of the same degree ([distinct-degree factorization](/distinct-degree-factorization/)), then split each product ([equal-degree factorization](/equal-degree-factorization/)).
- **Root finding.** Find only the factors of degree $1$. Over $\mathbb{F}_q$ this is the special case of equal-degree factorization with degree $1$. Over $\mathbb{R}$ or $\mathbb{C}$ it is a numerical or [root isolation](/real-root-isolation/) problem.
- **Factorization over number fields.** Factor in $\mathbb{Q}(\alpha)[x]$. Trager's norm method (1976) reduces it to factoring over $\mathbb{Q}$.
- **Absolute factorization.** Factor over $\overline{\mathbb{Q}}$ or $\mathbb{C}$, returning factors with coefficients in an explicit number field. For instance, $x^2 + y^2$ is irreducible over $\mathbb{Q}$ but equals $(x + iy)(x - iy)$ over $\mathbb{Q}(i)$.
- **Sparse and black-box factorization.** The input is given by its $t$ nonzero terms, or as a black box that evaluates $f$. The Kaltofen-Trager (1990) algorithm returns black boxes for the factors.

## Examples

- **Over $\mathbb{Q}$, $\mathbb{F}_p$ and number fields.** $x^4 + 1$ is irreducible over $\mathbb{Q}$, but it factors modulo every prime $p$, into linear or quadratic factors. Over $\mathbb{F}_2$ it is $(x + 1)^4$. Over $\mathbb{Q}(\sqrt{2})$ it is $(x^2 - \sqrt{2} x + 1)(x^2 + \sqrt{2} x + 1)$, and over $\mathbb{Q}(i)$ it is $(x^2 - i)(x^2 + i)$. This is the standard example of why factoring modulo one prime does not settle the factorization over $\mathbb{Q}$.
- **All elements of a finite field.** Over $\mathbb{F}_p$, $x^p - x = \prod_{a \in \mathbb{F}_p} (x - a)$.
- **Content over $\mathbb{Z}$.** $6x^2 + 6 = 2 \cdot 3 \cdot (x^2 + 1)$ over $\mathbb{Z}$, where $2$ and $3$ are irreducible factors. Over $\mathbb{Q}$, $6$ is a unit and the factorization is $6 \cdot (x^2 + 1)$.
- **Cyclotomic factors.** $x^6 - 1 = (x - 1)(x + 1)(x^2 + x + 1)(x^2 - x + 1)$ over $\mathbb{Q}$. In general $x^n - 1 = \prod_{m \mid n} \Phi_m(x)$, a product of cyclotomic polynomials.
- **Multivariate.** $x^2 - y^2 = (x - y)(x + y)$. The cusp $y^2 - x^3$ is irreducible even over $\mathbb{C}$, so it is *absolutely irreducible*.

## Known algorithms

| ring | algorithm | cost | status |
|---|---|---|---|
| $\mathbb{F}_q$, univariate | [Berlekamp](/berlekamp-factorization/) (1967) | polynomial in $d$ and $q$; randomized polynomial in $d$ and $\log q$ | proved |
| $\mathbb{F}_q$, univariate | [Cantor-Zassenhaus](/cantor-zassenhaus-algorithm/) (1981) | randomized, about $d^2 \log q$ operations in $\mathbb{F}_q$ up to logarithmic factors, with fast arithmetic | proved, Las Vegas |
| $\mathbb{F}_q$, univariate | Kaltofen-Shoup (1998), Kedlaya-Umans (2008) | randomized, subquadratic in $d$ | proved |
| $\mathbb{Z}$ or $\mathbb{Q}$, univariate | [Zassenhaus](/zassenhaus-algorithm/) (1969): factor mod $p$, [Hensel lifting](/hensel-lifting/), try subsets of factors | exponential in the number of modular factors in the worst case | proved; fast on typical inputs |
| $\mathbb{Z}$ or $\mathbb{Q}$, univariate | Lenstra, Lenstra and Lovász (1982), with the [LLL algorithm](/lll-algorithm/) | polynomial in $d$ and $\log \|f\|_\infty$ | proved |
| $\mathbb{Z}$ or $\mathbb{Q}$, univariate | van Hoeij (2002): recombination by lattice reduction | later proved polynomial (Belabas, van Hoeij, Klüners and Steel); very fast in practice | proved |
| $\mathbb{Z}$ or $\mathbb{Q}$, univariate | [Kronecker](/kronecker-factorization-method/) (1882): interpolation through divisors of values | exponential in $d$ | proved; historical |
| number fields | Trager (1976) norm method; Landau (1985) | polynomial (Landau) | proved |
| multivariate | Hensel lifting from a bivariate or univariate image (Wang 1978, Kaltofen 1985) | polynomial in the dense size, randomized | proved (Kaltofen) |

Over $\mathbb{F}_q$, no deterministic algorithm polynomial in $d$ and $\log q$ is known, even for finding roots. Under the generalized Riemann hypothesis, such algorithms are known for special classes of inputs.

## Bounds

- **Coefficients of factors.** If $g$ divides $f$ in $\mathbb{Z}[x]$ and $\deg g = m$, each coefficient $g_j$ satisfies $|g_j| \le \binom{m}{j} \|f\|_2 \le 2^m \|f\|_2$ (the Landau-Mignotte bound, von zur Gathen and Gerhard, Section 6.6). Hensel lifting must reach a modulus $p^\ell$ beyond twice this bound. The bound is close to tight: factors can have larger coefficients than $f$, as in cyclotomic factors of $x^n - 1$, whose coefficients are unbounded as $n$ grows ($\Phi_{105}$ is the first with a coefficient $-2$).
- **Recombination.** The Swinnerton-Dyer polynomials, such as $x^4 - 10x^2 + 1$ with roots $\pm \sqrt{2} \pm \sqrt{3}$, are irreducible over $\mathbb{Q}$ but split into factors of degree at most $2$ modulo every prime. For the generalization with $k$ square roots, of degree $2^k$, there are at least $2^{k-1}$ modular factors, so Zassenhaus's subset search takes exponential time. This is what LLL and van Hoeij avoid.
- **Sparse inputs.** A sparse polynomial can have dense factors: $x^n - 1$ has $2$ terms, and its factors $\Phi_m$ can have many. Plaisted (1977) showed that some questions about sparse polynomials, such as whether two of them have a nontrivial common factor, are NP-hard. So no algorithm polynomial in the sparse size $t \log d$ is expected for general sparse factorization.
- **Integer factorization.** Factoring constants in $\mathbb{Z}[x]$ is integer factorization, for which no polynomial-time classical algorithm is known.

## Reductions

- **To square-free inputs.** A [square-free factorization](/square-free-factorization/) reduces the problem to square-free polynomials with gcds only.
- **From $\mathbb{Q}$ to $\mathbb{F}_p$.** Factor modulo a prime that does not divide the discriminant, lift with [Hensel lifting](/hensel-lifting/), and recombine.
- **From many variables to two, and from two to one.** Kaltofen (1985) reduces multivariate factorization over $\mathbb{Z}$ in polynomial time to bivariate and then univariate factorization, using effective Hilbert irreducibility to keep factors irreducible under random substitutions.
- **From number fields to $\mathbb{Q}$.** Trager's method factors the norm $\operatorname{res}_y(\mu(y), f(x - cy, y))$ over $\mathbb{Q}$ and takes gcds with $f$, where $\mu$ is the [minimal polynomial](/minimal-polynomial-algebraic-element/) of the generator.
- **To lattice reduction.** LLL and van Hoeij reduce recombination to finding short vectors in a lattice.

## Applications

- Simplification and normal forms in computer algebra, and the Bernoulli and Trager methods of [rational integration](/integration-of-rational-functions/).
- [Primary decomposition](/primary-decomposition/) and the decomposition of varieties into irreducible components, which start from factoring polynomials in a triangular or eliminated basis.
- Coding theory: list decoding of Reed-Solomon codes (Guruswami-Sudan) finds the linear factors $y - g(x)$ of a bivariate polynomial.
- Constructing finite fields $\mathbb{F}_{p^n}$ needs an irreducible polynomial of degree $n$, and cryptography over finite fields depends on such constructions.

## References
