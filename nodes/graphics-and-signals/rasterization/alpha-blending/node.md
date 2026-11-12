---
tag: KZBFDF
kind: concept
slug: alpha-blending
name: Alpha blending
area: graphics-and-signals/rasterization
level: intro
summary: Combining source and destination colors weighted by an opacity or coverage value.
prereqs: [pixel, frame-buffer]
see_also: [porter-duff-compositing, image-compositing, graphics-pipeline, depth-peeling, painters-algorithm, a-buffer, gamma-correction, wu-line-algorithm]
sources:
  - paper: doi:10.1145/964965.808606
    title: Thomas Porter and Tom Duff, Compositing digital images, Computer Graphics 18(3), SIGGRAPH 1984, pages 253 to 259
    locator: Section 2 (the alpha channel), Section 3 (RGBA pictures and premultiplied storage) and the over operator in Section 4.2
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 5, the section on transparency, alpha and compositing (blending order, premultiplied alpha and order-independent transparency)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, 1990
    locator: Chapter 17, the section on image compositing
  - paper: doi:10.1109/38.310740
    title: James F. Blinn, Compositing, Part 1, Theory, IEEE Computer Graphics and Applications 14(5), 1994, pages 83 to 87
    locator: the two meanings of alpha (coverage and opacity) and the premultiplied form
---

Alpha blending is the step of the [graphics pipeline](/graphics-pipeline/) that combines the color of a new fragment, the *source*, with the color already in the [frame buffer](/frame-buffer/), the *destination*, weighted by the source's alpha value. The usual form is $C = \alpha_s C_s + (1 - \alpha_s) C_d$, where $\alpha_s \in [0, 1]$ is an opacity or a coverage. It is the *over* operator of [Porter-Duff compositing](/porter-duff-compositing/), applied one fragment at a time. The result depends on the order of the fragments, and it is correct only on linear color values.

## In plain words

Each new color that a program draws comes with a number between zero and one, its alpha. Zero means "do not change what is there". One means "replace what is there". A value in between mixes the new color with the old color: a half means half of each. Alpha can mean two things. It can say how much of the pixel a shape covers, as at the soft edge of a letter. It can also say how much light a thin material blocks, as with tinted glass. For one layer over an opaque background both meanings use the same mix. With several transparent layers, the order matters: a red glass in front of a blue glass does not look the same as the blue glass in front of the red one. So programs draw transparent objects from the back to the front.

## The idea

**The blend equation.** A fragment has color $C_s$ and alpha $\alpha_s$. The frame buffer holds $C_d$ and possibly $\alpha_d$. Fixed-function blending hardware computes, on each channel,

$$C \leftarrow F_s\, C_s + F_d\, C_d,$$

where the program picks the factors $F_s$ and $F_d$ from a small list (zero, one, $\alpha_s$, $1-\alpha_s$, $\alpha_d$, $1 - \alpha_d$, and others), and can often pick separate factors for the alpha channel. Standard transparency uses $F_s = \alpha_s$ and $F_d = 1 - \alpha_s$. Additive blending, used for fire and glow, uses $F_s = F_d = 1$.

**Straight and premultiplied color.** A *straight* color stores the true color $c$ and the alpha separately. A *premultiplied* color stores $(\alpha c, \alpha)$. Over a destination with alpha $\alpha_d$, the exact result of a source over the destination is

$$\alpha = \alpha_s + (1-\alpha_s)\,\alpha_d, \qquad \alpha c = \alpha_s c_s + (1-\alpha_s)\,\alpha_d c_d.$$

In premultiplied form both lines are the same formula, $p \leftarrow p_s + (1 - \alpha_s)\, p_d$, on all four channels, with the factors $F_s = 1$ and $F_d = 1 - \alpha_s$. In straight form the color needs a division by $\alpha$. The usual straight setting $C = \alpha_s c_s + (1-\alpha_s) c_d$ is the special case $\alpha_d = 1$: it is right when the destination is opaque, and wrong when the result is later composited again. Porter and Duff argue for premultiplied storage, and Blinn derives the same formula from the area that each layer covers.

**Order dependence.** The operator over is associative but not commutative, so a stack of transparent surfaces must be blended in depth order. A [z-buffer](/z-buffer/) keeps only the nearest surface per pixel and does not sort the others. Renderers sort transparent objects back to front, as in the [painter's algorithm](/painters-algorithm/), or use an order-independent method such as [depth peeling](/depth-peeling/) or the [A-buffer](/a-buffer/). Additive blending is commutative, so it does not need the sort.

**Linear values.** The weights are fractions of area or of light, so the blend must act on linear light values. Values stored as sRGB codes (see [gamma correction](/gamma-correction/)) must be decoded before the blend and encoded after it. GPUs can do this in the sRGB render target formats.

**Coverage and opacity.** When alpha is a coverage, the method treats the layers as uncorrelated inside the pixel. This is the coverage assumption of Porter and Duff. It fails when two shapes share an edge, and the result is a faint seam. Antialiased line drawing, such as the [Wu line algorithm](/wu-line-algorithm/), writes its coverage values through this same blend.

## Examples

**One layer over a background.** Red $c_s = (1, 0, 0)$ with $\alpha_s = 1/2$ over an opaque green $c_d = (0, 1, 0)$ gives $(1/2, 1/2, 0)$ in linear values.

**Order.** Over an opaque black background, draw red and blue, each with $\alpha = 1/2$. If red is drawn first and blue second, the result is $(1/4, 0, 1/2)$. In the other order the result is $(1/2, 0, 1/4)$. The last layer drawn has the larger weight.

**Linear against sRGB.** A half-covered edge between white and black has the linear value $1/2$, which is the 8-bit sRGB code 188. Blending the codes 255 and 0 gives the code 128, which decodes to the linear value $0.216$. The edge then shows about 22% of the light instead of 50%, and edges look too dark and too thin.

**Straight blending into a transparent target.** Clear a render target to $(0, 0, 0, 0)$ and blend red with $\alpha_s = 1/2$ with the factors $\alpha_s$ and $1 - \alpha_s$ on all four channels. The color becomes $(1/2, 0, 0)$ and the alpha becomes $\alpha_s \cdot \alpha_s = 1/4$, though the true coverage is $1/2$. With premultiplied colors and the factors $1$ and $1 - \alpha_s$, the target becomes $(1/2, 0, 0, 1/2)$, which is right and can be composited again.

**A non-example.** A [z-buffer](/z-buffer/) depth test with blending turned off is not alpha blending: the nearest fragment replaces the color, whatever its alpha.

## Where it is used

- Transparent surfaces in real-time rendering: glass, water, smoke and particles, drawn after the opaque scene.
- Text and vector graphics, where antialiased edges carry a coverage value.
- User interfaces and window systems, which stack many partly transparent layers.
- Decals and overlays drawn onto a finished image.
- Film and video compositing, where whole images are combined. That is the problem of [image compositing](/image-compositing/), and its operator set is [Porter-Duff compositing](/porter-duff-compositing/).

## References
