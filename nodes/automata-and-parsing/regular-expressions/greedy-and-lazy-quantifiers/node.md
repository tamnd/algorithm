---
tag: WG67P2
kind: concept
slug: greedy-and-lazy-quantifiers
name: Greedy and lazy quantifiers
aliases:
- non-greedy quantifiers
- lazy matching
area: automata-and-parsing/regular-expressions
level: intro
summary: Quantifiers that prefer the longest or the shortest match when several parses are possible.
prereqs: [regular-expression, kleene-star]
see_also: [backtracking-regex-matching, pike-vm, posix-regex-semantics, submatch-extraction, regex-search, redos, extended-regular-expressions, bounded-repetition]
sources:
  - book: isbn:9780596528126
    title: Jeffrey E. F. Friedl, Mastering Regular Expressions, third edition, O'Reilly (2006)
    locator: Chapter 4, The Mechanics of Expression Processing (greedy and lazy quantifiers, backtracking, possessive quantifiers and atomic grouping)
  - url: "https://swtch.com/~rsc/regexp/regexp2.html"
    title: "Russ Cox, Regular Expression Matching: the Virtual Machine Approach (2009)"
    locator: the sections on the backtracking and Pike implementations, and on non-greedy operators as a change of thread priority
  - url: "https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap09.html"
    title: The Open Group, POSIX.1-2024 (IEEE Std 1003.1-2024), Base Definitions, Chapter 9, Regular Expressions
    locator: Section 9.1 (the leftmost-longest rule for matches and subexpressions)
  - paper: doi:10.1007/978-3-319-60134-2_2
    title: Martin Berglund, Brink van der Merwe, Bruce Watson and Nicolaas Weideman, On the semantics of atomic subgroups in practical regular expressions, CIAA 2017, Lecture Notes in Computer Science 10329
    locator: pp. 14 to 26 (atomic subgroups keep the languages regular)
---

A greedy quantifier, such as `*` or `+`, first tries to repeat its operand as many times as it can; a lazy quantifier, such as `*?` or `+?`, first tries as few times as it can. The two kinds differ only when a [regex search](/regex-search/) has several ways to match, and they decide which way a [backtracking](/backtracking-regex-matching/) engine or a [Pike VM](/pike-vm/) reports. For a whole string, a pattern with lazy quantifiers accepts exactly the same strings as the greedy pattern, so the choice changes the reported match and its [submatches](/submatch-extraction/), not the [regular language](/regular-language/).

## In plain words

Suppose a pattern says "a less-than sign, then some characters, then a greater-than sign", and the text is `<a><b>`. Two pieces of text fit: `<a>` and `<a><b>`. The pattern alone does not say which one to report.

A greedy repeat takes as much text as it can and gives back only what the rest of the pattern needs. So it reports the long piece, `<a><b>`.

A lazy repeat takes as little text as it can and takes more only when the rest of the pattern fails. So it reports the short piece, `<a>`.

Both kinds agree on the question "does this whole line fit the pattern?". They differ only in which piece they report and in how they cut that piece into groups.

## The idea

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. Patterns in the syntax of practical engines are in `code font`.

**The quantifiers.** In Perl-style syntax (Perl, PCRE, Python, Java, JavaScript, .NET, RE2):

| greedy | lazy | number of repetitions | language |
|---|---|---|---|
| `E*` | `E*?` | 0 or more | $E^*$ |
| `E+` | `E+?` | 1 or more | $EE^*$ |
| `E?` | `E??` | 0 or 1 | $E \mid \varepsilon$ |
| `E{m,n}` | `E{m,n}?` | from $m$ to $n$ | $E^m (E \mid \varepsilon)^{n-m}$ |
| `E{m,}` | `E{m,}?` | $m$ or more | $E^m E^*$ |

The two columns have the same language. A quantifier is a choice that the engine makes again at each step: repeat $E$ once more, or stop. A greedy quantifier tries "repeat" first and "stop" second. A lazy quantifier tries "stop" first and "repeat" second.

**Priority semantics.** A Perl-style engine orders all ways to match a pattern at a fixed start position. At each choice it prefers the first option: the left side of `|`, and the first option of each quantifier as in the table above. The engine reports the first match in this order, so it is a *leftmost-first* engine, not a leftmost-longest one. A [backtracking](/backtracking-regex-matching/) engine finds this match because it tries the options in this order and stops at the first success. A [Pike VM](/pike-vm/) finds the same match without backtracking: it keeps its threads in priority order, and a lazy quantifier only swaps the order of the two threads that a choice creates (Cox, 2009).

**What does not change.** Swap every greedy quantifier of a pattern for the lazy one, or the other way. Then:

- the set of strings that match the whole pattern does not change, because each quantifier still allows the same numbers of repetitions;
- a search finds a match at the same leftmost start position, because the engine tries each start position in turn and the start position is the first one at which any match exists;
- only the end of the reported match and the substrings that the groups capture can change.

So the greedy and the lazy pattern describe the same regular language, and an automaton that only answers "yes" or "no" treats them as the same pattern.

**POSIX has no lazy quantifiers.** POSIX [extended regular expressions](/extended-regular-expressions/) have only the greedy forms. A POSIX engine reports the leftmost match and, among those, the longest one; then each subexpression takes the longest string it can (POSIX.1-2024, Section 9.1). This rule depends only on the language of each part, and not on the order of the options, so in POSIX `a|ab` and `ab|a` report the same match. See [POSIX regex semantics](/posix-regex-semantics/).

**Possessive quantifiers and atomic groups.** Some engines also have possessive quantifiers `E*+`, `E++`, `E?+` and atomic groups `(?>E)`. A possessive quantifier repeats as often as it can and never gives back a repetition when the rest of the pattern fails. These forms, unlike lazy quantifiers, change the language: `a*+a` matches no string at all, because `a*+` takes every `a` and gives none back to the final `a`. They go beyond the operators of regular expressions, but Berglund, van der Merwe, Watson and Weideman (2017) show that a pattern with atomic groups still describes a regular language.

**Laziness is not a speed fix.** A lazy quantifier changes the order in which a backtracking engine tries options, not the number of options. When no match exists, the engine must try them all in either order. So `^(a+?)+?b` on a long string of letters `a` takes exponential time, the same as `^(a+)+b`. See [ReDoS](/redos/).

## Examples

All results are those of Python's `re` module, which is a leftmost-first backtracking engine.

**Tags.** On the text `<a><b>`:

| pattern | reported match |
|---|---|
| `<.+>` | `<a><b>` |
| `<.+?>` | `<a>` |

The greedy `.+` first reads `a><b>` and then gives back one character, so the final `>` matches the last character. The lazy `.+?` first reads only `a`, and the next `>` matches at once.

**Quoted strings.** On the text `say "hi" and "bye"`, the pattern `"(.*)"` captures `hi" and "bye`, from the first quote to the last one. The pattern `"(.*?)"` captures `hi`. The pattern `"([^"]*)"` also captures `hi`, and it has only one way to match at each start, so it does not depend on the priority rules at all.

**Same start, different end.** On the text `baaa`:

| pattern | span of the match | matched text |
|---|---|---|
| `a+` | from 1 to 4 | `aaa` |
| `a+?` | from 1 to 2 | `a` |

Both matches start at position 1, the first `a`. Only the end moves.

**Splitting the text between groups.** Each row matches the whole string, so each row has the same language as its greedy or lazy partner. Only the captured groups change.

| pattern | text | group 1 | group 2 |
|---|---|---|---|
| `(a*)(a*)` | `aaa` | `aaa` | empty |
| `(a*?)(a*)` | `aaa` | empty | `aaa` |
| `(a+?)(a*)` | `aaa` | `a` | `aa` |
| `(a{2,3})(a*)` | `aaaa` | `aaa` | `a` |
| `(a{2,3}?)(a*)` | `aaaa` | `aa` | `aa` |
| `(.*)(\d+)` | `abc123` | `abc12` | `3` |
| `(.*?)(\d+)` | `abc123` | `abc` | `123` |

The last two rows show a common bug: with a greedy `.*`, the number in group 2 keeps only its last digit.

**Empty matches.** A search for `x*` in `aaxx` returns the empty match at position 0, because `x*` matches the empty string there and position 0 is the leftmost start. A search for `x+` returns `xx` from position 2, and `x+?` returns the single `x` at position 2.

**Alternation is ordered too.** On `abcd`, the pattern `(a|ab)(c|bcd)(d*)` captures `a`, `bcd` and the empty string in Python: the first option `a` of group 1 leads to a match, so the engine never tries `ab`. A POSIX engine prefers the longer `ab` in group 1 and reports `ab`, `c` and `d`.

## Where it is used

- **Data extraction.** Lazy quantifiers find the shortest field between two delimiters, as in the tag and quote examples. A negated class such as `[^"]*` is often a better choice, because its meaning does not depend on priority.
- **Engines.** All Perl-style engines have both kinds, including [backtracking](/backtracking-regex-matching/) engines and automaton engines such as RE2, Go and Rust, which implement priority with a [Pike VM](/pike-vm/). POSIX tools such as [grep](/grep/) have only the greedy forms and use the leftmost-longest rule.
- **Submatch extraction.** The rules on this page are one of the two common answers to the question of which parse to report; the other is [POSIX regex semantics](/posix-regex-semantics/). See [submatch extraction](/submatch-extraction/).
- **Matching speed.** The choice of greedy or lazy does not fix [ReDoS](/redos/). Possessive quantifiers and atomic groups can limit backtracking, at the cost of a different language.

## References
