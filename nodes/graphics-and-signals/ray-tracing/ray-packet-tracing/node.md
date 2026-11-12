---
tag: Y70MRZ
kind: algorithm
slug: ray-packet-tracing
name: Ray packet tracing
aliases:
- packet tracing
area: graphics-and-signals/ray-tracing
level: advanced
summary: Trace a group of nearby rays through an acceleration structure together, so that each node is fetched once for the group and tested for all its rays in SIMD lanes.
solves: [closest-hit-query]
model: real-ram
complexity:
  vars: {m: "the number of rays in the packet", n: "the number of primitives", v: "the number of nodes that the packet visits", h: "the height of the tree"}
  time: {worst: O(m n), best: Θ(m)}
  space: {extra: O(m h)}
properties: {deterministic: true, exact: true, parallel: true}
history:
  year: 2001
  people: [Ingo Wald, Philipp Slusallek, Carsten Benthin, Markus Wagner]
  note: Wald, Slusallek, Benthin and Wagner traced packets of four rays through a kd-tree with SSE instructions, with a data layout made for the cache, and measured interactive frame rates on commodity PCs.
prereqs: [bvh-traversal, ray-coherence]
see_also: [simt-model, warp-divergence, memory-coalescing, kd-tree-traversal, bounding-volume-hierarchy, primary-ray-generation, beam-tracing, frustum-culling]
sources:
  - paper: doi:10.1111/1467-8659.00508
    title: Ingo Wald, Philipp Slusallek, Carsten Benthin and Markus Wagner, Interactive rendering with coherent ray tracing, Computer Graphics Forum 20(3) (Eurographics 2001), pages 153 to 165
    locator: the tracing of packets of four coherent rays in parallel with SSE, the traversal of the kd-tree by the packet, and the cache-aware data layout
  - paper: doi:10.1145/1189762.1206075
    title: Ingo Wald, Solomon Boulos and Peter Shirley, Ray tracing deformable scenes using dynamic bounding volume hierarchies, ACM Transactions on Graphics 26(1), 2007, article 6
    locator: the traversal of a BVH by large packets, with the early test of the first active ray and the frustum test of the whole packet
  - paper: doi:10.1145/1073204.1073329
    title: Alexander Reshetov, Alexei Soupikov and Jim Hurley, Multi-level ray tracing algorithm, ACM Transactions on Graphics 24(3) (SIGGRAPH 2005), pages 1176 to 1185
    locator: the search for a common entry point in the kd-tree for a whole beam of rays before the packet splits
  - paper: doi:10.1145/1572769.1572792
    title: Timo Aila and Samuli Laine, Understanding the efficiency of ray traversal on GPUs, High Performance Graphics 2009, pages 145 to 149
    locator: the comparison of traversal loops for single rays on SIMT hardware, where the warp plays the role of the packet
  - paper: doi:10.1145/1268517.1268547
    title: Solomon Boulos, Dave Edwards, J. Dylan Lacewell, Joe Kniss, Jan Kautz, Peter Shirley and Ingo Wald, Packet-based Whitted and distribution ray tracing, Graphics Interface 2007
    locator: packets of secondary rays for reflection, refraction, shadows and distribution effects
---

Ray packet tracing sends a group of rays, a *packet*, through a [bounding volume hierarchy](/bounding-volume-hierarchy/) or a [kd-tree](/kd-tree-traversal/) as one unit. The packet keeps one traversal stack. At each node it tests the box against all rays that are still active, with one ray per SIMD lane, and it descends into a child if at least one ray needs it. Each node is then fetched from memory once for the whole packet instead of once per ray. The result for each ray is exactly what tracing it alone would give. The method pays off for [coherent rays](/ray-coherence/), such as the primary rays of a tile of pixels, which visit almost the same nodes. For rays that go in unrelated directions, most lanes sit idle. Wald, Slusallek, Benthin and Wagner introduced it in 2001 with packets of four rays. The speedups reported for it are measurements on particular scenes and processors, not proved bounds.

## In plain words

A tour guide takes sixteen people through a museum. The visitors all want to see roughly the same rooms. It is quicker if the guide opens each door once for the whole group than if each visitor walks the museum alone and opens every door again.

When the group reaches a door to a wing that only some of them want to see, the others wait outside. That waiting is the cost of going together. If each visitor wants a different part of the museum, the group spends most of its time waiting, and going alone is better.

For a ray tracer the rooms are the nodes of a tree of boxes, the door is a memory fetch of a node, and the waiting visitors are SIMD lanes that do no useful work.

## The problem

Given a BVH over $n$ primitives and a packet of $m$ rays $o_i + t d_i$ with limits $t \in (0, t_{\max}]$, find for each ray its closest hit: the smallest $t$ at which it meets a primitive, and which primitive. Ties at equal $t$ go to the smaller primitive index, so that the answer does not depend on the order of the search. This is the [closest-hit query](/closest-hit-query/) for $m$ rays at once.

## The algorithm

```pseudo id=main
L1  for each ray i: best[i] ← none, limit[i] ← tmax
L2  stack ← [(root, all rays)]
L3  while stack is not empty
L4      (node, M) ← pop(stack)
L5      M ← {i ∈ M : ray i meets node.box for some t in [0, limit[i]]}   ▷ one SIMD test
L6      if M is empty then continue
L7      if node is a leaf then
L8          for each primitive k of node and each i ∈ M:
                if ray i hits k at t ≤ limit[i] and (t, k) < best[i] then best[i] ← (t, k), limit[i] ← t
L9      else
L10         order the children near to far by the sign of a ray of M along the split axis
L11         push (far, M); push (near, M)
L12 return best
```

A packet of one ray is the ordinary depth-first [BVH traversal](/bvh-traversal/). Line L5 uses the current `limit` of each ray, so a ray that has found a hit drops out of nodes that lie behind it, even if the node was pushed before the hit was found. In a SIMD version, $M$ is a bit mask, line L5 runs the [slab test](/slab-method/) for four, eight or sixteen rays in one instruction sequence, and line L6 tests whether the mask is zero.

## Example

The measurements come from the implementation. The scene is a height field of $8 \times 8$ squares, split into 128 triangles, under a BVH of 127 nodes with up to two triangles per leaf. A camera at $(4, -6, 8)$ shoots $16 \times 16$ primary rays at the field, and 240 of them hit it. The image is cut into square tiles, and each tile is one packet. A *lane slot* is one ray position in one node visit: a SIMD unit as wide as the packet spends one slot per visit and per ray, whether that ray is active or not.

| packet | node visits | ray-node tests | lane slots | useful slots |
|---|---|---|---|---|
| single rays | 4114 | 4114 | 4114 | 100% |
| $2 \times 2$ tiles | 1238 | 4114 | 4952 | 83% |
| $4 \times 4$ tiles | 446 | 4114 | 7136 | 58% |
| $8 \times 8$ tiles | 172 | 4114 | 11008 | 37% |
| $16 \times 16$, one packet | 123 | 4114 | 31488 | 13% |
| 16 random rays per packet | 1414 | 4114 | 22624 | 18% |

Every ray took part in the same 4114 ray-node tests in total, so the work of the box tests did not change. What changed is the number of node fetches, which fell from 4114 to 446 with $4 \times 4$ packets, and the share of lanes that did useful work, which fell as the packets grew. Packets of sixteen rays taken at random from the same image fetch more than three times as many nodes as $4 \times 4$ tiles, at less than a third of their lane use. All packets returned exactly the hits of single rays and of a linear scan over all triangles.

## Correctness

Fix a ray $i$ and a primitive $k$ that it hits at $t_k \le t_{\max}$. Let $N_0, \dots, N_\ell$ be the nodes on the path from the root to the leaf that holds $k$. Each box contains $k$, so the ray meets each box at the point of the hit, for $t = t_k$. While $(t_k, k) < best[i]$, we have $t_k \le limit[i]$, so line L5 keeps $i$ in the mask of every $N_j$ that it pops, and line L11 pushes $N_{j+1}$ with $i$ in the mask. The leaf $N_\ell$ is therefore popped with $i$ active, unless $best[i]$ becomes at most $(t_k, k)$ before. At the leaf, line L8 tests $k$. So at the end $best[i] \le (t_k, k)$ for every primitive $k$ that the ray hits, and $best[i]$ is the hit of a primitive, so it is the smallest pair. Each node is pushed only when its parent is popped, so it is popped at most once, and the loop stops after at most $2n - 1$ pops for a tree with leaves of one or more primitives. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $v$ be the number of nodes that the packet visits. The time is $\Theta(v m)$ for the box tests in a SIMD version, where every lane is tested at every visit, plus the primitive tests of the active rays in the leaves. Since $v \le 2n - 1$, the worst case is $O(m n)$, the same as $m$ separate traversals. The best case is $\Theta(m)$, when all rays miss the root box. The extra space is the stack: at most $h + 1$ entries for a tree of height $h$, because each pop pushes two children, and each entry holds a mask of $m$ bits. So it is $O(m h)$ as a list of indices and $O(h)$ words when $m$ fits in a machine word.

The point of packets is not the operation count. The number of ray-node tests is about the same as for single rays, as in the example. What falls is the number of node fetches, from about $m v_1$ for $m$ single rays that each visit $v_1$ nodes to about $v$, which is close to $v_1$ for a coherent packet. On a processor where a memory fetch costs far more than an arithmetic instruction (see the [memory hierarchy](/memory-hierarchy/)), and where a SIMD instruction tests four to sixteen rays for the price of one, this gives the speedup. How large it is depends on the scene, the packet size and the hardware. It is measured, not proved.

## Properties

- **Exact.** Each ray gets the same closest hit as alone, with the same tie rule. The tests check this with exact rational arithmetic against single-ray traversal and a linear scan.
- **One fetch per node per packet.** A node is visited at most once by a packet.
- **Not work-optimal per ray.** A ray can be tested against boxes that it would have skipped alone, because the near child is chosen by the direction of another ray, and because inactive lanes compute too.
- **Order-independent result.** The order of the rays in the packet and the order of the children change the counts, not the answers.
- **Needs coherence.** The gain depends on how many nodes the rays share. Primary rays and shadow rays toward one point light share many. Rays after a diffuse bounce share few.

## Variants and improvements

- **kd-tree packets.** Wald et al. (2001) traversed a kd-tree with packets of four rays. A kd-tree split is crossed in the same order by all rays whose direction has the same sign on the split axis, which is why kd-tree packets are simplest when all rays share their direction signs.
- **First active ray and frustum test.** For large packets in a BVH, Wald, Boulos and Shirley (2007) first test the first active ray, and descend with the whole packet if it hits. Otherwise a frustum test of the whole packet against the box can discard the node without testing each ray. Only when both fail are the rays tested one by one.
- **Entry point search.** The multi-level ray tracing algorithm of Reshetov, Soupikov and Hurley (2005) bounds a packet by a frustum, finds the deepest kd-tree node that the whole frustum must start from, and starts all rays there.
- **Secondary rays.** Boulos et al. (2007) packed reflection, refraction, shadow and distribution rays into packets. Rays can also be sorted or regrouped into new packets after each bounce, to restore coherence.
- **Single rays on SIMT hardware.** On a GPU, the 32 threads of a warp run one traversal each, and the hardware forms the group. A warp in which threads need different nodes suffers [warp divergence](/warp-divergence/), which is the same loss of lane use as an incoherent packet. Aila and Laine (2009) studied such traversal loops on the [SIMT model](/simt-model/).
- **Wide trees instead of wide packets.** A BVH with four or eight children per node uses the SIMD lanes to test one ray against several boxes. It helps incoherent rays, where packets do not.

## When to use it

Use packets for groups of rays that are known to be coherent: primary rays of a pixel tile from a [pinhole camera](/pinhole-camera-model/), shadow rays from nearby points toward one light, and the rays of one pixel's samples. Use single rays, a wide tree or a regrouping step for paths after diffuse bounces, where neighboring rays go in unrelated directions. Packet tracing is an implementation technique for speed. It changes no result and no asymptotic bound, so it is worth its complexity only where profiling shows that node fetches dominate.

## Pitfalls

- **Testing against a stale limit.** If line L5 used the limit from the time the node was pushed, rays would stay active in nodes behind their hit. The answer stays right, but the work grows.
- **Tie rules that depend on order.** With a rule "replace only if $t$ is smaller", the triangle returned for a tie depends on the visiting order, and a packet and a single ray can return different primitives with the same $t$. Compare $(t, k)$ pairs, as line L8 does, when exact agreement matters.
- **Mixed direction signs.** Ordering children by one ray's direction is fine for a BVH, where both children are always tested. In a kd-tree traversal that clips the $t$ interval at the split plane, rays with opposite signs need separate handling, or the packet must be split.
- **Packets that are too large.** Lane use falls as packets grow. In the example, one packet of 256 rays uses 13% of its lanes. Choose the size after measuring.
- **Divergent materials.** After the hit, shading code that differs per ray loses the same SIMD efficiency. Group shading work by material, or shade one ray at a time.
- **Measuring the wrong thing.** A count of box tests can show no gain from packets while the running time falls, because the gain is in memory traffic. Measure time, cache misses and lane use, not only operation counts.

## Implementations

## History

Before packets, ray tracers traced one ray at a time. In 2001, Wald, Slusallek, Benthin and Wagner combined three ideas on commodity PCs: packets of four coherent rays traced in parallel with SSE instructions, a kd-tree traversal written for the packet, and a data layout tuned to the cache. They reported interactive frame rates, measured on their scenes. Reshetov, Soupikov and Hurley (2005) added the shared entry point for beams of rays. Wald, Boulos and Shirley (2007) moved large packets to BVHs, which can be rebuilt or refitted for animated scenes. Boulos et al. (2007) extended packets to secondary rays. On GPUs the hardware groups single-ray traversals into warps, and Aila and Laine (2009) showed how close such per-ray loops can come to the limits of the hardware.

## References
