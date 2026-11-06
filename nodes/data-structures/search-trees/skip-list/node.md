---
tag: XYVYKG
kind: data-structure
slug: skip-list
name: Skip list
aliases:
- skiplist
area: data-structures/search-trees
level: core
summary: A randomized ordered dictionary made of layered linked lists, where higher layers skip over elements, giving expected logarithmic search, insertion and deletion.
implements: [ordered-set, ordered-symbol-table, dictionary]
model: comparison-model
complexity:
  vars: {n: the number of keys, p: "the promotion probability, a constant in (0, 1)"}
  time: {expected: Θ(log n), worst: Θ(n)}
  space: {expected: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [linked-list, randomized-algorithm, geometric-distribution, ordered-set]
see_also: [lock-free-skip-list, random-binary-search-tree, treap, red-black-tree, finger-search-tree, binary-search, las-vegas-algorithm, zip-tree]
sources:
  - paper: doi:10.1145/78973.78977
    title: William Pugh, Skip lists, a probabilistic alternative to balanced trees, Communications of the ACM 33(6), 1990
    locator: pages 668 to 676, the algorithms for search, insert and delete, and the analysis of the expected search cost
---

A skip list is an ordered [linked list](/linked-list/) with extra levels of "express" lists on top of it: each node is in level 1, and each node that is in level $i$ is also in level $i + 1$ with probability $p$, independently, for a fixed $p$ such as $1/2$. A search starts in the top level, moves right while the next key is smaller, and drops one level when it would overshoot. William Pugh introduced it in 1990 as a simpler alternative to balanced trees. Search, insert and delete take $O(\log n)$ expected time and the structure uses $O(n)$ expected space, for each input, because the randomness is in the levels and not in the input.

## In plain words

Picture a subway line with local trains that stop at every station, and an express line above it that stops only at some stations, and a super express above that which stops at even fewer. To reach a station, ride the fastest line as far as you can without passing your stop, then change to a slower line, and so on, until the local line takes you to the door.

In a skip list, each key is a station. Whether a key also gets an express stop is decided by coin flips. With a fair coin, about half the keys are on the second line, a quarter on the third, and so on. So each line has about half the stops of the line below, and a trip uses only a few stops on each line.

## The abstract type

A skip list implements an [ordered set](/ordered-set/), or an [ordered symbol table](/ordered-symbol-table/) when each node also stores a value: search, insert, delete, minimum (the first node of level 1, in $O(1)$ time), floor, ceiling, and iteration in order in $O(n)$ time. With a width on each link, it also gives rank and select in $O(\log n)$ expected time.

## Representation

There is a header node with $M$ forward pointers, where $M$ is a cap on the number of levels, such as 32. Each node $x$ has a key, a value, and a level $\ell(x) \ge 1$ with forward pointers $x.forward[1], \ldots, x.forward[\ell(x)]$. The skip list stores the number of levels in use, $S.level$.

**Invariant.**

- **(S1) Sorted base.** Following $forward[1]$ from the header visits each node once, in strictly increasing key order, and ends at NIL.
- **(S2) Levels are sublists.** For each $i \ge 1$, following $forward[i]$ from the header visits exactly the nodes with $\ell(x) \ge i$, in increasing key order.
- **(S3) Level count.** $S.level$ is the largest level of a node (1 if the list is empty), and $S.header.forward[i] = $ NIL for $i > S.level$.

The levels are drawn when a node is inserted: $\Pr[\ell(x) \ge i] = p^{i-1}$, a [geometric distribution](/geometric-distribution/), capped at $M$. They are never changed later, so the shape is a function of the random levels and the set of keys alone, not of the order of the operations.

## Operations

```pseudo id=main
SEARCH(S, k)
L1  x ← S.header
L2  for i ← S.level downto 1 do
L3      while x.forward[i] ≠ NIL and x.forward[i].key < k do x ← x.forward[i]
        update[i] ← x                          ▷ the last node of level i with key < k
L4  x ← x.forward[1]
L5  if x ≠ NIL and x.key = k then return x.value else return NIL

INSERT(S, k, v)
L6  run lines L1 to L3 to fill update[1 .. S.level]
L7  x ← update[1].forward[1]; if x ≠ NIL and x.key = k then x.value ← v; return
L8  lvl ← RANDOM-LEVEL()                       ▷ 1, then +1 while a coin with Pr[heads] = p shows heads, at most M
L9  if lvl > S.level then for i ← S.level + 1 to lvl do update[i] ← S.header; S.level ← lvl
L10 z ← a new node (k, v) with lvl forward pointers
L11 for i ← 1 to lvl do
L12     z.forward[i] ← update[i].forward[i]
L13     update[i].forward[i] ← z

DELETE(S, k)
L14 run lines L1 to L3 to fill update[1 .. S.level]
L15 x ← update[1].forward[1]; if x = NIL or x.key ≠ k then return false
L16 for i ← 1 to ℓ(x) do
L17     update[i].forward[i] ← x.forward[i]
L18 while S.level > 1 and S.header.forward[S.level] = NIL do S.level ← S.level − 1
```

**Search.** At each level, line L3 moves right while the next key is smaller than $k$, and the loop of line L2 then drops one level. At level 1 the node after $x$ is the first node with key $\ge k$, that is the ceiling of $k$, and line L5 tests it.

**Insert.** The array $update$ holds, for each level, the node after which $k$ belongs. The new node gets a random level, and lines L11 to L13 splice it into each of its lists, as in a linked-list insert. Each new level above $S.level$ starts at the header (line L9).

**Delete.** Lines L16 and L17 unlink $x$ from each list it is in; by (S2), $update[i]$ is its predecessor in level $i$. Line L18 drops empty top levels.

**Floor and ceiling.** After lines L1 to L3, $update[1]$ is the last node with key $< k$ and its successor is the ceiling. The floor is $k$ if $k$ is present, else $update[1]$ (or NIL if it is the header).

## Example

Take ten keys with these levels: 3 (1), 6 (4), 7 (1), 9 (2), 12 (1), 17 (2), 19 (1), 21 (3), 25 (1), 26 (1). The lists are:

```
level 4:  H → 6 ───────────────────────────────────────→ NIL
level 3:  H → 6 ──────────────────────────→ 21 ────────→ NIL
level 2:  H → 6 → 9 ─────────→ 17 ────────→ 21 ────────→ NIL
level 1:  H → 3 → 6 → 7 → 9 → 12 → 17 → 19 → 21 → 25 → 26 → NIL
```

**Search for 19.**

| level | moves | stops at | next key |
|---|---|---|---|
| 4 | H to 6 | 6 | NIL |
| 3 | none | 6 | 21, not $< 19$ |
| 2 | 6 to 9, 9 to 17 | 17 | 21, not $< 19$ |
| 1 | none | 17 | 19, not $< 19$ |

Line L4 moves to 19, and line L5 finds it. The search makes 3 moves to the right and 4 moves down, and it never looks at 3, 7 or 12. Each level has about half the nodes of the level below: here 10, 4, 2 and 1.

**Insert 20 with level 2.** The search for 20 leaves $update[1] = 19$ and $update[2] = 17$. Lines L11 to L13 splice 20 in after 19 in level 1 and after 17 in level 2, so level 2 becomes $6 \to 9 \to 17 \to 20 \to 21$. No other node changes.

## Correctness

Each operation keeps (S1) to (S3): an insert puts the new node, in each of its levels, right after the last node with a smaller key, so each level stays sorted and holds exactly the nodes of high enough level; a delete removes the node from exactly the levels it is in. For the search, the loop keeps this invariant: *when the loop of line L2 is at level $i$, $x$ is the header or a node of level $\ge i$ with $x.key < k$, and no node of level $\ge i$ has a key strictly between $x.key$ and $k$.* At level 1, (S2) covers all nodes, so $x.forward[1]$ is the first key $\ge k$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | expected time | worst case |
|---|---|---|
| search, floor, ceiling | $O(\log n)$ | $O(n + M)$ |
| insert, delete | $O(\log n)$ | $O(n + M)$ |
| minimum | $O(1)$ | $O(1)$ |
| iterate in order | $\Theta(n)$ | $\Theta(n)$ |
| space | $n/(1 - p)$ pointers plus the header | $nM$ pointers |

The expected time is over the random levels, for each fixed sequence of operations. Following Pugh, run the search path backwards from the end: at each node the path came either from above (the node is taller) or from the left. Each node is taller with probability $p$, independently of what the path has seen, so climbing $k$ levels takes $k/p$ steps in expectation. With $L = \lceil \log_{1/p} n \rceil$ levels, the expected number of steps is at most $(L - 1)/p + 2/(p(1 - p))$, which is about $2 \lg n + 8$ for $p = 1/2$. The full proof is in [the complexity proof](proofs/complexity.md).

The choice of $p$ trades time for space: $p = 1/2$ gives $2$ pointers per node on average, and $p = 1/4$ gives $4/3$ pointers per node and a search cost that is about the same, which is why Pugh recommends $p = 1/4$.

## Variants

- **Indexable skip list.** Store with each forward pointer the number of level-1 nodes it skips (its width). Then rank and select take $O(\log n)$ expected time, as in an [order statistic tree](/order-statistic-tree/).
- **Concurrent skip lists.** Inserts and deletes change only $O(1)$ pointers per level, and no rebalancing moves other nodes, so locks are local. The [lock-free skip list](/lock-free-skip-list/) uses compare-and-swap; Java's `ConcurrentSkipListMap` is one such design.
- **Deterministic skip lists.** Require between 1 and 2 nodes of level $i$ between consecutive nodes of level $i + 1$; this is a 1-2-3 tree in disguise and gives worst-case $O(\log n)$.
- **Finger search.** Starting from a known node, the search can climb and then go down, in $O(\log d)$ expected time for a target $d$ positions away; see [finger search trees](/finger-search-tree/).
- **Zip trees.** A [zip tree](/zip-tree/) is a binary search tree with the shape of a skip list, with geometric ranks in place of levels.

## When to use it

Use a skip list for an ordered map when simple code matters more than worst-case bounds, or when many threads update the map, since the local updates make concurrent versions much simpler than concurrent balanced trees. Redis uses skip lists for its sorted sets, and LevelDB and RocksDB use them for the in-memory table. For a single thread and the best constant factors, a [red-black tree](/red-black-tree/) or a B-tree uses less memory and has better cache behaviour.

## Pitfalls

- **A biased or shared generator.** The bound needs independent levels with $\Pr[\text{next level}] = p$. A generator whose output an adversary can predict, or a fixed seed with adversarial keys, can give a skip list of linear search cost. A poor generator whose low bits are not random gives too many or too few tall nodes.
- **No cap on the level.** Without $M$, a run of heads gives a node with a huge pointer array. With $M = 32$ and $p = 1/2$, the structure is fine for $n$ up to about $2^{32}$; for more keys, raise $M$.
- **Starting at level $M$.** Searching from level $M$ instead of $S.level$ costs $M$ extra steps on a small list. Keep $S.level$ and lower it after deletes (line L18).
- **Forgetting the new levels.** If line L9 does not set $update[i]$ to the header for the new top levels, the new node is not linked in those levels.
- **Equal keys.** Line L7 updates the value of an existing key. Without it, a second insert adds a second node, and a later delete removes only one.
- **Using the expected bound as a worst-case bound.** One operation can be slow with small probability. For hard real-time limits use a balanced tree.

## Implementations

The Python class follows the main block, with a seeded generator so that runs can be repeated, and adds floor, ceiling, iteration and a check of (S1) to (S3).

## History

Pugh (1990) introduced skip lists, with the algorithms for search, insert and delete, the analysis of the expected search cost, and timing tests against balanced trees. He presented them as a randomized alternative to balanced trees that is easier to code.

## References
