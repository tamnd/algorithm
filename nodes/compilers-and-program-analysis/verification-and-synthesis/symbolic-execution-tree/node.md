---
tag: 6MEYWW
kind: definition
slug: symbolic-execution-tree
name: Symbolic execution tree
aliases:
- execution tree
area: compilers-and-program-analysis/verification-and-synthesis
level: core
summary: The tree of all paths of symbolic execution of a program, with a node per statement and a path condition per branch.
prereqs: [path-condition, symbolic-execution]
see_also: [path-explosion-problem, concolic-testing, generational-search, control-flow-graph, bounded-model-checking, register-machine, halting-problem]
sources:
  - paper: doi:10.1145/360248.360252
    title: James C. King, Symbolic execution and program testing, Communications of the ACM 19(7), 1976
    locator: pp. 385 to 394, the section on the execution tree (forking and non-forking IF statements, the properties of the tree)
  - paper: doi:10.1145/3182657
    title: Roberto Baldoni, Emilio Coppa, Daniele Cono D'Elia, Camil Demetrescu and Irene Finocchi, A survey of symbolic execution techniques, ACM Computing Surveys 51(3), 2018
    locator: Article 50, Section 1 (the symbolic execution tree of the running example) and Section 2 (the symbolic execution engine and its states)
  - paper: doi:10.1145/2408776.2408795
    title: Cristian Cadar and Koushik Sen, Symbolic execution for software testing, three decades later, Communications of the ACM 56(2), 2013
    locator: pp. 82 to 90, the section on classical symbolic execution and its execution tree
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.4.3 (the infinity lemma)
---

The symbolic execution tree of a program is the tree of all its feasible paths: the root is the start of the program, each node is a point reached by some input together with the [path condition](/path-condition/) of the way there, and a node has two children where both sides of a branch are feasible. It is the object that [symbolic execution](/symbolic-execution/) explores, and that [concolic testing](/concolic-testing/) and [generational search](/generational-search/) explore one run at a time. It differs from the [control flow graph](/control-flow-graph/) in two ways: it unfolds every join and every loop, so it can be exponentially larger or infinite, and it drops the branches that no input takes.

## Definition

Take a program $P$ in the toy IR with parameters $x_1, \dots, x_k$ and input symbols $\alpha_1, \dots, \alpha_k$. A *symbolic state* is a triple $(B, \sigma, \pi)$: a block label $B$, a symbolic store $\sigma$ from names to expressions over the symbols, and a path condition $\pi$. The **symbolic execution tree** $T(P)$ is the rooted tree defined as follows.

1. The root is $(B_0, \sigma_0, \mathit{true})$, where $B_0$ is the entry block and $\sigma_0(x_j) = \alpha_j$.
2. Let $v = (B, \sigma, \pi)$ be a node. Run the instructions of $B$ on $\sigma$, as in the definition of the path condition, and add the implicit condition of each instruction that can trap. Call the result $\sigma'$ and $\pi'$.
    - Let $\pi_i$ be the path condition just before an instruction that can trap, with the implicit condition $c$. If $\pi_i \wedge \neg c$ is satisfiable, then $v$ has a *trap leaf* child with this condition.
    - If $B$ ends in `ret a`, $v$ has one *return leaf* child with the condition $\pi'$.
    - If $B$ ends in `jump L`, $v$ has one child $(L, \sigma', \pi')$.
    - If $B$ ends in `br a L1 L2`, let $b = \sigma'(a)$. The node has the child $(L_1, \sigma', \pi' \wedge b \ne 0)$ if this condition is satisfiable, and the child $(L_2, \sigma', \pi' \wedge b = 0)$ if that one is satisfiable.
3. Each edge is labeled with the condition that it adds.

A branch where both sides are feasible is a *forking* node, as King calls it. A branch where $\pi'$ implies one side is *non-forking*: it has one child and it adds a condition that changes no set of inputs. King's tree has one node per statement. The tree above has one node per block visit. The two trees have the same leaves and the same forks, and one is the other with chains of straight-line steps contracted.

**Basic facts.** Write $I(v)$ for the set of inputs that satisfy the path condition of $v$.

- Every node is reached by some input, because each node has a satisfiable path condition. Every input follows exactly one path from the root, and the children of a node split $I(v)$ into disjoint parts. The page [symbolic execution](/symbolic-execution/) proves this partition property.
- So, for a program whose runs all end, the leaves of $T(P)$ are in one-to-one correspondence with the feasible complete paths, and the sets $I(\ell)$ of the leaves $\ell$ partition the input space $\mathbb{Z}^k$.
- A node has at most $b = c + 2$ children, where $c$ is the largest number of instructions that can trap in one block: one trap leaf per such instruction, and one or two other children.

**Finiteness.** The tree is finite if and only if there is a number $L$ such that every run of $P$ visits at most $L$ blocks.

*Proof.* Suppose there is such an $L$. A block node $v$ at depth $d$ has a satisfiable path condition, so some input follows the path to $v$, and its run visits at least $d + 1$ blocks. So $d < L$. A leaf is a child of a block node, so its depth is at most $L$. A tree of depth at most $L$ in which each node has at most $b$ children has at most $1 + b + \dots + b^L$ nodes, so it is finite. Conversely, suppose the tree is finite with height $H$. By the partition property, the run of each input visits the blocks of one path from the root, and that path stays in the tree. So the run visits at most $H$ blocks; in particular it ends. $\square$

The condition "every run ends" is weaker than "the tree is finite". By the infinity lemma (König's lemma), an infinite tree in which each node has finitely many children has an infinite path from the root. Each finite prefix of that path is feasible, but no single input may follow the whole path. The loop example below shows this.

**Decidability.** For the toy IR over unbounded integers, whether $T(P)$ is finite is undecidable. Take a two-counter machine, which is a [register machine](/register-machine/) with two counters, and translate it into a toy IR program that ignores its parameters. Each test of a counter is a branch on known values, so it is non-forking, and $T(P)$ is a single chain that copies the run of the machine. The tree is finite exactly when the machine halts, and the [halting problem](/halting-problem/) for two-counter machines is undecidable. Even the one-child case needs a solver when the branches are on symbols: deciding whether a node has a given child is the feasibility of a path condition, which is decidable only in decidable theories (see [path condition](/path-condition/)).

## Examples and non-examples

**A join with an infeasible combination.** The parameter is $x$, with the symbol $\alpha$.

```
entry:
  t = x < 5
  br t a b
a:
  y = x + 1
  jump join
b:
  y = x - 1
  jump join
join:
  u = 10 < y
  br u c d
c:
  ret 1
d:
  ret 0
```

The CFG has 6 blocks, 6 edges and 4 complete paths. The tree has these nodes, written by block, with the store of $y$ and the path condition:

- `entry`, $\pi = \mathit{true}$. Forking: both $\alpha < 5$ and $\alpha \ge 5$ are satisfiable.
    - `a`, $\pi = \alpha < 5$. One child.
        - `join`, $y = \alpha + 1$, $\pi = \alpha < 5$. Non-forking: $\alpha < 5 \wedge 10 < \alpha + 1$ is unsatisfiable, so only the side to `d` exists.
            - `d`, $\pi = \alpha < 5 \wedge \alpha + 1 \le 10$, which is $\alpha < 5$. Return leaf.
    - `b`, $\pi = \alpha \ge 5$. One child.
        - `join`, $y = \alpha - 1$, $\pi = \alpha \ge 5$. Forking.
            - `c`, $\pi = \alpha \ge 5 \wedge 10 < \alpha - 1$, which is $\alpha \ge 12$. Return leaf.
            - `d`, $\pi = \alpha \ge 5 \wedge \alpha - 1 \le 10$, which is $5 \le \alpha \le 11$. Return leaf.

The tree has 3 leaves, one for each feasible path. The block `join` appears twice, with two different stores: the tree copies the code after a join once per incoming path. The three leaf conditions $\alpha < 5$, $5 \le \alpha \le 11$ and $\alpha \ge 12$ split the integers into three parts. For $x$ in $-30$ to $30$, they hold for 35, 7 and 19 values.

**Exponential size.** Put $k$ tests one after another, each on its own parameter: `t1 = x1 < 0; br t1 ...` with both arms joining before the next test. The CFG has $3k + 1$ blocks. Every combination of sides is feasible, so the tree has $2^k$ leaves and $2^k - 1$ forking nodes. This is the [path explosion problem](/path-explosion-problem/) in its simplest form.

**An infinite tree in which every run ends.** The parameter is $n$, with the symbol $\nu$.

```
entry:
  i = 0
  jump head
head:
  t = i < n
  br t body exit
body:
  i = i + 1
  jump head
exit:
  ret i
```

The $j$-th visit of `head` has $\sigma(i) = j - 1$ and the path condition $0 < \nu \wedge \dots \wedge j - 2 < \nu$, so both sides are feasible and the node forks: the exit side gives a leaf with $\nu = j - 1$ (or $\nu \le 0$ for $j = 1$), and the body side goes on. The tree has infinitely many leaves and one infinite path, the path that always enters the body. Each prefix of the infinite path is followed by large values of $\nu$, but no integer $\nu$ satisfies $j < \nu$ for all $j$. So every run ends, and the tree is still infinite. This agrees with the finiteness criterion: the run on $n$ visits $2n + 3$ blocks for $n \ge 0$, and that number has no bound. Tools cut such a tree at a depth bound and give up any claim about the part below it.

**Non-examples.**

- *The control flow graph.* The CFG has one node per block and shares the code after a join. It has paths that no input takes, such as entry, a, join, c above. The tree has neither property.
- *The tree of one run.* A concolic tool records the path of one concrete run with its path condition. That is one root-to-leaf path of the tree, not the tree. The tree is the union of all such paths, which the tool never stores in full.
- *A merged state graph.* A tool that merges the two `join` states into one state with the store $y = \mathrm{ite}(\alpha < 5, \alpha + 1, \alpha - 1)$ and the path condition true builds a directed acyclic graph, not a tree. It has fewer nodes and harder formulas. See [path explosion](/path-explosion-problem/) for state merging.

## Related definitions

- **Path condition.** The label of a node is a [path condition](/path-condition/), and the leaves are the feasible complete paths.
- **Execution tree in testing tools.** [Concolic testing](/concolic-testing/) explores this tree by depth-first search, one run per leaf. [Generational search](/generational-search/) explores it by expanding all branches of a run at once.
- **Unrolled formula.** [Bounded model checking](/bounded-model-checking/) encodes the tree up to a depth $L$ as one formula, with one copy of each variable per step, instead of one formula per leaf.
- **Computation tree.** In model checking, the computation tree of a transition system unfolds the concrete states, one tree per start state. The symbolic execution tree is one tree for all inputs, with sets of inputs at the nodes.

## References
