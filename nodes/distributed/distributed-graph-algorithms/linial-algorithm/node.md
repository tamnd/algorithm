---
tag: RAK95W
kind: algorithm
slug: linial-algorithm
name: Linial's coloring algorithm
aliases:
- Linial coloring
- colour reduction by set systems
area: distributed/distributed-graph-algorithms
level: advanced
summary: Deterministic LOCAL colour reduction by cover-free set families. It takes the identifiers to O(Delta^2) colours in log* n + O(1) rounds, on any graph of maximum degree Delta.
solves: [distributed-vertex-coloring]
model: local-model
complexity:
  vars: {n: the number of nodes, N: the size of the identifier space, Δ: the maximum degree}
  time: {worst: log* N + O(Δ^2)}
  space: {extra: O(Δ log N)}
properties: {deterministic: true, recursive: false}
prereqs: [local-model, graph-coloring, iterated-logarithm, cole-vishkin]
see_also: [cole-vishkin, distributed-vertex-coloring, linial-coloring-lower-bound, ring-coloring, distributed-mis, network-decomposition, probabilistic-method, union-bound]
sources:
  - paper: doi:10.1137/0221015
    title: Nathan Linial, Locality in distributed graph algorithms, SIAM Journal on Computing 21(1), 1992
    locator: pp. 193 to 201 (the colour reduction by set systems, O(Delta^2) colours in O(log* n) rounds, and the lower bound for rings)
  - paper: doi:10.1007/BF02772959
    title: Paul Erdős, Peter Frankl and Zoltán Füredi, Families of finite sets in which no set is covered by the union of r others, Israel Journal of Mathematics 51(1-2), 1985
    locator: pp. 79 to 89 (bounds on the size of cover-free families)
  - paper: doi:10.1137/12088848X
    title: Leonid Barenboim, Michael Elkin and Fabian Kuhn, Distributed (Delta+1)-coloring in linear (in Delta) time, SIAM Journal on Computing 43(1), 2014
    locator: pp. 72 to 95 (deterministic (Delta+1)-colouring in O(Delta) + log* n rounds)
  - book: doi:10.1007/978-3-031-02009-4
    title: Leonid Barenboim and Michael Elkin, Distributed Graph Coloring, Fundamentals and Recent Developments, Morgan and Claypool, 2013
    locator: Chapter 3 (basic distributed colouring algorithms, Linial's algorithm and colour reduction)
  - url: https://jukkasuomela.fi/da2020/
    title: Juho Hirvonen and Jukka Suomela, Distributed Algorithms 2020, online textbook
    locator: Chapter 4 (the LOCAL model, colouring by fast colour reduction)
---

Linial's algorithm is a deterministic distributed algorithm that turns the identifiers of a graph of maximum degree $\Delta$ into a proper colouring with $O(\Delta^2)$ colours in $\log^* N + O(1)$ rounds of the [LOCAL model](/local-model/), where $N$ bounds the identifiers. Each colour names a set from a cover-free family, a family in which no set lies inside the union of $\Delta$ others, and each node takes as its new colour a point of its own set that no neighbour's set holds. One round reduces $m$ colours to $O(\Delta^2 \log m)$ colours. It extends [Cole-Vishkin](/cole-vishkin/) from oriented rings to all graphs, with no orientation needed, and it is the first step of most deterministic algorithms for [distributed vertex colouring](/distributed-vertex-coloring/).

Notation on this page: $G = (V, E)$ is a simple graph with $n$ nodes and maximum degree at most $\Delta \ge 1$, and $N(v)$ is the set of neighbours of $v$. The identifiers are distinct integers in $[0, N)$, and every node knows $N$ and $\Delta$. The model is the synchronous LOCAL model: in each round each node sends a message to each neighbour, receives their messages and computes. $\lg$ is $\log_2$.

## In plain words

Every computer has a different serial number, and it wants a short colour so that no two neighbours share a colour. Each computer has at most a fixed number of neighbours, say three.

Give every possible colour its own set of tokens, chosen in advance so that the sets of any three colours never cover the set of a fourth. Each computer looks at the colours of its neighbours, throws away every token that appears in a neighbour's set, and keeps the smallest token left in its own set. That token is its new colour. A neighbour cannot keep the same token, because that token was in this computer's set, so the neighbour threw it away.

The tokens are far fewer than the old colours, so a few rounds bring the number of colours down to about the square of the degree. Simple clean-up rounds then remove the extra colours.

## The problem

The input is a graph of maximum degree $\Delta$ with distinct identifiers in $[0, N)$. The output is a proper colouring $c : V \to \{0, \dots, \Delta\}$, that is, $c(u) \ne c(v)$ for every edge $\{u, v\}$. This is [distributed vertex colouring](/distributed-vertex-coloring/) with $\Delta + 1$ colours. The cost is the number of rounds.

## The algorithm

A family $S_0, \dots, S_{m-1}$ of subsets of a ground set $U$ is **$\Delta$-cover-free** if no $S_x$ lies inside the union of $\Delta$ sets of the family other than $S_x$. If the current colouring is proper with $m$ colours and each node $v$ takes the least element of

$$S_{c(v)} \setminus \bigcup_{u \in N(v)} S_{c(u)},$$

then the new colouring is proper with $|U|$ colours. The set is not empty, since $v$ has at most $\Delta$ neighbours and their colours differ from $c(v)$. And if $u$ and $v$ are adjacent, the point chosen by $u$ lies outside $S_{c(v)}$, while the point chosen by $v$ lies inside it.

The family used here is built from polynomials. Let $q$ be a prime and $d \ge 1$ with $q^{d+1} \ge m$ and $q > \Delta d$. The colour $x$ names the polynomial $p_x$ of degree at most $d$ over $\mathrm{GF}(q)$ whose coefficients are the base-$q$ digits of $x$, and $S_x = \{(a, p_x(a)) : a \in \mathrm{GF}(q)\}$. Two different polynomials of degree at most $d$ agree at most at $d$ points, so $\Delta$ other sets cover at most $\Delta d < q$ of the $q$ points of $S_x$. The ground set $\mathrm{GF}(q)^2$ has $q^2$ points, and the point $(a, y)$ is the colour $aq + y$.

```pseudo id=main
LINIAL(G, identifiers id in [0, N), maximum degree Δ)
L1  for each node v in parallel do c(v) ← id(v); m ← N
L2  while the prime q with q > Δd and q^(d+1) ≥ m for some d ≥ 1, chosen as small as possible, has q² < m do
L3      for each node v in parallel do send c(v) to all neighbours and receive their colours      ▷ one round
L4          P ← the polynomial over GF(q) whose coefficients are the base-q digits of c(v)
L5          F ← the points (a, P(a)) for a in GF(q) that lie on no polynomial of a neighbour's colour
L6          (a, y) ← the least point of F; c(v) ← a·q + y
L7      m ← q²
L8  for x ← m − 1 down to Δ + 1 do      ▷ one round each
L9      for each node v with c(v) = x in parallel do c(v) ← the least colour in {0, ..., Δ} not used by a neighbour
L10 return c
```

All nodes know $N$ and $\Delta$, so they compute the same sequence of pairs $(q, d)$ and stop the loop in the same round.

## Example

Let $\Delta = 3$ and $N = 10^6$. The loop runs twice: first with $q = 17$ and $d = 5$ ($17 > 15$ and $17^6 \ge 10^6$), which gives $m = 289$, and then with $q = 7$ and $d = 2$ ($7 > 6$ and $7^3 = 343 \ge 289$), which gives $m = 49$. Then $q = 7$ is still the best choice and $49 \not< 49$, so the loop stops. Lines L8 and L9 then take $49 - 4 = 45$ rounds, one for each of the colours $48, \dots, 4$, for 47 rounds in total.

One step of the second round, with $q = 7$ and $d = 2$: a node of colour $100 = 2 \cdot 49 + 0 \cdot 7 + 2$ has the polynomial $2 + 2a^2$, whose values at $a = 0, \dots, 6$ are $2, 4, 3, 6, 6, 3, 4$. Its neighbours have the colours 5, 77 and 288, with the polynomials $5$, $4a + a^2$ and $1 + 6a + 5a^2$.

| $a$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| own, $2 + 2a^2$ | 2 | 4 | 3 | 6 | 6 | 3 | 4 |
| colour 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| colour 77, $4a + a^2$ | 0 | 5 | 5 | 0 | 4 | 3 | 4 |
| colour 288, $1 + 6a + 5a^2$ | 1 | 5 | 5 | 1 | 0 | 2 | 0 |

The neighbour of colour 77 blocks the points $(5, 3)$ and $(6, 4)$. The other three neighbours' polynomials miss the node's points. The least free point is $(0, 2)$, so the new colour is $0 \cdot 7 + 2 = 2$.

## Correctness

The full proof is in the proof file. The one-round step is proper by the argument under the algorithm, for any $\Delta$-cover-free family, and the polynomial family is $\Delta$-cover-free when $q > \Delta d$. Each run of the loop lowers $m$, so the loop stops. In lines L8 and L9 the nodes of colour $x$ are pairwise non-adjacent, so they change at the same time without conflict, and each one finds a free colour in $\{0, \dots, \Delta\}$ because it has at most $\Delta$ neighbours.

The cover-free condition is needed. With $q = 3$, $d = 1$ and $\Delta = 3$, so that $q = \Delta d$, the 9 lines of $\mathrm{GF}(3)^2$ are not 3-cover-free: each line has 3 points, and three other lines through those points cover it.

## Complexity

**One round, with the best family (proved in the proof file).** For $m \ge 2$, a $\Delta$-cover-free family of $m$ subsets of a set of $k = \lfloor e(\Delta + 1)^2 \ln m \rfloor + 1$ points exists. The proof is by the [probabilistic method](/probabilistic-method/): put each point into each set with probability $1/(\Delta + 1)$; a fixed set escapes a fixed group of $\Delta$ others at a fixed point with probability at least $1/(e(\Delta + 1))$, and a [union bound](/union-bound/) over the $m^{\Delta + 1}$ choices finishes the proof. So one round can take $m$ colours to $O(\Delta^2 \log m)$ colours. The nodes can agree on such a family by a fixed search, which costs local computation but no rounds. Erdős, Frankl and Füredi (1985) study how few points such a family can have.

**One round, with polynomials.** With $d = \lceil \lg m \rceil - 1$ and $q$ the least prime above $\Delta d$, Bertrand's postulate gives $q \le 2\Delta d$, so the new number of colours is at most $4 \Delta^2 \lg^2 m$.

**Theorem (proved in the proof file).** Let $p$ be the least prime above $2\Delta$, so $p < 4\Delta$. The loop of line L2 runs $\log^* N + O(1)$ times, with an absolute constant, and stops with at most $\max(p^2, 216) = O(\Delta^2)$ colours. Lines L8 and L9 take fewer than $\max(p^2, 216)$ more rounds.

Each round of the loop maps $\lg m$ to about $2 \lg \lg m + O(\log \Delta)$, which is why the count is $\log^* N$. All bounds are worst case and deterministic. Each message is one colour, so the algorithm also runs in the [CONGEST model](/congest-model/) in the same number of rounds. With $N = n^{O(1)}$, the total is $\log^* n + O(\Delta^2)$ rounds for $\Delta + 1$ colours.

## Properties

- **Deterministic and uniform in the graph.** No orientation and no randomness are needed. A node uses only the colours of its neighbours, and all nodes use the same family.
- **One hop per step.** The colour of a node after $t$ loop rounds depends only on the identifiers in its $t$-hop neighbourhood.
- **The bound depends on $\Delta$, not on $n$.** The number of colours after the loop is $O(\Delta^2)$ for every $n$. Only the $\log^* N$ term grows with the network.
- **Lower bound.** On a ring, $\Delta = 2$, and 3 colours need $\frac{1}{2} \log^* n - O(1)$ rounds by [Linial's lower bound](/linial-coloring-lower-bound/), so no algorithm that ends with $\Delta + 1$ colours can drop the $\log^*$ term.

## Variants and improvements

- **Faster reduction to $\Delta + 1$ colours.** Lines L8 and L9 cost $O(\Delta^2)$ rounds. Barenboim, Elkin and Kuhn (2014) reduce $O(\Delta^2)$ colours to $\Delta + 1$ in $O(\Delta)$ rounds, for a total of $O(\Delta) + \log^* n$; later work brings the dependence on $\Delta$ below linear. The [distributed vertex colouring](/distributed-vertex-coloring/) page lists these results.
- **Defective colouring.** A family in which a set may be partly covered gives a defective colouring, in which a node may share its colour with a few neighbours. Defective colourings are a building block of the faster $(\Delta + 1)$-colouring algorithms; the book of Barenboim and Elkin treats them.
- **Random colour trials.** A randomized algorithm that tries random colours reaches $\Delta + 1$ colours in $O(\log n)$ rounds w.h.p., without the $\Delta^2$ step; see [distributed vertex colouring](/distributed-vertex-coloring/).

## When to use it

Use it as the first step of a deterministic colouring or symmetry-breaking algorithm on graphs of small degree: it turns identifiers into $O(\Delta^2)$ colours in $\log^* n + O(1)$ rounds, and a proper colouring with $k$ colours gives a [maximal independent set](/distributed-mis/) in $k$ more rounds. On an oriented ring or a rooted tree, [Cole-Vishkin](/cole-vishkin/) is simpler and reaches 3 colours directly.

## Pitfalls

- **A family that is not cover-free.** With $q \le \Delta d$ the free set of line L5 can be empty, and the step fails. The example under Correctness shows this for $q = \Delta d$.
- **Nodes that disagree on the parameters.** Every node must use the same $(q, d)$ in each round; the choice may depend only on $m$ and $\Delta$, which all nodes know.
- **Expecting the loop to reach $\Delta + 1$ colours.** The loop stops near $p^2 < 16 \Delta^2$ colours. The reduction to $\Delta + 1$ is a separate phase, with its own cost.
- **Using the degree of the node in place of $\Delta$.** The family must be cover-free against $\Delta$ sets, the largest degree in the graph. A node of small degree in the same graph must still use the common family, or its new colour lies in a different range.
- **Reading $O(\Delta^2 \log m)$ as the polynomial bound.** The existence bound of $O(\Delta^2 \log m)$ points comes from a random family. The explicit polynomial family gives $O(\Delta^2 \log^2 m)$ points in one round, which is enough for the same $\log^* N + O(1)$ total.

## Implementations

## History

Linial (1992) introduced the colour reduction by set systems, with $O(\Delta^2)$ colours in $O(\log^* n)$ rounds, and in the same paper proved the $\Omega(\log^* n)$ lower bound for 3-colouring a ring. The bounds on cover-free families that he used come from Erdős, Frankl and Füredi (1985). Barenboim, Elkin and Kuhn (2014) gave the $O(\Delta) + \log^* n$ algorithm for $\Delta + 1$ colours that improves the $O(\Delta^2)$ clean-up.

## References
