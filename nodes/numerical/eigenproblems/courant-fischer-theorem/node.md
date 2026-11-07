---
tag: Z98CZ2
kind: theorem
slug: courant-fischer-theorem
name: Courant-Fischer theorem
aliases:
- min-max principle
- Courant-Fischer-Weyl theorem
- minimax characterization of eigenvalues
area: numerical/eigenproblems
level: advanced
summary: The k-th largest eigenvalue of a Hermitian matrix is the max over k-dimensional subspaces of the min of the Rayleigh quotient on them, and also a min-max over dimension n − k + 1.
prereqs: [rayleigh-quotient, spectral-theorem]
see_also: [weyls-inequality, cauchy-interlacing-theorem, rayleigh-ritz-method, hoffman-wielandt-theorem, singular-value-decomposition, lanczos-algorithm, positive-definite-matrix, generalized-eigenvalue-problem]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 4.2, Variational characterizations of eigenvalues of Hermitian matrices (the Rayleigh quotient theorem and the Courant-Fischer theorem), and Section 4.3 on Weyl's inequalities and interlacing
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.1.1, Eigenvalue Properties (the Courant-Fischer minimax theorem and its corollaries)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 10, Approximations from a Subspace (the minmax characterizations and their use for Rayleigh-Ritz approximations)
  - book: isbn:9780387948461
    title: Rajendra Bhatia, Matrix Analysis, Graduate Texts in Mathematics 169, Springer, 1997
    locator: Chapter III, Variational Principles for Eigenvalues (Section III.1)
  - paper: "E. Fischer, Über quadratische Formen mit reellen Koeffizienten, Monatshefte für Mathematik und Physik 16, 1905, pp. 234 to 249"
    title: E. Fischer, Über quadratische Formen mit reellen Koeffizienten
    locator: the min-max characterization for real quadratic forms
  - paper: "R. Courant, Über die Eigenwerte bei den Differentialgleichungen der mathematischen Physik, Mathematische Zeitschrift 7, 1920, pp. 1 to 57"
    title: R. Courant, Über die Eigenwerte bei den Differentialgleichungen der mathematischen Physik
    locator: the max-min principle for differential operators
---

The Courant-Fischer theorem characterizes each eigenvalue of a Hermitian matrix by an optimization over subspaces, with no reference to eigenvectors. The $k$-th largest eigenvalue $\lambda_k$ is the largest value that the minimum of the [Rayleigh quotient](/rayleigh-quotient/) $\rho(x) = x^* A x / x^* x$ can take on a $k$-dimensional subspace. It is also the smallest value that the maximum of $\rho$ can take on a subspace of dimension $n - k + 1$. From it follow [Weyl's inequality](/weyls-inequality/), the [Cauchy interlacing theorem](/cauchy-interlacing-theorem/), the optimality of the [Rayleigh-Ritz method](/rayleigh-ritz-method/), and the perfect conditioning of Hermitian eigenvalues.

## Statement

Let $A \in \mathbb{C}^{n \times n}$ be Hermitian with eigenvalues $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n$, and let $\rho(x) = x^* A x / x^* x$ for $x \ne 0$. Then for $k = 1, \dots, n$
$$\lambda_k = \max_{\dim S = k} \ \min_{0 \ne x \in S} \rho(x) = \min_{\dim S = n - k + 1} \ \max_{0 \ne x \in S} \rho(x),$$
where $S$ ranges over the subspaces of $\mathbb{C}^n$ of the given dimension. If $v_1, \dots, v_n$ are orthonormal eigenvectors with $A v_i = \lambda_i v_i$, the outer maximum is attained at $S = \operatorname{span}\{v_1, \dots, v_k\}$, and the outer minimum at $S = \operatorname{span}\{v_k, \dots, v_n\}$. For $k = 1$ and $k = n$ the theorem gives $\lambda_1 = \max_x \rho(x)$ and $\lambda_n = \min_x \rho(x)$ (the Rayleigh principle).

## In plain words

For a symmetric matrix, the value $\rho(x)$ measures how much the matrix stretches the vector $x$ along itself. The largest eigenvalue is the most stretch that any direction gets. The second largest eigenvalue is harder to describe directly, but this theorem does it. Pick a plane of vectors. Some vector in it gets the least stretch. Now choose the plane so that this least stretch is as large as possible. The answer is the second eigenvalue. The same idea with $k$ dimensions gives the $k$-th eigenvalue.

The theorem lets you prove facts about eigenvalues without knowing the eigenvectors. For example, if a symmetric change of the matrix is small, each eigenvalue moves by at most the size of the change.

## Proof

Expand $x = \sum_i c_i v_i$ in the orthonormal eigenvectors given by the [spectral theorem](/spectral-theorem/). Then
$$\rho(x) = \frac{\sum_i \lambda_i |c_i|^2}{\sum_i |c_i|^2},$$
a weighted average of the eigenvalues with weights $|c_i|^2$.

**Max-min, the upper bound.** Let $S$ have dimension $k$, and let $W = \operatorname{span}\{v_k, \dots, v_n\}$, of dimension $n - k + 1$. Since $\dim S + \dim W = n + 1 > n$, the intersection $S \cap W$ contains some $x \ne 0$. This $x$ has $c_i = 0$ for $i < k$, so $\rho(x)$ is an average of $\lambda_k, \dots, \lambda_n$, and $\rho(x) \le \lambda_k$. Hence $\min_{0 \ne x \in S} \rho(x) \le \lambda_k$ for every $S$ of dimension $k$.

**Max-min, attainment.** For $S = \operatorname{span}\{v_1, \dots, v_k\}$, every $x \in S$ is an average of $\lambda_1, \dots, \lambda_k$, so $\rho(x) \ge \lambda_k$, with equality at $x = v_k$. So the minimum over this $S$ is $\lambda_k$, and the maximum over all $S$ equals $\lambda_k$.

**Min-max.** Apply the max-min form to $-A$, whose eigenvalues in decreasing order are $-\lambda_n \ge \dots \ge -\lambda_1$; its $(n - k + 1)$-th largest eigenvalue is $-\lambda_k$, and $\rho_{-A} = -\rho_A$. So
$$-\lambda_k = \max_{\dim S = n-k+1} \min_{x \in S} (-\rho(x)) = -\min_{\dim S = n-k+1} \max_{x \in S} \rho(x),$$
with the minimum attained at $S = \operatorname{span}\{v_k, \dots, v_n\}$. $\blacksquare$

## Consequences

- **Weyl's inequality.** For Hermitian $A$ and $E$, $\lambda_k(A) + \lambda_n(E) \le \lambda_k(A + E) \le \lambda_k(A) + \lambda_1(E)$, so $|\lambda_k(A + E) - \lambda_k(A)| \le \|E\|_2$. *Proof:* $\rho_{A+E}(x) = \rho_A(x) + \rho_E(x)$ and $\lambda_n(E) \le \rho_E(x) \le \lambda_1(E)$; take the max-min of both sides. So the eigenvalues of a Hermitian matrix are perfectly conditioned in the absolute sense: the condition number of each is 1 ([eigenvalue condition number](/eigenvalue-condition-number/)). The general form $\lambda_{i+j-1}(A + B) \le \lambda_i(A) + \lambda_j(B)$ follows from the same dimension count.
- **Monotonicity.** If $B - A$ is positive semidefinite, then $\lambda_k(A) \le \lambda_k(B)$ for every $k$, since $\rho_A \le \rho_B$ pointwise.
- **Cauchy interlacing.** If $B = U^* A U$ with $U \in \mathbb{C}^{n \times m}$ having orthonormal columns, then $\lambda_k(A) \ge \lambda_k(B) \ge \lambda_{k + n - m}(A)$. *Proof of the left inequality:* the subspaces $U T$ with $\dim T = k$ form a subset of all $k$-dimensional subspaces of $\mathbb{C}^n$, and $\rho_B(y) = \rho_A(U y)$; a maximum over fewer subspaces is not larger. The right inequality follows from the min-max form in the same way. For a principal submatrix of order $n - 1$ this is the [Cauchy interlacing theorem](/cauchy-interlacing-theorem/).
- **Rayleigh-Ritz bounds.** The Ritz values $\theta_1 \ge \dots \ge \theta_m$ of $A$ on any $m$-dimensional subspace satisfy $\theta_k \le \lambda_k$ and $\theta_{m-j} \ge \lambda_{n-j}$, by the interlacing above. So the largest Ritz values of the [Lanczos algorithm](/lanczos-algorithm/) increase toward the top eigenvalues and never overshoot.
- **Singular values.** Applied to $A^* A$, $\sigma_k(A) = \max_{\dim S = k} \min_{0 \ne x \in S} \|A x\|_2 / \|x\|_2$, so $|\sigma_k(A + E) - \sigma_k(A)| \le \|E\|_2$ for every matrix, square or not ([singular value decomposition](/singular-value-decomposition/)).
- **Definite pencils.** For Hermitian $A$ and positive definite $B$, the eigenvalues of $A x = \lambda B x$ satisfy the same theorem with $\rho(x) = x^* A x / x^* B x$ ([generalized eigenvalue problem](/generalized-eigenvalue-problem/)).
- **Differential operators.** For self-adjoint operators bounded below with compact resolvent, such as the Dirichlet Laplacian on a bounded domain, the same max-min formula over subspaces of the form domain characterizes the eigenvalues. This is how Courant proved monotonicity under domain inclusion, and how Weyl's asymptotic law can be obtained.

## Tightness

- **Attainment needs the right subspace.** For $A = \operatorname{tridiag}(-1, 2, -1)$ of order 3, with eigenvalues $2 + \sqrt{2}$, 2 and $2 - \sqrt{2}$, the subspace $S = \operatorname{span}\{e_1, e_3\}$ gives $\rho(a e_1 + c e_3) = (2a^2 + 2c^2)/(a^2 + c^2) = 2$ for every nonzero $(a, c)$. So it attains $\lambda_2 = 2$ in both the max-min and the min-max form, although it is not spanned by eigenvectors. For $S = \operatorname{span}\{e_1, e_2\}$, the minimum of $\rho$ on $S$ is the smallest eigenvalue of $\begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}$, which is $1 < \lambda_2$.
- **Weyl's bound is attained.** For $E = \varepsilon I$ every eigenvalue moves by exactly $\varepsilon = \|E\|_2$.
- **Hermitian is needed.** For $A = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$, both eigenvalues are 0, but $\rho(x) = \bar x_1 x_2 / \|x\|_2^2$ takes every value in the disc $|z| \le 1/2$ (the numerical range of $A$). So no ordering of eigenvalues is characterized by $\rho$. For non-normal matrices the eigenvalues can also move much more than $\|E\|_2$ (see the [Bauer-Fike theorem](/bauer-fike-theorem/)).
- **The dimensions are sharp.** With $\dim S = k + 1$ instead of $k$ in the max-min form one gets $\lambda_{k+1}$, which can be smaller than $\lambda_k$. With $\dim S = k - 1$ the max-min is $\lambda_{k-1} \ge \lambda_k$.

## History

Ernst Fischer proved the min-max characterization for real quadratic forms in 1905. Earlier, Poincaré (1890) had used extremal properties of quadratic forms for the eigenvalues of vibrating systems. Hermann Weyl (1912) used the same principle to prove his inequalities for the eigenvalues of sums of operators, in his work on the asymptotic distribution of the eigenvalues of the Laplacian. Richard Courant (1920) stated the max-min form for differential operators, which does not need the earlier eigenfunctions. He made it a standard tool in the book of Courant and Hilbert, Methods of Mathematical Physics. Hence the names Courant-Fischer and Courant-Fischer-Weyl.

## References
