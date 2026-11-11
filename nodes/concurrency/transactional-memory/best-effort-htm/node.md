---
tag: W7DBTZ
kind: concept
slug: best-effort-htm
name: Best-effort hardware transactional memory
aliases:
- best-effort HTM
area: concurrency/transactional-memory
level: advanced
summary: Hardware transactions that may abort for any reason, even when run alone. No transaction is sure to commit, so software must always provide a fallback path, such as a lock.
prereqs: [hardware-transactional-memory]
see_also: [intel-tsx, transactional-lock-elision, hybrid-transactional-memory, herlihy-moss-htm, transaction-abort, transaction-irrevocability, contention-management, exponential-backoff]
sources:
  - paper: doi:10.1145/1168857.1168900
    title: "Peter Damron, Alexandra Fedorova, Yossi Lev, Victor Luchangco, Mark Moir and Daniel Nussbaum, Hybrid transactional memory, ASPLOS 2006, pp. 336 to 346"
    locator: a TM design that uses best-effort HTM when it can and does not depend on it
  - paper: doi:10.1145/1508244.1508263
    title: "Dave Dice, Yossi Lev, Mark Moir and Daniel Nussbaum, Early experience with a commercial hardware transactional memory implementation, ASPLOS 2009, pp. 157 to 168"
    locator: the checkpoint and commit instructions of Rock, the CPS register that reports why a transaction failed, and the reasons for failure seen in practice
  - paper: doi:10.1145/2370816.2370836
    title: "Amy Wang, Matthew Gaudet, Peng Wu, Jose Nelson Amaral, Martin Ohmacht, Christopher Barton, Raul Silvera and Maged Michael, Evaluation of Blue Gene/Q hardware support for transactional memories, PACT 2012"
    locator: speculation in the multi-versioned L2 cache, the short-running and long-running modes, and the software runtime that retries and then runs a transaction alone
  - paper: doi:10.1145/2485922.2485942
    title: "Harold W. Cain, Maged M. Michael, Brad Frey, Cathy May, Derek Williams and Hung Le, Robust architectural support for transactional memory in the Power architecture, ISCA 2013"
    locator: tbegin, tend and tabort, suspend and resume, rollback-only transactions, and the failure cause register with its persistent bit
  - paper: doi:10.1109/MICRO.2012.12
    title: "Christian Jacobi, Timothy Slegel and Dan Greiner, Transactional memory architecture and implementation for IBM System z, MICRO 2012"
    locator: nonconstrained transactions with a fallback, and constrained transactions that the machine guarantees to complete
  - book: "Intel 64 and IA-32 Architectures Software Developer's Manual, Volume 1, Chapter 16, Programming with Intel Transactional Synchronization Extensions"
    locator: the RTM abort status in EAX (Table 16-1), and the statement that software must provide a fallback path for RTM
  - book: "Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, Morgan and Claypool, 2010, doi:10.1007/978-3-031-01728-5"
    locator: the chapter on hardware-supported transactional memory
---

A **best-effort hardware transactional memory** runs transactions in hardware but promises nothing about whether a given transaction will ever commit. A transaction can abort because another processor touched its data, because its data does not fit in the cache, because of an interrupt, a page fault or a context switch, because it executed an instruction that the hardware cannot undo, or for reasons the manual does not list. It can abort every time, even when no other thread runs. Every best-effort HTM therefore needs a **fallback path**: code that does the same work without a hardware transaction, usually under a lock or in a [software transactional memory](/software-transactional-memory/).

## In plain words

A hardware transaction is fast because the processor keeps the tentative data in its cache and uses the cache coherence protocol to see conflicts. But a cache is small, and the processor has many other jobs. When something does not fit or cannot be undone, the simplest thing the hardware can do is give up and tell the program.

So the hardware makes a deal with the program: "I will try, and I will tell you roughly why I failed. You must have another way to do the work." The program tries a few times in hardware, and if it keeps failing, or if the reason says that trying again will not help, it takes a lock and does the work the slow way. The hard part is to make sure that the slow way and the fast way never get in each other's way.

## The idea

**Why best effort.** A transaction that must always commit needs hardware that can hold any amount of tentative state, survive interrupts and context switches, and guarantee progress against conflicts. Proposals for such unbounded HTM exist (see [hardware transactional memory](/hardware-transactional-memory/)), but they are complex. A best-effort design uses the structures that a processor already has: the read set is a set of marked cache lines, the write set is held in the cache or a store buffer, and a conflict is a coherence request for a marked line. Anything outside this simple case aborts.

**The abort status.** Software sees only that the transaction failed and a summary of why. In the model on this page the status word has the layout of the RTM abort status of [Intel TSX](/intel-tsx/):

| bit | name | meaning | retry? |
|---|---|---|---|
| 0 | explicit | the program called XABORT; bits 31 to 24 hold its 8-bit code | the program decides |
| 1 | retry | the hardware thinks that a retry may succeed | yes |
| 2 | conflict | another processor accessed a line of the transaction | usually yes |
| 3 | capacity | an internal buffer overflowed | no, not in the same form |
| none | other | an interrupt, an unsupported instruction, and similar | sometimes |

The Intel manual says that the retry bit is always clear when the explicit bit is set, and that the status can be 0, for example after an abort caused by the CPUID instruction. Other machines report causes differently: Rock had a checkpoint status (CPS) register with one bit per kind of failure, and the POWER architecture records the cause in a register that also says whether the failure is persistent.

**The fallback path.** The usual fallback is a single global lock, used as in [transactional lock elision](/transactional-lock-elision/):

1. Wait until the lock is free.
2. Begin a hardware transaction, and read the lock inside it. If the lock is held, abort explicitly.
3. Run the block and commit.
4. On an abort, look at the status. If a retry may help and the number of tries is below a limit, go to step 1. Otherwise take the lock and run the block without a transaction.

Reading the lock in step 2 is what makes the two paths safe together. The lock is now in the read set of every hardware transaction, so the store that takes the lock is a conflict that aborts all of them, and no hardware transaction can commit while a thread runs under the lock. Leaving it out lets a hardware transaction see half of the work of a lock holder; the page on lock elision shows such a run.

**Progress.** A best-effort HTM alone gives no progress guarantee. Progress comes from the fallback: if the number of hardware tries is bounded and the fallback lock is deadlock-free, then every attempt ends in a bounded number of tries, and some thread is always able to complete. The price is that the fallback serializes all threads while it runs.

The code for this page, `impl/python/htmsim.py`, is a small model of such a machine: per-processor read and write sets with separate bounds, conflict detection on every request (the requester wins, and ordinary loads and stores count as requests), and the status bits above. `impl/python/best_effort_htm.py` runs a block with the retry policy and fallback lock described here. The tests check the abort codes for conflict, capacity, explicit aborts and interrupts; that a block larger than the write buffer aborts on every try when no other thread runs; and, over all interleavings of two threads, that every thread finishes and the counter is right, even when the hardware can never commit.

## Examples

**A capacity abort.** With a write buffer of 4 lines, a block that writes 6 lines aborts with the capacity bit on the 5th write, every time. The retry policy sees no retry bit and goes to the lock after one try. Without a fallback, a loop that retries in hardware never ends; the test runs 100 tries and sees 100 capacity aborts and no commit.

**A conflict abort.** Thread 0 reads $x$ in a transaction, and thread 1 writes $x$. In the model the request of thread 1 aborts thread 0, whose next instruction raises an abort with the conflict and retry bits. Thread 0 waits for the lock to be free, retries, and commits.

**Commercial designs.**

| machine | year | notes |
|---|---|---|
| Sun Rock | 2009 (not shipped) | `chkpt` and `commit` instructions; the CPS register gives the reason for a failure; Dice, Lev, Moir and Nussbaum reported their experience with pre-production chips |
| IBM Blue Gene/Q | 2012 | speculation in a multi-versioned L2 cache; a short-running and a long-running mode; the software runtime retries a transaction and then runs it alone, without speculation |
| IBM zEC12 (System z) | 2012 | nonconstrained transactions need a fallback; **constrained transactions**, limited to a few instructions and a small memory footprint, are guaranteed by the machine to complete eventually and need none |
| Intel Haswell and later | 2013 | [TSX](/intel-tsx/): RTM with XBEGIN, XEND and XABORT, and HLE prefixes; later disabled by microcode on many processors |
| IBM POWER8 | 2014 | `tbegin.`, `tend.`, `tabort.`; suspend and resume for non-transactional accesses inside a transaction; rollback-only transactions; a failure cause register with a persistent bit |

The constrained transactions of System z are the main exception to the rule that a fallback is required: within their limits the hardware itself provides the progress guarantee.

## Where it is used

- **Lock elision.** Run critical sections of an existing lock as hardware transactions, with the lock as the fallback. This is the common use, because it needs no change in the program. See [transactional lock elision](/transactional-lock-elision/).
- **Hybrid TM.** Run transactions in hardware first and in an STM on failure; the hard part is to let both kinds run at the same time. See [hybrid transactional memory](/hybrid-transactional-memory/).
- **Simpler concurrent data structures.** A best-effort transaction can replace a [multi-word compare-and-swap](/multi-word-cas/) or a complex lock-free step, with a lock-free or locking path as the fallback.
- **Runtimes.** The Blue Gene/Q runtime and compilers with TM support use best-effort HTM with a serial, irrevocable fallback; see [transaction irrevocability](/transaction-irrevocability/).

## References
