---
tag: SZNNHA
kind: algorithm
slug: fernandez-de-la-vega-lueker-aptas
name: Fernandez de la Vega-Lueker APTAS for bin packing
aliases:
- FdlV-L APTAS
- Fernandez de la Vega-Lueker scheme
- linear grouping with the configuration LP
area: approximation/approximation-schemes
level: advanced
summary: Round item sizes to few distinct values, pack the rounded instance by linear programming, then place the small items greedily.
solves: [bin-packing]
model: real-ram
complexity:
  vars: {n: the number of items, ε: the accuracy parameter, c: an absolute constant}
  time: {worst: "O(n log n + (1/ε)^(c/ε^4))", average: "O(n log n + (1/ε)^(c/ε^4))", best: "O(n log n + (1/ε)^(c/ε^4))"}
  space: {extra: "O(n + (1/ε)^(c/ε^4))"}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1981
  people: [Wenceslas Fernandez de la Vega, George S. Lueker]
  note: Fernandez de la Vega and Lueker showed that bin packing can be solved within a factor 1 + ε in linear time, with linear grouping and a linear program over bin configurations.
prereqs: [bin-packing, asymptotic-ptas, bin-packing-lower-bound, configuration-lp, simplex-method, lp-duality]
see_also: [bin-packing-aptas, karmarkar-karp-bin-packing, epstein-levin-eptas-bin-packing, first-fit-bin-packing, bin-packing-inapproximability, basic-feasible-solution, bland-rule, cutting-stock-problem]
sources:
  - paper: doi:10.1007/BF02579456
    title: W. Fernandez de la Vega and G. S. Lueker, Bin packing can be solved within 1 + ε in linear time, Combinatorica 1(4), 1981, pp. 349-355
    locator: the grouping step, the linear program over configurations and the main theorem
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 9 (bin packing, the asymptotic PTAS with the additive 1)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 3.3 (an asymptotic polynomial-time approximation scheme for bin packing)
  - paper: "R. G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 1977, pp. 103-107"
    title: Bland 1977
    locator: the smallest index rule and its proof that the simplex method does not cycle
  - paper: "N. Karmarkar and R. M. Karp, An efficient approximation scheme for the one-dimensional bin-packing problem, FOCS 1982, pp. 312-320"
    title: Karmarkar and Karp 1982
    locator: the configuration LP solved approximately and geometric grouping
---

The Fernandez de la Vega-Lueker scheme (1981) was the first asymptotic approximation scheme for [bin packing](/bin-packing/). For each $\varepsilon \in (0, 1]$ it packs $n$ items into at most $(1 + \varepsilon)\,\mathrm{OPT} + 1$ unit bins, in time $O(n \log n)$ plus a term that depends on $\varepsilon$ alone. The scheme has three steps. It sets the small items aside. It rounds the large items up by *linear grouping*, so that only $O(1/\varepsilon^2)$ distinct sizes remain. It then solves the [configuration LP](/configuration-lp/) of the rounded instance and rounds a basic optimal solution up. A basic solution has few positive entries, so the rounding costs few bins. The [general scheme page](/bin-packing-aptas/) solves the rounded instance by dynamic programming instead; this page follows the paper and uses the linear program.

## In plain words

Bin packing is hard because there can be many different object sizes. First, put the tiny objects aside. At the end they fill gaps one by one and waste little room.

Sort the big objects and cut the sorted row into groups of equal count. Treat each object as if it were as big as the biggest object in its group. Now only a few sizes remain, and there are only a few ways to fill one box with such objects. Ask a linear program how many boxes of each fill pattern to use. It may answer with fractions, so round each count up. The best answer of the program uses few patterns, so rounding up adds only a few boxes. These extra boxes, and the boxes for the biggest group, are a small part of the total when the input is large.

## The problem

The input is a list of $n$ sizes $s_1, \ldots, s_n \in (0, 1]$ and an accuracy $\varepsilon \in (0, 1]$. The output is a packing into unit bins, that is, a partition of the items into bins of total size at most 1 each. We write $S = \sum_i s_i$ and $\mathrm{OPT}$ for the least number of bins.

*Ratio convention.* The guarantee $\mathrm{ALG} \le (1 + \varepsilon)\,\mathrm{OPT} + 1$ is asymptotic: the ratio $\mathrm{ALG}/\mathrm{OPT}$ is at most $1 + \varepsilon + 1/\mathrm{OPT}$, which tends to $1 + \varepsilon$ as $\mathrm{OPT}$ grows. A family with this property for every fixed $\varepsilon$ is an [asymptotic PTAS](/asymptotic-ptas/). The proof uses two [lower bounds on OPT](/bin-packing-lower-bound/): the size bound $S \le \mathrm{OPT}$, and $\mathrm{OPT}(X) \le \mathrm{OPT}$ for each sub-list $X$.

*Configurations.* Let the rounded instance $J$ have the distinct sizes $\sigma_1 > \cdots > \sigma_d$, with $b_t$ items of size $\sigma_t$. A configuration is a vector $C = (a_1, \ldots, a_d)$ of non-negative integers, not all zero, with $\sum_t a_t \sigma_t \le 1$: the contents of one bin. The configuration LP has one variable $x_C \ge 0$ per configuration, the number of bins filled as $C$:
$$\min \sum_C x_C \quad \text{subject to} \quad \sum_C a_t(C)\, x_C \ge b_t \ \text{ for } t = 1, \ldots, d.$$

## The algorithm

```pseudo id=main
FDLV-L(s[1 .. n], ε)
L1  δ ← ε/2
L2  I_L ← the items with s[i] ≥ δ, sorted by decreasing size; n' ← |I_L|
L3  if n' < 2/δ⁴ then pack I_L optimally (its size depends on ε alone) and go to L9
L4  K ← ⌊δ² n'⌋; cut I_L into groups G_1, ..., G_g of K consecutive items (the last group may be smaller)
L5  J ← the items of G_2, ..., G_g, each rounded up to the first (largest) size of its group
L6  solve the configuration LP of J by the simplex method; let x be the basic optimal solution
L7  for each configuration C, open ⌈x_C⌉ bins with the slots of C, and put each item of J, with its original size, into a free slot of its rounded size; drop the empty bins
L8  give each item of G_1 its own bin
L9  place each item with s[i] < δ into the first bin with room, or into a new bin if no bin has room
L10 return the bins
```

The sorting in line L2 is the only step that is not linear for fixed $\varepsilon$. The paper reaches linear time with selection instead of a full sort: line L4 needs only the items at ranks $1, K+1, 2K+1, \ldots$, which are $O(1/\varepsilon^2)$ order statistics.

## Example

Take $\varepsilon = 1$, so $\delta = \frac12$. The list has 12 large items $0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.6, 0.55, 0.5, 0.5, 0.5$ and 5 small items $0.3, 0.2, 0.2, 0.1, 0.1$. Here $n' = 12 < 2/\delta^4 = 32$, so line L3 would pack the large items exactly. To show the other steps on a small list, the trace below skips the test of line L3.

| step | result |
|---|---|
| L4 | $K = \lfloor \frac14 \cdot 12 \rfloor = 3$; $G_1 = \{0.9, 0.85, 0.8\}$, $G_2 = \{0.75, 0.7, 0.65\}$, $G_3 = \{0.6, 0.6, 0.55\}$, $G_4 = \{0.5, 0.5, 0.5\}$ |
| L5 | $J$ has three items each of size $0.75$, $0.6$ and $0.5$, so $d = 3$ and $b = (3, 3, 3)$ |
| L6 | the configurations are $[0.75]$, $[0.6]$, $[0.5]$ and $[0.5\ 0.5]$; the optimum is $x = (3, 3, 0, \frac32)$ with value $\frac{15}{2}$, and it has $3 = d$ positive entries |
| L7 | $3 + 3 + 0 + 2 = 8$ bins: $[0.65]$, $[0.7]$, $[0.75]$, $[0.55]$, $[0.6]$, $[0.6]$, $[0.5\ 0.5]$, $[0.5]$ |
| L8 | three more bins, $[0.9]$, $[0.85]$, $[0.8]$, for 11 bins in all |
| L9 | $0.3$ and $0.2$ go into $[0.5]$, which becomes full; $0.2$, $0.1$, $0.1$ go into $[0.55]$, which reaches load $0.95$ |

The result has 11 bins. This is optimal: the 9 items larger than $\frac12$ need a bin each, and no item of size $0.5$ fits next to them, so the three items of size $0.5$ need two more bins. The LP value $\frac{15}{2}$ is a lower bound for the rounded instance, and rounding it up cost half a bin here. The guarantee $(1 + 1) \cdot 11 + 1 = 23$ is loose on so small a list.

## Correctness

The proof bounds the bins of each step by a lower bound on $\mathrm{OPT}$.

1. **Grouping.** The rounded size of an item of $G_h$ is at most the smallest size of $G_{h-1}$. So each item of $J$ is at most a distinct item of $I_L$, and $\mathrm{OPT}(J) \le \mathrm{OPT}(I_L) \le \mathrm{OPT}$. The $K$ items of $G_1$ take $K \le \delta^2 n' \le \delta\,\mathrm{OPT}$ more bins, since $\delta n' \le \mathrm{OPT}$.
2. **The LP and its rounding.** The final simplex tableau of the dual LP gives a primal solution $x$ that is feasible, optimal, and has at most $d$ positive entries, because at most $d$ slack variables leave the basis. So $\sum_C \lceil x_C \rceil \le \mathrm{LP}^* + d \le \mathrm{OPT}(J) + d$. With $n' \ge 2/\delta^4$ we have $d < 2/\delta^2 \le \delta\,\mathrm{OPT}$. The large items use at most $(1 + 2\delta)\,\mathrm{OPT}$ bins.
3. **Small items.** If line L9 opens a new bin, every other bin has load more than $1 - \delta$. So the count $B$ satisfies $(B - 1)(1 - \delta) < S \le \mathrm{OPT}$, and $B \le (1 + 2\delta)\,\mathrm{OPT} + 1$ for $\delta \le \frac12$.

With $2\delta = \varepsilon$ the total is at most $(1 + \varepsilon)\,\mathrm{OPT} + 1$. The full proof is below.

## Complexity

- **Time.** Sorting costs $O(n \log n)$; the paper uses selection and gets $O(n)$ for fixed $\varepsilon$. The rounded instance has $d < 8/\varepsilon^2$ sizes and each configuration holds at most $2/\varepsilon$ items, so there are at most $\binom{d + 2/\varepsilon}{d} = 2^{O((1/\varepsilon) \log(1/\varepsilon))}$ configurations, and the LP has a size that depends on $\varepsilon$ alone. The exact step of line L3 on fewer than $32/\varepsilon^4$ items costs $2^{O(\varepsilon^{-4} \log(1/\varepsilon))}$ by trying all assignments, and this term dominates the dependence on $\varepsilon$. Line L9 runs in $O(1)$ per item if it keeps a list of the bins with load at most $1 - \delta$, since the proof needs only that a new bin opens when every bin is above $1 - \delta$. The model is the [real RAM](/real-ram/).
- **Space.** $O(n)$ for the items and bins, plus the LP and the exact step, whose sizes depend on $\varepsilon$ alone.

## Properties

| claim | statement | status |
|---|---|---|
| guarantee | $\mathrm{ALG} \le (1 + \varepsilon)\,\mathrm{OPT} + 1$ for $0 < \varepsilon \le 1$ | proved below |
| grouping | $\mathrm{OPT}(J) \le \mathrm{OPT}(I_L)$ and $J$ has fewer than $n'/K$ distinct sizes | proved below |
| basic solution | the LP solution has at most $d$ positive entries, so rounding up adds at most $d$ bins | proved below |
| time | $O(n \log n)$ plus a term in $\varepsilon$ alone; $O(n)$ with selection | proved below; linear time from the paper |
| additive term needed | no polynomial algorithm has $\mathrm{ALG} \le \rho\,\mathrm{OPT}$ with $\rho < \frac32$ on all lists, unless P = NP | [inapproximability](/bin-packing-inapproximability/) |

## Variants and improvements

- **Dynamic programming instead of the LP.** The rounded instance can be packed exactly by a dynamic program over count vectors, in time $n^{O(1/\varepsilon^2)}$. This gives the bound without the threshold of line L3 but is not linear; see the [general scheme](/bin-packing-aptas/).
- **Asymptotic FPTAS.** [Karmarkar and Karp](/karmarkar-karp-bin-packing/) solve the configuration LP only approximately, by the ellipsoid method on the dual with a knapsack separation oracle, and replace linear grouping by geometric grouping. The time is polynomial in $n$ and $1/\varepsilon$, and the bound is $\mathrm{OPT} + O(\log^2 \mathrm{OPT})$.
- **Efficient and robust schemes.** [Epstein and Levin](/epstein-levin-eptas-bin-packing/) keep an asymptotic $(1 + \varepsilon)$ packing while the items arrive, with a bounded number of moved items per arrival.
- **Cutting stock.** When there are few sizes with large counts, the same configuration LP is the Gilmore-Gomory model of the [cutting stock problem](/cutting-stock-problem/), and the rounding of a basic solution is the standard way to turn it into a packing.

## When to use it

The scheme is mainly a theoretical tool. It shows that the asymptotic ratio of bin packing can be made as close to 1 as we like, in linear time for each fixed $\varepsilon$. The constants are huge for small $\varepsilon$, so on real inputs [first fit](/first-fit-bin-packing/) or first fit decreasing, or column generation on the configuration LP, is a better choice. The two lemmas, linear grouping and the support bound of a basic solution, are reused in many approximation schemes for packing and scheduling.

## Pitfalls

- **The threshold.** The bound $d \le \delta\,\mathrm{OPT}$ needs $n' \ge 2/\delta^4$. Below it the LP route can lose up to $d$ bins on an instance with small $\mathrm{OPT}$, so the large items must be packed exactly there.
- **Basic solutions only.** Rounding up an arbitrary optimal LP solution can add one bin for each of many configurations. The bound of $d$ extra bins needs a basic solution, such as the one the simplex method returns.
- **Round up, not down.** Rounding sizes down gives an easier instance whose packing may be infeasible for the original items.
- **Cycling.** The configuration LP is degenerate in many cases. A pivot rule without an anti-cycling guarantee, such as the most negative reduced cost alone, can cycle; [Bland's rule](/bland-rule/) does not.
- **Exact arithmetic.** Floating-point simplex can return a solution that is not quite feasible, and rounding $x_C = 2.0000001$ up opens an extra bin. Exact fractions or a tolerance with a final feasibility check avoid this.

## Implementations

## History

Fernandez de la Vega and Lueker (1981) gave the result in the paper "Bin packing can be solved within 1 + ε in linear time". They introduced linear grouping, the restriction to large items with a greedy completion, and the use of a linear program over bin configurations whose basic solutions have few positive entries. The form with the additive term 1, as on this page, is the textbook statement (Vazirani, Chapter 9). Karmarkar and Karp (1982) turned the configuration LP into an asymptotic FPTAS.

## References
