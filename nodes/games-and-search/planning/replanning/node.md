---
tag: S4BFGJ
kind: problem
slug: replanning
name: Replanning
aliases:
- plan repair
- online replanning
area: games-and-search/planning
level: core
summary: When a plan stops working during execution, find a new plan from the current state, either from scratch or by repairing the old one, often in a simpler model than the real world.
prereqs: [classical-planning, execution-monitoring]
see_also: [d-star-lite, lifelong-planning-a-star, fast-forward-planner, stochastic-shortest-path, real-time-dynamic-programming, contingent-planning, strips-plan-existence-pspace-complete, online-algorithm]
sources:
  - paper: doi:10.1016/0004-3702(94)00082-C
    title: Bernhard Nebel and Jana Koehler, Plan reuse versus plan generation, a theoretical and empirical analysis, Artificial Intelligence 76(1-2), 1995
    locator: pp. 427 to 454 (plan modification is not easier than plan generation in the worst case, and conservative modification can be harder)
  - paper: "Maria Fox, Alfonso Gerevini, Derek Long and Ivan Serina, Plan stability, replanning versus plan repair, Proceedings of ICAPS 2006"
    locator: pp. 212 to 221 (the distance between plans as a measure of stability, and repair with LPG against planning from scratch)
  - paper: "Sungwook Yoon, Alan Fern and Robert Givan, FF-Replan, a baseline for probabilistic planning, Proceedings of ICAPS 2007"
    locator: pp. 352 to 359 (single-outcome and all-outcomes determinization, planning with FF, and replanning on an unexpected state)
  - book: isbn:9781107037274
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning and Acting, Cambridge University Press, 2016
    locator: whole book (planning and acting with online replanning, general locator)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11 (planning and acting in nondeterministic domains, online replanning)
---

Replanning is the problem of finding a new plan while a plan runs, when the state that the agent observes is not the state that the plan expects, or when the model of the world has changed. The agent has a plan, a goal and the current state. It can plan from scratch from the current state, or it can **repair** the old plan, keeping as much of it as it can. Replanning is also a strategy for acting in uncertain worlds: plan in a simple deterministic model, act, observe, and plan again when the world does not follow the model. FF-Replan (Yoon, Fern and Givan 2007) does this for probabilistic domains, and the incremental searches [D* Lite](/d-star-lite/) and [LPA*](/lifelong-planning-a-star/) do it for paths in graphs whose edge costs change. An [execution monitor](/execution-monitoring/) decides when a replan is needed.

## In plain words

You drive to work along your usual route, and the radio says that a bridge is closed. You do not go home and start again. You find a new way from where you are, and you try to keep most of your old route.

A replanning agent works the same way. It makes a plan, starts to follow it, and watches what happens. When something goes wrong, it makes a new plan from the place where it is now. It can plan in a simpler world than the real one, for example a world where each action always has its most common result. This is fast, and it works well when surprises are rare and can be fixed. It can fail badly when one bad surprise ends all hope, because the simple world does not show the danger.

## Definition

A **replanning instance** is a planning problem with extra data. It has a domain with states $S$, actions $A$ and a goal $G$, a current state $s$, and an old plan $\pi = a_0, \ldots, a_{n-1}$ that was made for an expected state $s_e \ne s$, or for an older domain. The task is to output a plan $\pi'$ that reaches $G$ from $s$ in the current domain, or to report that none exists. Two versions differ in what they ask of $\pi'$.

- **Replanning from scratch.** Any valid plan, often a shortest one. The old plan is ignored, so this is the [classical planning](/classical-planning/) problem again.
- **Plan repair.** A valid plan that is close to $\pi$. A common measure is the **plan distance** of Fox, Gerevini, Long and Serina (2006): the number of actions that are in $\pi$ and not in $\pi'$, plus the number that are in $\pi'$ and not in $\pi$. A plan is **stable** if its distance to the old plan is small. Repair can also ask to keep a given part of $\pi$, which Nebel and Koehler (1995) call conservative plan modification.

**Online replanning** is the loop that uses these steps to act. With a domain $D$ and a simpler model $\hat D$ used for planning:

1. Plan in $\hat D$ from the current state.
2. Do the first action, and observe the next state.
3. If the state is the one that the plan expects, go on with the plan. If not, go back to step 1.

The quality of the loop is measured in $D$: the probability of reaching $G$, and the expected cost or number of steps. For a [stochastic shortest path](/stochastic-shortest-path/) problem, the best possible values are those of an optimal policy.

## Variants

- **Changing graphs.** The domain is a graph whose edge costs change, as when a robot finds new obstacles. Incremental searches reuse the old search tree: [D*](/d-star/), [LPA*](/lifelong-planning-a-star/) and [D* Lite](/d-star-lite/).
- **Determinization.** For probabilistic domains, the planning model $\hat D$ keeps one outcome of each action (single-outcome, for example the most likely one) or makes each outcome a separate deterministic action (all-outcomes). FF-Replan plans in $\hat D$ with the [FF planner](/fast-forward-planner/).
- **Sampling futures.** Hindsight optimization and related methods plan in several sampled deterministic futures and choose the action that is good in most of them, which takes the probabilities into account.
- **Contingency on demand.** Plan a sequence for the expected case, and add branches only for the outcomes that turn up during execution, which lies between replanning and [contingent planning](/contingent-planning/).
- **Repair with a time limit.** The agent must act at a fixed rate, so the planner returns the best plan it has by the deadline, as in [real-time search](/real-time-a-star/) and [RTDP](/real-time-dynamic-programming/).

## Examples

**A risky shortcut.** From the start, the action risky reaches the goal with probability $3/5$ and a dead end with probability $2/5$. The action safe reaches a middle state, from which safe reaches the goal surely. Both determinizations give the one-step plan risky, so the replanning agent reaches the goal with probability $3/5$. The optimal policy uses safe twice and reaches the goal with probability $1$. The determinized model has no costs for danger, so it cannot see the dead end. With probability $p$ in place of $3/5$, the loss is $1 - p$, as large as we like.

**A slippery corridor.** States $0$ to $4$ in a row, and the action right moves one cell with probability $1/2$ and stays with probability $1/2$. The agent replans after each slip, with the same action as before. It reaches the goal with probability 1 and expected $8 = 4 / (1/2)$ steps, which is optimal.

**A lucky action.** The action try reaches the goal with probability $1/10$ and stays with probability $9/10$. The most likely outcome is to stay, so the single-outcome model has no plan, and the agent gives up. The all-outcomes model has the one-step plan try, and the agent reaches the goal in expected $10$ steps.

**Repair against scratch.** On a 5 by 5 grid with a wall at $x = 2$ for $y = 1, 2, 3$, the old plan from $(0, 0)$ to $(4, 4)$ goes east 4 times and north 4 times. After two steps the agent is pushed from $(2, 0)$ to $(1, 1)$. Repair by reconnection goes south, east, and joins the old plan: 8 steps, at distance 2 from the rest of the old plan. A shortest plan from scratch goes north 3 times and east 3 times: 6 steps, but at distance 12, because it shares no ground action with the old plan.

The implementation computes the success probabilities and expected steps of the replanning agent exactly, with fractions, over the Markov chain of states and plans in memory. It checks them against the best policy found by enumeration, and checks that with no dead end in the all-outcomes model the agent reaches the goal with probability 1.

## Known algorithms

- **Plan from scratch.** Run a planner from the current state. With a fast planner this is often the best choice in practice.
- **FF-Replan.** Determinize, plan with FF, follow the plan while the observed states are the expected ones, and plan again otherwise. With all-outcomes determinization and a plan in that model from every state, the agent reaches the goal with probability 1, because from every state some sequence of outcomes of positive probability leads to the goal.
- **Repair by reconnection.** Search from the current state for the nearest state from which a suffix of the old plan works, and append the suffix. The kernels of a triangle table, as in [execution monitoring](/execution-monitoring/), give the states from which each suffix works.
- **Local search repair.** LPG repairs a plan by local search on the plan graph, with a cost that counts the changes to the old plan (Fox et al. 2006).
- **Plan-space repair.** Remove the steps that no longer work, keep the [causal links](/causal-link/) that still hold, and refine the partial plan, as in [plan-space planning](/plan-space-planning/).
- **Incremental search.** D* Lite and LPA* keep the $g$ values and the priority queue of the last search, and update only the states whose values change.

## Bounds

- **Not easier than planning.** Nebel and Koehler (1995) show that, in the worst case, modifying a given plan is not easier than generating a plan from scratch. For STRIPS this is [PSPACE-complete](/strips-plan-existence-pspace-complete/). They also show that conservative modification, which must keep as much of the old plan as possible, can be harder than generation. So no repair method has a provable worst-case gain over replanning from scratch.
- **Cost of the loop.** The loop calls the planner at most once per step. With no surprises, it calls it once.
- **Loss of determinization.** The ratio of the success probability of the loop to that of the best policy has no positive lower bound. In the risky shortcut example it is $p$ against $1$, for any $p > 0$. With all-outcomes determinization and no dead ends in that model, the success probability is $1$, but the expected cost can still be far from optimal.

## Reductions

- **From classical planning.** Take an empty old plan. Replanning from scratch is classical planning, and repair with no plan to keep is classical planning.
- **To classical planning with costs.** A simple encoding that favors stable plans gives the actions of the old plan a lower cost than the other actions, and asks for a cheapest plan. It favors reuse, but it does not minimize the plan distance exactly, because it does not count the old actions that the new plan leaves out.
- **To stochastic shortest paths.** Online replanning with a determinization defines a policy, with memory, for a [stochastic shortest path](/stochastic-shortest-path/) problem. Its expected cost is at least the optimal value, and equal to it in some domains, such as the slippery corridor.
- **To incremental search.** For path planning with edge cost changes, replanning is the dynamic single-source shortest path problem.

## Applications

- Mobile robots and planetary rovers, which replan their paths as their sensors find new obstacles.
- Logistics and air traffic, where a schedule is repaired after a delay, and a stable repair is cheaper for the people who follow it than a new schedule.
- Video game characters, which replan a few times a second as the world changes.
- Probabilistic planning, where FF-Replan was a strong baseline in the International Probabilistic Planning Competitions.
- Mixed-initiative planning, where a human changes the goal and the planner adapts the current plan.

## References
