---
tag: R2YXYT
kind: concept
slug: level-of-detail
name: Level of detail
aliases:
- LOD
area: graphics-and-signals/real-time-rendering
level: intro
summary: Draw an object with a simpler representation when it covers few pixels, choosing among versions by distance, screen size or error.
prereqs: [graphics-pipeline]
see_also: [mesh-simplification, progressive-mesh, geomorphing, view-dependent-refinement, geometry-clipmaps, mipmap, texture-clipmap, impostor]
sources:
  - paper: doi:10.1145/360349.360354
    title: James H. Clark, Hierarchical geometric models for visible surface algorithms, Communications of the ACM 19(10), 1976, 547 to 554
    locator: the use of simpler versions of an object as it covers less of the screen, inside a hierarchy of objects (general locator)
  - paper: "David Luebke, Martin Reddy, Jonathan D. Cohen, Amitabh Varshney, Benjamin Watson and Robert Huebner, Level of Detail for 3D Graphics, Morgan Kaufmann, 2003"
    locator: the book as a whole (discrete, continuous and view-dependent LOD, the selection criteria and the switching methods) (general locator)
  - paper: doi:10.1145/237170.237216
    title: Hugues Hoppe, Progressive meshes, SIGGRAPH 1996, 99 to 108
    locator: the continuous sequence of meshes by vertex splits, and the geomorphs between them
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: the part on level of detail in the chapter on acceleration algorithms, and Chapter 13 on billboards and impostors (general locator)
---

Level of detail (LOD) is the idea of drawing an object with less detail when less of it can be seen: a far object covers few pixels, so a mesh with fewer triangles, a texture with fewer texels, or a flat image looks the same at a lower cost. A LOD scheme has three parts: a set of representations, a rule that picks one per object and frame, and a way to switch that hides the change. [Mesh simplification](/mesh-simplification/) and [progressive meshes](/progressive-mesh/) build the simpler meshes; this page is about the idea as a whole and how the pages for meshes, terrain, textures and images fit into it.

## In plain words

A tree far away fills a few dots on the screen. Drawing all its leaves wastes time, because nobody can see them.

So keep several versions of the tree: a full one, a simpler one, a very simple one, and maybe only a picture of it. Each frame, estimate how big the tree looks on the screen, and draw the cheapest version that still looks right at that size.

The hard part is the change from one version to the next. If it happens in one frame, the eye sees a jump. Good schemes make the change slowly, or make it so small that it falls inside one screen dot.

## The idea

**The representations.** Detail can drop in five ways, and each has its pages.

- *Discrete meshes.* A few meshes of the same object, made offline by [mesh simplification](/mesh-simplification/), for example with [quadric error metrics](/quadric-error-metrics/). This is the oldest and most common form.
- *Continuous meshes.* A [progressive mesh](/progressive-mesh/) stores a coarse mesh and a list of vertex splits, so any number of triangles between the coarse and the full mesh is available. [View-dependent refinement](/view-dependent-refinement/) refines it more where the viewer looks and is close, and less elsewhere.
- *Terrain.* Terrain is one object that is both near and far. [ROAM](/roam-terrain/) refines a binary tree of triangles to an error bound per frame. [Geometry clipmaps](/geometry-clipmaps/) keep nested regular grids around the viewer, each coarser ring with half the resolution of the ring inside it.
- *Textures.* A [mipmap](/mipmap/) is LOD for a texture: the hardware picks the level from the texel footprint of each pixel. A [texture clipmap](/texture-clipmap/) and [virtual texturing](/virtual-texturing/) keep only the parts of the fine levels that the view needs.
- *Images.* A [billboard](/billboard/) is a textured quad turned toward the camera. An [impostor](/impostor/) is an image of the object, rendered at run time and reused while the view does not change much.

The same idea drives [cascaded shadow maps](/cascaded-shadow-maps/), which give near slices of the view frustum smaller shadow texels.

**The selection.** The usual rule is the *screen-space error*. If a simplified version differs from the full object by at most $\varepsilon$ in world units, and it is at the distance $d$ from a camera whose field of view $\theta$ spans $W$ pixels of the image, then the error covers at most about

$$e = \frac{\varepsilon\, W}{2\, d \tan(\theta/2)}$$

pixels. The renderer picks the coarsest version with $e$ below a threshold, often one pixel or a few. Simpler rules use the distance alone, or the projected size of the bounding sphere. Under a time budget, the renderer picks versions for all objects so that the total cost fits the frame, with the most benefit per triangle. The threshold is a tuning, not a derived constant.

**The switch.** A sudden change of version is a *pop*. Three methods hide it.

- *Hysteresis.* Use two thresholds, one to switch to a coarser version and a lower one to switch back, so that an object near the threshold does not flicker between versions.
- *Blending.* Draw both versions for a short time and fade one out with [alpha blending](/alpha-blending/) or a dither pattern.
- *Morphing.* Move the vertices of the fine version from the positions that they have in the coarse version to their own positions over a few frames: a [geomorph](/geomorphing/). With continuous LOD, each step is small and the morph hides it fully.

**What LOD does not do.** It does not remove objects that are not visible; [frustum culling](/frustum-culling/) and [occlusion culling](/occlusion-culling/) do that, and a renderer uses both. It also changes the image: a LOD scheme trades a bounded error in pixels for speed, and the bound holds only for the error measure that it uses. A silhouette or a specular highlight can change more than the geometric error suggests.

## Examples

**The screen-space error.** A simplified mesh has the error $\varepsilon = 0.01$ m. The image is $W = 1920$ pixels wide with a horizontal field of view $\theta = 60°$, so $W / (2 \tan 30°) = 1662.8$ pixels per unit at distance 1.

| distance $d$ | error $e$ in pixels |
|---|---|
| 10 | 1.663 |
| 16.63 | 1.000 |
| 40 | 0.416 |

With a threshold of 1 pixel, the simplified mesh is used from 16.63 m on. A version with twice the error is used from twice that distance.

**The cost of a LOD chain.** If each version has a quarter of the triangles of the one before it, as when a mesh is simplified to half its resolution in each direction, the chain of all versions has at most $1 + 1/4 + 1/16 + \cdots = 4/3$ times the triangles of the full mesh. A mipmap chain has the same $4/3$ factor for the same reason.

**A mipmap level.** A $1024 \times 1024$ texture covers a square of $256 \times 256$ pixels, seen head on. Each pixel covers 4 texels in each direction, so the hardware uses level $\log_2 4 = 2$, which has $256 \times 256$ texels: one texel per pixel.

## Where it is used

Games and other real-time renderers use discrete mesh LOD for nearly every object, with a few versions per object and a blend or a dither at the switch. Terrain engines and flight simulators use continuous or grid-based terrain LOD, because one terrain spans all distances. Texture streaming uses mipmaps and virtual textures to keep only the texels in view. Large CAD and city models use hierarchies of simplified parts, which is the form that Clark proposed in 1976. Foliage, crowds and distant buildings use billboards and impostors.

## References
