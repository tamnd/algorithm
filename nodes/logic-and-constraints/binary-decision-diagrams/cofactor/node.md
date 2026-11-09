---
tag: D053GJ
kind: definition
slug: cofactor
name: Cofactor
aliases:
- restriction
- Shannon cofactor
- positive cofactor
- negative cofactor
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: The function obtained from f by fixing one variable to 0 or 1.
prereqs: [boolean-function]
see_also: [shannon-expansion, reduced-ordered-bdd, bdd-quantification, bdd-compose, generalized-cofactor, boolean-function-composition, bdd-apply]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 1.1, Notation (the restriction f|x_i=b, "sometimes termed a cofactor", and the dependency set), and Section 4.4, Restriction
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (subfunctions and the beads of a function)
  - book: isbn:9780521847513
    title: Yves Crama and Peter L. Hammer, Boolean Functions, Theory, Algorithms, and Applications, Cambridge University Press, 2011
    locator: Chapter 1, Fundamental concepts and applications (restrictions of Boolean functions)
---

The cofactor of a [Boolean function](/boolean-function/) $f$ by a variable $x_i$ and a bit $b$ is the function $f|_{x_i=b}$ that we get when we fix $x_i$ to $b$. The two cofactors $f|_{x_i=0}$ and $f|_{x_i=1}$ are the two halves of the [Shannon expansion](/shannon-expansion/), and in a [binary decision diagram](/binary-decision-diagram/) they are the two children of a node that tests $x_i$. Bryant calls the cofactor a restriction, and the operation that computes it on a [reduced ordered BDD](/reduced-ordered-bdd/) takes time linear in the size of the BDD.

## Definition

Let $f \in B_n$, let $1 \le i \le n$ and let $b \in \{0,1\}$. The **cofactor** (or **restriction**) of $f$ by $x_i = b$ is the function

$$f|_{x_i=b}(x_1, \ldots, x_n) = f(x_1, \ldots, x_{i-1}, b, x_{i+1}, \ldots, x_n).$$

It is again in $B_n$, and it does not depend on $x_i$. Many texts drop the unused variable and see it as a function in $B_{n-1}$; the two views give the same results. $f|_{x_i=1}$ is the **positive cofactor**, also written $f_{x_i}$, and $f|_{x_i=0}$ is the **negative cofactor**, also written $f_{\bar{x}_i}$.

For a partial assignment (a **cube**) $c = (x_{i_1} = b_1, \ldots, x_{i_k} = b_k)$ with distinct indices, the cofactor $f|_c$ fixes all of them at once. By the first property below, the order in which we fix them does not change the result.

**Properties.** Let $f, g \in B_n$, let $\circ$ be a binary operator applied pointwise, and let $i \neq j$.

1. $(f|_{x_i=b})|_{x_j=c} = (f|_{x_j=c})|_{x_i=b}$. Both sides are $f$ with the $i$-th argument set to $b$ and the $j$-th argument set to $c$.
2. $(f \circ g)|_{x_i=b} = f|_{x_i=b} \circ g|_{x_i=b}$, and $(\neg f)|_{x_i=b} = \neg (f|_{x_i=b})$. At each input $x$, both sides evaluate $f$ and $g$ at the same point, the point $x$ with $x_i$ replaced by $b$.
3. $f$ depends on $x_i$ if and only if $f|_{x_i=0} \neq f|_{x_i=1}$. If $f(x) \ne f(x')$ for two inputs that differ only in $x_i$, then at that point one cofactor gives $f(x)$ and the other gives $f(x')$. Conversely, if the cofactors differ at some $x$, the two inputs $x$ with $x_i = 0$ and $x$ with $x_i = 1$ differ only in $x_i$ and give different values.
4. If $f$ does not depend on $x_i$, then $f|_{x_i=0} = f|_{x_i=1} = f$.

The **Boolean difference** $\partial f / \partial x_i = f|_{x_i=0} \oplus f|_{x_i=1}$ is 1 exactly at the inputs where a change of $x_i$ changes $f$. By property 3, $f$ depends on $x_i$ if and only if $\partial f / \partial x_i \ne 0$.

**On a BDD.** Property 2 is the reason that [APPLY](/bdd-apply/) and [ITE](/ite-operator/) can work on the cofactors one variable at a time. In an [ordered BDD](/ordered-binary-decision-diagram/) with order $x_1 < \cdots < x_n$, let the root $u$ of $f$ test $x_k$. Then:

- if $i < k$, then $f$ does not depend on $x_i$ and $f|_{x_i=b}$ is $u$ itself;
- if $i = k$, then $f|_{x_i=0}$ is the low child and $f|_{x_i=1}$ is the high child, found in $O(1)$ time;
- if $i > k$, the operation RESTRICT of the [reduced ordered BDD](/reduced-ordered-bdd/) page computes it. It visits each node at most once, so it takes $O(|f|)$ time, and the result has at most $|f|$ nodes.

## Examples and non-examples

**Majority.** Let $f = \mathrm{MAJ}(x_1, x_2, x_3) = x_1 x_2 \vee x_1 x_3 \vee x_2 x_3$. Then

$$f|_{x_1=1} = x_2 \vee x_3 \vee x_2 x_3 = x_2 \vee x_3, \qquad f|_{x_1=0} = x_2 x_3.$$

The Boolean difference is $(x_2 \vee x_3) \oplus x_2 x_3 = x_2 \oplus x_3$. So $x_1$ decides the vote exactly when the other two votes differ. The cofactor by the cube $(x_1 = 1, x_2 = 0)$ is $x_3$.

**A variable that does not matter.** For $f = x_1 \vee x_1 x_2$, both cofactors by $x_2$ equal $x_1$. So $f$ does not depend on $x_2$, and its reduced ordered BDD has no node labelled $x_2$.

**On a BDD.** The reduced ordered BDD of $f = x_1 x_2 \vee x_3$ with the order $x_1 < x_2 < x_3$ has a root that tests $x_1$, a node that tests $x_2$, a node that tests $x_3$, and the two terminals. The cofactor $f|_{x_1=0} = x_3$ is the low child of the root. The cofactor $f|_{x_2=1} = x_1 \vee x_3$ is not a node of this BDD; RESTRICT builds it as a new node $(x_1, \text{low} = x_3, \text{high} = 1)$.

**Non-examples.**

- Putting another variable or a function in place of $x_i$, for example $f|_{x_i = x_j}$, is not a cofactor. It is [composition](/boolean-function-composition/), computed on BDDs by [BDD compose](/bdd-compose/).
- $\exists x_i\, f = f|_{x_i=0} \vee f|_{x_i=1}$ is not a cofactor. It is built from both cofactors; see [BDD quantification](/bdd-quantification/).
- The **generalized cofactor** $f \downarrow c$ by a function $c$ (for example the constrain operator) is a different operation: it only has to agree with $f$ where $c = 1$, and it is not a restriction to a fixed value. See [generalized cofactor](/generalized-cofactor/).

## Related definitions

- [Shannon expansion](/shannon-expansion/): $f = (\neg x_i \wedge f|_{x_i=0}) \vee (x_i \wedge f|_{x_i=1})$.
- [Boolean function](/boolean-function/): essential variables and the support are defined by cofactors.
- [Generalized cofactor](/generalized-cofactor/): cofactors with respect to a care set.
- [BDD quantification](/bdd-quantification/): $\exists$ and $\forall$ as the OR and the AND of the two cofactors.
- [BDD compose](/bdd-compose/): $f|_{x_i=g} = (g \wedge f|_{x_i=1}) \vee (\neg g \wedge f|_{x_i=0})$.

## References
