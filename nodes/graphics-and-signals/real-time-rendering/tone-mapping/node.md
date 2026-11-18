---
tag: RB0E9H
kind: problem
slug: tone-mapping
name: Tone mapping
aliases:
- tone reproduction
- tone reproduction problem
area: graphics-and-signals/real-time-rendering
level: core
summary: "Map the high dynamic range luminances of a rendered or captured image to the small range of a display, with a global curve or a local operator, while keeping contrast and detail visible."
prereqs: [color-spaces, gamma-correction]
see_also: [reinhard-tone-mapping, histogram-equalization, contrast-stretching, bilateral-filter, laplacian-pyramid, clahe, image-histogram, physically-based-shading]
sources:
  - paper: doi:10.1109/38.252554
    title: Jack Tumblin and Holly Rushmeier, Tone reproduction for realistic images, IEEE Computer Graphics and Applications 13(6), 1993, 42 to 48
    locator: the statement of tone reproduction as a map from scene values to display values that matches the brightness a viewer sees (general locator)
  - paper: doi:10.1145/566654.566575
    title: Erik Reinhard, Michael Stark, Peter Shirley and James Ferwerda, Photographic tone reproduction for digital images, ACM Transactions on Graphics 21(3) (SIGGRAPH 2002), 267 to 276
    locator: the global operator with the key value and the local dodging and burning operator
  - paper: doi:10.1145/566570.566574
    title: Frédo Durand and Julie Dorsey, Fast bilateral filtering for the display of high-dynamic-range images, SIGGRAPH 2002, 257 to 266
    locator: the local operator that splits the log luminance into a base layer, from a bilateral filter, and a detail layer, and compresses only the base
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 8, Light and Color (the part on scene to screen and tone mapping)
  - book: "Erik Reinhard, Greg Ward, Sumanta Pattanaik and Paul Debevec, High Dynamic Range Imaging, Acquisition, Display, and Image-Based Lighting, Morgan Kaufmann, 2005"
    locator: the chapters on tone reproduction, global and local operators (general locator)
  - paper: "John Hable, Uncharted 2, HDR Lighting, talk at the Game Developers Conference, 2010"
    locator: a filmic tone curve with a toe and a shoulder, fitted for a game (general locator)
---

Tone mapping is the problem of turning an image with a high dynamic range, such as a rendered frame in linear radiance or a merged set of photographs, into values that a display with a small range can show. Light in a scene can span many orders of magnitude between deep shadow and a bright sky, while a display shows a fixed and much smaller range. A plain scale and clip either crushes the shadows to black or burns the highlights to white. A tone operator is a function from the input luminances to display luminances that keeps as much of the visible structure as it can. Tone mapping is a separate step from the display encoding that [gamma correction](/gamma-correction/) does: tone mapping decides which linear value each pixel should get, and the encoding then stores that linear value for the display.

## In plain words

A real scene can have a lamp that is a million times brighter than the darkest corner. A screen can show only a small part of that range. If you set the brightness so that the corner is visible, the lamp and everything near it become pure white. If you set it for the lamp, the corner becomes pure black.

Tone mapping is the step that squeezes the large range into the small one in a good way. The simplest methods use one fixed curve for every pixel: dark values stay nearly as they are and bright values are pressed together more and more. Better but slower methods look at the neighborhood of each pixel, so that a detail in a bright area and a detail in a dark area can both stay visible. There is no single correct answer. The goal depends on what the image is for.

## Definition

**Input.** An image of $p$ pixels with world luminances $L_w(i) \ge 0$ in linear units, often with linear RGB colors. The dynamic range of the image is the ratio of its largest to its smallest nonzero luminance, often given in stops, $\log_2$ of the ratio.

**Output.** Display values $L_d(i) \in [0, 1]$, linear and relative to the white of the display, one per pixel. An encoding step turns them into code values afterwards.

**Operator classes.**
- A **global** operator is $L_d(i) = g(L_w(i))$ for one curve $g$, which can depend on statistics of the whole image (for example its log average or its histogram) but not on the position of the pixel.
- A **local** operator lets $L_d(i)$ depend on the neighborhood of pixel $i$, for example through a blurred luminance or a pyramid.

**The goal.** The problem has no single objective function. Each method states its own aim, and the aim decides the method. Common aims are to keep the order of brightness, to keep details visible in both the dark and the bright parts, to match the brightness or the contrast that a viewer of the real scene would see (Tumblin and Rushmeier), or to look like a photographic print or a film. Matching what a viewer sees is a goal stated with a model of human vision; whether a method reaches it is a measurement in a user study, not a proof.

**Cost model.** The real RAM, per pixel. A global operator reads each pixel a fixed number of times. A local operator reads a neighborhood of $k$ pixels, or a set of $r$ blurred images, per pixel.

## Variants

- **Global and local.** Global operators are fast and keep the order of brightness, but they lower contrast in the range they compress. Local operators can keep local contrast, but they can give halos or dark rings around bright edges.
- **Fixed curve and image adaptive.** A fixed curve with a manual exposure is common in games. An adaptive operator computes the exposure, or the whole curve, from the image.
- **Still images and video.** For video and real time, the exposure must change slowly over frames, or the image flickers. The speed of this adaptation is tuning.
- **Display target.** The target can be a standard display or a high dynamic range display with a larger range; the second needs less compression but still needs a curve.
- **Inverse tone mapping.** The opposite problem expands a standard range image for a high dynamic range display.

## Examples

Five pixels have $L_w = 0.01, 0.1, 1, 10, 100$, four orders of magnitude, or $13.3$ stops. Each row maps them to $[0, 1]$ and then encodes them with the sRGB curve to 8 bit code values.

| operator | 0.01 | 0.1 | 1 | 10 | 100 |
|---|---|---|---|---|---|
| divide by the largest value | 0 | 3 | 25 | 89 | 255 |
| exposure 1, then clip at 1 | 25 | 89 | 255 | 255 | 255 |
| key 0.18, then $L / (1 + L)$ | 6 | 36 | 109 | 210 | 249 |

The first row keeps the highlight but crushes the two darkest pixels into the code values 0 and 3. The second keeps the shadows but makes three pixels the same white. The third is the global [Reinhard operator](/reinhard-tone-mapping/): here the log average is 1, so the exposure maps $L_w$ to $L = 0.18 L_w$, and the curve gives the linear values $0.0018, 0.0177, 0.1525, 0.6429, 0.9474$. All five pixels stay distinct and in order. If the linear values of the third row go to 8 bits without the sRGB encoding, the codes are $0, 5, 39, 164, 242$, and the two dark pixels are again nearly black: the encoding is a separate step, and it must not be left out.

A local example: a dark detail inside a bright window and a bright detail inside a dark room both need contrast. A single increasing curve gives each luminance one output, so where the two areas overlap in luminance, it cannot raise the contrast in both. A local operator can, because it compresses each pixel relative to its neighborhood.

## Known algorithms

- **Linear scale and clip.** One exposure factor, then a clip at 1. $\Theta(p)$. The base line; see also [contrast stretching](/contrast-stretching/).
- **[Reinhard tone mapping](/reinhard-tone-mapping/).** Exposure from the log average and a key, then $L / (1 + L)$ or a form with a white point. An optional local step selects a blur size per pixel. Global $\Theta(p)$.
- **Tumblin and Rushmeier.** A global operator that maps the brightness that a viewer would see in the scene to the same brightness on the display, from a model of brightness perception.
- **Histogram based operators.** Build a curve from the histogram of the log luminance, related to [histogram equalization](/histogram-equalization/) with a limit on the slope, as in [CLAHE](/clahe/) for local contrast. $\Theta(p + b)$ for $b$ bins.
- **Durand and Dorsey.** Split the log luminance into a base layer, by a [bilateral filter](/bilateral-filter/), and a detail layer; compress only the base and add the detail back. This avoids most halos of plain blurs.
- **Pyramid and gradient methods.** Compress the bands of a [Laplacian pyramid](/laplacian-pyramid/), or the gradients of the log luminance and then solve for the image.
- **Filmic curves.** Fitted curves with a toe and a shoulder, such as the curve of Hable (2010) and fits of the ACES reference curve. They are the common choice in games. Their shapes and constants are tuning, chosen for the look of film, not derived from a model of vision.

## Bounds

Every operator must read each input pixel and write each output pixel, so $\Omega(p)$ time is needed, and a global operator with a curve from a constant number of image statistics reaches $\Theta(p)$. A histogram curve costs $\Theta(p + b)$ for $b$ bins. A local operator with a direct filter of $k$ taps per pixel costs $\Theta(p k)$. With a separable or recursive filter, or a pyramid, it costs $O(p)$ per scale, so $O(p r)$ for $r$ scales.

A proved limit of global operators: a global operator that keeps the order of brightness is an increasing function $g$. Where the image has a range of luminances that $g$ compresses, the slope of $g$ is below 1 on average over that range, so the contrast between nearby luminances in the range must drop. Only a local operator can keep contrast in two areas whose luminance ranges overlap, as the second example shows.

## Reductions

- **To display encoding.** The output of tone mapping is linear. The display encoding, for example the sRGB curve of [gamma correction](/gamma-correction/), is applied after it. The two steps do different jobs and do not replace each other.
- **From histogram equalization.** [Histogram equalization](/histogram-equalization/) of the log luminance is a global tone operator: its curve is the cumulative histogram. Methods that cap the slope of this curve limit the contrast gain.
- **From filtering.** A local operator that uses a blurred luminance reduces to a filter of the image, such as a [Gaussian filter](/gaussian-filter/) or a [bilateral filter](/bilateral-filter/), plus a global curve.

## Applications

Tone mapping is the last step of a renderer that shades in linear radiance, which is what [physically based shading](/physically-based-shading/) produces. Games apply it in every frame, often with an automatic exposure. Film and offline renderers apply it, together with color grading, before the output. Photography uses it to show a high dynamic range image merged from several exposures. A high dynamic range display still needs a curve, with less compression, because scenes can exceed its range too.

## References
