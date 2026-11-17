---
tag: S76VBE
kind: algorithm
slug: voxel-grid-downsampling
name: Voxel grid downsampling
aliases:
- voxel grid filter
area: computer-vision/point-clouds-and-registration
level: intro
summary: Reduce a point cloud by replacing the points in each cell of a 3D grid with their centroid, in linear expected time with hashing.
model: real-ram
complexity:
  vars: {n: the number of input points, m: the number of occupied voxels}
  time: {worst: Θ(n) expected, average: Θ(n) expected, best: Θ(n)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: true, online: false, recursive: false, order_independent: true, translation_invariant: false}
history:
  year: 1993
  people: [Jarek Rossignac, Paul Borrel]
  note: "Rossignac and Borrel simplified meshes by clustering the vertices on a uniform grid, one representative per cell. Pauly, Gross and Kobbelt (2002) used the same grid clustering on point-sampled surfaces, and the VoxelGrid filter of the Point Cloud Library made the centroid form the standard first step of point cloud pipelines."
prereqs: [point-cloud, hash-table]
see_also: [uniform-grid, spatial-hashing, octree, statistical-outlier-removal, point-cloud-normal-estimation, iterative-closest-point, mesh-simplification, tsdf-fusion]
sources:
  - paper: doi:10.1109/VISUAL.2002.1183771
    title: "Mark Pauly, Markus Gross and Leif P. Kobbelt, Efficient simplification of point-sampled surfaces, IEEE Visualization 2002, 163-170"
    locator: "Section 3.1, Clustering (uniform grid clustering after Rossignac and Borrel, and its two drawbacks: a fixed cell size that does not follow the sampling density, and the joining of parts that are not connected)"
  - paper: "Jarek Rossignac and Paul Borrel, Multi-resolution 3D approximations for rendering complex scenes, in Modeling in Computer Graphics, Springer, 1993"
    locator: "The vertex clustering on a uniform grid"
  - paper: doi:10.1109/ICRA.2011.5980567
    title: "Radu Bogdan Rusu and Steve Cousins, 3D is here: Point Cloud Library (PCL), IEEE International Conference on Robotics and Automation (ICRA), 2011"
    locator: "The library and its filtering module"
---

Voxel grid downsampling makes a [point cloud](/point-cloud/) smaller and more even. It cuts space into equal cubes, called voxels, and replaces all the points that fall in one cube by their average, the centroid. The output has one point per occupied cube, so its density is at most one point per cube, wherever the input was dense. A [hash table](/hash-table/) keyed by the integer index of the cube does the grouping in one pass, in $\Theta(n)$ expected time for $n$ points. It is the usual first step before [normal estimation](/point-cloud-normal-estimation/), [registration](/iterative-closest-point/) and meshing, because it bounds the number of points and evens out the sampling. It is the point cloud form of the vertex clustering used to simplify meshes.

## In plain words

Put a 3D grid of equal boxes over the points, like a stack of ice cube trays. Look at each box. If it is empty, skip it. If it holds points, throw them away and put one new point at their average position.

To do this fast, compute for each point the number of its box from its coordinates: divide by the box size and round down. Keep a table from box numbers to a running total and a count. One pass over the points fills the table, and one pass over the table gives the new points. The result never has two points in one box, so a dense patch near the scanner becomes as sparse as the box size asks.

## The problem

The input is a finite list $P$ of $n$ points in $\mathbb{R}^3$, a voxel size $s > 0$ and an origin $o$. The voxel with integer index $c = (i, j, k)$ is the half-open box $[o_x + is, o_x + (i+1)s) \times [o_y + js, o_y + (j+1)s) \times [o_z + ks, o_z + (k+1)s)$. These boxes cover space without overlap. The output has one point for each voxel that holds at least one input point: the centroid of the input points in that voxel.

There is no single correct downsampled cloud. This is one well-defined rule among many, chosen because it is fast, needs no neighbor search, and moves no point by more than one voxel diagonal.

## The algorithm

```pseudo id=main
VOXEL-DOWNSAMPLE(P, s, o)
L1  cells ← an empty hash table from integer triples to (sum, count)
L2  for each point p in P do
L3      c ← (⌊(p_x - o_x)/s⌋, ⌊(p_y - o_y)/s⌋, ⌊(p_z - o_z)/s⌋)
L4      if c is not in cells then cells[c] ← (0, 0)
L5      add p to the sum and 1 to the count of cells[c]
L6  Q ← an empty list
L7  for each entry (c, sum, count) of cells do
L8      append sum / count to Q
L9  return Q
```

Line L3 is the only geometric step: the floor of each scaled coordinate gives the index of the voxel. Line L5 keeps a running sum and a count, not a list of points, so the table needs one entry per occupied voxel. Line L8 divides once per voxel. Other values that the points carry, such as colors or intensities, are averaged in the same way at line L5.

The grid is never stored. Only the occupied voxels have entries, so a cloud that spans a kilometer with a voxel size of a centimeter costs no more than one that spans a meter, as long as the number of points is the same.

## Example

Take six points in the plane $z = 0$, voxel size $s = 1$ and origin $o = (0, 0, 0)$. All the voxels have $k = 0$, so the table shows only $i$ and $j$.

| point | $(x, y)$ | voxel $(i, j)$ |
|---|---|---|
| $p_1$ | (0.2, 0.1) | (0, 0) |
| $p_2$ | (0.6, 0.3) | (0, 0) |
| $p_3$ | (1.5, 0.2) | (1, 0) |
| $p_4$ | (1.8, 0.9) | (1, 0) |
| $p_5$ | (1.2, 0.4) | (1, 0) |
| $p_6$ | (0.3, 1.7) | (0, 1) |

After the loop, the table holds three entries: voxel $(0, 0)$ with sum $(0.8, 0.4)$ and count 2, voxel $(1, 0)$ with sum $(4.5, 1.5)$ and count 3, and voxel $(0, 1)$ with sum $(0.3, 1.7)$ and count 1. Line L8 gives the three output points $(0.4, 0.2)$, $(1.5, 0.5)$ and $(0.3, 1.7)$. Six points became three. Each output point lies in its own voxel, and the single point $p_6$ is kept as it is.

## Correctness

By the definition of the floor, line L3 gives the index $c$ exactly when the point lies in the half-open voxel $V(c)$, so each point goes to exactly one voxel. An induction on the loop of line L2 shows that after $t$ points the table holds, for each voxel met so far, the sum and the count of the first $t$ points in it. At the end, line L8 returns the centroid of each occupied voxel. A voxel is convex, so the centroid lies in the same voxel, and every input point is less than $s\sqrt{3}$, the voxel diagonal, from the output point of its voxel. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/) with the floor function and a hash table on integer keys. Let $m$ be the number of occupied voxels, with $m \le n$.

- **Time.** Line L3 costs $O(1)$ per point, and each lookup or insertion at lines L4 and L5 costs $O(1)$ expected with a good hash function. The total is $\Theta(n)$ expected. With a sort of the keys in place of the hash table, the time is $O(n \log n)$ in the worst case, or $O(n)$ with a [radix sort](/radix-sort/) on bounded integer keys.
- **Space.** $\Theta(m)$ extra for the table and the output.

No neighbor search is needed, so this is cheaper than any filter that looks at the $k$ nearest neighbors of each point, such as [statistical outlier removal](/statistical-outlier-removal/).

## Properties

- **Order independent.** The set of output points does not depend on the order of the input. Only the order of the output does.
- **Not translation invariant.** The output depends on where the grid starts. Moving the origin by half a voxel can split one cluster into two or join two clusters.
- **Bounded error.** Each input point is within one voxel diagonal, $s\sqrt{3}$, of its representative.
- **New points.** The centroids are usually not input points. On a curved surface, the centroid lies slightly inside the curve, not on the surface.
- **Density cap, not density target.** The output has at most one point per voxel. Sparse regions stay sparse, so the result is even only where the input was denser than the grid.

## Variants and improvements

- **Voxel centers.** Output the center of each occupied voxel in place of the centroid. This is cheaper and puts the points on a regular grid, but it moves points by up to half a diagonal even on a flat, dense surface.
- **Nearest input point.** Keep the input point closest to each centroid. The output is then a subset of the input, which keeps the original attributes and avoids points between surfaces.
- **Sort in place of hashing.** Compute all keys, sort them, and average each run of equal keys. This is deterministic, uses less memory per point and runs well on GPUs. Packing the three indices into one integer, or into a [Z-order](/z-order-curve/) key, makes the sort cheap.
- **Minimum count.** Drop the voxels with fewer than a set number of points. This also removes isolated points, a crude form of [outlier removal](/statistical-outlier-removal/).
- **Adaptive cells.** An [octree](/octree/) that splits a cell only while its points do not fit a plane keeps more points where the surface bends. Pauly, Gross and Kobbelt (2002) give hierarchical and incremental clustering of this kind.
- **Unit normals.** If the points carry normals, average them at line L5 and normalize at line L8, or estimate the normals again on the output.

## When to use it

Use a voxel grid filter to reduce a large cloud to a size that later steps can handle, to make the density more even before a fixed radius search, and to make the input of [ICP](/iterative-closest-point/) or [feature descriptors](/point-feature-histograms/) independent of the distance to the sensor. Choose the voxel size from the detail you need: a feature smaller than a voxel is lost. Use an adaptive method when the surface has both large flat parts and small detailed parts. Do not use it when every original sample must be kept, for example to measure noise.

## Pitfalls

- **Truncation in place of the floor.** Writing $\mathrm{int}((p_x - o_x)/s)$ at line L3 rounds toward zero, so the points in $(-s, 0)$ and in $[0, s)$ get the same index, and the voxel at the origin is twice as wide. Use the floor, or put the origin at the minimum corner of the bounding box so that all indices are at least zero.
- **Packed keys that overflow.** Many programs pack the three indices of line L3 into one 32-bit or 64-bit integer. If the cloud spans more voxels along an axis than the field holds, different voxels share a key and their points are averaged together. Check the extent divided by $s$ against the field width.
- **Large coordinates.** In floating point, $p_x - o_x$ loses digits when the coordinates are large, as with georeferenced lidar. Points near a voxel face then go to the wrong side. Subtract a local origin first.
- **Averaging normals as points.** Summing unit normals at line L5 gives a short vector, and normals of opposite sign cancel. Normalize at line L8, or estimate normals after downsampling.
- **One voxel across two surfaces.** A voxel that holds points of two surfaces, for example both sides of a thin wall, gets one centroid between them, in empty space. Use a voxel smaller than the thinnest part, or keep the nearest input point.

## Implementations

## History

Rossignac and Borrel (1993) simplified triangle meshes by clustering the vertices on a uniform grid and keeping one representative vertex per cell. Pauly, Gross and Kobbelt (2002) studied the simplification of point-sampled surfaces and listed this uniform grid clustering as the simplest method, with its two weak points: the cell size does not adapt to the sampling density, and points of parts that are not connected can fall into one cell. The VoxelGrid filter of the Point Cloud Library (Rusu and Cousins, 2011), which replaces the points of each voxel by their centroid, made the method the standard first step of point cloud processing in robotics.

## References
