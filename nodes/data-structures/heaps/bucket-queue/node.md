---
tag: DVKCF0
kind: data-structure
slug: bucket-queue
name: Bucket queue
aliases:
- bucket priority queue
- Dial's buckets
area: data-structures/heaps
level: core
summary: Array of buckets indexed by integer key, efficient when keys are small integers.
implements: [priority-queue]
model: word-ram
prereqs: [priority-queue, doubly-linked-list, decrease-key]
see_also: [dial-algorithm, radix-heap, calendar-queue, counting-sort, degeneracy-ordering, k-core, binary-heap, timing-wheel]
sources:
  - paper: "Robert B. Dial, Algorithm 360: Shortest-path forest with topological ordering, Communications of the ACM 12(11), 1969"
    locator: pages 632 to 633
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 4 (Shortest paths, label-setting algorithms), the section on Dial's implementation
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox
    locator: Chapter 10 (Shortest paths), the section on monotone integer priority queues, bucket queues
---

A bucket queue is a [priority queue](/priority-queue/) for items whose keys are integers in a small range $0 \ldots C$. It keeps an array of $C + 1$ buckets, where the bucket $B[k]$ is a list of the items with key $k$, and a cursor $\mathit{cur}$ that is at most the smallest key in the queue. Insert, delete and [decrease-key](/decrease-key/) take $O(1)$ time, because they only add an item to a bucket or remove it. Extract-min moves the cursor up past empty buckets, so it costs $O(1 + s)$ for $s$ skipped buckets. When the keys that are taken out never decrease, the cursor only goes up, and a whole run costs $O(n + C)$. This is the structure of [Dial's algorithm](/dial-algorithm/) (1969) for shortest paths with small integer edge weights, and of the linear-time [degeneracy ordering](/degeneracy-ordering/).

## In plain words

Suppose each item has a priority that is a small whole number, for example 0 to 100. Make 101 boxes in a row, one for each number. To add an item, drop it in its box. To change its number, take it out of one box and drop it in another.

To find the item with the smallest number, start at the left and walk right to the first box that is not empty. Keep a finger where you stopped. If the numbers you take out only grow, you never walk back, so all the walking for all items together is at most the number of boxes. No item is ever compared with another.

## The abstract type

A bucket queue implements the min-[priority queue](/priority-queue/) for integer keys in $0 \ldots C$: INSERT$(x, k)$, DELETE$(x)$, DECREASE-KEY$(x, k)$, FIND-MIN and EXTRACT-MIN. Items are named by a handle, here a hashable value, so that the caller can find them again. The type is often used in the *monotone* setting, where each key inserted is at least the last key extracted; Dijkstra's algorithm with non-negative integer weights has this property.

## Representation

- An array $B[0 \ldots C]$ of buckets. Each bucket is a [doubly linked list](/doubly-linked-list/), or any set with $O(1)$ insert, delete and "take any element". The Python code uses an insertion-ordered dictionary, so each bucket is first in, first out.
- A map $\mathit{key}$ from each item to its key. With items numbered $0 \ldots m - 1$, it is an array, and each item also stores its list node.
- A cursor $\mathit{cur}$ with the invariant that every non-empty bucket has index at least $\mathit{cur}$. It starts at $C + 1$.

The space is $\Theta(C + n)$ for $n$ items.

## Operations

```pseudo id=main
INSERT(Q, x, k)
L1  if k < 0 or k > C then error "key out of range"
L2  append x to B[k]; key[x] ← k
L3  if k < cur then cur ← k

DELETE(Q, x)
L4  remove x from B[key[x]]; remove x from key

DECREASE-KEY(Q, x, k)
L5  if k > key[x] then error "new key is larger"
L6  DELETE(Q, x); INSERT(Q, x, k)

EXTRACT-MIN(Q)
L7  if Q is empty then error "underflow"
L8  while B[cur] is empty do cur ← cur + 1
L9  x ← the first item of B[cur]
L10 DELETE(Q, x)
L11 return (x, cur)
```

Line L3 keeps the cursor invariant when a key below the cursor arrives; in the monotone setting this never happens except in the first insert. Line L8 moves the cursor to the first non-empty bucket; it stops inside the array because the queue is not empty and, by the invariant, every item sits at index at least $\mathit{cur}$. FIND-MIN is lines L7 to L9 without the delete.

## Example

Take $C = 6$. Insert $a$ with key 4, $b$ with key 2, $c$ with key 5, $d$ with key 2 and $e$ with key 6.

| step | buckets 0 to 6 (non-empty only) | cur | result |
|---|---|---|---|
| after the inserts | 2: b, d; 4: a; 5: c; 6: e | 2 | |
| EXTRACT-MIN | 2: d; 4: a; 5: c; 6: e | 2 | (b, 2) |
| EXTRACT-MIN | 4: a; 5: c; 6: e | 2 | (d, 2) |
| DECREASE-KEY(c, 3) | 3: c; 4: a; 6: e | 2 | |
| EXTRACT-MIN | 4: a; 6: e | 3 | (c, 3), after one skipped bucket |
| INSERT(f, 1) | 1: f; 4: a; 6: e | 1 | line L3 moves the cursor back |
| DELETE(a) | 1: f; 6: e | 1 | |
| EXTRACT-MIN | 6: e | 1 | (f, 1) |
| EXTRACT-MIN | empty | 6 | (e, 6), after five skipped buckets |

The items with equal keys $b$ and $d$ come out in the order of insertion.

## Correctness

The structure keeps two invariants: (B) each item $x$ in the queue is in exactly one bucket, the bucket $B[\mathit{key}[x]]$; and (C) every non-empty bucket has index at least $\mathit{cur}$. INSERT and DELETE keep (B) directly, and line L3 keeps (C). Line L8 moves the cursor only past empty buckets, so (C) holds, and when it stops, $B[\mathit{cur}]$ is non-empty and every item has key at least $\mathit{cur}$. So EXTRACT-MIN returns an item of the smallest key. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| INSERT, DELETE, DECREASE-KEY | $O(1)$ worst case |
| EXTRACT-MIN, FIND-MIN | $O(1 + s)$, for $s$ skipped empty buckets |
| create | $\Theta(C)$ |

**A whole run.** The cursor goes up only in line L8, by one per skipped bucket, and goes down only in line L3. Let $D$ be the sum of the drops of line L3. The cursor starts at $C + 1$ and never passes $C + 1$, so the total number of skipped buckets is at most $C + 1 + D$. A sequence of $n$ operations then costs $O(n + C + D)$.

**Monotone use.** If each key inserted is at least the last key extracted, then line L3 only fires before the first extract, so $D \le C + 1$ and a run costs $O(n + C)$. In Dijkstra's algorithm on a graph with $V$ vertices, $E$ edges and integer weights in $0 \ldots W$, all keys in the queue lie in a window of width $W$ above the cursor, and the largest key is at most $(V - 1)W$, so the plain bucket queue gives $O(E + VW)$ time, the bound of Dial's algorithm.

**Worst case.** Without monotone use, a single extract can skip $\Theta(C)$ buckets, and alternating inserts at 0 and $C$ with extracts can make each extract cost $\Theta(C)$.

## Variants

- **Circular buckets.** In the monotone setting with all keys in $\mathit{cur} \ldots \mathit{cur} + W$, an array of $W + 1$ buckets used modulo $W + 1$ is enough, so the space is $O(W)$ and not $O(VW)$. This is the form Dial used.
- **Max bucket queue.** Move the cursor down instead of up. The [greedy coloring](/greedy-coloring/) by degeneracy and the [k-core](/k-core/) peeling use buckets of degrees, where the keys are at most $n - 1$ and each key drops by one at a time.
- **Radix heap.** A [radix heap](/radix-heap/) uses $O(\log C)$ buckets of growing width and redistributes the items of a wide bucket when it is reached, which gives $O(\log C)$ amortized time per extract in the monotone setting.
- **Two-level buckets.** Buckets of width $\sqrt{C}$ with a second level inside the first non-empty one reduce the scan to $O(\sqrt{C})$ per extract.
- **Calendar queue.** A [calendar queue](/calendar-queue/) applies the same idea to real-valued event times, with a bucket width that adapts to the data.
- **Timing wheel.** A [timing wheel](/timing-wheel/) is a circular bucket queue for timers, keyed by the tick at which each timer fires.

## When to use it

Use a bucket queue when the keys are integers in a range $C$ that is not much larger than the number of operations, and especially when the use is monotone: shortest paths with small integer weights, breadth-first search with 0 or 1 weights, the peeling of a graph by degree, scheduling with a few priority levels, and the greedy choice in some approximation algorithms for [set cover](/set-cover/). For large or real keys, a [binary heap](/binary-heap/) is simpler and needs no range.

## Pitfalls

- **A large range.** The array costs $\Theta(C)$ space and time to create, and a scan can cost $\Theta(C)$. With $C$ much larger than $n$, use a heap or a radix heap.
- **Forgetting the cursor drop.** Without line L3, an insert below the cursor is never found, and the queue returns a wrong minimum.
- **Deleting by search.** Removing an item by searching its bucket costs the size of the bucket. Keep a handle to the list node, or a map from the item, so that delete is $O(1)$.
- **Circular buckets outside the window.** The circular variant is correct only while all keys lie within $W$ of the cursor. A key further away lands in the bucket of a smaller key.
- **Negative keys.** Shift the keys by the smallest possible value first.

## Implementations

The Python class `BucketQueue(c)` keeps the buckets as insertion-ordered dictionaries and the map `key` as a dictionary. `insert`, `delete`, `decrease_key`, `find_min` and `extract_min` follow the pseudocode, and `check_invariant` checks (B) and (C). Items must be hashable; keys are integers in $0 \ldots c$.

## History

Dial published the bucket form of Dijkstra's algorithm in 1969 as Algorithm 360 in the Communications of the ACM, with circular buckets for integer arc lengths. The structure is folklore in many other places: a counting sort keeps the same array of lists, and the linear-time degeneracy order of Matula and Beck (1983) uses buckets of degrees. Ahuja, Mehlhorn, Orlin and Tarjan (1990) refined it into the radix heap.

## References
