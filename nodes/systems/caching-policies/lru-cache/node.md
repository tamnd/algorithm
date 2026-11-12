---
tag: DKPAX9
kind: data-structure
slug: lru-cache
name: LRU cache
aliases:
- LRU cache with hash map and doubly linked list
- hash map with doubly linked list cache
- LRU cache data structure
area: systems/caching-policies
level: intro
summary: A hash map from key to node plus a doubly linked list in recency order. Get and put run in O(1) time under the LRU rule.
implements: [dictionary]
model: word-ram
complexity:
  vars: {n: the number of operations, c: the capacity in entries}
  time: {expected: O(1), worst: O(c)}
  space: {extra: Θ(c)}
prereqs: [lru, hash-table, doubly-linked-list]
see_also: [lru, sentinel-node, clock, lfu, two-q, move-to-front-heuristic, cache]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 10, Section 10.4.4 (the two implementations of LRU, with counters and with a stack kept as a doubly linked list)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.2 (doubly linked lists with a sentinel) and Chapter 11 (hash tables)
  - url: https://docs.python.org/3/library/functools.html#functools.lru_cache
    title: Python standard library documentation, functools.lru_cache
    locator: the decorator lru_cache and its maxsize parameter
  - url: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/LinkedHashMap.html
    title: Java SE API documentation, java.util.LinkedHashMap
    locator: the access-order constructor and the method removeEldestEntry
---

An LRU cache is a map with a fixed capacity $c$ that, when it is full and a new key arrives, evicts the entry used least recently. It pairs a [hash table](/hash-table/) from each key to a node with a [doubly linked list](/doubly-linked-list/) of the nodes in recency order, so that get and put each take $O(1)$ expected time. It is the standard way to run the [LRU](/lru/) policy in software. The LRU page is about which entry the policy evicts and how many misses that gives; this page is about the structure that finds and moves the entries.

## In plain words

Think of a stack of papers on a desk. Each time you use a paper, you pull it out and put it on top. So the paper at the bottom is the one you have not touched for the longest time. When the desk is full and a new paper arrives, you throw away the bottom one.

Pulling a paper out of the middle of a pile is slow if you must search for it. So you also keep an index card for each paper that says exactly where it is. With the index, you find any paper at once. With the pile, you know at once which paper is the oldest. Each paper is tied to the papers above and below it, so you can take it out and close the gap in one step.

## The abstract type

The cache stores pairs (key, value) with distinct keys, at most $c$ of them, where $c \ge 1$. It keeps a recency order on the stored keys.

- get(key): if key is stored, return its value and make key the most recently used. Otherwise return "absent" and change nothing.
- put(key, value): if key is stored, set its value and make it the most recently used. Otherwise, if $c$ keys are stored, remove the least recently used pair; then store (key, value) as the most recently used.
- delete(key): remove key and its value if present.

A request sequence of gets and puts is served exactly as the [LRU](/lru/) policy serves it: a get that returns "absent" is a miss, and the caller usually loads the value and calls put.

## Representation

- A hash table $M$ from each stored key to its node.
- A circular doubly linked list of nodes with one [sentinel node](/sentinel-node/) $S$. Each node holds key, value, prev and next. $S.next$ is the most recently used node and $S.prev$ the least recently used one. The empty cache has $S.next = S.prev = S$.

The node holds its own key so that, at an eviction, the code can delete the key of $S.prev$ from $M$ without a search.

## Operations

```pseudo id=main
UNLINK(x):     x.prev.next ← x.next;  x.next.prev ← x.prev
PUSH-FRONT(x): x.prev ← S;  x.next ← S.next;  S.next.prev ← x;  S.next ← x

GET(key)
L1  x ← M.lookup(key)
L2  if x = nil then return absent
L3  UNLINK(x)
L4  PUSH-FRONT(x)
L5  return x.value

PUT(key, v)
L6  x ← M.lookup(key)
L7  if x ≠ nil then
L8      x.value ← v
L9      UNLINK(x); PUSH-FRONT(x); return
L10 if |M| = c then
L11     y ← S.prev                      ▷ the least recently used node
L12     UNLINK(y)
L13     M.delete(y.key)
L14 x ← a new node (key, v)
L15 PUSH-FRONT(x)
L16 M.insert(key, x)
```

DELETE(key) looks up the node, unlinks it and deletes the key from $M$. With the sentinel, UNLINK and PUSH-FRONT have no special case for the first, the last or the only node.

## Example

Capacity $c = 3$. The list is shown from the most to the least recently used.

| operation | result | list after |
| --- | --- | --- |
| put(1, x) | | 1 |
| put(2, y) | | 2 1 |
| put(3, z) | | 3 2 1 |
| get(1) | x | 1 3 2 |
| put(4, w) | evicts (2, y) | 4 1 3 |
| get(2) | absent | 4 1 3 |
| get(3) | z | 3 4 1 |
| put(1, v) | updates 1 | 1 3 4 |
| put(5, u) | evicts (4, w) | 5 1 3 |

The get of 1 saves key 1 from the eviction at put(4, w), which takes 2 instead. A get of a missing key changes nothing. A put of a stored key moves it to the front and never evicts.

## Correctness

The invariant after each operation is: (a) the list is a consistent circle through $S$ ($x.next.prev = x$ and $x.prev.next = x$ for each node); (b) the keys of $M$ are exactly the keys of the list nodes, each once, and $M[\mathrm{key}]$ is the node of that key; (c) at most $c$ nodes are in the list; (d) the list order from $S.next$ to $S.prev$ is the recency order of the abstract type. UNLINK keeps (a) and removes one node; PUSH-FRONT keeps (a) and makes the node first. A get or an update moves one node to the front, which is the new recency order. An insertion into a full cache first removes the last node, the least recently used one, and its key from $M$, so the size stays at most $c$. The full proof is below.

## Complexity

- **get and put.** One hash lookup, at most one hash insertion and one hash deletion, and a constant number of pointer writes. So each operation takes $O(1)$ expected time with a hash table that has $O(1)$ expected cost, and $O(1)$ amortized expected time if the table resizes. The list part is $O(1)$ in the worst case. The worst case of one operation is $O(c)$, when all stored keys fall in one bucket of the hash table.
- **Space.** $\Theta(c)$ words: a node of four fields and one hash entry for each stored key, plus the sentinel.
- **A sequence of $n$ operations.** $O(n)$ expected time.

A plain array kept in recency order needs $\Theta(c)$ time to move an entry to the front. A list without the map needs $\Theta(c)$ time to find an entry. A [binary heap](/binary-heap/) keyed by the last use time needs $O(\log c)$ time. The map and the list together remove both costs.

## Variants

- **Singly linked list.** Without the prev pointer, an unlink needs the predecessor. A map from key to the predecessor node works, but each move then updates two map entries. The doubly linked version is simpler.
- **Library versions.** Java's LinkedHashMap with access order and an override of removeEldestEntry is an LRU cache. Python's OrderedDict with move_to_end and popitem(last=False) is one too, and functools.lru_cache keeps a dict and a circular doubly linked list of the same kind.
- **Concurrent LRU caches.** A single list needs a lock on each get, because a hit writes to the list. Practical caches split the keys into shards with one list each, or buffer the recency updates and apply them in batches, or use [CLOCK](/clock/), where a hit only sets a bit.
- **Other policies with the same parts.** [SLRU](/slru/) and [2Q](/two-q/) use two or three such lists, and the [O(1) LFU](/lfu/) structure uses one list for each frequency.

## When to use it

Use an LRU cache to memoize a function, to keep the results of database or network calls, or as the page table of a small buffer pool, when the recency of use is a good guide to the next use. Use a library version when one exists. Write your own when you need control over the eviction, for example a callback on each evicted pair. For many threads, prefer a sharded or a CLOCK-based cache.

## Pitfalls

- **A get that does not move the entry.** Then the structure is a FIFO cache, not an LRU cache.
- **Forgetting to delete the evicted key from the map.** The map then grows without bound and points to dead nodes.
- **Not storing the key in the node.** At an eviction, the code then cannot find the map entry of the last node without a scan.
- **Moving the entry on a put of a stored key, but not updating its value.** Or the reverse. Both steps are needed.
- **Evicting before checking for the key.** A put of a stored key into a full cache must not evict anything.
- **Capacity zero.** With $c = 0$, PUT would evict from an empty list. Reject $c < 1$, or make put a no-op.

## Implementations

## History

The textbook of Silberschatz, Galvin and Gagne gives the two classic ways to run LRU for pages: a time stamp in each page table entry, and a stack of page numbers kept as a doubly linked list with head and tail pointers, where a reference moves the page to the top. The hash map is what turns the stack into a cache for arbitrary keys. Standard libraries ship the structure: Java's LinkedHashMap supports access order and an eviction hook, and Python's functools.lru_cache uses a dictionary together with a circular doubly linked list.

## References
