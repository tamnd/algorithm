---
tag: 37Z7NT
kind: algorithm
slug: lr0-parsing
name: LR(0) parsing
area: automata-and-parsing/context-free-parsing
level: core
summary: Shift-reduce parser whose states come from LR(0) items without lookahead.
solves: [cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the number of input tokens, g: the grammar size, N: the number of LR(0) states}
  time: {worst: O(n), build: O(N g^2)}
  space: {extra: O(n), table: O(N g)}
properties: {deterministic: true, recursive: false}
history:
  year: 1965
  people: [Donald E. Knuth]
  note: Knuth defined LR(k) parsing for every k, including k = 0; DeRemer later built the practical SLR and LALR parsers on the LR(0) automaton.
prereqs: [lr-item, shift-reduce-parsing, handle]
see_also: [slr-parsing, lalr-parsing, canonical-lr-parsing, lr-parse-table, lr-grammar, viable-prefix, lr-item-sets, shift-reduce-conflict]
sources:
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.6.2, Items and the LR(0) Automaton; Section 4.6.3, The LR-Parsing Algorithm
  - book: isbn:9780521820608
    title: Andrew W. Appel and Jens Palsberg, Modern Compiler Implementation in Java, second edition
    locator: Section 3.3, LR Parsing (LR(0) parser generation with the production S' → S $)
  - paper: doi:10.1145/362619.362625
    title: Frank L. DeRemer, Simple LR(k) grammars, Communications of the ACM 14(7) (1971)
    locator: pp. 453 to 460 (lookahead added to the LR(0) automaton)
---

LR(0) parsing is the simplest [LR parsing](/lr-parsing/) method: a [shift-reduce](/shift-reduce-parsing/) parser whose states are the sets of [LR(0) items](/lr-item/) of the grammar, and whose decision to shift or to reduce depends on the state alone, never on the next token. It works for the grammars whose LR(0) automaton has no conflict, and then it parses in linear time and stops at the first token that cannot continue a sentence. Few practical grammars are LR(0), but its automaton is the skeleton of [SLR](/slr-parsing/) and [LALR](/lalr-parsing/) parsers, which only add lookahead to its complete items.

## In plain words

The parser reads tokens from left to right and keeps a stack. At each step it either pushes the next token, or it notices that the top of the stack is the whole right side of a grammar rule and replaces it by the rule's name. At the end, the stack must hold just the start symbol.

The hard part is to know when the top of the stack is a complete rule that should be replaced. LR(0) parsing answers this with a small machine built in advance from the grammar. Each state of the machine sums up what the stack holds. In a state where a rule has just been completed, the parser replaces it; in every other state it reads. It never peeks at the coming token to decide, which is what the 0 means.

## The problem

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. This page augments the grammar with a new start symbol $S'$ and the production $S' \to S \, \$$, where $\$ \notin \Sigma$ is an end marker that the parser shifts like a token.

The input is a grammar $G$ and tokens $w = a_1 \cdots a_n$. The output is a [parse tree](/parse-tree/) of $w$ with root $S$, or an error at the first token that cannot continue a sentence. The method applies when the augmented grammar is LR(0), that is, when the table built below has no conflict; see [LR(k) grammar](/lr-grammar/) for the definition and for the version without $\$$.

## The algorithm

The construction first removes the productions that use a nonterminal deriving no terminal string; they cannot occur in a parse tree of a sentence. Then it builds the LR(0) automaton by a breadth-first search over the item sets, with the CLOSURE and GOTO operations of the [LR item](/lr-item/) page, and gives each state one action.

```pseudo id=build
BUILD-LR0(G)                                 ▷ G augmented with S' → S $
B1  I0 ← CLOSURE({S' → ·S $}); C ← the list (I0)
B2  for each state I in C, in order, and each symbol X after a dot in I do
B3      J ← GOTO(I, X); if J is not in C then append J to C
B4      record the transition GOTO[I, X] = J
B5  for each state I in C do
B6      if I has two complete items, or a complete item and an item A → α·aβ with a a terminal, then report a conflict
B7      if I contains S' → S $· then ACTION[I] ← accept
B8      else if I contains a complete item A → β· then ACTION[I] ← reduce A → β
B9      else ACTION[I] ← shift
```

The parser keeps a stack of states, and for each state above the bottom one the tree of the symbol that led into it.

```pseudo id=main
LR0-PARSE(w)
L1  push state 0; append $ to w; i ← 1
L2  loop
L3      q ← the top state; act ← ACTION[q]
L4      if act = shift then
L5          if GOTO[q, w_i] is undefined then report an error at token i
L6          push GOTO[q, w_i] and the leaf w_i; i ← i + 1
L7      else if act = accept then return the tree of S below $ (an error if $ was not the last token)
L8      else act = reduce A → β:
L9          pop |β| states and their trees; make the node A with these trees as its children
L10         push GOTO[top state, A] and the new node
```

The state on top of the stack is the set of items valid for the string of symbols on the stack, by Knuth's theorem on the [LR item](/lr-item/) page. A complete item $A \to \beta \cdot$ in it means the top of the stack is $\beta$, the [handle](/handle/), so line L9 can pop it. Line L10 then moves from the state below $\beta$ over $A$, exactly as if $A$ had been read. With an empty right side, line L9 pops nothing and line L10 pushes a node with no children.

## Example

Take $S \to ( L ) \mid x$, $L \to S \mid L , S$, augmented with $S' \to S \, \$$. The automaton has 10 states:

| state | items | action |
|---|---|---|
| 0 | $S' \to \cdot S \$$, $S \to \cdot ( L )$, $S \to \cdot x$ | shift |
| 1 | $S \to ( \cdot L )$, $L \to \cdot S$, $L \to \cdot L , S$, $S \to \cdot ( L )$, $S \to \cdot x$ | shift |
| 2 | $S \to x \cdot$ | reduce $S \to x$ |
| 3 | $S' \to S \cdot \$$ | shift |
| 4 | $S \to ( L \cdot )$, $L \to L \cdot , S$ | shift |
| 5 | $L \to S \cdot$ | reduce $L \to S$ |
| 6 | $S' \to S \$ \cdot$ | accept |
| 7 | $S \to ( L ) \cdot$ | reduce $S \to ( L )$ |
| 8 | $L \to L , \cdot S$, $S \to \cdot ( L )$, $S \to \cdot x$ | shift |
| 9 | $L \to L , S \cdot$ | reduce $L \to L , S$ |

The transitions are $0 \xrightarrow{(} 1$, $0 \xrightarrow{x} 2$, $0 \xrightarrow{S} 3$, $1 \xrightarrow{(} 1$, $1 \xrightarrow{x} 2$, $1 \xrightarrow{S} 5$, $1 \xrightarrow{L} 4$, $3 \xrightarrow{\$} 6$, $4 \xrightarrow{)} 7$, $4 \xrightarrow{,} 8$, $8 \xrightarrow{(} 1$, $8 \xrightarrow{x} 2$, $8 \xrightarrow{S} 9$. No state has a conflict, so the grammar is LR(0). The parse of $( x , x )$:

| step | states | symbols | input | action |
|---|---|---|---|---|
| 1 | 0 | | $( x , x ) \$$ | shift |
| 2 | 0 1 | $($ | $x , x ) \$$ | shift |
| 3 | 0 1 2 | $( x$ | $, x ) \$$ | reduce $S \to x$ |
| 4 | 0 1 5 | $( S$ | $, x ) \$$ | reduce $L \to S$ |
| 5 | 0 1 4 | $( L$ | $, x ) \$$ | shift |
| 6 | 0 1 4 8 | $( L ,$ | $x ) \$$ | shift |
| 7 | 0 1 4 8 2 | $( L , x$ | $) \$$ | reduce $S \to x$ |
| 8 | 0 1 4 8 9 | $( L , S$ | $) \$$ | reduce $L \to L , S$ |
| 9 | 0 1 4 | $( L$ | $) \$$ | shift |
| 10 | 0 1 4 7 | $( L )$ | $\$$ | reduce $S \to ( L )$ |
| 11 | 0 3 | $S$ | $\$$ | shift |
| 12 | 0 3 6 | $S \$$ | | accept |

The reductions, read from the bottom up, are the rightmost derivation $S \Rightarrow ( L ) \Rightarrow ( L , S ) \Rightarrow ( L , x ) \Rightarrow ( S , x ) \Rightarrow ( x , x )$. On the input $( x \, x$ the parser reaches state 4 after $( x$ and finds no transition on the second $x$, so it reports an error at token 3, the first token that no sentence allows there.

## Correctness

Each state on the stack is the set of items valid for the symbols below and including it, so a reduction always pops a real handle and builds a correct tree node. When the input is a sentence, the reverse of its rightmost derivation is a run of the parser: at a handle the state has the complete item of that handle, and because the table has no conflict, the parser can only reduce by it; before the handle the next token can be shifted, so the state has a shift item and no complete item. Since the actions depend only on the tokens already shifted, an error at a token means that no sentence continues the shifted tokens with it. The number of steps is linear because an unambiguous grammar has no node above a node of the same nonterminal and the same yield in a tree, and because the parser cannot push more than $N$ empty subtrees in a row without looping. The full proof is below.

## Complexity

- **Parsing.** Every step creates one tree node: a leaf for a shift, an inner node for a reduction. The proof shows that the run on $n$ tokens creates at most $c \, (n + 2)$ nodes, where $c$ depends only on the grammar. Each step costs $O(1)$ for a fixed grammar, plus the length of the popped right side. So parsing takes $O(n)$ time and $O(n)$ space for the stack and the tree.
- **Building.** There are $|G| + 3$ LR(0) items, counting those of $S' \to S \$$, so there are at most $2^{|G| + 3}$ states $N$. Each closure takes $O(|G|)$ time with the productions grouped by left side, and each state has at most $|G|$ successors, so the build takes $O(N |G|^2)$ time and the table, with one action and at most $|G|$ transitions per state, takes $O(N |G|)$ space. For the grammars on this page $N$ is small, but it can grow exponentially with the grammar.

| quantity | bound |
|---|---|
| parse time | $O(n)$ |
| parse space | $O(n)$ |
| build time | $O(N \lvert G \rvert^2)$ |
| table size | $O(N \lvert G \rvert)$ |

## Properties

- **Valid prefix property.** The parser reports an error at the first token $a_i$ such that $a_1 \cdots a_i$ is not a prefix of a sentence.
- **No lookahead.** Reductions happen before the next token is examined, so an LR(0) parser can act as soon as a token arrives, which suits interactive input.
- **Left recursion is welcome.** $L \to L , S$ keeps the stack short: the parser reduces after each element. Right recursion such as $L \to S , L$ needs lookahead to decide when the list ends, and is not LR(0) here.
- **Grammar class.** LR(0) with $S' \to S \$$ is the weakest of the LR methods: every such grammar is SLR(1), LALR(1) and LR(1).
- **Unambiguous.** A grammar with a conflict-free LR(0) table is unambiguous, because the parser's run on a sentence is unique and determines the tree.

## Variants and improvements

- **Strict LR(0).** Without the end marker, $S' \to S \cdot$ is a complete item, and a state with it and a shift item is a conflict. Then only languages in which no sentence is a proper prefix of another can be parsed. The [LR(k) grammar](/lr-grammar/) page discusses both versions.
- **SLR(1).** Keep the automaton, but reduce by $A \to \beta$ only when the next token is in FOLLOW$(A)$. This resolves the conflicts of the expression grammar. See [SLR parsing](/slr-parsing/).
- **LALR(1).** Keep the automaton and compute exact lookaheads for its complete items. This is the method of [yacc](/yacc/) and Bison. See [LALR parsing](/lalr-parsing/).
- **Canonical LR(1).** Put the lookahead into the items themselves, which can multiply the number of states. See [canonical LR parsing](/canonical-lr-parsing/).
- **GLR.** When conflicts remain, run all actions and split the stack. See [GLR parsing](/glr-parsing/).

## When to use it

Use LR(0) parsing for small machine-designed languages where every construct has its own closing token, for teaching, and as the first stage of an SLR or LALR parser generator. For a typical programming language grammar it has conflicts, and SLR or LALR is the practical choice.

## Pitfalls

- **Empty productions.** A production $A \to \varepsilon$ gives the complete item $A \to \cdot$ in every state that predicts $A$, and it conflicts with any shift item there. $S \to a S b \mid \varepsilon$ is not LR(0) for this reason, while $S \to S a \mid \varepsilon$ is.
- **Forgetting the end marker.** If the parser accepts as soon as the stack holds $S$, it accepts prefixes of sentences. With $S' \to S \$$ it accepts only when the input ends.
- **Unproductive nonterminals.** A nonterminal that derives no terminal string can create a conflict in a state that no sentence ever reaches; remove such productions before building the table.
- **Recursion.** The driver is a loop over an explicit stack; a recursive implementation of the tree building can overflow on long inputs.

## Implementations

## History

Knuth (1965) introduced LR(k) grammars and their parsers, with LR(0) as the case $k = 0$. His construction for general $k$ produced very large tables, and LR parsing became practical only after DeRemer (1969 thesis, 1971 paper) showed that the LR(0) automaton plus lookahead sets for its complete items handles most programming language grammars. That is the SLR method, and LALR, used by yacc, refines its lookaheads.

## References
