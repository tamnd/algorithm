---
tag: JAW8XW
kind: technique
slug: exchange-operator
name: Exchange operator
aliases:
- Volcano exchange
- Graefe exchange operator
area: databases/query-processing
level: core
summary: An operator that splits a plan into parallel streams by partitioning, broadcasting or merging tuples, so other operators stay serial.
prereqs: [iterator-model, pipelining-and-materialization, hash-partitioning]
see_also: [parallel-hash-join, range-partitioning, data-skew, shared-nothing-architecture, morsel-driven-parallelism, combiner, k-way-merge, amdahls-law]
sources:
  - paper: doi:10.1145/93597.98720
    title: Goetz Graefe, Encapsulation of parallelism in the Volcano query processing system, Proceedings of ACM SIGMOD 1990, 102 to 111
    locator: the exchange operator
  - paper: doi:10.1109/69.273032
    title: Goetz Graefe, Volcano, an extensible and parallel query evaluation system, IEEE Transactions on Knowledge and Data Engineering 6(1), 120 to 135 (1994)
    locator: the exchange operator and its use for parallel query evaluation
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 73 to 169 (1993)
    locator: the section on parallel query execution
  - paper: doi:10.1145/129888.129894
    title: David DeWitt and Jim Gray, Parallel database systems, the future of high performance database systems, Communications of the ACM 35(6), 85 to 98 (1992)
    locator: pipelined and partitioned parallelism, and the split and merge of data streams
---

The exchange operator puts parallelism into a [query plan](/query-plan/) as one more operator. Below it, several copies of a subplan run in their own processes or threads; above it, one or more consumers read the tuples. In between, exchange moves each tuple to a consumer by a rule: a hash of a key, a key range, round robin, a copy to all, or a merge that keeps a sort order. To its parent and to its child it offers the same open, next and close calls as any operator of the [iterator model](/iterator-model/), so scans, joins and aggregations stay serial code and need no change for parallel execution. Graefe introduced it in the Volcano system in 1990.

## In plain words

A post office sorts letters by city. You do not teach every clerk how to work in a team. You give each clerk a pile and the same old job, and you put a row of bins between the clerks and the delivery workers, one bin per worker. A clerk drops each letter into the bin of the worker for its city. Each delivery worker takes letters only from his bin and does his old job. The bins are the exchange. Because the city decides the bin, all letters for one city meet in the same place, even though many clerks worked on them.

## When it applies

- A plan must run on several cores or several machines, and the operators are written for one thread, as in Volcano-style engines.
- The work can be split by data: rows that must meet, such as the rows of one join key or one group, can be sent to the same consumer by a function of the row.
- A pipeline should run in two processes at the same time, the producer and the consumer, with a buffer between them.
- The degree of parallelism can be chosen when the plan is built. If it must change while the query runs, see [morsel-driven parallelism](/morsel-driven-parallelism/).

## The template

An exchange has $n$ producers below and $m$ consumers above. Each producer runs its own copy of the child subplan, and each consumer $j$ reads from its own queue $Q[j]$. The rule ROUTE is the hole.

```pseudo id=main
OPEN(x)                                    ▷ x is an exchange with n producers and m consumers
L1  create the queues Q[0 .. m - 1]
L2  start n workers; worker w runs PRODUCE(x, w)
NEXT(x, j)                                 ▷ called by consumer j
L3  while Q[j] is empty and some producer has not ended do wait
L4  if Q[j] is empty then return EOF
L5  return the next tuple from Q[j]
PRODUCE(x, w)
L6  OPEN(child of x, copy w)
L7  while (t ← NEXT(child of x, copy w)) ≠ EOF do
L8      for each j in ROUTE(t) do add t to the packet for Q[j]    ▷ hole: hash, range, round robin or all
L9      send each full packet; wait while its queue holds too many packets    ▷ flow control
L10 send the last packets, CLOSE(child of x, copy w), and mark worker w as ended
```

Tuples move in packets of many tuples, so the cost of the queue and of the wake-up of a consumer is paid once per packet. Flow control stops a fast producer from filling the memory when its consumer is slow. A merging exchange uses one queue per producer at each consumer and returns the smallest head with a [k-way merge](/k-way-merge/), so sorted producer streams give a sorted consumer stream.

The rules for ROUTE:

- **Hash** on a key $k$: $\text{ROUTE}(t) = \{h(t.k) \bmod m\}$, for joins and aggregations on $k$. See [hash partitioning](/hash-partitioning/).
- **Range** on $k$: consumer $j$ gets the keys in the $j$-th range, for sorting. See [range partitioning](/range-partitioning/).
- **Round robin**: the tuples go to the consumers in turn, which gives equal counts when no key matters.
- **Broadcast**: $\text{ROUTE}(t) = \{0, \ldots, m - 1\}$, for a small input that every consumer needs.
- **Gather**: $m = 1$, to bring parallel streams back to one consumer, for example at the root of the plan.

**Why a hash exchange is correct for an equijoin.** Exchange both inputs of $R \bowtie_{R.k = S.k} S$ by the same $h$ on $k$. If $r.k = s.k$, then $h(r.k) = h(s.k)$, so $r$ and $s$ reach the same consumer, and the serial join there finds the pair. Each tuple goes to exactly one consumer, so no pair is found twice. The union of the $m$ local joins is therefore the full join. The same argument holds for grouping on $k$: all rows of a group meet at one consumer. A null key never matches in a join, so its consumer does not matter, but for grouping all nulls must go to the same consumer, which a hash of the null value does.

## Classic examples

- **Parallel hash join.** Hash exchanges on both inputs, then $m$ serial hash joins, one per consumer. This is the plan of a [parallel hash join](/parallel-hash-join/) on a [shared-nothing](/shared-nothing-architecture/) system, where the exchange sends tuples over the network.
- **Broadcast join.** If $S$ is small, broadcast $S$ to all consumers and leave $R$ where it is. With $m = 4$ and $|S| = 1000$, the exchange moves 4000 tuples of $S$ and none of $R$. A hash exchange of both inputs moves about $(1 - 1/m)$ of each input when the data starts spread evenly. Broadcast is better when $m |S|$ is smaller than the part of $R$ that would move.
- **Two-phase aggregation.** Each producer aggregates its own rows, a hash exchange on the grouping key sends the partial states, and each consumer merges them. With $n$ producers and $d$ groups, at most $n d$ partial states cross the exchange, in place of all the rows. This is the [combiner](/combiner/) of MapReduce.
- **Parallel sort.** A range exchange on the sort key, then a local sort at each consumer. The outputs of the consumers, taken in range order, are the sorted result. The other way is a local sort at each producer and a merging exchange.
- **Pipelined parallelism.** An exchange with $n = m = 1$ only puts a queue between two parts of a pipeline, so that they run on two cores at the same time.

## Variations

- **Kinds of parallelism.** A hash or range exchange gives partitioned parallelism inside one operator. An exchange with one producer and one consumer gives pipelined parallelism between operators. Two subtrees under separate exchanges can run at the same time, which gives parallelism between independent parts of a bushy plan.
- **Inside one machine and across machines.** In one machine the queues are in shared memory. Across machines the same operator sends packets over the network; many distributed engines call the same operator a shuffle.
- **Repartition only when needed.** If an input is already partitioned on the key, for example a table stored by [hash partitioning](/hash-partitioning/) on the join key, the optimizer leaves out the exchange. Partitioning is a property of a stream, like a sort order.
- **Fixed against elastic parallelism.** The classic exchange fixes $n$ and $m$ in the plan. Morsel-driven engines let threads take small pieces of input at run time, which balances the load and lets the number of threads change during the query.

## Pitfalls

- **Skew.** A hash exchange sends all rows of one key to one consumer. If one key has a large share of the rows, that consumer does most of the work, and the query runs at its speed. See [data skew](/data-skew/). Splitting hot keys or broadcasting their partners helps.
- **Memory of the queues.** With $n$ producers and $m$ consumers there are $n m$ streams, and each needs packet buffers. On many cores or many machines this grows fast.
- **Deadlock with merging and flow control.** A merging consumer must wait for a packet from one given producer. If that producer is blocked because the queue of another consumer is full, and that consumer waits for this one, no one moves. Larger buffers or spooling to disk break the cycle.
- **Order is lost.** A hash or round robin exchange mixes the streams, so an order from below is lost unless the exchange merges.
- **Startup cost.** Starting processes and queues costs time. For a small input a serial plan is faster, and [Amdahl's law](/amdahls-law/) limits the gain when part of the plan stays serial, for example a gather at the root.

## Exercises

1. Write ROUTE for a range exchange with split points $s_1 < \cdots < s_{m-1}$, and show that the outputs of the local sorts, taken in range order, form one sorted list.
2. In the broadcast join example, find the size of $R$ above which a broadcast of $S$ to $m$ consumers moves fewer tuples than a hash exchange of both inputs, if both inputs start evenly spread over the $m$ machines.
3. A query computes $\gamma_{g;\,\text{AVG}(v)}(R)$ with an exchange between a local and a global aggregation. Which state must cross the exchange, and why is sending the local averages wrong?
4. Give a plan with two merging exchanges and bounded queues that can deadlock, and say how spooling one input to disk removes the deadlock.

## References
