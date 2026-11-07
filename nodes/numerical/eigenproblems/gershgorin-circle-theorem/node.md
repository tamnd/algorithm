---
tag: 38MH00
kind: theorem
slug: gershgorin-circle-theorem
name: Gershgorin circle theorem
aliases:
- Gershgorin discs
- Gerschgorin circle theorem
- Geršgorin disc theorem
area: numerical/eigenproblems
level: intro
summary: Every eigenvalue of A lies in the union of the discs with centre a_ii and radius the sum of the other absolute values in row i. A union of k discs apart from the rest holds exactly k eigenvalues.
prereqs: [eigenvalue, eigenvector]
see_also: [diagonally-dominant-matrix, bauer-fike-theorem, bisection-eigenvalue-algorithm, spectral-radius, matrix-norms, eigenvalue-condition-number]
sources:
  - book: isbn:9783540211006
    title: Richard S. Varga, Geršgorin and His Circles, Springer Series in Computational Mathematics 36, Springer, 2004
    locator: Chapter 1, Basic Theory (Theorem 1.1, the disc theorem, and the result on disjoint unions of discs)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 6.1, Geršgorin discs (and Appendix D on the continuity of the roots of a polynomial)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.2, Perturbation Theory (the Gershgorin theorem and its use with diagonal scaling)
  - paper: "S. Gerschgorin, Über die Abgrenzung der Eigenwerte einer Matrix, Izvestiya Akademii Nauk SSSR, 1931"
    title: S. Gerschgorin, Über die Abgrenzung der Eigenwerte einer Matrix
    locator: pp. 749 to 754 (the original statement)
---

The Gershgorin circle theorem locates the [eigenvalues](/eigenvalue/) of a square matrix from its entries alone: each eigenvalue lies in a disc centred at a diagonal entry $a_{ii}$, with radius the sum of the absolute values of the other entries of row $i$. A stronger part counts: a union of $k$ discs that is disjoint from the other discs holds exactly $k$ eigenvalues. It costs $O(n^2)$ operations and needs no factorization, so it gives starting intervals for [bisection](/bisection-eigenvalue-algorithm/), stopping tests for iterations that drive off-diagonal entries to zero, and the nonsingularity of [diagonally dominant](/diagonally-dominant-matrix/) matrices.

## Statement

Let $A = (a_{ij}) \in \mathbb{C}^{n \times n}$. For $i = 1, \dots, n$ let
$$R_i = \sum_{j \neq i} |a_{ij}|, \qquad D_i = \{ z \in \mathbb{C} : |z - a_{ii}| \le R_i \}.$$

**Theorem.**

1. Every eigenvalue of $A$ lies in $\bigcup_{i=1}^{n} D_i$.
2. The same holds with the column sums $C_j = \sum_{i \neq j} |a_{ij}|$ in place of the row sums, since $A^T$ has the same eigenvalues as $A$. So each eigenvalue lies in the intersection of the row union and the column union.
3. Let $S \subseteq \{1, \dots, n\}$ with $|S| = k$, and let $U = \bigcup_{i \in S} D_i$ and $W = \bigcup_{i \notin S} D_i$. If $U \cap W = \emptyset$, then $U$ contains exactly $k$ eigenvalues of $A$, counted with algebraic multiplicity.
4. For each nonsingular diagonal $D = \operatorname{diag}(d_1, \dots, d_n)$, parts 1 to 3 hold for $D^{-1} A D$, whose discs have centres $a_{ii}$ and radii $\sum_{j \neq i} |a_{ij}| \, |d_j| / |d_i|$.

## In plain words

Look at one row of the matrix. Its diagonal entry gives a centre point. The sizes of the other entries in that row, added up, give a radius. Draw this circle for every row. The theorem says that every eigenvalue is inside at least one of the circles.

If the other entries are small compared with the diagonal, the circles are small and the eigenvalues are close to the diagonal entries. If a group of circles does not touch the rest, that group holds exactly as many eigenvalues as it has circles. So a circle that stands alone holds exactly one eigenvalue.

## Proof

**Part 1.** Let $A v = \lambda v$ with $v \neq 0$. Choose $i$ with $|v_i| = \max_j |v_j|$; then $|v_i| > 0$. Row $i$ of $A v = \lambda v$ reads $\sum_j a_{ij} v_j = \lambda v_i$, so
$$(\lambda - a_{ii}) v_i = \sum_{j \neq i} a_{ij} v_j, \qquad |\lambda - a_{ii}| \le \sum_{j \neq i} |a_{ij}| \frac{|v_j|}{|v_i|} \le R_i .$$
So $\lambda \in D_i$. $\square$

**Part 2.** $\det(tI - A^T) = \det((tI - A)^T) = \det(tI - A)$, so $A^T$ and $A$ have the same eigenvalues, and part 1 for $A^T$ uses the column sums of $A$. $\square$

**Part 4.** $D^{-1} A D$ is similar to $A$, so it has the same eigenvalues with the same multiplicities, and its $(i, j)$ entry is $a_{ij} d_j / d_i$. $\square$

**Part 3.** Let $\Delta = \operatorname{diag}(a_{11}, \dots, a_{nn})$ and $A(t) = \Delta + t (A - \Delta)$ for $t \in [0, 1]$. The discs of $A(t)$ have the same centres and the radii $t R_i \le R_i$, so they lie inside the discs of $A$. By part 1, every eigenvalue of every $A(t)$ lies in $U \cup W$.

$U$ and $W$ are finite unions of closed discs, so they are compact. They are disjoint, so $d = \min\{|x - y| : x \in U, y \in W\} > 0$. Let $N(t)$ be the number of eigenvalues of $A(t)$ in $U$, with multiplicity.

The coefficients of $p_t(z) = \det(zI - A(t))$ are polynomials in $t$, so they are continuous. The roots of a monic polynomial depend continuously on its coefficients (Horn and Johnson, Appendix D): for $t_0 \in [0, 1]$ and $\varepsilon = d/2$, there is $\eta > 0$ such that for $|t - t_0| < \eta$ the roots of $p_t$ can be listed as $z_1(t), \dots, z_n(t)$ and those of $p_{t_0}$ as $z_1(t_0), \dots, z_n(t_0)$ with $|z_m(t) - z_m(t_0)| < \varepsilon$ for each $m$. Every root of both polynomials lies in $U \cup W$. Two points at distance less than $d$, one in $U \cup W$ and one in $U \cup W$, are in the same one of the two sets. So $z_m(t) \in U$ if and only if $z_m(t_0) \in U$, and $N(t) = N(t_0)$.

So $N$ is locally constant on the interval $[0, 1]$, which is connected, so $N$ is constant. At $t = 0$, $A(0) = \Delta$ has the eigenvalues $a_{11}, \dots, a_{nn}$. The centre $a_{ii}$ lies in $D_i$, so it lies in $U$ for $i \in S$ and in $W$ for $i \notin S$; as $U \cap W = \emptyset$, exactly $k$ of them are in $U$. Hence $N(1) = N(0) = k$. $\blacksquare$

## Consequences

- **Diagonal dominance.** If $|a_{ii}| > R_i$ for every $i$ (strict row diagonal dominance), then $0$ is in no disc, so $0$ is not an eigenvalue and $A$ is nonsingular. This is the Lévy-Desplanques theorem.
- **Definiteness.** If $A$ is Hermitian, has positive diagonal and is strictly diagonally dominant, then each eigenvalue is real and lies in some $[a_{ii} - R_i, a_{ii} + R_i] \subset (0, \infty)$, so $A$ is [positive definite](/positive-definite-matrix/).
- **Real eigenvalues.** If $A$ is real and a disc $D_i$ is disjoint from all the others, it holds exactly one eigenvalue $\lambda$. Its centre is real, so the disc is symmetric about the real axis, and $\bar\lambda$, also an eigenvalue, lies in it too. Hence $\bar\lambda = \lambda$ and $\lambda$ is real.
- **A norm bound.** $|\lambda| \le |a_{ii}| + R_i \le \max_i \sum_j |a_{ij}| = \|A\|_\infty$ for each eigenvalue, the bound on the [spectral radius](/spectral-radius/) by the [infinity norm](/matrix-norms/).
- **Starting intervals.** For a real symmetric tridiagonal matrix with diagonal $a_i$ and off-diagonal $b_i$, every eigenvalue lies in $[\min_i (a_i - |b_{i-1}| - |b_i|), \max_i (a_i + |b_{i-1}| + |b_i|)]$, the interval with which [bisection](/bisection-eigenvalue-algorithm/) starts.
- **Perturbation of a diagonal matrix.** If $A = \Delta + E$ with $\Delta$ diagonal, every eigenvalue is within $\max_i \sum_{j} |e_{ij}|$ of a diagonal entry. With scaling (part 4) one gets more. Suppose every off-diagonal entry has modulus at most $\varepsilon$ and $|a_{ii} - a_{jj}| \ge g > 0$ for all $j \ne i$. Take $d_i = 1$ and $d_j = \delta = 2\varepsilon/g$ for $j \neq i$. Then disc $i$ of $D^{-1} A D$ has radius at most $(n-1)\varepsilon\delta = 2(n-1)\varepsilon^2/g$, and each other disc has radius at most $\varepsilon/\delta + (n-2)\varepsilon = g/2 + (n-2)\varepsilon$. When $2(n-1)\varepsilon^2/g + (n-2)\varepsilon < g/2$, disc $i$ is disjoint from the others, so by part 3 exactly one eigenvalue lies within $2(n-1)\varepsilon^2/g$ of $a_{ii}$. So a well separated diagonal entry is correct to second order in the off-diagonal entries. This explains the fast final convergence of the eigenvalue estimates in the [Jacobi algorithm](/jacobi-eigenvalue-algorithm/) and the QR algorithm (Golub and Van Loan, Section 7.2).

## Tightness

- **Eigenvalues on the boundary.** $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ has the eigenvalues $\pm 1$ and the two discs $|z| \le 1$, so both eigenvalues lie on the boundary circle: the radius in part 1 cannot be made smaller in general.
- **A disc can be empty.** $A = \begin{pmatrix} 0 & 1 \\ 4 & 0 \end{pmatrix}$ has the eigenvalues $\pm 2$ and the discs $|z| \le 1$ and $|z| \le 4$. The first disc holds no eigenvalue. Part 3 does not apply, since the discs overlap. With $D = \operatorname{diag}(1, 2)$, $D^{-1} A D = \begin{pmatrix} 0 & 2 \\ 2 & 0 \end{pmatrix}$, whose two discs $|z| \le 2$ have both eigenvalues on their boundary.
- **Part 3 needs disjointness.** In the last example, the union of the single disc $|z| \le 1$ is not disjoint from the other disc, and indeed it does not hold one eigenvalue.
- **A worked example.** $A = \begin{pmatrix} 10 & 1 & 0.5 \\ 0.2 & 5 & 0.3 \\ 1 & 1 & -2 \end{pmatrix}$ has the row discs with centres 10, 5, $-2$ and radii 1.5, 0.5, 2. They meet the real axis in $[8.5, 11.5]$, $[4.5, 5.5]$ and $[-4, 0]$ and are pairwise disjoint, so each holds one eigenvalue, which is real. The column radii are 1.2, 2 and 0.8, so the third eigenvalue also lies in $[-2.8, -1.2]$. The eigenvalues are about 10.087608, 4.991671 and $-2.079278$, and their sum is $13 = \operatorname{tr} A$.

## History

Semyon Aranovich Gerschgorin published the theorem in 1931 in the Bulletin of the Academy of Sciences of the USSR, in German. Special cases were known before: the nonsingularity of strictly diagonally dominant matrices goes back to Lévy (1881) and Desplanques (1887), and Varga's book traces this history and the many later refinements, such as the ovals of Cassini of Brauer and the use of diagonal scaling (Varga, Chapter 1).

## References
