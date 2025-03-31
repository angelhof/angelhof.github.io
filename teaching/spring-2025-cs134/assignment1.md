---
layout: default
overview: true
---

<h2 class="page-heading"><a href="/teaching/distributed-systems.html">CS 134: Distributed Systems</a> -- Assignment 1: MapReduce </h2>

<h3 class="page-heading">Due date: Friday April 11, 10pm</h3>

<!-- For questions, come to discussion sections on Fridays and post questions on <a href="https://piazza.com/ucla/spring2025/cs134">Piazza</a>. -->

<hr>

<h3 class="page-heading">Introduction</h3>


<p class="homepage">
In this assignment (which will be completed individually), you'll build a MapReduce library as a way to learn the Go programming language and as a way to learn about fault tolerance in distributed systems. In the first part you will write a simple MapReduce program. In the second part you will write a Master that hands out jobs to workers, and handles failures of workers. The interface to the library and the approach to fault tolerance is similar to the one described in the original <a href="http://research.google.com/archive/mapreduce-osdi04.pdf">MapReduce paper</a>. 
</p>


<h3 class="page-heading">Collaboration Policy</h3>


<p class="homepage">
You must write all the code you hand in for CS134, except for code that we give you as part of the assignment. You may discuss clarifications about the assignments with other students, but you may not discuss solutions or look at or copy each others' code. Please do not publish your code or make it available to future CS134 students -- for example, please do not make your code visible on GitHub. 
</p>

<h3 class="page-heading">Setting up the requirements</h3>

<p class="homepage">
<ul id="requirements" style="list-style-type:disc;">
    <li>
        Install Go: You'll implement this assignment (and all the other assignments) in <a href="http://www.golang.org/">Go</a>. The Go website contains lots of tutorial information which you may want to look at. You can find the installation instructions <a href="https://golang.org/doc/install">here</a>.
    </li>
    <li> Install the GoLand IDE (optional but highy encouraged): You can use whichever IDE/editor you prefer, but the Goland IDE is very useful and can be found <a href="https://www.jetbrains.com/go/">here</a> and it is free if you provide student identification.
    </li>
    <li>
        Install Git: We supply you with a non-distributed MapReduce implementation, and a partial implementation of a distributed implementation (skeleton code with utility components). You'll fetch the initial implementations with <a href="http://git.or.cz/">git</a> (a version control system). To learn more about git, look at the <a href="http://www.kernel.org/pub/software/scm/git/docs/user-manual.html">git user's manual</a>, or, if you are already familiar with other version control systems, you may find this <a href="http://eagain.net/articles/git-for-computer-scientists/">CS-oriented overview of git</a> useful.
    </li>
    <li>
    <p>
            Setup a private Git repository:
            To start this assignment,
            you should duplicate the (public) assignment 1 git repository into
            a private repository of your own.
            The assignment 1 repository can be found here:
            <a href="https://github.com/ucla-progsoftsys/cs134-assignment1-skeleton">
                <i>ucla-progsoftsys/assignment1-skeleton</i>
            </a>.
            Your own private copy of the assignment 1 repository is called a mirror repository.
            Each individual student should have their own private mirror repository where
            they commit their changes.
        </p>
        <ol>
        <li>First, you should create a new <strong>private</strong> repository on GitHub.
            Let's assume the name of this repository is <i>assignment1</i>. Also, replace
            ${USER_NAME} with your GitHub user name while running the following commands.</li>
        <li>Next, create a bare mirrored clone of <i>ucla-progsoftsys/assignment1-skeleton</i> repository.
<pre>$ git clone --mirror git@github.com:ucla-progsoftsys/assignment1-skeleton.git</pre>
        </li>
        <li>Then, you should mirror-push to the new repository, in 
addition to setting the push location to your private repository:
<pre>
$ cd assignment1-skeleton.git
$ git push --mirror git@github.com:${USER_NAME}/assignment1.git
$ git remote set-url --push origin git@github.com:${USER_NAME}/assignment1.git
</pre>
        </li>
        <li>To finish this step, remove the temporary local repository you created in the second step:
<pre>
$ cd ..
$ git clone git@github.com:${USER_NAME}/assignment1.git
$ rm -rf assignment1-skeleton.git
$ cd assignment1/
$ git remote -v
origin  git@github.com:${USER_NAME}/assignment1.git (fetch)
origin  git@github.com:${USER_NAME}/assignment1.git (push)
</pre>
        </li>
        </ol>
        <p>
        Now you have your own copy of the original <i>ucla-progsoftsys/assignment1-skeleton</i> repository. 
        </p>
        <p>
            Git allows you to keep track of the changes you make to the code.
            For example, if you want to checkpoint your progress, you can <emph>commit</emph> and <emph>push</emph> your changes
            by running:
        </p>
<pre>
# make some changes
$ git status
$ git commit -am 'Added partial solution to assignment 1'
$ git push
</pre>
<p></p>
</li>
</ul>
</p>


<h3 class="page-heading">Getting started</h3>


<p class="homepage">
There is an input file <tt>kjv12.txt</tt> in <i>src/main</i>, which was downloaded from
    <a href="https://web.archive.org/web/20130530223318/http://patriot.net/~bmcgin/kjv12.txt">here</a>.
    Assuming you are in the assignment1 directory,
    compile the initial code we provide you and run it with the downloaded input file:
    <mark>
    </mark>
</p>
<pre>
$ cd main
$ go run wc.go master kjv12.txt sequential
# command-line-arguments
./wc.go:15:1: missing return
./wc.go:21:1: missing return
</pre>
<p class="homepage">
    The compiler produces two errors, because the implementation of the
    <tt>Map()</tt> and <tt>Reduce()</tt> functions are incomplete.
</p>

<h3 class="page-heading">Part I: Word Count</h3>
<p>
Modify <tt>Map()</tt> and <tt>Reduce()</tt> functions so that <tt>wc.go</tt> reports the     number of occurrences of each word in alphabetical order.
</p>

<p>
    Before you start coding read Section 2 of the
    <a href="http://research.google.com/archive/mapreduce-osdi04.pdf">MapReduce paper</a>.
    Your <tt>Map()</tt> and <tt>Reduce()</tt> functions
    will differ a bit from those in the paper's Section 2.1. Your <tt>Map()</tt>
    will be passed some of the text from the file; it should split it
    into words, and return a <tt>list.List</tt> of key/value
    pairs, of type <tt>mapreduce.KeyValue</tt>. Your <tt>Reduce()</tt> will be
    called once for each key, with a list of all the values generated
    by <tt>Map()</tt> for that key; it should return a single output value.
</p>
<p>
    It will help to read
    our code for mapreduce, which is in <tt>mapreduce.go</tt> in
    package <tt>mapreduce</tt>. Look at
    <tt>RunSingle()</tt> and the functions it calls.
    This well help you to
    understand what MapReduce does and to learn Go by example.
</p>
<p>
    Once you understand this code, implement <tt>Map()</tt> and <tt>Reduce()</tt> in
    <tt>wc.go</tt>.
</p>

<p>
    After you finish implementing the <tt>Map()</tt> and <tt>Reduce()</tt> functions, your command line output should be similar to the following:
    </p>
<pre>
$ go run wc.go master kjv12.txt sequential
Split kjv12.txt
Split read 4834757
DoMap: read split mrtmp.kjv12.txt-0 966954
DoMap: read split mrtmp.kjv12.txt-1 966953
DoMap: read split mrtmp.kjv12.txt-2 966951
DoMap: read split mrtmp.kjv12.txt-3 966955
DoMap: read split mrtmp.kjv12.txt-4 966944
DoReduce: read mrtmp.kjv12.txt-0-0
DoReduce: read mrtmp.kjv12.txt-1-0
DoReduce: read mrtmp.kjv12.txt-2-0
DoReduce: read mrtmp.kjv12.txt-3-0
DoReduce: read mrtmp.kjv12.txt-4-0
DoReduce: read mrtmp.kjv12.txt-0-1
DoReduce: read mrtmp.kjv12.txt-1-1
DoReduce: read mrtmp.kjv12.txt-2-1
DoReduce: read mrtmp.kjv12.txt-3-1
DoReduce: read mrtmp.kjv12.txt-4-1
DoReduce: read mrtmp.kjv12.txt-0-2
DoReduce: read mrtmp.kjv12.txt-1-2
DoReduce: read mrtmp.kjv12.txt-2-2
DoReduce: read mrtmp.kjv12.txt-3-2
DoReduce: read mrtmp.kjv12.txt-4-2
Merge phaseMerge: read mrtmp.kjv12.txt-res-0
Merge: read mrtmp.kjv12.txt-res-1
Merge: read mrtmp.kjv12.txt-res-2
</pre>

<p>
    The actual output of the word count program will be in the file "mrtmp.kjv12.txt".
    Your implementation is correct if the following command produces the following top 10 words:
    </p><pre>
$ sort -n -k2 mrtmp.kjv12.txt | tail -10
unto: 8940
he: 9666
shall: 9760
in: 12334
that: 12577
And: 12846
to: 13384
of: 34434
and: 38850
the: 62075
</pre>

<p>
    To make testing easy for you, run:
    </p><pre>$ sh ./test-wc.sh</pre>
<p>
    and it will report if your solution is correct or not.
</p>

<p>
    Hint: you can use
    <a href="http://golang.org/pkg/strings/#FieldsFunc"><tt>strings.FieldsFunc</tt></a>
    to split a string into components.
</p>
<p>
    Hint: for the purposes of this exercise, you can consider a word to be
    any contiguous sequence of letters, as determined by
    <a href="http://golang.org/pkg/unicode/#IsLetter"><tt>unicode.IsLetter</tt></a>.
    A good read on what strings are in Go is the
    <a href="http://blog.golang.org/strings">Go Blog on strings</a>.
</p>

<p>
    Hint: the <a href="http://golang.org/pkg/strconv/">strconv package</a> is handy to
    convert strings to integers etc.
</p>

<p>
    You can remove the output file and all intermediate files with:
    </p><pre>$ rm mrtmp.*</pre>
<p></p>

<h3 class="page-heading">Part II: Distributing MapReduce jobs</h3>

<p>
    In this part you will complete a version of mapreduce that splits the
    work up over a set of worker threads, in order to exploit multiple
    cores. A master thread hands out work to the workers and waits for
    them to finish. The master should communicate with the workers via
    RPC. We give you the worker code (<tt>mapreduce/worker.go</tt>), the
    code that starts the workers, and code to deal with RPC messages
    (<tt>mapreduce/common.go</tt>).
</p>
<p>
    Your job is to complete <tt>master.go</tt> in the <tt>mapreduce</tt>
    package.  In particular, you should modify <tt>RunMaster()</tt> in
    <tt>master.go</tt> to hand out the map and reduce jobs to workers,
    and return only when all the jobs have finished.
</p>
<p>
    Look at <tt>Run()</tt> in <tt>mapreduce.go</tt>. It calls <tt>Split()</tt> to
    split the input into per-map-job files, then calls
    your <tt>RunMaster()</tt> to run the map and reduce jobs, then
    calls <tt>Merge()</tt> to assemble the per-reduce-job outputs into a
    single output file. <tt>RunMaster()</tt> only needs to tell the workers
    the name of the original input file (<tt>mr.file</tt>) and the job
    number; each worker knows from which files to read its input and to
    which files to write its output.
</p>
<p>
    Each worker sends a Register RPC to the master when it starts.
    <tt>mapreduce.go</tt> already implements the master's
    <tt>MapReduce.Register</tt> RPC handler for you, and passes the new
    worker's information to <tt>mr.registerChannel</tt>.  Your <tt>RunMaster</tt>
    should process new worker registrations by reading from this channel.
</p>
<p>
    Information about the MapReduce job is in the <tt>MapReduce</tt> struct,
    defined in <tt>mapreduce.go</tt>.  Modify the <tt>MapReduce</tt> struct to
    keep track of any additional state (e.g. the set of available workers),
    and initialize this additional state in the <tt>InitMapReduce()</tt>
    function.  The master does not need to know which Map or Reduce functions
    are being used for the job; the workers will take care of executing the
    right code for Map or Reduce.
</p>
<p>
    You should run your code using Go's unit test system. We supply you
    with a set of tests in <tt>test_test.go</tt>. You run unit tests in a
    package directory (e.g. the mapreduce directory) through GoLand (suggested) or as follows:
    </p>
<pre>
$ cd ../mapreduce
$ go test
</pre>
<p></p>
<p>
    The master should send RPCs to the workers in parallel so that the workers
    can work on jobs concurrently.  You will find the <tt>go</tt> statement useful
    for this purpose and the <a href="http://golang.org/pkg/net/rpc/">Go RPC documentation</a>.
</p>
<p>
    The master may have to wait for a worker to finish before it can hand out
    more jobs.  You may find channels useful to synchronize threads that are waiting
    for reply with the master once the reply arrives.  Channels are explained in the
    document on <a href="http://golang.org/doc/effective_go.html#concurrency">Concurrency in Go</a>.
</p>
<p>
    The easiest way to track down bugs is to insert log.Printf()
    statements, collect the output in a file with <tt>go test &gt;
    out</tt>, and then think about whether the output matches your
    understanding of how your code should behave. The last step (thinking)
    is the most important.
</p>
<p>
    The code we give you runs the workers as threads within a single UNIX
    process, and can exploit multiple cores on a single machine. Some
    modifications would be needed in order to run the workers on multiple
    machines communicating over a network. The RPCs would have to use TCP
    rather than UNIX-domain sockets; there would need to be a way to start
    worker processes on all the machines; and all the machines would have
    to share storage through some kind of network file system.
</p>
<p>
    You are done with Part II when your implementation passes the first test (the
    "Basic mapreduce" test) in <tt>test_test.go</tt> in the <tt>mapreduce</tt>
    package. You don't yet have to worry about failures of workers.
</p>

<h3 class="page-heading">Part III: Handling worker failures</h3>

<p>
    In this part you will make the master handle failed workers.
    MapReduce makes this relatively easy
    because workers don't have persistent state.  If a
    worker fails, any RPCs that the master issued to that worker will fail
    (e.g. due to a timeout).  Thus, if the master's RPC to the worker fails,
    the master should re-assign the job given to the failed worker to another worker.
</p>
<p>
    An RPC failure doesn't necessarily mean that the worker failed; the worker
    may just be unreachable but still computing.  Thus, it may happen that two
    workers receive the same job and compute it.  However, because jobs are
    idempotent, it doesn't matter if the same job is computed twice---both times it
    will generate the same output.  So, you don't have to do anything special for this
    case. (Our tests never fail workers in the middle of job, so you don't even have
    to worry about several workers writing to the same output file.)
</p>
<p>
    You don't have to handle failures of the master; we will assume it won't
    fail. Making the master fault-tolerant is more difficult because it keeps
    persistent state that would have to be recovered in order to resume
    operations after a master failure.
    Much of the later assignments are devoted to this challenge.
</p>
<p>
    Your implementation must pass the two remaining test cases in
    <tt>test_test.go</tt>. The first test case tests the failure of one worker.  The
    second test case tests handling of many failures of workers. Periodically, the
    test cases start new workers that the master can use to make forward progress,
    but these workers fail after handling a few jobs.
</p>

<h3>Assignment Submission</h3>
<p>
To submit the assignment, use Gradescope.    
You will receive full credit if your code passes the <tt>test_test.go</tt> tests when we run it.
<strong>Remember that late days cannot be used for this assignment.</strong>
</p>


<!-- Due date: Friday April 11, 10pm -->
    