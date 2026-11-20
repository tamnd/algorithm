---
tag: 7DNF62
kind: model
slug: bayesian-persuasion
name: Bayesian persuasion
aliases:
- information design
- Kamenica-Gentzkow persuasion
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: A sender commits to a signaling scheme about a state to sway a receiver's action. The optimal scheme is found by concavification or an LP.
prereqs: [bayes-theorem, linear-programming-problem]
see_also: [correlated-equilibrium, stackelberg-equilibrium, automated-mechanism-design, caratheodory-theorem, bayesian-game, revelation-principle, convex-hull, lp-duality]
sources:
  - paper: doi:10.1257/aer.101.6.2590
    title: "Emir Kamenica and Matthew Gentzkow, Bayesian persuasion, American Economic Review 101(6) (2011), 2590-2615"
    locator: "the prosecutor example; Proposition 1 (p. 2595) on recommendation schemes; Corollary 1 (p. 2596) on the value as the concave closure; Corollary 2 (p. 2597) on when the sender benefits"
---

Bayesian persuasion is a model of strategic communication with commitment. A sender knows, or will learn, a payoff-relevant state; a receiver takes an action that affects both of them. Before the state is drawn, the sender commits to a signaling scheme, a rule that maps each state to a random signal. The receiver sees the signal, updates its belief by [Bayes' theorem](/bayes-theorem/) and takes its best action. The sender cannot lie about the scheme and cannot pay the receiver; its only tool is the choice of what information to reveal. Kamenica and Gentzkow (2011) showed that the sender's best value is the concave closure of its value as a function of the receiver's belief, and with finitely many states and actions the optimal scheme is the solution of a small [linear program](/linear-programming-problem/).

## The machine

**Players.** A sender and a receiver. The model extends to several receivers, which is then called information design.

**Primitives.** A finite set $\Omega$ of states with a common prior $\mu_0 \in \Delta(\Omega)$, a finite set $A$ of receiver actions, and utilities $u_R(\omega, a)$ for the receiver and $u_S(\omega, a)$ for the sender. Both utilities depend on the state and the action only, not on the signal.

**Timing.**

1. The sender chooses a signaling scheme $\pi$: a finite signal set $\Sigma$ and, for each state $\omega$, a distribution $\pi(\cdot \mid \omega)$ over $\Sigma$. The scheme is public.
2. Nature draws $\omega \sim \mu_0$.
3. A signal $\sigma \sim \pi(\cdot \mid \omega)$ is drawn and shown to the receiver.
4. The receiver forms the posterior $\mu_\sigma(\omega) = \mu_0(\omega)\, \pi(\sigma \mid \omega) / \Pr[\sigma]$ and takes an action $a^*(\mu_\sigma)$ that maximizes $\sum_\omega \mu_\sigma(\omega)\, u_R(\omega, a)$. Ties are broken in favor of the sender.
5. The payoffs are $u_S(\omega, a)$ and $u_R(\omega, a)$.

**Information.** The receiver knows the prior and the scheme, and sees only the signal. The sender commits before it learns the state, so the scheme cannot depend on the state that occurs except through $\pi(\cdot \mid \omega)$. This commitment is what separates the model from cheap talk.

**Payoffs.** Write $\hat v(\mu) = \sum_\omega \mu(\omega)\, u_S(\omega, a^*(\mu))$ for the sender's expected utility when the receiver holds belief $\mu$. A scheme induces a distribution $\tau$ over posteriors, and the sender's expected utility is $\mathbb{E}_{\mu \sim \tau}[\hat v(\mu)]$.

## What it counts

The quantity of interest is the sender's best expected utility over all schemes,

$$V(\mu_0) = \max_\pi\ \mathbb{E}_\sigma\big[\hat v(\mu_\sigma)\big],$$

and a scheme that attains it. Secondary quantities are the value of persuasion $V(\mu_0) - \hat v(\mu_0)$, the gain over revealing nothing, and the number of signals an optimal scheme needs. In computational work the measure is the time to compute an optimal or near-optimal scheme as a function of $|\Omega|$ and $|A|$, or of a succinct description of the state space.

**Example (the prosecutor).** The state is guilty with prior $0.3$ or innocent with prior $0.7$. A judge convicts if and only if its belief in guilt is at least $\frac{1}{2}$, and acquits otherwise; the prosecutor wants a conviction in every state. With no information the judge acquits, and the prosecutor gets 0. With full information the conviction rate is $0.3$. The optimal scheme sends "convict" always when guilty and with probability $\frac{3}{7}$ when innocent. The posterior after "convict" is $\frac{0.3}{0.3 + 0.7 \cdot 3/7} = \frac{1}{2}$, so the judge convicts, and the conviction rate is $0.3 + 0.3 = 0.6$. The judge is not fooled: it knows the scheme and is exactly indifferent after "convict".

## Relation to other models

- **Mechanism design.** A mechanism designer controls outcomes and payments, given the agents' private information. A persuader controls information, given that the receiver chooses the outcome. Both use a revelation principle and commitment, and both lead to LPs with incentive constraints. [Automated mechanism design](/automated-mechanism-design/) and the persuasion LP are close relatives.
- **Correlated equilibrium.** The obedience constraints of the persuasion LP have the same form as those of a [correlated equilibrium](/correlated-equilibrium/): a mediator recommends actions and nobody wants to deviate. With several receivers, the outcomes that some information structure can induce are the Bayes correlated equilibria of Bergemann and Morris.
- **Stackelberg games.** The sender moves first and commits, so it is a leader in a [Stackelberg](/stackelberg-equilibrium/) sense. The receiver's best response is to the scheme, not to an action of the sender.
- **Cheap talk.** In the model of Crawford and Sobel the sender chooses its message after it learns the state and cannot commit. The equilibria there are partitions of the state space and give the sender less in general. Persuasion is the case of full commitment.
- **Bayesian games.** Fixing a scheme turns the interaction into a [Bayesian game](/bayesian-game/) of the receiver alone, with the signal as its type.

## Known results in the model

**Bayes plausibility (theorem).** A distribution $\tau$ over posteriors can be induced by some scheme if and only if $\mathbb{E}_{\mu \sim \tau}[\mu] = \mu_0$. Necessity is the law of total probability. For sufficiency, given $\tau$ with finite support, send signal $\mu$ in state $\omega$ with probability $\tau(\mu)\, \mu(\omega) / \mu_0(\omega)$; Bayes' theorem then gives posterior $\mu$.

**Concavification (theorem; Kamenica and Gentzkow, Corollary 1).** $V(\mu_0) = \operatorname{cav} \hat v(\mu_0)$, where $\operatorname{cav} \hat v$ is the smallest concave function above $\hat v$, that is $\sup\{z : (\mu_0, z) \in \text{the convex hull of the graph of } \hat v\}$. This follows from Bayes plausibility: the sender picks any distribution of posteriors with mean $\mu_0$, and the best average of $\hat v$ over such distributions is the concave closure. The idea goes back to Aumann and Maschler's work on repeated games with incomplete information. In the prosecutor example, $\hat v(\mu) = \mu$ for $\mu \ge \frac{1}{2}$ and $0$ below, its concave closure is $2\mu$ on $[0, \frac{1}{2}]$, and $V(0.3) = 0.6$.

**When the sender benefits (theorem; Corollary 2).** The sender gains from persuasion, $V(\mu_0) > \hat v(\mu_0)$, if and only if there is a Bayes-plausible distribution of posteriors that does better than the prior, that is if and only if $\hat v$ is not equal to its concave closure at $\mu_0$. For example, if the sender's utility does not depend on the state and the receiver's action at the prior is already the sender's favorite, there is no gain.

**Recommendations suffice (theorem; Proposition 1).** There is an optimal scheme whose signals are action recommendations that the receiver follows, so at most $|A|$ signals are needed. Merging all signals that lead to the same action keeps the posterior mean in the region where that action is optimal, because these regions are convex. By [Carathéodory's theorem](/caratheodory-theorem/), there is also an optimal scheme with at most $|\Omega|$ signals.

**A linear program (theorem).** With recommendations as signals, let $z(\omega, a) = \mu_0(\omega)\, \pi(a \mid \omega)$. Then the optimal scheme is

$$\max \sum_{\omega, a} z(\omega, a)\, u_S(\omega, a) \quad \text{s.t.} \quad \sum_a z(\omega, a) = \mu_0(\omega),\ \ \sum_\omega z(\omega, a) \big(u_R(\omega, a) - u_R(\omega, b)\big) \ge 0,\ \ z \ge 0,$$

for all $\omega$ and all $a \ne b$. It has $|\Omega| |A|$ variables and $|A|(|A| - 1)$ obedience constraints, so it is solved in polynomial time in the explicit input.

```pseudo id=main
PERSUASION-LP(μ0, u_R, u_S)
L1  make variables z(ω, a) ≥ 0, the probability of state ω and recommendation a
L2  for each state ω: add Σ_a z(ω, a) = μ0(ω)    ▷ the signals average back to the prior
L3  for each pair of actions a ≠ b: add Σ_ω z(ω, a) (u_R(ω, a) - u_R(ω, b)) ≥ 0    ▷ obedience
L4  solve: maximize Σ_ω Σ_a z(ω, a) u_S(ω, a)
L5  π(a | ω) ← z(ω, a) / μ0(ω) for each state ω with μ0(ω) > 0
L6  return π and the optimal value
```

The scheme that reveals nothing, with $z(\omega, a^*(\mu_0)) = \mu_0(\omega)$, is always feasible, so the LP is never infeasible. The tests check the LP against a brute-force concave closure for two states, which takes the best chord of $\hat v$ between the points $0$, $1$ and the beliefs where the receiver is indifferent between two actions.

**Aligned interests (theorem).** If $u_S = u_R$, revealing the state fully is optimal, because full information maximizes the receiver's expected utility over all schemes.

**Computation at scale.** When the state space is large and given implicitly, for example as a product of independent components, the explicit LP is too big. Dughmi and Xu (2016) studied this regime and gave both efficient algorithms and hardness results, depending on how the input is represented. With many receivers, private signals and public signals lead to different problems, which is an active research area.

## References
