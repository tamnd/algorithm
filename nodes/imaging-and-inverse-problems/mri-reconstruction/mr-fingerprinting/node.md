---
tag: Q8ASDJ
kind: technique
slug: mr-fingerprinting
name: MR fingerprinting
aliases:
- magnetic resonance fingerprinting
- MRF
area: imaging-and-inverse-problems/mri-reconstruction
level: research
summary: Vary the acquisition parameters pseudorandomly and match the signal evolution of each voxel to a dictionary simulated by the Bloch equations to get T1 and T2.
prereqs: [bloch-equations, nearest-neighbor-search]
see_also: [partial-separability-model, cosine-similarity, approximate-nearest-neighbor-search, maximum-likelihood-estimation, k-space-trajectory, nonuniform-fft, compressed-sensing-mri, cramer-rao-bound]
sources:
  - paper: doi:10.1038/nature11971
    title: Dan Ma, Vikas Gulani, Nicole Seiberlich, Kecheng Liu, Jeffrey L. Sunshine, Jeffrey L. Duerk and Mark A. Griswold, Magnetic resonance fingerprinting, Nature 495(7440), 2013
    locator: pages 187 to 192 (pseudorandom flip angles and repetition times, undersampled spiral images at each time point, a dictionary simulated from the Bloch equations, and matching by the largest normalized inner product)
---

MR fingerprinting (MRF) measures tissue properties such as the relaxation times $T_1$ and $T_2$ and the proton density in one scan. The scan changes the flip angle and the repetition time from one excitation to the next in a pseudorandom pattern, so that each tissue gives a different signal evolution, its fingerprint. A computer simulates the evolution for a grid of parameter values with the [Bloch equations](/bloch-equations/), and stores the results as a dictionary. For each voxel, the method picks the dictionary entry with the largest normalized inner product with the measured time course, which is a [nearest neighbor search](/nearest-neighbor-search/) by [cosine similarity](/cosine-similarity/), and reads off its parameters. Ma et al. (2013) introduced the method. The abbreviation MRF also names a [Markov random field](/markov-random-field/), which is not related.

## In plain words

A normal MRI scan makes one image with a fixed contrast. To measure $T_1$ and $T_2$ in each voxel, older methods repeat the scan many times with different settings and fit a curve, which takes long.

MRF changes the scanner settings all the time during one scan, in a planned but irregular way. Each tissue then gives its own signal curve over time, like a fingerprint. The computer has a large table of curves, one for each pair of $T_1$ and $T_2$, made by simulating the physics. For each voxel it finds the table curve with the most similar shape and reports its $T_1$ and $T_2$. The height of the curve gives the proton density. The images at each time point can be of low quality, because the match uses the whole curve.

## When it applies

- **The signal follows a model that can be simulated.** The Bloch equations, or the extended phase graph (EPG) form of them, predict the signal of a voxel from its parameters and the sequence. Effects that the model leaves out, such as motion, diffusion and partial volume, go into the error.
- **The parameters are few.** The dictionary has one entry per point of the parameter grid, so its size grows as the product of the grid sizes. Two to four parameters ($T_1$, $T_2$, the off-resonance, the transmit field $B_1$) are common.
- **The sequence makes the fingerprints different.** Different parameter values must give time courses that are not close to multiples of each other. This is a property of the sequence and is checked by simulation.
- **Each time point can be undersampled.** Each time point usually uses one interleaf of a spiral [k-space trajectory](/k-space-trajectory/), so the image of each time point has strong aliasing. The matching averages this aliasing over many time points (a measurement in the papers and in the example below, not a theorem).

## The template

Let $\theta = (\alpha_1, \mathrm{TR}_1, \ldots, \alpha_T, \mathrm{TR}_T)$ be the sequence, $G$ a grid of parameter values $p = (T_1, T_2, \ldots)$, and $x_v \in \mathbb{C}^T$ the time course of voxel $v$, taken from the images reconstructed at each time point (with a [nonuniform FFT](/nonuniform-fft/) for spiral data).

```pseudo id=main
MRF-MATCH(theta, G, X, L)
L1  for each p in G do
L2      d_p <- signal evolution of p under theta   ▷ Bloch or EPG simulation
L3      n_p <- ||d_p||;  d_p <- d_p / n_p
L4  if L > 0 then V <- first L right singular vectors of the dictionary;  d_p <- V^H d_p for all p
L5  for each voxel v do
L6      x <- x_v;  if L > 0 then x <- V^H x
L7      p* <- argmax over p in G of |<d_p, x>|
L8      T1(v), T2(v) <- the values in p*;  PD(v) <- <d_p*, x> / n_p*
L9  return the maps T1, T2 and PD
```

Lines L1 to L4 depend only on the sequence and are run once. Line L7 is the match and line L8 the proton density. Line L4 is the optional compression of McGivney et al. (2014): matching is done in an $L$ dimensional subspace.

**Matching is maximum likelihood on the grid (theorem).** Let $x = \rho\, d_p + e$ with an unknown complex scale $\rho$, a parameter $p \in G$ and white circular Gaussian noise $e$. The maximum likelihood estimate of $(p, \rho)$ minimizes $\|x - \rho d_p\|^2$. For a fixed $p$ the best $\rho$ is $\langle d_p, x\rangle / \|d_p\|^2$, and the remaining value is $\|x\|^2 - |\langle d_p, x\rangle|^2 / \|d_p\|^2$. So the best $p$ is the one with the largest $|\langle d_p, x\rangle| / \|d_p\|$, which is line L7, and $\rho$ is line L8. The absolute value removes the phase of $\rho$, which comes from the coil and the receiver. The theorem is about the grid only: values between grid points are rounded to a grid point.

**Compression keeps the match when the dictionary is in the subspace (theorem).** If every $d_p$ is in the span of the orthonormal columns of $V$, then $\langle d_p, x\rangle = \langle V^H d_p, V^H x\rangle$ for every $x$, so line L7 gives the same $p^*$ with or without compression. When the dictionary is only close to the subspace, the match can change, and how often is a measurement.

**Cost.** With $|G|$ entries, $T$ time points and $V$ voxels, the simulation costs $O(|G|\, T\, S)$ for $S$ phase states (at most $T$ for EPG), and the exhaustive match costs $O(V\, |G|\, T)$. With compression the match costs $O(V\, |G|\, L + V\, T\, L)$. The match is a dense matrix product, and an [approximate nearest neighbor search](/approximate-nearest-neighbor-search/) can replace it for large dictionaries.

**Example (measurement).** A scratch script simulates a FISP-type sequence by EPG: an inversion, a wait of 20 ms, then $T = 400$ excitations. The flip angles are four half sine lobes of random heights between 20 and 70 degrees, plus 5 degrees, and the repetition times are uniform between 11 and 15 ms, a total of 5.18 s. Each repetition has one gradient dephasing step, and the signal is read right after each pulse. There is no off-resonance and no $B_1$ error. The dictionary takes $T_1$ from 100 to 3000 ms and $T_2$ from 10 to 500 ms, in steps of 5 percent, with $T_2 < T_1$: 5109 entries. For four test tissues off the grid, complex Gaussian noise is added, with the signal to noise ratio (SNR) defined as the RMS of the signal over the noise standard deviation at one time point. Values are mean relative errors over 200 noise draws.

| tissue ($T_1$, $T_2$ in ms) | no noise: $T_1$, $T_2$ | SNR 2: $T_1$, $T_2$, PD | SNR 0.5: $T_1$, $T_2$, PD |
|---|---|---|---|
| 420, 38 | 0.020, 0.018 | 0.043, 0.060, 0.031 | 0.158, 0.231, 0.119 |
| 830, 75 | 0.018, 0.014 | 0.032, 0.048, 0.028 | 0.117, 0.188, 0.110 |
| 1330, 110 | 0.002, 0.007 | 0.025, 0.043, 0.026 | 0.095, 0.170, 0.102 |
| 2600, 280 | 0.011, 0.014 | 0.021, 0.053, 0.024 | 0.073, 0.201, 0.087 |

Without noise, the errors come from the grid alone; here they were at most 2.0 percent, less than half the step. At SNR 0.5 at each time point, the mean $T_1$ error was still at most 16 percent, because the match uses all 400 points. In this sequence $T_2$ is harder to measure than $T_1$.

## Classic examples

- **Inversion recovery balanced SSFP (Ma et al. 2013).** Pseudorandom flip angles and repetition times, one undersampled spiral per time point, and a dictionary over $T_1$, $T_2$ and the off-resonance. The balanced sequence is sensitive to the off-resonance, which is then a third parameter.
- **FISP MRF (Jiang et al. 2015).** An unbalanced gradient in each repetition removes most of the off-resonance sensitivity, and the EPG model simulates the signal. The example above is of this type.
- **Maps with the transmit field.** When $B_1$ varies over the body, the flip angles differ from the planned ones. A dictionary with $B_1$ as a parameter, or a separate $B_1$ map, keeps $T_2$ from being biased.

## Variations

- **SVD compression.** The dictionary has low rank in practice. In the example, the first 5 singular values hold 99.89 percent of the energy of the normalized dictionary, and the first 10 hold 99.998 percent. Matching with $L = 10$ gave the same entry as the full match in 97.5 to 99 percent of the noisy trials at SNR 2 (dictionary step 10 percent), against 55.5 to 93.5 percent with $L = 5$.
- **Subspace and low rank reconstruction.** The time courses lie close to a subspace of low dimension, which is the [partial separability model](/partial-separability-model/). Reconstruction in that subspace removes much of the aliasing before the match.
- **Faster matching.** Group matching, tree search and [approximate nearest neighbor search](/approximate-nearest-neighbor-search/) reduce the cost of line L7 for large dictionaries.
- **Regression in place of a dictionary.** A network trained on simulated fingerprints predicts the parameters directly, with no grid. Its accuracy is a measurement on its test data.
- **Sequence design.** The flip angles and repetition times can be chosen to lower the [Cramer-Rao bound](/cramer-rao-bound/) of the parameters, computed from the derivatives of the signal model.

## Pitfalls

- **A sequence that does not separate the parameters.** With a constant flip angle of 30 degrees and a constant TR of 12 ms after the same inversion, the same test (dictionary step 10 percent, SNR 2) gave $T_2$ errors of 0.071 to 0.126, against 0.044 to 0.059 for the varied sequence. The largest normalized inner product between two entries with the same $T_1$ and $T_2$ values that differ by a factor of 1.5 or more was 0.99999 for the constant sequence and 0.9992 for the varied one.
- **Model errors bias the maps.** An error in $B_1$, slice profile, off-resonance or the inversion efficiency changes the fingerprint, and the match then picks a wrong entry with no warning. A high inner product does not prove that the model is right.
- **Grid too coarse or too narrow.** Values between grid points are rounded, and values outside the grid are set to the edge of the grid. Tissues with two compartments in one voxel match an entry that fits neither.
- **Dictionary size.** A grid with four parameters and fine steps gives millions of entries. Memory and match time then dominate, and compression or approximate search is needed.
- **Time points that are too few.** The averaging of aliasing and noise depends on many time points. Short sequences give noisier maps, which is a measurement for each sequence.

## Exercises

1. Show that $\min_{\rho \in \mathbb{C}} \|x - \rho d\|^2 = \|x\|^2 - |\langle d, x\rangle|^2 / \|d\|^2$, and find the minimizer.
2. Show that if all dictionary entries lie in the span of the orthonormal columns of $V$, then matching with $V^H d_p$ and $V^H x$ gives the same result as matching in full length.
3. Why does line L7 use $|\langle d_p, x\rangle|$ and not its real part? What goes wrong without the absolute value?
4. A grid with a geometric step $1 + s$ in $T_1$ has $\lfloor \log(3000/100) / \log(1 + s) \rfloor + 1$ values from 100 to 3000 ms. How many for $s = 0.05$ and $s = 0.01$? With 50 values of $T_2$ and 400 time points of complex double precision, how much memory does each dictionary need?
5. Two entries have the normalized inner product 0.9992. For a time course of 400 points and a noise standard deviation equal to the RMS of the signal, estimate whether noise can switch the match between them.

## References
