---
title: Skew heap operations take O(log n) amortized time
proves: [time.amortized]
status: full
---

We prove that each merge of a top-down skew heap costs at most $2\lfloor \lg n_1 \rfloor + 2\lfloor \lg n_2 \rfloor + 4$ amortized units, where $n_1$ and $n_2$ are the sizes of its inputs. This is $O(\log n)$ for insert, delete-min and meld. The argument is Sleator and Tarjan's.

**Cost.** The actual cost of a merge is the number of calls of MERGE that reach line L2, which is the number of nodes on the *merge path*: the nodes whose children are swapped. All other work is $O(1)$ per call or per operation.

**Potential.** For a node $x$, let $s(x)$ be the number of nodes in its subtree. Call $x$ *heavy* if $s(x.right) > s(x.left)$, and *light* otherwise, with $s(\mathrm{NIL}) = 0$. Let $\Phi$ be the number of heavy nodes in all heaps. Then $\Phi \ge 0$, and $\Phi = 0$ when there are no nodes.

**Lemma 1.** On the right path of a tree with $m \ge 1$ nodes, at most $\lfloor \lg m \rfloor + 1$ nodes are light.

*Proof.* If $x$ is light, then $s(x.right) \le s(x.left)$ and $s(x.right) + s(x.left) = s(x) - 1$, so $s(x.right) \le (s(x) - 1)/2 < s(x)/2$. Along the right path, sizes never grow, and they fall below half at each light node. If the light nodes are $x_1, \dots, x_q$ from the top, then $1 \le s(x_q) < m/2^{q-1}$, so $2^{q-1} < m$ and $q - 1 \le \lfloor \lg m \rfloor$ when $m$ is not a power of 2, or $q - 1 \le \lg m - 1$ when it is. In both cases $q \le \lfloor \lg m \rfloor + 1$. $\square$

**Lemma 2.** In one merge, every heavy node on the merge path becomes light, and no node off the merge path changes its type.

*Proof.* The merge path consists of nodes of the right paths of the two inputs. A node off the merge path keeps both of its subtrees as they were, because MERGE only changes the fields of the nodes on its path, and returns other subtrees unchanged. So its type does not change.

Let $x$ be on the merge path, with old subtrees $L$ (left) and $R$ (right). After the merge, its right subtree is $L$ and its left subtree is the result of merging $R$ with another tree, which has at least $|R|$ nodes. If $x$ was heavy, then $|R| > |L|$, so now $s(x.left) \ge |R| > |L| = s(x.right)$, and $x$ is light. $\square$

**Theorem.** A merge of heaps with $n_1$ and $n_2$ nodes has amortized cost at most $2\lfloor \lg n_1 \rfloor + 2\lfloor \lg n_2 \rfloor + 4$, with $\lg 0$ read as $-1$ when a heap is empty.

*Proof.* Let the merge path have $h$ heavy and $\ell$ light nodes, measured before the merge. The actual cost is $h + \ell$. By Lemma 2, the $h$ heavy nodes become light, at most the $\ell$ light nodes become heavy, and no other node changes, so $\Delta\Phi \le \ell - h$. The amortized cost is at most $h + \ell + \ell - h = 2\ell$. The merge path is part of the right paths of the two inputs, so by Lemma 1, $\ell \le \lfloor \lg n_1 \rfloor + 1 + \lfloor \lg n_2 \rfloor + 1$. $\square$

**The operations.** Insert merges with a one-node heap, so its amortized cost is at most $2\lfloor \lg n \rfloor + 4$. Delete-min removes the root; this can only remove a heavy node, and the subtrees of all other nodes are unchanged, so $\Phi$ does not grow. It then merges two heaps of total size $n - 1$, at amortized cost at most $4 \lg n + 4$. Meld of heaps of sizes $n_1$ and $n_2$ costs at most $2 \lg n_1 + 2 \lg n_2 + 4 \le 4 \lg n + 4$.

Since $\Phi$ starts at $0$ and is never negative, the actual cost of any sequence of $m$ operations starting from empty heaps is at most the sum of the amortized costs, which is $O(m \log n)$ for $n$ the largest heap size. $\blacksquare$
