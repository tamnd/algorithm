---
tag: 3YTRA3
kind: technique
slug: supercompilation
name: Supercompilation
aliases:
- Turchin supercompiler
- positive supercompilation
area: compilers-and-program-analysis/optimizations
level: research
summary: Drives a program symbolically on unknown input, folds repeated configurations into recursion and generalizes to stop, giving a residual program.
prereqs: [partial-evaluation, deforestation]
see_also: [futamura-projections, plotkin-lgg, anti-unification-problem, knuth-morris-pratt, termination, binding-time-analysis, ramsey-theorem]
sources:
  - paper: doi:10.1145/5956.5957
    title: Valentin F. Turchin, The concept of a supercompiler, ACM Transactions on Programming Languages and Systems 8(3), 1986, 292-325
    locator: driving of Refal programs on configurations with unknown parts, the graph of states, looping back to an earlier configuration, and generalization
  - paper: doi:10.1017/s0956796800002008
    title: Morten Heine Sørensen, Robert Glück and Neil D. Jones, A positive supercompiler, Journal of Functional Programming 6(6), 1996, 811-838
    locator: driving with positive information for a first-order functional language, folding, the comparison with deforestation and partial evaluation, and the string matcher example
  - paper: doi:10.7551/mitpress/4301.003.0048
    title: Morten Heine Sørensen and Robert Glück, An algorithm of generalization in positive supercompilation, Logic Programming, Proceedings of the 1995 International Symposium (ILPS 1995), MIT Press
    locator: the homeomorphic embedding as the whistle, the most specific generalization, upward generalization and splitting, and the termination proof
  - paper: doi:10.1145/227699.227716
    title: David Sands, Total correctness by local improvement in the transformation of functional programs, ACM Transactions on Programming Languages and Systems 18(2), 1996, 175-234
    locator: the improvement theorem, used to prove that folding in transformations of this kind keeps the meaning of the program
  - paper: doi:10.1090/s0002-9947-1960-0111704-1
    title: "Joseph B. Kruskal, Well-quasi-ordering, the tree theorem, and Vazsonyi's conjecture, Transactions of the American Mathematical Society 95(2), 1960, 210-225"
    locator: the tree theorem, that finite trees are well-quasi-ordered by embedding
  - paper: doi:10.1017/s0305004100003844
    title: C. St. J. A. Nash-Williams, On well-quasi-ordering finite trees, Mathematical Proceedings of the Cambridge Philosophical Society 59(4), 1963, 833-835
    locator: the short proof of the tree theorem by a minimal bad sequence
  - paper: doi:10.1112/plms/s3-2.1.326
    title: Graham Higman, Ordering by divisibility in abstract algebras, Proceedings of the London Mathematical Society s3-2(1), 1952, 326-336
    locator: the well-quasi-ordering of words and of terms of an algebra with finitely many operations of bounded arity under embedding
  - paper: doi:10.1007/3-540-36377-7_17
    title: Michael Leuschel, Homeomorphic embedding for online termination of symbolic methods, The Essence of Computation, LNCS 2566, 2002, 379-403
    locator: the homeomorphic embedding as a whistle in supercompilation, partial deduction and term rewriting, its strength against well-founded orders, and its variants
---

Supercompilation, an idea of Valentin Turchin from the 1970s, transforms a program by running it on input that is partly or wholly unknown. This is *driving*: a call is unfolded, a `case` on a known constructor takes its branch, and a `case` on an unknown variable splits into one branch for each pattern, where the variable is known to match that pattern. The result is a *process tree* of terms. When a term is a renaming of an earlier term on the same path, the path *folds* into a recursive call. When a term grows in a way that may never fold, a *whistle* blows, and the supercompiler replaces terms by more general ones so that the tree stays finite. The residual program is read off the tree. Because driving keeps the outcome of each test, a supercompiler can do what [partial evaluation](/partial-evaluation/) and [deforestation](/deforestation/) do and more: from a naive string matcher and a fixed pattern it makes a matcher that reads each text character once. This page describes positive supercompilation in the form of Sørensen, Glück and Jones, with the homeomorphic embedding as the whistle, and proves that the whistle stops it. The common mistake is to think that the whistle only stops runs that would loop. It blows on finite runs too, and then the supercompiler generalizes and the result is weaker than it could be.

## In plain words

Imagine running a program without knowing its input. When the program tests the input, follow both answers, and remember on each side which answer holds. Each step is written down. When you reach a situation you have already seen, up to the names of the unknowns, you write "go back there" and stop on that side. That makes a loop in the new program.

Some programs never come back to the same situation: a list that the program builds keeps getting longer. So we watch for a situation that contains an earlier one inside it, as a smaller copy. When that happens, we forget the parts that differ and treat them as unknown. Now the situations do repeat.

The written record is a new program. It does the same job, but the tests and the data that were decided while driving are gone.

## When it applies

- The program is functional and first-order, with algebraic data types, as in the template. Supercompilers also exist for Refal, Turchin's language, for higher-order functional languages, and for logic programs, where the same method is called partial deduction.
- Part of the input is known and part is not, as in partial evaluation, or the program is a composition of stages, as in deforestation, or both.
- The program tests its unknown input, and later work depends on what those tests found. This is where positive information pays off.
- The time to supercompile, and the size of the residual program, are acceptable. Driving with full splitting can make a residual program much larger than the source.

## The template

**Language.** As for deforestation: a program is a list of equations $f(\bar x) = b$, and a term is a variable, $c(\bar t)$, $f(\bar t)$ or $\mathtt{case}\ t_0\ \mathtt{of}\ p_1 \to u_1 \mid \cdots \mid p_k \to u_k$ with flat patterns. The meaning is call by name. The residual program may also use $\mathtt{let}\ \bar z = \bar t\ \mathtt{in}\ g$, which means $g[\bar t / \bar z]$. Every term is written as $E[r]$ with a case context $E$ and a redex $r$, which is a variable, a constructor term or a call.

**Trivial and non-trivial terms.** A term is *trivial* if it is a variable, a constructor term $c(\bar t)$ with an empty context, or a `let`. Every other term is *non-trivial*, and its *kind* is that of its redex: var, con or call.

**Driving.** One step of driving gives the children of a term:

- trivial: a variable has none; $c(\bar t)$ has the children $t_1, \ldots, t_n$; $\mathtt{let}\ \bar z = \bar t\ \mathtt{in}\ g$ has the children $t_1, \ldots, t_n$ and $g$.
- kind var, $E[\mathtt{case}\ x\ \mathtt{of}\ p_i \to u_i]$: one child for each branch, $E[u_i]$ with $x$ replaced by $p_i$ everywhere. This replacement is the *positive information*.
- kind con, $E[\mathtt{case}\ c(\bar t)\ \mathtt{of} \ldots c(\bar y) \to u \ldots]$: the child $E[u[\bar t / \bar y]]$.
- kind call, $E[f(\bar t)]$ with $f(\bar x) = b$: the child $E[b[\bar t / \bar x]]$.

**Homeomorphic embedding.** All variables count as one symbol. The relation $s \trianglelefteq t$ holds if one of these holds:

- *variables*: $s$ and $t$ are both variables;
- *diving*: $t = h(t_1, \ldots, t_n)$ and $s \trianglelefteq t_i$ for some $i$;
- *coupling*: $s = h(s_1, \ldots, s_n)$, $t = h(t_1, \ldots, t_n)$ with the same symbol, and $s_i \trianglelefteq t_i$ for every $i$.

Here a `case` is a symbol whose name is the list of its patterns, and whose arguments are the selector and the branches. So $s \trianglelefteq t$ means that $s$ is $t$ with some parts cut out. For example, $\mathit{rev}(u, \mathit{Nil}) \trianglelefteq \mathit{rev}(r, \mathit{Cons}(x, \mathit{Nil}))$, by coupling, with $u \trianglelefteq r$ for the variables and $\mathit{Nil} \trianglelefteq \mathit{Cons}(x, \mathit{Nil})$ by diving.

**Generalization.** A term $g$ is a *generalization* of $s$ if $s = g\theta$ for a substitution $\theta$. The *most specific generalization* $\mathrm{msg}(s, t)$ is a common generalization $g$, with $g\theta_1 = s$ and $g\theta_2 = t$, of which every other common generalization is a generalization. It is computed by [anti-unification](/anti-unification-problem/): walk $s$ and $t$ together, keep the common symbols, and put one variable for each pair of different subterms, the same variable for the same pair. This is [Plotkin's least general generalization](/plotkin-lgg/). For the two terms above it is $\mathit{rev}(v, w)$.

**The algorithm.** Start with a tree of one node, labelled with the start term. Repeat until every leaf is done. Take a leaf $\beta$ that is not done, with term $t$.

1. If $t$ is trivial, drive it.
2. *Fold.* If a non-trivial ancestor $\alpha$ has a term $t_\alpha$ of which $t$ is a renaming, $\beta$ is done: it calls $\alpha$.
3. *Whistle.* If a non-trivial ancestor $\alpha$ of the same kind has $t_\alpha \trianglelefteq t$, take the nearest one, and:
   a. if $t = t_\alpha\theta$, relabel $\beta$ with $\mathtt{let}\ \bar z = \theta(\bar z)\ \mathtt{in}\ t_\alpha$, where $\bar z$ are the free variables of $t_\alpha$ (the body then folds by step 2);
   b. else, if $g = \mathrm{msg}(t_\alpha, t)$ is not a variable, delete the subtree below $\alpha$ and relabel $\alpha$ with $\mathtt{let}\ \bar z = \theta_1(\bar z)\ \mathtt{in}\ g$ (*upward generalization*);
   c. else *split* $t$: if $t = f(\bar t)$, relabel $\beta$ with a `let` that names the arguments that are not variables; if $t = \mathtt{case}\ t_0 \ldots$ with $t_0$ not a variable, name $t_0$ by a `let`; if $t = \mathtt{case}\ x\ \mathtt{of}\ p_i \to u_i$, give $\beta$ the children $u_i$, without positive information. In each case $\beta$ becomes a trivial node.
4. Else drive $t$.

The residual program has one function $h_\alpha(\bar z) $ for each node $\alpha$ that some fold calls, with $\bar z$ the free variables of $t_\alpha$. Its body is read off the subtree of $\alpha$: a var node becomes a `case` on that variable, a con node and a call node become their child, a trivial node becomes the constructor or `let` that it is, and a fold becomes a call of $h_\alpha$.

**Legality.** *Each step of driving, folding and generalization replaces a term by an equal one in call by name, so if the residual program gives a value, the source gives the same value; and a source run that gives a value is matched by a residual run.* The first half is the least solution argument of [deforestation](/deforestation/): the meanings of the terms $t_\alpha$ satisfy the residual equations. The positive information is sound because, in the branch for $p_i$, the value of $x$ does match $p_i$. A `let` from steps 3a, 3b and 3c is a substitution, so it is an equation too. For the second half, every fold is reached after at least one call step on its path, and the induction on the number of call steps of deforestation goes through. Sands (1996) proves total correctness for transformations of this kind in general.

**Profit.** Every test that the driving decides, every constructor that a `case` takes apart at once, and every call that is unfolded, is gone from the residual program. In a var node, the residual program tests the variable once, and positive information makes every later test of the same value in that branch a con node, which is decided. This is how the string matcher below reads each text character only once. Generalization gives some of this back: a part of a term that the whistle forgets is computed at run time again.

**Termination.** *Theorem. For a finite program and any start term, the algorithm stops.* The proof needs an order theorem.

A *quasi-order* $\le$ on a set is reflexive and transitive. It is a *well-quasi-order* (wqo) if every infinite sequence $a_1, a_2, \ldots$ has indices $i < j$ with $a_i \le a_j$. A sequence with no such pair is *bad*.

*Theorem (Higman 1952, Kruskal 1960). For a finite set of symbols, each with a fixed number of arguments, $\trianglelefteq$ is a wqo on the finite terms over these symbols and variables.*

*Lemma 1. $\trianglelefteq$ is a quasi-order.* Reflexivity is coupling on every node, or the variable rule. For transitivity, let $s \trianglelefteq t \trianglelefteq u$; we show $s \trianglelefteq u$ by induction on the size of $u$. If $t \trianglelefteq u$ by diving, $t \trianglelefteq u_i$, so $s \trianglelefteq u_i$ by induction and $s \trianglelefteq u$ by diving. If both are variables, $s$ is a variable too, since nothing else embeds in a variable. If by coupling, $t = h(\bar t)$ and $u = h(\bar u)$ with $t_i \trianglelefteq u_i$: when $s \trianglelefteq t_i$ by diving, $s \trianglelefteq u_i$ by induction, and then $s \trianglelefteq u$; when $s = h(\bar s)$ by coupling, $s_i \trianglelefteq u_i$ for every $i$ by induction, and then $s \trianglelefteq u$. $\square$

*Lemma 2. In a wqo, every infinite sequence has an infinite subsequence $a_{i_1} \le a_{i_2} \le \cdots$.* Call $i$ *terminal* if no $j > i$ has $a_i \le a_j$. The terminal indices form a bad subsequence, so there are finitely many. After the last one, every index $i$ has a later $j$ with $a_i \le a_j$; start after the last terminal index and follow such steps. By transitivity, each element is below all later ones. $\square$

*Lemma 3. If $\le_1, \ldots, \le_n$ are wqos on $A_1, \ldots, A_n$, the order on $A_1 \times \cdots \times A_n$ that compares each component is a wqo.* For $n = 2$: given pairs $(a_i, b_i)$, Lemma 2 gives a subsequence on which the $a$ do not go down, and since $\le_2$ is a wqo, two of its $b$ are in order, $b_i \le_2 b_j$ with $i < j$. Then $(a_i, b_i) \le (a_j, b_j)$. Larger $n$ follow by induction. $\square$

*Proof of the theorem* (Nash-Williams 1963). Suppose there is a bad sequence. Choose $t_1$ of least size such that some bad sequence starts with $t_1$; then $t_2$ of least size such that some bad sequence starts with $t_1, t_2$; and so on. Every finite part $t_1, \ldots, t_k$ starts a bad sequence, so the whole sequence $(t_i)$ is bad. Let $S$ be the set of all arguments of all the $t_i$. *$S$ is wqo:* suppose $s_1, s_2, \ldots$ is bad in $S$, with $s_k$ an argument of $t_{f(k)}$. Each $t_i$ has finitely many arguments, so we may pass to a subsequence with $f(1) < f(2) < \cdots$. The sequence $t_1, \ldots, t_{f(1) - 1}, s_1, s_2, \ldots$ is bad: two $t$ are not in order since $(t_i)$ is bad; $t_i \trianglelefteq s_k$ would give $t_i \trianglelefteq t_{f(k)}$ by diving, with $i < f(1) \le f(k)$; and two $s$ are not in order by choice. But $s_1$ is smaller than $t_{f(1)}$, which breaks the choice of $t_{f(1)}$. So $S$ is wqo. Now at most one $t_i$ is a variable, since two variables are in order. There are finitely many symbols, so infinitely many $t_i$ have the same top symbol $h$ with $n$ arguments. Their lists of arguments are in $S^n$, which is wqo by Lemma 3, so two of them, $t_i$ and $t_j$ with $i < j$, have $s_m \trianglelefteq s'_m$ for every argument; by coupling, $t_i \trianglelefteq t_j$. This contradicts badness. $\square$

The whistle compares only terms of the same kind. The relation "$s \trianglelefteq t$ and $s$, $t$ have the same kind" is the product order of $\trianglelefteq$ with equality on the three kinds, and equality on a finite set is a wqo, so by Lemma 3 it is a wqo too.

*Proof of termination.* The non-trivial terms that the algorithm meets are built from the function names, the constructors and the `case` pattern lists of the program, which are finite in number, so the theorem applies to them. (i) Every node has finitely many children. (ii) A non-trivial node changes its label at most once, in step 3a, 3b as the node $\alpha$, or 3c, and then it is trivial. A trivial node never changes, and it is never an $\alpha$ in step 3b. A node is deleted only when an ancestor changes. (iii) So, by induction on the depth $d$, there is a time after which no node of depth at most $d$ changes or is deleted: the root changes at most once, and once the nodes of depth $d$ are fixed, each of their finitely many children changes at most once more. (iv) Suppose that the algorithm does not stop. The fixed nodes form a *limit tree*. It is infinite: if it had depth $D$, then after the nodes of depth $D + 1$ are fixed, there are none of them, and all later steps act on fixed nodes, so there are only finitely many. (v) By König's lemma, a tree that is infinite and finitely branching has an infinite path. (vi) On this path, the children of a trivial node are smaller than it: the arguments of a constructor, the parts of a `let`, the branches of a split `case`, and the body of a `let` made by a split, which names at least one argument that is not a variable. So the path has infinitely many non-trivial nodes $n_1, n_2, \ldots$, in order of depth. Each of them is driven, not folded and not relabelled, since it is fixed and has children. When $n_j$ was driven for the last time, its ancestors had their final labels, and the whistle did not blow; so no $n_i$ with $i < j$ and the same kind has $t_{n_i} \trianglelefteq t_{n_j}$. The terms $t_{n_1}, t_{n_2}, \ldots$ form a bad sequence for the wqo above, which is impossible. $\square$

## Classic examples

The examples come from a short script that implements the algorithm above and an evaluator that counts the calls, the `case` steps and the cases on text characters. Every residual program was checked against the source; the inputs are stated with each example.

**A string matcher.** The naive matcher tests whether a pattern occurs in a text over the letters `A` and `B`. It compares the pattern with the text, and after a mismatch it starts again one place to the right:

```
loop(pp, ss, op, os) = case pp of
    Nil -> True
  | Cons(p, pr) -> case ss of
        Nil -> False
      | Cons(s, sr) -> case eq(p, s) of True -> loop(pr, sr, op, os)
                                      | False -> next(op, os)
next(op, os) = case os of Nil -> False | Cons(s, sr) -> loop(op, sr, op, sr)
```

Here `eq` compares two letters by two `case` steps. Driving `loop(AAB, u, AAB, u)`, with the pattern `AAB` known and the text `u` unknown, by steps 1, 2 and 4 only (driving and folding, as in Sørensen, Glück and Jones), gives this program, with names chosen for reading:

```
m0(u) = case u of Nil -> False
          | Cons(s, r) -> case s of
                B -> m0(r)
              | A -> case r of Nil -> False
                       | Cons(s2, r2) -> case s2 of A -> m2(r2) | B -> m0(r2)
m2(r) = case r of Nil -> False
          | Cons(s, r2) -> case s of A -> m2(r2) | B -> True
```

This is the automaton of [Knuth, Morris and Pratt](/knuth-morris-pratt/) for `AAB`: `m0` has matched nothing, the inner `case` has matched `A`, and `m2` has matched `AA`, where a further `A` keeps the state. Each text character is tested once. The positive information is what makes it work. After a mismatch, the source restarts on `os`, but `os` is now known to start with the letters that were read, so the restart is driven over known letters, and those tests are decided. Without positive information, as in deforestation or partial evaluation, the result tests the same characters again. On the text `AAAAAAAAAB`, the source does 56 calls, 128 case steps and 24 tests of a text character; the residual program does 9 calls, 20 case steps and 10 tests. On `AAAAAAAAAA` the counts are 61, 140 and 26 against 10, 21 and 10. The two programs agree on 1000 random texts of length 0 to 12, from a generator with seed 7.

**Reverse with an accumulator.** `rev(xs, acc) = case xs of Nil -> acc | Cons(x, r) -> rev(r, Cons(x, acc))`, from `rev(u, Nil)`. Driving gives the var node `case u of ...`, and in its `Cons` branch the call node `rev(r, Cons(x, Nil))`. The ancestor `rev(u, Nil)` embeds in it, as shown above, and the new term is not an instance of it, since `Nil` is not a variable. So step 3b fires: $\mathrm{msg} = \mathit{rev}(v, w)$, and the root becomes `let v = u, w = Nil in rev(v, w)`. Driving `rev(v, w)` gives `rev(r, Cons(x, w))`, which is an instance of `rev(v, w)` (step 3a), and then a fold. The residual program is `h(v, w) = case v of Nil -> w | Cons(x, r) -> h(r, Cons(x, w))` with the start `h(u, Nil)`, which is the source again: the whistle saved termination and lost nothing, since there was nothing to gain. Deforestation does not stop on this term.

**Deforestation as a special case.** From `app(app(a, b), c)` the algorithm gives

```
h(a, b, c) = case a of Nil -> app2(b, c) | Cons(x, r) -> Cons(x, h(r, b, c))
```

where `app2` is `app` again. This is the one-pass program of deforestation, with no intermediate list. The whistle does not blow.

## Variations

- **Turchin's supercompiler.** Turchin drove Refal programs, whose data are strings with patterns, and kept a graph of configurations. He used generalization and checked for repeated configurations by his own methods; the homeomorphic embedding came later, from the work on termination of term rewriting.
- **Perfect supercompilation.** Positive supercompilation keeps only what a test says in its true direction: $x$ matches $p_i$. A *perfect* supercompiler also keeps negative information, such as $x \ne A$ in the else branch of a test on letters, and can then decide more tests.
- **Higher-order supercompilation.** Supercompilers for languages with `fun x -> e` add rules for a call of an unknown function and for a known lambda, and need care with sharing. Supercompilers of this kind have been built for Haskell.
- **Distillation.** Hamilton's distillation compares and folds whole process trees, not only terms, and can make programs asymptotically faster, which positive supercompilation cannot.
- **Other whistles.** Leuschel (2002) compares the homeomorphic embedding with well-founded orders. Some systems use a bound on the depth or on the size of terms instead, which is simpler and cruder.
- **Partial deduction.** The same scheme for logic programs, with unfolding of atoms, is partial deduction. The embedding was used there for termination as well.

## Pitfalls

- **The whistle blows too early.** In the string matcher, after the text gave `AA`, driving reaches the call node `loop([B], r, AAB, Cons(A, Cons(A, r)))`. After a third `A` and a restart, it reaches `loop(AAB, Cons(A, Cons(A, r2)), AAB, Cons(A, Cons(A, r2)))`. The first embeds in the second: `[B]` embeds in `AAB` by diving, and a variable embeds in any term. With the whistle on (step 3 included), the script generalizes the pattern position, and the residual program tests pattern letters at run time: on `AAAAAAAAAB` it does 57 case steps against 20 without the whistle and 128 for the source. It is still correct. Real supercompilers refine the whistle, for example by comparing only terms with the same redex or by ignoring some positions.
- **Comparing terms of different kinds.** If the whistle also compares a call node with a var node, it blows on `app(app(a, b), c)`. The script, with that change, generalizes the inner call to `let g = app(a, b) in app(g, c)` and gives two separate `app` functions with the intermediate list, which is no fusion at all. Comparing only terms of the same kind keeps the order a wqo and avoids this case.
- **Termination is not speed.** The theorem gives no bound on the size of the tree. Driving that splits on many variables can make a residual program exponentially larger than the source.
- **Strict languages.** The steps are equations of call by name. In a strict language, unfolding can drop an argument that does not stop, and a `let` must keep the order of effects.
- **Lost sharing.** Unfolding `dup(g(y))` with `dup(x) = Pair(x, x)` copies the call `g(y)`. A supercompiler for a lazy language with sharing must bind such arguments with a `let` instead.
- **No laws.** Like deforestation, supercompilation does not prove algebraic laws. `flip(flip(t))` for a tree mirror `flip` becomes a copy function, not $t$.

## Exercises

1. Drive `loop(AB, u, AB, u)` by hand, with driving and folding only, and give the residual matcher. How many functions does it have?
2. Show that the sequence of terms $f(\mathit{Nil}), f(\mathit{Cons}(x_1, \mathit{Nil})), f(\mathit{Cons}(x_2, \mathit{Cons}(x_1, \mathit{Nil}))), \ldots$ is not bad, and find the first pair $i < j$ with $t_i \trianglelefteq t_j$.
3. Give an infinite bad sequence for $\trianglelefteq$ when there are infinitely many constructors, which shows that finiteness of the set of symbols is needed.
4. Compute $\mathrm{msg}(f(x, x), f(A, B))$ and $\mathrm{msg}(\mathit{Cons}(A, \mathit{Nil}), \mathit{Cons}(B, \mathit{Nil}))$, with the substitutions $\theta_1$ and $\theta_2$.
5. Without positive information, drive `loop(AAB, u, AAB, u)` with folding. Which tests of the text are done twice in the residual program?

## References
