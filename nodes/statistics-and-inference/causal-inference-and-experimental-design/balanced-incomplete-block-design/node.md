---
tag: JG5X5V
kind: definition
slug: balanced-incomplete-block-design
name: Balanced incomplete block design
aliases:
- BIBD
- 2-design
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: Puts v treatments into b blocks of size k < v so that each pair of treatments shares exactly lambda blocks. Then bk = vr, lambda(v-1) = r(k-1), and b >= v (Fisher).
prereqs: [randomized-block-design]
see_also: [latin-square-design, orthogonal-array, hamming-code, golay-code, quadratic-residue, determinant, linear-mixed-model, exact-cover]
sources:
  - paper: doi:10.1111/j.1469-1809.1936.tb02134.x
    title: "Frank Yates, Incomplete randomized blocks, Annals of Eugenics 7(2), 1936"
    locator: pp. 121 to 140 (balanced incomplete blocks and their intrablock analysis)
  - paper: doi:10.1111/j.1469-1809.1940.tb02237.x
    title: "Ronald A. Fisher, An examination of the different possible solutions of a problem in incomplete blocks, Annals of Eugenics 10(1), 1940"
    locator: pp. 52 to 75 (the inequality b >= v and the enumeration of designs)
  - book: isbn:9780471718130
    title: George E. P. Box, J. Stuart Hunter and William G. Hunter, Statistics for Experimenters, second edition, Wiley, 2005
    locator: Section 4.5 (balanced incomplete block designs), starting on p. 162
  - book: isbn:9781119492443
    title: Douglas C. Montgomery, Design and Analysis of Experiments, tenth edition, Wiley, 2019
    locator: Chapter 4 (the balanced incomplete block design and its intrablock analysis; chapter-level locator)
  - book: isbn:9780521006019
    title: J. H. van Lint and R. M. Wilson, A Course in Combinatorics, second edition, Cambridge University Press, 2001
    locator: the chapter on block designs (Fisher's inequality, symmetric designs, the Bruck-Ryser-Chowla theorem; general locator, chapter number not confirmed)
---

A balanced incomplete block design (BIBD) is used when a block cannot hold every treatment: a day allows three runs but there are seven catalysts, a judge can taste four wines out of thirteen. It places $v$ treatments in $b$ blocks of $k < v$ units so that every treatment appears in the same number $r$ of blocks and every pair of treatments appears together in the same number $\lambda$ of blocks. Because all pairs are treated alike, all treatment differences are estimated with the same precision after the block effects are removed. In combinatorics the same object is a 2-$(v, k, \lambda)$ design; with $\lambda = 1$ it is a Steiner system $S(2, k, v)$. Its parameters must satisfy two counting identities and Fisher's inequality $b \ge v$.

## Definition

Let $X$ be a set of $v$ treatments. A **balanced incomplete block design** with parameters $(v, b, r, k, \lambda)$ is a list of $b$ subsets of $X$, the blocks, such that

1. every block has $k$ elements, $2 \le k < v$;
2. every treatment lies in exactly $r$ blocks;
3. every pair of distinct treatments lies together in exactly $\lambda \ge 1$ blocks.

The **incidence matrix** $N$ is the $v \times b$ 0/1 matrix with $N_{ij} = 1$ when treatment $i$ is in block $j$. In an experiment, the blocks are assigned to the actual blocks at random and the treatments to the units of each block at random.

**Theorem 1 (the counting identities).** $bk = vr$ and $\lambda(v - 1) = r(k - 1)$.

*Proof.* Count the pairs (treatment, block containing it). By blocks there are $bk$; by treatments there are $vr$. For the second identity, fix a treatment $x$ and count the pairs $(y, B)$ with $y \ne x$ and $x, y \in B$. Each of the $r$ blocks that contain $x$ gives $k - 1$ choices of $y$; each of the $v - 1$ treatments $y$ gives $\lambda$ blocks. $\square$

So $r$ and $b$ follow from $(v, k, \lambda)$: $r = \lambda(v - 1)/(k - 1)$ and $b = vr/k$, and both must be integers.

**Theorem 2 (Fisher's inequality).** $b \ge v$.

*Proof.* The entry $(i, l)$ of $NN^\top$ counts the blocks that contain both $i$ and $l$, so $NN^\top = (r - \lambda)I + \lambda J$, where $J$ is the all-ones matrix. $J$ has the eigenvalue $v$ on the all-ones vector and 0 on its orthogonal complement, so $NN^\top$ has the [eigenvalues](/eigenvalue/) $r + (v - 1)\lambda$ once and $r - \lambda$ with multiplicity $v - 1$, and

$$\det(NN^\top) = (r - \lambda)^{v-1}\big(r + (v - 1)\lambda\big).$$

Since $k < v$, Theorem 1 gives $r = \lambda(v-1)/(k-1) > \lambda$, so the [determinant](/determinant/) is positive. Then $v = \operatorname{rank}(NN^\top) \le \operatorname{rank}N \le b$. $\square$

A design with $b = v$ (so $r = k$) is **symmetric**; in a symmetric design any two blocks meet in exactly $\lambda$ treatments. The test file checks the two identities and the determinant formula in exact arithmetic for every design on this page.

**The intrablock analysis.** The model is $y = \mu + \tau_{\text{treatment}} + \beta_{\text{block}} + e$ with iid $N(0, \sigma^2)$ errors and $\sum\tau_i = 0$. Let $T_i$ be the total of treatment $i$, $B_j$ the total of block $j$, and

$$Q_i = T_i - \frac1k\sum_{j \ni i}B_j,$$

the treatment total adjusted for the blocks it is in.

**Theorem 3 (the estimates).** The least squares estimates are $\hat\tau_i = kQ_i/(\lambda v)$, and $\operatorname{Var}(\hat\tau_i - \hat\tau_l) = 2k\sigma^2/(\lambda v)$ for every pair $i \ne l$.

*Proof.* The normal equation of block $j$ is $k(\mu + \beta_j) + \sum_{l \in j}\tau_l = B_j$. Solve it for $\mu + \beta_j$ and put that into the normal equation of treatment $i$, $r(\mu + \tau_i) + \sum_{j \ni i}\beta_j = T_i$. This gives $C\tau = Q$ with

$$C = rI - \frac1kNN^\top = \frac{r(k - 1) + \lambda}{k}I - \frac\lambda kJ = \frac{\lambda v}{k}\Big(I - \frac1vJ\Big),$$

using $NN^\top = (r - \lambda)I + \lambda J$ and $r(k - 1) = \lambda(v - 1)$. For $\sum\tau_i = 0$, $(I - J/v)\tau = \tau$, so $\tau = kQ/(\lambda v)$. $Q$ is $X_T^\top(I - P_B)y$, where $X_T$ and $X_B$ are the treatment and block indicator matrices and $P_B = X_BX_B^\top/k$ is the projection onto the block indicators, so its covariance is $\sigma^2X_T^\top(I - P_B)X_T = \sigma^2C$. Then $\operatorname{Var}(\hat\tau_i - \hat\tau_l) = (k/(\lambda v))^2\sigma^2(e_i - e_l)^\top C(e_i - e_l) = (k/(\lambda v))^2\sigma^2 \cdot 2\lambda v/k = 2k\sigma^2/(\lambda v)$. $\square$

The adjusted treatment sum of squares is $k\sum_iQ_i^2/(\lambda v)$ on $v - 1$ degrees of freedom, the error sum of squares is what remains after the blocks (unadjusted) and the adjusted treatments, on $bk - v - b + 1$ degrees of freedom, and their ratio of mean squares has the exact F law under $\tau = 0$ by the same projection argument as in the [randomized block design](/randomized-block-design/). A complete block design with the same $r$ would give $\operatorname{Var} = 2\sigma^2/r$, so the **efficiency factor** is $E = \lambda v/(rk) < 1$, the price of incomplete blocks when $\sigma^2$ is the same. With random block effects, a [linear mixed model](/linear-mixed-model/) recovers extra information from the block totals (Yates, 1940).

**What is cited, not proved.** The Bruck-Ryser-Chowla theorem gives further conditions for symmetric designs; for example, it rules out the projective plane of order 6, a symmetric $(43, 43, 7, 7, 1)$ design, although those parameters pass Theorems 1 and 2.

## Examples and non-examples

**Example: four treatments in blocks of three.** All four 3-subsets of $\{1, 2, 3, 4\}$ form a $(4, 4, 3, 3, 2)$ design, with $E = 8/9$. The responses:

| block | treatments | responses |
|---|---|---|
| 1 | 1, 2, 3 | 71, 76, 70 |
| 2 | 1, 2, 4 | 70, 77, 72 |
| 3 | 1, 3, 4 | 75, 73, 70 |
| 4 | 2, 3, 4 | 80, 77, 73 |

The treatment totals are $T = (216, 233, 220, 215)$, and the adjusted totals are $Q = (-2, 11, -\frac53, -\frac{22}3)$, so $\hat\tau = kQ/(\lambda v) = (-\frac34, \frac{33}8, -\frac58, -\frac{11}4)$; the test file checks that these equal exact least squares.

| source | sum of squares | df | mean square | F | p |
|---|---|---|---|---|---|
| blocks (unadjusted) | $110/3$ | 3 | | | |
| treatments (adjusted) | $817/12 = 68.08$ | 3 | 22.69 | $4085/573 = 7.129$ | 0.0296 |
| error | $191/12 = 15.92$ | 5 | 3.183 | | |
| total | $362/3$ | 11 | | | |

The treatments differ at the 5% level. Ignoring the blocks, the one-way F on the raw treatment means 72, 77.67, 73.33 and 71.67 is $3.521$ on $(3, 8)$, $p = 0.0686$.

**Example: the Fano plane.** Developing the base block $\{0, 1, 3\}$ modulo 7 gives the seven blocks $\{0,1,3\}, \{1,2,4\}, \{2,3,5\}, \{3,4,6\}, \{0,4,5\}, \{1,5,6\}, \{0,2,6\}$, a symmetric $(7, 7, 3, 3, 1)$ design: the projective plane of order 2. It works because the differences of $\{0, 1, 3\}$, namely $\pm1, \pm2, \pm3$, cover every nonzero residue modulo 7 once. Any two blocks meet in exactly one treatment, and $E = 7/9$.

**Example: Kirkman's schoolgirls.** Fifteen girls walk in five rows of three on seven days, and no two girls walk in the same row twice. The 35 rows form a $(15, 35, 7, 3, 1)$ design whose blocks split into 7 parallel classes, one per day: a resolvable design, a Kirkman triple system. The code takes the 35 lines of the projective space $PG(3, 2)$ and finds the days by backtracking:

| day | rows |
|---|---|
| 1 | 1 2 3, 4 8 12, 5 10 15, 6 11 13, 7 9 14 |
| 2 | 1 4 5, 2 8 10, 3 13 14, 6 9 15, 7 11 12 |
| 3 | 1 6 7, 2 9 11, 3 12 15, 4 10 14, 5 8 13 |
| 4 | 1 8 9, 2 12 14, 3 5 6, 4 11 15, 7 10 13 |
| 5 | 1 10 11, 2 13 15, 3 4 7, 5 9 12, 6 8 14 |
| 6 | 1 12 13, 2 4 6, 3 9 10, 5 11 14, 7 8 15 |
| 7 | 1 14 15, 2 5 7, 3 8 11, 4 9 13, 6 10 12 |

**Example: designs from algebra.** The quadratic residues $\{1, 3, 4, 5, 9\}$ modulo 11, developed cyclically, give a symmetric $(11, 11, 5, 5, 2)$ design (see [quadratic residue](/quadratic-residue/)); $\{0, 1, 3, 9\}$ modulo 13 gives the projective plane of order 3, $(13, 13, 4, 4, 1)$; and the 12 lines of the affine plane over $\mathbb F_3$ give $(9, 12, 4, 3, 1)$, a resolvable design whose four parallel classes come from the rows, the columns and the two [Latin squares](/latin-square-design/) of order 3.

**Non-example: a cyclic block that is not a difference set.** Developing $\{0, 1, 2\}$ modulo 7 gives seven blocks of size 3 with $r = 3$, but its differences are $\pm1, \pm1, \pm2$: pairs at distance 1 meet twice, pairs at distance 3 never. It is not balanced.

**Non-example: parameters that pass the identities.** $(v, k, \lambda) = (21, 6, 1)$ gives the integers $r = 20/5 = 4$ and $b = 21 \cdot 4/6 = 14$, so Theorem 1 holds, but $b = 14 < 21 = v$ violates Fisher's inequality. No such design exists.

## Related definitions

- [Randomized block design](/randomized-block-design/): the complete case $k = v$, where the treatment means need no adjustment.
- [Latin square design](/latin-square-design/): complete blocks in two directions; affine planes and finite fields give both Latin squares and BIBDs.
- [Orthogonal array](/orthogonal-array/): strength-2 arrays balance pairs of levels, as BIBDs balance pairs of treatments.
- [Hamming code](/hamming-code/): the seven codewords of weight 3 of the [7, 4] Hamming code are the lines of the Fano plane.
- [Golay code](/golay-code/): its codewords of weight 8 form the Steiner system $S(5, 8, 24)$, a 5-design.
- [Exact cover](/exact-cover/): finding a design or a resolution, such as Kirkman's seven days, is an exact cover search.

## References
