---
title: Probabilistic serial returns an envy-free and ordinally efficient random assignment
proves: [correctness, termination]
status: full
---

Fix agents $1, \dots, n$, objects $O$ with $|O| = m$, and a strict list of acceptable objects for each agent. A random assignment is a matrix $Q \ge 0$ with row and column sums at most 1 and $Q_{io} = 0$ when $i$ does not accept $o$. For a set $A$ of objects write $Q_i(A) = \sum_{o \in A} Q_{io}$. A top set of agent $i$ is the set of its $k$ best objects for some $k$. Row $q$ dominates row $p$ for agent $i$ if $q(A) \ge p(A)$ for every top set $A$ of $i$.

Number the passes of the loop of line L4 as $1, 2, \dots$, let $t_s$ be the value of $t$ at the start of pass $s$ and $\delta_s$ the step of line L8, so that pass $s$ covers the interval $[t_s, t_s + \delta_s]$. Read the algorithm as a process in continuous time: during this interval agent $i$ eats top[i] at speed 1.

**Claim 1 (tops only move down).** If agent $i$ eats object $x$ in pass $s$ and object $y$ in a later pass, then $x \succ_i y$, and $x$ was used up at the end of some pass between them. Once top[i] is NIL it stays NIL. *Proof.* left[o] never increases, so an object with left $= 0$ stays used up. In line L5, top[i] is the best object of $i$ with left $> 0$; the set of such objects only shrinks, so the best of them can only get worse, and it changes only when the old one is used up. $\square$

**Claim 2 (each pass but the last uses up an object).** If $\delta_s < 1 - t_s$, then some object $o$ with eaters[o] $> 0$ has $\delta_s = \text{left}[o] / \text{eaters}[o]$, and after line L9 left[o] $= 0$. Also left[o] $\ge 0$ always. *Proof.* Line L9 lowers left[o] by eaters[o] $\cdot \delta_s \le$ left[o]. If $\delta_s < 1 - t_s$, the minimum in line L8 is reached at some $o$, where the decrease equals left[o]. $\square$

**Termination.** By Claim 2, every pass with $\delta_s < 1 - t_s$ uses up an object that was not used up before, so there are at most $m$ such passes. A pass with $\delta_s = 1 - t_s$ sets $t = 1$ and ends the loop. Line L6 also ends the loop. So there are at most $m + 1$ passes.

**The output is a random assignment.** Line L9 adds to $P_{io}$ only when $o$ = top[i], an acceptable object. Column $o$ sums to $1 - \text{left}[o] \le 1$ by Claim 2. Row $i$ sums to the total time that $i$ eats, at most $t \le 1$.

**Envy-freeness.** Fix agents $i, j$ and a top set $A$ of $i$. Let $\tau$ be the end of the last pass in which some object of $A$ has left $> 0$ at its start (or $0$ if there is none). Before $\tau$, some object of $A$ is not used up, so top[i] is in $A$ (by Claim 1 and the definition of top), and $i$ eats from $A$ at speed 1. Agent $j$ eats at speed at most 1. After $\tau$, every object of $A$ is used up and nobody eats from $A$. So $P_i(A) = \tau \ge P_j(A)$. As $A$ was any top set, the row of $i$ dominates the row of $j$ for agent $i$. In particular, two agents with the same list get the same row.

**Ordinal efficiency.** Let $Q$ be a random assignment such that for every agent $i$, $Q_i$ dominates $P_i$ for $i$. We prove $Q = P$.

Let $T_1 < T_2 < \dots < T_K$ be the distinct times at which some object is used up, let $V_k$ be the set of objects used up at time $T_k$, and $U_k = V_1 \cup \dots \cup V_k$, with $U_0 = \emptyset$ and $T_0 = 0$. Between $T_{k-1}$ and $T_k$ no object is used up, so by Claim 1 every agent eats one fixed object $x_i^k$ during this interval, or nothing.

*Induction claim:* $Q_{io} = P_{io}$ for every agent $i$ and every $o \in U_k$. It holds for $k = 0$. Assume it for $k - 1$ and take $o \in V_k$.

- Let $E$ be the set of agents with $x_i^k = o$. If $P_{jo} > 0$ for some agent $j$, then $j$ ate $o$ at some time, and by Claim 1 it moves away from $o$ only when $o$ is used up, at $T_k$. So $j \in E$. Hence $\sum_{i \in E} P_{io} = 1$, because $o$ is used up.
- Take $i \in E$ and let $A_i$ be the top set of $i$ that ends with $o$. Every object that $i$ prefers to $o$ was used up before $i$ started on $o$, so it lies in $U_{k-1}$. Agent $i$ has eaten without a break from time 0 to $T_k$ (by Claim 1, a NIL top stays NIL), and only objects of $A_i$, and nobody eats from $A_i$ after $T_k$. So $P_i(A_i) = T_k$, and $Q_i(A_i) \ge P_i(A_i)$ by domination. Since $Q_i$ and $P_i$ agree on $A_i \setminus \{o\} \subseteq U_{k-1}$, we get $Q_{io} \ge P_{io}$.
- So $1 \ge \sum_{\text{all } i} Q_{io} \ge \sum_{i \in E} Q_{io} \ge \sum_{i \in E} P_{io} = 1$. All inequalities are equalities: $Q_{io} = P_{io}$ for $i \in E$, and $Q_{io} = 0 = P_{io}$ for $i \notin E$.

This proves the induction claim for $k$, so $Q$ and $P$ agree on $U_K$, the set of all used-up objects.

Now take an agent $i$. Both $Q_i$ and $P_i$ are zero outside the objects that $i$ accepts. If every object that $i$ accepts is in $U_K$, then $Q_i = P_i$ by the induction claim. Otherwise some acceptable object $y$ is never used up. Then top[i] is never NIL, so $i$ eats at every moment, the loop does not stop at line L6, and it stops with $t = 1$. Let $x$ be the object that $i$ eats in the last pass and $A$ the top set of $i$ that ends with $x$. Every object that $i$ prefers to $x$ was used up before $i$ started on $x$, so $A \setminus \{x\} \subseteq U_K$. Agent $i$ ate only objects of $A$, for a total time of 1, so $P_i(A) = 1$ and $P_i$ is zero outside $A$. Domination gives $Q_i(A) \ge 1$; as the row sum of $Q_i$ is at most 1, $Q_i(A) = 1$ and $Q_i$ is zero outside $A$. Since $Q_i = P_i$ on $A \setminus \{x\}$, also $Q_{ix} = 1 - P_i(A \setminus \{x\}) = P_{ix}$. So $Q_i = P_i$. This holds for every agent, so $Q = P$, and no other assignment dominates $P$: it is ordinally efficient. $\blacksquare$

**Weak strategyproofness** (that no false list gives a row that dominates the true row with a strict gain) is proved by Bogomolnaia and Moulin (2001); it is not reproved here, and the tests check it exhaustively for 3 agents and 3 objects.

**Cost.** By the termination argument there are at most $m + 1$ passes. Lines L7 to L10 cost $O(n + m)$ per pass. For line L5, each agent keeps a pointer into its list. By Claim 1 the pointer only moves forward, so all pointer moves together cost at most the total list length, $O(nm)$. The total is $O(m(n + m))$ arithmetic operations.
