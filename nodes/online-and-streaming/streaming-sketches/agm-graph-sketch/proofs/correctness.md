---
title: The AGM sketch returns a spanning forest of the final graph, except with probability at most n((1 + δ)/2)^R plus the error of the samplers
proves: [correctness]
status: full
---

Let $G = (V, E)$ be the final graph on $V = [n]$, with edge multiplicities $m_{uv} \in \mathbb{Z}$ given by the stream (insertions minus deletions). The graph of the problem has $m_{uv} \in \{0, 1\}$; the lemmas below only need that an edge is present exactly when $m_{uv} \ne 0$. For a set $S \subseteq V$ write $\partial S$ for the set of edges with exactly one end in $S$.

**The sampler.** We use the [L0 sampler](/l0-sampler/) as a black box with these properties, for a vector $y$ that is fixed before its seeds are drawn:

- (P1) Linearity. The counters are a fixed linear function of $y$ once the seeds are fixed. So, for sketches with the same seeds, $\mathcal{S}(y) + \mathcal{S}(y') = \mathcal{S}(y + y')$.
- (P2) Under the good event $G_{\text{samp}}$ of the sampler (every 1-sparse test answers correctly), a query returns EMPTY if $y = 0$, and otherwise returns a coordinate $i$ with $y_i \ne 0$ or FAIL.
- (P3) If $y \ne 0$, the query returns FAIL with probability at most $\delta$.

The L0 sampler page proves (P2) with $\Pr[\text{not } G_{\text{samp}}] \le c(L + 1)N/(q - 1)$ for a sampler of dimension $N$ with $c$ copies, and (P3) for a random hash.

**Lemma 1 (cut lemma).** For every $S \subseteq V$, the vector $y_S = \sum_{w \in S} a_w$ has the value $m_{uv}([u \in S] - [v \in S])$ at the coordinate of the pair $u < v$. In particular $\mathrm{supp}(y_S) = \partial S$.

*Proof.* By the definition of $a_w$, the coordinate of $u < v$ of $a_w$ is $m_{uv}$ if $w = u$, $-m_{uv}$ if $w = v$, and 0 otherwise. Summing over $w \in S$ gives $m_{uv}[u \in S] - m_{uv}[v \in S]$. This is nonzero exactly when $m_{uv} \ne 0$ and exactly one of $u, v$ lies in $S$, that is, when $\{u, v\} \in \partial S$. $\square$

**Lemma 2 (the vertex sketches follow the stream).** After the stream, the round-$r$ counters of vertex $w$ equal $\mathcal{S}_r(a_w)$, and for every $S$, $\sum_{w \in S}\mathcal{S}_r(a_w) = \mathcal{S}_r(y_S)$.

*Proof.* An update $(u, v, d)$ with $u < v$ changes the coordinate $e$ of $u < v$ by $+d$ in $a_u$ and by $-d$ in $a_v$, and leaves all other vectors alone. Line L2 applies exactly these turnstile updates to the samplers of $u$ and $v$ in every round. By (P1) the counters after all updates are $\mathcal{S}_r$ of the sum of the updates, which is $a_w$. The second claim is (P1) applied to the shared seeds of round $r$. $\square$

**The good event.** Let $G_\star$ be the event that every query made in line L6 satisfies (P2). There are at most $Rn$ queries. Each query concerns a vector $y_C$ where $C$ is determined by rounds before $r$, which are independent of the seeds of round $r$. So the bound of (P2) applies to each query, and by the union bound $\Pr[\text{not } G_\star] \le Rn \cdot c(L + 1)N/(q - 1)$, which is $1/\mathrm{poly}(n)$ for $q$ polynomial in $n$ of large enough degree. From here on we assume $G_\star$ for the deterministic statements.

**Lemma 3 (safety).** Under $G_\star$, at all times: (a) every edge in $F$ is an edge of $G$; (b) $F$ is a forest, and the components of the algorithm are exactly the vertex sets of the trees of $F$; (c) every closed component is a connected component of $G$.

*Proof.* At the start $F = \emptyset$ and each vertex is a component, so (a) to (c) hold. In round $r$, a query on a component $C$ that returns an edge returns, by (P2) and Lemma 1, an edge of $\partial C$, which is an edge of $G$. Line L8 adds such an edge $\{a, b\}$ only if $a$ and $b$ are in different components, that is, in different trees of $F$; adding it joins two trees into one tree, and the components are merged in the same way. So (a) and (b) are kept.

For (c): a component $C$ is marked closed in line L7 only if its query returns EMPTY, which by (P2) means $y_C = 0$, so $\partial C = \emptyset$ by Lemma 1. The vertices of $C$ are connected in $G$, because by (b) they are joined by the tree of $F$ on $C$ and by (a) its edges lie in $G$. A connected set with no edge leaving it is a connected component of $G$. A closed component never takes part in a merge later, because no edge of $\partial C$ exists, so no pick of another component joins it; so it stays closed and (c) is kept. $\square$

**Corollary.** Under $G_\star$, if every component is closed when SPANNING-FOREST returns, then $F$ is a spanning forest of $G$. Indeed, by Lemma 3 the trees of $F$ are spanning trees of the connected components of $G$, one per component.

**Lemma 4 (one round).** Let a round start with $k$ components that have $\partial C \ne \emptyset$, and let $s$ of them get an edge in line L7. Then after line L8 at most $k - s/2$ components have $\partial C \ne \emptyset$.

*Proof.* Consider the auxiliary graph $H$ whose nodes are the components at the start of the round and whose edges are the picks. A pick is an edge of $\partial C$ for some component $C$, so its other end lies in a component that also has $\partial \ne \emptyset$; components with $\partial C = \emptyset$ are isolated in $H$. Line L8 merges the components exactly along the connected parts of $H$ (it adds a pick when its ends are in different current components, which is the rule of a union-find run over the edges of $H$). A connected part of $H$ with $t$ nodes becomes one component. Every one of the $s$ components with a pick lies in a part with $t \ge 2$ nodes, since its pick joins it to another component. A part with $t \ge 2$ nodes reduces the number of components by $t - 1 \ge t/2$, and these parts together contain at least $s$ nodes, so the number of components among the $k$ drops by at least $s/2$. Components with $\partial C = \emptyset$ before the round do not change. So at most $k - s/2$ components that come from the $k$ are left, and only these can have a nonempty boundary. $\square$

**Theorem 1.** Let each sampler fail with probability at most $\delta$ as in (P3), let $\rho = (1 + \delta)/2$, and let $R \ge \log(n/\delta_{\text{all}})/\log(1/\rho)$. Then SPANNING-FOREST returns a spanning forest of $G$ with probability at least $1 - \delta_{\text{all}} - \Pr[\text{not } G_\star]$.

*Proof.* Let $k_r$ be the number of components with $\partial C \ne \emptyset$ at the start of round $r$, so $k_1 \le n$. Fix everything that happens in rounds $1, \ldots, r - 1$. This fixes the components of round $r$, and it depends only on the seeds of rounds before $r$. The seeds of round $r$ are fresh, so for each of the $k_r$ components, (P3) applies to the fixed nonzero vector $y_C$, and the query fails with probability at most $\delta$. So the expected number $s$ of components that get an edge is at least $(1 - \delta)k_r$, and Lemma 4 gives
$$\mathbb{E}[k_{r+1} \mid \text{rounds } 1..r-1] \le k_r - \tfrac{1}{2}(1 - \delta)k_r = \rho\, k_r.$$
Taking expectations and iterating, $\mathbb{E}[k_{R+1}] \le \rho^R n \le \delta_{\text{all}}$ by the choice of $R$. Since $k_{R+1}$ is a nonnegative integer, Markov's inequality gives $\Pr[k_{R+1} \ge 1] \le \delta_{\text{all}}$. (If the loop stops earlier because every component is closed, then $k = 0$ from then on.)

Now assume $G_\star$ and $k_{R+1} = 0$. Each component without boundary that is not yet closed will answer EMPTY at its next query by (P2), but the last round may end before that query. So consider the final partition: every component has $\partial C = \emptyset$, and by Lemma 3 (a) and (b) its vertices are joined by a tree of $F$ made of edges of $G$. A connected vertex set with empty boundary is a connected component of $G$. Hence $F$ is a spanning forest of $G$, whether or not the component was marked closed. The failure probability is at most $\Pr[k_{R+1} \ge 1] + \Pr[\text{not } G_\star]$. $\square$

**Theorem 2 (space).** With constant $\delta$ and $R = O(\log n)$, the sketch uses $O(n \log^3 n)$ bits.

*Proof.* There are $n$ vertices and $R = O(\log(n/\delta_{\text{all}}))$ rounds, which is $O(\log n)$ for $\delta_{\text{all}} = 1/\mathrm{poly}(n)$. Each vertex keeps one sampler per round. A sampler of dimension $N \le n^2$ with constant $\delta$ has $O(1)$ copies of $O(\log N) = O(\log n)$ levels, each with three counters. With multiplicities in $\{0, 1\}$, every coordinate of $a_w$ is $0$ or $\pm 1$, so $|A| \le N$, $|B| \le N^2$ and $0 \le C < q$; with $q$ polynomial in $n$, each counter has $O(\log n)$ bits. The product is $n \cdot O(\log n) \cdot O(\log n) \cdot O(\log n) = O(n \log^3 n)$ bits. The seeds add $O(R \log n)$ words. $\blacksquare$
