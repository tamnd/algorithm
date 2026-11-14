---
tag: 23G7RV
kind: theorem
slug: front-door-criterion
name: Front-door criterion
aliases:
- front-door adjustment
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: If a mediator set intercepts all directed paths from X to Y and has no unblocked back-door paths, the effect of X on Y is identified even with unmeasured confounding of X and Y.
prereqs: [do-calculus, backdoor-criterion, d-separation, structural-causal-model]
see_also: [mediation-analysis, instrumental-variables-estimation, average-treatment-effect, ordinary-least-squares, bayesian-network, directed-acyclic-graph]
sources:
  - paper: doi:10.1093/biomet/82.4.669
    title: Judea Pearl, Causal diagrams for empirical research, Biometrika 82(4), 1995, pages 669 to 688
    locator: "Section 3: the front-door condition and its adjustment formula, derived from the rules of the do-calculus"
  - book: isbn:9780521895606
    title: Judea Pearl, Causality, Models, Reasoning, and Inference, 2nd edition, Cambridge University Press, 2009
    locator: "Section 3.3: the front-door criterion, its adjustment formula and the smoking, tar and cancer example; Section 3.4 for the proof by the do-calculus"
  - book: isbn:9781119186847
    title: Judea Pearl, Madelyn Glymour and Nicholas P. Jewell, Causal Inference in Statistics, A Primer, Wiley, 2016
    locator: "Chapter 3, Section 3.4 (the front-door criterion)"
---

The front-door criterion gives a way to find the causal effect of a treatment $X$ on an outcome $Y$ when a hidden variable affects both and no set of measured variables closes the back doors. It uses a set $M$ of mediators through which all of the effect passes. If nothing hidden links $X$ to $M$, and $X$ itself closes the back doors from $M$ to $Y$, then the effect of $X$ on $M$ and the effect of $M$ on $Y$ can each be found from data, and their combination is the effect of $X$ on $Y$. The theorem is a short consequence of the three rules of the [do-calculus](/do-calculus/), and it is the standard example of an effect that is identifiable although the [back-door criterion](/backdoor-criterion/) fails.

## Statement

Let $G$ be the [directed acyclic graph](/directed-acyclic-graph/) of a [structural causal model](/structural-causal-model/) with independent noises. Some nodes of $G$ can be hidden. Let $X$, $Y$ and $M$ be disjoint sets of observed nodes with discrete values. A back-door path from a set $A$ to a set $B$ is a path from a node of $A$ to a node of $B$ whose first arrow points into the node of $A$. Blocking is in the sense of [d-separation](/d-separation/).

**Definition (front-door criterion).** The set $M$ satisfies the front-door criterion relative to $(X, Y)$ if

1. every directed path from a node of $X$ to a node of $Y$ goes through a node of $M$;
2. every back-door path from $X$ to $M$ is blocked by the empty set (it has a collider);
3. every back-door path from $M$ to $Y$ is blocked by $X$.

**Theorem (front-door adjustment).** If $M$ satisfies the front-door criterion relative to $(X, Y)$ and $P(x, m) > 0$ for all values $x$ of $X$ and $m$ of $M$, then for all $x$ and $y$

$$P(y \mid \mathrm{do}(x)) = \sum_m P(m \mid x) \sum_{x'} P(y \mid x', m)\, P(x').$$

So the interventional distribution of $Y$ is a function of the observed distribution of $(X, M, Y)$. For continuous variables the sums become integrals over densities.

## In plain words

A hidden cause can push both the treatment and the outcome, so treated and untreated units differ in more than the treatment. Sometimes the treatment acts only through a measured step in between, such as smoking acting through tar in the lungs. If nothing hidden pushes both the treatment and that step, then the link between treatment and step is causal. If the treatment itself carries all the hidden news about the outcome, then comparing units with the same treatment shows how the step moves the outcome. Chain the two parts and you get the effect of the treatment, although the hidden cause was never measured. If the effect has a second route that skips the measured step, or a hidden cause touches the step, the chain gives a wrong answer.

## Proof

The proof applies the three rules of the do-calculus as they are stated on the [do-calculus](/do-calculus/) page. For a set $A$, $G_{\overline A}$ is $G$ without the arrows into $A$, and $G_{\underline A}$ is $G$ without the arrows out of $A$. A path is open given a set $S$ when each of its colliders is in $S$ or has a descendant in $S$, and none of its non-colliders is in $S$. Two sets are d-separated given $S$ when no path between them is open given $S$.

**Lemma 1 (deleting arrows).** Let $H$ be $G$ with some arrows deleted. A path that is open given $S$ in $H$ is open given $S$ in $G$. So d-separation in $G$ implies d-separation in $H$.

*Proof.* The path uses only arrows of $G$, with the same directions, so its colliders and non-colliders are the same in $G$. A descendant in $H$ is a descendant in $G$. So each collider still has itself or a descendant in $S$, and no non-collider is in $S$. $\square$

**Lemma 2 (a subpath).** If a path is open given $S$, then each subpath between two of its nodes is open given $S$. Its inner nodes keep their role.

*Proof.* The inner nodes of the subpath have the same two neighbors on it. $\square$

**Lemma 3.** Condition 2 gives (a) $(M \perp X)_{G_{\underline X}}$, (b) no node of $X$ is a descendant of a node of $M$, and (c) $(M \perp X)_{G_{\overline M}}$.

*Proof.* (a) Suppose a path between $X$ and $M$ is open given the empty set in $G_{\underline X}$. By Lemma 2, take the subpath from its last node in $X$ to the next node in $M$. It has no collider. Its first arrow is an arrow of $G_{\underline X}$ at a node of $X$, so it points into that node. By Lemma 1 it is a back-door path from $X$ to $M$ in $G$ with no collider, against condition 2.

(b) Suppose $m_0 \to \cdots \to x_0$ is a directed path with $m_0 \in M$ and $x_0 \in X$. Let $x^*$ be its first node in $X$ and let $m^*$ be the last node of $M$ before $x^*$. The part from $m^*$ to $x^*$, read from $x^*$, is a back-door path from $X$ to $M$, and as a directed path it has no collider, against condition 2.

(c) In $G_{\overline M}$ no arrow points into $M$. A path from a node of $M$ that is open given the empty set has no collider, and it starts with an arrow out of its first node, so it is a directed path. A directed path from $M$ to $X$ in $G_{\overline M}$ is one in $G$, which (b) excludes. $\square$

**Lemma 4.** Condition 3 gives $(Y \perp M \mid X)_{G_{\underline M}}$ and $(Y \perp M \mid X)_{G_{\overline X \underline M}}$.

*Proof.* Suppose a path between $M$ and $Y$ is open given $X$ in $G_{\underline M}$. By Lemma 2, take the subpath from its last node in $M$ to the next node in $Y$. No arrow leaves $M$ in $G_{\underline M}$, so its first arrow points into its node of $M$. By Lemma 1 it is open given $X$ in $G$, and it is a back-door path from $M$ to $Y$, against condition 3. The graph $G_{\overline X \underline M}$ is $G_{\underline M}$ with more arrows deleted, so the second claim follows by Lemma 1. $\square$

**Lemma 5.** Condition 1 gives $(Y \perp X \mid M)_{G_{\overline X\, \overline M}}$.

*Proof.* In $H = G_{\overline X\, \overline M}$ no arrow points into $X$ or $M$. Suppose a path from a node of $X$ to a node of $Y$ is open given $M$ in $H$. A node of $M$ on it cannot be a collider, since no arrow enters it, and cannot be a non-collider, since it is in $M$. So the path avoids $M$. A collider $c$ on it would need a descendant in $M$, but a directed path from $c$ into $M$ ends with an arrow into $M$, which $H$ does not have. So the path has no collider. It starts with an arrow out of a node of $X$, so it is a directed path. It is a directed path in $G$ from $X$ to $Y$ that avoids $M$, against condition 1. $\square$

**Proof of the theorem.** By positivity every conditional probability below is defined. In the do-calculus, the rule 3 condition for deleting $\mathrm{do}(z)$ given $w$ uses the set $Z(W)$ of nodes of $Z$ that are not ancestors of $W$. With $W$ empty, $Z(W) = Z$. We use the five steps below.

1. By the law of total probability in the model under $\mathrm{do}(x)$,
$$P(y \mid \mathrm{do}(x)) = \sum_m P(m \mid \mathrm{do}(x))\, P(y \mid \mathrm{do}(x), m).$$
2. $P(m \mid \mathrm{do}(x)) = P(m \mid x)$ by rule 2 with condition $(M \perp X)_{G_{\underline X}}$, which is Lemma 3 (a).
3. $P(y \mid \mathrm{do}(x), m) = P(y \mid \mathrm{do}(x), \mathrm{do}(m))$ by rule 2 with condition $(Y \perp M \mid X)_{G_{\overline X \underline M}}$, which is Lemma 4.
4. $P(y \mid \mathrm{do}(x), \mathrm{do}(m)) = P(y \mid \mathrm{do}(m))$ by rule 3 with condition $(Y \perp X \mid M)_{G_{\overline M\, \overline X}}$, which is Lemma 5.
5. By the law of total probability under $\mathrm{do}(m)$,
$$P(y \mid \mathrm{do}(m)) = \sum_{x'} P(y \mid x', \mathrm{do}(m))\, P(x' \mid \mathrm{do}(m)) = \sum_{x'} P(y \mid x', m)\, P(x').$$
The first factor uses rule 2 with condition $(Y \perp M \mid X)_{G_{\underline M}}$, which is Lemma 4. The second uses rule 3 with condition $(X \perp M)_{G_{\overline M}}$, which is Lemma 3 (c).

Put steps 2 to 5 into step 1 to get the formula. $\square$

Step 5 is the back-door adjustment for the effect of $M$ on $Y$ with the adjustment set $X$. Lemma 3 (b) and condition 3 are exactly the two conditions of the back-door criterion for that pair.

**An example with two mediators.** Let $U$ be a hidden fair coin, and let all other variables be binary. Let $P(X = 1 \mid U = u) = \frac15, \frac45$ for $u = 0, 1$. Let $X$ act on $Y$ through two mediators: $P(M_1 = 1 \mid x) = \frac14, \frac34$ and $P(M_2 = 1 \mid x) = \frac12, \frac9{10}$ for $x = 0, 1$, independently given $X$, and $P(Y = 1 \mid m_1, m_2, u) = \frac1{10} + \frac15m_1 + \frac15m_2 + \frac25u$. The graph has $U \to X$, $U \to Y$, $X \to M_1 \to Y$ and $X \to M_2 \to Y$. The set $M = \{M_1, M_2\}$ meets both directed paths. The back-door paths from $X$ to $M$ go through $U \to Y \leftarrow M_j$, with the collider $Y$. The back-door paths from $M_j$ to $Y$ start $M_j \leftarrow X$, so $X$ blocks them. The exact values, in Fractions, are as follows.

- In the model, $P(Y = 1 \mid \mathrm{do}(X = x)) = \frac3{10} + \frac15\bigl(P(M_1 = 1 \mid x) + P(M_2 = 1 \mid x)\bigr)$, which is $\frac9{20} = 0.45$ for $x = 0$ and $\frac{63}{100} = 0.63$ for $x = 1$. The effect is $0.18$.
- The plain conditionals are $P(Y = 1 \mid X = 0) = 0.33$ and $P(Y = 1 \mid X = 1) = 0.75$, a difference of $0.42$, because $U$ raises both $X$ and $Y$.
- From the observed distribution, $P(X = 1) = \frac12$ and $P(Y = 1 \mid x', m_1, m_2)$ is $\frac9{50}, \frac{21}{50}$ for $(m_1, m_2) = (0, 0)$ and $x' = 0, 1$, it is $\frac{19}{50}, \frac{31}{50}$ for $(0, 1)$ and for $(1, 0)$, and it is $\frac{29}{50}, \frac{41}{50}$ for $(1, 1)$. So the inner sum $\sum_{x'} P(Y = 1 \mid x', m)P(x')$ is $\frac3{10}, \frac12, \frac12, \frac7{10}$.
- The outer sum with $P(m \mid X = 1) = \frac1{40}, \frac9{40}, \frac3{40}, \frac{27}{40}$ gives $\frac{3 + 45 + 15 + 189}{400} = \frac{63}{100}$. For $X = 0$ it gives $\frac9{20}$. Both agree with the model.

## Consequences

- **Identification without a back-door set.** In the example, every back-door path from $X$ to $Y$ goes through the hidden $U$, and the only observed nodes are descendants of $X$. No set satisfies the back-door criterion, but the effect is identified.
- **Plug-in estimation.** Replace each probability in the formula by its sample frequency. The estimate is consistent when the cells $(x, m)$ have positive probability. With many values of $M$ the cells are small, and one fits models for $P(m \mid x)$ and $P(y \mid x, m)$ instead.
- **The linear case: a product of coefficients.** Let $X = U + e_X$, $M = 2X + e_M$ and $Y = 3M + 4U + e_Y$, with $U$ hidden and the four noises uncorrelated with variance 1. The effect of $X$ on $Y$ is $2 \cdot 3 = 6$. The least squares slope of $Y$ on $X$ is $\operatorname{Cov}(X, Y)/\operatorname{Var}X = 16/2 = 8$, which is biased by $U$. The front-door estimate takes the slope $\alpha = 2$ of $M$ on $X$ (step 2) and the coefficient $\beta = 3$ of $M$ in the least squares fit of $Y$ on $M$ and $X$ (step 5), and returns $\alpha\beta = 6$. With several mediators in a linear model, the estimate is $\sum_j\alpha_j\beta_j$, where the $\beta_j$ come from one fit of $Y$ on all of $M$ and $X$. See [ordinary least squares](/ordinary-least-squares/).
- **Relation to mediation.** The formula chains the effect of $X$ on $M$ with the effect of $M$ on $Y$. Condition 1 says that there is no direct effect of $X$ on $Y$, so in the terms of [mediation analysis](/mediation-analysis/) the whole effect is indirect.
- **A special case of the do-calculus.** The proof uses only the three rules. Effects that neither the back-door nor the front-door criterion covers can still be identifiable, and the do-calculus decides each case.

## Tightness

Each hypothesis is needed. The three counterexamples below use the graph $U \to X \to M \to Y \leftarrow U$ with one binary mediator, a hidden fair coin $U$, $P(X = 1 \mid u) = \frac15, \frac45$, and one change each. The values are exact.

- **Condition 1.** In the two-mediator example, the set $\{M_1\}$ misses the path $X \to M_2 \to Y$. The formula with $M_1$ alone gives $0.49$ and $0.59$, an effect of $0.10$ instead of $0.18$.
- **Condition 2.** Add the arrow $U \to M$, with $P(M = 1 \mid x, u) = \frac1{10} + \frac35x + \frac15u$ and $P(Y = 1 \mid m, u) = \frac1{10} + \frac25m + \frac25u$. The back-door path $X \leftarrow U \to M$ has no collider. The model gives $P(Y = 1 \mid \mathrm{do}(X = x)) = 0.38, 0.62$, but the formula gives $\frac{23909}{75250} \approx 0.3177$ and $\frac{51341}{75250} \approx 0.6823$.
- **Condition 3.** Keep $U$ out of $M$, but add a second hidden fair coin $V$ with $V \to M$ and $V \to Y$: $P(M = 1 \mid x, v) = \frac1{10} + \frac35x + \frac15v$ and $P(Y = 1 \mid m, u, v) = \frac1{10} + \frac25m + \frac15u + \frac15v$. The back-door path $M \leftarrow V \to Y$ does not pass through $X$. The model gives $0.38$ and $0.62$, but the formula gives $0.36125$ and $0.63875$.
- **Positivity.** If $M = X$ always, then $P(y \mid x', m)$ is undefined for $x' \ne m$, and the graph is in effect $X \to Y$ with the hidden $U$ on both, where the effect is not identifiable.

With all three conditions and $P(M = 1 \mid x) = \frac1{10} + \frac35x$, $P(Y = 1 \mid m, u) = \frac1{10} + \frac25m + \frac25u$, the model and the formula both give $0.34$ and $0.58$.

The criterion is sufficient, not necessary, for identification. Other graphs with hidden confounding of $X$ and $Y$ have identifiable effects that need other sequences of the rules.

## History

Pearl introduced the front-door condition in "Causal diagrams for empirical research" (Biometrika, 1995), together with the rules of the do-calculus from which he derived it. His motivating example asks for the effect of smoking on lung cancer when an unmeasured genotype might cause both, with the tar deposit in the lungs as the mediator. Chapter 3 of *Causality* (2000, second edition 2009) states the criterion and the adjustment formula and proves them by the do-calculus. The primer by Pearl, Glymour and Jewell (2016) gives a textbook account next to the back-door criterion.

## References
