---
tag: TVHXNT
kind: concept
slug: race-condition
name: Race condition
aliases: [race hazard]
area: concurrency/mutual-exclusion
level: intro
summary: A bug in which the result of a concurrent program depends on how the steps of its processes interleave. A data race is a related but different defect.
history:
  year: 1965
  people: [Edsger W. Dijkstra]
  note: Dijkstra stated the critical section problem in 1965 to stop the interference of concurrent processes on shared variables. Netzer and Miller separated general races from data races in 1992.
see_also: [critical-section, mutual-exclusion-problem, mutex, sequential-consistency, linearizability, fetch-and-add, compare-and-swap, peterson-algorithm]
sources:
  - paper: doi:10.1145/130616.130623
    title: Robert H. B. Netzer and Barton P. Miller, What are race conditions? Some issues and formalizations, ACM Letters on Programming Languages and Systems 1(1), 1992, pages 74 to 88
    locator: the definitions of general races and data races, and of feasible and apparent races
  - url: "https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf"
    title: ISO/IEC 9899:201x (C11) committee draft N1570
    locator: Section 5.1.2.4, Multi-threaded executions and data races, paragraphs 4 and 25
  - paper: doi:10.1145/1375581.1375591
    title: Hans-J. Boehm and Sarita V. Adve, Foundations of the C++ concurrency memory model, PLDI 2008, pages 68 to 78
    locator: the data race definition, the data-race-free model and its sequential consistency guarantee
  - url: "https://docs.oracle.com/javase/specs/jls/se17/html/jls-17.html"
    title: The Java Language Specification, Java SE 17 edition, Chapter 17, Threads and Locks
    locator: Sections 17.4.1 (conflicting accesses), 17.4.5 (happens-before order and data races), 17.4.8 (causality), 17.7 (long and double)
  - paper: doi:10.1145/265924.265927
    title: Stefan Savage, Michael Burrows, Greg Nelson, Patrick Sobalvarro and Thomas Anderson, Eraser, a dynamic data race detector for multithreaded programs, ACM Transactions on Computer Systems 15(4), 1997
    locator: the lockset algorithm
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 1, Introduction, and Chapter 2, Mutual Exclusion
---

A race condition is a bug in which the result of a concurrent program depends on the order in which the steps of its processes interleave, and some of these orders give a wrong result. The classic case is a lost update: two processes each read a counter, add one, and write it back, and the counter goes up by one instead of two. A data race is a different, narrower defect: two unordered conflicting accesses to the same memory location, at least one of them a plain write. Each one can happen without the other.

## In plain words

Two clerks share one ledger. Each clerk reads the total, adds a new sale on scrap paper, and writes the new total back. If both clerks read the total before either writes, the second write erases the first sale. Nothing is wrong with either clerk's steps. The bug is in the order in which the steps of the two clerks mix.

The program is correct for some orders and wrong for others. A test can pass a thousand times and fail on the next run, because the order depends on timing that the program does not control. The fix is to make the read and the write one step that no other clerk can split, or to let only one clerk use the ledger at a time.

## The idea

**Model.** There are $n$ processes $p, q, \ldots$ that run asynchronously: each takes steps at its own speed. A step is one access to shared memory: a read, a write, or one atomic read-modify-write such as [fetch-and-add](/fetch-and-add/) or [compare-and-swap](/compare-and-swap/). Unless the text says otherwise, the memory is [sequentially consistent](/sequential-consistency/): a run is one interleaving of the steps of all processes, and each read returns the last value written to its location in that interleaving.

**Race condition.** A program has a race condition if two runs that differ only in the interleaving of steps give different results, and at least one of the results breaks the specification of the program. Netzer and Miller call the underlying event a *general race*: two accesses to the same shared object whose order is not fixed by the synchronization of the program. A general race is a bug only when one of its orders is wrong. Many races are intended, for example two processes that compete for a lock.

**Data race.** Two accesses *conflict* if they touch the same memory location and at least one of them writes. A run has a *data race* if it holds two conflicting accesses from different processes, at least one of them a plain (non-atomic) access, and no synchronization orders one before the other. In a sequentially consistent run, this means that the two accesses can be next to each other in some interleaving (Boehm and Adve 2008).

**What the languages say.** The two notions matter because modern languages treat a data race as a contract violation:

- C11 defines conflicting evaluations in Section 5.1.2.4 paragraph 4 of N1570, and says in paragraph 25 that an execution contains a data race if it contains two conflicting actions in different threads, at least one of which is not atomic, and neither happens before the other. Any such data race results in undefined behavior. C++11 has the same rule in its section on multi-threaded executions.
- Java defines a data race in JLS Section 17.4.5 as two conflicting accesses that happens-before does not order. A program whose sequentially consistent executions are all free of data races is *correctly synchronized*, and all its executions then appear sequentially consistent. A Java program with a data race still has a defined meaning, but it is weak: a read may see a stale or reordered value, within the limits of the causality rules of Section 17.4.8. A plain write to a 64-bit `long` or `double` can even be split into two 32-bit writes (Section 17.7). Accesses to `volatile` fields never form a data race.

So in C and C++ a data race makes the whole program undefined, and in Java it gives weak, hard to predict values. In both, a program without data races behaves as if it were sequentially consistent. This "data-race-free implies sequential consistency" contract is the base of the C++ model (Boehm and Adve 2008). Note what the contract does not give: a data-race-free program can still have a race condition.

**How to remove a race condition.** Make the steps that must not be split into one atomic step, as a [fetch-and-add](/fetch-and-add/) does for a counter, or put them in a [critical section](/critical-section/) that at most one process runs at a time. The second way leads to the [mutual exclusion problem](/mutual-exclusion-problem/) and to the [mutex](/mutex/).

## Examples

**The lost update.** Each process runs `counter := counter + 1` as two steps, a read into a local register $r$ and a write of $r + 1$. The counter starts at 0. This interleaving loses one update:

| step | process | action | local $r$ | counter |
|---|---|---|---|---|
| 1 | $p$ | read counter | $r_p = 0$ | 0 |
| 2 | $q$ | read counter | $r_q = 0$ | 0 |
| 3 | $p$ | write $r_p + 1$ | | 1 |
| 4 | $q$ | write $r_q + 1$ | | 1 |

If $p$ runs both of its steps before $q$ starts, the counter ends at 2. The test file runs all 6 interleavings of the 4 steps: the final value is 1 or 2. With three processes the final value can be 1, 2 or 3. In C or C++ this code also has a data race, so the program is undefined and the compiler may produce stranger results than a lost update.

**A race condition without a data race.** Write the increment with an atomic load and an atomic store, for example `atomic_load` and `atomic_store` in C11. Each access is now atomic, so there is no data race and the program is defined. The update is still lost in the same interleaving as above, because the load and the store are two steps. The same holds for a check-then-act: a bank account holds 150, and two processes each run "if balance ≥ 100 then balance := balance − 100 and pay out 100" with atomic accesses. If both load 150 before either stores, both pay out, and the bank pays 200 from an account that held 150. The test file finds exactly two final states: (balance 50, paid 100) and (balance 50, paid 200).

**A data race without a race condition.** Two threads each set a plain shared flag `done := true`. The final value is `true` in every interleaving, so the result does not depend on the order. It is still a data race: in C11 the program has undefined behavior, and a compiler may assume that no other thread writes `done`. The fix is to make `done` an atomic variable, which costs little.

**The fixes.** A single fetch-and-add, or a read and a write inside a critical section guarded by a [test-and-set](/test-and-set/) lock, gives the final value 3 for three processes in every interleaving, and the checker finds no data race.

## Where it is used

The notion is the reason for the whole [mutual exclusion](/mutual-exclusion-problem/) area. Dijkstra (1965) stated the critical section problem so that processes that share variables do not interfere with each other. Every lock on this site, from [Peterson's algorithm](/peterson-algorithm/) to the [mutex](/mutex/) of an operating system, exists to remove race conditions on the data it guards. Lock-free objects remove them with atomic read-modify-write steps and a correctness condition such as [linearizability](/linearizability/).

Race detection is a large field of tools. Dynamic detectors watch one run and report two accesses that no lock or happens-before edge orders: Eraser (Savage et al. 1997) checks that each shared variable is always guarded by some common lock, and later tools such as ThreadSanitizer use happens-before. Netzer and Miller (1992) point out that a detector that looks at one run sees only *apparent* races, and that some of them cannot happen in any real run (they are not *feasible*). [Model checkers](/deadlock-freedom-checking/) look at every interleaving of a small program instead.

The tests of this page do the same on a small scale. Each process is a Python generator that yields one shared memory step at a time, and a deterministic explorer runs every interleaving. Python threads are not used, because they cannot show a race on demand. The function `outcomes` returns the set of final values over all interleavings. The function `data_race` reports a state in which two processes are about to make conflicting accesses to one address and at least one of them is plain. An atomic load is modelled as a fetch-and-add of 0 and an atomic store as a swap.

**Pitfalls.**

- A race condition is a property of interleavings, so tests that pass do not show that it is absent. The bad interleaving can need a rare timing.
- Removing data races by making every access atomic does not remove race conditions. The steps that must happen together must be one atomic step or one critical section.
- "Benign" data races in C or C++ are not benign: the program is undefined, and an optimizing compiler can turn a race on a flag into an infinite loop or a torn read.
- On real hardware a program with a data race can also see orders that no interleaving gives, for example under TSO on x86. The page on [Peterson's algorithm](/peterson-algorithm/) shows a lock that fails this way.

## References
