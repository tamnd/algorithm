---
tag: YMKAJR
kind: algorithm
slug: chang-roberts
name: Chang-Roberts algorithm
aliases:
- LCR algorithm
- Le Lann-Chang-Roberts algorithm
area: distributed/leader-election
level: intro
summary: Ring election in which each process sends its id one way round and processes forward only ids larger than their own. Worst case n(n+1)/2 messages, average n H_n.
solves: [ring-leader-election]
model: asynchronous-model
complexity:
  vars: {n: the number of processes}
  time: {worst: Θ(n)}
  messages: {worst: Θ(n^2), average: Θ(n log n), best: Θ(n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1979
  people: [Ernest Chang, Rosemary Roberts]
  note: Improves the 1977 ring algorithm of Gerard Le Lann, in which each identifier goes all the way round.
prereqs: [ring-network, ring-leader-election, asynchronous-model, message-complexity]
see_also: [hirschberg-sinclair, peterson-leader-election, franklin, ring-election-lower-bound, explicit-leader-election, harmonic-series, find-maximum, hire-assistant]
sources:
  - paper: doi:10.1145/359104.359108
    title: Ernest Chang and Rosemary Roberts, An improved algorithm for decentralized extrema-finding in circular configurations of processes, Communications of the ACM 22(5), 1979
    locator: pages 281 to 283 (the algorithm, the n(n+1)/2 worst case and the average number of messages)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 3, Section 3.3 (the LCR algorithm in the synchronous ring) and Chapter 15, Section 15.1.1 (LCR in the asynchronous ring)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 3, Section 3.3.1 (an O(n^2) algorithm for asynchronous rings)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 7, Section 7.2 (the algorithms of Le Lann and of Chang and Roberts, and the average case)
  - paper: doi:10.1145/1634.1889
    title: Jan Pachl, Ephraim Korach and Doron Rotem, Lower bounds for distributed maximum-finding algorithms, Journal of the ACM 31(4), 1984
    locator: pages 905 to 918 (the average lower bound n H_n for unidirectional rings)
---

The Chang-Roberts algorithm elects a leader on a unidirectional [ring network](/ring-network/) of processes with distinct identifiers. Each process sends its identifier round the ring, and each process forwards only identifiers that are larger than its own, so only the largest identifier comes back to its owner. It sends $n(n+1)/2$ election messages in the worst case and $n H_n \approx 0.69\, n \log_2 n$ on average over random orders, where $H_n$ is the [harmonic number](/harmonic-series/). It is the first algorithm in most courses on [ring election](/ring-leader-election/).

## In plain words

Picture people sitting in a circle, each with a different number on a card. Each person can only pass notes to the person on their left. To choose a leader, each person writes their own number on a note and passes it on.

When a note arrives, the person compares it with their own card. If the note is larger, they pass it on. If it is smaller, they throw it away, because that number cannot win. If the note shows their own number, it has gone all the way round without meeting anyone larger, so they are the leader. They then send a second note round the circle that tells everybody who won.

Small numbers die early and big numbers travel far. The worst order is when the numbers get smaller in the direction the notes move, because then each note travels as far as possible.

## The problem

The network is a ring of $n \ge 1$ processes $p_0, \ldots, p_{n-1}$ in the [asynchronous model](/asynchronous-model/). Process $p_i$ can send only to $p_{i+1}$ (indices modulo $n$). Process $p_i$ has an identifier $u_i$, the identifiers are distinct and come from a totally ordered set, and the processes do not know $n$. All processes start. Each message is delivered after a finite delay. Channels need not be FIFO.

The goal is the explicit form of [leader election](/ring-leader-election/): exactly one process ends with status *leader*, every other process ends with status *non-leader*, and every process learns the identifier of the leader. Here the leader is the process with the largest identifier.

## The algorithm

The code of the process with identifier $u$ is below. It reacts to each message that arrives.

```pseudo id=main
CHANG-ROBERTS(u)                         ▷ the code of the process with identifier u
L1  send ⟨elect, u⟩ to the next process
L2  status ← unknown
L3  on receiving ⟨elect, v⟩:
L4      if v > u then send ⟨elect, v⟩ to the next process
L5      else if v = u then
L6          status ← leader
L7          send ⟨leader, u⟩ to the next process
L8      else discard the message           ▷ v < u, so v cannot win
L9  on receiving ⟨leader, v⟩:
L10     if v ≠ u then status ← non-leader, leader ← v
L11         send ⟨leader, v⟩ to the next process
L12     else drop the message              ▷ the announcement has gone round
```

Lines L3 to L8 are the election. An identifier survives at a process only if it is larger than the identifier of that process (line L4). An identifier that returns to its owner (line L5) has beaten all the others. Lines L9 to L12 are the announcement, which tells each process the result. Without them a process with status *unknown* cannot tell whether the election is over. A process may receive an *elect* message after the announcement on a channel that is not FIFO; it applies lines L3 to L8 as usual, and its status does not change.

## Example

Take $n = 5$ with identifiers $3, 7, 1, 5, 2$ at $p_0, \ldots, p_4$, and messages moving from $p_i$ to $p_{i+1}$. The table follows the run in synchronous rounds, where each message takes one round.

| round | messages sent | what happens |
|---|---|---|
| 1 | 3, 7, 1, 5, 2 | 3 dies at $p_1$, 1 dies at $p_3$, 2 dies at $p_0$; 7 and 5 go on |
| 2 | 7, 5 | 7 passes $p_3$, 5 passes $p_0$ |
| 3 | 7, 5 | 7 passes $p_4$, 5 dies at $p_1$ |
| 4 | 7 | 7 passes $p_0$ |
| 5 | 7 | 7 arrives at $p_1$, which becomes the leader |

The identifiers travel $1, 5, 1, 3, 1$ hops, so there are $11$ elect messages. The announcement from $p_1$ then takes $5$ more messages, in rounds 6 to 10, for $16$ in total. The worst case for $n = 5$ is $15$ elect messages, the best case is $9$, and the average over all $120$ orders is $5 H_5 = 137/12 \approx 11.42$.

## Correctness

Let $p_m$ hold the largest identifier $u_{\max}$. The proof has three steps.

- **The largest identifier returns.** Each process $p_i \ne p_m$ has $u_i < u_{\max}$, so line L4 forwards $\langle \text{elect}, u_{\max} \rangle$. After $n$ hops it reaches $p_m$, which sets status *leader* in line L6.
- **No other identifier returns.** The identifier $u_i$ of $p_i \ne p_m$ meets $p_m$ before it can return to $p_i$, because $p_m$ lies on the way round. There $u_i < u_{\max}$, and line L8 discards it, if no other process has discarded it earlier. So no process other than $p_m$ ever runs line L6.
- **Everyone learns.** Only $p_m$ sends a *leader* message. It travels once round the ring, each other process sets status *non-leader* and stores $u_{\max}$ (line L10), and $p_m$ drops it when it returns (line L12).

The number of messages is finite, by the bound in the next section, so the run ends. The proof in full, with the count of messages, is in the [proof of correctness](proofs/correctness/).

## Complexity

**Elect messages, worst case.** Number the identifiers by rank. The identifier of rank $k$ from the bottom (there are $k - 1$ smaller ones) is discarded at the first larger identifier, so it travels at most $k$ hops, and the largest travels exactly $n$. The total is at most

$$\sum_{k=1}^{n} k = \frac{n(n+1)}{2}.$$

The bound is reached when the identifiers decrease in the direction in which the messages travel. Then the identifier of rank $k$ passes the $k - 1$ smaller identifiers that follow it. For $n = 5$ the order $5, 4, 3, 2, 1$ gives $5 + 4 + 3 + 2 + 1 = 15$ messages.

**Elect messages, best case.** The largest identifier always travels $n$ hops, and every other identifier at least $1$. So at least $2n - 1$ messages are sent, and the increasing order $1, 2, \ldots, n$ gives exactly $2n - 1$.

**Elect messages, average case.** Take all $n!$ assignments of the identifiers to the processes as equally likely. The expected number of elect messages is exactly

$$n H_n = n \sum_{k=1}^{n} \frac{1}{k} = n \ln n + O(n) \approx 0.693\, n \log_2 n.$$

The identifier with $r - 1$ larger identifiers travels to the first of them, and the expected position of the first of $r - 1$ random positions among the $n - 1$ others is $n/r$. Summing $n/r$ over $r = 1, \ldots, n$ gives $n H_n$. The proof page has the details.

**Total messages.** The announcement adds exactly $n$ messages. So the total is at most $n(n+1)/2 + n = n(n+3)/2$, and $n H_n + n$ on average. The count does not depend on the order in which the network delivers messages, because each decision of line L4 depends only on the identifier and the process.

**Time.** In the synchronous model the leader knows after $n$ rounds and all processes know after $2n$ rounds. In the asynchronous model, if each message takes at most one time unit, the same bounds hold in time units, because no process waits before it forwards the largest identifier. So the time is $\Theta(n)$.

**Space and message size.** A process stores its identifier, its status and the leader's identifier. Each message holds one identifier.

## Properties

- **Deterministic and comparison based.** A process only compares identifiers, so the result is the same for any identifiers in the same relative order.
- **Uniform.** The processes do not need to know $n$.
- **No FIFO needed.** The proof does not use the order of messages on a channel.
- **Not message optimal.** The worst case $\Theta(n^2)$ is far from the $\Omega(n \log n)$ [lower bound](/ring-election-lower-bound/). The average $n H_n$ is optimal for unidirectional rings: Pachl, Korach and Rotem proved that every such algorithm sends at least $n H_n$ messages on average over random orders.
- **Not fault tolerant.** One lost message or one crashed process stops the election.

## Variants and improvements

- **Le Lann's algorithm.** Each process forwards every identifier, so each goes all the way round and each process sees all of them. This costs exactly $n^2$ messages, and each process can pick the largest identifier without an announcement.
- **Only some processes start.** A process that has not started when the first *elect* message arrives starts then: it sends its own identifier if it is larger than the arriving one, and otherwise it only forwards. An identifier is discarded only at a process with a larger identifier, and that process has started and sent its own. So some message keeps moving until the process with the largest identifier receives one. That process then starts and sends its identifier, which wins.
- **Minimum in place of maximum.** Reverse each comparison to elect the smallest identifier.
- **Bidirectional rings.** Sending in both directions does not lower the worst case by itself. [Hirschberg and Sinclair](/hirschberg-sinclair/) and [Franklin](/franklin/) use the second direction to reach $O(n \log n)$ messages, and [Peterson](/peterson-leader-election/) and [Dolev, Klawe and Rodeh](/dolev-klawe-rodeh/) reach $O(n \log n)$ in one direction.

## When to use it

Use it to teach leader election, and on small rings where $n^2$ messages are cheap. It is short, needs no FIFO channels and no knowledge of $n$, and its average cost is optimal for one direction. When the identifiers can be in a bad order, for example when they increase as the ring is built, use an $O(n \log n)$ algorithm such as [Peterson's](/peterson-leader-election/). When processes can crash, use an election that tolerates crashes, such as the [bully algorithm](/bully-algorithm/) or the election of [Raft](/raft/).

## Pitfalls

- **Equal identifiers.** The algorithm needs distinct identifiers. With identifiers $2, 1, 2$ the identifier of $p_0$ reaches $p_2$, which sees its own value and becomes leader, and the same happens at $p_0$. Two processes become leader.
- **No announcement.** Without lines L9 to L12 only the leader knows the result. The other processes keep status *unknown*, and they cannot tell when the election ends.
- **Counting the worst case wrongly.** The worst case is $n(n+1)/2$ elect messages, not $n^2$. The value $n^2$ is the cost of Le Lann's algorithm, which never discards.
- **Expecting the average in practice.** The $n H_n$ bound is for a uniformly random order. Identifiers that are given out in order round the ring can give the worst case.

## Implementations

## History

Le Lann proposed in 1977 an election on a ring in which each identifier goes all the way round. Chang and Roberts published the improvement in 1979: discard each identifier that meets a larger one. They gave the worst case $n(n+1)/2$ and the average case of the number of messages. Lynch calls the algorithm LCR, after Le Lann, Chang and Roberts, and gives it in the synchronous and the asynchronous ring. Hirschberg and Sinclair reached $O(n \log n)$ in 1980 on bidirectional rings, and Peterson and Dolev, Klawe and Rodeh reached it on unidirectional rings in 1982.

## References
