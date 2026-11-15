---
tag: 0W0JD2
kind: algorithm
slug: iterative-learning-control
name: Iterative learning control
aliases:
- ILC
area: control/robust-and-adaptive-control
level: advanced
summary: Improves the input of a system that repeats a task, by learning from the error of the last trial so the error falls from trial to trial.
model: real-ram
complexity:
  vars: {J: the number of trials, N: the number of samples per trial, n: the order of the plant}
  time: {worst: O(J (N n^2 + N^2))}
  space: {extra: O(N^2)}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1984
  people: [Suguru Arimoto, Sadao Kawamura, Fumio Miyazaki]
  note: "Arimoto, Kawamura and Miyazaki proposed the update of the input from the error of the last trial for robot manipulators and proved its convergence; Uchiyama had published a similar idea in Japanese in 1978."
prereqs: [adaptive-control, state-space-representation, spectral-radius, matrix-norms]
see_also: [toeplitz-system-solving, internal-model-principle, h-infinity-norm, lqr-problem, model-predictive-control, feedforward-control, extremum-seeking-control, z-transform]
sources:
  - paper: doi:10.1002/rob.4620010203
    title: "Suguru Arimoto, Sadao Kawamura and Fumio Miyazaki, Bettering operation of robots by learning, Journal of Robotic Systems 1(2), 1984"
    locator: "pages 123 to 140 (the learning update from the error of the last trial and its convergence)"
  - paper: doi:10.1109/MCS.2006.1636313
    title: "Douglas A. Bristow, Marina Tharayil and Andrew G. Alleyne, A survey of iterative learning control, IEEE Control Systems Magazine 26(3), 2006"
    locator: "pages 96 to 114 (the lifted system, asymptotic and monotonic convergence, the P-type, plant inversion and norm-optimal designs, the Q-filter)"
  - paper: doi:10.1049/ip-cta:19960244
    title: "Notker Amann, David H. Owens and Eric Rogers, Iterative learning control for discrete-time systems with exponential rate of convergence, IEE Proceedings, Control Theory and Applications 143(2), 1996"
    locator: "pages 217 to 224 (the norm-optimal learning law)"
  - paper: doi:10.1080/002071700405905
    title: "Richard W. Longman, Iterative learning control and repetitive control for engineering practice, International Journal of Control 73(10), 2000"
    locator: "pages 930 to 954 (the large transient growth of simple learning laws and the frequency domain condition for monotonic decay)"
---

Iterative learning control (ILC) is a method for a system that does the same task again and again from the same initial state: after each trial it corrects the whole input signal with the error signal of that trial, so that the error falls from trial to trial. The update is $u_{j+1} = Q(u_j + L e_j)$, where $j$ is the trial number, $e_j = y_d - y_j$ is the tracking error over the trial, and $L$ and $Q$ are filters or matrices. Because the correction is computed between trials, $L$ can use the error at later times of the trial, which a causal feedback controller cannot do. ILC learns a feedforward input for one fixed reference; a feedback loop is usually still present to reject disturbances that do not repeat.

## In plain words

Think of a robot arm that draws the same curve every few seconds. On the first try, the arm misses the curve a little. After the try, you look at the whole record of the miss: at each moment, how far off and in which direction. For the next try, you change the push at each moment a little, in the direction that removes the miss. You can use what happened just after each moment, because the try is already over. After many tries the arm follows the curve almost exactly. The method only works if every try starts the same way and the task is the same. If the push is changed too much at once, the miss can grow very large before it shrinks.

## The problem

The plant is $x(k+1) = Ax(k) + Bu(k)$, $y(k) = Cx(k)$, with one input, one output and the first Markov parameter $CB \ne 0$ (relative degree one). Each trial starts at the same state $x(0) = x_0$ and has $N$ samples with the sampling period $h$. The input $u(0), \dots, u(N-1)$ gives the outputs $y(1), \dots, y(N)$. With the vectors $u_j, y_j \in \mathbb{R}^N$ of trial $j$, the lifted model is
$$y_j = P u_j + d,\qquad P = \begin{pmatrix} CB & 0 & \cdots & 0\\ CAB & CB & \cdots & 0\\ \vdots & & \ddots & \\ CA^{N-1}B & \cdots & CAB & CB\end{pmatrix},$$
where $d$ is the response to $x_0$. $P$ is lower triangular Toeplitz. Given a reference $y_d \in \mathbb{R}^N$, find inputs $u_j$ with $e_j = y_d - y_j \to 0$ as $j \to \infty$, without knowing $P$ exactly.

## The algorithm

Choose the learning matrix $L$ and the filter $Q$ (often $Q = I$). Common choices of $L$:

- **P-type (Arimoto):** $L = \gamma I$, that is $u_{j+1}(k) = u_j(k) + \gamma e_j(k + 1)$ in terms of the unlifted signals.
- **Plant inversion:** $L = \hat P^{-1}$ for a model $\hat P$ of the plant.
- **Norm-optimal:** $L = (P^TP + wI)^{-1}P^T$ with a weight $w > 0$. It minimizes $\|e_{j+1}\|^2 + w\|u_{j+1} - u_j\|^2$.

```pseudo id=main
ILC(trial, y_d, u₀, L, Q, J)                     ▷ J updates
L1  u ← u₀
L2  for j ← 0 to J do
L3      y ← run one trial with input u            ▷ same initial state each trial
L4      e ← y_d - y                               ▷ the error over the whole trial
L5      u ← Q (u + L e)                           ▷ between trials
L6  return u and the errors of all trials
```

With $Q = I$, the error obeys $e_{j+1} = (I - PL)\,e_j$ exactly, because $d$ and $y_d$ are the same in every trial.

## Example

Take $y(k+1) = a\,y(k) + u(k)$ with $y(0) = 0$, so $P_{ik} = a^{i-k}$ for $i \ge k$. The trial has $N = 30$ samples, the reference is $y_d(k) = \sin(\pi k/30)$ for $k = 1, \dots, 30$, and $u_0 = 0$, so $\|e_0\|_2 = 3.873$. With the P-type law:

| $a$ | $\gamma$ | $\|I - \gamma P\|_2$ | $\max_\omega \lvert 1 - \gamma \bar P(e^{\mathrm{i}\omega})\rvert$ | behavior of $\|e_j\|_2$ |
|---|---|---|---|---|
| 0.9 | 1 | 7.0487 | 9 | grows to $1.1 \times 10^6$ at trial 14, zero after trial 30 in exact arithmetic |
| 0.9 | 0.5 | 3.1213 | 4 | grows to 54.14 at trial 4, then decays; $7.0 \times 10^{-4}$ at trial 30 |
| 0.5 | 0.5 | 0.6666 | 2/3 | decreases in every trial; 0.379 after one trial |

All three cases converge, because $I - \gamma P$ is lower triangular with the diagonal $1 - \gamma$, so its spectral radius is $|1 - \gamma| < 1$. Only the last one converges monotonically in the 2-norm. The first case is nilpotent: $I - P$ is strictly lower triangular, so $(I - P)^{30} = 0$ and the error is exactly zero after 30 updates (the tests check this in Fraction arithmetic), but on the way it grows by a factor of about $3 \times 10^5$. These are measurements of the stated runs.

The norm-optimal law with $a = 0.9$ removes the transient growth. For $w = 1$, $\|I - PL\|_2 = 0.7826$ and $\|e_j\|_2$ is $3.873, 0.0948, 0.0194, 0.0099$ for $j = 0$ to 3. For $w = 0.1$, $\|I - PL\|_2 = 0.2647$ and $\|e_1\|_2 = 0.0115$.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows four facts (theorems). First, with $Q = I$ and the same initial state, $e_{j+1} = (I - PL)e_j$, so $e_j = (I - PL)^je_0$. Second, $e_j \to 0$ for every $e_0$ if and only if the [spectral radius](/spectral-radius/) $\rho(I - PL) < 1$; for the P-type law this is $|1 - \gamma CB| < 1$, a condition that does not depend on $A$. Third, if $\|I - PL\|_2 < 1$, then $\|e_{j+1}\|_2 \le \|I - PL\|_2\,\|e_j\|_2$, so the decay is monotonic; for $L = \gamma I$ a sufficient condition is $\max_\omega|1 - \gamma \bar P(e^{\mathrm{i}\omega})| < 1$, where $\bar P(z) = \sum_{k \ge 0} CA^kB\,z^{-k} = z\,C(zI - A)^{-1}B$ is the transfer function of the plant advanced by one sample (for $A$ with all eigenvalues inside the unit circle), because a finite section of a Toeplitz operator has a norm at most the peak of its symbol. Fourth, the norm-optimal law gives $I - PL = w(PP^T + wI)^{-1}$, whose 2-norm is $w/(\sigma_{\min}^2 + w) < 1$, where $\sigma_{\min} > 0$ is the smallest singular value of $P$.

## Complexity

In the real-RAM model, one trial costs $O(Nn^2)$ to simulate with a dense $A$ of order $n$, and one update with a dense $L$ costs $O(N^2)$. So $J$ trials cost $O(J(Nn^2 + N^2))$, and storing $L$ takes $O(N^2)$. The P-type law needs only $O(N)$ per update. The norm-optimal matrix costs $O(N^3)$ once. With int or Fraction data the implementation is exact, so the property exact is true; the entries grow in size with the number of trials.

## Properties

- **Asymptotic convergence.** Theorem: $e_j \to 0$ for all $e_0$ if and only if $\rho(I - PL) < 1$.
- **Monotonic convergence.** Theorem: $\|I - PL\|_2 < 1$ gives a decay in every trial with that factor. Without it, the error can grow by many orders of magnitude before it decays, as in the example.
- **Robustness.** Theorem: if the true plant is $P = (I + \Delta)\hat P$ with a model $\hat P$ and an output multiplicative error $\Delta$, the law $L = \hat P^{-1}$ gives $I - PL = -\Delta$, so it converges monotonically in the 2-norm if $\|\Delta\|_2 < 1$.
- **Q-filter trade-off.** With a filter $Q$, the input obeys $u_{j+1} = Q(I - LP)u_j + QL(y_d - d)$, so it converges if $\rho(Q(I - LP)) < 1$ (theorem). A low pass $Q$ makes this hold under high frequency model errors and noise, but the limit error is in general not zero; the bias is set by $Q$ (rule of thumb: put the bandwidth of $Q$ where the model is still good).
- **Repetition needed.** The error recursion holds only when the initial state, the reference and the disturbances are the same in every trial. A disturbance that changes from trial to trial is not learned.

## Variants and improvements

- **PD-type and phase lead laws.** Use $L$ with a time shift of several samples or a derivative; this compensates the phase lag of the plant.
- **Q-filtered ILC.** Use a zero phase low pass $Q$ to stop the learning at frequencies where the model is poor (Bristow, Tharayil and Alleyne 2006).
- **Norm-optimal ILC.** Amann, Owens and Rogers (1996) minimize a quadratic cost in each trial; the decay is monotonic in the 2-norm. It is close to [LQR](/lqr-problem/) over the trial.
- **Repetitive control.** For a periodic task with no reset between periods, the learning runs continuously; its design rests on the [internal model principle](/internal-model-principle/).
- **Nonlinear and adaptive ILC.** For nonlinear plants with a Lipschitz condition, contraction mapping arguments give similar results.

## When to use it

Use ILC when a system repeats the same motion from the same initial state, for example robot manipulators, wafer stages, printers, machine tools, and batch processes in chemistry. It suits cases where feedback alone cannot reach the required accuracy because of delays and phase lag, but the error repeats. If the task changes in every run, use a feedback design or [model predictive control](/model-predictive-control/). If a good model is available, plant inversion or a norm-optimal law learns in a few trials; with no model, a small P-type gain with a Q-filter is a safer start.

## Pitfalls

- **Transient growth.** $\rho(I - PL) < 1$ alone allows the error to grow by a large factor before it decays; in practice this damages the plant. Check $\|I - PL\|_2 < 1$ or the frequency condition.
- **Non-repeating initial state.** A different $x_0$ in each trial adds an error term that learning cannot remove.
- **Noise.** The law adds the measured error to the input, so the noise accumulates in $u$ trial after trial; use a Q-filter or a learning gain that decreases with $j$.
- **Relative degree.** With $CB = 0$ the first output does not depend on the first input; shift the error by the relative degree, otherwise $P$ is singular.
- **Error sign.** This page uses $e = y_d - y$. With $e = y - y_d$ the sign of $L$ changes.

## Implementations

## History

Uchiyama (1978) published in Japanese a method that corrects the input of a robot from the error of the last motion. Arimoto, Kawamura and Miyazaki (1984) gave the update in its standard form, proved its convergence, and introduced the name learning control for robots; their paper is the usual start of the field. Amann, Owens and Rogers (1996) introduced the norm-optimal law with monotonic convergence. Longman (2000) explained the large transient growth of simple laws in practice and gave the frequency domain condition. Bristow, Tharayil and Alleyne (2006) wrote the standard survey.

## References
