---
tag: RTYVEA
kind: concept
slug: hopping-window
name: Hopping window
aliases:
- jumping window
- sliding window with a slide period
- overlapping fixed-size window
area: online-and-streaming/sliding-windows
level: intro
summary: Windows of size s that start every h time units, [o + jh, o + jh + s); with h < s they overlap and each item is in about s/h windows.
prereqs: [tumbling-window, time-based-window]
see_also: [tumbling-window, session-window, landmark-window, time-based-window, sliding-window-model, sliding-window-aggregation, two-stacks-queue, moving-average]
sources:
  - paper: doi:10.14778/2824032.2824076
    title: Tyler Akidau et al., The Dataflow Model, a practical approach to balancing correctness, latency, and cost in massive-scale, unbounded, out-of-order data processing, PVLDB 8(12), 2015
    locator: Section 1.2 (sliding windows with a size and a period) and Section 2.2.1 (window assignment, the example Sliding(2m, 1m))
  - paper: doi:10.1007/s00778-022-00778-6
    title: Juliane Verwiebe, Philipp M. Grulich, Jonas Traub and Volker Markl, Survey of window types for aggregation in stream processing systems, The VLDB Journal 32, 2023
    locator: the section on sliding (hopping) windows among the window types
  - url: https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/
    title: Apache Flink documentation, Windows
    locator: Window Assigners, Sliding Windows (size, slide and offset)
---

A hopping window of size $s$ and hop $h$ is one of the windows $[o + jh, o + jh + s)$ on the time axis, for all integers $j$: a new window starts every $h$ time units and each window lasts $s$ time units. When $h < s$ the windows overlap, and each item belongs to $\lfloor s/h \rfloor$ or $\lceil s/h \rceil$ of them. Kafka Streams calls these hopping windows; the Dataflow model of Akidau et al. (2015) and Apache Flink call them sliding windows, with a size and a period (or slide). On this page an item of the stream $\sigma$ is a pair $(\tau, v)$, $s > 0$ is the size, $h > 0$ is the hop and $o$ is the offset.

## In plain words

Think of a report of the last hour that is made every 15 minutes. Each report covers one hour, and two reports in a row share 45 minutes. An item that happened at some moment appears in each report whose hour contains that moment, which is four reports here. If the step between reports equals the length of a report, the reports do not overlap, and you get tumbling windows. If the step is longer than a report, some items fall between the reports and appear in none.

## The idea

The windows are $H_j = [\,o + jh,\; o + jh + s\,)$ for $j \in \mathbb{Z}$. A timestamp $\tau$ is in $H_j$ if and only if $o + jh \le \tau < o + jh + s$, that is, $(\tau - o - s)/h < j \le (\tau - o)/h$.

```pseudo id=main
HOPPING-ASSIGN(τ, s, h, o)              ▷ size s > 0, hop h > 0, offset o
L1  hi ← ⌊(τ − o)/h⌋
L2  lo ← ⌊(τ − o − s)/h⌋ + 1
L3  return the windows [o + jh, o + jh + s) for j = lo, ..., hi

HOPPING-SUMS(σ, s, h, o)                ▷ s and h are integers
L4  g ← gcd(s, h)
L5  P[b] ← sum of the v with o + g⌊(τ − o)/g⌋ = b, for each pane start b
L6  for each window start b = o + jh whose window meets a nonempty pane do
L7      emit (b, b + s, P[b] + P[b + g] + ... + P[b + s − g])
```

**Number of windows of one item.** Let $x = (\tau - o)/h$ and $r = s/h$. Lines L1 and L2 give $\lfloor x \rfloor - \lfloor x - r \rfloor$ windows, the number of integers in the interval $(x - r, x]$ of length $r$. This number is $\lfloor r \rfloor$ or $\lfloor r \rfloor + 1$. It is exactly $r$ when $h$ divides $s$, and then each item is in $s/h$ windows. When $h > s$, some items are in no window.

**Panes.** Let $g = \gcd(s, h)$. The panes are the [tumbling windows](/tumbling-window/) of size $g$ and offset $o$. Each start $o + jh$ and each end $o + jh + s$ is a pane boundary, because $g$ divides $h$ and $s$. So each hopping window is the union of $s/g$ consecutive panes, and an associative aggregate of the window is the combination of $s/g$ pane aggregates (line L7). Each item is added to one pane only, instead of to $\lceil s/h \rceil$ windows. To combine the panes faster than $s/g$ steps per window, keep the panes of the last $s/g$ pane positions in a [sliding-window aggregation](/sliding-window-aggregation/) structure, such as the [two-stacks queue](/two-stacks-queue/), which gives $O(1)$ amortized combines per window.

**Relation to other windows.** With $h = s$ the windows are the tumbling windows of size $s$; Dataflow states that fixed windows are sliding windows with size equal to period. As $h$ goes down to the time unit, the hopping windows end at every time step, and they become the time-based windows of the [sliding window model](/sliding-window-model/), with one answer at each step.

## Examples

- $s = 10$, $h = 5$, $o = 0$. The timestamp 12 has hi $= 2$ and lo $= \lfloor 2/5 \rfloor + 1 = 1$, so it is in $[5, 15)$ and $[10, 20)$. Each item is in exactly 2 windows.
- $s = 10$, $h = 3$, $o = 0$. The timestamp 12 is in $[3, 13)$, $[6, 16)$, $[9, 19)$ and $[12, 22)$: 4 windows, which is $\lceil 10/3 \rceil$. The timestamp 11 is in $[3, 13)$, $[6, 16)$ and $[9, 19)$: 3 windows, which is $\lfloor 10/3 \rfloor$.
- The Dataflow example: with a size of 2 minutes and a period of 1 minute, an item at 12:00 is in $[11{:}59, 12{:}01)$ and $[12{:}00, 12{:}02)$.
- $s = 6$, $h = 4$: then $g = 2$, the panes are $[0, 2), [2, 4), \ldots$, and the window $[4, 10)$ is the union of the panes $[4, 6)$, $[6, 8)$ and $[8, 10)$.

## Where it is used

- Stream processing systems: sliding windows in Dataflow, Apache Beam and Apache Flink, and hopping windows in Kafka Streams. In Kafka Streams and Flink the windows are half-open, $[\text{start}, \text{end})$, and aligned to the epoch.
- Dashboards and alerts that show a statistic of the last period and refresh it at a shorter step, such as the [moving average](/moving-average/) of the last hour every minute.
- A hopping window is a cheap approximation of a true sliding window: it answers every $h$ time units instead of at every step, and the answer is late by at most $h$.

## References
