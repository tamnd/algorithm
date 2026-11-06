---
tag: 563D5B
kind: definition
slug: sentential-form
name: Sentential form
area: automata-and-parsing/context-free-parsing
level: intro
summary: Any string of terminals and nonterminals derivable from the start symbol.
prereqs: [context-free-grammar, derivation]
see_also: [leftmost-derivation, handle, viable-prefix, shift-reduce-parsing, top-down-parsing, parse-tree, bottom-up-parsing]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 5.1.6, Sentential Forms (left-sentential and right-sentential forms)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.2.3, Derivations (sentential form, sentence, left-sentential form); Section 4.5.2, Handle Pruning (right-sentential forms)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Chapter 2, Grammars as a Generating Device (sentential forms and sentences)
---

A sentential form of a [context-free grammar](/context-free-grammar/) is a string of terminals and nonterminals that can be [derived](/derivation/) from the start symbol. The sentential forms are the lines that appear in derivations, and the ones made of terminals only are the sentences, that is, the strings of the language. The forms that come from [leftmost](/leftmost-derivation/) and rightmost derivations are the ones that top-down and bottom-up parsers track, and the [handles](/handle/) and [viable prefixes](/viable-prefix/) of LR parsing are defined on right-sentential forms.

## Definition

We use the notation of the [context-free grammar](/context-free-grammar/) page: a grammar $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. A derivation step $\beta A \gamma \Rightarrow \beta \alpha \gamma$ uses a production $A \to \alpha$, and $\Rightarrow^*$ is its reflexive and transitive closure.

A string $\alpha \in (V \cup \Sigma)^*$ is a **sentential form** of $G$ if $S \Rightarrow^* \alpha$. Write

$$SF(G) = \{\, \alpha \in (V \cup \Sigma)^* : S \Rightarrow^* \alpha \,\}.$$

- A **sentence** of $G$ is a sentential form in $\Sigma^*$. So $L(G) = SF(G) \cap \Sigma^*$.
- A **left-sentential form** is an $\alpha$ with $S \Rightarrow_{lm}^* \alpha$, where each step rewrites the leftmost nonterminal.
- A **right-sentential form** is an $\alpha$ with $S \Rightarrow_{rm}^* \alpha$, where each step rewrites the rightmost nonterminal.

Three facts follow at once from the definition.

1. $S$ itself is a sentential form (a derivation with zero steps), and so are $\alpha$ for each production $S \to \alpha$.
2. $SF(G)$ is closed under derivation: if $\alpha \in SF(G)$ and $\alpha \Rightarrow^* \beta$, then $\beta \in SF(G)$, because the two derivations can be joined.
3. Each sentence is both a left-sentential and a right-sentential form. A string $w \in \Sigma^*$ with $S \Rightarrow^* w$ has a [parse tree](/parse-tree/), and that tree gives a leftmost and a rightmost derivation of $w$.

**$SF(G)$ is a context-free language.** Make a grammar $G'$ whose terminals are $V \cup \Sigma$. For each $A \in V$ take a new nonterminal $A'$. For each production $A \to X_1 \cdots X_k$ of $G$, put $A' \to Y_1 \cdots Y_k$ in $G'$, where $Y_i = X_i'$ if $X_i \in V$ and $Y_i = X_i$ if $X_i \in \Sigma$. Also put $A' \to A$ for each $A \in V$, and take $S'$ as the start symbol. A derivation in $G'$ is a derivation in $G$ in which each nonterminal occurrence is either rewritten further (as $A'$) or frozen (by $A' \to A$). By induction on the length of the derivation, $S' \Rightarrow^* \alpha$ in $G'$ for $\alpha \in (V \cup \Sigma)^*$ if and only if $S \Rightarrow^* \alpha$ in $G$. So $L(G') = SF(G)$, and $|G'| = |G| + 2|V|$. In particular, any general recognizer, such as the [CYK algorithm](/cyk-algorithm/) or the [Earley parser](/earley-parser/), run on $G'$ tests whether a given string is a sentential form of $G$.

## Examples and non-examples

**Equal counts.** For $S \to aSb \mid \varepsilon$, the sentential forms are $a^k S b^k$ and $a^k b^k$ for $k \ge 0$. Each derivation step either replaces $S$ by $aSb$ or erases it, and there is only ever one nonterminal. There are 7 sentential forms of length at most 6: $S$, $aSb$, $aaSbb$ and $\varepsilon$, $ab$, $aabb$, $aaabbb$. Since each form has at most one nonterminal, the left-sentential, the right-sentential and the plain sentential forms are the same here.

**Expressions.** Take the expression grammar

$$E \to E + T \mid T, \qquad T \to T * F \mid F, \qquad F \to (\,E\,) \mid a.$$

The rightmost derivation of $a + a * a$ is

$$E \Rightarrow E + T \Rightarrow E + T * F \Rightarrow E + T * a \Rightarrow E + F * a \Rightarrow E + a * a \Rightarrow T + a * a \Rightarrow F + a * a \Rightarrow a + a * a.$$

Each of its 9 lines is a right-sentential form. A [shift-reduce parser](/shift-reduce-parsing/) visits these lines from the last to the first: it finds the [handle](/handle/) of each right-sentential form and replaces it by a nonterminal.

- $E + T * F$ and $E + a * a$ are sentential forms, and right-sentential forms.
- $a + T$ is a sentential form ($E \Rightarrow E + T \Rightarrow T + T \Rightarrow F + T \Rightarrow a + T$) and a left-sentential form, but not a right-sentential form: a rightmost derivation rewrites $T$ before it can touch the $E$ on the left.
- $(\,E\,) * F$ is a sentential form: $E \Rightarrow T \Rightarrow T * F \Rightarrow F * F \Rightarrow (\,E\,) * F$.
- **Non-example.** $E * a$ is not a sentential form. The only productions that put a symbol to the right of a nonterminal $E$ are $E \to E + T$ and $F \to (\,E\,)$, so in any sentential form an $E$ is followed by $+$, by $)$ or by nothing. The same argument rules out $T * E$, and $E +$ is ruled out because $T$ never derives the empty string.

**Neither left nor right.** For $S \to ABC$, $A \to a$, $B \to b$, $C \to c$, the form $aBc$ is a sentential form ($S \Rightarrow ABC \Rightarrow aBC \Rightarrow aBc$). The left-sentential forms are $S$, $ABC$, $aBC$, $abC$, $abc$, and the right-sentential forms are $S$, $ABC$, $ABc$, $Abc$, $abc$. So $aBc$ is in neither list. It is reached only by mixing the order of the steps.

**Balanced parentheses.** For $S \to SS \mid (\,S\,) \mid \varepsilon$, the sentential forms of length at most 3 are 8 strings: $\varepsilon$, $S$, $SS$, $()$, $SSS$, $S()$, $(S)$ and $()S$. The string $)S($ is a non-example, since in every sentential form each prefix has at least as many $($ as $)$.

**Non-example: a string with a symbol of no grammar.** A string that holds a symbol outside $V \cup \Sigma$ is never a sentential form. Neither is a string over $V \cup \Sigma$ that holds a nonterminal that is not reachable from $S$, such as $B$ in a grammar where no right side reachable from $S$ contains $B$ ([useless symbols](/useless-symbol-elimination/)).

## Related definitions

- A [derivation](/derivation/) is a sequence of sentential forms, each obtained from the one before by one step. A [leftmost derivation](/leftmost-derivation/) goes through left-sentential forms only.
- The [language](/context-free-language/) of $G$ is the set of sentences, the sentential forms without nonterminals.
- A [handle](/handle/) of a right-sentential form $\gamma$ is the occurrence of a right side that the last step of a rightmost derivation of $\gamma$ produced, and a [viable prefix](/viable-prefix/) is a prefix of a right-sentential form that does not extend past its handle. A [top-down parser](/top-down-parsing/) works through left-sentential forms, and a [bottom-up parser](/bottom-up-parsing/) through right-sentential forms in reverse.
- A [parse tree](/parse-tree/) whose leaves, read from left to right, spell $\alpha$ is a tree for the sentential form $\alpha$. Its leaves may be nonterminals, which are not yet expanded.

## References
