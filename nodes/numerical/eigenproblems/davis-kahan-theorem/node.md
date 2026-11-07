---
tag: 5549JD
kind: theorem
slug: davis-kahan-theorem
name: Davis-Kahan sin θ theorem
aliases:
- Davis-Kahan theorem
- sin theta theorem
- Davis-Kahan bound
area: numerical/eigenproblems
level: research
summary: For Hermitian A and A + E, the sines of the angles between corresponding invariant subspaces are at most the norm of the residual E X divided by the gap separating the spectra.
prereqs: [symmetric-eigenproblem, eigenvector, matrix-norms, weyls-inequality]
see_also: [sylvester-equation, rayleigh-ritz-method, eigenvalue-condition-number, hoffman-wielandt-theorem, courant-fischer-theorem, principal-component-analysis, spectral-clustering, inverse-iteration]
sources:
  - paper: doi:10.1137/0707001
    title: Chandler Davis and W. M. Kahan, The rotation of eigenvectors by a perturbation. III, SIAM Journal on Numerical Analysis 7, 1970
    locator: pp. 1 to 46 (the sin θ, tan θ, sin 2θ and tan 2θ theorems; Section 6 for sin θ)
  - book: isbn:9780126702309
    title: G. W. Stewart and Ji-guang Sun, Matrix Perturbation Theory, Academic Press, 1990
    locator: Chapter I, Section 5 (canonical angles between subspaces) and Chapter V, Section 3 (the Davis-Kahan theorems for Hermitian matrices)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics, 1998
    locator: Chapter 11, Approximations from a Subspace (residual bounds for invariant subspaces, the sin θ theorem)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.1.3, Eigenvector and Invariant Subspace Perturbation (the gap-dependent bound for symmetric matrices) and Section 6.4.3 (subspace angles)
  - paper: doi:10.1093/biomet/asv008
    title: Y. Yu, T. Wang and R. J. Samworth, A useful variant of the Davis-Kahan theorem for statisticians, Biometrika 102, 2015
    locator: pp. 315 to 323 (Theorem 1, a bound in terms of the eigengap of the unperturbed matrix)
  - paper: "R. Bhatia, C. Davis and A. McIntosh, Perturbation of spectral subspaces and solution of linear operator equations, Linear Algebra and its Applications 52/53, 1983, pp. 45 to 67"
    title: R. Bhatia, C. Davis and A. McIntosh, Perturbation of spectral subspaces and solution of linear operator equations
    locator: the Sylvester equation bound with the constant π/2 for spectra that are separated but not by an interval
---

The Davis-Kahan sin θ theorem bounds how far an invariant subspace of a Hermitian matrix turns under a perturbation. If $X$ spans an invariant subspace of $A$ and $\tilde X$ spans the matching invariant subspace of $A + E$, the canonical angles $\Theta$ between them satisfy $\|\sin \Theta\| \le \|E X\| / \delta$. Here $\delta$ is the distance between the eigenvalues of $A$ on $X$ and the other eigenvalues of $A + E$, and the inequality holds in the Frobenius norm and, when the eigenvalues of $A$ on $X$ lie in an interval that the others avoid, in every unitarily invariant norm. In contrast to eigenvalues, which move by at most $\|E\|_2$ by [Weyl's inequality](/weyls-inequality/), eigenvectors can move a lot when the gap is small. The theorem says that the gap is the only thing that matters. The same proof gives a residual bound for computed subspaces, which is how eigensolvers certify Ritz vectors.

## Statement

**Notation.** $A$ and $\tilde A = A + E$ are Hermitian $n \times n$. For $X, \tilde X \in \mathbb{C}^{n \times k}$ with orthonormal columns, the canonical angles $0 \le \theta_1 \le \dots \le \theta_k \le \pi/2$ between their ranges are defined by $\cos \theta_i = \sigma_i(X^* \tilde X)$. With $\tilde X_\perp$ an orthonormal basis of the orthogonal complement of the range of $\tilde X$, the singular values of $\tilde X_\perp^* X$ are $\sin \theta_1, \dots, \sin \theta_k$ (together with zeros), and $\sin \Theta = \operatorname{diag}(\sin \theta_i)$. $\|\cdot\|$ denotes a unitarily invariant norm, such as the spectral norm $\|\cdot\|_2$ or the Frobenius norm $\|\cdot\|_F$.

Let $A X = X \Lambda_1$ with $X^* X = I_k$ and $\Lambda_1$ Hermitian $k \times k$ (diagonal, if one likes), so the range of $X$ is invariant under $A$. Let $\tilde A = [\tilde X, \tilde X_\perp] \operatorname{diag}(\tilde \Lambda_1, \tilde \Lambda_2) [\tilde X, \tilde X_\perp]^*$ be a spectral splitting of $\tilde A$ with $\tilde X \in \mathbb{C}^{n \times k}$.

1. **Frobenius form.** If $\delta = \min \{ |\mu - \lambda| : \mu \in \operatorname{spec}(\tilde \Lambda_2), \lambda \in \operatorname{spec}(\Lambda_1) \} > 0$, then
$$\|\sin \Theta(X, \tilde X)\|_F \le \frac{\|\tilde X_\perp^* E X\|_F}{\delta} \le \frac{\|E X\|_F}{\delta}.$$
2. **Sin θ theorem (Davis and Kahan 1970).** If the spectrum of $\Lambda_1$ lies in an interval $[a, b]$ and the spectrum of $\tilde \Lambda_2$ lies outside $(a - \delta, b + \delta)$ with $\delta > 0$, or the spectrum of $\tilde \Lambda_2$ lies in $[a, b]$ and that of $\Lambda_1$ outside $(a - \delta, b + \delta)$, then for every unitarily invariant norm
$$\|\sin \Theta(X, \tilde X)\| \le \frac{\|\tilde X_\perp^* E X\|}{\delta} \le \frac{\|E X\|}{\delta}.$$
3. **Residual form.** Let $X$ have orthonormal columns, but not necessarily span an invariant subspace, let $M$ be Hermitian $k \times k$, and let $R = A X - X M$. If $A = [Y, Y_\perp] \operatorname{diag}(\Lambda_1, \Lambda_2) [Y, Y_\perp]^*$ and the separation hypotheses of item 1 or 2 hold between the spectra of $M$ and $\Lambda_2$, then $\|\sin \Theta(X, Y)\| \le \|R\| / \delta$ in the corresponding norms.
4. **Gap of the unperturbed matrix.** Let $\lambda_1 \ge \dots \ge \lambda_n$ be the eigenvalues of $A$ and $\tilde \lambda_1 \ge \dots \ge \tilde \lambda_n$ those of $\tilde A$. Let $X$ and $\tilde X$ be eigenvectors for the indices $r, r + 1, \dots, s$, and $\delta_0 = \min(\lambda_{r-1} - \lambda_r, \lambda_s - \lambda_{s+1})$, with $\lambda_0 = +\infty$ and $\lambda_{n+1} = -\infty$. If $\|E\|_2 < \delta_0$, then $\|\sin \Theta(X, \tilde X)\| \le \|E X\| / (\delta_0 - \|E\|_2)$ for every unitarily invariant norm.

## In plain words

When you change a symmetric matrix a little, its eigenvalues change by at most the size of the change. Its eigenvectors are different: they can swing far if two eigenvalues are close, because then the matrix barely cares which direction in their plane is an eigenvector.

The theorem gives the exact price. The turn of a group of eigenvectors is at most the size of the change divided by the distance from their eigenvalues to all the others. A group of eigenvectors that is well separated from the rest is stable even if the eigenvalues inside the group are close together. That is why algorithms and statistics often work with whole groups of eigenvectors rather than single ones.

## Proof

**Step 1 (the Sylvester equation).** From $\tilde A \tilde X_\perp = \tilde X_\perp \tilde \Lambda_2$ and Hermitian symmetry, $\tilde X_\perp^* \tilde A = \tilde \Lambda_2 \tilde X_\perp^*$. Multiply $\tilde A X = A X + E X = X \Lambda_1 + E X$ on the left by $\tilde X_\perp^*$:
$$\tilde \Lambda_2 S - S \Lambda_1 = \tilde X_\perp^* E X, \qquad S = \tilde X_\perp^* X.$$
The nonzero singular values of $S$ are the $\sin \theta_i$, so $\|S\| = \|\sin \Theta\|$ for every unitarily invariant norm. Since $\|\tilde X_\perp^*\|_2 = 1$, $\|\tilde X_\perp^* E X\| \le \|E X\|$, which gives the second inequality in items 1 and 2. It remains to bound $S$ from the [Sylvester equation](/sylvester-equation/) $\tilde \Lambda_2 S - S \Lambda_1 = R'$ with $R' = \tilde X_\perp^* E X$.

**Step 2 (Frobenius norm).** Diagonalize: $\tilde \Lambda_2 = P \operatorname{diag}(\mu_i) P^*$ and $\Lambda_1 = W \operatorname{diag}(\lambda_j) W^*$ with $P$, $W$ unitary. For $\hat S = P^* S W$ and $\hat R = P^* R' W$, the equation reads $(\mu_i - \lambda_j) \hat s_{ij} = \hat r_{ij}$, so $|\hat s_{ij}| \le |\hat r_{ij}| / \delta$. Summing squares, $\|S\|_F = \|\hat S\|_F \le \|\hat R\|_F / \delta = \|R'\|_F / \delta$.

**Step 3 (interval separation, any unitarily invariant norm).** Suppose the spectrum of $\Lambda_1$ is in $[a, b]$ and that of $\tilde \Lambda_2$ avoids $(a - \delta, b + \delta)$. Put $c = (a + b)/2$ and $r = (b - a)/2$. Then $\|\Lambda_1 - c I\|_2 \le r$, and every eigenvalue of $\tilde \Lambda_2 - c I$ has modulus at least $r + \delta$, so $\|(\tilde \Lambda_2 - c I)^{-1}\|_2 \le 1/(r + \delta)$. Rewrite the equation as $(\tilde \Lambda_2 - cI) S = R' + S (\Lambda_1 - cI)$. Using $\|B C D\| \le \|B\|_2 \|C\| \|D\|_2$ for unitarily invariant norms,
$$\|S\| \le \frac{\|R'\| + r \|S\|}{r + \delta}, \qquad \text{so} \qquad \delta \|S\| \le \|R'\| .$$
In the reverse configuration, the spectrum of $\tilde \Lambda_2$ is in $[a, b]$ and that of $\Lambda_1$ avoids $(a - \delta, b + \delta)$. Write $S (\Lambda_1 - cI) = (\tilde \Lambda_2 - cI) S - R'$ and use $\|(\Lambda_1 - cI)^{-1}\|_2 \le 1/(r + \delta)$ in the same way.

**Step 4 (residual form).** With $R = A X - X M$, the same multiplication by $Y_\perp^*$ gives $\Lambda_2 (Y_\perp^* X) - (Y_\perp^* X) M = Y_\perp^* R$. Steps 2 and 3 apply with $\Lambda_2$ in place of $\tilde \Lambda_2$ and $M$ in place of $\Lambda_1$.

**Step 5 (gap of $A$).** Take $\tilde X$ for the indices $r, \dots, s$, so that $\tilde \Lambda_2$ holds $\tilde \lambda_j$ for $j < r$ and $j > s$. By Weyl's inequality, $|\tilde \lambda_j - \lambda_j| \le \|E\|_2$ for every $j$. So the spectrum of $\Lambda_1$ lies in $[\lambda_s, \lambda_r]$, while $\tilde \lambda_j \ge \lambda_{r-1} - \|E\|_2 \ge \lambda_r + \delta_0 - \|E\|_2$ for $j < r$, and $\tilde \lambda_j \le \lambda_s - \delta_0 + \|E\|_2$ for $j > s$. That is interval separation with $\delta = \delta_0 - \|E\|_2 > 0$, and Step 3 gives item 4. $\square$

## Consequences

- **One eigenvector.** For a simple eigenvalue $\lambda_j$ with gap $\delta_0 = \min_{i \ne j} |\lambda_i - \lambda_j|$, the unit eigenvector $\tilde x$ of $A + E$ for $\tilde \lambda_j$ satisfies $\sin \angle(x_j, \tilde x) \le \|E\|_2 / (\delta_0 - \|E\|_2)$. To first order, the eigenvector condition number is $1/\delta_0$, as in GVL Section 8.1.
- **Ritz vectors.** In the [Rayleigh-Ritz method](/rayleigh-ritz-method/) and [Lanczos](/lanczos-algorithm/), with $X$ the Ritz vectors, $M = X^* A X$ and $R = A X - X M$, item 3 bounds the angle to the true eigenvectors by $\|R\|_2 / \delta$. This is a computable certificate once the gap $\delta$ is known or estimated, for example from the Ritz values and the [Courant-Fischer theorem](/courant-fischer-theorem/).
- **Inverse iteration.** For [inverse iteration](/inverse-iteration/), a small residual certifies a good eigenvector only when the gap is large; within a cluster, only the cluster's subspace is certified.
- **Statistics and machine learning.** [Principal component analysis](/principal-component-analysis/) and [spectral clustering](/spectral-clustering/) estimate eigenspaces of a population matrix from a sample matrix. Item 4, or its variant by Yu, Wang and Samworth (2015), $\|\sin \Theta\|_F \le 2 \min(\sqrt{k} \|E\|_2, \|E\|_F) / \delta_0$, which needs no condition on $\|E\|_2$, converts a bound on the noise $E$ into a bound on the error of the estimated subspace.
- **Companions.** The same paper proves the tan θ theorem, $\|\tan \Theta\| \le \|R\| / \delta$ under a stronger separation condition, and the sin 2θ and tan 2θ theorems for the case where the perturbation is measured off the block diagonal.

## Tightness

- **The constant 1 is attained in the limit.** Take $A = \operatorname{diag}(0, \delta)$, $E = \begin{pmatrix} 0 & \varepsilon \\ \varepsilon & 0 \end{pmatrix}$ and $X = e_1$. Then $\tilde \Lambda_2 = \tilde \lambda_1 = \delta/2 + \sqrt{\delta^2/4 + \varepsilon^2}$, and a short computation gives $\sin \theta = \varepsilon / \sqrt{\tilde \lambda_1^2 + \varepsilon^2}$, while the bound of item 2 is $\|E X\|_2 / \tilde \lambda_1 = \varepsilon / \tilde \lambda_1$. The ratio tends to 1 as $\varepsilon / \delta \to 0$. For $\delta = 1$ and $\varepsilon = 0.1$: $\sin \theta = 0.0985376$ and the bound is $0.0990195$.
- **The gap cannot be dropped.** For $A = I_2$ (gap 0), every unit vector is an eigenvector, and an arbitrarily small $E$ can make the eigenvectors of $A + E$ any orthonormal pair. So no bound of the form $f(\|E\|)$ without a gap exists.
- **Interval separation matters for the spectral norm.** If the spectra of $\Lambda_1$ and $\tilde \Lambda_2$ are only $\delta$ apart, interlaced rather than separated by an interval, the Frobenius bound of item 1 still holds, but in the spectral norm the Sylvester equation only gives $\|S\|_2 \le c \|R'\|_2 / \delta$ with $c = \pi/2$ (Bhatia, Davis and McIntosh 1983), and a constant larger than 1 is needed in general.
- **The separation is between $\Lambda_1$ and $\tilde \Lambda_2$.** Item 2 mixes an unperturbed and a perturbed spectrum. A bound with the gap $\delta_0$ of $A$ alone needs the loss $\|E\|_2$ of item 4, or a factor 2 as in Yu, Wang and Samworth.
- **Non-Hermitian matrices.** The theorem fails without symmetry: invariant subspaces of non-normal matrices are governed by $\operatorname{sep}(T_{11}, T_{22})$, which can be much smaller than the eigenvalue gap (Stewart 1973; Stewart and Sun, Chapter V).

## History

Chandler Davis and William Kahan proved the sin θ, tan θ, sin 2θ and tan 2θ theorems in the third part of their paper series on the rotation of eigenvectors by a perturbation, published in 1970 and announced in 1969. Earlier results go back to Kato's perturbation theory and Wilkinson's analysis of eigenvectors. Bhatia, Davis and McIntosh extended the Sylvester equation bounds to spectra without interval separation in 1983. Since the 2000s the theorem has become a standard tool in statistics and machine learning, and Yu, Wang and Samworth gave in 2015 a version that depends only on the population eigengap.

## References
