---
tag: BEP2MK
kind: theorem
slug: conductance-rumor-spreading-bound
name: Conductance bound on rumor spreading
aliases:
- Giakkoupis rumor spreading bound
area: distributed/gossip
level: research
summary: On every connected n-node graph of conductance Φ, push-pull informs all nodes in O(log n / Φ) rounds w.h.p. (Giakkoupis 2011). The bound is tight, and push or pull alone can be slow.
prereqs: [graph-conductance, push-pull-gossip, random-phone-call-model, union-bound]
see_also: [graph-conductance, push-pull-gossip, push-gossip, pull-gossip, push-rumor-spreading-time, conductance, cheeger-inequality, rumor-spreading-problem]
sources:
  - paper: doi:10.4230/LIPIcs.STACS.2011.57
    title: George Giakkoupis, Tight bounds for rumor spreading in graphs of a given conductance, Proceedings of the 28th Symposium on Theoretical Aspects of Computer Science (STACS), LIPIcs 9, 57-68, 2011
    locator: Theorem 1 (O(φ^-1 log n) for push-pull), Theorem 2 (conditions for pull), Lemma 4 and Lemma 5 (the three phases of pull), Corollary 7, Lemma 13 (push and pull symmetry), Lemma 15 (two stars, the lower bound)
  - paper: doi:10.1145/1806689.1806745
    title: Flavio Chierichetti, Silvio Lattanzi and Alessandro Panconesi, Almost tight bounds for rumour spreading with conductance, Proceedings of the 42nd ACM Symposium on Theory of Computing (STOC), 399-408, 2010
    locator: the bound O(log^2(1/φ) φ^-1 log n) for push-pull, graphs of conductance φ and diameter Ω(φ^-1 log n), the star example
  - paper: doi:10.1145/3173043
    title: Flavio Chierichetti, George Giakkoupis, Silvio Lattanzi and Alessandro Panconesi, Rumor spreading and conductance, Journal of the ACM 65, 2018
    locator: the journal version that combines the conductance results of the authors
  - paper: doi:10.1137/1.9781611973402.59
    title: George Giakkoupis, Tight bounds for rumor spreading with vertex expansion, Proceedings of the 25th ACM-SIAM Symposium on Discrete Algorithms (SODA), 801-815, 2014
    locator: Theorem 1 (O(log n log Δ / α) rounds for push-pull), Section 1 (the earlier bounds and the lower bound Ω(log n log Δ / α)), Section 2 (the definition of α)
---

The conductance bound on rumor spreading says that on every connected graph with $n$ nodes and [conductance](/graph-conductance/) $\Phi$, [push-pull gossip](/push-pull-gossip/) informs all nodes in $O(\log n / \Phi)$ rounds with high probability, from any start node. Giakkoupis (2011) proved it, after Chierichetti, Lattanzi and Panconesi (2010) had proved it up to a factor polynomial in $\log(1/\Phi)$. The bound is tight: two stars joined at their centers need $\Omega(\log n / \Phi)$ rounds. Push alone or pull alone does not satisfy it: on a star, whose conductance is 1, each of them needs a number of rounds linear in $n$ from some start nodes.

## Statement

**Model.** The [random phone call model](/random-phone-call-model/) on a connected undirected graph $G = (V, E)$: synchronous rounds, no failures, and in each round every node calls one neighbor chosen uniformly at random, independently. In *push*, an informed caller sends the rumor to the called node; in *pull*, an informed called node sends it to the caller; *push-pull* does both. A node informed in round $t$ acts as informed from round $t + 1$. The *broadcast time* is the number of rounds until all nodes are informed. "With high probability" (w.h.p.) means with probability $1 - O(n^{-c})$ for any fixed constant $c > 0$.

| Symbol | Meaning |
|---|---|
| $n$, $m$ | the numbers of nodes and edges |
| $d(v)$, $\Delta$, $\delta$ | the degree of $v$, the maximum and the minimum degree |
| $D$ | the diameter |
| $\Phi$ | the conductance, $\min_{0 < \mathrm{vol}(S) \le m} \lvert E(S, V \setminus S) \rvert / \mathrm{vol}(S)$ |
| $\alpha$ | the vertex expansion, $\min_{0 < \lvert S \rvert \le n/2} \lvert \partial S \rvert / \lvert S \rvert$ |
| $f$ | not used here (the number of crashed nodes on other pages) |

**Theorem 1 (Giakkoupis 2011, Theorem 1).** For any graph on $n$ vertices and any start vertex, the broadcast time of push-pull is $O(\Phi^{-1} \log n)$ rounds w.h.p.

**Theorem 2 (tightness, Giakkoupis 2011, Lemma 15).** For every $\phi$ with $2/(n + 2) \le \phi \le 1/2$ there are $n$-vertex graphs of conductance $\Theta(\phi)$ on which, for every start vertex and every constant $c > 0$, push-pull needs at least $c \ln n / (3\phi)$ rounds to inform all vertices with probability $1 - n^{-c}$.

**Theorem 3 (push and pull alone).** On the star with center $z$ and $n - 1 \ge 2$ leaves, $\Phi = 1$, and

1. push needs at least $n - 2$ rounds from every start vertex, and $(n - 1)H_{n-1}$ rounds in expectation from the center;
2. pull from a leaf needs $n$ rounds in expectation, and more than $(n - 1)/2$ rounds with probability at least $1/2$;
3. push-pull needs at most 2 rounds from every start vertex.

**Theorem 4 (vertex expansion, Giakkoupis 2014, Theorem 1).** For a graph with $n$ vertices, maximum degree at most $\Delta$ and vertex expansion at least $\alpha$, push-pull informs all vertices in $O(\log n \cdot \log \Delta / \alpha)$ rounds with probability $1 - O(n^{-\beta})$, for any constant $\beta > 0$. Since $\Delta < n$, this is $O(\log^2 n / \alpha)$.

## In plain words

In each round, every node phones a random neighbor, and the news goes along the call in whichever direction it can. If the network has no bottleneck, many links always join people who know to people who do not, so the group that knows keeps growing fast. A single link between two halves is a bottleneck: the news waits until somebody happens to use that link. A star shows why both directions are needed: the center talks to only one leaf per round, so pushing from the center is slow, and a leaf that knows the news waits a long time before the center calls it, so pulling is slow too. With both, the leaf tells the center and all the leaves ask the center in the next round.

## Proof

**Theorem 3 (complete).** Every set of leaves has as many cut edges as volume, and so does the center alone, which has volume $n - 1 \le m$; these are all the sets with volume at most $m = n - 1$, so $\Phi = 1$.

1. *Push.* A leaf has only the center as neighbor, so only the center can push to a leaf, and it pushes to one leaf per round. So at most one leaf is informed per round, and at least $n - 2$ rounds are needed to inform the $n - 1$ leaves, or $n - 2$ of them if the start is a leaf. From the center, each round informs a uniformly random leaf, so the time is that of the [coupon collector problem](/coupon-collector-problem/) with $n - 1$ coupons, $(n - 1)H_{n-1}$ in expectation.
2. *Pull from a leaf $\ell$.* An uninformed leaf calls the center, which is uninformed, so it learns nothing. The center learns the rumor only in a round in which its call goes to $\ell$, which happens with probability $1/(n - 1)$ in each round, independently. So the center is informed after a geometric number of rounds with mean $n - 1$, and every other leaf pulls from it in the next round: $n$ rounds in expectation. The center is still uninformed after $k = \lfloor (n - 1)/2 \rfloor$ rounds with probability $(1 - \frac{1}{n-1})^{k} \ge 1 - \frac{k}{n-1} \ge \frac{1}{2}$, and then at least $k + 2 > (n - 1)/2$ rounds are needed.
3. *Push-pull.* If the start is the center, every leaf calls it in round 1 and pulls the rumor. If the start is a leaf, it calls the center in round 1 and pushes the rumor, and in round 2 every leaf pulls it. $\blacksquare$

**Theorem 2 (complete, following Giakkoupis).** Take a star with $a = \lceil 1/\phi \rceil$ vertices and a star with $n - a$ vertices, and join the centers $v$ and $v'$ by an edge. Giakkoupis notes that the conductance is $\Theta(\phi)$; the small star alone has volume $2a - 1$ and one cut edge. The condition $\phi \ge 2/(n + 2)$ gives $n - a \ge a$. Let $v$ be the center on the side of the start vertex, informed in round $j$. All paths to the other side use the edge $\{v, v'\}$, and in one round the rumor crosses it only if $v$ calls $v'$ or $v'$ calls $v$, with probabilities $1/d(v)$ and $1/d(v')$, and the degrees of the centers are $a$ and $n - a$. So the rumor has not crossed by round $j + i$ with probability
$$\left(1 - \frac{1}{a}\right)^{i}\left(1 - \frac{1}{n - a}\right)^{i} \ge \left(1 - \frac{1}{a}\right)^{2i} \ge (1 - \phi)^{2i} \ge e^{-3i\phi},$$
using $1/a \le \phi \le 1/2$ and $1 - x \ge e^{-3x/2}$ for $0 \le x \le 1/2$. For $i < c \ln n / (3\phi)$ this is more than $n^{-c}$. $\blacksquare$

**A symmetry between push and pull (complete).** Giakkoupis (2011, Lemma 13) states that the probability that push carries a rumor from $v$ to $u$ within $t$ rounds equals the probability that pull carries a rumor from $u$ to $v$ within $t$ rounds. The proof is a time reversal. Let $c_r(w)$ be the neighbor that $w$ calls in round $r$. Push informs $u$ by round $t$ exactly when there are nodes $v = w_0, w_1, \ldots, w_k = u$ and rounds $r_1 < \cdots < r_k \le t$ with $c_{r_i}(w_{i-1}) = w_i$. Pull informs $v$ from $u$ exactly when there are rounds $s_1 < \cdots < s_k \le t$ along the reversed path with $w_{i-1}$ calling $w_i$ in the round $s_{k+1-i}$. Setting $c'_r = c_{t+1-r}$ turns one condition into the other, and $(c'_1, \ldots, c'_t)$ has the same distribution as $(c_1, \ldots, c_t)$, because the rounds are independent and identically distributed. $\blacksquare$

**Theorem 1 (sketch; the full proof is in Giakkoupis 2011, Sections 3 to 5).**

1. *Pull from a set.* For any informed set $S_0$, pull informs all vertices in $50(\beta + 2)\log n \,/\, \Phi + \Delta / \lceil \Phi\, \mathrm{vol}(S_0) \rceil$ rounds with probability $1 - O(n^{-\beta})$ (Lemma 4). The run has three phases: until the informed volume reaches $\Delta$, until it exceeds $m$, and until the uninformed volume is 0. In each, after $O(1/\Phi)$ rounds (or $O(\Delta / \lceil \Phi\, \mathrm{vol}(S_0) \rceil)$ in the first), the informed volume doubles, or the uninformed volume halves, with probability at least $1/2$ (Lemma 5). The reason is that at least $\Phi \min\{\mathrm{vol}(S), \mathrm{vol}(V \setminus S)\}$ edges cross the cut, and an uninformed endpoint $w$ of such an edge pulls along it with probability $1/d(w)$, which gains $d(w)$ volume with probability $1/d(w)$.
2. *Pull from a vertex of maximum degree.* If $d(s) = \Delta$, the second term is $O(1/\Phi)$, so pull from $s$ informs all vertices in $O(\log n / \Phi)$ rounds w.h.p. (Corollary 7).
3. *Push to a vertex of maximum degree.* By the symmetry above, push from any $v$ reaches $s$ within the same number of rounds w.h.p.
4. *Push-pull.* Push-pull does at least what push does, so it informs $s$ in $O(\log n / \Phi)$ rounds, and then it does at least what pull does from $s$, so it informs all vertices in $O(\log n / \Phi)$ more rounds.

**Theorem 4 (cited, not proved here).** The proof of Giakkoupis (2014) follows how the informed set grows in terms of its boundary and the degrees of the boundary vertices; it is long and is not reproduced.

## Consequences

- **Graphs with no bottleneck.** On expanders, where $\Phi$ is bounded below by a constant, push-pull takes $O(\log n)$ rounds from every start, which matches the $\log_3 n + O(\log \log n)$ rounds on the complete graph up to the constant.
- **A link to random walks.** By [Cheeger's inequality](/cheeger-inequality/), $\Phi \ge \lambda_2/2$, so push-pull also takes $O(\log n / \lambda_2)$ rounds, where $\lambda_2$ is the spectral gap of the normalized Laplacian.
- **Push and pull under degree conditions.** Push alone and pull alone also take $O(\log n / \Phi)$ rounds w.h.p. from any start vertex if $\Delta = O(1/\Phi)$, or if the degrees at the two ends of each edge are within a constant factor of each other (Giakkoupis 2011, Theorem 2, Theorem 12 and Section 4). The star breaks both conditions.
- **Social networks.** Chierichetti, Lattanzi and Panconesi noted that the bound suggests why rumors spread fast among people, since experimental studies find high conductance in social networks (as reported by Giakkoupis 2011, Section 1).

## Tightness

- **Two stars.** By Theorem 2, the $\log n / \Phi$ bound cannot be improved for any $\Phi \ge 2/(n + 2)$. The implementation of push-pull runs this graph with $n = 400$ and a small star of $a$ vertices, so $\Phi = 1/(2a - 1)$, from a leaf of the small star, over 200 seeds:

| $a$ | $\Phi$ | mean rounds | most rounds |
|---|---|---|---|
| 5 | 1/9 | 7.4 | 25 |
| 10 | 1/19 | 11.7 | 63 |
| 20 | 1/39 | 19.0 | 89 |
| 40 | 1/79 | 37.2 | 199 |

The mean grows linearly in $1/\Phi$, because the rumor waits about $1/(1/a + 1/(n - a))$ rounds for the edge between the centers. The tail, which is what a w.h.p. bound measures, is longer: the slowest of the 200 runs takes several times the mean.
- **Diameter.** Chierichetti, Lattanzi and Panconesi (2010) gave graphs of conductance $\Phi \ge 1/n^{1-\varepsilon}$ and diameter $\Omega(\log n / \Phi)$, which also forces $\Omega(\log n / \Phi)$ rounds.
- **Very small conductance.** For $\Phi = o(1/n)$ the bound is not tight, since push informs every connected graph in $O(n \log n)$ rounds w.h.p. (Feige et al. 1990).
- **The star.** With $n = 200$ and 100 seeds, the implementation gives a mean of 1166 rounds for push from the center, against $(n - 1)H_{n-1} \approx 1168$; 181 rounds for pull from a leaf, against an expectation of 200; and exactly 2 rounds for push-pull from a leaf.
- **Vertex expansion.** The bound of Theorem 4 matches the lower bound $\Omega(\log n \cdot \log \Delta / \alpha)$ known for some graphs with $\Delta / \alpha \le n^{1 - \varepsilon}$, as Giakkoupis (2014) states. Conductance and vertex expansion are incomparable, so neither theorem implies the other.

## History

Chierichetti, Lattanzi and Panconesi asked whether rumor spreading is fast in every graph of high conductance, and noted that the star rules this out for push and pull alone. They proved a first bound for push-pull, polynomial in $\log n$ and $1/\Phi$, at SODA 2010, and then $O(\log^2(1/\Phi)\, \Phi^{-1} \log n)$ at STOC 2010. Giakkoupis (2011) removed the $\log^2(1/\Phi)$ factor with a new analysis through pull from a vertex of maximum degree and the push and pull symmetry, and showed tightness for all $\Phi = \Omega(1/n)$. The four authors later published the combined results in the Journal of the ACM. For vertex expansion, earlier work, including Giakkoupis and Sauerwald (SODA 2012), gave larger polylogarithmic upper bounds and the lower bound $\Omega(\log n \log \Delta / \alpha)$, and Giakkoupis (2014) closed the gap with $O(\log n \log \Delta / \alpha)$.

## References
