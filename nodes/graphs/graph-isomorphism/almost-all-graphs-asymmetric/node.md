---
tag: VJYCP9
kind: theorem
slug: almost-all-graphs-asymmetric
name: Almost all graphs are asymmetric
aliases:
- Erdős-Rényi asymmetry theorem
area: graphs/graph-isomorphism
level: core
summary: For random graphs G(n,1/2) the probability of being asymmetric tends to 1 as n grows; equivalently, almost all labeled graphs have trivial automorphism group.
prereqs: [asymmetric-graph, erdos-renyi-model, union-bound, permutation]
see_also: [graph-automorphism-group, graph-automorphism, canonical-labeling, weisfeiler-leman, probabilistic-method, burnside-lemma]
sources:
  - paper: doi:10.1007/BF01895716
    title: Paul Erdős and Alfréd Rényi, Asymmetric graphs, Acta Mathematica Academiae Scientiarum Hungaricae 14, 295 to 315 (1963)
    locator: the whole paper (almost all graphs are asymmetric, with the asymptotic probability of a symmetry)
  - book: isbn:9780521797221
    title: Béla Bollobás, Random Graphs, second edition, Cambridge University Press, 2001
    locator: Chapter 9, The automorphism group (asymmetry of random graphs)
  - paper: doi:10.1137/0209047
    title: László Babai, Paul Erdős and Stanley M. Selkow, Random graph isomorphism, SIAM Journal on Computing 9(3), 628 to 635 (1980)
    locator: the whole paper (a stronger statement, canonical labeling of almost all graphs by degrees)
---

A graph is [asymmetric](/asymmetric-graph/) when its only automorphism is the identity. Erdős and Rényi proved in 1963 that almost all graphs are asymmetric: if every pair of $n$ labeled vertices is joined with probability $1/2$, independently, the probability that the graph has a non-trivial automorphism tends to 0 as $n$ grows. Small graphs are often symmetric, but symmetry is a rare accident in large graphs. The theorem explains why the number of graphs up to isomorphism is about $2^{\binom n2}/n!$, and why isomorphism tests based on refinement work on random inputs.

## Statement

Let $G \sim G(n, 1/2)$ be the [Erdős-Rényi random graph](/erdos-renyi-model/) on the vertex set $[n] = \{1, \ldots, n\}$: each of the $N = \binom n2$ pairs is an edge with probability $1/2$, independently. Equivalently, $G$ is a uniformly random labeled simple undirected graph on $[n]$. The graphs are uncolored and undirected.

**Theorem.** For $n \ge 3$,
$$\Pr[\mathrm{Aut}(G) \ne \{\mathrm{id}\}] \le \sum_{s=2}^{n} \left( n \cdot 2^{-(n-2)/4} \right)^{s},$$
and this tends to 0 as $n \to \infty$. Hence the fraction of labeled graphs on $[n]$ that are asymmetric tends to 1. Moreover $\Pr[\mathrm{Aut}(G) \ne \{\mathrm{id}\}] \ge 2^{-(n-2)}$ for $n \ge 2$, so the convergence is not faster than exponential.

## In plain words

Draw a large network by flipping a fair coin for every pair of points to decide whether to link them. Then the network almost surely has no symmetry: no way to move points around, other than leaving every point in place, keeps all the links. A symmetry would need a lot of luck. If it moves some points, then many pairs of points move to other pairs, and the coin flips for each such pair and its image must agree. Each agreement has chance one half, and there are so many of them that the total chance shrinks to zero, even after you count all possible symmetries.

## Proof

Fix a permutation $\sigma \ne \mathrm{id}$ of $[n]$, and let $s \ge 2$ be the size of its support, the set of vertices it moves. The permutation $\sigma$ acts on the set $\mathcal P$ of the $N$ unordered pairs by $\{u, v\} \mapsto \{\sigma(u), \sigma(v)\}$, and $\mathcal P$ splits into the cycles of this action. Let $c$ be the number of cycles.

*Step 1: the probability for one permutation.* $\sigma$ is an automorphism of $G$ exactly when, for every pair $p$, $p \in E \iff \sigma(p) \in E$, that is, when every cycle of pairs lies entirely inside $E$ or entirely outside. The pairs are independent with probability $1/2$ each, so a cycle of length $\ell$ is all in or all out with probability $2 \cdot 2^{-\ell} = 2^{1 - \ell}$, and
$$\Pr[\sigma \in \mathrm{Aut}(G)] = \prod_{\text{cycles } C} 2^{1 - |C|} = 2^{c - N}.$$

*Step 2: many pairs move.* Call a pair moved when $\sigma(p) \ne p$. Let $u$ be in the support and $w$ outside it. Then $\sigma(\{u, w\}) = \{\sigma(u), w\}$, and $\sigma(u) \ne u$; also $\sigma(u) \ne w$, since $w$ is the image of itself only. So $\{u, w\}$ is moved, and there are $s(n - s)$ such pairs. A pair $\{u, v\}$ inside the support is fixed only when $\sigma$ swaps $u$ and $v$, and there are at most $s/2$ such pairs. So the number $M$ of moved pairs satisfies
$$M \ge s(n - s) + \binom s2 - \frac s2 = \frac{s(2n - s - 2)}{2} \ge \frac{s(n - 2)}{2},$$
using $s \le n$ in the last step.

*Step 3: few cycles.* Every fixed pair is a cycle of length 1, and every moved pair lies in a cycle of length at least 2. So the number of cycles is $c \le (N - M) + M/2 = N - M/2$, and by Steps 1 and 2,
$$\Pr[\sigma \in \mathrm{Aut}(G)] = 2^{c - N} \le 2^{-M/2} \le 2^{-s(n-2)/4}.$$

*Step 4: union bound.* The number of permutations with support of size exactly $s$ is at most $\binom ns s! \le n^s$. By the [union bound](/union-bound/),
$$\Pr[\mathrm{Aut}(G) \ne \{\mathrm{id}\}] \le \sum_{s=2}^{n} n^s \, 2^{-s(n-2)/4} = \sum_{s=2}^{n} x^s, \qquad x = n \cdot 2^{-(n-2)/4}.$$
As $n \to \infty$, $x \to 0$ because $2^{(n-2)/4}$ grows faster than $n$. Once $x < 1$ the sum is at most $x^2 / (1 - x)$, which tends to 0.

*Lower bound.* The transposition $\tau = (1\,2)$ is an automorphism exactly when vertices 1 and 2 have the same neighbors among $3, \ldots, n$; the pair $\{1, 2\}$ itself is fixed by $\tau$. These are $n - 2$ independent events of probability $1/2$, so $\Pr[\tau \in \mathrm{Aut}(G)] = 2^{-(n-2)}$, and the probability of some non-trivial automorphism is at least this. $\blacksquare$

## Consequences

- **Counting graphs up to isomorphism.** Let $g_n$ be the number of isomorphism classes of graphs on $n$ vertices. A class with automorphism group $A$ contains $n! / |A|$ labeled graphs, so $2^{N} \le n! \, g_n$, with near equality when almost all labeled graphs are asymmetric. Hence $g_n \sim 2^{\binom n2} / n!$ (Pólya; Oberschelp gave the full asymptotic series).
- **Isomorphism is easy on average.** Babai, Erdős and Selkow (1980) proved a stronger statement: for almost all graphs, the degrees of the vertices and of their neighbors give every vertex a distinct label. So a linear-time [canonical labeling](/canonical-labeling/), and [color refinement](/weisfeiler-leman/), succeed on almost all graphs.
- **Isomorphisms are unique.** For almost all pairs of isomorphic graphs there is exactly one isomorphism, since the set of isomorphisms is a coset of $\mathrm{Aut}(G)$.
- **Hard instances are special.** The inputs that defeat practical isomorphism tools, such as strongly regular graphs and the [Cai-Fürer-Immerman](/cai-furer-immerman-construction/) graphs, are highly structured and rare among all graphs.

## Tightness

- **Small $n$.** The statement is asymptotic. For small $n$ the fraction of asymmetric labeled graphs is far from 1. An exhaustive count gives:

| $n$ | asymmetric labeled graphs | all labeled graphs | fraction |
|---|---|---|---|
| 5 | 0 | 1024 | 0 |
| 6 | 5760 | 32768 | 0.176 |
| 7 | 766080 | 2097152 | 0.365 |

These are $8 \cdot 6!$ and $152 \cdot 7!$: there are 8 asymmetric graphs on 6 vertices and 152 on 7 vertices up to isomorphism.

- **The bound in the proof is crude.** The value $x^2/(1-x)$ is below 1 only from $n = 23$ on; it is about $3.2 \cdot 10^{-3}$ at $n = 40$ and $1.5 \cdot 10^{-4}$ at $n = 50$. The true probability of a symmetry is dominated by transpositions of two vertices with the same neighbors, and so by the lower bound up to a polynomial factor; Erdős and Rényi computed its asymptotic value.
- **Other edge probabilities.** For $G(n, p)$ the statement fails when $p$ is very small, for example below $(\ln n)/n$, where isolated vertices appear and any two of them can be swapped. For $p$ and $1 - p$ not too small, almost all graphs are still asymmetric (Wright 1971; see Bollobás, Chapter 9).
- **Restricted classes.** The theorem fails for classes that force symmetry, such as vertex-transitive graphs, and holds in other forms for others: almost all regular graphs of fixed degree $d \ge 3$ are asymmetric, but almost all trees are not, since a random tree has many pairs of leaves at a common vertex.

## History

Erdős and Rényi proved the theorem in "Asymmetric graphs" (1963), together with results on how many edges must be changed to make a graph symmetric. Pólya and later Oberschelp (1967) had found the asymptotic number of unlabeled graphs, which is equivalent to the statement on average. Wright (1971) extended the theorem to $G(n, p)$. Babai, Erdős and Selkow (1980) turned it into an algorithm, a canonical labeling that works for almost all graphs.

## References
