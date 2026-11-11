---
tag: SCFQ76
kind: problem
slug: smallest-grammar-problem
name: Smallest grammar problem
aliases:
- minimal grammar problem
- smallest SLP problem
area: compression-and-coding/dictionary-compression
level: advanced
summary: Find the smallest context-free grammar that generates exactly one given string.
prereqs: [grammar-based-compression, straight-line-program-grammar]
see_also: [smallest-grammar-np-hardness, re-pair, sequitur, byte-pair-encoding, lempel-ziv-factorization, addition-chain, approximation-ratio, kolmogorov-complexity]
sources:
  - paper: doi:10.1109/TIT.2005.850116
    title: Moses Charikar, Eric Lehman, Ding Liu, Rina Panigrahy, Manoj Prabhakaran, Amit Sahai and abhi shelat, The smallest grammar problem, IEEE Transactions on Information Theory 51(7), 2005, pages 2554 to 2576
    locator: Section III (the table of upper and lower bounds), Section V (hardness, Theorem 1 with the ratio 8569/8568 and Theorem 2 on addition chains), Section VI (analysis of LZ78, Bisection, Sequential, Sequitur, Longest Match, Greedy and Re-Pair), Section VII (the O(log(n/g*)) algorithm and the lemma that LZ77 is never larger than a grammar)
  - paper: doi:10.1109/TIT.2020.3038147
    title: Hideo Bannai, Momoko Hirayama, Danny Hucke, Shunsuke Inenaga, Artur Jeż, Markus Lohrey and Carl Philipp Reh, The smallest grammar problem revisited, IEEE Transactions on Information Theory 67(1), 2021, pages 317 to 328
    locator: the tight ratio of LZ78 and of Bisection, and the lower bound for Re-Pair (arXiv 1908.06428)
  - paper: doi:10.1016/S0304-3975(02)00777-6
    title: Wojciech Rytter, Application of Lempel-Ziv factorization to the approximation of grammar-based compression, Theoretical Computer Science 302(1-3), 2003, pages 211 to 222
    locator: the AVL grammar algorithm with ratio O(log n), and the bound of the LZ77 factorization by the grammar size; preliminary version CPM 2002
  - paper: doi:10.1016/j.tcs.2015.05.027
    title: Artur Jeż, Approximation of grammar-based compression via recompression, Theoretical Computer Science 592, 2015, pages 115 to 134
    locator: the linear-time algorithm with output size O(g* log(n/g*)); conference version CPM 2013
  - paper: doi:10.4230/LIPIcs.ICALP.2016.122
    title: Katrin Casel, Henning Fernau, Serge Gaspers, Benjamin Gras and Markus L. Schmid, On the complexity of grammar-based compression over fixed alphabets, ICALP 2016, LIPIcs 55, Article 122
    locator: NP-completeness for fixed alphabets, the 1-level variant, the exact exponential algorithm, and the case of a bounded number of nonterminals; journal version Theory of Computing Systems 65(2), 2021
---

The smallest grammar problem asks for the smallest [straight-line program](/straight-line-program-grammar/) (SLP), a context-free grammar that generates exactly one given string. It is the optimization problem behind [grammar-based compression](/grammar-based-compression/): each grammar compressor, such as [Re-Pair](/re-pair/) or [Sequitur](/sequitur/), is a heuristic or an approximation algorithm for it. The problem is NP-hard ([hardness theorem](/smallest-grammar-np-hardness/)), the best known polynomial-time [approximation ratio](/approximation-ratio/) is $O(\log(n/g^{*}))$, and no algorithm can reach a ratio below $8569/8568$ unless P = NP.

## In plain words

You have a long text and you want to describe it with a set of rules. Each rule gives a short name to a piece of text, built from letters and from other names. One rule, the main one, spells the whole text. The cost of a set of rules is the total number of letters and names that you write on the right of all rules.

The question is: what is the cheapest set of rules for this one text? You must choose which repeated pieces get names, and how to build each piece from the others. These choices interact, so a greedy choice can be wrong. No fast exact method is known, and there is strong evidence that none exists. Fast methods exist that are never more than a modest factor away from the best.

## Definition

**Input.** A string $w \in \Sigma^{+}$ of length $n$ over an alphabet $\Sigma$ of size $\sigma$.

**Output.** An SLP $G$ with $\mathrm{val}(G) = w$, of minimum **size** $|G|$, the total length of the right-hand sides of all rules. Write $g^{*}(w)$ for this minimum. This is the size measure of Charikar et al. (2005). Some papers count the rules of an SLP in Chomsky normal form instead; the two measures differ by at most a factor of 2 plus $\sigma$ (see the [SLP page](/straight-line-program-grammar/)), so ratios of the form $O(f(n))$ do not change, but constants such as $8569/8568$ do.

**Decision version.** Given $w$ and an integer $k$, is $g^{*}(w) \le k$? It is in NP: a grammar of size at most $k \le n$ is a certificate. To check it, compute the length of each nonterminal bottom-up, stop with "no" when a length exceeds $n$, and else expand the grammar and compare with $w$. This takes time polynomial in $n$.

**Approximation ratio.** An algorithm $A$ has ratio $\rho(n)$ if $|A(w)| \le \rho(n) \cdot g^{*}(w)$ for each string $w$ of length $n$. All bounds below are in the worst case, with no probability model on $w$.

## Variants

- **Rule count in Chomsky normal form.** Minimize the number of rules of a CNF SLP. Many algorithmic papers use this measure.
- **Fixed alphabet.** The alphabet size is a constant. Charikar et al. prove hardness with an alphabet that grows with the input. Casel et al. (2016) prove NP-completeness for each fixed alphabet with at least 24 symbols.
- **1-level grammars.** All rules except the start rule contain only terminals. Casel et al. prove this variant NP-complete already for an alphabet of 5 symbols.
- **Bounded number of nonterminals.** If the number of nonterminals is bounded by a constant, Casel et al. solve the problem in polynomial time.
- **Run-length SLPs and macro schemes.** Allow rules $X \to Y^{k}$, or allow pointers into the text in the style of Storer and Szymanski. These models can be smaller than any SLP. The [LZ77 factorization](/lempel-ziv-factorization/) is a macro scheme of this kind.

## Examples

The values of $g^{*}$ below come from an exact search: the expansions of the rules of a smallest grammar can be chosen distinct, and each one occurs at least twice in $w$, so the search tries each set of repeated substrings as the set of expansions and parses optimally with it. The column $z$ is the number of phrases of greedy LZ77 in which a phrase may not overlap its source, and $z'$ allows the overlap.

| $w$ | $n$ | $g^{*}$ | a smallest grammar | Re-Pair | Sequitur | $z$ | $z'$ |
|---|---|---|---|---|---|---|---|
| abcabcabcabc | 12 | 7 | $A \to abc$, $S \to AAAA$ | 8 | 7 | 5 | 4 |
| xabcabcyabcabc | 14 | 9 | $A \to abc$, $S \to xAAyAA$ | 10 | 9 | 7 | 7 |
| 0001100011 | 10 | 7 | $A \to 00011$, $S \to AA$ | 10 | 10 | 6 | 5 |
| aaaaaaaa | 8 | 6 | $A \to aa$, $B \to AA$, $S \to BB$ | 6 | 6 | 4 | 2 |

The string 0001100011 shows why pair-based methods can lose. Re-Pair builds 00011 from four rules of length 2, at a cost of 8, and then writes $S \to WW$. The smallest grammar writes 00011 in one rule of length 5. Among all binary strings of length at most 11, the largest ratio of Re-Pair to $g^{*}$, and also of Sequitur to $g^{*}$, is $10/7$, reached at this string.

**Addition chains.** Charikar et al. give the string $x^{9} \mid x^{23}$, where $\mid$ is a symbol that occurs once. Its smallest grammar has size 13: $S \to A \mid A A B x x$, $A \to BBB$, $B \to xxx$. The rules count the way to 9 and 23 by sums, which is an addition chain.

## Known algorithms

The table gives the approximation ratio of the classical grammar compressors as analyzed by Charikar et al. (2005), with the later tight bounds of Bannai et al. (2021).

| algorithm | upper bound | lower bound |
|---|---|---|
| LZ78 (and LZW) | $O((n/\log n)^{2/3})$ | $\Omega((n/\log n)^{2/3})$ (Bannai et al.) |
| Bisection | $O((n/\log n)^{1/2})$ | $\Omega((n/\log n)^{1/2})$ (Bannai et al.) |
| Sequential | $O((n/\log n)^{3/4})$ | $\Omega(n^{1/3})$ |
| Sequitur | | $\Omega(n^{1/3})$, from the bound for Sequential |
| Longest Match | $O((n/\log n)^{2/3})$ | $\Omega(\log \log n)$ |
| Greedy | $O((n/\log n)^{2/3})$ | $1.37\ldots$ |
| Re-Pair | $O((n/\log n)^{2/3})$ | $\Omega(\log n / \log \log n)$ (Bannai et al.), before that $\Omega(\sqrt{\log n})$ |

Charikar et al. also show that every *irreducible* grammar (no repeated pair of adjacent symbols, each nonterminal used at least twice, distinct nonterminals with distinct expansions) has size within $O((n/\log n)^{3/4})$ of $g^{*}$. Their Re-Pair differs in a detail from the original of Larsson and Moffat, so the bounds in the table are for their version.

Algorithms with a logarithmic ratio:

- **Charikar et al. (2005).** Ratio $O(\log(n/g^{*}))$, by building a balanced grammar from an LZ77 factorization.
- **Rytter (2003).** AVL grammars, built from an LZ77 factorization with $z$ phrases, of size $O(z \log n)$, so the ratio is $O(\log n)$. The time is $O(n \log \sigma)$.
- **Jeż (2015).** Recompression, which needs no LZ77 factorization, gives size $O(g^{*} \log(n/g^{*}))$ in linear time.

**Exact algorithms.** The search used for the table above is exponential. Casel et al. give an exact algorithm in $O(3^{n})$ time up to a polynomial factor. No polynomial-time algorithm is known, and none exists unless P = NP.

## Bounds

- **Lower bound by LZ77.** For each $w$, $z \le g^{*}(w)$, where $z$ is the number of phrases of the greedy LZ77 parse without self-reference (Charikar et al., Lemma 9 in Section VII-D; also Rytter 2003). The proof turns a grammar into a parse: the first occurrence of each nonterminal is expanded, and each later occurrence becomes one copy phrase. The bound fails for LZ77 with overlapping copies: $a^{n}$ has $z' = 2$, but $g^{*}(a^{n}) = \Omega(\log n)$.
- **Upper bound by LZ77.** $g^{*}(w) = O(z \log n)$ by Rytter's construction.
- **Absolute bounds.** $g^{*}(w) = \Omega(\log n)$ for each $w$ (Charikar et al., Lemma 1), and $g^{*}(w) \le n$. A grammar of size $m$ has at most $m k$ distinct substrings of length $k$ (Charikar et al.); this gives lower bounds on $g^{*}$ for strings with many distinct substrings.
- **Hardness of approximation.** No polynomial-time algorithm has ratio below $8569/8568$ unless P = NP ([hardness theorem](/smallest-grammar-np-hardness/)). An algorithm with ratio $o(\log n / \log \log n)$ would improve the best known approximation for addition chains, which has stood since Yao (1976).
- **The gap.** The best ratio lies somewhere between the constant $8569/8568$ and $O(\log(n/g^{*}))$. It is open whether a constant-factor approximation exists.

## Reductions

- **From vertex cover.** Charikar et al. map a graph $H$ of maximum degree 3 to a string whose smallest grammar has size $15|V| + 3|E| + \tau(H)$, where $\tau(H)$ is the minimum [vertex cover](/vertex-cover/) size. This gives NP-hardness and the constant $8569/8568$. The full reduction is on the [hardness page](/smallest-grammar-np-hardness/).
- **From addition chains.** For a set $T = \{k_1, \ldots, k_p\}$ of distinct positive integers, let $\sigma_T = x^{k_1} \mid x^{k_2} \mid \cdots \mid x^{k_p}$ with distinct separators. If $\ell^{*}$ is the length of the shortest [addition chain](/addition-chain/) that contains $T$, then $\ell^{*} \le g^{*}(\sigma_T) \le 4 \ell^{*}$ (Charikar et al., Theorem 2).
- **To and from LZ77.** The two bounds above make LZ77 and the smallest grammar equivalent up to a factor $O(\log n)$. All algorithms with a logarithmic ratio except Jeż's use this link.

## Applications

The value $g^{*}(w)$ is a measure of how repetitive $w$ is. Unlike [Kolmogorov complexity](/kolmogorov-complexity/), it is computable, and it is approximable within a logarithmic factor. Many algorithms on compressed text run in time polynomial in the grammar size, so a smaller grammar makes them faster. Grammar compressors for highly repetitive data and the indexes built on them aim at a grammar close to $g^{*}$. In linguistics, de Marcken and others asked whether the rules of a smallest grammar for English text match the words and phrases of the language (Charikar et al., Section I).

## References
