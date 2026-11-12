---
tag: A93SQT
kind: problem
slug: image-compositing
name: Image compositing
aliases:
- layer compositing
- alpha compositing problem
area: graphics-and-signals/rasterization
level: intro
summary: Combine partially transparent image layers into one output image.
prereqs: [alpha-blending, digital-image]
see_also: [porter-duff-compositing, alpha-blending, depth-peeling, a-buffer, painters-algorithm, parallel-reduction, monoid, ray-marching]
sources:
  - paper: doi:10.1145/964965.808606
    title: Thomas Porter and Tom Duff, Compositing digital images, Computer Graphics 18(3), SIGGRAPH 1984, pages 253 to 259
    locator: Section 4 (the operators and the compositing arithmetic) and Section 5 (examples of compositing expressions)
  - paper: doi:10.1109/38.329100
    title: James F. Blinn, Compositing, Part 2, Practice, IEEE Computer Graphics and Applications 14(6), 1994, pages 78 to 82
    locator: the under operator and the front-to-back order
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 5, the section on transparency, alpha and compositing (blending order and order-independent transparency)
  - url: https://jcgt.org/published/0002/02/09/
    title: Morgan McGuire and Louis Bavoil, Weighted Blended Order-Independent Transparency, Journal of Computer Graphics Techniques 2(2), 2013, pages 122 to 141
    locator: the weighted average blend and its error for layers of similar depth
---

Image compositing is the problem of combining a stack of partly transparent image layers, each with a coverage or opacity value $\alpha$ at each [pixel](/pixel/), into one image. The standard answer puts each layer *over* the ones behind it, with the operator of [Porter-Duff compositing](/porter-duff-compositing/) on premultiplied colors. Because over is associative, the layers can be combined from the back, from the front, or as a tree, and all orders of evaluation give the same image. The hard case is a set of transparent fragments that arrive in no particular depth order, as in real-time rendering.

## In plain words

A film shot, a web page or a game screen is often built from layers: a background, a character, smoke, text. Each layer has some pixels that are solid, some that are clear, and some that are partly clear, as at soft edges. The task is to make the final picture that a viewer sees through all the layers. The rule for two layers is fixed: the front layer covers part of the back layer, and the rest of the back layer shows through. For many layers, you can start at the back and paint each layer on top, or start at the front and add each layer behind. Both give the same picture. Starting at the front lets you stop early at a pixel once it is solid. When the layers come in a random order, you must first find their front-to-back order at each pixel.

## Definition

**Model.** An image is a $W \times H$ grid of point samples. Each sample is a premultiplied tuple $p = (r, g, b, \alpha)$ of linear values in $[0, 1]$ with $r, g, b \le \alpha$. Each output pixel depends only on the input pixels at the same position, so no border rule is needed. Costs count operations on channel values in the [real RAM](/real-ram/).

**Input (a layer stack).** Layers $L_1, \ldots, L_n$, from front ($L_1$) to back ($L_n$), each a $W \times H$ image.

**Output.** The image

$$C = L_1 \text{ over } L_2 \text{ over } \cdots \text{ over } L_n, \qquad p \text{ over } q = p + (1 - \alpha_p)\, q,$$

computed per pixel. By associativity the expression needs no brackets. The [alpha blending](/alpha-blending/) page explains the blend formula and the premultiplied form.

**Input (unsorted fragments).** At each pixel, a list of $k$ fragments, each with a premultiplied color and a depth, in arbitrary order. The output at the pixel is the over of the fragments in order of increasing depth. This is the *order-independent transparency* problem.

## Variants

- **Layer stack.** The order is given. This is the case of film, user interface and 2D drawing compositors.
- **Compositing expressions.** Porter and Duff combine layers by a tree of operators (over, in, out, atop, xor, plus) and unary operators such as dissolve. Mattes and holdouts are written this way.
- **Order-independent transparency.** The order must be found per pixel from fragment depths.
- **Approximate order-independent transparency.** Accept an error in exchange for a fixed amount of memory and one pass.
- **Front-to-back accumulation along a ray.** Volume rendering and [ray marching](/ray-marching/) composite samples along each ray with the same rule, front to back.

## Examples

Take one pixel with three layers, front to back: $L_1 = (0, 0, 1/4, 1/4)$ (blue, quarter coverage), $L_2 = (1/2, 0, 0, 1/2)$ (red, half coverage) and $L_3 = (1, 1, 1, 1)$ (opaque white).

**Back to front.** $L_2$ over $L_3$ $= (1/2, 0, 0, 1/2) + (1/2)(1, 1, 1, 1) = (1, 1/2, 1/2, 1)$. Then $L_1$ over that $= (0, 0, 1/4, 1/4) + (3/4)(1, 1/2, 1/2, 1) = (3/4, 3/8, 5/8, 1)$.

**Front to back.** Keep the sum $S$ and the transmittance $T = 1 - \alpha_S$. Start with $S = 0$, $T = 1$. Each layer does $S \leftarrow S + T \cdot L_i$ and $T \leftarrow T (1 - \alpha_i)$.

| step | layer | $S$ (color) | $T$ |
|---|---|---|---|
| start | | $(0, 0, 0)$ | $1$ |
| 1 | $L_1$ | $(0, 0, 1/4)$ | $3/4$ |
| 2 | $L_2$ | $(3/8, 0, 1/4)$ | $3/8$ |
| 3 | $L_3$ | $(3/4, 3/8, 5/8)$ | $0$ |

The result is the same. After step 3, $T = 0$, so any layer behind $L_3$ cannot change the pixel.

**Wrong order.** Composite the same three layers in the order $L_2$ over $L_1$ over $L_3$. Then $L_1$ over $L_3 = (3/4, 3/4, 1, 1)$, and $L_2$ over that is $(1/2 + 3/8, 3/8, 1/2, 1) = (7/8, 3/8, 1/2, 1)$. This differs from $(3/4, 3/8, 5/8, 1)$, because over is not commutative.

## Known algorithms

- **Back-to-front over.** Start with the back layer and put each layer over the result. This is the method of the [painter's algorithm](/painters-algorithm/) and of GPU [alpha blending](/alpha-blending/) with sorted objects. It needs one accumulator per pixel.
- **Front-to-back under.** Blinn's *under* operator, $S \leftarrow S + (1 - \alpha_S) L_i$, adds each layer behind the result. A pixel can stop when $\alpha_S$ reaches 1, or a threshold close to 1.
- **Tree reduction.** Associativity allows a balanced tree of over operations, as a [parallel reduction](/parallel-reduction/) over the [monoid](/monoid/) of premultiplied pixels with over and the clear pixel. Sort-last parallel renderers combine the images of several processors this way.
- **Porter-Duff expressions.** Evaluate a tree of [Porter-Duff operators](/porter-duff-compositing/) bottom up.
- **Depth peeling.** [Depth peeling](/depth-peeling/) renders the scene once per layer, each time keeping the nearest fragment behind the previous layer, and composites the layers in order.
- **A-buffer.** The [A-buffer](/a-buffer/) keeps a list of fragments per pixel, with coverage masks, sorts each list and resolves it. It also fixes the coverage assumption at shared edges.
- **Weighted blended transparency.** McGuire and Bavoil replace the ordered over by a weighted average with depth-based weights. It needs one pass and fixed memory. The result is not exact, and the error grows when layers of high $\alpha$ have similar depths.

## Bounds

- **Layer stack.** With $n$ layers, back-to-front compositing does $n - 1$ over operations per pixel, $\Theta(nWH)$ time in total, with $\Theta(WH)$ extra space. This is optimal in the worst case: if every layer has $\alpha < 1$ at a pixel, each layer's value at that pixel changes the result, so an algorithm must read all $nWH$ input pixels.
- **Early termination.** Front to back, a pixel costs $O(m)$ where $m$ is the number of layers up to and including the first with $\alpha = 1$. The worst case is still $\Theta(n)$ per pixel.
- **Parallel depth.** A balanced tree of over operations has depth $\lceil \log_2 n \rceil$ and does $n - 1$ operations per pixel.
- **Unsorted fragments.** With $k$ fragments at a pixel, sorting by depth in the [comparison model](/comparison-model/) takes $\Theta(k \log k)$ comparisons in the worst case (the [sorting problem](/sorting-problem/)), and the compositing then takes $\Theta(k)$. Depth peeling with $n$ passes rasterizes the scene $n$ times.

## Reductions

- Order-independent transparency reduces to a sort per pixel followed by a layer stack. Conversely, a layer stack is the special case in which the depths are the layer numbers.
- Compositing a stack over all prefixes, for example to show each partial result, is an [all-prefix-sums](/all-prefix-sums/) scan with over as the associative operator.
- Front-to-back and back-to-front evaluation are the two ways to bracket the same associative product, so they give the same result in exact arithmetic. In floating point they can differ in the last bits.

## Applications

- Visual effects for film, where rendered elements, live action plates and mattes are combined by compositing expressions.
- Window systems and user interfaces, which composite the windows and layers of the screen in each frame.
- Transparent objects in real-time rendering: glass, foliage cards, smoke and particles.
- Volume rendering and participating media, which accumulate samples along each ray front to back.
- Sort-last parallel rendering, where each processor renders part of the scene and the partial images are composited.

## References
