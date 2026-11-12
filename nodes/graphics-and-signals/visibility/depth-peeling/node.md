---
tag: 0TEAXT
kind: algorithm
slug: depth-peeling
name: Depth peeling
area: graphics-and-signals/visibility
level: advanced
summary: Render the scene once per depth layer with two depth tests, so that pass m keeps the m-th nearest surface at each pixel, then blend the layers in order.
solves: [hidden-surface-removal]
model: real-ram
complexity:
  vars: {n: the number of triangles, W: the image width in pixels, H: the image height in pixels, P: "the number of covered pixel centers, summed over all triangles", d: "the depth complexity, the largest number of fragments at one pixel"}
  time: {worst: Θ((d + 1) (W H + n + P))}
  space: {extra: Θ(W H)}
properties: {stable: true, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1989
  people: [Abraham Mammen, Cass Everitt]
  note: Mammen described the rendering of layers in depth order with a second depth buffer in 1989. Everitt showed in 2001 how to run it on a GPU, with the shadow-map compare as the second depth test, for order-independent transparency.
prereqs: [z-buffer, alpha-blending]
see_also: [a-buffer, occlusion-query, z-fighting, painters-algorithm, porter-duff-compositing, image-compositing, shadow-mapping]
sources:
  - paper: doi:10.1109/38.31463
    title: Abraham Mammen, Transparency and antialiasing algorithms implemented with the virtual pixel maps technique, IEEE Computer Graphics and Applications 9(4), 1989, pages 43 to 55
    locator: the whole paper (the layers in depth order from two depth buffers, and the transparency algorithm)
  - paper: "Cass Everitt, Interactive Order-Independent Transparency, NVIDIA technical white paper, 2001"
    locator: the whole paper (depth peeling with two depth tests, one pass per layer, and the front-to-back blend of the layers)
  - paper: "Louis Bavoil and Kevin Myers, Order Independent Transparency with Dual Depth Peeling, NVIDIA technical white paper, 2008"
    locator: the whole paper (peeling the nearest and the farthest layer in each pass)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 5.5 (transparency, the over and under operators, and depth peeling)
---

Depth peeling gets the surfaces at each pixel in depth order, one layer per pass, with only an ordinary [z-buffer](/z-buffer/). Each pass draws the whole scene with two depth tests: a fragment must be behind the layer that the previous pass kept, and nearer than every other such fragment in this pass. So pass 1 keeps the nearest surface, pass 2 the second nearest, and so on. The layers are then blended in order, which gives correct transparency without a sort of the scene. It is one method for *order-independent transparency*; the [A-buffer](/a-buffer/) with per-pixel lists is another.

## In plain words

To draw glass correctly, you must mix the colors at each dot from the nearest surface to the farthest one, in order. But the surfaces arrive in any order.

Depth peeling draws the whole scene many times. The first time, it keeps only the nearest surface at each dot, as a normal depth buffer does. The second time, it throws away everything that is not behind the first surface, and keeps the nearest of what is left: the second surface. Each time it peels one more layer, like the skin of an onion.

When a time comes where no dot gets a new surface, all layers are found. Then the layers are mixed in order.

## The problem

The input is a list of $n$ triangles in screen space, each with a color and an opacity $\alpha \in [0, 1]$, an image of $W \times H$ pixels and a background. A vertex is $(x, y, z)$ with $x$ to the right and $y$ down in pixel units, and $z$ the depth, smaller nearer, affine in $x$ and $y$ on each triangle. Pixel $(i, j)$ is the point sample at $(i + \tfrac12, j + \tfrac12)$, under the [top-left fill rule](/top-left-fill-rule/). A *fragment* is a pair of a triangle and a pixel center that it covers, with the plane depth there.

The output is the list of layers: layer $m$ gives, at each pixel, the triangle of the $m$-th nearest fragment there, or nothing. Fragments are ordered by the key (depth, index), so that equal depths have a fixed order. The second output is the color at each pixel: the [over](/alpha-blending/) composite of the fragments in this order, then the background. With exact arithmetic both are exact.

## The algorithm

$\mathit{prev}$ is the depth buffer of the previous pass, read only, and $\mathit{best}$ is the depth buffer of this pass, with the usual less-than test. Depths are compared as keys (depth, index).

```pseudo id=main
DEPTH-PEEL(W, H, T)
L1  prev ← −∞ at each pixel
L2  loop
L3      best ← +∞ at each pixel; layer ← nothing at each pixel
L4      for each fragment (pixel p, key z, triangle k) of the scene do
L5          if z ≤ prev[p] then discard                   ▷ the peel test
L6          if z < best[p] then                           ▷ the usual depth test
L7              best[p] ← z; layer[p] ← k
L8      if no pixel of best was written then stop         ▷ an occlusion query that counts 0
L9      output layer
L10     prev ← best

COMPOSITE(layers)                                       ▷ at each pixel, front to back
L11 τ ← 1; c ← 0
L12 for each layer m = 1, 2, ... with a triangle k at the pixel do
L13     c ← c + τ α_k color_k; τ ← τ (1 − α_k)
L14 c ← c + τ · background
```

On a GPU, line L5 is the second depth test. Everitt ran it with the shadow-map compare of the texture unit: $\mathit{prev}$ is bound as a depth texture, and a fragment whose depth is not greater than the texel is killed. Line L8 is an [occlusion query](/occlusion-query/) on the pass. The blend of lines L11 to L14 runs after each pass, with the *under* operator, so that no layer needs to be stored.

## Example

Three rectangles on a $6 \times 1$ image, drawn in the order $A$, $B$, $C$: $A$ covers $x \in [0, 6]$ at depth 3, $B$ covers $[0, 4]$ at depth 1, $C$ covers $[2, 6]$ at depth 2. The passes give:

| pass | layer | what the peel test removes |
|---|---|---|
| 1 | `BBBBCC` | nothing |
| 2 | `AACCAA` | $B$, and $C$ at pixels 4 and 5 |
| 3 | `..AA..` | everything but $A$ at pixels 2 and 3 |
| 4 | nothing written | everything; stop |

At pixel 2 the three passes give $B$, $C$, $A$, the order of the depths 1, 2, 3, although $A$ was drawn first. At pixel 0 the second layer is already the last. If $B$ has $\alpha = \tfrac12$ and $A$ is opaque, pixel 0 gets $\tfrac12 \mathrm{col}_B + \tfrac12 \mathrm{col}_A$.

## Correctness

Let the fragments at a pixel have the keys $\kappa_1 < \kappa_2 < \dots < \kappa_r$. By induction on $m$, after pass $m$ the value $\mathit{prev}$ at the pixel is $\kappa_m$ if $m \le r$ and $+\infty$ if not. Pass 1 has $\mathit{prev} = -\infty$, so it keeps the least key, as a z-buffer does. In pass $m + 1$ the peel test lets through exactly the keys greater than $\kappa_m$, and the depth test keeps the least of them, which is $\kappa_{m + 1}$; with no such key the pixel keeps $+\infty$, and it then rejects every fragment in later passes. So layer $m$ is the $m$-th fragment at each pixel, the loop stops after pass $d + 1$, and the composite takes the fragments in key order, which is the over composite front to back. The proof file gives the details.

## Complexity

Each pass is a z-buffer pass, $\Theta(W H + n + P)$. There are $d + 1$ passes, the last one writing nothing, so the time is $\Theta((d + 1)(W H + n + P))$. This is the main cost: the whole scene is drawn once for each layer, even in regions with one layer. The extra space is three buffers of $W \times H$: $\mathit{prev}$, $\mathit{best}$ and the accumulated color, with the under blend after each pass.

## Properties

- **Exact order.** Each pixel gets its fragments in exact depth order, whatever the order of the triangles.
- **No extra memory per fragment.** The memory does not depend on the depth complexity, unlike the per-pixel lists of the [A-buffer](/a-buffer/).
- **Many passes.** The number of passes is the largest depth complexity over all pixels, so one small region with many layers sets the cost for the whole screen.
- **Image space.** Only pixel centers are peeled; see [object space and image space](/object-space-vs-image-space/).

## Variants and improvements

- **Dual depth peeling.** Bavoil and Myers (2008) peel the nearest and the farthest remaining layer in each pass, with a min-max blend in place of the depth test, which about halves the number of passes.
- **Fewer passes.** Stop after a fixed number of passes, and blend the rest in one approximate pass; the far layers add little when the near ones are fairly opaque.
- **Several layers per pass.** Methods that keep the $k$ nearest fragments in each pass, with multiple render targets or a k-buffer, peel $k$ layers at once.
- **Other uses.** The layers of a depth peel give the depth complexity of the scene, the thickness of objects for volume effects, and the depth layers for screen-space ray tracing and ambient occlusion.

## When to use it

Use depth peeling for correct transparency on hardware that has a depth test and a depth texture but no per-pixel lists, or when the memory of lists cannot be bounded, and when the number of layers is small. With many layers, an [A-buffer](/a-buffer/) with lists, a sort of the scene with the [painter's algorithm](/painters-algorithm/), or an approximate weighted blend is faster.

## Pitfalls

- **Precision of the peel test.** The peel test compares the depth of a fragment with the depth stored in the previous pass. If the two are computed in different ways, for example at different precisions, a fragment can fail to match its own stored depth, and a layer is peeled twice or skipped. Use the same depth computation in both passes.
- **Coplanar surfaces.** With depth alone as the key, as in the hardware form, a strict peel test keeps only one of several fragments with equal depth at a pixel, and the others are lost; a non-strict test peels the same layer again and never ends. A tie break by an index or a primitive ID fixes this. See [z-fighting](/z-fighting/).
- **The stop test.** Stopping when a pass writes no pixel needs a count over the image, as an occlusion query gives; a fixed number of passes can stop too early.
- **Blend order.** Front-to-back blending needs the under operator and the transmittance kept per pixel; using the usual over operator in this order gives wrong colors.

## Implementations

## History

Mammen (1989) described the rendering of transparent surfaces in depth order, one layer per pass, with a second depth buffer that holds the layer of the previous pass. Everitt (2001) showed how to do it on a GPU of that time, with a depth texture and the shadow-map compare as the second depth buffer, and called the method depth peeling. Bavoil and Myers (2008) introduced dual depth peeling.

## References
