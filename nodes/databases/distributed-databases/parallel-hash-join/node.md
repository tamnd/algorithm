---
tag: XNDHHS
kind: algorithm
slug: parallel-hash-join
name: Parallel hash join
aliases:
- partitioned parallel hash join
- Gamma hash join
area: databases/distributed-databases
level: core
summary: "Hash-partition both inputs across the nodes on the join key in one round of messages, then let each node join its pair of partitions locally. A frequent key value puts all its work on one node."
solves: [relational-join]
model: bsp-model
complexity:
  vars: {n: "the number of input tuples, |R| + |S|", p: the number of nodes, z: the number of output tuples, L: the largest number of input tuples at one node after the redistribution, D: the largest number of output tuples at one node}
  time: {worst: "O(n/p + L + D)", expected: "O(n/p + L + D)"}
  space: {extra: O(n)}
  communication: {worst: O(n), expected: "n(p - 1)/p"}
  messages: {worst: "p(p - 1)"}
properties: {deterministic: true, exact: true, online: false, in_place: false, recursive: false}
history:
  year: 1983
  people: [Masaru Kitsuregawa, Hidehiko Tanaka, Tohru Moto-oka, David J. DeWitt, Robert H. Gerber]
  note: "The GRACE database machine (1983) split relations into buckets by hashing so that bucket pairs could be joined in parallel. DeWitt and Gerber (1985) gave multiprocessor Grace and Hybrid hash joins, and the Gamma machine made the parallel Hybrid hash join its default join."
prereqs: [hash-join, shared-nothing-architecture]
see_also: [grace-hash-join, hybrid-hash-join, hash-partitioning, data-skew, reduce-side-join, hypercube-shares-join, exchange-operator, bloom-join]
sources:
  - paper: "David J. DeWitt and Robert H. Gerber, Multiprocessor hash-based join algorithms, Proceedings of the 11th International Conference on Very Large Data Bases (VLDB), 1985, pages 151 to 164"
    locator: Section 4.2.1 (the multiprocessor Grace hash join with partitioning nodes and joining nodes), Section 4.2.2 (the multiprocessor Hybrid hash join), and Section 4.3.2 (the assumption that the smaller relation fits in the aggregate memory, and bucket overflow)
  - paper: doi:10.1007/BF03037022
    title: Masaru Kitsuregawa, Hidehiko Tanaka and Tohru Moto-oka, Application of hash to data base machine and its architecture, New Generation Computing 1(1), 1983, pages 63 to 74
    locator: the GRACE hash join, which partitions both relations into buckets by hashing and joins each pair of buckets separately
  - paper: doi:10.1109/69.50905
    title: David J. DeWitt, Shahram Ghandeharizadeh, Donovan A. Schneider, Allan Bricker, Hui-I Hsiao and Rick Rasmussen, The Gamma database machine project, IEEE Transactions on Knowledge and Data Engineering 2(1), 1990, pages 44 to 62
    locator: the sections on declustering (round robin, hashed and range partitioning), on split tables, and on the join operator (the parallel Hybrid hash join is the default), and the speedup and scaleup measurements of join queries
  - book: isbn:9783030262525
    title: M. Tamer Özsu and Patrick Valduriez, Principles of Distributed Database Systems, fourth edition, Springer, 2020
    locator: Chapter 8, Parallel Database Systems
---

The parallel hash join computes the equi-join $R \bowtie S$ on a [shared-nothing](/shared-nothing-architecture/) machine of $p$ nodes. Every node sends each of its tuples to the node that a hash function of the join key chooses, so that tuples with the same key meet at the same node, and then every node runs an ordinary [hash join](/hash-join/) on what it received. It is the parallel form of the [Grace hash join](/grace-hash-join/): Grace puts the hash partitions on one disk and joins them one after the other, while this algorithm puts them on different nodes and joins them at the same time. The method is a direct use of [hash partitioning](/hash-partitioning/), and it is the database form of the [reduce-side join](/reduce-side-join/) of MapReduce.

## In plain words

Ten clerks share a big pile of orders and a big pile of customer cards. Each clerk has a part of each pile on the desk. To match orders with customers, they agree on a rule: the last digit of the customer number tells which clerk gets the paper. Every clerk walks through the papers on the desk and hands each one to the clerk that the rule names. After that, all papers with the same customer number lie on one desk. Each clerk now matches the papers on the desk alone, and no clerk needs to talk to another again.

The plan works well when the papers spread evenly. If half of the orders belong to one customer, one clerk gets half of the work and the other clerks wait.

## The problem

The input is two bags $R$ and $S$, spread over $p$ nodes: node $i$ holds the parts $R_i$ and $S_i$, and $R$ is the bag union of the $R_i$. The output is the natural join $R \bowtie S$ under bag semantics, as on the [relational join problem](/relational-join/): if a tuple $r$ of $R$ matches a tuple $s$ of $S$ on the common attributes $J$, the output holds $r \cdot s$ once for each pair of copies, and a NULL in $J$ matches nothing. A routing key $K$ is a nonempty subset of $J$, often all of $J$. The output may stay spread over the nodes.

**Cost model.** The nodes share no memory and no disk, and send messages over a network. The cost has three parts: the number of tuples sent from one node to a different node, the number of messages, and the number of communication rounds. Local work is counted apart, as the largest load on one node, because the slowest node decides when the join ends. The page uses $n = |R| + |S|$ for the number of input tuples and $z$ for the number of output tuples. In the [BSP model](/bsp-model/), the redistribution is one superstep whose $h$-relation is the largest number of tuples that one node sends or receives.

## The algorithm

```pseudo id=main
PARALLEL-HASH-JOIN(R_0..R_{p-1}, S_0..S_{p-1}, K, h)    ▷ node i holds R_i and S_i
L1  for each node i = 0, ..., p - 1 do in parallel       ▷ redistribution, one round
L2      for each tuple r of R_i do send r to node h(r[K]) mod p
L3      for each tuple s of S_i do send s to node h(s[K]) mod p
L4  for each node j = 0, ..., p - 1 do in parallel       ▷ local join phase
L5      R'_j, S'_j ← the tuples of R and of S that node j received
L6      build a hash table on R'_j with the key r[J]
L7      for each s in S'_j and each r in the bucket of s with r[J] = s[J] do output r · s at node j
L8  return the bag union of the outputs of all nodes
```

Lines L1 to L3 are the redistribution phase, also called the shuffle. A tuple whose target is its own node does not use the network. All sends go out in the same round, so the cost is one round no matter how many nodes there are. Lines L4 to L7 are the build and probe phases of the [hash join](/hash-join/), done at each node on its own data. If $R'_j$ does not fit in the memory of node $j$, the node runs a [Grace](/grace-hash-join/) or [hybrid hash join](/hybrid-hash-join/) instead; this changes the local disk cost, not the network cost.

The function $h$ in line L2 must be the same at every node, and it must be computed from the key value only. The local hash table in line L6 should use a different hash function than $h$: every key at node $j$ has the same value of $h$ modulo $p$, so a table indexed by $h$ modulo a multiple of $p$ would use only a fraction of its buckets.

## Example

Let $p = 3$ and $h(v) = v$, so the target of key $v$ is $v \bmod 3$. $R(A, B)$ has the tuples $r_0$ to $r_7$ with the keys $3, 1, 4, 1, 5, 9, 2, 6$, and $S(A, C)$ has the tuples $s_0$ to $s_5$ with the keys $1, 4, 1, 8, 5, 3$. The tuples start in round robin order: tuple number $k$ is at node $k \bmod 3$.

| node | holds at the start | receives in lines L1 to L3 | local output |
|---|---|---|---|
| 0 | $r_0$ (3), $r_3$ (1), $r_6$ (2); $s_0$ (1), $s_3$ (8) | $r_0, r_5, r_7$; $s_5$ | $r_0 s_5$: 1 tuple |
| 1 | $r_1$ (1), $r_4$ (5), $r_7$ (6); $s_1$ (4), $s_4$ (5) | $r_1, r_2, r_3$; $s_0, s_1, s_2$ | key 1: $2 \times 2 = 4$, key 4: 1; 5 tuples |
| 2 | $r_2$ (4), $r_5$ (9); $s_2$ (1), $s_5$ (3) | $r_4, r_6$; $s_3, s_4$ | $r_4 s_4$: 1 tuple |

Only $r_0$, $r_1$ and $s_1$ are already at their target node, so 11 of the 14 tuples cross the network, in 6 messages, one for each ordered pair of different nodes. The nodes hold 4, 6 and 4 tuples after the shuffle and output 1, 5 and 1 tuples, which make the 7 tuples of $R \bowtie S$. For comparison, a broadcast of $R$ to the two other nodes sends 16 tuples, and a broadcast of $S$ sends 12.

Skew changes the picture. Take $p = 4$, 12 tuples of $R$ and 8 tuples of $S$, all with the key 7, placed round robin. Every tuple goes to node $h(7) \bmod 4$. That node holds all 20 tuples and computes all 96 output tuples, and the other three nodes do nothing. The tests of the implementation check both runs.

## Correctness

Two tuples that match agree on $J$, so they agree on $K \subseteq J$, have the same value of $h$, and are sent to the same node. Each copy of a tuple is sent to exactly one node, so each matching pair is joined at exactly one node, by the hash join of lines L6 and L7, and the bag union of line L8 has the right count for every output tuple. The full proof, with the network cost and the skew bound, is in [the proof page](proofs/correctness.md).

## Complexity

- **Network (theorem).** Each tuple is sent at most once, so at most $n$ tuples cross the network, in one round and at most $p(p - 1)$ messages. If $h$ maps keys to nodes uniformly and independently, and the start node of a tuple does not depend on its key, a tuple stays home with probability $1/p$, and the expected number of tuples sent is $n(p - 1)/p$. If both inputs are already hash-partitioned on $K$ with the same $h$, nothing is sent.
- **Local work.** Node $j$ does $O(|R'_j| + |S'_j| + z_j)$ expected work, where $z_j$ is its output. The join ends when the slowest node ends, so the time is $O(n/p + L + D)$, where $n/p$ is the scan of the local parts (when they start even), $L$ the largest load after the shuffle and $D$ the largest local output.
- **Balance (theorem and its limit).** Under a uniform random $h$, each node receives $n/p$ tuples in expectation. When every key value has few tuples, the largest load is close to $n/p$ with high probability, by a [Chernoff bound](/chernoff-bound/). But if one key value has $m_R$ tuples in $R$ and $m_S$ in $S$, one node receives all $m_R + m_S$ of them and outputs $m_R m_S$ tuples, whatever $h$ is. See [data skew](/data-skew/).
- **Memory.** In total $O(n)$ for the inputs; node $j$ needs room for the hash table on $R'_j$.

## Properties

- **One round.** The algorithm talks once. Later nodes do not wait on one another, so the method scales with $p$ when the keys spread well. Gamma reported join speedup that was close to linear on a 32 node machine (a measurement, DeWitt et al. 1990).
- **Equality only.** Hash routing can only bring together tuples with equal keys. A band join or an inequality join needs range routing or a broadcast.
- **Exact under bags.** Duplicates and their counts survive, because each copy is routed once and joined once.
- **Pipelined.** A node can start the probe of line L7 as soon as it has all its tuples of $R$, so in Gamma the build relation is redistributed first and the probe relation streams after it.
- **Skew sensitive.** The load of a node is the sum over the key values that $h$ sends to it. Uniform $h$ balances the number of distinct keys, not the number of tuples.

## Variants and improvements

- **Grace and Hybrid on each node.** DeWitt and Gerber (1985) made multiprocessor versions of the Grace and the Hybrid hash joins. In their Grace version, nodes with disks partition the inputs and send buckets to diskless joining nodes. In the Hybrid version, every node has a disk and both partitions and joins. A tuple whose bucket belongs to the node that partitions it goes at once into the local build or probe, so the Hybrid version puts less load on the network than the Grace version.
- **Bit vector filters.** A node can send a bit vector of the keys of $R'_j$ to the nodes of $S$ before the probe, so that tuples of $S$ with no match are not sent. This is a [Bloom filter](/bloom-filter/) used as in the [Bloom join](/bloom-join/). DeWitt and Gerber report that the filter helped all the join methods they measured.
- **Broadcast join.** If $R$ is small, send all of $R$ to every node and leave $S$ where it is. The cost is $|R|(p - 1)$ tuples, and skew in $S$ does no harm. This is the [map-side join](/map-side-join/) of MapReduce.
- **Co-located join.** If both relations are already partitioned on the join key with the same function, as a [horizontal fragmentation](/horizontal-fragmentation/) can arrange, lines L1 to L3 send nothing.
- **Skew handling.** Find the frequent key values first, split the tuples of a frequent value on one side over several nodes and send the matching tuples of the other side to all of them. The [data skew](/data-skew/) page lists such methods.
- **More than two relations.** A chain of parallel hash joins shuffles once per join. The [HyperCube or Shares join](/hypercube-shares-join/) replicates tuples so that a multiway join needs only one round.
- **Operators in a plan.** The [exchange operator](/exchange-operator/) packs lines L1 to L3 into a plan operator, so that the local join stays a serial operator.

## When to use it

Use it for a large equi-join of two relations that are not partitioned on the join key, on a cluster of nodes that share nothing. If one relation is much smaller than the other, compare $|R|(p - 1)$ for a broadcast with about $n(p - 1)/p$ for the shuffle and pick the smaller one. If both relations are already partitioned on the key, join in place. If the key has a few very frequent values, add a skew step or use a broadcast.

## Pitfalls

- **Different hash functions at different nodes.** Line L2 and line L3 must use the same $h$ and the same $p$ at every node. A function that depends on a per process seed, such as the string hash of some languages, sends equal keys to different nodes and loses matches.
- **Routing on more attributes than the join uses.** $K$ must be a subset of the join attributes $J$. If $K$ holds an attribute outside $J$, two matching tuples can go to different nodes.
- **The same hash for routing and for the local table.** All keys at node $j$ have the same $h(v) \bmod p$. A local table indexed by $h(v) \bmod m$ with $m$ a multiple of $p$ puts them all in a few buckets.
- **Counting balance by keys.** A uniform hash function gives each node about the same number of distinct keys. The number of tuples can still be far from even. Measure the load in tuples.
- **Memory per node.** The build side must fit in the memory of each node, not in the total memory. DeWitt and Gerber point out that a bucket can overflow the memory of its node even when the smaller relation fits in the total memory.

## Implementations

## History

The GRACE database machine of Kitsuregawa, Tanaka and Moto-oka (1983) split the two relations into buckets by a hash function, so that each pair of buckets could be joined apart from the others and in parallel. DeWitt and Gerber (1985) gave multiprocessor versions of the Grace and Hybrid hash joins, measured them in a simulation, and found close to linear speedup. The Gamma machine of DeWitt et al. ran on 32 processors of an Intel iPSC/2 in 1990. It routed tuples through split tables, which map hash values to nodes, and used the parallel Hybrid hash join as its default join. The same plan returned in MapReduce as the reduce-side join.

## References
