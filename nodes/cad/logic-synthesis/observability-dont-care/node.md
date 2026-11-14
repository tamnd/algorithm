---
tag: TPSGJ3
kind: definition
slug: observability-dont-care
name: Observability don't-care
aliases:
- ODC
area: cad/logic-synthesis
level: advanced
summary: The input conditions under which the value of an internal node cannot be seen at any output, so its function may change there.
prereqs: [dont-care-condition, boolean-network, cofactor]
see_also: [dont-care-condition, multi-level-logic-synthesis, two-level-logic-minimization, espresso, dont-care-minimization, shannon-expansion, boolean-equivalence-checking]
sources:
  - paper: "Hamid Savoj and Robert K. Brayton, The use of observability and external don't cares for the simplification of multi-level networks, Proceedings of the 27th Design Automation Conference (DAC), 1990, pages 297 to 301"
    title: The use of observability and external don't cares for the simplification of multi-level networks
    locator: observability don't cares of the nodes of a network, the computation of subsets of them, and compatible don't cares for several nodes
  - paper: doi:10.1109/5.52213
    title: Robert K. Brayton, Gary D. Hachtel and Alberto L. Sangiovanni-Vincentelli, Multilevel logic synthesis, Proceedings of the IEEE 78(2), 1990, pages 264 to 300
    locator: the don't cares of a node in a Boolean network, satisfiability and observability don't cares, and node simplification
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 8, Multiple-Level Combinational Logic Optimization, the sections on don't care conditions in multiple-level networks
---

An observability don't-care of a node in a [Boolean network](/boolean-network/) is an input vector of the network at which the value of the node cannot change any primary output. At such a vector, the other inputs of the gates after the node block its value. For example, if a node $y$ only feeds the AND gate $z = y \bar{a}$, then every vector with $a = 1$ hides $y$. The set of these vectors, the ODC of the node, is a [don't-care condition](/dont-care-condition/) that the rest of the circuit gives to the node: the node may compute any function that agrees with its own on the other vectors, and the outputs stay the same. Synthesis uses this freedom to make the local function of the node smaller. The set is the complement of a Boolean difference, which is easy to write and expensive to compute for a large network, and the ODCs of two nodes cannot in general be used at the same time.

## Definition

Let $N$ be a Boolean network with primary inputs $x = (x_1, \ldots, x_n)$, primary outputs $z_1, \ldots, z_m$, and an internal node $y$ with global function $g_y$. Let $N_y$ be the network in which the output of $y$ is cut from $y$ and driven by a new primary input $s$. In $N_y$, each output is a function $z_j(x, s)$.

**Boolean difference.** For a function $F(x, s)$, the Boolean difference with respect to $s$ is
$$\frac{\partial F}{\partial s} = F|_{s = 0} \oplus F|_{s = 1},$$
the exclusive OR of the two [cofactors](/cofactor/). It is 1 at $x$ exactly when the value of $s$ changes $F$ at $x$.

**Observability don't-care.** The ODC of $y$ for output $z_j$ and the ODC of $y$ are
$$\mathrm{ODC}_j(y) = \Big\{x : \frac{\partial z_j}{\partial s}(x) = 0\Big\}, \qquad \mathrm{ODC}(y) = \bigcap_{j = 1}^m \mathrm{ODC}_j(y).$$
As a function, $\mathrm{ODC}(y) = \prod_j \overline{\partial z_j / \partial s}$. If output $z_j$ has its own external don't-care set $E_j$, then $\mathrm{ODC}_j(y)$ also contains $E_j$.

**The freedom of one node (exact).** Let $h : \{0,1\}^n \to \{0,1\}$. Changing $y$ so that its global function becomes $h$, with new fanins that are not in the transitive fanout of $y$, keeps every primary output function if and only if
$$h(x) = g_y(x) \quad \text{for every } x \notin \mathrm{ODC}(y).$$
*Proof.* Nodes outside the transitive fanout of $y$ keep their global functions, so after the change each output is $z_j(x, h(x))$, with the same function $z_j(x, s)$ of $N_y$. Fix $x$. If $h(x) = g_y(x)$, then $z_j(x, h(x)) = z_j(x, g_y(x))$ for all $j$. If $h(x) \ne g_y(x)$, the two values of $s$ are both used, and all outputs agree at $x$ exactly when $\partial z_j / \partial s (x) = 0$ for every $j$, that is, when $x \in \mathrm{ODC}(y)$. So the outputs are unchanged at every $x$ exactly when $h$ and $g_y$ differ only inside $\mathrm{ODC}(y)$. $\square$

So the realizations of $y$ form the interval of functions between $g_y \cdot \overline{\mathrm{ODC}(y)}$ and $g_y + \mathrm{ODC}(y)$, as on the [don't-care condition](/dont-care-condition/) page.

**Local form.** A minimizer works on the local function $f_y$ over the fanins $u_1, \ldots, u_k$, not on $g_y$. Let $\phi(x) = (g_{u_1}(x), \ldots, g_{u_k}(x))$. The local don't-care set is
$$D_{\mathrm{loc}}(y) = \{w \in \{0,1\}^k : \phi(x) = w \Rightarrow x \in \mathrm{ODC}(y) \text{ for all } x\}.$$
It holds the fanin values that never occur, the satisfiability don't-cares, and the values whose every preimage is hidden. Any $f'$ that equals $f_y$ outside $D_{\mathrm{loc}}(y)$ is a safe replacement: by the freedom above, the global function changes only at vectors $x$ with $\phi(x) \in D_{\mathrm{loc}}(y)$, and these lie in $\mathrm{ODC}(y)$. The local form can lose freedom, since a fanin value with one hidden and one visible preimage must keep its value.

**One fanout.** If $y$ has exactly one fanout $v$, then
$$\mathrm{ODC}(y) = \mathrm{ODC}(v) \cup \Big\{x : \frac{\partial f_v}{\partial y} = 0 \text{ at } x\Big\},$$
where the derivative of the local function $f_v$ is taken with its other fanins at their values for $x$. *Proof.* All paths from $y$ to the outputs pass through $v$, and the other fanins of $v$ do not depend on $y$. Flipping $y$ at $x$ either leaves $v$ the same, when $\partial f_v / \partial y = 0$ at $x$, or flips $v$, and then the outputs stay the same exactly when $x \in \mathrm{ODC}(v)$. $\square$ In a network where every internal node has one fanout, this rule computes all ODCs from the outputs back to the inputs.

**Compatible don't-cares.** Sets $D_1, \ldots, D_r$ for nodes $y_1, \ldots, y_r$ are compatible if every simultaneous change of each $y_i$ inside $D_i$ keeps all outputs. The full sets $\mathrm{ODC}(y_1), \ldots, \mathrm{ODC}(y_r)$ are not compatible in general, so a tool that simplifies many nodes in one pass needs compatible subsets. Savoj and Brayton (1990) compute such compatible observability don't-cares by putting the nodes in an order and giving each node only the vectors that stay hidden whatever the earlier nodes do inside their own sets.

## Examples and non-examples

**Examples.** The inputs are $a, b, c$, and the vectors are written $abc$.

- *Simplification.* Let $y = a + b$ and the only output $z = y \bar{a}$. Then $z|_{s=0} = 0$ and $z|_{s=1} = \bar{a}$, so $\partial z / \partial s = \bar{a}$ and $\mathrm{ODC}(y) = \{a = 1\}$, the four vectors $100, 101, 110, 111$. Every vector with $a = 1$ maps to fanin values with $a = 1$, so $D_{\mathrm{loc}}(y) = \{(a, b) : a = 1\}$. On the care set $a = 0$, $y = b$, so $y$ can become the wire $b$, and $z = b \bar{a}$ is the same function. This saves one literal and one node.
- *Two outputs.* Add the output $z_2 = y + c$. Then $\mathrm{ODC}_2(y) = \{c = 1\}$, and $\mathrm{ODC}(y) = \{a = 1\} \cap \{c = 1\} = \{101, 111\}$. Now $D_{\mathrm{loc}}(y)$ over the fanins $a, b$ is empty, since the fanin value $(1, 0)$ comes from both $101$, which is hidden, and $100$, which is not. No SOP of one literal agrees with $a + b$ off the ODC, so $y$ stays as it is.
- *Reconvergent fanout.* Let $y = a b$ feed two buffers $u = y$ and $v = y$, and let $z = u v$, so $z = a b$. For the edge into $u$ alone, $u$ is hidden when $v = 0$, so its ODC is $\{y = 0\}$, the three vectors $00, 01, 10$ over $a b$, and the same holds for $v$. The ODC of $y$ itself is empty, because $z = y$. Taking the intersection of the ODCs of the fanout edges would claim that $y$ may become the constant 1, which makes $z = 1$. So the one-fanout rule does not extend to several fanouts by intersection.
- *Two nodes at once.* Let $y_1 = a$, $y_2 = a$ and $z = y_1 + y_2$ over one input $a$. Each node has $\mathrm{ODC} = \{a = 1\}$, since the other node is 1 there. Each one alone may become the constant 0. Both at once give $z = 0$, not $a$. The compatible sets in the order $y_1, y_2$ are $\{a = 1\}$ for $y_1$ and $\emptyset$ for $y_2$.

A script checked each example on all input vectors.

**Non-examples.**

- A vector that never occurs at the primary inputs is an input don't-care of the whole circuit, not an observability don't-care. The definition above does not put it in $\mathrm{ODC}(y)$, although tools often add both kinds to the don't-care set of a node.
- Let a node $w$ have the fanins $y = a b$ and $a$. The fanin value $(y, a) = (1, 0)$ of $w$ never occurs. It is a satisfiability don't-care of that node. It is in $D_{\mathrm{loc}}$, but it is not a vector of the primary inputs, so it is not in any ODC.
- A node that drives a primary output directly, with no external don't-cares on that output, has an empty ODC, since $\partial z / \partial s = 1$ for $z = s$.
- An ODC is not a timing or test property. A node that is hidden at a vector is still computed, and it can still be on a slow path.

## Related definitions

- **[Don't-care condition](/dont-care-condition/).** The general idea of inputs where the output is free. The ODC is the kind that comes from the context of a node.
- **Satisfiability don't-care.** The fanin values of a node that no input vector produces. With the ODC, it makes up the local don't-care set.
- **[Cofactor](/cofactor/) and [Shannon expansion](/shannon-expansion/).** The Boolean difference is the exclusive OR of the two cofactors of the expansion on $s$.
- **[Two-level logic minimization](/two-level-logic-minimization/) and [Espresso](/espresso/).** Simplifying a node means minimizing its local SOP with $D_{\mathrm{loc}}(y)$ as the don't-care set.
- **[Don't-care-based function minimization](/dont-care-minimization/).** The same freedom used to make a BDD smaller.
- **[Multi-level logic synthesis](/multi-level-logic-synthesis/).** Uses ODCs in its Boolean simplification steps.
- **[Boolean equivalence checking](/boolean-equivalence-checking/).** A check after an ODC-based change compares the outputs, not the changed node, since the node itself has a new function.

## References
