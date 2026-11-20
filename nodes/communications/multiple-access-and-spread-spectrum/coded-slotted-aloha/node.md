---
tag: KAWTQF
kind: algorithm
slug: coded-slotted-aloha
name: Coded slotted ALOHA
aliases:
- irregular repetition slotted ALOHA
- IRSA
area: communications/multiple-access-and-spread-spectrum
level: research
summary: Users send several copies of a packet in random slots, and the receiver removes collisions by iterative interference cancellation.
solves: [medium-access-control]
model: word-ram
complexity:
  vars: {K: the number of active users, M: the number of slots in a frame, E: the number of copies sent}
  time: {worst: Θ(K + M + E), average: Θ(K + M + E), best: Θ(K + M + E)}
  space: {extra: Θ(M + E)}
properties: {deterministic: false, order_independent: true, linear_time: true, frame_synchronous: true}
history:
  year: 2007
  people: [Enrico Casini, Riccardo De Gaudenzi, Oscar del Rio Herrero]
  note: "Casini, De Gaudenzi and del Rio Herrero proposed contention resolution diversity slotted ALOHA in 2007, with two copies per packet. Liva made the number of copies random in 2011 and analysed the scheme as a code on a graph."
prereqs: [slotted-aloha, bipartite-graph]
see_also: [unsourced-random-access, successive-interference-cancellation, ldpc-code, binary-erasure-channel, tanner-graph, balls-into-bins, repetition-code, degree-distribution]
sources:
  - paper: "Enrico Casini, Riccardo De Gaudenzi and Oscar del Rio Herrero, Contention resolution diversity slotted ALOHA (CRDSA): an enhanced random access scheme for satellite access packet networks, IEEE Transactions on Wireless Communications 6(4), 2007"
    locator: pp. 1408 to 1419 (two copies of each packet per frame, pointers to the twin copy and iterative cancellation of the copies of decoded packets)
  - paper: "Gianluigi Liva, Graph-based analysis and optimization of contention resolution diversity slotted ALOHA, IEEE Transactions on Communications 59(2), 2011"
    locator: pp. 477 to 487 (irregular numbers of copies, the bipartite graph of users and slots, the analysis by density evolution and optimized distributions such as 0.5x^2 + 0.28x^3 + 0.22x^8 with threshold 0.938)
  - paper: doi:10.1109/TIT.2015.2492579
    title: Enrico Paolini, Gianluigi Liva and Marco Chiani, Coded slotted ALOHA, a graph-based method for uncoordinated multiple access, IEEE Transactions on Information Theory 61(12), 2015
    locator: pp. 6815 to 6832 (density evolution in Corollary 3.1, the upper bound on the load for a given rate in Theorem 4.1 and the distributions of Table I)
  - paper: doi:10.1109/ISTC.2012.6325214
    title: Krishna R. Narayanan and Henry D. Pfister, Iterative collision resolution for slotted ALOHA, an optimal uncoordinated transmission policy, 7th International Symposium on Turbo Codes and Iterative Information Processing, Gothenburg, 2012
    locator: pp. 136 to 139 (the soliton distribution of the number of copies and the proof that the throughput tends to 1 packet per slot)
---

Coded slotted ALOHA is a random access scheme for many users who send short packets without coordination. Time is cut into frames of $M$ slots. Each of the $K$ active users sends $d$ copies of its packet in $d$ slots chosen at random, where $d$ is drawn from a degree distribution $\Lambda$. Each copy carries pointers to the slots of the other copies. The receiver decodes every slot that holds a single copy, then subtracts the other copies of the packets it has decoded. This can leave new slots with a single copy, and the process repeats. In plain [slotted ALOHA](/slotted-aloha/), a slot with two packets is lost, and the throughput is at most $1/e \approx 0.368$ packets per slot. With well chosen distributions, coded slotted ALOHA resolves almost all packets at loads up to about $0.9$ packets per slot in long frames. The decoder is the peeling decoder of an [LDPC code](/ldpc-code/) on the [binary erasure channel](/binary-erasure-channel/), and its analysis is the same. This page is about a scheme on the collision channel. [Unsourced random access](/unsourced-random-access/) is a problem on the Gaussian channel, in which all users share one codebook and the receiver must output only the list of messages; coded slotted ALOHA is one building block of schemes for it.

## In plain words

Each user shouts its message several times at random moments in a frame. Often two users shout at the same moment, and both are lost at that moment. But if one copy of a message gets through clearly at some other moment, the listener now knows that message and where its other copies were. The listener removes those copies from the moments where they collided. A collision of two then becomes a clean single message, and the chain goes on. Extra copies cost energy, but they turn most collisions into packets that can be recovered.

## The problem

A frame has $M$ slots and $K$ active users, each with one packet. The load is $G = K/M$ packets per slot. Users do not coordinate, and the receiver does not know in advance which users are active. The model is the collision channel with perfect cancellation:

- A slot with one copy is decoded correctly, and a check code tells the receiver that it succeeded.
- A slot with two or more copies gives nothing by itself.
- When a packet is known, the receiver can rebuild each of its copies and subtract them exactly. The pointers in the packet header tell it where the copies are.

The goal is to resolve as many packets as possible. The measures are the packet loss rate $P_L$, the fraction of the $K$ packets that are not resolved, and the throughput $T = G(1 - P_L)$ in packets per slot. This is a form of the [medium access control](/medium-access-control/) problem for many short, uncoordinated transmissions, such as satellite return links and machine-type traffic.

## The algorithm

The users are $0, \ldots, K - 1$ and the slots are $0, \ldots, M - 1$. $N(u)$ is the set of slots of user $u$, and $C[s]$ is the set of users whose copies in slot $s$ are not yet cancelled.

```pseudo id=main
CODED-SLOTTED-ALOHA(K, M, Λ)
    ▷ transmitter of each user u
L1  d ← a degree drawn with Pr(d) = Λ_d
L2  N(u) ← d distinct slots drawn uniformly from 0, …, M - 1; send one copy in each
    ▷ receiver, at the end of the frame
L3  for each user u and each slot s ∈ N(u) do add u to C[s]
L4  Q ← a queue of the slots s with |C[s]| = 1
L5  while Q is not empty do
L6      s ← take a slot from Q
L7      if |C[s]| ≠ 1 then continue
L8      u ← the only user in C[s]; decode its packet from slot s
L9      append u to the resolved list D
L10     for each slot t ∈ N(u) do
L11         remove u from C[t] and subtract its copy from slot t
L12         if |C[t]| = 1 then
L13             add t to Q
L14 return D
```

A real receiver does not know $C[s]$. It tries to decode each slot and keeps the result only if the check code passes, which in the model happens exactly when $|C[s]| = 1$. Line L8 then reads the pointers from the header, which gives $N(u)$ for line L10. The implementation works on the graph directly: it is given $N(u)$ for each user and returns the order in which the users are resolved.

The users and slots form a [bipartite graph](/bipartite-graph/), with an edge for each copy. It is the [Tanner graph](/tanner-graph/) of a code: each user is a variable node of degree $d$, a [repetition code](/repetition-code/), and each slot is a check node. Lines L5 to L13 are the peeling decoder of that code on the erasure channel.

## Example

Take $M = 6$ slots and $K = 6$ users, so $G = 1$, with these slots:

| user | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $N(u)$ | 0, 1 | 1, 2 | 2, 3 | 3 | 4, 5 | 4, 5 |

So $C[0] = \{0\}$, $C[1] = \{0, 1\}$, $C[2] = \{1, 2\}$, $C[3] = \{2, 3\}$, $C[4] = C[5] = \{4, 5\}$. Line L4 puts slot 0 in the queue, the only clean slot.

| step | slot taken | user resolved | slots cleaned (line L13) |
|---|---|---|---|
| 1 | 0 | 0 | 1 |
| 2 | 1 | 1 | 2 |
| 3 | 2 | 2 | 3 |
| 4 | 3 | 3 | none |

The decoder returns $D = [0, 1, 2, 3]$. Users 4 and 5 used the same two slots, so each of those slots holds two unknown copies, and nothing can separate them. Here $P_L = 2/6$ and $T = 4/6$. Without cancellation, only slot 0 is clean, and the throughput is $1/6$.

## Correctness

A **stopping set** is a set $S$ of users such that every slot of a user in $S$ holds at least two users of $S$. In the example, $\{4, 5\}$ is a stopping set. The union of two stopping sets is a stopping set, so a largest one, $S^*$, exists.

Theorem: the decoder stops with exactly the users of $S^*$ unresolved, whatever order line L6 uses. When it stops, no slot is left with a single uncancelled copy, so the unresolved users form a stopping set. Conversely, the first user of any stopping set to be resolved would need a slot with no other member of the set, which a stopping set does not have. In the collision channel, no other receiver can do better, because each slot of a user in $S^*$ has a second unknown copy. Every resolved packet is correct, since its slot holds only its own copy once the known copies are subtracted. The proof, with the queue invariant, is in the proof file below.

## Complexity

**Time.** Line L3 makes $E = \sum_u |N(u)|$ insertions. A slot enters the queue at most once, because its set only shrinks and reaches size 1 only once, so the loop runs at most $M$ times. Lines L10 to L13 run once for each copy of a resolved user, at most $E$ times in total. So the decoder costs $\Theta(K + M + E)$ word operations. With mean degree $\bar d = \sum_d d \Lambda_d$, $E$ is about $\bar d K$. Each operation on $C[s]$ is $O(1)$ with a counter and the sum of the identifiers of the users still in the slot: when the counter is 1, the sum is the remaining user.

**Space.** $\Theta(M + E)$ for the slot sets and the lists $N(u)$. A real receiver also stores the $M$ received slot signals for the frame.

## Properties

- **Density evolution threshold (theorem).** Let $K$ and $M$ grow with $G = K/M$ fixed. Let $p$ be the probability that a copy is still unresolved after an iteration. Paolini, Liva and Chiani (Corollary 3.1) give the recursion $p \leftarrow 1 - \exp(-G \sum_d d \Lambda_d p^{d-1})$, from $p = 1$. The threshold $G^*$ is the largest load at which $p$ goes to 0. Below $G^*$, almost all packets are resolved in long frames. The implementation finds $G^*$ by bisection, with these results:

| distribution $\Lambda(x)$ | mean degree | $G^*$ (computed) | load bound |
|---|---|---|---|
| $x^2$ (two copies, as in CRDSA) | 2 | 0.5 (exact) | 0.7968 |
| $x^3$ | 3 | 0.8185 | 0.9405 |
| $x^4$ | 4 | 0.7723 | 0.9802 |
| $x^5$ | 5 | 0.7018 | 0.9930 |
| $0.5x^2 + 0.28x^3 + 0.22x^8$ (Liva 2011) | 3.6 | 0.9386 | 0.9695 |
| $0.554016x^2 + 0.261312x^3 + 0.184672x^6$ (Paolini et al., Table I) | 3 | 0.8792 | 0.9405 |

  The values agree with the published thresholds 0.5, 0.938 and 0.8792 within $10^{-3}$ (checked in the tests). For $x^2$ the recursion is $p \leftarrow 1 - e^{-2Gp}$. Since $1 - e^{-z} < z$ for $z > 0$, $p$ falls to 0 when $2G \le 1$, and a fixed point $p > 0$ exists when $2G > 1$, so $G^* = 1/2$ exactly. Near $G = 1/2$ the recursion converges very slowly, so the bisection with 20000 iterations stops at 0.4996.

- **Load bound (theorem).** With rate $R = 1/\bar d$, one packet for $\bar d$ copies, every distribution has $G^* \le G_R$, the positive root of $G = 1 - e^{-G/R}$ (Paolini et al., Theorem 4.1). For $R = 1/3$ this gives 0.9405. To reach loads near 1, the mean degree must grow.
- **Stability (closed form).** Near $p = 0$, the recursion multiplies $p$ by $2 \Lambda_2 G$. So $G^* \le 1/(2\Lambda_2)$. Users of degree 2 help the decoder start, but too many of them stop it before the end. For the distribution of Liva, this bound is 1.
- **Throughput tends to 1 (theorem).** Narayanan and Pfister showed that the soliton distribution, $\Lambda_d = 1/(d(d-1))$ for $d \ge 2$ with a truncation, gives $G^*$ as close to 1 as wanted, at the cost of a mean degree that grows like the logarithm of the largest degree.
- **Error floor in finite frames (measurement and heuristic).** For Liva's distribution with $M = 200$ and 2000 frames at each load (one generator with seed 7, the loads in turn), $P_L$ was 0.0010 at $G = 0.3$, 0.0020 at $G = 0.4$ and 0.0025 at $G = 0.5$. The floor comes from small stopping sets. The smallest is two users of degree 2 on the same two slots, with probability about $\Lambda_2 \cdot (K - 1)\Lambda_2 / \binom{M}{2}$ for a given user, which is $0.0012$ at $G = 0.5$. This is about half of the measured floor; larger stopping sets give the rest.
- **Finite frames lose part of the threshold (measurement).** With $M = 200$, $K = GM$ and 100 frames for each point (a new generator with seed 1 for each distribution, the loads in turn), $P_L$ was:

| distribution | $G = 0.4$ | $G = 0.5$ | $G = 0.6$ | $G = 0.7$ | $G = 0.8$ |
|---|---|---|---|---|---|
| $x^2$ | 0.016 | 0.030 | 0.109 | 0.263 | 0.40 |
| Liva 2011 | 0.0011 | 0.0022 | 0.0025 | 0.0076 | 0.042 |
| Paolini et al., $R = 1/3$ | 0.0005 | 0.0022 | 0.0053 | 0.0215 | 0.085 |

  At $G = 0.8$, Liva's distribution gives $T = 0.766$ packets per slot, about twice the peak of slotted ALOHA. A new generator with seed 1 and one copy per user ($\Lambda = x$) at $G = 0.4$ gave $P_L = 0.3291$, against the closed form $1 - (1 - 1/M)^{K-1} = 0.3270$.
- **Energy cost (closed form).** A user sends $\bar d$ copies, so it uses $\bar d$ times the energy of slotted ALOHA for each packet: 3.6 times, or 5.6 dB, for Liva's distribution.

## Variants and improvements

- **CRDSA.** The first scheme, by Casini, De Gaudenzi and del Rio Herrero, sends exactly two copies, $\Lambda = x^2$. Its threshold is 0.5.
- **A random number of copies.** Liva drew $d$ from an optimized distribution, which is the scheme on this page. It is the special case of the general scheme below in which every local code is a repetition code.
- **Coded slotted ALOHA with local codes.** Paolini, Liva and Chiani split each packet into $k$ segments and encode them with a short $(n, k)$ code instead of repetition. A slot node then resolves a segment, and a user node resolves the packet when any $k$ of its $n$ segments are known. This gives better thresholds at a given rate.
- **Frameless ALOHA.** Users send in each slot with a small probability, and the receiver ends the frame when enough packets are resolved, as in a rateless code.
- **Capture and multipacket reception.** If the receiver can decode the strongest of two colliding copies, or two copies at once with [successive interference cancellation](/successive-interference-cancellation/), more slots start the peeling, and loads above 1 become possible.
- **Unsourced random access.** When every user sends from the same codebook and the receiver needs only the list of messages, coded slotted ALOHA becomes one building block. Each slot then carries a short multiuser code. See [unsourced random access](/unsourced-random-access/).

## When to use it

Use coded slotted ALOHA when many devices send short, rare packets and a handshake for each packet would cost more than the data: satellite return links (it is in the DVB-RCS2 standard, as CRDSA), sensor networks and machine-type traffic. The receiver must store a whole frame and cancel signals well, and the users must agree on the frame boundaries. When the traffic is steady, scheduled access such as [TDMA](/time-division-multiple-access/) or [OFDMA](/orthogonal-frequency-division-multiple-access/) wastes less energy. When devices are few and can listen before they send, [CSMA/CA](/csma-ca/) is simpler.

## Pitfalls

- **Reading the threshold as a frame result.** $G^*$ holds only as $M$ grows. With $M = 200$, Liva's distribution loses about 4 percent of the packets at $G = 0.8$, below its threshold of 0.94.
- **Ignoring the error floor.** A $P_L$ near $10^{-3}$ at low load comes from small stopping sets, not from the load, and more iterations do not remove it. Avoid many users of degree 2, or add an outer code.
- **Assuming perfect cancellation.** Each copy passes through its own channel. The receiver must estimate the gain and phase of each copy before it subtracts it, or residual interference builds up over the iterations.
- **Sending two copies in the same slot.** Line L2 draws distinct slots. Two copies in one slot cannot help, and a user can then form a stopping set alone.
- **Forgetting the energy cost.** For the same energy per packet, each copy of a user with $\bar d$ copies has $\bar d$ times less energy. Compare schemes at equal energy, not at equal power per slot.

## Implementations

## History

Abramson's ALOHA system of 1970 and the slotted version of Roberts in 1972 lost every collided packet. In 2007, Casini, De Gaudenzi and del Rio Herrero proposed contention resolution diversity slotted ALOHA (CRDSA) for satellite networks. Each packet was sent twice, with pointers to its twin, and the receiver cancelled the copies of decoded packets iteratively. In 2011, Liva saw that the process is the erasure decoding of a code on a graph. He let the number of copies vary, optimized its distribution with density evolution, and obtained thresholds above 0.9. In 2012, Narayanan and Pfister showed that the soliton distribution brings the throughput arbitrarily close to 1. In 2015, Paolini, Liva and Chiani replaced repetition with general local codes and gave an upper bound on the load for each rate. Later work used the scheme as an outer code for unsourced random access, and studied frameless versions, capture and fading channels.

## References
