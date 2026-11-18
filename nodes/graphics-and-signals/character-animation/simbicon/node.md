---
tag: FMSJGE
kind: algorithm
slug: simbicon
name: SIMBICON
aliases:
- simple biped locomotion control
area: graphics-and-signals/character-animation
level: research
summary: Control a simulated biped with a finite state machine of target poses tracked by PD controllers, with balance feedback on the swing hip.
model: real-ram
complexity:
  vars: {n: the number of links of the character}
  time: {control: O(n), simulation_step: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2007
  people: [KangKang Yin, Kevin Loken, Michiel van de Panne]
  note: "Yin, Loken and van de Panne presented SIMBICON at SIGGRAPH 2007 as a simple controller for many biped gaits in 2D and 3D."
prereqs: [pid-controller, forward-kinematics]
see_also: [deepmimic, zero-moment-point, linear-inverted-pendulum-model, capture-point, passive-dynamic-walking, raibert-hopping-controller, hybrid-zero-dynamics, penalty-contact]
sources:
  - paper: doi:10.1145/1276377.1276509
    title: "KangKang Yin, Kevin Loken and Michiel van de Panne, SIMBICON, simple biped locomotion control, ACM Transactions on Graphics 26(3) (SIGGRAPH 2007), article 105"
    locator: "the finite state machine of target poses, the PD control with the torso and swing hip in the world frame, the stance hip rule, the balance feedback law, and the gains kp 300 and kd 30"
  - paper: doi:10.1145/3197517.3201311
    title: "Xue Bin Peng, Pieter Abbeel, Sergey Levine and Michiel van de Panne, DeepMimic, example-guided deep reinforcement learning of physics-based character skills, ACM Transactions on Graphics 37(4) (SIGGRAPH 2018)"
    locator: the later learned controllers that track motion clips with PD targets
---

SIMBICON is a simple controller that makes a simulated two legged character walk, run or skip in a physics simulation.
It has three parts.
A finite state machine with a few states per step holds target poses: for each joint, a target angle.
Each joint tracks its target with a proportional derivative (PD) torque, except that the torso and the swing hip track angles in the world frame, and the stance hip takes the torque that makes this possible.
A balance feedback law moves the target of the swing hip with the horizontal distance $d$ from the stance foot to the center of mass and with the velocity $v$: $\theta_d = \theta_{d0} + c_d d + c_v v$, so the character steps farther forward when it falls forward.
Yin, Loken and van de Panne (2007) showed that this small set of rules gives robust gaits in 2D and 3D; the gait parameters are found by hand or by optimization, and no stability property is proved.

## In plain words

To walk, you do not plan every muscle.
You repeat a few poses: swing a leg forward, plant it, swing the other leg.
SIMBICON does the same: it holds a short list of poses and moves each joint toward the pose of the moment with a spring and a damper.
When the character tips forward, it places the next foot a bit farther ahead to catch itself, and when it tips back, a bit closer.
It also keeps the upper body upright as seen from the world, not as seen from the leg.
That is enough for the simulated character to keep walking, also when something pushes it.

## The problem

The input is a simulated articulated character with joint motors, its state (the positions and velocities of all links), contact with the ground, and a gait: for each state of the machine, a duration or an end condition, the target angles, and the feedback gains $c_d$ and $c_v$.
The task is to compute the joint torques at every simulation step so that the character walks without falling.

The simulation is a model: a rigid body system with joint torques, gravity and a ground contact model.
Its laws are classical mechanics, and its contact force is a penalty model or a constraint solver.
The controller is a heuristic on top of it, and the gains and target poses are tuning.

## The algorithm

```pseudo id=main
SIMBICON-STEP(s, q, q̇, gait)                     ▷ state, positions, velocities
L1  if (s is timed and its clock ≥ T) or (s waits for contact and the swing foot touches)
        s ← (s + 1) mod 4; clock ← 0             ▷ two states per step, the legs alternate
L2  d ← x_com - x_stance foot; v ← ẋ_com          ▷ the code uses the hip in place of the com
L3  θ_swh ← θ_d0 + c_d d + c_v v                 ▷ the balance feedback
L4  τ_torso ← k_p (θ_torso - φ_torso) - k_d φ̇_torso      ▷ PD in the world frame
L5  τ_B ← k_p (θ_swh - φ_swing thigh) - k_d φ̇_swing thigh ▷ swing hip, world frame
L6  τ_A ← -τ_torso - τ_B                         ▷ stance hip
L7  knee torques ← PD on the relative knee angles
L8  return the hip and knee torques, clamped to the torque limit
```

Each state has the targets: the torso angle and the swing hip angle in the world frame, and the knee angles relative to the thigh.
For a walk the paper uses four states: state 0 lasts a fixed time and lifts and swings the leg; state 1 ends when the swing foot touches the ground; states 2 and 3 are the same with the legs swapped.

**The stance hip rule.**
The torso and the swing thigh have no motor that connects them to the world.
The torque $\tau_B$ at the swing hip acts on the swing thigh and, as a reaction, on the torso.
Setting the stance hip torque to $\tau_A = -\tau_{\text{torso}} - \tau_B$ makes the total torque of the two hips on the torso exactly $\tau_{\text{torso}}$, so the torso behaves as if a PD motor tied it to the world; the stance leg, which pushes on the ground, takes the reaction.

**The feedback.**
If the center of mass is ahead of the stance foot ($d > 0$) or moves forward fast ($v$ large), the swing target moves forward and the next step is longer, which slows the body.
The paper applies the same law in the sagittal and in the coronal plane in 3D.

## Example

The code simulates a planar toy with five links: a torso (70 kg, 0.48 m), two thighs (5 kg, 0.45 m) and two shins with point feet (4 kg, 0.50 m).
The ground is a penalty spring and damper with a tangential spring and a Coulomb limit $\mu = 0.8$; the step is symplectic Euler with $\Delta t = 1$ ms, and the torques are limited to 400 N m.
The gains are the paper's $k_p = 300$ and $k_d = 30$ for all joints.
The gait has two states per step:

| state | duration | $c_d$ | $c_v$ | torso | swing hip | swing knee | stance knee |
|---|---|---|---|---|---|---|---|
| 0, 2 | 0.30 s | 0 | 0.20 | 0 | 0.40 | -1.10 | -0.05 |
| 1, 3 | until contact | 2.20 | 0 | 0 | -0.70 | -0.05 | -0.10 |

These values are tuning for the toy, not the table of the paper.

Started at 0.8 m/s, the toy walks for 5 s without a fall, with 14 foot strikes and 5.94 m covered.
The step settles at about 0.42 m and 0.34 s, about 1.2 m/s.
Over 10 s it makes 29 strikes and covers about 12.1 m.
Started at any speed from 0.3 to 1.2 m/s, it also walks.
With $c_d = c_v = 0$ and the same targets, it falls after 0.81 s and 2 strikes.
All these numbers are measurements of this toy, and they show only that the feedback matters here.

## Correctness

The proof file proves the exact parts of the controller.

- A joint torque is a generalized force $+\tau$ on the child angle and $-\tau$ on the parent angle.
- So the stance hip rule of line L6 gives the torso exactly the generalized force $\tau_{\text{torso}}$ of line L4, as long as no hip torque is clamped (Theorem 1).
- The swing target of line L3 is affine in $d$ and $v$, and for positive gains it moves forward when the body is ahead or moves faster.
- The state machine visits the states in the order $0, 1, 2, 3, 0, \dots$; the timed states last their duration rounded up to a simulation step, and each end of a contact state is one foot strike (Theorem 2).

What is not proved is that the character walks.
The paper does not prove stability or a limit cycle; it shows robustness by experiments, such as pushes and slopes.
The code shows only a measurement on one toy.

## Complexity

The controller costs $O(1)$ per joint, $O(n)$ for $n$ links.
The simulation is the expensive part: the code builds the mass matrix of the $n + 2$ coordinates and solves it by Gaussian elimination, $O(n^3)$ per step, and $O(n^2)$ space.
A recursive method such as the articulated body algorithm costs $O(n)$ per step.
With 1 ms steps, one second of motion is 1000 steps.

## Properties

- **Simple.** Each state has a few angles and two gains; a gait is a small table.
- **Robust in practice.** The feedback places the feet to catch the body; the paper reports gaits that survive pushes and changes of the ground.
- **Not exact.** The character follows the targets only roughly, and the walk is a measured behavior, not a guarantee.
- **Online.** Each torque uses only the current state.
- **No reference motion.** Unlike [DeepMimic](/deepmimic/), SIMBICON needs no motion capture; but its gaits look less like a person unless the targets come from data.

## Variants and improvements

- **Optimized gaits.** Search the target angles, durations and gains with an optimizer for speed, style or robustness.
- **Generalized controllers.** Later work by Coros, Beaudoin and van de Panne made the gait parameters depend on the speed and the terrain, with virtual forces and gravity compensation.
- **Tracking data.** Use target poses from motion capture and keep the feedback, to get a more human style.
- **Learned policies.** [DeepMimic](/deepmimic/) replaces the state machine by a neural network policy that outputs PD targets, trained by reinforcement learning to track a clip.
- **Model based balance.** Robotics controllers use the [zero moment point](/zero-moment-point/), the [linear inverted pendulum model](/linear-inverted-pendulum-model/) or the [capture point](/capture-point/) to choose the steps with a model, where SIMBICON uses a linear law with tuned gains.

## When to use it

Use SIMBICON as a first controller for a simulated character in a game or a study of locomotion: it is short, easy to tune by hand, and reacts to pushes.
It is not a model of human walking and not a robot controller with guarantees; for a real robot, the [zero moment point](/zero-moment-point/) and [hybrid zero dynamics](/hybrid-zero-dynamics/) methods have a theory.
For a character that must move like captured motion, use a tracking controller such as [DeepMimic](/deepmimic/).

## Pitfalls

- **The frame of the torso.** A torso PD in the frame of the stance thigh does not keep the torso upright; the world frame rule of line L6 is the core of the method.
- **The center of mass.** The feedback uses the center of mass; the code uses the hip, which is close for this toy with a heavy torso but not in general.
- **Torque limits.** When a hip torque is clamped, the torso no longer gets its PD torque, and a fall can follow.
- **Stiff contact.** A stiff penalty ground needs small time steps; with a large step the feet bounce or sink.
- **Tuning.** Small changes in the table can make a gait fail. Change one value at a time and test from several start speeds.
- **Contact detection.** If the swing foot touches early, for example by scuffing, the state machine switches early, and the step is short.

## Implementations

## History

KangKang Yin, Kevin Loken and Michiel van de Panne presented SIMBICON at SIGGRAPH 2007.
It built on earlier work on hand designed controllers for simulated figures, such as the controllers of Hodgins and coworkers for running and athletics in the 1990s, and on foot placement rules like those of the [Raibert hopping controller](/raibert-hopping-controller/).
The simple rules made it a common base for later work on simulated locomotion, which moved to optimization of the gaits and then to learned policies such as [DeepMimic](/deepmimic/) in 2018.

## References
