---
tag: XP6DXP
kind: data-structure
slug: hash-ring
name: Hash ring
aliases:
- consistent hash ring
- hash circle
area: systems/load-balancing-and-hashing
level: core
summary: "A sorted set of server points on a circle of hash values. A key goes to the next point clockwise, found by binary search in O(log N) time; inserting or removing a point changes one arc only."
prereqs: [consistent-hashing, binary-search, balanced-binary-search-tree]
see_also: [consistent-hashing, virtual-nodes, chord, red-black-tree, rendezvous-hashing, maglev-hashing, jump-consistent-hash, multi-probe-consistent-hashing]
sources:
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, STOC 1997
    locator: Section 4.2 (the construction with points of buckets and items on the unit interval) and the remark on its implementation with a balanced binary search tree, O(log C) time per item
  - paper: doi:10.1145/383059.383071
    title: Ion Stoica, Robert Morris, David Karger, M. Frans Kaashoek and Hari Balakrishnan, Chord, a scalable peer-to-peer lookup service for Internet applications, SIGCOMM 2001
    locator: Section 4.2 (the identifier circle modulo 2^m and the successor of a key)
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, third edition
    locator: Chapter 12, Section 12.2 (successor in a binary search tree) and Chapter 13 (red-black trees, O(log n) insert and delete)
---

A hash ring is the data structure behind [consistent hashing](/consistent-hashing/). It holds a set of points on a circle of hash values, $\{0, \ldots, R - 1\}$ with $R$ usually $2^{32}$ or $2^{64}$, and each point has an owner, a server. Its main query is the *successor*: given a position $x$, return the first point at or after $x$ going clockwise, wrapping from the end of the circle to the start. A key is stored on the owner of the successor of its hash. The points are kept sorted, in an array or in a [balanced search tree](/balanced-binary-search-tree/), so a query is a [binary search](/binary-search/) in $O(\log N)$ time for $N$ points. Each point owns the arc from the point before it up to itself, and inserting or removing a point changes only one neighboring arc, which is why few keys move when a server joins or leaves.

## In plain words

Picture a round table with numbered seats. Some seats hold a person, and each person has a name tag. To find who serves seat number 37, walk around the table from seat 37 in the direction of the numbers and stop at the first seat with a person. When you pass the last seat, you go on at seat 0.

Each person serves the empty seats just before them. If a new person sits down, they take over part of one neighbor's seats and nothing else changes. If a person leaves, the next person around the table takes over their seats.

## The abstract type

A hash ring stores a set $P$ of distinct positions in $\{0, \ldots, R-1\}$, each with an owner. It supports:

- **successor(x).** The point $p \in P$ with the least clockwise distance $(p - x) \bmod R$, with its owner. Undefined if $P$ is empty.
- **insert(p, s).** Add the point $p$ with owner $s$. An error if $p$ is already in $P$.
- **remove(p).** Remove the point $p$ and return its owner.
- **arc(p).** The positions that $p$ serves: the half-open circular interval $(q, p]$, where $q$ is the point before $p$.

Consistent hashing builds on these: a lookup of a key is successor(h(key)), a server joins by inserting its [virtual nodes](/virtual-nodes/), and the share of a server is the total length of the arcs of its points.

## Representation

The points are kept in increasing order of position, in two parallel arrays $pos[0 .. N-1]$ and $owner[0 .. N-1]$, with the invariant $pos[0] < pos[1] < \cdots < pos[N-1]$. A balanced binary search tree keyed by position, such as a [red-black tree](/red-black-tree/), is the other common form: its "ceiling" query (least key at least $x$) is the successor, and inserts and removes cost $O(\log N)$. The positions come from a hash function: $h(\text{server}, r)$ for the $r$-th point of a server. The size of the ring $R$ only has to be large enough that two points rarely collide.

## Operations

```pseudo id=main
RING-SUCCESSOR(pos, owner, x)
L1  i ← least index with pos[i] ≥ x, or N if there is none   ▷ binary search
L2  if i = N then i ← 0                                       ▷ wrap around
L3  return (pos[i], owner[i])
RING-INSERT(pos, owner, p, s)
L4  i ← least index with pos[i] ≥ p, or N
L5  if i < N and pos[i] = p then error "position taken"
L6  shift pos[i .. N − 1] and owner[i .. N − 1] one place right; pos[i] ← p; owner[i] ← s
RING-REMOVE(pos, owner, p)
L7  i ← least index with pos[i] ≥ p; if i = N or pos[i] ≠ p then error "no point"
L8  shift pos[i + 1 .. N − 1] and owner[i + 1 .. N − 1] one place left; return the old owner[i]
RING-ARC(pos, i)                                              ▷ the arc of pos[i]
L9  return (pos[i − 1], pos[i]]                                ▷ pos[−1] means pos[N − 1]
```

The arc has $(pos[i] - pos[i-1]) \bmod R$ positions; if $N = 1$ the single point owns all $R$ positions. With a balanced tree, lines L1 and L4 are a ceiling search, line L6 is a tree insert, and line L8 is a tree delete.

## Example

A ring with $R = 100$. Servers A, B and C have points at 12, 47 and 80.

| point | owner | arc | length |
| --- | --- | --- | --- |
| 12 | A | $(80, 12]$, that is 81 to 99 and 0 to 12 | 32 |
| 47 | B | $(12, 47]$ | 35 |
| 80 | C | $(47, 80]$ | 33 |

The lengths add up to 100. Queries: successor(5) is 12 (A), successor(30) is 47 (B), successor(47) is 47 itself (B), and successor(90) finds no point at or after 90, so line L2 wraps to index 0 and returns 12 (A).

**Insert 40 for server D.** Line L4 finds index 1 (the point 47), and line L6 shifts 47 and 80 right. The array is now 12, 40, 47, 80. The arc of 47 shrinks from $(12, 47]$ to $(40, 47]$, length 7, and the new point gets $(12, 40]$, length 28. The arcs of 12 and 80 do not change. Every position in $(12, 40]$ moved from B to D, and nothing else moved.

**Remove 80.** The arc $(47, 80]$ joins the arc of the next point clockwise, 12, which now owns $(47, 12]$, length 65. Only positions that C owned change owner.

## Correctness

The array stays strictly increasing, since an insert puts the new point between its neighbors and a remove deletes one entry (Lemma 1 of the proof). On a strictly increasing array the least index with $pos[i] \ge x$ has the least clockwise distance from $x$, and if there is none, $pos[0]$ has it (Lemma 2). The arc of each point is the interval from the point before it, and the arcs partition the ring (Lemma 3). An insert of $p$ splits the arc of its successor into two and a remove merges the arc of $p$ into its successor, so no other arc changes (Lemma 4). The tests check all operations against a linear scan of the ring on random sequences of inserts, removes and queries.

## Complexity

| operation | sorted array | balanced search tree |
| --- | --- | --- |
| successor | $O(\log N)$ | $O(\log N)$ |
| insert | $O(N)$, for the shift | $O(\log N)$ |
| remove | $O(N)$, for the shift | $O(\log N)$ |
| arc | $O(\log N)$ | $O(\log N)$ |
| build from $N$ points | $O(N\log N)$ by sorting | $O(N\log N)$ |
| space | $N$ positions and $N$ owners | $O(N)$ nodes |

With $n$ servers and $v$ points each, $N = nv$. The array form is faster in practice for lookups, because it is compact in memory, and joins and leaves are rare compared with lookups. The shift of $N$ entries for each of the $v$ points of a joining server costs $O(nv^2)$, or $O(nv\log(nv))$ if all the points of the server are merged in one pass.

## Variants

- **Lookup table.** Precompute the owner of each of $2^b$ equal slices of the ring, and keep a list of points for the slices that hold a point. A lookup is then $O(1)$ in expectation. Karger et al. gave this trick in 1997, with about $C\log C$ slices for $C\log C$ points, each slice with its own small search tree. [Maglev hashing](/maglev-hashing/) goes further and fills a table of fixed size directly.
- **Successor lists for replicas.** To store $r$ copies of a key, take the owners of the first $r$ points clockwise that belong to distinct servers. This is the preference list of Dynamo-style stores.
- **Distributed ring.** In [Chord](/chord/) no node holds the whole ring. Each node knows its successor and $O(\log n)$ fingers, and a lookup takes $O(\log n)$ messages.
- **Unit interval.** Karger et al. described the points on $[0, 1]$ with the closest point as the owner; the circular successor rule is the common form today.
- **Several probes per key.** [Multi-probe consistent hashing](/multi-probe-consistent-hashing/) keeps one point per server and does several successor queries per key.

## When to use it

Use a hash ring when keys must map to a changing set of servers and every client must compute the same answer, which is the setting of [consistent hashing](/consistent-hashing/). The sorted array is the right choice for a small or slowly changing ring and many lookups; use a balanced tree when points change often. If servers are numbered $0, \ldots, n-1$ and only change at the end, [jump consistent hash](/jump-consistent-hash/) needs no ring at all. If $n$ is small, [rendezvous hashing](/rendezvous-hashing/) is simpler, with $O(n)$ time per lookup and no structure to keep.

## Pitfalls

- **Forgetting the wrap.** A key past the last point belongs to the first point. Without line L2 the lookup reads past the end of the array.
- **Successor or predecessor.** Some libraries give a key to the first point at or after it, others to the first point strictly after it, or to the point before it. All are correct, but clients that mix them disagree on keys near the points.
- **Collisions.** Two points at the same position make the owner depend on the insert order. Reject them, or break ties by owner name, and use 64-bit positions.
- **Too few points.** With one point per server the arcs differ by a factor of about $\ln n$ ([consistent hashing load bound](/consistent-hashing-max-load-bound/)); use [virtual nodes](/virtual-nodes/).
- **Copying the ring on every change.** Systems that publish the ring to clients often rebuild it from scratch on each join; this is $O(N\log N)$ and fine when changes are rare, but a busy ring needs incremental updates.

## Implementations

The Python file stores the ring in two sorted lists and uses `bisect_left` for the successor search. It has insert, remove, successor, the arc of a point and the share of each owner. The tests run the example above and compare 3000 random operations against a linear scan.

## History

Karger, Lehman, Leighton, Panigrahy, Levine and Lewin described the points of buckets and items on the unit interval in 1997 and noted that a balanced binary search tree finds the bucket of an item in $O(\log C)$ time, with $O(\log^2 C)$ time to add or remove a bucket of $\log C$ points. Chord (Stoica et al., 2001) used an identifier circle of size $2^m$ and the successor of each key, and spread the ring over the nodes themselves. Client libraries for memcached in the 2000s, such as ketama, kept the whole ring as a sorted array with many points per server, and this is the common form today.

## References
