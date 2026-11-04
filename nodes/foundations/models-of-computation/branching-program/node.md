---
tag: S0NWSF
kind: model
slug: branching-program
name: Branching program
aliases:
- binary branching program
- BP
area: foundations/models-of-computation
level: advanced
summary: Directed acyclic graph with query nodes; a non-uniform model for space and the basis of BDDs.
prereqs: [boolean-circuit, non-uniform-computation, logspace]
see_also: [nc, p-poly, binary-decision-diagram, decision-tree-model, circuit-complexity, turing-machine]
sources:
  - paper: "David A. Barrington, Bounded-width polynomial-size branching programs recognize exactly those languages in NC1, Journal of Computer and System Sciences 38(1) (1989)"
    locator: the main theorem and its proof (the width-5 construction)
  - book: "Ingo Wegener, Branching Programs and Binary Decision Diagrams: Theory and Applications, SIAM (2000)"
    locator: the chapters on the basic definitions, on bounded width and on lower bounds
  - paper: "Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8) (1986)"
    locator: the definition of ordered binary decision diagrams and the dependence of their size on the variable order
  - book: isbn:9780521424264
    title: "Sanjeev Arora and Boaz Barak, Computational Complexity: A Modern Approach"
    locator: Chapter 6, Boolean circuits (the classes NC and P/poly)
  - paper: "E. I. Nečiporuk, On a Boolean function, Soviet Mathematics Doklady 7 (1966)"
    locator: the lower bound on the size of branching programs and formulas for an explicit function
---

A branching program is a directed acyclic graph whose inner nodes each query one input variable and whose edges are labeled by the answer. It computes a Boolean function by following one path from the source to a sink. The model measures memory: a program with few nodes is a machine with few states. Branching programs of polynomial size are the same as [logarithmic space](/logspace/) with advice, and branching programs of constant width and polynomial size are the same as the class [NC](/nc/)$^1$ (Barrington, 1989).

## The machine

**Definition.** A *branching program* on the variables $x_1, \dots, x_n$ is a directed acyclic graph with one *source* node. Each node that is not a sink has out-degree 2. It is labeled by a variable $x_i$, and its two outgoing edges are labeled $0$ and $1$. Each sink is labeled $0$ or $1$ (a program for a function with one output bit). On an input $x \in \{0,1\}^n$ the computation starts at the source. At a node labeled $x_i$ it follows the edge labeled $x_i$. It stops at a sink, and the label of the sink is the output $f(x)$. The graph is acyclic, so the computation stops after at most as many steps as there are nodes. The same variable can occur on many nodes of one path, unless the program is read-once.

**Leveled programs.** A program is *leveled* when the nodes are split into layers $0, 1, \dots, L$, the source is the only node of layer $0$, all sinks are in layer $L$, and every edge goes from layer $j$ to layer $j+1$. The *length* is $L$, the *width* is the largest number of nodes in one layer, and the *size* is the number of nodes. Any program of size $s$ can be made leveled. Put each node that is not a sink in the layer of its longest distance from the source, and let $L$ be one more than the largest such layer, or $0$ if the source is a sink. Put every sink in layer $L$. A longest path has at most $s - 1$ edges, so $L \le s - 1$. Then give each node $v$ one chain of new copies in the layers before the layer of $v$. Each copy queries any variable and has two equal outgoing edges to the next copy, and the last copy points to $v$. An edge $u \to v$ that skips layers goes instead to the copy of $v$ in the layer after the layer of $u$. All the edges that enter $v$ share this one chain. Each node gets fewer than $L$ copies, so the size is at most $sL < s^2$. The length is $L < s$, and the program computes the same function.

**Variants.**

- A program is *oblivious* when all nodes of one layer query the same variable. Then the program is a fixed sequence of queries $x_{i_1}, \dots, x_{i_L}$ and a transition table for each query.
- A program is *read-once* when each variable occurs at most once on each path.
- An *ordered binary decision diagram* (OBDD) is a read-once program in which the variables occur in the same order $x_{\pi(1)}, \dots, x_{\pi(n)}$ on every path. OBDDs are the main data structure of the area of [binary decision diagrams](/binary-decision-diagram/).
- A program can have more than two sinks, or more than one output. This page uses one output bit.

**A model with no uniformity.** A branching program has a fixed number $n$ of variables. A function on inputs of all lengths is computed by a *family* $(P_n)_{n \ge 1}$, and the family is not required to have any finite description. So the model is non-uniform in the sense of [non-uniform computation](/non-uniform-computation/), like a [Boolean circuit](/boolean-circuit/).

**Example: parity.** Let $f(x) = x_1 \oplus \dots \oplus x_n$. A leveled program of length $n$ and width $2$ computes $f$. Layer $j$ has two nodes $(j, 0)$ and $(j, 1)$, and the node $(j, b)$ means that the parity of $x_1, \dots, x_j$ is $b$. Every node of layer $j - 1$ queries $x_j$. The $0$-edge of $(j-1, b)$ goes to $(j, b)$ and the $1$-edge goes to $(j, 1 - b)$. The source is $(0, 0)$ and the sink $(n, b)$ has label $b$ (the two nodes of layer $n$ are the sinks).

## What it counts

The main measures are the size, and for leveled programs the length and the width. They correspond to resources of other models.

- **Size and space.** A program of size $s$ remembers $\lceil \lg s \rceil$ bits of state. So $\lg(\text{size})$ is the space of a machine that reads its input only by queries to single bits. This is why the model is the non-uniform model of space.
- **Length and time.** The length bounds the number of queries on every path. For a program that is not leveled, the length is the number of edges on its longest path. A decision tree is a program in which every node has in-degree at most 1, so a [decision tree](/decision-tree-model/) is a branching program and the size of a tree can be exponentially larger than the size of the equivalent program.
- **Width.** The width is the number of states that the computation holds at one time. A small width means that the program cannot hold much information between two queries. This is the resource that Barrington's theorem relates to circuit depth.

Computation inside the program is free: the program has no other operations than the queries.

## Relation to other models

**Boolean circuits.** The comparison with a [Boolean circuit](/boolean-circuit/) is by depth. By Barrington's theorem below, a function computed by circuits of polynomial size and depth $O(\log n)$ (the class $\mathrm{NC}^1$) has a polynomial-size program of width $5$, and the converse holds.

**Logarithmic space.** The class $\mathrm{L/poly}$ is the class of languages decided by a deterministic logarithmic-space machine with a polynomial-length advice string for each input length (see [non-uniform computation](/non-uniform-computation/)). A language is in $\mathrm{L/poly}$ if and only if it has branching programs of polynomial size. Proof of "only if". Let $M$ be a machine that uses space $c \lg n$ and let $a_n$ be its advice for length $n$. Assume that $M$ halts on every input. A configuration of $M$ is a state, the content of the work tape, and the positions of the input head, the advice head and the work head. For fixed $n$ the number $C$ of configurations is at most $|Q| \cdot |\Gamma|^{c \lg n} \cdot (c \lg n) \cdot n \cdot |a_n| = \mathrm{poly}(n)$, where $Q$ is the set of states and $\Gamma$ is the work alphabet. The advice $a_n$ is fixed, so it is built into the transition function. A halting computation never repeats a configuration, so it has at most $C$ steps. Take $T = C$ layers. The nodes are the pairs (layer $t$, configuration). A configuration whose input head is on position $i$ queries $x_i$, and its two successors in layer $t+1$ are the configurations that $M$ reaches after reading $0$ or $1$. A configuration whose input head is on an endmarker, or that is halting, queries $x_1$ and has two equal outgoing edges to its successor in the next layer (a halting configuration is its own successor). The sinks are the nodes of layer $T$, labeled $1$ for the accepting configurations and $0$ for the others. The size is $T \cdot C = \mathrm{poly}(n)$. Proof of "if". Let $P_n$ be a program of size $s = \mathrm{poly}(n)$. Give a description of $P_n$ as the advice. The machine keeps the index of the current node, which takes $\lceil \lg s \rceil$ bits. It reads the variable of that node from the input, reads the advice to find the successor, and repeats until it reaches a sink. The space is $O(\log n)$. $\square$

**Uniform version.** If the family $(P_n)$ can be generated by a logarithmic-space machine from $1^n$, then the language is in $\mathrm{L}$: the machine of the "if" part computes the description of a node from $1^n$ when it needs it, instead of reading it from the advice. So polynomial-size branching programs are to $\mathrm{L}$ what polynomial-size circuits are to $\mathrm{P}$.

**Turing machines.** A [Turing machine](/turing-machine/) has a tape of unbounded length and a program that is the same for all inputs. A branching program is its unrolled configuration graph for a fixed input length, as in the proof above.

## Known results in the model

**Barrington's theorem (1989).** Let $f = (f_n)$ be a family of Boolean functions. Then $f$ is computed by a family of leveled programs of constant width and polynomial length if and only if $f \in \mathrm{NC}^1$, the class of functions computed by Boolean circuits of polynomial size, depth $O(\log n)$ and fan-in 2. In fact width $5$ suffices.

The proof uses programs over the symmetric group $S_5$. A *permutation program* of length $L$ is a list of instructions $(i_j, a_j, b_j)$ for $j = 1, \dots, L$, where $i_j \in \{1, \dots, n\}$ and $a_j, b_j \in S_5$. On the input $x$ the instruction $j$ gives the permutation $c_j = b_j$ if $x_{i_j} = 1$ and $c_j = a_j$ if $x_{i_j} = 0$. The program has the value $P(x) = c_L \circ \dots \circ c_2 \circ c_1$. Let $\alpha$ be a $5$-cycle. The program *computes $f$ with the cycle $\alpha$* if $P(x) = \alpha$ when $f(x) = 1$ and $P(x) = \mathrm{id}$ when $f(x) = 0$.

*Step 0: a permutation program gives a width-5 program.* Take layers $0, \dots, L$ with the nodes $(j, 1), \dots, (j, 5)$. At the end, keep only the nodes reachable from the source $(0, 1)$, so that layer $0$ holds just the source. Node $(j-1, u)$ queries $x_{i_j}$, and its $0$-edge goes to $(j, a_j(u))$ and its $1$-edge to $(j, b_j(u))$. Then the node of layer $L$ that is reached from $(0, 1)$ is $(L, P(x)(1))$. A $5$-cycle moves the point $1$, so $P(x)(1) = \alpha(1) \ne 1$ if $f(x) = 1$ and $P(x)(1) = 1$ if $f(x) = 0$. Label the sink $(L, \alpha(1))$ with $1$ and every other sink with $0$. This program has width $5$, length $L$ and computes $f$.

*Step 1: change of cycle.* If $f$ is computed with the cycle $\alpha$ by a program of length $L$, and $\beta$ is any other $5$-cycle, then $f$ is computed with the cycle $\beta$ by a program of length $L$. The $5$-cycles form one conjugacy class of $S_5$, so there is $\gamma \in S_5$ with $\beta = \gamma \alpha \gamma^{-1}$. Replace each $a_j$ and $b_j$ by $\gamma a_j \gamma^{-1}$ and $\gamma b_j \gamma^{-1}$. The new value is $\gamma P(x) \gamma^{-1}$, which is $\beta$ when $P(x) = \alpha$ and $\mathrm{id}$ when $P(x) = \mathrm{id}$.

*Step 2: negation.* Let a program of length $L$ compute $f$ with the cycle $\alpha$. Replace $a_L$ and $b_L$ by $\alpha^{-1} a_L$ and $\alpha^{-1} b_L$. The new value is $\alpha^{-1} P(x)$, which is $\mathrm{id}$ when $f(x) = 1$ and $\alpha^{-1}$ when $f(x) = 0$. So this program computes $\neg f$ with the cycle $\alpha^{-1}$, which is a $5$-cycle, and by Step 1 it computes $\neg f$ with any cycle. The length does not change.

*Step 3: inverse program.* Reverse the list of instructions and replace each $a_j$, $b_j$ by its inverse. The new value is $P(x)^{-1}$. So if the first program computes $f$ with the cycle $\alpha$, the new program computes $f$ with the cycle $\alpha^{-1}$. The length does not change.

*Step 4: conjunction.* There are $5$-cycles $\alpha$ and $\beta$ such that $\kappa = \beta^{-1} \alpha^{-1} \beta \alpha$ is also a $5$-cycle. For example, take $\alpha = (1\,2\,3\,4\,5)$ and $\beta = (1\,2\,4\,5\,3)$. Then $\kappa = (1\,5\,3\,2\,4)$: it sends $1 \mapsto 5$, $5 \mapsto 3$, $3 \mapsto 2$, $2 \mapsto 4$ and $4 \mapsto 1$. Let $f$ be computed by a program $F$ of length $l_f$ and $g$ by a program $G$ of length $l_g$. By Step 1, take $F$ with the cycle $\alpha$ and $G$ with the cycle $\beta$. Write the instruction lists one after the other as $F, G, F^{-1}, G^{-1}$, where $F^{-1}$ is the inverse program of Step 3 (it has the cycle $\alpha^{-1}$ for $f$, and $G^{-1}$ has the cycle $\beta^{-1}$ for $g$). The value is $G^{-1}(x) F^{-1}(x) G(x) F(x)$, where $F(x)$ stands for the value of the program $F$ and so on.

- If $f(x) = g(x) = 1$, the value is $\beta^{-1} \alpha^{-1} \beta \alpha = \kappa$.
- If $f(x) = 0$, then $F(x) = F^{-1}(x) = \mathrm{id}$ and the value is $G^{-1}(x) G(x) = \mathrm{id}$.
- If $f(x) = 1$ and $g(x) = 0$, then $G(x) = G^{-1}(x) = \mathrm{id}$ and the value is $F^{-1}(x) F(x) = \alpha^{-1} \alpha = \mathrm{id}$.

So the long program computes $f \wedge g$ with the cycle $\kappa$, and its length is $2 l_f + 2 l_g$. By Step 1, it computes $f \wedge g$ with any cycle.

*Step 5: the circuit.* A circuit of depth $d$ with gates AND, OR, NOT of fan-in at most 2 unfolds to a formula of the same depth, where each gate is copied for each of its uses. The formula has at most $2^{d+1}$ gates. Replace each OR gate by the three gates $a \vee b = \neg(\neg a \wedge \neg b)$. Now every root-to-leaf path has at most $d$ AND gates. We prove by structural induction on the formula the following hypothesis: every formula over AND and NOT whose root-to-leaf paths have at most $d'$ AND gates is computed with any $5$-cycle by a permutation program of length at most $4^{d'}$. There are three cases. A variable $x_i$ is computed with the cycle $\alpha$ by the single instruction $(i, \mathrm{id}, \alpha)$, of length $1 = 4^0$. A NOT of a subformula $g$ has the same bound $d'$ as $g$; by the hypothesis for $g$, then Step 2 and Step 1, it is computed with any cycle by a program of the same length, at most $4^{d'}$. An AND of two subformulas has $d' \ge 1$, and each subformula has at most $d' - 1$ AND gates on each path; by the hypothesis and Step 4 the length is at most $2 \cdot 4^{d'-1} + 2 \cdot 4^{d'-1} = 4^{d'}$. For $d = c \lg n$ the length is $n^{2c}$, a polynomial. By Step 0 the width is $5$. This proves the direction from $\mathrm{NC}^1$ to bounded width.

*Step 6: the other direction.* Let $P$ be a leveled program of width $k$ and length $L = \mathrm{poly}(n)$. For each layer $j$ the input $x$ defines a map $\tau_j : [k] \to [k]$ that sends the index of a node of layer $j-1$ to the index of its successor in layer $j$. The map $\tau_j$ depends on at most $k$ input bits, so it is computed from $x$ by a circuit of constant size (the constants are $k$ and the program). The program accepts if and only if $\tau_L \circ \dots \circ \tau_1$ sends the index of the source to the index of an accepting sink. Compose the maps by a balanced binary tree with $L$ leaves. Each composition of two maps $[k] \to [k]$ is a circuit of constant size and depth, because $k$ is a constant. The tree has depth $\lceil \lg L \rceil = O(\log n)$. So the whole circuit has polynomial size and depth $O(\log n)$. $\square$

**Example of the construction.** For $f = (x_1 \wedge x_2) \wedge (x_3 \wedge x_4)$, a formula with two AND gates on each path, the construction gives a permutation program of length $16 = 4^2$. It has the value $(1\,2\,3\,4\,5)$ on the input $1111$ and the value $\mathrm{id}$ on the other $15$ inputs.

**Size and the variable order.** For OBDDs the order of the variables changes the size by an exponential factor, which Bryant (1986) discussed. Let $f = x_1 x_2 \vee x_3 x_4 \vee \dots \vee x_{2k-1} x_{2k}$. In the order $x_1, x_2, \dots, x_{2k}$ the minimal OBDD has $2k + 2$ nodes (including the two sinks), and in the order $x_1, x_3, \dots, x_{2k-1}, x_2, x_4, \dots, x_{2k}$ it has $2^{k+1}$ nodes. For a fixed order, the minimal OBDD has one node for each distinct subfunction that is obtained by fixing the variables before $x_{\pi(i)}$ and that depends on $x_{\pi(i)}$, plus the two sinks (see Wegener's book, the chapter on OBDDs). In the first order, the subfunctions at $x_{2i-1}$ and at $x_{2i}$ are $\bigvee_{j \ge i} x_{2j-1}x_{2j}$ and $x_{2i} \vee \bigvee_{j > i} x_{2j-1}x_{2j}$, one each, so the size is $2k + 2$. In the second order, fixing $x_1, x_3, \dots, x_{2i-1}$ in the $2^i$ possible ways gives $2^i$ different subfunctions, all of which depend on $x_{2i+1}$, so the first $k$ levels have $2^k - 1$ nodes. After all odd variables are fixed, with the set $A$ of the $i$ for which $x_{2i-1} = 1$, the subfunction is $\bigvee_{i \in A} x_{2i}$. The subfunctions that depend on $x_{2j}$ are $\bigvee_{i \in A'} x_{2i}$ with $A' \subseteq \{j, \dots, k\}$ and $j \in A'$, which gives $2^{k-j}$ nodes for $x_{2j}$ and $2^k - 1$ nodes on the last $k$ levels. The total is $2(2^k - 1) + 2 = 2^{k+1}$. For $k = 2, 3, 4, 5$ the sizes are $6, 8, 10, 12$ in the first order and $8, 16, 32, 64$ in the second order.

**Lower bounds.** No explicit function in $\mathrm{NP}$ is known to need superpolynomial size on general branching programs, and such a function would show $\mathrm{NP} \not\subseteq \mathrm{L/poly}$. Nečiporuk (1966) proved that some explicit function needs size $\Omega(n^2 / \log^2 n)$, and bounds of about this order are the best known for general programs (see Wegener's book). Strong lower bounds are known for restricted programs, for example read-once programs and OBDDs with a fixed order.

## References
