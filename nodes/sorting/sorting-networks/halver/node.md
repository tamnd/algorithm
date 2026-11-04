---
tag: EPJBZB
kind: definition
slug: halver
name: Halver
aliases:
- epsilon-halver
- AKS halver
area: sorting/sorting-networks
level: advanced
summary: A network that roughly halves the inputs so that large and small values end up on the correct sides up to an epsilon error.
prereqs: [sorting-network, bipartite-graph]
see_also: [aks-sorting-network, zero-one-principle, regular-graph, perfect-matching, hall-theorem, spectral-gap, probabilistic-method, expander-codes]
sources:
  - paper: doi:10.1007/s00453-007-9025-6
    title: Joel Seiferas, Sorting networks of logarithmic depth, further simplified, Algorithmica 53 (2009)
    locator: Section 6 (the definitions of epsilon-halving and approximate separation, Lemma 1 and its proof sketch) and Section 7 (Paterson's bound on the depth of halvers)
  - paper: doi:10.1007/BF02579338
    title: M. Ajtai, J. Komlós and E. Szemerédi, Sorting in c log n parallel steps, Combinatorica 3(1) (1983)
    locator: pp. 1 to 19
  - paper: doi:10.1007/BF01840378
    title: M. S. Paterson, Improved sorting networks with O(log N) depth, Algorithmica 5 (1990)
    locator: the appendix (the theorem on the depth of halvers)
---

An $\varepsilon$-halver is a network of [comparators](/comparator/) on $2m$ wires that moves the small items to the first half and the large items to the second half, except for a fraction $\varepsilon$ of them. It does not sort, but for a fixed $\varepsilon > 0$ it can have a depth that does not depend on $m$, which no network that halves exactly can have. Halvers are built from expander graphs, and they are the building block of the [AKS sorting network](/aks-sorting-network/) of depth $O(\log n)$.

## Definition

Let $m \ge 1$ and $0 \le \varepsilon \le 1$. A comparator network $H$ on the wires $0, \ldots, 2m - 1$ has the *first half* $W_0 = \{0, \ldots, m-1\}$ and the *second half* $W_1 = \{m, \ldots, 2m-1\}$. Then $H$ is an *$\varepsilon$-halver* if, for each input of $2m$ distinct items and each $k$ with $1 \le k \le m$:

- at most $\varepsilon k$ of the $k$ smallest items end on wires of $W_1$, and
- at most $\varepsilon k$ of the $k$ largest items end on wires of $W_0$.

The condition is on every $k$, not only on $k = m$. So the few smallest items are almost all in the correct half, and that is what the AKS network needs.

**The zero-one form.** $H$ is an $\varepsilon$-halver if and only if, for each input in $\{0, 1\}^{2m}$, the number of zeros that end in $W_1$ is at most $\varepsilon z$ when the input has $z \le m$ zeros, and the number of ones that end in $W_0$ is at most $\varepsilon w$ when the input has $w \le m$ ones.

*Proof.* A comparator network commutes with each non-decreasing map $f$, as in the [zero-one principle](/zero-one-principle/). For distinct items and $k \le m$, let $f$ map the $k$ smallest items to 0 and the others to 1. Then the zeros of $H(f(x)) = f(H(x))$ are on the wires of the $k$ smallest items of $H(x)$, so the two conditions are the same. Each 0-1 input with $z$ zeros is $f(x)$ for such an $x$ with $k = z$. The ones are handled in the same way. $\square$

**The expander construction.** Let $G$ be a bipartite graph between $W_0$ and $W_1$ with this *expansion property*: each set $S$ of vertices on one side has more than $\min\bigl(|S|(1 - \varepsilon)/\varepsilon, \ (1 - \varepsilon) m\bigr)$ neighbours. Make one comparator $[u : v]$ for each edge $\{u, v\}$ with $u \in W_0$ and $v \in W_1$, which puts the minimum on $u$, in any order. Then the network is an $\varepsilon$-halver.

*Proof.* Take a 0-1 input with $z \le m$ zeros. Each comparator $[u : v]$ can only lower the value on $u$ and only raise the value on $v$. So a wire of $W_0$ never goes from 0 to 1, and a wire of $W_1$ never goes from 1 to 0. Let $S \subseteq W_1$ be the wires that end with 0. Each $v \in S$ holds 0 at all times. For each neighbour $u$ of $v$, the comparator $[u : v]$ leaves 0 on $u$, and $u$ keeps it to the end. So all wires of $S$ and of its neighbourhood $N(S)$ end with 0, and $|S| + |N(S)| \le z$. Suppose $|S| > \varepsilon z$. If $|N(S)| > |S|(1 - \varepsilon)/\varepsilon$, then $|S| + |N(S)| > |S|/\varepsilon > z$. Otherwise $|N(S)| > (1 - \varepsilon) m \ge (1 - \varepsilon) z$, and $|S| + |N(S)| > \varepsilon z + (1 - \varepsilon) z = z$. Both cases contradict $|S| + |N(S)| \le z$. So at most $\varepsilon z$ zeros end in $W_1$, and the ones are symmetric. $\square$

If $G$ is $d$-[regular](/regular-graph/), then by [Hall's theorem](/hall-theorem/) its edges split into $d$ [perfect matchings](/perfect-matching/). Each matching is one layer of $m$ comparators with disjoint wires, so the halver has depth $d$ and size $dm$. For each $\varepsilon > 0$ there is a $d$, which depends only on $\varepsilon$, such that $d$-regular bipartite graphs with the expansion property exist for each $m$. This is Lemma 1 of Seiferas: $\varepsilon$-halvers of constant depth exist.

## Examples and non-examples

**Examples.**

- **One matching.** The layer $[i : i + m]$ for $i < m$ (Batcher's half-cleaner) is a $\tfrac12$-halver for $m \ge 2$. A zero ends in $W_1$ only if its partner is also 0, so at most $z/2$ zeros do; an input with two zeros on one pair reaches $z/2$. For $m = 1$ the single comparator sorts, so it is a 0-halver.
- **The complete bipartite graph.** The $m$ layers $[u : m + ((u + s) \bmod m)]$ for $s = 0, \ldots, m-1$ give $K_{m,m}$, and the network is a 0-halver. By the proof above, a zero that ends in $W_1$ would force all $m$ wires of $W_0$ to end with 0, which needs $m + 1$ zeros. So the $m$ smallest items always end in $W_0$. It is not a sorting network for $m \ge 2$: for $m = 2$ the input $(1, 0, 2, 3)$ passes unchanged.
- **Sorting networks.** Each sorting network on $2m$ wires is a 0-halver. A 0-halver has depth more than $\lg m$. The value on an output wire is one of the inputs that can reach it, and at most $2^D$ inputs reach a wire in depth $D$. If at most $m$ inputs reached a wire of $W_0$, then putting the $m$ largest items on them would leave a large item on that wire. So exact halvers of constant depth do not exist.
- **Random matchings.** Take eight random perfect matchings between the halves of 16 wires, and let the network use the first $d$ of them. For one such choice, trying all $2^{16}$ inputs gave $\varepsilon = \tfrac12, \tfrac12, \tfrac25, \tfrac13, \tfrac27, \tfrac27, \tfrac14, \tfrac14$ for $d = 1, \ldots, 8$. More layers never make $\varepsilon$ larger here, because each comparator only moves zeros to $W_0$ and ones to $W_1$. A small $\varepsilon$ needs a large $d$, and the expansion property for large sets needs large $m$.
- **Paterson's bound.** Paterson proved that an $\varepsilon$-halver of depth $\lceil 2 \log \varepsilon / \log(1 - \varepsilon) + 2/\varepsilon - 1 \rceil$ exists for each $m$. For $\varepsilon = 1/100$ this is 1116, and for $\varepsilon = 1/700$ it is 10564.

**Non-examples.**

- **The empty network.** With no comparators, an input with its $m$ smallest items in $W_1$ keeps them there. So it is only a 1-halver, which is no condition at all.
- **A network that halves only on average.** The definition is about each input. A network that puts few items on the wrong side for most inputs, but many for some, is not an $\varepsilon$-halver for small $\varepsilon$.
- **A bound only for $k = m$.** A network for which at most $\varepsilon m$ of the $m$ smallest items end in $W_1$ may still put all of the $k$ smallest items in $W_1$ for some small $k$. The definition asks the bound for each $k \le m$.
- **Comparators in both directions.** The proof of the expander construction uses that each comparator puts its minimum on $W_0$. A network on the same edges whose comparators point in mixed directions is not an $\varepsilon$-halver in general.

## Related definitions

- **$\varepsilon$-approximate $\lambda$-separator.** For $\lambda \le 1/2$: for each $\lambda' \le \lambda$, at most $\varepsilon \lambda' n$ of the $\lfloor \lambda' n \rfloor$ smallest items end outside the first $\lfloor \lambda n \rfloor$ positions, and the same for the largest items and the last positions. For $\lambda = 1/2$ this is $\varepsilon$-halving. Seiferas builds a separator of depth $O(\log 1/\lambda)$ from halvers applied to nested prefixes and suffixes (his Lemma 2).
- **$\varepsilon$-nearsorter.** The notion of the original AKS paper, used where later versions use separators. For each $k$ it bounds by a fraction $\varepsilon$ how many of the $k$ smallest items end far from the first $k$ positions.
- **Bipartite expander.** A [bipartite graph](/bipartite-graph/) in which each small set of vertices has many neighbours. A large [spectral gap](/spectral-gap/) of a regular graph implies such expansion, and random regular graphs are expanders with high probability, by the [probabilistic method](/probabilistic-method/).
- **[AKS sorting network](/aks-sorting-network/).** It applies separators made from halvers in each bag of a binary tree, and corrects their errors over time.
- **[Sorting network](/sorting-network/).** A network that sorts each input; each one is a 0-halver.

## References
