---
tag: RMWSPE
kind: definition
slug: regex-derivative
name: Brzozowski derivative of a regular expression
aliases:
- Brzozowski derivative
- derivative of a regex with respect to a symbol
area: automata-and-parsing/regular-expressions
level: advanced
summary: The expression for the suffixes after reading a symbol a, defined by structural recursion.
prereqs: [regular-expression]
see_also: [brzozowski-derivatives, antimirov-derivatives, brzozowski-finiteness-theorem, myhill-nerode-relation, regex-equivalence, extended-regular-expressions, regex-matching, deterministic-finite-automaton]
sources:
  - paper: doi:10.1145/321239.321249
    title: Janusz A. Brzozowski, Derivatives of regular expressions, Journal of the ACM 11(4) (1964)
    locator: pp. 481 to 494 (the definition by recursion, the theorem that the derivative denotes the quotient, similarity and the finiteness of dissimilar derivatives, and the derivative automaton)
  - paper: doi:10.1017/S0956796808007090
    title: Scott Owens, John Reppy and Aaron Turon, Regular-expression derivatives re-examined, Journal of Functional Programming 19(2) (2009)
    locator: pp. 173 to 190 (derivatives with intersection, complement and character classes, and the normal forms that keep the DFA small)
  - paper: "Valentin Antimirov, Partial derivatives of regular expressions and finite automaton constructions, Theoretical Computer Science 155(2) (1996)"
    locator: pp. 291 to 319 (partial derivatives as sets of expressions)
---

The Brzozowski derivative of a [regular expression](/regular-expression/) $r$ with respect to a symbol $a$ is an expression $\partial_a r$ that denotes the strings $w$ such that $aw \in L(r)$: what remains to be read after the first symbol $a$. It is computed by a recursion on the syntax of $r$, with no automaton. Brzozowski introduced it in 1964 and used it to build DFAs directly from expressions. Repeated derivatives give a matcher ([derivative-based matching](/brzozowski-derivatives/)), a DFA construction, and tests of [equivalence](/regex-equivalence/), and the definition works unchanged for intersection and complement.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols of $\Sigma$, $\varepsilon$, $\emptyset$, union $\mid$, concatenation and star $^*$. Practical features beyond regular languages, such as backreferences, have no derivative in this sense.

**Quotient of a language.** For a language $L \subseteq \Sigma^*$ and a string $u$, the *left quotient* is $u^{-1} L = \{w \in \Sigma^* : uw \in L\}$.

**Nullability.** Let $\nu(r) = \varepsilon$ if $\varepsilon \in L(r)$ and $\nu(r) = \emptyset$ otherwise. It is computed by $\nu(\emptyset) = \nu(a) = \emptyset$, $\nu(\varepsilon) = \nu(r^*) = \varepsilon$, $\nu(r \mid s) = \varepsilon$ if either side gives $\varepsilon$, and $\nu(rs) = \varepsilon$ if both sides do.

**Derivative by a symbol.** For $a \in \Sigma$,
$$\begin{aligned}
\partial_a \emptyset &= \emptyset, & \partial_a \varepsilon &= \emptyset, & \partial_a b &= \begin{cases} \varepsilon & b = a \\ \emptyset & b \ne a \end{cases} \\
\partial_a (r \mid s) &= \partial_a r \mid \partial_a s, & \partial_a (rs) &= (\partial_a r)\, s \mid \nu(r)\, \partial_a s, & \partial_a (r^*) &= (\partial_a r)\, r^*.
\end{aligned}$$

**Derivative by a string.** $\partial_\varepsilon r = r$ and $\partial_{ua} r = \partial_a (\partial_u r)$.

**The basic facts.** For every expression $r$, symbol $a$ and string $u$:

1. $L(\partial_a r) = a^{-1} L(r)$, and so $L(\partial_u r) = u^{-1} L(r)$.
2. $u \in L(r)$ if and only if $\nu(\partial_u r) = \varepsilon$.

Fact 1 is proved by induction on $r$. The cases of the constants, symbols and union are direct. For concatenation, a string $aw$ is in $L(r) L(s)$ either as $(a w_1) w_2$ with $a w_1 \in L(r)$ and $w_2 \in L(s)$, or as $\varepsilon \cdot (aw)$ with $\varepsilon \in L(r)$ and $aw \in L(s)$; these are the two terms. For star, a string $aw \in L(r)^*$ is a concatenation of nonempty strings of $L(r)$, the first of which starts with $a$, so $w \in (a^{-1} L(r)) L(r)^*$, and the converse is clear. The string version follows by induction on $u$. Fact 2 follows from Fact 1, since $u \in L(r)$ if and only if $\varepsilon \in u^{-1} L(r)$.

**Similarity.** Two expressions are *similar* if one can be turned into the other with the laws $r \mid r = r$, $r \mid s = s \mid r$ and $(r \mid s) \mid t = r \mid (s \mid t)$. Brzozowski proved that every expression has only finitely many derivatives up to similarity ([Brzozowski finiteness theorem](/brzozowski-finiteness-theorem/)). Implementations keep unions in a normal form, sorted and without duplicates, and also simplify with $\emptyset r = r \emptyset = \emptyset$, $\varepsilon r = r \varepsilon = r$ and $\emptyset \mid r = r$.

**The derivative automaton.** The DFA whose states are the derivatives of $r$ up to similarity, with start state $r$, moves $s \xrightarrow{a} \partial_a s$, and accepting states the nullable ones, accepts $L(r)$ by Fact 2.

## Examples and non-examples

**A derivative step by step.** Let $r = (a \mid b)^* abb$, read as $(a \mid b)^*$ followed by $abb$. Since $(a \mid b)^*$ is nullable,
$$\partial_a r = \big(\partial_a (a \mid b)^*\big)\, abb \mid \partial_a(abb) = (\varepsilon \mid \emptyset)(a \mid b)^* abb \mid \varepsilon bb,$$
which simplifies to $(a \mid b)^* abb \mid bb$. The strings that can follow a first $a$ are those of $r$ itself and the string $bb$.

**The derivative automaton of $(a \mid b)^* abb$.** With the simplifications above, a script found four derivatives:

| state | expression | nullable | by $a$ | by $b$ |
|---|---|---|---|---|
| 0 | $(a \mid b)^* abb$ | no | 1 | 0 |
| 1 | $(a \mid b)^* abb \mid bb$ | no | 1 | 2 |
| 2 | $(a \mid b)^* abb \mid b$ | no | 1 | 3 |
| 3 | $(a \mid b)^* abb \mid \varepsilon$ | yes | 1 | 0 |

This is the minimal DFA of the language. The script also checked Fact 1 on 4000 random expressions over two and three letters, including $\emptyset$, $\varepsilon$ and nested stars, by comparing the strings of $L(\partial_a r)$ with those of $a^{-1} L(r)$ up to length 5.

**Matching by derivatives.** To test $abb \in L(r)$, take $\partial_a r$, then $\partial_b$, then $\partial_b$: the states $0 \to 1 \to 2 \to 3$ in the table, and state 3 is nullable, so $abb \in L(r)$. For $ab$ the last state is 2, which is not nullable.

**Concatenation needs the nullable term.** $\partial_b(a^* b) = \varepsilon$, from the second term $\nu(a^*)\, \partial_b b$. The rule $(\partial_b a^*)\, b$ alone gives $\emptyset$, which is wrong, because $b \in L(a^* b)$.

**Not finite without simplification.** With no simplification at all, the derivatives of $a^*$ by $a, aa, aaa, \ldots$ are $\varepsilon a^*$, then $\emptyset a^* \mid \varepsilon a^*$, and so on, all different, with sizes 4, 9, 14, 19, $\ldots$ growing by 5 each time. They all denote $a^*$. With $\varepsilon r = r$ the first one is already $a^*$, and the sequence stops.

**Not the minimal DFA in general.** For $r = a^* \mid a a^*$ the derivatives up to similarity are $a^* \mid aa^*$, $a^*$ and $\emptyset$, three states, while $L(r) = a^*$ has a minimal DFA with two. Similarity identifies some equivalent expressions but not all, and identifying all of them is the [equivalence](/regex-equivalence/) problem.

**Not a syntactic prefix removal.** $\partial_a r$ is not obtained by deleting a leading $a$ from the text of $r$: $\partial_a ((ab)^*)$ is $b (ab)^*$, which is not a subexpression of $(ab)^*$, and $\partial_a (b \mid a)$ is $\varepsilon$, although $r$ does not start with $a$.

## Related definitions

- **Derivatives of extended expressions.** With intersection and complement, $\partial_a (r \mathbin{\&} s) = \partial_a r \mathbin{\&} \partial_a s$ and $\partial_a (\neg r) = \neg\, \partial_a r$, with $\nu$ extended in the obvious way. This is a strength of derivatives: no product or complement construction is needed ([extended regular expressions](/extended-regular-expressions/)). Owens, Reppy and Turon (2009) use this in a lexer generator, with character classes as labels.
- **Partial derivatives.** Antimirov's partial derivative $\partial_a r$ is a set of expressions whose union denotes the same language, defined with $\partial_a (r \mid s) = \partial_a r \cup \partial_a s$. The sets give an NFA with at most one more state than the number of symbol occurrences in $r$ ([Antimirov partial derivatives](/antimirov-derivatives/)).
- **Quotients and the Myhill-Nerode relation.** The quotients $u^{-1} L$ are exactly the classes that the [Myhill-Nerode relation](/myhill-nerode-relation/) distinguishes: the minimal DFA of $L$ has one state per distinct quotient. Derivatives are syntactic names for these quotients.
- **Right derivatives.** The symmetric operation removes a last symbol, with $\partial^R_a (rs) = r\, \partial^R_a s \mid \partial^R_a r\, \nu(s)$; it is the derivative of the reversed expression.
- **Derivative automaton and matcher.** The DFA above, built lazily during matching, is the [derivative-based matcher](/brzozowski-derivatives/).

## References
