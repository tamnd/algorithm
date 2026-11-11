---
tag: KB7E0K
kind: concept
slug: nested-transactions
name: Nested transactions
aliases:
- closed nesting
- partial abort
area: concurrency/transactional-memory
level: advanced
summary: "A transaction that starts inside another one. Flat nesting merges it into the parent; closed nesting lets it abort alone; open nesting lets it commit early."
prereqs: [transaction, read-set-and-write-set, transaction-abort]
see_also: [open-nested-transactions, retry-and-orelse, redo-log, undo-log, transaction-irrevocability, reentrant-lock, two-phase-commit, transactional-boosting]
sources:
  - paper: doi:10.1016/j.scico.2006.05.010
    title: "J. Eliot B. Moss and Antony L. Hosking, Nested transactional memory: model and architecture sketches, Science of Computer Programming 63(2), 2006, pp. 186 to 201"
    locator: the model of closed and open nesting for transactional memory, the rules for read and write sets on commit and abort of a child, and the sketches of hardware support
  - book: "J. Eliot B. Moss, Nested Transactions: An Approach to Reliable Distributed Computing, MIT Press, 1985 (PhD thesis, MIT, 1981)"
    locator: the original model of nested transactions in databases, with locks inherited by the parent
  - book: doi:10.1007/978-3-031-01728-5
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, 2010
    locator: Chapter 2 (Basic transactions, the section on nesting) and Chapter 4 (Software transactional memory, the support for nesting in redo and undo logs)
---

A **nested transaction** is a transaction that begins while another transaction of the same thread is running. Nesting happens as soon as code that uses transactions calls a library that also uses them. Three meanings are common: **flat nesting** treats the inner transaction as part of the outer one, **closed nesting** lets the inner transaction abort and retry alone while its effects stay private to the outer one until the outer one commits, and **open nesting** lets the inner transaction commit for everyone at once. Moss developed nested transactions for databases in 1981; Moss and Hosking carried the model over to transactional memory in 2006.

## In plain words

Transactions are useful because they compose: a function that moves money from one account to another can be called inside a bigger transaction that pays several bills, and the whole thing is still all or nothing. So a transaction often starts inside another one.

The simplest rule is to ignore the inner start and end: everything is one big transaction. That is flat nesting. Its drawback is that any problem in the inner part throws away the work of the whole.

Closed nesting gives the inner part its own undo. If the inner part fails, only it is redone; the outer work stays. When the inner part succeeds, its changes join the outer transaction and still become visible to other threads only when the outer one commits. Open nesting, described on its own page, goes further and publishes the inner changes at once.

## The idea

### The tree of transactions

A thread that starts a transaction inside a transaction builds a tree: the *top-level* transaction is the root, and each nested transaction is a child of the transaction that was running when it began. Most TMs allow only *linear nesting*: a transaction has at most one active child at a time, so the active transactions of a thread form a path from the root. Moss and Hosking work mostly with this case. Parallel nesting, where a transaction runs several children at the same time, is harder and appears mainly in research systems.

Each transaction $T$ has a read set $R(T)$ and a write set $W(T)$ (see [read set and write set](/read-set-and-write-set/)). A child $C$ of $T$ sees the writes of $T$ and of all its ancestors, and they see none of its writes until it commits.

### Flat nesting

The inner `begin` and `commit` only change a depth counter; reads and writes go to the sets of the top-level transaction. An abort anywhere aborts the top-level transaction. This is cheap and is what most hardware TMs do (Intel TSX, for example, counts nesting levels and aborts the outermost transaction on any abort). Its meaning is that of a [reentrant lock](/reentrant-lock/): taking it again inside itself is a no-op. A flat inner transaction cannot abort on its own, so an inner `abort` statement must abort the whole.

### Closed nesting

Rules for a child $C$ of $T$:

| event | effect |
|---|---|
| $C$ reads $x$ | look in $W(C)$, then in the write sets of the ancestors from the nearest; add $x$ to $R(C)$ |
| $C$ writes $x$ | add $x$ to $W(C)$, private to $C$ |
| $C$ commits | $R(T) \leftarrow R(T) \cup R(C)$, $W(T) \leftarrow W(T) \cup W(C)$ (the writes of $C$ win); nothing becomes visible to other threads |
| $C$ aborts | drop $R(C)$ and $W(C)$; $T$ goes on and may run $C$ again |
| $T$ (top level) commits | all writes become visible at once |

The top-level commit validates the whole merged read set, so the outcome is the same as with flat nesting whenever no child aborts. The gain is *partial abort*: if a conflict touches only locations that $C$ accessed, the TM can abort and retry $C$ alone. Example: the outer transaction writes $x \leftarrow 1$, then a child reads $y$, a hot counter, and writes $y \leftarrow y + 1$.

| step | outer $T$ | child $C$ | another thread |
|---|---|---|---|
| 1 | write $x \leftarrow 1$ (in $W(T)$) | | |
| 2 | | begin; read $y = 5$; write $y \leftarrow 6$ (in $W(C)$) | |
| 3 | | | commit $y \leftarrow 9$ |
| 4 | | validation finds $y$ changed; abort $C$ only | |
| 5 | | begin; read $y = 9$; write $y \leftarrow 10$; commit into $T$ | |
| 6 | commit: $x = 1$, $y = 10$ become visible | | |

With flat nesting step 4 would abort $T$ and redo step 1 as well.

A conflict that involves a location in $R(T)$ or $W(T)$ (one that the parent or an earlier child accessed) cannot be fixed by retrying only $C$; the TM must abort the nearest ancestor whose sets contain the location.

### Implementing closed nesting

- **Redo log.** Keep one write buffer per nesting level, or one buffer whose entries carry the level. A read searches from the innermost level out. Commit of a child merges its buffer into the parent's; abort drops it. On a TL2-like STM the read set needs per-level marks so that a child's reads can be dropped or kept. The `orElse` construct of [retry and orElse](/retry-and-orelse/) uses this: the first alternative is a closed nested transaction.
- **Undo log.** Keep one undo log with a mark at the start of each child. A child abort undoes entries back to its mark, in reverse order; a child commit just removes the mark. Locks taken by the child pass to the parent, as in Moss's database model, where a committing child's locks are inherited by its parent.
- **Hardware.** Hardware with closed nesting needs a level tag on each cache line in the read and write sets, or a log in memory; this is why most commercial HTMs only flatten. Moss and Hosking sketch hardware for both closed and open nesting.

### Open nesting in one paragraph

An open nested child commits for everyone: its writes become visible to other threads at once, and its locations leave the read and write sets of the parent. If the parent later aborts, the effect of the child cannot be undone from a log, so the programmer supplies a compensating action, and the parent holds abstract locks to keep the semantics serializable. See [open nested transactions](/open-nested-transactions/).

## Examples

**A library call inside a transaction.** `atomic { transfer(a, b, 10); transfer(b, c, 5) }` where `transfer` itself uses `atomic`. With flat or closed nesting the result is the same as one transaction with four updates. Closed nesting allows the second transfer to retry alone if only $c$ conflicts.

**Error handling.** A language can map an exception that leaves a nested atomic block to a child abort: the child's writes are undone and the exception goes on to the parent, which may catch it and try something else. Flat nesting cannot do this without aborting the whole.

**orElse.** `orElse (take q₁) (take q₂)` runs `take q₁` as a closed child; if it calls `retry`, its writes go, its reads stay, and `take q₂` runs.

**Counters in a long transaction.** Open nesting fits a shared statistics counter or a unique-ID generator inside a long transaction better than closed nesting: closed nesting keeps the counter in the parent's sets until the top-level commit, so all transactions that use the counter conflict for their whole length.

## Where it is used

- Database systems since Moss's thesis use nested transactions for partial rollback (savepoints are the flat-log version of the same idea) and for distributed transactions, where each subtransaction runs at one site and [two-phase commit](/two-phase-commit/) closes the top level.
- Most STMs for languages (GHC Haskell for `orElse`, and many research STMs for Java, C# and C++) implement closed nesting, often only where it is needed and flat nesting elsewhere.
- Hardware TMs such as Intel TSX and IBM POWER flatten nested transactions up to a fixed depth and abort if the depth is exceeded.

## References
