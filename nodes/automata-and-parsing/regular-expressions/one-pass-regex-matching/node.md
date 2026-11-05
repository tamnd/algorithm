---
tag: KX64F8
kind: algorithm
slug: one-pass-regex-matching
name: One-pass regex matching
aliases:
- one-pass DFA matching
- RE2 one-pass matcher
area: automata-and-parsing/regular-expressions
level: advanced
summary: Matches a one-unambiguous regex in linear time with a deterministic one-pass automaton.
solves: [regex-matching]
model: word-ram
complexity:
  vars: {m: the number of nodes of the regular expression, k: the number of symbol occurrences in the expression, n: the length of the word}
  time: {worst: O(m k^2 + n)}
  space: {extra: O(m k + n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 2010
  people: [Russ Cox]
  note: Cox described the one-pass engine of RE2, which runs with a single set of submatch positions; the expressions with a deterministic position automaton had been characterized by Brüggemann-Klein and Wood in 1998.
prereqs: [glushkov-automaton, deterministic-finite-automaton]
see_also: [one-unambiguous-regular-expression, pike-vm, nfa-simulation, lazy-dfa-construction, backtracking-regex-matching, submatch-extraction, ll1-parsing, regex-to-nfa-conversion]
sources:
  - url: "https://swtch.com/~rsc/regexp/regexp3.html"
    title: Russ Cox, Regular Expression Matching in the Wild (2010)
    locator: section Step 4, Match, subsection on submatches (the definition of a one-pass regular expression, the examples x*yx*, x*x, x(y|z) and (xy|xz), and the engine that never copies the submatch boundary set) and section Performance (RE2 uses the OnePass engine for ([0-9]+)-([0-9]+)-([0-9]+))
  - paper: doi:10.1006/inco.1997.2695
    title: Anne Brüggemann-Klein and Derick Wood, One-unambiguous regular languages, Information and Computation 142(2) (1998)
    locator: pp. 182 to 206 (the definition of one-unambiguous expressions, their characterization by a deterministic Glushkov automaton, and the existence of regular languages with no one-unambiguous expression)
  - paper: doi:10.1016/0304-3975(93)90287-4
    title: Anne Brüggemann-Klein, Regular expressions into finite automata, Theoretical Computer Science 120(2) (1993)
    locator: pp. 197 to 213 (star normal form, and the construction of the Glushkov automaton in linear time for deterministic expressions)
  - paper: doi:10.1070/RM1961v016n05ABEH004112
    title: Victor M. Glushkov, The abstract theory of automata, Russian Mathematical Surveys 16(5) (1961)
    locator: pp. 1 to 53
---

One-pass regex matching decides whether a word is in the language of a [regular expression](/regular-expression/) by following a single state, with no copies and no backtracking, when the expression allows it. The test is made once, when the expression is compiled: the [Glushkov automaton](/glushkov-automaton/) must be deterministic after its useless states are removed, which is the condition that the expression is [one-unambiguous](/one-unambiguous-regular-expression/). If the test passes, the matcher reads the word once, makes one table lookup per symbol, and also tells which occurrence of a symbol in the expression matched each symbol of the word, so a matcher can record submatch positions with one set of registers.

## In plain words

Some patterns never make you guess. In "any number of a, then b, then any number of a", each letter of the input tells you exactly which letter of the pattern it matches: an a before the b belongs to the first part, the b is the b, and an a after it belongs to the last part. Other patterns make you guess. In "any number of a, then a", an a can be part of the repetition or the last letter, and you only find out at the end.

The one-pass matcher checks the pattern before it reads any text. If no guess is ever needed, it builds a table that says, for each place in the pattern and each next letter, the one place to go. Then it reads the text once, from left to right.

## The problem

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union.

Number the occurrences of symbols in $r$ from left to right as positions $1, \dots, k$, and write $\mathrm{sym}(p)$ for the symbol at position $p$. The marked expression $r'$ is $r$ with each occurrence replaced by its position, so its words are sequences of positions. A word $w$ is in $L(r)$ exactly when some sequence in $L(r')$ has the symbols $w$.

The input is $r$ and a word $w = a_1 \cdots a_n$. The output is "not one-pass" if $r$ is not one-unambiguous. Otherwise it is the answer to $w \in L(r)$, and, when the answer is yes, the sequence of positions $p_1 \cdots p_n \in L(r')$ that spells $w$. For a one-unambiguous expression this sequence is unique.

Brüggemann-Klein and Wood call $r$ one-unambiguous when, for any two sequences $u p v$ and $u q v'$ in $L(r')$ with $\mathrm{sym}(p) = \mathrm{sym}(q)$, we have $p = q$. In words: after any prefix, the next symbol of the word fixes the next position.

## The algorithm

The Glushkov sets of $r$ are $\mathrm{First}$, the positions that can start a sequence of $L(r')$, $\mathrm{Last}$, the positions that can end one, and $\mathrm{Follow}(p)$, the positions that can come right after $p$. Position $0$ is the start state, with $\mathrm{Follow}(0) = \mathrm{First}$. A position is useful when it is reachable from $0$ along $\mathrm{Follow}$ and can reach a final position. Only useful positions count: an occurrence under $\emptyset$, as in $a\emptyset \mid a$, never takes part in a match.

```pseudo id=main
ONE-PASS-COMPILE(r)
L1  compute sym, Follow and Nullable of r, with Follow(0) ← First(r)
L2  F ← Last(r), and also 0 if Nullable(r)
L3  U ← the positions reachable from 0 that can reach F
L4  for each p ∈ U ∪ {0} do
L5      T[p] ← an empty map from symbols to positions
L6      for each q ∈ Follow(p) ∩ U do
L7          if sym(q) is a key of T[p] then return NOT-ONE-PASS
L8          T[p][sym(q)] ← q
L9  return (T, F)

ONE-PASS-MATCH(T, F, w)
L10 p ← 0; P ← an empty list
L11 for each symbol a of w do
L12     if a is not a key of T[p] then return reject
L13     p ← T[p][a]; append p to P
L14 if p ∈ F then return (accept, P) else return reject
```

Line L1 is the [Glushkov construction](/glushkov-automaton/). Line L3 trims the automaton with two graph searches, one forward from $0$ and one backward from $F$. Lines L4 to L8 fill a table with at most one entry for each pair of a position and a symbol, and give up at line L7 when a position has two useful successors with the same symbol. The matcher at lines L10 to L14 is a run of the resulting [deterministic automaton](/deterministic-finite-automaton/).

## Example

Take $r = a^* b a^*$, Cox's $x^*yx^*$ over the alphabet $\{a, b\}$. The positions are $a_1$, $b_2$ and $a_3$.

| set | value |
|---|---|
| $\mathrm{Follow}(0) = \mathrm{First}$ | $\{1, 2\}$ |
| $\mathrm{Follow}(1)$ | $\{1, 2\}$ |
| $\mathrm{Follow}(2)$ | $\{3\}$ |
| $\mathrm{Follow}(3)$ | $\{3\}$ |
| $F = \mathrm{Last}$ | $\{2, 3\}$ |

All four states are useful. The rows of the table are $T[0] = T[1] = \{a \mapsto 1, b \mapsto 2\}$ and $T[2] = T[3] = \{a \mapsto 3\}$. No row has a clash, so $r$ is one-pass.

On $w = aaba$ the matcher visits $0, 1, 1, 2, 3$. The last state $3$ is in $F$, so it accepts with $P = 1\,1\,2\,3$: the first two a's match the first $a^*$, and the last a matches the second one. On $abab$ it visits $0, 1, 2, 3$ and then finds no entry for $b$ in $T[3]$, so it rejects after reading four symbols.

Now take $r = a^* a$, Cox's $x^*x$. Here $\mathrm{Follow}(0) = \{1, 2\}$ and both positions carry $a$, so line L7 returns "not one-pass". The expression $a a^*$ denotes the same language and is one-pass: its table is $T[0] = \{a \mapsto 1\}$ and $T[1] = T[2] = \{a \mapsto 2\}$. In the same way $a(b \mid c)$ is one-pass and $ab \mid ac$ is not.

Finally, $a\emptyset \mid a$ has positions $a_1$ and $a_2$, both in $\mathrm{First}$. Position $1$ cannot reach $F = \{2\}$, so line L3 drops it, and the table is $T[0] = \{a \mapsto 2\}$. Without the trim, line L7 would reject an expression that is one-unambiguous.

## Correctness

The matcher keeps one position, and the table gives each pair of a position and a symbol at most one next position. By the Glushkov theorem, a sequence of positions is in $L(r')$ exactly when it starts in $\mathrm{First}$, each step follows $\mathrm{Follow}$, and it ends in $\mathrm{Last}$. Every position on such a sequence is useful, so every sequence that spells a word of $L(r)$ is a path in the table, and there is only one such path, the one the matcher takes. The trim also makes the compile test exact: a clash between two useful positions extends to two sequences of $L(r')$ that violate the definition of one-unambiguity. The full proof is below.

## Complexity

The Glushkov sets take $O(m k^2)$ time with plain sets, as on the [Glushkov automaton](/glushkov-automaton/) page, since each concatenation or star joins at most $k$ sets of size at most $k$. The two searches at line L3 and the loops at lines L4 to L8 visit each pair $(p, q)$ with $q \in \mathrm{Follow}(p)$ once, which is $O(k^2)$. So compiling costs $O(m k^2)$ time and $O(m k)$ space for the stack of sets.

Matching costs one table lookup per symbol. With each row stored as an array indexed by the symbol, a lookup takes constant time, so a word of length $n$ costs $O(n)$ time; a hash map gives the same bound in expectation. The matcher keeps one position, plus the $n$ entries of $P$ when the caller asks for them.

## Properties

- The matcher is deterministic and online: it reads each symbol once, never moves back, and can stop at the first symbol with no table entry.
- The output $P$ is the unique parse of $w$ at the level of positions. Because positions are numbered from left to right, the positions under one subexpression form an interval, so $P$ tells which part of $r$ matched each symbol. This is what lets RE2 record submatches with one set of registers.
- The check is exact for the language of positions, not for the language of words: $a^* a$ fails and $a a^*$ passes, though they denote the same language. Brüggemann-Klein and Wood also show that some regular languages have no one-unambiguous expression at all.

## Variants and improvements

- **RE2's one-pass engine.** Cox describes an engine that analyses the compiled program of RE2, with empty-width instructions and capture slots, rather than the positions of the expression. For each instruction and input byte it records the single action to take, including which capture slots to set, and falls back on another engine when the analysis fails.
- **Linear-time compilation.** Brüggemann-Klein (1993) builds the Glushkov automaton of an expression in star normal form, and shows that for deterministic expressions the construction runs in linear time in the size of the expression.
- **Other fallbacks.** When the test fails, a matcher can use the [Pike VM](/pike-vm/) for submatches, [NFA simulation](/nfa-simulation/) or a [lazy DFA](/lazy-dfa-construction/) for a yes or no answer, or a bounded [backtracking matcher](/backtracking-regex-matching/) for small inputs, as RE2 does.

## When to use it

Use it when submatch positions are needed and the expression is of a form such as $(d^+)\text{-}(d^+)$, where each symbol fixes its role: it is the cheapest way to get them in linear time. It is also the natural matcher for content models that must be deterministic by design. For a yes or no answer with no submatches, a DFA gives the same speed for every expression, one-pass or not.

## Pitfalls

- Checking determinism on the untrimmed Glushkov automaton rejects one-unambiguous expressions that contain $\emptyset$, such as $a\emptyset \mid a$, and expressions whose clashing positions are unreachable, such as $b \mid \emptyset a(b \mid b)$.
- One-pass is a property of the expression, not of its language, so a test on the language does not tell whether the table exists.
- The table gives a position for each symbol, not a full parse tree. In $(a^*)^*$ the positions are fixed, but the number of iterations of each star is not, so a group inside a star needs a rule, such as "the last iteration", to make its submatch unique.
- An unanchored search adds a guess at each start position, and the guesses clash: $(a \mid b)^* a^* b a^*$ is not one-pass even though $a^* b a^*$ is. Cox defines the property for anchored matches.

## Implementations

## History

Glushkov (1961) introduced the automaton whose states are the positions of an expression. Brüggemann-Klein (1993) gave its quadratic construction and the linear one for deterministic expressions, and Brüggemann-Klein and Wood (1998) defined one-unambiguous expressions, proved that they are the ones with a deterministic Glushkov automaton, and showed that not every regular language has one. Cox (2010) described RE2's one-pass engine, which uses the same idea on compiled programs to find submatches in one pass.

## References
