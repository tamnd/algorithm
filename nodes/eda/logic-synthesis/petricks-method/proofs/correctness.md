---
title: Petrick's method lists the irredundant covers and returns a cheapest one
proves: [correctness]
status: full
---

Let the rows be $r_1, \ldots, r_m$, each a set of primes. A set $S$ of primes is a transversal of rows $r_1, \ldots, r_t$ when $S \cap r_i \ne \emptyset$ for every $i \le t$. It is a minimal transversal when no proper subset of $S$ is a transversal. Write $M_t$ for the set of minimal transversals of the first $t$ rows. The only transversal of no rows that is minimal is $\emptyset$, so $M_0 = \{\emptyset\}$.

**Lemma 1 (absorption).** Let $X$ be a finite family of sets. The sets that line L7 keeps are the inclusion-minimal sets of $X$, each one time.

*Proof.* Line L7 goes through the distinct sets of $X$ in order of size and keeps a set unless it contains a set already kept. If $t$ is minimal in $X$, no other set of $X$ is a subset of $t$, so no kept set is a subset of $t$, and $t$ is kept. If $t$ is not minimal, some set of $X$ is a proper subset of $t$, and among those there is a minimal one $s$ of $X$. It is smaller than $t$, so it comes first and is kept, and then $t$ is removed. Repeated sets are merged before the pass. $\square$

**Lemma 2 (invariant).** If no row among $r_1, \ldots, r_t$ is empty, then after the $t$-th pass of line L2 the list products is exactly $M_t$.

*Proof.* By induction on $t$. For $t = 0$, line L1 sets products to $\{\emptyset\} = M_0$. Assume products $= M_{t-1}$ before the pass for row $r = r_t$.

Every set in step is a transversal of the first $t$ rows. A set $T$ that line L5 adds meets the first $t - 1$ rows by the hypothesis and meets $r$ by the test. A set $T \cup \{j\}$ that line L6 adds contains $T$, which meets the first $t - 1$ rows, and contains $j \in r$.

Every set of $M_t$ is in step. Let $S \in M_t$. Then $S$ is a transversal of the first $t - 1$ rows, so it contains some $T \in M_{t-1}$. If $T$ meets $r$, then $T$ is a transversal of the first $t$ rows with $T \subseteq S$, so $T = S$ by the minimality of $S$, and line L5 adds it. If $T$ does not meet $r$, then $S$ meets $r$ at some $j$, and $j \notin T$. Line L6 adds $T \cup \{j\}$, which is a transversal of the first $t$ rows with $T \cup \{j\} \subseteq S$, so it is equal to $S$.

So $M_t \subseteq \mathrm{step}$, and every set of step is a transversal. A minimal set of step is then a minimal transversal: if it had a transversal as a proper subset, that subset would contain a set of $M_t \subseteq \mathrm{step}$, which contradicts its minimality in step. Conversely, a set of $M_t$ is minimal in step, since every set of step is a transversal. So the minimal sets of step are exactly $M_t$, and by Lemma 1 line L7 sets products to $M_t$. $\square$

**Lemma 3 (empty row).** If some row is empty, no transversal exists, and PETRICK returns the empty list.

*Proof.* No set meets an empty row. Line L3 returns $\emptyset$ when it reaches the first empty row. $\square$

**Theorem.** If every row is nonempty, PETRICK returns $M_m$, the set of all irredundant covers, and CHEAPEST returns a cover of least weight. If the rows are the on-set minterms of $f$ and the columns are all the primes of $f$, this cover is a minimum sum of products of $f$.

*Proof.* The first claim is Lemma 2 with $t = m$. A cover of the table is a transversal of all rows. Let $S$ be a cover of least weight. Each weight $w(j) = (1, \ell_j)$ is greater than $(0, 0)$, so removing a prime from a cover lowers its weight. If $S$ were not minimal, a proper subset would be a cover of smaller weight, which is impossible. So $S \in M_m$, and line L8, which takes the least weight over $M_m$, returns a set of the same weight as $S$. For the last claim, every set of primes whose union contains the on-set is a cover of $f$, since the primes lie inside the on-set together with the don't-care set. By Quine's theorem (see the prime implicant page) some minimum cover of $f$ consists of primes, so its weight is the least weight over the transversals of the table. $\blacksquare$

**Termination.** The loop of line L2 runs once per row, and each pass works on finite lists.
