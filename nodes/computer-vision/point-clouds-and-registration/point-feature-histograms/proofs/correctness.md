---
title: The Darboux features of a pair are complete rigid invariants of the pair, so the PFH and FPFH histograms do not change under rigid motions
proves: [correctness]
status: full
---

All normals are unit vectors. For a pair of points with normals, $(p_a, \mathbf{n}_a)$ and $(p_b, \mathbf{n}_b)$ with $p_a \ne p_b$, let $\hat d = (p_b - p_a) / \lVert p_b - p_a \rVert$. Lines P1 to P5 of the pair procedure choose the source $s$ and the target $t$, set $\mathbf{u} = \mathbf{n}_s$, $\mathbf{v} = \mathbf{u} \times \hat d / \lVert \mathbf{u} \times \hat d \rVert$ and $\mathbf{w} = \mathbf{u} \times \mathbf{v}$, with $\hat d$ now pointing from $p_s$ to $p_t$, and return

$$\alpha = \mathbf{v} \cdot \mathbf{n}_t, \qquad \phi = \mathbf{u} \cdot \hat d, \qquad \theta = \operatorname{atan2}(\mathbf{w} \cdot \mathbf{n}_t, \mathbf{u} \cdot \mathbf{n}_t), \qquad \delta = \lVert p_t - p_s \rVert.$$

The pair is *degenerate* when $\mathbf{u} \times \hat d = 0$, that is, when the source normal lies along the line of the pair; the procedure then returns nothing.

**Lemma 1 (the frame).** For a pair that is not degenerate, $(\mathbf{u}, \mathbf{v}, \mathbf{w})$ is an orthonormal basis with $\mathbf{w} = \mathbf{u} \times \mathbf{v}$, so it is right handed. Moreover

$$\hat d = \phi\, \mathbf{u} - \sqrt{1 - \phi^2}\, \mathbf{w}, \qquad \mathbf{n}_t = \alpha\, \mathbf{v} + \sqrt{1 - \alpha^2}\, (\cos\theta\, \mathbf{u} + \sin\theta\, \mathbf{w}).$$

*Proof.* $\mathbf{v}$ is a unit vector orthogonal to $\mathbf{u}$, and the cross product of two orthogonal unit vectors is a unit vector orthogonal to both. The vector $\hat d$ is orthogonal to $\mathbf{v}$, so $\hat d = (\hat d \cdot \mathbf{u})\, \mathbf{u} + (\hat d \cdot \mathbf{w})\, \mathbf{w}$. Here $\hat d \cdot \mathbf{u} = \phi$, and by the rule for the triple product $\hat d \cdot (\mathbf{u} \times \mathbf{v}) = \mathbf{v} \cdot (\hat d \times \mathbf{u}) = -\mathbf{v} \cdot (\mathbf{u} \times \hat d) = -\lVert \mathbf{u} \times \hat d \rVert = -\sqrt{1 - \phi^2}$. For $\mathbf{n}_t$, write $\mathbf{n}_t = \alpha\, \mathbf{v} + a\, \mathbf{u} + b\, \mathbf{w}$ with $a = \mathbf{u} \cdot \mathbf{n}_t$ and $b = \mathbf{w} \cdot \mathbf{n}_t$. Since $\mathbf{n}_t$ is a unit vector, $a^2 + b^2 = 1 - \alpha^2$, and $\theta = \operatorname{atan2}(b, a)$ gives $a = \sqrt{1 - \alpha^2} \cos\theta$ and $b = \sqrt{1 - \alpha^2} \sin\theta$. $\square$

**Theorem 1 (complete invariants).** Take two pairs that are not degenerate, each with its source and target as chosen at line P2. They have the same features $(\alpha, \phi, \theta, \delta)$ if and only if a proper rigid motion $x \mapsto R x + c$, with $R$ a rotation, maps the source of one to the source of the other, the target to the target, and the normals to the normals.

*Proof.* If such a motion exists, then differences of points and the normals are multiplied by $R$. A rotation keeps dot products and satisfies $R\mathbf{a} \times R\mathbf{b} = R(\mathbf{a} \times \mathbf{b})$, so $\hat d$, $\mathbf{u}$, $\mathbf{v}$ and $\mathbf{w}$ are all multiplied by $R$, and the four features, which are dot products and a length, do not change. Conversely, let the frames of the two pairs be $F = (\mathbf{u}, \mathbf{v}, \mathbf{w})$ and $F' = (\mathbf{u}', \mathbf{v}', \mathbf{w}')$, both right handed and orthonormal by Lemma 1. There is exactly one rotation $R$ with $R F = F'$; set $c = p'_s - R p_s$. Then $R \mathbf{n}_s = \mathbf{n}'_s$ because $\mathbf{n}_s = \mathbf{u}$. By Lemma 1, $\hat d$ and $\mathbf{n}_t$ have coordinates in $F$ that depend only on $\phi$, $\alpha$ and $\theta$, so $R \hat d = \hat d'$ and $R \mathbf{n}_t = \mathbf{n}'_t$, and $R p_t + c = p'_s + \delta\, R \hat d = p'_s + \delta\, \hat d' = p'_t$. $\square$

So the four numbers say everything about the shape of a pair of oriented points and nothing about its position. FPFH, and many PFH implementations, drop $\delta$, because it depends on the sampling density.

**Lemma 2 (the order of the pair).** If $|\mathbf{n}_a \cdot \hat d| \ne |\mathbf{n}_b \cdot \hat d|$, the procedure returns the same features for the pair given as $(a, b)$ and as $(b, a)$.

*Proof.* Line P2 makes the source the point whose normal has the larger value $|\mathbf{n} \cdot \hat d|$; reversing the pair negates $\hat d$, which does not change these two values. So both calls choose the same source and target and compute the same $\hat d$ from source to target, and lines P3 to P5 then do the same computation. $\square$

When the two values are equal, as on a plane where both are 0, the procedure keeps the order it was given. The features are then still rigid invariants, and the histograms below visit each pair in a fixed order.

**Theorem 2 (the histograms).** Let a rigid motion with a rotation act on the points and the normals. Then every SPFH, FPFH and PFH histogram of the procedures is unchanged, except for features that lie exactly on a bin border, where rounding can move a count to the next bin. Each of the three parts of an SPFH or FPFH sums to 1 when the point has at least one neighbor in a pair that is not degenerate.

*Proof.* Distances do not change, so line L2 finds the same neighbor sets, and the same pairs are formed. By Theorem 1 each pair has the same features, so line L5 adds to the same bins. Line L6 scales each part by its total, which is the number of valid pairs and is positive under the assumption. At line L8, the weight $1 / (|K_i|\, \lVert p_j - p_i \rVert)$ depends only on distances, so the weighted sum is the same, and line L9 scales each part, whose total is positive because $\mathrm{SPFH}(p_i)$ adds a positive amount and every weight is positive. The PFH counts all pairs of the neighborhood and is scaled the same way. $\square$

**Proposition 3 (which pairs FPFH sees).** The FPFH of $p_i$ counts the pairs $(p_i, p_j)$ for $p_j \in K_i$, with weight 1 before the scaling, and the pairs $(p_j, p_l)$ for $p_j \in K_i$ and $p_l \in K_j$, with weight $1 / (|K_i|\, \lVert p_j - p_i \rVert)$ times the scaling of $\mathrm{SPFH}(p_j)$.

*Proof.* Expand line L8 with the definition of SPFH at lines L3 to L6. $\square$

So FPFH does not count all pairs among the neighbors of $p_i$, as the PFH does: a pair $(p_j, p_l)$ of two neighbors is counted only if $p_l \in K_j$. It does count pairs that reach up to distance $2r$ from $p_i$. This is the price of computing each pair feature once per pair of neighbors in the whole cloud, in place of once per pair in each neighborhood. $\blacksquare$
