---
tag: VKSKJW
kind: theorem
slug: revelation-principle
name: Revelation principle
aliases:
- Myerson revelation principle
area: algorithmic-game-theory/mechanism-design
level: intro
summary: Any outcome reached in a dominant-strategy or Bayes-Nash equilibrium of any mechanism is also reached by a direct mechanism in which truth telling is an equilibrium of the same kind.
prereqs: [direct-revelation-mechanism, dominant-strategy-incentive-compatibility]
see_also: [bayesian-incentive-compatibility, bayes-nash-equilibrium, first-price-auction, english-auction, vickrey-auction, myerson-optimal-auction, gibbard-satterthwaite-theorem, myerson-satterthwaite-theorem]
sources:
  - paper: doi:10.2307/1914083
    title: "Allan Gibbard, Manipulation of voting schemes, a general result, Econometrica 41(4) (1973), 587-601"
    locator: the dominant-strategy form, used to reduce any strategyproof game form to a strategyproof voting rule
  - paper: doi:10.2307/1912346
    title: "Roger B. Myerson, Incentive compatibility and the bargaining problem, Econometrica 47(1) (1979), 61-73"
    locator: the Bayesian form, any Bayesian equilibrium of any mechanism is equivalent to a Bayesian incentive compatible direct mechanism
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), Section 9.4.3 (the revelation principle for dominant strategies) and Section 9.6.1 (the Bayesian revelation principle)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Section 10.2.2 (the revelation principle)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 4 (the revelation principle, and why DSIC direct mechanisms lose nothing)
---

The revelation principle says that a planner who wants a certain outcome in equilibrium may restrict attention to [direct revelation mechanisms](/direct-revelation-mechanism/) in which the agents report their types and tell the truth. Any indirect mechanism, with any messages and any rounds, can be replaced by a direct one that asks for the types and then plays the equilibrium strategies for the agents. The dominant-strategy form is due to Gibbard (1973), and the Bayesian form to Myerson (1979). It is a statement about incentives only: it needs a planner that can commit to the rules, and it says nothing about the cost of computation or communication.

## Statement

Let there be $n$ agents with type sets $V_1, \ldots, V_n$ and [quasilinear utilities](/quasilinear-utility/) $u_i = v_i(o) - p_i$. A mechanism gives each agent a set $M_i$ of messages and has an outcome function $g : M_1 \times \cdots \times M_n \to O \times \mathbb{R}^n$. A strategy of agent $i$ is a map $s_i : V_i \to M_i$.

**Theorem (dominant strategies).** If, in the mechanism $(M, g)$, each $s_i(v_i)$ is a dominant strategy of agent $i$ of type $v_i$, then the direct mechanism $(x, p)(v) = g(s_1(v_1), \ldots, s_n(v_n))$ is [DSIC](/dominant-strategy-incentive-compatibility/), and for every type profile it gives the same outcome and the same payments as the original mechanism in that equilibrium.

**Theorem (Bayesian).** Let the types be drawn from a common prior $F$. If $s = (s_1, \ldots, s_n)$ is a [Bayes-Nash equilibrium](/bayes-nash-equilibrium/) of the mechanism $(M, g)$, then the direct mechanism $g \circ s$ is [BIC](/bayesian-incentive-compatibility/) for $F$, and it gives the same outcome and payments as the original mechanism in that equilibrium, for every type profile.

The same proof works without money, for any preferences over outcomes, and for randomized mechanisms with expected utility.

## In plain words

Suppose people play a game set up by a planner, and each person has a best way to play for each thing they might privately know. The planner can offer a new game: "Tell me what you know, and I will play the old game for you in the way that is best for you." Nobody gains by a false answer to the new question, because a false answer only makes the planner play the old game in a way that the person could already have chosen, and did not choose because it was worse. So the planner may as well ask people directly and expect true answers, as long as the planner keeps the promise to play for them and is able to do it.

## Proof

Dominant strategies. Fix an agent $i$, a true type $v_i$, a report $b_i \in V_i$ and reports $b_{-i}$ of the others. Write $m_{-i} = (s_j(b_j))_{j \ne i}$, the messages that the direct mechanism sends for the others. In the direct mechanism, the truthful report gives agent $i$ the result $g(s_i(v_i), m_{-i})$, and the report $b_i$ gives $g(s_i(b_i), m_{-i})$. The message $s_i(b_i)$ is one of the messages in $M_i$, and $s_i(v_i)$ is a dominant strategy of type $v_i$, so it is at least as good for type $v_i$ as any other message against any messages of the others, in particular against $m_{-i}$. So the truthful report gives agent $i$ a utility at least as large as the report $b_i$. This holds for every $i$, $v_i$, $b_i$ and $b_{-i}$, which is the definition of DSIC. The outcome and the payments at the truthful profile $v$ are $g(s(v))$ by construction.

Bayesian. Fix $i$, $v_i$ and $b_i$, and let the others tell the truth. Then the others' messages are $s_{-i}(v_{-i})$ with $v_{-i}$ drawn from the prior conditional on $v_i$. The expected utility of type $v_i$ in the direct mechanism is $\mathbb{E}_{v_{-i}}[u_i(g(s_i(v_i), s_{-i}(v_{-i})))]$ for the truth, and $\mathbb{E}_{v_{-i}}[u_i(g(s_i(b_i), s_{-i}(v_{-i})))]$ for the report $b_i$. Since $s$ is a Bayes-Nash equilibrium, $s_i(v_i)$ is a best response of type $v_i$ to $s_{-i}$, so the first expectation is at least the second, because $s_i(b_i)$ is one of the possible messages. So truth is a Bayes-Nash equilibrium of the direct mechanism.

## Consequences

- **Design over truthful direct mechanisms.** To find the best mechanism for an objective, such as revenue, it is enough to search over truthful direct mechanisms. Myerson used this to find the revenue-optimal auction ([Myerson's optimal auction](/myerson-optimal-auction/)).
- **Impossibility results cover all mechanisms.** A result that rules out a truthful direct mechanism rules out every mechanism with an equilibrium of that kind. The [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/), the [Myerson-Satterthwaite theorem](/myerson-satterthwaite-theorem/) and the [Green-Laffont theorem](/green-laffont-theorem/) all use this step.
- **The first-price auction has a BIC direct version.** With two bidders and values uniform on $[0, 1]$, bidding half the value is a Bayes-Nash equilibrium of the [first-price auction](/first-price-auction/). Its direct version gives the item to the highest report and charges the winner half its report. A bidder of value $v$ that reports $r$ wins with probability $r$ and pays $r/2$, so its expected utility is $r(v - r/2)$, which is largest at $r = v$, with value $v^2/2$.
- **The English auction has the Vickrey auction as its direct version.** With private values, staying in until the price reaches the value is a dominant strategy of the [English auction](/english-auction/). The direct version asks for the value and simulates the clock, and this is the [Vickrey auction](/vickrey-auction/).

## Tightness

The proof uses each of the following, and the result fails without it.

- **Commitment.** The planner must run $g \circ s$ after it hears the reports. If it can change the rules once it knows the types, as a seller who learns a high value and then raises the price, the agents will not report the truth.
- **Simulation.** The direct mechanism must be able to compute $s_i(b_i)$ for the agent. If the strategies are hard to compute, or the agents act on information that the planner cannot use, the direct version may not exist in a usable form.
- **No claim about computation.** A direct mechanism may need far more communication than the original. In a combinatorial auction with $m$ items, a full report is a number for each of the $2^m$ bundles, while an ascending auction can end after few queries. The direct version can also need hard computations, such as the [winner determination problem](/winner-determination-problem/) solved inside $g \circ s$.
- **Only one equilibrium is kept.** The direct mechanism has the truthful equilibrium, but it may have other equilibria too, with other outcomes. In the Vickrey auction with values $(10, 7, 3)$, the bids $(0, 100, 0)$ form a Nash equilibrium in which bidder 2 wins at price 0: bidder 1 would have to pay 100 to win, and bidders 2 and 3 cannot do better. So the principle gives partial implementation, not full implementation.
- **The type of equilibrium is kept.** A mechanism with only a Bayes-Nash equilibrium gives a BIC direct mechanism, not a DSIC one. The two forms cannot be mixed.

## History

Gibbard (1973) used the dominant-strategy form in the proof of the Gibbard-Satterthwaite theorem: a game form in which every player has a dominant strategy can be turned into a strategyproof voting rule. The Bayesian form was given by Myerson (1979) for bargaining problems and became the standard first step in auction design, starting with Myerson's optimal auction of 1981. Dasgupta, Hammond and Maskin (1979) gave related results on incentive compatibility for general implementation at about the same time.

## References
