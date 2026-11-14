---
tag: JW5WMB
kind: definition
slug: algebraic-kernel
name: Algebraic kernel
aliases:
- kernel and cokernel
area: eda/logic-synthesis
level: core
summary: A cube-free quotient of a sum of products by a cube, its cokernel. Two expressions have a common divisor of two or more cubes only if a kernel of each shares two or more cubes with the other.
prereqs: [sum-of-products, algebraic-division]
see_also: [kernel-extraction, multi-level-logic-synthesis, boolean-network, implicant, cofactor, common-subexpression-elimination]
sources:
  - paper: "Robert K. Brayton and Curtis T. McMullen, The decomposition and factorization of Boolean expressions, Proceedings of the International Symposium on Circuits and Systems (ISCAS), 1982, pages 49 to 54"
    locator: the definitions of cube-free expressions, kernels, cokernels and kernel levels, and the theorem on common multi-cube divisors
  - paper: doi:10.1109/TCAD.1987.1270347
    title: Robert K. Brayton, Richard Rudell, Alberto Sangiovanni-Vincentelli and Albert R. Wang, MIS, a multiple-level logic optimization system, IEEE Transactions on Computer-Aided Design 6(6), 1987, pages 1062 to 1081
    locator: kernels as the candidate divisors of the factoring and extraction commands
  - paper: doi:10.1109/5.52213
    title: Robert K. Brayton, Gary D. Hachtel and Alberto L. Sangiovanni-Vincentelli, Multilevel logic synthesis, Proceedings of the IEEE 78(2), 1990, pages 264 to 300
    locator: the algebraic model, kernels and the kernel theorem
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 8, Multiple-Level Combinational Logic Optimization, the section on kernels and kernel sets
---

An algebraic kernel of a [sum of products](/sum-of-products/) $F$ is a quotient $F / c$ of [algebraic division](/algebraic-division/) by a cube $c$ that is cube-free: it has two or more cubes and no literal common to all of them. The cube $c$ is a cokernel of that kernel. Kernels are the divisors that algebraic synthesis tries, because Brayton and McMullen proved that two expressions have a common divisor of two or more cubes only if some kernel of the one and some kernel of the other share two or more cubes. [Kernel extraction](/kernel-extraction/) uses this to find shared logic in a [Boolean network](/boolean-network/).

## Definition

We use cubes and SOPs as sets of literals and sets of cubes, as on the [sum of products](/sum-of-products/) page, and the quotient $F / c = \{x \setminus c : x \in F, c \subseteq x\}$ of an SOP $F$ by a cube $c$.

**Cube-free.** An SOP $G$ is cube-free if $|G| \ge 2$ and $\bigcap_{x \in G} x = \emptyset$. Equivalently, the only cube $c$ with $G = \{c\} \cdot (G / c)$ is the constant cube 1. A single cube is never cube-free.

**Kernel.** A cube $c$ is a cokernel of $F$ if $F / c$ is cube-free, and then $K = F / c$ is a kernel of $F$. The kernel set is
$$\mathcal{K}(F) = \{F / c : c \text{ a cube}, F / c \text{ cube-free}\}.$$
If $F$ itself is cube-free, then $F \in \mathcal{K}(F)$ with cokernel 1. One kernel can have several cokernels.

**Levels.** A kernel $K$ has level 0 if $\mathcal{K}(K) = \{K\}$. It has level $n$ if it has a kernel of level $n - 1$ other than itself and no kernel of level $n$ or more other than itself. Level-0 kernels are the smallest units of the algebraic structure of $F$.

**Kernel theorem (Brayton and McMullen 1982).** For SOPs $F$ and $G$, there is an SOP $D$ with $|D| \ge 2$ that is an algebraic divisor of both, meaning $F / D \neq \emptyset$ and $G / D \neq \emptyset$, if and only if there are kernels $K_F \in \mathcal{K}(F)$ and $K_G \in \mathcal{K}(G)$ with $|K_F \cap K_G| \ge 2$.

*Proof.* If $|K_F \cap K_G| \ge 2$, let $D = K_F \cap K_G$ and let $c$ be a cokernel of $K_F$. The cubes of $K_F$ share no variable with $c$, so $c \cup d \in F$ for each $d \in D$, and $c \in F / D$. The same holds for $G$. For the other direction, let $D$ be a common divisor with $|D| \ge 2$, and let $e$ be the common cube of $D$. Then $D' = D / e$ is cube-free, and it is a common divisor too: if $q \in F / D$, then $q \cup e$ shares no variable with $D'$, since each cube of $D$ holds the literal of $e$ for each variable of $e$, and $(q \cup e) \cup d' = q \cup d \in F$. So we can take $D$ cube-free. Let $q \in F / D$. Every $d \in D$ is in $F / q$, because $q \cup d \in F$ and $q \cap d = \emptyset$. So $D \subseteq F / q$, and the common cube of $F / q$ lies inside the common cube of $D$, which is empty. So $F / q$ has at least two cubes and is cube-free, a kernel of $F$ that contains $D$. A kernel of $G$ that contains $D$ comes in the same way, and their intersection holds $D$. $\square$

## Examples and non-examples

**Kernels.**

- $F = ace + bce + de + g$. Its kernels are $a + b$ with cokernel $ce$, $ac + bc + d$ with cokernel $e$, and $F$ itself with cokernel 1. The cube $c$ is not a cokernel, since $F / c = ae + be$ has the common literal $e$.
- $F = ac + ad + bc + bd + e$ has the kernels $c + d$ with the two cokernels $a$ and $b$, $a + b$ with the cokernels $c$ and $d$, and $F$ itself. That makes 3 kernels and 5 cokernels.
- $F = adf + aef + bdf + bef + cdf + cef + g$ has the kernels $d + e$ (cokernels $af$, $bf$, $cf$), $a + b + c$ (cokernels $df$, $ef$), $ad + ae + bd + be + cd + ce$ (cokernel $f$), and $F$ (cokernel 1). The kernels $d + e$ and $a + b + c$ have level 0. The kernel with cokernel $f$ is the product $(a + b + c)(d + e)$ multiplied out, and has level 1. So $F$ itself, with a kernel of level 1 other than itself, has level 2.
- A product of $k$ sums of two literals each, $(a_1 + b_1)(a_2 + b_2) \cdots (a_k + b_k)$ multiplied out, has $2^k$ cubes. Its kernels are the products of the nonempty subsets of the factors, $2^k - 1$ of them. A cokernel picks a literal from each factor of a proper subset of the factors, so there are $\sum_{j < k} \binom{k}{j} 2^j = 3^k - 2^k$ cokernels. For $k = 4$ that is 15 kernels and 65 cokernels for an SOP of 16 cubes.

**The kernel theorem at work.**

- $F = ac + ad + bc + bd + e$ and $G = cf + df + g$ share the kernel $c + d$, so $c + d$ divides both: $F = (a + b)(c + d) + e$ and $G = f(c + d) + g$.
- $F = ax + bx + cx$ and $G = ay + by + dy$ have the kernels $a + b + c$ and $a + b + d$, which share the two cubes $a$ and $b$. So $a + b$ divides both, with $F = x(a + b) + cx$ and $G = y(a + b) + dy$.
- $F = ab + cd$ and $G = ac + bd$ have only themselves as kernels, and these share no cube, so no multi-cube algebraic divisor is common to them.

**Non-examples.**

- $ab + ac$ is not a kernel of itself, because $a$ is common to both cubes. Its only kernel is $b + c$, with cokernel $a$.
- A single cube such as $abc$ has no kernel, since every quotient of it by a cube is a single cube.
- $a + ab$ is not cube-free, since $a$ is in both cubes. The algebraic model treats it as written, even though as a function it equals $a$. Its kernel is $1 + b$ with cokernel $a$, because $F / a = \{\emptyset, \{b\}\}$ has two cubes and no common literal.
- For $F = abc + abd$, the quotient $F / a = bc + bd$ is not a kernel, since $b$ is common. The cokernel is $ab$, with kernel $c + d$.
- The theorem is about algebraic divisors only. $F = a + bc$ and $G = a + bd$ share the Boolean divisor $a + b$, since $F = (a + b)(a + c)$ and $G = (a + b)(a + d)$ as functions. Their kernels are $F$ and $G$, which share only the cube $a$, and indeed $a + b$ is not an algebraic divisor of either.

## Related definitions

- **[Algebraic division](/algebraic-division/).** The quotient $F / c$ by a cube is the special case of weak division with a divisor of one cube.
- **Kernel-cube matrix.** The table of [kernel extraction](/kernel-extraction/), with a row for each cokernel of each node and a column for each kernel cube. Rectangles of it are common divisors.
- **[Cofactor](/cofactor/).** The cofactor $F_a$ sets $a = 1$ and keeps the cubes without $a$. The quotient $F / a$ keeps only the cubes with $a$. A kernel is a quotient, not a cofactor.
- **[Implicant](/implicant/).** A cube of a two-level cover. Kernels are sums of cubes inside one expression and say nothing about the function's implicants.
- **[Common subexpression elimination](/common-subexpression-elimination/).** The compiler analogue of extracting shared divisors from expressions.

## References
