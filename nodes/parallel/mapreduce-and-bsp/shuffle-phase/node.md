---
tag: 2C13E0
kind: concept
slug: shuffle-phase
name: Shuffle phase
aliases:
- shuffle and sort
- grouping by key
area: parallel/mapreduce-and-bsp
level: intro
summary: The step that routes all pairs with the same key to the same reducer, sorting them on the way.
prereqs: [mapreduce-model, external-merge-sort]
see_also: [partitioner, combiner, data-skew, k-way-merge, hash-partitioning, h-relation, scatter-and-gather, secondary-sort]
sources:
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, 6th Symposium on Operating Systems Design and Implementation (OSDI), 2004"
    locator: Section 3.1 (execution overview, steps 4 and 5) and Section 4.2 (ordering guarantees)
  - book: isbn:9781491901632
    title: Tom White, Hadoop, The Definitive Guide, fourth edition, O'Reilly, 2015
    locator: Chapter 7 (How MapReduce Works), the part on shuffle and sort (map side, reduce side, and configuration tuning)
  - book: isbn:9781108476348
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition, Cambridge University Press, 2020
    locator: Section 2.2.2 (Grouping by Key) and Section 2.5 (The Communication-Cost Model)
  - book: isbn:9781608453429
    title: Jimmy Lin and Chris Dyer, Data-Intensive Text Processing with MapReduce, Morgan and Claypool, 2010
    locator: Section 2.2 (the shuffle and sort between map and reduce) and Section 2.4 (partitioners and combiners)
---

The shuffle phase is the part of a [MapReduce](/mapreduce-model/) round between the map calls and the reduce calls. It moves every intermediate pair to the reduce task that owns its key and sorts each reduce task's input by key, so that the values of one key arrive together. It is the only step of a round in which machines exchange data, so the communication cost of a MapReduce algorithm is the cost of its shuffles.

## In plain words

After the map step, every computer holds a pile of notes, each with a key on it. The reduce step needs all notes with the same key in one place. The shuffle does this. Each computer sorts its notes into one bin for each receiving computer, and inside each bin it puts the notes in key order. Then every receiving computer collects its bin from every sending computer, and merges the sorted bins into one sorted list. Equal keys are now next to each other, and the reduce step reads them in one pass. The cost is the amount of data that crosses the network and, above all, the amount that the busiest receiving computer must take in.

## The idea

Let there be $M$ map tasks and $R$ reduce tasks, and let $P$ be the set of intermediate pairs after any [combiner](/combiner/). A [partitioner](/partitioner/) $\pi : K \to \{0, \dots, R-1\}$ gives each key an owner. The shuffle delivers each pair $(k, v) \in P$ from the map task that made it to reduce task $\pi(k)$, and each reduce task groups its pairs by key. The order of the values of one key is not fixed, unless the job uses a [secondary sort](/secondary-sort/).

### The map side

In Dean and Ghemawat's description (Section 3.1, step 4), each map task buffers its output in memory and from time to time writes it to its local disk, cut into $R$ regions by the partitioner. Hadoop (White, Chapter 7) refines this into the following steps.

1. **Buffer.** The map task writes each output pair to a circular buffer in memory, together with its partition number $\pi(k)$.
2. **Sort and spill.** When the buffer is nearly full, a background thread sorts its contents by (partition, key) and writes them to disk as one spill file. If there is a combiner, it runs on each partition of the sorted spill before the write.
3. **Merge.** When the map task ends, it merges its spill files into one file, sorted by (partition, key), with an index of where each of the $R$ partitions starts. This is a [k-way merge](/k-way-merge/) of sorted runs. The combiner can run again on the merged output.

### The copy and the reduce side

4. **Copy.** Reduce task $j$ fetches partition $j$ from the output of each of the $M$ map tasks, as soon as each map task ends. There are $M \cdot R$ such transfers in a round.
5. **Merge.** Each fetched partition is already sorted, so the reduce task holds $M$ sorted runs. It merges them, in memory when they fit and else as an [external merge sort](/external-merge-sort/). In Dean and Ghemawat's description the reduce task instead sorts all of its data after the copy (Section 3.1, step 5). Both give the same grouped input.
6. **Reduce.** The reduce task scans the merged run once and calls reduce on each group of equal keys, in increasing key order. Dean and Ghemawat (Section 4.2) guarantee this order within a partition.

### The cost

Let $s(k, v)$ be the size of a pair in bytes. The shuffle has these costs, which are the ones the [MapReduce model](/mapreduce-model/) counts.

- **Total communication.** $B = \sum_{(k, v) \in P} s(k, v)$ bytes, or $|P|$ pairs. A combiner lowers $B$, and the partitioner does not change it.
- **Largest reducer input.** $L = \max_j \sum_{(k, v) \in P,\ \pi(k) = j} s(k, v)$. The partitioner and the key frequencies decide $L$. A reduce task cannot start its reduce calls before its whole input has arrived, so $L$ bounds the round from below: if a machine receives at most $\beta$ bytes per second, the copy takes at least $L/\beta$ seconds, however many machines there are. Since the $R$ inputs add up to $B$, $L \ge B/R$, with equality only for a perfectly even split. See [data skew](/data-skew/).
- **Local sorting work.** A map task with $n_i$ output pairs sorts them in $O(n_i \log n_i)$ comparisons. A reduce task with $L_j$ pairs in $M$ runs merges them with a heap in $O(L_j \log M)$ comparisons, see [k-way merge](/k-way-merge/).

In [BSP](/bsp-model/) terms, the copy is an [h-relation](/h-relation/) with $h = \max(\max_i \text{out}_i, \max_j \text{in}_j)$, the largest number of words that one machine sends or receives. It is an all-to-all exchange, the general case of [scatter and gather](/scatter-and-gather/).

## Examples

**The transfer matrix of word count.** Take the [word count](/word-count/) job on the documents "a rose is a rose" (split 0) and "is a rose", "a b" (split 1), with $R = 2$, no combiner, and a partitioner that sends "a" and "is" to reduce task 0 and "rose" and "b" to reduce task 1. A pair (w, 1) has $|w| + 1$ bytes.

| | to reduce task 0 | to reduce task 1 | sent |
|---|---|---|---|
| map task 0 | (a,1), (is,1), (a,1): 7 bytes | (rose,1), (rose,1): 10 bytes | 17 bytes |
| map task 1 | (is,1), (a,1), (a,1): 7 bytes | (rose,1), (b,1): 7 bytes | 14 bytes |
| received | 14 bytes | 17 bytes | $B = 31$ bytes |

So $B = 31$ and $L = 17$, while $B/R = 15.5$. Reduce task 0 merges the sorted runs (a, a, is) and (a, a, is) into a, a, a, a, is, is, and calls reduce twice. Reduce task 1 merges (rose, rose) and (b, rose) into b, rose, rose, rose.

**Spills on the map side.** Let map task 0 have a buffer of 3 pairs. Its output a, rose, is, a, rose gives two spills. The first spill holds a, rose, is, and sorted by (partition, key) it is (0, a), (0, is), (1, rose). The second spill holds a, rose, sorted as (0, a), (1, rose). The final merge gives partition 0 as a, a, is and partition 1 as rose, rose, the same runs as in the table. With a combiner that adds the counts, the first spill would send (a, 1), (is, 1), (rose, 1), and a second combiner pass on the merge would join the two spills into (a, 2), (is, 1), (rose, 2).

**A heavy key.** If one key carries 30% of the pairs, its reduce task receives at least $0.3\,B$ bytes, so with $R = 100$ the largest input is at least 30 times the average $B/100$, and adding reduce tasks does not help. A combiner or a change of key is the fix, see [data skew](/data-skew/).

## Where it is used

- Every MapReduce round that has a reduce phase: [word count](/word-count/), the [inverted index](/inverted-index/), [distributed sorting](/distributed-sorting/) and the [reduce-side join](/reduce-side-join/). A map-only job such as [distributed grep](/distributed-grep/) has no shuffle.
- The sort inside the shuffle is what a [secondary sort](/secondary-sort/) uses to deliver values in a chosen order, and what [distributed sorting](/distributed-sorting/) uses with a range [partitioner](/partitioner/) to sort the whole input.
- The [map-side join](/map-side-join/) avoids the shuffle of the large input by broadcasting the small one or by joining inputs that are already partitioned the same way.
- The group-by-key and repartition steps of dataflow systems such as Spark ([resilient distributed datasets](/resilient-distributed-datasets/)) and of parallel databases ([hash partitioning](/hash-partitioning/) in a [grace hash join](/grace-hash-join/)) do the same work.

## References
