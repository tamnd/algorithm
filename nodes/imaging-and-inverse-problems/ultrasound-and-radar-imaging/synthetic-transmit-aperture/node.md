---
tag: 065Q29
kind: technique
slug: synthetic-transmit-aperture
name: Synthetic transmit aperture imaging
aliases:
- STA imaging
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Fire one element at a time, record on all elements, and beamform every pixel from all pairs. The image is focused on transmit and on receive at every point, at the cost of M firings per frame."
prereqs: [dynamic-receive-focusing]
see_also: [total-focusing-method, saft, plane-wave-compounding, delay-and-sum-beamforming, walsh-hadamard-transform, coherence-factor, b-mode-image-formation, synthetic-aperture-radar]
sources:
  - paper: doi:10.1016/j.ultras.2006.07.017
    title: "Jorgen Arendt Jensen, Svetoslav Ivanov Nikolov, Kim Lokke Gammelmark and Morten Hogholm Pedersen, Synthetic aperture ultrasound imaging, Ultrasonics 44 (supplement), 2006, e5 to e15"
    locator: "synthetic transmit aperture imaging, low and high resolution images, virtual sources, coded and spatially encoded transmits, and motion (general locator)"
  - paper: doi:10.1109/58.384453
    title: "Mustafa Karaman, Pai-Chi Li and Matthew O'Donnell, Synthetic aperture imaging for small scale systems, IEEE Transactions on Ultrasonics, Ferroelectrics, and Frequency Control 42(3), 1995, 429 to 442"
    locator: "synthetic aperture schemes with single elements and subapertures on transmit, and their signal-to-noise ratio (general locator)"
  - paper: doi:10.1016/j.ndteint.2005.04.002
    title: "Caroline Holmes, Bruce W. Drinkwater and Paul D. Wilcox, Post-processing of the full matrix of ultrasonic transmit-receive array data for non-destructive evaluation, NDT and E International 38(8), 2005, 701 to 711"
    locator: "the same acquisition and summation in nondestructive testing, as full matrix capture and the total focusing method (general locator)"
---

Synthetic transmit aperture (STA) imaging builds the transmit focus of an ultrasound array after the scan. In conventional imaging, all elements fire together with delays that focus the pulse at one depth, and [dynamic receive focusing](/dynamic-receive-focusing/) handles the receive side. STA instead fires one element at a time and records the echoes on all $M$ elements. After $M$ firings, the system has the trace $r_{ij}$ of every transmit element $i$ and receive element $j$. For each pixel $p$ it sums these traces at the two-way times $(|p - e_i| + |p - e_j|)/c$. This is the delay that a transmit focused exactly at $p$ would need, so every pixel is focused on transmit and on receive. The image of one firing is a low-resolution image, focused on receive only, and their coherent sum is the high-resolution image. The price is $M$ firings per frame and a low signal-to-noise ratio, because only one small element transmits. In nondestructive testing the same acquisition is called full matrix capture and the sum the [total focusing method](/total-focusing-method/).

## In plain words

A normal scanner focuses its pulse by firing all elements with small delays, so the sound meets at one depth. Everywhere else the pulse is wide. Synthetic aperture turns this around. Fire one element alone, so the sound spreads everywhere, and record what all elements hear. Repeat with the next element, and so on. Now you have a recording for every pair of a sender and a listener. For any point you can compute after the fact what a pulse focused at exactly that point would have given: shift each recording by the right time and add them all up. Every point gets its own perfect focus, but you must wait for one firing per element.

## When it applies

STA needs an array whose elements can fire one at a time and whose channels can all be stored, and a target that does not move much during the $M$ firings. It assumes the [pulse-echo model](/pulse-echo-imaging/) with a known speed of sound. It fits shallow imaging, where each firing is short and the elements are close to the target, research systems with full channel access, and nondestructive testing of static parts. It fits poorly for deep imaging, where one element gives too little energy, and for fast motion, such as the heart, without motion compensation.

## The template

```pseudo id=main
STA(r_ij for i, j = 1 … M, e_1 … e_M, pixels, c)   ▷ r_ij: transmit i, receive j
L1  for each pixel p do
L2      acc ← 0
L3      for i ← 1 to M do                           ▷ each firing gives a low-resolution image
L4          for j ← 1 to M do
L5              acc ← acc + w_ij(p) · SAMPLE(r_ij, (|p - e_i| + |p - e_j|) / c)
L6      I(p) ← |acc|                                ▷ the high-resolution image
```

The weights $w_{ij}$ are apodizations on transmit and receive, often with an f-number on both sides. SAMPLE interpolates the trace at the exact time, as on the [TFM](/total-focusing-method/) page, which proves that the sum is linear, that its peak for a point scatterer is at the scatterer, and that its cost is $O(M^2 n^2)$ for an $n \times n$ image. By reciprocity, $r_{ij} = r_{ji}$ in the model, so only $M(M+1)/2$ distinct traces are needed: 136 of the 256 traces for $M = 16$.

## Classic examples

**The frame time.** For a depth of 60 mm and $c = 1.54$ mm/us, one firing waits $120/1.54 = 77.92$ us. With $M = 128$ elements, STA needs $128$ firings, $9.97$ ms per frame, about 100 frames per second. This is the same as 128 focused lines, but each STA frame is focused at every depth.

**The data volume.** One frame holds $M^2$ traces: 256 for $M = 16$, 16384 for $M = 128$. With 2000 samples per trace, the latter is about 33 million samples per frame, which is why STA was long a research method.

**Recursive imaging.** Each new firing replaces the oldest low-resolution image in the sum, so a new high-resolution image is available after every firing, not every $M$ firings. Motion between the firings still enters the sum.

**Sparse transmit.** Fire only every $k$-th element. The frame needs $M/k$ firings, and the transmit aperture is sampled more coarsely, which raises the grating lobes of the transmit side.

**Relation to SAFT and plane waves.** [SAFT](/saft/) uses only the diagonal pairs $i = j$, the case of one moving element. [Plane-wave compounding](/plane-wave-compounding/) fires all elements in each firing with linear delays; in the model its traces are sums of time-shifted STA traces, and $N$ angles give a frame with fewer firings.

## Variations

- **Multi-element subapertures and virtual sources.** Several elements fire together, with delays that focus at a point in front of or behind the array. The point acts as a virtual source, with more energy than one element; the transmit time in L5 is computed from the virtual source (Karaman, Li and O'Donnell 1995 used subapertures).
- **Spatial encoding.** All elements fire in each of $M$ firings with signs from the rows of a Hadamard matrix. Decoding with the [Walsh-Hadamard transform](/walsh-hadamard-transform/) recovers the single-element traces. In the model with additive white noise and no motion, the decoded traces have $M$ times less noise variance than single-element firings, because each firing uses all elements. This is a theorem for that model; motion and nonlinear effects break the decoding.
- **Coded excitation.** Long coded pulses, such as chirps, with [pulse compression](/pulse-compression/) on receive raise the energy per firing.
- **Adaptive combination.** The sum over pairs can be weighted by a [coherence factor](/coherence-factor/), or replaced by [delay-multiply-and-sum](/delay-multiply-and-sum/) or the [Capon beamformer](/capon-beamformer/).

## Pitfalls

- **Motion.** The firings are spread over the frame time, so a moving target changes the phase of the low-resolution images and the coherent sum loses its gain. Use fewer firings, recursive imaging with motion compensation, or plane waves.
- **Low energy.** One small element sends little energy, and the echoes from deep tissue fall below the noise. Use virtual sources, spatial encoding or coded pulses.
- **Directivity.** A single element has a wide but not uniform beam; pixels at large angles get little energy and should be weighted down or left out.
- **Time origin.** The time in L5 assumes that each firing starts at $t = 0$ at the element. With virtual sources, the origin is at the virtual source, and a sign error in the time puts the transmit focus in the wrong place.
- **Data rate.** Storing all $M^2$ traces needs hardware that many systems do not have.

## Exercises

1. Show that, in the pulse-echo model with point elements, the sum of L5 over $i$ and $j$ can use only the pairs $i \le j$ with a weight of $2$ for $i < j$, and count the traces for $M = 16$. (The delay is symmetric in $i$ and $j$ and $r_{ij} = r_{ji}$; $16 \cdot 17 / 2 = 136$.)
2. For a depth of 40 mm and $M = 64$ elements, compute the frame time of STA and of plane-wave compounding with 9 angles. (One firing is $80/1.54 = 51.9$ us, so STA takes $3.32$ ms and 9 plane waves $0.47$ ms.)
3. Let $H$ be an $M \times M$ Hadamard matrix with $H^T H = M I$, and let the encoded data be $y = H x + n$ with independent noise of variance $\sigma^2$ in each entry. Show that the decoded data $\frac{1}{M} H^T y$ equal $x$ plus noise of variance $\sigma^2 / M$ in each entry.

## References
