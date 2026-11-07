---
tag: XKZYKR
kind: theorem
slug: weyls-inequality
name: Weyl's inequality
aliases:
- Weyl's perturbation theorem
- Weyl's inequalities for eigenvalues
- Weyl's monotonicity theorem
area: numerical/eigenproblems
level: advanced
summary: For Hermitian A and B, λ_(i+j-1)(A + B) ≤ λ_i(A) + λ_j(B). So no eigenvalue of a Hermitian matrix moves by more than the 2-norm of a Hermitian perturbation.
prereqs: [spectral-theorem, rayleigh-quotient]
see_also: [courant-fischer-theorem, cauchy-interlacing-theorem, hoffman-wielandt-theorem, bauer-fike-theorem, davis-kahan-theorem, symmetric-eigenproblem, singular-value-decomposition, eigenvalue-condition-number]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 4.3, Eigenvalue inequalities for Hermitian matrices (Weyl's inequalities and their corollaries)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.1.2, Eigenvalue Sensitivity (the perturbation bound for symmetric matrices), and Section 2.4 for the singular value version
  - book: isbn:9780387948461
    title: Rajendra Bhatia, Matrix Analysis, Graduate Texts in Mathematics 169, Springer, 1997
    locator: Chapter III, Variational Principles for Eigenvalues (Weyl's inequalities, Lidskii's theorem and the Horn problem)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 10, Approximations from a Subspace (the minmax characterizations and Weyl's monotonicity theorem)
  - paper: "Hermann Weyl, Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen, Mathematische Annalen 71, 1912"
    title: Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen (mit einer Anwendung auf die Theorie der Hohlraumstrahlung)
    locator: Math. Ann. 71 (1912), pp. 441 to 479
  - paper: "William Fulton, Eigenvalues, invariant factors, highest weights, and Schubert calculus, Bulletin of the American Mathematical Society 37, 2000"
    title: Eigenvalues, invariant factors, highest weights, and Schubert calculus
    locator: Bull. Amer. Math. Soc. 37(3) (2000), pp. 209 to 249
---

Weyl's inequality compares the eigenvalues of a sum of two Hermitian matrices with the eigenvalues of the summands. With all eigenvalues in decreasing order, it says $\lambda_{i+j-1}(A + B) \le \lambda_i(A) + \lambda_j(B)$. The case $j = 1$, together with the same bound for $-A$ and $-B$, gives the perturbation theorem used throughout numerical linear algebra: if $A$ and $E$ are Hermitian, then $|\lambda_i(A + E) - \lambda_i(A)| \le \|E\|_2$ for every $i$. So the eigenvalues of a Hermitian matrix are perfectly conditioned in the absolute sense, and a backward stable algorithm for the [symmetric eigenproblem](/symmetric-eigenproblem/) computes every eigenvalue with an absolute error of order $u\|A\|_2$. The bound fails for nonnormal matrices, where the [Bauer-Fike theorem](/bauer-fike-theorem/) and pseudospectra take its place.

## Statement

**Notation.** For a Hermitian $M \in \mathbb C^{n \times n}$, $\lambda_1(M) \ge \lambda_2(M) \ge \dots \ge \lambda_n(M)$ are its eigenvalues, repeated by multiplicity. $\|E\|_2$ is the spectral norm, and for Hermitian $E$ it equals $\max(|\lambda_1(E)|, |\lambda_n(E)|)$.

**Theorem (Weyl 1912).** Let $A$ and $B$ be Hermitian of order $n$. Then

$$\lambda_{i+j-1}(A + B) \le \lambda_i(A) + \lambda_j(B) \qquad \text{whenever } 1 \le i, j \text{ and } i + j - 1 \le n,$$

$$\lambda_{i+j-n}(A + B) \ge \lambda_i(A) + \lambda_j(B) \qquad \text{whenever } i, j \le n \text{ and } i + j - n \ge 1.$$

**Corollary 1 (the perturbation bound).** For Hermitian $A$ and $E$ and every $i$,

$$\lambda_i(A) + \lambda_n(E) \le \lambda_i(A + E) \le \lambda_i(A) + \lambda_1(E), \qquad \text{so} \qquad |\lambda_i(A + E) - \lambda_i(A)| \le \|E\|_2.$$

**Corollary 2 (monotonicity).** If $E$ is Hermitian positive semidefinite, then $\lambda_i(A + E) \ge \lambda_i(A)$ for every $i$. If moreover $E$ has rank one, then $\lambda_{i+1}(A + E) \le \lambda_i(A)$ for $i = 1, \dots, n - 1$, so the eigenvalues of $A$ and $A + E$ interlace.

## In plain words

When two symmetric tables are added, each answer of the sum is limited by the answers of the parts: roughly, the sum cannot have more large answers than the parts supply between them. The most used form is about small changes. If a symmetric table is changed by a symmetric table whose largest effect on any arrow is some small amount, then no answer moves by more than that amount. This holds for every symmetric table, with no special conditions, which is why symmetric problems are so reliable to compute.

## Proof

*Fact used.* By the [spectral theorem](/spectral-theorem/), a Hermitian $M$ has orthonormal eigenvectors $m_1, \dots, m_n$ with $M m_k = \lambda_k(M) m_k$. If $x \in \operatorname{span}\{m_k, \dots, m_n\}$, then $x = \sum_{l \ge k} c_l m_l$ and $x^* M x = \sum_{l \ge k} \lambda_l(M)|c_l|^2 \le \lambda_k(M)\|x\|_2^2$. If $x \in \operatorname{span}\{m_1, \dots, m_k\}$, then in the same way $x^* M x \ge \lambda_k(M)\|x\|_2^2$.

*First inequality.* Let $a_k$, $b_k$ and $c_k$ be orthonormal eigenvectors of $A$, $B$ and $A + B$, and consider the subspaces

$$S_1 = \operatorname{span}\{a_i, \dots, a_n\}, \quad S_2 = \operatorname{span}\{b_j, \dots, b_n\}, \quad S_3 = \operatorname{span}\{c_1, \dots, c_{i+j-1}\},$$

of dimensions $n - i + 1$, $n - j + 1$ and $i + j - 1$. For subspaces of $\mathbb C^n$, $\dim(S \cap S') \ge \dim S + \dim S' - n$. So $\dim(S_1 \cap S_2) \ge n - i - j + 2$, and then $\dim(S_1 \cap S_2 \cap S_3) \ge (n - i - j + 2) + (i + j - 1) - n = 1$. Take a unit vector $x$ in the intersection. By the fact above, applied three times,

$$\lambda_{i+j-1}(A + B) \le x^*(A + B) x = x^* A x + x^* B x \le \lambda_i(A) + \lambda_j(B).$$

*Second inequality.* The eigenvalues of $-M$ in decreasing order are $\lambda_k(-M) = -\lambda_{n-k+1}(M)$. Let $i, j \le n$ with $i + j - n \ge 1$, and put $i' = n - i + 1$ and $j' = n - j + 1$, so $i', j' \ge 1$ and $i' + j' - 1 = 2n + 1 - i - j \le n$. The first inequality for $-A$ and $-B$ with indices $i'$ and $j'$ reads $-\lambda_{n - (i'+j'-1) + 1}(A + B) \le -\lambda_i(A) - \lambda_j(B)$, and $n - (i' + j' - 1) + 1 = i + j - n$. Multiplying by $-1$ gives the claim.

*Corollary 1.* The first inequality with $B = E$ and $j = 1$ gives $\lambda_i(A + E) \le \lambda_i(A) + \lambda_1(E)$. The second with $j = n$ gives $\lambda_i(A + E) \ge \lambda_i(A) + \lambda_n(E)$. Both $|\lambda_1(E)|$ and $|\lambda_n(E)|$ are at most $\|E\|_2$.

*Corollary 2.* If $E$ is positive semidefinite, $\lambda_n(E) \ge 0$, and Corollary 1 gives $\lambda_i(A + E) \ge \lambda_i(A)$. If $E$ has rank one, $\lambda_2(E) = 0$, and the first inequality with the roles $A \to A$, $B \to E$, $j = 2$ gives $\lambda_{i+1}(A + E) \le \lambda_i(A) + \lambda_2(E) = \lambda_i(A)$. $\blacksquare$

## Consequences

- **Absolute accuracy of symmetric eigensolvers.** A backward stable method returns the exact eigenvalues of $A + E$ with $E$ Hermitian and $\|E\|_2 \le c(n) u \|A\|_2$, so each computed eigenvalue has an error of at most $c(n) u \|A\|_2$. For $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ and $E = \operatorname{diag}(0.1, -0.1)$ the eigenvalues move from $3$ and $1$ to $3.004988$ and $0.995012$, by $0.004988 \le 0.1$. The motion is much smaller than the bound because $E$ mostly acts across the gap; that second-order effect is quantified by the [Davis-Kahan theorem](/davis-kahan-theorem/) and the residual bounds of the [Rayleigh quotient](/rayleigh-quotient/).
- **Singular values.** Applying Corollary 1 to the Hermitian matrices $\begin{pmatrix} 0 & A \\ A^* & 0 \end{pmatrix}$, whose eigenvalues are $\pm\sigma_i(A)$ and zeros, gives $|\sigma_i(A + E) - \sigma_i(A)| \le \|E\|_2$ for every matrix $A$ and $E$ of the same shape ([singular value decomposition](/singular-value-decomposition/)).
- **Residual bound.** If $\|x\|_2 = 1$, $\rho = x^* A x$ and $r = A x - \rho x$, then $E = -(r x^* + x r^*)$ is Hermitian with $\|E\|_2 = \|r\|_2$ and $(A + E) x = \rho x$, so some eigenvalue of $A$ is within $\|r\|_2$ of $\rho$.
- **Interlacing.** Corollary 2 is the rank-one form of [Cauchy interlacing](/cauchy-interlacing-theorem/), and it is the reason the [secular equation](/secular-equation/) of a diagonal plus rank-one matrix has one root in each gap.
- **Stronger forms.** The [Hoffman-Wielandt theorem](/hoffman-wielandt-theorem/) bounds all eigenvalue changes together in the Frobenius norm, and Lidskii's theorem says that the vector $\lambda(A + E) - \lambda(A)$ lies in the convex hull of the permutations of $\lambda(E)$.
- **The [Courant-Fischer theorem](/courant-fischer-theorem/)** gives another proof, and the dimension count above is the same one that proves it.

## Tightness

- **Corollary 1 is attained.** For $E = \epsilon I$, every eigenvalue moves by exactly $\epsilon = \|E\|_2$.
- **The index inequality is attained.** For $A = \operatorname{diag}(3, 1)$ and $B = \operatorname{diag}(0, 2)$, $A + B = 3I$ and $\lambda_2(A + B) = 3 = \lambda_2(A) + \lambda_1(B)$, the case $i = 2$, $j = 1$.
- **Hermitian $A$ and $E$ are both needed.** For the nonnormal $A = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$ and $E = \begin{pmatrix} 0 & 0 \\ \epsilon & 0 \end{pmatrix}$, the eigenvalues move from $0$ to $\pm\sqrt\epsilon$, which is $10^{-4}$ for $\epsilon = 10^{-8}$, far more than $\|E\|_2 = \epsilon$.
- **The full answer is Horn's problem.** The set of all possible spectra of $A + B$ for given spectra of $A$ and $B$ is described by a finite list of linear inequalities conjectured by Alfred Horn in 1962 and proved through the work of Klyachko (1998) and Knutson and Tao (1999); Weyl's inequalities are among them, but not all of them (Fulton 2000).

## History

Hermann Weyl proved the inequalities in 1912, in his paper on the asymptotic distribution of the eigenvalues of differential operators, where he used them to compare the eigenvalues of a sum of operators with those of the parts. The min-max approach of Fischer (1905) and Courant (1920) gives the same results. Ky Fan (1949) and Lidskii (1950) extended them to sums of eigenvalues, and Horn's 1962 conjecture on the complete set of inequalities was proved in 1998 and 1999. In numerical analysis the corollary became the standard statement that symmetric eigenvalues are well conditioned, through Wilkinson's 1965 book.

## References
