---
tag: 1NWMTW
kind: concept
slug: shared-nothing-architecture
name: Shared-nothing architecture
aliases:
- shared nothing
- shared-disk and shared-memory architectures
area: databases/distributed-databases
level: intro
summary: "A parallel database design in which each node has its own processors, memory and disks, and the nodes work together only by messages. Partitioned data lets it scale out."
see_also: [parallel-hash-join, horizontal-fragmentation, hash-partitioning, range-partitioning, data-skew, speedup, amdahls-law, exchange-operator]
sources:
  - paper: "Michael Stonebraker, The case for shared nothing, IEEE Database Engineering Bulletin 9(1), 1986, pages 4 to 9"
    locator: the comparison of shared memory, shared disk and shared nothing designs for parallel database systems, and the argument that shared nothing scales best
  - paper: doi:10.1145/129888.129894
    title: David DeWitt and Jim Gray, Parallel database systems, the future of high performance database systems, Communications of the ACM 35(6), 1992, pages 85 to 98
    locator: the definitions of speedup and scaleup, the barriers to linear speedup (startup, interference and skew), the three hardware designs, and data partitioning by round robin, hash and range
  - book: isbn:9783030262525
    title: M. Tamer Özsu and Patrick Valduriez, Principles of Distributed Database Systems, fourth edition, Springer, 2020
    locator: Chapter 8, Parallel Database Systems, the part on parallel architectures
---

A shared-nothing system is a set of nodes, each with its own processors, memory and disks, joined by a network. No node can read the memory or the disks of another node; all cooperation goes through messages. Each relation is split into fragments that live on different nodes, and each operator runs on all the nodes at once, each on its own fragment. Stonebraker (1986) argued that this design scales to more nodes than the designs that share memory or disks, and most large parallel and distributed databases now use it.

## In plain words

Picture a library split over ten small branch buildings. Each branch has its own staff, its own shelves and its own catalog, and the branches talk only by phone. A question about all the books goes to every branch at once, each branch answers for its own shelves, and the answers are put together. To grow the library you add another branch; no branch waits for a shared door or a shared catalog. The weak point is balance: if most of the popular books sit in one branch, that branch does most of the work and the others wait.

## The idea

**Three designs.** Parallel database machines are often put in three classes by what the processors share.

- *Shared memory.* All processors use one memory and all disks. Any processor can do any work, and balancing the load is easy, but the memory bus and the cost of keeping caches consistent limit the number of processors.
- *Shared disk.* Each processor has its own memory, and all processors reach all disks over a network. A page that one node changes must be locked and sent to any other node that caches it, so the nodes still interfere.
- *Shared nothing.* Each node has its own memory and disks. Only messages cross the network, so the only shared resource is the network itself.

**Data is partitioned.** In a shared-nothing system, a relation is split by [horizontal fragmentation](/horizontal-fragmentation/) into parts, one or more per node. DeWitt and Gray (1992) list three common rules: round robin (tuple $i$ goes to node $i \bmod p$), [hash partitioning](/hash-partitioning/) (a hash of a key chooses the node) and [range partitioning](/range-partitioning/) (ranges of a key go to different nodes). A query that names one key value goes to one node under hash or range partitioning, while a full scan goes to all of them.

**Operators are parallel.** A scan, a selection or an aggregation runs on every node on its local part, and the partial results are combined. A join of two relations that are not partitioned on the join key first sends each tuple to the node that the key chooses, then joins locally; this is the [parallel hash join](/parallel-hash-join/). The [exchange operator](/exchange-operator/) packs this sending into a plan operator.

**Speedup and scaleup.** DeWitt and Gray measure a parallel system in two ways.

- *Speedup* is the time of a fixed job on a small system divided by its time on a system that is $p$ times larger. The ideal is linear speedup, a factor of $p$.
- *Scaleup* is the time of a job on a small system divided by the time of a job that is $p$ times larger on a system that is $p$ times larger. The ideal is linear scaleup, a value of 1.

They name three barriers to linear speedup: *startup*, the time to start the work at many nodes; *interference*, the slowdown when nodes compete for shared resources; and *skew*, when one node gets more than its share of the work and the job waits for it. A shared-nothing design removes most of the interference, so startup and [data skew](/data-skew/) remain the main limits. [Amdahl's law](/amdahls-law/) gives the limit when part of the job cannot run in parallel.

## Examples

**Speedup and scaleup.** A scan of 100 GB takes 100 s on 1 node. On 10 nodes with the data spread evenly it takes 12 s, of which 2 s is the time to start the query at all nodes and to combine the answers. The [speedup](/speedup/) is $100/12 \approx 8.3$, not 10, because of the startup time. A scan of 1,000 GB on 10 nodes takes 110 s, so the scaleup is $100/110 \approx 0.91$.

**Skew.** The same 10 nodes hold a relation that is hash partitioned on a customer number. If one customer owns 30 percent of the rows, the node of that customer holds at least 30 percent of the data, and a scan of all the rows takes at least 30 percent of the time of one node, so the speedup is at most about 3.3, whatever the other nodes do.

**Local and global work.** A relation of orders is hash partitioned on the order number over 4 nodes. A lookup of one order by its number goes to one node. A lookup by customer number must go to all 4 nodes, unless there is also a partitioning or an index on the customer number.

**Systems.** The Gamma machine of DeWitt and his students, the Teradata database machine and Tandem NonStop SQL are early shared-nothing systems that DeWitt and Gray (1992) describe. Later parallel databases and the [MapReduce](/mapreduce-model/) family of systems use the same design.

## Where it is used

- Parallel data warehouses, where large scans and joins run on all nodes at once, with the [parallel hash join](/parallel-hash-join/) as the main join.
- Distributed transaction systems that split the data over servers by a shard key, as in [sharding](/sharding/), and that try to keep each transaction on one node, as [Schism](/schism-partitioning/) does.
- The design of fragments and their placement, studied as the [data allocation problem](/data-allocation-problem/).
- Batch systems such as MapReduce, whose shuffle phase is the redistribution step of a shared-nothing join.

## References
