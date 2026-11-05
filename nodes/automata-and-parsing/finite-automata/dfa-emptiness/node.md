---
tag: 8JA7E6
kind: problem
slug: dfa-emptiness
name: DFA emptiness
aliases:
- language emptiness problem
area: automata-and-parsing/finite-automata
level: intro
summary: Decide whether an automaton accepts any string, by checking reachability of an accepting state.
model: word-ram
complexity:
  vars: {n: the number of states, σ: the alphabet size}
  time: {worst: O(nσ)}
prereqs: [deterministic-finite-automaton, graph-reachability, breadth-first-search]
see_also: [dfa-finiteness, dfa-equivalence, nfa-universality, regex-emptiness, reachability, product-construction, nondeterministic-logspace, automata-theoretic-approach]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 4.1, Decidable Languages (Theorem 4.4, the emptiness problem for DFAs, and Theorem 4.5, equivalence by emptiness of the symmetric difference)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.3, Decision Properties of Regular Languages (testing emptiness)
  - paper: doi:10.1016/S0022-0000(75)80050-X
    title: Neil D. Jones, Space-bounded reducibility among combinatorial problems, Journal of Computer and System Sciences 11(1) (1975)
    locator: pp. 68 to 85 (the NL-completeness of directed reachability)
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125 (the decision problems for finite automata)
  - paper: "Dexter Kozen, Lower bounds for natural proof systems, 18th Annual Symposium on Foundations of Computer Science (FOCS 1977)"
    locator: pp. 254 to 266 (the PSPACE-completeness of the emptiness of an intersection of finite automata)
---

DFA emptiness is the problem of deciding whether a [deterministic finite automaton](/deterministic-finite-automaton/) accepts at least one string. The language is non-empty exactly when some accepting state is reachable from the start state, so the problem is [graph reachability](/graph-reachability/) on the transition graph, and a [breadth-first search](/breadth-first-search/) solves it in time linear in the size of the transition table. It is the basic step of many other decisions: [equivalence](/dfa-equivalence/), inclusion and universality all reduce to it.

## In plain words

An automaton is a map of states joined by arrows, and each arrow carries a letter. A word is accepted when you can follow its letters from the start state and end on an accepting state. So the automaton accepts some word exactly when you can walk from the start to an accepting state along the arrows, in any way at all. The letters do not matter for this question, only the arrows.

To answer it, explore the map from the start: visit each state once and follow each arrow once. If you meet an accepting state, the letters on your path spell a word that the automaton accepts. If the search ends without one, the automaton accepts nothing. An accepting state that the search never reaches does not count.

## Definition

**Input.** A DFA $M = (Q, \Sigma, \delta, q_0, F)$ with a complete transition function $\delta : Q \times \Sigma \to Q$ and no $\varepsilon$-moves, given as a table of $n \cdot \sigma$ entries, where $n = |Q|$ and $\sigma = |\Sigma|$.

**Output.** "Empty" if $L(M) = \emptyset$, and "non-empty" otherwise. The search version also outputs a witness $w \in L(M)$ when one exists.

**The characterization.** Let $R = \{ \delta^*(q_0, w) : w \in \Sigma^* \}$ be the set of reachable states. Then

$$L(M) \neq \emptyset \iff R \cap F \neq \emptyset.$$

*Proof.* If $w \in L(M)$, then $\delta^*(q_0, w) \in F$, and this state is in $R$ by the definition of $R$. If $f \in R \cap F$, some $w$ has $\delta^*(q_0, w) = f \in F$, so $w \in L(M)$. $\square$

In the transition graph, $R$ is the set of vertices that a walk from $q_0$ can reach, and a walk with labels $a_1 \cdots a_k$ from $q_0$ ends in $\delta^*(q_0, a_1 \cdots a_k)$.

**Short witnesses.** If $L(M) \neq \emptyset$, then $L(M)$ contains a string of length at most $n - 1$. Take a shortest $w \in L(M)$. If its run $r_0, \ldots, r_{|w|}$ visits a state twice, say $r_i = r_j$ with $i < j$, then removing the symbols $a_{i+1} \cdots a_j$ gives a shorter string with the same last state, which is a contradiction. So the run visits $|w| + 1$ different states, and $|w| + 1 \le n$.

## Variants

- **Non-emptiness with a witness.** Return a shortest string in $L(M)$. A breadth-first search that records the parent of each state gives it, and its length is the distance from $q_0$ to the nearest accepting state.
- **NFA and epsilon-NFA emptiness.** For a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) or an [epsilon-NFA](/epsilon-nfa/) the same characterization holds, with all transitions as edges. The time is linear in the number of states and transitions. No determinization is needed.
- **Universality.** $L(M) = \Sigma^*$ if and only if the complement DFA, with $F$ replaced by $Q \setminus F$, is empty. So DFA universality is as easy as emptiness. For NFAs, universality is PSPACE-complete: see [NFA universality](/nfa-universality/).
- **Intersection emptiness.** Given DFAs $M_1, \ldots, M_k$, decide whether $L(M_1) \cap \cdots \cap L(M_k) = \emptyset$. For a fixed $k$, a search of the [product construction](/product-construction/) takes $O(\sigma \prod_i n_i)$ time. When $k$ is part of the input, the problem is PSPACE-complete (Kozen, 1977).
- **Emptiness of a regular expression.** See [regex emptiness](/regex-emptiness/). The test is one bottom-up pass over the expression: $\emptyset$ is empty, a symbol and $\varepsilon$ are not, a concatenation is empty when one of its parts is, a union is empty when both of its parts are, and a star is never empty.
- **Emptiness for infinite words.** For a [Büchi automaton](/buchi-automaton/), the language is non-empty if and only if some accepting state is reachable and lies on a cycle.

## Examples

Let $\Sigma = \{a, b\}$, $Q = \{0, 1, 2, 3, 4, 5\}$ and $q_0 = 0$, with this table:

| $\delta$ | $a$ | $b$ |
|---|---|---|
| 0 | 1 | 0 |
| 1 | 1 | 2 |
| 2 | 3 | 0 |
| 3 | 3 | 3 |
| 4 | 5 | 4 |
| 5 | 4 | 5 |

- **$F = \{3\}$: non-empty.** A breadth-first search from 0 visits 0, 1, 2, 3 in this order and stops at 3. The parents give the path $0 \xrightarrow{a} 1 \xrightarrow{b} 2 \xrightarrow{a} 3$, so the witness is $aba$. States 0 to 3 track how much of $aba$ the input ends with, and $L(M)$ is the set of strings that contain $aba$.
- **$F = \{5\}$: empty.** The search visits 0, 1, 2, 3 and stops. State 5 is accepting but not reachable, so $L(M) = \emptyset$. A test that checks only "$F \neq \emptyset$" gives the wrong answer here.
- **$F = \{2, 5\}$: non-empty.** The search reaches 2 first, with the witness $ab$ of length 2, which is a shortest accepted string.
- **$F = \emptyset$.** The language is empty without a search.

## Known algorithms

- **Graph search.** A [breadth-first search](/breadth-first-search/) or a [depth-first search](/depth-first-search/) from $q_0$ over the edges $q \to \delta(q, a)$ visits each reachable state once and reads each of its $\sigma$ entries once. It stops at the first accepting state or when the reachable set is complete. Time $O(n\sigma)$, space $O(n)$ for the visited marks. The breadth-first version gives a shortest witness.
- **Logarithmic space.** Guess a walk of length at most $n - 1$ one state at a time, with a counter. This puts non-emptiness in [nondeterministic logspace](/nondeterministic-logspace/). By the [Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/), emptiness is in NL too, and by [Savitch's theorem](/savitch-theorem/) both are in deterministic space $O(\log^2 n)$.
- **Inside a larger test.** [DFA equivalence](/dfa-equivalence/) searches the product of two DFAs for a pair of states where one accepts and the other rejects. [DFA finiteness](/dfa-finiteness/) adds a cycle test on the useful states.

## Bounds

**Upper bound.** $O(n\sigma)$ time on the [word RAM](/word-ram/), which is linear in the size of the table.

**Lower bound.** Count the table entries that an algorithm reads. For $\sigma \ge 2$ and $n \ge 2$, every deterministic algorithm reads at least $(n - 1)\sigma - (n - 2)$ entries on some input, which is $\Omega(n\sigma)$.

*Proof.* Let $Q = \{0, \ldots, n-1\}$, $q_0 = 0$, $F = \{n - 1\}$, and let $a$ be one symbol. Fix the chain $\delta(i, a) = i + 1$ for $0 \le i \le n - 3$, and $\delta(n-1, c) = n - 1$ for each $c$. Call the other entries $\delta(q, c)$ with $q \le n - 2$ the free entries; there are $(n-1)\sigma - (n-2)$ of them. Give the algorithm the DFA $M_0$ in which every free entry is 0. In $M_0$ no edge enters $n - 1$ from another state, so $L(M_0) = \emptyset$. Suppose the algorithm stops on $M_0$ without reading the free entry $\delta(q, c)$. Let $M_1$ be $M_0$ with this one entry changed to $n - 1$. The chain makes $q$ reachable in $M_1$, so $L(M_1) \neq \emptyset$. The algorithm reads the same values on $M_1$ as on $M_0$, so it gives the same answer, and it is wrong on one of them. $\square$

**Space.** Non-emptiness of a DFA is NL-complete under logspace reductions. It is in NL by the algorithm above. For hardness, directed reachability is NL-complete (Jones, 1975), and it stays NL-complete for graphs where each vertex has at most two outgoing edges. Such a graph with source $s$ and target $t$ becomes a DFA over $\{a, b\}$: the vertices are the states, $s$ is the start state, $F = \{t\}$, each vertex sends $a$ and $b$ along its outgoing edges, and a missing edge is a self-loop. A walk from $s$ to $t$ exists exactly when the DFA accepts some string.

## Reductions

- **From DFA emptiness to reachability**, by the characterization: same graph, linear time.
- **From reachability to DFA non-emptiness**, by the construction in the Bounds section, in logarithmic space.
- **From DFA equivalence to emptiness.** $L(M_1) = L(M_2)$ if and only if the symmetric difference is empty. The product DFA with the accepting pairs $(F_1 \times (Q_2 \setminus F_2)) \cup ((Q_1 \setminus F_1) \times F_2)$ has $n_1 n_2$ states.
- **From inclusion to emptiness.** $L(M_1) \subseteq L(M_2)$ if and only if $L(M_1) \cap \overline{L(M_2)} = \emptyset$, again by the product.

## Applications

- **Model checking.** In the [automata-theoretic approach](/automata-theoretic-approach/), a system satisfies a property when the product of the system with an automaton for the bad behaviours is empty. A witness of non-emptiness is a counterexample trace. A [safety property](/safety-property/) uses finite-word automata as here.
- **Equivalence and inclusion checks** of lexers, protocol specifications and regular expressions, through the reductions above.
- **Dead-state removal.** A state $q$ is dead when the DFA with start state $q$ is empty. Removing dead and unreachable states is the first step of many constructions.

## References
