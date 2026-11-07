---
tag: Q03RMC
kind: theorem
slug: hadamard-bound
name: Hadamard bound
aliases:
- Hadamard's inequality
- Hadamard's determinant inequality
area: algebra/exact-linear-algebra
level: advanced
summary: Bounds the absolute value of a determinant by the product of the Euclidean norms of its columns.
prereqs: [determinant]
see_also: [determinant-computation, multimodular-determinant, bareiss-algorithm, cramers-rule, dixon-p-adic-lifting, gram-schmidt-orthogonalization, lattice-determinant, lll-algorithm]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 16, Short vectors in lattices (Hadamard's inequality, proved with the Gram-Schmidt orthogonal basis); used in Section 5.5, Modular determinant computation, to bound the number of primes
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition
    locator: Section 7.8, Determinant inequalities (Hadamard's inequality for positive semidefinite matrices and for arbitrary matrices, with the case of equality)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.5, Basic algorithms on lattices (Hadamard's inequality for the determinant of a lattice, through Gram-Schmidt orthogonalization)
  - paper: "Jacques Hadamard, Resolution d'une question relative aux determinants, Bulletin des Sciences Mathematiques 17, 1893"
    locator: pp. 240 to 246 (the inequality and the case of equality)
  - paper: "James Joseph Sylvester, Thoughts on inverse orthogonal matrices, simultaneous sign-successions, and tessellated pavements in two or more colours, Philosophical Magazine 34, 1867"
    locator: pp. 461 to 475 (the doubling construction of orthogonal matrices with entries plus and minus one)
---

The Hadamard bound says that the absolute value of a determinant is at most the product of the Euclidean lengths of the columns, and also at most the product of the lengths of the rows. Geometrically, a parallelepiped with given edge lengths has the largest volume when the edges are orthogonal. In exact linear algebra it is the standard *a priori* bound on the size of a determinant: an $n \times n$ integer matrix with entries less than $2^b$ in absolute value has a determinant with at most $n(b + \tfrac12 \log_2 n) + 1$ bits. That number decides how many primes a [multimodular determinant](/multimodular-determinant/) needs, how far [Dixon's p-adic lifting](/dixon-p-adic-lifting/) must go, and how large the numbers in the [Bareiss algorithm](/bareiss-algorithm/) and in elimination over $\mathbb{Q}$ can become.

Notation: $A$ is an $n \times n$ matrix over $\mathbb{R}$ or $\mathbb{C}$ with rows $a_1, \dots, a_n$ and columns $a^1, \dots, a^n$, $\|v\| = (\sum_j |v_j|^2)^{1/2}$ is the Euclidean norm, and $\langle u, v \rangle = \sum_j u_j \overline{v_j}$. For an integer matrix, $b$ is the maximum binary length of an entry, so $|a_{ij}| < 2^b$.

## Statement

**Theorem (Hadamard's inequality).** For every $n \times n$ matrix $A$ over $\mathbb{C}$,

$$
|\det A| \le \prod_{i=1}^{n} \|a_i\| \qquad \text{and} \qquad |\det A| \le \prod_{j=1}^{n} \|a^j\|.
$$

Equality holds in the first inequality exactly when some row is zero or the rows are pairwise orthogonal, and in the second exactly when some column is zero or the columns are pairwise orthogonal.

**Corollary.** If $|a_{ij}| \le B$ for all $i, j$, then $|\det A| \le n^{n/2} B^n$. If $A$ has integer entries with $|a_{ij}| < 2^b$, then $\log_2 |\det A| < n(b + \tfrac12 \log_2 n)$ whenever $\det A \ne 0$. The same bounds hold for every $k \times k$ minor with $k$ in place of $n$.

## In plain words

Think of the rows of a square matrix as the edges of a box that starts at one corner. The determinant measures the volume of that box, up to its sign. If you keep the length of each edge fixed and only turn the edges, the volume is largest when the edges meet at right angles, and then it is the product of the lengths. A slanted box is flatter and has less volume. So the determinant can never be larger than the product of the row lengths. For whole numbers, this tells you in advance how many digits the determinant can have.

## Proof

We prove the bound for the rows. The bound for the columns follows by applying it to the transpose $A^T$ (over $\mathbb{C}$, to $\overline{A}^T$), because $|\det A^T| = |\det \overline{A}^T| = |\det A|$.

*Case 1: the rows are linearly dependent.* Then $\det A = 0$ and the inequality holds. Equality means that the product of the norms is $0$, that is, some row is zero.

*Case 2: the rows are linearly independent.* Apply [Gram-Schmidt orthogonalization](/gram-schmidt-orthogonalization/) to the rows: put $a_1^* = a_1$ and, for $i = 2, \dots, n$,

$$
a_i^* = a_i - \sum_{j<i} \mu_{ij}\, a_j^*, \qquad \mu_{ij} = \frac{\langle a_i, a_j^* \rangle}{\langle a_j^*, a_j^* \rangle}.
$$

By induction on $i$, the vectors $a_1^*, \dots, a_i^*$ are pairwise orthogonal, they span the same space as $a_1, \dots, a_i$, and each $a_i^*$ is nonzero, because $a_i$ is not in the span of $a_1, \dots, a_{i-1}$. Let $A^*$ be the matrix with rows $a_i^*$. Then $A = L A^*$, where $L$ is lower triangular with $1$ on the diagonal and $\mu_{ij}$ below it. So $\det A = \det L \cdot \det A^* = \det A^*$.

The rows of $A^*$ are orthogonal, so $A^* \overline{A^*}^T$ is the diagonal matrix with entries $\|a_i^*\|^2$. Taking determinants, $|\det A^*|^2 = \det A^* \cdot \overline{\det A^*} = \prod_i \|a_i^*\|^2$, so $|\det A| = \prod_i \|a_i^*\|$.

Finally, $a_i = a_i^* + \sum_{j<i} \mu_{ij} a_j^*$, and $a_i^*$ is orthogonal to every $a_j^*$ with $j < i$. By Pythagoras,

$$
\|a_i\|^2 = \|a_i^*\|^2 + \Big\| \sum_{j<i} \mu_{ij} a_j^* \Big\|^2 \ge \|a_i^*\|^2. \qquad (1)
$$

Multiplying over $i$ gives $|\det A| = \prod_i \|a_i^*\| \le \prod_i \|a_i\|$.

*Equality in case 2.* All factors are positive, so equality holds exactly when $\|a_i^*\| = \|a_i\|$ for every $i$, that is, when the second term in (1) is $0$ for every $i$. The vectors $a_j^*$ are orthogonal and nonzero, so this means $\mu_{ij} = 0$ for all $j < i$, which by induction gives $a_i^* = a_i$ for every $i$. So the rows $a_i$ are pairwise orthogonal. Conversely, if the rows are orthogonal, then every $\mu_{ij}$ is $0$ and $a_i^* = a_i$.

*The corollary.* If $|a_{ij}| \le B$, then $\|a_i\| \le \sqrt{n} B$, so $|\det A| \le (\sqrt{n} B)^n = n^{n/2} B^n$. With $B = 2^b$ (a strict bound $|a_{ij}| < 2^b$ gives $\|a_i\| < \sqrt{n}\, 2^b$ for every nonzero row), taking $\log_2$ gives $\log_2 |\det A| < n(b + \tfrac12 \log_2 n)$. A $k \times k$ minor is the determinant of a $k \times k$ matrix with the same entry bound, so the same argument applies with $k$. $\blacksquare$

**Example.** For $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$, the row norms are $\sqrt{5}$, $\sqrt{11}$ and $\sqrt{17}$, and the bound is $\sqrt{935} \approx 30.58$, while $\det M = 18$. For $\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ the row bound is $\sqrt{5} \cdot 5 \approx 11.18$, the column bound is $\sqrt{10} \cdot \sqrt{20} \approx 14.14$, and the determinant is $-2$. The two bounds differ, and a program may use the smaller one.

## Consequences

- **Number of primes.** To recover an integer $d$ with $|d| \le H$ from its residues, the product of the moduli must exceed $2H$. With $H = n^{n/2} 2^{bn}$, about $n(b + \tfrac12 \log_2 n)/\log_2 p + 1$ primes near $p$ suffice. This is how the [multimodular determinant](/multimodular-determinant/) chooses the number of primes (MCA Section 5.5).
- **Size of solutions.** By [Cramer's rule](/cramers-rule/), the solution of a nonsingular integer system $Ax = b'$ has numerators $\det A_j(b')$ and denominator $\det A$, all bounded by the Hadamard bound of the matrices involved. This fixes the precision of p-adic lifting and of rational reconstruction.
- **Size of intermediate numbers.** Every entry produced by the [Bareiss algorithm](/bareiss-algorithm/) is a minor of the input, and every entry produced by elimination over $\mathbb{Q}$ is a quotient of two minors. So every intermediate number has $O(n(b + \log n))$ bits. This gives the proved bound of $O(n^5 (b + \log n)^2)$ bit operations for [elimination over $\mathbb{Q}$](/determinant-gaussian-elimination/) with schoolbook arithmetic.
- **Characteristic polynomial.** The coefficient of $x^{n-k}$ in $\det(xI - A)$ is, up to sign, a sum of $\binom{n}{k}$ principal minors of order $k$, so its absolute value is at most $\binom{n}{k} k^{k/2} B^k$. This bounds the primes needed for a modular [characteristic polynomial](/characteristic-polynomial-computation/).
- **Lattices.** For a basis $b_1, \dots, b_n$ of a full-rank lattice $L$, the [determinant of the lattice](/lattice-determinant/) satisfies $\det L = \prod_i \|b_i^*\| \le \prod_i \|b_i\|$, with the Gram-Schmidt vectors $b_i^*$. The ratio $\prod_i \|b_i\| / \det L \ge 1$ is the orthogonality defect, which [LLL reduction](/lll-algorithm/) makes small.
- **Positive semidefinite form.** For a positive semidefinite matrix $G$, $\det G \le \prod_i g_{ii}$. Apply this to the Gram matrix $G = A \overline{A}^T$, whose diagonal entries are $\|a_i\|^2$, to get the theorem again.

## Tightness

The inequality is sharp for each $n$: an orthogonal matrix, or a diagonal one, reaches equality. The corollary $n^{n/2} B^n$ is sharp exactly when there is a matrix with entries $\pm B$ and orthogonal rows, that is, a *Hadamard matrix* of order $n$ scaled by $B$. Sylvester's doubling $H_{2m} = \begin{pmatrix} H_m & H_m \\ H_m & -H_m \end{pmatrix}$, starting from $H_1 = (1)$, gives them for every power of $2$. For example $H_4$, with rows $(1, 1, 1, 1)$, $(1, -1, 1, -1)$, $(1, 1, -1, -1)$, $(1, -1, -1, 1)$, has $\det H_4 = 16 = 4^{4/2}$.

A Hadamard matrix of order $n > 2$ exists only when $4$ divides $n$, and the Hadamard conjecture says it exists for every multiple of $4$. For other orders the corollary is not attained. For $n = 3$, the largest determinant of a matrix with entries $\pm 1$ is $4$, a value found by a search over all $2^9$ matrices, while the bound is $3^{3/2} \approx 5.196$.

For random integer matrices, the determinant is usually much smaller than the bound, but only by a factor that is exponential in $n$ with a small base, so the bit length $n(b + \tfrac12 \log_2 n)$ is the right order. Modular codes that use the bound are therefore not wasteful by more than a constant factor in the number of primes; early termination codes save that factor in practice, at the price of a probabilistic answer.

## History

Jacques Hadamard proved the inequality and the case of equality in 1893, in a short note that answered a question about the largest determinant of a matrix with bounded entries. Matrices with entries $\pm 1$ and orthogonal rows had appeared earlier, in James Joseph Sylvester's 1867 paper, which gave the doubling construction. The matrices that attain the bound are now called Hadamard matrices. In computer algebra, modular algorithms use it because they need a bound on the size of the result before the computation starts.

## References
