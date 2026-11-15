---
title: Aggressive dead code elimination keeps the outcome of every run that ends
proves: [correctness]
status: full
---

**Setting.** $P$ is a program of the toy IR with no phi-functions, and $P'$ is the program that aggressive dead code elimination returns. A *statement* is an instruction or a terminator. We assume three things:

1. every block that the entry reaches also reaches a `ret` block;
2. no run of $P$ reads a name before it is defined;
3. only runs of $P$ that end are compared: runs that return a value or trap.

Assumption 1 is checked by the implementation, which raises an error otherwise. Assumption 3 is the termination assumption of the algorithm. A loop with no marked statement disappears, so a run of $P$ that loops forever inside such a loop can end in $P'$. At the end we show that this is the only difference.

**Definitions.** Add a virtual exit node with an edge from every `ret` block. A node $Y$ *post-dominates* $X$ if every path from $X$ to the exit passes through $Y$. It *strictly* post-dominates $X$ if also $Y \ne X$. By assumption 1 every block has post-dominators, and they form a tree with the exit as its root: $\mathrm{ipdom}(X)$ is the parent of $X$. The strict post-dominators of $X$ are the nodes on the tree path from $\mathrm{ipdom}(X)$ to the root. A block $Y$ is *control dependent* on a block $C$ if $Y$ post-dominates a successor of $C$ and $Y$ does not strictly post-dominate $C$.

The implementation finds the control dependences on $C$ by walking, for each successor $s$ of $C$, up the tree from $s$ to $\mathrm{ipdom}(C)$, without $\mathrm{ipdom}(C)$ itself. This gives exactly the definition. $\mathrm{ipdom}(C)$ post-dominates $s$ or equals it, so it lies on the tree path from $s$ to the root. A node $Y$ on that path post-dominates $s$. It strictly post-dominates $C$ exactly when it is $\mathrm{ipdom}(C)$ or above it, because the strict post-dominators of $C$ are the nodes from $\mathrm{ipdom}(C)$ to the root.

A block is *useful* if it holds a marked statement. Every `ret` is marked, so every `ret` block is useful. When the loop of line L5 stops, the marked set has three closure properties:

- **(M1)** every critical statement is marked: `ret`, store, call, `alloc`, an operation that may trap, and a definition of an address-taken name;
- **(M2)** if $S$ is marked and reads a name $u$, every definition of $u$ that reaches $S$ is marked;
- **(M3)** if a useful block $Y$ is control dependent on $C$, the branch of $C$ is marked.

(M2) and (M3) hold because every marked statement goes through the work list once, and lines L7 to L10 mark what it needs.

## Lemma 1: an unmarked branch leads to its nearest useful post-dominator

Let $B$ be a block whose terminator is an unmarked branch. Take a path $B = v_0, v_1, \ldots, v_k$ in the graph with $k \ge 1$, $v_k$ useful and $v_1, \ldots, v_{k-1}$ not useful. Then:

**(a)** $v_k$ strictly post-dominates $B$;

**(b)** $B$ has a useful strict post-dominator, so the walk of line L14 stops at a block $N$ and never reaches the virtual exit;

**(c)** $v_k = N$.

**Proof of (a).** Write $Y = v_k$. Let $j$ be the largest index in $0, \ldots, k-1$ such that $Y$ does not strictly post-dominate $v_j$, and suppose that such a $j$ exists. $Y$ post-dominates $v_{j+1}$: if $j + 1 = k$ then $v_{j+1}$ is $Y$, and otherwise $Y$ strictly post-dominates it by the choice of $j$. So $Y$ is control dependent on $v_j$, and by (M3) the branch of $v_j$ is marked. If $j = 0$, this is the branch of $B$, which is not marked. If $j \ge 1$, then $v_j$ is useful, but $v_1, \ldots, v_{k-1}$ are not. Both cases are impossible. So no such $j$ exists, and in particular $Y$ strictly post-dominates $v_0 = B$.

**Proof of (b).** By assumption 1 there is a path from $B$ to a `ret` block, which is useful and is not $B$, since $B$ ends with a branch. Cut the path at the first useful block after $B$. By (a) that block strictly post-dominates $B$.

**Proof of (c).** By (a), $Y = v_k$ is a useful strict post-dominator of $B$. $N$ is the nearest one, so if $Y \ne N$, then $Y$ lies above $N$ on the tree path to the root, and $N$ does not appear among $v_0, \ldots, v_k$: $v_0 = B \ne N$, the blocks $v_1, \ldots, v_{k-1}$ are not useful, and $v_k = Y$. If some path from $Y$ to the exit avoids $N$, then the path from $B$ through $Y$ to the exit avoids $N$, which is impossible, because $N$ post-dominates $B$. So $N$ post-dominates $Y$. Also $Y$ post-dominates $N$, because it is above $N$ in the tree. Two nodes that post-dominate each other are equal, so $Y = N$, which is a contradiction. $\square$

## Lemma 2: the same marked statements run, with the same values

Fix an input on which the run of $P$ ends. A step of a run is *marked* if it executes a marked statement.

**Claim.** The run of $P'$ executes the same marked statements as the run of $P$, in the same order, each reading the same values and writing the same values. Between two of them $P'$ executes only jumps. $P'$ ends in the same way as $P$.

**Proof.** We follow both runs from one *meeting point* to the next. A meeting point is a moment at which both runs are at the start of the same block $X$, with the same values in every name and cell that a marked statement can read next. The runs start at a meeting point, the entry. At a meeting point:

1. $P$ runs all instructions of $X$, and $P'$ runs the marked ones, in the same order. The unmarked ones cannot trap, because every operation that may trap is critical, and they write only names, never memory.
2. Then $P$ runs the terminator of $X$:
   - a `ret` is marked, and both programs return;
   - a jump is the same in $P'$, and both runs go to the same block;
   - a marked branch reads the same value in both runs, and both go to the same block;
   - an unmarked branch goes to some successor in $P$, while $P'$ jumps to $N$, the nearest useful post-dominator of $X$. The run of $P$ ends, and it ends in a useful block: at a `ret`, or at a trap, which only a marked operation can cause. So after $X$ the run of $P$ reaches some useful block, and by Lemma 1 the first useful block it reaches is $N$. On the way it runs only statements of blocks that are not useful, so no marked statement.

In each case both runs next meet at the start of the same block, and $P$ runs no marked statement between the two meetings that $P'$ does not run. Each step of this argument uses at least one block visit of the finite run of $P$, so $P'$ also reaches the end.

It remains to show that each marked statement reads the same values in both runs. We use induction over the marked steps in their common order. Let $S$ be a marked statement that reads the name $u$.

- If $u$ is address-taken, every statement that can write $u$ is marked: the definitions of $u$ by (M1), and the stores and calls, which are critical. So the writes to $u$ before $S$ are the same marked steps in both runs. By induction they write the same values in the same order, and $P'$ runs no other write. So $u$ has the same value at $S$.
- If $u$ is not address-taken, only definitions of $u$ by name write it, because a pointer in the toy IR points to a heap cell or to an address-taken name. In the run of $P$, let $W$ be the last definition of $u$ before $S$. The part of the run from $W$ to $S$ is a path with no other definition of $u$, so $W$ reaches $S$, and by (M2) $W$ is marked. By induction $W$ writes the same value in $P'$. Between $W$ and $S$, $P'$ runs only marked statements that $P$ also runs there, and none of them defines $u$. If no definition of $u$ comes before $S$, then $u$ is a parameter, and the same argument shows that $P'$ does not change it either.

A load or a called function reads memory cells. They are written only by stores, which are marked, and by called functions, which run inside marked calls. Allocations are marked too, so both runs number the heap cells in the same way. By induction the memory is the same at every marked step.

So $S$ reads the same values, and it does the same thing in both runs: it writes the same value, takes the same branch, returns the same value, or traps. $\square$

## The theorem

**Theorem.** For every input on which the run of $P$ ends, the run of $P'$ ends with the same outcome: the same return value, or a trap. $P'$ also executes at most as many instructions and terminators as $P$.

**Proof.** The outcome follows from Lemma 2. For the count: $P'$ runs a subset of the instructions that $P$ runs, and each block that $P'$ visits stands for a different visit of $P$ to a block, so it runs at most as many terminators. $\square$

**Runs that do not end.** Suppose the run of $P$ never ends. If it executes marked statements forever, the meeting points of Lemma 2 go on forever, so the run of $P'$ does not end either. Otherwise, after its last marked statement the run of $P$ stays forever in blocks that are not useful, and $P'$ may jump past them and return. This is the case that assumption 3 excludes: the algorithm removes loops with no marked statement and so assumes that they end. A compiler for a language in which a loop with no effect may run forever must mark the branches of loops that it cannot prove to end.
