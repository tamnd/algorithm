---
tag: 3DN6XM
kind: algorithm
slug: charge-flipping
name: Charge flipping
aliases:
- charge flipping algorithm
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: Solve a crystal structure by iterating between imposing the measured magnitudes and flipping the sign of electron density below a small threshold.
solves: [crystallographic-phase-problem]
model: real-ram
complexity:
  vars: {N: "the number of grid points in the unit cell, with an FFT", K: "the number of cycles"}
  time: {worst: O(K N log N)}
  space: {extra: O(N)}
properties: {deterministic: false, online: false, in_place: false, exact: false}
history:
  year: 2004
  people: [Gabor Oszlanyi, Andras Suto]
  note: Oszlanyi and Suto introduced charge flipping as an ab initio method that needs no atomic model, no symmetry and no probability theory of phases. Palatinus and Chapuis made it widely available in the program Superflip (2007).
prereqs: [crystallographic-phase-problem, discrete-fourier-transform, error-reduction-algorithm]
see_also: [direct-methods-crystallography, patterson-function, hybrid-input-output, difference-map, phase-retrieval, coherent-diffraction-imaging, fast-fourier-transform, raar]
sources:
  - paper: doi:10.1107/S0108767303027569
    title: Gabor Oszlanyi and Andras Suto, Ab initio structure solution by charge flipping, Acta Crystallographica A 60(2), 2004, 134 to 141
    locator: the algorithm, the threshold delta and the tests on known structures (general locator)
  - paper: doi:10.1107/S0108767304027746
    title: Gabor Oszlanyi and Andras Suto, Ab initio structure solution by charge flipping. II. Use of weak reflections, Acta Crystallographica A 61(1), 2005, 147 to 152
    locator: the special treatment of weak reflections (general locator)
  - paper: doi:10.1107/S0108767307046028
    title: Gabor Oszlanyi and Andras Suto, The charge flipping algorithm, Acta Crystallographica A 64(1), 2008, 123 to 134
    locator: review of the algorithm, its variants and its relation to other iterative phasing methods (general locator)
  - paper: doi:10.1107/S0021889807029238
    title: Lukas Palatinus and Gervais Chapuis, SUPERFLIP, a computer program for the solution of crystal structures by charge flipping in arbitrary dimensions, Journal of Applied Crystallography 40(4), 2007, 786 to 790
    locator: the program Superflip (general locator)
  - url: https://superflip.fzu.cz/download/superflip_user_manual.pdf
    title: Lukas Palatinus, Superflip user manual
    locator: Chapter 2, the charge flipping algorithm (random start phases, F(000), the threshold delta, the R-value as a convergence indicator)
---

Charge flipping is an iterative method that finds the phases of the structure factors of a crystal from their measured amplitudes. It repeats two steps: in real space it changes the sign of all density below a small threshold $\delta$, and in reciprocal space it puts back the measured amplitudes while it keeps the new phases. It needs no atomic model, no knowledge of the chemistry and no symmetry, and it works in the space group $P1$. It is a direct solution of the [crystallographic phase problem](/crystallographic-phase-problem/), a case of [phase retrieval](/phase-retrieval/) for a periodic object.

## In plain words

A crystal scatters X-rays into sharp spots. The brightness of each spot can be measured, but not its phase, and without the phases the picture of the atoms cannot be computed.

Charge flipping starts with random phases and computes a first picture, which is mostly noise. A real crystal picture is almost empty, with a few strong peaks at the atoms. So the method keeps the strong positive parts and turns every weak part upside down. It then computes the spots of this changed picture, keeps their new phases and puts back the measured brightness. After many rounds of this, the picture often jumps quickly from noise to the true atoms. The atoms can come out shifted or mirrored, because the measured brightness is the same for all those pictures.

## The problem

The density $\rho$ is a real function on a grid of $N$ points in the unit cell. Its structure factors are the unnormalized [DFT](/discrete-fourier-transform/) $F(h) = \sum_x \rho(x) e^{-2\pi i\, h \cdot x}$, with $h \cdot x$ the scaled product of the index and the grid point. The data are the amplitudes $|F_{\text{obs}}(h)|$ for the observed reflections $h$, usually without $F(0)$, the total charge. Friedel symmetry $F(-h) = \overline{F(h)}$ holds because $\rho$ is real. The task is to find the phases, and so $\rho$. Any solution can be shifted on the grid or inverted through a point without a change of the data, so the answer is unique at best up to these changes.

## The algorithm

```pseudo id=main
CHARGE-FLIPPING(|F_obs|, δ, K)
L1  F(h) <- |F_obs(h)| e^{iφ(h)} with random φ, φ(-h) = -φ(h); F(h) <- 0 if h is not observed
L2  for cycle <- 1 .. K do
L3      ρ <- IDFT(F)
L4      g(x) <- ρ(x) if ρ(x) > δ, else -ρ(x)          ▷ flip the weak density
L5      G <- DFT(g)
L6      for each index h do
L7          if h is observed then F(h) <- |F_obs(h)| G(h) / |G(h)|
L8          else if h = 0 then F(0) <- G(0)        ▷ the total charge is free
L9          else F(h) <- 0
L10 return IDFT(F)
```

At cycle 0, $F(0) = 0$ unless it is observed. The threshold $\delta$ is the only parameter. It must be small compared with the peaks of the density but larger than the ripple of the truncated Fourier series. The Superflip manual recommends finding it by trial. The progress is followed with the R-value $R = \sum_h \big| |F_{\text{obs}}(h)| - |G(h)| \big| / \sum_h |F_{\text{obs}}(h)|$ over the observed $h$.

## Example

The test file builds a two-dimensional cell of $16 \times 16$ grid points with 8 point atoms, seven of weight 1 and one of weight 2, and zero density elsewhere. All reflections except $F(0)$ are observed. With $\delta = 0.2$ and the start phases of seed 1, the R-value develops as follows (measurement).

| cycle | 1 | 5 | 10 | 20 | 30 | 40 | 50 | 60 | 80 | 100 | 150 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R | 0.510 | 0.420 | 0.401 | 0.387 | 0.323 | 0.368 | 0.165 | 0.060 | 0.011 | 0.007 | 0.004 |

The R-value stays high for about 40 cycles and then falls in a few cycles; this sudden drop is the typical sign of a solution in charge flipping. After 150 cycles the density matches the true one, after the best shift and inversion, with a relative error below 0.25. Of 10 random starts with 150 cycles, 7 reached the structure. The other 3 stayed at an R-value between 0.15 and 0.26, so the usual practice is to run several starts and keep the one with a low R-value.

With $\delta = 0.1$ and with $\delta = 0.3$, none of 4 starts solved the same cell in 200 cycles, while 3 of the same 4 starts solved it with $\delta = 0.2$. The choice of $\delta$ matters. In a one-dimensional test with 64 points and $\delta = 0.1$, the iteration reached $R < 10^{-3}$ with a dense density that is not the structure. A low R-value is evidence of a solution, not a proof.

## Correctness

There is no proof that charge flipping converges. The [proof](proofs/correctness.md) shows the structure of each cycle.

- **The flip is a reflection (theorem).** The flip is $2T_\delta - I$, with $T_\delta$ the hard threshold that sets values at or below $\delta$ to zero. For $\delta = 0$ it is the reflection through the cone of nonnegative densities, $|\rho| = 2\max(\rho, 0) - \rho$.
- **The amplitude step is a projection (theorem).** Lines L6 to L9 give the nearest point to $G$ among the transforms with the measured amplitudes, zero unobserved entries and a free $F(0)$. So a cycle is a projection after a reflection. This places charge flipping next to [hybrid input-output](/hybrid-input-output/) and the [difference map](/difference-map/); [error reduction](/error-reduction-algorithm/) uses the threshold in place of the reflection.
- **Atomic densities are fixed points (theorem).** If every value of the true density is $0$ or above $\delta$, and all reflections that are not observed are zero, then the iteration started at the true structure factors stays there with $R = 0$.
- **Shift and inversion (theorem).** If the start is shifted or inverted, the whole run is shifted or inverted in the same way. The data are the same for these densities, so the origin and the hand of the result are arbitrary.
- **What is not proved.** That the iteration reaches the true structure. In practice the R-value often stays above zero near the solution, because the small values below $\delta$ keep changing sign.

## Complexity

In the [real RAM](/real-ram/) model with the [fast Fourier transform](/fast-fourier-transform/), each cycle costs two DFTs of $N$ points, $O(N \log N)$, plus $O(N)$ for the flip and the amplitude step. $K$ cycles cost $O(K N \log N)$, and the memory holds a few arrays of $N$ numbers. The number of cycles to a solution is random and depends on the structure, the resolution and $\delta$; for the small test above it is about 50 to 80.

## Properties

- **Ab initio.** The method uses only the amplitudes and the fact that the density is mostly near zero with a few peaks.
- **No symmetry needed.** It works in $P1$. The symmetry and the origin are found from the result afterward.
- **Random start.** Each run starts from random phases, and different starts can give different results. Runs are repeated, and the best is kept.
- **One parameter.** Only $\delta$ must be chosen.
- **Atomic resolution.** The method relies on separated peaks in the density, so it needs data to near atomic resolution (a heuristic, not a sharp limit).

## Variants and improvements

- **Weak reflections (Oszlanyi and Suto 2005).** For the weakest observed reflections, the phase is not simply copied from $G$ but shifted by $\pi/2$, which helps the iteration leave stagnation.
- **More than three dimensions.** Superflip applies the same cycle to the density of modulated and incommensurate structures in superspace, which has more than three dimensions.
- **Extra constraints in real space.** The flip can be combined with other constraints on the density, for example on its histogram or its symmetry, once a first map is available.
- **Relation to other methods.** With the threshold in place of the flip, the method becomes error reduction. With other mixes of projection and reflection it becomes HIO, the difference map or [RAAR](/raar/).

## When to use it

Use charge flipping to solve small molecule and inorganic crystal structures from single crystal or powder data with atomic resolution, especially when no model is available or the symmetry is uncertain. It is simple to run and often works where the space group is not known. For large structures with many atoms, or for data at lower resolution, [direct methods](/direct-methods-crystallography/) and dual space programs or, for macromolecules, phasing by heavy atoms or molecular replacement are the usual choices. To find a few heavy atoms, the [Patterson function](/patterson-function/) is another classic tool.

## Pitfalls

- **Wrong $\delta$.** If $\delta$ is too small, the density can settle into a wrong state with many small positive values. If it is too large, real atoms are flipped. Try several values.
- **Trust in R alone.** A low R-value is a sign, not a proof. Check that the density has sensible peaks, distances and a chemically plausible structure.
- **Missing reflections.** Unobserved reflections are set to zero, which adds ripple. Large gaps in the data, such as missing low angle reflections, make convergence harder.
- **Origin and hand.** The result is shifted and possibly inverted. Compare structures only after a search over shifts and inversion, and fix the origin from the symmetry.
- **One run is not enough.** Some starts stagnate. Run several starts and keep the best.
- **A grid that is too coarse.** The grid must be fine enough to sample the peaks of the atoms at the resolution of the data, or the flip mixes atoms with their surroundings.

## Implementations

## History

Oszlanyi and Suto (2004) introduced charge flipping and showed that it solved a range of known structures from their amplitudes alone. In 2005 they added the special treatment of weak reflections. Palatinus and Chapuis (2007) released Superflip, which made the method a standard tool and extended it to structures in more than three dimensions. Oszlanyi and Suto (2008) reviewed the method and its relation to the iterative projection methods of optical phase retrieval, such as the work of Fienup and of Elser.

## References
