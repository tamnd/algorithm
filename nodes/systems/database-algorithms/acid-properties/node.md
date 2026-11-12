---
tag: 62H2R4
kind: definition
slug: acid-properties
name: ACID properties
aliases:
- ACID
- atomicity, consistency, isolation and durability
area: systems/database-algorithms
level: intro
summary: "The four guarantees of a database transaction: atomicity (all or nothing), consistency (constraints kept), isolation (as if alone) and durability (commits survive crashes)."
prereqs: []
see_also: [serializability, isolation-levels, crash-recovery, concurrency-control, write-ahead-logging, two-phase-commit, transaction, atomic-commit]
sources:
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983, pages 287 to 317
    locator: the section on the transaction concept, where the four properties are named and the acronym ACID is introduced
  - paper: "Jim Gray, The transaction concept, virtues and limitations, Proceedings of the 7th International Conference on Very Large Data Bases (VLDB), 1981, pages 144 to 154"
    locator: the definition of a transaction as a state transformation with the properties of consistency, atomicity and durability
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 1 (the ACID properties) and Chapter 4 (transaction models)
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 1 (transactions, recoverability and serializability as the correctness criteria of the system)
---

The ACID properties are four guarantees that a database system gives for each transaction: *atomicity*, *consistency*, *isolation* and *durability*. A transaction is a group of reads and writes that the system treats as one unit of work. Haerder and Reuter introduced the acronym in 1983, building on Gray's 1981 account of transactions as atomic, consistent and durable state changes. In a real system, isolation comes from [concurrency control](/concurrency-control/) and atomicity and durability come from [crash recovery](/crash-recovery/).

## Definition

**Model.** The database is a set of data items with values; its *state* is the map from items to values. A transaction $T$ is a program that reads and writes items and then ends with commit (make the changes permanent) or abort (cancel them). Seen from outside, a committed transaction is a map from the state before it to the state after it. The system runs many transactions at the same time and can fail by a *crash*: main memory is lost and stable storage (disk) survives. Each property is a promise about what users can observe under this model.

- **Atomicity.** For each transaction, either all of its writes take effect or none of them does. This holds when the transaction aborts on its own, when the system aborts it (for example to break a [deadlock](/deadlock/)), and when the system crashes in the middle. After a crash, recovery removes the effects of every transaction that had not committed.
- **Consistency.** Each transaction, run alone from a state that satisfies the integrity constraints of the database, ends in a state that satisfies them. This is mostly the duty of the transaction program. The system helps by checking the declared constraints (keys, foreign keys, checks) and aborting a transaction that breaks them. The other three properties then make sure that the constraints also hold when transactions run concurrently and when failures occur.
- **Isolation.** Concurrent transactions do not see each other's partial effects: the result of the concurrent execution is the same as the result of some serial execution of the committed transactions. The precise form is [serializability](/serializability/). SQL systems also offer weaker [isolation levels](/isolation-levels/), and the default level of many systems is weaker than serializable.
- **Durability.** Once the system has reported the commit of a transaction, its effects survive every later failure in the failure model, in particular crashes. The usual failure model covers the loss of main memory. Survival of a lost disk needs an archive copy or replication.

**How they fit together.** Atomicity and isolation together let a programmer reason about one transaction at a time: a transaction sees a state produced by complete committed transactions, and leaves either its full effect or nothing. With consistency of each transaction alone, this gives the main theorem behind the concept: every state that users can observe, and every state after recovery, satisfies the integrity constraints. The proof is an induction over the equivalent serial order (see the consistency argument on the [serializability](/serializability/) page).

**Mechanisms.** Each property maps to a group of algorithms.

| property | threat | mechanism |
|---|---|---|
| atomicity | abort, crash before commit | undo information in a [write-ahead log](/write-ahead-logging/), or [shadow paging](/shadow-paging/) |
| consistency | a bad program, bad input | constraint checks; the program's own logic |
| isolation | concurrent transactions | [two-phase locking](/two-phase-locking/), [timestamp ordering](/timestamp-ordering/), [optimistic](/optimistic-concurrency-control/) and [multiversion](/multiversion-concurrency-control/) concurrency control |
| durability | crash after commit | redo information forced to the log at commit, [group commit](/group-commit/), [ARIES](/aries-recovery/) restart |

The [steal and force policies](/steal-and-force-policies/) of the buffer manager decide how much undo and redo work recovery needs.

## Examples and non-examples

**A transfer.** A transaction moves 100 from account $A$ to account $B$: it reads $A = 500$ and $B = 200$, writes $A = 400$ and writes $B = 300$, then commits. The constraint is that the total stays 700.

- If the system crashes after the write of $A$ and before the commit, atomicity requires that recovery restore $A = 500$. A state with $A = 400$ and $B = 200$ would lose 100.
- If a second transaction reads $A$ and $B$ while the transfer runs and sees $A = 400$ and $B = 200$, isolation is broken: no serial order shows the total 600.
- If the system reports the commit and then crashes before the new values reach the disk, durability requires that recovery redo the writes, so that $A = 400$ and $B = 300$ after restart.

**A lost update breaks isolation.** Two transactions each read a counter $x = 10$, add 1 and write it back. The interleaving $r_1(x)\ r_2(x)\ w_1(x)\ w_2(x)$ ends with $x = 11$, while each serial order ends with $x = 12$. Each transaction alone is consistent and atomic, but the execution is not isolated.

**Non-example: a commit acknowledged from memory.** A system that replies "committed" when the log record is only in a memory buffer, and writes it to disk later, does not give durability: a crash in between loses a commit that the client has already seen. Group commit is correct because it delays the reply until the log write that holds the commit record is on disk.

**Non-example: read uncommitted.** At the isolation level READ UNCOMMITTED, a transaction can read a value written by a transaction that later aborts. The reader then acts on a state that never existed, so isolation in the sense above does not hold, even though each transaction is still atomic and durable.

**In-memory transactions.** A [transaction](/transaction/) of software transactional memory gives atomicity and isolation for memory words, but there is no stable storage, so durability does not apply, and consistency is left to the program. Its safety condition, [opacity](/opacity/), is stronger than serializability in one way: it also covers transactions that later abort.

## Related definitions

- **[Serializability](/serializability/)** is the exact meaning of isolation; [conflict serializability](/conflict-serializability/) is the version that schedulers enforce.
- **[Isolation levels](/isolation-levels/)** are the named weaker forms of isolation (read committed, repeatable read, snapshot isolation and others).
- **[Crash recovery](/crash-recovery/)** is the part of the system that gives atomicity and durability after a failure, usually with a [write-ahead log](/write-ahead-logging/).
- **[Concurrency control](/concurrency-control/)** is the part that gives isolation.
- **[Atomic commitment](/atomic-commit/)**, solved by [two-phase commit](/two-phase-commit/), extends atomicity to a transaction that runs at several sites: all sites commit or all abort. Two-phase commit is a commit protocol; it is not [two-phase locking](/two-phase-locking/), which is a concurrency control method.
- **Consistency in other senses.** The C of ACID is about integrity constraints of one database. The consistency of the CAP theorem and of replicated storage is a different notion, close to [linearizability](/linearizability/).

## References
