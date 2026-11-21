---
title: The graph search computes Kemmerer's closure of the shared resource matrix
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are $n$ attributes and $m$ primitives. For a primitive $q$, $R_0(q)$ is the set of attributes that $q$ references in the input matrix, and $M(q)$ is the set of attributes that $q$ modifies. The matrix has no other entries.

**Kemmerer's closure.** A family $R = (R(p))_p$ of attribute sets is *closed* if $R_0(p) \subseteq R(p)$ for each $p$, and

$$ a \in R(p) \text{ and } a \in M(q) \implies R(q) \subseteq R(p) \qquad \text{for all } p, q, a. \tag{K} $$

Kemmerer's procedure starts from $R_0$ and, while some entry breaks (K), adds the missing R entries. It only adds entries that (K) forces, and it stops when (K) holds. So it returns the least closed family $R^*$: by induction on the number of added entries, each added entry is in every closed family. The family $R^*$ exists, because the intersection of closed families is closed and the family "every primitive references every attribute" is closed.

**The flow graph.** Let $G$ be the directed graph on the attributes with an edge $a \to b$ when some primitive $q$ has $a \in M(q)$ and $b \in R_0(q)$. In words: $q$ may write into $a$ a value that depends on $b$, so a reader of $a$ may learn about $b$. Lines L1 to L4 build exactly the edge sets $E[a] = \{ b : a \to b \}$, because they visit each primitive $q$, each $a \in M(q)$ and add all of $R_0(q)$ to $E[a]$. For a set $S$ of attributes, let $\mathrm{Reach}(S)$ be the set of attributes $b$ with a directed path (of length 0 or more) from some $a \in S$ to $b$.

**Claim 1.** For each primitive $p$, $R^*(p) = \mathrm{Reach}(R_0(p))$.

*Proof.* Let $T(p) = \mathrm{Reach}(R_0(p))$.

First, $T$ is closed. It contains $R_0(p)$ (paths of length 0). For (K), take $a \in T(p)$ and $a \in M(q)$, and let $c \in T(q)$. Then there is a path from some $b \in R_0(q)$ to $c$. Since $a \in M(q)$ and $b \in R_0(q)$, $a \to b$ is an edge, so there is a path from a vertex of $R_0(p)$ to $a$, then to $b$, then to $c$. So $c \in T(p)$, and $T(q) \subseteq T(p)$. Since $R^*$ is the least closed family, $R^*(p) \subseteq T(p)$.

Second, every closed family $R$ has $T(p) \subseteq R(p)$. We show by induction on $k$ that if a path of length $k$ goes from some vertex of $R_0(p)$ to $c$, then $c \in R(p)$. For $k = 0$, $c \in R_0(p) \subseteq R(p)$. For $k \ge 1$, the path ends with an edge $a \to c$, and by induction $a \in R(p)$. The edge comes from a primitive $q$ with $a \in M(q)$ and $c \in R_0(q)$. By (K), $R(q) \subseteq R(p)$, and $c \in R_0(q) \subseteq R(q)$, so $c \in R(p)$. Taking $R = R^*$ gives $T(p) \subseteq R^*(p)$. $\square$

**Claim 2.** For each primitive $p$, the loop of lines L6 to L10 ends with $R[p] = \mathrm{Reach}(R_0(p))$.

*Proof.* This is a graph search with a stack. We use the invariant: (a) every element of $R[p]$ is in $\mathrm{Reach}(R_0(p))$; (b) every element of the stack is in $R[p]$; (c) for every $a \in R[p]$ that is not on the stack, $E[a] \subseteq R[p]$.

Line L6 sets $R[p] = R_0(p)$ and puts all of it on the stack, so (a), (b) and (c) hold. Line L8 pops $a$, which may break (c) for $a$ only. Lines L9 and L10 then add each $b \in E[a]$ that is missing, and push it. Each such $b$ is reachable, since $a$ is reachable and $a \to b$ is an edge, so (a) holds. The new elements are on the stack, so (b) and (c) hold for them, and now $E[a] \subseteq R[p]$, so (c) holds for $a$. Each attribute is pushed at most once, because it is pushed only when it enters $R[p]$, and nothing leaves $R[p]$. So the loop ends after at most $n$ pops.

At the end the stack is empty, so by (c) the set $R[p]$ is closed under the edges of $G$, and it contains $R_0(p)$. A set that contains $R_0(p)$ and is closed under the edges contains every vertex on a path from $R_0(p)$, so $\mathrm{Reach}(R_0(p)) \subseteq R[p]$. With (a), equality holds. $\square$

**Claim 3.** Lines L11 to L13 return exactly the attributes $a$ for which some primitive modifies $a$ and some primitive references $a$ in $R^*$, each with its list of modifiers and its list of sensors.

*Proof.* The M entries do not change in the closure, so the modifiers of $a$ are $\{p : a \in M(p)\}$. By Claims 1 and 2, the sensors of $a$ in the closed matrix are $\{p : a \in R[p]\}$. Line L13 computes both lists and keeps $a$ when both are non-empty. $\square$

**Theorem.** SHARED-RESOURCE-MATRIX returns Kemmerer's closed matrix $R^*$ and the list of rows of $R^*$ that have both an R entry and an M entry.

*Proof.* Claims 1 and 2 give $R[p] = R^*(p)$ for each primitive $p$. Claim 3 gives the candidate list. $\blacksquare$
