---
tag: ACQM80
kind: concept
slug: computational-graph
name: Computational graph
aliases:
- expression graph
area: machine-learning/neural-network-training
level: intro
summary: "A directed acyclic graph of primitive operations. Forward evaluation walks it in topological order; reverse mode differentiation walks it backward."
prereqs: [directed-acyclic-graph, topological-sort]
see_also: [automatic-differentiation, backpropagation, backpropagation-through-time, gradient-checkpointing, expression-dag, straight-line-program, computation-dag, gradient]
sources:
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 6.5.1 (computational graphs), Sections 6.5.2 to 6.5.6 (the chain rule on the graph and general back-propagation) and Section 10.1 (unfolding a recurrent graph)
  - book: isbn:9780898716597
    title: Andreas Griewank and Andrea Walther, Evaluating Derivatives, Principles and Techniques of Algorithmic Differentiation, second edition, SIAM, 2008
    locator: Chapter 2 (evaluation procedures, the computational graph and the three-part form of a program)
  - paper: "Atilim Gunes Baydin, Barak A. Pearlmutter, Alexey Andreyevich Radul and Jeffrey Mark Siskind, Automatic differentiation in machine learning: a survey, Journal of Machine Learning Research 18(153), 2018"
    locator: Section 3 (the evaluation trace of f(x1, x2) = ln(x1) + x1 x2 - sin(x2) and its computational graph)
  - paper: doi:10.1137/0711010
    title: "F. L. Bauer, Computational graphs and rounding error, SIAM Journal on Numerical Analysis 11(1), 1974"
    locator: pp. 87 to 96 (the graph of a computation and derivatives as sums over paths)
  - paper: doi:10.1145/355586.364791
    title: "R. E. Wengert, A simple automatic derivative evaluation program, Communications of the ACM 7(8), 1964"
    locator: pp. 463 to 464 (a program written as a list of elementary assignments)
---

A computational graph is a [directed acyclic graph](/directed-acyclic-graph/) whose nodes are the inputs of a program and the results of its primitive operations, and whose arcs go from each value to the operations that use it. To compute the function, you evaluate the nodes in a [topological order](/topological-sort/). To compute its derivatives, [automatic differentiation](/automatic-differentiation/) walks the same graph: forward mode in the same order, reverse mode (called [backpropagation](/backpropagation/) for neural networks) in the opposite order.

## In plain words

Write a formula as a list of small steps. Each step does one simple thing, such as a product, a sum or a sine, and uses values that earlier steps made. Draw one box for each value and an arrow from a value to each step that uses it. The drawing is the computational graph. It has no cycles, because a step only uses older values.

To get the result, you work through the boxes so that each box comes after the boxes it needs. To find how much the result changes when one input changes, you can carry a rate of change along the arrows from the inputs to the result. You can also go the other way, from the result back to all inputs at once. The second way gives the change for every input in one pass, and this is what neural network training uses.

## The idea

**Definition.** Fix a set $\Phi$ of primitive operations, for example $+$, $-$, $\times$, $/$, $\exp$, $\log$, $\sin$, $\tanh$ and the matrix product. A computational graph for a function $F : \mathbb{R}^p \to \mathbb{R}^m$ is a directed acyclic graph $G = (V, E)$ with nodes $v_{1-p}, \ldots, v_0, v_1, \ldots, v_L$ such that:

- the nodes $v_{1-p}, \ldots, v_0$ are the inputs and have no incoming arcs;
- each other node $v_i$ carries an operation $\varphi_i \in \Phi$ and has the value $v_i = \varphi_i\big((v_j)_{j \in \mathrm{pa}(i)}\big)$, where $\mathrm{pa}(i)$ is the list of its parents, and $(j, i) \in E$ exactly when $j \in \mathrm{pa}(i)$;
- $m$ chosen nodes are the outputs.

The numbering $1 - p, \ldots, L$ is a topological order: each parent has a smaller index than its child. Written out in this order, the graph is a program with one assignment per line. Wengert (1964) used this form, and it is now called the *evaluation trace* or *Wengert list*. In algebraic complexity the same object is a [straight-line program](/straight-line-program/); in a compiler it is an [expression DAG](/expression-dag/) after common subexpressions are merged.

**Forward evaluation.** Visit the nodes in topological order and compute $v_i$ from its parents. Each node is computed once, after all its parents, so the cost is one call of $\varphi_i$ per node, $O(\lvert V \rvert + \lvert E \rvert)$ steps if each primitive costs $O(1)$ per argument. A topological order exists because $G$ is acyclic, and [topological sort](/topological-sort/) finds one in $O(\lvert V \rvert + \lvert E \rvert)$ time. A program that is executed line by line already produces its nodes in a topological order.

**Local partials and the chain rule on the graph.** Give each arc $(j, i)$ the weight $c_{ij} = \partial \varphi_i / \partial v_j$, evaluated at the current values. Let $y$ be one output. Then for every node $j$,

$$\bar v_j := \frac{\partial y}{\partial v_j} = \sum_{i \,:\, j \in \mathrm{pa}(i)} \bar v_i \, c_{ij}, \qquad \bar y = 1.$$

Here $\partial y / \partial v_j$ means: treat $v_j$ as a free variable, recompute every node that depends on it, and differentiate $y$. *Proof.* The output node has $\bar y = 1$. Fix another node $j$. For $k \ge j$, let $g_k$ be $y$ as a function of $v_{1-p}, \ldots, v_k$, all treated as free, with the nodes $k + 1, \ldots, L$ recomputed from them. Then $\bar v_k = \partial g_k / \partial v_k$ for every $k$, and $g_L$ is $y$ itself, so $\partial g_L / \partial v_j = 0$. For $k > j$, $g_{k-1}$ is $g_k$ with $v_k$ replaced by $\varphi_k$ of its parents, which all have indices below $k$. The multivariate chain rule gives $\partial g_{k-1} / \partial v_j = \partial g_k / \partial v_j + \bar v_k \, c_{kj}$, with $c_{kj} = 0$ when $j$ is not a parent of $k$. Add these equations for $k = L, L - 1, \ldots, j + 1$: $\bar v_j = \partial g_j / \partial v_j = \sum_{k > j} \bar v_k \, c_{kj}$, which is the sum over the children of $j$. The argument also holds when a child of $j$ has another parent that depends on $v_j$, because each $g_k$ keeps all earlier nodes free. If $j$ has no path to $y$, every $\bar v_k$ in the sum with $c_{kj} \ne 0$ is 0, and $\bar v_j = 0$. $\blacksquare$

The same argument in increasing order gives the forward rule $\dot v_i = \sum_{j \in \mathrm{pa}(i)} c_{ij} \dot v_j$, where $\dot v_i$ is the derivative of $v_i$ along a fixed input direction. Unrolling either recursion gives Bauer's path formula (1974): $\partial y / \partial x_k$ is the sum, over all directed paths from the input $x_k$ to $y$, of the product of the arc weights on the path.

**Graph, not tree.** A node can have many children. The graph then shares the value, while an expression tree would copy the whole subexpression. The chain of $n$ nodes $v_{i} = v_{i-1} \cdot v_{i-1}$ computes $x^{2^n}$; as a tree it has $2^n$ leaves. Sharing is also why the path formula is a bad algorithm: the number of paths can grow exponentially, while both recursions above visit each arc once.

**One run, one graph.** A program with loops and branches does not have one fixed graph. The graph is the trace of one run on one input: a loop of $T$ rounds becomes $T$ copies of its body. This is how a recurrent network is *unfolded* over time before [backpropagation through time](/backpropagation-through-time/). Frameworks differ in when they build the graph. A *static* framework (Theano, TensorFlow 1) builds a symbolic graph first and then runs it many times. A *dynamic* framework (Chainer, PyTorch) records the graph while the program runs, on each call. The mathematics is the same; a static graph is easier to optimize, and a dynamic graph is easier to use with data-dependent control flow.

**Memory.** Reverse mode needs the values $v_j$ (or the weights $c_{ij}$) of the forward run. So a stored graph uses memory proportional to the number of nodes. [Gradient checkpointing](/gradient-checkpointing/) stores only some nodes and computes the others again.

## Examples

**A small trace.** Take $f(x_1, x_2) = \ln x_1 + x_1 x_2 - \sin x_2$ at $(x_1, x_2) = (2, 5)$, the example of Baydin et al. (2018). The graph has 2 input nodes and 5 operation nodes.

| node | operation | parents | value | arc weights $c_{ij}$ |
|---|---|---|---|---|
| $v_{-1}$ | input $x_1$ | | 2 | |
| $v_0$ | input $x_2$ | | 5 | |
| $v_1$ | $\ln$ | $v_{-1}$ | 0.693147 | $1 / v_{-1} = 0.5$ |
| $v_2$ | $\times$ | $v_{-1}, v_0$ | 10 | $v_0 = 5$, $v_{-1} = 2$ |
| $v_3$ | $\sin$ | $v_0$ | $-0.958924$ | $\cos v_0 = 0.283662$ |
| $v_4$ | $+$ | $v_1, v_2$ | 10.693147 | 1, 1 |
| $v_5$ | $-$ | $v_4, v_3$ | 11.652071 | 1, $-1$ |

The node $v_{-1}$ has two children, $v_1$ and $v_2$, and so does $v_0$. The backward rule gives $\bar v_5 = \bar v_4 = 1$, $\bar v_3 = -1$, $\bar v_2 = \bar v_1 = 1$, then $\bar v_0 = \bar v_2 \cdot 2 + \bar v_3 \cdot 0.283662 = 1.716338$ and $\bar v_{-1} = \bar v_1 \cdot 0.5 + \bar v_2 \cdot 5 = 5.5$. These are $\partial f / \partial x_2 = x_1 - \cos x_2$ and $\partial f / \partial x_1 = 1/x_1 + x_2$. By the path formula, $\partial f / \partial x_1$ has two paths, $v_{-1} \to v_1 \to v_4 \to v_5$ with product $0.5$ and $v_{-1} \to v_2 \to v_4 \to v_5$ with product $5$.

**A dense layer.** For a layer $a = \tanh(W x + b)$ with $W \in \mathbb{R}^{k \times d}$, a framework uses three nodes: a matrix product $u = W x$, a sum $z = u + b$ and an elementwise $\tanh$. Its arc weights are not stored as matrices. The reverse rule for $u = Wx$ is $\bar x = W^\top \bar u$ and $\bar W = \bar u x^\top$, and the rule for $\tanh$ is $\bar z = \bar a \odot (1 - a \odot a)$. Coarse primitives like these keep the graph small: one node per layer instead of one node per scalar product.

**Many paths, few arcs.** Let $v_0 = x$ and, for $k = 1, \ldots, n$, let $s_k = \sin v_{k-1}$, $c_k = \cos v_{k-1}$ and $v_k = s_k + c_k$. The graph has $3n + 1$ nodes and $4n$ arcs, and there are $2^n$ paths from $x$ to $v_n$. For $n = 30$ the path formula sums $2^{30} = 1073741824$ products; either recursion does $4 \cdot 30 = 120$ multiply-adds.

**A non-example.** A program that changes a variable in place, $x \leftarrow x + 1$ inside a loop, is not itself a graph, because the same name holds different values. Its trace is a graph after each assignment gets a new node. A cyclic "graph" such as a recurrent network drawn with a self-loop is a compact picture of a family of graphs, one per sequence length; it becomes a DAG only after unfolding.

## Where it is used

- [Automatic differentiation](/automatic-differentiation/): forward mode and reverse mode are the two recursions above.
- [Backpropagation](/backpropagation/) is the reverse recursion on the graph of a layered network, and [backpropagation through time](/backpropagation-through-time/) is the same on an unfolded recurrent network.
- [Gradient checkpointing](/gradient-checkpointing/) chooses which node values to keep.
- [Expression DAGs](/expression-dag/) and [straight-line programs](/straight-line-program/) are the same object in compilers and in algebraic complexity; the [computation DAG](/computation-dag/) of parallel computing uses it to measure work and span.
- The [gradient](/gradient/) of a training loss in [gradient descent](/gradient-descent/) is read off the input nodes after one backward walk.

## References
