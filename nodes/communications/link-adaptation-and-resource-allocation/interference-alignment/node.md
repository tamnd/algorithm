---
tag: BAD5BM
kind: technique
slug: interference-alignment
name: Interference alignment
aliases:
- Cadambe-Jafar alignment
area: communications/link-adaptation-and-resource-allocation
level: research
summary: "Precode so interference at each receiver fills half its space. K users get K/2 degrees of freedom asymptotically, over time-varying or frequency-selective channels with ever longer symbol extensions."
prereqs: [mimo-capacity, zero-forcing-precoding, eigenvalue]
see_also: [zero-forcing-precoding, block-diagonalization, weighted-mmse-precoding, mimo-capacity, spatial-multiplexing, weighted-sum-rate-maximization, dirty-paper-coding, singular-value-decomposition]
sources:
  - paper: doi:10.1109/TIT.2008.926344
    title: "Viveck R. Cadambe and Syed A. Jafar, Interference alignment and degrees of freedom of the K-user interference channel, IEEE Transactions on Information Theory 54(8), 2008, pages 3425 to 3441"
    locator: "the K/2 degrees of freedom of the K-user interference channel with time-varying or frequency-selective coefficients, the alignment scheme over symbol extensions, the 3-user scheme over 2n + 1 symbols with 3n + 1 streams, and the closed form for the 3-user MIMO channel with constant coefficients"
  - paper: doi:10.1109/TIT.2008.926460
    title: "Mohammad Ali Maddah-Ali, Abolfazl S. Motahari and Amir K. Khandani, Communication over MIMO X channels: interference alignment, decomposition, and performance analysis, IEEE Transactions on Information Theory 54(8), 2008, pages 3457 to 3470"
    locator: "the alignment of interference in the two-user MIMO X channel, and the resulting gain in multiplexing over the interference channel"
---

Interference alignment is a way to choose the transmit beams of several users who share a band, so that at each receiver all the interference falls into one subspace, and the rest of the receive space is free for the wanted signal. In a $K$-user interference channel, each receiver has $K - 1$ interferers. Without alignment, each interferer takes its own dimensions, and the users must share the band, so the sum rate grows like $\log \mathrm{SNR}$ times a constant that does not grow with $K$. Cadambe and Jafar (2008) showed that, when the channel coefficients vary in time or frequency, the interference at every receiver can be packed into half of its signal space at once. Each user then gets half of its interference-free rate at high SNR, and the sum has $K/2$ degrees of freedom: the sum rate grows like $(K/2) \log_2 \mathrm{SNR}$. The $K/2$ is reached only in the limit: the scheme codes over symbol extensions, blocks of many channel uses, whose length grows without bound as the fraction approaches $1/2$. With multiple antennas and constant channels, a closed form works for three users, and iterative methods find aligned beams for small systems.

## In plain words

Many pairs of radios talk at the same time on the same frequency, and each receiver hears all the other senders as noise. A receiver can listen in several independent directions, like several separate ears. Normally each unwanted sender takes up some of these directions, and soon none are left for the wanted sender. Interference alignment chooses how each sender transmits so that, at every receiver, all the unwanted senders arrive from the same few directions. The receiver ignores those directions and listens in the others, where only its own sender is heard. With careful choices, every receiver can keep half of its directions clean. This only works fully when the channels change over time or frequency and the senders plan over very long blocks.

## When it applies

- **An interference network.** Several transmitter-receiver pairs share a band, each receiver wants only its own transmitter, and no pair can cancel the others' data (the transmitters do not share messages, unlike in [dirty paper coding](/dirty-paper-coding/)).
- **Channel knowledge at the transmitters.** Each transmitter must know the channels of all links, or at least those it affects, to compute its beam. This is global channel state information.
- **Enough dimensions.** Alignment needs spare signal dimensions: antennas, subcarriers or time slots. With constant channels and one antenna per node, the dimensions must come from symbol extensions over channels that vary, or from more abstract constructions.
- **High SNR.** The gain is in degrees of freedom, the slope of the sum rate against $\log_2 \mathrm{SNR}$. It shows at high SNR, where interference, not noise, limits the rates.
- **Generic channels.** The constructions need the channel matrices to be in general position, which holds with probability $1$ for continuous fading laws.

## The template

**Signal model.** Transmitter $j$ sends $d_j$ streams $x_j$ through a precoder $V_j$ (a matrix with $d_j$ columns). Receiver $k$ gets

$$y_k = H_{kk} V_k x_k + \sum_{j \ne k} H_{kj} V_j x_j + z_k,$$

where $H_{kj}$ is the channel from transmitter $j$ to receiver $k$ over all antennas and channel uses. Receiver $k$ applies a filter $U_k$ with $d_k$ columns.

**Alignment conditions.** The interference is removed when

$$U_k^H H_{kj} V_j = 0 \quad \text{for all } j \ne k, \qquad \operatorname{rank}\big(U_k^H H_{kk} V_k\big) = d_k.$$

The first condition says that all interference lies in the orthogonal complement of the columns of $U_k$; the second, that the wanted streams remain separable there. In terms of subspaces: at receiver $k$, the span of all $H_{kj} V_j$ with $j \ne k$ must have dimension at most $M_k - d_k$, where $M_k$ is the receive dimension.

**The 3-user 2x2 MIMO closed form.** Three pairs, two antennas each, one stream per user: $d_k = 1$ in $M_k = 2$ dimensions, so each receiver needs its two interferers on the same line. The three conditions are $H_{12} v_2 \parallel H_{13} v_3$, $H_{21} v_1 \parallel H_{23} v_3$ and $H_{31} v_1 \parallel H_{32} v_2$. The last two give $v_2$ and $v_3$ from $v_1$, and the first makes $v_1$ an eigenvector of a fixed matrix:

```pseudo id=main
ALIGN-THREE-USERS(H)
L1  E ← (H_13 H_23^{-1} H_21)^{-1} H_12 H_32^{-1} H_31
L2  v_1 ← an eigenvector of E
L3  v_2 ← H_32^{-1} H_31 v_1
L4  v_3 ← H_23^{-1} H_21 v_1
L5  for k ← 1 to 3: u_k ← a unit vector orthogonal to H_kj v_j for one j ≠ k
L6  return v_1, v_2, v_3 and u_1, u_2, u_3
```

Line L5 uses one interferer, since the other one is parallel to it. Each user then sends one stream free of interference, for $3$ streams in total, while any one pair alone could send $2$. With $M$ antennas at every node, the same idea gives three users $3M/2$ degrees of freedom; for odd $M$ it needs an extension over two channel uses.

**Symbol extensions.** With one antenna and coefficients that change in every channel use, take $n$ uses together: each $H_{kj}$ becomes an $n \times n$ diagonal matrix, and the alignment conditions are solved in this larger space. For three users, Cadambe and Jafar give user 1 $n + 1$ streams and users 2 and 3 $n$ streams each over $2n + 1$ uses, for $(3n + 1)/(2n + 1)$ degrees of freedom per use, which tends to $3/2$. For $K$ users, the construction aligns exactly in some dimensions and approximately in the count, and the fraction per user tends to $1/2$ as the extension grows.

## Classic examples

**A real 3-user example.** Take the integer channels

$$H_{11} = I, \ H_{12} = \begin{pmatrix} 1 & 2 \\ 0 & 1 \end{pmatrix}, \ H_{13} = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}, \ H_{21} = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}, \ H_{22} = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}, \ H_{23} = \begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix},$$

$$H_{31} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \ H_{32} = \begin{pmatrix} 1 & 1 \\ 1 & 2 \end{pmatrix}, \ H_{33} = \begin{pmatrix} 2 & 0 \\ 1 & 1 \end{pmatrix}.$$

Line L1 gives $E = \begin{pmatrix} 1 & 2 \\ -1 & -4 \end{pmatrix}$, with eigenvalues $(-3 \pm \sqrt{17})/2$. For $\lambda = (\sqrt{17} - 3)/2 = 0.5616$, $v_1 = (2, \lambda - 1) = (2, -0.4384)$, then $v_2 = (-2.8769, 2.4384)$ and $v_3 = (3.5616, 0.7808)$. At receiver 1, both interferers arrive along $(1, 1.2192)$; at receiver 2 along $(1, 0.4384)$; at receiver 3 along $(1, -4.5616)$. Each receiver projects onto the orthogonal line, where the wanted signal has a nonzero gain, so all three streams are free of interference. The other eigenvalue gives a second solution.

**The K-user interference channel.** With time-varying or frequency-selective channels and one antenna per node, the sum has $K/2$ degrees of freedom, reached in the limit of long symbol extensions; with two users, it is $1$, which time sharing already gets. For $K = 10$ users, each user gets about half its own interference-free rate at high SNR, while time sharing gives each one tenth.

**The X channel.** Two transmitters each have a message for each of two receivers. Maddah-Ali, Motahari and Khandani (2008) aligned the unwanted messages at each receiver; with $M$ antennas per node, the X channel has $4M/3$ degrees of freedom (Jafar and Shamai), more than the $M$ of the interference channel with two users.

## Variations

- **Iterative alignment.** For constant MIMO channels with more users, Gomadam, Cadambe and Jafar (2011) proposed alternating minimization of the leakage $\sum_k \sum_{j \ne k} \|U_k^H H_{kj} V_j\|_F^2$: fix the precoders and take $U_k$ as the eigenvectors of the smallest eigenvalues of the interference covariance at receiver $k$, then do the same for the reverse network. The leakage decreases at each step. A max-SINR version replaces leakage by the SINR and works better at moderate SNR.
- **Feasibility for constant channels.** With $K$ users, $M$ transmit and $N$ receive antennas and $d$ streams each, a necessary condition for alignment in general position is $M + N \ge (K + 1) d$; for some sizes it is also sufficient. Without extensions, constant channels allow only a fixed number of users to align.
- **Ergodic alignment.** With fading, pair each channel state with a complementary state and send the same symbols in both; the interference cancels in the sum. Each user gets half of its interference-free rate at every SNR, not only at high SNR.
- **Real interference alignment.** For constant scalar channels, alignment on rationally independent dimensions of the real line (lattice and number-theoretic arguments) also reaches $K/2$ for almost all channels, but only in the high-SNR limit.
- **Blind and partial alignment.** Schemes that exploit known patterns of channel change (for example reconfigurable antennas) need no channel knowledge at the transmitters, at a smaller gain.

## Pitfalls

- **K/2 is asymptotic.** The fraction $1/2$ per user is a limit over symbol extensions of growing length; any finite scheme gets less, for example $(3n + 1)/(2n + 1)$ for three users. With constant scalar channels and no extensions, alignment gives no gain.
- **Degrees of freedom are a high-SNR measure.** At low and moderate SNR, the noise boost of the receive projection can make alignment worse than treating interference as noise or than [weighted sum rate](/weighted-sum-rate-maximization/) methods such as [WMMSE](/weighted-mmse-precoding/).
- **Channel knowledge.** Every transmitter needs accurate channels of the whole network. Errors leave residual interference whose power grows with the transmit power, so the rate stops growing at high SNR unless the feedback precision grows like $\log \mathrm{SNR}$ bits per coefficient.
- **Long extensions.** The extension length needed for a fraction near $1/2$ grows very fast with $K$, and the channels must stay different across the uses of the extension.
- **Ill-conditioned channels.** When the channel matrices are close to singular, the closed form uses near-singular inverses, the wanted gain $|u_k^H H_{kk} v_k|$ can be tiny, and the scheme loses at any practical SNR.

## Exercises

1. In the 3-user 2x2 closed form, show that the two eigenvectors of $E$ give two different aligned solutions, and that if $E$ has a repeated eigenvalue with a single eigenvector, only one remains.
2. Verify the example: compute $H_{12} v_2$ and $H_{13} v_3$ and show that they are parallel.
3. Show that for $K = 2$ users with one antenna each, time sharing already gets $1$ degree of freedom, the same as $K/2$, so alignment gives nothing.
4. For three single-antenna users over $2n + 1$ channel uses, count the dimensions of the interference at receiver 1 when user 1 sends $n + 1$ streams and the others $n$ each, and explain why the interference must fill at most $n$ dimensions.
5. Write the leakage minimization for three 2x2 users as alternating steps, and show that the leakage does not increase from one step to the next.

## References
