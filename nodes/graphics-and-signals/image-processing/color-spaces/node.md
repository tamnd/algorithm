---
tag: PBFC5X
kind: concept
slug: color-spaces
name: Color spaces
aliases:
- RGB
- HSV
- YCbCr
- CIELAB
- color model
area: graphics-and-signals/image-processing
level: intro
summary: Coordinate systems for pixel colors, such as sRGB, CIE XYZ, CIELAB, YCbCr and HSV, and the matrices and formulas that convert between them.
prereqs: [digital-image, gamma-correction]
see_also: [color-quantization, jpeg-compression, image-histogram, histogram-equalization, alpha-blending, principal-component-analysis, spectral-rendering, k-means]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 7.1, Color Fundamentals, page 530; Section 7.2, Color Models, page 535 (RGB, page 537; CMY and CMYK, page 538; HSI, page 541; device independent models, page 548)
  - paper: "International Electrotechnical Commission, IEC 61966-2-1:1999, Multimedia systems and equipment, Colour measurement and management, Part 2-1, Colour management, Default RGB colour space, sRGB, with Amendment 1, 2003"
    locator: the primaries, the D65 white point, the transfer functions and the RGB to XYZ matrix with its inverse
  - paper: doi:10.25039/TR.015.2018
    title: Commission Internationale de l'Eclairage, CIE 015:2018, Colorimetry, fourth edition, 2018
    locator: Section 8.2.1, CIE 1976 (L*a*b*) colour space, CIELAB
  - paper: doi:10.1145/965139.807361
    title: Alvy Ray Smith, Color gamut transform pairs, Computer Graphics (SIGGRAPH 78 Proceedings) 12(3), 1978
    locator: pages 12 to 19 (the hexcone model, HSV, and its transform pair with RGB)
---

A color space is a coordinate system for colors: it gives each pixel color three numbers, and it says what those numbers mean, either in terms of the light that a standard observer sees or in terms of a device. RGB spaces such as sRGB give the amounts of three primaries, CIE XYZ is the device-independent base defined from human color matching, CIELAB is a nonlinear map of XYZ in which equal distances are meant to look about equally different, YCbCr splits a brightness signal from two color differences for compression, and HSV rewrites RGB as hue, saturation and value for color pickers. The conversions are a 3 by 3 matrix on linear values, a per-channel transfer function such as the [sRGB gamma curve](/gamma-correction/), or a piecewise formula. This page covers the coordinates of one color; [gamma correction](/gamma-correction/) covers the per-channel curve and [color quantization](/color-quantization/) the choice of a small palette.

## In plain words

A screen makes every color by mixing red, green and blue light, so three numbers per pixel are enough to describe the colors it can show. But the same three numbers look different on different screens, and they are awkward for many jobs. So people use other sets of three numbers for the same color. One set is tied to human vision, so that a color can be described without naming a screen. Another set is arranged so that the distance between two colors matches how different they look. Video and JPEG files split each color into brightness and two color parts, because the eye notices fine detail in brightness more than in color. Paint programs offer hue, saturation and brightness, because people think about color that way. Converting between the sets is a small formula per pixel.

## The idea

**The model.** On this page a color is three channel values. RGB values are in $[0, 1]$, or 8-bit codes divided by 255. The matrices below apply to linear RGB, so encoded sRGB codes are first decoded with the [sRGB transfer function](/gamma-correction/). YCbCr and HSV are applied to the encoded values, as in practice. Each conversion works on one pixel alone, so there is no pixel position and no border rule.

**RGB and XYZ.** An RGB space is fixed by the chromaticities $(x, y)$ of its three primaries and of its white. sRGB, defined in IEC 61966-2-1, uses red $(0.64, 0.33)$, green $(0.30, 0.60)$, blue $(0.15, 0.06)$ and the white D65 at $(0.3127, 0.3290)$. Write each chromaticity as the XYZ vector $(x/y, 1, (1 - x - y)/y)$, put the three primaries as the columns of a matrix $P$, and solve $P\,s = w$ for the white $w$. Then $M = P\operatorname{diag}(s)$ maps linear RGB to XYZ, with $M(1, 1, 1)^T = w$. For sRGB, this computation rounded to 4 digits gives the matrix of the standard:

$$\begin{pmatrix} X \\ Y \\ Z \end{pmatrix} = \begin{pmatrix} 0.4124 & 0.3576 & 0.1805 \\ 0.2126 & 0.7152 & 0.0722 \\ 0.0193 & 0.1192 & 0.9505 \end{pmatrix} \begin{pmatrix} R \\ G \\ B \end{pmatrix}.$$

The middle row gives the relative luminance $Y$, so green counts for about 72 percent of the brightness and blue for 7 percent. The exact inverse of this 4-digit matrix, rounded to 4 digits, has the rows $(3.2406, -1.5372, -0.4986)$, $(-0.9689, 1.8758, 0.0415)$ and $(0.0557, -0.2040, 1.0570)$. Rounded to 7 digits instead, it equals the inverse given in the 2003 amendment of the standard.

**CIELAB.** CIE 015 defines, relative to a white $(X_n, Y_n, Z_n)$,

$$L^* = 116 f(Y/Y_n) - 16, \quad a^* = 500\,(f(X/X_n) - f(Y/Y_n)), \quad b^* = 200\,(f(Y/Y_n) - f(Z/Z_n)),$$

with $f(t) = t^{1/3}$ for $t > \varepsilon$ and $f(t) = (\kappa t + 16)/116$ otherwise, where $\varepsilon = (6/29)^3 = 216/24389$ and $\kappa = (29/3)^3 = 24389/27$. With these exact fractions, the two pieces of $f$ meet with equal value and slope. $L^*$ runs from 0 for black to 100 for the white, $a^*$ goes from green to red and $b^*$ from blue to yellow. The Euclidean distance $\Delta E^*_{ab}$ is the simplest color difference; later formulas such as CIEDE2000 correct its uneven parts.

**YCbCr.** With luma weights $K_R$ and $K_B$, $K_G = 1 - K_R - K_B$,

$$Y' = K_R R' + K_G G' + K_B B', \quad C_b = 128 + \frac{B' - Y'}{2(1 - K_B)}, \quad C_r = 128 + \frac{R' - Y'}{2(1 - K_R)},$$

on 8-bit encoded values. JPEG files use the full range 0 to 255 with the weights of BT.601, $K_R = 0.299$ and $K_B = 0.114$; this gives, for example, $C_b = 128 - 0.168736 R' - 0.331264 G' + 0.5 B'$ and $C_r = 128 + 0.5 R' - 0.418688 G' - 0.081312 B'$. Video uses a limited range, 16 to 235 for luma, and HD video uses the BT.709 weights. Because the eye resolves fine detail in $Y'$ better than in $C_b$ and $C_r$, [JPEG compression](/jpeg-compression/) and video codecs store the two chroma planes at half resolution or less.

**HSV.** Smith's hexcone model sets the value $V = \max(R, G, B)$, the saturation $S = (V - \min)/V$ (0 when $V = 0$), and the hue $H$ as an angle in six sectors of 60 degrees, decided by which channel is the largest. HSV is fast and intuitive, but it is not perceptual: colors with the same $V$ can look very different in brightness, for example pure blue and pure yellow, which both have $V = 1$. Gonzalez and Woods use the related HSI model, with $I = (R + G + B)/3$.

**Exact round trips.** RGB to XYZ, YCbCr and HSV are rational maps, so with exact fractions they invert exactly. CIELAB has a cube root, so its round trip is exact only on the linear segment of $f$.

## Examples

- **The white point.** sRGB white $(1, 1, 1)$ goes to the row sums of the matrix, $(0.9505, 1, 1.089)$, the XYZ of D65 at the precision of the matrix.
- **Pure red in CIELAB.** Linear $(1, 0, 0)$ with the 4-digit matrix and its own white gives $(L^*, a^*, b^*) = (53.2329, 80.1053, 67.2228)$. Green gives $(87.737, -86.1884, 83.1861)$ and blue $(32.3026, 79.1936, -107.8537)$. The often cited red $(53.2408, 80.0925, 67.2032)$ comes from a more precise matrix and the white $(0.95047, 1, 1.08883)$; the difference is only the rounding of the inputs.
- **Gray in CIELAB.** Linear gray $0.5$, which is sRGB code 188, has $L^* = 76.0693$. A gray with $Y = 0.18$ has $L^* = 49.4961$, close to the middle of the $L^*$ scale.
- **Red in YCbCr.** The 8-bit red $(255, 0, 0)$ gives $Y' = 76.245$, $C_b = 84.972$ and $C_r = 255.5$, so the red corner is just outside the 8-bit range and must be clamped to 255 after rounding. Any gray $(g, g, g)$ gives $(g, 128, 128)$.
- **A blue in HSV.** $(R, G, B) = (0.2, 0.4, 0.8)$ has $V = 0.8$, $S = 0.75$ and, because blue is the largest channel, $H = 4 + (0.2 - 0.4)/0.6 = 11/3$ sectors, that is 220 degrees.

## Where it is used

Every color image file states, or assumes, an RGB space, most often sRGB. Color management converts between device spaces through XYZ or CIELAB. CIELAB distances drive color tolerance checks in industry, and they are a better space than RGB for clustering colors with [k-means](/k-means/) in [color quantization](/color-quantization/). [JPEG compression](/jpeg-compression/) and video codecs work in YCbCr. Contrast methods such as [histogram equalization](/histogram-equalization/) and [CLAHE](/clahe/) are usually applied to a brightness channel ($Y'$, $L^*$ or $V$) and not to R, G and B one by one, which would change the hues (Gonzalez and Woods, Section 7.5). Color pickers and simple segmentation by hue use HSV. Physically based renderers do their light math in a linear RGB space, or in spectra, and convert at the end (see [spectral rendering](/spectral-rendering/)).

## References
