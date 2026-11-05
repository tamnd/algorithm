---
tag: 7QKACH
kind: problem
slug: dfa-minimization
name: DFA minimization
aliases:
- minimal DFA construction
- state minimization
area: automata-and-parsing/finite-automata
level: core
summary: Given a DFA, compute the smallest DFA recognizing the same language.
model: word-ram
complexity:
  vars: {n: the number of states, σ: the alphabet size}
  time: {worst: O(σ n log n)}
prereqs: [deterministic-finite-automaton, myhill-nerode-relation, minimal-dfa-uniqueness]
see_also: [hopcroft-minimization, moore-minimization, brzozowski-minimization, table-filling-minimization, partition-refinement, dfa-equivalence, nfa-minimization, state-complexity]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.4, Equivalence and Minimization of Automata (the table-filling algorithm and the minimization of DFAs)
  - paper: "John E. Hopcroft, An n log n algorithm for minimizing states in a finite automaton, in Z. Kohavi and A. Paz (eds.), Theory of Machines and Computations, Academic Press, 1971"
    locator: pp. 189 to 196
  - paper: "Edward F. Moore, Gedanken-experiments on sequential machines, in C. E. Shannon and J. McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press, 1956"
    locator: pp. 129 to 153
  - paper: "Janusz A. Brzozowski, Canonical regular expressions and minimal state graphs for definite events, Symposium on the Mathematical Theory of Automata, Microwave Research Institute Symposia Series 12, Polytechnic Institute of Brooklyn, 1962"
    locator: pp. 529 to 561
  - paper: doi:10.1137/0216062
    title: Robert Paige and Robert E. Tarjan, Three partition refinement algorithms, SIAM Journal on Computing 16(6) (1987)
    locator: pp. 973 to 989
  - paper: doi:10.1016/0304-3975(92)90142-3
    title: Dominique Revuz, Minimisation of acyclic deterministic automata in linear time, Theoretical Computer Science 92(1) (1992)
    locator: pp. 181 to 189
---

DFA minimization asks for the smallest [deterministic finite automaton](/deterministic-finite-automaton/) that accepts the same language as a given one. The answer is unique up to the names of the states, by the [uniqueness of the minimal DFA](/minimal-dfa-uniqueness/), and it is found in two steps: remove the unreachable states, then merge the states that no input can tell apart. The second step is a [partition refinement](/partition-refinement/), and [Hopcroft's algorithm](/hopcroft-minimization/) does it in $O(\sigma n \log n)$ time for $n$ states and $\sigma$ symbols.

## In plain words

Two states of a machine are interchangeable when every possible rest of the input gets the same answer from both of them. Then the machine can keep one of them and send all arrows that went to the other one to it instead. A state that the machine can never reach from the start can simply be thrown away.

After both clean-ups, no smaller machine for the same set of words exists, and every smallest machine is the same one with different state names. The main work is to find which states are interchangeable. Start by splitting the states into accepting and rejecting ones. Then keep splitting a group whenever one letter sends its members into different groups. When no group splits any more, each group becomes one state.

## Definition

**Input.** A complete DFA $M = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to Q$ and no $\varepsilon$-moves, given as a table with $n \sigma$ entries, where $n = |Q|$ and $\sigma = |\Sigma|$.

**Output.** A complete DFA $M'$ with $L(M') = L(M)$ and the least possible number of states.

**Equivalent states.** States $p, q$ are equivalent, written $p \sim q$, if $\delta^*(p, z) \in F \Leftrightarrow \delta^*(q, z) \in F$ for each $z \in \Sigma^*$. This is an equivalence relation, and it is compatible with the transitions: $p \sim q$ implies $\delta(p, a) \sim \delta(q, a)$, by taking the suffixes $az$.

**The quotient.** Let $R$ be the set of reachable states. The quotient $M / {\sim}$ has the states $\{ [q] : q \in R \}$, the start state $[q_0]$, the transitions $[q] \xrightarrow{a} [\delta(q, a)]$ and the accepting states $\{ [q] : q \in F \cap R \}$. The transitions are well defined because $\sim$ is compatible with them, and the accepting states because equivalent states agree on $z = \varepsilon$. By induction on $|w|$, $[q_0]$ reaches $[\delta^*(q_0, w)]$ on $w$, so $L(M / {\sim}) = L(M)$. Its states are all reachable and pairwise not equivalent, so by Part 3 of the [uniqueness theorem](/minimal-dfa-uniqueness/) it is the minimal DFA. Its number of states is the index of the [Myhill-Nerode relation](/myhill-nerode-relation/) of $L(M)$.

**Characterization by stable partitions.** A partition $P$ of $R$ is *stable* if $p, q$ in one block imply $\delta(p, a), \delta(q, a)$ in one block for each $a$, and it *respects $F$* if each block lies in $F$ or in $R \setminus F$. The classes of $\sim$ form the coarsest partition that is stable and respects $F$. So minimization is the computation of a coarsest stable refinement of $\{F \cap R, R \setminus F\}$.

## Variants

- **Partial DFAs.** For a DFA with a partial transition function and $m$ defined transitions, the minimal partial DFA is the minimal complete DFA without its dead state. Valmari and Lehtinen (2008) gave an $O(m \log n)$ algorithm that does not first complete the DFA, which matters when $m$ is much smaller than $n \sigma$.
- **Acyclic DFAs.** For a DFA whose graph has no cycles, such as the DFA of a finite word list, Revuz (1992) gives an $O(n)$ time algorithm that merges states level by level from the leaves, by their height. A minimal acyclic DFA of a sorted word list can also be built one word at a time, without the large intermediate trie.
- **Moore and Mealy machines.** States are equivalent when they give the same output sequence on every input. The same refinement starts from the partition by output instead of $\{F, Q \setminus F\}$. See [Moore machine](/moore-machine/) and [Mealy machine](/mealy-machine/).
- **NFA minimization.** Finding a smallest NFA is PSPACE-complete, and minimal NFAs are not unique. See [NFA minimization](/nfa-minimization/).
- **Incompletely specified machines.** If some outputs are "don't care", the states form a compatibility relation that is not transitive, and finding a smallest machine is NP-hard (Pfleeger, 1973).
- **Weighted and sequential transducers.** After the outputs or weights are pushed towards the start state, the same refinement minimizes them (Mohri, 1997).

## Examples

Let $\Sigma = \{a, b\}$, $q_0 = 0$ and $F = \{3, 4, 6\}$, with this table:

| $\delta$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $a$ | 1 | 3 | 4 | 5 | 5 | 5 | 6 |
| $b$ | 2 | 4 | 3 | 5 | 5 | 5 | 3 |

The DFA accepts the strings of length exactly 2. State 6 is accepting but unreachable, so the first step removes it. The refinement on $\{0, 1, 2, 3, 4, 5\}$ runs as follows.

| round | partition | reason for the split |
|---|---|---|
| 0 | $\{3, 4\}$, $\{0, 1, 2, 5\}$ | accepting or not |
| 1 | $\{3, 4\}$, $\{0, 5\}$, $\{1, 2\}$ | 1 and 2 go into $\{3, 4\}$, 0 and 5 do not |
| 2 | $\{3, 4\}$, $\{1, 2\}$, $\{0\}$, $\{5\}$ | on $a$, 0 goes to $\{1, 2\}$ and 5 goes to $\{0, 5\}$ |
| 3 | no change | the partition is stable |

The minimal DFA has the 4 states $\{0\}$, $\{1, 2\}$, $\{3, 4\}$, $\{5\}$: "nothing read", "one symbol read", "two symbols read" (accepting) and "too long" (dead). A script checked the rounds, the language up to length 8, and the count of 4.

## Known algorithms

| algorithm | time | idea |
|---|---|---|
| [table filling](/table-filling-minimization/) | $O(\sigma n^2)$ | mark distinguishable pairs, propagate marks backwards |
| [Moore](/moore-minimization/) | $O(\sigma n^2)$ | refine by the classes of the successors, in at most $n - 2$ rounds |
| [Hopcroft](/hopcroft-minimization/) | $O(\sigma n \log n)$ | refine by splitters, process the smaller half |
| [Brzozowski](/brzozowski-minimization/) | exponential in the worst case | reverse, determinize, reverse, determinize |
| Revuz | $O(n)$ | acyclic DFAs only |

All of them first remove the unreachable states by a graph search in $O(\sigma n)$ time, except Brzozowski's, which never builds them. Over a fixed alphabet, Moore's algorithm takes $O(n \log n)$ time on average over uniformly random DFAs (Bassino, David and Nicaud, 2009), and it is often fast in practice. Hopcroft's algorithm is a case of [partition refinement](/partition-refinement/); Paige and Tarjan (1987) extended the same "smaller half" idea to the coarsest stable partition of a relation.

## Bounds

**Upper bound.** $O(\sigma n \log n)$ time and $O(\sigma n)$ space on the [word RAM](/word-ram/), by Hopcroft's algorithm.

**Lower bound.** Every algorithm must read $\Omega(\sigma n)$ entries of the table on some input. The language of a DFA is empty exactly when its minimal DFA is one rejecting state, so the adversary bound of [DFA emptiness](/dfa-emptiness/) carries over. No lower bound above $\Omega(\sigma n)$ is known for general algorithms. For Hopcroft's algorithm itself, the bound $\Theta(n \log n)$ is tight: there are families of unary and binary DFAs on which it does $\Theta(n \log n)$ work, whichever order it uses for its splitters (Berstel and Carton, 2004; Castiglione, Restivo and Sciortino, 2008).

**Space-bounded complexity.** Two states are inequivalent exactly when one string leads them into $F$ and into $Q \setminus F$. A nondeterministic logspace machine can guess this string one symbol at a time while it tracks the two states, so state inequivalence is in NL, and state equivalence is in NL because NL is closed under complement. Cho and Huynh (1992) showed that DFA minimization is NL-complete.

## Reductions

- **Equivalence reduces to minimization.** Two DFAs accept the same language if and only if their minimal DFAs, with states numbered in breadth-first order, are equal. See [DFA equivalence](/dfa-equivalence/).
- **Minimization reduces to coarsest stable partition.** The classes of $\sim$ are the coarsest partition of $R$ that respects $F$ and is stable under the $\sigma$ functions $\delta(\cdot, a)$, which is the problem that [partition refinement](/partition-refinement/) solves.
- **Minimization of a reversed DFA.** If $M$ has all its states reachable, the subset construction applied to the reversal of $M$, with only the reachable subsets, gives a minimal DFA for $L(M)^R$. Brzozowski's algorithm uses this fact twice.

## Applications

- **Lexer and regex compilers** minimize the DFA that the [subset construction](/subset-construction/) produces, which often has many equivalent states.
- **Dictionaries.** A minimal acyclic DFA of a word list stores the list compactly and shares common suffixes as well as prefixes.
- **Hardware design.** State minimization of a finite-state machine reduces the number of flip-flops and the logic of a circuit.
- **Verification.** Minimizing the automata of components, or the quotient by [bisimulation](/bisimulation/) for labelled transition systems, reduces state spaces before a model checker explores them.
- **Learning.** The [L* algorithm](/lstar-algorithm/) learns the minimal DFA of an unknown regular language, and minimization gives the canonical target to compare with.

## References
