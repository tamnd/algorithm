---
tag: FA07T5
kind: algorithm
slug: parsing-with-derivatives
name: Parsing with derivatives
aliases:
- Brzozowski derivative parsing
area: automata-and-parsing/context-free-parsing
level: research
summary: Recognizes strings by symbolically differentiating the grammar with respect to each input token.
solves: [context-free-language-recognition]
model: word-ram
complexity:
  vars: {n: the number of input tokens, g: the grammar size}
  time: {worst: O(g n^3), best: Θ(n)}
  space: {extra: O(g n^3)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 2011
  people: [Matthew Might, David Darais, Daniel Spiewak]
  note: Might, Darais and Spiewak extended Brzozowski's 1964 derivatives of regular expressions to context-free grammars with laziness, memoization and fixed points; Adams, Hollenbeck and Might proved the cubic bound in 2016.
prereqs: [brzozowski-derivatives, context-free-grammar, memoization]
see_also: [regex-derivative, antimirov-derivatives, earley-parser, parser-combinators, cyk-algorithm, shared-packed-parse-forest, first-and-follow-sets, fixed-point]
sources:
  - paper: doi:10.1145/2034773.2034801
    title: Matthew Might, David Darais and Daniel Spiewak, Parsing with derivatives, a functional pearl, Proceedings of the 16th ACM SIGPLAN International Conference on Functional Programming (ICFP 2011)
    locator: pp. 189 to 195
  - paper: doi:10.1145/2908080.2908128
    title: Michael D. Adams, Celeste Hollenbeck and Matthew Might, On the complexity and performance of parsing with derivatives, PLDI 2016
    locator: pp. 224 to 236; Section 2 (memoization, laziness and the nullability fixed point), Section 3 (Lemma 1, Theorems 8 and 9, the O(G n^3) bound), Section 4 (compaction and fixed points in practice)
  - paper: doi:10.1145/321239.321249
    title: Janusz A. Brzozowski, Derivatives of regular expressions, Journal of the ACM 11(4) (1964)
    locator: pp. 481 to 494
  - paper: doi:10.1145/3360553
    title: Ian Henriksen, Gianfranco Bilardi and Keshav Pingali, Derivative grammars, a symbolic approach to parsing with derivatives, Proceedings of the ACM on Programming Languages 3, OOPSLA (2019)
    locator: the relation between derivative grammars and Earley parsing
  - paper: doi:10.1145/3385412.3385992
    title: Romain Edelmann, Jad Hamza and Viktor Kunčak, Zippy LL(1) parsing with derivatives, PLDI 2020
    locator: pp. 1036 to 1051 (linear time for LL(1) grammars)
---

Parsing with derivatives recognizes a string by repeatedly taking the *derivative* of the grammar with respect to the next token: the derivative of a language $L$ by a token $c$ is the language of the strings $v$ such that $c v$ is in $L$. After all $n$ tokens of $w$, the string is in the language exactly when what remains contains the empty string. Brzozowski introduced derivatives for regular expressions in 1964; Might, Darais and Spiewak extended them to arbitrary context-free grammars in 2011 by treating the grammar as a cyclic graph and computing derivatives lazily, with memoization and a fixed point for nullability. The method needs no tables and no grammar transformation, handles left recursion, ambiguity and $\varepsilon$-productions, and Adams, Hollenbeck and Might showed in 2016 that it runs in $O(|G| n^3)$ time, like the other general parsers.

## In plain words

Think of a grammar as a description of a set of sentences. Reading the first word of a sentence, we can ask: which endings are still possible? The answer is a new description, and it can be computed from the old one by simple rules: a choice between two descriptions gives a choice between their two leftovers, and a sequence gives the leftover of its first part followed by its second part, plus, if the first part may be empty, the leftover of the second part.

So the parser keeps one description and updates it once per word. At the end, it asks one question: may the leftover description be empty? If yes, the sentence was accepted.

Grammars refer to themselves, so the descriptions are graphs with loops. The parser remembers every leftover it has already built and reuses it, which ties the loops and keeps the work small.

## The problem

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. Given a grammar $G$ and a string $w = a_1 \cdots a_n$ of tokens, decide whether $w \in L(G)$: this is [context-free language recognition](/context-free-language-recognition/).

The derivative of a language $L$ by a token $c$ is $\partial_c L = \{ v : c v \in L \}$, and $\partial_{a_1 \cdots a_n} L = \partial_{a_n} \cdots \partial_{a_1} L$. Then

$$w \in L \iff \varepsilon \in \partial_w L,$$

so recognition reduces to $n$ derivatives and one *nullability* test. The algebra is the one of [Brzozowski derivatives](/brzozowski-derivatives/):

$$\partial_c \emptyset = \partial_c \{\varepsilon\} = \emptyset, \quad \partial_c \{a\} = \begin{cases} \{\varepsilon\} & a = c \\ \emptyset & a \ne c \end{cases}, \quad \partial_c (L_1 \cup L_2) = \partial_c L_1 \cup \partial_c L_2,$$

$$\partial_c (L_1 L_2) = (\partial_c L_1)\, L_2 \ \text{ if } \varepsilon \notin L_1, \qquad \partial_c (L_1 L_2) = (\partial_c L_1)\, L_2 \cup \partial_c L_2 \ \text{ if } \varepsilon \in L_1.$$

For regular expressions these rules work on finite trees. A grammar is recursive, so its languages are a *graph* with cycles: each nonterminal becomes a union node over its productions, each production a chain of concatenation nodes, and a nonterminal in a right side is an edge back to its union node. The meaning of the graph is the least solution of the equations above, which is $L(G)$.

## The algorithm

The nodes are $\emptyset$, $\varepsilon$, tokens, unions $y \cup z$ and concatenations $y \circ z$. $D_c$ computes a node for the derivative of a node; it is memoized on the pair (node, token) and, to tie cycles, stores the new node in the memo table *before* computing its children. NULLABLE decides whether a node's language contains $\varepsilon$, as a least fixed point.

```pseudo id=main
RECOGNIZE(L, w)                             ▷ L is the graph of G, rooted at S
L1  for each token c of w in order do L ← D_c(L)
L2  return NULLABLE(L)

D_c(x)
L3  x ← COMPACT(x)                          ▷ skip ∅ ∪ y, y ∪ ∅, ε ∘ y; ∅ ∘ y and y ∘ ∅ give ∅
L4  if x is ∅ or ε then return ∅
L5  if x is a token a then return ε if a = c, else ∅
L6  if memo[x, c] exists then return memo[x, c]
L7  if x = y ∪ z then u ← a new ∪ node; memo[x, c] ← u; u.children ← D_c(y), D_c(z)
L8  else if x = y ∘ z and not NULLABLE(y) then u ← a new ∘ node; memo[x, c] ← u; u.children ← D_c(y), z
L9  else u ← a new node (□ ∘ z) ∪ □; memo[x, c] ← u; fill the holes with D_c(y) and D_c(z)
L10 return u

NULLABLE(x)
L11 collect the nodes reachable from x whose nullability is not yet decided
L12 mark ε; mark a ∪ node when one child is marked, a ∘ node when both are; propagate until no change
L13 the collected nodes left unmarked are not nullable; return whether x is marked
```

The children of a new node are computed after the node is in the memo table, so a recursive call that reaches $x$ again finds $u$ and points to it: this is the "laziness" of the original paper. The implementation keeps the pending nodes on an explicit stack instead of recursing, so deep grammars and long inputs do not hit Python's recursion limit. NULLABLE uses one counter per node, the number of children still to be proven nullable, which makes all its calls together linear in the number of nodes; recomputing the fixed point by repeated passes, as the first implementations did, is quadratic.

COMPACT (line L3) applies identities such as $\emptyset \cup y = y$ and $\varepsilon \circ y = y$ to the old node before deriving it. It changes no language, but without it the useless $\emptyset$ branches made by earlier steps are derived again and again; on the left recursive grammar below, it cuts the nodes built for about 1000 tokens from about 255000 to about 2500. Might et al. call such rules compaction; Adams et al. give a larger set.

## Example

Take the left recursive grammar $S \to S + n \mid n$ and the input $n + n$. The graph has $S = (S \circ P) \cup (n \cup \emptyset)$ with $P = + \circ n$. Write $S_i$ for the root after $i$ tokens.

| step | token | new root | nodes built | nullable |
| --- | --- | --- | --- | --- |
| 0 | | $S = (S \circ P) \cup (n \cup \emptyset)$ | | no |
| 1 | $n$ | $S_1 = (S_1 \circ P) \cup \varepsilon$ | 2 | yes |
| 2 | $+$ | $S_2 = ((S_2 \circ P) \cup (\varepsilon \circ n)) \cup \emptyset$ | 4 | no |
| 3 | $n$ | $S_3 = (S_3 \circ P) \cup \varepsilon$ | 2 | yes |

Step 1: $D_n(S)$ creates the union $S_1$ and puts it in the memo table. Its left child is $D_n(S \circ P)$; $S$ is not nullable, so line L8 creates $D_n(S) \circ P$, and $D_n(S)$ is found in the memo table: it is $S_1$ itself, a cycle. The right child $D_n(n \cup \emptyset)$ is compacted to $D_n(n) = \varepsilon$. So $S_1$ is the language $\{\varepsilon, {+n}, {+n+n}, \ldots\}$ of the possible continuations, and it is nullable: the input $n$ alone is a sentence.

Step 2: $S_1 \circ P$ now has a nullable left part, so line L9 builds $(D_+(S_1) \circ P) \cup D_+(P)$, where $D_+(S_1) = S_2$ by the memo table and $D_+(P) = \varepsilon \circ n$. The branch $D_+(\varepsilon) = \emptyset$ stays, but it is skipped by the next compaction. $S_2$ is not nullable: $n +$ is not a sentence.

Step 3: compaction removes the $\emptyset$ branch of $S_2$ and turns $\varepsilon \circ n$ into $n$, and the derivative has the same shape as $S_1$. It is nullable, so $n + n$ is accepted, after 8 nodes in total. The tests check every node of this table.

Memoization is what keeps the work polynomial. For the grammar $S \to A^{12}$ (twelve copies of $A$), $A \to a \mid \varepsilon$, which has no recursion, the derivative without memoization copies the tail of the sequence twice for each nullable head:

| tokens | nodes built with memoization | nodes built without |
| --- | --- | --- |
| 1 | 23 | 47 |
| 2 | 56 | 347 |
| 4 | 87 | 4412 |
| 6 | 104 | 19202 |
| 8 | 117 | 44288 |

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The meaning of a graph node is the least language that satisfies the node equations; for the grammar graph it is $L(G)$, because membership proofs in the graph and parse trees are the same objects up to contraction. Compaction rewrites a node to one with the same language. NULLABLE computes the least solution of the Boolean equations $\varepsilon \in [y \cup z] \iff \varepsilon \in [y] \lor \varepsilon \in [z]$ and $\varepsilon \in [y \circ z] \iff \varepsilon \in [y] \land \varepsilon \in [z]$, and the counters make it mark a node exactly when its last needed child is marked.

The main lemma: after one step, each memo node $u$ for a node $x$ denotes $\partial_c [x]$. The family $\partial_c [x]$ satisfies the equations of the new nodes, by the derivative rules, so the least solution is contained in it; conversely, if $c v \in [x]$, induction on the size of a membership proof gives $v \in [u]$, using the nullable branch of line L9 exactly when the first part of a concatenation matched the empty string. Then after $i$ tokens the root denotes $\partial_{a_1 \cdots a_i} L(G)$, and line L2 answers $\varepsilon \in \partial_w L(G)$, that is $w \in L(G)$. Every call stops because the memo keys are pairs of an existing node and a token.

## Complexity

Adams, Hollenbeck and Might bound the work by the number of nodes created. Every call of $D_c$ that is not a memo hit creates at least one node and does $O(1)$ other work, and all calls of NULLABLE together are linear in the number of nodes, using the counter method above. To count the nodes, they name each one by the initial node it came from and the tokens it was derived by, with one marker for the second branch of line L9, and show that every name is $N u$ or $N u \bullet v$ for an initial node $N$ and substrings $u$, $u v$ of the input. There are $O(|G|)$ choices of $N$, $O(n^2)$ substrings and $O(n)$ positions of the marker, so at most $O(|G| n^3)$ nodes are ever created, and the time and space are $O(|G| n^3)$. The memo table needs hashing of (node, token) pairs, $O(1)$ expected time per lookup.

The first paper gave only an exponential bound, $O(2^{2n} |G|^2)$, and a widely held belief was that the method was inherently exponential. The cubic bound matches CYK and Earley in $n$; for unambiguous or deterministic grammars, the observed growth is usually much smaller, and the best case is linear: for $S \to a S \mid \varepsilon$ on $a^n$, the memo table makes every step after the first a lookup.

## Properties

- **Online.** After each token, the current node is the language of the possible continuations; NULLABLE on it says whether the prefix read so far is a sentence, and an empty language means no continuation can succeed.
- **No preprocessing.** No tables, no normal form, no removal of left recursion or $\varepsilon$-productions. The grammar can be written with combinators, which is why the method is popular as a parser-combinator library.
- **Purely functional in spirit.** The method is a few equations plus memoization, laziness and a fixed point. The mutable memo table and the in-place filling of children are the only imperative parts.
- **Not linear for deterministic grammars.** Even on LL(1) or LR(1) grammars, the plain method can build more than a constant number of nodes per token, unlike the deterministic parsers.

## Variants and improvements

- **Parse forests.** Might et al. attach reduction functions to nodes and let $\varepsilon$ nodes carry the trees built so far, so that the final nullable node yields all parse trees. With a shared, possibly cyclic, representation of the trees, as in a [shared packed parse forest](/shared-packed-parse-forest/), the cubic bound still holds.
- **Faster implementations.** Adams et al. report a speedup of almost 1000 times over the original implementation, mostly from the linear-time fixed point, better compaction and cheaper memo tables.
- **Derivative grammars.** Henriksen, Bilardi and Pingali (2019) express the derivatives as new grammar rules instead of graph nodes and relate the resulting parser to the [Earley parser](/earley-parser/).
- **LL(1) with zippers.** Edelmann, Hamza and Kunčak (2020) restrict to LL(1) grammars and use a zipper to focus on the active part of the grammar, which gives linear time.
- **Regular expressions.** On regular expressions, the same rules give Brzozowski's construction of a DFA, whose states are derivatives up to similarity; see [regex derivatives](/regex-derivative/) and the partial derivatives of [Antimirov](/antimirov-derivatives/).

## When to use it

Use parsing with derivatives when you want a general context-free parser that is small, easy to write in a functional language, and accepts any grammar written as combinators, including left recursive and ambiguous ones, for example in teaching, prototyping or language workbenches. For production parsers of deterministic languages, an [LR](/lr-parse-table/) or LL parser is faster by large constant factors and linear. For general parsing with predictable performance, the [Earley parser](/earley-parser/) and GLR parsers are better understood and have mature implementations.

## Pitfalls

- **No memoization, or memoization after the fact.** Storing the derivative only after its children are computed loops forever on any recursive grammar, and forgetting to memoize makes the graph grow exponentially, as the table above shows.
- **Naive nullability.** A recursive NULLABLE that recurses into cycles does not terminate; an iterated fixed point that rescans all nodes until nothing changes is correct but quadratic. Use the least fixed point with counters, and note that nullability must start from "not nullable" (the least fixed point); starting from "nullable" gives wrong answers on cycles such as $S \to S$.
- **Nullability of unfinished nodes.** Line L8 asks NULLABLE about the first child of an old node, which is complete. Asking it about a node created in the current step, whose children are still holes, reads an incomplete graph.
- **Deep recursion.** The derivative of a deeply nested graph recurses as deep as the graph; on long inputs this overflows the call stack in many languages. Keep the pending nodes on an explicit stack.
- **Garbage growth.** Without compaction, the $\emptyset$ branches of all earlier steps stay reachable and are derived again at every step; on the left recursive grammar of the example, the number of nodes built then grows quadratically in $n$ instead of linearly.

## Implementations

## History

Brzozowski defined derivatives of regular expressions in 1964 and showed that a regular expression has finitely many dissimilar derivatives, which gives a DFA; Owens, Reppy and Turon revived the method for regular-expression matching in 2009. Might, Darais and Spiewak's functional pearl at ICFP 2011 extended derivatives to context-free grammars: the grammar is a cyclic graph, derivatives are memoized and computed lazily, and nullability is a least fixed point. They reported an exponential worst-case bound and slow running times, and many implementations followed. Adams, Hollenbeck and Might proved in 2016 that the method is cubic, with a counting argument over names of nodes, and made it competitive with other general parsers. Later work related derivatives to Earley parsing and gave linear-time versions for LL(1) grammars.

## References
