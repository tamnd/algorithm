---
tag: M0XJS0
kind: concept
slug: zeno-behavior
name: Zeno behavior
aliases:
- Zeno execution
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: An execution of a hybrid system with infinitely many discrete transitions in finite time, such as a bouncing ball.
prereqs: [hybrid-automata]
see_also: [switched-system, timed-automata, event-triggered-control, sliding-mode-control, hybrid-zero-dynamics, dwell-time-theorem, ode-initial-value-problem, picard-lindelof-theorem]
sources:
  - paper: "Karl Henrik Johansson, Magnus Egerstedt, John Lygeros and Shankar Sastry, On the regularization of Zeno hybrid automata, Systems and Control Letters 38(3), 141-150, 1999"
    locator: the definition of Zeno executions, the water tank example, and the temporal and spatial regularizations
  - book: isbn:9780691153896
    title: Rafal Goebel, Ricardo G. Sanfelice and Andrew R. Teel, Hybrid Dynamical Systems, Modeling, Stability, and Robustness, Princeton University Press, 2012
    locator: the definitions of hybrid time domains and of complete and Zeno solutions, and the bouncing ball example
  - book: isbn:9780817642976
    title: Daniel Liberzon, Switching in Systems and Control, Birkhäuser, 2003
    locator: the introductory chapter on switched and hybrid systems (solutions with infinitely many switches in finite time, chattering and sliding motion)
---

Zeno behavior is an execution of a hybrid system that makes infinitely many discrete transitions in a finite amount of time. The transition times $t_1 < t_2 < \cdots$ get closer and closer and converge to a finite limit, the Zeno time. The standard example is a ball that bounces on the floor and loses a fixed fraction of its speed at each bounce: the bounces come faster and faster, and there are infinitely many of them before a finite time. The name comes from Zeno of Elea, whose paradox of Achilles and the tortoise splits a finite time into infinitely many steps. Zeno behavior is a property of the model, not of the physical system: a real ball comes to rest. But it breaks simulators, which slow down to a stop near the Zeno time, and it breaks proofs that assume time goes to infinity along every execution.

## In plain words

A hybrid model mixes smooth motion with sudden events, such as an impact or a valve that switches. Normally the events are spread out in time. In a Zeno run the events come faster and faster, so an infinite number of them fit into a short, finite time. The model then has no answer for what happens after that time, even though the real object keeps going. A computer simulation has to handle each event one by one, so it gets stuck just before that time. Engineers find this problem in models of bouncing objects, of switched controllers, and of tanks that share one pump. They fix it by changing the model so that events cannot come too close together, or by saying what the model does after the limit time.

## The idea

**Executions.** A [hybrid automaton](/hybrid-automata/) has discrete locations, a continuous state $x$, flows inside each location, and transitions with guards and resets. An execution is a sequence of intervals $[t_0, t_1], [t_1, t_2], \dots$ of continuous flow, separated by discrete transitions. It is **Zeno** if it has infinitely many transitions and

$$t_\infty = \lim_{i \to \infty} t_i = \sum_{i} (t_{i+1} - t_i) < \infty.$$

The limit $t_\infty$ is the Zeno time. The definition includes two different cases:

- the intervals between transitions are positive and shrink, as in the bouncing ball;
- from some point on, the transitions happen at the same instant, with intervals of length zero. This is a livelock of the discrete part, for example two transitions whose guards stay true after each reset.

**Why it matters.** The usual theorems about hybrid systems state properties as $t \to \infty$. On a Zeno execution, time never passes $t_\infty$, so a property such as convergence can hold along the execution and still say nothing about the real system. A safety property checked along all executions can also hold only because the Zeno executions never reach the bad time. A simulator that detects events one by one needs infinitely many steps to reach $t_\infty$, so it stalls or skips events because of rounding.

**Continuing past the Zeno time.** If the state converges as $t \to t_\infty$, the execution can be extended by a rule chosen by the modeler. For the bouncing ball, the natural extension is to rest on the floor. In the framework of hybrid inclusions of Goebel, Sanfelice and Teel, solutions are defined on hybrid time domains, and a Zeno solution is a complete solution whose time stays bounded, so it is a valid object of the theory, not a failure of it.

**Regularization.** Johansson, Egerstedt, Lygeros and Sastry (1999) study two ways to remove Zeno executions by a small change of the model:

- temporal regularization: each discrete transition takes, or must be followed by, at least a time $\varepsilon > 0$;
- spatial regularization: the guards are separated by a hysteresis band of width $\varepsilon$, so the state has to travel a distance before the next switch.

Both give non-Zeno models for $\varepsilon > 0$. As $\varepsilon \to 0$, their executions can converge to different limits after $t_\infty$, so the choice of regularization is a modeling decision. For a state-dependent switched system, the limit is often a sliding motion on the switching surface, the motion that [sliding mode control](/sliding-mode-control/) uses on purpose.

**Ruling it out.** A [switched system](/switched-system/) usually assumes a finite number of switches on every bounded interval, which excludes Zeno signals by definition. The [dwell-time theorem](/dwell-time-theorem/) asks for a positive time between switches, which is stronger. A hybrid model has no Zeno executions if, for example, every cycle of discrete transitions needs a positive amount of time to be traversed. A cycle of zero-duration transitions is a sign of the second kind of Zeno behavior.

## Examples

**Bouncing ball.** A ball falls from height $h_0 = 1$ m with $g = 9.81$ m/s$^2$. At each impact its velocity changes from $v$ to $-e v$ with restitution coefficient $e = 0.5$. The first impact is at $t_1 = \sqrt{2 h_0 / g} \approx 0.4515$ s, and each flight after an impact lasts $e$ times as long as the one before. So $t_\infty = t_1 \left(1 + 2e/(1 - e)\right) = 3 t_1 \approx 1.3546$ s.

| impact | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| time (s) | 0.4515 | 0.9030 | 1.1288 | 1.2417 | 1.2981 | 1.3264 | 1.3405 |
| height of the next bounce (m) | 0.25 | 0.0625 | 0.0156 | 0.0039 | 0.0010 | 0.0002 | 0.0001 |

The heights shrink by the factor $e^2 = 0.25$ at each impact. After $t_\infty$ the model has no execution, while the real ball lies on the floor. The extension $x = 0$, $v = 0$ for $t \ge t_\infty$ is the natural choice.

**Water tanks.** Two tanks lose water at constant rates $v_1 = 2$ and $v_2 = 3$. One inflow of rate $w = 4$ is switched to tank 1 when the level $x_1$ falls to $r_1 = 1$, and to tank 2 when $x_2$ falls to $r_2 = 1$. From $x(0) = (2, 2)$, the total volume falls at the constant rate $v_1 + v_2 - w = 1$. The switching keeps both levels at or above 1, and the switches come faster and faster as both levels approach 1 together. The total reaches $r_1 + r_2 = 2$ at $t = 2$, and this is the Zeno time: no execution goes past it. This is the example of Johansson et al. (1999). Temporal and spatial regularizations give different continuations of it after the Zeno time.

**Zero-time livelock.** A hybrid automaton with two locations, a guard that is always true on both transitions and no reset that falsifies it, can switch back and forth forever at time 0. This is Zeno behavior of the second kind, and it is a modeling error.

**Non-example.** A switched system with a dwell time of 0.1 s has at most $10T + 1$ switches in any interval of length $T$, so it has no Zeno executions.

## Where it is used

- [Hybrid automata](/hybrid-automata/) and [timed automata](/timed-automata/): verification tools must decide whether a model has non-Zeno executions, and the semantics of timed automata usually keeps only the runs in which time diverges.
- [Event-triggered control](/event-triggered-control/): a triggering rule must be proved to have a positive minimum time between events, or the controller can ask for infinitely many updates in finite time.
- [Sliding mode control](/sliding-mode-control/): an ideal relay switching law produces chattering, a Zeno-like infinite switching, and the sliding motion is its limit.
- Mechanical systems with impacts, such as walking robots modeled with [hybrid zero dynamics](/hybrid-zero-dynamics/), granular contact and bouncing parts on a conveyor, need a rule for the Zeno case.
- Simulation of hybrid systems: event-detecting solvers for the [initial value problem](/ode-initial-value-problem/) need a guard against Zeno executions, such as a limit on the number of events in a time window.
- Stability theory of [switched systems](/switched-system/): the class of switching signals is chosen to exclude Zeno signals before any stability result is stated.

## References
