---
tag: B1XGPE
kind: problem
slug: inspection-localization
name: Localization for inspection
aliases:
- best-fit alignment to CAD
- part localization
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Find the rigid motion that places measured points best on the CAD surfaces, in least squares or in the minimax sense, before the deviations of the part are read.
prereqs: [rigid-body-transformation, kabsch-algorithm, point-projection-onto-a-surface]
see_also: [iterative-closest-point, point-to-plane-icp, point-cloud-registration, datum-reference-frame, three-two-one-locating-principle, hausdorff-distance, slippage-analysis, cad-based-inspection]
sources:
  - paper: doi:10.1109/34.121791
    title: Paul J. Besl and Neil D. McKay, A method for registration of 3-D shapes, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(2), 1992, 239 to 256
    locator: the iterative closest point algorithm, the proof that its mean squared error does not increase and converges, and its local minima
  - paper: doi:10.1107/S0567739476001873
    title: Wolfgang Kabsch, A solution for the best rotation to relate two sets of vectors, Acta Crystallographica Section A 32(5), 1976, 922 to 923
    locator: the rotation of least squared distance between two matched sets of vectors
  - paper: doi:10.1109/34.88573
    title: Shinji Umeyama, Least-squares estimation of transformation parameters between two point patterns, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(4), 1991, 376 to 380
    locator: the closed form by the singular value decomposition with the sign correction that excludes reflections, and its proof
  - paper: doi:10.1016/0262-8856(92)90066-C
    title: Yang Chen and Gérard Medioni, Object modelling by registration of multiple range images, Image and Vision Computing 10(3), 1992, 145 to 155
    locator: the registration that minimizes the distances from points to the tangent planes of the other surface
  - paper: doi:10.1109/70.134279
    title: C.-H. Menq, H.-T. Yau and G.-Y. Lai, Automated precision measurement of surface profile in CAD-directed inspection, IEEE Transactions on Robotics and Automation 8(2), 1992, 268 to 278
    locator: the localization of measured points to a CAD surface for profile inspection
  - paper: doi:10.1016/j.cad.2004.02.009
    title: Yadong Li and Peihua Gu, Free-form surface inspection techniques state of the art review, Computer-Aided Design 36(13), 2004, 1395 to 1417
    locator: the survey of localization methods for free-form surface inspection, least squares and minimax
  - url: https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-tolerancing
    title: ASME Y14.5-2018, Dimensioning and Tolerancing, The American Society of Mechanical Engineers, 2019
    locator: the standard as a whole (profile tolerances and datum reference frames); no clause is quoted
---

Localization for inspection is the problem of placing measured points of a part, given in the coordinates of the measuring machine, onto the nominal CAD model by a rigid motion, so that the deviation of each point from the model can be read. The motion is chosen to minimize the sum of the squared distances from the points to the model surfaces, or their maximum, or it is fixed by the datum features of the drawing. With known pairs of points the least-squares problem has a closed form, the [Kabsch algorithm](/kabsch-algorithm/). Without pairs it is solved by iterations such as the [iterative closest point](/iterative-closest-point/) method, which converge to a local minimum. The choice of the objective changes the result of a profile tolerance check. This page is the problem; the workflow around it is [CAD-based inspection](/cad-based-inspection/), and the evaluation of form, which needs no model, is [form error evaluation](/form-error-evaluation/).

## In plain words

A part lies somewhere on the table of a measuring machine. The machine records points on its surface, but it does not know how the part sits. Before we can say "this point is 0.1 mm too high", we must lay the measured points over the drawing of the part in the computer.

We look for the move, a turn and a shift with no stretching, that makes the points sit as close to the drawing as possible. "As close as possible" can mean the smallest total of the squared gaps, or the smallest worst gap. If we knew which spot on the drawing each point belongs to, one formula would give the best move. We do not, so we guess the spots as the nearest ones, find the best move for that guess, then guess again. Each round makes the fit no worse.

## Definition

The input is a set of measured points $q_1, \dots, q_n$ in $\mathbb{R}^3$, after the correction for the probe radius, and a nominal surface $M$, a set of trimmed patches of the CAD model. A rigid motion is $T(x) = R x + t$ with $R$ a rotation, $\det R = 1$, and $t \in \mathbb{R}^3$. Let $d(x, M)$ be the distance from $x$ to $M$, signed by the outer normal when $M$ is closed. The deviation of $q_i$ under $T$ is $d(T q_i, M)$.

**Least-squares localization.** Minimize $f(T) = \sum_{i} d(T q_i, M)^2$ over rigid motions.

**Minimax localization.** Minimize $g(T) = \max_{i} \lvert d(T q_i, M) \rvert$, the one-sided [Hausdorff distance](/hausdorff-distance/) from the moved points to $M$. A profile tolerance of total width $\tau$ with no datum is met by the sample exactly when $\min_T g(T) \le \tau / 2$.

**Datum localization.** The drawing names datum features in order of precedence. The motion is fixed by fitting the primary datum first, which removes up to three degrees of freedom, then the secondary, then the tertiary, as in the [datum reference frame](/datum-reference-frame/) and the [3-2-1 locating principle](/three-two-one-locating-principle/). Only the degrees of freedom the datums leave free are fitted to the toleranced surface.

The output is the motion $T$ and the deviations $d(T q_i, M)$.

## Variants

- **Known correspondences.** Each $q_i$ has a matching nominal point $p_i$, from targets or from a measurement plan that probes known points. Then $f$ becomes $\sum_i \lvert R q_i + t - p_i \rvert^2$, which the Kabsch closed form solves.
- **Point to plane.** Replace $d(x, M)$ by the distance to the tangent plane at the current closest point, as in [point-to-plane ICP](/point-to-plane-icp/) after Chen and Medioni. This lets the points slide along the surface and needs fewer iterations.
- **Restricted motions.** A part held in a fixture, or a feature whose datums fix some degrees of freedom, is fitted over a subgroup: translations only, rotation about one axis, and so on.
- **Weighted and robust fits.** Points on critical surfaces get larger weights, and outliers from dirt or burrs are trimmed or down-weighted.
- **Symmetric parts.** If a rigid motion maps $M$ onto itself, the problem has several optima, and if a continuous family of motions slides $M$ along itself, the motion is not determined in those directions. [Slippage analysis](/slippage-analysis/) finds these directions.
- **Registration of two clouds.** When the model is another point cloud, the problem is [point cloud registration](/point-cloud-registration/).

## Examples

**Least squares against minimax.** A flat profile surface is located by datums except for a shift $s$ along its normal. Four points have the normal deviations $0, 0, 0, 0.4$ mm before the shift. The least-squares shift is the mean, $s = 0.1$, which leaves the deviations $-0.1, -0.1, -0.1, 0.3$ and the largest one $0.3$. The minimax shift is the midrange, $s = 0.2$, which leaves $-0.2, -0.2, -0.2, 0.2$ and the largest one $0.2$. Under a profile tolerance of $0.5$ mm, a zone of $\pm 0.25$ mm, the least-squares placement rejects the part and the minimax placement accepts it. The drawing must state which placement applies.

**A symmetric outline.** The model is the boundary of the rectangle $[-2, 2] \times [-1, 1]$ in the plane, and the measured points are $48$ points spread evenly on that boundary, so the true motion is the identity. ICP started at a rotation of $85$ degrees reaches the identity, and started at $91$ degrees reaches the rotation by $180$ degrees, which fits the outline exactly as well: the error is $0$ at both. Started at exactly $90$ degrees, the pairs are symmetric, the Kabsch step returns the same rotation, and ICP stays there with the squared error $26.5$. In every run the error did not increase. These runs were measured with a small script, and they show why a part with symmetric surfaces needs a datum or a feature that breaks the symmetry.

## Known algorithms

**The Kabsch closed form, for known pairs.** For pairs $(q_i, p_i)$, the minimizer of $\sum_i \lvert R q_i + t - p_i \rvert^2$ is found as follows.

- *Translation.* For fixed $R$, the sum is a convex quadratic in $t$ with gradient $2 \sum_i (R q_i + t - p_i)$, so $t = \bar p - R \bar q$ with the centroids $\bar q, \bar p$. With $a_i = q_i - \bar q$ and $b_i = p_i - \bar p$ the sum becomes $\sum_i \lvert R a_i - b_i \rvert^2$.
- *Rotation.* Expand: $\sum_i \lvert R a_i - b_i \rvert^2 = \sum_i \lvert a_i \rvert^2 + \sum_i \lvert b_i \rvert^2 - 2 \operatorname{tr}(R H)$ with $H = \sum_i a_i b_i^{\mathsf T}$, since $\lvert R a_i \rvert = \lvert a_i \rvert$ and $b_i^{\mathsf T} R a_i = \operatorname{tr}(R a_i b_i^{\mathsf T})$. Let $H = U \Sigma V^{\mathsf T}$ be a [singular value decomposition](/singular-value-decomposition/). Then $\operatorname{tr}(R H) = \operatorname{tr}(V^{\mathsf T} R U \Sigma) = \sum_k Z_{kk} \sigma_k$ with $Z = V^{\mathsf T} R U$ orthogonal, so $\lvert Z_{kk} \rvert \le 1$ and $\operatorname{tr}(R H) \le \sum_k \sigma_k$. The bound is reached at $Z = I$, that is $R = V U^{\mathsf T}$.
- *The sign.* If $\det(V U^{\mathsf T}) = -1$, then $V U^{\mathsf T}$ is a reflection, and the best rotation is $R = V \operatorname{diag}(1, 1, -1) U^{\mathsf T}$ with $\sigma_3$ the smallest singular value. The proof that this is optimal among rotations is in Umeyama (1991).

The time is $\Theta(n)$ to form $H$ and $O(1)$ for the $3 \times 3$ decomposition.

**ICP, for unknown pairs.** Iterative closest point, after Besl and McKay (1992), alternates two steps: pair each moved point $T_k q_i$ with its closest point $c_i$ on $M$, then set $T_{k+1}$ to the rigid motion that minimizes $\sum_i \lvert T q_i - c_i \rvert^2$ by the Kabsch closed form. It repeats until the error stops decreasing.

*ICP never increases the error.* Let $E(T, c) = \sum_i \lvert T q_i - c_i \rvert^2$ for points $c_i \in M$. The pairing step chooses $c_i$ as the closest point to $T_k q_i$, so $E(T_k, c) = f(T_k)$. The Kabsch step gives $E(T_{k+1}, c) \le E(T_k, c)$. And $d(T_{k+1} q_i, M) \le \lvert T_{k+1} q_i - c_i \rvert$ for each $i$, since $c_i$ is one point of $M$, so $f(T_{k+1}) \le E(T_{k+1}, c) \le E(T_k, c) = f(T_k)$. The values $f(T_k)$ do not increase and are bounded below by $0$, so they converge. Besl and McKay prove this; the limit is in general a local minimum, and the result depends on the start. If the closest point is found only approximately, for example by Newton steps of [point projection onto a surface](/point-projection-onto-a-surface/), the proof still holds when the step keeps the previous partner of a point whenever the new one is farther.

**Point-to-plane steps.** Each step minimizes the squared distances to tangent planes, linearized in the small rotation, a $6 \times 6$ linear system. It converges in fewer iterations near the optimum but has no monotone guarantee without a line search.

**Minimax localization.** Linearize the motion as a small screw of three rotations and three translations, the [small displacement torsor](/small-displacement-torsor/), and the deviations as the distances to tangent planes. Then minimizing the largest deviation is a [linear program](/linear-programming-problem/) in seven variables. Repeated with updated planes and a bound on the step, this gives a local method, as in the free-form inspection literature that Li and Gu survey.

**A good start.** ICP and the minimax iterations need a start near the right motion: from the probing of datum features, from three or more known points, or from a coarse global search.

## Bounds

- **Known pairs.** $\Theta(n)$ time: every point must be read, and the closed form uses each point once.
- **ICP iterations.** One iteration costs $n$ closest-point queries. Against a fine mesh of $m$ triangles with a [k-d tree](/kd-tree/) or another spatial index this is about $O(n \log m)$ in practice; against trimmed spline patches it is $n$ point projections. The number of iterations has no useful bound in general, and it is large when the surface lets the points slide.
- **No global guarantee.** The least-squares and minimax objectives are not convex in the rotation, and ICP and the linearized methods stop at local minima or, as in the symmetric example, at stationary points. A certified global optimum needs a search over all rotations.

## Reductions

- **Known pairs reduce to the orthogonal Procrustes problem**, solved by one $3 \times 3$ singular value decomposition.
- **Least-squares localization without pairs reduces to a sequence of problems with pairs**, by the pairing step of ICP.
- **Minimax localization with a linearized motion reduces to linear programming** in seven variables, a fixed dimension, so each program takes $O(n)$ time by the methods for fixed dimension.
- **Form error is localization with a free reference.** When the nominal feature is a plane or a cylinder and its size and place are free, the minimax localization is the minimum zone problem of [form error evaluation](/form-error-evaluation/).

## Applications

- **Free-form surfaces.** Turbine blades, dies and car body panels are checked by profile tolerances after a best fit, and the deviations are shown as a color map on the model.
- **Measuring machine programs.** The part coordinate system of a measuring machine program is set by probing the datum features, a datum localization, before the rest of the points are taken.
- **Scans.** Optical and laser scans of a whole part are aligned to the CAD model by ICP after a coarse alignment, then compared surface by surface.
- **Reverse engineering.** Aligning a scan to a reference model, or two scans to each other, uses the same methods.

## References
