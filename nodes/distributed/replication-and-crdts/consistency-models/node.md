---
tag: RP1X08
kind: concept
slug: consistency-models
name: Consistency models
aliases:
- consistency spectrum
- memory consistency models
area: distributed/replication-and-crdts
level: core
summary: Formal contracts on what values reads may return, ordered from linearizability through sequential, causal and PRAM consistency down to eventual consistency.
prereqs: [linearizability, sequential-consistency, happened-before]
see_also: [causal-consistency, eventual-consistency, strong-eventual-consistency, session-guarantees, cap-theorem, pacelc, quiescent-consistency, serializability]
sources:
  - paper: doi:10.1145/78969.78972
    title: Maurice P. Herlihy and Jeannette M. Wing, Linearizability, a correctness condition for concurrent objects, ACM TOPLAS 12(3), 1990
    locator: pages 463 to 492, Section 2 (histories and the definition of linearizability) and Section 3 (locality, and the example that sequential consistency is not local)
  - paper: doi:10.1109/TC.1979.1675439
    title: Leslie Lamport, How to make a multiprocessor computer that correctly executes multiprocess programs, IEEE Transactions on Computers C-28(9), 1979
    locator: pages 690 to 691 (the definition of sequential consistency)
  - paper: doi:10.1007/BF01784241
    title: Mustaque Ahamad, Gil Neiger, James E. Burns, Prince Kohli and Phillip W. Hutto, Causal memory, definitions, implementation, and programming, Distributed Computing 9(1), 1995
    locator: pages 37 to 49 (the causality order, the definition of causal memory, and its place between sequential consistency and PRAM)
  - paper: "Richard J. Lipton and Jonathan S. Sandberg, PRAM, a scalable shared memory, Princeton University technical report CS-TR-180-88, 1988"
    title: Richard J. Lipton and Jonathan S. Sandberg, PRAM, a scalable shared memory, 1988
    locator: the definition of PRAM consistency and the lower bound for sequential consistency
  - paper: doi:10.1145/2926965
    title: Paolo Viotti and Marko Vukolić, Consistency in non-transactional distributed storage systems, ACM Computing Surveys 49(1), 2016
    locator: Article 19, Sections 2 and 3 (the framework of histories, visibility and arbitration, and the partial order of more than 50 models)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 9 (distributed shared memory, linearizability, sequential consistency and their costs)
  - paper: "Prince Mahajan, Lorenzo Alvisi and Mike Dahlin, Consistency, availability, and convergence, University of Texas at Austin technical report UTCS TR-11-22, 2011"
    title: Prince Mahajan, Lorenzo Alvisi and Mike Dahlin, Consistency, availability, and convergence, 2011
    locator: Section 2 (stronger as a strict subset of executions, real-time causal consistency) and Theorem 3.1 (no model stronger than real-time causal is always available and one-way convergent)
---

A consistency model is a contract between a shared or replicated store and its clients: it says which values the reads in a history may return. Models are compared by the sets of histories they allow, and model $A$ is *stronger* than model $B$ when $A$ allows a strict subset of the histories that $B$ allows. For read/write registers the main chain is [linearizability](/linearizability/) $\subset$ [sequential consistency](/sequential-consistency/) $\subset$ [causal consistency](/causal-consistency/) $\subset$ PRAM, with [eventual consistency](/eventual-consistency/) at the weak end and the client-centric [session guarantees](/session-guarantees/) on a separate axis. Stronger models are easier to program against, and weaker models can answer during network partitions and without waiting for remote replicas.

## In plain words

Copies of the same data live on several machines. When a program reads, which value may it see? A consistency model is the rule that answers this question.

The strictest rule says the copies must act like one copy: a read sees every write that finished before it began. A weaker rule lets the order differ from the clock, as long as everyone agrees on one order. A weaker one again only keeps causes before their effects. Weaker still, each reader only sees each writer's writes in the order that writer made them. The weakest common rule says only that the copies agree in the end, after the writes stop.

A stronger rule is easier for programmers. A weaker rule lets each machine answer at once, also when the network is broken.

## The idea

**Histories.** There are $n$ client processes $p_1, \ldots, p_n$ and a set of read/write registers $x, y, \ldots$ that start at 0. A process issues one operation at a time, and each operation has an invocation time and a response time on a global clock that the processes cannot read. A *history* is the set of completed operations, written $w(x)v$ for a write of $v$ to $x$ and $r(x)v$ for a read of $x$ that returned $v$. Assume that each written value is unique for its register, which is the usual convention that makes the source of each read clear.

A consistency model is a predicate on histories. It is a *safety* property: it restricts which values come back, and it says nothing about whether operations return at all. Whether every operation returns, during partitions and crashes, is a separate *liveness* property ([availability](/cap-theorem/)). The store behind the history is a set of replicas in some system model, typically the asynchronous model with $n$ replicas, crash failures of up to $f$ of them, and channels that may lose or delay messages. The definition of a model does not depend on that system model; the cost of implementing it does.

**Legal serializations.** A *serialization* of a set of operations is a total order of them. It is *legal* if each read in it returns the value of the last write to the same register before it, or 0 if there is none. Program order $\to_{po}$ orders the operations of each process. Real-time order $\to_{rt}$ puts $a$ before $b$ when $a$ responds before $b$ is invoked. The *writes-into* relation $\to_{wi}$ links a write $w(x)v$ to each read $r(x)v$. The *causality order* $\leadsto$ is the transitive closure of $\to_{po} \cup \to_{wi}$, the read/write form of [happened-before](/happened-before/).

The four classic models differ in which operations a serialization must contain and which orders it must respect.

| model | serialized operations | order respected | due to |
| --- | --- | --- | --- |
| linearizable | all operations, one order for everyone | $\to_{po}$ and $\to_{rt}$ | Herlihy and Wing (1990) |
| sequential | all operations, one order for everyone | $\to_{po}$ | Lamport (1979) |
| causal | for each process $p$: the operations of $p$ and all writes | $\leadsto$ | Ahamad et al. (1995) |
| PRAM (FIFO) | for each process $p$: the operations of $p$ and all writes | $\to_{po}$ | Lipton and Sandberg (1988) |

Linearizability and sequential consistency ask for one order that all processes agree on. Causal consistency and PRAM give each process its own view, and two processes may see concurrent writes in different orders.

**The hierarchy.** Each model in the table contains the one above it.

*Linearizable implies sequential*: the same order works, with one constraint less. *Sequential implies causal*: in a legal total order of all operations, a read follows the write it reads from, because written values are unique, so the order respects $\to_{wi}$ and $\to_{po}$, and hence their transitive closure. Removing the reads of other processes keeps it legal, since reads change nothing. *Causal implies PRAM*: $\leadsto$ contains $\to_{po}$, so a view that respects $\leadsto$ respects $\to_{po}$.

Each inclusion is strict, as the separating histories in the examples show. Below PRAM sits eventual consistency, which is not of the same form: it puts no bound on what a read returns at a given time, and only asks that the replicas agree once updates stop. [Strong eventual consistency](/strong-eventual-consistency/) adds a safety part: replicas that have received the same updates are in the same state.

**Other axes.** The [session guarantees](/session-guarantees/) of Terry and others (read your writes, monotonic reads, writes follow reads, monotonic writes) constrain only what one client sees across its own operations. A store can give all four and still let two clients see concurrent writes in different orders. Transactional models such as [serializability](/serializability/) and [snapshot isolation](/snapshot-isolation/) order transactions over many objects; serializability without real time is the multi-object form of sequential consistency, and strict serializability (or [external consistency](/external-consistency/)) is the multi-object form of linearizability. [Quiescent consistency](/quiescent-consistency/) is incomparable with sequential consistency.

**Locality.** Linearizability is *local*: a history is linearizable if and only if its restriction to each object is linearizable (Herlihy and Wing, Theorem 1). Sequential consistency is not local. In the store buffer history below, the restriction to $x$ and the restriction to $y$ are each sequentially consistent, but the whole history is not.

**Costs.** Stronger models need more waiting. With message delays in $[d - u, d]$, any sequentially consistent implementation of two registers has $|W| + |R| \ge d$, where $|W|$ and $|R|$ are the worst-case times of a write and a read (Lipton and Sandberg; Attiya and Welch 1994); see [PACELC](/pacelc/). Under a network partition, no implementation is both linearizable and available, by the [CAP theorem](/cap-theorem/). Mahajan, Alvisi and Dahlin (2011) showed that no model stronger than real-time causal consistency can be implemented by a store that is always available and one-way convergent, so causal consistency is close to the strongest model that an available store can give.

## Examples

**Separating histories.** Each history is in the weaker model and not in the stronger one. Operations of one process are listed left to right in program order; times are given only where real time matters.

| history | lin. | seq. | causal | PRAM |
| --- | --- | --- | --- | --- |
| $p_1$: $w(x)1$ in $[0, 1]$; $p_2$: $r(x)0$ in $[2, 3]$ | no | yes | yes | yes |
| $p_1$: $w(x)1$; $p_2$: $w(x)2$; $p_3$: $r(x)1$, $r(x)2$; $p_4$: $r(x)2$, $r(x)1$ | no | no | yes | yes |
| $p_1$: $w(x)1$, $r(y)0$; $p_2$: $w(y)1$, $r(x)0$ (store buffer) | no | no | yes | yes |
| $p_1$: $w(x)1$; $p_2$: $r(x)1$, $w(y)1$; $p_3$: $r(y)1$, $r(x)0$ | no | no | no | yes |
| $p_1$: $w(x)1$, $w(x)2$; $p_2$: $r(x)2$, $r(x)1$ | no | no | no | no |

*Sequential but not linearizable.* The read starts after the write ends and returns the old value. The order $r(x)0, w(x)1$ is legal and respects program order, but not real time.

*Causal but not sequential.* The writes of $p_1$ and $p_2$ are concurrent, so causal consistency lets $p_3$ and $p_4$ see them in different orders. One global order would have to put $w(x)1$ both before and after $w(x)2$. The store buffer history is the same pattern on two registers: each process reads 0 from the register that the other one wrote, so in any total order the first write would have to come after the read that follows the other write. Multiprocessors with store buffers, such as x86 with its TSO model, allow it.

*PRAM but not causal.* $p_2$ reads $x = 1$ and then writes $y = 1$, so $w(x)1 \leadsto w(y)1$. Process $p_3$ sees the effect $y = 1$ and then the old $x = 0$. PRAM only orders each writer's own writes, and these two writes come from different processes, so the view $w(y)1, r(y)1, r(x)0, w(x)1$ is allowed.

*Not PRAM.* Process $p_2$ sees the two writes of $p_1$ in the reverse order. Only eventual consistency allows this, as long as the final value is 2 everywhere.

**Linearizable histories.** A read that overlaps a write may return the old or the new value. A read that starts after a write ends must return the new value. Two reads in real-time order may not see the new value and then the old one: $p_1$: $w(x)1$ in $[0, 10]$; $p_2$: $r(x)1$ in $[1, 2]$; $p_3$: $r(x)0$ in $[3, 4]$ is sequentially consistent, but not linearizable.

**Eventual consistency.** In a store where a read goes to any replica and replicas exchange writes in the background, the last history above is possible: $p_2$ reads 2 from a replica that has both writes, and then 1 from a replica that has only the first one. Once both writes reach every replica, a [last-writer-wins](/last-writer-wins/) rule makes all replicas return 2.

## Where it is used

- **Multiprocessor memory.** Lamport defined sequential consistency for multiprocessors. Real processors give weaker models, such as TSO on x86, which allows the store buffer history, and languages such as Java and C++ give sequential consistency only to programs without data races.
- **Coordination services and databases.** Systems built on [consensus](/consensus-problem/), such as [Raft](/raft/) or [Paxos](/paxos/) based stores, give linearizable operations through a [replicated state machine](/replicated-state-machine/). Spanner gives [external consistency](/external-consistency/) with [TrueTime](/truetime/).
- **Geo-replicated stores.** COPS and similar systems give causal consistency with convergent conflict handling (causal+), which stays available during partitions.
- **Dynamo-style stores.** [Dynamo-style replication](/dynamo-style-replication/) gives eventual consistency by default, with [quorum](/quorum-replication/) settings and [session guarantees](/session-guarantees/) to make reads stronger.
- **CRDTs.** [CRDTs](/crdt/) give [strong eventual consistency](/strong-eventual-consistency/), and op-based CRDTs on [causal broadcast](/causal-broadcast/) also give causal consistency.
- **Testing.** Checkers such as the ones in the implementation search for a legal serialization. For linearizability the problem is NP-complete in general (Gibbons and Korach 1997), so such checkers are exponential in the worst case and are used on short histories.

## References
