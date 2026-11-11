---
tag: Z003W9
kind: concept
slug: transaction-irrevocability
name: Transaction irrevocability
aliases:
- irrevocable transactions
- inevitable transactions
- inevitability
area: concurrency/transactional-memory
level: advanced
summary: An irrevocable transaction is guaranteed never to abort, so it can do I/O and other actions that cannot be undone; a TM can allow at most one at a time.
prereqs: [transaction, transaction-abort, readers-writer-lock]
see_also: [contention-management, open-nested-transactions, transactional-lock-elision, best-effort-htm, hybrid-transactional-memory, retry-and-orelse, encounter-time-locking, mutex]
sources:
  - paper: doi:10.1145/1378533.1378584
    title: "Adam Welc, Bratin Saha and Ali-Reza Adl-Tabatabai, Irrevocable transactions and their applications, SPAA 2008, pp. 285 to 296"
    locator: the irrevocable mode of McRT-STM, the rule that only one transaction is irrevocable at a time, and the designs that let other transactions run alongside it
  - paper: "Michael F. Spear, Maged M. Michael and Michael L. Scott, Inevitability mechanisms for software transactional memory, 3rd ACM SIGPLAN Workshop on Transactional Computing (TRANSACT), 2008"
    locator: the term inevitability and the comparison of mechanisms, from a global lock that runs the inevitable transaction alone to mechanisms that let other transactions commit
  - book: doi:10.1007/978-3-031-01728-5
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, 2010
    locator: Chapter 3 (Building on basic transactions, the section on irrevocability and I/O)
---

An **irrevocable transaction** (also called an inevitable transaction) is a transaction that the TM guarantees will commit: once it becomes irrevocable, it is never aborted and never re-executed. This lets a transaction perform actions that cannot be rolled back, such as I/O, system calls or calls into code that the TM does not instrument. Because two irrevocable transactions that conflict could not both commit, a TM allows **at most one irrevocable transaction at a time**, and every conflict with it must be resolved against the other transaction. Welc, Saha and Adl-Tabatabai, and Spear, Michael and Scott, studied the mechanisms in 2008.

## In plain words

A transaction normally runs on the understanding that it may be thrown away and run again. That is fine for reads and writes of memory, but not for printing a page or sending a message: those cannot be taken back, and running them twice is wrong.

An irrevocable transaction is one that has been promised it will finish. From the moment it gets the promise, anything that gets in its way must step aside, wait or be thrown away instead. Only one transaction can hold the promise at any time: if two promised transactions blocked each other, the system could not keep both promises. The cost is that other transactions lose some freedom while the promised one runs.

## The idea

### Why only one

Let $T_1$ and $T_2$ both be irrevocable and run at the same time. $T_1$ reads $x$ and then writes $y$; $T_2$ reads $y$ and then writes $x$; each read happens before the other's write. Any serial order puts one of them first, say $T_1$; then $T_2$ should have read the value of $y$ that $T_1$ wrote, but it read the old value. So $T_2$ must abort, which breaks its promise, and the case where $T_2$ comes first is the same with the roles swapped. Waiting does not help, because both reads have already happened. The TM cannot know the access sets of transactions in advance, so it cannot pick in advance two irrevocable transactions that are safe together. Hence the rule: one irrevocable transaction at a time, taken through a global token.

### The template

```
become_irrevocable(T):
    acquire the irrevocability token        ▷ wait if another holds it
    validate T                               ▷ if T is already doomed, abort it now (the last abort it can have)
    switch T to irrevocable mode
irrevocable mode:
    every read and write takes a lock that other transactions respect   ▷ or: other transactions may not commit
    on a conflict with another transaction U: abort U, or make U wait
commit(T): write back (or keep the in-place writes), release locks, release the token
```

A transaction can start irrevocable, or become irrevocable in the middle, just before its first unsafe action. In the second case it must validate at that point: a transaction that has already seen an inconsistent state must abort before the promise, because after it there is no way back.

### Mechanisms

The mechanisms differ in how much the other transactions can do while one is irrevocable.

- **Serial irrevocable mode.** The token is a global [readers-writer lock](/readers-writer-lock/): every transaction holds it in read mode, and the irrevocable transaction holds it in write mode, so it runs alone. This is simple and needs no instrumentation of the irrevocable code, so the code can call any library. It stops all other transactions.
- **Writers wait.** Other transactions may run, but they may not commit while the irrevocable transaction runs (or may not commit writes to locations it accessed). The irrevocable transaction needs instrumentation of its reads, so that later writers see them, but no other transaction can change what it read.
- **Lock everything it touches.** The irrevocable transaction takes encounter-time locks on its reads and writes (as in [encounter-time locking](/encounter-time-locking/)); the [contention manager](/contention-management/) always resolves a conflict with it by aborting or delaying the other transaction. Other transactions can run and commit freely on unrelated data. Welc, Saha and Adl-Tabatabai describe designs of this kind in McRT-STM.
- **Read filters.** Spear, Michael and Scott also compare mechanisms where writers check a summary of the reads of the inevitable transaction before they commit.

Spear, Michael and Scott found that the best choice depends on the workload; when irrevocable transactions are rare, the simple serial mode costs little.

### Interactions

- An irrevocable transaction cannot call [retry](/retry-and-orelse/) or an explicit abort; a TM must reject or forbid this.
- An irrevocable transaction never runs the compensations of [open nested](/open-nested-transactions/) children, since it never aborts; a transaction that has no compensation for an action must become irrevocable before it.
- With hardware TM, a hardware transaction cannot be irrevocable, because the hardware can abort it at any time (on capacity overflow, for example). Systems therefore run the irrevocable part on the fallback path, usually under a global lock. The fallback lock of [transactional lock elision](/transactional-lock-elision/) is in effect an irrevocable mode: a thread that holds it runs alone and cannot abort.

## Examples

**Output inside a transaction.** `atomic { x ← x + 1; print(x) }`. If the transaction prints and then aborts, the retry prints again and the output shows a value that was never committed. Making the transaction irrevocable before `print` fixes both problems.

**Calling a library.** A transaction calls a function from a library compiled without TM support. The TM cannot log its writes, so it switches the transaction to serial irrevocable mode first. The GCC TM runtime (libitm) behaves in this way for code that is not transaction safe: it switches to a serial irrevocable mode.

**Long or large transactions.** A transaction that has aborted many times, perhaps because it is long and always loses conflicts, can be run as irrevocable to ensure progress. This is a common last resort in contention managers and in hybrid TMs, where a transaction that overflows the hardware's capacity again and again falls back to a serial path.

**Two irrevocable requests.** Thread 1 runs `atomic { read x; become_irrevocable; write y; output }` and thread 2 runs the mirror image. With the token, the second thread to ask waits until the first commits; then it validates, finds that $x$ or $y$ has changed, and aborts once before it becomes irrevocable. No promise is broken.

## Where it is used

- Most STMs for C and C++ (including the GCC runtime that implements the transactional language constructs of the C++ Transactional Memory Technical Specification) provide a serial irrevocable mode for unsafe code.
- McRT-STM (Intel) used irrevocability for I/O and for calls to uninstrumented code, as described by Welc et al.
- Lock-elision schemes and hybrid TMs use a global fallback lock that plays the role of the irrevocability token.

## References
