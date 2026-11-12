---
title: On a factor tree the two passes of belief propagation give the exact marginals
proves: [correctness]
status: full
---

We use the pseudocode BELIEF-PROPAGATION and SEND of the page. The factor graph is a forest; by line L1 we may treat one tree at a time, since trees share no variable and no factor, and the product of the factors splits over the trees. So let the factor graph be a tree with root $r$. Let $\lambda_x$ be the evidence indicator of the variable $x$ (the constant 1 if $x$ is not observed), and let
$$\tilde p(x) = \prod_{v} \lambda_v(x_v) \prod_{f} f(x_f)$$
be the product of all the factors and indicators, over all the variables of the tree.

**Sides of an edge.** Removing the edge $\{u, w\}$ splits the tree into two parts. Let $T_{u \setminus w}$ be the part that holds $u$. Let $V_{u \setminus w}$ be its variables, and $\Pi_{u \setminus w}$ the product of its factors and of the indicators of its variables. Because the graph is a tree, every factor and every variable is on exactly one side, so for a variable $x$ and a factor $f$ next to it,
$$\tilde p = \Pi_{x \setminus f} \cdot \Pi_{f \setminus x}, \qquad V_{x \setminus f} \cap V_{f \setminus x} = \{x\}. \tag{1}$$

**Claim (the meaning of a message).** Each message is a sum over its side:

- for a variable $x$ and a factor $f$: $\mu_{x \to f}(x) = \sum_{V_{x \setminus f} \setminus \{x\}} \Pi_{x \setminus f}$;
- for a factor $f$ and a variable $x$: $\mu_{f \to x}(x) = \sum_{V_{f \setminus x} \setminus \{x\}} \Pi_{f \setminus x}$.

*Proof.* Induction on the number of nodes in the side. First, the messages a node uses exist when it sends: in line L2 a node sends to its parent after all the nodes below it, which are later in the breadth-first order; in line L3 a node sends to a child after it has received from its parent, which is earlier in the order. In both cases the node has the messages from all its other neighbours, and these come from smaller sides.

*Variable to factor (line L6).* The side $T_{x \setminus f}$ is $x$ with the sides $T_{g \setminus x}$ of its other factors $g$. These sides are pairwise disjoint and share only $x$ with each other. So the sum of $\Pi_{x \setminus f} = \lambda_x \prod_g \Pi_{g \setminus x}$ over all the variables except $x$ splits into $\lambda_x(x) \prod_g \sum \Pi_{g \setminus x}$, which by induction is $\lambda_x(x) \prod_g \mu_{g \to x}(x)$, the value line L6 computes. If $x$ is a leaf, the product is empty and the message is $\lambda_x$, which is also the sum over its side.

*Factor to variable (line L7).* The side $T_{f \setminus x}$ is $f$ with the sides $T_{y \setminus f}$ of its other variables $y$. These are pairwise disjoint, and $T_{y \setminus f}$ meets the scope of $f$ only in $y$. Summing $\Pi_{f \setminus x} = f \prod_y \Pi_{y \setminus f}$ over all the variables except $x$, first sum inside each side over the variables other than $y$; by induction this gives $\mu_{y \to f}(x_y)$. What remains is the sum over the other variables of the scope of $f$ of $f(x_f) \prod_y \mu_{y \to f}(x_y)$, which is line L7. $\blacksquare$

**Theorem.** After lines L2 and L3, every edge carries a message in each direction, and for each variable $x$, line L4 gives
$$b_x(x) = \lambda_x(x) \prod_{f \in N(x)} \mu_{f \to x}(x) = \sum_{\text{all variables but } x} \tilde p.$$
So $\sum_x b_x(x) = Z$, the sum of $\tilde p$, and $b_x / Z = P(X = x \mid e)$ when $\tilde p$ is a Bayesian network times the indicators. For a factor $f$, $f(x_f) \prod_{y \in f} \mu_{y \to f}(x_y) = \sum_{\text{variables not in } f} \tilde p$.

*Proof.* Line L2 sends from each non-root node to its parent and line L3 from each parent to its child, so each edge carries one message each way: $2|E|$ messages in total. For the variable $x$, the tree is $x$ with the disjoint sides $T_{f \setminus x}$ of its factors, which meet only in $x$. So the sum of $\tilde p = \lambda_x \prod_f \Pi_{f \setminus x}$ over all the variables except $x$ splits, and the claim gives the formula. The statement for a factor follows in the same way from the sides $T_{y \setminus f}$. Line L4 divides by $Z$, which is the same at every variable of the tree. Over a forest, $Z$ is the product of the sums of the trees. $\blacksquare$

**Remark (where trees are used).** Equation (1) and the disjoint sides are the only places where the proof uses that the graph is a tree. On a graph with a cycle, the side of an edge is not defined, a message can return to its sender along the cycle, and the same updates (loopy belief propagation) are not exact in general.
