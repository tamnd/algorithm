---
tag: 03GAAZ
kind: algorithm
slug: nearest-neighbor-deconvolution
name: Nearest neighbor deconvolution
aliases:
- neighboring plane deblurring
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Sharpen each plane of a widefield focal series by subtracting a fraction of the two adjacent observed planes, blurred by the one-plane defocus PSF. Fast, linear and approximate."
solves: [image-deblurring]
model: real-ram
complexity:
  vars: {n: the number of pixels per plane, p: the number of planes (n_z in the text), m: the number of nonzero entries of a defocused PSF}
  time: {worst: Θ(p n m), average: Θ(p n m), best: Θ(p n m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, iterative: false, linear: true, nonnegative: false, exact: false}
history:
  year: 1983
  people: [David A. Agard, John W. Sedat]
  note: Agard and Sedat used neighbor subtraction to study the 3D structure of polytene chromosome nuclei from widefield focal series, and Agard (1984) described it in his review of optical sectioning microscopy.
prereqs: [point-spread-function, gibson-lanni-model, neumann-series]
see_also: [wiener-filter, richardson-lucy-deconvolution, richardson-lucy-total-variation, unsharp-masking, optical-transfer-function, image-deblurring, van-cittert-deconvolution]
sources:
  - paper: doi:10.1146/annurev.bb.13.060184.001203
    title: D. A. Agard, Optical sectioning microscopy, cellular architecture in three dimensions, Annual Review of Biophysics and Bioengineering 13, 1984
    locator: pages 191 to 219
  - paper: doi:10.1038/302676a0
    title: David A. Agard and John W. Sedat, Three-dimensional architecture of a polytene nucleus, Nature 302(5910), 1983
    locator: pages 676 to 681
  - paper: doi:10.1006/meth.1999.0873
    title: James G. McNally, Tatiana Karpova, John Cooper and Jose Angel Conchello, Three-dimensional imaging by deconvolution microscopy, Methods 19(3), 1999
    locator: pages 373 to 385 (nearest neighbor and no neighbor methods next to the iterative ones)
---

Nearest neighbor deconvolution removes out-of-focus light from a focal series taken with a widefield fluorescence microscope. Each plane $y_j$ of the stack contains the in-focus image of plane $j$ of the object plus blurred light from all other planes. The method assumes that most of this haze comes from the two adjacent planes, and that the observed neighbors $y_{j \pm 1}$ are good stand-ins for the unknown neighbors of the object. It subtracts them, blurred by the PSF of a source one plane away:

$$\hat x_j = y_j - c\,\big(h_{+1} \ast y_{j-1} + h_{-1} \ast y_{j+1}\big),$$

with a constant $c$ chosen by eye; the analysis below suggests values at or below $1/2$. Agard and Sedat used it in the early 1980s as a fast alternative to full 3D deconvolution. It costs two 2D convolutions per plane and no iterations. It is linear and is the first-order term of the [Neumann series](/neumann-series/) of the inverse, so it removes the fine detail of out-of-focus objects well. It cannot put the mean intensity back in the right plane, it creates negative values that must be clipped, and it adds the noise of three planes.

## In plain words

A microscope that takes a stack of pictures at different focus depths sees each thing sharply in one picture and as a blurred glow in the pictures above and below. To clean one picture, take the picture just above and the one just below, blur them by the amount that one step of focus causes, and subtract a part of that from the picture. The glow from things in the neighbor slices goes away, and things in the slice itself stay sharp. The trick is a guess: the neighbor pictures are themselves glowing copies, not clean slices, and things two or more slices away are ignored. So the result is only approximately right, some pixels come out negative and are set to zero, and the total brightness of each slice is not correct. In return it is very fast.

## The problem

The object is a stack $x_0, \dots, x_{n_z - 1}$ of planes, each an image of $n$ pixels, recorded at equal focus steps. The data stack is

$$y_j = \sum_k h_{j-k} \ast x_k + e_j,$$

where $h_d$ is the 2D [PSF](/point-spread-function/) of a point source $d$ planes away from focus (a slice of the 3D PSF, for example from the [Gibson-Lanni model](/gibson-lanni-model/)), $\ast$ is periodic 2D convolution with the PSF centered at index $0$, and planes outside the stack are empty. The goal is a fast estimate of the in-focus content of each plane. A complete answer would solve the 3D deconvolution problem for the whole stack; this method gives up exactness to work one plane at a time.

## The algorithm

```pseudo id=main
NEAREST-NEIGHBOR(y, h_prev, h_next, c, h0, alpha, clip)   ▷ h_prev = h_{+1}, h_next = h_{-1}
L1  for j ← 0 to n_z - 1
L2      b ← 0
L3      if j > 0:        b ← h_prev * y[j - 1]           ▷ blurred plane below
L4      if j < n_z - 1:  b ← b + h_next * y[j + 1]       ▷ blurred plane above
L5      x[j] ← y[j] - c · b
L6      if h0 is given:  x[j] ← Wiener(x[j], h0, alpha)  ▷ optional in-focus filter
L7      if clip:         x[j] ← max(x[j], 0)
L8  return x
```

Line L6 is the optional second step of Agard's scheme: a 2D filter that undoes the in-focus blur $h_0$, here $\overline{H_0}\,\hat x_j/(|H_0|^2 + \alpha)$ in the Fourier domain (a [Wiener filter](/wiener-filter/) with a constant noise-to-signal ratio $\alpha$). Line L7 sets negative values to zero. End planes have one neighbor only.

## Example

A measurement: 7 planes of $16 \times 16$ pixels with point sources of brightness 50, 100 and 100 in planes 2, 3 and 4, at different lateral positions. The PSF of a source $d$ planes away is a normalized Gaussian of width $0.7 + 1.5|d|$ pixels; each $h_d$ sums to 1, as for a widefield microscope, where every plane receives all the light of every source. The target for each plane is $h_0 \ast x_j$, the in-focus image without haze. Error norms over the whole stack:

| method | stack error |
|---|---|
| raw data | 44.0 |
| $c = 0.3$, clipped | 24.3 |
| $c = 0.45$ | 20.5 |
| $c = 0.45$, clipped | 17.1 |
| $c = 0.5$, clipped | 15.4 |
| $c = 0.6$, clipped | 13.5 |

The haze around each source in its neighbor planes is mostly gone, and clipping helps because the subtraction overshoots. The plane sums tell the other half of the story. In the data every plane sums to 250, the total brightness, whatever plane the sources are in. After the method with $c = 0.45$ the interior planes sum to $25 = (1 - 2 \cdot 0.45) \cdot 250$ and the end planes to $137.5$, while the true plane sums are $0, 0, 50, 100, 100, 0, 0$. The method has no way to tell which plane the mean light came from (Claim 4 of the proof). In this example a larger $c$ gives a smaller error, but the best $c$ depends on the object and the PSF.

## Correctness

The full proof is in `proofs/correctness.md`. Write the blur as $\mathcal A = \mathcal A_0 + \mathcal E + \mathcal R$: the in-focus part, the two neighbor terms and the rest. Lines L1 to L5 compute $(\mathcal I - c\mathcal E)\,y$.

1. **Error formula.** For $y = \mathcal A x$, $\hat x = (\mathcal I - c\mathcal E)\mathcal A x$. In the ideal case $h_0 = \delta$ and no light from planes two or more away, $\hat x = x + (1 - c)\mathcal E x - c\,\mathcal E^2 x$, which the test checks in exact rational arithmetic.
2. **Neumann series.** In that case, with $c = 1$ and $\|\mathcal E\| < 1$, the method is the Neumann series of $(\mathcal I + \mathcal E)^{-1}$ cut after the linear term, and the error is $-\mathcal E^2 x$, at most $\|\mathcal E\|^2\|x\|$.
3. **The mean is not restored.** If the defocused PSFs sum to 1, an interior plane of a constant stack becomes $(1 - 2c)$ times the constant. At low lateral frequencies $\mathcal E$ is not small, and the method only rescales; at high lateral frequencies the defocused OTFs are small and the method is accurate.
4. **No positivity.** The output can be negative, so clipping is needed, and clipping makes the method nonlinear.

## Complexity

In the real-RAM model each plane needs two 2D convolutions and a linear combination. With $m$ nonzero entries in a defocused PSF, a direct convolution costs $\Theta(nm)$; with the [FFT](/fast-fourier-transform/) and the two OTFs computed once, $\Theta(n \log n)$. So the whole stack costs $\Theta(n_z n m)$ or $\Theta(n_z n \log n)$, with no iterations. The optional filter of L6 adds $\Theta(n \log n)$ per plane. Beyond the output, the extra space is $\Theta(n)$ for the blurred neighbors. A plane can be processed as soon as it and its two neighbors are recorded, so the method works on a stream of planes.

## Properties

- Linear in $y$ without clipping, and a fixed 3D filter: a convolution in $z$ with three taps.
- Not exact, even without noise. The error is first order in the neighbor PSFs for $c \ne 1$ and second order for $c = 1$.
- No noise model. The noise of the result is the noise of $y_j$ plus $c$ times the blurred noise of two other planes; the blur smooths the subtracted noise, so the increase is modest, but the L6 filter amplifies high frequencies.
- Not quantitative: plane sums and the axial position of diffuse objects are wrong.

## Variants and improvements

- **No neighbor deconvolution.** Use no neighbor planes at all: subtract a blurred copy of the plane itself, $\hat x_j = y_j - c\, h_{\mathrm{blur}} \ast y_j$, which is [unsharp masking](/unsharp-masking/) with a defocused PSF. It needs only one image per plane and is even more approximate.
- **More neighbors.** Subtract planes $j \pm 2$ with their PSFs as well. This lowers the error from distant planes but adds noise and, by Claim 2 of the proof, more higher-order terms.
- **Fourier domain form.** All steps are convolutions, so the method can be written as one 3D filter on the FFT of the stack.
- **Full 3D deconvolution.** Constrained iterative methods, such as [Richardson-Lucy](/richardson-lucy-deconvolution/) and [RLTV](/richardson-lucy-total-variation/), use the whole 3D PSF and keep the estimate nonnegative. They are quantitative but cost many 3D FFTs.

## When to use it

Use it for a quick look at a widefield stack, for a live preview during acquisition, or when only a few planes are recorded. It improves the contrast of small structures, such as chromosomes, vesicles or filaments, near their focal plane. Do not use it for measurements of intensity, volume or axial position, or when objects are large and diffuse. For quantitative work use a constrained iterative 3D method.

## Pitfalls

- The defocused PSF must match the focus step and the optics. A PSF that is too narrow subtracts sharp copies of neighbor features and creates dark ghosts; a PSF that is too wide leaves the haze.
- Depth-dependent aberration, such as the spherical aberration of the Gibson-Lanni model, changes $h_{\pm 1}$ with depth. A single pair of PSFs is then wrong for part of the stack.
- A large $c$ removes too much light from interior planes; for $c > 1/2$ a uniform region becomes negative and is clipped to zero.
- The end planes have one neighbor and are treated differently, so their brightness does not match the interior planes.
- The L6 filter with a small $\alpha$ amplifies the noise at frequencies where $|H_0|$ is small.

## Implementations

## History

Agard and Sedat (1983) studied the 3D architecture of polytene chromosome nuclei from focal series, and Agard (1984) reviewed optical sectioning microscopy, with the nearest neighbor scheme as the fast option next to constrained iterative 3D deconvolution. McNally, Karpova, Cooper and Conchello (1999) reviewed it next to the no neighbor and the constrained iterative methods.

## References
