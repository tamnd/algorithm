---
tag: M3X8Y4
kind: theorem
slug: karhunen-loeve-theorem
name: Karhunen-Loève theorem
aliases:
- Kosambi-Karhunen-Loève theorem
- Karhunen-Loève expansion
area: compression-and-coding/transforms-for-compression
level: advanced
summary: A zero-mean square-integrable process has an orthogonal eigenfunction expansion with uncorrelated coefficients.
prereqs: [spectral-theorem, mercer-theorem]
see_also: [karhunen-loeve-transform, principal-component-analysis, gaussian-process, signal-decorrelation, energy-compaction, kernel-pca, courant-fischer-theorem, transform-coding]
sources:
  - paper: "Kari Karhunen, Zur Spektraltheorie stochastischer Prozesse, Annales Academiae Scientiarum Fennicae, Series A I 34, 1946"
    title: Kari Karhunen, Zur Spektraltheorie stochastischer Prozesse
    locator: the series expansion of a second-order process on an interval in the eigenfunctions of its covariance
  - paper: "Kari Karhunen, Über lineare Methoden in der Wahrscheinlichkeitsrechnung, Annales Academiae Scientiarum Fennicae, Series A I 37, 1947"
    title: Kari Karhunen, Über lineare Methoden in der Wahrscheinlichkeitsrechnung
    locator: the full treatment of the expansion (Karhunen's thesis)
  - paper: "Michel Loève, Fonctions aléatoires du second ordre, Comptes Rendus de l'Académie des Sciences, Paris 220, 1945"
    title: Michel Loève, Fonctions aléatoires du second ordre
    locator: the expansion announced for second-order random functions
  - paper: "Michel Loève, Probability Theory, D. Van Nostrand, 1955"
    title: Michel Loève, Probability Theory
    locator: the chapter on second-order random functions (the proper orthogonal decomposition with uniform mean-square convergence)
  - paper: doi:10.1007/978-81-322-3676-4_15
    title: D. D. Kosambi, Statistics in function space, Journal of the Indian Mathematical Society 7, 1943, reprinted in D. D. Kosambi, Selected Works in Mathematics and Statistics, Springer, 2016
    locator: pp. 115 to 123 of the reprint (an early form of the expansion in eigenfunctions of the covariance)
  - paper: doi:10.1098/rsta.1909.0016
    title: James Mercer, Functions of positive and negative type, and their connection with the theory of integral equations, Philosophical Transactions of the Royal Society A 209, 1909
    locator: pp. 415 to 446 (a continuous positive kernel is the uniformly convergent sum of its eigenfunction products)
  - paper: doi:10.1007/978-1-4612-3094-6
    title: Roger G. Ghanem and Pol D. Spanos, Stochastic Finite Elements, A Spectral Approach, Springer, 1991
    locator: Chapter 2, Representation of Stochastic Processes, pp. 15 to 65 (the Karhunen-Loève expansion, its error and worked kernels)
  - paper: doi:10.1037/h0071325
    title: Harold Hotelling, Analysis of a complex of statistical variables into principal components, Journal of Educational Psychology 24(6), 1933
    locator: pp. 417 to 441, continued in 24(7), pp. 498 to 520 (the finite-dimensional case, principal components)
---

## Statement

Let $(X_t)_{t \in [a,b]}$ be a real random process on a bounded interval with $E[X_t] = 0$ and $E[X_t^2] < \infty$ for each $t$, and suppose that its covariance $K(s,t) = E[X_s X_t]$ is continuous on $[a,b]^2$. Let $T_K$ be the integral operator on $L^2[a,b]$ given by

$$(T_K f)(s) = \int_a^b K(s,t)\, f(t)\, dt ,$$

and write $\langle f, g\rangle = \int_a^b f(t) g(t)\, dt$.

**Theorem (Karhunen-Loève).**

1. $T_K$ has finitely or countably many positive eigenvalues $\lambda_1 \ge \lambda_2 \ge \dots > 0$, counted with multiplicity, with continuous eigenfunctions $e_1, e_2, \dots$ that are orthonormal in $L^2[a,b]$, and $\sum_k \lambda_k = \int_a^b K(t,t)\, dt < \infty$.
2. The coefficients $Z_k = \int_a^b X_t\, e_k(t)\, dt$ exist as mean-square integrals and satisfy $E[Z_k] = 0$ and $E[Z_j Z_k] = \lambda_k$ if $j = k$, and 0 if $j \ne k$.
3. The series $X_t = \sum_k Z_k\, e_k(t)$ converges in mean square, uniformly in $t$:
$$\sup_{t \in [a,b]} E\Big[\Big(X_t - \sum_{k \le n} Z_k e_k(t)\Big)^2\Big] = \sup_{t \in [a,b]} \Big(K(t,t) - \sum_{k \le n} \lambda_k e_k(t)^2\Big) \xrightarrow[n \to \infty]{} 0 .$$
4. **Optimality.** For each $n$ and each set of continuous functions $f_1, \dots, f_n$ that are orthonormal in $L^2[a,b]$,
$$\int_a^b E\Big[\Big(X_t - \sum_{k=1}^{n} \langle X, f_k\rangle f_k(t)\Big)^2\Big] dt \;\ge\; \sum_{k > n} \lambda_k ,$$
with equality for $f_k = e_k$. Here $\langle X, f\rangle = \int_a^b X_t f(t)\, dt$.
5. If $X$ is a Gaussian process, the $Z_k$ are independent, and $Z_k$ has the normal distribution with mean 0 and variance $\lambda_k$.

## In plain words

A random curve, such as a noisy signal over one second, can be written as a sum of fixed shapes, each multiplied by a random weight. Among all ways to choose the shapes, one choice is special: the shapes that the covariance of the curve maps to multiples of themselves. With these shapes, the random weights have no correlation with each other, the sum gives back the curve, and the first few shapes keep more of the average energy of the curve than any other set of the same size.

The weights are uncorrelated, which does not make them independent. They are independent when the curve is Gaussian. The theorem is the version for continuous time of the Karhunen-Loève transform on vectors, and of principal component analysis.

## Proof

**Step 0 (two facts about the process).** First, $X$ is continuous in mean square, because $E[(X_s - X_t)^2] = K(s,s) - 2K(s,t) + K(t,t)$ and $K$ is continuous. Second, $K$ is symmetric and positive semidefinite: for points $t_1, \dots, t_m$ and real $c_1, \dots, c_m$,

$$\sum_{i,j} c_i c_j K(t_i, t_j) = E\Big[\Big(\sum_i c_i X_{t_i}\Big)^2\Big] \ge 0 .$$

**Step 1 (the eigenfunctions).** A continuous, symmetric, positive semidefinite kernel on $[a,b]^2$ satisfies the hypotheses of [Mercer's theorem](/mercer-theorem/). So $T_K$, a compact self-adjoint operator to which the [spectral theorem](/spectral-theorem/) applies, has nonnegative eigenvalues; its eigenfunctions $e_k$ for the positive eigenvalues $\lambda_k$ are continuous and orthonormal; and

$$K(s,t) = \sum_k \lambda_k\, e_k(s)\, e_k(t),$$

where the series converges absolutely and uniformly on $[a,b]^2$. Setting $s = t$ and integrating gives $\sum_k \lambda_k = \int_a^b K(t,t)\, dt$. This proves part 1.

**Step 2 (mean-square integrals).** Let $f$ and $g$ be continuous on $[a,b]$. For a partition $P$ of $[a,b]$ with points $t_i$ and lengths $\Delta_i$, let $S_P = \sum_i X_{t_i} f(t_i) \Delta_i$. For two partitions $P$ and $Q$,

$$E[S_P S_Q] = \sum_{i,j} f(t_i)\, K(t_i, s_j)\, f(s_j)\, \Delta_i \Delta'_j ,$$

which is a Riemann sum of the continuous function $f(s) K(s,t) f(t)$ on $[a,b]^2$. As the meshes go to 0, $E[S_P S_Q]$, $E[S_P^2]$ and $E[S_Q^2]$ all tend to $\iint f K f$, so $E[(S_P - S_Q)^2] \to 0$. The sums are therefore a Cauchy family in $L^2$ of the probability space, and their limit $\langle X, f\rangle$ exists. Each $S_P$ has mean 0, and the mean and the inner product of $L^2$ are continuous under this limit, so

$$E[\langle X, f\rangle] = 0, \qquad E[\langle X, f\rangle \langle X, g\rangle] = \iint f(s) K(s,t) g(t)\, ds\, dt = \langle f, T_K g\rangle, \qquad E[X_s \langle X, g\rangle] = (T_K g)(s) .$$

**Step 3 (uncorrelated coefficients).** With $f = e_j$ and $g = e_k$, Step 2 gives $E[Z_j] = 0$ and

$$E[Z_j Z_k] = \langle e_j, T_K e_k\rangle = \lambda_k \langle e_j, e_k\rangle ,$$

which is $\lambda_k$ if $j = k$ and 0 otherwise. This proves part 2.

**Step 4 (convergence).** Let $S_n(t) = \sum_{k \le n} Z_k e_k(t)$. By Step 2, $E[X_t Z_k] = (T_K e_k)(t) = \lambda_k e_k(t)$. Expanding the square and using Step 3,

$$E[(X_t - S_n(t))^2] = K(t,t) - 2\sum_{k \le n} \lambda_k e_k(t)^2 + \sum_{k \le n} \lambda_k e_k(t)^2 = K(t,t) - \sum_{k \le n} \lambda_k e_k(t)^2 .$$

By Step 1, the series $\sum_k \lambda_k e_k(t)^2$ converges to $K(t,t)$ uniformly in $t$. So the right side tends to 0 uniformly in $t$. This proves part 3.

**Step 5 (optimality).** Let $f_1, \dots, f_n$ be continuous and orthonormal, and let $P_n X_t = \sum_k \langle X, f_k\rangle f_k(t)$. By Step 2,

$$E[(X_t - P_n X_t)^2] = K(t,t) - 2\sum_k f_k(t)\, (T_K f_k)(t) + \sum_{j,k} f_j(t)\, f_k(t)\, \langle f_j, T_K f_k\rangle .$$

Integrate over $t$. The orthonormality $\langle f_j, f_k\rangle = \delta_{jk}$ removes the terms with $j \ne k$ in the last sum, and gives

$$\int_a^b E[(X_t - P_n X_t)^2]\, dt = \sum_k \lambda_k - \sum_{k=1}^{n} \langle f_k, T_K f_k\rangle .$$

It remains to show $\sum_{k \le n} \langle f_k, T_K f_k\rangle \le \sum_{j \le n} \lambda_j$. The eigenfunctions $e_j$ span the closure of the range of $T_K$, and $T_K$ is zero on the orthogonal complement. So with $c_{kj} = \langle f_k, e_j\rangle$,

$$\langle f_k, T_K f_k\rangle = \sum_j \lambda_j c_{kj}^2, \qquad \sum_{k \le n} \langle f_k, T_K f_k\rangle = \sum_j \lambda_j w_j, \qquad w_j = \sum_{k \le n} c_{kj}^2 .$$

Each $w_j$ is at most $\|e_j\|^2 = 1$ by Bessel's inequality for the orthonormal $f_k$, and $\sum_j w_j \le \sum_k \|f_k\|^2 = n$ by Bessel's inequality for the orthonormal $e_j$. A sum $\sum_j \lambda_j w_j$ with decreasing $\lambda_j \ge 0$, weights in $[0,1]$ and total weight at most $n$ is largest when the weight 1 sits on $\lambda_1, \dots, \lambda_n$: moving weight from an index $j > n$ to an index $i \le n$ with $w_i < 1$ does not decrease the sum, because $\lambda_i \ge \lambda_j$. So $\sum_j \lambda_j w_j \le \sum_{j \le n} \lambda_j$, and the error is at least $\sum_{k > n} \lambda_k$. For $f_k = e_k$, $\langle e_k, T_K e_k\rangle = \lambda_k$ and the bound is reached. This proves part 4.

**Step 6 (the Gaussian case).** If $X$ is Gaussian, each finite family of Riemann sums $(S_{P}^{(1)}, \dots, S_{P}^{(m)})$ for $e_1, \dots, e_m$ is a linear image of a Gaussian vector, so it is Gaussian. Limits in $L^2$ of Gaussian vectors are Gaussian, so $(Z_1, \dots, Z_m)$ is a Gaussian vector. Its covariance is diagonal by Step 3, and a Gaussian vector with a diagonal covariance has independent entries. This proves part 5.

$\blacksquare$

## Consequences

- **The finite case is the KLT.** If the index set is $\{0, \dots, N-1\}$ instead of an interval, $K$ is the covariance matrix, $T_K$ is multiplication by it, Mercer's theorem is the [spectral theorem](/spectral-theorem/) for symmetric matrices, and the expansion is the [Karhunen-Loève transform](/karhunen-loeve-transform/). The theorem on this page is the statement for continuous time; the KLT page gives the algorithm for vectors. [Principal component analysis](/principal-component-analysis/) is the same expansion with the covariance estimated from data.
- **Uniqueness.** The expansion is the only one with both properties. If $X_t = \sum_k Y_k g_k(t)$ in mean square, uniformly in $t$, with orthonormal $g_k$ and uncorrelated $Y_k$, then $K(s,t) = \sum_k E[Y_k^2]\, g_k(s) g_k(t)$, and so $T_K g_k = E[Y_k^2]\, g_k$. When an eigenvalue has multiplicity greater than 1, each orthonormal basis of its eigenspace works.
- **Brownian motion.** On $[0,1]$ with $K(s,t) = \min(s,t)$, differentiating $T_K e = \lambda e$ twice gives $-e = \lambda e''$ with $e(0) = 0$ and $e'(1) = 0$. The solutions are
$$e_k(t) = \sqrt2 \sin\big((k - \tfrac12)\pi t\big), \qquad \lambda_k = \frac{1}{(k - \frac12)^2 \pi^2}, \qquad k = 1, 2, \dots$$
and $W_t = \sum_k Z_k \sqrt2 \sin((k-\frac12)\pi t)$ with independent $Z_k$ of variance $\lambda_k$. The total is $\int_0^1 t\, dt = \frac12$. The first term keeps $8/\pi^2 \approx 81.1\%$ of it, the first three keep 93.3%, and the first ten keep 98.0%. This expansion is a common way to simulate a path.
- **Brownian bridge.** With $K(s,t) = \min(s,t) - st$, the eigenfunctions are $\sqrt2 \sin(k\pi t)$ with $\lambda_k = 1/(k^2\pi^2)$, and the sum is $\frac16$.
- **Stationary periodic processes.** If $K(s,t) = k(s - t)$ with $k$ of period $b - a$, then $T_K$ is a convolution, the eigenfunctions are the sines and cosines of the Fourier series, and the eigenvalues are the Fourier coefficients of $k$. For such processes the KL expansion is the Fourier series. The [discrete cosine transform](/discrete-cosine-transform/) is close to the KLT of a first-order Markov source for a related reason.
- **Compression.** Part 4 is the continuous form of the statement that the KLT has the best [energy compaction](/energy-compaction/). Part 5 is why, for Gaussian sources, [transform coding](/transform-coding/) with the KLT reduces to coding independent scalars.
- **Kernels and Gaussian processes.** The same Mercer expansion gives the features of [kernel PCA](/kernel-pca/) and finite-rank approximations of a [Gaussian process](/gaussian-process/) prior.

## Tightness

- **Uncorrelated is not independent.** Let $U$ be uniform on $[-1,1]$, let $e_1, e_2$ be orthonormal continuous functions, and let $X_t = U e_1(t) + (U^2 - \frac13) e_2(t)$. Then $E[U(U^2 - \frac13)] = E[U^3] = 0$, so $K(s,t) = \frac13 e_1(s)e_1(t) + \frac{4}{45} e_2(s)e_2(t)$. The two eigenvalues differ, so the KL coefficients are $U$ and $U^2 - \frac13$, which are uncorrelated, but the second is a function of the first. Part 5 needs the Gaussian hypothesis.
- **Continuity of the covariance.** Let $X_t$, $t \in [0,1]$, be independent with the standard normal distribution for each $t$. Then $K(s,t)$ is 1 if $s = t$ and 0 otherwise. This kernel is zero almost everywhere, so $T_K = 0$ has no positive eigenvalues and the expansion is empty, although $E[X_t^2] = 1$ for each $t$. If $K$ is only square integrable, the Hilbert-Schmidt theory still gives eigenfunctions, but convergence holds only in mean square integrated over $t$, not for each $t$.
- **A bounded interval.** On the whole line, a stationary covariance such as $K(s,t) = e^{-|s-t|}$ gives a convolution operator that is not compact and has no eigenfunctions in $L^2(\mathbb{R})$. A spectral representation with a continuous spectrum replaces the series.
- **The bound in part 4 is reached**, by $f_k = e_k$, so it cannot be improved. When $\lambda_n = \lambda_{n+1}$, the best $n$-term subspace is not unique.
- **The zero mean.** For a process with a mean $m(t)$, apply the theorem to $X_t - m(t)$. Using the second moment $E[X_s X_t]$ in place of the covariance still gives an expansion, but the coefficients are then correlated with the mean term.

## History

James Mercer proved the expansion of a continuous positive kernel in 1909. Harold Hotelling introduced principal components for a finite set of variables in 1933. D. D. Kosambi described an expansion of random functions in the eigenfunctions of their covariance in 1943. Kari Karhunen gave the expansion of a second-order process in 1946, with a full treatment in his 1947 thesis, and Michel Loève announced it independently in 1945 and gave it in his book Probability Theory (1955). The name Karhunen-Loève theorem is standard; some authors add Kosambi. In engineering the expansion became a tool of detection and estimation theory in the 1960s, and its discrete form, the Karhunen-Loève transform, became the reference transform of transform coding after Huang and Schultheiss (1963). In fluid mechanics it is called the proper orthogonal decomposition, and in uncertainty quantification it is the basis of the spectral stochastic finite elements of Ghanem and Spanos (1991).

## References
