---
tag: 2ZZP2Q
kind: model
slug: nbti-reaction-diffusion-model
name: Reaction-diffusion model of NBTI
aliases:
- NBTI R-D model
- reaction-diffusion aging model
area: eda/power-reliability-and-manufacturability
level: research
summary: Models the threshold shift of a PMOS transistor under negative bias as hydrogen released at the interface diffusing away, giving a power-law in time and partial recovery.
prereqs: [heat-equation]
see_also: [finite-difference-method, static-timing-analysis, black-equation, compact-thermal-model, leakage-power, gate-sizing, laplace-transform]
sources:
  - paper: doi:10.1063/1.323909
    title: Kjell O. Jeppson and Christer M. Svensson, Negative bias stress of MOS devices at high electric fields and degradation of MNOS devices, Journal of Applied Physics 48(5), 2004 to 2014, 1977
    locator: the model of interface states created by a reaction at the interface and limited by the diffusion of the released hydrogen species into the oxide, and its t^(1/4) law
  - paper: "Muhammad A. Alam and Souvik Mahapatra, A comprehensive model of PMOS NBTI degradation, Microelectronics Reliability 45(1), 71 to 81, 2005"
    title: Muhammad A. Alam and Souvik Mahapatra, A comprehensive model of PMOS NBTI degradation, Microelectronics Reliability 45(1), 71 to 81, 2005
    locator: the reaction-diffusion equations, their regimes (reaction-limited, equilibrium, diffusion-limited, saturation), the exponents 1/4 for atomic and 1/6 for molecular hydrogen, and the recovery after the stress
  - paper: doi:10.1109/TED.2011.2164543
    title: Tibor Grasser, Ben Kaczer, Wolfgang Goes, Hans Reisinger, Thomas Aichinger, Philipp Hehenberger, Paul-Jurgen Wagner, Franz Schanovsky, Jacopo Franco, Maria Toledano Luque and Michael Nelhiebel, The paradigm shift in understanding the bias temperature instability, from reaction-diffusion to switching oxide traps, IEEE Transactions on Electron Devices 58(11), 3652 to 3666, 2011
    locator: the comparison of reaction-diffusion predictions with measured recovery, and the switching oxide trap model proposed in its place
  - paper: "Sanjay V. Kumar, Chris H. Kim and Sachin S. Sapatnekar, An analytical model for negative bias temperature instability, IEEE/ACM International Conference on Computer-Aided Design, 2006"
    title: Sanjay V. Kumar, Chris H. Kim and Sachin S. Sapatnekar, An analytical model for negative bias temperature instability, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 2006
    locator: the closed-form treatment of alternating stress and recovery for circuit aging analysis (general locator, page numbers not checked)
---

The reaction-diffusion (R-D) model explains *negative bias temperature instability* (NBTI), the slow rise of the threshold voltage of a PMOS transistor whose gate is held negative with respect to its channel at high temperature. In the model, the stress breaks silicon-hydrogen bonds at the interface between the channel and the gate oxide. The freed hydrogen diffuses into the oxide, and the broken bonds left behind are interface traps that shift the threshold voltage. Since the diffusion of hydrogen limits the rate, the number of traps grows as a power of time, $t^{1/4}$ for atomic hydrogen and $t^{1/6}$ for molecular hydrogen. When the stress is removed, hydrogen returns and part of the shift recovers.

The model is a physical picture with fitted rates: the forward and reverse rates, the diffusivity and their temperature and field dependence come from fits to measured threshold shifts. It is also debated. Since about 2010 a large body of measurements of recovery has been read as evidence against it, and an alternative based on charge trapping in oxide defects has been proposed. This page states the model and proves what follows from it under its approximations. The section on relation to other models gives the debate.

## The machine

Let $x \ge 0$ be the depth into the oxide, with the interface at $x = 0$.

- $N_0$: the density of Si-H bonds at the interface that can break, per unit area.
- $N_{it}(t)$: the density of broken bonds, the interface traps, per unit area.
- $N_H(x, t)$: the density of free hydrogen in the oxide, per unit volume.

**Reaction at the interface.** Bonds break at rate $k_f$ and re-form with a hydrogen atom at the interface at rate $k_r$:

$$ \frac{dN_{it}}{dt} = k_f (N_0 - N_{it}) - k_r N_{it} N_H(0, t). $$

**Diffusion in the oxide.**

$$ \frac{\partial N_H}{\partial t} = D \frac{\partial^2 N_H}{\partial x^2}, \qquad x > 0. $$

**Conservation.** Each broken bond has released one hydrogen atom, and no hydrogen was in the oxide at first, so $N_{it}(t) = \int_0^\infty N_H(x, t)\, dx$.

**Threshold shift.** The traps hold a positive charge when the PMOS channel is inverted, and $\Delta V_{th} = q N_{it} / C_{ox}$, with $C_{ox}$ the oxide capacitance per unit area. Part of the measured shift also comes from charge trapped in the oxide, which this model does not contain.

**Molecular variant.** Atomic hydrogen at the interface can pair into $H_2$, which then is the diffusing species. With a fast pairing equilibrium $N_{H_2}(0, t) = k_H N_H(0, t)^2$, diffusion of $N_{H_2}$ with diffusivity $D_2$, and conservation $N_{it} = 2 \int_0^\infty N_{H_2}\, dx$.

**Fitted parts.** $k_f$, $k_r$, $D$, $k_H$ and $N_0$ are not measured independently. $k_f$ depends on the oxide field and on temperature, $D$ follows an Arrhenius law with a fitted activation energy, and the whole set is fitted to measured $\Delta V_{th}(t)$ curves at several voltages and temperatures.

## What it counts

The model counts interface traps $N_{it}(t)$, and so the threshold shift $\Delta V_{th}(t)$, of one transistor under a given stress history: the times during which the gate is under negative bias (stress) and the times during which it is not (recovery). A circuit tool turns $\Delta V_{th}$ into extra delay of each gate and checks the aged circuit with [static timing analysis](/static-timing-analysis/), usually as a guard band on the clock period.

The model has four regimes, in order of time: a reaction-limited start with $N_{it} \approx k_f N_0 t$, a short plateau where the two reactions balance, the *diffusion-limited regime* where the power laws below hold, and saturation when $N_{it}$ approaches $N_0$ or the hydrogen front reaches the far side of the oxide. Most measurements and all circuit use concern the diffusion-limited regime.

## Relation to other models

**The debate.** Jeppson and Svensson introduced the reaction-diffusion explanation in 1977 for the $t^{1/4}$ growth they measured. Alam and Mahapatra gave the full set of regimes and the recovery, and the model was the standard picture of NBTI for circuit work in the 2000s. Grasser and coworkers (2011) compared it with measurements made within microseconds after the stress, and found the following.

- Recovery starts at once and continues over many decades of time, while the R-D model predicts recovery on a time scale set by the stress time (Theorem 3 below).
- The fitted time exponent depends on the delay of the measurement, so a measured exponent near 1/4 or 1/6 does not confirm the model.
- Behavior after short or alternating stress does not match R-D predictions.

They proposed that most of the shift comes from charge capture in oxide defects with a wide distribution of capture and emission times (switching oxide traps), and called this a paradigm shift. Later models combine a trapping part with an interface trap part, and their relative share is still argued. Circuit tools still use power laws in $t$ with fitted exponents, often motivated by the R-D model, because they are simple.

**Other aging mechanisms.** Electromigration of wires is described by [Black's equation](/black-equation/), another fitted law. Hot carrier injection and positive bias instability in NMOS transistors have their own models. Temperature enters all of them through Arrhenius factors, so they all use the temperature map of the [compact thermal model](/compact-thermal-model/).

**Same mathematics.** The diffusion part is the [heat equation](/heat-equation/) on a half-line with a nonlinear boundary condition. The [finite difference method](/finite-difference-method/) solves it numerically, and the [Laplace transform](/laplace-transform/) gives the half-derivative relation used in Theorem 1.

## Known results in the model

**Approximations of the diffusion-limited regime.** These are assumptions, not results:

- (A1) Quasi-equilibrium: $dN_{it}/dt$ is small compared with each reaction term, so $k_f(N_0 - N_{it}) = k_r N_{it} N_H(0, t)$.
- (A2) $N_{it} \ll N_0$.
- (A3) The oxide is semi-infinite, $D$ is constant, and hydrogen is not trapped in the oxide.
- (A4) $N_H(x, 0) = 0$.
- (A5) The resulting problem has a unique solution.

With (A1) and (A2), the boundary condition becomes $N_H(0, t)\, N_{it}(t) = K$ with $K = k_f N_0 / k_r$.

**Theorem 1 (the $t^{1/4}$ law).** Under (A1) to (A5), $N_{it}(t) = a\, K^{1/2} (Dt)^{1/4}$ with $a = (4\, \Gamma(3/4) / \Gamma(1/4))^{1/2} \approx 1.163$.

*Proof of the exponent.* Let $u(x, t) = N_H(x, t)$ solve the problem, with $N(t) = \int u\, dx$. For $\lambda > 0$ put $u_\lambda(x, t) = \lambda^{1/2} u(\lambda x, \lambda^2 t)$. It solves the diffusion equation, it is 0 at $t = 0$, and its integral is $N_\lambda(t) = \lambda^{-1/2} N(\lambda^2 t)$. Its boundary value satisfies $u_\lambda(0, t) N_\lambda(t) = u(0, \lambda^2 t) N(\lambda^2 t) = K$. So $u_\lambda$ solves the same problem, and by (A5) $u_\lambda = u$. Then $N(\lambda^2 t) = \lambda^{1/2} N(t)$ for all $\lambda$ and $t$, and with $t = 1$ and $s = \lambda^2$, $N(s) = N(1)\, s^{1/4}$.

*Proof of the constant.* Measure time in $s = Dt$. For the diffusion equation on $x > 0$ with zero initial data and boundary value $g(s) = c s^\alpha$, $\alpha > -1$, the total amount $\int_0^\infty u\, dx$ is the half-order integral of $g$, $c\, \Gamma(\alpha + 1)/\Gamma(\alpha + 3/2)\, s^{\alpha + 1/2}$. This follows from the Laplace transform of the problem, whose solution is $\hat g(p) e^{-x \sqrt p}$, with integral $\hat g(p)/\sqrt p$. For $\alpha = 0$ it gives the known $2\sqrt{s / \pi}$. Put $N = A s^{1/4}$, so $g = (K/A) s^{-1/4}$ and $\alpha = -1/4$. Then $A s^{1/4} = (K/A)\, \Gamma(3/4)/\Gamma(5/4)\, s^{1/4}$, and with $\Gamma(5/4) = \Gamma(1/4)/4$, $A^2 = 4 K \Gamma(3/4)/\Gamma(1/4)$. $\square$

**Theorem 2 (the $t^{1/6}$ law).** In the molecular variant, under the same approximations with $N_H(0) = K / N_{it}$, $N_{it}(t) = (12\, k_H K^2\, \Gamma(2/3)/\Gamma(1/6))^{1/3} (D_2 t)^{1/6}$, a constant of about $1.429\, (k_H K^2)^{1/3}$.

*Proof.* The boundary condition is now $u(0, t) N(t)^2 = k_H K^2$ for $u = N_{H_2}$ and $N = 2 \int u\, dx$. The map $u_\lambda(x, t) = \lambda^{2/3} u(\lambda x, \lambda^2 t)$ gives $N_\lambda(t) = \lambda^{-1/3} N(\lambda^2 t)$ and $u_\lambda(0, t) N_\lambda(t)^2 = u(0, \lambda^2 t) N(\lambda^2 t)^2$, so the problem is invariant, and as before $N(s) = N(1) s^{1/6}$. For the constant, $N = A s^{1/6}$ gives $g = k_H K^2 A^{-2} s^{-1/3}$, and $A s^{1/6} = 2\, k_H K^2 A^{-2}\, \Gamma(2/3)/\Gamma(7/6)\, s^{1/6}$ with $\Gamma(7/6) = \Gamma(1/6)/6$. $\square$

The usual textbook estimate takes a triangular hydrogen profile of length $\sqrt{Dt}$, so $N_{it} = N_H(0)\sqrt{Dt}/2$, which with $N_H(0) = K/N_{it}$ gives $N_{it} = (K/2)^{1/2}(Dt)^{1/4}$. It has the right exponent, but its constant 0.707 is 0.61 times the exact 1.163.

**Theorem 3 (recovery scales with stress time).** Stress up to $t_s$, then remove the bias. Assume that in recovery bond breaking stops and every hydrogen atom that reaches the interface re-forms a bond at once, so $N_H(0, t) = 0$ for $t > t_s$ and $N_{it} = \int N_H\, dx$ still holds. Then the remaining fraction $N_{it}(t_s + t_r) / N_{it}(t_s)$ depends only on $t_r / t_s$.

*Proof.* The scaled solution $u_\lambda$ of Theorem 1 solves the stress phase on $[0, t_s/\lambda^2]$, and its recovery phase satisfies the same zero boundary condition. By uniqueness the solution for stress time $t_s / \lambda^2$ is $u_\lambda$, and the ratio $N_\lambda(\tau_s + \tau_r)/N_\lambda(\tau_s)$ with $\tau = t/\lambda^2$ equals $N(t_s + t_r)/N(t_s)$. $\square$

**Measured by a finite difference solve.** Backward Euler in time, $\Delta x = 0.02$ on $[0, 40]$, time steps of 1 percent of $t$, and $K = D = 1$:

| quantity | measured | exact under the model |
|---|---|---|
| slope of $\log N_{it}$ against $\log t$, $t \in [1, 10]$, atomic | 0.2500 | 1/4 |
| $N_{it}(100) / 100^{1/4}$, atomic | 1.157 | 1.163 |
| slope, $t \in [1, 10]$, molecular ($k_H = 1$) | 0.1660 | 1/6 |
| $N_{it}(100) / 100^{1/6}$, molecular | 1.422 | 1.429 |
| remaining fraction at $t_r / t_s = 0.1$, 1, 2 (atomic) | 0.763, 0.453, 0.350 | depends only on $t_r/t_s$ |

The recovery fractions agree to 3 digits for $t_s = 1$ and $t_s = 4$, as Theorem 3 says. They are measured values of this numerical solve, not proved constants. In this model, half of the shift needs a recovery time close to the stress time. Measured devices recover a large part within microseconds even after long stress, which is one of the observations used against the model.

## References
