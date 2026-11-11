---
tag: M45GVF
kind: concept
slug: zombie-transactions
name: Zombie transactions
aliases:
- doomed transactions
- zombie transaction
- inconsistent reads
area: concurrency/transactional-memory
level: research
summary: Running transactions that have seen an inconsistent state and will abort, but can loop, fault or corrupt memory first. Opacity forbids them; sandboxing contains them.
prereqs: [transaction-validation, transaction-abort]
see_also: [opacity, global-version-clock, tl2, norec, privatization-safety, use-after-free, type-stable-memory, epoch-based-reclamation]
sources:
  - paper: doi:10.1145/1345206.1345233
    title: "Rachid Guerraoui and Michał Kapałka, On the correctness of transactional memory, PPoPP 2008, pages 175-184"
    locator: the definition of opacity, motivated by transactions that observe inconsistent states before they abort
  - paper: doi:10.1145/2370816.2370843
    title: Luke Dalessandro and Michael L. Scott, Sandboxing transactional memory, PACT 2012
    locator: running transactions without the per-read checks of opacity, and containing the faults, loops and stray writes of zombies
  - paper: doi:10.1145/872035.872048
    title: "Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III, Software transactional memory for dynamic-sized data structures, PODC 2003, pages 92-101"
    locator: the validation of all opened objects at each open, so that a transaction never acts on an inconsistent view
  - paper: doi:10.1007/11864219_13
    title: "Michael F. Spear, Virendra J. Marathe, William N. Scherer III and Michael L. Scott, Conflict detection and validation strategies for software transactional memory, DISC 2006, LNCS 4167, pages 179-193"
    locator: the cost of validation that keeps transactions consistent, and ways to reduce it
  - paper: doi:10.1145/1065944.1065952
    title: Tim Harris, Simon Marlow, Simon Peyton Jones and Maurice Herlihy, Composable memory transactions, PPoPP 2005
    locator: the GHC implementation, in which a transaction that may be looping on an inconsistent view is validated by the runtime
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 2 (consistency during transactions) and Chapter 4 (Software transactional memory)
---

A **zombie transaction** (also a *doomed* transaction) is a running transaction that has already read an inconsistent state, a mix of values that no serial run of the transactions could produce, and so is certain to abort, but has not found this out yet. It goes on running the program on values that break the program's invariants. If the transactional memory checks reads only at commit, the zombie may never get there: it can loop forever, divide by zero, follow a pointer into freed memory, or, in an STM that writes in place, write through a garbage pointer. The committed transactions can still be [serializable](/serializability/); the damage happens in a transaction that will never commit. [Opacity](/opacity/) is the condition that rules zombies out: every transaction, also one that aborts, sees values that one serial order respecting real time explains. STMs such as [TL2](/tl2/), [NOrec](/norec/) and DSTM meet it by [validating](/transaction-validation/) during the run. Another fix, *sandboxing* (Dalessandro and Scott, PACT 2012), lets zombies exist but catches them before they can do harm.

## In plain words

Two numbers $x$ and $y$ are always equal: every transaction that changes one changes the other. A reader reads $x$, and it is 0. Then another transaction sets both to 1 and commits. The reader now reads $y$, and it is 1. The reader has seen $x = 0$ and $y = 1$, a state that never existed. If its next line is `while x != y: wait`, it waits forever, because it is waiting for a change in its own private copy of the values. An STM that checks the reads only at commit will never stop it, because it never reaches the commit. The reader is a zombie: dead already, but still walking.

## The idea

**Where zombies come from.** An STM with invisible reads does not tell a reader that a word it read has changed. The reader must check for itself. If it checks only at commit, then between a bad read and the commit it runs on a view that the program was never written to handle. That window is the life of the zombie.

**What a zombie can do.** It runs ordinary code on impossible values. The typical harms are:

- **Infinite loops.** A loop whose exit condition holds in every consistent state never ends. Example 1 below.
- **Faults.** A division by a value that is never zero in a consistent state, an array index out of range, a null pointer. Example 2.
- **Use of freed memory.** A committed transaction unlinks a node and frees it; a zombie that read the old link follows it into memory that has been reused. This is a [use-after-free](/use-after-free/), and the reason that STMs for unmanaged languages pair with [type-stable memory](/type-stable-memory/) or [epoch-based reclamation](/epoch-based-reclamation/).
- **Stray writes.** In an STM with [eager versioning](/eager-versioning/), writes go to memory at once; a zombie that computes an address from garbage can write anywhere, also outside the transactional heap where no undo log covers it. The same delayed effects are part of the [privatization](/privatization-safety/) problem.

**Fix 1: opacity.** Make every read come from one consistent state. The cost is a check per read. Incremental validation checks the whole read set at each read and costs $r(r+1)/2$ checks for $r$ reads. A [global version clock](/global-version-clock/), as in TL2, makes it one comparison per read. NOrec validates by value, only when a global counter has moved. A [multi-version STM](/multi-version-stm/) gives a reader an old consistent snapshot instead. With any of these, a transaction that would become a zombie aborts at the bad read.

**Fix 2: sandboxing.** Let the transaction run on an unchecked view, and stop it before an effect can escape. Dalessandro and Scott (PACT 2012) describe the parts: the runtime validates before any fault is delivered to the program (a fault on an inconsistent view becomes an abort, a fault on a consistent view is real), validates from time to time to stop infinite loops (for example from a timer, or on loop back edges), and validates before operations whose effects cannot be undone or contained, such as writes in place through computed addresses and indirect jumps. The committed transactions are serializable, because the commit validates. The promise is weaker than opacity: zombies exist, but they cannot do anything that a user can observe. In exchange, the STM need not check each read.

**Managed runtimes.** In a language with type safety and garbage collection, faults become exceptions and there is no stray write through a bad pointer, so loops are the main harm. The GHC implementation of Harris, Marlow, Peyton Jones and Herlihy validates a transaction that may be looping, which stops such a zombie.

**Hardware.** A [best-effort HTM](/best-effort-htm/) detects conflicts on the cache lines it has read, and aborts a transaction as soon as another core writes one of them. So a hardware transaction does not run on after a conflicting write, and zombies of this kind do not arise there.

## Examples

All runs come from the simulation on this page. The STM has three modes: validation at commit only, per-read checks against a version clock (opaque), and sandboxing with a check every $P$ loop iterations and before any fault escapes.

**1. A zombie that loops forever.** The invariant is $x = y = 0$. The reader runs `u ← x; v ← y; while u ≠ v: tick; return u`, and the writer adds 1 to both words. Schedule: the reader begins and reads $x = 0$; the writer runs to commit; the reader reads $y = 1$.

| Mode | What the reader does next |
|---|---|
| Commit only | Loops: still running after 500 steps, with no end in sight. The committed history (the writer alone) is serializable; the full history is not opaque. |
| Opaque | Aborts at the read of $y$, whose version is newer than its start time; the retry reads 1 and 1 and returns 1. No loop iteration runs. |
| Sandboxed, $P = 1, 4, 16$ | Runs exactly $P$ iterations, then the check finds that $x$ has changed and aborts; the retry returns 1. |

**2. A zombie that divides by zero.** The invariant is $y = x + 1$, from $x = 0$, $y = 1$. The reader runs `v ← y; u ← x; return 10 / (v - u)`, which is 10 in every consistent state. In the same kind of schedule it reads $y = 1$ (old) and $x = 1$ (new). Under commit-only validation the division by zero escapes from the transaction and crashes the run. Under opacity the read of $x$ aborts. Under sandboxing the fault is caught, the read set is validated, the validation fails, and the fault becomes an abort; the retry returns 10. If instead the data really is $x = y = 0$, a consistent but wrong state, the sandbox validates, finds the view consistent, and raises the fault: it belongs to the program, not to a zombie.

**3. Random runs.** 60 seeded runs of three transfers and two audits on three accounts of 10. Each audit adds up the accounts and then spins while the sum is not 30.

| Mode | Audit reads with a sum other than 30 | Runs in which an audit never ends |
|---|---|---|
| Commit only | 4 | 4 |
| Opaque | 0 | 0 |
| Sandboxed ($P = 4$) | 4 | 0 |

The exhaustive search over all schedules of one writer and one reader confirms each row: with commit-only validation some schedule has a zombie that spins without end, and some reader sees an inconsistent pair, while the committed transactions are always serializable; with opacity no loop iteration ever runs; with sandboxing no zombie runs more than $P$ iterations and no fault escapes.

**4. A non-example.** A transaction that reads a consistent state and then loses a conflict at commit aborts, but it was never a zombie: every value it acted on fit one serial order. Aborts are normal; zombies are aborts that came too late.

## Where it is used

- **Design of STMs.** DSTM validates all opened objects at each open, TL2 checks each read against a global clock, and NOrec revalidates by value whenever a global counter moves. Each choice is there to keep zombies out, and each has a cost that [transaction validation](/transaction-validation/) measures.
- **Correctness conditions.** Opacity was defined by Guerraoui and Kapałka (PPoPP 2008) in large part to name what is wrong with zombies: serializability of the committed transactions says nothing about the ones that abort.
- **STM for unmanaged languages.** In C and C++, a zombie can crash the process or corrupt memory outside the TM. Systems either stay opaque or sandbox, and pair either with safe memory reclamation.
- **Teaching and testing.** The two harms in the examples, a loop and a division by zero, are the standard way to show why an STM that is only serializable is not safe to program against.

## References
