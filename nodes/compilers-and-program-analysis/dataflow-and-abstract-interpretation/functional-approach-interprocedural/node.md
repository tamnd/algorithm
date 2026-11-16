---
tag: KZA2TR
kind: technique
slug: functional-approach-interprocedural
name: Functional approach to interprocedural analysis
aliases:
- procedure summaries
- Sharir-Pnueli functional approach
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Computes for each procedure a summary function from input facts to output facts and applies it at each call site.
prereqs: [interprocedural-dataflow-analysis, distributive-dataflow-framework, mop-mfp-coincidence-theorem]
see_also: [context-sensitivity, ifds-framework, ide-framework, interprocedural-constant-propagation, mod-ref-analysis, pushdown-reachability, elimination-dataflow-methods, tabulation]
sources:
  - paper: "Micha Sharir and Amir Pnueli, Two approaches to interprocedural data flow analysis, in Steven S. Muchnick and Neil D. Jones (eds.), Program Flow Analysis: Theory and Applications, Prentice-Hall, 1981"
    locator: the functional approach (summary functions computed for each procedure, then applied at the calls), its exactness for distributive frameworks, and its variant for finite lattices that tabulates the summaries only at the inputs that occur
  - paper: doi:10.1007/3-540-55984-1_13
    title: "Jens Knoop and Bernhard Steffen, The interprocedural coincidence theorem, Compiler Construction (CC '92), Lecture Notes in Computer Science, 125 to 140, 1992"
    locator: the interprocedural fixed point equals the meet over valid paths when every function is distributive
  - paper: doi:10.1145/199448.199462
    title: "Thomas Reps, Susan Horwitz and Mooly Sagiv, Precise interprocedural dataflow analysis via graph reachability, Proceedings of the 22nd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '95), 49 to 61, 1995"
    locator: summaries of distributive subset functions as path edges and summary edges in the exploded supergraph
  - paper: doi:10.1016/0304-3975(96)00072-2
    title: "Mooly Sagiv, Thomas Reps and Susan Horwitz, Precise interprocedural dataflow analysis with applications to constant propagation, Theoretical Computer Science 167(1-2), 131 to 170, 1996"
    locator: summaries made of environment transformers with a compact representation, applied to linear constant propagation
  - paper: doi:10.1016/j.scico.2005.02.009
    title: "Thomas Reps, Stefan Schwoon, Somesh Jha and David Melski, Weighted pushdown systems and their application to interprocedural dataflow analysis, Science of Computer Programming 58(1-2), 206 to 263, 2005"
    locator: summaries as weights in a bounded idempotent semiring, computed by pushdown reachability
  - paper: doi:10.1145/2487568.2487569
    title: "Rohan Padhye and Uday P. Khedker, Interprocedural data flow analysis in Soot using value contexts, Proceedings of the 2nd ACM SIGPLAN International Workshop on State of the Art in Java Program Analysis (SOAP '13), 31 to 36, 2013"
    locator: value contexts, a tabulated functional approach that keys each analysis of a procedure by its input value
---

The functional approach of Sharir and Pnueli (1981) analyzes a procedure once, as a function. For each procedure it computes a *summary*: a function that maps the fact at the entry of the procedure to the fact at its exit, over all ways through the body, including the calls it makes. At each call site, the analysis applies the summary of the callee to the fact before the call. A fact that comes into a procedure from one caller then goes back to that caller only, so the analysis follows only valid paths, at any depth of calls and with recursion. For distributive frameworks it computes exactly the meet over valid paths (MVP) of [interprocedural dataflow analysis](/interprocedural-dataflow-analysis/). The [IFDS](/ifds-framework/) and [IDE](/ide-framework/) frameworks are efficient forms of it for special kinds of summaries.

## In plain words

When you read a program by hand, you do not reread a helper function every time it is called. You read it once, write down what it does ("adds one to its argument", "sets the flag"), and use that note at every call. The functional approach does the same. First it works out a note for each procedure that says, for any fact that holds when the procedure starts, what holds when it returns. A procedure that calls itself needs a few rounds until its note stops changing. Then it starts at the main procedure and uses the notes to carry facts across every call. Because each call gets its own answer from the note, facts from one caller never leak to another.

## When it applies

- The transfer functions have a representation that is closed under composition and pointwise meet, and that has a cheap equality test. Gen-kill pairs, distributive functions on subsets of a finite set (as relations), and the linear functions of [IDE](/ide-framework/) all qualify.
- The space of these functions has finite height, so the iteration of phase 1 stops. For gen-kill functions over $u$ facts the height is $O(u)$.
- For an exact answer, every function is distributive. For monotone functions, the result is still sound, but it can be below MVP.
- If no compact representation exists but the lattice is finite, the tabulated variant computes each summary only at the input values that actually reach the procedure (see Variations).

## The template

Use the meet convention of Kildall: $\top$ is the start value, the result is the greatest solution, and lower values are less precise. (The join convention of Cousot flips the order.) The supergraph of the [interprocedural dataflow analysis](/interprocedural-dataflow-analysis/) page gives, for each call site $s$ in a procedure that calls $q$, a call point $c_s$, a return point $r_s$, a function $\mathit{call}_s$ on the call edge, a function $h_s$ on the return edge, and a function $l_s$ on the call-to-return edge, which carries the caller's local facts around the call. Edges inside a procedure carry functions $f_e$. The holes are REPR, a representation of functions with the operations COMPOSE ($\circ$), MEET ($\sqcap$) and APPLY, and the order of the worklist.

```pseudo id=main
SUMMARIES(program, ι)
L1  for each point n of each procedure p do φ[n] ← λx.⊤        ▷ phase 1: summaries
L2  for each procedure p do φ[entry_p] ← id; add entry_p to W
L3  while W is not empty do
L4      remove a point m from W
L5      for each edge (m, n) inside a procedure, with function f do UPDATE(n, f ∘ φ[m])
L6      if m = c_s for a call site s that calls q then
L7          UPDATE(r_s, (h_s ∘ φ[exit_q] ∘ call_s ∘ φ[c_s]) ⊓ (l_s ∘ φ[c_s]))
L8      if m = exit_q then add c_s to W for every call site s of q
L9  for each procedure p do X[entry_p] ← ⊤                     ▷ phase 2: entry values
L10 X[entry_main] ← ι; add main to W
L11 while W is not empty do
L12     remove a procedure p from W
L13     for each call site s in p, calling q do
L14         v ← call_s(φ[c_s](X[entry_p]))
L15         if X[entry_q] ⊓ v ≠ X[entry_q] then X[entry_q] ← X[entry_q] ⊓ v; add q to W
L16 for each point n of each procedure p do X[n] ← φ[n](X[entry_p])
L17 return X
```

UPDATE$(n, g)$ sets $\varphi[n] \leftarrow \varphi[n] \sqcap g$ and adds $n$ to $W$ if this changes $\varphi[n]$. After phase 1, $\varphi[n]$ maps the fact at the entry of the procedure of $n$ to the fact at $n$, and $\varphi[\mathit{exit}_q]$ is the summary of $q$. Line L8 handles recursion and calls to procedures whose summary is not final yet: when a summary drops, every call site that used it is looked at again.

**Correctness.** Call a path *same-level valid* if its call and return edges match as brackets, as on the [interprocedural dataflow analysis](/interprocedural-dataflow-analysis/) page. A path may also take a call-to-return edge. Let $\mathrm{SL}(n) = \mathop{\large\sqcap} \{ f_\pi : \pi$ a same-level valid path from $\mathit{entry}_p$ to $n \}$, where $f_\pi$ is the composition of the functions along $\pi$.

*Lemma 1 (phase 1).* If all functions are monotone, $\varphi[n] \sqsubseteq \mathrm{SL}(n)$. If they are also distributive, $\varphi[n] = \mathrm{SL}(n)$.

*Proof.* Phase 1 is a chaotic iteration from $\top$ on the inequations $\varphi[\mathit{entry}_p] \sqsubseteq \mathrm{id}$, $\varphi[n] \sqsubseteq f \circ \varphi[m]$ and the inequation of line L7. In a lattice of finite height it stops at the greatest solution, as in the [Kleene fixed-point theorem](/kleene-fixed-point-theorem/). For the first part, show $\varphi[n] \sqsubseteq f_\pi$ by induction on the length of $\pi$. If $\pi$ ends with an edge inside a procedure, use the inequation of L5 and monotonicity. If $\pi = \pi' \cdot (c_s \to \mathit{entry}_q) \cdot \rho \cdot (\mathit{exit}_q \to r_s)$ with $\rho$ same-level valid in $q$, the induction gives $\varphi[c_s] \sqsubseteq f_{\pi'}$ and $\varphi[\mathit{exit}_q] \sqsubseteq f_\rho$, and the inequation of L7 gives $\varphi[r_s] \sqsubseteq h_s \circ f_\rho \circ \mathit{call}_s \circ f_{\pi'} = f_\pi$. The call-to-return edge is the same. For the second part, show that SL is a solution. Distributive functions commute with meets, and in a lattice of finite height every meet is a finite meet. So $f \circ \mathrm{SL}(m)$ is the meet of $f \circ f_\pi$ over the paths $\pi$ to $m$, and each $f \circ f_\pi$ is the function of a same-level valid path to $n$. The right side of L7 expands in the same way into a meet of functions of same-level valid paths to $r_s$. So SL is below every right side, and $\mathrm{SL} \sqsubseteq \varphi$ because $\varphi$ is the greatest solution. $\square$

*Lemma 2 (phase 2).* A valid path to a point $n$ of $p$ splits at its last unmatched call edge into a valid path to $\mathit{entry}_p$ and a same-level valid path from $\mathit{entry}_p$ to $n$. So $\mathrm{MVP}(n) = \mathrm{SL}(n)(\mathrm{MVP}(\mathit{entry}_p))$ when the functions are distributive, and the values $\mathrm{MVP}(\mathit{entry}_q)$ form the greatest solution of the inequations of lines L10 to L15. The proof is the same as for Lemma 1, with values in place of functions. $\square$

*Theorem (interprocedural coincidence; Sharir and Pnueli 1981, Knoop and Steffen 1992).* If every function is distributive and the function space has finite height, SUMMARIES stops and returns $X = \mathrm{MVP}$. If the functions are only monotone, $X \sqsubseteq \mathrm{MVP}$, so the result is sound.

**Cost.** Let $H$ be the height of the space of functions, $E$ the number of edges of the supergraph, and $C$ the number of call sites. Each $\varphi[n]$ drops at most $H$ times, and each drop costs work in proportion to the out-edges of $n$, plus the call sites of $q$ when $n = \mathit{exit}_q$. Over all procedures, the call sites revisited at line L8 add up to $H C$, so phase 1 takes $O(H (E + C))$ function operations. Phase 2 does the same with the height of $L$. For gen-kill problems over $u$ facts, $H = O(u)$ and each operation costs $O(u / w)$ word operations.

### Walk-through: reaching definitions with recursion

The definitions $d_1$ and $d_2$ both assign the global `g`. A gen-kill function is a pair (gen, kill) with $f(x) = (x \setminus \mathit{kill}) \cup \mathit{gen}$. The meet is $\cup$ on sets and $(g_1 \cup g_2, k_1 \cap k_2)$ on pairs, and $(g_2, k_2) \circ (g_1, k_1) = (g_2 \cup (g_1 \setminus k_2), k_1 \cup k_2)$. Since `g` is global, $\mathit{call}_s$ and $h_s$ are the identity, and $l_s = \lambda x.\top = (\emptyset, \text{all})$, because no fact is about a local.

```text
main:  d1: g = 0
       s1: call p()
p:     if c then
           d2: g = 1
           s2: call p()
       return
```

Phase 1 for `p`. After `d2`, $\varphi = (\{d_2\}, \{d_1\})$, and so at $c_{s2}$. The exit of `p` is the meet of the else branch, $\mathrm{id} = (\emptyset, \emptyset)$, and $\varphi[r_{s2}]$.

| round | $\varphi[r_{s2}] = \varphi[\mathit{exit}_p] \circ \varphi[c_{s2}]$ | $\varphi[\mathit{exit}_p] = \mathrm{id} \sqcap \varphi[r_{s2}]$ |
|---|---|---|
| 0 | $\top = (\emptyset, \text{all})$ | $(\emptyset, \emptyset)$ |
| 1 | $(\emptyset, \emptyset) \circ (\{d_2\}, \{d_1\}) = (\{d_2\}, \{d_1\})$ | $(\{d_2\}, \emptyset)$ |
| 2 | $(\{d_2\}, \emptyset) \circ (\{d_2\}, \{d_1\}) = (\{d_2\}, \{d_1\})$ | $(\{d_2\}, \emptyset)$, stable |

The summary of `p` is $x \mapsto x \cup \{d_2\}$: after a call of `p`, $d_2$ may reach, and nothing is killed for sure, because the call may take the else branch. Phase 2 starts with $X[\mathit{entry}_{main}] = \emptyset$. The call `s1` gives $\varphi[c_{s1}](\emptyset) = \{d_1\}$ at the entry of `p`. The call `s2` then gives $\varphi[c_{s2}](\{d_1\}) = \{d_2\}$, so $X[\mathit{entry}_p] = \{d_1, d_2\}$, and one more round changes nothing. After `s1` in `main`, the summary gives $\{d_1\} \cup \{d_2\} = \{d_1, d_2\}$. Each recursion depth is a different valid path, and the summary covers all of them at once.

## Classic examples

- **Gen-kill problems.** Interprocedural reaching definitions, live variables and available expressions over globals and parameters use (gen, kill) pairs as summaries, as in the walk-through.
- **IFDS.** A distributive function on subsets of a finite set $D$ is fixed by what it does to the empty set and to each single fact. It is a bipartite graph on $D \cup \{0\}$, and composition is the composition of relations. The [IFDS framework](/ifds-framework/) stores the summaries of phase 1 as *path edges* and *summary edges* and finds them by graph reachability.
- **IDE.** For environments that map each fact to a value, such as linear constant propagation, the [IDE framework](/ide-framework/) labels each edge of the IFDS graph with a function on values, such as $\lambda l.\, a l + b$.
- **Side effects.** A [mod-ref](/mod-ref-analysis/) summary is the set of locations that a procedure and its callees may modify or read. It is a gen-only summary, so it is a union over the call graph.
- **Jump functions.** [Interprocedural constant propagation](/interprocedural-constant-propagation/) after Callahan, Cooper, Kennedy and Torczon (1986) summarizes how a procedure passes constants on to its callees. These are partial summaries that trade precision for speed.

## Variations

- **Tabulated summaries.** When functions have no compact form but the lattice is finite, compute $\varphi_q$ only at the inputs that reach $q$. Keep a table from (procedure, input value) to output value, and fill it on demand from the calls. Sharir and Pnueli describe this variant for finite lattices. Padhye and Khedker (2013) call the table entries *value contexts*. It works for any monotone framework of finite height, and it is the input-as-context case on the [context sensitivity](/context-sensitivity/) page.
- **Bottom-up order.** Compute summaries over the [strongly connected components](/strongly-connected-components/) of the call graph, callees first, in reverse [topological order](/topological-sort/). Iterate only inside a component with recursion. This is the usual order of compositional analyzers.
- **Elimination inside a procedure.** Phase 1 inside one procedure is a path problem on functions, so [elimination methods](/elimination-dataflow-methods/) can compute the summaries without iteration on reducible graphs.
- **Pushdown systems.** The program is a [pushdown system](/pushdown-reachability/) and the summaries are weights in a semiring. Reps, Schwoon, Jha and Melski (2005) compute them with saturation of a weighted automaton, and get witness paths too.
- **Summaries for libraries.** A summary written once for a library procedure can stand in for its code, so the analysis of a client does not need the library source.

## Pitfalls

- **The function space is too large.** The space $L \to L$ can be huge even for a small $L$, and constant propagation over all integers has no finite one. Use a restricted class of functions (gen-kill, IFDS relations, IDE micro-functions) or the tabulated variant.
- **Not distributive means not exact.** For full constant propagation, the summary of a procedure with two branches is the meet of two functions, and applying it after the meet loses the relation between values. Lemma 1 still gives soundness, but the result can be below MVP.
- **Locals through the callee.** A summary must not route the caller's local facts through the callee, or the facts of one caller leak into another through the callee's body. The call-to-return function $l_s$ carries them around the call.
- **Starting summaries too low.** Phase 1 must start the summaries at $\lambda x.\top$, not at the identity. A start below the greatest solution still gives a sound result, but a less precise one, since the iteration only goes down.
- **Forgetting to revisit callers.** When the summary of $q$ drops, every call site of $q$ must be processed again (line L8). Without this, recursive procedures and calls processed early keep stale summaries and the result is unsound.

## Exercises

1. Prove the composition and meet formulas for gen-kill pairs used in the walk-through, and show that the height of the space of pairs over $u$ facts is $2u$.
2. In the walk-through, replace the else branch of `p` by `d3: g = 2`. Compute the summary of `p` and the facts at the return point of `s1`.
   <details><summary>Hint</summary>In every run of `p` that returns, the deepest call takes the else branch, and nothing assigns `g` after it. Expect $x \mapsto (x \setminus \{d_1, d_2\}) \cup \{d_3\}$, so only $d_3$ reaches the return point of `s1`.</details>
3. Give a non-distributive example, with constant propagation, where the functional approach returns $\bot$ for a variable that is a constant on every valid path.
4. Show that the tabulated variant for a finite lattice $L$ computes $\varphi_q(v)$ only for inputs $v$ that reach the entry of $q$ on some valid path, and bound its work by the number of such pairs.
5. Show that phase 1 with summaries $\varphi[\mathit{exit}_q]$ started at the identity can stop at a solution strictly below the greatest one. Use a procedure that only calls itself.

## References
