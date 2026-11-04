---
tag: 2VZSMS
kind: theorem
slug: ben-or-theorem
name: Ben-Or's theorem
aliases:
- Ben-Or lower bound
- Milnor-Thom connected components bound
area: foundations/lower-bounds
level: advanced
summary: An algebraic computation tree that decides a set W in R^n has height at least c1 log C - c2 n, where C is the number of connected components of W or of its complement.
prereqs: [algebraic-computation-tree, algebraic-decision-tree, decision-tree-model]
see_also: [element-distinctness-lower-bound, element-distinctness, linear-decision-tree, real-ram, reduction-lower-bound, counting-argument]
sources:
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80-86"
    locator: the main theorem on the height of algebraic computation trees, the bound on the components of a set defined by equations and inequalities, and the application to element distinctness
  - paper: doi:10.1090/S0002-9939-1964-0161339-9
    title: "John Milnor, On the Betti numbers of real varieties, Proceedings of the American Mathematical Society 15(2) (1964), 275-280"
    locator: Theorem 2 (the sum of the Betti numbers of a variety defined by equations of degree at most k in m variables is at most k(2k-1)^(m-1))
  - paper: doi:10.1016/0196-6774(82)90002-5
    title: "J. Michael Steele and Andrew C. Yao, Lower bounds for algebraic decision trees, Journal of Algorithms 3(1) (1982), 1-8"
    locator: the main theorem (algebraic decision trees of fixed degree)
  - paper: doi:10.1016/0022-0000(79)90054-0
    title: "David P. Dobkin and Richard J. Lipton, On the complexity of computations under varying sets of primitives, Journal of Computer and System Sciences 18(1) (1979), 86-91"
    locator: the component counting bound for linear decision trees
---

Ben-Or's theorem is a lower bound for the [algebraic computation tree](/algebraic-computation-tree/): a tree of height $h$ that decides a set $W \subseteq \mathbb{R}^n$ has $h \ge c_1 \lg C - c_2 n$, where $C$ is the number of connected components of $W$ or of its complement and $c_1, c_2 > 0$ are absolute constants. The tree may add, subtract, multiply, divide, take square roots and test signs, at unit cost each. The proof bounds the number of components of the inputs that reach one leaf by a theorem of Milnor on real algebraic sets. Ben-Or proved it in 1983, and it gives the $\Omega(n \log n)$ bound for [element distinctness](/element-distinctness-lower-bound/) and many problems of computational geometry.

## Statement

The model is the algebraic computation tree as defined on [its page](/algebraic-computation-tree/): computation nodes with one of $+, -, \times, \div, \sqrt{\ }$ on inputs, real constants and earlier values; branch nodes with a test $u > 0$, $u \ge 0$ or $u = 0$ on an earlier value $u$; leaves labelled accept or reject. The tree is *valid*: no input that reaches a division divides by zero, and no input that reaches a root takes the root of a negative number. The *height* $h$ is the largest number of computation and branch nodes on a path from the root to a leaf. This is the worst-case cost, with unit cost for each operation and each test.

For $S \subseteq \mathbb{R}^m$ write $\mathrm{cc}(S)$ for the number of connected components of $S$.

**Theorem (Ben-Or 1983).** Let $n \ge 1$, let $W \subseteq \mathbb{R}^n$, and let $T$ be a valid algebraic computation tree of height $h$ that decides $W$. Let $C = \mathrm{cc}(W)$ or $C = \mathrm{cc}(\mathbb{R}^n \setminus W)$. Then

$$C \le 2 \cdot 3^{\,n-1} \cdot 18^{\,h}, \qquad\text{so}\qquad h \ \ge\ \frac{\lg C - n \lg 3}{\lg 18}.$$

In particular $h = \Omega(\log C - n)$. The constants $1/\lg 18 \approx 0.24$ and $\lg 3/\lg 18 \approx 0.38$ come from the proof below; Ben-Or's paper states the bound with its own constants, and only the form $c_1 \lg C - c_2 n$ matters for the uses.

## In plain words

Picture all possible inputs as points in space. The inputs that the program accepts form a set, and this set can fall apart into separate pieces. The theorem says that a program that must tell apart many pieces must run for a long time.

The reason is that a short program cannot cut space into many pieces. Fix the answers to all the tests along one run. The inputs that give these answers are described by a short list of equations and inequalities of low degree. A classical theorem from algebraic geometry says that such a short list describes only a limited number of pieces. A short program has few runs, and each run covers few pieces. So the total number of pieces is small, unless the program is long.

## Proof

The proof has two lemmas about connected components, a lemma that counts the components of one leaf, and a sum over the leaves.

**Fact 1 (continuous images).** If $f : X \to Y$ is continuous and onto, then $\mathrm{cc}(Y) \le \mathrm{cc}(X)$. *Proof.* Take $k$ different components $Y_1, \ldots, Y_k$ of $Y$, pick $y_i \in Y_i$ and $x_i \in X$ with $f(x_i) = y_i$. If $x_i$ and $x_j$ with $i \ne j$ were in one component $K$ of $X$, then $f(K)$ would be a connected subset of $Y$ that holds $y_i$ and $y_j$, so $Y_i = Y_j$, which is false. So the $x_i$ lie in $k$ different components of $X$, and $k \le \mathrm{cc}(X)$. Since $k$ is any number of components of $Y$, $\mathrm{cc}(Y) \le \mathrm{cc}(X)$. $\square$

**Fact 2 (finite unions).** If $W = R_1 \cup \cdots \cup R_L$, then $\mathrm{cc}(W) \le \sum_\ell \mathrm{cc}(R_\ell)$. *Proof.* Take $k$ different components of $W$ and a point in each. Each point lies in some $R_\ell$ and in a component $K$ of $R_\ell$. The set $K$ is connected and lies in $W$, so it lies inside one component of $W$. So two of the chosen points that lie in different components of $W$ give different pairs $(\ell, K)$. Hence $k \le \sum_\ell \mathrm{cc}(R_\ell)$. $\square$

**Lemma 1 (Milnor 1964, Theorem 2).** Let $m \ge 1$ and $d \ge 1$. Let $f_1, \ldots, f_r \in \mathbb{R}[y_1, \ldots, y_m]$ have degree at most $d$, and let $V = \{y \in \mathbb{R}^m : f_1(y) = \cdots = f_r(y) = 0\}$. Then the sum of the Betti numbers of $V$ is at most $d(2d-1)^{m-1}$. In particular $\mathrm{cc}(V) \le d(2d-1)^{m-1}$.

The number of components is the zeroth Betti number, so it is at most the sum. For $r = 0$ the set is $\mathbb{R}^m$ with one component, and the bound holds. This page uses Lemma 1 without proof; Milnor's proof uses Morse theory.

**Lemma 2 (equations and inequalities).** Let $m \ge 1$, $d \ge 2$ and $0 \le s \le t$. Let $q_1, \ldots, q_r, p_1, \ldots, p_t \in \mathbb{R}[y_1, \ldots, y_m]$ have degree at most $d$, and let

$$S = \{y \in \mathbb{R}^m : q_i(y) = 0 \text{ for all } i,\ \ p_j(y) > 0 \text{ for } j \le s,\ \ p_j(y) \ge 0 \text{ for } s < j \le t\}.$$

Then $\mathrm{cc}(S) \le d(2d-1)^{m+t-1}$.

*Proof.* Take $k \ge 1$ different components of $S$ and a point $a_i$ in the $i$-th one. Let $\varepsilon = \min\{p_j(a_i) : 1 \le i \le k,\ 1 \le j \le s\}$, and let $\varepsilon = 1$ if $s = 0$. Then $\varepsilon > 0$, since each $p_j$ with $j \le s$ is positive on $S$. This is the step from strict to non-strict inequalities. Let

$$S_\varepsilon = \{y : q_i(y) = 0,\ p_j(y) \ge \varepsilon \ (j \le s),\ p_j(y) \ge 0 \ (s < j \le t)\}.$$

Then $S_\varepsilon \subseteq S$ and every $a_i \in S_\varepsilon$. Now add one variable $z_j$ for each inequality, and let $V \subseteq \mathbb{R}^{m+t}$ be the zero set of

$$q_i(y) \ (1 \le i \le r), \qquad p_j(y) - \varepsilon - z_j^2 \ (j \le s), \qquad p_j(y) - z_j^2 \ (s < j \le t).$$

Each of these polynomials has degree at most $\max(d, 2) = d$. The projection $\pi(y, z) = y$ maps $V$ onto $S_\varepsilon$: a point of $V$ has $p_j(y) = \varepsilon + z_j^2 \ge \varepsilon$ or $p_j(y) = z_j^2 \ge 0$, and a point $y \in S_\varepsilon$ lifts with $z_j = \sqrt{p_j(y) - \varepsilon}$ or $z_j = \sqrt{p_j(y)}$. Lift each $a_i$ to a point $b_i \in V$. If $b_i$ and $b_l$ with $i \ne l$ were in one component $K$ of $V$, then $\pi(K)$ would be a connected subset of $S_\varepsilon \subseteq S$ that holds $a_i$ and $a_l$, which contradicts the choice of the $a_i$. So $V$ has at least $k$ components, and Lemma 1 in $m + t$ variables gives $k \le d(2d-1)^{m+t-1}$. This holds for every finite $k$ not larger than $\mathrm{cc}(S)$, so $\mathrm{cc}(S) \le d(2d-1)^{m+t-1}$. $\square$

**Lemma 3 (one leaf).** Let $\lambda$ be a leaf of $T$, and let $R(\lambda) \subseteq \mathbb{R}^n$ be the set of inputs whose path ends at $\lambda$. Then $\mathrm{cc}(R(\lambda)) \le 2 \cdot 3^{\,n + 2h - 1}$.

*Proof.* Let the path to $\lambda$ have $c$ computation nodes and $b$ branch nodes, with $c + b \le h$. Give a new variable $v_i$ to the $i$-th computation node on the path. Each operand of a node is an input $x_k$, a constant, or an earlier $v_{i'}$, so it is a polynomial of degree at most 1 in the variables $(x, v) \in \mathbb{R}^{n+c}$. Write the conditions below.

- A node $v_i = u + w$, $v_i = u - w$ or $v_i = u w$ gives the equation $v_i - u - w = 0$, $v_i - u + w = 0$ or $v_i - uw = 0$.
- A node $v_i = u / w$ gives the equation $v_i w - u = 0$.
- A node $v_i = \sqrt{u}$ gives the equation $v_i^2 - u = 0$ and the inequality $v_i \ge 0$.
- A branch node that tests $u$ gives one condition, the one that the path takes: $u > 0$ or its negation $-u \ge 0$; $u \ge 0$ or its negation $-u > 0$; $u = 0$ (an equation) or its negation $u^2 > 0$.

Each polynomial has degree at most 2. Let $S_\lambda \subseteq \mathbb{R}^{n+c}$ be the set of points that satisfy all these conditions. It has the form of Lemma 2 with $d = 2$, $m = n + c$ and at most $t \le b + c$ inequalities, since each node gives at most one inequality.

*Claim: $R(\lambda) = \pi(S_\lambda)$, where $\pi(x, v) = x$.* If $x \in R(\lambda)$, let $v_i$ be the value that $T$ computes at the $i$-th computation node on input $x$. Every equation holds by the definition of the operation, a root is non-negative, and every branch condition holds because the path of $x$ takes these branches. So $(x, v) \in S_\lambda$. Conversely let $(x, v) \in S_\lambda$. We show by induction along the path that $x$ reaches each node of the path and that each $v_i$ equals the value that $T$ computes on $x$. The root is reached. At a computation node that $x$ reaches, the operands are true values by the induction hypothesis. For $+$, $-$ and $\times$ the equation fixes $v_i$ to the true value. For $u/w$ the tree is valid, so $w \ne 0$, and $v_i w = u$ gives $v_i = u/w$. For $\sqrt{u}$ the tree is valid, so $u \ge 0$, and $v_i^2 = u$ with $v_i \ge 0$ gives $v_i = \sqrt{u}$. At a branch node, the tested value is a true value, and the condition of $S_\lambda$ says that $x$ takes the branch of the path. So $x$ reaches $\lambda$, and $x \in R(\lambda)$.

By Fact 1 and Lemma 2, $\mathrm{cc}(R(\lambda)) \le \mathrm{cc}(S_\lambda) \le 2 \cdot 3^{\,n + c + t - 1}$. Since $c + t \le 2c + b \le 2h$, this is at most $2 \cdot 3^{\,n + 2h - 1}$. $\square$

**Proof of the theorem.** Every path has at most $h$ branch nodes, and only branch nodes have two children, so $T$ has at most $2^h$ leaves. The set $W$ is the union of $R(\lambda)$ over the accepting leaves, and $\mathbb{R}^n \setminus W$ is the union over the rejecting leaves. By Fact 2 and Lemma 3, in both cases

$$C \le 2^h \cdot 2 \cdot 3^{\,n + 2h - 1} = 2 \cdot 3^{\,n-1} \cdot 18^{\,h}.$$

Take $\lg$ of both sides: $\lg C \le 1 + (n-1)\lg 3 + h \lg 18 \le n \lg 3 + h \lg 18$, since $1 \le \lg 3$. This is the second form. $\square$

### A small example

Let $W = \{x \in \mathbb{R}^2 : x_1 x_2 > 0\}$, the union of two open quadrants, so $\mathrm{cc}(W) = 2$. The tree "$v_1 = x_1 \times x_2$, test $v_1 > 0$" decides $W$ with height 2. Its accepting leaf has $R(\lambda) = W$, which is not connected. So the argument of the [linear decision tree](/linear-decision-tree/), where each leaf gives one convex region, fails here, and the components must be counted. Lemma 3 uses $S_\lambda = \{(x_1, x_2, v_1) : v_1 - x_1 x_2 = 0,\ v_1 > 0\}$ with $m = 3$ and $t = 1$, and Lemma 2 bounds its components by $2 \cdot 3^3 = 54$. The true count is 2, so the constants are far from tight, but they are constants.

## Consequences

- **Element distinctness.** The set $\{x \in \mathbb{R}^n : x_i \ne x_j \text{ for all } i < j\}$ has $n!$ components, so every tree that decides it has height $\Omega(n \log n)$. The count, the exact numbers and the problems that follow by reduction are on the page [element distinctness lower bound](/element-distinctness-lower-bound/).
- **Algebraic decision trees.** For a fixed degree $d$, the same counting gives $h = \Omega(\log C - n)$ for an [algebraic decision tree](/algebraic-decision-tree/) of degree $d$, with constants that depend on $d$. This is the earlier result of Steele and Yao (1982).
- **Real RAM programs.** A program on the [real RAM](/real-ram/) with the operations of the tree, no floor function and no conversion of reals to addresses unrolls, for each input size, into a computation tree whose height is at most the worst-case running time. So the bound is a lower bound on the running time of such programs.
- **Reductions.** A cheap reduction inside the same model carries the bound to new problems. See [lower bounds by reduction](/reduction-lower-bound/).

### Pitfalls

- **The model.** The bound holds for trees with $+, -, \times, \div, \sqrt{\ }$ and sign tests. It does not hold for machines with a floor function, with indirect addressing by a real value, or with hashing of the input. For example, on a word RAM with integer keys, element distinctness takes $O(n)$ expected time with a hash table.
- **What is counted.** $C$ counts the connected components of the set $W$ itself (or of its complement), not the number of regions or cells of some arrangement. A set with many cells that merge into one connected set gets no bound.
- **What it says.** The theorem bounds the worst-case height of a deterministic tree that decides membership. It says nothing about the average height under a distribution, and nothing about randomized trees.
- **Small component counts.** If $C \le 3^n$ then the bound is at most zero. A set with $2^{O(n)}$ components gets at most an $O(n)$ bound from this theorem.

## Tightness

- **The form is tight for element distinctness.** Sorting with comparisons and testing neighbours decides the set of distinct inputs with $O(n \log n)$ nodes, which matches $\Omega(\log n!) = \Omega(n \log n)$.
- **The constants are not tight.** For element distinctness with $n = 100$, the theorem gives $h \ge 88$, while at least $\lceil \lg 100! \rceil = 525$ comparisons are needed in the [comparison model](/comparison-model/). For $n = 1000$ the bound is $h \ge 1666$, against $\lg 1000! \approx 8529.4$. The bound becomes positive only from $n = 7$ on.
- **The term in $n$.** The bound gives nothing when $\lg C$ is $O(n)$, and it cannot separate a hard set with few components from an easy one. Other methods are needed for such sets.

## History

Dobkin and Lipton (1979) counted the components of a set to get lower bounds for [linear decision trees](/linear-decision-tree/), where each leaf region is convex. Steele and Yao (1982) extended the count to algebraic decision trees of fixed degree by the bound of Milnor (1964) on the Betti numbers of a real algebraic set. Milnor notes in his paper that Thom obtained similar bounds. Ben-Or (STOC 1983) added the variables for the intermediate values, which lets the degree grow with the height, and so covered computation trees with division and square roots. His paper applies the theorem to element distinctness and to other problems.

## References
