---
tag: MB1XCY
kind: technique
slug: pointer-jumping
name: Pointer jumping
aliases:
- path doubling
- Wyllie's algorithm
area: parallel/parallel-primitives
level: intro
summary: Replace each pointer by its pointer's pointer, so that each pointer spans twice the distance after each round and every chain is crossed in a logarithmic number of rounds.
prereqs: [linked-list, pram-model, erew-pram]
see_also: [list-ranking, parallel-list-ranking, list-contraction, tree-contraction, euler-tour-technique, work-efficiency, crew-pram, shiloach-vishkin]
sources:
  - paper: "James C. Wyllie, The Complexity of Parallel Computations, PhD thesis, Cornell University, 1979 (Technical Report TR 79-387)"
    title: The Complexity of Parallel Computations
    locator: the list ranking program by pointer doubling on a shared memory machine (exact chapter to be checked)
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 2, Section 2.2 (pointer jumping, with the roots of a forest as the main example), and Chapter 3, Section 3.1 (list ranking)
  - book: isbn:9780262031417
    title: Cormen, Leiserson and Rivest, Introduction to Algorithms, first edition, 1990
    locator: Chapter 30, Section 30.1 (pointer jumping, list ranking and parallel prefix on a list)
---

Pointer jumping is a technique for the [PRAM](/pram-model/) in which every node of a linked structure replaces its pointer $next[i]$ by $next[next[i]]$, all nodes at the same time. After $k$ rounds each pointer jumps over $2^k$ links, so a chain of $n$ nodes is crossed in $\lceil \log_2 n \rceil$ rounds. Wyllie (1979) used it to solve [list ranking](/list-ranking/) in $O(\log n)$ time with $n$ processors, and the method runs on the [EREW PRAM](/erew-pram/). The method is fast but not [work-efficient](/work-efficiency/): it does $\Theta(n \log n)$ work where a sequential walk does $\Theta(n)$.

Notation on this page: $n$ is the number of nodes, $W$ the work (the number of processor steps that do something), $S$ the span or parallel time in synchronous rounds, and $d(i)$ the number of links from node $i$ to the end of its list. The model is the synchronous PRAM.

## In plain words

People stand in a long line. Each person knows only the person in front of them. Each person wants to know how far they are from the front of the line.

In each round, every person asks the person in front of them two things: "who is in front of you?" and "how far does your arrow reach?". Then the person moves their own arrow to point to that person, and adds the two distances. After one round each arrow skips one person, after two rounds it skips three, after three rounds it skips seven. The reach of an arrow doubles in each round. So a line of a million people is done in twenty rounds, but every person works in every round.

## When it applies

- The data is a set of pointer chains: [linked lists](/linked-list/), the parent pointers of a [rooted forest](/rooted-tree/), or a function $f$ on a finite set that you want to iterate.
- You need, for each node, a value that combines the values along the path to the end of its chain with an [associative operator](/associative-operator/): the distance, a sum, the first node of the chain, the root.
- You have many processors and want few rounds, and the extra factor $\log n$ in the work does not matter. When it matters, use [list contraction](/list-contraction/) to shrink the list first.

## The template

The template ranks the nodes of a set of disjoint lists. Each node $i$ has a successor $next[i]$, or $\mathit{nil}$ at a tail. The value $rank[i]$ ends as $d(i)$. The `for all ... in parallel` step is one synchronous PRAM step: each processor reads the old values, and then all processors write.

```pseudo id=main
POINTER-JUMP-RANK(next[0 .. n − 1])
L1  for all i in parallel do
L2      rank[i] ← 0 if next[i] = nil else 1
L3  repeat ⌈log₂ n⌉ times
L4      for all i with next[i] ≠ nil in parallel do
L5          rank[i] ← rank[i] + rank[next[i]]
L6          next[i] ← next[next[i]]
```

The hole in the template is the operator of line L5. With $+$ and the start values of line L2, the result is the distance to the tail. With another associative operator $\oplus$ and start value $x_i$ at each node, the result is the suffix sum $x_i \oplus x_{next(i)} \oplus \cdots \oplus x_{tail}$, if you keep the order of the two operands. Lines L5 and L6 read $rank[next[i]]$ and $next[next[i]]$ before any processor writes.

### The invariant

Let $\mathrm{nx}^{(m)}(i)$ be the node $m$ links after $i$ in the original list, or $\mathit{nil}$ if $d(i) < m$. After $k$ rounds, for each node $i$:

$$next[i] = \mathrm{nx}^{(2^k)}(i), \qquad rank[i] = \min(2^k, d(i)).$$

*Proof.* By induction on $k$. For $k = 0$, line L2 gives $next[i] = \mathrm{nx}^{(1)}(i)$ and $rank[i] = 1 = \min(1, d(i))$ if $i$ has a successor, and $rank[i] = 0 = d(i)$ at a tail. Assume the claim after $k$ rounds and look at node $i$ in round $k + 1$. If $next[i] = \mathit{nil}$, then $d(i) < 2^k$, the node does nothing, and both claims hold for $k + 1$ because $\mathrm{nx}^{(2^{k+1})}(i) = \mathit{nil}$ and $\min(2^{k+1}, d(i)) = d(i) = rank[i]$. Otherwise $j = next[i] = \mathrm{nx}^{(2^k)}(i)$, so $d(i) = 2^k + d(j)$ and $rank[i] = 2^k$. Line L6 sets $next[i] = next[j] = \mathrm{nx}^{(2^k)}(j) = \mathrm{nx}^{(2^{k+1})}(i)$. Line L5 sets $rank[i] = 2^k + \min(2^k, d(j)) = \min(2^{k+1}, 2^k + d(j)) = \min(2^{k+1}, d(i))$. $\square$

After $K = \lceil \log_2 n \rceil$ rounds, $2^K \ge n > d(i)$ for each node, so $rank[i] = d(i)$ and all pointers are $\mathit{nil}$. For one list of $n$ nodes this number of rounds is also needed: the head has $d = n - 1$, and $\min(2^k, n - 1) = n - 1$ needs $2^k \ge n - 1$; the pointers are all $\mathit{nil}$ only when $2^k \ge n$.

### Cost

- **Span.** Each round is $O(1)$ PRAM steps, so $S = \Theta(\log n)$ with $n$ processors.
- **Work.** In round $k + 1$ the active nodes are those with $d(i) \ge 2^k$. On one list of $n$ nodes there are $n - 2^k$ of them, so the number of active steps is exactly $\sum_{k=0}^{K-1} (n - 2^k) = nK - 2^K + 1$, with $K = \lceil \log_2 n \rceil$. This is $\Theta(n \log n)$, and it is $\Theta(n \log n)$ also if every processor is charged for every round. A sequential walk does $\Theta(n)$ work, so pointer jumping is not work-efficient.
- **Exclusive access.** The map $i \mapsto next[i]$ stays injective on the nodes with $next[i] \ne \mathit{nil}$, because $next[i] = \mathrm{nx}^{(2^k)}(i)$ and distinct nodes have distinct successors at the same distance. Split each round in three substeps: each processor reads its own two cells, then each processor $i$ reads the two cells of $next[i]$, then each processor writes its own two cells. No cell is read or written by two processors in one substep, so the template runs on the [EREW PRAM](/erew-pram/).

## Classic examples

The list of the trace is $3 \to 0 \to 6 \to 2 \to 5 \to 1 \to 7 \to 4$, so $next = [6, 7, 5, 0, \mathit{nil}, 1, 2, 4]$ by node number. Each cell shows $rank[i], next[i]$, with the nodes in list order.

| round | 3 | 0 | 6 | 2 | 5 | 1 | 7 | 4 |
|---|---|---|---|---|---|---|---|---|
| start | 1, 0 | 1, 6 | 1, 2 | 1, 5 | 1, 1 | 1, 7 | 1, 4 | 0, nil |
| 1 | 2, 6 | 2, 2 | 2, 5 | 2, 1 | 2, 7 | 2, 4 | 1, nil | 0, nil |
| 2 | 4, 5 | 4, 1 | 4, 7 | 4, 4 | 3, nil | 2, nil | 1, nil | 0, nil |
| 3 | 7, nil | 6, nil | 5, nil | 4, nil | 3, nil | 2, nil | 1, nil | 0, nil |

Three rounds are $\lceil \log_2 8 \rceil$. The active steps are $7 + 6 + 4 = 17 = 8 \cdot 3 - 2^3 + 1$.

- **[List ranking](/list-ranking/).** The template itself, due to Wyllie. It is the base step of [parallel list ranking](/parallel-list-ranking/), which first shrinks the list to about $n / \log n$ nodes and then runs this template, so that the total work is $O(n)$.
- **Roots of a forest.** Each node of a [rooted forest](/rooted-tree/) holds $parent[i]$, and a root points to itself. The round $parent[i] \leftarrow parent[parent[i]]$ makes every node point to its root after $\lceil \log_2 h \rceil$ rounds, where $h \ge 1$ is the largest depth. Many nodes read the cell of one root in the same step, so this form needs a [CREW PRAM](/crew-pram/). JáJá uses it as the first example of the technique.
- **Prefix sums on a list.** Replace $+$ in line L5 by an associative operator. This gives the suffix (or, on the reversed list, the prefix) sums of a list, the list form of [all-prefix-sums](/all-prefix-sums/).
- **Connectivity.** The shortcut step of [Shiloach-Vishkin](/shiloach-vishkin/) connected components is one round of pointer jumping on the parent pointers of the current forest.
- **The Euler tour technique.** The parallel form of the [Euler tour technique](/euler-tour-technique/) ranks the list of the tour edges, and the ranks give preorder numbers, depths and subtree sizes.

## Variations

- **Stop early.** Stop when all pointers are $\mathit{nil}$, which needs a global OR in each round. On a set of short lists this saves rounds; on one list it saves nothing.
- **Any associative operator.** The operator need not be commutative. Keep $rank[i]$ on the left: it covers the links before $next[i]$.
- **Iterating a function.** For any function $f$ on a finite set, $k$ rounds of $g \leftarrow g \circ g$ give $f^{2^k}$. This is the parallel form of repeated squaring, and the basis of binary lifting tables.
- **Work-efficient use.** Do $O(\log \log n)$ rounds of [list contraction](/list-contraction/) until about $n / \log n$ nodes remain, then pointer jumping on the small list costs $O(n)$ work, then put the removed nodes back.

## Pitfalls

- **Writing in place.** If a processor writes $next[i]$ before another processor reads it in the same round, the second processor jumps twice, and the invariant breaks. In a real program, use two arrays and swap them after each round, as the implementation does.
- **Wrong operand order.** With a non-commutative operator, line L5 must be $rank[i] \oplus rank[next[i]]$. The order $rank[next[i]] \oplus rank[i]$ gives a wrong result.
- **Tails that point to themselves.** If a tail points to itself instead of $\mathit{nil}$, many nodes read the cell of the tail in the same step, and the program needs concurrent reads. Line L5 must then also add $0$ at the tail, which the start value $rank = 0$ of the tail gives.
- **Using it for large inputs on few processors.** With $p \ll n$ processors the run takes $\Theta((n \log n)/p)$ time, which is worse than $\Theta(n/p)$. For large lists, use a work-efficient [list ranking](/list-ranking/) method.

## Exercises

1. Show that $\lceil \log_2 n \rceil$ rounds are also enough when the input is a set of disjoint lists of total size $n$, and that they are needed when one list has $n$ nodes.
2. Change the template so that each node also learns the tail of its list. Which cells are read by many processors at the same time?
3. Count the work exactly when the input is $n / m$ lists of $m$ nodes each.

## References
