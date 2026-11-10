---
tag: G9PD69
kind: concept
slug: exponential-moving-average
name: Exponential moving average
aliases:
- EMA
- EWMA
- Exponentially weighted moving average
- exponentially weighted moving average
- exponential smoothing
area: online-and-streaming/sliding-windows
level: intro
summary: "The average s_t = a x_t + (1 - a) s_(t-1), which gives the item of age j the weight a(1 - a)^j; it needs O(1) memory, matches a W-item window at a = 2/(W + 1), and has a bias correction."
prereqs: [moving-average, geometric-series]
see_also: [moving-average, exponential-decay, forward-decay, iir-filter, adam, round-trip-time-estimation, sliding-window-aggregation]
sources:
  - paper: "S. W. Roberts, Control chart tests based on geometric moving averages, Technometrics 1(3), 1959"
    locator: pages 239 to 250, the geometric moving average chart with weights r(1 - r)^j
  - paper: "J. Stuart Hunter, The exponentially weighted moving average, Journal of Quality Technology 18(4), 1986"
    locator: pages 203 to 210, the EWMA as a forecast and its relation to the moving average
  - url: https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc431.htm
    title: NIST/SEMATECH e-Handbook of Statistical Methods
    locator: Section 6.4.3.1, single exponential smoothing, the recurrence, the expanded weights and the choice of the start value
  - url: https://arxiv.org/abs/1412.6980
    title: Diederik P. Kingma and Jimmy Ba, Adam, a method for stochastic optimization, ICLR 2015
    locator: Section 3, initialization bias correction of the moment estimates by 1 - beta^t
  - url: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html
    title: pandas documentation, DataFrame.ewm
    locator: the parameters com, span, halflife and alpha, and the adjust option with its two formulas
---

The exponential moving average of a stream $x_1, x_2, \ldots$ is $s_t = \alpha x_t + (1 - \alpha) s_{t-1}$ with a smoothing factor $0 < \alpha \le 1$. Unrolled, it gives the item of age $j$ the weight $\alpha (1 - \alpha)^j$, so old items fade instead of leaving a window at a fixed time. It needs one number of memory and $O(1)$ time per item, and with $\alpha = 2/(N + 1)$ its weights have the same mean age as a [moving average](/moving-average/) of $N$ items. A start at $s_0 = 0$ biases the early values toward 0, and dividing by $1 - (1 - \alpha)^t$ removes the bias exactly.

## In plain words

Keep one number, the current average. When a new value comes, move the average a fixed fraction of the way toward it: with a fraction of one tenth, the average closes a tenth of the gap. A value seen one step ago has already been diluted once, a value two steps ago twice, and so on, so each older value counts a fixed factor less than the next newer one. Nothing ever leaves outright; old values just fade. A large fraction makes the average follow the data fast and stay noisy, and a small fraction makes it smooth and slow.

## The idea

**Weights.** Write $\beta = 1 - \alpha$. Unrolling the recurrence from a start value $s_0$ gives

$$s_t = \alpha \sum_{j=0}^{t-1} \beta^j x_{t-j} + \beta^t s_0.$$

The item of age $j$, where the newest item has age 0, has weight $\alpha \beta^j$. These weights form a [geometric series](/geometric-series/) with sum $\alpha (1 - \beta^t)/(1 - \beta) = 1 - \beta^t$, and the start value keeps the remaining weight $\beta^t$. So $s_t$ is a weighted mean of the start value and the items, and the influence of the start value decays like $\beta^t$.

**The start.** Three conventions are common.

- $s_1 = x_1$, the same as $s_0 = x_1$. Then $s_t$ is a true weighted mean of the items, and the oldest item keeps the extra weight $\beta^{t-1}$. This is pandas with `adjust=False`.
- $s_0$ equal to the mean of the first few items, often of the first $N$, as in many finance tools.
- $s_0 = 0$, which is natural for vectors such as gradient moments. Then the weights of the items sum only to $1 - \beta^t$, and $s_t$ is biased toward 0 for small $t$.

**Bias correction.** With $s_0 = 0$, define $\hat{s}_t = s_t / (1 - \beta^t)$. Since $\alpha \sum_{j<t} \beta^j = 1 - \beta^t$,

$$\hat{s}_t = \frac{\sum_{j=0}^{t-1} \beta^j x_{t-j}}{\sum_{j=0}^{t-1} \beta^j},$$

a weighted mean whose weights sum to 1, at every $t$. A constant stream $x_i = c$ gives $\hat{s}_t = c$ from the first step on. This is the correction of the Adam optimizer, with $\beta = \beta_1$ or $\beta_2$, and it is the same as pandas with `adjust=True`. For large $t$ the factor $1 - \beta^t$ tends to 1, and the correction fades out.

**Effective window.** An exponential average has no window, but $\alpha$ can be matched to a moving average of $N$ items by the mean age of the weights. For the infinite series, the mean age is $\sum_{j \ge 0} j \alpha \beta^j = \beta/\alpha$. For a moving average of $N$ items it is $(0 + 1 + \cdots + (N - 1))/N = (N - 1)/2$. Setting $(1 - \alpha)/\alpha = (N - 1)/2$ gives

$$\alpha = \frac{2}{N + 1}, \qquad N = \frac{2}{\alpha} - 1.$$

This is the convention of pandas `span` and of most finance tools, with ages counted from 0 for the newest item. Two further facts support it. For white noise of variance $\sigma^2$, the variance of the exponential average in the steady state is $\sum_j \alpha^2 \beta^{2j} \sigma^2 = \frac{\alpha}{2 - \alpha} \sigma^2$, which with $\alpha = 2/(N + 1)$ is exactly $\sigma^2/N$, the variance of the $N$-item moving average. And the last $N$ items carry the weight $1 - \beta^N$, which tends to $1 - e^{-2} \approx 0.865$ as $N$ grows, so about 86 percent of the weight lies in the matching window. Other conventions exist: $\alpha = 1/N$, which gives the newest item the same weight $1/N$ as in the window, and the half-life.

**Other parameters.**

| parameter | meaning | $\alpha$ |
|---|---|---|
| span $N$ | same mean age as an $N$-item window | $2/(N + 1)$ |
| center of mass $c$ | mean age of the weights | $1/(1 + c)$ |
| half-life $h$ | weight halves every $h$ items, $\beta^h = 1/2$ | $1 - 2^{-1/h}$ |
| time constant $\tau$ | weight falls by $e$ every $\tau$ items | $1 - e^{-1/\tau}$, about $1/\tau$ |

**Computation.** The update $s \leftarrow s + \alpha (x - s)$ costs one subtraction, one multiplication and one addition. Each rounding error is multiplied by $\beta < 1$ at every later step, so errors do not build up as in the running sum of a moving average: the total error stays within a small multiple of $u/\alpha$ times the size of the values, where $u$ is the unit roundoff.

**Irregular times.** When items arrive at times $t_1 < t_2 < \cdots$, the factor for a gap $\Delta$ is $e^{-\lambda \Delta}$, so $s \leftarrow s + (1 - e^{-\lambda \Delta})(x - s)$. This is [exponential decay](/exponential-decay/) over real time, and [forward decay](/forward-decay/) computes the same weights without rescaling at every step.

## Examples

$\alpha = 1/2$ and the stream $4, 8, 6, 2$:

| $t$ | $x_t$ | $s_t$ with $s_0 = 0$ | corrected $s_t / (1 - 2^{-t})$ | $s_t$ with $s_1 = x_1$ |
|---|---|---|---|---|
| 1 | 4 | 2 | 4 | 4 |
| 2 | 8 | 5 | 20/3 | 6 |
| 3 | 6 | 11/2 | 44/7 | 6 |
| 4 | 2 | 15/4 | 4 | 4 |

The zero start gives 2 at $t = 1$, half the only item seen. The corrected value at $t = 4$ is $(2 + 6/2 + 8/4 + 4/8)/(1 + 1/2 + 1/4 + 1/8) = 7.5 / (15/8) = 4$, the weighted mean with weights $1, 1/2, 1/4, 1/8$ from the newest item.

For a window of $N = 19$ items, the matching factor is $\alpha = 2/20 = 0.1$, the center of mass is 9, and the half-life is $\ln 2 / (-\ln 0.9) \approx 6.58$ items.

## Where it is used

- **Statistical process control.** The EWMA control chart of Roberts (1959) detects small shifts of a process mean faster than a chart of single values.
- **Forecasting.** Simple exponential smoothing uses $s_t$ as the forecast of $x_{t+1}$; Holt and Winters added trend and season terms.
- **Optimization.** Momentum and the Adam optimizer keep exponential averages of gradients and of squared gradients, with the bias correction above; see [Adam](/adam/) and [stochastic gradient descent](/stochastic-gradient-descent/).
- **Networking.** TCP estimates the [round-trip time](/round-trip-time-estimation/) with an exponential average with $\alpha = 1/8$, and its deviation with $1/4$.
- **Systems.** The Unix load average is an exponential average of the run-queue length over 1, 5 and 15 minutes.
- **Signal processing.** It is the simplest [IIR filter](/iir-filter/), a first-order low-pass filter.
- **Finance.** Exponential averages of prices with a span of 12, 26 or 50 days, and indicators such as MACD built from them.

## References
