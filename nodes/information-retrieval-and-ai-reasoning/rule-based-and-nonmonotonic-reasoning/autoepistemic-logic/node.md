---
tag: M9X6W3
kind: model
slug: autoepistemic-logic
name: Autoepistemic logic
aliases:
- Moore autoepistemic logic
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: A modal logic of an agent reasoning about its own beliefs, whose belief sets are stable expansions of the premises.
prereqs: [nonmonotonic-reasoning, kripke-structure, fixed-point]
see_also: [default-logic, default-extension, default-logic-complexity, stable-model-semantics, negation-as-failure, circumscription]
sources:
  - paper: doi:10.1016/0004-3702(85)90042-6
    title: Robert C. Moore, Semantical considerations on nonmonotonic logic, Artificial Intelligence 25(1), 75 to 94 (1985)
    locator: the definition of stable expansions, the soundness and completeness of expansions with respect to autoepistemic interpretations, and the older-brother example
  - paper: doi:10.1093/logcom/2.3.397
    title: Georg Gottlob, Complexity results for nonmonotonic logics, Journal of Logic and Computation 2(3), 397 to 425 (1992)
    locator: the Sigma2P-completeness of expansion existence and credulous reasoning and the Pi2P-completeness of skeptical reasoning in autoepistemic logic
  - paper: "Michael Thomas and Heribert Vollmer, Complexity of non-monotonic logics, Bulletin of the EATCS 102 (2010), arXiv:1009.1990"
    locator: Section 4, Definition 4.4 and Proposition 4.5 (Niemelä's full sets characterize stable expansions) and Theorem 4.6 (the complexity of autoepistemic logic, citing Niemelä 1990 and Gottlob 1992)
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: the reading of negation as failure as an autoepistemic operator, under which stable models correspond to stable expansions
---

Autoepistemic logic is a logic for an agent that reasons about what it believes. It adds a modal operator $L$, where $L\varphi$ reads "I believe $\varphi$". A premise such as $\neg L\,\mathit{brother} \supset \neg\mathit{brother}$ says "if I do not believe that I have an older brother, then I have none", which is how a person reasons from the absence of knowledge. Moore (1985) defined the acceptable belief sets as the *stable expansions* of the premises: sets that contain exactly what follows from the premises together with a correct record of their own beliefs and non-beliefs. The logic is nonmonotonic, because a new premise can turn a non-belief into a belief and so remove conclusions. For finite propositional premises, the main tasks are $\Sigma_2^p$-complete or $\Pi_2^p$-complete.

## The machine

For a logic, the machine is its syntax and its semantics.

**Syntax.** Formulas are built from propositional atoms with the classical connectives and the unary operator $L$. A formula without $L$ is *objective*. A premise set $A$ is a set of formulas. This page uses the propositional case with $A$ finite.

**Stable sets.** Following Stalnaker, a set $T$ is *stable* when it is closed under propositional consequence, contains $L\varphi$ for each $\varphi \in T$, and contains $\neg L\varphi$ for each $\varphi \notin T$. Here propositional consequence treats each formula $L\varphi$ as a new atom. A stable set is the belief set of an ideal introspective agent: it knows what it believes and what it does not believe. A consistent stable set is fixed by its objective part, which is the theory of a nonempty set of worlds. $L\varphi$ is then true exactly when $\varphi$ is true in all of these worlds, which is a [Kripke structure](/kripke-structure/) in which every world sees every world.

**Stable expansions.** A set $T$ is a *stable expansion* of $A$ when

$$T = \mathrm{Th}\bigl(A \cup \{L\varphi : \varphi \in T\} \cup \{\neg L\varphi : \varphi \notin T\}\bigr),$$

where $\mathrm{Th}$ is propositional consequence with the formulas $L\varphi$ as atoms. Every expansion is stable and contains $A$. The definition is a fixed point, like the definition of an [extension](/default-extension/) in default logic: the candidate $T$ appears on both sides. Moore (1985) showed that the expansions are exactly the belief sets that are *sound* (every autoepistemic interpretation that makes $A$ true and reads $L$ by $T$ makes all of $T$ true) and *complete* (they contain every formula true in all such interpretations).

**A finite test.** Let $\Sigma$ be the set of the subformulas of $A$ of the form $L\varphi$. An expansion is determined by which members of $\Sigma$ it contains. For premises without nested $L$, a set $\Lambda \subseteq \Sigma$ gives an expansion exactly when, with $S_\Lambda = A \cup \Lambda \cup \{\neg L\varphi : L\varphi \in \Sigma \setminus \Lambda\}$,

$$L\varphi \in \Lambda \iff S_\Lambda \models \varphi \qquad \text{for each } L\varphi \in \Sigma.$$

The expansion is then the stable set whose objective part is the objective consequences of $S_\Lambda$. Niemelä's *full sets* extend this test to nested operators (Thomas and Vollmer 2010, Definition 4.4 and Proposition 4.5). So an expansion is found by guessing $\Lambda$ and making $|\Sigma|$ classical entailment tests.

## What it counts

For finite propositional premises $A$ and a formula $\varphi$, the tasks are:

- **Existence:** does $A$ have a stable expansion?
- **Credulous reasoning:** is $\varphi$ in some stable expansion?
- **Skeptical reasoning:** is $\varphi$ in every stable expansion?

The cost is measured in the size of $A$ and $\varphi$, with propositional satisfiability as the basic oracle.

### Examples

Each line uses the finite test with $\Sigma$ the set of the $L$-subformulas.

| Premises $A$ | Expansions | Why |
|---|---|---|
| $\mathit{b} \supset L\mathit{b}$ | one, with $\neg\mathit{b}$ | With $\Lambda = \emptyset$, $S_\Lambda$ entails $\neg\mathit{b}$ and not $\mathit{b}$. With $\Lambda = \{L\mathit{b}\}$, $S_\Lambda$ does not entail $\mathit{b}$. |
| $\neg Lp \supset q$ | one, with $q$ and $\neg Lp$ | Only $\Lambda = \emptyset$ passes. |
| $\neg Lp \supset p$ | none | $\Lambda = \emptyset$ gives $p$, and $\Lambda = \{Lp\}$ does not give $p$. |
| $Lp \supset p$ | two, one with $p$ and one without | Both $\Lambda = \emptyset$ and $\Lambda = \{Lp\}$ pass. |
| $\neg Lp \supset q,\ \neg Lq \supset p$ | two, $\{Lp, \neg Lq\}$ and $\{\neg Lp, Lq\}$ | The other two choices of $\Lambda$ fail. |

The first line is Moore's example: "if I had an older brother, I would know it", so in the absence of that belief the agent concludes that it has no older brother. The fourth line shows that an expansion need not be grounded: $p$ is believed only because $Lp$ is assumed. The default $p : p / p$ has only the extension without $p$.

## Relation to other models

- **[Default logic](/default-logic/).** A default $\alpha : \beta / \gamma$ can be written as the premise $L\alpha \wedge \neg L\neg\beta \supset \gamma$. Extensions and expansions are similar fixed points but not the same. Konolige (1988) showed that extensions correspond to a stricter, *strongly grounded* kind of expansion under this reading. The fourth example above shows the difference.
- **Logic programs.** Gelfond and Lifschitz (1988) read the rule $p \leftarrow q, \mathit{not}\ r$ as $q \wedge \neg L r \supset p$. Under this reading, the [stable models](/stable-model-semantics/) of a normal program are the objective atoms of the stable expansions, and [negation as failure](/negation-as-failure/) is "not believed".
- **Modal logic.** A stable set is the theory of a set of worlds that all see each other, so belief in a single expansion follows the axioms of the modal system KD45 for consistent sets. Autoepistemic logic adds the nonmonotonic fixed point on top.
- **[Circumscription](/circumscription/).** Circumscription minimizes truth in the models of the premises. Autoepistemic logic instead fixes what the agent believes, and the two coincide only on special inputs.

## Known results in the model

- **Complexity** (Niemelä 1990, Gottlob 1992; Thomas and Vollmer 2010, Theorem 4.6): for finite propositional premises, existence and credulous reasoning are $\Sigma_2^p$-complete, and skeptical reasoning is $\Pi_2^p$-complete. Membership follows from the finite test: guess $\Lambda$, then make polynomially many calls to a SAT oracle. The proof of hardness is the same pattern as for [default logic](/default-logic-complexity/).
- **No expansion or many.** As the examples show, a premise set can have no expansion, one, or several, so existence is a real question, unlike for normal default theories.
- **Stratified premises.** Gelfond (1987) studied premises that can be split into layers so that each $\neg L$ refers only to lower layers. Such premises have a unique expansion, which is computed layer by layer, in the same way as the unique stable model of a [stratified logic program](/stratified-logic-program/).
- **Algorithms.** The finite test gives a guess-and-check procedure. Practical systems search over $\Lambda$ with a SAT solver for the entailment tests, or translate the program fragment to [answer set programming](/answer-set-programming/).

## References
