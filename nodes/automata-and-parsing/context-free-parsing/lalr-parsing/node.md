---
tag: 2JWXYX
kind: algorithm
slug: lalr-parsing
name: LALR(1) parsing
aliases:
- LALR parsing
- LALR(1)
- look-ahead LR parsing
- lookahead LR parsing
area: automata-and-parsing/context-free-parsing
level: core
summary: Merges LR(1) states with identical cores, giving LR(1)-sized-down tables used by yacc.
solves: [cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the length of the input string (the grammar is fixed)}
  time: {worst: O(n), best: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1969
  people: [Frank DeRemer]
  note: DeRemer introduced LALR(k) parsers in his 1969 MIT thesis; Johnson's yacc made LALR(1) the standard method of parser generators in the 1970s.
prereqs: [lr-item, lr0-parsing, first-and-follow-sets, shift-reduce-parsing]
see_also: [lalr-grammar, slr-parsing, canonical-lr-parsing, lr-parse-table, reduce-reduce-conflict, yacc, glr-parsing, handle]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.7.4, Constructing LALR Parsing Tables; Section 4.7.5, Efficient Construction of LALR Parsing Tables
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 9.7, LALR(1) (9.7.1 Constructing the LALR(1) Parsing Tables, 9.7.2 Identifying LALR(1) Conflicts)
  - paper: doi:10.1145/69622.357187
    title: Frank DeRemer and Thomas Pennello, Efficient computation of LALR(1) look-ahead sets, ACM Transactions on Programming Languages and Systems 4(4) (1982)
    locator: pp. 615 to 649
  - paper: doi:10.1145/362619.362625
    title: Frank L. DeRemer, Simple LR(k) grammars, Communications of the ACM 14(7) (1971)
    locator: pp. 453 to 460
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (canonical LR(k) parsing, linear time)
---

LALR(1) parsing is [shift-reduce parsing](/shift-reduce-parsing/) driven by a table built on the [LR(0) automaton](/lr0-parsing/), with one lookahead terminal attached to each completed item. It has exactly the states of the LR(0) automaton, but it decides almost as well as [canonical LR(1) parsing](/canonical-lr-parsing/), whose automaton is often many times larger. The result is the same as building the LR(1) automaton and merging the states that have the same [LR(0) items](/lr-item/). This is the method of yacc, Bison and most other parser generators.

## In plain words

A bottom-up parser reads the input from left to right and keeps a stack. At each step it must choose: push the next word, or replace the top of the stack by a rule name. A small machine, built once from the grammar, tells it what the stack can look like. That machine says when a rule is complete, but not always whether the parser should use the rule now.

The LALR method adds to each complete rule in each state of the machine a list of words that may come next. The parser uses the rule only when the next word is in the list. The lists are computed by passing words along the arrows of the machine until nothing changes. The machine keeps its small size, and the lists remove most of the wrong choices.

## The problem

Given a [context-free grammar](/context-free-grammar/) $G = (V, \Sigma, P, S)$ and a string $w = a_1 \cdots a_n$ over $\Sigma$, decide whether $S \Rightarrow^* w$ and, if so, build a [parse tree](/parse-tree/) of $w$. We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length, and $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$ the grammar size. LALR(1) parsing solves this problem only for the grammars whose table has no conflict, the [LALR(1) grammars](/lalr-grammar/), and it reports the other grammars when it builds the table. We also assume that every nonterminal derives some terminal string; [useless symbols](/useless-symbol-elimination/) can be removed first.

## The algorithm

The grammar is **augmented** with a fresh start symbol $S'$ and the production $S' \to S$, numbered 0. The input ends with the end marker $\$ \notin \Sigma$. An LR(0) item $A \to \alpha \bullet \beta$ is a production with a dot; an LR(1) item $[A \to \alpha \bullet \beta,\ a]$ adds a terminal or $\$$, its **lookahead**. For a set $C$ of LR(1) items, $\mathrm{CLOSURE}_1(C)$ is the least set that contains $C$ and, with each $[A \to \alpha \bullet B \beta,\ a]$ where $B \in V$, contains $[B \to \bullet \eta,\ b]$ for every $B \to \eta$ in $P$ and every terminal $b \in \mathrm{FIRST}(\beta a)$. Here $\mathrm{FIRST}(\gamma)$ is the set of terminals that begin strings derived from $\gamma$, as on the page on [FIRST and FOLLOW sets](/first-and-follow-sets/).

The LR(0) automaton has one state for each set of **kernel items**: the start state has the kernel $\{S' \to \bullet S\}$, and $\mathrm{GOTO}(q, X)$ has the kernel $\{A \to \alpha X \bullet \beta : A \to \alpha \bullet X \beta$ in the LR(0) closure of $q\}$. The table builder attaches a set $\mathrm{LA}[q, i]$ of lookaheads to each kernel item $i$ of each state $q$, and grows these sets to a fixed point.

```pseudo id=main
LALR-TABLE(G)                                  ▷ G augmented with production 0: S′ → S
L1  build the LR(0) automaton: kernels K[0], …, K[s−1] with K[0] = {S′ → • S}, and GOTO
L2  LA[0, S′ → • S] ← {$}; LA[q, i] ← ∅ for every other state q and kernel item i
L3  repeat
L4      for each state q do
L5          C ← CLOSURE1({ [i, a] : i ∈ K[q], a ∈ LA[q, i] })
L6          for each [A → α • X β, b] ∈ C do add b to LA[GOTO(q, X), A → α X • β]
L7  until no set LA[q, i] changed during the pass
L8  for each state q and each [A → α • β, b] ∈ CLOSURE1 of K[q] with its sets LA do
L9      if β = a β′ with a ∈ Σ then add "shift GOTO(q, a)" to ACTION[q, a]
L10     else if β = ε then add ("accept" if A = S′, else "reduce A → α") to ACTION[q, b]

LALR-PARSE(w)                                  ▷ w = a1 … an, and a(n+1) = $
L11 if some ACTION[q, a] has two entries then report "G is not LALR(1)" and stop
L12 stack ← [0]; i ← 1
L13 loop: q ← the top of the stack; a ← a(i)
L14     if ACTION[q, a] = shift q′ then push q′; i ← i + 1
L15     else if ACTION[q, a] = reduce A → β then pop |β| states; push GOTO(top, A); make a node A over the popped subtrees
L16     else if ACTION[q, a] = accept then return the tree of S
L17     else return "reject"                   ▷ empty entry
```

Lines L3 to L7 are lookahead propagation. A lookahead in a kernel item of $q$ passes through the closure of $q$ to items whose dot moves over $X$, and so arrives in the kernel of $\mathrm{GOTO}(q, X)$. The closure also creates lookaheads of its own, from $\mathrm{FIRST}(\beta)$, which arrive by the same route. A state of the LR(1) automaton is reached from several paths, and the LALR state with its core collects the lookaheads of all of them. The implementation stores each tree node on a value stack in parallel with the state stack, and it uses no recursion.

## Example

The grammar of assignments through pointers, from the Dragon book, is not [SLR(1)](/slr-parsing/) but is LALR(1):

$$S \to L = R \mid R, \qquad L \to * R \mid \mathit{id}, \qquad R \to L.$$

Number the productions 0 $S' \to S$, 1 $S \to L = R$, 2 $S \to R$, 3 $L \to * R$, 4 $L \to \mathit{id}$, 5 $R \to L$. The LR(0) automaton has 10 states; after lines L1 to L7 their kernels and lookaheads are:

| state | kernel items with LA | state | kernel items with LA |
|---|---|---|---|
| 0 | $S' \to \bullet S$, $\{\$\}$ | 5 | $L \to \mathit{id} \bullet$, $\{=, \$\}$ |
| 1 | $S' \to S \bullet$, $\{\$\}$ | 6 | $S \to L = \bullet R$, $\{\$\}$ |
| 2 | $S \to L \bullet = R$, $\{\$\}$; $R \to L \bullet$, $\{\$\}$ | 7 | $R \to L \bullet$, $\{=, \$\}$ |
| 3 | $S \to R \bullet$, $\{\$\}$ | 8 | $L \to * R \bullet$, $\{=, \$\}$ |
| 4 | $L \to * \bullet R$, $\{=, \$\}$ | 9 | $S \to L = R \bullet$, $\{\$\}$ |

The lookahead $=$ of state 4 comes from the closure of state 0: the item $[S \to \bullet L = R,\ \$]$ adds $[L \to \bullet * R,\ =]$, whose dot moves over $*$ into state 4. The table is (s$k$ is shift to state $k$, r$p$ is reduce by production $p$):

| state | $*$ | $\mathit{id}$ | $=$ | $\$$ | GOTO |
|---|---|---|---|---|---|
| 0 | s4 | s5 | | | $S$: 1, $L$: 2, $R$: 3 |
| 1 | | | | accept | |
| 2 | | | s6 | r5 | |
| 3 | | | | r2 | |
| 4 | s4 | s5 | | | $L$: 7, $R$: 8 |
| 5 | | | r4 | r4 | |
| 6 | s4 | s5 | | | $L$: 7, $R$: 9 |
| 7 | | | r5 | r5 | |
| 8 | | | r3 | r3 | |
| 9 | | | | r1 | |

Parsing $\mathit{id} = * \mathit{id}$:

| stack | rest of input | action |
|---|---|---|
| 0 | $\mathit{id} = * \mathit{id}\ \$$ | shift 5 |
| 0 5 | $= * \mathit{id}\ \$$ | reduce $L \to \mathit{id}$ |
| 0 2 | $= * \mathit{id}\ \$$ | shift 6 |
| 0 2 6 | $* \mathit{id}\ \$$ | shift 4 |
| 0 2 6 4 | $\mathit{id}\ \$$ | shift 5 |
| 0 2 6 4 5 | $\$$ | reduce $L \to \mathit{id}$ |
| 0 2 6 4 7 | $\$$ | reduce $R \to L$ |
| 0 2 6 4 8 | $\$$ | reduce $L \to * R$ |
| 0 2 6 7 | $\$$ | reduce $R \to L$ |
| 0 2 6 9 | $\$$ | reduce $S \to L = R$ |
| 0 1 | $\$$ | accept |

In state 2, SLR(1) would reduce $R \to L$ on every terminal of $\mathrm{FOLLOW}(R) = \{=, \$\}$, and this collides with the shift on $=$. LALR(1) knows that in state 2 only $\$$ can follow this $R$, because a right side $R$ that starts the input can only be the whole $S$. The canonical LR(1) automaton of the same grammar has 14 states: states 4, 5, 7 and 8 above each come from two LR(1) states, one with lookahead $\{=, \$\}$ and one with $\{\$\}$.

## Correctness

The [proof](proofs/correctness.md) has three parts. First, if every nonterminal derives a terminal string, the fixed point of lines L3 to L7 gives, for each LR(0) state, exactly the union of the lookaheads of the canonical LR(1) states with that core, so the table of lines L8 to L10 is the LR(1) table merged by core. Second, a conflict-free table therefore makes the same moves as the canonical LR(1) parser on every sentence, so the driver accepts every $w \in L(G)$; and every node it builds is a correct derivation step, so it accepts nothing else. Third, the driver halts on every input, because an endless run of reductions would give the grammar infinitely many parse trees for one string, but an LALR(1) grammar is LR(1) and so unambiguous.

## Complexity

**Parsing.** With the table fixed, each move of the driver takes $O(1)$ time. On an accepted input there are $n$ shifts and one reduction for each internal node of the parse tree. The grammar is unambiguous, so no nonterminal $A$ derives $\mu A \nu$ with $\mu \nu \Rightarrow^* \varepsilon$; a chain of nodes that all span the same piece of the input therefore has at most $|V|$ nodes, and the tree has $O(n + 1)$ nodes with a constant that depends on the grammar. So the time is $\Theta(n)$ and the stack holds $O(n)$ entries. On a rejected input the driver halts, possibly after some reductions that the canonical LR(1) parser would not make, but it never shifts a terminal that the LR(1) parser would reject.

**The table.** The table has one row for each LR(0) state, and the number $s$ of states is the same as for [SLR(1)](/slr-parsing/) and [LR(0)](/lr0-parsing/). Each kernel is a set of dotted productions, and there are $|G|$ of them, so $s \le 2^{|G|}$; for grammars of programming languages, $s$ is in the hundreds, while canonical LR(1) automata are often several times larger. The fixed point of lines L3 to L7 is simple but can need many passes. DeRemer and Pennello compute the same sets with two relations between the nonterminal transitions of the LR(0) automaton and a strongly connected components search, in time linear in the size of these relations, times the cost of a set union.

## Properties

- **Same states as LR(0).** The automaton, the GOTO table and the shift entries are those of LR(0) and SLR(1); only the reduce entries differ.
- **Between SLR(1) and LR(1).** Every SLR(1) grammar is LALR(1) and every LALR(1) grammar is LR(1), and both inclusions are strict; see [LALR grammar](/lalr-grammar/).
- **Same languages as LR(1).** Every deterministic context-free language has an SLR(1) grammar, so LALR(1) grammars describe exactly the deterministic context-free languages.
- **No new shift-reduce conflicts.** Merging LR(1) states with the same core cannot create a [shift-reduce conflict](/shift-reduce-conflict/), because the shift items of a merged state are already in each part. It can create a [reduce-reduce conflict](/reduce-reduce-conflict/).
- **Delayed error detection.** After the LR(1) parser would stop, the LALR parser can make some more reductions, but it reports the error before it shifts the next terminal.

## Variants and improvements

- **Efficient lookaheads.** DeRemer and Pennello's relations "reads" and "includes" are the standard method in Bison and other generators. Bermudez and Logothetis give a simpler construction through a transformed grammar. The Dragon book computes the lookaheads by "spontaneous generation" with a dummy lookahead and propagation links, which is the same fixed point as lines L3 to L7.
- **LALR(k).** Each completed item carries strings of up to $k$ terminals; it is rarely used for $k > 1$.
- **Precedence and associativity.** Generators such as yacc resolve conflicts of ambiguous expression grammars by declared operator precedence instead of reporting them.
- **Minimal LR(1).** Methods such as IELR(1) in Bison split LALR states only where merging creates a conflict, so they accept every LR(1) grammar with tables close to LALR size.
- **Generalized LR.** [GLR parsing](/glr-parsing/) runs an LALR or other LR table with conflicts and keeps all the choices on a graph-structured stack.

## When to use it

Use LALR(1) through a parser generator when the language has a deterministic grammar and you want a fast parser with a compact table, as in most programming language front ends. Use [canonical LR(1)](/canonical-lr-parsing/) or IELR(1) if a grammar that is LR(1) shows reduce-reduce conflicts only under LALR. Use [GLR](/glr-parsing/) or the [Earley parser](/earley-parser/) if the grammar is ambiguous or needs more than one terminal of lookahead.

## Pitfalls

- **Mysterious reduce-reduce conflicts.** The grammar $S \to a A d \mid b B d \mid a B e \mid b A e$, $A \to c$, $B \to c$ is LR(1) with 14 LR(1) states. After $a\,c$ the LR(1) state holds $[A \to c \bullet, d]$ and $[B \to c \bullet, e]$; after $b\,c$ it holds $[A \to c \bullet, e]$ and $[B \to c \bullet, d]$. LALR merges the two into one state, where both reductions have lookahead $\{d, e\}$, and the table has two conflicts. Such conflicts are hard to explain to the grammar author, because they come from paths that the author does not see together.
- **Useless symbols.** If a nonterminal derives no terminal string, $\mathrm{FIRST}(\beta a)$ can be empty, and some LR(0) items get no lookahead. Remove [useless symbols](/useless-symbol-elimination/) first.
- **Conflicts resolved by default.** yacc resolves a shift-reduce conflict in favor of the shift and a reduce-reduce conflict in favor of the earlier production, with only a warning. A grammar with warnings may parse a language other than the one it describes.
- **Error positions.** Because of delayed error detection, the state at the error may have lost information that a canonical LR(1) parser still has; error messages that list the expected terminals can then be wrong.

## Implementations

## History

Knuth defined LR(k) grammars and their canonical parsers in 1965, but the tables were too large for the computers of the time. DeRemer's 1969 MIT thesis introduced LALR(k) parsers and his 1971 paper introduced SLR(k), both on the LR(0) automaton. Stephen Johnson's yacc at Bell Labs, in the early 1970s, built LALR(1) tables with precedence declarations, and through Unix it made LALR(1) the usual method of parser generators. DeRemer and Pennello published their efficient lookahead computation in 1982, and GNU Bison, a free replacement for yacc, uses it.

## References
