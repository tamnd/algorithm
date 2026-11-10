---
title: The Karp-Luby estimators are unbiased, have relative variance below m, and need O(m log(1/δ)/ε²) samples
proves: [correctness]
status: full
---

**Setting.** Finite sets $A_1, \ldots, A_m$ have union $U$ with $|U| \ge 1$, and $W = \sum_i |A_i|$. One *sample* is a pair $(i, x)$ with $\Pr[i] = |A_i|/W$ and $x$ uniform in $A_i$. So each pair with $x \in A_i$ has probability $\frac{|A_i|}{W} \cdot \frac{1}{|A_i|} = \frac{1}{W}$: the sample is uniform over the $W$ pairs. For $x \in U$ let $c(x) \ge 1$ be the number of sets that hold $x$, so that $\sum_{x \in U} c(x) = W$ and $c(x) \le m$.

The *0-1 estimator* is $W \cdot Y$, with $Y = 1$ if $i$ is the least index with $x \in A_i$, and $Y = 0$ otherwise. The *coverage estimator* is $X = W / c(x)$.

**Statement.**

1. $E[WY] = E[X] = |U|$.
2. $\frac{\operatorname{Var}[WY]}{|U|^2} = \frac{W}{|U|} - 1 \le m - 1$ and $\frac{\operatorname{Var}[X]}{|U|^2} \le \frac{W}{|U|} - 1 \le m - 1$.
3. Let $0 < \varepsilon < 1$ and $0 < \delta < 1$, and let $N \ge 3m \ln(2/\delta)/\varepsilon^2$. The mean of $N$ independent copies of either estimator is within a factor $1 \pm \varepsilon$ of $|U|$ with probability at least $1 - \delta$.

**Proof of 1.** Each $x \in U$ has exactly one least index $i$ with $x \in A_i$, so exactly $|U|$ of the $W$ equally likely pairs have $Y = 1$. Hence $E[Y] = |U|/W$ and $E[WY] = |U|$. For the coverage estimator, group the pairs by their element:
$$E[X] = \sum_{(i, x)} \frac{1}{W} \cdot \frac{W}{c(x)} = \sum_{x \in U} c(x) \cdot \frac{1}{c(x)} = |U|.$$

**Proof of 2.** Put $\mu = E[Y] = |U|/W$. Since $Y^2 = Y$, $\operatorname{Var}[WY] = W^2(\mu - \mu^2)$, and dividing by $|U|^2 = W^2 \mu^2$ gives $\frac{1}{\mu} - 1 = \frac{W}{|U|} - 1$. For the coverage estimator, $X \le W$ because $c(x) \ge 1$, so $E[X^2] \le W\,E[X] = W|U|$ and
$$\frac{\operatorname{Var}[X]}{|U|^2} = \frac{E[X^2]}{|U|^2} - 1 \le \frac{W}{|U|} - 1.$$
Finally, $W = \sum_{x \in U} c(x) \le m|U|$, so $\frac{W}{|U|} - 1 \le m - 1$.

**Proof of 3.** Let $Z_1, \ldots, Z_N$ be independent copies of $Y$, or of $X/W$. In both cases $Z_t \in [0, 1]$, and $E[Z_t] = |U|/W \ge 1/m$ by part 1 and the bound $W \le m|U|$. Let $S = \sum_t Z_t$ and $\mu_S = E[S] = N|U|/W \ge N/m$. The Chernoff bound for independent variables with values in $[0, 1]$ gives, for $0 < \varepsilon < 1$,
$$\Pr\big[|S - \mu_S| \ge \varepsilon \mu_S\big] \le 2 \exp\!\left(-\frac{\varepsilon^2 \mu_S}{3}\right) \le 2 \exp\!\left(-\frac{\varepsilon^2 N}{3m}\right) \le 2 \exp\!\left(-\ln\frac{2}{\delta}\right) = \delta.$$
The estimate is $W S / N$ and its mean is $W \mu_S / N = |U|$, so the event $|S - \mu_S| < \varepsilon \mu_S$ is the event that the estimate is within a factor $1 \pm \varepsilon$ of $|U|$. $\blacksquare$
