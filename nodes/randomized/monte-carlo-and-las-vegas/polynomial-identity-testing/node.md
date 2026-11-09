---
tag: M50GS4
kind: problem
slug: polynomial-identity-testing
name: Polynomial identity testing
aliases:
- PIT
- identity testing for arithmetic circuits
area: randomized/monte-carlo-and-las-vegas
level: core
summary: Decide whether a polynomial given as a formula or arithmetic circuit is identically zero; random evaluation solves it with one-sided error, and no deterministic polynomial-time algorithm is known.
prereqs: [polynomial-ring, schwartz-zippel-lemma, one-sided-error]
see_also: [schwartz-zippel-lemma, matrix-product-verification, tutte-matrix, rnc-perfect-matching, aks-primality-test, hitting-set-generator, straight-line-program, co-rp]
sources:
  - paper: doi:10.1145/322217.322225
    title: Jacob T. Schwartz, Fast probabilistic algorithms for verification of polynomial identities, Journal of the ACM 27(4), 1980
    locator: pages 701 to 717 (random evaluation of polynomial identities, with the bound d/|S|)
  - paper: "Valentine Kabanets and Russell Impagliazzo, Derandomizing polynomial identity tests means proving circuit lower bounds, Computational Complexity 13(1-2), 2004"
    title: Valentine Kabanets and Russell Impagliazzo, Derandomizing polynomial identity tests means proving circuit lower bounds
    locator: pages 1 to 46, main theorem (a deterministic polynomial-time PIT algorithm implies that NEXP is not in P/poly or that the permanent has no polynomial-size arithmetic circuits)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 7, Section 7.2 (polynomial identity testing for arithmetic circuits over the integers, with reduction modulo a random number); Chapter 20 (derandomization of PIT and circuit lower bounds)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 7, Algebraic techniques (verifying polynomial identities and perfect matchings in graphs)
  - paper: "Manindra Agrawal and Somenath Biswas, Primality and identity testing via Chinese remaindering, Journal of the ACM 50(4), 2003"
    title: Manindra Agrawal and Somenath Biswas, Primality and identity testing via Chinese remaindering
    locator: pages 429 to 443 (a randomized identity test with few random bits, and the primality test from the identity (x + 1)^n = x^n + 1 modulo n)
---

Polynomial identity testing (PIT) asks whether a polynomial, given in a compact form such as an arithmetic circuit, is the zero polynomial. Expanding the circuit into monomials can take exponential time, because a small circuit can have exponentially many terms and exponential degree. Evaluating it at a random point is fast, and by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) a nonzero polynomial of degree $d$ is nonzero at a random point of $S^m$ with probability at least $1 - d/|S|$. So PIT has a randomized polynomial-time algorithm with [one-sided error](/one-sided-error/). Whether it has a deterministic one is a central open problem, and Kabanets and Impagliazzo (2004) showed that a deterministic algorithm would prove circuit lower bounds that are not known today.

## In plain words

You get a recipe that builds a number from some unknown inputs by adding and multiplying, perhaps with a lot of reuse of earlier results. You must decide whether the recipe always gives zero, as a formula, whatever the inputs are.

Writing out the formula in full can give a result too long to write down. Instead, choose random inputs from a large enough set and follow the recipe. If the result is not zero, the recipe is surely not zero. If the result is zero, the recipe is probably zero, and trying a few more random inputs makes the doubt as small as you like. Nobody knows how to do this as fast without random choices.

## Definition

Notation on this page: $F$ is a field, $m$ is the number of variables, $s$ is the size of the circuit, $d$ is the degree of the polynomial, and $\Pr$ is over the random point only.

An **arithmetic circuit** over $F$ is a directed acyclic graph. Its sources are the variables $x_1, \dots, x_m$ and constants from $F$; each other node is a $+$ gate or a $\times$ gate with two inputs; one node is the output. It computes a polynomial $P_C \in F[x_1, \dots, x_m]$ in the obvious way. The *size* $s$ is the number of nodes. A *formula* is a circuit whose gates have out-degree 1. A circuit is also called a [straight-line program](/straight-line-program/).

**Polynomial identity testing.**

- *Input:* an arithmetic circuit $C$ over $F$.
- *Question:* is $P_C = 0$ as a polynomial, that is, is every coefficient of $P_C$ zero?

Testing whether two circuits $C_1$ and $C_2$ compute the same polynomial is the same problem for the circuit $C_1 - C_2$.

The question is about the formal polynomial, not about the function $F^m \to F$. Over a finite field these differ: over $\mathbb{F}_p$ the polynomial $x^p - x$ is nonzero, but it is zero at every point of $\mathbb{F}_p$. Over an infinite field they agree.

**Degree and size.** A circuit of size $s$ has degree at most $2^{s}$: $s$ squarings of $x$ give $x^{2^s}$. Over $\mathbb{Z}$ its coefficients and its values at small points can have $2^{O(s)}$ bits. Both facts shape the algorithms below.

## Variants

- **White-box and black-box.** In the white-box form, the algorithm reads the circuit. In the black-box form, it can only evaluate $P_C$ at points of its choice (perhaps in an extension field). The random algorithm is black-box. A deterministic black-box algorithm is the same as an explicit *hitting set*: a set $H$ of points such that every nonzero polynomial of the class is nonzero somewhere on $H$. See [hitting set generator](/hitting-set-generator/).
- **Formulas, circuits and low-degree circuits.** For formulas and for circuits with degree at most polynomial in $s$, the random algorithm works directly over a large enough field. For general circuits the degree can be $2^s$, which needs $|S| > 2^s$, so elements of $O(s)$ bits.
- **Over the integers.** The values can have $2^{O(s)}$ bits, too many to compute. The standard fix computes modulo a random integer of $O(s)$ bits; a nonzero value is nonzero modulo a random such number with good probability. Arora and Barak give the details.
- **Restricted classes.** Sparse polynomials (few monomials, black-box), read-once branching programs, depth-3 circuits with bounded top fan-in, and symbolic determinants of matrices whose entries are linear forms (Edmonds' problem) are studied as special cases. Several of them have deterministic polynomial-time or quasi-polynomial-time algorithms; the symbolic determinant in general does not.
- **Degree 1.** When the polynomial is $\sum_j D_{ij} x_j$ for a matrix $D$ given in factored form $D = AB - C$, PIT is [matrix product verification](/matrix-product-verification/).

## Examples

- **A square of a sum.** $C_1 = (x + y)(x + y)$ and $C_2 = x \cdot x + 2 \cdot x \cdot y + y \cdot y$. Over $\mathbb{F}_{101}$ at $(x, y) = (3, 4)$ both give 49. The difference $C_1 - C_2$ is the zero polynomial, so every point agrees. With $C_2' = x \cdot x + y \cdot y$, the difference is $2xy$, which is zero at only 201 of the $10201$ points of $\mathbb{F}_{101}^2$.
- **Vandermonde determinant.** The identity $\det\big(x_i^{\,j-1}\big)_{i,j=1}^{n} = \prod_{i<j} (x_j - x_i)$ has degree $n(n-1)/2$ on each side. Expanding the determinant has $n!$ terms, but both sides can be evaluated at a random point in $O(n^3)$ field operations. At $(x_1, x_2, x_3) = (2, 5, 7)$ both sides are $3 \cdot 5 \cdot 2 = 30$. See [Vandermonde matrix](/vandermonde-matrix/).
- **A circuit of exponential degree.** Over $\mathbb{F}_2$, square $(x + 1)$ $s$ times and subtract $x^{2^s} + 1$, also built by $s$ squarings. The result is zero, because $(a + b)^2 = a^2 + b^2$ in characteristic 2. The degree is $2^s$, larger than $|\mathbb{F}_2| = 2$, so a test over $\mathbb{F}_2$ itself proves nothing; the test must pick $S$ in an extension field $\mathbb{F}_{2^t}$ with $2^t \ge 2^{s+1}$, for an error at most $1/2$.
- **Perfect matchings.** A graph has a [perfect matching](/perfect-matching/) if and only if the determinant of its [Tutte matrix](/tutte-matrix/) is a nonzero polynomial. The circuit is a determinant of a matrix with variable entries, of degree $n$.

## Known algorithms

- **Random evaluation.** Pick $r$ uniformly from $S^m$ with $|S| \ge 2d$, evaluate $C$ at $r$ in $O(s)$ field operations, and say "zero" if and only if the value is 0. If $P_C = 0$ the answer is always right. If $P_C \ne 0$ it is wrong with probability at most $d/|S| \le 1/2$, by the Schwartz-Zippel lemma. With $k$ independent points the error is at most $2^{-k}$, see [error amplification](/error-amplification/). This places PIT in [co-RP](/co-rp/) (the zero polynomials form a co-RP language) for circuits whose values can be computed in polynomial time.
- **Fewer random bits.** Agrawal and Biswas (2003) gave a test that uses fewer random bits, by testing the identity modulo a random polynomial of small degree. Pairwise independent points (see [k-wise independence](/k-wise-independence/)) also save random bits at the cost of a slower fall of the error.
- **Deterministic, by brute force.** Expand the circuit into monomials, in time exponential in $s$ in the worst case. Or use a grid: a nonzero polynomial of degree at most $d$ in each variable is nonzero somewhere on $S^m$ with $|S| = d + 1$, by the individual-degree form of the lemma. This needs $(d + 1)^m$ evaluations.
- **Deterministic, for special classes.** Polynomial-time or quasi-polynomial-time algorithms exist for several restricted classes, such as sparse polynomials and some classes of low-depth circuits. No deterministic polynomial-time algorithm is known for general circuits or formulas.

## Bounds

- **Upper bound.** PIT for circuits whose values can be computed in polynomial time is in co-RP, so in [BPP](/bpp/) and in [co-NP](/co-np/).
- **Derandomization and lower bounds.** Kabanets and Impagliazzo (2004) proved that if PIT has a deterministic polynomial-time algorithm, then NEXP $\not\subseteq$ P/poly or the permanent has no arithmetic circuits of polynomial size. Either conclusion is a circuit lower bound far beyond current techniques. In the other direction, lower bounds for explicit polynomials give hitting sets and so deterministic tests, in the style of the [Nisan-Wigderson generator](/nisan-wigderson-generator/). So derandomizing PIT and proving arithmetic circuit lower bounds are nearly equivalent.
- **No lower bound.** No superlinear lower bound on the time of PIT is known, and it could be in P.

## Reductions

- **Perfect matching to PIT.** By the Tutte matrix, as above. The random test decides perfect matching with one evaluation of a determinant, and it gives the parallel algorithm of [RNC perfect matching](/rnc-perfect-matching/).
- **Primality to PIT.** An integer $n \ge 2$ is prime if and only if $(x + 1)^n = x^n + 1$ in $(\mathbb{Z}/n\mathbb{Z})[x]$. This is an identity test for a circuit of size $O(\log n)$ with repeated squaring, but over a ring that is not a field and with degree $n$. Agrawal and Biswas (2003) tested it modulo random polynomials. The [AKS primality test](/aks-primality-test/) derandomizes this one instance: it checks the identity modulo $x^r - 1$ for a small $r$ and a few values in place of 1, and it is the main example of a PIT instance with a known deterministic polynomial-time algorithm.
- **Matrix product verification to PIT.** $AB = C$ if and only if the linear polynomial vector $(AB - C)x$ is zero. [Freivalds' algorithm](/freivalds-algorithm/) is random evaluation of it.
- **Equivalence of read-once branching programs.** Two read-once branching programs compute the same Boolean function if and only if their arithmetized polynomials are equal, which is a PIT instance.

## Applications

- Testing algebraic identities in computer algebra and in symbolic geometry theorem proving, the motivation of Schwartz (1980).
- Randomized and parallel algorithms for matching, through the Tutte and Edmonds matrices.
- [Fingerprinting](/fingerprinting/) of strings and files, where a string is the coefficient vector of a univariate polynomial.
- Interactive proofs and probabilistically checkable proofs, where the verifier checks low-degree polynomial identities at random points.
- Program checking: compare a fast matrix product or polynomial product with a random evaluation of the claimed answer.

## References
