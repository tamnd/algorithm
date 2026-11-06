---
tag: 895AV2
kind: definition
slug: ll-grammar
name: LL(k) grammar
aliases:
- LL(1) grammar
area: automata-and-parsing/context-free-parsing
level: core
summary: A grammar parsable deterministically top-down with k symbols of lookahead.
prereqs: [context-free-grammar, leftmost-derivation, first-and-follow-sets]
see_also: [ll-parse-table, ll1-parsing, ll-k-parsing, lr-grammar, left-recursion, left-factoring, ambiguity, lookahead-parsing]
sources:
  - paper: doi:10.1145/321466.321477
    title: P. M. Lewis II and R. E. Stearns, Syntax-directed transduction, Journal of the ACM 15(3) (1968)
    locator: pp. 465 to 488 (the definition of LL(k) grammars)
  - paper: doi:10.1016/S0019-9958(70)90446-8
    title: D. J. Rosenkrantz and R. E. Stearns, Properties of deterministic top-down grammars, Information and Control 17(3) (1970)
    locator: pp. 226 to 256 (the LL(k) condition, strong LL(k) grammars, removal of empty productions, decidability of equivalence)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.4.3, LL(1) Grammars
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 8, Deterministic Top-Down Parsing (Section 8.2 on LL(1) grammars, and the sections on LL(k) and strong LL(k) grammars)
---

An LL(k) grammar is a [context-free grammar](/context-free-grammar/) in which the next $k$ input tokens always determine which production a top-down parser must apply. The name says that such a parser reads the input from the Left, builds a [Leftmost derivation](/leftmost-derivation/), and looks $k$ tokens ahead. An LL(1) grammar is exactly a grammar whose [LL parse table](/ll-parse-table/) has no conflict, so the [LL(1) parser](/ll1-parsing/) handles it in linear time without backtracking.

## Definition

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. Lowercase letters $w, x, y$ are strings of terminals, and Greek letters are strings over $V \cup \Sigma$.

For a terminal string $x$, $\mathrm{FIRST}_k(x)$ is the prefix of length $k$ of $x$, or $x$ itself when $|x| < k$. For a string $\alpha$ of grammar symbols, $\mathrm{FIRST}_k(\alpha) = \{ \mathrm{FIRST}_k(x) : \alpha \Rightarrow^* x \}$, and $\mathrm{FOLLOW}_k(A)$ is the set of $\mathrm{FIRST}_k(x)$ over all sentential forms $S \Rightarrow^* \beta A x'$ with $x' \Rightarrow^* x$. A string shorter than $k$ in these sets means that the input ends there.

**LL(k) grammar.** Let $k \ge 0$. The grammar $G$ is *LL(k)* if for any two leftmost derivations

$$S \Rightarrow_{lm}^* w A \alpha \Rightarrow_{lm} w \beta \alpha \Rightarrow^* w x \quad \text{and} \quad S \Rightarrow_{lm}^* w A \alpha \Rightarrow_{lm} w \gamma \alpha \Rightarrow^* w y$$

with $\mathrm{FIRST}_k(x) = \mathrm{FIRST}_k(y)$, the productions agree: $\beta = \gamma$. A language is *LL(k)* if some LL(k) grammar generates it. In words: once a parser has matched $w$ and has $A$ as the leftmost nonterminal, the next $k$ tokens fix the production of $A$, whatever the rest of the input is.

An equivalent form of the condition: for each left-sentential form $w A \alpha$ and each two different productions $A \to \beta$ and $A \to \gamma$,

$$\mathrm{FIRST}_k(\beta \alpha) \cap \mathrm{FIRST}_k(\gamma \alpha) = \emptyset.$$

The test depends on the context $\alpha$, and a grammar can have infinitely many left-sentential forms. Rosenkrantz and Stearns (1970) showed that only finitely many sets $\mathrm{FIRST}_k(\alpha)$ occur, so the condition is decidable for each fixed $k$; the [LL(k) parsing](/ll-k-parsing/) page builds one table for each of them.

**Strong LL(k).** The grammar is *strong LL(k)* if for each two different productions $A \to \beta$ and $A \to \gamma$,

$$\mathrm{FIRST}_k(\beta \, \mathrm{FOLLOW}_k(A)) \cap \mathrm{FIRST}_k(\gamma \, \mathrm{FOLLOW}_k(A)) = \emptyset,$$

where $\mathrm{FIRST}_k$ of a set of strings is taken string by string and truncated to length $k$. This replaces each context $\alpha$ by all of them at once, so a strong LL(k) grammar is LL(k), and a table with one row for each nonterminal and one column for each lookahead string suffices.

**The case $k = 1$.** Let every nonterminal of $G$ be reachable from $S$ and derive some terminal string. Then $G$ is LL(1) if and only if it is strong LL(1), if and only if the [LL parse table](/ll-parse-table/) has no cell with two productions; that is, the sets $\mathrm{PREDICT}(A \to \beta)$, equal to $\mathrm{FIRST}(\beta)$ together with $\mathrm{FOLLOW}(A)$ when $\beta$ is [nullable](/nullable-symbol/), are pairwise disjoint for the productions of each $A$. For the nontrivial direction, suppose the token $a$ is in two PREDICT sets of $A$. Since $A$ is reachable and every symbol derives a terminal string, there is a left-sentential form $w A \alpha$; when $a$ comes from $\mathrm{FOLLOW}(A)$, this form can be chosen with $a \in \mathrm{FIRST}_1(\alpha)$, by deriving the part before $A$ to terminals. Then $a$ lies in both $\mathrm{FIRST}_1(\beta \alpha)$ and $\mathrm{FIRST}_1(\gamma \alpha)$, and the grammar is not LL(1). For $k \ge 2$, strong LL(k) is a proper subclass, as an example below shows.

**Properties.** These hold for every $k$:

- An LL(k) grammar is unambiguous: two different leftmost derivations of one sentence first differ at a step where they expand the same $A$ in the same left-sentential form, with the same remaining input.
- An LL(k) grammar whose symbols are all reachable and productive is not left-recursive. The grammar classes grow with $k$: LL(k) grammars are LL(k+1), and $S \to a^k b \mid a^k c$ is LL(k+1) but not LL(k).
- Every LL(k) grammar is an [LR(k) grammar](/lr-grammar/), so every LL(k) language is a [deterministic context-free language](/deterministic-context-free-language/). The converse fails, for grammars and for languages.
- Rosenkrantz and Stearns (1970) showed that empty productions can be removed from an LL(k) grammar at the cost of one more token of lookahead, and that it is decidable whether two LL(k) grammars generate the same language, while for general context-free grammars [equivalence is undecidable](/cfg-equivalence-undecidable/).

## Examples and non-examples

**The expression grammar.** $E \to T E'$, $E' \to + T E' \mid \varepsilon$, $T \to F T'$, $T' \to * F T' \mid \varepsilon$, $F \to ( E ) \mid id$ is LL(1). Its PREDICT sets are $\{+\}$ and $\{), \$\}$ for $E'$, $\{*\}$ and $\{+, ), \$\}$ for $T'$, and $\{(\}$ and $\{id\}$ for $F$; each pair is disjoint. Its table is on the [LL parse table](/ll-parse-table/) page.

**LL(2) but not LL(1).** $S \to a S \mid a$ needs two tokens: with the input $a a$, the first $a$ does not tell whether more follows. $\mathrm{FIRST}_2(a S) = \{aa\}$ and $\mathrm{FIRST}_2(a) = \{a\}$ are disjoint, so the grammar is LL(2). [Left factoring](/left-factoring/) gives $S \to a S'$, $S' \to S \mid \varepsilon$, which is LL(1), since $\mathrm{PREDICT}(S' \to S) = \{a\}$ and $\mathrm{PREDICT}(S' \to \varepsilon) = \{\$\}$. In the same way $S \to a a b \mid a a c$ is LL(3) and not LL(2).

**LL(2) but not strong LL(2).** Take $S \to a A a a \mid b A b a$ and $A \to b \mid \varepsilon$. The left-sentential forms with $A$ are $a A a a$ and $b A b a$.

| context | $\mathrm{FIRST}_2$ with $A \to b$ | $\mathrm{FIRST}_2$ with $A \to \varepsilon$ |
|---|---|---|
| after $a$, before $a a$ | $b a$ | $a a$ |
| after $b$, before $b a$ | $b b$ | $b a$ |
| strong test, $\mathrm{FOLLOW}_2(A) = \{aa, ba\}$ | $ba, bb$ | $aa, ba$ |

In each real context the two sets are disjoint, so the grammar is LL(2). The strong test merges the two contexts and finds $ba$ on both sides, so the grammar is not strong LL(2). It is not LL(1): in the second context, $\mathrm{FIRST}_1$ is $b$ for both productions.

**Non-examples.**

- **Left recursion.** $E \to E + T \mid T$, $T \to a$ is not LL(k) for any $k$. Take the left-sentential form $E \alpha$ with $\alpha = (+T)^j$ and $2j + 1 \ge k$, reached with $w = \varepsilon$. Expanding by $E \to T$ leads to $x = a (+a)^j$, and expanding by $E \to E + T$ leads to $y = a (+a)^{j+1}$. The first $k$ tokens of $x$ and $y$ agree, but the productions differ. [Left recursion elimination](/left-recursion-elimination/) gives the LL(1) grammar above.
- **Ambiguity.** An [ambiguous](/ambiguity/) grammar is not LL(k) for any $k$. The dangling else, $S \to i \, S \mid i \, S \, e \, S \mid x$, is an example; so is $E \to E + E \mid a$.
- **A language with no LL(k) grammar.** $\{ a^m b^m : m \ge 1 \} \cup \{ a^m c^m : m \ge 1 \}$ is a deterministic context-free language, and it has an LR(0) grammar, but no LL(k) grammar for any $k$. A top-down parser would have to commit to the $b$ branch or the $c$ branch while it still reads $a$'s, and the decisive token can be arbitrarily far away.

## Related definitions

- [LL(1) grammar](/ll-1-grammar/) and [LL(k) grammar](/ll-k-grammar/): the pages on these classes in the area of parser generators, with the table tests they use.
- [LR(k) grammar](/lr-grammar/): the bottom-up counterpart, which decides each production after seeing all of its yield and $k$ more tokens; it contains every LL(k) grammar.
- [LL parse table](/ll-parse-table/), [LL(1) parsing](/ll1-parsing/) and [LL(k) parsing](/ll-k-parsing/): the tables and drivers for these grammars.
- [Lookahead](/lookahead-parsing/): the tokens beyond the current position that a parser examines.
- [Left recursion](/left-recursion/) and [left factoring](/left-factoring/): the two common reasons a natural grammar is not LL(k), and the rewrites that often fix them.
- [Recursive descent parsing](/recursive-descent-parsing/): the hand-written form of an LL(k) parser.

## References
