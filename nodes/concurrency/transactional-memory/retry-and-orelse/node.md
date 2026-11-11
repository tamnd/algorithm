---
tag: E1CEZX
kind: concept
slug: retry-and-orelse
name: Retry and orElse
aliases:
- composable blocking transactions
- conditional synchronization in STM
area: concurrency/transactional-memory
level: advanced
summary: "Two STM constructs: retry aborts a transaction and blocks it until a location it read changes; orElse tries one alternative and runs a second if the first retries."
prereqs: [transaction, condition-variable, read-set-and-write-set]
see_also: [nested-transactions, monitor, semaphore, software-transactional-memory, transaction-abort, tl2, lazy-versioning, deadlock]
sources:
  - paper: doi:10.1145/1065944.1065952
    title: "Tim Harris, Simon Marlow, Simon Peyton Jones and Maurice Herlihy, Composable memory transactions, PPoPP 2005, pp. 48 to 60"
    locator: the sections that define retry and orElse (with the left bias of orElse) and that describe their implementation in GHC
  - paper: doi:10.1145/1378704.1378725
    title: "Tim Harris, Simon Marlow, Simon Peyton Jones and Maurice Herlihy, Composable memory transactions, Communications of the ACM 51(8), 2008, pp. 91 to 100"
    locator: the shorter journal version with the same constructs
  - paper: doi:10.1145/949305.949340
    title: "Tim Harris and Keir Fraser, Language support for lightweight transactions, OOPSLA 2003, pp. 388 to 402"
    locator: conditional critical regions, the guarded atomic blocks that came before retry
  - book: doi:10.1007/978-3-031-01728-5
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, 2010
    locator: Chapter 3 (Building on basic transactions, the section on condition synchronization)
---

**retry** and **orElse** are two constructs that let a transaction wait for a condition and choose between alternatives without locks or condition variables. `retry` says "this transaction cannot go on in the current state": the system aborts it and runs it again only after some location it read has changed. `orElse` runs a first alternative and, if that alternative calls `retry`, discards its effects and runs a second one. Harris, Marlow, Peyton Jones and Herlihy introduced both in 2005 in the STM of the Glasgow Haskell Compiler, where they make blocking operations composable.

## In plain words

A transaction that takes an item from an empty queue cannot finish. With locks, the code would wait on a condition variable, and the programmer must remember which signal wakes it. With `retry`, the transaction just gives up. The system knows exactly what the transaction looked at, so it puts the thread to sleep and wakes it only when one of those things changes. No signal is needed, and none can be forgotten.

`orElse` joins two such operations. "Take from queue one, or else from queue two" tries the first; if that one would block, its changes vanish and the second runs. If both would block, the thread sleeps until either queue changes. Because the parts do not need to know about each other, small blocking operations combine into larger ones, which is hard with locks.

## The idea

### Semantics

The constructs, in the notation of Haskell STM:

```
atomically : STM a → IO a                 ▷ run a transaction
retry      : STM a                        ▷ abort and wait
orElse     : STM a → STM a → STM a        ▷ left-biased choice
```

- `atomically t` runs $t$ as one transaction. If $t$ calls `retry`, the effect is as if the transaction had not started; the thread then waits and runs $t$ again. A run of $t$ that commits never called `retry`.
- `orElse t₁ t₂` runs $t_1$. If $t_1$ returns a value, that is the value of the whole. If $t_1$ calls `retry`, all writes of $t_1$ are undone and $t_2$ runs. If $t_2$ also calls `retry`, the `orElse` calls `retry`. So `orElse` is left-biased: if both alternatives can go on, the first wins.
- `retry` is a unit for `orElse`: `orElse retry t` behaves like $t$, and `orElse t retry` behaves like $t$.

The usual helper is `check b = if b then return () else retry`, which turns a condition into a guard. With it, `atomically (do { v ← readTVar q; check (v > 0); writeTVar q (v − 1) })` is a blocking take, like a [semaphore](/semaphore/) wait.

### When to wake up

A transaction that called `retry` saw a state in which it could not go on. Running it again in the same state gives the same answer, because transactions are deterministic functions of the values they read. So the implementation waits until at least one location in the read set of the failed attempt has a newer value:

```
on retry in attempt A:
    validate A                     ▷ if A saw an inconsistent state, rerun at once
    for each location ℓ in the read set of A:
        add this thread to the wait queue of ℓ
    sleep
on commit of a transaction that writes ℓ:
    wake every thread in the wait queue of ℓ
```

In GHC each transactional variable has a wait queue, and a committing writer wakes the threads in the queues of the variables it wrote. A woken transaction starts again from the beginning. If the read set is empty, the transaction waits forever, which is the correct meaning of a transaction that can never go on.

### orElse as a nested transaction

The first alternative of `orElse` runs as a [closed nested transaction](/nested-transactions/): its writes go to a private log that is dropped if it calls `retry`. Its reads are not dropped. They stay in the read set of the enclosing transaction, for two reasons. The choice of the second branch depends on the fact that the first branch could not go on, so if a value that the first branch read changes before the commit, the transaction must be validated again. And if both branches retry, the thread must wake when a location read by either branch changes: the wait set is the union of the read sets of both alternatives.

On a TL2-like STM with a redo log, the nested log is cheap: copy the redo log before the first branch and restore the copy if the branch retries.

### What the constructs replace

With a [monitor](/monitor/), a blocking take is a loop `while empty: wait(nonEmpty)` and every put must `signal(nonEmpty)`. A missing signal is a lost wake-up, and a thread that waits inside two nested monitors can [deadlock](/deadlock/). A take from one of two queues needs a new lock that covers both queues. With `retry` the wake-up is automatic and exact, and with `orElse` the choice is written from the two existing operations. Harris and Fraser had earlier proposed conditional critical regions, atomic blocks with a guard condition; `retry` moves the guard to any point inside the transaction, so it composes.

## Examples

**Waking only for the right write.** Process 0 runs `atomically (take q)` with $q = 0$. Process 1 runs `atomically (z ← 1)` and later `atomically (q ← 1)`.

| step | process 0 | process 1 | read set of process 0 |
|---|---|---|---|
| 1 | read $q = 0$; `retry`; sleep on $\{q\}$ | | $\{q\}$ |
| 2 | (still asleep: $z$ is not in the read set) | commit $z \leftarrow 1$ | $\{q\}$ |
| 3 | | commit $q \leftarrow 1$, wake the waiters of $q$ | $\{q\}$ |
| 4 | run again: read $q = 1$, write $q \leftarrow 0$, commit | | $\{q\}$ |

The implementation for this page checks all interleavings of this program on a small TL2 model: in every run where process 0 sleeps, it wakes only after the version of $q$ has changed, and there are runs where $z$ changes while it sleeps without waking it. If process 1 never writes $q$, process 0 stays asleep in every run.

**Take from either queue.** `orElse (take q₁) (take q₂)` with $q_1 = q_2 = 0$ sleeps on $\{q_1, q_2\}$. A put to either queue wakes it, and it then takes from that queue. If the first branch had written to a log before it called `retry`, that write is gone. If both queues hold items, it takes from $q_1$.

**A bounded buffer.** `put` checks `v < capacity` and `take` checks `v > 0`, both with `check`. Random runs on the model with up to two producers, two consumers, a capacity of one or two, and `orElse` over two buffers, always finish with every item taken, which means no wake-up was lost.

**Choosing a default.** `orElse (take q) (return Nothing)` is a non-blocking take: it returns at once if the queue is empty. This turns any blocking operation into a polling one without changing it.

## Where it is used

- The STM of the Glasgow Haskell Compiler (`Control.Concurrent.STM`) provides `retry`, `orElse` and `check`, and its library of transactional queues and channels is built on them.
- ScalaSTM, a library STM for Scala, provides `retry` with the same wake-up rule and `orAtomic` as its form of `orElse`.
- Other STMs that cannot track the read set of a retrying transaction approximate `retry` by aborting and sleeping for a timeout, which is correct but wakes too early or too late.

## References
