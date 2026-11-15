---
tag: B93JKJ
kind: theorem
slug: internal-model-principle
name: Internal model principle
aliases:
- Francis-Wonham internal model principle
area: control/classical-control
level: core
summary: A stable loop keeps zero steady-state error to a class of references or disturbances under all small plant changes only if the controller contains a model of the generator of that class.
history:
  year: 1976
  people: [Bruce A. Francis, W. Murray Wonham, Edward J. Davison]
  note: Francis and Wonham named and proved the principle for multivariable linear systems in 1975 and 1976. Davison gave existence conditions for the robust servomechanism problem in 1976.
prereqs: [steady-state-error, final-value-theorem, feedback-control-loop]
see_also: [output-regulation-problem, regulator-equations, steady-state-error, internal-model-control, integral-state-feedback, pid-controller, disturbance-observer, offset-free-mpc]
sources:
  - paper: doi:10.1016/0005-1098(76)90006-6
    title: B. A. Francis and W. M. Wonham, The internal model principle of control theory, Automatica 12(5) (1976) 457-465
    locator: the whole paper (structurally stable regulation and the internal model in the controller)
  - paper: doi:10.1109/TAC.1976.1101137
    title: E. J. Davison, The robust control of a servomechanism problem for linear time-invariant multivariable systems, IEEE Transactions on Automatic Control 21(1) (1976) 25-34
    locator: the whole paper (existence conditions and the structure of a robust servo controller)
  - paper: doi:10.1137/0315033
    title: B. A. Francis, The linear multivariable regulator problem, SIAM Journal on Control and Optimization 15(3) (1977) 486-505
    locator: the whole paper (the regulator problem with internal stability, and its solution by the regulator equations)
---

The internal model principle says what a feedback controller must contain to drive the error to zero for a whole class of reference or disturbance signals, and to keep doing so when the plant changes a little. If the signals are steps, the controller needs an integrator. If they are sinusoids of frequency $\omega_0$, it needs the poles $\pm j\omega_0$. In general it needs the unstable modes of the system that generates the signals, the *exosystem*, and in a loop with $p$ outputs it needs $p$ copies of them. Francis and Wonham proved the principle in 1975 and 1976 for multivariable linear systems. The key hypothesis is that zero error must hold for all plants near the nominal one, the structural stability of the regulation property. Without it, a controller can reach zero error for one plant only.

## Statement

**Setup.** Consider a negative unity feedback loop with $e = r - y$, a strictly proper plant $P = b/a$ and a proper controller $C = n_c/d_c$, both written with coprime real polynomials. The loop is internally stable when the characteristic polynomial $\chi = a\,d_c + b\,n_c$ is Hurwitz. Let $\varphi$ be a monic real polynomial with all roots in the closed right half plane. The signal class of $\varphi$ is the set of all signals whose Laplace transform is $\nu(s)/\varphi(s)$ for a real polynomial $\nu$ with $\deg \nu < \deg\varphi$: the outputs of the exosystem with characteristic polynomial $\varphi$, for all its initial states. For example, $\varphi = s$ gives the constants, $\varphi = s^2$ the ramps $\alpha + \beta t$, and $\varphi = s^2 + \omega_0^2$ the sinusoids of frequency $\omega_0$.

**Theorem (single output).** Let the loop be internally stable.

1. (*Regulation.*) $e(t) \to 0$ for every reference $r$ in the signal class of $\varphi$ if and only if $\varphi$ divides $a\,d_c$.
2. (*Robust regulation.*) The following are equivalent:
   - (a) there is a neighborhood of the plant coefficients (with the degrees of $a$ and $b$ fixed) such that, for every plant $b'/a'$ in it, the loop with the same $C$ is internally stable and $e(t) \to 0$ for every $r$ in the class of $\varphi$;
   - (b) $\varphi$ divides $d_c$: the controller has every root of $\varphi$ as a pole, with at least the same multiplicity.

The same holds for a disturbance $d_o$ at the plant output, because $y = S\,d_o$ and $e = S\,r$ use the same $S = a\,d_c/\chi$.

**Theorem (Francis and Wonham 1976, multivariable form, informal).** Let a linear plant with $m$ inputs and $p$ regulated outputs be driven by an exosystem $\dot w = S_w w$ whose eigenvalues are all in the closed right half plane, and let the controller be driven by the error. Suppose the closed loop is internally stable and the error goes to 0 for every initial state of the plant, the controller and the exosystem. Then this regulation property holds for all plant data in a neighborhood of the nominal data if and only if the controller contains a $p$-fold copy of the exosystem dynamics: in a precise sense stated in the paper, $p$ copies of the minimal polynomial of $S_w$ appear in the controller. For $p = 1$ and a transfer function controller this is part 2 above. A common sufficient form is $C(s) = C_0(s)\,\varphi(s)^{-1} I_p$, the series connection of $p$ exosystem models with a stabilizer $C_0$.

**Existence (Davison 1976, in short).** For a plant $\dot x = A x + B u$, $y = C x + D u$ with error $e = r - y$, a controller with this property exists if and only if $(A, B)$ is stabilizable, $(C, A)$ is detectable, and $\operatorname{rank} \begin{bmatrix} A - \lambda I & B \\ C & D \end{bmatrix} = n + p$ at every root $\lambda$ of $\varphi$. The rank condition says that the plant has no transmission zero at a mode of the exosystem, and it needs $m \ge p$.

## In plain words

To cancel a disturbance that keeps coming back in the same pattern, the controller must be able to make that pattern by itself. A heater that must hold a room at a set temperature against a steady heat loss needs a part that adds up the error over time, so it can keep giving heat when the error is zero. A controller that must cancel a hum at one frequency needs a part that oscillates at that frequency. You can sometimes tune a controller without such a part so that it works for one exact plant. But the first small change in the plant then brings the error back. Only a copy of the signal pattern inside the controller gives zero error that survives small plant changes, and a system with several outputs needs one copy for each output.

## Proof

The proof is for the single-output theorem. It uses the [final value theorem](/final-value-theorem/) in its exact form for rational transforms, including its Lemma A: an exponential polynomial $\sum_p q_p(t)\,e^{p t}$ over exponents with $\operatorname{Re} p \ge 0$ goes to 0 only if all $q_p$ are zero.

**Part 1.** For $R = \nu/\varphi$,

$$E(s) = S(s) R(s) = \frac{a(s)\,d_c(s)\,\nu(s)}{\chi(s)\,\varphi(s)}.$$

*If.* Let $a\,d_c = \varphi\,\psi$. Then $E = \psi\,\nu/\chi$. Since $P$ is strictly proper and $C$ is proper, $\deg\chi = \deg(a\,d_c)$, so $\deg(\psi\nu) < \deg\psi + \deg\varphi = \deg\chi$ and $E$ is strictly proper. Its poles are roots of the Hurwitz $\chi$, so $e(t) \to 0$.

*Only if.* Suppose $\varphi$ does not divide $a\,d_c$. Then some root $\lambda$ of $\varphi$ has a larger multiplicity $\mu$ in $\varphi$ than its multiplicity $\kappa$ in $a\,d_c$. Take $\nu = 1$, which is allowed since $\deg\varphi \ge 1$. Because $\operatorname{Re}\lambda \ge 0$ and $\chi$ is Hurwitz, $\chi(\lambda) \ne 0$, so after all cancellations $E$ still has a pole of order $\mu - \kappa \ge 1$ at $\lambda$. Then $e(t)$ is an exponential polynomial whose part with exponents in the closed right half plane is not zero, and by Lemma A it does not go to 0. $\square$

**Part 2, (b) implies (a).** Let $\varphi \mid d_c$. The roots of $\chi' = a'\,d_c + b'\,n_c$ depend continuously on the coefficients of $a'$ and $b'$, and the degree of $\chi'$ stays the same near $(a, b)$, because its leading coefficient is that of $a'\,d_c$. So $\chi'$ stays Hurwitz in a neighborhood of the plant, and coprimeness of $a'$ and $b'$ also persists there, because the resultant of $a$ and $b$ is nonzero and depends continuously on the coefficients. For each such plant $\varphi \mid a'\,d_c$, so Part 1 gives $e(t) \to 0$.

**Part 2, (a) implies (b).** Suppose $\varphi$ does not divide $d_c$, and let $\lambda$ be a root of $\varphi$ whose multiplicity $\mu$ in $\varphi$ is larger than its multiplicity $\kappa$ in $d_c$. Perturb only the constant term of the plant denominator: $a_\varepsilon = a + \varepsilon$ and $b_\varepsilon = b$. Then $a_\varepsilon(\lambda) = a(\lambda) + \varepsilon$ is nonzero for all $\varepsilon \ne -a(\lambda)$, so for all small $\varepsilon \ne 0$ the multiplicity of $\lambda$ in $a_\varepsilon\,d_c$ is exactly $\kappa < \mu$, and $\varphi$ does not divide $a_\varepsilon\,d_c$. If (a) held, these plants would be in the neighborhood, the loop would be internally stable for them, and Part 1 would give an $r$ in the class with $e(t) \not\to 0$. So (a) fails. $\square$

The multivariable theorem needs the geometric approach of Francis and Wonham, or the frequency-domain arguments in the later literature; the proof is in the 1976 paper. The idea is the same: a mode of the exosystem that is not a pole of the controller must be cancelled by the plant, and a small perturbation of the plant breaks the cancellation.

## Consequences

- **Integral action.** For steps ($\varphi = s$), robust zero error needs a pole of $C$ at $s = 0$. This is the reason for the I term of the [PID controller](/pid-controller/) and for [integral state feedback](/integral-state-feedback/). For ramps a double integrator is needed. The table of the [steady-state error](/steady-state-error/) page is Part 1 for $\varphi = s^{k+1}$.
- **The point of entry does not matter.** The internal model must be in the controller, not only somewhere in the loop. A plant integrator rejects a step reference, but not a step disturbance at the plant input (the example on the steady-state error page).
- **Sinusoids.** A resonant term $1/(s^2 + \omega_0^2)$ in $C$ rejects a sinusoidal disturbance of frequency $\omega_0$ for all small plant changes. Periodic signals with many harmonics need many such terms, which leads to repetitive control.
- **Multivariable plants.** A plant with $p$ outputs needs $p$ copies, for example $p$ integrators for $p$ constant references, and at least as many inputs as outputs (Davison's rank condition).
- **State-space regulation.** The [output regulation problem](/output-regulation-problem/) asks for the same property in state space; its solvability is decided by the [regulator equations](/regulator-equations/), and the controllers that solve it robustly contain the internal model. [Disturbance observers](/disturbance-observer/) and [offset-free MPC](/offset-free-mpc/) build the model into an estimator.
- **Not internal model control.** [Internal model control](/internal-model-control/) is a controller structure that contains a model of the plant, not of the signals. The two names are close and the ideas are different.

## Tightness

**Regulation without robustness.** Let $P(s) = 1/(s(s + 1))$ and $C = 2$. The loop has $\chi = s^2 + s + 2$, and $\varphi = s$ divides $a\,d_c = s(s + 1)$, so the step error is 0 by Part 1. But $s \nmid d_c = 1$. Perturb the plant to $a_\varepsilon = s(s + 1) + \varepsilon$: the step error becomes $S(0) = \varepsilon/(\varepsilon + 2)$, for example 0.0476 for $\varepsilon = 0.1$. If the physics guarantees that the plant pole stays exactly at 0 (an angle that is the integral of a speed), the perturbation class is smaller, and a smaller internal model is enough. The theorem is relative to the class of perturbations.

**The model must be exact.** Let $P(s) = 1/(s + 1)$ and $r = \sin t$ ($\varphi = s^2 + 1$). The controller $C = (5 s^2 + 11 s + 7)/(s^2 + 1)$ gives $\chi = (s + 2)^3$ and $S = (s + 1)(s^2 + 1)/(s + 2)^3$, so $S(\pm j) = 0$ and the error goes to 0. For the changed plant $1/(s + 1.5)$, $\chi = s^3 + 6.5 s^2 + 12 s + 8.5$ is still Hurwitz ($6.5 \cdot 12 > 8.5$) and the error still goes to 0. If the controller denominator is $s^2 + 1.01$ instead, the error amplitude is $|S(j)| = 0.0013$, small but not zero. A proportional controller $C = 10$ leaves $|S(j)| = 0.128$.

**Robustness is local.** Part 2 promises zero error only in a neighborhood where the loop stays internally stable. A large plant change can destabilize the loop, and then the internal model does not help.

**Internal stability is needed.** Without it, some closed-loop map has poles in the closed right half plane. A controller zero that cancels an unstable plant pole can give an $S$ with zero error to the reference while a load disturbance makes an internal signal grow without bound.

## History

Integral action was used in governors and process controllers long before a general theory. In the early 1970s several groups studied the servomechanism and regulator problems for multivariable linear systems. Francis and Wonham presented the internal model principle at an IFAC symposium in 1975 and published it in Automatica in 1976, in the language of the geometric approach. Davison (1976) solved the robust servomechanism problem and gave the existence conditions above. Francis (1977) treated the linear multivariable regulator problem with internal stability. The principle was later extended to nonlinear systems in the theory of output regulation.

## References
