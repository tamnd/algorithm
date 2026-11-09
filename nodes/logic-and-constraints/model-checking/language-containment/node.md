---
tag: 01J1CV
kind: problem
slug: language-containment
name: Language containment
aliases:
- Language inclusion
area: logic-and-constraints/model-checking
level: advanced
summary: Decide whether every word accepted by one automaton is accepted by another. For nondeterministic Büchi automata it is PSPACE-complete; for a deterministic right side it is polynomial.
prereqs: [buchi-automaton, nondeterministic-finite-automaton, automata-theoretic-approach]
see_also: [automata-theoretic-approach, ltl-model-checking, nfa-universality, regex-equivalence-pspace-completeness, simulation-relation, subset-construction, product-construction, ltl-model-checking-pspace-completeness]
sources:
  - paper: "A. Prasad Sistla, Moshe Y. Vardi and Pierre Wolper, The complementation problem for Büchi automata with applications to temporal logic, Theoretical Computer Science 49, 1987"
    locator: complementation of Büchi automata with 2^O(n^2) states, and PSPACE-completeness of containment and universality for Büchi automata
  - paper: "Robert P. Kurshan, Computer-Aided Verification of Coordinating Processes: The Automata-Theoretic Approach, Princeton University Press, 1994"
    locator: verification as language containment of ω-automata, with the specification given as a deterministic automaton
  - paper: "Martin De Wulf, Laurent Doyen, Thomas A. Henzinger and Jean-François Raskin, Antichains: a new algorithm for checking universality of finite automata, Computer Aided Verification (CAV 2006), Lecture Notes in Computer Science 4144, Springer, 2006"
    locator: the antichain algorithms for universality and language inclusion of finite automata
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 4 (regular safety properties and ω-regular properties, checked as the emptiness of a product with an automaton for the bad behaviours)
---

Language containment asks whether $\mathcal{L}(A) \subseteq \mathcal{L}(B)$ for two automata $A$ and $B$ over the same alphabet. In verification, $A$ describes the behaviours of a system and $B$ the behaviours that a specification allows, so containment says that the system has no bad behaviour. The problem reduces to the emptiness of $\mathcal{L}(A) \cap \overline{\mathcal{L}(B)}$, and its cost is the cost of the complement of $B$: polynomial when $B$ is deterministic, and [PSPACE](/pspace/)-complete for nondeterministic finite automata and for nondeterministic [Büchi automata](/buchi-automaton/). LTL model checking is the case where $B$ comes from a formula, and the [automata-theoretic approach](/automata-theoretic-approach/) solves it by negating the formula instead of complementing $B$.

## In plain words

Two machines read sequences of letters. Each accepts some sequences and rejects others. The question is whether every sequence that the first machine accepts is also accepted by the second. If the first machine is a system and the second is a rule, a yes means that the system obeys the rule.

To answer, look for one sequence that the first machine accepts and the second rejects. Such a sequence is a counterexample. Finding it means running the first machine together with a machine for "rejected by the second". That second machine is easy to build when the rule machine never has to guess. When it may guess, the machine for its rejections can be far larger, and this is where the cost comes from.

## Definition

Let $\Sigma$ be a finite alphabet.

- **Input.** Two automata $A$ and $B$ over $\Sigma$ of the same kind: nondeterministic finite automata on finite words, or Büchi automata on infinite words.
- **Question.** Is $\mathcal{L}(A) \subseteq \mathcal{L}(B)$?

A *counterexample* is a word in $\mathcal{L}(A) \setminus \mathcal{L}(B)$. On infinite words, if a counterexample exists, then one of the form $u v^\omega$ exists, since $\mathcal{L}(A) \cap \overline{\mathcal{L}(B)}$ is ω-regular and every nonempty ω-regular language has an ultimately periodic word.

The size of the input is $|A| + |B|$, the numbers of states and transitions. In verification, $A$ is often a [Kripke structure](/kripke-structure/) $M$ read as an automaton whose words are the traces of its paths; then every infinite run of $A$ is accepting.

## Variants

- **Universality.** Is $\mathcal{L}(B) = \Sigma^\omega$ (or $\Sigma^*$)? This is containment with $A$ accepting everything. For finite words it is [NFA universality](/nfa-universality/).
- **Equivalence.** Is $\mathcal{L}(A) = \mathcal{L}(B)$? This is two containments.
- **Deterministic right side.** $B$ is a deterministic finite automaton, or a deterministic Büchi automaton. The complement of $B$ is then of the same size (for Büchi, a co-Büchi automaton), and containment is polynomial.
- **Other acceptance conditions.** Rabin, Streett, parity and Muller automata give the same problem with other costs for complementation and emptiness.
- **Trace inclusion.** For two Kripke structures, are the traces of one among the traces of the other? This is the case where every run of both automata is accepting, and it is still PSPACE-complete; Kanellakis and Smolka (1990) treat this and related equivalences of finite-state processes.
- **Beyond finite automata.** For context-free grammars, and for timed automata (Alur and Dill 1994), containment is undecidable.

## Examples

| $\mathcal{L}(A)$ | $\mathcal{L}(B)$ | Contained? | Counterexample |
|---|---|---|---|
| $(ab)^\omega$ | words with infinitely many $a$ | yes | none |
| $(ab)^\omega$ | words with finitely many $b$ | no | $(ab)^\omega$ |
| words with finitely many $b$ | words with infinitely many $a$ | yes | none |
| words with infinitely many $a$ | words with finitely many $b$ | no | $(ab)^\omega$ |
| $\{ab, ac\}$ | $a\{b, c\}$ | yes, and equal | none |

The language "finitely many $b$" is accepted by a nondeterministic Büchi automaton with two states, which guesses the position of the last $b$. No deterministic Büchi automaton accepts it, so containment *in* this language is the case where determinism cannot be assumed.

**Simulation is not containment.** Let $A$ read $a$ and then go to one state $q$ with edges $b$ and $c$ to accepting states, and let $B$ read $a$ to two states $q_1$ and $q_2$, with only $b$ from $q_1$ and only $c$ from $q_2$. Both accept $\{ab, ac\}$. The automaton $B$ does not simulate $A$, since after $a$ it must choose $q_1$ or $q_2$ before it sees the next letter, and either choice fails one of the two continuations. So a [simulation](/simulation-relation/) check is sound for containment, but it can fail to prove a containment that holds.

## Known algorithms

- **Complement, then emptiness.** Build $\overline{B}$, form the [product](/product-construction/) $A \times \overline{B}$, and test emptiness: [reachability](/graph-reachability/) of an accepting state for finite words, a reachable accepting cycle for infinite words. For finite words, $\overline{B}$ comes from the [subset construction](/subset-construction/), with up to $2^n$ states for $n$ states of $B$. For Büchi automata, Safra's construction (1988) and the rank-based construction of Kupferman and Vardi (2001) give $2^{O(n \log n)}$ states.
- **On the fly in polynomial space.** Explore $A \times \overline{B}$ without building $\overline{B}$: a state of $\overline{B}$ for finite words is a set of states of $B$, written with $n$ bits, and its successor is computed when needed. A nondeterministic search for a counterexample then runs in polynomial space, and [Savitch's theorem](/savitch-theorem/) makes it deterministic. The same holds for Büchi automata with the states of a complement construction.
- **Deterministic $B$.** For a deterministic Büchi automaton $B$, a run of $B$ rejects iff it visits $F_B$ only finitely often. So $\mathcal{L}(A) \not\subseteq \mathcal{L}(B)$ iff the product $A \times B$ has a reachable cycle that meets $F_A$ and avoids $F_B$. This is a search for strongly connected components in the product with the states of $F_B$ removed, in time $O(|A| \cdot |B|)$.
- **Negate the formula.** When $B$ is the automaton of an LTL formula $\varphi$, use the automaton of $\neg\varphi$ as $\overline{B}$, with $2^{O(|\varphi|)}$ states and no complementation; this is the [automata-theoretic approach](/automata-theoretic-approach/).
- **Antichains.** In the subset construction, a set of states of $B$ that contains another reached set is never needed for a counterexample, so only the minimal sets are kept. De Wulf, Doyen, Henzinger and Raskin (2006) showed that this often avoids most of the exponential blow-up; there are extensions to Büchi automata.
- **Simulation first.** If $B$ simulates $A$ (a polynomial check), containment holds. Tools use simulation to prune the search, and fall back to complementation when it fails.

## Bounds

| Case | Complexity | Source |
|---|---|---|
| $B$ a DFA or a deterministic Büchi automaton | polynomial, $O(\lvert A\rvert \cdot \lvert B\rvert)$ | product and SCC search |
| NFA on finite words | PSPACE-complete | Meyer and Stockmeyer 1972 |
| nondeterministic Büchi automata | PSPACE-complete | Sistla, Vardi and Wolper 1987 |
| size of a Büchi complement | $2^{\Theta(n \log n)}$ states | Safra 1988 upper bound; Michel 1988 lower bound |
| $B$ from an LTL formula $\varphi$ | $O(\lvert A\rvert \cdot 2^{O(\lvert\varphi\rvert)})$ time, PSPACE-complete | [Sistla and Clarke 1985](/ltl-model-checking-pspace-completeness/) |
| context-free languages, timed automata | undecidable | classical; Alur and Dill 1994 |

Hardness for Büchi automata follows from the case of finite words: for a new letter $\#$, $\mathcal{L}(N_1) \subseteq \mathcal{L}(N_2)$ iff $\mathcal{L}(N_1) \#^\omega \subseteq \mathcal{L}(N_2) \#^\omega$, and Büchi automata for these languages are made from $N_1$ and $N_2$ by adding one accepting state with a $\#$ loop. With $B$ fixed, containment is polynomial in $|A|$, which is why model checking against a fixed specification automaton scales with the system.

## Reductions

- **To emptiness.** $\mathcal{L}(A) \subseteq \mathcal{L}(B)$ iff $\mathcal{L}(A \times \overline{B}) = \emptyset$. All the algorithms above are ways to build or explore $\overline{B}$.
- **From universality.** $\mathcal{L}(B)$ is universal iff $\mathcal{L}(U) \subseteq \mathcal{L}(B)$ for the one-state automaton $U$ that accepts everything. So containment is at least as hard as [NFA universality](/nfa-universality/), and is PSPACE-hard.
- **From LTL model checking.** $M \models \varphi$ iff $\mathcal{L}(M) \subseteq \mathcal{L}(A_\varphi)$. This reduction is exponential, because $A_\varphi$ can have $2^{\Theta(|\varphi|)}$ states; the polynomial-space bound for LTL comes from building $A_{\neg\varphi}$ on the fly, not from this reduction.
- **To LTL model checking.** If $B$ is given as an automaton, there may be no short LTL formula for $\mathcal{L}(B)$, and some ω-regular languages have no LTL formula at all (for example, "$p$ holds at every even position"). So containment is the more general question.

## Applications

- **Verification of coordinating processes.** Kurshan's COSPAN checks a system of processes against a specification given as an ω-automaton, with the specification deterministic so that its complement is cheap.
- **Refinement checking.** The FDR checker for CSP checks trace refinement, which is containment of trace languages, by making the specification deterministic with the subset construction.
- **LTL model checking.** Every LTL check is a containment question, solved by the [automata-theoretic approach](/automata-theoretic-approach/).
- **Abstraction.** An abstract model must contain the behaviours of the concrete one; see [simulation](/simulation-relation/) and [bisimulation](/bisimulation/) for stronger, polynomial relations that imply containment.

## References
