---
tag: Z1RECF
kind: concept
slug: cam-follower-motion-laws
name: Cam follower motion laws
aliases:
- cam displacement diagram
- cycloidal cam motion
- simple harmonic cam motion
- 3-4-5 polynomial cam law
area: cad/mechanism-and-assembly-design
level: intro
summary: Rise and return laws, such as harmonic, cycloidal and 3-4-5 polynomial, chosen for the follower displacement so velocity and acceleration stay continuous.
see_also: [cam-profile-synthesis, cam-pressure-angle, parametric-continuity, minimum-jerk-trajectory, trapezoidal-velocity-profile, hermite-interpolation]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 8.1 (p. 410, cam terminology), Section 8.2 (p. 416, s v a j diagrams) and Section 8.3 (p. 417, double-dwell cam design, with the fundamental law of cam design on p. 420, simple harmonic motion on p. 421, cycloidal displacement on p. 422 and polynomial functions on p. 439)
  - book: isbn:9780831133672
    title: Robert L. Norton, Cam Design and Manufacturing Handbook, 2nd edition, Industrial Press, 2009
    locator: Section 2.3, the fundamental law of cam design
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: the chapter on cam design, standard cam motions (general locator)
---

A cam follower motion law is the function that gives the lift of a cam follower as the cam turns through one segment of its cycle. A cam is a part with a shaped edge that turns on a shaft, and the follower is the part that rides on that edge and moves in and out. A cycle is cut into segments: a rise, where the follower moves out by the lift $L$; a dwell, where it stands still; and a return, where it moves back. A law is chosen for each rise and return. The choice fixes the velocity, the acceleration and the jerk of the follower, and through them the forces and the vibration of the machine. This page proves the derivatives and the end values of the three classic laws: simple harmonic, cycloidal and the 3-4-5 polynomial.

## In plain words

A cam pushes a rod out, holds it still, and lets it come back. The shape of the cam edge decides how the rod speeds up and slows down. If the push starts with a sudden kick, the rod and the springs shake, the cam wears, and the machine is noisy. A good law starts the push gently and ends it gently, so the rod leaves a rest and comes back to a rest with no jolt. The three classic laws differ in how gentle they are at the two ends. The gentler laws need a larger speed and a larger push in the middle to move the same distance in the same turn of the cam.

## The idea

**Normalized form.** Let the cam turn through the angle $\theta$, and let a rise of lift $L$ take the cam angle $\beta$. Put $x = \theta/\beta \in [0, 1]$ and write the displacement as $s(\theta) = L f(x)$, where $f(0) = 0$ and $f(1) = 1$. By the chain rule, the derivatives with respect to the cam angle are

$$s' = \frac{L}{\beta} f'(x), \qquad s'' = \frac{L}{\beta^2} f''(x), \qquad s''' = \frac{L}{\beta^3} f'''(x).$$

If the cam turns at a constant rate $\omega$, then $\theta = \omega t$, and the velocity, acceleration and jerk in time are $v = \omega s'$, $a = \omega^2 s''$ and $j = \omega^3 s'''$. The four plots of $s$, $v$, $a$ and $j$ over one cycle are the s v a j diagrams. The numbers $C_v = \max |f'|$ and $C_a = \max |f''|$ are the peak velocity and acceleration coefficients of the law. A return of the same length uses $1 - f(x)$, which changes the sign of every derivative.

**The fundamental law of cam design.** Norton states it as follows: the cam-follower function must be continuous through the first and second derivatives of displacement across the entire interval (360°), and as a corollary the jerk must be finite across the entire interval. A dwell has $s' = s'' = s''' = 0$. So a rise between two dwells obeys the law exactly when $f'$ and $f''$ are zero at both ends. If $f''$ is not zero at an end, the acceleration jumps there, and the jerk is a Dirac delta, that is, infinite.

**Simple harmonic motion.** The follower moves as the projection of a point that turns at a constant rate on a half circle:

$$f(x) = \tfrac12(1 - \cos \pi x).$$

Differentiation gives

$$f' = \tfrac{\pi}{2}\sin \pi x, \qquad f'' = \tfrac{\pi^2}{2}\cos \pi x, \qquad f''' = -\tfrac{\pi^3}{2}\sin \pi x.$$

At the ends, $f(0) = 0$, $f(1) = 1$ and $f'(0) = f'(1) = 0$, so the displacement and the velocity are continuous with the dwells. But $f''(0) = \pi^2/2$ and $f''(1) = -\pi^2/2$. The acceleration jumps from $0$ to $\pi^2 L/(2\beta^2)$ at the start of the rise and from $-\pi^2 L/(2\beta^2)$ to $0$ at the end. So the jerk is infinite at both ends, and the law fails the fundamental law of cam design next to a dwell. Its coefficients are $C_v = \pi/2 \approx 1.571$ at $x = \tfrac12$ and $C_a = \pi^2/2 \approx 4.935$ at the ends.

**Cycloidal motion.** The follower moves as a point on a circle that rolls once along a line, seen from the side:

$$f(x) = x - \frac{\sin 2\pi x}{2\pi}.$$

Differentiation gives

$$f' = 1 - \cos 2\pi x, \qquad f'' = 2\pi \sin 2\pi x, \qquad f''' = 4\pi^2 \cos 2\pi x.$$

At the ends, $f(0) = 0$, $f(1) = 1 - 0 = 1$, $f'(0) = f'(1) = 1 - 1 = 0$ and $f''(0) = f''(1) = 0$. So the displacement, the velocity and the acceleration are all continuous with the dwells, and the law obeys the fundamental law of cam design. The jerk is $4\pi^2$ at both ends, against $0$ in the dwell, so the jerk jumps by the finite amount $4\pi^2 L/\beta^3$. The coefficients are $C_v = 2$ at $x = \tfrac12$ and $C_a = 2\pi \approx 6.283$ at $x = \tfrac14$ and $x = \tfrac34$.

**The 3-4-5 polynomial.** Ask for the polynomial of least degree with $f(0) = 0$, $f(1) = 1$ and $f' = f'' = 0$ at both ends. Six conditions fix a polynomial of degree 5. Since $f'$ has a double zero at $0$ and at $1$, it has the form $f' = c\,x^2(1 - x)^2$, and $f(1) = 1$ gives $c \int_0^1 x^2(1-x)^2\,dx = c/30 = 1$. So $c = 30$, and integration gives

$$f(x) = 10x^3 - 15x^4 + 6x^5.$$

Differentiation gives

$$f' = 30x^2(1 - x)^2, \qquad f'' = 60x(1 - x)(1 - 2x), \qquad f''' = 60 - 360x + 360x^2.$$

The factors show $f'(0) = f'(1) = 0$ and $f''(0) = f''(1) = 0$, so the law obeys the fundamental law of cam design. The jerk is $f'''(0) = f'''(1) = 60$, so it jumps by the finite amount $60L/\beta^3$ at each dwell. The peak velocity is $C_v = f'(\tfrac12) = 30/16 = 1.875$. The peak acceleration is where $f''' = 0$, that is $6x^2 - 6x + 1 = 0$, so $x = (3 - \sqrt3)/6 \approx 0.2113$. There $x(1 - x) = \tfrac16$ and $1 - 2x = 1/\sqrt3$, so $C_a = 60 \cdot \tfrac16 \cdot \tfrac1{\sqrt3} = 10/\sqrt3 \approx 5.774$. This is the same quintic as the [minimum-jerk trajectory](/minimum-jerk-trajectory/) of robot motion planning.

**Higher order.** Ask also for $f''' = 0$ at both ends. Eight conditions give degree 7, $f' = 140x^3(1-x)^3$, and $f(x) = 35x^4 - 84x^5 + 70x^6 - 20x^7$, the 4-5-6-7 polynomial. Its jerk is continuous with the dwells, and the price is $C_v = 140/64 = 2.1875$ and $C_a \approx 7.513$.

The pattern of the laws is a trade. Each extra order of smoothness at the ends raises the peak velocity and the peak acceleration for the same lift and the same cam angle.

## Examples

Take a rise of $L = 20$ mm over $\beta = 90°$ $= \pi/2$ rad, with the cam at 300 rpm, so $\omega = 10\pi$ rad/s and the rise takes $0.05$ s. The peaks are $v_{\max} = C_v L\omega/\beta$ and $a_{\max} = C_a L\omega^2/\beta^2$, with $L\omega/\beta = 400$ mm/s and $L\omega^2/\beta^2 = 8000$ mm/s².

| Law | $C_v$ | $C_a$ | peak $v$ (mm/s) | peak $a$ (m/s²) | at the dwell ends |
| --- | --- | --- | --- | --- | --- |
| simple harmonic | $\pi/2$ | $\pi^2/2$ | 628.3 | 39.48 | $a$ jumps by 39.48 m/s², $j$ infinite |
| cycloidal | $2$ | $2\pi$ | 800.0 | 50.27 | $a = 0$, $j$ jumps by 6317 m/s³ |
| 3-4-5 polynomial | $1.875$ | $10/\sqrt3$ | 750.0 | 46.19 | $a = 0$, $j$ jumps by 9600 m/s³ |
| 4-5-6-7 polynomial | $2.1875$ | $7.513$ | 875.0 | 60.11 | $a = 0$, $j = 0$ |

The jerk values come from $j = \omega^3 L f'''/\beta^3$ with $L\omega^3/\beta^3 = 160\,000$ mm/s³: $4\pi^2 \cdot 160 = 6317$ m/s³ for the cycloidal law and $60 \cdot 160 = 9600$ m/s³ for the 3-4-5 law. The harmonic law has the smallest peaks, and it is the only one with an acceleration jump.

**Non-example: harmonic motion with no dwell.** Let the follower rise over $\beta$ with the harmonic law and return at once over the next $\beta$ with $1 - f$. At the joint, the rise ends with $f''(1) = -\pi^2/2$ and the return starts with $-f''(0) = -\pi^2/2$. The values agree, so there is no jump. The whole cycle is one cosine, $s = \tfrac{L}{2}(1 - \cos(\pi\theta/\beta))$, which is the motion of a round cam turning on an off-center shaft (an eccentric). The jump of the harmonic law is a property of the joint to a dwell, not of the law alone.

## Where it is used

- [Cam profile synthesis](/cam-profile-synthesis/) turns a chosen law into the cam outline, and the law must be continuous for the outline to be smooth.
- The [cam pressure angle](/cam-pressure-angle/) depends on $s'$, so a law with a large $C_v$ needs a larger cam to keep the angle small.
- Cam design programs offer more laws: modified sine and modified trapezoid, which join cycloidal pieces and constant pieces to lower $C_a$, and polynomials fitted to many conditions, which are [Hermite interpolation](/hermite-interpolation/) of the end values. Norton covers these laws in Section 8.3.
- Motion profiles of servo drives and robots use the same laws. The 3-4-5 polynomial is the minimum-jerk profile, and the [trapezoidal velocity profile](/trapezoidal-velocity-profile/) is the constant-acceleration law that fails the fundamental law of cam design.
- The continuity conditions are those of [parametric continuity](/parametric-continuity/): obeying the law means that the whole cycle is a $C^2$ function of $\theta$.

## References
