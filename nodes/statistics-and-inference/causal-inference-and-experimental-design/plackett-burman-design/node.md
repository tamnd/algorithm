---
tag: 9V49FC
kind: definition
slug: plackett-burman-design
name: Plackett-Burman design
aliases:
- Plackett-Burman screening design
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: Two-level screening designs for N - 1 factors in N runs, N a multiple of 4, built from Hadamard matrices. Main effects are estimated independently of each other.
prereqs: [fractional-factorial-design]
see_also: [orthogonal-array, hadamard-code, quadratic-residue, factorial-design, walsh-hadamard-transform, kronecker-product, determinant, optimal-experimental-design]
sources:
  - paper: doi:10.1093/biomet/33.4.305
    title: "R. L. Plackett and J. P. Burman, The design of optimum multifactorial experiments, Biometrika 33(4), 1946"
    locator: the article starting on p. 305 (the cyclic generators of the two-level designs for N = 12, 20, 24, ... and the table of designs up to N = 100; page range not confirmed)
  - book: isbn:9780471718130
    title: George E. P. Box, J. Stuart Hunter and William G. Hunter, Statistics for Experimenters, second edition, Wiley, 2005
    locator: Section 7.1 (Plackett and Burman designs), starting on p. 281
  - paper: "R. E. A. C. Paley, On orthogonal matrices, Journal of Mathematics and Physics 12, 1933"
    locator: the construction of Hadamard matrices of order q + 1 from the quadratic residues of a prime power q = 3 (mod 4) (general locator)
  - book: isbn:9781119492443
    title: Douglas C. Montgomery, Design and Analysis of Experiments, tenth edition, Wiley, 2019
    locator: the chapter on two-level fractional factorial designs, where Plackett-Burman designs appear as non-regular screening designs (chapter-level locator)
---

A Plackett-Burman design studies up to $N - 1$ two-level factors in $N$ runs, where $N$ is a multiple of 4. Regular [fractional factorial designs](/fractional-factorial-design/) need $N$ to be a power of two, so they jump from 8 to 16 to 32 runs. Plackett and Burman (1946) filled the gaps with designs of 12, 20, 24, 28, ... runs. Each design is a Hadamard matrix with its first column removed, so its columns are orthogonal and the main effects are estimated independently, each with the precision of a full factorial of the same size. The price is partial aliasing: when $N$ is not a power of two, a two-factor interaction does not fall on one column but spreads over many columns with small weights, such as $\pm 1/3$ for $N = 12$.

## Definition

A **Hadamard matrix** of order $N$ is an $N \times N$ matrix $H$ with entries $\pm 1$ and $HH^\top = NI$. Changing the sign of a row or of a column keeps this property, so $H$ can be **normalized** to have a first column of $+1$ entries.

A **Plackett-Burman design** with $N$ runs is the $N \times (N - 1)$ matrix $D$ that is left when the first column of a normalized Hadamard matrix is removed. Row $u$ is a run and column $j$ is a factor; the entry is the level, $-1$ or $+1$, of factor $j$ in run $u$. With $k < N - 1$ factors, use $k$ of the columns; the unused "dummy" columns estimate noise when the active effects are few. The runs are done in random order, as in any [randomized experiment](/randomized-experiment/). The main effect of factor $j$ is estimated as in a [factorial design](/factorial-design/): $\hat E_j = 2 x_j^\top y/N$, the mean response at $+1$ minus the mean response at $-1$.

**Theorem 1 (the possible orders).** If a Hadamard matrix of order $N$ exists, then $N = 1$, $N = 2$ or $N$ is a multiple of 4.

*Proof.* Let $N \ge 3$. Normalize the first row to all $+1$ by changing the signs of columns. Take rows 2 and 3 and let $a, b, c, d$ count the columns where they are $(+, +)$, $(+, -)$, $(-, +)$ and $(-, -)$. Then $a + b + c + d = N$; orthogonality to row 1 gives $a + b - c - d = 0$ and $a - b + c - d = 0$; and orthogonality of rows 2 and 3 gives $a - b - c + d = 0$. The only solution is $a = b = c = d = N/4$, so $4$ divides $N$. $\square$

The Hadamard conjecture says that a Hadamard matrix exists for every multiple of 4. It is open; see the [Hadamard code](/hadamard-code/) page for its status.

**Theorem 2 (orthogonality).** Let $X = [\mathbf 1 \mid D] = H$ be the model matrix of the main-effect model $y = Xb + e$. Then $X^\top X = NI$. So every column of $D$ has $N/2$ entries of each sign, the columns are pairwise orthogonal, the estimates $\hat E_j$ are uncorrelated with $\operatorname{Var}(\hat E_j) = 4\sigma^2/N$ under independent errors of variance $\sigma^2$, and any two columns show each of the four level pairs exactly $N/4$ times. In other words, $D$ is an [orthogonal array](/orthogonal-array/) of strength 2.

*Proof.* $HH^\top = NI$ means $H^{-1} = H^\top/N$, so also $H^\top H = NI$: the columns of $H$ are orthogonal with squared length $N$. A column of $D$ is orthogonal to the column of ones, so it sums to zero and has $N/2$ entries of each sign. Least squares gives $\hat b = X^\top y/N$ with covariance $\sigma^2 I/N$, and $\hat E_j = 2\hat b_j$. For the pair counts, apply the argument of Theorem 1 to the column of ones and two columns of $D$. $\square$

**Theorem 3 (the cyclic construction of Paley).** Let $q$ be a prime with $q \equiv 3 \pmod 4$, let $\chi$ be the Legendre symbol modulo $q$ (the [quadratic residue](/quadratic-residue/) character, with $\chi(0) = 0$), and let $\chi'(u) = \chi(u)$ for $u \ne 0$ and $\chi'(0) = +1$. Rows $i = 0, \dots, q - 1$ of $D$ have the entry $\chi'(i + j)$ in column $j = 0, \dots, q - 1$, and the last row is all $-1$. Then $[\mathbf 1 \mid D]$ is a Hadamard matrix of order $N = q + 1$. So the first row has $+$ at $0$ and at the residues, and each next row is the previous one moved one place to the left.

*Proof.* Every row has squared length $q + 1$. First, for $d \ne 0$, $\sum_u \chi(u)\chi(u + d) = -1$: the term $u = 0$ is zero, and for $u \ne 0$, $\chi(u)\chi(u + d) = \chi(u^2)\chi(1 + d u^{-1}) = \chi(1 + du^{-1})$; as $u$ runs over the nonzero elements modulo $q$, $1 + du^{-1}$ takes every value except 1, and $\sum_z \chi(z) = 0$, so the sum is $-\chi(1) = -1$. Now take rows $i \ne l$ and $d = l - i$. With $\chi' = \chi + \delta_0$,

$$1 + \sum_u \chi'(u)\chi'(u + d) = 1 + \sum_u \chi(u)\chi(u + d) + \chi(d) + \chi(-d) = 1 - 1 + 0 = 0,$$

because $q \equiv 3 \pmod 4$ makes $-1$ a non-residue, so $\chi(-d) = -\chi(d)$. A row $i < q$ against the last row gives $1 - \sum_u \chi'(u) = 1 - (0 + 1) = 0$. $\square$

For $q = 11$ the first row is `++-+++---+-`, exactly the generator that Plackett and Burman printed for $N = 12$. For $q = 19$ it is `++--++++-+-+----++-`, their generator for $N = 20$. The construction also works for prime powers $q$ with the quadratic character of the field with $q$ elements, which gives $N = 28$ from $q = 27$. The test file checks Theorem 3 for $q = 3, 7, 11, 19, 23, 31, 43$.

**Theorem 4 (partial aliasing).** Suppose the true model also has two-factor interactions, $\mathbb E[y] = b_0 + \sum_j b_j x_j + \sum_{a < b} b_{ab}\, x_a \circ x_b$, with effects $E_j = 2b_j$ and $E_{ab} = 2b_{ab}$. Then

$$\mathbb E[\hat E_i] = E_i + \sum_{a < b,\ a, b \ne i} \rho_{i, ab}\, E_{ab}, \qquad \rho_{i, ab} = \frac{x_i^\top (x_a \circ x_b)}{N}.$$

*Proof.* $\hat E_i = 2x_i^\top y/N$ is linear in $y$. Orthogonality (Theorem 2) removes $b_0$ and every $b_j$ with $j \ne i$, and leaves $2b_i$. An interaction that contains $i$ has $x_i^\top (x_i \circ x_b) = \sum_u x_b(u) = 0$. The other interactions contribute $2 b_{ab}\rho_{i, ab}$. $\square$

For the Sylvester designs with $N = 2^m$, the product of two columns is another column, so every $\rho$ is $0$ or $\pm 1$: complete aliasing, as in a regular fraction. For $N = 12$ the test file computes all $11 \cdot 45 = 495$ coefficients in exact arithmetic and finds $\rho_{i, ab} = \pm 1/3$ in every case. This is measured on the design, not proved here for other $N$.

## Examples and non-examples

**Example: the 12-run design.** The cyclic shifts of `++-+++---+-` and a row of minus signs give the design for 11 factors, columns $A$ to $L$ (without $I$):

| run | levels of $A, B, C, D, E, F, G, H, J, K, L$ |
|---|---|
| 1 | `++-+++---+-` |
| 2 | `+-+++---+-+` |
| 3 | `-+++---+-++` |
| 4 | `+++---+-++-` |
| 5 | `++---+-++-+` |
| 6 | `+---+-++-++` |
| 7 | `---+-++-+++` |
| 8 | `--+-++-+++-` |
| 9 | `-+-++-+++--` |
| 10 | `+-++-+++---` |
| 11 | `-++-+++---+` |
| 12 | `-----------` |

Every column has six $+$ and six $-$, and every pair of columns shows $(+,+)$, $(+,-)$, $(-,+)$ and $(-,-)$ three times each. Any three columns contain all 8 level combinations, four of them once and four twice: a full $2^3$ design plus a half fraction. So if at most three factors matter, the experiment contains a full factorial in them. The test file checks all 165 triples.

**Example: an interaction, spread or concentrated.** Let the response be $y = 50 + 5x_A + 3x_D + 4x_A x_D$ with no noise, so $E_A = 10$, $E_D = 6$ and $E_{AD} = 8$. In the 12-run design the responses are $62, 62, 44, 48, 48, 48, 44, 46, 44, 62, 46, 46$, and the estimates are $\hat E_A = 10$, $\hat E_D = 6$, and $\pm 8/3$ for each of the other nine factors: $\rho = \pm 1/3$ times $E_{AD} = 8$. In the 8-run Sylvester design (the saturated $2^{7-4}$ fraction), the same model gives $10$ and $6$ for the two factors and $8$ on the one column equal to $x_A x_D$, a false main effect as large as a real one, and $0$ elsewhere. The 12-run design spreads the interaction thinly; the 8-run design hides it completely behind one factor.

**Example: from Sylvester to Plackett-Burman.** With $N = 8$ the Sylvester matrix $H_2^{\otimes 3}$, a [Kronecker product](/kronecker-product/) power whose rows are [Walsh-Hadamard](/walsh-hadamard-transform/) functions, gives the saturated $2^{7-4}$ design. The Kronecker product of the 12-run Hadamard matrix with $H_2$ gives a Hadamard matrix of order 24, and the Paley construction with $q = 23$ gives another.

**Example: a code.** The rows of a normalized Hadamard matrix $H$ of order $N$ and of $-H$, read as 0/1 vectors, form a binary code of $2N$ words with minimum distance $N/2$, the [Hadamard code](/hadamard-code/). For $N = 12$ it is the non-linear $(12, 24, 6)$ code.

**Non-example: 6 runs.** No two-level design with 6 runs has 5 orthogonal balanced columns, because a Hadamard matrix of order 6 does not exist (Theorem 1). The test file confirms it directly: no two $\pm 1$ vectors of length 6 that start with $+1$ and sum to zero are orthogonal.

**Non-example: the 12-run design is not a regular fraction.** In a regular $2^{k-p}$ fraction the product of two columns is again a column, up to sign. In the 12-run design $x_A \circ x_B$ has correlation $\pm 1/3$ with nine columns and equals none of them, so there is no defining relation and no resolution in the regular sense. Its main effects are clear of each other, as in resolution III.

## Related definitions

- [Fractional factorial design](/fractional-factorial-design/): the regular two-level fractions with $2^{k-p}$ runs and complete aliasing.
- [Factorial design](/factorial-design/): the full $2^k$ design; its model matrix is a Sylvester-Hadamard matrix.
- [Orthogonal array](/orthogonal-array/): a Plackett-Burman design is an orthogonal array of strength 2 with $N$ runs and $N - 1$ two-level factors, the largest number that the Rao bound allows.
- [Hadamard code](/hadamard-code/): the code from the rows of a Hadamard matrix and their negatives.
- [Quadratic residue](/quadratic-residue/): the residues of a prime $q \equiv 3 \pmod 4$ give the cyclic generators.
- [Optimal experimental design](/optimal-experimental-design/): among $N \times N$ matrices with entries $\pm 1$, a Hadamard matrix has the largest [determinant](/determinant/), $N^{N/2}$, so for the main-effect model a Plackett-Burman design is D-optimal.

## References
