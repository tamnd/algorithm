---
tag: 748HQP
kind: definition
slug: principle-of-optimality
name: Bellman's principle of optimality
aliases:
- principle of optimality
area: techniques/dynamic-programming
level: intro
summary: Every tail of an optimal policy is itself optimal for the corresponding subproblem.
prereqs: [optimal-substructure, cut-and-paste-argument]
see_also: [bellman-equation, bellman-optimality-equation, markov-decision-process, value-iteration, dag-shortest-paths, held-karp-algorithm, memoization, tabulation]
sources:
  - book: isbn:9780486428093
    title: Richard Bellman, Dynamic Programming, Princeton University Press, 1957 (Dover reprint, 2003)
    locator: Chapter III, Section 3 (the statement of the principle of optimality)
  - paper: doi:10.1090/S0002-9904-1954-09848-8
    title: Richard Bellman, The theory of dynamic programming, Bulletin of the American Mathematical Society 60(6), 1954
    locator: pp. 503 to 515
  - book: isbn:9781886529434
    title: Dimitri P. Bertsekas, Dynamic Programming and Optimal Control, Volume I, fourth edition, Athena Scientific, 2017
    locator: Chapter 1, The Dynamic Programming Algorithm
---

Bellman's principle of optimality says that an optimal sequence of decisions has optimal tails: whatever the first state and the first decision, the decisions that follow must be optimal for the state that the first decision leads to. Richard Bellman stated it in his 1957 book *Dynamic Programming* as the source of all the functional equations of the subject. It holds when the state carries all the information that the future depends on and the objective adds up, or combines monotonically, over the stages. In the language of algorithms the same property is [optimal substructure](/optimal-substructure/), and the equation that it gives is the [Bellman equation](/bellman-equation/).

## Definition

Bellman's words, from Chapter III, Section 3 of the 1957 book, are: "An optimal policy has the property that whatever the initial state and initial decision are, the remaining decisions must constitute an optimal policy with regard to the state resulting from the first decision."

### A deterministic multistage process

Fix a number of stages $N \ge 1$ and a set of states $S$. At stage $t \in \{0, \ldots, N-1\}$ in state $s \in S$, a finite nonempty set $D_t(s)$ of decisions is allowed. A decision $d \in D_t(s)$ gives a reward $r_t(s, d) \in \mathbb{R}$ and leads to the state $T_t(s, d)$ at stage $t + 1$.

A *policy from $(s, t)$* is a sequence of decisions $\pi = (d_t, d_{t+1}, \ldots, d_{N-1})$ with $s_t = s$, $d_u \in D_u(s_u)$ and $s_{u+1} = T_u(s_u, d_u)$ for $t \le u < N$. Its return is $R_t(s, \pi) = \sum_{u=t}^{N-1} r_u(s_u, d_u)$. The optimal value is $V_t(s) = \max_\pi R_t(s, \pi)$ over all policies from $(s, t)$, with $V_N(s) = 0$. A policy is *optimal from $(s, t)$* when its return is $V_t(s)$. The maximum exists because the set of policies is finite. For a cost, replace max by min.

The *tail* of $\pi$ is $\pi' = (d_{t+1}, \ldots, d_{N-1})$. It is a policy from $(s_{t+1}, t + 1)$ where $s_{t+1} = T_t(s, d_t)$.

**The principle of optimality.** The process satisfies the principle when, for each stage $t < N - 1$, each state $s$ and each policy $\pi$ that is optimal from $(s, t)$, the tail $\pi'$ is optimal from $(T_t(s, d_t), t + 1)$.

### The principle holds for this process

**Claim.** The process above satisfies the principle of optimality, and for $0 \le t < N$,

$$ V_t(s) = \max_{d \in D_t(s)} \bigl( r_t(s, d) + V_{t+1}(T_t(s, d)) \bigr). \tag{1} $$

**Proof.** Let $\pi = (d_t, \pi')$ be optimal from $(s, t)$ and let $s' = T_t(s, d_t)$. Then $R_t(s, \pi) = r_t(s, d_t) + R_{t+1}(s', \pi')$. Suppose that $\pi'$ is not optimal from $(s', t+1)$. Then some policy $\sigma$ from $(s', t+1)$ has $R_{t+1}(s', \sigma) > R_{t+1}(s', \pi')$. The sequence $(d_t, \sigma)$ is a policy from $(s, t)$, because the decisions allowed after stage $t$ depend only on the state $s'$ and the stage. Its return is $r_t(s, d_t) + R_{t+1}(s', \sigma) > R_t(s, \pi)$, which contradicts that $\pi$ is optimal. So $\pi'$ is optimal, and the principle holds.

For (1), the principle gives $V_t(s) = r_t(s, d_t) + V_{t+1}(s')$ for the first decision $d_t$ of an optimal policy, so $V_t(s)$ is at most the right side of (1). Conversely, for each $d \in D_t(s)$, the decision $d$ followed by an optimal policy from $(T_t(s, d), t+1)$ is a policy from $(s, t)$ with return $r_t(s, d) + V_{t+1}(T_t(s, d))$, so $V_t(s)$ is at least each term of the maximum. ∎

The proof uses two facts about the process, and the principle can fail without either of them.

1. **The state is a sufficient summary.** The decisions, rewards and transitions after stage $t$ depend on the past only through $s_{t+1}$. Without this, the tail $\sigma$ may not be allowed after $d_t$, and the paste fails.
2. **The objective is separable and monotone.** The return is $r_t(s, d_t)$ combined with the return of the tail, by a combination that is strictly increasing in the tail. With a sum this holds. With a combination that is only non-decreasing, such as a maximum, the paste gives no strict gain, and only the weak form holds: *some* optimal policy has optimal tails. Equation (1) still holds in that case.

### The stochastic form

In a [Markov decision process](/markov-decision-process/), the next state is random, with a law that depends only on the current state and decision. A policy is then a rule that picks a decision for each state and stage, and the return is an expectation. The principle reads: if a policy is optimal from $(s, t)$, then from each state $s'$ that it reaches at stage $t + 1$ with positive probability, its rule is optimal from $(s', t + 1)$. The condition "with positive probability" is necessary. On a state that is never reached, an optimal policy can make any decision without changing its expected return. The functional equation becomes the [Bellman optimality equation](/bellman-optimality-equation/), with an expectation over the next state inside the maximum.

## Examples and non-examples

### Example: a layered shortest path

A trip goes from $A$ through one of $B_1, B_2$, then one of $C_1, C_2$, to $D$. The costs are $A B_1 = 2$, $A B_2 = 4$, $B_1 C_1 = 7$, $B_1 C_2 = 3$, $B_2 C_1 = 1$, $B_2 C_2 = 5$, $C_1 D = 3$ and $C_2 D = 6$. The four routes cost $A B_2 C_1 D = 8$, $A B_1 C_2 D = 11$, $A B_1 C_1 D = 12$ and $A B_2 C_2 D = 15$.

Equation (1) with min, from the last stage back, gives $V(C_1) = 3$, $V(C_2) = 6$, $V(B_1) = \min(7 + 3, 3 + 6) = 9$, $V(B_2) = \min(1 + 3, 5 + 6) = 4$ and $V(A) = \min(2 + 9, 4 + 4) = 8$. The optimal route is $A, B_2, C_1, D$. Its tail from $B_2$ costs $1 + 3 = 4 = V(B_2)$, as the principle says. A decision that is best for one stage alone is not enough: the cheapest first edge is $A B_1$, but every route through $B_1$ costs at least 11. This computation is [shortest paths in a DAG](/dag-shortest-paths/), done in reverse topological order.

### Example: allocation of a resource

Split $W$ units of a resource among projects $1, \ldots, N$, where giving $x$ units to project $t$ returns $g_t(x)$. Take the state at stage $t$ to be the number of units left. Then (1) reads $V_t(w) = \max_{0 \le x \le w} (g_t(x) + V_{t+1}(w - x))$ with $V_N = 0$. This is the form of the [knapsack](/knapsack-problem/) recurrences.

### Non-example: the state forgets the history

Find a longest simple path in a graph, with the state "the current vertex". The decisions allowed later depend on the vertices already visited, not only on the current one. In the complete graph on $a, b, c$, the longest simple path from $a$ to $c$ is $a, b, c$. Its tail from $b$ is the single edge $b, c$, but from $b$ the longest simple path to $c$ is $b, a, c$, which reuses $a$. The principle fails for this state. It holds again for the state "the current vertex and the set of visited vertices", and that larger state is what the [Held-Karp algorithm](/held-karp-algorithm/) uses for the traveling salesman problem, with up to $2^n$ times as many states.

### Non-example: the objective is not separable

On the layered graph above, ask for the route whose total cost is closest to 10. The totals are 8, 11, 12 and 15, so the optimal route is $A, B_1, C_2, D$, with total 11. Its tail from $B_1$ costs 9. For the same question asked from $B_1$, "the route to $D$ whose cost is closest to 10", the tail $B_1, C_1, D$ costs exactly 10 and is better. So the tail of the optimal policy is not optimal for its own subproblem. The objective $|c - 10|$ of the total cost $c$ is not a monotone function of the cost of the tail. The fix is again a larger state: with the state "the vertex and the cost so far", the tail problem becomes "closest to 10 minus the cost so far", and the principle holds.

### Non-example of the strict form: a bottleneck objective

Let the cost of a route be its most expensive edge, to be minimized. Take edges $s \to a$ of cost 9, $a \to b$ of cost 1, $a \to b'$ of cost 5, and $b \to t$, $b' \to t$ of cost 1. Both routes from $s$ cost 9, so both are optimal. The tail $a, b', t$ of the route $s, a, b', t$ costs 5, while the best route from $a$ costs 1. The strict principle fails, the weak form holds (the route $s, a, b, t$ has an optimal tail), and the equation $V(x) = \min_{(x, y)} \max(c(x, y), V(y))$ is still correct.

## Related definitions

- **[Optimal substructure](/optimal-substructure/).** The same property, stated for subproblems of an algorithmic problem rather than for tails of a decision sequence. In a DP over a [DAG](/dp-on-dag/), a policy is a path and its tail is a suffix of the path.
- **[Bellman equation](/bellman-equation/) and [Bellman optimality equation](/bellman-optimality-equation/).** The functional equation (1) and its stochastic form. The principle is what makes the equation true for the optimal value.
- **[Value iteration](/value-iteration/).** Solves the Bellman optimality equation of an infinite-horizon problem by repeated application of (1). The [Bellman contraction](/bellman-contraction/) theorem proves that it converges when the future is discounted.
- **[Cut-and-paste argument](/cut-and-paste-argument/).** The proof technique of the claim above: replace a tail that is not optimal with a better one and get a contradiction.
- **[Memoization](/memoization/) and [tabulation](/tabulation/).** The two ways to compute the values $V_t(s)$ from (1), top-down from the start or backward from the last stage.

## References
