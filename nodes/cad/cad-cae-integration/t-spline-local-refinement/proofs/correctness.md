---
title: The refinement stops with an analysis-suitable, nested T-mesh, and the new control points give the same surface
proves: [correctness]
status: full
---

We use the notation of the page. $T_1$ is an analysis-suitable bicubic T-mesh in index space with the outer lines complete, $R$ is the request, and $T_2$ is the T-mesh during and after lines L1 to L6. For a T-mesh $T$, an *extension* is the closed segment from the end of the edge extension to the end of the face extension of a T-junction. $E(T_1 \to T_2)$ is the coupled extension graph and $W$ its number of edges. Two steps of the argument are theorems that we cite and do not prove here; they are marked *(cited)*.

**Lemma 1 (a candidate exists).** If $W > 0$, line L4 has at least one insertion edge, and it is not an edge of $T_2$.

*Proof.* $W > 0$ means that $E$ has a crossing edge or a loop edge. Each of them involves an extension of a T-junction $J$ of $T_2$ that is missing the edge in some direction $d$. The face part of that extension is the walk from $J$ in direction $d$ to the second perpendicular line, so the walk meets at least one perpendicular line, and the segment from $J$ to the first one is an insertion edge. Its first unit edge, at $J$ in direction $d$, is not in $T_2$, because $J$ is missing that edge. $\square$

**Lemma 2 (termination).** The loop of lines L3 to L6 stops after at most $u$ rounds, where $u$ is the number of unit edges of the index grid.

*Proof.* By Lemma 1 every round adds at least one unit edge that $T_2$ did not have, and no round removes an edge. $T_2$ is a subset of the $u$ unit edges, so there are at most $u$ rounds. When the loop stops, $W = 0$. $\square$

**Lemma 3 (what $W = 0$ means).** When the loop stops, $T_1 \cup R \subseteq T_2$, $T_2$ is analysis-suitable, and no face extension of $T_2$ ends strictly inside a face extension of $T_1$ in the same direction.

*Proof.* Line L1 puts $T_1$ and $R$ into $T_2$, and later lines only add edges. $W = 0$ means that there is no crossing edge, so no horizontal extension of $T_2$ meets a vertical one, which is the definition of analysis-suitable (Li, Zheng, Sederberg, Hughes and Scott, Definition 7). It also means that there is no loop edge, which is the second statement. $\square$

**Step 4 (nesting, cited).** By Lemma 3, $T_1$ and $T_2$ are analysis-suitable and $T_1^{ext} \subseteq^{\wedge} T_2^{ext}$ in the sense of Scott, Li, Sederberg and Hughes (Section 4.1). Li and Scott (2014) prove that then every blending function $N_A$ of $T_1$ lies in the span of the blending functions $N_B$ of $T_2$. By Theorem 18 of Li and coauthors (2012) the $N_B$ are linearly independent, so the coefficients $c_{AB}$ in $N_A = \sum_B c_{AB} N_B$ are unique.

**Step 5 (the pair formula, cited).** For a cubic B-spline $N[x_0, \ldots, x_4]$ and a finer knot vector that contains $x$, the coefficient of a fine B-spline $N[y_0, \ldots, y_4]$ depends only on $x$ and $y$: it is a discrete B-spline of Cohen, Lyche and Riesenfeld, the number that the [Oslo algorithm](/oslo-algorithm/) computes, and [Boehm's rule](/boehm-knot-insertion/) one knot at a time gives the same number. Scott and coauthors (Section 4.3) use this to show that $c_{AB}$ is the product of the univariate coefficient of $N[s_B]$ in $N[s_A]$ and that of $N[t_B]$ in $N[t_A]$, and is 0 when the index box of $B$ is not inside that of $A$ or when $s_B$ or $t_B$ is not a piece of the insertion. Lines L7 to L10 compute exactly these products, by the one-knot form of Boehm's rule proved on the [T-spline](/t-spline/) page (Lemma 3 of its proof). So $M_{AB} = c_{AB}$.

**Lemma 6 (the surface does not change).** If $N_A = \sum_B M_{AB} N_B$ for every old anchor $A$, then with $Q_B = \sum_A M_{AB} Q_A$ from line L11,

$$\sum_A Q_A N_A = \sum_B Q_B N_B,$$

and the rational surfaces of $(T_1, Q)$ and $(T_2, Q')$ are equal.

*Proof.* $\sum_A Q_A N_A = \sum_A Q_A \sum_B M_{AB} N_B = \sum_B \big(\sum_A M_{AB} Q_A\big) N_B = \sum_B Q_B N_B$, by exchanging two finite sums. Both sides are vectors $(x, y, z, w)$ of functions. The surface is $(x/w, y/w, z/w)$, so it is the same on both meshes. $\square$

**Theorem.** REFINE stops. Its output $T_2$ contains $T_1$ and the request, is analysis-suitable, and every old blending function is the combination of new ones given by its row of $M$. The control points of line L11 give the same rational surface.

*Proof.* Termination is Lemma 2, and the properties of $T_2$ are Lemma 3. The identity $N_A = \sum_B M_{AB} N_B$ is Step 4 with Step 5. The surface is Lemma 6. $\square$

**Remark (what the tests check).** The two cited steps are checked exactly on every mesh of the tests: for each old function, the tests expand $N_A$ and $\sum_B M_{AB} N_B$ in the tensor B-splines on all index lines of the box, with a Boehm insertion that is independent of lines L7 to L10, and compare the two coefficient lists in exact rational arithmetic. The tests also give a T-mesh that is analysis-suitable but not nested, which shows that the loop edges of Lemma 3 are needed. $\blacksquare$
