---
tag: 6A2CCM
kind: algorithm
slug: parks-mcclellan-algorithm
name: Parks-McClellan algorithm
aliases:
- Remez exchange filter design
- equiripple FIR design
area: graphics-and-signals/signal-processing
level: advanced
summary: "Find the linear phase FIR filter of a given length with the smallest largest weighted error in its bands. It uses the Remez exchange, and the best error has equal ripples of alternating sign."
solves: [digital-filter-design]
model: real-ram
complexity:
  vars: {N: the number of taps (N = 2L + 1), L: the degree of the amplitude, G: the number of grid points, I: the number of iterations}
  time: {worst: O(I L G), average: O(I L G), best: O(L G), per_sample: O(N)}
  space: {extra: O(G)}
properties: {causal: true, stable: true, linear_phase: true, optimal: "minimax on the grid", deterministic: true, iterative: true}
history:
  year: 1972
  people: [Thomas W. Parks, James H. McClellan]
  note: Parks and McClellan showed in 1972 that the optimal linear phase FIR filter with fixed band edges is a Chebyshev approximation problem and solved it with the Remez exchange. The program of McClellan, Parks and Rabiner of 1973 made the method the standard FIR design tool.
prereqs: [fir-filter, remez-algorithm, chebyshev-equioscillation-theorem]
see_also: [minimax-approximation, digital-filter-design, barycentric-interpolation, chebyshev-polynomials, window-functions, iir-filter, linear-programming-problem, gibbs-phenomenon]
sources:
  - paper: doi:10.1109/TCT.1972.1083419
    title: Thomas W. Parks and James H. McClellan, Chebyshev Approximation for Nonrecursive Digital Filters with Linear Phase, IEEE Transactions on Circuit Theory 19(2), 1972
    locator: pp. 189 to 194 (the filter design as weighted Chebyshev approximation, the alternation theorem and the exchange algorithm)
  - paper: "James H. McClellan and Thomas W. Parks, A Program for the Design of Linear Phase Finite Impulse Response Digital Filters, IEEE Transactions on Audio and Electroacoustics 20(3), 1972, pages 195 to 199"
    locator: the first program for the exchange algorithm
  - paper: doi:10.1109/TAU.1973.1162525
    title: James H. McClellan, Thomas W. Parks and Lawrence R. Rabiner, A Computer Program for Designing Optimum FIR Linear Phase Digital Filters, IEEE Transactions on Audio and Electroacoustics 21(6), 1973
    locator: pp. 506 to 526 (the four types of linear phase filters, the dense grid, the barycentric formulas and the program)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 7.7, Optimum Approximations of FIR Filters (the alternation theorem for low-pass filters and the Parks-McClellan algorithm)
---

The Parks-McClellan algorithm designs a linear phase [FIR filter](/fir-filter/) with $N$ taps whose frequency response is as close as possible to an ideal one, in the minimax sense. The user gives the band edges and a weight for each band. The algorithm finds the taps that minimize the largest weighted error over the pass band and the stop band. Thomas Parks and James McClellan saw in 1972 that this is a weighted [minimax approximation](/minimax-approximation/) problem for a cosine polynomial, and they solved it with the [Remez exchange algorithm](/remez-algorithm/). By the [Chebyshev equioscillation theorem](/chebyshev-equioscillation-theorem/), the optimal error has equal ripples that alternate in sign, so these filters are also called equiripple filters. Frequencies on this page are $\omega$ in radians per sample, $\omega \in [0, \pi]$, because the amplitude is even in $\omega$.

## In plain words

You want a filter that passes low tones and stops high tones, with a gap between the two bands where you do not care. A filter with a fixed number of taps cannot do this exactly, so its response has small waves around the ideal values. This method finds the filter whose worst wave is as small as possible.

The best filter has a clear signature: all its biggest waves have the same height, and they go up and down in turn. The method guesses where the biggest waves are, finds the filter whose waves at those places have equal height, then looks where the waves of that filter really peak and moves the guesses there. After a few rounds the guesses stop moving and the filter is the best one.

## The problem

This page treats the type 1 low-pass case: $N = 2L + 1$ taps with $h[n] = h[N - 1 - n]$. Then $H(e^{i\omega}) = e^{-iL\omega} A(\omega)$ with the real amplitude

$$A(\omega) = \sum_{k=0}^{L} a_k \cos(k\omega), \qquad a_0 = h[L], \quad a_k = 2h[L - k].$$

The input is $N$, the pass band edge $\omega_p$, the stop band edge $\omega_s$ with $0 < \omega_p < \omega_s < \pi$, and a stop band weight $K > 0$. Let $F = [0, \omega_p] \cup [\omega_s, \pi]$. The desired response is $D = 1$ with weight $W = 1$ on $[0, \omega_p]$, and $D = 0$ with weight $W = K$ on $[\omega_s, \pi]$. The weighted error is $E(\omega) = W(\omega)\big(D(\omega) - A(\omega)\big)$. The task is to find $a_0, \ldots, a_L$ that minimize $\max_{\omega \in F} |E(\omega)|$. The transition band $(\omega_p, \omega_s)$ is not part of $F$.

If the optimum is $\delta^*$, the pass band ripple is $\delta_p = \delta^*$ and the stop band ripple is $\delta_s = \delta^*/K$. So $K = \delta_p/\delta_s$ sets the ratio of the two ripples. The length $N$ sets their size. In practice $F$ is replaced by a dense grid of about $16(L + 1)$ points.

With $x = \cos\omega$, $\cos(k\omega) = T_k(x)$ is a [Chebyshev polynomial](/chebyshev-polynomials/), so $A$ is an ordinary polynomial of degree $L$ in $x$. The problem is the weighted Chebyshev approximation of $D$ on the compact set $\cos(F) \subset [-1, 1]$ by polynomials of degree $L$. Polynomials of degree $L$ satisfy the Haar condition, so the alternation theorem applies: $A$ is optimal if and only if there are $L + 2$ points $\omega_0 < \cdots < \omega_{L+1}$ in $F$ with $E(\omega_j) = \pm(-1)^j \max_F |E|$. The optimum is unique.

This is one method of [digital filter design](/digital-filter-design/).

## The algorithm

The algorithm keeps a reference set $R$ of $L + 2$ frequencies. On $R$ it solves for the polynomial whose error has equal size $|\delta|$ and alternating signs. Then it moves $R$ to the local extrema of that error. This is the multiple exchange version of the [Remez algorithm](/remez-algorithm/), with the formulas in [barycentric](/barycentric-interpolation/) form.

```pseudo id=main
PARKS-MCCLELLAN(N = 2L + 1, ωp, ωs, K)          ▷ grid F, D and W as in the problem; x_k = cos ω_k
L1  R ← L + 2 grid points spread evenly over F   ▷ R = {ω_0 < ω_1 < … < ω_{L+1}}
L2  repeat
L3      δ ← Σ_k b_k D(ω_k) / Σ_k b_k (−1)^k / W(ω_k)      ▷ b_k = 1 / Π_{i ≠ k} (x_k − x_i)
L4      A ← the polynomial in x of degree L with A(ω_k) = D(ω_k) − (−1)^k δ / W(ω_k)
L5      E(ω) ← W(ω) (D(ω) − A(ω)) for every ω in F
L6      C ← the local extrema of E in each band, with the band edges as end points
L7      in each run of neighbours of C with the same sign of E, keep only the one with the largest |E|
L8      while |C| > L + 2 do remove the end point of C with the smaller |E|
L9      if C = R or max_F |E| − |δ| ≤ ε · max_F |E| then stop
L10     R ← C
L11 h ← the N taps of A, from the inverse DFT of the N samples A(2πj/N)
```

Line L3 solves the $L + 2$ linear equations $A(\omega_k) + (-1)^k \delta / W(\omega_k) = D(\omega_k)$ for the unknown $\delta$ without solving for $a_0, \ldots, a_L$. It uses the fact that the divided difference of order $L + 1$ of a polynomial of degree $L$ is zero. Line L4 passes a polynomial of degree $L$ through $L + 1$ of the values; it is evaluated in barycentric form, and it also takes the right value at the last point. Lines L6 to L8 pick the new reference set: at most one point per ripple, alternating signs, and $L + 2$ points that keep the largest errors. Line L9 stops when the set does not change or the largest error on the grid is the levelled error $|\delta|$.

## Example

Take $N = 13$ ($L = 6$), $\omega_p = 0.4\pi$, $\omega_s = 0.6\pi$, $K = 1$, and a grid of $16(L + 1) = 112$ points. The reference set has $L + 2 = 8$ points. The levelled error and the reference set after each exchange are

| iteration | $\lvert\delta\rvert$ | new reference set $/\pi$ |
|---|---|---|
| 1 | 0.01072 | 0, 0.145, 0.291, 0.4, 0.6, 0.709, 0.855, 1 |
| 2 | 0.04429 | 0, 0.167, 0.327, 0.4, 0.6, 0.673, 0.833, 1 |
| 3 | 0.05083 | 0, 0.175, 0.327, 0.4, 0.6, 0.673, 0.825, 1 |
| 4 | 0.05086 | the same set, so it stops |

The levelled error grows at each step, as the theory says. The final filter is

$$h \approx (0,\ 0.0537,\ 0,\ -0.0915,\ 0,\ 0.3132,\ 0.5,\ 0.3132,\ 0,\ -0.0915,\ 0,\ 0.0537,\ 0).$$

Its error is $\pm 0.05086$ at all eight reference points, with alternating signs: four in the pass band, including $\omega = 0$ and the edge $0.4\pi$, and four in the stop band, including the edge $0.6\pi$ and $\pi$. On a grid of 20001 points the largest error is 0.050906, within 0.1 percent of $|\delta|$. The stop band is about $-25.9$ dB. Because the bands are symmetric about $\pi/2$ and $K = 1$, the filter is a half-band filter: $A(\pi/2) = 1/2$, and every second tap except the center is zero. The two outer taps are zero, so 11 taps give the same filter.

**Three taps.** For $N = 3$ ($L = 1$), $A(\omega) = a_0 + a_1\cos\omega$. With $\omega_p = 0.3\pi$, $\omega_s = 0.7\pi$ and $c = \cos(0.3\pi)$, the optimum is $a_0 = 1/2$, $a_1 = 1/(1 + c)$ and $\delta^* = (1 - c)/(2(1 + c)) \approx 0.12981$. The three extremal frequencies are $0.3\pi$, $0.7\pi$ and $\pi$. The algorithm finds the same value.

## Correctness

Two facts make the algorithm correct. First, for any reference set with alternating signs, the levelled error $|\delta|$ is a lower bound for the optimum: no polynomial of degree $L$ can have an error smaller than $|\delta|$ at all $L + 2$ points, because the difference of the two polynomials would change sign $L + 1$ times. This is the theorem of de la Vallée Poussin. The largest error of the current $A$ is an upper bound. So at every step

$$|\delta| \;\le\; \delta^* \;\le\; \max_F |E|,$$

and when line L9 stops with the two sides equal, $A$ is optimal on the grid, by the alternation theorem. Second, the exchange keeps alternating signs and errors of at least $|\delta|$ on the new set, so the next $|\delta|$ is a weighted average of those errors and it does not decrease. The full proofs are in the proof file. Optimality holds on the grid; on the continuous bands the error is larger by an amount that falls as the grid gets denser.

## Complexity

The cost model is real arithmetic operations. Let $G$ be the number of grid points, about $16(L + 1)$, and $I$ the number of iterations.

- **One iteration.** The barycentric weights $b_k$ cost $O(L^2)$. Evaluating $A$ on the grid costs $O(L)$ per point, so lines L5 and L6 cost $O(LG)$. This dominates, and it is $O(L^2)$ for the usual grid.
- **Iterations.** The number $I$ has no simple bound, but the method converges fast in practice. The example stops after four iterations.
- **Taps.** Line L11 costs $O(N^2)$ with direct sums, or $O(N \log N)$ with the [fast Fourier transform](/fast-fourier-transform/).
- **Using the filter.** The result is an FIR filter of $N$ taps, so it costs $N$ multiplies per output sample, or $L + 1$ if the symmetric pairs are added first.

For the same ripples and transition band the equiripple filter is shorter than a filter designed by [window functions](/window-functions/), because the window method gives the same ripple in both bands, and its error is large only near the band edges, so it is smaller than needed in the rest of the bands.

## Properties

- **Optimal.** For the given $N$, band edges and weights, no linear phase filter has a smaller largest weighted error on the grid.
- **Equiripple.** The optimal error has at least $L + 2$ alternations. A low-pass type 1 filter can have $L + 3$; such filters are called extraripple filters.
- **Linear phase, causal and stable.** The result is a symmetric FIR filter. It delays all frequencies by $L$ samples.
- **Not maximally flat.** The pass band has ripples of size $\delta_p$. For a flat pass band, see the [Butterworth filter](/butterworth-filter/) or a maximally flat FIR design.
- **Trade off.** More taps lower the error. For $\omega_p = 0.3\pi$ and $\omega_s = 0.5\pi$ the optimal $|\delta|$ is about 0.0813 for 9 taps, 0.0407 for 13, 0.0115 for 21 and 0.0019 for 31.

## Variants and improvements

- **Other types and shapes.** The program of 1973 handles the four linear phase types, any number of bands, differentiators and Hilbert transformers. Types 2 to 4 factor out $\cos(\omega/2)$, $\sin\omega$ or $\sin(\omega/2)$ and approximate a modified $D/Q$ with weight $WQ$.
- **Estimating the length.** Kaiser's empirical formula gives the length for given $\delta_p$, $\delta_s$ and transition width. The design is run and $N$ is changed until the ripples are met.
- **Linear programming.** The same minimax problem on a grid is a [linear program](/linear-programming-problem/). This is slower but allows extra constraints, such as a value at one frequency.
- **Constrained least squares and convex designs.** Mix a minimax bound in one band with a least squares error in another, as a [convex optimization](/convex-optimization-problem/) problem.
- **Robust implementations.** Later implementations improve the start set, the grid and the barycentric formulas, so that the exchange also works for much longer filters.
- **IIR filters.** For a magnitude only specification, an elliptic [IIR filter](/iir-filter/) needs a much lower order, but it is not linear phase.

## When to use it

Use the Parks-McClellan algorithm when you need a linear phase FIR filter with given band edges and ripples and the fewest taps, for example for an anti aliasing filter in [sample rate conversion](/sample-rate-conversion/) or a channel filter in a receiver. Use the window method when a quick design is enough or when the stop band must fall off away from the edge. Use an IIR design when the phase does not matter and the cost per sample must be as low as possible.

## Pitfalls

- **No convergence.** Very wide transition bands, very long filters or extreme weights can make the exchange fail or stop with a wrong set. Check the alternation count and the error on a dense grid.
- **Ripple in the transition band.** The transition band is not controlled. With several bands, the response can have a bump there that is larger than in the bands.
- **Grid too coarse.** The optimum is computed on the grid. Use 16 or more points per ripple and check the result on a finer grid.
- **Wrong type.** A symmetric filter with an even number of taps (type 2) has $A(\pi) = 0$, so it cannot be a high-pass filter. Use type 1, or the antisymmetric type 4.
- **Units of the edges.** Some tools take edges as fractions of the sample rate or of the Nyquist frequency instead of in radians per sample. A factor of 2 or $2\pi$ changes the filter.
- **Ripples in decibels.** The pass band ripple $\delta_p$ gives $20\log_{10}(1 + \delta_p)$ dB of gain error. The stop band ripple gives $20\log_{10}\delta_s$ dB of attenuation. Convert before you choose $K$.

## Implementations

## History

The design of FIR filters by windows and by frequency sampling was common in the 1960s, but these methods did not give the shortest filter for a specification. In 1972 Thomas Parks and James McClellan at Rice University showed that, with fixed band edges and a weight, the optimal linear phase filter is a weighted Chebyshev approximation problem. They used the alternation theorem to describe the optimum and the Remez exchange of 1934 to compute it. In 1973 McClellan, Parks and Lawrence Rabiner published a Fortran program for all four types of linear phase filters. It became the standard tool for FIR design, and its algorithm is in most signal processing software under the name remez or firpm.

## References
