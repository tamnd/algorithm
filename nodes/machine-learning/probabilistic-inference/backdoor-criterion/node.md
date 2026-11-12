---
tag: 7C4MVG
kind: theorem
slug: backdoor-criterion
name: Backdoor criterion
aliases:
- back-door criterion
- back-door adjustment
area: machine-learning/probabilistic-inference
level: advanced
summary: If Z has no descendant of X and blocks every path into X, then P(y | do(x)) is the sum over z of P(y | x, z) P(z), so the effect follows from observational data.
prereqs: [structural-causal-model, d-separation]
see_also: [do-calculus, d-separation-query, bayes-ball, directed-acyclic-graph, bayesian-network, conditional-probability-table]
sources:
  - paper: doi:10.1214/ss/1177010894
    title: Judea Pearl, Comment, Graphical models, causality and intervention, Statistical Science 8(3), 1993, pages 266 to 269
    locator: the first statement of the back-door condition and the adjustment formula for intervention
  - paper: doi:10.1093/biomet/82.4.669
    title: Judea Pearl, Causal diagrams for empirical research, Biometrika 82(4), 1995, pages 669 to 688
    locator: "Section 3: the back-door and front-door criteria and their adjustment formulas, derived from the rules of the do-calculus"
  - book: isbn:9780521895606
    title: Judea Pearl, Causality, Models, Reasoning, and Inference, 2nd edition, Cambridge University Press, 2009
    locator: "Section 3.3: the back-door criterion, the back-door adjustment, the front-door criterion and the front-door adjustment; Section 3.4 for the proof by the do-calculus"
  - book: isbn:9781119186847
    title: Judea Pearl, Madelyn Glymour and Nicholas P. Jewell, Causal Inference in Statistics, A Primer, Wiley, 2016
    locator: "Chapter 3, Sections 3.3 (the back-door criterion) and 3.4 (the front-door criterion)"
  - paper: "Ilya Shpitser, Tyler VanderWeele and James M. Robins, On the validity of covariate adjustment for estimating causal effects, UAI 2010"
    title: Ilya Shpitser, Tyler VanderWeele and James M. Robins, On the validity of covariate adjustment for estimating causal effects, Proceedings of the 26th Conference on Uncertainty in Artificial Intelligence, 2010
    locator: the complete graphical criterion for a set to be valid for covariate adjustment
---

The back-door criterion is Pearl's graphical test for confounding control. A causal graph and a set $Z$ of measured variables are given. If $Z$ contains no descendant of the cause $X$, and $Z$ blocks every path that enters $X$ through an arrow into $X$, then the effect of setting $X$ is the adjustment formula

$$P(y \mid \mathrm{do}(x)) = \sum_z P(y \mid x, z)\, P(z).$$

The right side uses only the distribution of the observed data. So the test tells you which covariates to "control for" in an observational study, and which ones you must leave out. Pearl stated it in 1993 and proved it as a consequence of the [do-calculus](/do-calculus/) in 1995.

## Statement

**Setting.** $M$ is a [structural causal model](/structural-causal-model/). Its graph $G$ is a [directed acyclic graph](/directed-acyclic-graph/) on all its variables, observed and hidden, and the noises of $M$ are independent. A hidden common cause is drawn as an explicit hidden node with arrows to the variables it affects. $X$, $Y$ and $Z$ are disjoint sets of observed variables. $P_x$ is the distribution of the submodel $M_x$ that sets $X := x$, so $P(y \mid \mathrm{do}(x)) = P_x(y)$.

$G_{\underline X}$ is the graph $G$ with every arrow *out of* a node of $X$ deleted. A *back-door path* from $x$ to $y$ is a path in $G$ (a sequence of distinct nodes, each pair joined by an arrow in either direction) whose first arrow points into $x$. A path is *blocked* by $Z$ when it has a non-collider in $Z$, or a collider $c$ such that neither $c$ nor any descendant of $c$ is in $Z$. This is the blocking of [d-separation](/d-separation/).

**Definition (back-door criterion).** $Z$ satisfies the back-door criterion relative to $(X, Y)$ when

1. no node of $Z$ is a descendant of a node of $X$, and
2. $Z$ d-separates $X$ from $Y$ in $G_{\underline X}$.

**Lemma 1 (the path form).** Let $X = \{x\}$ and $Y = \{y\}$ be single nodes and let $Z$ satisfy condition 1. Then condition 2 holds if and only if $Z$ blocks every back-door path from $x$ to $y$ in $G$. This second form is the wording of Pearl (1993; 2009, Section 3.3).

**Theorem (back-door adjustment).** If $Z$ satisfies the back-door criterion relative to $(X, Y)$, then for every $x$ and $y$ with $P(x, z) > 0$ for all $z$ with $P(z) > 0$,

$$P(y \mid \mathrm{do}(x)) = \sum_z P(y \mid x, z)\, P(z).$$

In particular, the causal effect of $X$ on $Y$ is identifiable from the observed distribution.

**Front-door criterion (for contrast).** A set $M$ satisfies the front-door criterion relative to single nodes $(x, y)$ when $M$ meets every directed path from $x$ to $y$, there is no unblocked back-door path from $x$ to $M$, and $x$ blocks every back-door path from $M$ to $y$. Then, under the same positivity condition,

$$P(y \mid \mathrm{do}(x)) = \sum_m P(m \mid x) \sum_{x'} P(y \mid x', m)\, P(x').$$

## In plain words

To learn what a treatment does, you can compare treated and untreated units, but only if nothing else makes them differ. A common cause of the treatment and the outcome opens a "back door" through which the two are related even when the treatment does nothing. The criterion says: find measured variables that close every such back door, and make sure that none of them is itself an effect of the treatment. Then compare treated and untreated units within each group of equal values of those variables, and average the results with the size of each group as its weight. Variables caused by the treatment must stay out, and some variables that are not caused by it must also stay out, because they open new back doors.

## Proof

**Proof of Lemma 1.** A simple path from $x$ to $y$ visits $x$ only once. So the paths between $x$ and $y$ in $G_{\underline x}$ are exactly the paths of $G$ whose first arrow enters $x$, which are the back-door paths. Deleting arrows out of $x$ does not change which nodes of such a path are colliders. It can change only one thing: the set of descendants of a collider $c$. Suppose $c$ has a descendant $s \in Z$ in $G$ but not in $G_{\underline x}$. Then every directed path from $c$ to $s$ uses an arrow out of $x$, so $s$ is a descendant of $x$. This contradicts condition 1. So under condition 1, each back-door path is blocked in $G$ exactly when it is blocked in $G_{\underline x}$. $\square$

**Proof of the theorem.** By the law of total probability in the submodel,

$$P_x(y) = \sum_z P_x(y \mid z)\, P_x(z).$$

We show $P_x(z) = P(z)$ and $P_x(y \mid z) = P(y \mid x, z)$.

*Step 1: $P_x(z) = P(z)$.* Let $N$ be the set of nodes that are not descendants of $X$ (a node of $X$ counts as its own descendant). A parent of a node of $N$ is in $N$ too. So the values of the nodes of $N$ come from their equations and their noises alone, and these are the same in $M$ and in $M_x$. Hence the nodes of $N$ have the same joint law in $M$ and $M_x$. By condition 1, $Z \subseteq N$.

*Step 2: $P_x(y \mid z) = P(y \mid x, z)$.* This is rule 2 of the do-calculus for this case. We give the argument here. Add a new root $F$ with values $\{\text{idle}, x\}$, each with probability $\frac12$, and an arrow from $F$ to each node of $X$. In the new model $M'$, the equations of $X$ return $x$ when $F = x$ and their old value when $F$ is idle. Then $P'(\cdot \mid F = \text{idle}) = P$ and $P'(\cdot \mid F = x) = P_x$. $M'$ is a structural causal model with independent noises on the graph $G' = G + \{F \to X\}$. So every d-separation in $G'$ is a conditional independence of $P'$ (the [d-separation](/d-separation/) page proves this).

We use one fact about d-separation. Two sets are d-connected given $S$ exactly when some *walk* (a path on which nodes may repeat) joins them, such that each collider on the walk is in $S$ and no non-collider on it is in $S$. The [Bayes-ball](/bayes-ball/) algorithm moves its ball along such walks, and its correctness proof is this fact.

We claim that $Y$ and $F$ are d-separated by $X \cup Z$ in $G'$. If they are not, take a walk as above from $F$ to $Y$ given $S = X \cup Z$. Cut it at its first node in $Y$. Let $x^*$ be the last node of $X$ on the walk. The walk leaves $x^*$ through an arrow into $x^*$. If it left through an arrow out of $x^*$, then $x^*$ would be a non-collider, but $x^* \in S$. The rest of the walk, from $x^*$ to $Y$, has no node of $X$ after $x^*$, and $F$ has no other neighbours. So it uses no arrow out of $X$, and it is a walk in $G_{\underline X}$. Its colliders are in $S$ but not in $X$, so they are in $Z$. Its non-colliders are not in $Z$. So $X$ and $Y$ are d-connected given $Z$ in $G_{\underline X}$, which contradicts condition 2.

So $P'(y \mid F, X, Z)$ does not depend on $F$:

$$P_x(y \mid z) = P'(y \mid F = x, X = x, z) = P'(y \mid F = \text{idle}, X = x, z) = P(y \mid x, z).$$

The first equality holds because $X = x$ always holds when $F = x$. Both conditional probabilities are defined because $P_x(z) = P(z) > 0$ and $P(x, z) > 0$.

*Step 3.* Substituting both steps into the total probability gives the formula. $\square$

**The front-door formula.** Pearl (1995) derives it by three uses of the do-calculus: $P(m \mid \mathrm{do}(x)) = P(m \mid x)$ by rule 2, $P(y \mid \mathrm{do}(m)) = \sum_{x'} P(y \mid x', m) P(x')$ by the back-door theorem with $Z = \{x\}$, and $P(y \mid \mathrm{do}(x), \mathrm{do}(m)) = P(y \mid \mathrm{do}(m))$ by rule 3. The [do-calculus](/do-calculus/) page proves the rules.

## Consequences

**Doing is not seeing, and adjustment fixes it.** In the treatment example on the [structural causal model](/structural-causal-model/) page, a severity $Z$ causes both the treatment $X$ and the recovery $Y$, and $X \to Y$. The set $\{Z\}$ satisfies the criterion. With $P(Z = 1) = \frac12$, $P(Y = 1 \mid X = 1, Z = 0) = 0.8$ and $P(Y = 1 \mid X = 1, Z = 1) = 0.4$,

$$P(Y = 1 \mid \mathrm{do}(X = 1)) = 0.8 \cdot \tfrac12 + 0.4 \cdot \tfrac12 = 0.6,$$

and in the same way $P(Y = 1 \mid \mathrm{do}(X = 0)) = 0.6 \cdot \frac12 + 0.1 \cdot \frac12 = 0.35$. The effect is $0.25$. The raw comparison $P(Y = 1 \mid X = 1) - P(Y = 1 \mid X = 0) = 0.5 - 0.475 = 0.025$ is ten times smaller, because treated patients are mostly severe.

**Choosing a set.** Take the graph with the arrows $Z_1 \to Z_3$, $Z_2 \to Z_3$, $Z_1 \to X$, $Z_3 \to X$, $Z_3 \to Y$, $Z_2 \to Y$, $X \to W$ and $W \to Y$. Among the subsets of $\{Z_1, Z_2, Z_3, W\}$, exactly three satisfy the criterion:

| set | result | reason |
|---|---|---|
| $\emptyset$ | fails | the path $X \leftarrow Z_3 \to Y$ is open |
| $\{Z_3\}$ | fails | $Z_3$ is a collider on $X \leftarrow Z_1 \to Z_3 \leftarrow Z_2 \to Y$, so conditioning on it opens that path |
| $\{Z_1, Z_3\}$, $\{Z_2, Z_3\}$, $\{Z_1, Z_2, Z_3\}$ | pass | $Z_3$ blocks the first path and $Z_1$ or $Z_2$ blocks the second |
| any set with $W$ | fails | $W$ is a descendant of $X$ |

All three valid sets give the same number on the population. With finite samples, they give estimates of different variance.

**Adjusting for the parents.** If all parents of $X$ are observed and $Y$ is not a parent of $X$, then $Z = \mathrm{Pa}(X)$ satisfies the criterion. In $G_{\underline X}$, each path from $X$ starts with an arrow from a parent into $X$, and that parent is a non-collider in $Z$. This gives the "adjustment for direct causes" of the structural causal model page.

**Covariate selection in practice.** "Adjust for everything measured before the treatment" is not a safe rule. In the *M-graph* $A \to X$, $A \to C$, $B \to C$, $B \to Y$, $X \to Y$ with $A$ and $B$ hidden, the empty set is valid, but $\{C\}$ is not. $C$ is a collider on $X \leftarrow A \to C \leftarrow B \to Y$, so adjusting for it opens that path. A mediator $X \to M \to Y$ must also stay out, since it is a descendant of $X$.

**Other forms of the same formula.** Writing $P(y \mid x, z) P(z) = P(x, y, z) / P(x \mid z)$ gives the inverse probability weighting form, with weights $1 / P(x \mid z)$. The quantity $P(x \mid z)$ is the propensity score of Rosenbaum and Rubin. A back-door set is also a set for which the potential outcomes $Y_x$ are independent of $X$ given $Z$. This is called conditional ignorability.

**Front door when no back door exists.** Let $U \to X$, $U \to Y$ with $U$ hidden, and $X \to M \to Y$. Every back-door path goes through $U$, and the only observed candidate $M$ is a descendant of $X$, so no set satisfies the criterion. But $M$ satisfies the front-door criterion. Take $U$ a fair coin, $P(X = 1 \mid U) = 0.2, 0.8$ for $U = 0, 1$, $P(M = 1 \mid X) = 0.1, 0.9$ for $X = 0, 1$, and $P(Y = 1 \mid M, U)$ equal to $0.1, 0.5, 0.4, 0.8$ for $(M, U) = (0,0), (1,0), (0,1), (1,1)$. The observed distribution gives $P(Y = 1 \mid x, m) = 0.16, 0.34, 0.56, 0.74$ for $(x, m) = (0,0), (1,0), (0,1), (1,1)$, and $P(X = 1) = \frac12$. The front-door formula gives

$$P(Y = 1 \mid \mathrm{do}(X = 1)) = 0.1 \cdot \tfrac{0.16 + 0.34}{2} + 0.9 \cdot \tfrac{0.56 + 0.74}{2} = 0.025 + 0.585 = 0.61,$$

and $0.29$ for $\mathrm{do}(X = 0)$. These are the true values in the model. The raw conditionals are $0.7$ and $0.2$.

**Checks in code.** The implementation tests the criterion with the reachability search for d-separation in $G_{\underline X}$ ([d-separation query](/d-separation-query/)), and computes both adjustment formulas. The tests:

- build 40 random models with 6 nodes, hidden nodes and noises uniform on $\{0, 1, 2, 3\}$;
- for every set that passes the criterion, compare the adjustment with $P(y \mid \mathrm{do}(x))$, computed exactly by solving the submodel for every noise value;
- compare the graph test with the path form of Lemma 1 on 300 random DAGs;
- check the examples above, and the front-door formula on random models of the front-door graph.

## Tightness

- **Condition 1 is needed.** In $X \to M \to Y$, $X \to Y$, the empty set is valid, and adjusting for the mediator $M$ gives a wrong answer for most parameter values. The tests check this.
- **Condition 2 is needed.** In the treatment example the empty set fails ($0.5 \ne 0.6$). In the M-graph, the pre-treatment variable $C$ fails.
- **Positivity is needed.** If some $z$ with $P(z) > 0$ has $P(x, z) = 0$, then $P(y \mid x, z)$ is not defined by the data, and the formula has no value.
- **Sufficient, not necessary, for adjustment.** In $X \to Y$, $X \to D$, the set $\{D\}$ breaks condition 1, but $\sum_d P(y \mid x, d) P(d) = P(y \mid x) = P(y \mid \mathrm{do}(x))$, because $Y$ and $D$ are independent given $X$. Shpitser, VanderWeele and Robins (2010) gave the adjustment criterion, which describes exactly the sets for which the adjustment formula is right in every model with the graph.
- **Sufficient, not necessary, for identification.** The front-door graph above has no back-door set, but the effect is identifiable. The do-calculus is complete for identification, so it decides every case. In the bow graph $X \to Y$, $X \leftarrow U \to Y$ with $U$ hidden, no method works, because the effect is not identifiable.

## History

Pearl gave the back-door condition and the adjustment formula in his 1993 comment in *Statistical Science*, in a discussion of graphical models and intervention. In "Causal diagrams for empirical research" (Biometrika, 1995) he derived the back-door and front-door adjustments from the three rules of the do-calculus. Chapter 3 of *Causality* (2000, second edition 2009) gives the standard account. Greenland, Pearl and Robins (1999) brought the criterion to epidemiology as a tool for choosing confounders from a causal diagram. Shpitser, VanderWeele and Robins (2010) closed the gap between the back-door criterion and valid adjustment with a complete criterion.

## References
