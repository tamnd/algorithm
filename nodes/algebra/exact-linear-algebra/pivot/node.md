---
tag: S0VPP8
kind: concept
slug: pivot
name: Pivot
aliases: [pivot element, pivoting, pivot column, pivot position]
area: algebra/exact-linear-algebra
level: intro
summary: The leading nonzero entry chosen in a row during elimination; choosing it is pivoting.
prereqs: [gaussian-elimination]
see_also: [echelon-form, reduced-row-echelon-form, rank, lu-decomposition, bareiss-algorithm, partial-pivoting, fill-in, structured-gaussian-elimination]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 3.2, The LU Factorization (pivots and leading principal minors), and Section 3.4, Pivoting (row interchanges, partial and complete pivoting)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer
    locator: Section 2.2.2, Gaussian elimination and solving linear systems (in exact arithmetic any nonzero pivot is correct, and the choice only changes the cost)
  - paper: doi:10.1090/S0025-5718-1968-0226829-0
    title: Erwin H. Bareiss, Sylvester's identity and multistep integer-preserving Gaussian elimination, Mathematics of Computation 22(103), 1968
    locator: pp. 565 to 578 (the pivots of fraction-free elimination are the leading principal minors)
  - paper: doi:10.1287/mnsc.3.3.255
    title: Harry M. Markowitz, The elimination form of the inverse and its application to linear programming, Management Science 3(3), 1957
    locator: the rule that chooses a pivot of small row count times column count to limit fill-in in sparse elimination
---

A *pivot* is the nonzero entry that [Gaussian elimination](/gaussian-elimination/) uses at one step to clear the other entries of its column. In an [echelon form](/echelon-form/) the pivot of a row is its first nonzero entry, and the columns that hold pivots are the *pivot columns*. *Pivoting* is the choice of the pivot, by row swaps and sometimes column swaps, when the natural candidate is zero or a poor choice. In exact arithmetic any nonzero pivot gives a correct result, so the choice is about cost: the size of the numbers, the fill-in of a sparse matrix, or the length of a gcd computation over the integers.

## In plain words

Elimination solves equations by using one equation to remove a variable from all the others. The number that multiplies that variable in the chosen equation is the pivot. You divide by it, so it must not be zero.

When the number you would like to use is zero, you swap in another equation that has a nonzero number there. If no equation has one, that variable is free, and you move on to the next one.

When you compute exactly, with fractions or with remainders, every nonzero choice gives the right answer. The choice still matters for speed: a good choice keeps the numbers short and keeps the empty places of a sparse matrix empty. When you compute with rounded numbers, the choice also controls the rounding errors.

## The idea

**Notation.** $A$ is an $m \times n$ matrix over a field $K$ or an integral domain $R$; for a square matrix $n$ is its size. Rows and columns are numbered from $1$.

**Pivots in an echelon form.** A matrix $E$ is in row echelon form when each zero row is below each nonzero row, and the first nonzero entry of each nonzero row is strictly to the right of the first nonzero entry of the row above. That first nonzero entry is the *pivot* of the row, its place $(i, p_i)$ is a *pivot position*, and $p_1 < p_2 < \cdots < p_r$ are the *pivot columns*. The number $r$ of pivots is the [rank](/rank/) of $E$, and of each matrix that row operations turn into $E$.

**Pivots during elimination.** At step $k$, elimination has $k-1$ pivot rows above and a remaining block below. It looks for the first column $c$ in which the remaining block has a nonzero entry, picks one such entry $a_{ic}$ (the pivot), swaps row $i$ into row $k$, and subtracts multiples $a_{jc}/a_{kc}$ of row $k$ from the rows $j > k$. Over an integral domain the [Bareiss algorithm](/bareiss-algorithm/) multiplies by the pivot instead of dividing, and then divides exactly by the previous pivot.

**Pivot columns do not depend on the choices.** Column $j$ of $A$ is a pivot column if and only if column $j$ is not a linear combination of columns $1, \ldots, j-1$. Proof: row operations act by an invertible matrix $P$ on the left, and $P$ keeps every linear relation among the columns: $\sum_l c_l a_l = 0$ if and only if $\sum_l c_l (P a_l) = 0$. So column $j$ of $A$ depends on the earlier columns exactly when column $j$ of $E = PA$ does. In $E$, a pivot column has a nonzero entry in a row where all earlier columns are zero, so it is not a combination of them; a non-pivot column $j$ has nonzero entries only in the rows $1, \ldots, t$ of the pivots to its left, and the pivot columns $p_1, \ldots, p_t$ restricted to these rows form an invertible triangular matrix, so column $j$ is a combination of them. $\square$ So the pivot columns are the same for every sequence of pivot choices. They are the *column rank profile* of $A$: the lexicographically first set of $r$ independent columns.

**Pivots and leading minors.** Let $A$ be $n \times n$ and let $\Delta_k$ be the determinant of the leading $k \times k$ block of $A$, with $\Delta_0 = 1$. Suppose elimination runs with no row swaps and its pivots $u_{11}, \ldots, u_{kk}$ are nonzero. Then

$$\Delta_k = u_{11} u_{22} \cdots u_{kk}, \qquad u_{kk} = \frac{\Delta_k}{\Delta_{k-1}}.$$

Proof: step $t$ adds multiples of row $t$ to rows below it. Restricted to the leading $k \times k$ block, for $t < k$, this adds multiples of a row of the block to another row of the block, which does not change its determinant. After $k-1$ steps the leading block is upper triangular with diagonal $u_{11}, \ldots, u_{kk}$, and its determinant is their product. $\square$ So elimination without swaps on an $n \times n$ matrix meets no zero pivot in steps $1$ to $n-1$ if and only if $\Delta_1, \ldots, \Delta_{n-1}$ are all nonzero. This is the condition for an [LU decomposition](/lu-decomposition/) without a permutation. In the Bareiss algorithm the $k$-th pivot is $\Delta_k$ itself, which is why its divisions are exact.

**Pivoting strategies.** In exact arithmetic the choice of a nonzero pivot never changes the result of a determinant, a rank or a solution. It changes the cost.

- *Over $\mathbb{Z}/p\mathbb{Z}$ or another finite field*, every nonzero entry costs the same, so take the first one.
- *Over $\mathbb{Q}$ with fractions*, a pivot with a short numerator and denominator keeps the new entries shorter. The bound on the final sizes comes from the [Hadamard bound](/hadamard-bound/) on minors and does not depend on the choice, but the gcd work in between does.
- *For a sparse matrix*, a pivot in a row with $r_i$ nonzeros and a column with $c_j$ nonzeros can create up to $(r_i - 1)(c_j - 1)$ new nonzeros (the [fill-in](/fill-in/)). Markowitz's rule picks a nonzero pivot with small $(r_i - 1)(c_j - 1)$. [Structured Gaussian elimination](/structured-gaussian-elimination/) builds on this idea.
- *Over $\mathbb{Z}$ for normal forms*, the [Hermite](/hermite-normal-form/) and [Smith](/smith-normal-form/) forms make the pivot the gcd of a column. Taking the entry of smallest absolute value as the pivot and reducing the others modulo it is Euclid's algorithm on the column.
- *In floating point*, [partial pivoting](/partial-pivoting/) takes the entry of largest absolute value in the column, and [complete pivoting](/complete-pivoting/) the largest in the whole remaining block, to bound the [growth factor](/growth-factor/). These rules are about rounding error and have no role in exact arithmetic.

## Examples

**Pivots equal ratios of leading minors.** For

$$A = \begin{pmatrix} 2 & 1 & 1 \\ 4 & 3 & 3 \\ 8 & 7 & 9 \end{pmatrix}$$

elimination without swaps subtracts $2$ and $4$ times row $1$, then $3$ times the new row $2$, and gives the upper triangular matrix with rows $(2, 1, 1)$, $(0, 1, 1)$, $(0, 0, 2)$. The pivots are $2, 1, 2$. The leading minors are $\Delta_1 = 2$, $\Delta_2 = 2 \cdot 3 - 1 \cdot 4 = 2$ and $\Delta_3 = \det A = 4$, and indeed $2 = 2/1$, $1 = 2/2$ and $2 = 4/2$.

**A zero pivot needs a swap.** For $A = \begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix}$ the first candidate is $a_{11} = 0$, and $\Delta_1 = 0$. Elimination swaps the two rows and gets the pivots $1$ and $1$, with $\det A = -1 \cdot 1 = -1$ because of the swap. Without the swap there is no factorization $A = L U$ with $L$ unit lower triangular: the entry $(1,1)$ of $LU$ is $u_{11}$, so $u_{11} = 0$, and then the entry $(2,1)$ of $LU$ is $l_{21} u_{11} = 0 \neq 1$.

**A column with no pivot.** For the matrix with rows $(1, 2, 3)$, $(4, 5, 6)$, $(7, 8, 9)$ the pivot columns are $1$ and $2$. Column $3$ has no pivot, because column $3$ equals $2 \cdot$ column $2 - $ column $1$. The rank is $2$.

**Pivot order and fill-in.** Take the $5 \times 5$ arrow matrix with $5$ on the diagonal, $1$ in the rest of the first row and the first column, and $0$ elsewhere. It has $13$ nonzero entries. With $a_{11}$ as the first pivot, each row $i$ from $2$ to $5$ becomes $\tfrac{24}{5}$ on the diagonal and $-\tfrac15$ in the other places of columns $2$ to $5$, and the remaining $4 \times 4$ block has $16$ nonzeros instead of $4$. With the pivots $a_{55}, a_{44}, a_{33}, a_{22}$ first, each step changes only the entry $(1,1)$, and there is no fill-in at all. Both orders give the same determinant.

## Where it is used

- [Gaussian elimination](/gaussian-elimination/) and [Gauss-Jordan elimination](/gauss-jordan-elimination/) pick one pivot in each step; the number of pivots is the [rank](/rank/), read in [rank computation](/rank-computation/).
- The [reduced row echelon form](/reduced-row-echelon-form/) scales each pivot to $1$ and clears its column, and its free columns give the [nullspace](/nullspace/).
- The [LU decomposition](/lu-decomposition/) with row swaps records the pivot rows in a permutation, $P A = L U$.
- The [Bareiss algorithm](/bareiss-algorithm/) divides by the previous pivot, which is a leading minor.
- The [determinant by Gaussian elimination](/determinant-gaussian-elimination/) is the product of the pivots, with a sign for each row swap.
- [Structured Gaussian elimination](/structured-gaussian-elimination/) chooses pivots in sparse columns first to keep the matrix sparse.
- The [Kannan-Bachem algorithm](/kannan-bachem-algorithm/) and other normal form algorithms over $\mathbb{Z}$ make each pivot a gcd.

## References
