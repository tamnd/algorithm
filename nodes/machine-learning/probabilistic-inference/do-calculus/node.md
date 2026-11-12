---
tag: XER6WP
kind: theorem
slug: do-calculus
name: Do-calculus
aliases:
- Pearl's do-calculus
- rules of the do-calculus
area: machine-learning/probabilistic-inference
level: advanced
summary: Three rules, each with a d-separation test in a cut graph, that rewrite interventional probabilities. They are sound, and complete for identifying causal effects.
prereqs: [structural-causal-model, d-separation]
see_also: [backdoor-criterion, bayes-ball, d-separation-query, directed-acyclic-graph, bayesian-network, conditional-independence]
sources:
  - paper: doi:10.1093/biomet/82.4.669
    title: Judea Pearl, Causal diagrams for empirical research, Biometrika 82(4), 1995, pages 669 to 688
    locator: "Section 3: the three inference rules, their proof with intervention nodes, and the derivations of the back-door and front-door formulas"
  - book: isbn:9780521895606
    title: Judea Pearl, Causality, Models, Reasoning, and Inference, 2nd edition, Cambridge University Press, 2009
    locator: "Section 3.4: the rules of the do-calculus with their proofs and examples"
  - paper: "Yimin Huang and Marco Valtorta, Identifiability in causal Bayesian networks: a sound and complete algorithm, AAAI 2006, pages 1149 to 1154"
    title: Yimin Huang and Marco Valtorta, Identifiability in causal Bayesian networks, a sound and complete algorithm, Proceedings of the 21st National Conference on Artificial Intelligence (AAAI), 2006, pages 1149 to 1154
    locator: an identification algorithm whose every step follows from the three rules, proved complete, which shows that the rules are complete
  - paper: "Ilya Shpitser and Judea Pearl, Identification of joint interventional distributions in recursive semi-Markovian causal models, AAAI 2006, pages 1219 to 1226"
    title: Ilya Shpitser and Judea Pearl, Identification of joint interventional distributions in recursive semi-Markovian causal models, Proceedings of the 21st National Conference on Artificial Intelligence (AAAI), 2006, pages 1219 to 1226
    locator: the ID algorithm, hedges as the obstacle to identification, and completeness of the do-calculus
  - paper: "Jin Tian and Judea Pearl, A general identification condition for causal effects, AAAI 2002"
    title: Jin Tian and Judea Pearl, A general identification condition for causal effects, Proceedings of the 18th National Conference on Artificial Intelligence (AAAI), 2002
    locator: c-components and the identification of the effect of a single intervention
---

The do-calculus is a set of three rules for rewriting expressions like $P(y \mid \mathrm{do}(x), z)$, where $\mathrm{do}(x)$ means that $X$ was set to $x$ by an intervention. Each rule says that you may add or remove a conditioning event, or exchange an intervention for an observation, when a d-separation holds in a graph made by cutting some arrows of the causal graph. Pearl introduced the rules in 1995. If a sequence of rules turns a causal effect into an expression with no $\mathrm{do}$, then the effect can be computed from observational data. Huang and Valtorta (2006) and Shpitser and Pearl (2006) proved the converse: when no such sequence exists, no method can compute the effect from the observed distribution.

## Statement

**Setting.** $M$ is a [structural causal model](/structural-causal-model/) with independent noises. Its causal graph $G$ is a [directed acyclic graph](/directed-acyclic-graph/) on all variables, observed and hidden. A hidden common cause of two variables is a hidden node with arrows to both. (Pearl draws it as a dashed bidirected arc. The cut graphs below then delete an arc when they delete an arrow into one of its ends.) $X$, $Y$, $Z$ and $W$ are disjoint sets of observed variables, and any of them except $Y$ may be empty. $P(y \mid \mathrm{do}(x), w)$ is the conditional distribution of $Y$ given $W = w$ in the submodel $M_x$ that replaces the equations of $X$ by $X := x$.

**Cut graphs.** $G_{\overline X}$ is $G$ with every arrow *into* a node of $X$ deleted. $G_{\underline Z}$ is $G$ with every arrow *out of* a node of $Z$ deleted. Combined marks combine the deletions, so $G_{\overline X \underline Z}$ has both. $(Y \perp Z \mid S)_H$ means that $S$ d-separates $Y$ from $Z$ in the graph $H$, in the sense of [d-separation](/d-separation/). Write $Z(W)$ for the set of nodes of $Z$ that are not ancestors of any node of $W$ in $G_{\overline X}$.

**Theorem (Pearl 1995).** For all values for which both sides are defined:

**Rule 1 (insertion or deletion of observations).**
$$P(y \mid \mathrm{do}(x), z, w) = P(y \mid \mathrm{do}(x), w) \quad \text{if } (Y \perp Z \mid X, W)_{G_{\overline X}}.$$

**Rule 2 (exchange of action and observation).**
$$P(y \mid \mathrm{do}(x), \mathrm{do}(z), w) = P(y \mid \mathrm{do}(x), z, w) \quad \text{if } (Y \perp Z \mid X, W)_{G_{\overline X \underline Z}}.$$

**Rule 3 (insertion or deletion of actions).**
$$P(y \mid \mathrm{do}(x), \mathrm{do}(z), w) = P(y \mid \mathrm{do}(x), w) \quad \text{if } (Y \perp Z \mid X, W)_{G_{\overline X\, \overline{Z(W)}}}.$$

**Completeness (Huang and Valtorta 2006; Shpitser and Pearl 2006).** A causal effect $P(y \mid \mathrm{do}(x))$ is *identifiable* in $G$ when every two models with graph $G$ and the same positive distribution of the observed variables have the same $P(y \mid \mathrm{do}(x))$. It is identifiable if and only if a finite sequence of the three rules, together with probability calculus, turns it into an expression with no $\mathrm{do}$.

## In plain words

An experiment and an observation can give different answers, because an observed value also carries news about its causes. Each rule names a case where that difference cannot arise. Rule 1: once you act on some variables, an extra observation that is cut off from the outcome can be ignored. Rule 2: acting on a variable and merely seeing it are the same when the only remaining links between it and the outcome leave it through its effects, so no hidden cause is shared. Rule 3: an action can be ignored when it cannot reach the outcome at all. The tests use only the causal diagram. The theorem also says these three moves are enough to find every causal effect that the data can give.

## Proof

Rule 1 is a plain conditional independence. Rules 2 and 3 compare two different models, so we join them in one model with extra switch nodes, as Pearl (1995) does.

**Two facts about d-separation.**

- *Soundness.* If a structural causal model with independent noises has the graph $H$, then every d-separation in $H$ is a conditional independence of its distribution. The [d-separation](/d-separation/) page proves this.
- *Walks.* Sets $A$ and $B$ are d-connected given $S$ in $H$ if and only if some walk (a path on which nodes may repeat) joins $A$ to $B$ such that each collider on the walk is in $S$ and each non-collider on the walk is not in $S$. The [Bayes-ball](/bayes-ball/) algorithm moves along exactly such walks, and its correctness proof shows this fact. We call such a walk *open given $S$*.

**The model $M_x$.** The submodel $M_x$ is a structural causal model with independent noises, and its graph is $G_{\overline X}$. In $M_x$, $X = x$ always holds, so adding $X = x$ to a condition changes nothing.

**Rule 1.** By soundness in $G_{\overline X}$, the condition gives $Y \perp Z \mid X, W$ under $P_{M_x}$. So $P_{M_x}(y \mid z, w) = P_{M_x}(y \mid w)$. $\square$

**The switch nodes.** For rules 2 and 3, start from $M_x$ and add a new root $F_v$ for each $v \in Z$, with values $\{\text{idle}\} \cup \mathrm{dom}(v)$, independent of everything and with every value positive. Add the arrow $F_v \to v$. The new equation of $v$ returns $F_v$ when $F_v$ is not idle, and the old value otherwise. Call the new model $M'$ and its graph $G'$. With $F = (F_v)_{v \in Z}$:

$$P'(\cdot \mid F = \text{idle}) = P_{M_x}, \qquad P'(\cdot \mid F = z) = P_{M_{x, z}}.$$

$M'$ has independent noises, so soundness holds in $G'$. The only neighbour of $F_v$ is $v$.

**Rule 2.** We show $(Y \perp F \mid X, Z, W)_{G'}$. Then $P'(y \mid F, x, z, w)$ does not depend on $F$. With $F = z$ the condition $Z = z$ always holds, so this gives $P_{M_{x,z}}(y \mid w) = P_{M_x}(y \mid z, w)$, which is rule 2.

Suppose a walk from some $F_v$ to $Y$ is open given $S = X \cup Z \cup W$. Cut it at its first node in $Y$. Let $z^*$ be the last node of $Z$ on it. If the walk leaves $z^*$ through an arrow out of $z^*$, then $z^*$ is a non-collider in $S$, so the walk is not open. So it leaves through an arrow into $z^*$. After $z^*$ the walk meets no node of $Z$, and so no switch node. Its part from $z^*$ to $Y$ therefore uses no arrow out of $Z$ and no switch arrow, so it is a walk in $G_{\overline X \underline Z}$. Its colliders are in $S$ but not in $Z$, so they are in $X \cup W$. Its non-colliders are not in $X \cup W$. So $Y$ and $Z$ are d-connected given $X \cup W$ in $G_{\overline X \underline Z}$, against the condition. $\square$

**Rule 3.** We show $(Y \perp F \mid X, W)_{G'}$. Then $P_{M_{x,z}}(y \mid w) = P'(y \mid F = z, w) = P'(y \mid F = \text{idle}, w) = P_{M_x}(y \mid w)$, which is rule 3.

Suppose a walk from some $F_v$ to $Y$ is open given $S = X \cup W$. Cut it at its first node in $Y$, and let $z^*$ be the last node of $Z$ on it. As before, the part $p$ from $z^*$ to $Y$ uses no switch arrow, and its inner nodes are not in $Z$.

- If $p$ leaves $z^*$ through an arrow out of $z^*$, or if $z^* \notin Z(W)$, then every arrow of $p$ is in $G_{\overline X\, \overline{Z(W)}}$. Then $p$ is open given $X \cup W$ there, against the condition.
- Otherwise $p$ starts with an arrow into $z^*$, and $z^* \in Z(W)$. Look at the arrow by which the walk reaches this visit of $z^*$. If it points into $z^*$, then $z^*$ is a collider, so $z^* \in S$. But $z^* \in Z$ is not in $X \cup W$. So the walk reaches $z^*$ from a child $b_1$, with $z^* \to b_1$. Read the walk backwards from $z^*$. It follows arrows forward, $z^* \to b_1 \to b_2 \to \cdots$, until the first node $b_k$ where it turns and takes an arrow that points into $b_k$. Such a turn exists: the graph is acyclic, and the walk starts with $F_v \to v$, which points into $v$. At $b_k$ both arrows point in, so $b_k$ is a collider and $b_k \in S = X \cup W$. No arrow enters a node of $X$ in $G_{\overline X}$, so $b_k \in W$. Then $z^*$ is an ancestor of a node of $W$ in $G_{\overline X}$, which contradicts $z^* \in Z(W)$. $\square$

**Completeness.** The proof is long, and we only describe it. Shpitser and Pearl (2006) give an algorithm, ID, that takes $G$, $X$ and $Y$. It either returns a formula for $P(y \mid \mathrm{do}(x))$ in terms of the observed distribution, or it finds a structure called a *hedge*. Each step of ID that returns a formula follows from the three rules and probability calculus. When ID finds a hedge, they build two models with the graph $G$ that agree on the observed distribution but disagree on $P(y \mid \mathrm{do}(x))$. So the effect is not identifiable. Huang and Valtorta (2006) proved completeness in the same year with a related algorithm.

## Consequences

**The back-door adjustment.** If $Z$ satisfies the [back-door criterion](/backdoor-criterion/) relative to $(X, Y)$, then

$$P(y \mid \mathrm{do}(x)) = \sum_z P(y \mid \mathrm{do}(x), z)\, P(z \mid \mathrm{do}(x)) = \sum_z P(y \mid x, z)\, P(z).$$

The second step uses rule 3 for $P(z \mid \mathrm{do}(x)) = P(z)$: no node of $Z$ is a descendant of $X$, so every path from $X$ to $Z$ in $G_{\overline X}$ has a collider, and the conditioning set is empty. It uses rule 2 for $P(y \mid \mathrm{do}(x), z) = P(y \mid x, z)$: its condition $(Y \perp X \mid Z)_{G_{\underline X}}$ is the second half of the back-door criterion.

**The front-door formula.** Let $U$ be hidden with $U \to X$ and $U \to Y$, and let $X \to M \to Y$. No observed set satisfies the back-door criterion, but the rules identify the effect.

1. $P(m \mid \mathrm{do}(x)) = P(m \mid x)$ by rule 2, since $(M \perp X)_{G_{\underline X}}$: the only path $X \leftarrow U \to Y \leftarrow M$ has the collider $Y$.
2. $P(y \mid \mathrm{do}(x), m) = P(y \mid \mathrm{do}(x), \mathrm{do}(m))$ by rule 2, since in $G_{\overline X \underline M}$ the only arrows left are $U \to Y$ and $X \to M$, and $X$ is in the condition. Then $P(y \mid \mathrm{do}(x), \mathrm{do}(m)) = P(y \mid \mathrm{do}(m))$ by rule 3, since $X$ has no arrows at all in $G_{\overline M\, \overline X}$.
3. $P(y \mid \mathrm{do}(m)) = \sum_{x'} P(y \mid x', m) P(x')$. This is the back-door adjustment with $Z = \{X\}$: rule 2 gives $P(y \mid \mathrm{do}(m), x') = P(y \mid m, x')$, and rule 3 gives $P(x' \mid \mathrm{do}(m)) = P(x')$.

Then $P(y \mid \mathrm{do}(x)) = \sum_m P(m \mid \mathrm{do}(x)) P(y \mid \mathrm{do}(x), m) = \sum_m P(m \mid x) \sum_{x'} P(y \mid x', m) P(x')$. The back-door criterion page computes this on numbers: $0.61$ for $\mathrm{do}(X = 1)$, where the plain conditional gives $0.7$. Step 1 cannot be repeated for $Y$: in $G_{\underline X}$ the path $X \leftarrow U \to Y$ is open, so $P(y \mid \mathrm{do}(x)) \ne P(y \mid x)$ in general.

**Models with no hidden variables.** If no variable is hidden, the back-door adjustment with $Z = \mathrm{Pa}(X)$ always applies, and it gives the truncated factorization of the [structural causal model](/structural-causal-model/) page. So the calculus matters only when some variables are hidden.

**Algorithms.** The ID algorithm turns completeness into a procedure. It splits the graph into *c-components*, the sets of nodes joined by hidden common causes (Tian and Pearl 2002), and works on each one. It runs in time polynomial in the size of the graph, so nobody needs to search over sequences of rules by hand.

**Checks in code.** The implementation tests the three conditions with the reachability search of the [d-separation query](/d-separation-query/) page on the cut graphs. It also computes every interventional distribution of a causal Bayesian network with hidden nodes exactly, by the truncated factorization over all nodes, with fractions. The tests:

- draw 150 random DAGs with 5 or 6 nodes, up to two hidden nodes, and tables with entries in $\{\frac1{10}, \dots, \frac9{10}\}$;
- for random disjoint $X$, $Y$, $Z$, $W$, check each rule's equality for every value whenever its graph condition holds (39, 86 and 84 cases for rules 1, 2 and 3);
- confirm that the equality fails for some values in most cases where the condition does not hold;
- check each step of the front-door derivation and the examples below.

## Tightness

- **Rule 2 cuts the arrows out of $Z$.** In the graph $Z \to Y$ alone, $Y$ and $Z$ are d-connected in $G$, yet $P(y \mid \mathrm{do}(z)) = P(y \mid z)$. A link that leaves $Z$ through its own effects carries the same information in the experiment and in the observation. Only the back-door links, which enter $Z$, can make them differ. So rule 2 tests the graph without the arrows out of $Z$.
- **$Z(W)$, not $Z$, in rule 3.** Let $U \to Z$, $U \to Y$ and $Z \to W$, with all nodes observed. In $G_{\overline Z}$ the node $Z$ has only the arrow $Z \to W$, so $(Y \perp Z \mid W)$ holds there. But $P(y \mid \mathrm{do}(z), w) = P(y)$, while $P(y \mid w) \ne P(y)$ in general, since $W$ carries news about $U$ through $Z$. The correct rule keeps the arrow $U \to Z$, because $Z$ is an ancestor of $W$, and then $Z \leftarrow U \to Y$ is open given $W$. The tests check this example with numbers: $P(Y = 1 \mid \mathrm{do}(Z = 1), W = 1) = P(Y = 1) = 0.45$, but $P(Y = 1 \mid W = 1) \ne 0.45$.
- **Not every effect is identifiable.** In the *bow graph* $X \to Y$ with a hidden $U \to X$, $U \to Y$, take a fair coin $U$. Model A has $X := U$, $Y := U$. Model B has $X := U$, $Y := X$. Both give $X = Y$, a fair coin. But $P(Y = 1 \mid \mathrm{do}(X = 1))$ is $\frac12$ in model A and $1$ in model B. Model A does not use the arrow $X \to Y$, which a model with the graph is allowed to do. So no sequence of rules can remove the $\mathrm{do}$ here.
- **The rules give equalities for every model with the graph.** A particular model can have more equalities, for example when two causal paths cancel. The rules do not find those.

## History

Pearl's 1993 comment in *Statistical Science* treated an intervention as a new root node in the graph, which is the switch node of the proof above. In "Causal diagrams for empirical research" (Biometrika, 1995), with discussion, he stated the three rules, proved them by that construction, and derived the back-door and front-door formulas. Pearl conjectured that the rules were complete. Tian and Pearl (2002) introduced c-components and a general condition for the effect of a single intervention. In 2006, Shpitser and Pearl gave the ID algorithm with its hedge criterion, and Huang and Valtorta proved completeness independently. Shpitser and Pearl later extended the results to conditional effects and to counterfactual queries.

## References
