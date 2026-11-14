---
tag: 7KPYDY
kind: technique
slug: draft-angle-analysis
name: Draft angle analysis
aliases:
- draft analysis
area: cad/manufacturing-process-planning
level: intro
summary: Colours each face of a part by the angle between its normal and the pull direction, so faces with too little draft for release from the mold are found.
prereqs: [mold-parting-direction]
see_also: [undercut-detection, parting-line-generation, silhouette-curve-of-a-surface, isophote, manufacturability-analysis]
sources:
  - paper: doi:10.1016/S0010-4485(01)00117-8
    title: M. W. Fu, A. Y. C. Nee and J. Y. H. Fuh, The application of surface visibility and moldability to parting line generation, Computer-Aided Design 34(6), 2002, 469 to 480
    locator: the classification of the faces of a molded part by their orientation to the parting direction, with the faces parallel to it as a separate class
---

Draft angle analysis measures, for each face or each point of a molded or cast part, the angle between the surface and the pull direction $d$ of the mold, and marks the places where this angle is too small for the part to slide out. A wall that is exactly parallel to $d$ rubs along the mold over its whole height when the mold opens, so walls get a small taper, the draft. The analysis is one formula per normal, $\alpha = \arcsin\bigl(n \cdot d / (\lvert n \rvert \lvert d \rvert)\bigr)$, and a test of $\lvert\alpha\rvert$ against a minimum $\alpha_{\min}$. It assumes that the direction is fixed and that the face is not an undercut. The tests for those are [mold parting direction](/mold-parting-direction/) and [undercut detection](/undercut-detection/).

## In plain words

When a molded part comes out of its mold, its side walls slide along the mold. If a wall is exactly straight up and down, it scrapes along the whole way and may stick. So designers tilt walls a little, so that they come free as soon as the mold starts to move.

The analysis looks at every face and asks how much it is tilted from the direction in which the mold opens. Faces with enough tilt get one colour, and faces with too little tilt get another, so the designer can fix them.

## When it applies

- The part is made in a mold or die that opens by a straight pull along a known direction $d$: injection molding, die casting, sand casting with a pattern, forging.
- The face is formed by one half of the mold and is not an undercut. An undercut face cannot come free at any draft.
- There is a minimum draft $\alpha_{\min} > 0$ for the material, the surface texture and the depth of the wall. It is a design rule from the material supplier or a design handbook, not a value that geometry gives.

## The template

**The draft angle.** Let $n$ be a normal of the surface at a point, pointing out of the part. The *draft angle* $\alpha \in [-90^\circ, 90^\circ]$ is the angle between the tangent plane and the direction $d$, with a sign:

$$\sin \alpha = \frac{n \cdot d}{\lvert n \rvert \, \lvert d \rvert}.$$

*Why.* The angle between a line and a plane is the complement of the angle $\varphi$ between the line and the normal of the plane: the line, its projection onto the plane and the normal lie in one plane, and the projection is perpendicular to the normal. So $\alpha = 90^\circ - \varphi$ and $\sin\alpha = \cos\varphi = n \cdot d / (\lvert n \rvert \lvert d \rvert)$. The sign tells the side: $\alpha > 0$ means the surface faces $+d$ and goes to the half that moves along $+d$; $\alpha < 0$ means it goes to the half that moves along $-d$.

```pseudo id=main
DRAFT-ANALYSIS(faces, d, α_min)
L1  for each face f (or each sample point of a curved face) with outward normal n
L2      α ← arcsin(n · d / (|n| |d|))
L3      if α ≥ α_min then class[f] ← "positive draft, half +d"
L4      else if α ≤ -α_min then class[f] ← "negative draft, half -d"
L5      else class[f] ← "insufficient draft"
L6  return class
```

**An exact test.** Lines L3 and L4 do not need the arcsine. Since $\sin$ is increasing on $[-90^\circ, 90^\circ]$, $\alpha \ge \alpha_{\min}$ holds if and only if $n \cdot d > 0$ and $(n \cdot d)^2 \ge \sin^2(\alpha_{\min}) \, \lvert n \rvert^2 \lvert d \rvert^2$. For integer or rational $n$ and $d$, both sides are exact except the one constant $\sin^2 \alpha_{\min}$, which can be given as a rational bound. This decides faces close to the threshold correctly, where a rounded $\alpha$ can be on the wrong side.

**Cost.** One dot product and one comparison per face or per sample point, so linear in the size of the model.

## Classic examples

Pull direction $d = (0, 0, 1)$ and minimum draft $\alpha_{\min} = 1^\circ$, so $\sin^2 \alpha_{\min} = 0.00030459$.

| normal $n$ | $n \cdot d$ | $\lvert n \rvert^2$ | $\alpha$ | class |
|---|---|---|---|---|
| $(10, 0, 1)$ | 1 | 101 | $5.71^\circ$ | positive draft |
| $(20, 0, 1)$ | 1 | 401 | $2.86^\circ$ | positive draft |
| $(0, 57, -1)$ | $-1$ | 3250 | $-1.005^\circ$ | negative draft |
| $(0, 100, 1)$ | 1 | 10001 | $0.573^\circ$ | insufficient |
| $(1, 0, 0)$ | 0 | 1 | $0^\circ$ | insufficient |

The face $(0, 57, -1)$ is just past the threshold. The exact test compares $(n \cdot d)^2 = 1$ with $0.00030459 \times 3250 = 0.98991$, so it passes. The face $(0, 100, 1)$ gives $0.00030459 \times 10001 = 3.046 > 1$, so it fails. The vertical face $(1, 0, 0)$ has zero draft and is always in the insufficient class.

**What a degree means.** A wall of height $h$ with draft $\alpha$ moves its top edge sideways by $h \tan \alpha$. For $h = 50$ mm and $\alpha = 1^\circ$ this is $0.87$ mm. So the draft changes the size of the part at the top of deep walls, and the designer must allow for it in the tolerances.

## Variations

- **Colour maps on curved surfaces.** CAD systems evaluate $\alpha$ at the points of a tessellation or of the surface and colour the surface by it. The curves $\alpha = \pm\alpha_{\min}$ are [isophotes](/isophote/) of the normal field for the light direction $d$, and the curve $\alpha = 0$ is the [silhouette curve](/silhouette-curve-of-a-surface/) for $d$, where the [parting line](/parting-line-generation/) runs on a smooth part.
- **Three classes or five.** Some tools split each class again, for example into "enough draft", "too little draft" and "vertical", on each side, so that the designer sees both the side and the problem.
- **Adding draft.** The same test drives the repair: a draft feature rotates a wall about a neutral line on it by the missing angle. The test is then run again.
- **Textured surfaces.** A textured wall needs more draft than a smooth one, since the texture locks into the mold. The rule $\alpha_{\min}$ then depends on the face, not only on the part.

## Pitfalls

- **Normals that point in.** A face with the wrong orientation gets the opposite sign and is put on the wrong side. Check the orientation of the model first.
- **Undercuts with good draft.** A face under a lip can have a large positive draft and still be blocked by the lip. Draft analysis does not test that. Run [undercut detection](/undercut-detection/) as well.
- **One normal per face.** A curved face can have enough draft at one end and too little at the other. Test sample points, or bound the normal over the face.
- **Rounding near the threshold.** Comparing a rounded $\alpha$ with $\alpha_{\min}$ can put a face just at the limit on either side. Use the squared test above.

## Exercises

1. Show that rotating a vertical wall by the angle $\beta$ about a horizontal line on it, away from the part, gives it the draft angle $\beta$.
2. For $d = (0, 0, 1)$ and $n = (a, 0, 1)$ with an integer $a > 0$, find the largest $a$ for which the face passes a minimum draft of $1^\circ$. (Answer: $a = 57$, since $1 \ge 0.00030459\,(a^2 + 1)$ holds for $a \le 57$ and fails for $a = 58$.)

## References
