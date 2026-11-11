---
tag: 5XDG91
kind: concept
slug: grammar-based-compression
name: Grammar-based compression
aliases:
- grammar compression
- grammar-based code
area: compression-and-coding/dictionary-compression
level: advanced
summary: Compress a string by storing a small grammar that generates it.
prereqs: [straight-line-program-grammar, context-free-grammar]
see_also: [smallest-grammar-problem, re-pair, sequitur, byte-pair-encoding, lz78, lempel-ziv-factorization, dictionary-based-compression, compressed-indexing]
sources:
  - paper: doi:10.1109/TIT.2005.850116
    title: Moses Charikar, Eric Lehman, Ding Liu, Rina Panigrahy, Manoj Prabhakaran, Amit Sahai and abhi shelat, The smallest grammar problem, IEEE Transactions on Information Theory 51(7), 2005, pages 2554 to 2576
    locator: Sections I and II (the model and the size measure), Section VI (LZ78, Bisection, Sequential, Sequitur, Re-Pair and others analyzed as grammar compressors), Section VII-D (LZ77 and grammars)
  - paper: doi:10.1109/18.841160
    title: John C. Kieffer and En-hui Yang, Grammar-based codes, a new class of universal lossless source codes, IEEE Transactions on Information Theory 46(3), 2000, pages 737 to 754
    locator: the definition of a grammar-based code as a grammar transform followed by an encoding of the grammar, the reduction rules, and the universality of codes built on irreducible grammars for stationary ergodic sources
  - paper: doi:10.1515/gcc-2012-0016
    title: Markus Lohrey, Algorithmics on SLP-compressed strings, a survey, Groups Complexity Cryptology 4(2), 2012, pages 241 to 299
    locator: the algorithms that work on the grammar without decompression (equality, pattern matching, membership)
  - paper: doi:10.1016/S0304-3975(02)00777-6
    title: Wojciech Rytter, Application of Lempel-Ziv factorization to the approximation of grammar-based compression, Theoretical Computer Science 302(1-3), 2003, pages 211 to 222
    locator: the relation between the LZ77 factorization and the smallest grammar, and the AVL grammars
---

Grammar-based compression stores a string as a small [straight-line program](/straight-line-program-grammar/) (SLP), a [context-free grammar](/context-free-grammar/) that generates that one string and nothing else. Each nonterminal names a substring that repeats, and its rule says how to build it from shorter parts. Algorithms such as [Re-Pair](/re-pair/) and [Sequitur](/sequitur/) build the grammar, and a second stage writes the grammar to bits. The approach is a form of [dictionary-based compression](/dictionary-based-compression/) whose dictionary is hierarchical, and it lets many algorithms run on the compressed text without expanding it.

## In plain words

A text that repeats itself can be described by its parts. Instead of writing a long phrase each time it appears, you give it a short name once, and then you write the name. A name can also be used inside the definition of another name. So you get a small set of rules that tell how to rebuild the text, like a recipe with sub-recipes.

To get the text back, you start from the main rule and replace each name by its definition until only plain letters remain. A good set of rules is much shorter than the text when the text repeats a lot. The rules also show the structure of the text, and some searches can run on the rules without rebuilding the whole text.

## The idea

**The object.** The input is a string $w$ of length $n$ over an alphabet $\Sigma$ of size $\sigma$. A grammar compressor produces an SLP $G$ with $\mathrm{val}(G) = w$. Its size $|G|$ is the total length of the right-hand sides of the rules. The analysis is in the worst case: there is no probability model on $w$, and the question is how $|G|$ compares with the smallest possible size $g^{*}(w)$, the optimum of the [smallest grammar problem](/smallest-grammar-problem/).

**Two stages.** Kieffer and Yang (2000) define a *grammar-based code* in two steps. A *grammar transform* maps $w$ to a grammar $G$. Then an encoder writes $G$ as a sequence of bits, for example with [arithmetic coding](/arithmetic-coding/) of the symbols of the right-hand sides. A grammar of size $g$ has at most $g$ distinct nonterminals, so a plain encoding takes $O(g \log n)$ bits when $\sigma \le n$. Kieffer and Yang show that if the transform always gives an *irreducible* grammar (no repeated pair of adjacent symbols, each rule used at least twice, distinct rules derive distinct strings), and the encoder is chosen well, the code is universal for the class of stationary ergodic sources. That result uses a probability model; the rest of this page does not.

**Why size can be very small.** A grammar can describe a string of exponential length. The rules $X_1 \to a$ and $X_i \to X_{i-1} X_{i-1}$ derive $a^{2^{m-1}}$ with $m$ rules. In the other direction, each grammar for $w$ has size $\Omega(\log n)$, and a string with no repeated substring of length 2 needs size $n$.

**How it compares with LZ77.** Let $z$ be the number of phrases of the greedy [Lempel-Ziv factorization](/lempel-ziv-factorization/) of $w$, in the variant in which a phrase may not overlap its source. Each grammar for $w$ has size at least $z$ (Charikar et al. 2005, Lemma 9 in Section VII-D), and Rytter (2003) turns the factorization into a grammar of size $O(z \log n)$. So the best grammar and the best LZ77 parse are within a factor of $O(\log n)$ of each other, and LZ77 is never worse. Grammars pay for this with a more rigid structure, and gain the ability to compute on the compressed form.

**The algorithms.** Finding a smallest grammar is NP-hard ([hardness theorem](/smallest-grammar-np-hardness/)), so practical compressors are heuristics or approximation algorithms:

- *Off-line, by pairs.* [Re-Pair](/re-pair/) replaces the most frequent pair of adjacent symbols by a new nonterminal, again and again. [Byte-pair encoding](/byte-pair-encoding/) does the same inside a byte budget.
- *On-line.* [Sequitur](/sequitur/) reads the string from left to right and keeps two invariants, digram uniqueness and rule utility. The phrases of [LZ78](/lz78/) also form a grammar: phrase $k$ is a rule $X_k \to X_j a$ that extends an earlier phrase $X_j$ by one symbol.
- *Approximation.* Charikar et al. (2005) and Rytter (2003) give algorithms whose output is within a factor $O(\log n)$ of $g^{*}$; the algorithm of Charikar et al. is within $O(\log(n/g^{*}))$.

## Examples

**LZ78 as a grammar.** The LZ78 parse of $w$ = aababcabcd is a | ab | abc | abcd. Each phrase is an earlier phrase plus one symbol, so the parse is the grammar

$$X_1 \to a, \quad X_2 \to X_1 b, \quad X_3 \to X_2 c, \quad X_4 \to X_3 d, \quad S \to X_1 X_2 X_3 X_4.$$

Its size is $1 + 2 + 2 + 2 + 4 = 11$, for a string of length 10. Every LZ78 grammar has this shape: rules of length 2 that grow one symbol at a time, so a phrase of length $\ell$ costs $\ell$ rules on its way up. This is why LZ78 can be far from the smallest grammar, with ratio $\Theta((n / \log n)^{2/3})$ in the worst case (see the [smallest grammar problem](/smallest-grammar-problem/)).

**Re-Pair on a short string.** On $w$ = xabcabcyabcabc ($n = 14$), Re-Pair creates $A \to ab$, then $B \to Ac$, then $C \to BB$, and the start rule becomes $S \to xCyC$. The size is $2 + 2 + 2 + 4 = 10$. The rule $C$ shows the hierarchy: abcabc is built from abc, which is built from ab.

**Fibonacci words.** The Fibonacci word of length 1597 has an SLP with 17 rules, one for each Fibonacci number. On this input, in the test code of the [Re-Pair](/re-pair/) and Sequitur pages, Re-Pair finds 13 rules and a final sequence of 3 symbols, for a size of $2 \cdot 13 + 3 = 29$, and [Sequitur](/sequitur/) finds a grammar of size 35. Both sizes are $O(\log n)$ here, while a plain encoding needs $n$ symbols.

**A string with no gain.** The string abcdefgh has no repeated pair, so the only grammar is $S \to$ abcdefgh, of size 8. Random text over a large alphabet behaves like this, and a grammar compressor then gives no gain before the entropy coding stage.

## Where it is used

- **Computing on compressed text.** Equality of two compressed strings, [pattern matching in compressed text](/pattern-matching-in-compressed-text/), random access and membership in a regular language can be solved in time polynomial in the grammar size (Lohrey's survey). This is useful when the text is too large to expand.
- **Indexes for repetitive collections.** Collections of genomes of one species, version histories and similar data are highly repetitive. Grammar-based [compressed indexes](/compressed-indexing/) store them in space close to $|G|$ and still answer queries. Grammar size is one of the standard measures of repetitiveness, next to the LZ77 parse size and the size of a [string attractor](/string-attractor/).
- **Structure discovery.** Nevill-Manning and Witten used Sequitur to show the phrase structure of text, music and DNA. The rules of a small grammar are candidates for words, motifs or phrases.
- **Tokenization.** The merges of [byte-pair encoding](/byte-pair-encoding/) define the subword vocabulary of many neural language models. The goal there is a vocabulary of fixed size, not the smallest grammar.
- **General-purpose compressors.** Grammar compressors are not the common choice for general files, where LZ77 compressors such as [DEFLATE](/deflate/) and [Zstandard](/zstandard/) dominate. Their place is highly repetitive data and data that must stay searchable.

## References
