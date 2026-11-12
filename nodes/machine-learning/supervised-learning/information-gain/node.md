---
tag: 4FPWB7
kind: concept
slug: information-gain
name: Information gain
aliases:
- entropy reduction of a split
- ID3 gain criterion
area: machine-learning/supervised-learning
level: intro
summary: "The drop in label entropy from splitting a set of examples: IG = H(Y) - H(Y | split). ID3 and C4.5 choose the split of largest gain or gain ratio."
prereqs: [shannon-entropy, conditional-entropy]
see_also: [gini-impurity, id3, c4-5, decision-tree-learning, binary-entropy-function, normalized-mutual-information, feature-selection]
sources:
  - paper: doi:10.1007/BF00116251
    title: J. R. Quinlan, Induction of decision trees, Machine Learning 1(1), 1986
    locator: pages 81 to 106, Table 1 (the 14 Saturday mornings), Section 4 (the information-based selection of an attribute, with gain(outlook) = 0.246 bits) and Section 7 (the bias toward attributes with many values and the gain ratio)
  - book: isbn:9780070428072
    title: Tom M. Mitchell, Machine Learning, McGraw-Hill, 1997
    locator: Chapter 3, Section 3.4.1 (entropy and information gain, Table 3.2 PlayTennis), Section 3.7.2 (thresholds on continuous attributes) and Section 3.7.3 (gain ratio)
  - book: isbn:9781558602380
    title: J. Ross Quinlan, C4.5, Programs for Machine Learning, Morgan Kaufmann, 1993
    locator: Chapter 2 (the gain criterion, the gain ratio criterion and the restriction to tests of at least average gain)
  - paper: "Usama M. Fayyad and Keki B. Irani, On the handling of continuous-valued attributes in decision tree generation, Machine Learning 8(1), 1992"
    locator: pages 87 to 102 (the best threshold for the entropy criterion lies at a boundary point between classes)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 2 (Sections 2.2 to 2.6, conditional entropy, mutual information, Jensen's inequality and the fact that conditioning reduces entropy)
---

Information gain is the drop in the [entropy](/shannon-entropy/) of the class labels when a set of examples is split into parts: $IG = H(Y) - H(Y \mid \text{split})$, where the second term is the [conditional entropy](/conditional-entropy/), the size-weighted mean entropy of the parts. It equals the mutual information between the label and the outcome of the split, under the empirical distribution of the examples. [ID3](/id3/) chooses at each node the attribute of largest gain; because the gain favours attributes with many values, [C4.5](/c4-5/) divides it by the entropy of the split and uses the gain ratio.

## In plain words

Entropy measures how mixed a set of labels is. A set where every example has the same label has entropy zero. A set with half yes and half no has entropy one bit, the most for two labels.

When you split the examples by a question, each part has its own entropy. Weigh each part by its share of the examples and add them up. Information gain is the entropy before the split minus this weighted entropy after it. It says how much the answer to the question tells you about the label.

A tree learner asks the question with the largest gain first. The gain has a known bias: a question with many possible answers, such as an identity number, cuts the data into tiny pure parts and gets the largest gain while it predicts nothing for new data.

## The idea

**Setting and notation.** A node holds a sample $S$ of $n$ examples $(x_i, y_i)$ with labels in $k$ classes. Let $p_c = |\{i : y_i = c\}| / n$. The entropy of the labels, in bits, is

$$ H(S) = -\sum_{c=1}^{k} p_c \log_2 p_c, $$

with $0 \log_2 0 = 0$. A *split* $A$ is any rule that sends each example to one of $r$ branches: the value of a categorical attribute, or the outcome of a test $x_j \le \theta$. It partitions $S$ into $S_1, \ldots, S_r$. The **information gain** of $A$ is

$$ IG(S, A) = H(S) - \sum_{v=1}^{r} \frac{|S_v|}{|S|} H(S_v) = H(Y) - H(Y \mid A), $$

where $Y$ and $A$ are the label and the branch of an example drawn uniformly from $S$. So $IG(S, A)$ is the mutual information $I(Y; A)$ of the empirical distribution. With natural logarithms the unit is the nat, and $1$ nat $= 1/\ln 2 \approx 1.4427$ bits.

**Basic facts.** Write $w_v = |S_v|/|S|$ and $p^{(v)}$ for the label distribution of $S_v$, so the parent distribution is $p = \sum_v w_v p^{(v)}$.

1. **Non-negative.** $IG(S, A) \ge 0$, with equality if and only if every nonempty branch has the same label distribution as $S$. *Proof.* $H$ is a strictly concave function of the distribution, since $-t \log t$ is strictly concave on $[0, 1]$. By Jensen's inequality, $H(p) = H(\sum_v w_v p^{(v)}) \ge \sum_v w_v H(p^{(v)})$, with equality if and only if all $p^{(v)}$ with $w_v > 0$ are equal. $\square$
2. **Bounded.** $IG(S, A) \le H(S) \le \log_2 k$, with $IG = H(S)$ if and only if every branch is pure. Also $IG(S, A) = I(Y; A) \le H(A) \le \log_2 r$.
3. **Refinement never lowers the gain.** If the split $A'$ refines $A$ (each branch of $A'$ lies inside one branch of $A$), then $IG(S, A') \ge IG(S, A)$. *Proof.* Apply fact 1 inside each branch $S_v$ of $A$ to the sub-split that $A'$ makes of it: the weighted entropy of the sub-branches is at most $H(S_v)$. Summing with the weights $w_v$ gives $H(Y \mid A') \le H(Y \mid A)$. $\square$
4. **A divergence form.** $IG(S, A) = \sum_v w_v\, D(p^{(v)} \,\|\, p)$, the weighted Kullback-Leibler divergence of each branch from the parent. This is the identity $I(Y; A) = \sum_a \Pr[A = a]\, D(P_{Y \mid A = a} \,\|\, P_Y)$ (Cover and Thomas, Chapter 2).

**The bias toward many-valued attributes.** Fact 3 is the problem. An attribute with a distinct value for each example, such as a record number, refines every other split, so its gain is $H(S)$, the largest possible, and the tree it gives has one example per leaf and no use on new data. Even without such an extreme, attributes with more values get larger gains by chance. Quinlan (1986, Section 7; 1993, Chapter 2) corrects this with the **split information** and the **gain ratio**:

$$ SI(S, A) = -\sum_{v=1}^{r} \frac{|S_v|}{|S|} \log_2 \frac{|S_v|}{|S|} = H(A), \qquad GR(S, A) = \frac{IG(S, A)}{SI(S, A)}. $$

The split information is the entropy of the branch sizes, which is large for many small branches. The ratio is unstable when $SI$ is near zero, that is when almost all examples go to one branch, so C4.5 maximizes the gain ratio only among the attributes whose gain is at least the average gain of the attributes it examined.

**Sampling bias.** The gain is computed on the sample, and it is positive by chance even when $Y$ and $A$ are independent. Under independence, $2 n \ln 2 \cdot IG(S, A)$ (the $G$ statistic, with $IG$ in bits) is asymptotically $\chi^2$ with $(r - 1)(k - 1)$ degrees of freedom. So the expected chance gain grows with the number of branches $r$, which is the statistical side of the same bias.

## Examples

**PlayTennis (Quinlan 1986, Table 1; Mitchell 1997, Table 3.2).** The 14 days have 9 positive and 5 negative labels, so $H(S) = H(9/14) = 0.940$ bits. The attribute outlook splits them into sunny (2 positive, 3 negative), overcast (4, 0) and rain (3, 2):

$$ IG(S, \text{outlook}) = 0.9403 - \left(\tfrac{5}{14} \cdot 0.9710 + \tfrac{4}{14} \cdot 0 + \tfrac{5}{14} \cdot 0.9710\right) = 0.9403 - 0.6935 = 0.2467 \text{ bits}. $$

| attribute | branches | $H(Y \mid A)$ | $IG$ | value printed by Quinlan and Mitchell | $SI$ | $GR$ |
|---|---|---|---|---|---|---|
| outlook | 3 | 0.6935 | 0.2467 | 0.246 | 1.5774 | 0.1564 |
| temperature | 3 | 0.9111 | 0.0292 | 0.029 | 1.5567 | 0.0188 |
| humidity | 2 | 0.7885 | 0.1518 | 0.151 | 1.0000 | 0.1518 |
| windy | 2 | 0.8922 | 0.0481 | 0.048 | 0.9852 | 0.0488 |

Outlook has the largest gain, so ID3 puts it at the root. The sources print 0.246 and 0.151 because they subtract the rounded values: $0.940 - 0.694 = 0.246$ and $0.940 - 0.789 = 0.151$. Rounded from the exact values the gains are 0.247 and 0.152; the choice of the root is the same.

**A record number.** Add the day number (1 to 14) as an attribute. Each branch holds one day, so $H(Y \mid \text{day}) = 0$ and $IG = 0.9403$, larger than any real attribute. Its split information is $\log_2 14 = 3.8074$, so its gain ratio is $0.2470$, which is still larger than the 0.1564 of outlook. The gain ratio alone does not stop this attribute; C4.5 also requires that at least two branches of a test hold at least two examples, which the day number fails.

**A numeric threshold (Mitchell 1997, Section 3.7.2).** Temperatures 40, 48, 60, 72, 80, 90 have labels no, no, yes, yes, yes, no. The test $x \le 54$ has gain $0.4591$ bits, and $x \le 85$ has gain $0.1909$. Tests between two examples of the same label, such as $x \le 66$ with gain $0.0817$, cannot be better than the best test at a boundary between labels, a result of Fayyad and Irani (1992).

**No gain, yet a perfect split pair.** Take the four points of $\{0, 1\}^2$ with label $y = x_1 \oplus x_2$. Each single feature splits the labels into two branches with one 0 and one 1 each, so both gains are 0, though the two features together give the label exactly. A greedy learner that stops when the best gain is 0 makes no split here.

**Binary labels.** With two classes and a fraction $q$ of positives, $H = h(q) = -q \log_2 q - (1 - q) \log_2(1 - q)$, the [binary entropy function](/binary-entropy-function/). It is 0 at $q \in \{0, 1\}$ and 1 at $q = 1/2$.

## Where it is used

- [ID3](/id3/) chooses each test by information gain; [C4.5](/c4-5/) uses the gain ratio with the average-gain filter, and the gain to choose a threshold on a numeric attribute. [Decision tree learning](/decision-tree-learning/) in general uses an impurity measure, and the entropy is one choice; the [Gini impurity](/gini-impurity/) of CART is the other common one.
- In [feature selection](/feature-selection/), features are ranked by their mutual information with the label, which is the information gain of the split by the feature value.
- In clustering evaluation, the [normalized mutual information](/normalized-mutual-information/) is the same quantity between two partitions, scaled to $[0, 1]$.
- The quantity is the mutual information of information theory; the [conditional entropy](/conditional-entropy/) page gives the general definitions and the chain rule.

## References
