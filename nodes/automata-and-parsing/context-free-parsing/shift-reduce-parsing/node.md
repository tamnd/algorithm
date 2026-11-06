---
tag: PZXCZZ
kind: algorithm
slug: shift-reduce-parsing
name: Shift-reduce parsing
aliases:
- bottom-up parsing
- shift-reduce parser
area: automata-and-parsing/context-free-parsing
level: core
summary: Bottom-up parsing using a stack, shifting input and reducing handles to nonterminals.
solves: [cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the number of input tokens, r: the number of reductions, which is the number of inner nodes of the parse tree}
  time: {worst: O(n + r), best: Θ(1)}
  space: {extra: O(n + r)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1965
  people: [Donald E. Knuth]
  note: Floyd's operator precedence parser of 1963 was a shift-reduce parser for a restricted class of grammars; Knuth's LR(k) paper of 1965 defined handles and viable prefixes and showed how to choose each move with a finite automaton and k tokens of lookahead.
prereqs: [bottom-up-parsing, stack, sentential-form]
see_also: [handle, viable-prefix, shift-reduce-conflict, reduce-reduce-conflict, lr-parsing, slr-parsing, lalr-parsing, operator-precedence-parsing]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.5, Bottom-Up Parsing (4.5.1 Reductions, 4.5.2 Handle Pruning, 4.5.3 Shift-Reduce Parsing, 4.5.4 Conflicts During Shift-Reduce Parsing); Section 4.6.3, The LR-Parsing Algorithm
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 3.2, Two Ways to Parse a Sentence; Chapter 7, General Directional Bottom-Up Parsing; Chapter 9, Deterministic Bottom-Up Parsing
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (handles, the LR(k) condition, and the parsing automaton)
  - paper: doi:10.1145/321172.321179
    title: Robert W. Floyd, Syntactic analysis and operator precedence, Journal of the ACM 10(3) (1963)
    locator: pp. 316 to 333 (precedence relations that decide when to reduce)
---

Shift-reduce parsing is the standard form of [bottom-up parsing](/bottom-up-parsing/). The parser keeps a [stack](/stack/) of grammar symbols and reads the input from left to right. At each step it either *shifts* the next token onto the stack or *reduces* the right side $\beta$ of a production $A \to \beta$ on top of the stack to $A$, building a node of the [parse tree](/parse-tree/). It accepts when the input is used up and the stack holds only the start symbol. The reductions, read backwards, are a rightmost [derivation](/derivation/) of the input. The driver is the same for all bottom-up methods; they differ only in how they decide the move. With the tables of [LR parsing](/lr-parsing/) the decision takes constant time and the whole parse takes linear time.

## In plain words

Read the tokens one by one and put each on a pile. Every time the top of the pile spells the right side of a grammar rule, such as "expression plus term", you may take those pieces off and put back the single piece "expression". That piece remembers the pieces it replaced. If the whole input has been read and the pile holds one piece, the start symbol, the input is a sentence.

The hard part is the decision. When the top of the pile matches a rule, combining at once can be wrong: in `a + b * c`, after `a + b`, combining the sum is a mistake, because `b` belongs to the product. A shift-reduce parser needs a rule that tells it, from the pile and the next token, whether to read on or to combine, and with which rule.

## The problem

We use the notation of the [context-free grammar](/context-free-grammar/) page: a grammar $G = (V, \Sigma, P, S)$, productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. The input is $w = a_1 \cdots a_n$, followed by the end marker $a_{n+1} = \$$. The output is a [parse tree](/parse-tree/) of $w$, or an error if $w \notin L(G)$ ([the parsing problem](/cfg-parsing-problem/)).

A *configuration* is a pair $(\gamma, a_{pos} \cdots a_n)$: the stack $\gamma \in (V \cup \Sigma)^*$, written with its top on the right, and the rest of the input. The parser starts at $(\varepsilon, w)$ and should end at $(S, \varepsilon)$.

## The algorithm

```pseudo id=main
SHIFT-REDUCE(G, w, DECIDE)
L1  stack ← empty;  pos ← 1
L2  loop
L3      act ← DECIDE(stack, a_pos …)               ▷ shift, reduce by A → β, accept, or error
L4      if act = shift then
L5          push the leaf a_pos;  pos ← pos + 1
L6      else if act = reduce by A → β then
L7          pop the |β| trees x_1 … x_k on top      ▷ their roots spell β
L8          push the tree node(A, x_1 … x_k)
L9      else if act = accept then return the tree on the stack
L10     else error
```

Each stack entry is a tree whose root is a grammar symbol, so the stack is a sequence of finished subtrees, and its symbols are the roots. A reduction by $A \to \varepsilon$ pops nothing and pushes a leafless node $A$. DECIDE may only accept when the stack is $S$ and pos is $n + 1$.

**The decision.** A run is correct when every reduction undoes the last step of a rightmost derivation, that is, when it reduces a [handle](/handle/). Because everything to the right of a handle in a right sentential form is terminal, the handle of a correct run is always on top of the stack, never buried inside it, which is why a stack suffices. The symbol strings that can be on the stack in a correct run are the [viable prefixes](/viable-prefix/). The methods differ in DECIDE:

- [Operator precedence parsing](/operator-precedence-parsing/) compares the topmost terminal of the stack with the next token by a table of precedence relations.
- [LR(0)](/lr0-parsing/), [SLR(1)](/slr-parsing/), [LALR(1)](/lalr-parsing/) and [canonical LR(1)](/canonical-lr-parsing/) parsers run a finite automaton over the stack, which recognizes the viable prefixes, and look at the next token. They keep the automaton states on the stack next to the symbols, so each decision takes $O(1)$ time.
- [GLR parsing](/glr-parsing/) does not decide: it follows every possible move at once.

A grammar for which a method's DECIDE never has two possible moves is accepted by the method; otherwise the method reports a [shift-reduce conflict](/shift-reduce-conflict/) or a [reduce-reduce conflict](/reduce-reduce-conflict/).

**An exact decision for every grammar.** The implementation of this page pairs the driver with a decision procedure that works for every context-free grammar, including ambiguous ones and ones with $\varepsilon$-productions and cycles, at the price of looking at the whole input. It calls a configuration *good* if some sequence of moves leads from it to accept. A stack $X_1 \cdots X_m$ is good at position pos exactly when it splits as $\beta_1 \cdots \beta_k$ for a chain of [items](/lr-item/) $[S' \to \beta_1 \cdot A_2 \delta_1]$, $[A_2 \to \beta_2 \cdot A_3 \delta_2]$, ..., $[A_k \to \beta_k \cdot \delta_k]$ with $\delta_k \delta_{k-1} \cdots \delta_1 \Rightarrow^* a_{pos} \cdots a_n$: the chain is the path from the root of the future parse tree down to the node being built. The procedure shifts if the shifted configuration is good, and otherwise takes the first move of a shortest sequence of good reductions after which a shift, or accept, is good. It is a reference, slow but correct; real parsers use a table.

## Example

The expression grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (\,E\,) \mid \mathtt{id}$ on the input $\mathtt{id} + \mathtt{id} * \mathtt{id}$. The moves, as produced by the implementation:

| stack | rest of the input | move |
|---|---|---|
| (empty) | id + id * id | shift |
| id | + id * id | reduce $F \to \mathtt{id}$ |
| F | + id * id | reduce $T \to F$ |
| T | + id * id | reduce $E \to T$ |
| E | + id * id | shift |
| E + | id * id | shift |
| E + id | * id | reduce $F \to \mathtt{id}$ |
| E + F | * id | reduce $T \to F$ |
| E + T | * id | shift |
| E + T * | id | shift |
| E + T * id | (empty) | reduce $F \to \mathtt{id}$ |
| E + T * F | (empty) | reduce $T \to T * F$ |
| E + T | (empty) | reduce $E \to E + T$ |
| E | (empty) | accept |

There are 5 shifts, one for each token, and 8 reductions, one for each inner node of the tree. In the row with stack $E + T$ and next token $*$, the top matches the right side of $E \to E + T$, but reducing would give the stack $E$ before $* \, \mathtt{id}$, and no right sentential form starts with $E\,*$. The good move is to shift. A driver whose DECIDE reduces whenever a right side is on top makes exactly this mistake and then fails on a sentence of the language; the tests check this. Read backwards, the 8 reductions are the rightmost derivation $E \Rightarrow E + T \Rightarrow E + T * F \Rightarrow E + T * \mathtt{id} \Rightarrow E + F * \mathtt{id} \Rightarrow E + \mathtt{id} * \mathtt{id} \Rightarrow T + \mathtt{id} * \mathtt{id} \Rightarrow F + \mathtt{id} * \mathtt{id} \Rightarrow \mathtt{id} + \mathtt{id} * \mathtt{id}$.

## Correctness

**Claim 1 (any decision).** If the driver accepts, the tree it returns is a parse tree of $w$ with root $S$, and the productions of its reductions, read from last to first, are the steps of a rightmost derivation $S \Rightarrow^*_{rm} w$.

**Claim 2 (exact decision).** With the exact decision procedure, the driver accepts every $w \in L(G)$ and reports an error for every $w \notin L(G)$, and it always stops.

For Claim 1, the invariant is that the stack holds trees whose leaves, left to right, spell $a_1 \cdots a_{pos-1}$, and that the stack symbols $\gamma$ satisfy $\gamma \Rightarrow^*_{rm} a_1 \cdots a_{pos-1}$ by the reductions done so far, read backwards. A shift adds a leaf and a terminal. A reduction by $A \to \beta$ replaces the roots $\beta$ by $A$; since everything after the top of the stack is terminal, the step $\alpha A\, a_{pos} \cdots a_n \Rightarrow \alpha\beta\, a_{pos} \cdots a_n$ rewrites the rightmost nonterminal, so it is a rightmost step. At accept the stack is the single tree $S$ over all of $w$.

For Claim 2, the item chains characterize goodness: a configuration in the run of a parse tree $T$ has the chain of nodes from the root of $T$ to the node being built, and conversely a chain with $\delta_k \cdots \delta_1 \Rightarrow^* a_{pos} \cdots a_n$ can be completed into a parse tree of $w$ whose postorder run passes through the configuration. The start configuration is good exactly when $w \in L(G)$. Each move of the procedure keeps the configuration good, and from a good configuration an accepting run shifts the next token, or accepts, after finitely many reductions, so the breadth-first search finds a target. Between two shifts there are finitely many moves, so the run stops. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

**The driver.** Each token is shifted once, so there are $n$ shifts, and each reduction creates one inner node of the tree, so there are $r$ reductions. A reduction by $A \to \beta$ costs $O(|\beta| + 1)$, and the sum of $|\beta|$ over all reductions is the number of edges of the tree, at most $n + r$. So the driver does $O(n + r)$ work besides the calls of DECIDE, and the stack and the tree take $O(n + r)$ space. The best case is an error at the first decision.

**With an LR table.** For a fixed LR(1) grammar, DECIDE is a table lookup, and the tree has $O(n)$ inner nodes: an LR(1) grammar is unambiguous and has no cycle $A \Rightarrow^+ A$, and a parse tree without such a cycle has $O(n)$ nodes for a fixed grammar. So an LR parser runs in $O(n)$ time.

**With the exact procedure.** Each test of goodness runs an item automaton over the stack, with one input position attached to each item, after a one-time computation of all pairs (nonterminal, substring) with $A \Rightarrow^* a_i \cdots a_j$. This is polynomial per test, but the breadth-first search can visit many stacks. The procedure is meant for checking, not for speed.

## Properties

- **One pass, left to right.** Each token is shifted once, and the tree is built in postorder, so semantic actions run as soon as a node is complete, as in [yacc](/yacc/).
- **Not recursive.** All state is in the stack; nesting depth costs stack entries, not program recursion.
- **Online with LR tables.** An LR parser reports an error at the first token that cannot extend a viable prefix of a sentence. The exact procedure of this page is offline, since it looks at the whole input.
- **Left recursion is welcome.** A left-recursive production such as $E \to E + T$ reduces as soon as its right side is complete and keeps the stack short; right recursion keeps the whole list on the stack until its end.

## Variants and improvements

- **LR parsing.** States of the LR(0) or LR(1) item automaton stored on the stack turn DECIDE into a table lookup ([LR parse table](/lr-parse-table/)). The LR(0), SLR(1), LALR(1) and LR(1) methods differ in how the reduce entries are restricted by lookahead.
- **Precedence parsing.** [Operator precedence](/operator-precedence-parsing/) and the [shunting-yard algorithm](/shunting-yard-algorithm/) decide by comparing operators and need no automaton, for expression grammars.
- **Conflict resolution.** Parser generators accept some grammars with conflicts by resolving them with declared precedence and associativity, or by preferring shift, as for the dangling else.
- **Generalized parsing.** [GLR parsing](/glr-parsing/) runs all moves of a conflict in parallel on a [graph-structured stack](/graph-structured-stack/) and parses every grammar.
- **Recursive ascent.** [Recursive ascent](/recursive-ascent-parsing/) writes the LR automaton as mutually recursive procedures, one per state, instead of a table and an explicit stack.

## When to use it

Use a shift-reduce parser, through a parser generator, when the grammar is large, left recursive, or changes often, and you want linear-time parsing with a guarantee that the grammar has no conflicts. Use [recursive descent](/recursive-descent-parsing/) when you write the parser by hand and the grammar is LL(1) or close to it. Use a general method such as the [Earley parser](/earley-parser/) or [GLR parsing](/glr-parsing/) for ambiguous grammars.

## Pitfalls

- **Reducing as soon as possible.** A right side on top of the stack is not always a handle, as in the example. The decision must use the left context (the whole stack) and the lookahead.
- **Shifting as soon as possible.** The opposite rule fails too: on $\mathtt{id} + \mathtt{id}$ it shifts the $+$ while the stack holds $\mathtt{id}$, and the $\mathtt{id}$ can then never be reduced, since it is no longer on top.
- **Accepting too early.** The stack $S$ alone is not enough; the input must also be used up, or the parser accepts a prefix of the input.
- **Cycles and empty reductions.** With $A \to \varepsilon$ or a cycle $A \Rightarrow^+ A$, a careless decision rule can reduce forever without shifting. LR tables for such grammars have conflicts; a general procedure needs a measure that decreases, such as the shortest path used here.
- **Deep right recursion.** A right-recursive list $L \to x\, L \mid x$ keeps every element on the stack until the end, so the stack grows with the input.

## Implementations

## History

Floyd's operator precedence method of 1963 decided between shifting and reducing by precedence relations between terminal symbols, an early shift-reduce method for expression-like languages. Knuth's 1965 paper on LR($k$) grammars defined handles of right sentential forms, showed that the strings on the stack form a regular language, and gave the automaton that decides each move with $k$ tokens of lookahead. The practical table constructions followed: DeRemer's SLR and LALR methods around 1969 to 1971, and the LALR parser generator yacc in the 1970s.

## References
