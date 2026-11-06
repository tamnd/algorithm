---
tag: R5HRV8
kind: algorithm
slug: lr-parsing
name: LR(k) parsing
aliases:
- Knuth LR parsing
- LR parsing
- shift-reduce LR parsing
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Shift-reduce parser using k tokens of lookahead, recognizing all deterministic CFLs.
solves: [cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the number of input tokens, k: the number of lookahead tokens, G: fixed}
  time: {worst: O(k n), best: O(k)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1965
  people: [Donald E. Knuth]
  note: Knuth defined the LR(k) grammars, built the canonical parser from sets of items with k-token lookaheads, and showed that the LR(k) languages are exactly the deterministic context-free languages.
prereqs: [lr-item, lr-parse-table, lr-grammar]
see_also: [canonical-lr-parsing, lalr-parsing, slr-parsing, lr0-parsing, viable-prefix, ll-k-parsing, glr-parsing, deterministic-context-free-language]
sources:
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (LR(k) grammars, the item-set construction, and the equivalence with deterministic languages)
  - book: isbn:9780139145568
    title: Alfred V. Aho and Jeffrey D. Ullman, The Theory of Parsing, Translation, and Compiling, Volume I, Parsing
    locator: Section 5.2, Deterministic Bottom-Up Parsing (LR(k) grammars, sets of LR(k) items and the canonical LR(k) parser)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.7, More Powerful LR Parsers (4.7.1 to 4.7.3, canonical LR(1) items and tables)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 9, Deterministic Bottom-Up Parsing
---

LR(k) parsing is Knuth's deterministic bottom-up method: it reads the input from left to right, builds a rightmost derivation in reverse, and decides each shift or reduction from the stack and the next $k$ tokens. The stack is summarized by a state of a finite automaton whose states are sets of [LR items](/lr-item/) with lookahead strings, so each decision is one table lookup. It parses exactly the [LR(k) grammars](/lr-grammar/), which include every LL(k) grammar and many left-recursive ones, and for $k \ge 1$ their languages are exactly the [deterministic context-free languages](/deterministic-context-free-language/).

## In plain words

The parser reads words one at a time and keeps a pile of finished pieces. A piece is a word, or a group of pieces that a rule has joined. After each word, the parser asks whether the top pieces of the pile form the right side of a rule that should be joined now. If so, it replaces them by the rule's left side, and asks again. If not, it reads the next word.

To decide, it looks at the next few words and at its state, a single number that sums up the pile. A table built in advance maps the state and the next words to "read", "join by this rule" or "error". When the table never gives two answers, the parser never guesses. When the pile ends as the start symbol alone and the input is used up, the input is a sentence.

## The problem

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area.

$\mathrm{FIRST}_k$ and the $k$-concatenation $\oplus_k$ are as on the [LL(k) parsing](/ll-k-parsing/) page: lookahead strings have at most $k$ tokens, and a shorter one means that the input ends there. The grammar is *augmented* with a new start symbol $S'$ and the production $S' \to S$.

The input is a grammar in which every nonterminal derives some terminal string, a number $k \ge 0$, and tokens $w = a_1 \cdots a_n$. The output is a [parse tree](/parse-tree/) of $w$ when $w \in L(G)$, and otherwise an error at the first token where $w$ stops being a prefix of a sentence. The grammar is LR(k) when, in every rightmost derivation, the [handle](/handle/) of a right-sentential form $\alpha \beta y$ and its production are determined by $\alpha \beta$ and $\mathrm{FIRST}_k(y)$; see [LR grammar](/lr-grammar/).

## The algorithm

An *LR(k) item* $[A \to \beta_1 \cdot \beta_2, u]$ is a production with a dot and a lookahead string $u$ of at most $k$ tokens. It says: the stack ends with $\beta_1$, and after $\beta_2$ the input should continue with $u$. The *closure* of a set of items adds $[B \to \cdot \delta, v]$ for every item $[A \to \beta_1 \cdot B \beta_2, u]$ in the set, every production $B \to \delta$ and every $v \in \mathrm{FIRST}_k(\beta_2) \oplus_k \{u\}$, until nothing changes. The states are the closed sets reachable from $I_0 = \mathrm{CLOSURE}(\{[S' \to \cdot S, \varepsilon]\})$ by $\mathrm{GOTO}(I, X) = \mathrm{CLOSURE}(\{[A \to \beta_1 X \cdot \beta_2, u] : [A \to \beta_1 \cdot X \beta_2, u] \in I\})$.

```pseudo id=main
LR-PARSE(ACTION, GOTO, k, w)             ▷ w = a1 ⋯ an
L1  push the state I0; i ← 1
L2  loop
L3      s ← the state on top; u ← ai ⋯ a_min(i+k−1, n)
L4      if ACTION[s, u] is empty then error at a(i+d), where d is the length of the longest common prefix of u and a key of ACTION[s]
L5      if ACTION[s, u] = shift then
L6          if i > n or GOTO[s, ai] is empty then error at ai
L7          push the leaf ai and the state GOTO[s, ai]; i ← i + 1
L8      else if ACTION[s, u] = reduce A → β then
L9          pop |β| entries, and make their trees the children of a new node A
L10         push the node A and the state GOTO[s′, A], where s′ is the state now on top
L11     else (accept) if i ≤ n then error at ai, else return the tree on top
```

The tables are built once. Lines L6 and L11 matter only for $k = 0$, where the lookahead is always $\varepsilon$ and does not show the next token.

```pseudo id=build
LRK-TABLES(G, k)
L12 add S′ → S to G and compute FIRST_k of every nonterminal
L13 I0 ← CLOSURE({[S′ → ·S, ε]}); put I0 in the queue
L14 for each state I taken from the queue
L15     for each symbol X after a dot in I: GOTO[I, X] ← GOTO(I, X), queueing it if it is new
L16 for each state I and item [A → β1 · a β2, u] ∈ I with a ∈ Σ: set ACTION[I, v] ← shift for each v ∈ FIRST_k(a β2) ⊕k {u}
L17 for each item [A → β ·, u] ∈ I: set ACTION[I, u] ← reduce A → β, or accept when A = S′
L18 if a cell gets two different actions then report "not LR(k)"
```

A conflict at line L18 is a [shift-reduce conflict](/shift-reduce-conflict/) or a [reduce-reduce conflict](/reduce-reduce-conflict/); it occurs if and only if the grammar is not LR(k). The [LR parse table](/lr-parse-table/) page shows the same driver with the smaller tables of [SLR](/slr-parsing/) and [LALR](/lalr-parsing/) parsing, which use LR(0) states and approximate lookaheads.

## Example

The grammar

$$1: S \to A b c \qquad 2: S \to B b d \qquad 3: A \to a \qquad 4: B \to a$$

has the language $\{abc, abd\}$. After reading $a$, the parser must reduce it to $A$ or to $B$, and the token $b$ after it does not tell which: only the token after $b$ does. So the grammar is not LR(1), and it is LR(2). With $k = 2$ the states are:

| state | items | ACTION | GOTO |
|---|---|---|---|
| 0 | $[S' \to \cdot S, \varepsilon]$, $[S \to \cdot A b c, \varepsilon]$, $[S \to \cdot B b d, \varepsilon]$, $[A \to \cdot a, bc]$, $[B \to \cdot a, bd]$ | $ab$: shift | $S$: 3, $A$: 1, $B$: 2, $a$: 4 |
| 1 | $[S \to A \cdot b c, \varepsilon]$ | $bc$: shift | $b$: 5 |
| 2 | $[S \to B \cdot b d, \varepsilon]$ | $bd$: shift | $b$: 6 |
| 3 | $[S' \to S \cdot, \varepsilon]$ | $\varepsilon$: accept | |
| 4 | $[A \to a \cdot, bc]$, $[B \to a \cdot, bd]$ | $bc$: reduce 3; $bd$: reduce 4 | |
| 5 | $[S \to A b \cdot c, \varepsilon]$ | $c$: shift | $c$: 7 |
| 6 | $[S \to B b \cdot d, \varepsilon]$ | $d$: shift | $d$: 8 |
| 7 | $[S \to A b c \cdot, \varepsilon]$ | $\varepsilon$: reduce 1 | |
| 8 | $[S \to B b d \cdot, \varepsilon]$ | $\varepsilon$: reduce 2 | |

State 4 is where the lookahead does its work: the two complete items have the lookaheads $bc$ and $bd$. With $k = 1$ both would be $b$, a reduce-reduce conflict. The parser on $a \, b \, d$:

| step | stack | rest of the input | lookahead | action |
|---|---|---|---|---|
| 1 | $0$ | $a b d$ | $ab$ | shift, go to 4 |
| 2 | $0 \ a \ 4$ | $b d$ | $bd$ | reduce by 4, $B \to a$; GOTO[0, B] = 2 |
| 3 | $0 \ B \ 2$ | $b d$ | $bd$ | shift, go to 6 |
| 4 | $0 \ B \ 2 \ b \ 6$ | $d$ | $d$ | shift, go to 8 |
| 5 | $0 \ B \ 2 \ b \ 6 \ d \ 8$ | | $\varepsilon$ | reduce by 2, $S \to B b d$; GOTO[0, S] = 3 |
| 6 | $0 \ S \ 3$ | | $\varepsilon$ | accept |

The reductions, read backward, give the rightmost derivation $S \Rightarrow B b d \Rightarrow a b d$. On $a \, b \, b$ the parser shifts $a$ and finds no entry for $bb$ in state 4. The longest common prefix with a key is $b$, so the error is at the third token: $ab$ starts a sentence and $abb$ does not.

For the expression grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to ( E ) \mid id$, the canonical LR(1) automaton has 22 states, against 12 for the LR(0) automaton that SLR and LALR use: canonical LR(1) splits states that differ only in their lookaheads.

## Correctness

Assume every nonterminal derives a terminal string and LRK-TABLES reports no conflict. Three lemmas about the item sets do the work.

- **Validity.** Every item in the state reached by a stack $\gamma$ is *valid* for $\gamma$: some rightmost derivation $S' \Rightarrow_{rm}^* \alpha A y \Rightarrow_{rm} \alpha \beta_1 \beta_2 y$ has $\gamma = \alpha \beta_1$ and $\mathrm{FIRST}_k(y) = u$.
- **Completeness.** Every node of a parse tree gives such an item in the right state.
- **Keys.** The keys of a state cover $\mathrm{FIRST}_k(\beta_2) \oplus_k \{u\}$ for each of its items.

Here is how the lemmas give the result. A parse that accepts returns a parse tree, since each reduction joins trees by a production. On a sentence the parser builds the nodes of its tree in postorder, because completeness puts the right action in each cell and there is no conflict. Validity makes every key a $\mathrm{FIRST}_k$ of a real continuation of the input read so far. The keys lemma keeps the tokens already seen as lookahead consistent with the next state. Together they give the exact error position. Termination with a linear number of steps is Knuth's theorem, which the proof cites. The full proof is below.

## Complexity

- **Parsing.** For a fixed LR(k) grammar the parser makes $O(n + 1)$ moves (Knuth, 1965): $n$ shifts and $O(n + 1)$ reductions, since the parse tree of a sentence has $O(n + 1)$ nodes. Each move reads a lookahead of $k$ tokens, so the time is $O(k n)$, or $O(n)$ with a rolling encoding of the window. The stack takes $O(n)$ space.
- **Tables.** The number of canonical LR(k) states can be exponential in the size of the grammar, and it grows with $k$, because each item carries one of up to $\sum_{j \le k} |\Sigma|^j$ lookaheads. This is why practical generators use [LALR(1)](/lalr-parsing/), which has as many states as the LR(0) automaton, or merge compatible canonical states.

## Properties

- **Deterministic, online, no backtracking.** Each token is shifted once.
- **Valid prefix property.** An error at $a_j$ means that $a_1 \cdots a_{j-1}$ starts a sentence and $a_1 \cdots a_j$ does not. The canonical tables never reduce on a lookahead that cannot follow; SLR and LALR tables may make a few extra reductions before they find the same error.
- **Power.** The tables have no conflict exactly for LR(k) grammars. Every LL(k) grammar is LR(k), left recursion is welcome, and every LR(k) grammar is unambiguous.
- **Languages.** For each $k \ge 1$, the LR(k) languages are exactly the deterministic context-free languages, so any LR(k) grammar can be replaced by an LR(1) grammar for the same language. The LR(0) languages are the deterministic languages with the prefix property, where no sentence is a proper prefix of another.

## Variants and improvements

- **SLR(1) and LALR(1).** Use the LR(0) automaton and add lookaheads from FOLLOW sets ([SLR](/slr-parsing/)) or from merged LR(1) states ([LALR](/lalr-parsing/)). The tables are much smaller, and the class is a little smaller than LR(1). [Yacc](/yacc/) and its successors are LALR(1).
- **Canonical LR(1).** The case $k = 1$, described on the [canonical LR parsing](/canonical-lr-parsing/) page. Pager's and later state-merging methods give the full LR(1) class with tables close to LALR size.
- **GLR.** [GLR parsing](/glr-parsing/) runs the same automaton on all actions of a conflicting cell at once, with a graph-structured stack, and handles every context-free grammar.
- **Precedence declarations.** Generators resolve some conflicts of ambiguous expression grammars by operator precedence and associativity, which keeps the grammar short while the parser stays deterministic.

## When to use it

Use an LR parser generator when the grammar is natural for the language but not LL: left recursion, long common prefixes, or decisions that need the whole right side. In practice that means LALR(1) or a minimal LR(1) generator; canonical LR(k) with $k \ge 2$ is mainly of theoretical interest, since every LR(k) language has an LR(1) grammar. For ambiguous grammars use [GLR](/glr-parsing/) or the [Earley parser](/earley-parser/), and for hand-written parsers [recursive descent](/recursive-descent-parsing/).

## Pitfalls

- **Forgetting the augmented start.** Without $S' \to S$, the parser cannot tell when to accept, and a start symbol that occurs on a right side causes spurious conflicts or early acceptance.
- **Accepting with input left.** With $k = 0$ the accept action does not see the input, so the driver must check that all tokens were shifted (line L11).
- **Error position.** With $k \ge 2$ the bad token can be inside the lookahead window; report it, not the current position.
- **Table size.** Canonical LR(k) tables blow up quickly; a grammar that needs $k \ge 2$ is usually better rewritten, or parsed with a generalized method.

## Implementations

## History

Knuth (1965) introduced the LR(k) grammars and the canonical construction, and proved that they generate exactly the deterministic languages. His tables were too large for the machines of the time. Korenjak (1969) split grammars into smaller parts, and DeRemer (1969, 1971) gave the SLR and LALR methods, which made LR parsing practical; Johnson's Yacc (1975) made LALR(1) the standard for compiler front ends. Pager (1977) showed how to merge canonical states without losing the LR(1) property. Tomita (1985) turned the LR automaton into a general parser for any grammar, the start of [GLR parsing](/glr-parsing/).

## References
