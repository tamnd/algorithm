---
tag: 501KAB
kind: definition
slug: single-parameter-environment
name: Single-parameter environment
aliases:
- single-parameter domain
- one-parameter agents
area: algorithmic-game-theory/mechanism-design
level: core
summary: "A setting in which each agent's private type is one number, its value per unit of allocation, and outcomes are feasible allocation vectors."
prereqs: [quasilinear-utility, dominant-strategy-incentive-compatibility]
see_also: [monotone-allocation-rule, myerson-lemma, cycle-monotonicity, position-auction, vickrey-auction, knapsack-problem, uniform-machine-scheduling, myerson-optimal-auction]
sources:
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 3 (single-parameter environments and Myerson's lemma) and Lecture 4 (knapsack auctions)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), the part on single-parameter domains
  - paper: "Aaron Archer and Eva Tardos, Truthful mechanisms for one-parameter agents, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS 2001), 482-491"
    locator: the one-parameter model with private cost per unit of load, and the monotonicity characterization
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the single-item model with one private value per bidder
---

In a single-parameter environment each agent's private information is one number $v_i$, its value for one unit of allocation, and the agent's value for an outcome is $v_i$ times the amount it receives. The mechanism chooses an allocation vector from a fixed feasible set and charges payments. This is the setting where truthful mechanisms are completely understood: by [Myerson's lemma](/myerson-lemma/) an allocation rule can be made truthful if and only if it is [monotone](/monotone-allocation-rule/), and then the payments are fixed. When an agent's type is a vector of several numbers, the environment is multi-parameter, and the right condition is [cycle monotonicity](/cycle-monotonicity/) instead.

## Definition

There are $n$ agents and a set $X \subseteq \mathbb{R}_{\ge 0}^n$ of *feasible allocations*. The set $X$ is public. Each agent $i$ has a private *value per unit* $v_i \ge 0$, its type. If the mechanism chooses $x \in X$ and charges agent $i$ the amount $p_i$, the agent's utility is
$$u_i = v_i x_i - p_i,$$
which is [quasilinear](/quasilinear-utility/) with the valuation $o \mapsto v_i x_i(o)$.

A direct mechanism asks each agent for a bid $b_i \ge 0$ and returns an allocation rule $x(b) \in X$ and a payment rule $p(b) \in \mathbb{R}^n$. In the general language of the area, the outcome set is $O = X$, and agent $i$'s valuation is the function $v_i(x) = v_i \cdot x_i$. So the type set of agent $i$ is not all of $\mathbb{R}^O$ but the half-line $\{t \cdot e_i : t \ge 0\}$ of valuations that depend only on coordinate $i$ and scale with one number. That is the meaning of *single-parameter*.

Two common variants:

- **Cost version.** Agents are service providers. Agent $i$ has a private cost $c_i \ge 0$ per unit of work, the mechanism assigns work $x_i$ and pays the agent the amount $q_i$, and the utility is $q_i - c_i x_i$. In the convention of this area $p_i = -q_i$ and the value per unit is $-c_i$. Archer and Tardos (2001) call these agents *one-parameter agents*.
- **Randomized mechanisms.** If $x(b)$ is random, the relevant quantity is the expected allocation $\mathbb{E}[x_i(b)]$. Then $x_i$ is a probability or an expected amount, and the same theory applies to expectations. See [truthful in expectation](/truthful-in-expectation/).

## Examples and non-examples

A small example. A search page has two ad slots. Slot 1 gets 2 clicks per hour and slot 2 gets 1 click. Three advertisers have values per click $v = (10, 7, 3)$. A feasible allocation gives each advertiser the number of clicks of its slot, so $X$ is the set of vectors with entries $2, 1, 0$ in some order, for example $x = (2, 1, 0)$. Advertiser 1 has value $10 \cdot 2 = 20$ for this outcome, and advertiser 2 has value $7 \cdot 1 = 7$. The value for any outcome is the advertiser's one number times its clicks, so this is a single-parameter environment.

More examples:

- **Single item.** $X = \{x \in \{0,1\}^n : \sum_i x_i \le 1\}$. The [Vickrey auction](/vickrey-auction/) and [Myerson's optimal auction](/myerson-optimal-auction/) live here.
- **$k$ identical items, unit demand.** $X = \{x \in \{0,1\}^n : \sum_i x_i \le k\}$.
- **Position auctions.** As in the small example above, with slot click rates $\alpha_1 \ge \alpha_2 \ge \dots \ge \alpha_k$. See [position auction](/position-auction/).
- **Knapsack auctions.** Agent $i$ has a public size $w_i$, and $X = \{x \in \{0,1\}^n : \sum_i w_i x_i \le W\}$ for a capacity $W$. Choosing the welfare-maximizing allocation is the [knapsack problem](/knapsack-problem/).
- **Single-minded bidders with known bundles.** In a [combinatorial auction](/combinatorial-auction/) each bidder wants one public bundle and has a private value for it. The value is one number, so the setting is single-parameter. If the bundle is private too, the type has two parts, but a similar monotonicity theory still works; see [single-minded bidder mechanism](/single-minded-bidder-mechanism/).
- **Related machines.** Machine $i$ has a private cost $c_i$ per unit of processing, and jobs have public sizes. The amount $x_i$ is the total size of the jobs on machine $i$. This is the cost version, studied by Archer and Tardos (2001); see [uniform machine scheduling](/uniform-machine-scheduling/).
- **Public project.** $X = \{(0, \dots, 0), (1, \dots, 1)\}$: the project is built for all or for nobody, and $v_i$ is agent $i$'s value for it.

Non-examples:

- **Two items with additive values.** A bidder has a value $a_i$ for item A and $b_i$ for item B. The type is the pair $(a_i, b_i)$, which is two numbers.
- **Unrelated machines.** Machine $i$ has a separate private time $t_{ij}$ for each job $j$. The type is a vector of $m$ numbers. This is the [truthful scheduling problem on unrelated machines](/truthful-scheduling-unrelated-machines/).
- **General combinatorial auctions.** A bidder has a value for each bundle, which is $2^m - 1$ numbers.
- **Values with externalities.** If a bidder's value depends on which other bidder wins, the value is not a single number times $x_i$.
- **Budgets.** A bidder with a private value and a private budget has a two-dimensional type, and its utility is not quasilinear above the budget.

## Related definitions

- **[Monotone allocation rule](/monotone-allocation-rule/).** An allocation rule is monotone if $x_i(b_i, b_{-i})$ does not decrease when $b_i$ increases. In single-parameter environments this is exactly the condition for truthfulness.
- **[Myerson's lemma](/myerson-lemma/).** The theorem that makes the characterization precise and gives the unique payment formula $p_i(b) = b_i x_i(b) - \int_0^{b_i} x_i(z, b_{-i}) \, dz$.
- **[Cycle monotonicity](/cycle-monotonicity/).** The condition that replaces monotonicity when types are vectors. In a single-parameter environment it reduces to ordinary monotonicity.
- **[Roberts' theorem](/roberts-theorem/).** On the unrestricted multi-parameter domain, the truthful rules are only the [affine maximizers](/affine-maximizer/). A single-parameter environment is a very restricted domain, so Roberts' theorem does not apply, and many more rules are truthful, for example any monotone approximation algorithm.
- **Bayesian single-parameter setting.** If each $v_i$ is drawn from a known distribution $F_i$, the same environment is the setting of [revenue equivalence](/revenue-equivalence-theorem/), [virtual valuations](/virtual-valuation/) and the [optimal auction](/myerson-optimal-auction/).
- **[DSIC](/dominant-strategy-incentive-compatibility/).** The truthfulness notion used throughout: truthful bidding maximizes $v_i x_i(b) - p_i(b)$ for every $b_{-i}$.

## References
