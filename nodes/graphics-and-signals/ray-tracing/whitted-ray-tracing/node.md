---
tag: GC6JDN
kind: algorithm
slug: whitted-ray-tracing
name: Whitted ray tracing
aliases:
- recursive ray tracing
area: graphics-and-signals/ray-tracing
level: intro
summary: Render each pixel by following, from the visible point, a reflected ray, a refracted ray and shadow rays to the lights, recursively to a fixed depth, and adding up the weighted intensities.
model: real-ram
complexity:
  vars: {P: the number of pixels, n: the number of objects, m: the number of point lights, D: the maximum depth of the ray tree}
  time: {worst: Θ(2^D P n (m + 1))}
  space: {extra: O(D)}
properties: {deterministic: true, recursive: false}
history:
  year: 1980
  people: [Turner Whitted]
  note: Whitted extended ray casting with a tree of reflected, refracted and shadow rays per pixel, and showed mirror reflection, refraction through glass and shadows in one renderer.
prereqs: [ray-casting, snells-law, fresnel-equations]
see_also: [distributed-ray-tracing, path-tracing, phong-shading, shadow-determination, bounding-volume-hierarchy, beam-tracing, cone-tracing, global-illumination]
sources:
  - paper: doi:10.1145/358876.358882
    title: Turner Whitted, An improved illumination model for shaded display, Communications of the ACM 23(6), 1980, 343 to 349
    locator: equation (2) for the intensity, the directions of the reflected and refracted rays, the tree of rays per pixel, and the results section with the times and the share of the intersection tests
  - paper: doi:10.1145/1468075.1468082
    title: Arthur Appel, Some techniques for shading machine renderings of solids, AFIPS Spring Joint Computer Conference, vol. 32, 1968, 37 to 45
    locator: the rays from the eye for visibility and the rays to the light for shadows, which Whitted's method extends
  - paper: "Roy A. Hall and Donald P. Greenberg, A testbed for realistic image synthesis, IEEE Computer Graphics and Applications 3(8), 1983"
    locator: the adaptive control of the depth of the ray tree by the weight of each ray
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 4, Ray Tracing (shadows and ideal specular reflection), and the later chapter on more ray tracing (transparency and refraction)
---

Whitted ray tracing renders an image by following rays from the eye into the scene and, at each surface that a ray hits, sending new rays: one in the mirror direction, one through the surface if the object is transparent, and one toward each light to test for shadow. The reflected and refracted rays are traced in the same way, so each pixel gets a tree of rays, cut at a fixed depth. The intensity at a hit is a local term plus constant multiples of the intensities that come back along the reflected and refracted rays. It is [ray casting](/ray-casting/) made recursive, and it was the first method that rendered mirrors, glass and shadows correctly in one renderer. The reflected ray obeys the law of reflection and the refracted ray obeys [Snell's law](/snells-law/); modern versions weight them by the [Fresnel equations](/fresnel-equations/).

## In plain words

Imagine looking at a room full of shiny balls and glass marbles. To know the color of one spot on a shiny ball, you ask three questions. Is the spot lit, or is something between it and the lamp? What does the ball reflect there, like a mirror? If the ball is glass, what do you see through it?

The second and third questions are new pictures of the same scene, seen from the spot in a new direction. So the renderer asks the same three questions again where those new lines of sight land, and again, a few levels deep. The answers come back up and add up to one color for the pixel.

Light that bounces between two mirrors would go on forever, so the renderer stops after a fixed number of bounces.

## The problem

The scene is a set of $n$ objects, each with a surface normal at every point and a material with the constants $k_a$ (ambient), $k_d$ (diffuse), $k_s$ (mirror) and $k_t$ (transmission), and for transparent solids an index of refraction $\eta$. There are $m$ point lights with the intensities $E_\ell$, a background value, a [pinhole camera](/pinhole-camera-model/) and a maximum depth $D \ge 0$.

For a ray $r = (o, d)$ with unit direction $d$, let $p$ be its closest hit and $n$ the unit normal there, turned so that $n \cdot d < 0$. The value of the ray with $k$ levels left is

$$V_k(r) = k_a + k_d \sum_{\ell \text{ visible from } p} E_\ell \cos\theta_\ell + [k > 0]\,\big(k_s\,V_{k-1}(r_s) + k_t\,V_{k-1}(r_t)\big),$$

where $\theta_\ell$ is the angle between $n$ and the direction to light $\ell$, $r_s$ is the reflected ray from $p$, and $r_t$ is the refracted ray from $p$, whose term is dropped under total internal reflection. A ray that hits nothing has the background value. The pixel gets $V_D$ of the ray through its center. This is the [Lambertian](/lambertian-reflectance/) part and the recursive part of Whitted's equation (2); the paper also adds a Phong highlight for each light, which is a local term like the diffuse one and changes nothing below.

## The algorithm

```pseudo id=main
WHITTED(objects, lights, camera, D)
L1  for each pixel (i, j) of the image
L2      image[i, j] ← TRACE(PRIMARY-RAY(i, j, 1/2, 1/2), D)

TRACE((o, d), D)
L3  I ← 0;  S ← a stack holding (o, d, 1, 0)                ▷ ray, weight, depth
L4  while S is not empty
L5      pop (o, d, w, k) from S
L6      find the closest hit of (o, d) in (ε, ∞)
L7      if there is none then I ← I + w · background;  continue
L8      p ← the hit point;  n ← the normal, turned so that n · d < 0;  η ← n_this side / n_other side
L9      I ← I + w · ka
L10     for each light ℓ
L11         if n · (ℓ − p) > 0 and no object meets the segment from p to ℓ then I ← I + w · kd · E_ℓ · cos(n, ℓ − p)
L12     if k = D then continue
L13     if ks > 0 then push (p, d − 2 (d · n) n, w · ks, k + 1)
L14     if kt > 0 and REFRACT(d, n, η) exists then push (p, REFRACT(d, n, η), w · kt, k + 1)
L15 return I
```

Line L2 is [primary ray generation](/primary-ray-generation/) through the pixel center, as in ray casting. Line L6 is a [closest-hit query](/closest-hit-query/), for example by a scan over the objects with the [ray-sphere](/ray-sphere-intersection/) and [ray-plane](/ray-plane-intersection/) tests; the lower bound $\varepsilon$ keeps a new ray from hitting the surface it starts on. Line L8 turns the normal toward the incoming ray: when the ray leaves a solid the normal flips and the ratio of the indices is inverted. Lines L10 and L11 are the shadow rays, an [any-hit query](/any-hit-query/) on the open segment to each light, which is the ray form of [shadow determination](/shadow-determination/).

Line L13 is the law of reflection. Line L14 uses Snell's law: with $c = -d \cdot n$ and $\eta = n_1 / n_2$, the refracted direction is $\eta\,d + (\eta c - \sqrt{1 - \eta^2 (1 - c^2)})\,n$, and it does not exist when the root is of a negative number, which is total internal reflection.

Whitted described the method as a recursion: build the tree of rays, then evaluate it from the leaves up. TRACE walks the same tree with an explicit stack. Each node carries the product of the coefficients on its path from the root, its weight $w$, and adds $w$ times its local term at once. Because $V_k$ is linear in the values of the children, the sum over the nodes of weight times local term equals the recursive value.

## Example

A glass sphere of radius 1 at $(0, 0, -4)$ with $k_s = 0.1$, $k_t = 0.9$, $\eta = 1.5$ and no local term; behind it a wall $z = -8$ with $k_a = 0.1$ and $k_d = 0.6$; one point light of intensity 1 at $(0, 4, -6)$; a black background; $D = 3$. Trace the ray from the eye at the origin along $-z$, through the center of the sphere, so that every refraction is at normal incidence and the rays stay on the axis.

| pop | node | depth $k$ | weight $w$ | hit | local term | $I$ after |
|---|---|---|---|---|---|---|
| 1 | eye | 0 | 1 | sphere, front, $z = -3$ | 0 | 0 |
| 2 | T | 1 | 0.9 | sphere, back from inside, $z = -5$ | 0 | 0 |
| 3 | TT | 2 | 0.81 | wall, $z = -8$ | 0.3683 | 0.2983 |
| 4 | TR | 2 | 0.09 | sphere, front from inside, $z = -3$ | 0 | 0.2983 |
| 5 | TRT | 3 | 0.081 | none | background 0 | 0.2983 |
| 6 | TRR | 3 | 0.009 | sphere, back from inside, $z = -5$ | 0 | 0.2983 |
| 7 | R | 1 | 0.1 | none | background 0 | 0.2983 |

The names list the steps from the eye: T for refracted, R for reflected. Pop 1 pushes R and then T, so T comes out first. At the wall the shadow ray to the light runs from $z = -8$ to $z = -6$ and misses the sphere; the cosine is $2/\sqrt{20}$, so the local term is $0.1 + 0.6 \cdot 0.4472 = 0.3683$. The ray TRT leaves the sphere toward the eye and hits nothing. Node TRR is at the depth $D$, so it spawns no children.

The value for $D = 3$ is $0.81 \cdot 0.3683 = 0.2983$. For $D = 4$ the ray TRRT, with weight $0.0081$, also reaches the wall, and the value is $0.3013$. The light that bounces inside the sphere forms the geometric series $0.2983 \cdot (1 + 0.01 + 0.0001 + \cdots)$, whose limit is $0.3014$.

## Correctness

TRACE returns $V_D(o, d)$. The proof, in [the correctness proof](proofs/correctness.md), shows by induction over the iterations of line L4 that $I$ plus the sum of $w \cdot V_{D-k}$ over the entries of the stack always equals $V_D(o, d)$. Each iteration replaces an entry by its local term and its children, which is one unfolding of the definition, so the sum is unchanged. The loop ends because each entry has depth at most $D$ and each push raises the depth, so at most $2^{D+1} - 1$ entries are ever pushed; at the end the stack is empty and $I = V_D(o, d)$.

## Complexity

The tree of one pixel has at most $2^{D+1} - 1$ rays, when every hit is both reflecting and refracting. Each ray costs one closest-hit query and $m$ shadow queries, each $\Theta(n)$ by a scan, so a pixel costs $O(2^D\,n\,(m + 1))$ and the image $\Theta(2^D P\,n\,(m + 1))$ in the worst case. In typical scenes most surfaces are opaque and many rays leave the scene, so the trees are small, but the intersection tests still dominate: Whitted measured that they took 75 percent of the time for simple scenes and over 95 percent for complex ones. A [bounding volume hierarchy](/bounding-volume-hierarchy/) cuts the cost of each query from $\Theta(n)$ to about $O(\log n)$ for scenes that are not adversarial.

The stack holds at most $D + 1$ entries at once: one sibling waits at each level above the current one, so the extra space is $O(D)$ per pixel, besides the image.

## Properties

- **Deterministic.** No random numbers: each pixel samples one ray, so edges alias unless the renderer adds supersampling.
- **Exact for its model.** Within the model, mirror reflection, refraction and hard shadows from point lights are exact up to rounding.
- **Iterative.** The pseudocode replaces the recursion by a stack, so there is no limit from the call stack; the recursive form has depth $D$.
- **Pixels are independent.** Each pixel can be computed by its own thread, which made ray tracing one of the first embarrassingly parallel graphics methods.
- **No indirect diffuse light.** Light that reaches a diffuse surface by way of another diffuse surface, a mirror or a lens is missing: shadows are hard, there is no color bleeding and no caustics. These need [global illumination](/global-illumination/).

## Variants and improvements

- **Fresnel weights.** Replace the constants $k_s$ and $k_t$ by the [Fresnel](/fresnel-equations/) reflectance $F(\theta)$ and the transmittance $1 - F(\theta)$, or by Schlick's approximation, so that glass reflects more at grazing angles. Whitted noted that a Fresnel term would be better but kept constants.
- **Adaptive depth.** Hall and Greenberg (1983) stop a branch when its weight $w$ falls below a threshold, instead of at a fixed depth, so that faint rays cost nothing and strong ones go deep.
- **Highlights.** Whitted adds the Phong highlight of each point light as a local term. This is the Phong reflection model evaluated at the hit, not [Phong shading](/phong-shading/), which is the interpolation of normals across a triangle; a ray tracer computes the exact normal at every hit, so neither Phong nor [Gouraud shading](/gouraud-shading/) is needed for curved primitives.
- **Antialiasing.** Whitted traced rays at the pixel corners and subdivided a pixel when the corners differed. [Supersampling](/supersampling-antialiasing/) traces several rays per pixel instead.
- **Glossy reflection, soft shadows and blur.** [Distributed ray tracing](/distributed-ray-tracing/) replaces each single ray by many rays spread over the gloss lobe, the area of the light, the lens or the shutter interval.
- **Full light transport.** [Path tracing](/path-tracing/) follows one random branch of the tree per path and samples diffuse reflection as well, which solves the [rendering equation](/rendering-equation/).
- **Bundles of rays.** [Beam tracing](/beam-tracing/) and [cone tracing](/cone-tracing/) trace volumes of rays at once, for antialiasing and for soft effects.

## When to use it

Use Whitted ray tracing to learn rendering, as the next step after ray casting, and for images whose interest is in mirrors, glass and sharp shadows from small lights. It is deterministic and noise free, so it also suits previews and technical images such as the design of optics. For soft shadows, glossy surfaces or indirect light, use distributed ray tracing or path tracing; for large scenes at interactive rates, add a bounding volume hierarchy or rasterize with a [z-buffer](/z-buffer/) and trace only the reflections.

## Pitfalls

- **Self-intersection.** Querying from $t > 0$ at line L6 lets a reflected, refracted or shadow ray hit its own surface at $t \approx 0$ through rounding, which gives speckled shadows and black reflections. Start at $\varepsilon > 0$, as line L6 does, or offset $p$ along the normal, to the inside for a refracted ray.
- **Leaving a solid.** Keeping the outward normal and the ratio $1/\eta$ at line L8 when the ray is inside a glass sphere bends the ray the wrong way at the exit. Flip the normal and use $\eta$ when $n \cdot d > 0$, as line L8 does.
- **Total internal reflection.** Taking the square root at line L14 without testing the sign of $1 - \eta^2 (1 - c^2)$ gives NaN for rays inside glass at grazing angles. Drop the refracted ray, as line L14 does, and with Fresnel weights give its share to the reflected ray.
- **No depth limit.** Omitting the test of line L12 makes a ray between two parallel mirrors loop forever. Keep the cut at depth $D$, or cut by weight.
- **Black shadows of glass.** Line L11 treats every object as opaque, so a glass ball casts a shadow as dark as a stone one. Whitted attenuated the light by the objects that the shadow ray crosses; a correct caustic needs path tracing or [photon mapping](/photon-mapping/), not a change of line L11.
- **Energy.** Choosing $k_a + k_d + k_s + k_t > 1$ at lines L9 to L14 makes the value between two mirrors grow with $D$ instead of converging. Keep the sum at most 1, or use $F$ and $1 - F$.

## Implementations

## History

Arthur Appel (1968) cast rays from the eye to find the visible surface and from that surface to the light to find shadows. Kay and Greenberg (1979) rendered transparent objects with refraction by a scanline method. Turner Whitted, at Bell Labs, published the recursive method in 1980: a tree of rays per pixel, reflected and refracted rays in the exact directions, shadow rays to every light, and an adaptive subdivision of pixels for antialiasing, with bounding spheres to speed up the intersection tests. His images of glass and mirror spheres over a checkerboard, at 480 by 640 pixels, took 44 to 122 minutes each on a VAX-11/780, and they made ray tracing the standard picture of realistic rendering. Hall and Greenberg (1983) added the Fresnel weights and adaptive depth, Cook, Porter and Carpenter (1984) generalized the method to [distributed ray tracing](/distributed-ray-tracing/), and Kajiya (1986) to path tracing.

## References
