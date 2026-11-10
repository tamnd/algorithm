---
tag: QSH7SV
kind: data-structure
slug: l0-sampler
name: L0 sampler
aliases:
- l0 sketch
- support sampler
area: online-and-streaming/streaming-sketches
level: advanced
summary: Linear sketch of a vector under insertions and deletions that returns a nonzero coordinate, nearly uniform over the support, in O(log² n log(1/δ)) bits.
model: word-ram
complexity:
  vars: {n: the dimension of the vector, δ: the failure probability}
  time: {update: O(log n log(1/δ)), query: O(log n log(1/δ))}
  space: {extra: O(log n log(1/δ))}
properties: {online: true, deterministic: false, mergeable: true, linear: true}
history:
  year: 2011
  people: [Hossein Jowhari, Mert Sağlam, Gábor Tardos]
  note: Frahling, Indyk and Sohler (2005) and Cormode, Muthukrishnan and Rozenbaum (2005) gave the first samplers from dynamic streams. Jowhari, Sağlam and Tardos (PODS 2011) reached O(log² n) bits for constant δ, with zero relative error, and proved a matching lower bound.
prereqs: [l0-sampling-problem, linear-sketch, turnstile-model, k-wise-independent-hashing, schwartz-zippel-lemma]
see_also: [agm-graph-sketch, count-sketch, min-wise-independent-hashing, minhash, fingerprinting, distinct-elements-problem, reservoir-sampling, polynomial-identity-testing]
sources:
  - url: https://arxiv.org/abs/1012.4889
    title: Hossein Jowhari, Mert Sağlam and Gábor Tardos, Tight bounds for Lp samplers, finding duplicates in streams, and related problems, PODS 2011
    locator: the section on L0 samplers (s-sparse recovery and the O(log² n) bit sampler) and the lower bound section (Ω(log² n) for 0, ±1 vectors)
  - url: https://arxiv.org/abs/1704.00633
    title: Michael Kapralov, Jelani Nelson, Jakub Pachocki, Zhengyu Wang, David P. Woodruff and Mobin Yahyazadeh, Optimal lower bounds for universal relation, and for samplers and finding duplicates in streams, FOCS 2017
    locator: the main theorem (universal relation, Θ(min{n, log(1/δ) log²(n/log(1/δ))})) and its corollary for samplers
---

An L0 sampler is a small random [linear sketch](/linear-sketch/) of a vector $x \in \mathbb{Z}^n$ that changes under [turnstile](/turnstile-model/) updates $x_i \leftarrow x_i + d$, with $d$ positive or negative. At any time it returns a coordinate $i$ with $x_i \ne 0$, together with the value $x_i$, and the coordinate is close to uniform over the support. The sketch uses $O(\log n \log(1/\delta))$ counters of $O(\log n)$ bits, so $O(\log^2 n \log(1/\delta))$ bits, and it fails with probability at most $\delta$. It solves the [L0 sampling problem](/l0-sampling-problem/), and it is the building block of the [AGM graph sketch](/agm-graph-sketch/).

## In plain words

Think of a large set of numbered boxes. People put tokens into boxes and take them out again, and at the end you want the number of one box that is not empty. You cannot remember every box. So you make a few small notebooks. Notebook 0 watches all boxes, notebook 1 watches a random half of them, notebook 2 a random quarter, and so on. Each notebook keeps only three running totals. If exactly one watched box is not empty, the three totals tell you which box it is and how many tokens it has. If more than one is not empty, a check tells you so, with almost no chance of a mistake. Some notebook in the chain is likely to see exactly one box.

## The abstract type

The state is a vector $x \in \mathbb{Z}^n$, at first zero, with $|x_i| \le M$ at all times for a known $M$ that is polynomial in $n$.

- **Update(i, d)** sets $x_i \leftarrow x_i + d$.
- **Query()** returns one of three answers. EMPTY means $x = 0$. A pair $(i, x_i)$ means $x_i \ne 0$. FAIL means the sketch gives no answer.
- **Add(S₁, S₂)** returns the sketch of $x + y$ from the sketches of $x$ and $y$, if both use the same random seeds.

The guarantee: if $x = 0$ the answer is EMPTY. If $x \ne 0$, the answer is FAIL with probability at most $\delta$, a wrong answer (a wrong pair, or EMPTY) has probability at most $R(L + 1)\,n/q$, where $R$, $L$ and $q$ are defined below, and the returned coordinate is close to uniform over $\mathrm{supp}(x) = \{i : x_i \ne 0\}$. The probability is over the random seeds only; the sequence of updates is fixed in advance.

## Representation

The sketch has $R = \lceil \ln(1/\delta)/\ln(32/17) \rceil$ independent copies. Fix a prime $q$ larger than $nM$ and polynomial in $n$, for example $q > n^4$, so that $R(L + 1)\,n/q$ is small. Each copy has:

- a hash function $h : [n] \to \{0, \ldots, q - 1\}$, a random polynomial of degree $k - 1$ over $\mathbb{Z}_q$, so $h$ is [k-wise independent](/k-wise-independent-hashing/);
- a random base $z \in \{1, \ldots, q - 1\}$ for the fingerprint;
- $L + 1$ levels, $L = \lceil \log_2 n \rceil + 2$. Coordinate $i$ belongs to level $j$ if $h(i) < q/2^j$, so every coordinate is on level 0, about half are on level 1, and the levels are nested;
- for each level $j$, three counters over the coordinates on that level:
$$A_j = \sum_{i} x_i, \qquad B_j = \sum_{i} i\,x_i, \qquad C_j = \sum_{i} x_i z^i \bmod q.$$

The triple $(A, B, C)$ is a 1-sparse recovery structure. Every counter is a linear function of $x$, so the whole sketch is a matrix times $x$, and Add is entry-wise addition.

## Operations

```pseudo id=main
UPDATE(i, d)
for each copy with hash h and base z:
L1  t ← the deepest level j ≤ L with h(i) < q / 2^j
L2  for j ← 0 to t do A_j ← A_j + d; B_j ← B_j + i·d; C_j ← C_j + d·z^i mod q

DECODE(A, B, C)
L3  if A = 0 and B = 0 and C = 0 then return ZERO
L4  if A ≠ 0 and A divides B and i = B/A is in 1..n and C = A·z^i mod q then return ONE(i, A)
L5  return MANY

QUERY()
L6  for each copy:
L7      for j ← L down to 0: r ← DECODE(A_j, B_j, C_j); if r = ZERO, go on to j − 1
L8          if r = ONE(i, v) then return (i, v); if r = MANY, stop this copy
L9      if every level gave ZERO then return EMPTY
L10 return FAIL
```

Query scans from the deepest level up. The first level that is not ZERO is the deepest level that holds a nonzero coordinate. If exactly one coordinate of the support lives there, DECODE returns it. If two or more do, this copy gives up, and the next copy is tried.

## Example

Take $n = 8$, $\delta = 1/2$, so $R = 2$ copies and $L = 5$. The code of this page with seed 0 gives copy 1 the levels

| coordinate | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| deepest level | 1 | 2 | 1 | 0 | 3 | 1 | 1 | 1 |

The updates are $(2, +3)$, $(5, +1)$, $(7, +2)$, $(4, -1)$, $(5, -1)$, $(6, +5)$, $(6, -5)$. At the end $x_2 = 3$, $x_4 = -1$, $x_7 = 2$, and all other coordinates are 0, because coordinates 5 and 6 went up and down again. The counters of copy 1 are:

| level $j$ | coordinates of the support on level $j$ | $A_j$ | $B_j$ | DECODE |
|---|---|---|---|---|
| 5, 4 | none | 0 | 0 | ZERO |
| 3 | none (5 is on it, but $x_5 = 0$) | 0 | 0 | ZERO |
| 2 | 2 | 3 | 6 | ONE(2, 3) |
| 1 | 2, 7 | 5 | 20 | MANY |
| 0 | 2, 4, 7 | 4 | 16 | MANY |

Query stops at level 2 and returns $(2, 3)$. Levels 1 and 0 show why the fingerprint is needed. On both, $B/A = 4$, which is a valid coordinate, but $C_1 = 3z^2 + 2z^7 \ne 5z^4$ and $C_0 = 3z^2 - z^4 + 2z^7 \ne 4z^4$, so line L4 rejects them. Level 3 has $A = B = C = 0$ even though coordinate 5 was updated, because the sketch is linear and the updates cancelled.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has four parts.

1. **The 1-sparse test.** If the vector $y$ on a level is zero, DECODE returns ZERO. If $y$ has exactly one nonzero coordinate $i$, then $A = y_i$, $B = i\,y_i$, $C = y_i z^i$, and DECODE returns $(i, y_i)$. If $y$ has two or more nonzero coordinates, a wrong ONE needs $\sum_\ell y_\ell z^\ell - A z^{i} \equiv 0 \pmod q$ for the computed $i$. This is a nonzero polynomial in $z$ of degree at most $n$ over the field $\mathbb{Z}_q$, so it has at most $n$ roots, and a random $z$ is a root with probability at most $n/q$ (the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) in one variable). ZERO is also wrong only on a root of $\sum_\ell y_\ell z^\ell$.
2. **The answer is the min-hash coordinate.** Because the levels are nested, the deepest level with a nonzero coordinate is the level of the coordinate $i^*$ of the support with the smallest hash. If DECODE returns ONE there, it returns $i^*$. So the output is the [min-wise](/min-wise-independent-hashing/) element of the support, which is uniform when $h$ is a random function.
3. **One copy succeeds with probability at least 15/32**, if $h$ is a random function. The copy fails only if the two smallest hash values of the support fall on the same level. Above level $L$ this needs $h_{(2)} < 2h_{(1)}$, which has probability exactly $1/2$. On level $L$ it needs two values below $q/2^L \le q/(4n)$, which has probability at most $1/32$.
4. **Copies.** The copies use independent seeds, so all $R$ copies fail with probability at most $(17/32)^R \le \delta$.

Part 3 is proved for a truly random $h$. With a $k$-wise independent $h$ the success probability and the uniformity hold up to an error that falls exponentially in $k$; this follows from the min-wise results of Indyk (2001) and is not proved here. Jowhari, Sağlam and Tardos avoid this step with $s$-sparse recovery, see the variants.

## Complexity

**Space.** There are $R(L + 1) = O(\log n \log(1/\delta))$ levels, each with three counters. $|A| \le nM$, $|B| \le n^2 M$ and $C < q$, so each counter has $O(\log n)$ bits when $M$ and $q$ are polynomial in $n$. Each copy also keeps $k$ hash coefficients and $z$, $O(k \log n)$ bits. The total is $O(\log^2 n \log(1/\delta))$ bits for constant $k$. The code uses the fixed prime $q = 2^{61} - 1$ and Python integers.

**Time.** An update evaluates one hash per copy, $O(k)$ operations, computes $z^i \bmod q$ in $O(\log n)$ multiplications, and changes at most $L + 1$ levels. So it costs $O(\log n \log(1/\delta))$ word operations. In expectation a coordinate is on only 2 levels per copy, so the expected cost is $O(\log n \cdot R)$ for the powers and $O(R)$ for the counters. A query runs DECODE at most $L + 1$ times per copy, $O(\log n \log(1/\delta))$ in all.

**Lower bound.** Jowhari, Sağlam and Tardos showed that sampling from vectors with entries in $\{0, \pm 1\}$ needs $\Omega(\log^2 n)$ bits for constant $\delta$. Kapralov, Nelson, Pachocki, Wang, Woodruff and Yahyazadeh (2017) proved the bound $\Omega(\min\{n, \log(1/\delta)\log^2(n/\log(1/\delta))\})$ for the universal relation problem and derived matching bounds for samplers. So the space of this page is optimal up to constants for most $\delta$.

## Variants

- **s-sparse recovery per level.** Jowhari, Sağlam and Tardos keep an $s$-sparse recovery structure with $s = O(\log(1/\delta))$ on each level and use only $O(\log n)$ levels in one copy. A level with between 1 and $s$ nonzero coordinates is recovered in full, and a uniform element of it is returned. This gives zero relative error: conditioned on success, the output is exactly uniform.
- **Lp samplers.** Scaling each coordinate by a random factor $u_i^{-1/p}$ and finding the heaviest coordinate with a [Count-Sketch](/count-sketch/) samples $i$ with probability close to $|x_i|^p/\|x\|_p^p$ for $0 < p < 2$ (Monemizadeh and Woodruff 2010; Andoni, Krauthgamer and Onak 2011; Jowhari, Sağlam and Tardos 2011).
- **Strict turnstile.** If all $x_i \ge 0$ at the end, a level with $A_j \cdot B_j^{(2)} = B_j^2$, where $B^{(2)} = \sum i^2 x_i$, holds one coordinate, and no fingerprint is needed. This variant fails for general signs.
- **Insertion-only streams.** Without deletions, [reservoir sampling](/reservoir-sampling/) on distinct elements, or a min-hash over the items, gives the same output with $O(\log n)$ bits.

## When to use it

Use an L0 sampler when the data has deletions, or when you need to add and subtract sketches. The main use is in graph sketches: a sampler of the signed incidence vector of a set of vertices returns an edge that leaves the set, which drives the [AGM graph sketch](/agm-graph-sketch/) for connectivity, spanning forests and cuts. Other uses are finding duplicates in a stream, sampling distinct items under deletions, and estimating the [number of distinct elements](/distinct-elements-problem/) of subsets. If the stream has no deletions, a plain sample or a min-hash is smaller and simpler.

## Pitfalls

- **Same seeds for Add.** Two sketches can be added only if they use the same hash functions and bases. In AGM, each vertex keeps its own counters but all vertices share the seeds.
- **Do not trust B/A alone.** With mixed signs, $B/A$ can be a valid coordinate when the level holds many coordinates, as at levels 0 and 1 of the example. The fingerprint check of line L4 is needed.
- **Prime too small.** The test needs $q > \max|y_i|$ so that a nonzero value is nonzero modulo $q$, and $q \gg n$ so that the false accept rate $n/q$ is small. With the code's $q = 2^{61} - 1$ the rate is below $2^{-40}$ for $n \le 2^{20}$.
- **Adaptive updates.** The guarantee is for a stream fixed before the seeds are drawn. If the updates depend on earlier answers, as in a Borůvka loop that reuses one sketch, use fresh sketches for each round.
- **Low independence.** A pairwise independent hash makes the output far from uniform on some inputs. Use $k$-wise independence with $k = \Theta(\log(1/\varepsilon))$ for an $\varepsilon$ bias, or the $s$-sparse variant.

## Implementations

## History

Cormode, Muthukrishnan and Rozenbaum (VLDB 2005) used nested hash levels with small recovery structures to sample distinct items under deletions, which they called inverse sampling. Frahling, Indyk and Sohler (SoCG 2005) gave samplers for dynamic geometric streams with $O(\log^3 n)$ bits. Monemizadeh and Woodruff (SODA 2010) extended sampling to $\ell_p$ weights. Jowhari, Sağlam and Tardos (PODS 2011) gave the $O(\log^2 n)$ bit L0 sampler with zero relative error and the first tight lower bound, and Kapralov et al. (FOCS 2017) settled the dependence on $\delta$. Ahn, Guha and McGregor (SODA 2012) used L0 samplers to sketch graphs, which made them a standard tool.

## References
