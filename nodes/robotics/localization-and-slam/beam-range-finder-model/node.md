---
tag: FJ9F2M
kind: model
slug: beam-range-finder-model
name: Beam range finder model
aliases:
- beam model
area: robotics/localization-and-slam
level: core
summary: "A mixture of a Gaussian hit, short readings, max range readings and random noise for each beam of a range sensor."
history:
  year: 2005
  people: [Sebastian Thrun, Wolfram Burgard, Dieter Fox]
  note: Probabilistic Robotics sets out the beam model as a mixture of four distributions per beam, with an algorithm that fits the mixture weights and the noise parameters to recorded data.
prereqs: [bayes-filter]
see_also: [likelihood-field-model, monte-carlo-localization, amanatides-woo-traversal, ray-casting, expectation-maximization, odometry-motion-model, landmark-measurement-model, inverse-sensor-model]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 6, Section 6.3 (beam models of range finders: the basic measurement algorithm in Section 6.3.1, adjusting the intrinsic parameters in Section 6.3.2, the derivation in Section 6.3.3 and practical considerations in Section 6.3.4)"
---

The beam range finder model gives the probability of a scan from a laser or sonar range sensor, given the pose of the robot and a map. Each beam of the sensor reports the distance to the first thing it hits, up to a maximum range. The model compares the reading of each beam with the range $z^*$ that the beam should report in the map, found by casting a ray from the sensor until it meets an obstacle. A reading is explained as one of four causes: a correct hit with Gaussian noise, an early return from an object that is not in the map (such as a person), a failure that returns the maximum range, or an unexplained random value. The model is the measurement model $p(z_t \mid x_t, m)$ of the [Bayes filter](/bayes-filter/), and [Monte Carlo localization](/monte-carlo-localization/) uses it to weight particles. The notation is the one of Thrun, Burgard and Fox (2005).

## The machine

**State.** The pose $x_t = (x, y, \theta)$ of the robot and a map $m$, usually an [occupancy grid map](/occupancy-grid-map/). The mounting pose of the sensor on the robot is known.

**Measurement.** A scan $z_t = (z_t^1, \ldots, z_t^K)$ of $K$ beams. Beam $k$ has a known bearing $\theta_k$ in the sensor frame and a reading $z_t^k \in [0, z_{\max}]$ in meters.

**Expected range.** For each beam, $z_t^{k*}$ is the range at which the ray from the sensor pose in direction $\theta + \theta_k$ first meets an obstacle in $m$, capped at $z_{\max}$. On a grid this is a walk along the cells of the ray, as in the [Amanatides-Woo traversal](/amanatides-woo-traversal/), the same first-hit query as [ray casting](/ray-casting/) in graphics.

**The four parts.** Writing $z = z_t^k$ and $z^* = z_t^{k*}$:

- hit: $p_{\mathrm{hit}}(z) = \eta\, \mathcal N(z;\ z^*, \sigma_{\mathrm{hit}}^2)$ for $0 \le z \le z_{\max}$ and 0 otherwise, with $\eta$ the inverse of the Gaussian mass on $[0, z_{\max}]$;
- short: $p_{\mathrm{short}}(z) = \eta\, \lambda_{\mathrm{short}}\, e^{-\lambda_{\mathrm{short}} z}$ for $0 \le z \le z^*$ and 0 otherwise, with $\eta = 1 / (1 - e^{-\lambda_{\mathrm{short}} z^*})$;
- max: $p_{\max}(z) = 1$ if $z = z_{\max}$ and 0 otherwise;
- random: $p_{\mathrm{rand}}(z) = 1 / z_{\max}$ for $0 \le z < z_{\max}$ and 0 otherwise.

**The model.** With weights $z_{\mathrm{hit}} + z_{\mathrm{short}} + z_{\max} + z_{\mathrm{rand}} = 1$,

$$p(z_t^k \mid x_t, m) = z_{\mathrm{hit}}\, p_{\mathrm{hit}} + z_{\mathrm{short}}\, p_{\mathrm{short}} + z_{\max}\, p_{\max} + z_{\mathrm{rand}}\, p_{\mathrm{rand}}, \qquad p(z_t \mid x_t, m) = \prod_{k=1}^{K} p(z_t^k \mid x_t, m).$$

**Parameters.** The four weights, $\sigma_{\mathrm{hit}}$ in meters and $\lambda_{\mathrm{short}}$ in 1/m. They are fitted to data, not derived from the sensor data sheet; Thrun, Burgard and Fox (2005) give an algorithm for this in Section 6.3.2.

**Standing assumptions.** The beams are independent given the pose and the map. This is an approximation: neighboring beams see the same unmodeled person, the same map error and the same pose error. The map is static, and every object that is not in it shows up only as a short reading. The expected range is a function of the pose and the map only.

**Example.** Take $z^* = 4$ m, $\sigma_{\mathrm{hit}} = 0.2$ m, $\lambda_{\mathrm{short}} = 0.5$ /m, $z_{\max} = 8$ m and the weights $0.7, 0.1, 0.1, 0.1$. Then $\eta_{\mathrm{hit}} \approx 1$, since the Gaussian lies far inside $[0, 8]$, and $\eta_{\mathrm{short}} = 1/(1 - e^{-2}) \approx 1.15652$. The model gives:

| reading $z$ | hit part | short part | max part | random part | $p(z)$ |
|---|---|---|---|---|---|
| 4.0 | 1.39630 | 0.00783 | 0 | 0.0125 | 1.41662 |
| 4.2 | 0.84690 | 0 | 0 | 0.0125 | 0.85940 |
| 3.6 | 0.18897 | 0.00956 | 0 | 0.0125 | 0.21103 |
| 2.0 | about $10^{-22}$ | 0.02127 | 0 | 0.0125 | 0.03377 |
| 6.0 | about $10^{-22}$ | 0 | 0 | 0.0125 | 0.0125 |
| 8.0 | about $10^{-87}$ | 0 | 0.1 | 0 | 0.1 |

A reading 2 m short of the expected range is about 2.7 times more likely than a reading 2 m beyond it, because the short part covers readings in front of the obstacle and nothing covers readings behind it except the random part.

## What it counts

The model assigns a likelihood to a scan at a hypothesized pose. In a particle filter the weight of each particle is this likelihood. One evaluation costs $K$ ray casts plus $O(K)$ arithmetic. A ray cast on a grid with cell side $s$ visits $O(1 + z_{\max}/s)$ cells, so one scan at one pose costs $O(K (1 + z_{\max}/s))$, and a particle filter with $N$ particles pays this $N$ times per scan. A common speedup is to precompute the expected ranges for a grid of poses and bearings, which trades memory for time.

## Relation to other models

- **[Likelihood field model](/likelihood-field-model/).** Drops the ray cast. It looks only at the end point of each beam and its distance to the nearest obstacle, which is smooth in the pose and needs no ray casting, but it ignores the free space along the beam.
- **Correlation-based models.** Compare a local map built from the scan with the global map. [Correlative scan matching](/correlative-scan-matching/) works in this way.
- **[Landmark measurement model](/landmark-measurement-model/).** Uses a few extracted features, each with a range and a bearing, instead of every raw beam.
- **[Inverse sensor model](/inverse-sensor-model/).** Goes the other way, from a reading to the occupancy of the cells along the beam. Mapping needs the inverse model; localization needs this forward model.
- **[Gaussian mixture model](/gaussian-mixture-model/).** The beam model is a mixture too, but only one of its parts is Gaussian, one part is a point mass, and the parts depend on $z^*$.

## Known results in the model

- **Theorem (a mixed distribution).** Each part is a probability distribution on $[0, z_{\max}]$: $p_{\mathrm{hit}}$, $p_{\mathrm{short}}$ and $p_{\mathrm{rand}}$ are densities that integrate to 1 by the choice of $\eta$, and $p_{\max}$ is a point mass of 1 at $z_{\max}$. So with weights that sum to 1 the model is a distribution, with a density part on $[0, z_{\max}]$ and an atom at the range $z_{\max}$ whose size is the weight of the max part.
- **Theorem (the unit matters).** The formula multiplies densities and probabilities as if they were the same kind of number. If ranges are measured in centimeters instead of meters, every density value is divided by 100 and the point mass is not. In the example, a perfect hit gives 1.41662 per meter but 0.0141662 per centimeter, while a max range reading still gives 0.1. So in centimeters a max range reading counts about 7 times more than a perfect hit, and in meters about 14 times less. The ranking of poses by $p(z_t \mid x_t, m)$ can change with the unit when scans differ in their number of max range readings.
- **Learning the parameters.** Section 6.3.2 of Thrun, Burgard and Fox (2005) fits the weights, $\sigma_{\mathrm{hit}}$ and $\lambda_{\mathrm{short}}$ to readings with known $z^*$ by an iteration that alternates the responsibility of each part for each reading and a weighted fit of the parameters. This is [expectation maximization](/expectation-maximization/) for a mixture, so the likelihood does not decrease, and like all EM it may stop at a local optimum.
- **Heuristic (overconfidence from independence).** Since the beams are not independent, the product over $K$ beams makes the likelihood much too peaked when $K$ is large, so a filter can lose the true pose. Common fixes are to use only a subset of the beams or to raise each beam likelihood to a power below 1. Both are heuristics with a tuning parameter.
- **Not smooth in the pose.** $z^*$ jumps when a beam slides past the corner of an obstacle, so a small change of the pose can change the likelihood by orders of magnitude. With a small $\sigma_{\mathrm{hit}}$ the likelihood surface over poses has many sharp peaks, which makes gradient search and coarse particle sets fail. The [likelihood field model](/likelihood-field-model/) avoids this.

## References
