---
tag: NAW8AG
kind: technique
slug: billboard
name: Billboard
aliases:
- billboarding
area: graphics-and-signals/real-time-rendering
level: intro
summary: Draw a textured quad that is rotated each frame to face the camera, used for particles, foliage and distant objects.
prereqs: [texture-mapping, alpha-blending]
see_also: [impostor, particle-system, level-of-detail, z-buffer, cube-map, euler-angles, graphics-pipeline]
sources:
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 13 (beyond polygons), the part on billboarding (screen-aligned, world-oriented and axial billboards, and particles) (general locator)
  - paper: "David Luebke, Martin Reddy, Jonathan D. Cohen, Amitabh Varshney, Benjamin Watson and Robert Huebner, Level of Detail for 3D Graphics, Morgan Kaufmann, 2003"
    locator: the parts on image-based representations of distant objects (general locator)
---

A billboard is a flat quad with a texture that is turned toward the camera each frame, so that a picture of a tree, a puff of smoke or a light glow looks the same from every side. The template has two holes, the rule that gives the facing direction and the rule that gives the up direction, and the common kinds of billboards differ only in these two rules. An [impostor](/impostor/) is a billboard whose texture is rendered from the real object at run time and refreshed when the view changes; a plain billboard uses a fixed texture made in advance.

## In plain words

Cut a picture of a tree out of paper and hold it up in front of a friend. If you turn it so that it always faces them, they see a tree from wherever they stand, though there is only one flat sheet.

A billboard does the same on the screen. Each frame the program turns a small rectangle with a picture on it toward the camera and draws it. It is cheap, because the rectangle has only two triangles.

The rules for the turn decide what it looks like. A puff of smoke can turn in every direction. A tree must stay upright and only turn around its trunk, or it would tip over when the camera looks down at it.

## When it applies

- The object looks about the same from all directions around some axis or point: smoke, fire, sparks, a glow around a light, a distant tree, or a text label.
- It covers few pixels, or it is fuzzy, so the lack of depth and of parallax inside it does not show.
- Many copies are drawn, so the saving over a mesh matters: a [particle system](/particle-system/) with thousands of particles, or a forest.
- The texture has transparent parts, and the renderer can use an alpha test, or [alpha blending](/alpha-blending/) in sorted order.

## The template

The holes are the *normal rule* $N$, which gives the unit vector $n$ that the quad faces, the *up rule* $U$, which gives an approximate up vector, and the *size* $(s_x, s_y)$ of the quad, in world units.

```pseudo id=main
BILLBOARD(p, N, U, s_x, s_y)                       ▷ p is the center of the quad
L1  n ← N(p)                                       ▷ the facing direction, a unit vector
L2  u' ← U(n)                                      ▷ an approximate up, not parallel to n
L3  r ← normalize(u' × n)                          ▷ the right vector
L4  u ← n × r                                      ▷ the exact up, at a right angle to n and r
L5  corners ← p ± (s_x / 2) r ± (s_y / 2) u
L6  draw the quad with its texture, with the depth test, and with an alpha test or a sorted blend
```

The steps of the method are:

1. Choose the kind of billboard, which fixes the rules $N$ and $U$ (see the table below), and the size of the quad.
2. For each billboard, compute $n$ by line L1 and the approximate up $u'$ by line L2.
3. Make an orthonormal frame from them by lines L3 and L4. The vector $r$ is at a right angle to $n$ and $u'$, and $u$ is the part of $u'$ that is at a right angle to $n$, normalized.
4. Place the four corners by line L5. This is often done in the vertex shader, with the center $p$ and a corner index per vertex.
5. Draw by line L6. For blending, sort the billboards from back to front first.

| kind | normal rule $N(p)$ | up rule $U(n)$ |
|---|---|---|
| screen-aligned | minus the view direction of the camera, the same for all billboards | the up vector of the camera |
| viewpoint-oriented | $\mathrm{normalize}(e - p)$, toward the eye $e$ | the world up |
| axial | $e - p$ with its part along the axis $a$ taken out, normalized | the axis $a$, so that $u = a$ |

A screen-aligned billboard lies in a plane parallel to the image, so it shows its texture without any perspective distortion. A viewpoint-oriented one turns toward the eye itself, so a camera that only turns in place does not change it. An axial one turns only around its axis, which keeps a tree upright.

**A walk-through.** The eye is at $e = (0, 2, 0)$, the world up is $(0, 1, 0)$, and a $2 \times 2$ quad has its center at $p = (3, 0, -4)$, at the distance $|e - p| = 5.3852$.

- Viewpoint-oriented: line L1 gives $n = (-3, 2, 4)/5.3852 = (-0.5571, 0.3714, 0.7428)$. Line L3 gives $r = (0.8, 0, 0.6)$, and line L4 gives $u = (0.2228, 0.9285, -0.2971)$. The corners of line L5 are $(1.9772, -0.9285, -4.3029)$, $(3.5772, -0.9285, -3.1029)$, $(4.0228, 0.9285, -3.6971)$ and $(2.4228, 0.9285, -4.8971)$. The quad leans back toward the eye, which is above it.
- Axial, with $a = (0, 1, 0)$: line L1 gives $n = (-0.6, 0, 0.8)$, and $r = (0.8, 0, 0.6)$ as before, with $u = a$. The corners are $(2.2, -1, -4.6)$, $(3.8, -1, -3.4)$, $(3.8, 1, -3.4)$ and $(2.2, 1, -4.6)$. The quad stays upright.

The two normals differ by $\arctan(2/5) = 21.8°$, the angle at which the eye looks down at the center. A tree texture drawn on the first quad would lean back by that angle; on the second it stays vertical, and the viewer sees it a little from above, which the texture does not show.

## Classic examples

**Particles.** A [particle system](/particle-system/) draws each particle of smoke, fire, dust or sparks as a small screen-aligned or viewpoint-oriented billboard, often with [alpha blending](/alpha-blending/) in back to front order, or with an additive blend, which needs no sort. A rotation of the quad around $n$ by a random angle per particle hides the repeated texture.

**Trees and grass.** Distant trees are drawn as axial billboards around the vertical axis, often with two or three crossed quads in place of one so that the tree keeps some volume as the camera moves around it. This is a step of [level of detail](/level-of-detail/): the full mesh near the viewer, then a billboard far away.

**Glows and flares.** The halo around a light, a lens flare or the sun disk is a screen-aligned billboard, drawn with an additive blend and often without the depth test, but with a visibility test of the light.

**Labels and icons.** Text over a character or a map marker is a screen-aligned billboard, often with a size in pixels in place of world units, so that it can be read at any distance.

**Impostors.** An [impostor](/impostor/) renders a complex object into a texture and shows it on a billboard until the view has moved too far, then renders it again.

## Variations

- **Crossed quads.** Two or three quads at fixed angles, with no turning at all, give a tree some volume from all horizontal directions and avoid the visible turn of a single quad.
- **Soft particles.** Fade the alpha of each pixel of a billboard by the difference between its depth and the depth already in the [z-buffer](/z-buffer/), so that the hard line where a smoke quad cuts the ground goes away.
- **Sprites in the hardware.** Point sprites, and quads built in a geometry or vertex shader from one point per billboard, move steps 2 to 4 to the GPU.
- **Normal-mapped billboards.** A normal map on the quad lets the lights shade a billboard as if it had relief, which helps clouds and trees.
- **Views from several directions.** A set of textures rendered from several directions, chosen or blended by the direction to the eye, gives a billboard that changes with the view; this is the step toward [impostors](/impostor/).

## Pitfalls

- **Up parallel to the normal.** For a viewpoint-oriented billboard straight below the eye, the world up of line L2 is parallel to $n$, and line L3 normalizes a zero vector. Choose another up, such as the up of the camera, when $|u' \times n|$ is small.
- **The wrong kind for upright objects.** If line L1 uses the screen-aligned or viewpoint-oriented rule for a tree, the tree tips over when the camera looks down at it, by $21.8°$ in the walk-through. Use the axial rule.
- **Screen-aligned quads that cut each other.** With the screen-aligned rule of line L1, a turn of the camera turns all quads at once. Quads that are close together then cut through each other in new places, and the line where they cross moves. The viewpoint-oriented rule avoids this for a camera that only turns.
- **Blending without a sort.** If line L6 blends the billboards in the order in which they were made, a far quad drawn after a near one is hidden by the depth test, and its transparent edges show the background, not the near particle. Sort from back to front, or use an additive blend or an alpha test.
- **A hard cut at the ground.** With a plain depth test in line L6, a large smoke quad that meets the ground or a wall shows a straight line there. Use soft particles.
- **A size in the wrong space.** If line L5 uses a size in pixels for an object that should get smaller with distance, or a size in world units for a label that must be readable, the billboard has the wrong size on the screen.

## Exercises

1. Show that the vectors $r$ and $u$ of lines L3 and L4 are unit vectors, are at a right angle to each other and to $n$, and that $u$ points to the same side of the plane of $n$ and $r$ as $u'$.
2. For the walk-through, compute the corners of the screen-aligned billboard when the camera looks from $e$ at $p$, with the camera up as close to $(0, 1, 0)$ as possible. Compare them with the viewpoint-oriented corners.
3. A particle system draws 10,000 particles, each a quad of $40 \times 40$ pixels on the screen, with blending. Count the pixels that the blending writes in one frame, and say why large overlapping particles are expensive even though each has only two triangles.
4. Write the axial rule for an axis $a$ that is not vertical, for example for a beam of light along a direction $a$. What happens when the eye lies on the line through $p$ along $a$?
5. A tree is shown as two crossed quads at a right angle, with no turning. From how many horizontal directions does the viewer see a quad exactly edge-on, and how can the texture or a third quad hide this?

## References
