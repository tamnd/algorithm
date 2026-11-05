---
tag: KR6661
kind: problem
slug: regex-matching
name: Regular expression matching
aliases:
- regex membership
- pattern matching with regular expressions
area: automata-and-parsing/regular-expressions
level: core
summary: Decide whether a given string belongs to the language of a given regular expression.
prereqs: [regular-expression, nondeterministic-finite-automaton]
see_also: [thompson-nfa-simulation, regex-search, thompson-construction, backtracking-regex-matching, redos, backurs-indyk-regex-hardness, submatch-extraction, backreference-matching]
sources:
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 3.7, From Regular Expressions to Automata (simulation of an NFA, its cost, and the time and space trade-off between NFA and DFA)
  - paper: doi:10.1145/128749.128755
    title: Eugene W. Myers, A four Russians algorithm for regular expression pattern matching, Journal of the ACM 39(2) (1992)
    locator: the whole paper (time O(mn / log n))
  - paper: "Philip Bille and Mikkel Thorup, Faster regular expression matching, ICALP 2009, Lecture Notes in Computer Science 5555"
    locator: pp. 171 to 182
  - paper: doi:10.1109/FOCS.2016.56
    title: Arturs Backurs and Piotr Indyk, Which regular expression patterns are hard to match?, FOCS 2016
    locator: pp. 457 to 466 (Section 1, the lower bound for patterns of type concatenation of stars, and Tables 1 and 2)
  - url: "https://swtch.com/~rsc/regexp/regexp1.html"
    title: Russ Cox, Regular Expression Matching Can Be Simple And Fast, 2007
    locator: sections Regular Expression Search Algorithms, Simulating the NFA and Performance
---

Regular expression matching is the problem of deciding, for a [regular expression](/regular-expression/) $r$ and a string $w$, whether $w$ is in the language $L(r)$. The whole string must match; finding a match inside a longer text is [regex search](/regex-search/). The classic solution, [Thompson's NFA simulation](/thompson-nfa-simulation/), takes $O(mn)$ time for an expression of size $m$ and a string of length $n$; faster algorithms gain only polylogarithmic factors, and under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) no algorithm is polynomially faster.

## In plain words

You have a pattern, such as "any mix of the letters a and b, ending in abb", and a word. Does the word fit the pattern, from its first letter to its last?

The pattern can allow many choices: how many times to repeat a part, and which of two options to take. Trying the choices one by one can take a very long time. The good method reads the word once and keeps track of every place in the pattern where you could be after each letter. The number of such places is at most the size of the pattern, so the work is at most the size of the pattern for each letter of the word.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols of a finite alphabet $\Sigma$, the constants $\varepsilon$ and $\emptyset$, union $r \mid s$, concatenation $rs$ and star $r^*$. The size $m$ of $r$ is the number of nodes of its syntax tree.

**Input.** A regular expression $r$ over $\Sigma$ of size $m$ and a string $w \in \Sigma^*$ of length $n$.

**Output.** Yes if $w \in L(r)$, and no otherwise.

The two inputs play different roles, and bounds are stated in both $m$ and $n$. In many uses the pattern is short and fixed, and the text is long; then a bound linear in $n$ matters most.

## Variants

- **Search.** Decide whether some substring of $w$ is in $L(r)$, or find the leftmost or all such substrings. This is [regex search](/regex-search/). It reduces to matching with the expression $\Sigma^* r \Sigma^*$, but direct algorithms are faster in practice.
- **Submatches.** Report, for a match, which substring each parenthesized group of $r$ matched. This needs a rule that picks one parse among many: [submatch extraction](/submatch-extraction/), under [POSIX](/posix-regex-semantics/) or greedy rules.
- **Extended expressions.** With intersection and complement as operators ([extended regular expressions](/extended-regular-expressions/)), the language is still regular, but the automaton can be much larger. Membership stays polynomial: a dynamic program computes, for each subexpression and each substring $w_{i+1} \cdots w_j$, whether the substring matches, in $O(m n^3)$ time, since concatenation and star try every split point.
- **Counting.** Bounded repetition $r\{k\}$ is a short form for $k$ copies of $r$. Expanding it multiplies the size, so a bound in terms of the written pattern needs care ([bounded repetition](/bounded-repetition/)).
- **Backreferences.** A backreference `\1` must repeat the exact substring that group 1 matched. The language is no longer regular in general, and the problem becomes NP-complete ([backreference matching](/backreference-matching/)). No algorithm on this page handles it.
- **Fixed pattern.** If $r$ is fixed, the problem is membership in one [regular language](/regular-language/), solved by a DFA in $O(n)$ time and $O(1)$ space.

## Examples

Let $r = (a \mid b)^* abb$, of size 10. It denotes the strings over $\{a, b\}$ that end in $abb$.

| $w$ | in $L(r)$? |
|---|---|
| $\varepsilon$ | no |
| $abb$ | yes |
| $aabb$ | yes |
| $abab$ | no |
| $ababb$ | yes |
| $abba$ | no |

**With derivatives.** The [Brzozowski derivative](/brzozowski-derivatives/) $D_a(r)$ denotes the strings $u$ with $au \in L(r)$, and $w \in L(r)$ if and only if the derivative by all symbols of $w$, in order, contains $\varepsilon$. Write $S = (a \mid b)^*$. For $w = abb$:

- $D_a(S\,abb) = S\,abb \mid bb$, since $D_a(S) = S$ and $S$ contains $\varepsilon$, so the $a$ can also start $abb$.
- $D_b(S\,abb \mid bb) = S\,abb \mid b$.
- $D_b(S\,abb \mid b) = S\,abb \mid \varepsilon$.

The last expression contains $\varepsilon$, so $abb \in L(r)$.

**A hard case for backtracking.** For $r_k = (a \mid \varepsilon)^k a^k$ and $w = a^k$, the match exists, but a greedy [backtracking matcher](/backtracking-regex-matching/) tries about $2^k$ ways to use the optional parts before it finds it. The language of $r_3$ is $\{aaa, aaaa, aaaaa, aaaaaa\}$. Thompson's simulation needs $O(k^2)$ steps on $r_k$; see [ReDoS](/redos/) for measurements.

## Known algorithms

| algorithm | time | extra space | notes |
|---|---|---|---|
| [Backtracking](/backtracking-regex-matching/) | exponential in the worst case | $O(m + n)$ | supports backreferences and lookaround; open to [ReDoS](/redos/) |
| [Thompson's NFA simulation](/thompson-nfa-simulation/) | $O(mn)$ | $O(m)$ | builds the [Thompson NFA](/thompson-construction/) and keeps the set of active states |
| [Pike VM](/pike-vm/) | $O(mn)$ | $O(m)$ times the number of groups | the simulation with submatch positions per thread |
| DFA by [subset construction](/subset-construction/) | $2^{O(m)} \lvert\Sigma\rvert + O(n)$ | $2^{O(m)}$ | fast when the DFA is small; can be exponential ([state blowup](/regex-dfa-state-blowup/)) |
| [Lazy DFA](/lazy-dfa-construction/) | $O(mn)$ worst case, often $O(n)$ | a bounded cache | used by RE2 and grep |
| [Brzozowski derivatives](/brzozowski-derivatives/) | depends on simplification | | builds a DFA from the expression itself |
| [Bit-parallel simulation](/bit-parallel-regex-matching/) | $O(n \lceil m / W \rceil)$ | tables of size exponential in the block length | $W$ is the machine word length; fast for short patterns |
| Myers (1992) | $O(mn / \log n)$ | | four Russians tables on blocks of the NFA |
| Bille and Thorup (2009) | roughly $O(mn / \log^{1.5} n)$ | | the fastest known in general |

All of them except backtracking use only the finite state set of an automaton, and none of them supports backreferences.

## Bounds

- **Upper bound.** $O(mn)$ time and $O(m)$ extra space on the [word RAM](/word-ram/), by Thompson's method. Algorithms that use word-level parallelism and table lookup gain a factor of $\log n$ (Myers) and about $\log^{1.5} n$ (Bille and Thorup).
- **Trivial lower bound.** $\Omega(m + n)$, since in general every symbol of the pattern and the text must be read.
- **Conditional lower bound.** Backurs and Indyk (2016) proved that, if the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) holds, no algorithm decides matching or membership in time $O((mn)^{1 - \delta})$ for any constant $\delta > 0$, already for patterns that are concatenations of stars and symbols, with $m \le n$. So the gap between $mn$ and the best algorithms is at most polylogarithmic unless the hypothesis fails. See [Backurs and Indyk](/backurs-indyk-regex-hardness/).
- **Space.** A text read once from left to right needs only the set of active states, $O(m)$ words; for a fixed pattern this is $O(1)$.

## Reductions

- **To NFA acceptance.** [Thompson's construction](/thompson-construction/) turns $r$ into an NFA with at most $2m$ states and $4m$ moves in $O(m)$ time, so any algorithm for NFA acceptance with $s$ states and $t$ moves in time $O(tn)$ gives $O(mn)$ for matching. The [Glushkov automaton](/glushkov-automaton/) has no $\varepsilon$-moves and $m' + 1$ states, where $m'$ is the number of symbol occurrences, but up to quadratically many moves.
- **From search.** Search for $r$ in $w$ reduces to matching $\Sigma^* r \Sigma^*$ against $w$, and the expression grows by $O(\lvert\Sigma\rvert)$.
- **From orthogonal vectors.** The lower bound of Backurs and Indyk reduces [orthogonal vectors](/orthogonal-vectors-hypothesis/) to matching: each vector becomes a gadget in the pattern or the text, and a match exists exactly when two vectors are orthogonal.
- **From string matching.** If $r$ is a single string, matching is equality and search is [string matching](/string-matching/), solved in linear time; a union of strings gives [dictionary matching](/dictionary-matching/), solved by [Aho-Corasick](/aho-corasick/).

## Applications

- **Text search tools.** [grep](/grep/), sed, awk and editors match patterns against lines of text, and search is matching with an implicit $\Sigma^*$ on both sides.
- **Input validation.** Programs check that a field is a date, an e-mail address or an identifier by a full match. Validation with untrusted input is where [ReDoS](/redos/) happens, which favors the $O(mn)$ methods.
- **Lexical analysis.** A scanner matches the longest prefix of the input against the union of the token patterns, with a DFA built once ahead of time.
- **Bioinformatics and networks.** Protein motifs (PROSITE patterns) and intrusion detection signatures are regular expressions matched against long sequences or packet streams.

## References
