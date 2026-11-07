---
tag: YZ8PWB
kind: theorem
slug: cramers-rule
name: Cramer's rule
aliases:
- Cramer's method
- Cramer's theorem
- adjugate formula
area: algebra/exact-linear-algebra
level: intro
summary: Expresses each unknown of a square nonsingular system as a ratio of determinants.
prereqs: [determinant]
see_also: [determinant, laplace-expansion, matrix-inversion, hadamard-bound, dixon-p-adic-lifting, gaussian-elimination, unimodular-matrix, determinant-computation]
sources:
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition
    locator: Chapter 5, Section 5.4, Additional properties of determinants (the classical adjoint and Cramer's rule)
  - book: isbn:9780980232714
    title: Gilbert Strang, Introduction to Linear Algebra, fourth edition
    locator: Chapter 5, Section 5.3, Cramer's rule, inverses, and volumes
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition
    locator: Section 5.5, Modular determinant computation (solutions of integer systems as quotients of determinants, bounded by Hadamard's inequality)
  - book: "Gabriel Cramer, Introduction a l'analyse des lignes courbes algebriques, Geneva, 1750"
    locator: the appendix on the solution of linear equations (the rule for any number of unknowns)
---

Cramer's rule gives the solution of a square linear system $Ax = b$ with $\det A \ne 0$ in closed form: the unknown $x_j$ is $\det A_j(b) / \det A$, where $A_j(b)$ is $A$ with column $j$ replaced by $b$. Behind it is the adjugate identity $\operatorname{adj}(A)\, A = A \operatorname{adj}(A) = \det(A)\, I$, which holds over each commutative ring. The rule is a slow way to compute a solution, but it is the main tool to *bound* solutions: for an integer system, it shows that each solution is an integer vector divided by $\det A$, and with the [Hadamard bound](/hadamard-bound/) it fixes how large the numbers can be.

Notation: $R$ is a commutative ring, for example $\mathbb{Z}$ or a field $K$. $A$ is an $n \times n$ matrix over $R$ with columns $a_1, \dots, a_n$, $e_1, \dots, e_n$ are the unit vectors, and $A^{(k,i)}$ is the $(n-1) \times (n-1)$ matrix obtained from $A$ by deleting row $k$ and column $i$.

## Statement

**Theorem.** Let $n \ge 1$ and $b \in R^n$. For $1 \le j \le n$ let $A_j(b)$ be $A$ with column $j$ replaced by $b$. Define the *adjugate* $\operatorname{adj}(A)$ as the $n \times n$ matrix with entries $\operatorname{adj}(A)_{ik} = (-1)^{i+k} \det A^{(k,i)}$ (note the transposed indices).

1. $\operatorname{adj}(A)\, A = A\, \operatorname{adj}(A) = \det(A)\, I_n$.
2. If $x \in R^n$ satisfies $Ax = b$, then $\det(A)\, x_j = \det A_j(b)$ for each $j$.
3. If $\det A$ is a unit of $R$ (over a field: if $\det A \ne 0$), then $Ax = b$ has exactly one solution, $x_j = \det A_j(b) / \det A$, and $A^{-1} = \operatorname{adj}(A) / \det A$.

## In plain words

Take a square system with as many equations as unknowns, whose determinant is not zero. To find one unknown, replace its column of coefficients by the column of right-hand sides and take the determinant of that new matrix. Divide by the determinant of the original matrix. The result is the value of that unknown. Each unknown needs one more determinant, so the rule is slow for big systems. Its real use is as a fact: every solution is a quotient of two determinants. So the bottom of each fraction is the same number, and the size of every value is bounded by the size of determinants.

## Proof

*Part 2.* Let $Ax = b$, so $b = \sum_{k} x_k a_k$. The [determinant](/determinant/) is linear in column $j$, so

$$
\det A_j(b) = \sum_{k=1}^{n} x_k \det(a_1, \dots, a_{j-1}, a_k, a_{j+1}, \dots, a_n).
$$

For $k \ne j$, the matrix in the term has the column $a_k$ twice, so its determinant is $0$, because the determinant is alternating. The term $k = j$ is $x_j \det A$. This proves part 2, over any commutative ring.

*Cofactors.* Let $C_{ki} = \det(a_1, \dots, a_{i-1}, e_k, a_{i+1}, \dots, a_n)$, the determinant of $A$ with column $i$ replaced by $e_k$. We show $C_{ki} = (-1)^{i+k} \det A^{(k,i)}$, so that $\operatorname{adj}(A)_{ik} = C_{ki}$. Move column $i$ to the front by $i - 1$ swaps of adjacent columns, and row $k$ to the top by $k - 1$ swaps of adjacent rows. Each swap changes the sign, so $C_{ki} = (-1)^{i+k-2} \det B = (-1)^{i+k} \det B$, where $B$ has first column $e_1$ and has $A^{(k,i)}$ in rows $2, \dots, n$ and columns $2, \dots, n$. In the Leibniz formula for $\det B$, a nonzero term needs $\sigma(1) = 1$, because column $1$ of $B$ is zero except in row $1$, where it is $1$. The permutations with $\sigma(1) = 1$ are the permutations of $\{2, \dots, n\}$, with the same sign. So $\det B = \det A^{(k,i)}$.

*Part 1.* Entry $(i, j)$ of $\operatorname{adj}(A) A$ is $\sum_k C_{ki}\, a_{kj}$. By linearity of the determinant in column $i$, this is the determinant of $A$ with column $i$ replaced by $\sum_k a_{kj} e_k = a_j$. For $j = i$ this is $\det A$. For $j \ne i$ the column $a_j$ appears twice, so it is $0$. Hence $\operatorname{adj}(A) A = \det(A) I$. Apply this to $A^T$. Since $\det$ is invariant under transposition and $(A^T)^{(k,i)} = (A^{(i,k)})^T$, we get $\operatorname{adj}(A^T) = \operatorname{adj}(A)^T$, so $\operatorname{adj}(A)^T A^T = \det(A) I$. Transposing gives $A \operatorname{adj}(A) = \det(A) I$.

*Part 3.* Let $d = \det A$ be a unit. By part 1, $A \cdot (d^{-1} \operatorname{adj}(A)) = I$ and $(d^{-1}\operatorname{adj}(A)) \cdot A = I$, so $A^{-1} = d^{-1}\operatorname{adj}(A)$. Then $x = A^{-1} b$ is a solution, and each solution satisfies $x = A^{-1} A x = A^{-1} b$, so it is unique. Its entry $j$ is $d^{-1} \sum_k C_{kj} b_k$, and by linearity in column $j$, $\sum_k C_{kj} b_k = \det A_j(b)$. So $x_j = \det A_j(b)/d$, which also follows from part 2. $\blacksquare$

**Example.** For $2x + y = 5$ and $x + 3y = 10$, $\det A = 2 \cdot 3 - 1 \cdot 1 = 5$, $\det A_1(b) = 5 \cdot 3 - 1 \cdot 10 = 5$ and $\det A_2(b) = 2 \cdot 10 - 5 \cdot 1 = 15$. So $x = 1$ and $y = 3$. For the matrix $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$ and $b = (1, 0, 7)$, $\det M = 18$ and the three replaced determinants are $18$, $-18$ and $36$, so $x = (1, -1, 2)$.

## Consequences

- **Solutions of integer systems.** If $A$ and $b$ have integer entries and $d = \det A \ne 0$, then $d \cdot x$ is an integer vector. With the [Hadamard bound](/hadamard-bound/), each numerator $\det A_j(b)$ and the common denominator $d$ have absolute value at most $n^{n/2} B^n$ when all entries of $A$ and $b$ are at most $B$ in absolute value. This bound tells [Dixon's p-adic lifting](/dixon-p-adic-lifting/) and the multimodular methods how far to lift or how many primes to use before rational reconstruction.
- **The inverse.** $A^{-1} = \operatorname{adj}(A)/\det A$. Over $\mathbb{Z}$, an integer matrix has an integer inverse exactly when $\det A = \pm 1$, which is the definition of a [unimodular matrix](/unimodular-matrix/). Over any commutative ring, $A$ is invertible exactly when $\det A$ is a unit: part 3 gives one direction, and $\det A \det A^{-1} = 1$ the other.
- **Entries of elimination.** The entries that [Gaussian elimination](/gaussian-elimination/) produces are quotients of minors of the input, a fact of the same kind; the [Bareiss algorithm](/bareiss-algorithm/) keeps the numerators of these quotients as integers.
- **Cost.** Computing $n + 1$ determinants by elimination costs $\Theta(n^4)$ field operations, against $\Theta(n^3)$ for one elimination with back substitution, so the rule is not a good algorithm for $n \ge 3$ or so. For $n = 2$ and $n = 3$ it is a common closed form in geometry code.
- **Polynomial and parametric systems.** Over $R = K[t]$, part 2 shows that the solution of a system whose entries are polynomials in $t$ is a vector of rational functions with the common denominator $\det A$, of degree at most the sum of the column degrees.

## Tightness

The hypothesis that $\det A$ is a unit cannot be dropped.

- Over $\mathbb{Z}$, the $1 \times 1$ system $2x = 1$ has $\det A = 2 \ne 0$ but no integer solution. Part 2 still holds for every solution in a larger ring: $2 \cdot \tfrac12 = 1 = \det A_1(b)$.
- Over a field with $\det A = 0$, part 2 gives a necessary condition only. For $A = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ and $b = (1, 2)$, $\det A_1(b) = 1 - 2 = -1 \ne 0 = \det(A) x_1$, so there is no solution. But the converse fails: for the zero $2 \times 2$ matrix and $b = (1, 0)$, all $\det A_j(b)$ are $0$, and still there is no solution. When a solution exists it is not unique, so no formula of this kind can give "the" solution.

## History

Gabriel Cramer published the rule for systems with any number of unknowns in 1750, in an appendix to his book on algebraic curves, where he needed it to find the curve through given points. The adjugate matrix and the matrix form of the rule came in the nineteenth century, with the theory of matrices.

## References
