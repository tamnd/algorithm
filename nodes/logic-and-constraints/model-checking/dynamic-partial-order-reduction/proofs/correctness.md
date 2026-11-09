---
title: DPOR is sound, and with persistent backtrack sets it meets every trace of maximal executions
proves: [correctness]
status: sketch
---

We use the program model and the pseudocode of the page. The state space is acyclic and finite, so every execution is finite. A *maximal* execution from a state $s$ is an execution from $s$ that ends in a state where no thread is enabled. For a thread $p$ that does not move, its next step $\mathit{next}(s, p)$ stays the same instruction, so we may speak of "the next step of $p$" along an execution that avoids $p$.

Parts 1 and 2 below are complete proofs. Part 3, the fact that DPOR computes persistent sets, is a sketch of the proof of Flanagan and Godefroid (POPL 2005).

## Part 1. Independence in the program model

**Lemma 1.** Let $a$ and $b$ be next steps of two different threads, independent in the sense of the page (no common variable or lock that one of them writes). Then, in any state $s$:

1. executing $b$ does not change whether $a$ is enabled;
2. if both are enabled in $s$, then $s \cdot a \cdot b = s \cdot b \cdot a$.

*Proof.* A read or write step is always enabled. A lock or unlock step on lock $l$ is enabled according to the owner of $l$ only, and $b$ does not write $l$, because a lock step writes its lock and $a$, $b$ are independent. This gives (1). For (2), $a$ changes only the program counter and register of its thread and the variables or locks it writes, and its effect depends only on what it reads; $b$ writes none of what $a$ reads or writes, and the converse also holds, so the two orders give the same state. $\square$

## Part 2. Soundness, and persistent sets suffice

**Lemma 2 (soundness).** Each execution that EXPLORE builds is an execution of the program, and each state recorded as final is a reachable state in which no thread is enabled.

*Proof.* Line L9 extends $E$ only by the next step of a thread $p$ in $\mathit{backtrack}(s)$. A thread enters this set at line L6 (enabled in $s$ by choice), at line L4 (enabled in $\mathit{pre}(E, i)$ by the test), or at line L5 (enabled by the definition of $E_i$); the set of a state is only changed while that state is on the current execution, and the state does not change, so $p$ is enabled when line L9 runs. The final-state test is applied to the last state of $E$. $\square$

**Definition.** A set $T$ of threads enabled in $s$ is *persistent* in $s$ if for every execution $s = s_0 \xrightarrow{a_1} s_1 \cdots \xrightarrow{a_k} s_k$ in which no $a_j$ is a step of a thread in $T$, each $a_j$ is independent with the next step of each thread in $T$.

**Theorem 3 (persistent sets meet every trace).** Suppose a depth-first search explores, from each state $s$ it visits in which some thread is enabled, the next step of each thread of a nonempty persistent set $P(s)$. Then for each visited state $s$ and each maximal execution $w$ from $s$, the search explores from $s$ a maximal execution that is equivalent to $w$, that is, the same Mazurkiewicz trace. In particular, it reaches every reachable final state, including every deadlock.

*Proof.* By induction on the length of $w$. If no thread is enabled in $s$, then $w$ is empty and there is nothing to show. Otherwise $w = a_1 a_2 \ldots a_m$ with $m \ge 1$.

*Some step of $w$ belongs to a thread of $P(s)$.* If not, pick $p \in P(s)$; it is enabled in $s$. By persistence every $a_j$ is independent with the next step of $p$, so by Lemma 1(1) the step of $p$ stays enabled along $w$, and it is enabled in the last state of $w$. This contradicts the maximality of $w$.

*Move it to the front.* Let $k$ be the least index such that $a_k$ is a step of a thread $p \in P(s)$. Then $a_1, \ldots, a_{k-1}$ are steps of threads outside $P(s)$, so by persistence each is independent with $a_k$, which is the next step of $p$ in $s$. By Lemma 1(1), $a_k$ is enabled in each of $s_0, \ldots, s_{k-1}$. Swap $a_k$ with $a_{k-1}$ by Lemma 1(2): both are enabled in $s_{k-2}$, and the swap gives the same state $s_k$. Repeating this $k - 1$ times gives the execution $w' = a_k\, a_1 \ldots a_{k-1}\, a_{k+1} \ldots a_m$, which is equivalent to $w$ and ends in the same state.

*Use the induction hypothesis.* The search explores the step $a_k$ of $p$ from $s$, so it visits $s' = s \cdot a_k$. The rest of $w'$ is a maximal execution from $s'$ of length $m - 1$. By induction the search explores from $s'$ a maximal execution equivalent to it, and prefixing $a_k$ gives an explored execution from $s$ equivalent to $w'$, hence to $w$. Equivalent executions end in the same state, by Lemma 1(2). $\square$

## Part 3. DPOR explores persistent sets (sketch)

**Claim (Flanagan and Godefroid 2005).** In an acyclic state space, when EXPLORE returns from a state $s$ (when the loop of lines L7 to L9 ends), the set $\mathit{done}(s)$ is persistent in $s$.

With Theorem 3, the claim gives the result of the page: DPOR reaches every final state and explores at least one execution of each Mazurkiewicz trace of maximal executions. The proof in the paper goes by contradiction, in outline as follows.

1. Suppose that some state $s$ is a counterexample, and choose one that is left last among all counterexamples, so that every state explored below $s$ satisfies the claim.
2. Then there are $p \in \mathit{done}(s)$ and an execution $a_1 \ldots a_k$ from $s$ that avoids the threads of $\mathit{done}(s)$, with $a_k$ dependent with the next step $n$ of $p$; take $k$ least. Let $q$ be the thread of $a_k$; then $a_1, \ldots, a_{k-1}$ are independent with $n$.
3. By the choice of $s$, the subtree below $s \cdot n$ was explored with persistent sets, so by Theorem 3 it contains an execution in which, after $n$, the steps that $a_k$ depends on are run and then the next step of $q$ is $a_k$ (or a step that conflicts with $n$ in the same way).
4. When the search reaches the end of the prefix just before that step, line L2 for thread $q$ looks back along the current execution. The step $n$ at the position of $s$ is dependent with $a_k$, it is not a step of $q$, and nothing in between makes $n$ happen before $q$, because the steps in between come from the independent part $a_1 \ldots a_{k-1}$ and its dependencies. So either line L2 finds this position, or it finds a later race on the same path whose reversal is again handled below $s$, by the induction of step 1.
5. If line L2 finds the position of $s$, then line L4 adds $q$, or line L5 adds every thread enabled in $s$, to $\mathit{backtrack}(s)$. In both cases a thread that runs before $n$ the steps leading to $a_k$ is added, and the loop of line L7 does not end before it is in $\mathit{done}(s)$. A careful choice of the counterexample shows that this thread is $q$ or a thread of the prefix $a_1 \ldots a_{k-1}$, which contradicts the assumption that the execution avoids $\mathit{done}(s)$.

The details, in particular step 4, where the happens-before relation is used to show that the race is detected at the right place, and step 5, where "enabled in $\mathit{pre}(E, i)$" is needed, are in the paper of Flanagan and Godefroid (POPL 2005), in the section on the correctness of the algorithm. The paper of Abdulla, Aronis, Jonsson and Sagonas (POPL 2014) gives another proof of the same fact through source sets. $\blacksquare$
