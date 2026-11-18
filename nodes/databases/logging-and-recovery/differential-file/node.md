---
tag: PBST4C
kind: data-structure
slug: differential-file
name: Differential file
aliases:
- Severance-Lohman differential files
area: databases/logging-and-recovery
level: advanced
summary: Keep changes in a separate file with a filter of changed keys and merge them into the main file later, which eases backup and recovery.
model: word-ram
complexity:
  vars: {n: the entries in the differential file, m: the length of the filter array, k: the hash functions of the filter, N: the records of the main file}
  time: {worst: Θ(k)}
  space: {extra: Θ(m + n)}
properties: {persistent: false, concurrent: false, external: true}
prereqs: [bloom-filter]
see_also: [shadow-paging, log-structured-merge-tree, media-recovery, point-in-time-recovery, checkpointing, crash-recovery, b-plus-tree]
sources:
  - paper: doi:10.1145/320473.320484
    title: Dennis G. Severance and Guy M. Lohman, Differential files, their application to the maintenance of large databases, ACM Transactions on Database Systems 1(3), 1976, pages 256 to 267
    locator: the differential file organization and its use for backup and recovery, the section on the search filter, and Section 2.6, Designing a Bloom filter
  - paper: doi:10.1145/358628.358632
    title: Lee L. Gremillion, Designing a Bloom filter for differential file access, Communications of the ACM 25(9), 1982, pages 600 to 604
    locator: the choice of the filter size and the number of hash functions for a differential file, paper level
  - paper: doi:10.1145/319758.319762
    title: Houtan Aghili and Dennis G. Severance, A practical guide to the design of differential files for recovery of on-line databases, ACM Transactions on Database Systems 7(4), 1982, pages 540 to 565
    locator: the design of differential files for recovery, paper level
  - paper: doi:10.1145/362686.362692
    title: Burton H. Bloom, Space/time trade-offs in hash coding with allowable errors, Communications of the ACM 13(7), 1970, pages 422 to 426
    locator: the hash-coded filter with allowable errors, paper level
---

A differential file keeps a large file of records unchanged and writes every insert, change and delete to a second, small file, the *differential file*. A read checks the small file first, but only when an in-memory [Bloom filter](/bloom-filter/) of the changed keys says that the key may be there. Now and then a *reorganization* merges the changes into a new copy of the main file. Severance and Lohman (1976) proposed it to make backup and recovery of large databases cheap: the main file changes only at a reorganization, so one dump of it stays valid until the next one. It differs from [shadow paging](/shadow-paging/), which keeps old and new versions of whole pages and switches a root pointer at commit; a differential file keeps changes at the level of records and merges them in a batch much later.

## In plain words

Think of a large printed phone book and a short list of corrections next to it. You never write in the book. A new number, a changed number or a removed name goes on the list. To find a name, you look at the list first, and if the name is not on it, you look in the book.

Reading the list each time costs work. So you keep a small card of marks: each name on the list sets a few marks. If one of the marks of a name is missing, the name is surely not on the list, and you go straight to the book. Sometimes all the marks are there by chance, and you read the list for nothing.

Once a month you print a new book with all the corrections, keep a copy in a safe place, and start an empty list.

## The abstract type

The structure stores a relation with a key: a set of records, at most one per key. The operations are:

- lookup(key): the record with this key, or *absent*;
- put(key, record): insert a record, or replace the record with this key;
- delete(key): remove the record with this key;
- scan(): all records in key order;
- reorganize(): no change to the relation; it only moves data between the parts of the structure.

The relation that the structure holds is the main file with the entries of the differential file applied over it, as defined under Correctness.

## Representation

- The **main file** $M$: the records at the last reorganization, sorted by key, for example a [B+ tree](/b-plus-tree/) or a sorted file on disk. It is read-only between reorganizations.
- The **differential file** $D$: one entry per changed key, the newest one. An entry is a new record or a *delete marker*. A real system keeps $D$ as an append-only file with an index on its keys; the code keeps a dict.
- The **filter** $F$: a Bloom filter of $m$ bits with $k$ hash functions $h_1, \dots, h_k$ over the keys in $D$, in main memory.
- The **archive**: a dump of each generation of $M$, made at the reorganization that writes it.

## Operations

```pseudo id=main
LOOKUP(key)
L1 if the bits h_1(key), ..., h_k(key) of F are all 1 then
L2     if D has an entry for key then return its record, or absent for a delete marker
L3 return the record of key in M, or absent
PUT(key, entry)                                    ▷ entry is a record or the delete marker
L4 D[key] ← entry
L5 set the bits h_1(key), ..., h_k(key) of F to 1
REORGANIZE()
L6 M' ← the merge of M and D in key order: an entry of D replaces the record of M, and a delete marker drops it
L7 dump M' to the archive; make M' the main file
L8 D ← empty; F ← all zeros
```

A lookup of an unchanged key whose filter bits are not all set reads only $M$ (line L3). A lookup whose bits are all set reads $D$; if $D$ has no entry, this was a *false positive* and the lookup goes on to $M$. A put or a delete writes only $D$ and the filter. A scan merges $M$ and $D$ in key order, as line L6 does.

**Backup and recovery.** Between two reorganizations only $D$ changes. A backup is then a dump of $D$ only, and the dump of $M$ in the archive stays valid. If the disk that holds $M$ fails, copy $M$ from the archive. If $D$ is lost, restore its last dump and redo the changes logged since. The cost of a dump and of this redo grows with the size of $D$, not with the size of the database. The analysis of how large $D$ may grow before a reorganization is in Aghili and Severance (1982).

## Example

Main file $M$: keys 1, 2 and 3 with records a, b and c. The filter has $m = 16$ bits and $k = 2$ hash functions; for the hand example take $h_1(x) = x \bmod 16$ and $h_2(x) = (5x + 3) \bmod 16$ (the code uses a cryptographic hash instead).

1. put(2, B): $D = \{2 \mapsto B\}$, set bits 2 and 13.
2. delete(3): $D$ gets a delete marker for 3, set bits 3 and 2.
3. put(4, d): $D$ gets $4 \mapsto d$, set bits 4 and 7.

The filter now has bits 2, 3, 4, 7 and 13 set.

| lookup | bits | reads | answer |
|---|---|---|---|
| 1 | 1 and 8: bit 1 is 0 | $M$ | a |
| 2 | 2 and 13: both 1 | $D$ | B |
| 3 | 3 and 2: both 1 | $D$ | absent (delete marker) |
| 5 | 5 and 12: bit 5 is 0 | $M$ | absent |
| 18 | 2 and 13: both 1 | $D$, then $M$ | absent (a false positive) |

reorganize() writes $M' = \{1 \mapsto a, 2 \mapsto B, 4 \mapsto d\}$, dumps it, and clears $D$ and the filter.

## Correctness

Define the relation that the structure holds as $R(M, D)$: the records of $M$ whose key has no entry in $D$, plus the records of $D$. A delete marker in $D$ removes its key.

**Claim.** If the structure holds $R(M, D)$ = the relation of the abstract type before an operation, then after put or delete it holds the changed relation, lookup returns the record of the abstract type, and reorganize does not change $R$.

*Proof.* A Bloom filter has no false negatives: line L5 sets every bit of each key in $D$, and only line L8 clears bits, at the same time as it empties $D$. So when $D$ has an entry for the key, line L1 is true and line L2 returns the entry; when $D$ has none, lookup reaches line L3 either directly or after a false positive, and returns the record of $M$. That is the definition of $R(M, D)$. Line L4 keeps only the newest entry for a key, which is the effect of the newest put or delete. Line L6 computes $R(M, D)$ itself, so after line L8, $R(M', \emptyset) = R(M, D)$. $\square$

The filter affects only the cost of a lookup, never its answer. The [proof](proofs/correctness.md) states the invariants in full.

## Complexity

Costs are in record reads of $M$ and $D$ and in in-memory bit probes.

- **lookup**: $k$ bit probes. For a key that has an entry in $D$, one read of $D$. For an unchanged key, one read of $M$, plus one read of $D$ with the probability $p$ of a false positive.
- **put and delete**: one write to $D$ and $k$ bit sets. $M$ is not written.
- **reorganize**: one pass over $M$ and $D$ and one write of $M'$, $O(N + n)$ records if $D$ is kept in key order, plus the dump of $M'$.
- **Space**: $m$ bits of memory for the filter, and $n$ entries in $D$.

**False positive rate (theorem, in an idealized model).** If the $k$ hash values of each key are independent and uniform over the $m$ bits, the probability that a key not in $D$ passes the filter after $n$ entries is about $p \approx (1 - e^{-kn/m})^k$, the standard Bloom filter bound. It is smallest near $k = (m/n) \ln 2$. With $m = 10 n$ and $k = 7$, $p$ is under 1 percent, so unchanged keys almost never cost a read of $D$. Real hash functions only approximate the model.

## Variants

- **Filter design.** Severance and Lohman give the design of the filter in their Section 2.6, and Gremillion (1982) gives a method to choose its size and number of hash functions for a differential file.
- **Several differential files.** Two or more differential files over one read-only main file give two or more versions of the data, each seen through its own changes, for example a test version next to the live one.
- **Log-structured merge trees.** A [log-structured merge tree](/log-structured-merge-tree/) also puts all changes in a small structure, keeps Bloom filters on its sorted runs, and merges in the background. It has many levels and merges continually, where a differential file has one level and reorganizes in a batch.
- **Delta stores in column stores.** A read-optimized main store with a small write-optimized delta store and a periodic merge follows the same plan.

## When to use it

Use a differential file when the data is large, the rate of change is small, and backup or recovery of the whole data is costly. The main file stays read-only, so it can be dumped once and kept in compressed or read-optimized form. It does not help when most records change between two reorganizations: then $D$ grows as large as $M$, and every lookup passes the filter. A buffer of changes with no filter costs a read of $D$ on every lookup; the filter is what makes reads of unchanged keys cheap.

## Pitfalls

- **Delete without a marker.** If delete only removed the key from $D$, a deleted record of $M$ would come back at the next lookup. A delete needs a marker in $D$ and filter bits.
- **Clearing filter bits.** A plain Bloom filter cannot remove a key, because a bit may belong to several keys. Clear the whole filter only when $D$ is emptied at a reorganization.
- **A filter that is too small.** As $n$ grows past the design size, $p$ tends to 1 and each lookup reads $D$. Size $m$ for the largest $D$ before a reorganization, or reorganize earlier.
- **Losing the old generation too early.** Keep the old main file and its dump until the new main file is dumped. Otherwise a failure during the reorganization leaves no valid copy.

## Implementations

## History

Severance and Lohman described differential files in ACM Transactions on Database Systems in 1976, with a search filter of the kind that Bloom had proposed in 1970 for hash coding with allowable errors. Gremillion (1982) studied the design of that filter, and Aghili and Severance (1982) gave a guide to the design of differential files for the recovery of on-line databases. The plan of a read-only main structure, a small structure of changes and a batch merge returns in log-structured merge trees and in the delta stores of column stores.

## References
