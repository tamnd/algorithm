---
tag: 16KWQT
kind: theorem
slug: liu-layland-utilization-bound
name: Liu-Layland utilization bound
aliases:
- rate-monotonic utilization bound
- Liu-Layland bound
area: systems/scheduling
level: advanced
summary: "Rate-monotonic priorities meet all deadlines of n tasks with deadlines equal to periods if the utilization is at most n(2^(1/n) - 1), which tends to ln 2. The test is sufficient only."
prereqs: [rate-monotonic-scheduling, utilization, rate-monotonic-optimality]
see_also: [rate-monotonic-scheduling, rate-monotonic-optimality, response-time-analysis, schedulability-analysis, earliest-deadline-first, deadline-monotonic-scheduling]
sources:
  - paper: doi:10.1145/321738.321743
    title: "C. L. Liu and James W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, Journal of the ACM 20(1) (1973), 46-61"
    locator: the least upper bound n(2^(1/n) - 1) of the processor utilization for the rate-monotonic priority assignment, and its limit ln 2
  - paper: doi:10.1016/S0020-0190(00)00016-8
    title: "Raymond Devillers and Joël Goossens, Liu and Layland's schedulability test revisited, Information Processing Letters 73(5-6) (2000), 157-161"
    locator: the gap in the original proof of the bound, and a complete proof
  - paper: doi:10.1109/TC.2003.1214341
    title: "Enrico Bini, Giorgio C. Buttazzo and Giuseppe M. Buttazzo, Rate monotonic analysis: the hyperbolic bound, IEEE Transactions on Computers 52(7) (2003), 933-942"
    locator: the test that the product of (U_i + 1) is at most 2, its proof, and its comparison with the Liu-Layland bound
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 4, Periodic Task Scheduling (the utilization bound of rate monotonic and the hyperbolic bound)
---

The Liu-Layland utilization bound says that [rate-monotonic scheduling](/rate-monotonic-scheduling/) meets all deadlines of $n$ periodic tasks with deadlines equal to their periods, on one processor, if the total [utilization](/utilization/) is at most $n(2^{1/n} - 1)$. The bound is $1$ for one task, about $0.828$ for two, and it falls to $\ln 2 \approx 0.693$ as $n$ grows. It is a sufficient test, not a necessary one: many task sets above it are schedulable, and the hyperbolic bound of Bini, Buttazzo and Buttazzo, $\prod_i (U_i + 1) \le 2$, accepts all sets that it accepts and more.

## Statement

Let $\tau = \{\tau_1, \ldots, \tau_n\}$ be independent [sporadic or synchronous periodic](/sporadic-task-model/) tasks $\tau_i = (C_i, T_i)$ with implicit deadlines $D_i = T_i$, on one processor with preemption at any time and no overheads. Let $U_i = C_i / T_i$ and $U = \sum_i U_i$.

**Theorem 1 (hyperbolic bound; Bini, Buttazzo and Buttazzo 2003).** If

$$\prod_{i=1}^n (U_i + 1) \le 2,$$

then rate-monotonic priorities meet all deadlines of $\tau$.

**Theorem 2 (Liu and Layland 1973).** If

$$U \le n\left(2^{1/n} - 1\right),$$

then rate-monotonic priorities meet all deadlines of $\tau$.

**Facts on the bound.** The value $b_n = n(2^{1/n} - 1)$ decreases in $n$, and $b_n \to \ln 2$:

| $n$ | 1 | 2 | 3 | 4 | 5 | 10 | 100 | $\infty$ |
|---|---|---|---|---|---|---|---|---|
| $b_n$ | 1 | 0.8284 | 0.7798 | 0.7568 | 0.7435 | 0.7177 | 0.6956 | 0.6931 |

For each $n$, the bound is the best possible in terms of $U$ alone: there are sets of $n$ tasks with $U$ above $b_n$ by any small amount that miss a deadline.

## In plain words

You have several repeating jobs on one processor, ranked so that the job that repeats most often goes first. Add up the share of the processor that each job needs. If the total is at most a certain limit, every job is on time; you do not need to look at the jobs in more detail. The limit depends only on the number of jobs. For one job it is the whole processor; for two it is about 83 percent; for many jobs it falls slowly towards about 69 percent.

The test can say "yes" without a full check, but it never says "no". Many sets of jobs above the limit are still on time. A second test multiplies the shares instead of adding them, and it says "yes" more often.

## Proof

Write $\operatorname{hp}(k)$ for the tasks before $\tau_k$ in the rate-monotonic order and $W_k(t) = C_k + \sum_{j \in \operatorname{hp}(k)} \lceil t / T_j \rceil C_j$. By the [critical instant theorem](/rate-monotonic-optimality/), task $\tau_k$ misses a deadline in some legal release pattern if and only if $W_k(t) > t$ for each $t \in (0, T_k]$.

*Proof of Theorem 1.* Assume that rate-monotonic priorities miss a deadline. We show that $\prod_i (U_i + 1) > 2$. If some $U_i > 1$, this is clear, so let each $U_i \le 1$. Let $\tau_k$ be a task that misses a deadline. The tasks in $\operatorname{hp}(k)$ have periods at most $T_k$. We drop the other tasks; this can only make the product smaller, since each factor is at least 1. Rename the tasks so that $\tau_k$ becomes $\tau_m$, the other ones are $\tau_1, \ldots, \tau_{m-1}$, and $W(t) = W_k(t) > t$ for each $t \in (0, T_m]$.

*Step 1: short periods are stretched.* For $i < m$, let $q_i = \lfloor T_m / T_i \rfloor \ge 1$ and replace $\tau_i$ by $(q_i C_i, q_i T_i)$. Its utilization does not change. Its new period is in $(T_m / 2, T_m]$: if $q_i = 1$, then $T_i > T_m / 2$; if $q_i \ge 2$, then $q_i T_i > T_m q_i / (q_i + 1) \ge 2 T_m / 3$. For each $t > 0$, the integer $q_i \lceil t / (q_i T_i) \rceil$ is at least $t / T_i$, so it is at least $\lceil t / T_i \rceil$. So the new demand $W'(t)$ is at least $W(t)$, and still $W'(t) > t$ for each $t \in (0, T_m]$. From now on we use the new tasks, sorted so that $T_m / 2 < T_1 \le \cdots \le T_{m-1} \le T_m$.

*Step 2: the demand at the periods.* Let $S = \sum_{i < m} C_i$, $A = C_m + S$, and $P_j = \sum_{i \le j} C_i$ (so $P_0 = 0$ and $P_{m-1} = S$). Take $j \le m$ and $i < m$. Since $T_j > T_m / 2 \ge T_i / 2$ and $T_j \le T_m < 2 T_i$, we have $\lceil T_j / T_i \rceil = 1$ if $i \ge j$ and $\lceil T_j / T_i \rceil \le 2$ if $i < j$. So

$$T_j < W(T_j) \le C_m + S + P_{j-1} = A + P_{j-1} \qquad (1 \le j \le m).$$

*Step 3: the product telescopes.* For $i < m$, the bound $T_i < A + P_{i-1}$ and $C_i \ge 0$ give

$$1 + \frac{C_i}{T_i} \ge 1 + \frac{C_i}{A + P_{i-1}} = \frac{A + P_i}{A + P_{i-1}},$$

so $\prod_{i < m} (1 + U_i) \ge (A + S) / A$. For $i = m$, since $C_m > 0$ and $T_m < A + S$,

$$1 + \frac{C_m}{T_m} > \frac{A + S + C_m}{A + S} = \frac{2A}{A + S}.$$

The product of the two bounds is $2$. So $\prod_{i \le m} (1 + U_i) > 2$, and the product over the original tasks is at least as large. $\blacksquare$

*Proof of Theorem 2.* By the inequality of arithmetic and geometric means,

$$\prod_{i=1}^n (1 + U_i) \le \left(\frac{1}{n}\sum_{i=1}^n (1 + U_i)\right)^n = \left(1 + \frac{U}{n}\right)^n.$$

If $U \le n(2^{1/n} - 1)$, then $1 + U/n \le 2^{1/n}$, so the product is at most 2, and Theorem 1 applies. $\blacksquare$

*Proof of the facts.* Let $g(x) = (2^x - 1)/x$ for $x > 0$, so $b_n = g(1/n)$. Since $2^x$ is convex, the slope $g(x)$ of the chord from $0$ to $x$ increases with $x$; so $b_n$ decreases in $n$. As $x \to 0$, $g(x)$ tends to the derivative of $2^x$ at $0$, which is $\ln 2$. The claim that the bound is the best possible is shown under Tightness. $\blacksquare$

## Consequences

- **A test in $O(n)$ time.** An admission controller can accept a new task if the new $U$ stays below $b_n$, or below $\ln 2$ for any number of tasks, without any further analysis.
- **The hyperbolic test is stronger.** By the proof of Theorem 2, each set that passes the Liu-Layland test passes the hyperbolic test. The converse fails: $(C, T) = (1, 2), (1, 3)$ has $U = 5/6 > 0.8284$ but $\tfrac32 \cdot \tfrac43 = 2$; $(3, 5), (1, 4)$ has $U = 0.85$ but $1.6 \cdot 1.25 = 2$. Both are schedulable.
- **Best fixed order.** By the [optimality of rate-monotonic priorities](/rate-monotonic-optimality/), a set that fails under rate-monotonic priorities fails under every fixed order, so $b_n$ is also the guaranteed utilization of the best fixed order.
- **The price of fixed priorities.** [EDF](/earliest-deadline-first/) meets all deadlines for each $U \le 1$. So fixed priorities may waste up to $1 - \ln 2 \approx 31\%$ of the processor in the worst case, but they waste much less for most task sets.

## Tightness

**The bound is the best possible.** Take periods $T_i = 2^{(i-1)/n}$ for $i = 1, \ldots, n$, and

$$C_i = T_{i+1} - T_i \quad (i < n), \qquad C_n = 2 T_1 - T_n.$$

Then $U = \sum_{i<n} (2^{1/n} - 1) + (2^{1/n} - 1) = n(2^{1/n} - 1)$, since $2 T_1 / T_n = 2^{1/n}$, and the product $\prod_i (1 + U_i) = \frac{T_n}{T_1} \cdot \frac{2 T_1}{T_n} = 2$ telescopes. So the set is schedulable by Theorem 1. Let $T_0 = 0$. For $t \in (T_j, T_{j+1}]$, the tasks $\tau_1, \ldots, \tau_j$ have two releases in $[0, t)$ and the others one, so $W_n(t) = C_n + \sum_{i<n} C_i + \sum_{i \le j} C_i = T_1 + (T_{j+1} - T_1) = T_{j+1} \ge t$. If $C_n$ grows by any $\varepsilon > 0$, then $W_n(t) \ge t + \varepsilon > t$ on all of $(0, T_n]$, so $\tau_n$ misses its deadline with $U = b_n + \varepsilon / T_n$. With integers close to these periods the same happens:

| periods | $C$ | $U$ | $b_n$ |
|---|---|---|---|
| $70, 99$ | $29, 41$ | $0.8284271$ | $0.8284271$ |
| $100, 126, 159$ | $26, 33, 41$ | $0.7797664$ | $0.7797631$ |
| $1000, 1189, 1414, 1682$ | $189, 225, 268, 318$ | $0.7568285$ | $0.7568285$ |

Each of these sets is schedulable, its product $\prod_i (1 + U_i)$ is exactly 2, and its $U$ is a little above $b_n$, so it fails the Liu-Layland test and passes the hyperbolic test. Adding 1 to the last $C$ makes the last task miss its deadline. For $(29, 70), (41, 99)$, the response time of the second task is exactly 70; with $C_2 = 42$, its first job misses the deadline 99.

**The bound is not necessary.** The set $(1, 4), (2, 6), (3, 12)$ has $U = 5/6 > b_3$ and product $25/12 > 2$, so it fails both tests, but its response times are 1, 3 and 10, and it is schedulable. Harmonic periods are schedulable up to $U = 1$. So the exact tests, [response-time analysis](/response-time-analysis/) or a simulation over the [hyperperiod](/hyperperiod/), are needed above the bounds.

**The assumptions are needed.** The theorems are about rate-monotonic priorities with implicit deadlines. With deadlines shorter than the periods, a set with a small $U$ can fail: $(C, T, D) = (1, 10, 1), (1, 10, 1)$ has $U = 0.2$ and misses a deadline under each order.

## History

Liu and Layland (1973) stated the bound $n(2^{1/n} - 1)$ and its limit $\ln 2$, with a proof that first reduces to periods within a factor 2 and then finds the task set with the least utilization that fully uses the processor. Devillers and Goossens (2000) showed that a step of this proof does not follow as written, and gave a complete proof. Bini, Buttazzo and Buttazzo (2003) gave the hyperbolic bound, which is tight in a stronger sense: it is the best test that uses only the individual utilizations $U_i$.

## References
