---
tag: J62EG8
kind: technique
slug: quasi-steady-state-approximation
name: Quasi-steady-state approximation
aliases:
- QSSA
area: biology/systems-biology
level: core
summary: Reduce a stiff kinetic model by setting the derivatives of fast intermediate species to zero and solving for them algebraically.
prereqs: [mass-action-kinetics, stiff-ode-problem]
see_also: [michaelis-menten-kinetics, hill-equation, chemical-reaction-network, runge-kutta-methods, backward-euler-method, jacobian-linearization, gillespie-algorithm, gene-regulatory-network]
sources:
  - paper: doi:10.1137/1031091
    title: Lee A. Segel and Marshall Slemrod, The quasi-steady-state assumption, a case study in perturbation, SIAM Review 31(3), 1989, 446-477
    locator: the time scales t_c and t_s of the enzyme scheme, the parameter E_T / (S_0 + K_M), the inner and outer solutions, and the reverse QSSA
  - paper: doi:10.1042/bj0190338
    title: George Edward Briggs and John Burdon Sanderson Haldane, A note on the kinetics of enzyme action, Biochemical Journal 19(2), 1925, 338-339
    locator: the steady state assumption for the enzyme-substrate complex
  - paper: doi:10.1007/BF02458281
    title: José A. M. Borghans, Rob J. de Boer and Lee A. Segel, Extending the quasi-steady state approximation by changing variables, Bulletin of Mathematical Biology 58(1), 1996, 43-63
    locator: the total QSSA with the total substrate S + C as the slow variable, and its validity when the enzyme is not scarce
  - paper: "Leonor Michaelis and Maud L. Menten, Die Kinetik der Invertinwirkung, Biochemische Zeitschrift 49, 1913, 333-369"
    title: Michaelis and Menten 1913
    locator: the rapid equilibrium assumption for the binding of the enzyme and the substrate
---

The quasi-steady-state approximation (QSSA) reduces a kinetic model with fast and slow parts. Some species, usually short-lived intermediates such as an enzyme-substrate complex, change much faster than the others. After a short start, they follow the slow species closely. The QSSA sets the time derivatives of these fast species to zero, solves the resulting algebraic equations for them, and puts the solution into the equations of the slow species. The result has fewer variables and no fast time scale. [Michaelis-Menten kinetics](/michaelis-menten-kinetics/) is the classic result. The approximation has conditions, and it fails when they do not hold.

## In plain words

Think of a small bucket under a tap, with a hole in its bottom. The water level in the bucket adjusts within seconds to the flow from the tap. If the tap turns slowly over hours, the level at each moment is the level at which outflow equals inflow for the current tap setting. So to follow the bucket you do not need its own equation; you need the balance "outflow = inflow" and the tap.

In a reaction network, the fast species is the bucket. Its derivative is not zero, but it is small against the rates that make and use it. Setting it to zero replaces a differential equation by an algebraic one.

## When it applies

- The model has a clear separation of time scales: the fast species relax in a time $t_c$ much shorter than the time $t_s$ over which the slow species change. For the enzyme scheme, Segel and Slemrod (1989) give $t_c = 1/(k_1 (S_0 + K_M))$ and $t_s = (S_0 + K_M)/(k_2 E_T)$, and the condition $\varepsilon = E_T/(S_0 + K_M) \ll 1$.
- The fast subsystem, with the slow species held fixed, has a stable equilibrium, and the state starts in its basin of attraction. Then the fast species are attracted to the slow manifold, the set where their derivatives are zero. Tikhonov's theorem on singular perturbations (1952) gives the convergence as the ratio of the time scales goes to zero.
- The fast species hold a small part of the conserved amounts, or the slow variable is chosen so that the fast reactions do not change it. If a lot of substrate sits in the complex, use the total substrate as the slow variable (the total QSSA below).
- The question is about times after the fast start. The QSSA does not describe the first instants, the *initial layer*, of length about $t_c$.

## The template

The state is split into slow variables $x$ and fast variables $y$, with $\dot x = f(x, y)$ and $\dot y = g(x, y)$.

```pseudo id=main
QSSA-REDUCE(f, g, x0)
L1  choose the fast variables y and slow variables x, so that the fast reactions do not change x
L2  solve g(x, y) = 0 for y = h(x)                  ▷ the slow manifold
L3  check that every eigenvalue of ∂g/∂y at (x, h(x)) has a negative real part
L4  form the reduced model dx/dt = f(x, h(x))
L5  start it at x(0) = x0; the fast variables start at h(x0) after the initial layer
L6  check the reduction: compare with the full model, or bound the ratio of time scales
L7  return the reduced model and the range of parameters where L6 holds
```

Line L3 is the condition of stability of the fast subsystem: the [Jacobian](/jacobian-linearization/) $\partial g/\partial y$ must be stable, or the full state moves away from the slow manifold. Line L1 matters for the error. If the fast reactions change $x$, the start $x(0) = x_0$ of the reduced model is wrong by the amount that moves into $y$ during the initial layer.

The full model with $t_c \ll t_s$ is a [stiff problem](/stiff-ode-problem/). An explicit [Runge-Kutta method](/runge-kutta-methods/) on it needs a step of the order of $t_c$ for the whole run. The reduced model has only the slow time scale, so it allows a step of the order of $t_s$. An implicit method such as [backward Euler](/backward-euler-method/) on the full model is the other way to handle the stiffness without the approximation.

## Classic examples

**Michaelis-Menten.** The scheme $E + S \rightleftharpoons C \to E + P$ with $e = E_T - c$ has the slow variable $s$ and the fast variable $c$. Line L2 gives $k_1 (E_T - c) s = (k_{-1} + k_2) c$, so $c = h(s) = E_T s/(K_M + s)$ with $K_M = (k_{-1} + k_2)/k_1$. Line L3: $\partial \dot c/\partial c = -(k_1 s + k_{-1} + k_2) < 0$. Line L4 gives $\dot s = -k_2 E_T s/(K_M + s)$, the Michaelis-Menten law.

Take $k_1 = 1$ per mM per second, $k_{-1} = k_2 = 1$ per second (so $K_M = 2$ mM), and $S_0 = 10$ mM. The table compares the free substrate $s$ (in mM) of the full model (a Runge-Kutta solution with step $0.001$ s), of the standard QSSA above (sQSSA), and of the total QSSA (tQSSA) below:

| $E_T$ (mM) | $\varepsilon$ | $t$ (s) | full | sQSSA | tQSSA |
|---|---|---|---|---|---|
| 0.1 | 0.0083 | 10 | 9.0987 | 9.1727 | 9.0920 |
| 0.1 | 0.0083 | 50 | 5.9547 | 6.0162 | 5.9493 |
| 0.1 | 0.0083 | 100 | 2.6197 | 2.6534 | 2.6185 |
| 1 | 0.083 | 5 | 5.4185 | 6.0162 | 5.3704 |
| 1 | 0.083 | 10 | 2.3372 | 2.6534 | 2.3366 |
| 10 | 0.83 | 0.5 | 1.9520 | 6.0162 | 2.0551 |
| 10 | 0.83 | 1 | 0.9241 | 2.6534 | 1.1927 |

For $E_T = 0.1$ mM, $t_c = 0.083$ s and $t_s = 120$ s. The complex reaches its largest value $0.0831$ mM at $t = 0.76$ s, close to the quasi-steady value $h(10) = 0.0833$ mM, and the sQSSA is within about 1.3 percent at $t = 100$ s. Most of the error is the substrate that went into the complex in the initial layer. For $E_T = 10$ mM, $\varepsilon = 0.83$ is not small, $t_s = 1.2$ s is only 14 times $t_c$, and the sQSSA is wrong by a factor of 3 at $t = 0.5$ s.

**Promoter binding in a gene circuit.** A transcription factor binds and leaves a promoter in seconds, while the protein levels change over minutes to hours. The QSSA (here a rapid equilibrium, see below) on the bound fraction gives a [Hill function](/hill-equation/) as the production rate. The models of the [genetic toggle switch](/genetic-toggle-switch/) and the [repressilator](/repressilator/) are reduced in this way. A second reduction often removes the mRNA when it is much shorter-lived than the protein.

## Variations

- **Rapid equilibrium.** Assume that the fast reactions are at equilibrium, not only that the fast species are steady. For the enzyme scheme this is $k_1 e s = k_{-1} c$, the assumption of Michaelis and Menten (1913), with $K_S = k_{-1}/k_1$ in place of $K_M$. It needs the extra condition $k_2 \ll k_{-1}$.
- **Total QSSA (Borghans, de Boer and Segel 1996).** Take the total substrate $\bar s = s + c$ as the slow variable. The binding and release do not change it, so line L1 holds. The quasi-steady complex solves $k_1(E_T - c)(\bar s - c) = (k_{-1} + k_2) c$, the root $c = \tfrac12\big(E_T + K_M + \bar s - \sqrt{(E_T + K_M + \bar s)^2 - 4 E_T \bar s}\big)$, and $\dot{\bar s} = -k_2 c$. The table shows that for $E_T = 10$ mM it is much closer to the full model than the sQSSA (5 percent off at $t = 0.5$ s, against a factor of 3), and that it is also better for $E_T = 0.1$ and $1$ mM. The table reports the free substrate $\bar s - c$.
- **Reverse QSSA.** When the enzyme is in large excess and the substrate is scarce, the substrate can be the fast variable instead (Segel and Slemrod 1989).
- **Stochastic use.** Gillespie simulations sometimes use the reduced rate law as a propensity, for example $a(s) = V_{\max} s/(K_M + s)$ for the conversion. This is a second approximation on top of the first, and it needs its own check against the full stochastic model. It can fail even when the deterministic QSSA is good.

## Pitfalls

- **The wrong condition.** $E_T \ll S_0$ is the usual statement in textbooks, but the relevant parameter is $\varepsilon = E_T/(S_0 + K_M)$. The table above uses $S_0 = 10$ mM, so $E_T = 1$ mM satisfies $E_T \ll S_0$ only weakly, and the sQSSA is 11 percent off at $t = 5$ s.
- **The fast species is not constant.** The QSSA does not say that $c$ is constant. It says that $\dot c$ is small against the rates that make and use $c$, so $c$ follows $h(s(t))$ as $s$ changes. In the example $c$ falls from $0.083$ to $0.057$ mM between $t = 0$ and $t = 100$ s.
- **The initial layer.** The reduced model cannot satisfy both $s(0) = S_0$ and $c(0) = 0$. Started at $s(0) = S_0$, it ignores the substrate that binds in the first instants. For a scarce enzyme this is a small error; otherwise use the total QSSA.
- **An unstable fast subsystem.** If $\partial g/\partial y$ has an eigenvalue with a positive real part, the slow manifold repels the state and the reduced model is wrong. If $g = 0$ has several roots, pick the stable branch, and watch for points where the branch folds and the state jumps.
- **Mass is not kept exactly.** The reduced model keeps the slow variable's balance, but the amount in the fast species is implicit. Sums such as $s + c + p$ are not conserved exactly by the reduced variables.
- **A good fit is not a proof.** A reduced model that fits data well does not show that the scheme has two time scales. The condition must be checked from the rate constants.

## Exercises

1. For the scheme $A \rightleftharpoons B$ (rates $k_1$, $k_{-1}$, both large) followed by $B \to C$ (rate $k_2$, small), apply the template with $A + B$ as the slow variable, and give the reduced rate of $C$ formation.
2. Derive $t_c$ and $t_s$ for the enzyme scheme from the linearized equation of $c$ and from $S_0$ divided by the largest rate $V_{\max}$.
3. Show that the root of the total QSSA tends to the sQSSA value $E_T s/(K_M + s)$ when $E_T \ll \bar s + K_M$.
4. A gene with mRNA $m$ (lifetime 2 min) and protein $p$ (lifetime 60 min) has $\dot m = \beta - m/2$ and $\dot p = \kappa m - p/60$. Apply the QSSA to $m$, and find the error of $p$ at $t = 10$ min from $m = p = 0$.
5. Give a network in which $\partial g/\partial y$ has a positive eigenvalue on part of the slow manifold, and describe what the full model does there.

## References
