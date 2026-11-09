---
title: Saturation returns the reachable states
proves: [correctness]
status: full
---

We use the notation of the page. For a level $l$, write $S_{\le l} = S_l \times \cdots \times S_1$ for the set of $l$-tuples, with $S_{\le 0} = \{()\}$. For an event $e$ and a level $l$, let $\mathcal{N}_e^{\le l}$ be the relation on $S_{\le l}$ given by $\mathcal{N}_e^{\le l}(t_l, \ldots, t_1) = \mathcal{N}_{e,l}(t_l) \times \cdots \times \mathcal{N}_{e,1}(t_1)$. For $l \ge \mathrm{Top}(e)$, this is the action of $e$ on the lower part of a state; the levels above $l$ are not changed by $e$. Let $\mathcal{N}_{\le l} = \bigcup \{\mathcal{N}_e^{\le l} : \mathrm{Top}(e) \le l\}$. For a set $X$ and a relation $\rho$, $\rho^*(X)$ is the least set that holds $X$ and is closed under $\rho$; it is the set of states that $\rho$ reaches from $X$ in zero or more steps. A node is *saturated* when its set is closed under $\mathcal{N}_{\le l}$, where $l$ is its level. The terminals are saturated, as $\mathcal{N}_{\le 0}$ only relates $()$ to itself or to nothing.

**Lemma 1 (unions).** If $X$ and $Y$ are closed under a relation $\rho$, then so is $X \cup Y$. Hence the MDD union of two saturated nodes at level $l$ is saturated.

*Proof.* $\rho(X \cup Y) = \rho(X) \cup \rho(Y) \subseteq X \cup Y$. ∎

**Lemma 2 (lower events at the children).** Let $p$ be a node at level $k$ with saturated children. Then $\mathcal{B}(p)$ is closed under every $\mathcal{N}_e^{\le k}$ with $\mathrm{Top}(e) < k$.

*Proof.* Such an event does not touch level $k$. So for $(i, t) \in \mathcal{B}(p)$, the successors are $(i, t')$ with $t' \in \mathcal{N}_e^{\le k-1}(t)$. As $t \in \mathcal{B}(p[i])$, $\mathrm{Top}(e) \le k - 1$, and $p[i]$ is saturated, we get $t' \in \mathcal{B}(p[i])$, so $(i, t') \in \mathcal{B}(p)$. ∎

We prove three claims together, by induction on the level. Each claim speaks about one call; the calls made inside it are at the same level or one level lower, and a call at the same level is only FIX inside REC-FIRE or SATURATE, which we treat directly.

- **(F$_k$)** If each $ch[i]$ is a saturated node at level $k - 1$, then FIX$(k, ch)$ terminates and returns a node for $\mathcal{N}_{\le k}^*(X)$, where $X = \{(i, t) : t \in \mathcal{B}(ch[i])\}$ is the set of the input children.
- **(S$_k$)** For a node $p$ at level $k$, SATURATE$(p)$ terminates and returns a node for $\mathcal{N}_{\le k}^*(\mathcal{B}(p))$.
- **(R$_l$)** For an event $e$ with $l < \mathrm{Top}(e)$ and a saturated node $q$ at level $l$, REC-FIRE$(e, l, q)$ terminates and returns a node for $\mathcal{N}_{\le l}^*(\mathcal{N}_e^{\le l}(\mathcal{B}(q)))$.

*Proof of (R$_l$), assuming (F$_l$) and (R$_{l-1}$).* If $l < \mathrm{Bot}(e)$, then $\mathcal{N}_e^{\le l}$ is the identity on $S_{\le l}$, so the claimed set is $\mathcal{N}_{\le l}^*(\mathcal{B}(q)) = \mathcal{B}(q)$, as $q$ is saturated. Line L12 returns $q$. If $l = 0$, then $l < \mathrm{Bot}(e)$, as $\mathrm{Bot}(e) \ge 1$. Else lines L14 to L17 set
$$ch[j] = \bigcup \{\mathrm{REC\text{-}FIRE}(e, l - 1, q[i]) : j \in \mathcal{N}_{e,l}(i)\}.$$
By (R$_{l-1}$), each part is a saturated node for $\mathcal{N}_{\le l-1}^*(\mathcal{N}_e^{\le l-1}(\mathcal{B}(q[i])))$, and by Lemma 1 each $ch[j]$ is saturated. The set $Y$ of the children is
$$Y = \{(j, t) : j \in \mathcal{N}_{e,l}(i), \; t \in \mathcal{N}_{\le l-1}^*(\mathcal{N}_e^{\le l-1}(\mathcal{B}(q[i]))) \text{ for some } i\}.$$
It holds $\mathcal{N}_e^{\le l}(\mathcal{B}(q))$, by taking zero steps of $\mathcal{N}_{\le l-1}$. And it is a subset of $\mathcal{N}_{\le l}^*(\mathcal{N}_e^{\le l}(\mathcal{B}(q)))$, since each step of $\mathcal{N}_{\le l-1}$ on the lower part is a step of $\mathcal{N}_{\le l}$ that keeps level $l$. So $\mathcal{N}_{\le l}^*(Y) = \mathcal{N}_{\le l}^*(\mathcal{N}_e^{\le l}(\mathcal{B}(q)))$, and by (F$_l$) line L18 returns a node for this set. A result in the cache is the result of an earlier call with the same arguments, so line L13 returns the same set. ∎

*Proof of (F$_k$), assuming (R$_{k-1}$).* During the loop, each $ch[i]$ stays a saturated node at level $k - 1$: line L8 calls REC-FIRE$(e, k - 1, ch[i])$ with $\mathrm{Top}(e) = k > k - 1$ on a saturated node, which by (R$_{k-1}$) returns a saturated node, and line L9 takes unions, which are saturated by Lemma 1. Let $Z$ be the set of the current children.

*Soundness.* $Z \subseteq \mathcal{N}_{\le k}^*(X)$ at all times. At the start $Z = X$. Line L9 adds $(j, t)$ with $j \in \mathcal{N}_{e,k}(i)$ and $t \in \mathcal{N}_{\le k-1}^*(\mathcal{N}_e^{\le k-1}(\mathcal{B}(ch[i])))$. Then there is $(i, u) \in Z$ with $(j, t'') \in \mathcal{N}_e^{\le k}(i, u)$ and $t$ reached from $t''$ by steps of $\mathcal{N}_{\le k-1}$, which are steps of $\mathcal{N}_{\le k}$ that keep level $k$. So $(j, t) \in \mathcal{N}_{\le k}^*(Z) \subseteq \mathcal{N}_{\le k}^*(X)$.

*Termination.* Each change in line L9 strictly grows one $ch[j]$, and $S_{\le k}$ is finite, so there are finitely many changes. A round of lines L7 to L9 with no change ends the loop. Each REC-FIRE call terminates by (R$_{k-1}$).

*Closure.* At the end, the last round made no change. So for each event $e$ with $\mathrm{Top}(e) = k$, each $i$, and each $j \in \mathcal{N}_{e,k}(i)$, the node for $\mathcal{N}_{\le k-1}^*(\mathcal{N}_e^{\le k-1}(\mathcal{B}(ch[i])))$ is a subset of $ch[j]$. In particular $\mathcal{N}_e^{\le k}(Z) \subseteq Z$. By Lemma 2, $Z$ is also closed under the events with top below $k$. So $Z$ is closed under $\mathcal{N}_{\le k}$, and it holds $X$. Together with soundness, $Z = \mathcal{N}_{\le k}^*(X)$, the least such set. Line L11 returns the node of $Z$. ∎

*Proof of (S$_k$), assuming (S$_{k-1}$) and (F$_k$).* At level 0, line L1 returns the terminal, which is saturated. At level $k \ge 1$, line L3 makes saturated children for $\mathcal{N}_{\le k-1}^*(\mathcal{B}(p[i]))$, by (S$_{k-1}$). Their set $X'$ satisfies $\mathcal{B}(p) \subseteq X' \subseteq \mathcal{N}_{\le k}^*(\mathcal{B}(p))$, so $\mathcal{N}_{\le k}^*(X') = \mathcal{N}_{\le k}^*(\mathcal{B}(p))$. By (F$_k$), line L4 returns a node for this set. The cache maps $p$ to this result, and it maps a saturated node to itself, which is correct because $\mathcal{N}_{\le k}^*(\mathcal{B}(r)) = \mathcal{B}(r)$ for a saturated $r$. ∎

The induction goes up the levels: (R$_0$) holds, as shown at the start of its proof. For $k \ge 1$, (R$_{k-1}$) gives (F$_k$), then (F$_k$) and (S$_{k-1}$) give (S$_k$), and (F$_k$) and (R$_{k-1}$) give (R$_k$).

**Theorem.** SATURATE$(p_0)$, where $p_0$ is the MDD of the initial states at level $K$, returns the MDD of $\mathcal{N}^*(\mathcal{B}(p_0))$, the set of reachable states.

*Proof.* Every event has $\mathrm{Top}(e) \le K$, and $\mathcal{N}_e^{\le K} = \mathcal{N}_e$. So $\mathcal{N}_{\le K} = \mathcal{N}$, and (S$_K$) gives the claim. ∎
