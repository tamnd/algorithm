---
tag: NPGSAB
kind: data-structure
slug: texture-clipmap
name: Texture clipmap
aliases:
- clipmap
area: graphics-and-signals/real-time-rendering
level: advanced
summary: A mipmap whose finer levels are clipped to a fixed-size window around the viewer, so that very large textures fit in a bounded memory.
model: real-ram
complexity:
  vars: {N: the side of the finest level in texels, C: the clip size in texels, d: "the number of finest-level texels by which the center moves, along one axis"}
  time: {build: Θ(C^2 (1 + log(N/C))), recenter: O(C (d + log(N/C))), lookup: O(1)}
  space: {total: Θ(C^2 (1 + log(N/C)))}
properties: {persistent: false, concurrent: false, external: true}
history:
  year: 1998
  people: [Christopher C. Tanner, Christopher J. Migdal, Michael T. Jones]
  note: Tanner, Migdal and Jones presented the clipmap at SIGGRAPH 98 as a virtual mipmap for textures much larger than texture memory.
prereqs: [mipmap, texture-mapping]
see_also: [geometry-clipmaps, virtual-texturing, level-of-detail, circular-buffer, bilinear-filtering, anisotropic-filtering]
sources:
  - paper: doi:10.1145/280814.280855
    title: Christopher C. Tanner, Christopher J. Migdal and Michael T. Jones, The clipmap, a virtual mipmap, SIGGRAPH 98, 151 to 158
    locator: the clip stack and the clip pyramid, the clip center, the toroidal update of the clipped levels, and the choice of a coarser level outside the clip region (general locator)
  - paper: doi:10.1145/1015706.1015799
    title: Frank Losasso and Hugues Hoppe, Geometry clipmaps, terrain rendering using nested regular grids, ACM Transactions on Graphics 23(3), SIGGRAPH 2004, 769 to 776
    locator: the comparison with the texture clipmap and the reuse of its nested windows for geometry (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: the part on texture streaming and very large textures in the chapter on texturing (general locator)
---

A texture clipmap is a [mipmap](/mipmap/) in which every level larger than a clip size $C$ keeps only a $C \times C$ window of texels around a *clip center*, the point of the texture that the viewer looks at; the levels of size $C$ or less are kept whole. A full mipmap of a $16384^2$ texture takes about 358 million texels, and a clipmap with $C = 512$ takes 1.66 million. [Virtual texturing](/virtual-texturing/) keeps the pages that the view needs, wherever they are, with a page table; the clipmap keeps fixed windows around one point, so it needs no table, and a lookup only has to find the finest level whose window holds the point. [Geometry clipmaps](/geometry-clipmaps/) use the same nested windows for the heights of a terrain.

## In plain words

A huge photo of the ground is too big for the graphics card, and a viewer near the ground sees fine detail only close by. Far away, the coarse versions of the photo are enough.

So keep each coarse version of the photo whole while it is small. For each large version, keep only a square of fixed size around the place under the viewer. The squares of the finer versions cover smaller areas, and the coarsest versions cover everything.

To color a point, use the finest version whose square holds that point. When the viewer moves, each square moves with them. Only the strip of new texels on one side is loaded, and it goes into the place of the strip that drops off the other side.

## The abstract type

A texture clipmap of a texture with the mipmap levels $0$ (finest, $N \times N$) to $\log_2 N$ (one texel) has these operations.

- **build(c)**: make the clipmap for the clip center $c$.
- **recenter(c)**: change the clip center to $c$, so that every clipped level holds its new window.
- **lookup(u, v, lambda)**: the filtered sample at the point $(u, v)$ for the level of detail $\lambda$ that the hardware computes, but from a coarser level if the window of level $\lambda$ does not hold the point.

Inside the windows, lookup gives the same value as the full mipmap. Outside, it gives a value of a coarser level, which is a blur, not a wrong texel.

## Representation

Level $l$ has $N / 2^l$ texels along each side. The levels with $N / 2^l > C$ form the *clip stack*: each is an array $S_l$ of $C \times C$ texels. The clip center at level $l$ is $c_l = \lfloor c / 2^l \rfloor$ per coordinate, and the window of level $l$ is the square of texels $t$ with $c_l - C/2 \le t < c_l + C/2$ in each coordinate. The texel $t$ is stored at the slot $(t_x \bmod C, t_y \bmod C)$, a *toroidal* address as in a [circular buffer](/circular-buffer/), so a texel that stays in the window keeps its slot when the center moves. The levels with $N / 2^l \le C$ form the *clip pyramid* and are stored whole, as in a mipmap.

In level 0 units the window of level $l$ is a square of side $C \cdot 2^l$, so each level of the stack covers four times the area of the level before it, and the pyramid covers the whole texture. The full texture stays on disk or in main memory, and the stack is filled from it.

## Operations

```pseudo id=main
RECENTER(c)                                       ▷ the new clip center, in level 0 texels
L1  for each level l of the clip stack do
L2      c_l ← floor(c / 2^l)                          ▷ per coordinate
L3      for each texel t with c_l - C/2 ≤ t < c_l + C/2 that is not in the old window do
L4          S_l[t_x mod C, t_y mod C] ← texel t of level l, read from the full texture
L5      the window of level l ← the new window

LOOKUP(u, v, λ)                                   ▷ λ from the texel footprint, as for a mipmap
L6  l_min ← the smallest l such that the levels l, l + 1, ... all hold the bilinear taps of (u, v)
L7  l ← max(λ, l_min)
L8  return the trilinear sample between the levels floor(l) and floor(l) + 1
```

BUILD is RECENTER with every texel new, plus the fill of the pyramid. The pyramid levels hold every point. The code finds $l_{\min}$ in line L6 by a walk from the coarsest level down, in $O(\log(N/C))$ steps. A renderer can compute it in $O(1)$: a window of level $l$ reaches about $C \cdot 2^{l-1}$ level 0 texels from the center, so $l_{\min}$ follows from the largest coordinate distance between $(u, v)$ and $c$ with a logarithm, and a margin of a few texels covers the filter; that margin is a tuning.

## Example

Take a $16384 \times 16384$ texture and $C = 512$. The levels have the sides 16384, 8192, ..., 1. The five levels of side 16384 to 1024 form the stack, with $5 \cdot 512^2 = 1{,}310{,}720$ texels. The pyramid holds the levels of side 512 to 1, with $(4^{10} - 1)/3 = 349{,}525$ texels. So the clipmap has 1,660,245 texels, against 357,913,941 for the full mipmap: 215.6 times fewer. At 4 bytes per texel, that is 6.64 MB in place of 1.43 GB.

**A lookup.** The clip center is $c = (8000, 8000)$ and the point is at the level 0 texel $(8400, 8100)$, with $\lambda = 0$.

| level | center $c_l$ | the point at this level | window holds the point |
|---|---|---|---|
| 0 | $(8000, 8000)$ | $(8400, 8100)$ | no, $8400 \ge 8000 + 256$ |
| 1 | $(4000, 4000)$ | $(4200, 4050)$ | yes |
| 2 | $(2000, 2000)$ | $(2100, 2025)$ | yes |

So line L6 gives $l_{\min} = 1$, and the lookup returns a sample of level 1 where the full mipmap would give level 0. The point is 400 texels from the center, and the full level 0 detail reaches only 256.

**A move.** Moving the center by 64 texels of level 0 in $x$ moves the windows of the levels 0 to 4 by 64, 32, 16, 8 and 4 texels. Line L4 then loads $512 \cdot (64 + 32 + 16 + 8 + 4) = 63{,}488$ texels, against 1,310,720 for a reload of the whole stack.

## Correctness

The proof file gives the arguments. The tests compare the stack after 60 random moves with a fresh fill and with the full mipmap, and compare 800 lookups with trilinear samples of the full mipmap.

- **One slot per texel.** The texels of a window have, in each coordinate, $C$ consecutive values, which have $C$ distinct residues mod $C$. So the toroidal slots of line L4 are one to one on a window (a proved property).
- **The update.** A texel in both the old and the new window keeps its slot and its value, and line L4 writes each new texel. So after line L5 each stack level holds exactly its new window, as a fresh fill would (a proved property).
- **The lookup.** The lookup reads only texels inside the windows, and it returns the trilinear sample of the full mipmap at $\max(\lambda, l_{\min})$. So if $l_{\min} \le \lambda$, it equals the sample of the full mipmap. Otherwise $l > \lambda$, and the sample comes from a coarser level of the same mipmap, so it is a blurred value of the right image (a proved property of the structure; how visible the blur is depends on the scene).
- **Nesting.** In level 0 units the window of level $l$ is $[2^l (c_l - C/2), 2^l (c_l + C/2))$ in each coordinate, and $2^l c_l$ lies in $(c - 2^l, c]$. Comparing the two ends with those of level $l + 1$ shows that for $C \ge 4$ each window lies inside the next coarser one. So the levels that hold a point are $l_{\min}$ and all coarser ones, and line L6 is well defined (a proved property).

## Complexity

| operation | time | note |
|---|---|---|
| build | $\Theta(C^2 (1 + \log(N / C)))$ | each stack level and the pyramid once |
| recenter | $O(C (d + \log(N / C)))$ | a move by $d$ level 0 texels along one axis writes at most $C (d / 2^l + 1)$ texels at level $l$; the $+1$ is the rounding of $c_l$ |
| lookup | $O(1)$ | the level from the distance to the center, then a mipmap sample; the walk of the code takes $O(\log(N / C))$ |

The space is $\Theta(C^2 (1 + \log(N / C)))$: $C^2$ texels for each of the $\log_2(N / C)$ stack levels, and less than $\frac43 C^2$ for the pyramid. The full mipmap needs $\Theta(N^2)$. The cost of a recenter is dominated in practice by the reads from disk or main memory, which is why the structure is external.

## Variants

- **Virtual texturing.** [Virtual texturing](/virtual-texturing/) splits all levels into pages and keeps the pages that the frame uses, with a page table per lookup. It serves views where the needed texels are not around one point, such as many objects with their own textures.
- **Geometry clipmaps.** [Geometry clipmaps](/geometry-clipmaps/) use the same stack for the heights of a terrain, with the window centered on the viewer.
- **Several centers.** A scene with two areas of interest, such as two viewers, needs two stacks or larger windows; the clipmap serves one center well.
- **Updates over several frames.** A large move can load the new strips over several frames, and the lookup uses a coarser level until a strip is complete, which a margin in line L6 makes safe.

## When to use it

Use a texture clipmap for one very large texture seen from a viewer that moves over it, such as satellite images on a terrain in a flight simulator or a map viewer, when the full mipmap does not fit in texture memory. If the texels in view are spread over many textures, or the view jumps far from frame to frame, [virtual texturing](/virtual-texturing/) fits better. If the texture fits in memory, a plain [mipmap](/mipmap/) is simpler.

## Pitfalls

- **An address relative to the window.** If line L4 stores the texel at $t - (c_l - C/2)$ in place of $t \bmod C$, the slot of every texel changes when the center moves, and each move must copy the whole stack.
- **No margin for the filter.** If line L6 tests only the point and not its footprint, a bilinear or trilinear sample near the border of a window reads texels outside it, which hold values of the opposite side of the window.
- **The wrong level.** If line L7 uses $\min$ in place of $\max$, the lookup can read a finer level than the hardware asked for, and the texture aliases; or, with a window that does not hold the point, it reads a wrong texel.
- **One center for all levels without rounding.** If line L2 uses $c / 2^l$ without the floor, the windows of the levels do not start on texel borders, and the test of line L6 and the slots of line L4 disagree by one texel.
- **A visible edge between levels.** Where $l_{\min}$ jumps from one level to the next across the image, the sharpness changes along a line. Blending between $\lfloor l \rfloor$ and $\lfloor l \rfloor + 1$ in line L8 with a fractional $l_{\min}$ near the border hides it.

## Implementations

## History

Tanner, Migdal and Jones presented the clipmap at SIGGRAPH 98 as a "virtual mipmap": a mipmap of a texture much larger than texture memory, in which only a window around a point of interest is kept for each fine level, and the windows are updated toroidally as the point moves. Losasso and Hoppe took the same nested windows from textures to terrain geometry in 2004, as [geometry clipmaps](/geometry-clipmaps/). Later systems for large textures moved to page-based [virtual texturing](/virtual-texturing/), which does not need a single center of interest.

## References
