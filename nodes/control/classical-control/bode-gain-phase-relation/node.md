---
tag: BXDHRJ
kind: theorem
slug: bode-gain-phase-relation
name: Bode gain-phase relation
aliases:
- Bode's gain-phase theorem
area: control/classical-control
level: advanced
summary: "For a stable minimum-phase G, the phase at omega_0 is a weighted average of the slope of ln |G| against ln omega. A slope of -20n dB per decade over a wide band gives a phase near -90n degrees."
prereqs: [bode-plot, minimum-phase]
see_also: [phase-margin, loop-shaping, bode-sensitivity-integral, hilbert-transform, nyquist-stability-criterion, time-delay-system, lead-lag-compensator, poles-and-zeros]
sources:
  - paper: doi:10.1002/j.1538-7305.1940.tb00839.x
    title: Hendrik W. Bode, Relations Between Attenuation and Phase in Feedback Amplifier Design, Bell System Technical Journal 19(3), 1940
    locator: pp. 421 to 454 (the phase of a minimum phase network as an integral of the slope of its attenuation against log frequency, and its use in feedback amplifier design)
  - book: "Hendrik W. Bode, Network Analysis and Feedback Amplifier Design, Van Nostrand, 1945"
    locator: the chapters on the relations between the real and imaginary parts of network functions and on gain and phase; no chapter locator confirmed
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Section 10.4, Bode's Relations and Minimum Phase Systems
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 6.5, Bode's Gain-Phase Relationship
---

The Bode gain-phase relation says that for a stable minimum-phase transfer function $G(s)$ the phase at any frequency is fixed by the gain curve: it is a weighted average of the slope of $\ln|G(j\omega)|$ against $\ln\omega$, with a weight that is large near that frequency and small far away. If the gain falls with a constant slope of $-20n$ dB per decade over a wide band around $\omega_0$, the phase at $\omega_0$ is near $-90n$ degrees; this is an approximation, and it is good only when the band is wide. So the gain of a loop cannot fall fast near its crossover frequency without a large phase lag, and this limits every loop shaping design. Hendrik Bode proved the relation in 1940 for feedback amplifiers.

## Statement

**Notation.** $G$ is a real rational transfer function. Frequencies are in rad/s. Write $\omega = \omega_0 e^{\nu}$, so $\nu = \ln(\omega/\omega_0)$ is the distance from $\omega_0$ on a log scale ($\nu = \ln 10 = 2.303$ is one decade). Let $M(\nu) = \ln|G(j\omega_0 e^{\nu})|$ and $\varphi(\omega) = \arg G(j\omega)$ in radians. A slope $dM/d\nu = -n$ is a slope of $-20n$ dB per decade.

**Hypotheses.** $G(s) = s^{\ell}G_0(s)$, where $\ell$ is an integer and $G_0$ is real rational and proper, with all its poles and all its zeros in the open left half plane, and $G_0(0) > 0$. So $G$ is [minimum-phase](/minimum-phase/) in the continuous-time sense: no poles or zeros in the open right half plane, and no time delay. The phase is the continuous branch with $\varphi(0^+) = 90\ell$ degrees.

**Theorem.** For every $\omega_0 > 0$,

$$\varphi(\omega_0) = \frac{1}{\pi}\int_{-\infty}^{\infty} \frac{dM}{d\nu}\, \ln\coth\frac{|\nu|}{2}\, d\nu.$$

For $\ell = 0$ there is the equivalent form

$$\varphi(\omega_0) = \frac{2\omega_0}{\pi}\int_0^{\infty} \frac{\ln|G(j\omega)| - \ln|G(j\omega_0)|}{\omega^2 - \omega_0^2}\, d\omega.$$

The weight $\ln\coth(|\nu|/2)$ is positive, even, and has the total integral $\pi^2/2$. So a constant slope $dM/d\nu = -n$ gives exactly $\varphi = -n\pi/2$, that is, $-90n$ degrees. The weight has 91.9 percent of its mass within one decade of $\omega_0$ and 99.2 percent within two decades.

## In plain words

For a system with no hidden delay and no zeros or poles on the wrong side, the gain curve decides the phase curve. At each frequency, the phase lag is an average of how steeply the gain falls, taken over the frequencies nearby, with the most weight on the closest ones. A gain that falls by a factor of ten for each factor of ten in frequency gives a lag of a quarter turn. A gain that falls twice as fast gives a lag of a half turn, which is where a feedback loop starts to oscillate. So a designer cannot cut the gain of a loop steeply just above its crossover frequency: the lag that comes with the steep fall reaches back to the crossover and eats the margin.

## Proof

**Step 1. The logarithm is analytic.** $G_0$ has no poles or zeros in the half plane $\operatorname{Re} s > -\delta$ for some $\delta > 0$, and this half plane is simply connected. So $F(s) = \ln G_0(s)$ has an analytic branch there, which we fix by $F(0) = \ln G_0(0)$, a real number. Since $G_0$ has real coefficients, $F(\bar s) = \overline{F(s)}$. On the imaginary axis $F(j\omega) = M(\omega) + j\varphi(\omega)$, where $M(\omega) = \ln|G_0(j\omega)|$ is even in $\omega$ and $\varphi$ is odd. If $G_0$ has relative degree $r$, then $|F(s)| \le r\ln|s| + c$ for large $|s|$.

**Step 2. A contour integral.** Fix $\omega_0 > 0$, put $M_0 = M(\omega_0)$ and $\varphi_0 = \varphi(\omega_0)$, and let

$$\Phi(s) = \big(F(s) - M_0\big)\left(\frac{1}{s - j\omega_0} - \frac{1}{s + j\omega_0}\right) = \big(F(s) - M_0\big)\frac{2j\omega_0}{s^2 + \omega_0^2}.$$

$\Phi$ is analytic in the right half plane. Integrate it counterclockwise around the half disk of radius $R$ in the right half plane: down the imaginary axis from $jR$ to $-jR$, with small half circles into the right half plane around $\pm j\omega_0$, and back along the arc. By Cauchy's theorem the integral is 0.

- **The arc.** There $|\Phi| \le (r\ln R + c')\,2\omega_0/(R^2 - \omega_0^2)$ and the length is $\pi R$, so the arc gives 0 as $R \to \infty$.
- **The small half circles.** At $j\omega_0$, $\Phi$ has a simple pole with residue $F(j\omega_0) - M_0 = j\varphi_0$. At $-j\omega_0$ the residue is $-(F(-j\omega_0) - M_0) = -(M_0 - j\varphi_0 - M_0) = j\varphi_0$. Each half circle goes clockwise around its pole and gives $-j\pi \cdot j\varphi_0 = \pi\varphi_0$ in the limit, so together they give $2\pi\varphi_0$.
- **The axis.** With $s = j\omega$, the axis gives $-j\int_{-R}^{R}\Phi(j\omega)\,d\omega = 2\omega_0\int_{-R}^{R}\frac{F(j\omega) - M_0}{\omega_0^2 - \omega^2}\,d\omega$, as a principal value. The part with $j\varphi(\omega)$ is odd in $\omega$ and drops out. The part with $M(\omega) - M_0$ is even and has no singularity, because $M(\omega) - M_0$ vanishes at $\pm\omega_0$. It gives $4\omega_0\int_0^{R}\frac{M(\omega) - M_0}{\omega_0^2 - \omega^2}\,d\omega$.

Adding the three parts and letting $R \to \infty$ gives the second form of the theorem.

**Step 3. The slope form.** Substitute $\omega = \omega_0 e^{\nu}$, so $d\omega = \omega\,d\nu$ and $\omega_0\omega/(\omega^2 - \omega_0^2) = 1/(2\sinh\nu)$. The second form becomes

$$\varphi_0 = \frac{1}{\pi}\int_{-\infty}^{\infty}\frac{M(\nu) - M_0}{\sinh\nu}\,d\nu.$$

For $\nu \ne 0$, $\frac{d}{d\nu}\ln\coth(|\nu|/2) = -1/\sinh\nu$. Integrate by parts on $(-\infty, 0)$ and on $(0, \infty)$. The boundary terms vanish: near 0, $(M - M_0)\ln\coth(|\nu|/2)$ behaves like $\nu\ln(2/|\nu|) \to 0$; at $\pm\infty$, $\ln\coth(|\nu|/2) \approx 2e^{-|\nu|}$ while $M$ grows at most linearly in $\nu$. What is left is the slope form.

**Step 4. The total weight.** For $u > 0$, $\ln\coth u = \ln(1 + e^{-2u}) - \ln(1 - e^{-2u}) = 2\sum_{k\ \text{odd}} e^{-2ku}/k$, so $\int_0^\infty \ln\coth u\,du = \sum_{k\ \text{odd}} 1/k^2 = \pi^2/8$. Hence $\int_{-\infty}^{\infty}\ln\coth(|\nu|/2)\,d\nu = 4 \cdot \pi^2/8 = \pi^2/2$.

**Step 5. Integrators.** For $s^{\ell}$ the phase is the constant $\ell\pi/2$, and $M = \ell\nu + \ell\ln\omega_0$ has the slope $\ell$, so by step 4 the slope form gives $\ell\pi/2$ too. Both sides of the slope form add over products, so the theorem holds for $s^{\ell}G_0$. $\square$

**A check by hand.** For $G = 1/(s + 1)$ at $\omega_0 = 1$, $M(\nu) = -\frac12\ln(1 + e^{2\nu})$ and $dM/d\nu = -e^{2\nu}/(1 + e^{2\nu}) = -\frac12 - \frac12\tanh\nu$. The part $-\frac12\tanh\nu$ is odd and the weight is even, so only $-\frac12$ counts, and the formula gives $\frac{1}{\pi}\cdot(-\frac12)\cdot\frac{\pi^2}{2} = -\pi/4$, which is $-45$ degrees, the true phase of $1/(1 + j)$. At $\omega_0 = 0.5$ and $\omega_0 = 2$ there is no such symmetry, and the slope form, evaluated by quadrature, equals $-26.57$ and $-63.43$ degrees, which are $-\arctan 0.5$ and $-\arctan 2$.

## Consequences

- **The slope at crossover.** For the loop transfer function $L$ at its gain crossover $\omega_c$, the [phase margin](/phase-margin/) is $180 + \arg L(j\omega_c)$ degrees. A slope of $-20$ dB per decade around $\omega_c$ gives a phase near $-90$ degrees and a margin near 90 degrees. A slope of $-40$ dB per decade gives a phase near $-180$ degrees and almost no margin. So a minimum-phase loop needs a slope of about $-20$ to $-30$ dB per decade over roughly a decade around crossover, and it can fall faster only well away from it. This is the rule behind [loop shaping](/loop-shaping/).
- **The cost of a fast cut-off.** High gain at low frequency and low gain at high frequency must be joined by a transition of finite steepness. The relation gives the price in phase of each extra 20 dB per decade, and so it bounds how close the low and high frequency bands can be.
- **Phase lead must come with gain.** A [lead-lag compensator](/lead-lag-compensator/) gives phase lead only by a rising gain over a band. The relation says that no minimum-phase network can give lead without a rise of gain.
- **Non-minimum-phase systems lag more.** A transfer function $G = R(s)e^{-s\tau}$, with $R$ rational with no poles in the closed right half plane and a delay $\tau \ge 0$, can be written $G = G_{mp}B\,e^{-s\tau}$, with $G_{mp}$ minimum-phase and $B$ a product of all-pass factors $(z_i - s)/(\bar z_i + s)$ for the zeros $z_i$ of $R$ in the right half plane. $B$ and $e^{-s\tau}$ have a gain of 0 dB at all frequencies, so $G$ has the gain of $G_{mp}$, and they add only lag for $\omega > 0$. So among systems with a given gain curve, the minimum-phase one has the least phase lag, which is where the name comes from. A [time delay](/time-delay-system/) or a zero in the right half plane therefore limits the crossover frequency that a design can reach.
- **A Hilbert pair.** The relation says that $\ln|G|$ and $\arg G$ on the imaginary axis are the real and imaginary parts of the boundary values of one analytic function, so each is a [Hilbert transform](/hilbert-transform/) of the other in a suitable form. The same fact in optics is the Kramers-Kronig relations.
- **The sensitivity integral.** The [Bode sensitivity integral](/bode-sensitivity-integral/) is a second limit of the same kind, proved by a similar contour argument.

## Tightness

- **A zero in the right half plane.** $1/(s + 1)$ and $(1 - s)/(1 + s)^2$ have the same gain at every frequency, so the formula gives $-45$ degrees for both at $\omega_0 = 1$. The true phase of the second is $\arg(1 - j) - 2\arg(1 + j) = -45 - 90 = -135$ degrees. The extra lag $-2\arctan\omega$ is that of the all-pass factor $(1 - s)/(1 + s)$, which has a gain of 0 dB and slope 0.
- **A delay.** $e^{-s\tau}$ has a gain of 0 dB, so the formula gives 0, but the phase is $-\omega\tau$ radians.
- **A pole in the right half plane.** $1/(s - 1)$ has the same gain as $1/(s + 1)$, but its phase is $-180 + \arctan\omega$ degrees, not $-\arctan\omega$.
- **The $-90n$ rule is approximate.** With a slope of $-n$ only over one decade on each side of $\omega_0$ and 0 outside, the phase is about $0.919$ times $-90n$ degrees; any slope farther away still moves the phase. The rule is exact only for a constant slope at all frequencies, that is, for $s^{-n}$.

## History

Bode derived the relation in "Relations Between Attenuation and Phase in Feedback Amplifier Design" (1940), in the work at Bell Telephone Laboratories on long-distance feedback amplifiers that followed Nyquist's 1932 stability rule. He used it to show how much feedback an amplifier can have over a given band, and he gave the full theory in his 1945 book. The same mathematics, the relation between the real and imaginary parts of a function that is analytic in a half plane, is older; in optics it is known from the work of Kramers and Kronig in the 1920s.

## References
