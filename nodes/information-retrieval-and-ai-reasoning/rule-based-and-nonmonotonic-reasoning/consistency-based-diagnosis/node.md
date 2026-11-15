---
tag: X57HBD
kind: problem
slug: consistency-based-diagnosis
name: Consistency-based diagnosis
aliases:
- model-based diagnosis
- Reiter diagnosis
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: Given a system description and observations, find minimal sets of components whose abnormality makes the observations consistent.
prereqs: [sat, hitting-set]
see_also: [reiter-hs-tree, abductive-reasoning, minimal-unsatisfiable-subset, minimal-correction-subset, minimal-transversal-enumeration, assumption-based-truth-maintenance, circumscription]
sources:
  - paper: doi:10.1016/0004-3702(87)90062-2
    title: Raymond Reiter, A theory of diagnosis from first principles, Artificial Intelligence 32(1), 57 to 95 (1987)
    locator: the definitions of a system, a diagnosis and a conflict set, Theorem 4.4 (the minimal diagnoses are the minimal hitting sets of the conflict sets) and the HS-tree
  - paper: doi:10.1016/0004-3702(87)90063-4
    title: Johan de Kleer and Brian C. Williams, Diagnosing multiple faults, Artificial Intelligence 32(1), 97 to 130 (1987)
    locator: the General Diagnostic Engine, minimal conflicts and candidates computed with an ATMS, the polybox circuit, and measurement selection by minimum entropy
  - paper: doi:10.1016/0004-3702(89)90079-9
    title: Russell Greiner, Barbara A. Smith and Ralph W. Wilkerson, A correction to the algorithm in Reiter's theory of diagnosis, Artificial Intelligence 41(1), 79 to 88 (1989)
    locator: the counterexamples to Reiter's pruning rules and the corrected HS-DAG
---

Consistency-based diagnosis finds the faulty parts of a system from a model of how the parts should work. The engineer gives the *system description*, a logical model of each component under the assumption that it is not abnormal, and the *observations*, the measured inputs and outputs. If the observations contradict the model, some components must be faulty. A *diagnosis* is a minimal set of components such that assuming exactly these are abnormal, and all others work, is consistent with the observations. Reiter (1987) gave the theory and proved that the minimal diagnoses are exactly the minimal [hitting sets](/hitting-set/) of the *conflict sets*, the sets of components that cannot all be working. No model of faulty behaviour is needed.

## In plain words

You have a circuit and you know what each part should do. You put in some values and measure the outputs, and one output is wrong. Some parts must be broken, but which? A group of parts is *in conflict* if they cannot all be working, because together they would predict a different output. Every explanation of the failure must blame at least one part of every conflict. The smallest ways to do that are the diagnoses. You do not need to know how a broken part behaves, only how a working part behaves.

## Definition

A *system* is a triple $(\mathit{SD}, \mathit{COMPS}, \mathit{OBS})$ (Reiter 1987):

- $\mathit{COMPS}$ is a finite set of components,
- $\mathit{SD}$, the system description, is a set of formulas that uses an atom $\mathit{AB}(c)$ for each $c \in \mathit{COMPS}$, meaning "$c$ is abnormal",
- $\mathit{OBS}$ is a set of formulas, the observations.

A set $\Delta \subseteq \mathit{COMPS}$ is a *diagnosis* when

$$\mathit{SD} \cup \mathit{OBS} \cup \{\mathit{AB}(c) : c \in \Delta\} \cup \{\neg\mathit{AB}(c) : c \in \mathit{COMPS} \setminus \Delta\}$$

is consistent, and no proper subset of $\Delta$ has this property. A set $C \subseteq \mathit{COMPS}$ is a *conflict set* when $\mathit{SD} \cup \mathit{OBS} \cup \{\neg\mathit{AB}(c) : c \in C\}$ is inconsistent. It is *minimal* when no proper subset is a conflict set.

**Theorem** (Reiter 1987, Theorem 4.4). $\Delta$ is a diagnosis exactly when it is a minimal hitting set of the collection of the minimal conflict sets.

When the system description only says how working components behave, a superset of a consistent assumption is also consistent, so the minimal diagnoses determine all the consistent fault sets.

The **tasks** are: decide whether a given set is a diagnosis; find one diagnosis, all of them, or one of minimum size; and, given probabilities, find the most probable ones.

## Variants

- **Minimum-cardinality diagnosis.** Prefer the diagnoses with the fewest faulty components. This is an optimization problem, usually solved with [MaxSAT](/max-sat/) on the soft constraints $\neg\mathit{AB}(c)$.
- **Probabilistic diagnosis.** Each component fails independently with a known probability, and the candidates are ranked by their posterior probability. De Kleer and Williams (1987) also choose the next measurement to minimize the expected entropy of the candidates.
- **Fault models.** A component can be in one of several modes, each with its own behaviour. Then a superset of a consistent fault set need not be consistent, and the definition must list the mode of each component.
- **Abductive diagnosis.** With complete fault models, one can ask for faults that *entail* the observations instead of being consistent with them. That is [abduction](/abductive-reasoning/).
- **Diagnosis of knowledge bases and programs.** The components are the clauses of a knowledge base, the constraints of a model or the statements of a program, and the same definitions apply.

## Examples

**The polybox.** This circuit is the standard example of de Kleer and Williams (1987). Three multipliers compute $X = A \cdot C$ ($M_1$), $Y = B \cdot D$ ($M_2$) and $Z = C \cdot E$ ($M_3$). Two adders compute $F = X + Y$ ($A_1$) and $G = Y + Z$ ($A_2$). The inputs are $A = 3$, $B = 2$, $C = 2$, $D = 3$, $E = 3$, so a working circuit gives $F = 12$ and $G = 12$. The measurement is $F = 10$ and $G = 12$.

- If $M_1$, $M_2$ and $A_1$ work, then $X = 6$, $Y = 6$ and $F = 12$, which contradicts $F = 10$. So $\{A_1, M_1, M_2\}$ is a minimal conflict set.
- If $M_1$, $M_3$, $A_1$ and $A_2$ work, then $X = 6$ and $Z = 6$, so $Y = F - X = 4$ by $A_1$ and $G = 4 + 6 = 10$ by $A_2$, which contradicts $G = 12$. So $\{A_1, A_2, M_1, M_3\}$ is a second minimal conflict set.
- The minimal hitting sets of these two sets are $\{A_1\}$, $\{M_1\}$, $\{A_2, M_2\}$ and $\{M_2, M_3\}$. These are the four diagnoses. The single faults $A_1$ or $M_1$ are the most likely ones when faults are rare.

**No fault.** If the observation is $F = 12$ and $G = 12$, then $\mathit{SD} \cup \mathit{OBS}$ with all components working is consistent, there is no conflict set, and the only diagnosis is $\emptyset$.

**Inconsistent observations.** A diagnosis exists exactly when $\mathit{SD} \cup \mathit{OBS}$ is consistent, since then the set of all components is a consistent fault set. If the observations contradict the description even with every component abnormal, for example two different values on one wire, there is no diagnosis.

## Known algorithms

- **[Reiter's hitting set tree](/reiter-hs-tree/).** It computes the minimal conflict sets on demand with a theorem prover and builds the hitting sets breadth-first, so the diagnoses appear in order of size. Reiter's pruning rules can lose diagnoses. Greiner, Smith and Wilkerson (1989) gave counterexamples and the corrected HS-DAG.
- **The General Diagnostic Engine** (de Kleer and Williams 1987). It propagates values with an [assumption-based truth maintenance system](/assumption-based-truth-maintenance/), which records the minimal conflicts, and maintains the minimal candidates incrementally as conflicts arrive.
- **[Minimal correction subsets](/minimal-correction-subset/).** Put $\mathit{SD} \cup \mathit{OBS}$ as hard constraints and $\{\neg\mathit{AB}(c) : c \in \mathit{COMPS}\}$ as soft constraints. The minimal conflict sets are the [minimal unsatisfiable subsets](/minimal-unsatisfiable-subset/) of the soft part, and the diagnoses are its minimal correction subsets. Reiter's theorem is the hitting set duality between the two, and modern diagnosers enumerate correction subsets with a [SAT](/sat/) solver.
- **Explicit conflicts.** When all minimal conflict sets are known, enumerating the diagnoses is [minimal transversal enumeration](/minimal-transversal-enumeration/) of the conflict [hypergraph](/hypergraph/).

## Bounds

- **Testing a candidate.** Deciding whether a given $\Delta$ is consistent with the observations is one satisfiability test, so it is NP-complete for propositional system descriptions. Minimality adds one test for each $c \in \Delta$, since only $\Delta \setminus \{c\}$ needs checking, which places the test for a diagnosis in DP.
- **Existence.** A diagnosis exists exactly when $\mathit{SD} \cup \mathit{OBS}$ is consistent, which is NP-complete.
- **Minimum cardinality.** Deciding whether a diagnosis of size at most $k$ exists is NP-complete. It is NP-hard even when consistency is trivial, by the reduction from [vertex cover](/vertex-cover/) below.
- **Number of diagnoses.** It can be exponential. With $n$ disjoint minimal conflict sets $\{a_i, b_i\}$ there are $2^n$ diagnoses, so any algorithm that lists them all takes exponential time on some inputs.

## Reductions

- **From [vertex cover](/vertex-cover/).** Given a graph, let the components be its vertices, $\mathit{OBS} = \emptyset$ and $\mathit{SD} = \{\mathit{AB}(u) \vee \mathit{AB}(v) : uv \text{ an edge}\}$. The minimal conflict sets are the edges, the diagnoses are the minimal vertex covers, and a diagnosis of size at most $k$ exists exactly when a vertex cover of size at most $k$ exists. The construction is linear.
- **To [hitting set](/hitting-set/).** By Reiter's theorem, once the minimal conflict sets are known, diagnosis is the minimal hitting set problem on them.
- **To [circumscription](/circumscription/).** Minimize the atoms $\mathit{AB}(c)$ in $\mathit{SD} \cup \mathit{OBS}$ with all other atoms varying. The $\mathit{AB}$-parts of the minimal models are the diagnoses.

## Applications

Consistency-based diagnosis is used for digital and analog circuits, cars, spacecraft and process plants, where a model of normal behaviour exists but faults are too varied to list. The same definitions are used to debug knowledge bases, configuration models, constraint models, spreadsheets and programs, where a "component" is a rule, a constraint, a formula or a statement.

## References
