---
tag: VAAJVS
kind: algorithm
slug: lalr-lookahead-computation
name: LALR lookahead computation
aliases:
- DeRemer-Pennello lookahead computation
- LALR lookahead propagation
area: automata-and-parsing/parser-generators
level: advanced
summary: Efficient computation of LALR(1) lookahead sets via relations and digraph traversal, due to DeRemer and Pennello.
solves: [parser-table-construction]
model: word-ram
complexity:
  vars: {X: the number of nonterminal transitions of the LR(0) automaton, r: the number of pairs in the reads and includes relations, g: the grammar size, σ: the number of terminals}
  time: {relations: O(X g), digraph: O((X + r) σ), total: O(X g σ)}
  space: {relations: O(X g), sets: O(X σ)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1982
  people: [Frank DeRemer, Thomas Pennello]
  note: DeRemer and Pennello expressed the LALR(1) lookaheads through the relations reads, includes and lookback on the transitions of the LR(0) automaton, and computed the two unions over them with one strongly connected components search each.
prereqs: [lalr-parsing, lr-item-sets, tarjan-scc]
see_also: [yacc, parser-table-construction, first-and-follow-sets, nullable-symbol, canonical-lr-parsing, slr-parsing, strongly-connected-components, transitive-closure]
sources:
  - paper: doi:10.1145/69622.357187
    title: Frank DeRemer and Thomas Pennello, Efficient computation of LALR(1) look-ahead sets, ACM Transactions on Programming Languages and Systems 4(4) (1982)
    locator: pp. 615 to 649 (the relations reads, includes and lookback, the equations for Read, Follow and LA, and the procedure Digraph)
  - paper: doi:10.1137/0201010
    title: Robert Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2) (1972)
    locator: pp. 146 to 160 (the strongly connected components algorithm that Digraph follows)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.7.5, Efficient Construction of LALR Parsing Tables (the propagation method, which computes the same sets)
---

LALR lookahead computation finds, for every completed item of the LR(0) automaton of a grammar, the set of tokens on which an [LALR(1) parser](/lalr-parsing/) should reduce by it. DeRemer and Pennello reduce the problem to two unions over graphs: three relations on the nonterminal transitions of the automaton, called reads, includes and lookback, say where lookahead tokens come from, and a depth-first search that handles each strongly connected component once collects the tokens. The result is the same as merging the canonical LR(1) states by core, without building them, and the cost is linear in the size of the relations times the cost of one set union.

## In plain words

An LR parser built from the small LR(0) machine knows when a rule is complete but not always whether to use it now. The answer depends on which tokens can come next, and those tokens arrive from different places. Some can be read right after the rule's name in the machine. Some come from rules that can vanish, so the parser looks past them. And some come from further out: if the rule's name ends a bigger rule, whatever can follow the bigger rule can follow this one too.

The method writes these "comes from" links down as arrows between moves of the machine and then collects, for each move, every token reachable along the arrows. Loops of arrows are handled by treating a whole loop as one node, so each token set is built once.

## The problem

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, the empty string $\varepsilon$, start symbol $S$, input length $n$ and size $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$. The end marker is $\$$, and the augmented grammar adds $S' \to S$ as production 0. $G$ is reduced: every nonterminal is reachable from $S$ and derives some terminal string. For an LR(0) state $p$ and a string $\beta$ of grammar symbols, $\mathrm{GOTO}(p, \beta)$ is the state reached from $p$ by the moves on the symbols of $\beta$ (see [LR item sets](/lr-item-sets/)). A *nonterminal transition* is a pair $(p, A)$ with $A \in V$ such that $\mathrm{GOTO}(p, A)$ is defined; $X$ is the set of them.

**Input.** The augmented grammar and its LR(0) automaton.

**Output.** For every state $q$ and every completed item $A \to \omega \cdot$ in $q$ with $A \ne S'$, the set $\mathrm{LA}(q, A \to \omega)$ of terminals $a$ (or $\$$) such that some canonical LR(1) state with the same core as $q$ contains the item $[A \to \omega \cdot,\ a]$. These are the LALR(1) lookaheads: the parser reduces by $A \to \omega$ in state $q$ exactly on them.

## The algorithm

The relations, for nonterminal transitions $(p, A)$ and $(p', B)$, a state $q$ and a production $A \to \omega$:

- $\mathrm{DR}(p, A)$, the *direct reads*, is the set of terminals $t$ such that $\mathrm{GOTO}(\mathrm{GOTO}(p, A), t)$ is defined, together with $\$$ when $(p, A)$ is the transition of state 0 on $S$.
- $(p, A)$ *reads* $(r, C)$ when $r = \mathrm{GOTO}(p, A)$, $C \in V$ is [nullable](/nullable-symbol/) and $\mathrm{GOTO}(r, C)$ is defined.
- $(p, A)$ *includes* $(p', B)$ when there is a production $B \to \beta A \gamma$ with $\gamma \Rightarrow^* \varepsilon$ and $\mathrm{GOTO}(p', \beta) = p$.
- $(q, A \to \omega)$ *lookback* $(p, A)$ when $\mathrm{GOTO}(p, \omega) = q$.

The sets wanted satisfy
$$\mathrm{Read}(x) = \mathrm{DR}(x) \cup \bigcup_{x \text{ reads } y} \mathrm{Read}(y), \qquad \mathrm{Follow}(x) = \mathrm{Read}(x) \cup \bigcup_{x \text{ includes } y} \mathrm{Follow}(y),$$
$$\mathrm{LA}(q, A \to \omega) = \bigcup_{(q, A \to \omega) \text{ lookback } (p, A)} \mathrm{Follow}(p, A),$$
each in the least solution. A least solution of $F(x) = F'(x) \cup \bigcup_{x R y} F(y)$ is the union of $F'(y)$ over all $y$ reachable from $x$ along $R$, and DIGRAPH computes it.

```pseudo id=main
LALR-LOOKAHEADS(G)
L1  build the LR(0) automaton of G augmented with S' → S; X ← its transitions (p, A) on nonterminals
L2  for each (p, A) in X with r = GOTO(p, A): DR(p, A) ← the terminals t with GOTO(r, t) defined, and $ if r contains S' → S·
L3  (p, A) reads (r, C) when r = GOTO(p, A), GOTO(r, C) is defined and C is nullable
L4  Read ← DIGRAPH(X, reads, DR)
L5  for each (p', B) in X and each B → X1 … Xm: walk p = p', GOTO(p', X1), …; if Xj is a nonterminal and Xj+1 … Xm is nullable, (p, Xj) includes (p', B)
L6  Follow ← DIGRAPH(X, includes, Read)
L7  for each (p, A) in X and each production A → ω: q ← GOTO(p, ω); LA(q, A → ω) ← LA(q, A → ω) ∪ Follow(p, A)
DIGRAPH(X, R, F')
L8  set N(x) ← 0 for all x; for each x in X with N(x) = 0: TRAVERSE(x)
TRAVERSE(x)
L9  push x on the stack; d ← the depth of the stack; N(x) ← d; F(x) ← F'(x)
L10 for each y with x R y: if N(y) = 0 then TRAVERSE(y)
L11     N(x) ← min(N(x), N(y)); F(x) ← F(x) ∪ F(y)
L12 if N(x) = d: repeat N(top) ← ∞; F(top) ← F(x); pop, until the popped element is x
```

**Lines L2 to L4.** $\mathrm{Read}(p, A)$ is the set of tokens that can come right after $A$ in state $p$ without leaving the right side that $A$ is part of: those the next state can shift directly, and those it can shift after moving over nullable nonterminals, which the reads relation follows.

**Lines L5 and L6.** If $A$ ends a right side $B \to \beta A \gamma$ up to nullable symbols, everything that can follow $B$ from the state where $B$'s right side started can follow $A$. Line L5 finds these pairs by walking each right side from each state with a transition on its left side.

**Line L7.** A reduction by $A \to \omega$ in state $q$ pops back to a state $p$ with $\mathrm{GOTO}(p, \omega) = q$ and then moves on $A$, so it can be followed by whatever follows $A$ from such a $p$.

**DIGRAPH (L8 to L12).** It is [Tarjan's strongly connected components](/tarjan-scc/) search with sets: $N(x)$ is the stack depth of $x$, lowered to the least depth of a node that $x$ reaches and that is still on the stack. When the search leaves the root $x$ of a component, every node of the component has been visited below $x$, its set $F(x)$ holds everything the component reaches, and all members get that set. The implementation runs the search with an explicit stack of frames instead of recursion.

## Example

**Grammar.** $S \to L = R \mid R$, $L \to {*}\,R \mid \mathit{id}$, $R \to L$, productions 1 to 5, the grammar of the Dragon book that is LALR(1) but not [SLR(1)](/slr-parsing/). Its LR(0) automaton has 10 states; those that matter are

| state | kernel items |
|---|---|
| 0 | $S' \to \cdot S$ |
| 2 | $S \to L \cdot = R$, $R \to L \cdot$ |
| 4 | $L \to * \cdot R$ |
| 5 | $L \to \mathit{id} \cdot$ |
| 6 | $S \to L = \cdot R$ |
| 7 | $R \to L \cdot$ |
| 8 | $L \to * R \cdot$ |
| 9 | $S \to L = R \cdot$ |

with $\mathrm{GOTO}(0, L) = 2$, $\mathrm{GOTO}(4, L) = \mathrm{GOTO}(6, L) = 7$, $\mathrm{GOTO}(4, R) = 8$, $\mathrm{GOTO}(6, R) = 9$, and the moves on $*$ and $\mathit{id}$ from states 0, 4 and 6 going to 4 and 5.

**Relations.** No symbol is nullable, so reads is empty and Read = DR.

| transition | DR = Read | includes | Follow |
|---|---|---|---|
| $(0, S)$ | $\$$ | | $\$$ |
| $(0, L)$ | $=$ | $(0, R)$ | $=, \$$ |
| $(0, R)$ | | $(0, S)$ | $\$$ |
| $(4, L)$ | | $(4, R)$ | $=, \$$ |
| $(4, R)$ | | $(0, L)$, $(4, L)$, $(6, L)$ | $=, \$$ |
| $(6, L)$ | | $(6, R)$ | $\$$ |
| $(6, R)$ | | $(0, S)$ | $\$$ |

$(0, L)$ includes $(0, R)$ because of $R \to L$; $(4, R)$ includes $(0, L)$ because of $L \to * R$ with $\mathrm{GOTO}(0, *) = 4$. The pair $(4, L)$ and $(4, R)$ include each other, a component of two nodes, and DIGRAPH gives both the union $\{=, \$\}$.

**Lookaheads.** $R \to L \cdot$ in state 2 looks back only to $(0, R)$, so its set is $\{\$\}$ and the state has no conflict between the shift on $=$ and the reduction. In state 7 the same item looks back to $(4, R)$ and $(6, R)$ and gets $\{=, \$\}$. The other sets are $\{=, \$\}$ for $L \to \mathit{id} \cdot$ and $L \to * R \cdot$, and $\{\$\}$ for $S \to R \cdot$ and $S \to L = R \cdot$. SLR(1) would use $\mathrm{FOLLOW}(R) = \{=, \$\}$ in state 2 and report a shift-reduce conflict there.

**Reads.** In $S \to A\,B\,c$, $A \to a$, $B \to b \mid \varepsilon$, the state after $A$ shifts $b$ and moves on the nullable $B$, so $\mathrm{DR}(0, A) = \{b\}$, $(0, A)$ reads $(2, B)$ with $\mathrm{DR}(2, B) = \{c\}$, and $A \to a \cdot$ gets $\{b, c\}$.

## Correctness

The proof in [correctness](proofs/correctness.md) shows that the merged LR(1) lookaheads are the least solution of three rules over LR(0) states, that $\mathrm{LA}(q, A \to \omega)$ is the union of the merged lookaheads of the items $A \to \cdot \omega$ along the lookback pairs, and that these equal the sets Follow defined by reads and includes; the key step is that the tokens reachable from a state through moves on nullable nonterminals are exactly the FIRST sets of the rest of its kernel items. It then shows that DIGRAPH computes the union over reachable nodes. The tests compare the sets with canonical LR(1) states merged by core on random grammars with ε-productions, left recursion and ambiguity, and compare DIGRAPH with plain reachability and with a naive fixed point.

## Complexity

- **Relations.** DR and reads look at the moves out of one state per transition. Line L5 walks every right side of $B$ once per transition on $B$, and line L7 walks every right side of $A$ once per transition on $A$, so both take $O(|X| \cdot |G|)$ steps, and includes and lookback have at most that many pairs.
- **DIGRAPH.** Each node is pushed and popped once and each pair of the relation is looked at once, with one set union each: $O((|X| + r) \cdot \sigma)$ time for sets of $\sigma$ terminals stored as bit vectors.
- **Total.** $O(|X| \cdot |G| \cdot \sigma)$ including the unions of line L7, not counting the LR(0) automaton itself, whose number of states can be exponential in $|G|$ (see [LR item sets](/lr-item-sets/)). The propagation method of the Dragon book, used on the [yacc](/yacc/) page, instead closes every kernel item with a dummy lookahead and then iterates to a fixed point over the propagation links.
- **Space.** The relations and one set per transition.

## Properties

- **Same sets as LR(1) merging.** The result equals the lookaheads of canonical LR(1) states merged by core, so it is the LALR(1) table, without the size of the LR(1) collection.
- **Between SLR and LR.** $\mathrm{LA}(q, A \to \omega) \subseteq \mathrm{FOLLOW}(A)$, the set that [SLR(1)](/slr-parsing/) would use, and the union over all transitions on $A$ of $\mathrm{Follow}(p, A)$ is exactly $\mathrm{FOLLOW}(A)$.
- **Diagnosis.** DeRemer and Pennello point out that a cycle in reads, or a cycle in includes through a transition with a nonempty Read set, means that the grammar is not LR(k) for any $k$; on random grammars the tests here found an LR(k) conflict for $k = 1, 2, 3$ in every such case.
- **No recursion.** DIGRAPH runs on an explicit stack, so long chains of unit productions do not exhaust a call stack.

## Variants and improvements

- **Propagation.** The Dragon book's method closes each kernel item with a dummy lookahead $\#$ to find spontaneous lookaheads and propagation links, then iterates; it gives the same sets. It is simpler to write and is the method on the [yacc](/yacc/) page.
- **SLR.** Replacing Follow by $\mathrm{FOLLOW}(A)$ gives [SLR(1)](/slr-parsing/) tables; replacing lookback by the full LR(1) construction gives [canonical LR(1)](/canonical-lr-parsing/) tables.
- **Simpler formulations.** Bermudez and Logothetis (1989) compute the same sets as FOLLOW sets of a transformed grammar whose nonterminals are the nonterminal transitions $(p, A)$, so that an ordinary FOLLOW computation gives the LALR(1) lookaheads.
- **Fewer states than LR(1), fewer conflicts than LALR(1).** Pager's method merges canonical LR(1) states only when merging cannot create a conflict, and IELR(1) starts from the LALR(1) automaton and its lookaheads and splits the states whose merging did create one; Bison offers IELR(1) through `%define lr.type`.

## When to use it

Use it in a parser generator that builds LALR(1) tables for large grammars, where both the canonical LR(1) collection and repeated closures with lookaheads are too slow. For small grammars, teaching or testing, the propagation method or merging canonical LR(1) states gives the same sets with less code, and serves as a check.

## Pitfalls

- **The end marker.** $\$$ must enter through $\mathrm{DR}(0, S)$, or through an explicit production $S' \to S\,\$$; forgetting it leaves every set that depends on the end of input empty.
- **Nullable suffixes.** includes needs $\gamma \Rightarrow^* \varepsilon$ for the whole rest of the right side, and reads needs every nullable nonterminal transition out of the next state, not only the one right after $A$; missing either gives sets that are too small and silently drops reductions.
- **Recursion in DIGRAPH.** A recursive TRAVERSE overflows the call stack on long chains of unit productions; keep an explicit stack.
- **Shared sets.** All members of a component end with the same set; an implementation that shares one mutable set object among them must not change it later.
- **Unreduced grammars.** Unproductive nonterminals make the LR(0) and LR(1) automata disagree on which items exist, so reduce the grammar first.

## Implementations

## History

DeRemer introduced LALR(k) parsers in his 1969 MIT thesis, defined through the LR(0) automaton with lookahead added. DeRemer and Pennello published the relational method in ACM Transactions on Programming Languages and Systems in 1982; it reduced the computation to two traversals of graphs with Tarjan's 1972 strongly connected components search. Bermudez and Logothetis gave a derivation of the same sets through an ordinary FOLLOW computation on a transformed grammar in 1989.

## References
