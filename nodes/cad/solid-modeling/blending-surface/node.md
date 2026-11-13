---
tag: 290CBG
kind: definition
slug: blending-surface
name: Blending surface
aliases:
- fillet surface
- blend
area: cad/solid-modeling
level: core
summary: A surface that joins two surfaces smoothly along their meeting, as a fillet on a concave edge or a round on a convex one, with tangent or curvature continuity.
prereqs: [parametric-surface, parametric-continuity, boundary-representation]
see_also: [rolling-ball-blend, offset-surface, solid-offsetting, trimmed-surface, surface-surface-intersection, sweep-surface, coons-patch, feature-based-modeling]
sources:
  - paper: "Janos Vida, Ralph R. Martin and Tamas Varady, A survey of blending methods that use parametric surfaces, Computer-Aided Design 26(5), 341 to 365, 1994"
    locator: the whole survey (the terms of blending, the classes of rolling-ball, spine-based and trimline-based methods, and vertex blending)
  - paper: "Byoung K. Choi and Suk Y. Ju, Constant-radius blending in surface modelling, Computer-Aided Design 21(4), 213 to 220, 1989"
    locator: the whole paper (the constant-radius rolling-ball surface between two parametric surfaces, from the intersection of their offsets)
  - paper: doi:10.1016/0167-8396(86)90017-8
    title: Jaroslaw R. Rossignac and Aristides A. G. Requicha, Offsetting operations in solid modelling, Computer Aided Geometric Design 3(2), 129 to 148, 1986
    locator: the definitions of constant-radius rounding and filleting as compositions of growing and shrinking
---

A blending surface is a surface that joins two surfaces $S_1$ and $S_2$ with a smooth transition, in place of the sharp edge where they meet. It touches $S_1$ along one curve and $S_2$ along another, the *trimlines*, and the parts of the two surfaces between the trimlines and the edge are cut away. On a concave edge, where material is added, the blending surface is a *fillet*; on a convex edge, where material is removed, it is a *round*. The join is smooth in the sense of geometric continuity: the same tangent plane along each trimline ($G^1$), or also the same curvature ($G^2$).

## Definition

Let $S_1$ and $S_2$ be two regular surfaces, usually faces of a [boundary representation](/boundary-representation/) that meet along an edge $E$ at an angle. A **blending surface** of $S_1$ and $S_2$ is a surface $B$ with two boundary curves $C_1 \subset S_1$ and $C_2 \subset S_2$, such that

- $B$ meets $S_1$ along $C_1$ and $S_2$ along $C_2$, and nowhere else near $E$;
- the join along each $C_i$ is $G^k$ for a stated $k \ge 1$;
- the solid whose boundary uses $B$ and the trimmed parts of $S_1$ and $S_2$ beyond $C_1$ and $C_2$ is a valid solid.

The curves $C_1$ and $C_2$ are the **trimlines** (also called contact curves or linkage curves). The surfaces $S_1$ and $S_2$ are cut back to [trimmed surfaces](/trimmed-surface/) that end at the trimlines.

Geometric continuity is a condition on the shape, not on a parametrization (compare [parametric continuity](/parametric-continuity/)):

- $G^0$: $B$ and $S_i$ share the curve $C_i$.
- $G^1$: also, at each point of $C_i$, $B$ and $S_i$ have the same tangent plane, so their normals are parallel. The surfaces meet without a crease.
- $G^2$: also, at each point of $C_i$, $B$ and $S_i$ have the same normal curvature in every tangent direction. Reflections of light lines pass the join without a kink.

The orientation follows the convention of the B-rep pages: the normal of every face points out of the solid, and each loop runs counterclockwise around it (the right-hand rule). Along a $G^1$ join, the outward normal of $B$ equals the outward normal of $S_i$, not only up to sign.

**Fillet and round.** The edge $E$ is *concave* when the solid occupies more than a half-space near $E$ (an inner corner), and *convex* when it occupies less. A blending surface on a concave edge adds material and is a fillet. One on a convex edge removes material and is a round. Rossignac and Requicha express the constant-radius versions as offset compositions: rounding $(S \downarrow r) \uparrow r$ and filleting $(S \uparrow r) \downarrow r$, see [solid offsetting](/solid-offsetting/).

**Classes of construction.** Vida, Martin and Várady sort the parametric methods by what defines the surface:

- **Rolling ball.** $B$ is the envelope of a ball that rolls while it touches both surfaces. The [rolling-ball method](/rolling-ball-blend/) gives a $G^1$ surface whose cross sections are circular arcs, of constant or varying radius.
- **Spine based.** A spine curve is chosen first, and a cross-section curve is swept along it, as in a [sweep surface](/sweep-surface/). The rolling ball is the case where the spine is the path of the ball center and the cross section is an arc.
- **Trimline based.** The trimlines are chosen first, for example as curves at a given distance from $E$ on each surface, and a cross section, such as a cubic Hermite curve with the tangent planes as end conditions, joins them.

Where three or more blending surfaces meet at a vertex of the solid, a separate *vertex surface* fills the hole that they leave, often an $n$-sided patch such as a [Coons patch](/coons-patch/) or a piece of a sphere.

## Examples and non-examples

- **A quarter cylinder.** Two half-planes $y = 0$, $x \ge 0$ and $x = 0$, $y \ge 0$ bound the solid $x, y \ge 0$, which has a convex edge along the $z$ axis. A round of radius $r$ is the quarter cylinder of axis $x = y = r$ and radius $r$, with trimlines $x = r, y = 0$ and $x = 0, y = r$. It is $G^1$: on each trimline the cylinder has the normal of the plane. It is not $G^2$: across the trimline the normal curvature in the cross direction jumps from $0$ to $1/r$.
- **A rounded box corner.** Rounding all edges of a box with the same radius $r$ gives quarter cylinders on the $12$ edges and an eighth of a sphere of radius $r$ at each corner, as the vertex surface. The sphere joins each cylinder with $G^1$. Along the join both have the normal curvature $1/r$, but across it the cylinder has $0$ and the sphere $1/r$, so the join is not $G^2$.
- **A shaft shoulder.** A cylinder of radius $R$ standing on a plane has a concave edge along the circle where they meet. A fillet of radius $r$ is a piece of a torus with axis radius $R + r$ and tube radius $r$.
- **A $G^2$ cross section.** Replacing the circular arc of the first example by a quintic polynomial curve whose ends match position, tangent and zero curvature of the planes gives a $G^2$ round, at the price of a curve that is not an arc.

Non-examples:

- **A chamfer.** The plane strip $x + y = r$ between the two half-planes joins them along the same trimlines. It is $G^0$ but not $G^1$: it has a crease along each trimline. It is a blending surface only in the weak sense of $G^0$, and CAD systems treat it as a separate operation.
- **A fillet that is too large.** On a plate of thickness $t$, a round of radius $r > t$ on the top edge reaches past the bottom face. The trimlines fall outside the faces, the third condition fails, and the operation must be rejected or merged with the bottom edge.

## Related definitions

- The [offset surface](/offset-surface/) at distance $r$ of each $S_i$ contains the path of the center of the rolling ball, so constant-radius rolling-ball surfaces are built from the [intersection of two offsets](/surface-surface-intersection/).
- A fillet or a round is a typical feature of [feature-based modeling](/feature-based-modeling/). It refers to the edge it rounds, which is why the naming of edges matters for the history of the model.
- [Solid offsetting](/solid-offsetting/) gives the rounding and filleting of a whole solid at once, with the radius $r$ on every convex or concave edge.
- [Parametric continuity](/parametric-continuity/) $C^k$ is the stronger condition on a parametrization. $G^k$ joins can use any parametrization that gives the same shape.

## References
