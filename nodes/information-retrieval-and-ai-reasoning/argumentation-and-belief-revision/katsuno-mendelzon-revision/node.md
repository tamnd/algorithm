---
tag: H2PF3G
kind: theorem
slug: katsuno-mendelzon-revision
name: Katsuno-Mendelzon revision theorem
aliases:
- KM revision postulates
- faithful assignment theorem
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: Propositional revision operators satisfying the AGM postulates are exactly those that select minimal models under a faithful total preorder.
prereqs: [agm-postulates, grove-spheres]
see_also: [dalal-revision, agm-representation-theorem, epistemic-entrenchment, belief-update, darwiche-pearl-postulates, belief-merging, possible-models-approach, total-order]
sources:
  - paper: doi:10.1016/0004-3702(91)90069-V
    title: Hirofumi Katsuno and Alberto O. Mendelzon, Propositional knowledge base revision and minimal change, Artificial Intelligence 52(3), 263 to 294 (1991)
    locator: Section 3 (the postulates R1 to R6, faithful assignments and the representation theorem) and Section 5 (partial preorders)
  - paper: "Peter Gärdenfors, Belief revision: an introduction, in Peter Gärdenfors (ed.), Belief Revision, Cambridge University Press (1992)"
    locator: Theorem 13 (the result of Katsuno and Mendelzon stated for belief sets)
  - paper: doi:10.1007/BF00247909
    title: Adam Grove, Two modellings for theory change, Journal of Philosophical Logic 17(2), 157 to 170 (1988)
    locator: the whole paper (systems of spheres, the general form of the same result)
  - paper: doi:10.1016/0004-3702(92)90018-S
    title: Eiter and Gottlob, On the complexity of propositional knowledge base revision, updates, and counterfactuals, Artificial Intelligence 57(2-3), 227 to 270 (1992)
    locator: Section 3 (which of the operators of Dalal, Satoh, Borgida, Weber and others satisfy R1 to R6)
---

The Katsuno and Mendelzon theorem translates the [AGM postulates](/agm-postulates/) for revision into a statement about possible worlds, for a finite propositional language. Hirofumi Katsuno and Alberto Mendelzon (1991) wrote the postulates as six conditions R1 to R6 on an operator $\psi \circ \mu$ on formulas, and showed that an operator satisfies them if and only if it is given by a faithful assignment: each base $\psi$ gets a total preorder on worlds with the models of $\psi$ at the bottom, and $\psi \circ \mu$ has as its models the least models of $\mu$. It is the finite form of [Grove's spheres](/grove-spheres/), and it is the standard way to define and test concrete operators such as [Dalal's](/dalal-revision/).

## Statement

**Setting.** $L$ is a propositional language over a finite set of atoms. A world (an interpretation) assigns true or false to each atom, and $\mathcal{W}$ is the finite set of all worlds. $\mathrm{Mod}(\varphi) \subseteq \mathcal{W}$ is the set of models of a formula $\varphi$. For any set of worlds there is a formula with exactly those models; write $\mathrm{form}(I, J)$ for one whose models are $I$ and $J$. A revision operator maps two formulas $\psi$ (the base) and $\mu$ (the new information) to a formula $\psi \circ \mu$.

**The postulates.**

| | postulate |
|---|---|
| R1 | $\psi \circ \mu$ implies $\mu$ |
| R2 | if $\psi \wedge \mu$ is satisfiable, then $\psi \circ \mu \leftrightarrow \psi \wedge \mu$ |
| R3 | if $\mu$ is satisfiable, then $\psi \circ \mu$ is satisfiable |
| R4 | if $\psi_1 \leftrightarrow \psi_2$ and $\mu_1 \leftrightarrow \mu_2$, then $\psi_1 \circ \mu_1 \leftrightarrow \psi_2 \circ \mu_2$ |
| R5 | $(\psi \circ \mu) \wedge \varphi$ implies $\psi \circ (\mu \wedge \varphi)$ |
| R6 | if $(\psi \circ \mu) \wedge \varphi$ is satisfiable, then $\psi \circ (\mu \wedge \varphi)$ implies $(\psi \circ \mu) \wedge \varphi$ |

For $K = \mathrm{Cn}(\psi)$ and $K * \mu = \mathrm{Cn}(\psi \circ \mu)$, these say the same as K*1 to K*8 (Katsuno and Mendelzon 1991, Section 3).

**Faithful assignments.** A preorder is a reflexive and transitive relation, and it is total when any two elements are comparable. Write $I <_\psi J$ for $I \le_\psi J$ and not $J \le_\psi I$. An assignment that maps each formula $\psi$ to a preorder $\le_\psi$ on $\mathcal{W}$ is faithful when

1. if $I, J \in \mathrm{Mod}(\psi)$, then $I <_\psi J$ does not hold;
2. if $I \in \mathrm{Mod}(\psi)$ and $J \notin \mathrm{Mod}(\psi)$, then $I <_\psi J$;
3. if $\psi \leftrightarrow \phi$, then $\le_\psi = \le_\phi$.

For a set $S$ of worlds, $\mathrm{Min}(S, \le_\psi) = \{I \in S : \text{there is no } J \in S \text{ with } J <_\psi I\}$.

**Theorem** (Katsuno and Mendelzon 1991, Section 3). An operator $\circ$ satisfies R1 to R6 if and only if there is a faithful assignment of total preorders $\psi \mapsto \le_\psi$ such that for all $\psi$ and $\mu$

$$\mathrm{Mod}(\psi \circ \mu) = \mathrm{Min}(\mathrm{Mod}(\mu), \le_\psi).$$

## In plain words

Think of each set of beliefs as a ranking of all the possible situations, from "fits what I believe" down to "very surprising". The situations that fit the beliefs share the top place, and every other situation is below them. To take in a new fact, look at the situations where the fact holds and keep the best ranked of them. The theorem says that this recipe gives exactly the revision methods that obey the six rules. Every ranking gives a method that obeys them, and every method that obeys them comes from some ranking, which you can read off by asking the method to choose between two situations at a time.

## Proof

**From preorders to the postulates.** Let $\psi \mapsto \le_\psi$ be faithful and total, and define $\mathrm{Mod}(\psi \circ \mu) = \mathrm{Min}(\mathrm{Mod}(\mu), \le_\psi)$.

- R1: $\mathrm{Min}(S) \subseteq S$.
- R2: if $\mathrm{Mod}(\psi) \cap \mathrm{Mod}(\mu)$ is nonempty, then by condition 1 its members are equal in $\le_\psi$, and by condition 2 they are strictly below every other world. So they are exactly the minimal models of $\mu$.
- R3: a nonempty finite set has a minimal element under a total preorder.
- R4: by condition 3, and because $\mathrm{Min}$ depends only on $\mathrm{Mod}(\mu)$.
- R5 and R6: suppose $\mathrm{Min}(\mathrm{Mod}(\mu)) \cap \mathrm{Mod}(\varphi)$ holds a world $m$. Each world of this set is minimal in the smaller set $\mathrm{Mod}(\mu \wedge \varphi)$. Conversely, let $y$ be minimal in $\mathrm{Mod}(\mu \wedge \varphi)$. Then $y \le_\psi m$ because the preorder is total, and $m \le_\psi y$ because $m$ is minimal in $\mathrm{Mod}(\mu)$. So $y$ is equivalent to $m$, $y$ is minimal in $\mathrm{Mod}(\mu)$, and $y$ is in the set. So $\mathrm{Min}(\mathrm{Mod}(\mu \wedge \varphi)) = \mathrm{Min}(\mathrm{Mod}(\mu)) \cap \mathrm{Mod}(\varphi)$, which gives R5 and R6. If the intersection is empty, R5 is trivial and R6 does not apply.

**From the postulates to preorders.** Let $\circ$ satisfy R1 to R6. For each $\psi$ define

$$I \le_\psi J \quad\text{if and only if}\quad I \in \mathrm{Mod}(\psi \circ \mathrm{form}(I, J)).$$

By R4 this does not depend on the choice of $\mathrm{form}(I, J)$.

- *Total and reflexive.* By R1 and R3, $\mathrm{Mod}(\psi \circ \mathrm{form}(I, J))$ is a nonempty subset of $\{I, J\}$, so it holds $I$ or $J$. With $J = I$ it holds $I$.
- *A key step.* By R5 and R6, if $(\psi \circ \mu) \wedge \varphi$ is satisfiable, then $\psi \circ (\mu \wedge \varphi) \leftrightarrow (\psi \circ \mu) \wedge \varphi$.
- *Transitive.* Let $I \le_\psi J$ and $J \le_\psi H$, and let $R = \mathrm{Mod}(\psi \circ \mathrm{form}(I, J, H))$, a nonempty subset of $\{I, J, H\}$. If $I \in R$, the key step with $\varphi = \mathrm{form}(I, H)$ gives $I \in \mathrm{Mod}(\psi \circ \mathrm{form}(I, H))$, so $I \le_\psi H$. If $I \notin R$ but $J \in R$, the key step with $\varphi = \mathrm{form}(I, J)$ gives $\mathrm{Mod}(\psi \circ \mathrm{form}(I, J)) = \{J\}$, against $I \le_\psi J$. If $R = \{H\}$, the key step with $\varphi = \mathrm{form}(J, H)$ gives $\{H\}$, against $J \le_\psi H$.
- *Faithful.* If $I$ and $J$ are models of $\psi$, R2 gives $\mathrm{Mod}(\psi \circ \mathrm{form}(I, J)) = \{I, J\}$, so they are equivalent. If $I$ is a model of $\psi$ and $J$ is not, R2 gives $\{I\}$, so $I <_\psi J$. Condition 3 is R4.
- *It represents $\circ$.* If $\mu$ is unsatisfiable, both sides are empty by R1. Otherwise, let $I \in \mathrm{Mod}(\psi \circ \mu)$ and $J \in \mathrm{Mod}(\mu)$. The key step with $\varphi = \mathrm{form}(I, J)$ gives $I \in \mathrm{Mod}(\psi \circ \mathrm{form}(I, J))$, so $I \le_\psi J$, and $I$ is minimal. Conversely, let $I$ be minimal in $\mathrm{Mod}(\mu)$ and suppose $I \notin \mathrm{Mod}(\psi \circ \mu)$. Take $J \in \mathrm{Mod}(\psi \circ \mu)$, by R3. The key step gives $\mathrm{Mod}(\psi \circ \mathrm{form}(I, J)) = \{J\}$, so $J <_\psi I$, against the minimality of $I$. $\square$

**Checks on small languages.** Fix two atoms and $\psi = a \wedge b$. An operator for this $\psi$ that satisfies R1 to R4 must give $\psi \wedge \mu$ when it is satisfiable, and any nonempty subset of $\mathrm{Mod}(\mu)$ for each of the 7 satisfiable $\mu$ that exclude $ab$. That makes $3^3 \cdot 7 = 189$ operators. Exactly 13 of them satisfy R5 and R6, one for each of the 13 total preorders on the other three worlds. For Dalal's operator, the preorder built in the second half of the proof is the Hamming distance to $\mathrm{Mod}(\psi)$, and it reproduces the operator on every $\mu$.

## Consequences

- **Concrete operators.** To show that an operator satisfies the AGM postulates, it is enough to exhibit the preorders. [Dalal's operator](/dalal-revision/) uses $I \le_\psi J$ if and only if $\mathrm{dist}(I, \mathrm{Mod}\,\psi) \le \mathrm{dist}(J, \mathrm{Mod}\,\psi)$, with the Hamming distance. Weighted distances work the same way.
- **The postulates fix one preorder per base and no more.** Nothing ties $\le_\psi$ to $\le_{\psi \circ \mu}$. Rules for that link are the [Darwiche and Pearl postulates](/darwiche-pearl-postulates/) for iterated revision.
- **Update is different.** Katsuno and Mendelzon also characterized [update](/belief-update/) by a preorder for each world rather than for each base, and showed that it is a different operation, with different postulates.
- **Merging.** The same method, with an assignment from profiles of bases to preorders, characterizes [belief merging](/belief-merging/) operators.

## Tightness

- **Totality is needed for R6.** Satoh's operator compares the sets of atoms that change by inclusion, which gives a partial preorder. It satisfies R1 to R5 but not R6 (Eiter and Gottlob 1992, Section 3). Over three atoms, take $\psi = \neg a \wedge \neg b \wedge \neg c$, let $\mu$ have the models $\{a\}$, $\{b\}$ and $\{b, c\}$, each written as its set of true atoms, and let $\varphi$ have the models $\{a\}$ and $\{b, c\}$. Satoh's operator gives $\psi \circ \mu$ the models $\{a\}$ and $\{b\}$, so $(\psi \circ \mu) \wedge \varphi$ has the one model $\{a\}$. But $\psi \circ (\mu \wedge \varphi)$ has the models $\{a\}$ and $\{b, c\}$, since $\{b, c\}$ is minimal once $\{b\}$ is gone. Dalal's operator gives $\{a\}$ in both cases. For partial preorders, Katsuno and Mendelzon (Section 5) give a matching theorem with R1 to R5 and two other postulates in place of R6.
- **Condition 2 is needed for R2.** Over two atoms, let $\psi$ have the one model $a \bar b$ (with $\bar b$ for "$b$ is false"), and give the world $ab$ the same rank as $a \bar b$. Then $\mu = a$ is consistent with $\psi$, but the operator returns both models of $a$, not $\psi \wedge \mu$.
- **Finiteness is used** to have a formula for each set of worlds and a minimum in each nonempty set. For an infinite language, Grove's systems of spheres take the place of the preorders, and condition S4 asks for the minimum explicitly.

## History

Grove (1988) had characterized the AGM revisions by systems of spheres over maximal consistent sets. Katsuno and Mendelzon (1991) brought the result to knowledge bases in computer science: they fixed a finite language, used formulas for belief sets, and replaced spheres by preorders on interpretations, which made it easy to classify the operators proposed in AI. The same year they separated revision from update at KR'91. Eiter and Gottlob (1992) used R1 to R6 to classify the operators of Dalal, Satoh, Borgida, Weber and others before analysing their complexity.

## References
