---
title: Dead-end elimination never removes a rotamer of a global minimum
proves: [correctness]
status: full
---

We use the model and the pseudocode of the page. There are $n$ residues. Residue $i$ has a finite set $R_i$ of live rotamers, and at the start $R_i$ holds all its rotamers. The energy of an assignment $x = (x_1, \ldots, x_n)$ with $x_i \in R_i$ is

$$E(x) = \sum_i E_i(x_i) + \sum_{i < j} E_{ij}(x_i, x_j),$$

where we write $E_{ij}(r, s) = E_{ji}(s, r)$ and $E_{ij} = 0$ for a pair with no interaction. A *global minimum* is an assignment over the initial sets with the least energy. For live sets $R = (R_1, \ldots, R_n)$, two rotamers $r \ne t$ of residue $i$, define

$$D_R(i; r, t) = \Big[E_i(r) + \sum_{j \ne i} \min_{s \in R_j} E_{ij}(r, s)\Big] - \Big[E_i(t) + \sum_{j \ne i} \max_{s \in R_j} E_{ij}(t, s)\Big],$$

$$G_R(i; r, t) = E_i(r) - E_i(t) + \sum_{j \ne i} \min_{s \in R_j} \big[E_{ij}(r, s) - E_{ij}(t, s)\big].$$

The Desmet test removes $r$ when $D_R(i; r, t) > 0$ for a live $t \ne r$. The Goldstein test removes $r$ when $G_R(i; r, t) > 0$ for a live $t \ne r$.

**Lemma 1 (the Desmet test implies the Goldstein test).** For the same sets $R$, $G_R(i; r, t) \ge D_R(i; r, t)$.

*Proof.* For each $j \ne i$ and each $s \in R_j$, $E_{ij}(r, s) - E_{ij}(t, s) \ge \min_{s' \in R_j} E_{ij}(r, s') - \max_{s' \in R_j} E_{ij}(t, s')$. Take the minimum over $s$ on the left, and add the terms over $j$ and the self energies. $\square$

**Lemma 2 (the swap bound).** Let $x$ be an assignment with $x_j \in R_j$ for each $j \ne i$ and $x_i = r$. Let $x'$ equal $x$ except that $x'_i = t$. Then $E(x) - E(x') \ge G_R(i; r, t)$.

*Proof.* The terms that do not contain residue $i$ are the same in $E(x)$ and $E(x')$. So

$$E(x) - E(x') = E_i(r) - E_i(t) + \sum_{j \ne i} \big[E_{ij}(r, x_j) - E_{ij}(t, x_j)\big].$$

Each bracket is at least the minimum of the same bracket over $s \in R_j$, because $x_j \in R_j$. $\square$

**Theorem 1 (soundness).** At each point of the run, with either test, each global minimum $x^*$ has $x^*_i \in R_i$ for each $i$.

*Proof.* By induction on the number of removals. At the start each $R_i$ holds all rotamers. Assume that the claim holds before a removal, and that the removal takes $r$ from $R_i$ because a test succeeds with a live $t \ne r$. Assume, for a contradiction, that a global minimum $x^*$ has $x^*_i = r$. By the hypothesis, $x^*_j \in R_j$ for each $j$. Let $x'$ equal $x^*$ except that $x'_i = t$. For the Goldstein test, Lemma 2 gives $E(x^*) - E(x') \ge G_R(i; r, t) > 0$. For the Desmet test, Lemma 1 and Lemma 2 give $E(x^*) - E(x') \ge D_R(i; r, t) > 0$. So $E(x') < E(x^*)$, and $x'$ is an assignment over the initial sets. This contradicts the choice of $x^*$. So no global minimum uses $r$, and the claim holds after the removal. $\blacksquare$

**Corollary.** After the elimination, the least energy over the live sets equals the least energy over all assignments, and the assignments that reach it over the live sets are exactly the global minima. Each $R_i$ stays nonempty: a test removes $r$ only when a different rotamer $t$ is live, so the last live rotamer of a residue is never removed.

**Termination.** Each pass of the outer loop either removes at least one rotamer or is the last pass. The total number of rotamers $N = \sum_i |R_i|$ at the start is finite, and each removal lowers it by exactly 1. So there are at most $N - n + 1$ passes.

**Lemma 3 (monotone, transitive, antisymmetric).** (a) If $R'_j \subseteq R_j$ and $R'_j \ne \emptyset$ for each $j \ne i$, then $G_{R'}(i; r, t) \ge G_R(i; r, t)$. (b) For the same sets, $G_R(i; r, u) \ge G_R(i; r, t) + G_R(i; t, u)$ for three distinct rotamers $r, t, u$ of residue $i$. (c) For the same sets, $G_R(i; r, t) + G_R(i; t, r) \le 0$. So $G_R(i; r, t) > 0$ and $G_R(i; t, r) > 0$ cannot both hold.

*Proof.* (a) A minimum over a smaller nonempty set is at least the minimum over the larger set. (b) The self terms add up: $(E_i(r) - E_i(t)) + (E_i(t) - E_i(u)) = E_i(r) - E_i(u)$. For each $j$ and each $s$, $E_{ij}(r, s) - E_{ij}(u, s) = [E_{ij}(r, s) - E_{ij}(t, s)] + [E_{ij}(t, s) - E_{ij}(u, s)]$, and the minimum of a sum is at least the sum of the minima. (c) The self terms cancel. For each $j$ write $a_s = E_{ij}(r, s) - E_{ij}(t, s)$. Then $\min_s a_s + \min_s (-a_s) \le a_{s_0} - a_{s_0} = 0$ for any $s_0 \in R_j$. $\square$

**Theorem 2 (Goldstein removes at least what Desmet removes).** Run the loop to its end once with the Desmet test, with final sets $R^D$, and once with the Goldstein test, with final sets $R^G$, in any orders. Then $R^G_i \subseteq R^D_i$ for each $i$.

*Proof.* At the end of the Goldstein run, no test succeeds: $G_{R^G}(i; r, u) \le 0$ for each $i$ and each two distinct $r, u \in R^G_i$.

First, a fact about the Goldstein run. *If $t$ was removed from $R_i$ in that run, then there is a $u \in R^G_i$ with $u \ne t$ and $G_{R^G}(i; t, u) > 0$.* We show it by induction on the removals, from the last one back to the first. When $t$ was removed, a live $t_1 \ne t$ had $G_R(i; t, t_1) > 0$ for the sets $R$ of that moment. The final sets are nonempty subsets of $R$, so Lemma 3(a) gives $G_{R^G}(i; t, t_1) > 0$. If $t_1 \in R^G_i$, take $u = t_1$. This case covers the last removal, because then nothing is removed after $t$. Otherwise $t_1$ was removed later than $t$, because it was live when $t$ was removed. By the induction hypothesis there is a $u \in R^G_i$, $u \ne t_1$, with $G_{R^G}(i; t_1, u) > 0$. Here $u \ne t$, because $t \notin R^G_i$. So $t, t_1, u$ are distinct, and Lemma 3(b) gives $G_{R^G}(i; t, u) > 0$. This shows the fact.

Now assume, for a contradiction, that some rotamer is in $R^G$ but was removed in the Desmet run. Take the first such removal of the Desmet run: rotamer $r$ of residue $i$, removed with the live competitor $t$ and the sets $R$ of that moment. Each rotamer that the Desmet run removed before is not in $R^G$, by the choice of $r$. So $R^G_j \subseteq R_j$ for each $j$. By Lemma 1 and Lemma 3(a), $G_{R^G}(i; r, t) \ge G_R(i; r, t) \ge D_R(i; r, t) > 0$.

If $t \in R^G_i$, then the Goldstein test succeeds at the end of the Goldstein run with $r$ and $t$. This is a contradiction. If $t \notin R^G_i$, the fact gives a $u \in R^G_i$, $u \ne t$, with $G_{R^G}(i; t, u) > 0$. If $u = r$, then $G_{R^G}(i; r, t) > 0$ and $G_{R^G}(i; t, r) > 0$, which Lemma 3(c) forbids. So $r, t, u$ are distinct, and Lemma 3(b) gives $G_{R^G}(i; r, u) > 0$ with both $r$ and $u$ in $R^G_i$. This is again a contradiction. $\blacksquare$

Theorem 2 compares the final sets. It does not say that the Goldstein run removes each rotamer earlier, or with the same competitor.

**Corollary (order independence).** Two runs with the Goldstein test, in any two orders, end with the same sets. Two runs with the Desmet test, in any two orders, also end with the same sets.

*Proof.* In the proof of Theorem 2, the Desmet run is used only through one property of each of its removals: $G_R(i; r, t) > 0$ for the sets $R$ of that moment. A removal of a second Goldstein run has this property by definition. So the proof shows that the final sets of one Goldstein run are subsets of those of the other, and by symmetry they are equal. For the Desmet test, write $a_R(r) = E_i(r) + \sum_{j \ne i} \min_{s \in R_j} E_{ij}(r, s)$ and $b_R(t) = E_i(t) + \sum_{j \ne i} \max_{s \in R_j} E_{ij}(t, s)$, so that $D_R(i; r, t) = a_R(r) - b_R(t)$ and $a_R \le b_R$. Then $D$ has the three properties of Lemma 3: it grows when the sets shrink; $D(r, u) = a(r) - b(u) \ge [a(r) - b(t)] + [a(t) - b(u)] = D(r, t) + D(t, u)$; and $D(r, t) + D(t, r) = [a(r) - b(r)] + [a(t) - b(t)] \le 0$. The proof of Theorem 2, with $D$ in place of $G$ throughout, shows that two Desmet runs end with the same sets. $\blacksquare$
