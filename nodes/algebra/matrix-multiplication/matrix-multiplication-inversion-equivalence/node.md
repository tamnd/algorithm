---
tag: DP942C
kind: theorem
slug: matrix-multiplication-inversion-equivalence
name: Equivalence of matrix multiplication and inversion
aliases:
- inversion reduces to multiplication
- multiplication reduces to inversion
- matrix inversion is no harder than multiplication
area: algebra/matrix-multiplication
level: core
summary: Over a field, inverting an n×n matrix and multiplying two n×n matrices cost the same up to constant factors, so inversion also has the exponent ω.
prereqs: [naive-matrix-multiplication, matrix-inversion, schur-complement, reduction]
see_also: [strassen-algorithm, matrix-multiplication-exponent, lup-decomposition, determinant-computation, positive-definite-matrix, transitive-closure, triangular-system-solving, cholesky-decomposition]
sources:
  - paper: doi:10.1007/BF02165411
    title: Volker Strassen, Gaussian elimination is not optimal, Numerische Mathematik 13 (1969)
    locator: pp. 354 to 356 (inversion and determinant by block recursion with the fast product, when the leading blocks are invertible)
  - paper: doi:10.1090/S0025-5718-1974-0331751-8
    title: James R. Bunch and John E. Hopcroft, Triangular factorization and inversion by fast matrix multiplication, Mathematics of Computation 28(125) (1974)
    locator: pp. 231 to 236 (LUP decomposition and inversion of every nonsingular matrix over a field in O(M(n)) operations)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 28, Matrix Operations, Section 28.2, Inverting matrices (the theorems that multiplication is no harder than inversion and inversion is no harder than multiplication, with the regularity conditions)
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms
    locator: Chapter 6, Matrix multiplication and related operations (LUP decomposition, inversion and determinants in O(M(n)))
  - paper: "Walter Baur and Volker Strassen, The complexity of partial derivatives, Theoretical Computer Science 22 (1983), doi:10.1016/0304-3975(83)90110-X"
    locator: the main theorem and its corollary on the determinant (all partial derivatives at a constant factor more cost)
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory
    locator: Chapter 16, Problems related to matrix multiplication (inversion, determinant and LUP decomposition have the exponent ω)
---

Matrix multiplication and matrix inversion are equally hard up to constant factors. Multiplying two $n \times n$ matrices reduces to inverting one $3n \times 3n$ upper triangular matrix, and over a field, inverting a nonsingular $n \times n$ matrix reduces to a constant number of products of each size $n/2^j$ by block elimination. So any fast product, such as [Strassen's](/strassen-algorithm/), gives inversion with the same exponent, and the [exponent ω](/matrix-multiplication-exponent/) is also the exponent of inversion.

## Statement

Let $F$ be a field. Costs are counted in the algebraic model: field operations, divisions and zero tests, each at unit cost. Let $M(n)$ be the cost of the best algorithm that multiplies two $n \times n$ matrices over $F$, and $I(n)$ the cost of the best algorithm that inverts each nonsingular $n \times n$ matrix over $F$.

**Theorem.**

1. (Multiplication reduces to inversion.) $M(n) \le I(3n)$. This part holds over every ring.
2. (Inversion reduces to multiplication.) Suppose $M$ is regular: $M(2n) \le C \cdot M(n)$ for some constant $C$, and $M(n/2) \le c \, M(n)$ for some constant $c < 1/2$ and all even $n$. Then $I(n) = O(M(n))$.

In particular, $M(n) = O(n^{\alpha})$ for some $\alpha \ge 2$ implies $I(n) = O(n^{\alpha})$ (the regularity conditions hold for the bound $n^{\alpha}$, with $C = 2^{\alpha}$ and $c = 2^{-\alpha}$), and $I(n) = O(n^{\alpha})$ implies $M(n) = O(n^{\alpha})$. So the exponent of inversion equals $\omega$.

The proof below gives part 2 in full over the field $\mathbb{R}$ (and each subfield of it, such as $\mathbb{Q}$), where $A^{\mathsf T} A$ is positive definite. Over an arbitrary field, part 2 holds by the LUP decomposition of Bunch and Hopcroft (1974); the proof outline is given after the main proof.

## In plain words

Two jobs on square tables of numbers turn out to be equally hard: multiplying two tables, and finding the table that undoes a given table.

If you can undo tables fast, you can multiply fast: put the two tables into one larger table of a special shape, undo it, and read the product from one corner of the answer.

If you can multiply fast, you can undo tables fast: cut the table into four quarters, undo two smaller tables, and glue the pieces together with a few multiplications. The work is dominated by the multiplications at the top level, so undoing costs a constant times one multiplication.

## Proof

**Part 1.** Let $A, B \in R^{n \times n}$ over a ring $R$, and let

$$D = \begin{pmatrix} I_n & A & 0 \\ 0 & I_n & B \\ 0 & 0 & I_n \end{pmatrix}, \qquad E = \begin{pmatrix} I_n & -A & AB \\ 0 & I_n & -B \\ 0 & 0 & I_n \end{pmatrix}.$$

Block multiplication gives $DE = I_{3n}$: the block in position $(1, 2)$ is $-A + A = 0$, in position $(2, 3)$ it is $-B + B = 0$, and in position $(1, 3)$ it is $AB - AB + 0 = 0$. Also $ED = I_{3n}$ by the same computation. So $D$ is always invertible and $D^{-1} = E$. An inversion algorithm applied to $D$ returns $E$, whose top right block is $AB$. Building $D$ costs no arithmetic, so $M(n) \le I(3n)$. For example, with $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ and $B = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix}$, the top right block of $D^{-1}$ is $\begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix} = AB$.

**Part 2, positive definite case.** Let $A \in \mathbb{R}^{n \times n}$ be symmetric positive definite, with $n$ a power of two, and write

$$A = \begin{pmatrix} B & C^{\mathsf T} \\ C & D \end{pmatrix}, \qquad S = D - C B^{-1} C^{\mathsf T}.$$

The leading block $B$ is symmetric positive definite, since $x^{\mathsf T} B x$ is $A$'s form on vectors whose second half is $0$. The [Schur complement](/schur-complement/) $S$ is also symmetric positive definite: for $y \ne 0$ put $x = -B^{-1} C^{\mathsf T} y$; then $y^{\mathsf T} S y = (x, y)^{\mathsf T} A \, (x, y) > 0$. So $B^{-1}$ and $S^{-1}$ exist, and a direct block multiplication checks

$$A^{-1} = \begin{pmatrix} B^{-1} + W^{\mathsf T} S^{-1} W & -W^{\mathsf T} S^{-1} \\ -S^{-1} W & S^{-1} \end{pmatrix}, \qquad W = C B^{-1}.$$

Here $W^{\mathsf T} = B^{-1} C^{\mathsf T}$ because $B^{-1}$ is symmetric. The algorithm inverts $B$ recursively, forms $W = C B^{-1}$, $S = D - W C^{\mathsf T}$, inverts $S$ recursively, forms $V = S^{-1} W$ and $W^{\mathsf T} V$, and assembles $A^{-1}$ from $B^{-1} + W^{\mathsf T} V$, $-V^{\mathsf T}$, $-V$ and $S^{-1}$. That is $2$ inversions and $4$ products of order $n/2$, plus $O(n^2)$ additions and transposes. With $I_{\mathrm{pd}}(n)$ the cost for positive definite input,

$$I_{\mathrm{pd}}(n) \le 2 I_{\mathrm{pd}}(n/2) + 4 M(n/2) + a n^2$$

for a constant $a$. Unrolling, and using $M(n/2^{j+1}) \le c^{j+1} M(n)$ and $M(n) \ge n^2$ (each product writes $n^2$ outputs),

$$I_{\mathrm{pd}}(n) \le \sum_{j \ge 0} 2^j \left( 4 c^{j+1} M(n) + a \frac{n^2}{4^j} \right) + n \cdot I_{\mathrm{pd}}(1) \le \frac{4c}{1 - 2c} M(n) + 2a n^2 + n = O(M(n)),$$

because $2c < 1$.

**Part 2, nonsingular case over $\mathbb{R}$.** Let $A$ be nonsingular. Then $A^{\mathsf T} A$ is symmetric positive definite, since $x^{\mathsf T} A^{\mathsf T} A x = \lVert Ax \rVert^2 > 0$ for $x \ne 0$. And $A^{-1} = (A^{\mathsf T} A)^{-1} A^{\mathsf T}$. This costs two products and one positive definite inversion, so $I(n) \le 2 M(n) + I_{\mathrm{pd}}(n) = O(M(n))$.

**Sizes that are not powers of two.** Let $N = 2^{\lceil \lg n \rceil} < 2n$ and invert $\operatorname{diag}(A, I_{N-n})$, whose inverse is $\operatorname{diag}(A^{-1}, I_{N-n})$. This costs $O(M(N)) = O(M(2n)) = O(M(n))$ by the first regularity condition. $\blacksquare$

**Part 2 over an arbitrary field (outline).** Over a finite field the matrix $A^{\mathsf T} A$ need not be positive definite in any sense, and its leading block can be singular. For example, over $\mathbb{F}_2$ the matrix $A = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ is invertible, but $A^{\mathsf T} A = \begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix}$ has the leading entry $0$. Bunch and Hopcroft avoid this with pivoting. They compute an [LUP decomposition](/lup-decomposition/) $A = LUP$ of an $m \times n$ matrix of full row rank by splitting it into its top and bottom halves of rows: decompose the top half recursively, eliminate its pivot columns from the bottom half with one product, decompose what remains of the bottom half recursively, and combine the factors with permutations. The cost satisfies $T(m) \le 2T(m/2) + O(M(m) \cdot n/m)$, which is $O(M(n))$ for $m = n$ under the regularity conditions. Then $A^{-1} = P^{-1} U^{-1} L^{-1}$, and a triangular matrix is inverted in $O(M(n))$ by the block rule $\begin{pmatrix} L_1 & 0 \\ L_2 & L_3 \end{pmatrix}^{-1} = \begin{pmatrix} L_1^{-1} & 0 \\ -L_3^{-1} L_2 L_1^{-1} & L_3^{-1} \end{pmatrix}$, with $2$ products per level.

## Consequences

- **Fast inversion.** Strassen's algorithm gives inversion in $O(n^{\log_2 7})$ operations, and each bound $M(n) = O(n^{\alpha})$ on the product gives $I(n) = O(n^{\alpha})$. So every improvement of the [exponent ω](/matrix-multiplication-exponent/) applies to inversion.
- **Related problems with the exponent ω.** By the same block methods, the [LUP decomposition](/lup-decomposition/), the solution of a nonsingular linear system, and the [determinant](/determinant-computation/) all take $O(M(n))$ operations over a field. Conversely, Baur and Strassen (1983) showed that the gradient of a rational function costs at most a constant factor more than the function itself; the gradient of $\det A$ is the adjugate $\det(A) A^{-1}$, so the determinant is also as hard as inversion, up to a constant factor.
- **Gaussian elimination is not optimal.** The $\Theta(n^3)$ cost of [Gaussian elimination](/gaussian-elimination/) is not the true cost of inversion. This was the point of the title of Strassen's 1969 paper.
- **Boolean analogue.** Over the Boolean semiring there is no inverse, but the [transitive closure](/transitive-closure/) plays its role: $A^* = I + A + A^2 + \cdots$, and the same two reductions show that transitive closure and Boolean matrix multiplication have the same cost up to constant factors (Furman 1970, Fischer and Meyer 1971, Munro 1971).

## Tightness

- **Both directions are needed.** Part 1 alone shows that inversion is at least as hard as multiplication. With part 2 the two costs are within constant factors. The constants are small: for $M(n) = n^{\omega}$ with $\omega > 2$ the positive definite recursion costs about $4 / (2^{\omega} - 2)$ times $M(n)$ beyond the lower order terms, which is $2/3$ for $\omega = 3$ and $0.8$ for $\omega = \log_2 7$.
- **The regularity conditions.** The proof uses them only to sum the costs over the levels of the recursion and to pad to a power of two. Every bound of the form $n^{\alpha}$ with $\alpha > 1$ meets both conditions, so they exclude only cost functions that jump irregularly between sizes. With $c = 1/2$, as for a cost linear in $n$, the sum over the levels would gain a $\log n$ factor.
- **The field assumption.** Inversion is defined only for nonsingular matrices over a ring with division of the pivots. Over a commutative ring that is not a field, such as $\mathbb{Z}/12\mathbb{Z}$ or $\mathbb{Z}$ with exact integer inverses, the reduction of part 2 does not apply as stated, because the pivots of the block method need not be units.
- **Numerical stability.** Over floating-point numbers, the reduction through $A^{\mathsf T} A$ squares the condition number, and the error bounds of fast products are weaker than those of the classical product. The theorem is about operation counts in exact arithmetic, not about stable numerical algorithms.

## History

Strassen's 1969 paper, which introduced the $7$ multiplication product, also showed that inversion and the determinant can be computed in $O(n^{\log_2 7})$ operations by block recursion, when the leading blocks met in the recursion are invertible. Bunch and Hopcroft (1974) removed this condition with the LUP decomposition, so inversion of every nonsingular matrix over a field costs $O(M(n))$. The converse reduction, multiplication through the inverse of a $3n \times 3n$ triangular matrix, is presented in CLRS. The positive definite proof with $A^{\mathsf T} A$ follows the presentation of CLRS. Baur and Strassen (1983) added the determinant to the class of problems with exponent $\omega$.

## References
