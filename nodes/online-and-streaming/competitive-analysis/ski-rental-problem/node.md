---
tag: ZE91R2
kind: problem
slug: ski-rental-problem
name: Ski rental problem
aliases:
- rent-or-buy problem
area: online-and-streaming/competitive-analysis
level: intro
summary: Renting costs one unit per day and buying costs B once; the number of days is unknown.
prereqs: [online-algorithm, competitive-ratio]
see_also: [break-even-strategy, take-the-stairs-strategy, bahncard-problem, randomized-online-algorithm, yao-minimax-principle, tcp-acknowledgment-problem, advice-model, learning-augmented-algorithms]
sources:
  - paper: doi:10.1007/BF01762111
    title: "Anna R. Karlin, Mark S. Manasse, Larry Rudolph and Daniel D. Sleator, Competitive snoopy caching, Algorithmica 3(1) (1988), 79-119"
    locator: the rent-or-buy decision in snoopy caching and the deterministic factor 2
  - paper: doi:10.1007/BF01189993
    title: "Anna R. Karlin, Mark S. Manasse, Lyle A. McGeoch and Susan Owicki, Competitive randomized algorithms for nonuniform problems, Algorithmica 11(6) (1994), 542-571"
    locator: the randomized rent-or-buy algorithm with ratio tending to e/(e-1) and the matching lower bound
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: the rent-or-buy (ski rental) examples of competitive analysis
  - paper: doi:10.1007/BF01294260
    title: "Shai Ben-David, Allan Borodin, Richard M. Karp, Gabor Tardos and Avi Wigderson, On the power of randomization in on-line algorithms, Algorithmica 11(1) (1994), 2-14"
    locator: the adversary models used for the deterministic and randomized bounds
---

In the ski rental problem, a skier who does not know how many days the season will last must decide each day whether to rent skis for 1 or to buy them for $B$. It is the simplest online problem with a non-trivial answer, and it models every rent-or-buy decision: keep paying a small cost, or pay a large cost once. The best deterministic rule, rent for $B - 1$ days and then buy, pays at most $2 - 1/B$ times the offline optimum, and the best randomized rule pays about $e/(e-1) \approx 1.582$ times the optimum in expectation (Karlin, Manasse, McGeoch and Owicki 1994).

## In plain words

You go skiing, and each morning you can rent skis or buy them. Renting is cheap for one day, but the rent adds up. Buying is expensive once, then free. If you knew how long you would ski, the choice would be easy: buy at once for a long trip, rent every day for a short one. But you do not know. Any day can be the last one, for example because you break a leg.

If you buy too early, you may have wasted money on skis you hardly use. If you rent too long, you may pay the rent many times over. The best plan without luck is to rent until the rent paid is about the price of the skis, and then buy. That way you never pay more than about twice what you would have paid with perfect knowledge.

## Definition

**Notation.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution on $\sigma$, and $c$ is the competitive ratio. Here $\sigma$ is a season of $n$ ski days, so we write $\mathrm{ALG}(n)$ and $\mathrm{OPT}(n)$.

**Discrete version.** Fix an integer $B \ge 1$. The requests are ski days $1, 2, \ldots, n$, and $n \ge 1$ is not known in advance: the algorithm learns that the season is over only when no new day comes. On each day, if the skier does not own skis, it either rents for cost 1 or buys for cost $B$. After a purchase, the remaining days are free.

A deterministic online algorithm is the same as a buy day $j \in \{1, 2, 3, \ldots\} \cup \{\infty\}$: rent on days $1, \ldots, j - 1$ and buy at the start of day $j$, if the season lasts that long. Its cost is

$$\mathrm{ALG}_j(n) = \begin{cases} n & \text{if } n < j, \\ j - 1 + B & \text{if } n \ge j. \end{cases}$$

The [offline optimum](/offline-optimum/) knows $n$: it buys on day 1 if $n \ge B$ and rents otherwise, so $\mathrm{OPT}(n) = \min(n, B)$.

**Continuous version.** Scale so that $B = 1$. The season has a length $y \ge 0$, renting costs $t$ for a period of length $t$, and buying costs 1. An algorithm buys at a time $x \in [0, \infty]$. It pays $y$ if $y < x$ and $x + 1$ if $y \ge x$, and $\mathrm{OPT}(y) = \min(y, 1)$.

**Strict ratio.** Since $\mathrm{OPT}(n) \le B$, an additive constant $b \ge B - 1$ would make the rule "buy on day $B$" 1-competitive. So the ratios for ski rental are strict ($b = 0$), or equivalently $B$ is taken large compared with $b$.

## Variants

- **Elevator or stairs.** Wait for an elevator or walk up the stairs. The waiting time is unknown. See the [take-the-stairs strategy](/take-the-stairs-strategy/).
- **Bahncard.** Buy a discount card that is valid for a limited time and lowers the price of each trip. The [Bahncard problem](/bahncard-problem/) has ski rental as a special case.
- **TCP acknowledgment.** Delay acknowledgments to send them in batches. The [TCP acknowledgment problem](/tcp-acknowledgment-problem/) has the same ratios $2$ and $e/(e-1)$.
- **Multi-slope ski rental.** Several options, each with a buy cost and a rent rate, and the algorithm may move from one option to a cheaper rate.
- **Spin or block.** A thread waiting for a lock can spin (pay per unit of time) or block (pay a fixed context-switch cost). This is the continuous version, studied by Karlin, Manasse, McGeoch and Owicki.
- **Ski rental with predictions.** The algorithm gets a predicted season length that may be wrong. See [learning-augmented algorithms](/learning-augmented-algorithms/).
- **Ski rental with advice.** One bit of [advice](/advice-model/) ("the season has at least $B$ days") gives ratio 1.

## Examples

**$B = 10$.** The [break-even strategy](/break-even-strategy/) rents on days 1 to 9 and buys on day 10.

- A season of 3 days: it pays 3, and $\mathrm{OPT} = 3$.
- A season of 10 days: it pays $9 + 10 = 19$, and $\mathrm{OPT} = 10$. The ratio is $1.9 = 2 - 1/10$.
- A season of 100 days: it still pays 19, against $\mathrm{OPT} = 10$.

**The exact worst ratio of each buy day for $B = 4$.** The worst season for "buy on day $j$" ends on day $j$, just after the purchase.

| buy on day $j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | never |
|---|---|---|---|---|---|---|---|---|
| $\max_n \mathrm{ALG}_j(n)/\mathrm{OPT}(n)$ | $4$ | $5/2$ | $2$ | $7/4$ | $2$ | $9/4$ | $5/2$ | $\infty$ |

## Known algorithms

- **[Break-even strategy](/break-even-strategy/).** Buy on day $B$, when the rent already paid ($B - 1$) plus one more day would reach the price $B$. Strictly $(2 - 1/B)$-competitive, the best deterministic ratio.
- **Randomized buy day (Karlin, Manasse, McGeoch and Owicki 1994).** Buy on day $j \in \{1, \ldots, B\}$ with probability

$$p_j = \frac{c_B}{B} \left(1 - \frac{1}{B}\right)^{B - j}, \qquad c_B = \frac{1}{1 - (1 - 1/B)^B}.$$

It is strictly $c_B$-competitive against an [oblivious adversary](/oblivious-adversary/). For $B = 4$ the probabilities are $27/175, 36/175, 48/175, 64/175$ and $c_4 = 256/175 \approx 1.463$. The values $c_B$ increase with $B$ to $e/(e-1)$: $c_{10} \approx 1.5353$, $c_{100} \approx 1.5774$, $c_{1000} \approx 1.5815$.
- **[Take-the-stairs strategy](/take-the-stairs-strategy/).** The same break-even rule for waiting times, with ratio $2 - E/S$ when the elevator ride takes $E$ and the stairs take $S$.

## Bounds

| algorithm class | discrete, buy price $B$ | continuous |
|---|---|---|
| deterministic | $2 - 1/B$ | $2$ |
| randomized, oblivious adversary | $c_B = 1/(1 - (1 - 1/B)^B)$ | $e/(e-1)$ |
| randomized, adaptive adversary | $2 - 1/B$ | $2$ |
| one bit of advice | $1$ | $1$ |

All bounds in the table are tight.

**Deterministic upper bound.** The rule $j = B$ has $\mathrm{ALG}_B(n) \le (2 - 1/B) \cdot \mathrm{OPT}(n)$ for every $n \ge 1$.

*Proof.* If $n < B$, the rule rents every day and pays $n = \mathrm{OPT}(n)$. If $n \ge B$, it pays $B - 1 + B = 2B - 1$, and $\mathrm{OPT}(n) = B$, so the ratio is $(2B - 1)/B = 2 - 1/B$. $\square$

**Deterministic lower bound.** For every deterministic rule $j$ there is a season with $\mathrm{ALG}_j(n) \ge (2 - 1/B) \cdot \mathrm{OPT}(n)$.

*Proof.* If $j = \infty$, the season of $n$ days costs $n$ against $\mathrm{OPT} = B$, which is unbounded. Otherwise take $n = j$: the season ends on the day of the purchase, and the rule pays $j - 1 + B$.

- If $j \le B$, then $\mathrm{OPT}(j) = j$ and the ratio is $(j - 1 + B)/j = 1 + (B - 1)/j \ge 1 + (B - 1)/B = 2 - 1/B$.
- If $j > B$, then $\mathrm{OPT}(j) = B$ and the ratio is $(j - 1 + B)/B \ge (2B)/B = 2$. $\square$

So $2 - 1/B$ is the exact deterministic ratio, reached only by $j = B$. In the continuous version the same argument gives exactly 2.

**Randomized bound, continuous version: deriving the optimal distribution.** Let the buy time $x$ have a density $p$ on $[0, 1]$. For a season $y \in [0, 1]$,

$$\mathbb{E}[\mathrm{ALG}(y)] = \int_0^y (x + 1)\, p(x)\, dx + y \int_y^1 p(x)\, dx.$$

The best distribution makes $\mathbb{E}[\mathrm{ALG}(y)] = c \cdot y$ for all $y \in [0, 1]$, so that no season is worse than another. Differentiating in $y$ gives $(y + 1) p(y) - y p(y) + \int_y^1 p(x)\, dx = c$, that is

$$p(y) + \int_y^1 p(x)\, dx = c.$$

Differentiating again gives $p'(y) - p(y) = 0$, so $p(y) = a e^y$. At $y = 1$ the equation gives $p(1) = c$, so $c = a e$. The density integrates to 1, so $a(e - 1) = 1$. Hence

$$p(x) = \frac{e^x}{e - 1} \text{ on } [0, 1], \qquad c = \frac{e}{e - 1} \approx 1.582.$$

For $y \ge 1$ the algorithm always buys, and $\mathbb{E}[\mathrm{ALG}(y)] = 1 + \mathbb{E}[x] = 1 + 1/(e - 1) = e/(e - 1) = c \cdot \mathrm{OPT}(y)$. So the rule is strictly $e/(e-1)$-competitive against an oblivious adversary.

**Randomized lower bound, continuous version.** By the [Yao principle](/yao-minimax-principle/), it is enough to give a distribution on seasons where every deterministic buy time has $\mathbb{E}[\mathrm{ALG}] \ge \tfrac{e}{e-1} \mathbb{E}[\mathrm{OPT}]$. Let $y$ have density $e^{-y}$ on $[0, 1)$ and an atom of mass $1/e$ at $y = 2$. Then $\Pr[y \ge x] = e^{-x}$ for $x \in [0, 1]$, and

$$\mathbb{E}[\mathrm{OPT}] = \int_0^1 y e^{-y}\, dy + \frac{1}{e} = 1 - \frac{1}{e}.$$

For a buy time $x \le 1$, $\mathbb{E}[\mathrm{ALG}_x] = \int_0^x y e^{-y}\, dy + (x + 1) e^{-x} = 1$. For $x > 1$, the seasons below 1 cost $1 - 2/e$ and the atom costs at least 2, so $\mathbb{E}[\mathrm{ALG}_x] \ge 1$. So every deterministic rule has ratio at least $1/(1 - 1/e) = e/(e-1)$.

**Randomized bound, discrete version.** The same method works with sums. Requiring $\mathbb{E}[\mathrm{ALG}(n)] = c \cdot n$ for $n = 1, \ldots, B$ gives $p_n B + \sum_{i > n} p_i = c$, so $p_n = (1 - 1/B) p_{n+1}$, which gives the distribution in Known algorithms. For the lower bound, the distribution with $\Pr[n = i] = (1 - 1/B)^i/(B - 1)$ for $i = 1, \ldots, B - 1$ and the remaining mass $(1 - 1/B)^{B-1}$ on $n = 2B - 1$ gives every deterministic rule an expected cost of at least $c_B \cdot \mathbb{E}[\mathrm{OPT}]$ (for $B \ge 2$).

**Adaptive adversaries.** The [adaptive offline adversary](/adaptive-offline-adversary/) ends the season on the purchase day and pays $\mathrm{OPT}$, so the deterministic proof applies to every outcome of the coins. The [adaptive online adversary](/adaptive-adversary/) also ends the season on the purchase day $j$ (or after a large day $N$), and serves it with one of two fixed rules: rent every day, or buy on day 1. Against these two rules, a $c$-competitive algorithm needs $\mathbb{E}[j] + B - 1 \le c \cdot \mathbb{E}[j]$ and $\mathbb{E}[j] + B - 1 \le c \cdot B$. The first gives $c \ge 2 - 1/B$ when $\mathbb{E}[j] \le B$, and the second gives it when $\mathbb{E}[j] \ge B$.

## Reductions

- Ski rental is the [Bahncard problem](/bahncard-problem/) with discount factor $\beta = 0$, infinite validity, and one trip of price 1 per day: a card that makes all later trips free is a pair of skis.
- Ski rental is a two-state [metrical task system](/metrical-task-systems/) in which the cost of staying in state "rent" is 1 per request, the cost of state "own" is 0, and the move from "rent" to "own" costs $B$ (and there is no way back).
- Lower bounds for ski rental give lower bounds for any problem that contains a rent-or-buy decision, such as [TCP acknowledgment](/tcp-acknowledgment-problem/) and snoopy caching.

## Applications

- **Snoopy caching.** In a multiprocessor, a cache can keep updating a shared block (rent) or drop it and fetch it again later (buy). Karlin, Manasse, Rudolph and Sleator (1988) used the rent-or-buy argument for this problem.
- **Spin locks.** A waiting thread spins or blocks; the competitive rule spins for the time a context switch costs and then blocks.
- **Power management.** A device that is idle can stay on (pay power per second) or go to sleep (pay a fixed wake-up cost). The break-even rule turns it off after the idle time that costs as much as one wake-up.
- **Cloud computing.** Pay for a server by the hour, or reserve it for a long period at a fixed price.
- **Teaching.** Ski rental is the standard first example of competitive analysis and of the gain from randomization.

## References
