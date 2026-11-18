---
tag: GYSR9F
kind: algorithm
slug: motion-matching
name: Motion matching
aliases:
- learned motion matching
area: graphics-and-signals/character-animation
level: research
summary: Every few frames, search a motion database for the frame whose pose and future trajectory features best match the current state and the user input.
model: real-ram
complexity:
  vars: {f: the number of frames in the database, d: the number of feature dimensions}
  time: {normalize_database: O(f d), search: O(f d), query: O(d)}
  space: {database: O(f d)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 2016
  people: [Simon Clavet, Michael Büttner]
  note: "Clavet presented motion matching for the game For Honor at GDC 2016, after a talk with Büttner in 2015. Holden and coworkers published learned motion matching in 2020."
prereqs: [motion-graph, nearest-neighbor-search, kd-tree]
see_also: [motion-blending, k-nearest-neighbors, two-bone-inverse-kinematics, footskate-cleanup, verbs-and-adverbs, deepmimic, principal-component-analysis]
sources:
  - url: https://www.gdcvault.com/play/1023280/Motion-Matching-and-The-Road
    title: "Simon Clavet, Motion matching and the road to next-gen animation, Game Developers Conference, 2016"
    locator: "the talk as a whole: the search over the database for the best pose and trajectory match, and the blend to the found frame"
  - paper: doi:10.1145/3386569.3392440
    title: "Daniel Holden, Oussama Kanoun, Maksym Perepichka and Tiberiu Popa, Learned motion matching, ACM Transactions on Graphics 39(4) (SIGGRAPH 2020)"
    locator: "the description of basic motion matching, its feature vector and its normalization, before the learned variant"
  - paper: doi:10.1145/566654.566605
    title: "Lucas Kovar, Michael Gleicher and Frederic Pighin, Motion graphs, ACM Transactions on Graphics 21(3) (SIGGRAPH 2002), 473 to 482"
    locator: the precomputed transitions that motion matching replaces by a search at run time
---

Motion matching animates a character from a large database of captured motion with no hand-made state machine and no precomputed transitions.
Every frame of the database gets a feature vector: a few numbers about the current pose (foot positions and velocities, hip velocity) and a few about the near future (where the character will be and which way it will face in a third, two thirds and one second).
At run time, every few frames, the game builds the same vector from the current pose and the trajectory that the player asks for, finds the database frame with the nearest vector, and jumps there with a short [blend](/motion-blending/).
The search is a [nearest neighbor search](/nearest-neighbor-search/) with $f$ frames and $d$ dimensions, $O(f d)$ by brute force, or faster with a [k-d tree](/kd-tree/) or other index.
The page describes the search of Clavet (2016); the alias "learned motion matching" names a later method of Holden and coworkers (2020), which replaces the database by neural networks, and is not the method of this page.

## In plain words

Think of a large library of short films of a person who walks, runs and turns.
Each frame has a label that says where the feet are now and where the person will be one second later.
Many times per second, the game writes the same kind of label for the character on the screen: where its feet are now, and where the player wants it to be one second later.
Then it looks through the library for the frame with the closest label.
If that frame is not the one that would play next anyway, the game cuts to it with a short smooth fade.
The character always plays real captured motion, and it follows the stick within a few frames.

## The problem

The input is a database of $f$ frames with raw feature vectors $v_1, \dots, v_f \in \mathbb{R}^d$, split into groups (for example foot positions, foot velocities, hip velocity, trajectory positions, trajectory directions), a weight $w_g > 0$ for each group, and a set $P$ of playable frames.
Each dimension $k$ has the mean $\mu_k$ and the standard deviation $\sigma_k$ over the database.
The normalized vector of $v$ is $x_k = (v_k - \mu_k)\, w_{g(k)} / \sigma_k$.

A query is a raw vector $v^q$, built from the current pose and the desired future trajectory in the local frame of the character.
The task is to return

$$i^* = \operatorname*{arg\,min}_{i \in P} \sum_{k=1}^{d} (x_{ik} - x^q_k)^2,$$

with ties broken by the lower frame number.
The positions and directions are in the ground frame of the character at that frame (the root projected on the floor, with its heading), so a turn to the left matches every turn to the left in the database.

## The algorithm

```pseudo id=main
MOTION-MATCHING-SEARCH(X, P, vq)               ▷ normalized frames, playable set, raw query
L1  xq ← (vq - μ) ⊙ s                          ▷ sₖ = w_g(k) / σₖ, the group weight over the std
    best ← ∞; i* ← none
L2  for each frame i in P
        s ← 0
L3      for k ← 1 to d: s ← s + (X[i][k] - xq[k])²
L4          if s > best then stop this sum      ▷ the frame cannot win
L5      if s < best then best ← s; i* ← i
L6  return i*
```

The run time loop calls the search.
Each tick, the character advances to the next frame of its clip.
Every $n$ ticks, or when the input changes sharply, the game builds the query from the current frame and the desired trajectory, and searches.
If the result is not the frame that plays anyway, the character jumps to it and blends the pose over a few frames.
Frames near the end of a clip are left out of $P$, so that the character never reaches a clip end before the next search.

Line L4 is an early exit: the partial sums only grow, so once a partial sum is larger than the best full cost the frame cannot win.
A [k-d tree](/kd-tree/) over the normalized vectors gives the same answer and skips whole groups of frames: if the squared distance from the query to a splitting plane is larger than the best cost, no frame on the far side can win.

## Example

**By hand.**
Three normalized frames $X_0 = (0, 0)$, $X_1 = (1, 2)$, $X_2 = (3, 0)$ and the query $x^q = (1, 1)$.
Frame 0: $s = 1$, then $s = 2$; best $= 2$.
Frame 1: $s = 0$, then $s = 1$; best $= 1$, $i^* = 1$.
Frame 2: $s = 4 > 1$ after the first dimension, so line L4 stops the sum.
The search returns frame 1, with cost 1.

**The test database.**
The test builds five clips of 60 frames each at 30 frames per second: a straight walk at 1.2 m/s, a left turn and a right turn at 0.6 rad/s, a run at 2.5 m/s, and standing still.
Each frame has $d = 22$ features: the two foot positions (4 numbers, 2D), the two foot velocities (4), the hip velocity (2), the trajectory positions 20, 40 and 60 frames ahead (6) and the facing directions at the same times (6).
The group weights are 0.75 for the foot positions, 1.5 for the directions and 1 for the rest; these are tuning, chosen for the test.
The last 5 frames of each clip are not playable.

The character starts on frame 0 of the straight walk, with a search every 10 ticks, and the input asks for the features of the left turn from frame 70 on.
At tick 10, the search jumps from frame 10 to frame 80, the exact match.
At ticks 20 and 30, the best frame is the one that plays next, so no jump happens, and the character plays frames 80 to 109 of the turn.
A second run in which every query is the features of the next frame makes no jump at all, as it must.

## Correctness

The proof file shows that the normalized cost equals a weighted squared distance of the raw vectors with the weights $(w_{g(k)} / \sigma_k)^2$, that the partial sums of line L3 never decrease (also in floating point, where each added term is nonnegative), and so that the early exit of line L4 never drops a frame that could win or tie.
Line L6 then returns the brute force answer, with ties broken by the lower frame number, because line L5 replaces the best frame only on a strictly smaller cost and the frames are scanned in increasing order.
It also shows that the k-d tree search returns the same frame: a skipped subtree holds no frame with a cost at most the best cost at the time of the skip, and the best cost only decreases.

These are facts about the search.
The quality of the motion is a different question.
The choice of features, the group weights and the search interval are tuning; that a nearest match looks good and follows the input is a visual heuristic, checked by looking at results and not proved.

## Complexity

Normalizing the database costs $O(f d)$ once.
A query costs $O(d)$ to normalize and $O(f d)$ for the scan in the worst case; the early exit and the tree only lower the constant in practice.
A k-d tree with leaves of a few frames needs $O(f (d + \log f) \log f)$ time to build in the code (a spread over all dimensions and a sort at each level) and $O(f d)$ space for the vectors; in 20 to 30 dimensions its search often visits a large part of the leaves, so engines also use bounding boxes over runs of frames or lower the precision of the vectors.
With $f = 10^5$ frames, about an hour at 30 frames per second, and $d = 27$, one brute force search is $2.7 \cdot 10^6$ multiply and add steps.

## Properties

- **Exact.** All three searches of the code (brute force, the scan with early exit and the k-d tree) return the same frame.
- **Deterministic.** The same state and input give the same frame, also on ties.
- **Online.** Each search uses only the current state and the current input.
- **Data driven.** The character can only play motion that is in the database; there is no new pose except inside a blend.

## Variants and improvements

- **Inertialization.** Instead of a cross fade between the old and the new clip, many engines add an offset that starts at the pose difference and decays to zero, so that only one clip is evaluated.
- **Learned motion matching.** Holden and coworkers (2020) replace the stored features, the search and the pose lookup by three small neural networks, so that the memory no longer grows with the database. In their open source code the features have 27 dimensions: the two foot positions and velocities (12), the hip velocity (3), and the trajectory positions and directions at 20, 40 and 60 frames ahead (6 and 6, in 2D); the mean is taken per dimension and one standard deviation is shared by each group.
- **Tags and costs.** Add a cost for a jump, for a change of tag (walk, run), or for frames that the designers want to avoid.
- **Faster search.** Use bounding boxes over runs of frames, clusters, or a smaller set of key frames; quantize the vectors.
- **Contact cleanup.** After the jump and the blend, plant the feet with [two-bone inverse kinematics](/two-bone-inverse-kinematics/) or [footskate cleanup](/footskate-cleanup/).
- **Motion graphs.** A [motion graph](/motion-graph/) precomputes a few good transitions; motion matching allows a jump from any frame to any frame and decides at run time.

## When to use it

Use motion matching for a player character in a game that must answer the input within a few frames and that has a large, well covered motion capture database.
It reduces the hand work of blend trees and state machines.
It needs much data, and it can only play what was captured; for a character that must react to forces, a physics controller such as [SIMBICON](/simbicon/) or a learned policy such as [DeepMimic](/deepmimic/) fits better.

## Pitfalls

- **Unnormalized features.** Positions in meters, velocities in meters per second and unit directions have different scales. Without the normalization, one group decides every search.
- **Gaps in the data.** If no frame of the database matches the input, the nearest frame can still be far. Plan the capture so that it covers the turns, stops and speeds that the game asks for.
- **Too frequent jumps.** Searching every frame without a cost for a jump can make the character jitter between near equal frames. A search interval of a few frames, a small bonus for the current clip, or both, help.
- **Clip ends.** A frame near the end of a clip can be chosen and then run out before the next search. Leave the last frames out of the playable set.
- **The name.** "Learned motion matching" is a later, different method; do not confuse it with the plain search.

## Implementations

## History

Simon Clavet presented motion matching at GDC 2016 as the animation system of the game For Honor.
It grew out of a 2015 talk by Michael Büttner and Simon Clavet at the nucl.ai conference.
The idea of jumping between similar frames of motion capture data is older: [motion graphs](/motion-graph/) (2002) precompute such jumps.
In 2020, Daniel Holden, Oussama Kanoun, Maksym Perepichka and Tiberiu Popa published learned motion matching, which keeps the same behavior and replaces the database search by neural networks.

## References
