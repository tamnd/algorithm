---
tag: AFV0QQ
kind: theorem
slug: pacelc
name: PACELC
aliases:
- PACELC
area: distributed/replication-and-crdts
level: advanced
summary: Under a partition a replicated store trades availability for consistency; else it trades latency for consistency, since sequential consistency needs |W| + |R| ≥ d.
prereqs: [cap-theorem, sequential-consistency, linearizability]
see_also: [cap-theorem, consistency-models, eventual-consistency, quorum-replication, dynamo-style-replication, replicated-state-machine, clock-skew, partial-synchrony]
sources:
  - paper: doi:10.1109/MC.2012.33
    title: Daniel J. Abadi, Consistency tradeoffs in modern distributed database system design, IEEE Computer 45(2), 2012
    locator: pages 37 to 42 (the PACELC formulation, the latency argument from replication, and the classification of Dynamo, Cassandra, Riak, PNUTS, MongoDB, VoltDB, H-Store and Megastore)
  - paper: doi:10.1145/176575.176576
    title: Hagit Attiya and Jennifer L. Welch, Sequential consistency versus linearizability, ACM Transactions on Computer Systems 12(2), 1994
    locator: pages 91 to 122, Theorem 3.1 (|W| + |R| ≥ d for sequential consistency, due to Lipton and Sandberg), the algorithms with a local read or a local write, and the lower bounds u/4 for reads and u/2 for writes of linearizable registers with approximately synchronized clocks
  - paper: "Richard J. Lipton and Jonathan S. Sandberg, PRAM, a scalable shared memory, Princeton University technical report CS-TR-180-88, 1988"
    title: Richard J. Lipton and Jonathan S. Sandberg, PRAM, a scalable shared memory, 1988
    locator: Theorem 1 (the lower bound on the response time of sequentially consistent memory)
  - paper: doi:10.1145/564585.564601
    title: Seth Gilbert and Nancy Lynch, Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services, ACM SIGACT News 33(2), 2002
    locator: pages 51 to 59, Theorem 1 (the partition half of PACELC)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 9, the lower bounds on the response times of sequentially consistent and linearizable shared memory
---

PACELC extends the [CAP theorem](/cap-theorem/) with the case that CAP leaves out. It reads: if there is a Partition, a replicated store trades Availability against Consistency; Else, when the network works, it trades Latency against Consistency. Abadi proposed it in 2012 as a way to classify systems. Its first half is the CAP theorem, and its second half rests on an older lower bound of Lipton and Sandberg (1988), proved formally by Attiya and Welch (1994): in a network with message delay $d$, any sequentially consistent memory has a write time plus a read time of at least $d$, even with no failures at all.

## Statement

**Model.** There are $n \ge 2$ processes that implement shared read/write registers by sending messages. Every message is delivered, and its delay lies in $[d - u, d]$, where $d > 0$ is the largest delay and $u \ge 0$ the uncertainty. Each process has at most one operation pending at a time. $|W|$ and $|R|$ are the worst-case response times of a write and a read, over all executions. There are no crashes ($f = 0$) and no lost messages: this is the "else" case. For the partition case, use the model of the CAP theorem, in which messages may be lost.

**The PACELC classification (Abadi 2012).** A replicated data store makes two choices. *PA or PC:* when a partition separates the replicas, it either answers every request (availability) or keeps consistency and refuses some requests. *EL or EC:* when there is no partition, it either answers fast from nearby replicas (low latency) or waits for remote replicas (consistency). The classification is a design statement, not a theorem by itself. The two facts that force the choices are below.

**Fact P (CAP, Gilbert and Lynch 2002).** In an asynchronous network that may lose messages, no read/write register is both linearizable and available.

**Fact E (Lipton and Sandberg 1988; Attiya and Welch 1994, Theorem 3.1).** Any sequentially consistent implementation of two read/write registers $X$ and $Y$ has $|W| + |R| \ge d$. This holds even when clocks are perfect and every delay is exactly $d$ (so $u = 0$).

**Fact E for linearizability (Attiya and Welch 1994, Section 4).** With clocks that are only approximately synchronized, any linearizable implementation of a register with at least two readers has $|R| \ge u/4$, and with at least two writers has $|W| \ge u/2$.

Consistency is a safety property and latency a performance measure: Fact E says that no amount of engineering makes a sequentially consistent store respond in less than one message delay per write and read together.

## In plain words

A store keeps copies of its data in several places. When the network between them breaks, the CAP theorem forces a choice: answer anyway with data that may be old, or refuse.

PACELC says that the choice does not go away when the network works. A store can only give all users one agreed order of events if each write or each read waits for a message to cross the network. So a store that answers at once from the nearest copy cannot keep that order. A store that keeps it must make some requests wait at least one network trip.

Systems therefore get two labels. The first says what they do during a break: stay available or stay consistent. The second says what they do the rest of the time: answer fast or stay consistent.

## Proof

Fact P is the CAP theorem; see its [proof](/cap-theorem/). The proof of Fact E is short.

*Proof of Fact E.* Let $p$ and $q$ be two processes and suppose, for a contradiction, that a sequentially consistent implementation has $|W| + |R| < d$. Let both registers start at 0. Consider executions in which every message takes exactly $d$, which is allowed for every $u \ge 0$, and in which the processes are deterministic.

1. Let $\alpha_1$ be the execution in which $p$ invokes WRITE$(X, 1)$ at time 0 and, as soon as it returns, invokes READ$(Y)$, and $q$ invokes nothing. The write returns by time $|W|$ and the read by time $|W| + |R| < d$. No write to $Y$ happens, so the read of $Y$ returns 0 in every sequentially consistent history.
2. Let $\alpha_2$ be the symmetric execution: $q$ writes $Y = 1$ at time 0 and then reads $X$, and $p$ invokes nothing. The read of $X$ returns 0, for the same reason.
3. Let $\alpha$ be the execution in which both do their operations from time 0. Every message is sent at time 0 or later, so it arrives at time $d$ or later. Up to time $|W| + |R| < d$, process $p$ receives no message from $q$ in $\alpha$, and none in $\alpha_1$, and it has the same inputs at the same times in both. So $p$ takes the same steps and its read of $Y$ returns 0 in $\alpha$. In the same way, $q$'s read of $X$ returns 0 in $\alpha$.
4. The history of $\alpha$ is $p$: $w(X)1, r(Y)0$ and $q$: $w(Y)1, r(X)0$. Take any total order of these four operations that respects program order, and look at the read that comes last in it. It comes after the write of its own process, and after the other read, which comes after the write of the other process. So it comes after both writes, and in particular after the write to the register it reads, and a legal order makes it return 1. Both reads return 0, so no legal order exists and $\alpha$ is not sequentially consistent, a contradiction. $\square$

The bound needs only the gap between "a message is in flight" and "the operation has returned". Partitions, crashes and clock errors play no part, which is why it applies to the "else" branch.

## Consequences

- **Low latency means weak consistency.** A store that serves both reads and writes from the local replica, without waiting for any message, has $|W| + |R|$ close to 0 and so cannot be sequentially consistent, let alone linearizable. Such stores give [eventual consistency](/eventual-consistency/), [causal consistency](/causal-consistency/) or [session guarantees](/session-guarantees/), which have no such bound.
- **Consistency costs a round trip on some operation.** A linearizable store such as a [replicated state machine](/replicated-state-machine/) pays at least one message delay on writes or on reads, and in geo-replicated systems this delay is tens or hundreds of milliseconds.
- **Classification of systems (Abadi 2012).** In their default settings, Dynamo, Cassandra and Riak are PA/EL: they stay available under partitions and answer fast otherwise. Fully ACID systems such as VoltDB, H-Store and Megastore are PC/EC, and so are BigTable and HBase. MongoDB was classified PA/EC and Yahoo's PNUTS PC/EL. These labels describe defaults; many systems let each request choose, for example through the quorum sizes of [quorum replication](/quorum-replication/).
- **Quorums move the cost.** In [Dynamo-style](/dynamo-style-replication/) stores with $N$ replicas, read quorum $R$ and write quorum $W$, the setting $R + W > N$ makes reads see the last completed write, and each operation waits for the slowest replica in its quorum; $R = W = 1$ is fast and weak.

## Tightness

- **The bound $d$ is reached.** With perfect clocks and constant delays, Attiya and Welch give two linearizable algorithms: one in which reads are local ($|R| = 0$) and writes take time $d$, and one in which writes are local and reads take time $d$. So $|W| + |R| = d$ is achievable, and a designer can choose which operation is slow.
- **Linearizability costs more with clock uncertainty.** With approximately synchronized clocks, the bounds $u/4$ and $u/2$ show that neither operation of a linearizable register can be instant, while sequential consistency can still make one of them instant. Mavronicolas and Roth (1999) sharpened these bounds.
- **Two registers are needed.** The proof uses two registers and two processes. For a single register with a single writer and FIFO channels, local reads and local writes are already sequentially consistent: each reader sees the writer's values in the writer's order, so each read can be placed between the two writes that it falls between.
- **The classification is coarse.** PACELC names two binary choices, but real systems offer a range of models between the ends, and some choose per operation.

## History

Lipton and Sandberg proposed PRAM memory in 1988 as a scalable alternative to sequential consistency and showed that sequential consistency costs a message delay. Attiya and Welch gave the formal proof in 1991 (SPAA, journal version 1994), together with the matching algorithms and the bounds for linearizability, and Mavronicolas and Roth improved them in 1999. Abadi argued in 2012, in the IEEE Computer issue on the CAP theorem, that the latency trade-off had shaped the design of distributed databases more than partitions, and proposed PACELC to make it explicit.

## References
