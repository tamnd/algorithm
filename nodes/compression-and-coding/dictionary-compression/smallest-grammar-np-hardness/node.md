---
tag: 23VMPY
kind: theorem
slug: smallest-grammar-np-hardness
name: Hardness of the smallest grammar problem
aliases:
- grammar problem NP-hardness
- 8569/8568 inapproximability of the smallest grammar
area: compression-and-coding/dictionary-compression
level: advanced
summary: The smallest grammar problem is NP-hard, and no polynomial-time algorithm has approximation ratio below 8569/8568 unless P = NP.
prereqs: [smallest-grammar-problem, vertex-cover, np-hard, approximation-ratio]
see_also: [np-complete, vertex-cover-inapproximability, gap-preserving-reduction, l-reduction, addition-chain, straight-line-program-grammar, re-pair, polynomial-time-reduction]
sources:
  - paper: doi:10.1109/TIT.2005.850116
    title: Moses Charikar, Eric Lehman, Ding Liu, Rina Panigrahy, Manoj Prabhakaran, Amit Sahai and abhi shelat, The smallest grammar problem, IEEE Transactions on Information Theory 51(7), 2005, pages 2554 to 2576
    locator: Section V-A, Theorem 1 (the reduction from vertex cover on graphs of maximum degree 3 and the ratio 8569/8568); Section V-B, Theorem 2 (addition chains)
  - paper: doi:10.1145/322344.322346
    title: James A. Storer and Thomas G. Szymanski, Data compression via textual substitution, Journal of the ACM 29(4), 1982, pages 928 to 951
    locator: the NP-completeness results for macro schemes, on which the reduction of Charikar et al. is based
  - paper: "Piotr Berman and Marek Karpinski, On some tighter inapproximability results, further improvements, Technical Report TR98-065, Electronic Colloquium on Computational Complexity, 1998"
    locator: the bound 145/144 for vertex cover on graphs of maximum degree 3, as cited by Charikar et al.
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, a guide to the theory of NP-completeness, 1979
    locator: Appendix A1.1, problem GT1 (vertex cover, NP-complete also for graphs of maximum degree 3)
  - paper: doi:10.4230/LIPIcs.ICALP.2016.122
    title: Katrin Casel, Henning Fernau, Serge Gaspers, Benjamin Gras and Markus L. Schmid, On the complexity of grammar-based compression over fixed alphabets, ICALP 2016, LIPIcs 55, Article 122
    locator: NP-completeness for each fixed alphabet of at least 24 symbols, and for 1-level grammars over 5 symbols; journal version Theory of Computing Systems 65(2), 2021
---

The smallest grammar problem asks for the smallest [straight-line program](/straight-line-program-grammar/) that generates one given string. This theorem states that its decision version is [NP-complete](/np-complete/), and that no polynomial-time algorithm achieves an [approximation ratio](/approximation-ratio/) below $8569/8568$ unless P = NP. The proof is a reduction from [vertex cover](/vertex-cover/) on graphs of maximum degree 3, due to Charikar et al. (2005) and based on earlier arguments of Storer and Szymanski. It explains why grammar compressors such as [Re-Pair](/re-pair/) and [Sequitur](/sequitur/) are heuristics.

## Statement

The size $|G|$ of a grammar is the total length of the right-hand sides of its rules, and $g^{*}(w)$ is the smallest size of a straight-line program that derives the string $w$ of length $n$. The model is the worst case over all strings; the alphabet is part of the input.

**Theorem.**

1. The decision problem "given $w$ and $k$, is $g^{*}(w) \le k$?" is NP-complete.
2. Unless P = NP, no polynomial-time algorithm outputs, for each string $w$, a grammar for $w$ of size at most $\rho \cdot g^{*}(w)$ with a constant $\rho < 8569/8568$.

The core is an exact identity. For a simple graph $H = (V, E)$, let

$$\sigma_H = \prod_{v_i \in V} \big( \#v_i \mid v_i\# \mid \big)^{2} \;\prod_{v_i \in V} \big( \#v_i\# \mid \big) \;\prod_{(v_i, v_j) \in E} \big( \#v_i\#v_j\# \mid \big),$$

where each $\mid$ is a new symbol that occurs only once. Then

$$g^{*}(\sigma_H) = 15|V| + 3|E| + \tau(H),$$

where $\tau(H)$ is the size of a minimum vertex cover of $H$.

## In plain words

Take a network of points and links. Write a long text with one short piece for each point and one piece for each link, and put a unique marker between all pieces, so that no rule can reach across two pieces. A few pieces repeat, and the only real choice a compressor has is which points get their own rule for a three-letter piece.

Each such rule costs one extra symbol. Each link is cheap only when one of its two points has the rule. So the cheapest set of rules picks a smallest set of points that touches every link. That is the vertex cover problem, which is hard. A good compressor for this text would also give a good vertex cover, and vertex cover cannot be approximated too well, so neither can the compression.

## Proof

The full proof is in [the reduction from vertex cover](proofs/correctness.md). Its steps:

1. **Upper bound.** For a vertex cover $C$, use rules $A_i \to \#v_i$, $B_i \to v_i\#$, and $D_i \to A_i \#$ for $v_i \in C$. Write each edge block as $D_i B_j$ or $A_i D_j$. The size is $15|V| + 3|E| + |C|$.
2. **Normal form.** Any grammar can be changed, without growing, into one where each rule has length at least 2, each nonterminal is used at least twice, and expansions are distinct. Then each expansion occurs at least twice in $\sigma_H$ and contains no separator.
3. **The phrases.** The only strings of length at least 2 that occur twice and contain no separator are $\#v_i$, $v_i\#$ and $\#v_i\#$. A string that contains $v_i\#v_j$ occurs only in the block of that edge.
4. **Counting.** A rule for $\#v_i$ costs 2 and saves 2, and so does a rule for $v_i\#$. A rule for $\#v_i\#$ costs 1 net. An edge block costs 2 if one of its ends has that rule, and at least 3 otherwise. So each grammar has size at least $15|V| + 3|E| + |C| + u$, where $C$ is the set of vertices with a rule for $\#v_i\#$ and $u$ is the number of edges that $C$ misses. Adding one end of each missed edge gives a vertex cover of size at most $|C| + u$.
5. **NP-completeness.** Vertex cover is NP-complete on graphs of maximum degree 3 (Garey and Johnson, GT1), and the map $H \mapsto \sigma_H$ is a [polynomial-time reduction](/polynomial-time-reduction/). Membership in NP is on the [problem page](/smallest-grammar-problem/).
6. **The constant.** Berman and Karpinski show that vertex cover on graphs of maximum degree 3 has no polynomial-time approximation within $145/144$ unless P = NP. For such graphs with $|E| \ge |V|$, $15|V| + 3|E| \le 58.5\, \tau(H)$. A grammar within ratio $\rho$ then gives a cover within $1 + 59.5(\rho - 1)$, and this is below $145/144$ when $\rho < 1 + 1/8568$.

## Consequences

- **No exact polynomial algorithm.** Unless P = NP, each polynomial-time grammar compressor is a heuristic or an approximation algorithm. Re-Pair, Sequitur, LZ78 and [byte-pair encoding](/byte-pair-encoding/) all fall in this class.
- **Hardness does not depend on hierarchy.** The strings $\sigma_H$ have a large alphabet and only short repeats, so the smallest grammar has no deep nesting. Charikar et al. point out that the hardness comes from choosing phrases, not from building a hierarchy.
- **A second barrier.** By a different reduction (Charikar et al., Theorem 2), a grammar for $x^{k_1} \mid \cdots \mid x^{k_p}$ corresponds to an [addition chain](/addition-chain/) for $\{k_1, \ldots, k_p\}$ within a factor 4. So a ratio $o(\log n / \log \log n)$ for the smallest grammar would beat the best known method for addition chains, due to Yao (1976). This is not a proof of hardness, but it explains why no such ratio is known.
- **Approximation algorithms are near the limit of what is known.** The best ratio known is $O(\log(n / g^{*}))$, by Charikar et al. and by later algorithms (see the [problem page](/smallest-grammar-problem/)).

## Tightness

The constant $8569/8568$ is far from the best known upper bound $O(\log(n / g^{*}))$, and the true best ratio of a polynomial-time algorithm is unknown. The proof gives a small constant because the strings $\sigma_H$ are already almost incompressible: $g^{*}(\sigma_H) \ge 15|V|$, while the choice of a cover changes the size by at most $|V|$.

The reduction needs an alphabet whose size grows with the graph: one symbol per vertex and one separator per block. Casel et al. (2016) prove NP-completeness for each fixed alphabet of at least 24 symbols, and NP-completeness of the 1-level variant (only the start rule may contain nonterminals) over 5 symbols. Their results do not give a constant of inapproximability, and they do not cover alphabets with fewer than 24 symbols for the general problem.

The identity $g^{*}(\sigma_H) = 15|V| + 3|E| + \tau(H)$ holds for each simple graph. The degree bound and the condition $|E| \ge |V|$ are used only to compare $15|V| + 3|E|$ with $\tau(H)$ in the last step.

## History

Storer and Szymanski studied many "macro" compression schemes in the late 1970s, in Storer's Princeton PhD thesis (1978) and in their paper in the Journal of the ACM (1982), and proved most of them NP-hard. The smallest grammar problem, as an optimization problem with approximation ratios, was set out by Charikar, Lehman, Liu, Panigrahy, Prabhakaran, Sahai and shelat. Their paper appeared in 2005 and includes results first given by Lehman and Shelat (SODA 2002) and in Eric Lehman's MIT PhD thesis (2002). The constant $8569/8568$ and the addition chain link are from that work. Casel, Fernau, Gaspers, Gras and Schmid extended NP-completeness to fixed alphabets in 2016.

## References
