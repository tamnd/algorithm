---
tag: 70FJV6
kind: technique
slug: transactional-lock-elision
name: Transactional lock elision
aliases:
- TLE
- speculative lock elision
- lock elision
area: concurrency/transactional-memory
level: advanced
summary: Run the critical section of a lock as a hardware transaction that reads the lock but does not take it, so threads on different data run in parallel; on repeated aborts, take the lock.
prereqs: [best-effort-htm, spin-lock]
see_also: [intel-tsx, hardware-transactional-memory, hybrid-transactional-memory, mutex, readers-writer-lock, critical-section, exponential-backoff, contention-management]
sources:
  - paper: doi:10.1109/MICRO.2001.991127
    title: "Ravi Rajwar and James R. Goodman, Speculative lock elision: enabling highly concurrent multithreaded execution, MICRO 2001, pp. 294 to 305"
    locator: the idea of eliding a lock, the silent store pair that acquires and releases it, speculative execution of the critical section, and the fallback to the lock after a failure
  - paper: doi:10.1145/605397.605399
    title: "Ravi Rajwar and James R. Goodman, Transactional lock-free execution of lock-based programs, ASPLOS 2002, pp. 5 to 17"
    locator: transactional lock removal (TLR), which resolves conflicts by timestamps so that the oldest critical section wins, and the lock kept in shared state so that a write to it aborts the elided sections
  - paper: doi:10.1145/1508244.1508263
    title: "Dave Dice, Yossi Lev, Mark Moir and Daniel Nussbaum, Early experience with a commercial hardware transactional memory implementation, ASPLOS 2009, pp. 157 to 168"
    locator: experiments with transactional lock elision on the Rock processor
  - paper: doi:10.1145/2576793
    title: "Andi Kleen, Scaling existing lock-based applications with lock elision, Communications of the ACM 57(3), 2014, pp. 52 to 56"
    locator: the lemming effect, the fix of retrying only when the lock is free, and the adaptive elision of the GNU C library
  - book: "Intel 64 and IA-32 Architectures Software Developer's Manual, Volume 1, Chapter 16, Programming with Intel Transactional Synchronization Extensions"
    locator: Hardware Lock Elision with the XACQUIRE and XRELEASE prefixes, and the RTM abort status
  - book: "Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, Morgan and Claypool, 2010, doi:10.1007/978-3-031-01728-5"
    locator: the section on speculative lock elision and transactional lock removal
---

**Transactional lock elision** (TLE) runs the critical section of an ordinary lock as a hardware transaction. The transaction reads the lock word to check that it is free, but does not write it, so threads whose critical sections touch different data run in parallel, and only real data conflicts make them wait. If the transaction aborts too often, or for a reason that a retry will not fix, the thread takes the lock as usual. Rajwar and Goodman proposed the idea as speculative lock elision in 2001; it became the main use of [Intel TSX](/intel-tsx/) and other [best-effort HTM](/best-effort-htm/).

## In plain words

Many programs protect a large table with one lock, although two threads rarely change the same entry. The lock makes them take turns anyway.

With lock elision, a thread does not take the lock. It looks at the lock, sees that it is free, and does its work inside a hardware transaction. If another thread also works in the table on a different entry, both finish, and neither waited. If they touch the same entry, the hardware aborts one, and it tries again.

Looking at the lock is not optional. A thread that cannot use a transaction takes the lock for real. Because every transaction has read the lock, the hardware aborts all of them at that moment, so nobody sees the half-done work of the lock holder.

The program does not change. Only the code of the lock changes.

## When it applies

- **The hardware has transactions.** Lock elision needs a [hardware transactional memory](/hardware-transactional-memory/) that detects conflicts on the lines it reads and writes. A best-effort HTM is enough, because the lock itself is the fallback.
- **Critical sections are short and touch little data.** The data must fit in the read and write sets of the hardware. Large sections abort on capacity every time.
- **Conflicts on data are rare.** Elision helps when the lock is coarse and the threads usually touch different data. If the threads really do write the same words, they abort each other and the lock is faster.
- **Critical sections do nothing that a transaction cannot undo.** A system call, I/O, or a page fault aborts a transaction; such sections always run under the lock.
- **The lock word can be read and tested.** The elided path must be able to tell if the lock is held, and the lock must be released by a write that the coherence protocol sees. A [spin lock](/spin-lock/) or the fast path of a [mutex](/mutex/) works.

## The template

```pseudo id=main
ELIDED-CRITICAL-SECTION(lock, body)
L1  for try ← 1 to MAX-TRIES do
L2      wait until lock is free
L3      BEGIN-TRANSACTION
L4      if lock is held then ABORT(LOCK-BUSY)   ▷ the lock is now in the read set
L5      run body
L6      COMMIT; return
L7      on abort with status s:
L8          if s has no retry bit and s is not LOCK-BUSY then leave the loop
L9  acquire lock
L10 run body
L11 release lock
```

Line 4 is the key line. It reads the lock inside the transaction, so the lock is in the read set. A thread that acquires the lock on line 9 writes the lock word; the coherence protocol sends that write to every processor that holds the line, and each transaction that has read the lock aborts. While one thread holds the lock, no transaction can commit, so the lock path and the transactional path never overlap. Rajwar and Goodman state this for TLR: the lock stays in shared state in the caches, so "any write to the lock triggers invalidations thus automatically informing other participating processors".

Line 2 waits outside the transaction. Without it, a thread that starts while the lock is held aborts on line 4 at once, retries, aborts again, and soon uses all its tries; this is the lemming effect described below.

Line 8 is the retry policy. A conflict sets the retry bit, and a second try can succeed. A capacity abort has no retry bit, and the same section will overflow again, so the thread goes to the lock at once. An abort because the lock was busy is not a reason to give up: the thread waits on line 2 and tries again.

*Example: what goes wrong without line 4.* $P_0$ cannot use a transaction and takes the lock; $P_1$ elides the lock but does not read it. Both add 1 to a counter $c = 0$.

| step | $P_0$ (lock path) | $P_1$ (transaction, lock not read) | $c$ in memory |
|---|---|---|---|
| 1 | acquire the lock | | 0 |
| 2 | read $c = 0$ | | 0 |
| 3 | | begin; read $c = 0$; write $c = 1$ to its buffer | 0 |
| 4 | | commit | 1 |
| 5 | write $c = 1$ | | 1 |
| 6 | release the lock | | 1 |

One increment is lost. $P_1$ never conflicted with anything that the hardware watches: $P_0$ read $c$ before $P_1$ began, and $P_0$ wrote $c$ after $P_1$ committed. With line 4, step 3 reads the lock as held and aborts; or, if $P_1$ begins before step 1, the acquire in step 1 aborts it. The tests of the implementation explore every interleaving of this pair: without line 4 some schedules end with $c = 1$, and with it every schedule ends with $c = 2$.

**Why it is correct.** Consider any execution in which every transactional critical section reads the lock on line 4, and the lock is a correct mutual exclusion lock among the threads on lines 9 to 11. Take a transaction $T$ that commits and a lock holder $H$. $T$ read the lock as free, so $T$ read it before $H$ acquired it or after $H$ released it. In the first case, if $T$ had not committed before $H$ acquired the lock, the write of the acquire would have aborted $T$, since the lock is in its read set; so $T$ committed before $H$ began. In the second case $T$ began after $H$ ended. So every committed transaction is wholly before or wholly after every lock holder. Committed transactions are atomic and serializable among themselves by the HTM, and lock holders are serialized by the lock, so the whole execution is equivalent to running the critical sections one at a time. $\blacksquare$

**Progress.** Each call makes at most MAX-TRIES hardware attempts and then takes the lock, so if the lock is starvation-free, every call ends.

## Classic examples

- **Hardware Lock Elision in Intel TSX.** The XACQUIRE prefix on the instruction that takes a lock and the XRELEASE prefix on the instruction that releases it made the processor elide the lock in hardware, as in SLE: the acquiring write was not done, the line of the lock joined the read set, and old processors ignored the prefixes. Intel has since removed HLE; see [Intel TSX](/intel-tsx/).
- **Mutexes of the C library.** The GNU C library contains RTM-based elision for its [mutex](/mutex/) code, with an adaptive policy that skips elision for a while on a lock whose transactions keep aborting. Kleen describes this design. In recent releases the feature is off unless the user turns it on with a tunable.
- **The fallback of an HTM runtime.** The global lock behind [best-effort HTM](/best-effort-htm/) in a TM runtime is elided in exactly this way, and a [hybrid TM](/hybrid-transactional-memory/) uses a refined form of it in which the fallback is a software transaction.
- **Rock.** Dice, Lev, Moir and Nussbaum used TLE on Sun's Rock processor to run code written with locks, in C++ and in Java, as transactions.

## Variations

- **Speculative lock elision (SLE).** In the original proposal, the hardware finds a pair of stores to the lock (one that takes it and one that restores the old value) and elides both, with no new instructions. The lock is read, so it is in the cache in shared state; a conflict or a resource limit makes the processor restart and take the lock.
- **Transactional lock removal (TLR).** Rajwar and Goodman extended SLE in 2002 so that a data conflict does not send a thread to the lock. Each critical section has a timestamp, and on a conflict the oldest wins while the younger waits. With enough resources this gives starvation freedom without ever taking the lock.
- **Hardware versus software elision.** HLE needs no change of code at all; RTM-based elision puts the template into the lock library, where software can choose the retry policy and keep statistics.
- **Adaptive elision.** Count aborts per lock and stop eliding a lock that rarely commits, then try again after a while. This is the policy of the GNU C library and of many others.
- **Better fallbacks.** Afek, Levy and Morrison (2014) send threads that abort on a conflict to an auxiliary lock, so that they retry one at a time while the main lock stays free and other threads keep eliding it. Other work uses an [STM](/software-transactional-memory/) as the fallback instead of the lock.
- **Readers-writer locks.** Readers can elide the lock while a writer takes it, or writers can elide it too; the rules of the template are the same.

## Pitfalls

- **Not reading the lock.** A transaction that does not read the lock can commit in the middle of a lock holder's critical section, as in the example. The tests find this run in the model.
- **The lemming effect.** When one thread takes the lock, all elided transactions abort. If they retry at once, they find the lock still held, abort again, use up their tries, and take the lock themselves; each of them then aborts the transactions of others, and the program can run serialized for a long time. Kleen describes this and gives the fix in line 2: retry only when the lock is free, and wait for it outside the transaction. The name comes from Dice and colleagues at Sun. In the model of this page, with one thread that always takes the lock and three threads that elide it on disjoint data, 600 random schedules sent 429 of 900 elided sections to the lock when they retried at once, and none when they waited first.
- **Too many or too few tries.** A large retry count wastes time on sections that will never commit; a count of 1 gives up after one conflict. Use the status: stop on capacity, retry a few times on conflict.
- **Unlocking an elided lock.** The release must know if the lock was elided. With RTM the code can test whether it is inside a transaction (XTEST) or whether the lock word is free; a lock that records its owner may find the owner field empty after elision.
- **Critical sections that cannot abort.** A section that does I/O always aborts. Elision then only adds the cost of the failed try.
- **Locks with fairness.** A [ticket lock](/ticket-lock/) or a queue lock changes its word on every acquire, and its "free" test is more complex. Elision of such locks must test the right condition on line 4.

## Exercises

1. Show that, without line 2, a thread can abort with LOCK-BUSY on every try even though the lock is free most of the time. Describe a schedule.
2. Prove that line 2 is not needed for correctness: the template without line 2 still never lets a transaction overlap a lock holder.
3. A critical section reads 10 lines and writes 2. The hardware read set holds 8 lines. What does the retry policy of line 8 do, and how many tries does it waste?
4. Change the template so that a thread that aborts on conflict 3 times in a row takes the lock, but a thread that aborts because the lock was busy never counts that abort. Does the lemming effect come back?
5. Explain why TLR needs timestamps but SLE does not. *Hint.* Think about what each does on a data conflict.

## References
