---
tag: HBAZ23
kind: technique
slug: eligibility-traces
name: Eligibility traces
aliases:
- accumulating traces
- replacing traces
- dutch traces
- eligibility trace
area: machine-learning/reinforcement-learning
level: advanced
summary: "Keep a decaying memory z of recently visited states and give each one-step TD error to all of them in proportion to z. This computes lambda-return updates online."
prereqs: [temporal-difference-learning, td-error]
see_also: [td-lambda, watkins-q-lambda, sarsa, retrace, monte-carlo-policy-evaluation, generalized-advantage-estimation, actor-critic, value-function-approximation]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Chapter 12 (the accumulating trace in Section 12.2, the dutch trace in Sections 12.5 and 12.6, Sarsa(lambda) in Section 12.7, and the traces of the off-policy methods in Sections 12.9 and 12.10)
  - paper: "Satinder P. Singh and Richard S. Sutton, Reinforcement learning with replacing eligibility traces, Machine Learning 22, 1996, pages 123 to 158"
    locator: the replacing trace, and the equivalence of offline TD(1) with first-visit Monte Carlo (replacing) and every-visit Monte Carlo (accumulating)
  - paper: doi:10.1007/BF00115009
    title: "Richard S. Sutton, Learning to predict by the methods of temporal differences, Machine Learning 3(1), 1988, pages 9 to 44"
    locator: the TD(lambda) update with the accumulating trace
  - paper: "Harm van Seijen and Richard S. Sutton, True online TD(lambda), Proceedings of the 31st International Conference on Machine Learning (ICML 2014), PMLR 32(1), pages 692 to 700"
    locator: the trace of true online TD(lambda), later called the dutch trace
---

An eligibility trace is a short-term memory $z(x)$, one number for each state or state action pair $x$, that records how recently and how often $x$ was visited. At each step all traces decay by a factor, usually $\gamma\lambda$, and the trace of the current key goes up. The one-step [TD error](/td-error/) $\delta_t$ is then given to every key in proportion to its trace: $V(x) \leftarrow V(x) + \alpha\delta_t z(x)$. With accumulating traces and values held fixed during the episode, the total update equals that of the λ-return, the forward view of [TD(λ)](/td-lambda/). The rule for raising the trace gives the three common kinds: accumulating, replacing (Singh and Sutton 1996) and dutch (van Seijen and Sutton 2014).

## In plain words

When something good or bad happens, which of your past steps deserve the credit? A trace is a mark that each step leaves behind, like a footprint that fades. A fresh footprint is clear and an old one is faint.

Each time a surprise arrives, you hand it out to all the footprints, in proportion to how clear they are. So the last few steps get most of the credit and the old ones get little. You never have to store the past steps or look back at them: the fading marks are enough.

The kinds of trace differ in what happens when you step on the same place again. One adds a new mark on top of the old one, one replaces the old mark with a fresh one, and one does something in between.

## When it applies

- **An incremental method driven by a one-step error.** The method updates a value table, or the weights of a function, with an error that is known at each step: the TD error of [TD learning](/temporal-difference-learning/), of [SARSA](/sarsa/), of [Q-learning](/q-learning/) or of a critic in [actor-critic](/actor-critic/) methods.
- **A target that is a geometric mix of future errors.** The target you want is the λ-return, or more generally $V(S_t) + \sum_{k \ge t} c_{t+1} \cdots c_k\, \gamma^{k-t}\delta_k$ with decay factors $c_k$. Then the sum can be turned around in time, and the trace of each key collects the products of the decay factors.
- **Learning online, without waiting.** Traces give each step its update at once. The forward view needs the future and so waits until the end of the episode or of a window.
- **Rewards that are delayed.** One TD error moves credit back over many steps at once, where [TD(0)](/temporal-difference-learning/) moves it back by one step per visit.

## The template

**Conventions.** A *key* is what the values are indexed by: a state $s$ for prediction, or a pair $(s, a)$ for control. $Q$ stands for the value table, $V$ or $Q$. The trace $z$ is zero at the start of each episode. The holes are the error signal $\delta_t$, the decay factor $c_t$ and the trace rule.

```pseudo id=main
TRACE-UPDATE(episode, α)
L1  z(x) ← 0 for every key x
L2  for t ← 0, 1, ... until the episode ends do
L3      x_t ← the current key                          ▷ S_t, or (S_t, A_t)
L4      δ_t ← the one-step error                       ▷ hole: TD, SARSA or Q-learning error
L5      z(x) ← c_t z(x) for every key x                ▷ hole: c_t = γλ, or γλρ_t, or 0
L6      z(x_t) ← RAISE(z(x_t))                         ▷ hole: the trace rule
L7      for every key x with z(x) ≠ 0 do
L8          Q(x) ← Q(x) + α δ_t z(x)
```

The trace rule of line L6 is one of:

| kind | RAISE(u) | source |
| --- | --- | --- |
| accumulating | $u + 1$ | Sutton 1988 |
| replacing | $1$ | Singh and Sutton 1996 |
| dutch | $(1 - \alpha) u + 1$ | van Seijen and Sutton 2014 |

With $\alpha = 1$ the dutch trace is the replacing trace, and as $\alpha \to 0$ it tends to the accumulating trace. All three agree when no key is visited twice within the life of a trace.

**Why it works.** Take the accumulating trace, $c_t = \gamma\lambda$ and values held fixed during the episode (updates summed and applied at the end). By induction, $z_t(x) = \sum_{k \le t} (\gamma\lambda)^{t-k} \mathbf{1}\{x_k = x\}$. So the total update of key $x$ is

$$\alpha\sum_t \delta_t z_t(x) = \alpha\sum_k \mathbf{1}\{x_k = x\} \sum_{t \ge k} (\gamma\lambda)^{t-k}\delta_t = \alpha\sum_k \mathbf{1}\{x_k = x\}\big(G^\lambda_k - Q(x_k)\big),$$

by exchanging the two finite sums and then using the λ-return identity of the [TD error](/td-error/) page. The proof is on the [TD(λ)](/td-lambda/) page. With general decay factors, the same exchange gives the target $Q(x_k) + \sum_{t \ge k} c_{k+1} \cdots c_t\, \delta_t$ in place of the λ-return.

**Function approximation.** For a value $\hat v(s, w)$ with weights $w$, the trace is a vector of the size of $w$: line L5 becomes $z \leftarrow c_t z$, line L6 becomes $z \leftarrow z + \nabla\hat v(S_t, w)$ for an accumulating trace, and line L8 becomes $w \leftarrow w + \alpha\delta_t z$. With linear features $x_t$, the dutch trace is $z \leftarrow \gamma\lambda z + (1 - \alpha\gamma\lambda\, z^\top x_t)\, x_t$ (Sutton and Barto, Section 12.5). With one-hot features this is the tabular rule of the table above.

**Cost.** Lines L5 and L7 touch every key with a nonzero trace, so a step costs $O(|K|)$ for $|K|$ keys, or $O(d)$ for $d$ weights. With $c_t \le \gamma\lambda < 1$, a trace falls below $\epsilon$ after $\lceil \ln\epsilon / \ln(\gamma\lambda) \rceil$ steps without a visit, so keeping a list of recent keys and dropping the small traces bounds the cost by that number.

**Example.** Take $\gamma\lambda = 1/2$, $\alpha = 1/2$ and the visits A, A, B, A. The traces after each step:

| step | key | accumulating | replacing | dutch |
| --- | --- | --- | --- | --- |
| 1 | A | A 1 | A 1 | A 1 |
| 2 | A | A 3/2 | A 1 | A 5/4 |
| 3 | B | A 3/4, B 1 | A 1/2, B 1 | A 5/8, B 1 |
| 4 | A | A 11/8, B 1/2 | A 1, B 1/2 | A 37/32, B 1/2 |

The accumulating trace of A exceeds 1, and it can grow up to $1/(1 - \gamma\lambda) = 2$ if A is visited at every step. The replacing trace stays at most 1. The dutch trace of step 2 is $(1 - 1/2) \cdot 1/2 + 1 = 5/4$: decay first, then raise.

## Classic examples

- [TD(λ)](/td-lambda/): state keys, the TD error, $c_t = \gamma\lambda$, accumulating traces.
- True online TD(λ): dutch traces with a corrected update, equal to the online λ-return algorithm (van Seijen and Sutton 2014).
- SARSA(λ): pair keys and the [SARSA](/sarsa/) error (Sutton and Barto, Section 12.7).
- [Watkins's Q(λ)](/watkins-q-lambda/): pair keys, the [Q-learning](/q-learning/) error, and $c_t = 0$ after an exploratory action, which cuts all traces.
- Tree backup and [Retrace](/retrace/): $c_t = \gamma\lambda\pi(A_t \mid S_t)$ or $c_t = \gamma\lambda\min(1, \rho_t)$, products that keep the off-policy variance bounded.
- [Actor-critic](/actor-critic/) with traces: one trace for the critic weights and one for the policy weights (Sutton and Barto, Chapter 13).
- [Generalized advantage estimation](/generalized-advantage-estimation/): the same geometric sum of TD errors, computed backward over a stored batch in place of a trace.

## Variations

- **Replacing traces for control.** Singh and Sutton (1996) also set to 0 the traces of the other actions in the current state, so that only the action just taken stays eligible.
- **Traces and Monte Carlo.** With $\lambda = 1$, $\gamma = 1$ and offline updates, TD with replacing traces makes the same total update as first-visit [Monte Carlo](/monte-carlo-policy-evaluation/), and TD with accumulating traces the same as every-visit Monte Carlo (Singh and Sutton 1996). For $\gamma < 1$ the replacing case fails, because a revisit cuts the discounted tail of the first visit.
- **State-dependent λ.** Use $\lambda_t = \lambda(S_t)$ in the decay factor, for example a small $\lambda$ in states whose values are trusted (Sutton and Barto, Section 12.8).
- **Dutch traces for Monte Carlo.** Sutton and Barto (Section 12.6) show that dutch traces give the linear Monte Carlo update online, at a cost per step that does not depend on the episode length.
- **Truncated or windowed traces.** Store the last $n$ keys and drop older ones, a cheap form of the truncated λ-return.

## Pitfalls

- **Raise before decay.** Lines L5 and L6 must decay first and then raise. Raising first gives the current key a trace of $c_t$ instead of 1, and every update is off by one step.
- **Not resetting at the start of an episode.** Line L1 is part of each episode. A trace kept from the last episode gives credit for the new errors to old states.
- **Accumulating traces with a large α.** With $\alpha z(x) > 1$, one update overshoots the target, and repeated visits can make the values diverge. Use replacing or dutch traces, or a smaller $\alpha$.
- **Off-policy data without a cut.** With an exploratory action, the later errors are not about the target policy. Without the cut of Watkins's Q(λ) or the importance factors of [Retrace](/retrace/), the traces mix the two policies.
- **Replacing traces with function approximation.** The replacing rule needs the trace of one key. With general features, use the dutch trace instead; clipping a trace vector is not the same rule.
- **Cost of the sweep.** A naive loop over all keys at every step costs $O(|K|)$ even when few traces are nonzero. Keep the nonzero keys in a list.

## Exercises

1. With $\gamma\lambda = 1/2$, find the accumulating trace of A after the visits A, B, A, B. *Answer:* $1/8 + 1/2 = 5/8$.
2. Show that if a key is visited at every step, the accumulating trace tends to $1/(1-\gamma\lambda)$ and the dutch trace tends to $1/(1 - \gamma\lambda(1-\alpha))$.
3. Give an episode with $\gamma = 1/2$ and $\lambda = 1$ where offline TD with replacing traces and first-visit Monte Carlo make different updates. *Answer:* the states A, A with rewards 0 and 1 and $V = 0$: TD with replacing traces adds $\alpha \cdot 1$ to A (the TD errors are 0 and 1, both with trace 1 at the time), while first-visit MC adds $\alpha G_0 = \alpha/2$.

## References
