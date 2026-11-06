---
tag: 7CKCH5
kind: definition
slug: parsing-expression-grammar
name: Parsing expression grammar
aliases:
- PEG
area: automata-and-parsing/context-free-parsing
level: advanced
summary: A grammar with ordered choice and greedy repetition that always defines a deterministic parser.
prereqs: [context-free-grammar, recursive-descent-parsing, backtracking-parsing]
see_also: [packrat-parsing, parser-combinators, left-recursion, regex-lookaround, greedy-and-lazy-quantifiers, ll-grammar, ambiguity, memoization]
sources:
  - paper: doi:10.1145/964001.964011
    title: Bryan Ford, Parsing expression grammars, a recognition-based syntactic foundation, Proceedings of the 31st ACM Symposium on Principles of Programming Languages (POPL 2004)
    locator: pp. 111 to 122 (the definition, the formal semantics, well-formed grammars, the a^n b^n c^n example, closure under intersection and complement, and the undecidability of emptiness)
  - paper: doi:10.1145/581478.581483
    title: Bryan Ford, Packrat parsing, simple, powerful, lazy, linear time, Proceedings of the seventh ACM SIGPLAN International Conference on Functional Programming (ICFP 2002)
    locator: pp. 36 to 47 (linear-time parsing of such grammars by memoization)
  - paper: doi:10.1016/S0019-9958(73)90851-6
    title: Alexander Birman and Jeffrey D. Ullman, Parsing algorithms with backtrack, Information and Control 23(1) (1973)
    locator: pp. 1 to 34 (TDPL and GTDPL, the formal systems that PEGs generalize)
  - url: https://arxiv.org/abs/1304.3177
    title: Fabio Mascarenhas, Sérgio Medeiros and Roberto Ierusalimschy, On the relation between context-free grammars and parsing expression grammars, Science of Computer Programming (2014)
    locator: the result that an LL(1) grammar read as a PEG recognizes the same language
---

A parsing expression grammar (PEG) describes a language by a recognizer instead of a generator. Each nonterminal has exactly one rule, a parsing expression built from terminals, nonterminals, sequence, **ordered choice** $e_1 / e_2$, greedy repetition $e^*$ and the **not-predicate** $!e$. Matching an expression against an input either succeeds and consumes a prefix, or fails, and the result is always unique: a PEG cannot be ambiguous. Ford introduced PEGs in 2004, building on the TDPL formalism of Birman and Ullman. A PEG reads like a [context-free grammar](/context-free-grammar/) written for a [backtracking recursive descent parser](/backtracking-parsing/), and [packrat parsing](/packrat-parsing/) runs it in linear time. The class of languages differs from the context-free languages: PEGs recognize $\{a^n b^n c^n\}$, and $S \leftarrow a\, S\, a \,/\, a$ does not mean what the same context-free rules mean.

## Definition

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. A PEG writes its rules with $\leftarrow$ and its choice with $/$, to stress that they are not productions.

**Expressions.** Over a finite set $V_T$ of terminals and a finite set $V_N$ of nonterminals, the parsing expressions are:

| expression | name |
|---|---|
| $\varepsilon$ | empty |
| $a$, for $a \in V_T$ | terminal |
| $A$, for $A \in V_N$ | nonterminal |
| $e_1\, e_2$ | sequence |
| $e_1 \,/\, e_2$ | ordered choice |
| $e^*$ | zero or more |
| $!e$ | not-predicate |

The usual abbreviations are $e^+ = e\, e^*$, $e? = e \,/\, \varepsilon$, $\&e = !!e$ (and-predicate), and $.$ for the choice of all terminals (any one symbol), so $!.$ succeeds exactly at the end of the input.

**Grammars.** A PEG is $G = (V_N, V_T, R, e_S)$, where $R$ gives each $A \in V_N$ exactly one expression $R(A)$, written $A \leftarrow R(A)$, and $e_S$ is the start expression, usually a nonterminal $S$.

**Semantics.** Matching $e$ at position $i$ of the input $x = x_1 \cdots x_n$ has a result $\mathrm{m}(e, i)$ that is either a position $j \ge i$ (success, consuming $x_{i+1} \cdots x_j$) or $\mathsf{fail}$:

- $\mathrm{m}(\varepsilon, i) = i$;
- $\mathrm{m}(a, i) = i + 1$ if $i < n$ and $x_{i+1} = a$, and $\mathsf{fail}$ otherwise;
- $\mathrm{m}(A, i) = \mathrm{m}(R(A), i)$;
- $\mathrm{m}(e_1 e_2, i) = \mathrm{m}(e_2, j)$ if $\mathrm{m}(e_1, i) = j$, and $\mathsf{fail}$ if $e_1$ fails;
- $\mathrm{m}(e_1 / e_2, i) = \mathrm{m}(e_1, i)$ if this succeeds, and $\mathrm{m}(e_2, i)$ otherwise: the second alternative is tried only when the first fails;
- $\mathrm{m}(e^*, i) = \mathrm{m}(e^*, j)$ if $\mathrm{m}(e, i) = j$, and $i$ if $e$ fails: as many repetitions as possible, never fewer;
- $\mathrm{m}(!e, i) = i$ if $e$ fails at $i$, and $\mathsf{fail}$ if $e$ succeeds: it consumes nothing.

Formally, Ford defines these results as the least relation closed under the rules, with a step count; a result exists when the recursion is finite. The **language** of $G$ is the set of strings $x$ on which $e_S$ succeeds. Ford's definition allows $e_S$ to consume only a prefix; for a full match, write $e_S$ as $S\, !.$, the convention on this page.

**Well-formed grammars.** A PEG is **well-formed** if no nonterminal is left-recursive, directly or through other nonterminals at the start of sequences, and no $e^*$ has an $e$ that can succeed without consuming input. On a well-formed grammar every expression succeeds or fails on every input at every position (Ford calls this completeness). Well-formedness is decidable by a fixed-point computation over the expressions, similar to the computation of [nullable symbols](/nullable-symbol/).

## Examples and non-examples

The results below were checked by an interpreter of the semantics above on all inputs up to length 9.

**Not context-free: $a^n b^n c^n$.** Ford's grammar

$$S \leftarrow \&(A\, c)\; a^+\; B\; !., \qquad A \leftarrow a\, A?\, b, \qquad B \leftarrow b\, B?\, c$$

accepts exactly $\{a^n b^n c^n : n \ge 1\}$. The and-predicate checks that $a^k b^k c$ follows without consuming it, then $a^+$ consumes all the $a$'s and $B$ checks $b^m c^m$ up to the end. The predicates act as an intersection of two context-free conditions.

**Ordered choice is not union.** $S \leftarrow a \,/\, a\, b$ with $S\, !.$ accepts $a$ but not $a\, b$. On $a\, b$, the first alternative succeeds and consumes $a$, so $S$ returns at once; $!.$ then fails, and nothing goes back to try $a\, b$. The context-free grammar $S \to a \mid a\, b$ generates both. Putting the longer alternative first, $S \leftarrow a\, b \,/\, a$, accepts both.

**Repetition is greedy.** $a^*\, a$ never succeeds: $a^*$ consumes every $a$, and the final $a$ then fails. A [regular expression](/regular-expression/) matcher would backtrack into the star; a PEG does not, as with the possessive quantifiers of [greedy and lazy quantifiers](/greedy-and-lazy-quantifiers/).

**Same rules, different language.** The context-free grammar $S \to a\, S\, a \mid a$ generates the odd numbers of $a$'s. The PEG $S \leftarrow a\, S\, a \,/\, a$ with $S\, !.$ accepts $a^n$ only for $n = 1, 3, 7, 15, 31, 63, \ldots$, that is $n = 2^k - 1$: the inner $S$ commits to the longest match it can find, which leaves too few $a$'s for the outer one. In the same way, $S \leftarrow a\, S\, a \,/\, b\, S\, b \,/\, a \,/\, b \,/\, \varepsilon$ accepts no even palindrome except $\varepsilon$, and misses 22 of the 45 palindromes over $\{a, b\}$ of length at most 7.

**Lexical rules.** $\mathit{If} \leftarrow i\, f\, !\mathit{IdChar}$ matches the keyword `if` but not the prefix of the identifier `ifx`. The not-predicate does what a separate lexer does by longest match, inside the grammar.

**The dangling else.** $\mathit{Stmt} \leftarrow \mathtt{if}\ C\ \mathtt{then}\ \mathit{Stmt}\ \mathtt{else}\ \mathit{Stmt} \,/\, \mathtt{if}\ C\ \mathtt{then}\ \mathit{Stmt} \,/\, \ldots$ attaches each `else` to the nearest `if`, with no conflict to resolve: the ordered choice is the resolution.

**Non-example: left recursion.** $E \leftarrow E + T \,/\, T$ is not well-formed. Matching $E$ at position $i$ needs the result of $E$ at position $i$, and a direct recursive implementation loops. The standard rewriting is $E \leftarrow T\, (+\, T)^*$; several PEG tools also accept left recursion through a special fixed-point rule, outside Ford's definition.

**Non-example: a star over the empty match.** $(a?)^*$ is not well-formed, because $a?$ succeeds without consuming input, so the repetition would never stop.

## Related definitions

- **Context-free grammars.** A CFG generates strings, and a string can have several derivations; a PEG recognizes, and a match has one result, so the notion of [ambiguity](/ambiguity/) does not arise. Reading the productions of a CFG as a PEG, with $\mid$ replaced by $/$, can change the language. For [LL(1)](/ll-grammar/) grammars it does not: Mascarenhas, Medeiros and Ierusalimschy showed that such a grammar, read as a PEG, recognizes the same language, since at most one alternative can start with the next token.
- **Expressive power.** The PEG languages are closed under union, intersection and complement (by $/$, $\&$ and $!$), and they include every [deterministic context-free language](/deterministic-context-free-language/) that has an LL(1) grammar, as well as languages such as $\{a^n b^n c^n\}$ that are not context-free. Ford left open whether every context-free language has a PEG. Whether a PEG accepts any string at all is undecidable (Ford, 2004), unlike the [emptiness problem](/cfg-emptiness-problem/) for CFGs.
- **TDPL and GTDPL.** Birman and Ullman's top-down parsing language (1973) has rules of the form $A \leftarrow B C / D$, $A \leftarrow a$, $A \leftarrow \varepsilon$ and $A \leftarrow f$ (failure). Ford showed that every well-formed PEG can be reduced to this form, so PEGs and TDPL describe the same languages.
- **Packrat parsing.** A [packrat parser](/packrat-parsing/) memoizes $\mathrm{m}(A, i)$ for every nonterminal and position, so each is computed once. On a well-formed PEG this takes $O(|G| \cdot n)$ time and space. Without memoization, a backtracking parser of a PEG can take exponential time.
- **Parser combinators.** Most [parser combinator](/parser-combinators/) libraries implement PEG semantics: the choice combinator commits to the first alternative that succeeds.
- **Regular expressions with lookaround.** The predicates $\&e$ and $!e$ are the lookahead assertions of [regex lookaround](/regex-lookaround/), applied to whole grammar expressions.

## References
