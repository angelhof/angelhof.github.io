---
layout: post
title: Discussing "An optimality theory of concurrency control for databases" by Kung & Papadimitriou 
overview: true
tags: [serialization, concurrency, weak-serialization, scheduling, paper, linearizability]
---

This blog post is an intro to a (potentially long) series of posts that revolve around correctness criteria of concurrent objects and systems, most notably linearizability, sequential consistency, serializability, etc. My objective is to write those blog posts to help me better understand the above concepts, because I have found out that writting helps me organize my thoughts on a topic, and as a consequence, understand it more deeply.

I was planning to first read several important papers in this field and then organize them in a series of posts and that is why I started reading [[Kung & Papadimitriou 78](#kung-papadimitriou-1978)]. However, while reading it I was amazed by their results, and I thought that this specific paper might be a post on its own.

In this post, I will try write my thoughts while reading this paper, rephrasing and explaining their results, trying to elaborate more on them. While this post was mostly written to help me understand the paper, I think that it might be helpful to read it side by side with the original paper, to maybe get a firmer grasp of some ideas or implications that could be easily skipped if one doesn't pay too much attention (they certainly did skip me when I first read the paper). As I am far from an expert on this field (maybe not even knowledgable) I would _strongly_ encourage any comment or feedback on anything that is wrong, misphrased, etc in this post.

After this long (and possibly unnecessary) introduction let's get right into the paper.

## Motivation

Object systems are data systems that are shared among multiple users. An object system, usually comes with a description of what it means for the data that it stores to be consistent<a class="footnote" href="#fn-1"><sup>1</sup></a>. <span class="footnoteText">A standard instance of an object system is a database.</span> It is important for the data that is stored in the object system to always satisfy those requirements. For example, imagine a banking system which contains the data about the bank accounts of the bank's clients. A consistency requirement is that an account should never contain negative amounts of money.

User interact with an object system through sequences of requests (aka transactions) that read or update values of the system. Therefore an issue that naturally arises is making sure that executing the user requests on a consistent object system, should preserve its consistency. In a single user environment, this task is relatively simple, since each transaction is executed as a contiguous block, and a transaction starts executing only when the previous has finished. In this setting, the problem reduces to verifying that each transaction preserves the consistency requirements of the object system (if executed on a consistent state of the system). In the multi-user setting however, the problem is much harder, because even if each transaction preserves consistency; arbitrarily interleaving their requests might not.

<!-- It is desirable for a (database/object system) to be time-shared among multiple users.  -->
<!-- The different steps of different requests may be interleaved in any order, and despite assuming -->
<!-- that each transaction is correct on its own (it preserves the consistency of the database), -->
<!-- when arbitrarily interleaved with other transactions it might bring a consistent database state  -->
<!-- to an inconsistent one.  -->

<!-- Interpretation: -->
<!-- When there is only one user performing requests to the object system, it is easy as a problem to -->
<!-- verify and maintain consistency, because each request is executed after the other has finished. -->

<!-- If the multi-user system was also implemented in a naive way, a user would acquire a lock for -->
<!-- each one of their requests and release it when done. Then if each request preserves the consistency of -->
<!-- the database, inductively, the database is always in a consistent states if it starts from one. -->

<!-- However, acquiring a lock, and processing every request atomically offers very low performance, -->
<!-- and doesn't scale to many users.  -->

<!-- Thus in the quest for performance, requests from different users are allowed to be interleaved in  -->
<!-- possibly arbitrary ways. However, now the task of mainting consistency is not as simple, and  -->
<!-- executing arbitrary interleaving of (consistence preserving) requests, doesn't necessarily maintain -->
<!-- consistency. -->

<hr>

**TODO:** Introduce concurrent access control mechanisms before just stating them here

It is clear that consistency preservation should be the primary objective of a concurrent "access" control mechanism. However, it can't be considered in isolation. A trivial solution to preserve consistency would be to execute all transactions of the first user until they log off, then execute the transactions of the second user until they log off, etc. This execution order clearly preserves consistency, and enforcing it requires minimal information from each transaction (just the id of the user who issued it). However, its performance is disastrous! The more users interact with the system, the more each user has to wait until its requests are processed. Imagine wanting to transfer some money between some accounts on an online banking system, and having to wait for all the users who logged in before you to log out before the system processes your request. 

Therefore, there are two necessary properties to consider when designing a concurrent "access" control mechanism (which from now on we will call scheduler). 
- **Performance:**
  Which ideally represents how long does it take for a set of transactions to complete under the scheduler. Note that there is no universal metric of performance, so even reasoning about it can be tricky.
- **Information:**
  Which represents the information that the scheduler needs to make its decision. This typically includes syntactic and semantic information for the transactions as well as the integrity constraints.
  
Our objective as the designers of a scheduler is for it preserve the consistency requirements of the database, while striking a balance between performance and information needed. In this paper, the authors formalize this tradeoff between performance and needed information, and present upper bounds for several information granularities. They show that given only syntactic information, **serialization** [[Bernstein et al 1978](#bernstein-1978), [Papadimitriou 1978](#papadimitriou-1978)]
is the best one can hope for and when also given semantic information, **serialization** can be relaxed to a weaker form.

<!-- Consistency is the primary objective of concurrent "access" control. However, it is not the only -->
<!-- one. Trivial solutions exist for concurrent consistency, but they offer disastrous performance. -->
<!-- A trivial one would be to only execute user1's requests until they log off, then execute user2's... -->
<!-- This clearly lacks regarding performance, however it has a serious benefit. The concurrency control  -->
<!-- mechanism only needs to know about the User ID associated with each transaction to make its decisions. -->

<!-- Therefore, there are two necessary properties to consider for the design of a scheduler. -->
<!-- - **Its performance** -->
<!--   They measure performance as the set of request sequences which the scheduler can pass without  -->
<!--   any delay. So in the sense it is some form of latency. They call this set the __fixpoint set__ of  -->
<!--   a scheduler and they argue that if a scheduler has a strictly larger fixpoint set, it performs better -->
<!--   when regarding average delays (this seems a bit not believable). -->
  
<!-- - **The information that it needs/uses in order to schedule requests** -->
<!--   Typical information can be: -->
<!--   + syntactic information about the transactions -->
<!--   + semantic information about the meaning of the data and the operations performed -->
<!--   + integrity constraints, or the consistency requirements that the data must satisfy -->
<!--   However,they claim that excessive information might be distracting and make the  -->
<!--   scheduler less efficient. (Examined in detail in [Papadimitriou 1979]). -->
<!--   In addition, some information might not be available (like the integrity constraints -->
<!--   and if the semantics are expressed in a powerful enough language, then the scheduler  -->
<!--   may be faced with undecidable problems. -->
  
<!-- Intepretation: -->

<!-- We clearly want consistency as our main objective, when designing the concurrent access controller. -->
<!-- However, we have to somehow balance between performance and the information that the scheduler  -->
<!-- needs in order to make its decisions, because by designing it poorly we might end up with horrific -->
<!-- performance, or with undecidable decisions.  -->

<!-- -------------------------------------------------------------------------------------------------- -->
  
<!-- They examine the literature about concurrency control andy give a uniform (__uniform in what sense__) -->
<!-- framework to evaluate different solutions. They point out that there is a tradeoff between performance -->
<!-- of a scheduler and the information that it uses. Their approach allows them to formally show, that -->
<!-- when only syntactic information is available, **serialization** [Bernstein et al 1978, Papadimitriou 1979] -->
<!-- is the best one can hope for (__what does best mean?__). In case of semantic information, other approaches -->
<!-- [Lamport 1993] could be used. -->

<!-- -------------------------------------------------------------------------------------------------- -->

## Transaction Systems

<!-- WARNING: The point of this post is to be self-contained, and so below follow some necessary definitions that will allow us to formalize the notions and results discussed in the paper. If you don't want to realy understand the results of this paper formally, skip ahead to [this section](#optimal-schedulers) where the results are presented and explained in a more informal manner. -->

A transaction system is intuitively a triple of data, integrity constraints, and a set of prespecified transaction programs. In a sense a transaction system is like shared object, containins private fields, a set of invariants (integrity constraints) that must always hold for this data, and a set of methods (transactions) that are used to access and modify the private data.

### Syntax

A _transaction system_ $$T$$ contains a finite set of _transactions_ $$\{T_1, ..., T_n \}$$, where each transaction is a finite sequence of steps $$T_{i1}, ..., T_{im}$$. The transactions operate on a set of _variables_ $$V$$, which are abstract variables and the values that they represent are not important. Each transaction step $$T_{ij}$$ contains a read from a global variable $$x_{ij}$$ to a local variable $$t_{ij}$$ and then an assignment to the global value $$x_{ij} := f_{ij}(t_{i1}, ... t_{ij})$$. Note that the two commands are indivisible, and so each transaction step is executed atomically. Transactions are straight line programs in this simplified model, but their results also apply to more general programs.

<!-- **Syntax** -->

<!-- By a transaction system, they mean a database (data and integrity constraints) together with a set of prespecified transaction programs. In a sense a database is an object, with private data, invariants or integrity constraints that must always hold for this data, and a set of methods that are used to access and modify the private data. -->

<!-- They define transactions to be *finite* sequences of steps, where each step reads from a global variable to a local one and writes to the global variable, based on the values of the local variables in all previous steps. Note that each step is indivisible (atomic) and that transactions are straight line programs in this simplified model. (They claim that in Section 6 they extend those to transactions defined by more general programs. -->

### Semantics

A state of the transaction system $$T$$ is a triple $$(J, L, G)$$ where:
- $$J$$ is a tuple of program counters (one for each transaction) showing the next step of each transaction.
- $$L$$ is a tuple of the values of all local variables.
- $$G$$ is a product of the values of all global variables $$V$$.

The _integrity constraints_ $$IC$$ can be represented as a subset of all possible $$G$$ values. A state $$(J, L, G)$$ is called _consistent_ if $$G \in IC$$. A sequence of transaction steps is said to be _correct_ if a serial execution of the steps in the sequence maps _any_ consistent state to a consistent state.

__Note:__ As stated above, the basic assumption that they make in this paper is that all transactions in the transaction system are individually correct, and so the sequential composition of any transactions is also correct. The problem that they are tackling in this paper, i.e. finding an interleaving of transactions that is correct, is orthogonal to the sequential verification of each transaction. 


<!-- **Semantics** -->

<!-- They assume that each transaction is executed only once and that a state of the transaction system T is a triple (J, L, G) where J is a product of program counters which show the next step of each transaction, L is a product of the values of all local variables, and G is a product of the values of all global variables.  -->

<!-- Integrity constraints can be given as a subset of all possible value products of the global variables. A sequence of transaction steps is said to be **correct** if a serial execution of the steps in the sequence will map any consistent state of the transaction system into a consistent state. -->

<!-- **The basic assumption that they follow (and most other papers in the literature) is that all transactions in a transaction system are correct, so their sequential executions are correct. Verifying that a sequential transaction is correct is a different task, which is supposed to be much easier and orthogonal to the task that all those papers try to solve. All of those papers reason about the subset of interleavings of possible transactions that are correct, given that the transactions themselves are correct.** -->

**TODO: At the end of section 2 they give an example of the system that might be useful to use as a guiding example. Maybe add it**

### Schedules

They define a _schedule_ $$\pi$$ of a transaction system to be a permutation of the steps in $$T$$ such that the steps in each specific transaction are kept in order. Intuitively a schedule is an interleaving of all transactions. The set of all schedules of $$T$$ is denoted by $$H(T)$$. Following the definition of correct sequences of transaction steps, a schedule is _correct_ if its execution preserves the consistency of the database. The set of al correct schedules of $$T$$ is denoted by $$C(T)$$. Note that the set $$C(T)$$ is non-empty for all transaction systems, as it contains at least all the serial schedules as described above.

<!-- **Schedules** -->

<!-- They define a schedule π of a transaction system to be a permutation of the set of steps in $$T$$ such that the -->
<!-- steps in each specific transaction are kept in order. In practice a schedule is an interleaving of all the transaction steps. The set of all schedules of $$T$$ is denoted by $$H(T)$$. A schedule is said to be **correct** if its execution preserves the consistency of the database. The set of all correct schedules of $$T$$ is denoted by $$C(T)$$. The set $$C(T)$$ is always non empty as it at least contains all serial schedules (the ones that execute one transaction after the other). -->

<!-- Interpretation: -->

<!-- In this paper they don't really deal with what linearizability deals. There are several main differences to what I think of as linearizability. First of all, transaction steps are strictly atomic. Second, each transaction doesn't return any output, so our observation is always the state of the object. In addition, we have a set of invariants (integrity constraints) that have to always hold during the system execution. -->

<!-- **NOTE: It seems that a very important difference in many of those papers, is what they consider as observable. Is it the outputs of the requests to the system? Is it the system state? Is there a global observable time of requests? All those slight differences in the model, make for (possibly) interesting changes in the different approaches, and I would like to understand whether those different assumptions make a real difference. At least I want to mention this and ensure that I explicitly claim what do I think is observable** -->

<!-- NOTE: Another important note is that in this work they assume **FIFO communication channels** between each client and the database, so a schedule is always an interleaving where each individual client's requests are not reordered. This is very similar to sequential consistency, so here they already assume that schedules are sequentially consistent. _This makes some sense, because reordering individual client's requests might only need to happen in a distributed object system. **IS THAT CORRECT?**_ -->

### Scheduler

As stated above, the main problem that the paper deals with is designing a concurrency access control mechanism that orders (serializes) transaction steps from individual users, preserving the database consistency while not degrading performance. From now on, we will call the concurrency access control mechanism a _scheduler_. Formally a scheduler is a mapping $$S$$ from $$H$$ to $$C(T)$$. A scheduler is correct when it only produces correct schedules, $$S(H) \subseteq C(T)$$. 

An interesting point is how they measure the performance of a scheduler. They define the performance of a scheduler $$S$$ to be its _fixpoint set_ $$P$$, which is defined to be the largest subset of $$H(T)$$ satisfying:

$$
\forall h \in P : S(h) = h 
$$

In a sense, a scheduler's fixpoint set is the set of transaction step sequences (schedules) that the scheduler keeps intact, allowing them to be executed in the order that they appear. At first sight, it is not clear why this performance metric makes sense, however they justify why the size of the fixpoint set correlates with the waiting time for each user (which can also be thought of as the latency of a request).
- Assuming that the probability distribution schedules is uniform, the probability that none of the transaction steps have to wait is 
$$ |P| / |H| $$.
- The more schedules $$P$$ contains, the "easier" it is to rearrange a history originaly not in $$P$$ into one in $$P$$.
- If the fixpoint set of a scheduler $$S_1$$ is a strict superset of the fixpoint set of a scheduler $$S_2$$, then scheduler $$S_1$$ is clearly better performing than scheduler $$S_2$$, so this metric allows them to partially order schedulers based on their performance.

Except for the performance of the scheduler (i.e. how long do transaction steps have to wait until they are released), we must also think about the cost of the scheduler making decisions. In this paper, they address the _information_ that the scheduler needs to make a decision, whereas in [[Papadimitriou 1978](#papadimitriou-1978)] they examine the time that schedulers need to make decisions in relation to their performance.

The fixpoint set $$P$$ of an optimal scheduler (performance wise) would be equal to $$C(T)$$, as it would let all correct schedules be executed without any reordering. However, it is not always possible (nor sometimes desirable) to have a scheduler that executes all correct schedules in the order that they happened, because of the amount of information needed. 

<!-- **Scheduler** -->

<!-- A scheduler has to transform any schedule to a correct schedule. So it is a mapping S from H to C(T). A scheduler is correct when all its schedules are correct. They measure the **performance** of a scheduler by its fixpoint set P, which is defined to be the largest subset of H satisfying the following: -->

<!-- In a sense, a scheduler's fixpoint set, is the set of execution request sequences (schedules) that the scheduler keeps intact, without changing (it grants requests in the same order that they arrive). **NOTE: This is clearly not a universal performance metric but they explain in Section 6 why it is good enough** -->

<!-- Except for the performance of the scheduler (aka how long do requests have to wait until they are released), we must also think about the cost of the scheduler making decisions. This is either the information or the time thata scheduler requires to make a decision. In this work they derive upper bounds on the performance of schedulers based solely on the **information** that they use (the time that a scheduler needs to make its decisions is addressed in [Papadimitriou 78]). -->

<!-- Ideally we would want P to be equal to C(T), so that the scheduler lets all correct schedules pass intact. However, this is not always possible nor desirable because of the need for a lot of information. Below, they capture this in a formal theorem. What is a formal model of the information abailable to a scheduler S. -->

## Information Levels

In order to capture this relation of the information available to the scheduler with its performance, it is important to formally define the notion of information.

We say that a _level of information_ that is available to a scheduler about a transaction system $$T$$ is a set $$I$$ of transaction systems that contains $$T$$. Intuitively, the scheduler knows that $$T$$ is in $$I$$ but cannot distinguish it from the rest of the transaction systems. Alternatively, one could think about $$I$$ as a function that maps any transaction system to an information object $$I(T)$$. Then two transaction systems $$T$$ and $$T'$$ cannot be distinguished with level of information $$I$$ if they map to the same $$I(T) = I(T')$$.

Now follows one of the main theorems of the paper:



<!-- **A format theory** -->

<!-- A **level of information** available to a scheduler about a transaction system T is a set I of transaction systems that contains T. Intuitively, if S keeps this level of information, it know that T is among I, but doesn't know exactly which.  -->


<!-- **SIDE NOTE: Abstractions, Operations, and the properties that they have to satisfy** -->
<!-- NOTE: _I_ represents in a sense the abstraction that the scheduler does. The granularity to which it can distringuish amond different systems using the information that it gets. The more information (observables) the scheduler has, the finer distinctions it can make between different transaction systems, and thus the smaller the set I will be. This is a general phenomenon, when trying to reason about a system (If I am not wrong, it is also the idea behind abstract interpretation). Reasoning about the system itself is undecidable or requires an extreme amount of information, so the system is thought of as a set of systems, that are all equivalent to its other based on the amount of information that we get. Thus any operation or transition that the system does has to be lifted to the set of systems, and that is where imprecision can lead to very bad results. In a sense we want well behaving approximations, abstractions, that is abstractions that are size preserving when we apply to them operations that we would normally only apply to the system itself. For example, an range abstraction on integers, is not well behaving when the operation that we apply on our states/systems is multiplication with numbers larger than one. Because, when we multiply a number in the range [1, 10] with 2, we can only get [2, 4, .., 20], but our range abstraction will return [2, 20]. A point to be made here is that abstractions have to be chosen together with the operations that are to be applied on the abstracted object, and applying the operations on the abstractions must have some nice properties. -->

<!-- Alternatively we could define I as a projection that maps any transaction system to an object I(T). Then two transaction systems T T', can not be distinguished with level information I, if they map to the same I(T) = I(T'). -->

> **Theorem 1:** 
> For any scheduler using information I, its fixpoint set P must satisfy:
>
> $$
> P \subseteq \bigcap_{(T' \in I)} C(T')
> $$

The scheduler cannot distinguish between the different transaction systems in $$I$$, and because of that, all the schedules that it allows to be executed without any reordering, have to be in the correct schedule sets of all the indistinguishable transaction systems in $$I$$. Otherwise the scheduler might end up allowing an incorrect schedule to be executed as is, which would lead to an inconsistent state. Thus, this upper bound on $$P$$ indictates, that the coarser the level of information that is available to the scheduler, the less efficient the scheduler can be. 

<!-- **SIDE NOTE: It seems like in general when we want to prove something for all, we can assume for contradiction that one of the forall doesn't hold, and then use an adversary to somehow expose that one that doesn't work and create a contradiction.** -->

As a corollary, an optimal scheduler (in regards to the size of the fixpoint set as a metric of performance), has:

$$
P = \bigcap_{(T' \in I)} C(T')
$$

Using the above definitions of levels of information and performance, we can partially order schedulers based on sophistication (a scheduler $$S$$ is more sophisticated than $$S'$$, if it uses finer information for its decisions $$I \subseteq I'$$) and we can also partially order them in respect to performance ($$S$$ performs better than $$S'$$, if $$P' \subseteq P$$). 

Then, the mapping from a level of information $$I$$ to the fixpoint set of the optimal scheduler for $$I$$ captures the trade-off between scheduler information and performance. As stated above, the more information the scheduler has, the better performance it can have.

<!-- Using the above definitions of levels of information and performance, we can partially order schedulers based on sophistication (A scheduler S is more sophisticated than S', if I \subseteq I') and we can also partially order them in respect to performance (S performs better than S', if P' \subseteq P). Then the mapping from any level of information I to the fixpoint set of the optimal scheduler for I: -->

<!-- I -> P (= \bugcap ...) is a natural *isomorphism* between these two partially ordered sets. This capture the fundamental trade-off between scheduler information and performance. If I \subseteq I', then P' \subseteq P, for the optimal schedulers. -->


## Optimal Schedulers

We have now arrived to the main section of the paper, which contains results about optimal schedulers for several standard levels of information. 

### Maximum and Minimum Information Optimal Schedulers

The optimal _maximum information_ scheduler knows all the information about the transaction system $$I = \{T\}$$ and because of that $$P = C(T)$$.

The optimal _minimum information_ scheduler produces only serial schedules, that is schedules where each transaction is executed after another finishes and only one transaction is executed at each time. Those schedules are correct by definition as performing a transaction on a consistent state, returns a consistent state. 

<!-- **Maximum and Minimum Information Optimal Schedulers** -->

<!-- The optimal **maximum information** scheduler has I = {T} and because of that P = C(T). -->

<!-- The optimal **minimum information** scheduler produces only serial schedules, and thus only has serial schedules in its P. The proof is clear, by just constructing a contradiction when a scheduler with minimum information produces any non serial schedule interleaving. -->


### Optimal Schedulers for Complete Syntactic Information

Suppose that all syntactic information about $$T$$ is available, so $$I$$ is the set of all transaction systems with the same syntax. A schedule $$h$$ is _serializable_ if its execution results (the values of the variables in the final state of the system) are the same as the execution results of some serial schedule under Herbrand semantics<a class="footnote" href="#fn-2"><sup>2</sup></a>
<span class="footnoteText">Herbrand semantics is a way to interpret syntactic constructs without losing any information. A function call is interpreted as the name of the function being called and the names of the parameters passed to it. Intuitively it captures the history of the values of the variables during the computation. For example, the value of $$z$$ in after the end of transaction $$t_1 := f_1(x); z := f_2(y, t_1)$$ under Herbrand semantics is $$f_2(y, f_1(x))$$.</span>
[[Manna 74](#manna-1974)].

A serializable schedule is one that cannot be distinguished (by looking at the execution results) by a serial schedule (which is correct by definition). Based on the Herbrand semantics, two final results are equal, when exactly the same function calls and arguments where used to compute them. So "same execution results" means syntactic equality of the expressions used to compute a variable.

<!-- **Optimal Schedulers for Complete Syntactic Information** (WOW) -->

<!-- Suppose that all syntactic information is available, so I is the set of all transaction systems with the same syntax. (**NOTE(That might be wrong): From what I understand knowing the syntax of the program, means that we know all the names of functions and the arguments that they are given but not the the semantics of the calls themselves. So we don't know what might happen after a call. TODO: Make sure I understand this correctly**)  -->

<!-- A schedule is **serializable** if its execution results (**QUESTION: FINAL OR ALSO INTERMEDIATE RESULTS??**) are the same as the execution results of some serial schedule under the _Herbrand semantics_ (**Read side note below**).  -->

<!-- (**NOTE: A serializable schedule is one that cannot be distinguished (by looking at the execution results) by a serial schedule, which we said that is correct by definition. Because of the Herbrand semantics, two final results are equal, when exactly the same function calls and arguments where used to compute them. So "same execution results" means syntactic equality.**)  -->

<!-- (**NOTE 2: A schedule is serializable if we can reorder its steps to a serial one, while keeping the exact same syntactic results. For example the assignment x := f1(x) might sometimes preserve the value of variable x (based on some branching in f1). However, because we only have knowledge of syntax, we can only reorder the assignment x := f1(x) with the assignment x := f1(x) and not with x := f2(x) despite knowing that for x f1 and f2 return the same value.**)  -->

Let's denote the set of all serializable histories of $$T$$ as $$SR(T)$$. A _serialization scheduler_ is defined to be a scheduler which satisfies:

$$
\forall T, P = SR(T) \wedge S(H) = P
$$

So it is a scheduler that allows all serializable schedules to pass without an issue, and maps every other schedule to a serializable one. A serialization scheduler is "faster" compared to a serial scheduler, in the sense that its fixpoint set contains all serializable schedules (which are a superset of serial schedules). It ensures correctness for any history $$h$$ by reordering it to a serial schedule which has the same execution results (under Herbrand semantics) and is correct by definition. 

<!-- By SR(T) we denote the set of all serializable histories of T. A **serialization scheduler** is defined to be a scheduler S whose P = SR(T) and S(H) = P for any T. So it is the scheduler that allows all serializable schedules to pass without an issue, and that maps every other schedule to a serializable one. In a sense, a serialization scheduler, is "faster" than a serial scheduler because it allows all serializable schedules to pass by intact, and ensures correctness for H by making sure that there exists a reordering of it that gives syntactically equivalent results (under Herbrand semantics) to a serial schedule (which is always correct no matter what). In a sense, the way they make schedulers, is that they build them on top of the simple serial schedulers (which are correct by definition) by allowing them to do equivalent reorderings to schedules to bring them to a serial one. The other approach would be to make sure that the schedule preserves the integrity constraints, but that requires syntactic, semantic, and integrity information, making the problem undecidable(**is it correct that it becomes undecidable?**) -->

<!-- **Side Note on Herbrand Semantics:** -->
<!-- Herbrand semantics is a way to give semantic meaning to syntax, while not losing any information. What it does essentially is to interpret a function call, using the function call syntax itself. It is in a sense like lazy computation, where we keep every function call unintepreted, but we know that it was called. So the semantics of a final assignment migh be f1(x, f2(y,z)). -->

The serialization scheduler intuitively looks well-performing when only given syntactic information. Well now comes the main theorem of the paper and its very elegant proof.

> **Theorem 3:** 
> The serialization scheduler is correct, and is optimal(!) among all schedulers using complete syntactic information.

**Proof:**

Let's first focus on correctness, so the fact that the scheduler always produces a correct schedule:

$$
\forall T' \in I, SR(T') \subseteq C(T')
$$

To prove the above, they use Herbrand's theorem [[Manna 74](#manna-1974)] which states that if two sequences of steps are equivalent under the Herbrand interpretation, they are equivalent under any interpretation<a class="footnote" href="#fn-3"><sup>3</sup></a>.
<span class="footnoteText">Of course this assumes that functions are pure and don't produce any side effect.</span> 
Thus for every $$h \in SR(T')$$ there exists a serial schedule which has the same execution results with $$h$$. As we know that all serial schedules are correct, the above implies that every $$h \in SR(T')$$ is also correct.

<!-- **LEFT HERE** -->

<!-- **Theorem 3:** -->
<!-- The serialization scheduler is: -->
<!-- 1. Correct -->
<!-- 2. Optimal among all schedulers using complete syntactic information. -->


<!-- **Proof:** -->
<!-- 1. To prove correctness (SR(T') \subseteq C(T') for any T' \in I), (so the fact that all serializable schedules are correct), they use Herbrand's theorem [[Manna 74](#manna-1974)] which states that if two sequences of steps are equivalent under the Herbrand interpretation, they are equivalent under any interpretation.  -->

<!-- (Of course this assumes that functions are pure and don't introduce any side effect, so the interpretation of a function call f1(a1, a2, ..., an) only depends on f1, a1, a2, ..., an and nothing else.) -->

<!-- Thus if h \in SR(T') then the execution results of h are the same as those of some serial schedule for T'. This implies that for any h \in SR(T'), the execution of h preserves the consistency of T', as serial schedules all preserve the consistency of T', and thus h \in C(T').-->


To prove optimality, they show that for any history $$h \notin SR(T)$$ there exists a transaction system $$T' \in I$$ such that $$h \notin C(T')$$. Because the information that the scheduler has, does not allow it to distinguish between the transaction systems is $$I$$, if the scheduler produces a non serializable schedule $$h$$, then an adversary could force the scheduler to produce this incorrect schedule by giving it to execute the transaction system $$T'$$. 

Based on the above, given a history $$h \notin SR(T)$$, they want to define a transaction system $$T' \in I(T)$$ with very strict integrity constraints, such that $$h \notin C(T')$$. Let the semantics of $$T'$$ be the Herbrand interpretation. Now given the initial values of the global variables $$(v_1, v_2, ..., v_k)$$, the values $$(a1, a2, ..., ak) \in IC$$ if and only if there exists a possibly empty sequence $$S$$ of steps that is a concatenation of _serial executions_ of transactions such that the initial values of the global variables are transformed by $$S$$ to $$(a1, a2, ..., ak)$$. By this definition, all transactions are individually correct, and the basic assumption holds. Now it is easy to see that, if $$h$$ is any history, that doesn't belong to $$SR(T')$$, then it transforms the initial values $$(v1, ..., vk)$$ to values that are not in $$IC$$, so $$h \notin C(T')$$. $$\square$$

<!-- The semantics of T' are the Herbrand interpretation to simplify things. Now they give the stricter possible integrity constraints, that is (a1, a2, ..., ak) \in IC iff there exists a possibly empty sequence S of steps that is a concatenation of serial executions of transactions such that the initial values (v1, v2, ...vk) of the global variables are transformed by S to (a1, a2, ..., ak). By this definition, all transactions are individually correct, and the basic assumption holds. Now it is easy to see that, if h is any history, not in SR(T'), then it transforms the initial values (v1, ..., vk) to a set of values not in IC, so h not in C(T'). -->

<!-- **NOTE:** The optimality proof is based on the idea that a scheduler has to produce correct schedules for any transaction system, under any semantics, and with any integrity constraints. They use that in their favor, to construct a very strict transaction system, using the Herbrand semantics, and the integrity constraints that only serial executions of transactions lead the transaction system to a state that satisfies the IC.  -->

To get a better intuition of the construction of $$T'$$ in the proof, here follows an example (inspired by the _Figure 1_ in section 4.3 of the paper) of such a transaction system $$T'$$.

Suppose $$T'$$ is a system with one global variable $$x$$ with initial value $$x_0$$, and two transactions:

$$
T_1: x := f_1(x); x := f_2(x) \\
T_2: x := f_3(x)
$$

The set of acceptable final states $$IC = \{ x_0, x_1, x_2, x_{12}, x_{21} \}$$ 
where $$x_1$$ is the value of $$x$$ after executing $$T_1$$, so $$x_1 = f_2(f_1(x_0))$$ (similarly $$x_2 = f_3(x_0)$$) and $$x_{12}$$ is the value of $$x$$ after executing $$T_1; T_2$$, so $$x_1 = f_3(x_1)$$ (similarly $$x_{21} = f_2(f_1(x_2))$$).

Note that for this specific transaction system, the set of serializable schedules is the set of serial schedules, as there is no way to reorder any non serial schedule to give the same results (under Herbarnd semantics) with any serial schedule.

The above theorem shows that given complete syntactic information of the transactions, one can hope to create a scheduler whose fixpoint set $$P$$ is at best equal to $$SR(T)$$, because anything more than that wouldn't be correct for some interpretation and integrity constraints. That is why most approaches to concurrency control (at the time) had serialization as their objective.

<!-- To get a better intuition of the construction of a transaction system T' done in the proof, below follows an example (inspired by the Figure1 in section 4.3 of the paper, but slightly different) of a transaction system T' where: -->

<!-- A system with one global variable x with initial value x0, and two transactions -->
<!-- T1: x := f1(x); x := f2(x) -->
<!-- T2: x := f3(x) -->

<!-- The set of acceptable final states IC = {x0, x1, x2, x12, x21}  -->
<!-- where x1 is the value of x after executing T1 so x1 = f2(f1(x0)), similarly x2 = f3(x0) -->
<!-- and x12 is x after executing T1; T2 so x1 = f3(x1) and similarly x21 = f2(f1(x2)). -->

<!-- Note that for this specific transaction system, the set of serializable schedules is the set of serial schedules, as there is no way to reorder any non serial schedule to give the same results (under Herbarnd semantics) with any serial schedule. -->

<!-- The above theorem shows that given complete syntactic information of the transactions, one can hope to create a scheduler whose P is at most equal to SR(T), because anything more than that wouldn't be correct for some interpretation and integrity constraints. That is why, most approaches to concurrency control (at the time) had serialization as their goal [citations]. -->

In practice, we cannot even expect to get a scheduler with $$P = SR(T)$$, as in [[Papadimitriou 1978](#papadimitriou-1978)] it is shown that serialization is intractable, and for some transaction systems of restricted syntax, it can be _approximated_ by more restrictive schedulers. 

<!-- **QUESTION: How do we find a serializable schedule in the first place???** -->

<!-- In [[Papadimitriou 1978](#papadimitriou-1978)] it is shown that for some transaction systems of restricted syntax, although serialization is intractable (**I guess because all the different serial orderings are exponentially many**), it can be **approximated** by more restrictive schedulers. (See also [Papadimitriou 77]). So in practice, we cannot even expect to get a scheduler with performance P = SR(T). -->

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


<!-- **Optimal Scheduler for Complete semantic information, without integrity constraints** -->

<!-- In the example above, the history h = (T11, T21, T12) is not serializable since its final Herbrand value is not in IC. However, given an interpretation of the functions as f1(x) = x + 1, f2(x) = 2 * x, and f3(x) = 3 * x the history T11, T21, T12 returns the same value for x as the T1;T2 history. This shows, that given semantic information, a serialization scheduler, is not optimal, as we can do better.  -->

<!-- Therefore, they define a generalized notion of serialization as follows: -->

<!-- A schedule h is said to be weakly serializable, if starting from any state E, the execution of the schedule will end with a state that is achievable by some concatenation of transactions, possibly with repetitions and omissions of transactions also starting from state E. This way we extend P to be the set of schedules that lead to a semantically equivalent final state, instead of a syntactically equivalent one (which is semantic equivalence under Herbrand interpretation). -->

<!-- Denote by WSR(T) the set of all weakly serializable schedules of T. It is clear that SR(T) \subseteq WSR(T). The weak serialization scheduler is defined to be S that satisfies: P = WSR(T) and S(H) = P for any T. Similarly to above, it holds that the weak serialization scheduler is optimal among all schedulers using all information (syntactic and semantic) but the integrity constraints.  -->

Note that they don't propose an optimal scheduler that also has access to the integrity constraints.

## Discussion

An important question is how the above results relate to the real performance of a database that uses a specific scheduler. From the perspective of clients that use this database (by issuing transactions to it), the time for executing a transaction can be divided into three parts:

- _Scheduling time:_ This is the time that it takes for the scheduler to make its decision. It mostly depends on the sophistication of the scheduler and the amount of information that it has available.

- _Waiting time:_ The total time that the scheduler delayed executing each transaction step of a transaction, so that it could preserve consistency.

- _Execution time:_ The time that is actually spent in executing each step of the transaction.

The execution time only depends on the transactions, so it can be considered constant, and the scheduling time depends on several factors and they don't address it directly in this paper. Instead, they mostly focus on the waiting time, and they argue that the fixpoint set $$P$$ is a good metric of the waiting time as described [above](#scheduler). 

Another important issue is that there is an implicit assumption that underlies the model, and that is that all the information is available to the scheduler from the start. This implies that the transactions to be executed are fixed and known by the scheduler statically. However, that is not a reasonable assumption as in practice the scheduler would acquire most information (especially the knowledge about which transactions are to be executed) dynamically as the clients make requests. They pinpoint this issue, and suggest it as future work.

It is also very interesting to try and compare other consistency criteria with serializability (and weak serializability). On first sight, it seems like a connection can be found between serializability and linearizability.

In order to compare serializability with linearizability, we need to define the granularity of operations. We can define each transaction step to be an operation, its start time to be the moment that the user issued it for execution, and its end time to be the moment that its execution finished. 

The scheduler then delays executing each transaction step, until it is safe to do so (according to a sequential specification that depends on the information available to the scheduler). The difference of linearizability and serializability can be found in the following. Linearizability means that each possible execution of a system can be reordered to match a sequential execution of the sequential specification of the system. In the case of this paper however, the focus is on reducing the latency (or waiting time) of the system, so the time between the issuing of a transaction step for execution and the end of its actual execution. Therefore for each operation (transaction step) we have a start time and a lower bound for its end time, which corresponds to the sum of its start time and its execution time. The scheduler chooses an appropriate end time so that the execution is linearizable to one execution of the sequential specification. So the scheduler always produces linearizable executions (as it drags the end time until it is safe to execute its operation). 

So a scheduler in the setting of this paper actually tries to produce the 

ΣΗΜΕΙΩΣΗ 2: Πρακτικά στον Παπαδημητρίου ερευνούν τι γίνεται αν έχεις όλο και πιο καλό sequential specification και πιο refined. Χωρίς καθόλου ππληροφορία το sequential specification που έχεις είναι ότι επιτρέπεις μόνο sequential executions από transactions. Άρα ο scheduler παράγει πολύ μικρό υποσύνολο των πραγματικών correct schedules (τα οποία μπορούν να οριστούν με ένα complete specification των syntax, semantics, integrity constraints). Αν ο scheduler δει και συντακτική πληροφορία, μπορεί να δει μεγαλύτερο κομμάτι των correct schedules. Με όλο περισσότερη πληροφορία βλέπει και μεγαλύτερο κομμάτι των correct schedules. Αντίθετα, στο paper των Attiya & Welch, ψάχνουν για lower bounds (negative impossiblity results) για άπειρη πληροφορία για τα transactions (αλλά με άλλα constraints όπως τον ασυγχρονισμο ρολογιων κτλ).


<hr>



- The performance of a scheduler from a user's perspective
  
- Static vs Dynamic information

- What they leave as future work, to establish the optimality of an assertion based scheduler

- Similarity of serializability with linearizability and sequential consistency

- H analogia ths douleias se auto to paper me to refinement tou sequential specification



**NOTE:** (Κάποια από αυτά αξίζει να μπουν στο ποστ και άλλα στα notes mou.)

To serializability eiani similar με το sequential consistency. Γενικά είναι λίγο ιδιαίτερο αυτό το θέμα, επειδή για να οριστεί καν το linearizability τπρέπει να οριστεί ένα granularity operations, και τι σημαίνει πως ένα operation ολοκληρώνεται πριν αρχίσει ένα άλλο. 

Επειδή δεν υπάρχουν responses στο μοντέλο του Παπαδημητρίου, και όλα τα transaction steps απλά εισέρχονται στο σύστημα, πρέπει να αναδιαμορφώσουμε τους ορισμούς. Οι schedulers στον Παπαδημητρίου έχουν στόχο να βρουν ένα sequentially consistent scheduling των operations που έρχονται. Παρόλαυτα αν θεωρήσουμε πως τα operations είναι τα transactions και όχι τα transaction steps, και το μήκος τους είναι η χρονική περίοδος μέχρι να εκτελεστεί ένα transaaction, τότε οι schedulers του Παπαδημητρίου ψάχνουν για linearizable scheuling, αφού δεν πρόκειται να αλλάξουν την σειρά δύο ολοκληρωμένων operations, afou mporoun apla na kanoun execute to prwto kai meta to deutero (apo to definition oti kathe transaction apo mono tou einai correct). 

**Εναλλακτικά αν θεωρήσουμε πως το ενα operation είναι ένα transaction step, και το σύστημα απαντάει όταν τελειώσει το transaction step, αυτό το definition δεν είναι πολύ comparable με αυτό των Attiya and Welch για παράδειγμα, επειδή εκεί ένας user δεν μπορεί να κάνει queue (pipeline) τα requests του, ενώ εδώ γίνεται. Αντίθετα ένας user δεν μπορεί να κάνει pipeline transactions και πρέπει να περιμένει μέχρι να τελειώσει το πρώτο του για να κάνει κάποιο άλλο. 

To issue ofeiletai sto exhs. Πρακτικά οταν μιλαμε για linearizability και sequential consistency θελουμε ενα συστημα, που οτι τιμες και να επιστρεψει σε καθε operation, αυτές να μπορούν να εξηγηθούν με ενα linearizable h sc reorderign αυτων. Στην περίπτωση του Παπαδημητριου όμως, το σύστημα δεν επιστρέφει κάποια απάντηση, οπότε οποιοδήποτε input schedule είναι και linearizable (kai sequentially consistent). Αυτό που μας ενδιαφέρει στον Παπαδημητρίου είναι να μειώσουμε όσο μπορούμε το latency του κάθε transaction, δηλαδή τον χρόνο από τον οποίο έρχεται το πρώτο transaction step να εκτελεστεί μέχρι τον χρόνο που πραγματικά εκτελείται το τελευταίο transaction step. Για κάθε transaction λοιπόν έχουμε το start time του (ή βασικά ένα oredring τους) (το οποίο είναι η στιγμή που έρχεται για execution το πρώτο transaction step) και ένα ελάχιστο όριο για το end time του (τη στιγμή που έρχεται για execution το τελευταίο transaction step). Έχουμε δηλαδή ήδη ελάχιστες περιόδους για to κάθε operation (transaction). Είναι ξεκάθαρο ότι αν τα καθυστερήσουμε όλα έτσι ώστε να τα έκτελέσουμε ένα ένα, το τελευταίο θα κάνει overlap με πάρα πολλά από αυτα (για την ακρίβεια με όσα δεν τέλειωσαν πριν αυτό ξεκινήσει), και προφανώς είναι linearizable οποιδήποτε reordering τους. Οπότε πραγματικά στον Παπαδημητρίου ψάχνουν για linearizable, και όχι sequentially consistent ordering γιατί βασικά ποτέ δεν θα είχε νόημα να κάνουν reorder δυο transactions (αφού όλα κάνουν commute μεταξύ τους). 

Άρα το point είναι ότι στον Παπαδημητρίου το linearizability κάνει reduce σε sequential consistency γιατι πραγματικά τα transactions κάνουν commute (με κάθε έννοια observation (είτε οι απαντήσεις τους που είναι όλες ίδιες) είτε το τελικό global state που είναι πάντα consistent (άρα και ικανοποιεί το sequential specification)). Σε ένα τέτοιο setting (κυνηγώντας το performance, δεν θα έιχε ποτέ νόημα κάποιος να κάνει reorder δύο operations που το ένα τέλειωσε πριν αρχίσει το άλλο, γιατί όπως και να τα κάνει order, ικανοποιεί το specification, και αν τα κάνει order αλλιώς καθυστερεί τσάμπα τo πρώτο transaction που έτσι και αλλιώς τέλειωσε πριν το άλλο 

ΣΗΜΕΊΩΣΗ: Υπάρχουν διάφορες μικρές λεπτομέρειες που δεν καταλαβίνω ακόμα που έχουν να κάνουν με το ordering, και το response time, γιατι στον Παπαδημητρίπυ τα responses δεν είναι καλά ορισμένα, οπότε πρέπει να καταλάβω τι σημαίνουν με οτν δικό μου ορισμό, και τι σημαίνει να ολοκληρωθεί ένα transaction πριν από ένα άλλο.

ΣΗΜΕΙΩΣΗ 2: Πρακτικά στον Παπαδημητρίου ερευνούν τι γίνεται αν έχεις όλο και πιο καλό sequential specification και πιο refined. Χωρίς καθόλου ππληροφορία το sequential specification που έχεις είναι ότι επιτρέπεις μόνο sequential executions από transactions. Άρα ο scheduler παράγει πολύ μικρό υποσύνολο των πραγματικών correct schedules (τα οποία μπορούν να οριστούν με ένα complete specification των syntax, semantics, integrity constraints). Αν ο scheduler δει και συντακτική πληροφορία, μπορεί να δει μεγαλύτερο κομμάτι των correct schedules. Με όλο περισσότερη πληροφορία βλέπει και μεγαλύτερο κομμάτι των correct schedules. Αντίθετα, στο paper των Attiya & Welch, ψάχνουν για lower bounds (negative impossiblity results) για άπειρη πληροφορία για τα transactions (αλλά με άλλα constraints όπως τον ασυγχρονισμο ρολογιων κτλ).

<hr>

### Bibliography

<a name="bernstein-1978">[Bernstein et al. 78]</a>: P.A. Bernstein , N. Goodman, J.B. Rothnie, and C.H. Papadimitriou. 1978. A System of Distributed Databases (the Fully Redundant Case).

<a name="kung-papadimitriou-1978">[Kung & Papadimitriou 78]</a>: H.T. Kung and C.H. Papadimitriou. 1978. An optimality theory of concurrency control for databases.

<a name="manna-1974">[Manna 74]</a>: Z. Manna. 1974. Mathematical Theory of Computation

<a name="papadimitriou-1978">[Papadimitriou 78]</a>: C.H. Papadimitriou. 1978. Serializability of Concurrent Updates.
