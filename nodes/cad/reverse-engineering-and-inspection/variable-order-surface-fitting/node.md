---
tag: 710BVP
kind: algorithm
slug: variable-order-surface-fitting
name: Variable-order surface fitting segmentation
aliases:
- Besl-Jain segmentation
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Besl and Jain's region growing that seeds regions by curvature sign and grows them while fitting surfaces of rising polynomial order, until the fit error is too large.
solves: [primitive-segmentation]
model: real-ram
complexity:
  vars: {N: the number of pixels, w: the width of the curvature window, s: the number of seeds, r: the largest depth of a seed inside its block of one surface type, g: the largest number of growth passes for one seed, q: "the number of polynomial coefficients, at most 15"}
  time: {worst: "Θ(N w² + s N r + s (g + 4) N q²)"}
  space: {extra: "Θ(N + w² + N q)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1988
  people: [Paul J. Besl, Ramesh C. Jain]
  note: They segmented range images by seeding regions in the sign map of the mean and Gaussian curvature and growing each seed with polynomial surfaces of order one to four, choosing the lowest order whose fit error stays within the noise.
prereqs: [primitive-segmentation, surface-curvature, least-squares-approximation]
see_also: [region-growing, efficient-ransac-shape-detection, slippage-analysis, geometric-primitive-fitting, curvature-tensor-estimation, image-segmentation, fundamental-forms, reverse-engineering-of-geometric-models]
sources:
  - paper: doi:10.1109/34.3881
    title: Paul J. Besl and Ramesh C. Jain, Segmentation through variable-order surface fitting, IEEE Transactions on Pattern Analysis and Machine Intelligence 10(2), 1988, 167 to 192
    locator: the HK sign map with eight surface types, the seed regions found by erosion, the iterative variable-order region growing with planar, biquadratic, bicubic and biquartic surfaces, and the merging of regions
  - paper: doi:10.1016/0734-189X(86)90220-3
    title: Paul J. Besl and Ramesh C. Jain, Invariant surface characteristics for 3D object recognition in range images, Computer Vision, Graphics, and Image Processing 33(1), 1986, 33 to 80
    locator: the mean and Gaussian curvature of a range image as invariant characteristics, their estimation by local fits, and the classification of regions into eight surface types by their signs
  - paper: doi:10.1016/S0010-4485(96)00054-1
    title: Tamás Várady, Ralph R. Martin and Jordan Cox, Reverse engineering of geometric models, an introduction, Computer-Aided Design 29(4), 1997, 255 to 268
    locator: the section on segmentation, with face-based segmentation by region growing and the use of curvature signs to classify points
---

Variable-order surface fitting is an algorithm that segments a range image into regions, each fitted by a polynomial surface of the lowest order that matches the data within the noise. Besl and Jain (1988) introduced it. It has three stages. First, the mean curvature $H$ and the Gaussian curvature $K$ are estimated at every pixel, and the signs of $H$ and $K$ give each pixel one of eight [surface types](/surface-curvature/): peak, pit, ridge, valley, saddle ridge, saddle valley, flat and minimal. Second, a seed region is taken from the interior of a large block of pixels with one type. Third, the seed grows: a polynomial $z = f(x, y)$ is fitted to the region by [least squares](/least-squares-approximation/), starting with a plane; while the fit error is too large, the order rises through the four orders that Besl and Jain use, planar, biquadratic, bicubic and biquartic; when the fit is good, the region takes in the neighboring pixels that lie close to the surface, and the fit is repeated, until the region stops growing. It solves the [segmentation into primitives](/primitive-segmentation/) for range images, with polynomial surfaces as the primitives.

## In plain words

A range image is a picture where each pixel holds a distance instead of a color. To cut it into faces, the method first looks at how the surface bends at each pixel: up in all directions, down in all directions, like a saddle, like a gutter, or not at all. Where many neighboring pixels bend the same way, it plants a small seed.

Then it tries to cover the seed with the simplest smooth sheet: a flat one first, then gently curved ones of more and more complex shape, up to a limit. As soon as one fits within the noise, the seed spreads to every connected pixel that lies on that sheet, and the sheet is refitted. It stops when nothing more fits. Then it plants the next seed in what is left.

## The problem

**Input.** A range image: heights $z_{ij}$ on a rectangular grid of pixels at $(x, y) = (j h, i h)$; an error bound $\tau$ for the RMS error of a region; a band $\beta \ge \tau$ for the residual of a pixel that joins a region; thresholds $\varepsilon_H$ and $\varepsilon_K$ below which a curvature counts as zero.

**Output.** Disjoint regions of pixels, each 4-connected, with a polynomial $f$ of total degree $d \in \{1, 2, 3, 4\}$ for each region, whose RMS error on the region is at most $\tau$. Pixels may stay unlabeled. Besl and Jain call the four orders planar, biquadratic, bicubic and biquartic, although the polynomials are of total degree $1$ to $4$, with $3$, $6$, $10$ and $15$ coefficients.

## The algorithm

```pseudo id=main
VARIABLE-ORDER-SEGMENTATION(z, h, τ, β)
L1  type(p) ← (sign H(p), sign K(p)) at each pixel p, from a local quadratic fit
L2  while some 5 by 5 block of unblocked pixels has one type: S ← the deepest such block; block S
L3      R ← S; d ← 1
L4      f ← the least-squares polynomial of total degree d on R; e ← its RMS error on R
L5      if e > τ: if d = 4 reject S, else d ← d + 1 and go to L4
L6      R' ← R and the unused pixels connected to R through pixels q with |z(q) − f(q)| ≤ β
L7      if R' = R: accept (R, f, d), mark R used and blocked; else R ← R' and go to L4
L8  return the accepted regions
```

**Line L1.** On a window of $5 \times 5$ pixels the code fits $z \approx c_0 + c_1 u + c_2 v + c_3 u^2 + c_4 u v + c_5 v^2$; since the window has the same shape everywhere, each coefficient is one fixed linear filter. With $f_x = c_1$, $f_y = c_2$, $f_{xx} = 2 c_3$, $f_{xy} = c_4$, $f_{yy} = 2 c_5$ and $g = 1 + f_x^2 + f_y^2$, the curvatures of the graph with the upward normal are
$$ H = \frac{(1 + f_y^2) f_{xx} - 2 f_x f_y f_{xy} + (1 + f_x^2) f_{yy}}{2 g^{3/2}}, \qquad K = \frac{f_{xx} f_{yy} - f_{xy}^2}{g^2} , $$
from the [fundamental forms](/fundamental-forms/) of the graph. A cup $z = x^2 + y^2$ has $H > 0$ and $K > 0$, a pit. Each sign is $0$ when the value is within its threshold. The pair (sign $H$ = 0, sign $K$ > 0) cannot occur for exact curvatures, since $H^2 \ge K$.

**Line L2.** The depth of a pixel is the largest $k$ such that the block of side $2k - 1$ around it has one type and no blocked pixel; the code computes it by repeated erosion and takes the $5 \times 5$ block around the deepest pixel. Besl and Jain also erode the largest regions of one type to get seeds. A seed needs $25$ pixels because Lemma 1 of the proof shows that a $5 \times 5$ grid determines a polynomial of total degree $4$, and a $4 \times 4$ grid does not.

**Lines L4 and L5.** The fit uses the monomials $u^a v^b$ with $a + b \le d$ in the variables shifted to the centroid of the region and scaled to $[-1, 1]$, and modified Gram-Schmidt done twice, which is stable for the $15$ columns of the quartic. The order rises only when the current order cannot fit the region within $\tau$.

**Lines L6 and L7.** The growth is a breadth-first search from the region through unused pixels within the band. The new region contains the old one, so the loop either grows or stops. The code keeps the pixels of a region even when a later fit moves away from them; their residuals then count in the RMS error, and a larger error raises the order.

## Example

A $24 \times 24$ image with $h = 1/23$ has four quadrants of $144$ pixels, with steps of about $3$ in height between them and four polynomials:
$$ 0.3 x - 0.2 y + 0.1, \quad x^2 + y^2 + 0.5 x y + 3, \quad x^2 + y^2 + 0.4 x^3 - 0.2 x y^2 + 6, $$
$$ x^2 + y^2 + 0.3 x^4 + 0.2 x^2 y^2 - 0.1 y^3 + 9 . $$
The sign map is flat in the plane and pit in the other three quadrants, with other types along the steps, where the window crosses two quadrants. The four seeds, one per quadrant, give these RMS errors on their $25$ pixels, with $\tau = 10^{-9}$ and $\beta = 10^{-7}$:

| quadrant | order 1 | order 2 | order 3 | order 4 | result |
| --- | --- | --- | --- | --- | --- |
| plane | $2 \times 10^{-17}$ | | | | 144 pixels, order 1 |
| quadratic | $0.0194$ | $5 \times 10^{-16}$ | | | 144 pixels, order 2 |
| cubic | $0.0242$ | $0.000544$ | $9 \times 10^{-16}$ | | 144 pixels, order 3 |
| quartic | $0.0742$ | $0.00237$ | $3.9 \times 10^{-5}$ | $3.4 \times 10^{-15}$ | 144 pixels, order 4 |

Each seed reaches its true order on its $25$ pixels, grows in one pass to the whole quadrant, and stops; the largest residual of a final fit is $3.6 \times 10^{-15}$.

**With noise.** On the same quadrants over $[0, 2]^2$ with Gaussian noise $\sigma = 10^{-3}$, $\tau = 2 \sigma$, $\beta = 6 \sigma$ and curvature thresholds $0.1$, the code found four regions, each inside one quadrant, with $144$, $144$, $144$ and $139$ pixels and orders $1$, $2$, $3$ and $3$: the quartic quadrant was fitted within the noise by a cubic. At $\sigma = 10^{-2}$ the plane got no seed, because the noise made its curvature signs vary from pixel to pixel. These are measurements with the code of this page.

## Correctness

The correctness file proves:

- **Unisolvence.** A polynomial of degree at most $k$ in each variable that vanishes on a $(k + 1) \times (k + 1)$ grid is zero. So every region that contains a $5 \times 5$ seed determines a unique least-squares polynomial of each order, and the fits of lines L4 never fail.
- **Termination.** Each pass of lines L4 to L7 raises the order, rejects, accepts, or adds a pixel, and each seed blocks at least $25$ new pixels, so the algorithm stops after at most $N/25$ seeds and $N + 4$ passes per seed.
- **Exact recovery of one patch.** Let a seed lie in a 4-connected set $A$ of unused pixels where $z = g$ for a polynomial $g$ of total degree exactly $d^\ast \in \{1, \dots, 4\}$, let $\tau$ be smaller than the RMS errors of the lower orders on the seed, which are all positive, and let every unused pixel next to $A$ but outside it differ from $g$ by more than $\beta$. Then the growth returns exactly $A$, the polynomial $g$ and the order $d^\ast$, in exact arithmetic.

The tests check the last statement on $20$ random polynomial patches, five of each order from $1$ to $4$, and on the four quadrants; all $20$ patches and all four quadrants are recovered with the true order and the whole region. Not proved: that the curvature signs give a seed in every patch, and anything about noisy data, where $\tau$ and $\beta$ trade missed pixels against wrong ones.

## Complexity

The sign map costs $\Theta(w^2)$ per pixel, $\Theta(N w^2)$ in all. One seed search erodes the type map up to $r$ times, $\Theta(N r)$. A fit on a region of $n$ pixels with $q$ coefficients costs $\Theta(n q^2)$, and a growth pass $\Theta(n q)$ for the residuals; each seed has at most $3$ order raises and $g$ growth passes. With $s$ seeds and $n \le N$ this gives the bound in the front matter on the [real RAM](/real-ram/). In practice the regions are disjoint, and the total fitting work is closer to $\Theta((g + 4) N q^2)$.

## Properties

- **Lowest order first.** A region gets the simplest of the four surfaces that fits within $\tau$, which avoids fitting noise with a quartic where a plane will do.
- **Data driven.** No list of shapes is given; the orders and the regions come from the data.
- **Viewpoint dependent.** The polynomials are graphs $z = f(x, y)$ over the image plane, so a surface that is vertical in the view, or that folds over, cannot be one region. The curvature signs themselves do not depend on the viewpoint.
- **Not invariant fits.** A plane or a cylinder that is rotated in space gives a different polynomial, and a cylinder or a sphere is not a polynomial graph at all; it is fitted only approximately by a quartic, or broken into several regions.
- **Greedy.** The seeds are processed one at a time, and the first region takes the disputed pixels.

## Variants and improvements

- **Region merging and boundary refinement.** Besl and Jain merge adjacent regions whose surfaces agree along the shared boundary, and refine the boundaries between regions; the code here does neither.
- **Smoothing first.** Besl and Jain smooth the image before they estimate $H$ and $K$, since second derivatives amplify noise; this would help the noisy example.
- **Other surface families.** Later face-based methods for reverse engineering grow regions with the primitives of CAD, planes, spheres, cylinders, cones and tori, fitted by [geometric fitting](/geometric-primitive-fitting/), or with B-spline patches.
- **Point clouds and meshes.** On unordered points, the grid neighbors are replaced by a neighbor graph, the curvature comes from [curvature tensor estimation](/curvature-tensor-estimation/), and the fit must use the orthogonal distance instead of the height.
- **Other seeds.** Seeds can come from [RANSAC](/efficient-ransac-shape-detection/) candidates or from [slippage analysis](/slippage-analysis/) instead of curvature signs.

## When to use it

Use variable-order fitting to segment range images or height fields of smooth objects into pieces described by low-order polynomials, for example for recognition or for a first model of the surface. For CAD parts with planes, cylinders and cones in arbitrary directions, methods that fit the primitives themselves, such as [efficient RANSAC](/efficient-ransac-shape-detection/), give regions that match the design better. In [reverse engineering](/reverse-engineering-of-geometric-models/) it is a classic face-based method, and its seed and grow scheme is the base of many later ones.

## Pitfalls

- **Thresholds.** $\tau$ and $\beta$ must match the noise. Too small, and the regions stop early or the seeds are rejected; too large, and a region crosses a soft edge into the next face.
- **Growth stops before the order rises.** A region whose surface is of order $4$ can stop growing at order $3$ when the cubic fits the part it has grown to within $\tau$ and no neighbor lies within $\beta$, as in the noisy example.
- **Thin regions.** On a strip of $5$ columns any function of $x$ alone equals a quartic in $x$, so a quintic surface can be cut into strips that each pass the test. The tests show this.
- **Creases.** At an edge where two surfaces meet without a step, the pixels along the edge fit both; the first region takes them.
- **Curvature from noise.** The sign map uses second derivatives and is the most noise-sensitive part. Without smoothing, flat regions fall apart into random types and get no seed.

## Implementations

## History

Besl and Jain studied the mean and Gaussian curvature of range images as features that do not change with the viewpoint in 1986, and classified surfaces into eight types by their signs. In 1988 they built on this the segmentation by variable-order surface fitting, which became a standard method for range images; Besl's book Surfaces in Range Image Understanding (1988) gives the full account. Later comparisons of range image segmentation, such as the one by Hoover and others in 1996 on planar scenes, used it as a reference, and the seed and grow scheme with surface fits carried over to the face-based segmentation of point clouds in reverse engineering.

## References
