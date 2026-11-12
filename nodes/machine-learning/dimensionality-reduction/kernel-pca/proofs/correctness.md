---
title: Kernel PCA computes PCA in feature space from the centered Gram matrix
proves: [correctness]
status: full
---

**Setup.** $k(a, b) = \langle \Phi(a), \Phi(b)\rangle$ for a feature map $\Phi$ into a Hilbert space $\mathcal{H}$. The points $x_1, \ldots, x_n$ have the feature mean $\bar\Phi = \frac1n \sum_i \Phi(x_i)$ and the centered features $\tilde\Phi_i = \Phi(x_i) - \bar\Phi$. The covariance operator is $\bar C = \frac1n \sum_i \tilde\Phi_i \langle \tilde\Phi_i, \cdot\rangle$, and PCA in feature space asks for its eigenvectors $V$ with eigenvalues $\lambda > 0$. Let $K'_{ij} = \langle \tilde\Phi_i, \tilde\Phi_j\rangle$.

**Lemma 1 (centering).** $K' = K - \mathbf{1}_n K - K \mathbf{1}_n + \mathbf{1}_n K \mathbf{1}_n$, where $\mathbf{1}_n$ is the $n \times n$ matrix with all entries $1/n$. For a new point $t$, $\langle \tilde\Phi_i, \Phi(t) - \bar\Phi \rangle = k(x_i, t) - \frac1n \sum_l k(x_l, t) - \frac1n \sum_l K_{il} + \frac{1}{n^2}\sum_{l,m} K_{lm}$.

*Proof.* Expand $\langle \Phi(x_i) - \bar\Phi, \Phi(x_j) - \bar\Phi\rangle = K_{ij} - \frac1n \sum_l K_{lj} - \frac1n \sum_l K_{il} + \frac1{n^2}\sum_{l, m} K_{lm}$. The four terms are the entries $(i, j)$ of $K$, $\mathbf{1}_n K$, $K \mathbf{1}_n$ and $\mathbf{1}_n K \mathbf{1}_n$. The second formula is the same expansion with $\Phi(t)$ in place of $\Phi(x_j)$. $\square$

**Lemma 2 (the span).** Every eigenvector $V$ of $\bar C$ with $\lambda > 0$ is $V = \sum_i \alpha_i \tilde\Phi_i$ for some $\alpha \in \mathbb{R}^n$.

*Proof.* $V = \frac{1}{\lambda} \bar C V = \frac{1}{n\lambda} \sum_i \langle \tilde\Phi_i, V\rangle \tilde\Phi_i$. Take $\alpha_i = \langle \tilde\Phi_i, V\rangle / (n\lambda)$. $\square$

**Theorem.** (a) If $K'\alpha = \mu\alpha$ with $\mu > 0$ and $\alpha \ne 0$, then $V = \sum_i \alpha_i \tilde\Phi_i$ is an eigenvector of $\bar C$ with eigenvalue $\lambda = \mu / n$, and $\|V\|^2 = \mu\|\alpha\|^2$. So the scaling $\mu\|\alpha\|^2 = 1$ of L5 gives a unit vector. (b) Every eigenpair $(\lambda, V)$ of $\bar C$ with $\lambda > 0$ arises in this way from $\mu = n\lambda$. (c) Eigenvectors of $K'$ for different eigenvalues give orthogonal $V$. (d) The projection of $\Phi(t) - \bar\Phi$ on $V$ is $\sum_i \alpha_i \tilde k(x_i, t)$ with $\tilde k$ the centered kernel of Lemma 1, which is L6 to L8. For a training point $x_j$ it equals $(K'\alpha)_j = \mu \alpha_j$.

*Proof.* (a) $\bar C V = \frac1n \sum_j \tilde\Phi_j \langle \tilde\Phi_j, \sum_i \alpha_i \tilde\Phi_i\rangle = \frac1n \sum_j (K'\alpha)_j \tilde\Phi_j = \frac{\mu}{n} \sum_j \alpha_j \tilde\Phi_j = \frac{\mu}{n} V$. Also $\|V\|^2 = \sum_{i, j} \alpha_i \alpha_j K'_{ij} = \alpha^T K' \alpha = \mu \|\alpha\|^2 > 0$, so $V \ne 0$.

(b) By Lemma 2, $V = \sum_i \alpha_i \tilde\Phi_i$. Taking the inner product of $\bar C V = \lambda V$ with each $\tilde\Phi_l$ gives $\frac1n (K'^2 \alpha)_l = \lambda (K'\alpha)_l$, that is $K'(K' - n\lambda I)\alpha = 0$. Write $\alpha = \alpha_0 + \alpha_1$ with $\alpha_0$ in the null space of $K'$ and $\alpha_1$ in its range, which is orthogonal to it because $K'$ is symmetric. Then $\sum_i (\alpha_0)_i \tilde\Phi_i$ has the squared norm $\alpha_0^T K' \alpha_0 = 0$, so $V = \sum_i (\alpha_1)_i \tilde\Phi_i$. And $(K' - n\lambda I)\alpha_1$ lies in the range and in the null space of $K'$, since $K'(K' - n\lambda I)\alpha_1 = K'(K' - n\lambda I)\alpha = 0$; so it is $0$, and $K'\alpha_1 = n\lambda\alpha_1$.

(c) For $K'\alpha = \mu\alpha$ and $K'\beta = \nu\beta$ with $\mu \ne \nu$, $\langle V_\alpha, V_\beta \rangle = \alpha^T K' \beta = \nu\, \alpha^T \beta = 0$, because eigenvectors of a symmetric matrix for different eigenvalues are orthogonal.

(d) $\langle V, \Phi(t) - \bar\Phi\rangle = \sum_i \alpha_i \langle \tilde\Phi_i, \Phi(t) - \bar\Phi\rangle$, and Lemma 1 gives each term. For $t = x_j$ the inner products are $K'_{ij}$. $\blacksquare$

**Corollary (linear kernel).** For $k(a, b) = a^T b$, $\Phi$ is the identity, $K' = X_c X_c^T$, and the theorem says that the nonzero eigenvalues of $X_c X_c^T / n$ are the nonzero eigenvalues of the covariance $X_c^T X_c / n$, with $V = X_c^T \alpha$ the principal directions and the scores $X_c V = \mu\alpha$. So kernel PCA with the linear kernel is ordinary PCA.

**Remark.** The method finds only the nonzero part of the spectrum; at most $n - 1$ eigenvalues of $\bar C$ are nonzero, because the $\tilde\Phi_i$ sum to zero. The pre-image step of Mika et al. is a separate, approximate optimization and is not covered by this proof.
