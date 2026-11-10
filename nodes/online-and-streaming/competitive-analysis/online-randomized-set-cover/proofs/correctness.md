---
title: Online randomized set cover always returns a cover, and its expected cost is O(log m log n) times the optimum
proves: [correctness]
status: full
---

We use the pseudocode of the page. The ground set $X$ has $n \ge 2$ elements, the family $\mathcal{S}$ has $m$ sets, and each set $S$ has a cost $c_S > 0$. For an element $j$, $\mathcal{S}(j)$ is the family of sets that contain $j$, and $d = \max_j \lvert \mathcal{S}(j) \rvert \le m$. The adversary is oblivious: it fixes the sequence of arriving elements before the coins are drawn. $\mathrm{OPT}$ is the cost of a cheapest family that covers the elements that arrive, and $\mathrm{OPT}_{LP}$ is the optimum of the linear program

$$\min \sum_S c_S x_S \quad \text{subject to} \quad \sum_{S \in \mathcal{S}(j)} x_S \ge 1 \text{ for each arrived } j, \qquad x \ge 0,$$

whose dual is $\max \sum_j y_j$ subject to $\sum_{j \in S} y_j \le c_S$ for each $S$ and $y \ge 0$. Each cover gives a feasible 0/1 point, so $\mathrm{OPT}_{LP} \le \mathrm{OPT}$.

Line L5 is a continuous process. While $\sum_{S \in \mathcal{S}(j)} x_S < 1$, a dual variable $y_j$ rises, and each $S \in \mathcal{S}(j)$ moves by $dx_S / dy_j = (x_S + 1/d)/c_S$. The rate of $x_S$ depends only on $x_S$, so the closed form $x_S(t) = (x_S + 1/d) e^{t / c_S} - 1/d$ after a raise of size $t$ is exact, and the implementation finds $t$ by bisection.

**Claim 1 (the fractional part is feasible and stays at most 1).** After the step for $j$, $\sum_{S \in \mathcal{S}(j)} x_S \ge 1$. The values $x_S$ never decrease, and $x_S \le 1$ for each $S$ at all times.

*Proof.* Line L5 stops only when the sum reaches 1, and it stops, because the sum grows at rate at least $1/(d \max c_S) > 0$. No line decreases an $x_S$, so the constraint of $j$ stays true at later steps. A value $x_S$ rises only during a step for some $j \in S$ while $\sum_{T \in \mathcal{S}(j)} x_T < 1$, and then $x_S < 1$. As $x_S$ is continuous in $t$, it is at most 1 when the step ends. $\square$

**Claim 2 (the output is a cover).** After the step for $j$, some set of $C$ contains $j$, and from then on this stays true.

*Proof.* After L6, if no set of $C$ contains $j$, line L8 adds a set that contains $j$. Sets are never removed from $C$. $\square$

**Claim 3 (primal against dual).** Let $P = \sum_S c_S x_S$ and $D = \sum_j y_j$ at the end. Then $P \le 2D$.

*Proof.* Both start at 0, and both change only during L5. While $y_j$ rises,

$$\frac{dP}{dy_j} = \sum_{S \in \mathcal{S}(j)} c_S \cdot \frac{x_S + 1/d}{c_S} = \sum_{S \in \mathcal{S}(j)} x_S + \frac{\lvert \mathcal{S}(j) \rvert}{d} < 1 + 1 = 2,$$

because the sum is below 1 during the raise and $\lvert \mathcal{S}(j) \rvert \le d$. Integrate over all raises. $\square$

**Claim 4 (the dual is feasible after scaling).** For each set $S$, let $Y_S = \sum_{j \in S} y_j$. Then $x_S = (e^{Y_S / c_S} - 1)/d$, so $Y_S \le c_S \ln(1 + d)$. Hence $y / \ln(1 + d)$ is a feasible dual solution, and $D \le \ln(1 + d) \cdot \mathrm{OPT}_{LP}$.

*Proof.* $x_S$ changes only when some $y_j$ with $j \in S$ rises, and then $dx_S / dY_S = dx_S / dy_j = (x_S + 1/d)/c_S$. With $x_S = 0$ at $Y_S = 0$, the solution of this equation is $x_S = (e^{Y_S/c_S} - 1)/d$. Claim 1 gives $x_S \le 1$, so $e^{Y_S / c_S} \le 1 + d$. Then $\sum_{j \in S} y_j / \ln(1+d) \le c_S$ for each $S$, and weak duality gives $D / \ln(1 + d) \le \mathrm{OPT}_{LP}$. $\square$

Claims 3 and 4 give the bound of the fractional part:

$$P \le 2 \ln(1 + d) \cdot \mathrm{OPT}_{LP} \le 2 \ln(1 + d) \cdot \mathrm{OPT}. \tag{1}$$

**Claim 5 (the fractional run does not depend on the coins).** The values $x_S$ and $y_j$ at each step are fixed numbers, the same for each outcome of the thresholds $\theta_S$.

*Proof.* Lines L4 and L5 read only the set system, the current element and the current $x$. They never read $\theta$ or $C$. The sequence of elements is fixed in advance, because the adversary is oblivious. By induction over the steps, $x$ and $y$ are fixed. $\square$

This claim is the reason the analysis needs an oblivious adversary. An adaptive adversary sees $C$ and can choose the next element by it, and then the sequence, and with it $x$, depends on the coins.

**Claim 6 (the threshold sets).** Let $C_\theta$ be the sets added by L6 and $x_S$ the final values. Then $\mathbb{E}[c(C_\theta)] = \sum_S c_S \bigl(1 - (1 - x_S)^k\bigr) \le k P$.

*Proof.* The value $x_S$ changes only during the steps for elements of $S$, and at each such step L6 compares $x_S$ with $\theta_S$. As $x_S$ never decreases, $S \in C_\theta$ if and only if $\theta_S \le x_S$ for the final value. The threshold $\theta_S$ is the minimum of $k$ independent uniform values, so $\Pr[\theta_S \le t] = 1 - (1 - t)^k$ for $t \in [0, 1]$, and by Claim 5 the value $t = x_S$ is a fixed number in $[0, 1]$. Bernoulli's inequality gives $1 - (1 - t)^k \le k t$. Sum over $S$ with weight $c_S$. $\square$

**Claim 7 (the fallback sets).** For each arrived element $j$, the probability that line L8 runs at the step of $j$ is at most $e^{-k} \le 1/n^2$. The expected cost of all sets added by L8 is at most $\mathrm{OPT}/n$.

*Proof.* If L8 runs, then after L6 no set of $\mathcal{S}(j)$ is in $C$. In particular $\theta_S > x_S$ for each $S \in \mathcal{S}(j)$, where $x_S$ is the value at the end of the step for $j$. The thresholds of different sets are independent, so by Claim 5

$$\Pr[\text{L8 runs at } j] \le \prod_{S \in \mathcal{S}(j)} (1 - x_S)^k \le \exp\Bigl(-k \sum_{S \in \mathcal{S}(j)} x_S\Bigr) \le e^{-k},$$

with $1 - t \le e^{-t}$ and Claim 1. With $k = \lceil 2 \ln n \rceil$, $e^{-k} \le 1/n^2$. Line L8 adds the cheapest set that contains $j$. The optimal cover contains some set with $j$, so this cost is at most $\mathrm{OPT}$. If an element arrives a second time, Claim 2 says it is already covered, so L8 can run only at the first arrival of each element. There are at most $n$ such arrivals, so the expected fallback cost is at most $n \cdot (1/n^2) \cdot \mathrm{OPT} = \mathrm{OPT}/n$. $\square$

**Theorem.** For each set system with $n \ge 2$ elements and each fixed sequence of arriving elements, the output $C$ is a cover of the arrived elements, and

$$\mathbb{E}[c(C)] \le 2 k \ln(1 + d) \cdot \mathrm{OPT}_{LP} + \frac{\mathrm{OPT}}{n} \le \Bigl( (4 \ln n + 2) \ln(1 + m) + \frac{1}{n} \Bigr) \mathrm{OPT}.$$

So the algorithm is $O(\log m \log n)$-competitive against an oblivious adversary.

*Proof.* Claim 2 gives the cover. The cost is $c(C) \le c(C_\theta) + c(\text{fallback sets})$. Claim 6 and (1) bound the first term by $k P \le 2k \ln(1+d) \mathrm{OPT}_{LP}$ in expectation, and Claim 7 bounds the second by $\mathrm{OPT}/n$. Finally $k \le 2 \ln n + 1$, $d \le m$ and $\mathrm{OPT}_{LP} \le \mathrm{OPT}$. $\square$

**Remark (one element).** For $n = 1$ the code uses $k = 1$. Then the same steps give $\mathbb{E}[c(C)] \le 2 \ln(1 + d) \cdot \mathrm{OPT} + e^{-1} \mathrm{OPT}$, which is still a constant times $\log m$.

**Remark (what the bound depends on).** The factor $\ln(1 + d)$ comes from the fractional part and the factor $k = O(\log n)$ from the rounding. The page gives instances that show each factor is needed: the halving adversary forces $P \ge 1 + (\log_2 d)/2$ against $\mathrm{OPT} = 1$, and the $\Omega(\log n)$ integrality gap of the set cover LP limits each rounding that is compared with $\mathrm{OPT}_{LP}$. $\blacksquare$
