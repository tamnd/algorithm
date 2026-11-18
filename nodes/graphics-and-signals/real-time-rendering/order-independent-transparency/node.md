---
tag: YW69ZC
kind: problem
slug: order-independent-transparency
name: Order-independent transparency
aliases:
- OIT
area: graphics-and-signals/real-time-rendering
level: core
summary: Composite the transparent fragments of each pixel as if they were blended in depth order with the over operator, when the rasterizer delivers them in an arbitrary order.
prereqs: [alpha-blending, porter-duff-compositing]
see_also: [depth-peeling, a-buffer, per-pixel-linked-lists, weighted-blended-oit, painters-algorithm, z-buffer, deferred-shading, sorting-network]
sources:
  - paper: doi:10.1145/800031.808606
    title: "Thomas Porter and Tom Duff, Compositing digital images, SIGGRAPH 1984, Computer Graphics 18(3), 253-259"
    locator: the premultiplied alpha and the over operator
  - url: http://jcgt.org/published/0002/02/09/
    title: "Morgan McGuire and Louis Bavoil, Weighted blended order-independent transparency, Journal of Computer Graphics Techniques 2(2), 122-141, 2013"
    locator: the statement of the problem, the review of exact and approximate methods, and the weighted average with exact coverage
  - paper: "Jason C. Yang, Justin Hensley, Holger Grün and Nicolas Thibieroz, Real-time concurrent linked list construction on the GPU, Computer Graphics Forum 29(4) (EGSR 2010), 1297-1304"
    locator: the exact method with a list of fragments per pixel and a sort in a resolve pass
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 5.5, Transparency, Alpha, and Compositing (the over operator and the order-independent methods)
---

Order-independent transparency is the problem of drawing transparent surfaces without sorting them first. A GPU rasterizes triangles in the order in which they are submitted, and [alpha blending](/alpha-blending/) with the over operator of [Porter and Duff](/porter-duff-compositing/) gives the right result only when the transparent fragments of each pixel arrive from back to front. Sorting whole objects does not fix this, because objects can intersect and overlap in cycles. The problem asks for the composite in depth order of the fragments of each pixel, in a form that works for any arrival order. This page defines the problem and the cost measures. The methods are on their own pages: exact ones such as [depth peeling](/depth-peeling/), the [A-buffer](/a-buffer/) and [per-pixel linked lists](/per-pixel-linked-lists/), and approximate ones such as [weighted blended OIT](/weighted-blended-oit/).

## In plain words

Look at a blue window through a red one. The red glass is in front, so the result is mostly red with some blue. Swap the two and the result is mostly blue. Blending one color over another depends on which comes first, but the graphics hardware draws surfaces in whatever order the program sends them, not in the order of their distance. Sorting the objects first helps only partly, because two objects can cross each other, and then neither is wholly in front. The task is to get the result of a correct back-to-front blend at every pixel, no matter in which order the surfaces arrive.

## Definition

**Input.** For each pixel, an opaque background color $C_0$ and a multiset of $k$ fragments $(c_i, \alpha_i, z_i)$, where $c_i$ is a premultiplied color (the color times the opacity), $\alpha_i \in [0, 1]$ is the opacity and $z_i$ is the view depth. The fragments arrive in an arbitrary order, which the method cannot choose. Colors are linear RGB.

**Output.** The composite in depth order. With the fragments renamed so that $z_1 < z_2 < \dots < z_k$ (front to back),

$$C = \sum_{i=1}^{k} c_i \prod_{j < i} (1 - \alpha_j) + C_0 \prod_{i=1}^{k} (1 - \alpha_i).$$

This is $c_1 \text{ over } (c_2 \text{ over } (\dots (c_k \text{ over } C_0)))$, with $A \text{ over } B = A + (1 - \alpha_A) B$ in premultiplied form. The factor $\prod_i (1 - \alpha_i)$ is the transmittance of the stack, and $1 - \prod_i (1 - \alpha_i)$ is its coverage.

**Cost model.** $p$ pixels, $k$ fragments per pixel (with $K$ the largest $k$), and $n$ triangles. The measures that matter on a GPU are the number of geometry passes, the memory per pixel, whether the memory is bounded in advance, and the cost of the per-pixel sort. Fragments of one pixel can arrive at the same time from different threads, so a method that keeps state per pixel needs atomic operations or ordered writes.

**Ties.** Fragments with equal depth have no defined order. The composite of two such fragments depends on which goes first, so methods differ on ties.

## Variants

- **Exact.** The output must equal $C$ for every input, given enough memory or passes.
- **Approximate with bounded memory.** A fixed number of bytes per pixel, one geometry pass, and an output close to $C$ in some sense. Different methods are exact on different special cases.
- **Coverage only.** Compute only the transmittance $\prod_i (1 - \alpha_i)$, for example for shadows of transparent objects. This part is order independent by itself.
- **With MSAA.** Fragments carry a coverage mask of samples, as in the A-buffer.
- **Per object order.** The program sorts objects or triangles back to front, and the hardware blends in submission order. This is the [painter's algorithm](/painters-algorithm/) for transparency. It is exact only when no two transparent objects overlap in depth inside a pixel in a way that the sort gets wrong.

## Examples

**Order matters.** A red fragment $c = (0.5, 0, 0)$, $\alpha = 0.5$ and a blue fragment $c = (0, 0, 0.5)$, $\alpha = 0.5$ lie over a black background. With red in front, $C = (0.5, 0, 0) + 0.5 \cdot (0, 0, 0.5) = (0.5, 0, 0.25)$. With blue in front, $C = (0.25, 0, 0.5)$. The coverage is $1 - 0.5 \cdot 0.5 = 0.75$ in both cases.

**Same color.** Three fragments of the same color $(1, 1, 1)$ with $\alpha = 0.2, 0.5, 0.25$ over black: the premultiplied colors are $0.2, 0.5, 0.25$ times white. Front to back in this order, $C = 0.2 + 0.8 \cdot 0.5 + 0.8 \cdot 0.5 \cdot 0.25 = 0.7$ times white. Any other order also gives $0.7$, which is $1 - 0.8 \cdot 0.5 \cdot 0.75$. When all fragments share one color, the composite depends only on the coverage.

**Opaque fragments.** If all $\alpha_i = 1$, then $C = c_1$, the color of the nearest fragment. The problem then becomes the per-pixel visibility of a [z-buffer](/z-buffer/).

## Known algorithms

| method | exact | passes | memory per pixel | notes |
|---|---|---|---|---|
| sorted objects (painter's) | no, fails on overlaps | 1 | 0 extra | CPU sort per frame |
| [depth peeling](/depth-peeling/) | yes, with $K$ passes | $K$ | $O(1)$ | one layer per geometry pass |
| [A-buffer](/a-buffer/) | yes | 1 | $O(k)$, unbounded | list per pixel with coverage masks |
| [per-pixel linked lists](/per-pixel-linked-lists/) | yes if the pool is large enough | 1 plus a resolve | $O(k)$ from a shared pool | atomic counter, head pointers, sort in the resolve |
| k-buffer | only for $k \le$ its size | 1 | $O(s)$ for $s$ slots | keeps the nearest $s$ fragments, merges the rest |
| [weighted blended OIT](/weighted-blended-oit/) | coverage exact, color only in special cases | 1 | $O(1)$ | weighted average of colors, weight is tuning |
| moment-based and adaptive methods | no | 1 or 2 | $O(1)$ | approximate the transmittance as a function of depth |

The exact methods sort the fragments of each pixel, or visit them in depth order one pass at a time. The approximate methods replace the order by a function of depth that they can accumulate with commutative operations, such as sums and products.

## Bounds

- **Per-pixel sorting.** An exact method that collects the $k$ fragments of a pixel and sorts them by comparisons needs $\Omega(k \log k)$ comparisons in the worst case, by the [comparison sort lower bound](/comparison-sort-lower-bound/). The resolve passes often use [insertion sort](/insertion-sort/), $O(k^2)$, because $k$ is small and the code is short, or [sorting networks](/sorting-network/) for a fixed $K$.
- **Passes.** Depth peeling needs $K$ geometry passes to peel $K$ layers, so its cost is $O(K n)$ triangle work. Dual depth peeling peels from both ends and needs about $K / 2$.
- **Memory.** A one-pass exact method must keep information about every fragment of a pixel until the last one arrives, because a late fragment can land between any two earlier ones. Lists use $O(k)$ memory per pixel and a total of $O(\sum k)$, which is not known before the frame.
- **Bounded memory.** No known one-pass method with a fixed number of bytes per pixel is exact on all inputs. This page does not prove a lower bound for that case.

## Reductions

- **Exact OIT reduces to per-pixel sorting.** Sort the fragments of each pixel by depth, then fold the over operator from back to front. Every exact method in the table is a way to get the fragments in order.
- **Opaque input is the z-buffer problem.** With all $\alpha_i = 1$ the output is the nearest fragment, so an OIT method also solves visibility.
- **Coverage is order free.** The transmittance $\prod_i (1 - \alpha_i)$ is a product, so any blend that multiplies by $1 - \alpha$ computes it exactly in any order. Methods that accumulate commutative sums can thus be exact in coverage and approximate only in color.
- **One color.** If all fragments have the same unpremultiplied color, the output is that color times the coverage plus $C_0$ times the transmittance, which needs no order.

## Applications

Transparent surfaces in real-time rendering: glass, water surfaces, foliage with soft alpha, hair, particles and smoke, and volumetric effects drawn as many layers. A renderer with [deferred shading](/deferred-shading/) draws these surfaces in a forward pass after the opaque pass, so the OIT method also decides how they are lit. Scientific visualization uses exact OIT for volume and isosurface rendering, where many layers overlap and errors in order are easy to see.

## References
