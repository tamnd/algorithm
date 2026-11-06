---
tag: 12M6QZ
kind: algorithm
slug: canonical-lr-parsing
name: Canonical LR(1) parsing
aliases:
- Canonical LR parsing
- Knuth LR(1)
- LR(1) parsing
- canonical LR parsing
- canonical LR(1)
area: automata-and-parsing/context-free-parsing
level: core
summary: The most powerful LR parser with one token of lookahead, using full LR(1) item sets.
solves: [cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the input length, g: the grammar size, σ: the number of terminals, N: the number of LR(1) item sets}
  time: {worst: O(n), build: O(N g^3 σ^2)}
  space: {extra: O(n), table: O(N (g + σ))}
properties: {deterministic: true, recursive: false}
history:
  year: 1965
  people: [Donald E. Knuth]
  note: Knuth defined the LR(k) grammars and built their parsers from sets of items with k symbols of lookahead.
prereqs: [lr-item, viable-prefix, first-and-follow-sets, shift-reduce-parsing]
see_also: [lalr-parsing, slr-parsing, lr0-parsing, lr-item-sets, lr-k-grammar, lr-parse-table, glr-parsing, yacc]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.7, More Powerful LR Parsers (4.7.1 Canonical LR(1) Items, 4.7.2 Constructing LR(1) Sets of Items, 4.7.3 Canonical LR(1) Parsing Tables, 4.7.4 Constructing LALR Parsing Tables)
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (the LR(k) condition, the sets of states with lookahead strings, and the linear-time parser)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 9, Deterministic Bottom-Up Parsing (the LR(1) and LALR(1) sections)
  - paper: doi:10.1145/362619.362625
    title: Frank L. DeRemer, Simple LR(k) grammars, Communications of the ACM 14(7) (1971)
    locator: pp. 453 to 460 (LR(0) states with lookahead added afterwards, the smaller alternative to the canonical construction)
  - paper: doi:10.1007/BF00290336
    title: David Pager, A practical general method for constructing LR(k) parsers, Acta Informatica 7(3) (1977)
    locator: pp. 249 to 268 (merging compatible LR(1) states without new conflicts)
  - paper: doi:10.1016/0022-0000(83)90010-7
    title: Esko Ukkonen, Lower bounds on the size of deterministic parsers, Journal of Computer and System Sciences 26(2) (1983)
    locator: pp. 153 to 170 (grammars whose deterministic parsers must have exponential size)
---

Canonical LR(1) parsing is the [LR parsing](/lr-parsing/) method of Knuth with one token of lookahead: its states are the full sets of [LR(1) items](/lr-item/), each item a dotted production with one lookahead terminal. A [grammar](/context-free-grammar/) gets a table without conflicts exactly when it is an [LR(1) grammar](/lr-k-grammar/), so the method accepts more grammars than [SLR](/slr-parsing/) and [LALR](/lalr-parsing/). For such a grammar the parser solves the [parsing problem](/cfg-parsing-problem/) in $O(n)$ time with a [shift-reduce](/shift-reduce-parsing/) stack. The price is the size of the table, which can be exponential in the size of the grammar.

## In plain words

A shift-reduce parser reads tokens onto a stack and must decide at each step: read the next token, or replace the top of the stack by a grammar rule. An LR parser makes this decision with a finite automaton that reads the stack.

Each state of the automaton is a list of guesses. A guess says "I may be in the middle of this rule, at this point, and after the rule I expect this token." When the next token can only continue a rule, the parser reads it. When a rule is complete and the next token is one that the guess expects after it, the parser replaces the rule.

The canonical method keeps the expected next token in every guess, with no merging. That is the most information one token can give, so it accepts the most grammars, but it can need many states.

## The problem

**Notation.** The grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $n$ is the length of the input $w$, and $|G|$, written $g$ in the front matter, is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. The *augmented grammar* adds a new start symbol $S'$ with the one production $S' \to S$, and an end marker $\$ \notin \Sigma$ is put after the input. The number of terminals is $\sigma$.

The input is a grammar $G$ and a string $w \in \Sigma^*$. The output is a rightmost [derivation](/derivation/) of $w$, given as its reductions in reverse order, or the answer that $w \notin L(G)$. This is the [parsing problem](/cfg-parsing-problem/) for a grammar that is LR(1). For other grammars the table has a conflict, and the method reports it.

An *LR(1) item* $[A \to \alpha \cdot \beta, a]$ is a production with a dot in its right side and a lookahead $a \in \Sigma \cup \{\$\}$. The item is *valid* for a string $\gamma$ of grammar symbols if there is a rightmost derivation

$$S' \Rightarrow^*_{rm} \delta A x \Rightarrow_{rm} \delta \alpha \beta x$$

with $\gamma = \delta\alpha$ and $a$ the first symbol of $x\$$. The strings with a valid item are the [viable prefixes](/viable-prefix/). For a string $\theta$ of grammar symbols, FIRST$(\theta)$ is the set of terminals that begin a string derived from $\theta$, from the [FIRST sets](/first-and-follow-sets/) of the symbols.

## The algorithm

The construction builds the collection $C$ of item sets, one per state, by a breadth-first search over GOTO, and then fills the ACTION and GOTO tables. The driver runs the [shift-reduce](/shift-reduce-parsing/) loop with a stack of states.

```pseudo id=main
BUILD-TABLES(G)                            ▷ G augmented with S' → S
L1  I0 ← CLOSURE({[S' → ·S, $]})
L2  C ← the list (I0)                      ▷ state k is the item set C[k]
L3  k ← 0; while k < |C| do
L4      for each symbol X that follows a dot in an item of C[k] do
L5          J ← GOTO(C[k], X)
L6          if J is not in C then append J to C
L7          T[k, X] ← the index of J in C
L8      k ← k + 1
L9  for each state k and each item of C[k] do      ▷ two different actions in one entry are a conflict
L10     if the item is [A → α·aβ, b] with a ∈ Σ then ACTION[k, a] ← shift T[k, a]
L11     else if it is [A → α·, a] with A ≠ S' then ACTION[k, a] ← reduce A → α
L12     else if it is [S' → S·, $] then ACTION[k, $] ← accept
L13 GOTO-TABLE[k, A] ← T[k, A] for each state k and nonterminal A with T[k, A] defined

CLOSURE(I)
L14 J ← I
L15 for each [A → α·Bβ, a] in J with B ∈ V, each B → γ in R and each b ∈ FIRST(βa), add [B → ·γ, b] to J
L16 repeat line L15 until J does not change; return J

GOTO(I, X)
L17 return CLOSURE({[A → αX·β, a] : [A → α·Xβ, a] ∈ I})

LR-PARSE(w)
L18 push state 0 on an empty stack; a ← the first symbol of w$
L19 loop
L20     s ← the state on top of the stack
L21     if ACTION[s, a] = shift t then push t; a ← the next symbol of w$
L22     else if ACTION[s, a] = reduce A → β then pop |β| states; push GOTO-TABLE[top, A]; output A → β
L23     else if ACTION[s, a] = accept then return the output
L24     else return error                      ▷ the entry is empty
```

Line L15 is the heart of the method. If the parser may be about to see $B$ followed by $\beta$, with $a$ after the rule, then it may be about to see the right side of any production of $B$, followed by any terminal that can begin $\beta a$. GOTO moves the dot over one symbol, which is what a shift or the push after a reduction does. Line L22 pops $|\beta|$ states, none for an $\varepsilon$-production, and uses the state below them to decide where $A$ goes.

## Example

Take the grammar

$$S \to C C, \qquad C \to c C \mid d,$$

with the productions numbered 1: $S \to CC$, 2: $C \to cC$, 3: $C \to d$. Its language is $c^* d \, c^* d$. A lookahead written $c/d$ stands for two items, one with each lookahead.

| state | items | reached by |
|---|---|---|
| $I_0$ | $[S' \to \cdot S, \$]$, $[S \to \cdot CC, \$]$, $[C \to \cdot cC, c/d]$, $[C \to \cdot d, c/d]$ | start |
| $I_1$ | $[S' \to S \cdot, \$]$ | $I_0$ on $S$ |
| $I_2$ | $[S \to C \cdot C, \$]$, $[C \to \cdot cC, \$]$, $[C \to \cdot d, \$]$ | $I_0$ on $C$ |
| $I_3$ | $[C \to c \cdot C, c/d]$, $[C \to \cdot cC, c/d]$, $[C \to \cdot d, c/d]$ | $I_0, I_3$ on $c$ |
| $I_4$ | $[C \to d \cdot, c/d]$ | $I_0, I_3$ on $d$ |
| $I_5$ | $[S \to CC \cdot, \$]$ | $I_2$ on $C$ |
| $I_6$ | $[C \to c \cdot C, \$]$, $[C \to \cdot cC, \$]$, $[C \to \cdot d, \$]$ | $I_2, I_6$ on $c$ |
| $I_7$ | $[C \to d \cdot, \$]$ | $I_2, I_6$ on $d$ |
| $I_8$ | $[C \to cC \cdot, c/d]$ | $I_3$ on $C$ |
| $I_9$ | $[C \to cC \cdot, \$]$ | $I_6$ on $C$ |

In $I_0$, the item $[S \to \cdot CC, \$]$ gives the items of $C$ with the lookaheads FIRST$(C\$) = \{c, d\}$, because the first $C$ is followed by a second $C$. In $I_2$ the second $C$ is followed by nothing, so its items get the lookahead $\$$. The tables, with s$k$ for shift to state $k$ and r$p$ for reduce by production $p$, are these.

| state | $c$ | $d$ | $\$$ | GOTO $S$ | GOTO $C$ |
|---|---|---|---|---|---|
| 0 | s3 | s4 | | 1 | 2 |
| 1 | | | accept | | |
| 2 | s6 | s7 | | | 5 |
| 3 | s3 | s4 | | | 8 |
| 4 | r3 | r3 | | | |
| 5 | | | r1 | | |
| 6 | s6 | s7 | | | 9 |
| 7 | | | r3 | | |
| 8 | r2 | r2 | | | |
| 9 | | | r2 | | |

The parse of $cdd$:

| stack of states | rest of the input | action |
|---|---|---|
| 0 | c d d \$ | shift 3 |
| 0 3 | d d \$ | shift 4 |
| 0 3 4 | d \$ | reduce $C \to d$, GOTO$(3, C) = 8$ |
| 0 3 8 | d \$ | reduce $C \to cC$, GOTO$(0, C) = 2$ |
| 0 2 | d \$ | shift 7 |
| 0 2 7 | \$ | reduce $C \to d$, GOTO$(2, C) = 5$ |
| 0 2 5 | \$ | reduce $S \to CC$, GOTO$(0, S) = 1$ |
| 0 1 | \$ | accept |

The four reductions, read backwards, give $S \Rightarrow CC \Rightarrow Cd \Rightarrow cCd \Rightarrow cdd$. On the input $cd$ the parser shifts into states 3 and 4 and then sees $\$$. State 4 has no entry for $\$$, so the parser stops there. This is the first point where the input stops being a prefix of a sentence.

The states $I_3$ and $I_6$ have the same items without the lookaheads (the same *core*), and so do $I_4$ and $I_7$, and $I_8$ and $I_9$. [LALR](/lalr-parsing/) merges the states with the same core, which gives 7 states and no conflict here. For the expression grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (E) \mid \mathtt{id}$ there are 22 canonical states and 12 cores.

**A grammar that is LR(1) but not LALR(1).** For

$$S \to a A d \mid b B d \mid a B e \mid b A e, \qquad A \to c, \qquad B \to c,$$

the canonical collection has 14 states. After $ac$ the state holds $[A \to c \cdot, d]$ and $[B \to c \cdot, e]$, and after $bc$ it holds $[A \to c \cdot, e]$ and $[B \to c \cdot, d]$. Each state tells by the lookahead which reduction to make. The two states have the same core, so LALR merges them into one state with 13 states in total, and in the merged state both $A \to c$ and $B \to c$ are reductions on $d$ and on $e$: a [reduce-reduce conflict](/reduce-reduce-conflict/).

## Correctness

Three facts, proved in full below, give the correctness.

- **Validity.** Every item valid for a viable prefix $\gamma$ is in the state that the automaton reaches from $I_0$ by reading $\gamma$. The proof is by induction on the length of the derivation that makes the item valid, and on the position of the dot. A GOTO step handles a dot after a symbol, and line L15 handles an item that closure adds.
- **Soundness.** The parser keeps the invariant that the stack symbols derive the input read so far, by the reductions output, read backwards, as rightmost steps. Accept happens only when the stack holds state 0 and the state reached from it on $S$, and the whole input is read. So an output is a rightmost derivation of $w$, whether or not the table has conflicts.
- **Completeness.** Let the table have no conflict and $w \in L(G)$, with a parse tree $T$. At each step, the next event of a postorder walk of $T$ (shift the next leaf, or reduce the next inner node) comes from an item that is valid for the stack, so by validity it is in the table, and it is the only entry. The parser therefore performs the postorder of $T$ and accepts. Because the parser is deterministic, $T$ is the only parse tree: a grammar with a table free of conflicts is unambiguous.

The full proof: [correctness](proofs/correctness.md).

## Complexity

**Parsing.** Assume a table without conflicts and a grammar without [useless symbols](/useless-symbol-elimination/). Each step takes $O(1)$ time, except that a reduce pops $|\beta|$ states, at most a constant for a fixed grammar. There are at most $n$ shifts. For the reductions, take any moment of the run: by the correct-prefix property the run so far is also the start of the run on some sentence $w'$, and each reduction so far made a node of the unique parse tree of $w'$, inside the subtrees of the stack symbols. In that tree, a node and a descendant with the same span have different labels, since otherwise removing the part between them would give a second tree. So a subtree whose yield has length $\ell \ge 1$ has $O(\ell)$ nodes, and a subtree with empty yield has a bounded number. The stack symbols with empty yield come in blocks of fewer than $N$, because a repeated state inside a block would make the parser loop forever on $w'$. Together these bound the reductions by $O(n)$, and the stack by $O(n)$ states, for accepted and rejected inputs alike. The constant grows with $N$. The proof: [parsing time](proofs/complexity.md).

**Building the tables.** Let $M$ be the number of LR(1) items. It is at most $|G| (\sigma + 1)$, because a production $A \to \alpha$ has $1 + |\alpha|$ dot positions. A CLOSURE adds each item once, and for each item it reads the productions of one nonterminal for each lookahead, so it takes $O(M \cdot |G| \sigma) = O(|G|^2 \sigma^2)$ time. A state calls GOTO for at most $|G|$ symbols, and a lookup of the new item set, kept as a vector of $M$ flags in a trie, takes $O(M)$. So the construction takes $O(N |G|^3 \sigma^2)$ time for $N$ states, and the tables have $O(N (|G| + \sigma))$ entries. The bound is crude, but $N$ dominates it: $N$ can be exponential in $|G|$.

**The number of states.** $N \le 2^M$. For the grammar with productions $S \to A_i$, $A_i \to a_j A_i$ for $j \ne i$, and $A_i \to a_i$, for $1 \le i, j \le k$, we have $|G| = 3k^2 + k$, the table has no conflict, and the canonical collection has at least $2^k - 1$ states. Take a nonempty set $U$ of letters other than the full set, and a string $u$ that uses exactly the letters of $U$, with last letter $a_j$. The state reached by $u$ holds the item $[A_i \to a_j \cdot A_i, \$]$ exactly for the $i \notin U$. So the $2^k - 2$ sets $U$ give different states, and $I_0$ is one more. With $k = 1, \ldots, 6$ the collection has 4, 12, 32, 78, 182 and 416 states. Ukkonen proved lower bounds of this kind for every deterministic parser of some grammars, so the blow-up is not only a fault of the canonical construction.

| measure | bound |
|---|---|
| time to parse | $O(n)$ |
| extra space to parse | $O(n)$ |
| time to build | $O(N g^3 \sigma^2)$ |
| table size | $O(N (g + \sigma))$ |

## Properties

- **Deterministic.** For an LR(1) grammar each table entry has at most one action, and the parser never backs up.
- **Not recursive.** The driver is one loop with an explicit stack, so deep nesting in the input does not use the call stack.
- **The correct-prefix property.** For a grammar without useless symbols, the parser reads a token only if the input read so far, with that token, is a prefix of some sentence. So it reports an error at the first token where no sentence can continue.
- **The largest class with one token.** For a grammar without useless symbols, the tables have no conflict exactly when the grammar is LR(1). The languages of these grammars are the [deterministic context-free languages](/deterministic-context-free-language/), and canonical LR(1) parsers exist for every one of them.
- **Valid items equal state items.** For a grammar without useless symbols, the state reached by $\gamma$ holds exactly the items valid for $\gamma$. LALR and SLR states can hold more lookaheads, so their parsers can make some reductions before they detect an error, although they shift no wrong token either.

## Variants and improvements

- **[LALR(1)](/lalr-parsing/).** Merge the states with the same core and take the union of their lookaheads. The table has as many states as the [LR(0)](/lr0-parsing/) automaton: for a language like C, several hundred states instead of several thousand. Merging can add reduce-reduce conflicts, as in the example, but never a shift-reduce conflict. [Yacc](/yacc/) and Bison build LALR(1) tables by default.
- **[SLR(1)](/slr-parsing/).** Use the LR(0) states and reduce by $A \to \alpha$ on every token of FOLLOW$(A)$. It is simpler and accepts fewer grammars than LALR(1).
- **Pager's method and IELR.** Merge two canonical states only when the merge adds no conflict. The result has about the size of the LALR table and accepts every LR(1) grammar. Bison offers this as `%define lr.type ielr` and the full canonical table as `%define lr.type canonical-lr`.
- **LR(k) for $k \ge 2$.** Items carry lookahead strings of length $k$, and FIRST becomes FIRST$_k$. Every LR(k) language is also LR(1), so larger $k$ only helps with a given grammar, at a large cost in table size.
- **[GLR](/glr-parsing/).** Keep all actions of a conflict and run them in parallel on a graph-structured stack. This parses every context-free grammar and stays linear on the LR(1) parts.
- **Default reductions and table compression.** A state whose only reduction is $A \to \alpha$ can reduce on every token. This shrinks the table, and it delays the error until the next shift, which keeps the correct-prefix property for shifts.

## When to use it

Use a canonical LR(1) table when the grammar is LR(1) but LALR(1) gives a reduce-reduce conflict, and the grammar should not be rewritten. Use it also when the error must be found as early as possible, before any spurious reduction. In most other cases a generator with LALR(1) or IELR(1) tables gives the same parser with far fewer states. The method is a poor fit for an ambiguous grammar: resolve the ambiguity with precedence rules, or use [GLR](/glr-parsing/) or the [Earley parser](/earley-parser/).

## Pitfalls

- **Popping an empty right side.** A reduction by $A \to \varepsilon$ pops no state. In Python, `del stack[-0:]` deletes the whole stack, so the pop needs a guard for $|\beta| = 0$.
- **Lookaheads of closure items.** The lookahead of $[B \to \cdot\gamma, b]$ comes from FIRST$(\beta a)$, not from FOLLOW$(B)$. With FOLLOW the construction becomes a variant of SLR and loses the power of the method.
- **Nullable symbols in FIRST.** FIRST$(\beta a)$ must go past each symbol of $\beta$ that derives $\varepsilon$, and include $a$ when all of $\beta$ is nullable. Stopping at the first symbol misses lookaheads and makes a wrong table without a conflict.
- **The end marker in the grammar.** The marker $\$$ must not be a terminal of $G$, or the parser can accept before the end of the input.
- **Equality of item sets.** Two states are the same only when their items, lookaheads included, are the same. Comparing cores gives LALR, not the canonical collection.
- **Conflicts in a grammar with useless symbols.** A nonterminal that derives no terminal string can produce items that are never valid, and their conflicts are not real. Remove [useless symbols](/useless-symbol-elimination/) before building the table.

## Implementations

## History

Donald Knuth defined the LR(k) grammars in 1965. He showed that their parsers can be built from sets of states with lookahead strings, that they run in linear time, and that the LR(k) languages are the languages of deterministic pushdown automata. The tables were too large for the computers of the time. Frank DeRemer introduced LALR in his 1969 thesis and SLR in 1971, both based on the much smaller LR(0) automaton, and yacc, from the early 1970s, made LALR(1) the standard. David Pager showed in 1977 how to merge canonical states without new conflicts, and Esko Ukkonen proved in 1983 that some grammars need deterministic parsers of exponential size.

## References
