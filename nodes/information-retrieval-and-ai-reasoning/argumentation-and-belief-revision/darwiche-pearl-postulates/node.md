---
tag: 7DM126
kind: definition
slug: darwiche-pearl-postulates
name: Darwiche-Pearl postulates
aliases:
- iterated revision postulates
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: research
summary: Postulates on how revision changes the plausibility ordering of an epistemic state, so that sequences of revisions behave well.
prereqs: [katsuno-mendelzon-revision, agm-postulates]
see_also: [ordinal-conditional-functions, grove-spheres, belief-revision, epistemic-entrenchment, dalal-revision, system-z]
sources:
  - paper: doi:10.1016/S0004-3702(96)00038-0
    title: Adnan Darwiche and Judea Pearl, On the logic of iterated belief revision, Artificial Intelligence 89(1-2), 1 to 29 (1997)
    locator: the whole paper (epistemic states, the postulates R*1 to R*6 and C1 to C4, the representation of C1 to C4 by the conditions on faithful assignments, and the revision of ranking functions)
  - paper: "Adnan Darwiche and Judea Pearl, On the logic of iterated belief revision, in Ronald Fagin (ed.), Proceedings of the Fifth Conference on Theoretical Aspects of Reasoning about Knowledge (TARK 1994), Morgan Kaufmann, 5 to 23 (1994)"
    locator: the first version, with the postulates stated on belief sets
  - paper: doi:10.1016/0004-3702(91)90069-V
    title: Hirofumi Katsuno and Alberto O. Mendelzon, Propositional knowledge base revision and minimal change, Artificial Intelligence 52(3), 263 to 294 (1991)
    locator: Section 3 (faithful assignments of total preorders and the postulates R1 to R6)
  - paper: doi:10.1007/978-94-009-2865-7_6
    title: "Wolfgang Spohn, Ordinal conditional functions: a dynamic theory of epistemic states, in William L. Harper and Brian Skyrms (eds), Causation in Decision, Belief Change, and Statistics, vol. II, Kluwer, Dordrecht, 105 to 134 (1988)"
    locator: the whole paper (the problem of iterated change and the A,n-conditionalization of ranking functions)
---

The AGM postulates say how one revision changes a belief set, but they say almost nothing about the next revision. Two agents with the same beliefs can react differently to a second piece of news, because their beliefs come from different orders of plausibility. Adnan Darwiche and Judea Pearl (1997) moved revision from belief sets to epistemic states, which carry such an order, and added four postulates, C1 to C4, on how a revision may change the order. Their main theorem translates C1 to C4 into four simple conditions on the total preorders of a faithful assignment.

## Definition

**Epistemic states.** Fix a finite propositional language and its set $W$ of worlds. An epistemic state $\Psi$ has a belief set $\mathrm{Bel}(\Psi)$, given by a formula. A revision operator maps an epistemic state $\Psi$ and a formula $\mu$ to a new epistemic state $\Psi \circ \mu$. We write $\Psi \circ \mu \models \alpha$ for $\mathrm{Bel}(\Psi \circ \mu) \models \alpha$. The operator must satisfy the postulates R*1 to R*6 of Darwiche and Pearl. They are the postulates R1 to R6 of Katsuno and Mendelzon with $\psi$ replaced by $\mathrm{Bel}(\Psi)$, except that R*4 asks for equal results only when the two epistemic states are equal, not when their belief sets are equivalent.

**The postulates.** For all epistemic states $\Psi$ and formulas $\mu$ and $\alpha$:

| | postulate | reading |
|---|---|---|
| C1 | If $\alpha \models \mu$, then $(\Psi \circ \mu) \circ \alpha \equiv \Psi \circ \alpha$. | A later, stronger fact makes the earlier one redundant. |
| C2 | If $\alpha \models \neg \mu$, then $(\Psi \circ \mu) \circ \alpha \equiv \Psi \circ \alpha$. | A later fact that contradicts the earlier one wipes out its effect. |
| C3 | If $\Psi \circ \alpha \models \mu$, then $(\Psi \circ \mu) \circ \alpha \models \mu$. | Learning $\mu$ first does not stop $\alpha$ from giving $\mu$. |
| C4 | If $\Psi \circ \alpha \not\models \neg \mu$, then $(\Psi \circ \mu) \circ \alpha \not\models \neg \mu$. | Learning $\mu$ first does not make $\alpha$ give $\neg \mu$. |

Here $\equiv$ compares belief sets.

**Faithful assignments.** A faithful assignment maps each epistemic state $\Psi$ to a total preorder $\le_\Psi$ on $W$ whose least worlds are the models of $\mathrm{Bel}(\Psi)$. As in the [Katsuno and Mendelzon theorem](/katsuno-mendelzon-revision/), $\circ$ satisfies R*1 to R*6 if and only if there is a faithful assignment with $\mathrm{Mod}(\Psi \circ \mu) = \min(\mathrm{Mod}(\mu), \le_\Psi)$.

**Representation theorem** (Darwiche and Pearl 1997). Let $\circ$ satisfy R*1 to R*6, with the faithful assignment $\Psi \mapsto {\le_\Psi}$. Then $\circ$ satisfies C1, C2, C3 or C4 if and only if, for all worlds $w_1$ and $w_2$, the matching condition holds:

| | condition on the preorder before ($\le_\Psi$) and after ($\le_{\Psi \circ \mu}$) |
|---|---|
| CR1 | If $w_1 \models \mu$ and $w_2 \models \mu$, then $w_1 \le_\Psi w_2$ if and only if $w_1 \le_{\Psi \circ \mu} w_2$. |
| CR2 | If $w_1 \models \neg \mu$ and $w_2 \models \neg \mu$, then $w_1 \le_\Psi w_2$ if and only if $w_1 \le_{\Psi \circ \mu} w_2$. |
| CR3 | If $w_1 \models \mu$ and $w_2 \models \neg \mu$, then $w_1 <_\Psi w_2$ implies $w_1 <_{\Psi \circ \mu} w_2$. |
| CR4 | If $w_1 \models \mu$ and $w_2 \models \neg \mu$, then $w_1 \le_\Psi w_2$ implies $w_1 \le_{\Psi \circ \mu} w_2$. |

In words: revising by $\mu$ keeps the order among the $\mu$-worlds and among the $\neg \mu$-worlds, and a $\mu$-world never loses ground against a $\neg \mu$-world. Each postulate matches one condition, so the four can be adopted one at a time.

## Examples and non-examples

Use ranks for the preorders: a rank function $\kappa : W \to \mathbb{N}$ with some world of rank 0 gives $w_1 \le w_2$ when $\kappa(w_1) \le \kappa(w_2)$, and the belief set is the set of the worlds of rank 0. Write $\kappa(\mu)$ for the least rank of a model of $\mu$. The operators below were checked against C1 to C4 by a script, on random ranks over 3 atoms and on the cases shown.

- **The operator of Darwiche and Pearl.** Set $\kappa'(w) = \kappa(w) - \kappa(\mu)$ for $w \models \mu$ and $\kappa'(w) = \kappa(w) + 1$ for $w \models \neg \mu$. The $\mu$-worlds move down together and the $\neg \mu$-worlds move up together, so CR1 and CR2 hold, and no $\mu$-world falls behind a $\neg \mu$-world, so CR3 and CR4 hold. It satisfies C1 to C4.
- **Natural revision** (Boutilier). Move the least $\mu$-worlds to the bottom and keep the order of all other worlds. It satisfies C1 to C4, and only the least $\mu$-worlds change their place.
- **Lexicographic revision** (Nayak). Put every $\mu$-world below every $\neg \mu$-world, and keep the old order inside each group. It satisfies C1 to C4, and it also gives the latest fact priority over all older ones.
- **Non-example: forgetting the order.** After the revision, give rank 0 to the least $\mu$-worlds and rank 1 to all other worlds. This satisfies R*1 to R*6, since each single revision is right, but it breaks C1, C2 and C3. Take three worlds $w_1$, $w_2$ and $w_3$ with ranks 0, 1 and 2, and let $\mu$ have the single model $w_2$. After the revision, $w_2$ has rank 0 and both $w_1$ and $w_3$ have rank 1. Now let $\alpha$ have the models $w_1$ and $w_3$, so $\alpha \models \neg \mu$. Before, $\Psi \circ \alpha$ selects $w_1$. After, $(\Psi \circ \mu) \circ \alpha$ selects both $w_1$ and $w_3$, so C2 fails, and CR2 fails for $w_1$ and $w_3$.
- **Non-example: Spohn conditionalization with a fixed firmness.** The $(\mu, n)$-conditionalization of [ordinal conditional functions](/ordinal-conditional-functions/) sets $\kappa'(w) = \kappa(w) - \kappa(\mu)$ on $\mu$-worlds and $\kappa'(w) = \kappa(w) - \kappa(\neg \mu) + n$ on $\neg \mu$-worlds. Take four worlds with ranks $\kappa(w_0) = 0$, $\kappa(w_1) = 4$, $\kappa(w_2) = 5$ and $\kappa(w_3) = 6$, let $\mu$ have the models $w_0$ and $w_1$, and use $n = 1$. Then $\mu$ was believed with firmness 5, and the conditionalization lowers it to 1: the new ranks are 0, 4, 1 and 2. For $\alpha$ with the models $w_1$ and $w_2$, $\Psi \circ \alpha$ selects $w_1$, which satisfies $\mu$, but $(\Psi \circ \mu) \circ \alpha$ selects $w_2$, which does not. So C3 fails, and CR3 fails for $w_1$ and $w_2$. Revising by a belief that is already held can weaken it, which C1 to C4 forbid.

## Related definitions

- **The AGM and KM postulates.** C1 to C4 add to the [AGM postulates](/agm-postulates/) in the finite form R1 to R6 of [Katsuno and Mendelzon](/katsuno-mendelzon-revision/). Those fix only the least worlds of each new preorder, while C1 to C4 constrain the rest of it.
- **Belief sets against epistemic states.** In the first version (TARK 1994) the postulates were stated for belief sets. Freund and Lehmann (1994, in a technical report) showed that C2 is then inconsistent with the AGM postulates: no revision function on belief sets satisfies K*1 to K*4 and C2. The 1997 version avoids the conflict by revising epistemic states, so that two states with the same beliefs can be revised differently.
- **Spheres and ranks.** A total preorder on worlds is a [system of spheres](/grove-spheres/), and a rank function is a numbered one. [Ordinal conditional functions](/ordinal-conditional-functions/) are the ranked epistemic states that Darwiche and Pearl use for their operator.
- **Independence.** Later work added the condition that if $w_1 \models \mu$, $w_2 \models \neg \mu$ and $w_1 \le_\Psi w_2$, then $w_1 <_{\Psi \circ \mu} w_2$, which is stronger than CR3 and CR4 together. Lexicographic revision and the operator of Darwiche and Pearl satisfy it. Natural revision does not, since a $\mu$-world that is not among the least ones stays tied with a $\neg \mu$-world of the same rank.
- **Entrenchment.** An [epistemic entrenchment](/epistemic-entrenchment/) order on formulas carries the same information as a total preorder on worlds, so iterated revision can also be stated as a change of entrenchment.
- **Conditionals.** In [System Z](/system-z/) and [rational closure](/rational-closure/), a ranking of worlds also answers default queries. C1 to C4 can be read as conditions on which conditionals survive a revision.

## References
