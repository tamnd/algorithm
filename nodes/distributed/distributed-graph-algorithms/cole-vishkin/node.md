---
tag: PCJE4Q
kind: algorithm
slug: cole-vishkin
name: Cole-Vishkin algorithm
aliases:
- Cole-Vishkin coloring
- deterministic coin tossing
area: distributed/distributed-graph-algorithms
level: advanced
summary: Deterministic coin tossing. Each node recolours by the lowest bit where its colour differs from its successor's, which 3-colours an oriented ring in log* n + O(1) rounds.
solves: [ring-coloring]
model: local-model
complexity:
  vars: {n: the number of nodes, N: the size of the identifier space (N >= n)}
  time: {worst: O(log* N)}
  messages: {worst: O(n log* N)}
  space: {extra: O(log N)}
properties: {deterministic: true, recursive: false}
prereqs: [local-model, graph-coloring, iterated-logarithm, round-complexity]
see_also: [ring-coloring, linial-algorithm, linial-coloring-lower-bound, distributed-vertex-coloring, list-ranking, pointer-jumping, ruling-set, three-coloring]
sources:
  - paper: doi:10.1016/S0019-9958(86)80023-7
    title: Richard Cole and Uzi Vishkin, Deterministic coin tossing with applications to optimal parallel list ranking, Information and Control 70(1), 1986
    locator: pp. 32 to 53 (the deterministic coin tossing step and the 3-colouring of a linked list in O(log* n) time)
  - paper: doi:10.1137/0401044
    title: Andrew V. Goldberg, Serge A. Plotkin and Gregory E. Shannon, Parallel symmetry-breaking in sparse graphs, SIAM Journal on Discrete Mathematics 1(4), 1988
    locator: pp. 434 to 446 (the step on rooted trees, and the shift-down reduction from 6 to 3 colours)
  - paper: doi:10.1137/0221015
    title: Nathan Linial, Locality in distributed graph algorithms, SIAM Journal on Computing 21(1), 1992
    locator: pp. 193 to 201 (the lower bound that shows that log* n rounds are needed up to a constant factor)
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: Chapter 7 (vertex colouring, colouring of rings and rooted trees)
  - url: https://jukkasuomela.fi/da2020/
    title: Juho Hirvonen and Jukka Suomela, Distributed Algorithms 2020, online textbook
    locator: Chapter 1 (colouring a path or cycle fast, by the same bit trick)
---

The Cole-Vishkin algorithm, also called deterministic coin tossing, is a deterministic distributed algorithm that [3-colours](/three-coloring/) an oriented ring or a rooted tree in $\log^* N + O(1)$ rounds, where $N$ bounds the node identifiers and $\log^*$ is the [iterated logarithm](/iterated-logarithm/). In each round every node compares its colour with the colour of its successor and takes as its new colour the position of the lowest bit where the two differ, together with the value of its own bit there. A colour of $L$ bits becomes a colour of about $\log_2 L + 1$ bits, so the number of colours falls from $N$ to 6 in $\log^* N$ rounds, and three more rounds give 3 colours. Cole and Vishkin (1986) used it for parallel [list ranking](/list-ranking/), and it is the standard upper bound for [ring colouring](/ring-coloring/).

Notation on this page: the network is a ring $v_0, v_1, \dots, v_{n-1}$ with $n \ge 3$ nodes, and the successor of $v_j$ is $s(v_j) = v_{(j+1) \bmod n}$. Every node knows which neighbour is its successor (the ring is oriented). The identifiers are distinct integers in $[0, N)$, and every node knows $N$. The model is the synchronous [LOCAL model](/local-model/): in each round every node sends a message to each neighbour, receives their messages and computes. $\operatorname{bit}_i(c)$ is bit $i$ of the integer $c$, with bit 0 the least significant. $\lg$ is $\log_2$.

## In plain words

Every computer on a ring has a different serial number, and it wants a colour from three choices so that no two neighbours share a colour. Its serial number is already a colour, but there are far too many colours.

Each computer looks at the next computer on the ring and writes both serial numbers in binary. It finds the first place from the right where the two numbers differ. Its new colour is that place, together with its own digit in that place. Two neighbours cannot get the same new colour: if they chose the same place, their digits in that place differ.

The new colour is a much shorter number than the old one, so a few repetitions bring the number of colours down to six. Three more rounds remove the colours five, four and three, one colour class at a time.

## The problem

The input is a ring of $n$ nodes with an orientation and distinct identifiers in $[0, N)$. The output is a colour $c(v) \in \{0, 1, 2\}$ at every node such that $c(v) \ne c(s(v))$ for every $v$. This is the problem of [ring colouring](/ring-coloring/) with 3 colours, a case of [distributed vertex colouring](/distributed-vertex-coloring/). The cost is the number of rounds.

## The algorithm

The step of lines L4 and L5 maps two different colours $c \ne d$ to

$$f(c, d) = 2i + \operatorname{bit}_i(c), \qquad i = \min\{\, j : \operatorname{bit}_j(c) \ne \operatorname{bit}_j(d) \,\}.$$

All nodes keep the same bound $b$ on the colours, so they all stop the loop in the same round without any communication.

```pseudo id=main
COLE-VISHKIN(ring with successors s, identifiers id in [0, N))
L1  for each node v in parallel do c(v) ← id(v); b ← N
L2  while b > 6 do
L3      for each node v in parallel do send c(v) to both neighbours, and receive c(s(v))      ▷ one round
L4          i ← the least j with bit_j(c(v)) ≠ bit_j(c(s(v)))
L5          c(v) ← 2i + bit_i(c(v))
L6      b ← 2⌈lg b⌉
L7  for x ← 5, 4, 3 do      ▷ one round each
L8      for each node v with c(v) = x in parallel do c(v) ← the least colour in {0, 1, 2} not used by the two neighbours of v
L9  return c
```

Let $T(N)$ be the number of times the loop of line L2 runs. It depends only on $N$: $T(N) = 0$ for $N \le 6$, $T(7) = T(8) = 1$, $T(16) = 2$, $T(17) = T(256) = 3$, $T(2^{16}) = 4$ and $T(2^{65536}) = 5$.

## Example

Take the ring $v_0, \dots, v_5$ with $N = 256$ and the identifiers 213, 87, 215, 154, 138, 14. The bound $b$ goes $256 \to 16 \to 8 \to 6$, so the loop runs 3 times.

| Round | $v_0$ | $v_1$ | $v_2$ | $v_3$ | $v_4$ | $v_5$ |
|---|---|---|---|---|---|---|
| start ($b = 256$) | 213 | 87 | 215 | 154 | 138 | 14 |
| 1 ($b = 16$) | 2 | 14 | 1 | 9 | 4 | 0 |
| 2 ($b = 8$) | 4 | 0 | 6 | 1 | 5 | 2 |
| 3 ($b = 6$) | 5 | 2 | 0 | 4 | 1 | 3 |
| 4 (class 5) | 0 | 2 | 0 | 4 | 1 | 3 |
| 5 (class 4) | 0 | 2 | 0 | 2 | 1 | 3 |
| 6 (class 3) | 0 | 2 | 0 | 2 | 1 | 2 |

In round 1, $v_0$ has $213 = 11010101_2$ and its successor has $87 = 01010111_2$. They first differ at bit 1, and bit 1 of 213 is 0, so $v_0$ takes $2 \cdot 1 + 0 = 2$. Node $v_1$ compares $87$ with $215 = 11010111_2$, which first differ at bit 7, so it takes $2 \cdot 7 + 0 = 14$. In round 4, $v_0$ has colour 5 and its neighbours have 3 and 2, so it takes 0. The final colouring uses 3 colours after 6 rounds.

## Correctness

The full proof is in the proof file. Two facts carry it.

- **The step keeps the colouring proper.** Let $u = s(v)$ and $w = s(u)$, with $c(v) \ne c(u)$ and $c(u) \ne c(w)$. Node $v$ uses the index $i$ where $c(v)$ and $c(u)$ first differ, and $u$ uses the index $i'$ where $c(u)$ and $c(w)$ first differ. If $i \ne i'$, then $2i + \operatorname{bit}_i(c(v)) \ne 2i' + \operatorname{bit}_{i'}(c(u))$, because the two values lie in $\{2i, 2i+1\}$ and $\{2i', 2i'+1\}$. If $i = i'$, the bits $\operatorname{bit}_i(c(v))$ and $\operatorname{bit}_i(c(u))$ differ by the choice of $i$. In both cases the new colours differ.
- **The range shrinks.** If all colours lie in $[0, b)$, they have at most $L = \lceil \lg b \rceil$ bits, so $i \le L - 1$ and the new colour is at most $2L - 1$. This is line L6. For $b \ge 7$ the new bound is $2\lceil \lg b \rceil \ge 6$, so the loop stops with $b = 6$ when $N \ge 7$.

In line L8 the nodes of colour $x$ are pairwise non-adjacent, because the colouring is proper, so they can all change at once. Each has two neighbours, and two neighbours block at most two of the three colours $\{0, 1, 2\}$.

## Complexity

**Theorem (proved in the proof file).** On an oriented ring the algorithm uses exactly $T(N) + 3$ rounds, and $T(N) \le \log^* N$ for every $N \ge 1$. Here $\log^* N$ is the least $k$ with $N \le \operatorname{tower}(k)$, where $\operatorname{tower}(0) = 1$ and $\operatorname{tower}(k+1) = 2^{\operatorname{tower}(k)}$.

The key step: let $L_t = \lceil \lg b_t \rceil$, so that $L_{t+1} = 1 + \lceil \lg L_t \rceil$. If $L \le \operatorname{tower}(k) + 2$ for some $k \ge 1$, then $L \le 2^{\operatorname{tower}(k-1) + 1}$ and so $1 + \lceil \lg L \rceil \le \operatorname{tower}(k-1) + 2$. Starting from $L_0 \le \operatorname{tower}(\log^* N - 1)$, the value $L_t$ drops to 3 or less within $\log^* N - 1$ steps, and one more step gives $b = 6$.

This bound is worst case and deterministic. Each message is one colour of $\lceil \lg N \rceil$ bits or fewer, so the algorithm also runs in the [CONGEST model](/congest-model/) with the same number of rounds. A node sends 2 messages per round, so the total is $2n(T(N) + 3)$ messages. Each node does $O(\log N)$ local work per round. With $N = n^{O(1)}$, the time is $\log^* n + O(1)$, since $\log^*(n^k) \le \log^* n + O(1)$ for a fixed $k$.

## Properties

- **Deterministic.** No random bits; the output is a fixed function of the identifiers.
- **Needs an orientation.** Each node must know which neighbour is its successor, so that every edge is compared by one of its ends. On a ring without orientation, use [Linial's algorithm](/linial-algorithm/), which needs no orientation.
- **Local.** After $t$ loop rounds, the colour of $v$ depends only on the identifiers of $v, s(v), \dots, s^t(v)$.
- **Not the best constant.** The lower bound of [Linial](/linial-coloring-lower-bound/) is $\frac{1}{2} \log^* n - O(1)$ rounds. A node that reads $t$ nodes on both sides can run $2t$ steps for its predecessor at distance $t$, which halves the time; the details are on the [ring colouring](/ring-coloring/) page.

## Variants and improvements

- **Rooted trees.** Goldberg, Plotkin and Shannon (1988) apply the step with the parent in place of the successor. A root acts as if its parent's colour were its own colour with bit 0 flipped. Different children of one node may get the same colour, which is allowed, since they are not adjacent. This gives 6 colours in $T(N)$ rounds.
- **Shift-down for trees.** On a tree, a node can have many neighbours, so line L8 does not work directly. Before each colour class, every node takes the colour of its parent and every root takes a new colour in $\{0, 1, 2\}$ other than its current one. Then all children of a node share one colour, so each node sees at most 2 colours, and the class can recolour. This takes 6 rounds in place of 3.
- **Bounded-degree graphs.** A graph of maximum degree $\Delta$ splits into $\Delta$ rooted forests in one round: each node directs each edge toward the end with the larger identifier and numbers its outgoing edges $1, 2, \dots$, and forest $j$ holds the edges with number $j$. Each node has at most one outgoing edge in a forest, which points to its parent. All forests are 3-coloured at the same time, and the vector of the $\Delta$ colours is a proper colouring with $3^\Delta$ colours. Ways to reduce this to $\Delta + 1$ colours are on the [distributed vertex colouring](/distributed-vertex-coloring/) page.
- **Parallel list ranking.** On the PRAM, the same step 3-colours a linked list in $O(\log^* n)$ time with $n$ processors. Cole and Vishkin used the colours to pick a sparse set of list nodes for [list ranking](/list-ranking/) with $O(n)$ work, where [pointer jumping](/pointer-jumping/) does $\Theta(n \log n)$ work. The cost there is work and span; here it is rounds of message passing.
- **Ruling sets.** The colouring gives a [ruling set](/ruling-set/) in one more round. The nodes whose colour is larger than the colours of both neighbours are pairwise non-adjacent. From any node, a walk that always moves to a neighbour of larger colour stops at such a node within 2 steps, because the colour grows at each step and lies in $\{0, 1, 2\}$. So these nodes form a $(2, 2)$-ruling set.

## When to use it

Use it to break symmetry on paths, rings and rooted trees, and as a subroutine in algorithms for bounded-degree graphs, when a deterministic answer is needed in $O(\log^* n)$ rounds. It needs only one neighbour's colour per round and short messages. For general graphs, [Linial's algorithm](/linial-algorithm/) gives $O(\Delta^2)$ colours in $O(\log^* n)$ rounds in the same way.

## Pitfalls

- **Stopping on the number of bits alone.** The map $b \mapsto 2\lceil \lg b \rceil$ has the fixed point 6. A loop that waits for $b < 6$ never ends. Stop at $b \le 6$ and remove the colours 5, 4 and 3 by line L8.
- **Recolouring two classes at once.** Two nodes of colours 5 and 4 can be adjacent. If both change in the same round, they can choose the same colour. Each round of line L8 handles one class.
- **No common orientation.** If each node picks one neighbour to compare with, without a common orientation, an edge $\{u, v\}$ can be compared by neither end: $u$ and $v$ both pick their other neighbours. Then $u$ and $v$ can get the same new colour. The proof needs every edge to be the successor edge of one of its two ends.
- **Local stopping rules.** If each node stops when its own colour is small, neighbours run different numbers of steps, and the colours can clash. The common bound $b$ makes all nodes stop in the same round.
- **Using $n$ in place of $N$.** The number of rounds depends on the identifier space, not on the ring length. With identifiers up to $2^{64}$, the loop runs $T(2^{64}) = 4$ times even on a ring of 3 nodes.

## Implementations

## History

Cole and Vishkin (1986) introduced deterministic coin tossing for parallel list ranking on the PRAM. Goldberg, Plotkin and Shannon (1988) applied it to rooted trees and to graphs of bounded degree and gave the shift-down reduction from 6 to 3 colours. Linial (1992) proved that $\Omega(\log^* n)$ rounds are needed to 3-colour a ring, so the algorithm is optimal up to a constant factor, and he generalized the colour reduction to all graphs with $O(\Delta^2)$ colours.

## References
