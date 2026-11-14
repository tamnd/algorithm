---
tag: FG99C0
kind: algorithm
slug: midsurface-extraction
name: Mid-surface extraction
aliases:
- midsurface abstraction
- dimensional reduction of thin solids
area: cad/cad-cae-integration
level: advanced
summary: Replaces a thin-walled solid by its mid-surface with thickness attributes, by pairing opposite faces or by the medial axis, so shell elements can model it.
model: real-ram
complexity:
  vars: {n: number of boundary samples, k: largest number of shrink steps for one sample, m: number of kept medial points}
  time: {worst: "O(n^2 k + m^2)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1996
  people: [Mohsen Rezayat]
  note: Rezayat named midsurface abstraction in 1996 and built it by pairing opposite faces of the solid. Medial axis methods use the skeleton of Blum (1967) instead, and Ma, Bae and Choi gave the shrinking ball construction for sampled boundaries in 2012.
prereqs: [medial-axis]
see_also: [medial-surface-of-a-solid, medial-axis-decomposition-meshing, defeaturing, feature-recognition, isogeometric-kirchhoff-love-shell, hausdorff-distance, kd-tree-nearest-neighbor-search, straight-skeleton]
sources:
  - paper: doi:10.1016/0010-4485(96)00018-8
    title: M. Rezayat, Midsurface abstraction from 3D solid models, general theory and applications, Computer-Aided Design 28(11), 1996, 905 to 915
    locator: the whole paper (pairing of opposite faces, construction of the midsurface patches, and their joining)
  - paper: doi:10.1007/s00371-011-0594-7
    title: J. Ma, S. W. Bae and S. Choi, 3D medial axis point approximation using nearest neighbors and the normal field, The Visual Computer 28(1), 2012, 7 to 19
    locator: the whole paper, the shrinking ball algorithm that this page implements in 2D, and its pruning by the separation angle
  - paper: doi:10.1016/j.cad.2008.11.009
    title: A. Thakur, A. G. Banerjee and S. K. Gupta, A survey of CAD model simplification techniques for physics-based simulation applications, Computer-Aided Design 41(2), 2009, 65 to 80
    locator: the part of the survey on dimensional reduction, which covers midsurface methods by face pairing and by the medial axis
---

A thin-walled part, such as a sheet metal bracket, a plastic housing or a ship hull, is a solid whose thickness $t$ is small compared with its other sizes. A mesh of solid elements through such a thin wall needs several small elements across $t$, so it is large. Shell elements, such as [isogeometric Kirchhoff-Love shells](/isogeometric-kirchhoff-love-shell/) or [subdivision shells](/subdivision-shell-elements/), model the wall by a surface with a thickness value instead. Mid-surface extraction builds that surface from the CAD solid: the surface halfway between the two faces of the wall, with the local thickness at each point. There are two families. Face pairing finds pairs of opposite faces and offsets one of them by half the distance (Rezayat 1996). Medial methods take the [medial axis](/medial-axis/) in 2D or the [medial surface](/medial-surface-of-a-solid/) in 3D and remove its branches that do not belong to the wall. This page gives the medial method on sampled boundaries in 2D, where the mid-surface is a midline of a cross-section, proves that it is exact on a strip and an annular sector, proves the error when the samples on the two sides do not line up, and measures the result.

## In plain words

Think of a thin plate. For a strength check, engineers like to replace it by a flat sheet with no thickness that runs through its middle, and to write the thickness on the sheet as a number. The computation on the sheet is much faster.

To find the middle, roll a ball inside the part so that it always touches both faces of the wall. The center of the ball traces the middle, and the size of the ball gives the thickness.

The method here starts at each point of the border with a huge ball that touches it, then shrinks the ball until no other border point is inside. The final ball touches a second point, usually on the other face. Balls that touch two points on nearly opposite sides belong to the middle. Balls that touch two neighbors near a corner are thrown away.

## The problem

The input is a region $\Omega \subset \mathbb{R}^2$, the cross-section of a thin wall, given by $n$ samples $p_1, \dots, p_n$ of its boundary and the unit inward normals $n_1, \dots, n_n$ there. The output is a set of polylines that approximate the midline, with a thickness $2r$ at each vertex.

The reference midline is defined by the [medial axis](/medial-axis/): the set of centers of the maximal disks in $\Omega$. A medial point $c$ with radius $r$ touches the boundary in at least two points. Its separation angle is the angle at $c$ between two of them. The midline is the part of the medial axis where this angle is close to $180°$, so that the disk touches two opposite faces of the wall. The other branches run into corners, where the angle is close to $90°$ or smaller, and they are not part of the wall.

For a sample $p$ with inward normal $n$, the disks that touch the boundary at $p$ from inside are $B(r) = \{x : |x - c(r)| \le r\}$ with $c(r) = p + r n$. A sample $q$ lies strictly inside $B(r)$ if and only if $r > \rho(q)$, where

$$ \rho(q) = \frac{|q - p|^2}{2 \, n \cdot (q - p)} \quad \text{if } n \cdot (q - p) > 0, \qquad \rho(q) = \infty \quad \text{otherwise}, $$

is the radius of the circle tangent to the boundary at $p$ through $q$. So the largest disk touching at $p$ that holds no sample in its interior has the radius $\rho^* = \min_{q \ne p} \rho(q)$.

## The algorithm

```pseudo id=main
MIDLINE(samples p_1..p_n, inward normals n_1..n_n, start radius r_0, angle θ_min, radius r_min, link length ℓ)
L1  for i = 1 to n do
L2      c ← p_i + r n_i                     ▷ the center, with r = r_0 at the start
L3      j ← the sample nearest to c
L4      if j = i or |p_j - c| ≥ r then go to L6      ▷ no sample inside the disk
L5      r ← ρ(p_j); go to L2                 ▷ shrink until p_j is on the circle
L6      if a sample p_k touched the disk then θ ← the angle at c between p_i and p_k, else skip p_i
L7      if θ ≥ θ_min and r ≥ r_min then keep (c, 2r)
L8  link the kept centers into polylines, joining centers closer than ℓ
```

Lines L2 to L5 are the shrinking ball of Ma, Bae and Choi (2012). Line L5 shrinks the disk to the circle through the nearest sample $p_j$, and this sample becomes the touching sample $p_k$ of line L6. The loop stops when the nearest sample to the center is on or outside the circle. Line L7 keeps the disks that touch two nearly opposite points, $\theta \ge \theta_{\min}$, and drops the small disks that touch two neighboring samples, $r < r_{\min}$. The code uses $\theta_{\min} = 120°$, $r_{\min} = h$, the largest distance from a sample to its nearest neighbor, and $r_0 = 1000$ times the size of the bounding box. Line L8 builds the connected components of the graph with edges shorter than $\ell$ and walks each from its farthest point by nearest neighbors. The code uses $\ell$ equal to three times the largest gap between consecutive samples. In 3D the same lines give points of the mid-surface, and line L8 becomes the meshing of a point set with a thickness at each point.

## Example

All runs use the code of this page, with fixed inputs.

**A strip.** The strip $[0, 10] \times [-0.5, 0.5]$ has $t = 1$. Its long sides are sampled at spacing $s = 0.1$, at the points $x = 0.05, 0.15, \dots$, and the short sides at the points $y = -0.45, \dots, 0.45$. No sample is a corner. With aligned samples, the same $x$ on both sides:

| run | samples | kept | largest $\lvert y \rvert$ of a center | largest $\lvert r - t/2 \rvert$ | $x$ range | chains |
|---|---|---|---|---|---|---|
| aligned | 220 | 180 | 0 | 0 | 0.55 to 9.45 | 1 |
| top side shifted by $s/2$ | 219 | 181 | 0.00125 | 0.00125 | 0.5 to 9.5 | 1 |
| aligned, no pruning ($\theta_{\min} = 0$, $r_{\min} = 0$) | 220 | 220 | 0.45 | | | |

The aligned run is exact to the last bit. With the shifted side, the error is $s^2 / (8 t) = 0.00125$, the bound of the correctness section, attained. Without pruning, the 40 samples near the ends give disks with a separation angle of exactly $90°$, on the four corner bisectors. The kept centers end at about $x = t/2$ and $x = L - t/2$, not at the ends of the plate. Each midline is one chain with thickness $2r = 1$. The shrinking ball took 1.8 steps per sample on average and 8 at most, from $r_0 = 11000$.

**An annular sector.** The sector $2 \le \rho \le 2.5$, $0 \le \theta \le 90°$ has $t = 0.5$. Both arcs are sampled at the same 120 angles $(k + 1/2) \cdot 0.75°$, and each straight end at 10 points, 260 samples in all. The run keeps 208 centers. All lie on the mean arc $\rho_m = 2.25$ with $r = 0.25$, to $4.4 \times 10^{-16}$. Their angles run from $6.375°$ to $83.625°$, and the exact medial arc starts at $\theta_0 = \arcsin(t / (2 \rho_m)) = 6.379°$ and ends at $90° - \theta_0$, so the kept range matches it within one sample spacing. The midline is one chain.

## Correctness

The proof page proves four facts, with exact arithmetic.

1. **The shrinking ball.** If $\rho^* < r_0$, lines L2 to L5 stop after at most $n - 1$ shrinks with $r = \rho^*$, the largest empty disk that touches at $p_i$. The key fact is that the disks $B(r)$ are nested and that $q$ is inside $B(r)$ exactly when $r > \rho(q)$. If no sample $q$ has $n_i \cdot (q - p_i) > 0$, the disk never shrinks and no sample touches it.
2. **The strip.** For the rectangle $[0, L] \times [-t/2, t/2]$ with $L > t$, the medial axis is the midline segment from $(t/2, 0)$ to $(L - t/2, 0)$, where the separation angle is $180°$, and four corner branches, where it is $90°$. So any $\theta_{\min}$ in $(90°, 180°]$ keeps exactly the segment.
3. **The sampled strip.** Let $p$ be a sample on a long side at distance more than $r^* = t/2 + d^2 / (2 t)$ from both short sides, where $d$ is the smallest offset in $x$ from $p$ to a sample on the other side. Then the algorithm gives the center at distance $d^2 / (2 t)$ from the midline and the radius $r^*$, with the separation angle $180° - 2 \arctan(d / t)$. Aligned samples, $d = 0$, give the exact midline, and samples shifted by $s/2$ give the error $s^2 / (8 t)$.
4. **The annular sector.** If $t < r_1$ and $2 \arcsin(t / (2 r_1)) < \varphi \le 180°$, the points of the medial axis with a separation angle above $90° + \arcsin(t / (2 r_1))$ form exactly the arc $\rho = \rho_m$, $\theta_0 \le \theta \le \varphi - \theta_0$. If both arcs are sampled at the same angles, every arc sample in this range gives a center on that arc with $r = t/2$ exactly.

The tests check facts 1, 3 and 4 and a tapered strip, where $2r$ is the thickness measured normal to the sides. The behavior of the samples near the ends, which the pruning removes, is measured, not proved.

## Complexity

In the [real RAM](/real-ram/) model, with $n$ samples, at most $k$ shrinks per sample and $m$ kept points:

- **Shrinking.** Each step of line L3 is a linear scan, $O(n)$, and each sample takes at most $k + 1$ steps, so lines L1 to L7 cost $O(n^2 k)$. Fact 1 gives $k \le n - 1$, so the worst case is $O(n^3)$. In the example $k = 8$ and the mean is 1.8.
- **Nearest neighbors.** A [kd-tree](/kd-tree-nearest-neighbor-search/) built once over the samples answers line L3 in $O(\log n)$ expected time for well spread samples, so the shrinking costs $O(n k \log n)$ expected after an $O(n \log n)$ build.
- **Linking.** Line L8 compares all pairs, $O(m^2)$, and the default $r_{\min}$ costs $O(n^2)$ by the same scan. Both drop to $O(m \log m)$ and $O(n \log n)$ with a kd-tree.
- **Space.** $O(n)$ for the samples and the kept points.

## Properties

- **Local.** Each sample is processed alone, so the loop of line L1 runs in parallel without change.
- **Thickness for free.** The radius of each kept disk is half the local wall thickness, measured normal to the faces.
- **Needs normals.** The inward normals at the samples must be known. A CAD solid gives them, a scan needs an estimate.
- **Short at free edges.** The medial axis of a wall stops half a thickness before each free edge of the wall, so the result needs an extension there to match the mid-surface that an engineer expects.
- **Not exact.** Sampling, pruning and linking all add errors. Only special shapes with aligned samples come out exactly.

## Variants and improvements

- **Face pairing.** Rezayat (1996) finds pairs of faces of the solid that are close and nearly parallel, builds a midsurface patch between each pair, and then extends and joins the patches across the junctions. It works on the exact CAD surfaces and keeps their type, but the joining step is hard at T-joints and where the thickness changes.
- **Exact medial surfaces.** A [medial surface of a polyhedral solid](/medial-surface-of-a-solid/) can be traced exactly, then pruned in the same way by the angle or by the ratio of the size of a branch to its radius.
- **Shrinking ball in 3D.** Ma, Bae and Choi (2012) give the method for 3D point clouds with normals. The code of this page is its 2D form.
- **Decomposition first.** Split the part into thin regions and thick regions, for example at its medial axis as in [medial axis decomposition meshing](/medial-axis-decomposition-meshing/), and reduce only the thin regions. The thick regions stay solid and are joined to the shells.
- **Defeature first.** Small features such as fillets, holes and ribs break the pairing of faces, so they are often removed by [defeaturing](/defeaturing/) before the extraction.

## When to use it

Use mid-surface extraction when the part is a thin wall, with a ratio of span to thickness of about ten or more, and a shell model is accurate enough for the analysis. Use face pairing when the CAD solid has clean opposite faces. Use a medial method when the faces do not pair well or when only a mesh or a point set is available. Keep solid elements near thick regions, ribs and joints, where the shell assumption fails.

## Pitfalls

- **The free edges.** The medial axis of the strip ends at $x = t/2$, so the shell is too short by $t/2$ at each free edge, as the example shows. Extend the midline to the edge, or the model loses stiffness and mass.
- **Corner branches.** Each convex corner gives a branch with separation angle $90°$ that reaches the midline. Without pruning, they become false shell pieces.
- **Small disks at the samples.** A disk that touches two neighboring samples can pass the angle test. The test $r \ge r_{\min}$, with $r_{\min}$ about the sample spacing, removes them. With $r_{\min} = 0$ and the shifted strip of the example, the code keeps two such disks at the top corners, with radius 0.0625, angle $126.9°$ and centers at $y = 0.45$.
- **Sampling.** The samples on the two faces should be denser than the thickness. With the offset $d$ between the faces, the center moves by $d^2 / (2 t)$, so the error grows fast if the spacing approaches $t$.
- **Junctions.** At a T-joint or a change of thickness, the medial axis has a branch point and the shell needs a connection there. Neither pruning nor linking builds it.
- **Wrong normals.** A flipped normal sends the disk outside the region. Check the orientation before the run.

## Implementations

## History

Blum (1967) introduced the medial axis as a shape descriptor. Rezayat (1996) gave the name midsurface abstraction and built it by pairing faces of the CAD solid. Medial methods for the dimensional reduction of thin solids were developed in parallel, as surveyed by Thakur, Banerjee and Gupta (2009). Ma, Bae and Choi (2012) gave the shrinking ball construction of medial points from samples and normals, which this page uses in 2D.

## References
