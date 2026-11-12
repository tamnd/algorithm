---
tag: 2KJ4A7
kind: algorithm
slug: bvh-traversal
name: BVH traversal
aliases: [bounding volume hierarchy traversal]
area: graphics-and-signals/ray-tracing
level: intro
summary: Walk a bounding volume hierarchy with a stack to find the closest hit of a ray, visiting the nearer child first and skipping every box that starts beyond the best hit so far.
solves: [closest-hit-query, any-hit-query]
model: real-ram
complexity:
  vars: {n: the number of primitives, h: the height of the tree}
  time: {worst: O(n)}
  space: {extra: O(h)}
properties: {deterministic: true, recursive: false}
history:
  year: 1986
  people: [Timothy L. Kay, James T. Kajiya]
  note: Kay and Kajiya visited the hierarchy in the order of the distance at which the ray enters each volume, with a heap, and stopped when the next volume started beyond the best hit.
prereqs: [bounding-volume-hierarchy, slab-method]
see_also: [bvh-construction, kd-tree-traversal, bounding-interval-hierarchy, ray-packet-tracing, closest-hit-query, any-hit-query, depth-first-search, amanatides-woo-traversal]
sources:
  - paper: doi:10.1145/15886.15916
    title: Timothy L. Kay and James T. Kajiya, Ray tracing complex scenes, SIGGRAPH 1986, Computer Graphics 20(4), 269 to 278
    locator: the traversal of the hierarchy with a heap ordered by the entry distance, and the stop when the next entry is beyond the nearest hit
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 4, Section 4.3 Bounding Volume Hierarchies, the subsection on traversal (the stack of nodes and the choice of the near child from the sign of the direction on the split axis)
  - url: http://jcgt.org/published/0002/02/02/
    title: Thiago Ize, Robust BVH ray traversal, Journal of Computer Graphics Techniques 2(2), 2013, 12 to 27
    locator: the conditions under which a floating-point traversal misses a box that the ray meets, and the fix
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 6, Bounding Volume Hierarchies, the sections on tree traversal and the descent rules
---

BVH traversal answers a ray query on a [bounding volume hierarchy](/bounding-volume-hierarchy/). For the [closest-hit query](/closest-hit-query/) it keeps a stack of nodes, tests the boxes of the two children of each inner node with the [slab method](/slab-method/), visits the nearer child first, and skips any node whose box begins beyond the best hit found so far. For the [any-hit query](/any-hit-query/) of a shadow ray it returns at the first hit in the given range. The answer is exact, and the cost is $O(n)$ per ray in the worst case, while good trees on typical scenes need far fewer steps.

## In plain words

You look for the first thing a ray hits, and the scene is a set of nested boxes. Start at the outer box. At each box, look at its two inner boxes. If the ray misses one, forget it and everything inside. If the ray goes into both, open the nearer one first and put the other one on a pile to look at later.

When you reach a box with real objects in it, test them. If the ray hits one, remember how far away it is. From then on, any box on the pile that the ray only reaches after that distance can hold nothing closer, so you throw it away without opening it.

The boxes can overlap, so the first object you find is not always the closest. You stop only when the pile is empty.

## The problem

The input is a BVH whose boxes contain the primitives below them, and a ray $r(t) = o + t\,d$ with $d \ne 0$. The closest-hit query asks for a primitive $p$ and the least $t \ge 0$ with $r(t) \in p$, minimized over all primitives, or "none". The any-hit query asks whether some primitive has a hit with $0 \le t \le t_{max}$; it needs no particular hit. Both are defined on their problem pages. Here the primitives are triangles and the triangle test is [Möller-Trumbore](/moller-trumbore/), but the traversal works with any primitive test.

## The algorithm

The stack holds pairs $(v, t_v)$, where $t_v$ is the parameter at which the ray enters the box of $v$, computed when $v$ was pushed.

```pseudo id=main
CLOSEST-HIT(T, o, d)
L1  best ← none; tmax ← +∞
L2  t_root ← SLAB(box(root), o, d, [0, tmax]); if t_root = MISS then return none
L3  stack ← [(root, t_root)]
L4  while stack is not empty do
L5      (v, tv) ← pop the stack
L6      if tv > tmax then continue                       ▷ the box starts beyond the best hit
L7      if v is a leaf then for each primitive p of v do
L8          t ← INTERSECT(p, o, d); if t ≠ none and t ≤ tmax and t beats best then best ← (t, p); tmax ← t
L9      else (a, b) ← the children of v
L10         ta ← SLAB(box(a), o, d, [0, tmax]); tb ← SLAB(box(b), o, d, [0, tmax])
L11         if both hit then push the farther of (a, ta), (b, tb), then the nearer
L12         else push the one that hits, if any
L13 return best
```

Lines L10 to L12 test the child boxes at the parent, so a missed child is never pushed. Line L11 pushes the nearer child last, so it is popped next: the walk goes depth first toward the ray origin. Line L6 is the second test of a node: when the node was pushed its box started before $t_{max}$, but $t_{max}$ may have dropped since then.

ANY-HIT$(T, o, d, t_{max})$ is the same loop with a fixed $t_{max}$, with no ordering in line L11, and with a return of true at the first primitive hit in line L8. A shadow ray from a surface to a light uses $t_{max} = 1 - \epsilon$ for a direction that ends at the light.

## Example

Four triangles stand as walls across the x axis at $x = 1, 3, 5, 7$; the wall at $x = c$ has the corners $(c, 0, 0)$, $(c, 4, 0)$ and $(c, 0, 4)$. A median build gives the root 0 with box $x \in [1, 7]$, node 1 over the walls at 1 and 3, node 4 over the walls at 5 and 7, and the leaves 2, 3, 5, 6 for the walls at 1, 3, 5, 7. The ray starts at $o = (10, 1, 1)$ with $d = (-1, 0, 0)$, so it reaches the wall at $x = c$ at $t = 10 - c$.

| step | pop $(v, t_v)$ | L6 | action | tmax | stack after (top last) |
|---|---|---|---|---|---|
| 0 | | | root box: $t_{root} = 3$ | $+\infty$ | (0, 3) |
| 1 | (0, 3) | pass | children 1 at $t = 7$, 4 at $t = 3$; push 1, then 4 | $+\infty$ | (1, 7), (4, 3) |
| 2 | (4, 3) | pass | children 5 at $t = 5$, 6 at $t = 3$; push 5, then 6 | $+\infty$ | (1, 7), (5, 5), (6, 3) |
| 3 | (6, 3) | pass | leaf: wall at 7 hit at $t = 3$ | 3 | (1, 7), (5, 5) |
| 4 | (5, 5) | $5 > 3$, skip | | 3 | (1, 7) |
| 5 | (1, 7) | $7 > 3$, skip | | 3 | empty |

The answer is the wall at $x = 7$ at $t = 3$, after 5 box tests and 1 triangle test. A traversal that always goes left first finds the walls at 1, 3, 5 and 7 in that order, each nearer than the one before, and tests all four triangles. With the same ray, ANY-HIT with $t_{max} = 2$ rejects the root box and tests no triangle, and with $t_{max} = 3$ it returns true.

## Correctness

Claim: if each box of the tree contains the primitives below it, CLOSEST-HIT returns a hit with the least $t$, or none if the ray hits nothing, and ANY-HIT returns true exactly when a hit with $t \le t_{max}$ exists.

The key invariant: let $q$ be a primitive with the least hit parameter $\tau^*$. As long as best does not have the parameter $\tau^*$, some node on the path from the root to the leaf of $q$ is on the stack, or is the node being processed. A node $v$ on this path has $q$ inside its box, so the ray enters the box at some $t_v \le \tau^* \le t_{max}$. Then neither line L6 nor lines L10 to L12 drop it, and the next node on the path is pushed. The pruning only drops boxes that the ray enters after $t_{max}$, and by containment those hold no hit before $t_{max}$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The model is the [real RAM](/real-ram/); a box test and a primitive test cost $O(1)$. Each node is pushed at most once, by its parent, so a query pops at most $2n - 1$ nodes for a tree with $n$ leaves, makes at most $2n - 1$ box tests and tests each primitive at most once. That is $O(n)$ time in the worst case, and the bound is reached. Take $n$ triangles with the corners $(0, 0, z)$, $(10, 0, z)$ and $(10, 10, z)$ for $z = 0, \ldots, n - 1$. The ray through $(1, 9)$ along the z axis is inside every box but misses every triangle, since $9 > 1$ puts it on the wrong side of the diagonal. It pops all $2n - 1$ nodes and tests all $n$ triangles.

On scenes with a good build, for example with the [surface area heuristic](/surface-area-heuristic/), the number of visits per ray grows slowly with $n$, close to $\log n$. This is an observed behavior. No logarithmic bound holds in the worst case, and the SAH only gives an expected cost under its model of uniform random rays.

The extra space is the stack. Each pop of an inner node removes one entry and adds at most two, and the entries on the stack are siblings of nodes on the current root path, plus the next node. So at most $h + 1$ entries are on the stack, $O(h)$, where $h$ is the height. A fixed stack of 64 entries is common in GPU code because builds keep $h$ below that.

## Properties

- **Exact.** With exact box and primitive tests, the answer is exact. With floats, use the conservative slab test so that no box is lost.
- **Not front to back.** Leaves are reached in a near-first order, but sibling boxes overlap, so a later leaf can hold a closer hit. The loop must run until the stack is empty or line L6 rejects all that is left.
- **Output sensitive in practice.** A hit found early shrinks $t_{max}$ and prunes most of the rest. Rays that miss everything cost the most when they pass close to many boxes.
- **Any-hit is cheaper.** It needs no order and stops at the first hit, which suits shadow rays and occlusion tests.

## Variants and improvements

- **Order by the split axis.** PBRT stores the split axis in each inner node and visits first the child on the side of the ray origin, from the sign of $d$ on that axis. This needs no child box test before the push, but the order is coarser than by entry distance.
- **Order with a heap.** Kay and Kajiya kept all candidate nodes in a heap ordered by entry distance and took the nearest each time; the traversal stops when the least entry is beyond the best hit. A stack with near-first pushing is cheaper and is the common form.
- **Wide BVHs.** With 4 or 8 children per node, one SIMD slab test handles all the child boxes, and the hit children are sorted by distance before the push.
- **Packets and streams.** [Ray packet tracing](/ray-packet-tracing/) walks one tree for a group of coherent rays and tests a box against all of them at once.
- **Stackless traversal.** GPU versions avoid a per-ray stack with parent links, skip links or a restart trail, and pay with more box tests.
- **Robust traversal.** Ize (2013) shows when floating-point slab tests miss a box that the ray meets and pads the far value of the test. PBRT uses the factor $1 + 2\gamma_3$.
- **Two-level traversal.** For [object instancing](/object-instancing/), a leaf of the top tree holds an instance: the ray is moved into the frame of the instance and the traversal goes on in the bottom tree.

## When to use it

Use this traversal for every ray query on a BVH: camera rays, the rays of [path tracing](/path-tracing/), and shadow rays with the any-hit form. A [kd-tree traversal](/kd-tree-traversal/) can stop at the first hit inside the current leaf because kd-tree leaves do not overlap; the price is a structure with duplicated references and an unknown size. A grid walked with [Amanatides-Woo traversal](/amanatides-woo-traversal/) is cheaper per step on scenes of even density. For many coherent primary rays, a raster pipeline can replace the traversal.

## Pitfalls

- **Returning at the first hit in a closest-hit query.** Line L8 must update best and continue. A return there is only right for ANY-HIT, and it gives wrong answers when sibling boxes overlap.
- **No second test of $t_v$.** Without line L6, a node pushed when $t_{max}$ was larger is still opened. The answer stays right, but the pruning that makes the traversal fast is lost.
- **Comparing with the wrong bound.** Line L10 must test the child boxes on $[0, t_{max}]$ with the current $t_{max}$; a test on $[0, +\infty)$ keeps far boxes on the stack. For ANY-HIT, $t_{max}$ is the distance to the light, and using $+\infty$ makes surfaces behind the light cast shadows.
- **Self-intersection.** A secondary ray from a surface point can hit its own surface at $t \approx 0$ because of rounding. Offset the origin along the normal or start at a small $t_{min} > 0$, in line L2 and in line L8.
- **Stack overflow.** A fixed stack must hold $h + 1$ entries. A degenerate build can make $h$ close to $n$; check the height after the build, or fall back to a larger stack.
- **Ties.** Two primitives can have the same $t$, for example at a shared edge. Line L8 keeps the first one found with a strict comparison, so the primitive returned can depend on the tree, while the distance does not.

## Implementations

## History

Kay and Kajiya (1986) gave the ordered traversal of a hierarchy of bounding volumes: a heap of nodes keyed by the entry distance of the ray, and a stop as soon as the next entry is beyond the nearest hit. Later systems replaced the heap by a stack with near-first pushing, as in PBRT, and made the box test faster and robust (Williams et al. 2005, Ize 2013). Wide nodes, ray packets and stackless schemes adapted the same walk to SIMD units and GPUs.

## References
