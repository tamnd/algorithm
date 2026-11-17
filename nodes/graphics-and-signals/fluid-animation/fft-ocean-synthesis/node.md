---
tag: 6YE8FD
kind: algorithm
slug: fft-ocean-synthesis
name: Tessendorf FFT ocean synthesis
aliases:
- FFT ocean waves
- statistical ocean wave synthesis
area: graphics-and-signals/fluid-animation
level: core
summary: Fill a frequency grid with random amplitudes from an ocean spectrum such as Phillips, advance phases by the dispersion relation, and invert by FFT.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {N: "the number of grid points along one side of the patch"}
  time: {setup: "O(N^2)", frame: "O(N^2 log N)"}
  space: {extra: "O(N^2)"}
properties: {deterministic: true, exact: false, periodic: true, real_output: true, needs_simulation: false}
history:
  year: 2001
  people: [Jerry Tessendorf, Gary Mastin, Peter Watterberg, John Mareda]
  note: Mastin, Watterberg and Mareda (1987) filtered white noise by an ocean spectrum and inverted it by FFT. Tessendorf's course notes (2001) gave the form used today, with the time evolution by the dispersion relation and the choppy displacement.
prereqs: [fast-fourier-transform, discrete-fourier-transform]
see_also: [gerstner-waves, height-field-water, shallow-water-equations, fluid-simulation-for-animation, wave-equation]
sources:
  - book: "Jerry Tessendorf, Simulating Ocean Water, SIGGRAPH course notes, 2001"
    title: Simulating Ocean Water
    locator: the sections on the statistical wave model, the Phillips spectrum, the time evolution and choppy waves
  - paper: doi:10.1109/MCG.1987.276961
    title: Gary Mastin, Peter Watterberg and John Mareda, Fourier synthesis of ocean scenes, IEEE Computer Graphics and Applications 7(3), 16-23, 1987
    locator: the whole paper (white noise filtered by an ocean wave spectrum and inverted by FFT)
  - paper: doi:10.1017/S0022112058000550
    title: O. M. Phillips, The equilibrium range in the spectrum of wind-generated waves, Journal of Fluid Mechanics 4(4), 426-434, 1958
    locator: the equilibrium range of the spectrum (general locator)
---

FFT ocean synthesis makes an animated patch of deep ocean as a sum of many thousands of sine waves, one for each point of a frequency grid.
Each wave gets a random amplitude whose size comes from an ocean wave spectrum, often the Phillips spectrum, and a speed from the deep water dispersion relation $\omega^2 = g k$.
One inverse [fast Fourier transform](/fast-fourier-transform/) per frame then gives the heights at all $N^2$ grid points in $O(N^2 \log N)$ time.
Mastin, Watterberg and Mareda (1987) used this idea for images of the sea, and Tessendorf (2001) made it a standard method for ocean surfaces in film and games, with the motion in time and a horizontal "choppy" displacement.
There is no simulation: each frame comes from a closed formula, and the patch repeats in space, so it tiles.

## In plain words

The sea far from the coast looks like many waves of different lengths that run in different directions and pass through each other.
Long waves run faster than short ones.
The method picks a large set of wave lengths and directions on a regular grid, gives each one a random size, with more size for the waves that the wind makes most, and lets each wave run at its own speed.
To find the height of the water at every point of the grid, it adds up all the waves, and the fast Fourier transform does this sum for all points at once.
A small sideways push of each point makes the crests sharper.

## The problem

The input is the patch size $L$ (m), the grid size $N$ (a power of 2), the wind direction $\hat w$ and speed $V$ (m/s), a spectrum scale $A$, gravity $g = 9.81$ m/s², a random seed, the frame times $t$ and a choppiness $\lambda \ge 0$.
The output, for each frame, is the height $h$ and the horizontal displacement $D$ at the grid points $x = (aL/N, bL/N)$, $0 \le a, b < N$.
The wave vectors are $k = (2\pi n'/L, 2\pi m'/L)$ for the signed indices $-N/2 \le n', m' < N/2$, and

$$h(x, t) = \sum_k H(k, t)\, e^{i k\cdot x}, \qquad H(k, t) = h_0(k)\, e^{i\omega(k) t} + \overline{h_0(-k)}\, e^{-i\omega(k) t}, \qquad \omega(k) = (g |k|)^{1/2}.$$

The initial amplitudes are $h_0(k) = (\xi_r + i\xi_i)(P(k)/2)^{1/2}$ with independent standard normal $\xi_r, \xi_i$.
The Phillips spectrum, in the form of Tessendorf, is

$$P(k) = A\, \frac{e^{-1/(|k| \ell)^2}}{|k|^4}\, |\hat k\cdot\hat w|^2, \qquad \ell = V^2/g.$$

The dispersion relation $\omega^2 = g k$ is the law for small waves on deep water.
The Phillips spectrum is a fit, not a law: it approximates the spectrum of a wind sea in deep water, with the $|k|^{-4}$ fall of the equilibrium range of Phillips (1958) at short waves, a cut at waves longer than about $\ell$, the largest waves that a steady wind of speed $V$ can raise, and a factor that removes waves that run across the wind.
This is one method for [fluid simulation for animation](/fluid-simulation-for-animation/).

## The algorithm

```pseudo id=main
FFT-OCEAN(L, N, ŵ, V, A, seed, times, λ)
L1  for each k on the grid: h₀(k) ← (ξ_r + i ξ_i)(P(k)/2)^½, with ξ from the seeded generator
L2  for each frame time t
L3      for each k: H(k, t) ← h₀(k) e^{iω(k)t} + conj(h₀(-k)) e^{-iω(k)t}
L4      h ← inverse 2D FFT of H
L5      D ← inverse 2D FFT of -i λ (k/|k|) H
L6      output the points x + D with the heights h
```

Line L1 runs once.
It draws two normal numbers for each grid point, so a fixed seed gives the same ocean each time.
The code sets $h_0$ to 0 on the row and the column of the index $N/2$, where $k$ and $-k$ fall on the same grid point; this keeps the displacement of line L5 real, and it is a choice of this code.
Line L3 moves each wave forward in time: the factor $e^{i\omega t}$ turns its phase at the rate of the dispersion relation, and the second term is the partner wave that makes $H(-k) = \overline{H(k)}$.
That symmetry makes the height real.
Line L4 is the inverse 2D DFT, done by a 1D [FFT](/fast-fourier-transform/) on each row and then on each column, with no factor $1/N^2$.
Line L5 is optional: it moves each point toward the crests and away from the troughs, which makes the crests sharp and the troughs flat, as a [Gerstner wave](/gerstner-waves/) does.
The code writes its own radix-2 FFT, and the test compares it with a direct sum.

## Example

Take $L = 100$ m, $V = 10$ m/s (so $\ell = 10.19$ m), the wind along $x$, $A = 3\cdot 10^{-6}$, seed 3, and $t = 0$.
For each $N$, the table gives the largest imaginary part of the computed height, the largest difference from a direct evaluation of the sum, the measured root mean square height, the expected value $(\sum_k 2P(k))^{1/2}$ from the proof, and the time of one height field in this pure Python code.

| $N$ | max $\lvert\operatorname{Im} h\rvert$ (m) | max difference from the direct sum (m) | measured RMS height (m) | expected RMS height (m) | FFT time (s) | direct sum time (s) |
|---|---|---|---|---|---|---|
| 8 | 3.5e-16 | 1.3e-15 | 0.535 | 0.475 | 0.0001 | 0.002 |
| 16 | 3.7e-16 | 2.2e-15 | 0.533 | 0.504 | 0.0005 | 0.029 |
| 32 | 3.6e-16 | 4.0e-15 | 0.622 | 0.510 | 0.002 | 0.88 |
| 64 | 7.3e-16 | not run | 0.769 | 0.512 | 0.014 | not run |

The imaginary part is rounding only, and the FFT gives the same heights as the direct sum.
The measured RMS height of one random ocean differs from the expected value because a few long waves near the peak of the spectrum carry most of the energy.
The direct sum costs $N^4$ terms, so it is several hundred times slower at $N = 32$.

One wave of wavelength 10 m has $k = 0.628319$ rad/m, $\omega = 2.482701$ rad/s, the period $2.530786$ s and the phase speed $\omega/k = 3.951342$ m/s.
On this patch it is the wave of index 10, and it needs $N \ge 32$.

## Correctness

The [proof](proofs/correctness.md) shows these facts in exact arithmetic, and the tests check them:

- **FFT.** The radix-2 FFT of the code equals the DFT.
- **Real height.** $H(-k, t) = \overline{H(k, t)}$ for every $k$ and $t$, so the inverse DFT is real. With the Nyquist row and column set to 0, the displacement is real too.
- **The sum.** At the grid points, the inverse 2D DFT of line L4 equals the sum $\sum_k H(k, t) e^{ik\cdot x}$ with the signed wave vectors.
- **One wave.** A single $h_0(k)$ gives the height $2\operatorname{Re}(h_0(k) e^{i(k\cdot x + \omega t)})$, a cosine wave that runs at the speed $\omega/|k|$.
- **Statistics.** The mean height is 0, and the expected square height is $\sum_k 2P(k)$ at every point and every time.

Whether the result looks like a real sea is not a claim of this page; it depends on the spectrum.

## Complexity

Line L1 costs $O(N^2)$ once.
Each frame costs $O(N^2)$ for line L3 and $O(N^2 \log N)$ for each 2D FFT of lines L4 and L5: $N$ row transforms and $N$ column transforms of length $N$.
The memory is $O(N^2)$.
A direct sum would cost $O(N^4)$ per frame.
The FFTs are the main cost, and they run well on a GPU.

## Properties

- **Periodic.** The height is periodic with the period $L$ in $x$ and in $y$, because every wave vector is a multiple of $2\pi/L$ (proved). The patch tiles with no seam, but the repetition can show from far away.
- **No simulation.** Each frame comes from $h_0$ and $t$ alone, so any frame can be made at once, in any order (proved from the formula).
- **Dispersion.** Each wave runs at the deep water phase speed $(g/|k|)^{1/2}$, so long waves overtake short ones (a law of the model).
- **Stationary statistics.** The expected square height does not depend on $t$ (proved). One random ocean still changes its RMS height a little in time (measured).
- **Both directions.** $P(k) = P(-k)$, so the code makes as many waves that run against the wind as with it (proved from the formula).
- **Peak.** Along the wind, $P$ is largest at $|k|\ell = 1/\sqrt 2$, the wavelength $2\pi\sqrt 2\, \ell$, which is 90.6 m for $V = 10$ m/s (proved).

## Variants and improvements

- **Other spectra.** Measured ocean spectra such as JONSWAP or Pierson-Moskowitz in place of Phillips give other shapes of the sea. Each is a fit to measurements.
- **Finite depth.** $\omega^2 = g k \tanh(k d)$ for the depth $d$ slows the long waves. The code has this as an option of its dispersion function.
- **Looping in time.** Rounding each $\omega$ to a multiple of $2\pi/T$ makes the animation repeat with the period $T$.
- **Small wave cut.** A factor $e^{-|k|^2 s^2}$ removes waves much shorter than $s$; the code has it as the option `small`.
- **One direction.** Setting $P(k) = 0$ for $\hat k\cdot\hat w < 0$ removes the waves that run against the wind.
- **Cascades.** Several patches of different sizes, added together, hide the repetition of one patch.
- **Normals and foam.** The slope $\nabla h$ is one more inverse FFT of $i k H$. The Jacobian of $x \mapsto x + D$ falls below 0 where the choppy surface folds, which is a common place to put foam.

## When to use it

Use FFT ocean synthesis for open deep water seen from a ship, a plane or a shore far away, where the waves are not affected by objects.
For a few wave trains with direct control, [Gerstner waves](/gerstner-waves/) are simpler.
For water that reacts to objects or to a coast, use [height field water](/height-field-water/) or the [shallow water equations](/shallow-water-equations/), maybe on top of this method.

## Pitfalls

- **Height not real.** If line L3 uses only $h_0(k) e^{i\omega t}$, without the partner term, $H$ is not Hermitian and the inverse FFT has a large imaginary part.
- **Wrong wave vectors.** The FFT stores the negative frequencies in the upper half of the indices. Using the index $n$ in place of $n - N$ for $n \ge N/2$ in lines L1 and L3 gives wrong speeds and wrong directions.
- **The Nyquist row.** At the index $N/2$, $k$ and $-k$ are the same grid point, and the factor $-ik/|k|$ of line L5 is not odd there, so the displacement gets an imaginary part. Set $h_0$ to 0 there, as the code does.
- **Scale of the FFT.** Some FFT libraries divide the inverse by $N^2$. Then the amplitudes in line L1 must be multiplied by $N^2$, or the waves are far too small.
- **Too much chop.** A large $\lambda$ in line L5 folds the surface over itself near the crests.
- **Patch size and wind speed do not match.** The longest wave on the patch is $L$ and the shortest is $2L/N$. If the peak wavelength $2\pi\sqrt 2\,\ell$ of line L1 is longer than $L$, the main waves of the spectrum are not on the grid.

## Implementations

## History

Mastin, Watterberg and Mareda (1987) made images of the sea by filtering white noise with an ocean wave spectrum and then inverting it with an FFT.
Tessendorf wrote the method in the form used today in his SIGGRAPH course notes "Simulating Ocean Water", with the Phillips spectrum, the time evolution by the dispersion relation and the choppy displacement.
The notes appeared in several versions; this page cites the 2001 version.
The method is now a common way to make ocean surfaces in films and games.

## References
