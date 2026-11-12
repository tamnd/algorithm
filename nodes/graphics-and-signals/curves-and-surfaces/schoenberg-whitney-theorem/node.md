---
tag: 2RQ3DJ
kind: theorem
slug: schoenberg-whitney-theorem
name: Schoenberg-Whitney theorem
aliases:
- Schoenberg-Whitney condition
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The B-spline collocation matrix (N_j(τ_i)) for sites τ_0 < ... < τ_n is nonsingular exactly when N_i(τ_i) ≠ 0 for every i, that is, when each site lies inside the support of its own B-spline.
prereqs: [b-spline, determinant, curry-schoenberg-theorem]
see_also: [cubic-spline-interpolation, interpolation-problem, curve-interpolation, b-spline-fitting, collocation-method, banded-matrix, gaussian-elimination, knot-vector]
sources:
  - paper: doi:10.1090/S0002-9947-1953-0053177-X
    title: I. J. Schoenberg and Anne Whitney, On Pólya frequence functions III, the positivity of translation determinants with an application to the interpolation problem by spline curves, Transactions of the American Mathematical Society 74 (1953), 246 to 259
    locator: the application to interpolation by spline curves
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter XIII, Spline interpolation (the Schoenberg-Whitney theorem, total positivity of the collocation matrix and the routine SPLINT)
  - paper: doi:10.1512/iumj.1976.25.25043
    title: Carl de Boor, Total positivity of the spline collocation matrix, Indiana University Mathematics Journal 25(6) (1976), 541 to 551
    locator: all minors of (N_j(τ_i)) are nonnegative
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 9.2, Global interpolation (the choice of parameters and of knots by averaging)
---

The Schoenberg-Whitney theorem decides when interpolation by [B-splines](/b-spline/) is well posed. Take a degree $p$, a [knot vector](/knot-vector/) with $n + 1$ B-splines $N_0, \ldots, N_n$, and $n + 1$ sites $\tau_0 < \cdots < \tau_n$. The collocation matrix $A = (N_j(\tau_i))$ is nonsingular if and only if every diagonal entry $N_i(\tau_i)$ is nonzero, that is, if and only if the $i$-th site lies in the support of the $i$-th B-spline. So the question "does the interpolation problem have exactly one solution?" has an answer that you can check with $n + 1$ comparisons, without computing a [determinant](/determinant/). The [Curry-Schoenberg theorem](/curry-schoenberg-theorem/) gives the number of conditions; this theorem says where they can be put.

## Statement

Let $p \ge 0$, $n \ge 0$ and $t_0 \le \cdots \le t_{n+p+1}$ with $t_i < t_{i+p+1}$ for $0 \le i \le n$, so that no $N_i = N_{i,p}$ is identically zero. The B-splines come from the [Cox-de Boor recursion](/cox-de-boor-recursion/) with half-open spans, so they are continuous from the right. Let $\tau_0 < \tau_1 < \cdots < \tau_n$ be real numbers, the sites, and let $A$ be the $(n + 1) \times (n + 1)$ matrix with the entries $A_{ij} = N_j(\tau_i)$.

**Theorem.**

1. $A$ is nonsingular if and only if $N_i(\tau_i) \ne 0$ for $0 \le i \le n$.
2. $N_i(\tau_i) \ne 0$ if and only if $t_i < \tau_i < t_{i+p+1}$, or $\tau_i = t_i = t_{i+p}$.
3. The same holds with the closing rule at a clamped right end: if $t_{n+1} = t_{n+p+1}$ and $\tau_n = t_{n+1}$, and the row of $\tau_n$ holds the limits from the left, then $N_n(\tau_n) = 1$ and part 1 is true as stated.

The second case of part 2 is a site at a knot of multiplicity $p + 1$ that starts the support of $N_i$, as at the left end of a clamped knot vector, where $N_0(t_0) = 1$. In the usual interpolation problem the knot vector is clamped, the sites lie in $[t_p, t_{n+1}]$, and $\tau_0 = t_p$ and $\tau_n = t_{n+1}$ are allowed by parts 2 and 3.

For values $y_0, \ldots, y_n$ the theorem says: there is exactly one spline $s = \sum_j c_j N_j$ with $s(\tau_i) = y_i$ for all $i$ if and only if each site lies in the support of its own B-spline.

## In plain words

Each B-spline is nonzero only on a short stretch of the parameter line, and the stretches move to the right as the index grows. To interpolate, you pick one data site for each B-spline. Sort the sites and the B-splines from left to right and pair them in order. The theorem says the interpolation problem has exactly one solution when each site falls inside the stretch of its partner, and it has no unique solution as soon as one site falls outside. If too many sites crowd to the left, some B-splines on the right are never seen, and if too few sites are on the left, the B-splines there are asked to satisfy more conditions than they can. Nothing else can go wrong: the position of the sites inside their stretches does not matter for solvability, only for how well the problem is conditioned.

## Proof

The full proof is in [the proof of the Schoenberg-Whitney theorem](proofs/main.md). Its parts are these.

- **The value at the start of a support.** If $t_i = \tau < t_{i+p}$, then $N_{i,p}(\tau) = 0$, by induction on the degree: the left weight of the recursion is $0$ at $\tau = t_i$. If $t_i = t_{i+p} < t_{i+p+1}$, then $N_{i,p} = 1$ at $t_i$. Together with the positivity of $N_i$ inside its support, this gives part 2.
- **Necessity.** Suppose $N_k(\tau_k) = 0$. If $\tau_k \ge t_{k+p+1}$, the $k + 1$ columns $0, \ldots, k$ are zero in the rows $k, \ldots, n$, so they live in a space of dimension $k$ and are dependent. If $\tau_k \le t_k$, the $k + 1$ rows $0, \ldots, k$ are zero in the columns $k, \ldots, n$, and they are dependent for the same reason.
- **Sufficiency.** A site with $\tau_i = t_i = t_{i+p}$ makes row $i$ a unit row and splits $A$ into two smaller blocks of the same kind. For the other case the proof shows a stronger fact by induction on the degree: if a spline $g = \sum_j d_j N_j$ changes sign weakly, $g(\sigma_i^-) \, g(\sigma_i^+) \le 0$, at sites with $t_i < \sigma_i < t_{i+p+1}$, then $g = 0$. If a site sits too far left or right, say $\sigma_{i-1} < t_i$ or $\sigma_i > t_{i+p}$, the problem splits into two smaller ones. Otherwise $g$ is continuous on the sites, a weak form of Rolle's theorem puts a weak sign change of $g'$ between each two sites, and these points satisfy the condition for the B-splines of degree $p - 1$ that express $g'$, with the coefficients $p (d_j - d_{j-1})/(t_{j+p} - t_j)$. By induction they are $0$, so all $d_j$ are equal, and $g(\sigma_0) = 0$ with $N_0(\sigma_0) > 0$ gives $d_j = 0$.

## Consequences

- **Banded systems.** If the condition holds, then $A_{ij} = 0$ for $|i - j| > p$: a site in the support of $N_i$ is outside the supports of $N_j$ for $j \ge i + p + 1$ and $j \le i - p - 1$. So $A$ is a [banded matrix](/banded-matrix/) with $p$ diagonals on each side, and [Gaussian elimination](/gaussian-elimination/) solves the interpolation problem in $O(n p^2)$ operations.
- **No pivoting.** De Boor proved in 1976 that all minors of the collocation matrix are nonnegative. For such totally positive matrices, elimination without row exchanges is safe, and de Boor's routine SPLINT in A Practical Guide to Splines factors the band without pivoting.
- **Greville sites.** For a clamped knot vector with interior multiplicities at most $p$, the Greville abscissae $\tau_i = (t_{i+1} + \cdots + t_{i+p})/p$ are strictly increasing and always satisfy the condition, with $\tau_0 = t_0$ and $\tau_n = t_{n+1}$ under part 3. So interpolation at these sites is always well posed.
- **Knots by averaging.** In global curve interpolation the parameters $u_0 < \cdots < u_n$ come first, and The NURBS Book chooses the inner knots $t_{j+p} = (u_j + \cdots + u_{j+p-1})/p$. Then $t_k$ is an average of parameters below $u_k$ and $t_{k+p+1}$ is an average of parameters above $u_k$, so $t_k < u_k < t_{k+p+1}$ wherever these knots are inner knots, and the end sites $u_0 = t_0$ and $u_n = t_{n+1}$ are allowed by parts 2 and 3. So and [curve interpolation](/curve-interpolation/) with these knots always has a unique solution.
- **Least squares.** For [B-spline fitting](/b-spline-fitting/) to $N > n + 1$ distinct sites, the observation matrix has full column rank if and only if some $n + 1$ of the sites, in increasing order, satisfy the condition, because full column rank means that some $(n + 1) \times (n + 1)$ submatrix is nonsingular. Then the normal equations have a unique solution.
- **Collocation.** The same matrix appears in [collocation methods](/collocation-method/) for differential equations with spline trial functions, and the theorem tells which collocation points are allowed.

**Example.** Take $p = 2$ and the clamped knots $t = (0, 0, 0, 1, 2, 3, 3, 3)$, so $n = 4$. The supports are $N_0$ on $[0, 1)$, $N_1$ on $[0, 2)$, $N_2$ on $[0, 3)$, $N_3$ on $[1, 3)$ and $N_4$ on $[2, 3)$, with the closing rule at $3$. For the Greville sites $0, 1/2, 3/2, 5/2, 3$ the matrix is

$$A = \begin{pmatrix} 1 & 0 & 0 & 0 & 0 \\ 1/4 & 5/8 & 1/8 & 0 & 0 \\ 0 & 1/8 & 3/4 & 1/8 & 0 \\ 0 & 0 & 1/8 & 5/8 & 1/4 \\ 0 & 0 & 0 & 0 & 1 \end{pmatrix}, \qquad \det A = \frac{35}{128}.$$

| Sites $\tau_0, \ldots, \tau_4$ | The failing condition | $\det A$ |
|---|---|---|
| $0, 1/2, 3/2, 5/2, 3$ | none | $35/128$ |
| $0, 1, 2, 5/2, 3$ | none | $1/8$ |
| $0, 1/4, 1/2, 3/4, 3$ | $\tau_3 = 3/4 \le t_3 = 1$ | $0$ |
| $0, 1/2, 1, 3/2, 2$ | $\tau_4 = 2 = t_4$, but $t_4 < t_6$ | $0$ |

In the third row four sites lie in $[0, 1)$, where only the three B-splines $N_0, N_1, N_2$ are nonzero, so four rows live in a space of dimension three. In the fourth row no site is in $(2, 3]$, and $N_4$ is $0$ at every site, so its column is zero. All values were computed exactly, and a test over 3000 random knot vectors and sites, without the closing rule, found the determinant nonzero exactly when the diagonal was nonzero.

## Tightness

- **Distinct sites.** The statement needs $\tau_0 < \cdots < \tau_n$. Two equal sites give two equal rows. Repeated sites belong to Hermite interpolation, where a repeated site carries a derivative condition, and the matrix has rows of derivatives.
- **The pairing is fixed.** The condition pairs the $i$-th smallest site with $N_i$. It is not enough that every site lies in some support, or that every support contains some site: in the third row of the table every site lies in the support of $N_0$, $N_1$ or $N_2$.
- **Solvable is not well conditioned.** The condition is open, and the determinant goes to $0$ at its boundary. For the knots of the example and the sites $0, 1/4, 1/2, 1 + \varepsilon, 3$, the determinant is $\varepsilon^2/64$: $1/256$ for $\varepsilon = 1/2$ and $1/64000000$ for $\varepsilon = 1/1000$. A site that is almost at the end of its support gives an almost singular system.
- **The left end of a support.** A site exactly at $t_i$ is allowed only when $t_i = t_{i+p}$. For a simple knot the B-spline is continuous and $0$ there, so the site sees nothing of it.

## History

Schoenberg and Anne Whitney announced the result in a note in the Comptes Rendus in 1949 and published it in 1953, as part III of the series On Pólya frequency functions. They obtained it from the positivity of translation determinants of these functions and applied it to the interpolation problem by spline curves. De Boor proved in 1976 that the B-spline collocation matrix is totally positive, and A Practical Guide to Splines states the theorem for B-splines with arbitrary knots and uses it for its interpolation routine.

## References
