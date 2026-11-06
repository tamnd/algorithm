---
tag: 0KFTGG
kind: algorithm
slug: cyk-algorithm
name: CYK algorithm
aliases:
- Cocke-Younger-Kasami algorithm
- CKY algorithm
area: automata-and-parsing/context-free-parsing
level: core
summary: Cubic-time dynamic programming recognizer for grammars in Chomsky normal form.
solves: [context-free-language-recognition, cfg-membership-problem]
model: word-ram
complexity:
  vars: {n: the length of the input string, g: the number of productions of the grammar in Chomsky normal form, v: the number of nonterminals}
  time: {worst: Θ(n^3 g), best: Θ(n^3 g)}
  space: {extra: Θ(n^2 v)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1965
  people: [John Cocke, Tadao Kasami, Daniel H. Younger]
  note: Kasami described the method in a 1965 report and Younger published it in a journal in 1967.
prereqs: [chomsky-normal-form, derivation, parse-tree]
see_also: [earley-parser, valiant-algorithm, probabilistic-cky, chomsky-normal-form-conversion, parse-chart, inside-outside-algorithm, chart-parsing, context-free-language-recognition]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.4.4, Testing Membership in a CFL
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 4.2, The CYK Parsing Method (4.2.2 CYK Recognition with a Grammar in Chomsky Normal Form, 4.2.5 CYK Parsing with Chomsky Normal Form, 4.2.7 A Short Retrospective of CYK)
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 27, The Cocke-Kasami-Younger Algorithm
  - paper: doi:10.1016/S0019-9958(67)80007-X
    title: Daniel H. Younger, Recognition and parsing of context-free languages in time n^3, Information and Control 10(2) (1967)
    locator: pp. 189 to 208
  - paper: "Tadao Kasami, An efficient recognition and syntax-analysis algorithm for context-free languages, Scientific Report AFCRL-65-758, Air Force Cambridge Research Laboratory, Bedford, Massachusetts, 1965"
    locator: the full report
  - paper: "Martin Lange and Hans Leiß, To CNF or not to CNF? An efficient yet presentable version of the CYK algorithm, Informatica Didactica 8 (2009)"
    locator: Section 2 (the growth of the grammar under the normal-form conversions) and the CYK variant for binary normal form
---

The CYK algorithm decides whether a string $w$ of length $n$ is in the language of a [context-free grammar](/context-free-grammar/) in [Chomsky normal form](/chomsky-normal-form/), and builds a [parse tree](/parse-tree/) when it is. It is dynamic programming over substrings: for each substring it computes the set of nonterminals that derive it, shortest substrings first, in $\Theta(n^3 g)$ time for $g$ productions. It was the first general [context-free recognition](/context-free-language-recognition/) algorithm with a polynomial bound, and its table is the starting point of [probabilistic CKY](/probabilistic-cky/), the [inside-outside algorithm](/inside-outside-algorithm/) and [Valiant's algorithm](/valiant-algorithm/).

## In plain words

In Chomsky normal form, every rule either turns a placeholder into one letter or splits it into exactly two placeholders. So a placeholder can produce a piece of the input in only two ways: the piece is one letter that a rule gives directly, or the piece splits at some point into a left part and a right part, each produced by one of the two placeholders of a rule.

CYK fills a triangular table with one cell for each piece of the input. It first fills the cells of single letters. Then it fills the cells of pieces of length 2, then 3, and so on. For a piece, it tries every split point and every two-placeholder rule, and looks up the two shorter pieces, whose cells are already filled. The input is in the language when the cell of the whole input holds the start symbol.

## The problem

The input is a grammar $G = (V, \Sigma, P, S)$ in Chomsky normal form and a string $w = a_1 a_2 \cdots a_n \in \Sigma^*$. We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the input length, $|G|$ the grammar size. Chomsky normal form allows only $A \to BC$ with $B, C \in V$, $A \to a$ with $a \in \Sigma$, and $S \to \varepsilon$ when $S$ is on no right side. Write $g = |P|$ and $v = |V|$; in this form $|G| \le 3g$, so $g$ and $|G|$ differ by a constant factor.

The output of the recognizer is yes when $S \Rightarrow^* w$ and no otherwise ([membership problem](/cfg-membership-problem/)). The parser also outputs one parse tree. Any grammar can be brought to this form by [Chomsky normal form conversion](/chomsky-normal-form-conversion/), which keeps the language.

## The algorithm

$T[i, j]$ is the set of nonterminals that derive $a_i \cdots a_j$, for $1 \le i \le j \le n$.

```pseudo id=main
CYK(G, w)                                   ▷ G in Chomsky normal form, w = a1 … an
L1  if n = 0 then return (S → ε ∈ P)
L2  for i ← 1 to n do
L3      T[i, i] ← { A : A → a_i ∈ P }
L4  for len ← 2 to n do                     ▷ length of the substring
L5      for i ← 1 to n − len + 1 do
L6          j ← i + len − 1;  T[i, j] ← ∅
L7          for k ← i to j − 1 do            ▷ split a_i … a_k | a_{k+1} … a_j
L8              for each A → B C in P do
L9                  if B ∈ T[i, k] and C ∈ T[k + 1, j] then
L10                     add A to T[i, j];  if back[i, j, A] is unset then back[i, j, A] ← (k, B, C)
L11 return S ∈ T[1, n]
```

Lines L2 and L3 fill the diagonal, one cell for each input symbol. The loop of line L4 goes through the lengths in increasing order, so when line L9 reads $T[i, k]$ and $T[k + 1, j]$, both cells are for shorter substrings and are final. The back pointer of line L10 records one way to build $A$ over $a_i \cdots a_j$. To get a tree, start from $(1, n, S)$ and follow the back pointers: a node $(i, j, A)$ with $i < j$ and back pointer $(k, B, C)$ has children $(i, k, B)$ and $(k + 1, j, C)$, and a node $(i, i, A)$ has the leaf $a_i$. The tree has $2n - 1$ internal nodes, so this costs $O(n)$ time. The implementation walks it with an explicit stack, because the tree can be $n$ levels deep.

## Example

Take the grammar of Hopcroft, Motwani and Ullman's example

$$S \to AB \mid BC, \qquad A \to BA \mid a, \qquad B \to CC \mid b, \qquad C \to AB \mid a$$

and $w = baaba$, so $n = 5$. Row $\ell$ of the table lists $T[i, i + \ell - 1]$ for $i = 1, \ldots, 6 - \ell$; a dash is the empty set.

| length | $i = 1$ | $i = 2$ | $i = 3$ | $i = 4$ | $i = 5$ |
|---|---|---|---|---|---|
| 1 | $\{B\}$ | $\{A, C\}$ | $\{A, C\}$ | $\{B\}$ | $\{A, C\}$ |
| 2 | $\{A, S\}$ | $\{B\}$ | $\{C, S\}$ | $\{A, S\}$ | |
| 3 | dash | $\{B\}$ | $\{B\}$ | | |
| 4 | dash | $\{A, C, S\}$ | | | |
| 5 | $\{A, C, S\}$ | | | | |

Two cells, step by step:

- $T[1, 2]$ for $ba$: the only split is $b \mid a$, with $\{B\}$ and $\{A, C\}$. The pairs $BA$ and $BC$ match $A \to BA$ and $S \to BC$, so $T[1, 2] = \{A, S\}$.
- $T[1, 3]$ for $baa$: the split $b \mid aa$ gives $\{B\} \times \{B\}$, and the split $ba \mid a$ gives $\{A, S\} \times \{A, C\}$. No right side is $BB$, $AA$, $AC$, $SA$ or $SC$, so $T[1, 3] = \emptyset$.

$S \in T[1, 5]$, so $baaba$ is in the language. The string has 2 parse trees. Taking the first split found, with $k$ from small to large, gives

$$S \to B\,C, \quad B \to b, \quad C \to A\,B \text{ over } aaba, \quad A \to a, \quad B \to C\,C \text{ over } aba, \quad C \to A\,B \text{ over } ab, \quad C \to a.$$

## Correctness

**Claim.** After the loops, for all $1 \le i \le j \le n$, $T[i, j] = \{A \in V : A \Rightarrow^* a_i \cdots a_j\}$. So line L11 answers yes exactly when $w \in L(G)$, and line L1 handles $n = 0$, since in Chomsky normal form only $S \to \varepsilon$ derives the empty string.

The proof is by induction on $j - i$. A nonterminal derives a single symbol $a_i$ only by $A \to a_i$, because $A \to BC$ produces at least two symbols. For a longer substring, a derivation must start with some $A \to BC$, and by the splitting lemma of [derivations](/derivation/), $B$ and $C$ derive a nonempty prefix and a nonempty suffix, which is exactly what lines L7 to L10 test with cells that are correct by the induction hypothesis. The full proof, with the tree construction, is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** Line L8 runs once for each triple $(\text{len}, i, k)$ with $2 \le \text{len} \le n$, $1 \le i \le n - \text{len} + 1$, $i \le k \le i + \text{len} - 2$. The number of these triples is

$$\sum_{\text{len} = 2}^{n} (n - \text{len} + 1)(\text{len} - 1) = \binom{n + 1}{3} = \frac{(n + 1)\, n\, (n - 1)}{6},$$

the number of ways to choose $i \le k < j$ from $n$ positions. Each run loops over the binary productions, and with each $T[i, j]$ stored as a bit array indexed by nonterminal, line L9 is $O(1)$. Lines L2 and L3 cost $O(n g)$. So the time is $\Theta(n^3 g)$ on the [word RAM](/word-ram/), in the best and the worst case alike, because the loops do not depend on the contents of the table. For $n = 5$ the count is $\binom{6}{3} = 20$ splits.

**Space.** The table has $n(n + 1)/2$ cells of $v$ entries each, and the back pointers take at most one entry per (cell, nonterminal), so the space is $\Theta(n^2 v)$.

**The cost of the normal form.** The bound is in the size of the converted grammar. Conversion in the order: split long right sides, remove $\varepsilon$-productions, remove unit productions, gives a grammar of size $O(|G|^2)$; other orders can give an exponential size (Lange and Leiß). Their variant of CYK accepts unit and $\varepsilon$-productions in a binarized grammar and keeps the time $O(n^3 |G|)$.

## Properties

- **Deterministic.** The table is a function of the grammar and the input.
- **Not online.** A cell for a long substring needs the whole substring. The [Earley parser](/earley-parser/) processes the input from left to right instead.
- **Not adaptive.** Unlike Earley's algorithm, CYK takes cubic time even on an unambiguous or a deterministic grammar.
- **All parses.** The table holds every parse: keeping all back pointers instead of the first one gives a [shared packed parse forest](/shared-packed-parse-forest/) with $O(n^3 g)$ edges.

## Variants and improvements

- **Probabilistic CKY.** Replace the sets by the best probability of each nonterminal over each span, and union by maximum, to get the [most probable parse](/most-probable-parse/) of a [probabilistic context-free grammar](/probabilistic-context-free-grammar/) ([probabilistic CKY](/probabilistic-cky/)). Replace the maximum by a sum to get the inside probabilities of the [inside-outside algorithm](/inside-outside-algorithm/).
- **Counting parses.** Store in each cell the number of trees of each nonterminal, and multiply and add instead of testing and adding.
- **Valiant's algorithm.** The loop over $k$ is a Boolean matrix product in disguise, and [Valiant's algorithm](/valiant-algorithm/) computes the table in $O(n^\omega)$ time for a fixed grammar.
- **Bit-parallel rows.** Storing the cells as bit vectors over the nonterminals and grouping the inner loop by $B$ speeds the method by a word-size factor in practice.
- **Without normal form.** Grune and Jacobs (Section 4.2.1) and Lange and Leiß give versions that work on grammars with unit and $\varepsilon$-productions.

## When to use it

Use CYK when you need all parses or a probabilistic parse of short inputs, for example sentences in natural-language processing, and when you can keep the grammar in Chomsky normal form. Its regular loops make it easy to vectorize. Use the [Earley parser](/earley-parser/) when the grammar is large and not in normal form, or when many inputs are unambiguous, because Earley's algorithm is quadratic or linear on them. For a programming language, use a deterministic parser such as [LALR(1)](/lalr-parsing/) or [LL(1)](/ll1-parsing/), which runs in linear time.

## Pitfalls

- **Wrong loop order.** Iterating over $i$ and $j$ in plain row order (`for i ← 1 to n do for j ← i to n do`) reads $T[k + 1, j]$ before it is final. Iterate by length, as in line L4, or by $i$ from $n$ down to 1. The worked example $baaba$ catches this, since $T[1, 5]$ needs $T[2, 5]$.
- **Off-by-one splits.** The split point must satisfy $i \le k \le j - 1$, so both halves are nonempty. Writing `for k ← i to j` reads the empty substring $a_{j+1} \cdots a_j$ and indexes past the table.
- **Forgetting the empty input.** With $n = 0$ the table is empty, and $S \in T[1, 0]$ is meaningless. Line L1 must test $S \to \varepsilon$. The tests check both $S \to \varepsilon \mid a$ and a grammar without $S \to \varepsilon$ on the empty string.
- **Feeding a grammar that is not in normal form.** A unit production $A \to B$ or a production $A \to aB$ is silently ignored by the loops, which gives wrong answers. The implementation rejects such grammars.
- **Deep recursion when building the tree.** A right-branching tree for $w = a^n$ has depth $n$. Build it with an explicit stack.

## Implementations

## History

Tadao Kasami described the algorithm in a 1965 report of the Air Force Cambridge Research Laboratory, and Daniel Younger published it, with the $n^3$ bound in the title, in Information and Control in 1967. The name also credits John Cocke, and the three names appear in different orders, as CYK or CKY. Valiant showed in 1975 that the table can be computed with fast matrix multiplication.

## References
