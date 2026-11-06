---
tag: VNTPSZ
kind: algorithm
slug: ll-k-parsing
name: LL(k) parsing
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Top-down deterministic parser using k tokens of lookahead.
solves: [cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the number of input tokens, k: the number of lookahead tokens, G: fixed}
  time: {worst: O(k n), best: O(k)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1968
  people: [Philip M. Lewis II, Richard E. Stearns]
  note: Lewis and Stearns defined the LL(k) grammars; Rosenkrantz and Stearns (1970) studied their properties, and the parser driven by one table for each nonterminal and right context is the form given by Aho and Ullman (1972).
prereqs: [ll-grammar, ll1-parsing, first-and-follow-sets]
see_also: [ll-k-grammar, ll-parse-table, lookahead-parsing, ll-star-parsing, recursive-descent-parsing, top-down-parsing, lr-parsing, left-factoring]
sources:
  - book: isbn:9780139145568
    title: Alfred V. Aho and Jeffrey D. Ullman, The Theory of Parsing, Translation, and Compiling, Volume I, Parsing
    locator: Section 5.1, LL(k) Grammars (the LL(k) tables, the parsing algorithm that uses them, and strong LL(k) grammars)
  - paper: doi:10.1016/S0019-9958(70)90446-8
    title: D. J. Rosenkrantz and R. E. Stearns, Properties of deterministic top-down grammars, Information and Control 17(3) (1970)
    locator: pp. 226 to 256
  - paper: doi:10.1145/321466.321477
    title: P. M. Lewis II and R. E. Stearns, Syntax-directed transduction, Journal of the ACM 15(3) (1968)
    locator: pp. 465 to 488 (the definition of LL(k) grammars)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 8, Deterministic Top-Down Parsing (the sections on LL(k) and strong LL(k) parsing)
---

LL(k) parsing is deterministic top-down parsing with $k$ tokens of lookahead: it builds the [leftmost derivation](/leftmost-derivation/) of the input from left to right, and at each nonterminal it chooses the production from the next $k$ tokens. For $k \ge 2$ the next tokens alone are not always enough to name the production, because the tokens that may follow a nonterminal depend on where it occurs; the parser therefore keeps, with each nonterminal on its stack, a table for that nonterminal in its right context. For every [LL(k) grammar](/ll-grammar/) it accepts exactly the sentences, builds their [parse trees](/parse-tree/), and runs in time linear in the input.

## In plain words

The parser keeps a to-do list of grammar symbols, like an [LL(1) parser](/ll1-parsing/), but it may peek at the next $k$ words of the input instead of one. A word on the list must match the next input word. A placeholder on the list is replaced by the symbols of one of its rules, and the next $k$ words decide which rule.

The same placeholder can be followed by different words in different places of the grammar. A rule that produces nothing is right when the words after it fit the place where the placeholder stands. So each placeholder on the list carries a small table made for its place, and that table tells which rule to use for each possible group of $k$ words. The tables are built once, before any input is read.

## The problem

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area.

For a string $x \in \Sigma^*$, $\mathrm{FIRST}_k(x)$ is $x$ when $|x| \le k$ and its first $k$ tokens otherwise; for $\alpha \in (V \cup \Sigma)^*$, $\mathrm{FIRST}_k(\alpha)$ is the set of $\mathrm{FIRST}_k(x)$ over the terminal strings $x$ that $\alpha$ derives. A lookahead string shorter than $k$ means that the input ends there, so no end marker is needed. For sets of strings, $X \oplus_k Y = \{ \mathrm{FIRST}_k(xy) : x \in X, y \in Y \}$, and $\mathrm{FIRST}_k(\alpha \beta) = \mathrm{FIRST}_k(\alpha) \oplus_k \mathrm{FIRST}_k(\beta)$.

The input is a grammar $G$ in which every nonterminal derives some terminal string, a number $k \ge 1$, and tokens $w = a_1 \cdots a_n$. The output is a parse tree of $w$ with root $S$ when $w \in L(G)$, and otherwise an error at the first token where $w$ stops being a prefix of a sentence. As defined on the [LL(k) grammar](/ll-grammar/) page, $G$ is LL(k) when for any two leftmost derivations $S \Rightarrow_{lm}^* u A \alpha \Rightarrow_{lm} u \beta \alpha \Rightarrow_{lm}^* u x$ and $S \Rightarrow_{lm}^* u A \alpha \Rightarrow_{lm} u \gamma \alpha \Rightarrow_{lm}^* u y$ with $\mathrm{FIRST}_k(x) = \mathrm{FIRST}_k(y)$, the productions agree, $\beta = \gamma$. The choice may depend on the context $\alpha$, but only through the set $L = \mathrm{FIRST}_k(\alpha)$, and the tables below are indexed by it.

## The algorithm

For $A \in V$ and a set $L$ of strings of length at most $k$, the *LL(k) table* $T(A, L)$ maps a lookahead string $u$ to the production $A \to Y_1 \cdots Y_m$ with $u \in \mathrm{FIRST}_k(Y_1 \cdots Y_m) \oplus_k L$, together with the tables $T(Y_j, L_j)$, $L_j = \mathrm{FIRST}_k(Y_{j+1} \cdots Y_m) \oplus_k L$, for the nonterminals $Y_j$ of the right side. The parser starts with $T(S, \{\varepsilon\})$; each stack entry is a symbol, its table when it is a nonterminal, and the tree node that will receive its subtree.

```pseudo id=main
LLK-PARSE(G, k, T, w)                    ▷ T = the LL(k) tables, w = a1 ⋯ an
L1  i ← 1; push (S, T(S, {ε}))
L2  while the stack is not empty
L3      pop (X, t)
L4      if X is a terminal then
L5          if i > n or X ≠ ai then error at ai
L6          add the leaf ai to the tree; i ← i + 1
L7      else u ← ai ⋯ a_min(i+k−1, n)
L8          if t has no entry for u then error at a(i+d), where d is the length of the longest common prefix of u and a key of t
L9          let t[u] be (X → Y1 ⋯ Ym, t1, …, tm); add a new node X to the tree
L10         push (Ym, tm), …, (Y1, t1), so that Y1 is on top
L11 if i ≤ n then error at ai else accept and return the tree
```

The tables are built once, with a queue of the tables still to be filled. Only the tables reachable from $T(S, \{\varepsilon\})$ are made.

```pseudo id=build
LLK-TABLES(G, k)
L12 compute FIRST_k(A) for every A ∈ V, as a least fixed point
L13 create T(S, {ε}) and put it in the queue
L14 for each table T(A, L) taken from the queue
L15     for each production A → Y1 ⋯ Ym, with U ← FIRST_k(Y1 ⋯ Ym) ⊕k L
L16         if some u ∈ U already has another production in T(A, L) then report "not LL(k)"
L17         for each j with Yj ∈ V: Lj ← FIRST_k(Yj+1 ⋯ Ym) ⊕k L; create T(Yj, Lj) and queue it if it is new
L18         for each u ∈ U: T(A, L)[u] ← (A → Y1 ⋯ Ym, the tables of Y1, …, Ym)
```

At line L8, the error is placed at the first token of $u$ that no key of $t$ allows, not at $a_i$: the keys of $t$ are exactly the strings $\mathrm{FIRST}_k$ of what the stack can still derive, so $a_i \cdots a_{i+d-1}$ can still start a sentence and $a_{i+d}$ cannot. When $u$ is a proper prefix of a key, $i + d = n + 1$ and the input ends too early.

## Example

Take the grammar

$$0: S \to a A a a \qquad 1: S \to b A b a \qquad 2: A \to b \qquad 3: A \to \varepsilon$$

with $k = 2$. Its language is $\{ abaa, aaa, bbba, bba \}$. The tables:

| table | lookahead | production | tables for the right side |
|---|---|---|---|
| $T_0 = T(S, \{\varepsilon\})$ | $ab$, $aa$ | 0, $S \to a A a a$ | $T_1$ for $A$ |
| | $bb$ | 1, $S \to b A b a$ | $T_2$ for $A$ |
| $T_1 = T(A, \{aa\})$ | $ba$ | 2, $A \to b$ | |
| | $aa$ | 3, $A \to \varepsilon$ | |
| $T_2 = T(A, \{ba\})$ | $bb$ | 2, $A \to b$ | |
| | $ba$ | 3, $A \to \varepsilon$ | |

The lookahead $ba$ selects $A \to b$ in $T_1$ and $A \to \varepsilon$ in $T_2$. A single row for $A$, as in the [LL parse table](/ll-parse-table/) of a strong LL(k) parser, would put both productions at $ba$, because $\mathrm{FOLLOW}_2(A) = \{aa, ba\}$; the grammar is LL(2) but not strong LL(2). It is not LL(1) at all: in $T(A, \{b\})$ both productions of $A$ have the lookahead $b$.

The parser on $b \, b \, a$, with the top of the stack on the left:

| step | stack | rest of the input | lookahead | action |
|---|---|---|---|---|
| 1 | $S[T_0]$ | $b b a$ | $bb$ | expand by 1, $S \to b A b a$ |
| 2 | $b \ A[T_2] \ b \ a$ | $b b a$ | | match $b$ |
| 3 | $A[T_2] \ b \ a$ | $b a$ | $ba$ | expand by 3, $A \to \varepsilon$ |
| 4 | $b \ a$ | $b a$ | | match $b$ |
| 5 | $a$ | $a$ | | match $a$ |
| 6 | empty | empty | | accept |

On $b \, b \, b \, a$ step 3 sees $bb$ and expands $A \to b$. On $a \, b \, b \, a$ the parser expands $S \to a A a a$ on $ab$, matches $a$, and finds no entry for $bb$ in $T_1$; the longest common prefix with a key is $b$, of length 1, so the error is at the third token, the second $b$, and indeed $ab$ starts the sentence $abaa$ while $abb$ starts none.

## Correctness

Assume every nonterminal derives a terminal string. The proof below shows four things.

- **The tables.** LLK-TABLES reports a conflict if and only if $G$ is not LL(k).
- **Acceptance.** When there is no conflict, LLK-PARSE accepts exactly the sentences of $G$ and returns their parse trees.
- **Running time.** It stops after $O(n + 1)$ steps.
- **Errors.** It reports each error at the first token where the input stops being a prefix of a sentence.

The main invariant is that the table of each nonterminal on the stack is $T(X, L)$, with $L$ the set $\mathrm{FIRST}_k$ of the symbols below it. Two things follow. First, the keys of the table on top are exactly $\mathrm{FIRST}_k$ of the whole stack. Second, the parser follows the parse tree of any sentence, since the table entry is unique. Every table that BUILD makes comes from a left-sentential form $u A \alpha$ with $\mathrm{FIRST}_k(\alpha) = L$, which turns a conflict into a violation of the LL(k) condition, and conversely. As for termination, an LL(k) grammar has no left recursion, so the number of expansions is linear in the number of matched tokens. For the error position, a second invariant says that the tokens already inspected as lookahead remain a prefix of some key, so the parser makes the same moves on the input as on any sentence that agrees with it up to the reported token. The full proof is below.

## Complexity

- **Parsing.** The parse tree built on any input has $O(n + 1)$ inner nodes for a fixed grammar, so the parser does $O(n + 1)$ steps. Each expansion slices and hashes a lookahead of up to $k$ tokens, so the time is $O(k n)$ for a fixed grammar, or $O(n)$ with a rolling encoding of the window. The stack and the tree take $O(n)$ space.
- **Tables.** A table is indexed by $A$ and a set $L \subseteq \Sigma^{\le k}$, so there are at most $|V| \cdot 2^{s}$ tables with $s = \sum_{j = 0}^{k} |\Sigma|^j$, each with at most $s$ entries. The bound is exponential in $|\Sigma|^k$, but only the tables reachable from $T(S, \{\varepsilon\})$ are made: for the LL(1) expression grammar with $k = 2$ there are 15. The fixed point for $\mathrm{FIRST}_k$ costs time polynomial in $|G|$ and $s$.

## Properties

- **Deterministic, online, no backtracking.** Each token is matched once, and each decision looks at most $k$ tokens ahead.
- **Valid prefix property.** An error at $a_j$ means that $a_1 \cdots a_{j-1}$ starts a sentence and $a_1 \cdots a_j$ does not. With $k \ge 2$ the parser can see the bad token before it reaches it, and line L8 reports its position, not the position of the decision.
- **Left parse.** The expansions, in order, are the leftmost derivation, so semantic actions can run during the parse.
- **Exact class.** The tables have no conflict exactly for the LL(k) grammars. Each LL(k) grammar is unambiguous and has no left recursion.

## Variants and improvements

- **Strong LL(k).** Keep one table for each nonterminal and use $\mathrm{FOLLOW}_k(A)$ for every context. The tables are smaller, the driver is the [LL(1) parser](/ll1-parsing/) with longer lookahead, and it works for the strong LL(k) grammars, a proper subclass for $k \ge 2$, as the example shows. For $k = 1$ the two classes coincide.
- **Linear approximate lookahead.** The PCCTS and ANTLR parser generators replaced the sets of $k$-tuples by $k$ sets of single tokens, one for each lookahead position, which is smaller and often enough; this is the approach of Parr's thesis work on practical LL(k).
- **LL(*).** [LL(*) parsing](/ll-star-parsing/) uses a finite automaton for each decision and looks as far ahead as the decision needs, with backtracking as a last resort.
- **Recursive descent.** In a [recursive descent parser](/recursive-descent-parsing/), each procedure can pass its right context down as a parameter, which is the code form of the table $T(A, L)$.

## When to use it

Use LL(k) with $k \ge 2$ when a grammar is close to [LL(1)](/ll1-parsing/) and a few places need one or two more tokens, and [left factoring](/left-factoring/) would make the grammar harder to read. For larger $k$ the tables can grow fast, and an [LR parser](/lr-parsing/), which handles every LL(k) grammar with a $k$-token lookahead and many more, or an [LL(*)](/ll-star-parsing/) generator, is often the better choice.

## Pitfalls

- **Using FOLLOW sets for $k \ge 2$.** A single table row per nonterminal accepts only strong LL(k) grammars, and it reports conflicts that the context would resolve, as in the example.
- **The end of the input.** Lookahead strings shorter than $k$ must be part of the tables: they stand for the end of the input. Padding with end markers works too, but then every $\mathrm{FIRST}_k$ set must be padded the same way.
- **Error position.** Reporting the error at $a_i$ when the table lookup fails points at the wrong token whenever the bad token is further inside the lookahead window.
- **Unproductive symbols.** A nonterminal that derives no terminal string gives empty lookahead sets. Remove such symbols with [useless symbol elimination](/useless-symbol-elimination/) first, or the valid prefix property can fail.

## Implementations

## History

Lewis and Stearns (1968) introduced the LL(k) grammars through deterministic top-down translation. Rosenkrantz and Stearns (1970) proved their basic properties, among them that the LL(k) condition is decidable for each $k$, that strong LL(k) is a proper subclass, and that every LL(k) language has an LL(k+1) grammar without empty productions. Aho and Ullman (1972) gave the construction of the tables $T(A, L)$ and the parser that uses them. Since the tables can be large, practical tools stayed with LL(1) or used approximations, until Parr's work on linear approximate lookahead in the 1990s and on [LL(*)](/ll-star-parsing/) in 2011.

## References
