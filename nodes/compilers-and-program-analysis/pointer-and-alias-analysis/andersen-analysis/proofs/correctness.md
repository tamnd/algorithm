---
title: Andersen's worklist algorithm computes the least solution of the subset constraints in O(n^3 + m) time
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The program is a set $S$ of $m$ statements over a set $V$ of $n$ variables. Every variable is also a location, so a points-to assignment is a map $P : V \to 2^V$. The statements give the constraints

- $p = \&a$: $a \in P(p)$;
- $p = q$: $P(q) \subseteq P(p)$;
- $p = {*q}$: $P(a) \subseteq P(p)$ for every $a \in P(q)$;
- ${*p} = q$: $P(q) \subseteq P(a)$ for every $a \in P(p)$.

A *solution* is an assignment that meets all of them. Assignments are ordered pointwise by $\subseteq$, with the pointwise union as join and the empty sets as bottom. This is the order of abstract interpretation in the direction of Cousot: a larger assignment says more pointers may point to more places, so it is less precise and safer. "Least" below means least in this order.

**Lemma 1 (the least solution exists).** The pointwise intersection of any family of solutions is a solution. So there is a least solution $L$, the intersection of all solutions.

*Proof.* Let $P_i$ be solutions and $Q(v) = \bigcap_i P_i(v)$. For $p = \&a$, $a$ is in every $P_i(p)$. For $p = q$, $Q(q) \subseteq P_i(q) \subseteq P_i(p)$ for each $i$. For $p = {*q}$ and $a \in Q(q)$, $a \in P_i(q)$, so $Q(a) \subseteq P_i(a) \subseteq P_i(p)$ for each $i$. The store case is the same. The full assignment $P(v) = V$ is a solution, so the family is not empty. $\square$

The same $L$ is the least fixed point of the monotone map $F$ that adds to $P$ every fact one rule forces from $P$, by the Knaster-Tarski theorem; Lemma 1 is the direct form of this.

**The algorithm.** Write $E$ for the set of edges, $pts$ and $delta$ for the arrays of the pseudocode and $W$ for the worklist. An edge $u \to v$ stands for $pts(u) \subseteq pts(v)$. Line L3 puts the addresses in, line L4 adds the copy edges, and lines L8 and L9 add the edges that a load or a store needs for each new element of the set of its pointer. PROPAGATE adds to $pts(v)$ the part of a set that is new and records it in $delta(v)$.

**Lemma 2 (every fact is forced).** At all times, $pts(v) \subseteq L(v)$ for every $v$, and $L(u) \subseteq L(v)$ for every edge $u \to v$.

*Proof.* Both hold at the start, when all sets and $E$ are empty. Line L3 adds $a$ to $pts(p)$ only for a statement $p = \&a$, and $a \in L(p)$. Line L4 adds $q \to p$ for a statement $p = q$, and $L(q) \subseteq L(p)$. Line L8 adds $a \to p$ for a statement $p = {*n}$ and an $a \in pts(n) \subseteq L(n)$, so $L(a) \subseteq L(p)$ because $L$ is a solution. Line L9 is the same for a store. PROPAGATE along an edge $u \to w$ adds only elements of $pts(u) \subseteq L(u) \subseteq L(w)$. In line L10, $d \subseteq pts(n)$ and the edges are those of $E$. $\square$

**Lemma 3 (what is done is done).** Call $done(v) = pts(v) \setminus delta(v)$. The following hold each time line L5 tests the loop condition:

1. If $delta(v) \neq \emptyset$, then $v \in W$.
2. Every statement $p = \&a$ has $a \in pts(p)$, and every statement $p = q$ has the edge $q \to p$.
3. For every edge $u \to v$, $done(u) \subseteq pts(v)$.
4. For every statement $p = {*q}$ and every $a \in done(q)$, the edge $a \to p$ is in $E$; for every statement ${*p} = q$ and every $a \in done(p)$, the edge $q \to a$ is in $E$.

*Proof.* Parts 1 and 2 are clear: every write to $delta(v)$ comes with $push(v)$, $v$ leaves $W$ only in line L6 where $delta(v)$ is emptied, and lines L3 and L4 run before the loop. Before the loop, $done(v) = \emptyset$ for every $v$: line L3 puts $a$ into both $pts(p)$ and $delta(p)$, and PROPAGATE does the same with the new elements. So parts 3 and 4 hold then. Consider one pass of lines L6 to L10 at node $n$, with $d = delta(n)$. Sets only grow, and an element enters $done(v)$ only when $v = n$ and it is in $d$, because elsewhere new elements go into $pts(v)$ and $delta(v)$ together. So in this pass the new part of $done(u)$ is empty if $u \neq n$ and is $d$ if $u = n$. Part 3 for an edge $u \to v$: if the edge was added in this pass, ADD-EDGE sent all of $pts(u)$ to $v$ at that moment, and that set already held the old $done(u)$ and $d$. If the edge was there before, the old $done(u)$ was already in $pts(v)$, and for $u = n$ line L10 sends $d$ along every edge of $n$. Part 4: the new part of $done(n)$ is $d$, and lines L8 and L9 add the needed edges for each element of $d$. For $v \neq n$, $done(v)$ does not grow. $\square$

**Theorem 1 (correctness).** The loop stops, and then $pts = L$.

*Proof.* Each pass of the loop body takes a node out of $W$, and a node is put back only when some $pts(v)$ grows. By Lemma 2, $\sum_v |pts(v)| \le n^2$, so there are at most $n^2$ pushes after line L4, plus at most $n$ before, and the loop stops. Then $W$ is empty, so every $delta(v)$ is empty by part 1 of Lemma 3, and $done = pts$. Parts 2 to 4 now say that $pts$ meets every constraint: for $p = {*q}$ and $a \in pts(q)$ the edge $a \to p$ is in $E$, so $pts(a) \subseteq pts(p)$ by part 3, and the other forms are the same. So $pts$ is a solution, $L \subseteq pts$ by Lemma 1, and $pts \subseteq L$ by Lemma 2. $\square$

**Soundness for the program.** A flow-insensitive analysis must cover every run that executes the statements of $S$ in any order, any number of times. Let $val(v)$ be the location whose address $v$ holds in such a run, or none. Then $val(v) \in L(v)$ whenever $val(v)$ is defined, at every moment. This holds at the start, when nothing is defined. A step $p = \&a$ sets $val(p) = a \in L(p)$. A step $p = q$ sets $val(p) = val(q) \in L(q) \subseteq L(p)$. A step $p = {*q}$ with $val(q) = b$ sets $val(p) = val(b) \in L(b) \subseteq L(p)$, since $b \in L(q)$. A step ${*p} = q$ with $val(p) = b$ sets $val(b) = val(q) \in L(q) \subseteq L(b)$. Every path through a control flow graph made of these statements is such a run, so the result holds for the program under any control flow.

**Theorem 2 (time).** With hash sets, the algorithm takes $O(n^3 + m)$ expected time and $O(n^2 + m)$ space. With an $n \times n$ bit matrix for $E$ and bit vectors for the sets, the same bound holds in the worst case, counting word operations on vectors of $n$ bits as $O(n)$.

*Proof.* Reading the statements and filling the tables of loads and stores, without repeats, costs $O(m)$; after that there are at most $n^2$ distinct loads and $n^2$ distinct stores. Count the rest.

- *Edges.* There are at most $n^2$ distinct edges. Each one is added once, and its call of PROPAGATE costs $O(|pts(u)|) = O(n)$. Total $O(n^3)$.
- *Elements taken from delta.* An element $a$ enters $pts(v)$ once, so it is in the $d$ of line L6 for $v$ at most once. The $n^2$ pairs $(v, a)$ each cost, in lines L8 and L9, one test of ADD-EDGE per load and per store of $v$. The distinct loads and stores of all nodes number at most $2n^2$ in total, and each is met at most $n$ times, once per $a$, so these tests cost $O(n^3)$.
- *Line L10.* The pass at $v$ sends $d$ along at most $n$ edges at cost $O(|d|)$ each. Since each element is in the $d$ of $v$ at most once, the total over all passes at $v$ is $O(n \cdot n)$, and over all $v$ it is $O(n^3)$.
- *Worklist.* At most $n^2 + n$ pushes and pops, $O(1)$ each.

The space is the $O(n^2)$ edges and set elements plus the $O(m)$ statements. $\square$

The bound is for the worklist with difference propagation. A plain round-robin iteration, which applies every constraint in each round until no set changes, also reaches $L$, but each of up to $n^2$ rounds can cost $\Theta(m n)$.
