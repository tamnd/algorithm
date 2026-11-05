---
tag: KJDJBJ
kind: definition
slug: extended-regular-expressions
name: Extended regular expressions
aliases:
- ERE
- POSIX extended regex
- basic regular expressions
- BRE
area: automata-and-parsing/regular-expressions
level: intro
summary: POSIX syntax variants adding operators such as plus, question mark and bounded repetition.
prereqs: [regular-expression, kleene-star]
see_also: [posix-regex-semantics, bounded-repetition, backreference, grep, regex-matching, regex-search, regular-language, star-free-expressions]
sources:
  - url: "https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap09.html"
    title: The Open Group, POSIX.1-2024 (IEEE Std 1003.1-2024), Base Definitions, Chapter 9, Regular Expressions
    locator: Section 9.1 (the leftmost-longest rule), Section 9.3 (BREs, with 9.3.6 for the star, intervals and back-references), Section 9.4 (EREs, with 9.4.6 for the duplication symbols, 9.4.7 for alternation and 9.4.8 for precedence) and Section 9.5 (the grammar)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 3.3.1, Regular Expressions in UNIX (the extra operators and their translation to the basic operators)
  - book: isbn:9780596528126
    title: Jeffrey E. F. Friedl, Mastering Regular Expressions, third edition, O'Reilly (2006)
    locator: Chapter 3, Overview of Regular Expression Features and Flavors (the POSIX flavors and the tools that use them)
---

Extended regular expressions (EREs) and basic regular expressions (BREs) are the two pattern syntaxes that the POSIX standard defines for tools such as [grep](/grep/), `sed`, `awk` and the C functions `regcomp` and `regexec`. Both add operators to the [regular expressions](/regular-expression/) of automata theory: one or more, zero or one, bounded repetition, character classes and anchors. Each of these operators can be written with union, concatenation and [star](/kleene-star/), so EREs describe only [regular languages](/regular-language/). BREs also have backreferences, which describe languages that are not regular.

## Definition

**Notation.** This site writes the regular expressions of theory with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Patterns in POSIX syntax are written in `code font`.

**ERE syntax.** An ERE over a character set $\Sigma$ is built from these forms (POSIX.1-2024, Section 9.4):

| form | name | meaning as a regular expression |
|---|---|---|
| `c` | ordinary character | $c$ |
| `\c` | escaped special character | $c$, for $c$ one of `. [ \ ( ) * + ? { \| ^ $` |
| `.` | period | $c_1 \vert c_2 \vert \cdots \vert c_k$, all characters of $\Sigma$ |
| `[set]`, `[^set]` | bracket expression | the union of the characters in the set, or in its complement in $\Sigma$ |
| `(E)` | grouping | $E$; the group is also a subexpression for match reporting |
| `E*` | star | $E^*$ |
| `E+` | one or more | $E E^*$ |
| `E?` | zero or one | $E \vert \varepsilon$ |
| `E{m}` | exactly $m$ | $E^m$, the concatenation of $m$ copies, with $E^0 = \varepsilon$ |
| `E{m,}` | at least $m$ | $E^m E^*$ |
| `E{m,n}` | from $m$ to $n$ | $E^m (E \vert \varepsilon)^{n-m}$, for $0 \le m \le n$ |
| `E1E2` | concatenation | $E_1 E_2$ |
| `E1\|E2` | alternation | $E_1 \vert E_2$ |
| `^`, `$` | anchors | the start and the end of the string (or of a line) |

The precedence, from high to low, is: bracket expressions and escapes, grouping, the duplication symbols `* + ? {m,n}`, concatenation, anchors, and alternation (Section 9.4.8). So `ab*|c` means $(a(b^*)) \mid c$. In an interval, $m$ and $n$ are decimal numbers with $0 \le m \le n \le$ `RE_DUP_MAX`, a limit of the system that POSIX requires to be at least 255.

**BRE syntax.** A BRE (Section 9.3) has the ordinary characters, `.`, bracket expressions, `*` and the anchors, with these differences:

- grouping is written `\(E\)` and intervals `E\{m,n\}`, so plain `( ) { }` are ordinary characters;
- there is no `+`, `?` or `|`; whether `\+`, `\?` and `\|` are operators is up to the implementation (GNU makes them operators);
- a `*` at the start of the whole BRE, or right after `\(` or an initial `^`, is an ordinary character;
- **back-references** `\1` to `\9` match the same string as the $n$-th earlier subexpression matched (Section 9.3.6). POSIX EREs have no back-references (Section 9.5.1).

**Language.** For a pattern $p$ without back-references, the table defines a regular expression $T(p)$ by induction on $p$, and the language of $p$ is $L(T(p))$. Anchors do not change the set of whole strings that match; in a search they restrict where a match may start or end. For a BRE with back-references, the language is defined by the semantics on the [backreference](/backreference/) page.

**Which match.** When several substrings match, POSIX picks the leftmost one, and among those the longest; then each subexpression, from left to right, matches the longest string it can, consistent with the whole match (Section 9.1). This rule is the subject of [POSIX regex semantics](/posix-regex-semantics/). It does not change the language, only the match and the submatches that a search reports.

## Examples and non-examples

**Translations.** Each line gives an ERE and a regular expression with the same language over $\{a, b, c\}$; for each pair the two languages agree on all strings of length at most 7.

| ERE | regular expression | words of length at most 7 |
|---|---|---|
| `[ab]+c?` | $(a \vert b)(a \vert b)^*(c \vert \varepsilon)$ | 380 |
| `a{2,4}` | $aa(a \vert \varepsilon)(a \vert \varepsilon)$ | 3 |
| `(ab){2,}` | $abab(ab)^*$ | 2 |
| `a?b?` | $(a \vert \varepsilon)(b \vert \varepsilon)$ | 4 |
| `(a\|b){0,2}` | $\varepsilon \vert (a \vert b)(\varepsilon \vert a \vert b)$ | 7 |

**The same pattern in both syntaxes.** The ERE `(ab)+c{2}` is the BRE `\(ab\)\(ab\)*c\{2\}` in strict POSIX, because a BRE has no `+`. In a BRE, the pattern `(ab)+` matches the literal string `(ab)+`.

**Size.** The translation of an interval copies its operand. The ERE `((a{10}){10}){10}` has 1 character and three intervals, and its translation has $10^3 = 1000$ occurrences of $a$. So the size of $T(p)$ can be exponential in the length of $p$; see [bounded repetition](/bounded-repetition/).

**Non-examples.**

- The BRE `\(a*\)b\1` matches $\{a^n b a^n : n \ge 0\}$, which is not regular. It is a valid BRE but has no translation $T$. The ERE `(a*)b\1` is outside the POSIX ERE syntax, although GNU and other libraries accept it as an extension.
- `a**`, `a+*` and `*a` are not valid EREs: POSIX leaves the result of adjacent duplication symbols, and of a duplication symbol at the start of an ERE or after `(`, `|`, `^` or `$`, undefined (Sections 9.4.3 and 9.4.6).
- `a{,3}` is not a POSIX ERE interval; many tools read it as `a{0,3}`, but strict POSIX leaves it undefined.
- Perl-style features such as lazy quantifiers `*?`, lookahead `(?=...)` and `\d` are not part of BREs or EREs. See [greedy and lazy quantifiers](/greedy-and-lazy-quantifiers/) and [lookaround](/regex-lookaround/).

## Related definitions

- **[Regular expression](/regular-expression/).** The core syntax with $\emptyset$, $\varepsilon$, symbols, union, concatenation and star; every ERE is an abbreviation of one.
- **[Kleene star](/kleene-star/).** The operator behind `*`, `+` and the open interval `{m,}`.
- **[Bounded repetition](/bounded-repetition/).** The intervals `{m,n}`, which are short to write but can make the automaton large.
- **[Backreference](/backreference/).** The BRE feature `\n` that leaves the regular languages.
- **[POSIX regex semantics](/posix-regex-semantics/).** The leftmost-longest rule for matches and submatches.
- **Extended regular expressions in theory.** In automata theory, "extended regular expression" often means a regular expression with intersection and complement as extra operators. These also describe only regular languages, because the regular languages are closed under intersection and complement ([closure properties](/closure-properties-of-regular-languages/)). Their fragment without the star is the subject of [star-free expressions](/star-free-expressions/). That meaning is unrelated to the POSIX one.

## References
