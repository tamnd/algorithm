---
tag: P3DHGZ
kind: algorithm
slug: b-mode-image-formation
name: B-mode image formation
aliases:
- brightness mode imaging
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: intro
summary: "Turn beamformed ultrasound RF lines into a gray-scale image: detect the envelope of each line, compensate the loss with depth, compress on a log scale and map the lines to pixels."
model: real-ram
complexity:
  vars: {K: the number of lines, n: the number of samples per line, P: the number of output pixels}
  time: {worst: O(K n log n + P)}
  space: {extra: O(n)}
properties: {deterministic: true, linear_in_data: false, recursive: false, exact: true}
prereqs: [pulse-echo-imaging, delay-and-sum-beamforming, analytic-signal]
see_also: [hilbert-transform, speckle, dynamic-receive-focusing, plane-wave-compounding, bilinear-interpolation, fast-fourier-transform, image-noise, coherence-factor]
sources:
  - book: isbn:9780123964878
    title: "Thomas L. Szabo, Diagnostic Ultrasound Imaging: Inside Out, 2nd edition, Academic Press, 2014"
    locator: "Chapter 10, Imaging systems and applications (signal processing chain, envelope detection, compression and scan conversion); Chapter 4, Attenuation (depth gain)"
---

B-mode (brightness mode) image formation turns the beamformed radio frequency (RF) lines of an ultrasound scan into the gray-scale image that a user sees. Each line is the output of a beamformer, for example [delay-and-sum](/delay-and-sum-beamforming/) with [dynamic receive focusing](/dynamic-receive-focusing/), along one beam direction. The RF line oscillates at the transmit frequency, so the brightness comes from its envelope, the modulus of the [analytic signal](/analytic-signal/) built with the [Hilbert transform](/hilbert-transform/). A depth-dependent gain, time gain compensation, offsets the attenuation of the tissue. The envelope spans a range of about 60 dB or more between strong and weak echoes, so it is compressed on a log scale to the 256 gray levels of a display. Last, scan conversion maps the lines, given in depth and angle for a sector scan, to the pixels of a Cartesian image. The depth of a sample at time $t$ is $z = c t / 2$, because the echo travels down and back.

## In plain words

The scanner sends a pulse along one direction and records the echoes over time. Echoes from deeper places come back later, so time tells depth. The recording wiggles up and down very fast; what matters is how strong the wiggles are, so you trace their outline, the envelope. Deep echoes are weaker because sound loses energy on the way, so you turn up the gain with depth. Strong echoes are many thousands of times stronger than weak ones, so you use a log scale, as in decibels, before you turn strength into brightness. Finally, the recordings fan out from the probe, so you redraw them on a square grid of pixels.

## The problem

The input is $K$ real RF lines $x_k = (x_k[0], \ldots, x_k[n-1])$, one for each beam angle $\theta_k$ of a sector scan, sampled at the times $t_0 + q/f_s$. The parameters are the speed of sound $c$, a dynamic range $D$ in dB, an optional gain $G$ in dB per mm and an output grid of pixels $(x, z)$. The output is a gray level in $\{0, \ldots, 255\}$ for every pixel; pixels outside the sector are $0$.

## The algorithm

```pseudo id=main
B-MODE(x_1 … x_K, D, G)                    ▷ returns gray levels per line and sample
L1  for each line k do
L2      X ← DFT(x_k)
L3      a ← IDFT(h · X)                    ▷ h: 1 at 0 and n/2, 2 for positive, 0 for negative frequencies
L4      e_k ← |a|                          ▷ envelope
L5      e_k[q] ← e_k[q] · 10^{G z_q / 20}  ▷ time gain compensation, z_q = c (t_0 + q/f_s)/2
L6  e_max ← max over all k, q of e_k[q]
L7  d ← 20 log10(e_k[q] / e_max)          ▷ for every k, q
L8  d ← max(-D, d)                         ▷ clip to the dynamic range
L9  ℓ_k[q] ← ⌊255 (d + D)/D + 1/2⌋

SCAN-CONVERT(ℓ, θ_1 … θ_K, z_0 … z_{n-1}, pixels)
L10 for each pixel (x, z): r ← √(x² + z²), θ ← atan2(x, z)
L11 if (θ, r) is outside the grid of angles and depths then the pixel is 0
L12 else the pixel is the bilinear interpolation of ℓ at (θ, r) from the 4 nearest samples
```

Lines L2 and L3 compute the analytic signal of the line in the frequency domain; its real part is the line itself. Line L5 runs only when a gain is given. The log mapping of L6 to L9 is relative to the brightest value of the whole image. Scan conversion uses [bilinear interpolation](/bilinear-interpolation/) in the polar grid; the angles and depths must be evenly spaced.

## Example

**Log compression.** With $D = 40$ dB, the envelope values $1, 0.1, 0.01, 0.001, 0$ give $0, -20, -40, -60, -\infty$ dB, the clip of L8 gives $0, -20, -40, -40, -40$, and L9 gives the gray levels $255, 128, 0, 0, 0$. Every echo more than 40 dB below the brightest one is black.

**Depth axis.** With $t_0 = 6.5$ us, $f_s = 40$ MHz, $n = 64$ and $c = 1.54$ mm/us, the samples cover the depths from $1.54 \cdot 6.5 / 2 = 5.005$ mm to $6.218$ mm, in steps of $c/(2 f_s) = 0.01925$ mm.

**A point scatterer.** The tests simulate 21 lines from $-20$ to $20$ degrees in steps of 2 degrees, a Gaussian pulse at $f_0 = 5$ MHz with $\sigma_t = 0.1$ us, and a crude beam model with a Gaussian angular weight of width 2 degrees. A scatterer at depth 5.6 mm and angle 4 degrees is at $(x, z) = (0.391, 5.586)$ mm. On a grid with steps of 0.1 mm in $x$ and 0.05 mm in $z$, the brightest pixel of the converted image is at $(0.4, 5.6)$, with the gray level 252.5 after interpolation.

**Depth gain.** Two equal scatterers at 5.3 and 5.9 mm in a medium with an attenuation of 5 dB/mm one way differ by $2 \cdot 5 \cdot 0.6 = 6$ dB, which is 38 gray levels at $D = 40$ dB. A gain of $G = 10$ dB per mm of depth brings them to within one gray level.

## Correctness

The real part of the discrete analytic signal of L3 is the input line, because the weights $h_k + h_{-k}$ add to 2 at every frequency; for a tone with a whole number of cycles, the envelope is exactly the amplitude. The log mapping depends only on ratios to the brightest value, is monotone, maps the peak to 255 and everything at or below $-D$ dB to 0. Scan conversion is a convex combination of the four nearest samples and is exact for functions of the form $\alpha + \beta r + \gamma\theta + \delta r\theta$. The gain of L5 with $G = 2\alpha$ removes an attenuation of $\alpha$ dB per mm in the model. The proofs are in proofs/correctness.md.

For a pulse with a smooth envelope, the detected envelope is close to the true one but not equal, because the line is finite; the test measures an error of $6.4 \cdot 10^{-4}$ for a Gaussian pulse. This is a measurement, not a theorem.

## Complexity

In the real-RAM model, the envelope of a line of $n$ samples costs $O(n \log n)$ with a radix-2 FFT, so all lines cost $O(K n \log n)$. Lines L5 to L9 cost $O(K n)$, and scan conversion costs $O(1)$ per pixel, $O(P)$ in total. The extra space is $O(n)$ for one line. A real scanner computes the envelope with an IQ demodulator or a short Hilbert filter, at $O(1)$ per sample.

## Properties

- Not linear: the modulus and the logarithm destroy linearity. Speckle, the granular pattern of tissue, comes from the interference that the modulus makes visible; see [speckle](/speckle/).
- Scale invariant: multiplying the RF data by a constant does not change the image.
- The dynamic range $D$ and the gain curve are display choices. Values such as $D = 60$ dB are tuned for the eye and the tissue, not derived.
- The depth resolution is set by the pulse length, about $c\, \tau / 2$ for a pulse of duration $\tau$; the lateral resolution is set by the beamformer.

## Variants and improvements

- **IQ demodulation.** Mix the RF line with $e^{-i 2\pi f_0 t}$ and low-pass filter it, then take the modulus. This is the usual path in hardware and gives the same envelope for a narrow-band signal.
- **Compounding.** Spatial or frequency compounding averages envelopes of different angles or bands to lower the speckle contrast; [plane-wave compounding](/plane-wave-compounding/) sums before the envelope and does not.
- **Adaptive weights.** A [coherence factor](/coherence-factor/) or another adaptive beamformer changes the lines before this chain.
- **Other compression curves.** S-shaped and other gray maps are used in place of the pure log; they keep the order of the levels.
- **Linear arrays.** For parallel lines, scan conversion is a plain interpolation in $x$ and $z$, without the polar map.

## When to use it

B-mode image formation is the last step of almost every pulse-echo ultrasound system, whatever beamformer comes before it. Skip the log compression and the scan conversion when the data go to further processing, such as Doppler, elastography or quantitative backscatter estimation, which need the complex or linear values.

## Pitfalls

- **Wrong depth axis.** The depth is $c t / 2$, not $c t$.
- **Rectification in place of the envelope.** Taking $|x|$ of the RF line gives a rectified signal, not the envelope; use the analytic signal or IQ data.
- **Circular wrap.** The DFT treats the line as periodic, so a strong echo near one end leaks into the other end. Pad the line or use a finite Hilbert filter.
- **Log of zero.** A zero envelope has the level $-\infty$ dB; clip it, as line L8 does.
- **Nearest-neighbor scan conversion.** It gives jagged edges at depth, where the lines are far apart; use at least bilinear interpolation.
- **Gain too high.** Noise at depth grows with the gain and fills the image with a gray floor.

## Implementations

## History

Two-dimensional pulse-echo images of the body appeared in the 1950s, made with one transducer moved over the skin by a mechanical arm, and showed only bright echoes in black and white. Gray-scale display, with a log compression of the echo amplitude, came in the 1970s, together with real-time scanners that steer the beam electronically with arrays. Digital beamformers later moved the whole chain, envelope detection, compression and scan conversion, into software. The details of these steps are in textbooks such as Szabo (2014).

## References
