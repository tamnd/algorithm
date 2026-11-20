---
tag: 3QBKM0
kind: theorem
slug: roberts-theorem
name: "Roberts' theorem"
aliases:
- affine maximizer characterization
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: "On the unrestricted domain, every deterministic DSIC mechanism onto a range of at least 3 outcomes is an affine maximizer, with nonnegative weights not all zero and constants per outcome."
prereqs: [affine-maximizer, cycle-monotonicity]
see_also: [green-laffont-theorem, affine-maximizer, gibbard-satterthwaite-theorem, maximal-in-range-mechanism, vcg-mechanism, myerson-lemma, combinatorial-auction, nisan-ronen-conjecture]
sources:
  - paper: "Kevin Roberts, The characterization of implementable choice rules, in Jean-Jacques Laffont (ed.), Aggregation and Revelation of Preferences, North-Holland, 1979, 321-348"
    locator: the original theorem that implementable choice rules on the unrestricted quasilinear domain are affine maximizers
  - paper: doi:10.1007/s00355-008-0331-y
    title: "Ron Lavi, Ahuva Mu'alem and Noam Nisan, Two simplified proofs for Roberts' theorem, Social Choice and Welfare 32(3) (2009), 407-423"
    locator: the proof through weak monotonicity and positive association of differences, followed in the outline on this page
  - paper: "Shahar Dobzinski and Noam Nisan, A modular approach to Roberts' theorem, Proceedings of the 2nd International Symposium on Algorithmic Game Theory (SAGT 2009)"
    locator: a further proof that separates the steps of the argument
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), the part on affine maximizers and Roberts' theorem
---

Roberts' theorem says that on the unrestricted quasilinear domain, with at least three possible outcomes, the only deterministic outcome rules that can be made [DSIC](/dominant-strategy-incentive-compatibility/) are the [affine maximizers](/affine-maximizer/): rules that maximize a weighted sum of the agents' values, with nonnegative weights, plus a fixed constant for each outcome. Its close page, the [Green-Laffont theorem](/green-laffont-theorem/), works in the same domain but answers a different question: it takes the efficient rule as given and shows that its DSIC payments are the Groves payments. Roberts characterizes the outcome rules, and Green-Laffont the payments. Roberts' theorem is the money analog of the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/), and it explains why truthful approximation on rich domains is usually built from [maximal-in-range mechanisms](/maximal-in-range-mechanism/).

## Statement

Let $O$ be a finite set of outcomes and let there be $n$ agents with [quasilinear utilities](/quasilinear-utility/). Each agent's type set is the unrestricted domain $V_i = \mathbb{R}^O$. Let $f : V_1 \times \dots \times V_n \to O$ be a deterministic outcome rule whose range $R = \{ f(v) : v \in V \}$ has at least 3 elements.

**Theorem (Roberts 1979).** If there are payments $p$ such that $(f, p)$ is DSIC, then there are weights $k_1, \dots, k_n \ge 0$, not all 0, and constants $C : R \to \mathbb{R}$ such that for every profile $v$,
$$f(v) \in \arg\max_{o \in R} \Bigl( \sum_{i=1}^{n} k_i \, v_i(o) + C(o) \Bigr).$$

Conversely, every affine maximizer with positive weights is DSIC with weighted VCG payments, and an agent with weight 0 can be given a payment that does not depend on its report. So the theorem is a characterization.

## In plain words

Suppose a group must pick one of at least three options, everyone can have any values at all for the options, and money can change hands. Suppose the rule is designed so that nobody can ever gain by lying. Then the rule must work in a fixed and simple way. It gives each person a fixed importance, adds up the values of everyone with these importances, adds a fixed bonus to each option, and picks the option with the largest total. The importances and bonuses cannot depend on what anyone says. The usual rule that picks the best option for the group is one such rule, with equal importances and no bonuses. With only two options, many other rules are honest too.

## Proof

**One agent.** With $n = 1$ the theorem has a short complete proof. Let $(f, p)$ be DSIC. If $f(v) = f(v') = o$ and $p(v) < p(v')$, then type $v'$ gains by reporting $v$, so the payment depends only on the outcome: $p(v) = \pi(f(v))$ for a function $\pi$ on $R$. Every $o \in R$ is reachable by some report, so DSIC says that $f(v)$ maximizes $v(o) - \pi(o)$ over $R$. This is the affine form with $k_1 = 1$ and $C = -\pi$. For example, if the menu is $\pi(a) = 0$, $\pi(b) = 2$, $\pi(c) = 5$ and the type is $v = (3, 4, 9)$, the agent compares $3$, $2$ and $4$ and gets $c$. This case needs no assumption on the size of $R$.

**Many agents: outline.** The general proof is longer. The outline below follows Lavi, Mu'alem and Nisan (2009). Steps 1 and 2 are proved in full; step 3 is described, and the details are in their paper.

*Step 1: weak monotonicity.* Fix $i$ and $v_{-i}$. If $f(v_i, v_{-i}) = a$ and $f(v_i', v_{-i}) = b$, then
$$v_i(a) - v_i(b) \;\ge\; v_i'(a) - v_i'(b).$$
This is the 2-cycle case of [cycle monotonicity](/cycle-monotonicity/) and follows by adding the two DSIC inequalities, as there.

*Step 2: positive association of differences (PAD).* Let $f(v) = a$, and let $v'$ be a profile such that for every agent $i$ and every outcome $b \ne a$,
$$v_i'(a) - v_i(a) \;>\; v_i'(b) - v_i(b).$$
Then $f(v') = a$. Proof: change the agents from $v_i$ to $v_i'$ one at a time. Suppose that after changing agent 1, the outcome is $b \ne a$. Weak monotonicity for agent 1, with the type $v_1$ getting $a$ and the type $v_1'$ getting $b$, gives $v_1(a) - v_1(b) \ge v_1'(a) - v_1'(b)$, that is $v_1'(a) - v_1(a) \le v_1'(b) - v_1(b)$, which contradicts the assumption. So the outcome stays $a$. The same argument applies to agents $2, \dots, n$ in turn.

*Step 3: from PAD to a hyperplane.* For two outcomes $a \ne b$ in $R$, consider the set $P(a, b) \subseteq \mathbb{R}^n$ of difference vectors $\alpha$ for which there is a profile $v$ with $f(v) = a$ and $v_i(a) - v_i(b) = \alpha_i$ for all $i$. PAD gives three facts. First, $P(a, b)$ is closed upward: if $\alpha \in P(a, b)$ then $\alpha + \delta \in P(a, b)$ for every $\delta$ with all coordinates positive (raise each $v_i(a)$ by $\delta_i$ and leave the rest). Second, if $\alpha \in P(a, b)$ then $-\alpha - \delta \notin P(b, a)$ for $\delta > 0$, since a profile could otherwise be pushed toward both $a$ and $b$. Third, when all outcomes other than $a$ and $b$ have very low values, one of $a$ and $b$ must be chosen, so $\mathbb{R}^n$ is covered by $P(a, b)$ and $-P(b, a)$ up to the boundary. With a third outcome $c$, the sets satisfy $P(a, b) + P(b, c) \subseteq P(a, c)$ up to the boundary. This additivity is where $|R| \ge 3$ is used. Lavi, Mu'alem and Nisan show from these facts that all the sets $P(a, b)$ are translates of one convex set whose boundary is a hyperplane. Its normal vector gives the weights $k \ge 0$, and the translations give the constants $C(a) - C(b)$. $\square$

## Consequences

**Truthful rules on rich domains are weighted welfare maximizers.** If a mechanism must work for every valuation function over at least three outcomes, then it has no freedom beyond weights, constants and the choice of range. Objectives that are not affine, such as a max-min fairness objective, cannot be implemented exactly on this domain.

**Computation.** An affine maximizer over a large range, such as all allocations of a [combinatorial auction](/combinatorial-auction/), is as hard to compute as welfare maximization. Polynomial-time truthful mechanisms on rich domains are therefore often affine maximizers over a smaller range, which is the idea of [maximal-in-range mechanisms](/maximal-in-range-mechanism/). Nisan and Ronen (2007) showed that truthful VCG-based mechanisms must be maximal in range.

**Comparison with the case without money.** The [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) says that without money, on all strict preference orders over at least three outcomes, every strategyproof onto rule is a dictatorship. Roberts' theorem replaces dictatorship by affine maximization. A dictatorship is the special case with one weight 1, the others 0, and no constants.

**Payments.** Once the rule is an affine maximizer with positive weights, the argument of the [Green-Laffont theorem](/green-laffont-theorem/) shows that the payments are the weighted Groves payments, up to terms $h_i(b_{-i})$.

## Tightness

**Two outcomes are not enough.** With $R = \{\text{build}, \text{not}\}$, write $d_i = v_i(\text{build}) - v_i(\text{not})$ for each of three agents, and build when at least two agents have $d_i \ge 0$. The rule depends on each agent's report only through $d_i$, and more $d_i$ never turns "build" into "not". So it is monotone in a single-parameter sense, and threshold payments make it DSIC: a pivotal agent pays its threshold difference, 0. It is not an affine maximizer. The profile $d = (1, 1, -M)$ builds for every $M > 0$, so $k_1 + k_2 - M k_3 + C \ge 0$ for all $M$ forces $k_3 = 0$, where $C = C(\text{build}) - C(\text{not})$. By symmetry $k_1 = k_2 = 0$, so all weights are 0, which the conclusion of the theorem does not allow.

**The domain must be unrestricted.** In a [single-parameter environment](/single-parameter-environment/), [Myerson's lemma](/myerson-lemma/) allows every monotone rule, and many are not affine maximizers: the optimal auction with bidders of different distributions and the greedy knapsack rule are examples. Combinatorial auctions are also a restricted domain, since values are for bundles and an agent cares only about its own bundle, so Roberts' theorem does not apply there directly.

**Weights may be zero.** The theorem cannot promise positive weights. The rule that always picks agent 1's favorite outcome is DSIC with zero payments, and in affine form it has $k_1 = 1$ and $k_i = 0$ for all other agents.

**Deterministic rules only.** Randomized mechanisms that are [truthful in expectation](/truthful-in-expectation/) are not covered. Their outcome is a lottery, and the set of lotteries is infinite.

## History

Roberts (1979) proved the theorem in a volume edited by Laffont on the revelation of preferences. The original proof was considered hard to follow, and the result became widely used in computer science only after algorithmic mechanism design raised the question of which truthful rules are computationally feasible. Lavi, Mu'alem and Nisan (2009) gave two simpler proofs based on weak monotonicity, and Dobzinski and Nisan (2009) gave a modular one. Nisan's chapter in the *Algorithmic Game Theory* book (2007) presents the theorem as the main limit on truthful mechanism design for unrestricted domains.

## References
