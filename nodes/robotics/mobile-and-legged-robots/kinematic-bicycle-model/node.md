---
tag: 6CXJB8
kind: model
slug: kinematic-bicycle-model
name: Kinematic bicycle model
aliases:
- car-like robot model
- Ackermann steering model
area: robotics/mobile-and-legged-robots
level: intro
summary: A car modeled by one front and one rear wheel, with the steering angle and the wheelbase fixing the turning radius.
prereqs: [unicycle-model]
see_also: [unicycle-model, nonholonomic-constraint, dubins-path, reeds-shepp-path, pure-pursuit, stanley-controller, hybrid-a-star, differential-flatness]
sources:
  - book: isbn:9781461414322
    title: "Rajesh Rajamani, Vehicle Dynamics and Control, 2nd edition, Springer, 2012"
    locator: "Section 2.2 (kinematic model of lateral vehicle motion: the bicycle model about the center of gravity with the slip angle, and its use at low speed) and Section 2.3 (the dynamic bicycle model)"
  - paper: doi:10.1109/IVS.2015.7225830
    title: "Jason Kong, Mark Pfeiffer, Georg Schildbach and Francesco Borrelli, Kinematic and dynamic vehicle models for autonomous driving control design, IEEE Intelligent Vehicles Symposium, 2015"
    locator: "the kinematic bicycle model about the center of gravity and its comparison with a dynamic bicycle model in model predictive control"
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 13.3.1 (the car-like robot and its canonical form) and Section 13.3.2 (controllability)"
  - book: isbn:9780521862059
    title: "Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006"
    locator: "Section 13.1.2 (the simple car) and Section 15.3 (shortest paths for the Dubins and Reeds-Shepp cars)"
---

The kinematic bicycle model describes the motion of a car in the plane at low lateral acceleration. It merges the two front wheels into one steered wheel and the two rear wheels into one fixed wheel, on the center line of the car, a wheelbase $L$ apart. Neither wheel slips sideways, so the car turns about a point on the line of the rear axle, and the steering angle $\delta$ fixes the turning radius $L / \tan\delta$. At the center of the rear axle the model is the [unicycle](/unicycle-model/) with turning rate $v\tan\delta / L$: the turning rate is tied to the speed, and the radius has a lower bound $R_{\min} = L / \tan\delta_{\max}$, so the car cannot turn on the spot. It is the model behind the [Dubins](/dubins-path/) and [Reeds-Shepp](/reeds-shepp-path/) paths, behind [hybrid A\*](/hybrid-a-star/), and behind the path trackers [pure pursuit](/pure-pursuit/) and the [Stanley controller](/stanley-controller/). The equations depend on which point of the car is the reference, so each use of the model must say which one it uses.

## The machine

**Parameters.** The wheelbase $L$ (m), the distance from the rear axle to the front axle. For the center of mass form, the distances $l_r$ and $l_f = L - l_r$ (m) from the center of mass to the rear and front axles. The steering limit $\delta_{\max} < \pi/2$ (rad).

**Inputs.** The speed $v$ (m/s), positive forward, and the steering angle $\delta$ (rad) with $|\delta| \le \delta_{\max}$. In a model with continuous curvature, $\delta$ is a state and the steering rate $\dot\delta$ is the input.

**Rear axle form.** The state is the pose $(x, y, \theta)$ of the center of the rear axle, and $v$ is the speed of that point:

$$\dot x = v\cos\theta, \qquad \dot y = v\sin\theta, \qquad \dot\theta = \frac{v\tan\delta}{L}.$$

**Front axle form.** With $(x_f, y_f)$ the center of the front axle and $u$ its speed, the front wheel moves along its own plane:

$$\dot x_f = u\cos(\theta + \delta), \qquad \dot y_f = u\sin(\theta + \delta), \qquad \dot\theta = \frac{u\sin\delta}{L}.$$

The two speeds are related by $v = u\cos\delta$.

**Center of mass form.** With $(x_c, y_c)$ the center of mass and $V$ its speed, the velocity makes the slip angle $\beta = \arctan(l_r\tan\delta / L)$ with the heading:

$$\dot x_c = V\cos(\theta + \beta), \qquad \dot y_c = V\sin(\theta + \beta), \qquad \dot\theta = \frac{V\sin\beta}{l_r} = \frac{V\cos\beta\tan\delta}{L}.$$

This is the form in Rajamani (Section 2.2) and Kong et al. (2015). Here $\beta$ comes from geometry, not from tire slip.

**Constraints.** Two [Pfaffian constraints](/pfaffian-constraint/), both [nonholonomic](/nonholonomic-constraint/): the rear wheel has no velocity along the rear axle, and the front wheel has no velocity along its own axle.

**Ackermann steering.** A real car has two front wheels on a track of width $w$. They turn about the same center only if the inner wheel steers more than the outer one: $\tan\delta_i = L / (R - w/2)$ and $\tan\delta_o = L / (R + w/2)$, with $R$ the radius of the center of the rear axle, so $\cot\delta_o - \cot\delta_i = w / L$. The bicycle wheel, at the middle of the front axle, has $\tan\delta = L / R$, so $\cot\delta$ is the mean of $\cot\delta_i$ and $\cot\delta_o$. A steering linkage that meets this relation is an Ackermann linkage, which is why the model is also called the Ackermann steering model.

**Standing assumptions.** Planar motion on a flat road. Rigid body. The wheels roll without lateral slip, which holds when the lateral acceleration is small compared with the friction limit. Speed and steering angle are inputs, so engine, brake, steering dynamics and tire forces are not in the model. Rajamani notes that the model fits very low speed uses such as automated parking.

## What it counts

The model predicts the path of the car for given speed and steering signals.

**Radius and arcs.** For a constant $\delta \ne 0$, every point of the car moves on a circle about the same center, on the line of the rear axle at distance $R = L / \tan\delta$ from the rear axle center. The front axle center moves on a circle of radius $L / |\sin\delta|$, and the center of mass on one of radius $\sqrt{l_r^2 + R^2}$. For constant $v$ and $\delta$ over a time $t$, the rear axle center moves on an arc through the angle $v t\tan\delta / L$, and the arc formula of the unicycle gives the exact pose. A plan of constant steering pieces is therefore a path of arcs and lines.

**Worked example.** Take $L = 2.7$ m and $\delta_{\max} = 35°$. The minimum radius at the rear axle is $2.7 / \tan 35° = 3.856$ m. At $v = 10$ m/s and $\delta = 0.05$ rad, the turning rate is $10\tan(0.05)/2.7 = 0.1853$ rad/s and $R = 53.95$ m. The front axle center moves on a circle of 54.02 m at 10.013 m/s. With $l_r = 1.35$ m, the slip angle at the center of mass is $\beta = 0.0250$ rad and its radius is 53.97 m. The lateral acceleration is $v^2 / R = 1.853$ m/s², about 0.19 g, so the no-slip assumption is reasonable on a dry road; this is a heuristic judgment, not a bound from the model.

The model does not predict skid, understeer or oversteer, which depend on tire forces. Those need the dynamic bicycle model.

## Relation to other models

- **[Unicycle model](/unicycle-model/).** The rear axle form is the unicycle with $\omega = v\tan\delta / L$, so $|\omega| \le |v| / R_{\min}$.
- **Dubins car and Reeds-Shepp car.** The model at unit speed, forward only or with reverse, with $\rho = R_{\min}$. Their shortest paths are the [Dubins path](/dubins-path/) and the [Reeds-Shepp path](/reeds-shepp-path/).
- **[Differential-drive model](/differential-drive-model/).** Same constraint at the reference point, but no lower bound on the radius.
- **Dynamic bicycle model.** Adds the mass, the yaw inertia and lateral tire forces, often linear in the tire slip angles (Rajamani, Section 2.3). It is needed at higher lateral acceleration. Kong et al. compare the two models as the model inside a predictive controller.
- **Trailers.** A car that pulls trailers adds one angle and one more nonholonomic constraint for each trailer.
- **Path trackers.** [Pure pursuit](/pure-pursuit/) uses the rear axle form, and the [Stanley controller](/stanley-controller/) uses the front axle form.

## Known results in the model

- **Controllability (theorem).** With reverse allowed, the set of allowed velocities at each pose is symmetric about 0, and the Lie bracket of driving and turning gives the sideways direction, as for the unicycle. The car is small-time locally controllable: every pose near the start can be reached by a path that stays near the start. With forward motion only, every pose can still be reached, but nearby poses can need long paths, so it is not small-time locally controllable. With $\delta$ as a state and $\dot\delta$ as an input, the four-state model also satisfies the [Lie algebra rank condition](/lie-algebra-rank-condition/) for $|\delta| < \pi/2$.
- **No continuous stabilizing feedback (theorem).** Like the unicycle, the car fails [Brockett's condition](/brockett-condition/).
- **Flatness (theorem).** The position of the rear axle center is a flat output: the heading is the direction of its velocity, and $\tan\delta = L\kappa$, where $\kappa$ is the curvature of its path. See [differential flatness](/differential-flatness/). Where the planned path has a curvature above $1 / R_{\min}$, the car cannot follow it.
- **Shortest paths (theorems).** Dubins (1957): forward only, the shortest path has at most three pieces, each an arc of radius $R_{\min}$ or a line. Reeds and Shepp (1990): with reverse, a sufficient family of 48 words with at most five pieces and two cusps, reduced to 46 by Sussmann and Tang (1991).
- **Continuous curvature.** With $\delta$ as a state, the curvature of every path is continuous, and a bound on $\dot\delta$ bounds the rate of change of the curvature, so turns start with pieces close to clothoids. Shortest paths in this model are much harder to describe than Dubins paths, and planners use approximations made of lines, arcs and clothoids.

## References
