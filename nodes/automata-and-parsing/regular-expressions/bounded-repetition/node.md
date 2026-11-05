---
tag: P9T2BN
kind: concept
slug: bounded-repetition
name: Bounded repetition
aliases:
- counted repetition
- counting constraints
area: automata-and-parsing/regular-expressions
level: advanced
summary: The operator x{m,n} for counted repetition, which adds no expressive power but can make automata exponentially larger than the pattern.
prereqs: [regular-expression, kleene-star, subset-construction]
see_also: [extended-regular-expressions, regex-dfa-state-blowup, redos, glushkov-automaton, bit-parallel-regex-matching, lazy-dfa-construction, regex-equivalence, one-unambiguous-regular-expression]
sources:
  - url: "https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap09.html"
    title: The Open Group, POSIX.1-2024 (IEEE Std 1003.1-2024), Base Definitions, Chapter 9, Regular Expressions
    locator: Section 9.3.6 (the BRE interval expression \{m,n\}) and Section 9.4.6 (the ERE interval expression {m,n}, with 0 <= m <= n <= RE_DUP_MAX)
  - url: "https://github.com/google/re2/wiki/Syntax"
    title: RE2 regular expression syntax
    locator: section Repetitions (x{n,m}, x{n,} and x{n}, and the implementation restriction that rejects repetition counts above 1000)
  - url: "https://www.gnu.org/software/grep/manual/grep.html"
    title: GNU grep manual
    locator: Section 6.1, Known Bugs (large repetition counts in the {n,m} construct make grep use lots of memory)
  - url: "https://swtch.com/~rsc/regexp/regexp1.html"
    title: Russ Cox, Regular Expression Matching Can Be Simple And Fast (2007)
    locator: section Performance (the pattern a?^n a^n against the text a^n, exponential for backtracking engines)
  - paper: doi:10.1109/SWAT.1972.29
    title: Albert R. Meyer and Larry J. Stockmeyer, The equivalence problem for regular expressions with squaring requires exponential space, 13th Annual Symposium on Switching and Automata Theory (SWAT 1972)
    locator: pp. 125 to 129
  - paper: doi:10.1145/3428286
    title: Lenka Turoňová, Lukáš Holík, Ondřej Lengál, Olli Saarikivi, Margus Veanes and Tomáš Vojnar, Regex matching with counting-set automata, Proceedings of the ACM on Programming Languages 4(OOPSLA) (2020)
    locator: Article 218 (counting automata, and a determinization into counting-set automata whose size does not depend on the repetition bounds)
  - paper: doi:10.1016/j.ic.2006.12.003
    title: Pekka Kilpeläinen and Rauno Tuhkanen, One-unambiguity of regular expressions with numeric occurrence indicators, Information and Computation 205(6) (2007)
    locator: pp. 890 to 916
---

Bounded repetition is the regex operator $x\{i, j\}$, which matches between $i$ and $j$ consecutive strings of $x$; $x\{i\}$ means exactly $i$ and $x\{i,\}$ means at least $i$. It adds no expressive power, since it is shorthand for $i$ copies of $x$ followed by up to $j - i$ optional copies, but the counts are written in decimal, so a pattern of a few characters can stand for an expression thousands of nodes long. Every automaton built by expansion grows with the counts, and the DFA can grow exponentially with them, so bounded repetition is a common cause of memory blowup in automaton-based engines and of slow matching in [backtracking](/backtracking-regex-matching/) ones.

## In plain words

`a{3}` means `aaa`, and `a{2,4}` means two, three or four `a`. Any pattern with counts can be rewritten without them by writing the copies out, so counts do not let you describe anything new.

The catch is size. The number 1000 takes four characters to write, but `x{1000}` means a thousand copies of `x`. An engine that turns the pattern into an automaton must usually make those thousand copies. Worse, a pattern like "the 20th letter from the end is a" needs a deterministic automaton that remembers the last 20 letters, which is about a million states.

Engines handle this by limiting the counts, by building the automaton lazily, or by using counters instead of copies.

## The idea

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. Practical syntax is in `code font`; $x^i$ is $i$ copies of $x$ concatenated.

**Semantics.** For $0 \le i \le j$,
$$L(x\{i, j\}) = \bigcup_{l = i}^{j} L(x)^l, \qquad L(x\{i\}) = L(x)^i, \qquad L(x\{i,\}) = L(x)^i L(x)^*.$$
POSIX defines the interval expressions `\{m,n\}` in basic and `{m,n}` in extended regular expressions, with $0 \le m \le n \le$ `RE_DUP_MAX`. In practical engines, `x?`, `x+` and `x*` are $x\{0,1\}$, $x\{1,\}$ and $x\{0,\}$.

**Expansion.** Two standard rewrites remove the counts:
$$x\{i, j\} = x^i\, (x \mid \varepsilon)^{j - i} \qquad \text{(flat)}, \qquad x\{i, j\} = x^i\, \big(x\,(x\,( \cdots (x \mid \varepsilon) \cdots ) \mid \varepsilon) \mid \varepsilon\big) \qquad \text{(nested)},$$
where the nested form has $j - i$ levels. Both have $\Theta(j \cdot |x|)$ nodes. The flat form is ambiguous: a string of $l$ copies of $x$ can choose which $l - i$ of the optional factors to use. The nested form is unambiguous when $x$ is, and it is the form to use for backtracking and for parse counting.

**Succinctness.** A pattern with counts written in decimal has length about $|x| + \log_{10} j$, but every expansion has about $j \cdot |x|$ nodes. So:

- the Thompson and [Glushkov](/glushkov-automaton/) automata, and the NFAs of the other standard constructions, can have size exponential in the length of the pattern;
- the minimal DFA can be doubly exponential in it, as the example below shows;
- [equivalence](/regex-equivalence/) of expressions with counts is harder than for plain ones. Meyer and Stockmeyer (1972) showed that equivalence for expressions with squaring, $x^2$, requires exponential space, and $x^2 = x\{2\}$; for plain expressions the problem is [PSPACE-complete](/regex-equivalence-pspace-completeness/). Expanding the counts and then using polynomial space in the expanded size puts the problem in [EXPSPACE](/expspace/).

**Ways around the blowup.**

- **Limits.** RE2 rejects counts above 1000. POSIX allows implementations to stop at `RE_DUP_MAX`.
- **Lazy construction.** A [lazy DFA](/lazy-dfa-construction/) builds only the DFA states that the text reaches, at most one per text symbol, so the doubly exponential DFA is never built in full. The NFA, of size $j \cdot |x|$, still is.
- **Bit vectors.** In [bit-parallel matching](/bit-parallel-regex-matching/), the copies of $x$ become bits of a vector; for a chain of copies such as $a\{n\}$, one shift moves all of them in $O(\lceil n/w \rceil)$ word operations on words of $w$ bits.
- **Counters.** A counting automaton keeps a bounded counter instead of $j$ copies. Determinizing it naively gives back the blowup, because the DFA must track the set of all possible counter values; Turoňová, Holík, Lengál, Saarikivi, Veanes and Vojnar (2020) determinize into *counting-set automata*, which store such sets with constant-time operations, so that the size of the result does not depend on the bounds.
- **Backtracking.** A backtracking engine keeps one counter per active repetition and does not expand at all, but it can take exponential time, as below.

## Examples

**Expansions.** $a\{3\} = aaa$. $(ab)\{2,4\} = abab\,(ab\,(ab \mid \varepsilon) \mid \varepsilon)$ in the nested form, with 19 nodes when each $ab$ is a separate subtree. $a\{2,\} = aaa^*$. $x\{0,0\} = \varepsilon$. `a{1000}` is 7 characters long, and its expansion $a^{1000}$ has 1999 nodes and 1000 positions.

**The $n$-th symbol from the end.** Let $L_n = (a \mid b)^* a (a \mid b)\{n - 1\}$, the strings over $\{a, b\}$ whose $n$-th symbol from the end is $a$. The pattern has length $O(\log n)$, the Glushkov automaton has $2n + 1$ states, and the minimal DFA has exactly $2^n$ states. A DFA must remember the last $n$ symbols: if two strings $u \ne v$ of length $n$ differ at index $t$, with $u_t = a$ and $v_t = b$, then appending $b^{t-1}$ puts $u_t$ and $v_t$ at the $n$-th place from the end, so one of $ub^{t-1}$, $vb^{t-1}$ is in $L_n$ and the other is not. The state counts below were computed by the subset construction and minimization:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Glushkov states | 3 | 5 | 7 | 9 | 11 | 13 | 15 | 17 | 19 | 21 |
| minimal DFA states | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 |

With $n = 20$ the pattern `(a|b)*a(a|b){19}` has 16 characters, and the minimal DFA has $2^{20} = 1{,}048{,}576$ states.

**Ambiguity of the flat form.** For $x\{0,3\}$ written flat as $(x \mid \varepsilon)(x \mid \varepsilon)(x \mid \varepsilon)$, the string $x$ has 3 parse trees and $xx$ has 3, while the nested form has 1 for each. For $x\{0,10\}$ flat, the string $x^5$ has $\binom{10}{5} = 252$ parse trees, against 1 in the nested form.

**Backtracking.** Cox (2007) times the pattern $a?^n a^n$, that is `a{0,1}` repeated $n$ times and then $a^n$, on the text $a^n$. The text matches only if every optional $a$ is skipped, but a backtracking engine tries to take each optional $a$ first, and it can explore about $2^n$ combinations before it finds the match, so the time grows exponentially with $n$; an automaton method stays linear.

**Engines.** RE2 accepts `a{1000}` and rejects `a{1001}`. The GNU grep manual lists large counts in `{n,m}` as a known cause of high memory use.

## Where it is used

- **Validation patterns.** Formats with fixed lengths, such as `[0-9]{4}-[0-9]{2}-[0-9]{2}` for dates, postal codes or hexadecimal identifiers like `[0-9a-f]{32}`, are written with counts.
- **XML Schema.** Content models carry numeric occurrence indicators, `minOccurs` and `maxOccurs`, and the rule that content models must be deterministic has to be extended to counts (Kilpeläinen and Tuhkanen, 2007); see [one-unambiguous regular expressions](/one-unambiguous-regular-expression/).
- **Complexity theory.** Counting, like squaring, makes expressions exponentially more succinct, and it makes the equivalence problem EXPSPACE-hard.
- **Engine design.** Limits on counts, lazy DFAs, bit vectors and counting automata are all responses to the cost of expansion; see [regex DFA state blowup](/regex-dfa-state-blowup/) and [ReDoS](/redos/).

## References
