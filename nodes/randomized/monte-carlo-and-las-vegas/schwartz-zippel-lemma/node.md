---
tag: B38MAX
kind: theorem
slug: schwartz-zippel-lemma
name: Schwartz-Zippel lemma
aliases:
- DeMillo-Lipton-Schwartz-Zippel lemma
- Schwartz-Zippel-DeMillo-Lipton lemma
area: randomized/monte-carlo-and-las-vegas
level: core
summary: A nonzero polynomial of total degree d over a field is zero on at most a d/|S| fraction of the points of S^m, so evaluation at a random point detects it.
prereqs: [polynomial-ring, factor-theorem, conditional-probability]
see_also: [polynomial-identity-testing, freivalds-algorithm, matrix-product-verification, fingerprinting, tutte-matrix, reed-solomon-code, one-sided-error, hitting-set-generator]
sources:
  - paper: doi:10.1145/322217.322225
    title: Jacob T. Schwartz, Fast probabilistic algorithms for verification of polynomial identities, Journal of the ACM 27(4), 1980
    locator: pages 701 to 717, Lemma 1 (the bound d/|S| for a nonzero polynomial of total degree d)
  - paper: "Richard Zippel, Probabilistic algorithms for sparse polynomials, Proceedings of EUROSAM 1979, Lecture Notes in Computer Science 72, Springer, 1979"
    title: Richard Zippel, Probabilistic algorithms for sparse polynomials
    locator: pages 216 to 226 (a bound on the probability that a random point is a zero, with the degrees in each variable)
  - paper: "Richard A. DeMillo and Richard J. Lipton, A probabilistic remark on algebraic program testing, Information Processing Letters 7(4), 1978"
    title: Richard A. DeMillo and Richard J. Lipton, A probabilistic remark on algebraic program testing
    locator: pages 193 to 195 (the same kind of bound for testing algebraic programs at random points)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 7, Algebraic techniques (verifying polynomial identities, the Schwartz-Zippel theorem, and perfect matchings in graphs)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 1 (the univariate case for verifying polynomial identities) and the Schwartz-Zippel theorem with its proof by induction
---

The Schwartz-Zippel lemma bounds the number of zeros of a multivariate polynomial on a grid. If $P$ is a nonzero polynomial in $m$ variables of total degree $d$ over a field, and $S$ is a finite set of field elements, then a point drawn uniformly from $S^m$ is a zero of $P$ with probability at most $d/|S|$. It is the reason that [polynomial identity testing](/polynomial-identity-testing/) has a fast randomized algorithm with [one-sided error](/one-sided-error/): evaluate at one random point, and say "zero" only if the value is zero. The bound does not depend on the number of variables or on the number of terms, which can be exponential.

## Statement

Notation on this page: $F$ is a field (an integral domain is enough), $m$ is the number of variables, $d$ is the total degree, $S \subseteq F$ is a finite nonempty set, and $r = (r_1, \dots, r_m)$ has independent coordinates, each uniform on $S$. $\Pr$ is over the choice of $r$ only.

**Theorem (Schwartz 1980, Zippel 1979, DeMillo and Lipton 1978).** Let $P \in F[x_1, \dots, x_m]$ be a nonzero polynomial of total degree $d \ge 0$. Then

$$\Pr_{r \in S^m}[P(r) = 0] \le \frac{d}{|S|}, \qquad \text{equivalently} \qquad \#\{r \in S^m : P(r) = 0\} \le d\,|S|^{m-1}.$$

**Individual-degree form.** If $P$ has degree $d_i$ in $x_i$ and $d_i \le |S|$ for each $i$, then $P$ is nonzero on at least $\prod_{i=1}^{m} (|S| - d_i)$ points of $S^m$.

## In plain words

A polynomial that is not the zero polynomial cannot be zero almost everywhere. A nonzero polynomial in one variable of degree $d$ has at most $d$ roots. The lemma says the same holds for many variables in a sense of proportion: among all the points of a grid with side $|S|$, at most a $d/|S|$ part can be roots.

So to check whether two formulas give the same polynomial, pick a random point from a large grid and compare the two values. If the formulas differ, their difference is a nonzero polynomial, and a random point hits a root of it only rarely. If they are equal, every point agrees. The size of the grid controls the error, and nothing else does.

## Proof

**Induction on $m$**, the number of variables.

*Base case, $m = 1$.* A nonzero polynomial of degree $d$ in one variable over an integral domain has at most $d$ roots. (By the [factor theorem](/factor-theorem/), each root $a$ gives a factor $x - a$, and in an integral domain the degree of a product is the sum of the degrees.) So at most $d$ of the $|S|$ values of $r_1$ are roots, and $\Pr[P(r_1) = 0] \le d/|S|$.

*Inductive step, $m \ge 2$.* Assume the theorem for $m - 1$ variables. Write $P$ as a polynomial in $x_1$ with coefficients in the other variables:

$$P(x_1, \dots, x_m) = \sum_{i=0}^{k} x_1^{i}\, Q_i(x_2, \dots, x_m),$$

where $k$ is the largest index with $Q_k \ne 0$. Such a $k$ exists because $P \ne 0$. Each monomial of $x_1^k Q_k$ has total degree at most $d$, so $Q_k$ has total degree at most $d - k$.

Draw $r' = (r_2, \dots, r_m)$ first, then $r_1$; the two are independent. Let $E$ be the event $Q_k(r') = 0$.

- By the inductive hypothesis applied to $Q_k$, a nonzero polynomial in $m - 1$ variables of total degree at most $d - k$: $\Pr[E] \le (d - k)/|S|$.
- Fix any $r'$ outside $E$. Then $g(x_1) = P(x_1, r')$ is a polynomial in $x_1$ alone with leading coefficient $Q_k(r') \ne 0$, so it is nonzero of degree exactly $k$. By the base case, $\Pr_{r_1}[g(r_1) = 0] \le k/|S|$. As this holds for every such $r'$, $\Pr[P(r) = 0 \text{ and not } E] \le k/|S|$.

Together,

$$\Pr[P(r) = 0] \le \Pr[E] + \Pr[P(r) = 0 \text{ and not } E] \le \frac{d - k}{|S|} + \frac{k}{|S|} = \frac{d}{|S|}.$$

When $k = 0$, $Q_0 = P$ does not depend on $x_1$, and the first term alone gives the bound. $\square$

**Proof of the individual-degree form.** The same induction, with counts instead of probabilities. For $m = 1$, at most $d_1$ of the $|S|$ values are roots, so at least $|S| - d_1$ are not. For $m \ge 2$, let $k = d_1$ be the degree in $x_1$, so that $Q_k$ has degree at most $d_i$ in each $x_i$ for $i \ge 2$. By induction, $Q_k$ is nonzero on at least $\prod_{i \ge 2}(|S| - d_i)$ points $r'$. For each of them, $P(x_1, r')$ is nonzero of degree $d_1$ and so nonzero for at least $|S| - d_1$ values of $r_1$. Multiply. $\blacksquare$

**Where the field is used.** Only in the base case: a nonzero univariate polynomial of degree $d$ has at most $d$ roots. Over a ring with zero divisors this fails. Over $\mathbb{Z}/4\mathbb{Z}$ the degree-1 polynomial $2x$ is zero at $x = 0$ and at $x = 2$, so half of the points are roots, not at most a quarter. The tests check this example.

## Consequences

- **[Polynomial identity testing](/polynomial-identity-testing/).** To test whether an arithmetic circuit of degree $d$ computes the zero polynomial, evaluate it at one point of $S^m$ with $|S| \ge 2d$. A nonzero circuit gives a nonzero value with probability at least $1/2$, and the zero circuit never does. So PIT is in [co-RP](/co-rp/) when the values can be computed in polynomial time.
- **[Matrix product verification](/matrix-product-verification/).** If $D = AB - C$ is nonzero, some row $i$ of $D$ is nonzero, and $\sum_j D_{ij} x_j$ is a nonzero polynomial of degree 1 in the vector $x$. So a vector $r$ uniform on $S^n$ has $Dr = 0$ with probability at most $1/|S|$. This is the analysis of [Freivalds' algorithm](/freivalds-algorithm/) with a large $S$.
- **Perfect matchings.** A graph has a [perfect matching](/perfect-matching/) if and only if the determinant of its [Tutte matrix](/tutte-matrix/) is a nonzero polynomial, of degree $n$ (Lovász 1979). Substituting random values from $S$ with $|S| \ge 2n$ and computing one numerical [determinant](/determinant/) decides this with one-sided error at most $1/2$. This gives the parallel algorithms of [RNC perfect matching](/rnc-perfect-matching/).
- **Fingerprints for strings and multisets.** Two strings $a, b$ of length $n$ over $\mathbb{F}_p$ are equal if and only if $\sum_i (a_i - b_i) x^i$ is zero. One random $x$ detects a difference with probability at least $1 - n/p$. See [fingerprinting](/fingerprinting/).
- **Codes.** For $d < |F|$, two different polynomials of degree at most $d$ in $m$ variables over a finite field $F$ agree on at most a $d/|F|$ part of $F^m$. This is the distance bound of [Reed-Solomon codes](/reed-solomon-code/) ($m = 1$) and of [Reed-Muller codes](/reed-muller-code/).
- **Hitting sets.** A set of points on which every nonzero polynomial of a class is nonzero somewhere is a *hitting set*. The lemma with a union bound shows that a small random set is a hitting set for circuits of size $s$ and degree $d$ with high probability. Finding such a set deterministically is the open problem of derandomizing PIT, see [hitting set generator](/hitting-set-generator/).

## Tightness

The bound is exact for some polynomials. Let $s_1, \dots, s_d$ be distinct elements of $S$, with $d \le |S|$, and let

$$P(x_1, \dots, x_m) = (x_1 - s_1)(x_1 - s_2) \cdots (x_1 - s_d).$$

$P$ has total degree $d$ and is zero exactly when $r_1 \in \{s_1, \dots, s_d\}$. That is $d\,|S|^{m-1}$ points, and the probability is exactly $d/|S|$. The tests check this over $\mathbb{F}_7$ with $m = 3$ and every $d$ from 1 to 7.

Other polynomials are far from the bound. Over $\mathbb{F}_{101}$ with $S = \mathbb{F}_{101}$, the polynomial $2xy$ has total degree 2 and is zero when $x = 0$ or $y = 0$, which is $101 + 101 - 1 = 201$ of the $10201$ points. The ratio $0.01970$ is just below the bound $2/101 \approx 0.01980$. Over $\mathbb{F}_2$ the same polynomial is the zero polynomial, because $2 = 0$; so $(x + y)^2 = x^2 + y^2$ is a true identity there.

**The bound is useless when $d \ge |S|$.** Over $\mathbb{F}_p$, the polynomial $x^p - x$ is nonzero of degree $p$ and is zero at every point of $\mathbb{F}_p$. The lemma allows this, because $d/|S| = 1$. When the field is small, take $S$ in an extension field.

**The individual-degree form can be stronger.** For $P = x_1 x_2 \cdots x_m$ with $S = \{0, 1\}$, the total degree is $m$ and the bound $m/2$ says nothing for $m \ge 2$. The individual degrees are all 1, so at least $\prod (2 - 1) = 1$ point is a nonzero, which is exact: only $(1, \dots, 1)$.

## History

DeMillo and Lipton (1978) gave a bound of this kind in a note on testing algebraic programs at random inputs. Zippel (1979) used a bound in terms of the degree in each variable in his probabilistic algorithms for sparse polynomial interpolation. Schwartz (1980) proved the clean form $d/|S|$ with the total degree and used it to verify polynomial identities, including identities of determinants and of geometry theorems. The three papers were independent, which is why the lemma carries several names. Lipton has pointed out that the finite field case was proved much earlier by Ore (1922). The lemma became the basic tool of algebraic randomized algorithms: Lovász (1979) used it for perfect matchings, and later work used it for interactive proofs and probabilistically checkable proofs through low-degree tests.

## References
