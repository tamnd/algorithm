---
tag: FMWRYZ
kind: definition
slug: mumford-shah-functional
name: Mumford-Shah functional
aliases:
- Mumford-Shah model
area: computer-vision/segmentation-and-recognition
level: advanced
summary: An energy over a piecewise smooth image and a set of edges that weighs fit to the data, smoothness off the edges and the total edge length.
prereqs: [image-segmentation, euler-lagrange-equation]
see_also: [active-contours, level-set-method, total-variation-denoising, potts-model, image-segmentation-graph-cuts, markov-random-field, ultrametric-contour-map, normalized-cut]
sources:
  - paper: doi:10.1002/cpa.3160420503
    title: "David Mumford and Jayant Shah, Optimal approximations by piecewise smooth functions and associated variational problems, Communications on Pure and Applied Mathematics 42(5), 1989, 577-685"
    locator: "the definition of the functional, its piecewise constant limit, the first variation and the conjecture on the shape of the edge set"
  - paper: doi:10.1007/BF01052971
    title: "Ennio De Giorgi, Michele Carriero and Antonio Leaci, Existence theorem for a minimum problem with free discontinuity set, Archive for Rational Mechanics and Analysis 108, 1989, 195-218"
    locator: the existence of minimizers in the weak formulation and the closedness of the edge set
  - paper: doi:10.1002/cpa.3160430805
    title: "Luigi Ambrosio and Vincenzo Maria Tortorelli, Approximation of functionals depending on jumps by elliptic functionals via Gamma-convergence, Communications on Pure and Applied Mathematics 43(8), 1990, 999-1036"
    locator: the elliptic approximation with an edge indicator function and its Gamma-convergence to the Mumford-Shah functional
  - paper: doi:10.1109/83.902291
    title: "Tony F. Chan and Luminita A. Vese, Active contours without edges, IEEE Transactions on Image Processing 10(2), 2001, 266-277"
    locator: the two-phase piecewise constant case written with a level set function
  - paper: doi:10.1109/34.969114
    title: "Yuri Boykov, Olga Veksler and Ramin Zabih, Fast approximate energy minimization via graph cuts, IEEE Transactions on Pattern Analysis and Machine Intelligence 23(11), 2001, 1222-1239"
    locator: "Section 7 and the Appendix (NP-hardness of the Potts energy)"
  - paper: doi:10.1109/TPAMI.2010.161
    title: "Pablo Arbelaez, Michael Maire, Charless Fowlkes and Jitendra Malik, Contour detection and hierarchical image segmentation, IEEE TPAMI 33(5), 898-916, 2011"
    locator: "Eq. (4), the Mumford-Shah functional in the review of region-based segmentation"
---

The Mumford-Shah functional is an energy for [image segmentation](/image-segmentation/) and smoothing at the same time. Its arguments are an image $u$ and a set $K$ of curves, the edges. It adds three terms: how far $u$ is from the given image, how much $u$ varies away from the edges, and the total length of the edges. A minimizer is an image that is smooth inside regions and can jump across the edges, together with those edges. Mumford and Shah (1989) proposed it and studied its mathematics. It is the model behind many region-based segmentation methods, from [active contours](/active-contours/) without edges to discrete energies on a [Markov random field](/markov-random-field/).

## Definition

Let $\Omega \subset \mathbb{R}^2$ be a bounded open set, the image domain, and let $g : \Omega \to \mathbb{R}$ be the given image. For a closed set $K \subset \Omega$ and a function $u$ that is smooth on $\Omega \setminus K$,
$$E(u, K) = \int_{\Omega} (u - g)^2 \, dx \; + \; \mu \int_{\Omega \setminus K} \lvert \nabla u \rvert^2 \, dx \; + \; \nu\, \lvert K \rvert,$$
where $\lvert K \rvert$ is the length of $K$ (its one-dimensional Hausdorff measure) and $\mu, \nu > 0$ are weights. The Mumford-Shah problem is to minimize $E$ over all pairs $(u, K)$. The regions of the segmentation are the connected components of $\Omega \setminus K$. Papers place the weights on different terms; the form here is that of Eq. (4) of Arbelaez et al. (2011).

These facts follow from the definition or are theorems of the cited papers:

- **Each term needs the others.** Without the length term, more edges cost nothing, and $K$ can cut $\Omega$ into small regions where the gradient term is near 0. Without the gradient term, $u = g$ with $K = \emptyset$ costs nothing. Without the data term, a constant $u$ costs nothing.
- **The smooth part (theorem).** For a fixed $K$, $E$ is a strictly convex quadratic function of $u$. Its minimizer satisfies the [Euler-Lagrange equation](/euler-lagrange-equation/) $u - g = \mu \Delta u$ in $\Omega \setminus K$, with $\partial u / \partial n = 0$ on both sides of $K$ and on the border of $\Omega$. So $u$ is a smoothed $g$, and no smoothing crosses an edge.
- **The piecewise constant limit (theorem).** If $\mu \to \infty$, $u$ must be constant on each region $R_i$, and the best constant is the mean $c_i$ of $g$ on $R_i$. The energy becomes $\sum_i \int_{R_i} (g - c_i)^2 \, dx + \nu \lvert K \rvert$, the minimal partition problem. The proof: for a region $R$, $\int_R (g - c)^2 \, dx$ is a quadratic in $c$ with derivative $2 \int_R (c - g) \, dx$, which is zero at the mean.
- **Existence (theorem).** De Giorgi, Carriero and Leaci (1989) proved that a minimizer exists. Their proof works with a weak form in which $K$ is the set of jumps of $u$, and shows that this set is closed up to a set of zero length.
- **Shape of the edges (conjecture).** Mumford and Shah conjectured that the edges of a minimizer are a finite union of smooth arcs, which meet only in triple junctions at equal angles of 120 degrees or end at the border or in crack tips. This is the Mumford-Shah conjecture, not a theorem in general.
- **No convexity.** $E$ is not convex in the pair $(u, K)$, and minimization methods find local minima. In a discrete form on a pixel grid, the piecewise constant case with a fixed set of values is a [Potts model](/potts-model/), which is NP-hard to minimize for three or more values.

The functional is the definition of a good segmentation, not an algorithm. Methods to minimize it include the elliptic approximation of Ambrosio and Tortorelli (1990), where a function $v$ near 0 at edges and near 1 elsewhere replaces $K$; the [level set method](/level-set-method/) of Chan and Vese (2001) for two regions; greedy region merging that lowers the piecewise constant energy; and [graph cuts](/image-segmentation-graph-cuts/) on the discrete Potts form.

## Examples and non-examples

- **A step in one dimension.** Take the discrete form on six pixels with $g = (0, 0, 0, 1, 1, 1)$, $\mu = 1$, sums in place of integrals, differences $u_{i+1} - u_i$ in place of the gradient, and $\nu$ per cut between neighbors. With no cut, the best $u$ solves a linear system and is $(1/18, 2/18, 5/18, 13/18, 16/18, 17/18)$, with energy $4/9$. With one cut at the step, $u = g$ and the energy is $\nu$. Any set of cuts without the cut at the step costs at least $1/3 + \nu$ if it is not empty: with all other pairs cut, only the pair at the step is smoothed, and the best $u$ there is $(1/3, 2/3)$ with cost $1/9 + 1/9 + 1/9 = 1/3$. So the minimizer has the edge at the step if $\nu < 4/9$ and no edge if $\nu > 4/9$. A larger $\nu$ removes weak edges.
- **The edge cost does not depend on the contrast.** In the example, a step of height $h$ gives the no-cut energy $4h^2/9$, and the cut still costs $\nu$. So an edge appears when $h^2 > 9\nu/4$. In [total variation denoising](/total-variation-denoising/), a jump of height $h$ costs $\lambda h$ times its length, so strong edges cost more there. This is the main difference between the two energies.
- **Two regions of constant gray.** If $g$ is $a$ inside a disc of radius $r$ and $b$ outside, then $u = g$ with $K$ the circle has energy $2 \pi r \nu$. With no edge, the constant $u$ equal to the mean of $g$ has the energy $\lvert \Omega \rvert \sigma^2$, where $\sigma^2$ is the variance of $g$ over $\Omega$, and the best smooth $u$ costs less. So if $2 \pi r \nu > \lvert \Omega \rvert \sigma^2$, the circle is not the best edge set. For a small disc or a large $\nu$ the disc is lost.
- **Not a Gaussian blur.** Smoothing with a [Gaussian filter](/gaussian-filter/) blurs across all edges. The smooth part of a Mumford-Shah minimizer is smoothed only inside each region.
- **Not a boundary detector.** An edge detector such as [Canny](/canny-edge-detector/) marks pixels with a high gradient and does not ask the edges to close regions or to be short. The edge set of the Mumford-Shah functional comes from a global energy.

## Related definitions

The [Euler-Lagrange equation](/euler-lagrange-equation/) of the functional for a fixed edge set is a screened Poisson equation, solved region by region. [Total variation denoising](/total-variation-denoising/) is the convex energy that replaces the edge set and the gradient term by $\int \lvert \nabla u \rvert$. The [Potts model](/potts-model/) on a [Markov random field](/markov-random-field/) is the discrete piecewise constant case, where the edge length is the number of neighbor pairs with different labels. The Chan-Vese model is the two-region piecewise constant case, minimized with a [level set method](/level-set-method/). Arbelaez et al. (2011) review it among the region-based approaches to segmentation, in the same paper that defines the [ultrametric contour map](/ultrametric-contour-map/). The [normalized cut](/normalized-cut/) is another global criterion for a partition, based on a graph of pixel affinities instead of a fit to the image.

## References
