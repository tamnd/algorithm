---
tag: 8A5JRE
kind: concept
slug: epsilon-closure
name: Epsilon-closure
aliases:
- lambda-closure
area: automata-and-parsing/finite-automata
level: core
summary: Set of states reachable from a state using only empty-string transitions.
prereqs: [epsilon-nfa, graph-reachability]
see_also: [subset-construction, thompson-nfa-simulation, nfa-simulation, thompson-construction, depth-first-search, strongly-connected-components, transitive-closure, kleene-theorem]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 2.5.3, Epsilon-Closures, and Section 2.5.5, Eliminating Epsilon-Transitions
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.2, Nondeterminism (the set E(R) in the proof of Theorem 1.39)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 3.7.1, Conversion of an NFA to a DFA (the operations epsilon-closure(s), epsilon-closure(T) and move(T, a), and the stack algorithm for epsilon-closure)
---

The epsilon-closure of a set of states $S$ of an [epsilon-NFA](/epsilon-nfa/) is the set of states that can be reached from a state of $S$ by zero or more $\varepsilon$-moves, the moves that read no input. It is [graph reachability](/graph-reachability/) in the graph of the $\varepsilon$-moves alone, and a [depth-first search](/depth-first-search/) computes it in time linear in the size of that graph. The closure appears in each step of the [simulation](/nfa-simulation/) of an epsilon-NFA, in the [subset construction](/subset-construction/), and in the removal of $\varepsilon$-moves.

## In plain words

An automaton with empty moves can jump from one state to another without reading a letter. So when the machine is in some state, it is also, at no cost, in every state that it can reach by such jumps, then by more jumps from there, and so on. The closure of a state is this whole group of states.

To find it, start with the state itself, follow each empty move to a new state, and repeat from the new states. Keep a mark on the states that are already in the group, so that a loop of empty moves does not make the search go around forever. When no new state appears, the group is complete.

## The idea

Let $N = (Q, \Sigma, \delta, q_0, F)$ be an epsilon-NFA with $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to 2^Q$. The $\varepsilon$-graph $G_\varepsilon$ has the vertex set $Q$ and an edge $p \to r$ for each $r \in \delta(p, \varepsilon)$.

**Definition.** For $S \subseteq Q$, the epsilon-closure $\mathrm{Cl}(S)$ is the least set $C \subseteq Q$ such that $S \subseteq C$, and $\delta(p, \varepsilon) \subseteq C$ for each $p \in C$. Equivalently, $\mathrm{Cl}(S)$ is the set of vertices reachable in $G_\varepsilon$ from a vertex of $S$ by a path of length 0 or more. We write $\mathrm{Cl}(q)$ for $\mathrm{Cl}(\{q\})$.

The two definitions agree. The reachable set $R$ contains $S$ and is closed under the edges, so the least such set is a subset of $R$. Conversely, each set $C$ with the two properties contains every vertex of a path from $S$, by induction on the length of the path, so $R \subseteq C$.

**Properties.** For all $S, T \subseteq Q$:

- $S \subseteq \mathrm{Cl}(S)$ (extensive);
- $S \subseteq T$ implies $\mathrm{Cl}(S) \subseteq \mathrm{Cl}(T)$ (monotone);
- $\mathrm{Cl}(\mathrm{Cl}(S)) = \mathrm{Cl}(S)$ (idempotent), since $\mathrm{Cl}(S)$ already has the two properties of the definition;
- $\mathrm{Cl}(S \cup T) = \mathrm{Cl}(S) \cup \mathrm{Cl}(T)$, and so $\mathrm{Cl}(S) = \bigcup_{q \in S} \mathrm{Cl}(q)$, since a path starts at one vertex.

The first three properties make $\mathrm{Cl}$ a closure operator on the subsets of $Q$, which is the source of the name.

**Computing the closure of a set.** Push the states of $S$ on a stack and mark them. Pop a state $p$, and for each $r \in \delta(p, \varepsilon)$ that is not marked, mark $r$ and push it. Stop when the stack is empty; the marked states are $\mathrm{Cl}(S)$. Each state is pushed at most once because it is marked when pushed, so the loop ends. Each marked state is reachable from $S$, because it is in $S$ or was pushed along an edge from a marked state. Each reachable state is marked, by induction on the length of a shortest path from $S$: its predecessor on the path is marked, so it is pushed and popped, and the edge to the state is followed. The time is $O(|\mathrm{Cl}(S)| + t_\varepsilon(\mathrm{Cl}(S)))$, where $t_\varepsilon(C)$ is the number of $\varepsilon$-edges that leave $C$'s states; with all of $Q$ this is $O(n + t_\varepsilon)$ for $n$ states and $t_\varepsilon$ edges.

**Computing all the closures.** One search from each state takes $O(n(n + t_\varepsilon))$ time in total. All the states of one [strongly connected component](/strongly-connected-components/) of $G_\varepsilon$ have the same closure, so a faster way computes the components, contracts each one to a vertex, and takes the union of the closures of the successors in reverse topological order. This is the [transitive closure](/transitive-closure/) of $G_\varepsilon$, and its output can have $\Theta(n^2)$ pairs, for example on a path of $\varepsilon$-moves.

**The closure in the extended transition function.** The set of states that $N$ can be in after reading $w$ is

$$\hat\delta(S, \varepsilon) = \mathrm{Cl}(S), \qquad \hat\delta(S, wa) = \mathrm{Cl}\big(\mathrm{move}(\hat\delta(S, w), a)\big),$$

with $\mathrm{move}(T, a) = \bigcup_{p \in T} \delta(p, a)$. Two closures are needed: one at the start and one after each symbol. A closure before each symbol is then not needed, because each set $\hat\delta(S, w)$ is already closed.

## Examples

**A closure with a cycle.** Let $Q = \{0, 1, 2, 3, 4, 5\}$ with the $\varepsilon$-moves $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$ and $4 \to 5$.

| $q$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $\mathrm{Cl}(q)$ | $\{0,1,2,3\}$ | $\{0,1,2,3\}$ | $\{0,1,2,3\}$ | $\{3\}$ | $\{4,5\}$ | $\{5\}$ |

States 0, 1 and 2 form a strongly connected component, so they have the same closure. The stack algorithm from 0 pushes 0, pops it and pushes 1, pops 1 and pushes 2, pops 2, finds 0 marked and pushes 3, then pops 3. It stops after four pops. Also $\mathrm{Cl}(\{3, 4\}) = \{3, 4, 5\}$, the union of the two closures.

**A simulation step.** Take the epsilon-NFA for $a^* b^* c^*$ of the [epsilon-NFA](/epsilon-nfa/) page, with $\varepsilon$-moves $0 \to 1 \to 2$, loops $\delta(0, a) = \{0\}$, $\delta(1, b) = \{1\}$, $\delta(2, c) = \{2\}$, and $F = \{2\}$. The start set is $\mathrm{Cl}(0) = \{0, 1, 2\}$. On $b$, $\mathrm{move}(\{0, 1, 2\}, b) = \{1\}$ and $\mathrm{Cl}(\{1\}) = \{1, 2\}$. On a further $a$, $\mathrm{move}(\{1, 2\}, a) = \emptyset$, and the closure of the empty set is empty, so the string $ba$ is rejected.

**A non-example.** The set of states reachable by $\varepsilon$-moves *and* one symbol $a$ is not a closure: it is $\mathrm{Cl}(\mathrm{move}(\mathrm{Cl}(S), a))$, which is not extensive. In the second example, the state 0 is not in this set for $S = \{0\}$ and the symbol $b$.

## Where it is used

- **Simulation of an epsilon-NFA.** The [NFA simulation](/nfa-simulation/) and the [Thompson NFA simulation](/thompson-nfa-simulation/) apply the closure after each input symbol. With a [Thompson construction](/thompson-construction/) automaton, each state has at most two $\varepsilon$-moves, so a step takes $O(n)$ time.
- **The subset construction.** The [subset construction](/subset-construction/) for an epsilon-NFA uses $\mathrm{Cl}(q_0)$ as the start state and $\mathrm{Cl}(\mathrm{move}(S, a))$ as the transition, as in the step $2 \Rightarrow 3$ of [Kleene's theorem](/kleene-theorem/). The [lazy DFA construction](/lazy-dfa-construction/) computes these sets on demand.
- **Removal of $\varepsilon$-moves.** The NFA with $\delta'(q, a) = \mathrm{Cl}(\mathrm{move}(\mathrm{Cl}(q), a))$ and the accepting states $\{ q : \mathrm{Cl}(q) \cap F \neq \emptyset \}$ accepts the same language without $\varepsilon$-moves.
- **Compilers.** Lexer generators build their DFA by the subset construction with this closure. In parser generators, the closure of a set of [LR items](/lr-item-sets/) is the same kind of least fixed point.

## References
