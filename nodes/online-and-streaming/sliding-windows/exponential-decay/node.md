---
tag: PZMNKF
kind: concept
slug: exponential-decay
name: Exponential decay
aliases:
- time-decayed aggregation
- exponentially decaying window
- decaying window
area: online-and-streaming/sliding-windows
level: core
summary: Weighting a stream item of age a by e^(-lambda a) instead of cutting it off at a window edge, so decayed counts and sums need one number each and one multiplication per update.
prereqs: [sliding-window-model, exponential-moving-average]
see_also: [forward-decay, exponential-moving-average, moving-average, sliding-window-model, landmark-window, mergeable-summaries, exponential-histogram]
sources:
  - paper: "Edith Cohen and Martin J. Strauss, Maintaining time-decaying stream aggregates, Journal of Algorithms 59(1), 2006"
    locator: pages 19 to 36, decay functions in general, exponential decay with a single counter, and polynomial decay
  - url: http://www.mmds.org/
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets
    locator: Chapter 4, Section 4.7, decaying windows and the most popular elements
  - paper: doi:10.1109/ICDE.2009.65
    title: Graham Cormode, Vladislav Shkapenyuk, Divesh Srivastava and Bojian Xu, Forward decay, a practical time decay model for streaming systems, ICDE 2009
    locator: pages 138 to 149, backward decay and the cost of rescaling summaries
---

Exponential decay gives an item that arrived at time $t_i$ the weight $e^{-\lambda (t - t_i)}$ at a later time $t$, with a decay rate $\lambda > 0$, so recent items count fully and old items fade smoothly instead of leaving a window at a fixed age. The decayed count $C(t) = \sum_i e^{-\lambda (t - t_i)}$ and the decayed sum $S(t) = \sum_i x_i e^{-\lambda (t - t_i)}$ each need one stored number, because moving from time $t$ to $t'$ multiplies every weight by the same factor $e^{-\lambda (t' - t)}$. Exponential weights are the only decay with this property, which is why they are the default in streaming systems.

## In plain words

A sliding window treats a reading as fully important until it is a minute old, and then as worthless. Exponential decay softens that edge: a reading loses a fixed fraction of its importance in every second, so after one half-life it counts half, after two half-lives a quarter, and so on. The useful part is that all readings fade at the same rate. So you never need to remember the readings one by one: you keep one running total, shrink it by the right factor whenever time passes, and add each new reading at full weight.

## The idea

**Weights.** Fix a decay rate $\lambda > 0$. The weight of item $i$ at time $t \ge t_i$ is $w_i(t) = e^{-\lambda (t - t_i)}$, which is 1 on arrival and halves every **half-life** $h = \ln 2 / \lambda$. Time can be real, such as seconds, or a count of steps. In discrete steps it is common to write the factor per step as $\beta = e^{-\lambda}$ or as $1 - c$ for a small constant $c$, as in Mining of Massive Datasets.

**Decayed aggregates.** For items $(t_i, x_i)$ with $t_i \le t$:

$$C(t) = \sum_i e^{-\lambda (t - t_i)}, \qquad S(t) = \sum_i x_i\, e^{-\lambda (t - t_i)}, \qquad A = \frac{S(t)}{C(t)}.$$

$C$ is the decayed count, $S$ the decayed sum, and $A$ the decayed average. The common factor cancels in $A$, so the decayed average changes only when an item arrives, not while time passes.

**Update.** Store the pair $(C, \tau)$, the count scaled to the time $\tau$ of the last update. For a new item at time $t' \ge \tau$, or a query at $t'$:

$$C(t') = e^{-\lambda (t' - \tau)}\, C(\tau) + (\text{number of new items at } t').$$

This holds because $e^{-\lambda (t' - t_i)} = e^{-\lambda (t' - \tau)} e^{-\lambda (\tau - t_i)}$ for every old item. The same update works for $S$, for sums of squares, and for any linear statistic. Each update costs one exponential, one multiplication and one addition, and the memory is one number per statistic. Two summaries of disjoint item sets are **merged** by scaling both to the later of their two times and adding, which makes them [mergeable](/mergeable-summaries/) across machines.

**Effective window.** For one item per unit of time, $C(t)$ tends to $1/(1 - e^{-\lambda}) \approx 1/\lambda + 1/2$, so a decay rate $\lambda$ acts like a window of about $1/\lambda$ items. For steps of 1, the decayed average is exactly the bias-corrected [exponential moving average](/exponential-moving-average/) with $1 - \alpha = e^{-\lambda}$, because both are $\sum_j \beta^j x_{t-j} / \sum_j \beta^j$.

**Why exponential.** Suppose a decay function $f$, with weight $f(t - t_i)$, allows the update of a decayed count from time $\tau$ to $\tau + \Delta$ by one factor $h(\Delta)$ that does not depend on the items. Then $f(a + \Delta) = h(\Delta) f(a)$ for all ages $a, \Delta \ge 0$, and with $f(0) = 1$ this gives $f(a + \Delta) = f(a) f(\Delta)$. A positive monotone solution of this equation is $f(a) = e^{-\lambda a}$: $\ln f$ is additive and monotone, so it is linear. Other decay functions need more memory. For a sliding window, the step function, an exact count needs $\Omega(W)$ bits; for polynomial decay $f(a) = (1 + a)^{-k}$, Cohen and Strauss (2006) give approximate decayed counts with memory that grows with the logarithm of the stream length, built on sliding-window structures such as the [exponential histogram](/exponential-histogram/).

**Summaries with many counters.** For decayed counts of many keys, such as the most popular items of a stream, the update multiplies every counter by the factor, which costs time linear in the number of counters at every step. Mining of Massive Datasets uses this form with a factor $1 - c$ and drops counters that fall below $1/2$. Keeping one global scale factor avoids the rescaling, and this is exactly [forward decay](/forward-decay/) with $g(n) = e^{\lambda n}$: each counter stores its weights at arrival, and the global factor is applied only at a query.

**Numerics.** The stored values shrink over time and never overflow; after a long idle gap they underflow to 0, which is the correct limit. A forward-decay form with growing weights needs the opposite care, as described on its page.

## Examples

Take the half-life $h = 1$, so $\lambda = \ln 2$ and the factor per time unit is $1/2$. The items are (time, value): $(0, 4), (1, 8), (1, 6), (3, 2)$.

| event | factor since last update | $C$ after | $S$ after |
|---|---|---|---|
| add $(0, 4)$ | | 1 | 4 |
| add $(1, 8)$ | $1/2$ | $1/2 + 1 = 3/2$ | $2 + 8 = 10$ |
| add $(1, 6)$ | 1 | $5/2$ | 16 |
| add $(3, 2)$ | $1/4$ | $5/8 + 1 = 13/8$ | $4 + 2 = 6$ |
| query at $t = 5$ | $1/4$ | $13/32$ | $3/2$ |

The decayed average at $t = 3$ is $6 / (13/8) = 48/13 \approx 3.69$, and the query at $t = 5$ gives the same average, $(3/2)/(13/32) = 48/13$. A direct check at $t = 3$: the weights are $1/8, 1/4, 1/4, 1$, so $C = 13/8$ and $S = 4/8 + 8/4 + 6/4 + 2 = 6$.

## Where it is used

- **Monitoring and rates.** Decayed counts of requests or errors per key estimate recent rates without a buffer; the Unix load average and many metrics libraries use exponential decay over real time.
- **Popular items and trends.** Decayed counts rank trending search terms, hashtags or products, as in Mining of Massive Datasets, Section 4.7.
- **Network measurement.** Decayed traffic per flow or per prefix detects recent heavy users.
- **Recommendations and caching.** Decayed access counts rank cache entries in policies that mix recency and frequency.
- **Streaming summaries.** Decayed versions of samples, quantiles and heavy hitters are built with [forward decay](/forward-decay/), which gives the same weights with the scale factor applied at query time.

## References
