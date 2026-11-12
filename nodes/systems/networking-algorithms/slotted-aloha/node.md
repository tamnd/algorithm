---
tag: S3TWTY
kind: algorithm
slug: slotted-aloha
name: Slotted ALOHA
aliases:
- ALOHA
- slotted ALOHA protocol
area: systems/networking-algorithms
level: intro
summary: "Stations send only at slot starts, each with some probability. A slot carries a frame only when exactly one station sends, so the throughput is at most 1/e."
solves: [medium-access-control]
model: synchronous-model
complexity:
  vars: {n: the number of stations, p: the send probability}
  time: {worst: O(1), expected: O(1)}
  space: {extra: O(1)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1972
  people: [Norman Abramson, Lawrence G. Roberts]
  note: Abramson described ALOHA, the unslotted random access scheme of the ALOHA radio network at the University of Hawaii, in 1970. Roberts added slots in an ARPA note of 1972, reprinted in 1975.
prereqs: [medium-access-control, bernoulli-trials, poisson-distribution]
see_also: [csma-cd, csma-ca, binary-exponential-backoff, exponential-backoff, geometric-distribution, balls-into-bins]
sources:
  - paper: doi:10.1145/1478462.1478502
    title: "Norman Abramson, THE ALOHA SYSTEM: another alternative for computer communications, AFIPS Fall Joint Computer Conference, 1970"
    locator: pages 281 to 285 (the random access radio channel and the throughput G e^(-2G) of unslotted ALOHA)
  - paper: doi:10.1145/1024916.1024920
    title: "Lawrence G. Roberts, ALOHA packet system with and without slots and capture, ACM SIGCOMM Computer Communication Review 5(2), 1975"
    locator: pages 28 to 42 (slots, the throughput G e^(-G), and capture); first circulated as ARPA Satellite System Note 8, 1972
  - paper: doi:10.1109/TIT.1987.1057315
    title: "Ronald L. Rivest, Network control by Bayesian broadcast, IEEE Transactions on Information Theory 33(3), 1987"
    locator: pages 323 to 328 (the pseudo-Bayesian control of slotted ALOHA with ternary feedback)
  - book: isbn:9780132009164
    title: Dimitri Bertsekas and Robert Gallager, Data Networks, second edition, Prentice Hall, 1992
    locator: Chapter 4, Section 4.2 (slotted multiaccess, the instability of slotted ALOHA and its stabilization)
  - book: isbn:9780135928615
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 6, Section 6.3 (random access protocols, the efficiency of slotted ALOHA and ALOHA)
---

Slotted ALOHA is a random access protocol for [medium access control](/medium-access-control/). Time on the shared channel is cut into slots of one frame time, a station may start a frame only at the start of a slot, and a station whose frame collides sends it again in a later slot with some probability. With $n$ stations that each send with probability $p$, a slot carries a frame with probability $n p (1-p)^{n-1}$, which is largest at $p = 1/n$ and tends to $1/e \approx 0.368$ as $n$ grows. That is twice the best throughput of unslotted ALOHA, $1/(2e) \approx 0.184$.

## In plain words

Many radios share one channel. Nobody is in charge, and a radio cannot hear the others before it talks. If two radios talk at the same time, both messages are lost. In plain ALOHA a radio talks whenever it has a message, and it tries again after a random wait if the message is lost. Slotted ALOHA adds a clock that all radios share. Time is cut into slots, each the length of one message, and a radio may only start at the start of a slot. Now two messages are lost only if they start in the same slot, not if they merely overlap a little. Each waiting radio flips a biased coin in each slot to decide whether to try. When the coin is set well for the number of radios, a bit more than one slot in three carries a message.

## The problem

There are $n$ stations on one broadcast channel, for example a radio frequency or a satellite link. All frames have the same length, and the clock is shared, so the stations agree on slot boundaries. A station cannot sense the channel before it sends. At the end of each slot every station learns the outcome of that slot: *idle* (no frame), *success* (one frame) or *collision* (two or more frames, all lost). The task is to deliver the frames with a high *throughput*, the long-run fraction of slots that carry a success, and with no central control. This is the random access form of [medium access control](/medium-access-control/).

## The algorithm

Each station runs the same rule at the start of every slot. A frame is *backlogged* after it has collided at least once.

```pseudo id=main
SLOTTED-ALOHA(station, q)                     ▷ run at the start of each slot
L1  if the station has no frame then return
L2  F ← the frame at the head of the queue
L3  if F is new then send F in this slot
L4  else send F in this slot with probability q   ▷ F is backlogged
L5  at the end of the slot read the feedback
L6  if F was sent and the feedback is success then remove F from the queue
L7  else if F was sent then mark F backlogged     ▷ collision: F is kept
```

The feedback of line L5 comes from the channel itself: a station that listens to its own downlink, or an acknowledgement from the base station in the same slot, tells it whether its frame got through. Line L4 is the repeat rule, and it is the only parameter. In the analysis of a *saturated* channel, where every station always has a frame, every frame is treated as backlogged and each station sends with the same probability $p$ in each slot.

## Example

Three stations $A$, $B$ and $C$ always have a frame and send with $p = 1/3$. A run of ten slots with a fixed random seed gives:

| slot | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| senders | A B | A B | none | A C | A B C | none | B C | none | B | C |
| outcome | collision | collision | idle | collision | collision | idle | collision | idle | success | success |

Two of the ten slots succeed. The long-run success rate for $n = 3$ is $3 \cdot \frac13 \cdot (\frac23)^2 = 4/9 \approx 0.444$; ten slots are far too few to show it.

The best success rate $b_n = (1 - 1/n)^{n-1}$, reached at $p = 1/n$, in exact fractions:

| $n$ | 1 | 2 | 3 | 4 | 5 | 10 | 20 | 50 |
|---|---|---|---|---|---|---|---|---|
| $b_n$ | 1 | 1/2 | 4/9 | 27/64 | 256/625 | 0.38742 | 0.37735 | 0.37160 |

A simulation of $10^5$ slots with $n = 10$ and $p = 0.1$ (seed 1) gave a success rate of $0.39059$, against the exact $0.9^9 = 0.38742$. Idle slots were $0.34773$ of the total (exact $0.9^{10} \approx 0.34868$) and collisions $0.26168$ (exact $0.26390$). Each of the ten stations got between $3828$ and $4000$ of the successes.

**Instability.** In the infinite-population model with Poisson arrivals of $\lambda = 0.3$ new frames per slot, a start with $50$ backlogged frames and the fixed repeat probability $q = 0.1$ gave a backlog of $326$ after $1000$ slots and $1526$ after $5000$ slots (seed 7). The pseudo-Bayesian rule of the variants below, on the same arrivals model and seed, had a backlog of $4$ after $1000$ slots, never more than $59$, and delivered $0.305$ frames per slot over $20000$ slots, close to the arrival rate plus the initial backlog spread over the run.

## Correctness

Two frames overlap if and only if they start in the same slot, so a success slot delivers one intact frame, and line L7 keeps every frame that collided; no frame is lost for good. If $n$ stations send independently with probability $p$, station $i$ is the only sender with probability $p(1-p)^{n-1}$, and the $n$ such events are disjoint, so

$$S_n(p) = n p (1-p)^{n-1}, \qquad S_n'(p) = n (1-p)^{n-2} (1 - n p).$$

The derivative changes sign only at $p = 1/n$, so that is the best common probability, with $S_n(1/n) = (1 - 1/n)^{n-1}$. This value falls strictly toward $1/e$, because $(1 + 1/m)^m$ rises strictly to $e$. In the Poisson model of Abramson and Roberts, where the number of frames sent per slot is Poisson with mean $G$, the throughput is $S = G e^{-G}$, with its maximum $1/e$ at $G = 1$. Without slots a frame collides with any frame that starts within one frame time before or after it, a window of length two, so $S = G e^{-2G}$ with its maximum $1/(2e)$ at $G = 1/2$. The full proofs, and the drift argument for the instability, are in the proof file below.

## Complexity

- **Work per slot.** Each station does $O(1)$ work per slot: one random draw and one read of the feedback. It stores $O(1)$ state besides its queue: the backlogged flag, or the backlog estimate of the pseudo-Bayesian rule.
- **Throughput.** At most $b_n = (1 - 1/n)^{n-1}$ frames per slot with a common fixed probability, which is above $1/e$ and tends to it. In the Poisson model, at most $1/e$.
- **Delay.** With $n$ saturated stations and $p = 1/n$, a given station succeeds in a slot with probability $\frac1n b_n$, so its wait is geometric with mean $n / b_n$ slots, which is less than $e n$.
- **Feedback.** One of three symbols per slot. The protocol needs the slot clock and this feedback, and nothing else.

## Properties

- **Decentralized.** Each station decides alone. There is no token, no poll and no list of members.
- **Symmetric and fair in the long run.** Stations with the same $p$ get the same share. In the run above, the shares of ten stations differed by less than five percent.
- **Wasteful at best by a factor $e$.** About $37$ percent of the slots are idle and $26$ percent collide at $p = 1/n$ for large $n$.
- **Needs the number of stations.** The best $p$ is $1/n$. A wrong $p$ costs throughput on both sides: too large wastes slots on collisions, too small wastes them idle.
- **Unstable with a fixed repeat probability.** With many stations, a burst of collisions raises the backlog, more backlogged frames send, and more slots collide. The expected change of the backlog per slot becomes positive and stays positive.

## Variants and improvements

- **Pure ALOHA.** No slots: a station sends at once and repeats after a random delay. The throughput is $G e^{-2G}$, at most $1/(2e)$. It needs no shared clock.
- **Pseudo-Bayesian stabilization.** Rivest (1987) keeps an estimate $\hat{b}$ of the backlog at every station and sends each waiting frame with probability $\min(1, 1/\hat{b})$. In the form of Bertsekas and Gallager, $\hat{b}$ becomes $\max(\lambda, \hat{b} + \lambda - 1)$ after an idle slot or a success and $\hat{b} + \lambda + (e - 2)^{-1}$ after a collision, where $\lambda$ is the arrival rate. The success rate stays near $1/e$ at every backlog, and the backlog stays bounded in the run above. Rivest reports simulations and discusses stability for $\lambda < 1/e$.
- **Backoff.** A station that does not know $n$ can halve its send probability after each collision, as in [binary exponential backoff](/binary-exponential-backoff/); see also [exponential backoff](/exponential-backoff/).
- **Splitting (tree) algorithms.** After a collision, only a subset of the colliding stations tries again, and the subsets are split until each frame gets through. They reach stable throughputs near $0.487$ (Bertsekas and Gallager, Section 4.3).
- **Capture.** A receiver may decode the strongest of several frames. Roberts analyzes this case; capture raises the throughput above $1/e$.
- **Carrier sense.** Stations that can hear the channel do much better: see [CSMA/CD](/csma-cd/) and [CSMA/CA](/csma-ca/).

## When to use it

Use slotted ALOHA when the stations cannot hear each other before they send, the round trip is long compared with a frame, or the traffic is light and bursty, so that a reservation would cost more than the collisions. Satellite links, the random access channels of cellular networks and the framed slotted ALOHA of RFID tag reading are of this kind. If the stations can sense the channel and the propagation delay is short, carrier sense wins. If the load is high and steady, a controlled access scheme such as polling or time division wastes no slots.

## Pitfalls

- **Treating $G$ as the arrival rate.** $G$ counts every frame sent, repeats included. The throughput $S$ equals the arrival rate only when the system is stable.
- **A fixed repeat probability.** Line L4 with a constant $q$ is unstable with many stations. Adapt $q$ to the backlog, as the pseudo-Bayesian rule does, or the backlog can grow without bound.
- **Sending new frames at once under heavy load.** Line L3 sends a new frame in its first slot. Under load this adds collisions; the pseudo-Bayesian form treats new frames as backlogged.
- **Using the formula of the wrong variant.** $G e^{-G}$ is for slots, $G e^{-2G}$ for no slots. The factor 2 is the length of the vulnerable period.
- **Forgetting the guard time.** Real slots are a little longer than a frame, to absorb clock drift and propagation delay. The throughput in frames per second is lower than $1/e$ times the channel rate.

## Implementations

## History

Norman Abramson and his group at the University of Hawaii built the ALOHA radio network, and his 1970 paper describes its random access channel and computes the throughput $G e^{-2G}$. Lawrence Roberts proposed slots in an ARPA satellite note of 1972, published in 1975, and showed that they double the best throughput to $1/e$; the same paper treats capture. The instability of slotted ALOHA with a fixed repeat probability was studied in the 1970s, and Ronald Rivest proposed pseudo-Bayesian control in 1987. ALOHA inspired the Ethernet protocol, [CSMA/CD](/csma-cd/), at Xerox PARC.

## References
