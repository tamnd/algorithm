---
tag: 90F3MH
kind: problem
slug: regex-emptiness
name: Regex emptiness
aliases:
- empty language problem for regular expressions
area: automata-and-parsing/regular-expressions
level: core
summary: Decide whether a regular expression denotes the empty language.
prereqs: [regular-expression]
see_also: [dfa-emptiness, regex-universality, regex-inclusion, regex-equivalence, extended-regular-expressions, regular-language-intersection, graph-reachability, regex-to-nfa-conversion]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.3.2, Testing Emptiness of Regular Languages (the inductive test on regular expressions and the test by reachability on automata)
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer (1997)
    locator: Lectures 7 to 9 (regular expressions, their languages and the equivalence with finite automata)
  - paper: "Dexter Kozen, Lower bounds for natural proof systems, 18th Annual Symposium on Foundations of Computer Science (FOCS 1977)"
    locator: pp. 254 to 266 (the nonemptiness of the intersection of finite automata is PSPACE-complete)
  - paper: "Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Fifth Annual ACM Symposium on Theory of Computing (STOC 1973)"
    locator: pp. 1 to 9 (lower bounds for expressions with squaring and with complement)
---

Regex emptiness is the problem of deciding whether a [regular expression](/regular-expression/) denotes the empty language, $L(r) = \emptyset$. For ordinary regular expressions it is easy: one bottom-up pass over the syntax tree decides it in time linear in the size of the expression, and the same pass finds a shortest string in the language. It becomes hard when the syntax has intersection, which makes it PSPACE-complete, or complement, which makes it non-elementary. It is the base case of the harder questions of [universality](/regex-universality/), [inclusion](/regex-inclusion/) and [equivalence](/regex-equivalence/).

## In plain words

A pattern can describe no string at all. That happens only when it uses the "empty" constant in a place where it cannot be avoided: in every option of an "or", or in any part of a "then". A "repeat" is never empty, because repeating zero times gives the empty string.

So you can check a pattern from the leaves up. A letter is not empty, an "or" is empty only when both sides are, a "then" is empty when either side is, and a "repeat" is never empty. The same walk can build a shortest string that the pattern accepts.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols of $\Sigma$, $\varepsilon$, $\emptyset$, union $r \mid s$, concatenation $rs$ and star $r^*$. The size $m$ is the number of nodes of the syntax tree.

**Input.** A regular expression $r$.

**Output.** Yes if $L(r) = \emptyset$, no otherwise; in the "no" case, optionally a string $w \in L(r)$.

**The rule.** Define $E(r)$, read "$r$ is empty", by
$$E(\emptyset) = \text{true}, \quad E(\varepsilon) = E(a) = \text{false}, \quad E(r \mid s) = E(r) \wedge E(s), \quad E(rs) = E(r) \vee E(s), \quad E(r^*) = \text{false}.$$
Then $L(r) = \emptyset$ if and only if $E(r)$ is true. The proof is an induction on $r$ that follows the semantics: $L(r \mid s) = L(r) \cup L(s)$ is empty exactly when both parts are; $L(rs) = \{uv : u \in L(r), v \in L(s)\}$ is empty exactly when one part is, since otherwise a $u$ and a $v$ give the string $uv$; and $L(r^*)$ always contains $\varepsilon$.

**A shortest witness.** In the same pass compute $W(r)$, a shortest string of $L(r)$, or "none": $W(\emptyset)$ is none, $W(\varepsilon) = \varepsilon$, $W(a) = a$, $W(r \mid s)$ is the shorter of $W(r)$ and $W(s)$, $W(rs) = W(r)W(s)$, and $W(r^*) = \varepsilon$. The length of $W(r)$ is at most the number of occurrences of symbols in $r$, because each symbol of $W(r)$ comes from a different leaf.

## Variants

- **On automata.** For an NFA, emptiness is [graph reachability](/graph-reachability/) from the start state to an accepting state, in time linear in the size of the automaton; see [DFA emptiness](/dfa-emptiness/). Converting $r$ to an NFA by [Thompson's construction](/thompson-construction/) and testing reachability is a second linear-time method.
- **Nonemptiness of an intersection.** Given $r_1, \ldots, r_k$, decide whether $L(r_1) \cap \cdots \cap L(r_k) \neq \emptyset$. For a fixed $k$ this is reachability in the product of the automata, polynomial in the sizes ([regular language intersection](/regular-language-intersection/)). When $k$ is part of the input it is PSPACE-complete; Kozen (1977) proved it for DFAs, and the same encoding of a polynomial-space computation works for expressions.
- **Intersection as an operator.** With $\cap$ in the syntax, emptiness is PSPACE-complete by the same argument: the upper bound searches the product automaton one state at a time, a state being a tuple of positions of polynomial size.
- **Complement as an operator.** With complement in the syntax ([extended regular expressions](/extended-regular-expressions/)), emptiness of $\neg r$ is universality of $r$, and the problem is decidable but non-elementary: each nested complement can cost an exponential, and Stockmeyer and Meyer showed that no algorithm avoids a tower of exponentials whose height grows with the expression.
- **Emptiness of the language minus a word.** Deciding whether $L(r) \setminus \{\varepsilon\}$ is empty, or whether $L(r)$ is finite, uses the same kind of bottom-up pass with more information per node.

## Examples

| $r$ | empty? | shortest string | why |
|---|---|---|---|
| $(a \mid b)^* \emptyset (a \mid b)^*$ | yes | none | a concatenation with $\emptyset$ |
| $\emptyset^*$ | no | $\varepsilon$ | a star is never empty; $L(\emptyset^*) = \{\varepsilon\}$ |
| $a(b\emptyset \mid \emptyset)^*$ | no | $a$ | the star body is empty, the star is $\{\varepsilon\}$ |
| $(a\emptyset)^* b \mid \emptyset a$ | no | $b$ | the left branch denotes $\{b\}$, the right branch nothing |
| $((a \mid b)\emptyset)^* (ab \mid \emptyset)(b\emptyset \mid ba)$ | no | $abba$ | the only string of the language |

The answers were checked against the list of all strings, up to the number of symbol occurrences in the expression, that each expression denotes.

**A common mistake.** The expression $\emptyset^*$ is not empty. Rules that treat $\emptyset$ as absorbing everywhere give the wrong answer for star, and the equation $\emptyset^* = \varepsilon$ is one of the [laws](/regular-expression/) of regular expressions.

## Known algorithms

- **Bottom-up evaluation.** Compute $E$ and $W$ in post-order on the syntax tree, with an explicit stack for deep trees. Time $O(m)$ for $E$ and for the length of $W$; writing out $W$ costs its length, at most $m$.
- **Reachability on an automaton.** Build an NFA for $r$ and search for a path from the start to an accepting state with [breadth-first search](/breadth-first-search/); the path spells a shortest witness, since each symbol move adds one to its length and the search can use 0-1 weights for $\varepsilon$-moves. Time $O(m)$.
- **Product search for intersections.** For $r_1 \cap \cdots \cap r_k$, search the product of the $k$ automata. The product has up to $\prod_i O(m_i)$ states; a breadth-first search costs that much time, and a nondeterministic search needs only the current tuple, which gives the PSPACE upper bound by [Savitch's theorem](/savitch-theorem/).

## Bounds

- **Ordinary expressions.** $\Theta(m)$ time in the worst case on the [word RAM](/word-ram/): the algorithm is linear, and every node can matter, since replacing any one leaf by $\emptyset$ or by a symbol can change the answer.
- **Intersection.** PSPACE-complete when the number of expressions, or of $\cap$ operators, is part of the input ([PSPACE](/pspace/)).
- **Complement.** Non-elementary: for each fixed $k$, no algorithm runs in time bounded by a tower of $k$ exponentials.

## Reductions

- **From emptiness to the other decision problems.** $L(r) = \emptyset$ if and only if $L(r) \subseteq L(\emptyset)$, if and only if $r \equiv \emptyset$. So emptiness is the easy special case of [inclusion](/regex-inclusion/) and [equivalence](/regex-equivalence/), which are PSPACE-complete in general.
- **Universality is not its mirror.** $L(r) = \Sigma^*$ asks for emptiness of the complement, and complementing a regular expression or an NFA can cost an exponential. That is why [regex universality](/regex-universality/) is PSPACE-complete while emptiness is linear.
- **Inclusion against a DFA.** $L(r) \subseteq L(D)$ for a DFA $D$ is emptiness of $L(r) \cap \overline{L(D)}$, a product of an NFA for $r$ with the complemented DFA, so it is polynomial.

## Applications

- **Simplifying expressions.** Engines and tools that rewrite expressions remove empty subexpressions first: a union branch that is empty is dropped, and a concatenation with an empty part becomes $\emptyset$.
- **Derivative-based algorithms.** Matchers and equivalence checkers that use [Brzozowski derivatives](/brzozowski-derivatives/) test each derivative for emptiness to prune dead states.
- **Static analysis.** Checking that a pattern can match at all, or that a guard in a program is satisfiable when it is written as a regular constraint, is an emptiness test; string constraint solvers check emptiness of intersections of regular constraints.
- **Test generation.** The shortest witness $W(r)$ is a small test input that the pattern accepts.

## References
