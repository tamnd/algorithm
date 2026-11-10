---
tag: PRESKG
kind: model
slug: streaming-model
name: Streaming model
aliases:
- data stream model
- one-pass streaming model
- streaming algorithm
- data streaming
area: online-and-streaming/streaming-sketches
level: intro
summary: Input arrives as a sequence read once, with memory sublinear in the stream length.
prereqs: [asymptotic-notation, word-ram, space-complexity]
see_also: [cash-register-model, turnstile-model, frequency-vector, epsilon-delta-guarantee, linear-sketch, mergeable-summaries, sliding-window-model, one-way-communication-complexity]
sources:
  - paper: doi:10.1561/0400000002
    title: S. Muthukrishnan, Data Streams, Algorithms and Applications, Foundations and Trends in Theoretical Computer Science 1(2), 2005
    locator: Chapter Data Streaming, Formal Aspects, section Data Stream Models (time series, cash register and turnstile)
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999
    locator: pp. 137 to 147 (frequency moments in one pass, and the lower bounds by communication complexity)
  - paper: doi:10.1016/0304-3975(80)90061-4
    title: J. Ian Munro and Mike S. Paterson, Selection and sorting with limited storage, Theoretical Computer Science 12(3), 1980
    locator: pp. 315 to 323 (selection in few passes with small memory)
  - paper: doi:10.1016/0022-0000(85)90041-8
    title: Philippe Flajolet and G. Nigel Martin, Probabilistic counting algorithms for data base applications, Journal of Computer and System Sciences 31(2), 1985
    locator: pp. 182 to 209
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 1, Introduction (models and the summaries of this site), and Chapter 10, Lower Bounds
---

The streaming model is a model of computation for inputs that are too large to store. The input is a sequence $\sigma = (a_1, a_2, \ldots, a_m)$ of $m$ items from a universe $[n] = \{1, \ldots, n\}$. The algorithm reads the items one at a time, in order, in one pass, and it has a memory much smaller than the input: the goal is a space that is sublinear in both $m$ and $n$, and best of all polylogarithmic, $O(\mathrm{polylog}(m, n))$ bits. Most exact answers are impossible in such space, so streaming algorithms are randomized and approximate, with an [(ε, δ) guarantee](/epsilon-delta-guarantee/). On the pages of this site $m$ is the stream length and $n$ is the universe size, unless a page says otherwise.

## The machine

A streaming algorithm is a machine with a memory of $s$ bits and three parts.

1. **Initialization.** Set the memory to a start state. A randomized algorithm also draws its random seeds here, for example the seeds of its hash functions.
2. **Update.** For $j = 1, 2, \ldots, m$, read the item $a_j$ and change the memory. The item is then gone: the algorithm cannot read it again.
3. **Query.** At the end, or at any time if the algorithm is online, compute an answer from the memory.

Inside each step the machine is a [word RAM](/word-ram/) with words of $\Theta(\log(m + n))$ bits, so an item or a count fits in $O(1)$ words. The algorithm does not know $m$ in advance unless the problem says so.

The items can take several forms. In the simplest form each item is an element of $[n]$, and the stream defines the [frequency vector](/frequency-vector/) $f \in \mathbb{Z}^n$ with $f_i$ the number of times item $i$ occurs. In the general form each item is an update $(i, \Delta)$ that adds $\Delta$ to $f_i$. The rules on $\Delta$ give the update models:

| model | updates | invariant |
|---|---|---|
| [cash register](/cash-register-model/) | $\Delta > 0$ (often $\Delta = 1$) | $f$ only grows |
| strict [turnstile](/turnstile-model/) | $\Delta$ of either sign | $f_i \ge 0$ at all times |
| general [turnstile](/turnstile-model/) | $\Delta$ of either sign | none |

Muthukrishnan (2005) also names the time series model, where $a_j$ is the value $f_j$ itself, given in order of $j$.

**Randomness.** A randomized algorithm uses random bits. On this site the random bits that the algorithm must keep, such as hash seeds, count as space. Random bits used once and thrown away, such as the coin of a [Morris counter](/morris-counter/), do not. Some papers assume a free random oracle, which hides the cost of a fully random hash function; a page that does this says so.

## What it counts

- **Space.** The number of bits of memory, as a function of $m$, $n$, $\varepsilon$ and $\delta$. This is the main cost. A bound in words is a bound in bits times $\log(m + n)$; each page says which unit it uses.
- **Passes.** The number of times the algorithm reads the stream. The default is one pass. Multi-pass algorithms appear for problems such as selection (Munro and Paterson 1980).
- **Update time.** The time to process one item, worst case or amortized.
- **Query time.** The time to compute the answer from the memory. It is given apart from the update time, because some sketches have a cheap update and a costly query, or the opposite.
- **Error and failure probability.** The accuracy $\varepsilon$ and the failure probability $\delta$ of the answer.

## Relation to other models

- **Communication complexity.** A one-pass streaming algorithm with $s$ bits of memory gives a [one-way](/one-way-communication-complexity/) protocol with an $s$-bit message: Alice runs the algorithm on the first part of the stream and sends the memory to Bob, who runs it on the rest. So a lower bound of $c$ bits for the one-way communication of a problem is a lower bound of $c$ bits on the memory of each streaming algorithm for the stream form of that problem. With $p$ passes the same argument gives $p$ rounds and $(2p - 1)s$ bits in total. The problems used most are [INDEX](/index-problem/), [DISJ](/disjointness-problem/) and [GAP-HAMMING](/gap-hamming-distance/); see the page on the [INDEX lower bound](/index-problem-lower-bound/).
- **Online algorithms.** An [online algorithm](/online-algorithm/) also sees the input one item at a time, but it must make a decision for each item and is judged by its [competitive ratio](/competitive-ratio/), not by its memory. A streaming algorithm makes no decisions before the query; its constraint is the memory.
- **External memory.** The [external memory model](/external-memory-model/) also has a small fast memory and a large input, but it can read the input many times and in any order, and it counts block transfers.
- **Sliding windows.** In the [sliding window model](/sliding-window-model/) the query is about the last $W$ items only, so old items expire.
- **Graph streams.** When the items are the edges of a graph on $n$ vertices, many problems need $\Omega(n)$ bits, and the usual goal is $O(n \,\mathrm{polylog}\, n)$ bits, the semi-streaming setting. See [stream connectivity](/stream-connectivity-problem/) and the [AGM sketch](/agm-graph-sketch/).
- **Summaries and sketches.** Many streaming algorithms keep a [linear sketch](/linear-sketch/) or a [mergeable summary](/mergeable-summaries/). These also work when the data is split across machines.

## Known results in the model

**Proved here: the reduction to one-way communication.** Let $A$ be a one-pass algorithm with $s$ bits of memory that computes $g(\sigma_1 \sigma_2)$ with probability $1 - \delta$, where $\sigma_1\sigma_2$ is the concatenation. Alice, who holds $\sigma_1$, runs $A$ on $\sigma_1$ with public random bits and sends the $s$-bit memory. Bob, who holds $\sigma_2$, starts $A$ from that memory, runs it on $\sigma_2$, and outputs the query. The output has the same distribution as the output of $A$ on $\sigma_1\sigma_2$, so the protocol is correct with probability $1 - \delta$ and uses $s$ bits. $\square$

The other results in this table are cited, and proved on the linked pages.

| problem | model | space | page |
|---|---|---|---|
| count the events, $(1 \pm \varepsilon)$ | cash register | $\Theta(\log\log m + \log(1/\varepsilon) + \log\log(1/\delta))$ bits | [Morris counter](/morris-counter/) |
| distinct items $F_0$, exact | cash register | $\Omega(n)$ bits, randomized | [distinct elements](/distinct-elements-problem/) |
| distinct items $F_0$, $(1 \pm \varepsilon)$, constant $\delta$ | cash register | $\Theta(\varepsilon^{-2} + \log n)$ bits | [distinct elements](/distinct-elements-problem/) |
| second moment $F_2$, $(1 \pm \varepsilon)$ | turnstile | $O(\varepsilon^{-2}\log(1/\delta))$ words | [AMS sketch](/ams-sketch/) |
| moments $F_p$ for $p > 2$ | turnstile | $n^{1 - 2/p}$ up to polylog factors | [frequency moments](/frequency-moment-problem/), [lower bounds](/frequency-moment-lower-bounds/) |
| heavy hitters with error $\varepsilon m$ | cash register | $O(1/\varepsilon)$ counters, deterministic | [Misra-Gries](/misra-gries-summary/) |
| point queries with error $\varepsilon \|f\|_1$ | turnstile | $O(\varepsilon^{-1}\log(1/\delta))$ counters | [count-min sketch](/count-min-sketch/) |
| quantiles with rank error $\varepsilon m$ | cash register | $O(\varepsilon^{-1}\log(\varepsilon m))$ words, deterministic | [Greenwald-Khanna](/greenwald-khanna-summary/) |
| majority element, if one exists | cash register | 2 words | [Boyer-Moore](/boyer-moore-majority/) |
| sample one nonzero coordinate | turnstile | $O(\log^2 n \log(1/\delta))$ bits | [L0 sampler](/l0-sampler/) |

Two simple facts show why approximation and randomness are needed. An exact count of distinct items, by a deterministic algorithm, needs about $n$ bits, because the memory must tell apart all the sets of items seen so far (proof on the [distinct elements](/distinct-elements-problem/) page). A deterministic counter of $m$ events with constant relative error needs about $\log_2 m$ bits, while a randomized one needs only $O(\log\log m)$ (proof on the [approximate counting](/approximate-counting-problem/) page).

## References
