---
tag: 9KA907
kind: theorem
slug: mimo-capacity
name: MIMO channel capacity
aliases:
- Telatar capacity formula
- Foschini-Telatar capacity
area: communications/mimo-communications
level: core
summary: The capacity of a Gaussian MIMO channel is the log-determinant of I + H Q H^*/N0 maximized over input covariances Q.
prereqs: [mimo-channel-model, channel-capacity, singular-value-decomposition, water-filling-power-allocation]
see_also: [kronecker-channel-model, spatial-multiplexing, diversity-multiplexing-tradeoff, svd-precoding, ergodic-capacity, outage-capacity, shannon-hartley-theorem, dirty-paper-coding]
sources:
  - paper: doi:10.1002/ett.4460100604
    title: "Emre Telatar, Capacity of multi-antenna Gaussian channels, European Transactions on Telecommunications 10(6), 585-595, 1999"
    locator: "the capacity of the channel with a fixed known H (singular value decomposition and water-filling), the ergodic capacity under i.i.d. Rayleigh fading with the optimality of (P/t) I and the exact integral formula, and the non-ergodic case"
  - paper: doi:10.1023/A:1008889222784
    title: "Gerard J. Foschini and Michael J. Gans, On limits of wireless communications in a fading environment when using multiple antennas, Wireless Personal Communications 6(3), 311-335, 1998"
    locator: the capacity of quasi-static Rayleigh MIMO channels as a random variable and its outage distribution
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 7.1.1 (capacity via the singular value decomposition), Section 8.2.1 (fast fading capacity with CSI at the receiver), Section 8.2.3 (full CSI) and Section 8.4 (the slow fading MIMO channel)"
  - book: isbn:9780471241959
    title: "Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006"
    locator: Chapter 8 (the Gaussian distribution maximizes the differential entropy for a given covariance) and Chapter 9 (the section on parallel Gaussian channels and water-filling)
---

The MIMO capacity theorem gives the largest reliable rate of the [MIMO channel model](/mimo-channel-model/) $y = Hx + w$. For a fixed channel known at both ends, the capacity is $\log_2 \det(I + H Q H^H / N_0)$ maximized over input covariances $Q$ with trace at most $P$, and the best $Q$ pours power by water-filling into the singular directions of $H$. For i.i.d. Rayleigh fading known only at the receiver, equal power on all antennas is optimal, and the ergodic capacity grows as $\min(N_t, N_r) \log_2 \rho$ at high SNR. The [Kronecker channel model](/kronecker-channel-model/) shows how correlation lowers this capacity, and [spatial multiplexing](/spatial-multiplexing/) is the technique that turns the extra streams into rate.

## Statement

Take $y = Hx + w$ with $H \in \mathbb{C}^{N_r \times N_t}$, $w \sim \mathcal{CN}(0, N_0 I)$, an input power limit $\mathbb{E}[x^H x] \le P$ and $\rho = P/N_0$. Rates are in bits per channel use.

**Theorem (fixed channel known at both ends).** If $H$ is fixed and known to the transmitter and the receiver, the capacity is

$$C = \max_{Q \succeq 0,\ \mathrm{tr}\, Q \le P} \log_2 \det\!\left(I_{N_r} + \frac{1}{N_0} H Q H^H\right) = \sum_{i=1}^{n} \log_2\!\left(1 + \frac{p_i \sigma_i^2}{N_0}\right),$$

where $\sigma_1, \ldots, \sigma_n$ are the nonzero singular values of $H$, $p_i = (\mu - N_0/\sigma_i^2)^+$, and the water level $\mu$ is set by $\sum_i p_i = P$. The maximum is reached by $x \sim \mathcal{CN}(0, Q)$ with $Q = V \mathrm{diag}(p_i) V^H$, where $V$ holds the right singular vectors of $H$.

**Theorem (ergodic i.i.d. Rayleigh fading, CSIR).** If $H$ has i.i.d. $\mathcal{CN}(0, 1)$ entries, changes in an ergodic way from use to use, and is known to the receiver only, the capacity is

$$C = \mathbb{E}\, \log_2 \det\!\left(I_{N_r} + \frac{\rho}{N_t} H H^H\right),$$

reached by $x \sim \mathcal{CN}(0, (P/N_t) I)$.

## In plain words

With several antennas at each end, the link behaves like a set of separate pipes, one for each independent direction in which the antennas can send and listen. The number of pipes is at most the smaller of the two antenna counts. Each pipe has its own strength.

If the sender knows how strong each pipe is, it should give more power to the strong pipes and none to the very weak ones, like water poured into a vessel with an uneven floor. If the sender does not know the channel and the paths are random and unrelated, the best it can do is split the power equally over its antennas.

At high signal strength, every doubling of the power adds one bit per pipe, so a link with four antennas at each end gains four times as fast as a link with one.

## Proof

**Step 1 (the Gaussian input is best for a given covariance).** For an input with covariance $Q$, the mutual information is $I(x; y) = h(y) - h(y \mid x) = h(y) - \log_2 \det(\pi e N_0 I)$, since $y$ given $x$ is $\mathcal{CN}(Hx, N_0 I)$. The output has covariance $K_y = H Q H^H + N_0 I$. Among all complex random vectors with covariance $K_y$, the circularly symmetric Gaussian vector has the largest differential entropy, $\log_2 \det(\pi e K_y)$ (Cover and Thomas, Chapter 8, in its complex form). So

$$I(x; y) \le \log_2 \det(\pi e K_y) - \log_2 \det(\pi e N_0 I) = \log_2 \det\!\left(I + \frac{1}{N_0} H Q H^H\right),$$

with equality for $x \sim \mathcal{CN}(0, Q)$, which makes $y$ circularly symmetric Gaussian. The channel is memoryless with an average cost $\mathbb{E}[x^H x] \le P$, so the [channel coding theorem](/channel-coding-theorem/) with a cost constraint gives the capacity as the largest mutual information over inputs with $\mathrm{tr}\, Q \le P$.

**Step 2 (the singular value decomposition).** Write $H = U \Sigma V^H$ with unitary $U$ and $V$. Since $\det(I + AB) = \det(I + BA)$ and $U$ is unitary,

$$\det\!\left(I + \tfrac{1}{N_0} H Q H^H\right) = \det\!\left(I + \tfrac{1}{N_0} \Sigma \tilde Q \Sigma^H\right), \qquad \tilde Q = V^H Q V,$$

and $\mathrm{tr}\, \tilde Q = \mathrm{tr}\, Q$. The matrix $I + \Sigma \tilde Q \Sigma^H / N_0$ is positive definite, and by the Hadamard inequality its determinant is at most the product of its diagonal entries, $\prod_i (1 + \sigma_i^2 \tilde q_{ii} / N_0)$, with equality when $\tilde Q$ is diagonal. So the problem is to maximize $\sum_i \log_2(1 + \sigma_i^2 p_i / N_0)$ over $p_i \ge 0$ with $\sum_i p_i \le P$. The objective is concave, the constraints are linear, and the KKT conditions give $p_i = (\mu - N_0/\sigma_i^2)^+$, which is [water-filling](/water-filling-power-allocation/).

**Step 3 (ergodic fading with CSIR).** The receiver knows $H$, so the output is the pair $(y, H)$. For an input independent of $H$, $I(x; y, H) = I(x; H) + I(x; y \mid H) = I(x; y \mid H)$. Given $H$, Step 1 applies, so the largest value for a covariance $Q$ is $f(Q) = \mathbb{E}\, \log_2 \det(I + H Q H^H / N_0)$. For a memoryless channel whose state is i.i.d. over uses and known at the receiver, the coding theorem gives $C = \max_{\mathrm{tr}\, Q \le P} f(Q)$. The same holds for a stationary ergodic state, since the coding theorem then uses the ergodic theorem in place of the law of large numbers.

**Step 4 (equal power is optimal for i.i.d. Rayleigh).** Three facts hold.

- $f$ is concave in $Q$: $\log \det$ is concave on positive definite matrices, $Q \mapsto I + H Q H^H / N_0$ is affine, and an expectation of concave functions is concave.
- $f(W Q W^H) = f(Q)$ for every unitary $W$, because $H W$ has the same law as $H$ when the entries of $H$ are i.i.d. $\mathcal{CN}(0, 1)$.
- $f$ does not decrease when $Q$ grows in the positive semidefinite order, since $\log \det$ is monotone.

Let $\mathcal{G}$ be the finite group of matrices $W = \Pi D$, with $\Pi$ a permutation matrix and $D$ a diagonal matrix with entries $\pm 1$. For any $Q$, the average of $D Q D$ over the $2^{N_t}$ sign matrices sets the entries off the diagonal to zero, because $\mathbb{E}[d_i d_k] = 0$ for $i \ne k$. The average of the resulting diagonal matrix over all permutations is $(\mathrm{tr}\, Q / N_t) I$. So $\frac{1}{|\mathcal{G}|} \sum_{W \in \mathcal{G}} W Q W^H = (\mathrm{tr}\, Q / N_t) I$, and by concavity and invariance,

$$f\!\left(\tfrac{\mathrm{tr}\, Q}{N_t} I\right) \ge \frac{1}{|\mathcal{G}|} \sum_{W \in \mathcal{G}} f(W Q W^H) = f(Q).$$

By monotonicity, $f((P/N_t) I) \ge f((\mathrm{tr}\, Q / N_t) I)$ for every feasible $Q$. So $Q = (P/N_t) I$ is optimal, and $C = \mathbb{E}\, \log_2 \det(I + (\rho/N_t) H H^H)$. $\blacksquare$

## Consequences

- **Worked example (fixed channel).** Take $H = \begin{pmatrix} 1 & 0.5 \\ 0.5j & 1 \end{pmatrix}$. Then $H H^H = \begin{pmatrix} 1.25 & 0.5 - 0.5j \\ 0.5 + 0.5j & 1.25 \end{pmatrix}$, with eigenvalues $\sigma_1^2 = 1.95711$ and $\sigma_2^2 = 0.54289$.

| $\rho$ | equal power | water-filling | powers $(p_1, p_2)/N_0$ |
|---|---|---|---|
| 0 dB | 1.33092 | 1.56419 | (1, 0) |
| 10 dB | 5.32418 | 5.34103 | (5.6655, 4.3345) |
| 20 dB | 11.44204 | 11.44228 | both near 50 |

  At 0 dB the weak mode gets no power, because $1/\sigma_2^2 = 1.842$ is above the water level $1.51096$. At high SNR the two allocations meet.
- **The rank sets the slope.** For $2 \times 2$ at $\rho = 10$, $H = I$ gives $2 \log_2 6 = 5.1699$ bits, and the all-ones matrix of rank one gives only $\log_2 21 = 4.3923$ bits, though its entries are larger on average.
- **High SNR** (theorem, i.i.d. Rayleigh). $C = \min(N_t, N_r) \log_2 \rho + O(1)$. The ergodic values in the [MIMO channel model](/mimo-channel-model/) table show this: from 20 dB to 30 dB, the $4 \times 4$ capacity grows by 12.76 bits and the $1 \times 1$ capacity by 3.26 bits.
- **Low SNR** (first-order expansion). $C \approx \rho N_r / \ln 2$ with CSIR: the receive antennas collect more energy, and the transmit antennas do not help without CSIT. With CSIT, beamforming on the strongest singular direction already gives $\rho\, \mathbb{E}[\sigma_{\max}^2] / \ln 2$ to first order, which is larger.
- **Linear growth** (theorem, Telatar). For $N_t = N_r = n$ and i.i.d. Rayleigh fading, $C/n$ tends to a positive constant at each fixed $\rho$ as $n \to \infty$.
- **Slow fading.** If $H$ stays fixed for a whole codeword, $\log_2 \det(I + (\rho/N_t) H H^H)$ is a random variable, and Foschini and Gans described the link by its outage probability. For $1 \times 1$ at $R = 1$ bit, the outage probability is $1 - e^{-1/\rho}$: 0.095163 at 10 dB, 0.0099502 at 20 dB and 0.00099950 at 30 dB. See [outage capacity](/outage-capacity/) and the [diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/).
- **Receivers that reach it.** With CSIT, [SVD precoding](/svd-precoding/) and water-filling turn the channel into parallel scalar channels. With CSIR only, an MMSE receiver with successive interference cancellation reaches the ergodic capacity of the equal-power input (see [V-BLAST](/v-blast/)).

## Tightness

- **Equal power is not optimal with CSIT.** The example above has a gain of 0.233 bits at 0 dB from water-filling.
- **Equal power is not optimal for correlated channels.** If the transmitter knows the transmit correlation, more power on the strong eigenvectors of $R_t$ helps, most of all at low SNR; see the [Kronecker channel model](/kronecker-channel-model/).
- **Equal power fails for a Rician channel at low SNR.** A strong line-of-sight part makes beamforming in its direction better.
- **Gaussian inputs are needed.** With $M$-point constellations on each antenna, the rate cannot exceed $N_t \log_2 M$ bits per use, so the high-SNR growth stops.
- **CSIR is needed.** Without channel knowledge at the receiver, in block fading with coherence time $T$, Zheng and Tse showed in 2002 that the high-SNR slope is $M^*(1 - M^*/T)$ with $M^* = \min(N_t, N_r, \lfloor T/2 \rfloor)$, below $\min(N_t, N_r)$.
- **No capacity in the strict sense in slow fading.** With a quasi-static channel and no CSIT, any positive rate has a positive outage probability, so the ergodic formula is not an achievable rate for one codeword.

## History

Foschini, at Bell Labs, showed in 1996 that layered space-time processing could reach a rate that grows linearly with the number of antennas, and Foschini and Gans gave the outage view of quasi-static MIMO capacity in 1998. Telatar derived the capacity of the Gaussian MIMO channel with a fixed and with a Rayleigh fading matrix in a Bell Labs technical memorandum in 1995, published in the European Transactions on Telecommunications in 1999. The two works started the study of multi-antenna communication.

## References
