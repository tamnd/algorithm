---
title: The first part of Toda's theorem, PH in BP.parityP, as a sketch
proves: [statement]
status: sketch
---

This file sketches the first part of the theorem, $\mathsf{PH} \subseteq \mathsf{BP} \cdot \oplus\mathsf{P}$. The second part, $\mathsf{BP} \cdot \oplus\mathsf{P} \subseteq \mathsf{P}^{\#\mathsf{P}[1]}$, is proved in full on the theorem page. The sketch leaves out three things: the proof that $\oplus\mathsf{P}^{\oplus\mathsf{P}} = \oplus\mathsf{P}$, the exact error bookkeeping when the operators are exchanged, and the analysis of pairwise independent hashing in the isolation lemma. They are in Toda (1991), in Arora and Barak, Chapter 17, and in Fortnow (2009), which gives a shorter route for the whole first part.

## Tools

**Closure of parity.** A language is in $\oplus\mathsf{P}$ if it is $\{x : f(x) \text{ odd}\}$ for some $f \in \#\mathsf{P}$. Because #P is closed under sums and products, $\oplus\mathsf{P}$ is closed under complement (use $f + 1$), under the AND of polynomially many queries (use the product of the counts, which is odd exactly when all are odd) and so under any Boolean combination of polynomially many $\oplus\mathsf{P}$ conditions given by a polynomial-size formula.

**Parity oracles.** $\oplus\mathsf{P}^{\oplus\mathsf{P}} = \oplus\mathsf{P}$ (Papadimitriou and Zachos 1983). The idea is that a nondeterministic machine can guess each oracle answer together with a witness for it, and the parity of the paths that guess a wrong answer cancels. This proof is left out.

**The BP operator.** $\mathsf{BP} \cdot \oplus\mathsf{P}$ is closed under complement, since $\oplus\mathsf{P}$ is. Its error can be reduced from $1/3$ to $2^{-p(n)}$ for any polynomial $p$ by taking the majority of $O(p(n))$ independent runs: the majority of polynomially many $\oplus\mathsf{P}$ conditions is again a $\oplus\mathsf{P}$ condition by the closure above, and the Chernoff bound controls the error. Two BP operators merge into one: $\mathsf{BP} \cdot \mathsf{BP} \cdot \oplus\mathsf{P} = \mathsf{BP} \cdot \oplus\mathsf{P}$.

## Step 1: NP is in BP.parityP

Let $\varphi$ be a formula in $n$ variables. By the [Valiant-Vazirani theorem](/valiant-vazirani-theorem/), choose $k$ uniformly in $\{2, \ldots, n + 1\}$ and a random function $h : \{0,1\}^n \to \{0,1\}^k$ from a pairwise independent family. If $\varphi$ is satisfiable, then with probability at least $1/(8n)$ exactly one satisfying assignment $a$ has $h(a) = 0^k$. Then the number of satisfying assignments with $h(a) = 0^k$ is $1$, which is odd. If $\varphi$ is unsatisfiable, this number is $0$ for every $h$, which is even.

So the condition "the number of satisfying $a$ with $h(a) = 0^k$ is odd" is a $\oplus\mathsf{P}$ condition on $(\varphi, k, h)$ with one-sided error. Repeat with $t = 16 n$ independent choices and take the OR of the $t$ conditions, a $\oplus\mathsf{P}$ condition by the closure above. The error on a satisfiable $\varphi$ is at most $(1 - 1/(8n))^{16n} < e^{-2} < 1/3$. So $\mathrm{SAT} \in \mathsf{BP} \cdot \oplus\mathsf{P}$, and since this class is closed under polynomial-time many-one reductions, $\mathsf{NP} \subseteq \mathsf{BP} \cdot \oplus\mathsf{P}$.

The argument relativizes: for every oracle $A$, $\mathsf{NP}^A \subseteq \mathsf{BP} \cdot \oplus\mathsf{P}^A$.

## Step 2: induction on the levels

Assume $\Sigma_k^p \subseteq \mathsf{BP} \cdot \oplus\mathsf{P}$. Then also $\Pi_k^p \subseteq \mathsf{BP} \cdot \oplus\mathsf{P}$ by closure under complement. Now

$$\Sigma_{k+1}^p = \mathsf{NP}^{\Sigma_k^p} \subseteq \mathsf{NP}^{\mathsf{BP} \cdot \oplus\mathsf{P}}.$$

**Moving the BP operator out of the oracle.** The NP machine makes polynomially many oracle queries on each path, and there are exponentially many paths, but all queries have polynomial length. Reduce the error of the oracle language to $2^{-p(n)}$ with $p$ larger than the number of possible queries times a margin. Then one random string $r$ answers every possible query correctly with probability at least $2/3$, by a union bound. Fix such an $r$: the oracle becomes a $\oplus\mathsf{P}$ language with $r$ as part of its input. This gives

$$\mathsf{NP}^{\mathsf{BP} \cdot \oplus\mathsf{P}} \subseteq \mathsf{BP} \cdot \mathsf{NP}^{\oplus\mathsf{P}}.$$

**Applying Step 1 relative to a parity oracle.** By the relativized Step 1 with $A \in \oplus\mathsf{P}$,

$$\mathsf{BP} \cdot \mathsf{NP}^{\oplus\mathsf{P}} \subseteq \mathsf{BP} \cdot \mathsf{BP} \cdot \oplus\mathsf{P}^{\oplus\mathsf{P}} = \mathsf{BP} \cdot \oplus\mathsf{P}^{\oplus\mathsf{P}} = \mathsf{BP} \cdot \oplus\mathsf{P},$$

using that two BP operators merge and that $\oplus\mathsf{P}^{\oplus\mathsf{P}} = \oplus\mathsf{P}$. So $\Sigma_{k+1}^p \subseteq \mathsf{BP} \cdot \oplus\mathsf{P}$, and by induction $\mathsf{PH} \subseteq \mathsf{BP} \cdot \oplus\mathsf{P}$.

## What the steps leave out

- The proof of $\oplus\mathsf{P}^{\oplus\mathsf{P}} = \oplus\mathsf{P}$, from Papadimitriou and Zachos (1983) and Toda (1991).
- The error bookkeeping in the merge of two BP operators and in the move of BP out of the oracle, where the error of each level must be reduced before the next level is built. Arora and Barak, Chapter 17, give it in full.
- The analysis of the isolation lemma, which is on the [Valiant-Vazirani theorem](/valiant-vazirani-theorem/) page.
- Fortnow (2009) avoids most of the operator calculus. His proof of the first part uses relativized forms of results known before Toda's work and fits in a few pages.
