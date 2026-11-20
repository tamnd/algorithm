---
tag: RV95GV
kind: algorithm
slug: epie
name: Extended ptychographical iterative engine
aliases:
- ePIE
- ptychographical iterative engine
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: Update the object and the probe estimates in turn from each diffraction pattern by replacing the modulus and taking a weighted gradient step.
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {m: "the side of the m x m probe window, a power of two", J: "the number of scan positions", K: "the number of sweeps", n: "the side of the n x n object"}
  time: {worst: O(K J m^2 log m)}
  space: {extra: O(n^2 + m^2)}
properties: {deterministic: false, online: false, in_place: false, exact: false}
history:
  year: 2009
  people: [Andrew M. Maiden, John M. Rodenburg]
  note: Maiden and Rodenburg extended the PIE of Rodenburg and Faulkner (2004) so that it also recovers the probe, and visited the positions in random order.
prereqs: [phase-retrieval, ptychography, error-reduction-algorithm, fast-fourier-transform]
see_also: [difference-map, fourier-ptychography, coherent-diffraction-imaging, stochastic-gradient-descent, phase-retrieval-ambiguities, angular-spectrum-method, gerchberg-saxton-algorithm, hybrid-input-output]
sources:
  - paper: doi:10.1016/j.ultramic.2009.05.012
    title: Andrew M. Maiden and John M. Rodenburg, An improved ptychographical phase retrieval algorithm for diffractive imaging, Ultramicroscopy 109(10), 2009, 1256 to 1262
    locator: the ePIE object and probe update functions and the random order of the positions (general locator)
  - paper: doi:10.1063/1.1823034
    title: J. M. Rodenburg and H. M. L. Faulkner, A phase retrieval algorithm for shifting illumination, Applied Physics Letters 85(20), 2004, 4795 to 4797
    locator: the PIE object update with a known probe (general locator)
  - paper: doi:10.1126/science.1158573
    title: Pierre Thibault, Martin Dierolf, Andreas Menzel, Oliver Bunk, Christian David and Franz Pfeiffer, High-resolution scanning X-ray diffraction microscopy, Science 321(5887), 2008, 379 to 382
    locator: the joint reconstruction of object and probe with the difference map (general locator)
  - paper: doi:10.1016/j.ultramic.2008.12.011
    title: Pierre Thibault, Martin Dierolf, Oliver Bunk, Andreas Menzel and Franz Pfeiffer, Probe retrieval in ptychographic coherent diffractive imaging, Ultramicroscopy 109(4), 2009, 338 to 343
    locator: probe retrieval and the artifacts of scans on a regular grid (general locator)
  - paper: doi:10.1107/S0567739469001045
    title: W. Hoppe, Beugung im inhomogenen Primarstrahlwellenfeld. I. Prinzip einer Phasenmessung von Elektronenbeugungsinterferenzen, Acta Crystallographica A 25(4), 1969, 495 to 501
    locator: the principle of phase measurement with an inhomogeneous illumination (general locator)
  - paper: doi:10.1364/OPTICA.4.000736
    title: Andrew Maiden, Daniel Johnson and Peng Li, Further improvements to the ptychographical iterative engine, Optica 4(7), 2017, 736
    locator: the regularized rPIE update and the momentum variant mPIE (general locator)
---

The extended ptychographical iterative engine (ePIE) is an iterative method for [ptychography](/ptychography/). It finds a complex object and the complex illumination (the probe) from many far-field diffraction patterns, each recorded with the probe at a different position on the object, where neighboring positions overlap. For each position in turn, it replaces the moduli of the predicted pattern by the measured ones and then moves the object and the probe a step toward the corrected exit wave. It is a local, pattern-by-pattern method for [phase retrieval](/phase-retrieval/), and the overlap of the positions supplies the constraint that a single pattern does not.

## In plain words

A small spot of coherent light lights up part of a sample, and a camera far away records how the light spreads. The camera keeps only the brightness, not the phase. The spot then moves a little, so that the new spot overlaps the old one, and the camera records again.

The method keeps a guess of the sample and a guess of the spot. For one pattern, it predicts what the camera should see, keeps the predicted phase, and puts in the measured brightness. That gives a better guess of the light just after the sample. The method then changes the sample guess where the spot is bright, and the spot guess where the sample lets light through. Then it goes to the next position, in a random order. Each part of the sample is seen several times, so the guesses must agree with many patterns at once.

## The problem

The object $O$ is an $n_1 \times n_2$ complex image, the probe $P$ an $m_1 \times m_2$ complex image, and $R_1, \dots, R_J$ are the offsets of the probe window in the object. $O_j$ is the window of $O$ at $R_j$, and the exit wave is the pixelwise product $\psi_j = P \odot O_j$, the thin-object model. The far field is the 2D [DFT](/discrete-fourier-transform/) $F$, unnormalized as in this area. The data are the amplitudes

$$a_j = |F(P \odot O_j)|, \qquad j = 1, \dots, J,$$

the square roots of the measured intensities. The task is to find $O$, and usually $P$ as well, from the $a_j$ and the offsets. The answer can only be unique up to the ambiguities of the model, such as $(cO, P/c)$ for a complex constant $c$ (see [Correctness](#correctness)).

## The algorithm

The step sizes $\alpha$ and $\beta$ lie in $(0, 2]$; Maiden and Rodenburg used $\alpha = \beta = 1$.

```pseudo id=main
EPIE(a_1..a_J, R_1..R_J, O, P, K, α, β)
L1  for sweep <- 1 .. K do
L2      draw a random order of the positions
        for each position j in that order do
L3          ψ <- P ⊙ O_j                          ▷ exit wave
L4          Ψ <- F ψ
L5          ψ' <- F^-1 ( a_j · Ψ / |Ψ| )           ▷ phase 0 where Ψ = 0
L6          Δ <- ψ' - ψ
L7          O_j <- O_j + α · conj(P) / max|P|^2 · Δ
L8          P <- P + β · conj(O_j,old) / max|O_j,old|^2 · Δ
L9  return O, P
```

Line L5 is the modulus replacement of the [error-reduction algorithm](/error-reduction-algorithm/), applied to one pattern. Line L7 changes only the pixels of the object under the window. Line L8 uses the window as it was before line L7. To recover the object with a known probe, skip line L8; that is close to the original PIE of Rodenburg and Faulkner (2004), which used a different weighting of the object update.

## Example

**One pixel of the object step.** Take $\alpha = 1$ and the residual $\Delta = \psi' - \psi$ at two pixels of the window. At a pixel where $|P|^2 = \max |P|^2$, line L7 changes the exit wave by exactly $\Delta$, so the new exit wave there equals $\psi'$. At a pixel where $|P|^2 = 0.25 \max |P|^2$, the exit wave moves a quarter of the way, and the residual shrinks to $0.75$ of its size. Where the probe is zero, the object does not change at all, which is right because the data say nothing about it there.

**A small run (measurement).** The test file builds a random $12 \times 12$ object with moduli in $[0.6, 1]$ and phases in $[-1.2, 1.2]$, an $8 \times 8$ Gaussian probe with a quadratic phase, and a $3 \times 3$ grid of positions with a step of 2 pixels, so neighboring windows overlap by 75 percent along each axis. The probe is known, the start object is all ones, and the order uses the seed 2. The table gives the data error $\sum_j \||F\psi_j| - a_j\|^2 / \sum_j \|a_j\|^2$ and the largest error of the object on the central $8 \times 8$ pixels after the best global phase.

| sweeps | data error | object error |
|---|---|---|
| 0 | $4.26 \times 10^{-1}$ | |
| 1 | $6.22 \times 10^{-2}$ | 0.784 |
| 5 | $1.83 \times 10^{-2}$ | 0.472 |
| 10 | $1.04 \times 10^{-2}$ | 0.383 |
| 20 | $2.78 \times 10^{-3}$ | 0.266 |
| 40 | $1.03 \times 10^{-3}$ | 0.139 |
| 60 | $5.57 \times 10^{-4}$ | 0.087 |

The error falls fast in the first sweep and then slowly. When the probe is also unknown, the joint test on a 1D scan starts from the right probe modulus with no phase, and after 150 sweeps the data error is less than 1/50 of its value after the first sweep but does not reach zero, since the joint problem is harder.

## Correctness

The [proof](proofs/correctness.md) shows what each step guarantees; there is no proof of global convergence, and the problem is not convex.

- **Line L5 is a projection (theorem).** It returns the nearest exit wave whose far field has the measured moduli at position $j$.
- **Line L7 is a gradient step that does not increase the residual (theorem).** It is a step along the negative gradient of $\|P \odot O_j - \psi'\|^2$ with respect to the object. At each pixel the new residual is $(1 - \alpha |P|^2/\max|P|^2)$ times the old one, a factor in $[-1, 1]$ for $0 < \alpha \le 2$. With a fixed probe, the data error at the current position therefore does not grow. Line L8 has the same property with the roles of object and probe exchanged.
- **A consistent pair is a fixed point (theorem).** If an object and probe fit all the data, then $\psi' = \psi$ at every step and nothing changes.
- **Ambiguities (theorem).** The data do not change under $(cO, P/c)$, under a linear phase ramp on the object with the opposite ramp on the probe, and under a global phase. No algorithm can resolve these from the data alone.
- **What is not proved.** The total error can grow within a sweep, because a step at one position changes pixels that other positions share. The joint update of object and probe is not covered by the per-pixel bound. Convergence in practice is a measurement.

## Complexity

In the [real RAM](/real-ram/) model with the [fast Fourier transform](/fast-fourier-transform/), each position costs two DFTs of size $m \times m$, $O(m^2 \log m)$, plus $O(m^2)$ for the products and the updates. One sweep over $J$ positions costs $O(J m^2 \log m)$, and $K$ sweeps cost $O(K J m^2 \log m)$. The method stores the object, $O(n^2)$, and the probe and a few work arrays of size $m^2$. The number of sweeps that a reconstruction needs depends on the data, the overlap and the noise, and has no general bound.

## Properties

- **Sequential.** Each position updates the estimates before the next one is used, like [stochastic gradient descent](/stochastic-gradient-descent/) over the positions. The random order breaks the drift that a fixed order can cause.
- **Local.** Each update touches only the $m \times m$ window, so memory per step is small and very large objects are possible.
- **Stable in weak light.** The step is divided by the maximum of $|P|^2$, not by $|P|^2$ at each pixel, so the update is small where the probe is weak and noise there is not amplified.
- **Not deterministic as stated.** The order of the positions is random. A fixed seed makes a run repeatable.

## Variants and improvements

- **PIE (Rodenburg and Faulkner 2004).** The same scheme with a known probe and a different weighting of the object update.
- **Difference map for ptychography (Thibault et al. 2008).** Updates all positions at once with the [difference map](/difference-map/), and refines object and probe together. It is less prone to stagnation and maps well to parallel hardware, at the cost of memory for all exit waves.
- **rPIE and mPIE (Maiden, Johnson and Li 2017).** rPIE blends the per-pixel weight $|P|^2$ with its maximum to give a regularized step. mPIE adds momentum over the sweeps.
- **Position correction.** The scan positions are often not known exactly. Extensions refine them during the reconstruction.
- **Mixed states and multislice.** Partial coherence is modeled with several probe modes, and thick objects with several slices separated by [angular spectrum](/angular-spectrum-method/) propagation.
- **Maximum likelihood.** For low counts, a Poisson model of the noise replaces the modulus replacement by a gradient of the [likelihood](/maximum-likelihood-estimation/).
- **Fourier ptychography.** The same update structure, with the roles of real space and Fourier space exchanged, gives the usual solver for [Fourier ptychography](/fourier-ptychography/).

## When to use it

Use ePIE for scanning ptychography with X-rays, electrons or visible light, when the probe is not known well and the data set is large. It is simple, needs only two FFTs per position and little memory, and recovers the probe as a by-product. For data with strong noise, a model with a known probe error or a need for parallel speed, a difference map or a likelihood method may be better. For a single diffraction pattern with a support constraint, use the methods of [coherent diffraction imaging](/coherent-diffraction-imaging/) such as [hybrid input-output](/hybrid-input-output/).

## Pitfalls

- **Too little overlap.** With little overlap the patterns do not constrain each other, and the reconstruction fails. Experimental studies suggest an overlap of the probe area of about 60 percent or more; this is a guideline from measurements, not a theorem.
- **Raster grid pathology.** On a perfectly regular grid of positions, joint recovery of object and probe can produce a periodic artifact with the period of the grid. Thibault et al. (2009) describe this; a small random offset of the positions avoids it.
- **Scale and ramp ambiguities.** The returned object can carry a constant factor and a linear phase ramp that belong to the probe. Normalize the object, for example to a known empty region, before comparing results.
- **Wrong amplitudes.** The data are the square roots of the intensities. Using the intensities directly makes the modulus replacement wrong.
- **Too large steps.** Values of $\alpha$ above 2 make the residual grow at the bright pixels of the probe.
- **The thin-object model.** The product $P \odot O_j$ assumes that the object is thin compared with the depth of field. Thick objects need a multislice model.

## Implementations

## History

Hoppe (1969) proposed to find the phases of electron diffraction from patterns recorded with an inhomogeneous illumination, the idea that was later called ptychography. Rodenburg and Faulkner (2004) gave the ptychographical iterative engine (PIE), which updates the object from each pattern in turn with a known probe. Thibault and coworkers (2008) reconstructed both the object and the probe with the difference map. Maiden and Rodenburg (2009) added a probe update to PIE, which gave ePIE, and visited the positions in random order. Maiden, Johnson and Li (2017) later proposed the rPIE and mPIE variants.

## References
