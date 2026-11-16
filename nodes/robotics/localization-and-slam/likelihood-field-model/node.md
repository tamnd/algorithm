---
tag: 4N2WTX
kind: model
slug: likelihood-field-model
name: Likelihood field model
aliases:
- end-point model
area: robotics/localization-and-slam
level: core
summary: "Scores a range reading by the distance from its end point to the nearest obstacle in the map, a smooth and fast sensor model."
history:
  year: 2001
  people: [Sebastian Thrun]
  note: Thrun used a map of distances to the nearest obstacle to score the end points of laser scans in a 2001 journal paper on online mapping with teams of robots, and Probabilistic Robotics later set the model out under the name likelihood field.
prereqs: [bayes-filter, distance-transform]
see_also: [beam-range-finder-model, distance-transform, monte-carlo-localization, occupancy-grid-map, correlative-scan-matching, iterative-closest-point, normal-distributions-transform, grid-based-rbpf-slam]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 6, Section 6.4 (likelihood fields for range finders: the basic algorithm, its extensions and its limits), with Section 6.3 for the beam model it replaces"
  - paper: "Sebastian Thrun, A probabilistic online mapping algorithm for teams of mobile robots, International Journal of Robotics Research 20(5), 2001, pages 335 to 363"
    locator: the scan likelihood computed from the distance of each end point to the nearest obstacle in the map
---

The likelihood field model scores a scan from a laser range sensor against a map, given a pose of the robot. It does not trace each beam through the map. It takes only the end point of each beam, the place where the beam says an obstacle is, and asks how far that point is from the nearest obstacle in the map. A short distance gives a high score and a long distance a low one, with a Gaussian fall-off and a small constant floor for random readings. The distances for every point of the map are computed once, before localization starts, with a [distance transform](/distance-transform/). After that one beam costs one table lookup, and the score changes smoothly when the pose changes. The model is a measurement model $p(z_t \mid x_t, m)$ for the [Bayes filter](/bayes-filter/), used mainly in [Monte Carlo localization](/monte-carlo-localization/). It is a heuristic: it has no physical derivation, and it is not a normalized density over readings. The notation is the one of Thrun, Burgard and Fox (2005).

## The machine

**State.** The pose $x_t = (x, y, \theta)$ of the robot and a map $m$ with a set $O$ of occupied points or cells. The sensor sits at $(x_{\mathrm{s}}, y_{\mathrm{s}})$ in the robot frame.

**Measurement.** A scan of $K$ beams. Beam $k$ has a bearing $\theta_k$ in the sensor frame and a reading $z^k \in [0, z_{\max}]$.

**End points.** For each beam with $z^k < z_{\max}$, the end point in the world frame is

$$x_{z^k} = x + x_{\mathrm{s}}\cos\theta - y_{\mathrm{s}}\sin\theta + z^k \cos(\theta + \theta_k), \qquad y_{z^k} = y + y_{\mathrm{s}}\cos\theta + x_{\mathrm{s}}\sin\theta + z^k \sin(\theta + \theta_k).$$

Readings at $z_{\max}$ are skipped: they carry no end point.

**The model.** With $d_k$ the Euclidean distance from $(x_{z^k}, y_{z^k})$ to the nearest point of $O$,

$$q = \prod_{k:\ z^k < z_{\max}} \Bigl( z_{\mathrm{hit}}\, \mathcal N(d_k;\ 0, \sigma_{\mathrm{hit}}^2) + \frac{z_{\mathrm{rand}}}{z_{\max}} \Bigr).$$

**Parameters.** The weights $z_{\mathrm{hit}}$ and $z_{\mathrm{rand}}$, and $\sigma_{\mathrm{hit}}$ in meters. They are fitted to data in the same way as for the [beam model](/beam-range-finder-model/); they are not properties of the sensor alone, and $\sigma_{\mathrm{hit}}$ also absorbs map and pose errors.

**Precomputation.** On an [occupancy grid map](/occupancy-grid-map/) with $g$ cells, the cells above an occupancy threshold form $O$, and a [distance transform](/distance-transform/) stores the distance from each cell to the nearest cell of $O$. Exact Euclidean distance transforms run in $O(g)$ time. The table of $z_{\mathrm{hit}}\,\mathcal N(d; 0, \sigma^2) + z_{\mathrm{rand}}/z_{\max}$ per cell is the likelihood field that gives the model its name.

**Standing assumptions.** The beams are independent given the pose and the map, which is an approximation, as for the beam model. Only the end point matters: the cells that the beam passed through play no part.

**Example.** Take $\sigma_{\mathrm{hit}} = 0.2$ m, $z_{\mathrm{hit}} = 0.9$, $z_{\mathrm{rand}} = 0.1$ and $z_{\max} = 8$ m, so the floor is $0.1/8 = 0.0125$. A robot at $(1, 1, 0)$ with the sensor at its center sees a wall on the line $x = 4$. A beam with bearing 0 and reading $2.9$ ends at $(3.9, 1)$, at distance $0.1$ from the wall. The table gives the value of one beam as a function of $d$:

| $d$ (m) | 0 | 0.1 | 0.2 | 0.4 | 1.0 |
|---|---|---|---|---|---|
| beam value | 1.80774 | 1.59679 | 1.10137 | 0.25546 | 0.01251 |

So this beam scores $1.59679$. A reading of $3.1$ ends behind the wall at $(4.1, 1)$ and scores the same, which the beam model would not allow.

## What it counts

The model assigns a score to a scan at a hypothesized pose, used as the weight of a particle. After the precomputation one scan costs $O(K)$ time: two trigonometric terms and a table lookup per beam. The precomputation costs $O(g)$ time and $O(g)$ memory for a grid of $g$ cells. A filter with $N$ particles pays $O(N K)$ per scan, against $O(N K (1 + z_{\max}/s))$ for the beam model with ray casting on cells of side $s$.

## Relation to other models

- **[Beam range finder model](/beam-range-finder-model/).** Casts a ray for each beam and compares the reading with the expected range. It models free space, short readings and max range readings, but it is slow and not smooth in the pose. The likelihood field model gives up the physics for speed and smoothness.
- **Scan matching.** [Iterative closest point](/iterative-closest-point/) minimizes the sum of squared distances from end points to the nearest map points, which is the negative log of the likelihood field without the floor, up to constants. The [normal distributions transform](/normal-distributions-transform/) replaces the distance field with a Gaussian per cell. [Correlative scan matching](/correlative-scan-matching/) evaluates a likelihood field over a grid of poses.
- **[Grid-based Rao-Blackwellized particle filter SLAM](/grid-based-rbpf-slam/).** Can use end point scores of this kind on each particle's own map, both to weight the particles and to refine their poses by scan matching.

## Known results in the model

- **Theorem (smooth in the pose).** The distance $d(p) = \min_{o \in O} \lVert p - o \rVert$ to a nonempty set is 1-Lipschitz in $p$: $|d(p) - d(p')| \le \lVert p - p' \rVert$. The end point is a smooth function of the pose, and $\log\bigl(z_{\mathrm{hit}} \mathcal N(d; 0, \sigma^2) + c\bigr)$ with $c = z_{\mathrm{rand}}/z_{\max} > 0$ has a bounded derivative in $d$. So the log-likelihood of each beam is Lipschitz in the pose on any bounded set of poses. The beam model has no such bound, since its expected range jumps at the corners of obstacles. A lookup in a grid table makes the score piecewise constant; bilinear interpolation of the table restores continuity.
- **Theorem (not a density over readings).** For a fixed pose, $\int_0^{z_{\max}} \bigl(z_{\mathrm{hit}} \mathcal N(d(z); 0, \sigma^2) + z_{\mathrm{rand}}/z_{\max}\bigr)\,dz$ is not 1 in general. A beam that lies on the surface of a straight wall has $d(z) = 0$ for every $z$, so with the numbers of the example the integral is about $8 \times 1.80774 \approx 14.5$. A beam into open space far from every obstacle gives about $z_{\mathrm{rand}} = 0.1$. So $q$ is a score, not a probability density, and its values for scans with different numbers of valid beams are not on the same scale.
- **Heuristic (seeing through walls).** The model ignores the free space along each beam. A beam that passes through a wall in the map is not penalized, and an end point just behind a thin wall scores as high as one in front of it. In maps with thin walls this can let particles settle in the wrong room.
- **Unknown space.** Thrun, Burgard and Fox (2005) give end points that fall outside the known map the constant value $1/z_{\max}$, so that unexplored areas neither reward nor punish a pose.
- **Heuristic (independence of beams).** As for the beam model, the product over many correlated beams is too peaked. Using a subset of the beams is the common fix.

## References
