---
tag: HWYJKB
kind: algorithm
slug: coherent-point-drift
name: Coherent point drift
aliases:
- CPD
area: computer-vision/point-clouds-and-registration
level: advanced
summary: "Registers two point sets by fitting one as the centroids of a Gaussian mixture to the other with EM. It has rigid, affine and non-rigid forms; the non-rigid form keeps the motion smooth."
solves: [point-cloud-registration, non-rigid-registration]
model: real-ram
complexity:
  vars: {n: the number of data points, K: the number of centroids, N: the number of iterations}
  time: {worst: Θ(N K n), average: Θ(N K n), best: Θ(K n)}
  space: {extra: Θ(K n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2010
  people: [Andriy Myronenko, Xubo Song, Miguel Á. Carreira-Perpiñán]
  note: "Myronenko, Song and Carreira-Perpiñán gave the non-rigid method at NIPS 2006. Myronenko and Song gave the full method with the rigid, affine and non-rigid forms in IEEE TPAMI in 2010."
prereqs: [point-cloud-registration, expectation-maximization, gaussian-mixture-model]
see_also: [non-rigid-registration, robust-point-matching, iterative-closest-point, kabsch-algorithm, maximum-likelihood-estimation, kernel-trick, tikhonov-regularization, point-set-chamfer-distance]
sources:
  - paper: doi:10.1109/TPAMI.2010.46
    title: "Andriy Myronenko and Xubo Song, Point set registration: Coherent point drift, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(12), 2010, 2262-2275"
    locator: "The Gaussian mixture model with the uniform outlier term, the E-step, and the closed-form M-steps of the rigid, affine and non-rigid forms; the motion coherence prior and the fast Gauss transform and low-rank speed-ups"
  - paper: doi:10.1111/j.2517-6161.1977.tb01600.x
    title: "A. P. Dempster, N. M. Laird and D. B. Rubin, Maximum likelihood from incomplete data via the EM algorithm, Journal of the Royal Statistical Society, Series B 39(1), 1977, 1-38"
    locator: "The EM algorithm and the proof that each iteration does not decrease the likelihood"
  - paper: doi:10.1109/34.88573
    title: "Shinji Umeyama, Least-squares estimation of transformation parameters between two point patterns, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(4), 1991, 376-380"
    locator: "The main theorem: the best rotation and scale by the SVD, with the sign of the determinant, used in the rigid M-step"
---

Coherent point drift (CPD) registers two point sets by treating one of them as a [Gaussian mixture model](/gaussian-mixture-model/). The points of the moving set $Y$ are the centroids of the mixture, all with the same variance $\sigma^2$, and the points of the fixed set $X$ are the data. CPD moves the centroids so that the mixture explains the data as well as possible, by the [expectation maximization](/expectation-maximization/) (EM) algorithm. The E-step computes soft correspondences: for each data point, the probability that each centroid produced it. The M-step computes the transformation that best fits these weighted pairs, in closed form for a rigid motion with scale and for an affine map. A third form allows a smooth deformation, and so solves the [non-rigid registration](/non-rigid-registration/) problem. A uniform component of weight $w$ absorbs outliers. Each iteration does not increase the negative log-likelihood, but, like [iterative closest point](/iterative-closest-point/), CPD is a local method.

## In plain words

Put a soft, round cloud of fog around each point of the first set. Now look at the second set. Each of its points asks every fog cloud: how likely is it that I came from you? Near clouds get a large share of the point, far clouds get almost nothing.

With these shares fixed, find the turn, slide and stretch of the first set that makes the shares fit best. Move the first set. Then make the fog clouds a little smaller, because the sets now match better, and ask again.

At first the fog is wide, so every point pulls a little on every other point, and small details do not matter. As the fog shrinks, the matches become sharp. A point of the second set that is far from every cloud is counted as noise and pulls on nothing.

## The problem

**Input.** A fixed set $X = (x_1, \ldots, x_n)$ and a moving set $Y = (y_1, \ldots, y_K)$ in $\mathbb{R}^D$, with $n \ge 1$ and $K \ge 1$; an outlier weight $0 \le w < 1$; and a family of transformations $T$. (The paper writes $N$ for $n$ and $M$ for $K$.)

**Output.** A transformation $T$ and a variance $\sigma^2$ at a stationary point of the EM iteration for the likelihood of $X$ under the mixture

$$p(x) = \frac{w}{n} + \frac{1 - w}{K} \sum_{k=1}^{K} (2\pi\sigma^2)^{-D/2} \exp\!\left(-\frac{|x - T(y_k)|^2}{2\sigma^2}\right).$$

For the rigid form, $T(y) = s R y + t$ with $R \in SO(D)$, a scale $s > 0$ and a translation $t$. For the affine form, $T(y) = B y + t$ with any $D \times D$ matrix $B$. For the non-rigid form, $T(Y) = Y + G W$, where $G$ is the $K \times K$ Gaussian kernel matrix $G_{jk} = \exp(-|y_j - y_k|^2 / (2\beta^2))$ and $W$ is a $K \times D$ matrix of coefficients. The non-rigid form also adds the penalty $\frac{\lambda}{2} \operatorname{tr}(W^{\mathsf T} G W)$ to the negative log-likelihood, which is the motion coherence prior: it makes nearby centroids move together. CPD does not promise the global maximum of the likelihood. The problem is a form of [point cloud registration](/point-cloud-registration/) with soft correspondences.

## The algorithm

In the E-step, the posterior that data point $x_i$ comes from centroid $k$ is

$$P_{ki} = \frac{\exp(-|x_i - T(y_k)|^2 / (2\sigma^2))}{\sum_{j=1}^{K} \exp(-|x_i - T(y_j)|^2 / (2\sigma^2)) + c}, \qquad c = (2\pi\sigma^2)^{D/2} \, \frac{w}{1 - w} \, \frac{K}{n} .$$

The constant $c$ comes from the uniform component. A point far from every centroid gets small values $P_{ki}$ for all $k$, so it has little effect on the M-step. Below, $\mathbf 1$ is a vector of ones, $\operatorname{d}(v)$ is the diagonal matrix of a vector $v$, $X$ is the $n \times D$ matrix of the data and $Y$ is the $K \times D$ matrix of the centroids. The pseudocode is the rigid form.

```pseudo id=main
CPD-RIGID(X, Y, w, tol)         ▷ X = (x_1 .. x_n), Y = (y_1 .. y_K), in R^D
L1  R ← I ;  s ← 1 ;  t ← 0 ;  σ² ← (1/(D n K)) Σ_k Σ_i |x_i - y_k|²
L2  repeat (up to an iteration cap)
L3      P_ki ← E-step with T(y) = s R y + t ;  E ← -Σ_i log p(x_i)
L4      if E_prev - E ≤ tol · max(1, |E|) or σ² ≤ σ²_min then exit the loop
L5      N_P ← 1ᵀ P 1 ;  μ_x ← Xᵀ Pᵀ 1 / N_P ;  μ_y ← Yᵀ P 1 / N_P ;  X̂ ← X - 1 μ_xᵀ ;  Ŷ ← Y - 1 μ_yᵀ
L6      A ← X̂ᵀ Pᵀ Ŷ ;  U Σ Vᵀ ← SVD(A)
L7      R ← U diag(1, .., 1, det(U Vᵀ)) Vᵀ ;  s ← tr(Aᵀ R) / tr(Ŷᵀ d(P 1) Ŷ) ;  t ← μ_x - s R μ_y
L8      σ² ← (tr(X̂ᵀ d(Pᵀ 1) X̂) - 2 s tr(Aᵀ R) + s² tr(Ŷᵀ d(P 1) Ŷ)) / (N_P D)
L9  return R, s, t
```

Line L1 starts at the identity, with a large variance: the mean squared distance over all pairs, divided by $D$. Line L3 is the E-step; it also gives the negative log-likelihood $E$ of the current parameters at no extra cost, because the denominators of $P$ are the mixture densities up to a constant. Line L4 stops when $E$ no longer falls by more than a relative tol, or when $\sigma^2$ reaches a floor. Lines L5 to L8 are the M-step. Line L5 computes the weighted means and centers both sets. Line L6 forms the weighted cross-covariance $A$ and its [SVD](/singular-value-decomposition/). Line L7 is the weighted form of the [Kabsch algorithm](/kabsch-algorithm/) with the sign fix of Umeyama, followed by the best scale and translation. Line L8 is the best variance for the new pose. With the scale fixed to 1, line L7 skips the scale, and line L8 keeps the same formula with $s = 1$. The paper writes line L8 as $(\operatorname{tr}(\hat X^{\mathsf T} \operatorname{d}(P^{\mathsf T} \mathbf 1) \hat X) - s \operatorname{tr}(A^{\mathsf T} R)) / (N_P D)$, which is the same value when $s$ is the optimal scale.

The other forms change only lines L5 to L8.

- **Affine.** $B = A (\hat Y^{\mathsf T} \operatorname{d}(P\mathbf 1) \hat Y)^{-1}$, $t = \mu_x - B \mu_y$ and $\sigma^2 = (\operatorname{tr}(\hat X^{\mathsf T} \operatorname{d}(P^{\mathsf T}\mathbf 1) \hat X) - \operatorname{tr}(A B^{\mathsf T})) / (N_P D)$.
- **Non-rigid.** Solve $(G + \lambda \sigma^2 \operatorname{d}(P\mathbf 1)^{-1}) W = \operatorname{d}(P\mathbf 1)^{-1} P X - Y$ for $W$, set $T(Y) = Y + G W$, and set $\sigma^2 = (\operatorname{tr}(X^{\mathsf T} \operatorname{d}(P^{\mathsf T}\mathbf 1) X) - 2 \operatorname{tr}((P X)^{\mathsf T} T) + \operatorname{tr}(T^{\mathsf T} \operatorname{d}(P\mathbf 1) T)) / (N_P D)$. The reference code multiplies the linear system by $\operatorname{d}(P\mathbf 1)$, which gives $(\operatorname{d}(P\mathbf 1) G + \lambda \sigma^2 I) W = P X - \operatorname{d}(P\mathbf 1) Y$ and avoids a division by a small entry of $P\mathbf 1$.

The width $\beta$ of the kernel sets how far the motion of one centroid spreads to its neighbors, and $\lambda$ sets how much the method prefers smooth motion to a close fit. Both are tuning values that the user must choose.

## Example

Take the moving set $y_1 = (0, 0)$, $y_2 = (2, 0)$, $y_3 = (0, 1)$, $y_4 = (1, 1)$ in the plane. The data are the same points turned by 60 degrees and moved by $(0.5, 0)$: $x_1 = (0.5, 0)$, $x_2 = (1.5, 1.7321)$, $x_3 = (-0.366, 0.5)$, $x_4 = (0.134, 1.366)$. Run rigid CPD with scale, $w = 0$. The start variance is $\sigma^2 = 1.0647$. With this wide variance the first E-step spreads each point over all centroids; for example, $x_1$ gives the weights 0.379, 0.148, 0.237 and 0.237 to $y_1, \ldots, y_4$.

| M-steps | angle of $R$ | $s$ | $\sigma^2$ | $E$ after the step |
|---|---|---|---|---|
| 0 | 0 | 1 | 1.0647 | 10.5804 |
| 1 | 12.31° | 0.3778 | 0.4206 | 8.3821 |
| 2 | 30.97° | 0.3761 | 0.4058 | 8.2040 |
| 3 | 46.52° | 0.4534 | 0.3728 | 7.9732 |
| 4 | 55.16° | 0.5869 | 0.3040 | 7.5036 |
| 5 | 58.75° | 0.7437 | 0.2004 | 6.4142 |
| 6 | 59.38° | 0.8986 | 0.0821 | 3.1250 |
| 7 | 59.95° | 0.9973 | 0.00226 | -11.4655 |
| 8 | 60.00° | 1.0000 | $10^{-12}$ (the floor) | -97.6274 |

The negative log-likelihood $E$ falls at every step. The scale first drops to about 0.38: with a wide variance, every data point pulls on every centroid, so the best fit squeezes the moving set toward the weighted mean. As $\sigma^2$ falls, the soft matches become sharp, the scale returns to 1, and the eighth M-step gives the exact pose. The data fit exactly, so $\sigma^2$ goes to 0 and the code stops at its floor $10^{-12}$.

CPD is local. With the same four points and the scale fixed to 1, a true rotation of 90 degrees ends at 32.6 degrees, and a true rotation of 150 degrees ends at -30.1 degrees. Both are stationary points of EM that are not the truth.

## Correctness

Claim: each iteration does not increase the negative log-likelihood $E$, provided $N_P > 0$, $s > 0$ and the new $\sigma^2 > 0$. The proof has two parts. First, the EM bound: by Jensen's inequality, $E(\theta) - E(\theta_{\text{old}}) \le Q(\theta) - Q(\theta_{\text{old}})$, where $Q(\theta) = \frac{1}{2\sigma^2} \sum_{k,i} P_{ki} |x_i - T(y_k)|^2 + \frac{N_P D}{2} \log \sigma^2$ uses the posteriors $P$ of the old parameters. Second, lines L5 to L8 minimize $Q$ exactly. The translation drops out by centering. For a fixed scale, the rotation must maximize $\operatorname{tr}(A^{\mathsf T} R)$ over $SO(D)$, which the SVD with the sign fix does (Umeyama's theorem). The scale and the variance then have closed forms. The affine M-step is a least squares solve. The non-rigid M-step minimizes a convex function of $W$ and then $\sigma^2$, so it is a generalized EM step, and the bound holds for $E$ plus the penalty. The full proof is in [proofs/correctness.md](proofs/correctness.md). The claim does not give the global maximum of the likelihood, and it does not bound the number of iterations.

## Complexity

The model is the [real RAM](/real-ram/), and $D$ is a constant. Line L3 computes $K n$ squared distances and exponentials, $\Theta(K n)$ time. Lines L5 and L6 compute the row sums, the column sums and $A$, also $\Theta(K n)$, and the SVD of the $D \times D$ matrix $A$ takes $O(1)$ time. So a rigid or affine iteration takes $\Theta(K n)$ time, and $N$ iterations take $\Theta(N K n)$. The best case stops after the second E-step, $\Theta(K n)$. The matrix $P$ needs $\Theta(K n)$ extra space; an implementation that never stores $P$ can make two passes over the pairs and use $\Theta(K + n)$ space.

The non-rigid form also forms $G$ in $\Theta(K^2)$ time and solves a dense $K \times K$ system in each iteration, $\Theta(K^3)$ by Gaussian elimination, so an iteration takes $\Theta(K n + K^3)$ time and $\Theta(K n + K^2)$ space. The paper lowers these costs with the fast Gauss transform for the sums of line L3 and a low-rank approximation of $G$; these are approximations with their own error. The number of iterations $N$ has no useful bound. EM usually converges linearly, and the rate gets worse when the mixture components overlap much.

## Properties

- **Monotone.** The negative log-likelihood (plus the penalty in the non-rigid form) never increases.
- **Local.** The result depends on the start. The example has wrong stationary points at 90 and 150 degrees.
- **Soft correspondences.** No hard nearest neighbor decision is made. Every pair has a weight, which makes the cost smooth in the parameters.
- **Coarse to fine without a schedule.** The variance $\sigma^2$ is estimated, not set. It starts large and shrinks as the fit improves, which gives a coarse-to-fine search similar to the annealing of [robust point matching](/robust-point-matching/), but driven by the data.
- **Robust to outliers in X.** The uniform component with weight $w$ gives a data point far from all centroids a small total weight.
- **Not symmetric.** $X$ and $Y$ play different roles: every centroid is a mixture component, but data points can be outliers.
- **Deterministic.** The same input gives the same output.

## Variants and improvements

- **Fast sums.** The paper uses the fast Gauss transform for the E-step and a low-rank approximation of $G$ for the non-rigid solve, which makes large sets practical.
- **Other kernels and priors.** The motion coherence prior uses a Gaussian kernel. Other kernels, such as the thin plate spline kernel of [robust point matching](/robust-point-matching/), give other kinds of smooth motion.
- **Fixed scale.** Rigid CPD without scale is a probabilistic form of ICP with soft matches. As $\sigma^2 \to 0$, each posterior becomes a hard match to the closest centroid.
- **Features.** The posteriors can be multiplied by a feature similarity, so that points with different colors or descriptors do not match.
- **Bayesian forms.** Later work gives a Bayesian form of CPD with a prior on the transformation and a variational EM; it is outside this page.

## When to use it

Use CPD for small and medium point sets with noise and some outliers when a rough start is known. It is a good default for non-rigid registration of shapes such as contours, faces or organs, where the motion is smooth. For the rigid case on large clouds, ICP with a [k-d tree](/kd-tree/) is cheaper, because CPD looks at all $K n$ pairs in each iteration unless the fast sums are used. Without a rough start, use a global method first, such as [fast global registration](/fast-global-registration/) or [TEASER](/teaser-registration/). When most of $Y$ has no partner in $X$, the model is wrong: every centroid is a component that must explain some data, so the outlier term protects only against extra points in $X$.

## Pitfalls

- **The roles of X and Y.** $Y$ moves and is the mixture; $X$ is the data and may hold outliers. Swapping them changes the result and the meaning of $w$.
- **A wrong sign in line L7.** Without $\operatorname{diag}(1, \ldots, 1, \det(U V^{\mathsf T}))$, the rotation can be a reflection.
- **Underflow in line L3.** When $\sigma^2$ is small, all terms of a column can underflow to 0, and the posterior becomes 0/0. Shift each column by its least squared distance before the exponential, as the reference code does.
- **Sigma squared reaching zero.** On exact data $\sigma^2 \to 0$ and $\log \sigma^2 \to -\infty$. Use a floor and stop there.
- **Shrinking scale.** In the first iterations, the rigid form with scale can shrink $Y$ by a large factor, as in the example. It recovers on good data, but with many outliers it can stay small. Fix the scale if it is known.
- **Choice of w, beta and lambda.** These are tuning values. A $w$ that is too large makes CPD ignore real points; a small $\beta$ or $\lambda$ lets the non-rigid form overfit noise.
- **Units.** $\sigma^2$, $\beta$ and the outlier constant depend on the units. Normalize both sets to zero mean and unit variance first, and undo the normalization after.

## Implementations

## History

Myronenko, Song and Carreira-Perpiñán presented the non-rigid method at NIPS in 2006. Myronenko and Song published the full method in IEEE TPAMI in 2010, with the rigid, affine and non-rigid forms, the uniform outlier term and fast implementations. The non-rigid prior follows the motion coherence theory of Yuille and Grzywacz, which asks that nearby points move together. Earlier methods that also used soft correspondences include the softassign method of Gold, Rangarajan and others (1998), and its thin plate spline form by Chui and Rangarajan (2003), see [robust point matching](/robust-point-matching/). The EM algorithm itself is due to Dempster, Laird and Rubin (1977).

## References
