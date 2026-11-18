---
tag: SBHSMT
kind: algorithm
slug: primary-copy-locking
name: Primary copy locking
aliases:
- primary site locking
- primary copy two-phase locking
area: databases/distributed-databases
level: core
summary: "Distributed two-phase locking in which each item has one primary copy whose site grants all locks on the item."
solves: [concurrency-control]
model: asynchronous-model
complexity:
  vars: {n: the largest number of copies of an item, r: the number of reads of a transaction, w: the number of writes of a transaction}
  messages: {worst: "3r + w(2n + 1)"}
  space: {extra: "O(r + w n)"}
properties: {deterministic: true, recursive: false}
history:
  year: 1979
  people: [Michael Stonebraker]
  note: "Stonebraker (1979) proposed the primary copy method for the copies of data in distributed INGRES. Bernstein and Goodman (1981) described it as primary copy 2PL in their survey of distributed concurrency control."
prereqs: [strict-two-phase-locking, one-copy-serializability]
see_also: [read-one-write-all, quorum-replication, primary-backup-replication, eager-and-lazy-replication, two-phase-commit, deadlock-detection, lock-table, chandy-misra-haas]
sources:
  - paper: doi:10.1145/356842.356846
    title: "Philip A. Bernstein and Nathan Goodman, Concurrency control in distributed database systems, ACM Computing Surveys 13(2), 1981, pages 185 to 221"
    locator: "Section 3.2, Primary Copy 2PL (the message costs of reads and writes compared with basic 2PL), Section 3.4, Centralized 2PL, and Section 5.1, the methods that combine primary copy 2PL with other techniques"
  - paper: doi:10.1109/TSE.1979.234180
    title: "Michael Stonebraker, Concurrency control and consistency of multiple copies of data in distributed INGRES, IEEE Transactions on Software Engineering SE-5(3), 1979, pages 188 to 194"
    locator: the primary copy scheme for the multiple copies of data in distributed INGRES
  - book: isbn:9780201107159
    title: "Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987"
    locator: "Chapter 8, Replicated Data, Section 8.3 (the definition of one-copy serializability used in the proof)"
---

Primary copy locking is a form of distributed [two-phase locking](/two-phase-locking/) for replicated data. Each item has several copies, and one of them is the primary copy. Only the site of the primary copy keeps locks for the item. A transaction locks the item at that site before it reads any copy or writes the item. At commit it sends its writes to every copy, and the primary releases the locks only when all copies have the new value. This gives [one-copy serializability](/one-copy-serializability/) with one lock request per item, not one per copy as in [read-one write-all](/read-one-write-all/). The cost is an extra message for a read of a copy that is not the primary, and the primary site is a single point of failure for its items.

## In plain words

A library has several copies of a book in different rooms. Only the front desk keeps the list of who has borrowed the book, and you ask the front desk before you open any copy. To change the book, you get permission at the desk, give the new page to every room, and wait until each room says that it has the page. Only then does the desk let the next person in.

Because every reader and writer of the book passes through the one desk, they never see the book in a half-changed state, even when they read different copies. If the desk is closed, nobody can use the book.

## The problem

A database holds items $x, y, \dots$, and each item has copies at a fixed set of sites. The system must run transactions so that the history is [one-copy serializable](/one-copy-serializability/). Transactions run at a home site and send messages to the other sites. The model is the [asynchronous model](/asynchronous-model/): messages take any time and are not lost, and each channel between two sites is first in, first out. Sites can fail by stopping ([crash failure](/crash-failure/)) and stay down, and a message to a failed site comes back as "no response". The page assumes that at least one copy of each item stays up.

For each item $x$, a fixed copy is the *primary copy*, at the site $P(x)$. The site $P(x)$ runs a [lock table](/lock-table/) for $x$ with S (shared) and X (exclusive) locks. Two locks of different transactions conflict unless both are S.

## The algorithm

```pseudo id=main
PRIMARY-COPY-TRANSACTION(T)
L1  for each operation of T, in order do
L2      if the operation is a read of x then
L3          ask the site P(x) for an S lock on x
L4          read one copy of x: the copy at the home site of T if there is one, else the primary copy
L5      else                                         ▷ a write of x
L6          ask the site P(x) for an X lock on x; compute the new value of x
L7  commit T                                         ▷ T holds all its locks here
L8  send the new value of each written x to every copy of x except the primary copy
L9  wait until each of these copies has acknowledged or is found down
L10 tell each primary site to install the new values on its primary copies and release the locks of T
```

A read of the primary copy is one message: the lock request asks the primary to read the copy and send the value with the grant. A read of a local copy needs the lock at the primary and then a local read, which sends no message. If the local copy is down, the transaction reads the primary copy instead, still under its S lock. A transaction that reads and then writes an item upgrades its S lock to an X lock.

If a lock request gets "no response", the primary of the item is down and the transaction aborts. A transaction that holds or waits for a lock at a primary that fails, and has not reached line L7, also aborts. An abort sends a release to every primary site that the transaction asked. A transaction that has passed line L7 goes on to the end. The atomic commitment of a transaction whose writes span several primary sites, for example by [two-phase commit](/two-phase-commit/), is outside the pseudocode: line L7 is one decision.

**Deadlocks.** The primaries are separate lock managers, so a cycle of waits can span several sites. The code uses a central detector that reads the lock tables of all up sites, builds the [wait-for graph](/wait-for-graph/) and aborts the transaction with the largest id in each cycle. A distributed detector such as [Chandy-Misra-Haas](/chandy-misra-haas/) can do the same job.

## Example

The items are $x$ with copies at $A$ (primary), $B$ and $C$, $y$ with copies at $B$ (primary) and $C$, and $z$ with copies at $A$ (primary) and $C$. The counts below are from the code, and they count only messages between different sites.

**A write.** $T_1 = w_1[x]$ runs at site $D$, which holds no copy. It sends a lock request to $A$ and gets the grant (2 messages). At commit it sends the new value 100 to $x_B$ and $x_C$ and gets two acknowledgments (4 messages). Then it sends one release to $A$, which installs 100 on $x_A$ and drops the lock (1 message). That is 7 messages, and all three copies hold 100. Read-one write-all would lock all three copies: 6 messages before the commit protocol.

**Reads.** $T_1 = r_1[x]$ at site $B$ locks $x$ at $A$ and reads the local copy $x_B$: 2 messages for the lock and 1 for the release. The same read at site $A$ costs nothing. A read of $y$ at site $A$, which holds no copy of $y$, sends the lock request to $B$, and the grant carries the value of $y_B$: again 2 messages and 1 release. Under read-one write-all, the read at $B$ would cost no message at all, which is the extra cost of primary copy reads that Bernstein and Goodman point out.

**Why the primary waits for the acknowledgments.** In the code, the flag early_release makes the primary release the X lock when the new values are sent, not when they are acknowledged. With 3 random transactions per run, 1 of 200 runs gives a history that is not 1SR. In that run, $T_3 = w_3[x]$ runs at $D$ and $T_2 = r_2[x]\, w_2[x]$ runs at $C$:

$$c_3\; w_3[x_A]\; r_2[x_C]\; w_3[x_B]\; w_3[x_C]\; c_2\; w_2[x_A]\; w_2[x_B]\; w_2[x_C]$$

$T_3$ commits and the primary $A$ installs its value and releases the lock at once. $T_2$ gets the lock at $A$ and reads its local copy $x_C$ before the value of $T_3$ arrives there. So $T_2$ reads the initial value of $x$, and its write then overwrites the write of $T_3$: a lost update. In the order $T_3\, T_2$, $T_2$ would read from $T_3$; in the order $T_2\, T_3$, the last write of $x$ would be by $T_3$, but every copy ends with the value of $T_2$. With the acknowledgments, all 200 runs are 1SR in commit order.

## Correctness

The proofs are on [the proof page](proofs/correctness.md).

- **One-copy serializability (theorem).** Every history is 1SR, in the order of the commits (line L7). The X lock of a writer at the primary covers the installs at all copies (lines L8 to L10), and the S lock of a reader covers its read. So a reader sees the value of the last writer that committed before it, at any copy it reads, and conflicting transactions are ordered at the primary in the order of their commits.
- **Failures.** A failed primary grants no more locks, so its items stop, but the history stays 1SR. The tests inject one site failure at a random step in 200 runs, and all histories are 1SR in commit order. A copy at a failed site misses writes, and the code never reads it again, because the site never comes back.

## Complexity

- **Messages.** A read costs 2 messages to the primary, or none if the home site is the primary. A write of an item with $n$ copies costs 2 for the lock and $2(n - 1)$ for the installs and acknowledgments. The release costs one message per primary site. A transaction with $r$ reads and $w$ writes, at a home site with no copies and with all its items at different primaries, sends at most $3r + w(2n + 1)$ messages.
- **Compared with read-one write-all.** For a write, ROWA sends $2n$ lock messages and then the commit protocol sends values to the $n$ copies. Primary copy sends 2 lock messages, and the values go to the copies at commit. For a read of a local copy that is not the primary, ROWA sends nothing and primary copy sends 2 messages. So primary copy wins when writes are frequent, and ROWA wins for local reads.
- **Space.** Each primary site keeps the lock table of its items only. A transaction keeps its reads and the new values of its writes, $O(r + w)$, and $O(w n)$ entries for the acknowledgments it waits for.

## Properties

- **1SR, in commit order.** Shown above.
- **One lock per item.** No copy other than the primary has a lock table for the item.
- **A single point of failure per item.** When the primary site is down, the item cannot be read or written, even when other copies are up. The method alone has no way to move the primary.
- **Load on the primary.** All lock traffic for an item goes to one site. Placing the primaries of different items at different sites spreads the load.
- **Deadlocks.** Two-phase locking at the primaries can deadlock across sites, so the system needs detection or prevention.

## Variants and improvements

- **Centralized 2PL.** One site keeps the locks of all items. Bernstein and Goodman (1981, Section 3.4) describe it and note that Alsberg and Day call this the *primary site* method. It is primary copy locking with the same primary site for every item, so the alias "primary site locking" also names this special case.
- **Primary copy for write-write conflicts only.** The survey (Section 5.1) lists combinations in which primary copy 2PL orders writes against writes, while another method, for example basic 2PL, orders reads against writes. With basic 2PL for reads, a reader locks only the copy it reads.
- **A primary that moves.** If the primary fails, the other copies can elect a new primary. This needs a protocol that agrees on the new primary and on the last committed writes, such as the view change of [primary-backup replication](/primary-backup-replication/) or a consensus protocol like [Raft](/raft/) or [Paxos](/paxos/). Each group of copies of a shard then acts as one replicated lock manager, as in many sharded databases.
- **Lazy primary copy.** The primary commits a transaction alone and sends the writes to the other copies after the commit. This is the lazy master scheme of [eager and lazy replication](/eager-and-lazy-replication/). Reads of the other copies can then be stale, so the history is no longer 1SR unless reads also go to the primary.

## When to use it

Use primary copy locking when an item has several copies, writes are not rare and the sites rarely fail, and you want one lock manager per item instead of one per copy. Put the primary of each item at the site that writes it most. Do not use it when local reads must be free of messages, or when the items must stay available while their primary is down; then use a quorum method or a primary that moves by consensus.

## Pitfalls

- **Releasing before the copies have the value.** If the primary releases the X lock when the writes are only sent, a reader can lock the item and read a copy that has not got the new value. The example shows the lost update that follows.
- **Reading without the lock.** A read of a local copy without the S lock at the primary is cheap, but it can see a value in the middle of a write, or one that is about to change. This is what lazy replication does, and it is not 1SR.
- **Messages that pass each other.** An abort sends a release after a lock request to the same site. If channels are not first in, first out, the release can arrive first and leave a lock that is never released. The code delivers in order on each channel.
- **A primary that is only slow.** If a slow primary is taken for down and a new primary is chosen, the two can grant conflicting locks. Moving the primary needs agreement, not a timeout alone.

## Implementations

## History

Stonebraker (1979) proposed the primary copy method for distributed INGRES, to keep the copies of data consistent with locks at one copy. Alsberg and Day (1976) had earlier proposed a primary site scheme for the resilient sharing of distributed resources, which the survey files under centralized 2PL. In their 1981 survey, Bernstein and Goodman described primary copy 2PL beside basic, voting and centralized 2PL, and compared their message costs. Later systems kept the idea of one lock manager per item or per shard, and made the primary fault tolerant with replication protocols such as Paxos.

## References
