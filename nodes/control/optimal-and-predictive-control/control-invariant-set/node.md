---
tag: 60KZ9P
kind: definition
slug: control-invariant-set
name: Control invariant set
aliases:
- controlled invariant set
area: control/optimal-and-predictive-control
level: core
summary: A set of states from which some admissible input keeps the state inside the set for all future time.
prereqs: [positively-invariant-set, state-space-representation]
see_also: [maximal-positively-invariant-set, recursive-feasibility, mpc-stability-theorem, controlled-invariant-subspace, control-lyapunov-function, fourier-motzkin-elimination, reachable-set-computation, tube-mpc]
sources:
  - paper: doi:10.1016/S0005-1098(99)00113-2
    title: Franco Blanchini, Set invariance in control, Automatica 35(11), 1747-1767, 1999
    locator: the survey of controlled invariant sets, their computation by the backward recursion, and their use in constrained control
  - book: isbn:9783319179322
    title: Franco Blanchini and Stefano Miani, Set-Theoretic Methods in Control, 2nd edition, Birkhäuser, 2015
    locator: the chapters on controlled invariant sets and on the computation of the largest controlled invariant set
  - book: "Jean-Pierre Aubin, Viability Theory, Birkhäuser, 1991"
    locator: the definition of viable sets and of the viability kernel of a closed set under a set-valued dynamics
  - book: isbn:9781107016880
    title: Francesco Borrelli, Alberto Bemporad and Manfred Morari, Predictive Control for Linear and Hybrid Systems, Cambridge University Press, 2017
    locator: the chapter on invariant sets, with the predecessor set, the maximal control invariant set and the controllable sets
---

A control invariant set of a system with an input is a set of states from which the state can be kept inside the set forever, by a suitable choice of admissible inputs. It is the controlled version of a [positively invariant set](/positively-invariant-set/): there the system has no choice, here the controller has one, and the definition asks only that a good choice exists at each state. Control invariant sets inside the state constraints are the safe sets of constrained control. In model predictive control they make the problem [recursively feasible](/recursive-feasibility/), and they are the terminal sets of the [MPC stability theorem](/mpc-stability-theorem/).

## Definition

Let $x_{k+1} = f(x_k, u_k)$ be a discrete-time system with state constraints $x \in \mathbb{X}$ and input constraints $u \in \mathbb{U}$. A set $\mathcal{C} \subseteq \mathbb{X}$ is **control invariant** if

$$\forall x \in \mathcal{C} \ \ \exists u \in \mathbb{U} : \ f(x, u) \in \mathcal{C}.$$

With the predecessor set $\operatorname{Pre}(\mathcal{C}) = \{x : \exists u \in \mathbb{U},\ f(x, u) \in \mathcal{C}\}$, the condition is $\mathcal{C} \subseteq \operatorname{Pre}(\mathcal{C}) \cap \mathbb{X}$. If $\mathcal{C}$ is control invariant, a choice $u = \kappa(x)$ of such inputs is a feedback law, maybe nonlinear and not continuous, that makes $\mathcal{C}$ positively invariant for the closed loop and meets all constraints.

The union of control invariant subsets of $\mathbb{X}$ is again control invariant. So there is a largest one, the **maximal control invariant set** $\mathcal{C}_\infty$: the set of initial states for which some admissible input sequence keeps the state in $\mathbb{X}$ forever. It is the limit of the backward recursion

$$\mathcal{C}_0 = \mathbb{X}, \qquad \mathcal{C}_{k+1} = \operatorname{Pre}(\mathcal{C}_k) \cap \mathbb{X},$$

in the sense that $\mathcal{C}_\infty \subseteq \mathcal{C}_k$ for all $k$, with equality to $\bigcap_k \mathcal{C}_k$ under compactness and continuity assumptions. If $\mathcal{C}_{k+1} = \mathcal{C}_k$ for some $k$, then $\mathcal{C}_\infty = \mathcal{C}_k$. For linear systems with polyhedral $\mathbb{X}$ and $\mathbb{U}$, each $\operatorname{Pre}$ is the projection of a polyhedron, computed for example by [Fourier-Motzkin elimination](/fourier-motzkin-elimination/), but the recursion need not stop.

## Examples and non-examples

- **A scalar unstable plant.** Take $x_{k+1} = 2 x_k + u_k$, $|u| \le 1$, $\mathbb{X} = [-5, 5]$. The set $[-1, 1]$ is control invariant: $u = -x$ is admissible there and gives $x_{k+1} = x_k$. It is the maximal one: for $|x| > 1$, every admissible input gives $|x_{k+1}| \ge 2|x| - 1 > |x|$, and the distance $|x| - 1$ doubles at each step until the state leaves $\mathbb{X}$. The recursion gives $\mathcal{C}_k = [-a_k, a_k]$ with $a_{k+1} = (a_k + 1)/2$, so $a_k = 1 + 2^{2-k}$: $5, 3, 2, 1.5, \dots$. It converges to $[-1, 1]$ but never reaches it, so here the recursion does not stop after finitely many steps.
- **Non-example.** In the same system, $[-2, 2]$ is not control invariant: from $x = 2$, every admissible input gives $x_{k+1} \ge 3$.
- **Positively invariant sets of an admissible feedback.** If $u = K x$ meets the input limits on a set $\Omega \subseteq \mathbb{X}$ and $\Omega$ is positively invariant for $x_{k+1} = (A + B K) x_k$, then $\Omega$ is control invariant. The [maximal positively invariant set](/maximal-positively-invariant-set/) of the LQR closed loop, with the input limits added as outputs, is the usual example and the usual terminal set of [linear MPC](/linear-mpc/).
- **Sublevel sets of a control Lyapunov function.** If for every $x$ in $\{V \le \alpha\} \subseteq \mathbb{X}$ some $u \in \mathbb{U}$ gives $V(f(x, u)) \le V(x)$, then $\{V \le \alpha\}$ is control invariant (theorem, by the same argument as for Lyapunov sublevel sets). See [control Lyapunov function](/control-lyapunov-function/).
- **The feasible set of MPC.** If the terminal set $\mathbb{X}_f$ is control invariant, the set of states from which the MPC problem with horizon $N$ is feasible is control invariant too (theorem); this is the core of [recursive feasibility](/recursive-feasibility/).
- **Non-example: one step is not enough.** A set $\mathcal{C}$ with $\mathcal{C} \subseteq \operatorname{Pre}(\mathbb{X})$ only guarantees one admissible step. The first set of the recursion above, $[-3, 3] = \operatorname{Pre}(\mathbb{X}) \cap \mathbb{X}$, is not control invariant: from $x = 3$ the next state is at least 5, and from there at least 9.

## Related definitions

- **Positively invariant set.** The same property for a system without an input; see [positively invariant set](/positively-invariant-set/).
- **Viability kernel.** In viability theory (Aubin 1991), the dynamics is often a differential inclusion or a set-valued map, and the viability kernel of a closed set $K$ is the set of initial states from which at least one solution stays in $K$ forever. For the discrete-time system above with $K = \mathbb{X}$ and the inputs in $\mathbb{U}$, it is the maximal control invariant set $\mathcal{C}_\infty$. The difference is one of emphasis: a control invariant set is any set with the property, and there are many; the viability kernel is the single largest one, attached to a given constraint set.
- **Controlled invariant subspace.** In geometric control, a subspace $\mathcal{V}$ is a [controlled invariant subspace](/controlled-invariant-subspace/) of $x_{k+1} = A x_k + B u_k$ if $A \mathcal{V} \subseteq \mathcal{V} + \operatorname{im} B$, which is the same as $(A + B F) \mathcal{V} \subseteq \mathcal{V}$ for some linear $F$. It is a control invariant set for unconstrained inputs, with two extra features: the set is a linear subspace, and a linear feedback is enough. A bounded constraint set contains no subspace other than $\{0\}$, so with constraints the two notions part ways: control invariant sets are then bounded, usually polyhedral or ellipsoidal, and may need a nonlinear feedback.
- **Robust control invariant set.** For $x_{k+1} = f(x_k, u_k, w_k)$ with $w_k \in \mathbb{W}$, a set is robust control invariant if for each state in it some admissible input keeps the next state in it for every disturbance. It is used in [tube MPC](/tube-mpc/) and [min-max MPC](/min-max-mpc/).
- **$N$-step controllable set.** The set $\mathcal{K}_N(\mathcal{T})$ of states that some admissible input sequence brings into a target set $\mathcal{T}$ in $N$ steps while meeting the constraints. With $\mathcal{T} = \mathbb{X}_f$ it is the feasible set of MPC. If $\mathcal{T}$ is control invariant, then $\mathcal{K}_N(\mathcal{T})$ is control invariant and grows with $N$.
- **Reachable set.** The forward counterpart: the set of states that can be reached from a given initial set; see [reachable set computation](/reachable-set-computation/).

## References
