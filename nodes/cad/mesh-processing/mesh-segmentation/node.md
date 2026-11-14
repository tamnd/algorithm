---
tag: 4350RM
kind: problem
slug: mesh-segmentation
name: Mesh segmentation
aliases:
- mesh partitioning
area: cad/mesh-processing
level: core
summary: Partition the faces of a mesh into connected parts that are meaningful, such as near-planar charts or the limbs of a shape.
prereqs: [manifold-mesh, graph-partitioning-problem]
see_also: [mesh-parameterization, least-squares-conformal-maps, normalized-cut, spectral-clustering, k-means, region-growing, watershed-segmentation, image-segmentation-graph-cuts]
sources:
  - paper: doi:10.1111/j.1467-8659.2007.01103.x
    title: Ariel Shamir, A survey on mesh segmentation techniques, Computer Graphics Forum 27(6), 2008, 1539 to 1556
    locator: segmentation as an optimization problem with no single objective, the two types (part segmentation and surface-patch segmentation), and the classification of methods by goal, criteria and technique
  - paper: doi:10.1145/1015706.1015817
    title: David Cohen-Steiner, Pierre Alliez and Mathieu Desbrun, Variational shape approximation, ACM Transactions on Graphics 23(3), 2004, 905 to 914
    locator: the partition of a mesh into regions with planar proxies, and the normal-based error metric L^{2,1}
---

Mesh segmentation is the problem of dividing the faces of a mesh into connected groups, called segments, parts or charts, so that each group is meaningful for a task. For texture mapping, the groups are charts that can be flattened with little distortion. For simplification and reverse engineering, they are regions close to a plane or another simple surface. For modelling and shape analysis, they are the parts a person would name, such as the legs, the seat and the back of a chair. There is no single objective that covers all of these, as Ariel Shamir's 2008 survey stresses: the problem is a family of optimization problems, one for each chosen criterion, and the "right" answer depends on the use.

## In plain words

A mesh is a surface made of many small triangles. Segmentation colours the triangles, one colour per region, so that each region is all in one piece and makes sense. What makes sense depends on the job.

To wrap a picture around a model, you want regions that lie almost flat, so the picture does not stretch. To describe a model to a person, you want regions like "arm" and "head". These two goals give different answers for the same model.

So segmentation is not one problem with one best answer. You first choose what a good region is, and then you look for the best regions by that rule.

## Definition

**Input.** A connected triangle mesh $M$ with face set $F$, an oriented [manifold mesh](/manifold-mesh/) whose faces are oriented so that the outward normal follows the right-hand rule. Two faces are *adjacent* if they share an edge; this gives the dual graph $D(M)$, whose nodes are the faces.

**Output.** A partition of $F$ into sets $S_1, \ldots, S_k$, the segments, such that each $S_i$ induces a connected subgraph of $D(M)$.

**Objective.** A segmentation problem fixes a cost and constraints, and asks for a partition of least cost. Shamir sorts the common choices into two types.

- **Surface-patch segmentation.** Each segment should be close to a simple surface or be easy to flatten. Typical costs: the distance of the faces to a best-fitting plane or quadric, the deviation of the face normals from a proxy normal, or the distortion of a flattening of the segment. Typical constraints: each segment is a topological disk, has bounded size, or has bounded distortion.
- **Part segmentation.** Segments should be the parts of the shape. Typical costs prefer boundaries along concave creases (the minima rule of perception), short boundaries, and parts of similar thickness. Typical constraints: the number of parts.

Both add terms for the number of segments and for the length or smoothness of the boundaries. A cost without such a term is minimized by one segment per face or by a single segment.

**Example cost.** For patches with planar proxies, Cohen-Steiner, Alliez and Desbrun use $L^{2,1}(S_i, n_i) = \sum_{T \in S_i} \mathrm{area}(T)\, |n_T - n_i|^2$, where $n_T$ is the unit normal of $T$ and $n_i$ a unit proxy normal chosen for the segment, and they minimize the sum over the segments for a given $k$.

**Normals and creases.** Many costs use face normals and the sign of the dihedral angle between adjacent faces. A crease is concave when the far vertex of one triangle lies on the outer side of the plane of the other, which is the sign of ORIENT3D, the [orientation test](/orientation-test/). For nearly flat creases or sliver triangles, this sign and the normals suffer from [catastrophic cancellation](/catastrophic-cancellation/) in floating point. [Exact predicates](/shewchuk-expansion-sum/) settle the sign, but the normal of a sliver stays unreliable, which is one face of the [robustness problem](/geometric-robustness-problem/). Segmentations are usually measured to tolerate this noise, not proved correct under it.

**A different problem with a similar name.** In scientific computing, a finite element mesh is split into pieces of nearly equal size, one per processor, with few faces or elements on the cuts between pieces, to run a simulation in parallel. That is the [graph partitioning problem](/graph-partitioning-problem/) on the dual graph, with balance and cut size as the only goals; it is not about meaningful parts and is not covered here.

## Variants

- **Charts for parameterization.** Segments must be disks that flatten with low distortion, with short seams; this is the first step of [mesh parameterization](/mesh-parameterization/) of a closed surface.
- **Planar or developable patches.** Segments must be close to planes or to developable surfaces, for simplification, for fabrication from flat sheets, or for fitting CAD surfaces.
- **Semantic parts.** Segments must match the parts a person would name; ground truth comes from people, and results are compared on benchmarks.
- **Hierarchical segmentation.** A tree of segments at several levels of detail.
- **Co-segmentation.** A consistent segmentation of a set of similar shapes.
- **Fixed or free number of segments.** $k$ is given, or the cost includes a price per segment.

## Examples

**A cube.** Triangulate the unit cube with 12 triangles, two per square face. The dual graph has 12 nodes and 18 edges. With the planar cost $L^{2,1}$ and $k = 6$, the six square faces, two triangles each, are a segmentation with cost 0, and the seams are the 12 cube edges, of total length 12. With fewer than 6 segments the cost is positive, because some segment then holds triangles with two different normals.

**The same cube for texture mapping.** For charts that flatten without distortion, two segments are enough: the strip of front, top and back faces, and the strip of left, bottom and right faces. Each strip unfolds onto a $1 \times 3$ rectangle with no distortion, and the seams between the strips are 8 cube edges, of total length 8. So the best answer for planar patches (6 segments) and the best answer for low-distortion charts with short seams (2 segments) differ on the same input.

**A chair.** A part segmentation separates the legs, the seat and the back, along the concave creases where they meet. A planar segmentation of the same chair splits the curved back into many small near-planar patches and may join the seat with the tops of the legs where they are flush.

## Known algorithms

| method | type | idea | guarantee |
|---|---|---|---|
| [region growing](/region-growing/) | patches | grow segments from seed faces while a test of flatness or curvature holds | each segment meets the test; the result depends on the seeds |
| [watershed segmentation](/watershed-segmentation/) on a curvature function over the faces | patches and parts | flood from the minima of the function | over-segmentation, usually followed by merging |
| variational shape approximation (Cohen-Steiner, Alliez and Desbrun 2004) | patches | alternate between fitting a proxy plane to each segment and reassigning faces by flooding, in the style of [k-means](/k-means/) | the error usually decreases; a local optimum |
| hierarchical face clustering (Garland, Willmott and Heckbert 2001) | patches | merge adjacent segments in order of the cost of merging | a hierarchy; greedy |
| [spectral clustering](/spectral-clustering/) and [normalized cut](/normalized-cut/) on the dual graph | parts | cut the graph where the weights of the dual edges (from dihedral angles and distances) are small, by eigenvectors of a graph Laplacian | a relaxation of an NP-hard cut problem |
| graph cuts, as in [image segmentation](/image-segmentation-graph-cuts/) | parts | refine the boundary between two fuzzy regions by a minimum cut | the cut is optimal for its local problem |
| shape diameter function and learning methods | parts | label faces by local thickness or by a classifier trained on segmented examples | measured on benchmarks |

The [least squares conformal maps](/least-squares-conformal-maps/) paper of Lévy and coauthors also segments the surface into charts, which it grows from seeds so that their borders meet along feature curves of high curvature.

## Bounds

- **Proved.** Checking that a partition is valid, each segment connected in the dual graph, takes $O(|F|)$ time with a breadth-first search. Several common forms are NP-hard: the minimum [normalized cut](/normalized-cut/) of a graph (Shi and Malik 2000), balanced [graph partitioning](/graph-partitioning-problem/), and [k-means clustering](/k-means-np-hardness/). So the methods that optimize such costs over all partitions use relaxations or local search, and give no global guarantee.
- **No canonical answer.** Without a fixed cost there is no best segmentation, as the cube shows, and no single complexity.
- **Measured.** Part segmentations are compared with human segmentations on benchmarks, with measures such as the cut discrepancy and the Rand index; these results are measured, not proved.

## Reductions

- **To graph partitioning.** With a cost that is a sum over the dual edges that are cut, plus a balance or count term, segmentation is a weighted [graph partitioning problem](/graph-partitioning-problem/) on the dual graph.
- **To clustering.** With a cost that is a sum over faces of a distance to a segment proxy, it is a clustering problem like [k-means](/k-means/), with the extra condition that clusters are connected.
- **From image segmentation.** A pixel grid is a mesh of squares in the plane, so image segmentation methods, [watershed](/watershed-segmentation/) and graph cuts, carry over to meshes.
- **Into parameterization.** Charts from a segmentation are the disks that [mesh parameterization](/mesh-parameterization/) flattens.

## Applications

- **Texture atlases.** Charts are flattened and packed into one image.
- **Simplification and remeshing.** Planar patches become large flat faces of a coarse mesh, as in variational shape approximation.
- **Reverse engineering.** A scanned mesh is split into regions that are fitted by planes, cylinders and free-form surfaces to rebuild a CAD model.
- **Fabrication.** Developable charts are cut from flat sheets of metal, paper or cloth.
- **Shape analysis.** Parts support retrieval, correspondence, skeleton extraction for animation, and editing by parts.

## References
