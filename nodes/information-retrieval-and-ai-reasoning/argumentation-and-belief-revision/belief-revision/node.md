---
tag: T8HCQR
kind: problem
slug: belief-revision
name: Belief revision
aliases:
- theory revision
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: intro
summary: Change a consistent belief set to accept a new piece of information while keeping consistency and losing as little as possible.
see_also: [agm-postulates, levi-identity, partial-meet-contraction, grove-spheres, katsuno-mendelzon-revision, dalal-revision, belief-update, nonmonotonic-reasoning]
sources:
  - paper: doi:10.2307/2274239
    title: "Carlos E. Alchourrón, Peter Gärdenfors and David Makinson, On the logic of theory change: partial meet contraction and revision functions, Journal of Symbolic Logic 50(2), 510 to 530 (1985)"
    locator: the whole paper (the postulates for contraction and revision, partial meet contraction and the Levi identity)
  - book: isbn:9780262071093
    title: "Peter Gärdenfors, Knowledge in Flux: Modeling the Dynamics of Epistemic States, MIT Press (1988)"
    locator: Chapter 3 (expansion, revision and contraction and their postulates)
  - paper: "Peter Gärdenfors, Belief revision: an introduction, in Peter Gärdenfors (ed.), Belief Revision, Cambridge University Press (1992)"
    locator: Section 2.1 (the logic of belief sets) and Sections 3.1 to 3.4 (the postulates and Theorems 1 to 8)
  - paper: doi:10.1016/0004-3702(91)90069-V
    title: Hirofumi Katsuno and Alberto O. Mendelzon, Propositional knowledge base revision and minimal change, Artificial Intelligence 52(3), 263 to 294 (1991)
    locator: Section 3 (the postulates R1 to R6 for a finite propositional language and their representation)
  - paper: "Hirofumi Katsuno and Alberto O. Mendelzon, On the difference between updating a knowledge base and revising it, in James Allen, Richard Fikes and Erik Sandewall (eds), Proceedings of the Second International Conference on Principles of Knowledge Representation and Reasoning (KR'91), Morgan Kaufmann, 387 to 394 (1991)"
    locator: the whole paper (revision against update, with the book and magazine example); reprinted in Peter Gärdenfors (ed.), Belief Revision, Cambridge University Press (1992)
  - paper: doi:10.1016/0004-3702(92)90018-S
    title: Thomas Eiter and Georg Gottlob, On the complexity of propositional knowledge base revision, updates, and counterfactuals, Artificial Intelligence 57(2-3), 227 to 270 (1992)
    locator: Theorems 6.4, 6.6, 6.7 and 6.9 (the complexity of the main operators) and Section 7 (Horn bases)
---

Belief revision is the problem of changing what an agent believes when it learns something that may contradict its beliefs. The new information must be accepted, the result must be consistent when the new information is consistent, and the change must be as small as possible. The last requirement has no single formal meaning, so the problem is usually stated through postulates, the [AGM postulates](/agm-postulates/), and through the families of operators that satisfy them. This page states the problem and gives an overview of the operators and of the cost of computing them. Each part has its own page.

## In plain words

You hold a set of beliefs that fit together. Then you learn a new fact, and you decide to trust it. If the fact fits your beliefs, just add it and draw the new conclusions. If it clashes with them, something old must go, and the question is what. Giving up everything is safe but foolish. Giving up the wrong things is also bad. A good method gives up as little as it can, and it gives up the beliefs that you hold less firmly.

There are many reasonable methods, and they can give different answers. So the theory does two things. It lists rules that every good method should follow. Then it shows which methods follow them, and how hard each method is to compute.

## Definition

Fix a language $L$ of sentences with a consequence operation $\mathrm{Cn}$. In the AGM theory, $\mathrm{Cn}$ is Tarskian (it satisfies $A \subseteq \mathrm{Cn}(A)$, monotony and $\mathrm{Cn}(\mathrm{Cn}(A)) = \mathrm{Cn}(A)$), includes classical propositional logic, is compact and satisfies the deduction theorem (Gärdenfors 1992, Section 2.1). A belief set is a set $K$ of sentences with $K = \mathrm{Cn}(K)$. The inconsistent belief set, the set of all sentences, is written $K_\bot$.

Three operations change a belief set by a sentence $p$:

- **Expansion** $K + p = \mathrm{Cn}(K \cup \{p\})$. It is determined by $K$ and $p$.
- **Revision** $K * p$ is a belief set that contains $p$, is consistent when $p$ is consistent, and keeps as much of $K$ as it can.
- **Contraction** $K \div p$ is a belief set inside $K$ that does not contain $p$ when $p$ is not a tautology, and keeps as much of $K$ as it can.

The problem is to choose a revision function $*$, that is, a function from belief sets and sentences to belief sets. The postulates K*1 to K*8 on [the AGM postulates page](/agm-postulates/) are the accepted criteria. The [Levi identity](/levi-identity/) $K * p = (K \div \neg p) + p$ reduces revision to contraction.

In the finite case the language has $n$ atoms. A belief set is then given by one formula $\psi$ with $K = \mathrm{Cn}(\psi)$, or by its set of models $\mathrm{Mod}(\psi) \subseteq \{0,1\}^n$, and the operator is written $\psi \circ \mu$. The computational question for a fixed operator $\circ$ is:

> Given formulas $\psi$, $\mu$ and $q$, does $\psi \circ \mu$ entail $q$?

## Variants

- **Contraction.** Remove $p$ without adding anything. Revision and contraction define each other by the Levi identity and the Harper identity $K \div p = K \cap (K * \neg p)$.
- **Base revision.** The beliefs are a finite set of sentences that is not closed under $\mathrm{Cn}$, and the result depends on how the sentences are written. Formula-based operators such as WIDTIO ("when in doubt, throw it out") work on bases.
- **Iterated revision.** The input is an epistemic state with a plausibility order, not only a belief set, and the operator must also give the new order. See the [Darwiche and Pearl postulates](/darwiche-pearl-postulates/) and [ordinal conditional functions](/ordinal-conditional-functions/).
- **Update.** The world has changed, rather than the agent's knowledge of it. Each model of the old beliefs is changed separately. See [belief update](/belief-update/).
- **Merging.** Several bases of equal standing are combined. See [belief merging](/belief-merging/).

## Examples

Take two atoms $a$ and $b$, the belief set $K = \mathrm{Cn}(a \wedge b)$, and revise by $\neg a$.

- **Full meet revision** keeps nothing of $K$ when there is a conflict: $K * \neg a = \mathrm{Cn}(\neg a)$. It satisfies all eight AGM postulates, but it forgets $b$.
- **[Dalal's operator](/dalal-revision/)** changes as few atoms as possible: $K * \neg a = \mathrm{Cn}(\neg a \wedge b)$.
- **A non-example.** The operator $K * p = \mathrm{Cn}(p)$ for every $K$ and $p$ satisfies every postulate except K*4: it forgets all of $K$ even when $p$ is consistent with it.

The difference between revision and update shows in the book and magazine example of Katsuno and Mendelzon (1991, KR). A room has a book and a magazine, and the agent knows that exactly one of them is on the table: $\psi = (b \wedge \neg m) \vee (\neg b \wedge m)$. Now the agent learns $\mu = b$, the book is on the table.

| reading | result |
|---|---|
| revision: the agent was told more about a world that did not change | $b \wedge \neg m$ |
| update: a robot was told to put the book on the table | $b$ |

Under revision, $\mu$ is consistent with $\psi$, so postulate K*4 forces the result $\psi \wedge \mu = b \wedge \neg m$. Under update, the world where the magazine was on the table is moved to the nearest world with the book on the table, $b \wedge m$, and nothing is known about the magazine any more. Both rows follow from the Hamming distance on the four worlds over $b$ and $m$.

## Known algorithms

- **Selection among remainders.** [Partial meet contraction](/partial-meet-contraction/) intersects some of the maximal subsets of $K$ that do not imply $p$, and the Levi identity turns it into revision.
- **Entrenchment.** An [epistemic entrenchment](/epistemic-entrenchment/) order on sentences gives the contraction: keep $q$ when $p < p \vee q$.
- **Spheres and preorders.** A [system of spheres](/grove-spheres/), or a faithful total preorder on worlds as in the [Katsuno and Mendelzon theorem](/katsuno-mendelzon-revision/), gives $\mathrm{Mod}(\psi \circ \mu)$ as the least models of $\mu$.
- **Distance-based operators.** Dalal's operator ranks worlds by Hamming distance from $\mathrm{Mod}(\psi)$, and on model sets it is a breadth-first search over the cube $\{0,1\}^n$. Satoh's and Borgida's operators compare the sets of changed atoms by inclusion.

## Bounds

For formulas $\psi$, $\mu$ and $q$, the entailment problem above is hard for most operators (Eiter and Gottlob 1992):

| operator | complexity of "does $\psi \circ \mu$ entail $q$" |
|---|---|
| Dalal | $\mathrm{P}^{\mathrm{NP}[O(\log n)]}$-complete (Theorem 6.9) |
| Satoh, Borgida, Winslett, Forbus, Ginsberg | $\Pi_2^P$-complete (Theorem 6.4) |
| Weber, WIDTIO | $\Pi_2^P$-hard and in $\mathrm{P}^{\Sigma_2^P[O(\log n)]}$ (Theorems 6.6 and 6.7) |

When all formulas are Horn, Dalal's operator stays $\mathrm{P}^{\mathrm{NP}[O(\log n)]}$-complete (Theorem 7.4) and Forbus's stays $\Pi_2^P$-complete (Theorem 7.3), while Ginsberg's, Winslett's, Borgida's and Satoh's drop to coNP-complete (Theorem 7.2). These classes are in the [polynomial hierarchy](/polynomial-hierarchy/). Every operator that satisfies postulate R2 is [coNP](/co-np/)-hard: when $\psi$ and $\mu$ are both tautologies, R2 makes $\psi \circ \mu$ a tautology, and the question becomes whether $q$ is a tautology.

## Reductions

- **To and from counterfactuals.** Read the conditional "if $\mu$ were true then $q$ would be" as $q \in K * \mu$, the Ramsey test. Eiter and Gottlob treat the evaluation of such conditionals and the entailment problem for revision as the same task. The [Gärdenfors impossibility theorem](/gardenfors-impossibility-theorem/) shows that this reading cannot put the conditionals inside the belief sets when revision satisfies preservation.
- **To nonmonotonic inference.** For a fixed $K$, define "$p$ normally gives $q$" as $q \in K * p$. The AGM postulates then give an inference relation of the rational kind studied in [nonmonotonic reasoning](/nonmonotonic-reasoning/), as in [rational closure](/rational-closure/).
- **To SAT.** For Dalal's operator, a binary search on the distance with a [SAT](/sat/) solver as oracle decides entailment with $O(\log n)$ calls.

## Applications

- Updating a knowledge base or a database when a new fact contradicts it.
- Repair of a configuration or of an inconsistent data record, where each atom is one value that may be wrong.
- Model-based diagnosis, where an observation contradicts the assumption that all parts work; see [consistency-based diagnosis](/consistency-based-diagnosis/).
- Reason maintenance systems, which keep the record of why each belief is held so that it can be retracted; see the [justification-based truth maintenance system](/justification-based-truth-maintenance/).
- The theory of scientific change and of conditionals in philosophy, where the AGM theory began.

## References
