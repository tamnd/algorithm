---
tag: B9C3HD
kind: data-structure
slug: open-list
name: Open list
aliases:
- OPEN
area: games-and-search/heuristic-search
level: intro
summary: The priority queue of A* and other best-first searches. It holds the generated states that wait for expansion, ordered by f, and supports insert, insert-or-lower and remove-min.
implements: [priority-queue]
model: word-ram
complexity:
  vars: {k: the number of states in OPEN}
  time: {push: O(log k), pop: O(log k), contains: O(1)}
  space: {extra: O(k)}
prereqs: [priority-queue, binary-heap, hash-table, search-frontier]
see_also: [a-star-search, best-first-search, duplicate-detection, indexed-priority-queue, decrease-key, bucket-queue, partial-expansion-a-star, fringe-search]
sources:
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2) (1968)
    locator: pp. 100 to 107 (the statement of A* with nodes marked open and closed, and the reopening of closed nodes)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 2 (the lists Open and Closed of A*) and Chapter 3 (priority queues and dictionaries for the search, including bucket structures)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.3.2 (search data structures, the frontier as a priority queue and the reached table)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 2 (the lists OPEN and CLOSED of best-first search)
---

The open list, called OPEN, is the [priority queue](/priority-queue/) of [A*](/a-star-search/) and the other [best-first searches](/best-first-search/). It holds the states that the search has generated and not yet expanded, each with its cost $g$ so far and its evaluation $f$, and it gives back the state of least $f$. It is the concrete form of the [search frontier](/search-frontier/) of a best-first search. It differs from a plain priority queue in three ways: each state has at most one entry, an insert of a state that is already present lowers its entry only when the new $g$ is smaller, and ties in $f$ follow a fixed rule, usually toward larger $g$. The usual representation is a [binary heap](/binary-heap/) with a [hash table](/hash-table/) from states to their entries, so each operation costs $O(\log k)$ for $k$ states in OPEN.

## In plain words

OPEN is the list of places that a search knows about but has not visited yet. Each place has a score, and the search always takes out the place with the best score next. If the search finds a cheaper way to a place that is already on the list, the place gets the better score and stays on the list once. When two places have the same score, a fixed rule chooses, so the search does the same thing every time it runs.

## The abstract type

The content of OPEN is a finite map from states to pairs $(g, f)$, and it supports these operations.

- **PUSH$(n, g, f)$.** If $n$ is not in OPEN, add $n \mapsto (g, f)$. If $n$ is in OPEN with $g' > g$, replace its pair by $(g, f)$. If $n$ is in OPEN with $g' \le g$, change nothing. Report whether the content changed.
- **POP-MIN.** Remove and return the state $n$ with its pair that is least in the order of $f$, then of larger $g$, then of the earlier push. Report *empty* when there is no state.
- **CONTAINS$(n)$** and **G$(n)$.** Tell whether $n$ is in OPEN, and give its $g$.
- **REMOVE$(n)$.** Delete $n$ from OPEN, if it is there.

In A* the value $f$ is $g + h(n)$, so a smaller $g$ always gives a smaller $f$, and PUSH is the insert-or-[decrease-key](/decrease-key/) of line L11 of A*. The closed list CLOSED is a separate set of expanded states. OPEN and CLOSED together, with the table of $g$ values, do the [duplicate detection](/duplicate-detection/) of graph search.

## Representation

The code keeps two parts.

- A binary heap $H$ of entries $(f, -g, t, n)$, compared as tuples. The stamp $t$ comes from a counter that grows by one at each push, so equal $f$ and $g$ come out first in, first out.
- A hash table $\mathit{best}$ from each state in OPEN to the triple $(g, f, t)$ of its live entry.

An entry of $H$ whose stamp is not the one in $\mathit{best}$ is *stale*. A lowered state gets a new entry and leaves the old one in the heap, which is lazy deletion. POP-MIN skips stale entries when they come to the top. When more than half of the heap is stale, the heap is rebuilt from the live entries, so it never holds more than $2k + s$ entries for a small constant $s$.

An [indexed priority queue](/indexed-priority-queue/) is the other common choice. It stores the heap position of each state and moves the entry up in place on a decrease, so the heap has exactly $k$ entries. It needs more code, and lazy deletion is usually as fast.

## Operations

```pseudo id=main
PUSH(OPEN, n, g, f)
L1  if n ∈ best and best[n].g ≤ g then return false
L2  best[n] ← (g, f, t) with a new stamp t
L3  add the entry (f, −g, t, n) to H
L4  COMPACT(OPEN); return true

POP-MIN(OPEN)
L5  while H ≠ ∅ do
L6      (f, −g, t, n) ← remove the least entry of H
L7      if n ∈ best and best[n].t = t then
L8          remove n from best; COMPACT(OPEN); return (n, g, f)
L9  return empty

CONTAINS(OPEN, n)
L10 return n ∈ best

REMOVE(OPEN, n)
L11 remove n from best, if it is there; COMPACT(OPEN)

COMPACT(OPEN)
L12 if |H| > 2 |best| + s then
L13     H ← a heap built from the entries (f, −g, t, n) of best
```

## Example

These are the operations on OPEN in the example of the page [A* search](/a-star-search/), with the Manhattan heuristic. A cell $X\ g/f$ is a live entry, and the stamps grow from left to right in the order of the pushes.

| operation | result | live entries after it | heap size |
| --- | --- | --- | --- |
| PUSH A 2/6, B 3/7, F 1/8 | three inserts | A 2/6, B 3/7, F 1/8 | 3 |
| POP-MIN | A 2/6 | B 3/7, F 1/8 | 2 |
| PUSH C 6/8, D 5/7 | two inserts | B 3/7, D 5/7, C 6/8, F 1/8 | 4 |
| POP-MIN | D 5/7, the tie with B goes to larger $g$ | B 3/7, C 6/8, F 1/8 | 3 |
| PUSH G 8/8 | insert | B 3/7, C 6/8, F 1/8, G 8/8 | 4 |
| POP-MIN | B 3/7 | C 6/8, F 1/8, G 8/8 | 3 |
| PUSH C 5/7 | lower C, old entry stale | C 5/7, F 1/8, G 8/8 | 4 |
| PUSH C 5/7 | false, not cheaper | C 5/7, F 1/8, G 8/8 | 4 |
| POP-MIN | C 5/7 | F 1/8, G 8/8 | 3 |
| PUSH G 7/7 | lower G | G 7/7, F 1/8 | 4 |
| POP-MIN | G 7/7 | F 1/8 | 3 |

Here A* stops, because G is the goal. If the operations went on, the next POP-MIN would skip the stale entries C 6/8 and G 8/8 when they reach the top, and return F 1/8. At the tie of F 1/8 and C 6/8, the rule toward larger $g$ would put C first, but that entry of C is stale.

## Correctness

The [proof](proofs/correctness.md) uses the invariant that $H$ is a heap, that each state in $\mathit{best}$ has its live entry in $H$, and that $|H| \le 2|\mathit{best}| + s$. POP-MIN returns the least live entry, because every entry that comes out of the heap before it is smaller, so it is stale and not part of the content. PUSH replaces the pair only when the new $g$ is smaller, and the old entry then becomes stale because its stamp is no longer the one in $\mathit{best}$.

## Complexity

The costs are in the [word RAM](/word-ram/), with $O(1)$ expected time for each operation on the hash table. For $k$ states in OPEN:

| operation | time |
| --- | --- |
| PUSH | $O(\log k)$ amortized |
| POP-MIN | $O(\log k)$ amortized |
| CONTAINS, G | $O(1)$ |
| REMOVE | $O(1)$ amortized, plus the later skip of the stale entry |

Each stale entry is removed once, at line L6 or by a rebuild, and the proof charges that removal to the operation that made the entry stale. A rebuild takes $O(|H|)$ time, but it runs only when more than half of the heap is stale. The space is $O(k)$ entries. In A* with a consistent heuristic, OPEN sees at most $m + 1$ pushes for $m$ actions, so its total cost over a run is $O(m \log n)$ for $n$ states.

The heap order is the cost in practice. OPEN in a large search can hold millions of states, and the logarithmic factor and the cache misses of the heap then matter more than the work of generating states.

## Variants

- **Bucket OPEN.** When $f$ takes small integer values, as in unit-cost puzzles, a [bucket queue](/bucket-queue/) indexed by $f$, with a second level of buckets by $g$ for the tie rule, does each operation in $O(1)$ time. Edelkamp and Schroedl (Chapter 3) treat such structures. A [radix heap](/radix-heap/) works for larger integer keys when the removed keys never go down, which holds for a consistent heuristic.
- **Decrease-key in place.** An [indexed priority queue](/indexed-priority-queue/), or a [pairing heap](/pairing-heap/) or [Fibonacci heap](/fibonacci-heap/) with handles, lowers the entry without a stale copy.
- **No lowering at all.** Push every cheaper path as a new entry and check, when an entry comes out, whether it is still the cheapest for its state. This is what the A* code of this site does, with the table $g$ outside OPEN.
- **Partial expansion.** [Partial expansion A*](/partial-expansion-a-star/) puts the parent back in OPEN with a new $f$ instead of all its children, to keep OPEN small when the branching factor is large.
- **No priority queue.** [Fringe search](/fringe-search/) keeps OPEN as a list and scans it with an $f$ bound, as IDA* does, so it avoids the heap altogether.

## When to use it

Use an OPEN list with lazy deletion for A*, uniform-cost search and greedy best-first search on any graph whose states can be hashed. Use buckets when the values of $f$ are small integers. When the heuristic is not consistent, keep CLOSED separate and allow a state to be pushed again after it was expanded, because [reopening](/a-star-search/) needs it.

## Pitfalls

- **Many entries per state.** A heap without the table $\mathit{best}$, or without the check of line L7, returns the same state more than once and with a cost that is no longer the best.
- **Comparing states.** In a tuple $(f, g, n)$, a tie in $f$ and $g$ makes the heap compare the states themselves, which can fail or depend on their representation. Put a stamp before the state.
- **The tie rule changes the search.** Toward larger $g$ often expands fewer states, but in the example it took D before B. Toward smaller $g$, or last in first out, gives other counts. Each is correct, but compare two programs only with the same rule.
- **Checking membership in the heap.** A linear scan of the heap for CONTAINS costs $O(k)$ per call and makes the whole search quadratic. Use the table.
- **Lowering with a larger $g$.** PUSH must keep the old entry when the new $g$ is not smaller, or a worse path replaces a better one.

## Implementations

## History

The statement of A* by Hart, Nilsson and Raphael (1968) marks each node *open* or *closed*: the start is open, the open node of least $f$ is closed and expanded, and a closed node whose cost goes down is opened again. The names OPEN and CLOSED for the two lists come from there and from the books of Nilsson and of Pearl (1984, Chapter 2). The use of a binary heap with a hash table, and of lazy deletion, is standard engineering of priority queues, as in implementations of [Dijkstra's algorithm](/dijkstra/). Edelkamp and Schroedl give a full treatment of the data structures of OPEN and CLOSED for large searches.

## References
