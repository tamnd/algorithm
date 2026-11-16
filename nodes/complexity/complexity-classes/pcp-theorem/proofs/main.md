---
title: The PCP theorem, a sketch of the algebraic proof and of Dinur's proof
proves: [statement]
status: sketch
---

This file gives the hard inclusion $\mathsf{NP} \subseteq \mathsf{PCP}(\log n, 1)$ as a sketch, in two routes. The algebraic route follows Arora and Safra (1998) and Arora, Lund, Motwani, Sudan and Szegedy (1998). The combinatorial route follows Dinur (2007). The easy inclusion $\mathsf{PCP}(\log n, 1) \subseteq \mathsf{NP}$ is proved in full on [probabilistically checkable proof](/probabilistically-checkable-proof/). The sketch leaves out the analysis of the low-degree test, the proof of the composition theorem, the construction of the assignment tester and the expander analysis of the powering step. These steps are in the papers cited on the theorem page and in Arora and Barak, Chapter 22.

## The algebraic route

**Step 1: an outer verifier from low-degree polynomials.** Encode an assignment to a 3-SAT instance with $n$ variables as a polynomial of low degree over a finite field $\mathbb{F}$, in $m = O(\log n / \log\log n)$ variables, given by its table of values on $\mathbb{F}^m$. This is a codeword of the [Reed-Muller code](/reed-muller-code/). The table has polynomial size, and a position in it is named by $O(\log n)$ bits.

**Step 2: the low-degree test.** A cheating proof is an arbitrary table. The verifier picks a random line in $\mathbb{F}^m$ and checks that the table restricted to the line agrees with a univariate polynomial of low degree, which the proof also supplies. The [low-degree test](/low-degree-test/) theorem says that a table that passes with high probability is close to a single polynomial of low degree. Its analysis is left out.

**Step 3: checking the clauses by sum-check.** As in [IP = PSPACE](/ip-equals-pspace/), the condition "every clause is satisfied" becomes the statement that a polynomial built from the encoded assignment vanishes on a subcube. A random linear combination turns it into one sum, and the proof supplies the sum-check polynomials for it, as tables. The verifier needs the encoded assignment at a few random points, which it reads with self-correction along random lines.

**Step 4: the outer verifier.** Steps 1 to 3 give a verifier with $O(\log n)$ random bits and perfect completeness that reads a constant number of *symbols*, each of $\mathrm{poly}(\log n)$ bits (a field element or a univariate polynomial). So it reads $\mathrm{poly}(\log n)$ bits in total, which is too many.

**Step 5: proof composition.** Arora and Safra observed that the verifier's decision is itself a small computation on the bits it reads. Instead of reading these bits, the verifier can ask for a proof that the decision accepts, and check that proof with a second verifier, the *inner verifier*. The inner proof must also show that the bits it talks about are consistent with the symbols in the outer proof, which needs an outer verifier whose answers are encoded so that they can be checked locally. Composing the outer verifier with itself reduces the query count from $\mathrm{poly}(\log n)$ bits to $\mathrm{poly}(\log\log n)$ bits, with $O(\log n)$ random bits in total. The composition theorem is left out.

**Step 6: the Hadamard inner verifier.** Arora, Lund, Motwani, Sudan and Szegedy used the verifier based on the [Hadamard code](/hadamard-code/) as the last inner verifier. On an input of size $N$ it uses $\mathrm{poly}(N)$ random bits and $O(1)$ queries, with the [linearity test](/linearity-test/). Applied to a decision of size $N = \mathrm{poly}(\log\log n)$, it uses $\mathrm{poly}(\log\log n) = o(\log n)$ random bits and $O(1)$ queries. The composed verifier has $O(\log n)$ random bits, $O(1)$ queries, completeness $1$ and soundness bounded away from $1$, and repetition brings the soundness to $1/2$. $\square$

## Dinur's route

**Step 1: constraint graphs.** A [constraint graph](/constraint-graph/) has a set of variables over a constant alphabet $\Sigma$ and a binary constraint on each edge. Its *unsatisfiability* $\mathrm{UNSAT}(G)$ is the least fraction of edges violated by an assignment. Graph 3-coloring is NP-hard and is a constraint graph with $|\Sigma| = 3$. If $G$ is not colorable, $\mathrm{UNSAT}(G) \ge 1/|E|$. The goal is a polynomial-time map that keeps satisfiable graphs satisfiable and raises $\mathrm{UNSAT}$ to a constant. By the gap form on the theorem page, this proves the theorem.

**Step 2: preprocessing.** Replace each vertex by an expander graph to make the graph regular of constant degree, and add the edges of an expander with trivial constraints. The size grows by a constant factor, and $\mathrm{UNSAT}$ falls by at most a constant factor.

**Step 3: powering.** Make a new graph $G^t$ on the same vertices. A vertex now holds a value for each vertex within distance $t$, its *opinion* about its neighborhood. The edges are walks of length about $t$, and an edge checks that the opinions of its two ends agree and satisfy the constraints along the walk. The alphabet grows to $|\Sigma|^{d^{t}}$, a constant, and the size grows by a constant factor. The main lemma says that $\mathrm{UNSAT}(G^t) \ge \Omega(\sqrt{t}) \cdot \min\big(\mathrm{UNSAT}(G), 1/t\big)$. The proof uses the expander mixing property of the preprocessed graph and is left out.

**Step 4: alphabet reduction.** Bring the alphabet back to a fixed size $\Sigma_0$ by composition with an *assignment tester*: a constant-size PCP of proximity that checks one constraint over the large alphabet using constraints over $\Sigma_0$. Since the tested constraints have constant size, any construction works, even one with exponentially long proofs such as the Hadamard verifier. The step loses a constant factor in $\mathrm{UNSAT}$ and grows the size by a constant factor. The construction of the tester is left out.

**Step 5: iteration.** Choose $t$ so that Steps 2 to 4 together at least double $\mathrm{UNSAT}$ while it is below a fixed constant $\alpha$, and keep it at least $\alpha$ once it is there. Each round multiplies the size by a constant $C$. Start from $\mathrm{UNSAT} \ge 1/|E|$ and apply $\lceil \log_2 |E| \rceil$ rounds. Then $\mathrm{UNSAT} \ge \alpha$, and the size is $C^{O(\log |E|)} |E| = \mathrm{poly}(|E|)$. Satisfiable graphs stay satisfiable in every step. Writing each constraint over $\Sigma_0$ as a constant number of 3-clauses gives $\text{gap-3SAT}[1, 1 - \varepsilon]$. $\square$
