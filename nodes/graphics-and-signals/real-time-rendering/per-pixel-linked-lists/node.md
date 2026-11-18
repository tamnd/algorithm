---
tag: XK6ZQN
kind: algorithm
slug: per-pixel-linked-lists
name: Per-pixel linked list transparency
aliases:
- per-pixel fragment lists
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Append every transparent fragment to a linked list per pixel on the GPU with an atomic counter, then sort and blend each list in a resolve pass.
solves: [order-independent-transparency]
model: word-ram
complexity:
  vars: {f: the number of transparent fragments, p: the number of pixels, k: the largest number of fragments of one pixel, n: the number of nodes in the pool}
  time: {build: O(f), resolve: O(p + f k), worst: O(p k^2)}
  space: {total: O(p + n)}
properties: {deterministic: false, recursive: false, online: false, in_place: false}
history:
  year: 2010
  people: [Jason C. Yang, Justin Hensley, Holger Grün, Nicolas Thibieroz]
  note: Yang, Hensley, Grün and Thibieroz built linked lists of fragments per pixel on the GPU with atomic operations and sorted them in a resolve pass, in a paper at EGSR 2010.
prereqs: [order-independent-transparency, linked-list, fetch-and-add]
see_also: [a-buffer, weighted-blended-oit, depth-peeling, insertion-sort, memory-pool, compare-and-swap, alpha-blending, sorting-network]
sources:
  - paper: "Jason C. Yang, Justin Hensley, Holger Grün and Nicolas Thibieroz, Real-time concurrent linked list construction on the GPU, Computer Graphics Forum 29(4) (EGSR 2010), 1297-1304"
    locator: the head pointer buffer, the node buffer with an atomic counter, the atomic exchange that links a new node, and the sort and blend of each list in a second pass
  - url: http://jcgt.org/published/0002/02/09/
    title: "Morgan McGuire and Louis Bavoil, Weighted blended order-independent transparency, Journal of Computer Graphics Techniques 2(2), 122-141, 2013"
    locator: the review of exact methods with unbounded memory per pixel, and their cost compared with one-pass approximations
  - paper: doi:10.1145/800031.808606
    title: "Thomas Porter and Tom Duff, Compositing digital images, SIGGRAPH 1984, Computer Graphics 18(3), 253-259"
    locator: the over operator used by the resolve pass
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 5.5, Transparency, Alpha, and Compositing (the part on per-pixel lists of fragments)
---

Per-pixel linked lists are an exact method for [order-independent transparency](/order-independent-transparency/) on the GPU. In one geometry pass, every transparent fragment takes a free node from a large shared buffer by an atomic increment of a counter, stores its color, opacity and depth there, and links the node to the front of the list of its pixel with an atomic exchange on a head pointer. In a second, full-screen pass, each pixel walks its list into a small local array, sorts it by depth, and blends it back to front with the over operator. The method is a GPU form of the [A-buffer](/a-buffer/). Yang, Hensley, Grün and Thibieroz described it in 2010. It is exact as long as the shared buffer does not fill up, and its memory grows with the number of fragments.

## In plain words

Each pixel keeps a chain of notes, one note per transparent surface that covers it. A big box of blank notes is shared by the whole screen. When a surface is drawn at a pixel, it takes the next blank note, by asking a shared counter for a number that nobody else gets, writes its color and depth on it, and pins it to the front of the chain of that pixel. Thousands of surfaces do this at the same time, so the two steps that touch shared things are atomic. When all surfaces are drawn, each pixel reads its chain, puts the notes in order from near to far, and blends them from the back. If the box of notes runs out, the late surfaces are lost.

## The problem

The input is a stream of transparent fragments $(q, c, \alpha, z)$ produced by the rasterizer in an unknown order and in parallel: the pixel $q$, the premultiplied color $c$, the opacity $\alpha$ and the view depth $z$, smaller is nearer. The opaque pass has already written the background color $C_0$ and depth of each pixel, and fragments behind the opaque depth are discarded by the depth test. The output is, for each pixel, the composite in depth order

$$C = \sum_i c_i \prod_{j < i} (1 - \alpha_j) + C_0 \prod_i (1 - \alpha_i),$$

with the fragments of the pixel numbered from front to back. The machine is the word RAM with the atomic operations ATOMIC-ADD (fetch and add) and ATOMIC-EXCHANGE, as GPUs provide on buffers and images.

## The algorithm

Line L1 runs once per frame. Lines L2 to L5 run once per fragment, in parallel, in the fragment shader. Lines L6 to L10 run once per pixel, in a full-screen pass after the build. $n$ is the capacity of the node pool.

```pseudo id=main
PER-PIXEL-LINKED-LISTS(fragments, C0)
L1  head[q] ← NULL for every pixel q;  counter ← 0
L2  idx ← ATOMIC-ADD(counter, 1)                          ▷ for each fragment (q, c, α, z), in parallel
L3  if idx ≥ n then drop the fragment and stop
L4  node[idx].(c, α, z) ← (c, α, z)
L5  node[idx].next ← ATOMIC-EXCHANGE(head[q], idx)
L6  a ← empty;  i ← head[q]                               ▷ for each pixel q, after a barrier
L7  while i ≠ NULL: append node[i] to a;  i ← node[i].next
L8  INSERTION-SORT(a) by z, nearest first
L9  C ← C0[q];  for j from |a| down to 1: C ← c_j + (1 - α_j) C
L10 out[q] ← C
```

**The pool (lines L2 to L4).** The node buffer is one large array shared by all pixels, and the counter is a [fetch-and-add](/fetch-and-add/) allocator over it, as in a [memory pool](/memory-pool/) that never frees. Each fragment gets a distinct index, so the writes of line L4 never collide.

**The link (line L5).** The exchange puts the new node at the head of the list and returns the old head, which becomes the next field of the new node. This is the push of a [linked list](/linked-list/) stack, made safe for many writers by doing the read and the write of the head as one atomic step. No thread ever reads the next field during the build, so no lock and no [compare-and-swap](/compare-and-swap/) loop is needed.

**The resolve (lines L6 to L10).** The list is read into a local array of a fixed size, often 8 to 64 entries. [Insertion sort](/insertion-sort/) is the usual choice, because the lists are short and the code is small. The fold of line L9 is the over operator of [alpha blending](/alpha-blending/) from back to front.

**Memory.** A node holds the color, the opacity, the depth and the next index, for example 4 bytes of RGBA8, 4 bytes of depth and 4 bytes of index: 12 bytes. The head image holds one 32-bit index per pixel.

## Example

Two pixels and a pool of 3 nodes. Four fragments arrive: green at pixel 0 with $c = (0, 0.25, 0)$, $\alpha = 0.25$, $z = 3$; red at pixel 0 with $c = (0.5, 0, 0)$, $\alpha = 0.5$, $z = 1$; blue at pixel 1 with $c = (0, 0, 0.5)$, $\alpha = 0.5$, $z = 2$; and blue again at pixel 0 with $z = 2$. Say the threads run in this order without overlap.

| step | counter after | idx | head[0] | head[1] | next[idx] |
|---|---|---|---|---|---|
| green at 0 | 1 | 0 | 0 | NULL | NULL |
| red at 0 | 2 | 1 | 1 | NULL | 0 |
| blue at 1 | 3 | 2 | 1 | 2 | NULL |
| blue at 0 | 4 | 3 | dropped | | |

The pool is full, so the last fragment is lost. Pixel 0 walks $1 \to 0$, which is red then green, sorts them to red ($z = 1$), green ($z = 3$), and over black gives green $(0, 0.25, 0)$, then red over it: $(0.5, 0, 0) + 0.5 \cdot (0, 0.25, 0) = (0.5, 0.125, 0)$. With a pool of 4 nodes, the blue fragment would also be in the list of pixel 0, and the result would be $(0.5, 0.0625, 0.25)$. In another interleaving, a different fragment could win the last node, so with overflow the image depends on the timing.

## Correctness

The proofs are in the proofs folder, under the assumption that the atomic operations are linearizable and that the resolve starts after the build has finished. The counter gives the values $0, 1, \dots, f - 1$ to distinct threads, so the kept fragments have distinct nodes. Fix a pixel. Its exchanges happen in some total order, and each returns the node of the one before it, or NULL for the first. Each thread writes that value into the next field of its own node. So after the build, the list of the pixel runs through all its kept nodes in the reverse order of the exchanges and ends at NULL, with no node twice. The resolve then sorts the fragments by depth and folds the over operator, which is the definition of the composite. So the result is exact for every interleaving when the pool does not overflow and depths are distinct. With overflow, the result is the exact composite of the kept fragments. The tests run the build under many random interleavings of the atomic steps, in exact rational arithmetic, and check all three claims.

## Complexity

The model is the word RAM with atomic fetch-and-add and exchange. The build does $O(1)$ work and at most two atomic operations per fragment, $O(f)$ in total. The resolve reads every list once, $O(p + f)$, and sorts each list of $k_q$ fragments in $O(k_q^2)$, which sums to at most $O(f k)$ with $k$ the longest list. The memory is $p$ head pointers and $n$ nodes. At 1920 by 1080 pixels with an average of 4 transparent fragments per pixel and 12-byte nodes, the pool needs $2\,073\,600 \cdot 4 \cdot 12 = 99\,532\,800$ bytes, about 94.9 MiB, plus 7.9 MiB of heads.

On a GPU, all fragments of the frame contend on one counter. The hardware merges atomic increments within a warp, but the counter is still a hot spot. The resolve diverges when neighboring pixels have lists of very different length.

## Properties

- **Exact when the pool is large enough.** Every fragment is kept and sorted.
- **One geometry pass.** Unlike [depth peeling](/depth-peeling/), the scene is drawn once.
- **Unbounded memory.** The pool must be sized for the worst frame, or fragments are dropped.
- **Nondeterministic order.** The order of a list depends on timing. The image does not, unless the pool overflows or two depths are equal.
- **Lock-free.** No thread waits for another. Each fragment finishes in a fixed number of steps.
- **Local array limit.** The resolve can hold only a fixed number of fragments per pixel. Longer lists must be truncated or merged.

## Variants and improvements

- **Per-pixel arrays.** Count the fragments of each pixel in a first pass, compute offsets with a prefix sum, and write the fragments into a packed array in a second pass. The memory is exact but the geometry is drawn twice.
- **Fixed-size arrays per pixel.** Reserve $s$ slots per pixel and an atomic counter per pixel. There is no shared pool, but the memory is $p s$ and long lists overflow.
- **Insertion during the build.** Keep each list sorted by inserting new fragments in depth order with compare-and-swap. The resolve need not sort, but the build is slower and contended.
- **Keep the nearest $s$.** Merge fragments behind the first $s$ into one approximate layer, as in the k-buffer.
- **Sorting networks.** For a fixed local array size, a [sorting network](/sorting-network/) has no branches and can be faster than insertion sort on SIMT hardware.
- **MSAA.** Store a coverage mask in each node, as the A-buffer does.

## When to use it

Use it when the transparent content needs exact order, such as overlapping colored glass, scientific visualization with many layers, or reference images to test approximate methods against. It needs a memory budget for the worst depth complexity. For particles and smoke with very many layers and similar colors, [weighted blended OIT](/weighted-blended-oit/) is cheaper and has fixed memory.

## Pitfalls

- **Pool overflow.** A full pool drops fragments silently and the image changes with the timing. Check the counter after the frame and grow the pool, or fall back to an approximate method.
- **Local array overflow.** Lists longer than the local array of the resolve lose fragments. Clamp and report it.
- **No barrier.** The resolve must start after all writes of the build are visible. Use a memory barrier between the passes.
- **Early depth test.** Without the opaque depth test, fragments behind opaque surfaces fill the pool.
- **Resetting.** The head image must be set to NULL and the counter to 0 each frame. A stale head points to nodes of the previous frame.
- **Ties.** Coplanar transparent surfaces give equal depths, and the result then flickers with the timing. Break ties by a primitive id.

## Implementations

## History

The A-buffer of Carpenter (1984) kept a list of fragments per pixel in a software renderer, and depth peeling made exact transparency possible on GPUs without such lists, at one geometry pass per layer. When GPUs gained atomic operations and writes to arbitrary buffers from the fragment shader, Yang, Hensley, Grün and Thibieroz (2010) built the lists on the GPU in one pass with a global counter and an atomic exchange on a head pointer per pixel, and sorted and blended each list in a second pass. The method became a common reference for exact order-independent transparency, and later work on bounded memory, such as weighted blended OIT, compares against it.

## References
