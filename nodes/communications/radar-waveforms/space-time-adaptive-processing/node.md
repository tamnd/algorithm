---
tag: STKZ5N
kind: algorithm
slug: space-time-adaptive-processing
name: Space-time adaptive processing
aliases:
- STAP
area: communications/radar-waveforms
level: advanced
summary: "Filters radar data jointly over M antennas and P pulses with the weight R^-1 v, R estimated from training cells, to detect slow targets in the clutter of a moving radar."
model: real-ram
complexity:
  vars: {M: the number of antenna elements, P: the number of pulses, T: the number of training snapshots}
  time: {worst: Θ(T M^2 P^2 + M^3 P^3), average: Θ(T M^2 P^2 + M^3 P^3), best: Θ(T M^2 P^2 + M^3 P^3)}
  space: {extra: Θ(M^2 P^2)}
properties: {deterministic: true, linear_filter: true, adaptive: true, needs_training_data: true, constant_false_alarm_rate_with_known_covariance: true}
history:
  year: 1973
  people: [L. E. Brennan, I. S. Reed]
  note: "Brennan and Reed gave the theory of the optimum adaptive radar filter over antennas and pulses in 1973. Reed, Mallett and Brennan gave the loss of the sample matrix inversion weight in 1974."
prereqs: [beamforming, range-doppler-processing, cholesky-decomposition, positive-definite-matrix]
see_also: [capon-beamformer, moving-target-indication, kronecker-product, woodbury-identity, music-algorithm, cfar-detection, synthetic-aperture-radar, matrix-inversion]
sources:
  - paper: doi:10.1109/TAES.1973.309792
    title: Theory of adaptive radar
    locator: "L. E. Brennan and I. S. Reed, IEEE Transactions on Aerospace and Electronic Systems 9(2), 1973, pp. 237 to 252 (the optimum space-time weight and its SINR)"
  - paper: doi:10.1109/TAES.1974.307893
    title: Rapid convergence rate in adaptive arrays
    locator: "I. S. Reed, J. D. Mallett and L. E. Brennan, IEEE Transactions on Aerospace and Electronic Systems 10(6), 1974, pp. 853 to 863 (the distribution of the SINR loss of the sample matrix inversion weight)"
  - paper: "J. Ward, Technical Report 1015, MIT Lincoln Laboratory, 1994"
    title: Space-time adaptive processing for airborne radar
    locator: "the whole report (the clutter model, the clutter ridge, the clutter rank and the processing architectures)"
  - book: isbn:9780071444743
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, McGraw-Hill, 2005"
    locator: "Chapter 9, Sections 9.4 to 9.6 (the optimum space-time filter, the clutter rank, sample matrix inversion and the training data)"
---

Space-time adaptive processing (STAP) detects targets with a radar that moves, usually on an aircraft, where the ground clutter has a Doppler shift that depends on its angle. It stacks the samples of $M$ antenna elements over $P$ pulses at one range into a snapshot of length $D = MP$, estimates the covariance $R$ of clutter, jamming and noise from $T$ nearby range cells, and applies the weight $w = R^{-1} v$ for the space-time steering vector $v$ of the target. This weight gives the largest output signal to interference plus noise ratio (SINR) of all linear filters. It puts a null along the whole clutter ridge in angle and Doppler, which a fixed [beamformer](/beamforming/) followed by a Doppler filter, or an [MTI canceller](/moving-target-indication/), cannot do. In space only ($P = 1$), the same weight is the [Capon beamformer](/capon-beamformer/).

## In plain words

On a moving aircraft, the ground straight ahead comes closer fast and the ground to the side does not, so the clutter has a different Doppler shift in each direction. A slow target can have the same Doppler shift as the ground in some other direction, and a Doppler filter alone cannot separate them. But the target and that patch of ground are in different directions. If you use several antennas and several pulses together, you can cancel the ground in every direction at its own Doppler and keep the target. The weights that do this depend on the clutter, so you measure the clutter in cells near the one you test, compute its covariance, and solve a linear system with it.

## The problem

The input is $T$ training snapshots $x_1, \dots, x_T \in \mathbb{C}^D$ from range cells near the cell under test, assumed to hold the same interference and no target, the snapshot $x$ of the cell under test, the steering vector $v$ and a loading $\delta \ge 0$. Entry $pM + m$ of a snapshot is pulse $p$ at element $m$. For a uniform linear array, a target at spatial frequency $f_s$ and normalized Doppler $f_t$ has $v[pM + m] = e^{j 2\pi (f_t p + f_s m)}$, the [Kronecker product](/kronecker-product/) of a temporal and a spatial steering vector. The output is the weight $w$ with $(\hat{R} + \delta I) w = v$, where $\hat{R} = \frac{1}{T} \sum_t x_t x_t^H$, the filter output $y = w^H x$ and the statistic $\Lambda = |y|^2 / (v^H w)$, which is compared with a threshold.

## The algorithm

```pseudo id=main
SMI-STAP(x_1..x_T, v, x, delta)
L1  R <- (1/T) * sum over t of x_t x_t^H                ▷ the sample covariance, D x D
L2  R[i][i] <- R[i][i] + delta for i = 0, ..., D - 1   ▷ diagonal loading
L3  G <- CHOLESKY(R)                                   ▷ R = G G^H, G lower triangular
L4  w <- solve G a = v forward, then G^H w = a backward
L5  y <- w^H x
L6  Lambda <- |y|^2 / Re(v^H w)                         ▷ the adaptive matched filter statistic
L7  return w, y, Lambda
```

Line L1 is the sample matrix of sample matrix inversion (SMI). Line L2 adds a small multiple of the identity, which keeps the matrix positive definite when $T < D$ and lowers the noise in the weight. Line L3 is the [Cholesky decomposition](/cholesky-decomposition/), which exists because the matrix is Hermitian and positive definite. Line L4 solves for $w$ by two triangular substitutions; the inverse is never formed. Line L6 normalizes the output power by its value under interference only, so that a threshold on $\Lambda$ gives a known false alarm rate.

## Example

A toy case with $D = 2$ and $T = 2$: the training snapshots are $(3, 3)$ and $(1, -1)$, so

$$\hat{R} = \tfrac{1}{2}\left( \begin{bmatrix} 9 & 9 \\ 9 & 9 \end{bmatrix} + \begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix} \right) = \begin{bmatrix} 5 & 4 \\ 4 & 5 \end{bmatrix}.$$

The strong component along $(1, 1)$ plays the role of a jammer or of clutter. Take the target $v = (1, j)$ and $\delta = 0$.

| step | value |
|---|---|
| L3 | $G = \begin{bmatrix} 2.236 & 0 \\ 1.789 & 1.342 \end{bmatrix}$, that is $\sqrt{5}$, $4/\sqrt{5}$ and $3/\sqrt{5}$ |
| L4 | $w = \hat{R}^{-1} v = \left( (5 - 4j)/9,\ (-4 + 5j)/9 \right)$ |
| | $v^H w = 10/9$, the optimum SINR $v^H \hat{R}^{-1} v$ |
| | the gain on the jammer: $\lvert w^H (1, 1) \rvert^2 = 2/81$ |
| | the SINR of the plain matched filter $w = v$: $\lvert v^H v \rvert^2 / (v^H \hat{R} v) = 4/10 = 0.4$ |

The adaptive weight gives an SINR of $10/9$ against $0.4$ for the matched filter, a gain of 4.4 dB, because it almost nulls the direction $(1, 1)$.

A larger case: an array of $M = 4$ elements and $P = 4$ pulses, the clutter on the ridge $f_t = f_s$ (that is $\beta = 1$), 64 clutter patches and a clutter to noise ratio of 40 dB. For a target off the ridge at $f_s = 0$, $f_t = 0.5$, the optimum SINR is $0.833 D$, close to the noise-only value $D$. For a target on the ridge, at $f_s = f_t = 0.125$, it is about $4 \times 10^{-5} D$: a target with the speed and direction of the clutter cannot be seen. The non-adaptive weight $v$ gives about $0.0004 D$ off the ridge, because the clutter enters through its sidelobes.

## Correctness

The matrix of line L3 is Hermitian positive semidefinite, and it is positive definite if $\delta > 0$ or if the training snapshots span $\mathbb{C}^D$, which needs $T \ge D$. So the Cholesky factor exists, and the two substitutions of line L4 give the unique solution of $(\hat{R} + \delta I) w = v$. With the true covariance $R$, the Cauchy-Schwarz inequality in the inner product $a^H R b$ gives $|u^H v|^2 / (u^H R u) \le v^H R^{-1} v$ for every weight $u$, with equality exactly for multiples of $R^{-1} v$, so this weight maximizes the SINR. With the true $R$ and Gaussian interference, $\Lambda$ is exponential with mean 1, so $P(\Lambda > \eta) = e^{-\eta}$ for every $R$. For a clutter ridge $f_t = \beta f_s$ with an integer $1 \le \beta \le M$, the clutter covariance has rank $M + \beta(P - 1)$ (Brennan's rule). The [correctness proof](proofs/correctness.md) gives the arguments.

## Complexity

**Time.** Line L1 adds $T$ outer products of size $D \times D$: $\Theta(T D^2)$. Line L3 costs $\Theta(D^3)$, and line L4 costs $\Theta(D^2)$. With $D = MP$ the total is $\Theta(T M^2 P^2 + M^3 P^3)$ in every case, and with the usual $T \approx 2D$, it is $\Theta(M^3 P^3)$. One weight serves all the cells that share its training data, and lines L5 and L6 cost $\Theta(D)$ per cell.

**Space.** $\Theta(M^2 P^2)$ for $\hat{R}$ and $G$.

For $M = 16$ elements and $P = 32$ pulses, $D = 512$. With $T = 2D$ training cells, line L1 needs about $2.7 \times 10^8$ multiplications and line L3 about $4.5 \times 10^7$, for each set of training cells. Line L4 then costs about $5 \times 10^5$ for each steering vector. This cost is the reason for the reduced-rank and partially adaptive variants below.

## Properties

- **Optimum SINR (theorem).** With the true $R$, $w = R^{-1} v$ maximizes the output SINR, and the maximum is $v^H R^{-1} v$. The scale of $w$ does not matter.
- **The loss of SMI (theorem, Reed, Mallett and Brennan 1974).** With $T \ge D$ independent Gaussian training snapshots and no loading, the ratio $\rho$ of the SINR of the SMI weight to the optimum has a beta distribution with mean $(T + 2 - D)/(T + 1)$. So $T = 2D - 3$ gives a mean loss of exactly 3 dB. $T = 2D$ gives 1.76 dB for $D = 4$, 2.63 dB for $D = 16$ and 2.91 dB for $D = 64$. The tests check the mean by simulation for $T = 5$ and $T = 8$ with $D = 4$.
- **Clutter rank (theorem for integer $\beta$, rule otherwise).** The clutter covariance of a side-looking linear array has rank about $M + \beta(P - 1)$, with $\beta = 2 v_p T_r / d$ for the platform speed $v_p$, the pulse interval $T_r$ and the element spacing $d$. The tests check the exact rank for $(M, P, \beta) = (4, 4, 1)$, $(4, 4, 2)$, $(3, 4, 1)$ and $(4, 3, 2)$.
- **Constant false alarm rate with a known covariance (theorem).** $\Lambda$ is exponential with mean 1 under interference only. With $\hat{R}$ in place of $R$ the false alarm rate still does not depend on $R$, but its value changes with $T$.
- **The steering vector is separable.** $v = v_t \otimes v_s$, which the tests check.

## Variants and improvements

- **Diagonal loading.** Line L2 with $\delta$ near the noise power. It lets $T$ be much smaller than $2D$, close to twice the clutter rank, at a small loss.
- **Reduced-rank STAP.** Project onto the principal eigenvectors of $\hat{R}$ (the clutter subspace) and null that subspace, as in the principal components method. The rank $M + \beta(P - 1)$ is much smaller than $MP$.
- **Partially adaptive STAP.** First apply fixed Doppler filters or beams, then adapt over a few of them: factored STAP adapts over the elements in each Doppler bin, and the extended factored method over a few adjacent bins. This cuts $D$ from $MP$ to a small multiple of $M$.
- **Matrix updates.** When the training window slides by one cell, update $\hat{R}^{-1}$ with the [Woodbury identity](/woodbury-identity/) in $O(D^2)$.
- **Knowledge-aided STAP.** Use maps of the terrain or a model of the clutter to build part of $R$, when there are few homogeneous training cells.
- **Space only and time only.** With $P = 1$ the method is the adaptive spatial beamformer, the [Capon beamformer](/capon-beamformer/). With $M = 1$ it is an adaptive Doppler filter.

## When to use it

Use STAP on an airborne or spaceborne radar that must detect slow ground or air targets in strong clutter, for example ground moving target indication from an aircraft, when the clutter spreads over many Doppler bins because the platform moves. It is also the tool when jamming and clutter are present together. For a fixed radar, [MTI](/moving-target-indication/) and [range-Doppler processing](/range-doppler-processing/) are enough. When the training cells are few or not homogeneous, use loading, reduced-rank or partially adaptive forms.

## Pitfalls

- **Too few training snapshots in line L1.** With $T < D$ and $\delta = 0$, $\hat{R}$ is singular and line L3 fails. With $T$ only a little above $D$, the weight is noisy and the mean loss $(T + 2 - D)/(T + 1)$ is large: for $T = D$ it is $2/(D + 1)$, which is 9.3 dB for $D = 16$. Use $T \ge 2D$ or loading.
- **The target in the training data of line L1.** If the cell under test, or a cell with the same target, is in the training set, $\hat{R}$ learns the target and the weight nulls it. Leave guard cells around the cell under test, as in [CFAR](/cfar-detection/).
- **Inverting the matrix in line L4.** Forming $\hat{R}^{-1}$ explicitly and multiplying costs more and loses accuracy when the clutter to noise ratio is large, because $\hat{R}$ is then badly conditioned. Solve with the Cholesky factor.
- **The wrong order of the snapshot entries.** The steering vector and the snapshots must use the same order, here pulse major, $pM + m$. If the data are element major and $v$ is pulse major, the weight is the optimum for a different target and the clutter null lands in the wrong place.
- **Heterogeneous training.** Clutter changes from land to water and with range for a forward-looking array. If the training cells do not match the cell under test, the null is in the wrong place and false alarms rise. The theory of the SMI loss assumes independent and identically distributed training.
- **Using the real part in line L6 only by habit.** $v^H w$ is real and positive in exact arithmetic, because $\hat{R} + \delta I$ is positive definite. A rounding error can leave a tiny imaginary part, and the code takes the real part. A negative value means the matrix was not positive definite.

## Implementations

## History

L. E. Brennan and I. S. Reed published the theory of adaptive radar in 1973: the optimum weight over antenna elements and pulses and its SINR. In 1974, Reed, Mallett and Brennan derived the distribution of the SINR of the sample matrix inversion weight, which gave the rule that about twice as many training snapshots as degrees of freedom keep the loss within 3 dB on average. J. Ward's 1994 report at MIT Lincoln Laboratory set out the clutter model, the clutter ridge and the processing architectures that most later work uses. The large cost of full STAP led to the reduced-rank and partially adaptive methods.

## References
