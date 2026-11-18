---
tag: MY80RM
kind: algorithm
slug: deepmimic
name: DeepMimic
aliases:
- example-guided deep reinforcement learning of character skills
area: graphics-and-signals/character-animation
level: research
summary: "Train a physics-based character policy by reinforcement learning with a reward for tracking a reference motion clip, with reference state initialization and early termination."
model: real-ram
complexity:
  vars: {k: the control steps of an episode, s: the simulation steps per control step}
  time: {episode: O(k s)}
  space: {extra: O(k)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Xue Bin Peng, Pieter Abbeel, Sergey Levine, Michiel van de Panne]
  note: "Peng, Abbeel, Levine and van de Panne presented DeepMimic at SIGGRAPH 2018."
prereqs: [simbicon, ppo, imitation-learning, reward-function]
see_also: [markov-decision-process, generalized-advantage-estimation, policy-gradient-theorem, actor-critic, trpo, pid-controller, motion-matching, rigid-body-simulation-problem]
sources:
  - paper: doi:10.1145/3197517.3201311
    title: "Xue Bin Peng, Pieter Abbeel, Sergey Levine and Michiel van de Panne, DeepMimic, example-guided deep reinforcement learning of physics-based character skills, ACM Transactions on Graphics 37(4) (SIGGRAPH 2018)"
    locator: "the imitation reward and its weights, the task reward, the PD target actions at 30 Hz with the simulation at 1.2 kHz, Section 6.1 (reference state initialization), Section 6.2 (early termination), and the training with PPO"
  - url: https://arxiv.org/abs/1707.06347
    title: "John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford and Oleg Klimov, Proximal policy optimization algorithms, arXiv 1707.06347, 2017"
    locator: the clipped surrogate objective of PPO
  - url: https://arxiv.org/abs/1506.02438
    title: "John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan and Pieter Abbeel, High-dimensional continuous control using generalized advantage estimation, arXiv 1506.02438, 2015"
    locator: the advantage estimator GAE(lambda)
  - paper: doi:10.1145/1276377.1276509
    title: "KangKang Yin, Kevin Loken and Michiel van de Panne, SIMBICON, simple biped locomotion control, ACM Transactions on Graphics 26(3) (SIGGRAPH 2007), article 105"
    locator: the hand designed PD controllers that learned tracking policies replace
---

DeepMimic trains a neural network policy that makes a simulated character perform a skill from a motion clip: a walk, a backflip, a spin kick.
The character is a rigid body model with PD controlled joints in a physics simulation, so it can fall, be pushed, and react.
At each control step the policy sees the state of the character and the phase of the clip, and outputs target angles for the joint PD controllers.
The reward is high when the simulated pose, joint velocities, end effectors and center of mass are close to the clip at the same phase, and it can include a task term, such as a target direction.
Two simple episode rules make the training work for hard skills: reference state initialization (RSI) starts each episode at a random phase of the clip, in the reference state; early termination (ET) ends an episode when the character falls.
The policy is trained with [PPO](/ppo/); Peng, Abbeel, Levine and van de Panne presented the method in 2018.

## In plain words

You want a game character with a real body to do a backflip like an actor in a captured clip.
You do not write the muscle commands yourself.
Instead, you let a program try again and again, and you give it points for every moment it looks like the actor at the same moment of the clip.
To help it, you let it start some tries in the middle of the flip, not only at the start, so it can learn the landing before it can do the jump.
When it falls on its back, you stop that try at once, so it does not collect points while it lies on the floor.
After many millions of tries, it does the flip, and it can also recover when something pushes it.

## The problem

The problem is a [Markov decision process](/markov-decision-process/).
The state $s$ holds the positions, rotations and velocities of the links, relative to the root, and the phase $\phi \in [0, 1)$ of the clip.
The action $a$ is a target orientation for every joint, tracked by a PD controller in the simulation.
The policy $\pi(a \mid s)$ is a Gaussian whose mean is a neural network; the goal is the largest expected discounted return $E[\sum_k \gamma^k r_k]$.

The reward of the paper is

$$r = w^I r^I + w^G r^G, \qquad w^I = 0.7,\ w^G = 0.3,$$

$$r^I = 0.65\, r^p + 0.1\, r^v + 0.15\, r^e + 0.1\, r^c,$$

with the pose term $r^p = \exp(-2 \sum_j \|\hat q_j \ominus q_j\|^2)$ (the rotation angle between the reference and the simulated joint orientation), the velocity term $r^v = \exp(-0.1 \sum_j \|\hat{\dot q}_j - \dot q_j\|^2)$, the end effector term $r^e = \exp(-40 \sum_e \|\hat p_e - p_e\|^2)$ for hands and feet, and the center of mass term $r^c = \exp(-10 \|\hat p_c - p_c\|^2)$.
A hat marks the reference clip.
The weights and scales are tuning chosen in the paper.
The policy acts at 30 Hz and the simulation runs at 1.2 kHz.

## The algorithm

The training loop collects episodes with the current policy, estimates advantages with GAE($\lambda$) and fits the value function with TD($\lambda$) targets, and updates the policy with the clipped objective of PPO.
One episode is:

```pseudo id=main
EPISODE(π, clip, K)                              ▷ policy, reference, control steps
L1  t ← uniform phase of the clip; s ← the clip state at t   ▷ RSI (or t ← 0)
    for k ← 0 to K - 1
L2      a ← sample from π(· | s, phase of t)     ▷ PD targets in DeepMimic
L3      simulate s for 1/30 s at 1.2 kHz with the PD torques; t ← t + 1/30
L4      rₖ ← 0.7 r^I(s, clip(t)) + 0.3 r^G(s)    ▷ r^I alone if there is no task
L5      if a fall is detected then rₖ ← 0 and end the episode   ▷ ET; the rest is 0
L6  return the rewards and the return Σₖ γᵏ rₖ
```

**Reference state initialization.**
With a fixed start at phase 0, the policy must master the beginning of a skill before it ever sees the later parts; for a backflip, it rarely reaches the landing.
RSI starts each episode at a phase drawn uniformly from the clip, in the reference state of that phase, so every part of the clip appears as a start state from the first iteration.

**Early termination.**
When a fall is detected (in the paper, when certain links such as the torso or head touch the ground), the episode ends and the remaining rewards are zero.
Without it, the data is full of states lying on the ground, and these states still earn a positive reward.

**The code.**
The code in this page is a toy, not DeepMimic: it has no network and no PPO.
The character is one rigid rod on a motor at its base (an inverted pendulum), the reference is a sine wave of the rod angle, and the policy is a given function that outputs a torque directly.
It keeps the reward with the paper's weights and scales (for one joint, the rotation angle of the pose term is the angle difference), the 30 Hz control with 1.2 kHz simulation, RSI and ET.
Its discount $\gamma = 0.95$ and its fall height are toy choices.

## Example

The toy rod has mass 10 kg and length 1 m, the reference is $\hat q(t) = 0.4 \sin(2\pi t / 2)$, and an episode has 60 control steps (2 s).
With $\gamma = 0.95$ the largest possible return is $(1 - 0.95^{60}) / 0.05 = 19.08$.

- A PD policy on the reference with gravity compensation (a hand made stand in for a trained network), started by RSI with seed 7, gets the return 19.02, with a mean reward of 0.996 per step and no fall.
- The zero torque policy from the same start falls and ET ends the episode at step 18, with the return 7.91.
- The zero torque policy from phase 0 falls at step 15. With ET the return is 9.29. Without ET the episode goes on, the rod lies on the ground for 45 of the 60 steps, every one of these steps still earns a reward of at least 0.067, and the return grows to 10.22.

The last case shows why ET matters: without it, lying on the ground pays.

## Correctness

The proof file shows facts about the reward and the episode rules, which follow the paper.

- $0 < r^I \le 1$, with $r^I = 1$ exactly when every pose, velocity, end effector and center of mass difference is zero; the same holds for $r$ with a task reward in $[0, 1]$ (Theorem 1).
- Every RSI start state lies on the reference and has the reward 1, and the start phase is uniform (Theorem 2).
- With ET, no state at or after the fall adds to the return, and every return is in $[0, (1 - \gamma^K)/(1 - \gamma)]$ (Theorem 3).
- Without ET, a fallen state still has a positive reward, because every term of $r^I$ is positive.

Nothing is proved about the learning.
PPO with neural network policies has no convergence guarantee for this problem.
That RSI and ET speed up training and that the result looks like the clip are measurements and visual judgments in the paper.

## Complexity

One episode of $k$ control steps with $s$ simulation steps each costs $O(k s)$ simulation steps plus $k$ policy evaluations, and stores $O(k)$ rewards and states for the update.
In the toy, $s = 40$, so a 2 s episode is 2400 simulation steps.
The paper trains for tens of millions of samples per skill, which takes days of computer time; the cost is dominated by the simulation.

## Properties

- **Stochastic.** The policy samples actions, and RSI samples the start phase; the toy is repeatable only with a fixed seed.
- **Not exact.** A trained policy tracks the clip only approximately, and it can differ from the clip where the clip is not possible for the body.
- **Offline training, online use.** Training needs many episodes, but the trained policy runs in real time, one network evaluation per control step.
- **Physics based.** The character reacts to pushes and to changes of the ground, because the simulation applies the laws of rigid body mechanics and the policy reacts to the state.

## Variants and improvements

- **Tasks.** The task reward $r^G$ adds goals such as a heading, a target to strike, or a ball to throw at a target.
- **Many clips.** The paper also uses a reward that takes the best match over several clips, a skill selector, and a composite of policies.
- **Other bodies.** The paper retargets skills to an Atlas robot model and to non human characters by the same reward.
- **Adversarial imitation.** Later work replaces the hand made tracking reward by a learned discriminator, so that the character imitates the style of a data set instead of one clip at a time.
- **Hand designed control.** [SIMBICON](/simbicon/) uses a state machine and a feedback law in place of a learned policy, with no clip.

## When to use it

Use DeepMimic when a simulated character must perform skills from motion capture or keyframed clips, including dynamic ones like flips and kicks, and must react to forces.
It needs a physics model of the character, a clip for each skill, and much computer time to train.
For a kinematic character that never has to react to forces, [motion matching](/motion-matching/) is much cheaper.

## Pitfalls

- **No ET.** Without early termination, states on the ground fill the data and still pay a reward.
- **No RSI.** With a fixed start, hard skills such as a backflip may never be learned, because the policy never reaches the late phases.
- **Impossible clips.** A clip that the simulated body cannot follow, because of different masses or joint limits, gives a policy that tracks it badly.
- **Reward scales.** The scales inside the exponentials decide how fast each term drops; poor values give a reward that is nearly flat or nearly zero.
- **The phase input.** Without the phase, the policy cannot know which part of the clip to track.
- **The toy.** The code shows the reward and the episode rules only; it does not learn.

## Implementations

## History

Xue Bin Peng, Pieter Abbeel, Sergey Levine and Michiel van de Panne presented DeepMimic at SIGGRAPH 2018.
It joined two lines of work: physics based character controllers such as [SIMBICON](/simbicon/) (2007) and its successors, and deep reinforcement learning for continuous control with [PPO](/ppo/) (2017) and generalized advantage estimation (2015).
Later work by Peng and others replaced the tracking reward with adversarial motion priors and built large libraries of skills on the same base.

## References
