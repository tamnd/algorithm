---
tag: M9S346
kind: technique
slug: willis-formula
name: Willis formula for planetary gear trains
aliases:
- Willis equation
- epicyclic train value
- formula method for epicyclic trains
area: cad/mechanism-and-assembly-design
level: core
summary: Relates the speeds of sun, ring and carrier by (w_out - w_c)/(w_in - w_c) = train value, which reduces an epicyclic train to a fixed-axis one.
prereqs: [fundamental-law-of-gearing]
see_also: [grubler-formula, instant-center-of-velocity, involute-gear-tooth, degrees-of-freedom-analysis, kinematic-chain]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 9.9 (p. 520, epicyclic or planetary gear trains, with the tabular method on p. 523 and the formula method on p. 527), Section 9.10 (p. 529, efficiency of gear trains) and Section 9.12 (p. 536, differentials)
  - book: "Robert Willis, Principles of Mechanism, John W. Parker, London, 1841"
    title: Principles of Mechanism
    locator: the treatment of epicyclic trains (general locator)
  - book: isbn:9780521815178
    title: Faydor L. Litvin and Alfonso Fuentes, Gear Geometry and Applied Theory, 2nd edition, Cambridge University Press, 2004
    locator: Chapter 23, planetary gear trains
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: the chapter on gear trains, planetary trains (general locator)
---

A planetary gear train, also called an epicyclic gear train, is a gear train in which the axis of at least one gear moves. The planet gears turn on pins of an arm, also called the carrier, and the arm turns about the main axis. A sun gear, an external gear on the main axis, meshes with the planets, and a ring gear, an internal gear on the main axis, meshes with them from outside. The Willis formula gives the speeds: if $F$ and $L$ are the first and last gear of a chain of meshes through the planets, and $A$ is the arm, then

$$\frac{\omega_L - \omega_A}{\omega_F - \omega_A} = e,$$

where all speeds are measured in the fixed frame about parallel axes, and $e$ is the train value of the same gears when the arm is held still.

## In plain words

A planetary train is hard to think about because the planets move around while they turn. The trick is to ride on the arm. Seen from the arm, every gear axis stays in place, and the train is an ordinary train of gears, whose speed ratio is a product of tooth counts. Every speed seen from the arm is the true speed less the speed of the arm.

So you write the ordinary ratio with the arm speed taken away from each gear speed. That gives one equation that links three speeds: the first gear, the last gear and the arm. Know two of them, and the equation gives the third. A planetary train needs two known speeds, often one input and one part held still.

## When it applies

- The gears are spur or helical gears with parallel axes, or bevel gears whose first and last gears turn about the axis of the arm. All speeds in the formula are about axes parallel to the axis of the arm.
- One arm carries all the moving axes of the chain from $F$ to $L$. A train with two arms is split into two such chains that share members.
- The mechanism has two degrees of freedom. For a sun, one planet, a ring, an arm and the frame, the [Grübler formula](/grubler-formula/) counts $5$ links, $4$ turning joints and $2$ gear contacts, so $M = 3(5 - 1) - 2 \cdot 4 - 2 = 2$. Two speeds must be given. When one member is held, one input is enough.
- The formula is about speeds only. It gives no torques and no losses.

## The template

The holes are the chain with the arm held, the change to the frame of the arm, and the choice of the two known speeds.

```pseudo id=main
WILLIS(chain of meshes from F to L, two known speeds among ω_F, ω_L, ω_A)
L1  e ← 1
L2  for each mesh (i, j) along the chain, from F toward L          ▷ hole 1: the train with the arm held
L3      if the mesh is external then e ← e · (−z_i/z_j) else e ← e · (z_i/z_j)
L4  relation: ω_L − ω_A = e · (ω_F − ω_A)                          ▷ hole 2: the frame of the arm
L5  solve the relation for the one unknown speed                    ▷ hole 3: the two known speeds
L6  for each other gear g of the chain: ω_g ← ω_A + e_Fg · (ω_F − ω_A)
```

**Hole 1, the train with the arm held.** With the arm held, each gear turns about a fixed axis. At a mesh of gear $i$ with $z_i$ teeth and gear $j$ with $z_j$ teeth, the pitch circles roll without slip, so $r_i\omega_i = \mp r_j\omega_j$, and with $r = mz/2$ for the common module $m$ this is $\omega_j/\omega_i = \mp z_i/z_j$. The sign is minus for an external mesh, where the gears turn in opposite senses, and plus for an internal mesh. Two gears fixed to one shaft, a compound gear, have the ratio $1$. The train value $e$ is the product along the chain. A gear that meshes on both sides, such as a planet between the sun and the ring, cancels from the product and only sets the sign, which is why it is called an idler.

**Hole 2, the frame of the arm.** In the frame that turns with the arm, the speed of each gear is $\omega - \omega_A$, and hole 1 applies to these speeds.

**Hole 3, the two known speeds.** Line L5 is one linear equation in three speeds. Give any two, and it gives the third. Held members have the speed $0$. Line L6 uses the train value $e_{Fg}$ from $F$ to the gear $g$ to give the speed of every other gear, including the planets.

### Why the formula holds

1. *Angular speeds subtract.* In the plane, a frame that turns at $\omega_A$ adds $-\omega_A$ to the angular speed of every body, wherever its axis is. So a gear with the speed $\omega$ in the fixed frame has the speed $\omega - \omega_A$ in the frame of the arm.
2. *Rolling stays rolling.* At a pitch point the two pitch circles have the same velocity, because they roll without slip. A change of frame subtracts the same velocity, the velocity of the frame at that point, from both, so the two velocities are still equal in the frame of the arm.
3. *In the frame of the arm the train has fixed axes.* The arm carries the pins of the planets, and the sun and the ring turn about the main axis, which is the axis of the arm. So every gear of the chain turns about an axis that is fixed in the frame of the arm, and by steps 1 and 2 its pitch circle rolls on the next one. Hole 1 applies there to each mesh: $\omega_j - \omega_A = \mp (z_i/z_j)(\omega_i - \omega_A)$.
4. *The product.* Multiply the mesh relations along the chain. Each middle factor $\omega_i - \omega_A$ cancels, and $\omega_L - \omega_A = e(\omega_F - \omega_A)$. $\blacksquare$

The product form of line L4 holds even when $\omega_F = \omega_A$. Then $\omega_L = \omega_A$ too, and the whole train turns as one rigid body. The quotient form divides by zero in this case.

### Cost

The train value takes one multiplication for each mesh, so a chain of $n$ meshes costs $O(n)$. With integer tooth counts and rational speeds, exact fractions give exact speeds.

## Classic examples

**A simple planetary train.** Take a sun with $z_S = 24$, three planets with $z_P = 18$ and a ring with $z_R = 60$. The radii of a standard train with one module must close, $r_R = r_S + 2r_P$, so $z_R = z_S + 2z_P = 60$. The chain from the sun to the ring is sun to planet (external) and planet to ring (internal), so

$$e = \left(-\frac{24}{18}\right)\left(+\frac{18}{60}\right) = -\frac{2}{5}.$$

Hold the ring, $\omega_R = 0$, and drive the sun at $\omega_S = 1000$ rpm. Then $0 - \omega_A = -\tfrac25(1000 - \omega_A)$, so $\omega_A = \tfrac{2000}{7} = 285.714$ rpm, and the reduction is $1 + z_R/z_S = 3.5$. For the planet, $e_{SP} = -\tfrac43$ gives $\omega_P = \tfrac{2000}{7} - \tfrac43 \cdot \tfrac{5000}{7} = -\tfrac{2000}{3} = -666.667$ rpm.

**The same train by the tabular method.** Norton's tabular method writes the motion as a sum of two motions. First lock all gears to the arm and turn the whole train at the arm speed. Then hold the arm and turn the gears as a fixed-axis train. The two rows add up to the true speeds.

| motion | sun | planet | ring | arm |
| --- | --- | --- | --- | --- |
| all locked, turn with the arm | $285.714$ | $285.714$ | $285.714$ | $285.714$ |
| arm held | $714.286$ | $-952.381$ | $-285.714$ | $0$ |
| sum | $1000$ | $-666.667$ | $0$ | $285.714$ |

The second row is a fixed-axis train, so its entries have the ratios of hole 1: $-952.381/714.286 = -\tfrac43$ and $-285.714/714.286 = -\tfrac25$. The ring entry in that row must make the sum $0$, which fixes the arm speed.

**Other choices of the held member.** With the same gears:

| held | input | output |
| --- | --- | --- |
| ring | sun $1000$ rpm | arm $285.714$ rpm, ratio $3.5$ |
| arm | sun $1000$ rpm | ring $-400$ rpm, ratio $-2.5$ |
| sun | ring $1000$ rpm | arm $714.286$ rpm, ratio $1.4$ |
| none | sun $1000$ rpm and ring $-200$ rpm | arm $142.857$ rpm |

The arm held is the fixed-axis case, with $\omega_R/\omega_S = e$.

**A differential.** In a bevel gear differential the two side gears $L$ and $R$ have the same number of teeth and turn about the axis of the case, and the case is the arm. With the case held, the side gears turn in opposite senses at the same speed, so $e = -1$ and

$$\omega_{case} = \frac{\omega_L + \omega_R}{2}.$$

A car turning a corner drives the case, and the outer wheel turns faster than the case by as much as the inner wheel turns slower.

**A large ratio from a small difference.** Hold a sun $1$ with $100$ teeth. A compound planet has a gear of $101$ teeth meshed with gear $1$ and a gear of $99$ teeth meshed with an output sun $4$ of $100$ teeth. Two external meshes give $e = \tfrac{100}{101} \cdot \tfrac{99}{100} = \tfrac{99}{101}$, and $\omega_4 - \omega_A = \tfrac{99}{101}(0 - \omega_A)$ gives $\omega_4 = \tfrac{2}{101}\omega_A$, a reduction of $50.5$ in one stage. The two meshes have different center distances in teeth, $201$ and $199$, so they need different modules or a profile shift to share one arm.

## Variations

- **Several planets.** Planets in parallel share the load and do not change the speeds, since each gives the same relation. Equally spaced planets need tooth counts that let every planet mesh with the sun and the ring at once. In the example, $(z_S + z_R)/3 = 28$ is an integer, which is the usual condition for three equally spaced planets in a simple train.
- **Compound and two-stage trains.** For a train with two arms, write one Willis relation for each arm and solve the linear system. Each relation is one equation, and each arm or held member adds one speed.
- **Torques from power balance.** With no losses, the power of the three external members sums to zero and the torques balance, $T_S + T_R + T_A = 0$. With the speeds from the formula these two equations give the torques.
- **Instant centers.** The velocity of each pin of the arm and each pitch point can also be found by drawing, with the [instant center of velocity](/instant-center-of-velocity/) of each planet at its contact with a held gear.

## Pitfalls

- **The sign of the train value.** An internal mesh does not reverse the sense of rotation. Missing the plus sign of the ring mesh in the example gives $e = +\tfrac25$ and an arm speed of $-666.667$ rpm instead of $285.714$ rpm.
- **The arm is not a gear of the chain.** $F$ and $L$ must be gears that the chain connects through meshes. The speed of the arm appears in every term and never in the train value.
- **Planet speeds about their own pins.** Line L6 gives the speed of a planet in the fixed frame. The speed of the planet relative to its pin, which sets the bearing speed, is $\omega_P - \omega_A$, here $-952.381$ rpm, not $-666.667$ rpm.
- **Bevel planets.** In a bevel differential the planets turn about an axis square to the axis of the case. The relation holds for the side gears, which are coaxial with the case, but the speed of a bevel planet is not a number on the same axis.
- **Losses.** The formula is kinematic. The efficiency of an epicyclic train depends on which member is held and on the ratio, and it can be much lower than the efficiency of each mesh (Norton, Section 9.10). Compute it from the power that flows through the meshes in the frame of the arm, not from the overall ratio.

## Exercises

1. For the simple train with $z_S = 24$ and $z_R = 60$, show that the reduction from sun to arm with the ring held is $1 + z_R/z_S$, and that the reduction from ring to arm with the sun held is $1 + z_S/z_R$.
2. Prove the relation $T_S + T_R + T_A = 0$ and find the torque on the held ring when the sun receives $100$ N·m in the example.
3. In the train of the example, what speed must the ring have for the arm to stand still while the sun turns at $1000$ rpm?
4. Show that the differential relation $\omega_{case} = (\omega_L + \omega_R)/2$ follows from the Willis formula with $e = -1$.
5. Find tooth counts near $100$ for a compound planet train with a reduction of $100$ or more in one stage.

## References
