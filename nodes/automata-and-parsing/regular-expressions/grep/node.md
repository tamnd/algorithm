---
tag: B1JFJE
kind: algorithm
slug: grep
name: grep
area: automata-and-parsing/regular-expressions
level: core
summary: Program that prints lines matching a regular expression, by simulating a nondeterministic finite automaton built from the pattern.
solves: [regex-search]
model: word-ram
complexity:
  vars: {m: the number of nodes of the regular expression, N: the total length of the input lines}
  time: {worst: O(m(N + 1))}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1973
  people: [Ken Thompson, Alfred V. Aho]
  note: grep, a descendant of the editor ed, first appeared in Fourth Edition Unix; Aho's egrep, with a precomputed DFA, appeared in the Seventh Edition in 1979.
prereqs: [regular-expression, thompson-construction, nfa-simulation]
see_also: [regex-search, thompson-nfa-simulation, lazy-dfa-construction, extended-regular-expressions, backreference, boyer-moore, aho-corasick, backtracking-regex-matching]
sources:
  - url: "https://swtch.com/~rsc/regexp/regexp1.html"
    title: Russ Cox, Regular Expression Matching Can Be Simple And Fast (2007)
    locator: section History (ed in First Edition Unix, grep in the Fourth Edition, Aho's egrep in the Seventh Edition, the DFA built on the fly in the Eighth Edition) and section Performance
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422 (search by following all states of the automaton at once, with the start state added at each character)
  - url: "https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html"
    title: The Open Group, POSIX.1-2024 (IEEE Std 1003.1-2024), Shell and Utilities, grep
    locator: sections OPTIONS (-E, -F, -v, -x and the others), DESCRIPTION (a line is selected if a pattern matches any part of it) and RATIONALE (one command in place of grep, egrep and fgrep)
  - url: "https://www.gnu.org/software/grep/manual/grep.html"
    title: GNU grep manual
    locator: Section 5, Performance (automata, Boyer-Moore and Aho-Corasick for fixed strings, and a backtracking matcher for back-references), and Section 3.5, Back-references and Subexpressions
  - book: isbn:9780139376818
    title: Brian W. Kernighan and Rob Pike, The Unix Programming Environment, Prentice Hall (1984)
    locator: Section 1.2 (the name comes from the ed command g/regular-expression/p) and Section 4.1, The grep family
  - url: "https://lists.freebsd.org/pipermail/freebsd-current/2010-August/019310.html"
    title: Mike Haertel, why GNU grep is fast, freebsd-current mailing list (21 August 2010)
    locator: the whole message (Boyer-Moore skipping, no splitting of the input into lines before a match, raw input system calls)
---

grep is the Unix program that reads text line by line and prints each line that contains a match for a [regular expression](/regular-expression/). Its core is [regex search](/regex-search/) by automaton: build an NFA from the pattern with the [Thompson construction](/thompson-construction/), and run an [NFA simulation](/nfa-simulation/) that adds the start state again at each character, so that a match may begin anywhere in the line. This takes $O(mN)$ time for a pattern of $m$ nodes and an input of total length $N$, with no exponential case. Practical versions add a lazy DFA, fast string search for literal parts, and, for the backreferences of POSIX basic regular expressions, a backtracking matcher that goes beyond the regular languages.

## In plain words

You give grep a pattern and some text. It prints each line of the text in which some piece fits the pattern.

The pattern is turned into a small machine with states and arrows labelled by letters. grep reads each line one letter at a time and keeps the set of states that the machine could be in now. Before each letter it also puts the machine's first state in the set, because a match may start at any place in the line.

If the set ever holds the final state, some piece of the line ending here fits the pattern, and grep prints the line and goes to the next one.

The set never has more states than the machine, so the work for each letter is bounded, however the pattern is written.

## The problem

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. Patterns in the syntax of the tools are in `code font`.

The input is a regular expression $r$ with $m$ nodes and a sequence of lines $x^{(1)}, x^{(2)}, \ldots$, each a string without the newline character. A line $x$ is *selected* if some substring of $x$ is in $L(r)$, that is, if $x \in \Sigma^* L(r) \Sigma^*$. The output is the selected lines, in order. With the option `-v` the output is the lines that are not selected, and with `-x` a line is selected only if the whole line is in $L(r)$.

## The algorithm

```pseudo id=main
GREP(r, lines)
L1  N ← THOMPSON(r)                     ▷ start state s, accepting state f
L2  for each line x = x1 ... xℓ do
L3      S ← CLOSE({s})                  ▷ the ε-closure
L4      matched ← (f ∈ S)
L5      i ← 0
L6      while not matched and i < ℓ do
L7          i ← i + 1
L8          T ← {q′ : q ∈ S has a move on x_i to q′} ∪ {s}
L9          S ← CLOSE(T)
L10         matched ← (f ∈ S)
L11     if matched then print x
```

THOMPSON builds an NFA with at most $2m$ states, one start state $s$ and one accepting state $f$, in which each state has either one move on a symbol or at most two $\varepsilon$-moves. CLOSE adds all states that $\varepsilon$-moves reach, with an explicit stack, as on the [NFA simulation](/nfa-simulation/) page. The only change from plain NFA membership is the term $\cup \{s\}$ at line L8, which starts a new run at each position, and the exit from the loop at the first position where a match ends.

## Example

Take $r = ab^*c$ and, to keep the sets short, the NFA with states 0, 1 and 2, start state 0, accepting state 2, and the moves $0 \xrightarrow{a} 1$, $1 \xrightarrow{b} 1$ and $1 \xrightarrow{c} 2$. It has no $\varepsilon$-moves, so CLOSE changes nothing.

| line | sets $S$ after each character | result |
|---|---|---|
| `xabbcx` | start $\{0\}$; `x`: $\{0\}$; `a`: $\{0, 1\}$; `b`: $\{0, 1\}$; `b`: $\{0, 1\}$; `c`: $\{0, 2\}$ | $2 \in S$ after 5 characters: print |
| `abab` | start $\{0\}$; `a`: $\{0, 1\}$; `b`: $\{0, 1\}$; `a`: $\{0, 1\}$; `b`: $\{0, 1\}$ | never 2: skip |
| `ac` | start $\{0\}$; `a`: $\{0, 1\}$; `c`: $\{0, 2\}$ | print |

In the first line, the state 0 that line L8 adds before each character is what lets the run start at the `a` in position 2. The last `x` is never read, because the loop stops at the first match.

**No exponential case.** For the pattern $(a \mid a)^* b$ and a line of 20 letters `a`, a [backtracking](/backtracking-regex-matching/) matcher tries more than a million paths for the first start position alone. The Thompson NFA of this pattern has 12 states, so GREP does at most 12 state steps for each of the 20 characters.

## Correctness

For $0 \le j \le i \le \ell$ let $x[j:i] = x_{j+1} \cdots x_i$, and let $R(v)$ be the set of states in which some run of $N$ on $v$ ends, $\varepsilon$-moves included.

**Invariant.** After $i$ passes of the loop, $S = \bigcup_{j=0}^{i} R(x[j:i])$. For $i = 0$, line L3 gives $S = R(\varepsilon)$. For the step, the moves on $x_i$ from $S$ lead to the states of runs on $x[j:i]$ for $j < i$ that end in a symbol move, the added $s$ starts the run for $j = i$, and CLOSE adds the $\varepsilon$-moves after them, so $S$ becomes the union for $i$. The step is the same as on the [NFA simulation](/nfa-simulation/) page, with one more start state.

**Result.** By the invariant, $f \in S$ after $i$ passes if and only if some substring $x[j:i]$ ending at position $i$ is in $L(N) = L(r)$. The loop stops at the first such $i$ or after the last character, so `matched` is true if and only if some substring of $x$ is in $L(r)$, and line L11 prints exactly the selected lines. The full proof is below.

## Complexity

- **Building the NFA.** THOMPSON makes 2 states for each node of $r$ and at most 2 moves for each state, so it costs $O(m)$ time and space.
- **Each character.** $S$ has at most $2m$ states, each with at most two moves, so lines L8 to L10 cost $O(m)$ with a boolean array for membership. Over all lines this is $O(mN)$, plus $O(m)$ for the start of each line.
- **Space.** The NFA and two sets: $O(m)$ words, independent of the length of the lines. Lines are read one at a time, so the input need not fit in memory.
- **Early exit.** A selected line costs only up to the end of its first match.

## Properties

- **Online.** Each line is read once from left to right, and a line can be printed as soon as its first match ends.
- **Linear in the input.** The bound $O(mN)$ holds for every pattern without backreferences; no pattern makes the time exponential in $N$.
- **Yes or no for each line.** GREP does not need the leftmost or the longest match, only whether one exists. Options such as `-o`, which print the matched part, also need to know where the match starts and ends, which takes more work; see [POSIX regex semantics](/posix-regex-semantics/) for which match is meant.
- **No recursion.** THOMPSON walks the syntax tree with an explicit stack, and CLOSE uses one too.

## Variants and improvements

- **Lazy DFA.** Cache each set $S$ as a DFA state and its successor on each character. Most lines then cost one table lookup per character. This is [lazy DFA construction](/lazy-dfa-construction/), and Cox reports that egrep in Eighth Edition Unix already built its DFA on the fly. Cox also lists GNU grep and GNU `awk` among the programs that build DFAs.
- **Full DFA.** Aho's egrep built the whole DFA first with the [subset construction](/subset-construction/). This is fast for small patterns, but the DFA can have $2^{\Theta(m)}$ states.
- **Fixed strings.** With `-F` the patterns are strings, not expressions. A single string can be found with [Boyer-Moore](/boyer-moore/), which skips over parts of the text, and several strings with [Aho-Corasick](/aho-corasick/). GNU grep uses these algorithms for literal patterns, and Haertel explains that it searches a large buffer for a match before it looks for the line boundaries around it.
- **Bit-parallel simulation.** When the automaton fits in a machine word, the set $S$ is one word, and one step is a few word operations ([bit-parallel regex matching](/bit-parallel-regex-matching/)).
- **Backreferences.** POSIX basic regular expressions, the default syntax of grep, include backreferences `\1` to `\9`, which describe languages that are not regular ([backreference](/backreference/)). No automaton handles them. GNU grep runs a slower backtracking matcher when the pattern has them, and its manual warns that this can take exponential time.
- **Several patterns.** With several `-e` patterns, grep selects a line if any pattern matches it, which is the union of the patterns.

## When to use it

Use the automaton method of grep whenever the question is whether each line contains a match and the pattern is a true regular expression: it is linear in the input, uses memory that depends only on the pattern, and reads input of any size as a stream. For literal strings, a string search algorithm is faster. Patterns with backreferences need a backtracking matcher, with its exponential worst case.

## Pitfalls

- **Forgetting the restart.** Without $\cup \{s\}$ at line L8, the simulation only finds matches that begin at the start of the line, which is the behaviour of `-x` or of a pattern anchored with `^`.
- **Matching the empty string.** If $\varepsilon \in L(r)$, every line is selected, because the empty substring matches. The pattern `a*` selects every line, including empty ones.
- **Syntax differences.** In a basic regular expression, `+`, `?`, `|`, `(` and `{` are ordinary characters, and the operators are written with a backslash, if at all. `grep 'a|b'` searches for the three characters `a|b`; `grep -E 'a|b'` searches for `a` or `b`. See [extended regular expressions](/extended-regular-expressions/).
- **Full DFA blowup.** Building the whole DFA for a pattern such as $(a \mid b)^* a (a \mid b)^{k}$ needs $2^{k+1}$ states; the lazy DFA only builds the states that the input reaches.
- **Backreferences on untrusted input.** One `\1` turns the linear method into backtracking.

## Implementations

## History

Thompson (1968) described regular expression search by following all states of the automaton at once, adding the start state at each character. Cox reports that Thompson did not use this method in the editor `ed` of First Edition Unix (1971), or in its descendant `grep`, which first appeared in the Fourth Edition (1973); both used recursive backtracking. The name comes from the `ed` command `g/re/p`, which prints all lines that match a regular expression (Kernighan and Pike, 1984). Aho's `egrep` in the Seventh Edition (1979) was the first Unix tool with the full regular expression syntax and used a precomputed DFA, and by the Eighth Edition (1985) `egrep` built the DFA on the fly. POSIX later merged `grep`, `egrep` and `fgrep` into one command with the options `-E` and `-F`.

## References
