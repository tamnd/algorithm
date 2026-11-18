---
tag: HN9ERD
kind: concept
slug: eager-and-lazy-replication
name: Eager and lazy replication
aliases:
- lazy replication
- eager replication
area: databases/distributed-databases
level: core
summary: "Eager replication updates every copy inside the transaction, lazy replication after commit; in the analytical model of Gray et al., eager deadlocks grow as the cube of the node count."
prereqs: [one-copy-serializability, two-phase-locking]
see_also: [read-one-write-all, primary-copy-locking, primary-backup-replication, quorum-replication, two-phase-commit, last-writer-wins, eventual-consistency, highly-available-transactions]
sources:
  - paper: doi:10.1145/233269.233330
    title: "Jim Gray, Pat Helland, Patrick O'Neil and Dennis Shasha, The dangers of replication and a solution, Proceedings of the 1996 ACM SIGMOD International Conference on Management of Data, pages 173 to 182"
    locator: "Section 2 and Table 1 (eager and lazy, group and master), Section 3 (equations 1 to 13), Section 4 (lazy group, equations 14 to 18), Section 5 (lazy master, equation 19), Sections 6 and 7 (convergence and two-tier replication)"
  - book: isbn:9780201107159
    title: "Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987"
    locator: Chapter 8 (replicated data and one-copy serializability)
---

A replicated database keeps copies of each item on several nodes, and an update must reach all of them. *Eager* replication updates every copy inside the transaction that made the update, so the transaction commits only when all copies have the new value. *Lazy* replication updates one copy inside the transaction and sends the update to the other copies after the commit. Gray, Helland, O'Neil and Shasha (1996) added a second choice, who may update an item (any copy, called *group*, or one *master* copy), and used a simple analytical model to show that the rates of deadlocks and reconciliations grow much faster than the number of nodes.

## In plain words

Think of a joint bank account with three books: yours, your partner's and the bank's. With eager replication, each payment is written in all three books before it counts. The books always agree, and an overdraft is refused, but every payment must reach all three books, and a book that is away (a phone with no signal) stops all payments.

With lazy replication, each of you writes in your own book and the other books learn of it later. Payments are fast and work offline. But both of you can spend the same 1,000 dollars, and someone must sort it out later. Gray and his coauthors showed that both ways get much worse as the number of books grows: ten times more nodes gives about a thousand times more deadlocks or conflicts.

## The idea

**Two choices.** Section 2 of the paper sorts replication schemes by two choices.

- **Propagation.** Eager: one transaction updates all copies. Lazy: the first transaction updates one copy and commits, and then one more transaction per other node applies the update there.
- **Ownership.** Group: any node with a copy may update it (update anywhere). Master: each item has one master node; only the master updates its copy, and other nodes send their updates to it.

| | Lazy | Eager |
|---|---|---|
| Group | $N$ transactions, $N$ owners | one transaction, $N$ owners |
| Master | $N$ transactions, one owner | one transaction, one owner |

Eager schemes give [one-copy serializability](/one-copy-serializability/) when they lock the copies, as in [read-one-write-all](/read-one-write-all/) (eager group) and [primary copy locking](/primary-copy-locking/) (eager master). Locking turns conflicts into waits and deadlocks. Lazy group schemes cannot wait, since the first update has already committed. They detect a conflict when an update reaches a copy that has changed meanwhile, and must then *reconcile* it, by a rule or by a person. Lazy master schemes send each update to the master inside the transaction, so they wait and deadlock like eager schemes but have no reconciliation.

**The model.** Every result below is a heuristic estimate from the simple analytical model of Section 2, not a theorem and not a measurement. The database has $\text{DB\_Size}$ objects, and every node stores a copy of all of them. Each node starts $\text{TPS}$ transactions per second, each with $\text{Actions}$ updates of objects chosen uniformly at random, and each update takes $\text{Action\_Time}$. Reads are ignored, message delays and message processing are ignored, waits are assumed rare, and only deadlock cycles of two transactions are counted. The authors note that adding message delays would make every rate worse.

**One node.** A node has $\text{TPS} \cdot \text{Actions} \cdot \text{Action\_Time}$ transactions running at once (equation 1). A transaction waits with probability about

$$P_W \approx \frac{\text{Transactions} \cdot \text{Actions}^2}{2\, \text{DB\_Size}}$$

(equation 2), and it deadlocks with probability about $P_W^2 / \text{Transactions}$ (equation 3), since a deadlock needs two waits that close a cycle.

**Eager replication.** With $N$ nodes, a transaction updates $N$ copies, so it has $\text{Actions} \cdot N$ updates and lasts $N$ times longer, and there are $N$ times more of them. The number of transactions running at once grows as $N^2$ (equation 7). Putting this into equations 2 and 3 gives the system deadlock rate (equation 12):

$$\text{Eager\_Deadlock\_Rate} \approx \frac{\text{TPS}^2 \cdot \text{Action\_Time} \cdot \text{Actions}^5 \cdot N^3}{4\, \text{DB\_Size}^2}.$$

Ten times more nodes gives a thousand times more deadlocks, and ten times more updates per transaction gives a hundred thousand times more. If the database grows with the number of nodes, as in the checkbook example and in TPC-A, TPC-B and TPC-C, the rate grows only linearly in $N$ (equation 13). If a transaction updated the copies in parallel, its duration would not grow with $N$, and the growth would be quadratic.

**Lazy group replication.** Each wait in an eager system becomes a reconciliation in a lazy group system, because the conflict is found only after both updates committed. Waits are much more common than deadlocks, so the reconciliation rate follows the wait rate (equation 14):

$$\text{Lazy\_Group\_Reconciliation\_Rate} \approx \frac{\text{TPS}^2 \cdot \text{Action\_Time} \cdot (\text{Actions} \cdot N)^3}{2\, \text{DB\_Size}}.$$

For mobile nodes that stay disconnected for $\text{Disconnect\_Time}$ and then exchange their updates, the rate is about $\text{Disconnect\_Time} \cdot (\text{TPS} \cdot \text{Actions} \cdot N)^2 / \text{DB\_Size}$ (equation 18).

**Lazy master replication.** Updates go to the master copies, and the copies at other nodes are updated later in background transactions that can restart without harm to the user. There are $N$ times more transactions than on one node, but they are short, so the deadlock rate is (equation 19)

$$\text{Lazy\_Master\_Deadlock\_Rate} \approx \frac{(\text{TPS} \cdot N)^2 \cdot \text{Action\_Time} \cdot \text{Actions}^5}{4\, \text{DB\_Size}^2},$$

which grows as $N^2$. The acknowledgments of the copy used here say that a reader found a mistake in the published version of equation 19, and the form above is taken from that copy. Lazy master needs a connection to the master, so it does not help mobile nodes.

**Convergence without serializability.** Section 6 describes systems that give up serializability and keep only *convergence*: when updates stop and the nodes exchange them, all copies become equal. Timestamped replace, as in [last writer wins](/last-writer-wins/), converges but loses updates. Updates that commute, such as "add 50 to the balance", converge without loss.

**Two-tier replication.** The paper's own scheme (Section 7) has always-connected base nodes that hold the master copies, and mobile nodes that run *tentative* transactions on their local copy. When a mobile node connects, the base nodes run each tentative transaction again as a *base* transaction on the master copies, in lazy master style, and accept it only if it passes an acceptance test written by the application ("the balance must not go below zero"). A rejected transaction goes back to its owner. The master copies are always the result of a serializable execution, and if all transactions commute, nothing is rejected. Base transactions still deadlock at the $N^2$ rate of equation 19.

## Examples

**Numbers from the model.** Take $\text{TPS} = 10$ per node, $\text{Actions} = 5$, $\text{Action\_Time} = 10$ ms and $\text{DB\_Size} = 10{,}000$. These inputs are made up for the example; the numbers that follow are the formulas evaluated on them, not measurements.

| Nodes | eager deadlocks per day (eq. 12) | eager deadlocks per day, database grows with nodes (eq. 13) | lazy master deadlocks per day (eq. 19) | lazy group reconciliations per second (eq. 14) |
|---|---|---|---|---|
| 1 | 0.675 | 0.675 | 0.675 | 0.00625 |
| 10 | 675 | 6.75 | 67.5 | 6.25 |

At 10 nodes the chance that an eager transaction waits is about 0.06, so the assumption that waits are rare still holds roughly. A system that saw less than one deadlock a day on one node sees hundreds a day on ten, which is the scale-up trap that the paper warns about: a prototype on two nodes works, and the same design on many nodes does not.

**The checkbook.** The account holds 1,000 dollars. Under eager replication, the second person who tries to spend the money gets a refusal, or waits for the first transaction. Under lazy group replication, both payments of 1,000 dollars commit on their own books, and the conflict is found when the updates meet. Under lazy master replication, the bank is the master: a payment counts only when the bank's book accepts it. The cheque is a tentative transaction in the two-tier sense, and clearing it at the bank is the base transaction.

**Timestamps lose updates.** Two nodes add 50 and 30 to a balance of 200, writing 250 and 230 with timestamps $t_1 < t_2$. Last writer wins keeps 230 at every node, so the nodes converge but the deposit of 50 is lost. If the updates are sent as "add 50" and "add 30", every node ends with 280.

## Where it is used

- **Eager master and eager group.** [Primary copy locking](/primary-copy-locking/) and [read-one-write-all](/read-one-write-all/) are eager schemes, usually with [two-phase commit](/two-phase-commit/) at the end. Quorum schemes ([quorum replication](/quorum-replication/)) are eager schemes that update only a quorum of copies, which keeps updates possible when some nodes are down.
- **Lazy master.** [Primary-backup replication](/primary-backup-replication/) with asynchronous shipping of updates to the backups is lazy master: the primary commits alone, and a backup may be behind.
- **Lazy group.** Multi-master systems with conflict rules, such as Lotus Notes (append and timestamped replace), Microsoft Access (version vectors, most recent update wins) and the twelve reconciliation rules of Oracle 7, are the examples the paper names. Modern [eventually consistent](/eventual-consistency/) stores and [CRDTs](/crdt/) follow the same line, with commuting updates.
- **Limits of availability.** Which guarantees a lazy system can still give without waiting for other nodes is the subject of [highly available transactions](/highly-available-transactions/).

The model assumes locking with copies updated one after the other. Eager designs that order transactions in another way, for example by a total order broadcast to all nodes before they run (as in [Calvin](/calvin-deterministic-transactions/)), can avoid deadlocks across nodes, and the equations above do not describe them.

## References
