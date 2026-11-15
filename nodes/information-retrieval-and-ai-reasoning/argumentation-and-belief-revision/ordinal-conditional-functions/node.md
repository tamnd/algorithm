---
tag: N01YAW
kind: model
slug: ordinal-conditional-functions
name: Ordinal conditional functions
aliases:
- Spohn ranking functions
- OCF
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: Grades possible worlds by ordinal degrees of disbelief, which support iterated revision by conditionalization on ranks.
prereqs: [belief-revision, grove-spheres]
see_also: [darwiche-pearl-postulates, system-z, rational-closure, katsuno-mendelzon-revision, epistemic-entrenchment, conditional-probability, nonmonotonic-reasoning]
sources:
  - paper: doi:10.1007/978-94-009-2865-7_6
    title: "Wolfgang Spohn, Ordinal conditional functions: a dynamic theory of epistemic states, in William L. Harper and Brian Skyrms (eds), Causation in Decision, Belief Change, and Statistics, vol. II, Kluwer, Dordrecht, 105 to 134 (1988)"
    locator: the whole paper (ordinal conditional functions, the ranks of propositions, belief and firmness, conditional ranks, the A,n-conditionalization and its reversibility, and the comparison with probability)
  - paper: doi:10.1016/S0004-3702(96)00038-0
    title: Adnan Darwiche and Judea Pearl, On the logic of iterated belief revision, Artificial Intelligence 89(1-2), 1 to 29 (1997)
    locator: the whole paper (ranking functions as epistemic states, and a revision of ranks that satisfies C1 to C4)
  - paper: doi:10.1016/0004-3702(91)90069-V
    title: Hirofumi Katsuno and Alberto O. Mendelzon, Propositional knowledge base revision and minimal change, Artificial Intelligence 52(3), 263 to 294 (1991)
    locator: Section 3 (faithful assignments of total preorders, which a ranking function induces)
---

An ordinal conditional function, also called a ranking function, gives each possible world a degree of disbelief: rank 0 for the worlds that are not disbelieved at all, and higher ranks for worlds that are more surprising. Wolfgang Spohn introduced them in 1988 to solve a problem that the AGM theory leaves open: after a revision, an agent needs not only new beliefs but a new order of plausibility, so that it can revise again. Ranks carry the order, the firmness of each belief, and conditional beliefs, and Spohn's conditionalization changes all of them at once. The model sits between the qualitative orders of [Grove's spheres](/grove-spheres/) and probability, and it underlies the iterated revision of [Darwiche and Pearl](/darwiche-pearl-postulates/) and the default reasoning of [System Z](/system-z/).

## The machine

Let $W$ be a nonempty set of worlds, and a proposition be a subset of $W$. In the finite propositional case, $W$ is the set of the $2^n$ assignments to $n$ atoms and propositions are given by formulas.

**Definition (Spohn 1988).** An ordinal conditional function is a map $\kappa$ from $W$ to the ordinals such that some world has rank 0. Here we use ranks in $\mathbb{N}$, which covers the finite case. Extend $\kappa$ to propositions by

$$\kappa(A) = \min_{w \in A} \kappa(w), \qquad \kappa(\emptyset) = \infty.$$

Then $\kappa(W) = 0$, $\kappa(A \cup B) = \min(\kappa(A), \kappa(B))$, and $\min(\kappa(A), \kappa(\neg A)) = 0$ for every $A$: of a proposition and its negation, at least one is not disbelieved.

**Belief.** $A$ is believed in $\kappa$ when $\kappa(\neg A) > 0$, and $\kappa(\neg A)$ is the firmness of the belief. The belief set is the set of the propositions that contain $\kappa^{-1}(0)$, so it is consistent and closed under consequence. The two-sided rank $\tau(A) = \kappa(\neg A) - \kappa(A)$ is positive for believed propositions, negative for disbelieved ones, and 0 when the agent has no opinion.

**Conditional ranks.** For $\kappa(A) < \infty$ and $w \in A$, $\kappa(w \mid A) = \kappa(w) - \kappa(A)$, and $\kappa(B \mid A) = \kappa(A \cap B) - \kappa(A)$. $B$ is believed given $A$ when $\kappa(\neg B \mid A) > 0$. This is the rank form of a conditional "if $A$ then normally $B$".

**Conditionalization.** To learn $A$ with firmness $n$, Spohn's $(A, n)$-conditionalization sets

$$\kappa_{A,n}(w) = \begin{cases} \kappa(w \mid A) & w \in A, \\ \kappa(w \mid \neg A) + n & w \notin A. \end{cases}$$

Afterwards $\kappa_{A,n}(A) = 0$ and $\kappa_{A,n}(\neg A) = n$, and the order inside $A$ and inside $\neg A$ is kept. For $n \ge 1$, $A$ is believed with firmness exactly $n$.

## What it counts

A rank is a count of surprise, read as the number of independent "abnormalities" a world needs. Ranks add along conjunctions of independent facts and take the minimum along disjunctions, as log-probabilities add and take the maximum. The basic operations on an explicit table of $|W|$ ranks cost:

| operation | cost |
|---|---|
| rank of a proposition, belief test, firmness | $O(|W|)$, one minimum |
| conditional rank $\kappa(B \mid A)$ | $O(|W|)$, two minima |
| $(A, n)$-conditionalization | $O(|W|)$, two minima and one pass |

With $n$ atoms, $|W| = 2^n$, so practical systems store a ranking implicitly, for example as the ranks of a set of defaults in System Z.

**A worked example.** Take the atoms $r$ (it rained) and $w$ (the street is wet), and start from these ranks:

| world | $\neg r \wedge \neg w$ | $r \wedge w$ | $\neg r \wedge w$ | $r \wedge \neg w$ | belief set |
|---|---|---|---|---|---|
| $\kappa$ | 0 | 1 | 2 | 3 | $\neg r \wedge \neg w$ |
| $\kappa_1 = \kappa_{w,1}$ | 1 | 0 | 1 | 4 | $r \wedge w$ |
| $\kappa_2 = (\kappa_1)_{\neg r,2}$ | 0 | 2 | 0 | 6 | $\neg r$ |

At the start the agent believes that it did not rain, and conditionally on rain it believes the street is wet: $\kappa(\neg w \mid r) = 3 - 1 = 2 > 0$. It then sees a wet street and learns $w$ with firmness 1. Here $\kappa(w) = 1$ and $\kappa(\neg w) = 0$, so the $w$-worlds drop by 1 and the $\neg w$-worlds rise by 1. Now the best explanation, rain, is believed. Next it is told that it did not rain, with firmness 2. In $\kappa_1$, $\kappa_1(\neg r) = 1$ and $\kappa_1(r) = 0$, so the $\neg r$-worlds drop by 1 and the $r$-worlds rise by 2. The agent now believes $\neg r$, and it has no opinion on $w$ any more: the weak evidence for a wet street, firmness 1, is exactly balanced by the old surprise of a wet street without rain. This dependence on firmness is what a plain order of worlds cannot express.

## Relation to other models

- **Total preorders and spheres.** Forget the numbers and keep only the order $w_1 \le w_2$ when $\kappa(w_1) \le \kappa(w_2)$. This is a total preorder whose least worlds are the beliefs, which is a [system of spheres](/grove-spheres/) and a faithful assignment in the sense of [Katsuno and Mendelzon](/katsuno-mendelzon-revision/). The belief set of $\kappa_{A,n}$ for $n \ge 1$ is the set of the least $A$-worlds of $\kappa$, so the beliefs after a conditionalization are an AGM revision by $A$.
- **Probability.** Read $\kappa(w) = k$ as "the probability of $w$ is of the order $\varepsilon^k$" for a small $\varepsilon$. Then the minimum over a union matches the sum of probabilities, the sum of ranks matches the product, and $\kappa(B \mid A)$ matches the [conditional probability](/conditional-probability/) $P(B \mid A)$. Spohn's conditionalization is the rank form of Jeffrey's rule, which sets new probabilities for $A$ and $\neg A$ and keeps the conditional probabilities given each.
- **Entrenchment.** The firmness $\kappa(\neg A)$ ranks the beliefs, and an [epistemic entrenchment](/epistemic-entrenchment/) is the order of these values.
- **Iterated revision.** Darwiche and Pearl (1997) use ranking functions as epistemic states. Their operator sets $\kappa'(w) = \kappa(w) - \kappa(\mu)$ on $\mu$-worlds and $\kappa'(w) = \kappa(w) + 1$ elsewhere, and satisfies C1 to C4 of the [Darwiche and Pearl postulates](/darwiche-pearl-postulates/). Spohn's conditionalization with a fixed firmness can fail C3, because it can lower the firmness of a belief that was already held.
- **Defaults.** A set of defaults "if $A$ then normally $B$" read as $\kappa(A \wedge \neg B) > \kappa(A \wedge B)$ has a least ranking that satisfies all of them, the ranking of [System Z](/system-z/), which gives the same answers as [rational closure](/rational-closure/). This links ranks to [nonmonotonic reasoning](/nonmonotonic-reasoning/).
- **Possibility theory.** Possibility measures of Dubois and Prade grade worlds on $[0, 1]$ with max and min in place of min and sum. Ranks are their integer, additive form.

## Known results in the model

- **Belief sets are consistent and closed.** Since $\kappa^{-1}(0)$ is nonempty, the believed propositions are those that contain a fixed nonempty set of worlds. This holds for every $\kappa$ and every conditionalization of it (Spohn 1988).
- **Law of negation.** $\min(\kappa(A), \kappa(\neg A)) = 0$, so no proposition and its negation are both disbelieved.
- **Conditionalization is reversible.** If $\kappa(A) = 0$, the $(A, \kappa(\neg A))$-conditionalization of $\kappa_{A,n}$ gives back $\kappa$. If $\kappa(A) > 0$, the $(\neg A, \kappa(A))$-conditionalization does. So no information is lost, unlike AGM revision of belief sets, which cannot be undone. A script checked this on random ranks over 3 atoms.
- **Firmness is set, not added.** After $\kappa_{A,n}$ the firmness of $A$ is $n$ whatever it was before. A change that adds a fixed amount of evidence to $A$ instead is a different operation, and it can be written as an $(A, m)$-conditionalization for a suitable $m$.
- **AGM behaviour.** For each fixed $\kappa$, the map $A \mapsto$ the belief set of $\kappa_{A,1}$ satisfies the postulates R1 to R6, because it selects the least $A$-worlds of one total preorder.
- **Iterated behaviour.** The operator of Darwiche and Pearl on ranks satisfies C1 to C4. With $\kappa(w_0) = 0$, $\kappa(w_1) = 4$, $\kappa(w_2) = 5$ and $\kappa(w_3) = 6$, $A = \{w_0, w_1\}$ and $n = 1$, Spohn's conditionalization gives the ranks 0, 4, 1 and 2, which puts $w_2$ before $w_1$ and breaks CR3. A script checked both claims.

## References
