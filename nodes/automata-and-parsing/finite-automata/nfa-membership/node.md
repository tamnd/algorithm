---
tag: XKNBNP
kind: problem
slug: nfa-membership
name: NFA membership
aliases:
- string acceptance problem
- word problem for finite automata
area: automata-and-parsing/finite-automata
level: intro
summary: Given an automaton and a string, decide whether the automaton accepts the string.
model: word-ram
complexity:
  vars: {ℓ: the length of the string, n: the number of states, m: the number of transitions}
  time: {worst: O(ℓ(n + m))}
prereqs: [nondeterministic-finite-automaton]
see_also: [nfa-simulation, subset-construction, regex-matching, thompson-nfa-simulation, lazy-dfa-construction, backtracking-regex-matching, backurs-indyk-regex-hardness, nondeterministic-logspace]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 4.1, Decidable Languages (Theorem 4.2, the acceptance problem for NFAs); Section 8.5, NL-Completeness (PATH is NL-complete)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.3.3, Testing Membership in a Regular Language
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422 (the simulation of the automaton of a regular expression by a set of current states)
  - paper: doi:10.1016/S0022-0000(75)80050-X
    title: Neil D. Jones, Space-bounded reducibility among combinatorial problems, Journal of Computer and System Sciences 11(1) (1975)
    locator: pp. 68 to 85 (the NL-completeness of directed reachability)
  - paper: "Arturs Backurs and Piotr Indyk, Which regular expression patterns are hard to match?, 57th IEEE Symposium on Foundations of Computer Science (FOCS 2016)"
    locator: the conditional quadratic lower bounds for the membership and the pattern matching problems
  - paper: doi:10.1145/128749.128755
    title: Eugene W. Myers, A four Russians algorithm for regular expression pattern matching, Journal of the ACM 39(2) (1992)
    locator: pp. 430 to 448 (a speedup by a logarithmic factor of the simulation of the automaton of a regular expression)
---

NFA membership is the problem of deciding whether a given [nondeterministic finite automaton](/nondeterministic-finite-automaton/) accepts a given string. [NFA simulation](/nfa-simulation/) solves it in $O(\ell (n + m))$ time for a string of length $\ell$ and an NFA with $n$ states and $m$ transitions, by following the set of active states. Under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) this product of the two sizes cannot be improved by a polynomial factor in general. Every regular expression matcher solves this problem or its search version.

## In plain words

An NFA is a map of states and arrows, where a letter can lead from one state along several arrows. A string is accepted when at least one walk that spells the string ends in an accepting state. The question is: does such a walk exist for this one string?

Trying the walks one by one can take a very long time, because the number of walks can double with each letter. The good method keeps the set of all states that some walk can be in after each letter. The set never has more states than the automaton, so each letter costs a fixed amount of work for a fixed automaton. At the end, the answer is yes when the set holds an accepting state.

## Definition

**Input.** An NFA $N = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to \mathcal{P}(Q)$, as on the [NFA](/nondeterministic-finite-automaton/) page, and a string $w = a_1 \cdots a_\ell \in \Sigma^*$. The size of $N$ is given by $n = |Q|$ and $m = \sum_{q, a} |\delta(q, a)|$.

**Output.** Yes if $w \in L(N)$, that is, if there are states $r_0, \ldots, r_\ell$ with $r_0 = q_0$, $r_i \in \delta(r_{i-1}, a_i)$ for $1 \le i \le \ell$, and $r_\ell \in F$. No otherwise.

The problem allows $\varepsilon$-moves in the general form: then the input is an [epsilon-NFA](/epsilon-nfa/), and a run may take any number of $\varepsilon$-moves between two symbols. The bounds below hold for both forms, with $m$ counting the $\varepsilon$-moves too.

## Variants

- **DFA membership.** For a [DFA](/deterministic-finite-automaton/) the run is unique, and $\ell$ table lookups decide membership.
- **Regular expression membership.** The input is a [regular expression](/regular-expression/) instead of an NFA. This is [regex matching](/regex-matching/). The [Thompson construction](/thompson-construction/) reduces it to NFA membership with $O(k)$ states and transitions for an expression of length $k$.
- **Search.** Decide whether some substring of $w$ is in $L(N)$, or report the positions where a match ends. This is [regex search](/regex-search/). A self-loop on every symbol at the start state turns it into membership of the prefixes of $w$.
- **Fixed automaton.** When $N$ is fixed and only $w$ is input, convert $N$ once to a DFA with the [subset construction](/subset-construction/). Then each string costs $O(\ell)$ time, with a constant that can be exponential in $n$.
- **Counting runs.** Count the accepting runs on $w$. The same dynamic program over the states, with counts in place of a set, takes $O(\ell (n + m))$ arithmetic operations. An [unambiguous NFA](/unambiguous-nfa/) has at most one accepting run on each string.

## Examples

Let $N$ accept the strings over $\{a, b\}$ that end in $abb$: $Q = \{0, 1, 2, 3\}$, $q_0 = 0$, $F = \{3\}$, $\delta(0, a) = \{0, 1\}$, $\delta(0, b) = \{0\}$, $\delta(1, b) = \{2\}$, $\delta(2, b) = \{3\}$, and all other sets empty.

| string | sets of active states after each symbol | answer |
|---|---|---|
| $aabb$ | $\{0\}, \{0,1\}, \{0,1\}, \{0,2\}, \{0,3\}$ | yes |
| $abab$ | $\{0\}, \{0,1\}, \{0,2\}, \{0,1\}, \{0,2\}$ | no |
| $babb$ | $\{0\}, \{0\}, \{0,1\}, \{0,2\}, \{0,3\}$ | yes |
| $abbabb$ | $\{0\}, \{0,1\}, \{0,2\}, \{0,3\}, \{0,1\}, \{0,2\}, \{0,3\}$ | yes |
| $\varepsilon$ | $\{0\}$ | no |

**Many runs.** Let $N'$ have the states 0 and 1, both non-accepting, $\delta(q, a) = \{0, 1\}$ for both states and $\delta(q, c) = \emptyset$. On $a^{20}$ it has $2^{20} = 1{,}048{,}576$ runs. A search that tries the runs one at a time on $a^{20} c$ explores all of them before it answers no. The set of active states is $\{0, 1\}$ after each $a$ and $\emptyset$ after the $c$, so the set method takes 21 steps.

## Known algorithms

- [NFA simulation](/nfa-simulation/): follow the set of active states, with the [epsilon-closure](/epsilon-closure/) after each step. $O(\ell (n + m))$ time and $O(n)$ extra space. [Thompson's NFA simulation](/thompson-nfa-simulation/) is the same method on the automaton of a regular expression (Thompson, 1968).
- [Subset construction](/subset-construction/) followed by a DFA run: $O(\ell)$ time for the run, after a construction that can take $\Theta(2^n)$ time and space.
- [Lazy DFA construction](/lazy-dfa-construction/): build only the subsets that the input reaches, and keep them in a cache. A step that finds its subset in the cache costs one lookup, and a new subset costs one simulation step.
- [Bit-parallel regex matching](/bit-parallel-regex-matching/): store the set of active states in machine words of $w$ binary digits. For the automata of regular expressions, such as the [Glushkov automaton](/glushkov-automaton/), one step costs about $O(\lceil n / w \rceil)$ word operations plus table lookups.
- [Backtracking](/backtracking-regex-matching/): try the runs one at a time. Exponential time in the worst case, as in the example above. It is used because it extends to backreferences, which are not regular.

## Bounds

**Upper bound.** $O(\ell (n + m))$ time on the [word RAM](/word-ram/), by NFA simulation. Since $m \ge n - 1$ for an NFA whose states are all reachable, this is $O(\ell m)$ after the unreachable states are removed. For the automata of regular expressions, Myers (1992) saves a logarithmic factor with the [Four Russians method](/four-russians-method/).

**Lower bound by reading.** Each algorithm must read $w$ and, in the worst case, all of $N$, so $\Omega(\ell + n + m)$ time is necessary.

**Conditional lower bound.** Backurs and Indyk (2016) showed that, if the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) holds, then for some fixed kinds of regular expressions no algorithm decides membership in $O((\ell k)^{1 - \varepsilon})$ time for any $\varepsilon > 0$, where $k$ is the length of the expression. The Thompson construction maps an expression of length $k$ to an NFA with $O(k)$ states and transitions in linear time, so the same bound holds for NFA membership in terms of $\ell m$. See [the Backurs-Indyk hardness result](/backurs-indyk-regex-hardness/).

**Space.** NFA membership, with both $N$ and $w$ as input, is complete for [NL](/nondeterministic-logspace/) under logspace reductions. It is in NL: guess a run one state at a time, and keep only the current state and the position in $w$, which takes $O(\log n + \log \ell)$ space. It is NL-hard because directed reachability, which is NL-complete (Jones, 1975), reduces to it: for a graph $G$ with $V$ vertices and vertices $s$ and $t$, make an NFA over $\{a\}$ with one state per vertex, an $a$-transition for each edge, a self-loop on $t$, the start state $s$ and $F = \{t\}$. It accepts $a^{V}$ if and only if $t$ is reachable from $s$, because a path of length at most $V - 1$ can be padded with the loop at $t$.

## Reductions

- **To reachability.** $w \in L(N)$ if and only if some vertex $(f, \ell)$ with $f \in F$ is reachable from $(q_0, 0)$ in the layered graph with vertices $Q \times \{0, \ldots, \ell\}$ and an edge $(q, i - 1) \to (r, i)$ for each $r \in \delta(q, a_i)$. This graph has $O(\ell (n + m))$ vertices and edges, and a search of it is NFA simulation.
- **From reachability.** The unary construction of the Bounds section.
- **From regex matching.** By the Thompson construction or the Glushkov automaton, in linear time.

## Applications

- Regular expression search in tools such as [grep](/grep/), and in the regex libraries that guarantee linear time.
- Lexical analysis, where the NFA of all token patterns is built once and determinized.
- Input validation against a regular schema, such as a format of dates or identifiers.
- Checking a trace of a system against a property given as an automaton in runtime verification.

## References
