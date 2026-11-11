---
tag: H76MZA
kind: data-structure
slug: redo-log
name: Redo log
aliases:
- deferred-update log
- write set log
area: concurrency/transactional-memory
level: advanced
summary: Private buffer of the new values of a transaction, one entry per written word. Reads look it up first; commit copies it to memory; abort throws it away.
complexity:
  vars: {w: the number of distinct words the transaction writes, t: the number of its writes}
  steps: {write: O(1), lookup: O(1), write_back: Θ(w), discard: O(1)}
  space: {log: Θ(w), append_only_log: Θ(t)}
prereqs: [read-set-and-write-set]
see_also: [undo-log, lazy-versioning, tl2, norec, commit-time-locking, bloom-filter, hash-table, write-ahead-logging]
sources:
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 2 (the version management choices, eager and lazy) and Chapter 4 (Software transactional memory), the part on the logs that an STM keeps
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: Section 2.1 (the write set as a redo log that is written back at commit under the write locks) and Section 2.2 (low-level details)
  - paper: doi:10.1145/1693453.1693464
    title: Luke Dalessandro, Michael F. Spear and Michael L. Scott, NOrec, streamlining STM by abolishing ownership records, PPoPP 2010
    locator: the write set as a redo log, written back while the global sequence lock is held
  - paper: doi:10.1145/362686.362692
    title: Burton H. Bloom, Space/time trade-offs in hash coding with allowable errors, Communications of the ACM 13(7), 1970
    locator: the filter that answers membership with false positives and no false negatives
---

A redo log is the private buffer in which a [transaction](/transaction/) keeps its writes until it commits. Each entry holds a word and the new value that the transaction wants to give it. The transaction does not change shared memory before commit. When it reads a word, it first looks in its own redo log, so that it sees its own earlier writes. When it commits, it copies the entries to memory (*write-back*). When it aborts, it throws the log away, and memory was never touched. The redo log is the data structure of [lazy versioning](/lazy-versioning/), the policy of [TL2](/tl2/), [NOrec](/norec/) and the write-back mode of [TinySTM](/tinystm/). Its counterpart is the [undo log](/undo-log/), the data structure of eager versioning, which saves old values while the new values go straight to memory. This page gives the data structure; the versioning pages give the policy and its effect on conflicts.

## In plain words

The transaction keeps a private list of "word, new value" pairs. A write adds a pair, or changes the value in the pair if the word is already in the list. A read checks the list first: if the word is there, the read returns the value from the list; if not, it reads memory. At the end, if the transaction commits, it copies every pair to memory. If it aborts, it simply forgets the list. A dictionary from word to entry makes the check fast, and a small bit filter in front of it answers "not written" for most words without touching the dictionary.

## The abstract type

A redo log stores a partial map $L$ from words to values, private to one transaction.

| Operation | Effect |
|---|---|
| write$(a, v)$ | $L(a) \leftarrow v$ |
| lookup$(a)$ | return $L(a)$, or MISS if $a$ has no value in $L$ |
| write-back$(M)$ | for each $a$ with a value in $L$: $M(a) \leftarrow L(a)$ |
| discard | $L \leftarrow$ the empty map |

The STM combines lookup with a read of memory: read$(a)$ returns $L(a)$ if it exists, and the shared value otherwise. This is the *read after write* rule, and it is why the [write set](/read-set-and-write-set/) needs a fast lookup, while the read set does not.

## Representation

- A list $E$ of entries $[a, v]$, one per written word, in the order of the first write to the word.
- A map index from each written word to its position in $E$ (a [hash table](/hash-table/)).
- A filter $F$ of $f$ bits with $h$ hash functions, a small [Bloom filter](/bloom-filter/). A word that is in the log has all its $h$ bits set. A word with a clear bit is surely not in the log.

The list keeps the entries in one compact array, which makes write-back a simple loop. Small logs often skip the index and scan the list; the filter then avoids most scans.

## Operations

```pseudo id=main
WRITE(a, v)
L1  if a ∈ index then E[index[a]].value ← v                ▷ a second write to a word
L2  else index[a] ← |E|; append [a, v] to E; set the h bits of a in F

LOOKUP(a)
L3  if some bit of a in F is clear then return MISS        ▷ surely not written
L4  if a ∈ index then return E[index[a]].value else return MISS

WRITE-BACK(M)
L5  for each [a, v] in E: M[a] ← v

DISCARD()
L6  E ← empty; index ← empty; F ← 0
```

The STM calls these from its read, write, commit and abort code. A read is: $v \leftarrow$ LOOKUP$(a)$; if $v = $ MISS, then read shared memory (with the checks of the STM). A commit is: acquire the write locks or the global lock, validate, WRITE-BACK, release. An abort is: DISCARD.

## Example

Memory $x = y = z = 0$. A transaction writes $x \leftarrow 1$, $y \leftarrow 2$, $x \leftarrow 3$.

| Step | Operation | Entries $E$ | Result | Memory $(x, y, z)$ |
|---|---|---|---|---|
| 1 | write$(x, 1)$ | $[x, 1]$ | | $(0, 0, 0)$ |
| 2 | write$(y, 2)$ | $[x, 1], [y, 2]$ | | $(0, 0, 0)$ |
| 3 | write$(x, 3)$ | $[x, 3], [y, 2]$ | L1 updates in place | $(0, 0, 0)$ |
| 4 | lookup$(x)$ | same | 3 (read after write) | $(0, 0, 0)$ |
| 5 | lookup$(z)$ | same | MISS: read memory, 0 | $(0, 0, 0)$ |
| 6 | write-back | same | 2 words written | $(3, 2, 0)$ |

Before step 6, no other process can see the writes. If the transaction aborts instead of step 6, memory stays $(0, 0, 0)$ with no work at all. The test `test_worked_example` runs these steps.

With a filter of $f = 64$ bits and $h = 2$ hash functions, a log of 8 words set 13 bits in the test, and 414 of 10000 other words passed the filter (false positives), close to $(13/64)^2 \cdot 10000 \approx 413$. The usual estimate $(1 - e^{-hw/f})^h \cdot 10000$ gives about 489. A false positive costs one probe of the index and is then answered correctly.

## Correctness

The full proof is in [the correctness proof](proofs/correctness). It shows by induction on the writes that the log holds exactly one entry per written word, with the last value written, and that index and filter agree with the entries. So a lookup returns the last value the transaction wrote, the filter never hides a written word, and write-back leaves memory as if the writes had been applied one by one. The entries are for distinct words, so the order of write-back does not matter for the result.

The proof is about the private log. Atomic write-back with respect to other transactions is the job of the STM: [TL2](/tl2/) holds the write locks of all logged words during write-back ([commit-time locking](/commit-time-locking/)), and [NOrec](/norec/) holds one global lock.

## Complexity

Let $w$ be the number of distinct words written and $t$ the number of writes.

- write and lookup take $O(1)$ expected time with the hash index. A lookup of an unwritten word usually stops at the filter, with no probe.
- With a linear scan instead of the index, write and lookup take $O(w)$ time. The test `test_scan_costs_w_squared_probes_and_the_index_2w` counts the probes for $w$ distinct writes followed by a lookup of each word: $2w$ with the index and $w(w-1)/2 + w(w+1)/2 = w^2$ with the scan.
- write-back takes $\Theta(w)$ shared writes, one per word, however many times a word was written.
- discard takes $O(1)$ shared steps (none at all) and $O(w)$ local time to clear, or $O(1)$ with a generation counter.
- Space: $\Theta(w)$ entries. An append-only log takes $\Theta(t)$.

The memory cost of a commit is the point of comparison with the [undo log](/undo-log/). The redo log writes memory once per word at commit, and an abort costs nothing. The undo log writes memory at each first write and again at abort, and a commit costs nothing. The redo log adds a lookup to every read.

## Variants

- **Append-only log.** Append an entry at every write and write back in log order, so the last write wins. It saves the index, but the log grows with $t$ and a lookup must find the last entry of the word. The test shows 30 entries for 30 writes to 3 words, against 3 entries in the indexed log.
- **Scan with a filter.** Most transactions write few words. A short array scan, guarded by the filter, can be faster than a hash table.
- **Word or object granularity.** A word-based STM logs words. An object-based STM such as [DSTM](/dstm/) instead keeps a private copy of each object it writes; the copy plays the role of the log entry.
- **Write-back under different locks.** TL2 writes back under per-stripe locks, NOrec under one global sequence lock, and TinySTM in its write-back mode under encounter-time locks.
- **Database redo logs.** In a database, a redo log is a durable record on disk that lets recovery repeat committed work after a crash ([write-ahead logging](/write-ahead-logging/), [ARIES](/aries-recovery/)). The STM redo log is not durable and is never replayed after a crash; it shares only the idea of holding new values.

## When to use it

Use a redo log when aborts are frequent, because an abort is free; when readers must not see uncommitted values without extra checks, because memory holds only committed values; and when write locks should be held only for a short time at commit. Avoid it when transactions read many words that they also wrote, since each such read pays a lookup, or when the commit must be as short as possible, since write-back is done at commit.

## Pitfalls

- **Missing the read after write.** A read that goes straight to memory returns the old value after the transaction has written the word. Every read must look in the log first.
- **Write-back without locks.** Two committers that write back the same words at the same time can interleave and leave a state that neither wrote. The STM must lock the words (or hold a global lock) during write-back.
- **Partial values.** A log entry must hold the whole word. Logging bytes or fields of a word separately, and writing back the whole word, can overwrite fields that the transaction did not write. Byte-level logs need a mask per entry.
- **Wrong filter.** A filter must never give a false negative. Two hash functions that are not independent (for example, two CRC values of strings that differ in a fixed prefix) raise the false positive rate a lot; a first version of the test met this, with 2272 false positives in 10000 instead of about 400.
- **Privatization.** After a commit, the write-back of a slow committer can still be running when another thread reads the same data outside any transaction. See [privatization safety](/privatization-safety/).

## Implementations

## History

The idea of deferred update comes from databases, where a transaction can keep its updates in a private workspace and apply them at commit; the "redo" name comes from the database logs used in recovery. In transactional memory, lazy versioning with a private write buffer appears in hardware designs from Herlihy and Moss (1993), and in most software designs after DSTM (2003). The word-based STMs TL2 (2006) and NOrec (2010) keep the write set as a redo log and write it back at commit.

## References
