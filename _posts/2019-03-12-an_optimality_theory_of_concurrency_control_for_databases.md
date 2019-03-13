---
layout: post
title: Discussing "An optimality theory of concurrency control for databases" by Kung & Papadimitriou 
overview: true
tags: [serialization, concurrency, weak-serialization, scheduling, paper, linearizability]
---

This blog post is an intro to a (potentially long) series of posts that revolve around correctness criteria of concurrent objects and systems, most notably linearizability, sequential consistency, serializability, etc. My objective is to write these blog posts to help me better understand the above concepts, because I have found out that writting helps me organize my thoughts on a topic, and as a consequence, understand it more deeply.

I was initially planning to read several important papers in the field and then organize them in a series of posts and that is why I started reading [[Kung & Papadimitriou 1978](#kung-papadimitriou-1978)]. However, while reading it, I was amazed by their results and I thought that this specific paper deserves to be a post on its own.

In this post, I will try to write my thoughts on this this paper, rephrasing and explaining their results, and trying to elaborate more on them. While this post was mostly written to help me understand the paper, I think that it might be helpful to read it side by side with the original paper, to maybe get a firmer grasp of some ideas or implications that could be easily skipped if one doesn't pay too much attention (they certainly did skip me when I first read the paper). As I am far from an expert on this field (maybe not even knowledgable) I would _strongly_ encourage any comment or feedback on anything that is wrong, misphrased, etc in this post.

After this long (and possibly unnecessary) introduction let's get right into the paper.

## Motivation

Object systems are data systems that are shared among multiple users. An object system, usually comes with a description of what it means for the data that it stores to be consistent<a class="footnote" href="#fn-1"><sup>1</sup></a>. <span class="footnoteText">A standard instance of an object system is a database.</span> It is important for the data that is stored in the object system to always satisfy those requirements. For example, imagine a banking system which contains the data about the bank accounts of the bank's clients. A consistency requirement is that an account should never contain negative amounts of money.

User interact with an object system through sequences of requests (aka transactions) that read or update values of the system. Therefore an issue that naturally arises is making sure that executing the user requests on a consistent object system, should preserve its consistency. This is the task of concurrent "access" control mechanisms. In a single user environment, this task is relatively simple, since each transaction is executed as a contiguous block, and a transaction starts executing only when the previous has finished. In this setting, the problem reduces to verifying that each transaction preserves the consistency requirements of the object system (if executed on a consistent state of the system). In the multi-user setting however, the problem is much harder, because even if each transaction preserves consistency; arbitrarily interleaving their requests might not.

It is clear that consistency preservation should be the primary objective of a concurrent "access" control mechanism. However, it can't be considered in isolation. A trivial solution to preserve consistency would be to execute all transactions of the first user until they log off, then execute the transactions of the second user until they log off, etc. This execution order clearly preserves consistency, and enforcing it requires minimal information from each transaction (just the id of the user who issued it). However, its performance is disastrous! The more users interact with the system, the more each user has to wait until its requests are processed. Imagine wanting to transfer some money between some accounts on an online banking system, and having to wait for all the users who logged in before you to log out before the system processes your request. 

Therefore, there are two necessary properties to consider when designing a concurrent "access" control mechanism (which from now on we will call scheduler). 
- **Performance:**
  Which ideally represents how long does it take for a set of transactions to complete under the scheduler. Note that there is no universal metric of performance, so reasoning about it can be tricky.
- **Information:**
  Which represents the information that the scheduler needs to make its decision. This typically includes syntactic and semantic information for the transactions as well as the integrity constraints.
  
Our objective as the designers of a scheduler is for it to preserve the consistency requirements of the database, while striking a balance between performance and information needed. In this paper, the authors formalize this tradeoff between performance and needed information, and present upper bounds for several information granularities. They show that given only syntactic information, _serialization_ (often called serializability) [[Bernstein et al. 1978](#bernstein-1978), [Papadimitriou 1978](#papadimitriou-1978)] is the best one can hope for and when also given semantic information, it can be relaxed to the weaker notion of _weak-serialization_.

## Transaction Systems

A transaction system is intuitively a triple of data, integrity constraints, and a set of prespecified transaction programs. In a sense a transaction system is like shared object, containins private fields, a set of invariants (integrity constraints) that must always hold for this data, and a set of methods (transactions) that are used to access and modify the private data.

### Syntax

A _transaction system_ $$T$$ contains a finite set of _transactions_ $$\{T_1, ..., T_n \}$$, where each transaction is a finite sequence of steps $$T_{i1}, ..., T_{im}$$. The transactions operate on a set of _variables_ $$V$$, which are abstract variables and the values that they represent are not important. Each transaction step $$T_{ij}$$ contains a read from a global variable $$x_{ij}$$ to a local variable $$t_{ij}$$ and then an assignment to the global value $$x_{ij} := f_{ij}(t_{i1}, ... t_{ij})$$. Note that the two commands are indivisible, and so each transaction step is executed atomically. Transactions are straight line programs in this simplified model, but their results also apply to more general programs.


### Semantics

A state of the transaction system $$T$$ is a triple $$(J, L, G)$$ where:
- $$J$$ is a tuple of program counters (one for each transaction) showing the next step of each transaction.
- $$L$$ is a tuple of the values of all local variables.
- $$G$$ is a product of the values of all global variables $$V$$.

The _integrity constraints_ $$IC$$ can be represented as a subset of all possible $$G$$ values. A state $$(J, L, G)$$ is called _consistent_ if $$G \in IC$$. A sequence of transaction steps is said to be _correct_ if a serial execution of the steps in the sequence maps _any_ consistent state to a consistent state.

__Note:__ As stated above, the basic assumption that they make in this paper is that all transactions in the transaction system are individually correct, and so the sequential composition of any transactions is also correct. The problem that they are tackling in this paper, i.e. finding an interleaving of transactions that is correct, is orthogonal to the sequential verification of each transaction. 


### Schedules

They define a _schedule_ $$\pi$$ of a transaction system to be a permutation of the steps in $$T$$ such that the steps in each specific transaction are kept in order. Intuitively a schedule is an interleaving of all transactions. The set of all schedules of $$T$$ is denoted by $$H(T)$$. Following the definition of correct sequences of transaction steps, a schedule is _correct_ if its execution preserves the consistency of the database. The set of all correct schedules of $$T$$ is denoted by $$C(T)$$. Note that the set $$C(T)$$ is non-empty for all transaction systems, as it contains at least all the serial schedules as described above.


### Scheduler

As stated above, the main problem that the paper deals with is designing a concurrency access control mechanism that orders (serializes) transaction steps from individual users, preserving the database consistency while not degrading performance. From now on, we will call the concurrency access control mechanism a _scheduler_. Formally a scheduler is a mapping $$S$$ from $$H$$ to $$C(T)$$. A scheduler is correct when all of the schedules that it produces are correct, $$S(H) \subseteq C(T)$$. 

An interesting point is how they measure a performance. They define the performance of a scheduler $$S$$ to be its _fixpoint set_ $$P$$, which is defined to be the largest subset of $$H(T)$$ satisfying:

$$
\forall h \in P : S(h) = h 
$$

In a sense, a scheduler's fixpoint set is the set of transaction step sequences (schedules) that the scheduler keeps intact, allowing them to be executed in the order that they appear for execution. At first sight, it is not clear why this is a reasonable performance metric, however they justify it by arguing that the size of the fixpoint set correlates with the waiting time for each user (which can also be thought of as the latency of a request).
- Assuming that the probability distribution schedules is uniform, the probability that none of the transaction steps have to wait is 
$$ |P| / |H| $$.
- The more schedules $$P$$ contains, the "easier" it is to rearrange a history originaly not in $$P$$ into one in $$P$$.
- If the fixpoint set of a scheduler $$S_1$$ is a strict superset of the fixpoint set of a scheduler $$S_2$$, then scheduler $$S_1$$ is clearly better performing than scheduler $$S_2$$, so this metric allows them to partially order schedulers based on their performance.

Except for the performance of the scheduler (i.e. how long do transaction steps have to wait until they are released), we must also think about the cost of the scheduler making decisions. In this paper, they address the _information_ that the scheduler needs to make a decision, whereas in [[Papadimitriou 1978](#papadimitriou-1978)] they examine the time that schedulers need to make decisions in relation to their performance.

The fixpoint set $$P$$ of an optimal scheduler (performance wise) would be equal to $$C(T)$$, as it would let all correct schedules be executed without any reordering. However, it is not always possible (nor sometimes desirable) to have a scheduler that executes all correct schedules in the order that they happened, because of the amount of information needed. 

## Information Levels

In order to capture this relation of the information available to the scheduler with its performance, it is important to formally define the notion of information.

We say that a _level of information_ that is available to a scheduler about a transaction system $$T$$ is a set $$I$$ of transaction systems that contains $$T$$. Intuitively, the scheduler knows that $$T$$ is in $$I$$ but cannot distinguish it from the rest of the transaction systems. Alternatively, one could think about $$I$$ as a function that maps any transaction system to an information object $$I(T)$$. Then two transaction systems $$T$$ and $$T'$$ cannot be distinguished with level of information $$I$$ if they map to the same $$I(T) = I(T')$$.

One of the main theorems of the paper follows below:

> **Theorem 1:** 
> For any scheduler using information I, its fixpoint set P must satisfy:
>
> $$
> P \subseteq \bigcap_{(T' \in I)} C(T')
> $$

The scheduler cannot distinguish between the different transaction systems in $$I$$, and because of that, all the schedules that it allows to be executed without any reordering, have to be in the correct schedule sets of all the indistinguishable transaction systems in $$I$$. Otherwise the scheduler might end up allowing an incorrect schedule to be executed as is, which would lead to an inconsistent state. Thus, this upper bound on $$P$$ indictates, that the coarser the level of information that is available to the scheduler, the less efficient the scheduler can be. 

As a corollary, an optimal scheduler (in regards to the size of the fixpoint set as a metric of performance), has:

$$
P = \bigcap_{(T' \in I)} C(T')
$$

Using the above definitions of levels of information and performance, we can partially order schedulers based on sophistication (a scheduler $$S$$ is more sophisticated than $$S'$$, if it uses finer information for its decisions $$I \subseteq I'$$) and we can also partially order them in respect to performance ($$S$$ performs better than $$S'$$, if $$P' \subseteq P$$). 

Then, the mapping from a level of information $$I$$ to the fixpoint set of the optimal scheduler for $$I$$ captures the trade-off between scheduler information and performance. As stated above, the more information the scheduler has, the better performance it can have.


## Optimal Schedulers

We have now arrived to the main section of the paper, which contains results about optimal schedulers for several standard levels of information. 

### Maximum and Minimum Information Optimal Schedulers

The optimal _maximum information_ scheduler knows all the information about the transaction system $$I = \{T\}$$ and because of that $$P = C(T)$$.

The optimal _minimum information_ scheduler produces only serial schedules, that is schedules where each transaction is executed after another finishes and only one transaction is executed at each time. Those schedules are correct by definition as performing a transaction on a consistent state, returns a consistent state. 

### Optimal Schedulers for Complete Syntactic Information

Suppose that all syntactic information about $$T$$ is available, so $$I$$ is the set of all transaction systems with the same syntax. A schedule $$h$$ is _serializable_ if its execution results (the values of the variables in the final state of the system) are the same as the execution results of some serial schedule under Herbrand semantics<a class="footnote" href="#fn-2"><sup>2</sup></a>
<span class="footnoteText">Herbrand semantics is a way to interpret syntactic constructs without losing any information. A function call is interpreted as the name of the function being called and the names of the parameters passed to it. Intuitively it captures the history of the values of the variables during the computation. For example, the value of $$z$$ after the end of transaction $$t_1 := f_1(x); z := f_2(y, t_1)$$ under Herbrand semantics is $$f_2(y, f_1(x))$$.</span>
[[Manna 1974](#manna-1974)].

A serializable schedule is one that cannot be distinguished (by looking at the execution results) by a serial schedule (which is correct by definition). Based on the Herbrand semantics, two final results are equal, when exactly the same function calls and arguments where used to compute them. So "same execution results" means syntactic equality of the expressions used to compute a variable.

Let's denote the set of all serializable histories of $$T$$ as $$SR(T)$$. A _serialization scheduler_ is defined to be a scheduler which satisfies:

$$
\forall T, P = SR(T) \wedge S(H) = P
$$

So it is a scheduler that allows all serializable schedules to pass without an issue, and maps every other schedule to a serializable one. A serialization scheduler is "faster" compared to a serial scheduler, in the sense that its fixpoint set contains all serializable schedules (which are a superset of serial schedules). It ensures correctness for any history $$h$$ by reordering it to a serial schedule which has the same execution results (under Herbrand semantics) and is correct by definition. 

The serialization scheduler intuitively looks well-performing when only given syntactic information. Well now comes the main theorem of the paper and its very elegant proof.

> **Theorem 2:** 
> The serialization scheduler is correct, and is optimal(!) among all schedulers using complete syntactic information.

**Proof:**

Let's first focus on correctness, so the fact that the scheduler always produces a correct schedule:

$$
\forall T' \in I, SR(T') \subseteq C(T')
$$

To prove the above, they use Herbrand's theorem [[Manna 1974](#manna-1974)] which states that if two sequences of steps are equivalent under the Herbrand interpretation, they are equivalent under any interpretation<a class="footnote" href="#fn-3"><sup>3</sup></a>.
<span class="footnoteText">Of course this assumes that functions are pure and don't produce any side effect.</span> 
Thus for every $$h \in SR(T')$$ there exists a serial schedule which has the same execution results with $$h$$. As we know that all serial schedules are correct, the above implies that every $$h \in SR(T')$$ is also correct.

To prove optimality, they show that for any history $$h \notin SR(T)$$ there exists a transaction system $$T' \in I$$ such that $$h \notin C(T')$$. Because the information that the scheduler has, does not allow it to distinguish between the transaction systems is $$I$$, if the scheduler produces a non serializable schedule $$h$$, then an adversary could force the scheduler to produce this incorrect schedule by giving it to execute the transaction system $$T'$$. 

Based on the above, given a history $$h \notin SR(T)$$, they want to define a transaction system $$T' \in I(T)$$ with very strict integrity constraints, such that $$h \notin C(T')$$. Let the semantics of $$T'$$ be the Herbrand interpretation. Now given the initial values of the global variables $$(v_1, v_2, ..., v_k)$$, the values $$(a1, a2, ..., ak) \in IC$$ if and only if there exists a possibly empty sequence $$S$$ of steps that is a concatenation of _serial executions_ of transactions such that the initial values of the global variables are transformed by $$S$$ to $$(a1, a2, ..., ak)$$. By this definition, all transactions are individually correct, and the basic assumption holds. Now it is easy to see that, if $$h$$ is any history, that doesn't belong to $$SR(T')$$, then it transforms the initial values $$(v1, ..., vk)$$ to values that are not in $$IC$$, so $$h \notin C(T')$$. $$\square$$

To get a better intuition of the construction of $$T'$$ in the proof, here follows an example (inspired by _Figure 1_ in section 4.3 of the paper) of such a transaction system $$T'$$.

Suppose $$T'$$ is a system with one global variable $$x$$ with initial value $$x_0$$, and two transactions:

$$
T_1: x := f_1(x); x := f_2(x) \\
T_2: x := f_3(x)
$$

The set of acceptable final states $$IC = \{ x_0, x_1, x_2, x_{12}, x_{21} \}$$ 
where $$x_1$$ is the value of $$x$$ after executing $$T_1$$, so $$x_1 = f_2(f_1(x_0))$$ (similarly $$x_2 = f_3(x_0)$$) and $$x_{12}$$ is the value of $$x$$ after executing $$T_1; T_2$$, so $$x_1 = f_3(x_1)$$ (similarly $$x_{21} = f_2(f_1(x_2))$$).

Note that for this specific transaction system, the set of serializable schedules is the set of serial schedules, as there is no way to reorder any non serial schedule to give the same results (under Herbarnd semantics) with any serial schedule.

The above theorem shows that given complete syntactic information of the transactions, one can hope to create a scheduler whose fixpoint set $$P$$ is at best equal to $$SR(T)$$, because anything more than that wouldn't be correct for some interpretation and integrity constraints. That is why most approaches to concurrency control (at the time) had serialization as their objective.

In practice, we cannot even expect to get a scheduler with $$P = SR(T)$$, as in [[Papadimitriou 1978](#papadimitriou-1978)] it is shown that serialization is intractable, and for some transaction systems of restricted syntax, it can be _approximated_ by more restrictive schedulers. 


### Optimal Schedulers for Complete Semantic Information, without Integrity Constraints

In the example above, the history $$h = T_{11}; T_{21}; T_{12}$$ is not serializable since its final value (under Herbrand semantics) does not satisfy the integrity constraints. However, given an interpretation of the functions as $$f_1(x) = x + 1$$, $$f_2(x) = 2 * x$$, and $$f_3(x) = 3 * x$$ the history $$T_{11}; T_{21}; T_{12}$$ returns the same value for $$x$$ as $$T1;T2$$. This shows, that given semantic information, a serialization scheduler, is not optimal, and we can do better. 

Therefore, they define a generalized notion of serialization as follows:

A schedule $$h$$ is said to be _weakly serializable_<a class="footnote" href="#fn-4"><sup>4</sup></a>,
<span class="footnoteText">The name _weak serialization_ is (in my opinion) not the best way to define this generalized notion of serializability, because it doesn't indicate anything about its difference with serialization (except that it is weaker).</span> if starting from any state $$E$$, the execution of the schedule will end with a state that is achievable by some concatenation of transactions also starting from state $$E$$. This way the fixpoint set $$P$$ is extended to be the set of schedules that lead to a semantically equivalent final state, instead of a syntactically equivalent one (which is semantic equivalence under Herbrand interpretation).

Denote by $$WSR(T)$$ the set of all weakly serializable schedules of $$T$$. It is clear that $$SR(T) \subseteq WSR(T)$$. The weak serialization scheduler $$S$$ is defined so that it satisfies: 

$$
\forall T, P = WSR(T) \wedge S(H) = P
$$

Similarly to the above theorem, it holds that the weak serialization scheduler is optimal among all schedulers using all information (syntactic and semantic) but the integrity constraints. 

Note that they don't propose an optimal scheduler that also has access to the integrity constraints.

## Discussion

An important question is the relation of the above results to the real performance of a database using a specific scheduler. As the database is used by clients, a reasonable performance metric is the execution time of a transaction from the perspective of the clients. This can be divided into three parts:

- _Scheduling time:_ This is the time that it takes for the scheduler to make its decision. It mostly depends on the sophistication of the scheduler and the amount of information that it has available (and uses).

- _Waiting time:_ The total time that the scheduler delayed executing each transaction step of a transaction, so that it could preserve consistency.

- _Execution time:_ The time that is actually spent in executing each step of the transaction.

In this paper, they mostly focus on the waiting time, and they argue that the fixpoint set $$P$$ is a good metric of the waiting time as described [above](#scheduler). 

Another important issue that needs to be noted is that there is an implicit assumption underlying the model that all information is available to the scheduler from the start. This implies that the transactions to be executed are fixed and known by the scheduler statically. However, that is not a reasonable assumption as in practice the scheduler would acquire most information (especially the knowledge about which transactions are to be executed) dynamically as the clients make requests. They pinpoint this issue, and suggest it as future work.

Before closing this post, I would like to briefly touch on the following issue. There is often a confusion of the connection between correctness criteria for data objects (such as linearizability, sequential consistency, serializability) as these notions are very subtle. At first sight, it seems like linearizability and serializability are very similar notions (their names also mislead to this conclusion). However, this is not the case and I will try to clarify this confusion here.

Linearizability is used as a correctness criterion of a concurrent data object implementation against a sequential specification $$Spec$$. An execution $$e$$ of a concurrent system is linearizable (to $$Spec$$ if there exists an execution $$e'$$, such that $$e'$$ can be produced by $$Spec$$ and if $$op_1$$ was completed before $$op_2$$ in $$e$$, then $$op_1$$ completes before $$op_2$$ in $$e'$$ (in other words, $$e'$$ contains the same operations as $$e$$ with possibly some reordering of overlapping operations). An implementation of a data object is linearizable to $$Spec$$ if all executions that it produces are linearizable to $$Spec$$. Intuitively, linearizability means that a concurrent implementation behaves (from an observer's perspective [[Filipovic et al. 2010](#filipovic-2010)]) as a sequential specification<a class="footnote" href="#fn-5"><sup>5</sup></a>.
<span class="footnoteText">Linearizability and other correctness criteria for concurrent data objects are very interesting topics that deserve many blogposts, so I won't get into many details here. However, I plan to make a few posts related to these topics in the future.</span>

In contrast to the above, this work approaches the issue of correctness from a different viewpoint. Assuming that there exists a correctness specification of the system (defined based on the semantics and the integrity constraints) under which a set of schedules $$O$$ of the transaction system are correct, the goal is to design a scheduler with the largest subset of those schedules (ideally all of them) as its fixpoint set $$P$$, which reorders any other schedule to its "closest" reordering in $$P$$. The intuition is that the larger $$P$$ is, the more schedules are executed without any waiting (while preserving consistency of the database) and therefore the better the performance of the scheduler is. Specifically in this work, they study upper bounds on the fixpoint sets for several different levels of information available to the scheduler. The set of all serializable schedules for example, is the largest subset of schedules that a scheduler can hope to have in its fixpoint set if it only has syntactic information about the transaction system.


<hr>

### Bibliography

<a name="bernstein-1978">[Bernstein et al. 1978]</a>: P.A. Bernstein , N. Goodman, J.B. Rothnie, and C.H. Papadimitriou. 1978. A System of Distributed Databases (the Fully Redundant Case).

<a name="filipovic-2010">[Filipovic et al. 2010]</a>: I. Filipovic, P. O'Hearn, N. Rinetzky, and H. Yang. 2010. Abstraction for Concurrent Objects.

<a name="kung-papadimitriou-1978">[Kung & Papadimitriou 1978]</a>: H.T. Kung and C.H. Papadimitriou. 1978. An optimality theory of concurrency control for databases.

<a name="manna-1974">[Manna 1974]</a>: Z. Manna. 1974. Mathematical Theory of Computation

<a name="papadimitriou-1978">[Papadimitriou 1978]</a>: C.H. Papadimitriou. 1978. Serializability of Concurrent Updates.
