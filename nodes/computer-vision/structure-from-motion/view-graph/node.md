---
tag: P4TY5D
kind: data-structure
slug: view-graph
name: View graph
aliases:
- epipolar graph
- match graph
area: computer-vision/structure-from-motion
level: advanced
summary: A graph with one vertex per image and an edge for each verified pair, labeled by the relative pose, that global and incremental SfM work on.
model: real-ram
complexity:
  vars: {N: "the number of images (vertices)", E: "the number of verified image pairs (edges)"}
  time: {add_edge: "O(1)", spanning_tree: "O(E log E)", chain_rotations: "O(N)", cycle_error: "O(1)"}
  space: {extra: "O(N + E)"}
properties: {deterministic: true, static: false, exact: true}
history:
  year: 2001
  people: [Venu Madhav Govindu, Noam Levi, Michael Werman, Noah Snavely]
  note: Govindu combined the relative motions of many image pairs on a graph of views. Levi and Werman (2003) studied the viewing graph of fundamental matrices, and Snavely, Seitz and Szeliski used the image graph of large photo collections.
prereqs: [relative-pose-problem, feature-track]
see_also: [rotation-averaging, translation-averaging, global-structure-from-motion, incremental-structure-from-motion, maximum-spanning-tree, pose-graph, image-retrieval, union-find-connectivity]
sources:
  - paper: doi:10.1109/CVPR.2001.990963
    title: "Venu Madhav Govindu, Combining two-view constraints for motion estimation, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2001), vol. 2, 218-225"
    locator: "the whole paper (relative motions on the edges of a graph of views, and the consistency of the motions around cycles)"
  - paper: doi:10.1109/CVPR.2016.445
    title: "Johannes L. Schönberger and Jan-Michael Frahm, Structure-from-motion revisited, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2016), 4104-4113"
    locator: "the correspondence search and the scene graph (images as nodes, verified pairs as edges)"
  - paper: doi:10.1007/978-3-319-10578-9_5
    title: "Kyle Wilson and Noah Snavely, Robust global translations with 1DSfM, Computer Vision ECCV 2014, Lecture Notes in Computer Science, Springer, 2014, 61-75"
    locator: "the problem setup (the graph of pairwise translation directions) and the outlier filter on it"
  - paper: doi:10.1017/S096249291700006X
    title: "Onur Özyeşil, Vladislav Voroninski, Ronen Basri and Amit Singer, A survey of structure from motion, Acta Numerica 26, 2017, 305-364"
    locator: "the sections on the viewing graph, rotation estimation and location estimation"
---

A view graph has one vertex for each image of a reconstruction and one edge for each pair of images that has passed a geometric check. The edge $(i, j)$ stores the relative pose of camera $j$ with respect to camera $i$, a rotation $R_{ij}$ and a unit translation direction $t_{ij}$, as estimated from the [essential matrix](/essential-matrix/) of the pair, and a weight, usually the number of inlier matches. It is the data structure on which [global structure from motion](/global-structure-from-motion/) runs [rotation averaging](/rotation-averaging/) and [translation averaging](/translation-averaging/), and on which [incremental structure from motion](/incremental-structure-from-motion/) picks its first pair and the order of the next images. Its connected components are the parts of the scene that can be reconstructed together, a [maximum spanning tree](/maximum-spanning-tree/) of the weights gives a quick first set of absolute rotations, and the product of the relative rotations around a cycle measures how well the edges agree. The name epipolar graph stresses the two-view geometry on the edges. The name match graph is also used for it, and also for the finer graph of single features from which [feature tracks](/feature-track/) are built.

## In plain words

Draw one dot for each photo. When two photos show the same part of the scene, and the program has checked that their matched points fit one camera motion, draw a line between the two dots. On each line, write how the second camera is turned and in which direction it moved compared with the first one, and how many points support this. That drawing is the view graph. It tells which photos can be put together, which pair is the best place to start, and where a wrong line might be: if you go around a loop of lines and add up the turns, you should come back to where you started. If you do not, one of the lines in the loop is wrong.

## The abstract type

The view graph is an undirected graph $G = (V, E)$ with a label on each directed form of each edge. The operations are:

- **add-view(i)** and **add-edge(i, j, R, t, w)**: insert an image, or a verified pair with the relative pose $(R, t)$ and the weight $w$.
- **remove-edge(i, j)**: delete a pair, for example after an outlier test.
- **relative(i, j)**: return the label $(R_{ij}, t_{ij}, w_{ij})$, in the direction asked for.
- **neighbors(i)**, **edges()** and **components()**: the adjacency queries and the connected components.
- **maximum-spanning-tree()**: a spanning tree, or a forest if $G$ is not connected, of largest total weight.
- **chain-rotations(tree, root)**: absolute rotations along the tree, with $R_{\mathrm{root}} = I$.
- **cycle-error(i, j, k)**: the angle of the rotation $R_{ki} R_{jk} R_{ij}$ around a triangle.

The label convention is the one of the [relative pose problem](/relative-pose-problem/): a point with coordinates $X_i$ in the frame of camera $i$ has the coordinates $X_j = R_{ij} X_i + t_{ij}$ in the frame of camera $j$. With absolute poses $X_c = R_k X + t_k$, this gives $R_{ij} = R_j R_i^{\mathsf T}$ and $t_{ij} = t_j - R_{ij} t_i$, and the essential matrix of the pair is $E_{ij} = [t_{ij}]_\times R_{ij}$. The two-view data fix $t_{ij}$ only up to a positive scale, so it is stored as a unit vector.

## Representation

The reference code stores a dictionary of dictionaries: `adj[i][j]` holds the label of the direction $i \to j$, and `adj[j][i]` holds the label of the reverse direction. Each edge is stored twice so that a walk can leave a vertex along any edge without a test on the direction. The reverse of the label $(R, t)$ is $(R^{\mathsf T}, -R^{\mathsf T} t)$, since $X_i = R^{\mathsf T} X_j - R^{\mathsf T} t$. Large systems store the edges in a flat array with an index from each image pair, and keep the inlier matches of each edge next to its pose, because the later steps need them.

## Operations

```pseudo id=main
ADD-EDGE(G, i, j, R, t, w)
L1  adj[i][j] <- (R, t, w)
L2  adj[j][i] <- (R^T, -R^T t, w)
```

```pseudo id=tree
MAXIMUM-SPANNING-TREE(G)
L3  make each vertex its own set ; T <- empty
L4  for each edge (i, j) in the order of decreasing weight
L5      if FIND(i) != FIND(j)
L6          UNION(i, j) ; add (i, j) to T
L7  return T
```

```pseudo id=chain
CHAIN-ROTATIONS(G, T, root)
L8  R_root <- I ; Q <- a queue holding root
L9  while Q is not empty
L10     i <- the first vertex of Q, removed from Q
L11     for each tree neighbor j of i that has no rotation yet
L12         R_j <- R_ij R_i ; add j to Q
L13 return all R_j

CYCLE-ERROR(G, i, j, k)
L14 return the angle of R_ki R_jk R_ij, that is arccos((trace - 1) / 2)
```

Lines L1 and L2 keep the two directions of an edge consistent. Lines L3 to L7 are Kruskal's method with the largest weights first; ties are broken by the vertex numbers, so the result is deterministic. Lines L8 to L12 walk the tree in breadth-first order and compose the relative rotations, which makes every tree edge exact: $R_j R_i^{\mathsf T} = R_{ij}$. Line L14 composes the three rotations of a triangle; for exact edges the product is $R_i R_k^{\mathsf T} R_k R_j^{\mathsf T} R_j R_i^{\mathsf T} = I$, so the angle is the error of the loop.

## Example

Take 4 images whose cameras turn about the $Z$ axis by $0^\circ$, $10^\circ$, $25^\circ$ and $40^\circ$. The pairs give 5 edges, each written as (pair, relative angle, inliers):

| edge | relative rotation about $Z$ | weight |
|---|---|---|
| $(0, 1)$ | $10^\circ$ | 120 |
| $(0, 2)$ | $25^\circ$ | 95 |
| $(1, 2)$ | $15^\circ$ | 80 |
| $(2, 3)$ | $15^\circ$ | 60 |
| $(1, 3)$ | $35^\circ$ (wrong, the truth is $30^\circ$) | 30 |

Kruskal takes $(0, 1)$ and $(0, 2)$, skips $(1, 2)$ because it closes the cycle $0, 1, 2$, takes $(2, 3)$ and skips $(1, 3)$. The tree is $\{(0, 1), (0, 2), (2, 3)\}$. The chained rotations from root 0 are $0^\circ$, $10^\circ$, $25^\circ$ and $40^\circ$, which are the true ones, because the wrong edge is not in the tree. The cycle error of the triangle $(0, 1, 2)$ is $10^\circ + 15^\circ - 25^\circ = 0^\circ$. The cycle error of the triangle $(1, 2, 3)$ is $15^\circ + 15^\circ - 35^\circ = -5^\circ$, an angle of $5^\circ$, which points at one of the edges $(1, 2)$, $(2, 3)$ or $(1, 3)$. The reverse label of the edge $(1, 3)$ is a rotation by $-35^\circ$ and the translation $-R^{\mathsf T} t$. The reference code gives these numbers.

## Correctness

The reverse label of line L2 is the inverse rigid motion, so both directions describe the same pair (theorem). Lines L3 to L7 return a maximum weight spanning forest by the cut property of spanning trees, the same argument as for the [minimum spanning tree](/minimum-spanning-tree/) with the order reversed (theorem). The chained rotations satisfy every tree edge exactly, and if all edges are exact they equal the true rotations up to the gauge, $R_j = R_j^{\mathrm{true}} (R_{\mathrm{root}}^{\mathrm{true}})^{\mathsf T}$ (theorem). The cycle error is zero for exact edges (theorem), but a zero cycle error does not prove the edges right: two errors can cancel. The proof file below gives the details.

## Complexity

In the real RAM model, add-edge, relative and cycle-error cost $O(1)$, with a hash table for the adjacency. Components cost $O(N + E)$ by [breadth-first search](/breadth-first-search/). The spanning tree costs $O(E \log E)$ for the sort and $O(E\,\alpha(N))$ for the union-find steps. The chained rotations cost $O(N)$, one $3 \times 3$ product per tree edge. Checking all triangles costs $O(E^{3/2})$ with the standard triangle listing, which is fine for thousands of images but not for a dense graph of a million. The space is $O(N + E)$ for the poses; the inlier matches of the edges usually take far more memory than the graph.

## Variants

- **Weights.** The weight can be the inlier count, the ratio of inliers, the triangulation angle of the pair, or a score learned from the data. The maximum spanning tree trusts the weights, so the choice matters.
- **Cycle filtering.** Zach, Klopschitz and Pollefeys (2010) remove edges whose rotation cycles do not close, with a Bayesian test over many cycles. Many global pipelines remove edges whose triangle error is above a few degrees.
- **Skeletal graph.** Snavely, Seitz and Szeliski (2008) select a small subgraph of the images, a skeletal set, that keeps the reconstruction accurate, reconstruct it first and add the rest later.
- **Pose graph.** In SLAM, the edges carry full relative poses with a scale from odometry, and the graph is a [pose graph](/pose-graph/).
- **Triplet graph.** Some global methods use a graph whose vertices are image triplets, so that the relative scales of the translations in a triplet are fixed.
- **Building the graph.** Matching all $N (N - 1) / 2$ pairs is too slow for large sets, so the candidate pairs come from [image retrieval](/image-retrieval/) with a [vocabulary tree](/vocabulary-tree/), from GPS tags, or from the order of a video.

## When to use it

Use a view graph as soon as the input has more than a few images and no known order. It is the input of rotation and translation averaging in global SfM, and incremental SfM uses it to pick the first pair and to see which images can still be registered. For a short video, the graph is mostly a chain with some loop edges, and a [pose graph](/pose-graph/) with relative scales is often the better structure. For a few images that all see each other, a list of pairs is enough.

## Pitfalls

- **Direction conventions.** Mixing $R_{ij} = R_j R_i^{\mathsf T}$ with $R_{ij} = R_i^{\mathsf T} R_j$ is the most common bug. Fix one convention, store both directions, and test the reverse label against the inverse pose.
- **Repeated structures.** Symmetric buildings and repeated windows give wrong edges with many inliers. These edges pass the geometric check, and a maximum spanning tree on inlier counts may trust them; cycle tests or specialized checks are needed.
- **Unknown scale.** The translation of an edge has no length. Chaining translations along a tree, as one chains rotations, is wrong; positions need [translation averaging](/translation-averaging/).
- **Disconnected graphs.** A graph with several components gives several reconstructions in unrelated frames. Reconstruct each component alone, or merge them only with extra data.
- **Weak edges.** An edge with a short baseline has a poor translation direction even if its rotation is good. Store the triangulation angle and use it when the directions are averaged.

## Implementations

## History

Govindu (2001) combined the relative motions of many image pairs on a graph of views and used the consistency of the motions around cycles. Levi and Werman (2003) defined the viewing graph, with fundamental matrices on the edges, and asked which graphs determine all the cameras. In large photo collections, Snavely, Seitz and Szeliski (2006, 2008) organized the images by their matches and used the image graph to find a skeletal set. Global methods since Martinec and Pajdla (2007) and the survey of Özyeşil, Voroninski, Basri and Singer (2017) state rotation and location estimation as problems on this graph, and incremental systems such as COLMAP (Schönberger and Frahm 2016) build a scene graph of the same kind.

## References
