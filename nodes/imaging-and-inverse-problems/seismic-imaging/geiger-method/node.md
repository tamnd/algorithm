---
tag: 9PWX4B
kind: algorithm
slug: geiger-method
name: Geiger's method
aliases:
- Geiger earthquake location
area: imaging-and-inverse-problems/seismic-imaging
level: core
summary: "Locate an earthquake by Gauss-Newton steps on the hypocenter and origin time that fit the observed arrival times at the stations."
solves: [nonlinear-least-squares]
model: real-ram
complexity:
  vars: {n: the number of stations, k: the number of iterations}
  time: {worst: O(k n), average: O(k n), best: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, iterative: true, local_convergence: "quadratic for exact data", global_convergence: "not guaranteed", unknowns: 4}
history:
  year: 1910
  people: [Ludwig Geiger]
  note: Geiger (1910) proposed to locate an earthquake from arrival times alone by linearizing the travel times around a trial hypocenter and origin time and correcting the trial by least squares, step by step. An English translation appeared in 1912.
prereqs: [gauss-newton-algorithm, least-squares-problem]
see_also: [nonlinear-least-squares, levenberg-marquardt, normal-equations, condition-number, traveltime-tomography, eikonal-equation, fast-marching-method, seismic-reflection-model]
sources:
  - paper: "Ludwig Geiger, Herdbestimmung bei Erdbeben aus den Ankunftszeiten, Nachrichten von der Koeniglichen Gesellschaft der Wissenschaften zu Goettingen, Mathematisch-Physikalische Klasse, 1910, 331 to 349"
    title: Ludwig Geiger, Herdbestimmung bei Erdbeben aus den Ankunftszeiten, Nachrichten der Gesellschaft der Wissenschaften zu Goettingen, 1910, 331 to 349
    locator: the location of the focus and the origin time from arrival times by repeated linearized least-squares corrections
  - paper: "Ludwig Geiger, Probability method for the determination of earthquake epicenters from the arrival time only, Bulletin of St. Louis University 8(1), 1912, 60 to 71"
    title: Ludwig Geiger, Probability method for the determination of earthquake epicenters from the arrival time only, Bulletin of St. Louis University 8(1), 1912, 60 to 71
    locator: the English translation of the 1910 paper
  - book: isbn:9780521708425
    title: Peter M. Shearer, Introduction to Seismology, second edition, Cambridge University Press, 2009
    locator: Chapter 5 (inversion of travel time data), the section on earthquake location
  - paper: doi:10.1029/JB081i023p04381
    title: Keiiti Aki and W. H. K. Lee, Determination of three-dimensional velocity anomalies under a seismic array using first P arrival times from local earthquakes, 1. A homogeneous initial model, Journal of Geophysical Research 81(23), 1976, 4381 to 4399
    locator: the joint linearized inversion for hypocenters and velocity structure from local arrival times
---

Geiger's method locates an earthquake from the arrival times of its waves at a network of stations. The unknowns are the hypocenter, three coordinates, and the origin time. The predicted arrival time at a station is the origin time plus the travel time from the source, which depends on the source position in a nonlinear way. The method starts from a trial location, linearizes the travel times around it, and solves the small least-squares problem for a correction; then it repeats. This is the [Gauss-Newton algorithm](/gauss-newton-algorithm/) for a [nonlinear least-squares](/nonlinear-least-squares/) problem with four unknowns, and Geiger proposed it for earthquakes in 1910. It is the basic step of earthquake location, and the same linearization, with velocities as further unknowns, leads to [traveltime tomography](/traveltime-tomography/).

## In plain words

An earthquake sends waves to many stations, and each station notes when the first wave came. We do not know where or when the quake happened. Guess a place and a time. From the guess, compute when the wave should have reached each station, and compare with what the stations saw. Some stations heard it too early, some too late. Each mismatch hints which way to move the guess: toward the stations that heard it early. The method weighs all the hints at once, picks the move that best explains all the mismatches together, and moves the guess. Then it compares again. Near the right answer each move gets much smaller than the one before, and the guess settles on the place and time that fit the stations best.

## The problem

Input: stations $s_i = (a_i, b_i, c_i)$, $i = 1, \ldots, n$, with $n \ge 4$; observed P arrival times $T_i$; a velocity model, here a constant velocity $v$; a starting model $m_0$. Output: the model $m = (x, y, z, t_0)$ that minimizes
$$\Phi(m) = \sum_{i=1}^{n} \big(T_i - t_0 - D_i/v\big)^2, \qquad D_i = |h - s_i|, \quad h = (x, y, z).$$
The depth $z$ is positive down. With a layered or 3D velocity model, the travel time comes from ray tracing or from the [eikonal equation](/eikonal-equation/), and its derivative with respect to the source position is the slowness vector at the source; the method is the same.

## The algorithm

```pseudo id=main
GEIGER(stations s_i, times T_i, v, m₀)
L1  m ← m₀
L2  repeat until the update is small or the step limit is reached
L3      r_i ← T_i - (t₀ + |h - s_i| / v)                 ▷ residuals
L4      G_i ← ((h - s_i)ᵀ / (v |h - s_i|), 1)              ▷ Jacobian row
L5      solve (Gᵀ G + λ I) δ = Gᵀ r                         ▷ λ = 0: Gauss-Newton
L6      m ← m + δ
L7  return m
```

Row $i$ of the Jacobian holds the unit vector from station $i$ to the source divided by $v$, and a 1 for the origin time. Line L5 solves the [normal equations](/normal-equations/) of the linearized problem; with $\lambda > 0$ it is a [Levenberg-Marquardt](/levenberg-marquardt/) step. The code has two more safeguards, both heuristics and off by default: a limit on the length of the move, and the reflection of a source above the surface back below it.

## Example

**A good network.** Six stations at the surface, at $(0, 0)$, $(10, 0)$, $(0, 10)$, $(10, 10)$, $(5, 12)$ and $(3, 4)$ km, record a source at $(4000, 3000, 5000)$ m with origin time $0.5$ s, in a medium with $v = 6000$ m/s. The arrival times are $1.6785$, $1.8944$, $2.0811$, $2.2480$, $2.2240$ and $1.3660$ s. Start from $(4500, 3500, 7000)$ m and $0.4$ s:

| step | $(x, y, z)$ (m) | $t_0$ (s) | location error (m) | misfit (s²) |
|---|---|---|---|---|
| 1 | (3929.563, 2953.062, 4719.685) | 0.554 | 292.8 | $5.80 \times 10^{-3}$ |
| 2 | (3998.911, 2999.801, 4995.309) | 0.501 | 4.82 | $1.64 \times 10^{-6}$ |
| 3 | (4000.000, 3000.000, 4999.998) | 0.500 | $1.77 \times 10^{-3}$ | $1.13 \times 10^{-13}$ |
| 4 | (4000.000, 3000.000, 5000.000) | 0.500 | $2.8 \times 10^{-10}$ | $1.9 \times 10^{-27}$ |

From step 1 on, each error is between $5.6 \times 10^{-5}$ and $8.9 \times 10^{-5}$ times the square of the one before (in metres), the quadratic convergence of Claim 4 of the proof.

**Without the near station.** Drop the station at $(3, 4)$ km, the one close to the epicenter. From the same start, the first step jumps to the depth $z = -1183$ m, above the surface, and the next to $-9617$ m; plain Gauss-Newton still reaches the true source, after 10 steps. With all stations at the surface, a source at depth $z$ and its mirror image at $-z$ give the same times, so the data alone cannot rule out a negative depth. From the start $(5000, 5000, z_0)$ m and $0$ s, plain Gauss-Newton diverges for $z_0 = 2000$ m and $z_0 = 15000$ m, and converges to the mirror image $(4000, 3000, -5000)$ m for $z_0 = 8000$ m. With a step limit of 2000 m and the reflection of negative depths, it reaches the true source from all three starts, in 16, 12 and 17 steps. These are measurements on this network.

**Noisy times.** Add Gaussian noise with $\sigma = 10$ ms to the six times (seed 2). The method converges in 8 steps to a point 407 m from the true source, where $G^T r = 0$ to rounding; a grid search around that point finds no smaller misfit. The error is caused by the noise, not by the method: 10 ms of time is 60 m of path at 6000 m/s, and the geometry of the network enlarges it, most of all in depth.

## Correctness

Each step solves the linearized least-squares problem exactly, when $G$ has full column rank or $\lambda > 0$. The step is zero exactly when the gradient $-2G^T r$ of the misfit is zero, so a limit of the iteration is a stationary point. When the data are exact and $G$ has full rank at the true model, the iteration started close enough converges quadratically. For a fixed hypocenter the best origin time is the mean of $T_i - D_i/v$. With all stations at depth 0, a source and its mirror image fit equally well, and $G^T G$ is singular for a source at the surface. These are theorems, proved in proofs/correctness.md. Convergence from a far start is not guaranteed, and the safeguards that help in the example are heuristics.

## Complexity

In the real-RAM model each step costs $O(n)$: $n$ distances, $n$ Jacobian rows, the $4 \times 4$ matrix $G^T G$ in $O(16 n)$, and a solve of fixed size. With $k$ steps the total is $O(k n)$, and the extra space is $O(n)$. Near the solution with exact data, the number of steps to reach a precision $\epsilon$ grows like $\log\log(1/\epsilon)$. With a 3D velocity model the cost is dominated by the travel time computation.

## Properties

- Gauss-Newton: quadratic convergence near an exact fit (a theorem, Claim 4), linear or no convergence with large residuals.
- The depth and the origin time trade off: for a source deep below a small network, the depth and time columns of $G$ are nearly parallel. For five stations around a source at 10 km depth, the condition number of the scaled $G^T G$ is $2.4 \times 10^8$ for an aperture of 2 km and $1.3 \times 10^6$ for 30 km (a measurement; the network has all stations at about the same distance from the epicenter, which makes both large).
- A station near the epicenter constrains the depth best, since its ray is close to vertical (a heuristic).
- The result is only as good as the velocity model: an error in $v$ moves the location systematically, which noise analysis does not show.

## Variants and improvements

- Damped steps (Levenberg-Marquardt) and step limits, for a far start.
- Weighted least squares with the pick uncertainties, and robust norms, such as $\ell_1$, against wrong picks.
- Grid search or global search over the hypocenter with the best origin time at each point, which avoids local minima at a higher cost.
- Joint hypocenter determination: locate many events together with station corrections.
- Simultaneous inversion for hypocenters and velocity structure, as in Aki and Lee (1976), which leads to local earthquake tomography.
- Relative location of nearby events from time differences, which cancels most of the velocity model error.

## When to use it

Use it for routine location of local and regional earthquakes, and of induced events in mines and reservoirs, when a velocity model is available and a reasonable start exists, for example the station with the earliest arrival. Use a grid search first when the network is sparse or the start is poor.

## Pitfalls

- Stations all on one side of the source, or far from it compared with its depth, make $G^T G$ nearly singular, and the step is long and unreliable.
- A start too far away can give a step to a negative depth, a mirror solution, or divergence, as in the example.
- With fewer than four stations, or with stations on a line, the problem is underdetermined.
- A wrong velocity model gives a precise but wrong location; the formal error from $(G^T G)^{-1}$ does not include it.
- Mixing P and S picks needs separate velocities; using one velocity for both gives systematic errors.

## Implementations

## History

Geiger (1910) published the method in the Nachrichten of the Göttingen Society of Sciences, and an English translation appeared in the Bulletin of St. Louis University in 1912. He linearized the travel times around a trial focus and origin time and corrected the trial by least squares, repeating until the corrections were small. Each step needs the solution of a small linear system, which was laborious by hand; with digital computers the same linearized step became the core of many earthquake location programs. Aki and Lee (1976) extended the linearization to the velocity structure, solving for hypocenters and velocities together, an early form of local earthquake tomography.

## References
