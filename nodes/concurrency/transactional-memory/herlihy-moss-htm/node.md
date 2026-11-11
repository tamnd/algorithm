---
tag: JTKCNV
kind: algorithm
slug: herlihy-moss-htm
name: Herlihy-Moss transactional memory
aliases:
- Herlihy-Moss HTM
area: concurrency/transactional-memory
level: research
summary: "The first hardware transactional memory (1993): instructions LT, LTX, ST, COMMIT, ABORT and VALIDATE, run in a small transactional cache added to the cache coherence protocol."
complexity:
  vars: {n: the number of processors, C: the number of entries of a transactional cache}
  steps: {instruction: Θ(1), commit: Θ(1)}
  space: {cache: Θ(C)}
properties: {deterministic: true, serializable: true, deadlock_free: true, livelock_free: false, bounded_size: true}
history:
  year: 1993
  people: [Maurice Herlihy, J. Eliot B. Moss]
  note: Herlihy and Moss introduced transactional memory at ISCA 1993, as a multi-word generalization of load-linked and store-conditional built into the cache coherence protocol.
prereqs: [transaction, load-linked-store-conditional, serializability]
see_also: [hardware-transactional-memory, best-effort-htm, shavit-touitou-stm, read-set-and-write-set, zombie-transactions, transaction-validation, eager-conflict-detection, lazy-versioning]
sources:
  - paper: doi:10.1145/165123.165164
    title: "Maurice Herlihy and J. Eliot B. Moss, Transactional memory: architectural support for lock-free data structures, ISCA 1993, pp. 289 to 300"
    locator: Section 2 (the instructions and their intended use), Section 3 (the snoopy cache implementation, Tables 1 to 3), Section 4 (rationale, overflow), Section 5 (simulations) and Section 6 (relation to LL/SC)
  - book: "Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, Morgan and Claypool, 2010, doi:10.1007/978-3-031-01728-5"
    locator: the chapter on hardware-supported transactional memory
  - paper: doi:10.1145/224964.224987
    title: "Nir Shavit and Dan Touitou, Software transactional memory, PODC 1995, pp. 204 to 213"
    locator: a software version of transactional memory, motivated by the lack of the hardware support of Herlihy and Moss
  - paper: doi:10.1145/1250662.1250674
    title: "Jayaram Bobba, Kevin E. Moore, Haris Volos, Luke Yen, Mark D. Hill, Michael M. Swift and David A. Wood, Performance pathologies in hardware transactional memory, ISCA 2007, pp. 81 to 91"
    locator: conflict resolution policies of HTM and the pathologies they cause
---

**Herlihy-Moss transactional memory** is the design that gave transactional memory its name. In 1993 Maurice Herlihy and Eliot Moss proposed six new instructions, **LT**, **LTX**, **ST**, **COMMIT**, **ABORT** and **VALIDATE**, with which a program can define its own atomic read-modify-write operation on several independently chosen words of memory. The hardware keeps tentative values in a small, fully associative **transactional cache** next to the ordinary cache, and finds conflicts with a few additions to a snoopy cache coherence protocol. The design is a generalization of [load-linked and store-conditional](/load-linked-store-conditional/) from one word to many, not a construction on top of them: the paper says that LL is "essentially the same as LTX", and SC is "a combination of ST and COMMIT".

## In plain words

Each processor gets a small extra cache. When a program starts a transaction, every word it reads or writes is copied into this cache, and new values are written only there. Other processors cannot see them yet.

If another processor asks for a word in a way that clashes, the cache answers "busy", and the one that asked gives up its transaction. If the cache gets full, or an interrupt comes, the transaction also gives up. A transaction that gave up keeps running for a while, but its reads return junk, so the program asks "am I still alive?" before it trusts what it read.

At the end, the program asks to commit. If nothing went wrong, all new values become normal cache lines at once, and every other processor sees all of them together. If something went wrong, they are thrown away and the program tries again.

## The problem

Lock-free data structures avoid priority inversion, convoys and deadlock, but with only single-word primitives such as [compare-and-swap](/compare-and-swap/) or LL/SC they are hard to write when an operation must change several words: a doubly linked queue, for example, must change both head and tail when it is empty. Herlihy and Moss wanted a primitive that lets a programmer write "read these words, compute, write those words, all at once" directly, with performance close to a good spin lock.

The required behaviour is that of a [transaction](/transaction/): committed transactions appear to run one at a time (serializability), and each transaction either commits, making all its writes visible at once, or aborts and leaves no trace. The paper asks for this in the form "transactions appear to execute serially", and leaves open when exactly the hardware may abort.

## The algorithm

The processor has two flags: TACTIVE (a transaction is in progress) and TSTATUS (it has not been aborted). There is no begin instruction: the first transactional instruction starts a transaction. In the block below, "hold $a$ in mode S" means that the transactional cache of $P$ has an entry for $a$ obtained with a shared request (a T\_READ bus cycle), and mode X means an exclusive request (a T\_RFO cycle). Committed data is in memory or in ordinary cache lines.

```pseudo id=main
LT(P, a)                                         ▷ load-transactional: a joins the read set
L1  if not TSTATUS(P) then return an arbitrary value     ▷ P is an orphan: no bus cycle
L2  TACTIVE(P) ← true
L3  if a is in the transactional cache of P then return its value there
L4  if another live transaction holds a in mode X then    ▷ the T_READ gets BUSY
L5      ABORT-SELF(P); return an arbitrary value
L6  if the cache of P is full then ABORT-SELF(P); return an arbitrary value
L7  hold a in mode S with value mem[a]; return mem[a]
LTX(P, a) and ST(P, a, v)                        ▷ a joins the write set
L8  if not TSTATUS(P) then return an arbitrary value     ▷ ST does nothing
L9  TACTIVE(P) ← true
L10 if P holds a in mode X then go to L14
L11 if another live transaction holds a in any mode then  ▷ the T_RFO gets BUSY
L12     ABORT-SELF(P); return an arbitrary value
L13 if a is not in the cache of P and it is full then ABORT-SELF(P); return
L14 hold a in mode X (value mem[a] if new); for ST, set its tentative value to v
L15 return the tentative value of a                     ▷ LTX only
COMMIT(P)
L16 s ← TSTATUS(P)
L17 if s then every entry in mode X becomes the committed value   ▷ XABORT to NORMAL
L18 drop the transactional entries; TSTATUS(P) ← true; TACTIVE(P) ← false
L19 return s
ABORT(P)
L20 drop the transactional entries; TSTATUS(P) ← true; TACTIVE(P) ← false
VALIDATE(P)
L21 s ← TSTATUS(P)
L22 if not s then TSTATUS(P) ← true; TACTIVE(P) ← false
L23 return s
ABORT-SELF(P)                                    ▷ by hardware: BUSY, overflow or interrupt
L24 drop the transactional entries; TSTATUS(P) ← false   ▷ TACTIVE stays true
STORE(P, a, v) and LOAD(P, a)                    ▷ ordinary instructions, footnote 1 rule
L25 STORE: ABORT-SELF every other transaction that holds a
L26 STORE: mem[a] ← v
L27 LOAD: ABORT-SELF every other transaction that holds a in mode X
L28 LOAD: return mem[a]
```

**The transactional cache.** In the paper each transactional access makes two entries for the line: an XCOMMIT entry with the old value and an XABORT entry that receives the new one. COMMIT turns XCOMMIT entries into EMPTY and XABORT entries into NORMAL; an abort does the opposite. Both are a parallel reset of tag bits, so commit and abort take one cache cycle. The XCOMMIT entry only saves a write-back, so it can be evicted; an XABORT entry cannot, and a transaction that needs more entries than the cache has aborts (L6, L13). The block above shows one entry per line.

**Conflicts.** The other caches snoop the bus. A transactional cache of a live transaction answers a T\_READ for a line it holds in shared state with the value, and answers every other transactional request for a line it holds with **BUSY**. The processor that gets BUSY aborts: the transaction that holds a line keeps it until it ends. The paper notes that BUSY "helps prevent transactions from aborting each other too much", and that the policy "is theoretically subject to starvation".

**Orphans and VALIDATE.** An aborted transaction keeps executing until it reaches VALIDATE or COMMIT. Its transactional instructions make no bus cycles and "may return arbitrary values" (L1, L8), so the program must not act on what it read without a successful VALIDATE. The intended use is: read with LT or LTX, VALIDATE, write with ST, COMMIT, and go back to the start if VALIDATE or COMMIT fails.

**Ordinary loads and stores.** The paper leaves the mix of LOAD and STORE with transactional instructions on the same location undefined. Its footnote 1 suggests treating a LOAD or STORE "as a transaction that always commits, forcing any conflicting transactions to abort". Lines L25 to L28 and the code use this rule.

## Example

Two processors run the counter of Figure 1 of the paper, `ST(&counter, LTX(&counter) + 1)` followed by COMMIT, from counter 0.

| step | processor | instruction | effect | TSTATUS P0 | TSTATUS P1 | counter |
|---|---|---|---|---|---|---|
| 1 | P0 | LTX counter | hold counter in X, value 0 | true | true | 0 |
| 2 | P1 | LTX counter | T\_RFO gets BUSY from P0; P1 aborts, gets junk | true | false | 0 |
| 3 | P0 | ST counter 1 | tentative value 1 in the cache of P0 | true | false | 0 |
| 4 | P1 | ST counter | orphan: no effect | true | false | 0 |
| 5 | P0 | COMMIT | returns true; the entry becomes NORMAL | true | false | 1 |
| 6 | P1 | COMMIT | returns false; P1 backs off and retries | true | true | 1 |
| 7 to 9 | P1 | LTX, ST 2, COMMIT | returns true | true | true | 2 |

At step 2, P1 lost because it was the one asking. P0 never learned about the conflict. In step 4 the orphan computed with junk from step 2; this is harmless here because ST of an orphan does nothing, but a program that indexes an array with such junk must call VALIDATE first. The test `test_orphan_needs_validate` builds a reader that divides by $y - x$ for an invariant $y = x + 1$: without VALIDATE the orphan divides by zero, and with it the orphan retries.

## Correctness

Full proofs are in `proofs/correctness.md`. The core is an invariant of the caches: a line held in mode X by a live transaction is in no other transactional cache, a line held in mode S is held by no other transaction in mode X, and memory does not change for any line that a live transaction holds. This is strict [two-phase locking](/two-phase-locking/) with "no wait": an entry acts as a shared or exclusive lock taken at the first access and released only at the end, and a request that conflicts with a held lock makes the requester abort at once.

1. **Serializability.** Committed transactions, with each LOAD and STORE as a one-step transaction, are equivalent to running them one at a time in the order of their commit steps. This order respects real time.
2. **VALIDATE.** If VALIDATE returns true, all values the transaction has read come from one state of memory, the one at the step of the VALIDATE. In the words of the paper, "all values read before a successful VALIDATE are guaranteed to be consistent".
3. **Capacity.** A transaction that touches more distinct lines than the cache has entries never commits, even alone.
4. **No deadlock, but no livelock freedom.** No instruction waits. But two transactions that take $x, y$ and $y, x$ can make each other abort for ever: each one takes its first line again after it restarts, just before the other asks for it.

The tests check the first two claims on all interleavings of small programs (a shared counter, and a transfer between two accounts against a read-only audit) by replaying the committed transactions one by one in commit order, and on 600 seeded random runs with three processors. They check 3 and 4 with fixed schedules.

## Complexity

In hardware, each transactional instruction is one cache access or one bus cycle, so $\Theta(1)$, and COMMIT and ABORT are a parallel reset of tag bits in the fully associative cache, also $\Theta(1)$ cycles. The space is a transactional cache of $C$ entries per processor; the paper simulated 64 lines of 8 bytes, with 32 processors. In the model, a request looks at all $n$ caches and a commit visits the entries of one cache, so a step costs $O(n + C)$; the hardware does the same work in parallel during the snoop.

## Properties

- Serializable; committed writes become visible at once (lazy versioning in the cache).
- Conflict detection is eager: a conflict is found at the access, by the coherence protocol.
- The requester aborts (BUSY), and the holder keeps its lines.
- No deadlock; starvation and livelock are possible.
- The transaction size is bounded by the transactional cache.
- Orphans exist: an aborted transaction runs on with arbitrary values until VALIDATE or COMMIT.

## Variants and improvements

- **Directory protocol.** The paper describes the bus (snoopy) version and refers to a technical report for a similar extension of a directory-based protocol; Section 5 simulates both.
- **Overflow in software.** Section 4 suggests a LimitLESS-style trap: when the transactional cache is full, trap into software and emulate a larger one. Later unbounded HTM designs follow this idea; see [hardware transactional memory](/hardware-transactional-memory/).
- **Software transactional memory.** Shavit and Touitou gave a software version in 1995 because the hardware did not exist; see [Shavit-Touitou STM](/shavit-touitou-stm/).
- **Best-effort commercial HTM.** The machines that shipped HTM about twenty years later keep the core idea, a cache that buffers transactional lines and a coherence protocol that detects conflicts, but abort with a jump to a handler instead of running orphans, and give no size or progress guarantee. See [best-effort HTM](/best-effort-htm/).
- **Other conflict policies.** Aborting the holder instead of the requester, or stalling the requester, change which pathologies appear; Bobba et al. compare such policies.

## When to use it

The design is a reference point, not a product: no processor shipped these instructions. It is the model to study when you want to see how far a cache coherence protocol already does the work of a transaction, and what is left over: overflow, interrupts, orphans and progress. For real hardware, see [Intel TSX](/intel-tsx/) and the other [best-effort HTMs](/best-effort-htm/).

## Pitfalls

- **Trusting values before VALIDATE.** An orphan reads arbitrary values. Code that follows a pointer or indexes an array with them can fault or loop.
- **Retrying without backoff.** With requester-aborts, two symmetric transactions can abort each other for ever. The paper's examples back off exponentially after a failed COMMIT.
- **Transactions larger than the cache.** They abort every time; there must be another way to do the work.
- **Mixing ordinary and transactional access to the same data.** The paper leaves this undefined; the footnote rule used here is only one choice.
- **Reading "built on LL/SC".** The transactional cache does not use LL/SC; LL/SC is the one-word special case of it.

## Implementations

## History

Herlihy and Moss presented transactional memory at ISCA 1993 as "a new multiprocessor architecture intended to make lock-free synchronization as efficient (and easy to use) as conventional techniques based on mutual exclusion". They simulated it in the Proteus simulator for a bus machine and for a directory machine, and compared it on a counter, a producer and consumer buffer and a doubly linked list with test-and-test-and-set locks with backoff, MCS queue locks, LL/SC and hardware queueing. They traced the idea to the LOAD LINKED and STORE COND instructions of Jensen, Hagensen and Broughton and of the MIPS II and Alpha architectures. In 1995 Shavit and Touitou published software transactional memory, and hardware support of this kind reached commercial processors about two decades later.

## References
