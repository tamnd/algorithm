---
tag: YZPSJD
kind: technique
slug: virtual-texturing
name: Virtual texturing
aliases:
- sparse virtual texturing
- megatexture
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Page fixed-size tiles of a huge texture into a physical cache on demand, using a feedback pass and an indirection table, like virtual memory.
prereqs: [mipmap, texture-mapping]
see_also: [texture-clipmap, mipmap, demand-paging, lru-cache, working-set-model, paging-problem, quadtree, s3-texture-compression]
sources:
  - paper: "Christopher C. Tanner, Christopher J. Migdal and Michael T. Jones, The clipmap: a virtual mipmap, SIGGRAPH 98, pages 151 to 158"
    title: Tanner, Migdal and Jones, The clipmap, a virtual mipmap, SIGGRAPH 1998
    locator: the whole paper (a fixed-size region of each mip level around a center, updated as the center moves)
  - paper: "Sean Barrett, Sparse virtual textures, Game Developers Conference, 2008"
    title: Sean Barrett, Sparse virtual textures, GDC 2008
    locator: pages of the mip pyramid, a page table texture and a feedback pass (general locator)
  - paper: "J. M. P. van Waveren, id Tech 5 challenges: from texture virtualization to massive parallelization, course Beyond Programmable Shading, SIGGRAPH 2009"
    title: J. M. P. van Waveren, id Tech 5 challenges, SIGGRAPH 2009 course
    locator: texture virtualization in a shipped engine, with feedback, streaming and transcoding of pages (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 19, Acceleration Algorithms, the material on texture streaming and virtual texturing (general locator)
---

Virtual texturing treats a texture that is far too large for video memory as a virtual address space. Each level of its [mip pyramid](/mipmap/) is cut into pages of a fixed size, such as $128 \times 128$ texels. Only the pages that the current view needs live in a physical cache texture, and an indirection table maps each virtual page to its slot in the cache. A feedback pass finds the needed pages, and missing pages load in the background, as in [demand paging](/demand-paging/) of virtual memory. A plain mipmap keeps every level of the texture in memory. A [texture clipmap](/texture-clipmap/) keeps a fixed-size square of each level around one center point, which suits a terrain seen from one place. Virtual texturing keeps any set of pages, chosen by what the pixels actually sample, so it works for a whole world with unique texture on every surface.

## In plain words

Think of a huge map book with thousands of pages, and a small desk that holds only a few of them. You only need the pages for the part of the world you look at now, and a less detailed overview page for things far away.

Virtual texturing does this with a giant texture. It cuts the picture, and each smaller copy of it, into equal square tiles. A small table says, for each tile, where on the desk it lies, if it is there at all. Each frame, the renderer asks which tiles the screen used. Tiles that are missing load from disk, and tiles that nobody used for a while leave the desk. While a tile loads, the blurrier copy of that area stands in for it.

## When it applies

- The texture data of a scene is much larger than video memory: unique texture over a whole world, large terrain imagery, many detailed decals baked into one texture.
- The view at any moment sees a small part of the data at a fine level. The working set of pages fits in the cache.
- The data can stream from disk or from a fast decompressor fast enough to follow the camera, and a short blur while a page loads is acceptable.
- The shader can afford one dependent texture read for the indirection, and the engine can afford a feedback pass and a readback.
- It does not pay for small scenes whose textures fit in memory. Plain mipmapped textures are simpler and filter better then.

## The template

The inputs are a virtual texture of $2^L \times 2^L$ texels with its mip levels, a page size $P$ with a border of $b$ texels, and a physical cache of $S \times S$ slots.

1. Offline, cut every mip level into pages of $P \times P$ texels. Copy a border of $b$ texels from the neighbors around each page, so that [bilinear filtering](/bilinear-filtering/) inside a slot gives the same result as in the full texture. Compress the pages, for example with [block compression](/s3-texture-compression/), and store them on disk.
2. Feedback. Render the scene at a low resolution, and write for each pixel the page it needs: the page coordinates and the mip level, computed from the texture coordinate and its derivatives.
3. Read the feedback buffer back to the CPU, or reduce it on the GPU, and collect the set of distinct page requests, for example with a [hash table](/hash-table/).
4. For each requested page that is not in the cache, queue a load. The coarsest levels are always resident, so every request has a resident ancestor in the [quadtree](/quadtree/) of pages.
5. When a load ends, place the page in a free slot. If no slot is free, evict a page that was not requested in this frame, chosen by [least recently used](/lru-cache/) order.
6. Update the indirection table. For each virtual page at each level, store the slot and the level of the finest resident page that covers it, which is the page itself or an ancestor.
7. In the shading pass, read the indirection entry for the texture coordinate, compute the address of the texel in the cache from the slot and the offset inside the page, and sample the cache.

Step 4 makes every lookup valid: the indirection entry always points to a resident page that covers the texel, at the level requested or a coarser one. This is a proved property of the fallback to the ancestor. The address of step 7 is exact arithmetic, a law of the layout. The eviction order is a heuristic. The best order needs the future requests, as in [Belady's algorithm](/belady-algorithm/), and LRU only imitates it. The page size, the border, the feedback resolution and the number of loads per frame are tuning.

## Classic examples

**Sizes.** Take $2^{17} = 131072$ texels on a side, pages of $P = 128$ texels, and 4 bytes per texel. Level 0 has $1024 \times 1024 = 1048576$ pages, and all levels together have $\sum_{k=0}^{10} 4^k = 1398101$ pages. Level 0 alone holds 64 GiB, or 8 GiB with 4 bits per texel compression. A cache of $4096 \times 4096$ texels holds 64 MiB and $32 \times 32 = 1024$ pages. A screen of $1920 \times 1080$ pixels at about one texel per pixel needs $2073600 / 16384 \approx 127$ full pages. That is a lower bound, and partly covered pages, two mip levels at once and the borders raise the real count. The cache size is then set by measurement.

**An address trace.** Without borders, a texel at $(38500, 91700)$ on level 0 is in page $(300, 716)$, at the offset $(100, 52)$ inside the page. If that page is in slot $(5, 17)$, the cache texel is $(5 \cdot 128 + 100, 17 \cdot 128 + 52) = (740, 2228)$. If it is not loaded, but its parent on level 1 is in slot $(9, 2)$, the same point is texel $(19250, 45850)$ on level 1, in page $(150, 358)$ at the offset $(50, 26)$, and the cache texel is $(9 \cdot 128 + 50, 2 \cdot 128 + 26) = (1202, 282)$.

**Unique texturing of a game world.** id Tech 5 textured whole levels with one very large virtual texture, so that artists could paint every surface without repeated tiles. Pages streamed from disk and were transcoded to a GPU format at load time.

**Terrain.** Satellite imagery and baked terrain materials cover many kilometers at a fine resolution. Virtual texturing streams the pages near the camera, which a [texture clipmap](/texture-clipmap/) also does for one center, often together with [geometry clipmaps](/geometry-clipmaps/) for the heights.

## Variations

- **Clipmaps.** The [texture clipmap](/texture-clipmap/) of Tanner, Migdal and Jones (1998) keeps a fixed region of each level around a center and updates it as the center moves. It needs no feedback and no indirection, but it serves only one area of interest.
- **Procedural virtual texturing.** Pages are rendered on the GPU when they are requested, by blending materials and decals, in place of loading them from disk.
- **Hardware sparse textures.** Modern graphics APIs let the application map and unmap pages of a texture in memory and ask whether a texel is resident. The hardware does the indirection, and the engine still chooses the pages.
- **Feedback without a pass.** Write the page requests from the main shading pass, for a small random subset of the pixels, in place of a separate low-resolution pass.
- **Several virtual textures.** Albedo, normals and other material channels share one indirection table, with one cache texture per channel.

## Pitfalls

- **Filtering across page borders.** Bilinear and [anisotropic filtering](/anisotropic-filtering/) read neighbors of the texel, and in the cache those neighbors belong to another page. Borders of $b$ texels fix this for footprints up to $b$ texels. Wider anisotropic footprints still bleed.
- **Derivatives and mip selection.** The cache address jumps at page edges, so derivatives of the cache address are wrong there. Compute the level and the derivatives from the virtual coordinate, and sample with explicit gradients.
- **Trilinear filtering.** Blending two levels needs both pages. Without both, use one level, or do two lookups.
- **Latency and blur.** A page needs some frames to load. After a fast turn of the camera, surfaces are blurry for a moment and then sharpen. Load coarse pages first, and predict the camera motion.
- **Thrashing.** If the [working set](/working-set-model/) of pages is larger than the cache, pages evict each other every frame. Lower the resolution of the requests by one level when the cache overflows.
- **Missed pages.** A low-resolution feedback pass can miss small or thin objects, which then stay blurry. Jitter the feedback pixels over the frames.
- **Indirection precision.** The table needs enough bits for the slot, the level and the fraction of the coordinate. For $2^{17}$ texels, 32-bit floats for the texture coordinate are close to their limit.

## Exercises

1. Show that the levels $0$ to $L - p$ of a $2^L \times 2^L$ texture with pages of $2^p$ texels hold $(4^{L - p + 1} - 1)/3$ pages, and compare this with the pages of level 0.
2. Write the address computation of step 7 with a border of $b$ texels, so that the payload of a page is $P - 2b$ texels.
3. Show that after step 6 every indirection entry points to a resident page that covers the entry.
4. A camera turns by 90 degrees in half a second, and the disk delivers 200 pages per second. How long does it take to replace a working set of 400 pages, and what does the player see?
5. Compare the memory of a virtual texture cache of 1024 pages with the memory of a texture clipmap of the same texture with a clip size of 2048.

## References
