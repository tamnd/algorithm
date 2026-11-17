---
tag: 0X4Y7W
kind: model
slug: michaelis-menten-kinetics
name: Michaelis-Menten kinetics
aliases:
- Michaelis-Menten equation
area: biology/systems-biology
level: intro
summary: The rate law v = Vmax S / (Km + S) of an enzyme reaction, derived from mass action with a quasi-steady enzyme-substrate complex.
history:
  year: 1913
  people: [Leonor Michaelis, Maud Menten, G. E. Briggs, J. B. S. Haldane]
  note: Michaelis and Menten derived the rate law in 1913 with a fast binding equilibrium. Briggs and Haldane derived it in 1925 with a steady state of the complex, which gives the modern K_M.
prereqs: [mass-action-kinetics, quasi-steady-state-approximation]
see_also: [hill-equation, chemical-reaction-network, stoichiometric-matrix, stiff-ode-problem, newton-raphson-method, deficiency-zero-theorem, linear-regression, gene-regulatory-network]
sources:
  - paper: "Leonor Michaelis and Maud L. Menten, Die Kinetik der Invertinwirkung, Biochemische Zeitschrift 49, 1913, 333-369"
    title: Michaelis and Menten 1913
    locator: the rate of sucrose hydrolysis by invertase as a function of the sucrose concentration, with a fast equilibrium between the enzyme and the enzyme-sucrose complex
  - paper: doi:10.1042/bj0190338
    title: George Edward Briggs and John Burdon Sanderson Haldane, A note on the kinetics of enzyme action, Biochemical Journal 19(2), 1925, 338-339
    locator: the steady state of the complex, which gives K_M = (k_(-1) + k_2) / k_1
  - paper: doi:10.1137/1031091
    title: Lee A. Segel and Marshall Slemrod, The quasi-steady-state assumption, a case study in perturbation, SIAM Review 31(3), 1989, 446-477
    locator: the fast and slow time scales of the enzyme scheme and the condition E_T / (S_0 + K_M) much less than 1
  - book: isbn:9781439837177
    title: Uri Alon, An Introduction to Systems Biology, Design Principles of Biological Circuits, 2nd edition, CRC Press, 2019
    locator: Appendix A, the input functions of genes (Michaelis-Menten and Hill equations)
---

Michaelis-Menten kinetics is the rate law of a reaction $S \to P$ that an enzyme $E$ catalyzes. When the enzyme is much less abundant than the substrate, the rate of product formation is
$$v = \frac{V_{\max}\, [S]}{K_M + [S]}, \qquad V_{\max} = k_{\text{cat}}\, [E]_T,$$
where $[E]_T$ is the total enzyme. The rate is linear in $[S]$ for small $[S]$ and saturates at $V_{\max}$ for large $[S]$, and $v = V_{\max}/2$ exactly when $[S] = K_M$. It is not a [mass action](/mass-action-kinetics/) rate law. It comes from the mass action network $E + S \rightleftharpoons C \to E + P$ after the [quasi-steady-state approximation](/quasi-steady-state-approximation/) removes the complex $C$.

## The machine

**The reaction scheme.** The enzyme $E$ binds the substrate $S$ to form the complex $C$, and the complex either releases $S$ or converts it to the product $P$ and frees the enzyme:
$$E + S \;\underset{k_{-1}}{\overset{k_1}{\rightleftharpoons}}\; C \;\overset{k_2}{\longrightarrow}\; E + P .$$
Here $k_1$ is in 1/(M s), and $k_{-1}$ and $k_2 = k_{\text{cat}}$ are in 1/s. Write $s, e, c, p$ for the concentrations.

**The full equations.** With mass action,
$$\dot s = -k_1 e s + k_{-1} c, \qquad \dot c = k_1 e s - (k_{-1} + k_2) c, \qquad \dot p = k_2 c,$$
and two conservation laws hold: $e + c = E_T$ and $s + c + p = S_0$ (the [stoichiometric matrix](/stoichiometric-matrix/) page derives them). So $e = E_T - c$, and the state is $(s, c)$.

**The assumptions.**
- The enzyme is scarce: $E_T \ll S_0 + K_M$ (Segel and Slemrod 1989). Then $c$ reaches a quasi-steady state fast, and $s$ changes slowly after that.
- The conversion step is irreversible, or the product is removed, or the rate is measured at the start, when $p \approx 0$.
- The solution is well mixed, and the temperature and the pH are fixed.

**The derivation (Briggs and Haldane 1925).** Set $\dot c = 0$ in the slow phase: $k_1 (E_T - c) s = (k_{-1} + k_2) c$. Solve for $c$:
$$c = \frac{E_T\, s}{K_M + s}, \qquad K_M = \frac{k_{-1} + k_2}{k_1}.$$
Then $v = \dot p = k_2 c$ is the rate law above, and $\dot s = -v$ (to leading order, because $c$ is small).

**The original derivation (Michaelis and Menten 1913).** They assumed that the binding is at equilibrium, $k_1 e s = k_{-1} c$. This gives the same form with the dissociation constant $K_S = k_{-1}/k_1$ in place of $K_M$. The two agree when $k_2 \ll k_{-1}$. In general $K_M > K_S$, and $K_M$ is not a binding constant.

## What it counts

**The rate law.** For $K_M = 2$ mM and $V_{\max} = 0.1$ mM/s:

| $[S]$ (mM) | 0.5 | 1 | 2 | 4 | 10 | 20 | 100 |
|---|---|---|---|---|---|---|---|
| $v / V_{\max}$ | 0.2 | 0.3333 | 0.5 | 0.6667 | 0.8333 | 0.9091 | 0.9804 |
| $v$ (mM/s) | 0.02 | 0.03333 | 0.05 | 0.06667 | 0.08333 | 0.09091 | 0.09804 |

At $[S] = K_M$ the rate is half of $V_{\max}$. To reach $0.9\, V_{\max}$ the substrate must be $9 K_M$, and $0.99\, V_{\max}$ needs $99 K_M$: the saturation is slow.

**The two regimes.** For $s \ll K_M$, $v \approx (k_{\text{cat}}/K_M)\, E_T\, s$, a first order rate with the *specificity constant* $k_{\text{cat}}/K_M$. For $s \gg K_M$, $v \approx V_{\max}$, zero order: the enzyme is saturated.

**The integrated rate law.** With $\dot s = -V_{\max} s/(K_M + s)$, separate the variables:
$$V_{\max}\, t = K_M \ln\frac{S_0}{s} + (S_0 - s).$$
For $S_0 = 10$ mM and the constants above, half of the substrate is used at $t = (2 \ln 2 + 5)/0.1 = 63.863$ s, and 90 percent at $t = (2 \ln 10 + 9)/0.1 = 136.052$ s. The explicit solution uses the Lambert W function: $s(t) = K_M\, W\!\left(\frac{S_0}{K_M} e^{(S_0 - V_{\max} t)/K_M}\right)$. It gives $s = 8.3586$, $6.0162$, $2.6534$ and $0.0652$ mM at $t = 20$, $50$, $100$ and $200$ s.

**Against the full model.** Take $k_1 = 1$ per mM per second, $k_{-1} = k_2 = 1$ per second and $E_T = 0.1$ mM. Then $K_M = 2$ mM and $V_{\max} = 0.1$ mM/s, the same constants. A [Runge-Kutta](/runge-kutta-methods/) solution of the full equations with step $0.001$ s from $s = 10$, $c = 0$ gives $s = 9.0987$, $5.9547$ and $2.6197$ mM at $t = 10$, $50$ and $100$ s, against $9.1727$, $6.0162$ and $2.6534$ from the rate law. Most of the gap is the substrate held in the complex ($c \approx 0.08$ mM) and used in the first second; here $E_T/(S_0 + K_M) = 0.0083$. With $E_T = 10$ mM instead ($\varepsilon = 0.83$), the full model gives $s = 1.952$ mM at $t = 0.5$ s and the rate law gives $6.016$ mM, a factor of about 3; the [quasi-steady-state approximation](/quasi-steady-state-approximation/) page shows the numbers.

**Estimating the constants.** The double reciprocal (Lineweaver-Burk) form $1/v = (K_M/V_{\max})(1/s) + 1/V_{\max}$ is a line. For the constants above, the points $(1/s, 1/v)$ for $s = 1, 2, 4, 8$ mM are $(1, 30)$, $(0.5, 20)$, $(0.25, 15)$ and $(0.125, 12.5)$, on the line with slope $K_M/V_{\max} = 20$ s and intercept $1/V_{\max} = 10$ s/mM. With noisy data this line gives the most weight to the smallest rates, which have the largest relative errors. A nonlinear least squares fit of $v$ itself (for example by Gauss-Newton or [Newton](/newton-raphson-method/) steps) is the usual choice; [linear regression](/linear-regression/) on the reciprocals is a starting point only.

## Relation to other models

- **[Mass action kinetics](/mass-action-kinetics/).** The full scheme is a mass action network with three reactions. The rate law is its reduction to one variable.
- **[Quasi-steady-state approximation](/quasi-steady-state-approximation/).** The general technique, its validity conditions, and the total QSSA, which stays accurate when the enzyme is not scarce.
- **[Hill equation](/hill-equation/).** The Hill function with $n = 1$ has the same form, $x/(K + x)$. In gene circuits, the fraction of a promoter bound by a transcription factor often has this form (Alon 2019, Appendix A).
- **Inhibition.** A competitive inhibitor $I$ that binds $E$ with dissociation constant $K_I$ gives $v = V_{\max} s / (K_M (1 + [I]/K_I) + s)$: the apparent $K_M$ grows, and $V_{\max}$ does not change. The derivation is the same quasi-steady state with one more complex.
- **The reversible scheme.** With $E + S \rightleftharpoons C \rightleftharpoons E + P$ the network has deficiency zero and is weakly reversible, so by the [deficiency zero theorem](/deficiency-zero-theorem/) it has exactly one positive equilibrium in each positive compatibility class, for all rate constants. The irreversible scheme has no positive equilibrium: the substrate runs out.

## Known results in the model

**Shape.** $v(s)$ is increasing and concave on $s \ge 0$, with $v(0) = 0$, $v'(0) = V_{\max}/K_M$ and $v \to V_{\max}$ as $s \to \infty$. On a log scale of $s$ it is the logistic curve $V_{\max} / (1 + e^{-(\ln s - \ln K_M)})$, symmetric about $\ln K_M$. The ratio of the substrate levels that give 90 percent and 10 percent of $V_{\max}$ is $81$; for the Hill equation with coefficient $n$ it is $81^{1/n}$.

**Validity (a perturbation result).** Segel and Slemrod (1989) showed that the fast time scale of $c$ is $t_c = 1/(k_1 (S_0 + K_M))$ and the time scale of the substrate decay is $t_s = (S_0 + K_M)/(k_2 E_T)$. The rate law is the leading term of a singular perturbation expansion in $\varepsilon = E_T/(S_0 + K_M)$, and its error is small when $\varepsilon \ll 1$. This is a condition on the parameters, not a theorem with a numerical bound for each case. The older condition $E_T \ll S_0$ is stronger than needed: the rate law also works for a small $S_0$ when $E_T \ll K_M$.

**The Haldane relation.** For the reversible scheme with constants $V_f, K_{MS}$ forward and $V_r, K_{MP}$ backward, the equilibrium constant is $K_{eq} = [P]^*/[S]^* = V_f K_{MP}/(V_r K_{MS})$. So the four kinetic constants cannot be chosen freely.

**Stiffness of the full model.** The full equations have the time scales $t_c$ and $t_s$. In the example with $E_T = 0.1$ mM, $t_c = 0.083$ s and $t_s = 120$ s, a ratio of about 1400. The full model is then a [stiff problem](/stiff-ode-problem/), and the reduction removes the fast time scale.

## References
