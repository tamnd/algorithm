---
title: Espresso returns a prime and irredundant cover and stops
proves: [correctness]
status: full
---

We treat a cube and a cover as sets of points of $\{0,1\}^n$. Let $A = F \cup D$ be the points of the input on-set and don't-care set, and let $C = F \setminus D$ be the care points of the on-set. A cover $G$ is valid when $C \subseteq G \subseteq A$. A cube is an implicant when it lies in $A$, and prime when it is an implicant and no implicant contains it as a proper subset. A cover $G$ is irredundant when no cube $g \in G$ lies in $(G \setminus \{g\}) \cup D$. We assume that COMPLEMENT and the containment test are correct, as shown on the unate recursive paradigm page. So $R$, from line L1, is exactly the set of points outside $A$.

**Lemma 1 (EXPAND).** If every cube of $F$ is an implicant, then EXPAND(F, R) returns a cover of prime implicants whose union contains the union of $F$.

*Proof.* A cube is an implicant exactly when it meets no cube of $R$. Line L9 keeps only raises that meet no cube of $R$, so each grown cube is an implicant, and it contains the cube it started from. When line L10 stops, removing any one literal of $c$ gives a cube that meets $R$. Let $e$ be an implicant that contains $c$. Each position where $e$ has a dash and $c$ a literal gives a raise of $c$ inside $e$, which would meet no cube of $R$. So $e$ has the same literals as $c$, and $c$ is prime. A cube skipped at line L8 lies in a cube of the result. The final filter removes a cube only when it lies in another cube of the result, and of two equal cubes it removes only one, so the union does not change. $\square$

**Lemma 2 (IRREDUNDANT).** IRREDUNDANT(F, D) returns a subset $H$ of $F$ with $H \cup D = F \cup D$, and $H$ is irredundant.

*Proof.* Line L13 removes a cube that lies in $E \cup D$, and line L14 removes a cube that lies in what is left and $D$. Each removal keeps the union with $D$, since the removed cube lies in the union of the rest with $D$. For irredundancy, take $g \in E$. It does not lie in $(F \setminus \{g\}) \cup D$, and $H \setminus \{g\} \subseteq F \setminus \{g\}$, so it does not lie in $(H \setminus \{g\}) \cup D$. Take $g$ kept by line L14. When line L14 tested $g$, it did not lie in $E \cup (P \setminus \{g\}) \cup D$ for the $P$ of that moment. Later steps only remove cubes from $P$, so at the end $g$ still does not lie in $(H \setminus \{g\}) \cup D$. $\square$

**Lemma 3 (REDUCE).** If $G$ is valid, then REDUCE(G, D) returns a valid cover of implicants.

*Proof.* We show that after each pass of the loop over cubes, $G \cup D$ is unchanged on $C$, that is, $C \subseteq G \cup D$ stays true, and every cube is an implicant. Let $c$ be the current cube and $O$ the union of the other current cubes. Line L15 sets free to $c \setminus (O \cup D)$. If free is empty, $c \subseteq O \cup D$, and removing $c$ at line L16 keeps $C \subseteq G \cup D$. Otherwise line L17 replaces $c$ by the smallest cube $s$ that contains free. Since free $\subseteq c$ and $c$ is a cube, $s \subseteq c$, so $s$ is an implicant. The points of $c$ outside $s$ are outside free, so they lie in $O \cup D$. So $C \subseteq G \cup D$ again. As $C \cap D = \emptyset$, this means $C \subseteq G$. $\square$

**Theorem.** ESPRESSO returns a valid cover whose cubes are prime implicants, and the cover is irredundant.

*Proof.* The cubes of the input $F$ are implicants, and the input is valid. By Lemma 1, line L2 gives a valid cover of primes. By Lemma 2, line L3 gives an irredundant subset of it that is still valid, since removing cubes that $D$ and the rest cover keeps every point of $C$. Each pass of the loop applies Lemma 3, then Lemma 1 and then Lemma 2, so $G$ is a valid irredundant cover of primes after line L6. The loop returns $F$, which is either the output of line L3 or a $G$ of an earlier pass, so it has all three properties. $\blacksquare$

**Termination.** Let $F_0$ be the cover after line L3, with $c_0$ cubes. A pass that does not return sets $F$ to a cover $G$ with a strictly smaller cost in the lexicographic order. The costs are pairs $(a, b)$ of nonnegative integers with $a \le c_0$ and $b \le n a$, so there are at most $c_0 (n c_0 + 1)$ of them, and the loop runs at most that many times. EXPAND stops because each raise removes a literal. The recursions of COMPLEMENT and tautology stop by the argument on the unate recursive paradigm page.

**What is not claimed.** The result need not be a minimum cover. For $f = \sum m(1, 2, 3, 4, 5, 6)$ the result has four cubes, while a cover of three cubes exists. Every minimum cover can be made prime and irredundant, but not every prime and irredundant cover is minimum.
