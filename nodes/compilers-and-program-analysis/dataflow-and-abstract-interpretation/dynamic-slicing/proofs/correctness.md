---
title: The forward method returns the closure of the dynamic dependence graph, and that closure holds for its input
proves: [correctness, termination, complexity]
status: full
---

**Setting.** Fix a program, an input and a criterion $(p, q, V)$. The run is a finite sequence of statement instances $1, 2, \ldots, T$ (it stops at a `ret`, a trap or the end of the fuel). Instance $k$ is an execution of statement $s_k$, in a visit to block $b_k$. Let $t$ be the instance at which the run reaches $p$ for the $q$-th time, if it exists.

For an instance $k$ and a name $x$, let $w(k, x)$ be the last instance before $k$ that writes $x$, or none. For an instance $k$, let $c(k)$ be the latest branch instance $j < k$ such that the block $\mathrm{ipdom}(b_j)$ is not entered by the run after instance $j$, up to and including the visit of $k$; or none. The *parents* of $k$ are $w(k, y)$ for each name $y$ that $s_k$ reads, and $c(k)$. The *roots* are $w(t, x)$ for $x \in V$, and $c(t)$. Let $K$ be the set of instances reachable from the roots through parents, roots included. The dynamic slice is $\{ s_k : k \in K \}$. For an instance $k$, let $K(k)$ be the set of instances reachable from $k$ through parents, $k$ included, and $\sigma(k) = \{ s_j : j \in K(k) \}$.

Since $K(k) = \{k\} \cup \bigcup_{m \text{ parent of } k} K(m)$, we have $\sigma(k) = \{s_k\} \cup \bigcup_{m} \sigma(m)$ over the parents $m$ of $k$.

## 1. The open list

**Lemma 1.** Let $j_1 < j_2$ be two branch instances of the same block $X$. At every point after $j_2$, if $j_1$ is open (its ipdom block not entered since $j_1$), then $j_2$ is open too.

*Proof.* Both close when the run enters $\mathrm{ipdom}(X)$, and $j_2$ is later, so every entry of that block after $j_2$ is also after $j_1$. $\square$

So at any point, the latest open branch instance is never an older instance of a block that has a later open instance. Line L8 removes exactly those older instances, and line L9 removes the instances that close when the run enters the next block.

**Lemma 2.** Before instance $k$ runs, the list holds, in time order, the open branch instances that are the latest instance of their block, each with the set $\sigma(j)$. Its last entry is $c(k)$, or the list is empty and $c(k)$ is none.

*Proof.* By induction on $k$. At the start the list is empty and no branch has run. A non-branch instance changes nothing. A `jump` changes only the block; line L9 then drops the entries whose ipdom is the new block, and those are exactly the instances that close. For a branch instance $j$ of block $X$, line L8 drops the older entry of $X$, if there is one, and appends $j$ with the set $T$ of line L6, which is $\sigma(j)$ by Lemma 3 below, applied at $j$; line L9 then closes entries as for a `jump`, $j$ included if its successor is its ipdom block. The list is in time order because entries are appended. Every open instance that is not on the list has a later open instance of its block, by Lemma 1, so the latest open instance is on the list and is its last entry. That is $c(k)$ by definition. $\square$

## 2. The sets per name

**Lemma 3.** Before instance $k$ runs, for every name $x$: $DS[x] = \sigma(w(k, x))$ if $w(k, x)$ exists, and $DS[x] = \emptyset$ if $x$ is a parameter not yet written. At line L6 for instance $k$, $T = \sigma(k)$.

*Proof.* By induction on $k$, together with Lemma 2. Line L1 gives the case $k = 1$. At instance $k$, line L3 sets $C$ to $\sigma(c(k))$ by Lemma 2, or to $\emptyset$. Line L6 sets $T = \{s_k\} \cup C \cup \bigcup_y DS[y]$ over the names $y$ that $s_k$ reads. By the induction hypothesis $DS[y] = \sigma(w(k, y))$, or $\emptyset$ for a parameter not yet written, which has no parent instance. So $T = \sigma(k)$ by the recursion above. If $s_k$ writes $x$, line L7 sets $DS[x] = \sigma(k)$, and $w(k + 1, x) = k$. The other names keep their last writer and their set. $\square$

**Theorem 1 (correctness).** If the run reaches $p$ for the $q$-th time, line L5 returns the dynamic slice. Otherwise the method returns none.

*Proof.* Lines L3 to L5 run at instance $t$ before it executes. By Lemmas 2 and 3, the returned set is $\sigma(c(t)) \cup \bigcup_{x \in V} \sigma(w(t, x))$, which is $\{ s_k : k \in K \}$. If the run stops first, the loop ends without line L5. $\square$

**Termination and cost.** The loop runs once per instance, so at most $T$ times. Let $n$ be the number of statements and $b$ the number of blocks. Every set holds statements, so it has at most $n$ elements, and a statement of the toy IR reads at most two names. So line L6 costs $O(n)$. The list has at most one entry per block, so lines L8 and L9 cost $O(b)$, and $b \le n$. The total time is $O(T n)$. The method keeps one set per name and one per list entry, so the extra space is $O((v + b) n)$ for $v$ names. It does not store the run.

## 3. What the slice means

**Theorem 2 (the slice holds for its input).** Run the program on the same input again, but make every branch instance go the way it went in the first run, and let every instance of a statement outside the slice write any value it likes. Then at instance $t$ the names of $V$ have the same values as in the first run.

*Proof.* The forced branches give the same sequence of instances, so $w$ is the same function in both runs. We show by induction on $k$ that every $k \in K$ that writes a name writes the same value in both runs. Since $s_k$ is in the slice, it computes its result from the values of the names it reads, as in the first run. Each such value was written by $w(k, y)$, a parent of $k$ and so in $K$, and earlier than $k$; by induction it is the same, or it is the parameter value, which is the same. At $t$, the value of $x \in V$ comes from $w(t, x)$, a root, so it is the same. $\square$

The proof needs the same input and the same path. For another input the parents are different instances, and a statement that is not in the slice can then write a value that reaches $V$. For the same input, if a branch outside the slice goes the other way, a statement that never ran in the first run can overwrite a name that the slice reads. So the theorem does not give an executable program: to get one, Korel and Laski add statements, and their slices can be larger.
