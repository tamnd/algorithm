---
title: Randomized rounding of the set cover LP with repair has expected cost at most (ceil(ln n) + 1) times the LP value
proves: [correctness]
status: full
---

**Statement.** Let $U$ be a universe of $n \ge 1$ elements, $S_1, \ldots, S_m \subseteq U$ sets whose union is $U$, $c_1, \ldots, c_m \ge 0$ costs, and $x$ a feasible solution of the set cover LP with $x_j \le 1$ for each $j$. Let $t = \max(1, \lceil \ln n \rceil)$. Let $R$ be the random set of line L5, where each $j$ enters independently with probability $p_j = 1 - (1 - x_j)^t$, and let $I$ be the output of line L8. Then $I$ is a cover for each outcome, and

$$\mathbb{E}[c(I)] \le (t + 1) \sum_{j=1}^m c_j x_j.$$

With an optimal $x$, $\mathbb{E}[c(I)] \le (t + 1) \cdot \text{LP}^* \le (\lceil \ln n \rceil + 1) \cdot \text{OPT}$ for $n \ge 2$, and $\le 2 \cdot \text{OPT}$ for $n = 1$.

An optimal $x$ can be taken with $x_j \le 1$: replacing $x_j$ by $\min(x_j, 1)$ keeps each constraint, because a constraint that contains a capped variable already has a term equal to 1, and it does not raise the cost, because $c \ge 0$.

**Step 1: $I$ is a cover.** Lines L6 and L7 visit each element that the sets of $R$ do not cover, and add a set that contains it. Such a set exists because the union of all sets is $U$. So each element is covered by $I$.

**Step 2: the cost of the rounding.** For $0 \le a \le 1$ and an integer $t \ge 1$, $(1 - a)^t \ge 1 - t a$ (Bernoulli's inequality, by induction on $t$: $(1 - a)^{t+1} \ge (1 - t a)(1 - a) = 1 - (t + 1) a + t a^2 \ge 1 - (t + 1) a$). So $p_j \le t x_j$. By [linearity of expectation](/linearity-of-expectation/),

$$\mathbb{E}[c(R)] = \sum_{j=1}^m c_j p_j \le t \sum_{j=1}^m c_j x_j.$$

**Step 3: the chance that an element is missed.** Fix $e$ and let $J_e = \{j : e \in S_j\}$. The element is missed by $R$ when no $j \in J_e$ enters. These events are independent, so, with $1 - a \le e^{-a}$,

$$\Pr[e \text{ is missed}] = \prod_{j \in J_e} (1 - x_j)^t \le \exp\Big(-t \sum_{j \in J_e} x_j\Big) \le e^{-t} \le e^{-\ln n} = \frac{1}{n},$$

where the second inequality uses the constraint $\sum_{j \in J_e} x_j \ge 1$ and the third uses $t \ge \ln n$.

**Step 4: the cost of one repair.** Let $c_{\min}(e) = \min_{j \in J_e} c_j$. Since $\sum_{j \in J_e} x_j \ge 1$ and $x, c \ge 0$,

$$c_{\min}(e) \le c_{\min}(e) \sum_{j \in J_e} x_j \le \sum_{j \in J_e} c_j x_j \le \sum_{j=1}^m c_j x_j.$$

**Step 5: the total.** Line L7 adds at most one set of cost $c_{\min}(e)$ for each missed element, so $c(I) \le c(R) + \sum_{e} [e \text{ is missed}] \, c_{\min}(e)$. Taking expectations and using steps 2 to 4,

$$\mathbb{E}[c(I)] \le t \sum_j c_j x_j + \sum_{e \in U} \frac{1}{n} \sum_j c_j x_j = (t + 1) \sum_j c_j x_j.$$

**Step 6: comparison with OPT.** The indicator vector of an optimal cover is feasible for the LP, so $\text{LP}^* \le \text{OPT}$. With an optimal $x$ the bound becomes $(t + 1) \cdot \text{LP}^* \le (t + 1) \cdot \text{OPT}$, and $t = \lceil \ln n \rceil$ for $n \ge 2$ and $t = 1$ for $n = 1$. $\blacksquare$
