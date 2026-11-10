---
tag: XKC6Z1
kind: algorithm
slug: epstein-levin-eptas-bin-packing
name: Epstein-Levin EPTAS for bin packing
aliases:
- Epstein-Levin scheme
- robust APTAS for bin packing
- Epstein-Levin robust APTAS
area: approximation/approximation-schemes
level: research
summary: Asymptotic approximation scheme for bin packing that runs in time f(ε) n log n and, as items arrive, moves only a bounded amount of them per arrival.
solves: [bin-packing]
model: real-ram
complexity:
  vars: {n: the number of items, ε: the accuracy parameter, f: a function of ε alone}
  time: {worst: "O(f(ε) n log n)"}
  space: {extra: "O(f(ε) + n)"}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 2006
  people: [Leah Epstein, Asaf Levin]
  note: Epstein and Levin gave a robust asymptotic scheme for bin packing at ICALP 2006, in which items arrive one by one and each arrival moves items of total size at most a function of ε times the size of the new item.
prereqs: [bin-packing, asymptotic-ptas, configuration-lp, fernandez-de-la-vega-lueker-aptas]
see_also: [eptas, bin-packing-aptas, karmarkar-karp-bin-packing, first-fit-bin-packing, bin-packing-lower-bound, job-migration, eisenbrand-weismantel-proximity-theorem, integer-programming-fixed-dimension]
sources:
  - paper: "L. Epstein and A. Levin, A robust APTAS for the classical bin packing problem, Mathematical Programming 119(1), 2009, pp. 33-49"
    title: Epstein and Levin 2009
    locator: the robust APTAS with its three kinds of steps, the use of the proximity theorem, the migration factor, and the concluding remark on bins of size 1 + ε
  - paper: "L. Epstein and A. Levin, A robust APTAS for the classical bin packing problem, Proceedings of ICALP 2006, LNCS 4051"
    title: Epstein and Levin 2006
    locator: the conference version
  - paper: doi:10.1007/BF02579456
    title: W. Fernandez de la Vega and G. S. Lueker, Bin packing can be solved within 1 + ε in linear time, Combinatorica 1(4), 1981, pp. 349-355
    locator: linear grouping, which the scheme revises
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Corollary 17.2a (the proximity theorem of Cook, Gerards, Schrijver and Tardos), as quoted by Epstein and Levin
---

The scheme of Epstein and Levin packs items into bins as they arrive and keeps, after each arrival, a packing with at most $(1 + \varepsilon)\,\mathrm{OPT} + 1$ bins. When an item of size $s$ arrives, it may move other items, but their total size is at most $\beta(\varepsilon)\, s$; this bound $\beta$ is the *migration factor*, and a scheme with such a bound is called *robust*. Run on a fixed list, it is an asymptotic scheme for [bin packing](/bin-packing/) in time $f(\varepsilon)\, n \log n$, so the exponent of $n$ does not grow with $1/\varepsilon$, as in an [EPTAS](/eptas/). The key idea is to write the packing of the large items as an integer vector of bin patterns and to use the proximity theorem of integer programming: when one item arrives, the right side of the program changes by 1, so some new solution is close to the old one, and only a few bins change. This page is an outline. It proves the simplest variant from the paper, with bins of size $1 + \varepsilon$, and sketches the main scheme.

## In plain words

Boxes of different sizes arrive one at a time, and we put them on shelves of equal length. We want few shelves, but we may also move boxes that are already on shelves, as long as we never move much more than the box that just came.

We treat the large boxes as if they were a little longer, so that there are only a few lengths. Then a shelf is described by the list of lengths on it, and the whole packing by how many shelves have each list. When a box arrives, we look for a new count of lists that is close to the old one. A known theorem about whole-number equations says such a close count exists. So only a few shelves are rebuilt. Small boxes go to the first shelf with room.

## The problem

Items of sizes $s_1, s_2, \ldots \in (0, 1]$ arrive one at a time. After item $t$ arrives, the algorithm must hold a packing of $s_1, \ldots, s_t$ into bins, and $\mathrm{OPT}(t)$ is the least number of unit bins for them. On each arrival, the algorithm may move items between bins; the *migration factor* is the largest ratio of the total size moved to the size of the new item. The goal is a packing with at most $(1 + \varepsilon)\,\mathrm{OPT}(t) + 1$ unit bins at all times, a migration factor bounded by a function of $\varepsilon$, and little work per arrival. Offline bin packing is NP-hard, so an exact packing is out of reach even without arrivals; see the [asymptotic PTAS](/asymptotic-ptas/) for why the additive term is needed.

## The algorithm

The pseudocode is the variant from the concluding remarks of the paper: bins of size $1 + \varepsilon$, and at most $\mathrm{OPT}(t)$ of them. Large items are those of size at least $\varepsilon/4$. A *pattern* is a multiset of rounded sizes with sum at most $1 + \varepsilon$, the empty one included. The state is the vector $y$ that counts the bins of each pattern, so that $A y = (u, B)$, where the matrix $A$ has one row per rounded size and a row of ones, $u$ counts the large items by rounded size, and $B$ is the number of bins. $d$ is the number of patterns and $\Delta$ the largest absolute subdeterminant of $A$.

```pseudo id=main
ROBUST-INSERT(s, ε)
L1  if s < ε/4: put s into the first bin with room by Any Fit, or open a new bin if none has room; return
L2  round s up to r, the next power of 1 + ε/4, and add 1 to the count u_r
L3  let y be the pattern vector of the B bins before the arrival
L4  if the rounded items fit in B bins: find y' ≥ 0 with A y' = (u, B) and ‖y' − y‖∞ least, which is at most 3dΔ
L5  else: open a new bin that holds s alone; return
L6  keep min(y_p, y'_p) bins of each pattern p, refill the others by the patterns of y', and put their small items back by Any Fit
```

Line L4 is where the proximity theorem enters. The old vector $y$ solves the program with right side $(u - e_r, B)$, and the new right side differs by 1 in one entry, so some solution $y'$ lies within $d \Delta (1 + 2)$ of $y$ in every coordinate. Line L6 then empties at most $3 d^2 \Delta$ bins. The rounding is fixed when an item arrives, so the rounded instance only grows.

**The main scheme.** With bins of size 1, the paper calls items of size less than $\varepsilon/2$ small and keeps the large items in the groups of a revised form of the linear grouping of [Fernandez de la Vega and Lueker](/fernandez-de-la-vega-lueker-aptas/), with $m = 2/\varepsilon^2$ and between $4m + 1$ and $8m + 1$ groups of equal size. Each arrival is a regular step, in which the largest item of each group moves up to the next group, or one of two steps that create or join sets of groups. Each step changes the rounded instance in a bounded way, and the proximity theorem bounds the change of the pattern vector, as in line L4.

## Example

Take $\varepsilon = 1/2$, so bins have size $3/2$ and sizes round up to powers of $9/8$. The items $9/20$, $3/5$, $3/5$, $9/20$ arrive in this order. The size $9/20$ rounds to $(8/9)^6 \approx 0.4933$, called $b$, and $3/5$ rounds to $(8/9)^4 \approx 0.6243$, called $a$. There are $d = 7$ patterns: the empty one, $a$, $b$, $aa$, $ab$, $bb$ and $bbb$, and $\Delta = 6$.

| arrival | rounded items fit in $B$ bins? | bins after | patterns after | bins emptied | size moved |
|---|---|---|---|---|---|
| $9/20$ | no, $B = 0$ | $\{9/20\}$ | $b$ | 0 | 0 |
| $3/5$ | yes, as $ab$ | $\{3/5, 9/20\}$ | $ab$ | 1 | $9/20$ |
| $3/5$ | no, $a + a + b > 3/2$ | $\{3/5, 9/20\}$, $\{3/5\}$ | $ab$, $a$ | 0 | 0 |
| $9/20$ | yes, as $aa$ and $bb$ | $\{3/5, 3/5\}$, $\{9/20, 9/20\}$ | $aa$, $bb$ | 2 | $33/20$ |

At the last arrival, the vector moves from one $ab$ and one $a$ to one $aa$ and one $bb$, a change of 1 in four coordinates, far below the bound $3 d \Delta = 126$. The final packing has 2 bins of size $3/2$, while 3 unit bins are needed, since $3/5 + 9/20 > 1$.

## Correctness

**Theorem (the variant with bins of size $1 + \varepsilon$).** After every arrival, every item is in a bin, every bin has load at most $1 + \varepsilon$, and the number of bins is at most $\mathrm{OPT}(t)$. On the arrival of a large item $s$, the items moved have total size at most $12 (1 + \varepsilon) d^2 \Delta / \varepsilon$ times $s$; a small item moves nothing.

The proof file has these steps.

1. **Rounding.** A large item grows by a factor less than $1 + \varepsilon/4$, so the rounded items of an optimal packing fit in $\mathrm{OPT}(t)$ bins of size $1 + \varepsilon$. Proved in full.
2. **New bins.** Any Fit opens a bin only when every bin has load more than 1, and line L5 runs only when the rounded items need more than $B$ bins; in both cases $\mathrm{OPT}(t)$ exceeds the old count. Proved in full.
3. **Proximity.** Line L4 always finds $y'$ within $3 d \Delta$. Proved from the proximity theorem of Cook, Gerards, Schrijver and Tardos, which is cited, not proved.
4. **Refilling.** The items of the emptied bins and the new item fill exactly the new bins of line L6, and at most $3 d^2 \Delta$ bins are emptied. Proved in full.
5. **The main scheme.** With bins of size 1 and revised linear grouping, at most $(1 + \varepsilon)\,\mathrm{OPT}(t) + 1$ bins. Sketch, after Epstein and Levin.

## Complexity

- **Patterns.** At most $c \le 1 + \log_{1 + \varepsilon/4}(4/\varepsilon)$ rounded sizes and $d \le \binom{c + q}{q}$ patterns, with $q = \lfloor 4(1 + \varepsilon)/\varepsilon \rfloor$. By Hadamard's inequality, $\Delta \le (q \sqrt{c + 1})^{c + 1}$. All are functions of $\varepsilon$ alone.
- **Time.** Epstein and Levin bound the work per arrival by $f(\varepsilon) \log n$, so a list of $n$ items takes $O(f(\varepsilon)\, n \log n)$ time.
- **Migration.** At most $12 (1 + \varepsilon) d^2 \Delta / \varepsilon$ in the variant; the main scheme also has a migration factor that depends on $\varepsilon$ only.
- **The code.** It tests feasibility by a table over all count vectors and searches the box around $y$, which is exponential in the counts and is meant for small checks only.

## Properties

- **Online with repacking.** Items are packed at once on arrival, but earlier items may move, within the migration factor.
- **Deterministic.**
- **Efficient.** The running time has the form $f(\varepsilon)\, n \log n$.
- **Rounding once.** The rounded size of an item never changes, which is what keeps each change of the program small.

## Variants and improvements

- **Bins of size $1 + \varepsilon$.** The variant in the pseudocode, from the concluding remarks of the paper: at most $\mathrm{OPT}(t)$ bins, with all large items rounded to powers of $1 + \varepsilon/4$.
- **Offline schemes.** [Fernandez de la Vega and Lueker](/fernandez-de-la-vega-lueker-aptas/) and [Karmarkar and Karp](/karmarkar-karp-bin-packing/) pack a fixed list; the second one uses only $O(\log^2 \mathrm{OPT})$ extra bins.
- **Stronger proximity bounds.** The [Eisenbrand-Weismantel proximity theorem](/eisenbrand-weismantel-proximity-theorem/) gives a bound that does not grow with the number of columns, in place of the factor $d$ in line L4.

## When to use it

Use the scheme when items arrive over time, the packing must stay near optimal, and moving items costs in proportion to their size, such as virtual machines on servers. For a fixed list, an offline scheme or [First Fit](/first-fit-bin-packing/) after sorting is simpler. The constants $d$ and $\Delta$ grow very fast as $\varepsilon$ falls, so the scheme is mainly of theoretical interest.

## Pitfalls

- **Rounding again.** If the rounded sizes are recomputed on each arrival, many coordinates of the right side can change at once, and the proximity bound no longer gives a small change.
- **The migration factor of small items.** A small new item may not move large items, since the bound is relative to its size; this is why small items go by Any Fit only.
- **The empty pattern.** The program fixes the number of bins with the row of ones, so the empty pattern must be a column, or the old and new solutions cannot have the same number of bins.
- **Asymptotic only.** Without an additive term, no polynomial algorithm has a ratio below $3/2$ unless P = NP, as for offline bin packing, so the $+1$ of the main scheme is needed.

## Implementations

## History

Epstein and Levin presented the robust scheme at ICALP 2006, and the journal version appeared in Mathematical Programming in 2009. It combines the linear grouping of Fernandez de la Vega and Lueker from 1981 with the proximity theorem of Cook, Gerards, Schrijver and Tardos from 1986. Later work extended robust schemes to other packing problems and to settings where items also leave.

## References
