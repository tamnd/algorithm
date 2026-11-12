---
tag: F8X6BC
kind: model
slug: pomdp
name: Partially observable Markov decision process
aliases:
- POMDP
- partially observable MDP
area: machine-learning/reinforcement-learning
level: advanced
summary: "An MDP in which the agent sees only noisy observations of the state. The belief, a posterior over states, is a sufficient statistic, and the finite horizon value is convex and piecewise linear in it."
prereqs: [markov-decision-process, bayes-theorem]
see_also: [pomdp-planning, point-based-value-iteration, belief-space, hidden-markov-model, bayes-theorem, markov-game, bellman-optimality-equation, state-value-function]
sources:
  - paper: doi:10.1016/0022-247X(65)90154-X
    title: K. J. Astrom, Optimal Control of Markov Processes with Incomplete State Information, Journal of Mathematical Analysis and Applications 10(1), 174-205, 1965
    locator: "the conditional state distribution as a sufficient statistic"
  - paper: doi:10.1287/opre.21.5.1071
    title: Richard D. Smallwood and Edward J. Sondik, The Optimal Control of Partially Observable Markov Processes over a Finite Horizon, Operations Research 21(5), 1071-1088, 1973
    locator: "the piecewise linear convex value function and its algorithm"
  - paper: doi:10.1016/S0004-3702(98)00023-X
    title: Leslie Pack Kaelbling, Michael L. Littman and Anthony R. Cassandra, Planning and Acting in Partially Observable Stochastic Domains, Artificial Intelligence 101(1-2), 99-134, 1998
    locator: "the belief MDP, value functions as sets of vectors, the witness algorithm, the tiger problem"
  - paper: doi:10.1287/mnsc.28.1.1
    title: George E. Monahan, A Survey of Partially Observable Markov Decision Processes, Theory, Models, and Algorithms, Management Science 28(1), 1-16, 1982
    locator: "the enumeration algorithm"
  - paper: doi:10.1287/moor.12.3.441
    title: Christos H. Papadimitriou and John N. Tsitsiklis, The Complexity of Markov Decision Processes, Mathematics of Operations Research 12(3), 441-450, 1987
    locator: "P-completeness for MDPs, PSPACE-completeness for finite horizon POMDPs"
  - paper: doi:10.1016/S0004-3702(02)00378-8
    title: Omid Madani, Steve Hanks and Anne Condon, On the Undecidability of Probabilistic Planning and Related Stochastic Optimization Problems, Artificial Intelligence 147(1-2), 5-34, 2003
    locator: "undecidability for infinite and indefinite horizons"
---

A partially observable Markov decision process (POMDP) is a [Markov decision process](/markov-decision-process/) in which the agent does not see the state. After each action it gets an observation whose law depends on the new state. The agent can still act optimally with a function of its belief, the posterior distribution of the state given everything it has seen. With this, a POMDP becomes an MDP on the continuous space of beliefs, but optimal planning becomes much harder.

## The machine

A finite POMDP is a tuple $(S, A, P, R, \Omega, O, \gamma)$:

- $S$, $A$ and $\Omega$ are finite sets of states, actions and observations.
- $P(s' \mid s, a)$ is the transition law and $R(s, a)$ the expected reward, as in an MDP.
- $O(o \mid a, s')$ is the probability of the observation $o$ when the action $a$ led to the state $s'$.
- $0 \le \gamma \le 1$ is the discount, with $\gamma < 1$ for an infinite horizon.

The run: $S_0$ is drawn from an initial distribution $b_0$ that the agent knows. At step $t$ the agent picks $A_t$ from its history $h_t = (A_0, O_1, \dots, A_{t-1}, O_t)$, gets the reward $R_{t+1}$, the state moves to $S_{t+1} \sim P(\cdot \mid S_t, A_t)$, and the agent sees $O_{t+1} \sim O(\cdot \mid A_t, S_{t+1})$. The state and the rewards are hidden in the model, so a policy may depend on actions and observations only. The aim is to maximize $\mathbb{E}\left[\sum_t \gamma^t R_{t+1}\right]$.

**The belief update.** The belief is $b_t(s) = \Pr(S_t = s \mid h_t)$. After the action $a$ and the observation $o$, Bayes' rule gives

$$b'(s') = \frac{O(o \mid a, s') \sum_s P(s' \mid s, a)\, b(s)}{\Pr(o \mid b, a)}, \qquad \Pr(o \mid b, a) = \sum_{s'} O(o \mid a, s') \sum_s P(s' \mid s, a)\, b(s).$$

*Proof.* By the Markov property of the hidden chain and the observation model, $\Pr(S_{t+1} = s', O_{t+1} = o \mid h_t, A_t = a) = O(o \mid a, s') \sum_s P(s' \mid s, a) b_t(s)$, because given $S_t$ the next state and the observation do not depend on the earlier history, and the action is a function of $h_t$ and outside randomness only. Divide by the sum over $s'$. $\blacksquare$

The update costs $O(|S|^2)$ operations. It is the forward step of a [hidden Markov model](/hidden-markov-model/) filter, with the transition matrix picked by the action.

**The belief MDP.** The belief is a sufficient statistic (Astrom 1965): the expected reward of an action is $\rho(b, a) = \sum_s b(s) R(s, a)$, and the law of the next belief depends only on $(b, a)$. So the POMDP is an MDP whose states are the points of the probability simplex $\Delta(S)$, with a transition to $b^{a,o}$ with probability $\Pr(o \mid b, a)$. Its optimality equation is

$$V^*(b) = \max_a \left[\rho(b, a) + \gamma \sum_o \Pr(o \mid b, a)\, V^*(b^{a,o})\right].$$

For $\gamma < 1$ the right side is a $\gamma$-contraction in the max norm, as for a finite MDP ([Bellman contraction](/bellman-contraction/)), so the equation has one bounded solution. An optimal policy maps beliefs to actions.

## What it counts

The usual costs are the number of arithmetic operations, as a function of $|S|$, $|A|$, $|\Omega|$ and the horizon $H$, and the size of the value function, counted as a number of vectors in $\mathbb{R}^{|S|}$.

**Piecewise linear and convex value** (Smallwood and Sondik 1973). For each finite horizon $H$ there is a finite set $\Gamma_H \subset \mathbb{R}^{S}$ with

$$V_H(b) = \max_{\alpha \in \Gamma_H} \sum_s \alpha(s)\, b(s).$$

*Proof by induction.* $\Gamma_0 = \{0\}$. Suppose it holds for $H - 1$. In the recursion, $\Pr(o \mid b, a) V_{H-1}(b^{a,o}) = \max_{\alpha \in \Gamma_{H-1}} \sum_{s'} \alpha(s') O(o \mid a, s') \sum_s P(s' \mid s, a) b(s)$, because the normalizer cancels. This is a max of linear functions of $b$. Write $g_{a,o,\alpha}(s) = \sum_{s'} P(s' \mid s, a) O(o \mid a, s') \alpha(s')$. A sum over $o$ of maxima is the max over all choices $(\alpha_o)_{o \in \Omega}$ of the sum. So

$$\Gamma_H = \left\{ R(\cdot, a) + \gamma \sum_o g_{a,o,\alpha_o} \;:\; a \in A,\ \alpha_o \in \Gamma_{H-1} \text{ for each } o \right\}$$

works, and a max of linear functions is convex. $\blacksquare$

Each vector, an alpha vector, is the value of a conditional plan: a first action, then a plan of depth $H-1$ for each observation. Enumeration (Monahan 1982) builds $|\Gamma_H| = |A|\,|\Gamma_{H-1}|^{|\Omega|}$ vectors with no pruning, which grows doubly exponentially in $H$. Exact algorithms prune vectors that are never the max. Kaelbling, Littman and Cassandra describe the witness algorithm. The pruned set can still grow exponentially.

## Relation to other models

- **MDP.** If $\Omega = S$ and $O(o \mid a, s') = [o = s']$, the belief is a point mass and the POMDP is an MDP.
- **Hidden Markov model.** With one action and no rewards, a POMDP is a [hidden Markov model](/hidden-markov-model/), and the belief update is the forward filter.
- **Belief-space planning.** [POMDP planning](/pomdp-planning/), [point-based value iteration](/point-based-value-iteration/) and [belief-space](/belief-space/) methods in the planning area work on the belief MDP. Point-based methods keep alpha vectors only for a finite set of sampled beliefs.
- **Markov games.** A [Markov game](/markov-game/) adds players but keeps the state visible. Games with hidden state are partially observable stochastic games, which are harder still.
- **Reinforcement learning.** When $P$, $O$ and $R$ are unknown, a learner cannot form the belief. Common workarounds keep a window of past observations or a recurrent summary of the history.

## Known results in the model

Take the tiger problem of Kaelbling, Littman and Cassandra (1998). A tiger is behind the left or the right door, each with probability 1/2. *Listen* costs 1 and tells the correct side with probability 0.85. Opening the door without the tiger gives 10, opening the tiger door gives $-100$, and both reset the tiger at random.

- **Belief updates.** After one "left", $b(\text{left}) = 0.85$. After two, $b(\text{left}) = \frac{0.85^2}{0.85^2 + 0.15^2} = \frac{289}{298} \approx 0.970$. A "right" after that brings it back to 0.85, since the two observations cancel.
- **Value.** Without discount, $V_1(1/2) = -1$ (listen; opening gives $-45$), $V_2(1/2) = -2$ and $V_3(1/2) = 68/25 = 2.72$. The best 3-step plan listens twice and opens the door opposite the sound if both sounds agree, which gives $\frac{1990}{298} \approx 6.68$ in expectation at the belief $289/298$.
- **Vector counts.** Enumeration gives $|\Gamma_1| = 3$, $|\Gamma_2| = 3 \cdot 3^2 = 27$ and $|\Gamma_3| = 3 \cdot 27^2 = 2187$ vectors, and the max over them equals the recursive value at every belief.

General results:

- **Sufficient statistic** (Astrom 1965). Optimal control with incomplete information reduces to control of the conditional state distribution.
- **Finite horizon** (Smallwood and Sondik 1973). $V_H$ is piecewise linear and convex, and an exact algorithm computes it.
- **Complexity** (Papadimitriou and Tsitsiklis 1987). Deciding whether a finite horizon POMDP has a policy with expected cost at most a threshold is PSPACE-complete, for a horizon bounded by a polynomial in the input size. For a fully observed MDP the same question is P-complete.
- **Undecidability** (Madani, Hanks and Condon 2003). For infinite or indefinite horizons, several questions are undecidable, such as whether some policy reaches a goal state with probability above a threshold.
- **Approximation.** Because $V^*$ is convex, it can be approximated from below by a finite set of alpha vectors. Point-based methods choose these vectors at sampled beliefs.

## References
