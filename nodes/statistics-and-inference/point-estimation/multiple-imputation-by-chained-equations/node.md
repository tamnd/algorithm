---
tag: XHM517
kind: algorithm
slug: multiple-imputation-by-chained-equations
name: Multiple imputation by chained equations
aliases:
- MICE
- fully conditional specification
area: statistics-and-inference/point-estimation
level: advanced
summary: Fills each incomplete column in turn with draws from a regression on the other columns, repeats the cycle, and returns m completed tables for Rubin's rules.
model: real-ram
complexity:
  vars: {n: the number of rows, p: the number of columns, q: the number of incomplete columns, m: the number of imputations, T: the number of sweeps}
  time: {worst: "O(m T q (n p^2 + p^3))"}
  space: {extra: "O(m n p)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1999
  people: [S. van Buuren, H. C. Boshuizen, D. L. Knook]
  note: Van Buuren, Boshuizen and Knook (1999) imputed missing blood pressure covariates by cycling through one regression model per variable. Raghunathan and coauthors (2001) gave the same scheme as sequential regression imputation. Van Buuren and coauthors (2006) named it fully conditional specification and studied when it has a joint model behind it.
prereqs: [missing-data-mechanism, gibbs-sampling, multiple-imputation]
see_also: [ordinary-least-squares, bayesian-linear-regression, posterior-predictive-distribution, expectation-maximization, logistic-regression, k-nearest-neighbors, inverse-probability-weighting, ignorability]
sources:
  - paper: doi:10.18637/jss.v045.i03
    title: S. van Buuren and K. Groothuis-Oudshoorn, mice, Multivariate imputation by chained equations in R, Journal of Statistical Software 45(3), 2011
    locator: pages 1 to 67 (the algorithm, the univariate imputation methods including predictive mean matching, passive imputation, predictor selection and convergence checks)
  - paper: doi:10.1080/10629360600810434
    title: S. van Buuren, J. P. L. Brand, C. G. M. Groothuis-Oudshoorn and D. B. Rubin, Fully conditional specification in multivariate imputation, Journal of Statistical Computation and Simulation 76(12), 2006
    locator: pages 1049 to 1064 (compatible and incompatible conditional models, and simulations of their effect)
  - paper: "S. van Buuren, H. C. Boshuizen and D. L. Knook, Multiple imputation of missing blood pressure covariates in survival analysis, Statistics in Medicine 18(6), 1999"
    locator: pages 681 to 694 (the chained regression imputation of the covariates)
  - paper: "T. E. Raghunathan, J. M. Lepkowski, J. Van Hoewyk and P. Solenberger, A multivariate technique for multiply imputing missing values using a sequence of regression models, Survey Methodology 27(1), 2001"
    locator: pages 85 to 95 (sequential regression multivariate imputation)
  - book: isbn:9781138588318
    title: S. van Buuren, Flexible Imputation of Missing Data, second edition, CRC Press, 2018
    locator: Chapter 3 (univariate imputation, Bayesian regression draws and predictive mean matching) and Chapter 4 (multivariate missing data and fully conditional specification)
---

Multiple imputation by chained equations (MICE) makes the $m$ completed data sets that [multiple imputation](/multiple-imputation/) needs when more than one column of a table has missing values. It does not specify one joint model for all columns. It specifies one conditional model for each incomplete column, usually a regression on all the other columns, and it imputes the columns one at a time in a cycle. Each step draws the parameters of the regression from their posterior and then draws the missing values from the fitted model, so the imputations carry the uncertainty about the model as well as the noise. After some cycles the current table is stored, and the procedure starts again for the next of the $m$ tables. The $m$ results are then pooled with Rubin's rules. With only one incomplete column, the method is exact Bayesian regression imputation. With several, it is a heuristic that works well in practice but has no general guarantee.

## In plain words

A table has holes in several columns. First, fill every hole with a random value taken from the same column, as a rough start. Then take the first column with holes. Fit a regression that predicts this column from all the others, using only the rows where this column was really seen. Throw away the rough values in this column and put in new values predicted by the fit, with some random noise and some random change to the fit itself. Do the same for the next column with holes, which can now use the better values of the first column. Go around all the columns several times, until the filled values stop drifting. Keep the table. Start again with new random numbers to make the next table. Analyse every table in the usual way and combine the answers.

## The problem

The input is a table $Y$ with $n$ rows and $p$ numeric columns, in which some entries are missing, a number of imputations $m \ge 2$ and a number of sweeps $T \ge 1$. For a column $j$, $O_j$ is the set of rows where $Y_{ij}$ is observed and $M_j$ the set where it is missing. The $q$ incomplete columns are those with $M_j \ne \emptyset$. For each of them the user chooses a conditional model; here it is the normal linear regression of column $j$ on a constant and the other $p - 1$ columns, with the prior $\pi(\beta, \sigma^2) \propto 1/\sigma^2$.

The output is $m$ completed tables. Each one agrees with $Y$ on every observed entry and has a real number in every missing entry. The tables are the input for an analysis that runs on each and is pooled by Rubin's rules.

The method assumes that the data are missing at random (see [missing data mechanism](/missing-data-mechanism/)): the chance that an entry is missing may depend on observed entries, but not on the missing value itself. It needs $|O_j| > p$ for every incomplete column and regressions of full rank.

## The algorithm

```pseudo id=main
MICE(Y, m, T)
L1  for l ← 1 to m do
L2      fill each missing entry with a random observed value of its column
L3      for t ← 1 to T do
L4          for each incomplete column j, from left to right do
L5              draw (β*, σ*) from the posterior of the regression of column j on the other columns, rows O_j
L6              for each row i in M_j do Y_ij ← x_iᵀβ* + σ* z_i      ▷ x_i: the other columns of row i, z_i a fresh N(0, 1) draw
L7      store the completed table as imputation l
L8  return the m completed tables
```

Line L5 fits ordinary least squares to the rows of $O_j$, with the response taken from the data and the predictors taken from the current table, which holds imputed values from earlier steps. Then it draws $\sigma^{*2} = \mathrm{RSS}/c$ with $c \sim \chi^2_{|O_j| - p}$ and $\beta^* = \hat\beta + \sigma^* L u$ with $LL^{\mathsf T} = (X^{\mathsf T}X)^{-1}$ and $u$ standard normal. Line L6 then draws each missing value from the fitted model. Lines L5 and L6 together are one draw from the [posterior predictive distribution](/posterior-predictive-distribution/) of the missing values of column $j$, given the current values of all other columns. The sweep of lines L4 to L6 has the form of one scan of a [Gibbs sampler](/gibbs-sampling/), and the loop of line L3 runs it $T$ times so that the effect of the rough start of line L2 goes away.

The `pmm` variant (predictive mean matching) changes line L6. For each missing row it computes the prediction $x_i^{\mathsf T}\beta^*$, finds the 5 observed rows of the column whose fitted values $x_k^{\mathsf T}\hat\beta$ are closest to it, and copies the observed value of one of them at random.

## Example

The table has $n = 200$ rows and three columns $(y, x, z)$, generated by $z \sim N(0, 1)$, $x = 0.5z + e_1$ and $y = 1 + x - 2z + e_2$ with independent standard normal $e_1, e_2$. The value $y$ is missing with probability $1/(1 + e^{0.8 - 1.5z})$ and $x$ with probability $1/(1 + e^{1.2 + z})$, so the missingness depends only on the complete column $z$, which is missing at random. In the data set used here (seed 1 of Python's `random.Random`), 77 values of $y$ and 45 values of $x$ are missing, 8 rows miss both, and 86 rows are complete. Rows with large $z$ often lose $y$, and those rows have small $y$, so the mean of the observed $y$ is $1.245$, while the mean of all 200 values before deletion is $0.632$.

The table shows the mean of the 77 imputed $y$ values after each sweep, for three independent runs of lines L2 to L6 (seed 3). The random start of line L2 gives a mean of $1.257$ in the first run, the mean of the observed values. One sweep moves it to about $-0.3$, and after that the three chains move around the same level without a trend.

| sweep | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| chain 1 | $0.053$ | $-0.454$ | $-0.425$ | $-0.512$ | $-0.216$ | $-0.290$ | $-0.206$ | $-0.312$ |
| chain 2 | $-0.339$ | $-0.774$ | $-0.612$ | $-0.435$ | $-0.465$ | $-0.270$ | $-0.770$ | $-0.274$ |
| chain 3 | $-0.385$ | $-0.170$ | $-0.115$ | $-0.554$ | $-0.533$ | $-0.266$ | $-0.107$ | $-0.479$ |

With $m = 5$ and $T = 10$, the five estimates of the mean of $y$ are $0.653$, $0.718$, $0.837$, $0.641$ and $0.553$. Rubin's rules give $\bar Q = 0.680$, $W = 0.0178$, $B = 0.0111$, the total variance $W + (1 + 1/m)B = 0.0312$ and $\nu = 21.9$, so the 95% interval is $(0.314, 1.047)$. The interval from the observed $y$ alone is $1.245 \pm 0.32$, which misses the true mean $1$. For the coefficient of $x$ in the regression of $y$ on $x$ and $z$, the pooled estimate is $0.844$ with interval $(0.532, 1.156)$; here $B$ is larger than $W$, the fraction of the variance due to the missing data is $0.73$, and $\nu$ is only $7.5$.

The next table is measured, not proved. It repeats the setup for 300 data sets ($m = 5$, $T = 5$) and gives the mean error of the estimate and the coverage of the nominal 95% interval for the mean of $y$ and for the coefficient of $x$. The complete-case mean uses all observed $y$; the complete-case regression uses the rows where $y$ and $x$ are both observed. The Monte Carlo standard error of a coverage near $0.95$ is about $0.013$.

| method | mean of $y$: bias | mean of $y$: coverage | coefficient of $x$: bias | coefficient of $x$: coverage |
|---|---|---|---|---|
| MICE, normal draws | $0.002$ | $0.963$ | $-0.005$ | $0.940$ |
| MICE, predictive mean matching | $0.058$ | $0.900$ | $-0.064$ | $0.893$ |
| complete cases | $0.588$ | $0.063$ | $0.000$ | $0.960$ |

Three things show. Complete cases fail badly for the mean. They are fine for the regression coefficient, because the missingness depends only on $z$, which is in the regression. Predictive mean matching is biased here: the missing $y$ lie mostly below the observed ones, and matching can only copy observed values.

## Correctness

The proof below shows four facts. The observed entries are never changed, and every missing entry is filled after line L2, so the output has the stated form. The run stops after exactly $mTq$ regression draws. Line L5 draws exactly from the posterior of the normal linear model with the prior $1/\sigma^2$. If only one column is incomplete, every stored table is an exact and independent posterior predictive draw for any $T \ge 1$, because the predictors never change; MICE then reduces to the regression imputation on the [multiple imputation](/multiple-imputation/) page.

For two or more incomplete columns, the proof does not show convergence. The conditional models are chosen one by one, and in general no joint distribution has them as its full conditionals. Then the chain is not a Gibbs sampler for any joint model, and its limit, if it has one, can depend on the order of the columns. Liu, Gelman, Hill, Su and Kropko (2014) give conditions under which the limit is close to the right posterior predictive law in large samples when the models are compatible. The good coverage in the example is measured, for one data model.

## Complexity

One visit of line L5 builds the design in $O(np)$, forms $X^{\mathsf T}X$ in $O(np^2)$, inverts it and takes the Cholesky factor in $O(p^3)$, and draws $p + 1$ random variates. Line L6 costs $O(p)$ per missing entry, at most $O(np)$ per column. Lines L5 and L6 run $mTq$ times, so the time is $O(mTq(np^2 + p^3))$. The line L2 fill costs $O(np)$ per imputation. The working table and the design take $O(np)$ space, and the $m$ stored tables take $O(mnp)$.

The `pmm` variant also has to find the nearest fitted values. The reference implementation sorts all $|O_j|$ distances for each missing entry, which costs $O(|M_j|\,|O_j| \log |O_j|)$ per visit. Sorting the fitted values once and using binary search brings this to $O((|O_j| + |M_j|)\log |O_j|)$.

## Properties

- **Observed data are kept.** Every completed table agrees with the data on the observed entries.
- **Randomized.** The output depends on the random numbers. A fixed seed makes it reproducible, and different seeds give different but equally valid sets of imputations.
- **Proper for one incomplete column.** The parameters are drawn from their posterior before each set of missing values, so the between-imputation variance includes the uncertainty about the regression. This is what makes Rubin's rules give valid intervals.
- **Flexible by column.** Each column can have its own model: linear regression for a continuous column, logistic regression for a binary one, matching for a skewed one. This is the main reason MICE is used instead of a joint model.
- **No joint model in general.** The method is defined by the conditional models alone, and they need not fit together.
- **Embarrassingly parallel.** The $m$ chains are independent and can run at the same time.

## Variants and improvements

- **Predictive mean matching.** Copy the observed value of a donor with a close predicted mean. The imputations are always plausible values, such as integers or values in range, and the method is robust to some departures from normality. It cannot impute outside the range of the observed values.
- **Other conditional models.** Use [logistic regression](/logistic-regression/) for binary columns, multinomial or ordinal models for categorical ones, and classification and regression trees or random forests when the relations are nonlinear. The parameters must still be drawn from an approximate posterior, often by a bootstrap of the rows.
- **Passive imputation.** A derived column, such as a sum score or a ratio, is recomputed from its parts after each step instead of being imputed, so that it stays consistent with them.
- **Predictor selection.** With many columns, each regression uses only the columns that are correlated with the target or with its missingness. This keeps the regressions small and of full rank.
- **Joint modelling.** Draw all missing values from one multivariate model, for example the multivariate normal by data augmentation. It has a clear theory but is less flexible for mixed column types. For multivariate normal data, MICE with linear regressions uses conditionals that are compatible with that joint model.
- **Monotone patterns.** If the columns can be ordered so that a missing entry in one column implies a missing entry in all later columns, a single pass in that order, where each column is regressed only on the earlier columns, needs no iteration.

## When to use it

Use MICE when several columns of a data set have missing values, the data can be taken to be missing at random, and the columns are of different types, so that no single joint model is natural. It is the standard tool for this in medical and social science data. Include in the imputation models every variable of the later analysis, including the outcome, and any variable that predicts the missingness. If only one column is incomplete, the iteration is not needed, and plain regression imputation gives the same result. If the missingness depends on the missing values themselves, MICE alone does not remove the bias; a sensitivity analysis or a model for the missingness is needed.

## Pitfalls

- **Too few sweeps.** The chains must forget the rough start. Run several chains and plot the mean and variance of the imputed values against the sweep. A trend, or chains that do not mix, means that more sweeps are needed or that the models are poorly set up.
- **Leaving out the outcome.** If the outcome of the analysis is not a predictor in the models for the incomplete covariates, the imputed covariates have no relation with the outcome, and the estimated effects are biased toward zero.
- **Analysis and imputation models that disagree.** If the analysis has interactions or squared terms that the linear imputation models do not contain, the imputed values do not carry these relations. Impute the derived terms as columns of their own or use models that contain them.
- **Matching in the tail.** Predictive mean matching copies observed values, so it is biased when the missing values lie outside the range of the observed ones, as in the example.
- **Collinearity and perfect prediction.** A derived column that is a function of other columns makes the regression singular. A binary column that some predictor separates perfectly makes the logistic fit diverge. Remove such predictors or use passive imputation.
- **Missing not at random.** The method uses only the observed relations between the columns. If the missing values are systematically different from observed values with the same other columns, the imputations are biased in the same way.
- **One imputation.** A single completed table treats imputed values as data and gives standard errors that are too small. Use $m \ge 5$, and more when the fraction of missing information is large.

## Implementations

## History

Van Buuren, Boshuizen and Knook (1999) used a cycle of one regression model per incomplete variable to impute missing blood pressure values in a survival analysis of older people, and published software under the name MICE. Raghunathan, Lepkowski, Van Hoewyk and Solenberger (2001) gave the same idea as sequential regression multivariate imputation for survey data. Van Buuren, Brand, Groothuis-Oudshoorn and Rubin (2006) introduced the name fully conditional specification, showed by simulation that incompatible models often do little harm, and compared it with joint modelling. The R package `mice`, described by van Buuren and Groothuis-Oudshoorn (2011), made the method the most widely used form of multiple imputation. Liu, Gelman, Hill, Su and Kropko (2014) studied the stationary distribution of such iterative imputations.

## References
