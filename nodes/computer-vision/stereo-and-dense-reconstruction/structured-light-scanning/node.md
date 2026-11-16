---
tag: PK7WXN
kind: technique
slug: structured-light-scanning
name: Structured light scanning
aliases:
- structured light 3D scanning
- coded light projection
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: "Project coded patterns, such as Gray codes or shifted sine waves, so that each camera pixel decodes its projector column, then intersect the two rays to get depth."
prereqs: [point-triangulation, gray-code, camera-calibration]
see_also: [de-bruijn-sequence, depth-from-disparity, stereo-camera-calibration, photometric-stereo, range-image, point-cloud, tsdf-fusion, iterative-closest-point]
sources:
  - paper: doi:10.1016/0146-664X(82)90096-X
    title: "J. L. Posdamer and M. D. Altschuler, Surface measurement by space-encoded projected beam systems, Computer Graphics and Image Processing 18(1), 1982, pages 1 to 17"
    locator: "the coding of the projector positions by a sequence of binary patterns in time, so that each lit point carries its own code word"
  - paper: doi:10.1016/j.patcog.2003.10.002
    title: "Joaquim Salvi, Jordi Pagès and Joan Batlle, Pattern codification strategies in structured light systems, Pattern Recognition 37(4), 2004, pages 827 to 849"
    locator: "the classification of codes into time multiplexing, spatial neighborhood and direct codification, with binary and Gray codes, phase shifting and De Bruijn sequences"
  - paper: doi:10.1364/AOP.3.000128
    title: "Jason Geng, Structured-light 3D surface imaging: a tutorial, Advances in Optics and Photonics 3(2), 2011, pages 128 to 160"
    locator: "the triangulation principle, the sequential and single-shot techniques, and phase shifting combined with Gray codes"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 13.2, Active rangefinding"
---

Structured light scanning measures the 3D shape of a scene with one camera and one projector. The projector shows a known sequence of patterns, and the camera records how they fall on the scene. The patterns are chosen so that each camera pixel can decode which column of the projector lit it. The projector is then used like a second camera: the pixel gives a ray from the camera, the decoded column gives a plane from the projector, and their intersection is a 3D point. This is the same triangulation as in two-view stereo, but the hard step of stereo, finding which pixels match, is solved by the code. The usual codes are Gray codes, which give each column a binary code word over several images, and shifted sine waves, which give a fine position inside each stripe. The method gives dense and accurate depth for objects in a lab or a factory, and it is the principle of many 3D scanners and of the first Kinect.

## In plain words

Shine a slide projector at a statue and project black and white stripes. A camera beside the projector sees the stripes bend over the shape of the statue. Now project several stripe patterns, one after the other, each with stripes half as wide as before. Each point of the statue is black or white in each photo, and this sequence of black and white tells exactly which stripe of the projector hit it. Since you know where the projector and the camera are, and which way each points, you can draw a line from the camera through the point and a sheet of light from the projector through the stripe. Where the line meets the sheet is the point on the statue. Repeat for every pixel, and you get the shape.

## When it applies

- **You control the light.** The scene is lit mainly by the projector. Bright sunlight washes out the patterns unless the projector is strong or uses a narrow band of light, such as infrared, with a filter on the camera.
- **The scene stays still during the sequence,** for codes that use several images. For moving scenes, single-image codes exist but give less resolution.
- **The camera and the projector are calibrated.** The projector is modeled as an inverse [pinhole camera](/pinhole-camera-model/), and the pair is calibrated like a stereo pair ([stereo camera calibration](/stereo-camera-calibration/)), often with the help of the decoded patterns on a checkerboard.
- **The surface scatters light.** Matte surfaces work best. Shiny, transparent, very dark and translucent surfaces return little of the pattern, or return it to the wrong pixel.
- **Both devices see the point.** A point that the camera sees but the projector does not light, a shadow of the projector, gets no depth.

## The template

The template below uses $m$ Gray code patterns, each followed by its inverse, to find the stripe, and four shifted sine waves of period $P$ projector columns to find the position inside the stripe. The projector has $2^m P$ columns, and the Gray code stripes have width $P$, so they line up with the periods of the sine wave.

```pseudo id=main
STRUCTURED-LIGHT-SCAN(m, P, t)
L1  for j ← 1 to m do project Gray code bit j and its inverse; capture G_j and G'_j
L2  for i ← 0 to 3 do project A + B cos(2π x / P + i π/2) for projector column x; capture I_i
L3  for each camera pixel (u, v) do
L4      if |G_j - G'_j| < t for some j then mark (u, v) unknown; continue
L5      k ← the binary number of the Gray code word with bits [G_j > G'_j]
L6      φ ← atan2(I_3 - I_1, I_0 - I_2) mod 2π;  u_p ← P (k + φ / 2π)
L7      X(u, v) ← the intersection of the ray of (u, v) with the plane of projector column u_p
L8  return X
```

**Line L1, the Gray code.** Stripe number $b$ gets the code word $g = b \oplus (b \gg 1)$. Neighboring stripes differ in exactly one bit, so a pixel on the edge between two stripes is off by at most one stripe, never by a large jump as with plain binary codes. Comparing each image with its inverse, instead of with a fixed threshold, makes the decision work for dark and bright surfaces alike, and a small difference marks a pixel that the projector does not light.

**Line L2, the phase shift.** With the shifts $0, \pi/2, \pi, 3\pi/2$, the four readings are $I_0 = A + B \cos\varphi$, $I_1 = A - B \sin\varphi$, $I_2 = A - B \cos\varphi$ and $I_3 = A + B \sin\varphi$, where $A$ and $B$ include the albedo of the surface and the ambient light. So $I_3 - I_1 = 2 B \sin\varphi$ and $I_0 - I_2 = 2 B \cos\varphi$, and line L6 finds $\varphi$ whatever $A$ and $B$ are. The modulation $B = \tfrac12 \sqrt{(I_3 - I_1)^2 + (I_0 - I_2)^2}$ measures how well the pixel sees the pattern.

**Line L7, the triangulation.** The camera pixel gives the ray $X = \lambda K^{-1} (u, v, 1)^\top$, $\lambda > 0$, in the camera frame. The projector column $u_p$ gives a plane through the projector center, $n^\top X + c = 0$, from the calibration. The point is at $\lambda = -c / (n^\top K^{-1} (u, v, 1)^\top)$. When the projector and the camera are rectified, as in two-view stereo, this reduces to the formula of [depth from disparity](/depth-from-disparity/), with the decoded column in place of the matched pixel.

## Classic examples

- **A 3-bit Gray code.** With $m = 3$, the 8 stripes $b = 0, \dots, 7$ get the code words 000, 001, 011, 010, 110, 111, 101, 100. A pixel that reads white, white, black decodes $g = 110$, and the inverse map $b = g \oplus (g \gg 1) \oplus (g \gg 2)$ gives $b = 4$. With plain binary codes, the edge between stripes 3 and 4 (011 and 100) changes all three bits, and a pixel on it can decode to any of the 8 stripes.
- **One phase shift.** A pixel with $A = 100$, $B = 50$ and $\varphi = 1$ radian reads $I = (127.015, 57.926, 72.985, 142.074)$. Then $\mathrm{atan2}(84.147, 54.030) = 1.000$, the modulation is $B = 50$, and the mean of the four readings is $A = 100$. With $P = 32$ and the Gray code stripe $k = 4$, the projector column is $u_p = 32 (4 + 1/2\pi) = 133.09$, a position finer than one column.
- **Depth.** For a rectified camera and projector with focal length $f = 500$ pixels and baseline $b = 0.1$ m, a pixel whose column differs from its decoded projector column by $d = 20$ is at depth $Z = f b / d = 2.5$ m. Since $\partial Z / \partial d = -Z^2 / (f b)$, an error of 0.1 in $d$ moves the point by $6.25 / 50 \cdot 0.1 = 0.0125$ m there. This is why the sub-column accuracy of the phase matters.
- **A laser line.** A laser with a cylindrical lens projects one plane of light, and the camera finds the bright line in each row. Each image gives one profile, and the object moves on a stage or turns on a table between images. This is the slowest and one of the most robust forms, used in many industrial scanners.
- **One-shot codes.** Stripes in colors that follow a [De Bruijn sequence](/de-bruijn-sequence/), in which every window of $n$ neighboring stripes is different, let each pixel decode its stripe from its neighbors in one image. With 3 colors and windows of 3 stripes, a cyclic De Bruijn sequence has $3^3 = 27$ stripes. The first Kinect used a fixed pattern of infrared dots, whose local arrangement is unique, in the same spirit.

## Variations

Salvi et al. (2004) sort the codes into three groups.

- **Time multiplexing.** Several images per scan: binary codes (Posdamer and Altschuler 1982), Gray codes, phase shifting, and hybrids of Gray codes and phase shifting as in the template. They give the highest accuracy for static scenes.
- **Spatial neighborhood.** One image, with a pattern whose small windows are unique: De Bruijn stripes, grids and pseudo-random dots. They work on moving scenes but lose resolution and fail at depth edges, where a window spans two surfaces.
- **Direct codification.** Each column has its own gray level or color, as in a color ramp. These are simple but sensitive to the color and albedo of the surface.

Other changes:

- **Several frequencies.** Phase shifting with two or three periods, instead of a Gray code, finds the stripe from the phase of the coarser waves. This is called temporal phase unwrapping.
- **Two cameras and a projector.** The pattern only adds texture, and the two cameras do normal stereo matching. The projector then needs no calibration.
- **Fusion.** Scans from several positions are aligned with [ICP](/iterative-closest-point/) and merged, for example with [TSDF fusion](/tsdf-fusion/), into one model.

## Pitfalls

- **Nonlinear response.** A projector or camera with a gamma curve turns the sine waves into other periodic shapes, and the four-step formula then gives a phase error that repeats with the period. Make the response linear first, or use more shifts.
- **Errors at stripe edges.** Where the phase is near 0 or $2\pi$, a small error can put the Gray code stripe and the phase on opposite sides of an edge, and the column jumps by a full period $P$. Hybrids check that the two agree, or use an extra Gray code shifted by half a stripe.
- **Light that arrives indirectly.** Light reflected between surfaces, or scattered under the surface of skin, marble or wax, mixes several projector columns at one pixel. Fine patterns suffer most. Codes made only of high-frequency patterns reduce this.
- **Focus and resolution.** A projector has a limited depth of field. Out of focus, the finest Gray code stripes blur, and their bits become unreliable.
- **Motion.** If the object moves during the sequence, a pixel reads its bits from different points, and the code word is wrong.
- **Specular highlights.** A shiny surface reflects the projector straight into the camera at some pixels, which saturates them, and returns nothing at others.

## Exercises

1. Show that the Gray code words $g(b) = b \oplus (b \gg 1)$ of neighboring numbers $b$ and $b + 1$ differ in exactly one bit, and that $b = g \oplus (g \gg 1) \oplus (g \gg 2) \oplus \cdots$ inverts the map.
2. For three shifts $-2\pi/3, 0, 2\pi/3$, with readings $I_k = A + B \cos(\varphi + \delta_k)$, show that $\varphi = \mathrm{atan2}(\sqrt3 (I_1 - I_3), 2 I_2 - I_1 - I_3)$.
3. A projector has 1024 columns and the sine waves have the period $P = 32$. How many Gray code patterns does the template need? How many images does one scan take, with the inverse patterns?
4. With $f = 500$, $b = 0.1$ m and a decoding error of 0.1 column, find the depth error at 1 m and at 2 m. How does the error change if the baseline is doubled?
5. Explain why an object point that is in the shadow of the projector gets a small $|G_j - G'_j|$ for every $j$ and a small modulation $B$.

## References
