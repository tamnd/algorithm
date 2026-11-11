---
tag: CYTDK7
kind: theorem
slug: cap-theorem
name: CAP theorem
aliases:
- Brewer's theorem
- Brewer conjecture
- Gilbert-Lynch theorem
area: distributed/replication-and-crdts
level: intro
summary: No read/write register in an asynchronous network that may lose messages is both atomic (linearizable) and available, where every request to a live node gets an answer.
prereqs: [linearizability, asynchronous-model]
see_also: [pacelc, consistency-models, eventual-consistency, crdt, split-brain, partial-synchrony, quorum, flp-impossibility]
sources:
  - paper: doi:10.1145/564585.564601
    title: Seth Gilbert and Nancy Lynch, Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services, ACM SIGACT News 33(2), 2002
    locator: pages 51 to 59, Section 2 (the definitions of atomic, available and partition tolerant), Section 3 (Theorem 1, Corollary 1.1, and the solutions with two of the three), Section 4 (partially synchronous networks, Theorem 2, the centralized algorithm with timeouts, and the weaker consistency of Definition 3 and Theorem 4)
  - paper: doi:10.1145/343477.343502
    title: Eric A. Brewer, Towards robust distributed systems, abstract of the invited talk at PODC 2000
    locator: page 7 (the conjecture that a shared-data system can have at most two of consistency, availability and tolerance to network partitions)
  - paper: doi:10.1109/MC.2012.37
    title: Eric Brewer, CAP twelve years later, how the "rules" have changed, IEEE Computer 45(2), 2012
    locator: pages 23 to 29 (why "two of three" is misleading, partition detection, partition mode and recovery)
  - paper: "Seth Gilbert and Nancy A. Lynch, Perspectives on the CAP theorem, IEEE Computer 45(2), 2012"
    title: Seth Gilbert and Nancy A. Lynch, Perspectives on the CAP theorem, IEEE Computer 45(2), 2012
    locator: pages 30 to 36 (CAP as one case of the trade-off between safety and liveness in an unreliable network)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 9, Linearizability, the subsection on the cost of linearizability and the CAP theorem
---

The CAP theorem says that a replicated read/write register cannot be both *consistent* and *available* in a network that may *partition*. Here consistent means atomic, that is [linearizable](/linearizability/); available means that every request to a node that has not failed gets a response; and a partition is the loss of all messages between two groups of nodes. Brewer stated it as a conjecture in 2000, and Gilbert and Lynch proved it in 2002 for the [asynchronous model](/asynchronous-model/) and for a partially synchronous one. The theorem does not forbid consistency and availability when the network works; it says which one a system must give up while a partition lasts.

## Statement

**Model (Gilbert and Lynch 2002).** There are $n \ge 2$ nodes that communicate by messages. In the *asynchronous network model* there are no clocks, and nodes act only on the messages they receive and on local computation; a message may take any finite time, or be lost. No node needs to crash: the theorem holds with $f = 0$ crash failures. Clients send *requests* to nodes. The object is a read/write register with initial value $v_0$. An execution is *fair* if every node that has not failed takes infinitely many steps and every message that is sent and not lost is delivered.

- **Atomic consistency.** In every execution, there is a total order on all operations such that each operation looks as if it took effect at a single instant between its request and its response. This is linearizability.
- **Availability.** Every request received by a non-failing node results in a response. There is no time bound, but the response must come.
- **Partition tolerance.** The network may lose arbitrarily many messages sent from one node to another. A partition into groups $G_1$ and $G_2$ is the case where every message between the two groups is lost.

**Theorem 1.** In the asynchronous network model, no algorithm implements a read/write register that is available and atomic in all fair executions, including those in which messages are lost.

**Corollary 1.1.** In the asynchronous network model, no algorithm implements a read/write register that is available in all fair executions and atomic in all fair executions in which no message is lost.

**Theorem 2 (partially synchronous model).** Suppose each node has a clock, all clocks run at the same rate but are not synchronized, every message is either delivered within a known time $t_{msg}$ or lost, and each node processes a message within a known time $t_{local}$. Then no algorithm implements a read/write register that is available and atomic in all executions, including those in which messages are lost.

Consistency and availability are the safety part and the liveness part of the requirement: atomicity says that no response is ever wrong, and availability says that a response always comes.

## In plain words

A few servers keep copies of one value. Suddenly the network between two groups of servers breaks. A user writes a new value on one side. Another user then reads on the other side.

The server on the reading side has heard nothing. It has two choices. It can answer with the value it has, which is old, and then the system is not consistent. Or it can wait for news from the other side, which may never come, and then the system is not available.

No clever design avoids this choice. Whatever the reading server does, it does the same thing as in a world where no write happened at all, because from its side the two worlds look the same. When the network works, both properties are possible. The choice is only forced while the network is broken.

## Proof

*Proof of Theorem 1.* Assume that an algorithm $A$ is atomic and available in all fair executions. Split the nodes into two nonempty disjoint groups $G_1$ and $G_2$, and consider executions in which every message between $G_1$ and $G_2$ is lost.

1. Let $\alpha_1$ be the finite execution that starts with a write of a value $v_1 \ne v_0$ at a node of $G_1$, in which only nodes of $G_1$ take steps, and that ends when the write responds. The write does respond: extend $\alpha_1$ to a fair execution, in which the write gets a response by availability, and cut it there. Only $G_1$ takes steps up to that point; this is a valid prefix of a fair execution, because the asynchronous model has no bound on how long a node waits, and nodes of $G_2$ receive nothing from $G_1$ anyway.
2. Let $\alpha_2$ be the finite execution that starts in the initial state with a single read at a node of $G_2$, has no other requests, loses every message between the groups, and ends when the read responds. The read responds by availability. No write occurs in $\alpha_2$, so by atomicity the read returns $v_0$.
3. Let $\alpha$ be $\alpha_1$ followed by $\alpha_2$: first the steps of $\alpha_1$, then the steps of $\alpha_2$. In $\alpha$, the nodes of $G_2$ take no steps during $\alpha_1$, receive no message from $G_1$ at any time, and receive the same single read request as in $\alpha_2$. Their states and inputs are the same as in $\alpha_2$, step by step, so they take the same steps, and the read returns $v_0$ in $\alpha$ too.
4. In $\alpha$, the write of $v_1$ responded before the read was requested. Any total order that respects real time puts the write before the read, so the read must return $v_1$. It returns $v_0$, so $\alpha$ is not atomic. Extending $\alpha$ to a fair execution keeps this violation, which contradicts the assumption. $\square$

*Proof of Corollary 1.1.* Assume that $A$ is available in all fair executions and atomic in all fair executions without lost messages. Take $\alpha$ as above. Let $\alpha'$ be the same as $\alpha$, except that every message between the groups is delayed, not lost, until after the read responds, and then delivered. In the asynchronous model a node cannot tell a lost message from a delayed one, so every node takes the same steps in $\alpha'$ as in $\alpha$ until the read responds, and the read returns $v_0$. Extend $\alpha'$ to a fair execution in which every message is delivered. It loses no message and is not atomic, a contradiction. $\square$

*Proof of Theorem 2.* The same argument works, with one change. A node of $G_2$ now has a clock, so it could notice that it is being kept idle during $\alpha_1$. Let $\alpha_2'$ start with an idle interval as long as $\alpha_1$, in which $G_2$ receives no requests and no messages, followed by the read. The read in $\alpha_2'$ still returns $v_0$, since no write occurs. In $\alpha$ = $\alpha_1$ followed by the read, $G_2$ again sees an interval without messages followed by the read, so $\alpha$ and $\alpha_2'$ look the same to $G_2$, including the clock values. The read returns $v_0$ after the write has completed. $\square$

The implementation builds the three executions for three protocols (answer locally, forward to a primary, forward with a timeout) and checks that $G_2$ has the same view in $\alpha_2$ and in $\alpha$, and that each protocol either does not answer the read or answers $v_0$.

## Consequences

- **Partition mode.** While a partition lasts, each operation that needs data from the other side must either wait or be refused (the system keeps consistency, often called CP), or be served from local data (the system keeps availability, often called AP). Systems built on [consensus](/consensus-problem/), such as [Raft](/raft/) or [Paxos](/paxos/), keep consistency and serve only the side that has a [quorum](/quorum/); the minority side is unavailable. [Dynamo-style stores](/dynamo-style-replication/) and [CRDTs](/crdt/) keep availability and give [eventual consistency](/eventual-consistency/).
- **Sequential consistency is not enough to escape.** In the proof, the read returns $v_0$ after the write, which a sequentially consistent register allows. With two registers the theorem still holds: under a partition, $G_1$ writes $x = 1$ and reads $y$, and $G_2$ writes $y = 1$ and reads $x$. Each read happens on a side that cannot tell whether the other write occurred, so both return 0, which is the store-buffer history that no sequentially consistent execution allows (see [consistency models](/consistency-models/)).
- **What can be available.** Mahajan, Alvisi and Dahlin (2011) showed that no model stronger than real-time causal consistency can be both always available and one-way convergent. [Causal consistency](/causal-consistency/), [session guarantees](/session-guarantees/) for sessions that stay on one side, and [strong eventual consistency](/strong-eventual-consistency/) are all available under partitions.
- **Safety against liveness.** Gilbert and Lynch (2012) present CAP as one case of a general fact: in an unreliable network, a service cannot guarantee both a safety property (no wrong answer) and a liveness property (an answer always comes). The [FLP theorem](/flp-impossibility/) is another case.
- **Latency.** The theorem is silent when there is no partition. [PACELC](/pacelc/) adds the trade-off that remains then: consistency costs latency.

## Tightness

- **Any two of the three are possible (Section 3.2).** *Atomic and partition tolerant:* a centralized algorithm, in which one node stores the value and the other nodes forward requests to it and wait. It is always atomic, and under a partition the requests on the other side never get an answer. *Available and partition tolerant:* every node answers from its local copy, or even always returns $v_0$. *Atomic and available:* the centralized algorithm when no message is lost.
- **Partial synchrony helps a little.** Corollary 1.1 is false in the partially synchronous model (Section 4.3). A centralized algorithm in which a node waits $2 t_{msg} + t_{local}$ for the central node, and then answers from what it knows, is available always and atomic in every execution without lost messages. Gilbert and Lynch also give a weaker consistency condition that such an algorithm meets (Definition 3 and Theorem 4): if no message is lost for longer than a time $t$, operations separated by that interval are seen in order. The source calls it Delayed-$t$ consistency in some versions and $t$-Connected consistency in others.
- **Weaker availability.** If only the nodes in a majority must answer, consensus-based replication is atomic and available on the majority side of any partition. The theorem needs every non-failing node to answer.
- **One group is not enough.** The proof needs two nonempty groups that cannot talk, so $n \ge 2$. A single node is trivially atomic and available.

## History

Fox and Brewer discussed the trade-off between consistency and availability in the late 1990s, and Brewer stated the conjecture in his keynote talk at PODC 2000: of consistency, availability and partition tolerance, a shared-data system can have at most two. Gilbert and Lynch gave the formal definitions and the proof in 2002, with the first precise meaning of the three words. In 2012, a special issue of IEEE Computer revisited it: Brewer explained that partitions are rare and that the choice applies only during them, Gilbert and Lynch framed it as safety against liveness, and Abadi proposed [PACELC](/pacelc/). The informal "pick two of three" is often criticized, because partitions are not optional in a real network: the real choice is what to do while one lasts.

## References
