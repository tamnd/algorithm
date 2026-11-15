---
tag: TSA1J1
kind: problem
slug: abductive-reasoning
name: Abduction
aliases:
- abductive explanation
- inference to the best explanation
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: Given a theory and an observation, find a minimal consistent set of hypotheses that together with the theory entails the observation.
prereqs: [nonmonotonic-reasoning, sat, polynomial-hierarchy]
see_also: [consistency-based-diagnosis, abductive-logic-programming, assumption-based-truth-maintenance, set-cover, horn-sat, default-logic-complexity, qbf]
sources:
  - paper: doi:10.1145/200836.200838
    title: Thomas Eiter and Georg Gottlob, The complexity of logic-based abduction, Journal of the ACM 42(1), 3 to 42 (1995)
    locator: the definition of a propositional abduction problem and the complexity of checking, existence, relevance and necessity for general, Horn and definite Horn theories and for several minimality criteria
  - paper: "Bart Selman and Hector J. Levesque, Abductive and default reasoning: a computational core, Proceedings of the Eighth National Conference on Artificial Intelligence (AAAI-90), 343 to 348 (1990)"
    locator: the NP-hardness of finding an explanation for Horn theories
  - paper: "Gerhard Friedrich, Georg Gottlob and Wolfgang Nejdl, Hypothesis classification, abductive diagnosis and therapy, in Expert Systems in Engineering, Lecture Notes in Computer Science 462, Springer, 69 to 78 (1990)"
    locator: the NP-completeness of deciding whether a hypothesis is relevant for a definite Horn theory
  - paper: "Michael Thomas and Heribert Vollmer, Complexity of non-monotonic logics, Bulletin of the EATCS 102 (2010), arXiv:1009.1990"
    locator: Section 6, Theorem 6.1 (checking is DP-complete, existence is Sigma2P-complete, necessity is Pi2P-complete, also for subset-minimal explanations, citing Eiter and Gottlob 1995)
---

Abduction is reasoning from an observation back to a cause. Deduction goes from "rain makes the grass wet" and "it rained" to "the grass is wet". Abduction goes from the rule and the wet grass to the hypothesis "it rained". In logic-based abduction the input is a background theory, a set of allowed hypotheses and an observation, and an explanation is a set of hypotheses that is consistent with the theory and, together with it, entails the observation. Usually only the minimal explanations are wanted. For propositional theories, deciding whether an explanation exists is $\Sigma_2^p$-complete, one level above [SAT](/sat/), and it drops to NP for Horn theories and to polynomial time for definite Horn theories (Eiter and Gottlob 1995).

## In plain words

You see an effect and want to know what could have caused it. You have a list of possible causes and a set of rules that say what each cause brings about. An explanation is a choice of causes that does not contradict what you know and that would produce everything you see. Several choices may work. You prefer the ones that assume nothing extra: if one cause alone explains the effect, a pair that includes it is not a better explanation. The hard part is that "would produce" and "does not contradict" are both questions of logic, and the number of possible choices of causes grows exponentially.

## Definition

A *propositional abduction problem* (Eiter and Gottlob 1995) is a tuple $\mathcal{P} = (V, H, M, T)$:

- $V$ is a finite set of atoms,
- $H \subseteq V$ is the set of *hypotheses*,
- $M$ is a set of literals over $V$, the *manifestations* (observations),
- $T$ is a consistent propositional theory over $V$.

A set $S \subseteq H$ is an *explanation* (a *solution*) of $\mathcal{P}$ if

$$T \cup S \text{ is consistent} \qquad\text{and}\qquad T \cup S \models M.$$

Write $\mathrm{Sol}(\mathcal{P})$ for the set of explanations. An explanation is *subset-minimal* if no proper subset is an explanation. Other preference orders compare explanations by size or by priorities and penalties on the hypotheses.

The **decision tasks** for an order $\preceq$ on explanations are:

- **Checking:** is a given $S$ a $\preceq$-minimal explanation?
- **Existence:** is $\mathrm{Sol}(\mathcal{P})$ nonempty?
- **Relevance:** is a given $h \in H$ in some $\preceq$-minimal explanation?
- **Necessity:** is a given $h \in H$ in every $\preceq$-minimal explanation?

The **search task** is to output one minimal explanation, or all of them.

## Variants

- **Horn abduction.** $T$ is a set of Horn clauses and $M$ a set of atoms. **Definite Horn** abduction also requires every clause to have exactly one positive literal, so $T \cup S$ is always consistent.
- **Set-covering abduction.** Each hypothesis is a disease and $T$ only says which disease causes which symptom. An explanation is a set of diseases whose symptoms cover $M$. With minimum size as the criterion this is [set cover](/set-cover/).
- **Cardinality and weights.** Prefer the explanations with the fewest hypotheses, or with the least total cost. This turns the search into an optimization problem, often solved with [MaxSAT](/max-sat/).
- **First-order and logic-program abduction.** The theory is a first-order theory or a logic program, as in [abductive logic programming](/abductive-logic-programming/). Hypotheses are atoms of chosen *abducible* predicates.
- **Probabilistic abduction.** Choose the most probable explanation in a [Bayesian network](/bayesian-network/), which replaces logical minimality by probability.

## Examples

**Rain or sprinkler.** $V = \{\mathit{rain}, \mathit{sprinkler}, \mathit{wetGrass}, \mathit{wetStreet}\}$, $H = \{\mathit{rain}, \mathit{sprinkler}\}$, $M = \{\mathit{wetGrass}\}$ and

$$T = \{\mathit{rain} \supset \mathit{wetGrass},\ \mathit{sprinkler} \supset \mathit{wetGrass},\ \mathit{rain} \supset \mathit{wetStreet}\}.$$

The explanations are $\{\mathit{rain}\}$, $\{\mathit{sprinkler}\}$ and $\{\mathit{rain}, \mathit{sprinkler}\}$. The first two are subset-minimal, so both hypotheses are relevant and neither is necessary.

**A new fact removes an explanation.** Add $\neg\mathit{wetStreet}$ to $T$. Now $T \cup \{\mathit{rain}\}$ is inconsistent, the only minimal explanation is $\{\mathit{sprinkler}\}$, and $\mathit{sprinkler}$ becomes necessary. Abduction is nonmonotonic: more knowledge can remove explanations.

**No explanation.** With $H = \{\mathit{rain}\}$, $M = \{\mathit{wetGrass}\}$ and $T = \{\mathit{rain} \supset \mathit{wetStreet}\}$, no subset of $H$ entails $M$, so $\mathrm{Sol}(\mathcal{P}) = \emptyset$.

## Known algorithms

- **Generate and test.** Try the subsets of $H$ in order of size and keep those that pass one SAT test for consistency and one for entailment. This takes $2^{|H|}$ pairs of tests and finds all subset-minimal explanations.
- **Guess and check with two solvers.** For the $\Sigma_2^p$ case, one [SAT](/sat/) solver proposes a set $S$ and a second one looks for a model of $T \cup S$ that falsifies $M$. Each counterexample blocks a family of candidates, in the style of [CEGAR](/cegar/). Encodings into [QBF](/qbf/) follow the same quantifier pattern.
- **[Assumption-based truth maintenance](/assumption-based-truth-maintenance/).** For Horn theories, the ATMS keeps for each atom its label, the set of minimal consistent sets of assumptions that derive it. The label of the observation is the set of its minimal explanations. Labels can be exponentially large.
- **Definite Horn theories.** [Forward chaining](/forward-chaining/) decides $T \cup S \models M$ in linear time, as in [Horn-SAT](/horn-sat/). One minimal explanation is found by starting from $H$ and deleting hypotheses while the entailment still holds, with $|H|$ entailment tests.
- **Abductive logic programming.** Proof procedures in the style of SLDNF resolution collect abducible atoms as they go, see [abductive logic programming](/abductive-logic-programming/).

## Bounds

All results are for propositional problems and subset-minimal explanations, under polynomial-time reductions (Eiter and Gottlob 1995; Thomas and Vollmer 2010, Theorem 6.1).

| Theory | Checking | Existence | Relevance | Necessity |
|---|---|---|---|---|
| general | DP-complete | $\Sigma_2^p$-complete | $\Sigma_2^p$-complete | $\Pi_2^p$-complete |
| Horn | in P | NP-complete | NP-complete | coNP-complete |
| definite Horn | in P | in P | NP-complete | in P |

- The general upper bounds are direct: guess $S$, then one NP test (consistency) and one coNP test (entailment). Checking that $S$ is an explanation is the conjunction of an NP and a coNP question, which is what DP-completeness means.
- The NP-hardness of existence for Horn theories is due to Selman and Levesque (1990). For definite Horn theories, an explanation exists exactly when $T \cup H \models M$, and $h$ is necessary exactly when $T \cup (H \setminus \{h\}) \not\models M$, so both are polynomial. Relevance stays NP-complete even there (Friedrich, Gottlob and Nejdl 1990).
- The number of minimal explanations can be exponential: with $T = \{h_i \supset m_i,\ h'_i \supset m_i : i \le n\}$ and $M = \{m_1, \ldots, m_n\}$ there are $2^n$ of them.
- Preference by size or by penalties moves some tasks to classes of the [polynomial hierarchy](/polynomial-hierarchy/) defined by a bounded number of oracle calls. Eiter and Gottlob (1995) give the complete table.

## Reductions

- **From $\exists\forall$ QBF to existence** (a proof sketch of the lower bound). For $\exists X \forall Y \psi$, add a fresh atom $x'$ for each $x \in X$, a fresh atom $m$, and put $H = X \cup X'$, $M = \{m\}$ and $T = \{x' \leftrightarrow \neg x : x \in X\} \cup \{\psi \supset m\}$. A set $S$ is consistent with $T$ unless it contains both $x$ and $x'$, so it fixes a partial assignment of $X$. Since $m$ is free, $T \cup S \models m$ exactly when $T \cup S \models \psi$, that is, when $\psi$ holds for every completion of the partial assignment and every $Y$. So an explanation exists exactly when the QBF is true.
- **To and from [consistency-based diagnosis](/consistency-based-diagnosis/).** Diagnosis asks for faults that make the observations consistent, abduction for hypotheses that entail them. With fault models that predict the observed behaviour, diagnosis becomes abduction, and the two meet in a spectrum of definitions.
- **From [set cover](/set-cover/).** Minimum set-covering abduction is set cover, so finding a smallest explanation is NP-hard even when entailment is trivial.
- **To [default logic](/default-logic/).** Selman and Levesque (1990) related Horn abduction to finding extensions of simple default theories, which places both in a common computational core.

## Applications

- **Diagnosis** of devices and of patients, where the hypotheses are faults or diseases and the observations are symptoms.
- **Plan and intention recognition**, which explains observed actions by the goals that produce them.
- **Natural language interpretation**, which explains a sentence by the assumptions that make it coherent.
- **Database and knowledge-base updates**, where a view update is explained by changes to the base facts.
- **Test generation and debugging**, where the explanation of a failure is a set of suspicious statements.

## References
