---
tag: 95KA9B
kind: concept
slug: data-skew
name: Data skew
aliases:
- hot keys
- key skew
- reducer load imbalance
area: parallel/mapreduce-and-bsp
level: core
summary: Uneven key frequencies that overload a few reducers and stretch the job's makespan.
prereqs: [mapreduce-model, partitioner, shuffle-phase]
see_also: [partitioner, combiner, reduce-side-join, hypercube-shares-join, load-skew, list-scheduling, frequent-items-problem, speculative-execution]
sources:
  - paper: doi:10.1145/2594538.2594558
    title: Paul Beame, Paraschos Koutris and Dan Suciu, Skew in parallel query processing, PODS 2014
    locator: Section 4.1 (the join of two relations with heavy hitters, the threshold m_j/p, the grid of p_h servers for a value heavy in both relations, and the load O(L ln p)) and Theorem 1.1
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, 6th Symposium on Operating Systems Design and Implementation (OSDI), 2004"
    locator: Section 3.6 (stragglers and backup tasks) and Section 4.3 (the combiner, with the remark that word frequencies follow a Zipf distribution)
  - paper: doi:10.1145/1963405.1963491
    title: Siddharth Suri and Sergei Vassilvitskii, Counting triangles and the curse of the last reducer, WWW 2011
    locator: the introduction (the last reducer of a skewed graph decides the running time) and the partition algorithm
  - paper: doi:10.1137/0117039
    title: R. L. Graham, Bounds on multiprocessing timing anomalies, SIAM Journal on Applied Mathematics 17(2), 1969
    locator: the bound 4/3 minus 1/(3m) for the longest processing time first rule
---

Data skew is the uneven spread of work over the reducers of a [MapReduce](/mapreduce-model/) job, caused mostly by keys that occur far more often than others. All pairs with one key go to one reducer, so a key with a large share of the pairs makes that reducer slow, and the round ends only when the slowest reducer ends. No [partitioner](/partitioner/) that keeps a key whole can give a reducer less than the count of the most frequent key. The fixes either shrink the heavy keys before the [shuffle](/shuffle-phase/), with a [combiner](/combiner/), or split them over several reducers, by salting the key, by a skew-aware partitioner, or, for joins, by the heavy hitter method of Beame, Koutris and Suciu (2014).

## In plain words

Picture a post office where each clerk handles the letters for some streets. If one street gets half of all the mail, its clerk works long after the others have gone home, and the post office closes only when that clerk is done. More clerks do not help, because the letters of one street all go to one clerk.

There are a few ways out. If the job is only to count the letters, each mail carrier can count their own letters for that street first, and hand over one note instead of a bag. If the work must be done letter by letter, cut the busy street into parts, give each part to a different clerk, and add up the results at the end. A careful manager can also look at the amount of mail first, and give the busy streets to clerks who have little else to do.

## The idea

**The load and the bound.** Let key $k$ have $c(k)$ pairs, $N = \sum_k c(k)$, and let $c_{\max}$ be the largest count. With $R$ reducers, reducer $j$ gets $L_j = \sum_{k \to j} c(k)$ pairs, and the largest reducer input is $L = \max_j L_j$. If keys are not split, then

$$L \ge \max\left(\frac{N}{R}, \; c_{\max}\right).$$

The first term is the average, and the second holds because one reducer gets all of the largest key. The time of the reduce phase is the time of the slowest reducer, so it is at least proportional to $c_{\max}$, whatever $R$ is. The speedup of the reduce phase over one reducer is at most $N / c_{\max}$.

**Heavy keys are common.** Word frequencies, web links, social graphs and click logs follow a law close to Zipf's law, where the key of rank $i$ has a share proportional to $1/i$. Over $V$ keys, the top key then has the share $1/H_V$, where $H_V$ is the [harmonic number](/harmonic-series/). For $V = 10{,}000$, $H_V \approx 9.79$, so the top key holds about 10% of all pairs, and no number of reducers makes the reduce phase more than about 10 times faster than one reducer.

**Kinds of skew.**

- **Key skew.** A few keys have most of the pairs, as above.
- **Partition skew.** The keys are even, but the partitioner puts too many on one reducer. A hash partitioner has random collisions, and range split points chosen without a sample can be far off. The [partitioner](/partitioner/) page proves the balance bound of a hash partitioner, which needs every key to be small compared with $N/R$.
- **Work skew.** The input is even, but the work is not. In a [reduce-side join](/reduce-side-join/), the reducer of key $b$ outputs $|R_b| \cdot |S_b|$ tuples, so a key twice as frequent on both sides costs four times as much.
- **Record size skew.** A few values are much larger than the rest, such as a very long document or a vertex with millions of neighbours.

**Stragglers are not the same thing.** Dean and Ghemawat start backup copies of the last running tasks, because a slow machine often causes the delay (see [speculative execution](/speculative-execution/)). A reducer that is slow because of its data is just as slow on another machine, so backup tasks do not help against data skew.

**Fix 1: shrink the heavy keys before the shuffle.** For an aggregation with an associative and commutative operation, a [combiner](/combiner/) adds the values of each key in each map task. A key then sends at most one pair for each map task, so a heavy key costs at most $M$ pairs with $M$ map tasks. This is the first fix for counts, sums, minimums and maximums. It does not help when the reducer needs each value, as in a join.

**Fix 2: salting, or key splitting.** Find the heavy keys, for example from a sample, a [count-min sketch](/count-min-sketch/) or a [Misra-Gries summary](/misra-gries-summary/) of each split (the [frequent items problem](/frequent-items-problem/)). In the first round, send a pair of a heavy key $k$ with the key $(k, s)$, where $s$ is a random salt in $\{0, \ldots, S - 1\}$. The $S$ salted keys go to different reducers, which each compute a partial result. A second round combines the $S$ partial results of each heavy key. This needs an aggregation that can be split into parts, and it costs one more round and $S$ more pairs for each heavy key. For a join, the same idea splits the tuples of a heavy key on one side into $S$ random parts and copies the tuples of that key on the other side to all $S$ parts.

**Fix 3: skew-aware partitioning.** If the key counts are known, from a sample or a first pass, the keys can be placed on the reducers like jobs on machines, which is the [load balancing problem](/load-balancing-problem/). [List scheduling](/list-scheduling/) puts each key on the reducer with the least load so far. Its largest load is at most $N/R + c_{\max}$: when the last key of the most loaded reducer was placed, that reducer had the least load, which is at most the average load at that time, and so at most $(N - c)/R$, where $c \le c_{\max}$ is the count of that key. Placing the keys in order of decreasing count (the longest processing time first rule) gives at most $\left(\frac{4}{3} - \frac{1}{3R}\right)$ times the best possible largest load (Graham, 1969). No such partitioner goes below $c_{\max}$, so the heavy keys still need Fix 1 or Fix 2.

**Fix 4: heavy hitters in joins.** Beame, Koutris and Suciu (2014, Section 4.1) join $S_1(x, z)$ and $S_2(y, z)$ on $z$ with $p$ servers, where $S_j$ has $m_j$ tuples and the value $h$ occurs $m_j(h)$ times in $S_j$. A value $h$ is a *heavy hitter* of $S_j$ if $m_j(h) \ge m_j / p$, so each relation has at most $p$ of them.

- **Light values** go to the servers by a hash of $z$, as in a reduce-side join. Each such value has fewer than $m_j/p$ tuples in each relation.
- **A value heavy in $S_1$ only** gets $p_h = \lceil p \, m_1(h) / m_1 \rceil$ servers of its own. The tuples of $S_1$ with this value are spread over them, and the few tuples of $S_2$ with this value (fewer than $m_2/p$) are copied to all of them. The other case is the same with the roles swapped.
- **A value heavy in both** gets $p_h = \lceil p \, m_1(h) m_2(h) / \Sigma \rceil$ servers, where $\Sigma = \sum_{h'} m_1(h') m_2(h')$ over the values heavy in both. They form a grid of $p_1 \times p_2$ servers with $p_1 = \lceil \sqrt{p_h m_1(h)/m_2(h)} \rceil$ and $p_2 = \lceil \sqrt{p_h m_2(h)/m_1(h)} \rceil$. A tuple of $S_1$ picks a row and goes to every server of the row, a tuple of $S_2$ picks a column and goes to every server of the column, and each pair of tuples meets at exactly one server, as in the [Shares join](/hypercube-shares-join/).

Their load is $O(L \ln p)$ with high probability, where $L$ is the largest of $m_1/p$, $m_2/p$, $L_{12} = \sqrt{\Sigma / p}$ and two similar terms for the values heavy in one relation. They also prove that no one-round algorithm has a smaller load on all inputs with these heavy hitter counts, up to a constant factor, so the method is optimal for one round. On the servers of a value heavy in both, the load is at most $\lceil m_1(h)/p_1 \rceil + \lceil m_2(h)/p_2 \rceil \le 2 L_{12} + 2$, since $m_1(h)/p_1 \le \sqrt{m_1(h) m_2(h)/p_h} \le \sqrt{\Sigma/p}$, when the tuples of each side are dealt to the rows or columns in turn. The factor $\ln p$ comes from the hash of the light values.

## Examples

**An aggregation over Zipf keys.** Draw $N = 100{,}000$ keys from 10,000 keys by Zipf's law, with a fixed seed, and sum by key with $R = 16$ reducers. The average reducer input is 6,250. The top key has 10,022 pairs.

| method | largest reducer input |
|---|---|
| hash partitioner | 14,523 |
| list scheduling, longest first, with the exact counts | 10,022 |
| salting the 6 keys with at least $N/(4R)$ pairs into 16 salts, then hash | 8,083 in round 1, at most 16 in round 2 |

The skew-aware partitioner reaches $c_{\max} = 10{,}022$, which is the best possible without splitting keys. Salting goes below $c_{\max}$. Its largest load now comes from the hash collisions of the medium keys, so salting and a skew-aware partitioner work well together. Salting sent 96 more pairs, the partial sums of round 2. A combiner would cut every key, heavy or not, to at most one pair for each map task.

**A join over Zipf keys.** Draw 4,000 tuples for each of $R(A, B)$ and $S(B, C)$, with join values from 1,000 keys by Zipf's law, and use $p = 16$. The join has 460,500 tuples. Key 1 has 535 tuples in $R$ and 508 in $S$.

- The [reduce-side join](/reduce-side-join/) sends 8,000 tuples, an average of 500 for each reducer, and its largest reducer input is 1,437, because one reducer takes the 1,043 tuples of key 1.
- The heavy hitter method has $L = 250$. Keys 1 and 2 are heavy in both relations and get grids of 16 and 6 servers, so 38 servers are used in all. It sends 11,908 tuples. The largest load on a heavy server is 261, within the bound $2L + 2$, and the largest load on a light server is 751, from the hash of the light keys.

The largest load drops from 1,437 to 751, at the cost of about 50% more communication and more servers.

## Where it is used

- Every grouping job: [word count](/word-count/), where frequent words dominate without a combiner, and [inverted index](/inverted-index/) construction, where the posting lists of common terms are very long.
- Joins: the [reduce-side join](/reduce-side-join/) is sensitive to skew, the broadcast form of the [map-side join](/map-side-join/) is not, and the [Shares join](/hypercube-shares-join/) needs the heavy hitter treatment on skewed data.
- [Distributed sorting](/distributed-sorting/), where a very frequent key cannot be split by a range partitioner unless a tie-break makes the keys distinct.
- Graph computations on power-law graphs, where a vertex of high degree overloads its worker. Suri and Vassilvitskii called this the curse of the last reducer for [triangle counting](/triangle-counting/), and the [GAS model](/gas-model/) splits the work of such vertices over machines. The same issue arises in the [Pregel model](/pregel-model/).
- The same imbalance outside MapReduce is [load skew](/load-skew/) in caches and storage systems.

## References
