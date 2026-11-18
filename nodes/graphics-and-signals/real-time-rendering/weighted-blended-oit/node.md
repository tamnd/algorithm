---
tag: ZP9G80
kind: algorithm
slug: weighted-blended-oit
name: Weighted blended order-independent transparency
aliases:
- weighted blended OIT
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Approximate the over operator by a weighted average of the transparent colors with depth-based weights, computed in one pass with additive blending.
solves: [order-independent-transparency]
model: real-ram
complexity:
  vars: {k: the number of fragments of a pixel, f: the number of fragments in the frame, p: the number of pixels}
  time: {per_pixel: O(k), frame: O(f + p)}
  space: {per_pixel: O(1), frame: O(p)}
properties: {deterministic: true, recursive: false, online: true, in_place: false}
history:
  year: 2013
  people: [Morgan McGuire, Louis Bavoil]
  note: McGuire and Bavoil published the method in the Journal of Computer Graphics Techniques in 2013, as a weighted average with an exact coverage term and depth-based weights.
prereqs: [order-independent-transparency, alpha-blending]
see_also: [per-pixel-linked-lists, depth-peeling, a-buffer, porter-duff-compositing, particle-system, convex-combination, deferred-shading]
sources:
  - url: http://jcgt.org/published/0002/02/09/
    title: "Morgan McGuire and Louis Bavoil, Weighted blended order-independent transparency, Journal of Computer Graphics Techniques 2(2), 122-141, 2013"
    locator: the weighted average with the coverage term, the two render targets and their blend modes, and the weight functions of depth
  - url: http://casual-effects.blogspot.com/2014/03/weighted-blended-order-independent.html
    title: "Morgan McGuire, Weighted blended order-independent transparency, Casual Effects blog, March 2014"
    locator: the shader code and the weight function with the constants 0.03, 200, 1e-2 and 3e3
  - paper: doi:10.1145/800031.808606
    title: "Thomas Porter and Tom Duff, Compositing digital images, SIGGRAPH 1984, Computer Graphics 18(3), 253-259"
    locator: the premultiplied alpha and the over operator that the method approximates
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 5.5, Transparency, Alpha, and Compositing (the part on order-independent methods)
---

Weighted blended order-independent transparency is a one-pass approximation for [order-independent transparency](/order-independent-transparency/). It does not sort the fragments. Instead, it replaces the color part of the over operator by a weighted average of the fragment colors, and keeps the part that tells how much of the background shows through, which is a product and needs no order. The weight of each fragment is a function of its depth and opacity, larger for nearer fragments. On a GPU the whole method is two render targets with fixed blend modes and one full-screen pass, with a constant amount of memory per pixel. McGuire and Bavoil published it in 2013. The coverage is exact; the color is exact only in special cases, and the weight function is tuning.

## In plain words

Blending glass over glass in the right order needs a sort, and a sort per pixel is slow on a GPU. This method gives up the exact answer. It adds up the colors of all transparent layers, each multiplied by a weight, and divides by the sum of the weights, so the result is an average color. Separately, it multiplies together how much light each layer lets through, which gives the exact amount of background that shows. Nearer layers get larger weights, so they count more, as they would in a correct blend. When all the layers have about the same color, the result is right. When a red pane is in front of a blue pane, the result is a mix that is too even.

## The problem

The input is, for each pixel, an opaque background color $C_0$ and the transparent fragments $(c_i, \alpha_i, z_i)$ of that pixel in the order in which the rasterizer produces them: $c_i$ is the premultiplied linear color, $\alpha_i$ the opacity and $z_i > 0$ the view depth, smaller is nearer. The exact output is the composite in depth order defined on the [problem page](/order-independent-transparency/):

$$C = \sum_{i} c_i\, T_i + C_0 R, \qquad T_i = \prod_{z_j < z_i} (1 - \alpha_j), \qquad R = \prod_i (1 - \alpha_i).$$

The method must work in one geometry pass with $O(1)$ memory per pixel and blend operations that are commutative, so that the arrival order does not matter. Its output is

$$\tilde C = \frac{\sum_i c_i w_i}{\sum_i \alpha_i w_i} (1 - R) + C_0 R$$

for weights $w_i = w(c_i, \alpha_i, z_i) > 0$.

## The algorithm

The loop runs over the fragments of one pixel in arrival order. On a GPU, lines L1 to L5 are the blend units of two render targets, and lines L6 and L7 are a full-screen composite pass.

```pseudo id=main
WEIGHTED-BLENDED-OIT(fragments, C0, WEIGHT, ε)
L1  A ← 0 (one sum per color channel);  Aα ← 0;  R ← 1
L2  for each fragment (c, α, z) of the pixel, in arrival order
L3      w ← WEIGHT(c, α, z)
L4      A ← A + c w;  Aα ← Aα + α w                    ▷ additive blending
L5      R ← R (1 - α)                                  ▷ multiplicative blending
L6  avg ← A / max(Aα, ε)
L7  return avg (1 - R) + C0 R
```

**The render targets (lines L4 and L5).** The first target holds $(A, A_\alpha)$ in a 16-bit or 32-bit float RGBA format. The fragment shader writes $(c w, \alpha w)$ and the blend mode is ONE, ONE, an addition. The second target holds $R$ in one channel, cleared to 1. The shader writes $\alpha$ and the blend mode is ZERO, ONE_MINUS_SRC_ALPHA, so the stored value is multiplied by $1 - \alpha$. Both blends commute, so the order of the fragments does not matter. The depth test is on against the opaque depth buffer, with depth writes off.

**The composite (lines L6 and L7).** A full-screen pass reads both targets and blends $avg$ over the opaque image with the factor $1 - R$. The guard $\varepsilon$ stops a division by zero where no transparent fragment lies.

**The weight (line L3).** The weight should be larger for nearer fragments, because the exact weight of fragment $i$ is $T_i$, which falls as more fragments lie in front of it. The method cannot know $T_i$ without the order, so it uses a fixed function of depth. McGuire's blog post of 2014 gives

$$w = \max\big(\min(1, \max(c_r, c_g, c_b)),\ \alpha\big) \cdot \operatorname{clamp}\Big(\frac{0.03}{10^{-5} + (z / 200)^4},\ 10^{-2},\ 3 \cdot 10^{3}\Big),$$

where the code of this page uses the positive view depth for $z$ and the premultiplied color for $c$. The first factor makes nearly invisible fragments count little. The constants suit a depth range of a few hundred units and must be tuned for other scenes; the clamp keeps the weights inside the range of a 16-bit float.

## Example

A red fragment with $c = (0.5, 0, 0)$, $\alpha = 0.5$ lies in front of a blue fragment with $c = (0, 0, 0.5)$, $\alpha = 0.5$, over black. The exact result is $(0.5, 0, 0.25)$.

| weights (red, blue) | $A$ | $A_\alpha$ | $avg$ | $\tilde C$ | error per channel |
|---|---|---|---|---|---|
| 1, 1 | $(0.5, 0, 0.5)$ | 1 | $(0.5, 0, 0.5)$ | $(0.375, 0, 0.375)$ | 0.125 |
| 3, 1 | $(1.5, 0, 0.5)$ | 2 | $(0.75, 0, 0.25)$ | $(0.5625, 0, 0.1875)$ | 0.0625 |
| 2, 1 | $(1, 0, 0.5)$ | 1.5 | $(0.667, 0, 0.333)$ | $(0.5, 0, 0.25)$ | 0 |

In all rows $R = 0.25$, so $1 - R = 0.75$, the exact coverage. The weights 2 and 1 are in the ratio of the exact transmittances $T = (1, 0.5)$, and they give the exact result. With equal weights, the two panes are mixed half and half, and the red pane in front does not dominate. The order of the two fragments in the loop makes no difference in any row.

## Correctness

The method is not exact in general, so correctness here means a list of exact statements, which the proofs folder proves and the tests check in exact rational arithmetic.

- **Order independence.** Lines L4 and L5 build two sums and a product, which do not depend on the order of their terms. The tests shuffle the fragments and get the same fraction each time.
- **Exact coverage.** $R$ is the same product as in the exact composite, so the background term $C_0 R$ is exact.
- **A weighted mean.** $\tilde C - C_0 R = (1 - R) \sum_i \lambda_i (c_i / \alpha_i)$ with $\lambda_i = \alpha_i w_i / \sum_j \alpha_j w_j$, a convex combination of the unpremultiplied colors. The exact composite has the same form with $\lambda_i$ replaced by $\alpha_i T_i / (1 - R)$, because $\sum_i \alpha_i T_i = 1 - R$ by a telescoping sum.
- **Exact weights.** So if $w_i$ is proportional to $T_i$, the result is exact. The tests build this order-dependent weight and check equality.
- **Special cases.** With one fragment, or with all fragments of one unpremultiplied color, the result is exact for every positive weight.

How close the result is for a real weight function is a measurement on a scene, not a theorem.

## Complexity

The model is the real RAM. For a pixel with $k$ fragments, the method does $O(k)$ work and keeps $O(1)$ numbers: the color sums, the alpha sum and $R$, which is 5 numbers for RGB. For a frame with $f$ transparent fragments over $p$ pixels, the geometry pass costs $O(f)$ and the composite $O(p)$. At 1920 by 1080 pixels, an RGBA16F target and an R8 target take $2\,073\,600 \cdot 9 = 18\,662\,400$ bytes, about 17.8 MiB, whatever the depth complexity. There is no sort and no list, so the memory is known before the frame.

## Properties

- **One geometry pass, bounded memory.** No per-pixel storage grows with the number of fragments.
- **Order independent.** The result does not depend on the draw order, apart from floating-point rounding. Particles and other dynamic transparent geometry do not flicker when their order changes.
- **Exact coverage, approximate color.** The amount of background seen is right. The color is a weighted mean of the layers.
- **Weight is tuning.** The weight function depends on the depth range and the content of the scene.
- **Deterministic.** The same input gives the same output, except for rounding when the blend order changes on the GPU.
- **No refraction order.** Effects that need to know which surface is in front, such as refraction, are not supported by the average itself.

## Variants and improvements

- **Other weight functions.** The paper gives several functions of depth with different falloffs. The choice is a trade between near and far layers in the scene at hand.
- **Coverage only.** Without the color targets, the second target alone gives the exact transmittance of all transparent surfaces, for example for colored shadow maps.
- **Colored transmission.** Keep $R$ per color channel, so that colored glass tints the background differently in each channel. The product stays order independent.
- **Mixed methods.** Render the nearest few layers exactly, for example with a small fragment array or [depth peeling](/depth-peeling/), and the rest with weighted blending.
- **Moment-based and phenomenological methods.** Later methods approximate the transmittance $T(z)$ as a function of depth with a few moments per pixel and use it as the weight, at the cost of a second pass.

## When to use it

Use it for particles, smoke, foliage cards, glass panels and other transparent content where many layers overlap, the layers have similar colors, or speed matters more than an exact order. It fits a [deferred shading](/deferred-shading/) renderer as a forward pass after the opaque pass. Do not use it where a strongly colored surface in front must cover another strongly colored surface behind it, or where the exact image matters; then use [per-pixel linked lists](/per-pixel-linked-lists/) or [depth peeling](/depth-peeling/).

## Pitfalls

- **Overflow in 16-bit floats.** Large weights times many layers overflow half floats, whose largest value is 65504. Clamp the weight, or use a 32-bit target.
- **Wrong depth space.** The constants of a weight function refer to a depth in given units. A nonlinear depth buffer value or a scene in other units changes the falloff.
- **Opaque fragments.** A fragment with $\alpha = 1$ sets $R = 0$, but its color is still averaged with the others. Draw opaque surfaces in the opaque pass.
- **Premultiplied or not.** The accumulation must use premultiplied colors. Mixing the two forms gives colors that are too dark or too bright.
- **Division by zero.** A pixel with no transparent fragment has $A_\alpha = 0$. The guard $\varepsilon$ or a test on $R = 1$ avoids the division.
- **Expecting exact results.** Two strongly colored layers in the wrong ratio of weights give a visibly wrong mix, as the example shows.

## Implementations

## History

The over operator of Porter and Duff (1984) needs a back-to-front order, and exact methods for unsorted fragments, such as the A-buffer and depth peeling, need memory or passes that grow with the depth complexity. Earlier one-pass methods replaced the over operator by sums of colors that did not depend on order, but they did not keep the coverage exact or did not weight the layers by depth. McGuire and Bavoil (2013) combined a weighted average of the colors with the exact product of the transmissions, gave weight functions of depth, and mapped the method to two render targets with standard blend modes. McGuire published shader code and a revised weight in a blog post in 2014.

## References
