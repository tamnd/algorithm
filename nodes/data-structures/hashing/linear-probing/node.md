---
tag: J1RWHQ
kind: algorithm
slug: linear-probing
name: Linear probing
aliases:
- linear open addressing
- linear probing hash table
area: data-structures/hashing
level: intro
summary: Open addressing that probes consecutive slots h(k), h(k)+1, and so on.
solves: [dictionary-problem]
model: word-ram
complexity:
  vars: {n: the number of keys, m: the number of slots, α: the load factor n/m}
  time: {expected: Θ(1), worst: Θ(m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1954
  people: [Gene Amdahl, Elaine M. McGraw, Arthur L. Samuel]
  note: Knuth reports that linear probing was used in an assembler for the IBM 701 in 1954, and that Amdahl had the idea.
prereqs: [open-addressing, hash-function, load-factor]
see_also: [linear-probing-analysis, lazy-deletion, primary-clustering, quadratic-probing, double-hashing, robin-hood-hashing, separate-chaining, k-wise-independent-hashing]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4, Algorithm L (open addressing with linear probing), Algorithm R (deletion with linear probing), the analysis of Algorithm L, and the history at the end of the section
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.4, Open addressing; Section 11.5, Practical considerations (linear probing and its deletion without tombstones)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4, Hash Tables, the part on linear probing (LinearProbingHashST)
  - paper: doi:10.1137/070702278
    title: Anna Pagh, Rasmus Pagh and Milan Ružić, Linear probing with constant independence, SIAM Journal on Computing 39(3), 2009
    locator: pages 1107 to 1120
  - paper: doi:10.1007/978-3-642-14165-2_60
    title: Mihai Pătraşcu and Mikkel Thorup, On the k-independence required by linear probing and minwise independence, ICALP 2010, LNCS 6198
    locator: pages 715 to 726
---

Linear probing is the simplest rule of [open addressing](/open-addressing/): a key whose home slot $h(k)$ is full goes to the next slot $h(k) + 1$, then $h(k) + 2$, and so on, around the end of the array. It solves the [dictionary problem](/dictionary-problem/) with all keys in one array of $m$ slots. With a good [hash function](/hash-function/) and a [load factor](/load-factor/) $\alpha = n/m$ below a constant less than 1, each operation takes $\Theta(1)$ expected time, and the scan of adjacent slots makes it one of the fastest hash tables in practice. Its weakness is [primary clustering](/primary-clustering/): full slots form long runs, so the cost grows as $1/(1-\alpha)^2$ when the table gets full.

## In plain words

Picture a row of numbered lockers, with the end of the row joined to the start. Each key has a home locker, computed from the key. To store a key, go to its home locker. If the locker is taken, try the next one, and the next, until you find a free one.

To look for a key, start at its home locker and walk to the right. If you find the key, you are done. If you reach a free locker first, the key is not stored, because it would have gone into that locker.

To remove a key, empty its locker, then look at the keys just after it. A key whose walk passed the freed locker moves back into it, and the locker it leaves is handled the same way. So the walk from each home to its key never crosses a free locker.

## The problem

Keep a set of distinct keys, each with a value, under insert, search and delete. This is the [dictionary problem](/dictionary-problem/). The table is an array $T[0 \ldots m-1]$. Each slot is EMPTY or holds one key with its value. A hash function $h$ maps each key to a home slot in $\{0, \ldots, m-1\}$. All index arithmetic is modulo $m$.

## The algorithm

The table keeps $n < m$, so that at least one slot is EMPTY. An insert of a new key needs $n + 1 < m$; a real table grows before that, at a fixed load factor such as $1/2$, by [rehashing](/rehashing/).

```pseudo id=main
INSERT(T, k)                              ▷ requires n + 1 < m if k is new
L1  j ← h(k)
L2  while T[j] ≠ EMPTY do
L3      if T[j] = k then return j         ▷ k is present: update its value
L4      j ← (j + 1) mod m
L5  T[j] ← k, n ← n + 1
L6  return j

SEARCH(T, k)
L7  j ← h(k)
L8  while T[j] ≠ EMPTY do
L9      if T[j] = k then return j
L10     j ← (j + 1) mod m
L11 return NIL

DELETE(T, k)                              ▷ backward shift, no tombstones
L12 i ← SEARCH(T, k)
L13 if i = NIL then return
L14 T[i] ← EMPTY, n ← n − 1               ▷ i is the hole
L15 j ← i
L16 loop
L17     j ← (j + 1) mod m
L18     if T[j] = EMPTY then return
L19     r ← h(T[j])                       ▷ the home slot of the key at j
L20     if r is cyclically in (i, j] then continue   ▷ the key at j can stay
L21     T[i] ← T[j], T[j] ← EMPTY, i ← j  ▷ move it into the hole
```

INSERT and SEARCH walk from the home slot to the right until they see the key or an EMPTY slot. The walk is correct because of one invariant: for each key at slot $p$, the slots from its home $h(k)$ up to $p - 1$ are all full. So a search for a stored key never meets an EMPTY slot before the key.

DELETE must keep this invariant without a tombstone. After line L14 the slot $i$ is a hole. The scan of lines L17 to L21 looks at each later key of the same run. A key at $j$ with home $r$ may stay if $r$ is in the cyclic range $(i, j]$, because then its walk from $r$ to $j$ does not pass the hole. Otherwise its walk passes the hole, so line L21 moves it back into the hole, and its old slot becomes the new hole. The scan ends at the first EMPTY slot. The test of line L20 is $0 < (r - i) \bmod m \le (j - i) \bmod m$. This is Knuth's Algorithm R.

## Example

Take $m = 16$ and, to keep the numbers readable, $h(k) = k \bmod 16$. Insert 18, 34, 50, 20, 31, 47, 15 in this order.

| step | home | slots probed | slot used | full slots after the step |
|---|---|---|---|---|
| insert 18 | 2 | 2 | 2 | 2 |
| insert 34 | 2 | 2, 3 | 3 | 2, 3 |
| insert 50 | 2 | 2, 3, 4 | 4 | 2 to 4 |
| insert 20 | 4 | 4, 5 | 5 | 2 to 5 |
| insert 31 | 15 | 15 | 15 | 2 to 5, 15 |
| insert 47 | 15 | 15, 0 | 0 | 0, 2 to 5, 15 |
| insert 15 | 15 | 15, 0, 1 | 1 | 15, 0 to 5 |

The last insert joins two runs into one run of 7 full slots, from slot 15 around to slot 5. Key 20 has home 4 but sits in slot 5, because the keys of home 2 took slot 4 first: this is primary clustering. A successful search costs $1, 2, 3, 2, 1, 2, 3$ probes for the seven keys, which is 2 on average. A search for an absent key with home $h$ costs one probe more than the number of full slots from $h$ to the next EMPTY slot; over the 16 homes this averages $44/16 = 2.75$.

Now DELETE(18). The hole is slot 2.

| $j$ | key at $j$ | home $r$ | $r$ in $(i, j]$? | action | hole $i$ after |
|---|---|---|---|---|---|
| 3 | 34 | 2 | no ($r = i$) | move 34 to slot 2 | 3 |
| 4 | 50 | 2 | no | move 50 to slot 3 | 4 |
| 5 | 20 | 4 | no ($r = i$) | move 20 to slot 4 | 5 |
| 6 | EMPTY | | | stop | |

Slots 2 to 4 now hold 34, 50, 20, and slot 5 is EMPTY. Then DELETE(31) makes slot 15 the hole. Key 47 (home 15) moves to slot 15, and key 15 (home 15) moves to slot 0. Key 34 at slot 2 has home 2, which is in $(1, 2]$, so it stays, and so do 50 and 20. The scan stops at the EMPTY slot 5.

## Correctness

Each operation keeps three facts: the keys are distinct, at least one slot is EMPTY, and

> **(P)** for each key $x$ at slot $p$, every slot on the cyclic path $h(x), h(x)+1, \ldots, p-1$ is full.

SEARCH returns the slot of $k$ when $k$ is stored, by (P), and returns NIL otherwise, because it stops only at $k$ or at an EMPTY slot, and an EMPTY slot exists. INSERT puts a new key in the first EMPTY slot after its home, so (P) holds for it, and filling an EMPTY slot cannot break (P) for another key. For DELETE, the loop of line L16 keeps this invariant: the hole $i$ is the only EMPTY slot of the run that the deleted key was in, and every key outside the unscanned part of the run satisfies (P). The full proof, with the termination of each loop, is below.

## Complexity

Each probe costs $O(1)$ on the [word RAM](/word-ram/), plus the cost of a key comparison. The worst case of each operation is $\Theta(m)$ probes: if all keys hash to one slot, the run has length $n$.

The expected cost depends on how random the hash values are. If the $n$ keys hash independently and uniformly, Knuth's analysis gives, for $\alpha = n/m$ fixed and $m \to \infty$,

$$C'_n \to \frac{1}{2}\left(1 + \frac{1}{(1-\alpha)^2}\right) \text{ for a search that fails,} \qquad C_n \to \frac{1}{2}\left(1 + \frac{1}{1-\alpha}\right) \text{ for one that succeeds}.$$

The derivation is on the page [analysis of linear probing](/linear-probing-analysis/). The numbers show the price of clustering, against the bound $1/(1-\alpha)$ of [uniform hashing](/uniform-hashing-assumption/):

| $\alpha$ | fail, linear | succeed, linear | fail, uniform hashing |
|---|---|---|---|
| 0.5 | 2.5 | 1.5 | 2 |
| 0.75 | 8.5 | 2.5 | 4 |
| 0.9 | 50.5 | 5.5 | 10 |

So $\alpha \le c$ for a constant $c < 1$ gives $\Theta(1)$ expected time per operation. A DELETE scans to the end of its run, which costs about as much as a failed search.

Full independence is more than a real hash function gives. Pagh, Pagh and Ružić proved that a 5-wise independent family is enough for $O(1)$ expected time per operation at a constant load below 1. They also showed that a pairwise independent family can give expected time $\Omega(\log n)$. Pătraşcu and Thorup showed that 5-wise independence is the least that works in general: there are 4-wise independent families with expected time $\Omega(\log n)$. [Tabulation hashing](/tabulation-hashing/) is a fast family that also gives $O(1)$ expected time.

The space is the array of $m$ slots, with no pointers. A table that grows and shrinks at fixed load factors keeps $m = \Theta(n)$.

## Properties

- **One array, no pointers.** Each slot holds a key and a value. This uses less memory than [separate chaining](/separate-chaining/) for small records.
- **Cache-friendly.** A probe sequence reads adjacent slots, so a search of a few probes often touches one or two cache lines.
- **Order-independent layout.** The set of full slots after a sequence of inserts does not depend on the order of the inserts, only on the multiset of home slots: a slot is full exactly when, for some length $\ell \ge 1$, at least $\ell$ keys have their home among the $\ell$ slots that end at it. The positions of single keys do depend on the order.
- **No tombstones needed.** After a backward-shift deletion, the set of full slots is the same as if the deleted key had never been inserted, by the rule in the previous item, which holds for every table that satisfies (P), so failed searches cost the same.
- **Sensitive to the hash function.** Hash values that fall in a few nearby slots, such as consecutive integers with $h(k) = k \bmod m$, build long runs fast.

## Variants and improvements

- **Tombstones.** Mark a deleted slot as DELETED instead of shifting keys back. This is [lazy deletion](/lazy-deletion/). It is simpler and works with every probe rule, but tombstones make searches longer until the next rebuild.
- **[Robin Hood hashing](/robin-hood-hashing/).** When an insert meets a key that is closer to its home than the new key is to its own, the two swap places. The variance of the probe lengths becomes small, and a failed search can stop early.
- **Ordered linear probing.** Keep the keys of each run in sorted order of key, so that a failed search stops at the first larger key. Amble and Knuth called this ordered hash tables.
- **Bucketed probing.** Probe whole cache lines or groups of slots. The [Swiss table](/swiss-table/) checks 16 control bytes at a time, and [hopscotch hashing](/hopscotch-hashing/) keeps each key within a small neighbourhood of its home.
- **Other probe rules.** [Quadratic probing](/quadratic-probing/) and [double hashing](/double-hashing/) avoid primary clustering, at the cost of jumps in memory.

## When to use it

Use linear probing for a fast in-memory map or set of small records, with a good hash function and a load factor up to about $1/2$ to $3/4$. It is the default choice of many fast hash tables. Prefer [separate chaining](/separate-chaining/) when records are large, when the load factor may go above 1, or when the hash function may be poor or attacked. Prefer [double hashing](/double-hashing/) when you want a high load factor and memory locality matters less. Use [cuckoo hashing](/cuckoo-hashing/) when you need a worst-case constant number of probes for a search.

## Pitfalls

- **Delete by writing EMPTY.** Line L14 alone, without the loop of lines L16 to L21, breaks (P). In the example, after deleting 18 that way, a search for 50 stops at the EMPTY slot 2 and fails.
- **The wrong test in line L20.** The test must be cyclic. Take $m = 8$ with a key of home 7 in slot 7 and a key of home 0 in slot 0, and delete the first one. The hole is $i = 7$, and for the key at $j = 0$ the test $i < r \le j$ reads $7 < 0 \le 0$, which is false. So that key moves to slot 7, and a search from its home 0 meets the EMPTY slot 0 and fails. Use $0 < (r - i) \bmod m \le (j - i) \bmod m$.
- **A full table.** If $n = m$, the loops of lines L2 and L8 never stop for an absent key. Grow the table before $n + 1 = m$, and in practice much earlier.
- **A weak hash function.** With $h(k) = k \bmod m$, all multiples of $m$ share the home 0, and consecutive integers fill one long run. Aligned pointers have the same problem in their low bits. Use a hash function with good mixing, such as [multiplicative hashing](/multiplicative-hashing/) with the high bits, or [tabulation hashing](/tabulation-hashing/).
- **Mutable keys.** If a key changes after the insert, its home changes, and (P) breaks for it.

## Implementations

## History

Knuth, in the history at the end of Section 6.4, reports that Gene Amdahl, Elaine M. McGraw (then Boehme), Nathaniel Rochester and Arthur Samuel used open addressing with linear probing in an assembler for the IBM 701 in 1954, and that the idea is due to Amdahl. W. W. Peterson introduced the term open addressing in 1957. Knuth analysed linear probing in unpublished notes of 1963, and the exact formulas are in Section 6.4 with Algorithm L. The deletion without tombstones is Algorithm R of the same section. Pagh, Pagh and Ružić (STOC 2007, SIAM Journal on Computing 2009) and Pătraşcu and Thorup (ICALP 2010) settled how much independence of the hash function linear probing needs.

## References
