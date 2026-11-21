---
tag: QRYS9G
kind: theorem
slug: picard-condition
name: Picard condition
aliases:
- Picard criterion
- discrete Picard condition
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: "For compact A, Ax = y has a solution exactly when y is in the closure of the range (orthogonal to the null space of A*) and the sum of |<u_k, y>|^2 / sigma_k^2 is finite."
model: real-ram
prereqs: [singular-value-expansion, pseudoinverse]
see_also: [fredholm-integral-equation-first-kind, well-posed-problem, degree-of-ill-posedness, source-condition, truncated-svd, spectral-filter-factors, morozov-discrepancy-principle, regularization-method]
sources:
  - paper: doi:10.1007/BF03014061
    title: Emile Picard, Sur un theoreme general relatif aux equations integrales de premiere espece et sur quelques problemes de physique mathematique, Rendiconti del Circolo Matematico di Palermo 29, 1910, 79 to 97
    locator: the condition for the solvability of a first-kind integral equation in terms of the eigenfunction pairs of its kernel
  - book: "Rainer Kress, Linear Integral Equations, Springer, 1989"
    locator: the chapter on ill-posed problems (Picard's theorem for compact operators with a singular system)
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 2, Ill-Posed Linear Operator Equations (the Picard criterion for the domain of the generalized inverse)
  - paper: doi:10.1007/BF01933214
    title: Per Christian Hansen, The discrete Picard condition for discrete ill-posed problems, BIT 30(4), 1990, 658 to 672
    locator: the definition of the discrete Picard condition and its use with Tikhonov regularization
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapters 2 and 3 (the Picard condition for the SVE, and the discrete Picard plot)
---

The Picard condition decides when a linear equation $A x = y$ with a compact operator $A$ has a solution. It needs two things. The data $y$ must lie in the closure of the range of $A$, which is the same as being orthogonal to the null space of $A^*$. And the coefficients of $y$ on the left singular vectors must decay fast enough that $\sum_k |\langle u_k, y \rangle|^2/\sigma_k^2$ is finite. The second part alone is not enough. The theorem gives the existence test of a [well-posed problem](/well-posed-problem/) in terms of the [singular value expansion](/singular-value-expansion/). The *discrete* Picard condition, an alias of this page, is a different statement: a heuristic of Hansen for matrices, treated in its own section below.

## Statement

**Theorem (Picard).** Let $A: X \to Y$ be a compact linear operator between Hilbert spaces with singular system $(\sigma_k; v_k, u_k)$. Let $y \in Y$. Then $y \in R(A)$ if and only if

1. $y \in N(A^*)^\perp = \overline{R(A)}$, and
2. $\displaystyle \sum_k \frac{|\langle u_k, y \rangle|^2}{\sigma_k^2} < \infty.$

In this case the solutions of $A x = y$ are $x^\dagger + z$ with $z \in N(A)$, where
$$x^\dagger = \sum_k \frac{\langle u_k, y \rangle}{\sigma_k}\, v_k$$
is the solution of minimum norm, and $\|x^\dagger\|^2 = \sum_k |\langle u_k, y \rangle|^2/\sigma_k^2$.

**Least squares form.** Let $Q$ be the orthogonal projection onto $\overline{R(A)}$. The least squares problem $\min_x \|A x - y\|$ has a solution, that is, $y$ is in the domain $D(A^\dagger) = R(A) \oplus R(A)^\perp$ of the [pseudoinverse](/pseudoinverse/), if and only if condition 2 holds. Then $A^\dagger y = x^\dagger$ as above. The reason is that $Q y$ has the same coefficients $\langle u_k, Q y \rangle = \langle u_k, y \rangle$ and satisfies condition 1.

If the range of $A$ has finite dimension, the sum is finite and condition 2 always holds. The theorem has content only for an infinite singular system, where $\sigma_k \to 0$.

## In plain words

The forward operator shrinks each pattern of the unknown by its own gain, and the gains go to zero. So any data that really come from some unknown have pattern coefficients that shrink at least as fast as the gains, in the sense that coefficient divided by gain is square summable. If the data have too much of the fast patterns, no unknown can produce them. There is a second trap. The data can also contain a part that the operator cannot produce at all, a direction that no input reaches. That part has zero coefficient on every output pattern, so the sum does not see it. It must be checked on its own.

## Proof

**Only if.** Let $y = A x$. Then $y \in R(A) \subseteq \overline{R(A)} = N(A^*)^\perp$, which is condition 1. For each $k$,
$$\langle u_k, y \rangle = \langle u_k, A x \rangle = \langle A^* u_k, x \rangle = \sigma_k \langle v_k, x \rangle.$$
So $\sum_k |\langle u_k, y \rangle|^2/\sigma_k^2 = \sum_k |\langle v_k, x \rangle|^2 \le \|x\|^2$ by Bessel's inequality, since the $v_k$ are orthonormal. This is condition 2.

**If.** Assume conditions 1 and 2. The numbers $c_k = \langle u_k, y \rangle/\sigma_k$ are square summable and the $v_k$ are orthonormal, so the series $x^\dagger = \sum_k c_k v_k$ converges in $X$ (Riesz-Fischer). Since $A$ is bounded, it can be applied term by term:
$$A x^\dagger = \sum_k c_k A v_k = \sum_k c_k \sigma_k u_k = \sum_k \langle u_k, y \rangle u_k = P y,$$
where $P$ is the orthogonal projection onto the closed span of the $u_k$. That span is $\overline{R(A)}$: each $u_k = A v_k/\sigma_k$ is in $R(A)$, and each $A x = \sum_k \sigma_k \langle v_k, x \rangle u_k$ is in the closed span. By condition 1, $y \in \overline{R(A)}$, so $P y = y$ and $A x^\dagger = y$.

**The set of solutions.** If $A x = y$ then $A(x - x^\dagger) = 0$, so every solution is $x^\dagger + z$ with $z \in N(A)$. The vector $x^\dagger$ lies in the closed span of the $v_k$, which is $N(A)^\perp$. So $\|x^\dagger + z\|^2 = \|x^\dagger\|^2 + \|z\|^2$, and $x^\dagger$ is the unique solution of minimum norm. Its norm is $\sum_k |c_k|^2$ by Parseval. $\square$

The finite-rank case is the same proof with finite sums.

## Consequences

- **The generalized inverse is unbounded.** On its domain, $A^\dagger y = \sum_k \langle u_k, y \rangle v_k/\sigma_k$. With $y = u_k$, $\|A^\dagger u_k\| = 1/\sigma_k \to \infty$. So $A^\dagger$ is unbounded whenever the singular system is infinite.
- **Smoothness of the solution.** The same argument with weights shows that $x^\dagger$ lies in $R((A^* A)^\nu)$ (a [source condition](/source-condition/)) exactly when $\sum_k |\langle u_k, y \rangle|^2/\sigma_k^{2 + 4\nu} < \infty$. Faster decay of the data coefficients means a smoother solution.
- **Noisy data fail the condition.** The noise $e$ in $y^\delta = y + e$ usually has coefficients $\langle u_k, e \rangle$ that do not decay at all. Then the sum diverges for $y^\delta$ even when it converges for $y$, and $A^\dagger y^\delta$ does not exist. Regularization replaces $1/\sigma_k$ by bounded [spectral filter factors](/spectral-filter-factors/) so that the sum stays finite.
- **TSVD and the condition.** The [truncated SVD](/truncated-svd/) solution $x_k$ keeps the first $k$ terms of the Picard series. For data that satisfy the condition, $x_k \to x^\dagger$ as $k \to \infty$, and $\|x_k\|$ increases to $\|x^\dagger\|$.

**Worked example.** Take the integration operator $(A x)(s) = \int_0^s x(t)\,dt$ on $L^2(0,1)$, with $\sigma_k = 1/w_k$, $w_k = (k - \tfrac12)\pi$, $u_k(s) = \sqrt2 \sin(w_k s)$ and $v_k(t) = \sqrt2 \cos(w_k t)$. Its range is dense, because $A^* y = \int_t^1 y(s)\,ds = 0$ forces $y = 0$; so condition 1 always holds here.

- $y(s) = s$. Then $\langle u_k, y \rangle = \sqrt2 (-1)^{k+1}/w_k^2$, the ratios are $\sqrt2 (-1)^{k+1}/w_k$, and the sum is $\sum_k 2/w_k^2 = \tfrac{8}{\pi^2} \sum_k \tfrac{1}{(2k-1)^2} = 1$. The condition holds, and the Picard series is the cosine series of $x^\dagger = 1$, whose norm is 1.
- $y(s) = 1$. Then $\langle u_k, y \rangle = \sqrt2/w_k$, each ratio is $\sqrt2$, and the partial sums are $2K$. The condition fails, as it must: every $A x$ vanishes at $s = 0$.

**The discrete Picard condition.** The discrete Picard condition (Hansen 1990) is a heuristic for a matrix $A = \sum_{i=1}^n \sigma_i u_i v_i^T$ that comes from a discretized compact operator. Every finite sum is finite, so the theorem above says nothing about a matrix. Hansen's condition asks instead that the exact data $b$ have coefficients $|u_i^T b|$ that decay, on average, faster than the $\sigma_i$, until the $\sigma_i$ reach the level of the errors in the problem. If it holds, regularized solutions can approximate the exact solution; if it fails, no filtering helps. It is not a theorem: "on average" and "the level of the errors" are judged by eye on a Picard plot of $\sigma_i$, $|u_i^T b|$ and their ratio against $i$.

With noise, the coefficients of $b^\delta = b + e$ level off at a noise floor. For white noise with standard deviation $\sigma$ per entry, each $u_i^T e$ has standard deviation $\sigma$, because $U$ is orthogonal. The example below uses the rectangle-rule integration matrix with $n = 24$, the exact solution $x_j = \sin(\pi t_j)$ at the midpoints $t_j$, and Gaussian noise (seed 15) scaled to $\|e\| = 10^{-2}$, so the floor is about $10^{-2}/\sqrt{24} = 2.0 \times 10^{-3}$.

| $i$ | $\sigma_i$ | $\lvert u_i^T b \rvert$ | $\lvert u_i^T b^\delta \rvert$ |
|---|---|---|---|
| 1 | 0.650 | 1.93 | 1.93 |
| 2 | 0.217 | 0.369 | 0.370 |
| 3 | 0.131 | 0.0659 | 0.0651 |
| 4 | 0.0936 | 0.0147 | 0.0148 |
| 5 | 0.0732 | 0.0110 | 0.0107 |
| 6 | 0.0603 | 0.00301 | 0.00517 |
| 8 | 0.0450 | 0.000956 | 0.000429 |
| 12 | 0.0310 | 0.000157 | 0.00310 |
| 16 | 0.0249 | 0.0000294 | 0.00241 |
| 24 | 0.0209 | 0.0000000259 | 0.00527 |

The exact coefficients fall far faster than the singular values, so the exact data satisfy the discrete condition. The noisy coefficients stop falling near $i = 6$, at the floor. Components beyond that point carry mostly noise, which is why the discrepancy principle stops the [truncated SVD](/truncated-svd/) of this problem at $k = 6$. The plot gives the same advice by eye; it does not give a proved parameter choice.

## Tightness

- **Condition 1 cannot be dropped.** On $\ell^2$ let $A e_k = \sigma_k e_{k+1}$ with $\sigma_k = 1/k$, so $v_k = e_k$ and $u_k = e_{k+1}$. For $y = e_1$ every coefficient $\langle u_k, y \rangle$ is zero and the sum in condition 2 is $0$. But $y$ is orthogonal to the range, and $A^* e_1 = 0$, so $y \in N(A^*)$. No $x$ solves $A x = e_1$: since $\|A x - e_1\|^2 = \|A x\|^2 + 1$, the least squares solution is $x = 0$, with residual 1.
- **Decay faster than $\sigma_k$ is not enough.** If $\langle u_k, y \rangle = \sigma_k/\sqrt{k}$, the ratios $1/\sqrt{k}$ tend to zero, but $\sum_k 1/k$ diverges. The condition is about square summability, not about the ratio tending to zero.
- **No condition on finitely many terms.** Changing finitely many coefficients of $y$ never changes the answer. The condition is only about the tail.

## History

Emile Picard published the criterion in 1910 for integral equations of the first kind, in terms of the pairs of eigenfunctions of a non-symmetric kernel that Schmidt had introduced in 1907. In the operator form above it is standard in the theory of ill-posed problems; Kress states it as a theorem for compact operators, and Engl, Hanke and Neubauer use it to describe the domain of the generalized inverse. Per Christian Hansen introduced the discrete Picard condition in 1990 to explain when Tikhonov regularization of a discrete ill-posed problem can succeed, and the Picard plot became a standard diagnostic.

## References
