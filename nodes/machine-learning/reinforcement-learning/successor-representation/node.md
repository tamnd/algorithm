---
tag: FGK3ES
kind: concept
slug: successor-representation
name: Successor representation
aliases:
- successor matrix
- successor features
area: machine-learning/reinforcement-learning
level: research
summary: "M(s, s') is the expected discounted number of visits to s' from s under a policy: M = (I - gamma P)^(-1). Values follow as V = M r, so rewards can change without relearning."
prereqs: [state-value-function, temporal-difference-learning, bellman-expectation-equation]
see_also: [value-function-approximation, least-squares-td, model-based-reinforcement-learning, options-framework, td-lambda, neumann-series, laplacian-matrix, markov-chain]
sources:
  - paper: doi:10.1162/neco.1993.5.4.613
    title: Peter Dayan, Improving generalization for temporal difference learning, The successor representation, Neural Computation 5(4), 1993, pages 613 to 624
    locator: the definition of the successor representation, value as a linear function of it, and its learning by TD
  - paper: arxiv:1606.05312
    title: André Barreto, Will Dabney, Rémi Munos, Jonathan J. Hunt, Tom Schaul, Hado van Hasselt and David Silver, Successor features for transfer in reinforcement learning, Advances in Neural Information Processing Systems 30, 2017
    locator: successor features, generalized policy improvement and transfer across reward functions
  - paper: doi:10.1038/nn.4650
    title: Kimberly L. Stachenfeld, Matthew M. Botvinick and Samuel J. Gershman, The hippocampus as a predictive map, Nature Neuroscience 20(11), 2017, pages 1643 to 1653
    locator: place cells as rows of the successor representation and grid cells as its eigenvectors
  - paper: doi:10.1038/s41562-017-0180-8
    title: Ida Momennejad, Evan M. Russek, Jin H. Cheong, Matthew M. Botvinick, Nathaniel D. Daw and Samuel J. Gershman, The successor representation in human reinforcement learning, Nature Human Behaviour 1(9), 2017, pages 680 to 692
    locator: reward and transition revaluation experiments that separate the successor representation from model-free and model-based learning
  - paper: doi:10.1145/1102351.1102421
    title: Sridhar Mahadevan, Proto-value functions, Developmental reinforcement learning, Proceedings of the 22nd International Conference on Machine Learning, 2005, pages 553 to 560
    locator: basis functions from the eigenvectors of the graph Laplacian of the state space
  - paper: arxiv:1710.11089
    title: Marlos C. Machado, Clemens Rosenbaum, Xiaoxiao Guo, Miao Liu, Gerald Tesauro and Murray Campbell, Eigenoption discovery through the deep successor representation, International Conference on Learning Representations, 2018
    locator: options from the eigenvectors of a learned successor representation
---

The successor representation (SR) of a fixed policy $\pi$ in a Markov decision process is the matrix $M$ whose entry $M(s, s')$ is the expected discounted number of times the agent visits $s'$ when it starts in $s$ and follows $\pi$. In matrix form $M = \sum_{t \ge 0}\gamma^tP^t = (I - \gamma P)^{-1}$, where $P$ is the state transition matrix of the policy. The [state value](/state-value-function/) is then the product $V = Mr$ of the SR with the expected reward vector $r$. So the SR separates what the policy does, which states it reaches and how soon, from what those states are worth. Dayan (1993) introduced it and showed that it can be learned by [temporal difference learning](/temporal-difference-learning/): $M$ satisfies its own Bellman equation $M = I + \gamma PM$, with the indicator vector of the current state in place of the reward. When the rewards change, the new values follow from one product, with no new learning about the dynamics. Successor features (Barreto et al. 2017) extend the idea to feature vectors.

## In plain words

Think of every place you can be in. For each starting place, write down how often you expect to be in every other place in the future, counting soon visits more than late ones. This table is the successor representation.

Now suppose each place has a prize. Your expected future prize from a starting place is just the sum, over all places, of how often you will be there times the prize there. So when the prizes move, you do not need to explore again: the table of visits is still right, and you only redo the sum. The table can be learned by walking around, with the same kind of small corrections that TD learning uses for values.

## The idea

**Definition.** Fix a policy $\pi$ with state transition matrix $P(s, s') = \sum_a\pi(a \mid s)P(s' \mid s, a)$ and a discount $\gamma < 1$. Then

$$M(s, s') = \mathbb{E}_\pi\Big[\sum_{t \ge 0}\gamma^t\,\mathbf{1}[S_t = s'] \;\Big|\; S_0 = s\Big], \qquad M = \sum_{t \ge 0}\gamma^tP^t = (I - \gamma P)^{-1}.$$

The series is a [Neumann series](/neumann-series/); it converges because every eigenvalue of $\gamma P$ has modulus at most $\gamma < 1$. Every entry of $M$ is nonnegative, the diagonal entries are at least $1$, and every row sums to $1/(1 - \gamma)$, since the visits to all states add up to $\sum_t\gamma^t$.

**Values.** With $r(s)$ the expected reward on leaving $s$, the value is

$$V^\pi(s) = \mathbb{E}_\pi\Big[\sum_{t \ge 0}\gamma^tr(S_t)\Big] = \sum_{s'}M(s, s')r(s'), \qquad V^\pi = Mr.$$

It solves the [Bellman expectation equation](/bellman-expectation-equation/) $V = r + \gamma PV$, because $(I - \gamma P)Mr = r$. In the language of [value function approximation](/value-function-approximation/), $V$ is linear in the features $M(s, \cdot)$ with weights $r$.

**A Bellman equation for $M$.** Splitting off the first step gives $M = I + \gamma PM$: row $s$ of $M$ is the indicator $\mathbf{1}_s$ plus $\gamma$ times the expected row of the next state. So $M$ can be learned from transitions $s \to s'$ like a value function whose "reward" is the vector $\mathbf{1}_s$:

$$M(s, \cdot) \leftarrow M(s, \cdot) + \alpha\big(\mathbf{1}_s + \gamma M(s', \cdot) - M(s, \cdot)\big).$$

Each column $M(\cdot, j)$ is the value function for the reward $\mathbf{1}[s = j]$, so this is tabular TD(0) run on $n$ reward functions at once, and it converges under the same conditions on the step sizes as TD(0). The update costs $O(n)$ per step for $n$ states.

**Action-dependent SR and successor features.** The SR of pairs, $M(s, a, s')$, gives action values $Q = Mr$ and supports control. With a feature map $\phi$, the successor features $\psi^\pi(s) = \mathbb{E}_\pi[\sum_t\gamma^t\phi(S_t)]$ satisfy $\psi = \phi + \gamma P\psi$, and when $r(s) = \phi(s)^\top w$ the value is $\psi(s)^\top w$. Barreto et al. (2017) combine the successor features of several policies by generalized policy improvement, acting greedily with respect to $\max_i\psi^{\pi_i}(s, a)^\top w$, to transfer to new reward vectors $w$.

**Where the SR sits.** It lies between model-free and [model-based](/model-based-reinforcement-learning/) methods. A value function caches the sum $Mr$ and must be relearned when $r$ changes. A model stores $P$ and must plan to get values. The SR caches the multi-step dynamics under one policy, so reward changes are cheap, but changes in the transitions, or in the policy, require relearning $M$.

## Examples

**A four-state chain.** States $0, 1, 2, 3$ in a row. From each state the agent moves left or right with probability $1/2$, and stays put when it would leave the chain. With $\gamma = 1/2$,

$$M = \frac{1}{28}\begin{pmatrix} 41 & 11 & 3 & 1 \\ 11 & 33 & 9 & 3 \\ 3 & 9 & 33 & 11 \\ 1 & 3 & 11 & 41 \end{pmatrix}.$$

Each row sums to $84/28 = 2 = 1/(1 - \gamma)$. With reward $1$ in state $3$ only, $V = Mr$ is the last column, $(1, 3, 11, 41)/28$. If the reward moves to state $0$, the new values are the first column, $(41, 11, 3, 1)/28$, at once.

**Learning $M$ by TD.** On the same chain with $\gamma = 0.9$, TD learning of $M$ along one trajectory, with step size $1/k^{0.7}$ at the $k$-th visit to a state, gives these largest entry errors against the exact $M$, whose entries lie between $1.5$ and $4$ (seeds 0, 1 and 2):

| steps | seed 0 | seed 1 | seed 2 |
|---|---|---|---|
| 1000 | 0.629 | 0.926 | 0.616 |
| 10000 | 0.166 | 0.146 | 0.137 |
| 100000 | 0.014 | 0.045 | 0.034 |

With a constant step size $0.1$, the error stays near $0.2$ to $0.8$: the noise of each update does not average out.

**Revaluation in people.** Momennejad et al. (2017) trained people on sequences of rooms with rewards at the ends, then changed either the rewards or the transitions. People adapted better to reward changes than to transition changes, the pattern the SR predicts and pure model-based planning does not.

## Where it is used

- **Transfer across rewards.** Successor features and generalized policy improvement (Barreto et al. 2017) reuse what was learned about the dynamics for new tasks that differ only in the reward weights.
- **Exploration and options.** The eigenvectors of the SR of a random walk are those of the transition matrix, and for a random walk on a regular graph they are the eigenvectors of the graph [Laplacian](/laplacian-matrix/) used by proto-value functions (Mahadevan 2005). Machado et al. (2018) build eigenoptions from them for the [options framework](/options-framework/), and the norm of the SR serves as an exploration bonus.
- **Deep reinforcement learning.** Deep successor networks learn $\psi$ and $w$ with two heads of one network, and successor features underlie several transfer and multi-task agents.
- **Neuroscience.** Stachenfeld, Botvinick and Gershman (2017) model hippocampal place cells as rows of the SR and grid cells as its eigenvectors.
- **Link to LSTD.** With one-hot features, the matrix that [LSTD](/least-squares-td/) inverts is $D(I - \gamma\hat{P})$, with $D$ the diagonal matrix of visit counts and $\hat{P}$ the empirical transition matrix, so LSTD computes the value through the empirical SR $\hat{M} = (I - \gamma\hat{P})^{-1}$.

## References
