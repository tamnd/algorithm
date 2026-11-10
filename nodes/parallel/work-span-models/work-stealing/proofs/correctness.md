---
title: Work stealing runs each node exactly once, after its predecessors, in at most T_1 steps
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a DAG $G$ with $T_1$ unit-time nodes and one root, in which each node has at most two successors, and $p \ge 1$. A node *becomes enabled* in the step in which its last predecessor is executed; the root is enabled at the start. Number the steps $1, 2, \ldots$. In a step, each processor that has an assigned node at the start of the step runs lines L2 to L8, one processor at a time in the order of their numbers, and then each other processor runs lines L9 to L11, one processor at a time. So the executed node that *enables* $v$ is well defined: it is the predecessor of $v$ that is executed last in this order. A *place* is the assigned slot of one processor or one position in one deque.

**Lemma 1 (one place).** At the start of each step, each node that is enabled and not yet executed is in exactly one place, and no other node is in any place.

*Proof.* By induction on the steps. At the start of step 1, only the root is enabled; it is assigned to processor 0, and all deques are empty. Assume the claim at the start of a step. We look at each change of a place in the step.

- Line L3 executes the node $u$ in the slot of $q$. After this, $u$ is executed, and lines L5 to L8 overwrite the slot, so $u$ leaves its only place.
- A node $v$ that becomes enabled in the step has a predecessor $u$ that is executed in this step, and $v$ was not enabled before. If $u$ enables two nodes, line L5 puts one in the slot of $q$ and the other at the bottom of $D_q$. If $u$ enables one node, line L6 puts it in the slot of $q$. Since each node has one last predecessor, and the last predecessor is executed once (by the induction hypothesis, it was in one place), $v$ is put in exactly one place.
- Line L7 moves a node from the bottom of $D_q$ to the slot of $q$, which is free after line L3.
- Line L11 moves a node from the top of $D_r$ to the slot of the thief $q$. The slot of $q$ is free, because $q$ is a thief, and the node leaves $D_r$. Thieves act one at a time, so a second thief sees the deque without that node.

Each change keeps each enabled, unexecuted node in exactly one place and puts no other node in a place. So the claim holds at the start of the next step. $\square$

**Lemma 2 (busy owner).** At the start of each step, if $D_q$ is not empty, then $q$ has an assigned node.

*Proof.* By induction on the steps. At the start, all deques are empty. In a step, $D_q$ grows only in line L5, which also gives $q$ an assigned node. The slot of $q$ becomes empty only in line L8, and line L8 runs only when $D_q$ is empty. A thief removes nodes from $D_q$ but does not change the slot of $q$. A thief $q$ with an empty slot does not change $D_q$, and if it steals, its slot is no longer empty. So the claim holds at the end of the step. $\square$

**Theorem.** WORK-STEAL stops after at most $T_1$ steps. Each node of $G$ is executed exactly once, and in a later step than each of its predecessors. In each step at most $p$ nodes are executed, and $p \cdot T_p = T_1 + A$, where $A$ is the number of steal attempts.

*Proof.* A node is executed only in line L3, from the slot of a processor. By Lemma 1, a node is in a slot only after it becomes enabled, and it leaves all places when it is executed, so it is executed at most once. A node $v$ becomes enabled in the step in which its last predecessor is executed. In that step it is put in a place, and it is executed at the earliest in the next step, because line L3 of each processor runs before lines L5 to L11 put $v$ in a place. So $v$ runs in a later step than each of its predecessors.

Now assume that at the start of some step, a node is not executed. Among the unexecuted nodes, take a node $v$ that has no unexecuted predecessor. Such a node exists because $G$ is acyclic. If $v$ is the root, it is enabled. Otherwise all predecessors of $v$ are executed, so $v$ became enabled when the last of them was executed. By Lemma 1, $v$ is in a slot or in a deque. If $v$ is in the slot of $q$, then $q$ has an assigned node. If $v$ is in $D_q$, then $q$ has an assigned node by Lemma 2. So in this step, at least one processor executes a node in line L3. Each step before the end executes at least one node, and there are $T_1$ nodes, each executed at most once. So the loop stops after at most $T_1$ steps, and when it stops, every node is executed, so each node is executed exactly once.

In each step, each processor runs line L3 once (it executes one node) or line L10 once (it makes one steal attempt), and not both. So at most $p$ nodes run in a step, and summing over the $T_p$ steps gives $p \cdot T_p = T_1 + A$. $\blacksquare$
