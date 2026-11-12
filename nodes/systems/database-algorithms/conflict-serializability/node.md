---
tag: YBK3Q3
kind: definition
slug: conflict-serializability
name: Conflict serializability
aliases:
- conflict-serializable schedule
area: systems/database-algorithms
level: core
summary: "A schedule is conflict serializable if it orders every pair of conflicting actions the same way as some serial schedule. This holds exactly when its conflict graph is acyclic."
prereqs: [serializability, conflict-graph]
see_also: [view-serializability, two-phase-locking, timestamp-ordering, concurrency-control, topological-sort, linearizability, opacity]
sources:
  - paper: doi:10.1145/360363.360369
    title: K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11), 1976, pages 624 to 633
    locator: the definition of equivalent schedules by the order of dependent actions, and the theorem that a schedule is consistent when its dependency graph is acyclic
  - paper: doi:10.1145/322154.322158
    title: Christos H. Papadimitriou, The serializability of concurrent database updates, Journal of the ACM 26(4), 1979, pages 631 to 653
    locator: the polynomial class of schedules tested by a graph (called DSR there), against the NP-complete general test
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 2 (equivalence of histories, the serialization graph and the Serializability Theorem)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 3 (conflict serializability, the conflict graph test, and the relation to final-state and view serializability)
---

A schedule is *conflict serializable* if it is conflict equivalent to a serial schedule: the same actions, with every pair of conflicting actions in the same order. It is the form of [serializability](/serializability/) that real schedulers enforce, because it has a fast test: Eswaran, Gray, Lorie and Traiger (1976) showed that a schedule is conflict serializable exactly when its [conflict graph](/conflict-graph/) is acyclic. It is stricter than [view serializability](/view-serializability/), which is NP-complete to test.

## Definition

**Schedules and conflicts.** A transaction $T_i$ is a finite sequence of actions $r_i(x)$ and $w_i(x)$ on data items. A schedule $S$ over a set of transactions is a sequence that holds every action of every transaction once and keeps the order inside each transaction. We write $p <_S q$ when action $p$ comes before action $q$ in $S$. A schedule is *serial* when the actions of each transaction are contiguous. Two actions *conflict* if they belong to different transactions, touch the same item, and at least one of them is a write. For a schedule with commits and aborts, all notions here apply to its committed projection $C(S)$, the reads and writes of the committed transactions.

**Conflict equivalence.** Schedules $S$ and $S'$ over the same transactions are *conflict equivalent*, written $S \approx_c S'$, if for every pair of conflicting actions $p, q$:

$$p <_S q \iff p <_{S'} q.$$

**Conflict serializability.** $S$ is conflict serializable if $S \approx_c S'$ for some serial schedule $S'$. The class of such schedules is often called CSR.

**Theorem (Eswaran, Gray, Lorie and Traiger 1976).** Let $G(S)$ be the conflict graph of $S$: one node per transaction, and an edge $T_i \to T_j$ when some action of $T_i$ conflicts with a later action of $T_j$. Then $S$ is conflict serializable if and only if $G(S)$ is acyclic. Moreover, a serial schedule $T_{k_1} \cdots T_{k_m}$ is conflict equivalent to $S$ if and only if $T_{k_1}, \ldots, T_{k_m}$ is a topological order of $G(S)$.

*Proof.* We prove the second statement; the first follows from it, because a directed graph has a topological order exactly when it is acyclic ([topological ordering theorem](/topological-ordering-theorem/)).

Let $S'$ be the serial schedule in the order $\pi = T_{k_1}, \ldots, T_{k_m}$. In $S'$, an action of $T_i$ comes before an action of a different transaction $T_j$ exactly when $T_i$ comes before $T_j$ in $\pi$.

Assume that $S' \approx_c S$, and let $T_i \to T_j$ be an edge of $G(S)$. Then there are conflicting actions $p \in T_i$ and $q \in T_j$ with $p <_S q$. By equivalence $p <_{S'} q$, so $T_i$ comes before $T_j$ in $\pi$. This holds for every edge, so $\pi$ is a topological order.

Assume that $\pi$ is a topological order, and let $p \in T_i$ and $q \in T_j$ conflict. Then $i \ne j$. If $p <_S q$, the edge $T_i \to T_j$ is in $G(S)$, so $T_i$ comes before $T_j$ in $\pi$, so $p <_{S'} q$. If $q <_S p$, the same argument gives $q <_{S'} p$. So the two schedules order every conflicting pair the same way, and $S' \approx_c S$. $\square$

**Theorem (swaps).** $S \approx_c S'$ if and only if $S'$ can be obtained from $S$ by a finite sequence of swaps of two adjacent actions that belong to different transactions and do not conflict.

*Proof.* Such a swap changes the relative order of only the two swapped actions, which do not conflict and are not in the same transaction, so it keeps every conflicting pair and the order inside each transaction. Conversely, let $S \approx_c S'$. Move the first action $a$ of $S'$ to the front of $S$ by adjacent swaps. Each action $b$ that $a$ passes comes before $a$ in $S$ and after $a$ in $S'$. So $b$ is not in the same transaction as $a$ (the order inside a transaction is the same in both), and $b$ does not conflict with $a$ (by equivalence). So each swap is allowed. Then the first actions agree, and we repeat on the rest by induction on the length. $\square$

**Testing.** Build $G(S)$ and look for a cycle with a [depth-first search](/dfs-cycle-detection/) or [Kahn's topological sort](/topological-sort/). For $n$ actions and $m$ transactions this takes $O(n^2)$ time with a plain scan of all pairs, and $O(n + m)$ expected time with the reduced graph described on the conflict graph page.

## Examples and non-examples

The examples use $r_1(x)$ for a read of $x$ by $T_1$. All transactions commit.

**Conflict serializable.** In

$$S_1 = r_1(x)\ w_1(x)\ r_2(x)\ r_1(y)\ w_2(x)\ w_1(y)$$

the conflicting pairs are $w_1(x) < r_2(x)$, $r_1(x) < w_2(x)$ and $w_1(x) < w_2(x)$. All of them give the edge $T_1 \to T_2$. Swap $r_2(x)$ with $r_1(y)$, then $w_2(x)$ with $w_1(y)$, then $r_2(x)$ with $w_1(y)$, and you get the serial schedule $T_1 T_2$. The actions $r_1(y)$ and $w_1(y)$ touch an item that $T_2$ never uses, so they move freely.

**More than one serial order.** In $S_2 = r_1(x)\ r_2(y)\ r_3(z)\ w_1(y)$ the only conflict is $r_2(y) < w_1(y)$, so the only edge is $T_2 \to T_1$. The topological orders are $T_2 T_1 T_3$, $T_2 T_3 T_1$ and $T_3 T_2 T_1$, and a test over all six serial orders finds exactly these three.

**Non-example: the lost update.** In

$$S_3 = r_1(x)\ r_2(x)\ w_1(x)\ w_2(x)$$

the pair $r_1(x) < w_2(x)$ gives $T_1 \to T_2$, and the pair $r_2(x) < w_1(x)$ gives $T_2 \to T_1$. The graph has a cycle, so $S_3$ is not conflict serializable. If both transactions add 1 to $x$, the final value is the old value plus 1, not plus 2: the update of $T_1$ is lost.

**Non-example that is still serializable.** In

$$S_4 = r_1(x)\ w_2(x)\ w_1(x)\ w_3(x)$$

the pairs $r_1(x) < w_2(x)$ and $w_2(x) < w_1(x)$ give a cycle $T_1 \to T_2 \to T_1$. But $S_4$ is view equivalent to $T_1 T_2 T_3$: in both, $T_1$ reads the initial $x$ and $T_3$ writes the final $x$. The writes $w_2(x)$ and $w_1(x)$ are *blind* (not preceded by a read of $x$ in the same transaction) and both are overwritten by $T_3$, so their order does not matter. This is the standard example that [view serializability](/view-serializability/) is strictly larger.

## Related definitions

- **[Serializability](/serializability/)** is the general notion: equivalence to some serial schedule. Conflict serializability fixes the equivalence to "same order of conflicting actions". Every conflict serializable schedule is view serializable, because the order of conflicting actions fixes which write each read sees and which write is last on each item; the converse fails, as $S_4$ shows.
- **[View serializability](/view-serializability/)** uses the reads-from relation and the final writes. Its test is NP-complete (Papadimitriou 1979), which is why schedulers aim at conflict serializability. If a schedule has no blind writes, the two notions coincide.
- **[Conflict graph](/conflict-graph/)** is the test object. Its acyclicity is the characterization above.
- **Prefix closure.** Every prefix of a conflict serializable schedule is conflict serializable, because the conflict graph of a prefix is a subgraph of the full graph. Online schedulers need this property: they must accept or reject an action before the rest of the schedule exists.
- **Order-preserving and commit-order-preserving conflict serializability** add the demand that the serial order agrees with the real-time order of transactions that do not overlap, or with the commit order. [Strict two-phase locking](/strict-two-phase-locking/) in its rigorous form gives commit order (Weikum and Vossen, Chapter 3).
- **Recoverability, avoiding cascading aborts and strictness** are separate conditions about commits and aborts; they are defined on the [serializability](/serializability/) page. A conflict serializable schedule can still be unrecoverable.
- **Schedulers.** [Two-phase locking](/two-phase-locking/) and basic [timestamp ordering](/timestamp-ordering/) produce only conflict serializable schedules. Each proof shows that every edge of the conflict graph agrees with one fixed order (lock points, timestamps). The [Thomas write rule](/thomas-write-rule/) leaves this class and gives schedules that are only view serializable.
- **Close notions elsewhere.** [Linearizability](/linearizability/) is a condition on single operations of concurrent objects with real-time order; conflict serializability is about multi-item transactions and ignores real time. Strict serializability asks for both. [Opacity](/opacity/) in transactional memory also constrains what aborted and running transactions read, which serializability of committed transactions does not.

## References
