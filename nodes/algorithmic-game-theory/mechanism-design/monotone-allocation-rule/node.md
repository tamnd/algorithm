---
tag: 4J60KH
kind: definition
slug: monotone-allocation-rule
name: Monotone allocation rule
aliases:
- implementable allocation rule
area: algorithmic-game-theory/mechanism-design
level: core
summary: "In a single-parameter environment, an allocation rule under which bidding higher never lowers an agent's own allocation. These are exactly the rules that DSIC payments can support."
prereqs: [single-parameter-environment]
see_also: [myerson-lemma, cycle-monotonicity, knapsack-problem, single-minded-bidder-mechanism, truthful-in-expectation, maskin-monotonicity, vickrey-auction, position-auction]
sources:
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 3 (monotone and implementable allocation rules, Myerson's lemma) and Lecture 4 (the greedy knapsack auction)
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the monotonicity condition for incentive compatibility in the single-item model
  - paper: "Aaron Archer and Eva Tardos, Truthful mechanisms for one-parameter agents, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS 2001), 482-491"
    locator: the decreasing work curve condition for agents with private costs
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), the part on single-parameter domains
---

In a [single-parameter environment](/single-parameter-environment/), an allocation rule is *monotone* if an agent who raises its bid, with the other bids fixed, never receives less. Monotone rules are exactly the *implementable* ones: by [Myerson's lemma](/myerson-lemma/) a rule can be paired with payments that make truthful bidding a dominant strategy if and only if it is monotone. This is a condition for one-number types only. When each agent reports a vector, the condition that does the same job is [cycle monotonicity](/cycle-monotonicity/), and plain coordinatewise monotonicity is not enough.

## Definition

Let $X \subseteq \mathbb{R}_{\ge 0}^n$ be the feasible set of a single-parameter environment, and let $x : \mathbb{R}_{\ge 0}^n \to X$ be an allocation rule that maps bids $b$ to allocations. The rule $x$ is **monotone** if for every agent $i$, every profile $b_{-i}$ of the other bids, and all bids $z < z'$,
$$x_i(z, b_{-i}) \le x_i(z', b_{-i}).$$
So the *allocation curve* $z \mapsto x_i(z, b_{-i})$ is nondecreasing for every $i$ and $b_{-i}$. An allocation rule is **implementable** if some payment rule $p$ makes $(x, p)$ [DSIC](/dominant-strategy-incentive-compatibility/). Myerson's lemma says that, on bid sets that are intervals, implementable and monotone are the same.

Two special forms:

- **Win or lose rules.** If $x_i \in \{0, 1\}$, monotonicity says that each agent has a *threshold* $\theta_i(b_{-i})$: the agent wins when it bids above the threshold and loses when it bids below it. The DSIC payment with $p_i(0, b_{-i}) = 0$ is the threshold, paid only by a winner.
- **Cost version.** If agents have private costs per unit of work, as in Archer and Tardos (2001), the condition is reversed: the work $x_i(c_i, c_{-i})$ assigned to agent $i$ must be nonincreasing in its reported cost $c_i$.

For a randomized rule, the condition applies to the expected allocation $\mathbb{E}[x_i(z, b_{-i})]$, and the result is a [truthful in expectation](/truthful-in-expectation/) mechanism.

## Examples and non-examples

A small example: a knapsack auction. The capacity is $W = 10$. Bidders A, B and C have public sizes $5, 5, 10$ and bids $10, 9, z$. The rule is the greedy rule that is analyzed below: sort bidders by bid per unit of size, take the longest prefix of this order that fits, and output this prefix unless one single bidder alone has a larger bid, in which case output that bidder.

- If $z \le 18$, C has density at most $1.8$, so the order is A, B, C (ties broken by name). The prefix is $\{A, B\}$ with value $19$, and no single bid is larger than $19$, so C loses.
- If $18 < z \le 20$, the order is A, C, B. After A, C does not fit, so the prefix is $\{A\}$ with value $10$. The single bid $z > 18$ is larger, so C wins alone.
- If $z > 20$, C comes first and fits, and C wins.

So C loses at every bid up to $18$ and wins at every bid above $18$. The allocation curve of C is a step at $18$, which is monotone, and the DSIC payment of C when it wins is $18$.

More monotone rules:

- **Highest bid wins** one item. The threshold is the highest other bid, which gives the [Vickrey auction](/vickrey-auction/).
- **The $k$ highest bids win** $k$ identical items.
- **Sorted slots.** In a [position auction](/position-auction/), the $j$-th highest bidder gets slot $j$ with click rate $\alpha_j$, where $\alpha_1 \ge \alpha_2 \ge \cdots$. Bidding higher moves an agent to a better slot or keeps it in place.
- **Posted price.** Agent $i$ gets the item if $b_i \ge r$, for a fixed price $r$, as long as supply lasts in a fixed order of agents.
- **Exact welfare maximization.** Any rule that picks $x \in \arg\max_{x \in X} \sum_i b_i x_i$, with a fixed tie-breaking order, is monotone. Proof for 0/1 allocations: if an optimal set $S$ contains $i$ and $i$ raises its bid by $\delta > 0$, the value of $S$ rises by $\delta$, and the value of every set without $i$ stays the same. So every optimal set at the new bids contains $i$. For the [knapsack problem](/knapsack-problem/) this rule is optimal but not polynomial time unless P = NP.
- **The greedy knapsack rule** of the small example is monotone and is a 2-approximation (Roughgarden, Lecture 4). Proof of monotonicity: if $i$ is in the chosen prefix $S$ and raises its bid, $i$ moves earlier in the order, the first $|S|$ positions still hold the set $S$, so the new prefix contains $S$ and its value rose by the raise; the best other single bid did not change, so the prefix still wins. If $i$ won alone, it stays the best single bidder with a larger bid, and either the new prefix contains $i$ or it is no more valuable than the old one. Briest, Krysta and Vöcking (2005) gave a monotone rule with ratio $1 + \varepsilon$ that runs in polynomial time, a monotone version of the [knapsack FPTAS](/knapsack-fptas/).

Non-examples:

- **Second-highest bid wins.** The other bids are $5$ and $4$. An agent who bids $4.5$ is second highest and wins. If it bids $6$, it is highest and loses. Raising the bid loses the item, so no payments make this rule DSIC.
- **Capped rule.** The highest bidder wins only if its bid is at most $10$. A winner with bid $9$ loses when it bids $11$.
- **Most work to the most expensive machine.** In the cost version, a rule that gives all the work to the agent with the highest reported cost is not monotone, because reporting a higher cost brings more work.
- **Multi-parameter rules.** For two items with additive values, a rule can be monotone in each coordinate and still not be implementable. Monotonicity in each coordinate is not the right condition there; see [cycle monotonicity](/cycle-monotonicity/).

## Related definitions

- **[Myerson's lemma](/myerson-lemma/).** Monotone is equivalent to implementable, and the payment is $p_i(b) = b_i x_i(b) - \int_0^{b_i} x_i(z, b_{-i}) \, dz$ when $p_i(0, b_{-i}) = 0$.
- **Weak monotonicity.** The multi-parameter condition $v_i(a) - v_i(b) \ge v_i'(a) - v_i'(b)$ whenever the type $v_i$ gets $a$ and the type $v_i'$ gets $b$. It is necessary for DSIC, and for one-number types it is ordinary monotonicity.
- **[Cycle monotonicity](/cycle-monotonicity/).** The condition for every finite cycle of types, which is necessary and sufficient for implementability in any domain (Rochet 1987).
- **[Maskin monotonicity](/maskin-monotonicity/).** A different notion from social choice theory, about preference orders and Nash implementation. It shares the word only.
- **[Truthful in expectation](/truthful-in-expectation/).** For randomized rules, monotonicity of the expected allocation gives truthfulness in expectation, which is weaker than monotonicity of every outcome of the randomness.

## References
