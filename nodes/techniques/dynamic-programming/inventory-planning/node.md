---
tag: 5JQK7Z
kind: problem
slug: inventory-planning
name: Inventory planning
aliases:
- production planning
- lot sizing
area: techniques/dynamic-programming
level: core
summary: Choosing how many items to order each month to meet demand while minimizing ordering and storage cost, solved by dynamic programming.
prereqs: [optimal-substructure, tabulation]
see_also: [dp-on-dag, shortest-path, monge-property, row-minima-of-totally-monotone-matrices, knapsack-problem, np-hard]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 14, end-of-chapter problems, Inventory planning
  - paper: doi:10.1287/mnsc.5.1.89
    title: Harvey M. Wagner and Thomson M. Whitin, Dynamic version of the economic lot size model, Management Science 5(1), 89-96, 1958
    locator: the model with set-up costs, the property that production happens only when the stock is empty, and the O(n^2) algorithm
  - paper: doi:10.1287/opre.40.1.s145
    title: Albert Wagelmans, Stan van Hoesel and Antoon Kolen, Economic lot-sizing, an O(n log n) algorithm that runs in linear time in the Wagner-Whitin case, Operations Research 40(1-supplement-1), S145-S156, 1992
    locator: the whole paper
  - paper: doi:10.1287/opre.41.3.549
    title: Alok Aggarwal and James K. Park, Improved algorithms for economic lot size problems, Operations Research 41(3), 549-571, 1993
    locator: the use of Monge arrays and matrix searching for lot size problems
  - paper: doi:10.1287/mnsc.26.7.669
    title: M. Florian, J. K. Lenstra and A. H. G. Rinnooy Kan, Deterministic production planning, algorithms and complexity, Management Science 26(7), 669-679, 1980
    locator: the NP-hardness of the capacitated problem
---

The inventory planning problem asks how many units to produce in each period of a planning horizon so that every period's demand is met from production and stock, and the total cost of production and of holding stock is least. CLRS states a version in which a company can make $m$ machines a month with its own staff, pays $c$ per extra machine, and pays $h(j)$ to hold $j$ machines at the end of a month; a dynamic program over (month, stock) solves it in time polynomial in $n$ and the total demand $D$. Wagner and Whitin's 1958 lot-size model replaces the labor cost by a fixed set-up cost per production run and is solved in $O(n^2)$ time, and later in $O(n \log n)$ and $O(n)$ time. With general production capacities the problem is [NP-hard](/np-hard/).

## In plain words

A company knows how many products its customers will buy in each of the next months. It can make products in a month and sell them that month, or keep them in a store for later months. Making many products in one month can cost extra, and keeping products in the store also costs money.

The plan says how many to make each month. The only thing a month passes on to the next is how many products are left in the store. So for each month and each possible store level, keep the cheapest cost to reach it. Each month's best costs follow from the previous month's best costs.

## Definition

**CLRS version.** Given:

- the number of months $n$ and the demands $d_1, \ldots, d_n \ge 0$, with $D = \sum_i d_i$;
- the number $m$ of machines the regular staff can make in a month at no extra cost;
- the cost $c \ge 0$ per machine above $m$ in a month;
- a holding cost $h(j)$ for $j$ machines in stock at the end of a month, with $h(0) = 0$ and $h$ nondecreasing.

The stock starts at 0. A plan chooses $x_i \ge 0$ machines to make in month $i$, and the stock at the end of month $i$ is $s_i = s_{i-1} + x_i - d_i$, which must be $\ge 0$. The cost is

$$\sum_{i=1}^{n} \bigl( c \cdot \max(0, x_i - m) + h(s_i) \bigr).$$

Find a plan of least cost. Since $h$ is nondecreasing, an optimal plan exists with $s_n = 0$, and every $s_i \le D$.

## Variants

- **Wagner-Whitin lot sizing.** A set-up cost $K_i$ for each month with $x_i > 0$, a unit production cost $p_i$, and a unit holding cost $h_i$ per month. No capacity. This is the classic economic lot size model.
- **Concave costs.** Any concave production cost per month and linear holding costs; the zero-inventory property below still holds.
- **Capacities.** A limit $x_i \le C_i$. With equal capacities in all months and concave costs there are polynomial algorithms; with general capacities the problem is NP-hard, as shown by Florian, Lenstra and Rinnooy Kan.
- **Backlogging.** Demand may be met late at a penalty per unit and month; the stock may then be negative.

## Examples

**CLRS version.** Let $n = 4$, $d = (3, 6, 2, 5)$, $m = 4$, $c = 10$ and $h(j) = 2j$. The best plan makes $x = (4, 5, 3, 4)$, with stocks $s = (1, 0, 1, 0)$. Its cost is $10 \cdot 1$ for the extra machine in month 2, plus $2 + 0 + 2 + 0 = 4$ for holding, so 14. Two other plans for comparison:

| plan $x$ | stocks $s$ | extra labor | holding | total |
|---|---|---|---|---|
| $(3, 6, 2, 5)$ | $(0, 0, 0, 0)$ | $20 + 10 = 30$ | 0 | 30 |
| $(4, 6, 2, 4)$ | $(1, 1, 1, 0)$ | 20 | 6 | 26 |
| $(4, 5, 3, 4)$ | $(1, 0, 1, 0)$ | 10 | 4 | 14 |

A search over all plans with $x_i \le D$ confirms that 14 is the least cost.

**Wagner-Whitin version.** Let $d = (20, 50, 10, 50, 30)$, set-up cost $K = 100$ in every month, holding cost 1 per unit per month, and no unit production cost. With $F(j)$ the least cost to cover the months $1, \ldots, j$:

| $j$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $F(j)$ | 100 | 150 | 170 | 270 | 300 |
| last run starts in month | 1 | 1 | 1 | 4 | 4 |

The best plan makes 80 units in month 1 for months 1 to 3, with holding $50 \cdot 1 + 10 \cdot 2 = 70$, and 80 units in month 4 for months 4 and 5, with holding 30. The total is $2 \cdot 100 + 70 + 30 = 300$.

## Known algorithms

**Dynamic program for the CLRS version.** Let $f_i(s)$ be the least cost of months $1, \ldots, i$ that ends with stock $s$, for $0 \le s \le D$. Then $f_0(0) = 0$, $f_0(s) = +\infty$ for $s > 0$, and

$$f_i(s) = h(s) + \min_{0 \le s' \le s + d_i} \Bigl( f_{i-1}(s') + c \cdot \max\bigl(0, s + d_i - s' - m\bigr) \Bigr).$$

The answer is $f_n(0)$. The recurrence is correct because the cost of months $i + 1, \ldots, n$ depends on the plan for months $1, \ldots, i$ only through $s_i$, so an optimal plan's first $i$ months are an optimal plan to reach $s_i$. A direct evaluation takes $O(n D^2)$ time. Write $t = s + d_i$. For $s' \ge t - m$ the extra cost is 0, so that part is a minimum of $f_{i-1}$ over the window $[t - m, t]$; for $s' < t - m$ it is $c(t - m) + \min_{s' < t - m} (f_{i-1}(s') - c s')$, a prefix minimum. As $s$ grows, both are maintained in $O(1)$ amortized time per $s$, with a sliding window minimum and a running minimum, which gives $O(nD)$ time and $O(D)$ space. This is polynomial in $n$ and $D$ but not in the input size, since $D$ is a number in the input.

**Wagner and Whitin.** For set-up costs and linear holding costs, there is an optimal plan in which a month produces only when its starting stock is 0 (the zero-inventory property). So each run covers a block of consecutive months exactly, and with $F(0) = 0$,

$$F(j) = \min_{1 \le i \le j} \Bigl( F(i - 1) + K_i + p_i \sum_{t=i}^{j} d_t + \sum_{t=i}^{j} d_t \sum_{u=i}^{t-1} h_u \Bigr),$$

which takes $O(n^2)$ time with prefix sums. This is a shortest path in a [DAG](/dp-on-dag/) on the months $0, \ldots, n$.

**Faster lot sizing.** Wagelmans, van Hoesel and Kolen gave an $O(n \log n)$ algorithm, which runs in $O(n)$ time when the costs have the Wagner-Whitin form ($p_i + h_i \ge p_{i+1}$ for all $i$, so that making a unit early and holding it is never cheaper than making it later). Aggarwal and Park obtained similar bounds and extensions with [Monge](/monge-property/) arrays and [matrix searching](/row-minima-of-totally-monotone-matrices/).

## Bounds

- The CLRS version takes $O(nD)$ time by the dynamic program; the input has size $O(n + \log D)$ plus the description of $h$, so this is pseudo-polynomial.
- The uncapacitated lot size problem takes $O(n \log n)$ time, and $O(n)$ in the Wagner-Whitin case.
- The capacitated lot size problem with general capacities is NP-hard, so no polynomial algorithm is expected; dynamic programs over the stock level, like the one above, are pseudo-polynomial.

## Reductions

- **To shortest paths.** The (month, stock) table is a layered DAG with $n D$ vertices, and a plan is a path from $(0, 0)$ to $(n, 0)$. The Wagner-Whitin model is a shortest path on $n + 1$ vertices.
- **From knapsack-type problems.** The NP-hardness of the capacitated problem is shown by a reduction from a number problem in the style of the [knapsack problem](/knapsack-problem/), which also explains why the dynamic program depends on the size of the numbers.

## Applications

- **Production and procurement planning.** The lot size model is a basic model in operations research for how much to make or order each period.
- **Batch sizes in manufacturing**, where a set-up of a machine has a fixed cost and storage costs per unit and time.
- **Teaching.** The CLRS version is a standard exercise in finding the right state: the stock level is the only link between months.

## References
