---
tag: 9PG3A1
kind: definition
slug: rational-closure
name: Rational closure
aliases:
- Lehmann-Magidor rational closure
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: The canonical rational consequence relation for a set of conditionals, adding rational monotony to System P.
prereqs: [system-p]
see_also: [system-z, ordinal-conditional-functions, nonmonotonic-reasoning, default-logic, belief-revision]
sources:
  - paper: doi:10.1016/0004-3702(92)90041-U
    title: Daniel Lehmann and Menachem Magidor, What does a conditional knowledge base entail?, Artificial Intelligence 55(1), 1 to 60 (1992)
    locator: Section 2.6, Definition 10 (exceptional formulas), Section 3.4 (Rational Monotonicity), Section 3.6 (ranked models), Section 5.4, Definition 21 (rational closure), Section 5.6 (existence for finite bases) and Section 5.8 (the decision procedure, Lemma 33 and Corollary 6); erratum doi:10.1016/0004-3702(94)90073-6
  - paper: doi:10.1016/0004-3702(90)90101-5
    title: Sarit Kraus, Daniel Lehmann and Menachem Magidor, Nonmonotonic reasoning, preferential models and cumulative logics, Artificial Intelligence 44(1-2), 167 to 207 (1990)
    locator: Definition 15 (system P), on which rational closure builds
  - paper: doi:10.1016/0004-3702(95)00090-9
    title: Moisés Goldszmidt and Judea Pearl, Qualitative probabilities for default reasoning, belief revision, and causal modeling, Artificial Intelligence 84(1-2), 57 to 112 (1996)
    locator: the Z-ranking of a consistent set of defaults and its agreement with rational closure
---

The rational closure of a set of conditionals is the answer of Lehmann and Magidor (1992) to the question in the title of their paper: what does a conditional knowledge base entail? [System P](/system-p/) gives a safe answer that is too cautious: from "birds fly" it does not conclude "red birds fly". Rational closure adds the rule of Rational Monotonicity and picks one canonical relation among those that satisfy it. The idea is to treat every situation as normal as the knowledge base allows. Each formula gets a rank, its degree of exceptionality, and $\alpha \mathrel{|\!\sim} \beta$ holds when $\alpha \wedge \beta$ is less exceptional than $\alpha \wedge \neg\beta$. For a finite base, the ranks are computed with a quadratic number of satisfiability tests. [System Z](/system-z/) gives the same relation.

## Definition

The formulas are propositional over finitely many atoms. A *knowledge base* $K$ is a finite set of conditional assertions $\alpha \mathrel{|\!\sim} \beta$, read "if $\alpha$, then normally $\beta$". Write $K \models_P \alpha \mathrel{|\!\sim} \beta$ for preferential entailment, that is, derivability with the rules of [System P](/system-p/).

**Rational relations.** A preferential relation is *rational* if it also obeys

$$\text{Rational Monotonicity:}\quad \frac{\alpha \mathrel{|\!\sim} \gamma \qquad \alpha \not\mathrel{|\!\sim} \neg\beta}{\alpha \wedge \beta \mathrel{|\!\sim} \gamma}$$

(Section 3.4). In words, a conclusion survives new information unless the new information was expected to be false. Rational relations are exactly the relations of *ranked* models, preferential models whose order comes from ranking the states by levels (Section 3.6).

**Exceptionality** (Section 2.6, Definition 10). A formula $\alpha$ is *exceptional* for $K$ when $K \models_P \top \mathrel{|\!\sim} \neg\alpha$: normally, $\alpha$ is false. An assertion is exceptional when its antecedent is. For a finite $K$, exceptionality needs only one classical test (Section 5.8, Lemma 33 and Corollary 6): with $\tilde K = \{\alpha \supset \beta : \alpha \mathrel{|\!\sim} \beta \in K\}$, the *material counterpart*,

$$\alpha \text{ is exceptional for } K \iff \tilde K \models \neg\alpha.$$

**Ranks.** Put $C_0 = K$, and let $C_{i+1}$ be the set of the assertions of $C_i$ that are exceptional for $C_i$. The sets shrink, so for finite $K$ they become constant at some $C_m$. The *rank* of a formula $\alpha$ is the least $i$ such that $\alpha$ is not exceptional for $C_i$, and $\infty$ when $\alpha$ is exceptional for every $C_i$.

**Rational closure.** Lehmann and Magidor define the rational closure of $K$ as a canonical rational relation (Section 5.4, Definition 21), and prove that every finite $K$ has one (Section 5.6). For finite $K$ it is decided by ranks (Section 5.8):

$$\alpha \mathrel{|\!\sim} \beta \text{ is in the rational closure of } K \iff \mathrm{rank}(\alpha) < \mathrm{rank}(\alpha \wedge \neg\beta) \ \text{ or } \ \mathrm{rank}(\alpha) = \infty.$$

Each rank needs at most $m + 1$ tests of the form $\tilde C_i \models \neg\alpha$, and $m$ is at most $|K|$. So a query takes $O(|K|^2)$ calls to a SAT oracle when the $C_i$ are also computed, and $O(|K|)$ calls once they are known. For Horn assertions every test is a Horn test, and the whole procedure is polynomial.

**Basic properties.** The rational closure contains $K$ and every assertion that $K$ preferentially entails. It is rational, so it satisfies Rational Monotonicity. It is nonmonotonic: a stronger antecedent can lose a conclusion.

## Examples and non-examples

Each example uses $b$ for bird, $f$ for flies, $p$ for penguin, $w$ for has wings and $r$ for red.

- **Specificity.** $K = \{b \mathrel{|\!\sim} f,\ p \mathrel{|\!\sim} \neg f,\ p \mathrel{|\!\sim} b\}$. The material counterparts entail $\neg p$, so $p$ is exceptional and $C_1 = \{p \mathrel{|\!\sim} \neg f,\ p \mathrel{|\!\sim} b\}$. Nothing in $C_1$ is exceptional for $C_1$, so $C_2 = \emptyset$. The ranks are $\mathrm{rank}(b) = 0$, $\mathrm{rank}(b \wedge \neg f) = 1$, $\mathrm{rank}(p) = 1$ and $\mathrm{rank}(p \wedge f) = 2$. So $b \mathrel{|\!\sim} f$, $p \mathrel{|\!\sim} \neg f$ and $b \mathrel{|\!\sim} \neg p$ are all in the closure.
- **Irrelevance.** In the same $K$, $\mathrm{rank}(b \wedge r) = 0$ and $\mathrm{rank}(b \wedge r \wedge \neg f) = 1$, so "red birds fly" is in the rational closure. System P does not entail it. This is the gain from Rational Monotonicity.
- **Non-example: the drowning problem.** Add $b \mathrel{|\!\sim} w$. Now $\mathrm{rank}(p) = 1$ and $\mathrm{rank}(p \wedge \neg w) = 1$, because $C_1$ says nothing about wings. So $p \mathrel{|\!\sim} w$ is *not* in the closure. Penguins are exceptional birds, and rational closure throws away all bird properties for them, not only flying. Lexicographic closure and maximum-entropy ranking, described on the [System Z](/system-z/) page, keep $p \mathrel{|\!\sim} w$.
- **Conflict without priority.** $K = \{q \mathrel{|\!\sim} p,\ r \mathrel{|\!\sim} \neg p\}$ (the Nixon diamond). Here $q \wedge r$ has rank 1, and so do $q \wedge r \wedge p$ and $q \wedge r \wedge \neg p$. Neither $q \wedge r \mathrel{|\!\sim} p$ nor $q \wedge r \mathrel{|\!\sim} \neg p$ is in the closure.
- **Non-example: monotonicity.** $b \mathrel{|\!\sim} f$ is in the closure of the first $K$, but $b \wedge p \mathrel{|\!\sim} f$ is not. The closure is not closed under strengthening the antecedent.
- **Impossible antecedents.** If $K = \{a \mathrel{|\!\sim} \bot\}$, then $a$ is exceptional for every $C_i$, its rank is $\infty$, and $a \mathrel{|\!\sim} \beta$ is in the closure for every $\beta$.

## Related definitions

- [System P](/system-p/) gives the rules that every preferential relation satisfies. Rational closure is a rational relation that contains the preferential consequences of $K$.
- [System Z](/system-z/) computes the same relation as the least admissible ranking of worlds, through Pearl's tolerance partition. A rule is tolerated by a set exactly when it is not exceptional for that set, so the Z-rank of a rule equals its rank here.
- [Ordinal conditional functions](/ordinal-conditional-functions/) are the ranking functions that give ranked models directly.
- Rational closure is the conditional counterpart of choosing the most plausible worlds in [belief revision](/belief-revision/).
- The skeptical consequences of a [default theory](/default-logic/) are not a rational relation, or even a preferential one, so default logic and rational closure disagree on some inputs.

## References
