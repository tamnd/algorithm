---
tag: DYEHVA
kind: algorithm
slug: ll1-parsing
name: LL(1) table-driven parsing
aliases:
- LL parsing
- LL(1) parsing
- predictive parsing
- table-driven top-down parsing
area: automata-and-parsing/context-free-parsing
level: core
summary: Deterministic top-down parser that uses a parse table indexed by nonterminal and lookahead.
solves: [cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the number of input tokens, the grammar being fixed}
  time: {worst: O(n), best: O(1)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1968
  people: [Philip M. Lewis II, Richard E. Stearns]
  note: Lewis and Stearns defined the LL(k) grammars, the class that a deterministic top-down parser with k tokens of lookahead handles; the stack and table driver is the textbook form of the case k = 1.
prereqs: [ll-parse-table, leftmost-derivation, pushdown-automaton]
see_also: [ll-grammar, top-down-parsing, recursive-descent-parsing, ll-k-parsing, ll-star-parsing, lr-parsing, left-recursion-elimination, panic-mode-error-recovery]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.4.4, Nonrecursive Predictive Parsing (the driver and its trace on id + id * id); Section 4.4.3, LL(1) Grammars
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 8, Deterministic Top-Down Parsing (Section 8.2, LL(1) Parsing)
  - book: isbn:9780521820608
    title: Andrew W. Appel and Jens Palsberg, Modern Compiler Implementation in Java, second edition
    locator: Section 3.2, Predictive Parsing
  - paper: doi:10.1145/321466.321477
    title: P. M. Lewis II and R. E. Stearns, Syntax-directed transduction, Journal of the ACM 15(3) (1968)
    locator: pp. 465 to 488 (the definition of LL(k) grammars)
---

LL(1) parsing reads the input from left to right and builds its [leftmost derivation](/leftmost-derivation/) with one token of lookahead and no backtracking. It keeps a stack of the grammar symbols that remain to be matched, and when a nonterminal is on top it looks up the production to use in the [LL parse table](/ll-parse-table/) at the row of the nonterminal and the column of the next token. For an [LL(1) grammar](/ll-grammar/) it accepts exactly the sentences of the grammar, builds their [parse trees](/parse-tree/), and runs in time linear in the length of the input.

## In plain words

The parser holds a to-do list of grammar symbols, with the start symbol alone at first. It looks at the first item of the list and the next word of the input. If the item is a word, it must be the same word: the parser crosses both off. If the item is a placeholder, the parser asks the table which rule to use for this placeholder when this word comes next, and replaces the placeholder by the symbols of the rule.

The table always gives at most one answer, so the parser never guesses and never goes back. If the table has no answer, or a word does not match, the input has an error at this word. When the list and the input run out together, the input is a sentence of the grammar, and the rules that were used form its parse tree.

## The problem

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. The end marker $\$ \notin V \cup \Sigma$ marks the end of the input.

The input is a grammar $G$ and a string $w = a_1 \cdots a_n$ of tokens. The output is a parse tree of $w$ with root $S$ if $w \in L(G)$, and otherwise an error at a token position. This is the [CFG parsing problem](/cfg-parsing-problem/) restricted to LL(1) grammars.

The parser needs the table $M$ with one cell for each $A \in V$ and each $a \in \Sigma \cup \{\$\}$. As on the [LL parse table](/ll-parse-table/) page, $M[A, a]$ holds the productions $A \to \alpha$ with $a \in \mathrm{PREDICT}(A \to \alpha)$, where $\mathrm{PREDICT}(A \to \alpha)$ is $\mathrm{FIRST}(\alpha)$, together with $\mathrm{FOLLOW}(A)$ when $\alpha$ is [nullable](/nullable-symbol/). The grammar is *LL(1)* when no cell has two productions. We also assume that every nonterminal derives some terminal string, which [useless symbol elimination](/useless-symbol-elimination/) ensures; without it a parser can loop on a symbol that derives nothing.

## The algorithm

The parser is a deterministic [pushdown automaton](/pushdown-automaton/) with one state. Each stack entry is a grammar symbol together with the tree node that will receive its subtree.

```pseudo id=main
LL1-PARSE(G, M, w)                       ▷ M = the LL(1) table of G, w = a1 ⋯ an
L1  w ← a1 ⋯ an $; i ← 1
L2  push $, then S with a dummy root as its parent
L3  loop
L4      pop (X, parent) from the stack
L5      if X = $ then if i = n + 1 then accept and return the tree, else error
L6      if X is a terminal then
L7          if X ≠ ai then error
L8          add the leaf X to parent; i ← i + 1
L9      else
L10         p ← M[X, ai]
L11         if p is empty then error
L12         let p be X → Y1 ⋯ Yk; add a new node X to parent
L13         push Yk, …, Y1 with the new node as their parent, so that Y1 is on top
```

Lines L6 to L8 *match* a token, and lines L10 to L13 *expand* a nonterminal. An expansion with $k = 0$ pushes nothing, and the node gets no children, which stands for the single child $\varepsilon$. The sequence of productions chosen at line L10 is the left parse of $w$, the list of steps of its leftmost derivation. When the table is not given, it is built first with the method of the [LL parse table](/ll-parse-table/) page, which also reports the conflicts that make a grammar not LL(1).

## Example

Take the expression grammar without left recursion, with its productions numbered:

$$\begin{array}{llll} 0: E \to T E' & 1: E' \to + T E' & 2: E' \to \varepsilon & 3: T \to F T' \\ 4: T' \to * F T' & 5: T' \to \varepsilon & 6: F \to ( E ) & 7: F \to id \end{array}$$

Its table is:

| | id | + | * | ( | ) | \$ |
|---|---|---|---|---|---|---|
| $E$ | 0 | | | 0 | | |
| $E'$ | | 1 | | | 2 | 2 |
| $T$ | 3 | | | 3 | | |
| $T'$ | | 5 | 4 | | 5 | 5 |
| $F$ | 7 | | | 6 | | |

The parser on $id + id * id$, with the top of the stack on the left:

| step | stack | rest of the input | action |
|---|---|---|---|
| 1 | $E \ \$$ | $id + id * id \ \$$ | expand by 0, $E \to T E'$ |
| 2 | $T \ E' \ \$$ | $id + id * id \ \$$ | expand by 3, $T \to F T'$ |
| 3 | $F \ T' \ E' \ \$$ | $id + id * id \ \$$ | expand by 7, $F \to id$ |
| 4 | $id \ T' \ E' \ \$$ | $id + id * id \ \$$ | match $id$ |
| 5 | $T' \ E' \ \$$ | $+ id * id \ \$$ | expand by 5, $T' \to \varepsilon$ |
| 6 | $E' \ \$$ | $+ id * id \ \$$ | expand by 1, $E' \to + T E'$ |
| 7 | $+ \ T \ E' \ \$$ | $+ id * id \ \$$ | match $+$ |
| 8 | $T \ E' \ \$$ | $id * id \ \$$ | expand by 3, $T \to F T'$ |
| 9 | $F \ T' \ E' \ \$$ | $id * id \ \$$ | expand by 7, $F \to id$ |
| 10 | $id \ T' \ E' \ \$$ | $id * id \ \$$ | match $id$ |
| 11 | $T' \ E' \ \$$ | $* id \ \$$ | expand by 4, $T' \to * F T'$ |
| 12 | $* \ F \ T' \ E' \ \$$ | $* id \ \$$ | match $*$ |
| 13 | $F \ T' \ E' \ \$$ | $id \ \$$ | expand by 7, $F \to id$ |
| 14 | $id \ T' \ E' \ \$$ | $id \ \$$ | match $id$ |
| 15 | $T' \ E' \ \$$ | $\$$ | expand by 5, $T' \to \varepsilon$ |
| 16 | $E' \ \$$ | $\$$ | expand by 2, $E' \to \varepsilon$ |
| 17 | $\$$ | $\$$ | accept |

The left parse is $0, 3, 7, 5, 1, 3, 7, 4, 7, 5, 2$, eleven expansions for eleven inner nodes of the tree. In bracket notation the tree is

$$[E \ [T \ [F \ id] \ [T' \ \varepsilon]] \ [E' \ + \ [T \ [F \ id] \ [T' \ * \ [F \ id] \ [T' \ \varepsilon]]] \ [E' \ \varepsilon]]].$$

At step 5 the lookahead $+$ selects $T' \to \varepsilon$, a choice that comes from $+ \in \mathrm{FOLLOW}(T')$. On the input $id + )$ the parser matches $id$ and $+$, expands $T$ with the lookahead $)$, finds the cell $M[T, )]$ empty, and reports an error at the third token.

## Correctness

Let $G$ be LL(1), with every nonterminal productive. The claim is: LL1-PARSE accepts $w$ if and only if $w \in L(G)$, the tree it returns is a parse tree of $w$, and it always stops. The proof rests on one invariant: after the parser has matched $a_1 \cdots a_{i-1}$, the stack, read from the top, holds a string $\gamma$ with $S \Rightarrow_{lm}^* a_1 \cdots a_{i-1} \gamma$, and the tree built so far is the tree of this derivation. If the parser accepts, the stack is empty, so $S \Rightarrow^* w$ and the tree is a parse tree of $w$. If $w \in L(G)$, fix its parse tree $t$; whenever a nonterminal $X$ is on top, its node in $t$ uses a production $p$, and the next token is in $\mathrm{PREDICT}(p)$: it is the first token of the subtree's yield, or, when that yield is empty, a token that follows $X$ in a sentential form. Since $M[X, a_i]$ has only one production, it is $p$, so the parser follows $t$ and accepts. For termination, an LL(1) grammar whose nonterminals are productive is not left-recursive, so between two matches no nonterminal is expanded twice on one path of the tree. The full proof is below.

## Complexity

Each step either matches a token, which happens $n$ times, or expands a nonterminal, which creates an inner node of the tree. The proof of correctness shows that the tree built on any input, accepted or not, has at most $c \cdot (n + 1)$ inner nodes, where $c$ depends only on $G$. So:

- **Time.** $O(n)$ steps for a fixed grammar, each with one table lookup and $O(1)$ stack operations for each pushed symbol, so $O(n)$ time on the [word RAM](/word-ram/). If the first token has an empty cell in row $S$, the parser stops after $O(1)$ steps. Building the table costs $O(|V| \sigma^2 |G|)$ once, with $\sigma = |\Sigma| + 1$, independent of $w$.
- **Space.** The stack and the tree take $O(n)$ space. A recognizer that does not build the tree needs only the stack, whose height can still grow linearly: with $S \to a S b \mid \varepsilon$, after the $a$'s of $a^n b^n$ the stack holds $n$ copies of $b$.

The constant $c$ can be large for grammars with long chains of nullable or single-child productions. For the expression grammar each token gives at most a handful of expansions.

## Properties

- **Deterministic and online.** The parser makes no guesses and never backtracks, and it reads each token once, from left to right. It needs only the next token at each step, so it can work on a stream.
- **Valid prefix property.** When the parser reports an error at token $a_i$, the tokens $a_1 \cdots a_{i-1}$ are a prefix of some sentence of $L(G)$, and $a_1 \cdots a_i$ is not. So the error is reported at the first token at which the input stops being the start of a sentence. Error messages can list the expected tokens: the nonempty cells of the row of the top nonterminal.
- **Left parse.** The output is the leftmost derivation, in the order of a preorder walk of the tree. A [syntax-directed translation](/syntax-directed-translation/) can run its actions in this order while the parse goes on.
- **Empty productions.** A production $A \to \varepsilon$ is used when the next token is in $\mathrm{FOLLOW}(A)$. This decision is sometimes made on a token that is not in the language at that point: with the table above, the input $id \ )$ expands $T' \to \varepsilon$ and $E' \to \varepsilon$ on the token $)$, and finds the error only when $\$$ comes to the top of the stack. The valid prefix property still holds, because those expansions match no token.

## Variants and improvements

- **Recursive descent.** A [recursive descent parser](/recursive-descent-parsing/) puts the table into code: one function for each nonterminal, which switches on the next token. The call stack replaces the explicit stack, which is easier to write by hand but can overflow on deeply nested input.
- **More lookahead.** [LL(k) parsing](/ll-k-parsing/) looks at $k$ tokens. [LL(*) parsing](/ll-star-parsing/) looks ahead as far as needed with a finite automaton for each decision, and falls back to backtracking when even that fails.
- **Error recovery.** [Panic-mode error recovery](/panic-mode-error-recovery/) lets the parser go on after an error: it skips tokens until one in a synchronizing set, usually $\mathrm{FOLLOW}(A)$ for the nonterminal $A$ on top, and then pops $A$.
- **Default reductions.** An empty cell in a row that has a production with a nullable right side can be filled with it. The table compresses better, and the valid prefix property still holds because the error is found before the next match.
- **Making a grammar LL(1).** [Left recursion elimination](/left-recursion-elimination/) and [left factoring](/left-factoring/) turn many grammars into LL(1) form, as was done for the expression grammar above.

## When to use it

Use LL(1) parsing when the grammar is LL(1) or close to it, and you want a small fast parser, good error messages, and semantic actions that run during the parse. Many programming languages are designed so that a hand-written recursive descent parser, the code form of this table, can parse them. For grammars with left recursion or that need more lookahead, use [LR parsing](/lr-parsing/), which handles all LL(1) grammars and more, or a generator for [LL(*)](/ll-star-parsing/). For ambiguous grammars, use a general method such as the [Earley parser](/earley-parser/).

## Pitfalls

- **Left-recursive grammars.** A production $E \to E + T$ puts $E \to E + T$ and $E \to T$ in the same cells, so BUILD reports a conflict. Run [left recursion elimination](/left-recursion-elimination/) first.
- **Accepting with input left.** At line L5, check that all tokens were used. A driver that accepts as soon as the stack holds only $\$$ accepts every string that starts with a sentence.
- **The empty input.** With $w = \varepsilon$, the first lookahead is $\$$, and the parser must expand nullable productions on it. The column $\$$ of the table must be filled from $\mathrm{FOLLOW}$, with $\$ \in \mathrm{FOLLOW}(S)$.
- **Order of the pushed symbols.** Line L13 pushes the right side in reverse, so that its first symbol is on top. Pushing it in order parses the mirror image.
- **Unproductive symbols.** If some nonterminal derives no terminal string, a conflict-free table can still send the parser into a loop or into a dead end that the valid prefix property excludes. Remove such symbols before building the table.

## Implementations

## History

Lewis and Stearns (1968) defined the LL(k) grammars as those parsed by a deterministic top-down transducer with $k$ tokens of lookahead, and Rosenkrantz and Stearns (1970) studied their properties, among them the decidability of the LL(k) condition and the fact that each LL(k) language is deterministic. Knuth (1971) related top-down parsing with lookahead to recursive procedures. The table and stack driver with FIRST and FOLLOW sets is the form that the compiler textbooks present, for example Aho, Lam, Sethi and Ullman, and Appel.

## References
