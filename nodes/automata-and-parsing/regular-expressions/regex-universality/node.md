---
tag: SYDMCQ
kind: problem
slug: regex-universality
name: Regex universality
aliases:
- universality problem for regular expressions
area: automata-and-parsing/regular-expressions
level: advanced
summary: Decide whether a regular expression denotes all strings over its alphabet.
prereqs: [regular-expression, nfa-universality, pspace]
see_also: [regex-equivalence-pspace-completeness, regex-equivalence, regex-inclusion, regex-emptiness, nfa-universality, subset-construction, brzozowski-derivatives, regex-dfa-state-blowup]
sources:
  - paper: "Albert R. Meyer and Larry J. Stockmeyer, The equivalence problem for regular expressions with squaring requires exponential space, 13th Annual Symposium on Switching and Automata Theory (1972)"
    locator: pp. 125 to 129 (the reduction from Turing machines with bounded space; the universality of regular expressions is PSPACE-hard)
  - paper: "Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Fifth Annual ACM Symposium on Theory of Computing (STOC 1973)"
    locator: pp. 1 to 9 (regular expressions over a one-letter alphabet, and expressions with squaring and complement)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 8, Space Complexity (the nondeterministic space algorithm for the complement of NFA universality), and Section 9.1 (the regular expressions with exponentiation and the EXPSPACE-completeness proof)
  - paper: "Martin De Wulf, Laurent Doyen, Thomas A. Henzinger and Jean-Francois Raskin, Antichains: a new algorithm for checking universality of finite automata, Computer Aided Verification (CAV 2006), Lecture Notes in Computer Science 4144"
    locator: pp. 17 to 30
  - paper: "Janusz A. Brzozowski, Derivatives of regular expressions, Journal of the ACM 11(4) (1964)"
    locator: pp. 481 to 494 (finitely many dissimilar derivatives)
  - paper: "Richard E. Stearns and Harry B. Hunt III, On the equivalence and containment problems for unambiguous regular expressions, regular grammars and finite automata, SIAM Journal on Computing 14(3) (1985)"
    locator: pp. 598 to 611
---

Regex universality is the problem of deciding, for a [regular expression](/regular-expression/) $r$ over an alphabet $\Sigma$, whether $L(r) = \Sigma^*$. It is the complement-side twin of [emptiness](/regex-emptiness/), but much harder: emptiness takes linear time, while universality is [PSPACE](/pspace/)-complete (Meyer and Stockmeyer, 1972). It is coNP-complete over a one-letter alphabet. Every known algorithm takes exponential time in the worst case, and the shortest string that $r$ misses can be very long.

## In plain words

A pattern is universal if every string at all fits it. Checking that a pattern accepts nothing is easy, because you can look at the pattern from its leaves up. Checking that it accepts everything is not, because you must show that no string at all is missing.

One way is to turn the pattern into a machine and follow, letter by letter, the set of places the machine could be in, looking for a set that does not accept. The number of such sets can grow exponentially with the size of the pattern. No essentially better method is known, and complexity theory explains why: the problem is as hard as any problem solvable with a polynomial amount of memory.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols of $\Sigma$, $\varepsilon$, $\emptyset$, union $\mid$, concatenation and star $^*$. Let $m$ be the size of $r$.

**Input.** A finite alphabet $\Sigma$ and a regular expression $r$ over $\Sigma$.

**Output.** Yes if $L(r) = \Sigma^*$, no otherwise; in the "no" case, optionally a *counterexample* $w \in \Sigma^* \setminus L(r)$.

The alphabet is part of the input: $(a \mid b)^*$ is universal over $\{a, b\}$ but not over $\{a, b, c\}$.

## Variants

- **On automata.** [NFA universality](/nfa-universality/) is the same problem for NFAs, and it has the same complexity; the two are linearly equivalent by [regex to NFA conversion](/regex-to-nfa-conversion/) in one direction and by the reduction in the hardness proof in the other. For a DFA, universality is emptiness of the complement and takes linear time.
- **One letter.** For $\Sigma = \{a\}$ the problem is coNP-complete (Stockmeyer and Meyer, 1973). A counterexample is a number $\ell$ with $a^\ell \notin L(r)$, and it can be checked in polynomial time even when $\ell$ is written in binary, but it can be exponentially large.
- **Equivalence and inclusion.** Universality is $r \equiv \Sigma^*$, and also $\Sigma^* \subseteq L(r)$, so it is a special case of [equivalence](/regex-equivalence/) and of [inclusion](/regex-inclusion/), which are PSPACE-complete as well.
- **Richer syntax.** With a squaring operator $r^2$, or exponents written in binary, universality becomes EXPSPACE-complete (Meyer and Stockmeyer, 1972). With complement it becomes non-elementary (Stockmeyer and Meyer, 1973). Backreferences go beyond regular languages, and the automaton methods below do not apply to them.
- **Restricted expressions.** For unambiguous expressions and automata, universality and inclusion are polynomial (Stearns and Hunt, 1985; see [NFA equivalence](/nfa-equivalence/)).

## Examples

| $r$ over $\{a, b\}$ | universal? | shortest counterexample |
|---|---|---|
| $(a \mid b)^*$ | yes | none |
| $(a \mid b)^* a (a \mid b)^* \mid b^*$ | yes | none: a string either contains $a$ or is in $b^*$ |
| $(b \mid ab)^* (\varepsilon \mid a)$ | no | $aa$: the expression denotes the strings with no two adjacent $a$s |
| $a^* b^*$ | no | $ba$ |

For the second row, a script checked that all $2^9 - 1 = 511$ strings of length at most 8 are in the language.

**A long counterexample.** Over $\Sigma = \{a\}$ and for a prime $p$, the expression $(a^p)^* (\varepsilon \mid a)^{p - 2}$ denotes the strings $a^\ell$ with $\ell \bmod p \ne p - 1$. Take the union over the primes $2, 3, 5, 7$:
$$r = (aa)^* \mid (aaa)^*(\varepsilon \mid a) \mid (a^5)^*(\varepsilon \mid a)^3 \mid (a^7)^*(\varepsilon \mid a)^5.$$
A string $a^\ell$ is missing exactly when $\ell \equiv -1$ modulo all four primes, so the shortest counterexample is $a^{209}$, since $2 \cdot 3 \cdot 5 \cdot 7 = 210$. The expression has size 73. With the first $k$ primes, the size grows like $k^2 \log k$ while the shortest counterexample grows like $e^{(1 + o(1)) k \ln k}$, so it is not polynomial in $m$. A script confirmed the counterexamples $a^5$, $a^{29}$ and $a^{209}$ for the first two, three and four primes.

## Known algorithms

- **Subset search.** Build an NFA for $r$ with $O(m)$ states ([Thompson's construction](/thompson-construction/) or the [Glushkov automaton](/glushkov-automaton/)) and explore the sets of states reachable by the [subset construction](/subset-construction/), with [breadth-first search](/breadth-first-search/). The expression is universal if and only if every reachable set contains an accepting state, and a breadth-first search returns a shortest counterexample. Time $2^{O(m)}$.
- **Polynomial space.** Guess a counterexample one symbol at a time and keep only the current set of states, $O(m)$ space. This nondeterministic algorithm for non-universality runs in polynomial space, so the problem is in co-NPSPACE, which is PSPACE by [Savitch's theorem](/savitch-theorem/) and closure under complement.
- **Antichains.** A subset of a rejecting set is rejecting, so the search needs to keep only the minimal sets it has found (De Wulf, Doyen, Henzinger and Raskin, 2006). This is often much faster in practice; the worst case stays exponential.
- **Derivatives.** $L(r) = \Sigma^*$ if and only if every iterated [Brzozowski derivative](/brzozowski-derivatives/) of $r$ contains $\varepsilon$. Brzozowski (1964) showed that, up to associativity, commutativity and idempotence of union, $r$ has finitely many derivatives, so exploring them terminates. Their number can be exponential, as for the DFA.
- **One letter.** A shortest counterexample $a^\ell$ has $\ell$ at most the number of reachable subsets, so $\ell$ has $O(m)$ binary digits. Guess $\ell$ in binary and compute the set of states that $a^\ell$ reaches by repeated squaring of the Boolean transition matrix of the NFA, with $O(m)$ matrix products. This checks a counterexample in polynomial time and puts unary universality in coNP.

## Bounds

- **Complexity class.** PSPACE-complete for $\lvert\Sigma\rvert \ge 2$ (Meyer and Stockmeyer, 1972), and coNP-complete for $\lvert\Sigma\rvert = 1$ (Stockmeyer and Meyer, 1973). The proof of hardness, which encodes the runs of a Turing machine with polynomial space as strings and writes an expression for the strings that are *not* accepting runs, is on the page [PSPACE-completeness of regex equivalence](/regex-equivalence-pspace-completeness/).
- **Time.** $2^{O(m)}$ by the subset search. An algorithm in time $2^{o(m)}$ is not ruled out by PSPACE-completeness alone, but none is known.
- **Counterexamples.** The shortest string outside $L(r)$ has length at most the number of reachable subsets, $2^{O(m)}$, and it can be superpolynomially long in $m$, as the example with primes shows. So no algorithm can output a shortest counterexample in polynomial time in general.

## Reductions

- **From the acceptance problem of polynomial-space Turing machines.** As above: a machine rejects its input if and only if the expression of non-accepting histories is universal.
- **To equivalence and inclusion.** $L(r) = \Sigma^*$ if and only if $r \equiv (a_1 \mid \cdots \mid a_k)^*$ where $\Sigma = \{a_1, \ldots, a_k\}$. So equivalence and inclusion are PSPACE-hard as soon as universality is.
- **From NFA universality and back.** Linear in both directions, so results for one transfer to the other.
- **Emptiness is not a reduction target.** $L(r) = \Sigma^*$ is emptiness of the complement, but complementing an expression can cost an exponential in size ([state blowup](/regex-dfa-state-blowup/)), so the easy test for [emptiness](/regex-emptiness/) does not help.

## Applications

- **Checking that a validator accepts everything it should.** For example, that a pattern for tokens does not leave out any input, or that a set of routing rules written as patterns covers all paths.
- **Model checking.** Universality and inclusion of automata and expressions are the core of checking that a system's behaviors satisfy a specification; antichain algorithms come from this setting.
- **Lower bounds in other areas.** The PSPACE-hardness of universality is a common starting point for hardness proofs, for example for problems about automata, grammars and string constraints.

## References
