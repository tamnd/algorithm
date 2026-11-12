---
tag: R82KKG
kind: concept
slug: conflict-graph
name: Conflict graph
aliases:
- precedence graph
- serialization graph
area: systems/database-algorithms
level: core
summary: "A directed graph on the transactions of a schedule, with an edge Ti -> Tj when an action of Ti conflicts with a later action of Tj. It is acyclic exactly when the schedule is conflict serializable."
prereqs: [serializability, topological-sort, dfs-cycle-detection]
see_also: [conflict-serializability, view-serializability, two-phase-locking, timestamp-ordering, concurrency-control, wait-for-graph, topological-ordering-theorem, isolation-levels]
sources:
  - paper: doi:10.1145/360363.360369
    title: K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11), 1976, pages 624 to 633
    locator: the dependency graph of a schedule and the theorem that a schedule is consistent (equivalent to a serial one) when its dependency graph has no cycle
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 2 (the serialization graph of a history and the Serializability Theorem) and Chapter 4 (serialization graph testing schedulers)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 3 (conflict graphs and the test for conflict serializability)
  - paper: doi:10.1109/ICDE.2000.839388
    title: Atul Adya, Barbara Liskov and Patrick O'Neil, Generalized isolation level definitions, Proceedings of the 16th International Conference on Data Engineering (ICDE), 2000, pages 67 to 78
    locator: the direct serialization graph with write-write, write-read and read-write edges
---

The conflict graph of a [schedule](/serializability/) is a directed graph with one node for each committed transaction and an edge $T_i \to T_j$ when some action of $T_i$ conflicts with a later action of $T_j$. Eswaran, Gray, Lorie and Traiger (1976) showed that a schedule is equivalent to a serial schedule, in the sense of [conflict serializability](/conflict-serializability/), exactly when this graph has no cycle. A [topological order](/topological-sort/) of the graph then gives the equivalent serial order. Bernstein, Hadzilacos and Goodman call it the serialization graph; many textbooks call it the precedence graph.

## In plain words

Several programs change shared data at the same time, and the database mixes their steps. Two steps clash when they come from different programs, touch the same record, and at least one of them changes it. The order of two clashing steps matters: if you swap them, a program can see a different value or the record can end with a different value.

Draw one dot for each program. Each time a step of program A clashes with a later step of program B, draw an arrow from A to B. The arrow says "A must come before B". If the arrows never go round in a loop, you can line the programs up so that every arrow points forward, and running them one at a time in that line gives the same result. If there is a loop, no such line exists.

## The idea

**Model.** A transaction $T_i$ is a sequence of actions $r_i(x)$ (read item $x$) and $w_i(x)$ (write item $x$), followed by a commit $c_i$ or an abort $a_i$. A schedule $S$ is an interleaving of the actions of some transactions that keeps the order inside each transaction. Two actions *conflict* if they belong to different transactions, touch the same item, and at least one of them is a write. So there are three kinds of conflict on an item $x$: $r_i(x)$ before $w_j(x)$, $w_i(x)$ before $r_j(x)$, and $w_i(x)$ before $w_j(x)$. Two reads never conflict.

**Definition.** Let $C(S)$ be the committed projection of $S$: the reads and writes of the transactions that commit in $S$. The conflict graph $G(S) = (V, E)$ has

$$V = \{T_i : T_i \text{ commits in } S\}, \qquad E = \{(T_i, T_j) : i \ne j,\ \exists\, p \in T_i,\ q \in T_j,\ p <_S q,\ p \text{ and } q \text{ conflict}\}.$$

One edge stands for all conflicts in the same direction between the same two transactions, so the graph has at most $m(m-1)$ edges for $m$ transactions. Edges in both directions between $T_i$ and $T_j$ already form a cycle of length 2.

**The theorem.** A schedule $S$ is conflict serializable if and only if $G(S)$ is acyclic. If $G(S)$ is acyclic, every topological order $T_{k_1}, \ldots, T_{k_m}$ of $G(S)$ gives a serial schedule that is conflict equivalent to $C(S)$, and these are the only conflict equivalent serial orders. The proof is on the [conflict serializability](/conflict-serializability/) page. Its core is short. In a serial schedule every conflict goes from an earlier transaction to a later one, so a conflict equivalent serial order must put $T_i$ before $T_j$ for each edge, which is a topological order. Conversely, in the serial schedule of a topological order, each conflicting pair keeps the order that it has in $S$, because its edge points forward. A directed graph has a topological order exactly when it is acyclic, by the [topological ordering theorem](/topological-ordering-theorem/).

**How to build it.** Scan the schedule once and keep, for each item, the list of earlier actions on it.

```pseudo id=build
CONFLICT-GRAPH(S)                          ▷ S is a committed projection
L1  V ← the transactions of S, E ← ∅
L2  for each item x do seen[x] ← empty list
L3  for each action p of S, in order do
L4      for each action q in seen[item(p)] do
L5          if txn(q) ≠ txn(p) and (q or p is a write) then E ← E ∪ {(txn(q), txn(p))}
L6      append p to seen[item(p)]
L7  return (V, E)
```

For a schedule of $n$ actions this takes $O(n^2)$ time in the worst case, when all actions touch one item. To test acyclicity a smaller graph is enough. For each item, keep only the last writer and the readers since that write. A read gets one edge from the last writer. A write gets edges from the last writer and from each reader since the last write, and then clears the reader list. Each action adds at most two edges plus the edges of the reads it clears, and each read is cleared once, so the graph has $O(n)$ edges and is built in $O(n)$ expected time with hash maps. It has the same reachability as $G(S)$: an omitted edge from an earlier write $w$ to a later action $p$ is replaced by the path through the chain of writes on the same item between them, and an omitted edge from a read $r$ to a later write $p$ is replaced by the edge from $r$ to the first write after $r$, followed by that chain. Edges inside one transaction disappear because they join a node to itself. Same reachability means the same cycles through distinct nodes, so the test gives the same answer. Then a [depth-first search with three colors](/dfs-cycle-detection/) finds a cycle, or a topological order, in $O(m + |E|)$ time.

**Incremental use.** A scheduler can keep the graph while transactions run. Bernstein, Hadzilacos and Goodman call this serialization graph testing: when an action arrives, add its edges, and reject the action (abort its transaction) if an edge closes a cycle. The node of a committed transaction cannot be deleted at once, because a later action of a running transaction can still add an edge into a cycle through it. Their rule is to delete a committed node only when it has no incoming edges. (We give this rule from BHG Chapter 4; check the exact form there.)

**How it differs from close graphs.** The [wait-for graph](/wait-for-graph/) has an edge from a blocked transaction to the transaction whose lock it waits for, at this moment. A cycle there is a [deadlock](/deadlock/), and the graph changes as locks are released. The conflict graph records the order of conflicts that already happened. A cycle there means the schedule is not conflict serializable, and the cycle never goes away. Under [two-phase locking](/two-phase-locking/) a transaction that would close a conflict cycle has to wait, so the danger shows up in the wait-for graph instead. In transactional memory, a [transaction conflict](/transaction-conflict/) is the same relation on memory words, but STM systems detect it with read and write sets and version numbers, not with an explicit graph, and they also need [opacity](/opacity/) for transactions that abort.

## Examples

The examples use the notation $r_1(x)$ for a read of $x$ by $T_1$ and $w_2(z)$ for a write of $z$ by $T_2$. All transactions commit.

**An acyclic graph.** Take

$$S_1 = r_1(x)\ r_2(y)\ w_1(x)\ r_3(x)\ w_3(z)\ w_2(z).$$

| pair | conflict? | edge |
|---|---|---|
| $r_1(x)$, $w_1(x)$ | no, same transaction | |
| $w_1(x)$, $r_3(x)$ | yes, write then read | $T_1 \to T_3$ |
| $r_1(x)$, $r_3(x)$ | no, two reads | |
| $w_3(z)$, $w_2(z)$ | yes, write then write | $T_3 \to T_2$ |
| $r_2(y)$ and any other | no, no other action on $y$ | |

The graph has the edges $T_1 \to T_3 \to T_2$ and no cycle. Its only topological order is $T_1, T_3, T_2$, so $S_1$ is conflict equivalent to the serial schedule $r_1(x)\, w_1(x)\, r_3(x)\, w_3(z)\, r_2(y)\, w_2(z)$. The order differs from the order of the first actions ($T_1$, $T_2$, $T_3$): $T_2$ starts second but must be last.

**A cycle.** Take

$$S_2 = r_1(x)\ r_2(y)\ w_1(y)\ w_2(x).$$

The pair $r_2(y)$, $w_1(y)$ gives $T_2 \to T_1$, and the pair $r_1(x)$, $w_2(x)$ gives $T_1 \to T_2$. The cycle $T_1 \to T_2 \to T_1$ says that $S_2$ is not conflict serializable. In fact $S_2$ is not serializable in any sense: in $S_2$ each transaction reads the initial value of the item that the other one writes, while in each serial order the second transaction reads the value of the first.

**A serial schedule.** In $r_1(x)\, w_1(x)\, r_2(x)\, w_2(y)\, r_3(y)$ every edge goes from a transaction to a later one: $T_1 \to T_2$ and $T_2 \to T_3$. The graph of a serial schedule never has a cycle.

**An aborted transaction.** In $w_1(x)\, r_2(x)\, a_1\, c_2$ the conflict graph is built on the committed projection $r_2(x)$, so it has the node $T_2$ and no edge. The read of a value written by an aborted transaction is a problem of [recoverability](/serializability/), not of the order of committed transactions.

## Where it is used

- **Proofs of schedulers.** The standard proof that [two-phase locking](/two-phase-locking/), [timestamp ordering](/timestamp-ordering/) and serialization graph testing are correct shows that each edge of the conflict graph agrees with some fixed order (lock points, timestamps), so no cycle can form.
- **Serialization graph testing schedulers.** They keep the graph online and abort a transaction when its action would close a cycle (Bernstein, Hadzilacos and Goodman, Chapter 4).
- **Optimistic and multiversion systems.** Validation in [optimistic concurrency control](/optimistic-concurrency-control/) and the checks of [serializable snapshot isolation](/serializable-snapshot-isolation/) look for parts of cycles in a graph of this kind, with read-write edges between concurrent transactions.
- **Isolation levels and testing tools.** Adya, Liskov and O'Neil define the [isolation levels](/isolation-levels/) by the cycles that a direct serialization graph, with separate write-write, write-read and read-write edges, may or may not have. Tools that check the histories of real databases build such a graph and search it for cycles.
- **Teaching and debugging.** Drawing the graph of a short schedule is the fastest way to see whether it is conflict serializable and in which order the transactions take effect.

## References
