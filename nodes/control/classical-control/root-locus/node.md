---
tag: QR5VW2
kind: technique
slug: root-locus
name: Root locus
aliases:
- Evans root locus
area: control/classical-control
level: intro
summary: The paths of the closed-loop poles, the roots of D(s) + K N(s), as one gain K goes from 0 to infinity. Used to choose the gain and to place compensator poles and zeros.
history:
  year: 1948
  people: [Walter R. Evans]
  note: Evans published the graphical root locus method in 1948 and its use for synthesis in 1950.
prereqs: [feedback-control-loop, poles-and-zeros, second-order-system]
see_also: [root-locus-rules, step-response-specifications, lead-lag-compensator, ziegler-nichols-tuning, routh-hurwitz-criterion, gain-margin, nyquist-stability-criterion, pid-controller]
sources:
  - paper: doi:10.1109/T-AIEE.1948.5059708
    title: W. R. Evans, Graphical analysis of control systems, Transactions of the American Institute of Electrical Engineers 67(1) (1948) 547-551
    locator: the whole paper (the angle and magnitude conditions and the graphical construction of the locus)
  - paper: doi:10.1109/T-AIEE.1950.5060121
    title: W. R. Evans, Control system synthesis by root locus method, Transactions of the American Institute of Electrical Engineers 69(1) (1950) 66-69
    locator: the whole paper (the choice of gain and compensation from the locus)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Chapter 5, The Root-Locus Design Method
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 12, Frequency Domain Design (the section The Root-Locus Method)
---

The root locus of a loop is the set of paths that the closed-loop poles follow as one gain $K$ of the loop goes from 0 to infinity. For the unity feedback loop with the loop transfer function $L(s) = K\,G(s)$ and $G = N/D$, the closed-loop poles are the roots of $D(s) + K\,N(s) = 0$. Evans showed in 1948 that the paths can be drawn by hand from the poles and zeros of $G$ alone, with a few rules, and that one picks the gain from the drawing. The method turns time-domain specifications into a place in the $s$ plane where the dominant poles must be, and shows whether a gain alone can put them there or a compensator is needed. Today the roots are computed, but the rules still explain the shape of the paths and the effect of each added pole and zero.

## In plain words

When you turn up the gain of a feedback loop, its behavior changes: it gets faster, then it starts to ring, and at some gain it may become unstable. The behavior of a linear loop is set by a few numbers called its poles. The root locus is a picture of where these poles go as the gain grows. Each pole starts at a point fixed by the plant and moves along a curve. Some curves end at other fixed points of the plant, and the others run off to infinity along straight lines. From the picture you can read the gain that gives a wanted amount of ringing, the gain at which the loop goes unstable, and whether an extra part in the controller would bend the curves to a better place.

## When it applies

- **One parameter that enters linearly.** The characteristic polynomial must have the form $D(s) + K\,N(s)$ with $K$ real. A gain in a unity feedback loop gives this form. So does any parameter $\alpha$ that enters a characteristic polynomial linearly: write $\chi(s) = D_\alpha(s) + \alpha N_\alpha(s)$ and draw the locus of $N_\alpha/D_\alpha$.
- **Rational $G$.** $G$ is a real rational function with $n$ poles and $m$ zeros, $m \le n$. A time delay $e^{-s\tau}$ gives infinitely many branches; replace it by a Padé approximation first, and know that the result is approximate.
- **One input and one output.** For a multivariable loop, the locus of one gain with all other gains fixed is still defined, but the rules for its shape do not carry over in a simple way.
- **The angle and magnitude conditions.** A point $s$ is on the locus for some $K > 0$ if and only if $\angle G(s) = (2k + 1)\,180$ degrees for an integer $k$, and then $K = 1/|G(s)|$. All rules follow from these two conditions; see [root locus rules](/root-locus-rules/).

## The template

```pseudo id=main
ROOT-LOCUS-DESIGN(G, specs)
L1  write G = N/D with N and D monic; the closed-loop poles are the roots of D + K N
L2  turn specs into a target region for the dominant pair  ▷ zeta ≥ zeta_min, zeta omega_n ≥ sigma_min
L3  draw the locus: the rules for its shape, or the roots of D + K N on a grid of K
L4  if a branch crosses the target region at a point s* then
L5      K ← 1 / |G(s*)|                                     ▷ magnitude condition
L6  else
L7      add a compensator pole or zero to G (lead: pull the locus left; lag: raise the low-frequency gain), then go to L3
L8  find all closed-loop poles for this K, check that the others are far to the left of s*
L9  check the closed-loop zeros, simulate the step response, check the margins; if a check fails, go to L2 or L7
L10 return the controller
```

The target region of line L2 comes from the [step response specifications](/step-response-specifications/) of the [standard second-order system](/second-order-system/): a bound on the overshoot gives a minimum damping ratio, a sector around the negative real axis, and a bound on the settling time gives a minimum value of $\zeta\omega_n$, a half plane. Line L8 is needed because these formulas hold for a dominant pair only. Line L9 is needed because the locus shows only the poles; the zeros of $G$ stay zeros of the closed loop $T = K G/(1 + K G)$ and change the response.

## Classic examples

**A gain on a third-order plant.** Let $G(s) = 1/(s(s + 1)(s + 2))$, so $n = 3$, $m = 0$. The real axis segments of the locus are $(-\infty, -2]$ and $[-1, 0]$. Three asymptotes leave the centroid $-1$ at 60, 180 and 300 degrees. The two branches from 0 and $-1$ meet at the breakaway point $-1 + 1/\sqrt 3 = -0.42265$, at $K = 2/(3\sqrt 3) = 0.3849$, and leave the real axis. They cross the imaginary axis at $\pm j\sqrt 2$ for $K = 6$, which is the gain margin of the loop with $K = 1$ (see [gain margin](/gain-margin/) and the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/)). For an overshoot near 16 percent take $\zeta = 0.5$: the ray at 120 degrees meets the locus at $s^* = -1/3 + j/\sqrt 3$ ($\omega_n = 2/3$ rad/s), and $K = 1/|G(s^*)| = 28/27 = 1.037$. The third closed-loop pole is $-7/3$. A simulation of the step response gives the overshoot 15.54 percent and the 2 percent settling time 12.49 s.

**The ultimate gain for Ziegler-Nichols tuning.** For $G(s) = 1/(s + 1)^3$, the characteristic polynomial is $(s + 1)^3 + K$. The three branches leave the triple pole at 60, 180 and 300 degrees and move along straight lines; two of them cross the imaginary axis where $(1 + j\omega)^3 = -K$, at $\omega_u = \sqrt 3$ rad/s with $K_u = 8$. The ultimate gain 8 and the period $2\pi/\sqrt 3 = 3.628$ s are the inputs of the closed-loop [Ziegler-Nichols tuning](/ziegler-nichols-tuning/) rules.

**A lead compensator.** The first example settles slowly because the dominant pair is at $\zeta\omega_n = 1/3$. To make it about twice as fast with the same damping, aim at $\zeta = 0.5$, $\omega_n = 1.5$, that is $s^* = -0.75 \pm 1.299 j$. The angle of $G(s^*)$ is not $-180$ degrees there, so no gain puts a pole at $s^*$. A [lead-lag compensator](/lead-lag-compensator/) $C(s) = K (s + 1)/(s + 6)$ puts its zero on the plant pole at $-1$ and its pole at $-6$, where the angle condition at $s^*$ holds. The loop $K/(s(s + 2)(s + 6))$ with $K = 117/8 = 14.625$ has the closed-loop polynomial $s^3 + 8 s^2 + 12 s + 14.625 = (s + 6.5)(s^2 + 1.5 s + 2.25)$. The simulated overshoot is 15.81 percent and the 2 percent settling time is 5.52 s instead of 12.49 s. The velocity error constant rises from 0.519 to 1.219 1/s. The cancelled pole at $-1$ is stable, so the cancellation is harmless here; it would not be for an unstable pole.

**Complex poles and a zero.** For $G(s) = (s + 2)/(s^2 + 2 s + 2)$ the poles are $-1 \pm j$. The branch leaves $-1 + j$ at the departure angle 135 degrees, moves on the circle of radius $\sqrt 2$ around the zero $-2$, and meets the real axis at $-2 - \sqrt 2 = -3.414$ for $K = 2 + 2\sqrt 2 = 4.828$. Then one branch goes to the zero and one goes to $-\infty$. Every gain gives a stable loop, and along the circle the damping ratio of the complex pair rises from 0.707 to 1.

## Variations

- **Negative gain.** For $K < 0$ the angle condition becomes $\angle G(s) = k \cdot 360$ degrees. This complementary locus (the zero degree locus) is needed when $G$ has a negative leading coefficient, as with some plants that have a zero in the right half plane.
- **Root contours.** With two parameters, draw a family of loci, one for each value of the second parameter.
- **Discrete time.** For a sampled loop $L(z) = K G(z)$ with the period $h$, the same rules give the locus in the $z$ plane, and the target region is inside the unit circle. The curves of constant damping ratio map to spirals.
- **Other parameters.** The locus over a time constant or a pole location, after the polynomial is rewritten as $D_\alpha + \alpha N_\alpha$, shows the sensitivity of the poles to that parameter.
- **Numerical root locus.** A program finds the roots of $D + K N$ on a grid of $K$ and joins them into branches. This is what design tools draw; the rules then serve to check the plot and to choose the grid near breakaway points and imaginary axis crossings.

## Pitfalls

- **Dominance is assumed.** The formulas for the overshoot and the settling time hold for a pair of poles when all other poles and zeros are far away. In the first example a third pole 7 times farther away still moves the peak time from 5.44 s to 5.93 s. Check by simulation (line L9).
- **Zeros are not on the picture.** A zero of $G$ near the dominant pair raises the overshoot. A zero in the right half plane gives undershoot, and a branch that ends there makes the loop unstable at high gain.
- **Cancelling an unstable pole or zero.** A compensator zero on an unstable plant pole hides an unstable mode: the locus looks fine and the loop is not internally stable (see [feedback control loop](/feedback-control-loop/)). Cancelling a slow stable pole inexactly leaves a slow closed-loop pole with a small residue, a long tail in the step response.
- **The sign and scale of $G$.** The rules assume $N$ and $D$ monic and $K > 0$. If the leading coefficients have opposite signs, the 180 degree locus is the wrong one.
- **Multiple roots are hard to compute.** Near a breakaway point the closed loop has a double root, and computed roots are sensitive there (see [root conditioning](/root-conditioning/)). A plot that jumps between branches near such a point is a numerical effect, not a property of the loop.

## Exercises

1. For $G(s) = 1/(s(s + 4))$, find the gain for $\zeta = 0.5$. (Answer: the closed loop $s^2 + 4 s + K$ has $2\zeta\omega_n = 4$, so $\omega_n = 4$ and $K = 16$.)
2. For $G(s) = 1/(s(s + 1)(s + 2))$, find where the locus crosses the imaginary axis, with the Routh array of $s^3 + 3 s^2 + 2 s + K$. (Answer: $K = 6$, $\omega = \sqrt 2$.)
3. Show that the branches of $G(s) = 1/((s + 1)(s + 3))$ are the segment $[-3, -1]$ and the vertical line $\operatorname{Re} s = -2$. (Hint: the closed-loop poles are $-2 \pm \sqrt{1 - K}$.)

## References
