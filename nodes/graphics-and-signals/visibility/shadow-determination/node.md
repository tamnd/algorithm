---
tag: 9ZK8BG
kind: problem
slug: shadow-determination
name: Shadow determination
aliases:
- shadow computation
- shadow generation
area: graphics-and-signals/visibility
level: core
summary: Determine which surface points are hidden from a light source.
prereqs: [hidden-surface-removal, ray-casting]
see_also: [shadow-mapping, shadow-volume-algorithm, any-hit-query, whitted-ray-tracing, distributed-ray-tracing, ambient-occlusion, next-event-estimation, visibility-culling]
sources:
  - paper: doi:10.1145/563858.563901
    title: Franklin C. Crow, Shadow algorithms for computer graphics, Proceedings of SIGGRAPH 1977, Computer Graphics 11(2), pages 242 to 248
    locator: the survey of the shadow methods of the time and their classification
  - paper: doi:10.1145/965139.807402
    title: Lance Williams, Casting curved shadows on curved surfaces, Proceedings of SIGGRAPH 1978, Computer Graphics 12(3), pages 270 to 274
    locator: the depth image from the light and the depth comparison at each visible point
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 7 (Shadows), with Section 7.3 (Shadow Volumes), pages 230 to 234, and Section 7.4 (Shadow Maps), from page 234
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, 1990
    locator: Chapter 16, Section 16.4 (shadows)
---

Shadow determination is the problem of finding, for each point of a scene that the camera sees, whether a light reaches it, or which part of an area light reaches it. A point is in shadow from a point light when the segment from the point to the light meets an opaque surface. So the problem is [hidden surface removal](/hidden-surface-removal/) with the light in place of the eye, and each method for one problem gives a method for the other. Crow in 1977 surveyed the early methods. The main families today are [shadow mapping](/shadow-mapping/), which samples depth from the light, [shadow volumes](/shadow-volume-algorithm/), which bound the shadowed space with polygons, and shadow rays, which are [any-hit queries](/any-hit-query/) toward the light.

## In plain words

A point on the floor is lit if you could stand on it and see the lamp. If a table is in the way, the point is in shadow. Finding the shadows of a picture means asking that question for each point that the picture shows.

With a tiny lamp the answer is yes or no, and the shadows have sharp edges. With a large lamp, such as a window or a bright sky, a point can see part of the lamp. Then the shadow has a dark core and a soft edge, where more and more of the lamp becomes visible.

## Definition

**Input.** A scene of opaque surfaces. A light: a point $L$, a direction $d$ for a light at infinity, or an area light $A$, a surface that emits light. The set of *receiver points* $P$: in a renderer, the points that the camera sees, one for each pixel sample.

**Point and directional lights.** The point $P$ is *in shadow* when the open segment from $P$ to $L$ meets a surface. For a directional light, use the open ray from $P$ in the direction $-d$. The output is one bit $s(P)$ for each receiver point.

**Area lights.** For a point $y$ of $A$, let $\nu(P, y) = 1$ when the segment from $P$ to $y$ meets no surface, and $0$ otherwise. The output is the *visible fraction*
$$v(P) = \frac{1}{|A|} \int_A \nu(P, y)\, dy,$$
or the same integral with a weight for the emitted light and the angles. $P$ is in the *umbra* when $v(P) = 0$, in the *penumbra* when $0 < v(P) < 1$, and lit when $v(P) = 1$.

**Precision.** At *object precision*, the output is the exact shadow region on each surface, as polygons for polygonal scenes. At *image precision*, it is a value for each pixel sample. The surface of $P$ itself must not count as a blocker at $P$, so each method needs a rule for the segment near its start point.

## Variants

- **Hard and soft shadows.** Point and directional lights give hard shadows, with one bit per point. Area lights give soft shadows, with a fraction per point, and this needs many visibility tests or an estimate of the integral.
- **Many lights.** Each light gives its own problem. The cost grows with the number of lights unless the method selects the lights that matter at each point.
- **Self-shadowing.** An object shadows parts of itself, as on folds of cloth. Methods that treat each object as a single occluder or receiver miss this.
- **Transparent and partly opaque occluders.** The output is the product of the transmissions along the segment, not a bit. Examples are colored glass, smoke and hair.
- **Static or dynamic scenes.** For a static scene and a static light, the shadows can be computed once and stored, for example in a light map. Moving objects or lights need the computation for each frame.
- **Ambient occlusion.** The visible fraction of the hemisphere above $P$, with a distance limit, is a related problem. See [ambient occlusion](/ambient-occlusion/).

## Examples

**A square under a point light.** The occluder is the square $[-1, 1]^2$ at height $z = 2$. The light is $L = (0, 0, 4)$, and the ground is $z = 0$. The segment from $P = (p, 0, 0)$ to $L$ is at height $2$ halfway, at the point $(p/2, 0, 2)$. So $P$ is in shadow when $|p/2| \le 1$, that is, when $|p| \le 2$. For example, $(1.5, 0, 0)$ is in shadow and $(2.5, 0, 0)$ is lit. The shadow is the square $[-2, 2]^2$: the occluder scaled by the factor $4 / (4 - 2) = 2$ from the point under the light.

**The same square under a line light.** Replace $L$ by the segment light from $(-1, 0, 4)$ to $(1, 0, 4)$. The segment from $P = (p, 0, 0)$ to the light point $(\ell, 0, 4)$ is at height $2$ at $x = (p + \ell)/2$. So it is blocked when $|p + \ell| \le 2$. For $p \ge 0$, the light points with $\ell > 2 - p$ are visible, and the visible fraction is
$$v(p) = \begin{cases} 0 & 0 \le p \le 1, \\ (p - 1)/2 & 1 \le p \le 3, \\ 1 & p \ge 3. \end{cases}$$
The umbra is $|p| \le 1$, the penumbra is $1 < |p| < 3$, and at $p = 2$, the edge of the hard shadow above, exactly half of the light is visible.

**Errors of a sampled method.** A shadow map of the first scene stores the nearest depth from the light on a grid. A receiver point compares its own distance to the light with the stored distance of its grid cell. With a small offset (*bias*) to avoid false self-shadowing, points near the shadow edge at $|p| = 2$ can be put on the wrong side, up to about the size of one grid cell on the ground. [Shadow volumes](/shadow-volume-algorithm/) give the exact edge at each pixel sample.

## Known algorithms

| method | year | precision | idea |
|---|---|---|---|
| Shadow rays in [ray casting](/ray-casting/) | 1968 | image | for each visible point, an [any-hit query](/any-hit-query/) on the segment to the light |
| [Shadow volume algorithm](/shadow-volume-algorithm/) | 1977 | image, exact per sample | the volume behind each silhouette; count the crossings along the eye ray |
| [Shadow mapping](/shadow-mapping/) | 1978 | image, sampled from the light | a depth image from the light; compare depths |
| Shadow polygons by hidden surface removal from the light | 1978 | object | the visible parts from the light are the lit polygons |
| [Whitted ray tracing](/whitted-ray-tracing/) | 1980 | image | shadow rays at each hit point, also after reflections |
| [Distributed ray tracing](/distributed-ray-tracing/) | 1984 | image, soft shadows | many shadow rays to random points of an area light |

Appel in 1968 traced rays from visible points toward the light to find shadows. Atherton, Weiler and Greenberg in 1978 found the lit polygons with a hidden surface method run from the light. Reeves, Salesin and Cook in 1987 filtered the shadow map comparisons for soft edges (percentage-closer filtering). In path tracing, [next event estimation](/next-event-estimation/) is the shadow ray of a Monte Carlo estimate of the integral $v(P)$.

## Bounds

- **Per point.** One shadow test for a point light is one [any-hit query](/any-hit-query/). It takes $O(n)$ time for $n$ triangles by brute force. With a [bounding volume hierarchy](/bounding-volume-hierarchy/), it often takes time close to logarithmic in $n$, but in the worst case it is still $O(n)$.
- **Object precision.** The lit region of a polygonal scene under a point light is the visibility map from the light, mapped onto the surfaces. So its size has the same worst case as that of hidden surface removal: $\Theta(n^2)$ for $n$ polygons.
- **Soft shadows.** The boundaries of the umbra and the penumbra of a polygonal area light are made of pieces of planes and, in general, of quadric surfaces (the surfaces swept by the lines that meet three edges). So exact soft shadows are much more complex than hard shadows, and most methods estimate $v(P)$ with samples. With $k$ independent random samples of the light, the error of the mean has standard deviation $\sqrt{v(1 - v)/k} \le 1/(2\sqrt{k})$.
- **Sampled methods.** A shadow map of resolution $r \times r$ resolves the shadow edge only to the size of a grid cell on the receiver. That size grows with the distance from the light and with the angle between the receiver and the light direction.

## Reductions

- **To hidden surface removal from the light.** For a point light, the lit points are the points that the light sees. So a hidden surface method run from the light, at object or image precision, solves the problem. Shadow mapping is the [z-buffer](/z-buffer/) from the light.
- **To ray queries.** For a point light, $s(P)$ is an any-hit query on the segment from $P$ to $L$. For an area light, $v(P)$ is an integral of such queries, which [Monte Carlo integration](/monte-carlo-integration/) estimates.
- **To point-in-volume tests.** A point is in shadow when it is inside the union of the shadow volumes of the occluders. The shadow volume method counts crossings to decide this.
- **From visibility culling.** The objects that can cast a shadow into the view are found by [visibility culling](/visibility-culling/) from the light, which limits the work of each method.

## Applications

Shadows are a main cue of depth and contact in an image: they show where an object touches the ground and how far it is above it. Each renderer for games, film, architecture and product design computes them. Real-time renderers use shadow maps for most lights, and sometimes shadow volumes or ray-traced shadows on hardware with ray tracing support. Offline renderers use shadow rays. The same visibility question also arises outside graphics: in the planning of solar panels and buildings (which parts are in the sun), and in terrain analysis.

## References
