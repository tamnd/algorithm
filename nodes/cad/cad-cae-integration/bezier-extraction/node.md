---
tag: 5HN7GF
kind: technique
slug: bezier-extraction
name: Bezier extraction
aliases:
- Bezier extraction operator
area: cad/cad-cae-integration
level: advanced
summary: Write the B-splines or NURBS on each element as N = C^e B, a small matrix times the Bernstein polynomials, so a standard finite element code can run isogeometric analysis.
prereqs: [bernstein-polynomials, b-spline, nurbs, boehm-knot-insertion, finite-element-method]
see_also: [isogeometric-analysis, k-refinement, isogeometric-quadrature, t-spline, bezier-curve, de-casteljau-algorithm, cox-de-boor-recursion, knot-refinement]
sources:
  - paper: doi:10.1002/nme.2968
    title: "M. J. Borden, M. A. Scott, J. A. Evans and T. J. R. Hughes, Isogeometric finite element data structures based on Bézier extraction of NURBS, International Journal for Numerical Methods in Engineering 87(1-5), 2011, 15 to 47"
    locator: the whole paper, the extraction operator in one dimension with its knot insertion algorithm, the tensor product case and the NURBS case
  - paper: doi:10.1002/nme.3167
    title: "M. A. Scott, M. J. Borden, C. V. Verhoosel, T. W. Sederberg and T. J. R. Hughes, Isogeometric finite element data structures based on Bézier extraction of T-splines, International Journal for Numerical Methods in Engineering 88(2), 2011, 126 to 156"
    locator: the whole paper, extraction for T-splines
  - book: isbn:9780470748732
    title: J. A. Cottrell, T. J. R. Hughes and Y. Bazilevs, Isogeometric Analysis, Toward Integration of CAD and FEA, Wiley, 2009
    locator: Chapter 3 (NURBS as a basis for analysis, p. 69) and Appendix A (connectivity arrays, p. 313)
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, 2nd edition, Springer, 1997
    locator: Chapter 5, the decomposition of a B-spline curve into Bezier pieces by knot insertion
---

Bezier extraction writes the [B-splines](/b-spline/) of degree $p$ that are nonzero on one element as linear combinations of the $p + 1$ [Bernstein polynomials](/bernstein-polynomials/) of that element. For the element $e$ it gives a $(p + 1) \times (p + 1)$ matrix $C^e$, the *element extraction operator*, with $N^e(u) = C^e B(s)$, where $N^e$ is the vector of the local B-splines and $B(s)$ the vector of Bernstein polynomials in the local parameter $s \in [0, 1]$. The Bernstein polynomials are the same on every element, so a [finite element](/finite-element-method/) code can treat them as the shape functions of one reference element. The matrices $C^e$ carry all the information about the knots, and the usual element loop, assembly with a connectivity array and [Gauss quadrature](/isogeometric-quadrature/) stay as they are. Borden, Scott, Evans and Hughes introduced this form for NURBS in 2011, and Scott and coauthors applied it to T-splines in the same year.

The notation is the one of the [B-spline](/b-spline/) page: a clamped knot vector $u_1 \le \cdots \le u_m$ (here 1-based, as in the paper), degree $p$, $n = m - p - 1$ functions $N_1, \ldots, N_n$, and elements the nonempty spans $[u_k, u_{k+1})$. On the element with span $k$ only $N_{k-p}, \ldots, N_k$ are nonzero, and they are the rows of $N^e$ in this order. The local parameter is $s = (u - u_k)/(u_{k+1} - u_k)$. Borden and coauthors use the parent element $[-1, 1]$. The matrix $C^e$ is the same for both choices, since only the parameter of $B$ changes.

## In plain words

A spline is made of polynomial pieces, and each piece of each basis function is a polynomial on one element. A finite element code likes to use the same few polynomials on every element, the shape functions of a standard element. Bezier extraction finds, for each element, a small table of numbers that says how much of each standard polynomial each spline function contains there. The code keeps one table per element. It evaluates the standard polynomials once, multiplies by the table, and gets the spline functions. Everything else in the code, the loop over elements, the integration and the assembly, does not change. The tables come from cutting the spline into pieces at its knots, which is an exact operation.

## When it applies

- You want to run [isogeometric analysis](/isogeometric-analysis/) inside an existing [finite element](/finite-element-method/) code, with an element loop, element matrices and assembly by a connectivity array.
- The basis is a B-spline or [NURBS](/nurbs/) basis, a tensor product of them, or a T-spline (with a different way to compute $C^e$, see Variations). The basis must be piecewise polynomial on the elements, or a ratio of such functions.
- You evaluate the basis at many points per element, so the cost of the Bernstein values (shared by all elements of the same degree) and one small matrix product is lower than the [Cox-de Boor recursion](/cox-de-boor-recursion/) at each point.
- It is also the input format of Bezier based tools: element by element export of a spline model, Bezier projection and some refinement codes.

## The template

The operators come from knot insertion. Insert each interior knot until it has multiplicity $p$. Then each element has its own $p + 1$ control points, the Bezier points of that piece. The loop below is the one-pass algorithm of Borden and coauthors. It does the insertions for one element at a time, on the matrix instead of on control points, and copies the overlap with the next element into the next operator. Here $\alpha$ is a list of $p$ numbers, and "column $k$" is a column of $C^e$.

```pseudo id=main
BEZIER-EXTRACT(u_1..u_m, p)         ▷ clamped knots, interior multiplicities ≤ p
L1  a ← p + 1; b ← a + 1; e ← 1; C^1 ← I
L2  while b < m:
L3      C^{e+1} ← I; i ← b
L4      while b < m and u_{b+1} = u_b: b ← b + 1
L5      mult ← b − i + 1                         ▷ multiplicity of the knot u_b
L6      if mult < p:
L7          for j = p down to mult + 1: α_{j−mult} ← (u_b − u_a)/(u_{a+j} − u_a)
L8          r ← p − mult                         ▷ number of insertions of u_b
L9          for j = 1 to r:
L10             s ← mult + j
L11             for k = p + 1 down to s + 1: column k ← α_{k−s} · column k + (1 − α_{k−s}) · column k − 1
L12             if b < m: rows r−j+1 .. r+1 of column r−j+1 of C^{e+1} ← rows p−j+1 .. p+1 of column p+1 of C^e
L13     e ← e + 1
L14     if b < m: a ← b; b ← b + 1
L15 return C^1, ..., C^{e−1}
```

**Why $N^e = C^e B$.** Let $\hat u$ be the knot vector with every interior knot of multiplicity $p$, and let $\hat N_1, \ldots, \hat N_{\hat n}$ be its B-splines. [Knot insertion](/boehm-knot-insertion/) gives a matrix $A$ of size $\hat n \times n$ with the property: for every set of control points $P$, the control points on $\hat u$ of the same curve are $\hat P = A P$. So $\sum_i N_i(u) P_i = \sum_k \hat N_k(u) (A P)_k = \sum_i \big(\sum_k A_{ki} \hat N_k(u)\big) P_i$ for all $P$. Take $P$ to be the unit vectors: $N_i = \sum_k A_{ki} \hat N_k$, or $N = A^T \hat N$. On $\hat u$ each element has its own block of $p + 1$ functions $\hat N_k$, and on the element they are the Bernstein polynomials in $s$, because a B-spline whose knots are only the two ends of one element, each repeated, is a Bernstein polynomial. All other $\hat N_k$ are zero on the element. Restrict $N = A^T \hat N$ to the element: $N^e = C^e B$, where $C^e$ is the block of $A^T$ with the rows of the $p + 1$ functions that are nonzero on $e$ and the columns of the Bezier functions of $e$. The algorithm computes these blocks. Line L11 is Boehm's formula for the new control points, applied to the columns, because the columns of $C^e$ are the coefficients of the current control points in terms of the original ones. Line L12 copies the new points that also belong to the next element.

**Properties.** Each column of $C^e$ sums to 1, because $\sum_a N_a = 1$ and $\sum_j B_j = 1$ on the element ([partition of unity](/partition-of-unity/)), and the Bernstein polynomials are linearly independent. The entries are nonnegative, because Boehm's coefficients are convex combinations. $C^e$ is invertible: both $N^e$ and $B$ are bases of the polynomials of degree $p$ on the element (the $p + 1$ local B-splines are linearly independent there by the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/) on one span). The Bezier control points of the element are $(C^e)^T P^e$, where $P^e$ are the local control points, since $C(u) = (P^e)^T N^e = (P^e)^T C^e B$.

**NURBS.** With weights $w^e$ for the local functions, the [NURBS](/nurbs/) basis on the element is $R^e(s) = \frac{1}{W(s)} \operatorname{diag}(w^e)\, C^e B(s)$, where $W(s) = (w^e)^T C^e B(s)$ is the weight function in Bernstein form. So the same $C^e$ serves both the B-splines and the NURBS.

**Tensor products.** On a [tensor product](/tensor-product-surface/) patch the element operator is the Kronecker product of the one-dimensional operators of the two (or three) directions, in the order that matches the numbering of the local functions.

## Classic examples

**A cubic with simple knots.** Take $p = 3$ and $u = (0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4)$, so 7 functions and 4 elements. The algorithm gives

$$C^1 = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & \tfrac12 & \tfrac14 \\ 0 & 0 & \tfrac12 & \tfrac{7}{12} \\ 0 & 0 & 0 & \tfrac16 \end{pmatrix}, \quad C^2 = \begin{pmatrix} \tfrac14 & 0 & 0 & 0 \\ \tfrac{7}{12} & \tfrac23 & \tfrac13 & \tfrac16 \\ \tfrac16 & \tfrac13 & \tfrac23 & \tfrac23 \\ 0 & 0 & 0 & \tfrac16 \end{pmatrix},$$

and $C^3$, $C^4$ are $C^2$, $C^1$ with the rows and the columns in reverse order. Here $B_0, \ldots, B_3$ are the cubic Bernstein polynomials. Row 2 of $C^1$ says $N_2 = B_1 + \tfrac12 B_2 + \tfrac14 B_3$ on $[0, 1]$. At $u = s = 1/2$, $B(1/2) = (\tfrac18, \tfrac38, \tfrac38, \tfrac18)$ and $N_2(1/2) = \tfrac38 + \tfrac{3}{16} + \tfrac{1}{32} = \tfrac{19}{32}$, the value the Cox-de Boor recursion gives. The first column of $C^e$ holds the values of the local functions at the left end of the element, since only $B_0$ is nonzero at $s = 0$, and the last column holds the values at the right end. So the last column $(0, \tfrac16, \tfrac23, \tfrac16)$ of $C^2$ is $N_2(2), \ldots, N_5(2)$. In a longer uniform knot vector every interior element has the operator with first column $(\tfrac16, \tfrac23, \tfrac16, 0)$ and the same other columns as $C^2$.

**A quadratic.** For $p = 2$ and $u = (0, 0, 0, 1, 2, 3, 3, 3)$:

$$C^1 = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & \tfrac12 \\ 0 & 0 & \tfrac12 \end{pmatrix}, \quad C^2 = \begin{pmatrix} \tfrac12 & 0 & 0 \\ \tfrac12 & 1 & \tfrac12 \\ 0 & 0 & \tfrac12 \end{pmatrix}, \quad C^3 = \begin{pmatrix} \tfrac12 & 0 & 0 \\ \tfrac12 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}.$$

With the control points $P = (0, 0), (1, 2), (3, 2), (4, 0), (5, 1)$, the Bezier points of element 2 are $(C^2)^T (P_2, P_3, P_4) = (2, 2), (3, 2), (\tfrac72, 1)$.

**Element routine.** At a quadrature point $s_q$ of element $e$ the code does:

1. take $B(s_q)$ and $B'(s_q)$ from a table built once for degree $p$;
2. form $N^e = C^e B$ and $\frac{dN^e}{ds} = C^e B'$, then the NURBS values with the weights;
3. map with the geometry, $x = (P^e)^T R^e$, and build the element matrix as for any finite element;
4. assemble with the connectivity array (IEN), the list of the global numbers $k - p, \ldots, k$ of the local functions.

## Variations

- **T-splines and other local refinement.** Scott, Borden, Verhoosel, Sederberg and Hughes (2011) extract [T-splines](/t-spline/): each blending function has its own local knot vectors, and the operator of an element is found by knot insertion into each function separately. The element operators are then rectangular in general, since the number of functions on an element is not fixed. The same idea is used for [hierarchical](/hierarchical-b-spline/) and [THB-splines](/truncated-hierarchical-b-spline/) and for [LR B-splines](/lr-b-spline/).
- **Global form.** All the blocks together are $A^T$, the transpose of the [knot refinement](/knot-refinement/) matrix to the Bezier knot vector. It can also be computed with the [Oslo algorithm](/oslo-algorithm/).
- **Inverse operators.** $(C^e)^{-1}$ maps Bernstein coefficients back to B-spline coefficients on one element. Bezier projection uses it to project a function element by element and then averages the results.
- **Lagrange extraction.** Instead of Bernstein polynomials, use the Lagrange polynomials of the element, so that an existing Lagrange element can be reused. The matrix is then $C^e$ times the change of basis from Bernstein to Lagrange.

## Pitfalls

- **Zero length elements.** Repeated knots make spans of zero length. They are not elements, and the algorithm skips them in L4. A code that numbers elements by knot index gets empty elements and wrong connectivity.
- **Discontinuous knots.** As written, the algorithm assumes interior multiplicity at most $p$, so the curve is $C^0$ at least. A knot of multiplicity $p + 1$ breaks the overlap in L12 and needs its own handling.
- **Parent domain.** $C^e$ is the same on $[0, 1]$ and $[-1, 1]$, but the derivative $dB/ds$ gets a factor $2$ on $[-1, 1]$, and the Jacobian of the map from the parent element to the element is $(u_{k+1} - u_k)/2$ instead of $u_{k+1} - u_k$. Mixing the two conventions gives wrong element matrices.
- **The weights are not in $C^e$.** For NURBS the weights enter in a separate step. The rational basis is not a linear combination of Bernstein polynomials with constant coefficients, so a code that uses $C^e B$ as the shape functions of a NURBS model computes with the wrong basis.
- **Storage.** For a uniform knot vector the interior elements have the same $C^e$. A code that stores one matrix per element can share them, which saves memory for large tensor product models.

## Exercises

1. Compute the extraction operators for $p = 2$ and $u = (0, 0, 0, 1, 1, 2, 2, 2)$. Explain why $C^1$ and $C^2$ are both identity matrices.
2. Prove that the first column of the operator of an interior element in a uniform cubic knot vector is $(\tfrac16, \tfrac23, \tfrac16, 0)$, the values of the uniform cubic B-splines at a knot.
3. Show that $\int_e N_a\,du = \frac{h_e}{p+1} \sum_j C^e_{aj}$, where $h_e$ is the length of the element. Use $\int_0^1 B_j\,ds = \frac{1}{p+1}$.
4. Write the extraction operator of a tensor product element with $p = q = 2$ on the knot vectors of the quadratic example in both directions, for the element $[1, 2] \times [1, 2]$. Check that its columns sum to 1.
5. For a circle written as a quadratic NURBS with 9 control points and knots $(0, 0, 0, \tfrac14, \tfrac14, \tfrac12, \tfrac12, \tfrac34, \tfrac34, 1, 1, 1)$, show that every $C^e$ is the identity, and explain why.

## References
