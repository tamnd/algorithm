---
tag: B4SRCY
kind: problem
slug: regex-ambiguity-detection
name: Regex ambiguity detection
aliases:
- ambiguous regex detection
area: automata-and-parsing/regular-expressions
level: research
summary: Decide whether a regex admits two different ways to match some string, a cause of ReDoS.
prereqs: [regular-expression, glushkov-automaton, unambiguous-nfa, product-construction]
see_also: [redos, unambiguous-nfa, one-unambiguous-regular-expression, glushkov-automaton, posix-regex-semantics, submatch-extraction, state-elimination, cfg-ambiguity-undecidable]
sources:
  - paper: doi:10.1109/T-C.1971.223204
    title: Ronald V. Book, Shimon Even, Sheila A. Greibach and Gene Ott, Ambiguity in graphs and expressions, IEEE Transactions on Computers C-20(2) (1971)
    locator: pp. 149 to 153 (unambiguous expressions, an automaton that preserves the ambiguity of an expression, a test for ambiguity, and expressions from deterministic automata that are unambiguous)
  - paper: doi:10.1016/0304-3975(93)90287-4
    title: Anne Brüggemann-Klein, Regular expressions into finite automata, Theoretical Computer Science 120(2) (1993)
    locator: pp. 197 to 213 (the Glushkov automaton in quadratic time, star normal form, and a quadratic test for the ambiguity of an expression)
  - paper: doi:10.1016/0304-3975(91)90381-B
    title: Andreas Weber and Helmut Seidl, On the degree of ambiguity of finite automata, Theoretical Computer Science 88(2) (1991)
    locator: pp. 325 to 349 (the criteria EDA and IDA for exponential and polynomial ambiguity, and polynomial-time tests)
  - paper: doi:10.1142/S0129054111008477
    title: Cyril Allauzen, Mehryar Mohri and Ashish Rastogi, General algorithms for testing the ambiguity of finite automata and the double-tape ambiguity of finite-state transducers, International Journal of Foundations of Computer Science 22(4) (2011)
    locator: pp. 883 to 904 (tests for exponential, polynomial and finite ambiguity by intersecting an automaton with itself)
  - paper: doi:10.1145/1836089.1836120
    title: Claus Brabrand and Jakob G. Thomsen, Typed and unambiguous pattern matching on strings using regular expressions, PPDP 2010
    locator: pp. 243 to 254 (ambiguity of parse trees, its horizontal and vertical forms, and an ambiguity checker that reports example strings)
  - paper: doi:10.1007/978-3-319-40946-7_22
    title: Martin Sulzmann and Kenny Zhuo Ming Lu, Derivative-based diagnosis of regular expression ambiguity, CIAA 2016, Lecture Notes in Computer Science 9705
    locator: pp. 260 to 272
  - paper: doi:10.1007/978-3-319-40946-7_27
    title: Nicolaas Weideman, Brink van der Merwe, Martin Berglund and Bruce Watson, Analyzing matching time behavior of backtracking regular expression matchers by using ambiguity of NFA, CIAA 2016, Lecture Notes in Computer Science 9705
    locator: pp. 322 to 334 (exponential and polynomial backtracking related to the degree of ambiguity of an automaton for the expression)
---

Regex ambiguity detection is the problem of deciding whether a [regular expression](/regular-expression/) can match some string in two different ways. An ambiguous expression such as $a^* a^*$ forces a matcher to choose among parses, which is why [POSIX](/posix-regex-semantics/) and Perl need rules for capture groups, and an expression whose number of parses grows exponentially with the string, such as $(a \mid aa)^*$, can make a backtracking matcher run for exponential time, the root of most [ReDoS](/redos/) attacks. Unlike ambiguity of context-free grammars, which is [undecidable](/cfg-ambiguity-undecidable/), ambiguity of regular expressions is decidable in polynomial time, through the [Glushkov automaton](/glushkov-automaton/) and a product of the automaton with itself. The research questions are which notion of ambiguity matters, how fast the number of parses grows, and how to report a useful counterexample.

## In plain words

A pattern is ambiguous when some text fits it in more than one way. "Any number of a's, then any number of a's" fits "aaa" in four ways, depending on where the first part stops. Ambiguity does not change which texts match. It changes how much work a matcher may do and which pieces its groups report.

To check a pattern, label every letter of the pattern with its place, and ask whether two different labelled readings spell the same text. A machine that walks through the pattern letter by letter can answer this by running two copies of itself side by side on the same text and seeing whether they can split apart and still both finish.

The worst patterns are those where the number of ways explodes as the text grows, because a backtracking matcher may try every one of them.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols of $\Sigma$, $\varepsilon$, $\emptyset$, union $\mid$, concatenation and star $^*$. Let $m$ be the number of symbol occurrences in $r$.

**Marked expression.** Number the symbol occurrences of $r$ from 1 to $m$, and let $r'$ be the expression in which the $i$-th occurrence is replaced by a new symbol $a_i$, where $a$ is its letter. Erasing the numbers maps every string of $L(r')$ to a string of $L(r)$, and every string of $L(r)$ arises this way.

**Ambiguity.** The expression $r$ is *unambiguous* if no two different strings of $L(r')$ erase to the same string, and *ambiguous* otherwise. This is the notion of Book, Even, Greibach and Ott (1971); Brüggemann-Klein calls it weak ambiguity.

**Input.** A regular expression $r$.

**Output.** Whether $r$ is ambiguous, and if so a *witness*: a string $w$ with two different marked versions in $L(r')$.

**Degree of ambiguity.** For each $n$, let $d_r(n)$ be the largest number of marked versions of a string of length $n$. The expression is *finitely ambiguous* if $d_r$ is bounded, *polynomially ambiguous* if $d_r(n) = O(n^k)$ for some $k$, and *exponentially ambiguous* otherwise.

## Variants

- **Ambiguity of parse trees.** A parse tree records the side taken at each union, the split at each concatenation and the iterations of each star ([submatch extraction](/submatch-extraction/)). Two parse trees can give the same marked string: in $(a^*)^*$ the string $aa$ is one iteration of the outer star or two, and both read $a_1 a_1$. With empty iterations of a star forbidden, $(a^*)^*$ has $2^{n - 1}$ parse trees for $a^n$ while it is unambiguous in the marked sense. Brabrand and Thomsen (2010) decide this stronger notion, splitting it into *horizontal* ambiguity of concatenations and *vertical* ambiguity of unions and stars; Sulzmann and Lu (2016) do so with [derivatives](/regex-derivative/).
- **Degree.** Decide whether the ambiguity is finite, polynomial or exponential, and find the degree $k$ of a polynomial one. This is what matters for the running time of backtracking matchers.
- **Ambiguity of automata.** The same question for an NFA: whether some string has two accepting paths ([unambiguous NFA](/unambiguous-nfa/)).
- **Determinism.** A stronger condition: an expression is *deterministic*, or one-unambiguous, if a matcher can always tell which occurrence the next letter is without looking ahead, that is, if its Glushkov automaton is a DFA ([one-unambiguous regular expression](/one-unambiguous-regular-expression/)). Deterministic expressions are unambiguous, but $(a \mid b)^* abb$ is unambiguous and not deterministic.
- **Practical syntax.** Character classes, $r^+$, $r?$ and bounded repetition expand into the core syntax, and the expansion of $r\{2,5\}$ and similar forms can itself be ambiguous. Backreferences and lookaround go beyond this setting: backreferences leave the regular languages, and [lookaround](/regex-lookaround/) adds assertions that the definitions above do not cover.

## Examples

A script tested the method below against the definition on 1500 random expressions over two and three letters, including $\emptyset$, $\varepsilon$ and nested stars, by listing the marked strings of length at most 7, and it computed the counts in the table by counting accepting paths in the Glushkov automaton.

| expression | ambiguous? | shortest witness | $d_r(n)$ on $a^n$, $n = 1, \ldots, 8$ | degree |
|---|---|---|---|---|
| $(a \mid b)^* abb$ | no | none | 0 for all | finite |
| $(ab \mid a)(c \mid bc)$ | yes | $abc$ | 0 for all | finite, 2 |
| $(a \mid b)^* a (a \mid b)^*$ | yes | $aa$ | 1, 2, 3, 4, 5, 6, 7, 8 | linear |
| $a^* a^*$ | yes | $a$ | 2, 3, 4, 5, 6, 7, 8, 9 | linear |
| $a^* a^* a^*$ | yes | $a$ | 3, 6, 10, 15, 21, 28, 36, 45 | quadratic |
| $(a \mid aa)^*$ | yes | $aa$ | 1, 2, 3, 5, 8, 13, 21, 34 | exponential |
| $(aa \mid aaa)^*$ | yes | $aaaaa$ | 0, 1, 1, 1, 2, 2, 3, 4 | exponential |
| $(a^*)^*$ | no | none | 1 for all | finite |

- **$(ab \mid a)(c \mid bc)$.** The string $abc$ is $a_1 b_2 c_3$ or $a_4 b_5 c_6$: the $b$ belongs to the first or to the second factor. No string has more than two readings.
- **$a^* a^* a^*$.** A string $a^n$ is read by choosing where the first and second stars stop, $\binom{n + 2}{2}$ ways.
- **$(a \mid aa)^*$.** The readings of $a^n$ are the ways to write $n$ as an ordered sum of 1s and 2s, the Fibonacci numbers.
- **$(a^*)^*$.** Unambiguous in the marked sense, but with $2^{n - 1}$ parse trees for $a^n$ when every iteration is nonempty. A backtracking matcher explores these parse trees, which is why $(a^*)^* b$ is a classic ReDoS pattern although the test of the marked sense accepts it as unambiguous.

## Known algorithms

**The Glushkov automaton.** The [Glushkov automaton](/glushkov-automaton/) of $r$ has a start state $0$ and one state for each symbol occurrence $1, \ldots, m$; reading letter $a$ moves to an occurrence $i$ of $a$ that can come first, or that can follow the current occurrence. By Glushkov's theorem applied to the marked expression, the accepting paths $0 \to i_1 \to \cdots \to i_n$ correspond one to one to the strings $a_{i_1} \cdots a_{i_n}$ of $L(r')$. So $r$ is ambiguous if and only if its Glushkov automaton is ambiguous, and $d_r(n)$ is the largest number of accepting paths on a string of length $n$ (Book, Even, Greibach and Ott, 1971).

**Self-product test.** Remove the states that are not reachable from the start or cannot reach an accepting state. Build the product of the automaton with itself, with a move $(p, q) \xrightarrow{a} (p', q')$ whenever $p \xrightarrow{a} p'$ and $q \xrightarrow{a} q'$ ([product construction](/product-construction/)). The automaton is ambiguous if and only if some pair $(p, q)$ with $p \ne q$ is reachable from $(0, 0)$ and can reach a pair of accepting states. Two different accepting paths on the same string first differ at some step, which gives such a pair; conversely, a path of the product through such a pair is two different accepting paths. A search from $(0, 0)$ to such a pair and on to an accepting pair returns a witness. The product has $O(m^2)$ states and up to $O(m^4)$ moves, which is the bound of Book et al.; Brüggemann-Klein (1993) gave a quadratic test.

**Degree.** For an automaton with no useless states, Weber and Seidl (1991) proved:

- **EDA.** It is exponentially ambiguous if and only if some state $q$ has two different paths from $q$ back to $q$ with the same label. In $(a \mid aa)^*$, the first occurrence returns to itself on $aaa$ both as $a_1 a_1 a_1$ and through $a_2 a_3 a_1$.
- **IDA.** Without EDA, it is polynomially ambiguous, and the degree is the length $k$ of the longest chain of different states $p_0, \ldots, p_k$ with one string $v$ that loops at each $p_i$ and leads from each $p_{i - 1}$ to $p_i$. In $a^* a^*$ the two occurrences form such a chain with $v = a$.
- Without EDA and IDA it is finitely ambiguous.

EDA is a cycle in the self-product that passes both through a diagonal pair $(q, q)$ and an off-diagonal pair, and IDA is found in the product with three copies. Allauzen, Mohri and Rastogi (2011) test exponential ambiguity in time quadratic and polynomial ambiguity in time cubic in the number of transitions, also for automata with $\varepsilon$-moves.

**Parse trees and ReDoS.** For the stronger notion of parse trees, and for the running time of backtracking, the analysis must count the ways a matcher can split the text, not only the marked strings, so it is done on an automaton that keeps one path for each such way, closer to [Thompson's construction](/thompson-construction/) than to Glushkov's. Weideman, van der Merwe, Berglund and Watson (2016) relate exponential and polynomial backtracking to EDA and IDA of such an automaton, and use the witnesses to build attack strings ([ReDoS](/redos/)).

**Building unambiguous expressions.** Every regular language has an unambiguous expression: [state elimination](/state-elimination/) applied to a DFA produces one, because each accepted string has one path in the DFA and the construction preserves the ambiguity of the graph (Book et al., 1971).

## Bounds

- **Marked ambiguity.** Polynomial: $O(m^4)$ by the self-product, and quadratic time by Brüggemann-Klein's method. Any algorithm must read the expression, so $\Omega(m)$.
- **Witness length.** A shortest witness has length $O(m^2)$, the number of pairs in the product, since a shortest path visits no pair twice.
- **Degree of ambiguity.** Decidable in polynomial time, with the exact polynomial degree computable (Weber and Seidl, 1991; Allauzen, Mohri and Rastogi, 2011).
- **Context-free contrast.** For context-free grammars, ambiguity is undecidable ([CFG ambiguity](/cfg-ambiguity-undecidable/)); regular expressions are decidable because their parses are paths in a finite automaton.

## Reductions

- **To NFA ambiguity.** Through the Glushkov automaton, in polynomial size, as above.
- **To emptiness.** Ambiguity is nonemptiness of the part of the self-product that passes through an off-diagonal pair, a reachability question.
- **From NFA ambiguity.** An NFA without $\varepsilon$-moves can be turned into an expression by [state elimination](/state-elimination/), which preserves ambiguity, but the expression can be exponentially larger, so this direction is not a polynomial reduction in general.

## Applications

- **ReDoS detection.** Static analyzers flag expressions with exponential or high polynomial ambiguity, which backtracking engines may run for a long time, and produce attack strings from the witnesses ([ReDoS](/redos/)).
- **Predictable capture groups.** For an unambiguous expression every matching string has one parse, so the groups do not depend on the policy of the engine; leftmost-first and [POSIX](/posix-regex-semantics/) rules agree ([submatch extraction](/submatch-extraction/)).
- **Typed pattern matching.** Languages that split a string into typed fields by a regular expression reject ambiguous patterns, or warn and show a witness (Brabrand and Thomsen, 2010).
- **Schemas and validation.** XML DTDs and XML Schema require deterministic content models, a stronger form of unambiguity ([one-unambiguous regular expression](/one-unambiguous-regular-expression/)).
- **Counting and probability.** Unambiguous expressions and automata let one count the strings of each length, or compute probabilities, by counting paths ([unambiguous NFA](/unambiguous-nfa/)).

## References
