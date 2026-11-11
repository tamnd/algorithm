---
tag: TNZZPN
kind: definition
slug: strong-atomicity
name: Strong atomicity
aliases:
- strong isolation
area: concurrency/transactional-memory
level: advanced
summary: A TM is strongly atomic if every load or store outside a transaction acts as a transaction of one access, so plain code never sees or changes the inside of a running transaction.
prereqs: [weak-atomicity]
see_also: [privatization-safety, opacity, hardware-transactional-memory, best-effort-htm, read-barrier, write-barrier, linearizability, sequential-consistency]
sources:
  - paper: doi:10.1109/L-CA.2006.18
    title: "Colin Blundell, E Christopher Lewis and Milo M. K. Martin, Subtleties of transactional memory atomicity semantics, IEEE Computer Architecture Letters 5(2), 2006"
    locator: the names strong atomicity and weak atomicity, and the examples where the choice changes the behavior of a program
  - paper: doi:10.1145/1250734.1250744
    title: "Tatiana Shpeisman, Vijay Menon, Ali-Reza Adl-Tabatabai, Steven Balensiefer, Dan Grossman, Richard L. Hudson, Katherine F. Moore and Bratin Saha, Enforcing isolation and ordering in STM, PLDI 2007, pp. 78 to 88"
    locator: the anomalies that strong atomicity removes, the barriers on non-transactional accesses, and the analyses that remove most of these barriers in a Java STM
  - paper: "Martín Abadi, Tim Harris and Mojtaba Mehrara, Transactional memory with strong atomicity using off-the-shelf memory protection hardware, PPoPP 2009"
    locator: the use of page protection to trap the non-transactional accesses that conflict with transactions
  - book: doi:10.1007/978-3-031-01728-5
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, 2010
    locator: Chapter 2 (Basic transactions, the section on weak and strong isolation) and Chapter 5 (Hardware-supported TM)
---

**Strong atomicity** (also called strong isolation) is the guarantee that a transaction is atomic and isolated with respect to all other code, not only other transactions. A load or store outside any transaction behaves as a transaction of one access: it cannot see a partial state of a running transaction, and a running transaction cannot see or lose it. Blundell, Lewis and Martin named it in 2006, together with [weak atomicity](/weak-atomicity/). Hardware TMs get it almost for free from cache coherence; software TMs must add a barrier to plain accesses, which is why few do.

## Definition

**Model.** The model is that of [weak atomicity](/weak-atomicity/): processes run transactions and plain accesses on a shared memory of words, and a plain access is concurrent with a transaction if it happens between the begin of the transaction and the end of its commit or abort (including write-back or rollback).

**Strong atomicity.** Take an execution and replace each plain access $a$ by a transaction $T_a$ that makes the one access $a$ and commits at once. A TM is *strongly atomic* if, for every execution, the resulting history of transactions satisfies the TM's correctness condition (for example [opacity](/opacity/), or serializability of committed transactions) with every $T_a$ counted as committed, and the serial order agrees with the program order of each process.

In words: there is one serial order of all committed transactions and all plain accesses that explains every value read. A plain read returns the value of the last write before it in that order, so it never returns a value written by a transaction that is still running or that aborted, and a plain write is never lost or reordered inside a transaction.

**What it does not say.** Strong atomicity says nothing about how far apart the parts of a program are in time. A program that is not race free still has many possible results, one for each serial order; strong atomicity only removes the results that no serial order explains. It also does not make two transactions see each other's partial results, so code that waits inside a critical section for another thread does not work as a transaction (see the last example).

## Examples and non-examples

**The anomalies of weak atomicity disappear.** Each anomaly on the [weak atomicity](/weak-atomicity/) page needs a plain access that falls inside the interval of a conflicting transaction. With strong atomicity:

| anomaly | program | results under strong atomicity |
|---|---|---|
| non-repeatable read | `atomic { a ← X; b ← X }` and `X ← 1` | $a = b$ |
| intermediate lost update | `atomic { X ← X + 1 }` and `X ← 10` | $X \in \{10, 11\}$ |
| intermediate dirty read | `atomic { X ← 1; X ← 2 }` and a plain read of $X$ | the read sees 0 or 2 |
| granular lost update | `atomic { word0 ← 1 }` and `word1 ← 5`, one block | word 1 is 5 |

The implementation on the weak atomicity page checks this table on a small TL2-like STM and an eager STM: with each plain access made to wait for the block lock, and each plain store made to give the block a new version, no interleaving of the two processes gives a result outside the third column.

**Privatization.** On a strongly atomic TM the privatization idiom is safe without a fence. The plain load of the privatizer waits until the worker's lock is released (after the write-back, or after the rollback of a doomed worker), and a plain store bumps the version, so a worker that has not yet validated aborts. See [privatization safety](/privatization-safety/).

**Hardware TM.** On a [best-effort HTM](/best-effort-htm/) a transaction keeps its read and write sets in the cache. A plain store from another core to a line in either set, or a plain load of a line in the write set, is a coherence conflict, and the hardware aborts the transaction. The transaction keeps its writes in the cache until commit, so a plain load never sees them. This gives strong atomicity for plain accesses at the granularity of cache lines (with false conflicts between different words in the same line).

**Software TM with barriers.** Shpeisman et al. add a barrier to each plain access in a Java STM. A plain read checks the ownership record of the location and waits if a transaction owns it; a plain write also updates the record so that transactions see the change. Static analysis and dynamic escape analysis remove the barriers on data that no transaction can touch, which makes the cost small on their benchmarks. Abadi, Harris and Mehrara instead use page protection: pages that transactions use are protected, so a plain access to them traps.

**Non-example: a weakly atomic STM.** TL2 and most STMs in C and C++ do not check plain accesses, so all anomalies in the table are possible for programs with races.

**Non-example: waiting inside an atomic block.** Thread 1 runs `atomic { while flag = 0 do skip; ... }` and thread 2 runs `flag ← 1` outside any transaction. With a lock in place of `atomic`, thread 1 leaves the loop once thread 2 sets the flag. Under strong atomicity the store of thread 2 must be ordered before or after the whole transaction of thread 1. If it is after, thread 1 never sees it and loops forever (a TM will abort and retry the transaction, but each attempt that starts before the store loops). Blundell, Lewis and Martin use examples of this kind to show that strong atomicity can change the behavior of code that was correct with locks.

## Related definitions

- **[Weak atomicity](/weak-atomicity/).** Only transactions are isolated from each other. Every strongly atomic TM is also weakly atomic.
- **Single global lock atomicity.** Every race-free program behaves as if each atomic block took one global lock. It is weaker than strong atomicity (no guarantee for racy programs) and is the usual target of language-level STMs.
- **[Linearizability](/linearizability/).** Strong atomicity makes each transaction behave like a single atomic operation on the whole memory, in the same way as linearizability does for operations of an object, and makes plain accesses part of the same order.
- **[Sequential consistency](/sequential-consistency/).** The definition above assumes a sequentially consistent base memory. On a weaker memory model, the TM must also order plain accesses around transactions, which needs fences.
- **[Privatization safety](/privatization-safety/).** A consequence of strong atomicity; a weakly atomic TM must provide it by other means.

## References
