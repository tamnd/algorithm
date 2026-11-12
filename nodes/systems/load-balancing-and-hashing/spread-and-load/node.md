---
tag: QWXEEH
kind: definition
slug: spread-and-load
name: Spread and load
aliases:
- load in consistent hashing
- spread of a ranged hash function
area: systems/load-balancing-and-hashing
level: advanced
summary: "Spread is the number of distinct buckets that one item is sent to across many client views; load is the number of distinct items that one bucket receives across them."
prereqs: [consistent-hashing, balance-property, monotonicity-property]
see_also: [consistent-hashing-max-load-bound, rendezvous-hashing, hash-ring, virtual-nodes, balls-into-bins-max-load, load-balancing-problem, cache, chord]
sources:
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, distributed caching protocols for relieving hot spots on the World Wide Web, STOC 1997
    locator: pp. 654 to 663, Section 4.1 (the spread and load properties of a ranged hash family), Theorem 4.1 parts 3 and 4 (spread and load O(t log C) for the construction with points on the unit interval) and Section 4.4 (Theorem 4.5, spread at most t log(NV) for independent random preference orders)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 4, Section 4.2.1 (Theorem 4.4, the Chernoff bound, including the form Pr(X >= R) <= 2^(-R) for R >= 6 mu)
---

Spread and load are the two properties of a [consistent hash function](/consistent-hashing/) that look at many views at once. Karger et al. defined them in 1997, together with [balance](/balance-property/) and [monotonicity](/monotonicity-property/), for a web cache system in which each client knows only some of the caches. When the clients do not agree on the set of caches, one page can be stored in several caches, and one cache can be asked for more pages than its share. The *spread* of a page is the number of different caches that the clients send it to, so it counts the copies of the page. The *load* of a cache is the number of different pages that some client sends to it, so it counts what the cache must hold. A good scheme keeps both small, of order $t\log C$ when each client knows at least a $1/t$ fraction of the $C$ caches.

## Definition

**Setting.** As for the [balance property](/balance-property/), $\mathcal I$ is the set of items, $\mathcal B$ the set of buckets, a *view* is a nonempty set $\mathcal V \subseteq \mathcal B$, and a ranged hash function $f$ gives a bucket $f_{\mathcal V}(i) \in \mathcal V$ for each view $\mathcal V$ and item $i$. A ranged hash family is a set of such functions with a probability distribution, and the views are fixed before the function is drawn.

**The views (Karger et al., Section 4.1).** Let $\mathcal V_1, \ldots, \mathcal V_V$ be $V$ views that together contain $C$ distinct buckets, and let each view contain at least $C/t$ of them. So $t \ge 1$ measures how little of the system one client knows: $t = 1$ means every client knows every bucket, and $t = 2$ means every client knows at least half of them.

**Spread.** The spread of an item $i$ is the number of distinct buckets that the views send it to:

$$ \sigma(i) \;=\; \bigl|\{\, f_{\mathcal V_1}(i), \ldots, f_{\mathcal V_V}(i) \,\}\bigr|. $$

The spread $\sigma(f)$ of the function, for a given set of items, is the largest spread of an item. A ranged hash family has spread $\sigma$ if, for every choice of views as above, a random function from the family has spread at most $\sigma$ with high probability.

**Load.** The load of a bucket $b$ is the number of distinct items that at least one view sends to it:

$$ \lambda(b) \;=\; \Bigl|\, \bigcup_{j=1}^{V} f_{\mathcal V_j}^{-1}(b) \,\Bigr|, $$

where $f_{\mathcal V}^{-1}(b)$ is the set of items of $\mathcal I$ with $f_{\mathcal V}(i) = b$. The load $\lambda(f)$ of the function is the largest load of a bucket, and a family has load $\lambda$ if, for every choice of views as above, a random function has load at most $\lambda$ with high probability.

**Simple bounds.** Always $1 \le \sigma(i) \le \min(V, C)$ and $\lambda(b) \le |\mathcal I|$. If there is only one view, every item has spread 1 and the load of a bucket is the usual number of items in it, so load generalizes the [maximum load](/load-balancing-problem/) of one assignment.

**Spread and load count the same pairs.** Let $S(i) = \{ f_{\mathcal V_j}(i) : 1 \le j \le V \}$. Then $\sigma(i) = |S(i)|$ and $\lambda(b) = |\{ i : b \in S(i) \}|$, so both sums count the pairs $(i, b)$ with $b \in S(i)$:

$$ \sum_{i \in \mathcal I} \sigma(i) \;=\; \sum_{b \in \mathcal B} \lambda(b). $$

So the average load is $|\mathcal I|/C$ times the average spread. Small spread gives small *average* load, but the *largest* load also needs balance between the buckets.

**A factor $t$ is unavoidable.** Let $t$ be an integer and split the $C$ buckets into $t$ disjoint views of $C/t$ buckets each. Every function sends each item to a different bucket in each view, so every item has spread exactly $t$, whatever the function.

**Spread of a monotone function.** By Theorem 4.3 of Karger et al., a [monotone](/monotonicity-property/) $f$ has an order $\pi(i)$ of the buckets for each item, and $f_{\mathcal V}(i)$ is the first bucket of $\pi(i)$ in $\mathcal V$. So $\sigma(i)$ is the number of distinct first members of the views in the order $\pi(i)$. If every view has a member among the first $K$ buckets of $\pi(i)$, then $\sigma(i) \le K$.

## Examples and non-examples

**A small case.** Take the buckets $a, b, c, d$, so $C = 4$, and the three views $\{a, b, c\}$, $\{b, c, d\}$ and $\{a, c, d\}$, so $t = 4/3$. Let three items have the preference orders $i_1 : a, d, b, c$, $i_2 : c, a, b, d$ and $i_3 : b, a, c, d$. The views send $i_1$ to $a, d, a$, $i_2$ to $c, c, c$ and $i_3$ to $b, b, a$. So the spreads are 2, 1 and 2. The loads are $\lambda(a) = 2$ (items $i_1$ and $i_3$) and $\lambda(b) = \lambda(c) = \lambda(d) = 1$. Both sums are 5.

**Random preference orders (rendezvous hashing).** Let each item have an independent uniform random order $\pi(i)$ of $\mathcal B$. This is the function $\tilde f$ of Karger et al., and [rendezvous hashing](/rendezvous-hashing/) computes it with a hash score per pair of item and bucket. Theorem 4.5 of Karger et al. bounds its spread. Fix $N \ge 1$ and let $K = \lceil t\ln(NV) \rceil$.

*Spread.* The first $K$ buckets of $\pi(i)$ are a uniform random set of $K$ of the $C$ buckets. A view with $s \ge C/t$ buckets misses this set with probability

$$ \prod_{r=0}^{K-1} \frac{C - s - r}{C - r} \;\le\; \Bigl(1 - \frac{s}{C}\Bigr)^{K} \;\le\; \Bigl(1 - \frac1t\Bigr)^{K} \;\le\; e^{-K/t} \;\le\; \frac{1}{NV}. $$

By the [union bound](/union-bound/) over the $V$ views, with probability at least $1 - 1/N$ every view has a member among the first $K$ buckets of $\pi(i)$, and then $\sigma(i) \le K$. Over all items, $\sigma(\tilde f) \le K$ with probability at least $1 - |\mathcal I|/N$.

*Load.* Suppose $|\mathcal I| \le C$. Let $X_b$ be the number of items that have $b$ among the first $K$ buckets of their order. Each item does so with probability $K/C$, independently of the other items, so $X_b$ is a binomial variable with mean $\mu = |\mathcal I|K/C \le K$. If no item has a view that misses its first $K$ buckets, every item in the load of $b$ is counted by $X_b$, so $\lambda(b) \le X_b$. The [Chernoff bound](/chernoff-bound/) $\Pr[X \ge R] \le 2^{-R}$ for $R \ge 6\mu$, with $R = 6K$, and a union bound over the buckets give

$$ \Pr\bigl[\lambda(\tilde f) > 6K\bigr] \;\le\; \frac{|\mathcal I|}{N} + C \cdot 2^{-6K}. $$

Take $N = C^2$. Then $K \ge \ln(C^2 V) \ge 2\ln C$, so $C \cdot 2^{-6K} \le C e^{-4K} \le C^{-7}$, and the failure probability is at most $2/C$. So for $|\mathcal I| \le C$ items, both the spread and the load of $\tilde f$ are $O(t\log(CV))$ with probability at least $1 - 2/C$. This load argument is not the one of Karger et al., who give only a proof sketch for their load bounds.

**The hash ring.** Give each bucket $v$ random points on a circle and send an item to the bucket of the first point clockwise from it, as on a [hash ring](/hash-ring/). The order $\pi(i)$ of the buckets by their first point clockwise from item $i$ is a uniform random order, because the point sets of the buckets are independent and identically distributed. So the spread argument above holds for the ring word for word, for any $v$, and $\sigma \le \lceil t\ln(NV) \rceil$ with probability at least $1 - |\mathcal I|/N$. The load argument does not carry over, because the orders of different items are not independent: two nearby items have almost the same order, and with one point per bucket a bucket with a long arc gets many items in each view that contains it. Karger et al. give each bucket $\kappa\log C$ points and prove spread and load $O(t\log C)$ (Theorem 4.1, for $V = \rho C$ views and $C$ items, with probability $1 - C^{-\Omega(1)}$); the [virtual nodes](/virtual-nodes/) are needed for the load, not for the spread.

**A simulation.** $C = 100$ buckets, $V = 100$ views that are random sets of 50 buckets ($t = 2$), and 100 items, for 5 seeds (Python `random.Random(1000 + s)`). "ring $v$" is the hash ring with $v$ points per bucket, "hrw" is rendezvous hashing, and "mod" sends an item to the bucket with index $h(i) \bmod 50$ in the sorted view.

| scheme | max spread, 5 seeds | mean spread | max load, 5 seeds | mean load |
| --- | --- | --- | --- | --- |
| ring 1 | 9, 9, 9, 9, 9 | 6.75 | 19, 23, 16, 18, 21 | 6.75 |
| ring 5 | 9, 9, 10, 8, 9 | 6.71 | 18, 16, 15, 14, 13 | 6.71 |
| ring 20 | 9, 9, 9, 10, 9 | 6.83 | 17, 13, 13, 14, 14 | 6.83 |
| hrw | 9, 9, 9, 9, 9 | 6.76 | 12, 15, 16, 12, 15 | 6.76 |
| mod | 28, 25, 24, 24, 23 | 18.06 | 26, 32, 33, 33, 30 | 18.06 |

The mean spread and the mean load are equal because $|\mathcal I| = C$. The spread is about the same for all the monotone schemes, and $t\ln C = 9.21$ is close to the largest value seen. The largest load falls as the points per bucket increase, and rendezvous hashing is about as low as the ring with 20 points per bucket. With $N = 10^4$ the bounds above give $K = 28$, so spread at most 28 and load at most 168 with probability at least 0.99; the bounds are far from the observed values, but they hold for every choice of views.

**Mod-n hashing: high spread.** In each view the mod rule is [balanced](/balance-property/), but the position $h(i) \bmod |\mathcal V|$ points to an unrelated bucket in each view. In the simulation its mean spread is 18.06, about 2.7 times that of the monotone schemes, and by the identity above its mean load is 2.7 times larger too. So balance in each view does not give small spread.

**Disjoint views.** As above, $t$ disjoint views force spread $t$ on every function. This is not a defect of a scheme: the clients do not share a bucket, so each needs its own copy.

**One order for all items.** If every item uses the same order of $\mathcal B$, every view sends all items to its first member in that order. The spread of each item is the number of distinct first members, which can be small, but one bucket can receive every item, so the load is $|\mathcal I|$. Small spread does not give small load.

## Related definitions

- **[Balance](/balance-property/).** The same question in one view: each bucket gets $O(1/|\mathcal V|)$ of the items. Load with $V = 1$ is the item count of balance.
- **[Monotonicity](/monotonicity-property/).** Items move only to new buckets when buckets are added. A monotone function sends an item, in every view, to the first bucket of one order $\pi(i)$, and this is what keeps the spread low when the order is random.
- **Universality.** Karger et al. call a family universal if its restriction to each view is a universal hash family. Together with monotonicity it gives the expected fraction $|\mathcal V_1 \cap \mathcal V_2|/|\mathcal V_1 \cup \mathcal V_2|$ of items that two views send to the same bucket, which is the spread question for two views.
- **Maximum load.** In [load balancing](/load-balancing-problem/) and [balls into bins](/balls-into-bins-max-load/) the load of a bin is a count in one assignment. Load here is a count over the union of many assignments, so it is at least the largest of the counts in the single views.
- **Copies in caches.** In a web [cache](/cache/) system, spread is the number of copies of a page and load is the number of distinct pages that a cache must hold. Karger et al. combine consistent hashing with random trees of caches, which spread the requests for one popular page; spread and load measure only the disagreement between the views.

## References
