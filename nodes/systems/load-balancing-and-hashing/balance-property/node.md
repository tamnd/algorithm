---
tag: 236SPG
kind: definition
slug: balance-property
name: Balance property
aliases:
- balanced ranged hash family
area: systems/load-balancing-and-hashing
level: core
summary: "A ranged hash family is balanced if, in each view, a random function from it gives each bucket at most a constant times its fair share 1/|V| of the items, with high probability."
prereqs: [consistent-hashing, hash-function]
see_also: [monotonicity-property, spread-and-load, consistent-hashing-max-load-bound, virtual-nodes, balls-into-bins-max-load, universal-hashing, rendezvous-hashing, load-skew]
sources:
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, distributed caching protocols for relieving hot spots on the World Wide Web, STOC 1997
    locator: pp. 654 to 663, Section 4.1 (views, ranged hash functions and families, the balance property), Theorem 4.1 part 2 (Pr[f_V(i) = b] <= O(1/|V|)) and Section 4.4 (universality)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 4, Section 4.2.1 (Theorem 4.4, the Chernoff bound) and Chapter 5, Sections 5.2 and 5.4 (the maximum load of n balls in n bins)
  - url: https://arxiv.org/abs/1406.2294
    title: John Lamping and Eric Veach, A fast, minimal memory, consistent hash algorithm, arXiv:1406.2294, 2014
    locator: the introduction (balance and monotonicity as the two requirements on a consistent hash function)
---

The balance property is the first of the four properties that Karger et al. asked of a [consistent hash function](/consistent-hashing/) in 1997. A family of hash functions is *balanced* if, for any one set of usable buckets (a *view*), a function drawn from the family sends to each bucket at most a constant times its fair share $1/|\mathcal V|$ of the items, with high probability. An ordinary [hash function](/hash-function/) onto a fixed set of buckets already has it. The difficulty is to keep it together with [monotonicity](/monotonicity-property/), and plain consistent hashing with one point per bucket does not: it needs [virtual nodes](/virtual-nodes/) to be balanced.

## Definition

**Setting (Karger et al., Section 4.1).** Let $\mathcal I$ be the set of items and $\mathcal B$ the set of buckets. A *view* is a nonempty set $\mathcal V \subseteq \mathcal B$, the buckets that one client knows. A *ranged hash function* is a function $f : 2^{\mathcal B} \times \mathcal I \to \mathcal B$, written $f_{\mathcal V}(i)$, with $f_{\mathcal V}(i) \in \mathcal V$ for every view $\mathcal V$ and item $i$. A *ranged hash family* $\mathcal F$ is a set of ranged hash functions with a probability distribution on it, and a *random ranged hash function* is drawn from that distribution.

**Balance.** A ranged hash family $\mathcal F$ is *balanced* if, given a view $\mathcal V$ and a set $J$ of items, a random $f \in \mathcal F$ satisfies, with high probability,

$$ \bigl|\{\, i \in J : f_{\mathcal V}(i) = b \,\}\bigr| \;\le\; \beta \cdot \frac{|J|}{|\mathcal V|} \qquad \text{for every bucket } b \in \mathcal V, $$

where $\beta$ is a constant that does not depend on $\mathcal V$ or $J$. Karger et al. write this as "the fraction of items mapped to each bucket is $O(1/|\mathcal V|)$". In their theorems "with high probability" means probability at least $1 - C^{-\Omega(1)}$, where $C$ bounds the number of buckets.

**The per-item form.** Theorem 4.1 of Karger et al. proves balance for their construction in the form

$$ \Pr_f\bigl[f_{\mathcal V}(i) = b\bigr] \;\le\; \frac{\beta}{|\mathcal V|} \qquad \text{for every view } \mathcal V,\ i \in \mathcal I,\ b \in \mathcal V, $$

together with the fact that, once the bucket points are fixed, the items are assigned $\log C$-wise independently. The per-item form alone is weaker, as the last example below shows.

**The definition needs many items.** If $|J| = |\mathcal V| = n$, even a truly random function puts $(1 + o(1))\ln n/\ln\ln n$ items into the fullest bucket with high probability ([balls into bins](/balls-into-bins-max-load/)), which is not $O(1)$ times the fair share 1. So the item form of balance is only possible for $|J| = \Omega(|\mathcal V|\log|\mathcal V|)$. For hashing onto a circle or an interval, the clean way to say it is through *shares*: the share of bucket $b$ is the measure of the item positions that go to $b$, and balance means that the largest share is at most $\beta/|\mathcal V|$ with high probability. With enough items, balanced shares give balanced counts by the [Chernoff bound](/chernoff-bound/).

## Examples and non-examples

**A fixed random hash onto the view.** Let each item go to a uniform bucket of $\mathcal V$, independently, for instance by $h(i) \bmod |\mathcal V|$ with an ideal $h$. With $n = |\mathcal V|$ and $m = |J| \ge 3(c+1)n\ln n$ items, each bucket has mean $m/n$, and the Chernoff bound with $\delta = 1$ gives $\Pr[\text{some bucket has} \ge 2m/n] \le n\,e^{-m/(3n)} \le n^{-c}$. So the family is balanced with $\beta = 2$. It is not [monotone](/monotonicity-property/): a change of $|\mathcal V|$ moves almost every item.

**Consistent hashing with one point per bucket: a non-example.** Each bucket has one random point on the circle, and an item goes to the next point clockwise. The per-item form holds with equality: by symmetry every bucket has expected share $1/n$, so $\Pr[f_{\mathcal V}(i) = b] = 1/n$. But the largest share is between $(1-\epsilon)\ln n/n$ and $(1+c)\ln n/(n-1)$ with high probability, and its mean is $H_n/n$ ([consistent hashing load bound](/consistent-hashing-max-load-bound/)). For $n = 1000$ that mean is $7.485/n$, and for $n = 10^6$ it is $14.39/n$. No constant $\beta$ works for all $n$. A small case: four buckets at the points 0.10, 0.35, 0.40 and 0.90 own the arcs 0.20, 0.25, 0.05 and 0.50, so one bucket has twice its fair share and another a fifth of it.

**Consistent hashing with virtual nodes.** Give each bucket $v$ random points. If $v \ge 16\ln(2n^{c+1})$, every share lies in $[\frac{1}{3n}, \frac{3}{n}]$ with probability at least $1 - n^{-c}$ ([consistent hashing load bound](/consistent-hashing-max-load-bound/), with $\delta = 1/2$). For $c = 1$ that is $v = 159$ points for $n = 100$ buckets and $v = 233$ for $n = 1000$. So the family is balanced with $\beta = 3$ for the shares; this is the reason for the $\kappa\log C$ points per bucket in the construction of Karger et al.

**Rendezvous hashing.** Give each item an independent uniform random order of all buckets, and send it to the first bucket of the order that is in the view. This is the function $\tilde f$ of Karger et al., and [rendezvous hashing](/rendezvous-hashing/) computes it with a hash score per pair. In each view, an item goes to a uniform bucket of $\mathcal V$, independently of the other items, so the family is balanced exactly as the random hash above, and it is also monotone.

**The smallest bucket: a non-example.** Fix an order of $\mathcal B$ and let $f_{\mathcal V}(i)$ be the first bucket of $\mathcal V$ in this order, for every item. This function is monotone and every client with the same view agrees, but one bucket gets all the items, so it is not balanced.

**One random order for all items: the per-item form is not enough.** Draw one uniform random order of $\mathcal B$ and send every item to the first bucket of the order that is in $\mathcal V$. For each item and bucket, $\Pr[f_{\mathcal V}(i) = b] = 1/|\mathcal V|$, so the per-item form holds with $\beta = 1$. Yet in every outcome all the items go to the same bucket. The per-item form needs independence between items to give the item form.

## Related definitions

- **[Monotonicity](/monotonicity-property/).** When buckets are added to a view, items move only to the new buckets. Balance and monotonicity are independent: the random hash above is balanced and not monotone, and the smallest-bucket rule is monotone and not balanced.
- **[Spread and load](/spread-and-load/).** Balance looks at one view. Spread and load look at many views at once: how many different buckets one item is sent to, and how many different items one bucket receives.
- **Universality.** Karger et al. call a ranged hash family *universal* if its restriction to each view is a universal hash family (Section 4.4). They use it in the sense that in each view the expected fraction of items assigned to any $j$ buckets is $j/|\mathcal V|$, which is the per-item form of balance with $\beta = 1$. See [universal hashing](/universal-hashing/) for the usual definition by collision probabilities.
- **Maximum load.** In [load balancing](/load-balancing-problem/) and [balls into bins](/balls-into-bins-max-load/), the quality of an assignment is the largest count divided by the average. Balance asks that this ratio be $O(1)$ with high probability. [Bounded-load consistent hashing](/bounded-load-consistent-hashing/) makes it at most $1 + \epsilon$ in every outcome by a hard cap per bucket, at the cost of exact monotonicity.
- **Weighted balance.** When buckets have capacities $w_b$, the fair share of $b$ is $w_b/\sum_{b' \in \mathcal V} w_{b'}$, and virtual nodes in proportion to $w_b$ give it.
- **Balance of items, not of requests.** The property counts items. If a few items get most of the requests ([load skew](/load-skew/)), the buckets that hold them are hot even when the items are balanced. Karger et al. used random trees of caches, not balance, for such hot spots.

## References
