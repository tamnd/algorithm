---
tag: MES4WN
kind: algorithm
slug: map-side-join
name: Map-side join
aliases:
- broadcast join
- replicated join
- fragment-replicate join
- merge join of co-partitioned inputs
area: parallel/mapreduce-and-bsp
level: core
summary: Replicate a small relation to every mapper and join locally, avoiding the shuffle for that side.
solves: [relational-join]
model: mapreduce-model
complexity:
  vars: {r: the number of tuples of the large relation R, s: the number of tuples of the small relation S, M: the number of map tasks, z: the number of output tuples, D: the largest number of output tuples of one map task}
  time: {expected: O(r + M s + z)}
  space: {extra: Θ(M s)}
  depth: {expected: O(r/M + s + D)}
  communication: {worst: Θ(M s)}
properties: {deterministic: true, in_place: false, online: true}
history:
  year: 2010
  people: [Jimmy Lin, Chris Dyer, Spyros Blanas, Jignesh M. Patel]
  note: Copying a small relation to every site of a large one is an old method of distributed databases. Lin and Dyer (2010) and Blanas et al. (2010) described the broadcast join and the merge join of co-partitioned inputs for MapReduce.
prereqs: [mapreduce-model, relational-join, hash-join, sort-merge-join]
see_also: [reduce-side-join, hypercube-shares-join, data-skew, partitioner, semijoin, bloom-join, scatter-and-gather, external-merge-sort]
sources:
  - book: isbn:9781608453429
    title: Jimmy Lin and Chris Dyer, Data-Intensive Text Processing with MapReduce, Morgan and Claypool, 2010
    locator: Section 3.5.2, Map-Side Join (the merge of inputs that are partitioned and sorted the same way) and Section 3.5.3, Memory-Backed Join (the small relation in memory in every mapper)
  - paper: doi:10.1145/1807167.1807273
    title: Spyros Blanas, Jignesh M. Patel, Vuk Ercegovac, Jun Rao, Eugene J. Shekita and Yuanyuan Tian, A comparison of join algorithms for log processing in MapReduce, SIGMOD 2010, pages 975 to 986
    locator: the broadcast join, the directed join of pre-partitioned inputs, and their comparison with the repartition join
  - book: isbn:9781491901632
    title: Tom White, Hadoop, The Definitive Guide, fourth edition, O'Reilly, 2015
    locator: Chapter 9, MapReduce Features (the sections on joins and on side data distribution with the distributed cache)
---

A map-side join computes the equi-join $R(A, B) \bowtie S(B, C)$ inside the map tasks, with no [shuffle](/shuffle-phase/). There are two forms. The *broadcast join* copies the small relation $S$ to every map task, and each task joins its split of the large relation $R$ with a hash table of $S$. The *merge join* needs inputs that an earlier job left partitioned and sorted the same way on the join value: map task $i$ then merges part $i$ of $R$ with part $i$ of $S$, like a [sort-merge join](/sort-merge-join/). Each form saves the shuffle of the [reduce-side join](/reduce-side-join/), but only under a condition: the broadcast join needs a relation small enough to fit in the memory of each task, and the merge join needs the right partitioning.

## In plain words

Suppose you must match a huge list of sales against a short list of shops. Instead of moving the sales around, give every computer its own copy of the short list of shops. Each computer reads its share of the sales and looks up each shop in its copy. Nothing big moves over the network, only the copies of the short list.

There is a second trick for two big lists. If both lists were already cut into pieces in the same way, so that piece 3 of one list and piece 3 of the other list hold the same shops, and each piece is in order of shop, then each computer takes the two pieces with the same number and walks down both in order, like zipping two sorted lists together. Again nothing moves.

## The problem

The input is two bags of tuples, $R$ with tuples $(a, b)$ and $S$ with tuples $(b, c)$, and the output is the bag join $R \bowtie S$, in which $(a, b, c)$ appears $m_R(a, b) \cdot m_S(b, c)$ times. This is the equi-join case of the [relational join problem](/relational-join/). Let $r = |R|$, $s = |S|$ and $z = |R \bowtie S|$. For the broadcast join, $R$ is cut into $M$ splits $R_1, \ldots, R_M$, one for each map task, and $s$ tuples fit in the memory of a task. For the merge join, $R$ and $S$ are *co-partitioned*: both have $k$ parts, each part is sorted by the join value, and each join value occurs in at most one part index. The costs are those of the [MapReduce model](/mapreduce-model/): the rounds, the data sent over the network, and the largest task input.

## The algorithm

```pseudo id=main
BROADCAST-JOIN(R_1, ..., R_M, S)           ▷ R is cut into M splits; S is small
L1  copy S to every map task                     ▷ for example by the distributed cache
L2  for each map task i, in parallel do
L3      T ← a hash table of S on b
L4      for each (a, b) in R_i do
L5          for each c in T[b] do output (a, b, c)

MERGE-JOIN(R_i, S_i)                       ▷ part i of each input, both sorted by b
L6  p ← 0, q ← 0
L7  while p < |R_i| and q < |S_i| do
L8      if R_i[p].b < S_i[q].b then p ← p + 1
L9      else if R_i[p].b > S_i[q].b then q ← q + 1
L10     else
L11         find the ends p′ and q′ of the runs of the value R_i[p].b in R_i and in S_i
L12         output each (a, b, c) with (a, b) in R_i[p .. p′ − 1] and (b, c) in S_i[q .. q′ − 1]
L13         p ← p′, q ← q′
```

The merge join runs MERGE-JOIN once for each part index $i$, in map task $i$. In Hadoop, the input format reads part $i$ of each input in the same map task. Both joins are map-only jobs: the map output is the join, and there is no reduce phase.

## Example

Take $R = \{(\text{ann}, 1), (\text{bob}, 2), (\text{cid}, 1), (\text{dan}, 3)\}$ and $S = \{(1, x), (2, y), (1, z), (4, w)\}$.

**Broadcast.** Cut $R$ into $M = 2$ splits, $\{(\text{ann}, 1), (\text{bob}, 2)\}$ and $\{(\text{cid}, 1), (\text{dan}, 3)\}$. Each task gets the 4 tuples of $S$, so 8 tuples are copied, and builds $T[1] = [x, z]$, $T[2] = [y]$, $T[4] = [w]$. Task 1 outputs (ann, 1, x), (ann, 1, z) and (bob, 2, y). Task 2 outputs (cid, 1, x) and (cid, 1, z), and dan finds no entry for 3. The output has 5 tuples.

**Merge.** Suppose an earlier job with 2 reducers and the CRC-32 partitioner wrote both inputs. Part 0 holds the keys with hash 0, here only key 4, and part 1 holds keys 1, 2 and 3. So $R_0$ is empty, $S_0 = [(4, w)]$, $R_1 = [(\text{ann}, 1), (\text{cid}, 1), (\text{bob}, 2), (\text{dan}, 3)]$ and $S_1 = [(1, x), (1, z), (2, y)]$. Task 0 does nothing. Task 1 finds the run of 1 in both lists and outputs the 4 tuples of the product, then the runs of 2 give (bob, 2, y). Now $S_1$ is used up, so the loop stops before (dan, 3). The output is the same 5 tuples, and no tuple moved.

**A skewed large relation.** Let $R$ have 30,000 tuples with join values from 500 keys under a Zipf law (key $i$ has weight $1/i$), and let $S$ hold one tuple for each key, so $s = 500$. With $M = 10$ map tasks, the broadcast join copies $10 \times 500 = 5{,}000$ tuples and each task reads $3{,}000 + 500 = 3{,}500$ tuples. The reduce-side join with 10 reducers shuffles 30,500 pairs instead, and its largest reducer input is 5,872, because key 1 alone has 4,450 tuples in $R$ and all of them go to one reducer. The broadcast join cuts $R$ by position, not by key, so a heavy key does not make one task slower.

## Correctness

**Broadcast.** Each tuple $(a, b)$ of $R$ is in exactly one split, and that task has all of $S$. Its table holds every tuple of $S$ with join value $b$, with its copies, so the task outputs each matching tuple of $S$ with $(a, b)$ exactly once. No other task sees $(a, b)$.

**Merge.** Inside one part, the loop keeps an invariant at line L7: every matching pair is either *done* (both tuples before $p$ and $q$, and output once) or *open* (both tuples at or after $p$ and $q$, and not yet output). A step of line L8 or L9 skips a tuple that has no partner, and a step of lines L11 to L13 outputs the product of the two runs of one value, which are exactly the open pairs of that value. When the loop stops, one list is used up, so no pair is open. Over all parts, the co-partition condition puts both tuples of every matching pair in parts with the same index. The full proof is below.

## Complexity

**Broadcast join.**

- **Rounds.** One map-only round, with no shuffle.
- **Communication.** $M s$ tuples, one copy of $S$ for each task. In Hadoop, the distributed cache copies a file once to each machine, so the factor is the number of machines that run tasks, which can be smaller than $M$.
- **Memory.** $\Theta(s)$ in each task for the hash table.
- **Time.** Task $i$ does $O(s + |R_i| + z_i)$ expected work, where $z_i$ is its output. The total is $O(M s + r + z)$ expected.
- **Balance.** The splits of $R$ are cut by size, so each task reads about $r/M + s$ tuples whatever the keys are.

Compared with the [reduce-side join](/reduce-side-join/), which shuffles $r + s$ pairs, the broadcast join sends less data when $M s < r + s$, that is, when $s < r / (M - 1)$.

**Merge join.**

- **Rounds.** One map-only round, with no shuffle and no copies.
- **Communication.** None, if the inputs are already co-partitioned. If not, making them so costs a full shuffle of both inputs, which is the reduce-side join plus a sort.
- **Memory.** One run of one join value at a time, $O(\max_b |S_b|)$ when the runs of $S$ are buffered and those of $R$ stream.
- **Time.** Task $i$ does $O(|R_i| + |S_i| + z_i)$ work, $O(r + s + z)$ in total.
- **Balance.** The part sizes come from the earlier job. A heavy key in that job gives a large part here as well.

## Properties

- **Map-only.** Neither form has a reduce phase, so neither has the sort and the network transfer of the shuffle.
- **Asymmetric (broadcast).** One input must be small. Which input is the small one matters, unlike in the reduce-side join.
- **Robust to skew in the large relation (broadcast).** A heavy key of $R$ is spread over all tasks, because the splits ignore the key.
- **Needs a prepared layout (merge).** The two inputs must have the same number of parts, the same partitioner on the join value and sorted parts. Two outputs of jobs with the same reducers and the same partitioner have this layout.
- **Streaming (broadcast).** Each task reads its split of $R$ once, in order, and outputs as it goes.

## Variants and improvements

- **Inner and left outer joins (broadcast).** For a left outer join of $R$ with $S$, a tuple $(a, b)$ with no entry $T[b]$ outputs $(a, b, \text{null})$. A right or full outer join is harder, because no single task knows that a tuple of $S$ has no partner in any split of $R$. That needs a second step.
- **Semijoin before the broadcast.** If $S$ is too large to copy but only a few of its keys occur in $R$, first collect the distinct keys of $R$, keep only the tuples of $S$ with those keys, and broadcast the result. Blanas et al. study this as the semijoin and the per-split semijoin. A [Bloom join](/bloom-join/) sends a Bloom filter of the keys instead. See [semijoin](/semijoin/).
- **Directed join.** If only $R$ is partitioned on the join value, and $S$ is partitioned the same way, task $i$ can load part $i$ of $S$ into a hash table and probe it with part $i$ of $R$. Blanas et al. call this the directed join.
- **Bucketed tables.** Data systems such as Hive store tables in buckets by a hash of a column, sorted inside each bucket, so that a later join on that column can run as a merge join.
- **Several small relations.** A star join of a large fact table with several small dimension tables can copy all the small tables and join in one map pass.
- **Single machine.** The broadcast join is a [hash join](/hash-join/) with the build side copied. The merge join is the merge step of a [sort-merge join](/sort-merge-join/), and producing the sorted parts is an [external merge sort](/external-merge-sort/) in the earlier job.

## When to use it

Use the broadcast join when one relation fits in the memory of a task, and $M$ times its size is less than the size of the large relation. It is the best choice when the large relation has heavy keys, because it does not group by key. Use the merge join when both inputs already come from jobs with the same number of reducers and the same partitioner on the join value, for example in a pipeline where the same key is used again and again. When neither condition holds, use the [reduce-side join](/reduce-side-join/). For joins of three or more relations on different attributes, see the [Shares join](/hypercube-shares-join/).

## Pitfalls

- **A small side that is not small.** If the copy of $S$ does not fit in the memory of a task, the task fails or swaps. Sizes after a filter can be much larger than the estimate.
- **Paying the copies for each task.** The communication grows with $M$. With thousands of map tasks, a relation of moderate size costs more to copy than to shuffle.
- **A layout that only looks right (merge).** Two inputs with the same number of parts but different partitioners, or with a different key type such as an integer key in one and a string key in the other, put matching tuples in different parts. The join then loses tuples with no error. Check the layout first.
- **Duplicate join values on both sides (merge).** A merge that moves one pointer at a time on equal values misses pairs when a value repeats in both inputs. It must output the product of the two runs, as lines L11 to L13 do.
- **Outer joins on the copied side.** A right outer join cannot be done in the map tasks of a broadcast join alone.

## Implementations

## History

Copying a small relation to every site that holds a fragment of a large relation is an old method of distributed database systems, under the name fragment and replicate. For MapReduce, Lin and Dyer (2010) described the map-side merge join of inputs partitioned and sorted the same way, and the memory-backed join in which every mapper holds the small relation. In the same year, Blanas, Patel, Ercegovac, Rao, Shekita and Tian measured the broadcast join, the directed join and the semijoin variants on Hadoop against the repartition join, for the join of a large log with a reference table. Hadoop has a distributed cache for the copies and an input format for the merge of sorted parts, and Pig offers both as the replicated join and the merge join.

## References
