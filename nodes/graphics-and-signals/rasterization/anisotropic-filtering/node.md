---
tag: TZHJHY
kind: concept
slug: anisotropic-filtering
name: Anisotropic filtering
aliases:
- anisotropic texture filtering
area: graphics-and-signals/rasterization
level: advanced
summary: Texture filtering that accounts for the elongated footprint of a pixel on a surface seen obliquely.
prereqs: [texture-mapping, mipmap]
see_also: [bilinear-filtering, reconstruction-filter, integral-image, image-warping, antialiasing, perspective-correct-interpolation]
sources:
  - url: https://registry.khronos.org/OpenGL/extensions/EXT/EXT_texture_filter_anisotropic.txt
    title: EXT_texture_filter_anisotropic, OpenGL extension 187, NVIDIA Corporation, 1999, Khronos OpenGL registry
    locator: the changes to Section 3.8.5 (Px, Py, Pmax, Pmin, N = min(ceil(Pmax/Pmin), maxAniso), the level log2(Pmax/N) and the N probes) and the state table (a maximum anisotropy of at least 2.0)
  - paper: doi:10.1109/MCG.1986.276738
    title: Ned Greene and Paul S. Heckbert, Creating raster Omnimax images from multiple perspective views using the elliptical weighted average filter, IEEE Computer Graphics and Applications 6(6), 1986, pages 21 to 27
    locator: the description of the elliptical weighted average filter (the ellipse from the partial derivatives and the weighted sum over it)
  - paper: "Paul S. Heckbert, Fundamentals of Texture Mapping and Image Warping, MS thesis, University of California, Berkeley, report UCB/CSD 89/516, June 1989"
    locator: the chapters on resampling filters and on the elliptical weighted average filter (the derivation of the ellipse and its implementation)
  - paper: doi:10.1145/964965.808600
    title: Franklin C. Crow, Summed-area tables for texture mapping, Computer Graphics 18(3), SIGGRAPH 1984, pages 207 to 212
    locator: the whole paper (box filtering over axis-aligned rectangles in constant time)
  - paper: doi:10.1145/311535.311562
    title: Joel McCormack, Ronald Perry, Keith I. Farkas and Norman P. Jouppi, Feline, fast elliptical lines for anisotropic texture mapping, SIGGRAPH 1999
    locator: the whole paper (several trilinear probes along the major axis of the ellipse)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 6, Texturing, the part on minification (summed-area tables, ripmaps and unconstrained anisotropic filtering)
---

Anisotropic filtering is texture filtering that follows the shape of a pixel's footprint in the texture. A pixel on a surface seen at a grazing angle covers a long, thin region of the texture, and a [mipmap](/mipmap/) lookup, which filters over a square, must choose between blur along the short side and aliasing along the long side. Anisotropic methods filter over the elongated footprint instead: by a weighted sum over an ellipse (EWA), by several mipmap probes along the long axis (the GPU method), or by tables that filter rectangles (ripmaps and summed-area tables). It is a refinement of the [texture mapping](/texture-mapping/) lookup, not a separate algorithm.

## In plain words

Look at a long road or a tiled floor that runs away from you. Each pixel near the horizon sees a strip of the road that is short from side to side but long in the direction away from you. A normal texture lookup picks one blurry copy of the texture that is right for the long direction, so the picture also gets blurry from side to side, and the lines on the road fade. If it picks a sharp copy instead, the long direction flickers and shows false patterns. Anisotropic filtering reads several samples along the long direction of the strip, each from a sharper copy of the texture, and averages them. The road stays sharp across and smooth along. It costs more texture reads per pixel, so graphics cards let you set a limit, such as 16 reads.

## The idea

**The footprint.** At a pixel, the map from screen $(x, y)$ to texture $(u, v)$ in texels has the partial derivatives $(u_x, v_x)$ and $(u_y, v_y)$. To first order, the pixel's square maps to the parallelogram spanned by these two vectors, and a round pixel filter maps to an ellipse. On a surface that faces the viewer, both vectors have about the same length. On a surface seen at a grazing angle, one is much longer than the other: the ratio of the lengths, the *anisotropy*, grows without bound as the angle approaches the horizon.

**Why a mipmap is not enough.** Trilinear filtering chooses the level $\lambda = \log_2 \rho$ with $\rho = \max(P_x, P_y)$, where $P_x = \sqrt{u_x^2 + v_x^2}$ and $P_y = \sqrt{u_y^2 + v_y^2}$, so that one texel of that level covers the long side of the footprint. The level filters equally in both directions, so the short side is blurred by the anisotropy factor. Choosing the level from the short side would keep it sharp but undersample the long side, and the texture would alias.

**Elliptical weighted average (EWA).** Greene and Heckbert (1986) introduced a filter that sums texels with weights over the ellipse. With $(U_x, V_x) = (u_x, v_x)$ and $(U_y, V_y) = (u_y, v_y)$, the ellipse centered at the texture point is $Q(u, v) = A u^2 + B u v + C v^2 \le F$ with

$$A = V_x^2 + V_y^2, \quad B = -2(U_x V_x + U_y V_y), \quad C = U_x^2 + U_y^2, \quad F = (U_x V_y - U_y V_x)^2,$$

where $(u, v)$ is the offset from the center. Each texel inside gets the weight $w(Q/F)$ for a falling profile $w$, usually a truncated Gaussian kept in a table, and the result is $\sum w\, T / \sum w$. Heckbert's 1989 thesis derives and analyzes EWA in detail, and EWA is often credited to that thesis, but the filter was introduced in the 1986 paper. EWA is a high-quality reference, but its cost grows with the area of the ellipse; on a mipmap level where the minor axis spans a few texels, the cost is about proportional to the anisotropy.

**Probes along the major axis.** GPUs approximate the ellipse by $N$ trilinear or bilinear probes along its long axis. The OpenGL extension EXT_texture_filter_anisotropic, now in core OpenGL 4.6, states the ideal computation as

$$P_{\max} = \max(P_x, P_y), \quad P_{\min} = \min(P_x, P_y), \quad N = \min\big(\lceil P_{\max}/P_{\min} \rceil, \mathit{maxAniso}\big), \quad \lambda' = \log_2(P_{\max}/N),$$

and the result is the mean of $N$ lookups at level $\lambda'$, at the points $(x - 1/2 + i/(N + 1), y)$ for $i = 1, \dots, N$ when $P_x > P_y$ (and along $y$ otherwise), mapped into the texture. Each probe covers $P_{\max}/N \approx P_{\min}$ texels, so the level now fits the short side. The user limit $\mathit{maxAniso}$ is at least 2 and is commonly 16; when the anisotropy exceeds it, the level rises again and the image blurs. The extension lets implementations approximate $P_x$ and $P_y$ and the probe placement, so the exact output differs between GPUs. Feline (McCormack and coworkers, 1999) places the probes along the true major axis of the ellipse, with Gaussian weights.

**Axis-aligned methods.** A *ripmap* stores the texture reduced separately in $u$ and in $v$, all $(\log_2 W + 1)(\log_2 H + 1)$ combinations of the two reductions, which takes about four times the memory of the texture, against $4/3$ for a mipmap; it handles footprints that are long along $u$ or $v$, but not diagonal ones. A *summed-area table* (Crow, 1984), the [integral image](/integral-image/) of the texture, gives the box average over any axis-aligned rectangle in constant time. Both fail for footprints that run diagonally across the texture, which EWA and the probe method handle.

**Properties.** All methods are linear in the texture and use nonnegative weights that sum to 1 (in EWA by the division, in the probe method by the mean), so the result stays within the range of the texels read. None of them is exact for the true footprint of a projective map: they use the first-order ellipse or parallelogram, and the probe method uses a fixed number of probes at one level.

## Examples

**Stripes on a floor.** Take a texture of vertical stripes, one texel wide, alternating 0 and 1 along $u$ and constant along $v$. At some pixel the derivatives are $(u_x, v_x) = (1, 0)$ and $(u_y, v_y) = (0, 8)$: the footprint is one texel wide in $u$ and eight texels long in $v$, an anisotropy of 8. The box-filtered answer at a pixel centered on a stripe is that stripe's value, 0 or 1.

- *Trilinear.* $\rho = 8$, so $\lambda = 3$. A texel of level 3 averages $8 \times 8$ texels, four of each color, so every lookup returns $1/2$. The stripes vanish into gray.
- *Anisotropic with $\mathit{maxAniso} = 16$.* $P_{\max}/P_{\min} = 8$, so $N = 8$ and $\lambda' = \log_2(8/8) = 0$. The eight bilinear probes on level 0 lie on the stripe's center line in $u$, spaced $8/9$ texel apart in $v$, and each returns the stripe's value. The result is exactly 0 or 1, the box-filtered answer.
- *Anisotropic with $\mathit{maxAniso} = 4$.* $N = 4$ and $\lambda' = \log_2 2 = 1$. A texel of level 1 averages a $2 \times 2$ block with one texel of each color, so the result is $1/2$ again. With the limit below the anisotropy, the level rises and the detail is lost.

**An oblique footprint.** Let $(u_x, v_x) = (3, 4)$ and $(u_y, v_y) = (-8, 6)$. Then $P_x = 5$ and $P_y = 10$, and the two vectors are orthogonal, so they are the semi-axes of the ellipse. EWA gives $A = 52$, $B = 72$, $C = 73$ and $F = 50^2 = 2500$, and both points $(3, 4)$ and $(-8, 6)$ lie on $Q = F$. The ellipse has area $50\pi$ texels and is tilted, so neither a ripmap nor a summed-area table fits it. The probe method takes $N = 2$ probes along $y$ at level $\lambda' = \log_2 5 \approx 2.32$, where trilinear filtering would use $\log_2 10 \approx 3.32$, one level blurrier.

## Where it is used

- GPU texture units, for every texture lookup where anisotropic filtering is enabled, in games and other real-time rendering; ground, roads, walls and text seen at an angle benefit most.
- Offline renderers, which filter textures with EWA or with several probes from ray differentials; Physically Based Rendering implements EWA on a mipmap.
- [Image warping](/image-warping/) and resampling under strong perspective, such as map and street view renderers, where the same footprint analysis picks the filter.
- Shadow maps and environment maps, which are textures read with elongated footprints too.

## References
