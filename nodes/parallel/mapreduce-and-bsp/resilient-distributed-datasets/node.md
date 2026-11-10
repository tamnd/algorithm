---
tag: RWTK7Z
kind: concept
slug: resilient-distributed-datasets
name: Resilient distributed datasets
aliases:
- RDD
- immutable distributed collections with lineage
area: parallel/mapreduce-and-bsp
level: advanced
summary: Read-only partitioned collections built by deterministic bulk operations. Each records its lineage, so a lost partition is recomputed from its parents and data can stay in memory.
prereqs: [mapreduce-model, fault-tolerance-by-recomputation]
see_also: [iterative-mapreduce, checkpointing, pagerank, pregel-model, hash-partitioning, shuffle-phase, speculative-execution]
sources:
  - paper: "Matei Zaharia, Mosharaf Chowdhury, Tathagata Das, Ankur Dave, Justin Ma, Murphy McCauley, Michael J. Franklin, Scott Shenker and Ion Stoica, Resilient distributed datasets: a fault-tolerant abstraction for in-memory cluster computing, NSDI 2012"
    locator: Section 2.1 (the definition of an RDD), Section 2.3 (RDDs against distributed shared memory), Section 3.2.2 (PageRank), Section 4 (the RDD interface and narrow and wide dependencies), Section 5.1 (job scheduling and stages), Section 5.4 (checkpointing)
  - paper: "Matei Zaharia, Mosharaf Chowdhury, Michael J. Franklin, Scott Shenker and Ion Stoica, Spark: cluster computing with working sets, HotCloud 2010"
    locator: the first description of Spark and of RDDs with lineage
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, OSDI 2004"
    locator: Section 3.3, re-execution of lost tasks, which RDD lineage generalizes
---

A resilient distributed dataset (RDD) is a read-only collection of records, split into partitions over the machines of a cluster, that can be built only by deterministic bulk operations such as map, filter and join, from stable storage or from other RDDs. Zaharia and others introduced RDDs in Spark (2010 to 2012). An RDD does not store how to recover its data as copies; it stores its lineage, the operations that made it from its parents. If a machine fails, the system computes the lost partitions again from the lineage. Because recovery needs no copies, an RDD can stay in memory and be reused across the iterations of an algorithm.

## In plain words

Think of a spreadsheet where some sheets hold raw data and every other sheet is computed by a formula from earlier sheets. You never type into a computed sheet; you only add new sheets with new formulas. Now, if someone tears out a page of a computed sheet, you do not need a backup copy. You look at its formula and work that page out again from the pages it came from. If those pages are also gone, you work them out first, going back as far as needed. This is cheap when a formula uses only the matching page of the sheet before it. It costs more when a page needs every page of an earlier sheet, so such results are worth keeping or saving.

## The idea

**Definition (Section 2.1).** An RDD is a read-only, partitioned collection of records. It can be created only by deterministic operations, called transformations, on data in stable storage or on other RDDs. Each RDD records five things (Section 4):

- its list of partitions;
- its dependencies, the parent RDDs and which of their partitions each partition needs;
- a function that computes a partition from the parent partitions;
- optionally, a partitioner, such as a [hash partitioner](/hash-partitioning/), which tells which key is in which partition;
- optionally, preferred locations, such as the machines that hold the blocks of an input file.

Transformations are lazy: `map`, `filter`, `join` or `reduceByKey` only build a new RDD object. An action, such as `count`, `collect` or `save`, makes the scheduler compute the partitions that it needs. The program may call `persist` on an RDD to keep its partitions in memory after the first computation.

**Narrow and wide dependencies (Section 4).** A dependency is narrow when each partition of the parent is used by at most one partition of the child, as in `map`, `filter` and a join of two RDDs that have the same partitioner. It is wide when a partition of the child may need data from every partition of the parent, as in `reduceByKey` and `groupByKey`, which need a [shuffle](/shuffle-phase/). The difference matters twice:

- *Scheduling (Section 5.1).* A chain of narrow dependencies runs as one pipeline on each partition, without writing the data in between. The scheduler cuts the lineage graph into stages at the wide dependencies, and, as in MapReduce, it writes the map side of each shuffle to the local disks of the workers.
- *Recovery.* A lost partition with narrow dependencies needs only its own parent partitions. A lost partition with a wide dependency needs a piece of every parent partition. The stored shuffle outputs give these pieces, but if some of them are lost too, the matching parent partitions must be computed again.

**Recovery.** To get partition $i$ of an RDD $D$, the system runs this procedure.

```pseudo
procedure PARTITION(D, i)
    if D is checkpointed then return the data in stable storage
    if D is persisted and partition i is in memory then return it
    for each parent P of D and each partition j of P that partition i needs do
        if the dependency is wide and the shuffle output of (P, j) is stored then
            use it
        else
            compute PARTITION(P, j)            ▷ recursively, along the lineage
    data ← the function of D on those parent partitions
    if D is persisted then keep data in memory
    return data
```

The recovery gives the same data as the first computation by the argument for [re-execution](/fault-tolerance-by-recomputation/): the input in stable storage does not change, and every function along the lineage is deterministic, so by induction on the lineage graph, each recomputed partition equals the original one. The cost of a recovery is the work along the lineage back to data that is still in memory, in stored shuffle outputs, or in stable storage. Lost partitions of a narrow chain are rebuilt in parallel on many machines.

**Checkpointing (Section 5.4).** When the lineage is long and has wide dependencies, as in the ranks of PageRank after many iterations, the loss of one partition can force the system to compute much of the history again. A program can then checkpoint an RDD: write it to replicated stable storage, which cuts its lineage. Lineage handles the common case cheaply, and checkpoints bound the worst case.

**Why bulk operations (Section 2.3).** A distributed shared memory lets a program write any single cell, so fault tolerance needs checkpoints of the memory or a log of every write. An RDD changes only by a whole-dataset transformation, so the log is one entry per operation, not one per record. The price is that RDDs suit batch computations that apply the same operation to many records, not programs with many small writes to shared state, such as the storage of a web application.

## Examples

**PageRank (Section 3.2.2).** The paper writes PageRank like this, with $\alpha$ the probability of a random jump, so the follow probability is $1 - \alpha$.

```pseudo
links ← the (url, list of out-links) pairs, partitioned by url, persisted
ranks ← links.mapValues(v ↦ 1/N)
for t ← 1 to ITERATIONS do
    contribs ← links.join(ranks).flatMap((url, (outs, r)) ↦ [(d, r/|outs|) for d in outs])
    ranks ← contribs.reduceByKey(+).mapValues(s ↦ α/N + (1 − α) s)
```

`links` and every `ranks` share the hash partitioner, so the join is narrow: each partition of `links` meets the matching partition of `ranks` on the same machine, and the graph is never shuffled again after the first step. Only the contributions are shuffled, as in a [Pregel](/pregel-model/) superstep. In the simulator of this page, the lineage of `ranks` after $k$ iterations has depth $3 + 4k$ (the input, `links`, the first ranks, and four RDDs per iteration), and the input is read once per partition however many iterations run, because `links` is persisted. After half of the cached partitions and stored shuffle outputs are lost at random, the next action gives the same ranks, equal to the exact power iteration.

**A pitfall in the same program.** Take $N = 4$, the links $0 \to \{1, 2\}$, $1 \to \{2\}$, $2 \to \{0\}$, $3 \to \{0, 2\}$, and $\alpha = 0.15$. Vertex $3$ has no in-link, so it gets no contribution, and `reduceByKey` has no key $3$: the new `ranks` has no entry for it, and in the next join its links meet nothing. After three iterations the program returns $(0.3019, 0.2205, 0.3811)$ for vertices $0$ to $2$ and nothing for $3$. The exact values of [PageRank](/pagerank/) after three steps are $(0.3314, 0.2273, 0.4038, 0.0375)$. Adding the edge $2 \to 3$, so that every vertex has an in-link, makes the program exact. A full program adds the jump term for every vertex, for example by a join with all vertex keys.

**Recovery, narrow and wide.** In the simulator, an RDD `a = input.map(...)` with $P$ partitions is persisted, and `b = a.map(...)` is computed. After a failure that drops some cached partitions of `a`, the next action on `b` computes `input` and `a` only for the lost partitions. For `c = a.reduceByKey(...)`, losing partition $0$ of `c` costs one computation of `c` and none of `a`, because the shuffle outputs are stored. If the shuffle outputs are lost too, all $P$ partitions of `a` are computed again, unless `a` is persisted.

**A non-example: a random map.** An RDD built by `map(x ↦ x + random())` is not deterministic. When a partition of it is lost and recomputed, the new partition differs from the old one, and an RDD derived from both versions mixes them. The simulator shows this on seeded runs. Spark programs that need random numbers derive them from a fixed seed and the partition number.

## Where it is used

- Apache Spark, whose higher-level APIs (DataFrames and SQL, streaming in small batches, graph and machine learning libraries) run on RDDs or on the same model of lineage and stages.
- Iterative algorithms that read the same data many times: [PageRank](/pagerank/), logistic regression, [k-means](/k-means/) and other machine learning methods, where the authors report speedups up to about $20$ times over Hadoop. It removes the per-round cost of [iterative MapReduce](/iterative-mapreduce/).
- Interactive queries, where a user loads a dataset into memory once and runs many queries on it.
- Other models expressed on RDDs. The paper shows that MapReduce, Pregel and the loop model of HaLoop can be written as RDD programs.
- Fault tolerance in dataflow systems in general. Lineage-based recovery extends the [re-execution](/fault-tolerance-by-recomputation/) of MapReduce from two fixed stages to any graph of deterministic operations, and uses [checkpointing](/checkpointing/) only where the lineage becomes too long.

## References
