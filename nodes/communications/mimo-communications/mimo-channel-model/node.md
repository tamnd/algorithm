---
tag: 96JWPM
kind: model
slug: mimo-channel-model
name: MIMO channel model
aliases:
- multiple-input multiple-output channel
area: communications/mimo-communications
level: intro
summary: A channel with several transmit and receive antennas, written y = Hx + n with a random channel matrix H.
prereqs: [rayleigh-fading-channel, additive-white-gaussian-noise-channel]
see_also: [mimo-capacity, kronecker-channel-model, spatial-multiplexing, diversity-multiplexing-tradeoff, mimo-detection, alamouti-code, massive-mimo, geometry-based-stochastic-channel-model]
sources:
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 7.1 (the MIMO channel, capacity via the SVD, rank and condition number) and Section 7.3 (modeling of MIMO fading channels, with the i.i.d. Rayleigh model in Section 7.3.8)"
  - book: isbn:9780521826150
    title: "Arogyaswami Paulraj, Rohit Nabar and Dhananjay Gore, Introduction to Space-Time Wireless Communications, Cambridge University Press, 2003"
    locator: "Chapter 3, Space-time propagation and channel models"
  - paper: doi:10.1002/ett.4460100604
    title: "Emre Telatar, Capacity of multi-antenna Gaussian channels, European Transactions on Telecommunications 10(6), 585-595, 1999"
    locator: Section 2 (the model y = Hx + n with a power constraint on x) and the Rayleigh fading case
  - book: isbn:9780521762281
    title: "Robert W. Heath Jr. and Angel Lozano, Foundations of MIMO Communication, Cambridge University Press, 2018"
    locator: the chapters on the channel model and on MIMO channel models
---

The MIMO channel model describes a link with $N_t$ transmit antennas and $N_r$ receive antennas by one matrix equation, $y = Hx + w$. Each entry of the random matrix $H$ is the complex gain from one transmit antenna to one receive antenna. This page fixes the notation and the usual assumptions; the [MIMO capacity](/mimo-capacity/) page gives what the model can carry, and the [Kronecker channel model](/kronecker-channel-model/) is a common way to add correlation between antennas. The model reduces to the [Rayleigh fading channel](/rayleigh-fading-channel/) when $N_t = N_r = 1$ and to the [AWGN channel](/additive-white-gaussian-noise-channel/) when $H$ is a fixed scalar.

## The machine

One channel use takes a complex vector $x \in \mathbb{C}^{N_t}$, one entry for each transmit antenna, and returns

$$y = H x + w, \qquad H \in \mathbb{C}^{N_r \times N_t}, \qquad w \sim \mathcal{CN}(0, N_0 I_{N_r}).$$

Row $i$ of $H$ belongs to receive antenna $i$ and column $k$ to transmit antenna $k$, so $h_{ik}$ is the gain from transmit antenna $k$ to receive antenna $i$. The input has a total power limit $\mathbb{E}[x^H x] \le P$, summed over all transmit antennas, so adding antennas does not add power. The gains are normalized so that $\mathbb{E}|h_{ik}|^2 = 1$, and the **SNR** is $\rho = P/N_0$: the average SNR at each receive antenna.

A model is complete only with three more choices.

- **The law of $H$.** In the **i.i.d. Rayleigh** model, the entries are independent $\mathcal{CN}(0, 1)$. It describes rich scattering with antennas spaced far enough apart. Correlated models (Kronecker, geometry based), the [Rician](/rician-fading-channel/) model with a line-of-sight part, and the keyhole model are the common alternatives.
- **How $H$ changes in time.** In **fast fading**, $H$ changes from use to use, and a codeword sees many values of $H$. In **slow** or **quasi-static** fading, $H$ stays fixed for a whole codeword, which can then fall into an outage. **Block fading** keeps $H$ fixed for blocks of $T$ uses, for example the [coherence time](/coherence-time/).
- **Who knows $H$.** With **CSIR**, the receiver knows $H$ exactly, as from a perfect [channel estimate](/channel-estimation/). With **CSIT**, the transmitter knows it too. Without either, the channel is noncoherent.

A frequency-selective MIMO channel has a matrix tap for each delay. With [OFDM](/orthogonal-frequency-division-multiplexing/), it becomes one flat model $y_n = H_n x_n + w_n$ on each subcarrier $n$.

## What it counts

The model counts information and errors per channel use.

- **Rate** in bits per channel use, which is bits per second per hertz for a band of $W$ hertz with $W$ complex uses per second. The [MIMO capacity](/mimo-capacity/) is the largest reliable rate.
- **Error probability** of a code, averaged over the noise and the law of $H$. Its slope at high SNR on a log-log plot is the [diversity order](/diversity-order/).
- **Degrees of freedom**, the number of independent streams the channel can carry, which is the rank of $H$ and at most $\min(N_t, N_r)$.

The cost of a receiver algorithm on this model, for example in [MIMO detection](/mimo-detection/), is counted in complex operations per channel use, as a function of $N_t$, $N_r$ and the constellation size.

## Relation to other models

- **SISO, SIMO and MISO.** With $N_t = N_r = 1$, the model is the scalar [Rayleigh fading channel](/rayleigh-fading-channel/). With $N_t = 1$, $H$ is a column, and the receiver can use [maximal ratio combining](/maximal-ratio-combining/). With $N_r = 1$, $H$ is a row, and the transmitter can use [maximum ratio transmission](/maximum-ratio-transmission/) with CSIT or the [Alamouti code](/alamouti-code/) without it.
- **Correlated models.** The [Kronecker channel model](/kronecker-channel-model/) writes $H = R_r^{1/2} H_w R_t^{1/2}$, with $H_w$ i.i.d. Rayleigh. [Geometry-based stochastic channel models](/geometry-based-stochastic-channel-model/) build $H$ from clusters of scatterers with angles and delays.
- **Line of sight.** One plane wave between two uniform linear arrays gives $H = a_r b_t^H$, a rank-one matrix, with array response vectors $a_r$ and $b_t$. The Rician model adds such a term to a Rayleigh part.
- **Keyhole.** $H = h_r h_t^H$ with independent Rayleigh vectors. Each entry is Rayleigh distributed, but the rank is one, so the channel has one degree of freedom however many antennas it has.
- **Massive MIMO.** The [massive MIMO](/massive-mimo/) pages write the uplink as $y = G x + w$ with $G \in \mathbb{C}^{M \times K}$ for $M$ base station antennas and $K$ single-antenna users: the same model with a different name for the matrix.

## Known results in the model

- **Capacity with CSIR, fixed $H$** (theorem, Telatar 1999). With equal power on all antennas, the mutual information is $\log_2 \det(I_{N_r} + (\rho/N_t) H H^H)$. For $N_t = N_r = 2$, $H = I$ and $\rho = 10$, this is $2 \log_2 6 = 5.1699$ bits per use. For the rank-one $H$ with all four entries equal to 1, it is $\log_2(1 + 2\rho) = \log_2 21 = 4.3923$, even though every entry has the same magnitude: the rank, not the size of the entries, sets the number of streams.
- **Ergodic capacity, i.i.d. Rayleigh, CSIR** (theorem, Telatar 1999; values from his exact integral formula). In bits per use:

| $N_t \times N_r$ | 0 dB | 10 dB | 20 dB | 30 dB |
|---|---|---|---|---|
| $1 \times 1$ | 0.860 | 2.907 | 5.884 | 9.144 |
| $2 \times 1$ | 0.921 | 3.166 | 6.282 | 9.579 |
| $1 \times 2$ | 1.443 | 4.059 | 7.268 | 10.577 |
| $2 \times 2$ | 1.685 | 5.549 | 11.291 | 17.744 |
| $4 \times 4$ | 3.355 | 10.941 | 22.139 | 34.897 |

  Each 10 dB adds about $3.32 \min(N_t, N_r)$ bits at high SNR: $\min(N_t, N_r) \log_2 \rho$ is the leading term.
- **Diversity** (theorem, for i.i.d. Rayleigh and slow fading). The best error probability at a fixed rate falls as $\rho^{-N_t N_r}$, and the [diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/) gives the best exponent at each rate that grows with $\log \rho$.
- **Large arrays** (theorem, limit statement for i.i.d. Rayleigh). As the number of antennas at one end grows, $\|h\|^2/M \to 1$ ([channel hardening](/channel-hardening/)) and $h_i^H h_j / M \to 0$ for two users ([favorable propagation](/favorable-propagation/)).
- **Measurements.** Indoor and outdoor measurement campaigns found that the i.i.d. model overstates the capacity when antennas are close or the angular spread is small; this is why correlated models are used.

## References
