---
title: Each MCL iterate is column stochastic and stays inside the components, the read-out is a partition that refines the components, and a fixed point of inflation has uniform columns
proves: [correctness]
status: sketch
---

This page proves the facts that hold for every run of MCL. It does not prove that the loop of lines L3 to L8 converges: no such proof is known to this page, and the implementation stops after a fixed number of iterations if the change stays above $\varepsilon$. The status is a sketch for that reason; each lemma below is proved in full.

Let $G$ have vertices $V = \{0, \ldots, n-1\}$ and weights $A_{ij} = A_{ji} \ge 0$, and let $A$ be the matrix of line L1, so $A_{jj} \ge 1$ for every $j$. Let $e \ge 2$ be an integer, $r > 1$, and $0 \le \theta < 1/n$. Write $V_1, \ldots, V_c$ for the vertex sets of the connected components of $G$, and say that a matrix $X$ *respects the components* if $X_{ij} = 0$ whenever $i$ and $j$ lie in different components.

**Lemma 1 (column stochastic).** Every matrix $M$ that the algorithm holds after line L2 or line L7 is column stochastic.

*Proof.* After line L2, column $j$ of $A$ has the entry $A_{jj} \ge 1 > 0$, so its sum is positive, and dividing by it gives a nonnegative column with sum 1.

Assume $M$ is column stochastic. Then $M^e$ is column stochastic: for column-stochastic $X$ and $Y$, $(XY)_{ij} = \sum_k X_{ik} Y_{kj} \ge 0$ and $\sum_i (XY)_{ij} = \sum_k Y_{kj} \sum_i X_{ik} = \sum_k Y_{kj} = 1$. Line L6 raises the entries of a column $x$ of $M^e$ to the power $r$; since $x$ sums to 1 and has $n$ entries, its largest entry is at least $1/n > 0$, so the column of powers has a positive sum and the first division of line L7 gives a column $y$ with sum 1. The largest entry of $y$ is again at least $1/n > \theta$, so pruning keeps it, the column still has a positive sum, and the second division gives a nonnegative column with sum 1. $\square$

**Lemma 2 (components).** Every matrix $M$ that the algorithm holds respects the components.

*Proof.* $A_{ij} > 0$ with $i \ne j$ means that $\{i, j\}$ is an edge, so $i$ and $j$ lie in the same component; so $A$ respects the components, and so does $M$ after line L2, which only rescales columns. If $X$ and $Y$ respect the components and $i, j$ lie in different components, then in $(XY)_{ij} = \sum_k X_{ik} Y_{kj}$ each $k$ differs in component from $i$ or from $j$, so each term is 0. So $M^e$ respects the components. Lines L6 and L7 map zero entries to zero entries ($0^r = 0$, and a rescaled or pruned zero is zero), so they keep the property. $\square$

**Lemma 3 (the read-out).** Lines L9 and L10 return a partition of $V$, and each of its parts lies inside one component of $G$.

*Proof.* The connected components of any graph on $V$ partition $V$. By Lemma 2, every edge $\{i, j\}$ of $H$ has $M_{ij} > 0$ or $M_{ji} > 0$, so $i$ and $j$ lie in the same component of $G$. A path in $H$ therefore stays inside one component of $G$, and so does each component of $H$. $\square$

**Lemma 4 (fixed points of inflation).** Let $x$ be a probability vector with $\Gamma_r x = x$, that is $x_i^r / \sum_k x_k^r = x_i$ for all $i$. Then all the nonzero entries of $x$ are equal, so $x$ is uniform on its support $S$, with value $1/|S|$.

*Proof.* Let $s = \sum_k x_k^r > 0$. For $x_i > 0$, dividing $x_i^r = s\, x_i$ by $x_i$ gives $x_i^{r-1} = s$, and since $r - 1 > 0$, $x_i = s^{1/(r-1)}$, the same value for each $i$ in $S$. The entries sum to 1, so the value is $1/|S|$. $\square$

**Lemma 5 (stopping).** The loop of lines L3 to L8 ends.

*Proof.* Line L8 ends the loop when the change is at most $\varepsilon$ or when the number of iterations reaches the fixed limit, and each iteration raises that number by 1. $\square$

**Theorem.** MCL($G$, $e$, $r$, $\theta$, $\varepsilon$) stops and returns a partition of $V$ in which each cluster lies inside one connected component of $G$. Every matrix it computes is column stochastic, and if it stops at a matrix whose columns are fixed by inflation, each column is uniform on its support.

*Proof.* Lemma 5 gives termination, Lemma 3 the partition and the components, Lemma 1 the stochasticity and Lemma 4 the shape of the columns. $\square$

**What is not proved here.** That the loop reaches a change below $\varepsilon$ for every input, and that the limit is doubly idempotent ($M^2 = M$ and $\Gamma_r M = M$). Van Dongen studies these limits in the SIAM paper cited on the node page: he describes their structure as attractor systems with the vertices that flow to them, and shows that the clustering they define is stable under small perturbations, so that the iteration, once close to such a limit, keeps its clustering.

∎
