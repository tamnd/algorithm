---
tag: RBP3GB
kind: technique
slug: coded-aperture-imaging
name: Coded aperture imaging
aliases:
- uniformly redundant array imaging
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: Image X-rays or gamma rays through a mask of many holes and decode the overlapping shadows by correlation with a matched decoding array.
prereqs: [cross-correlation, circular-convolution, quadratic-residue, inverse-problem]
see_also: [autocorrelation, legendre-symbol, point-spread-function, convolution-theorem, single-pixel-camera, mlem-reconstruction, compressed-sensing, variational-regularization]
sources:
  - paper: doi:10.1086/180230
    title: Robert H. Dicke, Scatter-hole cameras for X-rays and gamma rays, Astrophysical Journal 153, 1968
    locator: page L101 (a mask with many randomly placed pinholes in place of one pinhole)
  - paper: doi:10.1364/AO.17.000337
    title: Edward E. Fenimore and Thomas M. Cannon, Coded aperture imaging with uniformly redundant arrays, Applied Optics 17(3), 1978
    locator: article from page 337 (the URA from twin primes, the mosaic mask and correlation decoding with flat sidelobes)
  - paper: doi:10.1364/AO.28.004344
    title: Stephen R. Gottesman and Edward E. Fenimore, New family of binary arrays for coded aperture imaging, Applied Optics 28(20), 1989
    locator: article from page 4344 (modified URAs of every prime size)
  - paper: doi:10.1007/BF00171998
    title: Ezio Caroli, John B. Stephen, Guido Di Cocco, Lorenzo Natalucci and Angela Spizzichino, Coded aperture imaging in X- and gamma-ray astronomy, Space Science Reviews 45(3-4), 1987
    locator: pages 349 to 403 (survey of mask patterns, decoding and noise)
---

Coded aperture imaging forms an image of X-rays or gamma rays, which no lens can focus, by placing a mask of many holes in front of a position sensitive detector. Each point of the scene casts a shifted copy of the mask pattern, so the detector records the scene convolved with the mask, and the scene is recovered by correlating the record with a decoding array. A uniformly redundant array (URA) is a mask whose periodic autocorrelation is a delta plus a constant; with the balanced decoding array $G = 2A - 1$ the decoding is exact for noiseless data (Fenimore and Cannon 1978). The mask collects about half the light, against a tiny fraction for a pinhole of the same resolution.

## In plain words

A pinhole camera makes a sharp image, but the small hole lets in very little light. Make many holes and much more light gets in, but each bright point in the scene now throws a whole pattern of spots on the detector, and the patterns of all points pile up into a blur. If the holes are placed in the right pattern, the blur can be undone. The decoder slides a copy of the hole pattern over the record and, at each position, adds the counts where the copy has holes and subtracts the counts where it has none. At the true position of a point the sum is large. At every wrong position the good pattern makes the sum the same small constant, which can be removed. So each point comes back sharp, and nothing is left over.

## When it applies

**Setting.** The radiation travels in straight lines and cannot be bent by a lens: hard X-rays, gamma rays, neutrons, and some visible light settings without lenses. The scene is far away compared with the mask, so a source at angle $\theta$ casts the mask shadow shifted by $D\tan\theta$, with $D$ the distance from mask to detector. The angular resolution is about the hole size divided by $D$.

**The cyclic model.** Let the basic array $A$ have $v$ cells with values in $\{0, 1\}$ (open or closed) and $k$ open cells, with indices in $\mathbb{Z}_v$ or in $\mathbb{Z}_r \times \mathbb{Z}_s$. If the mask is a $2 \times 2$ mosaic of the basic array and the detector has the size of one period, then each source in the fully coded field of view casts a complete cyclic shift of $A$ on the detector. For an object $O$ on the same grid the detector record is the [circular convolution](/circular-convolution/)

$$P(j) = \sum_i O(i)\,A(j - i) + B(j) + \text{noise},$$

where $B$ is the background. Without background and noise, $P = A \circledast O$.

**The URA property.** Write $(F \star H)(d) = \sum_t F(t)H(t + d)$ for the periodic [cross-correlation](/cross-correlation/). $A$ is a URA if its support is a cyclic $(v, k, \lambda)$ difference set: every nonzero difference occurs exactly $\lambda$ times among the open cells, that is

$$A \star A = (k - \lambda)\,\delta + \lambda.$$

The arrays used here have $v = 2k + 1$ and $\lambda = (k - 1)/2$. For the decoding array $G = 2A - 1$ (open $+1$, closed $-1$),

$$A \star G = 2(A \star A) - k = 2(k - \lambda)\delta + 2\lambda - k = (k + 1)\,\delta - 1.$$

**Exact decoding.** Correlate the noiseless record with $G$:

$$C(s) = \sum_j P(j)\,G(j - s) = \sum_i O(i)\,(A \star G)(i - s) = (k + 1)\,O(s) - \sum_i O(i).$$

Each object cell adds $k$ counts, so $S = \sum_j P(j) = k\sum_i O(i)$, and

$$O(s) = \frac{C(s) + S/k}{k + 1}.$$

Equivalently, the circulant matrix of $A$ has the power spectrum $k^2$ at frequency 0 and $k - \lambda$ at every other frequency, which is flat; the correlation with $G$ applies its inverse up to the known constant term.

## The template

```pseudo id=main
CODED-APERTURE(O, v)
L1  A ← a 0/1 array of v cells with A ⋆ A = (k − λ)δ + λ and 2λ = k − 1    ▷ hole: the array family
L2  P ← A ⊛ O, the cyclic shadow on the detector                            ▷ the instrument
L3  G ← 2A − 1
L4  k ← Σ A;  S ← Σ P
L5  for each shift s
L6      C(s) ← Σ_j P(j) G(j − s mod v)
L7      Ô(s) ← (C(s) + S/k) / (k + 1)
L8  return Ô
```

Line L2 is the measurement; the reconstruction is lines L3 to L8. The direct sums cost $O(v^2)$ operations. By the [convolution theorem](/convolution-theorem/) the correlation of line L6 for all $s$ costs $O(v\log v)$ with the [FFT](/fast-fourier-transform/). The implementation works with exact integers and returns fractions, so the delta property and the exact recovery can be checked without rounding.

## Classic examples

**Quadratic residues.** For a prime $p \equiv 3 \pmod 4$, let $A(j) = 1$ when $j$ is a nonzero [quadratic residue](/quadratic-residue/) mod $p$, that is when the [Legendre symbol](/legendre-symbol/) $(j/p) = 1$. Then $k = (p - 1)/2$ and the support is a $(p, (p-1)/2, (p-3)/4)$ difference set.

*Proof.* Let $N(d)$ be the number of pairs $(a, b)$ of nonzero squares with $a - b = d$. Multiplication by a nonzero square $c$ maps the squares onto themselves, so $N(cd) = N(d)$: $N$ is constant on the squares and constant on the non-squares. The swap $(a, b) \mapsto (b, a)$ gives $N(-d) = N(d)$, and $-1$ is a non-square for $p \equiv 3 \pmod 4$, so $N$ takes one value $\lambda$ on all $d \ne 0$. There are $k(k - 1)$ ordered pairs with $a \ne b$, so $(p - 1)\lambda = k(k - 1)$ and $\lambda = (k - 1)/2 = (p - 3)/4$. $\blacksquare$

| $p$ | open cells | $k$ | $\lambda$ | $A \star A$ | $A \star G$ |
|---|---|---|---|---|---|
| 7 | $\{1, 2, 4\}$ | 3 | 1 | $(3, 1, 1, 1, 1, 1, 1)$ | $(3, -1, -1, -1, -1, -1, -1)$ |
| 11 | $\{1, 3, 4, 5, 9\}$ | 5 | 2 | peak 5, sidelobes 2 | peak 5, sidelobes $-1$ |
| 19 | the 9 squares | 9 | 4 | peak 9, sidelobes 4 | peak 9, sidelobes $-1$ |
| 23 | the 11 squares | 11 | 5 | peak 11, sidelobes 5 | peak 11, sidelobes $-1$ |

**Twin primes.** For primes $r$ and $s = r + 2$, the array on $\mathbb{Z}_r \times \mathbb{Z}_s$ with $A(i, 0) = 1$ for all $i$, $A(0, j) = 0$ for $j \ne 0$, and otherwise $A(i, j) = 1$ when $(i/r)(j/s) = 1$, is a $(rs, (rs - 1)/2, (rs - 3)/4)$ difference set. For $r = 5$ it is a $5 \times 7$ array with $k = 17$ open cells and all sidelobes of $A \star A$ equal to 8. Fenimore and Cannon (1978) used arrays of this kind, which are close to square and so fit a square detector.

**A point source.** For $p = 11$ and a single source of strength 7 at cell 4, the record is the mask shifted by 4 and multiplied by 7. The correlation gives $C(4) = 6 \cdot 7 - 7 = 35$ and $C(s) = -7$ elsewhere, $S = 35$, and the formula returns 7 at cell 4 and 0 elsewhere.

**Random masks.** Dicke (1968) proposed a mask with many randomly placed holes. A random mask has an autocorrelation with a peak and random sidelobes, so correlation decoding leaves artifacts that depend on the scene. A URA removes them.

## Variations

- **Modified URAs.** Gottesman and Fenimore (1989) gave binary arrays for every prime size, including square $p \times p$ arrays, with a decoding array that differs from $2A - 1$ in one cell. Square arrays fit square detectors, and a free choice of size helps the design.
- **Hexagonal and other lattices.** Difference sets on hexagonal grids give masks for detectors with hexagonal pixels.
- **Iterative and variational decoding.** When the model is not exactly cyclic, because of partial coding at the edge of the field, a mask of finite thickness, detector blur or a near source, correlation is no longer an exact inverse. Then the reconstruction minimizes a [data fidelity term](/data-fidelity-term/) with the true forward model, with the Poisson likelihood and [MLEM](/mlem-reconstruction/), or with a regularizer as in [variational regularization](/variational-regularization/).
- **Lensless cameras.** In visible light, masks and diffusers close to a sensor replace the lens. The forward model is a calibrated convolution or a separable matrix, and the image is reconstructed by regularized least squares, often with total variation. Here the mask need not be a URA.
- **Compressive designs.** Coded apertures combined with fewer measurements than unknowns lead to [compressed sensing](/compressed-sensing/) and to the [single-pixel camera](/single-pixel-camera/), which codes in time instead of space.

## Pitfalls

- **The noise is spread over all pixels.** With Poisson counts and $G = \pm 1$, $\operatorname{Var}C(s) = \sum_j \mathbb{E}P(j) = k\sum_i O(i) + \sum_j B(j)$, the total number of counts, for every $s$. A faint source next to a bright one, or a source on a large diffuse background, gets the noise of the whole scene. For a single point source the coded aperture gains about a factor $\sqrt{k}$ in signal to noise ratio over a pinhole of the same size; for a scene with more than about $k$ bright cells of similar strength the gain falls below 1.
- **The fully coded field of view.** Sources outside the field where they cast a complete cyclic shift produce shadows that are not cyclic, and correlation decoding then makes ghost images. Shielding or a model based reconstruction is needed.
- **Near sources.** For a source at a finite distance the shadow is magnified, and the decoding array must be scaled to match.
- **Background.** A nonuniform background is not removed by the constant term and appears as structure in $\hat O$. It must be measured, for example by rotating the mask, or modeled.
- **Hole size and detector resolution.** If the detector pixel is not smaller than the projected hole, the record is blurred and the effective $A$ is not binary. The decoding must use the blurred pattern.

## Exercises

1. Show that $A \star A = (k - \lambda)\delta + \lambda$ is equivalent to the statement that every nonzero difference $a - b$ of open cells occurs exactly $\lambda$ times.
2. Show that for a $(v, k, \lambda)$ difference set $\lambda(v - 1) = k(k - 1)$, and that $2\lambda - k = -1$ forces $v = 2k + 1$.
3. Compute the URA for $p = 7$, the record of the object $O = (0, 2, 0, 0, 5, 0, 1)$ and its decoding by the formula of line L7.
4. Prove that the discrete Fourier transform of a URA has $|\hat A(\omega)|^2 = k - \lambda$ for every $\omega \ne 0$. What is the condition number of the circulant matrix of $A$?
5. Under Poisson noise, compute the signal to noise ratio of $\hat O(s)$ for a point source with $N$ counts on a uniform background of $b$ counts per detector cell, and compare it with a single pinhole.

## References
