---
tag: FX4QEZ
kind: algorithm
slug: reinhard-tone-mapping
name: Reinhard tone mapping operator
aliases:
- photographic tone reproduction
- Reinhard operator
area: graphics-and-signals/real-time-rendering
level: core
summary: "Scale luminance so that the log average maps to a key such as 0.18, then compress it with L/(1+L) or a white point curve. An optional local step adds dodging and burning."
solves: [tone-mapping]
model: real-ram
complexity:
  vars: {p: the number of pixels, r: the number of scales of the local operator, s: the largest scale in pixels}
  time: {global: Θ(p), local: Θ(p s)}
  space: {extra: Θ(p r)}
properties: {deterministic: true, recursive: false, online: false, in_place: false}
history:
  year: 2002
  people: [Erik Reinhard, Michael Stark, Peter Shirley, James Ferwerda]
  note: Reinhard, Stark, Shirley and Ferwerda took the key value and the dodging and burning of film photography, after the Zone System of Ansel Adams, and turned them into a global and a local tone operator in their SIGGRAPH 2002 paper.
prereqs: [tone-mapping, gaussian-filter]
see_also: [gamma-correction, separable-filter, bilateral-filter, laplacian-pyramid, histogram-equalization, mipmap, physically-based-shading, image-pyramid]
sources:
  - paper: doi:10.1145/566654.566575
    title: Erik Reinhard, Michael Stark, Peter Shirley and James Ferwerda, Photographic tone reproduction for digital images, ACM Transactions on Graphics 21(3) (SIGGRAPH 2002), 267 to 276
    locator: the initial luminance mapping (log average, key, the curve L/(1+L) and the white point form) and the automatic dodging and burning with the center-surround scale selection
  - url: https://www-old.cs.utah.edu/docs/techreports/2002/pdf/UUCS-02-001.pdf
    title: Erik Reinhard, Michael Stark, Peter Shirley and James Ferwerda, Photographic tone reproduction for digital images, University of Utah technical report UUCS-02-001, 2002
    locator: Section 3.1 Initial luminance mapping (Equations 1 to 4) and Section 3.2 Automatic dodging-and-burning (Equations 5 to 9, the parameters phi = 8, epsilon = 0.05, alpha1 = 0.35 and the ratio 1.6)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 8, Light and Color (the part on tone mapping)
  - book: "Erik Reinhard, Greg Ward, Sumanta Pattanaik and Paul Debevec, High Dynamic Range Imaging, Acquisition, Display, and Image-Based Lighting, Morgan Kaufmann, 2005"
    locator: the chapters on tone reproduction (general locator)
---

The Reinhard operator maps the luminance of a high dynamic range image to display values in $[0, 1]$. It first sets the exposure so that the log average luminance of the image maps to a mid gray value, the key $a$, which is $0.18$ by default. Then it compresses each scaled luminance $L$ with the curve $L / (1 + L)$, which is close to linear for dark values and squeezes bright values toward 1, or with a variant that maps a chosen white point to exactly 1. An optional local step divides by a blurred luminance in place of $L$, with a blur size picked per pixel, which copies the dodging and burning of a photographic print. Reinhard, Stark, Shirley and Ferwerda published it in 2002. It is one method for the [tone mapping](/tone-mapping/) problem, and its global form is one of the most used tone curves in games and renderers.

## In plain words

A rendered or photographed scene can be millions of times brighter in the sun than in the shadows, but a screen shows only a small range. The method works like a photographer. First it measures the typical brightness of the image and scales the whole image so that this typical brightness becomes a middle gray. Then it bends the brightness scale. Dark and middle values stay almost as they are, and very bright values are pushed together just below white, so they never clip hard.

The optional second part looks at the neighborhood of each pixel. It finds the largest area around each pixel where the brightness is nearly even, and uses the average of that area to set the compression. A pixel that is darker than its surroundings gets a little darker, and one that is brighter gets a little brighter, so edges and details stay visible.

## The problem

The input is an image of $p$ pixels with world luminances $L_w(i) \ge 0$ in linear units, and a key $a > 0$. The output is a display luminance $L_d(i) \in [0, 1]$ per pixel, in linear values, which a later step encodes for the display (see [gamma correction](/gamma-correction/)). A color image is first reduced to luminance. The paper uses $L_w = 0.27 R + 0.67 G + 0.06 B$; the Rec. 709 weights $0.2126, 0.7152, 0.0722$ are a common choice in other code. A common way to carry the result back to color scales each linear color by $L_d / L_w$, which keeps the ratios of the channels; this step is not part of the paper.

The method has two parts with different status. The log average, the scaling and the compression curve are exact formulas, and their properties below are proved. The choice of the key $a = 0.18$, the curve itself, the constants of the local step and the claim that the result looks like a good print are a visual heuristic and tuning, taken from film photography.

## The algorithm

Lines L1 to L5 are the global operator. $W$ is the white point: the smallest scaled luminance that maps to 1. $W = \infty$ gives the plain curve $L / (1 + L)$. Lines L6 to L14 are the local operator. $B_k$ is the scaled image blurred by a Gaussian of width $\alpha_1 s_k$, where $s_k = 1.6^k$ is the scale in pixels and $\alpha_1 = 1 / (2 \sqrt 2) \approx 0.35$. The surround of scale $k$ has the width $\alpha_2 s_k$ with $\alpha_2 = 1.6\, \alpha_1$, which is the center of scale $k + 1$, so the method needs only $r + 1$ blurs for $r$ scales. $\delta$ is a small constant, for example $10^{-6}$, that keeps $\log 0$ out of black pixels.

```pseudo id=main
REINHARD-GLOBAL(Lw[1..p], a, W)
L1  Lbar ← exp((1/p) · Σi log(δ + Lw[i]))                  ▷ the log average
L2  for each pixel i
L3      L ← (a / Lbar) · Lw[i]                              ▷ the exposure
L4      Ld[i] ← L · (1 + L / W²) / (1 + L)                  ▷ L / (1 + L) when W = ∞
L5  return Ld

REINHARD-LOCAL(Lw[1..p], a, φ, ε, r)
L6  compute Lbar as in L1;  L[i] ← (a / Lbar) · Lw[i] for each pixel i
L7  for k ← 0 to r:  Bk ← L blurred by a Gaussian of width α1 · 1.6^k
L8  for each pixel i
L9      m ← 0
L10     for k ← 0 to r - 1
L11         V ← (Bk[i] - Bk+1[i]) / (a · 2^φ / sk² + Bk[i])
L12         if |V| ≥ ε then leave the loop of L10, else m ← k
L13     Ld[i] ← min(1, L[i] / (1 + Bm[i]))
L14 return Ld
```

Line L1 is the geometric mean of $\delta + L_w$. Line L3 maps a pixel with the log average luminance to $a$. Line L4 is the curve of the paper with the white point; the paper sets $W$ by default to the largest value of $L$ in the image, so that the brightest pixel maps to exactly 1.

Line L7 uses the Gaussian $R(x, y, s) = e^{-(x^2 + y^2) / (\alpha s)^2} / (\pi (\alpha s)^2)$ of the paper. It is separable, so each blur is a row pass and a column pass of a 1D kernel (see [separable filter](/separable-filter/) and [Gaussian filter](/gaussian-filter/)). Line L11 is the normalized center-surround difference, a difference of Gaussians. The division by $B_k$ makes the test independent of the absolute luminance. The term $a\, 2^\varphi / s_k^2$ keeps $V$ from growing large when $B_k$ is near 0; it is large at small scales, so the first scales almost always pass. Line L12 goes up from the smallest scale while the center and the surround agree to within $\varepsilon$, and keeps the last scale that passes: the largest area around the pixel with no large change of contrast. Line L13 is the global curve with $B_m$ in place of $L$ in the denominator. It can exceed 1 at very bright pixels, so the paper clips it.

The paper uses $\varphi = 8$, $\varepsilon = 0.05$ and 8 scales that grow by a factor of 1.6, and gives their range as 1 to 43 pixels. It also gives a list of keys for low key and high key scenes: $0.045$, $0.09$, $0.18$, $0.36$ and $0.72$. All of these are tuning.

## Example

**The global operator.** The image has five pixels with $L_w = 0.01, 0.1, 1, 10, 100$. With $\delta = 0$ the log average is $\bar L = (0.01 \cdot 0.1 \cdot 1 \cdot 10 \cdot 100)^{1/5} = 1$, so with $a = 0.18$ the scaled values are $L = 0.18 L_w$.

| $L_w$ | $L$ | $L / (1 + L)$ | white point $W = 18$ |
|---|---|---|---|
| 0.01 | 0.0018 | 0.00180 | 0.00180 |
| 0.1 | 0.018 | 0.01768 | 0.01768 |
| 1 | 0.18 | 0.15254 | 0.15263 |
| 10 | 1.8 | 0.64286 | 0.64643 |
| 100 | 18 | 0.94737 | 1.00000 |

Four orders of magnitude of input fit in $[0, 1)$. The two darkest pixels are nearly unchanged, because $L / (1 + L) \approx L$ for small $L$. The check values of the plain curve: $L = 1$ maps to $0.5$ and $L = 3$ maps to $0.75$. The last column sets $W$ to the largest $L$, the default of the paper: the brightest pixel maps to exactly 1, and the change from the plain curve is small for the other pixels. With $\delta = 10^{-6}$ the log average becomes $1.000022$ and the values change by less than $10^{-5}$.

**The local operator.** The image is 32 by 32 pixels. The left half (columns 0 to 15) has $L_w = 0.05$ and the right half has $L_w = 5$. The log average is $0.5$ (with $\delta = 10^{-6}$, $0.500005$), so the scaled values are $0.018$ and $1.8$, and the global operator gives $0.0177$ and $0.6429$. For the pixel in row 16 and column 19, three pixels right of the step, lines L10 to L12 compute:

| $k$ | $s_k$ | width $\alpha_1 s_k$ | $B_k$ | $B_{k+1}$ | $a\,2^\varphi / s_k^2$ | $V$ | result |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 0.354 | 1.8000 | 1.8000 | 46.08 | 0.0000 | pass, $m = 0$ |
| 1 | 1.6 | 0.566 | 1.8000 | 1.8000 | 18.00 | 0.0000 | pass, $m = 1$ |
| 2 | 2.56 | 0.905 | 1.8000 | 1.7996 | 7.031 | 0.0000 | pass, $m = 2$ |
| 3 | 4.096 | 1.448 | 1.7996 | 1.7732 | 2.747 | 0.0058 | pass, $m = 3$ |
| 4 | 6.554 | 2.317 | 1.7732 | 1.6403 | 1.073 | 0.0467 | pass, $m = 4$ |
| 5 | 10.49 | 3.707 | 1.6403 | 1.4410 | 0.419 | 0.0968 | stop |

The surround of scale 5 reaches across the step, so $V$ goes above $\varepsilon = 0.05$ and the pixel keeps $m = 4$. Line L13 gives $L_d = 1.8 / (1 + 1.7732) = 0.6491$, a little brighter than the global $0.6429$, because the neighborhood includes some dark pixels. Right at the step, the dark pixel in column 15 maps to $0.0097$ in place of $0.0177$, and the bright pixel in column 16 to $0.9174$ in place of $0.6429$. Far from the step the result is close to the global one: the pixel in column 31 gives $0.6429$. The operator raises the contrast across the edge, which is the dodging and burning effect.

## Correctness

The proofs are in the proofs folder. The global operator has these proved properties, in exact arithmetic:

- $\bar L$ is the geometric mean of $\delta + L_w$, and a constant image maps every pixel to $a$ before the curve.
- With $\delta = 0$, multiplying all inputs by any $c > 0$ does not change the output. The operator removes the exposure of the input.
- The curve $g(L) = L (1 + L / W^2) / (1 + L)$ is strictly increasing, with $g(0) = 0$ and $g(W) = 1$. For $W = \infty$ it stays below 1. So the operator keeps the order of the pixels, and with $W$ equal to the largest $L$ no output exceeds 1. For $L > W$ the curve goes above 1, so a smaller $W$ needs a clip.

For the local operator: the two 1D passes give exactly the 2D convolution with the truncated and normalized Gaussian, the selected index is the largest $k$ such that all tests up to $k$ pass, the output is in $[0, 1]$, and on a constant image every $V$ is 0 and the result equals the global operator. A pixel with $B_m > L$ maps below the global value and a pixel with $B_m < L$ above it, before the clip.

None of this proves that the image looks right. That part is the heuristic of the paper, judged by viewing.

## Complexity

The model is the real RAM, with $p$ pixels and $r$ scales. The global operator reads each pixel twice: $\Theta(p)$ time and $\Theta(p)$ space for the output, or $O(1)$ extra space if it writes in place. On a GPU the log average is a reduction, often done with a chain of smaller and smaller images (see [mipmap](/mipmap/)).

In the local operator, the scale tests of lines L8 to L12 cost $O(p r)$. The blurs of line L7 dominate, and their cost depends on how they are computed. A direct separable blur of width $w$ costs $\Theta(p w)$, so all $r + 1$ blurs cost $\Theta(p \sum_k 1.6^k) = \Theta(p s)$, where $s$ is the largest scale: the widths grow geometrically, so the largest one dominates the sum. The paper computes the blurs with an FFT, at $O(p \log p)$ each, for $O(r p \log p)$. A blur of constant cost per pixel, for example a recursive Gaussian filter or an image pyramid, gives $\Theta(p r)$ in total. The memory is $\Theta(p r)$ to keep all blurs, or $\Theta(p)$ if the scales are done in order and each pixel keeps its current state.

## Properties

- **Global form is a fixed curve.** After the exposure, every pixel uses the same curve, so the operator is cheap, monotone and has no halos.
- **Exposure invariant.** The output depends only on the ratios of the luminances to their log average.
- **Soft shoulder.** $L / (1 + L)$ has slope 1 at 0 and slope $1 / (1 + L)^2$ at $L$, so contrast in bright areas drops fast. Very bright regions lose detail, and the white point form helps only near $W$.
- **Local form raises local contrast.** The local step keeps detail near edges, at the cost of $r + 1$ blurs and with the risk of dark rings around bright areas if the selected scales are too large.
- **Luminance only.** The operator maps luminance. How color is restored is a separate choice.

## Variants and improvements

- **Per channel.** Many real-time renderers apply $x / (1 + x)$ to each of R, G and B after the exposure. It is simpler, but it changes the hue and makes bright colors go toward white, while the luminance form keeps the channel ratios.
- **White point on luminance.** The form of line L4 with a fixed $W$ is often called extended Reinhard. A $W$ below the largest $L$ clips the brightest areas on purpose.
- **Fixed or slowly changing exposure.** In real time the log average of the last frames is smoothed over time to imitate the adaptation of the eye. The rate is tuning.
- **Other local operators.** The bilateral filter operator of Durand and Dorsey, from the same year, splits the log luminance into a base and a detail layer with a [bilateral filter](/bilateral-filter/). Pyramid methods work on a [Laplacian pyramid](/laplacian-pyramid/).
- **Filmic curves.** Games often replace $L / (1 + L)$ by fitted curves with a toe and a shoulder, such as the Hable curve and fits of the ACES curve. These are tuning, see [tone mapping](/tone-mapping/).

## When to use it

Use the global form as a simple, monotone and stable default for real-time and offline images, and when the output must keep the order of brightness. Choose the key for the scene: lower for dark scenes, higher for bright ones. Use the white point form when the brightest areas must reach white. Use the local form for still images with a very high dynamic range, such as interiors with windows, when detail in both the dark and the bright parts matters more than speed. For a film look, use a filmic curve in place of the plain curve.

## Pitfalls

- **Tone mapping in sRGB values.** The operator needs linear luminance. Apply it before the encoding for the display, and do not apply it to values that are already gamma encoded.
- **No $\delta$.** One black pixel makes $\log 0$ undefined and the log average 0. Add a small $\delta$ or skip black pixels.
- **Outliers in the log average.** A large black border or a few very bright pixels move the exposure of the whole image. Mask the border or clamp the values that enter line L1.
- **Values above $W$.** For $L > W$, line L4 gives values above 1. Clip, or set $W$ to the largest $L$.
- **Color shifts.** Scaling each channel by $L_d / L_w$ can push one channel above 1 for saturated bright colors. Clip each channel or desaturate toward white.
- **Normalizing the kernel.** The paper's Gaussian integrates to 1 on the plane, but its sum on a pixel grid with a cut radius does not. Divide by the sum, or a constant image does not stay constant and the scale test is biased.
- **The order of the scale test.** The paper states the rule as taking the first scale, from the lowest, where $|V| < \varepsilon$. Read literally, this almost always takes the smallest scale, because the term $a\, 2^\varphi / s^2$ makes $V$ small there, and the local operator then reduces to the global one. The code of this page goes up while the test passes and keep the last scale that passes, which matches the stated aim of the largest even area.

## Implementations

## History

The paper of Reinhard, Stark, Shirley and Ferwerda (2002) took its ideas from photography. The Zone System of Ansel Adams maps the luminance of a scene to print zones, with the middle gray of an 18 percent reflectance card as the anchor, which became the key $a = 0.18$. Dodging and burning, where the printer holds back or adds light to parts of a print, became the local operator. Its center-surround test follows the local contrast measure of Blommaert and Martens, with changes. Earlier work on tone reproduction in graphics, for example by Tumblin and Rushmeier (1993), had aimed at matching the brightness that a viewer perceives. Reinhard's global curve became a standard tone curve in real-time rendering, and the later book on high dynamic range imaging by Reinhard, Ward, Pattanaik and Debevec (2005) put it among many other operators.

## References
