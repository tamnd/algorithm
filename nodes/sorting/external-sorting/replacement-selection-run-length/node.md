---
tag: 1YP931
kind: theorem
slug: replacement-selection-run-length
name: Expected run length of replacement selection
aliases:
- snowplow run length theorem
area: sorting/external-sorting
level: advanced
summary: On random input, replacement selection produces runs of expected length about twice the heap capacity.
prereqs: [replacement-selection, expected-value, linearity-of-expectation, law-of-large-numbers]
see_also: [sorted-run, external-merge-sort, random-variable, polyphase-merge-sort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4.1, Multiway Merging and Replacement Selection (the snowplow argument, and the expected length of the first run)
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Section 5.2, Sorting by Merging (runs of 2M items on average)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition
    locator: Chapter 13, External Sorting (the average run length of replacement sort)
---

This theorem says that [replacement selection](/replacement-selection/) with a heap of $P$ items cuts $n$ random items into about $n/(2P)$ runs, so the runs have an average length of about $2P$. The exact form is $\frac{n}{2P} < \mathbb{E}[R_n] < \frac{n}{2P} + 2$ for the number $R_n$ of runs, and the average run length tends to $2P$ with probability 1. It explains why replacement selection halves the number of runs of an [external merge sort](/external-merge-sort/) on random data. The proof below is a version of Knuth's snowplow argument.

## Statement

Let $P \ge 1$ and $n \ge 1$ be integers. Let the input be $n$ keys $Y_1, \ldots, Y_n$ that are independent and have the same continuous distribution. Run REPLACEMENT-SELECTION with a heap of $P$ items, and let $R_n$ be the number of runs that it makes.

**Theorem.** (a) $\dfrac{n}{2P} < \mathbb{E}[R_n] < \dfrac{n}{2P} + 2$.

(b) With probability 1, $\dfrac{n}{R_n} \to 2P$ as $n \to \infty$.

The distribution of the keys does not matter, as long as it is continuous. If $G$ is the distribution function, the keys $G(Y_k)$ are independent and uniform on $[0, 1)$, and $G$ keeps the order of distinct keys, so the runs are the same. We therefore assume that the keys are uniform on $[0, 1)$, and, with probability 1, distinct.

## In plain words

Picture a snowplow on a circular road in steady snow. The plow clears the snow in front of it. Snow that falls behind the plow waits for the next round. The road is the range of the keys, one round of the plow is one run, and the snow on the road is the memory.

After some rounds, the amount of snow on the road is the same at each moment: it is the memory size. Just in front of the plow, the snow is deep, because it fell over almost a full round. Just behind the plow, there is almost no snow. On average it is half as deep as in front of the plow. So in one round the plow removes two times the snow that lies on the road at one moment. In the same way, one run removes about two times the memory size of items.

## Proof

Number the outputs $t = 1, \ldots, n$. The item of output $t$ has a run number $r_t \ge 1$ and a key $x_t \in [0, 1)$. Give each item the *due time*

$$\tau = (\text{its run number}) - 1 + (\text{its key}).$$

Write $\tau_t$ for the due time of output $t$.

**Step 1: the outputs come in order of due time.** The heap orders by run number, then by key, which is the order of due times. An item that replaces the output $x$ of run $r$ gets the run number $r$ only if its key is at least $x$, and else $r + 1$. In both cases its due time is at least $r - 1 + x$. So each item that enters the heap has a due time of at least the due time of the last output, and $\tau_1 \le \tau_2 \le \cdots \le \tau_n$.

**Step 2: the time in memory.** Give each item an *arrival time* $a_k$: the items $1, \ldots, \min(P, n)$ of the input enter at line L2 and get $a_k = 0$. Input item $P + t$, for $1 \le t \le n - P$, enters at output $t$ and gets $a_{P+t} = \tau_t$. Let $d_k$ be the due time of input item $k$, and let $U_k = d_k - a_k$.

For $k \le P$, the item is in run 1, so $d_k = Y_k$ and $U_k = Y_k$. For $k = P + t$, let $x$ be the key and $r$ the run number of output $t$, so $a_k = r - 1 + x$. If $Y_k \ge x$, then $d_k = r - 1 + Y_k$ and $U_k = Y_k - x$. If $Y_k < x$, then $d_k = r + Y_k$ and $U_k = 1 + Y_k - x$. In both cases

$$U_k = (Y_k - x) \bmod 1 \in [0, 1).$$

The key $x$ depends only on $Y_1, \ldots, Y_{k-1}$, and $Y_k$ is uniform on $[0,1)$ and independent of them. A shift modulo 1 of a uniform variable on $[0, 1)$ is uniform on $[0, 1)$. So, given $Y_1, \ldots, Y_{k-1}$, the variable $U_k$ is uniform on $[0, 1)$. Each $U_j$ with $j < k$ is a function of $Y_1, \ldots, Y_{k-1}$. Hence $U_1, \ldots, U_n$ are independent and uniform on $[0, 1)$, and $\mathbb{E}[U_k] = 1/2$.

**Step 3: the memory is full.** For a time $s \ge 0$, let $N(s)$ be the number of items $k$ with $a_k \le s < d_k$. An item with $a_k \le s < d_k$ has entered the heap and is not yet output at time $s$, by Step 1. For $n > P$: after each of the outputs $1, \ldots, n - P$, line L10 keeps the heap at $P$ items. With $\tau_0 = 0$ and $1 \le t \le n - P + 1$, at a time $s$ with $\tau_{t-1} \le s < \tau_t$ the heap holds the $P$ items that remain after output $t - 1$, and each of them has $a_k \le \tau_{t-1} \le s$ and $d_k \ge \tau_t > s$. So $N(s) = P$ for $0 \le s < \tau_{n-P+1}$, and $N(s) \le P$ for all $s$. Each item counts in $N$ during an interval of length $U_k$, so

$$\int_0^\infty N(s)\, ds = \sum_{k=1}^n U_k.$$

From $N(s) = P$ on $[0, \tau_{n-P+1})$, $N(s) \le P$, and $N(s) = 0$ for $s \ge \tau_n$:

$$P \, \tau_{n-P+1} \le \sum_{k=1}^n U_k \le P \, \tau_n.$$

**Step 4: the last due time.** The last item enters at time $\tau_{n-P}$ and each item has $U_k < 1$, so each due time is less than $\tau_{n-P} + 1 \le \tau_{n-P+1} + 1$. With Step 3, $\tau_n < \frac1P \sum_k U_k + 1$. For $n \le P$, all items have $a_k = 0$ and $d_k = Y_k$, so all are in run 1, $\tau_n < 1$, and the same bound holds; the lower bound $\sum_k U_k \le n \tau_n \le P \tau_n$ holds because each of the $n$ items is in memory only on $[0, \tau_n)$. So in all cases, with $S_n = \sum_{k=1}^n U_k$,

$$\frac{S_n}{P} \le \tau_n < \frac{S_n}{P} + 1.$$

**Step 5: from due time to runs.** By the [correctness proof](/replacement-selection/) of replacement selection, the runs are numbered $1, 2, \ldots, R_n$ with no gap, and the last output is in run $R_n$, so $\tau_n = R_n - 1 + x_n$ with $0 \le x_n < 1$. Hence $\tau_n < R_n \le \tau_n + 1$, and with Step 4,

$$\frac{S_n}{P} < R_n < \frac{S_n}{P} + 2.$$

The left inequality is strict with probability 1, and it is strict in expectation. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[S_n] = n/2$, which gives (a). By the strong [law of large numbers](/law-of-large-numbers/), $S_n / n \to 1/2$ with probability 1, so $R_n / n \to 1/(2P)$, which gives (b). $\blacksquare$

## Consequences

- **Half as many runs.** Load, sort and store makes $\lceil n/P \rceil$ runs. Replacement selection with the same memory makes about $n/(2P)$ on random input. For $P = 10$ and $n = 1000$ the theorem gives $50 < \mathbb{E}[R_n] < 52$; the mean over 4000 random inputs is 50.9.
- **The first run is shorter.** At the start, the heap holds $P$ items of run 1 and no item waits for run 2, so the first run is not in the steady state of the snowplow. Knuth's Section 5.4.1 shows that its expected length tends to $(e - 1)P \approx 1.718P$. For $P = 100$, the mean first run over 40 random inputs of $10^5$ items has 172.4 items.
- **Merge passes.** With fan-in $k$, an external merge sort of $r$ runs makes $\lceil \log_k r \rceil$ passes. Halving $r$ saves at most one pass, and exactly one when $k = 2$. On tapes, with small $k$, the gain is often a full pass.
- **Space and time are linked.** Step 3 is a law of the form "number in the system equals arrival rate times time in the system". The memory is the number in the system, one item arrives per output, and the mean time in the system is $1/2$ of a run.

## Tightness

- **The factor 2 is exact.** Part (b) gives the limit $2P$, and the additive error in part (a) is less than 2 runs for all $n$ and $P$.
- **Random order is needed.** The theorem is about average inputs. A reversed input gives runs of exactly $P$ items, except the last, which is the worst case: each run except the last has at least $P$ items. A sorted input gives one run.
- **Continuity is needed.** With equal keys, Step 2 fails: an item equal to the last output joins the current run, so $U_k = 0$ has a positive probability. If all keys are equal, there is one run, far fewer than $n/(2P)$.
- **Larger runs need other methods.** Natural selection, which sends the items for the next run to a reservoir, makes longer runs than $2P$ on random input, at the cost of extra I/O. Knuth's Section 5.4.1 analyzes it.

## History

Knuth's Section 5.4.1 gives the snowplow picture for the run length $2P$ of replacement selection and the limit $(e - 1)P$ for the first run, with the history of both results. The proof on this page replaces the steady-state picture of the snowplow by an exact count of the time that each item spends in memory, which gives the bounds for each $n$ and not only in the limit.

## References
