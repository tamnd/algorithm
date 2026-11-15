---
tag: 129BD3
kind: model
slug: system-p
name: System P
aliases:
- KLM preferential consequence
- preferential reasoning
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: The rules of reflexivity, left logical equivalence, right weakening, or, cut and cautious monotony for nonmonotonic consequence.
prereqs: [nonmonotonic-reasoning]
see_also: [rational-closure, system-z, circumscription, default-logic, default-extension, belief-revision, ordinal-conditional-functions]
sources:
  - paper: doi:10.1016/0004-3702(90)90101-5
    title: Sarit Kraus, Daniel Lehmann and Menachem Magidor, Nonmonotonic reasoning, preferential models and cumulative logics, Artificial Intelligence 44(1-2), 167 to 207 (1990)
    locator: Definition 1 (system C), Section 3.1 (Makinson's observation on default logic), Definitions 7, 15 and 16 (smoothness, system P and preferential models) and Theorem 3 (the representation theorem for preferential relations)
  - paper: doi:10.1016/0004-3702(92)90041-U
    title: Daniel Lehmann and Menachem Magidor, What does a conditional knowledge base entail?, Artificial Intelligence 55(1), 1 to 60 (1992)
    locator: Section 2.7, Theorem 4 (deciding preferential entailment is coNP-complete, and polynomial for Horn assertions) and Section 3.4 (Rational Monotonicity); erratum doi:10.1016/0004-3702(94)90073-6
---

System P is a set of six rules that any reasonable nonmonotonic consequence relation should obey. Kraus, Lehmann and Magidor (1990) wrote $\alpha \mathrel{|\!\sim} \beta$ for "if $\alpha$, then normally $\beta$" and asked which inference patterns hold for every sensible reading of "normally". Their answer has two sides that match exactly. On the syntactic side are the rules Reflexivity, Left Logical Equivalence, Right Weakening, Cut, Cautious Monotonicity and Or. On the semantic side are *preferential models*, in which $\alpha \mathrel{|\!\sim} \beta$ holds when the most normal situations that satisfy $\alpha$ also satisfy $\beta$. A relation obeys the rules exactly when some preferential model defines it. Deciding what a finite set of conditionals entails in System P is coNP-complete, the same as classical propositional entailment (Lehmann and Magidor 1992).

## The machine

For a logic, the machine is its syntax and its semantics. Here the formulas are propositional over a finite set of atoms, $\models$ is classical consequence, and the objects of study are *conditional assertions* $\alpha \mathrel{|\!\sim} \beta$ between formulas.

**Rules.** A *consequence relation* is a set of conditional assertions. It is *preferential* if it obeys these rules.

| Rule | Premises | Conclusion |
|---|---|---|
| Reflexivity | | $\alpha \mathrel{|\!\sim} \alpha$ |
| Left Logical Equivalence | $\models \alpha \leftrightarrow \beta$ and $\alpha \mathrel{|\!\sim} \gamma$ | $\beta \mathrel{|\!\sim} \gamma$ |
| Right Weakening | $\models \beta \supset \gamma$ and $\alpha \mathrel{|\!\sim} \beta$ | $\alpha \mathrel{|\!\sim} \gamma$ |
| Cut | $\alpha \wedge \beta \mathrel{|\!\sim} \gamma$ and $\alpha \mathrel{|\!\sim} \beta$ | $\alpha \mathrel{|\!\sim} \gamma$ |
| Cautious Monotonicity | $\alpha \mathrel{|\!\sim} \beta$ and $\alpha \mathrel{|\!\sim} \gamma$ | $\alpha \wedge \beta \mathrel{|\!\sim} \gamma$ |
| Or | $\alpha \mathrel{|\!\sim} \gamma$ and $\beta \mathrel{|\!\sim} \gamma$ | $\alpha \vee \beta \mathrel{|\!\sim} \gamma$ |

The first five rules form system C, for *cumulative* (Definition 1). System P is C plus Or (Definition 15). Cut and Cautious Monotonicity together say that adding a conclusion you already draw to the premises changes nothing. Derived rules of P include And ($\alpha \mathrel{|\!\sim} \beta$ and $\alpha \mathrel{|\!\sim} \gamma$ give $\alpha \mathrel{|\!\sim} \beta \wedge \gamma$) and the conditionalization rule ($\alpha \wedge \beta \mathrel{|\!\sim} \gamma$ gives $\alpha \mathrel{|\!\sim} \beta \supset \gamma$).

**Rules that fail.** Monotonicity ($\alpha \mathrel{|\!\sim} \gamma$ gives $\alpha \wedge \beta \mathrel{|\!\sim} \gamma$), Transitivity and Contraposition are not rules of P. Rational Monotonicity ($\alpha \mathrel{|\!\sim} \gamma$ and not $\alpha \mathrel{|\!\sim} \neg\beta$ give $\alpha \wedge \beta \mathrel{|\!\sim} \gamma$) is not a rule of P either. Adding it gives the rational relations studied by Lehmann and Magidor (1992, Section 3.4).

**Preferential models.** A preferential model is a triple $(S, l, \prec)$ (Definition 16). $S$ is a set of *states*, $l$ maps each state to a propositional world, and $\prec$ is a strict partial order on $S$, read "is more normal than". A state $s$ satisfies $\alpha$ when $l(s) \models \alpha$. Write $\hat\alpha$ for the set of the states that satisfy $\alpha$. The order must be *smooth* (Definition 7): for each $\alpha$, every state of $\hat\alpha$ is minimal in $\hat\alpha$ or has a minimal state of $\hat\alpha$ below it. The model defines

$$\alpha \mathrel{|\!\sim} \beta \iff \text{every } \prec\text{-minimal state of } \hat\alpha \text{ satisfies } \beta.$$

Different states may carry the same world, which is needed for the representation theorem. On a finite set of states every strict partial order is smooth.

**Representation** (Theorem 3). A consequence relation is preferential exactly when it is defined by some preferential model.

## What it counts

The central task is **preferential entailment**. A finite set $K$ of conditional assertions *preferentially entails* $\alpha \mathrel{|\!\sim} \beta$ when every preferential relation that contains $K$ contains $\alpha \mathrel{|\!\sim} \beta$. By the representation theorem, this is the same as derivability from $K$ with the rules of P, and the same as truth in every preferential model of $K$. The cost is measured in the size of $K$ and of the query, with propositional satisfiability as the basic test.

**Example.** Let $K$ be "birds normally fly", "penguins normally do not fly" and "penguins are normally birds": $\{b \mathrel{|\!\sim} f,\ p \mathrel{|\!\sim} \neg f,\ p \mathrel{|\!\sim} b\}$.

- $p \wedge b \mathrel{|\!\sim} \neg f$ is entailed: apply Cautious Monotonicity to $p \mathrel{|\!\sim} b$ and $p \mathrel{|\!\sim} \neg f$. The more specific class wins.
- $b \mathrel{|\!\sim} \neg p$ is entailed: from $p \wedge b \mathrel{|\!\sim} \neg f$, conditionalization gives $b \mathrel{|\!\sim} p \supset \neg f$, And with $b \mathrel{|\!\sim} f$ gives $b \mathrel{|\!\sim} f \wedge (p \supset \neg f)$, and Right Weakening gives $b \mathrel{|\!\sim} \neg p$. Birds are normally not penguins.
- $b \wedge r \mathrel{|\!\sim} f$ for an unrelated atom $r$ ("red birds fly") is *not* entailed. A preferential model of $K$ can contain a most normal red bird that does not fly. System P never assumes that unrelated information is irrelevant, which is the main reason it is called too cautious. [Rational closure](/rational-closure/) draws this conclusion.

## Relation to other models

- **Monotonic logic.** Classical consequence, $\alpha \mathrel{|\!\sim} \beta$ iff $\alpha \models \beta$, is preferential: take one state per world with the empty order. It is the special case that also satisfies Monotonicity.
- **Rational relations.** A preferential relation that also obeys Rational Monotonicity is *rational*, and it is defined by a *ranked* model, where the order comes from a ranking of the states (Lehmann and Magidor 1992). The [rational closure](/rational-closure/) of $K$ is the canonical rational relation that contains $K$, and [System Z](/system-z/) computes it with ranks.
- **[Circumscription](/circumscription/).** For a fixed theory, minimizing a set of atoms gives a preferential relation, because the models ordered by "fewer abnormal atoms" form a preferential model.
- **[Default logic](/default-logic/).** Skeptical consequence in default logic fails Cautious Monotonicity, even with only normal defaults (Makinson's observation, Section 3.1, worked out on the [extension page](/default-extension/)). So default logic is not preferential.
- **Ranking functions.** [Ordinal conditional functions](/ordinal-conditional-functions/) give ranked models directly: $\alpha \mathrel{|\!\sim} \beta$ when the rank of $\alpha \wedge \beta$ is below the rank of $\alpha \wedge \neg\beta$.
- **[Belief revision](/belief-revision/).** Revising a fixed belief set by $\alpha$ and asking whether $\beta$ is believed gives a consequence relation. The [AGM postulates](/agm-postulates/) for revision correspond closely to the rules of rational relations, so revision and preferential reasoning are two views of the same orderings, such as [Grove spheres](/grove-spheres/).

## Known results in the model

- **Representation:** preferential relations are exactly the relations of preferential models (Kraus, Lehmann and Magidor 1990, Theorem 3). Cumulative relations, those of system C, have a similar representation by cumulative models.
- **Complexity:** deciding whether a finite $K$ preferentially entails an assertion is coNP-complete, and it is polynomial when the assertions are Horn (Lehmann and Magidor 1992, Section 2.7, Theorem 4). The lower bound holds already for $K = \emptyset$, where $\alpha \mathrel{|\!\sim} \beta$ is entailed exactly when $\alpha \models \beta$.
- **Preferential entailment is not rational.** The preferentially entailed relation of a $K$ is the intersection of all preferential relations that contain it. It need not satisfy Rational Monotonicity, and the intersection of all rational relations that contain $K$ is again only preferential (Lehmann and Magidor 1992). This is why a canonical rational relation has to be chosen by another principle, which leads to [rational closure](/rational-closure/).
- **Impossible antecedents.** If $K$ preferentially entails $\top \mathrel{|\!\sim} \bot$, every assertion is entailed. A weaker failure is detected by the tolerance partition of [System Z](/system-z/). Suppose it leaves a nonempty set $R$ of rules without a rank. In a preferential model of $K$, a minimal state among those that satisfy some antecedent of $R$ would satisfy all of $R$ materially and so make one rule of $R$ tolerated. So no state satisfies an antecedent of $R$, and $K$ entails $\alpha \mathrel{|\!\sim} \bot$ for every antecedent $\alpha$ in $R$.

## References
