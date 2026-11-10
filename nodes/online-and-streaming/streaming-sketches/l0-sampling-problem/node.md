---
tag: JGTKTE
kind: problem
slug: l0-sampling-problem
name: L0 sampling problem
aliases:
- uniform sampling of the support
- support sampling
area: online-and-streaming/streaming-sketches
level: advanced
summary: Under insertions and deletions, keep a small sketch that returns a nonzero coordinate of the vector, close to uniform over the support. The space is Θ(log² n) bits for constant δ.
prereqs: [turnstile-model, linear-sketch, streaming-model, epsilon-delta-guarantee]
see_also: [l0-sampler, agm-graph-sketch, distinct-elements-problem, reservoir-sampling, minhash, count-sketch, stream-connectivity-problem, frequency-moment-problem]
sources:
  - url: https://arxiv.org/abs/1012.4889
    title: Hossein Jowhari, Mert Sağlam and Gábor Tardos, Tight bounds for Lp samplers, finding duplicates in streams, and related problems, PODS 2011
    locator: the definition of Lp samplers with relative error and failure probability, the O(log² n) bit L0 sampler, the Ω(log² n) lower bound, and the reduction for finding duplicates
  - url: https://arxiv.org/abs/1704.00633
    title: Michael Kapralov, Jelani Nelson, Jakub Pachocki, Zhengyu Wang, David P. Woodruff and Mobin Yahyazadeh, Optimal lower bounds for universal relation, and for samplers and finding duplicates in streams, FOCS 2017
    locator: the main theorem on the universal relation and the corollaries for L0 samplers
  - paper: doi:10.1007/s10619-013-7131-9
    title: Graham Cormode and Donatella Firmani, A unifying framework for ℓ0-sampling algorithms, Distributed and Parallel Databases 32(3), 2014
    locator: pp. 315 to 335 (the sampling, recovery and selection steps, and the experimental comparison)
  - paper: doi:10.1145/3297715
    title: Graham Cormode and Hossein Jowhari, Lp samplers and their applications, a survey, ACM Computing Surveys 52(1), 2019
    locator: the sections on L0 sampling and on applications to graphs and duplicates
---

The L0 sampling problem asks for a small summary of a vector $x \in \mathbb{Z}^n$ that changes by insertions and deletions, $x_i \leftarrow x_i + d$, and that can at any time return a coordinate $i$ with $x_i \ne 0$, chosen nearly uniformly from the support. The name comes from the L0 "norm" $\|x\|_0 = |\{i : x_i \ne 0\}|$: the sample is drawn with weight $|x_i|^0$, which is 1 on the support and 0 off it. Deletions make the problem hard, since an item that was sampled can be deleted later, and the answer must be correct for the final vector. The space needed is $\Theta(\log^2 n)$ bits for a constant failure probability.

## In plain words

A shop keeps a list of customers who have at least one open order. Orders are placed and cancelled all day, and at the end you want one random customer from the list, each with the same chance. A customer with ten orders must not be more likely than a customer with one, and a customer whose orders were all cancelled must never be picked. If orders were never cancelled, you could pick a random new customer as they arrive and keep only that one. Cancellations break this: your pick may disappear. The problem is to do the job with memory that is tiny compared to the number of customers.

## Definition

**Stream.** The vector starts at $x = 0 \in \mathbb{Z}^n$. The stream is a sequence of updates $(i, d)$ with $i \in [n]$ and $d \in \mathbb{Z}$, each meaning $x_i \leftarrow x_i + d$. This is the [turnstile model](/turnstile-model/). We assume $|x_i| \le M$ at all times with $M \le \mathrm{poly}(n)$. The *strict* turnstile model also promises $x_i \ge 0$ at the end.

**The output.** Let $U = \mathrm{supp}(x) = \{i : x_i \ne 0\}$ for the final vector. An L0 sampler with relative error $\varepsilon$, failure probability $\delta$ and additive error $\eta$ returns FAIL with probability at most $\delta$, returns EMPTY if $x = 0$, and otherwise returns $(i, x_i)$ such that, for every $i \in U$,
$$\Pr[\text{output } i \mid \text{not FAIL}] = \frac{1 \pm \varepsilon}{|U|} \pm \eta.$$
Usually $\eta = n^{-c}$ for a constant $c$. If $\varepsilon = 0$, the sampler has *zero relative error*. Some definitions return only $i$; returning $x_i$ too costs nothing in the known constructions.

**The randomness.** The probability is over the random choices of the algorithm. The stream is fixed in advance and may be chosen by an adversary who does not see the random bits.

**Space.** Space is counted in bits, because the bounds are polylogarithmic and the factors of $\log n$ matter.

## Variants

- **Insertion only.** With no deletions, a sample of the distinct items is easy: keep the item with the smallest hash value, a [min-hash](/minhash/), in $O(\log n)$ bits.
- **Lp sampling.** Return $i$ with probability close to $|x_i|^p/\|x\|_p^p$. For $p = 0$ this is L0 sampling, and for $0 < p < 2$ it is solved with scaled [Count-Sketch](/count-sketch/) structures.
- **Many samples.** Return $s$ distinct elements of the support, uniformly at random. The structures recover all of a level that holds at most $s$ coordinates, which costs a factor $s$ in space.
- **Perfect sampling.** Ask for $\varepsilon = 0$ and $\eta = 1/\mathrm{poly}(n)$. For L0 this is reached by the standard constructions; for $p > 0$ it needs further work.
- **Sketch arithmetic.** Ask for a linear sketch, so that the sketch of $x - y$ is computed from the sketches of $x$ and $y$. All known L0 samplers are linear, and graph applications need this.

## Examples

**Why counting updates is wrong.** Take $n = 5$ and the updates $(1, +1)$, $(1, +1)$, $(1, +1)$, $(2, +1)$, $(3, +1)$, $(3, -1)$, $(4, +2)$. The final vector is $x = (3, 1, 0, 2, 0)$ and $U = \{1, 2, 4\}$. An L0 sampler returns 1, 2 and 4 with probability $1/3$ each. Picking a random update and its coordinate would return 1 with probability $3/7$ and could return 3, which is not in the support.

**Cancelled pairs.** Take $x = e_7 - e_7 + e_9$, that is $(7, +1)$, $(7, -1)$, $(9, +1)$. The only correct answer is $(9, 1)$. A sampler that keeps the first coordinate it sees would keep 7 and fail.

**A graph.** In the [AGM graph sketch](/agm-graph-sketch/), coordinate $(u, v)$ with $u < v$ of the vector $a_w$ is $+1$ if $w = u$ and $(u, v)$ is an edge, $-1$ if $w = v$ and $(u, v)$ is an edge, and 0 otherwise. For a set $S$ of vertices, $\sum_{w \in S} a_w$ is nonzero exactly on the edges that leave $S$. An L0 sample of this sum is an edge that leaves $S$.

## Known algorithms

| method | stream model | guarantee | space in bits |
|---|---|---|---|
| store $x$ | any | exact, deterministic | $O(n \log M)$ |
| [min-hash](/minhash/) | insertion only | near uniform | $O(\log n)$ |
| Frahling, Indyk and Sohler 2005 | turnstile | near uniform | $O(\log^3 n)$ for constant $\delta$ |
| Cormode, Muthukrishnan and Rozenbaum 2005 | turnstile | near uniform | polylogarithmic |
| [L0 sampler](/l0-sampler/), nested levels with 1-sparse recovery | turnstile | near uniform | $O(\log^2 n \log(1/\delta))$ |
| Jowhari, Sağlam and Tardos 2011, $s$-sparse recovery | turnstile | zero relative error | $O(\log^2 n \log(1/\delta))$ |

The common pattern, described by Cormode and Firmani as sampling, recovery and selection, is this: subsample the coordinates at rates $1, 1/2, 1/4, \ldots$ with a hash function, keep a sparse recovery structure for each rate, and at query time pick a rate at which the surviving part of the support is small and nonzero, recover it, and select one element.

## Bounds

**Upper bound.** $O(\log^2 n \log(1/\delta))$ bits, from the [L0 sampler](/l0-sampler/) page or from Jowhari, Sağlam and Tardos. One factor $\log n$ is the number of rates, and the other is the size of a counter.

**Lower bound for constant δ.** Jowhari, Sağlam and Tardos proved that $\Omega(\log^2 n)$ bits are needed, even for vectors with entries in $\{0, 1, -1\}$, which matches the upper bound for constant $\delta$.

**Tight bound in δ.** Kapralov, Nelson, Pachocki, Wang, Woodruff and Yahyazadeh (2017) proved that the randomized one-way communication complexity of the universal relation (below) is $\Theta(\min\{n, \log(1/\delta)\log^2(n/\log(1/\delta))\})$, and derived a matching lower bound for L0 samplers. So the $\log(1/\delta)$ factor of the upper bound is needed when $\delta$ is not too small.

**Insertion only.** Without deletions, $O(\log n)$ bits suffice, so the extra factor $\log n$ is the price of deletions.

## Reductions

- **From the universal relation.** In the universal relation, Alice holds $a \in \{0, 1\}^n$ and Bob holds $b \in \{0, 1\}^n$ with $a \ne b$, and Bob must output an index $i$ with $a_i \ne b_i$, after one message from Alice. Alice runs an L0 sampler on the updates $(i, a_i)$ and sends its memory. Bob continues the same sampler with the updates $(i, -b_i)$, so it now holds a sketch of $a - b$, whose support is exactly the set of differing indices, and he queries it. So the space of an L0 sampler is at least the one-way communication of the universal relation, which gives the lower bounds above. Since $a - b \in \{0, \pm 1\}^n$, the bounds hold for such vectors.
- **To spanning forests.** L0 samples of sums of signed incidence vectors give edges that leave a set of vertices. Running [Borůvka](/boruvka/) on these samples gives a spanning forest of a graph under edge deletions; see [connectivity in streams](/stream-connectivity-problem/).
- **To finding duplicates.** Jowhari, Sağlam and Tardos find an item that repeats in a stream of $n + 1$ items from $[n]$. Let $x_i$ be the frequency of $i$ minus 1. Then $\sum_i x_i = 1$, the positive coordinates are the duplicates, and an $\ell_1$ sampler, a close relative of L0 samplers, returns a positive coordinate with probability more than 1/2. The space is $O(\log^2 n)$ bits for constant $\delta$, and the same lower bound applies.
- **To distinct elements of a subset.** Several independent L0 samples estimate which fraction of the support has a property, which with an estimate of $\|x\|_0$ from the [distinct elements problem](/distinct-elements-problem/) estimates the size of a subset of the support.

## Applications

- Graph sketching: connectivity, bipartiteness, minimum spanning tree weight and cut sparsifiers in dynamic graph streams, all through the [AGM graph sketch](/agm-graph-sketch/).
- Network monitoring: sampling the distinct flows or addresses that are active after starts and ends of connections, which Cormode, Muthukrishnan and Rozenbaum called inverse distribution sampling.
- Dynamic geometric streams: Frahling, Indyk and Sohler used L0 samples of point sets under insertions and deletions for estimates such as the weight of a minimum spanning tree.
- Distributed data: because the sketches are linear, each machine sketches its part, and the sum of the sketches is a sketch of the whole.

## References
