---
layout: default
overview: true
---

<h2 class="page-heading"><a href="/teaching/distributed-systems.html">CS 134: Distributed Systems</a> -- Assignment 1: MapReduce </h2>

<h3 class="page-heading">Due date: Friday April 10, 2026, 10pm</h3>

<hr>

<h3 class="page-heading">Introduction</h3>

<p class="homepage">
In this assignment (which will be completed individually), you'll build a MapReduce library as a way to learn the Go programming language and as a way to learn about fault tolerance in distributed systems. In the first part you will write a simple MapReduce program. In the second part you will write the distributed MapReduce logic (map and reduce task execution), plus a Master that hands out jobs to workers and handles failures of workers. The interface to the library and the approach to fault tolerance is similar to the one described in the original <a href="https://research.google.com/archive/mapreduce-osdi04.pdf">MapReduce paper</a>.
</p>

<h3 class="page-heading">Collaboration Policy</h3>

<p class="homepage">
You must write all the code you hand in for CS134, except for code that we give you as part of the assignment. You may discuss clarifications about the assignments with other students, but you may not discuss solutions or look at or copy each others' code. Please do not publish your code or make it available to future CS134 students -- for example, please do not make your code visible on GitHub. Please see the main class homepage for information about the use of AI.
</p>

<h3 class="page-heading">Revamped Assignment Notes</h3>

<p class="homepage">
This assignment has been revamped following feedback from last year. As a result, please be patient with us as we work out any unexpected skeleton code and test case bugs, ambiguous guidelines, or unclear instructions. If you find anything that seems off, incorrect, wrong, unclear, or otherwise needs more clarification, please do not hesitate to contact us via Piazza, office hours, discussion, or lecture!
</p>

<h3 class="page-heading">Setting up the requirements</h3>

<div>
<ul id="requirements" style="list-style-type:disc;">
    <li>
        Install the latest version of Go: You'll implement this assignment (and all the other assignments) in <a href="https://go.dev/dl/">Go</a>. The Go website contains lots of tutorial information which you may want to look at. You can find the installation instructions <a href="https://go.dev/doc/install">here</a>.
    </li>
    <li>Install an IDE/IDE extension of your choice: Some options are the GoLand IDE and the Go extension for VSCode.</li>
    <li>
        Install Git: We supply you with skeleton code with utility components. You'll fetch the initial implementations with <a href="https://git-scm.com/">git</a> (a version control system). You should already be familiar with git from CS 35L, but in case you've forgotten, you can look at the <a href="https://git-scm.com/docs/user-manual">git user's manual</a> or you may find this <a href="https://eagain.net/articles/git-for-computer-scientists/">CS-oriented overview of git</a> useful.
    </li>
    <li>
    <p>
            Setup a private Git repository:
            To start this assignment,
            you should duplicate the (public) assignment 1 git repository into
            a private repository of your own.
            The assignment 1 repository can be found here:
            <a href="https://github.com/ucla-progsoftsys/cs134-assignment1-skeleton">
                <em>ucla-progsoftsys/cs134-assignment1-skeleton</em>
            </a>.
            Your own private copy of the assignment 1 repository is called a mirror repository.
            Each individual student should have their own private mirror repository where
            they commit their changes.
        </p>
        <ol>
        <li>First, you should create a new <strong>private</strong> repository on GitHub. You should <strong>not</strong> store any solution code in public, since this is considered code sharing.
            Let's assume the name of this repository is <em>assignment1</em>. Also, replace
            ${USER_NAME} with your GitHub user name while running the following commands.</li>
        <li>Next, create a bare mirrored clone of <em>ucla-progsoftsys/cs134-assignment1-skeleton</em> repository.
<pre>$ git clone --mirror git@github.com:ucla-progsoftsys/cs134-assignment1-skeleton.git</pre>
        </li>
        <li>Then, you should mirror-push to the new repository, in
addition to setting the push location to your private repository:
<pre>
$ cd cs134-assignment1-skeleton.git
$ git push --mirror git@github.com:${USER_NAME}/assignment1.git
$ git remote set-url --push origin git@github.com:${USER_NAME}/assignment1.git
</pre>
        </li>
        <li>To finish this step, remove the temporary local repository you created in the second step:
<pre>
$ cd ..
$ git clone git@github.com:${USER_NAME}/assignment1.git
$ rm -rf cs134-assignment1-skeleton.git
$ cd assignment1/
$ git remote -v
origin  git@github.com:${USER_NAME}/assignment1.git (fetch)
origin  git@github.com:${USER_NAME}/assignment1.git (push)
</pre>
        </li>
        </ol>
        <p>
        Now you have your own copy of the original <em>ucla-progsoftsys/cs134-assignment1-skeleton</em> repository.
        </p>
        <p>
            Git allows you to keep track of the changes you make to the code.
            For example, if you want to checkpoint your progress, you can <em>commit</em> and <em>push</em> your changes
            by running:
        </p>
<pre>
# make some changes
$ git status
$ git commit -am 'Added partial solution to assignment 1'
$ git push
</pre>
</li>
</ul>
</div>

<h3 class="page-heading">Project Structure</h3>

<p class="homepage">
The repository is organized into two directories:
</p>
<ul>
    <li>
        <tt>sequential/</tt> &mdash; A standalone sequential word count program using the MapReduce pattern. This is where you'll work on Part I.
        Contains <tt>wc.go</tt> (your code), <tt>wc_test.go</tt> (test cases), and <tt>kjv12.txt</tt> (sample input).
    </li>
    <li>
        <tt>distributed/</tt> &mdash; A distributed MapReduce framework. This is where you'll work on Parts II and III.
        <ul>
            <li><tt>mapreduce/</tt> &mdash; The MapReduce library: <tt>mapreduce.go</tt> (framework and helpers), <tt>master.go</tt> (your code for the master), <tt>worker.go</tt> (worker implementation, do not modify), <tt>common.go</tt> (shared types and RPC helpers), and <tt>test_test.go</tt> (test cases).</li>
            <li><tt>main/wc.go</tt> &mdash; A driver program for running the distributed MapReduce manually (optional).</li>
        </ul>
    </li>
</ul>

<h3 class="page-heading">Part I: Sequential Word Count</h3>

<p>
In this part, you will implement a simple word count program using the MapReduce pattern to understand the overall Map and Reduce paradigms before moving to the distributed version,
all running sequentially. You will work in the <tt>sequential/</tt> directory.
</p>

<p>
    Before you start coding, read Section 2 of the
    <a href="https://research.google.com/archive/mapreduce-osdi04.pdf">MapReduce paper</a>.
    Your <tt>Map()</tt> and <tt>Reduce()</tt> functions
    will differ a bit from those in the paper's Section 2.1. Your <tt>Map()</tt>
    will be passed the entire file content as a single string value; it should split it
    into words, and return a <tt>list.List</tt> of key/value
    pairs, of type <tt>KeyValue</tt>. Your <tt>Reduce()</tt> will be
    called once for each unique key, with a list of all the values generated
    by <tt>Map()</tt> for that key; it should return a single output string.
</p>

<p>
    Open <tt>sequential/wc.go</tt> and implement the three functions marked with
    <tt>// Your code here</tt>:
</p>

<p>
    You can test your implementation by running:
</p>
<pre>
$ cd sequential
$ go test -v
=== RUN   TestPartI_MapSmallInput
--- PASS: TestPartI_MapSmallInput (0.00s)
=== RUN   TestPartI_ReduceSmallInput
--- PASS: TestPartI_ReduceSmallInput (0.00s)
=== RUN   TestPartI_DoMapReduceSmallInput
--- PASS: TestPartI_DoMapReduceSmallInput (0.00s)
=== RUN   TestPartI_DoMapReduceKJV12Input
--- PASS: TestPartI_DoMapReduceKJV12Input (0.17s)
=== RUN   TestPartI_MapRandomInput
--- PASS: TestPartI_MapRandomInput (0.41s)
=== RUN   TestPartI_ReduceRandomInput
--- PASS: TestPartI_ReduceRandomInput (0.00s)
=== RUN   TestPartI_DoMapReduceRandomInput
--- PASS: TestPartI_DoMapReduceRandomInput (0.07s)
=== RUN   TestPartI_DoMapReduceSingleWord
--- PASS: TestPartI_DoMapReduceSingleWord (0.00s)
=== RUN   TestPartI_DoMapReduceCaseSensitive
--- PASS: TestPartI_DoMapReduceCaseSensitive (0.00s)
=== RUN   TestPartI_MapWhitespaceOnly
--- PASS: TestPartI_MapWhitespaceOnly (0.00s)
=== RUN   TestPartI_ReduceSingleValue
--- PASS: TestPartI_ReduceSingleValue (0.00s)
=== RUN   TestPartI_MapNoLetters
--- PASS: TestPartI_MapNoLetters (0.00s)
PASS
ok      cs134-assignment1-sequential    0.834s
</pre>
<p>
    All tests should pass. You can also run the program directly:
</p>
<pre>
$ go run wc.go kjv12.txt
</pre>

<p>
    Hint: you can use
    <a href="https://pkg.go.dev/strings#FieldsFunc"><tt>strings.FieldsFunc</tt></a>
    to split a string into components.
</p>

<p>
    Hint: for the purposes of this exercise, you can consider a word to be
    any contiguous sequence of letters, as determined by
    <a href="https://pkg.go.dev/unicode#IsLetter"><tt>unicode.IsLetter</tt></a>.
    A good read on what strings are in Go is the
    <a href="https://go.dev/blog/strings">Go Blog on strings</a>.
</p>

<p>
    Hint: the <a href="https://pkg.go.dev/strconv">strconv package</a> is handy to
    convert strings to integers etc.
</p>

<p>
    Hint: use the test cases to understand what you are being tested! They can give
    helpful examples on how functions are called and what the expected return values for those calls are.
</p>

<h3 class="page-heading">Part II: Distributing MapReduce jobs</h3>

<p>
    In this part you will complete a version of MapReduce that splits the
    work up over a set of worker threads, in order to exploit multiple
    cores. You will work in the <tt>distributed/</tt> directory. A master thread hands out work to the workers and waits for
    them to finish. The master communicates with the workers via
    RPC, but results are passed via the file system. We give you the worker code (<tt>mapreduce/worker.go</tt>), the
    code that starts the workers, and code to deal with RPC messages
    (<tt>mapreduce/common.go</tt>).
</p>

<p>
    Tip for Part II + Part III: DPrintf is provided as a debug print function.
    Use this function in your code to print out debugging information. On run,
    set Debug = 1 to see all output, or set Debug = 0 in mapreduce.go to hide the output.
</p>

<p>
    There are two sub-tasks in this part:
</p>

<h4>Part II-A: Implement Worker logic</h4>

<p>
    First, implement <tt>DoMap()</tt> and <tt>DoReduce()</tt> in
    <tt>mapreduce/mapreduce.go</tt>. These functions are
    called with the appropriate arguments when the master does
    <tt>call(workerAddress, "Worker.DoJob", ...)</tt>,
    and each one executes to completion a single map or reduce task.
</p>

<p>
    <tt>DoMap()</tt> should read its assigned input split (use <tt>MapName()</tt> to get the filename),
    call the user-supplied <tt>Map</tt> function on the contents, and partition the resulting
    key-value pairs across <tt>nreduce</tt> intermediate files (use <tt>ReduceName()</tt>).
    Use the provided <tt>openPairsFile()</tt>, <tt>appendPairsFilePair()</tt>, and <tt>closePairsFile()</tt>
    helper functions to write key-value pairs to intermediate files.
</p>

<p>
    <tt>DoReduce()</tt> should read the intermediate files produced by all map tasks for its reduce
    partition, group values by key, call the user-supplied <tt>Reduce</tt>
    function for each key, and write the results to the merge output file (use <tt>MergeName()</tt>).
    The keys in the output should be sorted. You can just use <a href="https://pkg.go.dev/sort#Strings">sort.Strings</a> to handle the sorting.
    Use <tt>readFilePairs()</tt> to read intermediate files and the pairs file helpers to write output.
</p>

<p>
    We provide two tests in <tt>distributed/mapreduce/test_test.go</tt> that target only Part II-A logic:
    <tt>TestPartIIA_DoMapPartitioning</tt> and <tt>TestPartIIA_DoReduceAggregatesAndSorts</tt>.
</p>

<pre>
$ cd distributed/mapreduce
$ go test -v -run PartIIA
=== RUN   TestPartIIA_DoMapPartitioning
--- PASS: TestPartIIA_DoMapPartitioning (0.01s)
=== RUN   TestPartIIA_DoReduceAggregatesAndSorts
--- PASS: TestPartIIA_DoReduceAggregatesAndSorts (0.00s)
PASS
ok      cs134-assignment1/mapreduce     0.226s
alec:mapreduce % 
</pre>

<h4>Part II-B: Implement Master</h4>

<p>
    Next, complete <tt>RunMaster()</tt> in
    <tt>mapreduce/master.go</tt> to hand out the map and reduce jobs to workers,
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
    worker's information to <tt>mr.registerChannel</tt>. Your <tt>RunMaster</tt>
    should process new worker registrations by reading from this channel.
</p>

<p>
    <strong>How to use RPC/<tt>call()</tt>:</strong>
    RPC lets one process call a method running in another process (or on another machine)
    using request/reply semantics similar to a normal function call.
    In this assignment, the function you are calling over RPC is already defined for you (Worker.DoJob)
    For this and future assignments, the helper function signature to actually make an RPC call is as follows:
    <tt>call(srv, rpcname, args, reply) bool</tt>.
</p>

<ul>
    <li><tt>srv</tt> is the address of the server you are trying to contact.</li>
    <li><tt>rpcname</tt> is a string of the receiver and method name, for example <tt>"Worker.DoJob"</tt>.</li>
    <li><tt>args</tt> is a struct value containing the call arguments.</li>
    <li><tt>reply</tt> must be a pointer to a struct that is filled by the RPC handler.</li>
</ul>

<p>
    The returned <tt>bool</tt> indicates whether the RPC call completed and returned a response.
    If the return value is false, do not read fields from <tt>reply</tt>.
</p>

<pre>
// Arguments are specified in the struct as defined in common.go
args := &DoJobArgs{
    File: "kjv12.txt",
    Operation: Map,
    JobNumber: 3,
    NumOtherPhase: 50,
}

// Create an empty reply struct; the worker fills it in.
reply := DoJobReply{}

// This call blocks until the RPC returns or fails.
ok := call(workerAddr, "Worker.DoJob", args, &reply)

if ok {
    // RPC reached the worker; now read reply fields such as reply.OK.
} else {
    // Worker unreachable or RPC failed; reassign the job.
}
</pre>

<p>
    For a <tt>Reduce</tt> job, construct the args the same way except use
    <tt>Operation: Reduce</tt> and set <tt>NumOtherPhase: mr.nMap</tt>
    (because each reduce task reads one intermediate file from each map task).
    In this assignment's <tt>DoJobReply</tt>, the returned value to read is
    <tt>reply.OK</tt>. In general, the pattern is always: fill an args struct,
    pass a pointer to a reply struct, call RPC, check the returned <tt>bool</tt>,
    then read reply fields only if the call returned true.
</p>

<p>
    Information about the MapReduce job is in the <tt>MapReduce</tt> struct,
    defined in <tt>mapreduce.go</tt>. Modify the <tt>MapReduce</tt> struct to
    keep track of any additional state (e.g. the set of available workers),
    and initialize this additional state in the <tt>InitMapReduce()</tt>
    function. The master does not need to know which Map or Reduce functions
    are being used for the job; the workers will take care of executing the
    right code for Map or Reduce.
</p>

<p>
    The master should send RPCs to the workers in parallel so that the workers
    can work on jobs concurrently. You will find the <tt>go</tt> statement useful
    for this purpose and the <a href="http://golang.org/pkg/net/rpc/">Go RPC documentation</a>.
</p>

<p>
    The master may have to wait for a worker to finish before it can hand out
    more jobs. You may find channels useful to synchronize threads that are waiting
    for reply with the master once the reply arrives. Channels are explained in the
    document on <a href="http://golang.org/doc/effective_go.html#concurrency">Concurrency in Go</a>.
</p>

<p>
    You should run your code using Go's unit test system. We supply you
    with a set of tests in <tt>test_test.go</tt>. You can run unit tests as follows:
</p>
<pre>
$ cd distributed/mapreduce
$ go test -v -run PartIIB
=== RUN   TestPartIIB_Basic
Test: Basic mapreduce ...
  ... Basic Passed
--- PASS: TestPartIIB_Basic (1.17s)
=== RUN   TestPartIIB_Parallelism
Test: Parallelism ...
  ... Parallelism Passed
--- PASS: TestPartIIB_Parallelism (1.66s)
PASS
ok      cs134-assignment1/mapreduce     3.054s
</pre>

<p>
    You are done with Part II when your implementation passes the <tt>TestPartIIB_Basic</tt>
    and <tt>TestPartIIB_Parallelism</tt> tests in <tt>test_test.go</tt>.
    <tt>TestPartIIB_Basic</tt> verifies that the full MapReduce pipeline produces correct output
    with two workers. <tt>TestPartIIB_Parallelism</tt> verifies that your master dispatches jobs
    to multiple workers concurrently (i.e., not one at a time).
    You don't yet have to worry about failures of workers.
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
    process, and can exploit multiple cores on a single machine. For simplicity, all projects will use unix sockets (think using a file as a network connection), limiting running all components of our system to the same computer, but some
    modifications could be done in order to run the workers on multiple
    machines communicating over a network. The RPCs would have to use TCP
    rather than UNIX-domain sockets; there would need to be a way to start
    worker processes on all the machines; and all the machines would have
    to share storage through some kind of network file system.
</p>

<h3 class="page-heading">Part III: Handling worker failures</h3>

<p>
    In this part you will make the master handle failed workers.
    MapReduce makes this relatively easy
    because workers don't have persistent state. If a
    worker fails, any RPCs that the master issued to that worker will fail
    (e.g. due to a timeout). Thus, if the master's RPC to the worker fails,
    the master should re-assign the job given to the failed worker to another worker.
</p>

<p>
    An RPC failure doesn't necessarily mean that the worker failed; the worker
    may just be unreachable but still computing. Thus, it may happen that two
    workers receive the same job and compute it. However, because jobs are
    idempotent, it doesn't matter if the same job is computed twice--both times it
    will generate the same output. So, you don't have to do anything special for this
    case. (Our tests never fail workers in the middle of job without killing the worker,
    so you don't even have to worry about several workers writing to the same output file.)
</p>

<p>
    You don't have to handle failures of the master; we will assume it won't
    fail. Making the master fault-tolerant is more difficult because it keeps
    persistent state that would have to be recovered in order to resume
    operations after a master failure.
    Much of the later assignments are devoted to this challenge.
</p>

<p>
    Your implementation must pass the remaining test cases in
    <tt>test_test.go</tt>: <tt>TestPartIIIOneFailure</tt> and <tt>TestPartIIIManyFailures</tt>.
    <tt>TestPartIIIOneFailure</tt> starts two workers, one of which fails after handling 10 RPCs.
    Your master must detect the failure and complete all remaining jobs using the other worker.
    <tt>TestPartIIIManyFailures</tt> continuously starts pairs of workers that each fail after 10 jobs.
    Your master must keep making forward progress by re-assigning failed jobs to newly available workers.
</p>

<p>
    You can run all tests at once with:
</p>
<pre>
$ cd distributed/mapreduce
$ go test -v
=== RUN   TestPartIIA_DoMapPartitioning
--- PASS: TestPartIIA_DoMapPartitioning (0.00s)
=== RUN   TestPartIIA_DoReduceAggregatesAndSorts
--- PASS: TestPartIIA_DoReduceAggregatesAndSorts (0.00s)
=== RUN   TestPartIIB_Basic
Test: Basic mapreduce ...
  ... Basic Passed
--- PASS: TestPartIIB_Basic (1.20s)
=== RUN   TestPartIIB_Parallelism
Test: Parallelism ...
  ... Parallelism Passed
--- PASS: TestPartIIB_Parallelism (1.80s)
=== RUN   TestPartIII_OneFailure
Test: One Failure mapreduce ...
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker0 shutdown error
  ... One Failure Passed
--- PASS: TestPartIII_OneFailure (1.42s)
=== RUN   TestPartIII_ManyFailures
Test: ManyFailures mapreduce ...
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker3 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker4 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker7 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker11 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker6 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker10 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker1 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker0 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker2 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker8 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker5 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker9 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker12 shutdown error
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-worker13 shutdown error
  ... Many Failures Passed
--- PASS: TestPartIII_ManyFailures (8.35s)
=== RUN   TestPartIII_Timeout
Test: Timeout ...
DoWork: RPC /var/tmp/134-mapreduce-501/mr51565-timeout-worker0 shutdown error
  ... Timeout Passed
--- PASS: TestPartIII_Timeout (4.38s)
PASS
ok      cs134-assignment1/mapreduce     17.381s
</pre>

<p>
    It is highly recommended to also run your tests with the Go race detector enabled to catch potential concurrency issues:
</p>
<pre>
$ go test -v -race
</pre>
<p>
    For all assignments, the autograder may run your code with the race detector.
</p>

<h3>Assignment Submission</h3>

<p>
To submit the assignment, submit the code as-is to Gradescope, following the same
code structure as from the provided skeleton code. If you have your code pushed to a <em>private</em> GitHub repository, you can also submit by linking your GitHub account
in Gradescope and selecting your repository. 
Your autograder score displayed immediately after submission is NOT your final score. After the late submission period closes, we will re-run the exact same test cases on your current active submission in order to determine your final grade. Barring any academic integrity issues or egregious bugs in the autograder, the autograder in Gradescope is the same autograder we will use to determine your final score.
</p>
