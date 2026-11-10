---
tag: M90XJV
kind: algorithm
slug: double-coverage
name: Double coverage
aliases:
- k-server on a line algorithm
- DC
- double coverage algorithm
area: online-and-streaming/paging-and-caching-online
level: advanced
summary: Optimal deterministic k-server algorithm on a line metric, moving the two nearest servers toward a request.
solves: [k-server-problem]
model: real-ram
complexity:
  vars: {n: the number of requests, k: the number of servers}
  time: {worst: O(n log k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1991
  people: [Marek Chrobak, Howard J. Karloff, Thomas H. Payne, Sundar Vishwanathan, Lawrence L. Larmore]
  note: Chrobak, Karloff, Payne and Vishwanathan gave double coverage for the line and proved that it is k-competitive. Chrobak and Larmore extended it to trees in the same year.
prereqs: [k-server-problem, competitive-ratio, potential-function]
see_also: [work-function-algorithm, k-server-conjecture, tree-metric, metric-tree-embedding, paging-problem]
sources:
  - paper: doi:10.1137/0404017
    title: "Marek Chrobak, Howard J. Karloff, Thomas H. Payne and Sundar Vishwanathan, New results on server problems, SIAM Journal on Discrete Mathematics 4(2) (1991), 172-181"
    locator: the double coverage algorithm on the line and the proof that it is k-competitive
  - paper: doi:10.1137/0220008
    title: "Marek Chrobak and Lawrence L. Larmore, An optimal on-line algorithm for k servers on trees, SIAM Journal on Computing 20(1) (1991), 144-148"
    locator: the extension of double coverage to trees and its potential proof
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 10, the k-server problem, the section on the double coverage algorithm for the line and for trees
  - paper: doi:10.1016/j.cosrev.2009.04.002
    title: "Elias Koutsoupias, The k-server problem, Computer Science Review 3(2) (2009), 105-118"
    locator: Section 3.2, deterministic algorithms for tree metrics
---

Double coverage (DC) is a deterministic online algorithm for the [k-server problem](/k-server-problem/) on the real line. When a request falls between two servers, it moves both of them toward the request at the same speed until one arrives. When the request is outside all servers, only the nearest one moves. DC is $k$-competitive, and no deterministic algorithm can do better, so it is optimal on the line and, in its tree form, on every [tree metric](/tree-metric/).

## In plain words

Some repair vans wait at points on one long road. Calls come in one at a time, and a van must go to each call. If the call is beyond the last van at one end, the nearest van drives there. If the call is between two vans, both of those vans start to drive toward it at the same speed. The one that is nearer arrives first and takes the call. The other van stops where it is.

The second van seems to waste fuel. But it keeps the vans spread in a useful way. The rule that sends only the nearest van can be tricked into driving back and forth for ever, while one far van could fix the problem with one long trip. Double coverage never pays more than a fixed multiple of the best plan.

## The problem

There are $k$ servers at points $s_1 \le s_2 \le \dots \le s_k$ of the real line, and the distance is $d(x, y) = |x - y|$. A sequence $\sigma = r_1, r_2, \ldots, r_m$ of points arrives online. Before the next request is shown, some server must be at $r_t$. The cost is the total distance that the servers move. The aim is a small [competitive ratio](/competitive-ratio/): we want $\mathrm{DC}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + b$, where $\mathrm{OPT}$ is the [offline optimum](/offline-optimum/) from the same start and $b$ depends only on the start positions.

## The algorithm

```pseudo id=main
DOUBLE-COVERAGE(s_1 ≤ … ≤ s_k, σ)
L1  cost ← 0
L2  for each request r in σ do
L3      if r ≤ s_1 then cost ← cost + (s_1 − r), s_1 ← r
L4      else if r ≥ s_k then cost ← cost + (r − s_k), s_k ← r
L5      else find i with s_i ≤ r ≤ s_{i+1}; if r = s_i or r = s_{i+1} then go to the next request
L6          δ ← min(r − s_i, s_{i+1} − r)
L7          s_i ← s_i + δ, s_{i+1} ← s_{i+1} − δ
L8          cost ← cost + 2δ
L9  return cost
```

Lines L3 and L4 handle a request outside the servers: there is only one neighbour, and it moves to the request. Line L5 finds the two neighbours of an inside request. Lines L6 and L7 move both of them by the smaller of the two gaps, so the nearer one arrives at $r$ and the other one stops halfway. Both move by $\delta$, so the cost of line L8 is $2\delta$. The servers stay sorted, because $\delta \le (s_{i+1} - s_i)/2$.

DC is not lazy: it can move a server that does not serve the request. A lazy version, which moves a server only when it must serve and lets the other moves wait, never costs more. DC is easier to analyse in the form above.

## Example

Three servers start at $0, 10, 20$. The requests are $12, 4, 13, 19, 6, 20, 30$.

| request | moves | cost | positions | total |
|---|---|---|---|---|
| 12 | 10 and 20 move by 2 | 4 | 0, 12, 18 | 4 |
| 4 | 0 and 12 move by 4 | 8 | 4, 8, 18 | 12 |
| 13 | 8 and 18 move by 5 | 10 | 4, 13, 13 | 22 |
| 19 | 13 (the right one) moves by 6 | 6 | 4, 13, 19 | 28 |
| 6 | 4 and 13 move by 2 | 4 | 6, 11, 19 | 32 |
| 20 | 19 moves by 1 | 1 | 6, 11, 20 | 33 |
| 30 | 20 moves by 10 | 10 | 6, 11, 30 | 43 |

After the third request, two servers are at 13. The next request 19 is to the right of all servers, so line L4 moves only $s_3$. The request 6 is between 4 and 13, so both of them move by 2, and the server at 13 that is not a neighbour stays.

A brute-force search over all schedules gives $\mathrm{OPT} = 21$ for this sequence, with the configurations $(0,10,20)$, $(0,12,20)$, $(4,12,20)$, $(4,13,20)$, $(4,13,19)$, $(6,13,19)$, $(6,13,20)$, $(6,13,30)$. So DC pays about twice the optimum here, below the bound $3 \cdot 21 + 40 = 103$ of the theorem.

## Correctness

The potential is $\Phi = k \cdot M + \Sigma$, where $M$ is the cost of a minimum matching between the DC servers and the servers of an optimal schedule, and $\Sigma$ is the sum of the distances between all pairs of DC servers. A move of OPT by $d$ raises $\Phi$ by at most $k d$. A move of DC of cost $c$ lowers $\Phi$ by at least $c$: for an outside request, $M$ drops by $\delta$ and $\Sigma$ rises by $(k-1)\delta$; for an inside request, $M$ does not rise and $\Sigma$ drops by $2\delta$. Summing gives $\mathrm{DC}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + \Sigma_0$. The full proof, for the line and for trees, is below.

## Complexity

Each request needs the two neighbours of $r$ in a sorted array, which takes $O(\log k)$ time by binary search, and then $O(1)$ time to move them. The servers stay sorted, so no sort is needed after the first one. The total time is $O(k \log k + m \log k)$ and the extra space is $O(k)$. With the servers in a balanced search tree, the same bounds hold when they are given in any order.

## Properties

- **$k$-competitive.** $\mathrm{DC}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + \sum_{i<j} |s_i - s_j|$, where the $s_i$ are the start positions. The additive constant is $0$ when all servers start at one point.
- **Optimal among deterministic algorithms.** Every deterministic online algorithm has ratio at least $k$ on each metric with at least $k + 1$ points (Manasse, McGeoch and Sleator 1990). On $k+1$ points of the line, the adversary that always requests the uncovered point makes DC pay exactly $k$ times the optimum.
- **Memoryless.** The move depends only on the current positions and the request.
- **For one server it is optimal.** With $k = 1$, DC moves the single server to each request, which is what every schedule must do.

## Variants and improvements

- **Trees.** On a tree, a server is *active* if no other server lies on its path to $r$. All active servers move toward $r$ at the same speed. A server that becomes blocked stops. The phase ends when some server reaches $r$. Chrobak and Larmore proved that this is $k$-competitive on every tree.
- **Lazy double coverage.** Remember the DC positions, but move a real server only when it must serve a request. This never costs more, by the triangle inequality.
- **General metrics.** DC needs the geometry of a line or a tree. On a general metric the best known deterministic algorithm is the [work function algorithm](/work-function-algorithm/), with ratio at most $2k - 1$. A random [tree embedding](/metric-tree-embedding/) followed by DC on the tree gives a randomized algorithm for general metrics, but its ratio grows with the number of points.

## When to use it

Use DC for server, robot or head movement on a line or a tree, where a simple rule with a proven bound is needed. It is the base case that each new idea for the [k-server conjecture](/k-server-conjecture/) must pass. For [paging](/paging-problem/), which is the k-server problem on a uniform metric, use a paging rule such as [LRU](/lru/) instead.

## Pitfalls

- **Moving only the nearest server.** The greedy rule is not competitive. With servers at $0$ and $10$ and the requests $11, 10, 11, 10, \ldots$, greedy moves the server at $10$ back and forth and pays $1$ per request, while the optimum moves the server at $0$ to $10$ once and pays $11$ in total.
- **Moving by the full gap.** If both neighbours move until they reach $r$, the cost is the full gap $s_{i+1} - s_i$, and the two servers end at one point. The rule moves both by the smaller gap only.
- **Ties at equal positions.** Two servers can meet at one point. Keep them as two entries of the sorted array. Line L5 must then find a gap with $s_i \le r \le s_{i+1}$, and a request at that point costs nothing.
- **The additive constant.** The bound needs a constant that depends on the start. If the start positions are far apart, a short sequence can show a large ratio without a contradiction.

## Implementations

## History

Manasse, McGeoch and Sleator defined the k-server problem in 1988 and proved the lower bound $k$. Chrobak, Karloff, Payne and Vishwanathan found double coverage for the line and proved that it is $k$-competitive in their paper "New results on server problems" (SODA 1990, SIAM Journal on Discrete Mathematics 1991). Chrobak and Larmore gave the tree version and a short potential proof in 1991. The potential $k M + \Sigma$ is now the standard example of the potential method in online algorithms.

## References
