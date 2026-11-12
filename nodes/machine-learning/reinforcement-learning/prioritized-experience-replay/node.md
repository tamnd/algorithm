---
tag: T8RE4E
kind: technique
slug: prioritized-experience-replay
name: Prioritized experience replay
aliases:
- PER
- prioritized replay
area: machine-learning/reinforcement-learning
level: advanced
summary: "Sample replayed transition i with probability p_i^alpha / sum p^alpha, p_i = |TD error| + eps, correct the bias with weights (N P(i))^(-beta), and use a sum tree for O(log N) draws."
prereqs: [experience-replay, td-error, segment-tree]
see_also: [dqn, double-dqn, prioritized-sweeping, fenwick-tree, importance-sampling-off-policy, segment-tree]
sources:
  - paper: "Tom Schaul, John Quan, Ioannis Antonoglou and David Silver, Prioritized experience replay, International Conference on Learning Representations (ICLR), 2016, arXiv:1511.05952"
    locator: Section 3.3 and Equation 1 (stochastic prioritization, proportional and rank-based), Section 3.4 (importance-sampling weights and the annealing of beta), Algorithm 1, Appendix B.2.1 (the sum tree)
  - paper: doi:10.1007/BF00992699
    title: "Long-Ji Lin, Self-improving reactive agents based on reinforcement learning, planning and teaching, Machine Learning 8(3-4), 1992, pages 293 to 321"
    locator: the section on experience replay (uniform replay, the baseline that prioritization changes)
  - paper: doi:10.1007/BF00993104
    title: "Andrew W. Moore and Christopher G. Atkeson, Prioritized sweeping, reinforcement learning with less data and less time, Machine Learning 13(1), 1993, pages 103 to 130"
    locator: the priority queue ordered by the size of the expected value change (the model-based ancestor of the idea)
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 8.4 (prioritized sweeping)
---

Prioritized experience replay (Schaul, Quan, Antonoglou and Silver, 2016) changes the uniform draw of [experience replay](/experience-replay/): transition $i$ is drawn with probability $P(i) = p_i^\alpha / \sum_k p_k^\alpha$, where the priority $p_i$ grows with the size of its last [TD error](/td-error/) $\delta_i$. Transitions that the learner still predicts badly are replayed more often. The change of distribution biases the expected update, so each sampled update is multiplied by an importance weight $w_i = (N \cdot P(i))^{-\beta}$. A sum tree, a binary tree of partial sums like a [segment tree](/segment-tree/), gives both the draw and the priority update in $O(\log N)$ time.

## In plain words

Plain replay picks old experiences at random, each as likely as the next. Most of them teach the learner almost nothing, because it already predicts them well. A few are still surprising. Prioritized replay gives each stored experience a score: how wrong the learner was the last time it looked at it. Experiences with a high score are picked more often. A small extra amount keeps every score above zero, so nothing is left out forever.

Picking surprising experiences more often also distorts what the learner sees. So each picked experience counts a little less in the update when it was picked for its high score, which undoes the distortion.

To pick by score fast in a memory of a million items, the scores sit at the leaves of a tree in which each node stores the sum of the scores below it.

## When it applies

The setting is that of [experience replay](/experience-replay/): an unknown MDP with samples, the discounted criterion, and an off-policy learner, usually [DQN](/dqn/) or [Double DQN](/double-dqn/), that trains on minibatches from a buffer of $N$ transitions. Prioritization helps when:

- the reward is sparse or rare, so that a few transitions carry most of the information (the "blind cliffwalk" task of the paper is the extreme case: one transition out of an exponential number gives reward);
- the TD error of a transition is a usable signal of how much the learner can still gain from it;
- the update is a gradient step, so that an importance weight can scale it.

The cost is a sum tree of $2m$ numbers, where $m \ge N$ is a power of two, and $O(\log N)$ time per draw and per priority update, against $O(1)$ for uniform replay.

## The template

The holes are UPDATE (the learner, which returns the new TD errors of the sampled transitions) and the schedule of $\beta$. $D$ is the circular buffer, $T$ the sum tree over its slots, and $\epsilon > 0$ a small constant.

```pseudo id=main
PRIORITIZED-REPLAY(N, B, α, β, ε, UPDATE)
L1  T ← a sum tree over N leaves, all 0; p_max ← 1
L2  on each new transition: write it to slot next of D, T.UPDATE(next, p_max^α)
L3  to draw a minibatch: seg ← T.total / B
L4      for j ← 0 to B − 1: u ← (j + U(0, 1)) · seg, i_j ← T.FIND(u)
L5          P(i_j) ← T.leaf(i_j) / T.total, w_j ← (|D| · P(i_j))^(−β)
L6      w_j ← w_j / max_k w_k for each j
L7  after UPDATE returns the TD errors δ_j: p ← |δ_j| + ε, T.UPDATE(i_j, p^α), p_max ← max(p_max, p)
```

A new transition gets the largest priority seen so far (line L2), so it is replayed at least once soon. Line L4 is stratified: the range $[0, \text{total})$ is cut into $B$ equal segments and one point is drawn in each, which spreads a minibatch over high and low priorities. Line L5 is the importance weight, and line L6 scales the weights so that the largest is 1; the weights then only shrink steps. UPDATE multiplies the loss gradient of transition $i_j$ by $w_j$, that is, it uses $w_j \delta_j$ in place of $\delta_j$.

**The two kinds of priority.** The *proportional* variant uses $p_i = |\delta_i| + \epsilon$. The *rank-based* variant sorts the transitions by $|\delta_i|$ and uses $p_i = 1/\mathrm{rank}(i)$, which ignores the scale of the errors and is less sensitive to outliers; the paper samples it from $B$ precomputed segments of equal probability mass. $\alpha = 0$ is uniform replay, and $\alpha = 1$ is sampling in proportion to the priority itself.

**Why the weights correct the bias.** Uniform replay estimates $\frac{1}{N} \sum_i g_i$, where $g_i$ is the update from transition $i$. A draw from $P$ with weight $w_i = (N P(i))^{-1}$ (that is, $\beta = 1$ before normalization) has expected value $\sum_i P(i) \cdot \frac{1}{N P(i)} g_i = \frac{1}{N}\sum_i g_i$, the same. For $\beta < 1$ the correction is partial. The paper anneals $\beta$ linearly from $\beta_0$ to 1 over training, since an unbiased update matters most near convergence. The division by $\max_k w_k$ in line L6 multiplies all weights of a minibatch by one number, so it changes the step size but not the direction within the minibatch.

### The sum tree

Let $m$ be the smallest power of two with $m \ge N$. The array $\text{tree}[1 \ldots 2m-1]$ holds the leaf values $v_i = p_i^\alpha$ at $\text{tree}[m + i]$, and each internal node holds $\text{tree}[j] = \text{tree}[2j] + \text{tree}[2j+1]$. So $\text{tree}[1]$ is the total.

```pseudo id=find
FIND(u)                                   ▷ 0 ≤ u < tree[1]
F1  j ← 1
F2  while j < m do
F3      if u < tree[2j] then j ← 2j
F4      else u ← u − tree[2j], j ← 2j + 1
F5  return j − m

UPDATE(i, v)
U1  j ← m + i, tree[j] ← v
U2  while j > 1 do j ← ⌊j/2⌋, tree[j] ← tree[2j] + tree[2j + 1]
```

FIND returns the leaf $i$ with $v_0 + \cdots + v_{i-1} \le u < v_0 + \cdots + v_i$. The invariant of the loop is: $u$ minus the sum of the leaves left of the subtree of $j$ lies in $[0, \text{tree}[j])$. It holds at the root. If $u < \text{tree}[2j]$ the point is in the left child; otherwise it is in the right child, after the left child's total is removed. At a leaf, the invariant is exactly the claim. If $u$ is uniform on $[0, \text{total})$, leaf $i$ is returned with probability $v_i / \text{total} = P(i)$. Both procedures walk one root-to-leaf path, so they cost $\lg m = O(\log N)$ steps. A [Fenwick tree](/fenwick-tree/) can do the same job; the sum tree is the usual choice because its downward search is simple.

**Example.** Leaf values $v = (3, 1, 4, 1, 5)$, so $m = 8$ and three leaves are 0. The internal nodes are $\text{tree}[1 \ldots 7] = (14, 9, 5, 4, 5, 5, 0)$. FIND(8): at the root, $8 < 9$, go left to node 2; $8 \ge \text{tree}[4] = 4$, so $u \leftarrow 4$ and go to node 5; $4 \ge \text{tree}[10] = 4$, so $u \leftarrow 0$ and go to node 11, leaf 3. Indeed $3 + 1 + 4 = 8 \le 8 < 9$. Over a grid of $M$ equally spaced points $u_j = (j + \tfrac12)\,\text{total}/M$, each leaf $i$ is hit exactly $M v_i/\text{total}$ times when these are integers; with $v = (\tfrac12, 0, \tfrac32, 1, 1, 2)$ and $M = 600$ the counts are $(50, 0, 150, 100, 100, 200)$.

**Example (weights).** With $\alpha = 0.6$, $\epsilon = 0.01$ and TD errors $(2, -0.5, 0, 1)$, the priorities are $(2.01, 0.51, 0.01, 1.01)$ and $P \approx (0.467, 0.205, 0.0194, 0.309)$. With $\beta = 1$, the raw weights $(4P(i))^{-1}$ are about $(0.536, 1.22, 12.9, 0.809)$: the transition with error 0 is rare, so it gets the largest weight when it is drawn.

## Classic examples

- **[Double DQN](/double-dqn/) with prioritized replay.** Algorithm 1 of Schaul et al. is Double DQN with proportional prioritization; on the Atari games of the DQN benchmark both variants improved the median normalized score over uniform replay.
- **Rainbow and Ape-X.** Later agents combine prioritized replay with the other DQN extensions, and Ape-X computes the initial priorities in the actors, so that new transitions do not all get $p_{\max}$.
- **[Prioritized sweeping](/prioritized-sweeping/).** Moore and Atkeson (1993) ordered planning backups in a learned model by the size of the expected change, with a priority queue. Prioritized replay applies the same idea to stored real transitions.
- **[Dyna-Q](/dyna-q/).** Its planning step can draw the simulated transitions by priority in the same way.

## Variations

- **Rank-based sampling** with $p_i = 1/\mathrm{rank}(i)$, as above. Exact ranks would need a sorted structure; the paper keeps an approximately sorted heap.
- **Initial priorities.** $p_{\max}$ for new transitions (the paper), or the TD error computed when the transition is stored.
- **Weight normalization.** Normalize by the largest weight in the minibatch, or by the largest possible weight $(N \min_i P(i))^{-\beta}$ over the whole buffer, which needs a min tree next to the sum tree. The second keeps the step size independent of the minibatch.
- **Priorities from other signals.** Sequence priorities for recurrent agents mix the largest and the mean TD error of a sequence; other work uses the loss of a model or the novelty of a state.

## Pitfalls

- **Forgetting the weights.** Without the weights of line L5 the learner minimizes a loss weighted by $P$, and its fixed point moves. With function approximation this can shift the learned values; the weights must multiply the gradient, not the priority.
- **Priorities of zero.** With $p_i = |\delta_i|$ and $\epsilon = 0$, a transition with error 0 is never drawn again, even after the network has changed. Keep $\epsilon > 0$.
- **Stale priorities.** A priority is updated only when its transition is drawn, so most priorities describe an older network. This is accepted for speed; it is one reason the sampling is stochastic, not greedy.
- **Floating point drift in the tree.** After millions of updates in float32, the internal sums no longer equal the sums of the leaves, and FIND can step into a leaf of value 0 or past the last leaf. Recompute the internal nodes from time to time, and clamp $u$ below the total.
- **Overfitting to a few transitions.** With large $\alpha$ and small $\beta$, a handful of high-error transitions dominate the minibatches, for example transitions with noisy rewards whose error never shrinks. The rank-based variant and a smaller $\alpha$ reduce this.

## Exercises

1. Show that with $\alpha = 0$ the sampling is uniform and every weight is 1 after normalization, whatever $\beta$ is.
2. Show that if $u$ is uniform on $[0, \text{total})$, the stratified draw of line L4 still returns each leaf $i$ with marginal probability $P(i)$ when the minibatch index $j$ is itself chosen uniformly at random.
3. Give the extra array and the extra lines in UPDATE needed to return $\min_i v_i$ in $O(1)$ time, and use it to normalize the weights over the whole buffer.

## References
