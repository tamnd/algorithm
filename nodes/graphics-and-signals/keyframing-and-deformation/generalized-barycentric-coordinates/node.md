---
tag: P4XP7N
kind: concept
slug: generalized-barycentric-coordinates
name: Generalized barycentric coordinates
aliases:
- polygon barycentric coordinates
area: graphics-and-signals/keyframing-and-deformation
level: core
summary: Weights of the vertices of a polygon or polyhedron that reproduce linear functions and sum to one, used to interpolate and to deform with cages.
prereqs: [barycentric-interpolation]
see_also: [cage-based-deformation, floater-mean-value-coordinates, harmonic-coordinates, green-coordinates, barycentric-interpolation, mesh-parameterization, finite-element-method, bilinear-interpolation]
sources:
  - paper: doi:10.1017/S0962492914000129
    title: "Michael S. Floater, Generalized barycentric coordinates and applications, Acta Numerica 24, 161-214, 2015"
    locator: the whole survey (the definition, the properties of nonnegative coordinates, Wachspress, mean value and harmonic coordinates, and the applications)
  - paper: doi:10.1016/S0167-8396(03)00002-5
    title: "Michael S. Floater, Mean value coordinates, Computer Aided Geometric Design 20(1), 19-27, 2003"
    locator: the whole paper (the mean value coordinates of a star-shaped polygon)
  - paper: doi:10.1145/1183287.1183295
    title: "Kai Hormann and Michael S. Floater, Mean value coordinates for arbitrary planar polygons, ACM Transactions on Graphics 25(4), 1424-1441, 2006"
    locator: the whole paper (mean value coordinates for any simple polygon, which can be negative)
---

Generalized barycentric coordinates extend the barycentric coordinates of a triangle to polygons with any number of vertices, and to polyhedra.
For a polygon with the vertices $v_1, \dots, v_n$, they are functions $\lambda_1, \dots, \lambda_n$ on the polygon with $\sum_i\lambda_i(x) = 1$ and $\sum_i\lambda_i(x)v_i = x$ at every point $x$.
A triangle has exactly one such set, the usual barycentric coordinates; a polygon with $n > 3$ vertices has many, and each kind adds properties such as nonnegativity or smoothness.
They interpolate data given at the vertices, $f(x) = \sum_i\lambda_i(x)f_i$, and they deform shapes inside a cage, $x \mapsto \sum_i\lambda_i(x)v'_i$.
Michael Floater (2015) surveys them.

## In plain words

Inside a triangle, every point is a unique mix of the three corners, with weights that add up to 1.
Inside a square or any other polygon there are more corners than needed, so a point can be mixed from the corners in many ways.
Generalized barycentric coordinates are rules that pick one mix for every point, smoothly over the whole polygon.
Each rule must give back the point itself when it mixes the corner positions.
Good rules also keep the weights between 0 and 1, so that each corner only pulls a point toward itself.
With such a rule you can blend colors, heights or positions given at the corners over the whole polygon.

## The idea

The two defining properties are the **partition of unity** $\sum_i\lambda_i = 1$ and the **linear precision** $\sum_i\lambda_iv_i = x$.
Together they say that interpolation reproduces every linear function $g$: $\sum_i\lambda_i(x)g(v_i) = g(x)$, because $g(v_i) = a \cdot v_i + b$.
So a cage deformation with such coordinates reproduces every affine map of the cage.

Other properties that a kind may have:

- **Nonnegativity:** $\lambda_i \ge 0$. Then each $\sum_i\lambda_if_i$ lies between the smallest and the largest $f_i$.
- **Lagrange property:** $\lambda_i(v_j) = 1$ if $i = j$ and 0 otherwise, so interpolation matches the data at the vertices.
- **Linear on edges:** on the edge from $v_i$ to $v_{i+1}$ only $\lambda_i$ and $\lambda_{i+1}$ are nonzero, and they are linear. Then the interpolant on an edge depends only on the data at its two ends, so neighbouring polygons join continuously.
- **Smoothness** inside the polygon, and **invariance** under similarities of the polygon.

For a convex polygon, nonnegativity and linear precision already imply the Lagrange property and the linearity on edges.
A vertex $v_j$ of a convex polygon is an extreme point, so the only way to write it as a convex combination of the vertices puts all the weight on $v_j$.
A point on an edge lies on a supporting line of the polygon, so a convex combination of the vertices that gives it can use only the two vertices on that line, with the weights fixed by the position on the edge.

At one point $x$ of a polygon with $n$ vertices, the two properties are three linear equations in $n$ unknowns, so the possible weights form an affine space of dimension $n - 3$.
For $n = 3$ this is one point, which is why the triangle case is unique.
For $n = 4$ there is a one-parameter family at each point, and the kinds below pick different members of it.

## Examples

**Wachspress coordinates.** For a convex polygon, Wachspress coordinates are rational functions built from the areas of triangles formed by $x$ and the vertices. They are positive inside, have the Lagrange property and are linear on edges. They come from Eugene Wachspress's work on rational finite elements, and they are not defined well for polygons that are not convex.

**Mean value coordinates.** [Floater's mean value coordinates](/floater-mean-value-coordinates/) (2003) use the tangents of half angles at $x$: $\tilde\lambda_i = (\tan(\alpha_{i-1}/2) + \tan(\alpha_i/2))/|v_i - x|$, normalized to sum 1. They are positive inside convex polygons and in the kernel of star-shaped ones, and they are defined for any simple polygon with signed angles (Hormann and Floater 2006), where they can be negative. In the L-shaped polygon with the vertices $(0, 0)$, $(2, 0)$, $(2, 1)$, $(1, 1)$, $(1, 2)$, $(0, 2)$, the point $(0.875, 1.375)$ has the mean value coordinate $-0.0097$ for the vertex $(2, 1)$, which it sees from behind the reflex corner.

**Harmonic coordinates.** [Harmonic coordinates](/harmonic-coordinates/) solve the Laplace equation inside the polygon with data that are 1 at one vertex, 0 at the others and linear on edges. They are nonnegative for every simple polygon, convex or not: at the same point of the L shape, the coordinate of $(2, 1)$ is about $0.0031$. They have no closed form.

**Bilinear coordinates.** On a rectangle, the bilinear weights $(1 - s)(1 - t)$, $s(1 - t)$, $st$, $(1 - s)t$, with $(s, t)$ the scaled position, are generalized barycentric coordinates; on a rectangle the Wachspress, harmonic and [bilinear](/bilinear-interpolation/) coordinates all agree with them. At the center of the unit square all four are $1/4$.

**Green coordinates.** [Green coordinates](/green-coordinates/) also use the edge normals, $x = \sum_i\phi_iv_i + \sum_j\psi_jn_j$. They are not generalized barycentric coordinates in the strict sense, because the vertex weights alone do not reproduce $x$.

## Where it is used

- **Cage-based deformation.** [Cage-based deformation](/cage-based-deformation/) binds each point of a model to a cage by its coordinates and moves it with the cage vertices.
- **Mesh parameterization.** Floater's shape-preserving [parameterization](/mesh-parameterization/) writes each inner vertex as a convex combination of its neighbours, with weights such as mean value coordinates, and solves a linear system.
- **Interpolation on polygons.** Colors, normals or heights given at the vertices of polygons are blended over each polygon, as [barycentric interpolation](/barycentric-interpolation/) does on triangles.
- **Polygonal finite elements.** Coordinates that are linear on edges are shape functions of polygonal elements, which extend the [finite element method](/finite-element-method/) to meshes of polygons.
- **Image warping and morphing.** A polygon drawn around an image region warps the region when its vertices move.

## References
