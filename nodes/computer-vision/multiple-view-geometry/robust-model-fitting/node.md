---
tag: 6F92BC
kind: problem
slug: robust-model-fitting
name: Robust model fitting
aliases:
- outlier-robust estimation
- robust geometric estimation
area: computer-vision/multiple-view-geometry
level: core
summary: "Fit a model such as a homography or an essential matrix to data that contain a large fraction of outliers, which ordinary least squares cannot tolerate."
prereqs: [ordinary-least-squares, breakdown-point]
see_also: [ransac, msac, magsac, j-linkage, least-median-of-squares, m-estimator, hough-transform, ransac-iteration-bound]
sources:
  - paper: doi:10.1145/358669.358692
    title: "Martin A. Fischler and Robert C. Bolles, Random sample consensus: a paradigm for model fitting with applications to image analysis and automated cartography, Communications of the ACM 24(6), 1981, 381-395"
    locator: "The statement of the fitting problem with gross errors, the argument against least squares and the RANSAC paradigm"
  - paper: doi:10.1007/978-3-030-01258-8_43
    title: "Tat-Jun Chin, Zhipeng Cai and Frank Neumann, Robust fitting in computer vision: easy or hard?, European Conference on Computer Vision (ECCV 2018), arXiv:1802.06464"
    locator: "Section 1.1 (summary of results), Section 2 (Theorem 1, NP-completeness of the decision version of maximum consensus by reduction from k-SLAB), Section 3 (W[1]-hardness in the dimension and the FPT algorithm in the number of outliers) and Section 4 (APX-hardness)"
  - paper: doi:10.1080/01621459.1984.10477105
    title: "Peter J. Rousseeuw, Least median of squares regression, Journal of the American Statistical Association 79(388), 1984, 871-880"
    locator: "The breakdown point of least squares and the 50 percent breakdown point of least median of squares"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 4.7, Robust estimation (RANSAC, the distance threshold, the number of samples and the robust cost functions)"
---

Robust model fitting is the problem of finding the parameters of a model, such as a line, a plane, a [homography](/homography/) or an [essential matrix](/essential-matrix/), from measurements of which a large part are wrong. The wrong measurements, the outliers, do not follow the model at all, and they can be anywhere. In computer vision they come mostly from wrong matches between two images, and it is common that half of the matches or more are wrong. [Ordinary least squares](/ordinary-least-squares/) cannot handle this: a single outlier that is far enough away can move the fit as far as it likes. A robust method must give the outliers a bounded influence, and usually it must also find out which measurements they are. The best known methods, such as [RANSAC](/ransac/), fit the model to many small random samples and keep the model that most of the data agree with. Finding the model with the most agreeing data exactly is NP-hard.

## In plain words

Suppose you want to draw the best straight line through a set of dots. If all dots are close to one line, the usual method works: it makes the sum of the squared distances small. Now add a few dots that are far away and have nothing to do with the line. The usual method tries to please them too, and the line tilts toward them. One dot that is far enough can pull the line anywhere.

A robust method asks a different question: which line passes close to the largest number of dots? The far dots then do not count, because no good line passes near them. The hard part is to find that line without trying every possible line.

## Definition

The input is data $D = \{x_1, \ldots, x_n\}$, a set $\Theta$ of model parameters and a residual $r(\theta, x) \ge 0$ that says how far $x$ is from the model $\theta$. Some unknown subset $I \subseteq D$, the inliers, follows a true model $\theta_0$ up to noise, and the other items are outliers with no structure. The main forms of the goal are:

- **Maximum consensus.** With an inlier threshold $T$, find $\theta$ that maximizes $\Psi(\theta) = |\{i : r(\theta, x_i) \le T\}|$, the number of inliers.
- **M-estimation with a bounded loss.** Find $\theta$ that minimizes $\sum_i \rho(r(\theta, x_i))$ for a loss $\rho$ that grows like $r^2$ near 0 and is bounded, such as $\min(r^2, T^2)$. Maximum consensus is the case where $\rho$ is 0 up to $T$ and 1 after.
- **Least median of squares.** Find $\theta$ that minimizes the median of $r(\theta, x_i)^2$. It needs no threshold.

The breakdown point of an estimator is the smallest fraction of the data that, when replaced by arbitrary values, can move the estimate arbitrarily far. Least squares has breakdown point $1/n$. [Least median of squares](/least-median-of-squares/) has breakdown point close to $1/2$ (Rousseeuw, 1984), and maximum consensus can work with more than half outliers when the outliers have no common structure.

## Variants

- **Known or unknown noise level.** Maximum consensus and the truncated quadratic need a threshold $T$, which comes from the noise level. [MAGSAC](/magsac/) needs only an upper bound on it, and least median of squares needs none.
- **One model or several.** When the data contain several structures, such as several planes, the problem is to find all of them and their number. [J-linkage](/j-linkage/) and the [Hough transform](/hough-transform/) solve this form.
- **Linear and non-linear models.** For a line or a plane the residual is linear in $\theta$. For a [fundamental matrix](/fundamental-matrix/) or a camera pose it is not, which makes exact methods harder.
- **Prior information.** Matches often come with a quality score, which [PROSAC](/prosac/) uses to sample good matches first.
- **Time limits.** In real-time systems the time is fixed in advance, as in [preemptive RANSAC](/preemptive-ransac/).

## Examples

Take the 10 points $(x, 2x + 1)$ for $x = 0, 1, \ldots, 9$, which lie exactly on the line $y = 2x + 1$, and the 3 outliers $(1, 20)$, $(5, -10)$ and $(8, 40)$. The least squares line of the 13 points is $y = 2.091x + 2.048$. All 10 inliers are 1.05 to 1.87 below it, so with the threshold $T = 0.5$ on the vertical distance it has no inliers at all. Move the outlier $(8, 40)$ to $(8, 400)$, and the least squares line becomes $y = 13.71x - 23.00$: one point moves the fit as far as it likes.

Maximum consensus with $T = 0.5$ gives $y = 2x + 1$ with 10 inliers, and no line has more. Moving an outlier does not change this answer, as long as the outlier does not land within $T$ of the line. [RANSAC](/ransac/) finds it by drawing pairs of points. A pair of two inliers gives the true line, and with $10/13$ of the points inliers the [iteration bound](/ransac-iteration-bound/) asks for $\lceil \log 0.01 / \log(1 - (10/13)^2) \rceil = 6$ pairs to find such a pair with probability 0.99.

## Known algorithms

| algorithm | goal | type |
|---|---|---|
| [RANSAC](/ransac/) | maximum consensus | random sampling, no optimality guarantee |
| [MSAC](/msac/) | truncated quadratic | RANSAC loop with a different score |
| [MLESAC](/mlesac/) | likelihood of a mixture of inliers and outliers | RANSAC loop |
| [LO-RANSAC](/lo-ransac/) | maximum consensus or truncated quadratic | RANSAC loop with local refinement |
| [PROSAC](/prosac/) | maximum consensus | sampling guided by match quality |
| [Preemptive RANSAC](/preemptive-ransac/) | additive score | fixed time budget |
| [MAGSAC](/magsac/) | loss marginalized over the noise scale | RANSAC loop, no threshold |
| [Least median of squares](/least-median-of-squares/) | median squared residual | random sampling in practice |
| [M-estimators](/m-estimator/) by [IRLS](/iteratively-reweighted-least-squares/) | robust loss | local descent from a start model |
| [Hough transform](/hough-transform/) | votes in a parameter grid | exhaustive over the grid |
| [J-linkage](/j-linkage/) | several models | random hypotheses and clustering |

Exact methods for maximum consensus, such as branch and bound and tree search, also exist. They find the best model with a guarantee, but their time grows exponentially in the dimension or in the number of outliers.

## Bounds

Chin, Cai and Neumann (2018) studied maximum consensus for linear models, with residuals $|a_i^\top \theta - b_i|$ and $\theta \in \mathbb{R}^d$. They proved these results:

- The decision version is NP-complete (Theorem 1), by a reduction from the k-SLAB problem. So no algorithm solves maximum consensus in time polynomial in $n$ and $d$, unless P = NP.
- The problem is W[1]-hard in the dimension $d$. So no algorithm runs in time $f(d) \cdot \mathrm{poly}(n)$ for any function $f$, unless FPT = W[1].
- The problem is APX-hard, so it has no polynomial-time approximation scheme, unless P = NP.
- The problem is fixed-parameter tractable in the number of outliers $o$ and the dimension $d$: it can be solved in time $O(d^{\,o})\,\mathrm{poly}(n, d)$.

Random sampling has no worst-case guarantee, but its expected cost is simple. If a fraction $w$ of the items are inliers and a sample of $s$ inliers gives a good model, about $w^{-s}$ samples are needed on average, and the [iteration bound](/ransac-iteration-bound/) gives the number of samples for a confidence $p$. Each sample costs $\Theta(n)$ to score, so the time is $\Theta(n \log(1-p)/\log(1 - w^s))$ under these assumptions.

## Reductions

- **Maximum consensus and k-SLAB.** For linear models, maximum consensus with threshold $T$ is the same as finding a slab of width $2T$ that contains the most points, and the minimal width of a slab that holds $k$ points is the decision problem k-SLAB. Chin, Cai and Neumann use this to prove NP-hardness.
- **Least median of squares and slabs.** Least median of squares asks for the thinnest slab that contains half the points, the case $k = n/2$ of the same geometry.
- **From robust fitting to least squares.** Once the inliers are known, the problem becomes an ordinary [least squares problem](/least-squares-problem/) on the inliers. This is why most robust methods end with a refit.
- **M-estimation to weighted least squares.** A robust loss can be minimized by [iteratively reweighted least squares](/iteratively-reweighted-least-squares/), a sequence of [weighted least squares](/weighted-least-squares/) problems.

## Applications

- **Image stitching** fits a [homography](/homography-estimation/) between images from matched features, many of which are wrong ([image stitching](/image-stitching/)).
- **Two-view geometry** estimates the [fundamental matrix](/fundamental-matrix/) or the [essential matrix](/essential-matrix/) from matches, with the [five-point](/five-point-algorithm/) or [eight-point](/eight-point-algorithm/) solvers inside a RANSAC loop.
- **Camera pose** from 2D-3D matches uses [P3P](/p3p/) inside a robust loop ([perspective-n-point](/perspective-n-point/)).
- **Visual odometry and SLAM** estimate the motion between frames in real time ([visual odometry](/visual-odometry/)).
- **Image retrieval** checks a match between two images by [spatial verification](/spatial-verification/).
- **Point clouds** are split into planes, cylinders and other shapes ([efficient RANSAC for shape detection](/efficient-ransac-shape-detection/)).

## References
