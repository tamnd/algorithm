---
tag: RGG5F9
kind: algorithm
slug: schism-partitioning
name: Schism workload-driven partitioning
aliases:
- Schism
area: databases/distributed-databases
level: research
summary: "Partition and replicate tuples by a balanced min cut of a graph that joins tuples used by one transaction, then explain the cut as range predicates. A heuristic for few distributed transactions."
model: word-ram
complexity:
  vars: {m: "the number of accesses in the workload, the sum of the sizes of the transactions", d: the largest number of tuples in one transaction, k: the number of parts}
  time: {worst: "O(m d + m k)"}
  space: {extra: "O(m d)"}
properties: {deterministic: true, exact: false, online: false, in_place: false, recursive: false}
history:
  year: 2010
  people: [Carlo Curino, Evan Jones, Yang Zhang, Sam Madden]
  note: "Curino, Jones, Zhang and Madden presented Schism at VLDB 2010. It turned the choice of a partitioning for an OLTP database into a graph partitioning problem solved with METIS, and added replication and an explanation step."
prereqs: [horizontal-fragmentation, graph-partitioning-problem, shared-nothing-architecture]
see_also: [multilevel-graph-partitioning, hypergraph-partitioning, kernighan-lin, decision-tree-learning, hash-partitioning, data-allocation-problem, two-phase-commit, eager-and-lazy-replication]
sources:
  - paper: doi:10.14778/1920841.1920853
    title: "Carlo Curino, Evan Jones, Yang Zhang and Sam Madden, Schism: a workload-driven approach to database replication and partitioning, Proceedings of the VLDB Endowment 3(1-2), 2010, pages 48 to 57"
    locator: the graph of tuples and transactions, the star graph for replication, the use of METIS, the explanation phase with a decision tree, the final validation against hash partitioning and full replication, and the experiments on TPC-C and TPC-E (general locator)
  - paper: doi:10.1137/S1064827595287997
    title: George Karypis and Vipin Kumar, A fast and high quality multilevel scheme for partitioning irregular graphs, SIAM Journal on Scientific Computing 20(1), 1998, pages 359 to 392
    locator: the multilevel scheme with heavy edge matching, partitioning of the coarsest graph, and refinement during uncoarsening, which METIS implements
---

Schism chooses where each tuple of an OLTP database lives on a [shared-nothing](/shared-nothing-architecture/) cluster, so that few transactions need more than one node. It reads a trace of the workload and builds a graph with a node for each tuple and an edge for each pair of tuples that a transaction uses together. A balanced min cut of this graph, found with METIS, gives a fine-grained placement, and a star for each tuple lets the cut decide which tuples to copy. A decision tree then explains the placement as a few range predicates on the attributes, and a last check keeps whichever of the candidates causes the fewest distributed transactions. Every step after the graph is a heuristic.

## In plain words

A bank spreads its accounts over several servers. A transfer that touches two accounts on two servers is slow, because the servers must agree before they commit. Schism looks at a log of real transactions and draws a line between every two records that one transaction used. Records that are used together a lot get thick lines. It then cuts the drawing into equal pieces while it cuts as few thick lines as it can, and each piece goes to one server. A record that many transactions read but few change can be copied to several servers. Last, Schism looks for a simple rule, such as "accounts 1 to 1000 go to server 1", that gives about the same pieces, because a short rule is easier to keep than a list of every record.

## The problem

The input is a database of tuples, a workload of $m$ accesses grouped into transactions, and a number of parts $k$. Transaction $x$ reads a set $R(x)$ and writes a set $W(x)$ of tuples. A placement $P$ gives each tuple a nonempty set $P(t)$ of parts that hold a copy. Transaction $x$ is *local* if one part $p$ holds a copy of every tuple of $x$ and every tuple that $x$ writes has the single copy $\{p\}$, because a write must update every copy. Otherwise $x$ is *distributed* and needs a protocol such as [two-phase commit](/two-phase-commit/).

The goal is a placement with few distributed transactions and parts of about equal load. The cost is a count of transactions, not of tuples or bytes; the network cost of a distributed transaction is not modelled. When every transaction touches two tuples and there is no replication, the cost is exactly the cut weight of the graph below, so the problem is close to the [balanced graph partitioning problem](/graph-partitioning-problem/), which is NP-hard. Schism uses heuristics and makes no claim of optimality. It is a case of [horizontal fragmentation](/horizontal-fragmentation/) at the level of single tuples, chosen from the workload rather than from predicates written by a designer.

## The algorithm

```pseudo id=main
SCHISM(D, workload, k)
L1  G ← a node for each touched tuple, weighted by its accesses; an edge {t, t'} weighted by the number of transactions that touch both
L2  if replication is allowed then replace each tuple t by a star: a center and a replica per transaction that touches t; the star edges weigh the number of writes of t; the edges of each transaction join its replicas
L3  π ← a balanced k-way partition of G with a small cut weight    ▷ METIS in the paper
L4  lookup(t) ← the set of parts of the nodes of t in π
L5  tree ← a decision tree that predicts lookup(t) from the attributes of t
L6  for each candidate P in (hash, full replication, tree, lookup) do cost(P) ← the number of distributed transactions under P
L7  return the candidate with the smallest cost, the simplest one on a tie
```

**The graph.** Without replication, a cut edge $\{t, t'\}$ means that its transactions touch two parts. With replication, tuple $t$ becomes a center $c_t$ and one replica $r_{t,x}$ for each transaction $x$ that touches it. The transaction edges join the replicas of one transaction. A star edge $\{c_t, r_{t,x}\}$ weighs $u(t)$, the number of transactions that write $t$. If the cut puts a replica in another part than its center, the tuple gets a second copy, and the cut pays $u(t)$ for it: a copy is cheap for a tuple that is seldom written, and free for a tuple that is only read.

**The partitioner.** Line L3 is the [graph partitioning problem](/graph-partitioning-problem/) with a balance bound: every part may weigh at most $(1 + \epsilon)$ times the mean. The paper uses METIS, a [multilevel](/multilevel-graph-partitioning/) partitioner. The implementation on this page does the same in a small form: heavy edge matching to coarsen the graph, a greedy start on the smallest graph, and a local search with moves and swaps in the style of [Kernighan-Lin](/kernighan-lin/) at each level on the way back.

**The explanation.** A lookup table with one entry per tuple is exact for the trace, but it is large, and it says nothing about tuples that the trace did not touch. Line L5 learns a [decision tree](/decision-tree-learning/) on the attributes that the queries use in their predicates. Each leaf of the tree is a conjunction of range predicates, so the tree is a range partitioning that a router can store in a few lines.

**The validation.** Line L6 counts distributed transactions for each candidate on the workload, and line L7 keeps the best. If no candidate beats [hash partitioning](/hash-partitioning/) or full replication, Schism returns the simple scheme.

## Example

A database has eight tuples. Tuples 1, 2 and 3 belong to warehouse 1, tuples 4, 5 and 6 to warehouse 2, and tuples 7 and 8 are items that nobody writes. There are $k = 2$ parts and six transactions:

| transaction | reads | writes |
|---|---|---|
| $x_1$ | 7 | 1, 2 |
| $x_2$ | 8 | 2, 3 |
| $x_3$ | 7 | 4, 5 |
| $x_4$ | 8 | 5, 6 |
| $x_5$ | | 1, 3 |
| $x_6$ | | 4, 6 |

**Without replication.** The graph has 8 nodes and 14 edges of weight 1. The best balanced cut has weight 4: warehouse 1 with item 7 on one side and warehouse 2 with item 8 on the other, or a mirror of it. Both items do not fit on one side under the balance bound, so each item lives with one warehouse. The two transactions that read the item of the other warehouse, here $x_2$ and $x_3$, are distributed.

**With replication.** The graph has 24 nodes (8 centers and 16 replicas) and 26 edges of total weight 38. Each of the tuples 1 to 6 is written twice, so its two star edges weigh 2. The items are never written, so their stars have no edges. The partitioner finds a cut of weight 0: the two warehouses go to different parts, and each item gets a copy in both parts. Now no transaction is distributed.

**Explanation and validation.** The tree learned from the placement has three leaves: $id \le 3$ goes to the part of warehouse 1, $3 < id \le 6$ to the part of warehouse 2, and $id > 6$ to both parts. The counts of distributed transactions are:

| candidate | without replication | with replication |
|---|---|---|
| hash on $id \bmod 2$ | 4 | 4 |
| full replication | 6 | 6 |
| decision tree | 2 | 0 |
| lookup table | 2 | 0 |

Full replication makes every transaction distributed, since every transaction writes. With replication, the tree ties with the lookup table and is simpler, so Schism returns the three range predicates. The tests of the implementation check every number in this example.

## Correctness

Schism has no guarantee of optimality. What can be proved is the link between the cut and the cost, for any partition, on [the proof page](proofs/correctness.md):

- **Theorem.** Without replication, the number of distributed transactions is at most the cut weight, and the two are equal when every transaction touches at most two tuples.
- **Theorem.** With the star graph, the number of distributed transactions under the placement of line L4 is again at most the cut weight. So a cut of weight 0 gives a placement where every transaction is local.
- **By construction.** Line L7 never returns a placement that is worse on the trace than hash partitioning or full replication.

The cut can be much larger than the cost: a transaction with $d$ tuples split in two halves cuts up to $d^2/4$ of its own edges but counts once. This is why line L6 measures the real count.

## Complexity

- **Graph size.** A transaction with $d$ tuples adds $d(d - 1)/2$ edges, so the graph has $O(m)$ nodes and $O(m d)$ edges, and line L1 or L2 takes $O(m d)$ time. With replication, the number of nodes is $m$ plus the number of tuples.
- **Partitioning.** METIS is built for large sparse graphs and is fast in practice; the page gives no bound for it. The local search of the implementation recomputes all gains at each step and is meant for small inputs.
- **Validation.** One candidate costs $O(m k)$ set operations.
- **The bound in the front matter.** $O(m d + m k)$ covers lines L1, L2, L4 and L6. It leaves out the partitioner of line L3 and the tree of line L5, which have no simple bound.
- **Graph size in practice.** The graph grows with the trace, not with the database, and wide transactions make it dense. The paper keeps it small with sampling and filtering heuristics.

## Properties

- **Workload driven.** The placement fits the trace. If the access pattern changes, the placement has to be computed again.
- **Fine grained.** Unlike [hash partitioning](/hash-partitioning/) or [range partitioning](/range-partitioning/) on one key, the lookup table can follow any grouping of tuples, for example the tuples of one customer in several tables.
- **Heuristic at two levels.** The cut weight is a proxy for the count of distributed transactions, and the partitioner only finds a small cut, not the smallest.
- **Replication costs writes.** The star graph trades the reads that a copy makes local against the writes that every copy must take.
- **Explainable.** When the tree fits well, the result is a short set of range predicates over attributes such as a warehouse id, which a database designer can read and check.

## Variants and improvements

- **Graph or hypergraph.** A transaction is really a hyperedge on its tuples, and a [hypergraph partitioning](/hypergraph-partitioning/) counts each cut transaction once, which matches the cost better than the clique of edges. Later systems model the workload this way.
- **Sampling and filtering.** The paper shrinks the graph with sampling of the trace and with filters that drop parts of the trace that add many edges and little information.
- **Balance on data or on load.** The node weights can be the number of accesses, as on this page, or the size of the tuple.
- **Other partitioners.** The cut step can use any balanced partitioner, such as [Kernighan-Lin](/kernighan-lin/), [Fiduccia-Mattheyses](/fiduccia-mattheyses/) or a [multilevel](/multilevel-graph-partitioning/) method. The difference from the [graph partitioning problem](/graph-partitioning-problem/) itself is that Schism adds the workload graph, the replication stars, the explanation and the validation around it.
- **Data allocation.** Schism decides which tuples go together and how many copies they get. Which node gets which part is a separate question, the [data allocation problem](/data-allocation-problem/).

## When to use it

Use Schism for an OLTP database with many short transactions, a trace that represents the future workload, and a cluster where distributed transactions are costly. It works best when the data has a hidden grouping, such as the warehouses of a TPC-C database, that a single hash key does not show. For analytic workloads with large scans and joins, the [parallel hash join](/parallel-hash-join/) and plain hash partitioning are a better fit.

## Pitfalls

- **Overfitting the trace.** The lookup table is exact only for the tuples and transactions of the trace. New tuples need the tree, or a default such as hashing.
- **Balanced cut, unbalanced load.** A cut can be balanced in the node weights of the graph but not in the real load, if the weights do not match the cost of the accesses.
- **Copies of hot written tuples.** A tuple that many transactions read and also write should not be copied. The star edges weigh its writes, but a partitioner that ignores the balance of copies can still make a poor choice.
- **Big graphs.** One large scan in the trace adds a clique on all its tuples. Filter such statements before building the graph.
- **Reading the cut as the cost.** The cut overcounts wide transactions. Compare candidates by the count of distributed transactions, as line L6 does.

## Implementations

## History

Curino, Jones, Zhang and Madden presented Schism at VLDB 2010, in the context of shared-nothing OLTP systems where distributed transactions limit the throughput. Earlier work on distributed database design chose fragments from predicates and allocated them with cost models, as in [horizontal fragmentation](/horizontal-fragmentation/) and the [data allocation problem](/data-allocation-problem/). Schism instead worked from a trace at the level of single tuples, used a graph partitioner from scientific computing, and returned a range partitioning that a designer could read. The paper reports experiments on TPC-C, TPC-E and other workloads.

## References
