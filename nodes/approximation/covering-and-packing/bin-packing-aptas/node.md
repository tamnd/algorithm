---
tag: SC1BGZ
kind: algorithm
slug: bin-packing-aptas
name: Asymptotic PTAS for bin packing
aliases:
- Fernandez de la Vega-Lueker algorithm
- APTAS for bin packing
- linear grouping scheme
area: approximation/covering-and-packing
level: advanced
summary: Approximation scheme giving (1+eps)OPT plus O(1) bins for any fixed eps.
solves: [bin-packing]
model: real-ram
complexity:
  vars: {n: the number of items, ε: the accuracy parameter}
  time: {worst: "n^O(1/ε^2)", average: "n^O(1/ε^2)", best: "n^O(1/ε^2)"}
  space: {extra: "n^O(1/ε^2)"}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1981
  people: [Wenceslas Fernandez de la Vega, George S. Lueker]
  note: Fernandez de la Vega and Lueker introduced linear grouping and the asymptotic scheme in 1981.
prereqs: [bin-packing, asymptotic-ptas, bin-packing-lower-bound, first-fit-bin-packing, bin-packing-np-hardness]
see_also: [fernandez-de-la-vega-lueker-aptas, karmarkar-karp-bin-packing, epstein-levin-eptas-bin-packing, configuration-lp, first-fit-decreasing, ptas, bin-packing-inapproximability]
sources:
  - paper: "W. Fernandez de la Vega and G. S. Lueker, Bin packing can be solved within 1 + epsilon in linear time, Combinatorica 1(4), 1981, pp. 349-355"
    title: Fernandez de la Vega and Lueker 1981
    locator: the linear grouping lemma and the main theorem
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 3.3 (an asymptotic polynomial-time approximation scheme for bin packing)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 9 (an asymptotic PTAS for bin packing)
  - paper: "N. Karmarkar and R. M. Karp, An efficient approximation scheme for the one-dimensional bin-packing problem, FOCS 1982, pp. 312-320"
    title: Karmarkar and Karp 1982
    locator: the configuration LP and the bound OPT + O(log^2 OPT)
  - paper: "R. Hoberg and T. Rothvoss, A logarithmic additive integrality gap for bin packing, SODA 2017"
    title: Hoberg and Rothvoss 2017
    locator: the bound OPT + O(log OPT)
---

The asymptotic PTAS for [bin packing](/bin-packing/) is a family of algorithms, one for each $\varepsilon > 0$, that uses at most $(1 + \varepsilon)\,\mathrm{OPT} + 1$ bins and runs in time $n^{O(1/\varepsilon^2)}$. It combines three ideas: drop the small items and add them back greedily at the end, round the sizes of the large items by *linear grouping* so that only a constant number of distinct sizes remain, and solve the rounded instance exactly. No polynomial-time algorithm has an absolute ratio below $\frac32$ unless P = NP, so the additive term is needed. This page gives the general scheme with a full proof. The original paper, with its linear time version, is on [Fernandez de la Vega and Lueker](/fernandez-de-la-vega-lueker-aptas/).

## In plain words

Bin packing is hard because there are many different sizes. So you make the sizes simpler. First you put the tiny objects aside: they are easy, because at the end you can push them into gaps one by one, and they waste little space.

Then you sort the big objects and cut the sorted row into groups of equal count. In each group you treat every object as if it were as big as the biggest one in the group. Now there are only a few distinct sizes, and you can try all the ways to fill a box and find the best packing exactly. Making objects bigger costs at most a few extra boxes, and those extra boxes are a small part of the total when the input is large.

## The problem

The input is a list of $n$ sizes $s_1, \ldots, s_n$ in $(0, 1]$ and an accuracy $\varepsilon \in (0, 1]$. The output is a packing into unit bins. We write $S = \sum_i s_i$ and $\mathrm{OPT}$ for the least number of bins.

*Ratio convention.* The guarantee $\mathrm{ALG} \le (1 + \varepsilon)\,\mathrm{OPT} + 1$ is asymptotic: the ratio $\mathrm{ALG}/\mathrm{OPT}$ tends to at most $1 + \varepsilon$ as $\mathrm{OPT}$ grows, with an additive 1. A scheme with this property for each fixed $\varepsilon$ is an [asymptotic PTAS](/asymptotic-ptas/). The analysis uses two [lower bounds on OPT](/bin-packing-lower-bound/): the size bound $S \le \mathrm{OPT}$, and $\mathrm{OPT}(X) \le \mathrm{OPT}$ for each sub-list $X$.

## The algorithm

```pseudo id=main
APTAS(s[1 .. n], ε)
L1  δ ← ε/2; let I_L be the items with s[i] ≥ δ, sorted by decreasing size; n' ← |I_L|; K ← ⌊δ² n'⌋
L2  if K = 0 then pack I_L optimally (n' < 1/δ² is a constant) and go to L6
L3  cut I_L into groups G_1, G_2, ..., G_g of K consecutive items (the last group may be smaller)
L4  J ← the items of G_2, ..., G_g, each rounded up to the largest size in its group
L5  pack J optimally by dynamic programming over the counts of each size, put the original items into the slots of their rounded copies, and give each item of G_1 its own bin
L6  add the items with s[i] < δ by first fit, opening a new bin only when no bin has room
L7  return the bins
```

Line L5 is exact because $J$ has at most $2/\delta^2$ distinct sizes and each bin holds at most $1/\delta$ items, so the number of bin types (*configurations*) is a constant. The dynamic program computes, for each vector of remaining counts, the least number of bins, by trying each configuration for the bin of the first remaining item.

## Example

Take $\varepsilon = 1$, so $\delta = \frac12$, and the list of 14 items with large sizes $0.9, 0.8, 0.7, 0.65, 0.6, 0.55, 0.5, 0.5$ and small sizes $0.3, 0.2, 0.2, 0.1, 0.1, 0.1$.

| step | result |
|---|---|
| L1 | $n' = 8$ large items, $K = \lfloor \frac14 \cdot 8 \rfloor = 2$ |
| L3 | $G_1 = \{0.9, 0.8\}$, $G_2 = \{0.7, 0.65\}$, $G_3 = \{0.6, 0.55\}$, $G_4 = \{0.5, 0.5\}$ |
| L4 | $J$ = two items each of $0.7$, $0.6$, $0.5$ |
| L5 | optimal for $J$: five bins, $[0.7]$, $[0.7]$, $[0.6]$, $[0.6]$, $[0.5\ 0.5]$; with the originals and $G_1$: $[0.65]$, $[0.7]$, $[0.55]$, $[0.6]$, $[0.5\ 0.5]$, $[0.9]$, $[0.8]$ |
| L6 | first fit adds the small items: $[0.65\ 0.3]$, $[0.7\ 0.2\ 0.1]$, $[0.55\ 0.2\ 0.1\ 0.1]$, $[0.6]$, $[0.5\ 0.5]$, $[0.9]$, $[0.8]$ |

The result has 7 bins. The 8 large items need 7 bins, since only the two items of size $0.5$ can share a bin, so this is optimal. The guarantee is $(1+1) \cdot 7 + 1 = 15$; on small inputs the bound is loose, and the scheme is meant for large inputs and small $\varepsilon$.

## Correctness

The proof has three steps, each with a lower bound on $\mathrm{OPT}$.

1. **Rounding costs at most $K$ bins.** Map the $t$-th item of $G_h$ to the $t$-th item of $G_{h-1}$. The rounded size of an item of $G_h$ is the largest size in $G_h$, which is at most the smallest size in $G_{h-1}$. So $J$ is dominated item by item by a sub-list of $I_L$, and $\mathrm{OPT}(J) \le \mathrm{OPT}(I_L)$. The $K$ items of $G_1$ take $K$ more bins.
2. **$K$ is small.** Each large item has size at least $\delta$, so $\delta n' \le \mathrm{OPT}(I_L)$ and $K \le \delta^2 n' \le \delta\,\mathrm{OPT}(I_L)$. So the large items use at most $(1 + \delta)\,\mathrm{OPT}$ bins.
3. **Small items waste little.** If first fit opens a new bin for a small item, all other bins have load more than $1 - \delta$, so the count is less than $\frac{S}{1-\delta} + 1 \le (1 + 2\delta)\,\mathrm{OPT} + 1$.

With $\delta = \varepsilon/2$ the total is at most $(1 + \varepsilon)\,\mathrm{OPT} + 1$. The full proof, with the running time, is below.

## Complexity

- **Time.** The rounded instance has $d \le 2/\delta^2 = 8/\varepsilon^2$ distinct sizes. The dynamic program has at most $(n+1)^d$ states and at most $(1/\delta + 1)^d$ configurations, so the time is $n^{O(1/\varepsilon^2)}$, in the [real RAM](/real-ram/) model. This is polynomial for each fixed $\varepsilon$ but not in $1/\varepsilon$.
- **Space.** The table of the dynamic program has $n^{O(1/\varepsilon^2)}$ entries.

## Properties

| claim | statement | status |
|---|---|---|
| guarantee | $\mathrm{ALG} \le (1 + \varepsilon)\,\mathrm{OPT} + 1$ for $0 < \varepsilon \le 1$ | proved below |
| large items | the large items use at most $(1 + \varepsilon/2)\,\mathrm{OPT}$ bins | proved below |
| time | $n^{O(1/\varepsilon^2)}$ | proved below |
| additive term needed | no polynomial-time algorithm has $\mathrm{ALG} \le \rho\,\mathrm{OPT}$ with $\rho < \frac32$ for all lists, unless P = NP | [hardness theorem](/bin-packing-np-hardness/) |
| no FPTAS for the ratio | bin packing is strongly NP-hard | [hardness theorem](/bin-packing-np-hardness/) |

## Variants and improvements

- **Linear time.** Fernandez de la Vega and Lueker solve the rounded instance with a linear program over the configurations instead of the dynamic program, and get time linear in $n$ for fixed $\varepsilon$; see [their page](/fernandez-de-la-vega-lueker-aptas/).
- **Asymptotic FPTAS.** [Karmarkar and Karp](/karmarkar-karp-bin-packing/) solve the [configuration LP](/configuration-lp/) approximately and use geometric grouping. This gives $(1 + \varepsilon)\,\mathrm{OPT} + O(1/\varepsilon^2)$ bins in time polynomial in $n$ and $1/\varepsilon$, and also $\mathrm{OPT} + O(\log^2 \mathrm{OPT})$ bins in polynomial time.
- **Logarithmic additive term.** Hoberg and Rothvoss (2017) give $\mathrm{OPT} + O(\log \mathrm{OPT})$ bins, by rounding the configuration LP with discrepancy methods.
- **Efficient schemes.** The running time can be made $f(1/\varepsilon) + O(n \log n)$; see [the EPTAS of Epstein and Levin](/epstein-levin-eptas-bin-packing/).
- **Other problems.** The same pattern (remove small items, group, enumerate configurations, add small items back) gives asymptotic schemes for [bin covering](/bin-covering/), for [strip packing](/strip-packing/) (Kenyon and Rémila) and for many scheduling problems.

## When to use it

The scheme is a theoretical tool. It shows that bin packing is as easy to approximate as an NP-hard problem can be in the asymptotic sense. For practical instances, the exponent $1/\varepsilon^2$ is far too large, and [first fit decreasing](/first-fit-decreasing/) or column generation on the [cutting stock](/cutting-stock-problem/) model is the better choice. The grouping lemma itself is a useful step in many proofs.

## Pitfalls

- **The additive term is essential.** The scheme does not give $(1 + \varepsilon)\,\mathrm{OPT}$. On lists with $\mathrm{OPT} = 2$, no polynomial algorithm can always find 2 bins unless P = NP.
- **Group size.** The group size must be about $\delta^2 n'$, not $\delta n'$ or a constant. With a constant group size, there are too many distinct sizes and the exact step is not polynomial. With a larger group size, the $K$ extra bins are no longer at most $\delta\,\mathrm{OPT}$.
- **Round up, not down.** Rounding down gives an instance that is easier than the original, and its packing may not be feasible for the original items.
- **Small items last.** Small items must be added after the large items are packed, and the threshold for small must be the same $\delta$ that bounds the number of large items per bin.

## Implementations

## History

Fernandez de la Vega and Lueker (1981) gave the first asymptotic scheme, with linear grouping and a linear program over configurations. The version with exact dynamic programming over count vectors, as on this page, is the standard textbook form (Vazirani, Chapter 9; Williamson and Shmoys, Section 3.3). Karmarkar and Karp (1982) gave the asymptotic FPTAS and the bound $\mathrm{OPT} + O(\log^2 \mathrm{OPT})$, and Hoberg and Rothvoss (2017) improved it to $\mathrm{OPT} + O(\log \mathrm{OPT})$.

## References
