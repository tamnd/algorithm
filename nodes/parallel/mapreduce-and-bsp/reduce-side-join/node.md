---
tag: 2FMSJX
kind: algorithm
slug: reduce-side-join
name: Reduce-side join
aliases:
- repartition join
- shuffle join
area: parallel/mapreduce-and-bsp
level: core
summary: Tag records from each relation in the map phase and join them by key in the reducer.
solves: [relational-join]
model: mapreduce-model
complexity:
  vars: {n: the number of input tuples |R| + |S|, k: the number of reducers, z: the number of output tuples, L: the largest reducer input, D: the largest number of output tuples of one reducer}
  time: {worst: O(n log n + z)}
  space: {extra: Θ(n)}
  depth: {worst: O(L log L + D)}
  communication: {worst: Θ(n)}
properties: {deterministic: true, in_place: false, online: false}
history:
  year: 2010
  people: [Jimmy Lin, Chris Dyer, Spyros Blanas, Jignesh M. Patel]
  note: The method is the MapReduce form of the partitioned parallel hash join of the database machines of the 1980s. Lin and Dyer (2010) and Blanas et al. (2010) described it and its variants for MapReduce.
prereqs: [mapreduce-model, relational-join, hash-join, partitioner, shuffle-phase]
see_also: [map-side-join, hypercube-shares-join, data-skew, secondary-sort, grace-hash-join, sort-merge-join, semijoin, bloom-join]
sources:
  - book: isbn:9781608453429
    title: Jimmy Lin and Chris Dyer, Data-Intensive Text Processing with MapReduce, Morgan and Claypool, 2010
    locator: Section 3.5.1, Reduce-Side Join (the one-to-one, one-to-many and many-to-many cases, and the use of a secondary sort so that the reducer buffers only one side)
  - paper: doi:10.1145/1807167.1807273
    title: Spyros Blanas, Jignesh M. Patel, Vuk Ercegovac, Jun Rao, Eugene J. Shekita and Yuanyuan Tian, A comparison of join algorithms for log processing in MapReduce, SIGMOD 2010, pages 975 to 986
    locator: the standard repartition join and the improved repartition join (tags in the key so that the reducer buffers only the records of the smaller table), and their measured costs
  - book: isbn:9781108476348
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition, Cambridge University Press, 2020
    locator: Section 2.3.7, Computing Natural Join by MapReduce
---

The reduce-side join, also called the repartition join, computes the equi-join $R(A, B) \bowtie S(B, C)$ in one MapReduce round. The map function tags each tuple with the name of its relation and emits it with the join value $b$ as the key. The [shuffle](/shuffle-phase/) brings all tuples with the same $b$ to one reducer, which outputs the cross product of the $R$ tuples and the $S$ tuples of that key. It is the [hash join](/hash-join/) of one machine, spread over a cluster: the [partitioner](/partitioner/) does the partitioning step, and each reduce call joins one partition. It works on any two inputs, with no order and no partitioning given in advance. The shuffle carries every input tuple once, and the time of the round depends on the largest key group.

## In plain words

You have two lists, for example a list of people with their city and a list of cities with their country, and you want to match the rows that have the same city. Each computer reads some rows from either list. It puts a label on each row that says which list the row came from, and it sends the row to the computer that is in charge of its city. All rows for one city now sit on one computer. That computer puts the people rows on one side and the city rows on the other, and it pairs every row on one side with every row on the other side. Each row travels once. If one city has a very large number of rows, the computer in charge of it does much more work than the others, and the whole job waits for it.

## The problem

The input is two bags of tuples, $R$ with tuples $(a, b)$ and $S$ with tuples $(b, c)$, spread over the map tasks, and a number $k$ of reducers. The output is the bag join $R \bowtie S$: the tuple $(a, b, c)$ appears $m_R(a, b) \cdot m_S(b, c)$ times, where $m_R$ and $m_S$ count the copies in $R$ and $S$. This is the equi-join case of the [relational join problem](/relational-join/). For a value $b$, let $R_b$ and $S_b$ be the tuples of $R$ and $S$ with join value $b$. Then $|R \bowtie S| = \sum_b |R_b| \cdot |S_b|$. The costs are those of the [MapReduce model](/mapreduce-model/): the rounds, the pairs sent in the shuffle, and the largest reducer input $L$.

## The algorithm

The map function sees one tuple at a time. The tag $R$ or $S$ tells the reducer which relation a value came from. The function $h$ is a hash of the key that is the same in every map task.

```pseudo id=main
REDUCE-SIDE-JOIN(R, S, k)                  ▷ R holds (a, b), S holds (b, c); join on b
L1  for each (a, b) in R do emit (b, (R, a))         ▷ map: tag each tuple
L2  for each (b, c) in S do emit (b, (S, c))
L3  shuffle: send each pair with key b to reducer h(b) mod k
L4  for each key b at a reducer, with its values V do      ▷ reduce
L5      X ← the values in V with tag R
L6      Y ← the values in V with tag S
L7      for each x in X and each y in Y do output (x, b, y)
```

The reducer above holds the whole group $V$ in memory. The improved version uses a [secondary sort](/secondary-sort/): the key is the pair $(b, \text{tag})$, the partitioner and the grouping use only $b$, and the sort puts tag $R$ before tag $S$. Then all $R$ values of a group arrive first. The reducer keeps them in $X$, and it outputs $(x, b, c)$ for all $x \in X$ as each $S$ value $c$ goes past, without storing $Y$. So only one side is held in memory, and the user puts the smaller relation on that side.

## Example

Take $R = \{(\text{ann}, 1), (\text{bob}, 2), (\text{cid}, 1), (\text{dan}, 3)\}$ and $S = \{(1, x), (2, y), (1, z), (4, w)\}$, with $k = 2$ reducers. The map phase emits 8 tagged pairs, one for each tuple. With the CRC-32 hash of the program below, keys 1, 2 and 3 go to reducer 1 and key 4 goes to reducer 0. So reducer 1 gets 7 pairs and reducer 0 gets 1.

| reducer | key $b$ | $X$ (from $R$) | $Y$ (from $S$) | output |
|---|---|---|---|---|
| 1 | 1 | ann, cid | x, z | (ann, 1, x), (ann, 1, z), (cid, 1, x), (cid, 1, z) |
| 1 | 2 | bob | y | (bob, 2, y) |
| 1 | 3 | dan | none | none |
| 0 | 4 | none | w | none |

The output has 5 tuples. The largest group, for $b = 1$, holds 4 values. With the secondary sort, the reducer holds only the 2 values of $X$ for that key.

**A skewed input.** Draw 3,000 tuples for each relation, with join values from 500 keys and a Zipf law (key $i$ has weight $1/i$), and use $k = 16$ reducers. The shuffle sends 6,000 pairs, so the average reducer input is 375. The join has 318,654 tuples. Key 1 has 433 tuples in $R$ and 433 in $S$, a group of 866 pairs that one reducer must take, and that reducer outputs $433^2 = 187{,}489$ tuples for this key alone. The largest reducer input is 1,148, about three times the average. No partitioner can do better than the size of the largest group, because a group is never split.

## Correctness

The partitioner depends only on the key, so all pairs with key $b$ go to one reducer and form one group (lines L3 and L4). The tags split the group into $X$, the $a$ values of $R_b$, and $Y$, the $c$ values of $S_b$, with their copies (lines L5 and L6). Line L7 outputs each tuple $(a, b, c)$ exactly $m_R(a, b) \cdot m_S(b, c)$ times, and every output of the call for $b$ has join value $b$. A key that occurs in only one relation gives an empty side and no output. Adding over all keys gives the bag join. With the secondary sort, all $R$ values of a group come before the first $S$ value, so each $S$ value meets all of $X$, and the output is the same. The full proof is below.

## Complexity

Let $n = |R| + |S|$ and $\text{OUT} = |R \bowtie S|$.

- **Rounds.** One.
- **Communication.** The shuffle carries exactly $n$ pairs, so the replication rate is 1. Each pair holds one tag and one attribute value besides the key.
- **Work.** The map phase is $\Theta(n)$. A shuffle that sorts takes $O(n \log n)$ comparisons in total, and line L7 takes $\Theta(\text{OUT})$. So the total work is $O(n \log n + \text{OUT})$.
- **Largest reducer input.** The reducer of $b$ gets all $|R_b| + |S_b|$ pairs of the key, so $L \ge \max\left(n/k, \; \max_b (|R_b| + |S_b|)\right)$. When every group has at most $c$ pairs, the balance bound of the [partitioner](/partitioner/) page gives $L \le (1 + \varepsilon) n/k$ with probability at least $1 - k \exp(-\varepsilon^2 n / (3kc))$.
- **Largest reducer output.** The reducer of $b$ outputs $|R_b| \cdot |S_b|$ tuples for that key. With one heavy key, this term can be most of OUT, and one reducer does it alone.
- **Memory.** A reduce call holds $|R_b| + |S_b|$ values, or only $|R_b|$ with the secondary sort.

The time of the round is the time of the slowest reducer, which is $\Omega(\max_b (|R_b| + |S_b| + |R_b| \cdot |S_b|))$. For inputs where each key occurs a few times, this is close to $(n + \text{OUT})/k$. For skewed inputs, see [data skew](/data-skew/).

## Properties

- **No assumptions on the input.** The inputs need not be sorted or partitioned in any way, which is the difference from the [map-side join](/map-side-join/).
- **Every tuple is sent.** The communication is $n$ pairs even when most tuples have no partner. A [semijoin](/semijoin/) or a [Bloom join](/bloom-join/) filter can remove tuples with no partner before the shuffle.
- **One join attribute.** All relations in the round must be keyed on the same attribute. A join of three relations on different attributes needs a second round or the [Shares join](/hypercube-shares-join/).
- **Deterministic.** For a fixed hash function, the assignment of keys to reducers is fixed, so the same input always gives the same loads.

## Variants and improvements

- **One-to-one, one-to-many and many-to-many.** Lin and Dyer (Section 3.5.1) treat these three cases. When $b$ is a key of $R$, each group has at most one $R$ value, and with the secondary sort the reducer holds one tuple and streams the $S$ tuples.
- **Improved repartition join.** Blanas et al. put the tag in the key so that the reducer buffers only the records of the smaller table, as described above. They also study the broadcast join and semijoin filters.
- **Outer joins.** For a left outer join, a reduce call with an empty $Y$ outputs $(x, b, \text{null})$ for each $x \in X$. A full outer join does the same for both sides.
- **Several relations on one attribute.** $R_1(A_1, B), \ldots, R_m(A_m, B)$ join in one round in the same way: the reducer of $b$ outputs the product of the $m$ lists.
- **Skewed keys.** A heavy key can be split over several reducers: the tuples of one side are spread at random and the tuples of the other side are copied to all of them. See [data skew](/data-skew/) and the grid of Beame, Koutris and Suciu.
- **Single machine.** On one machine, the same idea is the [Grace hash join](/grace-hash-join/), which partitions both inputs to disk by a hash of the key and then joins each pair of partitions.

## When to use it

Use the reduce-side join when both relations are large, they are not sorted or partitioned on the join key, and no key is very frequent. If one relation fits in the memory of every mapper, the broadcast form of the [map-side join](/map-side-join/) avoids the shuffle of the large relation. If both inputs are already sorted and partitioned the same way on the key, the merge form of the map-side join avoids the shuffle completely. If some keys are very frequent, use a skew-aware method.

## Pitfalls

- **Relying on the order of values.** Without a secondary sort, the values of a group arrive in no fixed order, so the reducer must hold both sides before it can output anything. A reducer that assumes the $R$ values come first gives wrong results.
- **Large groups.** The reducer of a heavy key may run out of memory, and its output alone can be most of the join. Null or empty join values are a common source of one huge group. Remove them in the map function when the join does not match them.
- **A hash that changes between processes.** The partitioner must give the same reducer for the same key in every map task. The built-in string hash of some languages, Python among them, is salted per process.
- **Putting the large relation on the buffered side.** With the secondary sort, the relation whose tag sorts first is the one held in memory. Put the smaller relation there.
- **Counting only the input.** The output can be much larger than $n$, and writing it is often the main cost.

## Implementations

## History

The parallel database machines of the 1980s, such as Grace and Gamma, joined two relations by hash partitioning both of them on the join key and joining each partition on its own node. The reduce-side join is this method in MapReduce, with the shuffle in place of the network partitioning. Lin and Dyer (2010) described the reduce-side join with the one-to-one, one-to-many and many-to-many cases and the secondary sort. In the same year, Blanas, Patel, Ercegovac, Rao, Shekita and Tian compared the standard and the improved repartition join with the broadcast join and semijoin methods on Hadoop, for the join of a log with a reference table.

## References
