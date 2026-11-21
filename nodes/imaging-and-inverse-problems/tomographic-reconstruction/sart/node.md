---
tag: 9QD7WM
kind: algorithm
slug: sart
name: Simultaneous algebraic reconstruction technique
aliases:
- SART
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: Update the image by the normalized back projection of the residuals of one whole projection angle at a time, between ART and SIRT.
model: real-ram
complexity:
  vars: {n: "the side of the n x n image", a: "the number of projection angles", d: "the number of detector bins", K: "the number of sweeps"}
  time: {per_view: "O(d n)", per_sweep: "O(a d n)", total: "O(K a d n)"}
  space: {extra: "O(a d + n^2)"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: true, order_dependent: true, block_iterative: true}
history:
  year: 1984
  people: [Anders H. Andersen, Avinash C. Kak]
  note: Andersen and Kak combined the fast convergence of ART with the smooth images of SIRT by correcting the image once per projection angle, with all rays of the angle at once.
prereqs: [sirt, kaczmarz-method]
see_also: [sirt, siddon-algorithm, joseph-projector, distance-driven-projector, osem, semi-convergence, asd-pocs, landweber-iteration]
sources:
  - paper: "A. H. Andersen and A. C. Kak, Simultaneous algebraic reconstruction technique (SART): a superior implementation of the ART algorithm, Ultrasonic Imaging 6(1), 1984, 81 to 94"
    locator: the update per projection angle with the row and column normalization (general locator)
  - paper: doi:10.1109/TIP.2003.815295
    title: Ming Jiang and Ge Wang, Convergence of the simultaneous algebraic reconstruction technique (SART), IEEE Transactions on Image Processing 12(8), 2003
    locator: pp. 957 to 961 (convergence of the form that uses all rays in one step, to a weighted least squares solution)
  - paper: "P. P. B. Eggermont, G. T. Herman and A. Lent, Iterative algorithms for large partitioned linear systems, with applications to image reconstruction, Linear Algebra and its Applications 40, 1981, 37 to 67"
    locator: block-iterative methods that correct the image once per block of equations (general locator)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 7, algebraic reconstruction algorithms (ART, SIRT and SART)
---

SART reconstructs an image from the data $y$ of the discrete model $y = A x + e$ of tomography. Here $x \in \mathbb{R}^N$ holds the $N = n^2$ pixel values, $A$ is a sparse nonnegative $m \times N$ matrix, and its rows are grouped by projection angle into $a$ views $V_1, \dots, V_a$. For one view $v$, SART computes the residuals of all rays of the view, divides each by the sum of its row, back-projects them, divides each pixel by the sum of its column over the rays of that view, and adds the result. Then it moves to the next view. One pass through all views is a sweep, and it costs the same as one iteration of [SIRT](/sirt/): one forward and one back projection of all rays. It sits between [ART](/kaczmarz-method/), which corrects after each ray, and SIRT, which corrects after all rays. In practice it reaches a given error in far fewer passes than SIRT, and its images are smoother than those of ART.

## In plain words

A CT scan measures the object from many angles, and at each angle a row of detectors records many parallel rays. SART takes the angles one at a time. For the current angle, it computes what each ray would measure through the current image and compares it with the true measurement. It spreads the error of each ray back along the ray, divided by the length of the ray. Each pixel then takes the average correction of the rays of this angle that cross it, times a factor $\lambda$. Then SART goes to the next angle with the improved image.

Since the image changes after each angle and not only after all angles, the next angle already sees a better image. That is why SART needs fewer passes than SIRT. Since all rays of an angle act together, the correction is smoother than the ray by ray correction of ART.

## The problem

Given a nonnegative $m \times N$ matrix $A$ whose rows are split into views $V_1, \dots, V_a$, and data $y \in \mathbb{R}^m$, find $x$ with $A x \approx y$. Write $A_v$ and $y_v$ for the rows and data of view $v$, $r_i = \sum_j a_{ij}$ for the row sums, and $c_{vj} = \sum_{i \in V_v} a_{ij}$ for the column sums inside view $v$. Let $R_v = \operatorname{diag}(1/r_i)$ over the rays of the view, and $C_v = \operatorname{diag}(1/c_{vj})$, with $1/0 := 0$. The step for view $v$ is
$$x \leftarrow x + \lambda\, C_v A_v^T R_v\, (y_v - A_v x).$$
With exact consistent data, the target is a solution of $A x = y$. With noisy data, the target is a good early iterate, as for every iterative method of this kind (see [semi-convergence](/semi-convergence/)).

## The algorithm

```pseudo id=main
SART(A, y, V_1..V_a, λ, K, x0)            ▷ 0 < λ < 2
L1  r_i ← Σ_j a_ij for every ray i
L2  x ← x0
L3  for k ← 1 to K do                      ▷ one sweep
L4      for each view v in the chosen order do
L5          e_i ← (y_i - ⟨a_i, x⟩) / r_i for each ray i in V_v
L6          g ← A_v^T e;  c_v ← A_v^T 1      ▷ back projection and column sums of the view
L7          x_j ← x_j + λ g_j / c_vj for each pixel j with c_vj > 0
L8          (optional) x_j ← max(x_j, 0)
L9  return x
```

Line L5 is the forward projection of one view, and line L6 its back projection. A pixel that no ray of the view meets has $c_{vj} = 0$ and does not change in that step. The view order matters. A common choice visits the angles in an order that keeps successive angles far apart, so that their corrections are close to independent; the default of the code is the natural order. Line L8 keeps the image nonnegative.

## Example

Take a $2 \times 2$ image $x = (x_0, x_1, x_2, x_3)$ in row-major order with the true values $(1, 2, 3, 5)$, and three views with weights 0 or 1:

| view | ray | pixels | $y_i$ | $r_i$ |
|---|---|---|---|---|
| rows | row 0 | $x_0, x_1$ | 3 | 2 |
| rows | row 1 | $x_2, x_3$ | 8 | 2 |
| columns | column 0 | $x_0, x_2$ | 4 | 2 |
| columns | column 1 | $x_1, x_3$ | 7 | 2 |
| diagonal | ray 1 | $x_2$ | 3 | 1 |
| diagonal | ray 2 | $x_0, x_3$ | 6 | 2 |
| diagonal | ray 3 | $x_1$ | 2 | 1 |

Each pixel lies on exactly one ray of each view, so $c_{vj} = 1$ for all views and pixels. Start from $x = 0$ with $\lambda = 1$ and the order rows, diagonal, columns:

| step | residuals divided by $r_i$ | $x$ after the step |
|---|---|---|
| rows | $3/2,\ 4$ | $(3/2,\ 3/2,\ 4,\ 4)$ |
| diagonal | $-1,\ 1/4,\ 1/2$ | $(7/4,\ 2,\ 3,\ 17/4)$ |
| columns | $-3/8,\ 3/8$ | $(11/8,\ 19/8,\ 21/8,\ 37/8)$ |
| rows | $-3/8,\ 3/8$ | $(1,\ 2,\ 3,\ 5)$ |

For example, in the diagonal step the ray through $x_0$ and $x_3$ measures $3/2 + 4 = 11/2$ against $6$, so it adds $(6 - 11/2)/2 = 1/4$ to both pixels. SART finds the exact image in the first step of the second sweep and then stays there. With the order rows, columns, diagonal it is exact after the first sweep. With $\lambda = 1/2$ and the natural order, the first sweep gives $(49/32, 61/32, 85/32, 113/32)$, and 60 sweeps reach the true image to $10^{-12}$. The tests check all these values with `fractions.Fraction`.

A larger case: a disk of radius 0.6 on a $16 \times 16$ grid, 12 angles in $[0, \pi)$, 23 bins, the pixel-driven matrix of the shared helper, and the natural order. These are measurements of this setup. With exact data and $\lambda = 1$, the relative error $\|x_k - x\|/\|x\|$ is $0.36$ after one sweep, $0.11$ after 10 and $0.091$ after 40. On the same data, SIRT has the error $0.63$ after one iteration, $0.24$ after 10, $0.12$ after 100 and $0.094$ after 400, and one SIRT iteration costs the same as one sweep. With Gaussian noise of standard deviation 2 percent of the largest ray sum (seed 5), SART with $\lambda = 1$ has its smallest error $0.191$ at sweep 6, and the error grows to $0.248$ at sweep 40. With $\lambda = 1/4$ the smallest error is $0.182$ at sweep 31, and SIRT reaches $0.181$ at iteration 101. A smaller $\lambda$ gives a slower but flatter curve, which makes the stopping index less critical.

## Correctness

The proofs below need one assumption: all views have the same column sums, $C_v = C$ for every $v$. The pixel-driven matrix of the helper satisfies it exactly, because each pixel splits its whole weight $h^2/w$ among the bins of each view (a test checks this). Strip-integral weights, where $a_{ij}$ is the area of pixel $j$ inside strip $i$ divided by the strip width, satisfy it too when the strips of a view cover the image. Put $B_v = R_v^{1/2} A_v C^{1/2}$, $b_v = R_v^{1/2} y_v$ and $x = C^{1/2} z$. The step becomes
$$z \leftarrow z + \lambda B_v^T (b_v - B_v z),$$
a Landweber step on the block $v$, and $\|B_v\| \le 1$ by the Cauchy-Schwarz argument of [SIRT](/sirt/) applied to the rows of the view. These are theorems, proved in [proofs/correctness.md](proofs/correctness.md):

- **One step is SIRT.** If there is a single view that holds all rays, one sweep is exactly one SIRT iteration (a test checks this).
- **Consistent data.** If $A x = y$ has a solution and $0 < \lambda < 2$, the iterates converge, for any order, to the solution closest to $x_0$ in the norm $\sum_j c_j v_j^2$. The convergence is linear per sweep. The key fact is that each step lowers $\|z - \hat z\|^2$ by at least $\lambda(2 - \lambda)\|B_v (z - \hat z)\|^2$.
- **Inconsistent data.** For any data and $0 < \lambda < 2$, the iterates at the ends of the sweeps converge. Inside a sweep they follow a cycle of $a$ points. The limit depends on $\lambda$ and on the order, and in general it is not the weighted least squares solution of SIRT.

In a test with nine random rays and four pixels (seed 3), the distance from the limit to the weighted least squares solution is $0.17$, $0.11$, $0.054$, $0.021$ and $0.011$ for $\lambda = 1$, $1/2$, $1/4$, $1/10$ and $1/20$: about proportional to $\lambda$. This is a measurement. For ART, Censor, Eggermont and Gordon showed in 1983 that the limit tends to a weighted least squares solution as the relaxation goes to 0. We do not prove the block version here.

When the column sums differ from view to view, the steps act in different metrics, and the proof above does not apply. Jiang and Wang (2003) proved convergence for the form that takes all views in one step, from any start, to a weighted least squares solution, when $A \ge 0$. That form is SIRT.

## Complexity

In the real-RAM model, with $a$ views of $d$ rays each and an $n \times n$ image, a ray-driven matrix has $O(n)$ nonzero entries per ray. Line L5 reads the entries of the view once and line L6 reads them once more, so one view costs $O(d n)$ time and one sweep costs $O(a d n)$, the same as one SIRT iteration. Line L7 touches only the pixels the view meets. Line L1 takes one pass over $A$. The extra space is $O(a d)$ for the row sums and $O(n^2)$ for the dictionaries of one view; the code computes the column sums of a view on the fly instead of storing them for all views, which would cost $O(a n^2)$. With a matrix-free projector, count one projection and one back projection of one view per step.

The number of sweeps is the regularization parameter, as for SIRT. Its best value depends on the noise, on $\lambda$ and on the order. It is found by a stopping rule, not by a formula.

## Properties

- **Block iterative.** The image changes after each view, so later views see the corrections of earlier views. This is the source of the speed over SIRT.
- **Order dependent.** The iterates depend on the view order. With consistent data and common column sums, the limit does not.
- **Smooth corrections.** All rays of a view act together, and the division by $c_{vj}$ averages their corrections at each pixel. The streaks that ART can leave when it corrects ray by ray are weaker.
- **Not a fixed-point method for noisy data.** With fixed $\lambda$ and inconsistent data, the iterates cycle through $a$ points and do not converge to a single image.
- **Parallel inside a view.** The rays of one view are independent, so a view step is parallel over its rays and its pixels. The views are sequential.

## Variants and improvements

- **Ordered subsets.** Group the views into subsets and apply the step to one subset at a time. One subset holding all views is SIRT; one view per subset is SART. The [OSEM](/osem/) method does the same with the multiplicative update of the maximum likelihood method for emission tomography.
- **Diminishing relaxation.** Let $\lambda$ decrease from sweep to sweep. The cycle of the inconsistent case then shrinks, and the iterates can approach a weighted least squares solution. The step rule has to make $\sum_k \lambda_k$ diverge.
- **Bilinear or Joseph weights.** Andersen and Kak computed the weights with bilinear interpolation along each ray. Any projector works: [Siddon](/siddon-algorithm/), [Joseph](/joseph-projector/) or [distance-driven](/distance-driven-projector/).
- **With a prior.** Alternate SART sweeps with a total variation step, as [ASD-POCS](/asd-pocs/) does, to reconstruct piecewise constant images from few views.

## When to use it

Use SART when an algebraic method is needed (few views, a limited angle, noise, or a nonstandard geometry) and convergence per pass matters. It is the usual data step of iterative CT codes that work view by view. Use [SIRT](/sirt/) when the result must not depend on the order of the views, when all rays must be processed in parallel, or when a fixed-point analysis is needed. For complete data with many angles, [filtered back-projection](/filtered-back-projection/) is much cheaper.

## Pitfalls

- **Expecting a single limit with noise.** With fixed $\lambda$ and inconsistent data, SART does not converge to one image. Stop early, or let $\lambda$ decrease.
- **Bad view orders.** Consecutive views at nearby angles carry nearly the same information, so the second step adds little to the first. Interleave the angles. This is a heuristic; the code does not measure it.
- **Zero sums.** A ray outside the image has $r_i = 0$, and a pixel outside all rays of a view has $c_{vj} = 0$. Skip them, or the division fails.
- **An unmatched back projector.** Line L6 must use the transpose of the matrix of line L5. Otherwise the step is not a Landweber step for any block, and $\|B_v\| \le 1$ does not hold.
- **Too large $\lambda$.** Each block step needs $\lambda < 2$. Values near 2 converge slowly on the components with the largest singular value and amplify noise in early sweeps.

## Implementations

The Python code takes the sparse rows of $A$ as (column, weight) pairs and the views as lists of row indices; `views_by_angle` gives the views of the shared helper `imgkit.parallel_beam_matrix`. It works with float or `fractions.Fraction` data. The tests check the worked example exactly, the relaxed example, that one view of all rays is one SIRT step, the limit for consistent data against the projection of $x_0$ onto the solution set, the convergence of the sweep ends for inconsistent data and the dependence of the limit on $\lambda$, the equal column sums of the helper matrix, a disk phantom against SIRT, and the nonnegativity option.

## History

Gordon, Bender and Herman published ART in 1970, and Gilbert published SIRT in 1972. ART converged fast but gave noisy images with streaks; SIRT gave smooth images but converged slowly. Andersen and Kak proposed SART in 1984 in Ultrasonic Imaging as a compromise: one correction per projection angle, with bilinear weights along the rays. Block-iterative methods for partitioned linear systems had been studied by Eggermont, Herman and Lent in 1981. Jiang and Wang proved the convergence of the form that uses all rays in one step in 2003. SART became a standard data step of iterative CT, often accelerated with ordered subsets and run on GPUs.

## References
