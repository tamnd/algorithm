---
tag: HGJYE8
kind: problem
slug: traveltime-tomography
name: Traveltime tomography
aliases:
- seismic tomography
area: imaging-and-inverse-problems/seismic-imaging
level: core
summary: "Recover the velocity of the subsurface from the first-arrival times of waves along many source-receiver paths, a nonlinear inverse problem that is ill-posed where the rays are few."
model: real-ram
prereqs: [eikonal-equation, least-squares-problem, forward-operator]
see_also: [geiger-method, radon-transform, kaczmarz-method, sirt, lsqr, resolution-matrix, fast-marching-method, full-waveform-inversion]
sources:
  - paper: doi:10.1029/JB081i023p04381
    title: Keiiti Aki and W. H. K. Lee, Determination of three-dimensional velocity anomalies under a seismic array using first P arrival times from local earthquakes, 1. A homogeneous initial model, Journal of Geophysical Research 81(23), 1976, 4381 to 4399
    locator: the linearized inversion of local first P arrival times for velocity anomalies in blocks together with the hypocenters
  - paper: doi:10.1029/JB082i002p00277
    title: Keiiti Aki, Anders Christoffersson and Eystein S. Husebye, Determination of the three-dimensional seismic structure of the lithosphere, Journal of Geophysical Research 82(2), 1977, 277 to 296
    locator: the block model, the linear inversion of teleseismic travel time residuals at an array by damped least squares, and the resolution and error of the result
  - book: isbn:9780521708425
    title: Peter M. Shearer, Introduction to Seismology, second edition, Cambridge University Press, 2009
    locator: Chapter 5 (inversion of travel time data)
---

Traveltime tomography recovers the velocity of the earth from the times that waves take to travel between many sources and receivers. Each time is an integral of the slowness, the inverse of the velocity, along the ray from the source to the receiver; the ray itself depends on the slowness, so the problem is nonlinear. Linearized around a reference model, it is a large, sparse linear system, close to the [Radon transform](/radon-transform/) of medical CT but with curved rays and with the rays only where sources and receivers can be placed. Where the rays are few, or all go in the same direction, parts of the model are not seen at all, and the problem is ill-posed and needs regularization. It is used at all scales, from the mantle with earthquakes, to the crust with explosions, to the near surface and between wells in exploration.

## In plain words

Send waves from many places to many listeners and time each trip. A trip through slow rock takes longer than one through fast rock. Each time tells us only the total delay along one path, not where on the path the slow rock is. With many paths that cross each other in many directions, the slow places can be found, as a CT scanner finds bones from many X-ray shots. The hard parts are three. The paths bend toward fast rock, so the paths depend on the answer. Places with no paths, or with paths all in one direction, cannot be resolved. And noise in the times makes the details unstable, so the answer must be kept smooth or small where the data say little.

## Definition

**Input.** Sources $x_s$ and receivers $x_r$ at known positions, and for each pair $i = 1, \ldots, m$ a first-arrival time $T_i$, picked with an error of standard deviation $\sigma_i$. A parametrization of the slowness $s(x) = 1/v(x)$ in a region $\Omega$, usually cells or nodes, $s = \sum_j s_j \phi_j$ with $n$ unknowns $s_j$.

**Forward model.** The first-arrival time from $x_s$ to $x_r$ is
$$T(s; x_s, x_r) = \min_{\gamma} \int_\gamma s\, dl,$$
the minimum over paths $\gamma$ from $x_s$ to $x_r$ in $\Omega$ (Fermat's principle). Equivalently, $T(\cdot\,; x_s, \cdot)$ solves the [eikonal equation](/eikonal-equation/) $|\nabla T| = s$ with $T(x_s) = 0$. The data are $T_i = T(s; x_{s_i}, x_{r_i}) + e_i$ with noise $e_i$. In earthquake data the source positions and times are also unknown, and the problem is solved together with the location of the events ([Geiger's method](/geiger-method/)).

**Output.** A slowness model $s$ whose predicted times fit the data to within the noise, usually the minimizer of
$$\sum_i \sigma_i^{-2} \big(T_i - T(s; x_{s_i}, x_{r_i})\big)^2 + \lambda^2 \|L (s - s_0)\|^2$$
with a reference model $s_0$, a damping or smoothing operator $L$ and a weight $\lambda$, together with an estimate of how well each part of the model is resolved.

**Linearization.** Around a reference $s_0$ with the ray $\gamma_i$, a perturbation $\delta s$ changes the time by
$$\delta T_i = \int_{\gamma_i} \delta s\, dl + O(\|\delta s\|^2),$$
when the ray is unique and depends smoothly on $s$: the path is stationary for $s_0$, so the change of the path adds only a second-order term. On cells, $\delta T = G\, \delta s$ with $G_{ij}$ the length of ray $i$ in cell $j$, a sparse $m \times n$ matrix with about $n^{1/d}$ nonzeros per row in $d$ dimensions.

**Uniqueness and stability.** For straight rays (constant $s_0$) through all lines of a 2D region, the linearized data are the X-ray transform of $\delta s$, which is the Radon transform, and they determine $\delta s$ uniquely; the inversion is only mildly unstable (theorems about the Radon transform, not proved here). With a finite set of rays there are always models that no ray sees: the null space of $G$. With rays in a limited range of directions, details across the missing directions are lost. These are statements about the linearized problem. For the nonlinear problem, whether the first-arrival times between all boundary points determine an interior velocity is the boundary rigidity question; it is not used on this page.

## Variants

- Transmission geometries: crosswell (sources in one well, receivers in another), surface refraction (first arrivals that dive through the near surface), and VSP (sources at the surface, receivers in a well).
- Local earthquake tomography, solved jointly with the hypocenters, as in Aki and Lee (1976).
- Teleseismic tomography, which uses relative arrival times at an array from distant earthquakes and solves for the structure under the array, as in Aki, Christoffersson and Husebye (1977).
- Reflection traveltime tomography, which also inverts the times of reflected waves and the positions of the reflectors.
- Surface wave tomography, which inverts the travel times of surface waves at each period for maps of group or phase velocity; the times often come from [seismic interferometry](/seismic-interferometry/).
- Finite-frequency tomography, which replaces the ray by a sensitivity kernel of finite width; [full waveform inversion](/full-waveform-inversion/) fits the whole waveform in place of one time.

## Examples

**Two by two cells.** Four square cells of unit size, numbered row by row, are crossed by two horizontal and two vertical rays. Then
$$G = \begin{pmatrix} 1 & 1 & 0 & 0 \\ 0 & 0 & 1 & 1 \\ 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \end{pmatrix}$$
has rank 3, and the checkerboard $(1, -1, -1, 1)$ is in its null space: every ray crosses one fast and one slow cell, so the times do not change. One diagonal ray through cells 1 and 4, of length $\sqrt{2}$ in each, sees the checkerboard with the time $2\sqrt{2}$, and the five rays determine all four cells. More directions remove null space.

**Fermat's principle in numbers.** A straight path of 1000 m in a medium of 2000 m/s takes 0.5 s. Move its midpoint 10 m to the side: the path becomes $2\sqrt{500^2 + 10^2} = 1000.19998$ m, longer by 0.2 m, and the time grows by only $1.0 \times 10^{-4}$ s. A change of the path that is linear in the shift changes the time to second order, which is why the reference ray can be used in the linearization.

**Crosswell.** A square of 800 m is divided into $8 \times 8$ cells of 100 m. Eight sources at the cell centers of the left side and eight receivers at the cell centers of the right side give 64 straight rays for 64 unknowns. The background is 2000 m/s, and the four central cells are slow, 1800 m/s, which delays some rays by up to 14.8 ms. The measurements are these. The matrix $G$ has rank 50, not 64, so 14 patterns are not seen. The minimum-norm solution of the exact data gives 1842 m/s in the central cells and false fast cells of 2052 m/s above and below them, with a relative error of 0.48 in the slowness change: the nearly horizontal rays cannot place the anomaly in depth. With noise of 0.2 ms and damped least squares, $\min \|G\delta s - \delta T\|^2 + \lambda^2 \|\delta s\|^2$, the central cells come out at 1855 to 1864, 1871 to 1877, 1903 to 1905 and 1961 to 1962 m/s for $\lambda = 31.6$, 100, 316 and 1000 m: more damping, smaller and more stable anomalies, at the cost of bias.

## Known algorithms

- Linearized inversion with the rays of a reference model, by damped least squares, as in Aki, Christoffersson and Husebye (1977). The large sparse systems are solved by iterative methods: the [Kaczmarz method](/kaczmarz-method/) (called ART in tomography), [SIRT](/sirt/), [SART](/sart/), [CGLS](/cgls/) and [LSQR](/lsqr/), with the number of iterations as a regularization parameter ([semi-convergence](/semi-convergence/)).
- Nonlinear inversion by repeated linearization: trace rays in the current model, solve the linear system for an update, and repeat; this is a [Gauss-Newton](/gauss-newton-algorithm/) method on the misfit, often damped as in [Levenberg-Marquardt](/levenberg-marquardt/).
- Forward modeling by ray tracing (shooting or bending) or by solving the eikonal equation on a grid with the [fast marching method](/fast-marching-method/) or fast sweeping; the grid methods give first arrivals for all receivers at once and handle shadow zones.
- Gradients without rays by the [adjoint-state method](/adjoint-state-method/): one eikonal solve forward and one linear transport solve backward per source give the gradient of the misfit for all cells.
- Regularization by damping, smoothing or [Tikhonov regularization](/tikhonov-regularization/) in general; the choice of the weight is a [regularization method](/regularization-method/) question.
- Assessment by the [resolution matrix](/resolution-matrix/), checkerboard tests and the posterior covariance of the linearized problem.

## Bounds

- Data and unknowns: $m$ times for $n$ cells. Whatever $m$ is, the cells that no ray crosses, and the patterns in the null space of $G$, are not determined by the data (a theorem for the linearized problem). In the crosswell example, 64 rays determine only 50 of the 64 combinations.
- Cost of one forward step: straight-ray lengths cost $O(n^{1/d})$ per ray; a grid eikonal solve with fast marching costs $O(N \log N)$ per source for $N$ grid points. One iteration of LSQR or SIRT costs $O(\mathrm{nnz}(G)) = O(m\, n^{1/d})$.
- Stability: the condition number of $G$ restricted to its row space, 51 in the crosswell example, bounds the relative amplification of the data noise into the model for the minimum-norm solution (a theorem for least squares); damping lowers the amplification and adds bias.

## Reductions

- With constant reference velocity and full angular coverage in 2D, the linearized problem is the inversion of the Radon transform, the problem of CT (a theorem).
- Each linearized step is a sparse [least-squares problem](/least-squares-problem/), with Tikhonov regularization when damped.
- Locating earthquakes in a known model is the special case with four unknowns per event and no velocity unknowns, Geiger's method; the joint problem couples both.
- The interval velocities of flat layers from reflection moveout, the [Dix formula](/dix-formula/), are a one-dimensional special case of reflection traveltime inversion.

## Applications

- Images of the mantle and crust from earthquake arrival times at global and regional networks.
- Near-surface velocity models for statics corrections and as starting models for [migration](/seismic-migration/) and for full waveform inversion, where a good start helps avoid [cycle skipping](/cycle-skipping/).
- Crosswell imaging of reservoirs between boreholes, and monitoring of injected fluids.
- Volcano and geothermal studies with local earthquakes and, by interferometry, with ambient noise.

## References
