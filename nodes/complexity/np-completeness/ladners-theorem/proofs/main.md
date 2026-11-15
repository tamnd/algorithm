---
title: Proof of Ladner's theorem (general form)
proves: [statement]
status: full
---

We prove the density theorem for Karp reductions and then derive the corollary for NP. Throughout, $\le$ means $\le_m^p$, the polynomial-time many-one (Karp) reduction, computed by a deterministic multitape Turing machine; $A < B$ means $A \le B$ and $B \not\le A$. A language is nontrivial when it is neither $\emptyset$ nor $\{0,1\}^*$.

**Theorem.** Let $A$ and $B$ be computable nontrivial languages with $A < B$. Then there is a computable language $C$ with $A < C < B$.

## Two facts about finite changes and joins

Fact 1. If $D$ and $D'$ differ on finitely many strings and $E$ is nontrivial, then $D \le E$ implies $D' \le E$. Proof: fix $e_1 \in E$ and $e_0 \notin E$; the new reduction sends each of the finitely many exceptions to $e_1$ or $e_0$ by a table, and every other string as before.

Fact 2. For $D \oplus E = \{0y : y \in D\} \cup \{1y : y \in E\}$: $D \le D \oplus E$ and $E \le D \oplus E$ (add the prefix bit), and if $D \le F$ and $E \le F$ with $F$ nontrivial, then $D \oplus E \le F$ (strip the bit and apply the right reduction; send the empty string to a fixed non-element of $F$).

## The construction

Fix an enumeration $M_1, M_2, \ldots$ of clocked transducers: $M_j$ runs the $j$-th Turing machine for $n^j + j$ steps on inputs of length $n$ and outputs what it has written. Every polynomial-time computable function is computed by some $M_j$, and every $M_j$ computes a polynomial-time function. Fix deciders for $A$ and $B$, and fix $a_0 \notin A$ and $b_0 \notin B$.

We will define a function $g : \mathbb{N} \to \mathbb{N}$ and set

$$C = \{0y : y \in A\} \cup \{1y : y \in B \text{ and } g(|y|) \text{ is even}\}.$$

The requirements are, for $j \ge 1$:

- $R_{2j}$: $M_j$ is not a reduction of $C$ to $A$, that is, some $z$ has $z \in C \iff M_j(z) \notin A$;
- $R_{2j+1}$: $M_j$ is not a reduction of $B$ to $C$, that is, some $z$ has $z \in B \iff M_j(z) \notin C$.

Requirement number $s$ is written $R_s$ for $s \ge 2$; we start $g$ at $2$.

**The definition of $g$.** Let $g(0) = 2$. For $n \ge 1$, let $s = g(n-1)$ and run the following search on a fixed universal machine for at most $n$ steps:

> For $z = $ the strings in length-lexicographic order: if $s = 2j$, test whether $z \in C \iff M_j(z) \notin A$; if $s = 2j + 1$, test whether $z \in B \iff M_j(z) \notin C$. To test whether a string $1y$ is in $C$, the search needs $g(|y|)$; it computes it by this same definition, but only if $|y| < n$, and otherwise it moves on to the next $z$.

If the search finds such a $z$ within $n$ steps, let $g(n) = s + 1$; otherwise let $g(n) = s$.

The definition is well founded, because the search at $n$ uses $g$ only at arguments less than $n$. So $g$ is a total computable function, it never decreases, and it grows by at most 1 at each step.

## The cost of g

To compute $g(n)$, compute $g(0), g(1), \ldots, g(n)$ in order. Each search at $m \le n$ takes at most $m$ steps of the universal machine, and a multitape machine simulates them with polynomial overhead. So $g(n)$ is computable in time polynomial in $n$, and the set $G = \{y : g(|y|) \text{ even}\}$ is in P.

## C lies between A and B

$A \le C$ by $y \mapsto 0y$.

$C \le B$: send $0y$ to $f(y)$, where $f$ reduces $A$ to $B$; send $1y$ to $y$ if $g(|y|)$ is even and to $b_0$ otherwise; send the empty string to $b_0$. This is computable in polynomial time because $G \in \mathsf{P}$. In particular $C$ is computable, and $C$ is nontrivial because $A$ is.

## Every requirement is met

**Claim.** $g$ is unbounded.

Assume not. Then $g$ is eventually constant: there are $s$ and $n_0$ with $g(n) = s$ for all $n \ge n_0$. So the search fails at every $n \ge n_0$.

Every fixed string $z$ is tested at all large $n$: the test of the first $N$ strings in the order takes a fixed finite number of steps, and once $n$ exceeds that number and the lengths of all strings whose membership in $C$ the tests need, the search reaches $z$ within $n$ steps. Since the search fails for all $n \ge n_0$, no string $z$ passes the test.

Case $s = 2j$. No $z$ has $z \in C \iff M_j(z) \notin A$. So $z \in C \iff M_j(z) \in A$ for all $z$, and $M_j$ reduces $C$ to $A$. But $g(m) = 2j$ is even for all $m \ge n_0$, so $C$ differs from $A \oplus B$ only on strings $1y$ with $|y| < n_0$. By Fact 1, $A \oplus B \le A$, and by Fact 2, $B \le A \oplus B$. So $B \le A$, which contradicts $A < B$.

Case $s = 2j + 1$. No $z$ has $z \in B \iff M_j(z) \notin C$. So $M_j$ reduces $B$ to $C$. But $g(m)$ is odd for all $m \ge n_0$, so $C$ differs from $A \oplus \emptyset$ only on finitely many strings, and $A \oplus \emptyset \le A$ by Fact 2 ($\emptyset \le A$ by the constant map to $a_0$). By Fact 1, $C \le A$. So $B \le C \le A$, which contradicts $A < B$.

Both cases are impossible, so $g$ is unbounded. Since $g$ grows by steps of 1 from $2$, it takes every value $s \ge 2$, and for each $s$ there is an $n$ with $g(n - 1) = s$ and $g(n) = s + 1$. At that $n$ the search found a $z$ that passes the test for $R_s$. The test used only true values of $g$ (the definition is the same one), so $z$ is a true disagreement, and $R_s$ holds.

All $R_{2j}$ hold, so no polynomial-time function reduces $C$ to $A$: $C \not\le A$. All $R_{2j+1}$ hold, so $B \not\le C$. With the previous section, $A < C < B$. $\blacksquare$

## The corollary for NP

Assume P is not equal to NP. Let $A$ be any nontrivial language in P, for example the strings that start with 1, and let $B = \mathrm{SAT}$. Then $A \le B$, since a polynomial-time machine decides $A$ and maps members to a fixed satisfiable formula and non-members to a fixed unsatisfiable one. And $B \not\le A$, since otherwise SAT would be in P and P = NP. The theorem gives a computable $C$ with $A < C < \mathrm{SAT}$.

- $C \in \mathsf{NP}$, because $C \le \mathrm{SAT}$ and NP is closed under Karp reductions.
- $C \notin \mathsf{P}$: if $C$ were in P, then $C \le A$, by deciding $C$ and mapping to a fixed member or non-member of $A$; but $C \not\le A$.
- $C$ is not NP-complete, because $\mathrm{SAT} \not\le C$.

So $C$ is NP-intermediate.

Iterating the theorem gives an infinite chain $A < C_1 < C_2 < \cdots < \mathrm{SAT}$: apply it to $C_1$ and SAT, then to $C_2$ and SAT, and so on.
