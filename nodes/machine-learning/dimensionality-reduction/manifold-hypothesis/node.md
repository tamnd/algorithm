---
tag: A0XNJ4
kind: definition
slug: manifold-hypothesis
name: Manifold hypothesis
aliases:
- manifold assumption
area: machine-learning/dimensionality-reduction
level: intro
summary: "High-dimensional data often lies near a low-dimensional manifold embedded in the ambient space."
prereqs: [embedding, curse-of-dimensionality]
see_also: [intrinsic-dimension, intrinsic-dimension-estimation, manifold-learning, isomap, locally-linear-embedding, laplacian-eigenmaps, autoencoder, principal-component-analysis]
sources:
  - paper: doi:10.1090/jams/852
    title: Charles Fefferman, Sanjoy Mitter and Hariharan Narayanan, Testing the manifold hypothesis, Journal of the American Mathematical Society 29(4), 2016, pages 983 to 1049
    locator: the problem statement in the introduction (a distribution on the unit ball of a separable Hilbert space, the class of d-dimensional manifolds with volume at most V and reach at least tau, the mean squared distance L(M, P)) and the main theorem on the test
  - paper: doi:10.1126/science.290.5500.2319
    title: Joshua B. Tenenbaum, Vin de Silva and John C. Langford, A global geometric framework for nonlinear dimensionality reduction, Science 290(5500), 2000, pages 2319 to 2323
    locator: the face images that vary in two pose angles and one lighting direction, recovered as three coordinates by Isomap
  - paper: doi:10.1007/s00454-008-9053-2
    title: Partha Niyogi, Stephen Smale and Shmuel Weinberger, Finding the homology of submanifolds with high confidence from random samples, Discrete and Computational Geometry 39, 2008, pages 419 to 441
    locator: the condition number 1/tau of a submanifold (tau is the reach) and the sample sizes that depend on it
  - paper: doi:10.1109/TPAMI.2013.50
    title: Yoshua Bengio, Aaron Courville and Pascal Vincent, Representation learning, a review and new perspectives, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(8), 2013, pages 1798 to 1828
    locator: the section on manifold learning and the manifold hypothesis as a prior for representation learning
---

The manifold hypothesis is the assumption that real high-dimensional data, such as images, sounds or measurements, lie on or near a manifold whose dimension is much smaller than the number of coordinates. A set of $64 \times 64$ face images has 4096 coordinates, but if the images differ only by the pose of the head and the direction of the light, they form a surface of dimension about 3 in that space. The hypothesis explains why learning from data in high dimension is possible at all, and it is the starting point of [manifold learning](/manifold-learning/) and of many nonlinear [embedding](/embedding/) methods. Fefferman, Mitter and Narayanan (2016) made it a precise statement that can be tested from samples.

## Definition

**Informal statement.** Data points $x_1, \ldots, x_n \in \mathbb{R}^D$ are drawn from a distribution $P$ that is concentrated near a smooth submanifold $M \subset \mathbb{R}^D$ of dimension $d \ll D$. "Near" means that the distance from a typical point to $M$ is small compared with the size of $M$ and with the scale at which $M$ bends.

**Formal statement (Fefferman, Mitter and Narayanan 2016).** Let $P$ be a probability distribution supported on the unit ball of a separable Hilbert space $\mathcal{H}$, which includes every $\mathbb{R}^D$ and also infinite-dimensional spaces. For a closed $d$-dimensional submanifold $M$, let

$$L(M, P) = \mathbb{E}_{x \sim P}\, \operatorname{dist}(x, M)^2$$

be the mean squared distance of the data to $M$. Let $\mathcal{G}(d, V, \tau)$ be the class of $d$-dimensional submanifolds with volume at most $V$ and reach at least $\tau$. The hypothesis with parameters $(d, V, \tau, \varepsilon)$ is that some $M \in \mathcal{G}(d, V, \tau)$ has $L(M, P) \le \varepsilon$.

The **reach** of $M$ is the largest $\tau$ such that every point within distance $\tau$ of $M$ has a unique nearest point on $M$. A large reach rules out both sharp bends (every radius of curvature is at least $\tau$) and two distant parts of $M$ that come close to each other. Without a bound on the volume and the reach, the hypothesis would be empty: a curve of unlimited length can pass within $\varepsilon$ of any finite sample.

**The test.** Fefferman, Mitter and Narayanan give an algorithm that takes independent samples from $P$ and, with probability at least $1 - \delta$, tells apart the two cases below, for a constant $C$ fixed in the paper:

- some $M \in \mathcal{G}(d, CV, \tau / C)$ has $L(M, P) \le C\varepsilon$, or
- no $M \in \mathcal{G}(d, V / C, C\tau)$ has $L(M, P) \le \varepsilon / C$.

The number of samples depends on $d$, $V$, $\tau$, $\varepsilon$ and $\delta$. Because $\mathcal{H}$ may have infinite dimension, it cannot depend on the dimension of the space that holds the data.

## Examples and non-examples

- **Images of one object under a few changes.** The images of an object turned through all angles, as vectors of pixel values, form a closed curve: $d = 1$, with $D$ the number of pixels. Two angles and one light direction give $d = 3$; Tenenbaum, de Silva and Langford (2000) recovered these three coordinates from 698 face images with [Isomap](/isomap/).
- **Synthetic manifolds.** The Swiss roll (a rectangle rolled up in $\mathbb{R}^3$), the sphere and the torus are the standard test cases for [manifold learning](/manifold-learning/); for each, $d$ is known.
- **Physical systems.** A pendulum observed through many sensors has a state of two numbers, angle and speed, so its measurements lie near a 2-dimensional surface whatever the number of sensors.
- **Natural images in general.** Estimates of the [intrinsic dimension](/intrinsic-dimension/) of image data sets are far below the number of pixels; this is evidence for the hypothesis, though the data are near a manifold, not on it, and the dimension depends on the scale.
- **Non-example: noise.** Points drawn uniformly from a cube in $\mathbb{R}^D$, or with independent noise in every coordinate, fill all $D$ dimensions; no low-dimensional manifold is near them.
- **Non-example: pieces of different dimension.** Data that are a union of a curve and a surface, or of several clusters with different numbers of degrees of freedom, lie near a union of manifolds, not near one manifold. Many methods then fail at the places where the pieces meet; local estimates of the dimension show the difference.
- **Non-example: a linear subspace with noise.** Data near a $d$-dimensional subspace do satisfy the hypothesis, but here [principal component analysis](/principal-component-analysis/) already finds the structure. The hypothesis matters for the curved case, where linear methods overestimate $d$.

## Related definitions

- [Intrinsic dimension](/intrinsic-dimension/): the $d$ of the hypothesis, with several definitions that agree on manifolds.
- [Intrinsic dimension estimation](/intrinsic-dimension-estimation/): measuring $d$ from samples, which is the first check of the hypothesis.
- [Embedding](/embedding/): the manifold is the image of a low-dimensional space under an embedding into $\mathbb{R}^D$; manifold learning tries to invert it.
- [Curse of dimensionality](/curse-of-dimensionality/): the hypothesis is the main reason why the curse is less severe in practice; for example, the error of nearest neighbor regression depends on $d$, not on $D$, for data on a manifold.
- [Manifold learning](/manifold-learning/): methods such as [Isomap](/isomap/), [locally linear embedding](/locally-linear-embedding/) and [Laplacian eigenmaps](/laplacian-eigenmaps/) that assume the hypothesis and recover coordinates on the manifold.
- [Autoencoder](/autoencoder/): a neural network whose narrow middle layer gives coordinates on a learned manifold.

## References
