---
tag: 941H86
kind: problem
slug: submatch-extraction
name: Submatch extraction
aliases:
- capture group extraction
area: automata-and-parsing/regular-expressions
level: advanced
summary: Report the substrings matched by each capture group while still matching the whole pattern.
prereqs: [regex-search, posix-regex-semantics]
see_also: [pike-vm, backtracking-regex-matching, one-pass-regex-matching, posix-regex-semantics, greedy-and-lazy-quantifiers, regex-ambiguity-detection, backreference-matching, thompson-nfa-simulation]
sources:
  - url: "https://swtch.com/~rsc/regexp/regexp2.html"
    title: Russ Cox, Regular Expression Matching, the Virtual Machine Approach, 2009
    locator: sections Pike's Implementation and Submatching (threads that carry their capture positions, in priority order)
  - url: "https://swtch.com/~rsc/regexp/regexp3.html"
    title: Russ Cox, Regular Expression Matching in the Wild, 2010
    locator: Step 4, Match (find the overall match with DFAs first, then run a submatch engine on the matched text only)
  - paper: doi:10.1109/SPIRE.2000.878194
    title: Ville Laurikari, NFAs with tagged transitions, their conversion to deterministic automata and application to regular expressions, SPIRE 2000
    locator: pp. 181 to 187 (tags on the moves of an NFA that record positions, and their conversion to deterministic automata)
  - paper: "Alain Frisch and Luca Cardelli, Greedy regular expression matching, ICALP 2004, Lecture Notes in Computer Science 3142"
    locator: pp. 618 to 629 (the greedy parse tree in time linear in the text for a fixed expression, by a backward pass and a forward pass)
  - paper: doi:10.1007/978-3-642-18098-9_25
    title: Satoshi Okui and Taro Suzuki, Disambiguation in regular expression matching via position automata with augmented transitions, CIAA 2010, Lecture Notes in Computer Science 6482
    locator: pp. 231 to 240 (POSIX submatches in polynomial time with position automata)
  - url: "https://pubs.opengroup.org/onlinepubs/9699919799/functions/regcomp.html"
    title: The Open Group, POSIX.1-2017 System Interfaces, regcomp, regerror, regexec, regfree
    locator: DESCRIPTION, the numbered rules for pmatch
---

Submatch extraction is the problem of reporting, along with a match of a [regular expression](/regular-expression/), the substring that each of its capture groups matched. It is what a program needs to take a date, a key and a value, or the parts of a log line out of a text. The language of the pattern does not determine the answer: a string can be matched in many ways, and a *disambiguation policy*, leftmost-first as in Perl or leftmost-longest as in [POSIX](/posix-regex-semantics/), picks one. Automaton methods solve it in time $O(m n k)$ for a pattern of size $m$ with $k$ groups and a text of length $n$, without the exponential worst case of backtracking.

## In plain words

A pattern with groups is a pattern with labelled parts. When it matches, you want to know which piece of the text each labelled part covered.

Often the text can be cut into pieces in several ways that all fit. With the pattern "a or ab, then bc or c" and the text "abc", the first part can cover "a" or "ab". So every tool fixes a rule for choosing: try the options in the order they are written, or make the earlier parts as long as possible.

A backtracking matcher answers by trying cuts one at a time, which can take very long. Faster methods run all the attempts side by side and let each one carry a note of where its groups started and ended.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols, $\varepsilon$, $\emptyset$, union $\mid$, concatenation and star $^*$. Some subexpressions are marked as capture groups $1, \ldots, k$, by parentheses numbered in the order of their opening parenthesis. A *parse* of a string $s \in L(r)$ is a derivation of $s$ from the syntax tree of $r$: which side of each union is used, how $s$ is split at each concatenation, and how many iterations each star makes and what each covers.

**Input.** A pattern $r$ of size $m$ with $k$ groups, a text $T$ of length $n$, and a disambiguation policy.

**Output.** The match $(i, j)$ chosen by the policy, and for each group $g$ the pair of positions $(i_g, j_g)$ of the substring that it matched in the chosen parse, or $(-1, -1)$ if it did not take part. When a group matched several times inside a star, the last match is reported.

**Policies.**

- **Leftmost-first.** The parse that a [backtracking matcher](/backtracking-regex-matching/) finds first: the left side of a union before the right, one more iteration of a greedy star before stopping, and the reverse for a lazy star ([greedy and lazy quantifiers](/greedy-and-lazy-quantifiers/)). Used by Perl, Python, Java, JavaScript, .NET, RE2, Go and Rust.
- **Leftmost-longest, POSIX.** The longest of the leftmost matches, and then each subpattern from left to right as long as possible ([POSIX regex semantics](/posix-regex-semantics/)). Used by POSIX `regexec`.

## Variants

- **Anchored or not.** With the match required to cover the whole text, only the parse is to be chosen; in a search, the policy also chooses the match ([regex search](/regex-search/)).
- **Full parse trees.** Report every iteration of every star, not only the last one. The output can have size $\Theta(n)$ even with one group, as for $(a)^*$ on $a^n$. This is *regex parsing*, and Frisch and Cardelli (2004) compute the leftmost-first parse tree in time linear in $n$ for a fixed pattern.
- **All matches with groups.** Repeat the search after the end of each match, as `findall` does.
- **Backreferences.** If the pattern refers back to a group, as in `(a|b)*\1`, the groups must be known during the match, not only after it. The language is then not regular in general, and matching becomes NP-hard ([backreference matching](/backreference-matching/)); automaton methods do not apply.
- **Lookaround.** [Lookahead and lookbehind](/regex-lookaround/) assertions do not consume text and keep the language regular, but they change which parses are valid and need extra machinery in automaton engines.

## Examples

The leftmost-first answers are those of Python's `re` module. The POSIX answers were computed by a script that lists all parses and applies the POSIX rules.

| pattern | text | leftmost-first groups | POSIX groups |
|---|---|---|---|
| $(a \mid ab)(bc \mid c)$ | $abc$ | $(0, 1)$, $(1, 3)$ | $(0, 2)$, $(2, 3)$ |
| $(a \mid ab)(c \mid bcd)(d^*)$ | $abcd$ | $(0, 1)$, $(1, 4)$, $(4, 4)$ | $(0, 2)$, $(2, 3)$, $(3, 4)$ |
| $((a) \mid b)^*$ | $ab$ | $(1, 2)$, $(0, 1)$ | $(1, 2)$, $(-1, -1)$ |
| $(a^*)(ab)^*(b^*)$ | $abb$ | $(0, 1)$, $(-1, -1)$, $(1, 3)$ | the same |
| $(x^*)(x^*)$ | $xx$ | $(0, 2)$, $(2, 2)$ | the same |

In every row the overall match is the whole text. The first two rows differ because leftmost-first takes the first alternative $a$ that leads to some match, while POSIX makes the first group as long as it can. The third row differs in the reporting rule: group 2 matched only in the first iteration of the star, and POSIX reports it as absent because the enclosing group 1 reports the second iteration. The last row shows that both policies let the first star take everything and leave the empty string to the second.

## Known algorithms

| method | policy | time | space |
|---|---|---|---|
| [Backtracking](/backtracking-regex-matching/) | leftmost-first | exponential in $n$ in the worst case | a stack of choice points |
| [Pike VM](/pike-vm/) | leftmost-first | $O(m n k)$ | $O(m k)$ |
| [One-pass matching](/one-pass-regex-matching/) | leftmost-first, one-pass patterns only | $O(n k)$ after a precomputation | $O(m k)$ |
| Two-pass parsing, Frisch and Cardelli | leftmost-first, full parse tree | $O(m n)$ | $O(m n)$ |
| Tagged NFAs, Laurikari | positions by tags | $O(m n k)$ | $O(m k)$ |
| Okui and Suzuki | POSIX | polynomial | polynomial |

- **Backtracking.** Try the choices of the parse in priority order and record group positions on the way; the first complete parse is the leftmost-first one. Simple and supports every feature, but it can take time exponential in $n$ on patterns like $(a^*)^* b$ ([ReDoS](/redos/)).
- **Pike VM.** Run [Thompson's simulation](/thompson-nfa-simulation/) on a program for the pattern, with each thread carrying an array of $2k$ positions that it updates when it passes a group boundary. Keep the threads in priority order and, when two threads reach the same state, keep only the one with higher priority: both have the same future, so the lower one can never be preferred. At most $m$ threads are alive, and copying an array costs $O(k)$, which gives $O(m n k)$ time. Pike wrote this method for the sam editor; Cox (2009) describes it.
- **Find the match first.** Many engines first find the overall match with a fast [lazy DFA](/lazy-dfa-construction/), which has no groups, and then run the Pike VM, a one-pass matcher or backtracking on the matched substring only (Cox, 2010). The worst case is unchanged, but most texts are scanned at DFA speed.
- **One-pass patterns.** If at each position of every match there is only one way to continue, no thread can be lost and a single thread suffices, as in RE2's one-pass matcher.
- **Tags.** Laurikari (2000) puts *tags* on the moves of an NFA that record the current position into a register, and converts the tagged NFA to a deterministic automaton with register operations. The TRE library used this for POSIX matching, and the lexer generator re2c uses its descendants.
- **Parsing in two passes.** Run the automaton backward over the text to record which states can still reach the end, then go forward choosing at each step the first choice of highest priority that can still lead to a match. This yields the whole parse tree (Frisch and Cardelli, 2004).
- **POSIX.** The rule that maximizes subpatterns from left to right is not a priority order on the moves of an NFA, so the Pike VM does not apply directly. Okui and Suzuki (2010) keep with each thread enough information about the positions it has passed to compare threads in the POSIX order, and obtain a polynomial algorithm.

## Bounds

- **Lower bound.** Submatch extraction includes [regex matching](/regex-matching/): a pattern matches a text if and only if the extraction does not report "no match". So, under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/), no algorithm runs in time $O((m n)^{1 - \delta})$ for a constant $\delta > 0$ ([Backurs and Indyk](/backurs-indyk-regex-hardness/)).
- **Upper bound.** $O(m n k)$ time and $O(m k)$ space for leftmost-first by the Pike VM, which is within a factor $k$ of matching.
- **Output.** $\Theta(k)$ for the last match of each group, and up to $\Theta(n)$ for full parse trees.
- **Backtracking.** Exponential in $n$ in the worst case, although the same answers can be computed in polynomial time.

## Reductions

- **From matching.** As in the lower bound.
- **To matching for the overall match.** The overall leftmost-longest match is found by matching alone, with automata for $r$ and its reverse ([regex search](/regex-search/)); only the groups need more.
- **To parsing.** The last match of each group can be read off a full parse tree, so regex parsing solves submatch extraction, with output of size up to $n$.

## Applications

- **Extracting fields.** Dates, numbers, keys and values from configuration files, logs and network protocols, with `match.group(1)` in Python or `$1` in Perl.
- **Search and replace.** Replacement strings refer to groups, as in `s/(\w+) (\w+)/\2 \1/`.
- **Lexers and tokenizers.** Tagged automata let a lexer generator report the parts of a token without a second pass.
- **Routing and validation.** Web frameworks match URLs against patterns with groups for the parameters, such as the identifier in a path.

## References
