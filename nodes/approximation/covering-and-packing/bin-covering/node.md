---
tag: TQ2XDA
kind: problem
slug: bin-covering
name: Bin covering problem
aliases:
- dual bin packing
- bin covering
area: approximation/covering-and-packing
level: advanced
summary: Maximize the number of bins each filled to at least a threshold.
prereqs: [bin-packing, approximation-ratio, partition-problem]
see_also: [bin-packing, machine-covering, next-fit-bin-packing, bin-packing-aptas, three-partition, asymptotic-ptas]
sources:
  - paper: "S. F. Assmann, D. S. Johnson, D. J. Kleitman and J. Y.-T. Leung, On a dual version of the one-dimensional bin packing problem, Journal of Algorithms 5(4), 1984, pp. 502-525"
    title: Assmann, Johnson, Kleitman and Leung 1984
    locator: the definition, next fit covering with ratio 1/2, and the algorithms with asymptotic ratios 2/3 and 3/4
  - paper: "J. Csirik, D. S. Johnson and C. Kenyon, Better approximation algorithms for bin covering, SODA 2001, pp. 557-566"
    title: Csirik, Johnson and Kenyon 2001
    locator: the asymptotic PTAS for bin covering
  - paper: "K. Jansen and R. Solis-Oba, An asymptotic fully polynomial time approximation scheme for bin covering, Theoretical Computer Science 306, 2003, pp. 543-551"
    title: Jansen and Solis-Oba 2003
    locator: the asymptotic FPTAS
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 2, E. G. Coffman, M. R. Garey and D. S. Johnson, Approximation algorithms for bin packing, a survey (the section on bin covering)
---

The bin covering problem is the dual of [bin packing](/bin-packing/): given items with sizes in $(0, 1]$, split as many of them as possible into bins so that each bin has load *at least* 1, and make the number of covered bins as large as possible. It is NP-hard in the strong sense. A simple greedy rule, next fit covering, covers at least half of the optimal number of bins on every input, and no polynomial-time algorithm can promise more than half on every input unless P = NP. Asymptotically the problem is much easier: there are asymptotic approximation schemes.

## In plain words

You have objects of different weights, and you want to fill as many sacks as you can, where a sack counts only if it holds at least a fixed weight. Weight beyond the limit is wasted, and objects left over are wasted too. In bin packing the boxes have a maximum; here the sacks have a minimum.

A fast rule is to fill one sack until it reaches the limit, then start the next sack. Each full sack then holds less than twice the limit, so this rule fills at least half as many sacks as the best way. For large inputs, more careful rules come as close to the best as you want.

## Definition

The input is a list of sizes $s_1, \ldots, s_n$ with $0 < s_i \le 1$. A *cover* with $k$ bins is a family of $k$ pairwise disjoint sets $C_1, \ldots, C_k \subseteq \{1, \ldots, n\}$ with

$$\sum_{i \in C_j} s_i \ge 1 \qquad \text{for each } j = 1, \ldots, k.$$

Items in no set are unused. The goal is to make $k$ as large as possible, and $\mathrm{OPT}$ is the largest $k$. We write $S = \sum_i s_i$. Items of size at least 1 can each cover a bin alone, so the restriction $s_i \le 1$ loses nothing.

*Ratio convention.* This is a maximization problem. An algorithm has absolute ratio $\rho \le 1$ if $\mathrm{ALG} \ge \rho\,\mathrm{OPT}$ on every input, and asymptotic ratio $\rho$ if $\mathrm{ALG} \ge \rho\,\mathrm{OPT} - c$ for a constant $c$. The basic upper bound on $\mathrm{OPT}$ is the size bound $\mathrm{OPT} \le \lfloor S \rfloor$.

## Variants

- **Online bin covering.** Items arrive one by one, and each must be put into a bin at once. Next fit covering has ratio $\frac12$, and no online algorithm does better (Csirik and Totik 1988).
- **Cardinality constraints.** Each bin must also have at least, or at most, a given number of items.
- **Variable sized bins.** Bins of several thresholds, each with a profit.
- **Machine covering.** With a fixed number $m$ of bins, maximize the least load. This is the scheduling problem [machine covering](/machine-covering/), the dual of [makespan minimization](/makespan-minimization/).

## Examples

| list | $S$ | $\mathrm{OPT}$ | next fit covering |
|---|---|---|---|
| $0.6, 0.6, 0.5, 0.5, 0.4, 0.4$ | 3 | 3: $\{0.6, 0.4\}, \{0.6, 0.4\}, \{0.5, 0.5\}$ | 2: $\{0.6, 0.6\}, \{0.5, 0.5\}$, and $0.4, 0.4$ unused |
| $1, \varepsilon, 1, \varepsilon$ with small $\varepsilon$ | about 2 | 2 | 2 |
| $\frac12 + \varepsilon$ four times, then $\frac12 - \varepsilon$ four times | 4 | 4 | 3 |

In the first row, next fit covering puts the two items $0.6$ together and wastes $0.2$ in that bin, and then the two items $0.4$ cannot cover a bin.

## Known algorithms

- **Next fit covering.** Add items to the current bin until its load is at least 1, then start a new bin. It runs in $O(n)$ time.
  *Theorem.* Next fit covering covers at least $\frac12\,\mathrm{OPT}$ bins on every input. *Proof.* Let $a$ be the number of covered bins. In each covered bin, the load before its last item was less than 1, and the last item is at most 1, so the load is less than 2. The items of the unfinished last bin have total less than 1. So $S < 2a + 1$, hence $\lfloor S \rfloor \le 2a$, and $\mathrm{OPT} \le \lfloor S \rfloor \le 2a$. $\square$
- **Sorted rules.** Assmann, Johnson, Kleitman and Leung (1984) sort the items and fill each bin with a large item and small items, or with two medium items. They give algorithms with asymptotic ratios $\frac23$ and $\frac34$, in $O(n \log n)$ time.
- **Asymptotic PTAS.** Csirik, Johnson and Kenyon (2001) give, for each $\varepsilon > 0$, an algorithm with $\mathrm{ALG} \ge (1 - \varepsilon)\,\mathrm{OPT} - O(1)$ for a constant that depends on $\varepsilon$. It uses grouping and a linear program over configurations, in the style of the [asymptotic scheme for bin packing](/bin-packing-aptas/).
- **Asymptotic FPTAS.** Jansen and Solis-Oba (2003) make the running time polynomial in $n$ and $1/\varepsilon$.

## Bounds

| claim | statement | source |
|---|---|---|
| greedy, absolute | next fit covering gives $\mathrm{ALG} \ge \frac12\,\mathrm{OPT}$ | proved above |
| hardness, absolute | no polynomial-time algorithm has $\mathrm{ALG} \ge \rho\,\mathrm{OPT}$ for all inputs with $\rho > \frac12$, unless P = NP | proved below |
| asymptotic | $(1 - \varepsilon)\,\mathrm{OPT} - O_\varepsilon(1)$ for each $\varepsilon > 0$ | Csirik, Johnson and Kenyon 2001 |
| online | ratio $\frac12$, best possible for online algorithms | Csirik and Totik 1988 |

*The absolute bound $\frac12$ is best possible.* Take an instance of [partition](/partition-problem/) with positive integers of total $2B$, each at most $B$ (otherwise the answer is no), and use the items $a_i / B$. Then $S = 2$, so $\mathrm{OPT} \le 2$, and $\mathrm{OPT} = 2$ exactly when the integers split into two halves of sum $B$. Otherwise $\mathrm{OPT} = 1$. An algorithm with $\mathrm{ALG} \ge \rho\,\mathrm{OPT}$ and $\rho > \frac12$ returns more than 1 bin, that is 2 bins, on each yes-instance, so it decides partition.

## Reductions

- **From partition.** The reduction above shows that bin covering is NP-hard, already for deciding whether $\mathrm{OPT} \ge 2$.
- **From 3-partition.** With $3m$ integers in $(B/4, B/2)$ of total $mB$, the items $a_i / B$ give $\mathrm{OPT} = m$ exactly when a 3-partition exists: a bin with load at least $B$ in a cover of $m$ bins with total $mB$ has load exactly $B$, so it has exactly three items. Since [3-partition](/three-partition/) is strongly NP-complete, bin covering is strongly NP-hard, and no FPTAS exists unless P = NP.
- **To machine covering.** With a fixed number of bins, the question "can each of $m$ bins reach load at least $T$" is the decision version of [machine covering](/machine-covering/).

## Applications

- **Packing by minimum weight.** Fruit, fish or other goods of varying weight are packed into boxes that must each reach a stated minimum weight; the packer wants as many boxes as possible.
- **Work assignment.** Split jobs among workers so that as many workers as possible each get at least a full shift of work.
- **Resource splitting.** Divide indivisible assets into as many parts as possible such that each part reaches a value threshold.

## References
