---
tag: MPAC3F
kind: problem
slug: dfa-finiteness
name: DFA finiteness
aliases:
- finiteness of regular language
area: automata-and-parsing/finite-automata
level: core
summary: Decide whether the language of a DFA is finite, by looking for a cycle on a path to an accepting state.
model: word-ram
complexity:
  vars: {n: the number of states, σ: the alphabet size}
  time: {worst: O(nσ)}
prereqs: [dfa-emptiness, cycle-detection-in-graph, pumping-lemma-for-regular-languages]
see_also: [dfa-emptiness, dfa-equivalence, depth-first-search, topological-sort, strongly-connected-components, regular-language, nondeterministic-logspace, state-complexity]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.3, Decision Properties of Regular Languages, and the exercises of Section 4.3 on testing whether a regular language is infinite
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, first edition, 1979
    locator: Section 3.3, Decision Algorithms for Regular Sets (Theorem 3.7, a language is infinite if and only if it has a word of length between n and 2n - 1)
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125 (the decidability of emptiness and finiteness)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (a directed graph is acyclic if and only if a depth-first search finds no back edge)
---

DFA finiteness asks whether a [deterministic finite automaton](/deterministic-finite-automaton/) accepts only finitely many strings. The language is infinite exactly when some cycle of the transition graph lies on a path from the start state to an accepting state. So the test keeps the *useful* states, which are reachable from the start and can reach an accepting state, and looks for a cycle among them with a [depth-first search](/depth-first-search/) or a [topological sort](/topological-sort/). It takes $O(n\sigma)$ time. A cycle that is not on such a path, for example a loop on a dead state, does not count.

## In plain words

An automaton is a map of states joined by arrows with letters. An accepted word is a walk from the start to an accepting state. If such a walk can pass through a loop, then it can go around the loop once, twice, or as many times as we like, and each choice spells a different accepted word. So the automaton accepts infinitely many words.

If no walk from the start to an accepting state can meet a loop, then every such walk visits each state at most once, so it is short, and there are only finitely many of them. The test therefore throws away the states that are never reached and the states from which no accepting state can be reached. Then it checks whether the states that remain contain a loop.

## Definition

**Input.** A complete DFA $M = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to Q$ and no $\varepsilon$-moves, with $n = |Q|$ and $\sigma = |\Sigma|$.

**Output.** "Finite" if $L(M)$ is a finite set, and "infinite" otherwise.

A state $q$ is *useful* if $q = \delta^*(q_0, x)$ for some $x$ and $\delta^*(q, z) \in F$ for some $z$. Let $G_U$ be the subgraph of the transition graph on the useful states, with an edge $q \to \delta(q, a)$ when both ends are useful.

**Characterization.** $L(M)$ is infinite if and only if $G_U$ has a cycle.

*Proof.* Suppose $G_U$ has a cycle through $q$, with the label $y \neq \varepsilon$, so $\delta^*(q, y) = q$. Since $q$ is useful, some $x$ and $z$ have $\delta^*(q_0, x) = q$ and $\delta^*(q, z) \in F$. Then $\delta^*(q_0, x y^k z) = \delta^*(q, z) \in F$ for each $k \ge 0$, by the lemma $\delta^*(p, uv) = \delta^*(\delta^*(p, u), v)$. These strings have different lengths, so $L(M)$ is infinite.

Conversely, suppose $L(M)$ is infinite. It has a string $w$ with $|w| \ge n$. The run of $M$ on $w$ visits $|w| + 1 > n$ states, so some state repeats: $r_i = r_j$ with $i < j$. Each state of the run is reachable (by a prefix of $w$) and reaches $F$ (by the rest of $w$), so it is useful, and the part of the run from $r_i$ to $r_j$ is a cycle of $G_U$. $\square$

**A bounded-length form.** $L(M)$ is infinite if and only if it contains a string $w$ with $n \le |w| \le 2n - 1$. The "if" part is the argument above. For "only if", take a shortest $w \in L(M)$ with $|w| \ge n$, and suppose $|w| \ge 2n$. Among the first $n + 1$ states of its run, two are equal, $r_i = r_j$ with $0 \le i < j \le n$. Removing the symbols $i + 1, \ldots, j$ gives a string in $L(M)$ of length $|w| - (j - i) \ge 2n - n = n$, which is shorter than $w$: a contradiction. This form gives a simple but exponential test, by trying all strings of these lengths.

**The finite case.** If $L(M)$ is finite, every accepted string has length at most $n - 1$, since a longer one would make $L(M)$ infinite by the argument above.

## Variants

- **Counting.** If $L(M)$ is finite, $|L(M)|$ is the number of paths from $q_0$ to $F$ in the acyclic graph $G_U$, counted with their labels. A dynamic program in reverse topological order computes it in $O(n\sigma)$ arithmetic operations. The count can be as large as about $\sigma^{n-1}$, so the numbers need $O(n \log \sigma)$ digits.
- **The longest word.** In the finite case, the longest accepted string is a longest path in the acyclic graph $G_U$, found by the same dynamic program.
- **NFAs and epsilon-NFAs.** For an [NFA](/nondeterministic-finite-automaton/) the same test works on the graph of all transitions. For an [epsilon-NFA](/epsilon-nfa/), a cycle made only of $\varepsilon$-moves adds no new strings, so the test must look for a useful cycle that reads at least one symbol, for example within one [strongly connected component](/strongly-connected-components/) that has a symbol edge inside it.
- **Cofiniteness.** $L(M)$ is cofinite (its complement is finite) if and only if the DFA with $F$ replaced by $Q \setminus F$ has a finite language.
- **Finiteness of other descriptions.** For a regular expression, a bottom-up pass decides finiteness: a star of a language that contains a non-empty string is infinite. For context-free grammars, finiteness is also decidable by a cycle test on the useful nonterminals.

## Examples

Let $\Sigma = \{a, b\}$, $Q = \{0, 1, 2, 3, 4\}$, $q_0 = 0$, with this table:

| $\delta$ | $a$ | $b$ |
|---|---|---|
| 0 | 1 | 3 |
| 1 | 2 | 2 |
| 2 | 4 | 4 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |

The only cycles are the loops at 3 and at 4.

- **$F = \{2\}$: finite.** The useful states are 0, 1 and 2. States 3 and 4 have loops, but they cannot reach $F$, so they are not useful. The graph on $\{0, 1, 2\}$ has no cycle, and $L(M) = \{aa, ab\}$.
- **$F = \{2, 3\}$: infinite.** Now 3 is useful and has a loop. The strings $b$, $ba$, $bab$, and so on are all accepted.
- **$F = \{4\}$: infinite.** State 4 is useful and has a loop, and $L(M)$ is the set of strings of length at least 3 that start with $a$.
- **$F = \{0, 1, 2\}$: finite.** $L(M) = \{\varepsilon, a, aa, ab\}$, so $|L(M)| = 4$.

A script listed the accepted strings up to length 9 for each $F$: 2 strings, 513 strings, 508 strings and 4 strings.

## Known algorithms

- **Trim, then detect a cycle.** A [breadth-first search](/breadth-first-search/) from $q_0$ finds the reachable states, and a search from $F$ along reversed edges finds the states that reach $F$. Their intersection is the set of useful states. Then a [depth-first search](/depth-first-search/) on $G_U$ finds a back edge if and only if there is a cycle ([cycle detection](/cycle-detection-in-graph/)), or Kahn's [topological sort](/topological-sort/) removes vertices of in-degree 0 and fails to remove them all if and only if there is a cycle. Each step takes $O(n\sigma)$ time. An iterative search avoids deep recursion on long chains of states.
- **Strongly connected components.** Compute the components of the graph of useful states with [Tarjan's algorithm](/tarjan-scc/). The language is infinite if and only if some component has more than one state or a self-loop.
- **Minimize first.** In the minimal DFA every state is reachable and at most one state, the dead state, cannot reach $F$. So the language is infinite if and only if the minimal DFA without its dead state has a cycle.

## Bounds

**Upper bound.** $O(n\sigma)$ time and $O(n\sigma)$ space for the reversed edges, on the [word RAM](/word-ram/).

**Lower bound.** $\Omega(n\sigma)$ table entries must be read on some inputs. Take the adversary of [DFA emptiness](/dfa-emptiness/), with an accepting sink $n - 1$ that has a loop on each symbol. The language is empty, and so finite, until one unread entry is redirected to $n - 1$; then it is infinite.

**Space.** Infiniteness is in [NL](/nondeterministic-logspace/): guess a useful state, a cycle through it, a path to it from $q_0$ and a path from it to $F$. Finiteness is then in NL by the Immerman-Szelepcsényi theorem. Both are NL-hard: given a directed graph with out-degree at most 2 and vertices $s$ and $t$, build the DFA of the [emptiness](/dfa-emptiness/) page, and make $t$ accepting with a loop on each symbol. If $s$ reaches $t$, then $t$ is useful and the language is infinite. If not, the language is empty. So the language is infinite if and only if $s$ reaches $t$.

## Reductions

- **To cycle detection** on the useful part of the graph, by the characterization.
- **From reachability**, as in the Bounds section.
- **From emptiness.** $L(M)$ is non-empty if and only if $L(M)\,\Sigma^*$ is infinite, and a DFA for $L(M)\Sigma^*$ is $M$ with each accepting state made a sink with loops.

## Applications

- **Dictionaries and word lists.** A DFA that should encode a finite word list can be checked for accidental cycles, and its words can be enumerated or counted in the finite case.
- **Bounded languages in testing.** Test generators that enumerate all strings of a regular language need it to be finite, or need a length bound.
- **Grammar and regex analysis.** Linters warn when a pattern that should match finitely many strings, such as a set of keywords, has a reachable loop.
- **Theory.** The test is the standard example, after emptiness, of a decidable property of regular languages. The same idea, a cycle on a useful path, decides finiteness for context-free grammars, and it underlies the emptiness test for [Büchi automata](/buchi-automaton/), where an accepting state must lie on a reachable cycle.

## References
