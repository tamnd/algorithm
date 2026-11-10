---
tag: MVTW3R
kind: problem
slug: distinct-elements-problem
name: Distinct elements problem
aliases:
- Count-distinct problem
- F0 estimation
- cardinality estimation
- count distinct
- distinct elements problem
- number of distinct values
area: online-and-streaming/streaming-sketches
level: core
summary: Estimate the number of distinct items in a stream.
prereqs: [streaming-model, frequency-vector, epsilon-delta-guarantee]
see_also: [flajolet-martin-algorithm, pcsa, loglog-counting, hyperloglog, hyperloglog-plus-plus, linear-counting, kmv-sketch, l0-sampling-problem]
sources:
  - paper: doi:10.1016/0022-0000(85)90041-8
    title: Philippe Flajolet and G. Nigel Martin, Probabilistic counting algorithms for data base applications, Journal of Computer and System Sciences 31(2), 1985
    locator: pp. 182 to 209
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999
    locator: pp. 137 to 147 (the F_0 estimate with pairwise independent hashing, and the lower bounds for deterministic and for randomized algorithms)
  - paper: doi:10.1109/SFCS.2003.1238202
    title: Piotr Indyk and David Woodruff, Tight lower bounds for the distinct elements problem, FOCS 2003
    locator: pp. 283 to 288 (the Ω(1/ε²) lower bound)
  - paper: doi:10.1145/1807085.1807094
    title: Daniel M. Kane, Jelani Nelson and David P. Woodruff, An optimal algorithm for the distinct elements problem, PODS 2010
    locator: pp. 41 to 52 (O(1/ε² + log n) bits, O(1) update and query time)
  - paper: doi:10.1007/3-540-45726-7_1
    title: Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar, D. Sivakumar and Luca Trevisan, Counting distinct elements in a data stream, RANDOM 2002
    locator: pp. 1 to 10
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 2 (count distinct summaries)
---

The distinct elements problem asks for the number of different items in a stream: $F_0 = |\{i : f_i \ne 0\}|$, where $f$ is the [frequency vector](/frequency-vector/). An exact answer needs about $n$ bits for a universe of size $n$, also for randomized algorithms. With an estimate within a factor $1 \pm \varepsilon$ the space drops to $O(1/\varepsilon^2 + \log n)$ bits (Kane, Nelson and Woodruff 2010), and this is optimal. The practical algorithms hash each item and keep a few bits about the hash values: [Flajolet-Martin](/flajolet-martin-algorithm/), [PCSA](/pcsa/), [LogLog](/loglog-counting/), [HyperLogLog](/hyperloglog/), [linear counting](/linear-counting/) and the [KMV sketch](/kmv-sketch/). On this page $m$ is the length of the stream and $n$ is the size of the universe. On the sketch pages $m$ is instead the number of registers or bitmaps.

## In plain words

A web site wants to know how many different people visited it today. Each visit carries a user name, and the same person can visit many times. The simple way is to keep a list of every name seen so far, and that list can be huge. If an answer within a few percent is enough, there is a much smaller way. Turn each name into a random looking number with a hash function. The same name always gives the same number, so repeated visits change nothing. Then look at a rare pattern in the numbers, such as how small the smallest one is, or how many zeros one ends with. The more different names there are, the more extreme the rarest pattern gets, and that tells you the count.

## Definition

The input is a stream $\sigma = a_1, \ldots, a_m$ with $a_j \in [n] = \{1, \ldots, n\}$. Let $f_i$ be the number of times $i$ occurs. The output is
$$F_0(\sigma) = |\{i \in [n] : f_i > 0\}|.$$
The approximate version takes $\varepsilon, \delta \in (0, 1)$ and must output $\hat F_0$ with $\Pr[|\hat F_0 - F_0| \le \varepsilon F_0] \ge 1 - \delta$, the relative [(ε, δ) guarantee](/epsilon-delta-guarantee/). The cost is the space in bits, which includes the seeds of the hash functions, and the update time and query time are given separately. The stream is in the [cash register model](/cash-register-model/) unless a variant says otherwise, and it is chosen before the random seeds are drawn.

## Variants

- **Exact count.** Return $F_0$ exactly.
- **Constant factor.** Return $\hat F_0$ with $F_0/c \le \hat F_0 \le cF_0$. The AMS version of [Flajolet-Martin](/flajolet-martin-algorithm/) does this with $c = 3$ in $O(\log n)$ bits.
- **Turnstile streams.** With deletions, the count is $L_0 = |\{i : f_i \ne 0\}|$, the number of nonzero entries. This is the [L0 sampling problem](/l0-sampling-problem/) setting, and it needs [linear sketches](/linear-sketch/); the hash and maximum sketches of this page cannot undo a deletion.
- **Distributed counts and unions.** Count the distinct items of the union of many streams, each summarized on its own machine. All the sketches here are [mergeable](/mergeable-summaries/).
- **Intersections and similarity.** Estimate $|A \cap B|$ or the [Jaccard similarity](/jaccard-similarity/) $|A \cap B|/|A \cup B|$ of two streams. The KMV sketch and [MinHash](/minhash/) do this; an estimate from inclusion and exclusion on union sketches has error relative to $|A \cup B|$.
- **Sliding windows.** Count the distinct items among the last $W$ items.
- **Count distinct per key.** Many counts at once, one per group, as in a database query with GROUP BY.

## Examples

The stream $\sigma = a, b, c, a, d, e, b, f$ has $m = 8$ and $F_0 = 6$. The worked examples of the sketch pages use it with small fixed hash tables, so the values show how each sketch computes, not how accurate it is.

| sketch | parameters | estimate |
|---|---|---|
| [Flajolet-Martin](/flajolet-martin-algorithm/), one bitmap | lowest zero $R = 3$ | $2^3/\varphi \approx 10.34$ |
| AMS, one copy | $Z = 4$ | $2^{4.5} \approx 22.6$ |
| [PCSA](/pcsa/) | 4 bitmaps | $(4/\varphi)\,2^{3/4} \approx 8.70$ |
| [Linear counting](/linear-counting/) | 8 bits, 4 empty | $8\ln 2 \approx 5.55$ |
| [KMV](/kmv-sketch/) | $k = 3$, $v_3 = 0.30$ | $2/0.30 \approx 6.67$ |
| KMV | $k = 10$ | 6, exact, as $F_0 < k$ |

The second example is the classic database use. A table has a column with $10^9$ rows. An exact count distinct needs a sort or a hash table of the distinct values. HyperLogLog with $m = 2048$ registers of 5 bits, about 1.3 kB, has a relative standard error near $1.04/\sqrt{2048} \approx 2.3\%$, for any number of distinct values up to about $10^9$.

## Known algorithms

| algorithm | year | space | error |
|---|---|---|---|
| hash set or sort | | $O(F_0 \log n)$ bits | exact |
| bit vector of size $n$ | | $n$ bits | exact |
| [Flajolet-Martin](/flajolet-martin-algorithm/) | 1985 | $O(\log n)$ bits per bitmap | one bitmap: constant factor |
| [PCSA](/pcsa/) | 1985 | $m$ bitmaps of $O(\log n)$ bits | about $0.78/\sqrt m$ |
| [Linear counting](/linear-counting/) | 1990 | $m$ bits, $m$ linear in $F_0$ | good while $F_0/m$ is a small constant |
| AMS | 1996 | $O(\log n)$ bits | factor 3, constant probability |
| [KMV](/kmv-sketch/) and BJKST | 2002 | $k$ hash values | $1/\sqrt{k - 2}$, unbiased |
| [LogLog](/loglog-counting/) | 2003 | $m$ registers of $O(\log\log n)$ bits | about $1.30/\sqrt m$ |
| [HyperLogLog](/hyperloglog/) | 2007 | $m$ registers of $O(\log\log n)$ bits | about $1.04/\sqrt m$ |
| [HyperLogLog++](/hyperloglog-plus-plus/) | 2013 | sparse, then $m$ registers of 6 bits | HyperLogLog, with less bias for small counts |
| Kane, Nelson and Woodruff | 2010 | $O(1/\varepsilon^2 + \log n)$ bits | $(\varepsilon, 2/3)$, optimal |

The standard errors of PCSA, LogLog and HyperLogLog are asymptotic results for a fully random hash function. The AMS, BJKST and Kane, Nelson and Woodruff bounds are proved with hash families of limited independence, whose seeds are counted in the space. The algorithm of Kane, Nelson and Woodruff has $O(1)$ worst case update time and query time; it is of theoretical interest, and practice uses HyperLogLog.

## Bounds

**Deterministic exact counting needs $n - O(\log n)$ bits (proved here).** Let a deterministic one-pass algorithm output $F_0$ exactly. Let $A \ne B$ be two subsets of $[n]$ of size $n/2$, each fed as a stream in increasing order. If the two states are equal, take $x \in A \setminus B$ and append it. The answer on $A, x$ is $n/2$ and on $B, x$ it is $n/2 + 1$, but the algorithm is in the same state and gives the same answer. So all $\binom{n}{n/2}$ subsets give different states, and the algorithm needs $\log_2\binom{n}{n/2} \ge n - \log_2(n+1)$ bits, because $\binom{n}{n/2}$ is the largest of the $n + 1$ binomial coefficients that sum to $2^n$. $\square$

**Deterministic approximation (cited).** Alon, Matias and Szegedy show that a deterministic algorithm that approximates $F_0$ within a small constant factor also needs $\Omega(n)$ bits.

**Randomized exact counting needs $\Omega(n)$ bits (the reduction is proved here, the communication bound is cited).** In set disjointness, Alice has $A \subseteq [n]$, Bob has $B \subseteq [n]$, and they must decide whether $A \cap B = \emptyset$. Every randomized protocol with error $1/3$ needs $\Omega(n)$ bits of [communication](/communication-complexity/) (Kalyanasundaram and Schnitger, Razborov). Given a streaming algorithm with $s$ bits of state, Alice runs it on $A$, sends the state and $|A|$ to Bob, and Bob continues on $B$. Then $F_0 = |A| + |B| - |A \cap B|$, so Bob knows whether the sets meet. This is a protocol with $s + O(\log n)$ bits, so $s = \Omega(n)$. The same argument applies to a $(1 \pm \varepsilon)$ estimate with $\varepsilon < 1/(2n)$.

**Approximate counting needs $\Omega(1/\varepsilon^2 + \log n)$ bits (cited).**

- $\Omega(\log n)$ for any constant factor, from Alon, Matias and Szegedy.
- $\Omega(1/\varepsilon^2)$ from Indyk and Woodruff (2003), by a reduction from the gap-Hamming problem of communication complexity, for $1/\varepsilon^2$ up to a constant fraction of $n$. The proof uses the same reduction from a communication problem as above.

**The matching upper bound (cited).** Kane, Nelson and Woodruff (2010) give an algorithm with $O(1/\varepsilon^2 + \log n)$ bits that succeeds with probability $2/3$. With the [median trick](/median-trick/), $O((1/\varepsilon^2 + \log n)\log(1/\delta))$ bits give probability $1 - \delta$.

## Reductions

- **$F_0$ is a frequency moment.** It is $F_k = \sum_i f_i^k$ for $k = 0$, with $0^0 = 0$. See the [frequency moment problem](/frequency-moment-problem/).
- **Element distinctness.** All $m$ items of a stream are different exactly when $F_0 = m$. So an exact $F_0$ algorithm decides [element distinctness](/element-distinctness/), and lower bounds for element distinctness are lower bounds for exact $F_0$.
- **Union of sets.** $F_0$ of the concatenation of two streams is $|A \cup B|$. Merging two sketches with the same hash computes this, which is why mergeable sketches are the norm here.
- **Intersection.** $|A \cap B| = |A| + |B| - |A \cup B|$, but the error of this difference is relative to $|A \cup B|$, which is poor for a small intersection. The KMV sketch gives a better estimate from the hash values that both sketches share.
- **To $L_0$ in turnstile streams.** In the strict turnstile model, $F_0$ of the final $f$ is $L_0$. Sketches built for $L_0$ solve the problem with deletions, at a higher cost.

## Applications

- **Databases.** COUNT DISTINCT queries, and the statistics that a query optimizer uses to plan a [hash join](/hash-join/) or choose an index. This was the motivation of Flajolet and Martin, and it is the topic of [cardinality estimation](/cardinality-estimation/).
- **Web and product analytics.** Unique visitors, unique users per day, per page or per region, with mergeable sketches per hour that can be combined for any period.
- **Network monitoring.** The number of distinct flows, distinct source addresses, or distinct ports per source, which detect port scans and denial of service attacks.
- **Search and advertising.** Distinct queries, distinct users who saw an advertisement, and the overlap of two audiences.
- **Genomics.** The number of distinct $k$-mers in a set of sequencing reads, used to choose the size of later data structures.

## References
