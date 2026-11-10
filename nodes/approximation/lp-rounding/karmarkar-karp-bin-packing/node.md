---
tag: P2QGMB
kind: algorithm
slug: karmarkar-karp-bin-packing
name: Karmarkar-Karp bin packing
aliases:
- Karmarkar-Karp asymptotic bin packing
- Karmarkar-Karp algorithm
area: approximation/lp-rounding
level: advanced
summary: Group item sizes geometrically, solve the configuration LP, pack the integer part of a vertex, and repeat on the rest; the result uses OPT + O(log^2 OPT) bins.
solves: [bin-packing]
model: real-ram
complexity:
  vars: {n: the number of items, L: the time to solve one configuration LP to within an additive 1}
  time: {worst: O(L log n + n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1982
  people: [Narendra Karmarkar, Richard M. Karp]
  note: Karmarkar and Karp showed how to solve the Gilmore-Gomory configuration LP approximately in polynomial time and how to round it with geometric grouping, which gives OPT + O(log^2 OPT) bins; this stood as the best additive bound until Rothvoss (2013).
prereqs: [bin-packing, configuration-lp, basic-feasible-solution, first-fit-decreasing, asymptotic-ptas]
see_also: [configuration-lp, bin-packing-aptas, fernandez-de-la-vega-lueker-aptas, cutting-stock-problem, column-generation, ellipsoid-method, first-fit-bin-packing, bin-packing-inapproximability]
sources:
  - paper: doi:10.1109/SFCS.1982.61
    title: Narendra Karmarkar and Richard M. Karp, An efficient approximation scheme for the one-dimensional bin-packing problem, 23rd Symposium on Foundations of Computer Science, 1982
    locator: the approximate solution of the LP and the geometric grouping (OPT + O(log^2 OPT))
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 4.6 (bin packing, with the configuration LP and the O(log^2 OPT) rounding)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 9 (bin packing), notes
  - title: Rebecca Hoberg and Thomas Rothvoss, A logarithmic additive integrality gap for bin packing, Proceedings of the 28th ACM-SIAM Symposium on Discrete Algorithms, 2017
    locator: the OPT + O(log OPT) bound
---

The Karmarkar-Karp algorithm packs items of sizes in $(0, 1]$ into unit [bins](/bin-packing/) with $\text{OPT} + O(\log^2 \text{OPT})$ bins, an additive error that is tiny next to OPT. It rounds the [configuration LP](/configuration-lp/) of Gilmore and Gomory, which has a variable for each way to fill one bin. Each round puts aside the small items, groups the large items by size classes that double, rounds sizes up within each group, and solves the LP of the rounded items. A vertex of this LP has few nonzero values, so packing $\lfloor x_C \rfloor$ bins of each configuration $C$ leaves only a small amount of items. Those items form the next round. The size of the rest at least halves each round, so there are $O(\log \text{OPT})$ rounds, and each round loses $O(\log \text{OPT})$ bins to grouping. This page uses an exact LP solver on small inputs. The real algorithm solves the LP to within an additive 1 in polynomial time with the ellipsoid method.

## In plain words

Sort the items by size into bands: those bigger than one half, those between a quarter and a half, and so on. In each band, put the items in groups, and treat each item as being as big as the largest one in its group. Now there are few different sizes. Throw away the group of the biggest items in each band for later.

Next, find the best way to fill bins if a fraction of a bin pattern were allowed. A corner answer uses only a few patterns. Fill as many whole bins as each pattern allows. The fractional part holds very few items, so repeat with those items.

At the end, pack the items you threw away and the tiny items with a simple greedy rule. Few bins are lost at each step, and there are few steps.

## The problem

The input is $n$ items with sizes $s_1, \ldots, s_n \in (0, 1]$. A packing splits them into bins, each of total size at most 1, and the aim is the fewest bins, OPT. Write $\text{SIZE}(I) = \sum_i s_i$, so $\text{OPT} \ge \text{SIZE}(I)$. For a multiset $I$ with distinct sizes $v_1, \ldots, v_d$ and counts $b_1, \ldots, b_d$, a configuration is a vector $a \in \mathbb{Z}_{\ge 0}^d$ with $\sum_t a_t v_t \le 1$. The configuration LP is

$$\text{LP}(I) = \min \sum_C x_C \ \text{ s.t. } \sum_C a_{C, t} \, x_C \ge b_t \ (t = 1, \ldots, d), \quad x \ge 0.$$

Every packing gives a 0-1 point, so $\text{LP}(I) \le \text{OPT}$, and $\text{LP}(I) \ge \text{SIZE}(I)$, since each configuration holds total size at most 1. The configurations allow any number of copies of a size, not just $b_t$; the proof needs this. The bounds are asymptotic: deciding whether OPT is 2 is NP-hard by [partition](/partition-problem/), so no ratio below $3/2$ is possible, but an additive error is.

## The algorithm

```pseudo id=main
KARMARKAR-KARP(s)
L1  g ← min(1/2, 1 / SIZE(I));  J ← the items of size at least g;  S ← the others;  D ← ∅
L2  while J ≠ ∅ do
L3      group J geometrically: class l holds sizes in (2^(-l-1), 2^(-l)]; sort each class by size and cut it into groups of k · 2^l items; move the first group of each class to D, and round each other item up to the largest size in its group; call the rounded multiset J'
L4      find a vertex x of the configuration LP of J'
L5      for each configuration C, open ⌊x_C⌋ bins and fill each with items of J' as C prescribes
L6      J ← the items of J' that were not packed, with their true sizes
L7  pack D by first fit decreasing, using the existing bins and new bins
L8  pack S by first fit, using the existing bins and new bins
L9  return the bins
```

The grouping parameter is $k = 4$ in the analysis. Line L5 places a true item in the place of its rounded size, so each bin holds at most 1. A configuration may ask for more copies of a size than are left, and then the extra places stay empty. Line L4 needs a vertex, also called a [basic solution](/basic-feasible-solution/), because a vertex has at most $d$ nonzero values, one for each row. The configuration LP has exponentially many columns, but its dual has a separation problem that is a [knapsack problem](/knapsack-problem/). Karmarkar and Karp solve the LP to within an additive 1 with a variant of the [ellipsoid method](/ellipsoid-method/). In practice, [column generation](/column-generation/) solves it well.

## Example

The items have sizes $0.6, 0.6, 0.5, 0.5, 0.4, 0.4, 0.3, 0.3, 0.2$, numbered 1 to 9. Then $\text{SIZE} = 3.8$, so $g = 5/19 \approx 0.263$, and item 9 of size $0.2$ is small. To show the grouping on a small input, take $k = 1$: groups of 1 item in class 0 and of 2 items in class 1.

| class | sizes | groups | discarded to $D$ | rounded |
|---|---|---|---|---|
| 0, $(1/2, 1]$ | 0.6, 0.6 | $\{1\}, \{2\}$ | item 1 (0.6) | item 2 → 0.6 |
| 1, $(1/4, 1/2]$ | 0.5, 0.5, 0.4, 0.4, 0.3, 0.3 | $\{3, 4\}, \{5, 6\}, \{7, 8\}$ | items 3, 4 (0.5, 0.5) | items 5, 6 → 0.4; items 7, 8 → 0.3 |

Here $\text{LP}(J) = 11/3$ and $J' = \{0.6, 0.4, 0.4, 0.3, 0.3\}$ with $\text{LP}(J') = 2$. The vertex has $x = 1$ on the two configurations $(0.6, 0.4)$ and $(0.4, 0.3, 0.3)$. So line L5 opens two full bins, $\{2, 5\}$ and $\{6, 7, 8\}$, and nothing is left, so the loop ends after one round. The round packed $2 \le \text{LP}(J) - \text{LP}(\emptyset) = 11/3$ bins, as the proof requires.

Line L7 packs $D = \{0.6, 0.5, 0.5\}$, of size $1.6$, by first fit decreasing. The two bins are full, so item 1 opens bin 3, and items 3 and 4 share bin 4. Line L8 puts item 9 into bin 3, which then holds $0.8$. The result has 4 bins: $\{2, 5\}$, $\{6, 7, 8\}$, $\{1, 9\}$ and $\{3, 4\}$. This is optimal, since $\text{SIZE} = 3.8$; the LP of all items is $23/6$.

## Correctness

**Theorem (Karmarkar and Karp 1982).** With $k = 4$, the algorithm returns a valid packing with at most $\text{OPT} + O(\log^2 \text{OPT})$ bins. More precisely, with $\lambda = \log_2 \max(2, \text{SIZE}(I))$, the number of bins is at most $\max \big( \text{LP}(I) + 2 \cdot 4 (2\lambda + 1)(\lambda + 1) + 1, \ \text{SIZE}(I) + 3 \big)$.

The proof is in full in the proof file below. Its steps are:

1. *Grouping does not raise the LP.* Each rounded group is no larger, item by item, than the group before it, which is kept or discarded. So $J'$ is dominated by $J$, and $\text{LP}(J') \le \text{LP}(J)$. The proof uses the dual LP.
2. *Packed bins are paid for.* The fractional parts $x_C - \lfloor x_C \rfloor$ are feasible for the items left over. So the bins of line L5 number at most $\text{LP}(J) - \text{LP}(J_{\text{next}})$, and the sum over all rounds telescopes to at most $\text{LP}(I)$.
3. *The rest halves.* $\text{SIZE}(J_{\text{next}}) \le \text{LP}(J_{\text{next}})$ is less than the number of distinct sizes of $J'$. That number is at most $2 \, \text{SIZE}(J) / k$, since class $l$ has items of size more than $2^{-l-1}$ and groups of $k \cdot 2^l$. With $k = 4$, the size halves each round. Every large item has size at least $g$, so there are at most $\log_2(\text{SIZE}(I)/g) + 1$ rounds.
4. *Discards are small.* Each class discards $k \cdot 2^l$ items of size at most $2^{-l}$, so at most $k$ in size, and there are at most $\log_2(1/g) + 1$ classes. First fit decreasing opens at most $2 \, \text{SIZE}(D) + 1$ new bins.
5. *Small items are cheap.* If first fit opens a bin for a small item, all other bins are more than $1 - g$ full at the end. So the count is less than $\text{SIZE}(I) / (1 - g) + 1 \le \text{SIZE}(I) + 3$.

**The lower bound used.** $\text{LP}(I)$ and $\text{SIZE}(I)$, both at most OPT.

**Hardness.** Bin packing is [strongly NP-hard](/strong-np-hardness/), and ratio below $3/2$ is NP-hard; see [bin packing inapproximability](/bin-packing-inapproximability/). No result rules out $\text{OPT} + 1$ in polynomial time.

## Complexity

- **Time.** The number of rounds is $O(\log \text{SIZE}(I)) = O(\log n)$, and each round solves one LP with at most $n$ rows, in time $L$. Karmarkar and Karp give a polynomial $L$, for the LP solved to within an additive 1; this adds at most 1 bin per round, which the bound absorbs. The grouping and the packing of each round take $O(n \log n)$ time. First fit takes $O(n \log n)$ time with a tree of bin loads. The total is $O(L \log n + n \log n)$ in the worst case. The implementation below lists all configurations and solves the LP exactly, so it is for small inputs only.
- **Space.** The items, the groups and a vertex with at most $n$ nonzero values take $O(n)$ extra space, besides the LP solver.

## Properties

- **Additive guarantee.** The bound is $\text{OPT} + O(\log^2 \text{OPT})$, so the ratio tends to 1 as OPT grows. The error is much smaller than the $\varepsilon \cdot \text{OPT}$ of an [asymptotic PTAS](/asymptotic-ptas/).
- **Relative to the LP.** The proof bounds the bins by $\text{LP}(I) + O(\log^2 \text{SIZE})$, so it also shows that the integrality gap of the configuration LP is $O(\log^2 \text{OPT})$ in additive terms.
- **Deterministic.** With a fixed LP solver and fixed tie-breaking, the output depends only on the input.
- **Not online.** All items must be known, since the grouping and the LP use all of them.

## Variants and improvements

- **Linear grouping.** Grouping all large items into equal groups, as in [Fernandez de la Vega and Lueker](/fernandez-de-la-vega-lueker-aptas/), with one LP round, gives $(1 + \varepsilon)\text{OPT} + O(1/\varepsilon^2)$; see [bin packing APTAS](/bin-packing-aptas/).
- **Better rounding.** Rothvoss (2013) used discrepancy methods to get $\text{OPT} + O(\log \text{OPT} \cdot \log \log \text{OPT})$. Hoberg and Rothvoss (2017) got $\text{OPT} + O(\log \text{OPT})$, which bounds the additive integrality gap of the configuration LP by $O(\log \text{OPT})$.
- **The modified integer round-up conjecture.** It is conjectured that the configuration LP has additive gap at most 1, so that $\lceil \text{LP} \rceil + 1$ bins always suffice; no instance with gap more than 1 is known.
- **Cutting stock.** The same LP, with item demands, is the [cutting stock problem](/cutting-stock-problem/), and the same rounding applies.

## When to use it

Use the idea when OPT is large and a few bins matter, as in cutting stock with long orders. The full algorithm with the ellipsoid method is slow, but column generation solves the configuration LP fast in practice. Then the floor of the LP solution plus a greedy packing of the rest is a strong heuristic. For small inputs, first fit decreasing, which uses at most $\frac{11}{9}\text{OPT} + \frac{6}{9}$ bins, or an exact solver is a better choice.

## Pitfalls

- **Bounding the copies in a configuration.** If a configuration may hold at most $b_t$ copies of size $v_t$, the fractional parts need not be feasible for the leftover items, and step 2 of the proof fails. Configurations must allow any number of copies that fit.
- **Using an optimal point that is not a vertex.** The bound on the leftover size uses that a vertex has at most $d$ nonzero values. A point in the middle of a face can have many fractional values and leave a large rest.
- **Forgetting to discard the first group.** Rounding the first group up is safe only because it is set aside. Without the discard, $J'$ is not dominated by $J$, and $\text{LP}(J')$ can exceed $\text{LP}(J)$.
- **Taking $k$ too small.** With $k < 2$, the size of the rest need not shrink, and the number of rounds is not logarithmic. The loop still ends, since each round discards at least one item.

## Implementations

## History

Gilmore and Gomory (1961) introduced the configuration LP for the cutting stock problem and solved it by column generation. Fernandez de la Vega and Lueker (1981) gave the first asymptotic approximation scheme for bin packing, with linear grouping. Karmarkar and Karp (1982) showed how to solve the configuration LP approximately in polynomial time and how to round it with geometric grouping, for $\text{OPT} + O(\log^2 \text{OPT})$. This stayed the best additive bound for over thirty years, until Rothvoss (2013) and then Hoberg and Rothvoss (2017) brought it to $O(\log \text{OPT})$.

## References
