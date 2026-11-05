---
tag: HFG3GJ
kind: definition
slug: ll-k-grammar
name: LL(k) grammar
aliases:
- LL(k)
area: automata-and-parsing/parser-generators
level: advanced
summary: A grammar that can be parsed top-down deterministically with k tokens of lookahead.
prereqs: [ll-1-grammar, first-and-follow-sets]
see_also: [ll-grammar, ll-k-parsing, lr-k-grammar, lookahead-symbols, ll-star-parsing, left-factoring, parser-table-construction, ll-parse-table]
sources:
  - paper: doi:10.1016/S0019-9958(70)90446-8
    title: D. J. Rosenkrantz and R. E. Stearns, Properties of deterministic top-down grammars, Information and Control 17(3) (1970)
    locator: pp. 226 to 256 (the LL(k) condition, strong LL(k) grammars, and the decision procedure for a fixed k)
  - paper: doi:10.1145/321466.321477
    title: P. M. Lewis II and R. E. Stearns, Syntax-directed transduction, Journal of the ACM 15(3) (1968)
    locator: pp. 465 to 488 (the definition of LL(k) grammars)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 8, Deterministic Top-Down Parsing (the sections on LL(k) and strong LL(k) grammars)
---

## Definition

An LL(k) grammar is a [context-free grammar](/context-free-grammar/) in which a top-down parser, having matched a prefix of the input and facing a nonterminal, can always choose the production from the next $k$ tokens. This page states the class from the side of a parser generator: it gives the finite test that decides whether a grammar is LL(k) for a given $k$, the stronger test that a one-row-per-nonterminal table needs, and a construction that turns the first into the second. The derivation form of the definition and the basic properties are on the [LL(k) grammar](/ll-grammar/) page of the context-free parsing area; the case $k = 1$ is on the [LL(1) grammar](/ll-1-grammar/) page.

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, the empty string $\varepsilon$, start symbol $S$, input length $n$ and size $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$. Lowercase $w, x, y$ are terminal strings and Greek letters are strings over $V \cup \Sigma$. All grammars are assumed reduced: every nonterminal is reachable from $S$ and derives some terminal string.

**Lookahead sets.** For a terminal string $x$, $\mathrm{FIRST}_k(x)$ is the prefix of length $k$ of $x$, or $x$ itself if it is shorter; a short string means that the input ends there. For a string $\alpha$ of grammar symbols, $\mathrm{FIRST}_k(\alpha)$ is the set of $\mathrm{FIRST}_k(x)$ over all terminal strings $x$ with $\alpha \Rightarrow^* x$. For a set $L$ of strings, $\mathrm{FIRST}_k(\alpha L)$ is the union of $\mathrm{FIRST}_k(\alpha u)$ over $u \in L$, where $\alpha u$ is read with $u$ as fixed terminals. $\mathrm{FOLLOW}_k(A)$ is the union of $\mathrm{FIRST}_k(\alpha)$ over all sentential forms $S \Rightarrow^* \beta A \alpha$. The [FIRST and FOLLOW sets](/first-and-follow-sets/) page computes these sets for $k = 1$; for larger $k$ the same fixed-point rules work with concatenation truncated to length $k$.

**LL(k).** $G$ is *LL(k)* if for every left-sentential form $w A \alpha$ with $S \Rightarrow_{lm}^* w A \alpha$, and every two different productions $A \to \beta$ and $A \to \gamma$,
$$\mathrm{FIRST}_k(\beta \alpha) \cap \mathrm{FIRST}_k(\gamma \alpha) = \emptyset .$$
This is equivalent to the derivation condition of Lewis and Stearns (1968) stated on the [LL(k) grammar](/ll-grammar/) page.

**Local follow sets and the finite test.** The condition depends on $\alpha$ only through the set $L = \mathrm{FIRST}_k(\alpha)$, the *local follow set* of that occurrence of $A$. The pairs $(A, L)$ that occur are found by a closure that never builds a sentential form:

- $(S, \{\varepsilon\})$ occurs;
- if $(A, L)$ occurs and $A \to X_1 \cdots X_m$ is a production with $X_i$ a nonterminal, then $(X_i, \mathrm{FIRST}_k(X_{i+1} \cdots X_m L))$ occurs.

There are finitely many such pairs, at most $|V| \cdot 2^{(|\Sigma| + 1)^k}$, so for a fixed $k$ being LL(k) is decidable (Rosenkrantz and Stearns 1970): $G$ is LL(k) if and only if, for every pair $(A, L)$ that occurs and every two different productions $A \to \beta$ and $A \to \gamma$, the sets $\mathrm{FIRST}_k(\beta L)$ and $\mathrm{FIRST}_k(\gamma L)$ are disjoint. An [LL(k) parser](/ll-k-parsing/) uses one table row for each pair.

**Strong LL(k).** $G$ is *strong LL(k)* if for every nonterminal $A$ and every two different productions $A \to \beta$ and $A \to \gamma$,
$$\mathrm{FIRST}_k(\beta \, \mathrm{FOLLOW}_k(A)) \cap \mathrm{FIRST}_k(\gamma \, \mathrm{FOLLOW}_k(A)) = \emptyset .$$
$\mathrm{FOLLOW}_k(A)$ is the union of all local follow sets of $A$, so the strong test is the finite test with every row of $A$ merged into one, and a strong LL(k) grammar is LL(k). The strong test needs a table with one row per nonterminal and one column per string of at most $k$ tokens. For $k = 1$ the two tests agree on reduced grammars; for $k \ge 2$ they differ.

**From LL(k) to strong LL(k).** Replace each nonterminal by the pairs $(A, L)$ that occur, and each production $A \to X_1 \cdots X_m$ by the productions
$$(A, L) \to Y_1 \cdots Y_m, \qquad Y_i = (X_i, \mathrm{FIRST}_k(X_{i+1} \cdots X_m L)) \text{ if } X_i \in V, \quad Y_i = X_i \text{ otherwise},$$
with start symbol $(S, \{\varepsilon\})$. The new grammar $G_k$ generates $L(G)$, since each $(A, L)$ derives exactly the strings that $A$ derives. In every left-sentential form of $G_k$, the part to the right of an occurrence of $(A, L)$ has $\mathrm{FIRST}_k$ equal to $L$, by induction on the derivation; so $\mathrm{FOLLOW}_k((A, L)) = L$, and the strong test for $G_k$ is the finite test for $G$, row by row. Hence $G$ is LL(k) if and only if $G_k$ is strong LL(k), and the LL(k) languages are exactly the strong LL(k) languages. The price is the number of nonterminals, which is the number of pairs.

**Cost.** The sets $\mathrm{FIRST}_k$ and $\mathrm{FOLLOW}_k$ can contain up to $(|\Sigma| + 1)^k$ strings, so both tests take time exponential in $k$ in the worst case, and the finite test can in principle meet many local follow sets per nonterminal. Generators therefore use $k = 1$, a small fixed $k$, or lookahead computed only where a decision needs it, as in [LL(*) parsing](/ll-star-parsing/).

## Examples and non-examples

Every claim below was checked by a script that runs the finite test and the strong test, and compares the finite test with a direct search for conflicting left-sentential forms on random grammars.

**LL(2), not strong LL(2), not LL(1).** Take $S \to a\,A\,c \mid b\,A$ and $A \to c \mid \varepsilon$, whose language is $\{ac, acc, b, bc\}$. The occurring pairs are $(S, \{\varepsilon\})$, $(A, \{c\})$ from $S \to a\,A\,c$ and $(A, \{\varepsilon\})$ from $S \to b\,A$.

| pair | $\mathrm{FIRST}_2$ with $A \to c$ | $\mathrm{FIRST}_2$ with $A \to \varepsilon$ |
|---|---|---|
| $(A, \{c\})$ | $cc$ | $c$ |
| $(A, \{\varepsilon\})$ | $c$ | $\varepsilon$ |
| strong test, $\mathrm{FOLLOW}_2(A) = \{c, \varepsilon\}$ | $cc, c$ | $c, \varepsilon$ |

Each real row is disjoint, so the grammar is LL(2); the strong row has $c$ on both sides. With one token the row $(A, \{c\})$ has $c$ on both sides, so the grammar is not LL(1). The construction above gives $S \to a\,A_1\,c \mid b\,A_2$, $A_1 \to c \mid \varepsilon$, $A_2 \to c \mid \varepsilon$, with $A_1 = (A, \{c\})$ and $A_2 = (A, \{\varepsilon\})$; it generates the same language and is strong LL(2), since now $\mathrm{FOLLOW}_2(A_1) = \{c\}$ and $\mathrm{FOLLOW}_2(A_2) = \{\varepsilon\}$.

**One more token per step.** $S \to A\,b^m c \mid B\,b^m d$ with $A \to \varepsilon$ and $B \to \varepsilon$ is strong LL(m+1) and not LL(m): at the start the two productions of $S$ predict $b^m c$ and $b^m d$, which first differ in token $m + 1$. This was checked for $m = 1, 2, 3$. The grammar for $m = 1$ is LR(2) but not LR(1): an LR parser must reduce $A \to \varepsilon$ or $B \to \varepsilon$ before it has read anything, so it needs the same two tokens. This agrees with the fact that every LL(k) grammar is [LR(k)](/lr-k-grammar/).

**Not LL(k) for any k, although LR(1).** $S \to A\,a \mid B\,b$, $A \to a\,A \mid c$, $B \to a\,B \mid c$ generates $a^* c\,(a \mid b)$. The first production must be chosen at the start, and on the inputs $a^m c\,a$ and $a^m c\,b$ with $m \ge k$ the first $k$ tokens are $a^k$ in both cases, so the grammar is LL(k) for no $k$; the test finds a conflict in the row of $S$ for each $k \le 5$. An LR parser reads the whole $a^m c$ first and then reduces $c$ to $A$ or $B$ on the next token, so the grammar is LR(1) and not LR(0). The language itself is LL(1): $S \to a\,S \mid c\,T$, $T \to a \mid b$.

**Left recursion and ambiguity.** A left-recursive reduced grammar is LL(k) for no $k$, and neither is an ambiguous one; see the [LL(k) grammar](/ll-grammar/) page for both arguments, and [left factoring](/left-factoring/) for the rewrite that often turns an LL(k) grammar into an LL(1) one.

## Related definitions

- [LL(1) grammar](/ll-1-grammar/): the case $k = 1$, tested by the PREDICT sets, where strong and full LL(1) coincide.
- [LL(k) grammar](/ll-grammar/): the derivation form of the definition, the hierarchy in $k$, and the properties of LL(k) languages.
- [LL(k) parsing](/ll-k-parsing/) and [LL parse table](/ll-parse-table/): the parser and the table that the finite test builds.
- [LR(k) grammar](/lr-k-grammar/): the bottom-up class, which contains every LL(k) grammar and also grammars such as $S \to A\,a \mid B\,b$ above.
- [Lookahead symbols](/lookahead-symbols/): what the $k$ tokens mean for top-down and bottom-up parsers alike.
- [LL(*) parsing](/ll-star-parsing/): lookahead of unbounded length, decided by a finite automaton for each decision.

## References
