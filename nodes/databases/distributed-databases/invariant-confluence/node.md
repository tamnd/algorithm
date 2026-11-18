---
tag: 17HSK7
kind: theorem
slug: invariant-confluence
name: Invariant confluence
aliases:
- I-confluence
- coordination avoidance theorem
area: databases/distributed-databases
level: research
summary: "Transactions can keep an invariant with no coordination, staying available and convergent, exactly when merging two states reachable from a common valid state keeps it."
prereqs: [highly-available-transactions, eventual-consistency]
see_also: [ramp-transactions, calm-theorem, crdt, state-based-crdt, serializability, confluence, cap-theorem, two-phase-locking]
sources:
  - paper: doi:10.14778/2735508.2735509
    title: "Peter Bailis, Alan Fekete, Michael J. Franklin, Ali Ghodsi, Joseph M. Hellerstein and Ion Stoica, Coordination avoidance in database systems, Proceedings of the VLDB Endowment 8(3), 2014, pages 185 to 196"
    locator: "Section 3 (the system model, Definitions 1 to 5), Section 4 (Definition 6 and Theorem 1, with a proof sketch; the full proof is in the extended technical report, Appendix B), Section 5 and Table 2 (invariants and operations), Section 6 and Table 3 (TPC-C)"
  - paper: doi:10.14778/2732232.2732237
    title: "Peter Bailis, Aaron Davidson, Alan Fekete, Ali Ghodsi, Joseph M. Hellerstein and Ion Stoica, Highly available transactions, virtues and limitations, Proceedings of the VLDB Endowment 7(3), 2013, pages 181 to 192"
    locator: Section 4 (the transactional availability that the theorem uses)
---

Invariant confluence (I-confluence) is the test of Bailis, Fekete, Franklin, Ghodsi, Hellerstein and Stoica (2014) for when a set of transactions can preserve an application invariant with no coordination between servers. The theorem says that this is possible exactly when any two valid states that the transactions can reach from a common valid state merge into a valid state. So the need for coordination is a property of the invariant and the transactions, not of the concurrency control.

## Statement

**Model** (Section 3 of the paper). A database state is a set of versions of data items, and $\mathcal{D}$ is the set of states. The initial state $D_0$ is given. Two states are combined by a merge $\sqcup$, which is set union, so it is commutative, associative and idempotent. A transaction $t$ is a function $t : \mathcal{D} \to \mathcal{D}$ that adds versions to the *replica* it runs on: the versions that it can see at the servers it contacts. An invariant is a predicate $I$ on states, with $I(D_0)$ true. A state $D$ is *$I$-valid* if $I(D)$ is true.

A system is:

- *globally $I$-valid* if every replica always holds an $I$-valid state;
- *transactionally available* if a transaction that can reach servers holding each item it uses eventually commits or aborts, and it aborts only by its own choice or because committing would make its own replica state invalid;
- *convergent* if, when writes stop and messages between two servers are no longer delayed, the servers come to hold the same versions of the items they both store;
- *coordination-free* for a set $T$ of transactions if the progress of each $t \in T$ depends only on its own replica state.

A state $S$ is *$I$-$T$-reachable* if some partially ordered sequence of transactions from $T$ and merges, starting at $D_0$, yields $S$, and every intermediate state is $I$-valid. The earlier states in such a sequence are the *ancestors* of $S$.

**Definition 6 (I-confluence).** A set $T$ of transactions is *$I$-confluent* if, for all $I$-$T$-reachable states $D_i$ and $D_j$ that have a common ancestor, $I(D_i \sqcup D_j)$ is true.

**Theorem 1.** A globally $I$-valid system can execute a set $T$ of transactions with coordination freedom, transactional availability and convergence if and only if $T$ is $I$-confluent with respect to $I$.

The theorem holds in the asynchronous model, in which a network partition can last forever. The "only if" direction needs a partition that does not heal before the transactions must answer.

## In plain words

Let each server run transactions on its own copy and merge copies later. Each server checks the invariant on its own copy before it commits, so each copy stays valid. The only danger is the merge: two copies that are each valid may join into a copy that is not. A bank balance that must not go below zero shows this. Two servers each see 100, each allow a withdrawal of 100, and the merged balance is -100.

The theorem says that this danger is the whole story. If every merge of reachable valid states is valid, servers never need to talk before they commit. If some merge is not valid, then any system that never waits for another server will reach that merge in some run, so the system must coordinate, give up availability, or never converge.

## Proof

The paper gives a sketch and puts the full proof in its technical report. The proof below follows the sketch.

**If ($\Leftarrow$).** Suppose $T$ is $I$-confluent. Build this system. Each server $s$ holds a state $S_s$, at first $D_0$. A transaction at $s$ runs on $S_s$ and computes $S' = t(S_s)$. If $I(S')$ is true, it commits and $S_s := S'$; if not, it aborts. Servers send their states to each other whenever the network lets them, and a server that receives a state $S$ sets $S_s := S_s \sqcup S$.

We show by induction on the steps of a run that every $S_s$ is $D_0$ or $I$-$T$-reachable. At the start every $S_s$ is $D_0$. A commit replaces $S_s$ by $t(S_s)$, which is $I$-valid by the check, and the sequence that reached $S_s$ followed by $t$ reaches $t(S_s)$ with only valid states, so $t(S_s)$ is reachable. A merge combines $S_s$ with a state $S$ that some server held earlier. Both are $D_0$ or reachable, and both descend from $D_0$, which is a common ancestor. If one of them is $D_0$, the merge is the other state, since every reachable state contains $D_0$ (transactions and merges only add versions). If both are reachable, $I$-confluence gives that $S_s \sqcup S$ is $I$-valid, and it is reachable by the two sequences followed by the merge. So every replica is always valid, and the system is globally $I$-valid.

A transaction looks only at $S_s$, so the system is coordination-free. It never waits, and it aborts only when committing would make its replica invalid, so it is transactionally available. When writes stop and messages flow, every server receives every other state, and since union is commutative, associative and idempotent, all servers end with the union of all states. So the system is convergent. $\square$

**Only if ($\Rightarrow$).** Suppose $T$ is not $I$-confluent. Then there are reachable states $D_i$ and $D_j$ with a common ancestor $D_s$ such that $I(D_i \sqcup D_j)$ is false. Suppose, for a contradiction, that a system has all four properties.

Take two servers $p$ and $q$. First run, with no partition, the transactions and merges that reach $D_s$, and let the servers converge, so that both hold $D_s$. Each of these transactions keeps its replica valid, so transactional availability makes it commit. Now cut the network between $p$ and $q$ and never repair it while the next transactions run. At $p$, run the transactions that lead from $D_s$ to $D_i$, and at $q$ the ones that lead from $D_s$ to $D_j$. (If those sequences contain merges, use more servers on each side of the cut and let them merge with each other; the argument is the same.)

Look at a transaction $t$ at $p$. Its replica state is the state on $p$, and by coordination freedom its progress depends only on that state, so it acts as in a run where $q$ does nothing. Committing it keeps the replica valid, since every state on the way to $D_i$ is valid. By transactional availability it must commit, and it must do so in finite time, while the cut is still there. So $p$ reaches $D_i$, and in the same way $q$ reaches $D_j$. Now repair the network and stop all writes. By convergence $p$ and $q$ come to hold the same versions, which is $D_i \sqcup D_j$, since merge is union and no new writes occur. This state is not $I$-valid, so the system is not globally $I$-valid. This is a contradiction. $\square$

**The counterexample from the plain words, in the model.** Let a counter be the set of its increment and decrement versions, and let $I$ say that the sum is at least 0. Let $T$ hold a "deposit 1" and a "withdraw 1" that reads the sum and writes $-1$ only if the result stays valid. From $D_0 = \{\}$ the deposit reaches $D_s = \{+1\}$. A withdrawal at $p$ gives $D_i = \{+1, -1_a\}$, with sum 0, and a withdrawal at $q$ gives $D_j = \{+1, -1_b\}$, also with sum 0. Both are reachable and have the common ancestor $D_s$, but $D_i \sqcup D_j = \{+1, -1_a, -1_b\}$ has sum $-1$. So these transactions are not $I$-confluent, and a lower bound on a balance that can be decreased needs coordination. With increments only, every reachable state has a sum at least 0 and so does every union, so increments are $I$-confluent.

## Consequences

**A table of common cases.** Section 5 and Table 2 of the paper classify common SQL invariants and operations, with proofs in the technical report. These are theorems in the model above.

| Invariant | Operation | I-confluent |
|---|---|---|
| attribute equals or does not equal a value | any | yes |
| uniqueness | insert a value chosen by the user | no |
| uniqueness | insert some unique value chosen by the system | yes |
| AUTO_INCREMENT (sequential ids) | insert | no |
| foreign key | insert | yes |
| foreign key | delete | no |
| foreign key | cascading delete | yes |
| secondary index, materialized view | update | yes |
| counter greater than a bound | increment | yes |
| counter greater than a bound | decrement | no |
| counter less than a bound | decrement | yes |
| counter less than a bound | increment | no |
| set, list or map contains or does not contain an element | any | yes |
| size of a set, list or map equals a value | mutation | no |

The uniqueness rows show how much the operation matters. Two servers that insert users "Stan" and "Mary" both with id 5 each keep the ids unique, but the merge does not. If the system picks the id, each server can take ids from its own part of the id space, and every merge stays unique.

**TPC-C.** Section 6 and Table 3 apply the table to the 12 consistency conditions of TPC-C. Ten are $I$-confluent: the materialized views and the foreign keys. Two are not: order ids per district must be sequential, which New-Order assigns, and orders must be delivered in sequence, which Delivery does. So only those parts need coordination. The authors used [RAMP transactions](/ramp-transactions/) for the foreign keys and the views.

**Measurement.** This is a measurement from the paper's prototype, on Amazon EC2 cr1.8xlarge servers in the us-west-2 region with one TPC-C warehouse per server, published in 2014. The coordination-avoiding plan for New-Order scaled linearly to over 12.7 million transactions per second on 200 servers. With all transactions distributed, its throughput dropped by 29 percent from the case with none, while distributed [two-phase locking](/two-phase-locking/) dropped by over 90 percent. The paper notes that it knew of no other compliant multi-server TPC-C run above 500,000 New-Order transactions per second, and calls its result a 25-fold improvement.

**Relation to other conditions.** If transactions commute, their effects can be merged in any order, but $I$-confluence can hold without commutativity, and it can fail for commuting operations: the two withdrawals above commute, and the invariant still breaks. The [CALM theorem](/calm-theorem/) gives a related answer for programs: monotone programs need no coordination. [CRDTs](/crdt/) give merge functions for counters, sets and maps; the theorem then asks which invariants survive their merges.

## Tightness

- **Convergence is needed.** Without it, servers can keep their states apart forever. Each server stays valid and never needs coordination, whatever the invariant.
- **Availability is needed.** A system that may block can use locks or [two-phase commit](/two-phase-commit/) and keep any invariant, as [serializability](/serializability/) does.
- **The partition must be able to last.** The "only if" proof needs the cut to stay until the transactions have committed. If every message arrives within a known time, a server can coordinate with the others before it commits and still answer in bounded time. Then coordination costs latency but not availability, and the theorem no longer marks a hard limit.
- **The common ancestor matters.** Without it the definition would ask about merges of valid states that no run produces. Two states that each have unique ids but share some ids would fail even when no transaction assigns ids (footnote 4 of the paper).
- **The invariant must be complete.** The theorem protects only the invariants that are stated. If the application has a rule that is not stated, an $I$-confluent execution can break it.
- **Existence only.** The theorem says that a coordination-free implementation exists. It says nothing about its cost, and locking implementations of $I$-confluent transactions still coordinate.
- **Deciding the property.** For arbitrary programs, $I$-confluence is undecidable, as the paper notes. The table above covers common invariants that are checked by hand.

## History

The term comes from confluence in term rewriting and from observable confluence for constraint handling rules (Duck, Stuckey and Sulzmann, ICLP 2007), where it guarantees that any order of rule applications keeps an invariant. Bailis and his coauthors moved it to transactions on replicated data in "Coordination avoidance in database systems", published in PVLDB in 2014 and presented at VLDB 2015. It builds on their work on [highly available transactions](/highly-available-transactions/) (2013), which showed which isolation levels need coordination, and on [RAMP transactions](/ramp-transactions/) (2014).

## References
