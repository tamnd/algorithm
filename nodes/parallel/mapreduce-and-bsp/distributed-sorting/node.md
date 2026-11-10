---
tag: 1SRXBE
kind: problem
slug: distributed-sorting
name: Distributed sorting
aliases:
- terasort
- global sort over a cluster
- total order sort
area: parallel/mapreduce-and-bsp
level: core
summary: Sort data spread over a cluster so that the reducer outputs, read in order, are globally sorted, using a range partitioner with sampled split points.
prereqs: [mapreduce-model, partitioner, sample-sort, chernoff-bound]
see_also: [sample-sort, parallel-sorting-by-regular-sampling, external-samplesort, external-merge-sort, parallel-sorting-problem, shuffle-phase, data-skew, range-partitioning]
sources:
  - paper: "Owen O'Malley, TeraByte Sort on Apache Hadoop, Yahoo!, May 2008 (sortbenchmark.org/YahooHadoop.pdf)"
    locator: the description of TeraSort (sampling of split points before the job, N minus 1 sampled keys, the trie partitioner, 100,000 sampled keys) and the result on 910 nodes
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, 6th Symposium on Operating Systems Design and Implementation (OSDI), 2004"
    locator: Section 5.3 (the sort benchmark, the partitioning function on the initial bytes of the key, and the remark that a general sort would add a pre-pass MapReduce to sample split points)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 4 (Chernoff bounds, Theorem 4.5 for the lower tail)
  - paper: "W. D. Frazer and A. C. McKellar, Samplesort: a sampling approach to minimal storage tree sorting, Journal of the ACM 17(3), 1970"
    locator: the idea of choosing splitters from a sorted random sample
---

Distributed sorting is the problem of sorting a dataset that is spread over many machines, so that the output is cut into $R$ parts and the parts, read in order, form the sorted sequence. In the [MapReduce model](/mapreduce-model/), the standard method is the cluster version of [sample sort](/sample-sort/): a sample of the keys gives $R - 1$ split points, a range [partitioner](/partitioner/) sends each key to the reduce task of its range, and the [shuffle](/shuffle-phase/) sorts inside each task. O'Malley's TeraSort (2008) on Hadoop is the best-known implementation. A sample of $O(R \log(n/\delta)/\varepsilon^2)$ keys gives every reduce task at most $(1 + \varepsilon)n/R$ keys with probability at least $1 - \delta$, which this page proves.

## In plain words

To sort a mountain of records with many computers, give each computer one stretch of the key order: the first one gets the smallest keys, the next one the next stretch, and so on. Each computer sorts its own stretch, and the outputs, one after another, are sorted. The hard part is to choose where the stretches start and end, so that each computer gets about the same amount of work. The data may be bunched up in some places. So first take a random sample of the keys, sort the sample, and cut it into equal pieces. The cut points of the sample are good cut points for the whole data, and a bigger sample gives more even pieces.

## Definition

**Input.** $n$ records with keys from a totally ordered set, cut into $M$ splits on different machines, and a number $R$ of reduce tasks.

**Output.** $R$ files $F_0, \dots, F_{R-1}$ such that each file is sorted and every key of $F_j$ is at most every key of $F_{j+1}$. So the concatenation $F_0 F_1 \cdots F_{R-1}$ is the sorted input.

**Cost model.** The [MapReduce model](/mapreduce-model/): rounds, the pairs of the [shuffle](/shuffle-phase/), the largest reducer input $L$ (here, the largest number of keys in one $F_j$) and the memory per machine. Comparisons count the local work. The goal is $L$ close to $n/R$, since the slowest reduce task decides the time of the round.

## Variants

- **Sampled split points (TeraSort).** Draw a sample before the sort, sort it, and take $R - 1$ evenly spaced sample keys as split points. O'Malley's TeraSort samples in the program that submits the job, uses 100,000 sampled keys, and builds a two-level trie on the first two bytes of the key so that each map task finds the range of a key quickly. Keys $k$ with $\text{sample}[i-1] \le k < \text{sample}[i]$ go to reduce task $i$.
- **A sampling round.** The same, but the sample is drawn by a first MapReduce round, as Dean and Ghemawat suggest for a general sort (Section 5.3, "a pre-pass MapReduce operation").
- **Split points from the key format.** Dean and Ghemawat's benchmark partitions on the initial bytes of the key, which is balanced only because the benchmark keys are uniformly random.
- **Regular sampling.** Each map task sorts its split and contributes $R - 1$ evenly spaced keys of its own. [PSRS](/parallel-sorting-by-regular-sampling/) shows that this gives at most $2n/p - p$ keys per processor, with no randomness, at the cost of a local sort before the sample.
- **Ties.** Equal keys go to one task under a range partitioner. When one key value is very frequent, sort by (key, record id) instead, which makes all keys distinct and lets the split points cut a run of equal keys.

## Examples

**One sort round.** Take the keys 17, 3, 12, 8, 20, 1, 15, 6, 11, 9 in $M = 2$ splits, $R = 3$, and split points 7 and 13. A key $k$ goes to task $|\{s_i \le k\}|$: task 0 gets 3, 1, 6, task 1 gets 12, 8, 11, 9, and task 2 gets 17, 20, 15. After the sort inside each task, the outputs are (1, 3, 6), (8, 9, 11, 12) and (15, 17, 20), and their concatenation is sorted. The round sends each key once, 10 pairs.

**The effect of the sample size.** Take $n = 20{,}000$ uniform random keys and $R = 8$, so the fair share is $n/R = 2{,}500$. For each $a$, the sample has $s = 8a$ keys, and the table gives the largest bucket over 30 random inputs, as a multiple of $n/R$.

| $a$ | sample size $s$ | mean of the largest bucket | worst of the largest bucket |
|---|---|---|---|
| 1 | 8 | 2.75 | 4.80 |
| 4 | 32 | 1.88 | 2.64 |
| 16 | 128 | 1.39 | 1.85 |
| 64 | 512 | 1.20 | 1.39 |
| 147 | 1,176 | 1.13 | 1.23 |

With $\varepsilon = 0.5$ and $\delta = 0.1$, the bound below asks for $a = 147$ and promises a largest bucket of at most $\lceil 1.5 \cdot 2{,}500 \rceil = 3{,}750$ keys with probability at least 0.9. The bound is safe but not tight.

**Clustered keys.** Let the keys be $x^4$ for $x$ uniform in $[0, 1)$, with $n = 20{,}000$ and $R = 8$. The split points $1/8, 2/8, \dots, 7/8$, chosen evenly over the range without a sample, give task 0 the keys below $1/8$, which are a fraction $(1/8)^{1/4} \approx 0.595$ of the input: 11,850 keys. Split points from a sample with $a = 147$ give a largest bucket of 2,894 keys.

**A large job.** For $n = 10^9$ keys, $R = 1000$, $\varepsilon = 0.1$ and $\delta = 0.01$, the bound asks for $a = 5{,}573$, so a sample of about $5.6 \times 10^6$ keys, 0.56% of the input. O'Malley's 2008 run sorted 10 billion rows with 1,800 reduce tasks and a sample of 100,000 keys, about 55 per task, and the report says the distribution "was hardly perfect and would benefit from more samples".

## Known algorithms

**Sample, then range partition (two rounds).** Round 1: each map task draws its share of a uniform sample with replacement of $s = aR$ keys and sends it to one reduce task, which sorts the sample and outputs the split points $y_j = S[ja]$ for $j = 1, \dots, R-1$, where $S$ is the sorted sample. Round 2: each map task sends each key $k$ to task $|\{j : y_j \le k\}|$, found by binary search in $O(\log R)$ comparisons, and each reduce task sorts its keys with an [external merge sort](/external-merge-sort/) inside the shuffle and writes them.

| Measure | Round 1 (sample) | Round 2 (sort) |
|---|---|---|
| pairs shuffled | $s = aR$ | $n$ |
| largest reducer input | $s$ | at most $(1+\varepsilon)n/R$ with probability $\ge 1 - \delta$ |
| local work | $O(s \log s)$ comparisons on one task | $O(n \log R)$ to partition, $O((n/R)\log(n/R))$ per task to sort |

TeraSort runs round 1 on the submitting machine instead, so the cluster runs one MapReduce round.

**Other methods.** Regular sampling ([PSRS](/parallel-sorting-by-regular-sampling/)) gives a deterministic bound. On one machine with a disk, [external samplesort](/external-samplesort/) and [external merge sort](/external-merge-sort/) solve the same problem, and the [parallel sorting problem](/parallel-sorting-problem/) page lists the shared-memory methods.

## Bounds

**Theorem (the sample size).** Let the $n$ keys be distinct, $R \ge 2$, $a \ge 1$ and $\varepsilon > 0$, and let $w = \lceil (1+\varepsilon)n/R \rceil \le n$. Draw $s = aR$ keys independently and uniformly with replacement, sort them into $S[1] \le \dots \le S[s]$, and let $y_j = S[ja]$ for $1 \le j \le R - 1$. Bucket $j$ holds the keys in $[y_j, y_{j+1})$, with $y_0 = -\infty$ and $y_R = +\infty$. Then

$$\Pr[\text{some bucket has more than } w \text{ keys}] \le n \exp\Big(-\frac{\varepsilon^2 a}{2(1+\varepsilon)}\Big).$$

So $a \ge 2(1+\varepsilon)\ln(n/\delta)/\varepsilon^2$, a sample of $s = O(R \log(n/\delta)/\varepsilon^2)$ keys, makes every bucket at most $w$ with probability at least $1 - \delta$.

*Proof.* Call a set of $w$ keys that are consecutive in sorted order a run. There are $n - w + 1 \le n$ runs.

*Step 1: a large bucket leaves a run with at most $a$ draws.* Let bucket $j$ have more than $w$ keys, and let $W$ be its $w$ largest keys. A bucket holds all keys of an interval, so $W$ is a run. The bucket has a key smaller than every key of $W$, and that key is at least $y_j$, so every key of $W$ is greater than $y_j$ (the keys are distinct). Every key of $W$ is less than $y_{j+1}$. Let a draw with key in $W$ sit at position $i$ of $S$. If $j \ge 1$, then $S[i] > y_j = S[ja]$, and $S$ is sorted, so $i > ja$. If $j \le R - 2$, then $S[i] < S[(j+1)a]$, so $i < (j+1)a$. So the positions lie in $\{ja + 1, \dots, (j+1)a - 1\}$ for $1 \le j \le R - 2$, in $\{1, \dots, a - 1\}$ for $j = 0$, and in $\{(R-1)a + 1, \dots, Ra\}$ for $j = R - 1$. In each case there are at most $a$ positions, so at most $a$ draws fall in $W$.

*Step 2: a fixed run gets more than $a$ draws with high probability.* Fix a run $W$. Each draw falls in $W$ with probability $w/n$, independently, so the number $X$ of draws in $W$ is binomial with mean $\mu = aRw/n \ge a(1+\varepsilon)$. Let $\eta = \varepsilon/(1+\varepsilon)$, so $0 < \eta < 1$ and $a \le \mu/(1+\varepsilon) = (1 - \eta)\mu$. The lower tail of the [Chernoff bound](/chernoff-bound/), $\Pr[X \le (1-\eta)\mu] \le e^{-\eta^2\mu/2}$ (Mitzenmacher and Upfal, Theorem 4.5), gives

$$\Pr[X \le a] \le \exp\Big(-\frac{\eta^2 \mu}{2}\Big) \le \exp\Big(-\frac{\varepsilon^2}{(1+\varepsilon)^2} \cdot \frac{a(1+\varepsilon)}{2}\Big) = \exp\Big(-\frac{\varepsilon^2 a}{2(1+\varepsilon)}\Big).$$

*Step 3.* By Step 1, the event that some bucket has more than $w$ keys implies that some run has at most $a$ draws. By Step 2 and the [union bound](/union-bound/) over at most $n$ runs, its probability is at most $n e^{-\varepsilon^2 a/(2(1+\varepsilon))}$. For $a \ge 2(1+\varepsilon)\ln(n/\delta)/\varepsilon^2$ this is at most $n \cdot \delta/n = \delta$. $\blacksquare$

With $\varepsilon = 1$ this is the bound of the [sample sort](/sample-sort/) page: buckets of at most $\lceil 2n/R \rceil$ keys with probability at least $1 - n e^{-a/4}$. Keys that are not distinct become distinct with the tie-break (key, record id), and the theorem applies to the pairs.

**Other bounds.**

- **Comparisons.** Any comparison sort makes $\Omega(n \log n)$ comparisons in the worst case (see the [sorting problem](/sorting-problem/)), and the algorithm above makes $O(n \log n + s \log s)$ comparisons in total.
- **Largest reducer input.** At least $n/R$ for any partition into $R$ files, so the theorem is within a factor $1 + \varepsilon$ of the best possible.
- **Communication.** The sort round sends every key once, $n$ pairs, replication rate 1. Keys that are already on the machine that will write them need not move, but in the worst case a constant fraction of all keys must cross the network.
- **Rounds.** Two rounds, or one round plus a sample read by the driver. Once the split points are known, one round suffices.

## Reductions

- Each reduce task solves a one-machine [sorting problem](/sorting-problem/) on its range, with an [external merge sort](/external-merge-sort/) when the range does not fit in memory.
- Choosing the split points is the problem of estimating the [quantiles](/quantile/) $1/R, 2/R, \dots$ of the key distribution from a [random sample](/random-sampling/).
- The [secondary sort](/secondary-sort/) is the easier problem of sorting within each key, which needs no range partitioner.

## Applications

- The sort benchmarks (TeraSort and its successors), which measure the data rate of a cluster.
- Building sorted, range-partitioned files for later lookups and for the merge form of the [map-side join](/map-side-join/).
- Range partitioning of tables in parallel databases, see [range partitioning](/range-partitioning/).
- Any job whose output must be in a total order, for example a ranked list of all pages by a score.

## References
