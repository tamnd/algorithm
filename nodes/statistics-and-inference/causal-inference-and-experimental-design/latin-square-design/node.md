---
tag: AR1SZ9
kind: definition
slug: latin-square-design
name: Latin square design
aliases:
- Latin square experiment
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: Compares n treatments while blocking two nuisance factors with n levels each, by placing the treatments as the symbols of an n x n Latin square. Needs only n² runs.
prereqs: [randomized-block-design]
see_also: [counting-latin-squares, latin-square-completion, orthogonal-array, balanced-incomplete-block-design, singleton-bound, irreducible-polynomial, sudoku, latin-hypercube-sampling]
sources:
  - book: "Ronald A. Fisher, The Design of Experiments, Oliver and Boyd, Edinburgh, 1935"
    title: The Design of Experiments
    locator: the chapter on the Latin square (general locator, chapter not confirmed)
  - book: isbn:9780471718130
    title: George E. P. Box, J. Stuart Hunter and William G. Hunter, Statistics for Experimenters, second edition, Wiley, 2005
    locator: "Section 4.4 (more than one blocking component: Latin squares), starting on p. 157, and Appendix 4B (Latin, Graeco-Latin and hyper-Graeco-Latin squares)"
  - book: isbn:9781119492443
    title: Douglas C. Montgomery, Design and Analysis of Experiments, tenth edition, Wiley, 2019
    locator: Chapter 4 (the Latin square design and the Graeco-Latin square design; chapter-level locator)
  - paper: doi:10.4153/CJM-1960-016-5
    title: "R. C. Bose, S. S. Shrikhande and E. T. Parker, Further results on the construction of mutually orthogonal Latin squares and the falsity of Euler's conjecture, Canadian Journal of Mathematics 12, 1960"
    locator: pp. 189 to 203 (a pair of orthogonal Latin squares exists for every order except 2 and 6)
  - book: isbn:9780521006019
    title: J. H. van Lint and R. M. Wilson, A Course in Combinatorics, second edition, Cambridge University Press, 2001
    locator: the chapters on Latin squares and on orthogonal Latin squares (general locator, chapter numbers not confirmed)
---

A Latin square design compares $n$ treatments on $n^2$ experimental units that are classified in two directions, such as $n$ days by $n$ operators, or $n$ rows by $n$ columns of a field. Each treatment appears exactly once in each row and once in each column, so the treatments are placed as the symbols of a Latin square. Row and column differences then drop out of the treatment comparisons, as block differences do in a [randomized block design](/randomized-block-design/), but in two directions at once and with only $n^2$ runs instead of $n^3$. Two Latin squares that are orthogonal give a Graeco-Latin square, which blocks a third factor, and a complete set of $n - 1$ mutually orthogonal Latin squares exists when $n$ is a prime power.

## Definition

A **Latin square of order $n$** is an $n \times n$ array $L$ on $n$ symbols in which every symbol occurs exactly once in each row and exactly once in each column. Number the rows, columns and symbols $0, \dots, n - 1$. A **Latin square design** for $n$ treatments uses two blocking factors with $n$ levels each; the unit in row $i$ and column $j$ receives treatment $L(i, j)$. The square is randomized by permuting its rows, its columns and its symbols at random. The additive model is

$$y_{ij} = \mu + \rho_i + \gamma_j + \tau_{L(i,j)} + e_{ij},$$

with zero-sum row effects $\rho$, column effects $\gamma$ and treatment effects $\tau$, and iid $N(0, \sigma^2)$ errors. With row, column and treatment means $\bar y_{i\cdot}$, $\bar y_{\cdot j}$ and $\bar y_{(s)}$, the analysis is

| source | sum of squares | degrees of freedom |
|---|---|---|
| rows | $n\sum_i(\bar y_{i\cdot} - \bar y)^2$ | $n - 1$ |
| columns | $n\sum_j(\bar y_{\cdot j} - \bar y)^2$ | $n - 1$ |
| treatments | $n\sum_s(\bar y_{(s)} - \bar y)^2$ | $n - 1$ |
| error | $\sum_{i,j}(y_{ij} - \bar y_{i\cdot} - \bar y_{\cdot j} - \bar y_{(L(i,j))} + 2\bar y)^2$ | $(n - 1)(n - 2)$ |

and the treatment test is $F = MS_{\text{treatments}}/MSE$ on $(n - 1, (n - 1)(n - 2))$ degrees of freedom. A useful design needs $n \ge 3$.

**Theorem 1 (the analysis is exact).** The four sums of squares add up to the total, and under the model $F \sim F_{n-1,(n-1)(n-2)}$ when all $\tau_s = 0$.

*Proof.* Let $V_R$, $V_C$ and $V_T$ hold the zero-sum vectors that are constant on rows, on columns and on treatments. Rows and columns are orthogonal as in the randomized block design proof. For $a \in V_R$ and $c \in V_T$, $\langle a, c\rangle = \sum_i a_i\sum_j c_{L(i,j)} = \sum_i a_i\sum_s c_s = 0$, because row $i$ holds every symbol once. Columns and treatments are orthogonal for the same reason. So the constants, $V_R$, $V_C$ and $V_T$ are mutually orthogonal, and their orthogonal complement has dimension $n^2 - 1 - 3(n - 1) = (n - 1)(n - 2)$. Each sum of squares in the table is the squared length of the projection onto one of these subspaces, and the mean vector lies in their sum. The lemma on projections of a normal vector in the [one-way ANOVA](/one-way-anova/) proof gives the F law. $\square$

**Theorem 2 (a Latin square of every order).** For every $n \ge 1$, the cyclic square $L(i, j) = (i + j) \bmod n$ is a Latin square.

*Proof.* In row $i$, the map $j \mapsto (i + j) \bmod n$ is a bijection of $\{0, \dots, n - 1\}$ with inverse $s \mapsto (s - i) \bmod n$, so the row holds each symbol once. The same argument in $i$ applies to each column. $\square$

How many Latin squares there are is a hard counting problem; see [counting Latin squares](/counting-latin-squares/). Deciding whether a partly filled square can be completed is NP-complete; see [Latin square completion](/latin-square-completion/).

**Orthogonal squares.** Two Latin squares $L_1$ and $L_2$ of order $n$ are **orthogonal** if, superimposed, every ordered pair of symbols $(L_1(i,j), L_2(i,j))$ occurs exactly once. The superimposed square is a **Graeco-Latin square**: one symbol set blocks a third factor, or two treatment factors are run together. A set of squares that are orthogonal in pairs is a set of **mutually orthogonal Latin squares** (MOLS).

**Theorem 3 (at most $n - 1$ MOLS).** For $n \ge 2$, a set of mutually orthogonal Latin squares of order $n$ has at most $n - 1$ squares.

*Proof.* Renaming the symbols of one square keeps it Latin and keeps it orthogonal to the others, since a bijection of symbols maps the set of all $n^2$ ordered pairs onto itself. So assume the first row of every square is $0, 1, \dots, n - 1$. Look at the cell $(1, 0)$. In each square its symbol is not 0, because 0 is already in column 0 at $(0, 0)$. If two squares had the same symbol $s$ at $(1, 0)$, the pair $(s, s)$ would occur at $(1, 0)$ and also at $(0, s)$, which is a different cell; this contradicts orthogonality. So the squares have distinct nonzero symbols at $(1, 0)$, and there are at most $n - 1$ of them. $\square$

**Theorem 4 (a complete set for prime powers).** Let $q$ be a prime power and $\mathbb F_q$ the field with $q$ elements. For $a \in \mathbb F_q$, $a \ne 0$, put $L_a(x, y) = ax + y$. The $q - 1$ squares $L_a$ are mutually orthogonal Latin squares.

*Proof.* For fixed $x$, $y \mapsto ax + y$ is a bijection of $\mathbb F_q$; for fixed $y$, $x \mapsto ax + y$ is a bijection because $a \ne 0$ has an inverse. So each $L_a$ is Latin. For $a \ne b$ and a target pair $(u, v)$, the system $ax + y = u$, $bx + y = v$ gives $(a - b)x = u - v$, so $x = (u - v)/(a - b)$ and then $y = u - ax$: exactly one cell. So $L_a$ and $L_b$ are orthogonal. $\square$

For $q = p^m$ with $m > 1$, $\mathbb F_q$ is built as the polynomials over $\mathbb Z_p$ modulo an [irreducible polynomial](/irreducible-polynomial/) of degree $m$; the code finds one by trial division. Integers modulo a composite $n$ do not work, because $a$ may have no inverse.

**What is cited, not proved.** Euler conjectured in 1782 that no pair of orthogonal Latin squares exists for $n \equiv 2 \pmod 4$. Tarry checked $n = 6$ by hand in 1900, and $n = 2$ is immediate. Bose, Shrikhande and Parker (1960) proved that a pair exists for every other $n$, so Euler's conjecture fails for every $n \ge 10$. A complete set of $n - 1$ MOLS is equivalent to an affine plane of order $n$, and it is unknown whether one exists for any $n$ that is not a prime power.

**Theorem 5 (cyclic squares of even order have no mate).** If $n$ is even, the cyclic square has no orthogonal mate.

*Proof.* A mate $M$ would split the cells into $n$ classes $\{(i, j) : M(i, j) = s\}$, each holding one cell per row, one per column and, by orthogonality, one of each symbol of $L$: a transversal. Take one transversal, cells $(i, \pi(i))$ for a permutation $\pi$. Its symbols are all of $\mathbb Z_n$, so their sum is $n(n - 1)/2 \equiv n/2 \pmod n$ for even $n$. But the sum is also $\sum_i(i + \pi(i)) = n(n - 1) \equiv 0 \pmod n$. This is a contradiction. $\square$

**Codes and arrays.** $k - 2$ MOLS of order $n$ are the same object as an [orthogonal array](/orthogonal-array/) $OA(n^2, k, n, 2)$: one row per cell, holding the row index, the column index and the $k - 2$ symbols. Read as a code of length $k$ over $n$ symbols with $n^2$ words, it has minimum distance $k - 1$ and meets the [Singleton bound](/singleton-bound/), so it is an MDS code. The squares $L_a(x, y) = ax + y$ give the codewords $(x, y, ax + y)$, which are the evaluations of a linear code related to the [Reed-Solomon code](/reed-solomon-code/).

## Examples and non-examples

**Example: four treatments, days by operators.** The rows are four days, the columns four operators, and the treatments A to D follow the square $L_1$ of $\mathbb F_4$ below. The responses:

| | operator 1 | operator 2 | operator 3 | operator 4 |
|---|---|---|---|---|
| day 1 | A 30 | B 32 | C 31 | D 31 |
| day 2 | B 37 | A 34 | D 36 | C 28 |
| day 3 | C 29 | D 31 | A 31 | B 30 |
| day 4 | D 37 | C 31 | B 37 | A 25 |

The treatment means are 30, 34, 29.75 and 33.75, and the grand mean is 31.875.

| source | sum of squares | df | F | p |
|---|---|---|---|---|
| days | $117/4 = 29.25$ | 3 | 2.786 | 0.132 |
| operators | $269/4 = 67.25$ | 3 | 6.405 | 0.0267 |
| treatments | $257/4 = 64.25$ | 3 | $257/42 = 6.119$ | 0.0295 |
| error | 21 | 6 | | |

With $F_{(3,6,0.95)} = 4.757$, the treatments differ at the 5% level. A [one-way ANOVA](/one-way-anova/) of the same 16 values by treatment alone puts days and operators into the error, $SSW = 117.5$ on 12 degrees of freedom, and gives $F = 2.187$, $p = 0.142$.

**Example: a Graeco-Latin square of order 3.** $\mathbb F_3$ gives $L_1(x, y) = x + y$ and $L_2(x, y) = 2x + y$. Writing $L_1$ as A, B, C and $L_2$ as α, β, γ:

| | | |
|---|---|---|
| Aα | Bβ | Cγ |
| Bγ | Cα | Aβ |
| Cβ | Aγ | Bα |

Each of the nine pairs occurs once. By Theorem 3 no third square can be added.

**Example: a complete set of order 4.** $\mathbb F_4 = \{0, 1, \omega, \omega + 1\}$ with $\omega^2 = \omega + 1$, coded 0, 1, 2, 3. The three squares $L_a(x, y) = ax + y$ have the rows

- $L_1$: 0123, 1032, 2301, 3210;
- $L_\omega$: 0123, 2301, 3210, 1032;
- $L_{\omega+1}$: 0123, 3210, 1032, 2301.

They are mutually orthogonal, and the exhaustive search in the test file confirms that no set of 4 MOLS of order 4 exists.

**Non-example: order 2.** Theorem 3 allows at most $2 - 1 = 1$ square. Directly: after renaming symbols both squares are 01 / 10, and superimposed they show only the pairs 00 and 11. There is no Graeco-Latin square of order 2.

**Non-example: the cyclic square of order 4.** 0123 / 1230 / 2301 / 3012 is Latin but has no transversal (Theorem 5), so it has no orthogonal mate, while the square $L_1$ of $\mathbb F_4$, of the same order, has two mates.

**Non-example: order 6.** There is no pair of orthogonal Latin squares of order 6 (Tarry, 1900), so no Graeco-Latin design for six treatments; this is Euler's problem of the 36 officers.

**Non-example: interaction.** If the effect of a treatment depends on the day or the operator, the additive model fails and the interaction goes into the error with only $(n - 1)(n - 2)$ degrees of freedom. With $n = 3$ there are only 2. Small Latin squares are often replicated for this reason.

## Related definitions

- [Randomized block design](/randomized-block-design/): blocking in one direction; a Latin square blocks in two.
- [Balanced incomplete block design](/balanced-incomplete-block-design/): blocks smaller than the number of treatments; finite fields and affine planes give both kinds of design.
- [Orthogonal array](/orthogonal-array/): MOLS are orthogonal arrays of strength 2, and Latin squares are fractions of the $n^3$ factorial.
- [Factorial design](/factorial-design/): a Latin square is a one-$n$th fraction of the $n \times n \times n$ factorial in rows, columns and treatments, aliasing the interactions with the main effects.
- [Sudoku](/sudoku/): a Latin square of order 9 with the extra condition on the $3 \times 3$ boxes; its completion is an [exact cover](/exact-cover/) problem.
- [Latin hypercube sampling](/latin-hypercube-sampling/): one sample in each row and column stratum, the same idea used for numerical integration.

## References
