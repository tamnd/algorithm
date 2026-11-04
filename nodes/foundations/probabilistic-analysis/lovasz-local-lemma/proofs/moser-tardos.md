---
title: The Moser-Tardos algorithm resamples each event A at most x(A)/(1 - x(A)) times in expectation
id: moser-tardos
proves: [moser-tardos]
method: probabilistic
form: full
uses: [linearity-of-expectation, independent-random-variables]
sources:
  - {paper: "doi:10.1145/1667053.1667060", locator: "Moser and Tardos 2010, Theorem 1.2, Lemma 2.1 (witness trees and the tau-check) and Lemma 3.1 (the Galton-Watson process)"}
  - {book: "isbn:9781119061953", locator: "Alon and Spencer, The Probabilistic Method, 4th ed., Chapter 5, Section 5.7"}
  - {book: "isbn:9781107154889", locator: "Mitzenmacher and Upfal, 2nd ed., Section 6.10"}
---

**Statement.** Let $\mathcal P$ be a finite set of mutually [independent random variables](/independent-random-variables/), each of which the algorithm can sample. Let $\mathcal A$ be a finite set of events, and let each $A \in \mathcal A$ be determined by the values of a set $\mathrm{vbl}(A) \subseteq \mathcal P$ of variables. For $A \in \mathcal A$ let $\Gamma(A)$ be the set of events $B \in \mathcal A$ with $B \ne A$ and $\mathrm{vbl}(A) \cap \mathrm{vbl}(B) \ne \emptyset$, and let $\Gamma^+(A) = \Gamma(A) \cup \{A\}$. Assume that there is a map $x : \mathcal A \to (0,1)$ with
$$ \Pr[A] \le x(A) \prod_{B \in \Gamma(A)} \bigl(1 - x(B)\bigr) \qquad \text{for each } A \in \mathcal A. \tag{LLL} $$
Run MOSER-TARDOS (lines L1 to L5 of the [main page](/lovasz-local-lemma/)) with a selection rule in line L3 that may use the run so far and extra independent randomness, but not samples that the run has not yet drawn. Let $N_A$ be the number of times line L4 resamples the event $A$. Then $\mathbb E[N_A] \le x(A)/(1 - x(A))$ for each $A$. So the expected number of resampling steps is at most $\sum_{A} x(A)/(1-x(A))$, the algorithm stops with probability 1, and its output makes no event of $\mathcal A$ hold.

**Setup.**

- *The resampling table.* For each variable $P \in \mathcal P$ fix an infinite sequence $P^{(0)}, P^{(1)}, P^{(2)}, \ldots$ of independent samples of $P$, all sequences independent of each other. The run takes the value of $P$ in line L1 from $P^{(0)}$, and each time line L4 needs a new sample of $P$ it takes the next unused entry. Each sample is fresh and independent of everything before it, so the run has the same distribution as the algorithm. With this table, the value of $P$ just before step $s$ is $P^{(j)}$, where $j$ is the number of steps $s' < s$ that resampled an event $C$ with $P \in \mathrm{vbl}(C)$.
- *The log.* Let $C(1), C(2), \ldots$ be the events resampled in steps $1, 2, \ldots$. The log is finite if the run stops.
- *Witness trees.* A witness tree is a finite rooted tree whose vertices carry labels in $\mathcal A$, such that each child of a vertex $u$ has a label in $\Gamma^+([u])$, where $[u]$ is the label of $u$. It is *proper* if the children of each vertex have distinct labels. Two witness trees are the same if a bijection maps one to the other, keeps the root, the edges and the labels. Let $\mathcal T_A$ be the set of proper witness trees whose root has label $A$; it is countable.
- *The tree of step $t$.* Start with one root vertex with label $C(t)$. Then for $s = t-1, t-2, \ldots, 1$: if the tree has a vertex $u$ with $C(s) \in \Gamma^+([u])$, take such a vertex $u$ of maximum depth (break ties in any fixed way) and attach to it a new child with label $C(s)$; if no such vertex exists, skip $s$. The result is $\tau(t)$. A witness tree $\tau$ *occurs in the log* if $\tau = \tau(t)$ for some $t$. For a vertex $v$ of $\tau(t)$, let $q(v)$ be the step that created it ($q(\text{root}) = t$) and $d(v)$ its depth. The map $q$ is one to one.

**The proof.**

*Step 1 (depth order).* Let $\tau = \tau(t)$ and let $u, v$ be vertices with $q(u) < q(v)$ and $\mathrm{vbl}([u]) \cap \mathrm{vbl}([v]) \ne \emptyset$. Then $d(u) > d(v)$. Indeed, the construction handles step $q(v)$ before step $q(u)$, so $v$ is in the tree when step $q(u)$ is handled. The labels share a variable, so $[v] \in \Gamma^+([u])$, which is the same as $[u] \in \Gamma^+([v])$. So $v$ is a candidate, and the new vertex $u$ goes below a candidate of depth at least $d(v)$. Hence $d(u) \ge d(v) + 1$.

*Step 2 (consequences of Step 1).* (a) Two distinct vertices of the same depth have labels with disjoint variable sets, because Step 1 gives different depths otherwise. (b) Each tree $\tau(t)$ is proper. Each label is an event that the run resampled, so it held at some moment. An event with no variables is constant, so it would hold always, and then $\Pr[A] = 1 > x(A)$ contradicts (LLL). So each label has at least one variable, and two equal labels share it. Two children of one vertex have the same depth, so by (a) their labels share no variable, and hence they differ.

*Step 3 (no step is lost).* Let $v$ be a vertex of $\tau(t)$ and $P \in \mathrm{vbl}([v])$. Each step $s < q(v)$ with $P \in \mathrm{vbl}(C(s))$ creates a vertex of $\tau(t)$. Indeed, when step $s$ is handled, $v$ is already in the tree, and $C(s)$ and $[v]$ share $P$, so $C(s) \in \Gamma^+([v])$ and the step is not skipped.

*Step 4 (the $\tau$-check).* Fix a witness tree $\tau$ and an order of its vertices by decreasing depth (ties in a fixed way). The $\tau$-check visits the vertices in this order. At vertex $v$ it gives each $P \in \mathrm{vbl}([v])$ the value $P^{(i_v(P))}$, where $i_v(P)$ is the number of vertices $w$ visited before $v$ with $P \in \mathrm{vbl}([w])$, and it tests whether $[v]$ holds under these values. The check *passes* if $[v]$ holds at each vertex. If $v$ is visited before $v'$ and both use $P$, then $i_{v'}(P) \ge i_v(P) + 1$. So distinct vertices read distinct entries of the table. The values read at $v$ are independent samples of the variables in $\mathrm{vbl}([v])$, which are mutually independent in the original space, so $[v]$ holds with probability exactly $\Pr[[v]]$. The tests read disjoint sets of independent entries, so they are independent events. Hence
$$ \Pr[\tau\text{-check passes}] = \prod_{v \in V(\tau)} \Pr[[v]]. $$

*Step 5 (coupling).* Assume $\tau = \tau(t)$ for some $t$. We show that the $\tau$-check passes on the same table. Let $v$ be a vertex and $P \in \mathrm{vbl}([v])$. By the setup, the value of $P$ just before step $q(v)$ is $P^{(j)}$, where $j$ is the number of steps $s < q(v)$ with $P \in \mathrm{vbl}(C(s))$. By Step 3, these steps are exactly the $q(w)$ of the vertices $w$ with $q(w) < q(v)$ and $P \in \mathrm{vbl}([w])$, and $q$ is one to one, so $j$ is the number of such vertices. By Step 1, a vertex $w \ne v$ with $P \in \mathrm{vbl}([w])$ has $d(w) > d(v)$ if $q(w) < q(v)$ and $d(w) < d(v)$ if $q(w) > q(v)$. So $j$ is the number of vertices $w$ with $P \in \mathrm{vbl}([w])$ and $d(w) > d(v)$. By Step 2(a) no vertex of depth $d(v)$ other than $v$ uses $P$, so the decreasing-depth order visits exactly these $w$ before $v$, and $j = i_v(P)$. The algorithm resampled $[v]$ at step $q(v)$, and line L3 picks only an event that holds, so $[v]$ holds under the values $P^{(i_v(P))}$. This is the test of the $\tau$-check at $v$. With Step 4,
$$ \Pr[\tau \text{ occurs in the log}] \le \prod_{v \in V(\tau)} \Pr[[v]]. $$

*Step 6 (counting resamplings by trees).* Let $C(t) = A$. Each step $s < t$ with $C(s) = A$ creates a vertex of $\tau(t)$, because the root has label $A \in \Gamma^+(A)$. Only such steps create vertices labelled $A$. So $\tau(t)$ has exactly $\#\{s \le t : C(s) = A\}$ vertices labelled $A$, and two steps $t < t'$ with $C(t) = C(t') = A$ give different trees. By Step 2(b) these trees are in $\mathcal T_A$. So $N_A \le \sum_{\tau \in \mathcal T_A} \mathbf 1[\tau \text{ occurs}]$. Taking expectations ([linearity of expectation](/linearity-of-expectation/), which holds for a countable sum of nonnegative terms) and using Step 5 and then (LLL):
$$ \mathbb E[N_A] \le \sum_{\tau \in \mathcal T_A} \prod_{v \in V(\tau)} \Pr[[v]] \le \sum_{\tau \in \mathcal T_A} \prod_{v \in V(\tau)} x'([v]), \qquad x'(B) = x(B) \prod_{C \in \Gamma(B)} \bigl(1 - x(C)\bigr). $$

*Step 7 (a branching process).* Consider this random process. Round 0 makes a root with label $A$. In each later round, each vertex $u$ made in the previous round gets, for each $C \in \Gamma^+([u])$ independently, a child with label $C$ with probability $x(C)$. The process makes a proper witness tree with root $A$, or it never stops. Fix $\tau \in \mathcal T_A$. For a vertex $v$ of $\tau$ let $W_v$ be the set of labels in $\Gamma^+([v])$ that no child of $v$ carries. The process yields exactly $\tau$ when each vertex $v$ of $\tau$ gets children with exactly the labels of its children in $\tau$. These choices use disjoint independent coins, so
$$ p_\tau = \prod_{v \in V(\tau)} \Bigl( \prod_{\substack{u \text{ child of } v}} x([u]) \prod_{C \in W_v} (1 - x(C)) \Bigr). $$
Each vertex other than the root is the child of exactly one vertex. So the product of the factors $x([u])$ is $\prod_{v \ne \text{root}} x([v]) = \frac{1}{x(A)} \prod_{v} x([v])$. Since $\tau$ is proper, $\prod_{C \in W_v}(1-x(C)) = \prod_{C \in \Gamma^+([v])} (1 - x(C)) \big/ \prod_{u \text{ child of } v} (1 - x([u]))$, and the denominators multiply to $\prod_{v \ne \text{root}} (1 - x([v])) = \frac{1}{1 - x(A)} \prod_v (1 - x([v]))$. So
$$ p_\tau = \frac{1 - x(A)}{x(A)} \prod_{v} \frac{x([v]) \prod_{C \in \Gamma^+([v])} (1 - x(C))}{1 - x([v])} = \frac{1 - x(A)}{x(A)} \prod_{v \in V(\tau)} x'([v]), $$
because $\Gamma^+([v])$ holds $[v]$ itself, whose factor cancels the denominator.

*Step 8 (the sum).* Distinct trees $\tau \in \mathcal T_A$ are disjoint outcomes of one run of the process, so $\sum_{\tau \in \mathcal T_A} p_\tau \le 1$. With Steps 6 and 7,
$$ \mathbb E[N_A] \le \frac{x(A)}{1 - x(A)} \sum_{\tau \in \mathcal T_A} p_\tau \le \frac{x(A)}{1 - x(A)}. $$

**End.** Summing over the finitely many events, the expected total number of resampling steps is at most $\sum_A x(A)/(1 - x(A)) < \infty$. A random variable with finite expectation is finite with probability 1, so the run stops with probability 1. It stops only when the loop test of line L2 fails, that is, when no event of $\mathcal A$ holds. In particular such an assignment exists. ∎
