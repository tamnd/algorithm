---
tag: RWNCD5
kind: technique
slug: rehashing
name: Rehashing
aliases:
- dynamic resizing
- table resizing
area: data-structures/hashing
level: intro
summary: Grow the table and reinsert all keys when the load factor exceeds a threshold.
prereqs: [hash-table, load-factor, amortized-cost, potential-method]
see_also: [array-doubling, separate-chaining, open-addressing, lazy-deletion, linear-hashing, extendible-hashing, cuckoo-hashing, consistent-hashing]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 16.4, Dynamic tables (expansion and contraction, with the potential method); Chapter 11, Hash tables
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4, Hash Tables (array resizing in SeparateChainingHashST and LinearProbingHashST)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4, Hashing (deletion and the rebuilding of an open-addressing table)
  - url: https://github.com/redis/redis/blob/unstable/src/dict.c
    title: Redis source, src/dict.c
    locator: the functions dictRehash and _dictRehashStep (incremental rehashing with two tables)
---

Rehashing is the operation that builds a new array for a [hash table](/hash-table/), usually of a different size, and inserts every stored key again with a hash function for the new size. A table rehashes when its [load factor](/load-factor/) $\alpha = n/m$ passes an upper bound, so that searches stay fast, and often also when $\alpha$ falls below a lower bound, so that the space stays $\Theta(n)$. If the size changes by a constant factor each time, one rehash costs $\Theta(n + m)$ but the total cost over any sequence of operations is $O(1)$ [amortized](/amortized-cost/) per operation. The same rebuild also removes the tombstones of [lazy deletion](/lazy-deletion/) and replaces a hash function that behaves badly.

## In plain words

A hash table is fast only while it is not too full. When too many keys are in too few slots, the lists get long, or the searches must look at many slots. So the table makes a new, bigger array, often twice as big, and moves every key into it. A key may go to a different slot in the new array, because the slot depends on the size of the array.

Moving all the keys is slow, but it happens rarely. After a doubling, the table can take as many new keys as it had in total before it must grow again. So the moves, shared out over all the insertions, cost only a small fixed amount per insertion.

## When it applies

- A hash table holds a number of keys that is not known in advance, or that changes a lot over time.
- The cost of an operation depends on the load factor, as it does for [separate chaining](/separate-chaining/) and for [open addressing](/open-addressing/).
- Open addressing must keep $\alpha$ strictly below 1, or an insertion fails.
- Deletions in open addressing have left many tombstones, and unsuccessful searches have become slow.
- The current hash function gives long chains or a failed insertion, as in [cuckoo hashing](/cuckoo-hashing/), and a new random function is likely to be better.

## The template

The table has $n$ keys in $m$ slots, an upper bound $\beta$ on the load (the holes are $\beta$, the growth factor and the lower bound), and a minimum size $m_0$ with $\beta m_0 \ge 1$.

```pseudo id=main
INSERT-WITH-RESIZE(T, k)
L1  insert k into T with the hash function for size m      ▷ hole: chaining or open addressing
L2  n ← n + 1
L3  if n > β · m then REHASH(T, 2m)                          ▷ hole: the growth factor

DELETE-WITH-RESIZE(T, k)
L4  delete k from T, n ← n − 1
L5  if m > m₀ and n < β · m / 4 then REHASH(T, m / 2)        ▷ hole: the lower bound

REHASH(T, m′)
L6  A ← a new empty table of m′ slots
L7  choose the hash function for size m′                    ▷ hole: same family, new size or new seed
L8  for each slot of T, for each key x stored there do
L9      insert x into A                                      ▷ no search for an equal key is needed
L10 T ← A, m ← m′
```

**The trigger (L3, L5).** The table grows when $\alpha$ passes $\beta$ and shrinks when $\alpha$ falls below $\beta/4$. The gap between the two bounds is essential: after any rehash, $\alpha$ is close to $\beta/2$, so many operations must happen before the next rehash.

**The new hash function (L7).** For the [division method](/division-method/), the function is $k \bmod m'$. For a [multiplicative](/multiplicative-hashing/) function with $m' = 2^{p}$, the function keeps $p$ bits instead of $p - 1$. A table can also draw a fresh random function at this point, which is how [universal hashing](/universal-hashing/) and cuckoo hashing recover from a bad choice.

**The reinsertion (L8, L9).** All keys are distinct, so line L9 inserts without a search. With open addressing, line L8 skips empty slots and tombstones, so the new table has no tombstones.

### Example

Take chaining with $h(k) = k \bmod m$, insertion at the head of a chain, $\beta = 1$ and $m = 4$. Insert $5, 9, 2, 14, 7$.

| step | $n$ | $m$ | chains (slot: keys, head first) |
|---|---|---|---|
| insert 5, 9, 2, 14 | 4 | 4 | 1: 9, 5; 2: 14, 2 |
| insert 7 | 5 | 4 | 1: 9, 5; 2: 14, 2; 3: 7 |
| rehash, $n > 1 \cdot 4$ | 5 | 8 | 1: 9; 2: 2; 5: 5; 6: 14; 7: 7 |

After the rehash, 9 and 5 are no longer in the same chain, because $9 \bmod 8 = 1$ and $5 \bmod 8 = 5$. The longest chain went from 2 keys to 1.

With $\beta = 3/4$ and $m = 8$ at the start, 1 000 insertions cause 8 rehashes, at $n = 7, 13, 25, 49, 97, 193, 385$ and $769$. Together they reinsert $1\,538$ keys, fewer than 2 per insertion. At the end $m = 2\,048$ and $\alpha \approx 0.49$.

### Cost

**Claim.** Assume $\beta m_0 \ge 1$. Count one unit for an insertion, deletion or search at load at most $\beta$, and one unit for each slot and each key that a rehash handles, so that REHASH from $m$ to $m'$ slots costs at most $m + m' + n$ units. Then any sequence of $N$ operations, from an empty table of $m_0$ slots, costs at most $(3 + 8/\beta) N + (\beta + 4) m_0$ units.

*Proof.* Use the [potential method](/potential-method/) with $\Phi = c\,|2n - \beta m|$, where $c = 1 + 4/\beta$. We have $\Phi \ge 0$ always, and $\Phi = c \beta m_0$ at the start.

An operation without a rehash changes $n$ by at most 1 and leaves $m$ the same. So $\Phi$ changes by at most $2c$, and the amortized cost is at most $1 + 2c = 3 + 8/\beta$.

A growth happens when line L2 makes $n > \beta m$. Before the insertion, $n - 1 \le \beta m$, because each insertion that makes $n > \beta m$ grows the table at once. So $\beta m < n \le \beta m + 1$. The potential before the rehash is $c(2n - \beta m)$ and after it is $c(2n - 2\beta m)$, both with a positive argument. The drop is exactly $c \beta m = \beta m + 4m$. The rehash costs at most $m + 2m + n \le 3m + \beta m + 1 \le \beta m + 4m$, since $m \ge 1$. So the rehash is paid by the drop.

A shrink happens when line L4 makes $n < \beta m / 4$. Then $2n < \beta m/2$, so the potential before is $c(\beta m - 2n)$ and after, with $m/2$ slots, is $c(\beta m/2 - 2n)$. The drop is exactly $c \beta m / 2 = \beta m / 2 + 2m$. The rehash costs at most $m + m/2 + n < 3m/2 + \beta m/4$, which is less than the drop.

After each growth, $n \le \beta m + 1 \le 2\beta m$ because $\beta m \ge 1$, so the new table has load at most $\beta$. After each shrink, the load is below $\beta/2$. So each operation runs at load at most $\beta$, as the unit costs assume. The total actual cost is the total amortized cost plus $\Phi_{\text{start}} - \Phi_{\text{end}} \le c \beta m_0 = (\beta + 4) m_0$. $\square$

Under the [uniform hashing assumption](/uniform-hashing-assumption/) or with a [universal](/universal-hashing/) function, one unit stands for $O(1)$ expected time when $\beta$ is a constant, so the operations take $O(1)$ expected amortized time. The space is $O(n + m_0)$: after each operation, either $m = m_0$ or $n \ge \beta m/4 - 1$, so $m \le 4(n+1)/\beta$. CLRS Section 16.4 gives the same argument for an array that doubles when full and halves at one quarter full, the case of [array doubling](/array-doubling/).

## Classic examples

- **[Array doubling](/array-doubling/).** A growable array is the same technique without hashing: copy to an array of twice the size when full. The amortized proof is the same.
- **[Separate chaining](/separate-chaining/) in libraries.** Java `HashMap` doubles when $\alpha$ passes 0.75 and never shrinks. Sedgewick and Wayne's `SeparateChainingHashST` doubles at $n \ge 10m$ and halves at $n \le 2m$.
- **[Open addressing](/open-addressing/) with [linear probing](/linear-probing/).** Sedgewick and Wayne's `LinearProbingHashST` doubles at $n \ge m/2$ and halves at $n \le m/8$. A [Swiss table](/swiss-table/) can rebuild at the same size when tombstones, not keys, fill the table.
- **[Lazy deletion](/lazy-deletion/).** Rehashing at the same size removes all tombstones. A table counts keys plus tombstones in the trigger for this.
- **[Cuckoo hashing](/cuckoo-hashing/).** When an insertion runs into a cycle of evictions, the table draws new hash functions and rehashes all keys, at the same size or larger.
- **[Dynamic perfect hashing](/dynamic-perfect-hashing/).** Each second-level table rehashes with a new random function when it gets a collision or gets too full, and the whole structure rebuilds after a fixed number of updates.

## Variations

- **Incremental rehashing.** Keep the old and the new table at the same time, and move a few chains from the old to the new table in each later operation. A search looks in both tables. Redis does this, with an index of the next chain to move. No single operation then pays for a full rehash, so the worst case of an operation is small, not only the amortized cost.
- **[Linear hashing](/linear-hashing/).** Split one bucket at a time, in a fixed order, so that the table grows by one bucket per step without a full rehash.
- **[Extendible hashing](/extendible-hashing/).** Keep a directory of $2^d$ pointers to buckets. A full bucket splits by one more bit of the hash value, and only the directory doubles.
- **Other growth factors.** Any factor $\gamma > 1$ gives $O(1)$ amortized cost, with a constant that grows as $\gamma$ tends to 1. A larger factor wastes more memory just after a growth.
- **Prime sizes.** A table that uses $k \bmod m$ with $m$ prime grows to the next prime from a fixed list near $2m$, instead of to $2m$ exactly.
- **[Consistent hashing](/consistent-hashing/).** In a distributed store, moving all keys when a server joins is too expensive. Consistent hashing moves only about $n/s$ of the keys when the number of servers changes from $s$ to $s + 1$.

## Pitfalls

- **Bounds that are too close.** If the table shrinks as soon as $\alpha < \beta/2$, a load near $\beta/2$ makes it rehash over and over. With $\beta = 1/2$ and $m = 16$, the 9th insertion grows the table to 32 slots, two deletions bring $n$ to 7 and shrink it to 16, and two insertions grow it again. Each four operations then cost two full rehashes. Keep the lower bound below half of the upper bound, as line L5 does with $\beta/4$.
- **Reusing the old slot numbers.** A key at slot $j$ in the old table is not at slot $j$ in the new one. Line L9 must compute the hash value again for the new size, or the search for the key fails.
- **Forgetting the tombstones.** In open addressing, a trigger that counts only live keys never fires on a table that is full of tombstones. Count keys plus tombstones for the trigger, and skip the tombstones in line L8.
- **Iterators and pointers.** A rehash in open addressing moves the keys, so a pointer to a stored item or an iterator over the table is no longer valid after an insertion. C++ `std::unordered_map` keeps pointers valid but not iterators, because its nodes do not move.
- **A stall in a latency-bound program.** One rehash of a table with millions of keys takes a long time. If a single slow operation is not acceptable, use incremental rehashing or [linear hashing](/linear-hashing/).
- **A table that is too small for β.** If $\beta m < 1$, one doubling may not bring the load below $\beta$. Start with $m_0 \ge 1/\beta$, as the claim above assumes.

## Exercises

1. Insert $3, 11, 19, 27, 6$ into a chained table with $h(k) = k \bmod m$, $m = 4$ and $\beta = 1$. Show the chains before and after the rehash. Which keys share a chain after it?
2. Repeat the cost claim for a growth factor $\gamma > 1$: grow to $\gamma m$ when $n > \beta m$, and shrink to $m/\gamma$ when $n < \beta m/\gamma^2$. Find a constant $c$ for the potential $c\,|\gamma n - \beta m|$ that makes the amortized cost $O(1)$.
3. A table only grows and never shrinks. Show that after $N$ insertions and $N$ deletions its space can be $\Theta(N)$ while it holds no keys. Is this a problem for a cache that runs for months?
4. In incremental rehashing from $m$ to $2m$ slots, each later operation moves $\lceil 1/\beta \rceil$ chains of the old table. Show that the move ends before the new table reaches its growth bound $n > 2\beta m$.

## References
