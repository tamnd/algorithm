---
tag: 0ZR2G1
kind: definition
slug: context-free-grammar
name: Context-free grammar
aliases:
- CFG
area: automata-and-parsing/context-free-parsing
level: intro
summary: A grammar whose productions replace one nonterminal at a time, generating a context-free language.
prereqs: [alphabet, regular-language]
see_also: [context-free-language, derivation, parse-tree, ambiguity, chomsky-normal-form, pushdown-automaton, cyk-algorithm, earley-parser]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 5.1, Context-Free Grammars (5.1.2 Definition of Context-Free Grammars, 5.1.3 Derivations Using a Grammar, 5.1.5 The Language of a Grammar)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.1, Context-Free Grammars (Definition 2.2)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.2, Context-Free Grammars
  - paper: doi:10.1016/S0019-9958(59)90362-6
    title: Noam Chomsky, On certain formal properties of grammars, Information and Control 2(2) (1959)
    locator: pp. 137 to 167 (the hierarchy of grammar types, with the context-free type among them)
  - paper: doi:10.1145/367236.367262
    title: Peter Naur (editor), Report on the algorithmic language ALGOL 60, Communications of the ACM 3(5) (1960)
    locator: pp. 299 to 311 (the syntax of ALGOL 60 in the metalinguistic notation now called BNF)
---

A context-free grammar is a finite set of rewriting rules, each of which replaces one nonterminal symbol by a string of symbols, no matter what surrounds it. Starting from a start symbol and applying rules until only terminal symbols are left gives the strings of the grammar, and the set of these strings is a [context-free language](/context-free-language/). Context-free grammars describe the syntax of nearly every programming language, and parsers such as [CYK](/cyk-algorithm/), [Earley](/earley-parser/) and the LR family take a grammar and a string and recover how the grammar produces the string.

## Definition

A **context-free grammar** is a 4-tuple $G = (V, \Sigma, P, S)$ where

- $V$ is a finite set of **nonterminals** (also called variables);
- $\Sigma$ is a finite [alphabet](/alphabet/) of **terminals**, with $V \cap \Sigma = \emptyset$;
- $P \subseteq V \times (V \cup \Sigma)^*$ is a finite set of **productions**; a production $(A, \alpha)$ is written $A \to \alpha$, its **left side** is $A$ and its **right side** is $\alpha$;
- $S \in V$ is the **start symbol**.

**Derivation.** For strings $\beta, \gamma \in (V \cup \Sigma)^*$, write $\beta A \gamma \Rightarrow \beta \alpha \gamma$ when $A \to \alpha \in P$. This is one **derivation step**. The relation $\Rightarrow^*$ is the reflexive and transitive closure of $\Rightarrow$, and $\Rightarrow^+$ is the transitive closure. A string $\alpha \in (V \cup \Sigma)^*$ with $S \Rightarrow^* \alpha$ is a [sentential form](/sentential-form/). The **language** of $G$ is

$$L(G) = \{\, w \in \Sigma^* : S \Rightarrow^* w \,\}.$$

The word *context-free* means that the step that rewrites $A$ does not look at $\beta$ or $\gamma$. A [derivation](/derivation/) is a sequence of steps, and a [parse tree](/parse-tree/) records which production rewrote each nonterminal, without the order of the steps.

**Notation.** The parsing pages of this site use one notation. The productions $A \to \alpha$ and $A \to \beta$ with the same left side are written together as $A \to \alpha \mid \beta$. The empty string is $\varepsilon$, so $A \to \varepsilon$ is an **$\varepsilon$-production**. A production $A \to B$ with $B \in V$ is a **unit production**. Upper-case letters $A, B, C, \ldots, S$ are nonterminals, lower-case letters $a, b, c$ and symbols such as $+$ and $($ are terminals, $X, Y$ are symbols of either kind, $u, v, w, x, y, z$ are strings of terminals, and Greek letters $\alpha, \beta, \gamma$ are strings over $V \cup \Sigma$. The input string of a parser is $w = a_1 a_2 \cdots a_n$, so $n$ is the input length. The **size** of the grammar is

$$|G| = \sum_{A \to \alpha \,\in\, P} \bigl(|\alpha| + 1\bigr),$$

the number of symbols needed to write all productions down. When only productions are listed, the start symbol is the left side of the first one.

## Examples and non-examples

**Equal counts.** The grammar $S \to aSb \mid \varepsilon$ generates $L = \{a^k b^k : k \ge 0\}$. Each step that uses $S \to aSb$ adds one $a$ on the left and one $b$ on the right, and the last step erases $S$. For instance $S \Rightarrow aSb \Rightarrow aaSbb \Rightarrow aabb$. The language is not a [regular language](/regular-language/): a finite automaton cannot count the $a$'s, which the [pumping lemma for regular languages](/pumping-lemma-for-regular-languages/) makes exact. So context-free grammars describe more than regular expressions do.

**Arithmetic expressions.** The grammar

$$E \to E + T \mid T, \qquad T \to T * F \mid F, \qquad F \to (\,E\,) \mid a$$

has $V = \{E, T, F\}$, $\Sigma = \{+, *, (, ), a\}$, start symbol $E$ and size $|G| = 4 + 2 + 4 + 2 + 4 + 2 = 18$. A derivation of $a + a * a$ that always rewrites the leftmost nonterminal is

$$E \Rightarrow E + T \Rightarrow T + T \Rightarrow F + T \Rightarrow a + T \Rightarrow a + T * F \Rightarrow a + F * F \Rightarrow a + a * F \Rightarrow a + a * a.$$

The string has exactly one parse tree, and in it $*$ sits below $+$, so the grammar encodes the usual precedence. The string $a + {*}\,a$ is not in the language. The productions $E \to E + T$ and $T \to T * F$ are [left recursive](/left-recursion/), which is fine for LR parsers and fatal for a naive [recursive descent parser](/recursive-descent-parsing/).

**Balanced parentheses.** $S \to SS \mid (\,S\,) \mid \varepsilon$ generates the [Dyck language](/dyck-language/) on one pair of brackets. Its words of length at most 6 are the 9 strings $\varepsilon$, $()$, $(())$, $()()$ and the 5 balanced strings of length 6. This grammar is [ambiguous](/ambiguity/): already $\varepsilon$ has infinitely many parse trees, because $S \Rightarrow SS \Rightarrow S \Rightarrow \varepsilon$ can repeat.

**Palindromes.** $S \to aSa \mid bSb \mid a \mid b \mid \varepsilon$ generates the palindromes over $\{a, b\}$. It has 13 words of length at most 4: 1 of length 0, 2 of length 1, 2 of length 2, 4 of length 3 and 4 of length 4.

**The empty language.** $S \to aS$ is a context-free grammar, and $L(G) = \emptyset$: each sentential form still holds $S$, so no derivation ends in a terminal string. A grammar may have [useless symbols](/useless-symbol-elimination/) like this one. Deciding whether $L(G) = \emptyset$ is the [CFG emptiness problem](/cfg-emptiness-problem/).

**Non-example: a left side with context.** The rules

$$S \to aSBc \mid abc, \qquad cB \to Bc, \qquad bB \to bb$$

form a grammar, but not a context-free one: the left sides $cB$ and $bB$ have two symbols, so a rule may fire only next to a given neighbor. This grammar generates $\{a^k b^k c^k : k \ge 1\}$, which no context-free grammar generates, by the [pumping lemma for context-free languages](/cfl-pumping-lemma/).

**Non-example: infinitely many rules.** The rule scheme $S \to a^k b^k$ for every $k \ge 0$ defines the same language as the first example, but it is not a grammar in the sense above, because $P$ must be finite. Finiteness is what lets an algorithm read the whole grammar.

**Non-example: a terminal on the left.** A rule $a \to b$ is not allowed: only a nonterminal may be rewritten.

## Related definitions

- A [context-free language](/context-free-language/) is $L(G)$ for some context-free grammar $G$; the same languages are the languages of [pushdown automata](/pushdown-automaton/), by the [equivalence of CFGs and PDAs](/cfg-pda-equivalence/).
- A [derivation](/derivation/) is a sequence of steps, a [leftmost derivation](/leftmost-derivation/) always rewrites the leftmost nonterminal, and a [parse tree](/parse-tree/) forgets the order of the steps.
- A grammar is [ambiguous](/ambiguity/) when some string has two parse trees. A language all of whose grammars are ambiguous has [inherent ambiguity](/inherent-ambiguity/).
- A [linear grammar](/linear-grammar/) has at most one nonterminal on each right side. A right-linear grammar, with productions $A \to aB$ and $A \to \varepsilon$ only, generates exactly the [regular languages](/regular-language/).
- [Chomsky normal form](/chomsky-normal-form/) allows only $A \to BC$ and $A \to a$ (and $S \to \varepsilon$). [Greibach normal form](/greibach-normal-form/) allows only $A \to a B_1 \cdots B_k$. Every grammar can be converted to both forms for the same language, except for the empty string.
- A [nullable symbol](/nullable-symbol/) is a nonterminal $A$ with $A \Rightarrow^* \varepsilon$. [Epsilon-production elimination](/epsilon-production-elimination/) and [unit-production elimination](/unit-production-elimination/) remove the two special kinds of production.
- Subclasses that parse in linear time: [LL grammars](/ll-grammar/), [LR grammars](/lr-grammar/), [LALR grammars](/lalr-grammar/) and [SLR grammars](/slr-grammar/).
- A [probabilistic context-free grammar](/probabilistic-context-free-grammar/) adds a probability to each production. A [parsing expression grammar](/parsing-expression-grammar/) looks similar but uses ordered choice, and its strings are defined by a recognizer, not by derivations.
- In BNF, the notation of the ALGOL 60 report, a production $A \to \alpha \mid \beta$ is written `<A> ::= α | β`.

## References
