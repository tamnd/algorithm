---
tag: QQ610A
kind: data-structure
slug: indexed-priority-queue
name: Indexed priority queue
aliases:
- index min priority queue
- indexed heap
area: data-structures/heaps
level: core
summary: Heap keyed by item indices, allowing O(log n) decrease-key and delete of a given item.
implements: [priority-queue]
model: comparison-model
prereqs: [binary-heap, heap-property, sift-up, sift-down, decrease-key]
see_also: [binary-heap, decrease-key, heap-delete, heap-increase-key, dijkstra, prim, handle, d-ary-heap]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority queues), the index priority queue API and the IndexMinPQ implementation
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.5 (Priority queues), the discussion of handles that map application objects to heap elements
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox
    locator: Section 6.2 (Addressable priority queues)
---

An indexed priority queue is a [binary heap](/binary-heap/) of item numbers $0 \ldots m - 1$, ordered by a key stored for each number, together with an inverse array that gives the position of each number in the heap. With the inverse array, the caller can name an item by its number and change its key or remove it in $O(\log n)$ time, without a search. The structure has three arrays: the heap $\mathit{pq}$, the position map $\mathit{qp}$ with $\mathit{pq}[\mathit{qp}[i]] = i$, and the keys $\mathit{key}$. Each swap in the heap updates two entries of $\mathit{qp}$. It is the usual priority queue of [Dijkstra's algorithm](/dijkstra/) and [Prim's algorithm](/prim/) on a graph with vertices $0 \ldots V - 1$, where [decrease-key](/decrease-key/) is the frequent operation. Sedgewick and Wayne call it IndexMinPQ.

## In plain words

A heap keeps its items in an array, and it moves them around all the time. If you want to make one item more urgent, you first need to know where it is now, and looking for it would take a long time.

So give each item a number, and keep a second array, a table of positions: entry $i$ says where the item $i$ is in the heap. Each time the heap swaps two items, it also fixes their two entries in the table. Now to change the item $i$, you read its place from the table, change its key, and move it up or down as in any heap.

## The abstract type

An indexed priority queue implements an addressable min-[priority queue](/priority-queue/) whose handles are the integers $0 \ldots m - 1$, fixed when the queue is created:

- INSERT$(i, k)$: add the item $i$ with key $k$; $i$ must not be in the queue.
- CONTAINS$(i)$ and KEY$(i)$.
- MIN-INDEX and EXTRACT-MIN, which removes and returns an item of smallest key.
- DECREASE-KEY$(i, k)$ with $k \le \mathit{key}[i]$, and CHANGE-KEY$(i, k)$ for any $k$.
- DELETE$(i)$.

Keys come from a [total order](/total-order/).

## Representation

For a capacity $m$ and $n$ items in the queue:

- $\mathit{pq}[0 \ldots n - 1]$ is a binary min-heap of item numbers: for $1 \le j < n$, $\mathit{key}[\mathit{pq}[\lfloor (j - 1)/2 \rfloor]] \le \mathit{key}[\mathit{pq}[j]]$.
- $\mathit{qp}[0 \ldots m - 1]$: $\mathit{qp}[i]$ is the position of $i$ in $\mathit{pq}$, or $-1$ if $i$ is not in the queue.
- $\mathit{key}[0 \ldots m - 1]$: the key of each item in the queue.

The link between the first two is the invariant $\mathit{pq}[\mathit{qp}[i]] = i$ for each $i$ in the queue, and $\mathit{qp}[\mathit{pq}[j]] = j$ for each $0 \le j < n$. The space is $\Theta(m)$. When the handles are not small integers, a hash table from items to positions plays the role of $\mathit{qp}$.

## Operations

```pseudo id=main
INSERT(i, k)
L1  if qp[i] ≠ −1 then error "already in the queue"
L2  qp[i] ← n; pq[n] ← i; key[i] ← k; n ← n + 1
L3  SWIM(qp[i])

EXTRACT-MIN()
L4  if n = 0 then error "underflow"
L5  i ← pq[0]; EXCH(0, n − 1); n ← n − 1
L6  SINK(0); qp[i] ← −1
L7  return (i, key[i])

DECREASE-KEY(i, k)
L8  if k > key[i] then error "new key is larger"
L9  key[i] ← k; SWIM(qp[i])

DELETE(i)
L10 j ← qp[i]; EXCH(j, n − 1); n ← n − 1
L11 if j < n then SWIM(j); SINK(j)
L12 qp[i] ← −1

EXCH(a, b)
L13 swap pq[a] and pq[b]; qp[pq[a]] ← a; qp[pq[b]] ← b

SWIM(j)
L14 while j > 0 and key[pq[j]] < key[pq[⌊(j − 1)/2⌋]] do
L15     EXCH(j, ⌊(j − 1)/2⌋); j ← ⌊(j − 1)/2⌋

SINK(j)
L16 while 2j + 1 < n do
L17     c ← 2j + 1; if c + 1 < n and key[pq[c + 1]] < key[pq[c]] then c ← c + 1
L18     if not key[pq[c]] < key[pq[j]] then return
L19     EXCH(j, c); j ← c
```

SWIM is [sift-up](/sift-up/) and SINK is [sift-down](/sift-down/), on positions in $\mathit{pq}$ and with keys read through $\mathit{key}$. The only change from a plain heap is that every move goes through EXCH, which keeps the position map in step. CHANGE-KEY sets the key and calls SWIM if it went down and SINK if it went up. DELETE is [heap delete](/heap-delete/): the moved item may need to go either way, so line L11 calls both, and at most one of them moves it.

## Example

Take $m = 6$ and insert the items $0, 1, 2, 3, 4$ with keys 50, 30, 40, 10, 60. Positions are 0-based.

| step | $\mathit{pq}$ | $\mathit{qp}[0 \ldots 5]$ |
|---|---|---|
| the five inserts | [3, 1, 2, 0, 4] | [3, 1, 2, 0, 4, −1] |
| DECREASE-KEY(4, 5): from position 4, swap with item 1, then with item 3 | [4, 3, 2, 0, 1] | [3, 4, 2, 1, 0, −1] |
| DELETE(3): item 3 at position 1 swaps with the last, item 1; key 30 stays | [4, 1, 2, 0] | [3, 1, 2, −1, 0, −1] |
| EXTRACT-MIN returns (4, 5); item 0 goes to the root and sinks below item 1 | [1, 0, 2] | [1, 0, 2, −1, −1, −1] |

In the inserts, item 3 with key 10 enters at position 3 and swims past item 0 (key 50) and item 1 (key 30) to the root. In the delete, item 1 with key 30 moves to position 1; its parent, item 4, has key 5, and its child, item 0, has key 50, so it stays.

## Correctness

The structure keeps two invariants: (H) $\mathit{pq}[0 \ldots n - 1]$ is a min-heap with respect to $\mathit{key}$, and (P) $\mathit{qp}$ is the inverse of $\mathit{pq}$ on the items in the queue, and $-1$ elsewhere. EXCH keeps (P), since it swaps two entries of $\mathit{pq}$ and writes the new positions of both. Since every change to $\mathit{pq}$ is an EXCH, an append or a removal of the last cell, (P) holds after each operation, and the heap part (H) follows from the sift-up and sift-down lemmas as in a plain binary heap. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| CONTAINS, KEY, MIN-INDEX | $O(1)$ |
| INSERT, EXTRACT-MIN, DECREASE-KEY, CHANGE-KEY, DELETE | $O(\log n)$ worst case |
| create | $\Theta(m)$ |

Each operation does one SWIM or SINK, or both in DELETE, and each of these moves one level per iteration, so at most $\lfloor \lg n \rfloor$ iterations with $O(1)$ work each. EXCH costs $O(1)$, a constant factor more than a plain swap. The space is $\Theta(m)$ for the three arrays.

**Dijkstra.** On a graph with $V$ vertices and $E$ edges, Dijkstra's algorithm does $V$ inserts, $V$ extracts and at most $E$ decrease-keys, so it runs in $O((V + E) \log V)$ time with this queue. A [Fibonacci heap](/fibonacci-heap/) lowers this to $O(E + V \log V)$.

## Variants

- **Max version.** Reverse each comparison.
- **[d-ary heap](/d-ary-heap/).** The same position map works for any array heap. A larger $d$ makes DECREASE-KEY cheaper, which suits graphs with many edges.
- **Hash-map positions.** For items that are not small integers, keep the positions in a hash table. The bounds become expected bounds.
- **Handles in the heap.** In place of a position map, each heap cell holds a pointer to a record, and the record stores its current position. This is the handle method of CLRS.
- **Lazy deletion.** Without a position map, push a new entry on each decrease and skip stale entries when they reach the root, see [lazy deletion](/lazy-deletion/). This uses $O(E)$ space in Dijkstra's algorithm, against $O(V)$.

## When to use it

Use it when items are known by a small integer name and their keys change while they wait: vertices in Dijkstra's and Prim's algorithms, events in a simulation that can be cancelled or moved, and jobs whose priority is updated. If keys only ever leave the queue at the top, a plain [binary heap](/binary-heap/) is simpler.

## Pitfalls

- **Swaps that skip the map.** A single swap that does not go through EXCH leaves $\mathit{qp}$ wrong, and later operations then change the wrong item. Write every move through one function.
- **Delete with one direction.** The item moved from the last cell may need to go up as well as down; see [heap delete](/heap-delete/).
- **Delete of the last cell.** If $j = n - 1$, the cell is gone after line L10, and line L11 must skip the repair.
- **Index out of range.** Indices must lie in $0 \ldots m - 1$; the arrays do not grow.
- **Clearing the slot.** After EXTRACT-MIN or DELETE, set $\mathit{qp}[i] = -1$, else CONTAINS still says yes and a later INSERT of $i$ fails.

## Implementations

The Python class `IndexedMinPQ(m)` keeps `pq` as a growing list and `qp` and `key` as lists of length $m$. `insert`, `extract_min`, `decrease_key`, `change_key`, `delete`, `contains`, `key_of` and `min_index` follow the pseudocode, and `check_invariant` checks (H) and (P). Keys need only the operation "<".

## History

The position map is as old as the use of heaps in graph algorithms: Johnson (1975) analysed $d$-heaps with an update operation for shortest paths and spanning trees, which needs the position of each vertex in the heap. The name "index priority queue" and the API with the arrays `pq`, `qp` and `keys` are those of Sedgewick's textbooks.

## References
