---
tag: 0XCQ9M
kind: concept
slug: configuration-lp
name: Configuration LP
aliases:
- configuration linear program
- Gilmore-Gomory LP
- set partitioning LP
area: approximation/lp-rounding
level: advanced
summary: An LP with one variable for each way to fill one bin or machine; it has exponentially many variables, its dual is separated by a knapsack problem, and it is far stronger than an assignment LP.
prereqs: [lp-relaxation, lp-duality, column-generation, knapsack-problem, bin-packing]
see_also: [karmarkar-karp-bin-packing, bin-packing, cutting-stock-problem, column-generation, unrelated-machine-scheduling-makespan, restricted-assignment-scheduling, integrality-gap, separation-oracle]
sources:
  - title: Paul C. Gilmore and Ralph E. Gomory, A linear programming approach to the cutting-stock problem, Operations Research 9(6), 1961
    locator: the LP with one column for each cutting pattern, and column generation by a knapsack problem
  - paper: doi:10.1109/SFCS.1982.61
    title: Narendra Karmarkar and Richard M. Karp, An efficient approximation scheme for the one-dimensional bin-packing problem, Proceedings of the 23rd IEEE Symposium on Foundations of Computer Science, 1982
    locator: solving the configuration LP to within an additive 1 and rounding it
  - title: Nikhil Bansal and Maxim Sviridenko, The Santa Claus problem, Proceedings of the 38th ACM Symposium on Theory of Computing, 2006
    locator: the configuration LP for max-min allocation and its solution by a dual with a knapsack separation
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 4.6 (the configuration LP for bin packing)
---

A configuration LP is a linear program with one variable for each *configuration*: a set of items that fits together in one bin, on one machine, or in one piece of stock. The LP chooses a fractional mix of configurations that covers every item. Gilmore and Gomory (1961) introduced it for the [cutting stock problem](/cutting-stock-problem/), and it is the basis of the [Karmarkar-Karp algorithm](/karmarkar-karp-bin-packing/) for bin packing. There are exponentially many variables, but the dual has one variable for each item, and checking a dual point is a [knapsack problem](/knapsack-problem/). So the LP can be solved, exactly or nearly, by [column generation](/column-generation/) or by the ellipsoid method. Its bound is much stronger than that of an assignment LP, because each configuration is already a whole, feasible way to fill one resource.

## In plain words

To pack items into boxes, you could ask for each item how much of it goes into each box. That is the assignment LP, and it is weak: it lets an item be split across boxes, so it only sees the total size.

The configuration LP instead lists every way to fill one box. A box is filled by one complete pattern, and the LP decides how many boxes use each pattern, possibly a fraction. Inside a box everything is whole, so only the count of each pattern can be fractional.

There are too many patterns to list. But the LP can be solved by adding good patterns one at a time, and finding the next good pattern is a knapsack problem.

## The idea

**The general form.** Let the resources be bins, or machines $i = 1, \ldots, m$, and the items be $j = 1, \ldots, n$. For each resource $i$, let $\mathcal{C}_i$ be the family of item sets that fit on $i$. For makespan scheduling with target $T$, $C \in \mathcal{C}_i$ when $\sum_{j \in C} p_{ij} \le T$. The configuration LP is

$$\sum_{C \in \mathcal{C}_i} x_{i, C} \le 1 \ \text{ for each } i, \qquad \sum_i \sum_{C \in \mathcal{C}_i : j \in C} x_{i, C} \ge 1 \ \text{ for each } j, \qquad x \ge 0.$$

Each resource picks a fractional mix of at most one configuration, and each item is covered. A schedule with makespan $T$ gives a 0-1 point, so if the LP is infeasible, no such schedule exists.

**Bin packing.** All bins are the same, so the LP counts bins of each type. With item sizes $v_1, \ldots, v_d$ that appear $b_1, \ldots, b_d$ times, a configuration is a vector $a \in \mathbb{Z}_{\ge 0}^d$ with $\sum_t a_t v_t \le 1$, and the Gilmore-Gomory LP is

$$\min \sum_C x_C \ \text{ s.t. } \ \sum_C a_{C, t} x_C \ge b_t \ \text{ for each size } t, \quad x \ge 0.$$

**The dual and its separation.** The dual of the bin packing LP is

$$\max \sum_t b_t w_t \ \text{ s.t. } \ \sum_t a_{C, t} w_t \le 1 \ \text{ for each configuration } C, \quad w \ge 0.$$

It has only $d$ variables. A point $w$ is feasible exactly when no configuration has value more than 1 under the weights $w$, and the best configuration is the solution of an unbounded knapsack problem with sizes $v_t$, values $w_t$ and capacity 1. So a [separation oracle](/separation-oracle/) for the dual is a knapsack solver. Knapsack is NP-hard, but it has an FPTAS and a pseudo-polynomial dynamic program. Karmarkar and Karp used the FPTAS inside the ellipsoid method to solve the LP to within an additive 1. In practice, column generation adds the best configuration as a new column until none has value more than 1.

**Why it is strong.** A vertex has at most as many nonzero variables as the LP has rows, so at most $d$ configurations are used. Rounding down each $x_C$ packs most items in whole bins, and only a set of items of total size less than $d$ is left. This is the core of the [Karmarkar-Karp](/karmarkar-karp-bin-packing/) rounding.

**Integrality gap.** For bin packing, $\text{SIZE} \le \text{LP} \le \text{OPT}$, and Hoberg and Rothvoss (2017) showed $\text{OPT} \le \text{LP} + O(\log \text{OPT})$. The *modified integer round-up conjecture* says that $\text{OPT} \le \lceil \text{LP} \rceil + 1$ always. For other problems the gap can stay large: for $R \| C_{\max}$ it is 2 (Verschae and Wiese 2014), no better than the much smaller assignment LP.

## Examples

**Three items of size 0.4.** The configurations are $a = (1)$ and $a = (2)$, since three copies have size $1.2 > 1$. The LP is $\min x_1 + x_2$ with $x_1 + 2x_2 \ge 3$, and its optimum is $x_2 = 3/2$, of value $3/2$. The optimum packing needs 2 bins, which is $\lceil 3/2 \rceil$. The size bound is only $1.2$.

**Three items of size 0.6.** Each configuration holds at most one item, so the LP is $\min x_1$ with $x_1 \ge 3$, of value 3 = OPT. The assignment view only gives the size bound $1.8$, so it would allow 2 bins. The configuration LP sees that no two of these items fit together.

**Restricted assignment.** Take machines 1 and 2, one job of time 2 that can run on both, and one job of time 1 that can run only on machine 1. For $T = 2$, machine 1 has the configurations $\{1\}$, $\{2\}$ and $\emptyset$, where job 1 is the long job, and machine 2 has $\{1\}$ and $\emptyset$. The point $x_{1, \{2\}} = 1$, $x_{2, \{1\}} = 1$ is feasible and integral, and it is the schedule of makespan 2.

## Where it is used

- **Bin packing and cutting stock.** The [Karmarkar-Karp algorithm](/karmarkar-karp-bin-packing/) rounds the LP to $\text{OPT} + O(\log^2 \text{OPT})$ bins, and Rothvoss and Hoberg-Rothvoss improved this to $\text{OPT} + O(\log \text{OPT})$. Gilmore and Gomory solved real [cutting stock](/cutting-stock-problem/) problems with it, and branch and price on this LP is still the standard exact method.
- **Scheduling.** For [restricted assignment](/restricted-assignment-scheduling/) the configuration LP estimates OPT within $33/17$ (Svensson 2012) and $11/6$ (Jansen and Rohwedder 2017). For [unrelated machines](/unrelated-machine-scheduling-makespan/) its gap is 2, the same as the assignment LP.
- **Max-min allocation.** In the Santa Claus problem, each child must get a set of gifts of large total value. Bansal and Sviridenko (2006) introduced the configuration LP for it, and in the restricted version its gap is a constant.
- **Assignment with profits.** For the profit version of the [generalized assignment problem](/generalized-assignment-problem/) and for welfare maximization, rounding the configuration LP gives ratio $1 - 1/e$ (Fleischer, Goemans, Mirrokni and Sviridenko 2006), and Feige and Vondrák (2006) beat $1 - 1/e$ by a small constant.
- **Routing and crew scheduling.** Vehicle routing and airline crew scheduling are solved in practice by set partitioning LPs, with one variable per feasible route or duty, which are configuration LPs.

## References
