---
tag: H66630
kind: technique
slug: object-instancing
name: Object instancing
aliases:
- instancing
area: graphics-and-signals/ray-tracing
level: intro
summary: Store one object once and place it many times with a transform per copy. Map each ray into the object's space with the inverse transform, and map normals back with the inverse transpose.
prereqs: [ray-casting, matrix-inversion]
see_also: [bounding-volume-hierarchy, bvh-traversal, closest-hit-query, ray-sphere-intersection, moller-trumbore, determinant, cross-product, whitted-ray-tracing]
sources:
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, 2016
    locator: Section 2.8 (Applying Transformations, with the transformation of normals by the inverse transpose) and Section 4.1 (Primitive Interface and Geometric Primitives, with the TransformedPrimitive class for object instancing)
  - paper: doi:10.1145/965105.807479
    title: Steven M. Rubin and Turner Whitted, A 3-dimensional representation for fast rendering of complex scenes, Computer Graphics 14(3) (SIGGRAPH 80), 1980, pages 110 to 116
    locator: the hierarchy of bounding volumes, each with its own transformation, and the transformation of the ray into the local coordinates of a volume
  - paper: doi:10.1145/37401.37417
    title: John M. Snyder and Alan H. Barr, Ray tracing complex models containing surface tessellations, SIGGRAPH 87, 1987, pages 119 to 128
    locator: the instancing of tessellated objects inside a hierarchy of grids, used to render scenes with very many triangles
  - paper: doi:10.1145/1461551.1461591
    title: Ivan E. Sutherland, Sketchpad, a man-machine graphical communication system, AFIPS Spring Joint Computer Conference, 1963
    locator: the master drawings and their instances, each instance a copy of a master under its own position, scale and rotation
---

Object instancing places one stored object many times in a scene. Each copy, an *instance*, holds only a reference to the shared object and an affine map $x \mapsto A x + s$ from the object's own coordinates to world coordinates. A ray tracer does not build the transformed copies. To intersect a ray with an instance, it maps the ray into object space with the inverse map, intersects the original object there, and maps the result back. The ray parameter $t$ of the hit is the same in both spaces when the direction is mapped and not normalized. The surface normal goes back with the inverse transpose $A^{-\mathsf{T}}$, not with $A$. A forest of a thousand trees, each with $10^5$ triangles, then costs the memory of one tree plus a thousand matrices.

## In plain words

Suppose you want to draw a thousand identical chairs in a hall. You can make a thousand copies of the chair model, each moved and turned to its place. Or you can keep one model and, for each chair, a small card that says "the model, moved by this much and turned by this angle".

To find where a ray hits chair number 7, you move the ray the opposite way, into the chair's own frame. You find the hit on the model there and carry the answer back to the hall. Moving the ray is cheap: one point and one direction. Moving a chair means moving all of its triangles.

There is one surprise. When the chair is stretched more in one direction than another, the direction straight out of the surface, the normal, needs a different matrix.

## When it applies

- The scene repeats the same geometry many times: trees, grass, rivets, buildings, chess pieces, a crowd of identical robots.
- Each copy differs from the object only by an affine map: translation, rotation, scale, shear or reflection. A copy that bends or deforms needs its own geometry.
- The intersector of the object works in any coordinate frame and with a direction that is not of unit length. A [ray-triangle intersection](/moller-trumbore/) or an [acceleration structure](/bounding-volume-hierarchy/) built in object space satisfies this.
- The cost of one matrix-vector product per instance visited is small next to the memory saved. In large scenes the memory decides: a flattened scene may not fit at all.

## The template

**Conventions.** An instance is a triple $(X, A, s)$: an object $X$ stored in object space, an invertible $3 \times 3$ matrix $A$ and a translation $s$. The instance occupies $\{A x + s : x \in X\}$. Store $W = A^{-1}$ with the instance. A ray is $o + t d$ for $t$ in $(t_{\min}, t_{\max}]$. The hole is the object-space intersector INTERSECT, which returns the parameter $t$, the index of the primitive hit and an object-space normal $n_X$.

```pseudo id=main
INTERSECT-INSTANCE(ray o + t·d, instance (X, A, s, W = A⁻¹), tmin, tmax)
L1  o' ← W·(o − s);  d' ← W·d          ▷ the ray in object space; do not normalize d'
L2  hit ← INTERSECT(X, o' + t·d', tmin, tmax)   ▷ hole: any object-space intersector
L3  if hit is none then return none
L4  (t, k, nX) ← hit                    ▷ t is the same parameter in world space
L5  p ← o + t·d                          ▷ the world hit point
L6  n ← Wᵀ·nX                            ▷ the inverse transpose of A
L7  return (t, p, k, n)

TRACE-SCENE(ray, instances)
L8  best ← none
L9  for each instance whose world box the ray meets before best.t (or tmax):
L10     h ← INTERSECT-INSTANCE(ray, instance, tmin, best.t or tmax)
L11     if h is not none and h.t < best.t then best ← h
L12 return best
```

**Why $t$ does not change.** The world point $o + t d$ lies on the instance exactly when $W(o + t d - s) = o' + t d'$ lies on $X$, because $x \mapsto W(x - s)$ is the inverse of the instance map. The same $t$ appears on both sides. So line L4 needs no conversion, the interval $(t_{\min}, t_{\max}]$ can be passed down unchanged, and hits of different instances compare directly in line L11. If line L1 normalized $d'$, the object-space parameter would be $t \lVert W d \rVert$ for a unit $d$, a different number for each instance.

**Why normals need the inverse transpose.** A normal $n$ at a point of $X$ is a vector with $n \cdot v = 0$ for every tangent vector $v$. The map sends the tangent $v$ to $A v$. For the vector $A^{-\mathsf{T}} n$,

$$(A^{-\mathsf{T}} n) \cdot (A v) = n^{\mathsf{T}} A^{-1} A v = n \cdot v = 0,$$

so $W^{\mathsf{T}} n$ is normal to the instance. The vector $A n$ is normal only when $A$ is a rotation times a uniform scale. The orientation is also kept: for a point $x + \epsilon n$ on the outer side, the mapped offset $\epsilon A n$ satisfies $(A^{-\mathsf{T}} n) \cdot (A n) = n \cdot n > 0$, so $A^{-\mathsf{T}} n$ points to the outer side of the instance even when $\det A < 0$. The normal is not of unit length; normalize it before shading.

**Cost.** Line L1 costs two matrix-vector products, 18 multiplications. Line L6 costs one more, and it can wait until the closest hit is known. The memory of an instance is $O(1)$: a reference, $A$, $W$ and $s$. The object itself is stored once. With a [BVH](/bounding-volume-hierarchy/) over the world boxes of the instances on top and one BVH per object below, the search is the usual [BVH traversal](/bvh-traversal/), with a change of frame at each instance leaf.

**Example.** Let $X$ be the unit sphere at the origin and the instance be $A = \operatorname{diag}(2, 1, 1)$, $s = (4, 0, 0)$: an ellipsoid with semi-axes 2, 1, 1 centered at $(4, 0, 0)$. Shoot the ray $o = (0, 0.8, 0)$, $d = (1, 0, 0)$.

| step | value |
|---|---|
| L1 | $o' = (-2, 0.8, 0)$, $d' = (0.5, 0, 0)$ |
| L2 | $(-2 + 0.5t)^2 + 0.64 = 1$ gives $t = 2.8$ (the smaller root) |
| L5 | $p = (2.8, 0.8, 0)$; in object space $q = (-0.6, 0.8, 0)$ |
| L6 | $n = W^{\mathsf{T}} q = (-0.3, 0.8, 0)$ |

The world ellipse $\bigl((x - 4)/2\bigr)^2 + y^2 = 1$ meets the line $y = 0.8$ first at $x = 2.8$, so $t = 2.8$ is right. Its tangent at $p$ is $(-1.6, -0.6, 0)$, the image $A(-0.8, -0.6, 0)$ of the sphere's tangent. The dot product with $(-0.3, 0.8, 0)$ is $0.48 - 0.48 = 0$. The wrong normal $A q = (-1.2, 0.8, 0)$ gives $1.92 - 0.48 = 1.44$. A normalized $d' = (1, 0, 0)$ would give the object-space parameter $1.4$, half the world value.

The tests build random scenes of shared triangle meshes under random invertible matrices with rational entries, some with negative determinant, and compare TRACE-SCENE with a flattened scene in which every triangle is mapped to world space. With exact fractions the parameter, the instance and the triangle agree exactly, and the cross-product normal of the mapped triangle equals $\det A$ times the normal of line L6.

## Classic examples

- **Two-level acceleration structures.** Hardware ray tracing interfaces split the scene into bottom-level structures, one per mesh, and a top-level structure over instances with a transform each. The traversal changes frame at each instance, as in lines L1 and L6.
- **Vegetation and crowds.** Forests, fields of grass and crowds reuse a few models under many transforms. Flattening would multiply the memory by the number of copies.
- **Quadric primitives.** Many ray tracers store one unit sphere, unit cylinder and unit cone, and every sphere, ellipsoid or cylinder of the scene is an instance of one of them. The [ray-sphere intersection](/ray-sphere-intersection/) then has a single, simple form.
- **Recursive models.** An instance can refer to an object that itself contains instances. Self-similar models such as fractal trees are stored as a few levels of instances; the transforms compose along the path.
- **Rasterization.** Graphics hardware draws instanced meshes by applying the per-instance transform to the vertices. That is the forward direction of the same map: a rasterizer moves the object, a ray tracer moves the ray.

## Variations

- **Nested instances.** Compose the maps along the path from the root. Store or compute $W$ for the composite map, or apply the inverse of each level in turn while descending.
- **Rigid instances.** For a rotation $R$ with translation, $W = R^{\mathsf{T}}$ and $W^{\mathsf{T}} = R$, so the normal map is $R$ itself. With a uniform scale $c$, the normal direction is $R n$ up to the factor $1/c$.
- **Motion blur.** Let $A$ and $s$ depend on the time of the ray, and interpolate between key transforms. The object and its structure stay static.
- **Delayed normal.** Return $n_X$ and the instance from the search, and apply $W^{\mathsf{T}}$ once to the closest hit. This saves a product for each hit that a later, nearer hit replaces.
- **World-space boxes.** The world box of an instance is the box of the eight mapped corners of the object box, which is loose under rotation. A tighter box maps the vertices or a hull of the object, once per instance at build time.

## Pitfalls

- **Normalizing the object-space direction.** Then $t$ is in object units. Comparing it with other hits, or with $t_{\max}$, gives wrong answers whenever $A$ scales. Keep $d' = W d$ as it is, or convert $t$ back by the factor $\lVert W d \rVert$.
- **Mapping normals with $A$.** This is right only for rotations and uniform scales. Under a non-uniform scale the shading normal tilts, and the error grows with the ratio of the scale factors.
- **Mirrored instances.** When $\det A < 0$, the image of a triangle has the opposite winding. A normal taken as the cross product of the mapped edges points inward. The tests check that this normal is $\det A$ times $W^{\mathsf{T}} n_X$. Back-face culling and the inside or outside test for refraction must use $W^{\mathsf{T}} n_X$ or the sign of $\det A$.
- **Forgetting to normalize the normal.** $W^{\mathsf{T}} n_X$ has the length of $n_X$ times a factor that depends on the direction. Shading formulas such as the [Fresnel equations](/fresnel-equations/) assume unit normals.
- **Offsets for secondary rays.** A fixed offset $\epsilon$ that moves a new ray off the surface means different world distances in different instances. Choose the offset in world space, from the size of the coordinates of the hit point.
- **Precision of far instances.** An object placed far from the origin by a large $s$ loses relative precision in $o - s$. Use the hit point computed in object space and mapped forward when the world value is too coarse, or keep the instance near the origin of its parent.
- **Singular matrices.** A matrix with $\det A = 0$ squashes the object flat and has no inverse. Reject such instances when the scene is built.

## Exercises

1. Show that the hit parameter is unchanged when $d' = W d$ and that it changes by the factor $\lVert W d \rVert$ when $d'$ is normalized, for a unit world direction $d$.
2. Prove that $A n$ is normal to the image of a surface for every normal $n$ if and only if $A^{\mathsf{T}} A = c^2 I$ for some $c > 0$.
3. For $A = \operatorname{diag}(-1, 1, 1)$ and the object triangle $(0,0,0)$, $(1,0,0)$, $(0,1,0)$ with normal $(0,0,1)$, compute the cross-product normal of the mapped triangle and $W^{\mathsf{T}} n$. *Answer:* $(0, 0, -1)$ and $(0, 0, 1)$; the instance is a mirror image, and only the second vector points to the side that maps from the outer side of the object.
4. A tree has $10^5$ triangles stored as three vertices of three 4-byte floats each. Compare the memory of a flattened forest of 1000 trees with that of one tree plus 1000 instances that each store $A$, $W$ and $s$ as 4-byte floats. *Answer:* $3.6 \times 10^9$ bytes against $3.6 \times 10^6 + 1000 \cdot 84$ bytes, about $3.7 \times 10^6$.
5. Write the world box of a unit cube instance under a rotation by $45°$ about the $z$ axis, and compare its volume with the cube's.

## References
