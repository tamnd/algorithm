---
tag: DPEQW9
kind: problem
slug: phase-unwrapping
name: Phase unwrapping
aliases:
- 2D phase unwrapping
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: core
summary: "Recover a continuous phase from values known only modulo 2 pi, as in interferometric SAR, MRI field maps and optical interferometry."
model: real-ram
prereqs: [analytic-signal]
see_also: [goldstein-branch-cut, least-squares-phase-unwrapping, sar-interferometry, quantitative-susceptibility-mapping, digital-holography-reconstruction, min-cost-flow-problem, np-hard, kasai-autocorrelation-estimator]
sources:
  - paper: doi:10.1364/AO.21.002470
    title: "Kazuyoshi Itoh, Analysis of the phase unwrapping algorithm, Applied Optics 21(14), 1982, 2470"
    locator: "one-dimensional unwrapping by summing wrapped differences and the condition that the true differences lie in (-pi, pi) (general locator)"
  - paper: doi:10.1029/RS023i004p00713
    title: "Richard M. Goldstein, Howard A. Zebker and Charles L. Werner, Satellite radar interferometry: two-dimensional phase unwrapping, Radio Science 23(4), 1988, 713"
    locator: "residues and branch cuts in two dimensions (general locator)"
  - paper: doi:10.1364/JOSAA.11.000107
    title: "Dennis C. Ghiglia and Louis A. Romero, Robust two-dimensional weighted and unweighted phase unwrapping that uses fast transforms and iterative methods, Journal of the Optical Society of America A 11(1), 1994, 107"
    locator: "the least squares formulation and its solution by fast cosine transforms (general locator)"
  - paper: doi:10.1109/36.673674
    title: "Mario Costantini, A novel phase unwrapping method based on network programming, IEEE Transactions on Geoscience and Remote Sensing 36(3), 1998, 813 to 821"
    locator: "the minimum L1 problem as a minimum cost flow problem (general locator)"
  - paper: doi:10.1364/JOSAA.17.000401
    title: "Curtis W. Chen and Howard A. Zebker, Network approaches to two-dimensional phase unwrapping: intractability and two new algorithms, Journal of the Optical Society of America A 17(3), 2000, 401"
    locator: "the NP-hardness of the minimum L0 problem (general locator)"
  - paper: doi:10.1364/JOSAA.14.002692
    title: "Thomas J. Flynn, Two-dimensional phase unwrapping with minimum weighted discontinuity, Journal of the Optical Society of America A 14(10), 1997, 2692"
    locator: "the minimum weighted discontinuity problem and an exact method for it (general locator)"
  - book: isbn:9780471249351
    title: "Dennis C. Ghiglia and Mark D. Pritt, Two-Dimensional Phase Unwrapping: Theory, Algorithms, and Software, Wiley, 1998"
    locator: "the chapters on path-following methods and on minimum-norm methods"
---

Phase unwrapping is the problem of recovering a phase $\varphi$ from its wrapped values $\psi = W(\varphi)$, which are known only modulo $2\pi$. Many sensors measure a complex number and keep only its angle, as in the [analytic signal](/analytic-signal/). Examples are an interferogram in [SAR interferometry](/sar-interferometry/), a field map in MRI, a fringe pattern in optical interferometry and a hologram. The angle lies in $(-\pi, \pi]$, and the physics is in the continuous phase. In one dimension the problem is easy when the samples are dense enough: sum the wrapped differences (Itoh 1982). In two dimensions the wrapped differences are in general not the gradient of any image. The points where they fail to be are the residues, and every method must choose where to put the error. Least squares is fast but not congruent. Minimum L1 is a [minimum cost flow problem](/min-cost-flow-problem/). Minimum L0, the fewest wrong edges, is [NP-hard](/np-hard/) (Chen and Zebker 2000).

## In plain words

A clock hand shows the minutes but not the hour. If you look at the clock often enough, you can count the turns and know the full time. If you look too rarely, you miss turns and cannot tell.

A wrapped phase is the same: every pixel shows the angle of a clock hand, and the task is to count the turns. Neighbouring pixels usually differ by less than half a turn, so you add up the small steps. In an image there are many paths between two pixels. Noise and real jumps make some paths count one turn more than others. Phase unwrapping is the art of choosing the turns so that the result is smooth and the few errors are in the right places.

## Definition

**Wrapping.** $W(x) = x - 2\pi k$ with the integer $k$ that puts the value in $(-\pi, \pi]$. A function $\varphi$ is congruent to $\psi$ if $\varphi - \psi \in 2\pi\mathbb{Z}$ at every sample.

**Input.** Wrapped values $\psi(v) \in (-\pi, \pi]$ on the vertices $v$ of a graph, usually a line of $n$ samples or a grid of $m \times n$ pixels with $N = mn$, and optionally a weight $w_e \ge 0$ for each edge $e$ (a quality map or a coherence).

**Wrapped gradient.** For an edge $e = (u, v)$, $g_e = W(\psi(v) - \psi(u))$.

**Residues.** On a grid, the sum of $g$ around a $2 \times 2$ square is $2\pi q$ with $q \in \{-1, 0, 1\}$. A square with $q \ne 0$ is a residue. If there are no residues, $g$ is the gradient of a unique image up to a constant, and that image is congruent to $\psi$.

**Output.** A function $\varphi$, usually required to be congruent to $\psi$, whose differences match $g$ in some sense:

$$\min_{\varphi} \sum_e w_e\, \big|\varphi(v) - \varphi(u) - g_e\big|^p, \qquad p \in \{0, 1, 2\},$$

where for $p = 0$ the term counts the edges with a nonzero error. For $p = 0$ and $p = 1$ the minimum is usually taken over congruent $\varphi$ only, so that the unknowns are integers (see Reductions). For $p = 2$ the minimum is taken over all real images, and the minimizer is in general not congruent.

**Itoh's condition.** If the true phase satisfies $|\varphi(v) - \varphi(u)| < \pi$ on every edge, then $g_e = \varphi(v) - \varphi(u)$, there are no residues, and summing $g$ along any path from a fixed vertex gives $\varphi$ up to one multiple of $2\pi$.

## Variants

- **One dimension.** A single sum of wrapped differences, exact under Itoh's condition.
- **Two and three dimensions.** Images and volumes, with residues on squares (and residue lines in 3D).
- **Weighted and masked.** Weights from a quality map or from the coherence lower the influence of noisy edges, and masks remove pixels with no signal.
- **Congruent or not.** Path-following and network flow methods return congruent results. Least squares returns a smooth result that is not congruent where there are residues.
- **Temporal and multi-frequency unwrapping.** Several measurements with different wavelengths, or a time series, resolve the turns pixel by pixel without spatial paths.
- **Absolute phase.** All formulations fix $\varphi$ only up to one constant $2\pi k$ per connected region. The absolute value needs outside information, for example a control point.

## Examples

**One dimension.** The true phase $(0, 2, 4, 6, 8)$ wraps to $\psi = (0, 2, -2.283, -0.283, 1.717)$. The wrapped differences are $(2, 2, 2, 2)$, because $W(-4.283) = 2.000$. Their running sum gives back $(0, 2, 4, 6, 8)$. With the true phase $(0, 4)$, the step of 4 is more than $\pi$: $\psi = (0, -2.283)$, and the sum gives $(0, -2.283)$. The two phases cannot be told apart from the data.

**A residue.** Take the $2 \times 2$ image $\psi = \begin{pmatrix} 0 & 2 \\ -2 & 2.5 \end{pmatrix}$. The wrapped differences around the square are $2$, $0.5$, $1.783$ and $2$ in the direction of the loop, with the sum $2\pi$: one residue with $q = +1$. No image has these four differences. A congruent solution must change one of them by $2\pi$, so the minimum L0 cost is 1. The least squares solution instead shares the error equally: each difference is wrong by $\pi/2$, and the result is not congruent. Both answers are shown on the pages of [Goldstein's algorithm](/goldstein-branch-cut/) and [least squares unwrapping](/least-squares-phase-unwrapping/).

**A vortex.** The angle $\operatorname{atan2}(i - 1.5, j - 1.5)$ on a $4 \times 4$ grid has a residue at the central square. Every path around it gains one full turn, so no continuous phase exists there. A cut from the centre to the border is the honest answer.

## Known algorithms

| Method | Formulation | Congruent | Time |
|---|---|---|---|
| Itoh summation | 1D, exact under Itoh's condition | yes | $O(n)$ |
| [Goldstein branch cuts](/goldstein-branch-cut/) | cuts between residues, then flood fill | yes | $O(N + R b^3 + R \sqrt{N})$ |
| Quality guided flood fill | path order from a quality map | yes | $O(N \log N)$ |
| [Least squares](/least-squares-phase-unwrapping/) (Ghiglia and Romero 1994) | $p = 2$, DCT Poisson solver | no | $O(N \log N)$ |
| Weighted least squares | $p = 2$ with weights, preconditioned conjugate gradients or multigrid | no | iterative |
| Minimum cost flow (Costantini 1998) | $p = 1$ | yes | polynomial |
| Minimum weighted discontinuity (Flynn 1997) | weighted count of discontinuities | yes | iterative |
| Statistical cost network flow | costs from a model of SAR data | yes | heuristic |

Here $R$ is the number of residues and $b$ the box radius of Goldstein's method.

## Bounds

- **Lower bound.** Every method reads all $N$ samples, so $\Omega(N)$ time.
- **One dimension.** $O(n)$, and the answer is unique up to $2\pi k$ under Itoh's condition (theorem).
- **No residues.** $O(N)$ by any path-following method. Path-following, least squares and minimum L1 all return the sum of $g$ along paths, up to a constant (theorem).
- **$p = 2$.** $O(N \log N)$ with a fast DCT for the unweighted problem (theorem).
- **$p = 1$.** Polynomial, by a minimum cost flow (Costantini 1998).
- **$p = 0$.** NP-hard (Chen and Zebker 2000). Greedy cut placement such as Goldstein's is not optimal: a $3 \times 4$ example on its page needs 3 wrong edges where 2 are enough.

## Reductions

**Minimum L1 to minimum cost flow.** Write a congruent result as $\varphi(v) - \varphi(u) = g_e + 2\pi n_e$ with integers $n_e$. A function $\varphi$ with these differences exists if and only if, around every $2 \times 2$ square, the sum of $g_e + 2\pi n_e$ is zero, that is $\sum_{\text{loop}} n_e = -q$. On the dual graph, whose nodes are the squares and one outside node, and whose arcs cross the primal edges, this says that $n$ is a flow whose net outflow at each square is $-q$. So the residues are supplies and demands, the outside node balances them, and the cost $\sum_e w_e |2\pi n_e|$ is linear in the flow on each arc in each direction. Minimum cost flow has integral optimal solutions, which gives integer $n_e$ (Costantini 1998).

**Minimum L0 and cuts.** For $p = 0$ the cost counts the arcs with nonzero flow. That is a fixed charge flow problem, and Chen and Zebker (2000) proved it NP-hard. Branch cut methods such as Goldstein's are heuristics for it: the edges with $n_e \ne 0$ lie on the cuts.

**Least squares to the Poisson equation.** For $p = 2$ the normal equations are the discrete [Poisson equation](/poisson-equation/) with Neumann boundary conditions, with the divergence of $g$ on the right hand side (Ghiglia and Romero 1994).

## Applications

- **[SAR interferometry](/sar-interferometry/).** The interferometric phase measures height or ground motion. It must be unwrapped before it can be turned into metres.
- **MRI.** Field maps, phase contrast velocity, water and fat separation and [quantitative susceptibility mapping](/quantitative-susceptibility-mapping/) all start from a wrapped phase.
- **Optical metrology.** Fringe projection profilometry, interferometric testing of surfaces and [digital holography](/digital-holography-reconstruction/).
- **Doppler ultrasound.** The [Kasai estimator](/kasai-autocorrelation-estimator/) returns a velocity modulo the aliasing limit $c\, \mathrm{PRF}/(4 f_0)$. Aliased colour Doppler images are unwrapped in space or in time.
- **Adaptive optics.** Wavefront sensors that measure wrapped phase differences.

## References
