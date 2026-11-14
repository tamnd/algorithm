---
tag: AEM16J
kind: theorem
slug: nurbs-approximation-estimates
name: Approximation estimates for NURBS spaces
aliases:
- isogeometric error estimates
area: cad/cad-cae-integration
level: research
summary: Bazilevs and coauthors (2006) bound the error of a NURBS projector by h^(l-k) times Sobolev norms, for 0 <= k <= l <= p + 1, so h-refined isogeometric spaces converge at the optimal rate.
prereqs: [approximation-theory, b-spline, nurbs, galerkin-method, finite-element-method]
see_also: [isogeometric-analysis, k-refinement, partition-of-unity, curry-schoenberg-theorem, poisson-equation, isogeometric-quadrature, analysis-suitable-t-spline, truncated-hierarchical-b-spline]
sources:
  - paper: doi:10.1142/S0218202506001455
    title: Y. Bazilevs, L. Beirão da Veiga, J. A. Cottrell, T. J. R. Hughes and G. Sangalli, Isogeometric analysis, approximation, stability and error estimates for h-refined meshes, Mathematical Models and Methods in Applied Sciences 16(7), 2006, 1031 to 1090
    locator: Section 2 (bent Sobolev spaces, NURBS and the geometry map), Section 3.1 to 3.3 (the spline, NURBS and physical projectors and the local and global estimates, Theorems 3.1 and 3.2 with Remark 3.1 in the preprint numbering), Section 3.4 (Dirichlet conditions), Section 5.1 (elasticity)
  - book: isbn:9780521705127
    title: Larry L. Schumaker, Spline Functions, Basic Theory, 3rd edition, Cambridge University Press, 2007
    locator: Chapter 12, the tensor product quasi-interpolant with local dual functionals (cited by Bazilevs and coauthors as Theorem 12.6 of the 1993 printing)
  - paper: doi:10.1007/s00211-010-0338-z
    title: L. Beirão da Veiga, A. Buffa, J. Rivas and G. Sangalli, Some estimates for h-p-k-refinement in isogeometric analysis, Numerische Mathematik 118(2), 2011, 271 to 305
    locator: the whole paper, estimates explicit in the degree and the smoothness
  - paper: doi:10.1017/S096249291400004X
    title: L. Beirão da Veiga, A. Buffa, G. Sangalli and R. Vázquez, Mathematical analysis of variational isogeometric methods, Acta Numerica 23, 2014, 157 to 287
    locator: the survey of approximation results for splines, NURBS and local refinement
  - paper: doi:10.1016/j.cma.2004.10.008
    title: "T. J. R. Hughes, J. A. Cottrell and Y. Bazilevs, Isogeometric analysis: CAD, finite elements, NURBS, exact geometry and mesh refinement, Computer Methods in Applied Mechanics and Engineering 194(39-41), 2005, 4135 to 4195"
    locator: the setting that the estimates analyse, with the geometry fixed on the coarsest mesh
---

These are the first error bounds for the spaces of [isogeometric analysis](/isogeometric-analysis/). Bazilevs, Beirão da Veiga, Cottrell, Hughes and Sangalli proved them in 2006 for h-refinement of a [NURBS](/nurbs/) patch: the degree is fixed, the mesh gets finer, and the geometry stays the one of the coarsest mesh. The result has the same rate as for finite elements of the same degree, $h^{l-k}$ for the $H^k$ error of a function in $H^l$ with $l \le p + 1$. It differs in two places: the constant depends on the geometry map and the weights, and the right side needs the full $H^l$ norm, not only the seminorm. The page states the result as the paper gives it and does not claim more.

## Statement

**Setting.** This is Section 2 and the start of Section 3 of the paper.

- *Patch.* On the parametric domain $(0, 1)^d$ take open knot vectors $\Xi_1, \ldots, \Xi_d$ and degrees $p_1, \ldots, p_d$, and let $p = \min_\alpha p_\alpha$. $S_h$ is the tensor product [B-spline](/b-spline/) space, and the elements $Q$ are the nonempty boxes between knots, with size $h_Q$.
- *Support extension.* $\tilde Q$ is the support extension of $Q$, the union of the supports of the B-splines whose support meets $Q$.
- *Weights and geometry fixed on a coarse mesh.* There is a coarsest mesh $\mathcal Q_{h_0}$. The weight function $w = \sum w_{\mathbf i} B_{\mathbf i}$ is in $S_{h_0}$, $w > 0$, and the geometry map $F = \sum C_{\mathbf i} R_{\mathbf i}$ with $R_{\mathbf i} = w_{\mathbf i} B_{\mathbf i}/w$ is in $(N_{h_0})^d$. Every mesh $\mathcal Q_h$ of the family refines $\mathcal Q_{h_0}$, and $w$ and $F$ are the same functions for all $h$.
- *Shape regularity.* The family is shape regular: the ratio of the smallest edge of $Q$ to its diameter $h_Q$ is bounded uniformly in $Q$ and $h$.
- *Map.* $F : (0, 1)^d \to \Omega$ is invertible with a smooth inverse on each element. $K = F(Q)$, $\tilde K = F(\tilde Q)$, and $h_K = \|\nabla F\|_{L^\infty(Q)}\, h_Q$.
- *Spaces.* $N_h = \{ s / w : s \in S_h \}$ is the NURBS space on the patch, and $V_h = \{ r \circ F^{-1} : r \in N_h \}$ the NURBS space on $\Omega$.

**Projectors.** $\Pi_{S_h} v = \sum_{\mathbf i} (\lambda_{\mathbf i} v) B_{\mathbf i}$ is the quasi-interpolant of Schumaker (Chapter 12) with dual functionals $\lambda_{\mathbf i}$ of local support. It reproduces splines, $\Pi_{S_h} s = s$ for $s \in S_h$, and it is locally stable, $\|\Pi_{S_h} v\|_{L^2(Q)} \le C \|v\|_{L^2(\tilde Q)}$. Then

$$\Pi_{N_h} v = \frac{\Pi_{S_h}(w v)}{w}, \qquad \Pi_{V_h} v = \big(\Pi_{N_h}(v \circ F)\big) \circ F^{-1}.$$

**Constants.** $C$ depends only on $d$, the $p_\alpha$ and the shape regularity. $C_{\mathrm{shape}}$ may also depend on the geometry, through the dimensionless functions $w / \|w\|_{L^\infty}$ and $\nabla F / \|\nabla F\|_{L^\infty}$, but not on $h$.

**Theorem (local estimate, Theorem 3.1 of the paper).** Let $k$ and $l$ be integers with $0 \le k \le l \le p + 1$. For every element $K = F(Q)$ and every $v \in L^2(\Omega) \cap H^l(\tilde K)$,

$$|v - \Pi_{V_h} v|_{H^k(K)} \le C_{\mathrm{shape}}\, h_K^{l-k} \sum_{i=0}^{l} \|\nabla F\|^{i-l}_{L^\infty(\tilde Q)}\, |v|_{H^i(\tilde K)}.$$

**Theorem (global estimate, Theorem 3.2 of the paper).** For the same $k$, $l$ and every $v \in H^l(\Omega)$,

$$\sum_{K \in \mathcal K_h} |v - \Pi_{V_h} v|^2_{H^k(K)} \le C_{\mathrm{shape}} \sum_{K \in \mathcal K_h} h_K^{2(l-k)} \sum_{i=0}^{l} \|\nabla F\|^{2(i-l)}_{L^\infty(F^{-1}(K))}\, |v|^2_{H^i(K)}.$$

The left side of the global estimate is the broken $H^k$ seminorm, the sum over elements. Section 3.4 gives the same bound for a projector that keeps homogeneous Dirichlet conditions, with $0 \le k < l \le p + 1$.

## In plain words

Cut the parameter square of a NURBS patch into smaller and smaller cells, and keep the shape and its weights exactly as the designer made them. Then the NURBS functions can follow any smooth function better and better, and the error goes down as fast as it does for ordinary finite elements of the same degree. If the cells get half as big, the error in the values drops by a factor of about two to the power of the degree plus one. The constants in front depend on how stretched and curved the shape is, but not on the cell size. The result says nothing about raising the degree, only about smaller cells.

## Proof

The proof has three steps: splines on the patch, NURBS on the patch, and the push-forward to $\Omega$. Two tools are cited and not proved here: a Bramble-Hilbert lemma on support extensions (Lemma 3.1 of the paper) and a change of variables bound (Lemma 3.5 of the paper).

**Tool 1 (Bramble-Hilbert on $\tilde Q$, cited).** For $0 \le k \le l \le p + 1$ and $v$ in the bent Sobolev space $\mathcal H^l$ there is an $s \in S_h$ with $|v - s|_{\mathcal H^k(\tilde Q)} \le C h_Q^{l-k} |v|_{\mathcal H^l(\tilde Q)}$. The bent space $\mathcal H^m$ is the space of functions that are $H^m$ on each element and have matching derivatives across a face up to the order $\min(m_{Q_1, Q_2}, m - 1)$, where $m_{Q_1, Q_2}$ is the smoothness of the splines across that face. Its seminorms are sums over elements. The proof maps $\tilde Q$ to a reference configuration with unit cells by a piecewise affine map. There are finitely many patterns of $\tilde Q$, so the constant is uniform.

**Tool 2 (change of variables, cited).** For $K = F(Q)$ and $m \ge 0$,

$$|v \circ F|_{H^m(Q)} \le C_{\mathrm{shape}} \|\det \nabla F^{-1}\|^{1/2}_{L^\infty(K)} \sum_{j=0}^{m} \|\nabla F\|^j_{L^\infty(Q)} |v|_{H^j(K)},$$
$$|v|_{H^m(K)} \le C_{\mathrm{shape}} \|\det \nabla F\|^{1/2}_{L^\infty(Q)} \|\nabla F\|^{-m}_{L^\infty(Q)} \sum_{j=0}^{m} |v \circ F|_{H^j(Q)}.$$

Both follow from the chain rule for derivatives of order $m$ and the bounds on $F$ and $F^{-1}$ on one element. Lower order terms appear because $F$ is not affine.

**Step 1 (splines, Lemma 3.3 of the paper).** Claim: $|v - \Pi_{S_h} v|_{H^k(Q)} \le C h_Q^{l-k} |v|_{\mathcal H^l(\tilde Q)}$. Take $s$ from Tool 1. Since $\Pi_{S_h} s = s$, we have $v - \Pi_{S_h} v = (v - s) - \Pi_{S_h}(v - s)$. The first term is bounded by Tool 1. On $Q$ the function $\Pi_{S_h}(v - s)$ is a polynomial, so the inverse inequality for polynomials on a shape regular box gives $|\Pi_{S_h}(v - s)|_{H^k(Q)} \le C h_Q^{-k} \|\Pi_{S_h}(v - s)\|_{L^2(Q)}$. By local stability this is at most $C h_Q^{-k} \|v - s\|_{L^2(\tilde Q)}$, and Tool 1 with $k = 0$ bounds that by $C h_Q^{l-k} |v|_{\mathcal H^l(\tilde Q)}$.

**Step 2 (NURBS on the patch, Lemma 3.4 of the paper).** Claim: $|v - \Pi_{N_h} v|_{H^k(Q)} \le C_{\mathrm{shape}} h_Q^{l-k} \|v\|_{\mathcal H^l(\tilde Q)}$, with the full norm on the right. Since $w \in S_{h_0} \subseteq S_h$, $w$ is a polynomial on each element with the smoothness of the splines across faces, so $w v \in \mathcal H^l$ when $v \in \mathcal H^l$. Write $v - \Pi_{N_h} v = \frac{1}{w}\,(w v - \Pi_{S_h}(w v))$. The Leibniz rule gives

$$|v - \Pi_{N_h} v|_{H^k(Q)} \le C \sum_{i=0}^{k} |1/w|_{W^{i,\infty}(Q)}\, |w v - \Pi_{S_h}(w v)|_{H^{k-i}(Q)}.$$

Step 1 with the pair $(k - i, l - i)$ bounds each term by $C h_Q^{l-k} |w v|_{\mathcal H^{l-i}(\tilde Q)}$. The Leibniz rule again gives $|w v|_{\mathcal H^{l-i}} \le C \sum_{j=0}^{l-i} |w|_{W^{j,\infty}} |v|_{\mathcal H^{l-i-j}}$. All the orders $l - i - j$ lie between 0 and $l$, so the sum is at most $C_{\mathrm{shape}} \|v\|_{\mathcal H^l(\tilde Q)}$, where the constant collects the norms of $w$ and $1/w$. Here the lower order seminorms of $v$ enter, which is why the full norm appears.

**Step 3 (push-forward, Theorem 3.1).** By definition $v - \Pi_{V_h} v = (v \circ F - \Pi_{N_h}(v \circ F)) \circ F^{-1}$. The second inequality of Tool 2 gives

$$|v - \Pi_{V_h} v|_{H^k(K)} \le C_{\mathrm{shape}} \|\det \nabla F\|^{1/2}_{L^\infty(Q)} \|\nabla F\|^{-k}_{L^\infty(Q)} \sum_{i=0}^{k} |v \circ F - \Pi_{N_h}(v \circ F)|_{H^i(Q)}.$$

For each $i \le k$, Step 2 with the pair $(i, l + i - k)$ bounds the $i$-th term by $C_{\mathrm{shape}} h_Q^{l-k} \sum_{j=0}^{l+i-k} |v \circ F|_{H^j(\tilde Q)}$. Since $j \le l$ in all terms, the double sum collapses to $\sum_{j=0}^{l} |v \circ F|_{H^j(\tilde Q)}$, a sum over the elements $Q'$ of $\tilde Q$. On each $Q'$ the first inequality of Tool 2 turns $|v \circ F|_{H^j(Q')}$ into $\|\det \nabla F^{-1}\|^{1/2} \sum_{i \le j} \|\nabla F\|^i |v|_{H^i(K')}$. The product of the two determinant factors is bounded by $C_{\mathrm{shape}}$, because $\nabla F$ varies by a bounded factor over $\tilde Q$ (shape regularity and $F$ fixed). Collect the sums into one sum over $i \le l$:

$$|v - \Pi_{V_h} v|_{H^k(K)} \le C_{\mathrm{shape}} \|\nabla F\|^{-k}_{L^\infty(\tilde Q)}\, h_Q^{l-k} \sum_{i=0}^{l} \|\nabla F\|^{i}_{L^\infty(\tilde Q)} |v|_{H^i(\tilde K)}.$$

Multiply and divide by $\|\nabla F\|^{l-k}_{L^\infty(Q)}$ and use $h_K = \|\nabla F\|_{L^\infty(Q)} h_Q$. The ratio $\|\nabla F\|^{l-k}_{L^\infty(\tilde Q)} / \|\nabla F\|^{l-k}_{L^\infty(Q)}$ is bounded and goes into $C_{\mathrm{shape}}$. This is the local estimate.

**Global estimate (Theorem 3.2).** Square the local estimate and add over $K$. Each $\tilde K$ is the union of a bounded number of elements, and each element lies in a bounded number of support extensions, with bounds that depend only on $p_\alpha$ and $d$. So the sum of the right sides is at most a constant times the sum over elements of $h_K^{2(l-k)} \sum_i \|\nabla F\|^{2(i-l)} |v|^2_{H^i(K)}$, after locally quasi-uniform meshes let us replace $h_{K'}$ by $h_K$ for neighbours. $\blacksquare$

## Consequences

- **Galerkin error for elasticity (Section 5.1 of the paper).** For linear elasticity with the NURBS space $V_h$ and the [Galerkin method](/galerkin-method/), Céa's argument gives $|u - u_h|_{H^1} \le C(\nu) \inf_{v_h} |u - v_h|_{H^1}$, with $\nu$ the Poisson ratio. With quasi-uniform meshes $h_K \simeq h$, $\min_\alpha p_\alpha = p$ and $u \in H^{p+1}$, the global estimate with $k = 1$, $l = p + 1$ gives $|u - u_h|_{H^1} \le C(\nu, u)\, C_{\mathrm{shape}}\, h^p$. If the problem has $H^2$ regularity, the Aubin-Nitsche argument gives $\|u - u_h\|_{L^2} \le C(\nu, u)\, C_{\mathrm{shape}}\, h^{p+1}$. The same holds for the [Poisson equation](/poisson-equation/).
- **Same rates as finite elements.** A NURBS space of degree $p$ converges at the rates of Lagrange finite elements of degree $p$ under h-refinement, while the geometry is exact on every mesh.
- **The smoothness does not hurt.** The estimate holds for any knot multiplicities, so $C^{p-1}$ spaces with about one function per element in each direction reach the same rate as $C^0$ spaces with about $p^d$ functions per element. That is the count behind [k-refinement](/k-refinement/), but the comparison of constants is not part of the theorem.
- **Tools for other proofs.** The paper also proves inverse estimates for NURBS (Section 4) and uses them for stabilized and mixed methods (Section 5).

## Tightness

- **The exponent $l - k$ with $l = p + 1$ cannot be raised.** Take $d = 1$, $w = 1$, $F$ the identity, a uniform mesh of $[0, 1]$ with $h = 1/N$, and $f(x) = x^{p+1}$. On each element any spline is a polynomial of degree $p$, so $\|f - s\|^2_{L^2(0,1)}$ is at least the sum of the squared best $L^2$ errors on the elements. On an element of length $h$ that error is $(h/2)^{p+1} \sqrt{h/2}\, \|\tilde P_{p+1}\|_{L^2(-1,1)}$, where $\tilde P_{p+1}$ is the monic Legendre polynomial, since $f$ restricted to the element is $(h/2)^{p+1}$ times a monic polynomial in the local variable on $[-1, 1]$. Summing $N = 1/h$ equal terms gives $\|f - s\|_{L^2} \ge c_p h^{p+1}$ for every spline $s$. For $p = 1$ the best error on $[0, h]$ is $x^2 - h x + h^2/6$ with squared norm $h^5/180$, so the bound is $h^2/\sqrt{180}$.
- **The full norm is needed (Remark 3.1 of the paper).** Take $d = 1$, $p = 1$, one element, $F$ the identity and $w(\xi) = 1 + \xi$. Then $N_h = \{ s/(1 + \xi) : s \in S_h\}$ contains $1$, but not $v(\xi) = \xi$, because $\xi (1 + \xi)$ is not piecewise linear on any mesh. So $v - \Pi_{N_h} v \ne 0$ on every mesh, while $|v|_{H^2} = 0$. A bound with only the seminorm $|v|_{H^{p+1}}$ on the right would force the error to be zero, so it is false for NURBS, unlike for splines or finite elements.
- **The constant depends on the geometry.** $C_{\mathrm{shape}}$ depends on $\nabla F$, $w$ and their inverses on each element. If $F$ degenerates, for example a square patch with one edge collapsed to a point to make a disk or a triangle, the assumption that $F^{-1}$ is smooth on each element fails, and the theorem does not apply as stated.
- **Only h-refinement.** The degree is fixed. The theorem says nothing about how the constant grows with $p$ or with the smoothness. Estimates explicit in $p$ and $k$ are partial and later (Beirão da Veiga, Buffa, Rivas and Sangalli 2011).

## History

Hughes, Cottrell and Bazilevs proposed isogeometric analysis in 2005 and showed convergence in numerical tests. Bazilevs, Beirão da Veiga, Cottrell, Hughes and Sangalli gave the first proofs in 2006: approximation by the projector above, inverse estimates, and error bounds for elasticity, Stokes type problems and advection-diffusion. Their spline step uses the quasi-interpolant with local dual functionals from Schumaker's book. Later work extended the estimates to explicit dependence on $p$ (2011), to [T-splines](/analysis-suitable-t-spline/) through dual-compatible bases, and to hierarchical splines such as [THB-splines](/truncated-hierarchical-b-spline/). Beirão da Veiga, Buffa, Sangalli and Vázquez surveyed the theory in Acta Numerica in 2014.

## References
