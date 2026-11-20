---
tag: 77A17Z
kind: definition
slug: orthogonal-space-time-block-codes
name: Orthogonal space-time block codes
aliases:
- OSTBC
area: communications/mimo-communications
level: core
summary: Space-time codes from orthogonal designs, which give full diversity and decouple the symbols at the receiver.
prereqs: [alamouti-code, mimo-channel-model, diversity-order]
see_also: [rank-and-determinant-criteria, golden-code, space-time-trellis-codes, diversity-multiplexing-tradeoff, maximal-ratio-combining, mimo-capacity, minimum-distance-detector, spatial-multiplexing]
sources:
  - paper: doi:10.1109/18.771146
    title: "Vahid Tarokh, Hamid Jafarkhani and A. Robert Calderbank, Space-time block codes from orthogonal designs, IEEE Transactions on Information Theory 45(5), 1456-1467, 1999"
    locator: "the definitions of real and complex orthogonal designs and their generalized forms, the linear maximum likelihood decoder, the existence results for real designs and the rate 1/2 and rate 3/4 complex codes"
  - paper: doi:10.1109/TIT.2003.818396
    title: "Xue-Bin Liang and Xiang-Gen Xia, On the nonexistence of rate-one generalized complex orthogonal designs, IEEE Transactions on Information Theory 49(11), 2984-2988, 2003"
    locator: the proof that rate-one generalized complex orthogonal designs do not exist for more than two antennas
  - paper: doi:10.1109/49.730453
    title: "Siavash M. Alamouti, A simple transmit diversity technique for wireless communications, IEEE Journal on Selected Areas in Communications 16(8), 1451-1458, 1998"
    locator: "the two-antenna code, the 2 by 2 complex orthogonal design"
  - book: isbn:9780521842914
    title: "Hamid Jafarkhani, Space-Time Coding - Theory and Practice, Cambridge University Press, 2005"
    locator: the chapters on orthogonal space-time block codes and on quasi-orthogonal space-time block codes
---

An orthogonal space-time block code (OSTBC) is a space-time block code whose codeword matrices have orthogonal rows of equal norm for every choice of the symbols. This one property gives two results: every pair of codewords differs by a full-rank matrix, so the code has the full [diversity order](/diversity-order/) $N_t N_r$, and the maximum likelihood decoder splits into one scalar decision per symbol. The [Alamouti code](/alamouti-code/) is the OSTBC for two antennas and the only complex one of rate one. For more antennas, complex OSTBCs exist only at lower rates, and the [golden code](/golden-code/) and other non-orthogonal codes trade the simple decoder for rate. The [rank and determinant criteria](/rank-and-determinant-criteria/) explain the diversity, and [space-time trellis codes](/space-time-trellis-codes/) are the trellis alternative.

## Definition

Rows are antennas and columns are time slots, as in the rest of this area. Let $s_1, \ldots, s_K$ be complex symbols.

A **complex orthogonal design** of size $N_t \times T$ is a matrix $X(s_1, \ldots, s_K)$ whose entries are $0$, $\pm s_k$ or $\pm s_k^*$, such that for all complex $s_1, \ldots, s_K$

$$X X^H = \left(\sum_{k=1}^{K} |s_k|^2\right) I_{N_t}.$$

The **generalized** form allows each entry to be a linear combination of $s_k$ and $s_k^*$ with the same identity. A **real orthogonal design** has real entries $0, \pm s_k$ and $X X^T = (\sum_k s_k^2) I$. The **rate** is $K/T$ symbols per channel use. The design is **square** if $T = N_t$.

An **orthogonal space-time block code** sends the codeword $\sqrt{a}\, X(s_1, \ldots, s_K)$ over $T$ uses of the [MIMO channel](/mimo-channel-model/) $Y = H \sqrt{a}\, X + W$, with the symbols from a constellation $\mathcal{A}$ and $a$ chosen to meet the power limit. With unit-energy symbols and entries $\pm s_k$, $\pm s_k^*$, the average energy per codeword is $a N_t K$; setting it to $T P$ gives $a = TP/(N_t K)$.

**Decoupled decoding (a theorem).** For any orthogonal design, $\mathrm{tr}(H X X^H H^H) = \|H\|_F^2 \sum_k |s_k|^2$, and $\mathrm{tr}(Y^H H X)$ is a real-linear function of the real and imaginary parts of the $s_k$. So the ML metric is

$$\|Y - \sqrt{a}\, H X\|_F^2 = \text{const} + a \|H\|_F^2 \sum_{k=1}^{K} \left| s_k - \frac{z_k}{\sqrt{a}\, \|H\|_F^2} \right|^2$$

for linear statistics $z_k$ of $Y$, and the ML decision is the nearest point of $\mathcal{A}$ to each $z_k / (\sqrt{a} \|H\|_F^2)$, one symbol at a time. Each symbol sees the SNR $a \|H\|_F^2 / N_0 = (T / (K N_t))\, \rho \|H\|_F^2$, the sum of all $N_t N_r$ channel gains, which is the output of [maximal ratio combining](/maximal-ratio-combining/) over $N_t N_r$ branches.

**Full diversity (a theorem).** For two codewords with symbol differences $e_k$, the difference $\Delta = X(e)$ satisfies $\Delta \Delta^H = (\sum_k |e_k|^2) I$, so it has full rank $N_t$, and by the rank criterion the diversity is $N_t N_r$.

## Examples and non-examples

**Alamouti, $N_t = 2$, rate 1.** $X = \begin{pmatrix} s_1 & -s_2^* \\ s_2 & s_1^* \end{pmatrix}$. Each symbol sees the SNR $(\rho/2) \|H\|_F^2$.

**Four antennas, rate 3/4.** Three symbols in four slots:

$$X = \begin{pmatrix} s_1 & s_2 & s_3 & 0 \\ -s_2^* & s_1^* & 0 & s_3 \\ -s_3^* & 0 & s_1^* & -s_2 \\ 0 & -s_3^* & s_2^* & s_1 \end{pmatrix}, \qquad X X^H = (|s_1|^2 + |s_2|^2 + |s_3|^2) I_4.$$

Removing any one row gives a rate 3/4 design for three antennas. With $T/(K N_t) = 4/12$, each symbol sees $(\rho/3) \|H\|_F^2$.

**Four antennas, rate 1/2.** Tarokh, Jafarkhani and Calderbank build a $4 \times 8$ design from the real $4 \times 4$ design

$$G(s) = \begin{pmatrix} s_1 & -s_2 & -s_3 & -s_4 \\ s_2 & s_1 & s_4 & -s_3 \\ s_3 & -s_4 & s_1 & s_2 \\ s_4 & s_3 & -s_2 & s_1 \end{pmatrix}$$

by placing $G(s)$ and $G(s^*)$ side by side: $X = [\,G(s)\ \ G(s^*)\,]$, with $X X^H = 2 \sum_k |s_k|^2 I_4$. It sends 4 symbols in 8 slots.

**Real designs.** Square real orthogonal designs of rate one exist only for $N_t = 2$, 4 and 8, a consequence of the Hurwitz-Radon theory. Generalized real designs of rate one exist for every $N_t$, for real constellations such as PAM.

**The rate limits for complex designs.**

- Rate one exists only for $N_t = 2$. Tarokh, Jafarkhani and Calderbank proved this for square designs; Liang and Xia proved it for generalized (non-square) designs in 2003.
- Liang (2003) showed that, for designs whose entries are $0$, $\pm s_k$ and $\pm s_k^*$, the largest rate for $N_t = 2m - 1$ or $2m$ antennas is $(m + 1)/(2m)$: 3/4 for three or four antennas, 2/3 for five or six.
- For $N_t \ge 3$ the rate is below 1, so an OSTBC cannot reach the [MIMO capacity](/mimo-capacity/) when $N_r \ge 2$, and even for $N_r = 1$ only the Alamouti code reaches it.

**Non-examples.**

- **Spatial multiplexing**, $X = (s_1, \ldots, s_{N_t})^T$ with $T = 1$: $X X^H = s s^H$ is not a multiple of $I$. Every difference matrix is a single column of rank one, so the diversity of uncoded multiplexing is at most $N_r$, even with an ML receiver.
- **Jafarkhani's quasi-orthogonal code** for four antennas sends four symbols in four slots. Its Gram matrix $X X^H$ has nonzero entries at positions (1, 4) and (2, 3), so pairs of symbols must be decoded jointly. It is not an OSTBC, but its rate is one.
- **The [golden code](/golden-code/)** sends four symbols in two slots on two antennas. Its difference matrices have full rank, but $X X^H$ is not a multiple of $I$, so the decoder must search jointly.
- **Delay diversity**, where antenna 2 sends the stream of antenna 1 one slot later, has full diversity with a suitable code but no orthogonal structure.

## Related definitions

- **Space-time block code.** Any map from $K$ symbols to an $N_t \times T$ matrix. A **linear dispersion code** has $X = \sum_k (A_k \mathrm{Re}\, s_k + j B_k \mathrm{Im}\, s_k)$ with fixed matrices; an OSTBC is the case in which the $A_k$ and $B_k$ satisfy conditions of Hurwitz-Radon type, among them $A_k A_l^H + A_l A_k^H = 2\delta_{kl} I$, the same for the $B_k$, and $A_k B_l^H = B_l A_k^H$ for all $k, l$.
- **Diversity order and coding gain.** Defined through the error slope and offset; for an OSTBC the coding gain is set by the minimum distance of the constellation, since all differences are scaled unitary matrices. See the [rank and determinant criteria](/rank-and-determinant-criteria/).
- **Quasi-orthogonal codes.** Codes whose Gram matrix is block diagonal, which allow rate one for four antennas at the cost of decoding pairs of symbols. Rotating the constellation of one symbol of each pair restores full diversity.
- **Differential space-time block codes.** Use the OSTBC structure to send data without channel knowledge at the receiver, with differential detection.
- **Diversity-multiplexing tradeoff.** An OSTBC of rate $K/T$ has the curve $N_t N_r (1 - rT/K)$, below the optimal [tradeoff](/diversity-multiplexing-tradeoff/) except at $r = 0$, and also at all $r$ for the Alamouti code on $2 \times 1$.

## References
