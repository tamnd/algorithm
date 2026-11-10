---
tag: H2Z01K
kind: concept
slug: partitioner
name: Partitioner
aliases:
- partitioning function
- hash partitioner
- range partitioner
area: parallel/mapreduce-and-bsp
level: intro
summary: The function that maps each intermediate key to a reducer, usually by hashing, or by key ranges for sorted output.
prereqs: [mapreduce-model, hash-function]
see_also: [shuffle-phase, distributed-sorting, secondary-sort, data-skew, hash-partitioning, range-partitioning, chernoff-bound, balls-into-bins-max-load]
sources:
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, 6th Symposium on Operating Systems Design and Implementation (OSDI), 2004"
    locator: Section 3.1 (the default hash(key) mod R) and Section 4.1 (partitioning function, with the example hash(Hostname(urlkey)) mod R)
  - book: isbn:9781608453429
    title: Jimmy Lin and Chris Dyer, Data-Intensive Text Processing with MapReduce, Morgan and Claypool, 2010
    locator: Section 2.4 (partitioners and combiners) and Section 3.4 (secondary sorting, with a partitioner on part of a composite key)
  - paper: "Owen O'Malley, TeraByte Sort on Apache Hadoop, Yahoo!, May 2008 (sortbenchmark.org/YahooHadoop.pdf)"
    locator: the description of the TeraSort partitioner (N minus 1 sampled keys and a two-level trie)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 4 (Chernoff bounds, Theorem 4.4)
---

A partitioner is the function that decides, for each intermediate key of a [MapReduce](/mapreduce-model/) round, which of the $R$ reduce tasks receives it. The default is a hash of the key modulo $R$, which spreads the distinct keys evenly. A range partitioner cuts the key space at $R - 1$ split points instead, so that the outputs of the reduce tasks, read in order, are sorted. The partitioner decides the largest reducer input of the [shuffle](/shuffle-phase/), but no partitioner can split a single heavy key.

## In plain words

When the map step is done, every note with a key must go to one receiving computer, and all notes with the same key must go to the same one. The partitioner is the rule that picks the receiver from the key. The usual rule mixes up the key with a hash and takes the remainder, which spreads the keys like random throws of balls into bins. Another rule gives each receiver one stretch of the sorted key order, so that the first receiver gets the smallest keys, the next one the next stretch, and so on. Then the outputs, read one after another, are in sorted order. A good rule gives every receiver about the same amount of work.

## The idea

A partitioner for $R$ reduce tasks is a function $\pi : K \to \{0, 1, \dots, R - 1\}$ on the intermediate keys. Two rules make it correct.

- **It is a function of the key only.** Every map task must send a key to the same reduce task, so $\pi$ must give the same result in every process. A hash that changes between processes, such as Python's built-in hash of a string, breaks this.
- **It agrees with the grouping.** Keys that the reduce side treats as one group must have the same $\pi$. With a [secondary sort](/secondary-sort/), the key is a composite (natural key, sort field) and $\pi$ must use only the natural key.

### Hash partitioning

The default of Dean and Ghemawat (Section 3.1) is $\pi(k) = h(k) \bmod R$ for a hash function $h$. Section 4.1 gives a custom example, $h(\text{Hostname}(k)) \bmod R$ for URL keys, so that all URLs of one host end up in the same output file.

**Balance, proved.** Model $h$ as a fully random function, so that the values $\pi(k)$ are independent and uniform on $\{0, \dots, R - 1\}$. Let key $k$ carry $c(k)$ pairs, let $P = \sum_k c(k)$ and $c_{\max} = \max_k c(k)$. The input of reduce task $j$ is $X_j = \sum_k c(k)\,[\pi(k) = j]$, with $\mathbb{E}[X_j] = P/R$. The scaled terms $c(k)[\pi(k) = j]/c_{\max}$ are independent and lie in $[0, 1]$, so the upper tail of the [Chernoff bound](/chernoff-bound/) (Mitzenmacher and Upfal, Theorem 4.4, in its form for independent variables in $[0, 1]$) gives, for $0 < \varepsilon \le 1$,

$$\Pr\Big[X_j \ge (1 + \varepsilon)\frac{P}{R}\Big] \le \exp\Big(-\frac{\varepsilon^2 P}{3 R\, c_{\max}}\Big).$$

By the [union bound](/union-bound/) over the $R$ reduce tasks, the largest input $L = \max_j X_j$ satisfies $L < (1 + \varepsilon)P/R$ with probability at least $1 - R\,e^{-\varepsilon^2 P/(3 R c_{\max})}$. So hash partitioning is balanced within a factor $1 + \varepsilon$ with probability at least $1 - \delta$ when

$$\frac{P}{R} \ge \frac{3\, c_{\max} \ln(R/\delta)}{\varepsilon^2},$$

that is, when the fair share $P/R$ is large compared with the heaviest key. The other side is a lower bound for every partitioner: the key with $c_{\max}$ pairs goes to one task, and the inputs add up to $P$, so

$$L \ge \max\Big(c_{\max}, \frac{P}{R}\Big).$$

When $c_{\max} > P/R$, no partitioner reaches the average, and the fix is to change the keys, see [data skew](/data-skew/). With unit weights this is the [balls into bins](/balls-into-bins/) setting, see [the maximum load](/balls-into-bins-max-load/).

### Range partitioning

A range partitioner has split points $s_1 < s_2 < \dots < s_{R-1}$ and sends $k$ to $\pi(k) = |\{i : s_i \le k\}|$, so reduce task $j$ gets the keys in $[s_j, s_{j+1})$, with $s_0 = -\infty$ and $s_R = +\infty$. Each reduce task sorts its own keys in the [shuffle](/shuffle-phase/), and the tasks hold increasing ranges, so the concatenation of the outputs of tasks $0, 1, \dots, R - 1$ is sorted. This is how MapReduce sorts the whole input, see [distributed sorting](/distributed-sorting/). A lookup costs $O(\log R)$ comparisons by binary search. TeraSort (O'Malley 2008) uses $R - 1$ sampled keys and a two-level trie on the first two bytes of the key to make the lookup faster.

The balance depends on the split points, not on a hash. Split points chosen without looking at the data, for example evenly over the possible key values, fail when the keys cluster. Split points taken from a random sample of the keys give each task $O(n/R)$ keys with high probability once the sample has $O(R \log n)$ keys, and [distributed sorting](/distributed-sorting/) proves a bound of this form. Equal keys still go to one task, so duplicates need a tie-break such as (key, record id) when one value is very frequent.

### Other partitioners

- **On part of the key.** For a [secondary sort](/secondary-sort/) or an [inverted index](/inverted-index/) with composite keys (term, document), $\pi$ hashes only the first field.
- **Co-partitioning.** Two jobs that use the same $\pi$ and the same $R$ put each key in the same part number in both outputs, which a [map-side join](/map-side-join/) needs.
- **Grid partitioners.** The [Shares (HyperCube) join](/hypercube-shares-join/) sends a tuple to a set of reducers given by a vector of hash values, one per attribute.
- **When $R$ changes.** With $h(k) \bmod R$, changing $R$ moves almost every key. [Consistent hashing](/consistent-hashing/) moves only a fraction of about $1/R$ of the keys when one bucket is added, which matters in storage systems more than in one MapReduce job.

## Examples

**Hash partitioning of unit keys.** Take $10^6$ distinct keys with one pair each and $R = 100$, so $P/R = 10^4$. The bound with $\delta = 0.01$ gives $\varepsilon = \sqrt{3 \ln(10^4)/10^4} \approx 0.0526$, so $L < 10{,}526$ with probability at least $0.99$. With the keys "k0" to "k999999" and CRC-32 modulo 100 as the hash, the largest input is 10,253 and the smallest is 9,822.

**Hash partitioning of Zipf keys.** Take $10^5$ distinct keys whose weights follow a Zipf law with exponent 1, with $P = 10^6$ pairs in total and $R = 100$. The heaviest key has $P/H_{10^5} \approx 10^6/12.09 \approx 82{,}712$ pairs, so $L \ge 82{,}712$, more than 8 times the average of $10^4$, for every partitioner.

**Range partitioning.** Take the keys 1 to 20, $R = 4$ and split points 6, 11, 16. Then $\pi(5) = 0$, $\pi(6) = 1$, $\pi(15) = 2$ and $\pi(20) = 3$, and the four tasks get 1 to 5, 6 to 10, 11 to 15 and 16 to 20. If the keys are instead 1000 values in $[0, 100)$ and the split points are 250, 500 and 750, chosen evenly over the range $[0, 1000)$ without a sample, then task 0 gets all 1000 keys.

**A weak hash.** In Java the hash code of an integer is the integer itself. With $\pi(k) = h(k) \bmod R$ and keys that are all multiples of $R$, every key goes to task 0. A hash that mixes the bits avoids this.

## Where it is used

- Every MapReduce round with a reduce phase, through the [shuffle](/shuffle-phase/).
- [Distributed sorting](/distributed-sorting/) and TeraSort, with a range partitioner from a sample.
- The [secondary sort](/secondary-sort/) and the value-to-key pattern of the [inverted index](/inverted-index/), with a partitioner on the natural key.
- Joins: the [reduce-side join](/reduce-side-join/) hashes the join key, the [map-side join](/map-side-join/) needs co-partitioned inputs, and the [Shares join](/hypercube-shares-join/) uses a grid.
- Parallel databases use the same two schemes as [hash partitioning](/hash-partitioning/) and [range partitioning](/range-partitioning/) of tables.

## References
