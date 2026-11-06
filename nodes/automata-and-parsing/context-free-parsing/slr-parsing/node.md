---
tag: 7X628Y
kind: algorithm
slug: slr-parsing
name: SLR(1) parsing
aliases:
- SLR parsing
- SLR(1)
- simple LR parsing
area: automata-and-parsing/context-free-parsing
level: core
summary: LR(0) automaton with reductions limited to FOLLOW-set lookaheads.
solves: [cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the number of input tokens, for a fixed grammar}
  time: {worst: O(n), best: Θ(1)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1969
  people: [Frank L. DeRemer]
  note: DeRemer's 1969 MIT thesis and his 1971 paper Simple LR(k) grammars added FOLLOW-set lookaheads to the LR(0) automaton, which made LR parsing practical for programming languages.
prereqs: [lr0-parsing, slr-grammar]
see_also: [lalr-parsing, canonical-lr-parsing, lr-parse-table, viable-prefix, shift-reduce-conflict, reduce-reduce-conflict, yacc, recursive-ascent-parsing]
sources:
  - paper: doi:10.1145/362619.362625
    title: Frank L. DeRemer, Simple LR(k) grammars, Communications of the ACM 14(7) (1971)
    locator: pp. 453 to 460
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.6.3, The LR-Parsing Algorithm (the moves on id * id + id); Section 4.6.4, Constructing SLR-Parsing Tables (Algorithm 4.46)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 9.8, SLR(1)
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (valid items and the LR(k) parsing automaton)
---

SLR(1) parsing, for "simple LR", is the [shift-reduce](/shift-reduce-parsing/) parser built on the automaton of [LR(0) parsing](/lr0-parsing/), with one token of lookahead used in the simplest way: in a state where a production $A \to \beta$ is complete, the parser reduces by it only if the next token is in $\text{FOLLOW}(A)$, the set of tokens that can follow $A$ anywhere in a sentence. On an [SLR(1) grammar](/slr-grammar/) the resulting table has one action per entry, and the parser runs in time linear in the input, builds the parse tree, and stops at the first token that no sentence allows there. The method handles the usual expression grammars, which LR(0) parsing cannot, with tables of exactly the same size; its lookaheads are coarser than those of [LALR(1)](/lalr-parsing/) and [canonical LR(1)](/canonical-lr-parsing/) parsing, so it accepts fewer grammars.

## In plain words

A bottom-up parser reads tokens onto a stack and, whenever the top of the stack is a complete grammar rule, may replace it by the rule's name. A small machine built in advance from the grammar tracks what the stack holds and says which rules can be complete.

An LR(0) parser replaces as soon as a rule is complete, which fails when a rule can be complete and still be the start of something longer, as `x` is in `x * y`. The SLR parser looks at the next token first. A rule for expressions is only worth completing if the next token is one that can come after an expression somewhere in the language, such as `+` or `)`. If the next token is `*`, it keeps reading instead. The lists of possible next tokens are computed once from the grammar.

## The problem

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. The grammar is augmented with a new start symbol $S'$ and the production $S' \to S$, and $\$$ is an end marker after the input.

**Input:** a grammar $G$ and tokens $w = a_1 \cdots a_n$.

**Output:** a [parse tree](/parse-tree/) of $w$ with root $S$, or an error at the first position $i$ such that $a_1 \cdots a_i$ is not a prefix of any sentence ($i = n + 1$ if $w$ is a proper prefix of a sentence). The method applies when $G$ is [SLR(1)](/slr-grammar/), that is, when the table below has no entry with two actions; otherwise the builder reports the [shift-reduce](/shift-reduce-conflict/) and [reduce-reduce conflicts](/reduce-reduce-conflict/).

## The algorithm

The builder removes the useless productions, builds the LR(0) automaton from the CLOSURE and GOTO operations on [LR items](/lr-item/), computes the [FOLLOW sets](/first-and-follow-sets/), and fills the table.

```pseudo id=build
BUILD-SLR(G)
B1  remove useless productions; add S' → S; compute FOLLOW(A) for every nonterminal A
B2  build the LR(0) automaton: the states C reachable from CLOSURE({S' → ·S}) and GOTO
B3  for each state I in C do
B4      for each item A → α·aβ in I with a a terminal: add "shift GOTO[I, a]" to ACTION[I, a]
B5      for each item A → β· in I with A ≠ S', and each a in FOLLOW(A): add "reduce A → β" to ACTION[I, a]
B6      if S' → S· is in I then add "accept" to ACTION[I, $]
B7  report every entry with two actions as a conflict
```

The driver is the LR driver. It keeps a stack of states and, for each state above state 0, the tree of the symbol that led into it.

```pseudo id=main
SLR-PARSE(w)
L1  push state 0; append $ to w; i ← 1
L2  loop
L3      q ← the top state; a ← w_i
L4      if ACTION[q, a] is empty then report an error at token i
L5      else if ACTION[q, a] = shift j then
L6          push j and the leaf a; i ← i + 1
L7      else if ACTION[q, a] = reduce A → β then
L8          pop |β| states and their trees; make the node A over these trees
L9          push GOTO[top state, A] and the new node
L10     else return the tree on the stack       ▷ ACTION[q, a] = accept
```

The only difference from LR(0) parsing is line B5: an LR(0) table reduces on every token, and the SLR(1) table only on $\text{FOLLOW}(A)$. The state on top of the stack is the set of items valid for the symbols on the stack (Lemma 1 of the proof), so a complete item $A \to \beta \cdot$ in it means that $\beta$ is on top, and line L9 continues from the state below $\beta$ as if $A$ had been read.

## Example

Take the expression grammar with its productions numbered:

$$(1)\ E \to E + T \quad (2)\ E \to T \quad (3)\ T \to T * F \quad (4)\ T \to F \quad (5)\ F \to ( E ) \quad (6)\ F \to \mathtt{id}$$

Then $\text{FOLLOW}(E) = \{+, ), \$\}$ and $\text{FOLLOW}(T) = \text{FOLLOW}(F) = \{+, *, ), \$\}$. The LR(0) automaton has 12 states, numbered in breadth-first order:

| state | items |
|---|---|
| 0 | $S' \to \cdot E$, $E \to \cdot E + T$, $E \to \cdot T$, $T \to \cdot T * F$, $T \to \cdot F$, $F \to \cdot ( E )$, $F \to \cdot \mathtt{id}$ |
| 1 | $S' \to E \cdot$, $E \to E \cdot + T$ |
| 2 | $E \to T \cdot$, $T \to T \cdot * F$ |
| 3 | $T \to F \cdot$ |
| 4 | $F \to ( \cdot E )$ and the closure items of $E$, $T$, $F$ |
| 5 | $F \to \mathtt{id} \cdot$ |
| 6 | $E \to E + \cdot T$, $T \to \cdot T * F$, $T \to \cdot F$, $F \to \cdot ( E )$, $F \to \cdot \mathtt{id}$ |
| 7 | $T \to T * \cdot F$, $F \to \cdot ( E )$, $F \to \cdot \mathtt{id}$ |
| 8 | $F \to ( E \cdot )$, $E \to E \cdot + T$ |
| 9 | $E \to E + T \cdot$, $T \to T \cdot * F$ |
| 10 | $T \to T * F \cdot$ |
| 11 | $F \to ( E ) \cdot$ |

States 1, 2 and 9 have LR(0) conflicts: a complete item next to a shift item. In state 2, for example, LR(0) parsing cannot choose between reducing $E \to T$ and shifting $*$. Since $* \notin \text{FOLLOW}(E)$, the SLR(1) table reduces on $+$, $)$, $\$$ and shifts on $*$. The table, with $s j$ for "shift and go to $j$" and $r k$ for "reduce by production $k$":

| state | $\mathtt{id}$ | $+$ | $*$ | $($ | $)$ | $\$$ | $E$ | $T$ | $F$ |
|---|---|---|---|---|---|---|---|---|---|
| 0 | s5 | | | s4 | | | 1 | 2 | 3 |
| 1 | | s6 | | | | acc | | | |
| 2 | | r2 | s7 | | r2 | r2 | | | |
| 3 | | r4 | r4 | | r4 | r4 | | | |
| 4 | s5 | | | s4 | | | 8 | 2 | 3 |
| 5 | | r6 | r6 | | r6 | r6 | | | |
| 6 | s5 | | | s4 | | | | 9 | 3 |
| 7 | s5 | | | s4 | | | | | 10 |
| 8 | | s6 | | | s11 | | | | |
| 9 | | r1 | s7 | | r1 | r1 | | | |
| 10 | | r3 | r3 | | r3 | r3 | | | |
| 11 | | r5 | r5 | | r5 | r5 | | | |

No entry has two actions, so the grammar is SLR(1). The parse of $\mathtt{id} * \mathtt{id} + \mathtt{id}$:

| step | states | symbols | input | action |
|---|---|---|---|---|
| 1 | 0 | | $\mathtt{id} * \mathtt{id} + \mathtt{id}\ \$$ | shift |
| 2 | 0 5 | $\mathtt{id}$ | $* \mathtt{id} + \mathtt{id}\ \$$ | reduce $F \to \mathtt{id}$ |
| 3 | 0 3 | $F$ | $* \mathtt{id} + \mathtt{id}\ \$$ | reduce $T \to F$ |
| 4 | 0 2 | $T$ | $* \mathtt{id} + \mathtt{id}\ \$$ | shift |
| 5 | 0 2 7 | $T *$ | $\mathtt{id} + \mathtt{id}\ \$$ | shift |
| 6 | 0 2 7 5 | $T * \mathtt{id}$ | $+ \mathtt{id}\ \$$ | reduce $F \to \mathtt{id}$ |
| 7 | 0 2 7 10 | $T * F$ | $+ \mathtt{id}\ \$$ | reduce $T \to T * F$ |
| 8 | 0 2 | $T$ | $+ \mathtt{id}\ \$$ | reduce $E \to T$ |
| 9 | 0 1 | $E$ | $+ \mathtt{id}\ \$$ | shift |
| 10 | 0 1 6 | $E +$ | $\mathtt{id}\ \$$ | shift |
| 11 | 0 1 6 5 | $E + \mathtt{id}$ | $\$$ | reduce $F \to \mathtt{id}$ |
| 12 | 0 1 6 3 | $E + F$ | $\$$ | reduce $T \to F$ |
| 13 | 0 1 6 9 | $E + T$ | $\$$ | reduce $E \to E + T$ |
| 14 | 0 1 | $E$ | $\$$ | accept |

Step 4 is where SLR(1) differs from LR(0): in state 2 with $*$ next, the parser shifts, and in step 8, in the same state with $+$ next, it reduces. The reductions, read from the bottom up, are the rightmost derivation $E \Rightarrow E + T \Rightarrow E + F \Rightarrow E + \mathtt{id} \Rightarrow T + \mathtt{id} \Rightarrow T * F + \mathtt{id} \Rightarrow T * \mathtt{id} + \mathtt{id} \Rightarrow F * \mathtt{id} + \mathtt{id} \Rightarrow \mathtt{id} * \mathtt{id} + \mathtt{id}$.

**Errors.** On $\mathtt{id} + * \mathtt{id}$ the parser reaches state 6 after $\mathtt{id} +$, has no action on $*$, and reports an error at token 3. On $( \mathtt{id}$ it shifts both tokens, then on $\$$ reduces $F \to \mathtt{id}$, $T \to F$ and $E \to T$, because $\$$ is in all three FOLLOW sets, and only then finds no action on $\$$ in state 8. The error is still reported at the right position, the end of the input, but after three reductions that a canonical LR(1) parser would not make. The tables and traces above were produced by the implementation.

## Correctness

The proof in `proofs/correctness.md` assumes that the table has no conflict. Its steps:

1. **The states are the valid items.** The state reached over a string $\gamma$ is the set of items $[A \to \alpha \cdot \beta]$ valid for $\gamma$, those with a rightmost derivation $S' \Rightarrow^*_{rm} \varphi A z \Rightarrow \varphi \alpha \beta z$ and $\gamma = \varphi \alpha$. It follows that every reduction pops a real right side, and the parser accepts only with a parse tree of $w$.
2. **Every move toward acceptance is in the table.** From a configuration that some sequence of legal moves can bring to acceptance, the next such move is in the table entry: a reduction by $A \to \beta$ because $A$ is followed by the next token in a sentential form, so that token is in $\text{FOLLOW}(A)$; a shift because the token is later reduced inside some production. With no conflicts, the parser makes exactly this move, so it accepts every sentence, and the grammar is unambiguous.
3. **Errors at the first bad token.** A shift happens only in a state with a valid item that has the token after the dot, so the tokens shifted so far are a prefix of a sentence. Conversely the runs on two inputs agree until they examine different tokens.
4. **Termination in $O(n)$ moves.** The automaton has no cycle of GOTO transitions over nullable symbols: otherwise an accepting run would have to build arbitrarily many empty trees before seeing a different next token. With this and unambiguity, the parser never reduces forever between two shifts, and the forest on the stack has $O(n)$ nodes.

The SLR parser may make reductions on a token that cannot follow, as on $( \mathtt{id}$ above, but these reductions never shift a wrong token, so the error position is the same as for canonical LR(1).

## Complexity

**Parsing.** Every move creates a node of the forest on the stack, a leaf for a shift and an inner node for a reduction, and no node is removed. The proof shows that for a fixed grammar the forest has $O(n)$ nodes, so the parser makes $O(n)$ moves, each in $O(1)$ time plus the length of the popped right side, which is bounded by the grammar. Time and space are $\Theta(n)$ on sentences and $O(n)$ in general; the best case is $\Theta(1)$, an error at the first token.

**Building.** Let $N$ be the number of LR(0) states. There are $|G| + 2$ items with $S' \to S$, so $N \le 2^{|G| + 2}$, and $N$ can be exponential in $|G|$, though it is a few hundred for programming language grammars. As for [LR(0) parsing](/lr0-parsing/), the automaton takes $O(N |G|^2)$ time. FOLLOW is a least fixpoint computed in polynomial time, and line B5 adds at most $|\Sigma| + 1$ entries per complete item, so the actions take $O(N |G| (|\Sigma| + 1))$ time. The table has $N$ rows and $|\Sigma| + 1 + |V|$ columns.

| quantity | bound |
|---|---|
| parse time | $O(n)$ for a fixed grammar |
| parse space | $O(n)$ |
| LR(0) states $N$ | at most $2^{\lvert G \rvert + 2}$ |
| build time | $O(N \lvert G \rvert^2 + N \lvert G \rvert \lvert \Sigma \rvert)$ plus FOLLOW |
| table size | $O(N (\lvert \Sigma \rvert + \lvert V \rvert))$ |

## Properties

- **Same states as LR(0).** The SLR(1) table has the rows of the LR(0) automaton; only the reduce entries change. LALR(1) also keeps these rows, and canonical LR(1) can have many more.
- **Grammar class.** Every LR(0) grammar is SLR(1), every SLR(1) grammar is LALR(1), and the inclusions are strict. The [SLR(1) grammar](/slr-grammar/) page gives the examples, including the unambiguous grammar $S \to L = R \mid R$, $L \to * R \mid \mathtt{id}$, $R \to L$, which is LALR(1) but not SLR(1).
- **Valid prefix property.** No token is shifted unless the tokens up to it are a prefix of a sentence. Reductions on a wrong token can happen before the error is noticed.
- **Deterministic and online.** One token of lookahead decides each move, so the parser can work on a stream and needs only the current token.
- **Unambiguous.** A grammar with a conflict-free SLR(1) table is unambiguous, and the parser returns its unique tree.

## Variants and improvements

- **LALR(1).** Replace $\text{FOLLOW}(A)$ in line B5 by the set of tokens that can follow $A$ when the parser is in this state. This is the method of [yacc](/yacc/) and Bison; see [LALR parsing](/lalr-parsing/).
- **Canonical LR(1).** Carry the lookahead in the items, which splits states; the parser then makes no reduction on a wrong token. See [canonical LR parsing](/canonical-lr-parsing/).
- **SLR(k).** DeRemer defined the method for $k$ tokens of lookahead, with $\text{FOLLOW}_k$ in place of FOLLOW.
- **Conflict resolution.** As in yacc, precedence and associativity declarations can select one action in a conflicting entry, so that an ambiguous expression grammar works with an SLR table; see [shift-reduce conflict](/shift-reduce-conflict/).
- **Generalized parsing.** [GLR parsing](/glr-parsing/) keeps all actions of a conflicting entry and follows them in parallel; it works with any LR table, including an SLR(1) one.
- **Recursive ascent.** The table can be compiled into one procedure per state; see [recursive ascent parsing](/recursive-ascent-parsing/).

## When to use it

Use SLR(1) when writing a bottom-up parser generator by hand, for teaching, and for small languages whose grammars are SLR(1), which includes many expression and statement grammars. When the builder reports conflicts that come from FOLLOW and not from ambiguity, switch to LALR(1), which costs a more complex lookahead computation but no larger table. For hand-written parsers, [recursive descent](/recursive-descent-parsing/) or [Pratt parsing](/pratt-parsing/) are usually simpler.

## Pitfalls

- **FOLLOW of the start symbol.** FOLLOW must be computed for the augmented grammar, with $\$ \in \text{FOLLOW}(S)$; otherwise the reductions at the end of the input are missing.
- **Unambiguous does not mean SLR.** A conflict in the SLR table can come from the coarseness of FOLLOW, as in the assignment grammar, and not from ambiguity. Rewriting the grammar or using LALR(1) removes it.
- **Useless productions.** A production that no sentence uses can still add tokens to FOLLOW sets and create conflicts. Remove useless symbols first.
- **Empty productions.** $A \to \varepsilon$ makes $A \to \cdot$ complete in every state that predicts $A$, so it is reduced on all of $\text{FOLLOW}(A)$; two such nonterminals in one state with overlapping FOLLOW sets are a reduce-reduce conflict.
- **Error messages.** Because reductions can happen before an error is detected, the state at the error is not always the state where the wrong token first appeared; error recovery must use the state at the time of detection.
- **Recursion.** The driver is a loop over an explicit stack, and the tree is built bottom-up; a recursive walk over the result can overflow on long inputs.

## Implementations

## History

Knuth (1965) defined LR($k$) grammars and showed that they can be parsed in linear time by a deterministic automaton, but his construction gave very large tables. DeRemer, in his 1969 MIT thesis and in his 1971 paper, observed that the LR(0) automaton with lookahead sets for its complete items suffices for most programming language grammars. The FOLLOW-set version is the SLR(k) method of the 1971 paper, and the state-dependent lookaheads give LALR(k), which became the method of yacc (Johnson, 1975). The SLR construction is the one taught first in compiler texts, including the Dragon book.

## References
