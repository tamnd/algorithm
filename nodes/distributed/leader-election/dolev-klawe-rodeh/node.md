---
tag: 2S8HY8
kind: algorithm
slug: dolev-klawe-rodeh
name: Dolev-Klawe-Rodeh algorithm
aliases:
- DKR algorithm
area: distributed/leader-election
level: core
summary: Unidirectional ring extrema finding. Each active process runs Franklin's bidirectional test for its active predecessor; all learn the maximum with at most 2n⌊lg n⌋ + 2n messages.
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
  people: [Danny Dolev, Maria Klawe, Michael Rodeh]
  note: Found at the same time as Peterson's algorithm, which uses the same comparison rule.
prereqs: [ring-network, ring-leader-election, franklin, chang-roberts]
see_also: [peterson-leader-election, hirschberg-sinclair, ring-election-lower-bound, explicit-leader-election, message-complexity, find-maximum]
sources:
  - paper: doi:10.1016/0196-6774(82)90023-2
    title: Danny Dolev, Maria Klawe and Michael Rodeh, An O(n log n) unidirectional distributed algorithm for extrema finding in a circle, Journal of Algorithms 3(3), 1982
    locator: pages 245 to 260 (the basic algorithm with messages of two kinds, its bound, and the refined algorithm)
  - paper: doi:10.1145/69622.357194
    title: Gary L. Peterson, An O(n log n) unidirectional algorithm for the circular extrema problem, ACM Transactions on Programming Languages and Systems 4(4), 1982
    locator: pages 758 to 762 (the same basic algorithm, found independently)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 7, Section 7.2 (the algorithm of Peterson and of Dolev, Klawe and Rodeh, and its relation to Franklin's algorithm)
  - paper: doi:10.1145/358506.358517
    title: Randolph Franklin, On an improved algorithm for decentralized extrema finding in circular configurations of processors, Communications of the ACM 25(5), 1982
    locator: pages 336 to 337 (the bidirectional algorithm that the unidirectional one simulates)
---

The Dolev-Klawe-Rodeh algorithm finds the largest identifier on a unidirectional [ring network](/ring-network/) and tells it to every process, with at most $2n \lfloor \lg n \rfloor + 2n$ messages. Its idea is to run [Franklin's](/franklin/) bidirectional algorithm on a ring where messages go only one way: each active process collects the values of its two active predecessors and decides, on behalf of the nearer one, whether that value is a local maximum. The basic algorithm uses the same comparison rule as [Peterson's algorithm](/peterson-leader-election/), found at the same time. This page gives the form of Dolev, Klawe and Rodeh, in which all processes learn the maximum and the process that holds it becomes the leader.

## In plain words

People sit in a circle and can pass notes only to the left. They want to find the largest number in the circle, and everybody must learn it.

A smarter method for a circle where notes can go both ways is this: in each round, each player compares their number with the numbers of the nearest players on both sides, and stays in only if theirs is the biggest. With notes going one way, a player cannot hear from the right. So each player does the test for the player on their right side: they learn that player's number and the number before it, and they compare these with their own. If that player's number wins, the player who did the test carries it on. In the end one number goes all the way round, and its carrier tells everybody that it is the largest.

## The problem

The network is a unidirectional ring of $n \ge 1$ processes $p_0, \ldots, p_{n-1}$ in the [asynchronous model](/asynchronous-model/). Process $p_i$ sends only to $p_{i+1}$, indices modulo $n$, over reliable FIFO channels. Identifiers are distinct and totally ordered, and the processes do not know $n$. All processes start. The task is *extrema finding*: every process must learn the largest identifier. The process that holds it then knows that it is the leader, so this solves the explicit form of [ring election](/ring-leader-election/) with the largest identifier as the leader.

## The algorithm

Each process is active or passive. A passive process forwards each message. An active process holds a value $\mathit{max}$, which is always the identifier of some process. There are three kinds of messages: $\langle \text{one}, x \rangle$ carries the value of an active process, $\langle \text{two}, y \rangle$ carries the value of the active process before it, and $\langle \text{found}, w \rangle$ carries the result.

```pseudo id=main
DOLEV-KLAWE-RODEH(u)                     ▷ the code of the process with identifier u
L1  active ← true, max ← u, status ← unknown
L2  send ⟨one, max⟩ to the next process
L3  on receiving ⟨one, x⟩:
L4      if not active then send ⟨one, x⟩
L5      else if x = max then active ← false, send ⟨found, max⟩   ▷ max went round: it is the largest
L6      else left ← x, send ⟨two, x⟩
L7  on receiving ⟨two, y⟩:
L8      if not active then send ⟨two, y⟩
L9      else if left > max and left > y then max ← left, send ⟨one, max⟩
L10     else active ← false
L11 on receiving ⟨found, w⟩:
L12     result ← w, status ← (leader if w = u else non-leader)
L13     if this process did not send ⟨found⟩ itself then send ⟨found, w⟩
```

Read the active processes of a phase as $a_1, \ldots, a_k$ in ring order with values $t_1, \ldots, t_k$. In Franklin's algorithm $a_{j-1}$ would stay a candidate if $t_{j-1} > \max(t_{j-2}, t_j)$, which needs messages from both sides. Here $a_j$ holds $t_j$, receives $\langle \text{one}, t_{j-1} \rangle$ and then $\langle \text{two}, t_{j-2} \rangle$, and so it can run that test itself (line L9). If the test succeeds, $a_j$ continues with the value $t_{j-1}$. So in each phase exactly the values that survive a round of Franklin's algorithm survive here, each moved one active process down the ring.

## Example

Take $n = 5$ with identifiers $3, 7, 1, 5, 2$ at $p_0, \ldots, p_4$.

| phase | active processes and values | test at each active process | values that survive |
|---|---|---|---|
| 1 | $p_0{:}3$, $p_1{:}7$, $p_2{:}1$, $p_3{:}5$, $p_4{:}2$ | $p_2$: $7 > \max(1, 3)$; $p_4$: $5 > \max(2, 1)$; the others fail | 7 at $p_2$, 5 at $p_4$ |
| 2 | $p_2{:}7$, $p_4{:}5$ | $p_4$: $7 > 5$; $p_2$: $5 < 7$ | 7 at $p_4$ |
| 3 | $p_4{:}7$ | $\langle \text{one}, 7 \rangle$ returns to $p_4$ | 7 is the maximum |

In Franklin's algorithm on the same ring the values 7 and 5 survive round 1, and 7 survives round 2: the same values. The run sends $10 + 10 + 5 = 25$ messages of kinds one and two. Then $p_4$ sends $\langle \text{found}, 7 \rangle$ round the ring, $5$ more messages, and $p_1$, whose identifier is 7, becomes the leader. The total is $30 = 2 \cdot 5 \cdot \lfloor \lg 5 \rfloor + 2 \cdot 5$, the worst case for $n = 5$.

## Correctness

The proof is the same as for [Peterson's algorithm](/peterson-leader-election/), whose proof page gives it in full; the steps are these.

- **What an active process receives.** FIFO channels and passive processes that only forward give $a_j$ first $\langle \text{one}, t_{j-1} \rangle$ and then $\langle \text{two}, t_{j-2} \rangle$ in its phase.
- **Who survives.** The values that survive are the local maxima of the cyclic sequence $t_1, \ldots, t_k$. If $k \ge 2$ there is at least one (the largest value) and at most $\lfloor k/2 \rfloor$, because two neighbours cannot both be local maxima. The largest identifier always survives.
- **The end.** When one active process is left, its value comes back to it as a *one* message (line L5). Its value is the largest identifier, and the *found* message carries it to every process once (lines L11 to L13). The process whose identifier equals it sets status *leader*, and the others set *non-leader*.

## Complexity

**Messages.** In a phase with $k \ge 2$ active processes, each gap between consecutive active processes is crossed by one *one* message and one *two* message, so the phase sends exactly $2n$ messages. There are at most $\lfloor \lg n \rfloor$ such phases, because $k$ at least halves in each of them. In the last phase the *one* message of the last active process goes round the ring, $n$ messages, and the *found* message goes round once more, $n$ messages:

$$M \le 2n \lfloor \lg n \rfloor + 2n.$$

For each $n \le 7$ some order of the identifiers reaches this bound exactly, and for $n = 2^k$ the bit-reversal order reaches it.

**Time.** A phase ends at most $2n$ time units after its last active process starts it, when each message takes at most one time unit. So the time is $O(n \log n)$.

**Space and message size.** Each process stores $\mathit{max}$, $\mathit{left}$ and a flag. Each message holds a kind and one identifier.

## Properties

- **Deterministic and comparison based.**
- **Uniform.** The processes do not know $n$.
- **FIFO channels.** The kinds of the messages say which value is which, but values of two different phases can still be confused without FIFO.
- **The process with the largest identifier is the leader**, and every process knows the maximum. This is the difference from Lynch's form of Peterson's algorithm, where the leader is the process that holds the largest value at the end.
- **Same values as Franklin.** The set of values that survive each phase is the set of survivors of Franklin's algorithm on the same ring, so the number of phases is the same.

## Variants and improvements

- **Peterson's form.** [Peterson's algorithm](/peterson-leader-election/) has the same comparison rule. In Lynch's presentation the process that receives its own value is the leader, without the extra trip that tells the others the maximum, so it costs $n$ messages less.
- **The refined algorithm.** Dolev, Klawe and Rodeh also give a more complex unidirectional algorithm with about $1.356\, n \lg n$ messages in the worst case.
- **Franklin's algorithm.** On a bidirectional ring the test runs at the process itself; see [Franklin's algorithm](/franklin/).

## When to use it

Use it on a unidirectional ring with FIFO channels when every process must learn the maximum, or when the process with the largest identifier must be the leader, with $O(n \log n)$ messages in the worst case. If any process can be the leader and the others need not learn the result, Peterson's form without an announcement saves $n$ messages. On small rings [Chang-Roberts](/chang-roberts/) is simpler.

## Pitfalls

- **Taking the finder for the leader.** The process that runs line L5 holds the largest value, but its own identifier can be small. In the example the finder is $p_4$ with identifier 2.
- **Forgetting the found message.** Without lines L11 to L13 only the finder knows the maximum, and the other passive processes cannot tell that the run has ended.
- **Mixing the two kinds.** A passive process must forward a *two* message as a *two* message. If it changes the kind, the next active process takes the second value for a first one.

## Implementations

## History

Dolev, Klawe and Rodeh published the algorithm in the Journal of Algorithms in 1982, and Peterson published the same comparison rule in ACM Transactions on Programming Languages and Systems in the same year; the two were found independently. Both papers answered the question of whether a unidirectional ring needs $\Theta(n^2)$ messages, after [Hirschberg and Sinclair](/hirschberg-sinclair/) had reached $O(n \log n)$ on bidirectional rings in 1980. Tel presents the basic algorithm and explains it as a simulation of Franklin's algorithm.

## References
