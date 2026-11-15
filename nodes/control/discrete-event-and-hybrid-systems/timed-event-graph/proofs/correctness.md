---
title: The earliest firing times of a live timed event graph satisfy x(k) = A0* A1 x(k-1)
proves: [correctness]
status: full
---

A timed event graph has transitions $t_1, \dots, t_n$ and a set of places. Each place $p$ has one input transition $t_{j(p)}$, one output transition $t_{i(p)}$, $m_p \in \{0, 1\}$ initial tokens and a holding time $\tau_p \ge 0$. Tokens leave a place in the order in which they entered it. Under the earliest firing rule, the $k$-th firing of $t_i$ happens as soon as each input place of $t_i$ holds its $k$-th token and that token has stayed its holding time. The initial token of a place with $m_p = 1$ counts as the output of a firing of $t_{j(p)}$ at a given time $x_{j(p)}(0)$.

Notation is that of [max-plus algebra](/max-plus-algebra/), with $\varepsilon = -\infty$. Define $A_0, A_1 \in \mathbb{R}_{\max}^{n \times n}$ by

$$(A_m)_{ij} = \max \{\tau_p : j(p) = j,\ i(p) = i,\ m_p = m\},$$

with $\max \emptyset = \varepsilon$.

## Lemma 1: the firing equations

For $k \ge 1$, the firing times satisfy

$$x(k) = A_0 \otimes x(k) \oplus A_1 \otimes x(k-1).$$

*Proof.* Take a place $p$ from $t_j$ to $t_i$. Its tokens enter in the order of the firings of $t_j$: first the $m_p$ initial tokens, then one token for each firing of $t_j$. So the $k$-th token that $t_i$ takes from $p$ comes from the firing number $k - m_p$ of $t_j$, where firing number 0 stands for the initial token. That token is available at $x_j(k - m_p) + \tau_p$. The earliest firing rule fires $t_i$ for the $k$-th time at the latest of these availability times over the input places of $t_i$:

$$x_i(k) = \max_{p:\ i(p) = i} \left(\tau_p + x_{j(p)}(k - m_p)\right).$$

Grouping the places by $m_p$ and by $j$, and keeping only the largest holding time among parallel places, gives the matrix equation. $\square$

## Lemma 2: the star of an acyclic matrix

If the graph of $A_0$ has no circuit, then $A_0^{\otimes n} = \mathcal{E}$ (the matrix with all entries $\varepsilon$), $A_0^* = E \oplus A_0 \oplus \cdots \oplus A_0^{\otimes (n-1)}$, and for every $b$ the equation $x = A_0 \otimes x \oplus b$ has exactly one solution, $x = A_0^* \otimes b$.

*Proof.* $(A_0^{\otimes n})_{ij}$ is the largest weight of a walk of length $n$ from $j$ to $i$. Such a walk visits $n + 1$ nodes, so it repeats one and contains a circuit, which does not exist. So no such walk exists and the entry is $\varepsilon$.

Existence: $A_0 \otimes A_0^* \otimes b \oplus b = (A_0 \oplus \cdots \oplus A_0^{\otimes n} \oplus E) \otimes b = A_0^* \otimes b$, because $A_0^{\otimes n} = \mathcal{E}$.

Uniqueness: let $x = A_0 \otimes x \oplus b$. Substituting the equation into itself $n$ times gives

$$x = A_0^{\otimes n} \otimes x \oplus (E \oplus A_0 \oplus \cdots \oplus A_0^{\otimes (n-1)}) \otimes b = A_0^* \otimes b. \qquad \square$$

## Theorem

If the places with no initial token form no circuit, then for every $x(0)$ and $k \ge 1$ the earliest firing times are $x(k) = A \otimes x(k-1)$ with $A = A_0^* \otimes A_1$.

*Proof.* By Lemma 1, $x(k)$ solves $x = A_0 \otimes x \oplus b$ with $b = A_1 \otimes x(k-1)$. The zero-token places are exactly the arcs of the graph of $A_0$, so by hypothesis that graph has no circuit, and Lemma 2 gives $x(k) = A_0^* \otimes A_1 \otimes x(k-1)$. $\square$

If the zero-token places form a circuit, no transition on it can ever fire, because each waits for a token from the one before it; the net is not live. The function `mp_star` detects this case by checking $A_0^{\otimes n} \ne \mathcal{E}$, which by the argument of Lemma 2 holds exactly when the graph of $A_0$ has a circuit.

A place with $m_p \ge 2$ tokens can be split into a chain of $m_p$ places with one token each, joined by new transitions with holding time 0 on all but one place, so the restriction to $m_p \in \{0, 1\}$ loses no generality. The new transitions add entries to the state vector.

## Cost

Building $A_0$ and $A_1$ takes one pass over the places. The star uses $n - 1$ max-plus matrix products, plus one more for the circuit check, so $O(n^4)$ operations; a Floyd-Warshall style recursion would give $O(n^3)$. The product $A_0^* \otimes A_1$ takes $O(n^3)$ and each step of the recurrence takes $O(n^2)$.
