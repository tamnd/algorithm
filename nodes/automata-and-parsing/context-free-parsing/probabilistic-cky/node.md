---
tag: W4N6QS
kind: algorithm
slug: probabilistic-cky
name: Probabilistic CKY
aliases:
- Viterbi CKY
area: automata-and-parsing/context-free-parsing
level: advanced
summary: CYK variant computing the highest-probability parse of a string under a PCFG in cubic time.
solves: [most-probable-parse]
model: word-ram
complexity:
  vars: {n: the length of the input string, g: the number of productions of the grammar in Chomsky normal form, v: the number of nonterminals}
  time: {worst: Θ(n^3 g), best: Θ(n^3 g)}
  space: {extra: Θ(n^2 v)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1991
  people: [Hermann Ney]
  note: Ney described the maximum-probability version of the CYK table for speech recognition; Baker had used the sum version for inside probabilities in 1979.
prereqs: [cyk-algorithm, probabilistic-context-free-grammar]
see_also: [most-probable-parse, inside-outside-algorithm, chomsky-normal-form-conversion, parse-chart, earley-parser, viterbi-algorithm, shared-packed-parse-forest, optimal-substructure]
sources:
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft
    locator: Appendix E, Statistical Constituency Parsing, Section E.2, Probabilistic CKY Parsing of PCFGs (Figure E.3), and the historical notes
  - book: isbn:9780262133609
    title: Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999
    locator: Chapter 11, Probabilistic Context Free Grammars (inside probabilities and the most likely parse)
  - paper: "Hermann Ney, Dynamic programming parsing for context-free grammars in continuous speech recognition, IEEE Transactions on Signal Processing 39(2) (1991)"
    title: Hermann Ney, Dynamic programming parsing for context-free grammars in continuous speech recognition
    locator: pp. 336 to 340
  - paper: "James K. Baker, Trainable grammars for speech recognition, Speech Communication Papers for the 97th Meeting of the Acoustical Society of America (1979)"
    title: James K. Baker, Trainable grammars for speech recognition
    locator: the inside computation on a CYK-style table
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 4.2, The CYK Parsing Method, and the discussion of probabilistic grammars in Chapter 4
---

Probabilistic CKY, also called Viterbi CKY, finds the [most probable parse](/most-probable-parse/) of a string under a [probabilistic context-free grammar](/probabilistic-context-free-grammar/) in [Chomsky normal form](/chomsky-normal-form/). It is the [CYK algorithm](/cyk-algorithm/) with a number in place of each yes or no: for every substring and every nonterminal, the table holds the largest probability of a tree with that root and that yield, computed from the two shorter pieces by a product and a maximum. A back pointer per entry recovers the best tree. It takes $\Theta(n^3 g)$ time for an input of length $n$ and a grammar of $g$ productions, like CYK. Ney described it for speech recognition in 1991; it is the base of most statistical constituency parsers, and replacing the maximum by a sum gives the inside probabilities of the [inside-outside algorithm](/inside-outside-algorithm/).

## In plain words

An ambiguous grammar can read one sentence in several ways. A probabilistic grammar puts a probability on each rule, and a reading gets the product of the probabilities of its rules. The task is to find the most probable reading without listing all readings, whose number can grow very fast.

The method fills the same triangular table as CYK. For each piece of the sentence and each placeholder, it stores the best probability of building that piece from that placeholder, and which split and which rule gave it. A short piece is filled from the rules for single words. A longer piece tries every split and every two-placeholder rule, multiplies the rule probability by the two stored best values, and keeps the largest. The best reading of a piece always uses the best readings of its two halves, so nothing is lost by keeping one number per entry.

## The problem

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. A production with probability $q$ is written $A \to \alpha\ [q]$.

The input is a probabilistic grammar $G = (V, \Sigma, P, S, q)$ in Chomsky normal form, so every production is $A \to BC$ with $B, C \in V$, $A \to a$ with $a \in \Sigma$, or $S \to \varepsilon$ when $S$ is on no right side, and a string $w = a_1 \cdots a_n$. Write $g = |P|$ and $v = |V|$. The probability $P(t)$ of a [parse tree](/parse-tree/) $t$ is the product of the probabilities of the productions at its nodes. The output is

$$\hat{t} = \operatorname{argmax}_{t \,:\, \mathrm{yield}(t) = w} P(t)$$

and its probability $P(\hat{t})$, or the answer that $w$ has no tree. Since $P(t \mid w) = P(t) / P(w)$ and $P(w)$ does not depend on $t$, $\hat{t}$ is also the tree of highest conditional probability given $w$. The algorithm uses only that the weights are nonnegative, not that they sum to 1, so it works for any weighted grammar with nonnegative weights.

## The algorithm

$\pi[i, j, A]$ is the largest probability of a tree with root $A$ and yield $a_i \cdots a_j$, and 0 when there is none. All entries start at 0.

```pseudo id=main
PROBABILISTIC-CKY(G, q, w)                  ▷ G in Chomsky normal form, w = a1 … an
L1  if n = 0 then return (q(S → ε), the tree S → ε) if S → ε ∈ P, else (0, no tree)
L2  for i ← 1 to n do
L3      for each A → a_i in P with q(A → a_i) > π[i, i, A] do π[i, i, A] ← q(A → a_i);  back[i, i, A] ← a_i
L4  for len ← 2 to n do                     ▷ length of the substring
L5      for i ← 1 to n − len + 1 do
L6          j ← i + len − 1
L7          for k ← i to j − 1 do            ▷ split a_i … a_k | a_{k+1} … a_j
L8              for each A → B C in P do
L9                  p ← q(A → B C) · π[i, k, B] · π[k + 1, j, C]
L10                 if p > π[i, j, A] then π[i, j, A] ← p;  back[i, j, A] ← (k, B, C)
L11 return π[1, n, S] and the tree built from back[1, n, S]
```

The line numbers match the [CYK algorithm](/cyk-algorithm/): line L9 replaces the test "$B \in T[i, k]$ and $C \in T[k + 1, j]$" by a product, and line L10 replaces "add $A$" by a running maximum. The loop of line L4 goes through the lengths in increasing order, so the two cells read by line L9 are final. The tree of line L11 is built as in CYK: the node $(i, j, A)$ with back pointer $(k, B, C)$ has the children $(i, k, B)$ and $(k + 1, j, C)$, and the node $(i, i, A)$ has the leaf $a_i$. The implementation walks it with an explicit stack, since the tree can be $n$ levels deep.

Line L1 handles the empty input: in Chomsky normal form only $S \to \varepsilon$ yields $\varepsilon$.

## Example

Take the grammar of Manning and Schütze from the [PCFG](/probabilistic-context-free-grammar/) page:

$$S \to NP\ VP\ [1.0], \quad PP \to P\ NP\ [1.0], \quad VP \to V\ NP\ [0.7] \mid VP\ PP\ [0.3], \quad NP \to NP\ PP\ [0.4],$$

$$P \to \text{with}\ [1.0], \quad V \to \text{saw}\ [1.0], \quad NP \to \text{astronomers}\ [0.1] \mid \text{ears}\ [0.18] \mid \text{saw}\ [0.04] \mid \text{stars}\ [0.18] \mid \text{telescopes}\ [0.1],$$

and $w$ = *astronomers saw stars with ears*, with $n = 5$. Row $\ell$ lists the nonzero entries $\pi[i, i + \ell - 1, \cdot]$ for $i = 1, \ldots, 6 - \ell$; a dash means all entries are 0. The values were computed with exact fractions by the implementation.

| length | $i = 1$ | $i = 2$ | $i = 3$ | $i = 4$ | $i = 5$ |
|---|---|---|---|---|---|
| 1 | $NP$ 0.1 | $V$ 1.0, $NP$ 0.04 | $NP$ 0.18 | $P$ 1.0 | $NP$ 0.18 |
| 2 | dash | $VP$ 0.126 | dash | $PP$ 0.18 | |
| 3 | $S$ 0.0126 | dash | $NP$ 0.01296 | | |
| 4 | dash | $VP$ 0.009072 | | | |
| 5 | $S$ 0.0009072 | | | | |

The cells where the maximum matters:

- $\pi[3, 5, NP]$, *stars with ears*: the split *stars* | *with ears* with $NP \to NP\ PP$ gives $0.4 \cdot 0.18 \cdot 0.18 = 0.01296$.
- $\pi[2, 5, VP]$, *saw stars with ears*, has two candidates. The split *saw* | *stars with ears* with $VP \to V\ NP$ gives $0.7 \cdot 1.0 \cdot 0.01296 = 0.009072$. The split *saw stars* | *with ears* with $VP \to VP\ PP$ gives $0.3 \cdot 0.126 \cdot 0.18 = 0.006804$. Line L10 keeps the first, with the back pointer $(2, V, NP)$. The second reading is gone from the table.
- $\pi[1, 5, S] = 1.0 \cdot 0.1 \cdot 0.009072 = 0.0009072$.

Following the back pointers gives the tree in which *with ears* modifies *stars*:

$$[_S\ [_{NP}\ \text{astronomers}]\ [_{VP}\ [_V\ \text{saw}]\ [_{NP}\ [_{NP}\ \text{stars}]\ [_{PP}\ [_P\ \text{with}]\ [_{NP}\ \text{ears}]]]]].$$

With sums instead of maxima, the same table gives $P(w) = 0.0009072 + 0.0006804 = 0.0015876$, so the best tree has conditional probability $4/7$. The loops of lines L8 to L10 run for $\binom{6}{3} = 20$ triples $(\text{len}, i, k)$.

## Correctness

The claim is that $\pi[i, j, A]$ ends as the largest probability $\mu(A, i, j)$ of a tree with root $A$ and yield $a_i \cdots a_j$. By the CYK structure lemma, such a tree is a production $A \to BC$ over a split $k$ with independent subtrees for $B$ over $a_i \cdots a_k$ and $C$ over $a_{k+1} \cdots a_j$, and its probability is $q(A \to BC)$ times the probabilities of the subtrees. Because the weights are nonnegative, the product grows with each factor, so for a fixed split and production the best choice is the best subtree on each side. This gives the recurrence

$$\mu(A, i, j) = \max_{i \le k < j}\ \max_{A \to BC}\ q(A \to BC) \cdot \mu(B, i, k) \cdot \mu(C, k + 1, j),$$

which lines L7 to L10 evaluate, by induction on the length, from cells that are already final. The back pointer is set by the term that gave the final maximum, so the tree built from it has exactly the probability $\mu$. The full proof, with the tree construction and the empty input, is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** As in CYK, lines L8 to L10 run once for each production and each of the $\binom{n + 1}{3} = (n + 1) n (n - 1) / 6$ triples $(\text{len}, i, k)$, and each run does two multiplications and a comparison. With $\pi$ stored as an array indexed by nonterminal, each run takes $O(1)$ time on the [word RAM](/word-ram/), with probabilities as floating-point numbers of fixed size. Lines L2 and L3 take $O(n g)$. So the time is $\Theta(n^3 g)$ in every case, since the loops do not depend on the values. Building the tree takes $O(n)$.

**Space.** The table has $n(n + 1)/2$ cells of $v$ entries and as many back pointers, so the space is $\Theta(n^2 v)$.

**Exact arithmetic.** With exact rationals, as in the tests, the numbers grow: a product of $2n - 1$ probabilities with $d$-digit denominators has about $(2n - 1) d$ digits, and the unit-cost assumption no longer holds. Floating-point numbers with logarithms are the practical choice.

## Properties

- **Deterministic.** Ties are broken by the order of the loops: line L10 keeps the first term that reaches the maximum.
- **Not online.** Like CYK, it needs the whole input before the long cells can be filled.
- **Exact, not approximate.** It returns a tree of maximum probability, not a heuristic one; pruning variants such as beam search give up this guarantee.
- **Semiring algorithm.** The same loops with (max, ·) give the best tree, with (+, ·) the inside probability $P(w)$, and with (or, and) CYK recognition. The implementation provides the first two.
- **Works for weighted grammars.** Nothing in the algorithm uses that the probabilities of a nonterminal sum to 1, only that they are nonnegative.

## Variants and improvements

- **Inside probabilities.** Replace the maximum by a sum to get $\beta_A(i, j)$ and $P(w) = \beta_S(1, n)$, the first half of the [inside-outside algorithm](/inside-outside-algorithm/). Baker used this computation in 1979.
- **Unary rules.** Treebank grammars have unit productions such as $NP \to N$. Practical parsers keep them and, after filling a cell, close it under the unary rules: if $q(A \to B) \cdot \pi[i, j, B] > \pi[i, j, A]$, update $\pi[i, j, A]$. Since probabilities are at most 1, a cycle of unary rules never improves a value, and $v$ rounds of updates suffice.
- **Probability-preserving normal form.** [Chomsky normal form conversion](/chomsky-normal-form-conversion/) can carry the probabilities: binarizing $A \to B C D\ [q]$ into $A \to B X\ [q]$, $X \to C D\ [1]$ keeps the probability of every tree; removing $\varepsilon$ and unit productions is harder, since the probabilities of infinitely many derivations must be summed for the inside version.
- **$k$ best parses.** Keep the $k$ best entries per cell and nonterminal, merging candidates in order, to get the $k$ most probable trees.
- **Pruning.** Beam search keeps only the highest entries of each cell, and coarse-to-fine parsing uses a small grammar to prune the cells of a large one. Agenda-based and A* parsers explore the entries in order of probability and can stop before filling the whole table.
- **Earley-style parsing.** Stolcke's probabilistic [Earley parser](/earley-parser/) computes the same quantities without the normal form, and also prefix probabilities.
- **Hidden Markov models.** For a right-linear grammar the table is unnecessary, and the method becomes the [Viterbi algorithm](/viterbi-algorithm/), linear in $n$.

## When to use it

Use probabilistic CKY to find the best parse of sentences of moderate length under a PCFG or any grammar with nonnegative rule weights in Chomsky normal form, for example in statistical constituency parsing or RNA secondary structure prediction. It is simple, exact and easy to vectorize. For long inputs or very large grammars, the cubic table is the bottleneck, and pruned or agenda-based variants are used. For deterministic programming-language grammars, a linear-time [LR](/lr-parse-table/) or LL parser is the right tool, since there is only one tree.

## Pitfalls

- **Underflow.** The probability of a tree is a product of $2n - 1$ numbers below 1, which can underflow a double for sentences of a few dozen words when the lexical probabilities are small. Use log probabilities: products become sums and the comparisons of line L10 stay the same. The tests show a case where the plain product is 0.0 and the log version is exact.
- **Max is not sum.** The Viterbi entry for $S$ over the whole input is not $P(w)$. Computing $P(t \mid w)$ needs the inside version too.
- **Wrong normal form.** A unit or $\varepsilon$-production other than $S \to \varepsilon$ is silently ignored by the loops, which can lose the best tree. The implementation rejects such grammars; convert them with probabilities carried along, or use the unary-closure variant.
- **The most probable tree is not the most probable labeled bracketing.** Other decoders, such as maximizing the expected number of correct constituents with outside probabilities, can score better on bracketing measures.
- **Off by one in the final cell.** With indices between the words, $0 \le i < j \le n$, the whole input is the cell $(0, n)$, not $(1, n)$. Mixing the two conventions reads an empty or wrong cell; the pseudocode on this page uses $1 \le i \le j \le n$ throughout.
- **Negative weights.** With feature weights that can be negative, the product is not monotone and the maximum of products is not a product of maxima. Work in log space with arbitrary real scores added, which is monotone.

## Implementations

## History

Baker introduced the inside-outside algorithm in 1979 to train probabilistic grammars for speech recognition, computing the inside probabilities on a CYK-style table. Ney published the maximum-probability version, with time alignment for continuous speech, in 1991, and Jurafsky and Martin credit him with the first description of probabilistic CKY. Probabilistic CKY then became the base of statistical constituency parsers trained on treebanks, including the lexicalized parsers of Collins and Charniak and the latent-annotation parsers of Petrov and Klein.

## References
