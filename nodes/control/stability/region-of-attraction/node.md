---
tag: PANAAN
kind: definition
slug: region-of-attraction
name: Region of attraction
aliases:
- domain of attraction
- basin of attraction
area: control/stability
level: core
summary: The set of initial states whose solutions converge to an asymptotically stable equilibrium. It is open, connected and invariant, and it is all of R^n exactly in the global case.
prereqs: [asymptotic-stability]
see_also: [region-of-attraction-estimation, asymptotic-stability, lyapunov-function, lyapunov-direct-method, lasalle-invariance-principle, positively-invariant-set, limit-cycle, sum-of-squares-programming]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 8.2, Region of Attraction (the definition, the topological properties, estimates by level sets of Lyapunov functions and the trajectory reversing method in the plane)
  - paper: doi:10.1109/TAC.1985.1104057
    title: "R. Genesio, M. Tartaglia and A. Vicino, On the estimation of asymptotic stability regions: state of the art and new proposals, IEEE Transactions on Automatic Control 30(8), 747-755, 1985"
    locator: the survey of estimation methods, the topological properties of the region and the trajectory reversing method
---

The region of attraction of an [asymptotically stable](/asymptotic-stability/) equilibrium is the set of all initial states whose solutions converge to that equilibrium. Asymptotic stability says only that some neighborhood of the equilibrium is attracted; the region of attraction says how large the attracted set really is. It is the whole state space exactly when the equilibrium is globally asymptotically stable. For a nonlinear system with several equilibria or with limit cycles it is a proper subset, and its boundary is made of whole solutions, for example the stable solutions of saddle points or an unstable [limit cycle](/limit-cycle/). The exact region is rarely computable, so in practice one proves that a given set lies inside it; that is [region of attraction estimation](/region-of-attraction-estimation/).

## Definition

**Setting.** $\dot x = f(x)$, with $f : D \to \mathbb{R}^n$ locally Lipschitz on a domain $D \subseteq \mathbb{R}^n$, $f(0) = 0$, and the origin asymptotically stable. Let $\phi(t, x_0)$ be the solution with $\phi(0, x_0) = x_0$.

**Definition.** The *region of attraction* of the origin is

$$\mathcal{R}_A = \{x_0 \in D : \phi(t, x_0) \text{ is defined for all } t \ge 0 \text{ and } \phi(t, x_0) \to 0 \text{ as } t \to \infty\} .$$

The origin is globally asymptotically stable if and only if $\mathcal{R}_A = \mathbb{R}^n$ (with $D = \mathbb{R}^n$). The same definition applies to any asymptotically stable equilibrium $x^*$, with $\phi(t, x_0) \to x^*$; in the theory of dynamical systems the set is called the basin of attraction, and it is also defined for attractors that are not points.

**Properties.** For an asymptotically stable origin (Khalil 2002, Section 8.2):

1. $\mathcal{R}_A$ is open.
2. $\mathcal{R}_A$ is invariant: a solution that starts in it stays in it for all the time it exists, forward and backward.
3. $\mathcal{R}_A$ is connected.
4. If $\mathcal{R}_A \ne \mathbb{R}^n$, its boundary is invariant: it is made of whole solutions, none of which converges to $0$. It can contain other equilibria, periodic orbits, and solutions that converge to them.

*Proof of 1.* By the definition of asymptotic stability there is a $\delta > 0$ such that the ball $B_\delta$ lies in $\mathcal{R}_A$. Let $x_0 \in \mathcal{R}_A$. There is a time $T$ with $|\phi(T, x_0)| < \delta / 2$. By continuous dependence on initial conditions, $|\phi(T, y) - \phi(T, x_0)| < \delta / 2$ for all $y$ close enough to $x_0$, so $\phi(T, y) \in B_\delta$, and then $\phi(t, y) \to 0$. So a neighborhood of $x_0$ lies in $\mathcal{R}_A$.

*Proof of 2.* If $\phi(t, x_0) \to 0$, then for any $s$ in the interval of existence, $\phi(t, \phi(s, x_0)) = \phi(t + s, x_0) \to 0$.

*Proof of 3.* Each $x_0 \in \mathcal{R}_A$ is joined to the connected set $B_\delta$ by the path $t \mapsto \phi(t, x_0)$, $0 \le t \le T$, which lies in $\mathcal{R}_A$ by property 2. So $\mathcal{R}_A$ is connected.

**Inner estimates by Lyapunov functions.** Let $V$ be a continuously differentiable [Lyapunov function](/lyapunov-function/) for the origin on $D$ with $\dot V(x) < 0$ for $x \in G \setminus \{0\}$, where $G \subseteq D$ is a neighborhood of $0$. If the component $\Omega_c$ of $\{x : V(x) \le c\}$ that contains the origin is bounded, its closure lies in $D$, and $\Omega_c \subseteq G$, then $\Omega_c$ is positively invariant and every solution from it converges to $0$, by the proof of the [direct method](/lyapunov-direct-method/). So $\Omega_c \subseteq \mathcal{R}_A$. With the [invariance principle](/lasalle-invariance-principle/), $\dot V \le 0$ on $\Omega_c$ is enough if no solution other than $0$ stays in $\{\dot V = 0\}$. The largest admissible level is

$$c^* = \min\{V(x) : x \ne 0,\ \dot V(x) = 0\}$$

when $\{\dot V < 0\}$ is the set $G$ and $\Omega_{c^*}$ stays bounded. A quadratic $V = x^T P x$ from the Jacobian $A$, with $A^T P + P A = -Q$, always gives some $c > 0$ when $A$ is Hurwitz, by the proof of the [indirect method](/lyapunov-indirect-method/). Searches over polynomial $V$ by [sum-of-squares programming](/sum-of-squares-programming/) give larger estimates.

**The set where $\dot V < 0$ is not an estimate by itself.** That set is in general not positively invariant: a solution can leave it while $V$ grows again. Only a sublevel set of $V$ that lies inside it is trapped.

## Examples and non-examples

- **Linear systems.** For $\dot x = A x$ with $A$ [Hurwitz](/hurwitz-matrix/), $\mathcal{R}_A = \mathbb{R}^n$. A linear system cannot have a proper region of attraction.
- **One dimension.** $\dot x = -x + x^2$ has the equilibria $0$ and $1$, and $\mathcal{R}_A = (-\infty, 1)$. The boundary is the equilibrium $1$. With $V = x^2$, $\dot V = 2 x^2 (x - 1) < 0$ for $x < 1$, $x \ne 0$, so $c^* = V(1) = 1$ and the estimate is $\{x^2 < 1\} = (-1, 1)$. The estimate is correct but smaller than the true region, because the level sets of $V$ are symmetric and the region is not.
- **A ball.** In $\mathbb{R}^n$, $\dot x = -x (1 - |x|^2)$ has $\frac{d}{dt}|x| = -|x| (1 - |x|^2)$. Solutions with $|x(0)| < 1$ converge to $0$, every point of the unit sphere is an equilibrium, and solutions with $|x(0)| > 1$ grow without bound. So $\mathcal{R}_A$ is the open unit ball, and its boundary is a sphere of equilibria.
- **Van der Pol in reverse time.** $\dot x_1 = -x_2$, $\dot x_2 = x_1 + (x_1^2 - 1) x_2$. The origin is asymptotically stable with the Jacobian $\begin{bmatrix} 0 & -1 \\ 1 & -1 \end{bmatrix}$, and the boundary of $\mathcal{R}_A$ is an unstable limit cycle. In the plane the cycle can be found by integrating the equation backward in time, where it attracts; this is the trajectory reversing method (Khalil 2002, Section 8.2; Genesio, Tartaglia and Vicino 1985). With $Q = I$ the Lyapunov equation gives $P = \begin{bmatrix} 3/2 & -1/2 \\ -1/2 & 1 \end{bmatrix}$, and for $V = x^T P x$,
  $$\dot V = -(x_1^2 + x_2^2) - x_1^3 x_2 + 2 x_1^2 x_2^2 .$$
  A numerical minimization of $V$ over the curve $\dot V = 0$ gives $c^* \approx 2.3045$, so $\{x^T P x < 2.3045\}$ lies in $\mathcal{R}_A$. The eigenvalues of $P$ are $0.69098$ and $1.80902$, so this ellipse contains the disc of radius $\sqrt{2.3045 / 1.80902} \approx 1.129$ around the origin.
- **Damped pendulum.** $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1 - b x_2$, $b > 0$. The region of attraction of $(0, 0)$ is unbounded, and its boundary consists of the saddle points $((2k + 1)\pi, 0)$ and the solutions that converge to them. The energy $V = \tfrac12 x_2^2 + 1 - \cos x_1$ with the invariance principle shows that $\Omega_c$, for every $c < 2$, lies in $\mathcal{R}_A$; the value $2$ is the energy of the upright position.
- **Not defined for an equilibrium that is not asymptotically stable (non-example).** For the harmonic oscillator no solution other than $0$ converges to $0$, so the attracted set is $\{0\}$, which is not open. The properties above need asymptotic stability. For an equilibrium that is attractive but not Lyapunov stable, such as the example on [asymptotic stability](/asymptotic-stability/), the set of attracted initial states can still be defined, but the term region of attraction is normally used only for asymptotically stable equilibria.

## Related definitions

- [Region of attraction estimation](/region-of-attraction-estimation/): methods that prove that a given set lies in $\mathcal{R}_A$, by Lyapunov level sets, sum-of-squares programs or simulation.
- [Positively invariant set](/positively-invariant-set/): a set that solutions do not leave. Every inner estimate by a level set is one.
- [Limit cycle](/limit-cycle/): an isolated periodic orbit; an unstable one often bounds a region of attraction in the plane.
- *Zubov's theorem*: the exact region of attraction is the set where a solution of a certain first-order partial differential equation, Zubov's equation, is less than 1. The equation can rarely be solved in closed form.
- [Barrier certificate](/barrier-certificate/): a function that proves that solutions from one set never reach another; it bounds reachable sets from the outside, while a level set of a Lyapunov function bounds $\mathcal{R}_A$ from the inside.
- *Practical stability*: convergence to a small set from a given set of initial states, used when the true region is too hard to find.

## References
