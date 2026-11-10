---
tag: 1RHMXP
kind: problem
slug: sliding-window-join
name: Sliding window join
aliases:
- windowed stream join
- window join
- symmetric hash join over windows
area: online-and-streaming/sliding-windows
level: research
summary: Join two streams so that each tuple matches the tuples in the current window of the other stream; the symmetric hash join does it in time linear in input plus output.
prereqs: [relational-join, hash-join, sliding-window-model]
see_also: [hash-join, nested-loop-join, relational-join, time-based-window, count-based-window, load-shedding, join-size-estimation-problem, sliding-window-aggregation]
sources:
  - paper: doi:10.1109/ICDE.2003.1260804
    title: Jaewoo Kang, Jeffrey F. Naughton and Stratis D. Viglas, Evaluating window joins over unbounded streams, ICDE 2003
    locator: pages 341 to 352, the probe, insert and invalidate steps of a window join, the per-unit-time cost model in terms of the arrival rates and window sizes, and asymmetric joins that use a different method in each direction
  - paper: "Annita N. Wilschut and Peter M. G. Apers, Dataflow query execution in a parallel main-memory environment, PDIS 1991"
    locator: the symmetric (pipelining) hash join, which keeps a hash table for each input and probes the other table with each arriving tuple
---

The sliding window join problem asks for all pairs of matching tuples from two streams $A$ and $B$ such that, when the later tuple of the pair arrives, the earlier tuple is still in the window of its stream. A window keeps the last $N$ tuples of a stream, or the tuples of the last $T$ time units, so the join needs bounded memory, while a [relational join](/relational-join/) of two unbounded streams does not. The symmetric hash join of Wilschut and Apers (1991) solves it: each arriving tuple removes expired tuples, probes a hash table on the window of the other stream, and is inserted into the hash table of its own window. Kang, Naughton and Viglas (2003) gave the cost model of these three steps and showed that the two directions of the join can use different methods.

## In plain words

Two sensors send readings with a location, and you want every pair of readings from the same location taken at most ten seconds apart. When a reading arrives, you look for matching readings of the other sensor from the last ten seconds, report each pair, and then store the new reading so that later readings of the other sensor can find it. Readings older than ten seconds can never be part of a new pair, so you throw them away. If the stored readings are grouped by location in a hash table, each look-up touches only the readings that match.

## Definition

Each tuple $u$ has a stream $s(u) \in \{A, B\}$, a timestamp $\tau(u)$, a join key $k(u)$ and a payload. Tuples arrive one at a time in an order with nondecreasing timestamps. The windows are given by lengths $T_A, T_B > 0$ for **time-based windows**, or by sizes $N_A, N_B \ge 1$ for **count-based windows**.

For time-based windows, the output is every pair $(a, b)$ with $s(a) = A$, $s(b) = B$, $k(a) = k(b)$, and

- $\tau(a) - \tau(b) < T_B$ if $b$ arrives before $a$,
- $\tau(b) - \tau(a) < T_A$ if $a$ arrives before $b$.

So the later tuple sees the earlier tuple in the window of the earlier tuple's stream at the arrival time of the later tuple. For count-based windows, the later tuple sees the last $N_A$ (or $N_B$) tuples of the other stream that arrived before it. Each pair is output once, at the arrival of its later tuple. Other join conditions, such as $|k(a) - k(b)| \le \delta$, give the variants below.

## Variants

- **Count-based or time-based windows**, see [count-based windows](/count-based-window/) and [time-based windows](/time-based-window/). With count-based windows the memory is fixed; with time-based windows it depends on the arrival rates.
- **Band and inequality joins.** For a condition such as $|k(a) - k(b)| \le \delta$, an ordered index such as a balanced search tree takes the place of the hash table, and a probe costs $O(\log n + \text{matches})$.
- **Multiway joins.** For $m$ streams, each arriving tuple probes the windows of the other streams in some order; the order changes the work in the same way as in [join ordering](/join-ordering/).
- **Limited memory.** If the windows do not fit, some tuples must be dropped and the output is approximate; which tuples to drop is a [load shedding](/load-shedding/) problem.
- **Out-of-order arrival.** If timestamps can arrive late, expiry must wait for a bound on the delay.

## Examples

$T_A = T_B = 3$ and the arrivals $a_1 = (1, x)$, $b_1 = (2, x)$, $b_2 = (2, y)$, $a_2 = (4, y)$, $b_3 = (5, x)$, $a_3 = (6, x)$, written as (timestamp, key). A window at time $t$ holds the tuples with timestamp greater than $t - 3$.

| arrival | expired before the probe | probe result | window of $A$ after | window of $B$ after |
|---|---|---|---|---|
| $a_1$ at 1 | | none | $a_1$ | |
| $b_1$ at 2 | | $(a_1, b_1)$ | $a_1$ | $b_1$ |
| $b_2$ at 2 | | none | $a_1$ | $b_1, b_2$ |
| $a_2$ at 4 | $a_1$ | $(a_2, b_2)$ | $a_2$ | $b_1, b_2$ |
| $b_3$ at 5 | $b_1, b_2$ | none | $a_2$ | $b_3$ |
| $a_3$ at 6 | | $(a_3, b_3)$ | $a_2, a_3$ | $b_3$ |

The tuples $a_1$ and $b_3$ have the same key but are 4 time units apart, so they do not join; $a_1$ expired at time 4, before $b_3$ arrived.

## Known algorithms

**Symmetric hash join.** For each stream $X$, keep a FIFO queue $Q_X$ of the tuples in its window, and a hash table $H_X$ that maps each key to a FIFO queue of the tuples with that key. For an arrival on stream $S$, let $O$ be the other stream.

```pseudo id=main
ARRIVE(S, τ, k, v)
L1  for X in {A, B}: while Q_X is not empty and time(front(Q_X)) ≤ τ − T_X do remove front(Q_X) from Q_X and from the front of H_X[its key]
L2  for each tuple u in H_O[k] do output the pair of (τ, k, v) and u
L3  append (τ, k, v) at the back of Q_S and at the back of H_S[k]
```

*Correctness.* Line L1 keeps the invariant that $Q_X$ and $H_X$ hold exactly the tuples of $X$ with timestamp greater than $\tau - T_X$. Since timestamps do not decrease, an expired tuple stays expired, and the tuples of $Q_X$ are in arrival order, so the expired tuples form a prefix of $Q_X$. The front of $Q_X$ is the oldest tuple of $X$, so it is also the oldest tuple with its key, which is the front of $H_X$ for that key; removing from the front of that queue removes the right tuple. Then line L2 outputs exactly the tuples of the other stream that are in its window and have key $k$, which is the definition. Line L3 makes the new tuple visible to later arrivals. Each pair is output once, by its later tuple.

*Cost.* Each tuple is inserted once and removed once, in $O(1)$ expected time with hashing. A probe costs $O(1)$ expected time plus the number of matches. The total time is $O(\text{input} + \text{output})$ in expectation, and the memory is the number of tuples in the two windows. For count-based windows, line L1 is dropped, and after line L3 the oldest tuple of $S$ is removed when $Q_S$ holds more than $N_S$ tuples.

**Nested loops.** Without an index, a probe compares the new tuple with every tuple in the other window, as in the [nested loop join](/nested-loop-join/). This needs no hash tables and works for any join condition.

**Cost model.** The model below follows the structure of the cost model of Kang, Naughton and Viglas, with probe, insert and invalidate costs per unit time; the formulas are derived here under simple assumptions. Let tuples arrive at rates $\lambda_A$ and $\lambda_B$ per time unit, and let $\sigma$ be the probability that a tuple of $A$ and a tuple of $B$ have equal keys. In the steady state the windows hold on average $n_A = \lambda_A T_A$ and $n_B = \lambda_B T_B$ tuples. Per time unit:

- *Output.* Each arrival of $A$ meets on average $\sigma n_B$ matches and each arrival of $B$ meets $\sigma n_A$, so the output rate is $R = \sigma(\lambda_A n_B + \lambda_B n_A) = \sigma \lambda_A \lambda_B (T_A + T_B)$.
- *Nested loops in both directions.* The probes make $\lambda_A n_B + \lambda_B n_A = R / \sigma$ comparisons.
- *Symmetric hash join.* The work is $\lambda_A + \lambda_B$ inserts, $\lambda_A + \lambda_B$ removals, $\lambda_A + \lambda_B$ probes and $R$ outputs, which is $\Theta(\lambda_A + \lambda_B + R)$.
- *Asymmetric choice.* Let an index on the window of $B$ cost $c_{\text{idx}}$ per tuple of $B$ to insert and remove, and let a comparison cost $c_{\text{cmp}}$. The index costs $\lambda_B c_{\text{idx}}$ per time unit and saves about $\lambda_A n_B (1 - \sigma) c_{\text{cmp}}$. So the index on $B$ pays off when $c_{\text{idx}} < \lambda_A T_B (1 - \sigma) c_{\text{cmp}}$, where $\lambda_A T_B$ is the number of probes that a tuple of $B$ receives while it is in its window. The same test with $A$ and $B$ swapped decides the other direction, so with very different rates the best plan can be a hash table on one window and a plain list on the other.

| method | time per time unit | memory |
|---|---|---|
| nested loops in both directions | $\lambda_A \lambda_B (T_A + T_B)$ comparisons | $n_A + n_B$ tuples |
| symmetric hash join | $O(\lambda_A + \lambda_B + R)$ expected | $n_A + n_B$ tuples and two hash tables |
| asymmetric join | by the test above, per direction | $n_A + n_B$ tuples and one or two indexes |
| ordered index, band joins | $O((\lambda_A + \lambda_B) \log n + R)$ | $n_A + n_B$ tuples and two search trees |

## Bounds

**Time.** Every algorithm reads each tuple and writes each output pair, so $\Omega(\text{input} + \text{output})$ time is necessary, and the symmetric hash join meets it in expectation. The output can be quadratic: if all keys are equal, an arrival matches the whole other window.

**Memory, proved here.** Take count-based windows and a universe of keys $U$ with $|U| \ge N_A$. After $N_A$ tuples of $A$ with distinct keys from a set $S$, the window of $A$ is exactly $S$, and one more tuple of $B$ with key $k$ produces output exactly when $k \in S$. So the state after the $N_A$ tuples determines $S$, and two different sets need two different states. An exact algorithm thus needs at least $\log_2 \binom{|U|}{N_A} \ge N_A \log_2 (|U| / N_A)$ bits for the window of $A$, and by symmetry for $B$. Storing the windows uses $O((N_A + N_B) \log |U|)$ bits for the keys, so the stored windows are optimal up to the factor between $\log |U|$ and $\log(|U| / N)$. The same argument holds for time-based windows with all the tuples of $S$ arriving within one window length.

## Reductions

- **From the relational join.** With windows longer than the streams, the problem is the pipelined [hash join](/hash-join/) of two finite relations, which outputs results while the inputs still arrive.
- **To set membership.** The memory bound above is the bound for storing a set under membership queries, since a probe of the other window is a membership query with multiplicities.
- **Join size.** Counting the output pairs without listing them is the [join size estimation problem](/join-size-estimation-problem/), which can use much less memory if an approximate count is enough.

## Applications

Correlation of events from two sources in a short time span, such as clicks with the ad impressions of the last minutes or alarms of two sensors at the same place; matching of trades with quotes in financial streams; network monitoring that pairs requests with responses within a timeout; and the join operators of stream processing systems, which offer interval or window joins over keyed streams.

## References
