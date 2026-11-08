---
tag: 5BCEXZ
kind: concept
slug: discrepancy
name: Discrepancy
aliases:
- L2 discrepancy
- star discrepancy
- extreme discrepancy
- L2 star discrepancy
- geometric discrepancy
area: numerical/quadrature
level: advanced
summary: A measure of how uniformly a point set fills the unit cube.
prereqs: [multidimensional-integration, monte-carlo-integration]
see_also: [koksma-hlawka-inequality, quasi-monte-carlo-integration, halton-sequence, sobol-sequence, equidistribution, cubature-rule, sparse-grid-quadrature, discrepancy-method]
sources:
  - book: isbn:9780898712957
    title: Harald Niederreiter, Random Number Generation and Quasi-Monte Carlo Methods, SIAM, CBMS-NSF Regional Conference Series in Applied Mathematics 63, 1992
    locator: Chapter 2, Section 2.1 (definitions of the extreme and star discrepancy, Theorem 2.6, the exact formula in one dimension) and Chapter 3 (the discrepancy of Halton and Hammersley point sets)
  - book: isbn:9780521191593
    title: Josef Dick and Friedrich Pillichshammer, Digital Nets and Sequences, Cambridge University Press, 2010
    locator: Chapters 2 and 3 (the L2 and star discrepancy, Warnock's formula, the lower bounds of Roth and Schmidt)
  - book: "L. Kuipers and H. Niederreiter, Uniform Distribution of Sequences, Wiley, 1974"
    locator: Chapter 1, Section 1 and Chapter 2, Sections 1 and 2 (uniform distribution modulo one, the discrepancy and its relation to uniform distribution)
  - book: isbn:9783540655282
    title: Jiří Matoušek, Geometric Discrepancy, An Illustrated Guide, Springer, 1999
    locator: Chapters 1 and 2 (discrepancy for axis-parallel boxes, the van der Corput and Halton constructions, and lower bounds)
  - paper: "Tony T. Warnock, Computational investigations of low-discrepancy point sets, in S. K. Zaremba (editor), Applications of Number Theory to Numerical Analysis, Academic Press, 1972, 319-343"
    locator: the closed formula for the L2 star discrepancy
  - paper: "K. F. Roth, On irregularities of distribution, Mathematika 1 (1954) 73-79"
    locator: the lower bound on the L2 discrepancy of every N-point set
  - paper: "Michael Gnewuch, Anand Srivastav and Carola Winzen, Finding optimal volume subintervals with k points and calculating the star discrepancy are NP-hard problems, Journal of Complexity 25 (2009) 115-127"
    locator: the NP-hardness of computing the star discrepancy when the dimension is part of the input
  - paper: "Hermann Weyl, Über die Gleichverteilung von Zahlen mod. Eins, Mathematische Annalen 77 (1916) 313-352"
    locator: uniform distribution modulo one and Weyl's criterion
---

The discrepancy of a finite point set in the unit cube $[0, 1)^s$ measures how far the fraction of points in a box can be from the volume of that box. A set with small discrepancy fills the cube evenly, without clusters or gaps, at every scale and in every axis-parallel direction. The notion matters for integration because of the [Koksma-Hlawka inequality](/koksma-hlawka-inequality/): the error of the equal-weight rule $\frac1N\sum f(x_i)$ is at most the variation of $f$ times the star discrepancy of the points. That turns the search for good [quasi-Monte Carlo](/quasi-monte-carlo-integration/) rules into the search for point sets of low discrepancy, such as [Halton](/halton-sequence/) and [Sobol](/sobol-sequence/) sequences.

## In plain words

Imagine scattering a fixed number of dots in a square and asking how evenly they are spread. Pick any rectangle with one corner at the bottom left. If the dots were perfectly even, the share of dots inside would equal the share of area the rectangle covers. Discrepancy is the worst mismatch over all such rectangles. Random dots leave noticeable clumps and holes, so their mismatch is fairly large. A regular grid looks even but lines up badly with thin rectangles. Cleverly built sequences do much better than both. When an average of function values is used to estimate an integral, a smaller mismatch means a smaller possible error.

## The idea

**Notation.** As on all quadrature pages: $I(f) = \int f$, a rule $Q_N(f) = \frac1N\sum_{i=1}^N f(x_i)$ with equal weights, where $N$ counts nodes (it plays the role of $n$), and $E_N = I - Q_N$. The dimension is $s$ and $P = \{x_1, \ldots, x_N\} \subset [0, 1)^s$, repetitions allowed. For $y \in [0, 1]^s$, $[0, y) = [0, y_1)\times\cdots\times[0, y_s)$ is an *anchored box*, $A(y) = \#\{i : x_i \in [0, y)\}$, and $\operatorname{vol}(y) = y_1\cdots y_s$.

**Local discrepancy.** $\Delta_P(y) = \frac{A(y)}{N} - \operatorname{vol}(y)$. It is $E_N$ with the sign reversed for the indicator function of $[0, y)$: discrepancy is the integration error on boxes.

**The three standard measures.**

- *Star discrepancy*: $D^*_N(P) = \sup_{y \in [0, 1]^s}\lvert\Delta_P(y)\rvert$.
- *Extreme discrepancy*: $D_N(P)$, the same supremum over all boxes $[u, v)$, not only anchored ones. Every box is a signed combination of $2^s$ anchored boxes, so $D^*_N \le D_N \le 2^sD^*_N$.
- *$L_2$ star discrepancy*: $T^*_N(P) = \bigl(\int_{[0, 1]^s}\Delta_P(y)^2\,dy\bigr)^{1/2}$. Since the cube has volume 1, $T^*_N \le D^*_N$.

**Warnock's formula.** Expanding the square and integrating each term in closed form,
$$T^*_N(P)^2 = \frac{1}{3^s} - \frac{2^{1-s}}{N}\sum_{i=1}^N\prod_{k=1}^s\bigl(1 - x_{ik}^2\bigr) + \frac{1}{N^2}\sum_{i,j=1}^N\prod_{k=1}^s\bigl(1 - \max(x_{ik}, x_{jk})\bigr),$$
computable exactly in $O(sN^2)$ operations. (The middle term uses $\int_{y > x}\operatorname{vol}(y)\,dy = \prod_k\frac{1 - x_k^2}{2}$, the last $\int 1[y > x_i]\,1[y > x_j]\,dy = \prod_k(1 - \max(x_{ik}, x_{jk}))$.)

**One dimension.** With the points sorted, $x_{(1)} \le \cdots \le x_{(N)}$,
$$D^*_N = \frac{1}{2N} + \max_{1 \le i \le N}\Bigl\lvert x_{(i)} - \frac{2i - 1}{2N}\Bigr\rvert.$$
*Proof.* Between consecutive points $A$ is constant and $\Delta$ decreases with slope $-1$, so the supremum is approached at a point $x_{(i)}$, from just above (value $\frac iN - x_{(i)}$) or at it (value $x_{(i)} - \frac{i - 1}{N}$). These two numbers average to $\frac{1}{2N}$, so their maximum is $\frac{1}{2N} + \lvert x_{(i)} - \frac{2i - 1}{2N}\rvert$. $\square$ Hence $D^*_N \ge \frac{1}{2N}$, with equality only for the midpoints $\frac{2i - 1}{2N}$, the [midpoint rule](/midpoint-rule/). In $s$ dimensions the bound $D^*_N \ge \frac{1}{2N}$ still holds, by restricting to boxes $[0, y_1)\times[0, 1)^{s-1}$.

**Random points (proved).** For $x_1, \ldots, x_N$ independent and uniform on $[0, 1)^s$, $\mathbb{E}\,\Delta(y)^2 = \frac{\operatorname{vol}(y)(1 - \operatorname{vol}(y))}{N}$, and integrating over $y$,
$$\mathbb{E}\,T^*_N(P)^2 = \frac{2^{-s} - 3^{-s}}{N}.$$
So random points have $T^*_N$ of order $N^{-1/2}$, the Monte Carlo rate. Their star discrepancy is also of order $N^{-1/2}$ (cited: in one dimension $\sqrt N\,D^*_N$ tends to the Kolmogorov-Smirnov distribution).

**Low-discrepancy constructions (cited).** The van der Corput sequence has $D^*_N = O(\frac{\log N}{N})$. In $s$ dimensions, the Halton and Sobol sequences have $D^*_N = O(\frac{(\log N)^s}{N})$, and $N$-point sets such as Hammersley points and digital nets have $O(\frac{(\log N)^{s-1}}{N})$ (Niederreiter 1992, Chapters 3 and 4). Point sets and sequences with these rates are called *low-discrepancy*.

**Lower bounds (cited).** Roth (1954): every $N$-point set in $[0, 1)^s$, $s \ge 2$, has $T^*_N \ge c_s\frac{(\log N)^{(s-1)/2}}{N}$, and so the same bound for $D^*_N$. Schmidt (1972): in the plane, $D^*_N \ge c\frac{\log N}{N}$ for every $N$-point set, which the Hammersley set attains up to the constant. Whether $(\log N)^{s-1}/N$ is the right order for $D^*_N$ in $s \ge 3$ dimensions is open.

**Uniform distribution.** An infinite sequence is *uniformly distributed* in $[0, 1)^s$ if $A(y)/N \to \operatorname{vol}(y)$ for every $y$; this holds if and only if $D^*_N \to 0$ (Kuipers and Niederreiter, Chapter 2). Weyl's criterion gives the equivalent condition in terms of exponential sums.

**Computing it.** $T^*_N$ is easy by Warnock's formula. $D^*_N$ is attained in the limit at a box whose corner coordinates are point coordinates or $1$, which gives an exact $O(N^{s+1})$ brute-force method; for $s$ part of the input, computing $D^*_N$ is NP-hard (Gnewuch, Srivastav and Winzen 2009), and in practice it is computed only for small $s$ and $N$.

**Floating point.** In Warnock's formula the three terms are of size $3^{-s}$, while their sum $T^{*2}_N$ is about $N^{-2}$ for a good set: at $N = 2048$ in two dimensions the terms are $0.111$, $0.222$ and $0.111$, and the result is $3.8 \times 10^{-7}$. The relative error is about $u$ times their ratio, here near $10^{-10}$, and it grows like $N^2$. Use compensated summation (`math.fsum`), or rational arithmetic for rational points, for large $N$.

## Examples

**Van der Corput in base 2** (in rational arithmetic, starting from $x_0 = 0$): $0, \frac12, \frac14, \frac34, \frac18, \ldots$. For $N = 2^k$ the points are $\{0, \frac1N, \ldots, \frac{N - 1}{N}\}$, and the formula gives $D^*_N = \frac1N$; between powers of two it is larger: $N\,D^*_N = 1.75, 1.875, 2.31, 2.45$ at $N = 7, 15, 100, 1000$, growing like $\log N$. The midpoints $\frac{2i - 1}{2N}$ attain the optimum $\frac{1}{2N}$, and their $T^{*2}_N = \frac{1}{12N^2}$ (checked exactly for $N = 4$ and $10$).

**The unit square, measured** ($D^*_N$ by the exact brute force, $T^*_N$ by Warnock's formula; random points with seed 1, the centered $k \times k$ grid, Halton in bases 2 and 3 from index 1, and Hammersley points $(\frac iN, \phi_2(i))$):

| $N$ | random | grid | Halton | Hammersley |
|---|---|---|---|---|
| 16 | $0.242$ / $0.070$ | $0.234$ / $0.060$ | $0.174$ / $0.046$ | $0.172$ / $0.069$ |
| 64 | $0.117$ / $0.035$ | $0.121$ / $0.030$ | $0.052$ / $0.014$ | $0.054$ / $0.021$ |
| 256 | $0.070$ / $0.021$ | $0.062$ / $0.015$ | $0.019$ / $0.0043$ | $0.016$ / $0.0063$ |

(each entry $D^*_N$ / $T^*_N$). Random points and the grid both lose about a factor 2 per factor 4 in $N$, the rate $N^{-1/2}$: a grid is even but a thin box between two rows of points sees an error of about $\frac1k = N^{-1/2}$. Halton and Hammersley lose about a factor 3 per factor 4 in $N$ at these sizes, on the way to $N^{-1}$ up to logarithms. Over 20 random sets, the mean of $T^{*2}_N$ was $2.7 \times 10^{-3}$ at $N = 64$ and $5.1 \times 10^{-4}$ at $N = 256$, against the exact expectations $2.2 \times 10^{-3}$ and $5.4 \times 10^{-4}$.

**A non-example: low discrepancy is not low degree.** The Hammersley set integrates constants exactly and nothing else in particular: as a [cubature rule](/cubature-rule/) it has degree 0. Conversely, a rule of high degree can have large discrepancy, because its weights are unequal and its nodes cluster near the boundary. Discrepancy and degree measure different things and suit different classes of integrands.

## Where it is used

- **Error bounds for quasi-Monte Carlo.** The Koksma-Hlawka inequality $\lvert E_N(f)\rvert \le V_{HK}(f)\,D^*_N(P)$ bounds the error of an equal-weight rule by the Hardy-Krause variation of $f$ times the star discrepancy, and the Hlawka-Zaremba identity gives the analogous bound with $T^*_N$ and an $L_2$ variation. These are the reason low-discrepancy points give errors near $N^{-1}$ instead of $N^{-1/2}$ for smooth integrands in moderate dimension; see [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/).
- **Design and testing of point sets.** $T^*_N$ and its weighted or centered variants are used to compare and optimize Sobol direction numbers, lattice rules and scrambled nets. In design of experiments, low-discrepancy designs are called space-filling designs.
- **Sampling in computer graphics.** Supersampling patterns for anti-aliasing and Monte Carlo rendering are judged by discrepancy; Dobkin, Eppstein and Mitchell gave algorithms for computing it in the plane for this purpose.
- **Pseudorandom numbers.** [Equidistribution](/equidistribution/) of generator outputs in several dimensions is a discrepancy-type property, tested by the spectral test and by statistical tests.
- **Uniform distribution theory.** In number theory the discrepancy of sequences such as $\{n\alpha\}$ quantifies how fast they become uniformly distributed, with bounds from continued fractions and exponential sums.
- **Combinatorial discrepancy** is a related but different notion: coloring the elements of a set system so that every set is nearly balanced. It appears in complexity theory as the [discrepancy method](/discrepancy-method/) and shares tools, such as Roth's orthogonal function method, with geometric discrepancy.

## References
