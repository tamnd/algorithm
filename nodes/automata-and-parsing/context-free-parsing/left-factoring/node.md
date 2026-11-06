---
tag: Q6MHSM
kind: technique
slug: left-factoring
name: Left factoring
aliases:
- grammar left factoring
area: automata-and-parsing/context-free-parsing
level: core
summary: Grammar transformation that factors out common prefixes of alternatives to enable LL parsing.
prereqs: [context-free-grammar, top-down-parsing, first-and-follow-sets]
see_also: [ll1-parsing, ll-grammar, recursive-descent-parsing, left-recursion-elimination, ll-k-parsing, ambiguity, parsing-expression-grammar, lalr-grammar]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.3.4, Left Factoring (Algorithm 4.21 and the dangling-else example)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 8.2.5, Solving LL(1) Conflicts (left-factoring and substitution)
  - book: isbn:9780120884780
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, second edition, Morgan Kaufmann, 2011
    locator: Section 3.3.1, Transforming a Grammar for Top-Down Parsing (left-factoring to eliminate backtracking)
---

Left factoring rewrites the productions $A \to \alpha \beta_1 \mid \alpha \beta_2$, whose right sides start with the same nonempty string $\alpha$, as $A \to \alpha A'$ and $A' \to \beta_1 \mid \beta_2$, with a new nonterminal $A'$. The language does not change. A top-down parser that must choose an alternative of $A$ after seeing one input symbol can then postpone the choice until it has read $\alpha$. It is, with [left recursion elimination](/left-recursion-elimination/), the standard way to prepare a grammar for [LL(1) parsing](/ll1-parsing/) and [recursive descent](/recursive-descent-parsing/).

## In plain words

A top-down parser decides which rule to use before it reads the words that the rule covers. If two rules for the same name begin with the same words, the next word cannot tell them apart. Left factoring moves the shared beginning into one rule and puts the different endings into a new name. The parser reads the shared words first and chooses between the endings only when they begin to differ. The set of sentences stays the same; only the shape of the parse trees changes.

## When it applies

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol. Left factoring applies when a nonterminal $A$ has two or more alternatives whose right sides begin with the same grammar symbol. Such alternatives always have overlapping FIRST sets, which is a FIRST/FIRST conflict of the [LL(1)](/ll-grammar/) test (if the common symbol derives at least one nonempty terminal string). Left factoring removes every such conflict that is visible in the symbols of the right sides.

It does not apply, by itself, when the conflict is hidden:

- two alternatives begin with different nonterminals that derive strings with the same first terminal, as in $A \to B c \mid a d$ with $B \to a b$;
- an alternative begins with a nullable nonterminal, so its FIRST set includes symbols that come after it;
- the conflict is between FIRST of one alternative and FOLLOW of $A$, which comes from an $\varepsilon$ alternative.

For the first two cases, one can substitute the right sides of the leading nonterminal into $A$ first and then factor. Left factoring is not needed for bottom-up parsing: an LR parser keeps both alternatives alive in one state of the [LR(0) automaton](/lr0-parsing/) until they differ.

## The template

The procedure repeats one step. For a nonterminal $A$, let $\alpha$ be the longest nonempty string that is a prefix of the right sides of at least two alternatives of $A$. Group all alternatives that start with $\alpha$ and replace them by one alternative that ends in a fresh nonterminal.

```pseudo id=main
LEFT-FACTOR(G)
L1  repeat
L2      for each nonterminal A of G do
L3          α ← the longest nonempty string that is a prefix of two or more alternatives of A
L4          if α exists then
L5              let A → α β1 | … | α βk be all alternatives of A that start with α, and A → γ1 | … | γm the others
L6              A′ ← a fresh nonterminal
L7              replace the productions of A by A → α A′ | γ1 | … | γm, and add A′ → β1 | … | βk
L8  until no nonterminal has two alternatives that start with the same symbol
L9  return G
```

Some $\beta_i$ can be $\varepsilon$, when an alternative is $\alpha$ itself; then $A' \to \varepsilon$ is one of the new productions.

**The language does not change.** Every derivation step $A \Rightarrow \alpha \beta_i$ in the old grammar becomes the two steps $A \Rightarrow \alpha A' \Rightarrow \alpha \beta_i$ in the new one, and every use of $A'$ in the new grammar comes after a use of $A \to \alpha A'$, so the two steps can be joined again. This gives a one-to-one map between the parse trees of a string in the two grammars: the new trees have an extra node $A'$ under each node that used a factored alternative. So an unambiguous grammar stays unambiguous, and an ambiguous grammar stays ambiguous.

**The loop ends.** Call an alternative of a nonterminal *clashing* if another alternative of the same nonterminal starts with the same symbol. In one step, let $x$ be the first symbol of $\alpha$. The $k \ge 2$ grouped alternatives were clashing. Afterwards, $A \to \alpha A'$ clashes only if some $\gamma_j$ starts with $x$, and such $\gamma_j$ clashed before too. No two $\beta_i$ start with the same symbol, because otherwise a prefix of two alternatives would be longer than $\alpha$; so no alternative of $A'$ clashes. Other nonterminals do not change. So each step lowers the number of clashing alternatives by at least $k - 1 \ge 1$, and the number of steps is less than the number of productions of $G$. With the grammar size $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$, one step changes $|G|$ by $2 - (k - 1)|\alpha| \le 1$, so the result has size less than $|G| + |P|$, where $|P|$ is the number of productions.

## Classic examples

**Statements that start with an identifier.** An assignment and a procedure call both start with $\mathit{id}$:

$$S \to \mathit{id} := E \mid \mathit{id}\ (\,L\,), \qquad L \to E \mid E\ ,\ L.$$

Left factoring gives

$$S \to \mathit{id}\ S', \quad S' \to := E \mid (\,L\,), \qquad L \to E\ L', \quad L' \to \varepsilon \mid ,\ L.$$

With $E \to \mathit{id} \mid \mathit{num}$ the result is LL(1): $S'$ chooses on $:=$ or $($, and $L'$ chooses $, L$ on the comma and $\varepsilon$ on $)$.

**Right-recursive expressions.** The grammar $E \to T + E \mid T$, $T \to a$ is not LL(1), because both alternatives start with $T$. Factoring gives

$$E \to T\ E', \qquad E' \to +\ E \mid \varepsilon,$$

which is LL(1). This is the same shape that [left recursion removal](/left-recursion-removal/) produces from the left-recursive $E \to E + T \mid T$.

**Several rounds.** The grammar $A \to a b c \mid a b d \mid a e \mid f$ needs two steps. The longest common prefix is $a b$, of the first two alternatives; the next one is $a$, of $a\,A''$ and $a e$:

$$A \to a\ A' \mid f, \qquad A' \to b\ A'' \mid e, \qquad A'' \to c \mid d.$$

**The dangling else.** The statement grammar

$$S \to \mathbf{if}\ E\ \mathbf{then}\ S \mid \mathbf{if}\ E\ \mathbf{then}\ S\ \mathbf{else}\ S \mid \mathit{other}$$

becomes

$$S \to \mathbf{if}\ E\ \mathbf{then}\ S\ S' \mid \mathit{other}, \qquad S' \to \mathbf{else}\ S \mid \varepsilon.$$

The FIRST/FIRST conflict is gone, but the grammar is still ambiguous, and it is still not LL(1): $\mathbf{else}$ is in FIRST of $\mathbf{else}\ S$ and also in $\mathrm{FOLLOW}(S')$. Parsers resolve this by always choosing $S' \to \mathbf{else}\ S$, which attaches each else to the nearest unmatched if.

**A hidden prefix.** In $A \to B c \mid a d$, $B \to a b$, the two alternatives start with different symbols, so LEFT-FACTOR does nothing. Substituting $B$ gives $A \to a b c \mid a d$, and factoring gives $A \to a A'$, $A' \to b c \mid d$.

## Variations

- **Factoring with substitution.** Replace a leading nonterminal of an alternative by its right sides, then factor. This exposes hidden prefixes, but it can grow the grammar and it does not always end (see the pitfalls).
- **Factoring in EBNF and hand-written parsers.** In extended BNF one writes $A \to \alpha\ (\beta_1 \mid \beta_2)$ and no new name is needed. In [recursive descent](/recursive-descent-parsing/), the code for $A$ reads $\alpha$ and then branches on the next token.
- **More lookahead instead.** An [LL(k)](/ll-k-parsing/) parser can choose between $\alpha \beta_1$ and $\alpha \beta_2$ without factoring when the strings they derive, followed by what can follow $A$, always differ within their first $k$ terminals. Backtracking parsers and [parsing expression grammars](/parsing-expression-grammar/) try the alternatives in order instead, at the cost of time or of a changed meaning of choice.
- **Factoring for bottom-up parsers.** LR parsers need no left factoring. Factoring common suffixes is sometimes used to reduce the number of reductions, but it is not needed for determinism.

## Pitfalls

- **The trees change.** The new node $A'$ is not in the old trees. Semantic actions written for $A \to \alpha \beta_1$ must be split: the code for $A'$ needs the values of $\alpha$, usually passed as inherited attributes or arguments.
- **Ambiguity remains.** Left factoring is a one-to-one map on parse trees, so it cannot remove ambiguity, as the dangling-else example shows.
- **Not enough for LL(1).** After factoring, a nonterminal with an $\varepsilon$ alternative $A' \to \beta \mid \varepsilon$ is LL(1) only if $\mathrm{FIRST}(\beta) \cap \mathrm{FOLLOW}(A') = \emptyset$. Hidden prefixes through nonterminals or nullable symbols are not seen by the procedure.
- **Substitution may not end.** With $S \to A \mid B$, $A \to a A b \mid a b$, $B \to a B c \mid a c$, substituting $A$ and $B$ and factoring gives $S \to a S_1$ with $S_1 \to A b \mid b \mid B c \mid c$. The alternatives $A b$ and $B c$ again start with nonterminals that both begin with $a$, and each further round of substitution and factoring makes a new nonterminal of the same shape, with one more $b$ or $c$ at the end of its alternatives.
- **Left recursion first.** Left factoring does not remove [left recursion](/left-recursion/). The usual order is to remove left recursion first and then to factor, because removing left recursion can create new common prefixes.
- **Keep the longest prefix.** Factoring a shorter prefix than the longest common one is also correct, but it leaves common prefixes in $A'$, and the procedure needs more steps.

## References
