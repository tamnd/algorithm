---
tag: 0BHT8C
kind: algorithm
slug: gll-parsing
name: GLL parsing
aliases:
- generalized LL parsing
area: automata-and-parsing/parser-generators
level: research
summary: Generalized top-down parsing with descriptors and a graph-structured stack that handles all context-free grammars, due to Scott and Johnstone.
solves: [context-free-language-recognition]
model: word-ram
complexity:
  vars: {n: the input length, g: the grammar size}
  time: {worst: O(g^3 n^2 + g^2 n^3)}
  space: {worst: O(g^2 n^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2010
  people: [Elizabeth Scott, Adrian Johnstone]
  note: Scott and Johnstone presented GLL at the LDTA workshop in 2009, published in Electronic Notes in Theoretical Computer Science in 2010, as a recursive descent parser that keeps every alternative alive in a graph-structured stack; their 2013 paper added the construction of a shared packed parse forest.
prereqs: [recursive-descent-parsing, graph-structured-stack, context-free-grammar]
see_also: [glr-parsing, earley-parser, shared-packed-parse-forest, context-free-language-recognition, parser-combinators, left-recursion, cyk-algorithm, packrat-parsing]
sources:
  - paper: doi:10.1016/j.entcs.2010.08.041
    title: Elizabeth Scott and Adrian Johnstone, GLL Parsing, Electronic Notes in Theoretical Computer Science 253(7) (2010)
    locator: pp. 177 to 189 (grammar slots, descriptors, the sets U, R and P, the functions add, create and pop, and the cubic worst case)
  - paper: doi:10.1016/j.scico.2012.03.005
    title: Elizabeth Scott and Adrian Johnstone, GLL parse-tree generation, Science of Computer Programming 78(10) (2013)
    locator: pp. 1828 to 1844 (building a binarised shared packed parse forest during GLL parsing)
---

GLL parsing is a general top-down parsing method: it runs [recursive descent](/recursive-descent-parsing/) on any context-free grammar, including left-recursive and ambiguous ones, by keeping every alternative alive at once. The call stacks of all the alternatives share one [graph-structured stack](/graph-structured-stack/), and the work still to do is a set of *descriptors*, each a grammar position, a stack top and an input position. Because a descriptor is never processed twice and stack nodes are shared, the method terminates on every grammar and recognises in polynomial time, cubic in the input length in the worst case.

## In plain words

A recursive descent parser follows the grammar like a program: each rule is a procedure, and reading a rule's name means calling it. It fails on rules that call themselves first, and it must guess between alternatives. GLL removes both problems. It tries every alternative, but instead of one call stack per attempt it keeps one shared map of "who is waiting for whom", where each waiting caller is recorded once per input position. A unit of pending work says: continue at this point of this rule, at this input position, and return to this waiting caller. The parser keeps a list of such units, never does the same unit twice, and when a rule finishes it hands the result to every caller waiting for it, including callers that only start waiting later.

## The problem

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, the empty string $\varepsilon$, start symbol $S$, input length $n$ and size $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$. The input is $w = a_1 \cdots a_n$; position $i$ means that $a_1 \cdots a_i$ has been read, and $w[j:i]$ is $a_{j+1} \cdots a_i$.

**Input.** A context-free grammar $G$, with no restriction (ε-productions, left recursion, cycles $A \Rightarrow^+ A$ and ambiguity are all allowed), and a string $w$.

**Output.** Whether $S \Rightarrow^* w$, the [recognition problem](/context-free-language-recognition/). The implementation also reports every triple $(A, j, i)$ with $A \Rightarrow^* w[j:i]$ for the calls of $A$ at $j$ that the search made, from which a parse forest can be built.

## The algorithm

A *grammar slot* is a production with a dot, $A \to \alpha \cdot \beta$, the point that a recursive descent procedure for $A$ has reached. A *GSS node* is a pair $(L, j)$ of a *return slot* $L = B \to \gamma X \cdot \delta$, the slot right after a nonterminal $X$, and the position $j$ at which $X$ was called: it stands for "a caller waits to resume at $L$ after $X$ has read from position $j$". Edges $v \to u$ go from a node to the nodes below it, so one node can have many stacks beneath it; the root $u_0$ is the bottom of every stack. A *descriptor* $(L, u, i)$ is a slot $L$, a stack top $u$ and an input position $i$. Three sets drive the search: $U$ holds every descriptor ever created, $R$ the ones still to process, and $P$ the pairs $(u, i)$ such that the call at $u$ has returned at position $i$.

```pseudo id=main
GLL(G, w)
L1  u0 ← the GSS root; for each production S → γ: ADD(S → ·γ, u0, 0)
L2  while R is not empty: remove a descriptor (L, u, i) from R
L3      while L = A → α·aβ with a terminal a: if a_{i+1} = a then L ← A → αa·β; i ← i + 1 else go to the next descriptor
L4      if L = A → α·Bβ with B a nonterminal: v ← CREATE(A → αB·β, u, i); for each B → γ: ADD(B → ·γ, v, i)
L5      else (L = A → α·): POP(u, i)
L6  accept if and only if POP(u0, n) was called
CREATE(L, u, i)
L7  v ← the GSS node (L, i), made if new
L8  if the edge v → u is new: add it; for each (v, k) in P: ADD(L, u, k)
L9  return v
POP(u, i)
L10 if u = u0: record that S derives a_1 … a_i; return
L11 if (u, i) is not in P: add (u, i) to P; for each edge u → v: ADD(L_u, v, i), where L_u is the return slot of u
ADD(L, u, i)
L12 if (L, u, i) is not in U: add it to U and to R
```

**Lines L2 to L5** are one step of recursive descent. Terminals are matched in place (L3). A nonterminal $B$ is a call (L4): the caller's continuation becomes the node $(A \to \alpha B \cdot \beta, i)$ on top of $u$, and every alternative of $B$ starts there. A finished alternative is a return (L5).

**CREATE (L7 to L9).** All calls of $B$ from the same return slot at the same position share one node, which is what keeps the stack finite under left recursion: a call of $E$ from $E \to \cdot E + E$ at position $j$ reaches the same node again and only adds an edge. If the shared call has already returned at some positions, those results are replayed to the new caller at once (L8), since the work below the node will not be done again.

**POP (L10 and L11)** returns from the call at $u$ to every caller below it, and records $(u, i)$ in $P$ for callers that arrive later. A return to the root records that $S$ derives a prefix of the input.

**ADD (L12)** discards duplicates, which bounds the work: there are finitely many descriptors.

The published algorithm generates code for a particular grammar, with one label per slot and a `goto` loop instead of recursion, and tests the next token against the FIRST and FOLLOW sets of an alternative before adding its descriptor. The interpreter here takes the grammar as data and skips that test, which changes the amount of work but not the result.

## Example

**Grammar.** $E \to E + E \mid n$, which is left-recursive and ambiguous, on the input $n + n$ ($n = 3$). The GSS nodes created are $u_1 = (E \to E \cdot + E, 0)$, $u_2 = (E \to E + E \cdot, 2)$ and $u_3 = (E \to E \cdot + E, 2)$. Descriptors are taken last in, first out.

| Step | Descriptor taken | What happens |
| --- | --- | --- |
| 1 | $(E \to \cdot n, u_0, 0)$ | match $n$; POP$(u_0, 1)$: $E$ derives $w[0:1]$, not the whole input |
| 2 | $(E \to \cdot E + E, u_0, 0)$ | create $u_1$, edge $u_1 \to u_0$; add $(E \to \cdot E + E, u_1, 0)$ and $(E \to \cdot n, u_1, 0)$ |
| 3 | $(E \to \cdot n, u_1, 0)$ | match; POP$(u_1, 1)$: $P \ni (u_1, 1)$; add $(E \to E \cdot + E, u_0, 1)$ |
| 4 | $(E \to E \cdot + E, u_0, 1)$ | match $+$; create $u_2$, edge $u_2 \to u_0$; add both alternatives of $E$ at $u_2$, position 2 |
| 5 | $(E \to \cdot n, u_2, 2)$ | match; POP$(u_2, 3)$; add $(E \to E + E \cdot, u_0, 3)$ |
| 6 | $(E \to E + E \cdot, u_0, 3)$ | POP$(u_0, 3)$: the whole input is derived, so it is accepted |
| 7 | $(E \to \cdot E + E, u_2, 2)$ | create $u_3$, edge $u_3 \to u_2$; add both alternatives at $u_3$, position 2 |
| 8 | $(E \to \cdot n, u_3, 2)$ | match; POP$(u_3, 3)$; add $(E \to E \cdot + E, u_2, 3)$ |
| 9 | $(E \to E \cdot + E, u_2, 3)$ | $+$ does not match at the end of the input |
| 10 | $(E \to \cdot E + E, u_3, 2)$ | $u_3$ exists; new edge $u_3 \to u_3$; replay $(u_3, 3)$: add $(E \to E \cdot + E, u_3, 3)$; the call descriptors are duplicates |
| 11 | $(E \to E \cdot + E, u_3, 3)$ | no match |
| 12 | $(E \to \cdot E + E, u_1, 0)$ | new edge $u_1 \to u_1$; replay $(u_1, 1)$: add $(E \to E \cdot + E, u_1, 1)$ |
| 13 | $(E \to E \cdot + E, u_1, 1)$ | match $+$; $u_2$ exists, new edge $u_2 \to u_1$; replay $(u_2, 3)$: add $(E \to E + E \cdot, u_1, 3)$ |
| 14 | $(E \to E + E \cdot, u_1, 3)$ | POP$(u_1, 3)$; add $(E \to E \cdot + E, u_0, 3)$ and $(E \to E \cdot + E, u_1, 3)$ |
| 15, 16 | the two descriptors of step 14 | no match |

The run processes 16 descriptors and builds 3 nodes besides the root and 6 edges. Left recursion appears as the self-loops $u_1 \to u_1$ and $u_3 \to u_3$: the call of $E$ by $E \to \cdot E + E$ at the same position returns to the same node, and the results already in $P$ are replayed along the new edge (steps 10, 12 and 13), where plain recursive descent would recurse forever. The calls found are $E$ at 0 deriving $w[0:1]$ and $w[0:3]$, and $E$ at 2 deriving $w[2:3]$. A script reproduced this trace from the implementation; on $n + n + n$ the run accepts with 5 nodes and finds both parses through the spans $(E, 0, 3)$ and $(E, 2, 5)$.

## Correctness

The proof in [correctness](proofs/correctness.md) shows three invariants that make every recorded fact true (soundness): a descriptor $(A \to \alpha \cdot \beta, u, i)$ whose node $u$ called $A$ at $j$ has $\alpha \Rightarrow^* w[j:i]$, each edge records a caller that really reached the call, and $(u, i) \in P$ means the called nonterminal derives the span. Completeness is an induction on the size of derivation trees: whenever a call of $X$ at $j$ is made and $X \Rightarrow^* w[j:i]$, the caller is eventually resumed at $i$, because whichever of the edge and the $P$ entry comes second triggers the resumption (L8 or L11). Termination follows from the finiteness of $U$. The tests compare the result with a brute-force fixed point over all substrings on 600 random grammars with every input up to length 6, plus longer random inputs, and also check the set of GSS nodes and the derived spans of every call.

## Complexity

Let $s \le |G|$ be the number of slots. There are at most $s (n + 1)$ GSS nodes, so at most $s^2 (n + 1)^2$ edges and $s \cdot (s (n + 1) + 1) \cdot (n + 1)$ descriptors, which is $O(|G|^2 n^2)$ space; $P$ has $O(|G| \, n^2)$ pairs.

- **Per descriptor.** Each descriptor is processed once; matching terminals and adding the alternatives of a called nonterminal cost $O(|G|)$, so $O(|G|^3 n^2)$ in total.
- **Replays.** A new edge replays at most $n + 1$ entries of $P$ (L8), and a new entry of $P$ walks the at most $s (n + 1) + 1$ edges out of one node (L11); both total $O(|G|^2 n^3)$.

So the time is $O(|G|^3 n^2 + |G|^2 n^3)$, cubic in $n$ for a fixed grammar, matching Scott and Johnstone's worst case. On the ambiguous grammar $E \to E + E \mid n$ the counts grow quadratically: 96, 286, 966 and 3526 descriptors for 5, 10, 20 and 40 operators.

## Properties

- **All context-free grammars.** No restriction on the grammar: ε-productions, hidden left recursion, cycles and ambiguity are handled, and the tests include all of them.
- **Top-down shape.** The parser follows the grammar's productions in the order a recursive descent parser would, so semantic actions and error messages can refer to grammar positions, as in hand-written parsers.
- **No recursion.** The work list replaces the call stack, so the implementation runs on a 20000-token left-recursive or right-recursive input without a deep host stack.
- **Order independence.** Descriptors may be taken from $R$ in any order: the final $U$, $P$ and GSS are the least sets closed under the steps of the algorithm, so the order changes only the sequence of events, not the result. The implementation takes them last in, first out.
- **Not online as written.** Descriptors at earlier positions can be processed after later ones, so the input must be available in full before the run.

## Variants and improvements

- **Parse forests.** Scott and Johnstone's 2013 paper builds a binarised [shared packed parse forest](/shared-packed-parse-forest/) during the run, with nodes for slots and spans, which keeps the forest cubic in size for every grammar.
- **Lookahead tests.** Testing the next token against the FIRST set of an alternative, or the FOLLOW set of its nonterminal if it is nullable, before adding its descriptor prunes most dead alternatives. Without it, $S \to A\,b$, $A \to a\,A \mid \varepsilon$ on $a^k b$ takes quadratic work, since $A$ is found to derive every $a^m$ that follows its call: the implementation here creates 5354, 20704 and 81404 descriptors for $k = 100$, 200 and 400.
- **Nonterminal-keyed stacks.** Keying GSS nodes by the called nonterminal and position, instead of the return slot and position, shares the work of one call among callers in different slots; Afroozeh and Izmaylova used this to speed up GLL in practice.
- **Combinators.** [Parser combinator](/parser-combinators/) libraries built on GLL, and memoized continuation-passing combinators in general, accept all context-free grammars, including left-recursive ones.
- **Relatives.** [GLR parsing](/glr-parsing/) does the same generalisation bottom-up, over an LR automaton; the [Earley parser](/earley-parser/) keeps item sets per position with similar cubic bounds; [CYK](/cyk-algorithm/) needs a grammar in Chomsky normal form.

## When to use it

Use GLL when the grammar should stay as written, with left recursion and ambiguity, and when a top-down structure is wanted: for language workbenches, reverse engineering of legacy languages whose grammars are not LR or LL, and combinator libraries that must accept any grammar. For grammars that are LL(1) or LALR(1), a deterministic parser from a [parser generator](/parser-generator/) is faster and reports conflicts; for natural language, chart parsers such as [Earley](/earley-parser/) are the usual choice.

## Pitfalls

- **Replays on late edges.** Omitting the replay of $P$ in CREATE (L8) loses every parse in which a shared call returned before a second caller arrived, which is exactly the left-recursive case; the tests here fail when it is removed.
- **Node identity.** Nodes must be keyed by the return slot and the call position only, not by the stack below; keying them by more makes the stack grow without bound on left recursion.
- **Recursion through ADD.** Processing a descriptor at once inside ADD, instead of queueing it in $R$, rebuilds the deep call stack that the method was meant to avoid.
- **Quadratic and cubic work on easy grammars.** Without lookahead tests, even an LL(1) grammar can make a call derive many spans, as in the $a^k b$ example; the worst case is cubic for highly ambiguous grammars.
- **Recognition is not parsing.** Accepting the input does not give a tree; building the forest needs the extra bookkeeping of the 2013 paper, and the forest of an ambiguous grammar can encode exponentially many trees.

## Implementations

## History

Scott and Johnstone introduced GLL at the Workshop on Language Descriptions, Tools and Applications (LDTA) in 2009, and the paper appeared in Electronic Notes in Theoretical Computer Science in 2010. It brought to top-down parsing the graph-structured stack that Tomita had used for generalized LR parsing in the 1980s, with the descriptor sets ensuring termination on left recursion. Their 2013 paper in Science of Computer Programming added the construction of shared packed parse forests, and later work by others refined the stack and used GLL inside parser combinator libraries.

## References
