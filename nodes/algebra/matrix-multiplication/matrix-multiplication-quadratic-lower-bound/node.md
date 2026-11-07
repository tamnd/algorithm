---
tag: 5FYZSV
kind: theorem
slug: matrix-multiplication-quadratic-lower-bound
name: Quadratic lower bound for matrix multiplication
aliases:
- Ω(n^2) lower bound
- trivial lower bound for matrix multiplication
- omega is at least 2
area: algebra/matrix-multiplication
level: intro
summary: Any algorithm for the product of two n by n matrices must read all 2n^2 input entries and needs at least n^2 operations and n^2 bilinear products, so ω is at least 2.
prereqs: [naive-matrix-multiplication, adversary-argument, trivial-lower-bound]
see_also: [matrix-multiplication-exponent, bilinear-complexity, tensor-rank, strassen-algorithm, lower-bound, counting-argument]
sources:
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer, Grundlehren der mathematischen Wissenschaften 315
    locator: Chapter 14 (multiplicative and bilinear complexity, the bound by the dimension of a flattening) and Chapter 17 (lower bounds for the complexity of algebras)
  - paper: doi:10.4086/toc.gs.2013.005
    title: Markus Bläser, Fast Matrix Multiplication, Theory of Computing Graduate Surveys 5, 2013
    locator: the sections on bilinear complexity and on lower bounds for the rank of matrix multiplication
  - paper: "Roger W. Brockett and David Dobkin, On the optimal evaluation of a set of bilinear forms, Linear Algebra and its Applications 19 (1978)"
    locator: pp. 207 to 235 (the bound 2n^2 − 1 for the rank of n by n matrix multiplication)
  - paper: "Markus Bläser, A 5/2 n^2 lower bound for the rank of n×n matrix multiplication over arbitrary fields, 40th IEEE Symposium on Foundations of Computer Science (FOCS 1999)"
    locator: pp. 45 to 50
  - paper: "Ran Raz, On the complexity of matrix product, SIAM Journal on Computing 32(5), 2003"
    locator: the main theorem (Ω(n^2 log n) for arithmetic circuits with bounded coefficients over the real or complex numbers)
  - paper: "J. M. Landsberg, New lower bounds for the rank of matrix multiplication, SIAM Journal on Computing 43(1), 2014"
    locator: the main theorem (a rank bound of the form 3n^2 − O(n^(3/2)))
  - paper: "Markus Bläser, On the complexity of the multiplication of matrices of small formats, Journal of Complexity 19(1), 2003"
    locator: pp. 43 to 60 (the rank of 3 by 3 matrix multiplication is at least 19)
---

The quadratic lower bound says that the product of two $n \times n$ matrices costs at least a constant times $n^2$ steps in every reasonable model: an algorithm must read all $2n^2$ input entries, a [straight-line program](/straight-line-program/) needs at least $n^2$ operations, and a bilinear algorithm needs at least $n^2$ products. So the [matrix multiplication exponent](/matrix-multiplication-exponent/) satisfies $\omega \ge 2$. This simple bound is still, up to constant factors, the best lower bound known for general algorithms, while the best upper bound is about $n^{2.37}$.

## Statement

Let $F$ be a field and $n \ge 1$. The input is a pair of $n \times n$ matrices $A$, $B$ over $F$, and the output is $C = AB$.

**Theorem.**

1. *(Input reading.)* Let a deterministic algorithm compute $AB$ for all inputs, where each step may read one input entry, and its later steps depend only on the values it has read. On the input with all entries equal to $1$, it reads all $2n^2$ entries. So on a [random access machine](/random-access-machine/) it takes at least $3n^2$ steps in the worst case (with $n^2$ writes for the output).
2. *(Straight-line programs.)* Let the entries of $A$ and $B$ be $2n^2$ distinct indeterminates. Each straight-line program over $F$ that uses the operations $+$, $-$, $\times$, $\div$ and constants from $F$, and that computes the $n^2$ entries $c_{ij} = \sum_k a_{ik} b_{kj}$, has at least $n^2$ operation steps.
3. *(Bilinear algorithms.)* Let a bilinear algorithm compute $AB$ with $r$ products: there are linear forms $u_\ell$ in the entries of $A$, $v_\ell$ in the entries of $B$, and matrices $W_\ell \in F^{n \times n}$ with $AB = \sum_{\ell=1}^{r} u_\ell(A)\, v_\ell(B)\, W_\ell$ for all $A$, $B$. Then $r \ge n^2$. In the language of [tensor rank](/tensor-rank/), the rank of the [matrix multiplication tensor](/matrix-multiplication-tensor/) $\langle n, n, n \rangle$ is at least $n^2$.

**Corollary.** $MM(n) \ge n^2$ for all $n \ge 1$, so $\omega \ge 2$.

## In plain words

The answer has as many cells as each input, and each cell of the answer depends on a full row of the first input and a full column of the second. If a method skips one input number, an adversary can change that number, which changes the answer, while the method still gives the same output. So a method must look at every input number and write every output number. In the algebra model, each answer cell is a new value that needs its own step. A third argument counts products: a method that uses too few products cannot even get back the first matrix when the second one is the identity.

## Proof

**Part 1.** Let $J$ be the input with all $2n^2$ entries equal to $1$. Assume that on $J$ the algorithm does not read the entry $a_{ik}$. Let $J'$ be the same input with $a_{ik} = 0$. The algorithm reads the same values on $J$ and $J'$ (it never reads $a_{ik}$), so it does the same steps and gives the same output. But $(J\text{'s } C)_{ij} - (J'\text{'s } C)_{ij} = (1 - 0) \cdot b_{kj} = 1 \ne 0$, so the output is wrong on one of them. This contradicts correctness. The same argument with $b_{kj}$ changed to $0$ changes $c_{ij}$ by $a_{ik} = 1$. So the algorithm reads all $2n^2$ entries on $J$. It also writes the $n^2$ entries of the output, and each read or write is a step.

**Part 2.** A straight-line program is a sequence of values. Each value is an input indeterminate, a constant of $F$, or the result of one operation on two earlier values. Each output is one of these values. The entry $c_{ij}$ is a polynomial of degree $2$, so it is not an input indeterminate (degree $1$) and not a constant (degree $0$). So $c_{ij}$ is the result of an operation step. Two different entries $c_{ij} \ne c_{i'j'}$ are different polynomials, since $c_{ij}$ holds the monomial $a_{i0} b_{0j}$ and $c_{i'j'}$ does not when $(i, j) \ne (i', j')$. One step gives one value, so the $n^2$ outputs need $n^2$ distinct steps.

**Part 3.** For each matrix $A$, let $L_A$ be the linear map $B \mapsto AB$ on $F^{n \times n}$. The map $\varphi : A \mapsto L_A$ is linear in $A$, and it is injective: if $L_A = 0$ then $A = A \cdot I = L_A(I) = 0$. So the image of $\varphi$ is a vector space of dimension $n^2$. By the bilinear identity, for each $A$,

$$L_A(B) = \sum_{\ell=1}^{r} u_\ell(A)\, \big( v_\ell(B)\, W_\ell \big), \quad\text{so}\quad L_A = \sum_{\ell=1}^{r} u_\ell(A)\, M_\ell,$$

where $M_\ell$ is the fixed linear map $B \mapsto v_\ell(B)\, W_\ell$. So each $L_A$ is in the span of the $r$ maps $M_1, \ldots, M_r$, and $n^2 = \dim \varphi(F^{n \times n}) \le r$.

**Corollary.** By Part 2, every algorithm in the algebraic model has $MM(n) \ge n^2$. If $MM(n) = O(n^{\tau})$ for some $\tau < 2$, then $n^2 \le c\, n^{\tau}$ for all large $n$, which is false. So each $\tau$ with $MM(n) = O(n^\tau)$ has $\tau \ge 2$, and $\omega \ge 2$. $\blacksquare$

## Consequences

- **The exponent.** $2 \le \omega$. The upper bound is $\omega < 2.371552$ (Vassilevska Williams, Xu, Xu and Zhou, 2024), see the [matrix multiplication exponent](/matrix-multiplication-exponent/). Whether $\omega = 2$ is open.
- **Optimal methods for related problems.** [Matrix-vector multiplication](/matrix-vector-multiplication/) needs $\Omega(n^2)$ by the same reading argument, and the obvious method meets it. So matrix-vector multiplication is solved, and only the matrix-matrix case is open.
- **Problems equivalent to multiplication.** Since inversion, determinant and LUP factorization have the same exponent as multiplication (see [inversion equivalence](/matrix-multiplication-inversion-equivalence/)), each of them also has exponent at least $2$.

## Tightness

The three bounds are far from the best known upper bounds, and the true answer is open.

- **Rank.** The rank of $\langle n, n, n \rangle$ is at least $2n^2 - 1$ (Brockett and Dobkin, 1978), at least $\tfrac{5}{2} n^2 - 3n$ (Bläser, 1999), and at least $3n^2 - O(n^{3/2})$ (Landsberg, 2014). For $n = 2$ the rank is exactly $7$, while Part 3 gives only $4$. For $n = 3$ the rank is between $19$ (Bläser, 2003) and $23$ ([Laderman](/laderman-algorithm/), 1976).
- **Total operations.** No lower bound of the form $\Omega(n^{2+\varepsilon})$, or even $\omega(n^2)$, is known for general arithmetic circuits. Raz proved $\Omega(n^2 \log n)$ for circuits over $\mathbb{R}$ or $\mathbb{C}$ whose constants have bounded absolute value.
- **Input reading.** Part 1 is tight for checking a product with randomness: [Freivalds' algorithm](/freivalds-algorithm/) verifies $AB = C$ in $O(n^2)$ time with one-sided error. So the hard part is computing the product, not reading it.

## History

The bound by input size is folklore and appears in the first studies of the algebraic complexity of matrix multiplication. The rank bound $2n^2 - 1$ is due to Brockett and Dobkin (1978). Bläser raised it to $\tfrac{5}{2} n^2 - 3n$ in 1999, and Landsberg and others to $3n^2 - o(n^2)$ in the 2010s. Raz gave the $\Omega(n^2 \log n)$ bound for bounded-coefficient circuits in 2002.

## References
