---
tag: 3XWDT5
kind: definition
slug: space-time-trellis-codes
name: Space-time trellis codes
aliases:
- STTC
area: communications/mimo-communications
level: advanced
summary: Trellis codes whose outputs are sent over several antennas, giving both diversity and coding gain.
prereqs: [rank-and-determinant-criteria, trellis-coded-modulation, viterbi-algorithm]
see_also: [alamouti-code, orthogonal-space-time-block-codes, golden-code, diversity-multiplexing-tradeoff, convolutional-code, trellis, mimo-channel-model, diversity-order]
sources:
  - paper: doi:10.1109/18.661517
    title: "Vahid Tarokh, Nambi Seshadri and A. Robert Calderbank, Space-time codes for high data rate wireless communication - performance criterion and code construction, IEEE Transactions on Information Theory 44(2), 744-765, 1998"
    locator: "the definition of space-time trellis codes, the bound on the number of states, the 4-PSK and 8-PSK codes for two antennas and their Viterbi decoding"
  - book: isbn:9780521842914
    title: "Hamid Jafarkhani, Space-Time Coding - Theory and Practice, Cambridge University Press, 2005"
    locator: the chapters on space-time trellis codes and super-orthogonal space-time trellis codes
  - book: isbn:9780521826150
    title: "Arogyaswami Paulraj, Rohit Nabar and Dhananjay Gore, Introduction to Space-Time Wireless Communications, Cambridge University Press, 2003"
    locator: "Chapter 6, Space-time coding without channel knowledge at the transmitter (space-time trellis codes)"
---

A space-time trellis code (STTC) is a trellis code in which each branch of the trellis carries $N_t$ symbols, one for each transmit antenna, all sent at the same time. Tarokh, Seshadri and Calderbank introduced these codes in 1998 together with the [rank and determinant criteria](/rank-and-determinant-criteria/), and chose the branch labels so that every pair of paths through the trellis gives a full-rank difference matrix. An STTC then gets full diversity like the [Alamouti code](/alamouti-code/) and the other [orthogonal space-time block codes](/orthogonal-space-time-block-codes/), and it also gets a coding gain that grows with the number of states, as [trellis-coded modulation](/trellis-coded-modulation/) does on one antenna. The price is a [Viterbi decoder](/viterbi-algorithm/) whose cost grows with the number of states, where an OSTBC needs only a linear combiner.

## Definition

Let $\mathcal{A}$ be a constellation of $2^b$ points. A **space-time trellis code** for $N_t$ transmit antennas at $b$ bits per channel use is a [trellis](/trellis/) with a finite set of states, a start state, and for each state $2^b$ outgoing branches, one for each $b$-bit input. Each branch has a next state and a label $(q^1, \ldots, q^{N_t}) \in \mathcal{A}^{N_t}$. At time $t$ the encoder is in state $\sigma_t$, reads $b$ bits, follows the branch, and antenna $i$ sends $q_t^i$.

A frame of $T$ inputs, usually followed by inputs that drive the encoder back to the start state, gives an $N_t \times T$ codeword matrix $X$ whose column $t$ is the branch label at time $t$. The receiver, which knows $H$, sees $Y = H X + W$ and runs the Viterbi algorithm on the trellis with branch metric

$$\sum_{j=1}^{N_r} \left| y_t^j - \sum_{i=1}^{N_t} h_{ji}\, q_t^i \right|^2,$$

which finds the maximum likelihood path when the noise is white and Gaussian.

**Diversity and coding gain.** Two paths that leave a common state and meet again later form an **error event**, and their codeword difference $\Delta$ is nonzero only over that event. The diversity of the code in quasi-static Rayleigh fading is $N_r$ times the smallest rank of $\Delta$ over all error events, and the coding gain is the smallest $(\det \Delta \Delta^H)^{1/N_t}$ among the full-rank ones, by the rank and determinant criteria.

**State bound (a theorem of Tarokh, Seshadri and Calderbank).** An STTC with diversity $r N_r$ at a rate of $b$ bits per channel use has at least $2^{b(r - 1)}$ states. So full diversity on two antennas at 2 bits per use needs at least 4 states.

## Examples and non-examples

**The 4-state QPSK code.** Use QPSK points $j^k$ with indices $k = 0, 1, 2, 3$, unit energy. The state is the last input. From state $s$ with input $i$, antenna 1 sends point $s$, antenna 2 sends point $i$, and the next state is $i$. The inputs $1, 3, 2$ from state 0, closed by the input 0, give

| time | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| antenna 1 | 0 | 1 | 3 | 2 |
| antenna 2 | 1 | 3 | 2 | 0 |

so antenna 1 sends the stream of antenna 2 one slot later. This is the 4-state 4-PSK code of Tarokh, Seshadri and Calderbank, and they note that it is a delay diversity code.

**Its rank and determinant (a theorem, with a short proof).** For an error event with symbol differences $e_1, \ldots, e_k$, the rows of $\Delta$ are $a = (0, e_1, \ldots, e_k)$ and $b = (e_1, \ldots, e_k, 0)$. With $S = \sum |e_t|^2$, $\det \Delta \Delta^H = S^2 - |\langle a, b \rangle|^2$. For $k = 1$ this is $|e_1|^4$. For $k \ge 2$, Cauchy-Schwarz on the overlapping parts gives $|\langle a, b \rangle|^2 \le (S - |e_1|^2)(S - |e_k|^2)$, so the determinant is at least $|e_1|^4 + |e_1|^2 |e_k|^2 + |e_k|^4$. Every nonzero QPSK difference has $|e|^2 \ge 2$, so every $\Delta$ has full rank 2, and the minimum determinant is $2^2 = 4$, reached by a single symbol error. A brute force over all error events of length up to 4 gives the same minimum, 4.

**Larger codes.** Tarokh, Seshadri and Calderbank gave QPSK and 8-PSK codes for two antennas with up to 32 states. All have full diversity, and the coding gain grows with the number of states. Later searches, some with the trace criterion for many receive antennas, found codes with larger gains.

**Non-example: the same symbol on both antennas.** The 4-state trellis with label $(i, i)$ on each branch has $\Delta$ with two equal rows, of rank one. The diversity is only $N_r$, whatever the trellis.

**Non-example: one TCM stream per antenna.** Two independent [trellis-coded modulation](/trellis-coded-modulation/) streams, one on each antenna, form one trellis with product labels. An error event in one stream alone leaves the other row of $\Delta$ zero, so the rank is one, and the diversity is $N_r$. This is spatial multiplexing with coding, not an STTC with full diversity.

**Non-example: OSTBCs.** The Alamouti code has full diversity and a block structure but no trellis memory between blocks, so it has no coding gain beyond the minimum distance of the constellation.

## Related definitions

- **Delay diversity.** Antenna $i$ sends the same coded stream delayed by $i - 1$ slots. It turns a transmit array into a frequency-selective channel for a single-antenna code. Wittneben and, separately, Seshadri and Winters proposed it in the early 1990s. With a suitable outer code it has full diversity; the 4-state code above is the simplest case.
- **Fast fading criteria.** When $H$ changes in every slot, Tarokh, Seshadri and Calderbank replace rank by the number of nonzero columns of $\Delta$ (the symbol-wise Hamming distance) and the determinant by the product of the squared column norms along the event.
- **Super-orthogonal space-time trellis codes.** Jafarkhani and Seshadri label the branches with whole Alamouti blocks, with different rotations on different branches, so that the code keeps the full diversity and the simple block structure and adds a coding gain from the trellis.
- **Decoding cost.** The Viterbi decoder does $2^b$ branch metrics per state per time, each of cost $N_t N_r$ multiply-adds, so the cost per time is of order $|\text{states}| \cdot 2^b N_t N_r$. By the state bound, this grows as $2^{b r}$ for diversity $r N_r$.
- **Diversity-multiplexing tradeoff.** An STTC sends at most one symbol per channel use, so its multiplexing gain is at most 1. Full-rate codes such as the [golden code](/golden-code/) send $\min(N_t, N_r)$ symbols per use; see the [diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/).

## References
