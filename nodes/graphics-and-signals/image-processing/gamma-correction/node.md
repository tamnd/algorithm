---
tag: FDBZJX
kind: concept
slug: gamma-correction
name: Gamma correction
aliases:
- gamma encoding
- power-law transform
- sRGB transfer function
area: graphics-and-signals/image-processing
level: advanced
summary: A power-law map between linear light and stored codes, such as the sRGB curve; codes are spread evenly for the eye, so averages and blends must decode to linear light first.
prereqs: [digital-image, pixel]
see_also: [color-spaces, alpha-blending, image-compositing, mipmap, bilinear-filtering, contrast-stretching, histogram-equalization, scalar-quantization]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.2, Power-Law (Gamma) Transformations, page 139
  - paper: "International Electrotechnical Commission, IEC 61966-2-1:1999, Multimedia systems and equipment, Colour measurement and management, Part 2-1, Colour management, Default RGB colour space, sRGB, with Amendment 1, 2003"
    locator: the sRGB transfer functions (slope 12.92 below the breakpoints 0.0031308 and 0.04045, exponent 2.4 with offset 0.055 above them)
  - book: isbn:9780123919267
    title: Charles Poynton, Digital Video and HD, Algorithms and Interfaces, second edition, Morgan Kaufmann, 2012
    locator: the chapters on perceptual uniformity and gamma
---

Gamma correction is the nonlinear map between linear light $L \in [0, 1]$ and the stored value $V \in [0, 1]$ of a pixel, in its simplest form the power law $V = L^{1/\gamma}$ with $\gamma$ near 2.2, and in the [sRGB](/color-spaces/) standard a short straight line near black followed by a $1/2.4$ power. The encoding spends more codes on dark values, where the eye sees small steps, so 8 bits are enough for display. The price is that stored codes are not proportional to light: averaging, blending, filtering and resampling are only physically right after decoding to linear values. As an enhancement, the same power law $s = c\,r^{\gamma}$ is a point operation that brightens or darkens the midtones; it differs from [contrast stretching](/contrast-stretching/), which is linear, and from [histogram equalization](/histogram-equalization/), whose curve comes from the image.

## In plain words

The eye is much better at telling apart two dark grays than two bright grays with the same difference in light. If a file stored light directly with 256 steps, the steps would be too coarse in the shadows, where banding shows, and finer than needed in the highlights. So files store a bent version of the light: the dark part of the range gets many of the codes and the bright part gets fewer. This bending is gamma encoding, and the screen or the program bends it back when it shows the image. The catch is that a stored number of half the maximum does not mean half the light. Any program that mixes pixels, for example to blur, shrink or blend two images, should first undo the bend, do the math on real light, and then bend the result again.

## The idea

**The model.** On this page, values are one channel, scaled to $[0, 1]$; $L$ is linear light, relative to the white of the display, and $V$ is the encoded value. For $b$-bit codes, $V = \text{code}/(2^b - 1)$. The map is applied to each channel and each pixel alone, so there is no pixel position and no border rule.

**The power law.** The plain form is

$$V = L^{1/\gamma}, \qquad L = V^{\gamma}.$$

Gonzalez and Woods write the point operation as $s = c\,r^{\gamma}$ for an input value $r$ and an output value $s$. With $\gamma < 1$ it lifts the dark values, and with $\gamma > 1$ it darkens the midtones. The practice comes from the cathode ray tube, whose light output was close to a power of its input voltage; encoding with the inverse power made the displayed light proportional to the scene light.

**The sRGB curve.** IEC 61966-2-1 defines the encoding

$$V = \begin{cases} 12.92\,L & L \le 0.0031308, \\ 1.055\,L^{1/2.4} - 0.055 & L > 0.0031308, \end{cases} \qquad L = \begin{cases} V/12.92 & V \le 0.04045, \\ \left(\frac{V + 0.055}{1.055}\right)^{2.4} & V > 0.04045. \end{cases}$$

The straight segment avoids the infinite slope of a pure power at 0. Over the whole range the curve is close to a 2.2 power: for the 256 codes of 8-bit sRGB, the largest difference between the sRGB decode and $V^{2.2}$ is 0.0085 in linear light, at code 191. The two pieces do not meet exactly at the published breakpoints: $12.92 \cdot 0.0031308 = 0.040449936$, while the power piece gives about $0.0404499075$ there, and the decode breakpoint 0.04045 is not equal to either. The gap is below $10^{-7}$, far below one 16-bit code. An earlier draft used the decode breakpoint 0.03928, which some old code still has.

**Why the codes are spread this way.** The encoding is a [scalar quantization](/scalar-quantization/) with uniform steps in $V$, so the steps in light are small in the shadows. For 8-bit sRGB, the 13 codes 0 to 12 all decode below $1/255$, the size of one step of a linear 8-bit encoding. A linear 8-bit encoding would give the whole range from 0 to $1/255$ one code.

**Doing math in linear light.** A point operation that only remaps values can work on codes. Anything that adds pixels with weights, such as [alpha blending](/alpha-blending/), [bilinear filtering](/bilinear-filtering/), a [mipmap](/mipmap/) or a blur, models the physics of light only on linear values. The correct steps are: decode with a 256-entry table, compute in floats, and encode the result, rounding to the nearest code.

## Examples

- **Code 128 is not half the light.** sRGB decodes $128/255$ to $L \approx 0.2159$, about 22 percent of white. The 2.2 power gives about 0.2195.
- **Half the light is code 188.** sRGB encodes $L = 0.5$ to $V \approx 0.735$, code 188 after rounding. The pure 2.2 power gives code 186.
- **Middle gray.** A surface that reflects 18 percent of the light, $L = 0.18$, encodes to $117.65$, code 118.
- **Averaging black and white.** The average of the codes 0 and 255 is 127.5, which displays at about 22 percent of white. Decoding to 0 and 1, averaging to 0.5 and encoding gives code 188, the right gray for a 50 percent mix, for example in a 2 to 1 downscale of a fine black and white checkerboard. The codes 64 and 192 average to 146 in linear light, not 128.
- **The 8-bit round trip.** Decoding each of the 256 codes and encoding again with rounding gives back the same code for every code.
- **Enhancement.** On a dark scan, $s = r^{0.5}$ maps $r = 0.04$ to $s = 0.2$ and $r = 0.25$ to $s = 0.5$, which opens up the shadows and compresses the highlights.

## Where it is used

Every 8-bit image file, video stream and display interface uses a gamma-like transfer function, most often sRGB for computer images and the related curves of video standards. Renderers and compositing programs decode textures to linear light, work there, and encode the frame buffer at the end; graphics APIs offer sRGB texture and frame buffer formats that do these steps in hardware. [Color space](/color-spaces/) conversions from sRGB to XYZ or CIELAB start by decoding, because the matrix applies to linear values. In image processing, the power law is one of the basic point operations, next to [contrast stretching](/contrast-stretching/) and [histogram equalization](/histogram-equalization/). Quality measures such as [PSNR](/psnr/) and [SSIM](/structural-similarity-index/) are usually computed on the encoded codes, so a score depends on which of the two the program used.

## References
