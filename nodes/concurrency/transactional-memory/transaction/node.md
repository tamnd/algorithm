---
tag: SQZPF9
kind: definition
slug: transaction
name: Transaction
aliases:
- atomic transaction
- atomic block
area: concurrency/transactional-memory
level: intro
summary: A block of reads and writes that either commits as a whole or aborts with no visible effect. In memory it gives atomicity and isolation, but not durability.
prereqs: [critical-section, serializability]
see_also: [software-transactional-memory, opacity, read-set-and-write-set, transaction-conflict, transaction-abort, nested-transactions, strong-atomicity, transaction-irrevocability]
sources:
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 1 (the motivation and the atomic block) and Chapter 2 (basic transactions, the semantics of transactions, and the difference from database transactions)
  - paper: doi:10.1145/165123.165164
    title: Maurice Herlihy and J. Eliot B. Moss, Transactional memory, architectural support for lock-free data structures, ISCA 1993
    locator: the definition of a transaction as a finite sequence of machine instructions that is serializable and atomic
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983
    locator: the section that defines the ACID properties (atomicity, consistency, isolation, durability)
  - paper: doi:10.1145/322154.322158
    title: Christos H. Papadimitriou, The serializability of concurrent database updates, Journal of the ACM 26(4), 1979
    locator: the definition of a serializable schedule
  - paper: doi:10.1145/1345206.1345233
    title: Rachid Guerraoui and Michał Kapałka, On the correctness of transactional memory, PPoPP 2008
    locator: the model of transactional histories (committed, aborted, live and commit-pending transactions) and the definition of opacity
---

A transaction is a block of reads and writes of shared memory that a process runs as one unit. It ends in one of two ways. It *commits*, and then all its writes take effect at once. Or it *aborts*, and then none of its writes take effect, and the program usually runs it again. Other processes never see a transaction half done. Herlihy and Moss (1993) took the idea from databases and applied it to the memory of a multiprocessor. In memory, a transaction gives two of the four ACID properties of a database transaction: **atomicity** and **isolation**. It does not give **durability**, because the memory does not survive a crash or a power loss.

## Definition

**Notation and model.** $n$ is the number of processes, $p$ and $q$ are processes, and $m$ is the number of shared words. The processes are asynchronous and may crash between any two steps. They share words with atomic read and write and, where a page says so, stronger primitives such as [compare-and-swap](/compare-and-swap/). The memory is [sequentially consistent](/sequential-consistency/).

**Definition.** A **transaction** $T$ of process $p$ is a sequence of operations

$$\text{begin}, \ \text{read}(a_1) \to v_1 \text{ or } \text{write}(a_1, v_1), \ \dots, \ \text{tryCommit}$$

on shared words $a_i$, which the system completes with **commit** or **abort**. Any read, write or tryCommit may return abort instead of a value. After an abort, $T$ takes no more steps.

The *status* of $T$ at a point of a run is:

| Status | Meaning |
|---|---|
| live | $T$ has begun and has not called tryCommit |
| commit-pending | $T$ has called tryCommit and has no answer yet |
| committed | tryCommit returned commit |
| aborted | an operation of $T$ returned abort |

A **history** is the sequence of the begin, read, write, tryCommit, commit and abort events of all transactions, in the order they occur. $T_1$ **precedes** $T_2$ in real time if $T_1$ commits or aborts before $T_2$ begins.

A system of transactions must give two properties:

1. **Atomicity** (all or nothing). The writes of a committed transaction all take effect. The writes of an aborted transaction have no effect on any other transaction.
2. **Isolation.** The result is as if the transactions ran one at a time. The usual forms of this rule are [serializability](/serializability/) (some serial order of the committed transactions gives the same reads and the same final state), strict serializability (the order also respects real time), and [opacity](/opacity/). Opacity is strict serializability for all transactions, also the aborted and live ones: each one reads values that agree with one serial order that respects real time.

The program code that makes a transaction is often an **atomic block**, `atomic { ... }`. The programmer marks the block, and the system ([software transactional memory](/software-transactional-memory/) or [hardware transactional memory](/hardware-transactional-memory/)) makes it a transaction. A block may run as many transactions, one for each attempt, until one attempt commits.

**What is not included.** Durability, the "D" of ACID (Haerder and Reuter 1983), is not part of a memory transaction: when the process or the machine stops, the memory is lost. Consistency, the "C", is the job of the program: if each transaction alone keeps an invariant true, then atomicity and isolation keep it true when transactions run at the same time.

## Examples and non-examples

The examples use two words $x$ and $y$, both 10 at the start. $T_1$ moves 3 from $x$ to $y$: it reads $x = 10$ and $y = 10$, writes $x = 7$ and $y = 13$, and calls tryCommit. $T_2$ is an audit that reads $x$ and $y$. The invariant is $x + y = 20$. A script checked each verdict below with a brute-force search over serial orders.

**Example (serial).** $T_1$ commits, then $T_2$ begins and reads $x = 7$, $y = 13$, and commits. The order $T_1, T_2$ explains it. It is serializable, strictly serializable and opaque. $T_2$ sees the sum 20.

**Example (serial order against the run order).** $T_2$ begins and reads $x = 10$. Then $T_1$ runs to its commit. Then $T_2$ reads $y = 10$ and commits. $T_2$ ran over the whole of $T_1$, but the order $T_2, T_1$ explains it, and real time allows it, because $T_2$ began before $T_1$ ended. It is opaque. So a transaction does not need to run alone; it must only look as if it did.

**Non-example (a torn read).** $T_2$ reads $x = 7$, which $T_1$ wrote, and then $y = 10$, the value from before $T_1$. In order $T_1, T_2$ it should read $y = 13$, and in order $T_2, T_1$ it should read $x = 10$. No serial order explains it, so if $T_2$ commits the history is not serializable, and $T_2$ reports the sum 17. A correct system must abort $T_2$ or never let it read these values.

**Non-example (an aborted transaction that saw a torn state).** The same reads, but $T_2$ aborts. The committed transactions alone ($T_1$) are serializable, so the history is serializable. It is not opaque, because the aborted $T_2$ saw a state that never existed. This is the run of a [zombie transaction](/zombie-transactions/): if $T_2$ divides by $20 - (x + y)$ or follows a pointer it read, it can fail before the system aborts it.

**Non-example (reads of old values after the end).** $T_1$ commits. Later $T_2$ begins and reads $x = 10$ and $y = 10$. The order $T_2, T_1$ explains the values, so the history is serializable. It is not strictly serializable, because $T_1$ ended before $T_2$ began, and real time puts $T_1$ first.

**Non-example (two critical sections).** A program takes a lock, reads $x$, releases the lock, then takes it again and writes $y$. Each [critical section](/critical-section/) is atomic, but the two together are not a transaction: another process can run between them. A transaction is one unit, however many words it touches.

**Example (an atomic block that cannot abort).** A block that prints a line or sends a packet cannot be undone. A system can still run it as a transaction if it makes it *irrevocable*: the block runs once, and the system makes sure that it never has to abort it. See [transaction irrevocability](/transaction-irrevocability/).

## Related definitions

- The [read set and write set](/read-set-and-write-set/) of a transaction are the words it has read and the words it has written. Two transactions [conflict](/transaction-conflict/) when one writes a word that the other reads or writes.
- [Transaction abort](/transaction-abort/) covers why a system aborts a transaction, and what retry costs.
- [Software transactional memory](/software-transactional-memory/) implements transactions in code on ordinary memory words. Hardware transactional memory uses the cache.
- [Serializability](/serializability/) and [opacity](/opacity/) are the isolation conditions. Opacity is the usual one for memory transactions, because a memory transaction can crash or loop on a torn state, which a database query cannot do in the same way.
- [Strong atomicity](/strong-atomicity/) and [weak atomicity](/weak-atomicity/) say what happens when code outside any transaction touches the same words.
- [Nested transactions](/nested-transactions/) are transactions inside transactions.
- [Multiversion concurrency control](/multiversion-concurrency-control/) and [snapshot isolation](/snapshot-isolation/) are database forms of isolation that keep old versions of data.

## References
