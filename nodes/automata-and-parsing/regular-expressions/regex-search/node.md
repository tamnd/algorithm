---
tag: 4VG1YN
kind: problem
slug: regex-search
name: Regular expression search
aliases:
- regex find
- leftmost match
area: automata-and-parsing/regular-expressions
level: core
summary: Find the occurrences of a regular expression inside a longer text, such as the leftmost match.
prereqs: [regex-matching, regular-expression]
see_also: [thompson-nfa-simulation, pike-vm, lazy-dfa-construction, posix-regex-semantics, submatch-extraction, string-matching, grep, aho-corasick]
sources:
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422 (the start of the automaton added at each character of the text)
  - url: "https://swtch.com/~rsc/regexp/regexp3.html"
    title: Russ Cox, Regular Expression Matching in the Wild, 2010
    locator: Step 4, Match, the parts Find the exact endpoint and Run the DFA backward to find the start (leftmost-first against leftmost-longest, and the reversed expression)
  - url: "https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap09.html"
    title: The Open Group, POSIX.1-2017 Base Definitions, Chapter 9, Regular Expressions
    locator: Section 9.1, Regular Expression Definitions (the match that begins earliest, and of these the longest)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 5, Regular expression matching (search with Thompson's and Glushkov's automata, and with bit-parallel and filtering methods)
---

Regular expression search is the problem of finding substrings of a text that belong to the language of a [regular expression](/regular-expression/): deciding whether one exists, finding the leftmost one, or listing them. It is what `grep`, text editors and the `search` and `find` functions of programming languages do. Unlike [regex matching](/regex-matching/), the expression may match anywhere, and the answer depends on a rule that picks one match among many: leftmost-longest in [POSIX](/posix-regex-semantics/), leftmost-first in Perl-style engines. With automata, all the usual forms take $O(mn)$ time for an expression of size $m$ and a text of length $n$.

## In plain words

You have a long text and a pattern, and you want to know where in the text the pattern occurs. A part of the text matches if the pattern fits it from the first letter of the part to the last.

There can be very many matching parts, and they can overlap, so a search tool must choose which ones to report. The usual choice is the match that starts first. If several matches start at the same place, POSIX tools take the longest one, while tools in the style of Perl take the first one that their order of trying finds.

The automaton method reads the text once and starts a new attempt at every letter, all at the same time. This costs no more than one full-text check.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page (union $\mid$, concatenation, star $^*$, $\varepsilon$, $\emptyset$). Let $r$ have size $m$ and let $T = t_1 \cdots t_n$. A *match* is a pair $(i, j)$ with $0 \le i \le j \le n$ and $t_{i+1} \cdots t_j \in L(r)$; it covers the substring $T[i..j)$, which is empty when $i = j$.

- **Decision.** Is there a match?
- **Earliest end.** The least $j$ such that some $(i, j)$ is a match.
- **Leftmost-longest.** The match $(i, j)$ with the least $i$, and among these the greatest $j$.
- **Leftmost-first.** The match with the least $i$, and among these the one that a backtracking matcher would find first, given an order on the choices of $r$ (left branch of a union first, greedy stars try one more round first).
- **All matches.** The set of all matches, which can have $\Theta(n^2)$ elements, or the list of non-overlapping matches found by repeating a leftmost search after the end of the last match.

## Variants

- **Anchors.** An anchored search requires $i = 0$, or $j = n$, or both; with both it is [regex matching](/regex-matching/). The symbols `^` and `$` of practical syntax ask for these, or for line boundaries.
- **Submatches.** Report also the substrings that the groups of $r$ matched: [submatch extraction](/submatch-extraction/). The rule that picks the match also picks the submatches.
- **Line-oriented search.** [grep](/grep/) asks, for each line, whether it contains a match, which is the decision version per line.
- **Fixed strings.** If $r$ is a string, search is [string matching](/string-matching/); if $r$ is a union of strings, it is [dictionary matching](/dictionary-matching/).
- **Features beyond regular languages.** Backreferences make the language of the pattern non-regular, and search with them is NP-hard ([backreference matching](/backreference-matching/)). [Lookaround](/regex-lookaround/) keeps the language regular but needs extra machinery in automaton engines. Neither is covered by the $O(mn)$ bounds below.

## Examples

**One text, several answers.** Let $T = babbbaabab$, with positions 0 to 10 between the letters, and $r = ab^*a$. The matches are $(1, 6)$ for $abbba$, $(5, 7)$ for $aa$ and $(6, 9)$ for $aba$. The leftmost match, longest or first, is $(1, 6)$. Repeating the search from position 6 gives $(6, 9)$, so a "find all" loop reports $abbba$ and $aba$, which is what Python's `re.finditer` returns; the match $(5, 7)$ overlaps the first one and is skipped.

**Earliest end is not leftmost.** Let $r = ab^*c \mid b$ and $T = abbc$. The matches are $(0, 4)$, $(1, 2)$ and $(2, 3)$. The match that ends first is $(1, 2)$, which a search that stops as soon as it sees an accepting state reports; the leftmost match is $(0, 4)$. Both are correct answers to different questions.

**Longest against first.** Let $r = a \mid ab$ and $T = ab$. The leftmost-longest match is $(0, 2)$. A Perl-style engine tries the left branch $a$ first, succeeds, and reports $(0, 1)$; Python's `re` does the same.

## Known algorithms

- **Restart matching at each position.** Run a matcher anchored at $i$ for each $i$. With Thompson's simulation this costs $O(m n^2)$; with backtracking it is the usual method of Perl-style engines, and it adds a factor of $n$ to their running time, which matters for [ReDoS](/redos/).
- **Thompson's search.** Add the start state of the NFA to the set of active states at every position ([Thompson's NFA simulation](/thompson-nfa-simulation/)). The set after position $j$ holds the states of all runs that started at any $i \le j$, so the first $j$ at which the accepting state is active is the earliest end. Time $O(mn)$, space $O(m)$. Thompson's 1968 program worked this way.
- **Leftmost-longest in two passes.** First find the leftmost start: run the NFA of the reversed expression $r^R$ over $T$ from right to left, adding its start state at every position; the least $i$ at which its accepting state is active is the least start of a match. Then run the NFA of $r$ anchored at $i$ and record the last position where the accepting state is active, stopping when the set of states is empty. Both passes are $O(mn)$. RE2 uses DFAs in two passes in the opposite order: forward for the end of the match, then backward from it to find the start.
- **One pass with start positions.** Keep with each active state the least start position of the runs that reach it. Runs that meet in the same state have the same future, so the least start is enough. This finds the leftmost-longest match in one pass of $O(mn)$ time.
- **Leftmost-first.** The [Pike VM](/pike-vm/) keeps the active states in priority order and drops a thread when a thread of higher priority reaches the same state. It gives the same answer as backtracking in $O(mn)$ time, together with submatches.
- **DFA.** A DFA for $\Sigma^* r$ finds the earliest end in $O(n)$ time after it is built. Building it can take time exponential in $m$, so engines build it lazily ([lazy DFA construction](/lazy-dfa-construction/)).
- **Filtering.** If every match contains a fixed string, search for that string first with a fast [string matching](/string-matching/) method and run the regex engine only near its occurrences. [grep](/grep/) and RE2 use such literal filters; they do not change the worst case.
- **Bit-parallel search.** [Bit-parallel](/bit-parallel-regex-matching/) simulation of the Glushkov automaton represents the set of active states as machine words, which is fast for short patterns.

## Bounds

- **Upper bound.** All forms except "all matches" take $O(mn)$ time and $O(m)$ extra space on the [word RAM](/word-ram/), by the algorithms above; the polylogarithmic speedups of [regex matching](/regex-matching/) apply to the decision version as well.
- **Output size.** Listing every match takes $\Omega(n^2)$ time when there are $\Theta(n^2)$ of them, as for $r = a^*$ and $T = a^n$, which has $(n + 1)(n + 2)/2$ matches including the empty ones.
- **Conditional lower bound.** Search is at least as hard as matching: to match $r$ against $w$, search for $\#r\#$ in $\#w\#$ with a new symbol $\#$; the only possible match is the whole text. So the lower bound of [Backurs and Indyk](/backurs-indyk-regex-hardness/) carries over: under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/), no algorithm runs in time $O((mn)^{1 - \delta})$ for a constant $\delta > 0$. Their paper states its results for both problems.

## Reductions

- **To matching.** A substring of $T$ is in $L(r)$ if and only if $T \in L(\Sigma^* r \Sigma^*)$, so decision search is matching with a slightly larger expression.
- **From matching.** As in the bounds above, with a fresh end marker.
- **Leftmost start to reversed search.** Matches of $r$ in $T$ are matches of $r^R$ in the reversed text, with the positions mirrored. The expression $r^R$ has the same size as $r$ and is built by swapping the operands of each concatenation.

## Applications

- **Search tools and editors.** [grep](/grep/), sed, awk, and the find and replace commands of editors.
- **Programming languages.** The `search`, `find`, `findall` and `replace` functions of regex libraries, with leftmost-first rules in Perl, Python, Java and JavaScript and leftmost-longest rules in POSIX tools.
- **Log and security analysis.** Scanning logs and network streams for signatures, where the text is long and the time per byte must be bounded.
- **Lexical analysis.** A scanner repeats an anchored longest-match search over the remaining input, with the union of all token patterns.

## References
