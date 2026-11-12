---
tag: MPWTBP
kind: concept
slug: early-depth-test
name: Early depth test
aliases:
- early-z
- early depth rejection
area: graphics-and-signals/visibility
level: advanced
summary: The depth test done before the fragment shader, not after it, so that hidden fragments are never shaded. It is valid only when the shader cannot change the result of the test.
prereqs: [z-buffer]
see_also: [hierarchical-z-buffer, graphics-pipeline, occlusion-query, painters-algorithm, alpha-blending, stencil-buffer, random-permutation]
sources:
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 23.7 (depth culling, early-z, and the conditions under which it is disabled)
  - url: https://registry.khronos.org/OpenGL/extensions/ARB/ARB_shader_image_load_store.txt
    title: The Khronos Group, ARB_shader_image_load_store, OpenGL extension specification
    locator: the layout qualifier early_fragment_tests (the depth and stencil tests run before the fragment shader, and a depth written by the shader is ignored)
---

The *early depth test* runs the depth test of the [z-buffer](/z-buffer/) before the fragment shader, not after it. In the logical order of the [graphics pipeline](/graphics-pipeline/) the shader runs first and the depth test second, so every fragment is shaded, also the ones that the test then rejects. When the shader cannot change the outcome of the test, the GPU can test first and skip the shader for each fragment that fails. The result is the same image, at a cost that depends on the order in which the scene is drawn.

## In plain words

A painter who paints a wall and then puts a cupboard in front of it has wasted the paint behind the cupboard. A depth buffer is like this too, in its basic form: it works out the full color of each new piece of a surface, and only then checks if something nearer is already there.

The early depth test does the check first. If something nearer is already at that dot, the color of the new piece is never worked out. This saves much work, because working out the color is the expensive step.

It only helps when near things come first. If the scene is drawn from far to near, each new piece is nearer than the old one, and nothing is saved.

## The idea

**The logical order.** For each fragment, the pipeline runs the fragment shader, then the per-fragment tests (stencil, then depth), then the blend. The depth test needs only the depth of the fragment, which is known after rasterization. So the test can move before the shader, if the move cannot change what is written.

**When the move is valid.** The test can run early when the shader does not decide the depth or the survival of the fragment:

- *Depth written by the shader.* If the shader writes its own depth, the depth to test is not known before the shader runs, and the test must be late. Qualifiers that promise the shader only moves the depth in one direction (conservative depth) let the hardware keep a part of the early test.
- *Discard.* A shader that can discard a fragment, as an alpha test does, decides whether the fragment writes depth. The test can still reject early, but the depth write must wait for the shader, and some hardware then does the whole test late.
- *Side effects.* A shader that writes to memory (image stores, atomic counters) runs for fragments that a late test would reject, and these writes are visible. OpenGL lets the shader ask for the early test explicitly with `layout(early_fragment_tests) in;`, and then the tests run before the shader and any depth that the shader writes is ignored.

**Coarse early tests.** GPUs also test whole tiles of pixels against the farthest depth of the tile, before the per-pixel early test. This is the one-level form of the [hierarchical z-buffer](/hierarchical-z-buffer/). The nearest depth of a tile lets a tile that is surely in front skip the reads of the depth buffer.

**The order of drawing.** The early test saves the shading of each fragment that is behind a fragment drawn *before* it. At a pixel with $d$ opaque surfaces at distinct depths, the number of shaded fragments is the number of fragments that are nearer than all the fragments drawn before them at that pixel. Front to back this is 1, back to front it is $d$, and a late test always shades $d$.

**Depth prepass.** Draw the scene once with depth writes only and a trivial shader, then draw it again with the full shader and the depth test *equal*. The second pass shades exactly one fragment per pixel, whatever the order, at the cost of drawing the geometry twice.

## Examples

**A random order.** Draw $d$ opaque layers that each cover a pixel, at distinct depths, in an order chosen uniformly at random from all [permutations](/random-permutation/). The $m$-th fragment drawn is shaded when it is the nearest of the first $m$, which has probability $1/m$. So the expected number of shaded fragments is
$$1 + \tfrac12 + \tfrac13 + \dots + \tfrac1d,$$
the harmonic number $H_d$. For $d = 4$ it is $\tfrac{25}{12} \approx 2.08$, against 4 for a late test and 1 for front to back.

| order | shaded fragments at a pixel with $d = 4$ layers |
|---|---|
| late depth test, any order | 4 |
| early test, back to front | 4 |
| early test, random order | $25/12$ on average |
| early test, front to back | 1 |
| depth prepass, then early test with *equal* | 1 (plus 4 depth-only fragments in the prepass) |

**An alpha-tested plant.** Leaves drawn as quads with a texture and a discard where the texture is clear cover a large part of the screen with many layers. The discard delays the depth write, so the layers do not hide one another early as opaque quads would. A depth prepass for the leaves, or a separate pass for the alpha-tested geometry, restores the early rejection.

**A shader that writes depth.** A shader that moves the depth of each fragment, for example to draw spheres as flat quads with an exact sphere depth, turns off the early test for every fragment it shades. If it only moves the depth farther from the camera, a conservative-depth qualifier lets the hardware reject early the fragments that are already behind the stored depth.

## Where it is used

Every GPU does early depth testing, and engines sort opaque objects roughly front to back to profit from it, often with a depth prepass. Deferred renderers rely on it in the pass that writes the surface attributes of each pixel. Transparent surfaces are drawn after the opaque ones, back to front with the depth test on and depth writes off, so that the early test rejects the transparent fragments behind opaque surfaces; see [alpha blending](/alpha-blending/). The same principle, a cheap test before expensive work, gives the [occlusion query](/occlusion-query/), which tests a whole bounding box before an object is drawn, and the [stencil buffer](/stencil-buffer/) test, which also runs early when it can.

## References
