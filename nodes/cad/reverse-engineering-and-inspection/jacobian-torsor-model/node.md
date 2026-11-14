---
tag: E9KXAA
kind: model
slug: jacobian-torsor-model
name: Jacobian-torsor model
aliases:
- Jacobian-torsor tolerance analysis
area: cad/reverse-engineering-and-inspection
level: research
summary: Desrochers and coauthors' tolerance analysis that maps the torsor intervals of each part through a kinematic Jacobian to the functional requirement of an assembly.
prereqs: [small-displacement-torsor, interval-arithmetic]
see_also: [tolerance-map, requicha-tolerance-zone-theory, direct-linearization-method, monte-carlo-tolerance-analysis, tolerance-stack-up, adjoint-map-se3, geometric-jacobian, datum-reference-frame]
sources:
  - paper: doi:10.1115/1.1573235
    title: Alain Desrochers, Walid Ghie and Luc Laperrière, Application of a unified Jacobian-torsor model for tolerance analysis, Journal of Computing and Information Science in Engineering 3(1), 2 to 14, 2003
    locator: the whole paper (functional elements and functional requirements, the Jacobian matrix of the chain, small displacement torsors with interval components, and the worked assembly)
  - paper: doi:10.1016/S0007-8506(07)61550-9
    title: Luc Laperrière, Walid Ghie and Alain Desrochers, Statistical and deterministic tolerance analysis and synthesis using a unified Jacobian-torsor model, CIRP Annals 51(1), 417 to 420, 2002
    locator: the whole paper (the unified model, and its worst-case and statistical forms)
  - paper: doi:10.1080/00207540902824982
    title: Walid Ghie, Luc Laperrière and Alain Desrochers, Statistical tolerance analysis using the unified Jacobian-torsor model, International Journal of Production Research 48(15), 4609 to 4630, 2010
    locator: the whole paper (the statistical form of the model)
  - paper: doi:10.1016/j.cad.2014.02.014
    title: Hua Chen, Sun Jin, Zhimin Li and Xinmin Lai, A comprehensive study of three dimensional tolerance analysis methods, Computer-Aided Design 53, 1 to 13, 2014
    locator: the part on the Jacobian-torsor model and its comparison with T-Maps and the other 3D methods
---

The Jacobian-torsor model is a 3D tolerance analysis that joins two tools. The [small displacement torsor](/small-displacement-torsor/) describes the deviation of each feature of each part, and the components of each torsor are given as intervals. The Jacobian matrix, borrowed from robot kinematics, carries a small displacement at each feature along the chain of parts to the point and frame of a functional requirement. Desrochers, Ghie and Laperrière gave this unified form in 2003, with a statistical form in 2002 and 2010. The result is one linear relation, the functional requirement torsor $FR = J \cdot FE$, where $FE$ stacks the torsors of the functional elements. Worst-case bounds come from interval arithmetic on this relation, and statistical bounds from the variances of its terms. Of the four variation models on this site it is the most direct to compute. It is also the coarsest: it keeps each torsor component in a separate interval, a box, where a [Tolerance-Map](/tolerance-map/) keeps the exact convex set and [Requicha's zones](/requicha-tolerance-zone-theory/) keep the surface.

## The machine

The "machine" of a variation model is its representation of a part and its assumptions about the deviations.

**The representation.** An assembly is a chain of *functional elements* (FEs) from a datum to the feature that carries the functional requirement (FR). An FE is a pair of features: two features on one part (an internal pair, whose torsor holds the tolerances of the part) or two features in contact on two parts (a contact pair, whose torsor holds the play of the joint). Each FE $i$ has a frame with origin $P_i$ and rotation $R_i$ from the global frame, and a torsor $FE_i = (u_i, \omega_i)$ of its small translation and small rotation in that frame. In this model each of the six components is an interval, for example $u_i \in [-0.05, 0.05]$. The functional requirement is the torsor of the target feature at its point $P$:

$$ FR = \sum_{i=1}^{n} J_i \, FE_i, \qquad J_i = \begin{pmatrix} R_i & -[d_i] R_i \\ 0 & R_i \end{pmatrix}, \quad d_i = P - P_i, $$

where $[d]$ is the skew-symmetric matrix with $[d] x = d \times x$, and both torsors list the translation first. The Jacobian $J = [J_1 \cdots J_n]$ is $6 \times 6n$. Components that the invariance of a feature leaves undetermined, such as a slide along a plane, are fixed (usually to zero) before propagation, and they must not affect the FR.

**Assumptions.** The model takes these as given.

- Each deviation is a small rigid motion of an ideal feature, so the model inherits the first-order (small-angle) approximation of the SDT and ignores form error.
- Deviations of the FEs add along the chain, which holds to first order.
- In the worst-case form, the components of all torsors vary independently over their intervals: the set of deviations is a box. In the statistical form they are independent random variables with given variances.
- The chain is open, or a closed loop has been cut into one open chain to the FR. The nominal geometry gives $R_i$ and $P_i$; the deviations do not change $J$.

## What it counts

A variation model counts no cost. This section says which variations the model can express.

- **3D rigid deviations of features and play in joints.** Every GD&T tolerance that bounds the position and orientation of an ideal feature, and every clearance in a contact, becomes intervals on the components of one torsor.
- **The worst-case range and the variance of each FR component.** Both are linear computations with $J$.
- **Sensitivities.** The entries of $J$ say how much each tolerance contributes to each FR component, which is the input of [tolerance allocation](/tolerance-allocation/).
- **What it cannot express.** Coupling between the components of one torsor is lost: a face that uses up its tolerance by offset cannot also tilt fully, but a box allows both at once. Form error, large rotations and nonlinear assembly behaviour, such as a contact that changes as parts move, are outside the model; the [direct linearization method](/direct-linearization-method/) solves for small kinematic adjustments in the loops, and [Monte Carlo analysis](/monte-carlo-tolerance-analysis/) can solve each sample exactly.

## Relation to other models

- **[Small displacement torsor](/small-displacement-torsor/).** The SDT gives the components and the transport law. The Jacobian of each FE is the transport law plus a change of frame.
- **[Tolerance-Map](/tolerance-map/).** The interval box of an FE is the smallest box that contains its T-Map. A T-Map analysis uses the exact convex set and Minkowski sums; the Jacobian-torsor analysis uses boxes and interval sums. On the same data, its worst case is never smaller than that of the T-Map, and the examples below show how much larger it can be.
- **[Direct linearization method](/direct-linearization-method/).** DLM builds the sensitivities from vector loops of dimensions and solves for the kinematic variables of closed loops. The Jacobian-torsor model builds them from the frames of 3D features. Both end with the worst-case and RSS formulas of [tolerance stack-up](/tolerance-stack-up/) applied to a linear map.
- **Robotics.** $J_i$ is the first-order form of the [adjoint map](/adjoint-map-se3/) of the rigid motion from FE $i$ to the FR, the same matrix that a [geometric Jacobian](/geometric-jacobian/) of a serial robot uses to move a twist from a joint to the tool. Here the "joints" are the deviations, and they are not driven but bounded.

## Known results in the model

The results below are proved here. The model and its worked assemblies are from Desrochers, Ghie and Laperrière, and the statistical form is from Laperrière, Ghie and Desrochers and from Ghie, Laperrière and Desrochers. There are no standard benchmarks for tolerance analysis, and no measured results are claimed here.

**The Jacobian of one element.** Let FE $i$ move the points of the target by the torsor $(u_i, \omega_i)$ at $P_i$, given in the frame of FE $i$. In the global frame its rotation is $R_i \omega_i$ and its translation at $P_i$ is $R_i u_i$. By the transport law of the SDT, the translation at $P$ is $R_i u_i + (R_i \omega_i) \times (P - P_i) = R_i u_i - d_i \times R_i \omega_i$, and the rotation is unchanged. This is the matrix $J_i$ above. $\square$ The FR torsors of several elements add because the composition of small motions adds to first order, as the SDT page proves.

**Interval propagation is exact on the box.** Let $y = \sum_j a_j x_j$ with each $x_j$ in $[l_j, h_j]$, independently. Then the range of $y$ over the box is

$$ \Big[\sum_j \min(a_j l_j, a_j h_j), \; \sum_j \max(a_j l_j, a_j h_j)\Big], $$

and [interval arithmetic](/interval-arithmetic/) applied term by term returns exactly this. *Proof.* The sum is separable, so its maximum over a box is the sum of the maxima of $a_j x_j$ over $[l_j, h_j]$, each at an endpoint; the minimum likewise. Interval multiplication by the number $a_j$ and interval addition compute these endpoint values. $\square$ The usual overestimation of interval arithmetic, which comes from a variable that occurs twice, does not arise, because each component appears once in $FR = J \cdot FE$. With symmetric intervals $[-T_j, T_j]$ the half-width is $\sum_j |a_j| T_j$, the worst-case formula of [tolerance stack-up](/tolerance-stack-up/).

**The box can overestimate by up to a factor $1 + \sqrt 2$.** Take a round face of radius $r$ with a size zone of width $t$. Its exact set of deviations is the double cone $|w| + r\sqrt{\alpha^2 + \beta^2} \le t/2$ of its [T-Map](/tolerance-map/), and the smallest box around it is $|w| \le t/2$, $|\alpha|, |\beta| \le t/(2r)$. For a linear output $c_0 w + c_1 \alpha + c_2 \beta$, write $A = |c_0| t/2$ and $B = \sqrt{c_1^2 + c_2^2}\, t/(2r)$. The worst case over the cone is $\max(A, B)$, at the apex or on the rim, because a linear function on a convex set takes its maximum at an extreme point. The worst case over the box is $A + (|c_1| + |c_2|) t/(2r) \le A + \sqrt 2 B$. So the ratio is at most $(A + \sqrt 2 B)/\max(A, B) \le 1 + \sqrt 2$, with equality when $A = B$ and $|c_1| = |c_2|$. $\square$ The equality case is concrete: the height of a rim point of the face at 45 degrees to the axes. The face lies in its zone, so the point moves at most $t/2$, but the box allows $(1 + \sqrt 2)\, t/2$.

**Statistical form.** If the components of $FE$ are independent with variances $\sigma_j^2$, then the variance of the FR component $y = \sum_j a_j x_j$ is $\sum_j a_j^2 \sigma_j^2$, exactly, for the linear model. This is the RSS formula of the stack-up page. Treating the six components of one torsor as independent is an assumption, and it is false for the same reason as above: their joint range is a cone or a polytope, not a box.

**Example, a column on a face.** A rectangular face of 40 by 20 mm ($a = 20$ along $x$, $b = 10$ along $y$) has a size zone of width $t = 0.1$, so its torsor at the centre has $w \in [-0.05, 0.05]$, $\alpha \in [-0.005, 0.005]$ and $\beta \in [-0.0025, 0.0025]$. A rigid column stands on it, and the FR is the vertical displacement of the point $P = (100, 0, 50)$ on the column. With $d = (100, 0, 50)$ and $R = I$, the vertical component of $u - d \times \omega$ is $w + \alpha d_y - \beta d_x = w - 100 \beta$. Interval propagation gives $[-0.05, 0.05] + 100 \cdot [-0.0025, 0.0025] = [-0.30, 0.30]$. The exact set for this face is the octahedron $|w| + 10|\alpha| + 20|\beta| \le 0.05$ of the [SDT page](/small-displacement-torsor/); over it the largest value of $w - 100\beta$ is at a vertex, $\max(0.05, 100 \cdot 0.0025) = 0.25$. So the box overestimates the worst case by 20 percent here.

## References
