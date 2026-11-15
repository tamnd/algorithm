---
tag: 7P7T6P
kind: problem
slug: belief-update
name: Belief update
aliases:
- Katsuno-Mendelzon update
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: Change beliefs to record that the world itself has changed, by revising each model of the old beliefs separately.
prereqs: [belief-revision, katsuno-mendelzon-revision]
see_also: [possible-models-approach, dalal-revision, agm-postulates, frame-problem, situation-calculus, belief-merging, polynomial-hierarchy]
sources:
  - paper: "Hirofumi Katsuno and Alberto O. Mendelzon, On the difference between updating a knowledge base and revising it, in James Allen, Richard Fikes and Erik Sandewall (eds), Proceedings of the Second International Conference on Principles of Knowledge Representation and Reasoning (KR'91), Morgan Kaufmann, 387 to 394 (1991)"
    locator: the whole paper (the postulates U1 to U8, the representation theorem with faithful assignments of preorders, one for each interpretation, and the book and magazine example); reprinted in Peter Gärdenfors (ed.), Belief Revision, Cambridge University Press (1992)
  - paper: "Marianne Winslett, Reasoning about action using a possible models approach, Proceedings of the Seventh National Conference on Artificial Intelligence (AAAI-88), 89 to 93 (1988)"
    locator: p. 90, Section 3 (the possible models approach, which changes each model of the theory separately)
  - paper: doi:10.1016/0004-3702(92)90018-S
    title: Thomas Eiter and Georg Gottlob, On the complexity of propositional knowledge base revision, updates, and counterfactuals, Artificial Intelligence 57(2-3), 227 to 270 (1992)
    locator: Section 3 (the update operators of Winslett and Forbus), Theorem 6.4 (the general case), Theorems 7.2 and 7.3 (Horn formulas)
---

Belief update is the problem of changing a knowledge base when the world has changed. It differs from [belief revision](/belief-revision/), where the world is fixed and the agent learns more about it. Hirofumi Katsuno and Alberto Mendelzon made the difference precise in 1991. They gave eight postulates, U1 to U8, for an update operator $\psi \diamond \mu$, and proved that the operators that satisfy them are exactly those that move each model of $\psi$ on its own to the closest models of $\mu$, under an order of closeness for each world. The [possible models approach](/possible-models-approach/) of Winslett is the standard example.

## In plain words

Your notes describe a room, but you are not sure of everything, so the notes allow several states of the room. Then someone does something, and now a new fact is true. Revision would ask: which of my possible states already fit the fact? Update asks something else: for each possible state, what would it look like after the smallest change that makes the fact true?

So if the new fact already holds in one of your states, revision drops the other states, but update keeps them all and moves each one. The book was maybe on the table and maybe not. Someone puts it on the table. You now know the book is there, and you have learned nothing about anything else in the room.

## Definition

Fix a finite propositional language. $\mathrm{Mod}(\psi)$ is the set of the models of $\psi$, and $\psi$ is complete when it has exactly one model. An update operator maps two formulas $\psi$ (the knowledge base) and $\mu$ (the new fact) to a formula $\psi \diamond \mu$. The postulates of Katsuno and Mendelzon (1991, KR) are:

| | postulate |
|---|---|
| U1 | $\psi \diamond \mu$ implies $\mu$. |
| U2 | If $\psi$ implies $\mu$, then $\psi \diamond \mu \equiv \psi$. |
| U3 | If $\psi$ and $\mu$ are satisfiable, then $\psi \diamond \mu$ is satisfiable. |
| U4 | If $\psi_1 \equiv \psi_2$ and $\mu_1 \equiv \mu_2$, then $\psi_1 \diamond \mu_1 \equiv \psi_2 \diamond \mu_2$. |
| U5 | $(\psi \diamond \mu) \wedge \phi$ implies $\psi \diamond (\mu \wedge \phi)$. |
| U6 | If $\psi \diamond \mu_1$ implies $\mu_2$ and $\psi \diamond \mu_2$ implies $\mu_1$, then $\psi \diamond \mu_1 \equiv \psi \diamond \mu_2$. |
| U7 | If $\psi$ is complete, then $(\psi \diamond \mu_1) \wedge (\psi \diamond \mu_2)$ implies $\psi \diamond (\mu_1 \vee \mu_2)$. |
| U8 | $(\psi_1 \vee \psi_2) \diamond \mu \equiv (\psi_1 \diamond \mu) \vee (\psi_2 \diamond \mu)$. |

U8 is the heart of update: each possible state of the world is updated on its own. U2 replaces the revision postulate R2, "if $\psi \wedge \mu$ is satisfiable then $\psi \circ \mu \equiv \psi \wedge \mu$", which update does not satisfy. Note that U2 makes an inconsistent base stay inconsistent, since an unsatisfiable $\psi$ implies every $\mu$.

**Representation.** A faithful assignment for update gives each interpretation $I$ a partial preorder $\le_I$ on interpretations such that $I <_I J$ for every $J \ne I$. Katsuno and Mendelzon prove that $\diamond$ satisfies U1 to U8 if and only if there is a faithful assignment with

$$\mathrm{Mod}(\psi \diamond \mu) = \bigcup_{I \in \mathrm{Mod}(\psi)} \mathrm{Min}(\mathrm{Mod}(\mu), \le_I).$$

With total preorders, the same holds for the postulates U1 to U6, U8 and U9, where U9 says: if $\psi$ is complete and $(\psi \diamond \mu_1) \wedge \mu_2$ is satisfiable, then $\psi \diamond (\mu_1 \wedge \mu_2)$ implies $(\psi \diamond \mu_1) \wedge \mu_2$.

Compare the [Katsuno and Mendelzon theorem for revision](/katsuno-mendelzon-revision/): there one preorder $\le_\psi$ is attached to the whole base, and $\mathrm{Mod}(\psi \circ \mu) = \mathrm{Min}(\mathrm{Mod}(\mu), \le_\psi)$.

The computational problem for a fixed operator is: given $\psi$, $\mu$ and $q$, does $\psi \diamond \mu$ entail $q$?

## Variants

- **Erasure.** Katsuno and Mendelzon also define erasure, which removes a fact in the way that update adds one. It stands to update as contraction stands to revision.
- **Partial or total preorders.** With a partial preorder for each world, as in the possible models approach, the operator satisfies U1 to U8 but may fail U9. With a total preorder, for example a distance, it satisfies U9.
- **Integrity constraints.** Laws of the domain, which Winslett calls protected formulas, must hold in every state after the update.
- **Actions with conditions.** In reasoning about action, an update is the effect of an action. The [frame problem](/frame-problem/) is the question of what stays the same, and the [situation calculus](/situation-calculus/) answers it with explicit axioms instead of a closeness order.
- **Iterated update.** U8 makes repeated updates easy to define: each world is updated by each new fact in turn.

## Examples

**The book and the magazine** (Katsuno and Mendelzon 1991, KR). Let $b$ say that the book is on the table and $m$ that the magazine is. The base is $\psi = (b \wedge \neg m) \vee (\neg b \wedge m)$ and the new fact is $\mu = b$. Take the [Hamming distance](/hamming-distance/) between worlds as the closeness.

| operator | world $b \wedge \neg m$ goes to | world $\neg b \wedge m$ goes to | result |
|---|---|---|---|
| update (each world on its own) | $b \wedge \neg m$ | $b \wedge m$ | $b$ |
| [Dalal's revision](/dalal-revision/) (the whole base) | | | $b \wedge \neg m$ |

Both results are right for their reading. If a robot was told to put the book on the table, the magazine has not moved, so it may still be on the table, and the update is right. If the agent only learned that the book is on the table, the old knowledge says that the magazine is not, and the revision is right.

**An action with an uncertain start.** Take the atoms $a$, $b$ and $c$, the base $\psi = \neg a \wedge (b \leftrightarrow c)$ with the two models $000$ and $011$, and the fact $\mu = (a \wedge \neg b \wedge \neg c) \vee (\neg a \wedge b \wedge c)$. The possible models approach moves $000$ to both $100$ and $011$, because the change sets $\{a\}$ and $\{b, c\}$ are not comparable by inclusion, and keeps $011$. The update is $\mu$. A revision keeps $\neg a \wedge b \wedge c$ alone.

**A failure of U9.** With the possible models approach and the base $000$, let $\mu_1$ have the models $100$, $011$ and $110$, and $\mu_2$ the models $011$ and $110$. Then $\psi \diamond \mu_1$ has the models $100$ and $011$, since $110$ changes $\{a, b\}$, which contains the change $\{a\}$ to $100$. So $(\psi \diamond \mu_1) \wedge \mu_2$ is $011$ alone. But $\psi \diamond (\mu_1 \wedge \mu_2)$ keeps both $011$ and $110$, whose change sets $\{b, c\}$ and $\{a, b\}$ are not comparable. U9 fails, as it may for a partial preorder.

## Known algorithms

- **[The possible models approach](/possible-models-approach/).** Compare change sets by inclusion for each model of $\psi$. On model sets over $n$ atoms it takes $O(k \cdot n \cdot 2^n)$ time for $k$ models of $\psi$.
- **Forbus's update.** Compare change sets by size, the Hamming distance, for each model of $\psi$. A breadth-first search from each model, in the manner of [Dalal's operator](/dalal-revision/), finds the nearest models of $\mu$.
- **Any faithful assignment.** Given a preorder for each world, the update is the union of the minimal models of $\mu$ for each model of $\psi$. The work is one minimum search for each model of $\psi$.
- **On formulas.** Entailment is checked by looking for a counterexample: a model $w$ of $\psi$ and a model $v$ of $\mu \wedge \neg q$ that is minimal for $w$. Minimality is a coNP test, so a [SAT](/sat/) solver inside a search for $w$ and $v$ decides the problem.

## Bounds

For formulas $\psi$, $\mu$ and $q$, "does $\psi \diamond \mu$ entail $q$" is $\Pi_2^P$-complete for both Winslett's and Forbus's operators (Eiter and Gottlob 1992, Theorem 6.4). For Horn formulas, Winslett's operator drops to coNP-complete (Theorem 7.2), while Forbus's stays $\Pi_2^P$-complete (Theorem 7.3). These classes are in the [polynomial hierarchy](/polynomial-hierarchy/). Every operator that satisfies U2 is coNP-hard: with $\psi$ and $\mu$ both tautologies, U2 makes $\psi \diamond \mu$ a tautology, and the question becomes whether $q$ is valid.

On explicit model sets the problem is easy: with $2^n$ worlds and a preorder for each that can be evaluated in polynomial time, the update takes time polynomial in $2^n$.

## Reductions

- **To complete bases.** By U8, the update of $\psi$ is the "or" of the updates of its models, each a complete base. So it is enough to define and compute updates of single worlds.
- **To revision of single worlds.** For a complete base, an update with total preorders picks the least models of $\mu$ in one total preorder in which the world itself is least. That is a revision of the complete base in the sense of the [Katsuno and Mendelzon theorem](/katsuno-mendelzon-revision/). So update is revision done world by world.
- **From reasoning about action.** An action with the postcondition $\mu$ is modelled as the update by $\mu$, as in Winslett (1988). The protected formulas become part of $\mu$.

## Applications

- Databases with incomplete information, where a transaction changes the world and the database holds a disjunction of possible states.
- Reasoning about the effects of actions in planning and robotics, where the start state is not fully known.
- Keeping a model of a changing system, such as a network or a device, when an event is reported.
- Counterfactual conditionals, "if $\mu$ were true then $q$", which Eiter and Gottlob (1992) study together with revision and update.

## References
