---
title: SSS* returns the minimax value and never evaluates a leaf that alpha-beta skips
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, lines L1 to L12, in the MAX view: the root is a MAX node, the children of a MAX node are MIN nodes and the other way round, and $f$ is the value of a leaf for MAX. A node at the depth limit counts as a leaf. Let $N(n)$ be the [minimax](/minimax/) value of node $n$, and $V = N(\text{root})$. A state $(n, s, h)$ has a node, a status LIVE or SOLVED, and a merit $h$. A node is solved when its SOLVED state is inserted.

For a node $n$, let $\beta(n)$ be the smallest $N(x)$ over all nodes $x$ that are left siblings of a node on the path from the root to $n$ (with $n$ itself) and whose parent is a MIN node, and $+\infty$ if there is none. Let $\alpha(n)$ be the largest such $N(x)$ with a MAX parent, and $-\infty$ if there is none.

## Correctness and termination

**Lemma 1 (the merit of a LIVE state).** When a LIVE state $(n, \text{LIVE}, h)$ is inserted, $h = \beta(n)$.

**Lemma 2 (the value of a SOLVED state).** When a SOLVED state $(n, \text{SOLVED}, h')$ is inserted, $h' = \min(\beta(n), N(n))$.

**Lemma 3 (a witness).** Let $n$ have a LIVE state inserted, and let $n$ not be solved yet, and not removed by line L10. Then OPEN holds a state $(w, s, h)$ with $w$ equal to $n$ or below it and $h \ge \min(\beta(n), N(n))$.

*Proof of the three lemmas.* By induction on the steps of the loop. Each node gets at most one LIVE state, since line L8 expands a MAX node once, and lines L7 and L11 move along the children of a MIN node once, from left to right.

*Lemma 1.* Line L1 inserts the root with $+\infty = \beta(\text{root})$. Lines L7 and L8 copy the merit of the parent $n$ to a child $c$ that has no left sibling with a MIN parent of its own: at line L7 the child is the first one, and at line L8 the parent is a MAX node. So $\beta(c) = \beta(n)$. Line L11 inserts the next sibling $m$ of a MAX node $n$ with the merit of the SOLVED state of $n$, which is $\min(\beta(n), N(n))$ by Lemma 2. The parent of $n$ and $m$ is a MIN node, so $\beta(m) = \min(\beta(n), N(n))$.

*Lemma 2.* Line L6 inserts $\min(h, f(n))$ for a leaf, which is $\min(\beta(n), N(n))$ by Lemma 1. Line L12 solves a MIN node $u$ when its last child $c_k$ is solved. Its children were solved from left to right, and by Lemma 2 for each and by Lemma 1 the last merit is $\min(\beta(u), N(c_1), \dots, N(c_k)) = \min(\beta(u), N(u))$. Line L10 solves a MAX node $u$ when the state of its MIN child $c$ is SOLVED and has the largest merit in OPEN. By Lemma 2, that merit is $\min(\beta(u), N(c))$, since $\beta(c) = \beta(u)$. No other child of $u$ has had its SOLVED state taken, since the first one solves $u$. So every other child $c'$ has its SOLVED state in OPEN, with merit $\min(\beta(u), N(c'))$ by Lemma 2, or it is not solved, and by Lemma 3 OPEN holds a state at $c'$ or below it with merit at least $\min(\beta(u), N(c'))$. The popped merit is the largest in OPEN, so it is at least that. So it is $\max_{c'} \min(\beta(u), N(c')) = \min(\beta(u), N(u))$.

*Lemma 3.* Follow a path down from $n$, and stop at the first node $w$ that has a state in OPEN. A node $v$ on the path with no state in OPEN had its LIVE state taken, and it is not solved: for $v = n$ by the hypothesis, and below $n$ because the SOLVED state of $v$ is not in OPEN, and taking it would have moved the parent of $v$ on, which the choice of $v$ rules out. So $v$ is not a leaf, since line L6 would have solved it. If $v$ is a MAX node, line L8 inserted all its children, and the path goes to a child $c$ with $N(c) = N(v)$. If $v$ is a MIN node, its children that are solved and taken from OPEN form a prefix, and the path goes to the next child, which lines L7 or L11 inserted; its value is at least $N(v)$. Along this path the value never goes below $N(n)$, and each solved left sibling at a MIN node on it has a value at least that of the MIN node, so at least $N(n)$. The tree is finite, so the path reaches such a $w$. By Lemmas 1 and 2, the merit of the state of $w$ is $\beta(w)$ or $\min(\beta(w), N(w))$. Both are at least $\min(\beta(n), N(n))$: the set for $\beta(w)$ adds only values at least $N(n)$ to the set for $\beta(n)$, and $N(w) \ge N(n)$. $\square$

**Theorem 1.** SSS* stops and returns $V$. It evaluates each leaf at most once.

*Proof.* Each node gets at most one LIVE state and at most one SOLVED state, so the loop makes at most twice the number of nodes steps. By Lemma 3 for the root, OPEN is not empty until the root is solved, so line L3 always finds a state. Line L4 returns the merit of the SOLVED root, which is $\min(+\infty, V) = V$ by Lemma 2. A leaf is evaluated only at line L6, for its one LIVE state. $\blacksquare$

The tie rule plays no part here: any state with the largest merit can be taken at line L3.

## Stockman's theorem

**Theorem 2.** Let alpha-beta search the same tree with the window $(-\infty, +\infty)$, from left to right, with a cutoff when the score reaches the bound. With ties in OPEN taken from the left, every leaf that SSS* evaluates is evaluated by alpha-beta too.

*Proof.* Two steps: SSS* evaluates a leaf $\ell$ only if $\alpha(\ell) < \beta(\ell)$, and alpha-beta evaluates every leaf with $\alpha(\ell) < \beta(\ell)$.

*SSS*.* Let SSS* evaluate $\ell$. Line L3 popped its LIVE state, with merit $\beta(\ell)$ by Lemma 1. Let $x$ be a left sibling of a node $y$ on the path to $\ell$, with a MAX parent $u$. The node $u$ was expanded at line L8, so $x$ has a LIVE state. The SOLVED state of $x$ has not been taken from OPEN, since that would solve $u$ at line L10 and remove $\ell$. So either that SOLVED state is in OPEN, with merit $\min(\beta(x), N(x))$ by Lemma 2, or $x$ is not solved, and by Lemma 3 OPEN holds a state at $x$ or below it with merit at least $\min(\beta(x), N(x))$. In both cases, OPEN holds a state at $x$ or below it, to the left of $\ell$, with merit $h \ge \min(\beta(x), N(x))$, and $\beta(x) = \beta(u)$. Line L3 took $\ell$ first, so $\beta(\ell) > h$ by the tie rule. If $\beta(u) \le N(x)$, this gives $\beta(\ell) > \beta(u)$, which is false, since the set for $\beta(\ell)$ contains the set for $\beta(u)$. So $\beta(\ell) > N(x)$. This holds for every such $x$, so $\alpha(\ell) < \beta(\ell)$.

*Alpha-beta.* We use the fail-soft bounds of the [alpha-beta](/alpha-beta-pruning/) page: for the window $(a, b)$, a result $r \le a$ gives $N \le r$, a result $r \ge b$ gives $N \ge r$, and a result strictly inside is exact. In the MAX view, a MAX node raises $a$ only with a result above $a$, and a MIN node lowers $b$ only with a result below $b$. Such a result is exact, or it gives a cutoff at once. So, at each node $u$ on the path to $\ell$ that alpha-beta reaches, the window $(a_u, b_u)$ satisfies $a_u \le \alpha(u)$ and $b_u \ge \beta(u)$: each bound is $\mp\infty$ or the exact value of a left sibling of a node on the path, with a MAX or a MIN parent.

Let $\alpha(\ell) < \beta(\ell)$, and suppose that alpha-beta does not evaluate $\ell$. Then a cutoff happens at a node $u$ on the path, after a left sibling $x$ of the path. If $u$ is a MAX node, the result $r$ of $x$ is at least $b_u$, so $N(x) \ge r \ge b_u \ge \beta(u) \ge \beta(\ell)$, against $N(x) \le \alpha(\ell) < \beta(\ell)$. If $u$ is a MIN node, $r \le a_u$, so $N(x) \le r \le a_u \le \alpha(u) \le \alpha(\ell)$, against $N(x) \ge \beta(\ell) > \alpha(\ell)$. So alpha-beta evaluates $\ell$. $\blacksquare$

## The size of OPEN

**Theorem 3.** On a uniform tree of branching factor $b$ and depth $d$, OPEN never holds more than $b^{\lceil d/2 \rceil}$ states.

*Proof.* When a node is solved, OPEN holds no state below it: line L6 solves a leaf, line L10 removes all states below the MAX node it solves, and line L12 solves a MIN node when its last child is solved, after its other children. A LIVE node has nothing below it in OPEN either. So no state in OPEN is below another one. Below a MIN node, only the child in progress can have states, since the children before it are solved and the children after it are not inserted yet. So the nodes with states are leaves of a subtree that takes all children at MAX nodes and one child at MIN nodes. The root is a MAX node, so $\lceil d/2 \rceil$ of the $d$ levels branch, and this subtree has at most $b^{\lceil d/2 \rceil}$ leaves. $\blacksquare$

The proof of Theorem 2 uses the tie rule in one place: it makes the inequality $\beta(\ell) > h$ strict. Alpha-beta cuts off on equality, so a leaf with $N(x) = \beta(\ell)$ for some $x$ is one that it skips.
