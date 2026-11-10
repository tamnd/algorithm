---
tag: M6ANZC
kind: algorithm
slug: peterson-leader-election
name: Peterson's leader election algorithm
area: distributed/leader-election
level: core
summary: Unidirectional ring election in phases. Each active process takes over the id of its active predecessor if that id is a local maximum, else it relays. At most 2n⌊lg n⌋ + n messages.
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
  people: [Gary L. Peterson]
  note: Found at the same time as the algorithm of Dolev, Klawe and Rodeh, published in the same year.
prereqs: [ring-network, ring-leader-election, chang-roberts, franklin]
see_also: [dolev-klawe-rodeh, hirschberg-sinclair, ring-election-lower-bound, explicit-leader-election, message-complexity, asynchronous-model]
sources:
  - paper: doi:10.1145/69622.357194
    title: Gary L. Peterson, An O(n log n) unidirectional algorithm for the circular extrema problem, ACM Transactions on Programming Languages and Systems 4(4), 1982
    locator: pages 758 to 762 (the algorithm, the 2n log n bound, and the refined version)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 15, Section 15.1.3 (the PetersonLeader algorithm, its correctness and its message bound)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 7, Section 7.2 (the algorithm of Peterson and of Dolev, Klawe and Rodeh)
  - paper: doi:10.1016/0196-6774(82)90023-2
    title: Danny Dolev, Maria Klawe and Michael Rodeh, An O(n log n) unidirectional distributed algorithm for extrema finding in a circle, Journal of Algorithms 3(3), 1982
    locator: pages 245 to 260 (the same basic algorithm, found independently)
---

Peterson's algorithm elects a leader on a unidirectional [ring network](/ring-network/) with $O(n \log n)$ messages, which shows that a second direction is not needed to beat the $\Theta(n^2)$ worst case of [Chang-Roberts](/chang-roberts/). It runs in phases. In each phase every active process learns the temporary identifiers of the two active processes before it; it stays active, and takes over its predecessor's identifier, only if that identifier is larger than both of its neighbours. At most half of the active processes survive each phase, so it sends at most $2n \lfloor \lg n \rfloor + n$ election messages. This page gives the form of Lynch's PetersonLeader; the same algorithm was found at the same time by [Dolev, Klawe and Rodeh](/dolev-klawe-rodeh/).

## In plain words

People sit in a circle and can pass notes only to the left. Each starts with a number, and all start "in the game".

In each round, each player passes their number on, and then passes on the number they got. So each player learns the numbers of the two players before them. Players who are out pass on every note without reading it.

Now each player looks at three numbers: the two they got and their own. If the middle one, the number of the player just before them, is the biggest of the three, the player stays in and adopts that number. Otherwise they leave the game. Two neighbours in the game can never both stay, so at least half of the players leave in each round. When a player gets back their own number, they are the only one left, and they are the leader.

## The problem

The network is a unidirectional ring of $n \ge 1$ processes $p_0, \ldots, p_{n-1}$ in the [asynchronous model](/asynchronous-model/). Process $p_i$ sends only to $p_{i+1}$, indices modulo $n$, and the channels are reliable and FIFO. Identifiers are distinct and totally ordered, and the processes do not know $n$. All processes start. The goal is that exactly one process becomes the leader and every other process learns that it is not the leader and learns the leader's identifier.

## The algorithm

Each process is *active* or a *relay*. A relay forwards each message. An active process holds a temporary identifier $\mathit{tid}$, which is always the identifier of some process.

```pseudo id=main
PETERSON-LEADER(u)                       ▷ the code of the process with identifier u
L1  mode ← active, tid ← u, status ← unknown, waiting ← first
L2  send ⟨val, tid⟩ to the next process
L3  on receiving ⟨val, v⟩:
L4      if mode = relay then send ⟨val, v⟩ to the next process
L5      else if waiting = first then
L6          if v = tid then status ← leader, send ⟨leader, u⟩      ▷ the only active process left
L7          else v1 ← v, waiting ← second, send ⟨val, v1⟩
L8      else waiting ← first                                       ▷ v is the second value
L9          if v1 > max(tid, v) then
L10             tid ← v1, send ⟨val, tid⟩                        ▷ stay active, start the next phase
L11         else mode ← relay
L12 on receiving ⟨leader, w⟩:
L13     if status ≠ leader then status ← non-leader, leader ← w, send ⟨leader, w⟩
```

Let the active processes of a phase be $a_1, \ldots, a_k$ in ring order, with temporary identifiers $t_1, \ldots, t_k$. Relays only forward, and the channels are FIFO, so $a_j$ first receives $t_{j-1}$, the value of its active predecessor (line L7), and then $t_{j-2}$, which $a_{j-1}$ forwards (line L8). Process $a_j$ then plays the role of $a_{j-1}$: it keeps $t_{j-1}$ alive if $t_{j-1}$ is a local maximum among $t_{j-2}, t_{j-1}, t_j$ (lines L9 and L10). A value that returns to its sender (line L6) has passed no other active process, so the sender is the last one.

## Example

Take $n = 5$ with identifiers $3, 7, 1, 5, 2$ at $p_0, \ldots, p_4$.

| phase | active processes and their tid | values received $(v_1, v_2)$ | result |
|---|---|---|---|
| 1 | $p_0{:}3$, $p_1{:}7$, $p_2{:}1$, $p_3{:}5$, $p_4{:}2$ | $p_0{:}(2,5)$, $p_1{:}(3,2)$, $p_2{:}(7,3)$, $p_3{:}(1,7)$, $p_4{:}(5,1)$ | $p_2$ takes 7, $p_4$ takes 5 |
| 2 | $p_2{:}7$, $p_4{:}5$ | $p_2{:}(5,7)$, $p_4{:}(7,5)$ | $p_4$ takes 7 |
| 3 | $p_4{:}7$ | $p_4{:}(7)$ | $p_4$ is the leader |

Phases 1 and 2 send $2 \cdot 5 = 10$ messages each, and phase 3 sends $5$, so there are $25$ election messages and $5$ announcement messages. The leader is $p_4$, whose own identifier is 2. Its temporary identifier is 7, the largest identifier, but the process that holds 7 is not the leader.

## Correctness

The proof follows the active processes from phase to phase.

- **What an active process receives.** By FIFO channels and relays that only forward, the active process $a_j$ receives $t_{j-1}$ and then $t_{j-2}$ in its phase, as said above. For $k = 2$ this is $t_{j-1}$ and then its own $t_j$.
- **Who survives.** $a_j$ survives exactly when $t_{j-1}$ is larger than both neighbouring values in the cyclic sequence $t_1, \ldots, t_k$. The temporary identifiers stay distinct, because the survivors carry the values of different predecessors.
- **At least one and at most half survive.** If $k \ge 2$, the successor of the process with the largest $t$ survives. Two consecutive values cannot both be local maxima, so at most $\lfloor k/2 \rfloor$ processes survive.
- **The end.** When $k = 1$, the only active process receives its own value and becomes the leader (line L6). No process becomes the leader while $k \ge 2$, because then each first value comes from another active process with a different value.

So exactly one process becomes the leader, its $\mathit{tid}$ is the largest identifier, and the announcement of lines L12 and L13 reaches every other process once. The full proof is in the [proof of correctness](proofs/correctness/).

## Complexity

**Messages.** In a phase with $k \ge 2$ active processes, each value of line L2 or L10 travels from an active process to the next one, and each value of line L7 does the same. The gaps between consecutive active processes add up to $n$, so the phase sends exactly $2n$ messages. The number $k$ starts at $n$ and at least halves while $k \ge 2$, so there are at most $\lfloor \lg n \rfloor$ such phases. The last phase sends $n$ messages. In total:

$$M \le 2n \lfloor \lg n \rfloor + n \text{ election messages}, \qquad \text{plus } n \text{ for the announcement}.$$

The bound is reached for $n = 2^k$ by the bit-reversal order, for example $0, 4, 2, 6, 1, 5, 3, 7$ for $n = 8$, where exactly half of the active processes survive each phase. For each $n \le 7$ the largest count over all orders is also exactly $2n \lfloor \lg n \rfloor + n$.

**Time.** If each message takes at most one time unit, a phase ends at most $2n$ time units after the last active process starts it: the first value crosses a gap of at most $n$ hops, and the second value follows it at most $n$ hops later. With at most $\lfloor \lg n \rfloor + 1$ phases the time is $O(n \log n)$. On the example ring the leader knows after 12 synchronous rounds.

**Space and message size.** A process stores $\mathit{tid}$, $v_1$, its mode and its status. Each message holds one identifier.

## Properties

- **Deterministic and comparison based.**
- **Uniform.** The processes do not know $n$.
- **Needs FIFO channels.** Without FIFO, a value of the next phase can overtake the second value of the current phase, and line L9 compares the wrong values. Tagging each value with the phase number and the position (first or second) removes this need.
- **The leader is not the process with the largest identifier.** It is the process that ends up holding the largest value. If the largest identifier must win, the leader announces $\mathit{tid}$ and the process whose identifier equals it takes over, which is the form of [Dolev, Klawe and Rodeh](/dolev-klawe-rodeh/).
- **Optimal up to the constant**, by the [ring election lower bound](/ring-election-lower-bound/).

## Variants and improvements

- **Dolev, Klawe and Rodeh.** The same comparison rule, found independently and published in the same year. Their paper frames it as extrema finding and explains it as a simulation of a bidirectional algorithm; see [their page](/dolev-klawe-rodeh/) for the difference.
- **Fewer messages per phase.** Peterson's paper also gives a refined version in which each active process sends one value per phase and the phases alternate between keeping larger and keeping smaller values. It uses about $1.44\, n \lg n$ messages.
- **Bidirectional rings.** [Franklin's algorithm](/franklin/) applies the same local maximum rule to an active process and its two active neighbours directly, with at most $2n \lfloor \lg n \rfloor + 2n$ messages.

## When to use it

Use it on a unidirectional ring when the worst case must be $O(n \log n)$ messages, the channels are FIFO, and it does not matter which process leads. When the channels may reorder messages, tag each value with its phase. When the process with the largest identifier must be the leader, use the form of Dolev, Klawe and Rodeh, which costs $n$ more messages. On small rings [Chang-Roberts](/chang-roberts/) is simpler.

## Pitfalls

- **Assuming the leader has the largest identifier.** In the example the leader $p_4$ has identifier 2.
- **Skipping the forward in line L7.** The successor then never gets its second value, and the run stops in the middle of a phase.
- **Non-FIFO channels.** The example works only because each active process gets its first and second values in order.
- **Counting phases.** There are at most $\lfloor \lg n \rfloor$ phases with two or more active processes and one more phase for the last process. Forgetting the last phase loses $n$ messages.

## Implementations

## History

Peterson published the algorithm in 1982 in ACM Transactions on Programming Languages and Systems. In the same year Dolev, Klawe and Rodeh published the same basic algorithm in the Journal of Algorithms, and both papers improved the constant further. These were the first unidirectional ring algorithms with $O(n \log n)$ messages. Lynch presents the algorithm as PetersonLeader in her chapter on asynchronous rings.

## References
