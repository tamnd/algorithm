---
tag: 6XWF0B
kind: algorithm
slug: active-constellation-extension
name: Active constellation extension
aliases:
- ACE
area: communications/ofdm-and-multicarrier
level: advanced
summary: "Lowers the PAPR of OFDM by moving the outer constellation points of each symbol outward, away from the decision boundaries. Decisions and distance margins are kept, and no side information is sent."
model: real-ram
complexity:
  vars: {N: the number of subcarriers, L: the oversampling factor, K: the number of iterations}
  time: {worst: O(K L N log(L N))}
  space: {extra: O(L N)}
properties: {deterministic: true, keeps_decisions: true, side_information: false, receiver_unchanged: true, adds_power: true}
history:
  year: 2003
  people: [Brian S. Krongold, Douglas L. Jones]
  note: "Krongold and Jones proposed active constellation extension in 2003, with a projection method and a faster gradient-project method."
prereqs: [peak-to-average-power-ratio, iterative-clipping-and-filtering, quadrature-amplitude-modulation]
see_also: [tone-reservation, selected-mapping, partial-transmit-sequence, projected-gradient-descent, minimum-distance-detector, convex-set, convex-function, fast-fourier-transform]
sources:
  - paper: doi:10.1109/TBC.2003.817088
    title: "Brian S. Krongold and Douglas L. Jones, PAR reduction in OFDM via active constellation extension, IEEE Transactions on Broadcasting 49(3), 2003, pages 258 to 268"
    locator: "the extension regions of the outer points of QPSK and QAM, the projection method and the gradient-project method"
  - paper: doi:10.1109/MWC.2005.1421929
    title: "Seung Hee Han and Jae Hong Lee, An overview of peak-to-average power ratio reduction techniques for multicarrier transmission, IEEE Wireless Communications 12(2), 2005, pages 56 to 65"
    locator: "the comparison of the reduction methods, including the methods that need no side information"
---

Active constellation extension (ACE) lowers the [peak-to-average power ratio](/peak-to-average-power-ratio/) (PAPR) of an [OFDM](/orthogonal-frequency-division-multiplexing/) symbol by moving some data points, but only in directions that cannot hurt the receiver. In a square [QAM](/quadrature-amplitude-modulation/) constellation, a point on the outer edge may move further out, away from the decision boundaries: the [minimum-distance detector](/minimum-distance-detector/) still decides the same point, and the distance to every other point can only grow. Each subcarrier therefore has a convex region of allowed positions. The algorithm clips the time signal, takes the in-band part of the clipping noise, adds it to the subcarrier values, and projects each value back onto its region. This is a projected gradient method on the clipped energy, like [clipping and filtering](/iterative-clipping-and-filtering/) with constraints that keep the data exact. Krongold and Jones proposed it in 2003. The page uses the unitary DFT pair $F[k, n] = e^{-j 2\pi k n / N}/\sqrt N$, $j$ is the imaginary unit, and the constellations have unit mean energy.

## In plain words

A receiver decides which point was sent by looking at which point is nearest. A point on the outer edge of the constellation can move further out and still be the nearest, and noise then has to push it even further to cause an error. ACE uses this freedom. It finds the tall peaks of the signal, works out how each tone should change to flatten them, and makes only the changes that move an outer point outward. Inner points stay where they are. It repeats this a few times. The receiver does not change at all and needs no extra information. The cost is a little more transmit power, because the moved points are further from the centre.

## The problem

The input is a block of $N$ points $X[0], \ldots, X[N-1]$ of a square QAM constellation, an oversampling factor $L$, usually 4, a clipping magnitude $A$, a step size $\mu$ and a number of iterations $K$. Each coordinate of a point at the outer level $\pm a_{\max}$ may grow in magnitude; each inner coordinate must stay fixed. This gives each subcarrier a region $E(X[k])$: a quadrant for a corner point, a half-line for an edge point and a single point for an inner point. The output is a vector $Y$ with $Y[k] \in E(X[k])$ and the oversampled symbol $x$ of $Y$, with a lower peak than the symbol of $X$.

## The algorithm

```pseudo id=main
ACE(X[0..N-1], constellation, L, A, μ, K)
L1  Y ← X
L2  x ← √L · F_LNᴴ (Y, with (L-1)N zeros in the middle)
L3  repeat K times
L4      e[t] ← (A/|x[t]| - 1) · x[t] if |x[t]| > A, else 0      ▷ clip(x, A) - x
L5      if e = 0 then stop
L6      E ← the N in-band values of F_LN e, divided by √L
L7      Y[k] ← the nearest point to Y[k] + μ E[k] in E(X[k]), for every k
L8      x ← √L · F_LNᴴ (Y, with (L-1)N zeros in the middle)
L9  return x, Y
```

Line L2 is the oversampled OFDM symbol; the zeros go in the middle of the spectrum because the indices $k \ge N/2$ are the negative frequencies. Line L4 computes the clipping noise, the change that would bring every sample above $A$ down to $A$. Line L6 takes its subcarrier values and drops its out-of-band part. Line L7 adds $\mu$ times these values to the current points and projects each point onto its region. The projection acts on the real and imaginary parts separately: an inner coordinate returns to its original value, and an outer coordinate is kept only if it moved outward. Line L8 forms the new symbol, which stays band-limited because it comes from $N$ subcarrier values. The receiver demodulates as usual.

## Example

Take $N = 64$ QPSK subcarriers, $L = 4$ and $A^2 = 10^{0.4}$, a clipping level 4 dB above the mean power. In QPSK every point is a corner point, so every subcarrier may move. For one block (Python `random.Random(1)`), plain OFDM has a PAPR of 6.94 dB. With $\mu = 2$, the PAPR after 1, 2, 4 and 8 passes is 6.41, 6.06, 5.65 and 5.28 dB. About 25 of the 64 subcarriers move, the largest move is 0.76 after 8 passes, and the mean power rises by 0.63 dB.

Over 200 random blocks (`random.Random(2)`), with the PAPR measured on $x$ and the added power in the mean:

| constellation | $\mu$ | passes $K$ | mean PAPR | 99 percent below | extra power |
|---|---|---|---|---|---|
| QPSK | | 0 | 7.39 dB | 9.48 dB | 0 dB |
| QPSK | 1 | 1 | 7.00 dB | 8.86 dB | 0.10 dB |
| QPSK | 1 | 4 | 6.26 dB | 7.77 dB | 0.30 dB |
| QPSK | 1 | 8 | 5.76 dB | 7.38 dB | 0.46 dB |
| QPSK | 2 | 1 | 6.61 dB | 8.17 dB | 0.20 dB |
| QPSK | 2 | 4 | 5.71 dB | 7.35 dB | 0.48 dB |
| QPSK | 2 | 8 | 5.30 dB | 6.93 dB | 0.66 dB |
| 16-QAM | | 0 | 7.42 dB | 10.08 dB | 0 dB |
| 16-QAM | 2 | 8 | 6.26 dB | 8.31 dB | 0.41 dB |

The step $\mu = 2$ reaches in 4 passes what $\mu = 1$ reaches in 8. 16-QAM gains less than QPSK, because its 4 inner points cannot move and its 8 edge points can move along one axis only.

## Correctness

The claim is that, after any number of passes, every $Y[k]$ lies in $E(X[k])$, so the receiver decides every $X[k]$ correctly without noise and every distance margin is at least as large as before; that $x$ is the exact band-limited symbol of $Y$; and that for $0 < \mu \le 2$ the clipped energy $\frac12 \sum_t (|x[t]| - A)_+^2$ never increases. The invariant is $Y[k] \in E(X[k])$ and $x = T(Y)$, which line L7 and line L8 keep. Each region is a [convex set](/convex-set/), and on each axis the outer point moves away from every other point, so all distances grow. Line L7 is a step of [projected gradient descent](/projected-gradient-descent/) on the clipped energy as a function of $Y$, with step $\mu/L$, and that gradient is $L$-Lipschitz, so the descent lemma gives the monotone decrease for $\mu \le 2$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Each pass costs one FFT and one inverse [FFT](/fast-fourier-transform/) of size $LN$, $O(LN\log(LN))$, plus $O(LN)$ for the clipping and $O(N)$ for the projections. One block costs $O(K L N \log(L N))$ operations in the real-RAM model, with $O(LN)$ memory. For $N = 64$, $L = 4$ and $K = 4$ this is 8 transforms of size 256 per symbol, against one for plain OFDM.

## Properties

- **Keeps decisions.** No moved point crosses a decision boundary, and its distance to every other point does not shrink.
- **Receiver unchanged.** The receiver needs no side information and no new processing.
- **Band-limited.** The output is always the symbol of $N$ subcarrier values, with no out-of-band clipping noise.
- **Adds power.** The moved points are further from the origin; 0.1 to 0.7 dB in the example.
- **Weaker for dense constellations.** Only the outer points move, a smaller share in 16-QAM and 64-QAM.
- **Monotone clipped energy.** For $\mu \le 2$ the clipped energy never increases. The peak itself is not guaranteed to fall in every pass.

## Variants and improvements

- **Step-size control.** Krongold and Jones also give a gradient-project method that chooses the step size on each pass instead of using a fixed one.
- **Power limit.** Bound how far a point may move, or the total added power, by adding a constraint to each region; the regions stay convex.
- **Combined with tone reservation.** Free tones can be added as regions equal to the whole plane, which joins ACE and [tone reservation](/tone-reservation/) in one method.
- **Standards.** The DVB-T2 broadcasting standard includes ACE as an option.

## When to use it

Use ACE when the receiver must not change, no side information can be sent, and no subcarriers can be spared for [tone reservation](/tone-reservation/). It works best with QPSK and small QAM. For 64-QAM and above, most points are inner points and the gain falls. If side information is acceptable, [selected mapping](/selected-mapping/) and [partial transmit sequences](/partial-transmit-sequence/) cost no power.

## Pitfalls

- **Moving inner points.** If line L7 lets an inner coordinate move, the point can cross a decision boundary and the data are lost. In line L7 an inner coordinate must return to its original value.
- **Projecting the step instead of the point.** If line L7 keeps only the outward part of the step $\mu E[k]$, a point that moved out can never move back, even when a later pass asks for it, and the added power only grows. Project the sum $Y[k] + \mu E[k]$ onto $E(X[k])$ in line L7, which lets a point move back toward its original position.
- **Keeping the out-of-band noise.** Using $\mathrm{clip}(x, A)$ itself as the new symbol after line L4 puts clipping noise outside the band. Take only the in-band values in line L6 and rebuild the symbol in line L8.
- **A step that is too large.** With $\mu > 2$ in line L7, the clipped energy can grow from one pass to the next. Keep $0 < \mu \le 2$ in line L7, or choose the step by a line search.
- **Nyquist-rate samples.** Line L2 with $L = 1$ clips the sampled peaks only, and the analog peaks between them remain. Use $L \ge 4$ in lines L2 and L8.

## Implementations

## History

Krongold and Jones published active constellation extension in 2003, with a method based on projections onto the extension regions and a faster gradient-project method. The method rests on the fact that the outer points of a constellation can move outward without loss. The allowed regions are convex, so peak reduction becomes a convex problem with no side information and no change at the receiver. The overview of Han and Lee (2005) places ACE among the methods that keep the receiver unchanged. ACE later became an option in the DVB-T2 broadcasting standard, together with tone reservation.

## References
