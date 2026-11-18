---
title: The SIMBICON stance hip rule gives the torso exactly its world frame PD torque, and the state machine cycles in order
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact.
The biped is planar, with the generalized coordinates $(x, y, \varphi_0, \varphi_1, \dots, \varphi_4)$: the hip position and the world angles of the torso, the two thighs and the two shins.
A joint between a parent link with angle $\varphi_p$ and a child link with angle $\varphi_c$ has the relative angle $\varphi_c - \varphi_p$.

This file proves only the exact parts of the controller.
That the toy walks without a fall is a measurement in the test, and the gains and the target poses are tuning.
No property of the gait (stability, a limit cycle, robustness to pushes) is proved here or in the paper.

## Joint torques as generalized forces

**Lemma 1.** A torque $\tau$ at a joint between the links $p$ and $c$, acting on $c$ and with the reaction $-\tau$ on $p$, has the generalized forces $Q_{\varphi_c} = \tau$ and $Q_{\varphi_p} = -\tau$, and no part on the other coordinates.

*Proof.*
The virtual work of the joint torque is $\tau\, \delta(\varphi_c - \varphi_p) = \tau\, \delta\varphi_c - \tau\, \delta\varphi_p$.
The generalized force is the coefficient of each virtual displacement. $\square$

## The stance hip rule

**Theorem 1.** Let $\tau_{\text{torso}}$ be any torque and $\tau_B$ any swing hip torque, and set the stance hip torque to $\tau_A = -\tau_{\text{torso}} - \tau_B$ (line L6).
If neither hip torque is clamped by the torque limit, the total generalized force on the torso angle from the joint torques is $Q_{\varphi_0} = \tau_{\text{torso}}$.

*Proof.*
The torso is the parent of both hips and of no knee.
By Lemma 1, $Q_{\varphi_0} = -\tau_A - \tau_B = \tau_{\text{torso}} + \tau_B - \tau_B = \tau_{\text{torso}}$. $\blacksquare$

So the torso feels the PD torque of line L4 on its world angle, as if a motor tied it to the world, and the swing thigh feels $\tau_B$ (plus the knee reaction), which is also a PD on its world angle (line L5).
This is the reason for the rule: neither link has a motor to the world, and the stance leg, which touches the ground, takes the reaction.
When the torque limit is active, the identity fails by the clamped amount; the test checks the identity without the limit.

**Lemma 2.** The swing thigh target of line L3, $\theta_{d} = \theta_{d0} + c_d d + c_v v$, is affine in the horizontal distance $d$ from the stance foot to the hip and in the hip velocity $v$.
For $c_d, c_v > 0$, a hip that is farther in front of the stance foot or moves faster forward gives a swing target that is farther forward.

*Proof.*
The partial derivatives are $c_d$ and $c_v$. $\square$

In the angle convention of the code, a positive thigh angle swings the foot forward, so a larger target places the next foot farther ahead; this is the balance feedback of the paper, and the gains are tuning.

## The state machine

**Theorem 2.** The controller visits the states in the order $0, 1, 2, 3, 0, \dots$.
States 0 and 2 last exactly their duration, rounded up to the next simulation step.
States 1 and 3 end at the first step at which the swing foot is below the ground.
Every end of state 1 or state 3 is counted as one foot strike.

*Proof.*
Line L1 tests the end condition once per step, and the only change of state is $s \leftarrow (s + 1) \bmod 4$ with the clock reset to 0.
A timed state with duration $T$ ends at the first step with clock $\ge T$, and the clock grows by the step $\Delta t$.
A contact state has no duration, so it ends exactly when the swing foot height is below 0, and the code records one strike there. $\blacksquare$

The swing side changes from state 1 to state 2 and from state 3 to state 0, so the legs alternate.
Whether a contact state ever ends is not proved: if the character falls with the swing foot in the air, the state can last to the end of the run, and the test reports the fall.
