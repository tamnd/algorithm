---
tag: 6TE8NF
kind: technique
slug: potential-field-method
name: Potential field method
aliases:
- artificial potential fields
area: games-and-search/planning
level: advanced
summary: Follows the gradient of attractive goal and repulsive obstacle potentials; can trap in local minima.
prereqs: [motion-planning, gradient-descent]
see_also: [configuration-space, hill-climbing, simulated-annealing, breadth-first-search, bug-algorithms, cell-decomposition, probabilistic-roadmap, collision-detection]
sources:
  - paper: doi:10.1177/027836498600500106
    title: Oussama Khatib, Real-time obstacle avoidance for manipulators and mobile robots, International Journal of Robotics Research 5(1), 1986
    locator: pages 90 to 98 (the attractive potential of the goal, the FIRAS repulsive potential with a limit distance, and the forces they give)
  - paper: doi:10.1109/70.163777
    title: Elon Rimon and Daniel E. Koditschek, Exact robot navigation using artificial potential functions, IEEE Transactions on Robotics and Automation 8(5), 1992
    locator: pages 501 to 518 (navigation functions on sphere worlds, with a unique minimum at the goal)
  - paper: doi:10.1177/027836499101000604
    title: Jérôme Barraquand and Jean-Claude Latombe, Robot motion planning, a distributed representation approach, International Journal of Robotics Research 10(6), 1991
    locator: pages 628 to 649 (numerical potential fields on a grid and the randomized path planner that escapes local minima with random walks)
  - paper: doi:10.1109/ROBOT.1991.131810
    title: Yoram Koren and Johann Borenstein, Potential field methods and their inherent limitations for mobile robot navigation, IEEE International Conference on Robotics and Automation (ICRA), 1991
    locator: pages 1398 to 1404 (trap situations, no passage between close obstacles, and oscillations near obstacles and in narrow passages)
  - book: isbn:9780262033275
    title: Howie Choset, Kevin M. Lynch, Seth Hutchinson, George Kantor, Wolfram Burgard, Lydia E. Kavraki and Sebastian Thrun, Principles of Robot Motion, MIT Press, 2005
    locator: Chapter 4 (attractive and repulsive potentials, gradient descent, local minima, the wave-front planner and navigation functions)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 5.4.3 (randomized potential fields), Sections 8.2.2 and 8.4.3 (navigation functions)
---

The potential field method moves a robot along the negative gradient of a function that pulls it toward the goal and pushes it away from the obstacles. Khatib introduced it in 1986 for the real-time control of arms and mobile robots. Each step needs only the distances to the nearby obstacles, so the method is fast and works online. It is not complete: the robot can stop in a local minimum of the field, short of the goal.

## In plain words

Think of the goal as a magnet and every obstacle as a source of a wind that blows away from it. The robot is a small ball. At each moment it takes a short step in the direction of the sum of the pull and the push. Far from all obstacles it heads straight to the goal. Near an obstacle it is pushed aside.

The danger is a place where the pull and the push cancel. For example, an obstacle shaped like a cup that opens away from the goal catches a robot that comes from below. The robot steps into the cup, the goal pulls it up against the bottom of the cup, the cup pushes it back, and it stays there. Nothing in the method tells it to go around.

## When it applies

- The robot must react fast to obstacles that it senses while it moves, and a full plan is too slow or not possible. This was Khatib's setting: a local controller under a higher-level planner.
- The obstacles are few and nearly convex, and they are far apart compared with the reach of the repulsion. Then the local minima are rare.
- A distance to each obstacle, or to the nearest point of each convex piece, is cheap to compute. A [collision detection](/collision-detection/) library that returns distances gives it.
- The method does not apply when a guarantee is needed. It is not complete, and it has no bound on the number of steps. Use a [cell decomposition](/cell-decomposition/) when the dimension is small, or a sampling planner such as the [probabilistic roadmap](/probabilistic-roadmap/) when it is large.

## The template

The robot is a point $q$ in the [configuration space](/configuration-space/), with $d$ coordinates. Let $q_G$ be the goal, $\rho_i(q)$ the distance from $q$ to the C-obstacle $i$, and $\rho_0$ the reach of the repulsion. Khatib's potential is

$$U(q) = \frac{\zeta}{2} \lVert q - q_G \rVert^2 + \sum_{i : \rho_i(q) \le \rho_0} \frac{\eta}{2} \left( \frac{1}{\rho_i(q)} - \frac{1}{\rho_0} \right)^2,$$

where $\zeta > 0$ weights the pull and $\eta > 0$ the push. The repulsion is zero beyond $\rho_0$, grows without bound at the obstacle, and has the gradient $\eta (1/\rho_0 - 1/\rho_i)\, \rho_i^{-2}\, \nabla \rho_i$, where $\nabla \rho_i$ is the unit vector from the nearest obstacle point to $q$. The planner is [gradient descent](/gradient-descent/) on $U$ with a bounded step.

```pseudo id=main
POTENTIAL-FIELD-PLAN(U, q_I, q_G, α, ε, ε_g, N)
L1  q ← q_I, path ← [q]
L2  repeat N times
L3      if ‖q − q_G‖ < ε then return path, "goal"
L4      g ← ∇U(q)
L5      if ‖g‖ < ε_g then return path, "stuck"      ▷ a critical point of U away from the goal
L6      ℓ ← min(α ‖g‖, α)                          ▷ a step of length at most α
L7      while U(q − ℓ g/‖g‖) ≥ U(q) do              ▷ the step climbs or enters an obstacle
L8          ℓ ← ℓ / 2
L9          if ℓ < ε_ℓ then return path, "stuck"
L10     q ← q − ℓ g/‖g‖, append q to path
L11 return path, "stuck"
```

**Why it stays free.** $U = \infty$ inside and on every obstacle, and line L7 accepts only steps that lower $U$. So every accepted point is free. The segments between points are not checked by this test alone. With a step $\alpha$ smaller than the clearance of the obstacles, or with a segment check, the whole path is free.

**What it promises.** $U$ falls at every accepted step and is bounded below by 0, so the run stops at the goal, at a point where the gradient is near zero, or after $N$ steps. A point where the gradient is zero and that is not the goal is a local minimum or a saddle of $U$. Descent from a random start almost never ends at a saddle, but it ends at a local minimum whenever the start lies in its basin. No bound on the number of steps holds in general, and none on whether the goal is reached. The step counts below are measured.

**Cost.** One evaluation of $U$ or $\nabla U$ needs the distance to every obstacle within $\rho_0$. For convex polygons with $n$ edges in total this is $O(n)$ time per evaluation, and the line search of L7 adds a few evaluations per step.

## Classic examples

All runs use $\zeta = \eta = \rho_0 = 1$, the step $\alpha = 0.02$ and the goal tolerance $10^{-3}$.

**A cup trap.** The obstacles form a cup that opens downward: the bar $[3, 7] \times [5, 5.5]$ and the two sides $[3, 3.5] \times [3, 5.5]$ and $[6.5, 7] \times [3, 5.5]$. The goal is $(5, 8)$, above the cup.

| start | result | points on the path | end point |
|---|---|---|---|
| $(5, 1)$ | stuck | 185 | $(5.0, 4.48376)$ |
| $(4.2, 1)$ | stuck | 584 | $(5.0, 4.48376)$ |
| $(1, 1)$ | goal | 725 | $(5, 8)$ |

The trap point lies $0.51624$ below the bar, where $U = 6.621$. On the line $x = 5$ the sides are $1.5$ away, beyond $\rho_0$, so only the goal and the bar act. With $\rho = 5 - y$ the derivative of $U$ in $y$ is zero when

$$8 - y = \frac{1/\rho - 1}{\rho^2},$$

and the root of this equation is the trap point. The potential at 2000 random points around it, at distances up to 0.3, is higher in every case, so it is a true local minimum and not a numerical stop. A start outside the cup, such as $(1, 1)$, goes around the cup and reaches the goal.

**A free run.** The obstacles are the square $[3, 4] \times [2, 4]$ and the triangle $(6, 5)$, $(8, 5.5)$, $(6.5, 7)$. From $(1, 1)$ to $(9, 9)$ the run reaches the goal after 895 points. The path has length 12.028, against 11.314 for the straight line, and its smallest distance to an obstacle is 0.442.

**The wave-front planner.** On a grid of free and blocked cells, give each free cell its number of steps to the goal by [breadth-first search](/breadth-first-search/) from the goal. Every free cell other than the goal that can reach the goal has a neighbor with a smaller number, so descent on this grid potential cannot get stuck. Barraquand and Latombe use such numerical potentials, and Latombe calls the simplest one NF1. It is a discrete navigation function. It is also a full search of the grid, so it costs as much as a grid planner.

## Variations

- **Navigation functions.** Rimon and Koditschek (1992) build a potential on a *sphere world*, a ball with disjoint ball obstacles, that has exactly one minimum, at the goal, and no other minima. Their function is $\varphi = \gamma / (\gamma^k + \beta)^{1/k}$, where $\gamma = \lVert q - q_G \rVert^2$ and $\beta$ is the product of the obstacle functions, for a large enough $k$. Descent then reaches the goal from almost every start. A world that is a diffeomorphic image of a sphere world gets one by the same map. This is the exact form of the method, and it is proved.
- **Saddles cannot be removed.** A smooth function on a plane region with $m$ holes, with its maximum on the boundary, only nondegenerate critical points and one minimum, must have at least $m$ saddle points, by Morse theory. So even a navigation function has critical points other than the goal. It is the minima that it removes.
- **Randomized path planner.** Barraquand and Latombe (1991) run descent until it stops, then take a random walk to leave the basin, and repeat. LaValle (Section 5.4.3) treats it as a sampling method. It is probabilistically complete on a grid, but the number of walks can be very large.
- **Conic attraction.** Far from the goal use $\zeta \lVert q - q_G \rVert$ instead of the square, so the pull does not grow with the distance (Choset et al., Chapter 4).
- **Workspace forces for arms.** For an arm, Khatib applies the forces at a few control points of the links in the workspace and maps them to joint torques through the transpose of the Jacobian. The page on [configuration space](/configuration-space/) explains why a field in the workspace is not the same as a field in $\mathcal{C}$.
- **Escape by search.** A planner can treat the potential as a heuristic and search the grid with it, as [hill climbing](/hill-climbing/) with restarts or [simulated annealing](/simulated-annealing/) do for optimization.

## Pitfalls

- **Local minima.** The cup example. Nonconvex obstacles, and convex obstacles close to each other, create them. A larger $\eta$ or $\rho_0$ does not remove them.
- **No passage between close obstacles.** Two obstacles less than about $2\rho_0$ apart push back from both sides, and the robot may not enter the gap even when it is wide enough (Koren and Borenstein 1991).
- **Oscillation.** In a narrow corridor, or along a wall, the push changes sign from one step to the next, and the path zigzags. A smaller step or a damped controller helps.
- **Goal near an obstacle.** If the goal is within $\rho_0$ of an obstacle, the push moves the minimum of $U$ away from the goal, and the robot stops short of it.
- **Sum over convex pieces.** If a nonconvex obstacle is split into convex pieces, the pushes of the pieces add up where they meet, and the sum has false minima. Use the distance to the whole obstacle.
- **Large steps.** A step longer than the clearance can jump over a thin obstacle. Check the segment of each step, or bound the step.
- **Reading "stuck" as "no path".** The method cannot tell the two apart. The cup example has a path from $(5, 1)$ around the cup, and the method stops anyway. The [Bug algorithms](/bug-algorithms/) solve this case by following the boundary.

## Exercises

1. In the cup example, show that the point found on the line $x = 5$ is a minimum in the $y$ direction. *Answer:* below the trap point the pull of the goal, $8 - y$, is larger than the push $(1/\rho - 1)/\rho^2$, so $U$ falls as $y$ grows; above it, the push grows without bound as $\rho \to 0$, so $U$ rises.
2. A disk obstacle lies between the start and the goal in the plane. Where is a saddle point of $U$? *Answer:* on the line from the goal through the center of the disk, behind the disk, where the pull and the push are opposite and equal. Descent from a start exactly on that line stops there.
3. Show that the grid potential of the wave-front planner has no local minimum other than the goal. *Answer:* a free cell at distance $k > 0$ from the goal has a neighbor on a shortest grid path at distance $k - 1$.
4. Why is it not enough to take $\rho_0$ very small to avoid local minima? *Answer:* with a small $\rho_0$ the push acts only near the boundary, but in the cup the goal still pulls the robot against the bottom of the cup, and the trap moves closer to the bar but does not go away.

## References
