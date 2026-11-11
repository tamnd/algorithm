---
tag: 1YQJMV
kind: definition
slug: read-set-and-write-set
name: Read set and write set
aliases:
- read set
- write set
- read log
- write log
area: concurrency/transactional-memory
level: intro
summary: The words a transaction has read and written so far. The read set is checked to detect conflicts; the write set holds the new or old values and must answer read-after-write lookups.
prereqs: [transaction]
see_also: [transaction-conflict, transaction-validation, redo-log, undo-log, tl2, norec, bloom-filter, opacity]
sources:
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 2 (read sets, write sets and conflicts) and Chapter 4 (Software transactional memory), the parts on STM logs and validation
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: Section 2.1 (the read set of addresses, the write set as a redo log, and the read-after-write check)
  - paper: doi:10.1145/1693453.1693464
    title: Luke Dalessandro, Michael F. Spear and Michael L. Scott, NOrec, streamlining STM by abolishing ownership records, PPoPP 2010
    locator: the read set of (address, value) pairs and value-based validation
  - paper: doi:10.1145/872035.872048
    title: "Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III, Software transactional memory for dynamic-sized data structures, PODC 2003, pages 92-101"
    locator: the read-only table of (object, version) pairs that a transaction validates
---

The **read set** of a [transaction](/transaction/) is the set of shared words (or objects) it has read so far; the **write set** is the set of words it has written so far. A transactional memory uses the two sets to decide whether two transactions conflict, to check that a transaction's reads are still valid, and to commit or undo its writes. In software transactional memory, each set is also a private data structure, a *log*, that holds more than the addresses: the read set holds what the STM needs to check a read later (a version or a value), and the write set holds the values to install or to restore. The two sets have different jobs and different costs. A read must look in the write set to see the transaction's own writes, so the write set needs a fast lookup. The read set needs no lookup; it only needs to be scanned at validation.

## Definition

**Notation and model.** $n$ is the number of processes, $p$ and $q$ are processes, $m$ is the number of shared words. A transaction $T$ runs read and write operations on words $a$. $r$ is the size of the read set and $w$ the size of the write set.

**Definition.** At a point in the run of $T$:

- the **read set** $RS(T)$ is the set of words $a$ such that $T$ has executed read$(a)$ and that read returned a value from shared memory;
- the **write set** $WS(T)$ is the set of words $a$ such that $T$ has executed write$(a, v)$ for some $v$.

Two live transactions $T$ and $U$ **conflict** on $a$ if $a \in WS(T) \cap (RS(U) \cup WS(U))$ or $a \in WS(U) \cap RS(T)$. See [transaction conflict](/transaction-conflict/).

Some authors put every read word in the read set, also the words that the transaction reads after writing them. Such a read returns the transaction's own value and cannot conflict on its own, so most STMs leave it out, as the definition above does.

**What each set holds in an STM.**

| Set | Entry | Example STM | Used for |
|---|---|---|---|
| read set | address only | [TL2](/tl2/) | at commit, check that the lock of each address is free and its version is at most the start time $rv$ |
| read set | (address, version of its lock) | [TinySTM](/tinystm/), [SwissTM](/swisstm/) | check that the version is unchanged, to extend the snapshot |
| read set | (address, value read) | [NOrec](/norec/) | value-based validation: read each address again and compare |
| read set | (object, version) | [DSTM](/dstm/) | check that the version is still current |
| write set | (address, new value) | TL2, NOrec, TinySTM write-back | a [redo log](/redo-log/), copied to memory at commit |
| write set | (address, old value) plus the held lock | TinySTM write-through | an [undo log](/undo-log/), copied back at abort |

**The read-after-write lookup.** With lazy versioning, memory does not hold the transaction's own writes. So every read$(a)$ must first look up $a$ in the write set and return the buffered value if it is there. This lookup happens at every read, also for the many words that are not in the write set, so it must be fast: a hash index, often with a small [Bloom filter](/bloom-filter/) in front of it. With eager versioning, memory already holds the transaction's writes, and no lookup is needed. The read set never needs a lookup: a word may even appear twice, which costs a little space and no correctness.

**Costs.** For a transaction that reads $r$ words and writes $w$ words:

| Operation | Cost |
|---|---|
| add a read to the read set | $O(1)$, an append |
| write-set lookup at a read (lazy versioning) | $O(1)$ expected with a hash index, $O(w)$ with a scan |
| add a write to the write set | $O(1)$ expected |
| validate the read set once | $O(r)$ |
| validate the read set at every read | $r(r+1)/2$ checks in all, see [transaction validation](/transaction-validation/) |
| commit the write set | $O(w)$ lock steps and memory writes |
| space | $\Theta(r + w)$ private words |

The read set is usually much larger than the write set, so the cost of keeping and checking it is the main cost of most STMs. A [global version clock](/global-version-clock/) lets an STM check each read once, in $O(1)$, instead of checking the whole read set again.

## Examples and non-examples

**Example (a transfer).** $T$ moves 3 from $x$ to $y$, with $x = y = 10$: it reads $x$, reads $y$, writes $x \leftarrow 7$, writes $y \leftarrow 13$. After the four operations, $RS(T) = \{x, y\}$ and $WS(T) = \{x, y\}$. In TL2 the read set holds $x, y$ and the write set holds $[x, 7], [y, 13]$. In NOrec the read set holds $(x, 10), (y, 10)$.

**Example (read after write).** $T$ writes $x \leftarrow 5$ and then reads $x$. In a redo-log STM, the lookup finds $x$ in the write set and returns 5; memory still holds the old value. The read does not enter the read set. If the lookup were skipped, $T$ would read the old value of $x$, which breaks the program order inside one transaction.

**Example (a read-only transaction).** An audit reads $x$ and $y$ and writes nothing. $WS = \emptyset$, so in TL2 it commits with no lock, no clock increment and no validation: each read was already checked against $rv$ when it happened.

**Example (a conflict).** $T$ has $RS(T) = \{x\}$, and $U$ has $WS(U) = \{x\}$. They conflict on $x$. If $U$ commits first, $T$ must abort or be ordered before $U$. If both only read $x$, they do not conflict.

**Non-example (a word that was not read).** A transaction that reads a pointer $p$ and then reads the node at $p$ has the node in its read set, not every node of the list. A conflict on a node it never read does not concern it. This is why STM allows more parallel work than one lock around the whole list.

**Non-example (striped metadata).** If the STM maps words to locks by a hash, then $x$ and $z$ may share one lock. A writer of $z$ then looks like a writer of $x$ to a reader of $x$: a *false conflict*. The read set is still $\{x\}$; the false conflict comes from the metadata, not from the sets. See [transaction conflict](/transaction-conflict/).

## Related definitions

- A [transaction conflict](/transaction-conflict/) is defined by the read and write sets.
- [Transaction validation](/transaction-validation/) checks the read set.
- The [redo log](/redo-log/) and the [undo log](/undo-log/) are the two forms of the write set.
- [Eager](/eager-conflict-detection/) and [lazy conflict detection](/lazy-conflict-detection/) say when the sets are compared.
- In databases, the read set and write set of a transaction are the basis of [optimistic concurrency control](/optimistic-concurrency-control/) (Kung and Robinson 1981), which validates a transaction's read set against the write sets of transactions that committed during its run.

## References
