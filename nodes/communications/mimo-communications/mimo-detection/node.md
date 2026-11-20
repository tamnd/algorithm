---
tag: CA7C65
kind: problem
slug: mimo-detection
name: MIMO detection
aliases:
- MIMO detection problem
area: communications/mimo-communications
level: core
summary: "Recover the symbol vector x from y = Hx + w with H known. The ML form is a closest vector search over a finite set, NP-hard in general."
model: real-ram
complexity:
  vars: {n: the number of transmitted streams, m: the number of receive antennas, M: the constellation size}
  time: {worst: O(M^n n m)}
prereqs: [mimo-channel-model, symbol-detection, closest-vector-problem]
see_also: [multiuser-detection, spatial-multiplexing, fincke-pohst-enumeration, schnorr-euchner-enumeration, minimum-distance-detector, mimo-capacity, diversity-multiplexing-tradeoff, massive-mimo]
sources:
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 8.3, Receiver architectures (the decorrelator, successive cancellation and the MMSE receiver for spatial multiplexing)"
  - paper: doi:10.1007/BF01553893
    title: "Sergio Verdú, Computational complexity of optimum multiuser detection, Algorithmica 4, 1989"
    locator: "the statement that the jointly optimum detector for binary symbols is NP-hard in the number of users, by a reduction from maximum cut"
  - paper: "Daniele Micciancio, The hardness of the closest vector problem with preprocessing, IEEE Transactions on Information Theory 47(3), 2001"
    locator: "the main theorem: the closest vector problem stays NP-hard when the lattice is known in advance and may be preprocessed"
  - paper: "E. Agrell, T. Eriksson, A. Vardy and K. Zeger, Closest point search in lattices, IEEE Transactions on Information Theory 48(8) (2002)"
    locator: "pages 2201 to 2214 (closest point search as sphere decoding, with the Pohst and Schnorr-Euchner enumerations)"
  - paper: doi:10.1109/TSP.2005.843746
    title: "Joakim Jaldén and Björn Ottersten, On the complexity of sphere decoding in digital communications, IEEE Transactions on Signal Processing 53(4), 2005"
    locator: "the main result: for a fixed SNR, the expected number of nodes that the sphere decoder visits grows exponentially in the number of streams"
---

MIMO detection is the problem of deciding the vector of symbols that several transmit antennas sent at the same time, from what several receive antennas heard, when the receiver knows the channel. Each receive antenna gets a mix of all the transmitted symbols plus noise, as the [MIMO channel model](/mimo-channel-model/) describes. The exact maximum likelihood (ML) solution is the vector of constellation points whose image under the channel is nearest to the received vector. This is a [closest vector problem](/closest-vector-problem/) restricted to a finite set, and it is [NP-hard](/np-hard/) in general. The exhaustive search is affordable for a few streams with a small constellation. For more, receivers use exact searches that are fast on average at high SNR, such as [sphere decoding](/schnorr-euchner-enumeration/), or approximate detectors that run in polynomial time. The same problem with users in the place of antennas is [multiuser detection](/multiuser-detection/).

## In plain words

Several transmit antennas send their own symbols at the same time on the same frequency. Each receive antenna hears all of them at once, each with its own gain and phase, plus some noise. The receiver knows the gains, because it has measured them before. It must find out which symbol came from each antenna. It could try every possible combination of symbols and keep the one that explains the received signal best, but the number of combinations grows very fast with the number of antennas. So the real question is how to find the best combination, or a good one, quickly.

## Definition

There are $n$ transmit streams and $m$ receive antennas. In one channel use the receiver sees

$$y = H x + w, \qquad w \sim \mathcal{CN}(0, N_0 I_m),$$

where $H \in \mathbb{C}^{m \times n}$ is the channel matrix, $x \in \mathcal{S}^n$ is the symbol vector, and $\mathcal{S}$ is a constellation of $M$ points such as QAM or PSK, scaled to the mean energy $E_s = 1$. The SNR is $E_s / N_0$ per stream at each receive antenna.

**Input:** $y$, $H$, the constellation $\mathcal{S}$, and for some detectors $N_0$.

**Output:** a decision $\hat x \in \mathcal{S}^n$, or, for soft output, a log-likelihood ratio for each bit of each symbol.

**Goal:** a small error probability. The *ML* (jointly optimum) detector minimizes $P(\hat x \ne x)$ for equally likely vectors. Since the noise is white and Gaussian, it is

$$\hat x_{\text{ML}} = \arg\min_{x \in \mathcal{S}^n} \|y - H x\|^2.$$

The *individually optimum* detector minimizes each $P(\hat x_k \ne x_k)$ by summing the likelihood over the other streams. A *soft-output* detector gives the bit log-likelihood ratios that a channel decoder needs.

For $m \ge n$ and $H$ of full column rank, the QR decomposition $H = Q R$ with $Q \in \mathbb{C}^{m \times n}$ and $R$ upper triangular gives $\|y - H x\|^2 = \|Q^H y - R x\|^2 + \|(I - Q Q^H) y\|^2$. The last term does not depend on $x$. So the metric is a sum of $n$ terms, where term $k$ depends only on $x_k, \ldots, x_n$. This turns ML detection into a search in a tree of depth $n$ with $M$ branches per node, which is the basis of sphere decoding and of the [K-best detector](/k-best-detector/).

## Variants

- **Hard or soft output.** Hard output decides $\hat x$. Soft output gives bit LLRs, as the [list sphere decoder](/list-sphere-decoder/) does.
- **Joint or individual.** The jointly optimum detector minimizes the vector error rate, and the individually optimum one the symbol error rate of each stream. At high SNR they differ very little.
- **Real or complex.** For square QAM, the complex model of size $m \times n$ is the same as a real model of size $2m \times 2n$ with PAM symbols. Many algorithms use the real form.
- **Overloaded systems.** With $n > m$, $H$ has no left inverse. ML, MMSE and the tree searches with regularization still work. The zero-forcing detector does not.
- **Large systems.** With $n$ and $m$ in the tens to hundreds, as in [massive MIMO](/massive-mimo/) uplinks, only detectors with polynomial cost are used.
- **Imperfect channel knowledge.** The receiver has an estimate $\hat H$ instead of $H$. The ML metric with $\hat H$ is then mismatched.
- **Coded and iterative.** The detector and the channel decoder exchange soft values over several rounds, as in [turbo equalization](/turbo-equalization/).

## Examples

Take $m = n = 2$, BPSK with $\mathcal{S} = \{+1, -1\}$, the real channel

$$H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix},$$

and the received vector $y = (0.5, 0.6)$. The sent vector was $x = (+1, -1)$, with $H x = (1, 0)$ and noise $w = (-0.5, 0.6)$. ML compares all $M^n = 4$ candidates:

| candidate $x$ | $H x$ | $\|y - H x\|^2$ |
|---|---|---|
| $(+1, +1)$ | $(3, 2)$ | 8.21 |
| $(+1, -1)$ | $(1, 0)$ | 0.61 |
| $(-1, +1)$ | $(-1, 0)$ | 2.61 |
| $(-1, -1)$ | $(-3, -2)$ | 19.01 |

ML decides $(+1, -1)$, the sent vector. The [zero-forcing detector](/zero-forcing-mimo-detector/) computes $H^{-1} y = (-0.1, 0.7)$ and decides $(-1, +1)$, which is wrong in both streams. The two columns of $H$ have the correlation $3/\sqrt{10} = 0.949$, so inverting $H$ makes the noise much larger. With 16-QAM and $n = 8$, the same exhaustive table would have $16^8 \approx 4.3 \times 10^9$ rows, which is why the algorithms below exist.

## Known algorithms

| algorithm | idea | exact ML | cost per channel use |
|---|---|---|---|
| exhaustive search | evaluate all $M^n$ metrics | yes | $O(M^n n m)$ |
| sphere decoding: [Fincke-Pohst](/fincke-pohst-enumeration/), [Schnorr-Euchner](/schnorr-euchner-enumeration/) | depth-first tree search inside a radius | yes | exponential in $n$ in the worst case and in expectation |
| [zero-forcing](/zero-forcing-mimo-detector/) | apply the pseudoinverse, slice | no | $O(n^2 m + n^3 + n M)$ |
| [MMSE](/mmse-mimo-detector/) | apply $(H^H H + (N_0/E_s) I)^{-1} H^H$, slice | no | $O(n^2 m + n^3 + n M)$ |
| [V-BLAST](/v-blast/) | ordered nulling and cancelling | no | $O(n^3 m + n^4 + n M)$ as written, less with square-root forms |
| [D-BLAST](/d-blast/) | diagonal layers with coding, nulling and cancelling | no | per frame, see its page |
| [K-best](/k-best-detector/) | breadth-first tree search keeping $K$ nodes per level | only for $K \ge M^{n-1}$ | $O(n^2 m + n^3 + n^2 K + n K M \log(K M))$ |
| [list sphere decoder](/list-sphere-decoder/) | sphere search that keeps a list, for bit LLRs | yes, for the list | exponential in $n$ in the worst case |
| [lattice reduction aided](/lattice-reduction-aided-detection/) | LLL on the basis, then ZF or SIC | no | $O((S + 1) n^2 m + n^3 + n M)$ for $S$ swaps |
| [semidefinite relaxation](/semidefinite-relaxation-detection/) | relax to an SDP, round | no (certifies ML when tight) | polynomial in $n$ |
| [AMP](/amp-mimo-detection/) | message passing with a symbol denoiser | no | $O(T (n m + n M))$ for $T$ steps |
| [expectation propagation](/expectation-propagation-detection/) | Gaussian approximation refined by moment matching | no | $O(n^2 m + T (n^3 + n M))$ for $T$ steps |

The [minimum distance detector](/minimum-distance-detector/) is the case $n = 1$, where ML costs $O(M m)$.

## Bounds

- **Hardness.** With $H$ part of the input, ML detection is NP-hard. For BPSK with a real $H$, write $H = S A$, where $S$ has the columns of $H$ scaled to unit norm and $A$ is the diagonal matrix of the column norms. Then ML detection is the jointly optimum [multiuser detection](/multiuser-detection/) problem with the signatures $S$ and the amplitudes $A$, and every such problem is a MIMO instance. Verdú (1989) showed that problem NP-hard by a reduction from maximum cut ([NP-hardness of optimum multiuser detection](/multiuser-detection-np-hardness/)). No algorithm polynomial in $n$ is known.
- **Preprocessing does not remove the hardness.** In a block fading channel, $H$ stays the same for many received vectors, so a receiver may spend a lot of work on $H$ first. For the closest vector problem in general lattices, Micciancio (2001) showed that the problem stays NP-hard when the lattice is known in advance: the preprocessing may take any time, but if its output has polynomial size and the rest runs in polynomial time, then NP is contained in P/poly. This is a result for general lattices, not a direct statement about a finite constellation.
- **Exhaustive search.** It needs $M^n$ metrics of $O(n m)$ each, so $O(M^n n m)$ per vector.
- **Sphere decoding is exponential on average.** Hassibi and Vikalo (2005) found that the expected cost of sphere decoding is close to polynomial for small $n$ and a range of SNR. Jaldén and Ottersten (2005) proved that, for any fixed SNR, the expected number of visited nodes grows exponentially in $n$. Fast average behavior at high SNR and small $n$ does not contradict this.
- **Diversity of ML.** In i.i.d. Rayleigh fading with $H$ entries $\mathcal{CN}(0, 1)$, ML reaches the receive diversity $m$. For a fixed pair $x \ne x'$ with $d = x - x'$, $\|H d\|^2$ is $\|d\|^2$ times a sum of $m$ independent unit exponentials, so the pairwise error probability is at most $(1 + \|d\|^2 \mathrm{SNR} / 4)^{-m}$. A union bound over the finitely many pairs gives diversity at least $m$, and a single stream with $m$ antennas cannot have more.
- **Diversity of linear detectors.** The zero-forcing detector has diversity $m - n + 1$ in the same fading (see [diversity order](/diversity-order/)). So for $n = m$ it has diversity 1, against $m$ for ML.

## Reductions

- **To a box-constrained closest vector problem.** For square $M$-QAM, the real and imaginary parts take values $c(2 z - (\sqrt M - 1))$ with $z \in \{0, \ldots, \sqrt M - 1\}$ and a scale $c$. So ML detection is a closest vector search in the lattice $H \mathbb{Z}^{2n}$ (in real form) over a box of integer coefficients. Sphere decoding is the enumeration of the [closest vector problem](/closest-vector-problem/) with this box.
- **From maximum cut.** For BPSK, every instance of maximum cut maps to an ML instance, which gives the hardness above.
- **Relaxations.** Dropping the constraint $x \in \mathcal{S}^n$ gives a least squares problem whose solution is the zero-forcing estimate. Adding a Gaussian prior gives the MMSE estimate. For binary symbols, lifting $x x^T$ to a positive semidefinite matrix gives the [semidefinite relaxation](/semidefinite-relaxation-detection/).
- **Same as multiuser detection and equalization.** Replacing the antennas by users gives [multiuser detection](/multiuser-detection/). Replacing $H$ by a convolution matrix gives the equalization of intersymbol interference.

## Applications

- **Spatial multiplexing.** Every [spatial multiplexing](/spatial-multiplexing/) receiver solves MIMO detection, in Wi-Fi (802.11n and later) and in LTE and 5G NR.
- **Massive MIMO uplink.** A base station with many antennas detects many single-antenna users at once.
- **Space-time codes.** Codes without an orthogonal structure, such as the [Golden code](/golden-code/), need a general MIMO detector at the receiver.
- **Lattice-coded systems and precoding.** The same closest point search appears in [vector perturbation precoding](/vector-perturbation-precoding/) at the transmitter.

## References
