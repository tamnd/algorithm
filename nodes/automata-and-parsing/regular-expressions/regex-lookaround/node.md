---
tag: X9TSM1
kind: concept
slug: regex-lookaround
name: Lookahead and lookbehind
aliases:
- lookaround assertions
- zero-width assertions
area: automata-and-parsing/regular-expressions
level: advanced
summary: Zero-width assertions that test the text ahead of or behind the current position without consuming it.
prereqs: [regular-expression, regex-search]
see_also: [extended-regular-expressions, backtracking-regex-matching, regex-search, submatch-extraction, backreference, redos, regex-derivative, product-construction]
sources:
  - paper: doi:10.3897/jucs.66330
    title: Martin Berglund, Brink van der Merwe and Steyn van Litsenborgh, Regular expressions with lookahead, Journal of Universal Computer Science 27(4) (2021)
    locator: pp. 324 to 340 (a translation of expressions with lookahead into Boolean automata with at most 3 more states than the length of the expression, so the languages are regular, and the state complexity of the translation to DFAs)
  - paper: doi:10.1145/3632934
    title: Konstantinos Mamouras and Agnishom Chattopadhyay, Efficient matching of regular expressions with lookaround assertions, Proceedings of the ACM on Programming Languages 8(POPL) (2024)
    locator: Article 92, pp. 2761 to 2791 (a formal semantics on positions, NFAs with oracle queries, and matching in time O(m n) by evaluating the assertions bottom-up)
  - url: "https://docs.python.org/3/library/re.html"
    title: Python Software Foundation, re, Regular expression operations, Python 3 documentation
    locator: section Regular Expression Syntax, the entries (?=...), (?!...), (?<=...) and (?<!...) (lookbehind patterns must match strings of fixed length)
  - url: "https://github.com/google/re2/wiki/Syntax"
    title: RE2 regular expression syntax reference
    locator: the entries for (?=re), (?!re), (?<=re) and (?<!re), marked as not supported
---

Lookahead and lookbehind, together called *lookaround*, are assertions in practical regex syntax that check whether the text just after or just before the current position matches a pattern, without consuming any of it. Positive lookahead `(?=r)` succeeds if a match of $r$ starts at the current position, negative lookahead `(?!r)` if none does, and lookbehind `(?<=r)` and `(?<!r)` do the same for a match of $r$ that ends there. Unlike backreferences, lookaround does not leave the regular languages: patterns with lookaround describe only regular languages, but an automaton for them can be much larger, and many engines built on automata do not support it.

## In plain words

Sometimes a pattern should match a piece of text only if it is followed, or preceded, by something else, without including that something in the match. For example: find a word only when a comma comes after it, or a price only when a dollar sign comes before it.

A lookaround is a test that peeks at the text around the current spot and then lets the rest of the pattern go on from that same spot, as if it had not moved. A positive test asks "does this come next?" and a negative one asks "does this not come next?". Tests can look ahead or behind.

Because the tests do not move, several of them can check the same spot, so a single pattern can demand several conditions at once.

## The idea

The core syntax of the [regular expression](/regular-expression/) page has union $\mid$, concatenation, star $^*$, $\varepsilon$ and $\emptyset$. Lookaround adds four forms, written here as in Perl, Python and JavaScript.

**Semantics on positions.** A pattern is matched against a text $T = t_1 \cdots t_n$ with positions $0, \ldots, n$, and denotes a set of pairs $(i, j)$, the matches that start at $i$ and end at $j$. For a core expression these are the pairs with $t_{i+1} \cdots t_j \in L(r)$. A lookaround matches only empty pieces, $i = j$:

- `(?=r)` matches $(i, i)$ if some $(i, j)$ with $j \ge i$ is a match of $r$;
- `(?!r)` matches $(i, i)$ if no such $j$ exists;
- `(?<=r)` matches $(i, i)$ if some $(h, i)$ with $h \le i$ is a match of $r$;
- `(?<!r)` matches $(i, i)$ if no such $h$ exists.

The assertion can see the whole text, not only the part that the enclosing pattern matches: a lookahead may read past the end of the final match, and a lookbehind before its start. This is what makes lookaround useful for searching in context, and it is also why lookaround is defined on positions of a text rather than on strings alone.

**Why the languages stay regular.** Take a pattern $p$ with lookaround and ask which whole strings it matches. At position $i$, a lookbehind `(?<=r)` asks whether the prefix $t_1 \cdots t_i$ is in $\Sigma^* L(r)$, a regular language; a DFA for it can run in parallel with the main automaton, by the [product construction](/product-construction/), and be consulted when the main run passes the assertion. A lookahead `(?=r)` asks whether the suffix $t_{i+1} \cdots t_n$ is in $L(r) \Sigma^*$. An automaton can check this by spawning, at that moment, a second run that must also accept, which is a universal branch of an alternating, or Boolean, automaton; a negative lookahead requires the second run to reject. Boolean automata accept only regular languages, and Berglund, van der Merwe and van Litsenborgh (2021) gave a translation with at most 3 more states than the length of the expression. Nested assertions are handled from the inside out. Converting the Boolean automaton to a DFA can cost far more states, as for complement and intersection in [extended regular expressions](/extended-regular-expressions/).

**Relation to intersection and complement.** For whole-string matching, a lookahead at the start is an intersection: `(?=r)s` matches the strings of $L(s) \cap L(r) \Sigma^*$, and `(?!r)s` those of $L(s) \setminus L(r) \Sigma^*$. So lookaround gives practical syntax for the intersection and complement that the core syntax lacks.

**Matching.** Backtracking engines test an assertion by running a nested backtracking search at the current position, which adds to their worst case ([backtracking regex matching](/backtracking-regex-matching/), [ReDoS](/redos/)). Mamouras and Chattopadhyay (2024) match in time $O(m n)$ for a pattern of size $m$ and a text of length $n$: they evaluate the innermost assertions first, for all positions of the text at once, and then treat each assertion as a precomputed table of truth values that an NFA consults through oracle queries.

**Beyond regular languages.** All of this is for lookaround over the core syntax. With [backreferences](/backreference/) the languages are not regular in general, with or without lookaround, and the automaton methods above do not apply.

## Examples

The answers below are those of Python's `re` module, and a script checked the equivalences on all strings over $\{a, b\}$ of length at most 10 and over $\{a, b, c\}$ of length at most 7.

- **Context without consuming.** `a(?=b)` on the text `ab ac ab` finds $(0, 1)$ and $(6, 7)$: the $a$ before $b$, without the $b$. `(?<=a)b` on `abcb` finds only $(1, 2)$.
- **Several conditions at once.** `(?=.*a)(?=.*b).*` matches, as a whole string, exactly the strings that contain both an $a$ and a $b$, the intersection $\Sigma^* a \Sigma^* \cap \Sigma^* b \Sigma^*$. Password rules such as `^(?=.*[0-9])(?=.*[a-z]).{8,}$` work the same way.
- **Avoiding a substring.** `((?!ab).)*` matches, as a whole string, exactly the strings with no $ab$; over $\{a, b\}$ this is the language of $b^* a^*$. With `abc` in place of `ab`, over $\{a, b, c\}$, the core expression is much less obvious, while the lookaround version stays short.
- **Overlapping matches.** `aa` on `aaaa` finds two matches, since a search resumes after the end of each match. `(?=(aa))` finds three, at positions 0, 1 and 2, because its matches are empty and the group captures the $aa$ that follows each position.
- **Word boundaries.** The anchor `\b` is a lookaround: it holds where a word character and a non-word character meet, that is, `(?<=\w)(?!\w)` or `(?<!\w)(?=\w)`.
- **A restriction.** Python rejects `(?<=a*)b` with the error "look-behind requires fixed-width pattern". Some engines, such as those of JavaScript and .NET, allow lookbehind of any length.

## Where it is used

- **Search and replace in context.** Editors and scripts insert or replace text at positions defined by their surroundings, such as inserting thousands separators with `\B(?=(\d{3})+(?!\d))`.
- **Validation.** Input rules that combine several conditions, such as password rules, are written as one pattern with several lookaheads.
- **Tokenizers.** Lexers use lookahead to decide where a token ends, for example to tell `1..2` from `1.5`.
- **Engine design.** Engines that guarantee linear-time matching, such as RE2, Go's `regexp` and Rust's `regex`, leave lookaround out, while backtracking engines such as PCRE, Java's and Python's support it. Recent algorithms that match lookaround in $O(m n)$ time remove the technical reason for that choice.

## References
