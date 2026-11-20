---
tag: 9ACKCQ
kind: definition
slug: bayesian-incentive-compatibility
name: Bayesian incentive compatibility
aliases:
- Bayes-Nash incentive compatibility
area: algorithmic-game-theory/mechanism-design
level: core
summary: A direct mechanism is BIC when truth telling is a Bayes-Nash equilibrium under the common prior. Each agent gains nothing in expectation by lying if the others tell the truth.
prereqs: [direct-revelation-mechanism, bayes-nash-equilibrium, dominant-strategy-incentive-compatibility]
see_also: [revelation-principle, agv-mechanism, myerson-satterthwaite-theorem, border-theorem, cremer-mclean-theorem, myerson-optimal-auction, individual-rationality, automated-mechanism-design]
sources:
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), the section on Bayesian-Nash implementation
  - book: isbn:9780195073409
    title: Andreu Mas-Colell, Michael D. Whinston and Jerry R. Green, Microeconomic Theory, Oxford University Press, 1995
    locator: Chapter 23, Section 23.D (Bayesian implementation)
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the characterization of BIC mechanisms for single-parameter agents with independent values by monotone interim allocation and the payment formula
  - paper: doi:10.3982/ECTA10592
    title: "Alex Gershkov, Jacob K. Goeree, Alexey Kushnir, Benny Moldovanu and Xianwen Shi, On the equivalence of Bayesian and dominant strategy implementation, Econometrica 81(1) (2013), 197-220"
    locator: for linear utilities and independent one-dimensional types, every BIC mechanism has a DSIC mechanism with the same interim utilities
---

A direct mechanism is Bayesian incentive compatible (BIC) when telling the truth is a [Bayes-Nash equilibrium](/bayes-nash-equilibrium/): if the other agents report their true types, no agent can raise its expected utility by a false report, where the expectation is over the others' types under a common prior. The difference from [dominant-strategy incentive compatibility](/dominant-strategy-incentive-compatibility/) (DSIC) is the quantifier on the others: DSIC asks that truth be best against every report of the others, while BIC asks it only on average against truthful others. BIC is the notion behind the [revelation principle](/revelation-principle/) for Bayes-Nash equilibrium, the [AGV mechanism](/agv-mechanism/) and the [Myerson-Satterthwaite theorem](/myerson-satterthwaite-theorem/).

## Definition

There are $n$ agents with [quasilinear utilities](/quasilinear-utility/). Agent $i$ has a private type $v_i$ from a set $V_i$. The types are drawn from a common prior $F$ on $V_1 \times \cdots \times V_n$, which every agent and the designer know. Unless stated otherwise the types are independent, $F = F_1 \times \cdots \times F_n$. A [direct revelation mechanism](/direct-revelation-mechanism/) $(x, p)$ maps reports $b$ to an outcome $x(b)$ and payments $p(b)$, where $p_i$ is paid by agent $i$. Agent $i$ of type $v_i$ who gets outcome $o$ and pays $p_i$ has utility $v_i(o) - p_i$.

The mechanism is BIC if for every agent $i$, every type $v_i$ and every report $b_i \in V_i$,

$$\mathbb{E}_{v_{-i}}\big[v_i(x(v_i, v_{-i})) - p_i(v_i, v_{-i})\big] \ \ge\ \mathbb{E}_{v_{-i}}\big[v_i(x(b_i, v_{-i})) - p_i(b_i, v_{-i})\big],$$

where $v_{-i}$ is drawn from the prior. With continuous types, "every type" may be weakened to "almost every type". With correlated types, the expectation is over $v_{-i}$ conditional on $v_i$, so the belief of the agent depends on its true type and not on its report.

Three stages of knowledge appear in Bayesian mechanism design. Ex ante, no one knows any type. At the interim stage, each agent knows its own type only. Ex post, all types are known. BIC is an interim condition. The matching participation constraint is interim [individual rationality](/individual-rationality/): the left side above is at least 0 for every $v_i$.

**Interim form.** Only the interim quantities matter for BIC. With independent types, write $X_i(b_i) = \mathbb{E}_{v_{-i}}[x(b_i, v_{-i})]$ for the distribution over outcomes that agent $i$ expects from report $b_i$, and $P_i(b_i) = \mathbb{E}_{v_{-i}}[p_i(b_i, v_{-i})]$ for its expected payment. BIC says that $v_i(X_i(v_i)) - P_i(v_i) \ge v_i(X_i(b_i)) - P_i(b_i)$, so it is the DSIC condition for a one-agent mechanism that offers the menu $\{(X_i(b), P_i(b)) : b \in V_i\}$.

**Single-parameter agents.** If each agent has one number $v_i \in [0, h]$, the value of an allocation $x_i \in [0, 1]$ is $v_i x_i$, and the types are independent, then a mechanism is BIC if and only if, for every $i$:

1. the interim allocation $Q_i(v_i) = \mathbb{E}_{v_{-i}}[x_i(v_i, v_{-i})]$ is nondecreasing in $v_i$, and
2. the expected payment is $P_i(v_i) = P_i(0) + v_i Q_i(v_i) - \int_0^{v_i} Q_i(z)\, dz$.

This is Myerson's characterization (1981). It is the expected form of [Myerson's lemma](/myerson-lemma/), which gives the same conditions pointwise in $v_{-i}$ for DSIC. The proof is the same: the two inequalities that compare types $v$ and $v'$ give $(v - v') Q_i(v') \le U_i(v) - U_i(v') \le (v - v') Q_i(v)$, where $U_i$ is the interim utility, and these force monotone $Q_i$ and $U_i(v) = U_i(0) + \int_0^v Q_i$.

## Examples and non-examples

- **Every DSIC mechanism is BIC**, for every prior. The [Vickrey auction](/vickrey-auction/) and the [VCG mechanism](/vcg-mechanism/) are examples. The converse fails, as the next example shows.
- **A BIC mechanism that is not DSIC.** Two bidders have values i.i.d. uniform on $[0, 1]$. The mechanism gives the item to the higher report $r$ and charges it $r/2$. A bidder of value $v$ who reports $r$ while the other tells the truth wins with probability $r$, so its expected utility is $(v - r/2)\, r = v r - r^2/2$. The derivative $v - r$ is zero at $r = v$, so truth is optimal: the mechanism is BIC. It is the direct form of the [first-price auction](/first-price-auction/) in its equilibrium $b(v) = v/2$. It is not DSIC: if the other reports $0.1$, a bidder of value $0.9$ who tells the truth pays $0.45$, and one who reports $0.3$ still wins and pays $0.15$.
- **A non-example.** The same allocation with the payment $r$ (the full report) is not BIC: the expected utility $(v - r)\, r$ is largest at $r = v/2$. This is why bidders shade their bids in a first-price auction.
- **AGV.** The [AGV mechanism](/agv-mechanism/) is efficient and exactly budget balanced and is BIC with independent types, but not DSIC. In its three-agent public project example, a low type gains $5/2$ ex post by a lie when the others report high, yet loses in expectation.
- **BIC depends on the prior.** The mechanism of the second example is not BIC if the values have the distribution $F(r) = r^2$ on $[0, 1]$. A bidder who reports $r$ then wins with probability $r^2$ and expects $(v - r/2)\, r^2$, whose derivative $2 v r - \frac{3}{2} r^2$ is zero at $r = 4v/3$, not at $v$. A DSIC mechanism has no such dependence. A mechanism that is BIC for every prior with full support on finite type sets is DSIC, because a prior can put almost all its weight on any single $v_{-i}$.
- **Correlated types.** With correlated types, the [Cremer-McLean theorem](/cremer-mclean-theorem/) gives BIC mechanisms that extract the full surplus by lotteries on the others' reports. These lotteries make sense only with the agent's conditional belief, which is why the definition conditions on $v_i$.

## Related definitions

- [Dominant-strategy incentive compatibility](/dominant-strategy-incentive-compatibility/): truth is best against every report of the others. DSIC implies BIC for every prior. For single-parameter agents with linear utility and independent types, Gershkov, Goeree, Kushnir, Moldovanu and Shi (2013) show the converse in a weaker sense: every BIC mechanism has a DSIC mechanism with the same interim utilities for all agents and the same expected welfare.
- [Revelation principle](/revelation-principle/): any Bayes-Nash equilibrium of any mechanism can be simulated by a BIC direct mechanism with the same outcomes. So for questions about what can be achieved in Bayes-Nash equilibrium, it is enough to search over BIC direct mechanisms.
- [Individual rationality](/individual-rationality/) and [budget balance](/budget-balance/): the constraints that BIC mechanisms are usually asked to meet as well. The [Myerson-Satterthwaite theorem](/myerson-satterthwaite-theorem/) shows that BIC, interim IR, budget balance and efficiency conflict in bilateral trade.
- [Border's theorem](/border-theorem/): with BIC only the interim allocation $Q_i$ matters, and Border's theorem says which interim allocations come from a real allocation rule. Together they turn the search for an optimal BIC auction into a linear program over interim quantities.
- [Myerson's optimal auction](/myerson-optimal-auction/): the revenue optimal mechanism among BIC and interim IR mechanisms for independent single-parameter agents; it is DSIC as well.
- Epsilon-BIC: a lie may gain at most epsilon in expectation. Learned mechanisms, as in [deep learning for auction design](/differentiable-economics/), and mechanisms built from samples are often only approximately incentive compatible, and the epsilon must be stated with its scale.

## References
