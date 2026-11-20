---
tag: 160Q7Q
kind: theorem
slug: cycle-monotonicity
name: "Rochet's theorem on cycle monotonicity"
aliases:
- cycle monotonicity
- "Rochet's theorem"
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: "Rochet (1987): an outcome rule can be made truthful with payments if and only if it is cycle monotone, meaning that no finite cycle of types has a negative total gain."
prereqs: [monotone-allocation-rule, dominant-strategy-incentive-compatibility]
see_also: [myerson-lemma, roberts-theorem, affine-maximizer, negative-cycle, bellman-ford, truthful-scheduling-unrelated-machines, convex-set, green-laffont-theorem]
sources:
  - paper: "Jean-Charles Rochet, A necessary and sufficient condition for rationalizability in a quasi-linear context, Journal of Mathematical Economics 16(2) (1987), 191-200"
    locator: the cyclic monotonicity condition and the construction of the payment by path sums
  - paper: doi:10.1145/1064009.1064040
    title: "Michael Saks and Lan Yu, Weak monotonicity suffices for truthfulness on convex domains, Proceedings of the 6th ACM Conference on Electronic Commerce (EC 2005), 286-293"
    locator: weak monotonicity implies cycle monotonicity when the type set is convex and the outcome set is finite
  - paper: doi:10.1111/j.1468-0262.2006.00695.x
    title: "Sushil Bikhchandani, Shurojit Chatterji, Ron Lavi, Ahuva Mu'alem, Noam Nisan and Arunava Sen, Weak monotonicity characterizes deterministic dominant-strategy implementation, Econometrica 74(4) (2006), 1109-1132"
    locator: weak monotonicity as the characterization on rich domains, including auction domains
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), the part on weak monotonicity; Chapter 12, Ron Lavi, Computationally efficient approximation mechanisms
  - book: "Rakesh V. Vohra, Mechanism Design: A Linear Programming Approach, Cambridge University Press, 2011"
    locator: the chapter on incentive compatibility, where cycle monotonicity is read as the absence of negative cycles in a graph of types
  - paper: "Ron Lavi and Chaitanya Swamy, Truthful mechanism design for multidimensional scheduling via cycle monotonicity, Games and Economic Behavior, 2009 (conference version in EC 2007)"
    locator: the design of truthful scheduling mechanisms by checking cycle monotonicity directly
---

Rochet's theorem says that a deterministic outcome rule can be paired with payments that make truthful reporting a dominant strategy if and only if it is *cycle monotone*: for every finite cycle of types, the total gain of each type from its own outcome over the next type's outcome is at least zero. It works for any type set, of any dimension. Its close page, [monotone allocation rule](/monotone-allocation-rule/), is the special case of one-number types, where cycle monotonicity reduces to "bid more, get more" and [Myerson's lemma](/myerson-lemma/) gives the payments in closed form. For vector types, checking pairs of types alone, which is weak monotonicity, is not enough in general.

## Statement

Truthfulness for agent $i$ is a condition for each fixed profile $b_{-i}$ of the other reports, so it is enough to treat one agent. Let $O$ be a set of outcomes, let $T$ be a set of valuations $t : O \to \mathbb{R}$, the agent's possible types, and let $f : T \to O$ be an outcome rule. A payment function $p : T \to \mathbb{R}$ **implements** $f$ if
$$t(f(t)) - p(t) \;\ge\; t(f(s)) - p(s) \quad \text{for all } s, t \in T. \tag{1}$$
The rule $f$ is **cycle monotone** if for every $k \ge 1$ and all types $t^0, t^1, \dots, t^{k-1} \in T$, with $t^k = t^0$,
$$\sum_{j=0}^{k-1} \Bigl( t^j\bigl(f(t^j)\bigr) - t^j\bigl(f(t^{j+1})\bigr) \Bigr) \;\ge\; 0. \tag{2}$$
The case $k = 2$ is **weak monotonicity**: if $f(t) = a$ and $f(s) = b$, then $t(a) - t(b) \ge s(a) - s(b)$.

**Theorem (Rochet 1987).** There is a payment function that implements $f$ if and only if $f$ is cycle monotone.

For $n$ agents, a mechanism $(f, p)$ is [DSIC](/dominant-strategy-incentive-compatibility/) if and only if, for every $i$ and every $b_{-i}$, the rule $t \mapsto f(t, b_{-i})$ satisfies (2) on agent $i$'s type set. Then the theorem gives the payments $p_i(\cdot, b_{-i})$ for each $b_{-i}$ separately.

## In plain words

Imagine a short tour through a few possible kinds of agent, ending where it started. At each stop, ask how much that kind of agent prefers what the rule gives it over what the rule gives the next kind on the tour. Add these amounts over the whole tour. The rule can be made honest with suitable prices exactly when this total is never negative, for every tour of any length. If some tour has a negative total, then any prices fail: the price differences along the tour would have to add up to more than zero, but they come back to the start and add up to exactly zero. When no tour is negative, the right prices are the shortest-route distances in a network whose stops are the kinds of agent.

## Proof

**Necessity.** Let $p$ implement $f$ and take a cycle $t^0, \dots, t^{k-1}, t^k = t^0$. Inequality (1) for the true type $t^j$ and the report $t^{j+1}$ gives
$$t^j\bigl(f(t^j)\bigr) - t^j\bigl(f(t^{j+1})\bigr) \;\ge\; p(t^j) - p(t^{j+1}).$$
Summing over $j$, the right side telescopes to $p(t^0) - p(t^k) = 0$. This is (2).

**Sufficiency.** Let $f$ be cycle monotone. For $s, t \in T$ define the length
$$c(s, t) = t\bigl(f(t)\bigr) - t\bigl(f(s)\bigr),$$
the gain of type $t$ from its own outcome over the outcome of $s$. Inequality (1) says exactly $p(t) \le p(s) + c(s, t)$ for all $s, t$. So the task is to find a *potential* $p$ on the complete directed graph with vertex set $T$ and edge lengths $c$, the same condition as for [shortest-path](/shortest-path/) distances.

The sum of $c$ around a cycle $t^0 \to t^1 \to \dots \to t^k = t^0$ is
$$\sum_{j=0}^{k-1} \Bigl( t^{j+1}\bigl(f(t^{j+1})\bigr) - t^{j+1}\bigl(f(t^j)\bigr) \Bigr),$$
which is the sum (2) for the same cycle traversed backwards. So cycle monotonicity says that this graph has no [negative cycle](/negative-cycle/).

Fix a type $t^0 \in T$ and set
$$p(t) = \inf \Bigl\{ \textstyle\sum_{j=1}^{k} c(s_{j-1}, s_j) \;:\; k \ge 0, \; s_0 = t^0, \; s_k = t, \; s_1, \dots, s_{k-1} \in T \Bigr\},$$
the infimum over all finite paths from $t^0$ to $t$. The one-edge path gives $p(t) \le c(t^0, t) < \infty$. For any path from $t^0$ to $t$, adding the edge from $t$ back to $t^0$ closes a cycle, whose length is at least 0. So every path has length at least $-c(t, t^0)$, and $p(t) > -\infty$. Finally, any path from $t^0$ to $s$ followed by the edge $(s, t)$ is a path to $t$, so $p(t) \le p(s) + c(s, t)$. That is (1), so $p$ implements $f$. The type set may be infinite; only finite paths and cycles are used. $\square$

## Consequences

**A small example where pairs are not enough.** There are three outcomes $a, b, c$ and three types, written as values $(t(a), t(b), t(c))$:
$$t^1 = (1, 2, 0), \qquad t^2 = (0, 1, 2), \qquad t^3 = (2, 0, 1),$$
with $f(t^1) = a$, $f(t^2) = b$ and $f(t^3) = c$. Every 2-cycle has sum 0. For example, the pair $t^1, t^2$ gives $(t^1(a) - t^1(b)) + (t^2(b) - t^2(a)) = -1 + 1 = 0$. So $f$ is weakly monotone. The 3-cycle $t^1, t^2, t^3$ gives
$$(1 - 2) + (1 - 2) + (1 - 2) = -3 < 0,$$
so $f$ is not cycle monotone. A direct check: the payments $p_a, p_b, p_c$ would need $p_b - p_a \ge 1$ for $t^1$, $p_c - p_b \ge 1$ for $t^2$ and $p_a - p_c \ge 1$ for $t^3$, and these three add up to $0 \ge 3$.

**One-number types.** If every type has the form $t(o) = v \cdot x(o)$ for a number $v$ and a fixed function $x$, as in a [single-parameter environment](/single-parameter-environment/), weak monotonicity for types $v$ and $w$ reads $(v - w)(x(f(v)) - x(f(w))) \ge 0$, which is monotonicity of the allocation. On interval type sets, monotone rules have payments by Myerson's lemma, so by the necessity part they are cycle monotone. So in one dimension the 2-cycle condition already implies the condition for all cycles.

**Convex domains.** Saks and Yu (2005) proved that when $O$ is finite and the type set is a convex subset of $\mathbb{R}^O$, weak monotonicity implies cycle monotonicity. Bikhchandani, Chatterji, Lavi, Mu'alem, Nisan and Sen (2006) showed that weak monotonicity characterizes implementability on other rich domains, including auction domains. The small example above is not convex, which is why it can fail.

**Computing payments.** For a finite type set, the payments are shortest-path distances and can be computed with the [Bellman-Ford algorithm](/bellman-ford/), which also detects a negative cycle, that is, a failure of (2).

**Designing mechanisms.** Lavi and Swamy (2009) built truthful mechanisms for scheduling on unrelated machines with two possible values per job by proving cycle monotonicity of their allocation rules directly. Lower bounds such as the one for [truthful scheduling on unrelated machines](/truthful-scheduling-unrelated-machines/) use weak monotonicity, the 2-cycle case, as their main tool, and so do the proofs of [Roberts' theorem](/roberts-theorem/).

**Outcome form.** By (1), two types with the same outcome must pay the same, so the payment depends only on the outcome. Writing $\delta(a, b) = \inf \{ t(b) - t(a) : f(t) = b \}$ for outcomes $a, b$ in the range, cycle monotonicity is the absence of negative cycles in the graph on outcomes with lengths $\delta$.

## Tightness

**Cycles of every length are needed.** The small example is weakly monotone but has no payments, so the condition for $k = 2$ cannot replace the full condition on general domains. Cycles of length 3 were enough there; on larger type sets longer cycles can be needed.

**The theorem needs quasilinear utility.** The telescoping in the necessity proof and the potential in the sufficiency proof use utilities of the form value minus payment. With budgets or risk aversion, the condition is different.

**Payments are not unique in general.** The construction gives one implementing $p$. On some domains other implementing payments differ from it by more than a constant, as in the two-bid example on the page [Myerson's lemma](/myerson-lemma/). On connected domains such as convex ones, payments are unique up to a constant, which is a form of [revenue equivalence](/revenue-equivalence-theorem/); compare the [Green-Laffont theorem](/green-laffont-theorem/) for efficient rules.

**Deterministic rules.** The statement is for deterministic $f$. For randomized rules it applies to lotteries over outcomes with expected values, which gives [truthfulness in expectation](/truthful-in-expectation/).

## History

Rochet (1987) proved the theorem in the language of rationalizability: an allocation rule can be rationalized by a payment schedule in a quasilinear setting exactly when it is cyclically monotone. The condition has the same form as the cyclical monotonicity that characterizes subgradients of convex functions in convex analysis. In algorithmic mechanism design the theorem was brought into use in the 2000s. Bikhchandani, Chatterji, Lavi, Mu'alem, Nisan and Sen (2006) and Saks and Yu (2005) studied when weak monotonicity suffices, and Lavi and Swamy (2007 conference, 2009 journal) used cycle monotonicity directly to design scheduling mechanisms. Vohra's book (2011) presents the theory through the network form used in the proof above.

## References
