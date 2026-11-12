---
tag: P4J42D
kind: algorithm
slug: dueling-network
name: Dueling network architecture
aliases:
- dueling DQN
- dueling Q-network
area: machine-learning/reinforcement-learning
level: advanced
summary: "A Q-network with a shared body and two heads, a state value V and advantages A, joined as Q = V + A - mean A so that V and A are identifiable; trained like DQN."
solves: [rl-control]
model: real-ram
complexity:
  vars: {W: the cost of the shared layers, H: the width of the last shared layer, M: the number of actions}
  time: {worst: "O(W + H M)"}
  space: {extra: "O(W + H M)"}
properties: {deterministic: true, online: true, exact: false, recursive: false}
history:
  year: 2016
  people: [Ziyu Wang, Tom Schaul, Matteo Hessel, Hado van Hasselt, Marc Lanctot, Nando de Freitas]
  note: "Wang and coauthors introduced the dueling architecture at ICML 2016, with the mean aggregation and Double DQN training."
prereqs: [dqn, advantage-function]
see_also: [double-dqn, prioritized-experience-replay, experience-replay, q-learning, value-function-approximation, actor-critic]
sources:
  - paper: "Ziyu Wang, Tom Schaul, Matteo Hessel, Hado van Hasselt, Marc Lanctot and Nando de Freitas, Dueling network architectures for deep reinforcement learning, Proceedings of the 33rd International Conference on Machine Learning (ICML), PMLR 48, 2016, pages 1995 to 2003, arXiv:1511.06581"
    locator: Section 3 (equation 7, the naive sum, and its lack of identifiability; equation 8, the max aggregation; equation 9, the mean aggregation), Section 4 (the corridor experiment and Atari results)
  - paper: "Leemon C. Baird III, Advantage updating, Technical Report WL-TR-93-1146, Wright Laboratory, Wright-Patterson Air Force Base, 1993"
    locator: the separate learning of a state value and advantages
  - paper: doi:10.1038/nature14236
    title: "Volodymyr Mnih and others, Human-level control through deep reinforcement learning, Nature 518(7540), 2015, pages 529 to 533"
    locator: the DQN network and training loop that the dueling network plugs into
  - paper: "Hado van Hasselt, Arthur Guez and David Silver, Deep reinforcement learning with double Q-learning, AAAI 2016, arXiv:1509.06461"
    locator: the Double DQN target used to train the dueling network
---

The dueling network architecture (Wang, Schaul, Hessel, van Hasselt, Lanctot and de Freitas, 2016) is a way to build the Q-network of [DQN](/dqn/). The shared layers compute a feature vector $z$ of the state. Two small heads then compute a scalar *state value* $V(s)$ and a vector of *advantages* $A(s, a)$, one per action, and a fixed aggregation layer joins them:

$$Q(s, a) = V(s) + \Big(A(s, a) - \frac{1}{M} \sum_{b} A(s, b)\Big).$$

The network outputs Q-values, so it trains with any Q-learning target, in the paper with [Double DQN](/double-dqn/). The gain is in what the network can learn fast: the value head gets a gradient from every sample, whatever action the sample has, so the value of a state is learned once for all actions.

## In plain words

In many situations it does not matter much what you do. A car on an empty road can steer a little left or right with no effect. What matters is how good the situation is. A standard Q-network must learn the value of each action on its own. A dueling network learns two things: how good the situation is (one number), and how much better or worse each action is than the others (one number per action). It adds them to get the action values.

Every sample teaches the first part. So the network learns the situation value quickly, and only the small differences between actions need samples of each action.

## The problem

The task is that of [DQN](/dqn/): [reinforcement learning control](/rl-control/) with a finite action set of size $M$ and a parametric $Q(s, a; \theta)$. The dueling network does not change the algorithm; it changes the function class. The design question is how to split $Q$ into a state part and an action part so that the split is unique.

The [advantage function](/advantage-function/) of a policy is $A^\pi(s, a) = Q^\pi(s, a) - V^\pi(s)$, and it has $\sum_a \pi(a \mid s) A^\pi(s, a) = 0$. For the greedy optimal policy, $\max_a A^*(s, a) = 0$. The naive sum $Q = V + A$ (equation 7 of the paper) does not use these facts, and it is not identifiable: $V + c$ and $A - c$ give the same $Q$ for every constant $c$, so the heads have no reason to learn a value and an advantage. The aggregation layer adds a constraint that fixes $c$.

## The algorithm

The forward pass for one state. $f$ is the shared body, $V$ and $A$ the two heads, with parameters $\theta$, $\beta$ and $\alpha$.

```pseudo id=main
DUELING-Q(s, θ, β, α, kind)
L1  z ← f(s; θ)                                   ▷ shared features
L2  v ← V(z; β)                                   ▷ value head, one number
L3  adv[a] ← A(z, a; α) for each action a          ▷ advantage head, M numbers
L4  c ← (1/M) Σ_b adv[b] if kind = mean, else max_b adv[b]
L5  Q[a] ← v + adv[a] − c for each action a
L6  return Q
```

**Training.** The output feeds the [DQN](/dqn/) loop unchanged. The paper uses the [Double DQN](/double-dqn/) target with uniform replay, and also with [prioritized replay](/prioritized-experience-replay/). The gradient flows back through line L5 into both heads: $\partial Q[a] / \partial v = 1$ and $\partial Q[a] / \partial \text{adv}[b] = [a = b] - w_b$, where $w_b = 1/M$ for the mean and $w$ is the one-hot vector of the argmax for the max. Two small changes come with it in the paper: the gradient entering the last shared layer is multiplied by $1/\sqrt{2}$, because two heads send gradient back into it, and the gradient norm is clipped to at most 10.

**Choosing the aggregation.** With the max (equation 8 of the paper), the greedy action has $Q = v$, so $v$ estimates $V^*$ and $\text{adv} - \max \text{adv}$ estimates $A^*$. With the mean (equation 9), $v$ is the mean of the Q-values over actions, so the heads are off from $V^*$ and $A^*$ by a constant. The paper uses the mean in its experiments: the advantages then need to move only as fast as their mean, not as fast as their maximum, which changes when the best action changes, so learning is more stable.

## Example

**One state, both aggregations.** On the 6-state chain of the [DQN](/dqn/) page with $\gamma = 0.9$, state 3 has $Q^*(3, \text{left}) = 0.6561$ and $Q^*(3, \text{right}) = 0.81$. The two identifiable splits are

| aggregation | $v$ | adv (left, right) up to a constant | $Q$ (left, right) |
|---|---|---|---|
| mean | 0.73305 | $(-0.07695, 0.07695)$ | $(0.6561, 0.81)$ |
| max | 0.81 | $(-0.1539, 0)$ | $(0.6561, 0.81)$ |
| naive sum | any $v$ | $(0.6561 - v, 0.81 - v)$ | $(0.6561, 0.81)$ |

With the max, $v = 0.81 = V^*(3)$. With the mean, $v$ is the mean of the two Q-values. With the naive sum, every $v$ works, so the split carries no information.

**A full run.** The implementation trains a dueling network (16 hidden units, one-hot input) with the Double DQN target on that chain for 3000 steps with sync period 50. With the mean aggregation and seeds 0 and 1, and with the max aggregation and seed 0, the greedy policy is optimal and $Q(s, \text{right})$ is within 0.03 of $0.9^{5-s}$ in every state.

## Correctness

The architecture has no learning guarantee beyond that of the algorithm that trains it. What is proved (full proofs below) is that the two aggregations give an identifiable split and the naive sum does not:

1. **Mean.** If $V + A(a) - \frac{1}{M}\sum_b A(b) = Q(a)$ for all $a$, then $V = \frac{1}{M}\sum_a Q(a)$, and $A$ is fixed up to an added constant, which does not change $Q$.
2. **Max.** If $V + A(a) - \max_b A(b) = Q(a)$ for all $a$, then $V = \max_a Q(a)$, and $A$ is fixed up to an added constant.
3. **Naive sum.** $V + A(a) = Q(a)$ has a solution for every $V$.
4. **Same class.** For each aggregation, every vector $Q \in \mathbb{R}^M$ is the output for some $V$ and $A$. With linear heads and the mean or the sum, the dueling heads represent exactly what a plain linear output layer of $M$ units can, from the same features. With the max, the output is piecewise affine in the features, a different class.

## Complexity

One forward pass costs the shared body $W$, plus $O(H)$ for the value head and $O(H M)$ for the advantage head, plus $O(M)$ for the aggregation: $O(W + H M)$ in total. The backward pass has the same cost. A plain DQN output layer costs $O(H M)$ too, so the extra cost is one head of $H + 1$ parameters. In the paper each head has its own fully connected hidden layer, which doubles the size of that part of the network.

## Properties

- **Same function class, different parameterization.** By fact 4, with the mean aggregation a dueling network represents exactly the Q-functions that a plain head on the same features can (with the max it is a piecewise affine class). The change is in the gradient dynamics, not in what can be represented.
- **Shared value learning.** Every sample updates $v$, so the value of a state improves even from samples of actions that are rarely taken.
- **Robust to small action gaps.** When the gap between the best and second-best action values is small compared with the scale of $Q$, noise in the estimates can swap the greedy action. Learning the gaps in a separate head that does not carry the scale of $V$ helps keep their order right.
- **Deterministic forward pass.**

## Variants and improvements

- **Max aggregation** (equation 8), where $v$ estimates $V^*$ directly.
- **Rainbow** (Hessel and others, 2018) combines the dueling network with [Double DQN](/double-dqn/), [prioritized replay](/prioritized-experience-replay/), multi-step targets, distributional outputs and noisy networks.
- **Advantage updating** (Baird, 1993) learned a value and advantages as two separate functions with separate update rules, in continuous time. The dueling network gets the same split from one network and one loss.
- **Normalized advantage functions** use a quadratic advantage $A(s, a) = -\frac12 (a - \mu(s))^\top P(s) (a - \mu(s))$ for continuous actions, whose maximum is 0 at $a = \mu(s)$; this is the max aggregation for an infinite action set.

## When to use it

Use it as the network of a DQN-family agent whenever the action set is finite, and especially when many actions have similar values in many states. The paper's corridor experiment shows that the gain over a plain head grows with the number of actions. It gives nothing for problems with one or two actions where all actions matter in every state, and it does not apply to [actor-critic](/actor-critic/) methods with continuous actions without a change like the quadratic advantage above.

## Pitfalls

- **Using the naive sum.** $Q = V + A$ trains, but the split is arbitrary, and the value head loses its meaning. Subtract the mean or the max.
- **Reading $v$ as $V^*$ under the mean.** With the mean aggregation, $v$ is the mean of the Q-values, not the maximum. Only with the max aggregation does $v$ estimate $V^*$.
- **Forgetting the gradient through the aggregation.** The subtracted mean or max depends on the advantage head, so the gradient to $\text{adv}[b]$ is $[a = b] - w_b$, not $[a = b]$. Auto-differentiation does this right; hand-written gradients often do not.
- **Ties in the max.** With the max aggregation, the gradient through $\max_b \text{adv}[b]$ is a subgradient; pick a fixed rule for ties.

## Implementations

## History

Baird (1993) proposed advantage updating, which learns a state value and an advantage function separately. Wang, Schaul, Hessel, van Hasselt, Lanctot and de Freitas (2016) put the same split inside one deep Q-network with an aggregation layer, showed that the naive sum is not identifiable, and trained the result with Double DQN. On the 57 Atari games it improved on Double DQN, and with prioritized replay it gave the best results reported at that time. Saliency maps in the paper showed the value head attending to the road ahead in Enduro and the advantage head attending to nearby cars. The architecture is one of the six parts of Rainbow (2018).

## References
