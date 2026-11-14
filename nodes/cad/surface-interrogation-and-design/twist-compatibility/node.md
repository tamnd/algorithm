---
tag: B9HV86
kind: concept
slug: twist-compatibility
name: Twist compatibility
aliases:
- compatibility of corner twists
area: cad/surface-interrogation-and-design
level: advanced
summary: At a patch corner the two edges each give a twist r_uv, and a smooth patch has r_uv = r_vu, so incompatible cross derivative data cannot be met by any polynomial patch.
prereqs: [coons-patch, tangent-plane-continuity, parametric-surface]
see_also: [gregory-patch, n-sided-patch, vertex-blend, coons-patch, bezier-patch, gordon-surface, tangent-plane-continuity]
sources:
  - paper: doi:10.1016/B978-0-12-079050-0.50009-6
    title: "J. A. Gregory, Smooth interpolation without twist constraints, in R. E. Barnhill and R. F. Riesenfeld (eds.), Computer Aided Geometric Design, Academic Press, 1974, pp. 71 to 87"
    locator: the compatibility conditions on the twists of boundary data, and the rational blend of the two twists that removes them
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 22, Coons Patches (the twist terms of the bicubically blended Coons patch and the compatibility problem)
  - paper: doi:10.1145/800059.801160
    title: "Hiroaki Chiyokura and Fumihiko Kimura, Design of solids with free-form surfaces, Computer Graphics 17(3), SIGGRAPH 1983"
    locator: the use of Gregory patches to fill a patch network with G1 joins where the corner twists of neighbouring patches disagree (general locator)
---

Twist compatibility is the condition that the two twist vectors at a corner of a patch agree. At a corner, one edge gives the cross derivative $r_v$ along it, and its derivative along the edge is a twist $r_{vu}$. The other edge gives $r_u$, and its derivative along that edge is a twist $r_{uv}$. Every polynomial patch has $r_{uv} = r_{vu}$, so when the two twists come from different and independent data, no polynomial patch can take both. This is the main obstacle to smooth joins of patches at a vertex, and Gregory's rational patch is one way around it.

## In plain words

To join a new patch smoothly to its neighbours, the patch must match not only the edges of the hole but also the slopes across them. The slopes come from the neighbours. At a corner of the hole two edges meet. Walk along the first edge and watch how the slope across it changes. Then walk along the second edge and watch how the slope across that edge changes. For any smooth surface these two rates of change are the same thing seen in two ways, so they must agree. When the neighbours were made independently, they usually do not agree, and then no ordinary polynomial patch fits. The way out is to give up smoothness at the single corner point: a patch with a rational blend uses the first rate near the first edge and the second rate near the second edge.

## The idea

**The data.** Let a patch $r(u, v)$ on $[0, 1]^2$ have the corner at $(0, 0)$. The boundary data near that corner are two edge curves and two cross derivatives:

$$r(u, 0) = c(u), \quad r(0, v) = d(v), \quad r_v(u, 0) = t(u), \quad r_u(0, v) = s(v).$$

Simple consistency at the corner needs $c(0) = d(0)$, $c'(0) = s(0)$ and $d'(0) = t(0)$. In a $G^1$ join the cross derivatives $t$ and $s$ come from the neighbouring patches, through condition (1) on the [tangent plane continuity](/tangent-plane-continuity/) page.

**The two twists.** Differentiate the cross derivatives along their edges:

$$r_{vu}(0, 0) = t'(0), \qquad r_{uv}(0, 0) = s'(0).$$

**Theorem.** If $t'(0) \ne s'(0)$, no patch $r$ of class $C^2$ near the corner, and in particular no polynomial or polynomial spline patch that is $C^2$ there, has $r_v(u, 0) = t(u)$ and $r_u(0, v) = s(v)$.

*Proof.* For a $C^2$ function the mixed partial derivatives are equal, $r_{uv} = r_{vu}$ (the theorem of Schwarz). From $r_v(u, 0) = t(u)$ for all $u$ we get $r_{vu}(0, 0) = t'(0)$, and from $r_u(0, v) = s(v)$ for all $v$ we get $r_{uv}(0, 0) = s'(0)$. So $t'(0) = s'(0)$, a contradiction. A polynomial is $C^\infty$. $\square$

The condition $t'(0) = s'(0)$ is the *twist compatibility* condition. It is a condition on the data, and it is easy to break: two neighbours that are designed separately, or $n$ patches around one vertex with cross derivatives chosen edge by edge, give two twists with no reason to agree.

**The rational blend.** The theorem needs $C^2$ at the corner point only. So replace the constant twist $W$ in the corner term of a Coons type construction by a function that is $s'(0)$ on one edge and $t'(0)$ on the other:

$$W(u, v) = \frac{u\, s'(0) + v\, t'(0)}{u + v}, \qquad (u, v) \ne (0, 0),$$

$$r(u, v) = c(u) + v\, t(u) + d(v) + u\, s(v) - \bigl[c(0) + u\, c'(0) + v\, d'(0) + u v\, W(u, v)\bigr].$$

This is the Boolean sum of the two first order Taylor projectors of the corner, $P_u f = f(0, v) + u f_u(0, v)$ and $P_v f = f(u, 0) + v f_v(u, 0)$, with the twist of $P_u P_v f$ replaced by $W$, as in [Coons patches](/coons-patch/).

*It meets all four conditions.* At $v = 0$: $r(u, 0) = c(u) + d(0) + u s(0) - c(0) - u c'(0) = c(u)$. Differentiate in $v$. The term $u v W$ has $\partial_v (u v W) = u W + u v W_v$, and for fixed $u > 0$, $W_v = u (t'(0) - s'(0)) / (u + v)^2$ is bounded, so at $v = 0$ this is $u W(u, 0) = u s'(0)$. Hence $r_v(u, 0) = t(u) + d'(0) + u s'(0) - d'(0) - u s'(0) = t(u)$. The edge $u = 0$ is symmetric, with $W(0, v) = t'(0)$. At the corner, $|u v W| \le u v \max(|s'(0)|, |t'(0)|)$ for vectors compared by length, so $r$ is continuous there, and the same bound gives $r_u(0, 0) = s(0)$ and $r_v(0, 0) = t(0)$. $\square$

The patch is not $C^2$ at the corner: its mixed derivative tends to $s'(0)$ along one edge and to $t'(0)$ along the other, as the theorem says it must. The full [Gregory patch](/gregory-patch/) does this at all four corners.

## Examples

**A plane that tilts along one edge.** Take $c(u) = (u, 0, 0)$, $d(v) = (0, v, 0)$, the cross derivative $t(u) = (0, 1, u)$ along $v = 0$, so the surface rises more steeply across that edge as $u$ grows, and $s(v) = (1, 0, 0)$ along $u = 0$, so it does not rise across that edge at all. The corner conditions hold: $s(0) = c'(0)$ and $t(0) = d'(0)$. The twists are $t'(0) = (0, 0, 1)$ and $s'(0) = (0, 0, 0)$, so the data are incompatible. A polynomial height $z(u, v)$ would need $z_{vu}(0, 0) = 1$ and $z_{uv}(0, 0) = 0$. The rational blend gives $W = (0, 0, v/(u + v))$ and

$$r(u, v) = \Bigl(u,\ v,\ \frac{u^2 v}{u + v}\Bigr).$$

Here $z_v = u^3/(u + v)^2$, which is $u$ at $v = 0$, and $z_u = u v (u + 2v)/(u + v)^2$, which is $0$ at $u = 0$, as asked. Both first derivatives tend to $0$ at the corner, so the patch is $C^1$ there. The mixed derivative is $z_{uv} = u^2 (u + 3v)/(u + v)^3$: it is $1$ on the edge $v = 0$ and $0$ on the edge $u = 0$, so it has no limit at the corner.

**Compatible data.** With $t(u) = (0, 1, u)$ and $s(v) = (1, 0, v)$ both twists are $(0, 0, 1)$, $W$ is constant, and the formula gives the polynomial $z = u v$, the hyperbolic paraboloid.

**The bicubic Coons patch.** The bicubically blended Coons patch interpolates positions and cross derivatives on all four edges. Its correction term is a bicubic Hermite patch that needs a twist vector at each corner. With incompatible data, any constant choice of that twist matches one edge and misses the other, so the patch is not $G^1$ to one of the neighbours near the corner.

## Where it is used

- **[Gregory patches](/gregory-patch/).** Each corner of the patch has two inner control points instead of one, and a rational blend picks one near each edge.
- **[n-sided patches](/n-sided-patch/) and [vertex blends](/vertex-blend/).** Where $n$ patches meet at a vertex, the $G^1$ conditions of the $n$ edges are coupled through the twists. Schemes either choose the cross derivatives so that the twists agree, or use rational blends, or split the region so that the problem moves to points where it can be solved.
- **Twist estimation.** When a designer gives only curves, as for a [Gordon surface](/gordon-surface/) or a bicubic Coons patch, the program must invent the twists. Any estimate that is the same for both edges makes the data compatible, but a poor estimate shows as a flat spot or a bulge near the corner.
- **Solid modelers.** Chiyokura and Kimura used Gregory patches so that a patch in a network can be changed locally, without the twist constraints that would tie it to all its neighbours.

## References
