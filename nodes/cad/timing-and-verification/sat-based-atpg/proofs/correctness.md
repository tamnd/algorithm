---
title: The ATPG formula is satisfiable exactly when the fault is detectable
proves: [correctness]
status: full
---

Let $C$ be a combinational circuit with lines in topological order and primary inputs $x_1, \ldots, x_n$, and let $(\ell, s)$ be the fault "line $\ell$ stuck at $s$". Let $K$ be the cone of $\ell$: the line $\ell$ and every line reachable from it. For a two-valued input vector $\tau$, write $g_\tau(k)$ and $b_\tau(k)$ for the values of line $k$ in the good and the faulty circuit. The formula $\Phi$ built by lines L1 to L6 has these parts.

- $\Gamma$: for every gate or branch $k$, the Tseitin clauses of $G_k = \mathrm{op}_k(G_{j_1}, \ldots)$, from line L1.
- $\Delta$: for every $k \in K$ with $k \ne \ell$, the Tseitin clauses of $F_k = \mathrm{op}_k(H_{j_1}, \ldots)$, where $H_j = F_j$ if $j \in K$ and $H_j = G_j$ otherwise, from line L3.
- The units $F_\ell = s$ and $G_\ell = \lnot s$, from line L4.
- For every primary output $o \in K$, the clauses of $D_o \leftrightarrow (G_o \oplus F_o)$, from line L5, and the clause $\bigvee_{o} D_o$, from line L6. If no output is in $K$, this clause is empty.

The Tseitin clauses of a gate with output variable $z$ have, for each value of the input variables, exactly one satisfying value of $z$, the gate value, and for XOR chains exactly one value of each helper variable (see the [Tseitin transformation](/tseitin-transformation/)).

**Lemma 1 (the variables are the circuit values).** For every vector $\tau$ there is exactly one assignment of the variables of $\Gamma$ and $\Delta$, with $G_{x_i} = \tau_i$ and $F_\ell = s$, that satisfies $\Gamma \cup \Delta$. In it, $G_k = g_\tau(k)$ for every line, and $F_k = b_\tau(k)$ for every $k \in K$.

*Proof.* Induction over the lines in topological order, using the Tseitin property. For $\Gamma$ this gives the good values. For $k \in K \setminus \{\ell\}$, each input $j$ of $k$ is in $K$, where $F_j = b_\tau(j)$ by induction, or not in $K$, where no path leads from $\ell$ to $j$, so $b_\tau(j) = g_\tau(j) = G_j$. So $F_k$ is the faulty gate value $b_\tau(k)$. And $F_\ell = s = b_\tau(\ell)$. $\square$

**Lemma 2 (outputs outside the cone).** For an output $o \notin K$ and every $\tau$, $g_\tau(o) = b_\tau(o)$.

*Proof.* The faulty circuit differs from the good one only at $\ell$, and no path leads from $\ell$ to $o$. Induction over the lines in topological order shows that every line outside $K$ has the same value in both circuits. $\square$

**Theorem 1.** $\Phi$ is satisfiable if and only if the fault is detectable. For every model, the values of $G_{x_1}, \ldots, G_{x_n}$ form a test.

*Proof.* Let $\tau$ detect the fault at output $o$. By Lemma 2, $o \in K$. If $g_\tau(\ell) = s$, the two circuits agree on every line, so $g_\tau(\ell) = \lnot s$. Take the assignment of Lemma 1 for $\tau$ and set each $D_o$ to $G_o \oplus F_o$. All clauses hold, and $D_o$ is true for the detecting output, so the last clause holds.

Conversely, let $\alpha$ be a model, and let $\tau_i = \alpha(G_{x_i})$. The restriction of $\alpha$ to $\Gamma \cup \Delta$ has $G_{x_i} = \tau_i$ and $F_\ell = s$, so by Lemma 1 it is the assignment of the circuit values. The last clause makes some $D_o$ true, and then $G_o \ne F_o$, that is, $g_\tau(o) \ne b_\tau(o)$. So $\tau$ detects the fault. $\square$

The unit $G_\ell = \lnot s$ is implied by the other clauses, since a model has a differing output and that needs a differing site. It is there to give the solver the activation value at once.

Line L7 adds, for every $k \in K$, a variable $A_k$ and the clauses $A_k \to (G_k \ne F_k)$, the clause $A_k \to \bigvee_{w} A_w$ over the fanouts $w$ of $k$ when $k$ is not a primary output, and the unit $A_\ell$. Call the result $\Phi_A$.

**Lemma 3 (paths of differences).** If $\tau$ detects the fault at output $o$, then there are lines $\ell = p_0, \ldots, p_r = o$, each a fanout of the one before, that all differ under $\tau$.

*Proof.* A line $k \ne \ell$ that differs is not a primary input, and since its gate is the same in both circuits, some input of $k$ differs. Walk back from $o$ along differing inputs. The walk ends, since the lines are in topological order, and it can end only at $\ell$. $\square$

**Theorem 2.** $\Phi_A$ is satisfiable if and only if $\Phi$ is satisfiable. The input values of a model of $\Phi_A$ form a test.

*Proof.* $\Phi_A$ contains $\Phi$, so a model of $\Phi_A$ is a model of $\Phi$ after the $A$ variables are dropped, and Theorem 1 gives the test. Conversely, take a model of $\Phi$ and its test $\tau$. Set $A_k$ true exactly when some path of lines that all differ under $\tau$ leads from $k$ to a primary output. Such a path stays in $K$. If $A_k$ is true, then $k$ differs, and if $k$ is not an output, the second line of its path is a fanout $w$ with $A_w$ true. By Lemma 3 applied to the detecting output, $A_\ell$ is true. So every new clause holds. $\square$
