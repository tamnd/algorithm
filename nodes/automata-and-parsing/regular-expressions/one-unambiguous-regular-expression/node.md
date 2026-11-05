---
tag: PBD15E
kind: definition
slug: one-unambiguous-regular-expression
name: One-unambiguous regular expression
aliases:
- deterministic regular expression
- one-unambiguous expression
area: automata-and-parsing/regular-expressions
level: research
summary: A regex whose positions can be matched by a one-symbol lookahead, so it has a deterministic Glushkov automaton.
prereqs: [regular-expression, glushkov-automaton]
see_also: [one-pass-regex-matching, regex-ambiguity-detection, deterministic-finite-automaton, regular-language, dfa-minimization, pike-vm]
sources:
  - paper: doi:10.1006/inco.1997.2695
    title: Anne Brüggemann-Klein and Derick Wood, One-unambiguous regular languages, Information and Computation 142(2) (1998)
    locator: pp. 182 to 206 (the definition through marked expressions, the characterization by a deterministic Glushkov automaton, the orbit property of the minimal DFA, and the existence of regular languages with no one-unambiguous expression)
  - paper: doi:10.1016/0304-3975(93)90287-4
    title: Anne Brüggemann-Klein, Regular expressions into finite automata, Theoretical Computer Science 120(2) (1993)
    locator: pp. 197 to 213 (star normal form and the construction of the Glushkov automaton, in linear time for deterministic expressions)
  - paper: doi:10.1109/T-C.1971.223204
    title: Ronald Book, Shimon Even, Sheila Greibach and Gene Ott, Ambiguity in graphs and expressions, IEEE Transactions on Computers C-20(2) (1971)
    locator: pp. 149 to 153 (unambiguous regular expressions)
  - url: "https://swtch.com/~rsc/regexp/regexp3.html"
    title: Russ Cox, Regular Expression Matching in the Wild (2010)
    locator: section Step 4, Match, subsection on submatches (one-pass regular expressions, with the examples x*yx*, x*x, x(y|z) and (xy|xz))
---

A [regular expression](/regular-expression/) is one-unambiguous when, reading a word from left to right, each symbol tells which occurrence of a symbol in the expression it matches, with no lookahead beyond that symbol. Equivalently, its [Glushkov automaton](/glushkov-automaton/) is deterministic once its useless states are removed. Brüggemann-Klein and Wood introduced the notion in 1998 and showed that some [regular languages](/regular-language/) have no one-unambiguous expression. These expressions are also called deterministic regular expressions, and they are the ones that [one-pass matching](/one-pass-regex-matching/) can run with a single state.

## Definition

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union.

Number the occurrences of symbols in $r$ from left to right as $1, \dots, k$; these are the *positions* of $r$, and $\mathrm{sym}(p)$ is the symbol at position $p$. The *marked expression* $r'$ is $r$ with each occurrence replaced by its position, so $L(r')$ is a language over the alphabet $\{1, \dots, k\}$. For example, $(a \mid b)^* a$ marks to $(1 \mid 2)^* 3$ with $\mathrm{sym}(1) = \mathrm{sym}(3) = a$. Replacing each position by its symbol maps $L(r')$ onto $L(r)$.

**Definition.** The expression $r$ is **one-unambiguous** if for all words $u, v, v'$ over the positions and all positions $p, q$:

$$u p v \in L(r') \text{ and } u q v' \in L(r') \text{ and } \mathrm{sym}(p) = \mathrm{sym}(q) \implies p = q.$$

A regular language is **one-unambiguous** if some one-unambiguous expression denotes it.

**Characterization.** Let $G$ be the Glushkov automaton of $r$: state $0$ is initial, state $p \ge 1$ is position $p$, there is a move from $p$ to $q$ on $\mathrm{sym}(q)$ when $q$ can follow $p$ in a word of $L(r')$ (or start one, for $p = 0$), and the final states are the positions that can end a word, plus $0$ if $\varepsilon \in L(r)$. Brüggemann-Klein and Wood show that $r$ is one-unambiguous exactly when $G$ is deterministic, that is, no state has two moves on the same symbol. That statement assumes every position is useful. With $\emptyset$, a position can be useless, as the first $a$ of $a\emptyset \mid a$, which makes $G$ nondeterministic though the definition holds. The exact form is: $r$ is one-unambiguous if and only if the part of $G$ on states that are reachable from $0$ and can reach a final state is deterministic. The proof on the [one-pass matching](/one-pass-regex-matching/) page shows this form.

## Examples and non-examples

| expression | one-unambiguous | reason |
|---|---|---|
| $a^* b a^*$ | yes | each a is placed by whether b has been seen |
| $a^* a$ | no | the first a can be position 1 or position 2 |
| $a a^*$ | yes | the same language as $a^* a$ |
| $a(b \mid c)$ | yes | after a, the next symbol picks the branch |
| $ab \mid ac$ | no | the first a can be position 1 or position 3 |
| $(a \mid b)^* a$ | no | an a can be position 1 or position 3 |
| $b^* a (b^* a)^*$ | yes | the same language as $(a \mid b)^* a$ |
| $(a \mid \varepsilon) a$ | no | the first a can be position 1 or position 2 |
| $a(a \mid \varepsilon)$ | yes | the same language as $(a \mid \varepsilon) a$ |
| $(a^*)^*$ | yes | there is only one position |
| $a\emptyset \mid a$ | yes | position 1 is useless, so only position 2 can match |

The pairs $a^* a$ and $a a^*$, $(a \mid b)^* a$ and $b^* a (b^* a)^*$, and $(a \mid \varepsilon)a$ and $a(a \mid \varepsilon)$ show that the property belongs to the expression, not to its language. Brüggemann-Klein and Wood show that for some regular languages no rewriting helps: no expression for them is one-unambiguous. They decide this from the minimal DFA of the language, with a condition on its strongly connected parts that they call the orbit property.

## Related definitions

- **[Glushkov automaton](/glushkov-automaton/).** The automaton with one state per position. One-unambiguity is the determinism of its useful part, so a one-unambiguous expression with $k$ occurrences of symbols gives a DFA with at most $k + 1$ states and no [subset construction](/subset-construction/).
- **Unambiguous expression.** Book, Even, Greibach and Ott call an expression unambiguous when each word of $L(r)$ comes from only one word of $L(r')$. One-unambiguous expressions are unambiguous: two marked words with the same symbols differ first at some place, after a common prefix, which breaks the definition. The converse fails: $(a \mid b)^* a$ is unambiguous, since an a is position 3 exactly when it is the last symbol, but it is not one-unambiguous, because that is not known when the a is read. $(a \mid \varepsilon)(a \mid \varepsilon)$ is not even unambiguous: $a$ comes from position 1 or position 2. See [regex ambiguity detection](/regex-ambiguity-detection/).
- **[One-pass regex matching](/one-pass-regex-matching/).** The matcher that uses a deterministic Glushkov automaton, and the one-pass engine of RE2, which Cox describes by the same condition: at each input byte of an anchored match, only one alternative makes sense.
- **Star normal form.** An expression is in Brüggemann-Klein's star normal form when, for every subexpression $s^*$, the body $s$ is not nullable and no last position of $s$ already has a first position of $s$ among its followers inside $s$. She shows that every expression can be rewritten into this form with the same Glushkov automaton, and that from this form the Glushkov automaton is built in quadratic time, and in linear time for deterministic expressions.
- **[Deterministic finite automaton](/deterministic-finite-automaton/) and [DFA minimization](/dfa-minimization/).** The language-level question, whether some one-unambiguous expression exists, is decided on the minimal DFA.

## References
