---
tag: K9W6TX
kind: technique
slug: cage-based-deformation
name: Cage-based deformation
aliases:
- cage deformation
area: graphics-and-signals/keyframing-and-deformation
level: core
summary: Enclose a detailed model in a coarse polyhedral cage, bind each point by cage coordinates, and deform the model by moving the cage vertices.
prereqs: [generalized-barycentric-coordinates, barycentric-interpolation]
see_also: [generalized-barycentric-coordinates, floater-mean-value-coordinates, harmonic-coordinates, green-coordinates, free-form-deformation, extended-free-form-deformation, shape-deformation, linear-blend-skinning]
sources:
  - paper: doi:10.1145/1073204.1073229
    title: "Tao Ju, Scott Schaefer and Joe Warren, Mean value coordinates for closed triangular meshes, SIGGRAPH 2005, ACM Transactions on Graphics 24(3), 561-566, 2005"
    locator: the whole paper (mean value coordinates for closed triangle meshes in 3D and their use to deform a model with a cage)
  - paper: doi:10.1016/S0167-8396(03)00002-5
    title: "Michael S. Floater, Mean value coordinates, Computer Aided Geometric Design 20(1), 19-27, 2003"
    locator: the whole paper (the 2D coordinates from the tangents of half angles, the partition of unity and the linear precision)
  - paper: doi:10.1145/1183287.1183295
    title: "Kai Hormann and Michael S. Floater, Mean value coordinates for arbitrary planar polygons, ACM Transactions on Graphics 25(4), 1424-1441, 2006"
    locator: the whole paper (mean value coordinates for polygons that are not star-shaped, with signed angles)
  - paper: doi:10.1007/978-94-007-5446-1_3
    title: "Jesús R. Nieto and Antonio Susín, Cage based deformations: a survey, in Deformation Models, Lecture Notes in Computational Vision and Biomechanics, Springer, 75-99, 2013 (online 2012)"
    locator: the whole survey (the cage coordinates and their properties)
---

Cage-based deformation moves a detailed model with a coarse cage around it.
The cage is a closed polygon in 2D or a closed triangle mesh in 3D, with far fewer vertices than the model.
Each point $p$ of the model is bound once to the cage by coordinates $w_i(p)$ with $\sum_i w_i(p) = 1$ and $\sum_i w_i(p)c_i = p$.
When the user moves the cage vertices to $c'_i$, the point moves to $p' = \sum_i w_i(p)c'_i$.
The model can be a mesh, a point cloud or a volume, because only its points matter.
The choice of coordinates decides the quality: mean value coordinates (Floater 2003 in 2D, Ju, Schaefer and Warren 2005 in 3D) have a closed form, [harmonic coordinates](/harmonic-coordinates/) are never negative, and [Green coordinates](/green-coordinates/) keep angles.

## In plain words

Put a detailed toy inside a simple wire box that roughly follows its shape.
Each point of the toy remembers how much each corner of the box pulls on it, as a list of weights that add up to 1.
Now bend the box by moving its corners.
Each point of the toy goes to the same weighted mix of the moved corners, so the toy bends with the box.
The animator works with a few corners instead of thousands of points.
If the box does not move, the weights put every point back where it was.

## When it applies

- The model is too detailed, or in a form that is hard to edit directly, such as a scanned mesh or a point cloud.
- A coarse shape around the model can describe the edit: a squash, a bend, a bulge, a pose of a limb.
- The same model is deformed many times, so binding once and deforming often pays off.
- The edit should be smooth in space; sharp folds and cuts are not what cages do.

## The template

1. **Build the cage.** Make a closed polygon or triangle mesh that encloses the model and roughly follows it, with a few vertices where the user wants control.
2. **Choose coordinates.** Pick a kind of [generalized barycentric coordinates](/generalized-barycentric-coordinates/) for the cage: mean value, harmonic or Green coordinates, or another kind.
3. **Bind.** Compute the weights $w_i(p)$ of every model point once and store them.
4. **Deform.** For each pose of the cage, compute $p' = \sum_i w_i(p)c'_i$ for every point. With the weights as an $N \times n$ matrix $W$, this is one matrix product $P' = WC'$.

```pseudo id=main
CAGE-DEFORM(points, c, c')
L1  for each point p, w(p) ← the coordinates of p in the cage c   ▷ once, at bind time
L2  for each point p do
L3      p' ← Σ_i w_i(p) c'_i
L4  return the points p'
```

With closed-form coordinates and a cage of $n$ vertices, line L1 costs $\Theta(n)$ per point and lines L2 and L3 cost $\Theta(n)$ per point per pose, so $N$ points cost $\Theta(Nn)$ for the binding and for each pose, and $\Theta(Nn)$ memory for the weights.
If the coordinates have the partition of unity and linear precision, the rest cage gives back every point, and an affine map of the cage moves the model by the same affine map, because $\sum_i w_i(Ac_i + t) = Ap + t$.
The implementation uses 2D mean value coordinates, and the [proof](proofs/correctness.md) shows these properties for them.

## Classic examples

**Mean value coordinates in 2D.** The coordinate of cage vertex $i$ at $p$ is $\tilde w_i/\sum_j\tilde w_j$ with $\tilde w_i = (\tan(\alpha_{i-1}/2) + \tan(\alpha_i/2))/|c_i - p|$, where $\alpha_i$ is the signed angle at $p$ from $c_i$ to $c_{i+1}$; see [Floater's mean value coordinates](/floater-mean-value-coordinates/).
For the L-shaped cage with the vertices $(0, 0)$, $(2, 0)$, $(2, 1)$, $(1, 1)$, $(1, 2)$, $(0, 2)$, the point $(0.5, 0.5)$ has the coordinates about $(0.5427, 0.1464, 0.0427, 0.0792, 0.0427, 0.1464)$.
Slide the top edge of the L by $0.5$ to the right, so that $(1, 2)$ goes to $(1.5, 2)$ and $(0, 2)$ to $(0.5, 2)$. The point $(0.5, 1.5)$ in the upper arm moves to about $(0.8464, 1.5)$: it follows the top edge by $0.346$ of its move, and its height does not change, because the cage moved only in $x$.

**Mean value coordinates in 3D.** Ju, Schaefer and Warren (2005) extended the coordinates to closed triangle meshes with a closed form per triangle, and used them to deform models with cages.

**Harmonic coordinates.** [Harmonic coordinates](/harmonic-coordinates/) (Joshi and others 2007) solve the Laplace equation inside the cage. They are never negative, so they behave well in concave cages, but they need a numerical solve.

**Green coordinates.** [Green coordinates](/green-coordinates/) (Lipman, Levin and Cohen-Or 2008) add a weight per cage edge or face for its normal. They give conformal maps in 2D, but do not reproduce general affine maps and do not interpolate the cage.

**Lattices.** [Free-form deformation](/free-form-deformation/) is the special case of a box cage with Bernstein weights, and [extended free-form deformation](/extended-free-form-deformation/) joins such cages.

## Variations

- **Point and bone handles.** [Bounded biharmonic weights](/bounded-biharmonic-weights/) compute weights for cages, points and bones together by a constrained optimization, and blend affine transforms instead of only positions, as in [linear blend skinning](/linear-blend-skinning/).
- **Sparse weights.** Coordinates that are 0 far from a vertex, or weights cut below a threshold and renormalized, make $W$ sparse and the deformation cheaper.
- **Normals and frames.** Transform the normals with the inverse transpose of the Jacobian of $p \mapsto \sum_i w_i(p)c'_i$, which needs the gradients of the coordinates.
- **Cages on the GPU.** The deformation is a matrix product, so it runs well on graphics hardware.

## Pitfalls

- **Negative weights.** Mean value coordinates can be negative in a concave cage. In the L-shaped cage, the point $(0.875, 1.375)$ has the weight $-0.0097$ for the vertex $(2, 1)$, which it sees from the back side of an edge: dragging that vertex right moves the point left. Use harmonic coordinates if this matters.
- **Points outside the cage.** The coordinates are made for points inside. Mean value coordinates exist outside too, but they give a poor deformation there, and harmonic coordinates do not exist there.
- **Cage too far from the model.** A loose cage gives weak, blurred control; a cage that cuts the model leaves parts outside.
- **Self-intersecting edits.** A cage that folds over itself gives a folded model; nothing in the method prevents it.
- **Memory.** Dense weights take $Nn$ numbers; for large models with many cage vertices, store sparse weights.
- **Not all coordinates interpolate.** With Green coordinates the model does not touch the moved cage, so a model that must stay inside the cage needs care.

## Exercises

1. Show that if the coordinates satisfy $\sum_i w_i = 1$ and $\sum_i w_ic_i = p$, then moving every cage vertex by an affine map $A(x) = Mx + t$ moves every bound point by $A$.

   *Answer.* $\sum_i w_iA(c_i) = M\sum_i w_ic_i + t\sum_i w_i = Mp + t = A(p)$.

2. Compute the mean value coordinates of the center of the unit square, and of the point $(0.25, 0)$ on its bottom edge.

   *Answer.* At the center every signed angle is $\pi/2$ and every distance is $\sqrt2/2$, so all $\tilde w_i$ are equal and each coordinate is $1/4$. On the bottom edge the coordinates are linear along the edge: $(0.75, 0.25, 0, 0)$.

3. In the L-shaped cage, why is the weight of the vertex $(2, 1)$ negative at $(0.875, 1.375)$?

   *Answer.* Seen from the point, the turn from $(2, 0)$ to $(2, 1)$ is counterclockwise, but the turn from $(2, 1)$ to $(1, 1)$ is clockwise: the point sees the edge from $(2, 1)$ to $(1, 1)$ from its back side. So $\alpha_2 < 0$, and $\tan(\alpha_2/2)$ outweighs $\tan(\alpha_1/2)$, which makes $\tilde w$ of $(2, 1)$ negative.

4. A model has $10^5$ points and its cage has 50 vertices. How many numbers does the binding store, and how many multiply-adds does one pose cost in 3D?

   *Answer.* $10^5 \cdot 50 = 5 \cdot 10^6$ weights, and $3 \cdot 5 \cdot 10^6 = 1.5 \cdot 10^7$ multiply-adds per pose, one set for each coordinate.

5. Explain why the deformed point $(0.8464, 1.5)$ of the slide example keeps its height $1.5$.

   *Answer.* The moved cage differs from the rest cage only in the $x$ coordinates of two vertices, so $\sum_i w_ic'_{i,y} = \sum_i w_ic_{i,y} = 1.5$ by linear precision.

## References
