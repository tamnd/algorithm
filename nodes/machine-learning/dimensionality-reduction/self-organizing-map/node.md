---
tag: MBT904
kind: algorithm
slug: self-organizing-map
name: Self-organizing map
aliases:
- Kohonen map
- SOM
- Kohonen self-organizing feature map
area: machine-learning/dimensionality-reduction
level: core
summary: "A grid of units with weight vectors; each input moves its best matching unit and that unit's grid neighbors toward it, so near units come to stand for near inputs."
model: real-ram
complexity:
  vars: {T: the number of steps, K: the number of units, D: the input dimension, n: the number of inputs}
  time: {worst: "O(T K D)"}
  space: {extra: "O(K D)"}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 1982
  people: [Teuvo Kohonen]
  note: Kohonen published the self-organizing map in Biological Cybernetics in 1982, as a model of the ordered feature maps of the cortex.
prereqs: [vector-quantization, k-means]
see_also: [lloyds-algorithm, principal-curves, umap, t-sne, sammon-mapping, multidimensional-scaling, trustworthiness-and-continuity, stochastic-gradient-descent]
sources:
  - paper: doi:10.1007/BF00337288
    title: "Teuvo Kohonen, Self-organized formation of topologically correct feature maps, Biological Cybernetics 43(1):59-69, 1982"
    locator: the grid of units, the selection of the best matching unit, and the update of the winner and its neighbors with a shrinking neighborhood
  - book: isbn:9783540679219
    title: "Teuvo Kohonen, Self-Organizing Maps, 3rd edition, Springer, 2001"
    locator: the chapter on the basic SOM algorithm, with the Gaussian neighborhood, the schedules for the learning rate and the radius, and the batch map
  - paper: "Marie Cottrell and Jean-Claude Fort, Étude d'un processus d'auto-organisation, Annales de l'Institut Henri Poincaré, Probabilités et Statistiques 23(1):1-20, 1987"
    title: Cottrell and Fort 1987
    locator: the proof that a one-dimensional chain with uniform input and a neighborhood of two units becomes ordered with probability 1, and stays ordered
  - paper: "Ed Erwin, Klaus Obermayer and Klaus Schulten, Self-organizing maps: ordering, convergence properties and energy functions, Biological Cybernetics 67(1):47-55, 1992"
    title: Erwin, Obermayer and Schulten 1992
    locator: there is no energy function for the SOM with a continuous input distribution; results on ordering in one dimension
  - paper: "Kimmo Kiviluoto, Topology preservation in self-organizing maps, Proceedings of the IEEE International Conference on Neural Networks, 1996, pp. 294-299"
    title: Kiviluoto 1996
    locator: the topographic error, the share of inputs whose best and second best units are not adjacent
  - paper: "Tom Heskes, Energy functions for self-organizing maps, in E. Oja and S. Kaski (eds.), Kohonen Maps, Elsevier, 1999, pp. 303-315"
    title: Heskes 1999
    locator: a modified winner rule under which the SOM descends an energy function
---

A self-organizing map (SOM), or Kohonen map, is a grid of units, usually a line or a rectangle of a few dozen to a few thousand units, each with a weight vector in the input space. For each input, the unit with the nearest weight wins, and the winner and its neighbors on the grid all move their weights toward the input. The neighborhood and the step size shrink over time. At the end, units that are near on the grid hold weights that are near in the input space, so the grid is a discrete, ordered map of the data: a [vector quantizer](/vector-quantization/) with a topology. Kohonen proposed it in 1982. The method is simple and robust in practice, but its convergence is proved only in special cases, mainly for a one-dimensional chain (Cottrell and Fort 1987).

## In plain words

Lay out a sheet of small cells, each with a point in the data space. Take one data point. Find the cell whose point is closest to it. Move that cell's point a step toward the data point, and also move the cells next to it on the sheet, by smaller steps the farther they are on the sheet.

Repeat with many data points. At first the steps are big and reach far across the sheet, so the whole sheet unfolds and spreads over the data. Later they are small and reach only a few cells, so each cell settles on its own part of the data. In the end, cells next to each other on the sheet stand for data points that are close.

## The problem

The input is a set of $n$ vectors $x_1, \ldots, x_n \in \mathbb{R}^D$ and a grid of $K$ units with fixed positions $r_1, \ldots, r_K$ (for example the points of a $5 \times 5$ square lattice). The output is a weight $w_j \in \mathbb{R}^D$ for each unit.

Two goals pull against each other:

- **Quantization.** Each input should be close to the weight of its *best matching unit* (BMU) $c(x) = \arg\min_j \|x - w_j\|$. The *quantization error* is
  $$\mathrm{QE} = \frac{1}{n} \sum_{i=1}^{n} \|x_i - w_{c(x_i)}\|.$$
- **Topology.** Units that are near on the grid should have near weights, so that the map is not twisted. The *topographic error* (Kiviluoto 1996) is the share of inputs whose best and second best units are not adjacent on the grid:
  $$\mathrm{TE} = \frac{1}{n} \sum_{i=1}^{n} \big[\, c_1(x_i) \text{ and } c_2(x_i) \text{ are not grid neighbors} \,\big].$$

Plain [k-means](/k-means/) with $K$ centers minimizes the squared quantization error and ignores the topology. The SOM gives up some quantization to get an ordered map.

## The algorithm

```pseudo id=main
SOM(x[1..n], r[1..K], T, α₀, σ₀, σ₁)
L1  w_j ← a random vector in the bounding box of the data, for j = 1..K
L2  for t ← 0 to T − 1 do
L3      x ← an input drawn at random
L4      c ← argmin_j ‖x − w_j‖                          ▷ best matching unit
L5      α ← α₀ (1 − t/T);  σ ← σ₀ (σ₁/σ₀)^{t/T}           ▷ shrinking rate and radius
L6      for j ← 1 to K do h_j ← exp(−‖r_j − r_c‖² / (2σ²))  ▷ neighborhood
L7          w_j ← w_j + α h_j (x − w_j)
L8  return w
```

The neighborhood $h$ on line L6 is a Gaussian of the *grid* distance between unit $j$ and the winner, not of the distance in the input space. Kohonen's original form is a "bubble": $h_j = 1$ inside a radius and $0$ outside. The schedules on line L5 are one common choice; any rate that falls to 0 and any radius that shrinks from about half the grid to about one unit will do. Training often has two phases: a short *ordering* phase with a large radius and rate, then a long *tuning* phase with a radius of about one unit and a small rate.

**Batch SOM.** Instead of one input at a time, each epoch finds the BMU of every input and then sets

$$w_j \leftarrow \frac{\sum_{i} h_{c(x_i), j}\, x_i}{\sum_i h_{c(x_i), j}},$$

the neighborhood-weighted mean of the inputs. The batch map has no learning rate, does not depend on the input order, and is what most libraries use. Without a neighborhood ($h_{cj} = [c = j]$) it is exactly Lloyd's algorithm for k-means.

## Example

Take a chain of $K = 3$ units at $r = 1, 2, 3$ with scalar weights $w = (0.2, 0.9, 0.4)$. This map is twisted: unit 2 is out of order. Use $\alpha = 0.5$ and $\sigma = 1$, so $h$ is $1$, $e^{-1/2} = 0.6065$ and $e^{-2} = 0.1353$ at grid distance 0, 1 and 2.

| step | input $x$ | BMU | $w_1$ | $w_2$ | $w_3$ |
|---|---|---|---|---|---|
| start | | | 0.2 | 0.9 | 0.4 |
| 1 | 0.5 | 3 | 0.2203 | 0.7787 | 0.45 |
| 2 | 0.0 | 1 | 0.1102 | 0.5425 | 0.4195 |
| 3 | 1.0 | 2 | 0.3800 | 0.7713 | 0.5956 |
| 4 | 0.0 | 1 | 0.1900 | 0.5374 | 0.5553 |
| 5 | 1.0 | 3 | 0.2448 | 0.6777 | 0.7776 |

In step 1, unit 3 wins with distance $0.1$. It moves half the way to $x$: $0.4 + 0.5 \cdot 0.1 = 0.45$. Unit 2 moves by $0.5 \cdot 0.6065 \cdot (0.5 - 0.9) = -0.1213$, and unit 1 by $0.5 \cdot 0.1353 \cdot 0.3 = 0.0203$. After step 5 the chain is ordered, $w_1 < w_2 < w_3$, and by the theorem below it stays ordered for all later inputs.

**The two errors.** For the inputs $0, 0.35, 0.55, 1$, the ordered map $w = (0.1, 0.5, 0.9)$ and the twisted map $w = (0.1, 0.9, 0.5)$ both have $\mathrm{QE} = (0.1 + 0.15 + 0.05 + 0.1)/4 = 0.1$, since they hold the same three weights. But in the twisted map the inputs $0$ and $0.35$ have their two best units at grid positions 1 and 3, which are not adjacent, so $\mathrm{TE} = 2/4 = 0.5$, against $0$ for the ordered map. This is why the two errors are reported together.

With 10 units, 200 uniform inputs on $[0, 1]$, $T = 2000$, $\alpha_0 = 0.5$ and a fixed seed, the chain ends ordered at about $0.908, 0.819, \ldots, 0.059$, with $\mathrm{QE} \approx 0.026$ and $\mathrm{TE} = 0$.

## Correctness

The full proofs are below. There is no general theorem that the SOM converges or that its map is optimal in any sense. What is proved:

1. **Order is absorbing in one dimension.** For a chain with scalar weights, a neighborhood that does not grow with grid distance and steps $\alpha h_j < 1$, an ordered chain ($w_1 < \cdots < w_K$ or the reverse) is still ordered after any update. The proof splits the pairs of adjacent units by their side of the winner and uses the fact that the input lies within half a gap of the winner's weight.
2. **Ordering from a random start**, in one dimension: Cottrell and Fort (1987) proved that with uniform inputs, a constant rate and a neighborhood of the two adjacent units, the chain becomes ordered with probability 1 in finite time.
3. **The batch step** is the exact minimizer of $\sum_i h_{c(x_i) j} \|x_i - w\|^2$ for each $j$ with the winners fixed.

In two or more dimensions there is no general proof that the map unfolds, and Erwin, Obermayer and Schulten (1992) showed that, for a continuous input distribution, the online SOM is not gradient descent on any energy function. Heskes (1999) changed the winner rule to get one.

## Complexity

In the [real RAM](/real-ram/) model, each online step finds the winner in $O(K D)$ time by a full scan and updates all $K$ weights in $O(K D)$, so $T$ steps cost $O(T K D)$, on every input. A batch epoch costs $O(n K D)$. The memory is $O(K D)$ for the weights and $O(K)$ for the grid. With a bubble neighborhood, only the units inside the radius are updated, and for a large map a tree on the weights can speed up the winner search.

## Properties

- **Online and incremental.** The online rule can follow a stream of inputs.
- **Topology preserving, mostly.** Near units have near weights. The reverse can fail: near inputs can land on far units where the map folds.
- **Density.** The weights crowd where the inputs are dense, but less than the density itself. For a one-dimensional chain in the limit of many units, the density of the weights grows as about the $2/3$ power of the input density, against $1/3$ in the optimal quantizer for the squared error in one dimension and $1$ for an exact match.
- **Fixed grid.** The shape and the size of the grid are set in advance. A grid that does not fit the data folds or leaves units in empty space ("dead units").
- **Randomized.** The result depends on the start and on the order of the inputs; the batch map removes the second dependence.

## Variants and improvements

- **Batch SOM** (above): faster and repeatable.
- **Hexagonal grids** give each unit six equal neighbors and are the default in the SOM Toolbox and in Kohonen's book.
- **Start from PCA.** Placing the grid on the plane of the first two [principal components](/principal-component-analysis/) skips most of the ordering phase.
- **U-matrix.** To show clusters, color each unit by the mean distance from its weight to the weights of its grid neighbors.
- **Growing maps** and **neural gas** drop the fixed grid: the neighbors are ranked by distance in the input space, or the grid grows where the error is large.
- **Generative topographic mapping** (Bishop, Svensén and Williams) is a probabilistic model with a similar grid, fitted by [expectation maximization](/expectation-maximization/), with a likelihood to compare models.
- **Principal curves.** A one-dimensional SOM with many units and a smoothing neighborhood is close to a discrete [principal curve](/principal-curves/).

## When to use it

Use a SOM to draw a picture of high-dimensional data on a fixed grid, for example for exploratory analysis of process data, documents or customer records, where each unit becomes a prototype that you can read. Use it when you want prototypes and a map in one step. For a picture of neighbors without prototypes, [t-SNE](/t-sne/) or [UMAP](/umap/) usually shows clusters more clearly. For prototypes without a map, use [k-means](/k-means/).

## Pitfalls

- **Twisted maps.** If the radius shrinks too fast, the map can freeze with a fold or a twist. Start with a radius of about half the grid.
- **The scale of the inputs.** The winner uses the Euclidean distance, so scale all features to similar ranges first.
- **The neighborhood in the wrong space.** The neighborhood uses the grid distance $\|r_j - r_c\|$, not the distance between weights. Using the latter gives a different method (neural gas uses ranks in the input space).
- **Step size at 1.** With $\alpha h_j \ge 1$ a weight can jump past the input, and order can be lost.
- **Reading the grid as a metric.** Equal grid steps can stand for very different distances in the data. Check a U-matrix.

## Implementations

## History

Kohonen published the self-organizing map in 1982, building on models of the formation of ordered maps in the visual cortex by von der Malsburg (1973) and by Willshaw and von der Malsburg (1976). He made the method simple enough for large practical use, wrote a book on it that went through three editions, and his group released the SOM_PAK and SOM Toolbox software. Cottrell and Fort (1987) gave the first rigorous proof of ordering, for one dimension. Erwin, Obermayer and Schulten (1992) showed that no energy function exists in the general case.

## References
