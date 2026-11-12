---
tag: JNG669
kind: data-structure
slug: photon-map
name: Photon map
area: graphics-and-signals/ray-tracing
level: advanced
summary: The store of photon hits for photon mapping. A left-balanced kd-tree in a flat array, with no pointers, that returns the k nearest photons around a point for a density estimate.
implements: [spatial-index]
model: real-ram
complexity:
  vars: {n: the number of photons, k: the number of photons asked for, h: the height of the tree}
  time: {build: "O(n log n) expected", nearest: O(n log k), height: Θ(log n)}
  space: {total: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1996
  people: [Henrik Wann Jensen]
  note: Jensen stored the photons of his two-pass global illumination method in a balanced kd-tree and estimated radiance from the nearest photons.
prereqs: [kd-tree, kd-tree-nearest-neighbor-search, binary-heap]
see_also: [photon-mapping, progressive-photon-mapping, k-nearest-neighbor-search, spatial-hashing, quickselect, final-gathering, irradiance-caching]
sources:
  - paper: doi:10.1007/978-3-7091-7484-5_3
    title: Henrik Wann Jensen, Global illumination using photon maps, Rendering Techniques '96 (Proceedings of the 7th Eurographics Workshop on Rendering), Springer, 1996, 21 to 30
    locator: the photon map as a balanced kd-tree and the radiance estimate from the nearest photons
  - book: isbn:9781568811475
    title: Henrik Wann Jensen, Realistic Image Synthesis Using Photon Mapping, AK Peters, 2001
    locator: Chapter 6, The Photon Map Data Structure, Section 6.3 The Balanced Kd-Tree and Section 6.4 Locating the Nearest Photons Efficiently
  - paper: doi:10.1145/361002.361007
    title: Jon Louis Bentley, Multidimensional binary search trees used for associative searching, Communications of the ACM 18(9), 1975, 509 to 517
    locator: the kd-tree and the search that skips subtrees on the far side of a splitting plane
  - paper: doi:10.1145/355744.355745
    title: Jerome H. Friedman, Jon Louis Bentley and Raphael A. Finkel, An algorithm for finding best matches in logarithmic expected time, ACM Transactions on Mathematical Software 3(3), 1977, 209 to 226
    locator: the k nearest neighbor search in a kd-tree with a bound that shrinks as neighbors are found
---

A photon map stores the points where photons hit surfaces in [photon mapping](/photon-mapping/), with the power and the incoming direction of each photon. Jensen built it as a [kd-tree](/kd-tree/) that is *left-balanced*: it is a complete binary tree, stored in a flat array like a [binary heap](/binary-heap/), so the node at index $i$ has its children at $2i$ and $2i+1$ and the tree needs no pointers. Each node splits along the axis in which its photons spread the most. The main query returns the $k$ photons nearest to a point within a maximum radius, which is a [k-nearest neighbor search](/kd-tree-nearest-neighbor-search/) with a bounded max-heap. The renderer divides their total power by the area $\pi r^2$ of the disc that holds them.

## In plain words

Photon mapping shoots millions of small packets of light from the lamps and records each place where one lands. Later, to know how bright a spot is, the renderer looks at the packets near that spot. Many packets close together mean a bright spot.

The photon map is the box that holds the packets so that the renderer can find the near ones fast. It cuts the space in two halves with a plane, so that each half has the same number of packets. It cuts each half again, and so on. To find the packets near a spot, it looks first in the half that holds the spot. It looks in the other half only if that half can still hold a packet nearer than the ones it already has.

## The abstract type

A photon map holds a fixed set of $n$ photons, each a point $x_p \in \mathbb{R}^3$ with a power $\Delta\Phi_p$ and a direction $\omega_p$. It is built once, after the photon pass, and is then read only. It supports these queries:

- **k-nearest.** For a point $x$, a count $k$ and a radius $r_{\max}$, return the $\min(k, m)$ photons nearest to $x$, where $m$ is the number of photons closer than $r_{\max}$.
- **In radius.** Return all photons closer to $x$ than a radius $r$.
- **Density estimate.** Return $\sum_p \Delta\Phi_p / (\pi r^2)$ over the k-nearest photons, with $r$ the distance to the farthest of them.

## Representation

The tree has $n$ nodes in an array $heap[1 \ldots n]$, one photon per node, with no empty slots. Node $i$ stores a photon and the axis $axis[i] \in \{x, y, z\}$ of its splitting plane. All photons in the subtree of $2i$ have a coordinate at most that of $heap[i]$ on that axis, and all photons in the subtree of $2i + 1$ have a coordinate at least that. The tree is complete, so its height is $\lfloor \log_2 n \rfloor$, and the left subtree of a tree with $n$ nodes has

$$\text{LEFT-SIZE}(n) = (2^{h-1} - 1) + \min(n - 2^h + 1,\ 2^{h-1}), \qquad 2^h \le n < 2^{h+1},$$

nodes, for $n \ge 2$. The root of each subtree is the photon of rank $\text{LEFT-SIZE}$ along the axis. This is the median when the last level is half full, and close to it otherwise. A compact photon record stores the position in three floats, the power in shared-exponent form and the direction in two bytes of spherical angles.

## Operations

```pseudo id=main
BUILD(P)                                   ▷ P is the list of n photons
L1  S ← a stack holding (1, P)
L2  while S is not empty do pop (i, Q)
L3      a ← the axis of the largest extent of the bounding box of Q
L4      m ← LEFT-SIZE(|Q|)
L5      select the photon q of rank m in Q along axis a; Q< ← the m photons before q, Q> ← the photons after q
L6      heap[i] ← q, axis[i] ← a
L7      push (2i, Q<) and (2i + 1, Q>) on S if they are not empty

K-NEAREST(x, k, r_max)
L8  H ← an empty max-heap keyed by squared distance, d2max ← r_max²
L9  S ← a stack holding (1, 0); while S is not empty do pop (i, b)    ▷ b ≤ the squared distance from x to the region of i
L10     if i > n or b ≥ d2max then continue
L11     δ ← x[axis[i]] − heap[i][axis[i]]
L12     push (far child, max(b, δ²)), then push (near child, b)       ▷ near is 2i if δ < 0, else 2i + 1
L13     d² ← ‖x − heap[i]‖²; if d² < d2max then insert (d², i) into H, and if |H| > k remove its largest
L14     if |H| = k then d2max ← the largest key in H
```

Line L5 is a [quickselect](/quickselect/) along one axis. It puts the photon of rank $m$ in place and the smaller and larger ones on the two sides in linear expected time, so the build needs no full sort. In the query, the near child is popped first. So the search reaches the leaf region of $x$ quickly, $H$ fills, the bound $d2max$ shrinks, and line L10 then skips far subtrees.

## Example

Ten photons lie in the plane $z = 0$ at the points $(2,3)$, $(5,4)$, $(9,6)$, $(4,7)$, $(8,1)$, $(7,2)$, $(1,8)$, $(6,9)$, $(3,1)$ and $(9,9)$. The bounding box spans 8 in $x$ and 8 in $y$, so the root splits on $x$. LEFT-SIZE$(10) = 6$, so the root is the photon of rank 6 in $x$, counting from 0, which is $(7, 2)$. Six photons go to the left and three to the right. BUILD gives this array:

| index | photon | axis | children |
|---|---|---|---|
| 1 | (7, 2) | x | 2, 3 |
| 2 | (4, 7) | y | 4, 5 |
| 3 | (9, 6) | y | 6, 7 |
| 4 | (3, 1) | x | 8, 9 |
| 5 | (6, 9) | x | 10 |
| 6 | (8, 1) | leaf | |
| 7 | (9, 9) | leaf | |
| 8 | (2, 3) | leaf | |
| 9 | (5, 4) | leaf | |
| 10 | (1, 8) | leaf | |

Query K-NEAREST$((8.6, 7), 2, \infty)$:

| pop | photon | $d^2$ | far child pushed with bound | $d2max$ after |
|---|---|---|---|---|
| node 1 | (7, 2) | 27.56 | node 2, bound 2.56 | $\infty$ |
| node 3 | (9, 6) | 1.16 | node 6, bound 1.00 | 27.56 |
| node 7 | (9, 9) | 4.16 | none | 4.16 |
| node 6 | (8, 1) | 36.36 | none | 4.16 |
| node 2 | (4, 7) | 21.16 | node 4, bound 2.56 | 4.16 |
| node 5 | (6, 9) | 10.76 | node 10, bound 6.76 | 4.16 |
| node 10 | skipped, bound 6.76 ≥ 4.16 | | | |
| node 4 | (3, 1) | 67.36 | node 8, bound 31.36 | 4.16 |
| node 9 | (5, 4) | 21.96 | none | 4.16 |
| node 8 | skipped, bound 31.36 ≥ 4.16 | | | |

The answer is $(9, 6)$ at squared distance 1.16 and $(9, 9)$ at 4.16. With unit powers, the density estimate is $2 / (\pi \cdot 4.16) = 0.153$ per unit area.

## Correctness

The build is correct by induction on the stack: each popped pair $(i, Q)$ fills node $i$ with a photon $q$ of $Q$ and pushes the two parts of $Q \setminus \{q\}$ to the children of $i$. The selection of line L5 puts each photon of $Q_<$ at or below $q$ on axis $a$ and each photon of $Q_>$ at or above it, which is the search tree order. The sizes are $m = \text{LEFT-SIZE}(|Q|)$ and $|Q| - 1 - m$, which are the sizes of the subtrees of $2i$ and $2i + 1$ in a complete tree, so each index from 1 to $n$ gets one photon. For the query, the value $b$ pushed with a node is a lower bound on the squared distance from $x$ to every photon in its subtree, because that subtree lies on the far side of each plane it was pushed across. A subtree is skipped only when $b \ge d2max$, and then none of its photons can enter $H$. The full proof is in the proof file.

## Complexity

- **Build.** Each level of the tree splits disjoint parts of the photon list, and lines L3 and L5 take linear expected time in the size of a part. There are $\lfloor \log_2 n \rfloor + 1$ levels, so the build takes $O(n \log n)$ expected time. With a linear time worst case selection, such as median of medians, it is $O(n \log n)$ in the worst case.
- **Space.** The array holds $n$ photons and $n$ axis values, with no pointers, so the space is $\Theta(n)$. The stack holds $O(\log n)$ entries.
- **k-nearest.** Each pop costs $O(1)$, and each insertion in $H$ costs $O(\log k)$. In the worst case the query visits all $n$ nodes, for example when all photons lie on a sphere around $x$. For photons spread with a smooth density on surfaces, the analysis of Friedman, Bentley and Finkel gives a logarithmic expected number of visited nodes for a fixed $k$, under their random model. Photon maps are not random in this sense, so this cost is observed, not proved.

## Variants

- **Separate maps.** Jensen keeps a *caustic map* for paths of the form light, specular, diffuse, a *global map* for all diffuse hits, and a *volume map* for photons in participating media. The caustic map is viewed directly and needs many photons. The global map is viewed through [final gathering](/final-gathering/).
- **Disc and filter.** Flatten the search sphere to a disc in the plane of the surface to reduce leaks from nearby surfaces. Weight the photons with a cone or a Gaussian filter to sharpen caustic edges.
- **Precomputed irradiance.** Store an irradiance value at a subset of photons and return the nearest one. Christensen described this in 1999 to make final gathering faster.
- **Hash grid.** [Progressive photon mapping](/progressive-photon-mapping/) and GPU renderers often use a [spatial hash](/spatial-hashing/) with a cell size equal to the search radius. The in-radius query then reads 8 cells in 3D. It needs no build sort, but it suits only a fixed radius.
- **Other trees.** A BVH over photon discs, or a tree with pointers, allows photons of different radii.

## When to use it

Use a photon map when you need the k nearest photons, with an adaptive radius that is small where photons are dense and large where they are sparse. This is the original photon mapping. When the radius is fixed per query or per pass, as in progressive photon mapping and in [vertex connection and merging](/vertex-connection-and-merging/), a hash grid is simpler and often faster. For general k-nearest search in other dimensions, see [k-nearest neighbor search](/k-nearest-neighbor-search/).

## Pitfalls

- **No maximum radius.** In a dark area the k nearest photons can be very far away, on other surfaces. Always give $r_{\max}$, and return fewer than $k$ photons if needed.
- **The bias of k-nearest.** For photons of a constant density $\lambda$ on a plane, the estimate $k/(\pi r_k^2)$ has the mean $\lambda k/(k-1)$, because the area $\pi r_k^2$ of the $k$-th neighbor follows a gamma law. The estimate $(k-1)/(\pi r_k^2)$ has the mean $\lambda$. For $k = 10$ the plain estimate is 11 percent too high. The tests measure this.
- **Leaks across surfaces.** A sphere around a point near a corner also collects photons on the other wall. Check the normal of each photon, or use a disc.
- **A bad pivot in the selection.** Quickselect with a fixed pivot rule can take quadratic time on adversarial input, for example many photons in a sorted order. Use a random pivot or median of medians.
- **One-based indexing.** The heap layout uses indices 1 to $n$. Mixing it with 0-based children $2i+1$ and $2i+2$ breaks the tree.

## Implementations

## History

Jensen and Christensen used photon maps for caustics and indirect light in 1995, and Jensen presented the two-pass method with a global photon map and a caustic map at the Eurographics Workshop on Rendering in 1996. The balanced kd-tree in heap order and the search for the nearest photons with a max-heap are described in Jensen's book of 2001. The tree goes back to Bentley's kd-tree of 1975, and the k-nearest search with a shrinking bound to Friedman, Bentley and Finkel in 1977.

## References
