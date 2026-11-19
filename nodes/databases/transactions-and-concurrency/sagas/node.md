---
tag: ND2BYK
kind: model
slug: sagas
name: Sagas
aliases:
- compensating transactions
- saga pattern
area: databases/transactions-and-concurrency
level: advanced
summary: "A long-lived transaction written as a sequence of local transactions, each with a compensating transaction that undoes it on failure."
prereqs: [acid-properties, atomic-commit]
see_also: [nested-transactions, open-nested-transactions, two-phase-commit, transaction-chopping, escrow-transactional-method, transaction-anomalies, write-ahead-logging, highly-available-transactions]
sources:
  - paper: doi:10.1145/38713.38742
    title: "Hector Garcia-Molina and Kenneth Salem, Sagas, Proceedings of ACM SIGMOD 1987, pages 249 to 259"
    locator: "the definition of a saga and its compensating transactions, the guarantee on the executed sequence, backward and forward recovery with save points, and the implementation on top of a database system; chapter level only"
  - book: isbn:9781558601901
    title: "Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993"
    locator: "Chapter 4, Transaction Models, the sections on chained transactions, sagas and long-lived transactions, chapter level only"
  - book: isbn:9781558605084
    title: "Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001"
    locator: "the chapters on multilevel and open nested transactions and on compensation, chapter level only"
  - paper: doi:10.1145/211414.211427
    title: "Dennis Shasha, François Llirbat, Eric Simon and Patrick Valduriez, Transaction chopping, algorithms and performance studies, ACM Transactions on Database Systems 20(3), 1995, pages 325 to 363"
    locator: "the condition under which pieces of a transaction can commit one by one and keep serializability, chapter level only"
---

A *saga* (Garcia-Molina and Salem, 1987) is a long-lived transaction written as a sequence $T_1, T_2, \ldots, T_n$ of ordinary transactions, each with a *compensating transaction* $C_i$ that undoes the effect of $T_i$ in the terms of the application. Each $T_i$ commits on its own and releases its locks, so a long process does not hold locks for its whole length, and no [two-phase commit](/two-phase-commit/) across the steps is needed. The system guarantees that either the whole sequence runs, or a prefix runs followed by the compensations of that prefix in reverse order. The cost is isolation: other transactions see the results of the steps as they commit, so a saga is atomic only in a semantic sense, and the [transaction anomalies](/transaction-anomalies/) between sagas are the application's problem. Sagas can be seen as [open nested transactions](/open-nested-transactions/) with one level of children, and a relative of [transaction chopping](/transaction-chopping/), which asks when such pieces need no compensation and keep serializability.

## The machine

**A saga.** A saga is a sequence of transactions $T_1, \ldots, T_n$ and compensating transactions $C_1, \ldots, C_{n-1}$. Each $T_i$ and each $C_i$ is an ACID transaction of the underlying database. $C_i$ undoes $T_i$ semantically: a cancellation for a booking, a refund for a charge. It need not restore the old state byte for byte, since other transactions may have run in between. The last step $T_n$ needs no compensation, because after it the saga is complete.

**The guarantee.** The system runs the saga so that the committed sequence is one of

$$T_1\, T_2 \cdots T_n \qquad \text{or} \qquad T_1 \cdots T_j\, C_j\, C_{j-1} \cdots C_1 \quad \text{for some } 0 \le j < n.$$

Transactions of other sagas and of other programs may run between any two of these steps.

**Execution.** A saga execution component runs the steps in order and writes a *saga log*: the start of the saga, the start and end of each step and each compensation. The log is durable, like the log of [write-ahead logging](/write-ahead-logging/). After a crash, the component reads the log and continues: it finishes or reruns the step in progress and then goes on forward or backward.

**Backward recovery.** If $T_{j+1}$ aborts, the component runs $C_j, \ldots, C_1$. Each compensation is retried until it commits; the model assumes that a compensation can always eventually succeed.

**Forward recovery.** If the saga takes *save points*, the component can instead roll back to the last save point, by compensations, and run the steps from there again. With a save point after every step and steps that can always be retried until they commit, the saga never compensates and always completes; this is pure forward recovery.

**Example.** A trip: $T_1$ books a flight, $T_2$ books a hotel, $T_3$ charges the card. $C_1$ cancels the flight and $C_2$ cancels the hotel. If the charge $T_3$ is declined, the saga runs $T_1\, T_2\, C_2\, C_1$. Between $T_1$ and $C_1$ the seat is taken and other customers see one seat fewer; that is the missing isolation.

## What it counts

The model replaces the ACID guarantees of one long transaction with weaker ones, and the measure is which of them survive.

| property | one long transaction | saga |
|---|---|---|
| atomicity | all or nothing | all, or a prefix and its compensations |
| consistency | each transaction keeps the constraints | each step keeps the constraints |
| isolation | serializable with other transactions | none between steps |
| durability | yes | yes, for each step and for the saga log |

The resource measures are those of locking. Locks are held only for the length of one step, not of the saga, so the time others wait falls from the length of the saga to the length of a step. The price is the work of compensation on failure, and the design effort to write each $C_i$.

## Relation to other models

- **Flat transactions and two-phase commit.** One flat transaction, or a distributed one decided by [two-phase commit](/two-phase-commit/), gives full isolation and holds its locks to the end. A saga gives up isolation to release them early. Sagas suit processes that run for minutes or days, or that cross services that will not take part in an [atomic commit](/atomic-commit/) protocol.
- **Nested transactions.** In closed [nested transactions](/nested-transactions/), the effect of a child is visible only to its parent until the top level commits. In [open nested transactions](/open-nested-transactions/), a child commits at once and its effect is undone by an inverse operation, as in a saga; the multilevel theory gives conditions under which the result is serializable at the higher level, which plain sagas do not ask for.
- **Transaction chopping.** [Transaction chopping](/transaction-chopping/) also splits a transaction into pieces that commit one by one, but it requires that only the first piece can roll back, so no compensation is needed, and it gives a test under which every execution stays serializable. A saga whose steps pass that test, and whose later steps never fail, is serializable.
- **Escrow.** A step that reserves an amount by the [escrow method](/escrow-transactional-method/) has a compensation, the release, that cannot fail and commutes with other reservations.
- **Weak isolation.** The isolation between steps of different sagas is close to that of read uncommitted at the level of the saga: another saga may see a booking that a later compensation cancels. [Highly available transactions](/highly-available-transactions/) study what can be guaranteed without coordination in similar settings.

## Known results in the model

**The guarantee needs only the log and retries.** If every step and every compensation is an ACID transaction, the saga log is durable, and compensations always commit in the end, then after any crash the component can bring the saga to one of the two forms of the guarantee: it reads the log, finishes or reruns the step in progress, and continues forward or backward. No locks are held across steps.

**Compensation is not inversion.** The state after $T_1 \cdots T_j\, C_j \cdots C_1$ with other transactions in between need not equal the state without the saga. If a compensation restores a saved value instead of applying an inverse change, it can erase a later update of another saga, a lost update. Compensations should be written as inverse operations, such as "add back 2 seats", that commute with other updates of the same kind.

**Sagas show the anomalies of no isolation.** A step of one saga can read a value that a step of another saga wrote and that a compensation later undoes; this is the dirty read of the [transaction anomalies](/transaction-anomalies/), at the level of the saga. Two sagas can read and act on the same state and both proceed, as in write skew. Applications counter this with application-level locks or states ("pending" bookings), with steps that commute, or by placing the step that can fail first.

**Order of steps.** Steps that can fail should come early, and steps that cannot be compensated, such as sending a message to a person, should come last. A step after which the saga never fails is called a pivot in the practice of microservices; with all such irreversible steps after the last step that can fail, the saga never needs a compensation it cannot run.

**Parallel steps.** Garcia-Molina and Salem also discuss sagas whose steps run in parallel. The guarantee then concerns a partial order, and recovery compensates every committed step in an order that respects it.

## References
