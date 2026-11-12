---
tag: SFJYM4
kind: concept
slug: occlusion-query
name: Occlusion query
aliases:
- hardware occlusion query
area: graphics-and-signals/visibility
level: advanced
summary: A GPU counter of the samples that pass the depth test while some geometry is drawn. A count of 0 for a bounding box proves the object inside it hidden.
prereqs: [z-buffer, bounding-volume]
see_also: [occlusion-culling, hierarchical-z-buffer, early-depth-test, any-hit-query, depth-peeling, visibility-coherence, axis-aligned-bounding-box, stencil-buffer]
sources:
  - url: https://registry.khronos.org/OpenGL/extensions/ARB/ARB_occlusion_query.txt
    title: The Khronos Group, ARB_occlusion_query, OpenGL extension specification
    locator: the overview and the issues (the counter of samples that pass the depth and stencil tests, the query objects, the result-available flag for polling, and the relation to HP_occlusion_test and NV_occlusion_query)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 19.7 (occlusion culling) and Section 19.7.1 (occlusion queries, their latency, and their use with a hierarchy)
  - paper: "Jiří Bittner, Michael Wimmer, Harald Piringer and Werner Purgathofer, Coherent Hierarchical Culling: Hardware Occlusion Queries Made Useful, Computer Graphics Forum 23(3), Eurographics 2004"
    locator: the whole paper (the use of the results of the previous frame and the interleaving of queries with rendering)
---

An *occlusion query* is a counter on the GPU. The program starts it, draws some geometry, and stops it; the counter then holds the number of samples of that geometry that passed the depth test (and the stencil test) of the [z-buffer](/z-buffer/). Its main use is [occlusion culling](/occlusion-culling/): draw the [bounding volume](/bounding-volume/) of an object, with color and depth writes off, and skip the object if the count is 0. It is a counter of rasterized samples against the current depth buffer, not a query on a ray: the [any-hit query](/any-hit-query/) of ray tracing, which tests whether a ray segment meets any surface, is also called an occlusion query in that field, and it is a different operation.

## In plain words

Before you draw a complex object, such as a car with many parts, you want to know if anything of it can be seen. Its box is simple to draw. So you draw the box, but you do not let it change the picture. You only ask the graphics card: how many dots of this box would have been in front of what is already drawn?

If the answer is 0, the whole box is behind other things, so the car in it is too. You do not draw the car. If the answer is more than 0, some part of the box can be seen, and you draw the car.

The answer takes some time to come back from the card, so programs often use the answer of the last picture.

## The idea

**What is counted.** Between the begin and the end of a query, each sample of each fragment that passes the depth and stencil tests adds 1 to the counter. With one sample per pixel this is a number of pixels; with [multisample antialiasing](/multisample-antialiasing/) it is a number of samples. The count is exact for the geometry that was drawn and the depth buffer at that moment: it does not depend on whether color or depth is written.

**Culling with a proxy.** Let $B$ be a closed box that contains the object $O$, with the eye outside $B$ and both front and back faces of $B$ drawn, and let the depth buffer hold the occluders drawn so far. If no sample of $B$ passes the depth test, then no sample of $O$ does either: a sample of $O$ that passes is a point $q$ of $O$ at a pixel center with a depth less than the stored depth, and the ray from the eye to $q$ meets the surface of $B$ at a point that is not farther than $q$, at the same pixel center. So a count of 0 for $B$ proves that $O$ adds nothing to the image. The test is conservative: a positive count does not mean that $O$ is visible, only that its box is.

**Boolean and counting forms.** The first hardware form, HP_occlusion_test, returned only whether any sample passed. NV_occlusion_query and then ARB_occlusion_query returned the count, and let many queries be in flight at once. Later OpenGL added a boolean target (any samples passed), which can stop counting at the first sample.

**Latency.** The GPU runs behind the CPU, often by a frame or more. A program that waits for the result of each query stalls the pipeline. The ARB extension has a flag that tells whether a result is available, so a program can poll and do other work. Common uses are:

- *Results from the last frame.* Use the result of frame $t - 1$ to decide what to draw in frame $t$, and issue new queries for the next frame. Objects change visibility rarely, which is [visibility coherence](/visibility-coherence/). An object that becomes visible is drawn one frame late, which can show as a brief gap.
- *Hierarchies.* Query the nodes of a bounding volume hierarchy or of an octree, and descend only into the visible ones. Coherent hierarchical culling (Bittner, Wimmer, Piringer and Purgathofer, 2004) skips the queries of nodes that were visible in the last frame and interleaves the other queries with rendering, to hide the latency.
- *Conditional rendering.* The GPU can skip a draw call by itself when a given query counted 0, with no round trip to the CPU.

## Examples

**A box behind a wall.** On an $8 \times 8$ screen with one sample per pixel, a wall at depth 1 covers the columns 0 to 5. A box at depth 5 covers the columns 4 to 7 in the rows 2 to 5, 16 pixels. The query over the box counts the box pixels that are not behind the wall: the columns 6 and 7 in four rows, which is 8. The object is drawn. If the wall covers all 8 columns, the count is 0, and the object is skipped, whatever its number of triangles.

**The fraction visible.** For a light source drawn as a small disk, the count divided by the number of samples of the disk drawn with no depth test is the fraction of it that is visible. Games use this to fade lens flares and glare.

**The stop test of depth peeling.** [Depth peeling](/depth-peeling/) stops when a pass writes no pixel. An occlusion query over the pass gives this count without a read of the image.

**A test that fails to cull.** A box that lies across the near plane of the camera is clipped, and part of it may not be drawn at all; if the camera is inside the box, no face of it may pass, and a count of 0 would cull a visible object. Programs treat a box that contains the camera, or meets the near plane, as visible without a query.

## Where it is used

Occlusion queries are used for occlusion culling in games and in viewers of large models, together with [frustum culling](/frustum-culling/) and a spatial hierarchy, to skip hidden objects in scenes such as cities and buildings. They also measure the depth complexity of a scene, the visible area of an object for the choice of a level of detail, and the visible part of a light. GPU-driven renderers often replace them with a [hierarchical z-buffer](/hierarchical-z-buffer/) test in a compute shader, which needs no query objects and no round trip.

## References
