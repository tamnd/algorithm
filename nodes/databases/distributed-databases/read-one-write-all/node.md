---
tag: JG3SB7
kind: algorithm
slug: read-one-write-all
name: Read-one write-all
aliases:
- ROWA
- ROWA-available
- available copies
area: databases/distributed-databases
level: core
summary: "A replica control protocol that reads any one copy of an item and writes all copies, or all available copies in its fault-tolerant form."
solves: [concurrency-control]
model: asynchronous-model
complexity:
  vars: {n: the largest number of copies of an item, r: the number of reads of a transaction, w: the number of writes of a transaction}
  messages: {worst: "2(r + w) n"}
  space: {extra: "O(r + w n)"}
properties: {deterministic: true, recursive: false}
history:
  year: 1984
  people: [Philip A. Bernstein, Nathan Goodman]
  note: "Read-one write-all is the simplest replica control rule of the early distributed databases. Bernstein and Goodman (1984) gave the available copies algorithm with its validation steps and a proof of one-copy serializability."
prereqs: [one-copy-serializability, strict-two-phase-locking, crash-failure]
see_also: [quorum-replication, primary-copy-locking, eager-and-lazy-replication, two-phase-commit, atomic-commit, deadlock-detection, failure-detector, primary-backup-replication]
sources:
  - book: isbn:9780201107159
    title: "Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987"
    locator: "Chapter 8, Replicated Data: the one-copy serializability theory (Sections 8.3 and 8.4), the atomicity of failures and recoveries (Section 8.5), the available copies algorithm with missing writes validation and access validation and its correctness, Theorem 8.7 (Section 8.6), the directory-oriented form (Section 8.7), communication failures (Section 8.8) and the virtual partition algorithm (Section 8.10)"
  - paper: doi:10.1145/1994.2207
    title: "Philip A. Bernstein and Nathan Goodman, An algorithm for concurrency control and recovery in replicated distributed databases, ACM Transactions on Database Systems 9(4), 1984, pages 596 to 615"
    locator: "the available copies algorithm, its treatment of site failures and recoveries, and its correctness proof"
---

Read-one write-all (ROWA) is the simplest way to keep the copies of a replicated item consistent. A transaction reads any one copy of an item, and it writes every copy. Each site runs strict two-phase locking on its own copies. The result is [one-copy serializable](/one-copy-serializability/): the users see the same results as with one copy of each item and a serial order of the transactions. Plain ROWA cannot write an item while one of its sites is down. The available copies form (ROWA-A) writes all copies whose sites answer, and it adds two checks at commit, missing writes validation and access validation, together with a copier transaction that brings a recovered copy up to date. Without these checks the scheme is wrong, and the page shows a history that proves it.

## In plain words

A club keeps the same member list in three offices. To look up a name, you can phone any one office. To change the list, you must phone all three offices and get each of them to make the change. Then every office always has the same list, and any one of them gives the correct answer.

If one office is closed, plain ROWA cannot change the list at all. The available copies form changes the list in the offices that are open and notes which office was closed. Before it finishes, it checks that the closed office is still closed, and that no open office closed in the meantime. A closed office that opens again does not answer lookups until it has copied the current list from another office.

## The problem

A database holds items $x, y, \dots$, and each item has copies $x_A, x_B, \dots$ at a fixed set of sites. Users submit transactions as if each item had one copy. The replica control protocol maps each logical read and write to actions on copies. The output must be [one-copy serializable](/one-copy-serializability/) (1SR): the physical history must be equivalent to a serial history of the same transactions on a database with one copy of each item.

The model is the [asynchronous model](/asynchronous-model/) with one strong addition. Sites fail by stopping ([crash failure](/crash-failure/)), a failed site loses its lock table and keeps its stored values, and a request to a failed site comes back as "no response". The answer "no response" is never wrong: the network does not lose messages, and it does not partition. This is a [failure detector](/failure-detector/) that makes no mistakes, and the available copies form is correct only under it. Each site runs [strict two-phase locking](/strict-two-phase-locking/) on its copies, with S locks for reads and X locks for writes held until commit or abort.

## The algorithm

```pseudo id=main
ROWA-A-TRANSACTION(T)
L1  for each operation of T, in order do
L2      if the operation is a read of x then
L3          for each copy x_A of x, in a fixed order, until one read succeeds do
L4              ask site A for an S lock on x_A and read x_A
L5          if no copy answered then abort T
L6      else                                        ▷ a write of x with value v
L7          send an X lock request for x_A, with v, to every copy x_A of x
L8          wait until each site has granted or is found down
L9          if no site granted then abort T         ▷ plain ROWA: if any site is down
L10         record the copies at the down sites as missed copies of T
L11 for each missed copy x_A of T do
L12     if site A is up again then abort T          ▷ missing writes validation
L13 for each copy x_A that T read or wrote do
L14     if site A failed after T locked x_A then abort T   ▷ access validation
L15 commit T at every site it accessed: install its writes and release its locks
```

Plain ROWA is the same procedure with the stronger test of line L9: a write aborts if any copy did not answer. It then never has missed copies, and lines L11 to L14 never abort in a run without failures.

**Recovery.** A site that recovers starts a new epoch and marks each replicated copy as unreadable. A read of an unreadable copy is refused, and line L3 then tries the next copy. For each such copy $x_A$, the site starts a copier transaction that reads $x$ at another site and writes the value to all copies of $x$, with the same procedure. A copy becomes readable again when a committed write, of the copier or of a user transaction, is installed on it. A copy with no other copy stays readable.

**Validation at commit.** A site records its epoch when it grants a lock, and line L14 compares it with the epoch at commit. In the code, lines L11 to L15 are one atomic step. In a real system this step is the vote phase of an [atomic commitment](/atomic-commit/) protocol such as [two-phase commit](/two-phase-commit/): each site that T accessed must still have T's locks, and each missed site must still be down.

**Deadlocks.** Strict 2PL at the sites can deadlock, also across sites. The code uses a central [deadlock detector](/deadlock-detection/) that reads the lock tables of all up sites, builds the [wait-for graph](/wait-for-graph/) and aborts the transaction with the largest id in each cycle. A distributed detector such as [Chandy-Misra-Haas](/chandy-misra-haas/) can replace it.

## Example

**A plain write.** Item $x$ has copies at $A$ and $B$, and $y$ has copies at $A$, $B$ and $C$. Transaction $T_1 = r_1[x]\, w_1[y]$ runs alone. It reads $x_A$ and writes all three copies of $y$. The code records the physical history $r_1[x_A]\, w_1[y_C]\, w_1[y_B]\, w_1[y_A]\, c_1$, in the order in which the random network delivered the grants. It sends $2 \cdot 1 + 2 \cdot 3 = 8$ messages: one request and one answer for the read, and one request and one grant for each copy of $y$.

**Why the validations are needed.** This is the example of Bernstein, Hadzilacos and Goodman. Item $x$ has copies at $A$ and $B$, and $y$ has copies at $C$ and $D$. Let $T_1 = r_1[x]\, w_1[y]$ and $T_2 = r_2[y]\, w_2[x]$.

| step | event | effect |
|---|---|---|
| 1 | $T_1$ reads $x_A$, $T_2$ reads $y_C$ | both reads get the initial value 0 |
| 2 | sites $A$ and $C$ fail | the S locks on $x_A$ and $y_C$ are lost |
| 3 | $T_1$ writes $y$ | $y_C$: no response, $y_D$: granted |
| 4 | $T_2$ writes $x$ | $x_A$: no response, $x_B$: granted |
| 5 | both commit | $y_D = 100$, $x_B = 200$ |

The code, run with the validations turned off, gives the history $r_1[x_A]\, r_2[y_C]\, w_1[y_D]\, w_2[x_B]\, c_1\, c_2$ with 12 messages. At the copy level it is conflict serializable, because no two actions touch the same copy. But it is not 1SR. In a serial one-copy history, either $T_1$ comes first and $T_2$ reads $y$ from $T_1$, or $T_2$ comes first and $T_1$ reads $x$ from $T_2$. Here both read the initial values. The brute-force test of the code finds no serial order.

With the validations on, line L14 sees that $A$ failed after $T_1$ locked $x_A$, and it aborts $T_1$; for the same reason, at $C$, it aborts $T_2$. The history ends in $a_1\, a_2$. If $A$ and $C$ had recovered before the commit, line L12 would have aborted both instead.

**A wrong copier.** Let the copier of a recovered copy write only that copy. In one test run (seed 28), site $A$ recovers and its copier $T_{1000}$ brings $x_A$ up to date, while a user transaction $T_3 = r_3[x]\, w_3[x]$ runs. The history contains $r_{1000}[x_B]\, r_3[x_B]\, w_{1000}[x_A]\, c_{1000}\, w_3[x_B]\, w_3[x_A]\, c_3$. The copier takes no lock on $x_B$ that conflicts with the S lock of $T_3$. In the one-copy view, both transactions read the initial $x$ and both write $x$, which is a lost update, and no serial order fits. When the copier writes all copies of $x$, its write on $x_B$ waits for the S lock of $T_3$, and all 250 test runs with one failure and one recovery are 1SR.

## Correctness

The claims are proved on [the proof page](proofs/correctness.md), in the model above.

- **One-copy serializability (theorem).** Every history of ROWA-A, and so of plain ROWA, is 1SR, in the order of the commits. The proof has two steps. First, at the moment a writer of $x$ commits, every copy of $x$ at an up site holds its X lock and gets its value: a copy that did not answer must still be down (line L12), and a copy that answered must still be locked (line L14). So every readable copy at an up site holds the last committed value of $x$. Second, a reader of $x_A$ holds its S lock on $x_A$ until it commits, and its site does not fail in that time. So no writer of $x$ can commit between the read and the commit of the reader.
- **The validations are needed.** The example above is a history that the protocol without lines L11 to L14 accepts, and it is not 1SR.
- **The copier must be a full transaction.** A copier that writes only the recovered copy gives histories that are not 1SR. The tests find them.

## Complexity

Let $n$ be the largest number of copies of an item.

- **Messages.** A read costs 2 messages if the first copy it tries answers, and at most $2n$. A write of an item with $n$ copies costs $2n$ messages, one request and one answer per copy. A transaction with $r$ reads and $w$ writes sends at most $2(r + w)n$ messages, and exactly $2r + 2wn$ if each item has $n$ copies and each read succeeds at its first try. The atomic commitment protocol adds its own messages, for example about $4s$ for two-phase commit over $s$ sites (prepare, vote, decision and acknowledgment).
- **Rounds.** The writes to the copies of one item go out in parallel, so each operation takes one round trip when the first copy answers.
- **Space.** A transaction keeps the values it read, one epoch per granted lock and its list of missed copies, $O(r + wn)$ in all. Each site keeps an epoch number and one readable flag per copy.
- **Availability.** Plain ROWA can read while one copy is up, and it can write only while all copies are up. With $n$ copies that are each up with probability $p$, independently, a write is possible with probability $p^n$, which falls as copies are added. ROWA-A can write while one copy is up.

## Properties

- **1SR, in commit order.** Shown above.
- **Reads are cheap.** A read touches one copy, so a read-mostly workload gains from more copies.
- **Writes touch every copy.** The cost and the lock time of a write grow with $n$.
- **Not partition tolerant.** The available copies form relies on the answer "no response". If the network splits into two parts, each part can see the other as down, and two transactions can commit in the two parts with conflicting accesses on different copies of one item. BHG Section 8.8 gives such a history that is not 1SR. Plain ROWA blocks its writes instead.
- **Deadlocks.** Strict 2PL at the sites can deadlock, so the system needs detection or prevention.

## Variants and improvements

- **Quorum consensus.** [Quorum replication](/quorum-replication/) reads $q_r$ copies and writes $q_w$ copies, with $q_r + q_w > n$ and $2 q_w > n$. ROWA is the case $q_r = 1$, $q_w = n$. Quorums keep writes possible when some copies are down, and also when the network is partitioned, at the cost of more expensive reads.
- **Directory-oriented available copies.** Bernstein, Hadzilacos and Goodman (Section 8.7) also give a version that keeps a directory of the available copies of each item. A transaction writes the copies that the directory lists, and special transactions change the directory when a copy fails or is created.
- **Virtual partitions.** The sites that can talk to each other agree on a view of which sites are up, and the transactions apply ROWA inside the view. A view may read or write an item only if it holds a read or write quorum of its copies, so a read still touches one copy. BHG Section 8.10 describes this method.
- **Primary copy.** [Primary copy locking](/primary-copy-locking/) takes locks only at one copy of each item and sends the writes to the other copies. It costs fewer lock messages, and the primary is a single point of failure for its items.
- **Lazy replication.** [Lazy replication](/eager-and-lazy-replication/) writes one copy inside the transaction and the other copies after the commit. It gives up 1SR for speed.

## When to use it

Use plain ROWA when reads are much more frequent than writes, the copies are few and the sites rarely fail. Use ROWA-A when sites fail and recover but the network does not partition, for example within one machine room with a reliable failure detector. When the network can split, use quorums, a primary with a consensus protocol, or [state machine replication](/state-machine-replication/).

## Pitfalls

- **Writing all available copies without validation.** This is the error of the example. The validations at commit are what make the scheme correct, and they must run inside the atomic commitment step.
- **A copier that writes only the new copy.** The copier must conflict with readers of the other copies. Make it an ordinary transaction that reads $x$ and writes all copies of $x$.
- **Reading a recovered copy too early.** A copy that has just come back can hold a stale value. Mark it unreadable until a committed write is installed on it.
- **Trusting timeouts as failure detection.** A slow site that is taken as down breaks the argument, because it can still hold locks and values. Use the available copies form only where "down" is certain, or use quorums.
- **Losing the epoch.** Access validation needs to know that the site did not fail and recover while the transaction held its lock. A site that only checks "up now" misses a failure and recovery between the lock and the commit.

## Implementations

## History

Read-one write-all is the basic replica control rule of the early work on replicated databases. Thomas (1979) and Gifford (1979) proposed voting schemes in which a write needs only a part of the copies, so that writes go on when some copies are down. Bernstein and Goodman (1984) gave the available copies algorithm, with missing writes validation, access validation and copier transactions, and proved it correct with the theory of one-copy serializability. Bernstein, Hadzilacos and Goodman (1987) present the theory, the counterexample to the naive algorithm and the full algorithm in Chapter 8 of their book.

## References
