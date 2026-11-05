---
tag: PV1GEE
kind: problem
slug: star-height-problem
name: Star height problem
aliases:
- Star height
- nesting depth of stars
- star height of regular languages
area: automata-and-parsing/regular-expressions
level: research
summary: Determine the minimum star height of a regular language; Hashiguchi showed it is decidable.
prereqs: [regular-expression, kleene-star, nondeterministic-finite-automaton]
see_also: [star-free-expressions, star-free-language, regex-minimization, state-elimination, kleene-theorem, dfa-minimization, syntactic-monoid, schutzenberger-theorem]
sources:
  - paper: doi:10.1307/mmj/1028998975
    title: Lawrence C. Eggan, Transition graphs and the star-height of regular events, Michigan Mathematical Journal 10(4) (1963)
    locator: pp. 385 to 397 (star height and the cycle rank of transition graphs, and languages of every star height over growing alphabets)
  - paper: doi:10.1016/S0019-9958(66)90083-0
    title: Françoise Dejean and Marcel-Paul Schützenberger, On a question of Eggan, Information and Control 9(1) (1966)
    locator: pp. 23 to 25 (languages of every star height over a two-letter alphabet)
  - paper: doi:10.1016/S0019-9958(67)90481-0
    title: Robert McNaughton, The loop complexity of pure-group events, Information and Control 11(1-2) (1967)
    locator: pp. 167 to 176 (star height of languages whose syntactic monoid is a group, computed from the minimal automaton)
  - paper: doi:10.1016/S0019-9958(82)91028-2
    title: Kosaburo Hashiguchi, Regular languages of star height one, Information and Control 53(3) (1982)
    locator: pp. 199 to 210
  - paper: doi:10.1016/0890-5401(88)90033-8
    title: Kosaburo Hashiguchi, Algorithms for determining relative star height and star height, Information and Computation 78(2) (1988)
    locator: pp. 124 to 169 (the star height of a regular language is computable)
  - paper: doi:10.1051/ita:2005027
    title: Daniel Kirsten, Distance desert automata and the star height problem, RAIRO Theoretical Informatics and Applications 39(3) (2005)
    locator: pp. 455 to 509 (a reduction to limitedness of distance desert automata, and an algorithm in double exponential space)
  - paper: doi:10.1007/3-540-45995-2_12
    title: Sylvain Lombardy and Jacques Sakarovitch, Star height of reversible languages and universal automata, LATIN 2002, Lecture Notes in Computer Science 2286
    locator: pp. 76 to 90 (the star height of reversible languages, and an estimate of the cost of Hashiguchi's method)
  - paper: doi:10.1007/978-3-319-60134-2_9
    title: Nathanaël Fijalkow, Hugo Gimbert, Edon Kelmendi and Denis Kuperberg, Stamina, stabilisation monoids in automata theory, CIAA 2017, Lecture Notes in Computer Science 10329
    locator: pp. 101 to 112 (an implementation that computes star height for small automata)
---

The star height problem asks, for a regular language, for the least nesting depth of stars in a [regular expression](/regular-expression/) that denotes it. Eggan posed it in 1963 and showed that the depth can be as large as one likes, so there is no fixed bound. It stayed open for 25 years, until Hashiguchi (1988) gave an algorithm. That algorithm is far too expensive to run, and even the best known method, by Kirsten (2005), needs double exponential space; how hard the problem really is remains open. With complement allowed in expressions the question changes completely: no language is known to need more than one level of stars, and whether one exists is a famous open problem.

## In plain words

A star means "repeat any number of times", and stars can sit inside stars: "repeat (something that itself repeats)". The star height of a pattern is how deeply its stars are nested. The star height of a set of strings is the smallest nesting that any pattern for it needs.

Some sets need no star at all, because they are finite. Most everyday sets need only one level. But some need two, such as the strings with an even number of a's, and for every number there are sets that need that many levels.

The problem is to compute this number for a given set. Hashiguchi showed that a program can always find it, but every known method takes an absurd amount of time even on small inputs.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols of $\Sigma$, $\varepsilon$, $\emptyset$, union $\mid$, concatenation and star $^*$. Practical features that go beyond regular languages, such as backreferences, play no role here.

**Star height of an expression.**
$$h(\emptyset) = h(\varepsilon) = h(a) = 0, \qquad h(r \mid s) = h(rs) = \max(h(r), h(s)), \qquad h(r^*) = h(r) + 1.$$

**Star height of a language.** For a regular language $L$, $h(L)$ is the least $h(r)$ over all expressions $r$ with $L(r) = L$.

**Input.** A regular language, given by a DFA, an NFA or a regular expression, and possibly a number $k$.

**Output.** $h(L)$, or whether $h(L) \le k$.

**Cycle rank.** For a directed graph $G$, the *cycle rank* $\mathrm{cr}(G)$ is 0 if $G$ has no cycle, where a loop counts as a cycle; $1 + \min_v \mathrm{cr}(G - v)$ if $G$ is strongly connected; and the largest cycle rank of a strongly connected component otherwise. **Eggan's theorem** (1963): $h(L)$ equals the least cycle rank of the graph of a nondeterministic automaton that accepts $L$. One direction is [state elimination](/state-elimination/): eliminating the states in a suitable order, following the recursive definition of cycle rank, gives an expression whose star height is at most the cycle rank.

## Variants

- **Bounded height.** Is $h(L) \le k$ for a fixed $k$? For $k = 0$ this is finiteness, since expressions without star denote finite languages and every finite language is a union of strings; it takes polynomial time from an automaton. For $k = 1$ Hashiguchi gave an algorithm in 1982, six years before the general case.
- **Generalized star height.** Allow intersection and complement in the expressions. Then the languages of height 0 are the [star-free languages](/star-free-language/), described by [star-free expressions](/star-free-expressions/), and $(aa)^*$ has height 1. No language is known to have generalized star height 2 or more, and it is open whether every regular language has height at most 1.
- **Restricted classes.** For languages whose [syntactic monoid](/syntactic-monoid/) is a group, McNaughton (1967) computed the star height from the minimal DFA; Lombardy and Sakarovitch (2002) extended such results to reversible languages.
- **Relative star height.** The star height of $L$ in expressions built over a given finite set of languages instead of single letters, which Hashiguchi (1988) also solved.

## Examples

A script computed the cycle rank of the minimal DFA, without its dead state, for each language below, and confirmed that $(b \mid a b^* a)^*$ denotes the strings with an even number of $a$s, on all strings of length at most 10 over $\{a, b\}$.

| language | expression | $h$ of expression | cycle rank of minimal DFA | $h(L)$ |
|---|---|---|---|---|
| $\{aab, ba\}$ | $aab \mid ba$ | 0 | 0 | 0 |
| $\{a, b\}^*$ | $(a \mid b)^*$ | 1 | 1 | 1 |
| $(ab)^*$ | $(ab)^*$ | 1 | 1 | 1 |
| strings ending in $abb$ | $(a \mid b)^* abb$ | 1 | 2 | 1 |
| an even number of $a$s | $(b \mid a b^* a)^*$ | 2 | 2 | 2 |

- **The DFA is only an upper bound.** The minimal DFA of $(a \mid b)^* abb$ has cycle rank 2, but the language has star height 1. Eggan's theorem minimizes over nondeterministic automata, and the NFA that guesses where $abb$ starts has a single loop.
- **An even number of $a$s.** In the minimal DFA, $a$ swaps the two states and $b$ fixes them, so the syntactic monoid is a group, and the DFA has one accepting state. McNaughton's theorem then gives star height equal to the cycle rank of the minimal DFA: the two states form a cycle, and removing either one leaves a state with a loop on $b$, so the rank is 2. As a consistency check, a search of all expressions of star height at most 1 with up to 14 symbols and operators found none for this language.
- **Every height occurs.** Dejean and Schützenberger (1966) gave languages over $\{a, b\}$ of every star height $n$, built by $e_1 = (ab)^*$ and $e_{n + 1} = (a^{2^n} e_n\, b^{2^n} e_n)^*$, which answered Eggan's question for a two-letter alphabet; Eggan's own examples used $2^n - 1$ letters.

## Known algorithms

- **Hashiguchi (1988).** The first algorithm. Hashiguchi introduced automata that count along their runs, distance automata, and used the decidability of whether their counts stay bounded to reduce the question to a finite but enormous search. Lombardy and Sakarovitch (2002) estimated that it would have to test a number of candidates that is a tower of exponentials even for a 4-state automaton.
- **Kirsten (2005).** A reduction of "$h(L) \le k$" to the *limitedness* problem for *distance desert automata*, nondeterministic automata that assign a cost to each run: $h(L) \le k$ if and only if an automaton built from an NFA for $L$ and $k$ has a bounded cost on every string of $L$. Limitedness is decided with a finite monoid of matrices, which gives an algorithm in double exponential space. Searching $k = 0, 1, 2, \ldots$ up to the cycle rank of an NFA for $L$ computes $h(L)$.
- **Cost functions.** Colcombet and Löding recast this method in the theory of regular cost functions and extended it to trees, and the tool Stamina (Fijalkow, Gimbert, Kelmendi and Kuperberg, 2017) implements it with stabilisation monoids for small automata.
- **Special cases.** For group languages and reversible languages, the star height can be read off the minimal or universal automaton, by McNaughton (1967) and Lombardy and Sakarovitch (2002).
- **Upper bounds.** [State elimination](/state-elimination/) on any automaton for $L$ gives an expression of height at most the cycle rank of its graph, in particular at most the number of states.

## Bounds

- **Decidability.** Decidable (Hashiguchi, 1988).
- **Upper bound.** Double exponential space in the size of an NFA for $L$ (Kirsten, 2005).
- **Lower bound.** No lower bound close to this is known, and the exact complexity is open. Even the special case $h(L) \le 1$ has no known efficient algorithm.
- **Unbounded heights.** For every $n$ there are languages over two letters with $h(L) = n$ (Dejean and Schützenberger, 1966).
- **Height of an automaton.** For an NFA with $n$ states, $h(L) \le \mathrm{cr} \le n$.

## Reductions

- **To limitedness.** "$h(L) \le k$" reduces to the limitedness of a distance desert automaton of size exponential in the input (Kirsten, 2005), and limitedness reduces to computations in a finite monoid of matrices over a small semiring.
- **From finiteness.** $h(L) = 0$ if and only if $L$ is finite ([DFA finiteness](/dfa-finiteness/)).
- **Generalized star height 0.** Deciding whether the generalized star height is 0 is deciding star-freeness, which reduces to the aperiodicity of the syntactic monoid by [Schützenberger's theorem](/schutzenberger-theorem/).

## Applications

- **Descriptional complexity.** Star height is a basic measure of how complex a regular language is, alongside the sizes of minimal DFAs, NFAs and expressions ([regex minimization](/regex-minimization/)), and lower bounds on star height give lower bounds on expression size.
- **Cost functions and limitedness.** The methods built to solve the star height problem, distance and desert automata and regular cost functions, became tools of their own, used for boundedness questions in logic, games and verification.
- **Algebraic classification.** Star height and generalized star height ask which languages need nested iteration, and they connect expressions to the structure of syntactic monoids, as in the [star-free](/star-free-expressions/) case.

## References
