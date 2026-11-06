---
tag: 9TE35V
kind: problem
slug: integer-relation-problem
name: Integer relation problem
aliases:
- integer relation detection
- integer relation finding
- linear dependence over the integers
area: number-theory/lattice-reduction
level: advanced
summary: Given real numbers, find a nonzero integer vector whose dot product with them is zero.
prereqs: [lattice, euclidean-algorithm, continued-fraction]
see_also: [pslq-algorithm, lll-algorithm, simultaneous-diophantine-approximation, approximate-svp, short-integer-solution, polynomial-factorization, lattice-basis-reduction, shortest-vector-problem]
sources:
  - paper: "H. R. P. Ferguson, D. H. Bailey and S. Arno, Analysis of PSLQ, an integer relation finding algorithm, Mathematics of Computation 68(225) (1999)"
    locator: pages 351 to 369 (the PSLQ algorithm, its iteration bound and the lower bound on relation norms)
  - paper: "J. Håstad, B. Just, J. C. Lagarias and C. P. Schnorr, Polynomial time algorithms for finding integer relations among real numbers, SIAM Journal on Computing 18(5) (1989)"
    locator: pages 859 to 881 (the HJLS algorithm in a model of exact real arithmetic)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 2.7.2, Linear and algebraic dependence using LLL (finding integer relations and minimal polynomials with a lattice of the form identity plus a scaled column)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 17, Applications of basis reduction (small linear relations, knapsacks and simultaneous Diophantine approximation)
---

The integer relation problem asks, for real numbers $x_1, \ldots, x_n$, for integers $m_1, \ldots, m_n$, not all zero, with $m_1 x_1 + \cdots + m_n x_n = 0$. For $n = 2$ it is the question whether $x_1 / x_2$ is rational, answered by the [Euclidean algorithm](/euclidean-algorithm/) and [continued fractions](/continued-fraction/). For larger $n$ it is solved by [lattice basis reduction](/lattice-basis-reduction/) and by the [PSLQ algorithm](/pslq-algorithm/), and it is how experimental mathematics finds identities such as minimal polynomials and formulas for constants from numerical values.

## In plain words

You are given a few numbers, perhaps known to many decimal places. You want to know whether some combination of them with whole-number weights adds up to exactly zero, and to find the weights if so.

With two numbers, this asks whether one is a fraction times the other, and the old method of repeated division finds the fraction. With more numbers, a method is needed that keeps trying combinations in an organized way, making the weights small while pushing the sum towards zero. When the numbers are only known approximately, the answer is a guess backed by evidence: a relation with small weights that holds to far more digits than chance would allow.

## Definition

**Input.** A vector $x = (x_1, \ldots, x_n) \in \mathbb{R}^n$, $n \ge 2$, with $x \ne 0$.

**Output.** A vector $m \in \mathbb{Z}^n \setminus \{0\}$ with $\langle m, x \rangle = \sum m_i x_i = 0$, called an **integer relation** for $x$, or a proof that no relation of norm at most a given bound $M$ exists.

The relations form the lattice $\Lambda(x) = \{m \in \mathbb{Z}^n : \langle m, x \rangle = 0\}$, of some rank $r \le n - 1$. The usual goal is a short relation, a short vector of $\Lambda(x)$, because short relations are the meaningful ones.

**Models of input.** The meaning of "given real numbers" matters.

- **Exact real arithmetic.** In a model where $+, -, \times, /$ and comparison of reals cost one step, the HJLS and PSLQ algorithms find a relation, if one exists, in a number of steps polynomial in $n$ and $\log M$, where $M$ is the norm of a shortest relation. Without any relation they run forever, but at every step they give a lower bound on the norm of any relation.
- **Finite precision.** In practice $x$ is known to $D$ digits. Then only approximate relations can be found: $m$ with $\|m\|$ small and $|\langle m, x \rangle| \le \varepsilon$. A relation found this way is accepted when it holds to many more digits than its size explains, and is then proved by other means.
- **Rational input.** If $x \in \mathbb{Z}^n$, relations always exist for $n \ge 2$, and the problem is to find a short one: the [shortest vector problem](/shortest-vector-problem/) on the lattice $\Lambda(x)$ of rank $n - 1$.

## Variants

- **Small linear forms.** Find $m \ne 0$ with $\|m\| \le M$ and $|\langle m, x \rangle|$ as small as possible; the finite-precision form of the problem.
- **Algebraic dependence.** For $\alpha$ real or complex, a relation for $(1, \alpha, \ldots, \alpha^d)$ is a polynomial with integer coefficients that vanishes at $\alpha$; the shortest one gives the minimal polynomial. This is the basis of the Kannan, Lenstra and Lovász method for algebraic numbers and of a step in [polynomial factorization](/polynomial-factorization/).
- **Simultaneous relations.** Find $m$ orthogonal to several vectors at once, or a basis of all relations $\Lambda(x)$.
- **Modular relations.** Find $m \ne 0$ small with $\langle m, x \rangle \equiv 0 \pmod q$; with several vectors $x$ this is the [short integer solution](/short-integer-solution/) problem of lattice cryptography.
- **The dual problem.** [Simultaneous Diophantine approximation](/simultaneous-diophantine-approximation/) asks for one integer $q$ that makes all $q x_i$ close to integers; the two problems are related by transference.

## Examples

- **The golden ratio.** For $x = (1, \varphi, \varphi^2)$ with $\varphi = (1 + \sqrt5)/2$, the relation $m = (1, 1, -1)$ holds because $\varphi^2 = \varphi + 1$. Reducing the lattice below with $C = 10^6$ returns $(-1, -1, 1)$ as its first vector.
- **A minimal polynomial.** For $\alpha = \sqrt2 + \sqrt3 \approx 3.1462643699$ and $x = (1, \alpha, \alpha^2, \alpha^3, \alpha^4)$, the relation $(1, 0, -10, 0, 1)$ gives $\alpha^4 - 10 \alpha^2 + 1 = 0$, the minimal polynomial of $\alpha$. The lattice method below with $C = 10^{12}$ finds it as the first vector of the reduced basis; the second vector has entries in the hundreds, so the first stands out.
- **No relation.** For $x = (1, \sqrt2)$ no relation exists, because $\sqrt2$ is irrational. The convergents of the continued fraction $[1; 2, 2, 2, \ldots]$ give approximate relations such as $(41, -29)$, with $41 - 29\sqrt2 \approx -0.0122$, and $(8119, -5741)$, with $8119 - 5741\sqrt2 \approx -6.2 \cdot 10^{-5}$. With $\sqrt 2$ known to 5 decimals, the input error times 5741 exceeds $6.2 \cdot 10^{-5}$, so the second looks exact; in exact arithmetic PSLQ never stops on this input, but the lower bound it reports for the norm of any relation keeps growing.
- **Constants.** The Bailey, Borwein and Plouffe formula $\pi = \sum_k 16^{-k} \big(\tfrac{4}{8k+1} - \tfrac{2}{8k+4} - \tfrac{1}{8k+5} - \tfrac{1}{8k+6}\big)$ was found in 1995 by running PSLQ on $\pi$ and the eight series $\sum_k 16^{-k}/(8k + j)$, $j = 1, \ldots, 8$.

## Known algorithms

The cost model is stated for each method: exact real arithmetic (each real operation one step) or integer arithmetic on numbers of $D$ digits.

- **Euclid and continued fractions** ($n = 2$). The continued fraction of $x_1 / x_2$ terminates if and only if a relation exists, and its convergents give the relation; $O(\log M)$ steps.
- **Lattice reduction** (Lenstra, Lenstra and Lovász, 1982; Kannan, Lenstra and Lovász, 1988). Round $C x_i$ to integers $c_i$ for a large scale $C$ and reduce the basis with rows
  $$(1, 0, \ldots, 0, c_1), \ (0, 1, \ldots, 0, c_2), \ \ldots, \ (0, \ldots, 0, 1, c_n).$$
  A lattice vector is $(m_1, \ldots, m_n, \sum m_i c_i)$, so a short vector has small $m$ and small $\sum m_i c_i \approx C \langle m, x \rangle$. [LLL](/lll-algorithm/) finds a vector within a factor $2^{(n-1)/2}$ of the shortest, in time polynomial in $n$ and in the number of digits of $C x$. The scale $C$ must be large, roughly $M^n$ up to factors exponential in $n$, for the true relation to be the shortest vector, so the method needs $D = \Omega(n \log M)$ digits.
- **Ferguson and Forcade (1979).** The first algorithm for $n \ge 3$ that is guaranteed to find a relation if one exists.
- **HJLS (Håstad, Just, Lagarias and Schnorr, 1989).** In exact real arithmetic, finds a relation within a factor $2^{n/2}$ of the shortest, or proves that none of norm below a bound exists, with a number of steps polynomial in $n$ and $\log M$. It is based on LLL applied to a basis that is updated as the numbers are processed.
- **[PSLQ](/pslq-algorithm/) (Ferguson and Bailey, 1992; analysed by Ferguson, Bailey and Arno, 1999).** Finds a relation in a number of iterations polynomial in $n$ and $\log M$, proved in exact arithmetic, and is numerically stable in multiprecision floating point. Each iteration gives a lower bound on the norm of any relation. It is the standard tool in experimental mathematics, with multi-level and parallel variants by Bailey and Broadhurst.

## Bounds

- **Polynomial time with exact reals.** HJLS and PSLQ find some relation in time polynomial in $n$ and $\log M$, where $M$ is the norm of a shortest relation; the relation found is within a factor exponential in $n$ of the shortest.
- **Shortest relation.** Finding a shortest relation for integer input is SVP on the relation lattice, so only approximations within factors like $2^{n/2}$ are known in polynomial time.
- **Precision.** With $x$ known to $D$ digits, any method can only certify relations of norm up to about $10^{D/(n-1)}$: a pigeonhole argument gives, for every $x$, an approximate relation with $\|m\|_\infty$ about $10^{D/(n-1)}$ that holds to $D$ digits, so true relations of larger norm cannot be told apart from chance.

## Reductions

- **To SVP.** The relation lattice $\Lambda(x)$ of integer input is a lattice of rank $n - 1$, and short relations are short vectors of it. The construction with $C$ above embeds approximate relations into the [approximate SVP](/approximate-svp/) problem.
- **From simultaneous approximation.** Simultaneous Diophantine approximation is solved by the same reduction on a transposed basis, and Lagarias showed that good algorithms for one give good algorithms for the other.
- **Minimal polynomials.** Factoring polynomials over $\mathbb{Q}$ with LLL finds an integer relation among powers of a $p$-adic root approximation.

## Applications

- **Experimental mathematics.** Identifying constants from numerical values: the BBP formula for $\pi$, evaluations of Euler sums and of multiple zeta values, and identities from quantum field theory found by Broadhurst.
- **Algebraic numbers.** Recognizing a numerical value as an algebraic number by its minimal polynomial; this is done by `algdep` in PARI/GP and `identify` in Maple and mpmath.
- **Polynomial factorization.** The van Hoeij method and the LLL step of the Lenstra, Lenstra and Lovász factoring algorithm solve relation problems in disguise.
- **Cryptanalysis.** Breaking knapsack cryptosystems is finding a small relation among the public weights and the target sum.

## References
