---
tag: XRTTYC
kind: algorithm
slug: multiple-hypothesis-tracking
name: Multiple hypothesis tracking
aliases:
- MHT
- Reid's algorithm
area: computer-vision/visual-tracking
level: advanced
summary: Keep a tree of association hypotheses over several frames, score them by likelihood, and prune, so that hard choices are made only when later data decide them.
solves: [data-association, multi-object-tracking]
model: real-ram
complexity:
  vars: {M: the number of hypotheses kept, n: the number of tracks in a hypothesis, m: the number of measurements in a frame, d: the dimension of a state}
  time: {worst: O(M² m³ (n + m) + M n d³), average: O(M² m³ (n + m) + M n d³), best: O(M² m³ (n + m) + M n d³)}
  space: {extra: O(M (n d² + m (n + m)))}
properties: {deterministic: true, exact: false, local: false, iterative: false, online: true}
history:
  year: 1979
  people: [Donald B. Reid]
  note: Reid gave the hypothesis-oriented algorithm and its recursive probability formula in IEEE Transactions on Automatic Control. Cox and Hingorani made it practical in 1996 by generating only the best children of each hypothesis with Murty's k-best assignments.
prereqs: [data-association, kalman-filter, track-gating, hungarian-algorithm, global-nearest-neighbor-association]
see_also: [joint-probabilistic-data-association, network-flow-tracking, assignment-problem, three-dimensional-matching, beam-search, best-first-branch-and-bound, priority-queue, multi-object-tracking]
sources:
  - paper: doi:10.1109/TAC.1979.1102177
    title: Donald B. Reid, An algorithm for tracking multiple targets, IEEE Transactions on Automatic Control 24(6), 1979, 843 to 854
    locator: the whole paper (hypothesis generation, the probability of a hypothesis, track initiation and pruning)
  - paper: doi:10.1109/34.481539
    title: Ingemar J. Cox and Sunita L. Hingorani, An efficient implementation of Reid's multiple hypothesis tracking algorithm and its evaluation for the purpose of visual tracking, IEEE Transactions on Pattern Analysis and Machine Intelligence 18(2), 1996, 138 to 150
    locator: the whole paper (the cost matrix of a hypothesis and the k best children by Murty's algorithm)
  - paper: "Katta G. Murty, An algorithm for ranking all the assignments in order of increasing cost, Operations Research 16(3), 1968, 682 to 687"
    locator: the whole paper (the partitioning of the solution space)
  - paper: doi:10.1109/MAES.2004.1263228
    title: Samuel S. Blackman, Multiple hypothesis tracking for multiple target tracking, IEEE Aerospace and Electronic Systems Magazine 19(1), 2004, 5 to 18
    locator: the whole paper (hypothesis-oriented and track-oriented MHT, scoring and pruning)
  - paper: "Chanho Kim, Fuxin Li, Arridhana Ciptadi and James M. Rehg, Multiple hypothesis tracking revisited, IEEE International Conference on Computer Vision (ICCV), 2015"
    locator: the whole paper (track-oriented MHT with appearance models on video benchmarks)
---

Multiple hypothesis tracking, or MHT, keeps several explanations of the measurements alive at once and decides between them only when later frames make the answer clear. A hypothesis is a complete story so far: which measurements form which tracks, which were false alarms, and which started new targets. In each frame every hypothesis is extended in every way the new measurements allow, each extension gets a probability by Reid's formula, and the least likely hypotheses are dropped. Donald Reid gave the method in 1979. Cox and Hingorani showed in 1996 that the best extensions of a hypothesis are the best solutions of one [assignment problem](/assignment-problem/), so they can be found in order with Murty's k-best method instead of by listing all of them. With one hypothesis kept, MHT is [GNN](/global-nearest-neighbor-association/) with likelihood costs. With many, it can recover from a decision that looked best in one frame but was wrong.

## In plain words

A detective with three suspects and a few clues does not name the culprit after the first clue. She keeps a short list of the stories that fit, each with a rough score. Each new clue can split a story into several, and stories that no longer fit drop off the list. MHT does this with measurements. A blip on the screen might be the plane we already follow, a new plane, or noise, so each story splits into several. The list is kept short by keeping only the few best stories, and the tracker reports the best story so far. If a later frame shows that the second-best story was right, the tracker switches to it, and the past is fixed at the same time.

## The problem

The input is a sequence of frames, each with a set of measurements $z_1, \ldots, z_m$, and a model: a [Kalman filter](/kalman-filter/) per target, a detection probability $p_D$, a density $\beta_{FT}$ of false alarms and a density $\beta_{NT}$ of new targets per unit of measurement space, and a gate $\gamma$. A hypothesis $h$ is a partition of all past measurements into tracks and false alarms. Reid's formula gives its probability recursively. If a child $h'$ of $h$ assigns the new measurements so that $N_{DT}$ of the $n$ tracks of $h$ are detected, $N_{FT}$ measurements are false alarms and $N_{NT}$ start new targets, then

$$
P(h') \propto P(h) \; p_D^{N_{DT}} (1 - p_D)^{n - N_{DT}} \; \beta_{FT}^{N_{FT}} \; \beta_{NT}^{N_{NT}} \prod_{(i, j)} \mathcal N(z_j; \hat z_i, S_i),
$$

with the product over the pairs of a track and its measurement, and the constant the same for all children in the frame. The output in each frame is the track set of the most probable hypothesis.

## The algorithm

```pseudo id=main
MHT-STEP(the hypotheses h with log weights w_h, the measurements z_1..z_m, the number M kept)
L1   for each hypothesis h: predict every track of h, with ẑ_i and S_i
L2       C ← the m × (n + 2m) matrix of h: c_ji ← -ln(p_D N(z_j; ẑ_i, S_i) / (1 - p_D)) if gated, else ∞; c_j,NT_j ← -ln β_NT; c_j,FT_j ← -ln β_FT
L3       the M assignments of least cost of C, by Murty's method
L4       for each such assignment a: a child of h with log weight w_h + n ln(1 - p_D) - cost(a)
L5   keep the M children of highest weight over all hypotheses, and normalize their weights
L6   in each kept child: update the assigned tracks, start the new targets, delete tracks missed too often
L7   return the tracks of the hypothesis of highest weight
```

A row of $C$ is a measurement. It can go to a track in its gate, to its own new-target column, or to its own false-alarm column. Other entries are $\infty$, so each measurement has exactly one role, and each track takes at most one measurement. The cost of an assignment is the negative log of Reid's factor for that child, divided by the factor $(1 - p_D)^n$ of a child with no detection. Line L4 puts the factor back.

**Murty's method.** It finds the assignments of a matrix in order of cost. Solve the matrix with the [Hungarian algorithm](/hungarian-algorithm/) and put the solution in a [priority queue](/priority-queue/). Pop the cheapest solution $a$ and report it. Then split the rest of its subproblem into disjoint parts: in part $t$, the free rows before row $t$ keep their columns in $a$, and row $t$ may not use its column $a(t)$. Solve each part and push it. Every other assignment of the subproblem falls in exactly one part.

Line L6 holds the track management, and it is a heuristic. The code deletes a track after 3 misses in a row and starts a new track at a measurement assigned to its new-target column, with zero velocity.

## Example

**One frame by hand.** Two tracks predict $\hat z_A = (1, 0)$ and $\hat z_B = (1, 2)$, both with $S = 0.653 I$. The measurements are $z_1 = (1.2, 0.3)$, $z_2 = (1.0, 1.4)$ and $z_3 = (0.8, 2.2)$, and $p_D = 0.8$, $\beta_{FT} = 0.02$, $\beta_{NT} = 0.002$. The cost matrix, with the columns A, B, the three new-target columns and the three false-alarm columns, is

$$
C = \begin{pmatrix}
0.125 & 2.268 & 6.215 & \infty & \infty & 3.912 & \infty & \infty \\
1.526 & 0.301 & \infty & 6.215 & \infty & \infty & 3.912 & \infty \\
3.761 & 0.087 & \infty & \infty & 6.215 & \infty & \infty & 3.912
\end{pmatrix}.
$$

The frame has 44 children. The best three, with their probabilities among all children, are:

| Child | Probability |
|---|---|
| $z_1 \to A$, $z_2$ false, $z_3 \to B$ | 0.416 |
| $z_1 \to A$, $z_2 \to B$, $z_3$ false | 0.336 |
| $z_1$ false, $z_2 \to A$, $z_3 \to B$ | 0.103 |

The first two are close. GNN would commit to the first. MHT keeps both, and the next frame, where the true track of B lands near one of $z_2$ and $z_3$, decides.

**A short sequence.** In the code, two targets with velocities $(1, \pm 0.25)$ cross at frame 10, each is detected with probability 0.85 and noise 0.5, and about one clutter point per frame falls near them. With $M = 5$ hypotheses over 20 frames, both tracks keep their identities, with a largest error of 0.99 and a mean error of 0.43. In this scene $M = 1$ does about as well. The benefit of more hypotheses shows when detections are missed for several frames during a close approach, when the best single choice is often wrong.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows these facts.

- **Theorem: costs and Reid's formula.** The assignments of finite cost of $C$ correspond one to one with the children of $h$, and the log weight of line L4 is the log of Reid's formula up to a constant that is the same for all children of all hypotheses in the frame.
- **Theorem: Murty's method.** It returns the assignments in order of nondecreasing cost, with no repeats and no gaps.
- **Theorem: global pruning.** Keeping the $M$ best children of each hypothesis and then the $M$ best overall gives exactly the $M$ best children of all hypotheses.
- **Theorem: hardness of the batch problem.** Finding the best partition of the measurements of 3 frames into tracks is NP-hard, by a reduction from [three-dimensional matching](/three-dimensional-matching/). So MHT prunes, and the hypothesis it returns is the best among those it kept, not always the best overall.

## Complexity

Per frame, each of the $M$ hypotheses builds a matrix with $m$ rows and $n + 2m$ columns. Murty's method for $M$ solutions solves up to $M m$ subproblems, each by the Hungarian algorithm in $O(m^2 (n + m))$ time. So a frame costs $O(M^2 m^3 (n + m))$ for the assignments and $O(M n d^3)$ for the Kalman filters. Sorting the $M^2$ children adds $O(M^2 \log M)$. The space is $O(M (n d^2 + m (n + m)))$. Practical systems cut this down: they split the measurements and tracks into clusters by the gates, run Murty's method on each cluster, and use the optimized versions of Murty's method of Miller, Stone and Cox (1997). Without pruning, the number of hypotheses grows exponentially with the number of frames.

## Properties

- **Deferred decisions.** A choice made in frame $t$ can be reversed in a later frame, as long as the other hypothesis is still kept.
- **Track initiation built in.** New targets and false alarms are part of each hypothesis, so MHT starts and confirms tracks with the same scoring.
- **Approximate.** Pruning to $M$ hypotheses can drop the right one.
- **A model of the data.** The quality depends on $p_D$, $\beta_{FT}$ and $\beta_{NT}$, which must be set or estimated.
- **Many hypotheses share tracks.** Implementations store tracks once and point to them, which the simple code here does not do.

## Variants and improvements

- **Track-oriented MHT.** Keep a tree of possible tracks instead of a list of hypotheses, score each track by a log-likelihood ratio, and find the best global hypothesis as a set of compatible tracks by integer programming. Kurien (1990) and Blackman (2004) describe this form, and most current systems use it.
- **N-scan pruning.** Fix every decision older than $N$ frames to the choice of the best hypothesis, which bounds the depth of the tree.
- **Multi-frame assignment.** Poore and others write the last few frames as a multidimensional assignment problem and solve it with [Lagrangian relaxation](/lagrangian-relaxation/).
- **MHT revisited.** Kim, Li, Ciptadi and Rehg (2015) added online appearance models to track-oriented MHT and obtained strong results on video benchmarks.
- **Batch alternatives.** [Network flow tracking](/network-flow-tracking/) solves a simpler model of the whole video exactly in polynomial time.
- **Soft alternatives.** [JPDA](/joint-probabilistic-data-association/) averages over the hypotheses of one frame instead of keeping them.

## When to use it

Use MHT when the targets come close to each other, detections are missed, and wrong identity decisions are costly, as in air surveillance or in tracking people through crowds. It is heavier than GNN and JPDA and has more parameters, so it pays off when those simpler methods swap or lose tracks. For offline video where all frames are known, [network flow tracking](/network-flow-tracking/) is a simpler choice with an exact solution of its own model.

## Pitfalls

- **Too few hypotheses.** With a small $M$, the right hypothesis can be dropped in the frame where it is second, and it never comes back.
- **Pruning only per parent.** Keeping $M$ children per parent without the global cut makes the number of hypotheses grow as $M^t$.
- **Weights that underflow.** Probabilities of long histories become tiny. Work with log weights and normalize each frame.
- **Duplicate tracks.** Different hypotheses can contain the same track. Without sharing, memory grows quickly.
- **Wrong clutter and birth densities.** If $\beta_{NT}$ is too large, every clutter point starts a track. If it is too small, true new targets are called false alarms for too long.
- **Reporting a jumping answer.** The best hypothesis can change from frame to frame, so the reported tracks can jump. Report decisions with a delay of a few frames if that matters.

## Implementations

## History

Donald Reid published the algorithm in 1979. He gave the recursive formula for the probability of a hypothesis, track initiation inside the same framework, and the clustering of tracks that share measurements. The exponential growth of hypotheses limited the method for years. Cox and Hingorani (1996) noted that the best children of a hypothesis are the best solutions of an assignment problem and generated them with Murty's 1968 algorithm for ranking assignments, which made Reid's method fast enough for vision. The track-oriented form, described by Kurien in 1990, became the standard in radar systems, and Blackman's 2004 survey called MHT the generally preferred method for data association in modern tracking systems. In 2015, Kim, Li, Ciptadi and Rehg revisited MHT for video and showed it was competitive with newer methods on multiple object tracking benchmarks.

## References
