---
tag: EJXDVD
kind: problem
slug: parser-table-construction
name: Parser table construction
aliases:
- parse table generation
- LR table construction
area: automata-and-parsing/parser-generators
level: core
summary: Given a context-free grammar, build the action and goto or predictive tables that drive a table-based parser.
prereqs: [parsing-table, first-and-follow-sets, lr-item-sets]
see_also: [parser-generator, yacc, lalr-lookahead-computation, ll-1-grammar, lr-k-grammar, parse-table-compression, shift-reduce-conflict, reduce-reduce-conflict]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.4.3, LL(1) Grammars; Section 4.6, Introduction to LR Parsing, Simple LR; Section 4.7, More Powerful LR Parsers (canonical LR(1), LALR, and the efficient construction of LALR parsing tables)
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (the canonical LR(k) construction and the test for the LR(k) property)
  - paper: "Frank DeRemer and Thomas Pennello, Efficient computation of LALR(1) look-ahead sets, ACM Transactions on Programming Languages and Systems 4(4) (1982)"
    locator: the relations reads, includes and lookback, and the Digraph procedure that computes the LALR(1) lookahead sets from them
  - paper: "David Pager, A practical general method for constructing LR(k) parsers, Acta Informatica 7 (1977)"
    locator: the merging of LR(1) states under a weak compatibility test, which gives tables close to LALR size for every LR(1) grammar
  - paper: "Joel E. Denny and Brian A. Malloy, The IELR(1) algorithm for generating minimal LR(1) parser tables for non-LR(1) grammars with conflict resolution, Science of Computer Programming (2010)"
    locator: the whole paper (the IELR(1) construction and its comparison with LALR(1) and canonical LR(1))
  - url: https://www.gnu.org/software/bison/manual/
    title: GNU Bison manual
    locator: section LR Table Construction (the lr.type values lalr, ielr and canonical-lr)
---

Parser table construction is the problem of turning a [context-free grammar](/context-free-grammar/) into the [parsing table](/parsing-table/) that drives a fixed table-driven parser, or of reporting the places where no such table exists for the chosen method. For top-down parsing the table maps a nonterminal and a lookahead token to a production; for bottom-up parsing it is a pair of ACTION and GOTO tables over the states of an LR automaton. It is the main job of a [parser generator](/parser-generator/), and the choice of method decides both which grammars are accepted and how large the table is.

## In plain words

A table-driven parser is a small, fixed loop that never changes from one language to the next. All the knowledge about the language sits in a table: for each situation the parser can be in and each next token, the table says what to do. Building that table from the grammar is the hard part.

The builder first works out all the situations the parser can be in, then fills each cell with the one right move. Sometimes a cell needs two moves, because the grammar is ambiguous or because the method looks too little ahead to choose. Then the builder reports a conflict, and the author either changes the grammar, adds a rule that picks one move, or switches to a stronger method.

## Definition

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, the empty string $\varepsilon$, start symbol $S$, input length $n$ and size $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$. The end marker is $\$$, and the augmented grammar adds $S' \to S$.

**LL(1) table construction.** Input: $G$. Output: a table $M : V \times (\Sigma \cup \{\$\}) \to 2^P$ with $A \to \alpha \in M[A, a]$ exactly when $a \in \mathrm{PREDICT}(A \to \alpha)$; see [LL(1) grammars](/ll-1-grammar/). The grammar is accepted when every cell has at most one production, and then the [LL(1) parser](/ll1-parsing/) driven by $M$ accepts exactly $L(G)$ and outputs its leftmost derivations.

**LR table construction.** Input: $G$ and a method $\mathcal{M}$, one of LR(0), SLR(1), LALR(1), LR(1) or LR(k). Output: a finite set $Q$ of states with a start state $q_0$, a table $\mathrm{GOTO} : Q \times V \to Q$, and a table
$$\mathrm{ACTION} : Q \times (\Sigma \cup \{\$\})^{k} \to 2^{\{\mathrm{shift}\ q\} \cup \{\mathrm{reduce}\ A \to \alpha\} \cup \{\mathrm{accept}\}},$$
where an empty entry means error. The grammar is accepted by $\mathcal{M}$ when every ACTION entry has at most one element. In that case the [shift-reduce parser](/shift-reduce-parsing/) driven by the table must accept exactly $L(G)$ and output the reverse of the rightmost derivation; otherwise the output is the list of conflicting entries, each a [shift-reduce](/shift-reduce-conflict/) or [reduce-reduce conflict](/reduce-reduce-conflict/).

The methods agree on what a correct table is and differ in $Q$ and in the lookaheads attached to reductions; the set of accepted grammars grows from LR(0) through SLR(1) and LALR(1) to LR(1).

## Variants

- **Conflict resolution.** Accept a grammar with conflicts and pick one action per cell by rules: operator precedence and associativity, shift over reduce, the earlier production in a reduce-reduce conflict. This is what [yacc](/yacc/) does; the table then parses $L(G)$ with one chosen tree per sentence.
- **Keeping the conflicts.** A [GLR parser](/glr-parsing/) uses the table with all its conflicts and follows every action, so any grammar is accepted.
- **Minimal LR(1).** Build tables that accept every LR(1) grammar but have close to LALR(1) size, by merging LR(1) states only when the merge creates no new conflict (Pager 1977), or by splitting LALR(1) states only where needed (IELR(1), Denny and Malloy 2010).
- **Compression.** Store the table in less space than $|Q| \cdot (|\Sigma| + 1 + |V|)$ cells; see [parse table compression](/parse-table-compression/).
- **Other table types.** An [operator precedence](/operator-precedence-parsing/) parser uses a table of relations between terminals, built from LEADING and TRAILING sets.

## Examples

**One grammar, four methods.** For the expression grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (\,E\,) \mid \mathit{id}$:

| method | states | ACTION entries | GOTO entries | conflicts |
|---|---|---|---|---|
| LR(0) automaton with FOLLOW, SLR(1) | 12 | 36 | 9 | 0 |
| LALR(1) | 12 | 36 | 9 | 0 |
| canonical LR(1) | 22 | 56 | 15 | 0 |

The LR(0) automaton alone has 3 states that need lookahead, so the grammar is not LR(0). SLR(1) and LALR(1) give the same table here. For the LL(1) form of the same language, $E \to T E'$, $E' \to + T E' \mid \varepsilon$, $T \to F T'$, $T' \to * F T' \mid \varepsilon$, $F \to (\,E\,) \mid \mathit{id}$, the LL(1) table has 5 rows and 6 columns, with 13 of its 30 cells filled and no conflict.

**Where the methods part.** For $S \to L = R \mid R$, $L \to * R \mid \mathit{id}$, $R \to L$, the SLR(1) construction finds a shift-reduce conflict on $=$ in one of its 10 states, LALR(1) finds none on the same 10 states, and canonical LR(1) needs 14 states.

**Conflicts that no method removes.** The ambiguous $E \to E + E \mid E * E \mid (\,E\,) \mid \mathit{id}$ has 10 LR(0) states and 4 conflicting cells under SLR(1) and LALR(1), on $+$ and $*$ in the two states that end with $E + E$ and $E * E$; canonical LR(1) splits these states and reports 8. The dangling else $S \to i\,S \mid i\,S\,e\,S \mid a$ has one conflict, on $e$, under each method. Precedence declarations or the shift-over-reduce rule fix both.

## Known algorithms

- **LL(1).** Compute nullable, [FIRST and FOLLOW](/first-and-follow-sets/), then place each production in the cells of its PREDICT set: $O(|G| \cdot |\Sigma|)$ time.
- **LR(0) and SLR(1).** Build the canonical collection of [LR(0) item sets](/lr-item-sets/) with CLOSURE and GOTO, the [subset construction](/subset-construction/) applied to the nondeterministic automaton of items. Shift on the terminal transitions, reduce on completed items, for every token under LR(0) parsing and on $\mathrm{FOLLOW}(A)$ under [SLR(1)](/slr-parsing/).
- **Canonical LR(1) and LR(k).** Build the item sets with lookahead strings, as defined on the [LR(k) grammar](/lr-k-grammar/) page (Knuth 1965); see [canonical LR parsing](/canonical-lr-parsing/).
- **LALR(1).** Three ways give the same table: merge the canonical LR(1) states with equal cores; propagate lookaheads through the LR(0) kernels, starting from the spontaneously generated ones (Dragon book, Section 4.7); or compute them from the relations of DeRemer and Pennello (1982) with a linear-time traversal of the relation graphs; see [LALR lookahead computation](/lalr-lookahead-computation/) and [LALR parsing](/lalr-parsing/).
- **Minimal LR(1).** Pager's method builds LR(1) states but merges two states with the same core when a compatibility test shows that the merge cannot create a conflict. IELR(1) starts from the LALR(1) automaton and splits states only where the merging of LALR(1) caused a conflict. Bison offers LALR(1), IELR(1) and canonical LR(1) through its `lr.type` setting, with LALR(1) as the default.

## Bounds

- **Output size.** The number of LR(0) states, and so the size of SLR(1) and LALR(1) tables, can be exponential in $|G|$; the [LR item sets](/lr-item-sets/) page gives a family with $|G| = O(m^2)$ and at least $2^m - 1$ states. Any construction that writes out these tables therefore needs exponential time in the worst case, and the useful measure is time in terms of $|G|$ and the output size.
- **Per state.** With the LR(0) automaton built, SLR(1) and LALR(1) lookaheads cost time polynomial in $|G|$, $|Q|$ and $|\Sigma|$; the DeRemer and Pennello method is linear in the size of its relations times $|\Sigma|$.
- **Canonical LR(1) and LALR(1).** Canonical LR(1) can have many more states than LALR(1): 22 against 12 for the expression grammar, and in general one LR(0) state can split into a copy for each distinct lookahead context.
- **LL(1).** The table has $|V| \cdot (|\Sigma| + 1)$ cells and is built in $O(|G| \cdot |\Sigma|)$ time, so LL(1) construction is polynomial.

## Reductions

- **Membership in a grammar class reduces to construction.** $G$ is LL(1), SLR(1), LALR(1) or LR(k) exactly when the corresponding construction yields no conflict, so building the table decides the class.
- **LR(0) states are a determinization.** The LR(0) automaton is the subset construction of a nondeterministic automaton with one state per dotted production, so its construction and its worst-case size follow those of the subset construction. It is not minimized afterwards: two states with different completed items call for different reductions even when their transitions agree, which is why [DFA minimization](/dfa-minimization/) does not apply as it stands.
- **LALR from LR(1).** The LALR(1) table is the image of the canonical LR(1) table under the map that sends each state to its core; a conflict-free LR(1) table maps to an LALR(1) table that can only gain reduce-reduce conflicts, never shift-reduce ones.

## Applications

- Generators of the [yacc](/yacc/) family build LALR(1) tables with precedence resolution; Bison also builds IELR(1), canonical LR(1) and GLR tables.
- LL(1) tables drive table-driven predictive parsers, and the same PREDICT sets drive generated [recursive descent](/recursive-descent-parsing/) parsers.
- The conflict reports of a table builder are a grammar debugging tool: each one names a state, a token and the competing items, and so locates an ambiguity or a missing token of lookahead.

## References
