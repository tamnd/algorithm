---
tag: 9N457B
kind: definition
slug: gross-substitutes
name: Gross substitutes
aliases:
- gross substitutes condition
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: A valuation has gross substitutes if raising some prices never makes the buyer drop an item whose price stayed the same. With such buyers, a Walrasian equilibrium of indivisible goods exists.
prereqs: [submodular-function, competitive-equilibrium]
see_also: [kelso-crawford-process, demange-gale-sotomayor-auction, combinatorial-auction, demand-query, matroid, submodular-function, tatonnement, assignment-game]
sources:
  - paper: doi:10.2307/1913392
    title: Alexander S. Kelso and Vincent P. Crawford, Job matching, coalition formation, and gross substitutes, Econometrica 50(6), 1483 to 1504 (1982)
    locator: the whole paper (the condition for firms that hire many workers, and the existence of equilibrium)
  - paper: doi:10.1006/jeth.1999.2531
    title: Faruk Gul and Ennio Stacchetti, Walrasian equilibrium with gross substitutes, Journal of Economic Theory 87(1), 95 to 124 (1999)
    locator: the whole paper (equivalent conditions, and gross substitutes as the largest class that contains unit demand and always has an equilibrium)
  - paper: doi:10.1007/s00199-001-0248-5
    title: Hans Reijnierse, Anita van Gellekom and Jos A. M. Potters, Verifying gross substitutability, Economic Theory 20(4), 767 to 776 (2002)
    locator: the whole paper (the local conditions on triples of goods)
  - paper: doi:10.1287/moor.28.3.463.16393
    title: Satoru Fujishige and Zaifu Yang, A note on Kelso and Crawford's gross substitutes condition, Mathematics of Operations Research 28(3), 463 to 469 (2003)
    locator: the whole paper (gross substitutes is the same as M-natural concavity)
  - paper: doi:10.1016/j.geb.2017.10.016
    title: Renato Paes Leme, Gross substitutability, an algorithmic survey, Games and Economic Behavior 106, 294 to 316 (2017)
    locator: Definition 1.3, Theorem 1.4 and Section 2 (examples, and the sum of matroid ranks that is not gross substitutes)
---

Gross substitutes is a condition on a buyer's valuation over bundles of indivisible goods: when some prices go up, the buyer never gives up a good whose price did not change. It is the condition under which markets for indivisible goods behave like markets for divisible goods: a Walrasian equilibrium exists, an ascending auction finds it, and welfare can be maximized with polynomially many [demand queries](/demand-query/). It is stronger than [submodularity](/submodular-function/), which only asks for decreasing marginal values, and weaker than unit demand, the case of the [DGS auction](/demange-gale-sotomayor-auction/).

## Definition

There are $m$ indivisible goods. A *valuation* is a function $v$ from bundles $S \subseteq \{1, \ldots, m\}$ to the reals with $v(\varnothing) = 0$. At a price vector $p$, the utility of $S$ is $v(S) - p(S)$ with $p(S) = \sum_{j \in S} p_j$, and the *demand set* is
$$D(v, p) = \arg\max_{S} \, \bigl(v(S) - p(S)\bigr).$$

**Gross substitutes (Kelso and Crawford 1982).** $v$ has gross substitutes when for all price vectors $p \le p'$ and every $S \in D(v, p)$ there is $T \in D(v, p')$ with
$$\{j \in S : p_j = p'_j\} \subseteq T.$$

In words: after a price rise, the buyer can keep every demanded good whose price did not rise. The condition allows ties in the demand set, so it asks only for some demanded bundle $T$.

Several conditions are equivalent to gross substitutes:

- **Local exchange conditions** (Reijnierse, van Gellekom and Potters 2002). For every bundle $S$ and distinct goods $i, j, k \notin S$ (writing $Sij$ for $S \cup \{i, j\}$),
$$v(Sij) + v(S) \le v(Si) + v(Sj), \qquad v(Sij) + v(Sk) \le \max\bigl(v(Sik) + v(Sj),\ v(Sjk) + v(Si)\bigr).$$
  These conditions involve only bundles that differ by at most three goods, so they can be checked with $O(2^m m^3)$ value queries.
- **M-natural concavity** (Fujishige and Yang 2003). Gross substitutes valuations are exactly the M-natural concave set functions of discrete convex analysis, which gives a link to valuated matroids.
- **Single improvement** (Gul and Stacchetti 1999). If a bundle is not demanded, the buyer can raise her utility by adding one good, removing one good, or swapping one good for another.

## Examples and non-examples

- **Additive** valuations, $v(S) = \sum_{j \in S} w_j$, have gross substitutes: each good is bought on its own.
- **Unit demand**, $v(S) = \max_{j \in S} w_j$: the buyer wants one good. This is the case of the [assignment game](/assignment-game/).
- **Assignment (OXS) valuations**: the buyer has several slots, slot $s$ values good $j$ at $w_{sj}$, and $v(S)$ is the largest total value of putting goods of $S$ in distinct slots. Firms that fill several positions in a job market have such valuations. They include additive and unit-demand valuations.
- **Weighted [matroid](/matroid/) rank functions** and, more generally, valuated matroids. For example, $v(S)$ is the total weight of the $k$ heaviest goods of $S$.
- **Complements are excluded.** If $v(\{a, b\}) = 3$ and $v(\{a\}) = v(\{b\}) = 0$, then at prices $(1, 1)$ the buyer wants both, and when the price of $b$ rises to $3$ she drops $a$, whose price did not change.
- **Submodular is not enough.** The budget-additive valuation $v(S) = \min(w(S), 4)$ with weights $(2, 2, 3)$ is submodular. But with $S = \varnothing$ and goods $a, b, c$, $v(ab) + v(c) = 7$ while $v(ac) + v(b) = v(bc) + v(a) = 6$, so it breaks the second local condition.
- **Sums of gross substitutes valuations need not have it.** Paes Leme (2017) gives the sum $v = r^a + 2r^b + 3r^c$ of three matroid rank functions on goods $a, b, c$, where $r^i$ is $1$ on a single good and on the pair without $i$ and $2$ on the other pairs and on $\{a, b, c\}$. At prices $(4, 5, 4)$ the demand set is $\{a\}, \{c\}, \{a, c\}, \{b, c\}$. When the price of $c$ rises very high, the only demanded bundle is $\{a\}$, so the bundle $\{b, c\}$ loses $b$, whose price did not change.

The Python code for this page checks both forms on small examples. One check tests the definition directly on a grid of price vectors for 3 goods. The other tests the local conditions. On all 148 monotone valuations on 3 goods with values in $\{0, 1, 2\}$, exactly 34 pass the local conditions, and the two checks agree on a random sample of these valuations.

## Related definitions

- **Walrasian equilibrium.** Kelso and Crawford (1982) showed that an equilibrium exists when every buyer has gross substitutes; see [competitive equilibrium](/competitive-equilibrium/). Gul and Stacchetti (1999) showed the converse in a strong form: if a class of valuations contains all unit-demand valuations and always has an equilibrium, it lies inside gross substitutes.
- **Ascending auctions.** The [Kelso-Crawford process](/kelso-crawford-process/) and the exact auction of Gul and Stacchetti (2000) need gross substitutes so that no bidder must give back a good. In a [combinatorial auction](/combinatorial-auction/) with gross substitutes bidders, welfare maximization is solvable in polynomial time with demand queries, and the linear program over bundles has an integral optimum.
- **Submodularity.** Every gross substitutes valuation is submodular (Gul and Stacchetti 1999); the budget-additive example shows the converse fails.
- **Gross substitutes for divisible goods.** In general equilibrium theory, gross substitutes is a condition on aggregate demand: raising one price does not lower the demand for any other good. It makes the [tatonnement](/tatonnement/) process converge. The condition on this page is the version for one buyer and indivisible goods.
- **Substitutes in matching with contracts.** Hatfield and Milgrom (2005) use a substitutes condition on choice functions over contracts; with money, it is related to gross substitutes.

## References
