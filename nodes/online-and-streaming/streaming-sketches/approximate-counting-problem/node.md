---
tag: MXWEG3
kind: problem
slug: approximate-counting-problem
name: Approximate counting problem
aliases:
- approximate counter
- counting with few bits
- approximate event counting
area: online-and-streaming/streaming-sketches
level: intro
summary: Maintain an approximate count of events using far fewer bits than an exact counter.
prereqs: [streaming-model, epsilon-delta-guarantee, space-complexity]
see_also: [morris-counter, cash-register-model, median-trick, distinct-elements-problem, frequency-moment-problem, dgim-algorithm, approximate-counting]
sources:
  - paper: doi:10.1145/359619.359627
    title: Robert Morris, Counting large numbers of events in small registers, Communications of the ACM 21(10), 1978
    locator: pp. 840 to 842
  - paper: doi:10.1007/BF01934993
    title: Philippe Flajolet, Approximate counting, a detailed analysis, BIT 25(1), 1985
    locator: pp. 113 to 134
  - paper: doi:10.1145/3517804.3526225
    title: Jelani Nelson and Huacheng Yu, Optimal bounds for approximate counting, PODS 2022
    locator: pp. 119 to 127 (the upper bound and the matching lower bound)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 2, Section 2.1, Morris Approximate Counter
---

The approximate counting problem asks for a counter that counts up to $n$ events in $o(\log n)$ bits. An exact counter needs $\lceil \log_2(n+1) \rceil$ bits, and so does each deterministic counter with a constant relative error, up to an additive constant. A randomized counter can do much better: the [Morris counter](/morris-counter/) uses $O(\log\log n)$ bits for a constant error, and the optimal space is $\Theta(\log\log n + \log(1/\varepsilon) + \log\log(1/\delta))$ bits (Nelson and Yu 2022). On this page $n$ is the number of events so far, and the stream holds only increments, with no item names. This is not the counting problem of [approximate counting](/approximate-counting/) in combinatorics, which counts the solutions of a #P problem.

## In plain words

You want to count how often something happens, and the count can get very large. You also need to keep very many such counts at the same time, so each one must be tiny. A normal counter has to hold every possible number up to the final count. If you only need the count to within ten percent, you can store much less: in effect, only how many digits the count has, with a little more detail. A machine that follows fixed rules cannot do this, because it would lose track of where it is. A machine that flips coins can. It moves its small number up only now and then, at random, so that on average it keeps pace with the true count.

## Definition

A counter has a state that changes at each event, and a query that maps the state to a number $\hat n$. The input is a sequence of $n$ events, and $n$ is not known in advance. The counter must answer the query after each event.

**Approximate counting.** Given $\varepsilon \in (0, 1)$ and $\delta \in (0, 1)$, after each number $n$ of events,
$$\Pr\big[\,|\hat n - n| \le \varepsilon n\,\big] \ge 1 - \delta.$$
This is the relative form of the [(ε, δ) guarantee](/epsilon-delta-guarantee/). The cost is the number of bits of the state, as a function of $n$, $\varepsilon$ and $\delta$. The random bits that are used once and thrown away are not stored, so they do not count as space.

The problem is a special case of the [streaming model](/streaming-model/): in the [cash register model](/cash-register-model/) with unit updates to one item, the count is $n = \|f\|_1$.

## Variants

- **Deterministic or randomized.** With a deterministic counter the error must hold for each $n$. With a randomized counter it holds with probability $1 - \delta$ for each fixed $n$.
- **For each time or for all times.** The usual guarantee is for each $n$ separately. A guarantee for all $n \le N$ at the same time costs more; with a union bound over the $O(\log_{1+\varepsilon} N)$ scales it is not much more.
- **Additive error.** If the final count is at most a known $N$, the error can be $\varepsilon N$. Keep each event with probability $p = 1/(\varepsilon^2 N)$ and count the kept events $C$. The estimate $C/p$ has standard deviation at most $\sqrt{N/p} = \varepsilon N$, and $C$ is about $1/\varepsilon^2$, so it needs $O(\log(1/\varepsilon))$ bits. A deterministic counter still needs about $\log_2 N$ bits, by the argument of the Bounds section. A relative error is the harder and more common goal.
- **Weighted increments.** Each event adds a positive weight. Morris type counters handle this with a skip by a geometric gap.
- **Many counters.** Keep one counter for each of many keys. This is where the saving matters.
- **Windows.** Count only the events of the last $W$ time steps. This is the [sliding window](/sliding-window-model/) problem of the [DGIM algorithm](/dgim-algorithm/).
- **Distinct events.** Count the number of different items, not the number of events. This is the [distinct elements problem](/distinct-elements-problem/).

## Examples

| events $n$ | exact counter | $\log_2 n$, about the Morris register | bits for the register |
|---|---|---|---|
| 1000 | 10 | 10 | 4 |
| $10^6$ | 20 | 20 | 5 |
| $10^9$ | 30 | 30 | 5 |
| $10^{18}$ | 60 | 60 | 6 |

A base 2 Morris counter for $10^9$ events thus needs 5 or 6 bits, against 30 for an exact counter. One such counter has a relative standard deviation near $1/\sqrt 2$, so to get within 10 percent with probability 0.9 you average many copies: about 135 by the normal approximation, or 500 by the Chebyshev bound. A smaller base is cheaper. Morris(a) with $a = 0.0074$ has a relative standard deviation of about $\sqrt{a/2} \approx 0.061$, and its register for $10^9$ events is near $\ln(an)/\ln(1+a) \approx 2145$, which needs 12 bits.

## Known algorithms

- **[Morris counter](/morris-counter/)** (Morris 1978). Raise a register $X$ with probability $2^{-X}$, and return $2^X - 1$. Unbiased, with variance $n(n-1)/2$. The base change Morris(a), the mean of copies (Morris+) and the median of means (Morris++) give any $(\varepsilon, \delta)$.
- **Flajolet's analysis** (1985). The exact distribution of the register and its asymptotic moments.
- **Nelson and Yu** (2022). A Morris(a) counter with a small change, with the optimal space.

## Bounds

**Exact counting.** Any counter that answers exactly must be in a different state after $0, 1, \ldots, n$ events, so it needs $\lceil\log_2(n+1)\rceil$ bits.

**Deterministic counting with relative error (proved here).** Let $\varepsilon < 1$, and let a deterministic counter with $S$ states give a value within $\varepsilon k$ of $k$ for each $k \le N$. Then $S > (1-\varepsilon)N/2$, so the counter needs at least $\log_2 N - 1 - \log_2(1/(1-\varepsilon))$ bits.

*Proof.* The state after $k$ events is $s_k = T(s_{k-1})$ for a fixed map $T$. Among $s_0, \ldots, s_S$ two states are equal, say $s_i = s_j$ with $i < j \le S$. Then $s_{i + r(j-i)} = s_i$ for each $r \ge 0$. Let $N'$ be the largest number of the form $i + r(j - i)$ that is at most $N$; then $N' > N - S$. The counter gives the same value $y$ after $i$ and after $N'$ events, so $y \le (1+\varepsilon)i \le (1+\varepsilon)S$ and $y \ge (1-\varepsilon)N' > (1-\varepsilon)(N-S)$. Both hold only if $N < 2S/(1-\varepsilon)$. $\square$

**Randomized counting (cited).** The Morris(a) counter gives $O(\log\log n + \log(1/\varepsilon) + \log(1/\delta))$ bits; the proof is on the [Morris counter](/morris-counter/) page. Nelson and Yu (2022) prove that $\Theta(\log\log n + \log(1/\varepsilon) + \log\log(1/\delta))$ bits are necessary and sufficient, for the guarantee at a fixed $n$.

**Why $\log\log n$.** A counter with $S$ states and constant error must at least tell apart counts that differ by a constant factor. There are $\Theta(\log n)$ such scales up to $n$, so $S$ grows with $\log n$, and the state has $\Omega(\log\log n)$ bits. This intuition is not a proof against randomized counters; the cited lower bound is.

## Reductions

- **Counting is $F_1$ in the cash register model.** With only increments, the count of events is the first [frequency moment](/frequency-moment-problem/) $F_1 = \|f\|_1$. Under deletions, an exact $F_1$ needs a full counter.
- **Counters inside sketches.** A sketch that holds many counters, such as a [count-min sketch](/count-min-sketch/), can store each counter as a Morris counter, at the price of more error.
- **The median trick.** The step from a constant success probability to $1 - \delta$ is the general [median trick](/median-trick/).

## Applications

- Per-flow and per-key counters in network devices, where memory per counter is small and the counts are large.
- Statistics in databases and storage systems, for example access counts used to choose what to keep in a cache.
- Counts of words and word sequences in large text collections.
- Teaching: the Morris counter is the standard first example of a streaming algorithm with a proof of unbiasedness.

## References
