---
tag: 8A69CT
kind: technique
slug: hybrid-beamforming
name: Hybrid beamforming
aliases:
- hybrid analog-digital precoding
area: communications/mimo-communications
level: research
summary: Splits the precoder into an analog network of phase shifters and a small digital precoder, so that a large array needs only a few RF chains. Common at millimeter wave.
prereqs: [svd-precoding, beamforming, orthogonal-matching-pursuit]
see_also: [massive-mimo, codebook-based-precoding, zero-forcing-precoding, compressed-sensing, delay-and-sum-beamforming, mimo-capacity, spatial-multiplexing, reconfigurable-intelligent-surface]
sources:
  - paper: doi:10.1109/TWC.2014.011714.130846
    title: "Omar El Ayach, Sridhar Rajagopal, Shadi Abu-Surra, Zhouyue Pi and Robert W. Heath Jr., Spatially sparse precoding in millimeter wave MIMO systems, IEEE Transactions on Wireless Communications 13(3), 1499-1513, 2014"
    locator: "the hybrid precoder F_RF F_BB with constant-modulus analog entries, the design as a sparse approximation of the optimal unconstrained precoder, and its solution by orthogonal matching pursuit over the array response vectors"
  - paper: doi:10.1109/JSTSP.2016.2520912
    title: "Foad Sohrabi and Wei Yu, Hybrid digital and analog beamforming design for large-scale antenna arrays, IEEE Journal of Selected Topics in Signal Processing 10(3), 501-513, 2016"
    locator: "the result that a hybrid structure with at least twice as many RF chains as data streams can realize any fully digital beamformer, and heuristic designs with fewer RF chains and finite-resolution phase shifters"
  - book: isbn:9780521762281
    title: "Robert W. Heath Jr. and Angel Lozano, Foundations of MIMO Communication, Cambridge University Press, 2018"
    locator: "the parts on hybrid precoding and on the channel model with a few propagation paths for large arrays"
---

Hybrid beamforming is a way to build the precoder of a large antenna array with fewer radio frequency (RF) chains than antennas. The transmitter sends $x = F_{RF} F_{BB}\, s$, where $F_{BB}$ is a small digital precoder that mixes $N_s$ data streams into $N_{RF}$ RF chains, and $F_{RF}$ is an analog network of phase shifters that connects each RF chain to all $n$ antennas. The phase shifters can change only the phase of a signal, so every entry of $F_{RF}$ has the same modulus. A fully digital precoder, such as [SVD precoding](/svd-precoding/), needs one RF chain (a mixer, a filter and a data converter) per antenna, which costs too much power and money for arrays of 64 to 256 antennas at millimeter wave. The design problem is to choose the two factors so that their product is close to the best digital precoder. [Codebook-based precoding](/codebook-based-precoding/) also restricts the precoder, but because of the feedback link, not because of the hardware.

## In plain words

A large antenna array can aim a narrow beam, but a full radio behind every antenna is expensive and uses much power. A hybrid design puts only a few full radios behind the array. Each radio drives all the antennas through a network of cheap phase shifters, which can delay the signal on each antenna but cannot make it stronger or weaker. The phase shifters do the coarse aiming, and the few radios do the fine mixing of the data streams.

At high frequencies the signal reaches the receiver along only a few paths. So a few beams, one for each strong path, are enough, and a few radios can do almost as well as one radio per antenna.

## When it applies

- The array is large ($n$ from 16 to several hundred) and the number of streams is small, $N_s \le N_{RF} \ll n$.
- The channel has few strong paths, as at millimeter wave. With $L$ paths, the channel matrix has rank at most $L$, and its row space is spanned by the $L$ array response vectors.
- The cost or power of the RF chains matters more than a small loss in rate.
- The analog network is narrowband or the same over the band: one $F_{RF}$ serves all subcarriers of an OFDM symbol, and only $F_{BB}$ can change per subcarrier.

## The template

**Model.** The link is $y = H F_{RF} F_{BB}\, s + w$ with $H \in \mathbb{C}^{m \times n}$, $\mathbb{E}[s s^H] = (P/N_s) I$, $w \sim \mathcal{CN}(0, N_0 I)$, $\rho = P/N_0$, $|[F_{RF}]_{ij}| = 1/\sqrt{n}$ for all entries, and the power constraint $\|F_{RF} F_{BB}\|_F^2 = N_s$. With an optimal receiver the rate is

$$R = \log_2 \det\!\left(I_m + \frac{\rho}{N_s} H F_{RF} F_{BB} F_{BB}^H F_{RF}^H H^H\right)$$

in bits per channel use. For a uniform linear array with half-wavelength spacing, the array response at angle $\phi$ is $a(\phi) = \frac{1}{\sqrt{n}} (1, e^{j\pi \sin\phi}, \ldots, e^{j\pi (n-1)\sin\phi})^T$, and a channel with $L$ paths is

$$H = \sqrt{\frac{n m}{L}} \sum_{l=1}^{L} \alpha_l\, a_r(\theta_l)\, a_t(\phi_l)^H.$$

**Spatially sparse precoding (El Ayach et al. 2014).** Let $F_{opt}$ be the first $N_s$ right singular vectors of $H$. Minimize $\|F_{opt} - F_{RF} F_{BB}\|_F$ with the columns of $F_{RF}$ taken from a dictionary $A_t$ of array response vectors, which all have constant modulus. This is a sparse approximation problem, and [orthogonal matching pursuit](/orthogonal-matching-pursuit/) solves it greedily:

1. Set the residual $F_{res} = F_{opt}$ and let $F_{RF}$ be empty.
2. Repeat $N_{RF}$ times: compute $\Psi = A_t^H F_{res}$, take the dictionary column $k$ with the largest row energy $\sum_j |\Psi_{kj}|^2$, and append it to $F_{RF}$.
3. After each step, set $F_{BB} = (F_{RF}^H F_{RF})^{-1} F_{RF}^H F_{opt}$, the least squares fit, and set $F_{res} = (F_{opt} - F_{RF} F_{BB}) / \|F_{opt} - F_{RF} F_{BB}\|_F$.
4. Scale $F_{BB} \leftarrow \sqrt{N_s}\, F_{BB} / \|F_{RF} F_{BB}\|_F$ to meet the power constraint.

With a dictionary of $D$ columns, one iteration costs $O(D n N_s)$ for the correlations and $O(n N_{RF}^2)$ for the least squares fit, in the real-RAM model, once per channel realization.

**Two facts with proofs.**

*Fact 1 (a sparse channel needs few RF chains).* If the dictionary holds the $L$ true array response vectors $a_t(\phi_l)$ and $N_{RF} \ge L$, a hybrid precoder can equal $F_{opt}$ exactly. Proof: every row of $H$ is a combination of the vectors $a_t(\phi_l)^H$, so the row space of $H$ lies in $\mathrm{span}\{a_t(\phi_l)\}$ after conjugation, and the right singular vectors with nonzero singular values lie in this span. So $F_{opt} = A_t B$ for some $L \times N_s$ matrix $B$, and $F_{RF} = A_t$ (constant modulus) with $F_{BB} = B$ gives $F_{RF} F_{BB} = F_{opt}$.

*Fact 2 (twice as many RF chains as streams is enough for any precoder, Sohrabi and Yu 2016).* For every $F \in \mathbb{C}^{n \times N_s}$ there is a hybrid factorization with $N_{RF} = 2 N_s$ and unit-modulus analog entries. Proof: if $F = 0$ take $F_{BB} = 0$. Otherwise let $c = \max_{ij} |F_{ij}| / 2 > 0$, and write $F_{ij}/c = r_{ij} e^{j\psi_{ij}}$ with $0 \le r_{ij} \le 2$. Let $\delta_{ij} = \arccos(r_{ij}/2)$. Then $e^{j(\psi_{ij} + \delta_{ij})} + e^{j(\psi_{ij} - \delta_{ij})} = 2\cos(\delta_{ij})\, e^{j\psi_{ij}} = r_{ij} e^{j\psi_{ij}}$. Put these two phases into two $n \times N_s$ matrices $A_1$ and $A_2$ with unit-modulus entries. Then $F_{RF} = [A_1\ A_2]$ and $F_{BB} = c \begin{pmatrix} I \\ I \end{pmatrix}$ give $F_{RF} F_{BB} = c (A_1 + A_2) = F$. The scale $1/\sqrt{n}$ of the template moves into $F_{BB}$. With more than $2 N_s$ chains, give the extra chains zero rows in $F_{BB}$.

## Classic examples

**A three-path channel.** Take $n = 16$ transmit antennas, $m = 4$ receive antennas, $L = 3$ paths with gains $\alpha = (1,\ 0.6 e^{j},\ 0.3 e^{-2j})$, angles of departure $(10°, -30°, 45°)$ and angles of arrival $(0°, 20°, -40°)$, both arrays uniform linear with half-wavelength spacing, and $\rho = 10$ (10 dB). The squared singular values of $H$ are 22.29, 6.15 and 1.78. The dictionary is the three true array response vectors. The rates in bits per channel use:

| precoder | $N_s = 1$ | $N_s = 2$ |
|---|---|---|
| fully digital, $F_{opt}$ | 7.807 | 11.801 |
| hybrid by OMP, $N_{RF} = N_s$ | 7.698 | 11.787 |
| hybrid by OMP, $N_{RF} = 3 = L$ | 7.807 | 11.801 |
| equal power on all antennas, no precoding | 7.254 (with all 16 RF chains) | |

With one RF chain, OMP picks the strongest path, so the hybrid precoder is analog beam steering toward $10°$, and it loses 0.11 bits. With $N_{RF} = L = 3$, Fact 1 applies, and the hybrid precoder is exact. With $N_s = 2$ and $N_{RF} = 2$, OMP picks the paths at $-30°$ and $10°$, and the residual $\|F_{opt} - F_{RF} F_{BB}\|_F$ is 0.111.

**Analog-only beamforming.** With $N_{RF} = N_s = 1$ and $F_{BB} = 1$, the precoder is a single phase-only beam. For a single-path channel this is optimal, because $F_{opt} = a_t(\phi_1)$ already has constant modulus. It is the transmit version of [delay-and-sum beamforming](/delay-and-sum-beamforming/).

**Massive MIMO downlink.** In a multiuser downlink with $K$ single-antenna users, a common two-stage design sets each column of $F_{RF}$ to the phases of the conjugate channel of one user (phase-only matched filtering), so $N_{RF} = K$, and then applies [zero-forcing precoding](/zero-forcing-precoding/) to the effective $K \times K$ channel $H F_{RF}$ in the digital stage.

## Variations

- **Fully connected and partially connected.** In the fully connected network each RF chain drives every antenna through its own phase shifter, $n N_{RF}$ phase shifters in total. In the partially connected (subarray) network each RF chain drives only $n / N_{RF}$ antennas, which needs $n$ phase shifters and no combiners, at a loss in beamforming gain.
- **Hybrid combining at the receiver.** The receiver uses the same structure, $W_{RF} W_{BB}$, and the two sides are often designed one after the other.
- **Finite-resolution phase shifters.** With $b$-bit phase shifters each phase is rounded to a multiple of $2\pi / 2^b$. Designs either round a continuous solution or optimize over the discrete set by coordinate updates.
- **Wideband design.** In OFDM, $F_{BB}[k]$ changes per subcarrier but $F_{RF}$ is common, and the design approximates all $F_{opt}[k]$ at once by simultaneous OMP.
- **Alternating optimization.** In place of OMP, alternate between $F_{BB}$ (a least squares fit for fixed $F_{RF}$) and the phases of $F_{RF}$ (a projection onto unit modulus for fixed $F_{BB}$). This needs no dictionary but converges only to a local solution.

## Pitfalls

- **Dictionary mismatch.** OMP with a dictionary on a grid of angles, not the true angles, cannot reach Fact 1, and the loss grows with the grid spacing. The true angles are not known without channel estimation.
- **Channel estimation through few RF chains.** The receiver sees the antennas only through $N_{RF}$ combinations, so it cannot measure all $m n$ channel entries at once. Beam training or [compressed sensing](/compressed-sensing/) over the sparse paths is needed, and its errors enter the precoder.
- **Approximating the wrong target.** OMP minimizes the distance to $F_{opt}$, not the rate. A small Frobenius error usually gives a small rate loss, but the two are not the same objective.
- **Power normalization.** Forgetting step 4 gives a precoder that uses more or less than the allowed power, and the rate comparison is then wrong.
- **Beam squint.** Phase shifters give the same phase at all frequencies, but the correct phase of an array response changes with frequency. Over a very wide band the beam points in different directions at the edges of the band. True time delay elements avoid this.
- **Overstating Fact 2.** Fact 2 needs $N_{RF} \ge 2 N_s$ and ideal phase shifters with continuous phases and a combiner for every RF chain. With fewer RF chains or quantized phases the hybrid precoder is only an approximation.

## Exercises

1. Show that for a single-path channel, $H = \sqrt{nm}\, \alpha\, a_r(\theta) a_t(\phi)^H$, the best single-stream precoder is $a_t(\phi)$, and compute the SNR gain over one antenna.
2. Write the complex number $1.5 e^{j 0.3}$ as a sum of two numbers of modulus 1, as in the proof of Fact 2, and give the two phases.
3. Show that Fact 2 is tight in the sense that one RF chain per stream cannot realize every precoder: give a vector in $\mathbb{C}^2$ that is not a scalar multiple of a vector with entries of equal modulus.
4. Count the phase shifters, RF chains and complex multiplications per symbol vector for a fully connected design with $n = 64$, $N_{RF} = 4$ and $N_s = 2$, and compare with a fully digital design.
5. In the three-path example with $N_s = 2$, the first OMP step finds the row energies 0.992, 0.995 and 0.021 for the paths at $10°$, $-30°$ and $45°$. Explain why the two strong paths get almost the same score, although their gains are 1 and 0.6, and why the order of selection does not change the result for $N_{RF} = 2$.

## References
