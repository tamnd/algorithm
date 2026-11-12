---
tag: 935TPJ
kind: data-structure
slug: learned-index
name: Learned index
aliases:
- learned index structures
- recursive model index
area: systems/database-algorithms
level: research
summary: "A model of the key distribution predicts where a key lies in a sorted array, with a stored error bound per model. A short search inside the bound finishes the lookup."
model: word-ram
complexity:
  vars: {n: the number of keys, m: the number of stage-2 models, e: the largest search window of a model}
  time: {worst: "O(log e)", best: "O(1)"}
  space: {extra: "Θ(m)"}
properties: {deterministic: true, static: true}
prereqs: [binary-search, ordinary-least-squares, b-plus-tree]
see_also: [learned-bloom-filter, interpolation-search, exponential-search, predecessor-problem, zone-map, fusion-tree, linear-regression, bulk-loading-b-tree]
sources:
  - paper: doi:10.1145/3183713.3196909
    title: "Tim Kraska, Alex Beutel, Ed H. Chi, Jeffrey Dean and Neoklis Polyzotis, The case for learned index structures, SIGMOD 2018"
    locator: pp. 489 to 504; the index as a model of the cumulative distribution, the recursive model index, the min and max error per last-stage model, and the search in that range
  - paper: doi:10.14778/3389133.3389135
    title: "Paolo Ferragina and Giorgio Vinciguerra, The PGM-index: a fully-dynamic compressed learned index with provable worst-case bounds, PVLDB 13(8) (2020)"
    locator: pp. 1162 to 1175; the optimal piecewise linear ε-approximation, the recursive construction, and the dynamic and compressed versions
---

A learned index replaces the search in a tree by a prediction. The keys are stored in a sorted array, so the position of a key $k$ is the number of keys below it, which is $n F(k)$ for the cumulative distribution $F$ of the keys. A small model, trained on the keys, predicts this position. Each model also stores the largest errors it makes on its own keys, so a lookup computes a prediction $p$ and searches only the window $[p + e_{lo}, p + e_{hi}]$. The recursive model index (RMI) of Kraska et al. (2018) uses a stage of models to choose one model of the next stage; the PGM-index of Ferragina and Vinciguerra (2020) uses an optimal piecewise linear model with a guaranteed error $\varepsilon$.

## In plain words

In a phone book, to find "Miller" you do not start at page one, and you do not open the middle page. You know that M is a bit after the middle of the alphabet, so you open the book there. Then you look a few pages forward or back.

A learned index does the same with numbers. It learns from the keys how far through the list each key should be. It writes down, once, how far its guesses were wrong at most. A lookup makes a guess and then searches only the few places that the stored error allows. If the keys follow a smooth pattern, the guess is very close and the search is very short.

## The abstract type

The structure answers lookups in a static set of $n$ distinct keys, stored in a sorted array $K[0..n-1]$:

- `lookup(k)`: the position $i$ with $K[i] = k$, or *absent*.

With extra care (see Pitfalls) it also gives `lower_bound(k)`, the first position with $K[i] \ge k$, which starts a range scan. It is an alternative to a [B+ tree](/b-plus-tree/) over the same sorted data, and to [binary search](/binary-search/) on it.

## Representation

A two-stage RMI with $m$ stage-2 models holds:

- the sorted array $K$;
- a stage-1 model $f_1$, here a line $a_1 k + b_1$;
- $m$ stage-2 models $f_1', \ldots, f_m'$, each a line, or *empty*;
- for each stage-2 model $j$, two integers $e_{lo}(j) \le e_{hi}(j)$.

The stage-1 model routes key $k$ to model $\rho(k) = \mathrm{clamp}(\lfloor m f_1(k) / n \rfloor, 0, m - 1)$. Let $D_j$ be the keys routed to model $j$.

**Invariant (error bounds).** For every key $K[i]$ in $D_j$, with $p = \lfloor f_j'(K[i]) \rfloor$: $e_{lo}(j) \le i - p \le e_{hi}(j)$.

The models here are fitted by least squares, as in the RMI paper for its simple models. Any other model works, since the invariant is measured after training, not assumed. The implementation computes the fit with exact fractions, so the bounds hold exactly; with floating point, the stored bounds must be computed with the same arithmetic as the lookup.

## Operations

```pseudo id=main
BUILD(K, m)                                  ▷ K sorted, distinct, n keys
L1  f_1 ← least squares line through the points (K[i], i)
L2  for each i do add i to D_ρ(K[i]),  where ρ(k) = clamp(⌊m · f_1(k) / n⌋, 0, m − 1)
L3  for each j with D_j not empty do f_j' ← least squares line through (K[i], i) for i in D_j
L4      e_lo(j) ← min, e_hi(j) ← max of i − ⌊f_j'(K[i])⌋ over i in D_j

LOOKUP(k)
L5  j ← ρ(k)
L6  if D_j is empty then return absent
L7  p ← ⌊f_j'(k)⌋
L8  lo ← max(0, p + e_lo(j)),  hi ← min(n − 1, p + e_hi(j))
L9  binary search K[lo..hi] for k
L10 return its position if found, else absent
```

A least squares line through $(x, y)$ points has slope $(n \sum xy - \sum x \sum y) / (n \sum x^2 - (\sum x)^2)$ and passes through the mean point; if all $x$ are equal, the slope is 0.

## Example

The 16 primes $2, 3, 5, \ldots, 53$ with $m = 4$. Line L1 fits $f_1(k) = \frac{6328}{22413} k + \frac{5804}{7471} \approx 0.2823 k + 0.7769$. Routing with $\lfloor 4 f_1(k) / 16 \rfloor$ splits the keys into four groups.

| model | keys | positions | line $f_j'$ | $[e_{lo}, e_{hi}]$ |
|---|---|---|---|---|
| 0 | 2 3 5 7 11 | 0 to 4 | $\frac{55}{128} k - \frac{13}{32}$ | [0, 1] |
| 1 | 13 17 19 23 | 5 to 8 | $\frac{4}{13} k + \frac{25}{26}$ | [0, 1] |
| 2 | 29 31 37 | 9 to 11 | $\frac{3}{13} k + \frac{33}{13}$ | [0, 1] |
| 3 | 41 43 47 53 | 12 to 15 | $\frac{5}{21} k + \frac{107}{42}$ | [0, 1] |

Lookup of 37: $f_1(37) \approx 11.22$ and $\lfloor 4 \cdot 11.22 / 16 \rfloor = 2$. Model 2 gives $\frac{3 \cdot 37 + 33}{13} = \frac{144}{13} \approx 11.08$, so $p = 11$ and the window is $[11, 12]$. The binary search finds 37 at position 11 after one comparison. Lookup of 30: model 2 gives $\frac{123}{13} \approx 9.46$, $p = 9$, window $[9, 10]$, which holds 29 and 31, so 30 is absent. Every lookup in this example searches at most 2 positions, against 4 or 5 probes for binary search over 16 keys.

**A larger case.** For 10,000 distinct keys drawn uniformly from $[0, 10^7)$ by `random.Random(4)`:

| stage-2 models $m$ | largest window | mean window over the keys |
|---|---|---|
| 1 | 105 | 104.6 |
| 10 | 50 | 38.6 |
| 100 | 23 | 11.6 |
| 1000 | 8 | 3.4 |

For 10,000 keys from a skewed distribution (rounded values of $e^{X}$ with $X$ normal, mean 10 and deviation 2), one line has a mean window of 5,897 positions, close to the whole array. With $m = 100$ the mean window is 34.8 and 33 models are empty; with $m = 1000$ it is 11.4. The second stage is what makes a simple model fit a skewed distribution.

## Correctness

For a key $K[i]$ that is present, LOOKUP computes the same route $\rho(K[i])$ as BUILD, so it reaches the model $j$ that was trained on $K[i]$ and whose bounds were measured on it. By the invariant, $i$ lies in $[p + e_{lo}(j), p + e_{hi}(j)]$, and also in $[0, n - 1]$. The binary search of line L9 runs on a sorted subarray that contains $k$, so it finds position $i$. For an absent key, line L10 returns a position only if $K[\text{pos}] = k$, which never holds, so the answer is *absent*. The full proof is below.

## Complexity

Let $e$ be the largest window $e_{hi}(j) - e_{lo}(j) + 1$ over all models.

- **Lookup.** Two model evaluations, $O(1)$, then a binary search over at most $e$ positions, $O(\log e)$ comparisons. When the models fit well, $e$ is a small constant and a lookup takes $O(1)$ time and touches one or two cache lines of $K$. There is no bound on $e$ in terms of $n$ for an RMI; it depends on how well the data fits. For a set where no line fits, $e$ can be close to $n$, and the lookup is a plain binary search.
- **Space.** $\Theta(m)$ numbers on top of the array, against $\Theta(n / B)$ nodes for a B+ tree with $B$ keys per node. For $m \ll n / B$ this is much smaller.
- **Build.** Line L1 is one pass, line L2 one pass, lines L3 and L4 one pass in total, so $O(n)$ arithmetic operations on top of the sort.

**The PGM bound.** The PGM-index fixes the error $\varepsilon$ instead of the number of models. It computes a piecewise linear function with the fewest segments such that every key's predicted position is within $\varepsilon$ of its true position, in $O(n)$ time, by a streaming algorithm for fitting lines between ranges of values (O'Rourke, 1981). The number of segments $s$ is at most $\lceil n / (2\varepsilon + 1) \rceil$ for integer $\varepsilon$: cut the array into runs of $2\varepsilon + 1$ consecutive keys and give each run a constant segment equal to the middle position; each key is then within $\varepsilon$ of its position. So an optimal segmentation has at most this many segments, and on real data it has far fewer. The PGM-index then indexes the first keys of the segments recursively in the same way, so a lookup takes $O(\log_c s)$ steps of $O(\log \varepsilon)$ each, for a fanout $c$ that depends on $\varepsilon$.

## Variants

- **Deeper RMI.** More stages, or neural networks in the top stage, as in the original paper. A model with a bad error can be replaced by a small B-tree, which gives a hybrid index with the worst case of a B-tree.
- **PGM-index.** Optimal piecewise linear models with a fixed $\varepsilon$, built recursively, with provable bounds; it supports inserts by the logarithmic method and can compress the segments.
- **Updatable learned indexes.** ALEX (Ding et al., 2020) keeps gaps in the arrays of the leaf models so that inserts shift few keys, and splits or retrains models as the data changes.
- **Other search in the window.** Exponential search from $p$ outward costs $O(\log |i - p|)$, which is better than binary search over the whole window when most errors are small. See [exponential search](/exponential-search/).
- **Learned structures for other tasks.** The same idea gives learned hash functions and the [learned Bloom filter](/learned-bloom-filter/), where a classifier filters most queries and a backup filter catches its false negatives.

## When to use it

Use a learned index for a large, read-mostly, sorted set of numeric keys whose distribution is smooth: time stamps, sequence numbers, sensor values, keys in a sorted run of an [LSM tree](/log-structured-merge-tree/). It saves space against a [B+ tree](/b-plus-tree/) and often saves time, because a lookup does one or two predictions instead of a root-to-leaf walk. Prefer a B+ tree when updates are frequent, when keys are long strings, or when a worst-case bound on the lookup is required and the data may be adversarial. [Interpolation search](/interpolation-search/) is close in spirit: it predicts with the line through the two ends of the current range and repeats, with no stored bound.

## Pitfalls

- **Bounds measured on other data.** The bounds are valid only for the keys used to measure them. After an insert, positions shift and the bounds of every model to the right may be wrong. Rebuild, or use an updatable variant.
- **Lower bound for an absent key.** The error bounds cover the positions of present keys only. For an absent key $k$, the true insertion point can lie outside the window, for example when $k$ falls between the last key of model $j$ and the first key of model $j + 1$ and is routed to model $j$. A range query must then check the edges of the window and extend the search with exponential search when the answer is at an edge.
- **Floating point.** A model evaluated with a different rounding at lookup time than at build time can give a position one off from the one the bounds were measured for. Measure the bounds with the same code that predicts, or widen them by one.
- **Empty models.** A stage-2 model may receive no keys. Its lookup must report *absent*, or fall back to a neighbour, never use an untrained line.
- **Adversarial or highly irregular data.** No small model fits a set with large jumps everywhere, and the windows become large. The worst case is a binary search over the window, not over the tree.

## Implementations

## History

Kraska, Beutel, Chi, Dean and Polyzotis proposed learned index structures at SIGMOD 2018. They argued that an index is a model of the cumulative distribution of the keys, introduced the recursive model index with min and max errors per model, and reported faster and smaller indexes than B-trees on several data sets. Ferragina and Vinciguerra gave the PGM-index in 2020, with optimal piecewise linear models and worst-case bounds. Updatable variants such as ALEX followed, as did learned versions of hash tables and Bloom filters.

## References
