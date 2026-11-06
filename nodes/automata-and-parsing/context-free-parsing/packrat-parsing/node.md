---
tag: 1PYY5B
kind: algorithm
slug: packrat-parsing
name: Packrat parsing
aliases:
- memoized recursive descent
- memoized recursive descent parsing
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Backtracking recursive descent with memoization, giving linear time for PEGs.
model: word-ram
complexity:
  vars: {n: the number of input tokens, g: the number of subexpressions of the grammar}
  time: {worst: O(g n), best: O(g)}
  space: {extra: O(g n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2002
  people: [Bryan Ford]
  note: Ford named and implemented packrat parsing in 2002 and defined parsing expression grammars in 2004; the linear-time tabular method for the TDPL formalism is due to Birman and Ullman (1970 to 1973).
prereqs: [parsing-expression-grammar, recursive-descent-parsing, memoization]
see_also: [backtracking-parsing, left-recursion, parser-combinators, top-down-parsing, ll-star-parsing, gll-parsing, earley-parser, cyk-algorithm]
sources:
  - paper: doi:10.1145/581478.581483
    title: Bryan Ford, Packrat parsing, simple, powerful, lazy, linear time, Proceedings of the seventh ACM SIGPLAN International Conference on Functional Programming (ICFP 2002)
    locator: pp. 36 to 47
  - paper: doi:10.1145/964001.964011
    title: Bryan Ford, Parsing expression grammars, a recognition-based syntactic foundation, Proceedings of the 31st ACM Symposium on Principles of Programming Languages (POPL 2004)
    locator: pp. 111 to 122 (the semantics, well-formedness, and the reduction of PEGs to TDPL, which gives linear-time recognition)
  - paper: doi:10.1016/S0019-9958(73)90851-6
    title: Alexander Birman and Jeffrey D. Ullman, Parsing algorithms with backtrack, Information and Control 23(1) (1973)
    locator: pp. 1 to 34 (TDPL and GTDPL, and their linear-time tabular recognition)
  - paper: doi:10.1145/1328408.1328424
    title: Alessandro Warth, James R. Douglass and Todd Millstein, Packrat parsers can support left recursion, Proceedings of PEPM 2008
    locator: pp. 103 to 110
---

Packrat parsing runs a [parsing expression grammar](/parsing-expression-grammar/) (PEG) in linear time. It is a [backtracking](/backtracking-parsing/) [recursive descent parser](/recursive-descent-parsing/) that remembers the result of every rule at every input position, so no rule is ever tried twice at the same place. Since a PEG gives each expression a unique result at each position, the table of results has $O(|G| \, n)$ entries, each computed once from a constant number of others.

## In plain words

A recursive descent parser has one procedure for each rule of the grammar. With ordered choice, a procedure tries its alternatives in turn and backs up to the same input position when one fails. Backing up makes such parsers slow: the second alternative often asks the same question as the first, such as "is there a term here?", and the answer is worked out again inside every retry. The time can grow exponentially.

Packrat parsing keeps a table with one cell for each rule and each input position. The first time a rule is tried at a position, the answer, a failure or the place where the match ends, goes into the cell. Every later question about that rule and that position is a lookup. The table has a fixed number of cells for each token, so the whole parse takes linear time, at the cost of linear memory.

## The problem

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. A PEG has instead one rule $A \leftarrow e_A$ for each $A \in V$, where $e_A$ is a parsing expression built from $\varepsilon$, terminals, nonterminals, sequence $e_1 e_2$, ordered choice $e_1 / e_2$, repetition $e^*$, and the predicates $!e$ and $\&e$. For a PEG, $|G|$ is the number of subexpressions of all rules.

**Input.** A PEG $G$ with start symbol $S$, and a string $w = a_1 \cdots a_n$.

**Output.** The result $\mathrm{m}(S, 0)$ of matching $S$ at position $0$ as defined on the [parsing expression grammar](/parsing-expression-grammar/) page: either $\mathsf{fail}$ or the end $j$ of the match. The input is accepted when $j = n$, and then the parser returns the parse tree, whose nodes are the rules used by the match. Otherwise it reports an error at the farthest position where a token test or a not-predicate failed, a heuristic that usually points at the offending token.

When the recursion in the definition of $\mathrm{m}$ does not terminate, because of [left recursion](/left-recursion/) or a repetition $e^*$ whose $e$ matches the empty string, there is no result; the parser then stops with a report that the grammar is not well-formed. On a well-formed grammar this never happens.

## The algorithm

Number every subexpression of the grammar. The parser evaluates pairs $(e, i)$ of a subexpression and a position, and keeps every computed result in the table $\mathit{memo}$. For ordered choice it also records which alternative succeeded, so that the tree can be read back without searching.

```pseudo id=main
PACKRAT-PARSE(G, S, w)                    ▷ w = a1 ⋯ an
L1  memo ← empty table; far ← 0
L2  j ← EVAL(e_S, 0)
L3  if j = fail or j < n then error at far, or at max(far, j) when j < n
L4  return TREE(e_S, 0)

EVAL(e, i)                                ▷ the end of the match of e at i, or fail
L5  if memo has (e, i) then return memo[e, i]
L6  if (e, i) is being evaluated then stop: "left recursion"
L7  by the form of e:
L8      terminal a or any: if i < n and a(i+1) matches then r ← i + 1 else r ← fail, far ← max(far, i)
L9      nonterminal A: r ← EVAL(e_A, i)
L10     e1 ⋯ ek: r ← i; for each ej while r ≠ fail: r ← EVAL(ej, r)
L11     e1 / ⋯ / ek: r ← EVAL(ej, i) for the first j where it is not fail, and remember j; r ← fail if there is none
L12     e1*: r ← EVAL(e1, i); if r = fail then r ← i; else if r = i then stop: "empty repetition"; else r ← EVAL(e, r)
L13     !e1 or &e1: r ← i when EVAL(e1, i) fails for !, succeeds for &; otherwise r ← fail (and far ← max(far, i) for !)
L14 memo[e, i] ← r; return r
```

The tree is read from the table after a successful match. A node for rule $A$ at position $i$ is built once and shared if the tree needs it twice, which can only happen for empty matches.

```pseudo id=tree
TREE(e, i)                                ▷ the leaves and nodes produced by the match of e at i
L15 terminal or any: the token a(i+1)
L16 nonterminal A: one node A whose children are TREE(e_A, i)
L17 sequence, choice, repetition: TREE of the parts, at the positions stored in memo, using the remembered alternative of a choice and the stored iterations of a repetition
L18 ε, !e1, &e1: nothing
```

EVAL is written recursively, as in Ford's original Haskell code. The implementation below keeps the pairs being evaluated on an explicit stack, so the depth of the input does not touch the call stack.

## Example

Take the PEG

$$S \leftarrow A\, b \;/\; A\, c, \qquad A \leftarrow a\, A \;/\; a$$

and the input $a\, a\, c$, with positions $0, 1, 2, 3$. Matching $S$ at $0$ tries $A\, b$ first.

| step | pair | result | how |
|---|---|---|---|
| 1 | $A$ at 2 | fail | $a$ fails at 2 in both alternatives |
| 2 | $A$ at 1 | 2 | $a\, A$ fails since $A$ at 2 fails; then $a$ matches |
| 3 | $A$ at 0 | 2 | $a\, A$ with $A$ at 1 ending at 2 |
| 4 | $A\, b$ at 0 | fail | $A$ ends at 2, and $b$ fails at 2 |
| 5 | $A\, c$ at 0 | 3 | $A$ at 0 is a lookup giving 2, then $c$ matches |

The second alternative of $S$ asks for $A$ at $0$ again and gets the answer from the table. The parser computes 20 of the $12 \cdot 4 = 48$ pairs of a subexpression and a position, and returns the tree $[S \ [A \ a \ [A \ a]] \ c]$. A backtracking parser without the table would match $A$ at 0, 1 and 2 twice each.

The saving grows with nesting. Let $A_0 \leftarrow a$ and $A_j \leftarrow A_{j-1}\, x \;/\; A_{j-1}\, y$ for $1 \le j \le k$, on the input $a\, y^k$. Each $A_j$ matches $A_{j-1}$, fails on $x$, and matches $A_{j-1}$ again before $y$. Plain backtracking evaluates $A_0$ $2^k$ times. The packrat parser computes each pair once: for $k = 20$ it computes 141 pairs in total, against more than a million rule calls without the table.

**An error.** With $E \leftarrow T\, (+\, T)^*$, $T \leftarrow F\, (*\, F)^*$, $F \leftarrow (\, E\, ) \;/\; x$ and the start expression $E\, !.$, the input $x + * x$ fails: after $x +$, $T$ fails at position 2 on $*$, the repetition stops after the first $x$, and $!.$ fails at position 1. The farthest failure is at position 2, the token $*$.

## Correctness

The proof shows four facts. Every value stored in the table equals $\mathrm{m}(e, i)$, by induction on the order in which the pairs are finished, since each line from L8 to L13 is the clause of the semantics for its form and uses only values already finished. Each pair is evaluated at most once: after it is finished it is in the table, and while it is open a second request stops the run at L6. A stop at L6 or L12 means that the semantics itself needs $\mathrm{m}(e, i)$ in order to compute $\mathrm{m}(e, i)$, so there is no result; conversely, when $\mathrm{m}(e_S, 0)$ exists, its finite derivation has no such cycle and the parser never stops early. Finally TREE follows exactly the successful subcomputations, in order, and so returns the parse tree. The full proof is below.

## Complexity

Let $g$ be the number of subexpressions of the grammar.

- **Time.** Each pair $(e, i)$ with $0 \le i \le n$ is evaluated at most once, and an evaluation does work proportional to the number of children of $e$, plus one more step for a repetition. Lookups are charged to the evaluation that makes them. So EVAL takes $O(g \, (n + 1))$ time in total. TREE expands each node $(A, i)$ once, and each step of TREE belongs to one such expansion or to one iteration of a repetition, which consumes a token; so TREE takes $O(g \, (n + 1))$ time as well. The best case is a failure at the first token, $O(g)$ for compiling the grammar.
- **Space.** The table has at most $g \, (n + 1)$ entries, and the explicit stack holds at most that many open pairs. This is the main cost in practice: a table entry for every subexpression and every token can use far more memory than the input itself. Ford's implementation memoizes only the nonterminals, after rewriting repetitions and choices into rules, which gives the same bound with $g$ the number of rules of the rewritten grammar.
- **Without the table.** Plain backtracking takes $\Theta(2^k)$ time on the example above with an input of length $k + 1$.

## Properties

- **Deterministic.** A PEG has one result at each position, so the parser never chooses between parse trees: it returns the unique tree, and an ambiguous context-free grammar read as a PEG gets one of its readings, the one fixed by the order of the alternatives.
- **Not online.** A choice can look arbitrarily far ahead, and a later alternative can be tried after the input has been read to its end, so in general the whole input and the whole table must be kept until the end. Predicates give unlimited lookahead for free.
- **Linear for every well-formed PEG**, including grammars for languages that are not context-free, such as $\{a^n b^n c^n\}$.
- **No valid prefix property.** The farthest failure is a heuristic: the input before the reported position need not be the beginning of any accepted input.

## Variants and improvements

- **Selective memoization.** Memoize only some rules, or only rules that are tried more than once at a position. This keeps the linear bound in typical grammars while using much less memory; the bound is then lost in the worst case.
- **Cut operators.** A cut in an ordered choice tells the parser that the alternatives after it will not be tried, so table entries left of the cut can be dropped and the memory becomes bounded for many grammars (Mizushima, Maeda and Yamaguchi, 2010).
- **Left recursion.** Warth, Douglass and Millstein (2008) change the table so that a left-recursive rule is first seeded with $\mathsf{fail}$ and then re-evaluated while its match grows, which lets packrat parsers accept rules such as $E \leftarrow E + T \,/\, T$. The linear bound does not survive in general.
- **Incremental parsing.** Keeping the table between edits and invalidating only the entries whose matches overlap the edited region gives fast reparsing in editors.
- **Context-free grammars.** Packrat parsing does not parse context-free grammars: ordered choice commits to the first success. For general context-free grammars the memoizing top-down methods are [GLL parsing](/gll-parsing/) and the [Earley parser](/earley-parser/), in cubic time. For [LL(*)](/ll-star-parsing/) grammars, ANTLR uses memoization only on the decisions where it backtracks.

## When to use it

- When the grammar is written as a PEG, or as the ordered choices of a [parser combinator](/parser-combinators/) library, and backtracking makes the plain parser slow.
- Scannerless parsing, where the grammar describes the characters directly, needs unlimited lookahead for keywords and identifiers, and benefits from not having a separate lexer.
- When memory is not a concern: the table can be many times the size of the input. For an LL(1) or LR grammar a deterministic [top-down](/top-down-parsing/) or bottom-up parser does the same job in constant memory per token.

## Pitfalls

- **Left recursion.** $E \leftarrow E + T \,/\, T$ makes $E$ at $i$ ask for $E$ at $i$. A recursive parser without a check loops until its stack overflows; rewrite with repetition, $E \leftarrow T\, (+\, T)^*$, or use the left-recursion variant.
- **Order of alternatives.** $S \leftarrow a \,/\, a\, b$ never matches $a\, b$ as a whole: put the longer alternative first. Ordered choice silently hides an alternative that a context-free grammar would accept.
- **State and side effects.** The table is correct only if the result of a rule depends on the rule and the position alone. Semantic actions with side effects, or rules that depend on a symbol table, break the memoization unless their state is part of the key.
- **Error messages.** A failed parse usually ends with a failure at position 0 of the start rule. Without the farthest-failure position, or the set of tokens expected there, the error message is useless.
- **Memory.** A table of all pairs $(e, i)$ in a hash map needs far more memory than the input. Store only nonterminals, and use arrays indexed by position.

## Implementations

## History

Birman and Ullman studied the formalisms TS and gTS, later called TDPL and GTDPL, in Birman's 1970 thesis and their 1973 paper, and showed that a table of the results of every nonterminal at every position recognizes these languages in linear time; Aho and Ullman included the method in their 1972 book, but it remained a theoretical device because the table was too large for the memories of the time. Ford (2002) implemented the idea as a lazy table in Haskell, called it packrat parsing, and showed that it handles practical grammars, including scannerless ones, in linear time. In 2004 he defined parsing expression grammars as the formal language behind it. Packrat parsing then spread to many parser generators; Python's parser since version 3.9 is a PEG parser with memoization.

## References
