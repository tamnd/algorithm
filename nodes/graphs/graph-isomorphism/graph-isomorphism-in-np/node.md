---
tag: GWMWS8
kind: theorem
slug: graph-isomorphism-in-np
name: Graph isomorphism is in NP
area: graphs/graph-isomorphism
level: intro
summary: An isomorphism between two graphs is a polynomial-size certificate that can be checked in polynomial time.
prereqs: [graph-isomorphism-definition, np, polynomial-time-verifier]
see_also: [graph-isomorphism-problem, np-intermediate, interactive-proofs, zero-knowledge-proof, polynomial-hierarchy, co-np, gi-completeness, subgraph-isomorphism]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 2 (NP and the verifier definition) and Chapter 8, Interactive proofs (the private-coin protocol for graph non-isomorphism, and the consequence that graph isomorphism is not NP-complete unless the polynomial hierarchy collapses)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 7.3, The class NP (verifiers), and Section 10.4, Interactive proof systems (graph non-isomorphism)
  - paper: doi:10.1145/116825.116852
    title: Oded Goldreich, Silvio Micali and Avi Wigderson, Proofs that yield nothing but their validity or all languages in NP have zero-knowledge proof systems, Journal of the ACM 38(3), 690 to 728 (1991)
    locator: the interactive proof for graph non-isomorphism and the zero-knowledge proof for graph isomorphism
  - paper: doi:10.1016/0020-0190(87)90232-8
    title: Ravi B. Boppana, Johan Håstad and Stathis Zachos, Does co-NP have short interactive proofs?, Information Processing Letters 25(2), 127 to 132 (1987)
    locator: the whole paper (if co-NP has constant-round interactive proofs, the polynomial hierarchy collapses to its second level)
  - paper: "Jacobo Torán, On the hardness of graph isomorphism, SIAM Journal on Computing 33(5), 1093 to 1108 (2004)"
    locator: the whole paper (hardness of graph isomorphism for NL, PL and DET under AC0 reductions)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Chapter 7, Beyond NP-completeness (graph isomorphism as a problem of open status), and the list of open problems at the end of the Appendix
---

The [graph isomorphism problem](/graph-isomorphism-problem/) is in [NP](/np/): when two graphs are isomorphic, the isomorphism itself is a certificate of $O(n \log n)$ length, and a [verifier](/polynomial-time-verifier/) checks it in $O(n^2)$ time. This is the easy half of the complexity of graph isomorphism. The open question is the other side: no polynomial-time algorithm is known, and the problem is believed not to be [NP-complete](/np-complete/), because its complement has a constant-round interactive proof. It is the best known natural candidate for an [NP-intermediate](/np-intermediate/) problem.

## Statement

Let $\mathrm{GI} = \{ \langle G, H \rangle : G \cong H \}$, where $G$ and $H$ are simple undirected graphs given by adjacency matrices, so the input length is $N = 2n^2$ for graphs with $n$ vertices each (pairs with different vertex counts are rejected at once).

**Theorem.** $\mathrm{GI} \in \mathrm{NP}$. More precisely, there is a deterministic verifier $V$ that, on input $\langle G, H \rangle$ and a certificate $c$, runs in $O(n^2)$ steps on a [word RAM](/word-ram/) (and in polynomial time on a [Turing machine](/turing-machine/)), such that

$$\langle G, H \rangle \in \mathrm{GI} \iff \exists c \text{ with } |c| = O(n \log n) \text{ and } V(\langle G, H \rangle, c) = \text{accept}.$$

The same holds for directed graphs, multigraphs given by multiplicity matrices, and vertex-colored or edge-labeled graphs.

## In plain words

Someone claims that two networks are the same network with the nodes renamed. To convince you, they hand you the renaming: for each node of the first network, its name in the second. You check two things. First, the renaming uses each name of the second network exactly once. Second, for each pair of nodes of the first network, they are linked exactly when their new names are linked in the second network. Both checks are fast. If the networks really are the same, a good renaming exists, and you accept it. If they are not, no renaming passes your checks, so nobody can fool you. Finding the renaming may be hard; checking it is easy.

## Proof

Let $G = (V, E)$ and $H = (W, F)$ with $V = W = \{1, \ldots, n\}$, given by adjacency matrices $A$ and $B$. The certificate is a list $c = (c_1, \ldots, c_n)$ of integers, read as the map $\varphi(i) = c_i$. Each $c_i$ needs $\lceil \log_2 (n+1) \rceil$ binary digits, so $|c| = O(n \log n)$.

The verifier $V$ does the following.

1. If $G$ and $H$ have different numbers of vertices, reject.
2. If some $c_i \notin \{1, \ldots, n\}$, reject. Use an array $\mathit{seen}[1 \ldots n]$, set to false. For $i = 1, \ldots, n$: if $\mathit{seen}[c_i]$, reject; else set $\mathit{seen}[c_i] \leftarrow$ true.
3. For all $i, j \in \{1, \ldots, n\}$: if $A[i][j] \ne B[c_i][c_j]$, reject.
4. Accept.

*Running time.* Step 2 takes $O(n)$ steps and step 3 takes $n^2$ comparisons, each $O(1)$ on a word RAM with words of $\Theta(\log n)$ binary digits. The total is $O(n^2)$, linear in the input length. On a multitape Turing machine each matrix lookup costs at most $O(N)$ steps, so the total is $O(N^2)$, still polynomial.

*Completeness.* Assume $G \cong H$ and let $\varphi$ be an isomorphism. Take $c_i = \varphi(i)$. Since $\varphi$ is a bijection onto $\{1, \ldots, n\}$, step 2 finds no value out of range and no value twice. Since $\varphi$ is an isomorphism, $\{i, j\} \in E \iff \{\varphi(i), \varphi(j)\} \in F$, so $A[i][j] = B[\varphi(i)][\varphi(j)]$ for all $i, j$, and step 3 does not reject. $V$ accepts.

*Soundness.* Assume $V$ accepts $c$. Step 2 shows that $c_1, \ldots, c_n$ are $n$ distinct values in $\{1, \ldots, n\}$, so $\varphi : i \mapsto c_i$ is a bijection. Step 3 shows $A[i][j] = B[\varphi(i)][\varphi(j)]$ for all $i, j$, which is the condition $\{i, j\} \in E \iff \{\varphi(i), \varphi(j)\} \in F$. So $\varphi$ is an isomorphism and $G \cong H$. Contrapositive: if $G \not\cong H$, no certificate is accepted.

For directed graphs, step 3 compares ordered pairs, which the matrix comparison already does. For multigraphs, the entries are multiplicities. For vertex colors, add the check $\mathrm{col}_G(i) = \mathrm{col}_H(c_i)$ for all $i$; for edge labels, compare labels instead of bits. Each change adds $O(n)$ or nothing to the cost. $\blacksquare$

## Consequences

- **Not likely NP-complete.** The complement, graph non-isomorphism, has a two-round private-coin interactive proof (Goldreich, Micali and Wigderson 1991): the verifier picks $i \in \{1, 2\}$ and a random permutation $\pi$, sends $\pi(G_i)$, and accepts when the prover names $i$. If $G_1 \not\cong G_2$ an all-powerful prover always answers correctly; if $G_1 \cong G_2$ the message hides $i$ and any prover is right with probability $1/2$. By Goldwasser and Sipser, private coins can be replaced by public coins, so graph non-isomorphism is in AM and GI is in coAM. Boppana, Håstad and Zachos (1987) proved that if a problem in coAM is NP-complete, then the [polynomial hierarchy](/polynomial-hierarchy/) collapses to its second level. So GI is not NP-complete unless this collapse happens.
- **Zero knowledge.** The same certificate structure gives a [zero-knowledge proof](/zero-knowledge-proof/) of isomorphism: the prover sends a random isomorphic copy, and on a random challenge reveals the map from $G$ or from $H$ to the copy.
- **Search to decision.** A decision procedure for GI gives an isomorphism with $O(n^2)$ calls: fix vertex $1$ of $G$ to each vertex $w$ of $H$ by attaching the same unique gadget (or color) to both, keep a choice that stays isomorphic, and continue with the next vertex. This is the [search-to-decision reduction](/search-to-decision-reduction/) for GI.
- **Variants in NP.** [Subgraph isomorphism](/subgraph-isomorphism/) is in NP by the same certificate, and it is NP-complete. Isomorphism of groups given by multiplication tables, of hypergraphs and of other finite structures is in NP for the same reason; many of these are [GI-complete](/gi-completeness/).

## Tightness

GI lies in NP and, by the interactive proof above, in coAM. Whether GI is in P is open. The best known running time is quasipolynomial, $\exp((\log n)^{O(1)})$, by [Babai's algorithm](/babai-quasipolynomial-algorithm/) (announced in 2015). Lower bounds are weak: Torán (2004) showed that GI is hard for the class DET under $\mathrm{AC}^0$ reductions, which is far from NP-hardness.

## History

That GI is in NP is immediate from the definition and was noted from the start of the theory of NP-completeness; Karp listed graph isomorphism in 1972 among problems whose status was open, and Garey and Johnson (1979) list it among the open problems. Goldreich, Micali and Wigderson gave the interactive proof for non-isomorphism in 1986 (journal version 1991), and Boppana, Håstad and Zachos drew the consequence for NP-completeness in 1987.

## References
