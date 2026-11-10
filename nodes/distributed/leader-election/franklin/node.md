---
tag: PG80TJ
kind: algorithm
slug: franklin
name: Franklin's algorithm
aliases:
- Franklin's bidirectional ring election
area: distributed/leader-election
level: core
summary: Bidirectional ring election in rounds. Each candidate compares its id with the nearest candidates on both sides and stays only if it is larger. At most 2n⌊lg n⌋ + 2n messages.
solves: [ring-leader-election]
model: asynchronous-model
complexity:
  vars: {n: the number of processes}
  time: {worst: O(n log n)}
  messages: {worst: O(n log n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1982
  people: [Randolph Franklin]
  note: A simpler bidirectional algorithm than Hirschberg-Sinclair, with a smaller constant.
prereqs: [ring-network, ring-leader-election, chang-roberts, message-complexity]
see_also: [hirschberg-sinclair, dolev-klawe-rodeh, peterson-leader-election, ring-election-lower-bound, explicit-leader-election, round-complexity]
sources:
  - paper: doi:10.1145/358506.358517
    title: Randolph Franklin, On an improved algorithm for decentralized extrema finding in circular configurations of processors, Communications of the ACM 25(5), 1982
    locator: pages 336 to 337 (the algorithm and its O(n log n) bound)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 7, Section 7.2 (Franklin's algorithm and the unidirectional simulation of Dolev, Klawe and Rodeh)
  - paper: doi:10.1016/0196-6774(82)90023-2
    title: Danny Dolev, Maria Klawe and Michael Rodeh, An O(n log n) unidirectional distributed algorithm for extrema finding in a circle, Journal of Algorithms 3(3), 1982
    locator: pages 245 to 260 (the unidirectional form of the same comparisons)
---

Franklin's algorithm elects the process with the largest identifier on a bidirectional [ring network](/ring-network/) with FIFO channels. It runs in rounds: each remaining candidate sends its identifier to the nearest candidate on each side, and it stays a candidate only if its identifier is larger than both identifiers it receives. At least half of the candidates drop out in each round with two or more candidates, and each round costs exactly $2n$ messages, so the algorithm sends at most $2n \lfloor \lg n \rfloor + 2n$ election messages. It improves the constant of [Hirschberg-Sinclair](/hirschberg-sinclair/) from about 8 to 2.

## In plain words

People sit in a circle, each with a different number, and can pass notes both ways. At first everyone is a candidate.

In each round, each candidate sends their number to the left and to the right. People who are no longer candidates just pass notes along. So each candidate gets the numbers of the nearest candidate on each side. A candidate whose number is bigger than both stays in. The others drop out and from then on only pass notes.

Two neighbouring candidates cannot both be bigger than each other, so at least half of the candidates drop out in each round. When only one candidate is left, its notes go all the way round and come back to it from both sides. Then it knows that it is the leader, and it tells everyone.

## The problem

The network is a bidirectional ring of $n \ge 1$ processes in the [asynchronous model](/asynchronous-model/), with reliable FIFO channels. Each process has a distinct identifier from a totally ordered set and two ports; the ring need not be oriented. The processes do not know $n$. All processes start. The goal is to make the process with the largest identifier the leader and to tell every process its identifier.

## The algorithm

Each process is *active* (a candidate) or *passive*. A passive process forwards each message to its other port. An active process keeps a queue of the values that have arrived on each port.

```pseudo id=main
FRANKLIN(u)                              ▷ the code of the process with identifier u
L1  active ← true, status ← unknown
L2  send ⟨val, u⟩ on both ports                       ▷ start of a round
L3  on receiving ⟨val, v⟩ on port p: if not active then send ⟨val, v⟩ on the other port
L4      else append v to the queue of port p
L5          when both queues are non-empty: take a from one queue and b from the other
L6          if a = u then status ← leader, send ⟨leader, u⟩ on one port   ▷ the only candidate left
L7          else if u > max(a, b) then
L8              send ⟨val, u⟩ on both ports                ▷ the next round
L9          else active ← false
L10             forward the values still in the queues, each to the port opposite to where it came
L11 on receiving ⟨leader, w⟩ on port p:
L12     if status ≠ leader then status ← non-leader, leader ← w, send ⟨leader, w⟩ on the other port
```

The queues of line L4 matter because the candidates are not in step. A candidate can receive the value of the next round from a fast neighbour on one port while it still waits for the value of the current round on the other port. FIFO channels and the queues make sure that $a$ and $b$ in line L5 belong to the same round. A candidate that drops out passes the values it has stored on (line L10), because they were meant for the next candidate along the ring.

## Example

Take $n = 5$ with identifiers $3, 7, 1, 5, 2$ at $p_0, \ldots, p_4$, linked in this order and from $p_4$ back to $p_0$.

| round | candidates | values received (left, right) | result |
|---|---|---|---|
| 1 | 3, 7, 1, 5, 2 | 3: (2, 7), 7: (3, 1), 1: (7, 5), 5: (1, 2), 2: (5, 3) | 7 and 5 stay |
| 2 | 7, 5 | 7: (5, 5), 5: (7, 7) | 7 stays |
| 3 | 7 | 7: (7, 7) | 7 is the leader |

Each round sends $10$ messages, so the election sends $30$, which is the worst case $2 \cdot 5 \cdot \lfloor \lg 5 \rfloor + 2 \cdot 5$ for $n = 5$. The announcement adds $5$.

## Correctness

The proof follows the candidates from round to round.

- **What a candidate receives.** Let the candidates of a round be $c_1, \ldots, c_k$ in ring order. Passive processes forward everything and channels are FIFO, so in that round $c_j$ receives the value of $c_{j-1}$ on one port and the value of $c_{j+1}$ on the other. When $k = 1$ both are its own value; when $k = 2$ both are the value of the other candidate.
- **Who stays.** $c_j$ stays exactly when its identifier is a local maximum of the cyclic sequence of the identifiers of the candidates. The largest identifier is always a local maximum, and two neighbours cannot both be local maxima. So if $k \ge 2$, between $1$ and $\lfloor k/2 \rfloor$ candidates stay.
- **The end.** No candidate receives its own value while $k \ge 2$, because identifiers are distinct. When $k = 1$ the last candidate, which holds the largest identifier, receives its own value from both sides and becomes the leader (line L6). The announcement passes every other process once.

The full proof is in the [proof of correctness](proofs/correctness/).

## Complexity

**Messages.** In a round with $k \ge 2$ candidates, the value that $c_j$ sends to the right crosses each link between $c_j$ and $c_{j+1}$ once, and the value it sends to the left crosses each link between $c_{j-1}$ and $c_j$ once. So each of the $n$ links carries exactly one message in each direction: $2n$ messages. The number of candidates starts at $n$ and at least halves while it is at least 2, so there are at most $\lfloor \lg n \rfloor$ such rounds. In the last round the two values of the last candidate go round the ring: $2n$ messages. So

$$M \le 2n \lfloor \lg n \rfloor + 2n \text{ election messages}, \qquad \text{plus } n \text{ for the announcement}.$$

The bound is reached for each $n \le 7$ by some order, and for $n = 2^k$ by the bit-reversal order, in which exactly half of the candidates stay in each round.

**Time.** If each message takes at most one time unit, each round ends at most $n$ time units after the last candidate starts it, since each value crosses a gap of at most $n$ hops through passive processes that forward at once. With at most $\lfloor \lg n \rfloor + 1$ rounds, the leader knows within $n(\lfloor \lg n \rfloor + 1)$ time units, which is $O(n \log n)$.

**Space and message size.** A process stores its identifier, its state and the values in its queues. Each message holds one identifier.

## Properties

- **Deterministic and comparison based.**
- **Uniform.** The processes do not know $n$.
- **Works on non-oriented rings.** Both ports are treated alike.
- **Needs FIFO channels**, or round numbers in the messages. Without them a value of the next round can be taken for a value of the current round.
- **The leader has the largest identifier.**

## Variants and improvements

- **Unidirectional rings.** [Dolev, Klawe and Rodeh](/dolev-klawe-rodeh/) run the same test on a unidirectional ring: each candidate tests its predecessor on its behalf. [Peterson's algorithm](/peterson-leader-election/) uses the same rule. Both keep the same values as Franklin's algorithm in each round.
- **Round numbers.** Tag each value with the round number of its sender. A candidate then keeps values of later rounds until it reaches that round, and FIFO is no longer needed.
- **Fixed distances.** [Hirschberg-Sinclair](/hirschberg-sinclair/) does not need FIFO channels, because a candidate probes a fixed distance $2^k$ and waits for answers. It pays with a constant of about 8 in place of 2.

## When to use it

Use it on a bidirectional ring with FIFO channels when the worst case must be $O(n \log n)$ messages with a small constant. If the channels can reorder messages, add round numbers or use Hirschberg-Sinclair. On a unidirectional ring use [Dolev-Klawe-Rodeh](/dolev-klawe-rodeh/).

## Pitfalls

- **Deciding on the first value.** A candidate must wait for one value from each side. A value from one side alone does not tell whether the other neighbour is larger.
- **Dropping stored values.** A candidate that drops out may hold a value of the next round from a fast neighbour (line L10). If it throws this value away, the next candidate waits for ever.
- **Assuming the rounds are in step.** In the asynchronous model different candidates are in different rounds at the same time. The analysis counts messages by round, not by time.

## Implementations

## History

Franklin published the algorithm in 1982 in the Communications of the ACM, as an improvement on the 1980 algorithm of Hirschberg and Sinclair. In the same year Dolev, Klawe and Rodeh, and Peterson, published unidirectional algorithms with the same comparisons. Tel presents Franklin's algorithm together with its unidirectional simulation.

## References
