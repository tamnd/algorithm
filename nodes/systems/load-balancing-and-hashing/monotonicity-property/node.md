---
tag: A1VFRT
kind: definition
slug: monotonicity-property
name: Monotonicity property
aliases:
- minimal disruption
- monotone ranged hash function
area: systems/load-balancing-and-hashing
level: core
summary: "A ranged hash function is monotone if, when buckets are added to a view, items move only to the new buckets, never between old ones. Mod-n hashing fails it; consistent hashing has it."
prereqs: [consistent-hashing, balance-property]
see_also: [spread-and-load, rendezvous-hashing, jump-consistent-hash, maglev-hashing, bounded-load-consistent-hashing, hash-ring, rehashing, dynamic-partitioning-problem]
sources:
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, distributed caching protocols for relieving hot spots on the World Wide Web, STOC 1997
    locator: pp. 654 to 663, Section 4.1 (the monotonicity property), Theorem 4.1 part 1 (the construction is monotone), Section 4.4 (Theorem 4.3, monotone functions are those given by a permutation per item; Theorem 4.4, the expected fraction |V1 ∩ V2| / |V1 ∪ V2| of items that keep their bucket)
  - paper: doi:10.1109/90.663936
    title: David G. Thaler and Chinya V. Ravishankar, Using name-based mappings to increase hit rates, IEEE/ACM Transactions on Networking 6(1), 1998
    locator: pp. 1 to 14, the highest random weight mapping and its minimal disruption when a server is removed
  - url: https://arxiv.org/abs/1406.2294
    title: John Lamping and Eric Veach, A fast, minimal memory, consistent hash algorithm, arXiv:1406.2294, 2014
    locator: the introduction (monotonicity as the requirement that keys move only to a new bucket when the number of buckets grows)
  - url: https://www.usenix.org/conference/nsdi16/technical-sessions/presentation/eisenbud
    title: Daniel E. Eisenbud et al., Maglev, a fast and reliable software network load balancer, NSDI 2016
    locator: Section 3.4 (Consistent Hashing, the goals of load balancing and minimal disruption)
---

The monotonicity property is the property of a [consistent hash function](/consistent-hashing/) that, when buckets are added to the set of usable buckets, each item either stays where it is or moves to one of the new buckets; no item moves from one old bucket to another. Karger et al. defined it in 1997 as one of four properties of a ranged hash family, with [balance](/balance-property/) and [spread and load](/spread-and-load/). The plain rule $h(i) \bmod n$ fails it badly: going from $n$ to $n + 1$ buckets moves $n/(n+1)$ of the items. The [hash ring](/hash-ring/), [rendezvous hashing](/rendezvous-hashing/) and, for buckets numbered $0$ to $n-1$, [jump consistent hash](/jump-consistent-hash/) have it.

## Definition

The setting is that of the [balance property](/balance-property/): items $\mathcal I$, buckets $\mathcal B$, views $\emptyset \ne \mathcal V \subseteq \mathcal B$, and a ranged hash function $f$ with $f_{\mathcal V}(i) \in \mathcal V$.

**Monotonicity (Karger et al., Section 4.1).** A ranged hash function $f$ is *monotone* if for all views $\mathcal V_1 \subseteq \mathcal V_2 \subseteq \mathcal B$ and all items $i$,

$$ f_{\mathcal V_2}(i) \in \mathcal V_1 \;\Longrightarrow\; f_{\mathcal V_1}(i) = f_{\mathcal V_2}(i). $$

A ranged hash family is monotone if every function in it is monotone. The condition is deterministic: it must hold for every function of the family, not only with high probability.

**Two readings of one condition.** Read from $\mathcal V_1$ to $\mathcal V_2$, it says that after buckets are *added*, an item is either still in its old bucket or in a new bucket of $\mathcal V_2 \setminus \mathcal V_1$. Read from $\mathcal V_2$ to $\mathcal V_1$, it says that after buckets are *removed*, every item whose bucket is still there keeps it, and only the items of removed buckets move. So stability under removal and stability under addition are the same property.

**Characterization by preference orders (Theorem 4.3).** $f$ is monotone if and only if there is an order $\pi(i)$ of $\mathcal B$ for each item $i$ such that $f_{\mathcal V}(i)$ is the first bucket of $\pi(i)$ that lies in $\mathcal V$.

*Proof.* If $f$ has this form and $f_{\mathcal V_2}(i) = b \in \mathcal V_1 \subseteq \mathcal V_2$, then every bucket before $b$ in $\pi(i)$ is outside $\mathcal V_2$, so outside $\mathcal V_1$, and $b$ is in $\mathcal V_1$; so $b$ is the first bucket of $\pi(i)$ in $\mathcal V_1$. Conversely, let $f$ be monotone and $\mathcal B$ finite. Define $b_1 = f_{\mathcal B}(i)$ and $b_{j+1} = f_{\mathcal B \setminus \{b_1, \ldots, b_j\}}(i)$; this lists all of $\mathcal B$. For a view $\mathcal V$, let $b_j$ be its first member in this list and $\mathcal W = \mathcal B \setminus \{b_1, \ldots, b_{j-1}\}$. Then $\mathcal V \subseteq \mathcal W$ and $f_{\mathcal W}(i) = b_j \in \mathcal V$, so monotonicity gives $f_{\mathcal V}(i) = b_j$. $\square$

**How many items keep their bucket (Theorem 4.4).** Let $f$ be monotone. For views $\mathcal V_1, \mathcal V_2$ and $\mathcal W = \mathcal V_1 \cup \mathcal V_2$, an item has $f_{\mathcal V_1}(i) = f_{\mathcal V_2}(i)$ if and only if $f_{\mathcal W}(i) \in \mathcal V_1 \cap \mathcal V_2$. Indeed, let $u = f_{\mathcal W}(i)$. If $u \in \mathcal V_1 \cap \mathcal V_2$, monotonicity applied to $\mathcal V_1 \subseteq \mathcal W$ and to $\mathcal V_2 \subseteq \mathcal W$ gives $f_{\mathcal V_1}(i) = u = f_{\mathcal V_2}(i)$. If $u \in \mathcal V_1 \setminus \mathcal V_2$, then $f_{\mathcal V_1}(i) = u \notin \mathcal V_2$, while $f_{\mathcal V_2}(i) \in \mathcal V_2$, so they differ; the case $u \in \mathcal V_2 \setminus \mathcal V_1$ is the same. If in addition each item of the view $\mathcal W$ goes to a uniform bucket of $\mathcal W$ (the per-item form of balance with $\beta = 1$, which Karger et al. get from universality), the expected fraction of items that keep their bucket is

$$ \frac{|\mathcal V_1 \cap \mathcal V_2|}{|\mathcal V_1 \cup \mathcal V_2|}. $$

Adding one bucket to $n$ moves $1/(n+1)$ of the items in expectation. A balanced scheme must give the new bucket about $1/(n+1)$ of the items, so no scheme moves fewer in expectation; this is the "smoothness" that Karger et al. describe in words in their introduction.

## Examples and non-examples

**Mod-n hashing: the standard non-example.** Number the buckets of a view in a fixed order and let $f_{\mathcal V}(i)$ be the bucket with index $h(i) \bmod |\mathcal V|$. Take $\mathcal V_1 = \{b_0, b_1, b_2\}$ and $\mathcal V_2 = \mathcal V_1 \cup \{b_3\}$. An item with $h(i) = 4$ goes to $b_{4 \bmod 4} = b_0 \in \mathcal V_1$ in $\mathcal V_2$ but to $b_{4 \bmod 3} = b_1$ in $\mathcal V_1$, so the implication fails. Of the items with $h(i) = 0, \ldots, 11$, only those with $h(i) = 0, 1, 2$ keep their bucket; the items with $h(i) = 4, 5, 6, 8, 9, 10$ move from one old bucket to another. In general, by the Chinese remainder theorem the pair $(h \bmod n, h \bmod (n+1))$ takes each value once as $h$ runs over $n(n+1)$ consecutive integers, and the pairs $(r, r)$ come from $h \equiv r$ for $r = 0, \ldots, n-1$. So exactly $1/(n+1)$ of the items keep their bucket and $n/(n+1)$ move, against the $1/(n+1)$ that a monotone scheme moves. For $n = 10$, 100000 random 64-bit hashes (Python `random.Random(5)`) had 90.78% of the items move, against $10/11 = 90.91\%$.

**The hash ring.** Each bucket has one or more points on a circle, and an item goes to the bucket of the first point clockwise from it. It is monotone: if the first point clockwise of item $i$ among the points of $\mathcal V_2$ belongs to a bucket $b \in \mathcal V_1$, it is also the first among the fewer points of $\mathcal V_1$, so $f_{\mathcal V_1}(i) = b$. In the preference order form, $\pi(i)$ lists the buckets by their first point clockwise from $i$. With 10 buckets of 100 points each and one bucket added (seed 5), 9.71% of 100000 keys moved, all of them to the new bucket, against the expected $1/11 = 9.09\%$. The closest point rule of Karger et al. on the unit interval is monotone by the same argument.

**Rendezvous hashing.** The item goes to the bucket with the highest score $w(i, b)$. Sorting the buckets by score gives the order $\pi(i)$, so the function is monotone. With independent uniform scores it is the function $\tilde f$ that Karger et al. call the most natural monotone consistent hash function.

**Jump consistent hash.** It accepts only the views $\{0, 1, \ldots, n-1\}$. On this chain of views it is monotone: when $n$ grows by one, a key either stays or moves to the new bucket $n$. A bucket in the middle cannot be removed, so the property for all views does not apply.

**Maglev hashing and bounded loads.** [Maglev hashing](/maglev-hashing/) fills a lookup table from per-server preference lists and keeps most keys on a change, but some keys move between old servers, so it is not exactly monotone. [Bounded-load consistent hashing](/bounded-load-consistent-hashing/) sends a key past a full bucket, so adding a bucket can let keys return to other old buckets; it bounds the expected number of moves instead.

**Monotone but useless.** The rule "every item goes to the first bucket of the view in one fixed order" is monotone, since it is the preference order form with the same order for every item, but it puts all items into one bucket. Monotonicity says nothing about [balance](/balance-property/).

**Not a ranged hash function at all.** Rules that look at the current loads, such as [least connections](/least-connections/) or [the power of two choices](/power-of-two-choices/), do not compute the bucket from the view and the item alone, so the property does not apply to them.

## Related definitions

- **[Balance](/balance-property/).** In one view, each bucket gets $O(1/|\mathcal V|)$ of the items. Monotone and balanced together give the minimum expected movement above.
- **[Spread and load](/spread-and-load/).** How many buckets an item is sent to across many views, and how many items a bucket gets across them. For a monotone function the spread of an item is the number of distinct first members of the views in its order $\pi(i)$.
- **Minimal disruption.** Thaler and Ravishankar used this term for the highest random weight mapping: when a server fails, only the items on that server are remapped. It is the removal reading of monotonicity. The Maglev paper uses "minimal disruption" for a looser goal, that few connections move when the backends change, without the guarantee for every item.
- **Universality.** Karger et al. call a ranged hash family universal if its restriction to each view is a universal hash family; together with monotonicity it gives the fraction $|\mathcal V_1 \cap \mathcal V_2|/|\mathcal V_1 \cup \mathcal V_2|$.
- **Rehashing.** A hash table that grows from $n$ to $n + 1$ slots with $h \bmod n$ moves $n/(n+1)$ of its keys, mostly between old slots. Doubling is a special case: $h \bmod 2n$ is either $h \bmod n$ or $h \bmod n + n$, so each key stays or moves to a new slot, and mod-n hashing is monotone on the chain of views $n, 2n, 4n, \ldots$ only. Inside one memory a move is cheap and full [rehashing](/rehashing/) is fine; across machines a move is a copy or a cache miss, which is why distributed systems want monotonicity for every change.

## References
