---
tag: 902D1T
kind: technique
slug: sliding-window-bundle-adjustment
name: Sliding window bundle adjustment
aliases:
- local bundle adjustment
- windowed bundle adjustment
area: computer-vision/structure-from-motion
level: advanced
summary: Optimize only the latest keyframes and the points they see, holding older ones fixed or marginalized, to keep visual odometry accurate at bounded cost.
prereqs: [bundle-adjustment, reduced-camera-system, keyframe-selection]
see_also: [schur-complement, sparse-bundle-adjustment, direct-sparse-odometry, visual-odometry, gauge-freedom, levenberg-marquardt, huber-m-estimator, extended-kalman-filter]
sources:
  - paper: doi:10.1002/rob.20360
    title: "Gabe Sibley, Larry Matthies and Gaurav Sukhatme, Sliding window filters and their application to planetary landing, Journal of Field Robotics 27(5), 2010, 587-608"
    locator: "the sliding window filter: a window of states optimized by Gauss-Newton, with old states removed by marginalization through the Schur complement"
  - paper: doi:10.1109/MRA.2012.2182810
    title: "Friedrich Fraundorfer and Davide Scaramuzza, Visual odometry, Part II: matching, robustness, optimization, and applications, IEEE Robotics and Automation Magazine 19(2), 2012, 78-90"
    locator: "windowed bundle adjustment over the last frames for visual odometry"
  - paper: doi:10.1177/0278364914554813
    title: "Stefan Leutenegger, Simon Lynen, Michael Bosse, Roland Siegwart and Paul Furgale, Keyframe-based visual-inertial odometry using nonlinear optimization, International Journal of Robotics Research 34(3), 2015, 314-334"
    locator: "the window of keyframes and recent frames, and the marginalization of old states into a linear prior, with observations dropped to keep the problem sparse"
  - paper: doi:10.1109/TPAMI.2017.2658577
    title: "Jakob Engel, Vladlen Koltun and Daniel Cremers, Direct sparse odometry, IEEE Transactions on Pattern Analysis and Machine Intelligence 40(3), 2018, 611-625"
    locator: "Section 2 (the windowed optimization, the marginalization with the Schur complement and the First Estimate Jacobians)"
---

## In plain words

[Bundle adjustment](/bundle-adjustment/) fixes all camera poses and all 3D points together so that the points project where they were seen. It gives the best answer, but its cost grows with the length of the path, so it cannot run for every frame of a long video. Sliding window bundle adjustment does the same, but only for the last few keyframes and the points they see. When a new keyframe comes in, an old one leaves. The old one can simply be frozen, or its information can be folded into a summary term, called a prior, that pulls the remaining keyframes toward what the old one said about them.

## When it applies

- The problem is a chain: frames come in order, and each one shares points mostly with its recent neighbors. This is the case in [visual odometry](/visual-odometry/).
- The cost per frame must stay bounded, so the full optimization over all frames is too slow.
- The errors are mostly local: the accuracy of the newest pose depends mostly on the recent frames.
- The window is at most a few dozen keyframes. Within the window the problem is a small bundle adjustment, solved with the [reduced camera system](/reduced-camera-system/) and the [Schur complement](/schur-complement/).

## The template

```pseudo id=main
WINDOW-STEP(window 𝒲 of keyframes, points, prior (Ĥ, b̂), new keyframe K)
L1  add K and its observations to 𝒲
L2  minimize Σ ρ(|r|²) + prior over the poses of 𝒲 and their points   ▷ hole: residuals, solver, robust loss ρ, gauge
L3  if 𝒲 has more than W keyframes then
L4      m ← the keyframe to remove                         ▷ hole: oldest, farthest, least visible
L5      either fix m (and drop it later), or marginalize m and its points into (Ĥ, b̂)   ▷ hole: fix or marginalize
L6  return 𝒲, the points and (Ĥ, b̂)
```

**The prior from marginalization.** Write the Gauss-Newton system of line L2 at the current state as $H x = b$, and split the unknowns into the ones that stay, $x_\alpha$, and the ones that leave, $x_\beta$ (the pose of $m$ and the points that only $m$ still observes). The Gauss-Newton model of the cost, minimized over $x_\beta$, is a quadratic in $x_\alpha$ with

$$
\hat H = H_{\alpha\alpha} - H_{\alpha\beta} H_{\beta\beta}^{-1} H_{\beta\alpha}, \qquad \hat b = b_\alpha - H_{\alpha\beta} H_{\beta\beta}^{-1} b_\beta.
$$

This is a theorem about quadratics: for each $x_\alpha$, the minimum over $x_\beta$ of $-b^{\mathsf T} x + \frac{1}{2} x^{\mathsf T} H x$ is $-\hat b^{\mathsf T} x_\alpha + \frac{1}{2} x_\alpha^{\mathsf T} \hat H x_\alpha$ plus a constant. The term $-\hat b^{\mathsf T} \delta + \frac{1}{2} \delta^{\mathsf T} \hat H \delta$, where $\delta$ is the change of the remaining unknowns since the marginalization, is then added to every later cost. For a linear problem with Gaussian noise, the window with the prior gives the same estimate of the remaining unknowns as the full problem; for the nonlinear problem it is an approximation, because the prior is a linearization made once.

**Example.** Two unknowns have the costs $E = (x_1 - 1)^2 + (x_2 - x_1 - 2)^2$: one measurement says $x_1 = 1$, another says $x_2 - x_1 = 2$. Remove $x_1$. The matrix $J^{\mathsf T} J$ is $\begin{pmatrix} 2 & -1 \\ -1 & 1 \end{pmatrix}$, so $\hat H = 1 - (-1) \cdot \frac{1}{2} \cdot (-1) = \frac{1}{2}$, and the prior is $\frac{1}{2}(x_2 - 3)^2$. Check by hand: for fixed $x_2$, the best $x_1$ is the mean of $1$ and $x_2 - 2$, and then $E = 2 \cdot ((x_2 - 3)/2)^2 = \frac{1}{2}(x_2 - 3)^2$. If instead $x_1$ is fixed at $1$, the remaining cost is $(x_2 - 3)^2$, twice as confident as it should be, because the uncertainty of $x_1$ is lost. If the measurements of $x_1$ are simply dropped, $x_2$ is not constrained at all.

## Classic examples

- **The sliding window filter (Sibley, Matthies and Sukhatme, 2010).** A window of states is optimized by Gauss-Newton, and old states are marginalized with the Schur complement. With a window of one state it is close to an extended Kalman filter with relinearization; with a window that holds everything it is full batch optimization (see [extended Kalman filter](/extended-kalman-filter/)).
- **Local bundle adjustment in visual odometry.** Many feature-based systems optimize the last $n$ keyframes and the points they see, and keep the older poses that see these points fixed. The fixed poses hold the [gauge](/gauge-freedom/) and the scale. Fraundorfer and Scaramuzza describe this windowed bundle adjustment as a standard step of visual odometry.
- **Keyframe-based visual-inertial odometry (Leutenegger and others, 2015).** A window of keyframes and recent frames with reprojection and inertial errors; old states are marginalized, and some observations are dropped first so that the prior does not fill the whole matrix.
- **Direct sparse odometry.** A window of 7 keyframes with the photometric error, inverse depths and affine brightness terms. Old keyframes are marginalized, and the residuals of other points into the leaving keyframe are dropped. See [direct sparse odometry](/direct-sparse-odometry/).

## Variations

- **Fix or marginalize.** Fixing old poses is simple and keeps the problem sparse, but it throws away their uncertainty and their information. Marginalization keeps the information as a dense prior on the remaining unknowns.
- **Keeping the problem sparse.** Marginalizing a pose whose points are also seen by other keyframes connects all of those keyframes with each other in $\hat H$. Systems drop some observations before they marginalize, so that the prior stays small. Dropping is an approximation: the dropped observations are lost.
- **Consistency.** If later Gauss-Newton steps evaluate the Jacobians of the variables in the prior at new values, the prior and the new terms can claim information that the data do not have, for example about the [gauge](/gauge-freedom/). The First Estimate Jacobians used by DSO evaluate those Jacobians at the values of the marginalization.
- **Solver.** Gauss-Newton or [Levenberg-Marquardt](/levenberg-marquardt/), with a robust loss such as the [Huber function](/huber-m-estimator/), and the Schur complement over the points.
- **Window contents.** Keyframes only, or keyframes plus the last few frames; a fixed number of keyframes, or a fixed time span.

## Pitfalls

- **Gauge.** Inside the window the problem has the same free motion as full bundle adjustment: 6 degrees of freedom for a stereo or inertial system and 7 for one camera. Hold some poses fixed, or rely on a prior that fixes them, or the matrix is singular.
- **Overconfidence.** Fixing old poses, or relinearizing the prior variables, makes the estimate more confident than it should be. It can then resist corrections and drift in a consistent direction.
- **Fill-in.** Marginalizing a pose with many shared points makes $\hat H$ dense over all keyframes that saw those points. Plan which observations to drop.
- **Bad starts.** The window is solved by a local method. A new keyframe with a bad pose, or new points with wrong depths, can pull the window into a wrong minimum. Use a robust loss and check the result.
- **Window size.** A short window gives more drift and less accuracy; a long window costs $O(W^3)$ for the reduced system per iteration. The size is a trade-off, tuned by experiment.

## Exercises

1. In the example, add a third measurement $x_2 = 4$ with the cost $(x_2 - 4)^2$ after $x_1$ is marginalized. Find the estimate of $x_2$ with the prior, and check that the full problem over $x_1$ and $x_2$ gives the same $x_2$. (Answer: minimize $\frac{1}{2}(x_2 - 3)^2 + (x_2 - 4)^2$, so $x_2 = 11/3$. The full problem gives the same, because all costs are linear least squares.)
2. A window has $W$ keyframes and $n$ points, and each point is seen by every keyframe. Show that one Gauss-Newton iteration with the Schur complement over the points costs $O(n W^2 + W^3)$, and compare with a dense solve, $O((n + W)^3)$.
3. Keyframes $1$ and $2$ share no point. Keyframe $m$ sees a point $p$ that keyframe $1$ also sees, and a point $q$ that keyframe $2$ also sees. Which new nonzero blocks does $\hat H$ get if you marginalize $m$ alone, and which if you marginalize $m$, $p$ and $q$? (Answer: marginalizing a variable connects all its neighbors. With $m$ alone, $p$ and $q$ become connected. With $m$, $p$ and $q$, keyframes $1$ and $2$ become connected.)

## References
