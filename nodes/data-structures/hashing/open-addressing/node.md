---
tag: 5V7ZTB
kind: technique
slug: open-addressing
name: Open addressing
aliases:
- closed hashing
area: data-structures/hashing
level: intro
summary: All keys live in the table itself, and collisions are resolved by probing other slots.
prereqs: [hash-table, probe-sequence, load-factor]
see_also: [linear-probing, quadratic-probing, double-hashing, lazy-deletion, separate-chaining, uniform-hashing-assumption, yao-open-addressing-lower-bound, rehashing]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 11, Hash Tables, Section 11.4, Open addressing
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4, Hashing (the part on open addressing, Algorithms L and D, and the history at the end of the section)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4, Hash Tables, the part on linear probing
  - paper: doi:10.1147/rd.12.0130
    title: W. W. Peterson, Addressing for random-access storage, IBM Journal of Research and Development 1(2), 1957
    locator: pages 130 to 146
---

Open addressing is a way to resolve collisions in a [hash table](/hash-table/): every key is stored in the slot array itself, and a key whose home slot is taken goes to another slot, chosen by a fixed [probe sequence](/probe-sequence/) for that key. A search follows the same probe sequence and stops at the key or at an empty slot. The method needs no lists and no pointers, so it uses less memory than [separate chaining](/separate-chaining/) and reads memory in a cache-friendly way, but the [load factor](/load-factor/) must stay below 1 and deletion needs care. [Linear probing](/linear-probing/), [quadratic probing](/quadratic-probing/) and [double hashing](/double-hashing/) are the classic probe rules.

## In plain words

Think of a car park with numbered spaces and no overflow area. Each car has a favourite space, computed from its plate number. If that space is free, the car parks there. If not, the driver follows a fixed route through the other spaces, the same route each time for that car, and parks in the first free space on the route.

To find a car, you walk the same route from its favourite space. If you reach the car, you are done. If you reach an empty space first, the car is not in the park, because the car would have parked there.

This works while the park has free spaces. When it is almost full, the routes get long. A car that leaves needs care too: if its space just becomes empty, a search for a later car on the same route stops there too early.

## When it applies

- You need a [dictionary](/dictionary/) with expected constant-time insert, search and delete, and the keys can be hashed.
- The records are small (a key and a short value or a pointer), so moving them inside one array is cheap and the space of a pointer per record matters.
- Memory access cost matters. A probe sequence that stays in nearby slots, as in [linear probing](/linear-probing/), reads few cache lines.
- The number of keys is known, or the table can be resized by [rehashing](/rehashing/) when the load factor passes a threshold.

It fits less well when the records are large (store pointers instead), when deletions are frequent and the probe rule has no cheap deletion, or when a bad or adversarial hash function is possible: with a weak hash, long runs of full slots form much faster than long chains do.

## The template

The table is an array $T[0 \ldots m-1]$. Each slot holds a key, or the mark EMPTY, or the mark DELETED. The probe function $h(k, i)$, for $i = 0, 1, \ldots, m-1$, gives the $i$-th slot to try for key $k$. The table holds $n$ keys, and the load factor is $\alpha = n/m$.

```pseudo id=main
INSERT(T, k)                              ▷ assume k is not in T
L1  for i ← 0 to m − 1 do
L2      j ← h(k, i)                       ▷ hole: the probe rule
L3      if T[j] = EMPTY or T[j] = DELETED then
L4          T[j] ← k
L5          return j
L6  error "table full"                    ▷ hole: grow and rehash instead

SEARCH(T, k)
L7  for i ← 0 to m − 1 do
L8      j ← h(k, i)
L9      if T[j] = EMPTY then return NIL   ▷ k would have been placed here
L10     if T[j] = k then return j
L11 return NIL

DELETE(T, k)
L12 j ← SEARCH(T, k)
L13 if j ≠ NIL then T[j] ← DELETED        ▷ hole: the deletion policy
```

**The probe rule (line L2).** With an ordinary [hash function](/hash-function/) $h'$, and a second one $h_2$:

- linear probing: $h(k, i) = (h'(k) + i) \bmod m$;
- quadratic probing: $h(k, i) = (h'(k) + c_1 i + c_2 i^2) \bmod m$;
- double hashing: $h(k, i) = (h'(k) + i \cdot h_2(k)) \bmod m$.

For the loops of lines L1 and L7 to see every slot, the sequence $h(k, 0), \ldots, h(k, m-1)$ must be a permutation of $\{0, \ldots, m-1\}$ for each key $k$. Linear probing always gives a permutation. Double hashing gives one when $h_2(k)$ and $m$ have no common factor. Quadratic probing gives one only for special choices of $c_1$, $c_2$ and $m$.

**Why the search may stop at EMPTY (line L9).** Keys are inserted at the first free slot of their probe sequence, and a slot never goes back to EMPTY. So if a slot on the probe sequence of $k$ is EMPTY now, it was EMPTY when $k$ was inserted, and the insert of $k$ would have stopped there or earlier. Hence $k$ is not after that slot. This is the invariant of open addressing: each key $k$ sits at position $h(k, i)$, and the slots $h(k, 0), \ldots, h(k, i-1)$ are all non-EMPTY.

**The deletion policy (line L13).** Writing EMPTY into the slot would break this invariant for each key whose probe sequence passes through the slot. The safe general policy is a DELETED mark, a tombstone: search skips it, and insert may reuse it. This is [lazy deletion](/lazy-deletion/). For linear probing there is also a deletion that moves keys back and leaves no tombstone.

**Insert when the key may be present.** Line L3 may reuse a DELETED slot that comes before a live copy of $k$ further on. A real insert first runs SEARCH, or it remembers the first DELETED slot and keeps probing until EMPTY or $k$.

**The cost.** Each operation costs one hash evaluation plus one step per probe. Under the [uniform hashing assumption](/uniform-hashing-assumption/), where the probe sequence of each key is a uniformly random permutation, independent of the others, a search for an absent key with $n$ keys and no tombstones in the table makes at most $1/(1 - \alpha)$ probes in expectation. The first $i$ probes all hit keys with probability

$$\frac{n}{m} \cdot \frac{n-1}{m-1} \cdots \frac{n-i+1}{m-i+1} \le \alpha^i,$$

because $(n - t)/(m - t) \le n/m$ for $0 \le t < n \le m$. So the expected number of probes $X$ is $\sum_{i \ge 1} \Pr[X \ge i] \le \sum_{i \ge 0} \alpha^i = 1/(1-\alpha)$. A successful search for the key inserted $(t+1)$-th repeats the probes of its insert, which saw $t$ keys, so on average over the $n$ keys it costs at most

$$\frac{1}{n} \sum_{t=0}^{n-1} \frac{m}{m - t} \le \frac{1}{\alpha} \ln \frac{1}{1 - \alpha}.$$

The last step bounds the sum $\sum_{t=0}^{n-1} 1/(m-t)$ by $\int_{m-n}^{m} dx/x = \ln(m/(m-n))$. At $\alpha = 1/2$ these bounds are 2 and about 1.386; at $\alpha = 0.9$ they are 10 and about 2.558. Real probe rules are not uniform. Linear probing does worse at a high load, as the [analysis of linear probing](/linear-probing-analysis/) shows, and [Yao's lower bound](/yao-open-addressing-lower-bound/) says that, for a successful search, uniform hashing is close to the best possible among the schemes that put each key in the first free slot of its sequence and never move it. These expected bounds also assume that the hash values are random enough. In the worst case, one operation can probe all $m$ slots.

### A small example

Take $m = 11$, $h'(k) = k \bmod 11$ and $h_2(k) = 1 + (k \bmod 10)$. For $k = 36$, $h'(36) = 3$ and $h_2(36) = 7$. The first probes are:

| rule | probe sequence |
|---|---|
| linear | 3, 4, 5, 6, 7, 8, 9, 10, 0, 1, 2 |
| quadratic, $c_1 = 0$, $c_2 = 1$ | 3, 4, 7, 1, 8, 6, 6, 8, 1, 7, 4 |
| double hashing | 3, 10, 6, 2, 9, 5, 1, 8, 4, 0, 7 |

Linear probing and double hashing reach all 11 slots. The quadratic sequence $3 + i^2 \bmod 11$ reaches only 6 slots, because a prime $m$ has only $(m+1)/2$ distinct squares modulo $m$.

Now the deletion problem. Take $m = 7$, $h'(k) = k \bmod 7$, and linear probing. Insert 10, 17 and 24: all three hash to 3, so they go to slots 3, 4 and 5. Delete 17. If slot 4 becomes EMPTY, a search for 24 probes slot 3 (key 10), then slot 4 (EMPTY), and returns NIL, which is wrong. If slot 4 becomes DELETED, the search skips it and finds 24 at slot 5.

## Classic examples

- **[Linear probing](/linear-probing/).** The simplest rule: try the next slot. It has the best cache behaviour, but it suffers from [primary clustering](/primary-clustering/): runs of full slots grow and merge. Its expected search cost is about $\frac{1}{2}(1 + 1/(1-\alpha)^2)$ for an absent key.
- **[Quadratic probing](/quadratic-probing/).** Offsets grow as a quadratic, which breaks up the runs of linear probing. Keys with the same home slot still share one sequence, which is [secondary clustering](/secondary-clustering/).
- **[Double hashing](/double-hashing/).** The step size comes from a second hash function, so two keys with the same home slot usually have different sequences. Its behaviour is close to uniform hashing.
- **[Robin Hood hashing](/robin-hood-hashing/).** Linear probing where an insert may move a key that is closer to its home slot, so that the probe lengths are more even.
- **[Swiss table](/swiss-table/).** A practical open-addressing table that probes groups of 16 slots at a time with one byte of metadata per slot.
- **[Cuckoo hashing](/cuckoo-hashing/) and [hopscotch hashing](/hopscotch-hashing/).** Keys stay in the array, but an insert may move other keys, so that a search looks at only a constant number of slots.

## Variations

- **Deletion policy.** Tombstones ([lazy deletion](/lazy-deletion/)) work with every probe rule, but they make searches longer until the next rebuild. With linear probing, Knuth's Algorithm R (Section 6.4) closes the gap by moving later keys of the run back, and leaves no tombstone.
- **Reordering on insert.** Brent's variation, ordered hashing and Robin Hood hashing move keys that are already in the table during an insert, to make later searches shorter. Yao's lower bound does not apply to such schemes.
- **Resizing.** When $\alpha$ passes a threshold such as $1/2$ or $7/8$, allocate a larger table and reinsert all keys. Tombstones are dropped during the rebuild. See [rehashing](/rehashing/).
- **Bucketed slots.** Each slot of the array is a bucket of $b$ records, for example a disk block or a cache line, and a probe reads a whole bucket. This is the classic form for files on disk, and it is the idea of the group probing in the Swiss table.

## Pitfalls

- **Deletion by writing EMPTY.** This breaks the invariant, and later searches miss keys, as in the example above. Use a tombstone, or the backward-shift deletion of linear probing.
- **A probe sequence that misses slots.** Quadratic probing with $m$ not prime, or double hashing with $\gcd(h_2(k), m) > 1$, can loop over a few full slots while free slots exist. Then an insert fails, or loops forever if the loop has no bound. Choose $m$ prime, or $m$ a power of 2 with an odd step for double hashing, or triangular offsets $i(i+1)/2$ with $m$ a power of 2 for quadratic probing.
- **A full table.** With $n = m$, a search for an absent key never meets EMPTY. Bound the loop by $m$ probes, as in lines L1 and L7, and grow the table well before it is full.
- **Load factor too high.** Under uniform hashing, the expected cost grows as $1/(1-\alpha)$, and for linear probing as $1/(1-\alpha)^2$. Keep $\alpha$ at or below a fixed constant less than 1.
- **Counting tombstones as free.** If the resize test uses only the live keys, a table with many deletions can fill with tombstones, and every search for an absent key then probes the whole table. Count tombstones in the trigger for a rebuild.
- **Duplicate keys.** Inserting into the first DELETED slot without a search first can store a second copy of a key that is already further on.

## Exercises

1. Show that $h(k, i) = (h'(k) + i(i+1)/2) \bmod m$ is a permutation of $\{0, \ldots, m-1\}$ for each key when $m$ is a power of 2.
2. With $m = 7$, $h'(k) = k \bmod 7$ and linear probing, insert 3, 10, 5, 17 in this order, then delete 10 by a tombstone. Which slots does a search for 17 probe?
3. Prove that $(n - t)/(m - t) \le n/m$ for $0 \le t < n \le m$, the step used in the cost bound.
4. Give a sequence of inserts and deletes that leaves a table with $m$ slots, one live key and $m - 1$ tombstones. What does a search for an absent key cost?

## References
