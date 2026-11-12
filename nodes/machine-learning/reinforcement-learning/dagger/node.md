---
tag: C2SKZR
kind: algorithm
slug: dagger
name: DAgger
aliases:
- Dataset Aggregation
area: machine-learning/reinforcement-learning
level: advanced
summary: "Imitation learning that runs the learned policy, asks the expert to label the states it visits, adds them to one data set and retrains, so errors grow linearly, not quadratically, in T."
solves: [imitation-learning]
model: real-ram
complexity:
  vars: {N: the number of iterations, M: the number of episodes per iteration, T: the episode length, C: the cost to train the classifier on the aggregated data once}
  time: {worst: "O(N M T + N C)"}
  space: {extra: "O(N M T)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 2011
  people: [Stephane Ross, Geoffrey J. Gordon, J. Andrew Bagnell]
  note: "Ross, Gordon and Bagnell reduced imitation learning to no-regret online learning at AISTATS 2011 and named the method DAgger."
prereqs: [imitation-learning, markov-decision-process]
see_also: [follow-the-leader, regret, online-convex-optimization, classification, structured-prediction, inverse-reinforcement-learning, offline-reinforcement-learning, policy]
sources:
  - paper: "Stephane Ross, Geoffrey J. Gordon and J. Andrew Bagnell, A reduction of imitation learning and structured prediction to no-regret online learning, Proceedings of the 14th International Conference on Artificial Intelligence and Statistics (AISTATS), 2011, pages 627 to 635, arXiv:1011.0686"
    locator: Section 2 (the T squared bound of behavior cloning and the u T bound for a policy with small loss on its own states), Section 3 (Algorithm DAgger, the beta schedule, the guarantees through no-regret learning), Section 5 (Super Tux Kart, Super Mario Bros and handwriting experiments)
  - paper: "Stephane Ross and J. Andrew Bagnell, Efficient reductions for imitation learning, Proceedings of the 13th International Conference on Artificial Intelligence and Statistics (AISTATS), 2010, pages 661 to 668"
    locator: the T squared epsilon bound for supervised imitation, and the forward training and SMILe algorithms
  - paper: "Hal Daume III, John Langford and Daniel Marcu, Search-based structured prediction, Machine Learning 75(3), 2009, pages 297 to 325"
    locator: SEARN, the earlier iterative reduction with stochastic policy mixing
  - paper: "Matti Kaariainen, Lower bounds for reductions, talk at the Atomic Learning Workshop, Toyota Technological Institute at Chicago, 2006"
    locator: the example where small classification error gives cost of order T squared
  - paper: "Stephane Ross and J. Andrew Bagnell, Reinforcement and imitation learning via interactive no-regret learning, arXiv:1406.5979, 2014"
    locator: AggreVaTe, DAgger with cost-to-go labels
---

DAgger (Dataset Aggregation; Ross, Gordon and Bagnell, 2011) learns a policy from an expert who can be asked what to do in any state. Plain [behavior cloning](/imitation-learning/) trains a classifier only on the states the expert visits. When the learned policy makes a mistake, it reaches states the expert never showed, makes more mistakes there, and its cost can grow as $T^2 \varepsilon$ over $T$ steps. DAgger runs the *learned* policy, asks the expert to label every state it visits, adds these labels to one growing data set, and trains again. The policy is then trained on the states it will actually meet. Because each round fits all the data so far, DAgger is an instance of [follow the leader](/follow-the-leader/), and any no-regret learner gives a policy whose cost is within $u T \varepsilon$ of the expert's.

## In plain words

A learner driver who only watches a good driver never sees the car close to the edge of the road, so they do not know how to recover from there. DAgger lets the learner drive, and an instructor in the passenger seat says what they would do at every moment. The learner adds these notes to all the earlier ones and practices again. After a few rounds the notes cover the places where the learner really goes, including the mistakes, and the learner knows how to get back.

## The problem

The setting is [imitation learning](/imitation-learning/) with an interactive expert. There is a [Markov decision process](/markov-decision-process/) with an unknown cost $C(s, a) \in [0, 1]$, an episode length $T$, and an expert policy $\pi^*$ that we can query: for any state $s$ the expert returns its action $\pi^*(s)$. We do not see the cost. We choose a policy from a class $\Pi$ (for example, a classifier) and want a small expected total cost $J(\pi) = \mathbb{E}\big[\sum_{t=1}^{T} C(s_t, a_t)\big]$.

Write $d_\pi$ for the average distribution of states over the $T$ steps of $\pi$, and $\ell(s, \pi) = \Pr[\pi(s) \ne \pi^*(s)]$ for the 0-1 loss against the expert (other surrogate losses also work). Two numbers measure a policy:

- $\varepsilon = \mathbb{E}_{s \sim d_{\pi^*}}[\ell(s, \pi)]$, its error on the *expert's* states. Behavior cloning makes this small.
- $\varepsilon_\pi = \mathbb{E}_{s \sim d_\pi}[\ell(s, \pi)]$, its error on *its own* states. DAgger makes this small.

## The algorithm

```pseudo id=main
DAGGER(expert π*, policy class Π, N, M, β_1, …, β_N)
L1  D ← ∅;  π̂_1 ← any policy in Π
L2  for i ← 1 to N
L3      π_i ← β_i π* + (1 − β_i) π̂_i        (in each state, use the expert with probability β_i)
L4      run π_i for M episodes of T steps
L5      D ← D ∪ {(s, π*(s)) : s visited in L4}   (the expert labels the states; π_i still acts)
L6      π̂_{i+1} ← the classifier in Π with the least loss on D
L7      keep π̂_{i+1} as a candidate
L8  return the best of π̂_1, …, π̂_{N+1} on validation episodes (or simply the last)
```

The mixing weights $\beta_i$ let the expert act in early rounds, when $\hat\pi_i$ is still poor. The theory needs the average $\frac{1}{N}\sum_i \beta_i \to 0$, for example $\beta_i = p^{i-1}$. Ross, Gordon and Bagnell report that the simple choice $\beta_1 = 1$ and $\beta_i = 0$ for $i \ge 2$ often works best; then the first round is behavior cloning, and every later round runs the learned policy only.

Line L5 is the key step: the states come from the learner, the labels from the expert. Line L6 trains on *all* data so far, not only on the newest round; this is what makes the method follow the leader, an online learner with no regret for many losses.

## Example

The implementation uses a windy lane. The position is $x \in \{-8, \dots, 8\}$, and a wind pushes it one step to the right at every step. The action $a \in \{-2, -1, 0\}$ steers left, so the next position is $x + a + 1$, clipped to the lane. The expert steers $-2$ when $x > 0$, $-1$ at $x = 0$ (to stay) and $0$ when $x < 0$. The cost of a step is $\min(|x|, 4)/4$, episodes have $T = 40$ steps from $x = 0$, and the expert's cost is 0 because it never leaves $x = 0$.

The learner is a table with one entry per position, fit by majority vote. Where it has no label, it does not steer ($a = 0$). To make it an imperfect classifier, it takes a uniformly random action with probability $0.1$, so even the best table errs with probability $0.1 \cdot 2/3 \approx 0.067$ in each state.

| policy | states with a label | $\varepsilon$ (expert's states) | $\varepsilon_\pi$ (own states) | cost $J$ |
|---|---|---|---|---|
| expert | | 0 | 0 | 0 |
| behavior cloning, 5 expert episodes | $0$ | 0.067 | 0.447 | 15.97 |
| DAgger $\hat\pi_1$ (no data) | none | 0.967 | 0.966 | 37.19 |
| DAgger $\hat\pi_2$ (round 1, $\beta_1 = 1$) | $0$ | 0.067 | 0.447 | 15.97 |
| DAgger $\hat\pi_3$ (round 2, $\beta_2 = 0$) | $-1, 0, 1, \dots, 8$ | 0.067 | 0.067 | 0.695 |
| the full correct table | all | 0.067 | 0.067 | 0.695 |

Behavior cloning sees only $x = 0$, because the expert never leaves it. Its error on the expert's states is the smallest possible, 0.067, but one random push to $x = 1$ puts it in a state with no label, it does not steer, and the wind carries it to the wall. At the last step 60% of its probability is at $x = 8$. DAgger's second round runs this poor policy, so it visits $1, 2, \dots, 8$, and the expert labels them. The third policy is then as good as the best table. With one episode per round and five rounds, DAgger's last policy equals the best table in 16 of 20 seeds, and it is better than behavior cloning in all 20.

The bounds of the next section hold here: for behavior cloning, $15.97 \le T^2 \varepsilon = 1600 \cdot 0.067 = 106.7$; for DAgger, with $u = 2$ for this lane, $0.695 \le u T \varepsilon_\pi = 2 \cdot 40 \cdot 0.067 = 5.33$.

## Correctness

DAgger does not find the expert's policy; it bounds the cost of the policy it returns. The [proof page](proofs/correctness.md) proves three steps.

1. **Behavior cloning can compound** (Ross and Bagnell, 2010). For any policy, $J(\pi) \le J(\pi^*) + T^2 \varepsilon$. The proof couples $\pi$ with the expert: until the first mistake the two runs are in the same state, and the probability of a mistake before step $t$ is at most $T\varepsilon$. Kääriäinen's example shows that the $T^2$ is tight.
2. **Small error on its own states is enough.** If every one-step deviation from the expert costs at most $u$ extra in the expert's cost-to-go, then $J(\pi) \le J(\pi^*) + u T \varepsilon_\pi$. This follows from the performance difference identity $J(\pi) - J(\pi^*) = \sum_t \mathbb{E}_{s \sim d^t_\pi}\big[Q^*_{T-t}(s, \pi) - Q^*_{T-t}(s, \pi^*)\big]$.
3. **DAgger makes $\varepsilon_\pi$ small.** Round $i$ gives the online loss $\ell_i(\pi) = \mathbb{E}_{s \sim d_{\pi_i}}[\ell(s, \pi)]$, and line L6 plays follow the leader on these losses. If this learner has average regret $\gamma_N$, then some $\hat\pi_i$ has $\varepsilon_{\hat\pi_i} \le \varepsilon_N + \gamma_N + \frac{1}{N}\sum_i \min(1, T\beta_i)$, where $\varepsilon_N$ is the loss of the best policy in $\Pi$ on the aggregated distributions. With step 2 this gives $J(\hat\pi) \le J(\pi^*) + uT(\varepsilon_N + \gamma_N + \dots)$, linear in $T$.

The tests check the bounds of steps 1 and 2 exactly on many tables and the identity of step 2 to $10^{-9}$.

## Complexity

Each round runs $M$ episodes of $T$ steps and asks $MT$ expert queries, so DAgger makes $NMT$ queries in all, and the data set grows to $NMT$ labeled states. Training once on the aggregated data costs $C$, which grows with the data, so the total is $O(NMT + NC)$. For the guarantee with a strongly convex loss, Ross, Gordon and Bagnell show that $N = \tilde O(T)$ rounds suffice (with finite samples, $N$ and $M$ also depend on the wanted confidence). Space is the data set, $O(NMT)$. In practice the cost is the expert's time: every visited state needs a label.

## Properties

- **Interactive.** DAgger needs an expert who can label states that the learner reaches; recorded demonstrations alone are not enough.
- **A reduction.** Any classifier or regressor can be used in line L6. The guarantee is in terms of its loss $\varepsilon_N$ and the regret of the online procedure.
- **Stationary policy.** The result is one policy for all time steps, unlike forward training (Ross and Bagnell, 2010), which trains $T$ policies.
- **Linear in $T$.** The cost bound is $u T \varepsilon_N$ in place of $T^2 \varepsilon$, when $u$ is small, that is, when the expert can recover from one mistake at small cost.
- **Not exact.** If $\Pi$ cannot represent the expert, even DAgger has $\varepsilon_N > 0$; it then has the best error among policies in $\Pi$ on the states it visits.

## Variants and improvements

- **SEARN** (Daumé, Langford and Marcu, 2009) and **SMILe** (Ross and Bagnell, 2010) are earlier iterative methods that mix stochastic policies; DAgger replaces mixing by data aggregation.
- **AggreVaTe** (Ross and Bagnell, 2014) asks the expert for its cost-to-go of each action, not only its best action, and so handles costs that differ between mistakes.
- **HG-DAgger** and **SafeDAgger** let a human expert take control only when needed, or let a learned rule decide when to ask, to reduce the number of queries.
- **DART** (Laskey and others, 2017) adds noise to the expert's demonstrations so that a single batch of data covers nearby states, without labels on the learner's own states.
- **Online learners other than follow the leader**, for example online gradient descent on the newest data, give the same guarantee when they have no regret; see [online convex optimization](/online-convex-optimization/).
- **Structured prediction.** The same reduction trains sequence labelers and parsers, where a "state" is a partial output and the "expert" is the correct output; see [structured prediction](/structured-prediction/).

## When to use it

- Use DAgger when an expert (a person, a planner with privileged information, or a slow optimal solver) can label any state cheaply, and behavior cloning drifts.
- Use it to distill a slow planner into a fast policy: the planner labels the states that the fast policy visits.
- Do not use it when only recorded data is available; then use [behavior cloning](/imitation-learning/), [inverse reinforcement learning](/inverse-reinforcement-learning/) or [offline reinforcement learning](/offline-reinforcement-learning/).
- Do not use it when the learner's mistakes are dangerous or expensive during training; run it in simulation, or let the expert take over (HG-DAgger).

## Pitfalls

- **Labels in states the expert would never reach** can be hard for a human to give: it is not natural to say what to do while the car is already off the road. The quality of these labels limits DAgger.
- **Training only on the newest round** loses the no-regret property and can oscillate between two policies.
- **Returning the last policy** is common and often works, but the guarantee is for the best of $\hat\pi_1, \dots, \hat\pi_{N+1}$ or for a mixture of them; keep a validation set.
- **A large $u$** (one mistake leads to a state the expert cannot leave cheaply) weakens the bound; then AggreVaTe or reinforcement learning is a better fit.
- **Labels must be the expert's action in that state**, not the action that $\pi_i$ took. Storing the learner's own actions is a common bug, and it teaches the learner its mistakes.

## Implementations

## History

Pomerleau's ALVINN (1989) learned to steer by behavior cloning and already found that the network could not recover from states that the human driver never showed. Kääriäinen (2006) gave a lower bound of order $T^2 \varepsilon$ for the plain reduction, and Ross and Bagnell (2010) proved the matching upper bound and proposed forward training and SMILe. Daumé, Langford and Marcu's SEARN (2009) used a related iterative reduction for structured prediction. Ross, Gordon and Bagnell (2011) proposed DAgger, proved its guarantees through no-regret online learning, and showed it on the Super Tux Kart and Super Mario Bros games and on handwriting recognition. Ross and Bagnell (2014) extended it to AggreVaTe with cost-to-go labels.

## References
