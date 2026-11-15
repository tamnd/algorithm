---
tag: SF82VG
kind: theorem
slug: rohrs-counterexample
name: Rohrs counterexample
aliases:
- Rohrs example
area: control/robust-and-adaptive-control
level: advanced
summary: An example of 1985 showing that standard adaptive controllers can go unstable under small unmodeled dynamics and disturbances.
prereqs: [model-reference-adaptive-control, routh-hurwitz-criterion]
see_also: [mit-rule, sigma-modification, parameter-projection, l1-adaptive-control, averaging-method, model-uncertainty, phase-margin, small-gain-theorem]
sources:
  - paper: doi:10.1109/TAC.1985.1104070
    title: "Charles E. Rohrs, Lena Valavani, Michael Athans and Gunter Stein, Robustness of continuous-time adaptive control algorithms in the presence of unmodeled dynamics, IEEE Transactions on Automatic Control 30(9), 1985"
    locator: "pages 881 to 889; the plant 2/(s+1) times 229/(s^2+30s+229), the model 3/(s+3), the initial gains 1.14 and -0.65; Fig. 6 (r = 0.3 + 1.85 sin 16.1t, instability) and Fig. 7 (r = 0.3 + 2 sin 8t, bounded)"
  - book: isbn:9780486498171
    title: "Petros A. Ioannou and Jing Sun, Robust Adaptive Control, Prentice Hall 1996 (Dover reprint 2012)"
    locator: "Section 8.3, Instability phenomena in adaptive systems (8.3.1 parameter drift, 8.3.2 high frequency unmodeled dynamics) and Section 8.4 (robust modifications of the adaptive law)"
  - paper: "Karl Johan Åström, Analysis of Rohrs counterexamples to adaptive control, Proceedings of the 22nd IEEE Conference on Decision and Control, 1983"
    locator: "the whole paper (an averaging analysis that explains the instability by the phase of the unmodeled dynamics at the frequency of the command)"
---

The Rohrs counterexample is a counterexample to the claim that the standard model reference adaptive controller, which keeps all signals bounded for a plant of the assumed structure, keeps this property when the plant has small unmodeled dynamics. Rohrs, Valavani, Athans and Stein (1985) took a first order plant with a fast, well damped second order factor that the designer ignores, and showed that a bounded command at a high frequency makes the gains drift until the closed loop loses stability. The unmodeled factor has a bandwidth of about 15 rad/s against the plant pole at 1 rad/s, so a fixed controller with the same nominal design has a large margin. The example started the work on robust adaptive control, with modifications such as [sigma modification](/sigma-modification/) and [parameter projection](/parameter-projection/).

## Statement

**The claim that fails.** For the plant $y = \frac{2}{s + 1}u$, the reference model $y_m = \frac{3}{s + 3}r$, the controller $u = k_r r + k_y y$, the error $e = y - y_m$ and the adaptive law
$$\dot k_r = -\gamma\, e\, r,\qquad \dot k_y = -\gamma\, e\, y,\qquad \gamma = 1,$$
all signals are bounded and $e(t) \to 0$ for every bounded $r$ and every initial state. This is a theorem for the plant above (it has relative degree one and the transfer function $\frac{2}{s+1}$, and the law is the Lyapunov law of the [MRAC](/model-reference-adaptive-control/) page for a plant with a positive high frequency gain). The ideal gains are $k_r^* = 1.5$ and $k_y^* = -1$.

**The counterexample.** Let the true plant be
$$y = \frac{2}{s + 1}\cdot\frac{229}{s^2 + 30s + 229}\,u,$$
with the same model, controller and law. The extra factor has the poles $-15 \pm 2j$ and the gain 1 at $s = 0$. Start with the plant and the model at rest and $k_r(0) = 1.14$, $k_y(0) = -0.65$, and apply
$$r(t) = 0.3 + 1.85\sin(16.1\,t).$$
Then:

1. For each frozen value of $k_y$, the closed loop is asymptotically stable if and only if $-17.03 < k_y < 0.5$ (exactly, $-7800/458 < k_y < 1/2$). The initial gains are inside, with the DC gain $0.9913$ from $r$ to $y$.
2. The solution of the adaptive loop has $k_y(t)$ decreasing on average: $k_y = -1.70$ at $t = 10$ s and $-12.6$ at $t = 20$ s, while $k_r$ grows to $3.77$ and $14.6$.
3. $k_y$ passes $-17.03$ at $t = 20.36$ s, and $|y|$ exceeds 10 at $t = 20.69$ s: the closed loop is unstable, and the signals grow without bound.

Item 1 is exact. Items 2 and 3 are measurements of a numerical solution (RK4 with the step 0.001 s, the same times with 0.0005 s), which agree with Fig. 6 of the paper.

## In plain words

An adaptive controller is designed for a simple model of a machine. The real machine has an extra small delay that the model leaves out; it only matters for fast signals. If the command contains a fast wave, at a speed where this small delay turns the response of the machine upside down, the adaptive rule reads the wrong direction from the data. It keeps raising the feedback gain, slowly, because it thinks this makes the error smaller. After about 20 seconds the gain is so large that the loop shakes itself apart. A fixed controller with the same starting tuning would have been fine forever. The lesson is that an adaptive rule that is proved correct for the model can fail for a machine that is only a little different.

## Proof

**Step 1 (the frozen loop).** With constant gains, $u = k_r r + k_y y$ and $y = G u$ with $G(s) = \frac{458}{(s + 1)(s^2 + 30s + 229)}$. The denominator of the closed loop is
$$(s + 1)(s^2 + 30s + 229) - 458k_y = s^3 + 31s^2 + 259s + (229 - 458k_y).$$
By the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/), a cubic $s^3 + a_1s^2 + a_2s + a_3$ has all roots in the open left half plane if and only if $a_1 > 0$, $a_3 > 0$ and $a_1a_2 > a_3$. Here $a_1 = 31$, $a_3 > 0$ means $k_y < 1/2$, and $31 \cdot 259 = 8029 > 229 - 458k_y$ means $k_y > -7800/458 = -17.0306$. At $k_y = -0.65$, $a_3 = 526.7$ and the DC gain is $k_r G(0)/(1 - k_yG(0)) = 2.28/2.3 = 0.9913$.

**Step 2 (the critical frequency).** $G(j\omega)$ is real when the imaginary part of the denominator $229 - 31\omega^2 + j(259\omega - \omega^3)$ is zero, that is at $\omega = \sqrt{259} = 16.0935$ rad/s. There the denominator is $229 - 31 \cdot 259 = -7800$ and $G = -458/7800 = -0.058718$: the phase is $-180$ degrees and $1/G = -17.03$, the same bound as in Step 1. At $\omega = 16.1$ the phase is $-180.02$ degrees and $|G| = 0.058669$. The reduced plant $2/(s + 1)$ has the phase $-86.4$ degrees at this frequency, so the unmodeled factor adds about $-94$ degrees exactly where the command has its energy.

**Step 3 (the direction of the drift).** This step is an approximation by averaging, valid while the gains change slowly compared with the loop. For frozen gains and a sine $r = r_1\sin\omega t$, the steady state is $y = T r$ with $T = k_rG/(1 - k_yG)$ and $y_m = Mr$ with $M = 3/(s + 3)$, so the mean of $e\,y$ over one period is
$$\overline{e\,y} = \frac{r_1^2}{2}\left(|T(j\omega)|^2 - \operatorname{Re}\big(M(j\omega)\overline{T(j\omega)}\big)\right).$$
At $\omega = 16.1$, $G$ is real and negative, so $T$ is real and negative while $1 - k_yG > 0$, and $\operatorname{Re}M(j16.1) = 9/(9 + 16.1^2) = 0.03356 > 0$. Both terms are then positive, so $\overline{e\,y} > 0$ and $\dot k_y = -e\,y$ decreases $k_y$ on average. In the same way $\overline{e\,r} = (r_1^2/2)\operatorname{Re}(T - M) < 0$, so $k_r$ increases. As $k_y$ falls, $1 - k_yG = 1 + 0.0587k_y$ moves toward zero, $|T|$ grows, and the drift becomes faster. The constant part $0.3$ of $r$ pulls the gains toward the correct DC gain, but with the amplitude $1.85$ the sine term dominates. Nothing stops $k_y$ before the bound $-17.03$ of Step 1.

**Step 4 (the instability).** The numerical solution of the six differential equations (three plant states, the model, $k_r$ and $k_y$) confirms Step 3 with the values of the Statement. Once $k_y < -17.03$, the frozen loop has a pair of poles in the right half plane, near $\pm 16.1j$, the oscillation at this frequency grows, and its growth makes $e\,y$ larger and drives $k_y$ further down. The claim that fails needs only one bounded command with unbounded signals, and this is such a command. $\square$

## Consequences

- **Small modeling errors matter.** The proofs of MRAC need the plant to have exactly the assumed relative degree and order. A factor with gain 1 at low frequency and a bandwidth 15 times the plant pole is enough to break the guarantee.
- **The command must not excite the unmodeled range.** A rule of thumb that follows from Step 3 is to keep the command and the adaptation slow relative to the frequencies where the model is wrong; Åström (1983) explained the effect by averaging.
- **Bounded disturbances cause drift.** With a constant command and a small disturbance, the gains can drift without bound even for the ideal plant (Ioannou and Sun, Section 8.3.1, give an explicit solution with $x \to 0$ and $k = 5(1 + t)^{1/5} \to \infty$). Large gains then meet the unmodeled dynamics.
- **Robust adaptive laws.** Leakage ([sigma modification](/sigma-modification/)), [parameter projection](/parameter-projection/), dead zones and normalization keep the gains bounded, at the cost of a bias or a residual error. With projection of $k_y$ into $[-10, 0]$, for example, the frozen loop of Step 1 stays asymptotically stable for every $k_y$ in the set.
- **Later designs.** [L1 adaptive control](/l1-adaptive-control/) separates the adaptation from the control bandwidth with a filter, partly in response to such examples.

## Tightness

- **The frequency matters.** With $r = 0.3 + 2\sin 8t$ the paper reports bounded signals (Fig. 7). At $\omega = 8$ the phase of $G$ is $-138.4$ degrees and $G = -0.1458 - 0.1296j$; in a simulation with the same start, the gains move to about $k_r = 1.42$ and $k_y = -5.5$ at $t = 100$ s and stay inside the interval of Step 1 (a measurement).
- **The unmodeled factor matters.** For the plant $2/(s + 1)$ without the extra factor, the theorem holds for every bounded command, so the counterexample needs the unmodeled dynamics.
- **The bound is sharp.** The frozen loop is asymptotically stable exactly for $-17.03 < k_y < 0.5$, so the instability appears precisely when the drift crosses $-17.03$, as the numerical solution shows.

## History

Rohrs, Valavani, Athans and Stein presented the examples at a conference in the early 1980s and published the full account in the IEEE Transactions on Automatic Control in 1985. They argued that the adaptive algorithms of that time were not robust to unmodeled dynamics. Åström (1983) analyzed the same examples by averaging and related the instability to the frequency content of the command and the phase of the unmodeled dynamics. Ioannou and Kokotović, Egardt, Narendra and Annaswamy, and others developed robust adaptive laws in the same years; Ioannou and Sun (1996) give the unified account.

## References
