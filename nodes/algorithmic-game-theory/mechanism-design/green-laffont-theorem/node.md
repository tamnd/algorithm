---
tag: NNHGSZ
kind: theorem
slug: green-laffont-theorem
name: Green-Laffont theorem
aliases:
- uniqueness of Groves mechanisms
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: "On unrestricted domains, every efficient DSIC mechanism is a Groves mechanism. A separate result (Green and Laffont 1979; Hurwicz; Walker 1980) shows that none is budget balanced."
prereqs: [groves-mechanisms, budget-balance]
see_also: [roberts-theorem, vcg-mechanism, clarke-pivot-rule, affine-maximizer, myerson-satterthwaite-theorem, agv-mechanism, revenue-equivalence-theorem, cycle-monotonicity]
sources:
  - paper: doi:10.2307/1911219
    title: "Jerry Green and Jean-Jacques Laffont, Characterization of satisfactory mechanisms for the revelation of preferences for public goods, Econometrica 45(2) (1977), 427-438"
    locator: the uniqueness of Groves mechanisms among efficient dominant-strategy mechanisms on unrestricted domains
  - paper: doi:10.2307/1911954
    title: "Bengt Holmstrom, Groves' scheme on restricted domains, Econometrica 47(5) (1979), 1137-1144"
    locator: the uniqueness on smoothly connected domains, which include the convex ones
  - book: "Jerry Green and Jean-Jacques Laffont, Incentives in Public Decision-Making, North-Holland, 1979 (Studies in Public Economics 1)"
    locator: the impossibility of strong budget balance for Groves mechanisms
  - paper: doi:10.2307/1912822
    title: "Mark Walker, On the nonexistence of a dominant strategy mechanism for making optimal public decisions, Econometrica 48(6) (1980), 1521-1540"
    locator: no efficient dominant-strategy mechanism for public decisions is budget balanced
  - paper: "Leonid Hurwicz and Mark Walker, On the generic nonoptimality of dominant-strategy allocation mechanisms, a general theorem that includes pure exchange economies, Econometrica 58(3) (1990), 683-704"
    locator: the general form of the budget-balance impossibility
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), Section 9.5.5 (uniqueness of prices on connected domains, with corollaries for welfare maximizers, bilateral trade and the public project)
  - paper: "Jean-Jacques Laffont and Eric Maskin, A differential approach to dominant strategy mechanisms, Econometrica 48(6) (1980), 1507-1520"
    locator: the characterization of dominant-strategy mechanisms on smooth domains by first-order conditions
---

The Green-Laffont theorem says that on unrestricted domains the [Groves mechanisms](/groves-mechanisms/) are the only [DSIC](/dominant-strategy-incentive-compatibility/) mechanisms that maximize welfare: once the outcome rule is efficient, the payments are fixed up to a term $h_i$ that does not depend on the report of agent $i$. It differs from [Roberts' theorem](/roberts-theorem/), its close page, in what it fixes. Green-Laffont takes the efficient outcome rule as given and characterizes the payments, while Roberts characterizes the outcome rules themselves, as affine maximizers. A second, separate result, in Green and Laffont (1979), Walker (1980) and Hurwicz and Walker (1990), adds that no Groves mechanism is budget balanced, so no efficient DSIC mechanism on this domain is.

## Statement

Let $O$ be a finite set with $|O| \ge 2$, and let there be $n$ agents with [quasilinear utilities](/quasilinear-utility/). The domain is *unrestricted*: each agent's type set is $V_i = \mathbb{R}^O$, all functions $O \to \mathbb{R}$.

**Theorem 1 (uniqueness; Green and Laffont 1977).** Let $(x, p)$ be a DSIC direct mechanism on the unrestricted domain such that $x(b) \in \arg\max_{o} \sum_j b_j(o)$ for every profile $b$, with any rule for ties. Then for each agent $i$ there is a function $h_i$ of $b_{-i}$ such that
$$p_i(b) = h_i(b_{-i}) - \sum_{j \ne i} b_j(x(b)) \quad \text{for every } b.$$

**Theorem 2 (budget balance; Green and Laffont 1979, Walker 1980, Hurwicz and Walker 1990).** If $n \ge 2$, no Groves mechanism on the unrestricted domain is strongly [budget balanced](/budget-balance/): for every choice of the functions $h_i$ there is a profile $b$ with $\sum_i p_i(b) \ne 0$.

Together: on the unrestricted domain with $n \ge 2$, no mechanism is efficient, DSIC and strongly budget balanced.

## In plain words

Suppose a mechanism always takes the choice that is best for the group, and nobody can ever gain by lying about their values. Then the way it charges people is almost forced. Each person must be paid the value the others get from the choice, and then charged an amount that the person's own answer does not affect. The only freedom left is this charge. A second result shows that this freedom is not enough to make the payments add up to zero for every possible set of answers. So such a mechanism must sometimes take money out of the group or put money in.

## Proof

**Theorem 1.** Fix an agent $i$ and the reports $b_{-i}$ of the others, and write $V(o) = \sum_{j \ne i} b_j(o)$. All quantities below are for this fixed $b_{-i}$, and $x(b_i)$, $p(b_i)$ are short for $x(b_i, b_{-i})$, $p_i(b_i, b_{-i})$.

Step 1: the payment depends only on the outcome. Let $x(b_i) = x(b_i')$. If $p(b_i) > p(b_i')$, then an agent of type $b_i$ gets the same outcome and pays less by reporting $b_i'$, which contradicts DSIC. By symmetry $p(b_i) = p(b_i')$. So there is a function $P$ on the range $R = \{x(b_i) : b_i \in V_i\}$ with $p(b_i) = P(x(b_i))$. The range is all of $O$: for any $o$, the report with $b_i(o) = K$ and $b_i(o') = 0$ elsewhere, with $K$ larger than $\max V - \min V$, makes $o$ the unique maximizer of $b_i + V$.

Step 2: $P(o) + V(o)$ is the same for all $o$. Let $H(o) = P(o) + V(o)$ and suppose $H(a) < H(c)$ for two outcomes $a$ and $c$. Choose $t$ with $0 < t < H(c) - H(a)$, and define the type $u$ by
$$u(c) = t - V(c), \qquad u(a) = -V(a), \qquad u(o) = -V(o) - 1 \text{ for every other } o.$$
Then $u(o) + V(o)$ is $t$ at $c$, 0 at $a$ and $-1$ elsewhere, so $c$ is the unique maximizer and the truthful report $u$ gives the outcome $c$. Its utility is $u(c) - P(c) = t - H(c)$. A report that gives the outcome $a$ exists by Step 1, and it gives the utility $u(a) - P(a) = -H(a)$. Since $-H(a) > t - H(c)$, the lie is profitable, which contradicts DSIC. So $H$ is constant on $O$. Call the constant $h_i(b_{-i})$. Then $p_i(b) = P(x(b)) = h_i(b_{-i}) - V(x(b))$, which is the Groves form. $\square$

The proof uses the unrestricted domain only in Step 1, to reach every outcome, and in Step 2, to use the type $u$. It works for any tie rule because $u$ has a unique maximizer.

**Theorem 2.** Fix two outcomes $o_0$ and $o_1$, and use only the types $v_i$ with $v_i(o_0) = 0$, $v_i(o_1) = \theta_i$ and $v_i(o) = -K$ elsewhere, with $K > 2n$, and $\theta_i \in \{a, a + 1\}$ for a number $a$ fixed below. With these types, an efficient rule chooses $o_1$ if $W = \sum_i \theta_i > 0$ and $o_0$ if $W < 0$. Write $h_i(\theta_{-i})$ for the Groves term. If the outcome is $o_1$, agent $i$ pays $h_i(\theta_{-i}) - (W - \theta_i)$, and the total payment is $\sum_i h_i(\theta_{-i}) - (n - 1) W$. If the outcome is $o_0$, the total payment is $\sum_i h_i(\theta_{-i})$. When $W = 0$ the two totals agree. So in every case
$$\sum_i p_i = \sum_i h_i(\theta_{-i}) - (n - 1) \max(0, W).$$

Suppose the mechanism is strongly budget balanced. Then $\sum_i h_i(\theta_{-i}) = (n - 1)\max(0, W)$ on all $2^n$ profiles of the cube $\{a, a + 1\}^n$. Apply the alternating sum $D f = \sum_{\varepsilon \in \{0, 1\}^n} (-1)^{n - |\varepsilon|} f(a + \varepsilon)$, where $|\varepsilon|$ is the number of ones. For a function that does not depend on $\theta_i$, the profiles pair up by flipping coordinate $i$, with opposite signs and equal values, so $D h_i = 0$ for each $i$, and $D$ of the left side is 0. Now take $a = -(n - 1)/n$. Then $W = |\varepsilon| - (n - 1)$, which is positive only for $\varepsilon = (1, \ldots, 1)$, where $W = 1$ and the sign is $+1$. So $D$ of the right side is $n - 1 \ge 1$. This is a contradiction, so the payments do not sum to 0 on some profile of the cube. $\square$

For $n = 2$ and $\theta_i \in \{-1/2, 1/2\}$, the alternating sum of the total payment is $-1$ for every choice of $h_1$ and $h_2$.

## Consequences

- **VCG is the canonical efficient DSIC mechanism.** On the unrestricted domain, any efficient DSIC mechanism is the [VCG mechanism](/vcg-mechanism/) plus a term $h_i(b_{-i}) - W_{-i}$ for each agent. If the zero valuation is a possible type, ex post IR forces $h_i \le W_{-i}$, so among the IR ones the [Clarke pivot rule](/clarke-pivot-rule/) collects the most.
- **Payments are pinned down.** Once the efficient outcome rule is fixed, the payment of agent $i$ is fixed up to a function of $b_{-i}$. This is the dominant-strategy analog of the [revenue equivalence theorem](/revenue-equivalence-theorem/).
- **Budget balance must be bought.** To balance the budget, give up one requirement: use the BIC [AGV mechanism](/agv-mechanism/), give up exact efficiency, or reduce the surplus with rebates that keep weak budget balance (Cavallo 2006). The surplus cannot reach zero on every profile.
- **The public project is underfunded.** With the planner as an agent, the payments of the citizens do not cover the cost in general, and no other efficient DSIC rule does better on all profiles (Nisan, Section 9.5.5).

## Tightness

- **Restricted domains.** Uniqueness can fail when the types are restricted. Take one agent, $O = \{0, 1\}$ and the two types $(1, 0)$ and $(0, 1)$. The efficient rule chooses 0 for the first type and 1 for the second. The payments $p = 0$ for the first type and $p = 1/2$ for the second are DSIC, since a lie changes the outcome for a gain of $-1$ and a payment change of at most $1/2$. A Groves mechanism with one agent has a constant payment, so this one is not Groves. Holmstrom (1979) showed that uniqueness holds on every smoothly connected domain, which includes the convex ones, so a finite type set like this one is outside the theorem.
- **One agent.** Theorem 2 needs $n \ge 2$. With one agent, $h_1 = 0$ gives the payment 0 and strong budget balance.
- **Weak budget balance is possible.** The Clarke pivot rule gives $\sum_i p_i \ge 0$, so Theorem 2 is only about the sum being exactly 0.
- **Bayesian incentives.** With a prior and independent types, the AGV mechanism is efficient, BIC and strongly budget balanced, so Theorem 2 needs dominant strategies. With interim IR added, even the Bayesian form fails for bilateral trade ([Myerson-Satterthwaite theorem](/myerson-satterthwaite-theorem/)).
- **Not about the outcome rule.** The theorem assumes that $x$ is efficient. Which outcome rules can be DSIC at all is the subject of [Roberts' theorem](/roberts-theorem/) and of [cycle monotonicity](/cycle-monotonicity/).

## History

Clarke (1971) and Groves (1973) found the payments that make efficient decisions DSIC. Green and Laffont (1977) proved that on unrestricted domains these are the only ones, and Holmstrom (1979) extended the uniqueness to smoothly connected domains. Laffont and Maskin (1980) gave a differential approach to dominant-strategy mechanisms on smooth domains. The impossibility of strong budget balance appears in the book of Green and Laffont (1979), Walker (1980) proved it for public decisions, and Hurwicz and Walker (1990) gave a general form that includes exchange economies.

## References
