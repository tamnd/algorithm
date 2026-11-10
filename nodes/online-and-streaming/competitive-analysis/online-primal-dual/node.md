---
tag: KSYT80
kind: technique
slug: online-primal-dual
name: Online primal-dual method
aliases:
- online primal-dual
- primal-dual method for online algorithms
area: online-and-streaming/competitive-analysis
level: research
summary: Raises a covering solution multiplicatively and its packing dual additively as constraints arrive; the primal stays within 2 of the dual, which is feasible after scaling by O(log d).
prereqs: [lp-duality, weak-duality, competitive-ratio, online-algorithm]
see_also: [online-set-cover-problem, online-randomized-set-cover, ski-rental-problem, balance-algorithm, online-adwords-problem, ranking-algorithm, primal-dual-schema, multiplicative-weights-update]
sources:
  - paper: doi:10.1561/0400000024
    title: "Niv Buchbinder and Joseph (Seffi) Naor, The design of competitive online algorithms via a primal-dual approach, Foundations and Trends in Theoretical Computer Science 3(2-3) (2009), 93-263"
    locator: Chapter 4 (online fractional covering and packing, Theorems 4.1 and 4.2, and the lower bound in Section 4.3), Chapter 5 (rounding for set cover), and the later chapters on ski rental, ad auctions and caching
  - paper: doi:10.1287/moor.1080.0363
    title: "Niv Buchbinder and Joseph (Seffi) Naor, Online primal-dual algorithms for covering and packing, Mathematics of Operations Research 34(2) (2009), 270-286"
    locator: the online fractional covering algorithm with ratio O(log d) and the matching lower bound
  - paper: doi:10.1137/060661946
    title: "Noga Alon, Baruch Awerbuch, Yossi Azar, Niv Buchbinder and Joseph (Seffi) Naor, The online set cover problem, SIAM Journal on Computing 39(2) (2009), 361-370"
    locator: the multiplicative update of the fractional solution and its randomized rounding
  - paper: doi:10.1007/978-3-540-75520-3_24
    title: "Niv Buchbinder, Kamal Jain and Joseph (Seffi) Naor, Online primal-dual algorithms for maximizing ad-auctions revenue, Algorithms ESA 2007, LNCS 4698, 253-264"
    locator: the primal-dual algorithm for budgeted allocation
---

The online primal-dual method designs and analyses online algorithms for problems that can be written as a covering LP whose constraints arrive one at a time, or as the packing LP that is its dual. When a constraint arrives unsatisfied, the algorithm raises the matching dual variable and, at the same time, raises the primal variables of the constraint multiplicatively, at a rate that adds a small constant to each. The two solutions grow together, so the primal cost stays within a factor 2 of the dual value, and the dual is feasible after scaling by $\ln(1 + d)$, where $d$ is the largest number of variables in a constraint. [Weak duality](/weak-duality/) then gives the ratio $O(\log d)$. Buchbinder and Naor (2009) made it a general method, and it gives ski rental, online set cover, the adwords bound and much more from one pattern.

## In plain words

Think of a list of needs that arrive one by one, and a set of tools that each cover some of the needs at a price. Each need must be met when it arrives, by buying parts of tools, and a purchase can never be undone.

When a need arrives that is not yet met, buy a little more of each tool that would help. Buy faster the tools that are cheap and the tools that are already partly bought. Keep a tally of how much effort went into each need. The tally gives a lower bound on what any plan must pay, and the purchases never cost more than a small multiple of the tally. Rounding the parts to whole tools, with a random threshold for each tool, turns this into a plan that buys whole tools.

## When it applies

The method applies when the problem has an LP formulation of this kind, possibly after a relaxation.

- **Covering primal, rows online.** Minimize $\sum_{i=1}^{m} c_i x_i$ over $x \ge 0$, subject to $\sum_{i \in S(j)} x_i \ge 1$ for each constraint $j = 1, \ldots, n$. Constraint $j$, with its set $S(j)$ of variables, arrives at step $j$, and the variables $x_i$ may only increase. In [online set cover](/online-set-cover-problem/), $i$ ranges over the $m$ sets and $j$ over the $n$ arriving elements.
- **Packing dual, columns online.** Maximize $\sum_j y_j$ subject to $\sum_{j : i \in S(j)} y_j \le c_i$ for each $i$, $y \ge 0$. A new primal row is a new dual variable.
- **A bound $d$.** $d = \max_j \lvert S(j) \rvert \le m$. The ratio depends on $d$ (or on the ratio of the largest to the smallest coefficient in the general form), not on the number of constraints.
- **A rounding step, if the problem is integral.** The method itself gives a fractional solution. For an integral problem one needs an online rounding scheme that keeps the cost within a further factor; for set cover this factor is $O(\log n)$.

## The template

Below, $x$ is the fractional covering solution and $y$ the dual. The continuous form raises $y_j$ as a parameter; the discrete form replaces line L5 by one multiplicative step, repeated.

```pseudo id=main
ONLINE-FRACTIONAL-COVER(c, d, σ)                    ▷ σ = S(1), S(2), ... revealed one at a time
L1  x_i ← 0 for each variable i
L2  for each arriving constraint j with set S(j) do
L3      y_j ← 0
L4      while Σ_{i ∈ S(j)} x_i < 1 do
L5          raise y_j continuously; for each i ∈ S(j) raise x_i at the rate dx_i/dy_j = (x_i + 1/d)/c_i
L6      ▷ discrete form: x_i ← x_i (1 + 1/c_i) + 1/(|S(j)| c_i) for i ∈ S(j), y_j ← y_j + 1 (needs c_i ≥ 1)
L7  return x, y
```

**Theorem (Buchbinder and Naor).** The continuous template returns a feasible covering solution with $\sum_i c_i x_i \le 2 \ln(1 + d) \cdot \mathrm{OPT}_{LP}$, where $\mathrm{OPT}_{LP}$ is the optimum of the covering LP on the whole input.

*Proof.* There are three steps.

1. *The primal is feasible and online.* Constraint $j$ is handled when it arrives, and line L4 stops only when $\sum_{i \in S(j)} x_i \ge 1$. The variables only increase, so earlier constraints stay satisfied. The loop ends: while it runs, each $x_i$ in $S(j)$ grows at rate at least $1/(d c_i)$.
2. *$P \le 2D$.* Let $P = \sum_i c_i x_i$ and $D = \sum_j y_j$. While $y_j$ rises by $dy$, the primal rises by $\sum_{i \in S(j)} c_i \, dx_i = \big(\sum_{i \in S(j)} x_i + \lvert S(j) \rvert / d\big) dy \le (1 + 1)\,dy$, since the loop runs only while $\sum_{i \in S(j)} x_i < 1$ and $\lvert S(j) \rvert \le d$. Both start at 0, so $P \le 2D$.
3. *$y / \ln(1 + d)$ is dual feasible.* Fix $i$ and let $Y_i = \sum_{j : i \in S(j)} y_j$. The variable $x_i$ changes only while some $y_j$ with $i \in S(j)$ rises, and then $dx_i / dY_i = (x_i + 1/d)/c_i$. With $x_i = 0$ at $Y_i = 0$, this gives $x_i = (e^{Y_i / c_i} - 1)/d$. While $x_i$ rises, the active constraint has $\sum_{i \in S(j)} x_i < 1$, so $x_i \le 1$ at all times. So $e^{Y_i/c_i} \le 1 + d$, that is $Y_i \le c_i \ln(1 + d)$.

By weak duality, $D / \ln(1 + d) \le \mathrm{OPT}_{LP}$. So $P \le 2D \le 2 \ln(1 + d)\,\mathrm{OPT}_{LP}$. $\square$

**Lower bound (fractional halving).** No deterministic online algorithm for fractional set cover, and in expectation no randomized online algorithm against an oblivious adversary, has a ratio $o(\log d)$.

*Proof.* Take $d = 2^k$ sets of cost 1. Element 1 lies in all of them. After element $t$ arrives and the algorithm has answered, the current family $C_t$ of $d/2^{t-1}$ sets has total weight $W_t \ge 1$. The adversary splits $C_t$ into two halves and lets element $t + 1$ lie in the half of smaller weight, so the other half keeps weight at least $W_t / 2 \ge 1/2$, and no later element uses it. After $k$ halvings one set is left, and it must have $x = 1$. The left-behind halves are disjoint, so the cost is at least $1 + k/2 = 1 + \frac{1}{2} \log_2 d$, while one set covers all $k + 1$ elements, so $\mathrm{OPT} = 1$. For a randomized algorithm, apply the argument to the expected values $\mathbb{E}[x_i]$, which an oblivious adversary can compute from the prefix. $\square$

## Classic examples

- **[Ski rental](/ski-rental-problem/).** Primal: minimize $Bx + \sum_j z_j$ with $x + z_j \ge 1$ for each ski day $j$. On day $j$, if $x < 1$, set $z_j = 1 - x$ and $x \leftarrow x(1 + 1/B) + 1/(cB)$ with $c = (1 + 1/B)^B - 1$. Each day raises the primal by $1 + 1/c$ and the dual by 1, and after $B$ days $x = 1$, so the dual is feasible. The ratio is $1 + 1/c$, which tends to $e/(e - 1) \approx 1.582$; for $B = 10$, $c \approx 1.5937$ and the ratio is about $1.6275$. Read as a distribution over the day to buy, $x$ is the randomized ski rental algorithm.
- **[Online set cover](/online-set-cover-problem/).** The template is the fractional step, with $d$ the largest number of sets that contain an element. [Randomized rounding with thresholds](/online-randomized-set-cover/) gives $O(\log m \log n)$.
- **[Adwords](/online-adwords-problem/) and [Balance](/balance-algorithm/).** Here the online objects are packing columns. The price $x_i$ of an advertiser rises multiplicatively with each query it gets, and each query goes to the largest $b_{ij}(1 - x_i)$. The ratio $(1 - 1/c)(1 - R_{\max})$ tends to $1 - 1/e$.
- **[Ranking](/ranking-algorithm/).** Devanur, Jain and Kleinberg (2013) split the gain of each matched edge with $g(y) = e^{y-1}$ and show that the dual is feasible in expectation over the random ranks: a randomized primal-dual analysis.
- **[Weighted paging](/weighted-paging-problem/).** Bansal, Buchbinder and Naor used a fractional primal-dual algorithm and an online rounding to get a randomized $O(\log k)$-competitive algorithm.

## Variations

- **Discrete updates.** Line L6 replaces the continuous rate by a multiplicative step, with one dual unit per step. With $c_i \ge 1$, each step raises the primal by at most 2 and the dual by 1, and Buchbinder and Naor show the ratio $O(\log d)$ for this form as well.
- **General coefficients.** Rows $\sum_i a_{ij} x_i \ge 1$ with $a_{ij} \ge 0$ are handled by a rate that grows with $a_{ij}/c_i$. Buchbinder and Naor (2009) give the general form and its ratio, which is again logarithmic.
- **Packing problems.** Read the pair the other way: the online objects are packing columns, and the covering prices rise as the capacity is used. Adwords and Balance are the standard examples.
- **Randomized primal-dual.** The dual is feasible only in expectation over the coins, as in the analysis of Ranking.
- **Learning-augmented primal-dual.** Bamas, Maggiori and Svensson (2020) bias the update toward a predicted solution and keep a robust bound when the prediction is bad; see [learning-augmented algorithms](/learning-augmented-algorithms/).

## Pitfalls

- **Starting the multiplicative update at zero.** A purely multiplicative rule $x_i \leftarrow x_i(1 + 1/c_i)$ never leaves 0. The additive term $1/d$ (or $1/(\lvert S(j) \rvert c_i)$) is what starts each variable.
- **Mixing up $d$, $m$ and $n$.** The fractional ratio is $O(\log d)$ with $d$ the largest row size, at most the number of variables $m$. It does not depend on the number of constraints $n$. The extra $\log n$ in online set cover comes from the rounding.
- **Forgetting that the dual needs scaling.** The dual $y$ itself is not feasible; only $y / \ln(1 + d)$ is. The ratio is the product of the factor 2 and this scaling.
- **Decreasing variables.** An online covering algorithm may not lower $x_i$. A rule that does so is not online in this model, even if the final solution is feasible.
- **Treating the fractional ratio as the integral one.** For an integral problem the rounding step is part of the algorithm and its loss must be added.

## Exercises

1. Show that the discrete update of line L6 raises the primal by at most 2 and the dual by 1 in each step when all $c_i \ge 1$.
2. Write the ski rental LP and its dual, and show that the update in the examples ends with $x = 1$ exactly after $B$ days.
3. In the halving lower bound, let the adversary split $C_t$ into $r$ equal parts instead of two. What bound does this give?
4. Apply the template to online vertex cover with edges arriving online ($d = 2$), and compare its fractional ratio with the integral ratio 2 of taking both endpoints.

## References
