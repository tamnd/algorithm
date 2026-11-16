---
tag: R3GF26
kind: concept
slug: minimal-solver
name: Minimal solver
aliases:
- minimal problem
- minimal case solver
area: computer-vision/multiple-view-geometry
level: advanced
summary: "An algorithm that finds all models consistent with the fewest data that fix them, often by solving a polynomial system, as used inside RANSAC."
prereqs: [ransac, polynomial-root-finding]
see_also: [five-point-algorithm, seven-point-algorithm, p3p, ransac-iteration-bound, groebner-basis, resultant, companion-matrix-method, essential-matrix-characterization]
sources:
  - paper: doi:10.1109/TPAMI.2004.17
    title: "David Nister, An efficient solution to the five-point relative pose problem, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(6), 2004"
    locator: the five-point solver as a hypothesis generator inside RANSAC and the reduction to a polynomial of degree 10
  - paper: doi:10.1007/978-3-540-88690-7_23
    title: "Zuzana Kukelova, Martin Bujnak and Tomas Pajdla, Automatic generator of minimal problem solvers, European Conference on Computer Vision (ECCV), 2008"
    locator: the Groebner basis method for minimal problems and its automatic generation
  - paper: doi:10.1109/CVPR.2017.256
    title: "Viktor Larsson, Kalle Astrom and Magnus Oskarsson, Efficient solvers for minimal problems by syzygy-based reduction, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017"
    locator: the reduction of the elimination template size of action matrix solvers
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 11.1, Basic equations (the minimum case of seven point correspondences)"
---

A minimal solver is an algorithm that takes the smallest set of data that fixes a geometric model, up to a finite number of choices, and returns all models that fit those data exactly. The problem it solves is called a minimal problem. Examples are the [seven-point algorithm](/seven-point-algorithm/) for the fundamental matrix, the [five-point algorithm](/five-point-algorithm/) for the essential matrix and [P3P](/p3p/) for the pose of a calibrated camera. Minimal solvers are the hypothesis generators of [RANSAC](/ransac/): the fewer data a sample needs, the fewer samples are needed to find one without outliers. Most of them reduce to a system of polynomial equations, and the craft is to solve that system fast and stably.

## In plain words

A model such as the motion between two cameras has a fixed number of unknown numbers. Each matched point gives some equations. When the number of equations is just enough, the model is fixed, but often not uniquely: the equations are not linear, so there can be a few answers that all fit. A minimal solver finds all of them. It is used where the data contain many wrong matches. A robust method picks a few matches at random, asks the minimal solver for all models that fit them, and checks each model against the rest. Small samples are much more likely to be free of wrong matches, so the minimal number matters a lot.

## The idea

**Counting.** Let the model have $d$ degrees of freedom, and let each datum give $k$ independent equations. A sample of $s$ data with $sk = d$ gives as many equations as unknowns. Over the complex numbers such a system has, in general position, a finite number $N$ of solutions, which is fixed by the problem; it is called the degree of the problem. The real solutions are a subset whose size depends on the data. If $sk > d$, the problem is overdetermined and exact data have one solution, but noisy data have none, so a least squares method such as the [eight-point algorithm](/eight-point-algorithm/) is used instead.

**From data to polynomials.** Most solvers in multiple view geometry follow the same plan.

1. Write the constraints that are linear in the unknowns of the model, and find their null space. For the fundamental matrix, seven matches leave a pencil $F_2 + a(F_1 - F_2)$; for the essential matrix, five matches leave a four-dimensional space.
2. Put the null space into the nonlinear constraints of the model: $\det F = 0$, or the cubic equations of the [characterization of essential matrices](/essential-matrix-characterization/).
3. Solve the resulting polynomial system in the few remaining unknowns.
4. Map each real solution back to a model, and drop those that break other conditions, such as [cheirality](/cheirality/).

**Ways to solve the polynomial system.**

- **One variable.** If the system reduces to one polynomial, its roots can be found by a [companion matrix](/companion-matrix-method/), by [Sturm sequences](/sturm-sequence/) and bisection, or in closed form up to degree 4. The seven-point and P3P solvers are of this kind.
- **Hidden variable.** Treat one unknown as a parameter, write the system as a matrix in the other monomials, and ask for its determinant to vanish. This is a [resultant](/resultant/) method; Nister's five-point solver uses it to get a polynomial of degree 10.
- **Gröbner basis and action matrix.** Compute a [Gröbner basis](/groebner-basis/) for the problem once, offline, with exact numbers. From it build a fixed elimination template: a sparse matrix that is filled with the data, reduced by Gaussian elimination, and gives a matrix whose eigenvalues are the solutions. Stewenius, Engels and Nister (2006) and Kukelova, Bujnak and Pajdla (2008) made this a general method, and the latter generate such solvers automatically.
- **Homotopy continuation.** Track the solutions of a known start system as it is deformed into the system of the data. It is general but slower, and is used mostly to study new problems.

**What makes a solver good.** It must return every real solution, so that the true model is not missed. It must be fast, because RANSAC calls it thousands of times. It must be stable in [floating point](/floating-point-model/): large elimination templates and near-double roots lose digits, and a short Newton polish at the end often helps. And it should detect degenerate samples, such as points on one plane, and reject them.

## Examples

The table lists some standard minimal problems. The last column is the number of samples that RANSAC needs to find one sample without outliers with probability 0.99 when half of the data are outliers, from the [iteration bound](/ransac-iteration-bound/) $N = \lceil \log(1 - p)/\log(1 - w^s) \rceil$.

| problem | sample $s$ | complex solutions | samples for $p = 0.99$, $w = 0.5$ |
|---|---|---|---|
| [P3P](/p3p/), camera pose from 3 points | 3 | up to 4 | 35 |
| [homography](/homography-estimation/), 4 point pairs | 4 | 1 (linear) | 72 |
| [essential matrix](/five-point-algorithm/), 5 point pairs | 5 | 10 | 146 |
| [fundamental matrix](/seven-point-algorithm/), 7 point pairs | 7 | 3 | 588 |
| fundamental matrix by the eight-point algorithm, not minimal | 8 | 1 (linear) | 1177 |

**Five-point example.** For five matches from the running example of the [eight-point algorithm](/eight-point-algorithm/) the five-point solver finds 4 real essential matrices, and one of them is the true one. Points that the other matches put behind a camera, or a poor fit to the other matches, rule out the other three.

**Seven-point example.** For 40 random scenes of seven points, the seven-point solver gave three real solutions 34 times and one solution 6 times. All candidates fit the seven matches exactly, so only other matches can tell them apart.

**Non-example.** Triangulation of a point from two views is not a minimal problem: two rays give four equations for three unknowns, and with noise they do not meet. It is solved by least squares, as in [linear triangulation](/linear-triangulation/).

## Where it is used

- **Robust estimation.** Inside [RANSAC](/ransac/), [LO-RANSAC](/lo-ransac/), [MSAC](/msac/), [PROSAC](/prosac/) and [preemptive RANSAC](/preemptive-ransac/), each sample is passed to a minimal solver, and every solution is scored.
- **Visual odometry and SLAM.** The five-point solver gives the relative pose between frames, as in [Nister's visual odometry](/nister-visual-odometry/), and P3P gives the pose against a map.
- **Structure from motion.** [Incremental structure from motion](/incremental-structure-from-motion/) starts from a two-view pair found by a minimal solver and adds cameras with P3P.
- **Calibration.** Minimal solvers with unknown focal length or lens distortion are used when the cameras are only partly calibrated.
- **Initial values.** A minimal solution on the inliers is a good starting point for [bundle adjustment](/bundle-adjustment/).

## References
