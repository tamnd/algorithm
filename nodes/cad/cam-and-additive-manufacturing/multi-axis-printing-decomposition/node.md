---
tag: N5ERYT
kind: algorithm
slug: multi-axis-printing-decomposition
name: Support-free decomposition for multi-axis printing
aliases:
- multi-axis 3D printing planning
area: cad/cam-and-additive-manufacturing
level: research
summary: Splits a model by planar cuts into parts that each print without support in their own build direction, and orders them so a printer that can turn the part needs no supports.
model: real-ram
complexity:
  vars: {n: number of voxels, h: largest number of layers in one direction, w: beam width, m: largest number of cuts}
  time: {beam: O(m w h n log n), exhaustive: O((5 h)^m n)}
  space: {extra: O(w h n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2017
  people: [Chenming Wu, Chengkai Dai, Guoxin Fang, Yong-Jin Liu, Charlie C. L. Wang]
  note: Wu, Dai, Fang, Liu and Wang built RoboFDM in 2017, a robot arm that turns the part so that a model split by planes prints without supports, and extended the planar decomposition to models with loops with a beam-guided search.
prereqs: [support-structure-generation, beam-search]
see_also: [build-orientation, curved-layer-printing, accessibility-cone, breadth-first-search, greedy-algorithm, collision-detection, staircase-effect, hash-table]
sources:
  - paper: doi:10.1109/ICRA.2017.7989140
    title: Chenming Wu, Chengkai Dai, Guoxin Fang, Yong-Jin Liu and Charlie C. L. Wang, RoboFDM, a robotic system for support-free fabrication using FDM, IEEE International Conference on Robotics and Automation (ICRA), 2017, 1175 to 1180
    locator: the decomposition of a model by planes into parts that are support-free in their own directions, printed one after the other in a collision-free order by a robot arm that holds the part
  - paper: arxiv:1812.00606
    title: Chenming Wu, Chengkai Dai, Guoxin Fang, Yong-Jin Liu and Charlie C. L. Wang, General support-effective decomposition for multi-directional 3D printing, IEEE Transactions on Automation Science and Engineering (preprint 2018)
    locator: the sequence of clipping planes found by a beam-guided search with manufacturing constraints, for models with loops and handles
  - paper: doi:10.1145/3197517.3201342
    title: Chengkai Dai, Charlie C. L. Wang, Chenming Wu, Sylvain Lefebvre, Guoxin Fang and Yong-Jin Liu, Support-free volume printing by multi-axis motion, ACM Transactions on Graphics 37(4), 2018, Article 134
    locator: the decomposition of a volume into curved layers that are support-free and collision-free, and the tool paths on each layer for a multi-axis printer
---

A printer that can turn the part, such as a robot arm or a five-axis table, can build different regions of a model in different directions. A region that overhangs in the vertical direction may grow sideways from a wall that is already printed, with no support at all. Support-free decomposition splits the model into parts and gives each part a build direction and a place in the print order, so that every part is free of overhangs in its own direction, given the parts that are already there. This page uses the planar version of Wu, Dai, Fang, Liu and Wang (RoboFDM, 2017, and the general form with a beam-guided search): peel parts off the model with planes, and print them in the reverse order. On a voxel model the overhang test is exact, so a plan that the search returns is proved to print with no support and, under a simple model of the print head, with no collision. The search for the fewest parts is a combinatorial search with no known efficient exact method, so the beam search is a heuristic, and its quality on this page is measured against exhaustive search on small models.

## In plain words

A normal printer always builds upward. A shelf that sticks out from a wall has nothing under it, so the printer needs props there. If the part can be turned on its side, the shelf can grow out of the wall, layer by layer, and each new layer rests on the one before it.

So the plan is: cut the model into a few pieces. Print the bottom piece the usual way. Then turn the part and print the next piece, which grows out of what is already there. The trick is to choose the cuts and the order so that no piece ever hangs in the air, and the nozzle never runs into the part.

## The problem

The model is a set $V$ of integer voxels $(x, y, z)$ with $z \ge 0$, and the platform lies under $z = 0$. The build directions are $D = \{+z, +x, -x, +y, -y\}$. The direction $-z$ is left out, because the part stands on the platform and the head cannot come from below it. In direction $d$ the layer of a voxel $v$ is $\langle v, d \rangle$.

**The overhang rule.** The support block $S(v, d)$ is the set of the 9 voxels one layer below $v$ in direction $d$: the voxel right under it and the 8 around that one. A voxel printed in direction $d$ can be deposited only if one voxel of $S(v, d)$ is already solid, or $d = +z$ and $v$ is on the platform. Each layer can stick out by one voxel per layer, which is the 45° rule of material extrusion on the voxel grid (see [support structure generation](/support-structure-generation/) for where the angle comes from).

**The head rule.** While layer $\ell$ in direction $d$ is printed, the head occupies the half-space $\langle p, d \rangle > \ell$, and no printed voxel may be there.

**Planar cuts.** From a region $R$, a cut in direction $d$ at level $c$ removes the part $P = \{v \in R : \langle v, d \rangle \ge c\}$. The cut is support-free if every voxel of $P$ has a voxel of $R$ in its support block. Let $U(R, d)$ be the voxels of $R$ with no voxel of $R$ in their support block. A plan is a sequence of support-free cuts $V = R_0 \supset R_1 \supset \dots \supset R_m$ whose last region, the base, has $U(R_m, +z) = \emptyset$. The task is to find a plan with few parts.

## The algorithm

The test for one cut is cheap. The cut $(d, c)$ is support-free exactly when $c$ is above every layer of $U(R, d)$, because the condition on a voxel of $P$ does not depend on $c$. So one pass over $R$ gives all the support-free cuts in a direction. The search over sequences is a [beam search](/beam-search/) that keeps the $w$ best regions after each round.

```pseudo id=main
DECOMPOSE(V, w, m)
L1  beam ← {(V, empty sequence)}
L2  for round = 0 to m do
L3      if some (R, s) in beam has U(R, +z) = ∅ then return PLAN(R, s)
L4      children ← empty map from regions to sequences
L5      for each (R, s) in beam and each direction d in D do
L6          ℓ ← max{⟨v, d⟩ : v ∈ U(R, d)}           ▷ −∞ if U is empty
L7          for each level c of R with c > ℓ and c > min level do
L8              P ← {v ∈ R : ⟨v, d⟩ ≥ c}; children[R \ P] ← s + (d, P)
L9      beam ← the w children with the fewest base overhangs |U(R \ P, +z)|, larger regions first
L10 return failure

PLAN(R, s)
L11 return (+z, R), then the parts of s in reverse order
```

Line L3 stops as soon as some region can be the base: it prints upward and has no overhang. Lines L6 to L8 list every support-free cut of $R$. Line L9 is the heuristic: it ranks the regions by the number of voxels that still hang in the vertical direction, and on a tie it keeps the region with more voxels, which leaves more material to support later cuts. Equal regions reached by different sequences are merged, because what can be cut next depends only on the region. Line L11 reverses the order: the last cut leaves the base, which is printed first, and the first part cut off is printed last.

For small models the same expansion can be run as a [breadth first search](/breadth-first-search/) over all regions, with no beam. It finds the least number of parts over all plans of planar cuts, and the tests use it as the reference.

## Example

A T-shaped model has a column of $2 \times 2$ voxels, 6 voxels tall ($x \in \{0, 1\}$, $y \in \{0, 1\}$, $0 \le z \le 5$), and two arms at the top ($z \in \{4, 5\}$), each 4 voxels long, from $x = -4$ to $-1$ and from $x = 2$ to $5$. It has 56 voxels.

In $+z$, the arm voxels at $z = 4$ with $x = -1$ and $x = 2$ are held by the column voxels at $z = 3$, diagonally, which is the 45° rule. The 12 voxels at $z = 4$ with $x \in \{-4, -3, -2, 3, 4, 5\}$ have nothing below them, so $U(V, +z)$ has 12 voxels and $V$ is not a base.

The cuts of $V$ in each direction, from lines L6 to L8:

| direction | highest layer in $U$ | valid levels $c$ | part sizes |
|---|---|---|---|
| $+z$ | 4 ($z = 4$) | 5 | 20 |
| $+x$ | 0 (column voxels at $x = 0$, $z \le 2$) | 1 to 5 | 28, 16, 12, 8, 4 |
| $-x$ | $-1$ (column voxels at $x = 1$, $z \le 2$) | 0 to 4 | 28, 16, 12, 8, 4 |
| $+y$, $-y$ | the first of the two layers | one level | 28 |

In $+x$ the voxels at $x = -4$ have nothing to their left, and the lower column voxels at $x = 0$ have nothing at $x = -1$, because the left arm is only at $z \ge 4$. So the cut must be at $c \ge 1$. Round 1 ranks the children by their remaining overhangs. The cut $(+x, 3)$ removes the right arm beyond $x = 2$ (12 voxels) and leaves 6 overhanging voxels, and so does $(-x, 2)$ on the left. The tie goes to the larger region and then to a fixed order. Round 2 cuts the other arm. Now the region is the column with one voxel of each arm, 32 voxels, with no overhang, and line L3 returns it.

| print order | direction | voxels | what it is |
|---|---|---|---|
| 1 | $+z$ | 32 | column, and the arm voxels at $x = -1$ and $x = 2$ |
| 2 | $-x$ | 12 | left arm, $-4 \le x \le -2$, grown leftward from $x = -1$ |
| 3 | $+x$ | 12 | right arm, $3 \le x \le 5$, grown rightward from $x = 2$ |

The breadth first search confirms that 3 parts is the least for this model: each arm needs its own direction, and the base must exist. A gallows with one arm needs 2 parts. A rod of two voxels that hangs under the end of an arm has no plan at all: the lower voxel touches only the voxel above it, so it has no support in any allowed direction.

**Measured quality.** On 400 random models in a $5 \times 2 \times 5$ box (each voxel present with probability 1/2, seed 7), 374 have a plan with at most 4 parts. Beam width 4 found a plan with the least number of parts on all 374. Width 1 (a greedy search) needed more parts or found no plan within 3 cuts on 3 of them. These are measurements on this test set, not a bound.

## Correctness

Three statements are proved. First, the cut $(d, c)$ is support-free exactly when $c$ is above the top layer of $U(R, d)$, so lines L6 to L8 list all the support-free cuts and no others. Second, the test is exact for the model: if a voxel $v$ of the part has no voxel of $R$ in its support block, no print order can deposit it, because only voxels of the model are ever solid. Third, every plan prints. Print the base by increasing $z$: each voxel off the platform has a voxel of the base one layer lower in its block. Then print each part $P_i$ by increasing layer, when exactly $R_{i+1} = R_i \setminus P_i$ is solid. A voxel of $P_i$ at layer $\ell$ has a voxel $w$ of $R_i$ at layer $\ell - 1$ in its block, and $w$ is either in $R_{i+1}$, which is printed, or in $P_i$ at a lower layer, which was printed just before. Every voxel of $R_{i+1}$ has layer less than $c_i \le \ell$, so no printed voxel is in the half-space of the head. By induction the whole model is printed, each voxel once.

The beam search is not complete: it can return failure when a plan exists. The breadth first search is complete up to its limit. The full proof is in [the correctness proof](proofs/correctness.md).

**What the tests check.** They print each plan voxel by voxel with an independent check of the support blocks and the head half-space, compare the beam result with the exhaustive minimum on random models, and check that a wrong order, a missing part or a single upward print is rejected.

## Complexity

With a [hash table](/hash-table/) of the voxels, $U(R, d)$ takes 9 lookups per voxel, $O(n)$ expected time. One region has at most $h - 1$ cuts per direction, and building one part and its rest takes $O(n)$. One round expands $w$ regions into at most $5 w h$ children in $O(w h n)$, and scoring them takes $O(n)$ each. The code sorts the children with the voxel list as a tie key, which adds a $\log n$ factor. So $m$ rounds take $O(m w h n \log n)$ time and $O(w h n)$ space for the children of one round.

The exhaustive search can visit $(5h)^m$ sequences in the worst case, so it is only for small models and few cuts. On the $5 \times 2 \times 5$ test models the whole set of 400 runs in about a second in Python.

## Properties

- **Sound.** Every returned plan prints without support and without head collision, under the stated model.
- **Exact test, heuristic search.** The support test for a cut is exact on voxels. The choice of cuts is a heuristic with no bound on the number of parts.
- **Only the region matters.** What can be cut next depends only on the remaining region, not on how it was reached.
- **Planar parts.** Each part is a half-space of the region, so the joints between parts are flat, and the head model holds automatically for planar cuts.
- **No guarantee of existence.** Some models have no plan, for example a voxel whose only neighbor is directly above it.

## Variants and improvements

- **Objectives.** RoboFDM and its successors weigh the number of parts, the area of the remaining overhang, and the printing time. When no plan without supports exists, the remaining overhang is left to a few supports.
- **Continuous planes.** The real method cuts a triangle mesh with planes of any normal, sampled on the sphere of directions, and tests the overhang of the faces. The voxel version of this page keeps the test exact.
- **Collision checks.** A nozzle is a cone, not a half-space. Then a part is printable only if the cone at each point avoids the printed material, which is a question of [accessibility cones](/accessibility-cone/) and [collision detection](/collision-detection/).
- **Curved layers.** Dai and coauthors (2018) replace planar parts by curved layers that grow over the volume, so the build direction changes from point to point. See [curved layer printing](/curved-layer-printing/).
- **One fixed direction.** When the printer cannot turn the part, the best single direction is the problem of [build orientation](/build-orientation/).

## When to use it

Use it for a robot arm or a five-axis printer when supports are costly: parts whose supports would be hard to remove, materials that do not have a soluble support, or surfaces that must stay clean. Models that branch, like trees, frames and brackets, often split into a few support-free parts. A closed box with a cavity does not split well: the roof of the cavity cannot grow upward, and in each sideways direction the far wall would have to grow across the cavity. The beam search with 4 cuts finds no plan for hollow cubes with sides 5, 7 and 8. On an ordinary three-axis printer the method does not apply.

## Pitfalls

- **Forgetting the printed parts.** A part is support-free only relative to the material printed before it. Testing each part alone, with nothing below it, rejects good plans.
- **Wrong order.** The parts must be printed in the reverse of the cut order. In the order of the cuts, the first part has nothing to rest on.
- **Allowing $-z$.** A part printed downward needs the head under the platform. Leave the direction out, or model the platform.
- **Ignoring the nozzle.** The half-space head is a model. A real head with a carriage can hit the part even when the planar cut is clean, and a robot can hit itself.
- **Too narrow a beam.** A greedy search (width 1) misses plans that a wider beam finds, as the measurements above show.
- **Weak joints.** Parts that grow in different directions meet at a flat joint, and the strength across it is lower than inside a part.

## Implementations

## History

Multi-directional printing grew with robot arm printers in the 2010s. Wu, Dai, Fang, Liu and Wang presented RoboFDM at ICRA 2017: a robot arm holds the platform, the model is split by planes into parts that are support-free in their own directions, and the parts are printed in a collision-free order. Their later paper on a general support-effective decomposition (preprint 2018) represents the decomposition by a sequence of clipping planes and finds it by a beam-guided search, which also works for models with loops and handles. Dai, Wang, Wu, Lefebvre, Fang and Liu (SIGGRAPH 2018) went from planar parts to curved layers that cover the whole volume.

## References
