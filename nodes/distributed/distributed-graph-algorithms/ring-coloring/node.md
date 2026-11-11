---
tag: MBAS0X
kind: problem
slug: ring-coloring
name: Ring coloring
aliases:
- 3-coloring of a cycle in distributed setting
- cycle coloring
area: distributed/distributed-graph-algorithms
level: advanced
summary: Properly 3-colour the nodes of a ring network. In the LOCAL model this takes (1/2) log* n ± O(1) rounds on an oriented ring, by Cole-Vishkin and Linial's lower bound.
prereqs: [local-model, graph-coloring, iterated-logarithm, three-coloring]
see_also: [cole-vishkin, linial-coloring-lower-bound, linial-algorithm, distributed-vertex-coloring, distributed-mis, distributed-maximal-matching, ruling-set, list-ranking]
sources:
  - paper: doi:10.1016/S0019-9958(86)80023-7
    title: Richard Cole and Uzi Vishkin, Deterministic coin tossing with applications to optimal parallel list ranking, Information and Control 70(1), 1986
    locator: pp. 32 to 53 (3-colouring a linked list in O(log* n) time)
  - paper: doi:10.1137/0221015
    title: Nathan Linial, Locality in distributed graph algorithms, SIAM Journal on Computing 21(1), 1992
    locator: pp. 193 to 201 (the (1/2) log* n − 1 lower bound for 3-colouring the n-cycle and the matching upper bound)
  - paper: doi:10.1145/2611462.2611505
    title: Juhana Laurinharju and Jukka Suomela, Brief announcement, Linial's lower bound made easy, PODC 2014
    locator: pp. 377 and 378 (the lower bound log*(n)/2 − 1 for directed cycles)
  - paper: doi:10.1137/0404036
    title: Moni Naor, A lower bound on probabilistic algorithms for distributive ring coloring, SIAM Journal on Discrete Mathematics 4(3), 1991
    locator: pp. 409 to 412 (Omega(log* n) for randomized algorithms)
  - url: https://jukkasuomela.fi/da2020/
    title: Juho Hirvonen and Jukka Suomela, Distributed Algorithms 2020, online textbook
    locator: Chapter 1 (colouring a path or a cycle fast) and Chapter 11 (hardness of colouring)
---

Ring colouring is the problem of giving every node of a ring network one of three colours so that neighbours get different colours, by a distributed algorithm in which each node starts knowing only its own identifier. It is the simplest problem of symmetry breaking: all nodes look the same except for their identifiers, and the question is how many rounds of the [LOCAL model](/local-model/) are needed. The answer is $\frac{1}{2} \log^* n \pm O(1)$ on an oriented ring, where $\log^*$ is the [iterated logarithm](/iterated-logarithm/): [Cole-Vishkin](/cole-vishkin/) gives the upper bound and [Linial's lower bound](/linial-coloring-lower-bound/) the lower bound. Two colours, in contrast, need a number of rounds linear in $n$.

Notation on this page: the ring has nodes $v_0, \dots, v_{n-1}$ with $n \ge 3$ and the edges $\{v_j, v_{(j+1) \bmod n}\}$. The identifiers are distinct integers in $[0, N)$ with $N \ge n$, usually $N = n^{O(1)}$, and every node knows $N$. On an oriented ring every node knows which neighbour is its successor $v_{(j+1) \bmod n}$. $T(N)$ is the number of colour reduction steps of Cole-Vishkin, with $T(N) \le \log^* N$.

## In plain words

Computers sit in a circle, and each can talk only to the two next to it. Each has a different serial number. They want to paint themselves with three paints so that no two neighbours share a paint. Talks happen in rounds, and the question is how many rounds they need.

With unlimited time, they could pass all serial numbers around the circle and then paint by a fixed rule. That takes rounds in proportion to the size of the circle. The surprise is that three paints need almost no time at all: the number of rounds grows like the number of times one must take a logarithm to bring the circle size down to one, which is at most five for any real network. Two paints are different: then a computer's paint depends on far-away parts of the circle, so the rounds grow with the size of the circle.

## Definition

**Input.** A ring of $n$ nodes in the synchronous LOCAL model. Each node knows its identifier, $N$, and on an oriented ring its successor.

**Output.** A colour $c(v) \in \{1, 2, 3\}$ at every node, with $c(v_j) \ne c(v_{(j+1) \bmod n})$ for all $j$.

**Cost.** The number of rounds until every node has fixed its colour, in the worst case over the placement of the identifiers. For a randomized algorithm, the output must be correct with high probability.

## Variants

- **Oriented and unoriented rings.** On an unoriented ring, a node cannot tell its two neighbours apart by direction. The lower bound still holds, since it holds for oriented rings. Cole-Vishkin needs the orientation; [Linial's algorithm](/linial-algorithm/) does not.
- **More colours.** A $c$-colouring for a fixed $c \ge 3$ takes $\Theta(\log^* n)$ rounds as well: it costs at most as much as a 3-colouring, and turns into one in $c - 3$ rounds.
- **Two colours.** Only even rings have a 2-colouring, and finding one takes $\Theta(n)$ rounds; see Bounds.
- **Paths and rooted trees.** A path is a ring with one edge removed, and the same bounds hold. On rooted trees, the method of Goldberg, Plotkin and Shannon (1988) gives 3 colours in $\log^* N + O(1)$ rounds; see [Cole-Vishkin](/cole-vishkin/).
- **Linked lists in the PRAM.** On a PRAM, a linked list with one processor per node is an oriented path, and 3-colouring it is a step of [list ranking](/list-ranking/). The cost there is parallel time and work, not rounds.

## Examples

The oriented ring of 6 nodes with identifiers 213, 87, 215, 154, 138, 14 and $N = 256$: Cole-Vishkin maps the identifiers to $2, 14, 1, 9, 4, 0$, then to $4, 0, 6, 1, 5, 2$, then to $5, 2, 0, 4, 1, 3$, all proper, and three more rounds give $0, 2, 0, 2, 1, 2$. That is 6 rounds; the [Cole-Vishkin](/cole-vishkin/) page shows each step.

A non-example: on the ring of 5 nodes, no 2-colouring exists, because an odd cycle is not bipartite. On the ring of 6 nodes, a 2-colouring exists, but with $t$ rounds and $4t + 3 \le n$ no algorithm finds it, as shown under Bounds.

## Known algorithms

| Algorithm | Ring | Rounds (worst case, deterministic) |
|---|---|---|
| Gather the whole ring, then colour by a fixed rule | any | $\lfloor n/2 \rfloor$ |
| [Cole-Vishkin](/cole-vishkin/) | oriented | $T(N) + 3 \le \log^* N + 3$ |
| Cole-Vishkin, two steps per round (below) | oriented | $\lceil T(N)/2 \rceil + 3 \le \frac{1}{2} \log^* N + 4$ |
| [Linial's algorithm](/linial-algorithm/) with $\Delta = 2$, then removal of colour classes | any | $\log^* N + O(1)$ to 25 colours, then 22 rounds |

**Two steps per round.** In $t$ rounds of the LOCAL model, a node $v$ learns the identifiers of the $t$ nodes before it and the $t$ nodes after it. After $s$ steps of Cole-Vishkin, the colour of a node $u$ depends only on the identifiers of $u$ and the $s$ nodes after it. So $v$ can compute the colour after $2t$ steps of the node $u$ that lies $t$ positions before $v$. Let $v$ output that colour. If $v$ and $w$ are adjacent with $w$ after $v$, the nodes $t$ positions before them are also adjacent, in the same order, so the outputs differ. With $t = \lceil T(N)/2 \rceil$ this gives a proper colouring with 6 colours, and three rounds of class removal give 3 colours.

## Bounds

**Upper bound.** $\frac{1}{2} \log^* N + 4$ rounds on oriented rings, by the construction above. With $N = n^{O(1)}$ this is $\frac{1}{2} \log^* n + O(1)$.

**Lower bound (Linial 1992).** Every deterministic algorithm that 3-colours all directed $n$-cycles with identifiers $\{1, \dots, n\}$ needs at least $\frac{1}{2} \log^* n - 1$ rounds. The proof is on the page [Linial's colouring lower bound](/linial-coloring-lower-bound/). Naor (1991) shows that randomized algorithms also need $\Omega(\log^* n)$ rounds. So the deterministic complexity on oriented rings is $\frac{1}{2} \log^* n \pm O(1)$.

**Two colours need $\Theta(n)$ rounds.** Gathering the ring takes $\lfloor n/2 \rfloor$ rounds. For the lower bound, let $\mathcal{A}$ 2-colour every even directed $n$-cycle in $t$ rounds, and assume $n \ge 4t + 3$. The output of a node depends only on the $2t + 1$ identifiers centred at it. Place two disjoint windows $W_u$ and $W_w$ of $2t + 1$ identifiers around nodes $u$ and $w$ so that $w$ is $d$ steps after $u$, with $d = 2t + 2$; the arc from $w$ back to $u$ then has $n - d \ge 2t + 1$ steps. In a 2-colouring, $c(u) = c(w)$ exactly when $d$ is even. Now move one identifier that lies strictly between the two windows on the short arc to the long arc. The windows, and so the outputs of $u$ and $w$, do not change, but the distance becomes $d - 1$, and the parity flips. This is a contradiction, so $n \le 4t + 2$, that is $t \ge (n - 2)/4$.

## Reductions

- **3-colouring gives an MIS in 3 rounds.** For $x = 1, 2, 3$, every node of colour $x$ with no neighbour in the set joins it. Nodes of one colour are not adjacent, so they can decide at once.
- **An MIS gives a 3-colouring in 1 round**, and a maximal matching of a directed ring gives a 3-colouring in 1 round; the [lower bound page](/linial-coloring-lower-bound/) has both. So 3-colouring, [MIS](/distributed-mis/) and [maximal matching](/distributed-maximal-matching/) on rings all take $\Theta(\log^* n)$ rounds.
- **Ruling sets.** A 3-colouring gives a $(2, 2)$-[ruling set](/ruling-set/) in one round: the nodes whose colour is larger than both neighbours' colours.
- **Vertex colouring.** Ring colouring is [distributed $(\Delta + 1)$-colouring](/distributed-vertex-coloring/) with $\Delta = 2$, so every lower bound for rings is a lower bound for that problem.

## Applications

- **Parallel list ranking.** The colouring picks a sparse set of list nodes that splices out the others, which leads to [list ranking](/list-ranking/) with linear work.
- **Colouring of trees and bounded-degree graphs.** A graph of maximum degree $\Delta$ splits into $\Delta$ rooted forests, and each is coloured as on a ring, which is the start of several $(\Delta + 1)$-colouring algorithms.
- **Lower bounds.** The ring is the standard hard case: the $\Omega(\log^* n)$ bound transfers to every problem that turns into ring colouring in $O(1)$ rounds.

## References
