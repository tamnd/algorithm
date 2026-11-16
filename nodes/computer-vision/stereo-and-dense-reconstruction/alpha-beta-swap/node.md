---
tag: Y9ZT41
kind: algorithm
slug: alpha-beta-swap
name: Alpha-beta swap
aliases:
- swap move algorithm
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: Minimize a multi-label energy with a semimetric pairwise term by repeated min cuts, each letting the sites labeled alpha or beta exchange those two labels. No constant factor bound.
solves: [map-inference]
model: real-ram
complexity:
  vars: {n: the number of sites, m: the number of neighbor pairs, L: the number of labels, k: the number of cycles over the label pairs, F: the time of one max flow on n + 2 nodes and n + m edges}
  time: {worst: O(k L^2 (F + n + m)), average: O(k L^2 (F + n + m)), best: O(L^2 (F + n + m))}
  space: {extra: O(n + m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2001
  people: [Yuri Boykov, Olga Veksler, Ramin Zabih]
  note: Boykov, Veksler and Zabih introduced the swap move together with the expansion move, and showed that swap works for any semimetric but that its local minima can be arbitrarily far from the optimum.
prereqs: [graph-representable-energies, max-flow-min-cut-theorem, markov-random-field]
see_also: [alpha-expansion, iterated-conditional-modes, qpbo, boykov-kolmogorov-max-flow, potts-model, graph-cut-stereo, loopy-belief-propagation, map-inference]
sources:
  - paper: doi:10.1109/34.969114
    title: Yuri Boykov, Olga Veksler and Ramin Zabih, Fast approximate energy minimization via graph cuts, IEEE Transactions on Pattern Analysis and Machine Intelligence 23(11), 2001, 1222-1239
    locator: Section 3 (the move spaces and the swap algorithm), Section 4 with Theorem 4.4 and Corollary 4.5 (the graph of a swap move), Section 6.2 and Figure 8 (swap local minima can be arbitrarily far from the optimum), Section 8 (experiments)
  - paper: doi:10.1109/TPAMI.2004.1262177
    title: Vladimir Kolmogorov and Ramin Zabih, What energy functions can be minimized via graph cuts?, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(2), 2004, 147-159
    locator: Theorem 4.1 and Section 4.1 (the graph for a regular binary energy, used here for each move)
  - paper: doi:10.1109/TPAMI.2007.70844
    title: Richard Szeliski, Ramin Zabih, Daniel Scharstein, Olga Veksler, Vladimir Kolmogorov, Aseem Agarwala, Marshall Tappen and Carsten Rother, A comparative study of energy minimization methods for Markov random fields with smoothness-based priors, IEEE Transactions on Pattern Analysis and Machine Intelligence 30(6), 2008, 1068-1080
    locator: the comparison of swap with expansion, ICM, loopy belief propagation and TRW-S on vision energies
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 4, Model fitting and optimization (Markov random fields and graph cut moves)
---

Alpha-beta swap is a move algorithm for multi-label energies of the form data cost plus pairwise cost, as in [MAP inference](/map-inference/) for a [Markov random field](/markov-random-field/). A swap move takes two labels $\alpha$ and $\beta$ and lets every site that has one of them take either one, while all other sites keep their labels. When the pairwise cost $V$ is a semimetric, the move energy is a regular binary energy, so the best move is found exactly by one [minimum cut](/min-cut-problem/) (the [Kolmogorov-Zabih theorem](/graph-representable-energies/)). The algorithm cycles over all pairs of labels until no swap lowers the energy. Swap needs less of $V$ than [alpha-expansion](/alpha-expansion/), which needs a metric, so it covers the truncated quadratic and other costs without the triangle inequality. The price is that its local minima have no constant factor guarantee: they can be arbitrarily far from the optimum, even for the [Potts model](/potts-model/).

## In plain words

Each pixel has a label, and neighbors with different labels pay a penalty. Pick two labels, say red and blue. Look only at the pixels that are red or blue now, and let each of them be red or blue again, in the best combination. All other pixels stay as they are. A minimum cut in a graph finds the best combination exactly, even though there are very many of them. Do this for every pair of labels and repeat until no pair helps. The method only moves pixels between labels they already use, so it can miss a third label that would be better for a whole group of pixels at once.

## The problem

**Input.** Sites with neighbor pairs $\mathcal{N}$ and weights $w_{pq} \ge 0$, $L$ labels, data costs $D_p(\ell)$, and a semimetric $V$: $V(a, b) = V(b, a) \ge 0$, and $V(a, b) = 0$ exactly when $a = b$. No triangle inequality is needed.

**Output.** A labeling $f$ with small energy

$$E(f) = \sum_p D_p(f_p) + \sum_{(p,q) \in \mathcal{N}} w_{pq}\, V(f_p, f_q),$$

which no $\alpha\beta$-swap improves. An $\alpha\beta$-swap of $f$ is a labeling $g$ that differs from $f$ only on sites labeled $\alpha$ or $\beta$, and has $g_p \in \{\alpha, \beta\}$ there.

## The algorithm

```pseudo id=main
ALPHA-BETA-SWAP(D, V, N, f)
L1   repeat
L2       success ← false
L3       for each pair of labels {α, β} do
L4           P ← the sites p with f_p = α or f_p = β
L5           U_p(0) ← D_p(α) + Σ w V(α, f_q), U_p(1) ← D_p(β) + Σ w V(β, f_q), sums over neighbors q not in P
L6           for each pair (p, q) inside P: θ(0,0) = θ(1,1) = 0, θ(0,1) = w V(α, β), θ(1,0) = w V(β, α)
L7           x ← a minimizer of Σ U_p(x_p) + Σ θ(x_p, x_q) by one minimum cut
L8           f' ← f with f'_p = α if x_p = 0 and f'_p = β if x_p = 1, for p in P
L9           if E(f') < E(f) then f ← f'; success ← true
L10  until success = false
L11  return f
```

Line L5 folds the pairs with one end outside $P$ into the data terms, because the outside label is fixed. Line L6 gives the pairs inside $P$. They are regular, since $0 + 0 \le V(\alpha, \beta) + V(\beta, \alpha)$, so line L7 is one cut on a graph with $|P| + 2$ nodes: an edge $p \to q$ of capacity $w(V(\alpha, \beta) + V(\beta, \alpha))$ for each inside pair, and source or sink edges for the linear parts. Boykov, Veksler and Zabih use the equivalent graph with a terminal edge to $\alpha$ and to $\beta$ for each site and an edge of capacity $w V(\alpha, \beta)$ for each inside pair (Section 4 of their paper).

## Example

Two neighboring sites $p$ and $q$, $w = 1$, labels $a, b, c$, the Potts model with $\lambda = 6$, and data costs $D_p = (0, 9, 1)$, $D_q = (9, 0, 1)$ for $(a, b, c)$. Start at $(a, b)$, which has $E = 0 + 0 + 6 = 6$.

| swap | labelings in the move space | energies | best |
|---|---|---|---|
| $\{a, b\}$ | $(a,b)$, $(b,a)$, $(a,a)$, $(b,b)$ | 6, 24, 9, 9 | $(a, b)$ |
| $\{a, c\}$ | $(a,b)$, $(c,b)$ | 6, 7 | $(a, b)$ |
| $\{b, c\}$ | $(a,b)$, $(a,c)$ | 6, 7 | $(a, b)$ |

No swap helps, so the algorithm stops at $(a, b)$ with $E = 6$. The optimum is $(c, c)$ with $E = 1 + 1 = 2$. A swap with $c$ can move only one of the two sites, since the other has a third label, and moving one site alone costs more. The $c$-expansion moves both at once and finds $(c, c)$. With $D_p(c) = D_q(c) = \delta$ and $\lambda = D_p(b) = D_q(a) = M$, the swap result costs $\lambda$ and the optimum $2\delta$, so the ratio is unbounded.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The binary energy of lines L5 and L6 equals the energy of the swap it describes, up to a constant made of the terms that do not touch $P$. Its pair terms are regular because $V(\alpha, \alpha) = V(\beta, \beta) = 0$ and $V \ge 0$, so the cut of line L7 gives the best swap. Each accepted move lowers the energy strictly and there are finitely many labelings, so the loop stops; in the last cycle no pair of labels gives an improving swap. The example above, with $\delta \to 0$, shows that no constant factor bound holds.

## Complexity

The model is the real RAM; the tests use integer costs.

- **One move.** The graph has $|P| + 2$ nodes and at most $|P|$ plus the inside pairs as edges. Building it takes time linear in $|P|$ and the pairs that touch $P$, and the cut takes at most the time $F$ of one max flow on $n + 2$ nodes and $n + m$ edges.
- **One cycle.** $L(L-1)/2$ moves. Each site is in $P$ for $L - 1$ of them, so the graphs of one cycle have $(L - 1) n$ site nodes in total. A crude bound is $O(L^2 (F + n + m))$.
- **Number of cycles.** With integer costs at most $E(f_0) - \min E + 1$.
- **Space.** $O(n + m)$.

## Properties

- **No approximation bound.** Section 6.2 and Figure 8 of Boykov, Veksler and Zabih: a swap local minimum can be arbitrarily far from the global minimum. Theorem 6.2 there gets a bound $2c$ by a different route, by replacing $V$ with a Potts model and running expansion, not by swap itself.
- **Weaker condition.** Only $V(a, a) = 0$ and $V \ge 0$ are used by the move, so truncated quadratic and other semimetrics are fine.
- **Stronger than one site at a time.** A change of one site from $\alpha$ to $\beta$ is a swap, so a swap local minimum is also a local minimum of [ICM](/iterated-conditional-modes/).
- **Neither move contains the other.** A swap can exchange $\alpha$ and $\beta$ between sites, which no single expansion does; an expansion can bring sites of many labels to $\alpha$ at once, which no single swap does.
- **Small graphs.** Each cut involves only the sites of two labels, so the graphs are smaller than those of expansion, but a cycle has $L(L-1)/2$ of them instead of $L$.

## Variants and improvements

- **Alpha-expansion.** For a metric $V$, [alpha-expansion](/alpha-expansion/) is usually better and has the bound $2c$.
- **Range moves.** For ordered labels and truncated convex $V$, Veksler (2007) proposed moves that let a set of sites take any label in a range of consecutive labels, solved by the construction of Ishikawa (2003). They generalize the swap move.
- **Nonregular moves.** If $V(a, a) \ne 0$ or a learned $V$ breaks the condition, the move energy can be nonregular; [QPBO](/qpbo/) then labels part of the sites.

## When to use it

Use swap when $V$ is a semimetric but not a metric, for example truncated quadratic smoothness on ordered labels, and when an approximation bound is not needed. In the benchmark of Szeliski et al. (2008), expansion usually reached a lower energy than swap. For a metric $V$, use [alpha-expansion](/alpha-expansion/). For a few labels on a chain, an exact [Viterbi](/viterbi-algorithm/) dynamic program is better than any move method.

## Pitfalls

- **The start and the order matter.** The local minimum depends on the starting labeling and on the order of the label pairs. Start from the best data label of each site, and keep the order fixed when you compare runs.
- **No guarantee.** Do not quote a factor of 2 for swap; that is the expansion bound.
- **Ties.** Accept a move only if it lowers the energy strictly.
- **Number of moves.** With many labels the $L^2/2$ moves per cycle are slow. Skip the pairs whose sites are not neighbors anywhere, or use expansion.

## Implementations

## History

Boykov, Veksler and Zabih introduced swap and expansion moves at ICCV 1999 and in the journal paper of 2001. They gave a graph for each move, proved that the swap move is a cut for a semimetric, and showed that swap local minima have no constant factor bound while expansion local minima are within $2c$. Kolmogorov and Zabih (2004) explained both conditions as cases of regularity. Szeliski et al. (2008) compared swap with other methods on a common benchmark.

## References
