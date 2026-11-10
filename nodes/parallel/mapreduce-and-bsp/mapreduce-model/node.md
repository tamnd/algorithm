---
tag: 5E46VV
kind: model
slug: mapreduce-model
name: MapReduce programming model
aliases:
- MapReduce
- map-reduce
- map/reduce
area: parallel/mapreduce-and-bsp
level: intro
summary: Computation as a map phase emitting key-value pairs, a shuffle by key, and a reduce phase per key.
prereqs: [hash-function, sorting-problem]
see_also: [word-count, shuffle-phase, combiner, partitioner, data-skew, mrc-model, bsp-model, mapreduce-communication-lower-bounds]
sources:
  - book: isbn:9781108476348
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition, Cambridge University Press, 2020
    locator: Chapter 2, Sections 2.2 (MapReduce, with 2.2.4 Combiners and 2.2.5 Details of MapReduce Execution), 2.5 (The Communication-Cost Model, with 2.5.2 Wall-Clock Time) and 2.6 (Complexity Theory for MapReduce, with 2.6.1 Reducer Size and Replication Rate and 2.6.6 Lower Bounds on Replication Rate)
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, 6th Symposium on Operating Systems Design and Implementation (OSDI), 2004"
    locator: Section 2 (programming model; 2.2 Types), Section 3.1 (execution overview, steps 1 to 7), Section 3.5 (task granularity), Section 4.1 (partitioning function) and Section 4.2 (ordering guarantees)
  - paper: doi:10.1145/1327452.1327492
    title: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, Communications of the ACM 51(1), 2008"
    locator: the journal version of the OSDI paper
  - book: isbn:9781608453429
    title: Jimmy Lin and Chris Dyer, Data-Intensive Text Processing with MapReduce, Morgan and Claypool, 2010
    locator: Chapter 2 (MapReduce basics, Sections 2.2 to 2.4)
  - paper: doi:10.1137/1.9781611973075.76
    title: Howard Karloff, Siddharth Suri and Sergei Vassilvitskii, A model of computation for MapReduce, Proceedings of the 21st ACM-SIAM Symposium on Discrete Algorithms (SODA), 2010
    locator: the definition of the class MRC (memory and machines sublinear in the input, a polylogarithmic number of rounds)
  - paper: doi:10.1145/2594538.2594558
    title: Paul Beame, Paraschos Koutris and Dan Suciu, Skew in parallel query processing, PODS 2014
    locator: Section 2 (the massively parallel computation model, servers, rounds and the load per server)
---

MapReduce is a programming model for computations on data that is spread over many machines. The programmer writes two functions, a map function that turns each input record into key-value pairs, and a reduce function that receives one key with all of its values. The system runs the map calls in parallel, moves every pair to the machine that owns its key (the [shuffle](/shuffle-phase/)), sorts by key, and runs the reduce calls in parallel. Dean and Ghemawat described the model and Google's system in 2004. In theory, the cost of a MapReduce algorithm is measured by its number of rounds, the data it moves between machines, and the largest input of one reducer.

## The machine

The input is a set of records $(k_1, v_1)$ in a distributed file system. The user gives two functions with these types:

$$\text{map}: (k_1, v_1) \to \text{list}(k_2, v_2), \qquad \text{reduce}: (k_2, \text{list}(v_2)) \to \text{list}(v_3).$$

The map function sees one record and nothing else. The reduce function sees one intermediate key $k_2$ and the list of all values $v_2$ that any map call emitted with that key. The order of the values in the list is not fixed. Dean and Ghemawat (Section 2.2) write the result type of reduce as $\text{list}(v_2)$, the same type as the intermediate values. Hadoop and Lin and Dyer let reduce emit pairs $(k_3, v_3)$ of a new type. The model is the same.

One run of a map and a reduce phase is a **round** (also called a job). Dean and Ghemawat (Section 3.1) execute a round as follows.

1. The library cuts the input into $M$ **splits**, typically 16 MB to 64 MB each, and starts copies of the program on the cluster.
2. One copy is the **master**. It gives $M$ map tasks and $R$ reduce tasks to idle **workers**.
3. A map worker reads its split, calls map on each record, and buffers the output pairs in memory.
4. From time to time it writes the buffer to its local disk, cut into $R$ regions by the [partitioner](/partitioner/), by default $\text{hash}(k_2) \bmod R$. It tells the master where the regions are.
5. Reduce worker $j$ reads region $j$ from the local disk of every map worker. When it has all its data, it sorts the pairs by key so that equal keys are next to each other. It uses an [external sort](/external-merge-sort/) when the data does not fit in memory.
6. It calls reduce once for each distinct key, in increasing key order (Section 4.2), and appends the output to its output file.
7. When all tasks are done, the master returns control to the user program. The output is $R$ files, one for each reduce task.

Steps 4 and 5 together are the [shuffle](/shuffle-phase/). An optional [combiner](/combiner/) runs a local reduce on the map side before step 4. A computation that needs more than one round chains jobs, and the output files of one round are the input of the next, see [iterative MapReduce](/iterative-mapreduce/).

The master keeps $O(M \cdot R)$ state and makes $O(M + R)$ scheduling decisions (Section 3.5). Google ran jobs with $M = 200{,}000$ and $R = 5{,}000$ on 2,000 machines, so each worker runs many tasks. Many small tasks balance the load and make recovery fast: when a worker fails, the master runs its tasks again on other workers, see [fault tolerance by recomputation](/fault-tolerance-by-recomputation/) and [speculative execution](/speculative-execution/).

## What it counts

The model has no notion of a clock step. The theory of MapReduce counts the following quantities, in the terms of Leskovec, Rajaraman and Ullman (Mining of Massive Datasets, 3rd edition, Sections 2.5 and 2.6).

| Measure | Definition |
|---|---|
| rounds | the number of map and reduce phases run one after another |
| communication | the number of pairs (or bytes) that the map tasks send to the reduce tasks, summed over all rounds |
| reducer size $q$ | the largest number of values in the list of one key |
| replication rate $r$ | the number of pairs that the map tasks emit, divided by the number of inputs |
| largest reducer input $L$ | the largest number of pairs (or bytes) that one reduce task receives |

Here a "reducer" in the sense of $q$ is one key with its list, not a reduce task. A reduce task handles many keys, so its input is a sum of key groups, and $L \ge q$. Mining of Massive Datasets (Section 2.5) defines the communication cost of an algorithm as the sum of the input sizes of all its tasks. The map input is read once in each algorithm, so the part that changes from one algorithm to another is the shuffle, and this page counts the shuffle.

The quantities trade against each other. A small $q$ means that each key fits in the memory of one machine and that the reduce work spreads over many tasks, but it often forces each input to go to more keys, so $r$ grows. The wall-clock time of a round is at least the time to read $L$ (Section 2.5.2), so a few heavy keys slow a whole round down, see [data skew](/data-skew/). The local work of map and reduce is counted too, but it is often linear in their input, and the network is the bottleneck.

In the [MRC model](/mrc-model/) of Karloff, Suri and Vassilvitskii (2010), the number of machines and the memory of each machine are sublinear in the input size, and an efficient algorithm uses a polylogarithmic number of rounds. In the massively parallel computation model of Beame, Koutris and Suciu, there are $p$ servers, and the main cost is the **load**: the largest number of tuples that one server receives in one round. The load is $L$ in the table above.

### A worked round

Three documents are cut into $M = 2$ splits: split 0 is "a rose is a rose", and split 1 is "is a rose" and "a b". The job is [word count](/word-count/): map emits (w, 1) for each word w, and reduce sums the values. There are $R = 2$ reduce tasks, and the partitioner sends "a" and "is" to task 0, and "rose" and "b" to task 1.

| | map task 0 | map task 1 | total |
|---|---|---|---|
| pairs emitted | 5 | 5 | 10 |
| messages to reduce task 0 | 3 (a, is, a) | 3 (is, a, a) | 6 |
| messages to reduce task 1 | 2 (rose, rose) | 2 (rose, b) | 4 |

Reduce task 0 gets 6 pairs (14 bytes, with one byte per character of key and value) and outputs (a, 4) and (is, 2). Reduce task 1 gets 4 pairs (17 bytes) and outputs (b, 1) and (rose, 3). The round sends 10 pairs and 31 bytes. Each input word gives one pair, so the replication rate is 1. The reducer size is $q = 4$ (the key "a"), and the largest reducer input is $L = 6$ pairs. A [combiner](/combiner/) would cut the messages from 10 to 7, because each map task would send (a, 2) once instead of (a, 1) twice.

### The simulator

The Python code of this page simulates a round. The map tasks run as one list comprehension over the splits. The shuffle is an explicit list of messages (source map task, destination reduce task, key, value), and each reduce task sorts and groups its own messages. The simulator counts the pairs and bytes sent, the input of each reduce task, and the rounds. It does not show speedup, which Python cannot show. The pages of this area ([word count](/word-count/), [inverted index](/inverted-index/), [distributed sorting](/distributed-sorting/) and the joins) use the same simulator and check their output against a computation on one machine.

## Relation to other models

- **[Work-span model](/work-span-model/).** The map phase is a [parallel map](/parallel-map/), and the shuffle plus reduce is a group-by-key, which is a sort or a hash partition. A round has span about that of a sort, so the number of rounds plays the role of the span, and the total map and reduce work plays the role of the work.
- **[BSP model](/bsp-model/).** A round is a [superstep](/superstep/) in which each machine computes locally and then sends messages. The shuffle is an [h-relation](/h-relation/) where $h$ is the largest number of pairs that one machine sends or receives. MapReduce fixes the pattern of communication (by key), while BSP lets the program address any processor. The barrier between the map and the reduce phase is a [barrier synchronization](/barrier-synchronization/).
- **[MRC model](/mrc-model/).** MRC adds explicit limits on memory per machine and on the number of machines, so that "one machine holds everything" is not allowed.
- **[PRAM model](/pram-model/).** A PRAM step can be simulated in a round, with memory cells as keys. Karloff, Suri and Vassilvitskii give such a simulation for a class of PRAM algorithms. The converse view is less useful, because a round costs much more than a PRAM step, so MapReduce algorithms aim at very few rounds.
- **Dataflow systems.** Spark keeps the same map and group-by-key operators but holds data in memory between rounds, see [resilient distributed datasets](/resilient-distributed-datasets/). Pregel adapts BSP to graphs, see [Pregel](/pregel-model/).

## Known results in the model

- **One round, no shuffle beyond the output.** [Distributed grep](/distributed-grep/) is a map-only job.
- **One round, replication rate 1.** [Word count](/word-count/), the [inverted index](/inverted-index/), grouping and aggregation, and the [reduce-side join](/reduce-side-join/) send each input once. Their largest reducer input is the size of the largest key group, so heavy keys hurt, see [data skew](/data-skew/).
- **Sorting in a constant number of rounds.** A sampling round picks split points, and a sort round with a range [partitioner](/partitioner/) sorts. With a sample of $O(R \log n)$ keys, every reduce task gets $O(n/R)$ keys with high probability, see [distributed sorting](/distributed-sorting/).
- **Multiway joins in one round.** The [Shares (HyperCube) join](/hypercube-shares-join/) of Afrati and Ullman replicates tuples on a grid of reducers. For the triangle query on three relations of size $r$ with $k$ reducers, it sends $3 r k^{1/3}$ tuples.
- **A lower bound on the replication rate.** Take $n$ inputs where every pair of inputs must meet at some reducer (the all-pairs problem, as in a similarity join). A reducer with $q_i \le q$ inputs covers at most $q_i(q_i - 1)/2$ pairs. The reducers must cover all $n(n-1)/2$ pairs, so $n(n-1)/2 \le \sum_i q_i(q_i-1)/2 \le \frac{q-1}{2}\sum_i q_i$. The replication rate is $r = \sum_i q_i / n$, so $r \ge (n-1)/(q-1)$. For $n = 1000$ and $q = 100$, the bound is $r \ge 999/99 \approx 10.09$, so the map tasks emit at least $10{,}091$ pairs. Mining of Massive Datasets (Section 2.6.6) gives this method and more bounds of this kind, for example $r \ge 2n^2/q$ for the product of two $n \times n$ matrices (Section 2.6.7). See [communication lower bounds for MapReduce](/mapreduce-communication-lower-bounds/).

### Pitfalls

- **Counting the wrong thing.** A MapReduce algorithm with few rounds can still send far more data than the input. Give the communication and the largest reducer input, not only the rounds.
- **Assuming an order of values.** The reduce function must not depend on the order of its values, unless the job uses a [secondary sort](/secondary-sort/).
- **A partitioner that differs between processes.** Python's built-in hash of a string changes from one process to the next, so a partitioner built on it sends one key to different reduce tasks from different map tasks. Use a hash that is fixed, as the simulator does with CRC-32.

## References
