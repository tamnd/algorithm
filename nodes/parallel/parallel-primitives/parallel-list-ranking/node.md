---
tag: PJYJ60
kind: algorithm
slug: parallel-list-ranking
name: Parallel list ranking
aliases:
- random mate list ranking
area: parallel/parallel-primitives
level: advanced
summary: Rank a linked list in parallel with O(n) expected work. Coin flips pick nodes to splice out, the rounds repeat until the list is empty, then the nodes come back in reverse order.
solves: [list-ranking]
model: work-span-model
complexity:
  vars: {n: the number of nodes}
  time: {expected: O(n)}
  depth: {expected: O(log^2 n)}
  space: {extra: O(n)}
properties: {deterministic: false, recursive: false, in_place: false}
prereqs: [list-ranking, list-contraction, work-span-model, linearity-of-expectation]
see_also: [pointer-jumping, list-contraction, euler-tour-technique, tree-contraction, parallel-pack, cole-vishkin, work-efficiency, independent-set]
sources:
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 3, Section 3.1 (list ranking; the randomized algorithm by independent sets)
  - paper: doi:10.1109/SFCS.1985.43
    title: Gary L. Miller and John H. Reif, Parallel tree contraction and its application, 26th Annual Symposium on Foundations of Computer Science (FOCS), 1985
    locator: pp. 478 to 489 (the random mate step that removes nodes chosen by coin flips)
  - paper: "Richard J. Anderson and Gary L. Miller, A simple randomized parallel algorithm for list-ranking, Information Processing Letters 33(5), 1990"
    title: A simple randomized parallel algorithm for list-ranking
    locator: pp. 269 to 273 (O(log n) expected time with n / log n processors on the EREW PRAM)
  - paper: doi:10.1016/S0019-9958(86)80023-7
    title: Richard Cole and Uzi Vishkin, Deterministic coin tossing with applications to optimal parallel list ranking, Information and Control 70(1), 1986
    locator: pp. 32 to 53 (the deterministic way to choose the nodes to remove)
---

Parallel list ranking by random mate solves [list ranking](/list-ranking/) with $O(n)$ expected work and $O(\log^2 n)$ span. It applies [list contraction](/list-contraction/) to ranks: each round flips a coin at each node, splices out the nodes that flip heads while their successor flips tails, and adds their weight into their predecessors. When no node is left, the nodes come back in the reverse order of the rounds, and each takes its rank from its successor. The result is always exact; only the running time is random. The plain [pointer jumping](/pointer-jumping/) method takes fewer rounds but does $\Theta(n \log n)$ work, so this algorithm is the [work-efficient](/work-efficiency/) one of the two.

Notation on this page: $n$ is the number of nodes, $m_r$ the number of live nodes at the start of round $r$, $R$ the number of rounds, $W$ the work and $S$ the span, both in the [work-span model](/work-span-model/) with binary forking. $\lg$ is $\log_2$.

## In plain words

Cars of a train stand in a yard, and each car knows only the car behind it. Each car wants to know how many cars are behind it.

In each round, every car flips a coin. A car leaves the train if it gets heads and the car behind it gets tails. Two cars next to each other can never both leave. The car in front of a leaving car now links to the car behind it, and it writes down that this link is longer by the length of the old link. Around one car in four leaves in each round.

When the yard is empty, the cars come back in the reverse order. The last car to leave is alone, so it knows its count. Each other car, when it comes back, adds its link length to the count of the car it linked to.

## The problem

The input is an array $next[0 \ldots n-1]$. Each value is a node index or $\mathit{nil}$, and the links form disjoint simple paths, so a set of [linked lists](/linked-list/). The output is $\mathrm{rank}(i)$ for each node $i$: the number of links from $i$ to the tail of its list. The [list ranking](/list-ranking/) page has the full definition, the lower bounds and the other algorithms.

## The algorithm

```pseudo id=main
RANDOM-MATE-RANK(next)                         ▷ next[i] is the successor of node i, or nil
L1  for each node i in parallel: w[i] ← 0 if next[i] = nil, else 1
L2  for each node i with next[i] ≠ nil in parallel: prev[next[i]] ← i
L3  L ← all nodes; H ← an empty stack of sets
L4  while L is not empty do
L5      for each i ∈ L in parallel: coin[i] ← heads or tails, each with probability 1/2
L6      D ← { i ∈ L : coin[i] = heads and (next[i] = nil or coin[next[i]] = tails) }
L7      for each i ∈ D in parallel: h ← prev[i], j ← next[i]; if h ≠ nil then w[h] ← w[h] + w[i], next[h] ← j; if j ≠ nil then prev[j] ← h
L8      L ← L \ D by a pack; push D on H
L9  while H is not empty do D ← pop H
L10     for each i ∈ D in parallel: rank[i] ← w[i] + (rank[next[i]] if next[i] ≠ nil, else 0)
L11 return rank
```

The weight $w[i]$ is the number of input links from $i$ to its current successor. It starts at 1, or at 0 at a tail (line L1). The back pointers of line L2 let a removed node find its predecessor in $O(1)$ time.

Each round has three steps. Line L6 chooses a set $D$ of nodes in which no two are adjacent: a node of $D$ has heads, and its successor has tails, so the successor is not in $D$. Line L7 splices each node of $D$ out of its list. The predecessor $h$ takes over the successor $j$ and adds the weight of the removed node to its own. Since no two nodes of $D$ are adjacent, the splices touch distinct cells and run at the same time. Line L8 packs the live nodes into a smaller array with a [parallel pack](/parallel-pack/), so the next round does work in proportion to the live nodes only.

A removed node keeps its $next$ and $w$ for good. Its $next$ points to a node that was removed in a later round, or is $\mathit{nil}$. So lines L9 and L10 handle the rounds from the last to the first, and each removed node finds the rank of its successor already computed.

## Example

Take $next = [6, 7, 5, 0, \mathit{nil}, 1, 2, 4]$, the list $3 \to 0 \to 6 \to 2 \to 5 \to 1 \to 7 \to 4$. The weights are in brackets. The coins below are one possible outcome.

| round | live list at the start | heads | $D$ | live list after |
|---|---|---|---|---|
| 1 | 3(1) 0(1) 6(1) 2(1) 5(1) 1(1) 7(1) 4(0) | 3, 6, 2, 1, 4 | 3, 2, 1, 4 | 0(1) 6(2) 5(2) 7(1) |
| 2 | 0(1) 6(2) 5(2) 7(1) | 6, 7 | 6, 7 | 0(3) 5(3) |
| 3 | 0(3) 5(3) | 0 | 0 | 5(3) |
| 4 | 5(3) | 5 | 5 | empty |

In round 1, node 6 has heads but is not removed, because its successor 2 also has heads. Node 2 leaves and node 6 takes over its successor 5 with weight $1 + 1 = 2$. Node 4 is a tail with heads, so it leaves, and node 7 becomes a tail with weight 1.

Lines L9 and L10 then put the nodes back:

| round undone | node: $w + $ rank of successor |
|---|---|
| 4 | 5: $3 + 0 = 3$ |
| 3 | 0: $3 + \mathrm{rank}(5) = 6$ |
| 2 | 6: $2 + \mathrm{rank}(5) = 5$; 7: $1 + 0 = 1$ |
| 1 | 3: $1 + \mathrm{rank}(0) = 7$; 2: $1 + \mathrm{rank}(5) = 4$; 1: $1 + \mathrm{rank}(7) = 2$; 4: $0 + 0 = 0$ |

The ranks by node number are $[6, 2, 4, 7, 0, 3, 5, 1]$, the same as a walk along the list.

## Correctness

The key invariant is: for each node $i$, live or removed, $\mathrm{rank}(i) = w[i] + \mathrm{rank}(next[i])$, with $\mathrm{rank}(\mathit{nil}) = 0$. Line L1 makes it true. A splice of node $i$ with predecessor $h$ and successor $j$ keeps it for $h$, because $\mathrm{rank}(h) = w[h] + \mathrm{rank}(i) = (w[h] + w[i]) + \mathrm{rank}(j)$. The splices of one round do not interfere, because $D$ has no two adjacent nodes. Then an induction from the last round to the first shows that line L10 sets the true rank. This holds for any outcome of the coins, so the algorithm is a Las Vegas algorithm. The [full proof](proofs/correctness.md) gives each step.

## Complexity

The [complexity proof](proofs/complexity.md) has the details. The main facts are:

- **Progress per round.** In a round with $m$ live nodes and $t \ge 1$ tails, a non-tail node is removed with probability $1/4$ and a tail with probability $1/2$. So $\mathbb{E}[|D|] = (m + t)/4$ and $\mathbb{E}[m_{r+1}] \le \tfrac34 \mathbb{E}[m_r]$, which gives $\mathbb{E}[m_{r+1}] \le (3/4)^r n$.
- **Rounds.** $\Pr[R > r] \le (3/4)^r n$ by the [Markov inequality](/markov-inequality/). So $\mathbb{E}[R] \le \log_{4/3} n + 5 \approx 2.41 \lg n + 5$, and $R \le (k+1) \log_{4/3} n$ with probability at least $1 - n^{-k}$.
- **Work.** A round costs $O(m_r)$, and $\mathbb{E}[\sum_r m_r] \le 4n$, so $\mathbb{E}[W] = O(n)$. With the charges of the implementation ($m$ for a loop over $m$ nodes, $2m$ for a pack), $W = 4n + 6 \sum_r m_r$ and $\mathbb{E}[W] \le 28n$.
- **Span.** A round has span $O(\log n)$, mostly in the two packs. So $S \le 2(\lceil \lg n \rceil + 1) + R\,(8 \lceil \lg n \rceil + 6) = O(\log^2 n)$ in expectation and with high probability.
- **Space.** The arrays $w$, $prev$, $coin$ and $rank$ and the stack $H$ take $O(n)$ extra space.

The tests measure, on single lists with 20 runs each, a mean of 14.2 rounds for $n = 64$, 23.8 for $n = 1000$ and 27.8 for $n = 4096$, below the bounds 19.5, 29.0 and 33.9. The mean work for $n = 4096$ is $27.97n$, so the bound $28n$ is almost exact for these charges.

## Properties

- **Randomized, always exact.** The coins change the running time, never the output.
- **Exclusive access.** Line L7 writes each cell from at most one node (the proof shows this), and line L10 reads $rank[j]$ only from the one node whose successor was $j$. Line L6 reads $coin[j]$ from $j$ and from its predecessor; two substeps make this exclusive. So on a PRAM the rounds run on the [EREW PRAM](/erew-pram/).
- **Not in place.** It needs the back pointers, the weights, and the record of the rounds.
- **Works on a set of lists.** Each list is handled at the same time, with no extra step.
- **Any associative operator.** With values $x_i$ in place of the weights and $w[h] \leftarrow w[h] \oplus w[i]$ in line L7, the same algorithm computes list suffix sums, as on the [list contraction](/list-contraction/) page.

## Variants and improvements

- **Stop early, then jump.** Stop the contraction when at most $n / \lg n$ nodes are live, rank these by [pointer jumping](/pointer-jumping/), then put the others back. The contraction takes $O(\log \log n)$ rounds in expectation, and pointer jumping does $O((n / \log n) \log n) = O(n)$ work, so the work stays $O(n)$. On a PRAM, where a pack takes $O(\log n)$ time and a pointer jumping round $O(1)$, the time drops to $O(\log n \log \log n)$.
- **Fewer processors, O(log n) time.** Anderson and Miller (1990) give each of $n / \lg n$ processors a queue of $\lg n$ nodes, and only the node at the front of each queue flips. This gives $O(\log n)$ expected time on the EREW PRAM with $O(n)$ work.
- **Deterministic choice.** [Deterministic coin tossing](/cole-vishkin/) (Cole and Vishkin 1986) replaces the coins by a 3-coloring of the list, computed from the bits of the node indices in $O(\log^* n)$ steps. Each color class is an independent set, and a large one can be removed. The deterministic algorithms reach $O(\log n)$ time with $O(n)$ work (Cole and Vishkin 1988; Anderson and Miller 1988).
- **Sparse ruling sets.** Practical codes for multicore processors and GPUs often pick about $n / \lg n$ random rulers, let each ruler walk its sublist to the next ruler in sequence, rank the short list of rulers, and then fill in the others. This needs few rounds and has good memory locality.

## When to use it

- Use it when $n$ is large and the work matters, for example on a multicore machine where the number of cores is much less than $n$. It is the simplest work-efficient list ranking.
- Use [pointer jumping](/pointer-jumping/) when $n$ is small, or when the machine has about $n$ processors, as on a GPU with one thread per node. Pointer jumping needs only $\lceil \lg n \rceil$ rounds and no packs, but it does $\Theta(n \log n)$ work.
- Use a sequential walk when $n$ is small or the list is already close to array order. List ranking does many random memory accesses, and a parallel code needs millions of nodes to beat a good sequential walk.
- Use a deterministic algorithm when random bits are not available or a fixed running time is necessary.

## Pitfalls

- **Removing all nodes with heads.** If line L6 is $D \leftarrow \{ i \in L : coin[i] = \text{heads} \}$, two adjacent nodes can both leave. Then node $i$ writes $next[h]$ for its predecessor $h$, which has left too, and the list breaks. Line L6 must also ask that the successor has tails.
- **Undoing the rounds in the wrong order.** If line L9 takes the sets from the first round to the last, a node reads $rank[next[i]]$ before its successor has a rank. Line L9 must pop the last round first.
- **Forgetting the back pointer.** If line L7 sets $next[h] \leftarrow j$ but not $prev[j] \leftarrow h$, a later round splices $j$ into a removed node. Both pointers must change.
- **A weight of 1 at the tail.** If line L1 sets $w[i] = 1$ at each node, the ranks count nodes, not links, and each rank is too large by 1. A tail starts with weight 0.
- **No pack.** If line L8 only marks nodes as removed and each round scans all $n$ nodes, the work becomes $\Theta(n \log n)$, no better than pointer jumping.

## Implementations

## History

Wyllie (1979) ranked lists by [pointer jumping](/pointer-jumping/) with $\Theta(n \log n)$ work. The search for $O(n)$ work and $O(\log n)$ time drove much of the early work on PRAM algorithms. The coin flip rule that removes a node with heads whose successor has tails is the random mate step that Miller and Reif (1985) used for [tree contraction](/tree-contraction/). Cole and Vishkin (1986) found deterministic coin tossing, which chooses the nodes without random bits. Cole and Vishkin (1988) and Anderson and Miller (1988) reached $O(\log n)$ time with $n / \log n$ processors deterministically, and Anderson and Miller (1990) gave a simple randomized algorithm with the same bounds.

## References
