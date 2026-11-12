---
tag: FWMAHV
kind: concept
slug: surface-tessellation
name: Surface tessellation
aliases:
- mesh tessellation
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Turning a smooth surface into a triangle mesh that stays within a given distance of it and has no cracks where patches meet. Second derivative bounds set the step counts.
prereqs: [parametric-surface, polygon-mesh]
see_also: [parametric-surface, polygon-mesh, mesh-generation, marching-cubes, bezier-patch, surface-curvature, disjoint-set-forest, de-casteljau-algorithm]
sources:
  - paper: doi:10.1016/0167-8396(86)90005-1
    title: Daniel Filip, Robert Magedson and Robert Markot, Surface Algorithms Using Bounds on Derivatives, Computer Aided Geometric Design 3(4), 295-311 (1986)
    locator: bounds on the distance between a parametric surface and its piecewise linear approximation from bounds on second derivatives, and their use to choose step sizes
  - paper: doi:10.1016/0146-664x(79)90094-7
    title: Jeffrey M. Lane and Loren C. Carpenter, A Generalized Scan Line Algorithm for the Computer Display of Parametrically Defined Surfaces, Computer Graphics and Image Processing 11(3), 290-297 (1979)
    locator: recursive subdivision of a patch until each piece is flat within a tolerance
  - paper: doi:10.1145/358808.358815
    title: Jeffrey M. Lane, Loren C. Carpenter, Turner Whitted and James F. Blinn, Scan Line Methods for Displaying Parametrically Defined Surfaces, Communications of the ACM 23(1), 23-34 (1980)
    locator: subdivision to flat pieces, and the cracks between neighbor pieces cut to different depths
---

Surface tessellation turns a smooth surface, given as a set of parametric patches, into a mesh of triangles. The mesh is what a GPU draws, what a 3D printer slices and what many geometry algorithms take as input. Two demands set the method: each triangle must stay within a tolerance of the true surface, and the triangles of neighbor patches must meet edge to edge, with no cracks. The first demand fixes how fine each patch must be cut, and the second forces neighbor patches to agree on how they cut their shared edges.

## In plain words

A curved surface is made of many curved pieces. A computer screen can only draw flat triangles, so each curved piece is replaced by a grid of small flat triangles. Small triangles follow the curve closely, but they cost time and memory, so the method picks the size from how much the piece bends and how much error is allowed. Two pieces that touch must cut their common edge into the same number of parts. If one cuts it into eight parts and the other into twelve, the points do not line up, and thin gaps appear between the pieces, through which the background shows. A good tessellation keeps the error small with few triangles and never leaves such a gap.

## The idea

Take a patch $S(u, v)$ on $[0, 1]^2$, for example a [Bézier patch](/bezier-patch/) of degree $(m, n)$ with a net of $(m + 1)(n + 1)$ control points. Cut the domain into $s_u \times s_v$ cells of size $h_u = 1/s_u$ by $h_v = 1/s_v$, cut each cell into two triangles along one diagonal, and map the grid vertices onto the surface. The mesh $T$ is the piecewise linear map that agrees with $S$ at the vertices.

### The chordal error bound

Let $M_{uu}$, $M_{uv}$, $M_{vv}$ bound $|S_{uu}|$, $|S_{uv}|$, $|S_{vv}|$ over the patch. Then at every point of the patch

$$|S(p) - T(p)| \le \frac{M_{uu} h_u^2 + 2 M_{uv} h_u h_v + M_{vv} h_v^2}{8}.$$

Proof: let $p$ be a domain point in a triangle with vertices $p_0, p_1, p_2$, and let $\lambda_i$ be its barycentric coordinates, so $T(p) = \sum \lambda_i S(p_i)$ and $\sum \lambda_i (p_i - p) = 0$. Write $\delta_i = p_i - p = (\alpha_i, \beta_i)$. By Taylor's formula with integral remainder, $S(p_i) = S(p) + DS(p)\, \delta_i + R_i$ with $|R_i| \le \frac12 (M_{uu} \alpha_i^2 + 2 M_{uv} |\alpha_i \beta_i| + M_{vv} \beta_i^2)$. The linear terms cancel in the weighted sum, so $|S(p) - T(p)| = |\sum \lambda_i R_i| \le \frac12 \sum \lambda_i (M_{uu} \alpha_i^2 + 2 M_{uv} |\alpha_i \beta_i| + M_{vv} \beta_i^2)$. In each triangle of the grid the $u$ coordinates of the vertices take only two values, $h_u$ apart, so $\sum \lambda_i \alpha_i^2$ is the variance of a two-point distribution on that span and is at most $h_u^2/4$. In the same way $\sum \lambda_i \beta_i^2 \le h_v^2/4$, and by Cauchy-Schwarz $\sum \lambda_i |\alpha_i \beta_i| \le h_u h_v / 4$. $\square$

For a Bézier patch the bounds come from the net with no search: $S_{uu}$ is a Bézier patch whose control points are $m(m - 1)$ times the second differences of the net in $i$, so by the convex hull property $M_{uu}$ is at most $m(m - 1)$ times the largest of their norms, and the same holds for $M_{uv}$ with $mn$ and the mixed differences, and for $M_{vv}$ with $n(n - 1)$. The bound is sharp: for the bilinear patch $z = uv$ in one cell, $M_{uu} = M_{vv} = 0$, $M_{uv} = 1$, the bound is $1/4$, and at the cell center the patch has height $1/4$ while the diagonal from $(0, 0, 0)$ to $(1, 1, 1)$ has height $1/2$. Bounds of this type go back to Filip, Magedson and Markot (1986).

To choose the steps, use $2 M_{uv} h_u h_v \le M_{uv} (h_u^2 + h_v^2)$: the bound is at most the tolerance $\epsilon$ when $(M_{uu} + M_{uv}) h_u^2 \le 4\epsilon$ and $(M_{vv} + M_{uv}) h_v^2 \le 4\epsilon$, so $s_u = \lceil ((M_{uu} + M_{uv}) / (4\epsilon))^{1/2} \rceil$ and $s_v$ in the same way. The step count grows as $\epsilon^{-1/2}$, so halving the error costs about twice the steps in each direction and four times the triangles.

### No cracks

Two neighbor patches meet along a boundary curve. If both put their vertices at the same parameters along it, the vertices are the same points and the triangles share the edges. If one patch uses 8 steps and the other 12, the two polylines differ between their common points, and the mesh has a crack. The rule is simple: every patch edge has one step count, used by both patches on it. A tensor-product grid uses $s_u$ on both edges $v = 0$ and $v = 1$ and $s_v$ on both edges $u = 0$ and $u = 1$, so the counts are linked across the whole surface. The linked edges form classes, which [union-find](/disjoint-set-forest/) builds in near linear time, and each class takes the largest count that any of its patches wants. The tolerance still holds, because more steps only lower the bound.

```pseudo id=main
TESSELLATE(nets P[1..k], tol)
L1  for each patch p: bound M_uu, M_uv, M_vv from the second differences of its net
L2      wanted[p] ← (⌈sqrt((M_uu + M_uv)/(4 tol))⌉, ⌈sqrt((M_vv + M_uv)/(4 tol))⌉)
L3  union-find: join the two s_u edges of each patch, its two s_v edges, and equal edges of different patches
L4  each class takes the largest wanted count of its members; (su[p], sv[p]) ← the counts of the classes of p
L5  for each patch p, i ← 0..su[p], j ← 0..sv[p]
L6      g[i][j] ← the vertex S_p(i/su[p], j/sv[p]), merged with an equal vertex made before
L7  for each cell (i, j) with corners a = g[i][j], b = g[i+1][j], c = g[i+1][j+1], d = g[i][j+1]
L8      emit the triangles (a, b, c) and (a, c, d)
```

The implementation evaluates the vertices with exact rational parameters $i/s_u$, and a shared edge is the same Bézier curve in both patches, so the two patches compute the same point and line L6 merges them by equality. In floating point the two patches can compute a shared point in different ways and get values that differ in the last bits. Production code therefore evaluates each shared edge once and gives the result to both patches. Merging by a distance tolerance is the other option, and it can merge points that should stay apart.

**Cost.** In the real RAM model, with de Casteljau along rows first, one vertex of a degree $(m, n)$ patch costs $(m + 1) n (n + 1)/2 + m(m + 1)/2$ linear interpolations; this is a worst case count. A patch gives $(s_u + 1)(s_v + 1)$ vertices and $2 s_u s_v$ triangles. Union-find over the $4k$ edges of $k$ patches costs $O(k \log k)$ in the worst case with the path halving of the implementation, and $O(k\, \alpha(k))$ with union by rank added. Merging vertices with a hash table costs expected $O(1)$ per vertex. Forward differences or evaluation of shared rows bring the cost per vertex down to a constant for a fixed degree.

### Uniform, adaptive and hardware tessellation

- **Uniform** steps per patch, as above, are simple and easy to make crack-free, but they put the same density everywhere in a patch.
- **Adaptive subdivision** splits a patch in two until each piece passes a flatness test, as in Lane and Carpenter (1979). Neighbor pieces split to different depths have T-junctions, where a vertex of one piece lies on an edge of the other, and they crack unless the edges are fixed up afterwards (Lane, Carpenter, Whitted and Blinn, 1980).
- **GPU tessellation** takes a factor for each edge and for the inside of each patch. The hardware cuts each edge by its own factor, so two patches with equal factors on a shared edge produce the same vertices there. The crack rule above is the rule for choosing those factors.

## Examples

- **A uniform cube.** Six bilinear patches form the faces of a cube. With $s \times s$ steps on every face the mesh has $V = 6s^2 + 2$ vertices, $F = 12 s^2$ triangles and $E = 18 s^2$ edges, so $V - E + F = 2$, and every edge is shared by exactly two triangles with opposite directions: the mesh is closed and oriented.
- **A rounded cube with a bulged top.** Bend each face of a cube into a bicubic patch, and bulge the top face more than the others. At the tolerance $0.02$ the bound asks for $12 \times 12$ steps on the top face and $8 \times 8$ on the other five. Used as they are, these steps give 490 vertices and 928 triangles, with 80 directed edges that have no partner, all on the four edges of the top face. The Euler characteristic is $-14$ instead of $2$. The twelve cube edges fall into three classes of four parallel edges each. The top face joins two of them to its count of 12, and the steps become $(12, 8)$, $(8, 12)$, $(8, 12)$, $(12, 8)$ on the four sides and $(12, 12)$ on the top and the bottom. The mesh then has 674 vertices and 1344 triangles, no open edges and $V - E + F = 2$.
- **The bound against the observed error.** For the same surface, sampling the distance between patch and mesh at many points in each triangle gives a largest observed error of $0.01026$ on the top face with $12 \times 12$ steps, against the bound $0.01916$, and $0.01564$ on a side face with $8 \times 8$ steps, against $0.01844$. The bound is a proved worst case and the observed errors are within a factor of two of it, so the bound does not waste many triangles here.
- **A sphere from a latitude chart.** At the poles a whole row of grid vertices maps to one point, and in each cell next to a pole one of the two triangles has zero area. They do no harm to the picture, but they break algorithms that need a normal per triangle, so tessellators remove them or use a chart with no singular points.

## Where it is used

- **Rendering.** GPUs draw triangles, so every curved surface model is tessellated before it is drawn, either before the program runs or in the GPU tessellation stage on every frame. The tolerance is often given in pixels on the screen, so near objects get fine meshes and far objects coarse ones.
- **CAD to downstream tools.** Export to the STL format for 3D printing, to finite element preprocessors and to collision tools needs a watertight mesh within a stated chordal tolerance.
- **Surface algorithms.** Intersection of two surfaces, ray casting and distance queries often start from a tessellation to find candidates and then refine on the exact surface.
- **The partner problems.** [Mesh generation](/mesh-generation/) also makes triangles, but for simulation: it fills a domain with elements of good shape, and the error it controls is that of the solver. Tessellation controls the distance to the surface and does not care about triangle shape. For an implicit surface $f = 0$ the analog of tessellation is [marching cubes](/marching-cubes/), which builds the mesh from samples of $f$ on a grid.

## References
