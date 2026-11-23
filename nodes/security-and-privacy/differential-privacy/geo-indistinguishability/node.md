---
tag: Y5XK8D
kind: definition
slug: geo-indistinguishability
name: Geo-indistinguishability
aliases:
- planar Laplace mechanism
area: security-and-privacy/differential-privacy
level: advanced
summary: Location privacy in which the probability of a reported location may change by at most e^(epsilon d) between true locations at distance d.
prereqs: [differential-privacy-definition, laplace-mechanism, metric-space]
see_also: [local-differential-privacy, spatial-cloaking, k-anonymity, euclidean-distance, sequential-composition-theorem, randomized-response]
sources:
  - url: "https://arxiv.org/abs/1212.1984"
    title: "Miguel E. Andrés, Nicolás E. Bordenabe, Konstantinos Chatzikokolakis and Catuscia Palamidessi, Geo-indistinguishability: differential privacy for location-based systems, ACM CCS 2013, pages 901 to 914"
    locator: "Definition 3.1 (geo-indistinguishability) and the remark on the Hamming metric, the composition of Section 3.3, equation (1) and the polar sampling with the Lambert W function in Section 4.1, discretization (Section 4.2, Theorem 4.1) and truncation (Section 4.3, Theorem 4.2)"
---

Geo-indistinguishability is a privacy definition for locations. A mechanism takes a user's true location and reports a randomized one. It is $\varepsilon$-geo-indistinguishable if, for any two true locations at distance $d$, the probability of each report changes by at most the factor $e^{\varepsilon d}$. So locations that are close are hard to tell apart from the report, and locations that are far apart may be told apart. This is the natural goal for location-based services: the user is willing to reveal the city, but not the street. Andrés, Bordenabe, Chatzikokolakis and Palamidessi defined it in 2013 and gave a mechanism that adds Laplace noise in the plane, with a density proportional to $e^{-\varepsilon d}$. It is [local differential privacy](/local-differential-privacy/) with the factor scaled by the distance.

## Definition

Let $\mathcal X$ be a set of locations with a [metric](/metric-space/) $d$, usually the [Euclidean distance](/euclidean-distance/) in the plane, and let $\mathcal Z$ be a set of reports. A mechanism $K$ maps each location $x$ to a probability distribution $K(x)$ on $\mathcal Z$.

**Definition (Andrés et al., Definition 3.1).** $K$ is **$\varepsilon$-geo-indistinguishable** if, for all $x, x' \in \mathcal X$ and every event $S \subseteq \mathcal Z$,

$$K(x)(S) \le e^{\varepsilon\,d(x, x')}\,K(x')(S).$$

The unit of $\varepsilon$ is one over the unit of distance. The paper states the same condition as $d_P(K(x), K(x')) \le \varepsilon\,d(x, x')$, where $d_P$ is the largest absolute log ratio of the probabilities of an event. A practical way to set $\varepsilon$ is to pick a radius $r$ and a level $\ell$, and ask for the factor $e^{\ell}$ between any two points within distance $r$; then $\varepsilon = \ell/r$.

Three facts follow from the definition.

1. **The metric is the neighbor relation.** There is no fixed set of neighbors. Every pair of locations is protected, with a strength that decays with the distance.
2. **Special cases.** With the discrete metric, $d(x, x') = 1$ for all $x \ne x'$, the definition is $\varepsilon$-LDP. With data sets as points and the Hamming metric, the number of records in which they differ, it is $\varepsilon$-[differential privacy](/differential-privacy-definition/) for neighbors together with group privacy for data sets at a larger distance.
3. **Composition.** If a user reports $n$ times with fresh noise, the reports together are $n\varepsilon$-geo-indistinguishable, by the same argument as [sequential composition](/sequential-composition-theorem/). Reports from the same place, averaged, reveal it more and more precisely.

## Examples and non-examples

**Laplace noise in the plane.** Report $z = x + (R\cos\theta, R\sin\theta)$, where $\theta$ is uniform on $[0, 2\pi)$ and $R$ has the Gamma law of shape 2 and scale $1/\varepsilon$, with the density $\varepsilon^2 r e^{-\varepsilon r}$. Then $z$ has the density $\frac{\varepsilon^2}{2\pi}e^{-\varepsilon\|z - x\|}$, which is equation (1) of the paper. For two true locations, the triangle inequality gives

$$\frac{e^{-\varepsilon\|z - x\|}}{e^{-\varepsilon\|z - x'\|}} = e^{\varepsilon(\|z - x'\| - \|z - x\|)} \le e^{\varepsilon\|x - x'\|},$$

so the mechanism is $\varepsilon$-geo-indistinguishable. The radius has the distribution function $C_\varepsilon(r) = 1 - (1 + \varepsilon r)e^{-\varepsilon r}$, which the paper inverts with the $W_{-1}$ branch of the Lambert $W$ function to sample $R$ from one uniform value.

**A worked setting.** Take $\ell = \ln 4$ within $r = 200$ m, so $\varepsilon = \ln 4/200 = 0.0069315$ per meter. Then two locations 200 m apart give reports whose probabilities differ by at most a factor 4. The noise radius has the mean $2/\varepsilon = 288.54$ m, the median $242.13$ m and the 95th percentile $684.39$ m. The report is within 200 m of the truth with probability $1 - (1 + \ln 4)/4 = 0.4034$. A service that needs the user within a few hundred meters, such as a search for nearby restaurants, still works.

**Laplace noise on each coordinate.** Adding independent one-dimensional $\mathrm{Lap}(1/\varepsilon)$ noise to each coordinate gives the factor $e^{\varepsilon(|x_1 - x'_1| + |x_2 - x'_2|)}$. That is $\varepsilon$-geo-indistinguishable for the Manhattan metric, and so $\sqrt 2\,\varepsilon$-geo-indistinguishable for the Euclidean metric, since the Manhattan distance is at most $\sqrt 2$ times the Euclidean one.

**Non-example: cloaking with a fixed grid.** [Spatial cloaking](/spatial-cloaking/) that reports the grid cell of the user fails for every $\varepsilon$. Two locations 1 m apart on the two sides of a cell border give reports with disjoint supports, so the factor is infinite.

**Non-example: a uniform point in a disk.** Reporting a uniform random point within 500 m of the truth also fails. For two true locations 10 m apart, some reports lie in one disk and not in the other, and they have probability 0 under one location only.

**Non-example: a rounded or truncated sampler.** Laplace noise in the plane computed in floating point and rounded to a grid, or cut off at the border of a map, is not exactly the mechanism above. Andrés et al. show that discretization needs a slightly larger $\varepsilon$ and a precision condition (Theorem 4.1), and that truncation to a region needs a remapping of the reports to the region (Theorem 4.2).

## Related definitions

- [Local differential privacy](/local-differential-privacy/) is the special case of the discrete metric: all pairs of inputs get the same protection.
- [Differential privacy](/differential-privacy-definition/) is the special case of data sets with the Hamming metric. Chatzikokolakis, Andrés, Bordenabe and Palamidessi (2013) studied this general form, privacy with respect to any metric, often called metric privacy or $d_{\mathcal X}$-privacy.
- [k-anonymity](/k-anonymity/) and spatial cloaking hide the user among others or in a region, but they give no bound of this form, and they fail against an attacker with side information.
- The [Laplace mechanism](/laplace-mechanism/) is the one-dimensional case: on the line, $x + \mathrm{Lap}(1/\varepsilon)$ is $\varepsilon$-geo-indistinguishable for $d(x, x') = |x - x'|$.

## References
