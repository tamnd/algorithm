---
tag: YM4CC5
kind: theorem
slug: serializability-theorem
name: Serializability theorem
aliases:
- precedence graph test for conflict serializability
area: databases/transactions-and-concurrency
level: core
summary: A schedule is conflict serializable exactly when its conflict graph is acyclic, and a topological order gives an equivalent serial order.
prereqs: [conflict-serializability, conflict-graph, topological-ordering-theorem]
see_also: [conflict-graph, conflict-serializability, view-serializability-np-completeness, two-phase-locking-theorem, transaction-schedule, topological-sort, timestamp-ordering, commitment-ordering]
sources:
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 2 (the serialization graph of a history over its committed transactions, and the Serializability Theorem)
  - paper: doi:10.1145/360363.360369
    title: K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11), 1976, pages 624 to 633
    locator: the dependency graph of a schedule and the theorem that a schedule is equivalent to a serial one when the graph has no cycle
  - paper: doi:10.1145/322154.322158
    title: Christos H. Papadimitriou, The serializability of concurrent database updates, Journal of the ACM 26(4), 1979, pages 631 to 653
    locator: the comparison of the conflict based test with other notions of serializability
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 3 (conflict serializability and the conflict graph test)
---

The serializability theorem says that the committed work of a [schedule](/transaction-schedule/) can be reordered into a serial schedule, by moves that keep every conflict, exactly when its *serialization graph* has no cycle. The serial orders that work are then exactly the topological orders of the graph. Eswaran, Gray, Lorie and Traiger stated it in 1976; Bernstein, Hadzilacos and Goodman gave it its name in their 1987 book, in the form with commits and aborts that is used here. It turns [conflict serializability](/conflict-serializability/) into a graph question that takes polynomial time, while the more permissive [view serializability](/view-serializability/) is NP-complete to test.

## Statement

Let $S$ be a schedule over $T_1, \ldots, T_n$ with read, write, commit and abort actions, and let $C(S)$ be its committed projection: the actions of the transactions that have committed in $S$. Two actions *conflict* if they belong to different transactions, touch the same item, and at least one is a write.

The *serialization graph* $SG(S)$ has one node for each committed transaction, and an arc $T_i \to T_j$ ($i \ne j$) if some action of $T_i$ in $C(S)$ conflicts with a later action of $T_j$ in $C(S)$. (This is the [conflict graph](/conflict-graph/) of $C(S)$.)

**Theorem (serializability theorem).** For every schedule $S$:

1. $C(S)$ is conflict equivalent to a serial schedule if and only if $SG(S)$ is acyclic.
2. A serial schedule $T_{k_1} \cdots T_{k_m}$ of the committed transactions is conflict equivalent to $C(S)$ if and only if $T_{k_1}, \ldots, T_{k_m}$ is a topological order of $SG(S)$.
3. $SG(S)$ can be built, and tested for a cycle, in time $O(N^2)$ for a schedule of $N$ actions.

## In plain words

Draw an arrow from one transaction to another whenever the first touched an item before the second, and one of the two touches was a write. Such a pair can never be swapped without changing what some transaction reads or what the database holds at the end, so any serial order that works has to follow every arrow. If the arrows go round in a circle, no order can follow them all. If they do not, sort the transactions so that every arrow points forward, and that order works.

## Proof

Write $G = SG(S)$ and $H = C(S)$. Part 2 implies part 1, because a directed graph has a topological order if and only if it is acyclic (the [topological ordering theorem](/topological-ordering-theorem/)). The [conflict serializability](/conflict-serializability/) page proves part 2 by comparing conflicting pairs directly. Here is a second proof that builds the serial schedule by swaps, in the same way as [Kahn's algorithm](/topological-sort/) builds a topological order. It uses the swap lemma from that page: two schedules are conflict equivalent if and only if one can be turned into the other by swapping adjacent actions of different transactions that do not conflict.

*Every equivalent serial order is a topological order.* Let $H'$ be serial in the order $\pi$ and conflict equivalent to $H$. For an arc $T_i \to T_j$ of $G$ there are conflicting $p \in T_i$ and $q \in T_j$ with $p <_H q$, so $p <_{H'} q$, so $T_i$ comes before $T_j$ in $\pi$.

*Every topological order gives an equivalent serial schedule.* We show by induction on the number $m$ of committed transactions: if $\pi = T_{k_1}, \ldots, T_{k_m}$ is a topological order of $G$, then $H$ can be turned into the serial schedule in the order $\pi$ by allowed swaps. For $m \le 1$, $H$ is already serial.

Let $m \ge 2$ and $T = T_{k_1}$. Since $\pi$ is a topological order, $T$ has no incoming arc. Take the actions of $T$ from first to last, and move each one to the left by adjacent swaps until it stands right after the actions of $T$ that are already at the front. An action $b$ that the action $a$ of $T$ passes in this way comes before $a$ in $H$ and is not an action of $T$. If $b$ conflicted with $a$, $G$ would have the arc from the transaction of $b$ to $T$, which does not exist. So each swap is allowed. The result is $H_1 = T \cdot H^-$, where $H^-$ is $H$ without the actions of $T$, in their old order.

The conflict graph of $H^-$ is $G$ without the node $T$, because removing actions does not change the order of the others. So $T_{k_2}, \ldots, T_{k_m}$ is a topological order of it, and by induction $H^-$ can be turned into the serial schedule $T_{k_2} \cdots T_{k_m}$ by allowed swaps. The same swaps work in $H_1$ behind the block of $T$. By the swap lemma the final serial schedule is conflict equivalent to $H$.

*Part 3.* $H$ has at most $N$ actions. Compare every pair of positions, which takes $O(N^2)$ time and gives at most $n^2$ arcs; then a [depth-first search](/dfs-cycle-detection/) finds a cycle or a topological order in time linear in the size of the graph. $\square$

**Worked example.** $S = r_1(x)\ r_2(y)\ w_3(x)\ w_1(y)\ c_1\ c_2\ c_3$. The conflicts are $r_1(x) <_S w_3(x)$, which gives $T_1 \to T_3$, and $r_2(y) <_S w_1(y)$, which gives $T_2 \to T_1$. The graph is the path $T_2 \to T_1 \to T_3$, with the single topological order $T_2, T_1, T_3$. The proof first moves $r_2(y)$ to the front, past $r_1(x)$, and then $c_2$ right behind it, past $r_1(x)$, $w_3(x)$, $w_1(y)$ and $c_1$; a commit conflicts with nothing. Then $T_1$ comes next: $r_1(x)$ is already in place, and $w_1(y)$ and $c_1$ move past $w_3(x)$, which touches another item. The result is $r_2(y)\ c_2\ r_1(x)\ w_1(y)\ c_1\ w_3(x)\ c_3$, and no other serial order is conflict equivalent to $S$.

## Consequences

- **Testing is easy.** Conflict serializability can be decided in polynomial time. Practical schedulers do not build the graph for every schedule; they use protocols whose output is acyclic by design.
- **The protocol theorems.** The [two-phase locking theorem](/two-phase-locking-theorem/) is proved by showing that every arc of $SG(S)$ points from the earlier to the later lock point. [Timestamp ordering](/timestamp-ordering/) makes every arc point from the smaller to the larger timestamp, and [commitment ordering](/commitment-ordering/) from the earlier to the later commit. Each then gets acyclicity for free.
- **Prefix closure.** If $S'$ is a prefix of $S$, then every transaction committed in $S'$ is committed in $S$, and every conflict of $C(S')$ is a conflict of $C(S)$. So $SG(S')$ is a subgraph of $SG(S)$, and conflict serializability of the committed projection is prefix closed.
- **A scheduler must also watch active transactions.** In $S = r_1(x)\ w_2(x)\ c_2\ w_1(x)$, the graph $SG(S)$ has the single node $T_2$. But if $T_1$ commits, the arcs $T_1 \to T_2$ and $T_2 \to T_1$ appear. A serialization graph testing scheduler therefore keeps the graph over all transactions that have not aborted, and refuses or aborts an action that would close a cycle.
- **Aborts remove arcs.** $r_1(x)\ w_2(x)\ w_1(x)\ c_1\ a_2$ has a cycle between $T_1$ and $T_2$ among all actions, but $T_2$ aborted, and $SG(S)$ is the single node $T_1$. The theorem says nothing about whether that abort was safe; that is the job of the [recovery classes](/recoverable-schedule/).

## Tightness

- **Only conflict equivalence.** Acyclicity is necessary for conflict serializability, not for serializability in general. $r_1(x)\ w_2(x)\ w_1(x)\ w_3(x)\ c_1\ c_2\ c_3$ has the cycle $T_1 \to T_2 \to T_1$, but it is [view equivalent](/view-serializability/) to $T_1 T_2 T_3$: the blind write $w_3(x)$ hides the order of the other two writes. For view serializability the graph is replaced by a polygraph with choice arcs, and the test becomes [NP-complete](/view-serializability-np-completeness/).
- **Only the read-write model.** The theorem treats every pair of accesses with a write as a conflict. With operations that commute, such as increments, a cycle in the read-write graph can still allow a serial order. Semantic concurrency control uses a smaller conflict relation, and the theorem holds for that relation with the same proof.
- **The bound in part 3 is for the plain method.** The number of conflicting pairs can be quadratic in $N$, but it is enough to keep, for each item, the last writer and the readers since that write; this gives $O(N)$ arcs and a test in time linear in $N$ up to hashing.

## History

Eswaran, Gray, Lorie and Traiger (1976) modeled a schedule as a sequence of actions, defined its dependency graph, and proved that a schedule is consistent (equivalent to a serial one) when the graph has no cycle; their paper used this to prove that two-phase transactions are safe. Papadimitriou (1979) compared this notion with broader ones and showed that they are harder to test. Bernstein, Hadzilacos and Goodman (1987) put the theorem in its present form over committed projections and called it the Serializability Theorem.

## References
