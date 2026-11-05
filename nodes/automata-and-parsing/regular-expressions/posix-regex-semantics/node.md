---
tag: EKZPJW
kind: definition
slug: posix-regex-semantics
name: POSIX regex semantics
aliases:
- leftmost-longest matching
- POSIX matching rules
area: automata-and-parsing/regular-expressions
level: advanced
summary: The matching rules that choose the leftmost-longest overall match and the subexpression rules.
prereqs: [regular-expression, regex-search]
see_also: [submatch-extraction, greedy-and-lazy-quantifiers, pike-vm, backtracking-regex-matching, regex-search, grep, backreference, regex-ambiguity-detection]
sources:
  - url: "https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap09.html"
    title: The Open Group, POSIX.1-2017 Base Definitions, Chapter 9, Regular Expressions
    locator: Section 9.1, Regular Expression Definitions, the entry on matching (the match that begins earliest, the longest such match, each subpattern from left to right as long as possible, and a null string is longer than no match)
  - url: "https://pubs.opengroup.org/onlinepubs/9699919799/functions/regcomp.html"
    title: The Open Group, POSIX.1-2017 System Interfaces, regcomp, regerror, regexec, regfree
    locator: DESCRIPTION, the numbered rules for pmatch (the last match of a repeated subexpression, -1 for a subexpression that did not participate, and nested subexpressions)
  - url: "https://pkg.go.dev/regexp"
    title: The Go Authors, package regexp, Go standard library documentation
    locator: func CompilePOSIX (leftmost-longest overall matches, and the POSIX rule that maximizes the first subexpression, then the second, which the package does not follow)
  - paper: doi:10.1007/978-3-642-18098-9_25
    title: Satoshi Okui and Taro Suzuki, Disambiguation in regular expression matching via position automata with augmented transitions, CIAA 2010, Lecture Notes in Computer Science 6482
    locator: pp. 231 to 240 (a precise leftmost-longest order on parses and a matcher that follows it)
  - paper: doi:10.1007/978-3-319-43144-4_5
    title: Fahad Ausaf, Roy Dyckhoff and Christian Urban, POSIX lexing with derivatives of regular expressions (proof pearl), Interactive Theorem Proving (ITP 2016), Lecture Notes in Computer Science 9807
    locator: pp. 69 to 86 (an inductive definition of the POSIX value of a string and a machine-checked proof that the derivative algorithm of Sulzmann and Lu computes it)
---

POSIX regex semantics is the rule, fixed by the POSIX standard for the regular expressions of `grep`, `sed`, `awk` and the C function `regexec`, that decides which match a search reports when a pattern matches a text in many ways. The overall match is the *leftmost-longest* one: the match that starts earliest, and among those the longest. Inside that match, each subexpression, from left to right, takes the longest string it can while the overall match stays the same, and this decides what the capture groups report. Perl, Python, Java and JavaScript instead use *leftmost-first* rules, and the two often give different answers.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols, $\varepsilon$, $\emptyset$, union $\mid$, concatenation and star $^*$. Parentheses in a pattern are *capture groups*, numbered by the position of their opening parenthesis, counting from 1. POSIX extended expressions also have $r^+$, $r?$, bounded repetition, bracket expressions and anchors, which expand into this syntax. POSIX basic expressions also have backreferences `\1` to `\9`, which go beyond regular languages ([backreference](/backreference/)); the rules below still choose the match, but matching with them is NP-hard.

Let $T = t_1 \cdots t_n$ be the text, with positions $0, \ldots, n$ between its symbols. A *match* of a pattern $r$ is a pair $(i, j)$ with $t_{i+1} \cdots t_j \in L(r)$.

**Rule 1, the overall match.** Among all matches, choose the one with the least $i$; among those, the one with the greatest $j$. This is the *leftmost-longest* match.

**Rule 2, the subexpressions.** The string $s = t_{i+1} \cdots t_j$ can usually be split among the parts of $r$ in several ways, called *parses*. Consistent with the overall match from Rule 1, each subpattern, from left to right, matches the longest possible string. For this purpose a null string is longer than no match at all. In terms of parses:

- for a concatenation $r_1 r_2 \cdots r_k$, choose the split $s = s_1 s_2 \cdots s_k$ with $s_\ell \in L(r_\ell)$ that makes $s_1$ as long as possible, then $s_2$ as long as possible, and so on;
- for a star $r^*$, choose the iterations from left to right, each as long as possible;
- for a union $r_1 \mid r_2$, both sides would match the same string $s$, so length does not decide; the formal versions choose the left side when it matches $s$.

Then apply the same rules inside each part.

**Rule 3, reporting.** For each group $k$, report the pair of positions of the string it matched in the chosen parse:

- if the group matched several times, as inside a star, report the last of them;
- if it did not take part in the match, report $(-1, -1)$;
- if it is inside another group, its report refers to the part of the text that the outer group reports, so a group that took part only in an earlier iteration of an enclosing star is reported as not taking part.

**Formal versions.** The standard states Rule 2 in one sentence, and the Go documentation calls it "not even well-defined" in general. Okui and Suzuki (2010) defined an order on parses that makes it precise and gave a matcher in polynomial time. Ausaf, Dyckhoff and Urban (2016) defined the POSIX parse of a string by inference rules, along the lines of the list above, and proved in the Isabelle proof assistant that the algorithm of Sulzmann and Lu, based on [derivatives](/regex-derivative/), computes it.

## Examples and non-examples

In the table, a pair $(i, j)$ is a position range and $(-1, -1)$ means "did not take part". The POSIX answers were computed by a script that lists all parses and applies Rules 1 to 3, and the leftmost-first answers are those of Python's `re` module.

| pattern | text | POSIX: match, groups | leftmost-first: match, groups |
|---|---|---|---|
| $a \mid ab$ | $ab$ | $(0, 2)$ | $(0, 1)$ |
| $(a \mid ab)(bc \mid c)$ | $abc$ | $(0, 3)$, $(0, 2)$, $(2, 3)$ | $(0, 3)$, $(0, 1)$, $(1, 3)$ |
| $(a \mid ab)(c \mid bcd)(d^*)$ | $abcd$ | $(0, 4)$, $(0, 2)$, $(2, 3)$, $(3, 4)$ | $(0, 4)$, $(0, 1)$, $(1, 4)$, $(4, 4)$ |
| $((a) \mid b)^*$ | $ab$ | $(0, 2)$, $(1, 2)$, $(-1, -1)$ | $(0, 2)$, $(1, 2)$, $(0, 1)$ |
| $(a^*)(ab)^*(b^*)$ | $abb$ | $(0, 3)$, $(0, 1)$, $(-1, -1)$, $(1, 3)$ | the same |
| $(a \mid b)^*$ | $abba$ | $(0, 4)$, $(3, 4)$ | the same |

- **Row 1.** The overall match differs: leftmost-first tries $a$ first and stops, POSIX prefers the longer $ab$.
- **Row 2.** Both find $abc$, but POSIX gives the first group the longer $ab$, while leftmost-first takes the first alternative $a$ that leads to a match.
- **Row 3.** POSIX maximizes the groups from left to right: the first group can be $ab$, because $cd$ still matches $(c \mid bcd)(d^*)$. Grouping the concatenation as $((a \mid ab)(c \mid bcd))(d^*)$ and maximizing the left part, $abcd$, first would give the first group only $a$; Rule 2 is about the subpatterns in order, not about a binary tree.
- **Row 4.** The star matches twice, $a$ then $b$, so group 1 reports the last iteration $(1, 2)$. Group 2 matched only in the first iteration, and the nested-group rule reports it as absent; Python keeps the old value $(0, 1)$.
- **Row 6.** The last iteration of the star wins: group 1 is the final $a$.
- **The null string.** Matching $(a^*)^*$ against $bc$, the overall match is the empty string at $(0, 0)$, and the standard says that the group matches the null string $(0, 0)$, because a null string is longer than no match. Definitions that forbid empty iterations of a star leave the group unset here, so this corner case is where formal versions and implementations most often disagree with the text of the standard.
- **Not a property of the language.** Two equivalent patterns can report different groups: $(a \mid ab)(bc \mid c)$ and $(ab \mid a)(c \mid bc)$ have the same language, and POSIX gives the same groups for both on $abc$, but leftmost-first gives $(0, 1), (1, 3)$ for the first and $(0, 2), (2, 3)$ for the second. Submatch rules depend on the syntax of the pattern, not only on its language.
- **Not Go's POSIX mode.** Go's `regexp.CompilePOSIX` follows Rule 1 but, as its documentation says, chooses the submatches that a backtracking search would find first among the leftmost-longest matches, not those of Rule 2.

## Related definitions

- **Leftmost-first.** The semantics of Perl and the languages that copied it: the match that a backtracking matcher finds first, trying the left side of a union first and one more iteration of a greedy star first ([backtracking regex matching](/backtracking-regex-matching/), [greedy and lazy quantifiers](/greedy-and-lazy-quantifiers/)). The [Pike VM](/pike-vm/) computes it without backtracking.
- **Leftmost-longest for the match only.** Some engines, such as Go's POSIX mode and DFA-based tools like [grep](/grep/) that report no groups, follow Rule 1 and leave the groups to a different rule or report none.
- **Submatch extraction.** The algorithmic problem of computing the groups under one of these rules, in time close to that of matching ([submatch extraction](/submatch-extraction/)).
- **Ambiguity.** A pattern is ambiguous if some string has more than one parse; Rules 2 and 3 matter only for ambiguous patterns ([regex ambiguity detection](/regex-ambiguity-detection/)).
- **Longest match in lexers.** Lexer generators use the longest match of the union of all token patterns, the "maximal munch" rule, with the earliest listed token winning ties; this is Rule 1 for anchored matches together with a priority rule.

## References
