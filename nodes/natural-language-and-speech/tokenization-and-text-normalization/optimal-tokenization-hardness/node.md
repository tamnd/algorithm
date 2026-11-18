---
tag: 81MQ79
kind: theorem
slug: optimal-tokenization-hardness
name: NP-hardness of optimal tokenization
aliases:
- tokenisation is NP-complete
- optimal BPE hardness
area: natural-language-and-speech/tokenization-and-text-normalization
level: research
summary: "Deciding whether K new pieces or K merges can shrink a corpus to a given number of tokens is NP-complete, so the optimization is NP-hard and greedy BPE is a heuristic."
prereqs: [subword-tokenization, byte-pair-encoding, np-complete, max-2-sat]
see_also: [np-hard, polynomial-time-reduction, apx, approximation-ratio, greedy-algorithm, unigram-language-model-tokenization, wordpiece, smallest-grammar-problem]
sources:
  - paper: doi:10.18653/v1/2025.acl-long.1365
    title: Philip Whittington, Gregor Bachmann and Tiago Pimentel, Tokenisation is NP-complete, ACL 2025 (long papers), pages 28133 to 28153, arXiv 2412.15210
    locator: Definition 1 (max-2-SAT), Definitions 2 to 5 (the direct and bottom-up problems), Theorem 1 with Lemmas 1 to 4 and Reduction 1 (Section 5.2), Theorem 2 with Lemmas 5 to 8 (Section 6.2), footnote 2 (Kozma and Voderholzer)
  - paper: arxiv:2411.08671
    title: László Kozma and Johannes Voderholzer, Theoretical analysis of byte-pair encoding, arXiv 2411.08671, 2024 (preprint)
    locator: the abstract (APX-completeness of the pair encoding problem and the bounds on the approximation factor of BPE)
  - paper: arxiv:2511.15709
    title: Violeta Kastreva, Philip Whittington, Dennis Komm and Tiago Pimentel, Tokenisation over bounded alphabets is hard, arXiv 2511.15709, 2025 (preprint)
    locator: the abstract (binary and unary alphabets)
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: "Michael R. Garey, David S. Johnson and Larry Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1 (1976), 237 to 267"
    locator: the NP-completeness of max-2-SAT
  - paper: doi:10.18653/v1/P16-1162
    title: Rico Sennrich, Barry Haddow and Alexandra Birch, Neural machine translation of rare words with subword units, ACL 2016
    locator: the section on byte pair encoding (the greedy merge learning algorithm)
---

## Statement

Let $\Sigma$ be a finite alphabet and let $D$ be a data set: a finite multiset of strings over $\Sigma$. Let $N$ be the total number of characters in $D$. A piece is a string over $\Sigma$ of length at least 2.

*Direct tokenization.* A vocabulary is $S = \Sigma \cup P$ for a set $P$ of $K$ pieces, so $|S| = |\Sigma| + K$. Each string $x$ of $D$ is tokenized by a shortest sequence of members of $S$ whose concatenation is $x$, and the cost of $S$ is the sum of these lengths over $D$, with multiplicity. The decision problem asks: given $D$, $K$ and $\delta$, is there a vocabulary with $K$ pieces and cost at most $\delta$?

*Bottom-up tokenization.* A merge is a pair $\langle s_1, s_2 \rangle$ of tokens. Applying it to a token sequence replaces, from left to right, every occurrence of $s_1$ followed by $s_2$ with the single token $s_1 s_2$. Each string of $D$ starts as its sequence of characters, and the merges of a sequence $m = (m_1, \ldots, m_K)$ are applied in order. The cost of $m$ is the total number of tokens left in $D$. The decision problem asks: given $D$, $K$ and $\delta$, is there a merge sequence of length $K$ with cost at most $\delta$?

**Theorem 1** (Whittington, Bachmann and Pimentel 2025, Theorem 1). The direct tokenization decision problem is NP-complete.

**Theorem 2** (Whittington, Bachmann and Pimentel 2025, Theorem 2). The bottom-up tokenization decision problem is NP-complete.

**Corollary.** The optimization versions (find a vocabulary, or a merge sequence, of minimum cost) are NP-hard: an algorithm for either one answers the decision problem by comparing the minimum cost with $\delta$.

The hypotheses matter. In both proofs the alphabet grows with the input: its size is $2J + 1$ (direct) or $2J + 2$ (bottom-up) for a [max-2-SAT](/max-2-sat/) instance with $J$ variables. The theorems say nothing about a fixed alphabet such as the 256 bytes; Kastreva et al. treat that case (see Tightness).

## In plain words

A tokenizer gets a budget: it may add a fixed number of new pieces to its alphabet, or a fixed number of merge steps. The aim is to write a text with as few tokens as possible. The theorem says that this aim is as hard as the hardest search problems that can be checked quickly. If someone hands you a vocabulary, you can count its tokens fast. But to find the best vocabulary, no fast method is known, and one would give fast methods for thousands of other hard problems.

So byte-pair encoding, which always merges the most frequent pair next, is a quick rule of thumb. It can miss the best answer even on a tiny text, as the example below shows.

## Proof

The proof has two parts for each theorem: the problem is in NP, and [max-2-SAT](/max-2-sat/) reduces to it. Max-2-SAT asks, for a set of $I$ clauses with two literals each over $J$ variables and a number $\psi$, whether some assignment satisfies at least $\psi$ clauses. Garey, Johnson and Stockmeyer (1976) proved it [NP-complete](/np-complete/).

**Membership in NP** (Lemmas 1 and 5 of the source). A piece that is not a substring of a string in $D$ is never used, and $D$ has fewer than $N^2$ distinct substrings. So a certificate only needs to list the useful pieces of a vocabulary, and if $K$ is at least the number of substrings the answer is found by taking them all. Likewise, a merge that applies nowhere changes nothing, and each useful merge removes at least one token, so at most $N$ merges matter. A certificate then has size polynomial in $N$. For a vocabulary, the cost of one string $x$ of length $n$ is a shortest path in its lattice. Positions are fenceposts $0, \ldots, n$, and $x[i{:}j]$ is the edge $i \to j$, present when $x[i{:}j] \in S$. The program $d[0] = 0$, $d[j] = \min_i (d[i] + 1)$ over the edges into $j$ runs in the TROPICAL semiring (min, +). It takes $O(n^2)$ substring tests per string, each $O(n)$ time with a hash set, so the check is polynomial. For a merge sequence, apply the $K$ merges in order; each pass is linear in the current length.

**Hardness of direct tokenization** (Reduction 1 and Lemmas 2 to 4 of the source). Given a max-2-SAT instance, use a separator symbol $\circledcirc$ and, for each variable $X_j$, two symbols $x_j^T$ and $x_j^F$. A literal $X_j$ becomes $x_j^T$ and a literal $\neg X_j$ becomes $x_j^F$. The data set has three parts:

- $D_1$: the strings $\circledcirc x_j^T \circledcirc$ and $\circledcirc x_j^F \circledcirc$ for each $j$, each $f$ times;
- $D_2$: the string $\circledcirc x_j^T \circledcirc x_j^F \circledcirc$ for each $j$, $f'$ times;
- $D_3$: the string $\circledcirc L_1 \circledcirc L_2 \circledcirc$ once for each clause $(L_1 \lor L_2)$.

Set $K = J$, $f' = 4I + 1$, $f = 4f'J + 4I + 1$ and $\delta = (4f + 3f')J + 5I - 2\psi$. If an assignment satisfies at least $\psi$ clauses, take the piece $\circledcirc x_j^T \circledcirc$ when $X_j$ is true and $\circledcirc x_j^F \circledcirc$ when it is false. Each pair in $D_1$ then costs $1 + 3$ tokens, each string in $D_2$ costs 3, and a clause string costs 3 if one of its literals is true and 5 if not. The total is at most $(4f + 3f')J + 3\psi + 5(I - \psi) = \delta$. For the converse, the large weights $f$ and $f'$ force an optimal vocabulary to spend its $J$ pieces on exactly one of $\circledcirc x_j^T \circledcirc$ and $\circledcirc x_j^F \circledcirc$ for each $j$: any other choice loses more on $D_1$ or $D_2$ than all of $D_3$ can gain. Such a vocabulary is an assignment, and a cost of at most $\delta$ means that at least $\psi$ clause strings cost 3, so at least $\psi$ clauses are satisfied. The source gives this step in full in its appendix (the proof of Lemma 3). The construction has polynomial size, which proves Theorem 1.

**Hardness of bottom-up tokenization** (Lemmas 6 to 8 of the source). The reduction follows the same plan with a second separator symbol, five families of strings and $K = 8J$ merges, so that the merges chosen for each variable encode its value. Membership and this reduction prove Theorem 2.

**A check of Reduction 1 (measurement by script).** For $J = 2$ and the four clauses $(X_1 \lor X_2)$, $(\neg X_1 \lor X_2)$, $(X_1 \lor \neg X_2)$ and $(\neg X_1 \lor \neg X_2)$, at most $\psi = 3$ clauses can be satisfied. Then $f' = 17$, $f = 153$, and the data set has 2,026 characters. An exhaustive search over all vocabularies of two pieces finds the minimum cost 1,340, which is exactly $\delta$ for $\psi = 3$ and more than $\delta = 1{,}338$ for $\psi = 4$. The best vocabulary is $\{\circledcirc x_1^T \circledcirc, \circledcirc x_2^T \circledcirc\}$, the assignment with both variables true.

## Consequences

- **Greedy BPE is not optimal (theorem, by example).** Take $D$ = "abc" twice, "cbcb" three times and "bcb" twice, 24 characters, and $K = 2$. [BPE](/byte-pair-encoding/) first counts the pairs, without overlaps: cb occurs 8 times, bc 7 times and ab 2 times, so it merges c + b (16 tokens left), then cb + cb (13 tokens: a b c, cbcb, b cb). The merges b + c, then bc + b give a bc, c bcb and bcb, so 12 tokens. An exhaustive search confirms that 12 is the best for bottom-up tokenization with 2 merges. The best direct vocabulary of 2 pieces, {abc, bcb}, gives 10 tokens, because its pieces need not be built from earlier merges. No step of greedy BPE has a tie here. The source gives no such example; this one was found and checked by a script.
- **The builders are heuristics.** Unless P = NP, no polynomial-time algorithm finds an optimal vocabulary or merge sequence in general. [BPE](/byte-pair-encoding/), [WordPiece](/wordpiece/) and the [unigram language model](/unigram-language-model-tokenization/) give good tokenizers in practice, but none of them is optimal for these objectives.
- **Approximation.** The theorems give no approximation ratio. Kozma and Voderholzer (2024) measure the compression utility (how much a pair encoding shortens the input) and show that maximizing it is [APX](/apx/)-complete, so a polynomial-time approximation scheme is unlikely. They also show that the worst-case [approximation ratio](/approximation-ratio/) of BPE for this utility is between 1/3 and about 0.4324.
- **The objective is one of many.** The theorems concern the number of tokens. A tokenizer is also judged by the quality of the model trained on it, which these results do not cover.

## Tightness

- **One merge is easy (theorem).** For $K = 1$, the cost of a merge $\langle a, b \rangle$ is $N$ minus the number of left-to-right replacements it makes, so the best single merge is the pair with the highest count without overlaps. That is the first step of greedy BPE when it counts pairs in this way.
- **A fixed budget is polynomial (theorem).** For a constant $K$, the bottom-up problem has at most $N^K$ merge sequences to try, since each step has at most $N$ adjacent token pairs, and each try is checked in polynomial time. The direct problem has at most $\binom{N^2}{K}$ vocabularies built from substrings. So the hardness needs $K$ to be part of the input.
- **Bounded alphabets.** The reductions above use an alphabet that grows with $J$. Kastreva, Whittington, Komm and Pimentel (2025) prove that both problems stay NP-complete over a binary alphabet, and are APX-hard there, and that direct tokenization is NP-complete even over a unary alphabet.
- **Other objectives.** The source notes that similar results for other objective functions remain open.

## History

Byte-pair encoding began as a compression method (Gage 1994), and Sennrich, Haddow and Birch (2016) used its greedy merges to build subword vocabularies for translation. In 2024, two groups gave hardness proofs at about the same time: Whittington, Bachmann and Pimentel (arXiv 2412.15210, published at ACL 2025) proved both the direct and the bottom-up decision problems NP-complete by reductions from max-2-SAT, and Kozma and Voderholzer (arXiv 2411.08671) independently proved hardness for the bottom-up case and studied how well BPE approximates the optimum. Kastreva et al. (2025) removed the need for a growing alphabet.

## References

- Philip Whittington, Gregor Bachmann and Tiago Pimentel. Tokenisation is NP-complete. Proceedings of ACL 2025 (long papers), pages 28133 to 28153. doi:10.18653/v1/2025.acl-long.1365. arXiv 2412.15210.
- László Kozma and Johannes Voderholzer. Theoretical analysis of byte-pair encoding. arXiv 2411.08671, 2024.
- Violeta Kastreva, Philip Whittington, Dennis Komm and Tiago Pimentel. Tokenisation over bounded alphabets is hard. arXiv 2511.15709, 2025.
- Michael R. Garey, David S. Johnson and Larry Stockmeyer. Some simplified NP-complete graph problems. Theoretical Computer Science 1 (1976), 237 to 267. doi:10.1016/0304-3975(76)90059-1.
- Rico Sennrich, Barry Haddow and Alexandra Birch. Neural machine translation of rare words with subword units. ACL 2016. doi:10.18653/v1/P16-1162.
