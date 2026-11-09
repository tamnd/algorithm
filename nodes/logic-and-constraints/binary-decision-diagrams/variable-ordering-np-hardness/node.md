---
tag: WTHETV
kind: theorem
slug: variable-ordering-np-hardness
name: NP-completeness of OBDD variable ordering
aliases:
- Bollig-Wegener theorem
- NP-hardness of optimal variable ordering
- improving the variable ordering is NP-complete
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: Given an OBDD and a bound s, it is NP-complete to decide whether some variable order gives at most s nodes. Bollig and Wegener 1996 for one output; Tani, Hamaguchi and Yajima 1993 for shared OBDDs.
prereqs: [variable-ordering, ordered-binary-decision-diagram, np-complete, polynomial-time-reduction]
see_also: [variable-ordering, friedman-supowit-ordering, bdd-sifting, window-permutation-reordering, np-completeness-proof, reduced-ordered-bdd]
sources:
  - paper: doi:10.1109/12.537122
    title: Beate Bollig and Ingo Wegener, Improving the variable ordering of OBDDs is NP-complete, IEEE Transactions on Computers 45(9), 1996, pages 993 to 1002
    locator: main theorem and its proof (reduction from optimal linear arrangement)
  - paper: "Seiichiro Tani, Kiyoharu Hamaguchi and Shuzo Yajima, The complexity of the optimal variable ordering problems of shared binary decision diagrams, ISAAC 1993, Lecture Notes in Computer Science 762, pages 389 to 398; journal version in IEICE Transactions on Information and Systems E79-D(4), 1996, pages 271 to 281"
    title: Tani, Hamaguchi and Yajima, The complexity of the optimal variable ordering problems of shared binary decision diagrams
    locator: main theorem (shared OBDDs, reduction from optimal linear arrangement)
  - paper: doi:10.1006/inco.2001.3076
    title: Detlef Sieling, The nonapproximability of OBDD minimization, Information and Computation 172(2), 2002, pages 103 to 138
    locator: main theorem (no constant-factor approximation unless P = NP)
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 5, The variable-ordering problem
  - paper: "Michael R. Garey, David S. Johnson and Larry Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 1976, pages 237 to 267"
    title: Garey, Johnson and Stockmeyer, Some simplified NP-complete graph problems
    locator: the NP-completeness of optimal linear arrangement
---

It is NP-complete to decide whether the variables of a given OBDD can be reordered so that the reduced diagram has at most $s$ nodes. Bollig and Wegener (1996) proved this for an OBDD with one root. Tani, Hamaguchi and Yajima (1993) had proved it before for shared OBDDs with several roots. Both proofs reduce the optimal linear arrangement problem on graphs to the ordering problem. The theorem explains why BDD packages use heuristics such as [sifting](/bdd-sifting/), and why the exact method, [Friedman-Supowit](/friedman-supowit-ordering/), takes exponential time. The problem itself, with its variants and methods, is on the page [variable ordering](/variable-ordering/).

## Statement

The variables are $x_1, \ldots, x_n$. For an order $\pi$ and a [Boolean function](/boolean-function/) $f$, $G_\pi(f)$ is the reduced $\pi$-OBDD of $f$, and $|G_\pi(f)|$ counts its nodes with the sinks. For a list $F$ of functions, $G_\pi(F)$ is the shared reduced OBDD.

**OBDD-ORDER.** The input is a $\pi$-OBDD $G$ (not necessarily reduced) of a function $f$, and an integer $s$. The question: is there an order $\pi'$ with $|G_{\pi'}(f)| \le s$?

**SHARED-OBDD-ORDER.** The same question for a shared $\pi$-OBDD of a list $F$ and the size $|G_{\pi'}(F)|$.

**Theorem (Tani, Hamaguchi and Yajima 1993).** SHARED-OBDD-ORDER is NP-complete.

**Theorem (Bollig and Wegener 1996).** OBDD-ORDER is NP-complete, already for OBDDs with one root.

The hypotheses matter. The function is given as an OBDD, which can be exponentially smaller than its truth table. If the input is the truth table, the [Friedman-Supowit](/friedman-supowit-ordering/) algorithm solves the problem in time polynomial in the table size.

The name of the paper, "improving the variable ordering", describes the same fact: given $G$ with order $\pi$, it is NP-hard to decide whether some other order gives fewer nodes than $\pi$ does. Take $s = |G_\pi(f)| - 1$.

## In plain words

Suppose that someone gives you a BDD and asks: can this be made smaller by a new order of the variables? There is no known fast method that always answers this, and the theorem says why. A fast method would also solve a known hard puzzle: put the points of a network on a line, so that the total length of the links is as small as possible. The proof turns each such network into a BDD whose best size tells the best total length. So BDD ordering is at least as hard as that puzzle. Since the puzzle is one of the hard problems for which no fast method is expected, tools use fast guesses that are often good, not methods that are always best.

## Proof

The theorem has two parts. The part "in NP" has a full proof below. For the part "NP-hard" we give only the proof idea. The two constructions are long, and we do not reproduce their gadgets here.

**Lemma 1 (restriction does not grow).** For each order $\pi$, each variable $x_i$ and each $c \in \{0, 1\}$, $|G_\pi(f|_{x_i = c})| \le |G_\pi(f)|$.

*Proof.* Start from $G_\pi(f)$. Redirect each edge that points to a node with variable $x_i$ to the $c$-child of that node, and do the same for the root pointer. The result is still a $\pi$-OBDD, because the new targets are lower in the order. On each input it follows the old path, except that it takes the $c$-edge at $x_i$ without a test, so it computes $f|_{x_i=c}$. It uses only nodes of $G_\pi(f)$. The reduction rules only delete nodes, so the reduced diagram $G_\pi(f|_{x_i=c})$ has at most $|G_\pi(f)|$ nodes. $\square$

**Lemma 2 (membership in NP).** OBDD-ORDER and SHARED-OBDD-ORDER are in NP.

*Proof.* The certificate is an order $\pi'$, of length $O(n \log n)$ bits. The check builds $G_{\pi'}$ from $G$ bottom-up. Process the nodes of $G$ so that each node comes after its children. A sink becomes the same sink. A node $v$ with variable $x_i$ and children $v_0, v_1$ becomes $h_v = \mathrm{ITE}(x_i, h_{v_1}, h_{v_0})$, computed in a manager with order $\pi'$. By the [Shannon expansion](/shannon-expansion/), $h_v$ is the function $f_v$ of node $v$. Take a path from the root to $v$, and let $a$ be the assignment of the variables that it tests. In an OBDD, $f_v$ does not depend on these variables, so $f_v = f|_a$. Lemma 1, applied once for each variable of $a$, gives $|G_{\pi'}(f_v)| \le |G_{\pi'}(f)|$. For a shared OBDD, the same holds with $f$ replaced by a root function $f_j$ above $v$, and $|G_{\pi'}(f_j)| \le |G_{\pi'}(F)|$.

First, if $s \ge |G|$, answer yes with $\pi' = \pi$: the reduction rules never add nodes, so $|G_\pi| \le |G| \le s$. Otherwise $s < |G|$. If the answer is yes for $\pi'$, each $h_v$ has at most $s$ nodes, so the check can stop with no as soon as some $h_v$ has more than $s$ nodes. Each ITE whose first argument is one variable takes $O(s^2)$ time with a [computed table](/computed-table/). So the check takes $O(|G| s^2) = O(|G|^3)$ time, and at the end it compares the size of the shared result with $s$. $\square$

**Lemma 3 (NP-hardness, proof idea).** The problem OPTIMAL LINEAR ARRANGEMENT is NP-complete (Garey, Johnson and Stockmeyer 1976): given a graph $H = (V, E)$ and an integer $K$, is there a bijection $\psi : V \to \{1, \ldots, |V|\}$ with

$$\sum_{\{u, w\} \in E} |\psi(u) - \psi(w)| \le K \, ?$$

Both proofs map $(H, K)$ in polynomial time to an OBDD instance $(G, s)$.

- The constructions give each vertex of $H$ its own variables, and build the functions from parts for the edges, so that the size of the part for an edge grows with the number of levels between the variables of its two endpoints. This bullet is our summary of the idea, not the exact construction; see the papers and Wegener's Chapter 5 for the gadgets.
- The main step is a normal-form argument: each order can be changed into an order of a special form without an increase of the size. In the special form, the order of the vertex variables is a linear arrangement $\psi$ of $H$, and the size is an explicit affine function of the cost of $\psi$. Then the OBDD has an order of size at most $s$ exactly when $H$ has an arrangement of cost at most $K$.
- For one root (Bollig and Wegener), the outputs of the shared construction must be combined into one function without a loss of control over the size. This needs further gadgets and a longer normal-form argument. This is the main new work of the 1996 paper.

Lemma 2 and Lemma 3 together give the two theorems. $\blacksquare$

## Consequences

- **No polynomial exact algorithm unless P = NP.** Exact methods, such as the $O(n^2 3^n)$ [Friedman-Supowit](/friedman-supowit-ordering/) program, take exponential time in the worst case.
- **Heuristics.** [Sifting](/bdd-sifting/) and [window permutation](/window-permutation-reordering/) run in polynomial time per pass, so by the theorem they cannot always find the best order unless P = NP. Their results are known only from measurements.
- **Approximation.** Sieling (2002) strengthened the theorem: for each constant $c > 1$, it is NP-hard to find an order whose size is at most $c$ times the best size. An earlier paper by Sieling (STACS 1998) excluded a polynomial-time approximation scheme.
- **The input matters.** For a truth table input, the problem is in polynomial time in the table size. The hardness comes from the compact OBDD input.

## Tightness

- The problem is in NP (Lemma 2), so NP-complete is the exact class of the decision version.
- The input of the hard instances is an OBDD of polynomial size. So the hardness does not come from a huge input or a huge diagram: even the question whether a small OBDD can be made smaller is hard.
- With the truth table as input, the problem is polynomial, so the theorem does not hold for that input form unless P = NP.

## History

Bryant (1986) showed by examples that the order can change the size by an exponential factor and asked how to find good orders. Friedman and Supowit (1990) gave an exact algorithm in $O(n^2 3^n)$ time. Tani, Hamaguchi and Yajima proved NP-completeness for shared OBDDs at ISAAC 1993, with a journal version in 1996. Bollig and Wegener closed the case of one output in 1996, after the question had been open for some years. Sieling then proved the nonapproximability results (1998 and 2002). Wegener's book (2000) presents the hardness proofs in Chapter 5.

## References
