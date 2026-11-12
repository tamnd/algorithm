---
tag: SK407A
kind: concept
slug: centroidal-voronoi-tessellation
name: Centroidal Voronoi tessellation
aliases:
- CVT
- centroidal Voronoi diagram
area: geometry/voronoi-and-delaunay
level: advanced
summary: Voronoi tessellation in which each site coincides with the centroid of its own cell.
prereqs: [voronoi-diagram, voronoi-cell]
see_also: [lloyds-algorithm, k-means, k-means-problem, mesh-generation, power-diagram, gradient-descent, fixed-point-iteration, delaunay-triangulation]
sources:
  - paper: doi:10.1137/S0036144599352836
    title: Q. Du, V. Faber and M. Gunzburger, Centroidal Voronoi tessellations, applications and algorithms, SIAM Review 41(4), 1999
    locator: the definition with a density, the energy and its gradient, the proof that minimizers are centroidal, Lloyd's method and the applications
  - paper: doi:10.1109/TIT.1982.1056489
    title: S. P. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 1982
    locator: the two optimality conditions for a quantizer (nearest-neighbour cells and centroid points) and the iteration between them
  - book: isbn:9780471986355
    title: A. Okabe, B. Boots, K. Sugihara and S. N. Chiu, Spatial Tessellations, Concepts and Applications of Voronoi Diagrams, second edition, Wiley, 2000
    locator: the chapter on locational optimization through Voronoi diagrams
---

A centroidal Voronoi tessellation (CVT) of a region $\Omega$ is a [Voronoi diagram](/voronoi-diagram/) of $n$ sites in $\Omega$ in which every site is the centroid (the center of mass) of its own [Voronoi cell](/voronoi-cell/). With a density $\rho$, the centroid is taken with respect to $\rho$. CVTs are the critical points of the **quantization energy**, the integral of the squared distance from a point of $\Omega$ to its nearest site. So the best placement of $n$ sites for that energy is always a CVT, although a CVT need not be the best placement. [Lloyd's algorithm](/lloyds-algorithm/) finds CVTs by moving each site to the centroid of its cell again and again.

## In plain words

Put some sites in a room and split the room by nearest site. Each piece has a balance point, the place where the piece would balance on a pin. If every site sits exactly on the balance point of its own piece, the split is centroidal.

Such splits are good for many jobs. If every person in the room walks to the nearest site, the average squared walk is small. The pieces tend to have the same size and a round shape, close to regular hexagons in a large flat room.

A simple way to get one: start with any sites, move each site to the balance point of its piece, split the room again, and repeat. The average squared walk goes down at every round.

## The idea

**Definition.** Let $\Omega \subset \mathbb{R}^d$ be compact with positive volume, let $\rho \ge 0$ be a density on $\Omega$ with positive integral on every open subset, and let $z_1, \ldots, z_n$ be distinct points of $\Omega$. The Voronoi cell of $z_i$ in $\Omega$ is $V_i = \{x \in \Omega : |x - z_i| \le |x - z_j| \text{ for all } j\}$, and its mass centroid is

$$z_i^* = \frac{\int_{V_i} x \, \rho(x) \, dx}{\int_{V_i} \rho(x) \, dx}.$$

The tessellation is **centroidal** when $z_i = z_i^*$ for every $i$.

**The energy.** For sites $z_1, \ldots, z_n$ and any partition $W_1, \ldots, W_n$ of $\Omega$, let

$$E = \sum_{i = 1}^{n} \int_{W_i} \rho(x) \, |x - z_i|^2 \, dx.$$

Two facts make CVTs the natural optimum. (1) For fixed sites, the Voronoi partition minimizes $E$ over all partitions, because each point $x$ pays the squared distance to the site of its part, which is smallest for its nearest site. (2) For a fixed partition, the centroids minimize $E$ over all sites, because $\int_{W} \rho |x - z|^2 \, dx = \int_{W} \rho |x - z^*|^2 \, dx + m \, |z - z^*|^2$ with $m = \int_W \rho$, the parallel axis rule. So at a minimum of $E$ over sites and partitions, the partition is Voronoi and the sites are centroids. With the Voronoi partition, the function $\mathcal{E}(z_1, \ldots, z_n)$ has gradient $\partial \mathcal{E} / \partial z_i = 2 m_i (z_i - z_i^*)$, so the CVTs are exactly its critical points (Du, Faber and Gunzburger).

**Not every CVT is a minimum.** A CVT can be a saddle point of the energy. The example below shows two CVTs of the same rectangle with different energies.

**Shape of the cells.** For the uniform density on a large planar region, the cells of an optimal CVT are close to regular hexagons; in the plane this follows from a theorem of L. Fejes Tóth on sums of moments. The corresponding statement for three dimensions (Gersho's conjecture) is not proved.

**Relation to k-means.** If $\rho$ is a sum of point masses at the data points, the energy is the [k-means](/k-means/) objective, the cells are the clusters, and Lloyd's iteration is the usual k-means algorithm. The [k-means problem](/k-means-problem/) is the discrete form of the search for the best CVT.

## Examples

**An interval.** For $\Omega = [0, 1]$ with uniform density and $n$ sites, the only CVT has the sites $z_i = (2i - 1)/(2n)$: each cell $[(i-1)/n, i/n]$ has its midpoint as its centroid. Any other arrangement has some site that is not the midpoint of its cell.

**Two CVTs of a rectangle.** Let $\Omega = [0, 4] \times [0, 2]$ with uniform density and $n = 2$.

| sites | cells | energy $E$ |
| --- | --- | --- |
| $(1, 1)$ and $(3, 1)$ | the two squares $[0,2] \times [0,2]$ and $[2,4] \times [0,2]$ | $16/3$ |
| $(2, 1/2)$ and $(2, 3/2)$ | the two strips $[0,4] \times [0,1]$ and $[0,4] \times [1,2]$ | $34/3$ |

Both are centroidal. A square $[-1, 1]^2$ has $\int (x^2 + y^2) = 8/3$, which gives $16/3$ for the first row, and a strip $[-2, 2] \times [-1/2, 1/2]$ has $16/3 + 1/3 = 17/3$, which gives $34/3$ for the second. The second CVT is not a minimum: moving the sites to $(19/10, 1/2)$ and $(21/10, 3/2)$ lowers the energy to $56/5$. Starting from the sites $(0, 0)$ and $(1, 0)$, [Lloyd's algorithm](/lloyds-algorithm/) moves to $(1/4, 1)$ and $(9/4, 1)$, then $(5/8, 1)$ and $(21/8, 1)$, and tends to the first CVT, with energies $173/6$, $91/12$, $283/48$ and so on, decreasing toward $16/3$.

**A grid.** For a square divided into $k \times k$ equal smaller squares, the sites at the centers of the small squares form a CVT, since the Voronoi cells are the small squares.

## Where it is used

- **Quantization and compression.** Lloyd's original use: the best scalar or vector quantizer for a signal is a CVT of the signal distribution.
- **Clustering.** The [k-means](/k-means/) method is the discrete case.
- **Mesh generation.** The dual of a CVT is a [Delaunay triangulation](/delaunay-triangulation/) with well-shaped triangles, used in [mesh generation](/mesh-generation/) and in the remeshing of surfaces.
- **Sampling and stippling.** Blue-noise point sets and stippled drawings use CVTs with a density taken from an image.
- **Coverage and location.** Placing facilities, sensors or robots so that the average squared distance to them is small. A variant with capacity limits uses the [power diagram](/power-diagram/).

## References
