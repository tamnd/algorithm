---
title: Nonrecursive DFS produces the same times and parents as recursive DFS
proves: [correctness, termination]
status: full
---

Fix a graph $G$, an order of $V$ and an order of each list. Let $R$ be the recursive procedure DFS of the [depth-first search](/depth-first-search/) page and $I$ the procedure ITERATIVE-DFS. We show that they compute the same $d$, $f$ and $\pi$.

**Steps.** Cut the run of $R$ into steps. A *root step* is one test of line L4 of $R$ (with the call it may start, up to the discovery of its root). Inside a call DFS-VISIT$(x)$, an *edge step* is one test of a list entry $v$ by the loop, with the discovery of $v$ if $v$ is white, and an *end step* is the end of the call, which sets $f[x]$. Cut the run of $I$ in the same way: a root step is one test of line L4, an edge step is one execution of lines L9 to L11, and an end step is one execution of line L12.

**Claim.** Consider the two runs after they have done the same number of steps of the same kinds since the same root step. Then:

1. both have the same colours, times $d$ and $f$, parents and clock;
2. the stack $S$ of $I$ lists, from bottom to top, exactly the vertices whose calls in $R$ are active, from the oldest to the newest;
3. for each $x$ on $S$, the call of $x$ in $R$ has tested exactly the first $\mathrm{next}[x] - 1$ entries of $\mathrm{Adj}[x]$.

*Proof.* By induction on the number of steps. At the start, nothing has happened in either run, both clocks are 0, $S$ is empty and no call is active.

*Root step.* Both runs are in their outer loops with no active call and an empty stack, by part 2, and they test the same vertex $u$, which has the same colour in both, by part 1. If $u$ is white, $R$ calls DFS-VISIT$(u)$, which makes $u$ gray and sets $d[u]$ to the next clock value, and $I$ does the same at line L5 and pushes $u$, with $\mathrm{next}[u] = 1$ and no entry tested. All three parts hold.

*Step inside a tree.* Let $x$ be the newest active call of $R$, which is the call that runs. By part 2, $x$ is the top of $S$, so line L7 gets the same $x$. By part 3, $R$'s loop in the call of $x$ has tested $\mathrm{next}[x] - 1$ entries.

- If $\mathrm{next}[x] \le |\mathrm{Adj}[x]|$, the loop of $R$ tests the entry $v = \mathrm{Adj}[x][\mathrm{next}[x]]$ next, and line L9 reads the same $v$ and increases $\mathrm{next}[x]$. If $v$ is white (the same in both runs), $R$ sets $\pi[v] = x$ and calls DFS-VISIT$(v)$, which makes $v$ gray and sets $d[v]$, and $I$ does the same at line L11 and pushes $v$ on top of $x$. The new call is the newest, with no entry tested, and $\mathrm{next}[v] = 1$ because $v$ was white and is pushed for the first time. If $v$ is not white, neither run changes anything else.
- If $\mathrm{next}[x] > |\mathrm{Adj}[x]|$, the call of $x$ in $R$ has tested its whole list, so it makes $x$ black, sets $f[x]$ and returns, and the next active call is the one below it. Line L12 does the same and pops $x$.

In each case, the two runs make the same change, and all three parts hold again. $\square$

**Termination.** Each edge step increases some $\mathrm{next}[x]$, which never exceeds $|\mathrm{Adj}[x]| + 1$ and is never reset, because a vertex is pushed only while it is white and is then gray or black for ever. Each end step pops a vertex, and each vertex is pushed at most once. So the loop of line L6 runs at most $m + n$ times in total, where $m$ is the total length of the lists, and $I$ terminates.

**Theorem.** ITERATIVE-DFS$(G)$ returns the same $d$, $f$ and $\pi$ as the recursive DFS$(G)$ with the same orders.

*Proof.* The runs of $R$ and $I$ have the same sequence of steps by the claim: whenever one of them can do an edge step or an end step, so can the other, and when the stack is empty, both are in the outer loop at the same vertex. When $I$ terminates, all of its steps are matched by steps of $R$, both outer loops have tested all vertices, and part 1 gives the same $d$, $f$ and $\pi$. $\blacksquare$
