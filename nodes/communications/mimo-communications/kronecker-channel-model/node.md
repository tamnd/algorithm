---
tag: 008KZF
kind: model
slug: kronecker-channel-model
name: Kronecker channel model
aliases:
- separable correlation model
area: communications/mimo-communications
level: advanced
summary: A MIMO channel model whose correlation is the product of a transmit and a receive correlation matrix.
prereqs: [mimo-channel-model, kronecker-product, positive-definite-matrix]
see_also: [mimo-capacity, geometry-based-stochastic-channel-model, rayleigh-fading-channel, spatial-multiplexing, massive-mimo, pilot-contamination, eigenvalue, lmmse-channel-estimation]
sources:
  - paper: doi:10.1109/JSAC.2002.801223
    title: "Jean Philippe Kermoal, Laurent Schumacher, Klaus I. Pedersen, Preben E. Mogensen and Frank Frederiksen, A stochastic MIMO radio channel model with experimental validation, IEEE Journal on Selected Areas in Communications 20(6), 1211-1226, 2002"
    locator: the model with separate transmit and receive correlation matrices and its comparison with indoor measurements
  - paper: doi:10.1109/26.837052
    title: "Da-Shan Shiu, Gerard J. Foschini, Michael J. Gans and Joseph M. Kahn, Fading correlation and its effect on the capacity of multielement antenna systems, IEEE Transactions on Communications 48(3), 502-513, 2000"
    locator: "the abstract one-ring model, the separable form of the correlation and the effect of correlation on capacity"
  - book: isbn:9780521826150
    title: "Arogyaswami Paulraj, Rohit Nabar and Dhananjay Gore, Introduction to Space-Time Wireless Communications, Cambridge University Press, 2003"
    locator: "Chapter 3, Space-time propagation and channel models, and Chapter 4, Capacity of space-time channels (the effect of fading correlation)"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 7.3, Modeling of MIMO fading channels (angular domain representation and the degrees of freedom of physical channels)"
---

The Kronecker channel model adds correlation between antennas to the [MIMO channel model](/mimo-channel-model/) in the simplest way that keeps the statistics in two small matrices. It writes the channel as $H = R_r^{1/2} H_w R_t^{1/2}$, where $H_w$ has i.i.d. $\mathcal{CN}(0, 1)$ entries, $R_r$ is the correlation between receive antennas and $R_t$ the correlation between transmit antennas. The full covariance of the entries is then a [Kronecker product](/kronecker-product/), which gives the model its name. The model shows how correlation lowers the [MIMO capacity](/mimo-capacity/), but it assumes that the scattering at the two ends is independent, and it cannot describe keyhole channels.

## The machine

Fix two Hermitian [positive semidefinite](/positive-definite-matrix/) matrices $R_t \in \mathbb{C}^{N_t \times N_t}$ and $R_r \in \mathbb{C}^{N_r \times N_r}$ with all diagonal entries equal to 1. A channel draw is

$$H = R_r^{1/2} H_w R_t^{1/2}, \qquad [H_w]_{ik} \text{ i.i.d. } \mathcal{CN}(0, 1),$$

where $R^{1/2}$ is the Hermitian square root. The rest is the [MIMO channel model](/mimo-channel-model/): $y = Hx + w$ with $w \sim \mathcal{CN}(0, N_0 I)$, a total power $P$ and $\rho = P/N_0$. $H$ is zero-mean Gaussian, so the model is a correlated Rayleigh model. Its second moments are

$$\mathbb{E}[h_{ik} h_{jl}^*] = [R_r]_{ij}\, [R_t]_{lk}, \qquad \mathbb{E}[\mathrm{vec}(H)\, \mathrm{vec}(H)^H] = R_t^T \otimes R_r.$$

So the correlation between two entries is the product of a receive factor and a transmit factor. The unit diagonals give $\mathbb{E}|h_{ik}|^2 = 1$.

A common choice for a uniform linear array is the **exponential model** $[R]_{ij} = r^{|i - j|}$ with $0 \le r < 1$. Another is the correlation of a uniform array that sees a cluster of scatterers with a given mean angle and angular spread, as in the one-ring model of Shiu and coauthors.

## What it counts

The model is used to compute capacity, outage and error rates as a function of the eigenvalues of $R_t$ and $R_r$. It also gives the covariance that a [linear MMSE channel estimator](/lmmse-channel-estimation/) needs, and it is the standard model of spatial correlation in [massive MIMO](/massive-mimo/) analyses, where each user has its own $R_t$ seen from the base station.

## Relation to other models

- **i.i.d. Rayleigh** is the case $R_t = I$ and $R_r = I$.
- **Full correlation at one end.** If $R_t$ is the all-ones matrix, every transmit antenna sees the same column up to a common factor, and $H$ has rank one.
- **The unstructured Rayleigh model** allows any covariance $C$ of $\mathrm{vec}(H)$. The Kronecker model is the subset $C = R_t^T \otimes R_r$. A covariance of size $N_t N_r$ is reduced to two of sizes $N_t$ and $N_r$.
- **Weichselberger model.** It keeps a coupling matrix between the transmit and receive eigenvectors, so that each transmit eigenmode can reach only some receive eigenmodes. The Kronecker model is the case of a rank-one coupling.
- **Virtual or angular representation.** Tse and Viswanath describe $H$ in the angular domain, with independent gains between transmit and receive angle bins. Kronecker is the case where the variance of each pair of bins is a product.
- **Keyhole.** $H = h_r h_t^H$ with independent Rayleigh vectors has $\mathbb{E}[h_{ik} h_{jl}^*] = \delta_{ij} \delta_{kl}$, the same second moments as i.i.d. Rayleigh. So no model based on correlation matrices alone, Kronecker included, can tell it from the i.i.d. channel, yet it has rank one.
- **Geometry based models** such as the [geometry-based stochastic channel model](/geometry-based-stochastic-channel-model/) generate $H$ from clusters and paths; their correlation is not separable in general.

## Known results in the model

- **Rank** (theorem). With probability one, $\mathrm{rank}(H) = \min(\mathrm{rank}\, R_r, \mathrm{rank}\, R_t)$. The reason is that $H$ acts as an i.i.d. Gaussian matrix of size $\mathrm{rank}\, R_r \times \mathrm{rank}\, R_t$ between the two ranges, and such a matrix has full rank almost surely. So correlation that makes either matrix singular removes degrees of freedom.
- **High-SNR loss** (theorem for $N_t = N_r = n$ and invertible $R_t$, $R_r$). With CSIR and equal power, $\log_2 \det(I + (\rho/n) H H^H) - \log_2 \det(I + (\rho/n) H_w H_w^H)$ tends to $\log_2 \det R_r + \log_2 \det R_t$ as $\rho \to \infty$. By the Hadamard inequality, $\det R \le 1$ for a correlation matrix, so correlation never helps at high SNR.
- **Example** (Monte Carlo, 100000 draws, seed 11). For $2 \times 2$ with $R_t = R_r = \begin{pmatrix} 1 & r \\ r & 1 \end{pmatrix}$, the ergodic capacity in bits per use is:

| $r$ | 10 dB | 30 dB | high-SNR loss $2 \log_2(1 - r^2)$ |
|---|---|---|---|
| 0 | 5.55 | 17.76 | 0 |
| 0.5 | 5.12 | 16.95 | -0.83 |
| 0.9 | 4.05 | 13.36 | -4.79 |

  At 30 dB with $r = 0.5$, the loss 0.81 is close to the limit 0.83. With $r = 0.9$, the loss is 4.40, still on its way to 4.79. The keyhole channel, which has the same correlation as $r = 0$, gives only 3.74 and 10.18 bits.
- **Low SNR** (first-order expansion). With equal power on all antennas, the ergodic capacity is $\rho N_r / \ln 2$ to first order in $\rho$, whatever the correlation. If the transmitter knows $R_t$ and sends on its strongest eigenvector, the first-order term is $\rho N_r \lambda_{\max}(R_t) / \ln 2$. So transmit correlation helps at low SNR when the transmitter uses it.
- **Measurements.** Kermoal and coauthors fitted the model to indoor measurements and found a good match for the capacity of small arrays. Later measurements found that it can misstate the capacity of larger arrays, which led to models with coupling such as the Weichselberger model.

## References
