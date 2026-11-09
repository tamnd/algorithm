---
tag: D19618
kind: technique
slug: automata-theoretic-approach
name: Automata-theoretic approach
aliases:
- Automata-based model checking
area: logic-and-constraints/model-checking
level: advanced
summary: Treat the system and the negated property as automata on infinite words, so that verification becomes emptiness of their product, a search for a reachable accepting cycle.
prereqs: [buchi-automaton, kripke-structure, linear-temporal-logic, product-construction]
see_also: [ltl-model-checking, ltl-to-buchi-translation, language-containment, nested-depth-first-search, on-the-fly-model-checking, ltl-model-checking-pspace-completeness, ltl-satisfiability, emerson-lei-algorithm]
sources:
  - paper: "Moshe Y. Vardi and Pierre Wolper, An automata-theoretic approach to automatic program verification, First Symposium on Logic in Computer Science (LICS 1986), IEEE, pages 332 to 344"
    locator: the reduction of model checking and satisfiability of LTL to the emptiness of Büchi automata
  - paper: doi:10.1006/inco.1994.1092
    title: Moshe Y. Vardi and Pierre Wolper, Reasoning about infinite computations, Information and Computation 115(1), 1994, pages 1 to 37
    locator: the translation of temporal formulas into Büchi automata and the decision procedures built on it
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 4, Sections 4.3 and 4.4 (ω-regular properties, the product with a Büchi automaton, nested depth-first search) and Chapter 5, Section 5.2 (automata-based LTL model checking)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 9 (model checking and automata theory)
---

The automata-theoretic approach treats both the system and the property as automata on infinite words. The system is correct when every behaviour it has is a behaviour that the property allows, which is a question of [language containment](/language-containment/). The approach avoids complementing an automaton: it builds an automaton for the *negation* of the property, takes its product with the system, and checks that the product accepts no word. That check is a search for a reachable accepting cycle, and a cycle found is a counterexample.

## In plain words

A system produces runs that go on forever. A property sorts these runs into good and bad ones. The approach builds a small machine that watches a run and raises a flag, again and again, exactly when the run is bad.

The checker then runs the system and the watcher together, step by step, and looks for a way to go round a loop in which the flag is raised. If it finds one, the path to the loop and the loop itself make a bad run of the system, which is a counterexample. If no such loop exists, no run of the system is bad, so the property holds.

This turns a question about logic into a search in a graph, which computers do well.

## When it applies

- The system is a finite [Kripke structure](/kripke-structure/), or anything whose runs can be read as the runs of a finite automaton: a set of processes, a program with bounded data, a model of hardware. Extensions handle [pushdown systems](/pushdown-system/) and probabilistic systems.
- The property is linear time: a set of infinite words. It is given as an [LTL](/linear-temporal-logic/) formula, or directly as an ω-automaton. It must be ω-regular, which LTL formulas are.
- An automaton for the complement of the property is easy to get. For LTL this is free, since $\neg\varphi$ is a formula. For a property given as a nondeterministic Büchi automaton, the complement is expensive; see Pitfalls.

The approach is not needed for branching-time logics such as [CTL](/computation-tree-logic/), which have direct labelling algorithms, though automata on trees play the same role there.

## The template

The holes are in capitals.

```pseudo id=main
AUTOMATA-CHECK(M, SPEC)
L1  B ← TRANSLATE(NEGATE(SPEC))                 ▷ a Büchi automaton for the bad words
L2  P ← PRODUCT(M, B)                           ▷ built lazily or in full
L3  c ← EMPTINESS(P)                            ▷ a reachable accepting cycle, or none
L4  if c = none then return "M satisfies SPEC"
L5  return the projection of the stem and the cycle of c onto M
```

The holes:

- **NEGATE and TRANSLATE.** For an LTL formula $\varphi$, translate $\neg\varphi$ with the [LTL to Büchi translation](/ltl-to-buchi-translation/), at most $2^{O(|\varphi|)}$ states. For a property given as an automaton for the bad words (a SPIN *never claim*), use it as it is. For a property given as an automaton for the good words, complement it.
- **PRODUCT.** Let $B = (Q, Q_0, \delta, F)$ with $\delta \subseteq Q \times 2^{AP} \times Q$. The product has the states $(s, q)$, the initial states $(s, q)$ with $s \in I$ and $q \in Q_0$, an edge $(s, q) \to (s', q')$ whenever $(s, s') \in R$ and $(q, L(s), q') \in \delta$, and the accepting states $(s, q)$ with $q \in F$. The automaton reads the label of each state of $M$ as it leaves it.
- **EMPTINESS.** Look for a reachable cycle through an accepting state: [nested depth-first search](/nested-depth-first-search/), an SCC search with [Tarjan's algorithm](/tarjan-scc/), or a symbolic fixed point as in the [Emerson-Lei algorithm](/emerson-lei-algorithm/). For a generalized Büchi automaton, the cycle must meet every acceptance set.

### Example

The system $M$ has three states: $s_0$ with label $\emptyset$, $s_1$ with label $\{r\}$ (a request is pending), and $s_2$ with label $\{g\}$ (the request is granted). The transitions are $s_0 \to s_1$, $s_1 \to s_1$, $s_1 \to s_2$ and $s_2 \to s_0$, and $s_0$ is initial. The property is $\varphi = \mathsf{G}(r \to \mathsf{F}\, g)$, every request is granted.

The negation is $\neg\varphi = \mathsf{F}(r \wedge \mathsf{G} \neg g)$. A Büchi automaton $B$ for it has two states: $q_0$ (initial) waits, with a loop on every letter and an edge to $q_1$ on letters with $r$ and without $g$; $q_1$ (accepting) has a loop on the letters without $g$, and no other edge. The reachable part of the product:

| Product state | Letter read | Successors |
|---|---|---|
| $(s_0, q_0)$ | $\emptyset$ | $(s_1, q_0)$ |
| $(s_1, q_0)$ | $\{r\}$ | $(s_1, q_0)$, $(s_1, q_1)$, $(s_2, q_0)$, $(s_2, q_1)$ |
| $(s_1, q_1)$ | $\{r\}$ | $(s_1, q_1)$, $(s_2, q_1)$ |
| $(s_2, q_0)$ | $\{g\}$ | $(s_0, q_0)$ |
| $(s_2, q_1)$ | $\{g\}$ | none, since $q_1$ rejects $g$ |

The accepting state $(s_1, q_1)$ has a loop, so the product is not empty. The counterexample has the stem $s_0 s_1$ and the cycle $s_1$: the system can keep the request pending forever. If the loop $s_1 \to s_1$ is removed, the only edge out of $(s_1, q_1)$ goes to the dead end $(s_2, q_1)$, no accepting cycle is left, and $M \models \varphi$. With the loop kept, a [fairness](/fairness/) assumption that $s_1$ is eventually left also makes the property hold; it is added as a conjunct of the formula, or as an extra acceptance condition.

### Why it is correct

Write $\mathcal{L}(M)$ for the set of traces of the paths of $M$ from $I$, and $\mathcal{L}(\varphi)$ for the set of words that satisfy $\varphi$. By definition, $M \models \varphi$ iff $\mathcal{L}(M) \subseteq \mathcal{L}(\varphi)$, and so

$$M \models \varphi \iff \mathcal{L}(M) \cap \overline{\mathcal{L}(\varphi)} = \emptyset \iff \mathcal{L}(M) \cap \mathcal{L}(B) = \emptyset,$$

since $\mathcal{L}(B) = \mathcal{L}(\neg\varphi) = \overline{\mathcal{L}(\varphi)}$ by the correctness of the translation.

*Product lemma.* A sequence $(s_0, q_0)(s_1, q_1) \ldots$ is an infinite path of $P$ from an initial state iff $s_0 s_1 \ldots$ is a path of $M$ from $I$ and $q_0 q_1 \ldots$ is a run of $B$ on its trace $L(s_0) L(s_1) \ldots$. This is the definition of the edges of $P$, read one step at a time. The path of $P$ visits accepting states infinitely often iff the run of $B$ does. So $P$ has an accepting infinite path iff some trace of $M$ is in $\mathcal{L}(B)$.

*Emptiness lemma.* A finite graph has an infinite path from an initial state through accepting states infinitely often iff it has a reachable cycle through an accepting state. If the path exists, some accepting state $f$ occurs infinitely often, and the segment between two of its occurrences is a cycle; conversely, a stem followed by the cycle repeated forever is such a path. So EMPTINESS answers exactly whether $P$ accepts some word, and the cycle it finds gives a lasso-shaped path of $M$ whose trace violates $\varphi$.

### Size and time

The product has at most $|S| \cdot |Q|$ states and $|R| \cdot |\delta|$ edges, and an emptiness check by nested depth-first search or Tarjan's algorithm is linear in it. For LTL, $|Q| = 2^{O(|\varphi|)}$, so the time is $O(|M| \cdot 2^{O(|\varphi|)})$, linear in the system. When the product is built on the fly from a successor function, the search can stop at the first accepting cycle, and the space can be cut to polynomial in $|\varphi|$ plus $\log |M|$, which is the upper bound of the [PSPACE-completeness theorem](/ltl-model-checking-pspace-completeness/). The size of $M$ is usually the limit, by the [state explosion problem](/state-explosion-problem/).

## Classic examples

- **LTL model checking in SPIN.** The property is translated into a *never claim*, a Büchi automaton for its negation written in Promela, and SPIN runs it in lockstep with the processes and searches for an acceptance cycle with nested depth-first search.
- **LTL satisfiability.** With no system, the product is $B$ itself, and $\varphi$ is satisfiable iff the automaton for $\varphi$ is not empty; see [LTL satisfiability](/ltl-satisfiability/).
- **Language containment between automata.** COSPAN and the work of Kurshan check $\mathcal{L}(M) \subseteq \mathcal{L}(A)$ with the specification given as an ω-automaton $A$ that is deterministic or easy to complement; see [language containment](/language-containment/).
- **Probabilistic systems.** Vardi (1985) used automata for LTL on Markov chains; the product with a deterministic automaton reduces the question to probabilities of reaching end components.
- **Branching time.** Kupferman, Vardi and Wolper (2000) gave the same plan for CTL and CTL* with alternating tree automata, where the emptiness check becomes a game.

## Variations

- **Generalized acceptance.** Keep one acceptance set per until formula and check emptiness by SCCs, or with a nested search that tracks the sets; this avoids the factor of degeneralization.
- **Safety properties.** For a [safety property](/safety-property/), an automaton on finite words for the bad prefixes suffices, and emptiness becomes [reachability](/reachability-problem/) of an accepting state. This is also the idea behind [liveness-to-safety](/liveness-to-safety/).
- **Alternating automata.** Translate $\varphi$ into an alternating automaton of linear size, and remove the alternation only lazily. LTL2BA (Gastin and Oddoux 2001) goes through very weak alternating automata.
- **Symbolic.** Encode $M$ and $B$ with BDDs, and compute the states with an accepting path by a fixed point, as in [symbolic model checking](/symbolic-model-checking/).
- **Bounded.** Look for accepting lassos of bounded length with SAT, as in [bounded model checking](/bounded-model-checking/).
- **On the fly.** Build the product while EMPTINESS runs; see [on-the-fly model checking](/on-the-fly-model-checking/).

## Pitfalls

- **Translating the property instead of its negation.** The product must use the automaton for the bad words. Translating $\varphi$ and searching for accepting cycles finds runs that satisfy $\varphi$, which proves nothing about the others.
- **Complementing Büchi automata.** If the specification is a nondeterministic Büchi automaton for the good words, its complement can need $2^{\Theta(n \log n)}$ states, and the constructions are complex. The approach is cheap only when the negation comes for free, as with LTL, or when the specification automaton is deterministic.
- **The label convention.** Some books label the states of the automaton, others its edges, and some read the label of the target state of $M$ instead of the source. Mixing conventions shifts the trace by one position and gives wrong answers for formulas with $\mathsf{X}$.
- **Deadlocks.** The semantics needs infinite paths. A state of $M$ with no successor must get a self-loop, or its finite runs are silently ignored by the product.
- **Fairness.** Without fairness, the counterexamples are often unfair runs, like the starving request above. Add the fairness assumption to the formula or to the acceptance condition.

## Exercises

1. In the example, remove the loop $s_1 \to s_1$ and list the reachable product states. Check that no accepting cycle exists.
2. Build a Büchi automaton for $\neg \mathsf{G}\mathsf{F}\, p$ and use it to check $\mathsf{G}\mathsf{F}\, p$ on a two-state system with states labelled $\{p\}$ and $\emptyset$ that may stay in the second state forever.
3. Prove the product lemma for the convention in which the automaton reads the label of the target state, and say what changes for the initial states.
4. Show that $\mathcal{L}(M) \subseteq \mathcal{L}(A)$ for a deterministic Büchi automaton $A$ can be checked in time polynomial in $|M| \cdot |A|$. (Hint: the complement of a deterministic Büchi automaton is a co-Büchi automaton of the same size.)

## References
