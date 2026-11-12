---
tag: 8STJSN
kind: algorithm
slug: td-lambda
name: TD(lambda)
aliases:
- lambda-return
- TD(lambda) learning
- backward view of TD(lambda)
area: machine-learning/reinforcement-learning
level: advanced
summary: "Learn V toward the lambda-return, a geometric mix of n-step returns. Traces give the same total update offline, step by step, without waiting for the end."
solves: [policy-evaluation]
model: real-ram
complexity:
  vars: {T: the total number of steps, S: the number of states}
  time: {worst: "O(S T)"}
  space: {extra: "O(S)"}
properties: {deterministic: true, online: true, exact: false, recursive: false}
history:
  year: 1988
  people: [Richard S. Sutton]
  note: Sutton defined TD(lambda) with eligibility traces and showed that with lambda = 1 it makes the same total update as the Widrow-Hoff rule on the full return.
prereqs: [n-step-td, eligibility-traces, td-error]
see_also: [temporal-difference-learning, watkins-q-lambda, generalized-advantage-estimation, retrace, monte-carlo-policy-evaluation, value-function-approximation]
sources:
  - paper: doi:10.1007/BF00115009
    title: "Richard S. Sutton, Learning to predict by the methods of temporal differences, Machine Learning 3(1), 1988, pages 9 to 44"
    locator: the definition of TD(lambda) with traces and the equivalence of TD(1) and the Widrow-Hoff rule
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 12.1 (the lambda-return and the offline lambda-return algorithm), Section 12.2 (TD(lambda) with accumulating traces) and Section 12.5 (true online TD(lambda))
  - paper: "Harm van Seijen and Richard S. Sutton, True online TD(lambda), Proceedings of the 31st International Conference on Machine Learning (ICML 2014), PMLR 32(1), pages 692 to 700"
    locator: the true online TD(lambda) algorithm and its equivalence to the online lambda-return algorithm
  - paper: "Peter Dayan, The convergence of TD(lambda) for general lambda, Machine Learning 8(3-4), 1992, pages 341 to 362"
    locator: the convergence of TD(lambda) for all lambda
  - paper: "Tommi Jaakkola, Michael I. Jordan and Satinder P. Singh, On the convergence of stochastic iterative dynamic programming algorithms, Neural Computation 6(6), 1994, pages 1185 to 1201"
    locator: the convergence with probability 1 of online tabular TD(lambda)
---

TD(λ) is the [policy evaluation](/policy-evaluation/) method that moves $V(S_t)$ toward the λ-return $G^\lambda_t$, the average of all [n-step returns](/n-step-td/) with weights $(1-\lambda)\lambda^{n-1}$. The *forward view* states this target; the *backward view* computes it online with [eligibility traces](/eligibility-traces/): each [TD error](/td-error/) $\delta_t$ updates every state in proportion to its trace. When the values are held fixed during an episode, the two views make exactly the same total update (Sutton 1988; Sutton and Barto, Sections 12.1 and 12.2). The parameter $\lambda \in [0, 1]$ moves the method from [TD(0)](/temporal-difference-learning/) at $\lambda = 0$ to every-visit [Monte Carlo](/monte-carlo-policy-evaluation/) at $\lambda = 1$.

## In plain words

n-step TD makes you choose how far ahead to look. TD(λ) does not choose: it mixes all look-ahead lengths, giving the most weight to short ones and less and less weight to longer ones. The parameter lambda sets how fast the weight drops.

This mix would seem to need the whole future. The trick is to turn it around. Each place you visit keeps a fading mark, its trace. At each step you get a one-step surprise, the TD error, and you hand it out to all the marked places, more to the places with stronger marks. Recent places get much of it, old places get little. Added up over an episode, this gives the same result as the mix of look-ahead lengths.

## The problem

The setting is that of [TD(0)](/temporal-difference-learning/): an unknown MDP, a fixed policy $\pi$, the discounted criterion with $0 \le \gamma \le 1$ (with $\gamma = 1$ only if episodes end), and the goal $V^\pi$. Episodes are the pairs $(S_t, R_{t+1})$, $t < T$, with $V(S_T) = 0$. For $0 \le \lambda \le 1$ the **λ-return** is

$$G^\lambda_t = (1 - \lambda) \sum_{n=1}^{T-t-1} \lambda^{n-1} G_{t:t+n} + \lambda^{T-t-1} G_t ,$$

where $G_{t:t+n}$ is the $n$-step return and $G_t$ the full return. The weights sum to 1. With $\lambda = 0$ it is the one-step target $R_{t+1} + \gamma V(S_{t+1})$, and with $\lambda = 1$ it is $G_t$. It satisfies the recursion $G^\lambda_t = R_{t+1} + \gamma\big((1-\lambda) V(S_{t+1}) + \lambda G^\lambda_{t+1}\big)$ with $G^\lambda_T = 0$.

The **offline λ-return algorithm** (the forward view) adds $\alpha(G^\lambda_t - V(S_t))$ to $V(S_t)$ for each $t$ at the end of the episode, with the targets computed from the values of the start of the episode.

## The algorithm

The backward view with accumulating traces:

```pseudo id=main
TD-LAMBDA(episodes, λ, α, γ, V, offline)
L1  for each episode (S_0, R_1), ..., (S_{T−1}, R_T) do
L2      z(s) ← 0 and Δ(s) ← 0 for each state s
L3      for t ← 0 to T − 1 do
L4          δ ← R_{t+1} + γ V(S_{t+1}) − V(S_t)          ▷ V(S_T) = 0
L5          z(s) ← γλ z(s) for each s;  z(S_t) ← z(S_t) + 1
L6          for each state s with z(s) ≠ 0 do
L7              if offline then Δ(s) ← Δ(s) + α δ z(s) else V(s) ← V(s) + α δ z(s)
L8      if offline then V(s) ← V(s) + Δ(s) for each state s
L9  return V
```

Line L4 computes the one-step [TD error](/td-error/). Line L5 decays all traces by $\gamma\lambda$ and adds 1 to the trace of the current state (an accumulating trace). Line L7 gives each state its share $\alpha \delta z(s)$ of the error. In the online form (the usual TD(λ)) the values change at once, so later TD errors use the new values. In the offline form the values stay fixed until line L8, and then the total update equals the forward view exactly. Other trace rules, replacing and dutch, are on the [eligibility traces](/eligibility-traces/) page.

## Example

The random walk A to E of the [TD(0)](/temporal-difference-learning/) page, with $\gamma = 1$, $V = 1/2$ everywhere, $\alpha = 1/10$ and $\lambda = 1/2$, and the episode C, B, C, D, E, then right with reward 1. All TD errors are 0 except the last one, $\delta_4 = 1 - 1/2 = 1/2$. The traces at $t = 4$, and the updates:

| state | visits | $z_4(s)$ | update $\alpha \delta_4 z_4(s)$ | new $V(s)$ |
| --- | --- | --- | --- | --- |
| E | $t = 4$ | $1$ | $1/20$ | $0.55$ |
| D | $t = 3$ | $1/2$ | $1/40$ | $0.525$ |
| C | $t = 0, 2$ | $(1/2)^4 + (1/2)^2 = 5/16$ | $1/64$ | $0.515625$ |
| B | $t = 1$ | $(1/2)^3 = 1/8$ | $1/160$ | $0.50625$ |

The forward view gives the same numbers. The λ-returns are $G^\lambda_0 = 17/32$ (C), $G^\lambda_1 = 9/16$ (B), $G^\lambda_2 = 5/8$ (C), $G^\lambda_3 = 3/4$ (D) and $G^\lambda_4 = 1$ (E). For C the two visits give $\alpha\big((17/32 - 1/2) + (5/8 - 1/2)\big) = \alpha \cdot 5/32 = 1/64$, the same as the trace update. TD(0) on this episode changes only E; TD(λ) sends the reward back along the whole path, with geometric decay.

Online and offline differ once several TD errors are nonzero. After this episode and the episode C, D, E, D, C, B, A, left, online TD(λ) gives $V(\mathrm{C}) = 0.50237$ and offline gives $0.50246$. D and E also differ in the fourth decimal ($0.51655$ and $0.54382$ online, $0.51648$ and $0.54359$ offline), while A $= 0.45$ and B $= 0.48063$ agree.

## Correctness

**Offline equivalence.** With $V$ fixed during an episode, for each state $s$,

$$\sum_{t=0}^{T-1} \alpha\, \delta_t\, z_t(s) = \sum_{t=0}^{T-1} \alpha \big(G^\lambda_t - V(S_t)\big)\, \mathbf{1}\{S_t = s\}.$$

The reason: the trace is $z_t(s) = \sum_{k \le t} (\gamma\lambda)^{t-k} \mathbf{1}\{S_k = s\}$, so exchanging the two sums gives $\sum_k \mathbf{1}\{S_k = s\} \sum_{t \ge k} (\gamma\lambda)^{t-k} \delta_t$, and the inner sum is $G^\lambda_k - V(S_k)$ by the λ-return identity of the [TD error](/td-error/) page. The proofs section proves the recursion, the identity and the exchange. For $\lambda = 1$ this is Sutton's (1988) result that TD(1) makes the same total update as the Monte Carlo rule with every visit counted.

**Convergence.** The expected λ-return target is $(T^\pi)^{(\lambda)} V = (1 - \lambda) \sum_n \lambda^{n-1} (T^\pi)^n V$, a contraction with modulus $\gamma(1-\lambda)/(1 - \gamma\lambda) \le \gamma$ whose fixed point is $V^\pi$. Online tabular TD(λ) converges to $V^\pi$ with probability 1 when each state is visited infinitely often and the steps meet the [Robbins-Monro conditions](/robbins-monro-conditions/) (Dayan 1992 for convergence in the mean, Jaakkola, Jordan and Singh 1994 and Dayan and Sejnowski 1994 with probability 1). With linear function approximation and on-policy sampling, Tsitsiklis and Van Roy (1997) proved convergence to a fixed point whose error is at most $(1 - \gamma\lambda)/(1-\gamma)$ times the best error in the span of the features.

## Complexity

Line L5 and the loop of line L6 touch every state with a nonzero trace, so a step costs $O(|S|)$ in the worst case and an episode of $T$ steps costs $O(|S| T)$. With $\gamma\lambda < 1$, traces fall below a threshold $\epsilon$ after $\lceil \ln \epsilon / \ln(\gamma\lambda) \rceil$ steps without a visit, so a list of the recent states, cut at that age, makes the cost per step $O(\min(|S|, \ln(1/\epsilon)/\ln(1/(\gamma\lambda))))$ at a small loss of accuracy. The memory is two tables of size $|S|$. The forward view needs the whole episode and $O(T^2)$ time if each λ-return is summed directly, or $O(T)$ by the backward recursion.

## Properties

- **One parameter from TD(0) to MC.** $\lambda = 0$ gives TD(0) exactly; offline $\lambda = 1$ gives every-visit constant-$\alpha$ MC exactly.
- **No delay.** The backward view uses only the past, so it learns from each step at once, unlike [n-step TD](/n-step-td/) and the forward view.
- **Online is not the forward view.** With online updates, the values change during the episode, and online TD(λ) differs slightly from both the offline and the online λ-return algorithms.
- **Markov sensitivity falls with λ.** Larger $\lambda$ relies less on bootstrapping, so it is less hurt by non-Markov states, at the price of more variance.

## Variants and improvements

- **True online TD(λ).** van Seijen and Sutton (2014) gave an algorithm with dutch traces whose online updates equal those of the *online* λ-return algorithm exactly, for linear function approximation, at the same $O(d)$ cost per step (Sutton and Barto, Section 12.5). Its tabular case uses the dutch trace of the [eligibility traces](/eligibility-traces/) page.
- **Replacing traces.** Reset the trace of the current state to 1 instead of adding 1. Offline TD(1) with replacing traces equals first-visit MC (Singh and Sutton 1996).
- **Control.** SARSA(λ) uses traces on state action pairs; [Watkins's Q(λ)](/watkins-q-lambda/) cuts the traces after an exploratory action; Peng's Q(λ) does not cut them.
- **Off-policy traces.** Tree backup, [Retrace](/retrace/) and [V-trace](/v-trace/) multiply the traces by truncated importance ratios.
- **Advantage estimation.** [Generalized advantage estimation](/generalized-advantage-estimation/) is the λ-return identity applied to the TD errors of a critic.
- **Truncated λ-return.** Cut the λ-return after a fixed horizon, as in Sutton and Barto, Section 12.3, to use it with a buffer instead of traces.

## When to use it

Use TD(λ) when rewards are delayed and [TD(0)](/temporal-difference-learning/) propagates them too slowly, but full Monte Carlo returns are too noisy. In the random walk experiments of Sutton and Barto (Sections 12.1 and 12.2), intermediate values of $\lambda$ give the lowest error, neither 0 nor 1, but the best value depends on the task and on $\alpha$. With function approximation prefer true online TD(λ). With large tables where the trace sweep is too costly, cut small traces, or use [n-step TD](/n-step-td/).

## Pitfalls

- **Decay and increment in the wrong order.** Line L5 decays by $\gamma\lambda$ first and then adds 1. Adding first and then decaying gives the current state a trace of $\gamma\lambda$, not 1, and shifts every update by one step.
- **Traces that survive the episode.** Line L2 must reset the traces at the start of each episode. Old traces would credit states of the last episode with the new TD errors.
- **Forgetting the discount in the trace.** The decay factor is $\gamma\lambda$, not $\lambda$. With $\lambda$ alone the method is no longer the λ-return of the discounted problem.
- **Accumulating traces with large α.** A state visited many times in a row gets a trace above 1, and $\alpha z(s) > 1$ overshoots. Replacing or dutch traces avoid this; see [eligibility traces](/eligibility-traces/).
- **Expecting the online result to equal the forward view.** The exact equivalence holds offline only. Use true online TD(λ) when the online equivalence matters.

## Implementations

## History

Sutton (1988) introduced TD(λ) with the trace update and showed the equivalence of TD(1) with the Widrow-Hoff rule. Watkins (1989) introduced the λ-return view and the forward view; Sutton and Barto present the forward and backward views and their offline equivalence in Sections 12.1 and 12.2. Dayan (1992), Dayan and Sejnowski (1994) and Jaakkola, Jordan and Singh (1994) proved convergence; Singh and Sutton (1996) introduced replacing traces, and van Seijen and Sutton (2014) introduced true online TD(λ).

## References
