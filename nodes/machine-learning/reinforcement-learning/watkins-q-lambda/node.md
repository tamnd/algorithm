---
tag: EMENRX
kind: algorithm
slug: watkins-q-lambda
name: Watkins's Q(lambda)
aliases:
- Watkins Q(lambda)
- "Watkins's Q(λ)"
area: machine-learning/reinforcement-learning
level: advanced
summary: "Q-learning with eligibility traces on state-action pairs. Traces decay by gamma lambda after a greedy action and are cut to zero after a non-greedy one, so it stays off-policy."
solves: [rl-control]
model: real-ram
complexity:
  vars: {T: the total number of steps, A: the largest number of actions in a state, S: the number of states}
  time: {worst: "O(S A T)"}
  space: {extra: "O(S A)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 1989
  people: [Christopher J. C. H. Watkins]
  note: Watkins proposed Q-learning in his PhD thesis together with its form with eligibility traces, cut after exploratory actions.
prereqs: [q-learning, td-lambda, eligibility-traces]
see_also: [retrace, importance-sampling-off-policy, sarsa, expected-sarsa, n-step-td, double-q-learning, tabular-q-learning-convergence, deadly-triad]
sources:
  - paper: "Christopher J. C. H. Watkins, Learning from Delayed Rewards, PhD thesis, University of Cambridge, 1989"
    locator: the proposal of Q-learning and of its multi-step form with traces
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 12.10 (Watkins's Q(lambda) to Tree-Backup(lambda))
  - paper: "Jing Peng and Ronald J. Williams, Incremental multi-step Q-learning, Machine Learning 22, 1996, pages 283 to 290"
    locator: Peng's Q(lambda), the form without the cut
---

Watkins's Q(λ) combines [Q-learning](/q-learning/) with [eligibility traces](/eligibility-traces/) on state-action pairs. Each step computes the Q-learning TD error $\delta = R + \gamma \max_a Q(S', a) - Q(S, A)$ and applies it to every pair in proportion to its trace, as [TD(λ)](/td-lambda/) does for states. The traces decay by $\gamma\lambda$ as long as the agent takes greedy actions, and are cut to zero as soon as it takes a non-greedy one. The cut keeps the method off-policy: rewards earned after an exploratory action do not count as evidence about the greedy policy. Watkins (1989) proposed it in the thesis that introduced Q-learning; Sutton and Barto (Section 12.10) present it as tree backup with a greedy target policy.

## In plain words

Q-learning fixes the score of one move per step. When a reward finally comes, only the last move learns of it, and the news crawls back one step per episode.

Traces let one reward update many earlier moves at once, each a little less the further back it was. But Q-learning learns the value of always playing the best move. If the agent took a random move on the way, the reward after it says something about that random detour, not about the best play before it. So at a random move, Watkins's Q(λ) wipes the memory of the earlier moves, and only the moves since then get credit.

## The problem

The setting is that of [Q-learning](/q-learning/) and [RL control](/rl-control/): a finite MDP that the algorithm can only sample, a discount $0 \le \gamma \le 1$, and the goal of $q_*$ and a greedy optimal policy, from data of an exploring behavior policy. One-step Q-learning propagates a reward back one pair per visit. The aim is faster credit assignment through multi-step returns, as in [n-step TD](/n-step-td/) and [TD(λ)](/td-lambda/), without losing the off-policy target $q_*$.

## The algorithm

```pseudo id=main
WATKINS-Q-LAMBDA(episodes, α, γ, λ, ε)
L1  Q(s, a) ← 0 for all pairs
L2  for each episode do
L3      z(s, a) ← 0 for all pairs; S ← the start state; A ← ε-greedy action for Q in S
L4      repeat until S is terminal
L5          take A, observe R and S′
L6          if S′ is terminal then δ ← R − Q(S, A); A′ ← none
L7          else A′ ← ε-greedy action for Q in S′
L8              A* ← A′ if Q(S′, A′) = max_b Q(S′, b), else a greedy action in S′
L9              δ ← R + γ Q(S′, A*) − Q(S, A)
L10         z(S, A) ← z(S, A) + 1
L11         for each pair (s, a) with z(s, a) ≠ 0 do
L12             Q(s, a) ← Q(s, a) + α δ z(s, a)
L13         if A′ = A* then z ← γλ z
L14         else z ← 0                     ▷ the cut: A′ is not greedy, or the episode ended
L15         S ← S′; A ← A′
L16 return Q
```

Line L8 prefers $A'$ when it ties for the max, so a tie is not a cut. In every case $Q(S', A^*) = \max_b Q(S', b)$, so line L9 is the Q-learning TD error. The next action $A'$ is drawn before the update of line L12, because the trace rule of lines L13 and L14 depends on it. The traces here are accumulating; replacing traces, $z(S, A) \leftarrow 1$, are also common.

## Example

**The cut on a fixed episode.** Take a chain of four states 0, 1, 2, 3. Two actions, $g$ and $x$, both move right, every step gives $R = 1$, and the step from state 3 ends the episode. Let $\gamma = 1$, $\lambda = 1/2$, $\alpha = 1/2$, and start with $Q(2, g) = 1$ and all other values 0, so that $g$ is greedy in state 2 and all actions tie elsewhere. The agent plays $g, g, x, g$; the $x$ in state 2 is not greedy.

| step | $S, A$ | $A'$ greedy? | $\delta$ | values after the step | traces after the step |
| --- | --- | --- | --- | --- | --- |
| 1 | 0, g | yes (tie) | $1$ | $Q(0,g) = 1/2$ | $z(0,g) = 1/2$ |
| 2 | 1, g | no, $x$ in state 2 | $1 + 1 - 0 = 2$ | $Q(0,g) = 1$, $Q(1,g) = 1$ | all cut to 0 |
| 3 | 2, x | yes (tie) | $1$ | $Q(2,x) = 1/2$ | $z(2,x) = 1/2$ |
| 4 | 3, g | episode ends | $1$ | $Q(2,x) = 3/4$, $Q(3,g) = 1/2$ | all 0 |

At step 2 the traces of $(0, g)$ and $(1, g)$ are cut, so the rewards of steps 3 and 4, which came after the exploratory $x$, change only $Q(2, x)$ and $Q(3, g)$. Without the cut, the same episode would also raise $Q(0, g)$ to $19/16$ and $Q(1, g)$ to $11/8$, crediting the greedy actions with the outcome of a detour.

**Faster credit when the agent stays greedy.** On a chain of five states with reward 1 only on the last step, all values 0 and greedy play, one episode with $\alpha = 1/2$ and $\gamma = 1$ sets $Q(i, g) = \tfrac12 (\gamma\lambda)^{4-i}$ for $i = 0, \dots, 4$: all five pairs learn of the reward at once for $\lambda = 1$, and only the last pair does for $\lambda = 0$, which is one-step Q-learning.

## Correctness

**The backup follows the greedy policy.** Between two cuts, the actions after the first one are greedy for $Q$, so the λ-return that the traces build (see [TD(λ)](/td-lambda/)) is a return of the greedy policy, with the max in each TD error. In the language of Sutton and Barto (Section 12.10), it is Tree-Backup(λ) with a greedy target policy $\pi$: the trace update $z \leftarrow \gamma\lambda\,\pi(A' \mid S')\,z$ is $\gamma\lambda z$ for a greedy $A'$ and $0$ otherwise. Every expected backup is thus a mix of Bellman optimality backups, whose fixed point is $q_*$.

**Two special cases.** With $\lambda = 0$, lines L13 and L14 leave no trace after the update, and the method is one-step Q-learning, except that the next action is drawn before the update. With a greedy behavior ($\varepsilon = 0$) there are no cuts, and it is a SARSA(λ) on greedy actions.

**Convergence.** For the tabular case, Munos, Stepleton, Harutyunyan and Bellemare (2016) showed that Watkins's Q(λ) converges to $q_*$, as a special case of their analysis of [Retrace](/retrace/), under conditions like those of [tabular Q-learning convergence](/tabular-q-learning-convergence/). The proofs section shows that the traces compute a λ-return that follows only greedy actions, and that $q_*$ is a fixed point of the expected update.

## Complexity

Each step costs one call to the environment, $O(A)$ for the ε-greedy choice and the max, and one update per pair with a nonzero trace. At most $SA$ pairs have a nonzero trace, and in practice only those visited since the last cut, so $T$ steps take $O(SAT)$ time in the worst case and $O(T(A + L))$ when traces stay over at most $L$ pairs. The tables of values and traces take $O(SA)$ memory. Traces below a small threshold can be dropped to keep $L$ small.

## Properties

- **Off-policy.** It learns about the greedy policy from an exploring behavior, like Q-learning.
- **Multi-step only while greedy.** The gain over Q-learning depends on the length of greedy runs. With $\varepsilon = 0.1$ and $k$ actions, a run lasts about $1 / (\varepsilon (1 - 1/k))$ steps on average.
- **Contains Q-learning.** With $\lambda = 0$ it is one-step Q-learning.
- **Online and incremental.** Each step is a constant number of passes over the traces, with no stored returns.

## Variants and improvements

- **Peng's Q(λ).** Peng and Williams (1996) never cut the traces. The backup uses the actual rewards along the behavior path and the max only at the bootstrap, a mix of the behavior and greedy policies. It converges to $q_*$ only if the behavior becomes greedy, but it often learns faster because the traces are not cut.
- **Naive Q(λ).** Keep Watkins's update and never cut the traces. The update is simpler than Peng's, but like Peng's form it does not learn $q_*$ in general while the behavior explores.
- **Tree-Backup(λ) and [Retrace](/retrace/).** Replace the 0 or 1 cut by $\pi(A' \mid S')$ for a general target policy, or by $\lambda \min(1, \pi / b)$, which cuts less often while staying safe off-policy.
- **[Importance sampling](/importance-sampling-off-policy/).** Weighting by $\pi / b$ instead of cutting gives unbiased but high-variance multi-step off-policy returns; for a greedy $\pi$ the ratio is 0 at a non-greedy action, which is again the cut.
- **Function approximation.** Replace the table by $\hat q(s, a, w)$ and the traces by a vector over the weights. Off-policy traces with bootstrapping and approximation can diverge (the [deadly triad](/deadly-triad/)).

## When to use it

Use Watkins's Q(λ) for tabular off-policy control when rewards are delayed and the behavior is mostly greedy, so that greedy runs are long and the traces help. If exploration is heavy, the cuts make it close to one-step Q-learning. If an on-policy answer is fine, SARSA(λ) uses every trace without cuts. For general target policies and longer traces, use Tree-Backup(λ) or Retrace.

## Pitfalls

- **Cutting on ties.** If the chosen action ties for the max, it is greedy; cutting there throws away traces for no reason.
- **Choosing the next action after the update.** The cut must use the action that will actually be taken next. Drawing it once, before the update, and then using it keeps the two consistent.
- **Cutting too late or too early.** The cut applies after the update with the current $\delta$, which still credits the earlier pairs for the step that led to the non-greedy state. Resetting before that update loses that credit.
- **Large step sizes with accumulating traces.** A pair visited many times in one greedy run gets a trace above 1, and $\alpha z > 1$ can overshoot. Use replacing traces or smaller $\alpha$.
- **Expecting a large speedup.** With ε-greedy exploration in every state, greedy runs are short and the speedup over Q-learning is often small.

## Implementations

## History

Christopher Watkins (1989) introduced Q-learning in his Cambridge PhD thesis, together with a multi-step form that uses traces of past state-action pairs and stops them at exploratory actions. Peng and Williams (1996) proposed the form without the cut. Sutton and Barto (first edition 1998, second edition 2018, Section 12.10) presented both, and placed Watkins's method within Tree-Backup(λ). Munos, Stepleton, Harutyunyan and Bellemare (2016) proved its convergence in the tabular case through their analysis of Retrace(λ).

## References
