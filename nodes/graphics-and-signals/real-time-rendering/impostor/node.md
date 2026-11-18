---
tag: K855WY
kind: technique
slug: impostor
name: Impostor
aliases:
- image impostor
area: graphics-and-signals/real-time-rendering
level: core
summary: Replace a distant complex object by an image of it rendered to a texture and drawn on a quad, refreshed when the view changes enough.
prereqs: [billboard, level-of-detail, texture-mapping]
see_also: [alpha-blending, mipmap, z-buffer, cube-map, occlusion-culling, geomorphing, texture-clipmap]
sources:
  - paper: doi:10.1145/199404.199420
    title: Paulo W. C. Maciel and Peter Shirley, Visual navigation of large environments using textured clusters, Proceedings of the 1995 Symposium on Interactive 3D Graphics (I3D 95), from page 95
    locator: the impostors of objects and clusters of objects, including texture-mapped ones, and the choice among them per frame (general locator)
  - paper: "Gernot Schaufler, Dynamically Generated Impostors, GI Workshop MVD'95, Infix, November 1995"
    locator: the impostors rendered at run time into a texture, and the error test that decides when an impostor must be rendered again (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 13 (beyond polygons), the parts on billboards and impostors (general locator)
---

An impostor shows a complex object by an image of it: the renderer draws the object once into a texture, from the current view, and then draws that texture on a single quad for as long as the view has not changed too much. A [billboard](/billboard/) uses a fixed texture made in advance; an impostor makes its texture at run time from the real object and refreshes it, so it can stand in for any object at its current angle and lighting. Against a simpler mesh from [level of detail](/level-of-detail/), it costs the same few triangles for any object, but it is right only near the view it was made from.

## In plain words

A far house takes many triangles to draw, but from far away it looks like a flat picture. So take a photo of it from where you stand, stick the photo on a sheet, and put the sheet where the house is. Each frame, draw the sheet in place of the house.

As you walk, the house should look a little different, because you see it from a new side. While the change is too small to see, keep the photo. When it would show, take a new photo.

The photo is cheap to draw and the house is expensive, so if one photo serves many frames, the scene draws much faster.

## When it applies

- The object is far from the viewer, or the view of it changes slowly, so that one image is good for many frames.
- The object costs much more to draw than a textured quad: many triangles, many small parts, or a complex shader.
- The object does not need correct depth against things very close to it, because the quad is flat.
- There is time and texture memory to render the images: one texture per impostor, of about the size of the object on the screen.

## The template

The holes are the *error test* $E$, which says whether the current image is still good for the eye $e$, the *placement* $Q$ of the quad, and the *resolution* $R$ of the texture.

```pseudo id=main
IMPOSTOR(object, e)                              ▷ holes: E, Q, R
L1  if the object has no image or E(image, e) is true then
L2      quad ← Q(object, e)                          ▷ a plane through the object center, facing e, that covers its projected bounds
L3      render the object alone into a texture of R x R texels, from e through the quad, with a transparent background
L4      image ← (texture, quad, e, the light state)  ▷ keep the view of this render for the test of line L1
L5  draw the quad with the texture, with the depth test and an alpha test or a blend
```

The steps of the method are:

1. Choose the objects that get impostors, often from a distance threshold or a cost test, as for [level of detail](/level-of-detail/).
2. For each such object, run line L1 each frame. A common error test compares the angle between the directions from the object center to $e$ and to the eye of the image with a threshold, and also checks the change of distance and of the lights.
3. When the test says so, place the quad by line L2, set a camera at $e$ with a view frustum through the quad, and render the object into the texture by line L3.
4. Store the image with the eye and the time of the render by line L4.
5. Draw the quad by line L5 in place of the object. Spread the renders of line L3 over several frames when many impostors need them at once.

**A walk-through.** The image is $W = 1920$ pixels wide with a horizontal field of view of $60°$, which gives $1920 / (2 \tan 30°) = 1662.8$ pixels per unit at the distance 1. An object with a bounding radius of 1 is at the distance $d = 20$.

- *Resolution.* The object covers about $2 \cdot 1662.8 / 20 = 166.3$ pixels across, so line L3 can use a $256 \times 256$ texture, 128 texels per unit. The texture is magnified on the screen only when the eye comes closer than $1662.8 / 128 = 12.99$.
- *Parallax.* The eye moves 0.5 to the side, so the direction to the object turns by $\arctan(0.5 / 20) = 1.432°$. A point of the object 1 unit in front of or behind the quad then moves on the quad by $1 \cdot \tan(1.432°) = 0.025$ units, which is $0.025 \cdot 1662.8 / 20 = 2.08$ pixels. The flat image does not show this shift, so it is the error of the impostor.
- *The test.* For an error of at most 1 pixel, the direction may turn by at most $\arctan(20 / 1662.8) = 0.689°$, a move of 0.241 units to the side. At 0.025 units per frame, one image serves 9 frames. The 1 pixel limit is a tuning, not a value from a source.

## Classic examples

**Distant objects in a walkthrough.** Maciel and Shirley (1995) replaced objects and clusters of objects in large scenes by cheaper representations, among them textured ones, and chose among them per frame to keep the frame rate. Schaufler (1995) rendered the images at run time and reused them while an error test allowed. This is the core form of the technique, a step past [level of detail](/level-of-detail/) meshes.

**Image caches for scenery.** Hierarchical image caches render whole regions of a scene, such as the far part of a city or a landscape, into textures on quads and reuse them over many frames, refreshing the near regions more often than the far ones.

**Precomputed view sets.** In place of a render at run time, a set of images of the object from many directions on a sphere or a hemisphere is made in advance, and line L3 becomes a choice, or a blend, of the nearest images. This is common for distant trees and rocks in games; it is a [billboard](/billboard/) with a texture per direction, like a [cube map](/cube-map/) of views.

**Clouds and smoke volumes.** A volume that is expensive to march is rendered into an impostor texture at a lower rate than the frame rate and composited with [alpha blending](/alpha-blending/).

**Portals.** The view through a door or a window into a far room can be rendered into a texture and drawn on the opening while the viewer is far from it, which joins impostors with [occlusion culling](/occlusion-culling/).

## Variations

- **Depth impostors.** Store a depth per texel with the color, so that the quad writes better depths into the [z-buffer](/z-buffer/) and objects near the impostor are hidden in the right places.
- **Layered impostors.** Several quads at different depths, each with a slice of the object, show some parallax and reduce the error of line L1.
- **Lighting in the image.** Render normals and material values in place of the final color, and shade the quad each frame, so that a moving light does not force a new render.
- **Budgets.** Rank the impostors by their error, and render only as many in one frame as the time budget allows; the rest keep their old images for a frame longer.
- **Blending between images.** When an impostor is refreshed, fade from the old image to the new one over a few frames, as a [geomorph](/geomorphing/) does for vertices, so that the refresh does not pop.

## Pitfalls

- **A test on the angle only.** If line L1 checks only the change of direction, an eye that walks straight toward the object never refreshes it, and the texture of line L3 is magnified and blurs. Test the distance as well.
- **A background that is not transparent.** If line L3 clears the texture to an opaque color, or keeps colors that are not premultiplied by alpha, the filtered edges of the quad show a dark or colored rim.
- **A quad that cuts the scene.** The flat quad of line L2 has one depth for the whole object. A character that walks into the space of a far building passes in front of the whole building or behind it at once, and a quad that meets the ground cuts it on a straight line.
- **A stale light.** If line L4 does not keep the light state and line L1 does not test it, a light that moves leaves the impostor lit from the old direction.
- **All renders in one frame.** If line L1 says true for many impostors at once, for example after a jump of the camera, the renders of line L3 make one frame much slower. Spread them over frames with a budget.
- **A texture size from the object, not the screen.** If $R$ in line L3 comes from the size of the object in the world, near impostors are blurry and far ones waste memory; take it from the projected size, as in the walk-through.

## Exercises

1. In the walk-through, the object moves to the distance 40. How many pixels does it cover, what texture size is enough, and how far may the eye move to the side before the error reaches 1 pixel?
2. Show that for a small turn $\theta$ of the direction to the object, the error of a point at depth $z$ from the quad is about $z \theta / d$ radians on the screen. What does this say about the refresh rate of near impostors against far ones?
3. An eye walks straight toward an impostor at the speed $v$. Write a test for line L1 that refreshes the image when the texture would be magnified, using the texels per unit of the image and the pixels per unit at the current distance.
4. A forest of 10,000 trees uses impostors, and the budget allows 50 renders of line L3 per frame. If every impostor must be refreshed after a turn of $1°$, how fast may the camera circle the forest center so that the budget is enough, for trees at the distance 100 and for trees at the distance 1000?
5. Compare an impostor with a precomputed set of 64 views on a hemisphere. What is the largest angle between the eye direction and the nearest view, roughly, and which of the two uses more memory for 10,000 identical trees?

## References
