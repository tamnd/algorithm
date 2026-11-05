---
tag: 75P5FT
kind: definition
slug: ll-1-grammar
name: LL(1) grammar
aliases:
- LL(1)
area: automata-and-parsing/parser-generators
level: core
summary: A grammar whose predictive parse table has at most one entry per cell, decided with one token of lookahead.
prereqs: [first-and-follow-sets, leftmost-derivation]
see_also: [ll-grammar, ll-k-grammar, ll1-parsing, ll-parse-table, recursive-descent-parsing, left-factoring, left-recursion-elimination, lookahead-symbols]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.4.3, LL(1) Grammars (the three conditions on two productions A to alpha and A to beta, and the construction of the predictive parsing table)
  - paper: doi:10.1016/S0019-9958(70)90446-8
    title: D. J. Rosenkrantz and R. E. Stearns, Properties of deterministic top-down grammars, Information and Control 17(3) (1970)
    locator: pp. 226 to 256 (LL(k) and strong LL(k) grammars)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 8, Deterministic Top-Down Parsing (LL(1) grammars, LL(1) conflicts and how to remove them)
---

An LL(1) grammar is a [context-free grammar](/context-free-grammar/) in which one token of lookahead always tells a top-down parser which production to apply to the leftmost nonterminal. For a grammar without useless symbols this is the same as asking that the PREDICT sets of the alternatives of each nonterminal, built from [FIRST and FOLLOW sets](/first-and-follow-sets/), be pairwise disjoint, which is in turn the same as asking that the [LL parse table](/ll-parse-table/) have at most one production in each cell. The test takes $O(|G| \cdot |\Sigma|)$ time, and a grammar that passes is parsed in linear time by an [LL(1) parser](/ll1-parsing/) or by [recursive descent](/recursive-descent-parsing/).

## Definition

**Notation.** A grammar is $G = (V, \Sigma, P, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, start symbol $S$, input length $n$ and size $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$. Lowercase $w$ is a terminal string, Greek letters are strings over $V \cup \Sigma$, and $\$$ is the end marker. For a string $\alpha$, $\mathrm{FIRST}_1(\alpha\$)$ is the set of first terminals of the strings $x\$$ with $\alpha \Rightarrow^* x$; it contains $\$$ exactly when $\alpha$ is nullable.

**The definition.** $G$ is *LL(1)* if, for every left-sentential form $S \Rightarrow_{lm}^* w A \alpha$ and every two different productions $A \to \beta$ and $A \to \gamma$,
$$\mathrm{FIRST}_1(\beta \alpha \$) \cap \mathrm{FIRST}_1(\gamma \alpha \$) = \emptyset .$$
This is the case $k = 1$ of the [LL(k) grammar](/ll-grammar/) definition: when $w$ has been matched and $A$ is the leftmost nonterminal, the next token, or the end of the input, fixes the production of $A$.

**PREDICT sets.** For a production $A \to \beta$ let
$$\mathrm{PREDICT}(A \to \beta) = \begin{cases} \mathrm{FIRST}(\beta) \cup \mathrm{FOLLOW}(A) & \text{if } \beta \Rightarrow^* \varepsilon, \\ \mathrm{FIRST}(\beta) & \text{otherwise.} \end{cases}$$
The LL(1) table puts $A \to \beta$ into the cell $M[A, a]$ for each $a \in \mathrm{PREDICT}(A \to \beta)$. Spelled out for two alternatives $A \to \beta \mid \gamma$, disjointness of their PREDICT sets is the three conditions of the Dragon book: $\mathrm{FIRST}(\beta) \cap \mathrm{FIRST}(\gamma) = \emptyset$; at most one of $\beta$ and $\gamma$ is nullable; and if $\gamma$ is nullable then $\mathrm{FIRST}(\beta) \cap \mathrm{FOLLOW}(A) = \emptyset$.

**Theorem.** Suppose every nonterminal of $G$ is reachable from $S$ and derives some terminal string. Then $G$ is LL(1) if and only if, for each nonterminal $A$, the PREDICT sets of its productions are pairwise disjoint.

*Proof.* First, the inclusion $\mathrm{FIRST}_1(\beta\alpha\$) \subseteq \mathrm{PREDICT}(A \to \beta)$ holds for every left-sentential form $w A \alpha$. A token of $\mathrm{FIRST}_1(\beta\alpha\$)$ either comes from $\beta$, and then it is in $\mathrm{FIRST}(\beta)$, or $\beta$ is nullable and it is the first token of a string derived from $\alpha\$$; in the second case $S\$ \Rightarrow^* w A \alpha \$$ shows that it is in $\mathrm{FOLLOW}(A)$. So disjoint PREDICT sets make the two sets of the definition disjoint, and $G$ is LL(1). This direction needs no assumption on $G$.

Conversely, let $a \in \mathrm{PREDICT}(A \to \beta) \cap \mathrm{PREDICT}(A \to \gamma)$. We build a left-sentential form $w A \alpha$ with $a$ in both $\mathrm{FIRST}_1$ sets. If $a \in \mathrm{FOLLOW}(A)$, there is a sentential form $\delta A \eta$ of $S\$$ with $\eta \Rightarrow^* a \cdots$. Take a derivation tree for it, and expand every nonterminal of $\delta$ to a terminal string, which is possible because each nonterminal derives one. Follow this tree by a leftmost derivation; at the moment $A$ becomes the leftmost nonterminal the form is $w A \alpha$, where $\alpha$ is the row of unexpanded right siblings of $A$ and of its ancestors, and the rest of the tree shows $\alpha\$ \Rightarrow^* a \cdots$. If $a \notin \mathrm{FOLLOW}(A)$, take any left-sentential form $w A \alpha$; one exists because $A$ is reachable and every nonterminal derives a terminal string. Now check the two productions. If $a$ lies in $\mathrm{PREDICT}(A \to \beta)$ through $\mathrm{FIRST}(\beta)$, then $\beta \Rightarrow^* a \cdots$ gives $a \in \mathrm{FIRST}_1(\beta\alpha\$)$. Otherwise $\beta$ is nullable and $a \in \mathrm{FOLLOW}(A)$, so we are in the first case and $\beta\alpha\$ \Rightarrow^* \alpha\$ \Rightarrow^* a \cdots$. The same holds for $\gamma$, so the definition fails at $w A \alpha$. ∎

**Deciding the property.** Compute the nullable set, FIRST and FOLLOW in $O(|G| \cdot |\Sigma|)$ time, then fill the table and look for a cell with two entries. The table has $|V| \cdot (|\Sigma| + 1)$ cells and filling it costs one step per element of a PREDICT set, so the whole test takes $O(|G| \cdot |\Sigma|)$ time. The test is the table construction itself, which is why an LL(1) parser generator reports "conflicts" in the cells where it fails.

## Examples and non-examples

**A statement list.** $L \to S\,L'$, $L' \to {;}\,S\,L' \mid \varepsilon$, $S \to \mathit{id} \mid \mathtt{begin}\ L\ \mathtt{end}$.

| production | PREDICT |
|---|---|
| $L \to S\,L'$ | $\mathit{id}$, $\mathtt{begin}$ |
| $L' \to {;}\,S\,L'$ | $;$ |
| $L' \to \varepsilon$ | $\mathtt{end}$, $\$$ |
| $S \to \mathit{id}$ | $\mathit{id}$ |
| $S \to \mathtt{begin}\ L\ \mathtt{end}$ | $\mathtt{begin}$ |

The sets of $L'$ and of $S$ are disjoint, so the grammar is LL(1). The production $L' \to \varepsilon$ is chosen on $\mathtt{end}$ and on $\$$, the two tokens of $\mathrm{FOLLOW}(L')$: the list ends when the parser sees what follows a list. The expression grammar $E \to T E'$, $E' \to + T E' \mid \varepsilon$, $T \to F T'$, $T' \to * F T' \mid \varepsilon$, $F \to (\,E\,) \mid \mathit{id}$ is LL(1) in the same way; its table is on the [LL parse table](/ll-parse-table/) page.

**A FIRST and FOLLOW conflict.** $S \to A\,a$, $A \to a \mid \varepsilon$ generates $\{a, aa\}$. Here $\mathrm{PREDICT}(A \to a) = \{a\}$ and, since $\mathrm{FOLLOW}(A) = \{a\}$, $\mathrm{PREDICT}(A \to \varepsilon) = \{a\}$, so the cell $M[A, a]$ holds both. With the input $a$ the parser cannot know whether that $a$ belongs to $A$. The grammar is LL(2), and $S \to a\,T$, $T \to a \mid \varepsilon$ generates the same language and is LL(1), with $\mathrm{PREDICT}(T \to \varepsilon) = \{\$\}$.

**The dangling else.** $S \to i\,E\,t\,S\,S' \mid a$, $S' \to e\,S \mid \varepsilon$, $E \to b$, where $i$, $t$ and $e$ stand for `if`, `then` and `else`. $\mathrm{FOLLOW}(S') = \mathrm{FOLLOW}(S) = \{e, \$\}$, so $M[S', e]$ holds both $S' \to e\,S$ and $S' \to \varepsilon$, and the grammar is not LL(1). It is ambiguous, so it is not LL(k) for any $k$. A parser generator that keeps $S' \to e\,S$ in that cell attaches each `else` to the nearest `then`, which is the rule of most languages.

**Left recursion.** In $E \to E + T \mid T$ every token of $\mathrm{FIRST}(T)$ is also in $\mathrm{FIRST}(E + T)$, so if $T$ derives anything, the two PREDICT sets meet. A reduced grammar with a left-recursive nonterminal is never LL(1); [left recursion elimination](/left-recursion-elimination/) turns this grammar into the $E'$ form above.

**Two nullable alternatives.** If $A \to \beta \mid \gamma$ with both nullable, both PREDICT sets contain $\mathrm{FOLLOW}(A)$, which is not empty when $A$ is reachable, so the grammar is not LL(1); the empty string has two derivations from $A$, and the grammar is ambiguous.

**Why the theorem needs reduced grammars.** $S \to a$, $B \to b\,c \mid b$ has a conflict in the cell $M[B, b]$, yet it is LL(1) by the definition, because no left-sentential form contains $B$. Table-driven tools report such conflicts anyway, so remove [useless symbols](/useless-symbol-elimination/) before the test.

## Related definitions

- **Strong LL(1).** The [LL(k)](/ll-grammar/) definition has a strong form that uses $\mathrm{FOLLOW}_k(A)$ in place of each context; the PREDICT test is the strong LL(1) test, so the theorem says that LL(1) and strong LL(1) coincide for reduced grammars. For $k \ge 2$ they differ; see [LL(k) grammar](/ll-k-grammar/).
- **LL(k) and LR(k).** Every LL(1) grammar is LL(k) for $k \ge 1$ and, when reduced, [LR(1)](/lr-k-grammar/); every LL(1) grammar is unambiguous.
- **Predictive parsing.** The [LL(1) parser](/ll1-parsing/) runs the table with a stack; [recursive descent](/recursive-descent-parsing/) encodes each row as a procedure that switches on the lookahead token.
- **Grammar transformations.** [Left factoring](/left-factoring/) and [left recursion elimination](/left-recursion-elimination/) remove the most common conflicts; they preserve the language but change the parse trees.
- **Lookahead.** [Lookahead symbols](/lookahead-symbols/) compares how LL and LR methods use the next token.

## References
