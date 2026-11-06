---
tag: 5G3BXT
kind: problem
slug: left-recursion-removal
name: Left recursion removal
aliases:
- left recursion elimination
area: automata-and-parsing/context-free-parsing
level: core
summary: Rewrite a grammar with left-recursive productions into an equivalent one suitable for top-down parsing.
model: word-ram
complexity:
  vars: {g: the size of the input grammar}
  time: {worst: O(g^2)}
prereqs: [left-recursion, context-free-grammar, nullable-symbol]
see_also: [left-recursion-elimination, greibach-normal-form, left-corner-parsing, epsilon-production-elimination, ll1-parsing, recursive-descent-parsing, left-factoring, top-down-parsing]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.3.3, Elimination of Left Recursion
  - paper: "Robert C. Moore, Removing left recursion from context-free grammars, Proceedings of the 1st North American Chapter of the Association for Computational Linguistics Conference (NAACL 2000)"
    locator: pp. 249 to 255 (the standard algorithm, the left-corner transform, and their output sizes)
  - paper: doi:10.1145/321250.321254
    title: Sheila A. Greibach, A new normal-form theorem for context-free phrase structure grammars, Journal of the ACM 12(1) (1965)
    locator: pp. 42 to 52
  - paper: "Daniel J. Rosenkrantz and Philip M. Lewis II, Deterministic left corner parsing, IEEE Conference Record of the 11th Annual Symposium on Switching and Automata Theory (1970)"
    locator: pp. 139 to 152
---

Left recursion removal is the problem of turning a [context-free grammar](/context-free-grammar/) into one that generates the same language and has no [left recursion](/left-recursion/), that is, no nonterminal $A$ with $A \Rightarrow^+ A \gamma$. [Top-down parsers](/top-down-parsing/) need it, because a parser that expands $A$ to look for $A$ again loops without reading input. Every grammar has a solution, and the textbook [left recursion elimination algorithm](/left-recursion-elimination/) finds one; the open part is how small the output can be kept.

## In plain words

Some grammar rules mention themselves at their very start, for example "an expression is an expression, a plus sign and a term". A parser that reads from left to right and works from the top down cannot use such a rule: to find an expression it must first find an expression.

The task is to rewrite the grammar so that no rule leads back to itself before reading anything, without changing which sentences it accepts. The self-reference may be direct, or may go through other rules, or may hide behind parts that can be empty. The new grammar usually describes the same sentences with a different shape, for example with lists that grow to the right instead of to the left.

## Definition

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area.

A nonterminal $A$ is *left-recursive* if $A \Rightarrow^+ A \gamma$ for some string $\gamma$. A grammar is left-recursive if one of its nonterminals is.

> **Problem.** Given a grammar $G$, output a grammar $G'$ with $L(G') = L(G)$ in which no nonterminal is left-recursive.

The output is judged by its size $|G'|$ and by how closely its parse trees follow those of $G$. Deciding whether $G$ is left-recursive at all is easy: draw an edge $X \to Y$ for each production $X \to \mu Y \nu$ with $\mu$ [nullable](/nullable-symbol/); $G$ is left-recursive exactly when this *left-corner graph* has a cycle, which [cycle detection](/cycle-detection/) finds in $O(|G|)$ time.

## Variants

- **Direct left recursion only.** Every left-recursive production has the form $A \to A \alpha$. Then the rewriting $A \to \beta A'$, $A' \to \alpha A' \mid \varepsilon$ of each such $A$ is enough.
- **Without empty productions.** The output may also be required to have no $\varepsilon$-production, except $S \to \varepsilon$ when $\varepsilon \in L(G)$ and $S$ occurs on no right side.
- **Greibach normal form.** A stronger requirement: every production has the form $A \to a \alpha$ with $a \in \Sigma$ and $\alpha \in V^*$. Such a grammar has no left recursion. See [Greibach normal form](/greibach-normal-form/).
- **Keeping the structure.** The output should let a parser rebuild the parse trees of $G$, for example so that $a - b - c$ still groups as $(a - b) - c$. The left-corner transform below has this property: each tree of the output maps back to a tree of $G$.
- **Smallest output.** Among the solutions, find one of least size, or at least one that is not much larger than $G$.

## Examples

**A left-recursive list.** $L \to L \, , \, x \mid x$ generates $x$, $x, x$, $x, x, x$, and so on. The grammar $L \to x L'$, $L' \to , \, x L' \mid \varepsilon$ generates the same lists and has no left recursion.

**The expression grammar.** $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to ( E ) \mid id$ becomes $E \to T E'$, $E' \to + T E' \mid \varepsilon$, $T \to F T'$, $T' \to * F T' \mid \varepsilon$, $F \to ( E ) \mid id$, the input of the [LL(1) parser](/ll1-parsing/).

**Indirect.** In $S \to A a \mid b$, $A \to S d \mid c$, neither production starts with its own left side, but $S \Rightarrow A a \Rightarrow S d a$. Substituting $S$ into $A$ gives $A \to A a d \mid b d \mid c$, and then $A \to b d A' \mid c A'$, $A' \to a d A' \mid \varepsilon$, while $S \to A a \mid b$ stays.

**Hidden.** In $A \to B A c \mid a$, $B \to b \mid \varepsilon$, no production starts with $A$, but $A \Rightarrow B A c \Rightarrow A c$. Removing the empty production of $B$ exposes it: $A \to B A c \mid A c \mid a$, $B \to b$, which becomes $A \to B A c A' \mid a A'$, $A' \to c A' \mid \varepsilon$.

**An ambiguous grammar.** $S \to S S \mid a$ becomes $S \to a S'$, $S' \to S S' \mid \varepsilon$. The output has no left recursion but is still ambiguous, so removal alone does not make a grammar [LL(1)](/ll-grammar/).

**A cycle.** $S \to S \mid a$ is left-recursive by $S \to S$. Here removal just drops $S \to S$. In general a cycle $A \Rightarrow^+ A$ is removed by merging the nonterminals on it, since they all derive the same strings.

## Known algorithms

| method | output size | notes |
|---|---|---|
| direct rewriting $A \to \beta A'$, $A' \to \alpha A' \mid \varepsilon$ | $O(\lvert G \rvert)$ | only for direct left recursion |
| [Paull's algorithm](/left-recursion-elimination/) | exponential in the worst case | orders the nonterminals and substitutes; the textbook method |
| left-corner transform after preparation | $O(\lvert G \rvert^2)$ | Rosenkrantz and Lewis (1970); keeps the trees recoverable |
| Moore's methods | smaller in practice | selective substitution and a selective left-corner transform |
| [Greibach normal form conversion](/greibach-normal-form-conversion/) | exponential for the classic method | solves the stronger variant |

**Preparation.** Most methods first make the grammar free of empty productions and of cycles $A \Rightarrow^+ A$: they remove the nonterminals that derive no terminal string, apply [epsilon-production elimination](/epsilon-production-elimination/), and merge the nonterminals of each cycle of unit productions $A \to B$. The empty string, if it is in $L(G)$, is added back with a new start symbol $S_0 \to S \mid \varepsilon$. To keep this step linear, split long right sides first, so that each right side has at most two symbols; then each production has at most four versions with nullable symbols left out.

**The left-corner transform.** For a prepared grammar with nonterminals $V$, introduce a new nonterminal $A\text{-}X$ for each $A \in V$ and each symbol $X$; it derives the strings $w$ such that $A \Rightarrow^* X w$ in a tree whose leftmost path goes from $A$ down to $X$. The productions are:

- $A \to a \; A\text{-}a$ for every $A \in V$ and $a \in \Sigma$;
- $A\text{-}X \to \beta \; A\text{-}B$ for every $A \in V$ and every production $B \to X \beta$ of $G$;
- $A\text{-}A \to \varepsilon$ for every $A \in V$.

Every production of an original $A$ starts with a terminal, and the only nullable right sides are those with $\beta = \varepsilon$, which come from unit productions. So a left recursion would need a cycle of unit productions, which the preparation removed. Each production $B \to X \beta$ is copied once for each $A$, so the output has size $O(|V| \cdot |G| + |V| \cdot |\Sigma|)$, which is $O(|G|^2)$ including the preparation.

## Bounds

- **Existence.** Every context-free grammar has an equivalent grammar without left recursion; Greibach (1965) proved the stronger statement that every context-free language without $\varepsilon$ has a grammar in Greibach normal form.
- **Upper bound.** By the left-corner transform, output size $O(|G|^2)$ and time $O(|G|^2)$ always suffice.
- **Lower bound.** Any method reads the whole grammar, so it takes $\Omega(|G|)$ time.
- **Paull's algorithm** can produce an output of size $2^{\Omega(|G|)}$ even on a grammar without left recursion, for a bad order of the nonterminals: with $A_0 \to a$ and $A_i \to A_{i-1} x \mid A_{i-1} y$, processing $A_0, A_1, \ldots$ in this order expands $A_i$ into $2^i$ productions. Moore (2000) reports that on large natural-language grammars the standard algorithm produces grammars far too large to use, and that his variants keep them manageable.

## Reductions

- **Detection to cycle detection.** A grammar is left-recursive if and only if its left-corner graph has a cycle, as in the definition.
- **Greibach normal form.** A grammar in Greibach normal form has no left recursion, so any conversion to it solves this problem; conversely, the classic conversion first removes left recursion and then substitutes forward.
- **LL(1) table construction.** A grammar whose [LL parse table](/ll-parse-table/) has no conflict and no useless symbol is not left-recursive, so left recursion removal is a necessary step on the way from a typical expression grammar to an LL(1) grammar, usually together with [left factoring](/left-factoring/).

## Applications

- **Recursive descent and LL parsing.** Hand-written [recursive descent parsers](/recursive-descent-parsing/) and table-driven LL parsers need grammars without left recursion. In practice the parser often implements the result as a loop, `parse T; while next is "+": parse "+" and T`, and rebuilds the left-associative tree as it goes.
- **Top-down natural-language parsing.** Grammars for natural language are full of left recursion, such as a noun phrase that starts with a possessive noun phrase. Top-down and [left-corner parsers](/left-corner-parsing/) for them use the left-corner transform or Moore's variants.
- **Normal forms.** Removal is a step of the conversion to Greibach normal form, which in turn gives a [pushdown automaton](/pushdown-automaton/) that reads one input symbol on every move.

## References
