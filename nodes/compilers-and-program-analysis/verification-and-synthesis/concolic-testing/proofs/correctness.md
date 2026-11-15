---
title: The depth-first concolic search finds every path of the domain once
proves: [correctness]
status: full
---

**Setting.** $P$ is a program of the toy IR with $k$ integer parameters and only constants, copies and binary operations. $D \subseteq \mathbb{Z}^k$ is a finite set of inputs, and the start input is in $D$. SOLVE is *exact over $D$*: given a list of conditions, it returns an input of $D$ that satisfies all of them if there is one, and reports that there is none otherwise. RUN tracks every operation symbolically, as described on the page, and records no condition whose expression is a constant. We assume that every run of $P$ on an input of $D$ ends; the programs of the tests satisfy this.

A condition is a pair $(e, s)$, and an input $u$ *satisfies* it when "$e(u) \ne 0$" has the truth value $s$ and the evaluation of $e(u)$ does not trap. For an input $u$, let $\mathrm{rec}(u) = (c_1, \dots, c_m)$ be the list of conditions that RUN records on $u$, and let $\mathrm{path}(u)$ be the blocks, the kind of outcome and the trapping instruction of its run.

## Lemma 1: the record is a function of the decisions

**Claim.** Let $u$ and $u'$ be inputs, and suppose the first $i$ conditions of $\mathrm{rec}(u)$ are $c_1, \dots, c_i$ and $u'$ satisfies all of them. Then the first $i$ conditions of $\mathrm{rec}(u')$ are also $c_1, \dots, c_i$. After the $i$-th condition, the two runs reach the same point with the same symbolic store, so the next event, either the condition $c_{i+1}$ or the end of the run with a given outcome kind and position, is the same in both runs up to its sense.

**Proof.** Induction over the steps of the run of $u$. At the start, both runs are at the entry with the store $x_j \mapsto \alpha_j$. A constant, a copy or an operation updates the store in a way that does not depend on the input, so the stores stay equal. An operation on two constants is folded, and it traps in both runs or in neither. At a check or a branch whose expression $e$ is a constant, both runs take the same side, because the value of a constant does not depend on the input. At a check or a branch with a symbolic expression $e$, both runs record a condition with the same expression $e$. If it is one of $c_1, \dots, c_i$, then $u'$ satisfies it, so $e(u')$ and $e(u)$ are both nonzero or both zero, and the runs take the same side: the same successor block at a branch, the same "go on" or "trap" at a check. Here we use that the symbolic store gives the true value of each name as a function of the input, which holds by the same induction: each symbolic operation is the concrete operation applied to the symbolic operands. $\square$

**Consequences.** Call $\mathrm{dec}(u) = \mathrm{rec}(u)$, the conditions with their senses, the *decision sequence* of $u$. Let $T_D$ be the set of the decision sequences of the inputs of $D$ and of all their prefixes.

- (a) $T_D$ is a binary tree: a prefix $(c_1, \dots, c_i)$ fixes the expression of $c_{i+1}$ by Lemma 1, so a node has at most two children, $(c_1, \dots, c_i, (e, \mathit{true}))$ and $(c_1, \dots, c_i, (e, \mathit{false}))$.
- (b) No decision sequence of an input is a proper prefix of another: by Lemma 1, after the same prefix both runs either end or record a further condition. So the decision sequences are exactly the leaves of $T_D$.
- (c) The leaves are in one-to-one correspondence with the paths $\{\mathrm{path}(u) : u \in D\}$. Two inputs with the same decision sequence have the same path by Lemma 1. Two different leaves first differ at a condition $(e, s)$ against $(e, \neg s)$. At a branch, the two runs go to different blocks, because a branch with equal targets records nothing. At a check, one run traps there and the other goes on, so the two paths differ in their outcome, in their blocks or in the trapping instruction.
- (d) For a node $q$ of $T_D$, let $\mathrm{Leaves}(q)$ be the leaves below $q$. Then an input of $D$ satisfies all conditions of $q$ if and only if its decision sequence lies in $\mathrm{Leaves}(q)$. This is Lemma 1 in one direction; in the other, a run whose decision sequence extends $q$ satisfies the conditions of $q$ by definition.

## Lemma 2: the invariant

Write the stack as $(d_1, f_1), \dots, (d_j, f_j)$ from the bottom, and $\bar{d_i}$ for $(d_1, \dots, d_{i-1}, \neg d_i)$, the *other side* at depth $i$. Let $O$ be the set of the decision sequences of the runs output so far.

**Claim.** The following hold.

- (I1) At line L3, the input $v$ is in $D$ and satisfies $d_1, \dots, d_j$, and $O = \bigcup_{i : f_i} \mathrm{Leaves}(\bar{d_i})$.
- (I2) At line L8, $(d_1, \dots, d_j)$ is a node of $T_D$ and $O = \bigcup_{i : f_i} \mathrm{Leaves}(\bar{d_i}) \cup \mathrm{Leaves}(d_1, \dots, d_j)$.

**Proof.** Initially the stack is empty, $O$ is empty, and $v$ is the start input, in $D$. So (I1) holds.

*From line L3 to line L8.* By (I1), $v$ satisfies $d_1, \dots, d_j$, which are the first $j$ conditions of the run of some earlier input (or $j = 0$). By Lemma 1 its record starts with $d_1, \dots, d_j$, so line L5 pushes exactly the rest $d_{j+1}, \dots, d_m$ with the flag false, and line L6 adds the leaf $\ell = (d_1, \dots, d_m)$ to $O$. The new entries have false flags, so the union over the done entries is unchanged. By (b), $\ell$ is a leaf, so $\mathrm{Leaves}(\ell) = \{\ell\}$, and (I2) holds with the new stack.

*Line L10.* The top entry $(d_j, \mathit{true})$ is popped. Every leaf below $(d_1, \dots, d_{j-1})$ lies below $(d_1, \dots, d_j)$ or below $\bar{d_j}$, and both sets are in $O$ by (I2). After the pop, (I2) holds with $\mathrm{Leaves}(d_1, \dots, d_{j-1})$.

*Line L12.* The solver is exact, so no input of $D$ satisfies $d_1, \dots, d_{j-1}, \neg d_j$, and by (d) $\mathrm{Leaves}(\bar{d_j})$ is empty. After the pop, (I2) holds as in the previous case.

*Line L13.* The solver returns $v' \in D$ that satisfies $d_1, \dots, d_{j-1}, \neg d_j$, and the top becomes $(\neg d_j, \mathit{true})$. Its other side is $(d_1, \dots, d_j)$, all of whose leaves are in $O$ by (I2), and the flag was false, so the union over the done entries now covers exactly what (I2) covered. So $O = \bigcup_{i : f_i} \mathrm{Leaves}(\bar{d_i})$ with the new stack, and $v'$ satisfies the new stack. (I1) holds. $\square$

## Theorem

**Claim.** The search stops. The runs that it outputs have pairwise different paths, and their paths are exactly $\{\mathrm{path}(u) : u \in D\}$. Exactly $R - 1$ solver calls succeed, where $R$ is the number of runs.

**Proof.** *Each run is new.* At line L3, by (I1), $v$ satisfies $d_1, \dots, d_j$, so by (d) its leaf lies below the current stack. Each set $\mathrm{Leaves}(\bar{d_i})$ is disjoint from $\mathrm{Leaves}(d_1, \dots, d_j)$, because their sequences differ at depth $i$. So the new leaf is not in $O$.

*Termination.* Each pass of the outer loop outputs a new leaf of $T_D$, and $T_D$ has at most $|D|$ leaves, since each leaf is the decision sequence of an input of $D$. So the outer loop runs at most $|D|$ times. Each pass of the inner loop pops an entry or leaves the loop, and each pass of the outer loop pushes finitely many entries, so the inner loop stops too.

*Completeness.* The search returns at line L8 with an empty stack. Then (I2) gives $O = \mathrm{Leaves}(\varepsilon)$, all the leaves of $T_D$. By (c), the paths output are exactly the paths of the inputs of $D$, and since the leaves output are pairwise different, so are the paths.

*Solver calls.* Every run but the first follows exactly one successful call on line L13, and every successful call is followed by a run. $\square$

**Remarks.** The finiteness of $D$ is used only for termination. With a solver that is exact over all of $\mathbb{Z}^k$, the invariant and the argument "each run is new" still hold, so no path is output twice, but on a program with an infinite tree the search need not stop, and it can stay forever in one infinite branch. If RUN replaces a symbolic subterm by its concrete value, Lemma 1 fails, a run can leave the predicted prefix, and the implementation reports the divergence.
