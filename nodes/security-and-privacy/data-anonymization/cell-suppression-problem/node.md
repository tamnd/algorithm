---
tag: PV767H
kind: problem
slug: cell-suppression-problem
name: Cell suppression problem
aliases:
- secondary cell suppression
area: security-and-privacy/data-anonymization
level: core
summary: Choose extra cells of a table with marginal totals to hide, so that no sensitive cell can be computed within a protection interval.
history:
  year: 1980
  people: [Lawrence H. Cox]
  note: "Cox gave the first methodology for complementary suppression in 1980. Kelly, Golden and Assad (1992) studied its hardness and network heuristics, and Fischetti and Salazar-Gonzalez solved it exactly by branch-and-cut."
prereqs: [linear-programming-problem, lp-duality]
see_also: [controlled-tabular-adjustment, mixed-integer-programming, branch-and-cut, simplex-method, generalization-and-suppression, microaggregation, dinur-nissim-reconstruction-attack, min-cost-flow-problem]
sources:
  - paper: doi:10.1080/01621459.1980.10477481
    title: "Lawrence H. Cox, Suppression methodology and statistical disclosure control, Journal of the American Statistical Association 75(370), 1980"
    locator: "pp. 377 to 385, primary and complementary suppression in tables with totals, and the audit of a suppression pattern"
  - paper: doi:10.1002/net.3230220407
    title: "James P. Kelly, Bruce L. Golden and Arjang A. Assad, Cell suppression, disclosure protection for sensitive tabular data, Networks 22(4), 1992"
    locator: "pp. 397 to 417, the network flow model of two-dimensional tables, heuristics for complementary suppression, and the hardness of the problem"
  - paper: "Matteo Fischetti and Juan-Jose Salazar-Gonzalez, Models and algorithms for the 2-dimensional cell suppression problem in statistical disclosure control, Mathematical Programming 84(2), 1999"
    locator: "pp. 283 to 312, the integer model for two-dimensional tables and its exact solution by branch-and-cut"
  - paper: "Matteo Fischetti and Juan-Jose Salazar-Gonzalez, Solving the cell suppression problem on tabular data with linear constraints, Management Science 47(7), 2001"
    locator: "pp. 1008 to 1027, the model for general tables with linear relations, the constraints from LP duality, and the branch-and-cut algorithm"
  - book: isbn:9781119978152
    title: "Anco Hundepool, Josep Domingo-Ferrer, Luisa Franconi, Sarah Giessing, Eric Schulte Nordholt, Keith Spicer and Peter-Paul de Wolf, Statistical Disclosure Control, Wiley, 2012"
    locator: "Chapter 4, Magnitude tabular data, pp. 131 to 182, Section 4.2 on the sensitivity rules and Section 4.3 on secondary risk and suppression"
  - book: isbn:9780387951218
    title: "Leon Willenborg and Ton de Waal, Elements of Statistical Disclosure Control, Lecture Notes in Statistics 155, Springer, 2001"
    locator: the chapters on tabular data and cell suppression
---

A statistical agency publishes tables of magnitudes, such as the turnover of firms by region and industry, with row and column totals. Some cells are sensitive: they are the sum of very few firms, and a published value would tell one firm about the turnover of another. The agency hides these *primary* cells. A hidden cell alone is not safe, because a reader can compute it from its row total and the other cells of the row. So the agency must also hide some *complementary* cells. The cell suppression problem asks for the cheapest set of complementary cells such that, for each sensitive cell, every table that agrees with the published cells and the totals leaves the sensitive value uncertain by at least its protection levels on both sides. Cox (1980) set up the method. The problem is strongly NP-hard in general. It is solved exactly by [branch-and-cut](/branch-and-cut/) on a model with 0-1 variables, and in practice also by network and other heuristics. [Controlled tabular adjustment](/controlled-tabular-adjustment/) is a later alternative that changes cells instead of hiding them.

## In plain words

A table shows the sales of shops by town and by kind of shop, with the sum of each row and each column. In one town, only two shops sell bikes. If the bike number for that town is printed, each of the two shops can subtract its own sales and learn the sales of the other one. So the office hides that number.

But the row sum is still printed. Anyone can subtract the other numbers of the row from the sum and get the hidden number back. So the office must hide more numbers, in the same row and in the same column, so that the sums no longer pin it down. Each hidden number is lost information. The problem is to hide as little as possible while every secret number can still be anything in a wide enough range.

## Definition

A table has $n$ cells with nonnegative values $a_1, \ldots, a_n$. The cells satisfy linear relations $M a = 0$, for example "a total equals the sum of its parts", and each cell has public bounds $lb_i \le a_i \le ub_i$, often $lb_i = 0$ and $ub_i = \infty$. A set $P$ of sensitive cells is given. Each $p \in P$ has a lower and an upper protection level $LPL_p, UPL_p \ge 0$. They come from a sensitivity rule. In the p% rule, for example, a cell with total $X$ and largest contributions $x_1 \ge x_2$ is sensitive when $X - x_1 - x_2 < (p/100)\, x_1$: the second largest contributor can then estimate $x_1$ within $p$ percent. The rule, its parameter $p$ and the protection levels are policy choices. Each other cell has a cost $w_i \ge 0$ of hiding it, such as its value, 1, or a log of its value.

For a set $S \supseteq P$ of hidden cells, the *attacker's interval* of a cell $p$ is $[y_p^-, y_p^+]$, where

$$y_p^- = \min y_p, \qquad y_p^+ = \max y_p \qquad \text{subject to } M y = 0,\ lb \le y \le ub,\ y_i = a_i \text{ for } i \notin S.$$

These are two [linear programs](/linear-programming-problem/). The set $S$ *protects* $p$ if $y_p^+ \ge a_p + UPL_p$ and $y_p^- \le a_p - LPL_p$.

- **Input:** $a$, $M$, $lb$, $ub$, $P$ with $LPL$ and $UPL$, and the costs $w$.
- **Output:** a set $S \supseteq P$ that protects every $p \in P$ and has the least cost $\sum_{i \in S \setminus P} w_i$.
- **Adversary:** a reader who knows the published cells, the relations, the bounds, and the method, and who can solve linear programs. A contributor to a cell is also an adversary for the others: the p% rule models the second largest contributor.

Checking a given $S$ is the *audit*: $2 |P|$ linear programs.

## Variants

- **Tables of counts.** For frequency tables, a cell with a small count is sensitive, and the protection asks that the hidden count is not pinned down, often in integers. The audit over the integers can be stricter than the one over the reals, but for two-dimensional tables the relations are totally unimodular and both give the same interval.
- **Sliding protection.** Only the width $y_p^+ - y_p^-$ must be at least a given level, not each side.
- **Two-dimensional, three-dimensional, linked and hierarchical tables.** Two-dimensional tables with totals have the structure of a network, which the heuristics use. Tables with more dimensions, tables that share cells, and tables with sub-totals by a hierarchy are harder.
- **Several tables from one data set.** A cell hidden in one table must stay hidden in every other table that contains it, or the protection fails.
- **Partial suppression.** Publish an interval for each hidden cell instead of a blank. The intervals are part of the output.
- **Costs.** The number of hidden cells, their total value, or a mix. The choice changes the solution, because a few large cells and many small cells can protect the same cell.

## Examples

Take the table with three rows and three columns and its totals:

| | c1 | c2 | c3 | total |
|---|---|---|---|---|
| r1 | 20 | 10 | 15 | 45 |
| r2 | **5** | 25 | 30 | 60 |
| r3 | 12 | 18 | 10 | 40 |
| total | 37 | 53 | 55 | 145 |

The cell (r2, c1) = 5 is sensitive with $LPL = UPL = 3$. The bounds are $y \ge 0$, and the cost of a cell is its value.

- **Hide (r2, c1) only.** Then $y_{21} = 60 - 25 - 30 = 5$. The interval is $[5, 5]$, and the cell is not protected.
- **Hide the rectangle (r2, c1), (r2, c3), (r3, c1), (r3, c3).** With $y_{21} = t$, the relations give $y_{23} = 35 - t$, $y_{31} = 17 - t$ and $y_{33} = 5 + t$, and the bounds give $0 \le t \le 17$. The interval is $[0, 17]$, which contains $[5 - 3, 5 + 3] = [2, 8]$. The cost is $30 + 12 + 10 = 52$. A search over all sets of up to 4 complementary cells shows that no other set protects the cell at a lower cost. Every set of 5 or more cells costs at least $10 + 10 + 12 + 15 + 18 = 65$, so the optimum is 52.
- **A higher protection level.** With $UPL = 15$, the interval must reach 20, and the rectangle above fails. The cheapest set becomes (r1, c1), (r1, c2), (r2, c2), with cost $20 + 10 + 25 = 55$. Its interval is $[0, 25]$: with $y_{21} = t$, the cell (r1, c1) is $25 - t$, and it reaches 0 at $t = 25$.

In each row or column that has a hidden cell, at least 2 cells must be hidden. Otherwise the relation of that row or column gives the hidden cell. So one sensitive cell in a two-dimensional table needs at least 3 complementary cells. The numbers above were checked by a script that solves the two linear programs of the audit for each candidate set.

## Known algorithms

- **The audit by linear programming.** For a candidate $S$, solve the $2|P|$ linear programs of the definition, for example by the [simplex method](/simplex-method/). Agencies run it on any pattern, even one found by hand, to check it.
- **Network flow heuristics for two-dimensional tables.** A table with row and column totals is a bipartite network. A pattern of hidden cells that lets a sensitive cell move corresponds to a cycle through it, and the cheapest such cycle is a [min-cost flow](/min-cost-flow-problem/) computation. Kelly, Golden and Assad (1992) give heuristics of this kind. They protect one sensitive cell at a time, so the result depends on the order and is not optimal.
- **Exact branch-and-cut.** Fischetti and Salazar-Gonzalez (1999, 2001) model the choice with a 0-1 variable $x_i$ for each cell. By [LP duality](/lp-duality/), the condition that the attacker's program gives $y_p^+ \ge a_p + UPL_p$ is a family of linear inequalities in $x$, one for each dual solution. The [branch-and-cut](/branch-and-cut/) algorithm adds the violated inequalities as cuts, and finds them by solving the attacker's programs. The papers report that it solves real tables to optimality, and the method is the base of the optimal suppression in the software tau-Argus.
- **Fast heuristics for large tables.** tau-Argus also has the hypercube method, which protects each cell by a box of hidden cells in its table, and modular methods that split a hierarchical table into small tables and protect each one. These are described in Hundepool et al. (2012, Chapter 4). Their loss is a measured quantity, with no proved bound.

## Bounds

- **Hardness.** The cell suppression problem is strongly NP-hard. Later papers, such as Fischetti and Salazar-Gonzalez (2001), credit the result to Kelly, Golden and Assad (1992). So no polynomial algorithm is expected, and exact methods are worst-case exponential.
- **The audit is polynomial.** Each attacker's interval is the value of a linear program, so a pattern can be checked in polynomial time.
- **A counting lower bound.** Each relation that contains a hidden cell must contain at least 2 hidden cells. In a two-dimensional table, a sensitive cell then needs at least 3 complementary cells, and a cheapest rectangle through it is an upper bound on the cost of protecting it alone.
- **No guarantee across releases.** The protection is only against the published table. Many tables from the same data, each protected alone, can together give an attacker more equations. With enough accurate statistics, reconstruction is possible, as the [Dinur-Nissim theorem](/dinur-nissim-reconstruction-attack/) shows in a related model.

## Reductions

- **The audit is a linear program.** It reduces to two [linear programs](/linear-programming-problem/) per sensitive cell.
- **The problem is a mixed-integer program.** With the 0-1 variables of the exact method, the problem is a [mixed-integer program](/mixed-integer-programming/) with an exponential family of constraints, which [branch-and-cut](/branch-and-cut/) handles by separation.
- **Two-dimensional tables and networks.** The relations of a table with row and column totals are the flow conservation of a bipartite network, so cycles of hidden cells are cycles of the network. This is what the network heuristics use.
- **Suppression versus adjustment.** [Controlled tabular adjustment](/controlled-tabular-adjustment/) has the same input. It publishes all cells, moves each sensitive cell out of its protection interval, and adjusts the others so that the relations still hold. Its exact form is also a mixed-integer program, with one binary variable for the direction of each sensitive cell.

## Applications

Cell suppression is the standard method for magnitude tables in business statistics at national statistical offices, and it is the main method of the tau-Argus software for tabular data. It is also used for tables of counts from censuses and from health data, where small counts are suppressed. Its weak points are the loss of many cells in large linked tables and the lack of a guarantee across many releases. These led to controlled tabular adjustment and, for some releases such as the 2020 US census, to methods based on [differential privacy](/differential-privacy-definition/).

## References
