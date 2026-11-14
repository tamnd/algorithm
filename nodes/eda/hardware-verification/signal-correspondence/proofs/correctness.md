---
title: Signal correspondence returns the coarsest inductive refinement of the simulation classes, which is sound and not complete
proves: [correctness]
status: full
---

**Setting.** The product machine has latches $s \in \{0, 1\}^L$, primary inputs $x \in \{0, 1\}^I$, initial state $s_0$ and next-state function $\delta(s, x)$. Each node $u$ (a latch, a gate, or one of the constants 0 and 1) has a value $u(s, x)$ in state $s$ under input $x$; for a latch, $u(s, x)$ is its bit of $s$. A state is *reachable* if it is $s_0$ or $\delta(t, x)$ for a reachable $t$ and some $x$.

A partition $\Pi$ of the nodes into classes, each with a first member $\mathrm{rep}(K)$, defines

$$E_\Pi(s, x) = \bigwedge_{K \in \Pi} \bigwedge_{u \in K} \big[u(s, x) = \mathrm{rep}(K)(s, x)\big].$$

$E_\Pi(s, x)$ holds exactly when all members of each class have equal values at $(s, x)$, so it does not depend on the choice of representatives. The partition $\Pi$ is *inductive* when

- (B) $E_\Pi(s_0, x)$ for every $x$, and
- (S) $E_\Pi(s, x_0) \Rightarrow E_\Pi(\delta(s, x_0), x_1)$ for all $s, x_0, x_1$.

$\Pi$ *refines* $\Pi'$, written $\Pi \le \Pi'$, when every class of $\Pi$ lies inside a class of $\Pi'$. If $\Pi \le \Pi'$, then $E_{\Pi'}(s, x) \Rightarrow E_\Pi(s, x)$, since $E_\Pi$ asks for a subset of the equalities, and (B) for $\Pi'$ gives (B) for $\Pi$.

**Theorem 1 (soundness).** If $\Pi$ is inductive, then $E_\Pi(s, x)$ holds for every reachable $s$ and every $x$. So if each output pair $(o, o')$ lies in one class of $\Pi$, the two circuits give the same output sequence for every input sequence from the initial state.

*Proof.* Induction on the reachability of $s$. For $s = s_0$, (B) gives the claim. If $s = \delta(t, x_0)$ with $t$ reachable, the hypothesis gives $E_\Pi(t, x_0)$, and (S) gives $E_\Pi(s, x_1)$ for every $x_1$. For an input sequence $x^0, x^1, \ldots$, the states $s^0 = s_0$, $s^{t+1} = \delta(s^t, x^t)$ are reachable, so $o(s^t, x^t) = o'(s^t, x^t)$ at every step $t$. $\square$

**Lemma 2 (each split is forced).** Let $\Pi$ be the current partition and $\Pi^\circ$ any inductive partition with $\Pi^\circ \le \Pi$. Let $\Pi'$ be the result of a split at line L3 or L7. Then $\Pi^\circ \le \Pi'$.

*Proof.* A split at line L3 uses a point $(s_0, x)$ and puts two nodes of a class of $\Pi$ in the same class of $\Pi'$ exactly when their values at the point are equal. Take a class $K^\circ$ of $\Pi^\circ$. It lies in one class $K$ of $\Pi$, and by (B) for $\Pi^\circ$ all its members have equal values at $(s_0, x)$. So $K^\circ$ lies in one class of $\Pi'$.

A split at line L7 uses a point $(s, x_0, x_1)$ with $C(s, x_0) = E_\Pi(s, x_0) = 1$, and splits by the values at $(\delta(s, x_0), x_1)$. Since $\Pi^\circ \le \Pi$, $E_\Pi(s, x_0)$ gives $E_{\Pi^\circ}(s, x_0)$, and (S) for $\Pi^\circ$ gives $E_{\Pi^\circ}(\delta(s, x_0), x_1)$. So again all members of a class of $\Pi^\circ$ have equal values at the point, and the class lies in one class of $\Pi'$. $\square$

**Lemma 3 (termination).** Lines L2 to L3 and L4 to L8 run at most $V - |\Pi_0|$ splits in total, for $V$ nodes and the partition $\Pi_0$ of line L1.

*Proof.* A split happens only at a point where some node $u$ and the representative of its class differ. They go to different classes, so the number of classes grows by at least 1. It never exceeds $V$. Each pass of lines L5 and L6 does a finite number of BDD checks. $\square$

**Theorem 4 (greatest fixed point).** The partition $\Pi$ at line L9 is inductive, refines $\Pi_0$, and is refined by every inductive partition that refines $\Pi_0$. So it is the unique coarsest inductive partition below $\Pi_0$.

*Proof.* Splits only refine, so $\Pi \le \Pi_0$. The loop of lines L2 and L3 stops when no class has a member that differs from its representative at $(s_0, x)$ for any $x$, which is (B). Later splits keep (B), because (B) passes to finer partitions. The loop of lines L4 to L8 stops when no $(s, x_0, x_1)$ has $E_\Pi(s, x_0)$ and a member that differs from its representative at $(\delta(s, x_0), x_1)$, which is (S). So $\Pi$ is inductive. Every inductive $\Pi^\circ \le \Pi_0$ satisfies $\Pi^\circ \le \Pi$: it holds for $\Pi_0$, and Lemma 2 keeps it through every split. Two partitions that each refine the other are equal, so the coarsest one is unique. $\blacksquare$

In terms of fixed points: let $\Phi(\Pi)$ be $\Pi$ split by the values at every point $(s_0, x)$ and at every point $(\delta(s, x_0), x_1)$ with $E_\Pi(s, x_0)$. Then $\Phi$ is monotone in the refinement order, its fixed points below $\Pi_0$ are the inductive partitions below $\Pi_0$, and Theorem 4 says the algorithm returns the greatest of them. It reaches it one counterexample at a time, not by computing $\Phi$ at once.

**Theorem 5 (incompleteness).** There are sequentially equivalent circuits that the algorithm does not prove, for every choice of random simulation.

*Proof.* Let $A$ have three latches $h_0, h_1, h_2$ with initial state $(1, 0, 0)$ and next state $(h_2, h_0, h_1)$, and the output $o = h_0 \wedge h_1$. Let $B$ have no latches and the output constant 0. The reachable states of $A$ are $(1, 0, 0)$, $(0, 1, 0)$ and $(0, 0, 1)$, and $o = 0$ in each, so $A$ and $B$ are sequentially equivalent. The nodes of the product are the constants 0 and 1, $h_0, h_1, h_2$, $o$ and the output $z$ of $B$ (there are no inputs). We show that no inductive partition at all has $o$ and $z$ in one class. Since the algorithm returns an inductive partition (Theorem 4), it does not prove the pair, whatever $\Pi_0$ is.

Let $\Pi$ be inductive. By Theorem 1, the members of each class agree in the three reachable states. In $(1, 0, 0)$ the node $h_0$ is 1 and $h_1, h_2, o, z$ and the constant 0 are 0. In $(0, 1, 0)$ the node $h_0$ is 0 and the constant 1 is 1. So $h_0$ is alone in its class. In the same way $h_1$ and $h_2$ are alone, and the constant 1 is alone (it differs from $o$, $z$ and the constant 0 everywhere). Suppose $o$ and $z$ share a class. That class is $\{o, z\}$ or $\{o, z, 0\}$, and all other classes have one member. Take $s = (1, 0, 1)$, which is not reachable. There $o = 1 \wedge 0 = 0$, so $E_\Pi(s)$ holds. But $\delta(s) = (1, 1, 0)$, where $o = 1$ and $z = 0$, so $E_\Pi(\delta(s))$ fails, and (S) fails. This contradicts the choice of $\Pi$. $\square$

The induction fails only because of the unreachable state $(1, 0, 1)$. A stronger hypothesis removes it: with the extra gates $h_1 \wedge h_2$ and $h_0 \wedge h_2$ in $A$, the class $\{0, o, h_1 \wedge h_2, h_0 \wedge h_2, z\}$ says that at most one latch is 1, which is inductive.
