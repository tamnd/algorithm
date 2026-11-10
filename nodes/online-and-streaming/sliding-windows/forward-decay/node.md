---
tag: SAPQHG
kind: concept
slug: forward-decay
name: Forward decay
aliases:
- forward-decayed aggregation
- landmark-based decay
area: online-and-streaming/sliding-windows
level: research
summary: A decay model with weights g(t_i - L)/g(t - L) for a landmark L, so item weights are fixed at arrival and one divisor is applied at query time; g(n) = e^(lambda n) gives exponential decay.
prereqs: [exponential-decay, landmark-window]
see_also: [exponential-decay, exponential-moving-average, landmark-window, weighted-reservoir-sampling, priority-sampling, space-saving, count-min-sketch, mergeable-summaries]
sources:
  - paper: doi:10.1109/ICDE.2009.65
    title: Graham Cormode, Vladislav Shkapenyuk, Divesh Srivastava and Bojian Xu, Forward decay, a practical time decay model for streaming systems, ICDE 2009
    locator: pages 138 to 149, the definition with a landmark and the function g, the equivalence with backward exponential decay, decayed aggregates, sampling and heavy hitters, and the numerical handling of exponential g
  - paper: "Edith Cohen and Martin J. Strauss, Maintaining time-decaying stream aggregates, Journal of Algorithms 59(1), 2006"
    locator: pages 19 to 36, backward decay functions defined by the age of an item
---

Forward decay, introduced by Cormode, Shkapenyuk, Srivastava and Xu (2009), weights an item that arrived at time $t_i$ by $g(t_i - L)/g(t - L)$ at query time $t$, where $L$ is a fixed landmark before all items and $g$ is a positive non-decreasing function. The numerator is fixed when the item arrives and the divisor is common to all items, so any summary that accepts weighted items, such as a sum, a sample or a heavy-hitter sketch, becomes a decayed summary by giving each item the weight $g(t_i - L)$. With $g(n) = e^{\lambda n}$ the weights are exactly those of [exponential decay](/exponential-decay/), and exponential $g$ is the only choice for which the weight depends on the age of the item alone.

## In plain words

Usual decay looks backward: at every moment, each old item has lost some weight because of its age, and the stored totals must be shrunk as time passes. Forward decay turns this around. It picks a fixed starting point in the past and gives each new item a weight that grows with how late it arrived. A later item gets a bigger weight, so older items count less by comparison, and nothing stored ever needs to change. Only when someone asks for an answer is the total divided by one number for the current time. With weights that grow exponentially, the answers are exactly those of exponential decay.

## The idea

**Definition.** Fix a landmark $L$ with $L < t_i$ for every item, and a function $g$ that is positive and non-decreasing for $n > 0$. When $g(0) > 0$, as for exponential $g$, items at time $L$ are allowed too. The weight of item $i$ at time $t \ge t_i$ is

$$w_i(t) = \frac{g(t_i - L)}{g(t - L)}.$$

Then $w_i(t_i) = 1$, $0 \le w_i(t) \le 1$, and $w_i(t)$ does not increase as $t$ grows, so it is a decay. The ratio $w_i(t)/w_j(t) = g(t_i - L)/g(t_j - L)$ of two items does not depend on $t$: the relative weights are fixed at arrival.

**Aggregates.** Keep the numerators $N_C = \sum_i g(t_i - L)$ and $N_S = \sum_i g(t_i - L)\, x_i$. Then

$$C(t) = \frac{N_C}{g(t - L)}, \qquad S(t) = \frac{N_S}{g(t - L)}, \qquad A = \frac{N_S}{N_C}.$$

An insert adds to the numerators and never rescales. The decayed average does not depend on $t$. The decayed maximum is $\max_i g(t_i - L) x_i / g(t - L)$, with one stored number. Two summaries with the same $g$ and the same landmark **merge** by adding their numerators, and any weighted summary merges as it does without decay.

**Summaries.** Because the weights are fixed at arrival, a weighted summary built on the weights $g(t_i - L)$ gives a decayed summary:

- a decayed sample from [weighted reservoir sampling](/weighted-reservoir-sampling/) or [priority sampling](/priority-sampling/), where the probabilities depend only on the relative weights;
- decayed heavy hitters from a weighted [Space-Saving](/space-saving/) summary or a [count-min sketch](/count-min-sketch/) that adds $g(t_i - L)$ instead of 1, with all counts divided by $g(t - L)$ at the query;
- decayed quantiles from a weighted quantile summary.

With backward decay each of these would need every stored counter to be rescaled as time passes, or would not work at all, because the order of the weights of stored items would have to be recomputed.

**Equivalence with exponential decay.** *Claim.* For $g(n) = e^{\lambda n}$ with $\lambda > 0$, $w_i(t) = e^{-\lambda (t - t_i)}$ for every landmark $L$. *Proof.* $w_i(t) = e^{\lambda (t_i - L)} / e^{\lambda (t - L)} = e^{\lambda (t_i - L) - \lambda (t - L)} = e^{-\lambda (t - t_i)}$. $\square$ So every forward-decayed aggregate with this $g$ is the backward exponentially decayed aggregate, and the choice of $L$ does not change any answer.

*Converse.* Suppose that $g$ is non-decreasing and positive on $n \ge 0$, and that $w_i(t)$ depends only on the age $t - t_i$ for every landmark, that is, $g(a + \Delta)/g(a) = h(\Delta)$ for all $a, \Delta \ge 0$. Setting $a = 0$ gives $g(\Delta) = g(0)\, h(\Delta)$, so $h(a + \Delta) = h(a) h(\Delta)$ with $h(0) = 1$. The function $\ln h$ is additive and monotone, so it is linear, $h(\Delta) = e^{\lambda \Delta}$, and $g(n) = g(0) e^{\lambda n}$. A constant factor $g(0)$ cancels in every weight. So exponential functions are the only $g$ for which forward decay is a decay by age alone. For any other $g$, such as the polynomial $g(n) = n^k$, the weight of an item depends on its arrival time relative to $L$, not only on its age: two items of age 2 at different times have different weights.

**Polynomial forward decay.** With $g(n) = n^k$, the weight $((t_i - L)/(t - L))^k$ falls slowly, and an item keeps a fixed share relative to its neighbours. This is a cheap substitute for backward polynomial decay $(1 + t - t_i)^{-k}$, which has no small exact summary.

**The landmark and numerics.** For exponential $g$, the numerators $e^{\lambda (t_i - L)}$ grow without bound, and in binary64 they overflow once $\lambda (t_i - L)$ passes about 709. The landmark can be moved forward: with a new landmark $L'$, multiply every stored numerator by $e^{-\lambda (L' - L)}$. Since $e^{\lambda (t_i - L)} e^{-\lambda (L' - L)} = e^{\lambda (t_i - L')}$, this gives exactly the numerators for $L'$, and by the equivalence above no answer changes. It costs one pass over the stored numbers, done rarely, for example when the exponent passes a threshold. Another option is to store the logarithms of the numerators. For polynomial $g$ the numerators grow only polynomially, and the landmark can stay fixed.

## Examples

Take the items (time, value): $(0, 4), (1, 8), (1, 6), (3, 2)$.

**Exponential.** $g(n) = 2^n$ and $L = 0$. The numerators are $N_C = 1 + 2 + 2 + 8 = 13$ and $N_S = 4 + 16 + 12 + 16 = 48$. At $t = 3$, dividing by $g(3) = 8$ gives $C = 13/8$ and $S = 6$, the same values as backward decay with half-life 1 on the [exponential decay page](/exponential-decay/), and the average is $48/13$. Moving the landmark to $L' = 3$ multiplies both numerators by $2^{-3}$, which gives $13/8$ and $6$, and the divisor becomes $g(0) = 1$, so every answer is unchanged.

**Polynomial.** $g(n) = n^2$ and $L = -1$. The numerators of the counts are $1, 4, 4, 16$, so $N_C = 25$. At $t = 3$ the divisor is $16$ and the weights are $1/16, 1/4, 1/4, 1$. At $t = 7$ the divisor is $64$ and the weights are $1/64, 1/16, 1/16, 1/4$. Every weight has dropped by the same factor 4, while backward exponential decay with half-life 1 would have dropped them by 16.

## Where it is used

- **Stream processing systems.** The paper implements forward-decayed aggregates in a network monitoring system with little overhead over undecayed queries, because each item only needs one extra weight computation.
- **Decayed sampling and heavy hitters.** Weighted samplers and frequency sketches gain time decay without new algorithms.
- **Distributed aggregation.** Summaries from different machines with a shared landmark merge by addition, which suits [mergeable summaries](/mergeable-summaries/).
- **Relation to other models.** It sits between the [landmark window](/landmark-window/), which weights every item after $L$ equally, and backward [exponential decay](/exponential-decay/), which it equals for exponential $g$. The [exponential moving average](/exponential-moving-average/) is the special case of unit time steps.

## References
