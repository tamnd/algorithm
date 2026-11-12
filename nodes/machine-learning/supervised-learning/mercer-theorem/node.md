---
tag: Z2X9JZ
kind: theorem
slug: mercer-theorem
name: Mercer's theorem
area: machine-learning/supervised-learning
level: advanced
summary: "A continuous, symmetric, positive semidefinite kernel on a compact domain has an eigen-expansion with nonnegative eigenvalues that converges absolutely and uniformly."
prereqs: [kernel-trick, spectral-theorem]
see_also: [kernel-trick, representer-theorem, karhunen-loeve-theorem, positive-definite-matrix, jacobi-eigenvalue-algorithm, kernel-pca, gaussian-process, support-vector-machine]
sources:
  - paper: doi:10.1098/rsta.1909.0016
    title: James Mercer, Functions of positive and negative type, and their connection with the theory of integral equations, Philosophical Transactions of the Royal Society of London, Series A 209, 1909
    locator: pp. 415 to 446 (the expansion of a continuous kernel of positive type on a closed interval)
  - paper: doi:10.1090/S0002-9947-1950-0051437-7
    title: Nachman Aronszajn, Theory of reproducing kernels, Transactions of the American Mathematical Society 68(3), 1950
    locator: pp. 337 to 404 (every positive definite kernel on a set has a unique reproducing kernel Hilbert space)
  - book: isbn:9780387772417
    title: Ingo Steinwart and Andreas Christmann, Support Vector Machines, Springer, 2008
    locator: Chapter 4 (kernels and reproducing kernel Hilbert spaces, including the section on Mercer's theorem)
  - book: isbn:9780262182539
    title: Carl Edward Rasmussen and Christopher K. I. Williams, Gaussian Processes for Machine Learning, MIT Press, 2006
    locator: Chapter 4 (covariance functions; the eigenfunction analysis of kernels and Mercer's theorem)
  - book: isbn:9780262194754
    title: Bernhard Schölkopf and Alexander J. Smola, Learning with Kernels, MIT Press, 2002
    locator: Chapter 2 (the Mercer kernel map and its relation to the reproducing kernel map)
---

Mercer's theorem says that a continuous, symmetric, positive semidefinite kernel $k$ on a compact domain is a sum $k(x, z) = \sum_j \lambda_j e_j(x) e_j(z)$ over the eigenfunctions $e_j$ of its integral operator, with eigenvalues $\lambda_j \ge 0$, and that the series converges absolutely and uniformly. So $\varphi(x) = (\sqrt{\lambda_j} e_j(x))_j$ is an explicit feature map with $k(x, z) = \varphi(x) \cdot \varphi(z)$, which justifies the [kernel trick](/kernel-trick/) for such kernels. James Mercer proved it for a closed interval in 1909. It is a different result from the Moore-Aronszajn theorem, which needs no topology at all.

## Statement

Let $X$ be a compact metric space and $\mu$ a finite Borel measure on $X$ whose support is all of $X$, so every nonempty open set has positive measure. Let $k : X \times X \to \mathbb{R}$ satisfy:

1. $k$ is continuous;
2. $k$ is symmetric: $k(x, z) = k(z, x)$;
3. $k$ is positive semidefinite: $\int_X \int_X k(x, z) f(x) f(z)\, d\mu(x)\, d\mu(z) \ge 0$ for every $f \in L^2(\mu)$.

Let $T_k$ be the integral operator $(T_k f)(x) = \int_X k(x, z) f(z)\, d\mu(z)$ on $L^2(\mu)$.

**Theorem (Mercer 1909, in the general form).** There is a finite or countable orthonormal family $(e_j)$ in $L^2(\mu)$ of eigenfunctions of $T_k$, with eigenvalues $\lambda_1 \ge \lambda_2 \ge \cdots > 0$, such that:

1. each $e_j$ has a continuous representative, and we use it;
2. $\lambda_j \to 0$ if the family is infinite;
3. for all $x, z \in X$,
$$k(x, z) = \sum_j \lambda_j\, e_j(x)\, e_j(z),$$
and the series converges absolutely and uniformly on $X \times X$;
4. $\sum_j \lambda_j = \int_X k(x, x)\, d\mu(x) < \infty$.

The other eigenvalues of $T_k$ are 0, so all of them are nonnegative. Mercer's original setting is $X = [a, b]$ with the Lebesgue measure.

**Remark on hypothesis 3.** For a continuous $k$ and a measure with full support, condition 3 holds if and only if every Gram matrix $(k(x_i, x_j))_{i,j}$ on finitely many points is positive semidefinite. One direction approximates the double integral by sums $\sum_{i,j} k(x_i, x_j) c_i c_j$. The other direction takes $f$ as a combination of the normalized indicators of small balls around $x_1, \ldots, x_n$, whose double integral tends to $\sum_{i,j} k(x_i, x_j) c_i c_j$ by continuity.

**Moore-Aronszajn is a separate theorem.** Let $X$ be any set, with no topology and no measure, and $k$ a symmetric function whose Gram matrices are all positive semidefinite. Then there is a unique Hilbert space $\mathcal{H}$ of functions on $X$ that contains each $k(x, \cdot)$ and satisfies $f(x) = \langle f, k(x, \cdot) \rangle_{\mathcal{H}}$ (Aronszajn 1950, who credits E. H. Moore). It gives the feature map $x \mapsto k(x, \cdot)$ but no eigen-expansion and no rate. Mercer's theorem needs continuity, compactness and a measure, and gives the expansion with uniform convergence.

## In plain words

A positive semidefinite matrix $K$ can be written as $\sum_j \lambda_j v_j v_j^\top$ with nonnegative eigenvalues and orthonormal eigenvectors. Mercer's theorem is the same statement for a kernel, which is a matrix with a continuum of rows and columns. The eigenvectors become eigenfunctions, the sum may have infinitely many terms, and the theorem adds that the infinite sum converges as well as one could hope: at every pair of points, and at the same speed everywhere.

## Proof

**Step 1. $T_k$ is compact, self-adjoint and positive.** The function $k$ is continuous on the compact set $X \times X$, so $|k| \le M$ for some $M$, and $\int\int k^2\, d\mu\, d\mu < \infty$. So $T_k$ is a Hilbert-Schmidt operator, which is compact. It is self-adjoint because $k$ is symmetric, and $\langle T_k f, f \rangle \ge 0$ by hypothesis 3. The spectral theorem for compact self-adjoint operators gives an orthonormal family $(e_j)$ of eigenfunctions with eigenvalues $\lambda_j \ne 0$, with $\lambda_j \to 0$ if there are infinitely many, such that $L^2(\mu) = \ker T_k \oplus \overline{\operatorname{span}}(e_j)$. Positivity gives $\lambda_j = \langle T_k e_j, e_j \rangle > 0$. For each $f \in L^2(\mu)$,

$$\langle T_k f, f \rangle = \sum_j \lambda_j \langle f, e_j \rangle^2. \tag{1}$$

**Step 2. Eigenfunctions are continuous.** For $f \in L^2(\mu)$ and $x, x' \in X$, the Cauchy-Schwarz inequality gives

$$|T_k f(x) - T_k f(x')| \le \sup_{z} |k(x, z) - k(x', z)| \cdot \mu(X)^{1/2} \lVert f \rVert_2,$$

which tends to 0 as $x' \to x$ because $k$ is uniformly continuous. So $T_k f$ is continuous. Since $e_j = T_k e_j / \lambda_j$, we choose this continuous representative. Then $T_k e_j(x) = \lambda_j e_j(x)$ at every point $x$.

**Step 3. The remainder is positive semidefinite.** Let

$$k_N(x, z) = k(x, z) - \sum_{j \le N} \lambda_j e_j(x) e_j(z).$$

It is continuous and symmetric, and by (1), $\int\int k_N f f\, d\mu\, d\mu = \sum_{j > N} \lambda_j \langle f, e_j \rangle^2 \ge 0$ for every $f \in L^2(\mu)$.

**Step 4. The diagonal is bounded.** A continuous kernel $h$ that satisfies hypothesis 3 has $h(x, x) \ge 0$ for each $x$. If $h(x_0, x_0) < 0$, then by continuity $h < -c$ on $U \times U$ for some $c > 0$ and some open ball $U$ around $x_0$, and $\mu(U) > 0$ because the support is all of $X$. The indicator $f = \mathbf{1}_U$ gives $\int\int h f f \le -c\, \mu(U)^2 < 0$, a contradiction. Apply this to $k_N$:

$$\sum_{j \le N} \lambda_j e_j(x)^2 \le k(x, x) \le M \quad \text{for all } x \text{ and } N. \tag{2}$$

So the series $\sum_j \lambda_j e_j(x)^2$ of nonnegative terms converges at every $x$.

**Step 5. Convergence in $z$ for fixed $x$.** By the Cauchy-Schwarz inequality and (2),

$$\sum_{j=m}^{n} |\lambda_j e_j(x) e_j(z)| \le \Big(\sum_{j=m}^{n} \lambda_j e_j(x)^2\Big)^{1/2} \Big(\sum_{j=m}^{n} \lambda_j e_j(z)^2\Big)^{1/2} \le \Big(\sum_{j=m}^{n} \lambda_j e_j(x)^2\Big)^{1/2} M^{1/2}. \tag{3}$$

For a fixed $x$ the right side tends to 0 as $m \to \infty$, independently of $z$. So the series $\tilde k(x, z) = \sum_j \lambda_j e_j(x) e_j(z)$ converges absolutely, and uniformly in $z$, and $\tilde k(x, \cdot)$ is continuous.

**Step 6. The series sums to $k$.** Fix $x$ and let $g = k(x, \cdot) \in L^2(\mu)$. Its coefficients are $\langle g, e_j \rangle = T_k e_j(x) = \lambda_j e_j(x)$ by Step 2. For $h \in \ker T_k$, $\langle g, h \rangle = T_k h(x)$, and $T_k h$ is a continuous function that is 0 almost everywhere, so it is 0 everywhere because $\mu$ has full support. So $g \perp \ker T_k$, and $g = \sum_j \lambda_j e_j(x) e_j$ in $L^2(\mu)$. The same series converges uniformly to $\tilde k(x, \cdot)$ by Step 5, hence also in $L^2(\mu)$, since $\mu$ is finite. So $k(x, \cdot) = \tilde k(x, \cdot)$ almost everywhere. Both are continuous and $\mu$ has full support, so they are equal everywhere.

**Step 7. Uniform convergence.** By Step 6 with $z = x$, the partial sums $s_N(x) = \sum_{j \le N} \lambda_j e_j(x)^2$ increase to $k(x, x)$ at each point. They are continuous, the limit is continuous, and $X$ is compact, so by Dini's theorem the convergence is uniform: $\varepsilon_m = \sup_x \sum_{j \ge m} \lambda_j e_j(x)^2 \to 0$. Then (3) gives $\sum_{j \ge m} |\lambda_j e_j(x) e_j(z)| \le (\varepsilon_m M)^{1/2}$ for all $x, z$, which is absolute and uniform convergence on $X \times X$.

**Step 8. The trace.** Integrate $k(x, x) = \sum_j \lambda_j e_j(x)^2$ over $X$. The convergence is uniform and $\mu$ is finite, so the sum and the integral commute, and $\int k(x, x)\, d\mu = \sum_j \lambda_j \lVert e_j \rVert_2^2 = \sum_j \lambda_j$. $\blacksquare$

## Consequences

- **An explicit feature map.** $\varphi(x) = (\sqrt{\lambda_j}\, e_j(x))_j$ lies in $\ell^2$ by (2), and $k(x, z) = \langle \varphi(x), \varphi(z) \rangle_{\ell^2}$. This is the feature space of the [kernel trick](/kernel-trick/) for continuous kernels on compact sets.
- **The reproducing kernel Hilbert space.** The RKHS of $k$ is $\{\sum_j c_j e_j : \sum_j c_j^2/\lambda_j < \infty\}$ with $\lVert f \rVert^2 = \sum_j c_j^2/\lambda_j$. Fast eigenvalue decay means a small space of smooth functions. This is the norm that the [representer theorem](/representer-theorem/) penalizes.
- **Gram matrices.** Every Gram matrix of $k$ is positive semidefinite, and the eigenvalues of $K/n$ on $n$ points drawn from $\mu$ approximate the $\lambda_j$. This is the basis of the Nyström method and of [kernel PCA](/kernel-pca/).
- **The Karhunen-Loève expansion.** If $k$ is the covariance of a centered process, the [Karhunen-Loève theorem](/karhunen-loeve-theorem/) expands the process as $\sum_j \sqrt{\lambda_j} Z_j e_j(x)$ with uncorrelated $Z_j$.
- **The trace class property.** $\sum_j \lambda_j < \infty$, so the eigenvalues decay faster than $1/j$ on average.

**A worked example.** On $[0, 1]$ with the Lebesgue measure, $k(x, z) = \min(x, z)$ (the covariance of Brownian motion) has

$$\lambda_j = \frac{1}{(j - \tfrac12)^2 \pi^2}, \qquad e_j(x) = \sqrt 2 \sin\big((j - \tfrac12)\pi x\big), \qquad j = 1, 2, \ldots$$

The trace is $\sum_j \lambda_j = \tfrac{4}{\pi^2} \cdot \tfrac{\pi^2}{8} = \tfrac12 = \int_0^1 x\, dx$. Since $|e_j| \le \sqrt 2$, the uniform error after $N$ terms is at most $2\sum_{j > N} \lambda_j < 2/(\pi^2 (N - \tfrac12))$. On a $41 \times 41$ grid, the maximum error falls as $N$ grows through 5, 20, 80 and 320, and stays below this bound. The midpoint rule with $n = 40$ points gives the matrix $K/n$, whose largest eigenvalues, from a cyclic Jacobi solver, are $0.40534$, $0.04508$, $0.01626$ and $0.00832$, against the exact $0.40528$, $0.04503$, $0.01621$ and $0.00827$.

**A numerical check of nonnegativity.** For a Gaussian kernel $\exp(-(x - z)^2/2\sigma^2)$ with $\sigma = 1$ on 12 random points in $[-2, 2]$ (seed 1909), the Jacobi eigenvalues of the Gram matrix range from about $10^{-11}$ to $6.47$, and they sum to the trace 12. The function $|x - z|$ is symmetric but not positive semidefinite: on the points 0 and 1 its Gram matrix has eigenvalues $1$ and $-1$.

## Tightness

Each hypothesis is needed.

- **Continuity.** Let $k(x, z) = 1$ if $x = z$ and 0 otherwise on $[0, 1]$. Every Gram matrix on distinct points is the identity, so $k$ is positive semidefinite in the Gram sense, and the Moore-Aronszajn theorem applies. But $T_k = 0$ for the Lebesgue measure, so the expansion is empty and gives 0, not $k(x, x) = 1$.
- **Full support.** Let $X = [0, 2]$, $\mu$ the Lebesgue measure on $[0, 1]$, and $k(x, z) = \max(0, x - 1) \max(0, z - 1)$. Then $T_k = 0$ on $L^2(\mu)$, while $k \ne 0$ on $(1, 2]^2$. In general the expansion only holds on the support of $\mu$.
- **Compactness.** On $\mathbb{R}$ with the Lebesgue measure, the Gaussian kernel gives a convolution operator, which is not compact and has no eigenfunctions in $L^2$. The Fourier transform plays the role of the expansion instead.
- **Positive semidefiniteness.** For a continuous symmetric kernel that is not positive semidefinite, the expansion can still exist in $L^2$, but it has negative eigenvalues, so $\varphi$ is not a feature map into a Hilbert space, and uniform convergence can fail.
- **No general rate.** The theorem gives no rate for $\lambda_j \to 0$. For $\min(x, z)$ the rate is $\Theta(j^{-2})$, and for the Gaussian kernel it is faster than any power.

## History

Hilbert and Schmidt developed the theory of integral equations with symmetric kernels from 1904 to 1907, including the expansion of a symmetric kernel in $L^2$. James Mercer (1909) studied kernels "of positive type" on an interval and proved that for these the eigen-expansion converges absolutely and uniformly. Aronszajn (1950) gave the general theory of reproducing kernels on arbitrary sets. Aizerman, Braverman and Rozonoer (1964) used such expansions in pattern recognition, and the support vector machine of Boser, Guyon and Vapnik (1992) made "Mercer kernels" a standard term in machine learning. Later work extended the theorem to compact metric spaces with a finite Borel measure of full support, as stated here, and to some non-compact domains under extra conditions.

## References
