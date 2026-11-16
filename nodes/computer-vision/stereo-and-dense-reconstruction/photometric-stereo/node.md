---
tag: QKJF6P
kind: algorithm
slug: photometric-stereo
name: Photometric stereo
aliases:
- Woodham photometric stereo
- calibrated Lambertian photometric stereo
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: "Recover a surface normal and albedo at each pixel from three or more images under known distant lights, by least squares on the Lambertian model."
model: real-ram
complexity:
  vars: {N: the number of images, W: the image width in pixels, H: the image height in pixels}
  time: {worst: Θ(N W H), average: Θ(N W H), best: Θ(N W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1980
  people: [Robert J. Woodham]
  note: "Woodham showed that images of a fixed scene from a fixed camera under several known light directions determine the surface orientation at each pixel, with no correspondence problem."
prereqs: [lambertian-reflectance, normal-equations]
see_also: [shape-from-shading, lambertian-reflectance, ordinary-least-squares, gauss-markov-theorem, singular-value-decomposition, fast-fourier-transform, poisson-equation, brdf]
sources:
  - paper: doi:10.1117/12.7972479
    title: "Robert J. Woodham, Photometric method for determining surface orientation from multiple images, Optical Engineering 19(1), 1980, pages 139 to 144"
    locator: the whole paper (the reflectance map for several light sources and the solution for the surface orientation and albedo)
  - paper: doi:10.1023/A:1008154927611
    title: "Peter N. Belhumeur, David J. Kriegman and Alan L. Yuille, The bas-relief ambiguity, International Journal of Computer Vision 35(1), 1999, pages 33 to 44"
    locator: the generalized bas-relief transformation and the proof that it preserves shading and shadows
  - paper: doi:10.1109/34.3909
    title: "Robert T. Frankot and Rama Chellappa, A method for enforcing integrability in shape from shading algorithms, IEEE Transactions on Pattern Analysis and Machine Intelligence 10(4), 1988, pages 439 to 451"
    locator: the projection of a gradient field onto integrable surfaces in the Fourier domain
  - book: isbn:9780262081597
    title: "Berthold K. P. Horn, Robot Vision, MIT Press, 1986"
    locator: the chapters on reflectance maps and photometric stereo
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 13.1.1, Shape from shading and photometric stereo"
---

Photometric stereo finds the direction a surface faces, and how much light it reflects, at every pixel of a fixed camera. The camera and the object do not move; only the light changes, and each image is taken with one known, distant light. For a matte (Lambertian) surface, each image gives one linear equation for the vector $g = \rho n$, the albedo times the unit normal. Three lights in general position give three equations and fix $g$, and more lights give a least squares solution. Unlike two-view stereo, no pixel matching is needed, since every image shows the same point at the same pixel. Unlike [shape from shading](/shape-from-shading/), which has one image and is ill-posed, the problem at each pixel is a small linear system with a unique solution.

## In plain words

Hold a matte object under a lamp. A part that faces the lamp is bright, and a part that turns away is darker. One photo cannot tell you if a patch is dark because it turns away or because its paint is dark. Now take three photos with the lamp in three different places, without moving the camera or the object. Each patch now has three brightness values, and only one direction and one paint shade explain all three. Solving a small set of equations at every pixel gives the direction the surface faces there and how bright its paint is. Joining the directions gives the shape.

## The problem

**Frame.** This page uses the height-field frame of Horn: $x$ and $y$ lie in the image plane, and $z$ points toward the viewer. This differs from the camera frame of the area, where $Z$ points away from the camera. A surface $z(x, y)$ with slopes $p = z_x$ and $q = z_y$ has the unit normal $n = (-p, -q, 1) / \sqrt{1 + p^2 + q^2}$.

**Input.**

- $N \ge 3$ images $I_1, \dots, I_N$ of size $W \times H$ from one fixed camera, with a linear response.
- A light vector $s_k$ for each image: its direction points toward a distant light, and its length is the strength of the light.
- A threshold below which a reading counts as shadow.

**Model.** At each pixel, $I_k = \max(0, \rho\, n^\top s_k)$ ([Lambertian reflectance](/lambertian-reflectance/) with attached shadows), with the albedo $\rho > 0$ and the unit normal $n$. The camera is orthographic, or far enough that the viewing direction is about the same at all pixels. There are no cast shadows, interreflections or highlights in the readings that are kept.

**Output.** The albedo $\rho$ and the normal $n$ at each pixel, or "unknown" where fewer than three lights in general position light the point.

## The algorithm

```pseudo id=main
PHOTOMETRIC-STEREO(I_1..I_N, s_1..s_N, threshold)
L1  for each pixel p do
L2      A ← {k : I_k(p) > threshold}                ▷ drop shadowed readings
L3      if |A| < 3 then mark p unknown; continue
L4      M ← Σ_{k ∈ A} s_k s_k^T;  b ← Σ_{k ∈ A} I_k(p) s_k
L5      solve M g = b; if M is singular then mark p unknown; continue
L6      ρ(p) ← |g|;  n(p) ← g / |g|
L7  return ρ, n
```

**Line L4, the normal equations.** With the light matrix $L$ whose rows are $s_k^\top$ for $k \in A$, $M = L^\top L$ and $b = L^\top I$. These are the [normal equations](/normal-equations/) of the overdetermined system $L g = I$. For exactly three lights, $M g = b$ has the same solution as $L g = I$.

**Line L5, the solve.** The code uses Gaussian elimination with partial pivoting on the $3 \times 3$ system. If all pixels use all lights, $M$ is the same for every pixel, so one inverse, or one pseudo-inverse of $L$, serves the whole image.

**Line L6, albedo and normal.** The length of $g$ is the albedo because $n$ has length 1. The slopes follow as $p = -n_x / n_z$ and $q = -n_y / n_z$.

**Integration.** The algorithm gives normals, not depths. A height map comes from integrating the slope field $(p, q)$. Noise makes the field slightly non-integrable, so methods find the surface whose slopes are closest to it: Frankot and Chellappa project the field onto integrable surfaces with the [fast Fourier transform](/fast-fourier-transform/), and least squares methods solve a [Poisson equation](/poisson-equation/) $\nabla^2 z = p_x + q_y$.

## Example

**Three lights.** Take $s_1 = (0, 0, 1)$, $s_2 = (0.6, 0, 0.8)$ and $s_3 = (0, 0.6, 0.8)$, all of length 1, and the readings $I = (0.6, 0.84, 0.66)$ at one pixel. The equations are

$$g_z = 0.6, \quad 0.6 g_x + 0.8 g_z = 0.84, \quad 0.6 g_y + 0.8 g_z = 0.66,$$

so $g = (0.6, 0.3, 0.6)$. Then $\rho = \sqrt{0.36 + 0.09 + 0.36} = 0.9$ and $n = (2/3, 1/3, 2/3)$. The slopes are $p = -1$ and $q = -0.5$: the surface goes down toward $+x$ and, less steeply, toward $+y$.

**A sphere with shadows.** The test file renders a cap of a unit sphere with random albedo under five lights, four of them at about 50 degrees from the view direction. Near the edge of the cap some lights do not reach the surface, and 68 of the 845 readings are 0. Dropping these readings recovers every albedo and normal to 9 decimal places, since every pixel still has three lit readings. Keeping them gives albedo errors larger than 0.01, because a 0 reading does not fit the linear model.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **Shadows.** With threshold 0, a reading is kept if and only if $s_k^\top g > 0$, and then it equals $s_k^\top g$.
2. **Exact recovery.** $M = \sum s_k s_k^\top$ is invertible if and only if the kept lights span 3D space, which needs at least three lights that are not in one plane through the origin. Then $b = M g$, so line L5 returns $g$ itself.
3. **Least squares.** With noise, $M^{-1} b$ is the unique minimizer of $\sum (I_k - s_k^\top g)^2$. For independent noise with equal variance it is the best linear unbiased estimate of $g$ by the [Gauss-Markov theorem](/gauss-markov-theorem/).
4. **Necessity.** If the lit lights lie in one plane through the origin, a vector orthogonal to that plane can be added to $g$ without changing any reading.

## Complexity

The model is the real RAM. Each pixel reads its $N$ values and builds $M$ and $b$ in $O(N)$, then solves a $3 \times 3$ system in $O(1)$. The total is $\Theta(N W H)$ in every case, and the output takes $\Theta(W H)$. When every pixel uses all lights, the $3 \times N$ pseudo-inverse of $L$ is computed once, and each pixel costs $3 N$ multiplications.

## Properties

- **Local.** Each pixel is solved on its own. There is no smoothness term and no matching.
- **Exact under the model.** Noise-free Lambertian readings from three or more lit, non-coplanar lights give the exact albedo and normal.
- **Gives normals, not depth.** The depth comes from integration and is known only up to an additive constant.
- **High detail.** The normals have the full resolution of the camera, which shows fine surface detail that triangulation methods miss.
- **Needs the light vectors.** The light directions and strengths must be calibrated, for example with a mirror sphere and a matte sphere.

## Variants and improvements

- **Unknown lights.** The images, stacked as a matrix of $N$ rows and $W H$ columns, have rank 3 under the model. The [singular value decomposition](/singular-value-decomposition/) factors it into normals and lights up to an invertible $3 \times 3$ matrix. Requiring an integrable surface reduces this to the generalized bas-relief ambiguity of Belhumeur, Kriegman and Yuille: $\bar z = \lambda z + \mu x + \nu y$, which gives the same images, shadows included.
- **Robust estimation.** Highlights and cast shadows are outliers to the linear model. Dropping the brightest and darkest readings, or a robust fit over many lights, handles them.
- **Non-Lambertian surfaces.** Methods with a general [BRDF](/brdf/), or with a table of reference objects of the same material, replace the dot product with a measured response.
- **Color.** With color images and white light, the normal is shared by the three channels, and each channel has its own albedo.
- **Near lights and perspective.** Lights close to the object change direction and strength across the surface, which makes the problem nonlinear but still solvable.

## When to use it

Use photometric stereo when you control the lighting and want fine surface detail of a mostly matte object, for example in industrial inspection, scanning of coins, documents, skin or relief. It needs a fixed camera and object while the light moves, so it does not suit moving scenes without special multiplexed lights. For absolute depth, combine it with a triangulation method, such as [structured light scanning](/structured-light-scanning/), whose depths fix the low frequencies that integration gets wrong.

## Pitfalls

- **Nonlinear camera response.** The model needs readings proportional to the light. Gamma-corrected images must be made linear first.
- **Shadows and highlights.** A 0 reading or a specular peak used as a Lambertian reading pulls the normal toward or away from that light. Drop them, as line L2 does for shadows.
- **Lights in one plane.** If all light directions lie in one plane through the surface point, for example lamps placed along one straight line, $M$ is singular. Three lamps at the same height around the camera are fine.
- **Integration drift.** Small biases in the normals add up over the integration and bend the surface, so the low-frequency shape can be wrong while the detail is right.
- **Mixed frames.** Normals in the height-field frame have $n_z > 0$ toward the viewer. In the camera frame of the area, a surface that faces the camera has a negative $Z$ component. Convert before you combine with other methods.

## Implementations

## History

Woodham (1980) introduced photometric stereo: with the camera fixed and the light moved between images, each image constrains the orientation of the surface through the reflectance map of its light, and together the images fix the orientation at each pixel. Horn's book Robot Vision (1986) treats it next to shape from shading. Frankot and Chellappa (1988) gave a fast way to integrate the normals into a surface. Belhumeur, Kriegman and Yuille (1999) showed that with unknown lights the shape can only be found up to the generalized bas-relief transformation, which explains why relief sculptures look right under many lights.

## References
