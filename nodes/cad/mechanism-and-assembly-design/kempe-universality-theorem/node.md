---
tag: N4ZZHA
kind: theorem
slug: kempe-universality-theorem
name: Kempe's universality theorem
aliases:
- Kempe linkage theorem
area: cad/mechanism-and-assembly-design
level: advanced
summary: Any bounded piece of a plane algebraic curve is traced by a point of some planar linkage, as Kempe argued in 1876 and Kapovich and Millson proved fully.
prereqs: [peaucellier-lipkin-linkage, coupler-curve]
see_also: [path-generation, kinematic-synthesis, semialgebraic-set, configuration-space, co-np, weierstrass-approximation-theorem, roberts-chebyshev-theorem, watt-and-stephenson-six-bar]
sources:
  - paper: doi:10.1112/plms/s1-7.1.213
    title: A. B. Kempe, On a general method of describing plane curves of the nth degree by linkwork, Proceedings of the London Mathematical Society s1-7, 213 to 216, 1876 (read June 1876; the publisher dates the volume 1875)
    locator: whole paper, the original construction with the reversor, multiplicator, additor and translator
  - paper: doi:10.1016/S0040-9383(01)00034-9
    title: Michael Kapovich and John J. Millson, Universality theorems for configuration spaces of planar linkages, Topology 41(6), 1051 to 1107, 2002
    locator: the first complete proof; Theorem E (the pen vertex gives a covering of a bounded open part of the curve) and Corollary C (every smooth compact manifold is a union of copies of a configuration space)
  - paper: arxiv:math/9807023
    title: Henry C. King, Planar linkages and algebraic sets, Turkish Journal of Mathematics 23(1), 33 to 56, 1999
    locator: the configuration spaces of linkages and cabled linkages up to analytic isomorphism, with a history of the theorem and Thurston's phrase that a linkage can sign your name
  - url: "http://web.mit.edu/tabbott/www/papers/mthesis.pdf"
    title: Timothy Good Abbott, Generalizations of Kempe's Universality Theorem, S.M. thesis, Massachusetts Institute of Technology, 2008 (joint work with Reid W. Barton and Erik D. Demaine)
    locator: Theorem 1.1 and Section 1.6 (statement and Kempe's strategy), Chapter 3 (braced parallelograms and contraparallelograms, reversor, additor, translator, Peaucellier half-plane), Chapter 4 (the corrected proof), Theorems 1.2 and 1.4 to 1.7 (coNP-hardness of rigidity, higher dimensions, drawable sets, bar counts)
  - book: "A. B. Kempe, How to Draw a Straight Line: A Lecture on Linkages, Macmillan, London, 1877"
    locator: the lecture on Peaucellier's cell and related straight-line linkages (general locator)
---

Kempe's universality theorem says that linkages can draw every algebraic curve. Fix any polynomial equation $f(x, y) = 0$ and any disk. Then some planar linkage, made only of rigid bars and pin joints with a few pins fixed to the ground, has a joint whose possible positions are exactly the points of the curve inside the disk. A [four-bar linkage](/four-bar-linkage/) gives one family of sextic [coupler curves](/coupler-curve/), and the [Peaucellier-Lipkin linkage](/peaucellier-lipkin-linkage/) gives a straight line. The theorem says that every algebraic curve can be drawn this way if enough bars are allowed.

The theorem is about existence, not about design. The linkages it builds have a number of bars that grows like the square of the degree of $f$, and nobody would machine one. In engineering, a curve is matched approximately by a small linkage, as the [path generation](/path-generation/) page describes. This page states the theorem, explains why Kempe's 1876 argument was incomplete, and sketches the corrected construction. The full proofs are long, and they are cited rather than repeated.

## Statement

A *linkage* is a graph whose edges, the *bars*, have fixed lengths, together with an assignment of fixed positions in the plane to some of the vertices. A *configuration* places every vertex in $\mathbb{R}^2$ so that the fixed vertices are where they must be and the ends of every bar are at the bar's length apart. The set of all configurations is the *configuration space* $\mathrm{Conf}(\mathcal{L})$. The *trace* of a vertex $v$ is the set of points that $v$ occupies over all configurations. A linkage *draws* a set $S$ if some vertex has trace exactly $S$. Bars may cross each other; the model ignores collisions.

**Theorem (Kempe's universality theorem, as stated by Abbott, Theorem 1.1).** "Let $f \in \mathbb{R}[x,y]$ be a polynomial, and let $B$ be a closed disk in the plane. Then there exists a planar linkage that draws the set $B \cap \{(x,y) \in \mathbb{R}^2 : f(x,y) = 0\}$."

The trace is exact. The pen vertex reaches every point of the curve inside $B$ and no other point.

**Stronger form (Kapovich and Millson, Theorem E).** Let $U$ be an open bounded subset of the curve $\{f = 0\}$. Then there is a linkage for which the map $\mathrm{Conf}(\mathcal{L}) \to \mathbb{R}^2$ that reads off the position of one vertex is a covering space over $U$. A path along the curve then lifts to a continuous motion of the whole linkage, so the pen can travel along each connected piece of the curve without the linkage having to jump.

## In plain words

Take any curve that can be written as a polynomial equation, such as a circle, an ellipse, a figure eight or something far more tangled. Draw a disk around the part you care about. The theorem promises a mechanism made of stiff rods and hinges, with some hinges bolted to the table, such that one hinge, holding a pen, can go to every point of the curve inside the disk and to nothing else.

Kempe's recipe turns the equation into a sum of waves, builds each wave from linkages that copy, double and add angles, adds the waves up with sliding parallelograms, and pins the result to a straight line. His gadgets could fold into unintended shapes, so the pen could stray off the curve. Adding braces that forbid those shapes repairs the proof.

## Proof

The complete proofs are in Kapovich and Millson (2002) and in Abbott's thesis (2008), which follows Kempe's plan and repairs it. The sketch below follows Abbott, Chapters 3 and 4. It shows how each step works and where Kempe's argument breaks, and it proves one bracing lemma in full.

**Step 1, the pen arm.** Fix a vertex $O$ at the origin and take a parallelogram $O M u N$ with $|OM| = R_1$ and $|ON| = R_2$, where $R_1 > R_2 > 0$. Let $\alpha$ and $\beta$ be the angles of $OM$ and $ON$ from the $x$ axis. The output vertex $u$ is

$$x = R_1 \cos\alpha + R_2 \cos\beta, \qquad y = R_1 \sin\alpha + R_2 \sin\beta,$$

and it can reach every point of the annulus $R_1 - R_2 \le |u| \le R_1 + R_2$. Choose the radii so that the annulus contains $B$. Kempe used a rhombus, $R_1 = R_2$. Abbott points out that with a rhombus the configurations over $u = O$ form a whole circle, which spoils the rigidity statements he needs, so he uses $R_1 \neq R_2$.

**Step 2, the polynomial becomes a sum of cosines.** Substitute the two formulas into $f$ and expand every product with $\cos A \cos B = \tfrac12[\cos(A+B) + \cos(A-B)]$ and the matching rules for $\cos A \sin B$ and $\sin A \sin B$. Then combine $d \cos\theta + e \sin\theta$ into $c\cos(\theta + \gamma)$. For $f$ of degree $n$ this gives, inside the annulus,

$$f(x, y) = \sum_{|r| + |s| \le n} f_{r,s} \cos(r\alpha + s\beta + \gamma_{r,s})$$

with real constants $f_{r,s} \ge 0$ and $\gamma_{r,s}$, summed over integer pairs $(r, s)$ (Abbott, Lemma 4.4). There are $2n^2 + 2n + 1$ such pairs. For example,

$$x^2 = \tfrac12(R_1^2 + R_2^2) + \tfrac12 R_1^2 \cos 2\alpha + \tfrac12 R_2^2 \cos 2\beta + R_1 R_2 \cos(\alpha + \beta) + R_1 R_2 \cos(\alpha - \beta),$$

and for the circle $x^2 + y^2 = \rho^2$,

$$x^2 + y^2 - \rho^2 = 2 R_1 R_2 \cos(\alpha - \beta) + (R_1^2 + R_2^2 - \rho^2).$$

With $R_1 = 3$, $R_2 = 2$ and $\rho = 4$ the circle is the set where $12\cos(\alpha - \beta) = 3$, that is $\alpha - \beta = \pm 75.52°$. Both identities were checked numerically at 1000 random angle pairs, with largest error $1.8 \times 10^{-14}$.

**Step 3, gadgets that make angles.** The term $f_{r,s}\cos(r\alpha + s\beta + \gamma_{r,s})$ is the $x$ coordinate of a bar of length $f_{r,s}$ at angle $r\alpha + s\beta + \gamma_{r,s}$. Kempe built such bars from three gadgets.

- The *reversor* glues two similar contraparallelograms, $Y O X P$ and $Z O Y W$, along the bar $OY$. Corresponding angles of similar figures are equal, so $\angle XOY = \angle YOZ$. Reading the bars in different orders gives $-\theta$, $2\theta$ or $\theta/2$ from $\theta$.
- The *multiplicator* chains $k - 1$ reversors to get $k\theta$ from $\theta$.
- The *additor* is two reversors that share a bisector bar $OM$. One forces $2\angle WOM = \angle WOX + \angle WOY$, the other forces $\angle WOZ = 2\angle WOM$, so $\angle WOZ = \angle WOX + \angle WOY$.

A bar fixed to the ground at angle $\gamma_{r,s}$ supplies the constant. With these, unit bars at all angles $r\alpha$ and $s\beta$ for $|r|, |s| \le n$ take $O(n)$ gadgets, and the sums $r\alpha + s\beta + \gamma_{r,s}$ take $O(n^2)$ additors.

**Step 4, adding the terms.** Kempe's *translator* is two parallelograms glued in a chain. It forces $\overrightarrow{OZ} = \overrightarrow{OY} + \overrightarrow{OX}$, so it moves a copy of a bar $OX$ to the end of another vector. Chaining one translator per term gives a vertex $W$ with

$$W = (a, b) + \sum_{|r|+|s| \le n} f_{r,s}\big(\cos\theta_{r,s},\ \sin\theta_{r,s}\big), \qquad \theta_{r,s} = r\alpha + s\beta + \gamma_{r,s},$$

for a fixed starting point $(a, b)$. Its $x$ coordinate is $a + f(x, y)$.

**Step 5, pinning to a line.** Attach a [Peaucellier-Lipkin cell](/peaucellier-lipkin-linkage/) that holds $W$ on the line $x = a$. Then every configuration has $f(x, y) = 0$ at the pen $u$, and every point of the curve in the annulus lifts to a configuration. Abbott instead uses a variant of the cell that holds $W$ in the half-plane $x \ge a$, which draws $\{f \ge 0\}$. Gluing the linkages for $f \ge 0$, for $-f \ge 0$ and for the disk $B$ at the same pen vertex gives the curve inside $B$.

**Step 6, where Kempe's proof breaks.** A four-bar loop $ABCD$ with $|AB| = |CD|$ and $|BC| = |DA|$ has three kinds of configurations: parallelograms, the degenerate ones in which all four joints lie on a line, and contraparallelograms (the crossed shape, with $AC \parallel BD$). The linkage can pass through a degenerate configuration and come out as the other kind. Kempe's gadgets assume one kind throughout: the pen arm and the translators need parallelograms, the reversors need contraparallelograms. After a switch, the angle relations of Step 3 or the vector sums of Step 4 fail, so the linkage has configurations Kempe did not intend, and the pen is no longer forced onto the curve. Abbott calls this failure to consider continuous motions between the kinds of configuration the primary error in the proof. The Peaucellier cell has the same defect: its rhombus can fold so that two opposite joints meet.

**Step 7, bracing.** The fix adds bars that are compatible with the intended configurations and impossible in the others. For the parallelogram this was known to Kapovich and Millson, and the proof is short. Let $M$ and $N$ be the midpoints of $AB$ and $CD$, held there by extra collinear bars, and add a bar $MN$ of length $|BC|$.

*Claim.* The braced linkage has every parallelogram and degenerate configuration of $ABCD$ and no nondegenerate contraparallelogram.

*Proof.* In a parallelogram, $\overrightarrow{MN} = \overrightarrow{BC}$, so the extra bar fits. The degenerate configurations are limits of parallelograms, so it fits there too. In a nondegenerate contraparallelogram, $|MN| = \tfrac12(|AC| + |BD|)$. Let $X$ be the crossing point of $AD$ and $BC$. By the triangle inequality, strict because the configuration is not degenerate,

$$2|MN| = |AC| + |BD| < (|AX| + |XC|) + (|BX| + |XD|) = (|AX| + |XD|) + (|BX| + |XC|) = |AD| + |BC| = 2|BC|.$$

So $|MN| < |BC|$, and the bar $MN$ cannot be placed. $\blacksquare$

For contraparallelograms Abbott adds a new bracing (his Proposition 3.3). A vertex $X$ is joined by bars of length $R_1$ to the midpoints of $AB$ and $CD$, and by bars of length $R_2$ to the midpoints of $BC$ and $DA$, with $R_1, R_2$ large and $R_2^2 - R_1^2 = \tfrac14(|AB|^2 - |AD|^2)$. For the Peaucellier cell he braces its rhombus as a parallelogram. With all these braces, Abbott proves in Chapter 4 that the construction draws exactly $B \cap \{f = 0\}$ and that the stronger covering form also holds. Kapovich and Millson reach the same theorem with a different argument based on complex algebra instead of trigonometry.

**Step 8, size.** Each gadget uses $O(1)$ bars, and Steps 3 and 4 use $O(n^2)$ gadgets, so the linkage has $O(n^2)$ bars for a curve of degree $n$ (Abbott, Theorem 1.6 with one output point in the plane).

## Consequences

**A linkage can sign your name.** By the [Weierstrass approximation theorem](/weierstrass-approximation-theorem/), a continuous curve can be approximated by an algebraic one, so a linkage can trace any drawing up to a small error. Thurston summarized the theorem this way, and King records the phrase. The covering form of the theorem means each connected stroke can be drawn in one continuous motion.

**Drawable sets.** King proved, and Abbott reproves (Theorem 1.5), that a set $S \subset \mathbb{R}^d$ with $d \ge 2$ is drawable if and only if $S = \mathbb{R}^d$ or $S$ is a compact [semialgebraic set](/semialgebraic-set/). Linkages in $d$ dimensions can also draw $B^m \cap \{f = 0\}$ for a polynomial $f$ in the coordinates of $m$ vertices (King, Abbott Theorem 1.4).

**Configuration spaces are universal.** Kapovich and Millson's Corollary C says that for every smooth compact manifold $M$ there is a linkage whose [configuration space](/configuration-space/) is diffeomorphic to a disjoint union of finitely many copies of $M$. Thurston had stated this in lectures without a proof. So the configuration spaces of planar linkages are as complicated as compact manifolds can be.

**Rigidity is hard.** Abbott uses the corrected construction, with an algorithm that builds a configuration over a given point, to prove that deciding whether a given configuration of a linkage is rigid is [coNP](/co-np/)-hard in every dimension $d \ge 2$ (Theorem 1.2). For contrast, rigidity of generic frameworks in the plane is decided combinatorially by [Laman's theorem](/laman-theorem/); the hardness concerns specific configurations.

**For mechanism design.** The theorem sets the outer limit of [kinematic synthesis](/kinematic-synthesis/): any algebraic path can be produced exactly, but only by very large linkages. Small linkages are the useful ones, and they give a few fixed families of curves. The four-bar gives coupler curves of degree six, and by the [Roberts-Chebyshev theorem](/roberts-chebyshev-theorem/) each such curve is traced by three different four-bars. The [Watt and Stephenson six-bars](/watt-and-stephenson-six-bar/) give a richer family. Exact straight-line and circle-arc motion from a handful of bars, as in Peaucellier's cell, is the exception.

## Tightness

**Boundedness cannot be dropped.** A drawable set is either bounded or the whole plane (Abbott, Proposition 2.5). If the pen's connected part of the linkage contains a fixed vertex, the pen stays within the sum of all bar lengths of that fixed vertex. If it contains none, the whole part can be translated so that the pen is at any point. So no linkage draws a full line or a full parabola, and the disk $B$ in the statement is needed.

**Algebraic is needed, up to semialgebraic.** By the characterization above, only compact semialgebraic sets are drawable. The arc $y = e^x$ for $0 \le x \le 1$ is not semialgebraic, because a semialgebraic function of one variable satisfies a polynomial equation, so no linkage draws it exactly. Approximations are all one can have.

**Bar count.** Abbott proves that drawing the zero set of a polynomial of degree $n$ in $d$ dimensions needs $\Omega(n^d)$ bars in the worst case (Theorem 1.7). In the plane this matches the $O(n^2)$ upper bound, so $\Theta(n^2)$ bars are needed for some curves of degree $n$. He also gives a tight $\Theta(n)$ bound for drawing a set of $n$ points.

**The braces are needed.** Without bracing, the gadgets of Step 3 and the cell of Step 5 have extra configurations, as Step 6 shows. Abbott notes that some later accounts, including published algorithms for building Kempe linkages, repeat this omission.

## History

Peaucellier found his exact straight-line linkage in 1864 and published it in 1873; Lipkin found it independently in 1871. Hart gave a version with fewer bars in 1875. Kempe presented his general method to the London Mathematical Society in June 1876 and published it in its Proceedings, with gadgets he named the reversor, multiplicator, additor and translator. A year later his lecture *How to Draw a Straight Line* brought Peaucellier's cell and related linkages to a wider audience.

For more than a century the 1876 proof was taken as complete. Thurston discussed the theorem in lectures in the 1970s, gave it the phrase about signing one's name, and stated the stronger claim about manifolds, without publishing proofs. Kapovich and Millson gave the first rigorous proof, which circulated as a preprint and was published in Topology in 2002; it also showed that Kempe's gadgets have degenerate configurations. King published a rigorous proof in 1999 as a corollary of his work on linkages with cables, and in later preprints extended the theorem to higher dimensions and to a characterization of drawable sets. Abbott, with Barton and Demaine, gave in 2008 an elementary proof that stays close to Kempe's own construction, with new braces for the contraparallelogram, together with the bar-count bounds and the coNP-hardness of rigidity.

## References
