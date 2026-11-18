---
tag: MPEKG5
kind: concept
slug: highly-available-transactions
name: Highly available transactions
aliases:
- HAT
area: databases/distributed-databases
level: research
summary: "The isolation and session guarantees that a replicated database can give while each client still gets an answer during network partitions that may never heal."
prereqs: [isolation-levels, cap-theorem]
see_also: [ramp-transactions, invariant-confluence, session-guarantees, causal-consistency, snapshot-isolation, one-copy-serializability, linearizability, eventual-consistency]
sources:
  - paper: doi:10.14778/2732232.2732237
    title: "Peter Bailis, Aaron Davidson, Alan Fekete, Ali Ghodsi, Joseph M. Hellerstein and Ion Stoica, Highly available transactions, virtues and limitations, Proceedings of the VLDB Endowment 7(3), 2013, pages 181 to 192"
    locator: "Section 3 and Table 2 (default isolation of 18 databases), Section 4 (high, sticky and transactional availability), Section 5 (achievable and unachievable guarantees), Table 3 and Figure 2 (summary), Section 6 (TPC-C and the prototype)"
  - paper: doi:10.1145/564585.564601
    title: "Seth Gilbert and Nancy Lynch, Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services, ACM SIGACT News 33(2), 2002, pages 51 to 59"
    locator: "the definition of availability that the HAT paper adopts, and the partition argument"
---

A highly available transaction (HAT) is a transaction that a replicated database can run under a guarantee that still lets every client get an answer while the network is split. Bailis, Davidson, Fekete, Ghodsi, Hellerstein and Stoica (2013) went through the common isolation levels and session guarantees and sorted them in three groups: those that any highly available system can give, those that need a client to stay with the same server, and those that no highly available system can give. The line between the groups is a theorem in the asynchronous model, where messages can be delayed without bound and a partition can last forever.

## In plain words

Picture a database copied to two data centers, and a cut cable between them. Each side can keep answering its own clients, or it can wait for the other side. The [CAP theorem](/cap-theorem/) says that answering forever and staying [linearizable](/linearizability/) cannot both hold. That result is about single reads and writes of fresh data, and it says little about transactions.

The HAT work asks the transaction question. Some guarantees need no talk across the cut: never show uncommitted writes, show all the writes of a transaction or none of them, never let a read go back in time. Others need it: stop two transactions on opposite sides from both changing the same balance, or always read the newest value. [Serializability](/serializability/) and [snapshot isolation](/snapshot-isolation/) are in the second group, and many weaker levels that real databases use are in the first.

## The idea

**The model.** Data items are replicated on servers, and possibly partitioned over them. Clients send the operations of a transaction to servers. The network is asynchronous: a message can be delayed for any finite time, and during a partition it can be delayed forever. Servers can crash. The definitions below follow Section 4 of the paper.

- **High availability.** Every client that can contact a correct server for each item that it uses eventually gets a response from that server, even under arbitrary partitions of any length between servers. This is the availability of Gilbert and Lynch.
- **Sticky availability.** The same promise, but only for a client that always contacts servers that have seen all its earlier operations. A client gets this by staying with one replica of the whole database, or by caching its own writes and acting as a server for itself.
- **Transactional availability.** A transaction that can reach a replica of each item it uses eventually commits or aborts. An abort that the transaction asks for, such as a user rollback, is *external*; an abort that the system decides is *internal*. The system may abort a transaction internally to keep the guarantee, but it must not keep aborting it forever.

A guarantee is *HAT-compliant* if some system gives it with transactional availability. The answer for each guarantee comes from Section 5 and Table 3 of the paper.

**Guarantees that a highly available system can give.**

- **Read uncommitted** (Adya's PL-1, no dirty writes). Writes to each item are applied in one order, and the orders of different items agree. A system can stamp all writes of a transaction with one unique timestamp and let the last writer win at each replica.
- **Read committed** (PL-2, no dirty reads). A transaction never reads an uncommitted or intermediate value. The client keeps its writes until commit, or the servers keep them hidden until they learn of the commit. This gives the definition of read committed, but not the recency that a lock-based read committed gives as a side effect.
- **Monotonic atomic view (MAV).** Once a transaction sees one effect of another transaction, it sees all of them. The paper sketches an algorithm in which the writes of a transaction carry one timestamp and the list of items written, and a replica reveals a write only when every replica of the items in the transaction has received its part ("pending stable"). A reader uses the timestamp and the list to ask for at least that version of the other items. No server waits for another, so the system stays available. [RAMP transactions](/ramp-transactions/) work out this idea in full.
- **Item cut isolation and predicate cut isolation.** A transaction that reads an item, or a predicate, twice sees the same result each time. This is the ANSI definition of repeatable read without its lock-based extras, and the client can give it by keeping a copy of what it read.
- **Three session guarantees:** [monotonic reads](/monotonic-reads/), monotonic writes and writes follow reads.

**Guarantees that need sticky availability.** [Read your writes](/read-your-writes/), PRAM (monotonic reads, monotonic writes and read your writes) and [causal consistency](/causal-consistency/) (PRAM with writes follow reads). If a client writes $x$ on one server, and then the partition sends it to a server that has not received the write, that server can either answer without the write or wait. So these guarantees are not available in general, but they are available to a client that stays with its servers.

**Guarantees that no highly available system can give** (Section 5.2):

- those that prevent **lost update**: cursor stability, [snapshot isolation](/snapshot-isolation/), repeatable read in the lock-based sense, and [one-copy serializability](/one-copy-serializability/);
- those that also prevent **[write skew](/write-skew/)**: repeatable read in the lock-based sense, one-copy serializability and strong one-copy serializability;
- those that need **recency**, a bound on how stale a read can be: safe, regular and atomic registers, [linearizability](/linearizability/), and strong one-copy serializability.

The proof for lost update is the partition argument of Gilbert and Lynch. Put two clients on opposite sides of a partition that never heals, and let each run a transaction that reads $x$ and writes a new value based on it. Each side must respond, so each transaction commits or aborts on its own. An internal abort is allowed only finitely often, so both commit in some run. Neither saw the other's write, so one of the updates is lost. Write skew is the same argument with two items. Recency fails because a server on the far side of the partition cannot learn of a write that it must return. These are theorems, and they hold only in the asynchronous model with partitions that can last forever: if a bound on message delay is assumed, the argument does not apply.

**Durability.** A client that wants its writes to survive $F$ server faults must reach $F + 1$ servers before it commits. Under the definition above, a client may be able to reach only one server, so durability beyond $F = 1$ is not highly available (Section 5.2.3).

**Combinations.** Figure 2 of the paper orders the guarantees in a partial order, and the HAT guarantees can be combined. With all of them and sticky availability, a client gets causally consistent, transactional snapshot reads. The diagram allows 144 combinations of HAT-compliant guarantees.

## Examples

**Lost update.** The paper's example (Section 5.2): $x$ is 100 on both sides of a partition. $T_1$ reads 100 and writes 120 (a deposit of 20); $T_2$ reads 100 and writes 130 (a deposit of 30). Both commit. When the partition heals, last writer wins gives 120 or 130, and one deposit is lost. A serial run gives 150. Under read committed, MAV and cut isolation this run is allowed, which is why those levels are available.

**Write skew.** $T_1$ reads $y = 0$ and writes $x = 1$; $T_2$ reads $x = 0$ and writes $y = 1$. Each one alone keeps the rule "at most one of $x$, $y$ is 1", and each runs on its own side of the partition. Both commit, and the rule is broken. Snapshot isolation also allows this run, even with no partition. Serializability forbids it, so serializability is not available.

**MAV.** $T_1$ writes $x = 1$, $y = 1$ and $z = 1$. A transaction $T_2$ that reads $y = 1$ must then read $x$ and $z$ as 1 or a later version. Before it reads $y$ it may see the old $x$, so MAV is weaker than a snapshot; the values move forward together once seen.

**TPC-C.** Section 6.2 checks the five TPC-C transactions. The two read-only ones (Order-Status and Stock-Level) run as HATs. Payment and Delivery need care with non-monotonic updates. New-Order must assign order numbers in sequence within a district, which needs lost update prevention, so a HAT system can keep the numbers unique but not sequential. The paper says in one place that four of the five transactions can be HATs and in another that New-Order and Payment are the two hard cases; the safe reading is that most of the work is available and a small part is not.

**Measurements.** These are measurements from the paper's prototype (a partitioned key-value store on LevelDB, in Java), with YCSB grouped into transactions of 8 operations, half reads, on Amazon EC2 m1.xlarge servers, 5 per cluster, published in 2013. With two clusters in one data center, routing each key to a master gave about half the throughput and double the latency of plain eventual consistency, and MAV gave about 75 percent of its throughput. With the two clusters in data centers across the continental United States, the average latency of the master configuration rose to about 300 ms while the HAT configurations stayed close to their single data center numbers. The abstract states that the latency gain is often two to three orders of magnitude over wide-area networks.

## Where it is used

- **Weak isolation in practice.** The survey in Section 3 (Table 2) found that only 3 of 18 databases default to serializability and 8 do not offer it at all. Read committed is a common default, and it is available, so many deployed applications already accept HAT-level guarantees.
- **Multi-partition atomic visibility.** [RAMP transactions](/ramp-transactions/) give read atomic isolation, a form of MAV, without coordination.
- **Deciding when coordination is needed.** [Invariant confluence](/invariant-confluence/) asks the same question per application: which invariants can survive HAT-style execution and merging. The [CALM theorem](/calm-theorem/) asks it for monotone programs.
- **Geo-replicated stores.** Systems that offer [causal consistency](/causal-consistency/) or [session guarantees](/session-guarantees/) with clients pinned to a data center use sticky availability.

## References
