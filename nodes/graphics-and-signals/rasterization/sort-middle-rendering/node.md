---
tag: H4TG4K
kind: concept
slug: sort-middle-rendering
name: Sort-middle rendering
aliases:
- sort-middle architecture
area: graphics-and-signals/rasterization
level: advanced
summary: A parallel renderer that splits the triangles freely among geometry units and then sends each screen-space triangle to the rasterizers of the screen regions it overlaps.
prereqs: [graphics-pipeline, tiled-rasterization]
see_also: [tiled-rasterization, graphics-pipeline, load-balancing-problem, image-compositing, z-buffer, bucket-sort, work-span-model, frame-buffer]
sources:
  - paper: doi:10.1109/38.291528
    title: Steven Molnar, Michael Cox, David Ellsworth and Henry Fuchs, A sorting classification of parallel rendering, IEEE Computer Graphics and Applications 14(4), 23 to 32, 1994
    locator: the whole paper (sort-first, sort-middle and sort-last; the overlap factor; the costs of sort-middle; Pixel-Planes 5, RealityEngine and Leo as sort-middle machines)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 18, Advanced Raster Graphics Architecture (by Steven Molnar and Henry Fuchs; parallel geometry and rasterization, and image partitions)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 23, Efficiency and Hardware (the sorting classes of parallel rendering and tile-based architectures)
---

Sort-middle rendering is the class of parallel renderers that redistribute the work between geometry processing and rasterization. The triangles are split among the geometry units in any balanced way. After each unit has transformed, clipped and projected its triangles, it sends each one to the rasterizers that own the screen regions the triangle overlaps. Each rasterizer then draws only its own region, with its own part of the [z-buffer](/z-buffer/) and the [frame buffer](/frame-buffer/). Molnar, Cox, Ellsworth and Fuchs (1994) named this class, together with sort-first and sort-last, by the point in the [graphics pipeline](/graphics-pipeline/) where a renderer sorts from object order to screen order. The cost of the sort is set by the overlap factor, the mean number of regions that a triangle touches.

## In plain words

Drawing a picture with many workers needs a way to split the job. The first half of the job, moving and projecting the triangles, can be split any way: give each worker the same number of triangles. The second half, filling the dots, is easier to split by place: give each worker one part of the screen.

Sort-middle does the first half with the first split and the second half with the second split. In the middle, each triangle is sent to the workers whose parts of the screen it lands on.

A triangle that lands across a border goes to more than one worker, so some triangles are sent and set up twice or more. And if most triangles land in one part of the screen, the worker for that part gets most of the work while the others wait.

## The idea

**The three classes.** A renderer does geometry processing (transform, lighting, clipping, projection) and then rasterization ([triangle rasterization](/triangle-rasterization/), shading, depth test). Geometry is naturally split by object: any unit can transform any triangle. Rasterization is naturally split by screen: two units that own different pixels never conflict. So somewhere the work must be sorted from object order to screen order, and Molnar et al. classify renderers by where:

- **Sort-first.** Before geometry processing. Each unit owns a screen region and gets the triangles that will land there, which needs a guess of the screen position before the transform, for example from the last frame. The 1994 paper notes that no sort-first system had been built.
- **Sort-middle.** Between geometry and rasterization, on screen-space triangles, whose position is known exactly. This page.
- **Sort-last.** After rasterization. Each unit draws its triangles to a full screen, and the fragments or whole images are then merged by depth with [image compositing](/image-compositing/). The paper splits it into sort-last-sparse, which sends only the fragments that were drawn, and sort-last-full, which sends whole images, as in PixelFlow.

**The sort.** Each geometry unit computes, for each of its screen-space triangles, the regions that its bounding box meets, and appends the triangle to the queue of each such region. This is a [bucket sort](/bucket-sort/) by region with one key per overlapped region. The regions are the tiles of [tiled rasterization](/tiled-rasterization/), and a rasterizer owns one region or several.

**The overlap factor.** Let a region be $W \times H$ pixels and a triangle have a bounding box of $w \times h$, at a uniformly random offset. The box meets $1 + w/W$ columns of regions in expectation, because the region borders are a lattice with spacing $W$ and an interval of length $w$ at a random offset holds $w/W$ of them on average. The offsets in $x$ and $y$ are independent, so the mean number of regions per triangle is

$$O = \frac{W + w}{W} \cdot \frac{H + h}{H} ,$$

the formula that Molnar et al. credit to John Eyles.

**The costs.** With $n_d$ screen-space triangles and the overlap factor $O_d$, Molnar et al. count $n_d O_d$ for sorting into regions, $n_d O_d$ for the redistribution, and $n_d (O_d - 1)$ for the extra setup of triangles that more than one rasterizer must set up. Two effects limit sort-middle:

- **Communication.** The traffic between the stages grows with the number of triangles, so a scene with a high tessellation ratio (many small triangles per pixel) sends much more data than its pixels need.
- **Load imbalance.** The rasterizer work follows the screen position of the triangles. When the triangles clump in a few regions, those rasterizers set the speed and the others wait. Smaller regions, many per rasterizer and interleaved over the screen, spread a clump, but they raise $O$: this is the trade-off between [load balance](/load-balancing-problem/) and overlap.

**Order.** Each region sees the triangles from several geometry units. For blending and for ties in the depth test, the triangles of a region must be drawn in the order of the input, so the queues carry sequence numbers and the rasterizer merges them in order.

## Examples

**Overlap factors.** For square regions of side $W$ and square boxes of side $w$, the formula gives the values below. A Monte Carlo run with 200000 boxes at random offsets per row, with `random.Random(7)`, gives the last column.

| region $W$ | box $w$ | $O = ((W + w)/W)^2$ | Monte Carlo |
| --- | --- | --- | --- |
| 16 | 10 | $2.6406$ | $2.6441$ |
| 32 | 10 | $1.7227$ | $1.7236$ |
| 64 | 10 | $1.3369$ | $1.3337$ |
| 32 | 1 | $1.0635$ | $1.0635$ |
| 32 | 32 | $4.0000$ | $4.0000$ |
| 32 | 100 | $17.0156$ | $17.0121$ |

With $32 \times 32$ regions and $10 \times 10$ boxes, each triangle goes to $1.72$ rasterizers on average, so the sort sends $72\%$ more triangles than the input has, and the extra setup is $0.72$ per triangle. With regions of 16, smaller for better balance, the factor is $2.64$. A box of the size of a region always meets 4 regions. For boxes of whole pixels at integer offsets, the count is $(W + w - 1)/W$ per axis, so $(41/32)^2 = 1.6416$ for the case of 32 and 10.

**Imbalance.** A $512 \times 512$ screen is split into 16 regions of $128 \times 128$, one per rasterizer. If the scene is a small object that covers one region, one rasterizer does nearly all the pixel work, and 16 rasterizers are barely faster than one. Interleaving $32 \times 32$ tiles over the 16 rasterizers spreads the object over all of them, at the cost of an overlap factor that is about $(1 + w/32)^2$ instead of $(1 + w/128)^2$.

**Tile-based GPUs.** A mobile GPU that sorts the triangles of a frame into tile lists and then renders the tiles one after the other, each in on-chip memory, is sort-middle in time: the sort is the same, and the tiles take turns on the same rasterizer instead of running on separate ones.

## Where it is used

- Parallel graphics hardware: the 1994 paper lists Pixel-Planes 5, the Silicon Graphics RealityEngine and the Sun Leo as sort-middle machines.
- Tile-based GPUs in phones and tablets, where rendering a tile in on-chip memory saves the traffic to the frame buffer in DRAM.
- Desktop GPUs, which split the screen among several rasterizer units by interleaved tiles after the geometry stage.
- Software rasterizers on many cores, which sort the triangles into tile queues and give whole tiles to threads, so that no two threads write the same pixel; the time is a [work and span](/work-span-model/) question with the sort as the step between the two parallel phases.

## References
