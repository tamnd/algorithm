---
tag: 1VH9MB
kind: technique
slug: curved-layer-printing
name: Curved layer fused deposition
aliases:
- non-planar slicing
- curved layer slicing
area: cad/cam-and-additive-manufacturing
level: research
summary: Deposits each layer on a curved surface, a level set of a field, instead of a plane, so thin curved shells lose their stairs and their layer bonds run along the shell.
prereqs: [slicing-for-additive-manufacturing, staircase-effect]
see_also: [multi-axis-printing-decomposition, adaptive-slicing, heat-method, level-set-method, isosurface-extraction, iso-parametric-toolpath, contour-parallel-toolpath, support-structure-generation]
sources:
  - paper: doi:10.1016/j.cad.2007.10.014
    title: Debapriya Chakraborty, B. Aneesh Reddy and A. Roy Choudhury, Extruder path generation for Curved Layer Fused Deposition Modeling, Computer-Aided Design 40(2), 2008, 235 to 243
    locator: the curved layers as offsets of a parametric surface and the extruder paths along its parameter lines
  - paper: doi:10.1145/3306346.3323022
    title: Jimmy Etienne, Nicolas Ray, Daniele Panozzo, Samuel Hornus, Charlie C. L. Wang, Jonàs Martínez, Sara McMains, Marc Alexa, Brian Wyvill and Sylvain Lefebvre, CurviSlicer, slightly curved slicing for 3-axis printers, ACM Transactions on Graphics 38(4), 2019, article 81
    locator: the optimized deformation of the part that is sliced by planes and mapped back, with bounds on the slope of the layers for a 3-axis machine
  - paper: doi:10.1145/3197517.3201342
    title: Chengkai Dai, Charlie C. L. Wang, Chenming Wu, Sylvain Lefebvre, Guoxin Fang and Yong-Jin Liu, Support-free volume printing by multi-axis motion, ACM Transactions on Graphics 37(4), 2018
    locator: the curved layers that grow over the volume and are printed by a robot arm without supports
---

## In plain words

An ordinary printer builds every part from flat slices. A thin curved shell, such as a helmet or a lens cover, then turns into a stack of rings with a step at each ring edge. Each glued joint between slices also cuts straight across the shell, and the part tends to break along those joints.

Curved layer printing makes the slices curved, like the skins of an onion. The nozzle moves up and down while it lays a bead, so each bead follows the shell. The outside comes out smooth, a thin shell needs only a few layers, and the joints run along the shell instead of across it. The price is that the nozzle must reach every curved layer without hitting what is already printed.

## When it applies

**Setting.** A part $\Omega$ is to be built by depositing beads of height $t$ and width $w$ from a nozzle. Instead of the planes $z = kt$ of [planar slicing](/slicing-for-additive-manufacturing/), the layers are the level sets

$$S_k = \{\, p \in \Omega : \varphi(p) = c_k \,\}, \qquad c_0 < c_1 < \dots < c_m,$$

of a scalar field $\varphi$ on $\Omega$, printed in increasing order of $c_k$. Planar slicing is the case $\varphi(x, y, z) = z$. A **toolpath** here is the ordered list of nozzle positions, and for a machine with more than three axes also nozzle directions, that the printer follows while it extrudes. Within a curved layer the toolpath is a set of curves on $S_k$ spaced about $w$ apart.

Three conditions make a field usable:

1. *Order.* Every point of a layer must rest on material that is already there, or on the bed. This holds when $\varphi$ grows away from the bed and has no local minimum inside $\Omega$ except on the bed.
2. *Thickness.* The gap between $S_k$ and $S_{k+1}$ must stay near $t$, since a bead cannot be made much thinner or thicker than its nozzle allows.
3. *Reach.* The nozzle and its holder must touch layer $k$ without hitting layers $0$ to $k$. On a 3-axis machine the nozzle is vertical, so the layers may only be slightly tilted. With a tilting head or a robot arm the nozzle can follow the normal of the layer.

The technique pays off on thin parts whose shape is mostly one curved surface: shells, domes, wings, covers, and bars that bend. On a bulky block the outer layers can follow the surface, but the inside gains nothing.

## The template

```pseudo id=main
CURVED-LAYERS(Ω, t, ⟨field⟩, ⟨levels⟩, ⟨paths⟩, ⟨reach⟩)
L1  φ ← ⟨field⟩(Ω)                                  ▷ planar slicing is φ = z
L2  c_0, …, c_m ← ⟨levels⟩(φ, t)                    ▷ keep (c_{k+1} − c_k) / |∇φ| close to t
L3  for k ← 0 to m − 1
L4      S_k ← {p ∈ Ω : φ(p) = c_k + ½(c_{k+1} − c_k)}     ▷ the middle surface of layer k
L5      P_k ← ⟨paths⟩(S_k, w)                       ▷ curves on S_k about w apart
L6      for each point p of P_k: d_p ← ⟨reach⟩(p, S_k)    ▷ nozzle direction, checked against layers 0..k
L7      if some point has no free direction: change ⟨field⟩ near p, or split Ω, and start again
L8  return P_0, …, P_{m−1} with their directions
```

The holes are:

- **Field** (L1). The signed distance to the outer surface gives offset layers. Chakraborty and coauthors used vertical offsets $z = f(x, y) - kt$ of the top surface. A blend between the bottom and the top surface, $\varphi = (z - b)/(u - b)$ over each point $(x, y)$, gives the same number of layers everywhere. CurviSlicer computes a field by optimization. A [level set method](/level-set-method/) can evolve the layers as a moving front.
- **Levels** (L2). Equal steps of $\varphi$, or steps chosen from $|\nabla\varphi|$ in the same way that [adaptive slicing](/adaptive-slicing/) chooses plane spacings.
- **Paths** (L5). Curves of constant parameter on a parametric surface, as in an [iso-parametric toolpath](/iso-parametric-toolpath/), or the level curves of the geodesic distance to the boundary of $S_k$, which is the curved version of a [contour-parallel toolpath](/contour-parallel-toolpath/). The **geodesic distance** between two points of a surface is the length of the shortest curve between them that stays on the surface, and the [heat method](/heat-method/) computes it from one point or curve to all vertices of a mesh. Steps of $w$ in geodesic distance give beads that are $w$ apart along the surface, which steps of $w$ in a parameter do not.
- **Reach** (L6). For a vertical nozzle: a bound on the slope of $S_k$ and a [collision](/collision-detection/) test of the nozzle body against the printed layers. For a 5-axis head: a direction near the normal of $S_k$ chosen from the cone of free directions, as in [multi-axis printing](/multi-axis-printing-decomposition/).

L4 is [isosurface extraction](/isosurface-extraction/) when $\varphi$ is sampled on a grid or a tetrahedral mesh.

**Walk-through.** Take a spherical shell of outer radius 50 mm and thickness 2 mm, cut off at $30°$ from the pole, so it is the part of $48 \le |p| \le 50$ with polar angle at most $30°$. Beads are $t = 0.2$ mm thick. The numbers below were computed by a short script.

| | planar layers | curved layers, $\varphi = \lvert p\rvert$ |
|---|---|---|
| layers | 43 (the part spans 8.43 mm in $z$) | 10 |
| layer thickness | 0.2 | 0.2 everywhere |
| cusp on the outer surface | 0 at the rim to 0.2 at the pole, area mean 0.187 | none |
| layer joints crossed by the middle meridian | 33 | 0 |
| the top layer | a flat disk of radius 4.47 mm | the whole outer surface |

The mean cusp matches the closed form $\tfrac12 t(1 + \cos 30°)$ from averaging the cusp of the [staircase effect](/staircase-effect/) over the cap. Two other fields on the same part behave differently:

- The blend $\varphi = (z - b)/(u - b)$ with 10 equal steps has layers between 0.1987 and 0.2013 mm thick, measured from $\Delta c / |\nabla\varphi|$ at 550 sample points out to the inner rim. For this shallow shell it is almost as good as the distance field.
- Vertical offsets of the outer surface by 0.2 mm give layers only $0.2 \cos\alpha$ thick along the normal, where $\alpha$ is the slope: 0.1755 mm at the inner rim, where $\alpha = 28.7°$. The shell is 2.294 mm tall there, so 10 such layers leave a gap of 0.294 mm that needs more layers or wider beads.

**What is proved.**

1. *Thickness.* If $\nabla\varphi \ne 0$ at a point $p$ of $S_k$, the distance from $p$ to the next level set, along the normal, is $\Delta c / |\nabla\varphi(p)| + O(\Delta c^2)$, where $\Delta c = c_{k+1} - c_k$. Proof: by Taylor's theorem, $\varphi(p + s\,n) = c_k + s\,|\nabla\varphi(p)| + O(s^2)$ with $n = \nabla\varphi / |\nabla\varphi|$, which reaches $c_k + \Delta c$ at the stated $s$. A field with $\nabla\varphi = 0$ inside $\Omega$ has layers of unbounded thickness there.
2. *Distance fields.* If $\varphi$ is the distance to a surface and $|\nabla\varphi| = 1$, every layer has thickness exactly $\Delta c$. This holds up to the focal distance, the radius of curvature, where offsets start to fold. For the shell above it holds down to radius 0.
3. *Vertical offsets.* For $\varphi = z - f(x, y)$, $|\nabla\varphi| = \sqrt{1 + |\nabla f|^2} = 1 / \cos\alpha$, so by claim 1 a vertical step of $t$ gives a normal thickness of $t \cos\alpha$. For a plane $f$ this is exact.
4. *Joints.* With planar layers, a curve in $\Omega$ whose height changes by $h$ crosses at least $\lfloor h / t \rfloor$ layer joints, by the intermediate value theorem applied to $z$ along the curve. A curve that stays in one level set of $\varphi$ crosses none. This is why the strength along a curved shell is no longer limited by the bond between layers.
5. *Outer surface.* If the outer surface of $\Omega$ is a level set of $\varphi$, the last layer lies on it, so the cusp of the [staircase effect](/staircase-effect/) is zero there. What remains is the ridge between neighboring beads within the layer, the [scallop height](/scallop-height/) of the bead shape.

What is not proved here: that any field satisfies the reach condition for a given nozzle, how much stronger a printed part becomes, or that a particular optimizer finds a field. Those are measured on machines in the papers below.

## Classic examples

- **Curved layer fused deposition.** Chakraborty, Reddy and Roy Choudhury (2008) described a thin part by a parametric surface, built it from vertical offsets of that surface, and moved the extruder along its parameter lines with a 3-axis machine. Their aim was thin curved parts with fewer layers, less stair-stepping and more strength along the shell. Claim 3 above shows the cost of vertical offsets on steep parts.
- **CurviSlicer.** Etienne and coauthors (2019) kept a standard 3-axis printer. They deform the part so that slicing it by planes and mapping the slices back gives layers that are slightly curved. An optimization chooses the deformation so that the top surfaces become layers where possible, while the slope of every layer stays under the bound that the nozzle allows and the layer thickness stays within the printable range.
- **Support-free volume printing.** Dai and coauthors (2018) used curved layers that grow over the whole volume and a robot arm that tilts the nozzle, so that overhangs are printed without [support structures](/support-structure-generation/). The planning of the order and directions is on the page on [multi-axis printing](/multi-axis-printing-decomposition/).
- **Layers along the load.** Later work by Fang and coauthors (2020) chose the field so that the beads follow the main stress directions of the loaded part, since a bead is stronger along its length than across a joint.

## Variations

- **Hybrid layers.** Print the bulk with planar layers and only the last few layers curved, so that the outer surface loses its staircase without a field for the whole part.
- **Curved layers on a curved bed.** Print on a curved mold or an existing part, with the first layer following the bed.
- **Varying thickness.** Use the change of $\Delta c / |\nabla\varphi|$ on purpose and let the bead height vary within a layer, or vary the flow so that the deposited volume matches the gap.
- **Fields from geometry.** The [heat method](/heat-method/) gives a smooth distance from the bed or from the boundary, and its level sets are layers that bend with the part.

## Pitfalls

- **Collision on steep layers.** A vertical nozzle on a layer tilted by $\alpha$ hits the material beside it when $\alpha$ exceeds what the nozzle cone allows, and the holder and the fan hit sooner. The limit depends on the machine, so it must be measured or computed from the nozzle shape, not assumed.
- **Uneven thickness.** By claim 1, a field with a small gradient somewhere has thick layers there and a field with a large gradient has thin ones. Equal steps of $\varphi$ are not equal layers unless $|\nabla\varphi|$ is nearly constant.
- **Gaps from vertical offsets.** Offsetting a surface vertically by $t$ fills less than $t$ along the normal on slopes, and the gaps add up across layers, as the walk-through shows.
- **Paths spaced in the parameter.** Equal steps in a parameter are unequal steps on the surface where the parameterization is stretched, which leaves gaps or overlaps between beads.
- **Nothing to stand on.** A field with a local minimum inside the part asks the printer to start a layer in the air.
- **Expecting gains on bulky parts.** Inside a block every field gives the same volume to fill, so most of the time saved comes from thin regions.

## Exercises

1. For the blend field $\varphi = (z - b(x, y))/(u(x, y) - b(x, y))$, write $|\nabla\varphi|$ in terms of $u - b$ and the gradients of $u$ and $b$, and show that the layers have thickness exactly $(u - b)/m$ wherever $u$ and $b$ are parallel planes.
2. Show that the area mean of the cusp height $t \cos\theta$ over a spherical cap of half angle $\beta$, printed with planar layers, is $\tfrac12 t (1 + \cos\beta)$.
3. A half-cylinder shell of outer radius 30 mm and thickness 1.2 mm is printed on a mold that fills it from below, with its axis horizontal. For $t = 0.2$, compare the number of planar layers with the number of curved layers given by $\varphi$ = distance to the axis, and find the part of each curved layer that a vertical nozzle with a slope limit of $30°$ can print.
4. On a mesh of a curved layer, compute the geodesic distance from the boundary with the heat method and extract the level curves at multiples of $w$. Measure the spacing of neighboring curves and compare it with curves of constant parameter on the same surface.
5. A solid ball rests on the bed. Show that $\varphi(p) = |p - q|$, the distance to its center $q$, breaks condition 1, and give a field on the ball other than $z$ that satisfies it.

## References
