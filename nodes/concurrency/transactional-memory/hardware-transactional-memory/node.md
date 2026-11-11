---
tag: V51MHT
kind: concept
slug: hardware-transactional-memory
name: Hardware transactional memory
aliases:
- HTM
area: concurrency/transactional-memory
level: advanced
summary: Transactions run by the processor itself. The cache keeps the tentative values, and the cache coherence protocol finds conflicts, so a transaction costs little more than the plain code.
prereqs: [transaction, read-set-and-write-set]
see_also: [herlihy-moss-htm, best-effort-htm, intel-tsx, hybrid-transactional-memory, transactional-lock-elision, software-transactional-memory, strong-atomicity, contention-management]
sources:
  - paper: doi:10.1145/165123.165164
    title: "Maurice Herlihy and J. Eliot B. Moss, Transactional memory: architectural support for lock-free data structures, ISCA 1993, pp. 289 to 300"
    locator: the first HTM, with a transactional cache and new instructions, and the argument that coherence protocols can detect conflicts
  - book: "Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, Morgan and Claypool, 2010, doi:10.1007/978-3-031-01728-5"
    locator: the chapter on hardware-supported transactional memory, with the design space of versioning, conflict detection, bounded and unbounded HTMs
  - paper: doi:10.1145/1250662.1250674
    title: "Jayaram Bobba, Kevin E. Moore, Haris Volos, Luke Yen, Mark D. Hill, Michael M. Swift and David A. Wood, Performance pathologies in hardware transactional memory, ISCA 2007"
    locator: the classes of HTM by versioning and conflict detection, and the pathologies that each conflict policy can show
  - paper: doi:10.1145/1508244.1508263
    title: "Dave Dice, Yossi Lev, Mark Moir and Daniel Nussbaum, Early experience with a commercial hardware transactional memory implementation, ASPLOS 2009, pp. 157 to 168"
    locator: the HTM of the Rock processor and the reasons for which its transactions failed in practice
  - paper: doi:10.1145/2485922.2485942
    title: "Harold W. Cain, Maged M. Michael, Brad Frey, Cathy May, Derek Williams and Hung Le, Robust architectural support for transactional memory in the Power architecture, ISCA 2013"
    locator: the HTM of the POWER architecture
---

A **hardware transactional memory** (HTM) runs [transactions](/transaction/) in the processor. The processor keeps the tentative writes of a transaction in its cache or in a log, marks the lines that the transaction reads and writes, and uses the cache coherence protocol to see when another processor touches one of them. If no conflict happens, the end instruction makes all the writes visible at once; otherwise the processor aborts the transaction and discards its writes. Herlihy and Moss proposed the idea in 1993, and commercial processors from IBM and Intel have shipped it since 2012.

## In plain words

A processor already keeps copies of memory in its cache, and it already talks to the other processors whenever one of them wants to change a line that others hold. That talk is exactly what a transaction needs to find conflicts.

So the hardware adds a little: a mark on each cache line that a transaction used, a way to keep new values private until the end, and a way to throw them away. When another processor asks for a marked line in a way that conflicts, the transaction fails. At the end, the hardware drops the marks, and all the new values become visible together.

The cost is close to that of plain loads and stores. The limits are those of the cache: a transaction that uses too much data, or runs too long, cannot fit.

## The idea

An HTM must answer the same questions as a [software TM](/software-transactional-memory/), but it answers them with cache hardware.

**Read and write sets.** The [read set and write set](/read-set-and-write-set/) are kept as marks on cache lines: a read bit and a write bit per line, or a separate small cache for transactional lines, as in the original design of [Herlihy and Moss](/herlihy-moss-htm/). Some research designs summarize the sets in hardware Bloom filters called signatures, which cannot overflow but can report false conflicts. Because the sets are tracked per line, two transactions that use different words on the same line conflict (false sharing).

**Versioning.** Where do the new values live before commit?

- *Lazy versioning.* New values stay in the cache (or a store buffer) and are not visible to others; old values stay in memory. Abort is cheap: discard the marked lines. Commit must make the lines visible together. Most commercial designs do this, which is why a transaction that writes more than the cache can hold must abort. See [lazy versioning](/lazy-versioning/).
- *Eager versioning.* New values go to memory in place, and old values go to an undo log in memory. Commit is cheap; abort must copy the log back. LogTM (Moore and colleagues, 2006) is the best-known example; because the log is in ordinary memory, such a design can support larger transactions. See [eager versioning](/eager-versioning/).

**Conflict detection.**

- *Eager.* The coherence request that would create a conflict is seen at once by the processor that holds the line, so the conflict is found at the access. Almost all HTMs, including all commercial ones, work in this way. See [eager conflict detection](/eager-conflict-detection/).
- *Lazy.* Transactions run without checking, and at commit a transaction broadcasts its write set; others that read those lines abort. The TCC design (Hammond and colleagues, 2004) is the standard example. See [lazy conflict detection](/lazy-conflict-detection/).

**Conflict resolution.** When a request hits a marked line, who loses?

- *Requester wins.* The holder aborts. This is simple, because the coherence protocol does not change, and it is what Intel TSX appears to do. It can livelock when two transactions keep aborting each other.
- *Requester loses.* The requester aborts, as with the BUSY reply of Herlihy and Moss. This can also livelock.
- *Requester stalls.* The holder delays the request (a negative acknowledgment) and the requester waits, as in LogTM. A cycle of waiting transactions would deadlock, so the hardware must detect possible cycles and abort one transaction, usually using timestamps.

Bobba and colleagues studied the combinations and named the pathologies that each can show, such as a writer that starves behind a stream of readers, and two transactions that keep aborting each other when both upgrade a line from read to write. These are hardware forms of [contention management](/contention-management/).

**Isolation.** The coherence protocol sees all accesses, transactional or not. So in most HTMs a plain store by another processor aborts a transaction that read the line, and a plain load cannot see the tentative writes of a transaction. This is [strong atomicity](/strong-atomicity/), which most software TMs do not give.

**Bounded, unbounded and best effort.** A transaction can exceed the hardware in two ways: in size, when its lines do not fit, and in time, when an interrupt, a context switch or a page fault comes before it ends.

- *Unbounded HTM.* Research designs keep the transaction alive in these cases: UTM and LTM (Ananian and colleagues, 2005) spill state to memory, VTM (Rajwar, Herlihy and Lai, 2005) virtualizes it so that transactions survive context switches, and LogTM keeps versions in memory. These designs need much more hardware and help from the operating system.
- *Bounded HTM.* The hardware guarantees to commit transactions within a known size and time, and the program must stay inside these limits. The constrained transactions of IBM System z are of this kind.
- *Best-effort HTM.* The hardware may abort any transaction, for any reason, and software must provide a fallback path. All widely used commercial HTMs are best effort; see [best-effort HTM](/best-effort-htm/).

**Interfaces.** An HTM can offer explicit transactions (begin and end instructions, as in [Intel TSX](/intel-tsx/) RTM, IBM POWER and System z), or elide existing locks without new code (speculative lock elision and Intel HLE; see [transactional lock elision](/transactional-lock-elision/)). The Herlihy and Moss design is between the two: it marks the individual loads and stores that belong to a transaction.

## Examples

**The design space.** Some systems, by their choices:

| system | year | versioning | conflict detection | on a conflict |
|---|---|---|---|---|
| [Herlihy and Moss](/herlihy-moss-htm/) | 1993 | lazy, in a transactional cache | eager | the requester aborts |
| TCC | 2004 | lazy, in the cache | lazy, at commit | the committer wins |
| LogTM | 2006 | eager, undo log in memory | eager | the requester stalls; a possible cycle aborts one |
| Sun Rock | 2009 (not shipped) | lazy, in a store buffer | eager | best effort; see [best-effort HTM](/best-effort-htm/) |
| [Intel TSX](/intel-tsx/) | 2013 | lazy, in the cache | eager | best effort; the requester appears to win |

**A conflict, step by step.** Processors $P$ and $Q$ run transactions. $P$ reads $x$; its line is marked as read, in shared state. $Q$ writes $x$; the write needs the line in exclusive state, so $Q$ sends an invalidation, and $P$ receives it for a marked line. With requester wins, $P$ aborts: its marks and its tentative writes are gone, and it restarts at its fallback address. $Q$ goes on, and its write stays in its cache, invisible to others, until $Q$ commits. No extra message was needed; the conflict was found by the message that the protocol sends anyway.

**A model.** The pages on [best-effort HTM](/best-effort-htm/) and [lock elision](/transactional-lock-elision/) include a small simulator, `htmsim.py`, with lazy versioning, eager detection, requester wins, bounded read and write sets, and abort codes in the format of Intel TSX. The page on [Herlihy and Moss](/herlihy-moss-htm/) simulates their original design, in which the requester loses.

## Where it is used

- **Commercial processors.** IBM Blue Gene/Q (2012), IBM zEC12 and later System z (2012), Intel processors with TSX (from 2013, now disabled on many by microcode), and IBM POWER8 and POWER9. Sun's Rock was never shipped.
- **Lock elision.** The main use in practice: run critical sections of existing locks as transactions, so that programs speed up without changes.
- **Runtimes and hybrids.** Language runtimes and [hybrid TMs](/hybrid-transactional-memory/) run transactions in hardware first and in software when the hardware fails.
- **Concurrent data structures.** A short hardware transaction can replace a [multi-word compare-and-swap](/multi-word-cas/) or a complex lock-free step, with a simpler path as the fallback.
- **Research.** HTM simulators and the [STAMP](/stamp-benchmark-suite/) benchmarks have been the standard way to compare designs.

## References
