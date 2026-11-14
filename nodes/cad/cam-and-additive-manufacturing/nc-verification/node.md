---
tag: AM6X7B
kind: problem
slug: nc-verification
name: NC verification
aliases:
- machining simulation
- NC simulation
area: cad/cam-and-additive-manufacturing
level: core
summary: Simulate a toolpath by subtracting the tool's swept volume from the stock, to show the final part and find gouges, collisions and missed material.
prereqs: [toolpath-planning, cutter-location-data]
see_also: [z-map-model, dexel-representation, swept-volume, gouge-detection, solid-boolean-operations, spatial-occupancy-enumeration, octree, inverse-tool-offset]
sources:
  - paper: doi:10.1016/0010-4485(78)90058-1
    title: Robert O. Anderson, Detecting and eliminating collisions in NC machining, Computer-Aided Design 10(4), 1978, 231 to 237
    locator: the stock and the tool as heights over a grid, and the collision test on it
  - paper: doi:10.1145/15922.15887
    title: Tim Van Hook, Real-time shaded NC milling display, Computer Graphics 20(4) (SIGGRAPH 86), 1986, 15 to 20
    locator: the subtraction of the tool in image space on depth intervals per pixel
  - paper: "Robert B. Jerard, Robert L. Drysdale, Kenneth Hauck, Barry Schaudt and John Magewick, Methods for detecting errors in numerically controlled machining of sculptured surfaces, IEEE Computer Graphics and Applications 9(1), 1989, 26 to 39"
    locator: simulation on vectors along the surface normals and on height grids, and the gouges and excess material each one finds
  - paper: "Robert L. Drysdale, Robert B. Jerard, Barry Schaudt and Ken Hauck, Discrete simulation of NC machining, Algorithmica 4(1), 1989, 33 to 60"
    locator: the cost and the accuracy of point-sample simulation as a function of the grid spacing
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer, 1998
    locator: the part on controlling accuracy and quality, on the z-map model and NC verification
---

NC verification checks a toolpath before it runs on a machine. It simulates the cut: starting from the stock, it removes the volume that the tool sweeps on each move, and then compares the result with the designed part. The comparison finds gouges, where the tool removed material of the part, excess, where material that should go is still there, and collisions, where the holder, the shank or a rapid move hits material. The simulated workpiece is also shown to the user. The task is stated here as a problem. The models that make it fast are on their own pages: the [z-map](/z-map-model/) stores one height per grid point, and the [dexel representation](/dexel-representation/) stores intervals along rays. Exact simulation with [solid Boolean operations](/solid-boolean-operations/) on a boundary representation is possible but slow, so most systems use such sampled models. This is verification of a machining program in mechanical manufacturing, not the verification of a circuit design.

## In plain words

A program for a milling machine is a long list of tool moves, made by a CAM system. Before running it on a costly block of metal, you want to see what it will cut.

The simulation starts with the block. For each move, it removes everything the tool passes through. At the end it holds the shape the machine would make, and you can look at it.

Then it compares that shape with the design. Places where the shape is below the design are gouges. Places above it are material left behind. A move where the holder or a fast move runs into material is a crash.

Most simulators do not keep the exact shape. They sample it on a grid of points or rays, which is fast and simple but only as precise as the grid.

## Definition

**Input.**

- The stock $W_0$, a solid, usually a box.
- The tool: the cutting part $T$, and the non-cutting parts $H$ (shank, holder), placed by a CL point $(c, a)$ as $T(c, a)$ and $H(c, a)$.
- The toolpath: CL points $(c_0, a_0), \dots, (c_m, a_m)$, and for each move $k$ its kind (cutting or rapid). Let $S_k$ be the [swept volume](/swept-volume/) of $T$ over move $k$, and $S^H_k$ that of $H$.
- The design part $P \subseteq W_0$ and a tolerance $\varepsilon \ge 0$.

**Output.**

1. The workpiece after each move, $W_k = W_{k-1} -^* S_k$, where $-^*$ is the [regularized](/regularized-set-operations/) difference. The final part is $W_m$.
2. Gouges: the points of $P$ removed, $P -^* W_m$, reported where their depth below the design surface exceeds $\varepsilon$, with the move that made each one.
3. Excess: the material left, $W_m -^* P$, reported where it is thicker than $\varepsilon$.
4. Collisions: the moves $k$ where $\operatorname{int} S^H_k \cap \operatorname{int} W_{k-1} \ne \emptyset$, and the rapid moves where $\operatorname{int} S_k \cap \operatorname{int} W_{k-1} \ne \emptyset$.

Item 4 depends on the order of the moves, since it uses $W_{k-1}$. Items 1 to 3 at the end depend only on the set of moves, since $W_m = W_0 -^* \bigcup_k S_k$.

**Sampled versions.** A sampled model replaces the solids by their traces on a set of sample lines. On a vertical line $\ell$, $W_k \cap \ell$ is a finite union of intervals. The z-map keeps only the top of the material on each vertical line, which is exact when the tool always comes from above (three axes, no undercut). The dexel model keeps all the intervals. The output is then exact on the sample lines, and says nothing between them.

## Variants

- **Exact solid simulation.** Represent $W_k$ as a boundary representation and subtract each $S_k$ with a [solid Boolean operation](/solid-boolean-operations/). It needs the swept volume as a solid, and the model grows with each move. It is used for short programs or for a final check.
- **Height grids.** The [z-map](/z-map-model/) (Anderson 1978) for three-axis paths. Each move updates the grid points under its footprint.
- **Ray intervals.** The [dexel representation](/dexel-representation/), in screen space for display (Van Hook 1986) or in object space, and three orthogonal dexel grids for parts with steep walls.
- **Vectors normal to the surface.** Jerard et al. (1989) put short vectors on the design surface along its normals, and each move cuts the vectors it meets. The remaining length of a vector is the local excess, and a vector cut below the surface marks a gouge.
- **Voxels and octrees.** A [spatial occupancy enumeration](/spatial-occupancy-enumeration/) or an [octree](/octree/) of the stock, with each move removing the cells inside its swept volume.
- **Five axes.** The tool axis changes during a move, so the swept volume is no longer a translation sweep, and the dexel and voxel models are used.

## Examples

**One move on a z-map.** Take the stock as heights $4$ over a grid of spacing $1$, the design part $z \le 0$, and one move of a ball end mill with a shank, radius $r = 2$, ball center from $(1, 1, 3)$ to $(5, 1, 1)$. On the line $y = 1$, the lowest point of the swept tool above each grid point $x$ is computed on the [z-map page](/z-map-model/):

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| height after the move | 1.268 | 0.764 | 0.264 | -0.236 | -0.736 | -1 | -0.732 | 1 | 4 |
| result | excess | excess | excess | gouge | gouge | gouge | gouge | excess | excess |

The exact values are $3 - \sqrt 3$, $3 - \sqrt 5$, $2.5 - \sqrt 5$, $2 - \sqrt 5$, $1.5 - \sqrt 5$, $-1$, $1 - \sqrt 3$ and $1$. The move goes down to $z = 1$ for the ball center, and the bottom of the ball reaches $z = -1$, below the design. With $\varepsilon = 0.25$ the report is a gouge at $x = 4, 5, 6$ of depth up to $1$, and $x = 3$ is within the tolerance. Between grid points the model knows nothing: the gouge also exists at $x = 3.5$, but a grid of spacing $2$ would only see it at $x = 4$ and $x = 6$.

**A collision.** On the same block, a rapid move of the same tool with ball center from $(0, 4, 3)$ to $(8, 4, 3)$ runs $3 > r$ away from the first cut, where the stock top is still at $4$. The ball bottom is at $1$, so the move crosses material, and the simulation reports a crash at the first grid point under it.

## Known algorithms

- **[Z-map model](/z-map-model/).** One height per grid point. A move of a ball end mill updates each grid point under it in $O(1)$ time by a closed form. Exact on the grid, for three axes.
- **[Dexel representation](/dexel-representation/).** Interval lists on rays, with Boolean operations by a merge in time linear in the number of intervals. Handles undercuts and many tools.
- **Exact Boolean operations.** [Solid Boolean operations](/solid-boolean-operations/) on B-reps or CSG trees, with the swept volume of each move as an operand.
- **Normal vectors.** The method of Jerard et al. (1989), which measures the error directly along the design normals.
- **[Gouge detection](/gouge-detection/).** Checks the CL data against the part without simulating the stock. It finds gouges but not excess material.

What is proved: the sampled models give the exact trace of $W_m$ on their sample lines, up to the rounding of the square roots in the tool formulas. What is measured: the error between the samples and the running time, which depend on the grid spacing, the part and the path. Drysdale et al. (1989) analyse how the cost and the accuracy of point-sample simulation depend on the spacing.

## Bounds

- **Grid models.** With $N$ sample lines, $m$ moves and $N_k$ lines under the footprint of move $k$, a z-map simulation takes $O(N + \sum_k N_k)$ time and $O(N)$ space. A dexel simulation multiplies each update by the number of intervals on the line.
- **Exact models.** The B-rep of $W_k$ gains faces with each move that cuts, so its size can grow with $k$, and each Boolean operation costs more than the one before.
- **Sampling error.** On a grid of spacing $h$, a gouge narrower than $h$ in both directions can fall between the samples. So a sampled check cannot prove that a path is free of gouges. A finer grid, or a direct [gouge detection](/gouge-detection/) on the surface, is needed for that.
- **No hardness.** Every version is a polynomial simulation. The cost question is how many samples or faces it needs.

## Reductions

- **To swept volumes and Boolean operations.** $W_m = W_0 -^* \bigcup_k S_k$, so exact verification is the computation of [swept volumes](/swept-volume/) followed by [regularized set operations](/regularized-set-operations/).
- **To one dimension.** On a sampled model the problem splits into independent problems on the lines: subtract one interval per move and line, and compare the result with the interval of $P$ on the line.

## Applications

- Checking CAM programs for dies, molds and aerospace parts before the first cut.
- Showing the machined part to the programmer, with the errors in color.
- Estimating the removed volume per move, which gives the cutting load and lets a CAM system change the feed rate.
- Checking the output of the post-processor, by simulating the machine code instead of the CL data.

## References
