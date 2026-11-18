---
tag: Q8VPTZ
kind: model
slug: gooch-shading
name: Gooch shading
aliases:
- Gooch tone shading
- cool-to-warm shading
area: graphics-and-signals/real-time-rendering
level: core
summary: "A non-photorealistic shading model for technical illustration that varies hue from cool to warm with the surface orientation instead of brightness."
prereqs: [lambertian-reflectance]
see_also: [toon-shading, silhouette-edge, blinn-phong-reflection-model, phong-shading, gouraud-shading, color-spaces, edge-detection, physically-based-shading]
sources:
  - paper: doi:10.1145/280814.280950
    title: Amy Gooch, Bruce Gooch, Peter Shirley and Elaine Cohen, A non-photorealistic lighting model for automatic technical illustration, SIGGRAPH 98, 1998, 447 to 452
    locator: Section 3 (illustration techniques), Section 4.1 (traditional diffuse shading, Equation 1), Section 4.2 (tone-based shading, Equations 2 and 3, Figures 7 and 8), Section 4.3 (metal objects) and Section 4.4 (the approximation with two lights)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 5, Shading Basics (the Gooch model as an example of a shading model, with t = (n·l + 1) / 2) (general locator)
---

Gooch shading is a lighting model for technical illustration, published by Amy Gooch, Bruce Gooch, Peter Shirley and Elaine Cohen in 1998. Technical illustrators draw edge lines in black and highlights in white, so the shading between them must stay in the middle tones. [Lambertian](/lambertian-reflectance/) shading cannot do this: half of a lit object goes to black, where the black [silhouettes](/silhouette-edge/) disappear. Gooch shading keeps the brightness in a narrow range and shows the orientation of the surface by a change of hue instead, from a cool color (blue) on the side away from the light to a warm color (yellow) on the side toward it. The object color is mixed into both ends, so a red part still looks red. In the form of Real-Time Rendering, with $t = (n \cdot l + 1) / 2$,

$$I = t\, k_{\text{warm}} + (1 - t)\, k_{\text{cool}}, \qquad k_{\text{cool}} = (0, 0, b) + \alpha k_d, \quad k_{\text{warm}} = (y, y, 0) + \beta k_d.$$

## The machine

**Quantities.** $n$ is the unit surface normal, $l$ the unit vector toward the light and $k_d$ the RGB diffuse color of the object, with channels in $[0, 1]$. $I$ is an RGB display color, not a radiance.

**Parameters.** $b \in [0, 1]$ is the strength of the blue, $y \in [0, 1]$ the strength of the yellow, and $\alpha$ and $\beta$ the parts of the object color in the cool and the warm end. The paper shows Figure 7 with $b = 0.4$, $y = 0.4$, $\alpha = 0.2$, $\beta = 0.6$, and Figure 8 with $b = 0.55$, $y = 0.3$, $\alpha = 0.25$, $\beta = 0.5$, to show that the exact values are not crucial. All four are visual tuning.

**Equation 1, the reference.** Traditional diffuse shading is $I = k_d k_a + k_d \max(0, l \cdot n)$ with an ambient color $k_a$. With $k_a = 0$, every point with $l \cdot n \le 0$ is black.

**Equation 2, the blend.** The paper blends two colors with the full range of $l \cdot n \in [-1, 1]$, so the side away from the light also changes color. As printed, Equation 2 is

$$I = \frac{1 + l \cdot n}{2} k_{\text{cool}} + \Big(1 - \frac{1 + l \cdot n}{2}\Big) k_{\text{warm}},$$

which gives $k_{\text{cool}}$ where the surface faces the light. The text of the paper and the two-light form of Section 4.4 put the warm color toward the light. This page uses the form of Real-Time Rendering above, with $k_{\text{warm}}$ at $t = 1$.

**Equation 3, the two ends.** $k_{\text{cool}} = k_{\text{blue}} + \alpha k_d$ and $k_{\text{warm}} = k_{\text{yellow}} + \beta k_d$, with $k_{\text{blue}} = (0, 0, b)$ and $k_{\text{yellow}} = (y, y, 0)$. A blue-to-yellow blend alone gives a strong sense of shape but colors unrelated to the object; a black-to-object-color blend alone is close to diffuse shading. The sum is a compromise between the two.

**Assumptions.** One light, placed so that $l$ is perpendicular to the gaze direction, which shows the full range of $l \cdot n$. The paper puts it up and to the right and keeps it fixed. No shadows. Edge lines are drawn in black and highlights use the Phong term $(r \cdot v)^p$ in white.

**Metal (Section 4.3).** For a metal part the paper maps twenty stripes of random intensity between 0 and 0.5 along the axis of largest curvature, makes the stripe nearest the light white and interpolates linearly between the stripe centers. This imitates the banded look that illustrators use for milled metal.

## What it counts

$I$ is the color to display at a point, as a function of the angle between the normal and the light. It is not a reflectance and has no energy meaning; the model aims at legibility of shape, not at a match with a real material.

**Example.** A pure red object, $k_d = (1, 0, 0)$, with the constants of Figure 7:

| $n \cdot l$ | $t$ | Gooch $I$ | Lambert $k_d \max(0, n \cdot l)$ |
|---|---|---|---|
| -1 | 0 | (0.2, 0, 0.4) | (0, 0, 0) |
| -0.5 | 0.25 | (0.4, 0.1, 0.3) | (0, 0, 0) |
| 0 | 0.5 | (0.6, 0.2, 0.2) | (0, 0, 0) |
| 0.5 | 0.75 | (0.8, 0.3, 0.1) | (0.5, 0, 0) |
| 1 | 1 | (1, 0.4, 0) | (1, 0, 0) |

The Gooch colors go from a red-violet to an orange and are never black, so a black edge line is visible everywhere. The Lambert colors are black on half of the surface.

## Relation to other models

- **[Lambertian reflectance](/lambertian-reflectance/).** With $k_{\text{cool}} = 0$ and $k_{\text{warm}} = k_d$, the blend is $k_d (1 + n \cdot l) / 2$. The paper notes that this looks much like diffuse shading, but it changes over the whole object, also where $n \cdot l < 0$.
- **[Blinn-Phong](/blinn-phong-reflection-model/) and the Phong reflection model.** Gooch shading replaces the diffuse term and keeps a Phong highlight. Section 4.4 builds the diffuse part from two Phong lights so that it runs in graphics packages such as OpenGL.
- **[Toon shading](/toon-shading/).** Another non-photorealistic method. Toon shading quantizes the diffuse term into flat bands; Gooch shading keeps a smooth blend and moves the hue. Both are drawn with black [silhouette edges](/silhouette-edge/).
- **[Physically based shading](/physically-based-shading/).** The opposite goal: Gooch shading gives up any relation to reflected energy to make shape easy to read.

## Known results in the model

- **The sign of Equation 2 (proved).** At $l \cdot n = 1$ the printed Equation 2 gives $k_{\text{cool}}$, and at $l \cdot n = -1$ it gives $k_{\text{warm}}$. The two-light form of Section 4.4 gives the reverse (next item). So the printed equation and the rest of the paper disagree, and the form with $t = (n \cdot l + 1) / 2$ and $k_{\text{warm}}$ at $t = 1$ is the one that matches the text.
- **Two lights give the blend (proved).** Section 4.4 uses a light in direction $l$ with intensity $(k_{\text{warm}} - k_{\text{cool}}) / 2$, a light in direction $-l$ with intensity $(k_{\text{cool}} - k_{\text{warm}}) / 2$, an ambient term $(k_{\text{cool}} + k_{\text{warm}}) / 2$ and a white object. With $x = n \cdot l$, the sum is $(k_{\text{cool}} + k_{\text{warm}}) / 2 + x (k_{\text{warm}} - k_{\text{cool}}) / 2$ for $x \ge 0$ and for $x < 0$, which is exactly $t k_{\text{warm}} + (1 - t) k_{\text{cool}}$. It needs lights with negative colors, and the paper turns off the highlight because the negative blue light gives artifacts.
- **Mid-tones (proved).** Each channel of $I$ lies between the same channel of $k_{\text{cool}}$ and $k_{\text{warm}}$, because $I$ is a convex blend. So if both ends are kept away from black and white, all of the shading is too.
- **Hue as a depth cue (heuristic).** That cool colors recede and warm colors advance, and that hue shifts can carry shape information, come from art practice and the perception literature that the paper cites, and from its own figures. The paper reports no user study.
- **The constants (tuning).** $b$, $y$, $\alpha$, $\beta$ and the light position are chosen by eye.

## References
