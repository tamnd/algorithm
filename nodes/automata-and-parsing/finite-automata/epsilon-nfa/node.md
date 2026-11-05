---
tag: Z7MJGZ
kind: model
slug: epsilon-nfa
name: Epsilon-NFA
aliases:
- NFA with epsilon-transitions
- epsilon-NFA
- lambda-NFA
area: automata-and-parsing/finite-automata
level: core
summary: NFA that also allows moves on the empty string without consuming input.
prereqs: [nondeterministic-finite-automaton]
see_also: [epsilon-closure, thompson-construction, subset-construction, kleene-theorem, thompson-nfa-simulation, deterministic-finite-automaton, glushkov-automaton, nfa-simulation]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 2.5, Finite Automata With Epsilon-Transitions (epsilon-closures, the extended transition function, and the elimination of epsilon-transitions)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.2, Nondeterminism (the NFA with epsilon moves and Theorem 1.39, the equivalence with DFAs)
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, Regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125 (nondeterministic automata and the subset construction)
---

An epsilon-NFA is a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) that may also change its state without reading an input symbol, along a transition labelled with the empty string $\varepsilon$. These moves make it easy to glue automata together, which is why the [Thompson construction](/thompson-construction/) builds an epsilon-NFA from a regular expression. Epsilon-NFAs accept exactly the [regular languages](/regular-language/): the $\varepsilon$-moves can be removed without adding states, and the [subset construction](/subset-construction/) with [epsilon-closures](/epsilon-closure/) gives a [DFA](/deterministic-finite-automaton/).

## The machine

An epsilon-NFA is a tuple $N = (Q, \Sigma, \delta, q_0, F)$, where $Q$ is a finite set of states, $\Sigma$ is a finite alphabet with $\varepsilon \notin \Sigma$, $q_0 \in Q$ is the start state, $F \subseteq Q$ is the set of accepting states, and

$$\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to 2^Q$$

is the transition function. The value $\delta(q, x)$ is the set of possible next states, and it may be empty. So the machine need not be complete: a missing move means that this branch of the computation stops. The $\varepsilon$-moves are allowed, and they are the only difference from an NFA. An NFA is an epsilon-NFA with $\delta(q, \varepsilon) = \emptyset$ for each $q$.

**Epsilon-closure.** The [epsilon-closure](/epsilon-closure/) $\mathrm{Cl}(S)$ of a set $S \subseteq Q$ is the set of states that can be reached from a state of $S$ by zero or more $\varepsilon$-moves. It is the least set that contains $S$ and contains $\delta(p, \varepsilon)$ for each of its members $p$.

**The extended transition function.** For $S \subseteq Q$ and $w \in \Sigma^*$ define

$$\hat\delta(S, \varepsilon) = \mathrm{Cl}(S), \qquad \hat\delta(S, wa) = \mathrm{Cl}\Big(\bigcup_{p \in \hat\delta(S, w)} \delta(p, a)\Big) \quad (a \in \Sigma).$$

The machine accepts $w$ if $\hat\delta(\{q_0\}, w) \cap F \neq \emptyset$, and $L(N)$ is the set of strings that it accepts.

**Paths.** The same language has a definition by paths. A path is a sequence of transitions $p_0 \xrightarrow{x_1} p_1 \xrightarrow{x_2} \cdots \xrightarrow{x_m} p_m$ with $x_t \in \Sigma \cup \{\varepsilon\}$ and $p_t \in \delta(p_{t-1}, x_t)$, and its label is $x_1 \cdots x_m$, where each $\varepsilon$ adds nothing. Then $\hat\delta(\{q_0\}, w)$ is the set of the last states of the paths from $q_0$ with label $w$. The proof is an induction on $|w|$: a path with label $wa$ is a path with label $w$, then one transition on $a$, then a path of $\varepsilon$-moves, and the closure in the definition adds exactly these last $\varepsilon$-moves. Lemma 2 of [the proof of Kleene's theorem](/kleene-theorem/) writes out this induction.

A run can take any number of $\varepsilon$-moves between two symbols, and an $\varepsilon$-cycle does not make it run forever, because the closure is a finite set.

**Example.** Let $\Sigma = \{a, b, c\}$, $Q = \{0, 1, 2\}$, $q_0 = 0$ and $F = \{2\}$, with the transitions $\delta(0, a) = \{0\}$, $\delta(1, b) = \{1\}$, $\delta(2, c) = \{2\}$, $\delta(0, \varepsilon) = \{1\}$ and $\delta(1, \varepsilon) = \{2\}$, and all other values empty. The closures are $\mathrm{Cl}(\{0\}) = \{0, 1, 2\}$, $\mathrm{Cl}(\{1\}) = \{1, 2\}$ and $\mathrm{Cl}(\{2\}) = \{2\}$. The language is $a^* b^* c^*$.

| input read | $\hat\delta(\{0\}, \cdot)$ |
|---|---|
| $\varepsilon$ | $\{0, 1, 2\}$ |
| $a$ | $\{0, 1, 2\}$ |
| $ab$ | $\{1, 2\}$ |
| $abc$ | $\{2\}$ |

The last set meets $F$, so $abc$ is accepted. On $ba$ the sets are $\{0, 1, 2\}$, $\{1, 2\}$ and $\emptyset$, so $ba$ is rejected.

## What it counts

A run is a sequence of moves. A move on a symbol reads one input symbol, and an $\varepsilon$-move reads nothing, so the number of moves of one branch is not bounded by the input length. For this reason the cost of an epsilon-NFA is measured by a simulation, not by the moves of one branch. The usual simulation keeps the set $\hat\delta(\{q_0\}, w)$ for the prefix $w$ read so far. One step of it reads one symbol, applies $\delta$ to each state of the set and takes the epsilon-closure. With $n$ states and $t$ transitions, a step takes $O(n + t)$ time on the [word RAM](/word-ram/), and the space is $O(n)$ for the set. See [NFA simulation](/nfa-simulation/) and [Thompson NFA simulation](/thompson-nfa-simulation/).

The size of an epsilon-NFA is its number of states $n$, and sometimes its number of transitions $t$, which is at most $n^2(|\Sigma| + 1)$.

## Relation to other models

- **NFAs.** Each NFA is an epsilon-NFA. Conversely, an epsilon-NFA with $n$ states becomes an NFA with the same $n$ states and the same start state: let $\delta'(q, a) = \mathrm{Cl}\big(\bigcup_{p \in \mathrm{Cl}(\{q\})} \delta(p, a)\big)$ and $F' = \{ q : \mathrm{Cl}(\{q\}) \cap F \neq \emptyset \}$. Each path of the epsilon-NFA with a non-empty label $a_1 \cdots a_k$ becomes a path of $k$ moves of the NFA, so the two machines accept the same strings. The number of transitions can grow from $O(n)$ to $\Theta(n^2)$ for one symbol. In the example above this gives $\delta'(0, a) = \{0, 1, 2\}$, $\delta'(0, b) = \delta'(1, b) = \{1, 2\}$, $\delta'(q, c) = \{2\}$ for each $q$, and $F' = \{0, 1, 2\}$.
- **DFAs.** The [subset construction](/subset-construction/) with closures gives a DFA with at most $2^n$ states: its start state is $\mathrm{Cl}(\{q_0\})$ and its transition on $a$ maps $S$ to $\hat\delta(S, a)$.
- **Regular expressions.** By [Kleene's theorem](/kleene-theorem/), epsilon-NFAs and regular expressions describe the same languages. The [Thompson construction](/thompson-construction/) gives an epsilon-NFA with at most $2s$ states for an expression of size $s$. The [Glushkov automaton](/glushkov-automaton/) is an NFA without $\varepsilon$-moves of a similar size.
- **Other machines.** The $\varepsilon$-move is also used in [pushdown automata](/pushdown-automaton/) and in [finite-state transducers](/finite-state-transducer/), where a move may read nothing and write output.

## Known results in the model

Here $n$ is the number of states, $t$ the number of transitions and $\sigma = |\Sigma|$.

- **Expressive power.** Epsilon-NFAs accept exactly the regular languages ([Kleene's theorem](/kleene-theorem/)). The $\varepsilon$-moves add no power and cost no states, only transitions.
- **Closure constructions.** Union, concatenation and star take $O(1)$ new states and $\varepsilon$-moves each, as in the proof of Kleene's theorem. This is the main use of the model. See [closure properties](/closure-properties-of-regular-languages/).
- **Membership.** Deciding $w \in L(N)$ takes $O(|w| (n + t))$ time by the set simulation.
- **Emptiness.** $L(N) \neq \emptyset$ if and only if a state of $F$ is reachable from $q_0$ along any transitions, which a graph search decides in $O(n + t)$ time. See [DFA emptiness](/dfa-emptiness/).
- **Determinization.** The subset construction gives at most $2^n$ states, and some epsilon-NFAs, even NFAs without $\varepsilon$-moves, need all of them. See the [determinization blow-up lower bound](/determinization-blowup-lower-bound/).
- **Universality and equivalence.** Deciding $L(N) = \Sigma^*$ is PSPACE-complete, and so is deciding the equivalence of two epsilon-NFAs. See [NFA universality](/nfa-universality/) and [NFA equivalence](/nfa-equivalence/).

### Pitfalls

- **Closure at the start.** The start set is $\mathrm{Cl}(\{q_0\})$, not $\{q_0\}$. A simulation that forgets it rejects $c$ in the example above, since $\delta(0, c) = \emptyset$.
- **Closure after each symbol, not before only.** Taking the closure before a symbol move and not after it loses the states that the last $\varepsilon$-moves reach. In the example, $\{0\}$ after $a$ must become $\{0, 1, 2\}$, or $ab$ is rejected.
- **Accepting states after removal.** When $\varepsilon$-moves are removed, a state whose closure meets $F$ must become accepting. In the example, state 0 must accept, or the empty string is lost.
- **Epsilon-cycles.** A closure computed by a naive recursion can loop on an $\varepsilon$-cycle. Mark the states that are already in the set.

## References
