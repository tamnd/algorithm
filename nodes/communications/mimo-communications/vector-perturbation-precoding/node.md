---
tag: RSA6ZS
kind: algorithm
slug: vector-perturbation-precoding
name: Vector perturbation precoding
aliases:
- vector perturbation
area: communications/mimo-communications
level: advanced
summary: Adds an integer offset to the data before channel inversion, chosen by a lattice search to cut transmit power.
model: real-ram
complexity:
  vars: {M: the number of base station antennas, K: the number of single-antenna users, N: the number of nodes the lattice search visits}
  time: {worst: "O(K^2 M + K^3 + N K)"}
  space: {extra: O(M K)}
properties: {deterministic: true, linear: false, needs_channel_at_transmitter: true, zero_interference: true, exact_search: true, receiver_uses_modulo: true}
history:
  year: 2005
  people: [Bertrand M. Hochwald, Christian B. Peel, A. Lee Swindlehurst]
  note: "Hochwald, Peel and Swindlehurst introduced vector perturbation in Part II of their 2005 paper, after Part I had shown the poor sum rate of plain channel inversion."
prereqs: [zero-forcing-precoding, closest-vector-problem, schnorr-euchner-enumeration]
see_also: [regularized-zero-forcing-precoding, tomlinson-harashima-precoding, dirty-paper-coding, lattice-reduction-aided-detection, babai-nearest-plane, lll-algorithm, fincke-pohst-enumeration, cholesky-decomposition]
sources:
  - paper: doi:10.1109/TCOMM.2004.841997
    title: "Bertrand M. Hochwald, Christian B. Peel and A. Lee Swindlehurst, A vector-perturbation technique for near-capacity multiantenna multiuser communication, Part II: perturbation, IEEE Transactions on Communications 53(3), 537-544, 2005"
    locator: the perturbed channel inverse, the choice of tau, the modulo receiver, the sphere encoder and the regularized form
  - paper: doi:10.1109/TCOMM.2004.840638
    title: "Christian B. Peel, Bertrand M. Hochwald and A. Lee Swindlehurst, A vector-perturbation technique for near-capacity multiantenna multiuser communication, Part I: channel inversion and regularization, IEEE Transactions on Communications 53(1), 195-202, 2005"
    locator: the loss of plain channel inversion that motivates the perturbation
  - paper: doi:10.1109/TIT.2002.800499
    title: "Erik Agrell, Thomas Eriksson, Alexander Vardy and Kenneth Zeger, Closest point search in lattices, IEEE Transactions on Information Theory 48(8), 2201-2214, 2002"
    locator: the Schnorr-Euchner enumeration for the closest point problem with an upper triangular generator
  - paper: doi:10.1007/BF01581144
    title: "Claus P. Schnorr and M. Euchner, Lattice basis reduction: improved practical algorithms and solving subset sum problems, Mathematical Programming 66, 181-199, 1994"
    locator: the enumeration order that visits candidates by their distance from the center
---

Vector perturbation (VP) precoding sends $x = \sqrt{P / \gamma}\, H^H (H H^H)^{-1} (s + \tau l)$ in a multiuser downlink, where $l$ is a vector of complex integers chosen to make the power $\gamma$ of the unscaled signal as small as possible. With $l = 0$ it is [zero-forcing precoding](/zero-forcing-precoding/) with channel inversion, which can need very much power when $H H^H$ is badly conditioned. The perturbation moves the data to another copy of itself on a grid of spacing $\tau$, and each user removes the offset with a modulo operation. Unlike [regularized zero-forcing precoding](/regularized-zero-forcing-precoding/), which accepts some interference to save power, VP keeps zero interference and saves power by the nonlinear offset; it can also be combined with the regularized inverse. It is the vector form of [Tomlinson-Harashima precoding](/tomlinson-harashima-precoding/): Tomlinson-Harashima precoding chooses the offsets one user at a time, while VP chooses them jointly by a lattice search.

## In plain words

A base station sends to several users at once and cancels the leaks between them. When two users are in similar directions, this canceling costs much power, and every user then hears a weak signal. Vector perturbation changes the data a little before the canceling. It adds a whole number of fixed steps to each symbol. Each user can remove these steps again, because it only looks at its symbol "modulo one step", like a clock that only shows the time and not the day. The base station tries the possible steps and picks the combination that needs the least power. The saving can be large, and users get a stronger signal.

## The problem

User $k$ receives $y_k = h_k^H x + w_k$, with $H = [h_1, \ldots, h_K]^H \in \mathbb{C}^{K \times M}$ of full row rank known at the base station and $w_k \sim \mathcal{CN}(0, N_0)$. The symbols $s_k$ come from a square QAM constellation whose real and imaginary parts lie in $[-\tau/2, \tau/2)$; Hochwald, Peel and Swindlehurst take $\tau = 2(|c|_{\max} + \Delta / 2)$, with $|c|_{\max}$ the largest absolute value of a real or imaginary part and $\Delta$ the distance between neighbor points. For QPSK with points $\pm 1 \pm j$ this gives $\tau = 4$, and for 16-QAM with parts in $\{\pm 1, \pm 3\}$ it gives $\tau = 8$. Every transmit vector must have power $P$. The goal is to choose $l \in (\mathbb{Z} + j \mathbb{Z})^K$ that minimizes

$$\gamma(l) = \|H^H (H H^H)^{-1} (s + \tau l)\|^2 = (s + \tau l)^H (H H^H)^{-1} (s + \tau l),$$

because the effective SNR of every user is $P / (\gamma N_0)$. This is an instance of the [closest vector problem](/closest-vector-problem/).

## The algorithm

```pseudo id=main
VP-PRECODE(H, s, P, τ)
L1  F ← Hᴴ (H Hᴴ)⁻¹                              ▷ the zero-forcing directions
L2  A ← (H Hᴴ)⁻¹                                 ▷ γ = uᴴ A u
L3  Aᵣ ← real form of A;  L Lᵀ ← Aᵣ;  R ← Lᵀ      ▷ uᴴ A u = ‖R v‖²
L4  l ← argmin over integer z of ‖R (v + τ z)‖²   ▷ Schnorr-Euchner search
L5  u ← s + τ l
L6  γ ← ‖F u‖²
L7  return x = √(P / γ) F u

VP-RECEIVE(y_k, γ, P, τ)
L8  return mod_τ(√(γ / P) y_k)                    ▷ real and imaginary parts into [-τ/2, τ/2)
```

Line L3 writes $u = a + j b$ as $v = (a, b) \in \mathbb{R}^{2K}$ and $A = A_R + j A_I$ as the real matrix $\begin{pmatrix} A_R & -A_I \\ A_I & A_R \end{pmatrix}$, and factors it with the [Cholesky decomposition](/cholesky-decomposition/). Line L4 is a depth-first [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/) from the last coordinate to the first: at each level it visits the integers in the order of their distance from the real center, and it stops a branch as soon as the partial sum reaches the best value found so far. The first path it follows is the [Babai nearest plane](/babai-nearest-plane/) point. Lines L1 to L3 depend only on $H$, so they run once per channel; lines L4 to L7 run once per data vector.

## Example

Take $K = M = 2$, QPSK with $\tau = 4$, $P = 4$ and

$$H = \begin{pmatrix} 1 & 2 \\ 0 & 1 \end{pmatrix}, \qquad H^{-1} = \begin{pmatrix} 1 & -2 \\ 0 & 1 \end{pmatrix}, \qquad s = \begin{pmatrix} 1 + j \\ -1 - j \end{pmatrix}.$$

Here $F = H^{-1}$. Without a perturbation, $F s = (3 + 3j, -1 - j)$ and $\gamma = 18 + 2 = 20$. The search finds $l = (-1 - j, 0)$, so $u = (-3 - 3j, -1 - j)$ and $F u = (-1 - j, -1 - j)$, with $\gamma = 4$. The real and the imaginary parts of this example are the same real problem. In real terms, the cost of $(u_1, u_2)$ is $(u_1 - 2 u_2)^2 + u_2^2$ for $u_1 \in 1 + 4 \mathbb{Z}$ and $u_2 \in -1 + 4 \mathbb{Z}$; the value 1 + 1 = 2 at $(-3, -1)$ is the smallest, and the next smallest is 10.

Line L7 sends $x = \sqrt{4 / 4}\, F u = (-1 - j, -1 - j)$, with power 4. Without noise the users receive $H x = (-3 - 3j, -1 - j)$. User 1 reduces $-3 - 3j$ modulo 4 into $[-2, 2)$ and gets $1 + j$; user 2 gets $-1 - j$ directly. Zero forcing would send $\sqrt{4 / 20}\, F s$, and each user would receive $0.447\, s_k$. For this data vector the perturbation raises the effective SNR by the factor $20 / 4 = 5$, or 7.0 dB.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Lemma 1 shows that $H F = I$, so the users hear no signal for the other users for every $l$, and that line L7 meets the power exactly. Lemma 2 shows that the modulo of line L8 removes $\tau l_k$ and returns $s_k$ without noise. Lemmas 3 and 4 show that $\gamma$ equals $\|R (v + \tau z)\|^2$ in real form. Theorem 1 shows that the Schnorr-Euchner search stops and returns a global minimizer over all integer vectors: the terms are nonnegative, so a partial sum is a lower bound for every completion, and the zigzag order makes the bounds at one level grow, so the search can stop a level at the first candidate that is not better.

## Complexity

Lines L1 to L3 cost $O(K^2 M + K^3)$ per channel. Line L4 costs $O(K)$ per visited node of the search tree, so $O(N K)$ for $N$ nodes. Lines L6 and L7 cost $O(M K)$. In the worst case $N$ grows exponentially with $K$; the closest vector problem is NP-hard in general, so no exact method is known to be polynomial. For small $K$ and well conditioned channels $N$ is small. The extra space is $O(M K)$ for $F$ and $O(K^2)$ for $R$.

## Properties

- **Zero interference.** $H x$ is a scaled copy of $s + \tau l$ for every $l$ (theorem).
- **Never worse than channel inversion.** $l = 0$ is a candidate, so $\gamma_{\mathrm{VP}} \le \gamma_{\mathrm{ZF}}$ for every channel and data vector.
- **Nonlinear.** The transmit signal is not a linear function of $s$, because $l$ depends on $s$.
- **Simple receiver.** Each user needs only a scale and a modulo, and no knowledge of the other users.
- **Common scale.** The scale $\sqrt{\gamma / P}$ changes with every data vector, so each user must know it or estimate it.
- **Large power saving on bad channels.** The saving is largest when $H H^H$ is close to singular, which is when channel inversion fails.

## Variants and improvements

- **Regularized VP.** Replace $(H H^H)^{-1}$ by $(H H^H + \alpha I)^{-1}$ in the search and in the precoder, as in Part II of Hochwald, Peel and Swindlehurst. Then some interference remains, but less noise is amplified, which helps at low SNR.
- **Approximate search.** Round the center at each level once ([Babai nearest plane](/babai-nearest-plane/)), or keep the $B$ best partial vectors per level, to bound the cost.
- **Lattice reduction.** Reduce the basis $\tau R$ with the [LLL algorithm](/lll-algorithm/) first and then round; the result is a good approximate perturbation at polynomial cost, the transmit counterpart of [lattice-reduction-aided detection](/lattice-reduction-aided-detection/).
- **Tomlinson-Harashima precoding.** Choose $l_k$ one user at a time after a QR factorization of $H$, which is the successive form of VP; see [Tomlinson-Harashima precoding](/tomlinson-harashima-precoding/).
- **Other enumerations.** The [Fincke-Pohst enumeration](/fincke-pohst-enumeration/) searches in the natural order inside a fixed radius.

## When to use it

Use VP when the base station has accurate channel knowledge, the number of users is close to the number of antennas, and the base station can afford a lattice search per data vector. These are the cases where linear precoders lose much power. When $K$ is much smaller than $M$, $H H^H$ is well conditioned and [zero-forcing precoding](/zero-forcing-precoding/) or [regularized zero-forcing precoding](/regularized-zero-forcing-precoding/) is almost as good at a much lower cost. When the search is too costly, use Tomlinson-Harashima precoding or a lattice-reduction-aided approximation.

## Pitfalls

- **The modulo needs the right $\tau$.** If $\tau$ is too small the constellation copies overlap and the modulo receiver makes errors without noise.
- **Modulo loss.** Noise near the edge of $[-\tau/2, \tau/2)$ wraps to the other side, and the perturbed signal has a different energy per symbol than the plain constellation. Compare VP with linear precoders at the same transmit power and with the same receiver.
- **Soft decisions.** The modulo makes the log-likelihood ratios for a channel decoder harder to compute, because each symbol has many copies.
- **Search cost.** The worst-case cost of an exact search grows exponentially with $K$; set a node limit in real time systems, and accept a small loss.
- **Stale channel.** A wrong $H$ leaves interference that is then also reduced modulo $\tau$, which can map it to a large error.

## Implementations

## History

Tomlinson (1971) and Harashima and Miyakawa (1972) used a modulo at the transmitter and the receiver to remove intersymbol interference. Peel, Hochwald and Swindlehurst (2005, Part I) showed that channel inversion in a multiuser downlink with as many users as antennas has a poor sum rate, and introduced the regularized inverse. In Part II, Hochwald, Peel and Swindlehurst (2005) added the integer perturbation of the data, chose it with a sphere search, and reported performance close to the sum capacity at high SNR. The search builds on the enumeration of Schnorr and Euchner (1994) and on the survey of closest point search by Agrell, Eriksson, Vardy and Zeger (2002). Later work replaced the exact search by lattice-reduction-aided approximations.

## References
