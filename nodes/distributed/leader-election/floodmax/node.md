---
tag: ZNV8N8
kind: algorithm
slug: floodmax
name: FloodMax
aliases:
- Flood max
- Synchronous maximum flooding
area: distributed/leader-election
level: intro
summary: Synchronous leader election in any connected network. Each process floods the largest id it has seen for diam rounds, then the process whose id it kept is the leader. diam·2m messages.
model: synchronous-model
complexity:
  vars: {n: the number of processes, m: the number of edges, d: the known bound on the diameter}
  time: {worst: O(d)}
  messages: {worst: O(d·m)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1996
  people: [Nancy A. Lynch]
  note: A textbook algorithm that shows the basic flooding idea for election in general networks.
prereqs: [synchronous-model, flooding, round-complexity, message-complexity]
see_also: [explicit-leader-election, ring-leader-election, echo-algorithm, awerbuch-leader-election, complete-network-leader-election, tree-leader-election, gallager-humblet-spira, korach-kutten-moran]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 4, Section 4.1 (FloodMax, its invariant, the bound of diam rounds and diam·|E| messages, and OptFloodMax)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 7 (election in general networks by extinction and by wave algorithms)
---

FloodMax elects a leader in any connected network in the [synchronous model](/synchronous-model/). Each process keeps the largest identifier it has seen, and in each round it sends this value to all its neighbours. After a number of rounds equal to a known bound $d$ on the diameter, every process holds the largest identifier, and the process that owns it is the leader. The algorithm uses $d$ rounds and exactly $2md$ messages on a graph with $m$ edges, and every process learns the leader, so it solves [explicit leader election](/explicit-leader-election/).

## In plain words

People stand in a crowd. Each person has a different number and can talk only to the people next to them. Everyone knows how many steps it takes at most to walk from any person to any other.

At each tick of a clock, each person tells all their neighbours the biggest number they have heard so far, and then listens. A big number moves one step further at each tick. After as many ticks as the longest walk, the biggest number has reached everyone.

Then each person checks: if the biggest number is my own number, I am the leader. Otherwise I am not, and I know who the leader is.

## The problem

The network is a connected undirected graph $G = (V, E)$ with $n$ processes and $m$ edges. Each process has a distinct identifier from a totally ordered set. The processes run in lock-step rounds: in each round each process sends messages to its neighbours, then receives all messages sent to it in that round, then changes its state. There are no failures. Every process knows a number $d \ge \mathrm{diam}(G)$; it need not know $n$ or the graph. The goal is that exactly one process outputs *leader*, every other process outputs *non-leader*, and every process learns the identifier of the leader.

## The algorithm

```pseudo id=main
FLOODMAX(u, d)                     ▷ the code of the process with identifier u
L1  max ← u, status ← unknown
L2  for round ← 1 to d do
L3      send max to all neighbours
L4      for each value v received in this round do
L5          if v > max then max ← v
L6  if max = u then status ← leader
L7  else status ← non-leader      ▷ and max is the identifier of the leader
```

The value $\mathit{max}$ never goes down. The process does not need to know which neighbour sent the value; it needs only the largest one.

**OptFloodMax.** A process sends in a round only if its $\mathit{max}$ changed in the round before, or the round is the first. A neighbour already has every older value, so the result does not change.

## Example

Take the path $p_0 - p_1 - p_2 - p_3 - p_4$ with identifiers $3, 1, 5, 2, 7$. The diameter is $4$ and $m = 4$, so take $d = 4$.

| after round | $p_0$ | $p_1$ | $p_2$ | $p_3$ | $p_4$ |
|---|---|---|---|---|---|
| 0 | 3 | 1 | 5 | 2 | 7 |
| 1 | 3 | 5 | 5 | 7 | 7 |
| 2 | 5 | 5 | 7 | 7 | 7 |
| 3 | 5 | 7 | 7 | 7 | 7 |
| 4 | 7 | 7 | 7 | 7 | 7 |

After round 4 only $p_4$ has $\mathit{max}$ equal to its identifier, so $p_4$ is the leader. Each round sends one message in each direction on each edge, $8$ messages, so the run sends $4 \cdot 8 = 32$ messages. OptFloodMax sends $8 + 4 + 3 + 2 = 17$: in round 2 only $p_1$ and $p_3$ send, in round 3 only $p_0$ and $p_2$, in round 4 only $p_1$.

If the processes stop after $3$ rounds, $p_0$ still holds $5$ and has the wrong leader. With other identifiers a process far from the maximum can even keep its own identifier and also claim to be the leader. This is why $d$ must be at least the diameter.

## Correctness

Let $\mathrm{dist}(v, w)$ be the number of edges on a shortest path. Let $u_{\max}$ be the largest identifier and $v_{\max}$ its process.

**Invariant.** After round $r$, $\mathit{max}_v$ is the largest identifier of a process $w$ with $\mathrm{dist}(v, w) \le r$.

*Proof by induction on $r$.* For $r = 0$, $\mathit{max}_v = u_v$ by line L1, and the only process at distance $0$ is $v$. Suppose the claim holds after round $r - 1$. In round $r$, process $v$ receives $\mathit{max}_w$ from each neighbour $w$, with the values after round $r - 1$, and line L5 sets $\mathit{max}_v$ to the largest of these values and its own. By the hypothesis this is the largest identifier in the union of the ball of radius $r - 1$ around $v$ and the balls of radius $r - 1$ around its neighbours. That union is exactly the ball of radius $r$ around $v$: a process at distance $k \le r$ with $k \ge 1$ is at distance $k - 1$ from a neighbour of $v$ on a shortest path, and every process in a neighbour's ball is at distance at most $r$ from $v$. $\square$

**Outputs.** After $d \ge \mathrm{diam}(G)$ rounds the ball of radius $d$ around each $v$ is all of $V$, so $\mathit{max}_v = u_{\max}$ for every $v$. Identifiers are distinct, so line L6 holds at $v_{\max}$ only. Every other process outputs *non-leader* and holds $u_{\max}$. For OptFloodMax the same invariant holds, because a process that does not send in round $r$ sends a value that each neighbour already received in an earlier round.

The [proof of correctness](proofs/correctness/) gives the details and the counts.

## Complexity

**Rounds.** Exactly $d$ rounds. If $d = \mathrm{diam}(G)$, this is the best that any algorithm can do in the worst case for maximum finding: a process at distance $\mathrm{diam}(G)$ from $v_{\max}$ cannot learn $u_{\max}$ in fewer rounds.

**Messages.** In each round each process sends one message on each incident edge, so each edge carries two messages per round:

$$M = 2m \cdot d.$$

With $d = \mathrm{diam}(G)$ this is $O(\mathrm{diam} \cdot m)$, and it can be $\Theta(nm)$, for example on a path or on a ring. OptFloodMax sends at most $2m$ messages in round 1 and then only from processes whose value changed, which is often much less but has the same worst case order.

**Space and message size.** A process stores $\mathit{max}$, its status and a round counter up to $d$. Each message holds one identifier.

## Properties

- **Deterministic and comparison based.**
- **Works on any connected graph**, given a bound $d \ge \mathrm{diam}(G)$.
- **Explicit.** Every process learns the identifier of the leader.
- **The leader has the largest identifier.**
- **All processes stop at the same round**, round $d$, and they know it.
- **Needs synchronous rounds.** In the asynchronous model a process cannot tell when the maximum has reached it.

## Variants and improvements

- **OptFloodMax.** Send only after a change. The worst case is the same, but the count on typical graphs is much lower.
- **Unknown diameter.** If $n$ is known, $d = n - 1$ works. If nothing is known, a process can stop when its value has not changed for a while only if the graph gives a bound on how far a value can lag; in general an algorithm for asynchronous networks is needed.
- **Asynchronous networks.** Each process starts a wave, such as the [echo algorithm](/echo-algorithm/), and smaller waves are extinguished. This costs $O(nm)$ messages in the worst case. [Gallager-Humblet-Spira](/gallager-humblet-spira/) and [Awerbuch's algorithm](/awerbuch-leader-election/) reach $O(m + n \log n)$.
- **Trees and complete graphs.** On a [tree](/tree-leader-election/) the saturation method uses $O(n)$ messages. On a [complete network](/complete-network-leader-election/) $O(n \log n)$ messages are enough.

## When to use it

Use FloodMax when the network is synchronous, the diameter or a bound on it is known, and the cost of $2md$ messages is acceptable. It is the simplest correct election for a general network and a good base for teaching and for tests. When the message count matters, use OptFloodMax or a spanning tree method.

## Pitfalls

- **A bound that is too small.** If $d < \mathrm{diam}(G)$, two processes can both output *leader*: a process whose identifier is the largest within distance $d$ also claims to lead. The test suite builds such a case on a path.
- **A bound that is too large.** It is safe but each extra round costs $2m$ more messages.
- **Mixing up the two forms.** FloodMax sends in every round, and the exact count $2md$ holds only for that form. OptFloodMax sends fewer messages, and its count depends on the identifiers.
- **Using it without synchrony.** In an asynchronous network there are no rounds to count, and the local test at line L6 can be made too early.

## Implementations

## History

Lynch presents FloodMax and OptFloodMax in Section 4.1 of her 1996 book as the basic election algorithm for general synchronous networks, together with the invariant above and a message bound of order $\mathrm{diam} \cdot |E|$. The idea of flooding the extreme value is older and appears in many early papers on extrema finding.

## References
