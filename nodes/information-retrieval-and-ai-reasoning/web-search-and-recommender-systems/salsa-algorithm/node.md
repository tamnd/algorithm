---
tag: XD0VVF
kind: algorithm
slug: salsa-algorithm
name: SALSA
aliases:
- stochastic approach for link-structure analysis
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Scores hubs and authorities of a query subgraph by two random walks on its bipartite hub-authority graph; the scores reduce to degrees weighted by component size.
solves: [link-analysis-ranking]
model: word-ram
complexity:
  vars: {n: the number of pages in the base set, m: the number of links among them}
  time: {worst: O(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false, directed: true, weighted: false}
history:
  year: 2000
  people: [Ronny Lempel, Shlomo Moran]
  note: Lempel and Moran presented SALSA at the WWW9 conference in 2000 and published the full analysis in ACM TOIS in 2001.
prereqs: [hits-algorithm, markov-chain, stationary-distribution, bipartite-graph]
see_also: [pagerank, trustrank, link-analysis-ranking, connected-components, eigenvector-centrality, power-iteration, link-spam]
sources:
  - paper: doi:10.1145/382979.383041
    title: R. Lempel and S. Moran, SALSA, the stochastic approach for link-structure analysis, ACM Transactions on Information Systems 19(2), 131-160 (2001)
    locator: the two Markov chains on the bipartite hub and authority graph, the proposition that an irreducible authority chain has a stationary distribution proportional to the weighted in-degree, the proposition for several components with a uniform start, and the TKC effect of HITS; this journal version is the one the page relies on
  - paper: "R. Lempel and S. Moran, The stochastic approach for link-structure analysis (SALSA) and the TKC effect, Computer Networks 33(1-6), 387-401 (2000), Proceedings of the 9th International World Wide Web Conference (WWW9)"
    locator: the conference version, with the definition of the chains, the analysis of their stationary distributions and the examples of the TKC effect
  - paper: doi:10.1145/1052934.1052942
    title: Allan Borodin, Gareth O. Roberts, Jeffrey S. Rosenthal and Panayiotis Tsaparas, Link analysis ranking, algorithms, theory, and experiments, ACM Transactions on Internet Technology 5(1), 231-297 (2005)
    locator: the section on SALSA (on a connected graph it ranks authorities by in-degree) and the comparison of InDegree, HITS and SALSA
---

SALSA (the stochastic approach for link-structure analysis) is a link analysis algorithm that gives each page of a small query graph a hub score and an authority score, as the [stationary distributions](/stationary-distribution/) of two random walks on the [bipartite graph](/bipartite-graph/) of hubs and authorities. Ronny Lempel and Shlomo Moran introduced it in 2000 as a stochastic form of [HITS](/hits-algorithm/). Their analysis shows that the scores need no iteration at all: inside each connected component, the authority score of a page is proportional to its in-degree, and the component as a whole gets a weight proportional to its number of authorities. Because each vote is divided by the degrees, a tightly knit block of pages cannot take all the weight, as it does in HITS.

## In plain words

Search engines first collect a small set of pages about a query, with the pages that link to them and the pages they link to. Some pages are good lists of links (hubs) and some are good sources (authorities). SALSA imagines a walker who stands on a source page, goes back along a random link to a page that points to it, and then forward along a random link of that list. The fraction of time the walker spends on a page is its authority score. A second walker does the same with the roles of lists and sources swapped. When all the pages are joined together, the time spent on a source turns out to depend only on how many pages point to it. When the graph falls into separate parts, each part gets a share that depends on its size.

## The problem

The input is the base set of a query: a directed graph $G = (V, E)$ on $n$ pages with $m$ links, built as for HITS from a root set of pages that match the query, plus the pages that link to the root set and the pages that the root set links to. Self links are removed and repeated links count once. Write $\mathrm{in}(p)$ and $\mathrm{out}(q)$ for the degrees. The hub side is $H = \{q : \mathrm{out}(q) > 0\}$ and the authority side is $A = \{p : \mathrm{in}(p) > 0\}$; a page can be on both sides. The bipartite graph $\tilde G$ has an edge between hub $q$ and authority $p$ for each link $(q, p)$.

The authority chain on $A$ moves from authority $i$ to a random hub $q$ that links to $i$, then to a random authority $j$ that $q$ links to:

$$P_A(i, j) = \sum_{q :\ (q, i) \in E,\ (q, j) \in E} \frac{1}{\mathrm{in}(i)\, \mathrm{out}(q)}.$$

The hub chain on $H$ is the same with the roles swapped: $P_H(q, r) = \sum_{p :\ (q, p) \in E,\ (r, p) \in E} 1 / (\mathrm{out}(q)\, \mathrm{in}(p))$. The output is the authority vector $a = \lim_k u_A P_A^k$ and the hub vector $h = \lim_k u_H P_H^k$, where $u_A$ and $u_H$ are the uniform distributions on $A$ and $H$. In matrix form, with $W_r$ the adjacency matrix with each row divided by its sum and $W_c$ the adjacency matrix with each column divided by its sum, $P_A$ is the part of $W_c^\top W_r$ on the authority rows and columns, and $P_H$ is the part of $W_r W_c^\top$ on the hub rows and columns. HITS uses $W^\top W$ and $W W^\top$ with no division.

## The algorithm

The closed form of Lempel and Moran turns the definition into a count. Let $\tilde G$ have components $c$ with authority sets $A_c$, hub sets $H_c$ and $m_c$ links.

```pseudo id=main
SALSA(G)                                     ▷ G = (V, E), the base set of a query
L1  E ← E without self links and repeated links
L2  H ← {q : out(q) > 0}; A ← {p : in(p) > 0}
L3  label the connected components of the undirected bipartite graph G̃
L4  for each component c: count |H_c|, |A_c| and m_c = |E_c|
L5  for each p ∈ A in component c: a(p) ← (|A_c| / |A|) · in(p) / m_c
L6  for each q ∈ H in component c: h(q) ← (|H_c| / |H|) · out(q) / m_c
L7  return h, a
```

Pages ranked by $a$ (or by $h$) go highest first, with ties to the smaller page number. The definition can also be run as written, by [power iteration](/power-iteration/) of the two chains from the uniform start. Each step costs $O(m)$: spread the mass of each authority over the hubs that link to it, then the mass of each hub over its links. The test file runs both and checks that they agree.

## Example

Take twelve pages. Hubs 0 to 3 each link to authorities 9 and 10, hubs 4 to 8 each link to authority 11, and hub 0 also links to 11. So $m = 14$, $\mathrm{in}(9) = \mathrm{in}(10) = 4$ and $\mathrm{in}(11) = 6$, and $\tilde G$ is connected through hub 0. From authority 11 the walker goes back to one of its six hubs; only hub 0 can send it to 9 or 10, so $P_A(11, 9) = P_A(11, 10) = \tfrac{1}{6} \cdot \tfrac{1}{3} = \tfrac{1}{18}$ and $P_A(11, 11) = \tfrac{8}{9}$. From authority 9, $P_A(9, 9) = P_A(9, 10) = \tfrac{11}{24}$ and $P_A(9, 11) = \tfrac{1}{12}$. The stationary vector is

$$a(9) = a(10) = \tfrac{4}{14} = \tfrac{2}{7} \approx 0.2857, \qquad a(11) = \tfrac{6}{14} = \tfrac{3}{7} \approx 0.4286.$$

As a check, $a(11) P_A(11, 11) + 2 \cdot a(9) P_A(9, 11) = \tfrac{3}{7} \cdot \tfrac{8}{9} + 2 \cdot \tfrac{2}{7} \cdot \tfrac{1}{12} = \tfrac{3}{7}$. The hub scores are $\mathrm{out}(q)/14$: $\tfrac{3}{14}$ for hub 0, $\tfrac{1}{7}$ for hubs 1 to 3 and $\tfrac{1}{14}$ for hubs 4 to 8. HITS, normalized to sum 1, gives the authorities about $0.3660$, $0.3660$ and $0.2679$: it ranks the block 9 and 10 above page 11, although more pages link to 11.

Now remove the link $0 \to 11$. The graph $\tilde G$ splits into the block (four hubs, two authorities, eight links) and the star (five hubs, one authority, five links). Theorem 2 of the proof file gives $a(9) = a(10) = \tfrac{2}{3} \cdot \tfrac{4}{8} = \tfrac13$ and $a(11) = \tfrac{1}{3} \cdot \tfrac{5}{5} = \tfrac13$, and every hub gets $\tfrac19$. HITS gives $\tfrac12$, $\tfrac12$ and $0$: the dominant eigenvalue of $W^\top W$ belongs to the block (8 against 5), so the star gets nothing. This is the tightly knit community (TKC) effect that Lempel and Moran describe.

## Correctness

The file proofs/correctness.md proves the closed form. Each row of $P_A$ sums to 1. The chain is reversible with weights $\mathrm{in}(i)$, because $\mathrm{in}(i) P_A(i, j)$ is a sum over the common hubs of $1/\mathrm{out}(q)$, which is symmetric in $i$ and $j$. So $\mathrm{in}(i)/m$ is stationary. Two authorities can reach each other exactly when they lie in the same component of $\tilde G$, and every state has a positive self loop, so on a connected $\tilde G$ the chain is irreducible and aperiodic: its stationary distribution is unique, and power iteration converges to it from any start. On a general $\tilde G$ the chain splits into one block per component, the uniform start puts mass $|A_c|/|A|$ on block $c$, and the block keeps it. This gives line L5, and the hub case gives line L6.

## Complexity

Repeated links can be removed in $O(n + m)$ worst-case time by two passes of counting sort on the pairs, or in expected $O(m)$ time with a hash set. The degrees, the graph search for the components and the counts take $O(n + m)$, and lines L5 and L6 take $O(n)$. So SALSA costs $\Theta(n + m)$ time on the word RAM and $O(n + m)$ extra space for the bipartite graph, with no iteration. Power iteration of the chains costs $O(m)$ for each step, and the number of steps depends on the second eigenvalue of each block, which can be close to 1. The closed form avoids that cost. The implementation sorts the links once to fix their order, which adds $O(m \log m)$. The real cost of query-time link analysis is building the base set, which needs the links into and out of each root page.

## Properties

- **In-degree inside a component.** On a connected $\tilde G$, SALSA ranks authorities exactly as the in-degree does, and hubs exactly as the out-degree does. Borodin, Roberts, Rosenthal and Tsaparas make the same point in their comparison of link analysis rankings.
- **Component weights.** Across components, the score is the in-degree share inside the component times the share of authorities in the component. A page in a small component can beat a page with a larger in-degree in a big one, and the other way round.
- **Weighted links.** With link weights, Lempel and Moran's result uses the weighted in-degree, the sum of the weights of the links into a page.
- **Stable against dense blocks.** Because each step divides by $\mathrm{out}(q)$ and $\mathrm{in}(i)$, a dense block gets weight in proportion to its links and its authorities, not by the size of its largest eigenvalue as in HITS.
- **Deterministic and exact.** The closed form uses only integer counts, so the scores are exact rational numbers.

## Variants and improvements

- **Weighted SALSA.** Give each link a weight, for example lower for links between pages of the same site, and replace the degrees by the sums of the weights.
- **SALSA on the global graph.** The same chains can run on the whole web graph instead of a query graph; on a connected graph this is in-degree ranking, which is easy to spam with a [link farm](/link-spam/).
- **Random walks with restart.** Adding a jump to a random page, as in [PageRank](/pagerank/), makes the chain irreducible on any graph, at the cost of the closed form.
- **Other bipartite graphs.** The same two walks can run on any bipartite graph, for example users and the items they chose. The closed form shows that, without a restart, they rank items by popularity inside each component.

## When to use it

Use SALSA when you want a query-dependent link score that rewards pages many hubs point to, without the instability of HITS on graphs with a dominant dense block. Know that, on a connected base set, you get in-degree ranking, so compute it as a count. If the base set has several components, the component weights carry the extra information. For a global, query-independent score, PageRank or [TrustRank](/trustrank/) is the usual choice.

## Pitfalls

- **Iterating when a count is enough.** The closed form is exact and linear in the input. Power iteration can take many steps when the second eigenvalue is near 1, and still gives only an approximation.
- **Mixing the two sides.** A page that is both a hub and an authority is two nodes of $\tilde G$. Merging them changes the components and the scores.
- **Forgetting the start.** The component weights $|A_c|/|A|$ come from the uniform start. A different start, or normalizing each component on its own, gives other scores for pages in different components.
- **Repeated links and self links.** If they are kept, the degrees and the components change. State the rule, and remove both as HITS implementations do.
- **Ties.** In-degrees are small integers, so many pages tie. Break ties by a fixed rule, here the smaller page number.

## Implementations

## History

Lempel and Moran presented SALSA at the Ninth International World Wide Web Conference (WWW9) in Amsterdam in 2000, under the title "The stochastic approach for link-structure analysis (SALSA) and the TKC effect", and published the full version in ACM Transactions on Information Systems in 2001. They designed it as a random walk version of Kleinberg's hubs and authorities. Their main analytic result is that the stationary distributions reduce to weighted degrees, scaled by the sizes of the components. Borodin, Roberts, Rosenthal and Tsaparas later placed SALSA among the link analysis ranking algorithms and compared it with HITS and in-degree ranking in theory and experiments.

## References
