---
tag: MEEZKQ
kind: technique
slug: loop-transfer-recovery
name: Loop transfer recovery
aliases:
- LQG/LTR
area: control/optimal-and-predictive-control
level: advanced
summary: Tunes the Kalman filter of an LQG design by fictitious input noise so that, for a square minimum phase plant, the loop tends to the LQR loop and recovers its margins.
prereqs: [lqg-control, lqr-stability-margins, kalman-bucy-filter, transmission-zero]
see_also: [lqg-guaranteed-margins-counterexample, loop-shaping, h-infinity-loop-shaping, gain-margin, phase-margin, sensitivity-function, infinite-horizon-lqr, minimum-phase]
sources:
  - paper: doi:10.1109/TAC.1979.1102095
    title: John C. Doyle and Gunter Stein, Robustness with observers, IEEE Transactions on Automatic Control 24(4), 607-611, 1979
    locator: the recovery of the state feedback loop by fictitious noise at the plant input, for minimum phase plants
  - paper: doi:10.1109/TAC.1981.1102555
    title: John C. Doyle and Gunter Stein, Multivariable feedback design, concepts for a classical/modern synthesis, IEEE Transactions on Automatic Control 26(1), 4-16, 1981
    locator: the singular value loop shaping view and loop transfer recovery as a design step
  - paper: doi:10.1109/TAC.1987.1104550
    title: Gunter Stein and Michael Athans, The LQG/LTR procedure for multivariable feedback control design, IEEE Transactions on Automatic Control 32(2), 105-114, 1987
    locator: the tutorial statement of the procedure, for minimum phase and nonminimum phase plants
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, 2nd edition, Wiley, 2005
    locator: the chapter on controller design, with LQG control and loop transfer recovery
---

Loop transfer recovery (LTR) is a design step that gives back to an [LQG](/lqg-control/) controller the robustness of the [LQR](/infinite-horizon-lqr/) loop it is built from. The LQR gain $K$ is fixed first. Then the Kalman filter is designed with fictitious process noise of intensity $q^2$ that enters at the plant input. As $q$ grows, the loop transfer function at the plant input tends, at every frequency, to the LQR loop $K (sI - A)^{-1} B$, and with it the gain margin $(1/2, \infty)$ and the 60 degree phase margin come back. The recovery needs a plant that is square and minimum phase. It fails for a plant with zeros in the right half plane.

## In plain words

A controller that sees the whole state of a machine is very tolerant of errors in the machine model. A controller that must estimate the state from a sensor loses much of that tolerance, because the estimator can be wrong in the same way as the model. LTR tells the estimator to expect large unknown pushes exactly where the motor acts. The estimator then trusts the sensor more and the model less in that direction, and the whole controller behaves more and more like the one that sees the state. The price is a faster estimator, which amplifies sensor noise. The trick works only for machines without delays or inverse responses of a certain kind.

## When it applies

- The plant $G(s) = C (sI - A)^{-1} B$ is square: as many inputs as outputs, $m = p$, and $G(s)$ is invertible as a matrix of rational functions.
- The plant is minimum phase: all its [transmission zeros](/transmission-zero/) have negative real part. Input recovery also needs $(A, B)$ stabilizable and $(C, A)$ detectable.
- The design goal can be stated as a target loop at one point of the loop, usually the plant input, and a state feedback $K$ that gives that target loop is available, often from LQR.
- The sensor noise and the unmodeled dynamics at high frequency allow a fast filter. LTR raises the controller bandwidth.

For a plant with right half plane zeros, LTR still helps at frequencies well below those zeros, but the LQR loop cannot be recovered, and other methods such as [H-infinity loop shaping](/h-infinity-loop-shaping/) are a better fit.

## The template

1. **Target loop.** Choose $K$, for example by LQR with weights $Q$ and $R$, so that $L_T(s) = K \Phi(s) B$ with $\Phi(s) = (sI - A)^{-1}$ has the wanted crossover frequency and shape. By the [LQR stability margins](/lqr-stability-margins/) theorem it has the gain margin $(1/2, \infty)$ and at least 60 degrees of phase margin in each channel when $R$ is diagonal.
2. **Fictitious noise.** For a scalar $q \ge 0$, design the Kalman filter with
$$W(q) = W_0 + q^2 B B^T, \qquad V = V_0,$$
where $W_0 \ge 0$ and $V_0 > 0$ are nominal intensities. The filter gain is $L_o(q) = S(q) C^T V_0^{-1}$ with the filter Riccati solution $S(q)$.
3. **Controller.** Use the LQG controller $C_q(s) = K (sI - A + BK + L_o(q) C)^{-1} L_o(q)$ from $y$ to $-u$, and the loop at the plant input $L_q(s) = C_q(s) G(s)$.
4. **Raise $q$.** Increase $q$ until $L_q(j\omega)$ is close to $L_T(j\omega)$ in the band up to and a little beyond crossover. Do not go further than needed: the controller bandwidth grows with $q$.
5. **Check.** Compute the margins of $L_q$ at the plant input and also at the plant output, and the [sensitivity functions](/sensitivity-function/), since LTR acts only at the point where the target was set.

**Why it works.** Write $L_o = q\, B M + o(q)$. For a square minimum phase plant, the filter Riccati solution satisfies $S(q)/q^2 \to 0$, and the filter equation divided by $q^2$ then gives $L_o V_0 L_o^T / q^2 \to B B^T$, and in fact $L_o(q)/q \to B M$ for a nonsingular matrix $M$ (Doyle and Stein 1979). With the matrix inversion lemma,

$$(\Phi^{-1} + L_o C)^{-1} L_o = \Phi L_o (I + C \Phi L_o)^{-1} \to \Phi B M (G M)^{-1} = \Phi B G^{-1},$$

$$(\Phi^{-1} + L_o C)^{-1} B = \Phi B - \Phi L_o (I + C \Phi L_o)^{-1} C \Phi B \to \Phi B - \Phi B G^{-1} G = 0,$$

at every $s$ that is not a pole of $G$ or a zero of $G$. The controller is $C_q = (I + K (\Phi^{-1} + L_o C)^{-1} B)^{-1} K (\Phi^{-1} + L_o C)^{-1} L_o$, so $C_q(s) \to K \Phi B G^{-1}$ and

$$L_q(s) = C_q(s) G(s) \to K \Phi(s) B = L_T(s).$$

The controller tends to the target loop times the inverse of the plant. The inverse $G^{-1}$ has the plant zeros as poles, so the limit is a stable controller only when those zeros have negative real part. This is why the plant must be minimum phase.

**What is not proved here.** The convergence is pointwise in $s$ and not uniform up to infinite frequency: $L_q$ rolls off like the plant at high frequency while $L_T$ may not. The rate of convergence and the size of $q$ needed depend on the plant, and for multivariable plants on the conditioning of $G$.

## Classic examples

**Double integrator.** $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$, so $G(s) = 1/s^2$, with no finite zeros. The LQR gain for $Q = I$, $R = 1$ is $K = \begin{bmatrix} 1 & \sqrt3 \end{bmatrix}$, and the target loop $L_T(s) = (\sqrt3\, s + 1)/s^2$ has a phase margin of 72.4 degrees and every gain in $(0, \infty)$. With $W = I + q^2 B B^T$ and $V = 1$ the filter gain is

$$L_o(q) = \begin{bmatrix} \sqrt{1 + 2\sqrt{1 + q^2}} \\ \sqrt{1 + q^2} \end{bmatrix},$$

so $L_o/q \to B$. The LQG loop at the plant input recovers step by step:

| $q$ | $L_o^T$ | phase margin | Hurwitz for input gains |
|---|---|---|---|
| 0 | (1.732, 1.000) | 39.0° | $(0, 4.00)$ |
| 3 | (2.706, 3.162) | 39.6° | $(0, 3.87)$ |
| 10 | (4.593, 10.05) | 45.7° | $(0, 4.63)$ |
| 30 | (7.812, 30.02) | 52.9° | $(0, 6.35)$ |
| 100 | (14.18, 100.0) | 59.8° | $(0, 9.94)$ |
| 1000 | (44.73, 1000.0) | 67.7° | $(0, 27.5)$ |
| target | | 72.4° | $(0, \infty)$ |

The upper gain limit first drops a little and then grows without bound. The controller tends to $K \Phi B G^{-1} = \sqrt3\, s + 1$, a PD law with no roll-off, which shows the growth of the controller bandwidth.

**A nonminimum phase plant.** Keep $A$, $B$ and $K$, and measure $y = x_1 - x_2$, so $C = \begin{bmatrix} 1 & -1 \end{bmatrix}$ and $G(s) = (1 - s)/s^2$ has a zero at $s = 1$. The target loop $K \Phi B$ is the same, since it does not depend on $C$. Now $L_o/q \to \begin{bmatrix} 2 \\ 1 \end{bmatrix}$, which is not along $B$, and the recovery fails: the phase margin is 27.6, 26.2, 26.5 and 26.5 degrees for $q = 0, 10, 100, 1000$, and the upper gain limit stays near 1.6.

**Doyle's example.** In the [LQG counterexample](/lqg-guaranteed-margins-counterexample/), the process noise enters along $h = (1, 1)$, not along $B$. Its growth makes the filter fast, but in a direction that destroys the margins instead of recovering them. The plant $1/(s - 1)^2$ has no zeros, so LTR with noise along $B$ applies to it.

## Variations

- **Recovery at the plant output.** The dual procedure fixes the Kalman filter first, with the target loop $C \Phi L_o$ at the plant output, and recovers it by LQR with $Q(q) = Q_0 + q^2 C^T C$ and a fixed $R$ (cheap control). Stein and Athans (1987) present the procedure in this form.
- **Partial recovery.** For a nonminimum phase plant, recover only in a band below the right half plane zeros, and accept the loss above it.
- **Discrete time.** In discrete time the recovery is in general only partial. The current estimator form of the discrete Kalman filter, which uses the newest measurement, gets closer to the target than the predictor form, which adds one step of delay.
- **H2 view.** Stein and Athans (1987) read LTR as the solution of a weighted [H2](/h2-norm/) trade-off between transfer functions. Modern practice often uses [H-infinity loop shaping](/h-infinity-loop-shaping/) for the same goal, with a guaranteed robustness margin and no limit process.

## Pitfalls

- **Forgetting the plant zeros.** For a plant with right half plane zeros, a larger $q$ does not help and can hurt. Compute the transmission zeros first.
- **Recovering at the wrong point.** Noise along $B$ recovers the loop at the plant input. The loop at the output can still have poor margins in a multivariable plant. Check both.
- **Too much recovery.** A large $q$ gives a fast filter and a controller with large gain at high frequency. Sensor noise, sampling and unmodeled dynamics then limit what is safe. Stop when the loop is close enough to the target near crossover.
- **A poor target.** LTR only copies the target loop. If $K$ gives a loop with the wrong bandwidth, the recovered design inherits it.
- **Squaring the plant by force.** Adding or removing channels to get a square plant can create zeros in the right half plane. Check the zeros of the squared plant.

## Exercises

1. For the double integrator with $W = I + q^2 B B^T$ and $V = 1$, show that $L_o = \left(\sqrt{1 + 2\sqrt{1 + q^2}},\ \sqrt{1 + q^2}\right)^T$. (Answer: with $S = \begin{bmatrix} s_1 & s_2 \\ s_2 & s_3 \end{bmatrix}$, the filter equation gives $1 + q^2 - s_2^2 = 0$, $s_3 = s_1 s_2$ and $2 s_2 + 1 - s_1^2 = 0$, and $L_o = (s_1, s_2)^T$.)
2. Show that $L_o(q)/q \to B$ in exercise 1. (Answer: $\sqrt{1 + q^2}/q \to 1$ and $\sqrt{1 + 2\sqrt{1 + q^2}}/q \to 0$.)
3. Show that the LQG controller of the double integrator tends to $\sqrt3\, s + 1$ as $q \to \infty$. (Answer: the limit is $K \Phi B G^{-1} = \frac{\sqrt3\, s + 1}{s^2} \cdot s^2$.)
4. For $C = \begin{bmatrix} 1 & -1 \end{bmatrix}$, find the zero of $G$ and explain why the limit controller $K \Phi B G^{-1}$ cannot be used. (Answer: $G(s) = (1 - s)/s^2$ has a zero at $s = 1$, so $G^{-1}$ has a pole at $s = 1$ that would cancel the plant zero, and the loop would not be internally stable.)
5. State the output recovery procedure for a fixed filter gain $L_o$. (Answer: LQR with $Q = Q_0 + q^2 C^T C$ and fixed $R$; as $q \to \infty$, $G(s) C_q(s) \to C \Phi(s) L_o$ for a square minimum phase plant.)

## References
