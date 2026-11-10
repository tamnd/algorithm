---
tag: NSECNP
kind: problem
slug: list-ranking
name: List ranking
aliases:
- linked-list ranking
area: parallel/parallel-primitives
level: core
summary: Given a linked list in an array, compute for each node its distance to the end of the list. The problem is easy in sequence and is the base of many parallel tree and graph algorithms.
prereqs: [linked-list, pram-model, work-span-model]
see_also: [pointer-jumping, parallel-list-ranking, list-contraction, euler-tour-technique, tree-contraction, all-prefix-sums, cole-vishkin, work-efficiency]
sources:
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 3, Section 3.1 (list ranking, the simple optimal and the randomized algorithms) and Section 3.2 (the Euler tour technique)
  - paper: "James C. Wyllie, The Complexity of Parallel Computations, PhD thesis, Cornell University, 1979 (Technical Report TR 79-387)"
    title: The Complexity of Parallel Computations
    locator: list ranking by pointer doubling in O(log n) time with n processors
  - paper: doi:10.1016/S0019-9958(86)80023-7
    title: Richard Cole and Uzi Vishkin, Deterministic coin tossing with applications to optimal parallel list ranking, Information and Control 70(1), 1986
    locator: pp. 32 to 53 (O(log n log* n) time with n/(log n log* n) processors, and O(log n) time with n log^(k) n / log n processors)
  - paper: "Richard Cole and Uzi Vishkin, Approximate parallel scheduling, Part I: the basic technique with applications to optimal parallel list ranking in logarithmic time, SIAM Journal on Computing 17(1), 1988"
    title: Approximate parallel scheduling, Part I
    locator: pp. 128 to 142 (O(log n) time with n / log n processors)
  - paper: doi:10.1007/BF01759076
    title: Richard J. Anderson and Gary L. Miller, Deterministic parallel list ranking, Algorithmica 6(6), 1991 (first in AWOC 1988, LNCS 319, pp. 81 to 90)
    locator: pp. 859 to 868 (a deterministic algorithm with O(log n) time on the EREW PRAM with n / log n processors)
  - paper: "Robert E. Tarjan and Uzi Vishkin, An efficient parallel biconnectivity algorithm, SIAM Journal on Computing 14(4), 1985"
    title: An efficient parallel biconnectivity algorithm
    locator: pp. 862 to 874 (the Euler tour technique, with tree functions computed by list ranking)
  - paper: "Stephen Cook, Cynthia Dwork and Ruediger Reischuk, Upper and lower time bounds for parallel random access machines without simultaneous writes, SIAM Journal on Computing 15(1), 1986"
    title: Upper and lower time bounds for parallel random access machines without simultaneous writes
    locator: pp. 87 to 97 (the OR of n bits needs Omega(log n) time on a CREW PRAM with any number of processors)
---

List ranking is the problem of computing, for each node of a [linked list](/linked-list/) that is stored in an array, the number of links from the node to the end of the list. A sequential walk solves it in $\Theta(n)$ time, but in parallel it is hard, because the order of the nodes is hidden in the pointers. It is the base of the parallel [Euler tour technique](/euler-tour-technique/), and through it of most parallel algorithms on trees and graphs. On the [EREW PRAM](/erew-pram/) it can be solved in $O(\log n)$ time with $O(n)$ work (Cole and Vishkin 1988; Anderson and Miller 1988).

Notation on this page: $n$ is the number of nodes, $p$ the number of processors, $W$ the work and $S$ the span or parallel time. Each bound below names its model: a [PRAM](/pram-model/) variant or the [work-span model](/work-span-model/).

## In plain words

You get a train of cars in a big yard. Each car has a note that names the car behind it. The cars are not parked in train order: car 7 may be in front of car 2 in the train but far away from it in the yard. Each car wants to know how many cars come behind it.

One worker can start at the front car and walk to the back, then count back. That takes one step per car. Many workers cannot simply split the yard between them, because a worker does not know where a car is in the train until somebody has followed the notes to it. The art of parallel list ranking is to find each car's place without following the notes one by one.

## Definition

**Input.** An array $next[0 \ldots n-1]$ with values in $\{0, \ldots, n-1\} \cup \{\mathit{nil}\}$, such that the graph with an edge $i \to next[i]$ for each $next[i] \ne \mathit{nil}$ is a set of disjoint simple paths. So no two nodes have the same successor, and there is no cycle. A node with $next[i] = \mathit{nil}$ is a tail; a node that is no node's successor is a head.

**Output.** For each node $i$, the value

$$\mathrm{rank}(i) = \min\{\, m \ge 0 : next^{m}(i) \text{ is a tail} \,\},$$

where $next^{m}$ is $next$ applied $m$ times. So the tail has rank 0 and the head of a list of $\ell$ nodes has rank $\ell - 1$.

**Weighted form.** Each node also has a value $x_i$ from a set with an [associative operator](/associative-operator/) $\oplus$. The output is the suffix sum $y_i = x_i \oplus x_{next(i)} \oplus \cdots \oplus x_{t}$, where $t$ is the tail of the list of $i$. With $x_i = 1$ for each node except $x_t = 0$ at the tails and $\oplus = +$, this is $\mathrm{rank}(i)$. The weighted form is also called list prefix sums or list scan.

## Variants

- **Rank from the head.** On one list of $n$ nodes, the position from the head is $n - 1 - \mathrm{rank}(i)$. On a set of lists, first compute each node's head by [pointer jumping](/pointer-jumping/) or by the same ranking on the reversed lists.
- **One list or many.** The definition allows a set of lists. Most algorithms handle the set at no extra cost, and the lower bounds below use it.
- **Circular lists.** A cycle has no tail. Break each cycle at one node first, for example at its smallest index, which itself needs a parallel minimum on each cycle.
- **List to array.** With the ranks, each node writes itself to position $n - 1 - \mathrm{rank}(i)$ of an output array. This turns a linked list into an array in one more parallel step.

## Examples

**One list.** For $next = [6, 7, 5, 0, \mathit{nil}, 1, 2, 4]$ the list is $3 \to 0 \to 6 \to 2 \to 5 \to 1 \to 7 \to 4$, and the ranks by node number are $[6, 2, 4, 7, 0, 3, 5, 1]$. The [pointer jumping](/pointer-jumping/) page traces this input round by round.

**A set of lists.** For $next = [2, \mathit{nil}, \mathit{nil}, 1, 0]$ the lists are $4 \to 0 \to 2$ and $3 \to 1$, and the ranks are $[1, 0, 0, 1, 2]$.

**The Euler tour of a tree.** Take the tree with root 0, children 1 and 2 of node 0, and children 3 and 4 of node 1. Replace each edge by two directed edges. The successor of the directed edge $(u, v)$ is $(v, w)$, where $w$ follows $u$ in the circular list of neighbours of $v$; cut the cycle before the first edge out of the root. The tour is a list of $2(5 - 1) = 8$ nodes:

| tour edge | (0,1) | (1,3) | (3,1) | (1,4) | (4,1) | (1,0) | (0,2) | (2,0) |
|---|---|---|---|---|---|---|---|---|
| rank | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
| position $7 - \mathrm{rank}$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| weight $+1$ down, $-1$ up | +1 | +1 | −1 | +1 | −1 | −1 | +1 | −1 |
| prefix sum of weights | 1 | 2 | 1 | 2 | 1 | 0 | 1 | 0 |

The successors come from local information, but the positions need list ranking. Once the positions are known, a prefix sum over the edges in tour order gives the depth of each vertex at its down edge: depth 1 for nodes 1 and 2, depth 2 for nodes 3 and 4. The prefix count of down edges gives the preorder numbers 1, 2, 3, 4 of the nodes 1, 3, 4, 2. This is why list ranking is the base of the Euler tour technique: a tree computation becomes a sum over a list, and only list ranking can put the list in order.

## Known algorithms

| algorithm | model | time | work | notes |
|---|---|---|---|---|
| sequential walk | RAM | $\Theta(n)$ | $\Theta(n)$ | find each head (the nodes that are nobody's successor), walk, then count back |
| [pointer jumping](/pointer-jumping/), Wyllie 1979 | EREW PRAM, $n$ processors | $\lceil \log_2 n \rceil$ rounds | $\Theta(n \log n)$ | simple, not work-efficient |
| [parallel list ranking](/parallel-list-ranking/) by random mate | work-span, randomized | span $O(\log^2 n)$ w.h.p. | $O(n)$ expected | proved in full on its page |
| Cole and Vishkin 1986, deterministic coin tossing | PRAM | $O(\log n \log^* n)$ | $O(n)$ | $n / (\log n \log^* n)$ processors |
| Cole and Vishkin 1988 | PRAM | $O(\log n)$ | $O(n)$ | $n / \log n$ processors |
| Anderson and Miller 1988 | EREW PRAM | $O(\log n)$ | $O(n)$ | deterministic, $n / \log n$ processors, simpler |

All work-efficient methods use the same plan, [list contraction](/list-contraction/): remove an [independent set](/independent-set/) of nodes and splice the list around them, until the list is small, then rank the small list and put the removed nodes back. They differ in how they choose the independent set (random coins, [deterministic coin tossing](/cole-vishkin/)) and in how they keep $n / \log n$ processors busy.

## Bounds

- **Work.** Each algorithm must read the pointer of each node, so $W = \Omega(n)$. If an algorithm never reads $next[i]$ for some non-tail node $i$, change $next[i]$ to $\mathit{nil}$: the output must change for $i$ and its predecessors, but the run does not.
- **Time with exclusive writes.** On a CREW PRAM, with any number of processors, the OR of $n$ bits needs $\Omega(\log n)$ time (Cook, Dwork and Reischuk 1986). List ranking on a set of lists computes the OR: for bits $x_1, \ldots, x_n$ make nodes $a_1, \ldots, a_{n+1}$ and $b_1, \ldots, b_n$; if $x_i = 1$ link $a_i \to b_i \to a_{i+1}$, else link $a_i \to a_{i+1}$ and leave $b_i$ alone. Each processor builds its links in $O(1)$ time from one bit, and $\mathrm{rank}(a_1) = n + \sum_i x_i$, which is more than $n$ exactly when the OR is 1. So list ranking needs $\Omega(\log n)$ time on the CREW PRAM, and the $O(\log n)$ algorithms above are optimal in time and in work there.
- **Span in the work-span model.** With binary fork and join, a value that depends on all $n$ inputs needs span $\Omega(\log n)$, so the same bound holds there.

## Reductions

- **Prefix sums on an array reduce to list ranking.** An array is a list with $next[i] = i + 1$. So [all-prefix-sums](/all-prefix-sums/) is the special case where the order is known, and it is much easier: work $O(n)$ and span $O(\log n)$ by a balanced tree, with no symmetry breaking.
- **Weighted to unweighted.** The weighted form is solved by the same algorithms: [pointer jumping](/pointer-jumping/) and [list contraction](/list-contraction/) only need associativity of $\oplus$.
- **Tree problems reduce to list ranking.** By the [Euler tour technique](/euler-tour-technique/), the preorder and postorder numbers, the depths and the subtree sizes of an $n$-vertex tree reduce to one weighted list ranking on $2n - 2$ nodes and $O(n)$ extra work in $O(1)$ time (Tarjan and Vishkin 1985).

## Applications

- The Euler tour technique, and through it rooting a tree, preorder numbering, subtree sizes, [lowest common ancestors](/lowest-common-ancestor/) and the biconnectivity algorithm of [Tarjan and Vishkin](/tarjan-vishkin/).
- The leaf numbering that [tree contraction](/tree-contraction/) and [tree expression evaluation](/tree-expression-evaluation/) need.
- Turning a linked list into an array, for example after a parallel graph algorithm produced its output as pointers.
- A test case for parallel machines and models: it has very little arithmetic and only random memory access, so it measures latency and memory bandwidth.

## References
