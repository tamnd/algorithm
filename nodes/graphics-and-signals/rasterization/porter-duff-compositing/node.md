---
tag: BSR165
kind: algorithm
slug: porter-duff-compositing
name: Porter-Duff compositing
aliases:
- Porter-Duff operators
- over operator
area: graphics-and-signals/rasterization
level: advanced
summary: Twelve operators such as over, in, out, atop and xor that combine two premultiplied RGBA images pixel by pixel, each as F_A times A plus F_B times B.
solves: [image-compositing]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H), average: Θ(W H), best: Θ(W H)}
  space: {extra: Θ(1)}
properties: {deterministic: true, in_place: false}
history:
  year: 1984
  people: [Thomas Porter, Tom Duff]
  note: Porter and Duff defined the algebra of twelve operators on premultiplied RGBA pictures at Lucasfilm and published it at SIGGRAPH 1984.
prereqs: [alpha-blending, pixel]
see_also: [image-compositing, alpha-blending, a-buffer, depth-peeling, gamma-correction, digital-image]
sources:
  - paper: doi:10.1145/964965.808606
    title: Thomas Porter and Tom Duff, Compositing digital images, Computer Graphics 18(3), SIGGRAPH 1984, pages 253 to 259
    locator: Section 3 (RGBA pictures, premultiplied storage) and Section 4 (the coverage assumptions in 4.1, the table of operators in 4.2, the unary operators in 4.4, plus in 4.5)
  - paper: doi:10.1109/38.310740
    title: James F. Blinn, Compositing, Part 1, Theory, IEEE Computer Graphics and Applications 14(5), 1994, pages 83 to 87
    locator: the derivation of over from subpixel coverage and the case for premultiplied colors
  - url: https://alvyray.com/Memos/MemosCG.htm
    title: Alvy Ray Smith, Alpha and the History of Digital Compositing, Microsoft Technical Memo 7, 1995
    locator: the sections on the integral alpha channel and on premultiplied alpha
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 5, the section on transparency, alpha and compositing
---

Porter-Duff compositing combines two images that carry a coverage value $\alpha$ at each [pixel](/pixel/) into one image, by one of twelve operators such as *over*, *in*, *out*, *atop* and *xor*. Thomas Porter and Tom Duff defined the operators in 1984. Each operator computes the result as $F_A \cdot A + F_B \cdot B$ on colors that are premultiplied by $\alpha$, where the two factors depend only on the two coverages. The operator *over* is associative on premultiplied colors, so a stack of layers can be combined in any grouping. This page gives the operator algebra; [alpha blending](/alpha-blending/) is the blend equation in a graphics pipeline, and [image compositing](/image-compositing/) is the problem of combining many layers.

## In plain words

Think of each pixel of a layer as a pane of glass that is partly painted. The coverage tells how much of the pane is painted. When you put one pane on another, each pixel splits into four parts: painted on neither pane, painted on the top pane only, painted on the bottom pane only, and painted on both. An operator is a rule that says which pane shows in each part. For example, *over* shows the top pane where it is painted, and the bottom pane elsewhere. *In* shows the top pane only where the bottom pane is also painted. The method does not know where the paint is inside the pixel, so it assumes that the two layers overlap as if the paint were spread at random. Then the size of each part is known, and the result is a weighted sum of the two colors.

## The problem

The input is two images $A$ and $B$ of $H$ rows and $W$ columns. Each pixel is a tuple $(r, g, b, \alpha)$ of reals in $[0, 1]$ with $r, g, b \le \alpha$. The color channels are *premultiplied*: the pixel stores the true color times the coverage, so $(0.5, 0, 0, 0.5)$ is full red that covers half the pixel. The values are linear light, not sRGB codes (see [gamma correction](/gamma-correction/)). A pixel is a point sample of the picture, not a little square; $\alpha$ is the fraction of the area near the sample that the layer covers, and the shape of that area inside the pixel is not stored. The output is an image $C$ of the same size. Each output pixel depends only on the two input pixels at the same place, so the pixel center convention and the border rule do not matter here.

## The algorithm

Write $\alpha_a$ and $\alpha_b$ for the coverages of the pixels $a$ and $b$. Porter and Duff assume that inside one pixel, $B$ divides each part of the pixel in the ratio $\alpha_b : 1 - \alpha_b$. Under this assumption the four parts have the areas

| part | area | possible contents |
|---|---|---|
| neither | $(1-\alpha_a)(1-\alpha_b)$ | nothing |
| $A$ only | $\alpha_a(1-\alpha_b)$ | nothing or $A$ |
| $B$ only | $(1-\alpha_a)\alpha_b$ | nothing or $B$ |
| both | $\alpha_a\alpha_b$ | nothing, $A$ or $B$ |

The choices give $2 \cdot 2 \cdot 3 = 12$ operators. The table lists the contents of the parts (neither, $A$ only, $B$ only, both) and the factors that follow from them.

| operator | parts | $F_A$ | $F_B$ |
|---|---|---|---|
| clear | (0, 0, 0, 0) | $0$ | $0$ |
| $A$ | (0, A, 0, A) | $1$ | $0$ |
| $B$ | (0, 0, B, B) | $0$ | $1$ |
| $A$ over $B$ | (0, A, B, A) | $1$ | $1-\alpha_a$ |
| $B$ over $A$ | (0, A, B, B) | $1-\alpha_b$ | $1$ |
| $A$ in $B$ | (0, 0, 0, A) | $\alpha_b$ | $0$ |
| $B$ in $A$ | (0, 0, 0, B) | $0$ | $\alpha_a$ |
| $A$ out $B$ | (0, A, 0, 0) | $1-\alpha_b$ | $0$ |
| $B$ out $A$ | (0, 0, B, 0) | $0$ | $1-\alpha_a$ |
| $A$ atop $B$ | (0, 0, B, A) | $\alpha_b$ | $1-\alpha_a$ |
| $B$ atop $A$ | (0, A, 0, B) | $1-\alpha_b$ | $\alpha_a$ |
| $A$ xor $B$ | (0, A, B, 0) | $1-\alpha_b$ | $1-\alpha_a$ |

```pseudo id=main
PORTER-DUFF(op, A, B)                ▷ A, B: H × W premultiplied RGBA images
L1  (F_A, F_B) ← the two factors of op in the table
L2  for each pixel position (i, j) do
L3      a ← A[i, j], b ← B[i, j]
L4      f_a ← F_A(α_a, α_b), f_b ← F_B(α_a, α_b)
L5      C[i, j] ← f_a · a + f_b · b    ▷ on all four channels, α included
L6  return C
```

Line L5 applies the same factors to the color channels and to $\alpha$. This works because the $\alpha$ channel of a premultiplied pixel is the premultiplied value of the constant color 1. The factor $F_A$ is $1$ when $A$ shows in both parts where $A$ is present, $1-\alpha_b$ when it shows only in the part "$A$ only", $\alpha_b$ when it shows only in the part "both", and $0$ otherwise. $F_B$ is the same with the roles of $A$ and $B$ exchanged.

Porter and Duff also define *plus* with $F_A = F_B = 1$, and three unary operators: *darken* scales the color channels by $\varphi$, *dissolve* scales all four channels by $\delta$, and *opaque* scales only $\alpha$ by $\omega$.

## Example

Let $a = (1/2, 0, 0, 1/2)$, full red at half coverage, and $b = (0, 0, 3/4, 3/4)$, full blue at three quarters coverage.

| operator | $F_A$ | $F_B$ | result $(r, g, b, \alpha)$ |
|---|---|---|---|
| $A$ over $B$ | $1$ | $1/2$ | $(1/2, 0, 3/8, 7/8)$ |
| $B$ over $A$ | $1/4$ | $1$ | $(1/8, 0, 3/4, 7/8)$ |
| $A$ in $B$ | $3/4$ | $0$ | $(3/8, 0, 0, 3/8)$ |
| $B$ in $A$ | $0$ | $1/2$ | $(0, 0, 3/8, 3/8)$ |
| $A$ out $B$ | $1/4$ | $0$ | $(1/8, 0, 0, 1/8)$ |
| $B$ out $A$ | $0$ | $1/2$ | $(0, 0, 3/8, 3/8)$ |
| $A$ atop $B$ | $3/4$ | $1/2$ | $(3/8, 0, 3/8, 3/4)$ |
| $B$ atop $A$ | $1/4$ | $1/2$ | $(1/8, 0, 3/8, 1/2)$ |
| $A$ xor $B$ | $1/4$ | $1/2$ | $(1/8, 0, 3/8, 1/2)$ |

Check $A$ over $B$ against the parts. Red shows in "$A$ only" and "both", of total area $1/2$, so the red channel is $1/2$. Blue shows in "$B$ only", of area $(1/2)(3/4) = 3/8$. The covered area is $1 - (1/2)(1/4) = 7/8$. The straight color of the result is $(1/2, 0, 3/8) / (7/8) = (4/7, 0, 3/7)$.

Add $c = (0, 1/4, 0, 1/4)$, green at quarter coverage. Then $(a$ over $b)$ over $c$ and $a$ over $(b$ over $c)$ both give $(1/2, 1/32, 3/8, 29/32)$.

## Correctness

Three facts make the method right. First, under the coverage assumption, line L5 gives the exact area-weighted sum of the parts: a part of area $s$ that shows a picture of straight color $x$ adds $s \cdot x$ to the color and $s$ to $\alpha$. Second, each result is again a valid premultiplied pixel, with $0 \le r, g, b \le \alpha \le 1$, so the operators can be chained. Third, *over* is associative, and the clear pixel $(0, 0, 0, 0)$ is its identity on both sides:

$$(a \text{ over } b) \text{ over } c = a + (1-\alpha_a)\, b + (1-\alpha_a)(1-\alpha_b)\, c = a \text{ over } (b \text{ over } c).$$

The key step is that the coverage of $a$ over $b$ is $\alpha_a + (1-\alpha_a)\alpha_b$, so its complement is the product $(1-\alpha_a)(1-\alpha_b)$. The paper states the table but does not prove associativity. The full proofs are below.

## Complexity

The loop of line L2 runs $WH$ times. Each pass evaluates two factors with at most one subtraction each, and does 8 multiplications and 4 additions on the 4 channels. So the time is $\Theta(WH)$ in every case, and the extra space is $\Theta(1)$ besides the output. For *over*, $F_A = 1$, so each pixel costs one subtraction and 4 multiply-adds. Combining a stack of $n$ layers with *over* takes $n - 1$ applications, $\Theta(nWH)$ time.

## Properties

- **Over is associative but not commutative.** In the example, $A$ over $B$ and $B$ over $A$ differ. Associativity lets a compositor merge the layers from the back, from the front, or as a balanced tree in parallel.
- **In is associative.** $(a$ in $b)$ in $c = \alpha_b \alpha_c \, a = a$ in $(b$ in $c)$.
- **Xor and plus are commutative.** Their factor pairs are symmetric in $A$ and $B$.
- **Opaque layers.** If $\alpha_a = 1$, then $A$ over $B$ is $A$ and $A$ in $B$ is $\alpha_b A$, a hard matte.
- **No straight-alpha form without division.** On straight colors, $A$ over $B$ needs $c = (\alpha_a c_a + (1-\alpha_a)\alpha_b c_b) / \alpha$. The common shortcut $c = \alpha_a c_a + (1-\alpha_a) c_b$ is not associative: with straight pixels $(1, 1/2)$, $(0, 1/2)$, $(1, 1/2)$ written as (color, $\alpha$), the two groupings give the colors $5/8$ and $3/4$.

## Variants and improvements

- **Under.** $B$ over $A$ written with the front layer first. It lets a renderer composite front to back and stop when $\alpha$ reaches 1 (see [image compositing](/image-compositing/)).
- **Plus.** Adds two images. It is used for cross dissolves, as $\text{dissolve}(A, t)$ plus $\text{dissolve}(B, 1-t)$, and for light that adds, such as glows.
- **Separable blend modes.** Formats such as PDF and SVG add modes such as multiply and screen, which change the color in the part "both" and keep the Porter-Duff weights of the other parts.
- **Correlated coverage.** The [A-buffer](/a-buffer/) keeps a subpixel mask with each fragment, so that two layers that share an edge get the true coverage instead of the uncorrelated estimate.
- **Order-independent transparency.** [Depth peeling](/depth-peeling/) sorts the layers per pixel on the GPU, then applies over in order.

## When to use it

Use Porter-Duff operators whenever you combine images that have a coverage channel: layers of a 2D drawing, rendered elements over a background plate, text over an image, or user interface layers. Use *over* for normal stacking, *in* and *out* for masks and holdouts, and *atop* to paint onto an existing shape only. If the layers share edges exactly, as adjacent shapes of one drawing do, the coverage assumption is wrong; use a subpixel mask or render the shapes together.

## Pitfalls

- **Mixing straight and premultiplied pixels.** Applying line L5 to straight colors darkens the edges of each layer, because the edge colors get multiplied by $\alpha$ twice. Convert once, at load time.
- **Conflation at shared edges.** Two layers of the same color that each cover a different half of a pixel should give $\alpha = 1$. Over gives $1/2 + (1/2)(1/2) = 3/4$, so a faint seam shows along the shared edge. With two layers on the same half, the true coverage is $1/2$ and over again gives $3/4$.
- **Compositing in sRGB.** The weights are fractions of area, so they apply to linear light. Blending sRGB codes makes the edges too dark.
- **Precision of premultiplied integers.** With 8-bit channels, a pixel of small $\alpha$ keeps few distinct colors. Unpremultiplying it and multiplying again changes the color.
- **Unpremultiply at zero coverage.** A pixel with $\alpha = 0$ has no color. Code that divides by $\alpha$ must test for zero.
- **Plus overflow.** Plus can give values above 1. Clamp the result, or keep the sum in a wider type.

## Implementations

## History

Smith dates the integral alpha channel, a fourth channel stored with each pixel, to work by Ed Catmull and himself at the New York Institute of Technology in the 1970s. Porter and Duff, at Lucasfilm, stored the colors premultiplied by $\alpha$, made the coverage assumption explicit, and derived the full set of operators in their 1984 SIGGRAPH paper. Blinn later wrote the derivation from subpixel coverage in a tutorial form.

## References
