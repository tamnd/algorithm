---
tag: 70V34K
kind: definition
slug: regular-expression
name: Regular expression
aliases:
- regex
- regexp
- rational expression
area: automata-and-parsing/regular-expressions
level: intro
summary: A syntax built from symbols, union, concatenation and star that denotes a regular language.
prereqs: [alphabet, regular-language]
see_also: [kleene-theorem, kleene-star, regex-matching, thompson-construction, state-elimination, extended-regular-expressions, backreference, kleene-algebra]
sources:
  - paper: "Stephen C. Kleene, Representation of events in nerve nets and finite automata, in C. E. Shannon and J. McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press, 1956"
    locator: pp. 3 to 41 (regular events, the operations on them, and their equivalence with finite automata)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.3, Regular Expressions (the formal definition, examples, and the equivalence with finite automata)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 3.1, Regular Expressions, and Section 3.4, Algebraic Laws for Regular Expressions
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 7, Pattern Matching and Regular Expressions; Lecture 8, Regular Expressions and Finite Automata; Lecture 9, Kleene Algebra and Regular Expressions
---

A regular expression over a finite [alphabet](/alphabet/) $\Sigma$ is a term built from $\emptyset$, $\varepsilon$ and the symbols of $\Sigma$ with three operations: union, concatenation and the [Kleene star](/kleene-star/). Each regular expression $r$ denotes a language $L(r) \subseteq \Sigma^*$, and the languages that regular expressions denote are exactly the [regular languages](/regular-language/), by [Kleene's theorem](/kleene-theorem/). The pattern languages of programming tools ("regexes") start from this syntax, add many abbreviations, and in some engines add features that leave the regular languages.

## Definition

Let $\Sigma$ be a finite alphabet that does not contain the symbols $\emptyset$, $\varepsilon$, $|$, $*$, $($ and $)$.

**Syntax.** The regular expressions over $\Sigma$ are the smallest set of strings such that

1. $\emptyset$ and $\varepsilon$ are regular expressions, and each $a \in \Sigma$ is a regular expression;
2. if $r$ and $s$ are regular expressions, then $(r \mid s)$, $(r s)$ and $(r^*)$ are regular expressions.

**Semantics.** The language $L(r) \subseteq \Sigma^*$ is defined by structural recursion:

$$L(\emptyset) = \emptyset, \qquad L(\varepsilon) = \{\varepsilon\}, \qquad L(a) = \{a\},$$

$$L(r \mid s) = L(r) \cup L(s), \qquad L(r s) = L(r)\,L(s) = \{ x y : x \in L(r),\ y \in L(s) \}, \qquad L(r^*) = \bigcup_{k \ge 0} L(r)^k,$$

where $L^0 = \{\varepsilon\}$ and $L^{k+1} = L\,L^k$. So $L(r^*)$ is the set of all concatenations of zero or more strings of $L(r)$. Two expressions $r$ and $s$ are *equivalent*, written $r \equiv s$, when $L(r) = L(s)$.

**Notation used on these pages.** All pages of this sub-area use the syntax above: union is $|$, concatenation is writing side by side, star is a postfix $*$, and the constants are $\varepsilon$ and $\emptyset$. Parentheses may be dropped under the usual precedence: star binds tighter than concatenation, and concatenation binds tighter than union. Union and concatenation are associative in meaning, so $a \mid b \mid c$ and $abc$ need no parentheses. So $ab^* \mid c$ means $((a(b^*)) \mid c)$. These abbreviations are not part of the core syntax:

| abbreviation | meaning |
|---|---|
| $r^+$ | $r r^*$ |
| $r?$ | $r \mid \varepsilon$ |
| $r^k$ | $r r \cdots r$ with $k$ copies, and $r^0 = \varepsilon$ |
| $\Sigma$ | $a_1 \mid a_2 \mid \cdots \mid a_\sigma$, the union of all symbols |

**Size.** The *size* $|r|$ is the number of nodes of the syntax tree of $r$: one for each occurrence of $\emptyset$, $\varepsilon$ or a symbol, and one for each operator. The *alphabetic width* is the number of occurrences of symbols of $\Sigma$. Algorithms on regular expressions state their costs in one of these two measures. For example $(a \mid b)^* abb$ has size 10 and alphabetic width 5.

**Kleene's theorem.** A language $L \subseteq \Sigma^*$ is regular if and only if $L = L(r)$ for some regular expression $r$. The [Thompson construction](/thompson-construction/) gives one direction, with an [epsilon-NFA](/epsilon-nfa/) of at most $2|r|$ states. [State elimination](/state-elimination/) gives the other direction, and its output can be exponentially larger than the automaton. The proof is on the [Kleene's theorem](/kleene-theorem/) page.

**Algebraic laws.** These identities hold for all expressions $r, s, t$. Each one follows from the semantics, and they are listed with proofs in Section 3.4 of Hopcroft, Motwani and Ullman.

- $r \mid s \equiv s \mid r$, $\; (r \mid s) \mid t \equiv r \mid (s \mid t)$, $\; r \mid r \equiv r$, $\; r \mid \emptyset \equiv r$.
- $(rs)t \equiv r(st)$, $\; \varepsilon r \equiv r \varepsilon \equiv r$, $\; \emptyset r \equiv r \emptyset \equiv \emptyset$.
- $r(s \mid t) \equiv rs \mid rt$ and $(s \mid t)r \equiv sr \mid tr$.
- $\emptyset^* \equiv \varepsilon^* \equiv \varepsilon$, $\; (r^*)^* \equiv r^*$, $\; r^* \equiv \varepsilon \mid r r^*$, $\; (r \mid s)^* \equiv (r^* s^*)^*$.

As one example of the proofs, take $r^* \equiv \varepsilon \mid r r^*$. With $L = L(r)$, the right side denotes $L^0 \cup L \bigcup_{k \ge 0} L^k = L^0 \cup \bigcup_{k \ge 0} L^{k+1} = \bigcup_{k \ge 0} L^k$, because concatenation distributes over arbitrary unions. Concatenation does not commute and does not distribute over intersection, so $rs \not\equiv sr$ in general, and $r(s \cap t)$ has no counterpart in the syntax. The complete proof systems for equivalence add a rule for solving equations of the form $X \equiv rX \mid s$, as in [Arden's lemma](/arden-lemma/) and the axioms of [Kleene algebra](/kleene-algebra/).

## Examples and non-examples

### Expressions and their languages

The table gives, over $\Sigma = \{a, b\}$, the number of strings of each length $n = 0, 1, \ldots, 8$ in the language.

| expression | language | strings of length 0 to 8 |
|---|---|---|
| $(a \mid b)^*$ | all strings | 1, 2, 4, 8, 16, 32, 64, 128, 256 |
| $a^* b^*$ | no $a$ after a $b$ | 1, 2, 3, 4, 5, 6, 7, 8, 9 |
| $(ab)^*$ | $\varepsilon, ab, abab, \ldots$ | 1, 0, 1, 0, 1, 0, 1, 0, 1 |
| $(a \mid b)^* abb$ | strings that end in $abb$ | 0, 0, 0, 1, 2, 4, 8, 16, 32 |
| $b^*(ab^*ab^*)^*$ | an even number of $a$ | 1, 1, 2, 4, 8, 16, 32, 64, 128 |
| $(a \mid b)^* a (a \mid b)(a \mid b)$ | the third symbol from the end is $a$ | 0, 0, 0, 4, 8, 16, 32, 64, 128 |
| $a(\varepsilon \mid b)$ | $\{a, ab\}$ | 0, 1, 1, 0, 0, 0, 0, 0, 0 |
| $\emptyset^*$ | $\{\varepsilon\}$ | 1, 0, 0, 0, 0, 0, 0, 0, 0 |
| $\emptyset a$ | $\emptyset$ | 0 for each length |

Some remarks on the table:

- **Different expressions, one language.** $a^*(ba^*)^*$ and $(a^* b^*)^*$ are both equivalent to $(a \mid b)^*$. For the first one, cut a string before each $b$: the first piece is in $a^*$ and each other piece is in $ba^*$. Deciding such equivalences in general is [regex equivalence](/regex-equivalence/), which is [PSPACE-complete](/regex-equivalence-pspace-completeness/).
- **The empty set and the empty string differ.** $L(\emptyset) = \emptyset$ has no strings, and $L(\varepsilon) = \{\varepsilon\}$ has one. The star of $\emptyset$ is $\{\varepsilon\}$, since $L^0 = \{\varepsilon\}$ for every $L$, and a concatenation with $\emptyset$ is $\emptyset$.
- **Size and automata.** The expression $(a \mid b)^* a (a \mid b)^{n-1}$ has size $O(n)$, but the smallest DFA of its language has $2^n$ states; see the [regex DFA state blowup](/regex-dfa-state-blowup/).
- **Two ways to match.** The expression $(a \mid ab)(c \mid bc)$ denotes $\{ac, abc, abbc\}$, and it matches $abc$ in two ways: $a \cdot bc$ and $ab \cdot c$. The language does not care, but the [submatches](/submatch-extraction/) and the time of a [backtracking matcher](/backtracking-regex-matching/) do. See [regex ambiguity detection](/regex-ambiguity-detection/).

### Non-examples

- **Strings that are not expressions.** $a \mid$, $({*}a)$ and $a)($ are not regular expressions: rule 2 makes each operator take whole expressions as operands, and the parentheses must match. In this syntax an empty operand is written $\varepsilon$, so $a \mid \varepsilon$, not $a \mid$.
- **Languages with no expression.** $\{a^n b^n : n \ge 0\}$ is not regular, so no regular expression denotes it. The strings $a^i$ and $a^j$ with $i \ne j$ need different states in any DFA, since $a^i b^i$ is in the language and $a^j b^i$ is not. The [pumping lemma](/pumping-lemma-for-regular-languages/) gives the same result.
- **Backreferences.** The engine pattern `(a*)b\1` uses a [backreference](/backreference/): `\1` must repeat the exact string that the group matched. It matches exactly the strings $a^n b a^n$ with $n \ge 0$, and this language is not regular by the same argument with the suffix $b a^i$. So a pattern with backreferences is not a regular expression in the sense of this page, and [matching it](/backreference-matching/) is NP-complete in general.

### Engine syntax that stays regular

Pattern languages of tools such as grep, Perl, Python and RE2 add syntax. This list says which additions keep the language regular.

- **Abbreviations.** `.` (any symbol), `[abc]` (a class of symbols), `r+`, `r?` and the counter `r{m,n}` ([bounded repetition](/bounded-repetition/)) are shorthands for core expressions, so they stay regular. A counter can make the expression exponentially shorter: `a{1000}` has 7 characters and stands for an expression of size 1999.
- **Intersection and complement.** [Extended regular expressions](/extended-regular-expressions/) add $\cap$ and complement. The languages stay regular, because regular languages are [closed](/closure-properties-of-regular-languages/) under both, but the expressions can be far more succinct.
- **Anchors and lookaround.** `^`, `$` and [lookahead and lookbehind](/regex-lookaround/) without backreferences keep the set of matched strings regular.
- **Not regular.** Backreferences and the recursive patterns of PCRE go beyond the regular languages. Greedy and lazy [quantifiers](/greedy-and-lazy-quantifiers/) do not change the language matched as a whole string; they change which match an engine reports.

## Related definitions

- [Regular language](/regular-language/): the class of languages that regular expressions denote.
- [Kleene star](/kleene-star/): the operation $L^*$, the one source of infinite languages in the syntax.
- [Kleene's theorem](/kleene-theorem/): regular expressions and finite automata describe the same languages.
- [Thompson's construction](/thompson-construction/), the [Glushkov automaton](/glushkov-automaton/) and [regex derivatives](/regex-derivative/): three ways to turn an expression into an automaton.
- [Kleene algebra](/kleene-algebra/): the equational theory of regular expressions.
- [Extended regular expressions](/extended-regular-expressions/) and [star-free expressions](/star-free-expressions/): the syntax with intersection and complement, and its fragment without star.
- [Star height](/star-height-problem/): the nesting depth of stars needed for a language.
- [Regex matching](/regex-matching/) and [regex search](/regex-search/): the two basic problems on an expression and a text.

## References
