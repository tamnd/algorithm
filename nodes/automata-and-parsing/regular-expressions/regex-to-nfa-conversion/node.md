---
tag: QQF3XA
kind: problem
slug: regex-to-nfa-conversion
name: Regex to NFA conversion
aliases:
- regex compilation to an automaton
area: automata-and-parsing/regular-expressions
level: core
summary: Build an automaton that recognises the language of a given regular expression.
prereqs: [regular-expression, nondeterministic-finite-automaton, epsilon-nfa]
see_also: [thompson-construction, glushkov-automaton, antimirov-derivatives, brzozowski-derivatives, kleene-theorem, dfa-to-regex-conversion, regex-dfa-state-blowup, subset-construction]
sources:
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.3, Lemma 1.55 (an NFA for each regular expression, by induction on the expression)
  - paper: "Robert McNaughton and Hisao Yamada, Regular expressions and state graphs for automata, IRE Transactions on Electronic Computers EC-9(1) (1960)"
    locator: pp. 39 to 47 (the automaton on the positions of the symbols)
  - paper: "Victor M. Glushkov, The abstract theory of automata, Russian Mathematical Surveys 16(5) (1961)"
    locator: pp. 1 to 53
  - paper: "Valentin Antimirov, Partial derivatives of regular expressions and finite automaton constructions, Theoretical Computer Science 155(2) (1996)"
    locator: pp. 291 to 319 (at most one more partial derivative than occurrences of symbols)
  - paper: "Juraj Hromkovič, Sebastian Seibert and Thomas Wilke, Translating regular expressions into small ε-free nondeterministic finite automata, Journal of Computer and System Sciences 62(4) (2001)"
    locator: pp. 565 to 588 (O(n log^2 n) moves by common follow sets)
  - paper: "Georg Schnitger, Regular expressions and NFAs without ε-transitions, STACS 2006, Lecture Notes in Computer Science 3884"
    locator: pp. 432 to 443 (the matching lower bound of Ω(n log^2 n) moves)
  - paper: "Yury Lifshits, A lower bound on the size of ε-free NFA corresponding to a regular expression, Information Processing Letters 85 (2003)"
    locator: pp. 293 to 299
---

Regex to NFA conversion is the problem of building a nondeterministic finite automaton that accepts exactly the language of a given [regular expression](/regular-expression/). It is the easy direction of [Kleene's theorem](/kleene-theorem/): automata with a number of states linear in the size of the expression always exist and are built in linear or quadratic time. It is the first step of most regex engines, which then simulate the automaton or turn it into a DFA. The main methods are [Thompson's construction](/thompson-construction/) with $\varepsilon$-moves, the [Glushkov automaton](/glushkov-automaton/) without them, and [Antimirov's partial derivatives](/antimirov-derivatives/).

## In plain words

A regular expression is a formula; an automaton is a machine with states and arrows that reads a word letter by letter. The task is to build a machine that says yes exactly to the words that the formula describes.

The formula is built from small parts with three operations: "or", "then" and "repeat". So the machine can be built from small parts in the same way: a tiny machine for each letter, and a rule for each operation that joins machines into a bigger one. Each rule adds only a few states, so the machine is about as big as the formula. Another method gives one state to each letter of the formula and draws an arrow wherever one letter can follow another.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols of $\Sigma$, $\varepsilon$, $\emptyset$, union $\mid$, concatenation and star $^*$. Let $m$ be the size of $r$ (the number of nodes of its syntax tree) and $m'$ its *alphabetic width*, the number of occurrences of symbols in it.

**Input.** A regular expression $r$.

**Output.** A nondeterministic finite automaton $N$, with or without [$\varepsilon$-moves](/epsilon-nfa/), such that $L(N) = L(r)$.

**Measures.** The number of states, the number of moves, and the time to build $N$. Different uses value them differently: simulation costs time proportional to the moves for each input symbol, and the [subset construction](/subset-construction/) costs time exponential in the states.

## Variants

- **With $\varepsilon$-moves.** Allowed by [Thompson's construction](/thompson-construction/); the result is easy to build and to reason about, and simulation must follow [$\varepsilon$-closures](/epsilon-closure/).
- **Without $\varepsilon$-moves.** The [Glushkov automaton](/glushkov-automaton/), also called the position automaton, has exactly $m' + 1$ states.
- **Fewest moves.** An $\varepsilon$-free NFA with as few moves as possible; the answer is $\Theta(m \log^2 m)$ in the worst case.
- **Fewest states.** Finding a smallest NFA is hard in general ([NFA minimization](/nfa-minimization/)); constructions that give quotients of the Glushkov automaton, such as the partial derivative automaton, are a cheap approximation.
- **Deterministic.** A DFA for $r$ can need $2^{\Omega(m)}$ states ([state blowup](/regex-dfa-state-blowup/)), so it is a different problem, solved by the [subset construction](/subset-construction/) or by [Brzozowski derivatives](/brzozowski-derivatives/).
- **Practical syntax.** Character classes, $r^+$, $r?$ and bounded repetition expand into the core syntax, the last one with a size increase ([bounded repetition](/bounded-repetition/)). Backreferences have no finite automaton, since the language is not regular in general ([backreference](/backreference/)).

## Examples

Take $r = (a \mid b)^* abb$, of size 10 and alphabetic width 5.

| construction | states | moves | $\varepsilon$-moves |
|---|---|---|---|
| [Thompson](/thompson-construction/) | 14 | 16 | 11 |
| [Glushkov](/glushkov-automaton/) | 6 | 11 | 0 |
| [Antimirov](/antimirov-derivatives/) | 4 | 5 | 0 |
| minimal DFA, for comparison | 4 | 8 | 0 |

The Glushkov automaton numbers the occurrences of symbols, $(a_1 \mid b_2)^* a_3 b_4 b_5$, and has a state for each of them plus an initial state 0. The positions that can come first are $a_1, b_2, a_3$, and the only one that can come last is $b_5$. A position $p$ has a move to $q$, labelled with the symbol of $q$, when $q$ can directly follow $p$: each of $a_1, b_2$ is followed by $a_1, b_2, a_3$; then $a_3$ by $b_4$, and $b_4$ by $b_5$. That gives 3 moves from 0, 6 from $a_1$ and $b_2$, and 2 more, 11 in total, and the accepting state $b_5$.

The partial derivatives of $r$, with $S = (a \mid b)^*$, are $S\,abb$, $bb$, $b$ and $\varepsilon$. The moves are $S\,abb \xrightarrow{a} S\,abb$, $S\,abb \xrightarrow{a} bb$, $S\,abb \xrightarrow{b} S\,abb$, $bb \xrightarrow{b} b$ and $b \xrightarrow{b} \varepsilon$, and the only accepting state is $\varepsilon$.

**Quadratic moves.** For $r = (a_1 \mid a_2 \mid \cdots \mid a_k)^*$ with distinct symbols, every position can follow every position, so the Glushkov automaton has $k + 1$ states and $k + k^2$ moves; the Thompson automaton has $O(k)$ of both.

## Known algorithms

| method | states | moves | time |
|---|---|---|---|
| [Thompson](/thompson-construction/) (1968) | at most $2m$ | at most $4m$ | $\Theta(m)$ |
| [Glushkov](/glushkov-automaton/), McNaughton and Yamada (1960), Glushkov (1961) | $m' + 1$ | $O(m'^2)$ | $O(m^2)$ |
| [Antimirov](/antimirov-derivatives/) partial derivatives (1996) | at most $m' + 1$ | $O(m'^2)$ | polynomial |
| Common follow sets, Hromkovič, Seibert and Wilke (1997, 2001) | not the measure it optimizes | $O(m \log^2 m)$ | polynomial |
| Inductive construction of the textbooks | $O(m)$ | $O(m)$ | $O(m)$ |

- **[Thompson's construction](/thompson-construction/)** builds, for each node of the syntax tree, a fragment with one entry and one exit, and joins the fragments with $\varepsilon$-moves. Each state has at most two moves, which makes the [simulation](/thompson-nfa-simulation/) simple.
- **The [Glushkov automaton](/glushkov-automaton/)** is computed from three functions of the expression: the positions that can come first, the positions that can come last, and for each position the positions that can follow it, all computed bottom-up on the syntax tree. It has no $\varepsilon$-moves, and all moves into a state carry the same symbol.
- **[Antimirov's partial derivatives](/antimirov-derivatives/)** take as states the expressions reachable from $r$ by partial derivatives, sets of expressions instead of the one expression of a [Brzozowski derivative](/brzozowski-derivatives/). Antimirov proved that there are at most $m' + 1$ of them, and the automaton is a quotient of the Glushkov automaton, so it is never larger.
- **The textbook construction** of Sipser and of Hopcroft, Motwani and Ullman is a variant of Thompson's construction; Sipser's version allows several accepting states and so adds fewer $\varepsilon$-moves.

## Bounds

- **States.** Every method above gives $O(m)$ states. Some expressions need $\Omega(m)$: the expression $a^k$, of alphabetic width $k$, needs $k + 1$ states in any NFA: an accepting run on $a^k$ visits $k + 1$ states, and if two of them were equal, the run could skip the loop between them and accept a shorter word, which is not in the language.
- **Moves with $\varepsilon$.** $O(m)$ moves suffice, by Thompson's construction.
- **Moves without $\varepsilon$.** Hromkovič, Seibert and Wilke proved that $O(m \log^2 m)$ moves suffice, and Schnitger (2006) proved a matching lower bound of $\Omega(m \log^2 m)$ for a family of expressions over a growing alphabet, improving a bound of $\Omega(m \log^2 m / \log \log m)$ by Lifshits (2003).
- **Determinism.** A DFA can need $2^{\Omega(m)}$ states; see [exponential state blowup](/regex-dfa-state-blowup/).
- **Time.** $\Theta(m)$ for Thompson's construction, which is optimal since the input must be read.

## Reductions

- **Regex problems to NFA problems.** Every decision problem on regular expressions, such as [matching](/regex-matching/), [emptiness](/regex-emptiness/), [universality](/regex-universality/), [inclusion](/regex-inclusion/) and [equivalence](/regex-equivalence/), reduces to the same problem on NFAs in linear time by this conversion. The upper bounds of the NFA problems therefore carry over, and the lower bounds of the regex problems carry back.
- **The other direction.** [DFA to regex conversion](/dfa-to-regex-conversion/) by [state elimination](/state-elimination/) goes back, but it can produce expressions of size exponential in the number of states, so the two directions are not equally cheap.
- **To DFAs.** The [subset construction](/subset-construction/) on any of these automata gives a DFA; on the Glushkov automaton, the states of the DFA are sets of positions, which is the method used by many lexer generators.

## Applications

- **Regex engines.** RE2, the Go and Rust regex libraries, and [grep](/grep/) compile patterns to an NFA first and then simulate it or build a DFA lazily ([lazy DFA construction](/lazy-dfa-construction/)).
- **Lexer generators.** Tools such as lex and flex convert the token patterns to automata and then to one DFA.
- **Bit-parallel matching.** The Glushkov automaton has $m' + 1$ states and all moves into a state carry the same symbol, which [bit-parallel regex matching](/bit-parallel-regex-matching/) exploits to update the state set with a few word operations.
- **Decision procedures.** Tools that decide [equivalence](/regex-equivalence/) and [inclusion](/regex-inclusion/) of expressions start from these automata.

## References
