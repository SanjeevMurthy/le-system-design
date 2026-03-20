# Part III. Derived Data

> Source: Designing Data-Intensive Applications (Martin Kleppmann), Chapter 12, Pages 407-574

## Key Concepts

- PART III
Derived Data
In Parts I and II of this book, we assembled from the ground up all the major consid‐
erations that go into a distributed database, from the layout of data on disk all the
way to
- Systems of Record and Derived Data
On a high level, systems that store and process data can be grouped into two broad
categories:
Systems of record
A system of record, also known as source of truth, h

## Content

PART III
Derived Data
In Parts I and II of this book, we assembled from the ground up all the major consid‐
erations that go into a distributed database, from the layout of data on disk all the
way to the limits of distributed consistency in the presence of faults. However, this
discussion assumed that there was only one database in the application.
In reality, data systems are often more complex. In a large application you often need
to be able to access and process data in many different ways, and there is no one data‐
base that can satisfy all those different needs simultaneously. Applications thus com‐
monly use a combination of several different datastores, indexes, caches, analytics
systems, etc. and implement mechanisms for moving data from one store to another.
In this final part of the book, we will examine the issues around integrating multiple
different data systems, potentially with different data models and optimized for dif‐
ferent access patterns, into one coherent application architecture. This aspect of
system-building is often overlooked by vendors who claim that their product can sat‐
isfy all your needs. In reality, integrating disparate systems is one of the most impor‐
tant things that needs to be done in a nontrivial application.


Systems of Record and Derived Data
On a high level, systems that store and process data can be grouped into two broad
categories:
Systems of record
A system of record, also known as source of truth, holds the authoritative version
of your data. When new data comes in, e.g., as user input, it is first written here.
Each fact is represented exactly once (the representation is typically normalized).
If there is any discrepancy between another system and the system of record,
then the value in the system of record is (by definition) the correct one.
Derived data systems
Data in a derived system is the result of taking some existing data from another
system and transforming or processing it in some way. If you lose derived data,
you can recreate it from the original source. A classic example is a cache: data can
be served from the cache if present, but if the cache doesn’t contain what you
need, you can fall back to the underlying database. Denormalized values, indexes,
and materialized views also fall into this category. In recommendation systems,
predictive summary data is often derived from usage logs.
Technically speaking, derived data is redundant, in the sense that it duplicates exist‐
ing information. However, it is often essential for getting good performance on read
queries. It is commonly denormalized. You can derive several different datasets from
a single source, enabling you to look at the data from different “points of view.”
Not all systems make a clear distinction between systems of record and derived data
in their architecture, but it’s a very helpful distinction to make, because it clarifies the
dataflow through your system: it makes explicit which parts of the system have which
inputs and which outputs, and how they depend on each other.
Most databases, storage engines, and query languages are not inherently either a sys‐
tem of record or a derived system. A database is just a tool: how you use it is up to
you. The distinction between system of record and derived data system depends not
on the tool, but on how you use it in your application.
By being clear about which data is derived from which other data, you can bring
clarity to an otherwise confusing system architecture. This point will be a running
theme throughout this part of the book.


Overview of Chapters
We will start in Chapter 10 by examining batch-oriented dataflow systems such as
MapReduce, and see how they give us good tools and principles for building largescale data systems. In Chapter 11 we will take those ideas and apply them to data
streams, which allow us to do the same kinds of things with lower delays. Chapter 12
concludes the book by exploring ideas about how we might use these tools to build
reliable, scalable, and maintainable applications in the future.




CHAPTER 10
Batch Processing
A system cannot be successful if it is too strongly influenced by a single person. Once the
initial design is complete and fairly robust, the real test begins as people with many different
viewpoints undertake their own experiments.
—Donald Knuth
In the first two parts of this book we talked a lot about requests and queries, and the
corresponding responses or results. This style of data processing is assumed in many
modern data systems: you ask for something, or you send an instruction, and some
time later the system (hopefully) gives you an answer. Databases, caches, search
indexes, web servers, and many other systems work this way.
In such online systems, whether it’s a web browser requesting a page or a service call‐
ing a remote API, we generally assume that the request is triggered by a human user,
and that the user is waiting for the response. They shouldn’t have to wait too long, so
we pay a lot of attention to the response time of these systems (see “Describing Perfor‐
mance” on page 13).
The web, and increasing numbers of HTTP/REST-based APIs, has made the request/
response style of interaction so common that it’s easy to take it for granted. But we
should remember that it’s not the only way of building systems, and that other
approaches have their merits too. Let’s distinguish three different types of systems:
Services (online systems)
A service waits for a request or instruction from a client to arrive. When one is
received, the service tries to handle it as quickly as possible and sends a response
back. Response time is usually the primary measure of performance of a service,
and availability is often very important (if the client can’t reach the service, the
user will probably get an error message).
389


Batch processing systems (offline systems)
A batch processing system takes a large amount of input data, runs a job to pro‐
cess it, and produces some output data. Jobs often take a while (from a few
minutes to several days), so there normally isn’t a user waiting for the job to fin‐
ish. Instead, batch jobs are often scheduled to run periodically (for example, once
a day). The primary performance measure of a batch job is usually throughput
(the time it takes to crunch through an input dataset of a certain size). We dis‐
cuss batch processing in this chapter.
Stream processing systems (near-real-time systems)
Stream processing is somewhere between online and offline/batch processing (so
it is sometimes called near-real-time or nearline processing). Like a batch pro‐
cessing system, a stream processor consumes inputs and produces outputs
(rather than responding to requests). However, a stream job operates on events
shortly after they happen, whereas a batch job operates on a fixed set of input
data. This difference allows stream processing systems to have lower latency than
the equivalent batch systems. As stream processing builds upon batch process‐
ing, we discuss it in Chapter 11.
As we shall see in this chapter, batch processing is an important building block in our
quest to build reliable, scalable, and maintainable applications. For example, Map‐
Reduce, a batch processing algorithm published in 2004 [1], was (perhaps overenthusiastically) called “the algorithm that makes Google so massively scalable” [2]. It
was subsequently implemented in various open source data systems, including
Hadoop, CouchDB, and MongoDB.
MapReduce is a fairly low-level programming model compared to the parallel pro‐
cessing systems that were developed for data warehouses many years previously [3,
4], but it was a major step forward in terms of the scale of processing that could be
achieved on commodity hardware. Although the importance of MapReduce is now
declining [5], it is still worth understanding, because it provides a clear picture of
why and how batch processing is useful.
In fact, batch processing is a very old form of computing. Long before programmable
digital computers were invented, punch card tabulating machines—such as the Hol‐
lerith machines used in the 1890 US Census [6]—implemented a semi-mechanized
form of batch processing to compute aggregate statistics from large inputs. And Map‐
Reduce bears an uncanny resemblance to the electromechanical IBM card-sorting
machines that were widely used for business data processing in the 1940s and 1950s
[7]. As usual, history has a tendency of repeating itself.
In this chapter, we will look at MapReduce and several other batch processing algo‐
rithms and frameworks, and explore how they are used in modern data systems. But
first, to get started, we will look at data processing using standard Unix tools. Even if
you are already familiar with them, a reminder about the Unix philosophy is worth‐
390 
| 
Chapter 10: Batch Processing


i. Some people love to point out that cat is unnecessary here, as the input file could be given directly as an
argument to awk. However, the linear pipeline is more apparent when written like this.
while because the ideas and lessons from Unix carry over to large-scale, heterogene‐
ous distributed data systems.
Batch Processing with Unix Tools
Let’s start with a simple example. Say you have a web server that appends a line to a
log file every time it serves a request. For example, using the nginx default access log
format, one line of the log might look like this:
216.58.210.78 - - [27/Feb/2015:17:55:11 +0000] "GET /css/typography.css HTTP/1.1"
200 3377 "http://martin.kleppmann.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X
10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115
Safari/537.36"
(That is actually one line; it’s only broken onto multiple lines here for readability.)
There’s a lot of information in that line. In order to interpret it, you need to look at
the definition of the log format, which is as follows:
$remote_addr - $remote_user [$time_local] "$request"
$status $body_bytes_sent "$http_referer" "$http_user_agent"
So, this one line of the log indicates that on February 27, 2015, at 17:55:11 UTC, the
server received a request for the file /css/typography.css from the client IP address
216.58.210.78. The user was not authenticated, so $remote_user is set to a hyphen
(-). The response status was 200 (i.e., the request was successful), and the response
was 3,377 bytes in size. The web browser was Chrome 40, and it loaded the file
because it was referenced in the page at the URL http://martin.kleppmann.com/.
Simple Log Analysis
Various tools can take these log files and produce pretty reports about your website
traffic, but for the sake of exercise, let’s build our own, using basic Unix tools. For
example, say you want to find the five most popular pages on your website. You can
do this in a Unix shell as follows:i 
cat /var/log/nginx/access.log | 
  awk '{print $7}' | 
  sort             | 
  uniq -c          | 
  sort -r -n       | 
  head -n 5          
Read the log file.
Batch Processing with Unix Tools 
| 
391


Split each line into fields by whitespace, and output only the seventh such field
from each line, which happens to be the requested URL. In our example line, this
request URL is /css/typography.css.
Alphabetically sort the list of requested URLs. If some URL has been requested
n times, then after sorting, the file contains the same URL repeated n times in a
row.
The uniq command filters out repeated lines in its input by checking whether
two adjacent lines are the same. The -c option tells it to also output a counter: for
every distinct URL, it reports how many times that URL appeared in the input.
The second sort sorts by the number (-n) at the start of each line, which is the
number of times the URL was requested. It then returns the results in reverse
(-r) order, i.e. with the largest number first.
Finally, head outputs just the first five lines (-n 5) of input, and discards the rest.
The output of that series of commands looks something like this:
4189 /favicon.ico
3631 /2013/05/24/improving-security-of-ssh-private-keys.html
2124 /2012/12/05/schema-evolution-in-avro-protocol-buffers-thrift.html
1369 /
 915 /css/typography.css
Although the preceding command line likely looks a bit obscure if you’re unfamiliar
with Unix tools, it is incredibly powerful. It will process gigabytes of log files in a
matter of seconds, and you can easily modify the analysis to suit your needs. For
example, if you want to omit CSS files from the report, change the awk argument to
'$7 !~ /\.css$/ {print $7}'. If you want to count top client IP addresses instead
of top pages, change the awk argument to '{print $1}'. And so on.
We don’t have space in this book to explore Unix tools in detail, but they are very
much worth learning about. Surprisingly many data analyses can be done in a few
minutes using some combination of awk, sed, grep, sort, uniq, and xargs, and they
perform surprisingly well [8].
Chain of commands versus custom program
Instead of the chain of Unix commands, you could write a simple program to do the
same thing. For example, in Ruby, it might look something like this:
392 
| 
Chapter 10: Batch Processing


counts = Hash.new(0) 
File.open('/var/log/nginx/access.log') do |file|
  file.each do |line|
    url = line.split[6] 
    counts[url] += 1 
  end
end
top5 = counts.map{|url, count| [count, url] }.sort.reverse[0...5] 
top5.each{|count, url| puts "#{count} #{url}" } 
counts is a hash table that keeps a counter for the number of times we’ve seen
each URL. A counter is zero by default.
From each line of the log, we take the URL to be the seventh whitespaceseparated field (the array index here is 6 because Ruby’s arrays are zero-indexed).
Increment the counter for the URL in the current line of the log.
Sort the hash table contents by counter value (descending), and take the top five
entries.
Print out those top five entries.
This program is not as concise as the chain of Unix pipes, but it’s fairly readable, and
which of the two you prefer is partly a matter of taste. However, besides the superfi‐
cial syntactic differences between the two, there is a big difference in the execution
flow, which becomes apparent if you run this analysis on a large file.
Sorting versus in-memory aggregation
The Ruby script keeps an in-memory hash table of URLs, where each URL is mapped
to the number of times it has been seen. The Unix pipeline example does not have
such a hash table, but instead relies on sorting a list of URLs in which multiple occur‐
rences of the same URL are simply repeated.
Which approach is better? It depends how many different URLs you have. For most
small to mid-sized websites, you can probably fit all distinct URLs, and a counter for
each URL, in (say) 1 GB of memory. In this example, the working set of the job (the
amount of memory to which the job needs random access) depends only on the
number of distinct URLs: if there are a million log entries for a single URL, the space
required in the hash table is still just one URL plus the size of the counter. If this
working set is small enough, an in-memory hash table works fine—even on a laptop.
On the other hand, if the job’s working set is larger than the available memory, the
sorting approach has the advantage that it can make efficient use of disks. It’s the
Batch Processing with Unix Tools 
| 
393


same principle as we discussed in “SSTables and LSM-Trees” on page 76: chunks of
data can be sorted in memory and written out to disk as segment files, and then mul‐
tiple sorted segments can be merged into a larger sorted file. Mergesort has sequential
access patterns that perform well on disks. (Remember that optimizing for sequential
I/O was a recurring theme in Chapter 3. The same pattern reappears here.)
The sort utility in GNU Coreutils (Linux) automatically handles larger-thanmemory datasets by spilling to disk, and automatically parallelizes sorting across
multiple CPU cores [9]. This means that the simple chain of Unix commands we saw
earlier easily scales to large datasets, without running out of memory. The bottleneck
is likely to be the rate at which the input file can be read from disk. 
The Unix Philosophy
It’s no coincidence that we were able to analyze a log file quite easily, using a chain of
commands like in the previous example: this was in fact one of the key design ideas of
Unix, and it remains astonishingly relevant today. Let’s look at it in some more depth
so that we can borrow some ideas from Unix [10].
Doug McIlroy, the inventor of Unix pipes, first described them like this in 1964 [11]:
“We should have some ways of connecting programs like [a] garden hose—screw in
another segment when it becomes necessary to massage data in another way. This is
the way of I/O also.” The plumbing analogy stuck, and the idea of connecting pro‐
grams with pipes became part of what is now known as the Unix philosophy—a set of
design principles that became popular among the developers and users of Unix. The
philosophy was described in 1978 as follows [12, 13]:
1. Make each program do one thing well. To do a new job, build afresh rather than
complicate old programs by adding new “features”.
2. Expect the output of every program to become the input to another, as yet
unknown, program. Don’t clutter output with extraneous information. Avoid
stringently columnar or binary input formats. Don’t insist on interactive input.
3. Design and build software, even operating systems, to be tried early, ideally within
weeks. Don’t hesitate to throw away the clumsy parts and rebuild them.
4. Use tools in preference to unskilled help to lighten a programming task, even if
you have to detour to build the tools and expect to throw some of them out after
you’ve finished using them.
This approach—automation, rapid prototyping, incremental iteration, being friendly
to experimentation, and breaking down large projects into manageable chunks—
sounds remarkably like the Agile and DevOps movements of today. Surprisingly little
has changed in four decades.
394 
| 
Chapter 10: Batch Processing


ii. Another example of a uniform interface is URLs and HTTP, the foundations of the web. A URL identifies
a particular thing (resource) on a website, and you can link to any URL from any other website. A user with a
web browser can thus seamlessly jump between websites by following links, even though the servers may be
operated by entirely unrelated organizations. This principle seems obvious today, but it was a key insight in
making the web the success that it is today. Prior systems were not so uniform: for example, in the era of
bulletin board systems (BBSs), each system had its own phone number and baud rate configuration. A refer‐
ence from one BBS to another would have to be in the form of a phone number and modem settings; the user
would have to hang up, dial the other BBS, and then manually find the information they were looking for. It
wasn’t possible to link directly to some piece of content inside another BBS.
The sort tool is a great example of a program that does one thing well. It is arguably
a better sorting implementation than most programming languages have in their
standard libraries (which do not spill to disk and do not use multiple threads, even
when that would be beneficial). And yet, sort is barely useful in isolation. It only
becomes powerful in combination with the other Unix tools, such as uniq.
A Unix shell like bash lets us easily compose these small programs into surprisingly
powerful data processing jobs. Even though many of these programs are written by
different groups of people, they can be joined together in flexible ways. What does
Unix do to enable this composability?
A uniform interface
If you expect the output of one program to become the input to another program,
that means those programs must use the same data format—in other words, a com‐
patible interface. If you want to be able to connect any program’s output to any pro‐
gram’s input, that means that all programs must use the same input/output interface.
In Unix, that interface is a file (or, more precisely, a file descriptor). A file is just an
ordered sequence of bytes. Because that is such a simple interface, many different
things can be represented using the same interface: an actual file on the filesystem, a
communication channel to another process (Unix socket, stdin, stdout), a device
driver (say /dev/audio or /dev/lp0), a socket representing a TCP connection, and so
on. It’s easy to take this for granted, but it’s actually quite remarkable that these very
different things can share a uniform interface, so they can easily be plugged together.ii
By convention, many (but not all) Unix programs treat this sequence of bytes as
ASCII text. Our log analysis example used this fact: awk, sort, uniq, and head all treat
their input file as a list of records separated by the \n (newline, ASCII 0x0A) charac‐
ter. The choice of \n is arbitrary—arguably, the ASCII record separator 0x1E would
have been a better choice, since it’s intended for this purpose [14]—but in any case,
the fact that all these programs have standardized on using the same record separator
allows them to interoperate.
Batch Processing with Unix Tools 
| 
395


The parsing of each record (i.e., a line of input) is more vague. Unix tools commonly
split a line into fields by whitespace or tab characters, but CSV (comma-separated),
pipe-separated, and other encodings are also used. Even a fairly simple tool like
xargs has half a dozen command-line options for specifying how its input should be
parsed.
The uniform interface of ASCII text mostly works, but it’s not exactly beautiful: our
log analysis example used {print $7} to extract the URL, which is not very readable.
In an ideal world this could have perhaps been {print $request_url} or something
of that sort. We will return to this idea later.
Although it’s not perfect, even decades later, the uniform interface of Unix is still
something remarkable. Not many pieces of software interoperate and compose as
well as Unix tools do: you can’t easily pipe the contents of your email account and
your online shopping history through a custom analysis tool into a spreadsheet and
post the results to a social network or a wiki. Today it’s an exception, not the norm,
to have programs that work together as smoothly as Unix tools do.
Even databases with the same data model often don’t make it easy to get data out of
one and into the other. This lack of integration leads to Balkanization of data.
Separation of logic and wiring
Another characteristic feature of Unix tools is their use of standard input (stdin) and
standard output (stdout). If you run a program and don’t specify anything else,
stdin comes from the keyboard and stdout goes to the screen. However, you can
also take input from a file and/or redirect output to a file. Pipes let you attach the
stdout of one process to the stdin of another process (with a small in-memory
buffer, and without writing the entire intermediate data stream to disk).
A program can still read and write files directly if it needs to, but the Unix approach
works best if a program doesn’t worry about particular file paths and simply uses
stdin and stdout. This allows a shell user to wire up the input and output in what‐
ever way they want; the program doesn’t know or care where the input is coming
from and where the output is going to. (One could say this is a form of loose coupling,
late binding [15], or inversion of control [16].) Separating the input/output wiring
from the program logic makes it easier to compose small tools into bigger systems.
You can even write your own programs and combine them with the tools provided
by the operating system. Your program just needs to read input from stdin and write
output to stdout, and it can participate in data processing pipelines. In the log analy‐
sis example, you could write a tool that translates user-agent strings into more sensi‐
ble browser identifiers, or a tool that translates IP addresses into country codes, and
simply plug it into the pipeline. The sort program doesn’t care whether it’s commu‐
nicating with another part of the operating system or with a program written by you.
396 
| 
Chapter 10: Batch Processing


iii. Except by using a separate tool, such as netcat or curl. Unix started out trying to represent everything as
files, but the BSD sockets API deviated from that convention [17]. The research operating systems Plan 9 and
Inferno are more consistent in their use of files: they represent a TCP connection as a file in /net/tcp [18].
However, there are limits to what you can do with stdin and stdout. Programs that
need multiple inputs or outputs are possible but tricky. You can’t pipe a program’s
output into a network connection [17, 18].iii If a program directly opens files for read‐
ing and writing, or starts another program as a subprocess, or opens a network con‐
nection, then that I/O is wired up by the program itself. It can still be configurable
(through command-line options, for example), but the flexibility of wiring up inputs
and outputs in a shell is reduced.
Transparency and experimentation
Part of what makes Unix tools so successful is that they make it quite easy to see what
is going on:
• The input files to Unix commands are normally treated as immutable. This
means you can run the commands as often as you want, trying various
command-line options, without damaging the input files.
• You can end the pipeline at any point, pipe the output into less, and look at it to
see if it has the expected form. This ability to inspect is great for debugging.
• You can write the output of one pipeline stage to a file and use that file as input
to the next stage. This allows you to restart the later stage without rerunning the
entire pipeline.
Thus, even though Unix tools are quite blunt, simple tools compared to a query opti‐
mizer of a relational database, they remain amazingly useful, especially for experi‐
mentation.
However, the biggest limitation of Unix tools is that they run only on a single
machine—and that’s where tools like Hadoop come in. 
MapReduce and Distributed Filesystems
MapReduce is a bit like Unix tools, but distributed across potentially thousands of
machines. Like Unix tools, it is a fairly blunt, brute-force, but surprisingly effective
tool. A single MapReduce job is comparable to a single Unix process: it takes one or
more inputs and produces one or more outputs.
As with most Unix tools, running a MapReduce job normally does not modify the
input and does not have any side effects other than producing the output. The output
MapReduce and Distributed Filesystems 
| 
397


iv. One difference is that with HDFS, computing tasks can be scheduled to run on the machine that stores a
copy of a particular file, whereas object stores usually keep storage and computation separate. Reading from a
local disk has a performance advantage if network bandwidth is a bottleneck. Note however that if erasure
coding is used, the locality advantage is lost, because the data from several machines must be combined in
order to reconstitute the original file [20].
files are written once, in a sequential fashion (not modifying any existing part of a file
once it has been written).
While Unix tools use stdin and stdout as input and output, MapReduce jobs read
and write files on a distributed filesystem. In Hadoop’s implementation of Map‐
Reduce, that filesystem is called HDFS (Hadoop Distributed File System), an open
source reimplementation of the Google File System (GFS) [19].
Various other distributed filesystems besides HDFS exist, such as GlusterFS and the
Quantcast File System (QFS) [20]. Object storage services such as Amazon S3, Azure
Blob Storage, and OpenStack Swift [21] are similar in many ways.iv In this chapter we
will mostly use HDFS as a running example, but the principles apply to any dis‐
tributed filesystem.
HDFS is based on the shared-nothing principle (see the introduction to Part II), in
contrast to the shared-disk approach of Network Attached Storage (NAS) and Storage
Area Network (SAN) architectures. Shared-disk storage is implemented by a central‐
ized storage appliance, often using custom hardware and special network infrastruc‐
ture such as Fibre Channel. On the other hand, the shared-nothing approach requires
no special hardware, only computers connected by a conventional datacenter net‐
work.
HDFS consists of a daemon process running on each machine, exposing a network
service that allows other nodes to access files stored on that machine (assuming that
every general-purpose machine in a datacenter has some disks attached to it). A cen‐
tral server called the NameNode keeps track of which file blocks are stored on which
machine. Thus, HDFS conceptually creates one big filesystem that can use the space
on the disks of all machines running the daemon.
In order to tolerate machine and disk failures, file blocks are replicated on multiple
machines. Replication may mean simply several copies of the same data on multiple
machines, as in Chapter 5, or an erasure coding scheme such as Reed–Solomon codes,
which allows lost data to be recovered with lower storage overhead than full replica‐
tion [20, 22]. The techniques are similar to RAID, which provides redundancy across
several disks attached to the same machine; the difference is that in a distributed file‐
system, file access and replication are done over a conventional datacenter network
without special hardware.
398 
| 
Chapter 10: Batch Processing


HDFS has scaled well: at the time of writing, the biggest HDFS deployments run on
tens of thousands of machines, with combined storage capacity of hundreds of peta‐
bytes [23]. Such large scale has become viable because the cost of data storage and
access on HDFS, using commodity hardware and open source software, is much
lower than that of the equivalent capacity on a dedicated storage appliance [24]. 
MapReduce Job Execution
MapReduce is a programming framework with which you can write code to process
large datasets in a distributed filesystem like HDFS. The easiest way of understanding
it is by referring back to the web server log analysis example in “Simple Log Analysis”
on page 391. The pattern of data processing in MapReduce is very similar to this
example:
1. Read a set of input files, and break it up into records. In the web server log exam‐
ple, each record is one line in the log (that is, \n is the record separator).
2. Call the mapper function to extract a key and value from each input record. In
the preceding example, the mapper function is awk '{print $7}': it extracts the
URL ($7) as the key, and leaves the value empty.
3. Sort all of the key-value pairs by key. In the log example, this is done by the first
sort command.
4. Call the reducer function to iterate over the sorted key-value pairs. If there are
multiple occurrences of the same key, the sorting has made them adjacent in the
list, so it is easy to combine those values without having to keep a lot of state in
memory. In the preceding example, the reducer is implemented by the command
uniq -c, which counts the number of adjacent records with the same key.
Those four steps can be performed by one MapReduce job. Steps 2 (map) and 4
(reduce) are where you write your custom data processing code. Step 1 (breaking files
into records) is handled by the input format parser. Step 3, the sort step, is implicit
in MapReduce—you don’t have to write it, because the output from the mapper is
always sorted before it is given to the reducer.
To create a MapReduce job, you need to implement two callback functions, the map‐
per and reducer, which behave as follows (see also “MapReduce Querying” on page
46):
Mapper
The mapper is called once for every input record, and its job is to extract the key
and value from the input record. For each input, it may generate any number of
key-value pairs (including none). It does not keep any state from one input
record to the next, so each record is handled independently.
MapReduce and Distributed Filesystems 
| 
399


Reducer
The MapReduce framework takes the key-value pairs produced by the mappers,
collects all the values belonging to the same key, and calls the reducer with an
iterator over that collection of values. The reducer can produce output records
(such as the number of occurrences of the same URL).
In the web server log example, we had a second sort command in step 5, which
ranked URLs by number of requests. In MapReduce, if you need a second sorting
stage, you can implement it by writing a second MapReduce job and using the output
of the first job as input to the second job. Viewed like this, the role of the mapper is to
prepare the data by putting it into a form that is suitable for sorting, and the role of
the reducer is to process the data that has been sorted. 
Distributed execution of MapReduce
The main difference from pipelines of Unix commands is that MapReduce can paral‐
lelize a computation across many machines, without you having to write code to
explicitly handle the parallelism. The mapper and reducer only operate on one record
at a time; they don’t need to know where their input is coming from or their output is
going to, so the framework can handle the complexities of moving data between
machines.
It is possible to use standard Unix tools as mappers and reducers in a distributed
computation [25], but more commonly they are implemented as functions in a con‐
ventional programming language. In Hadoop MapReduce, the mapper and reducer
are each a Java class that implements a particular interface. In MongoDB and
CouchDB, mappers and reducers are JavaScript functions (see “MapReduce Query‐
ing” on page 46).
Figure 10-1 shows the dataflow in a Hadoop MapReduce job. Its parallelization is
based on partitioning (see Chapter 6): the input to a job is typically a directory in
HDFS, and each file or file block within the input directory is considered to be a sepa‐
rate partition that can be processed by a separate map task (marked by m 1, m 2, and
m 3 in Figure 10-1).
Each input file is typically hundreds of megabytes in size. The MapReduce scheduler
(not shown in the diagram) tries to run each mapper on one of the machines that
stores a replica of the input file, provided that machine has enough spare RAM and
CPU resources to run the map task [26]. This principle is known as putting the com‐
putation near the data [27]: it saves copying the input file over the network, reducing
network load and increasing locality.
400 
| 
Chapter 10: Batch Processing


Figure 10-1. A MapReduce job with three mappers and three reducers.
In most cases, the application code that should run in the map task is not yet present
on the machine that is assigned the task of running it, so the MapReduce framework
first copies the code (e.g., JAR files in the case of a Java program) to the appropriate
machines. It then starts the map task and begins reading the input file, passing one
record at a time to the mapper callback. The output of the mapper consists of keyvalue pairs.
The reduce side of the computation is also partitioned. While the number of map
tasks is determined by the number of input file blocks, the number of reduce tasks is
configured by the job author (it can be different from the number of map tasks). To
ensure that all key-value pairs with the same key end up at the same reducer, the
framework uses a hash of the key to determine which reduce task should receive a
particular key-value pair (see “Partitioning by Hash of Key” on page 203).
The key-value pairs must be sorted, but the dataset is likely too large to be sorted with
a conventional sorting algorithm on a single machine. Instead, the sorting is per‐
formed in stages. First, each map task partitions its output by reducer, based on the
hash of the key. Each of these partitions is written to a sorted file on the mapper’s
local disk, using a technique similar to what we discussed in “SSTables and LSM-
Trees” on page 76.
MapReduce and Distributed Filesystems 
| 
401


Whenever a mapper finishes reading its input file and writing its sorted output files,
the MapReduce scheduler notifies the reducers that they can start fetching the output
files from that mapper. The reducers connect to each of the mappers and download
the files of sorted key-value pairs for their partition. The process of partitioning by
reducer, sorting, and copying data partitions from mappers to reducers is known as
the shuffle [26] (a confusing term—unlike shuffling a deck of cards, there is no ran‐
domness in MapReduce).
The reduce task takes the files from the mappers and merges them together, preserv‐
ing the sort order. Thus, if different mappers produced records with the same key,
they will be adjacent in the merged reducer input.
The reducer is called with a key and an iterator that incrementally scans over all
records with the same key (which may in some cases not all fit in memory). The
reducer can use arbitrary logic to process these records, and can generate any number
of output records. These output records are written to a file on the distributed filesys‐
tem (usually, one copy on the local disk of the machine running the reducer, with
replicas on other machines).
MapReduce workflows
The range of problems you can solve with a single MapReduce job is limited. Refer‐
ring back to the log analysis example, a single MapReduce job could determine the
number of page views per URL, but not the most popular URLs, since that requires a
second round of sorting.
Thus, it is very common for MapReduce jobs to be chained together into workflows,
such that the output of one job becomes the input to the next job. The Hadoop Map‐
Reduce framework does not have any particular support for workflows, so this chain‐
ing is done implicitly by directory name: the first job must be configured to write its
output to a designated directory in HDFS, and the second job must be configured to
read that same directory name as its input. From the MapReduce framework’s point
of view, they are two independent jobs.
Chained MapReduce jobs are therefore less like pipelines of Unix commands (which
pass the output of one process as input to another process directly, using only a small
in-memory buffer) and more like a sequence of commands where each command’s
output is written to a temporary file, and the next command reads from the tempo‐
rary file. This design has advantages and disadvantages, which we will discuss in
“Materialization of Intermediate State” on page 419.
A batch job’s output is only considered valid when the job has completed successfully
(MapReduce discards the partial output of a failed job). Therefore, one job in a work‐
flow can only start when the prior jobs—that is, the jobs that produce its input direc‐
tories—have completed successfully. To handle these dependencies between job
402 
| 
Chapter 10: Batch Processing


v. The joins we talk about in this book are generally equi-joins, the most common type of join, in which a
record is associated with other records that have an identical value in a particular field (such as an ID). Some
databases support more general types of joins, for example using a less-than operator instead of an equality
operator, but we do not have space to cover them here.
executions, various workflow schedulers for Hadoop have been developed, including
Oozie, Azkaban, Luigi, Airflow, and Pinball [28].
These schedulers also have management features that are useful when maintaining a
large collection of batch jobs. Workflows consisting of 50 to 100 MapReduce jobs are
common when building recommendation systems [29], and in a large organization,
many different teams may be running different jobs that read each other’s output.
Tool support is important for managing such complex dataflows.
Various higher-level tools for Hadoop, such as Pig [30], Hive [31], Cascading [32],
Crunch [33], and FlumeJava [34], also set up workflows of multiple MapReduce
stages that are automatically wired together appropriately. 
Reduce-Side Joins and Grouping
We discussed joins in Chapter 2 in the context of data models and query languages,
but we have not delved into how joins are actually implemented. It is time that we
pick up that thread again.
In many datasets it is common for one record to have an association with another
record: a foreign key in a relational model, a document reference in a document
model, or an edge in a graph model. A join is necessary whenever you have some
code that needs to access records on both sides of that association (both the record
that holds the reference and the record being referenced). As discussed in Chapter 2,
denormalization can reduce the need for joins but generally not remove it entirely.v
In a database, if you execute a query that involves only a small number of records, the
database will typically use an index to quickly locate the records of interest (see Chap‐
ter 3). If the query involves joins, it may require multiple index lookups. However,
MapReduce has no concept of indexes—at least not in the usual sense.
When a MapReduce job is given a set of files as input, it reads the entire content of all
of those files; a database would call this operation a full table scan. If you only want to
read a small number of records, a full table scan is outrageously expensive compared
to an index lookup. However, in analytic queries (see “Transaction Processing or
Analytics?” on page 90) it is common to want to calculate aggregates over a large
number of records. In this case, scanning the entire input might be quite a reasonable
thing to do, especially if you can parallelize the processing across multiple machines.
MapReduce and Distributed Filesystems 
| 
403


When we talk about joins in the context of batch processing, we mean resolving all
occurrences of some association within a dataset. For example, we assume that a job
is processing the data for all users simultaneously, not merely looking up the data for
one particular user (which would be done far more efficiently with an index).
Example: analysis of user activity events
A typical example of a join in a batch job is illustrated in Figure 10-2. On the left is a
log of events describing the things that logged-in users did on a website (known as
activity events or clickstream data), and on the right is a database of users. You can
think of this example as being part of a star schema (see “Stars and Snowflakes: Sche‐
mas for Analytics” on page 93): the log of events is the fact table, and the user data‐
base is one of the dimensions.
Figure 10-2. A join between a log of user activity events and a database of user profiles.
An analytics task may need to correlate user activity with user profile information:
for example, if the profile contains the user’s age or date of birth, the system could
determine which pages are most popular with which age groups. However, the activ‐
ity events contain only the user ID, not the full user profile information. Embedding
that profile information in every single activity event would most likely be too waste‐
ful. Therefore, the activity events need to be joined with the user profile database.
The simplest implementation of this join would go over the activity events one by
one and query the user database (on a remote server) for every user ID it encounters.
This is possible, but it would most likely suffer from very poor performance: the pro‐
cessing throughput would be limited by the round-trip time to the database server,
the effectiveness of a local cache would depend very much on the distribution of data,
and running a large number of queries in parallel could easily overwhelm the data‐
base [35].
404 
| 
Chapter 10: Batch Processing


In order to achieve good throughput in a batch process, the computation must be (as
much as possible) local to one machine. Making random-access requests over the
network for every record you want to process is too slow. Moreover, querying a
remote database would mean that the batch job becomes nondeterministic, because
the data in the remote database might change.
Thus, a better approach would be to take a copy of the user database (for example,
extracted from a database backup using an ETL process—see “Data Warehousing” on
page 91) and to put it in the same distributed filesystem as the log of user activity
events. You would then have the user database in one set of files in HDFS and the
user activity records in another set of files, and could use MapReduce to bring
together all of the relevant records in the same place and process them efficiently.
Sort-merge joins
Recall that the purpose of the mapper is to extract a key and value from each input
record. In the case of Figure 10-2, this key would be the user ID: one set of mappers
would go over the activity events (extracting the user ID as the key and the activity
event as the value), while another set of mappers would go over the user database
(extracting the user ID as the key and the user’s date of birth as the value). This pro‐
cess is illustrated in Figure 10-3.
Figure 10-3. A reduce-side sort-merge join on user ID. If the input datasets are parti‐
tioned into multiple files, each could be processed with multiple mappers in parallel.
When the MapReduce framework partitions the mapper output by key and then sorts
the key-value pairs, the effect is that all the activity events and the user record with
the same user ID become adjacent to each other in the reducer input. The Map‐
Reduce job can even arrange the records to be sorted such that the reducer always
MapReduce and Distributed Filesystems 
| 
405


sees the record from the user database first, followed by the activity events in time‐
stamp order—this technique is known as a secondary sort [26].
The reducer can then perform the actual join logic easily: the reducer function is
called once for every user ID, and thanks to the secondary sort, the first value is
expected to be the date-of-birth record from the user database. The reducer stores the
date of birth in a local variable and then iterates over the activity events with the same
user ID, outputting pairs of viewed-url and viewer-age-in-years. Subsequent Map‐
Reduce jobs could then calculate the distribution of viewer ages for each URL, and
cluster by age group.
Since the reducer processes all of the records for a particular user ID in one go, it only
needs to keep one user record in memory at any one time, and it never needs to make
any requests over the network. This algorithm is known as a sort-merge join, since
mapper output is sorted by key, and the reducers then merge together the sorted lists
of records from both sides of the join.
Bringing related data together in the same place
In a sort-merge join, the mappers and the sorting process make sure that all the nec‐
essary data to perform the join operation for a particular user ID is brought together
in the same place: a single call to the reducer. Having lined up all the required data in
advance, the reducer can be a fairly simple, single-threaded piece of code that can
churn through records with high throughput and low memory overhead.
One way of looking at this architecture is that mappers “send messages” to the reduc‐
ers. When a mapper emits a key-value pair, the key acts like the destination address
to which the value should be delivered. Even though the key is just an arbitrary string
(not an actual network address like an IP address and port number), it behaves like
an address: all key-value pairs with the same key will be delivered to the same desti‐
nation (a call to the reducer).
Using the MapReduce programming model has separated the physical network com‐
munication aspects of the computation (getting the data to the right machine) from
the application logic (processing the data once you have it). This separation contrasts
with the typical use of databases, where a request to fetch data from a database often
occurs somewhere deep inside a piece of application code [36]. Since MapReduce
handles all network communication, it also shields the application code from having
to worry about partial failures, such as the crash of another node: MapReduce trans‐
parently retries failed tasks without affecting the application logic.
GROUP BY
Besides joins, another common use of the “bringing related data to the same place”
pattern is grouping records by some key (as in the GROUP BY clause in SQL). All
406 
| 
Chapter 10: Batch Processing


records with the same key form a group, and the next step is often to perform some
kind of aggregation within each group—for example:
• Counting the number of records in each group (like in our example of counting
page views, which you would express as a COUNT(*) aggregation in SQL)
• Adding up the values in one particular field (SUM(fieldname)) in SQL
• Picking the top k records according to some ranking function
The simplest way of implementing such a grouping operation with MapReduce is to
set up the mappers so that the key-value pairs they produce use the desired grouping
key. The partitioning and sorting process then brings together all the records with the
same key in the same reducer. Thus, grouping and joining look quite similar when
implemented on top of MapReduce.
Another common use for grouping is collating all the activity events for a particular
user session, in order to find out the sequence of actions that the user took—a pro‐
cess called sessionization [37]. For example, such analysis could be used to work out
whether users who were shown a new version of your website are more likely to make
a purchase than those who were shown the old version (A/B testing), or to calculate
whether some marketing activity is worthwhile.
If you have multiple web servers handling user requests, the activity events for a par‐
ticular user are most likely scattered across various different servers’ log files. You can
implement sessionization by using a session cookie, user ID, or similar identifier as
the grouping key and bringing all the activity events for a particular user together in
one place, while distributing different users’ events across different partitions.
Handling skew
The pattern of “bringing all records with the same key to the same place” breaks
down if there is a very large amount of data related to a single key. For example, in a
social network, most users might be connected to a few hundred people, but a small
number of celebrities may have many millions of followers. Such disproportionately
active database records are known as linchpin objects [38] or hot keys.
Collecting all activity related to a celebrity (e.g., replies to something they posted) in a
single reducer can lead to significant skew (also known as hot spots)—that is, one
reducer that must process significantly more records than the others (see “Skewed
Workloads and Relieving Hot Spots” on page 205). Since a MapReduce job is only
complete when all of its mappers and reducers have completed, any subsequent jobs
must wait for the slowest reducer to complete before they can start.
If a join input has hot keys, there are a few algorithms you can use to compensate.
For example, the skewed join method in Pig first runs a sampling job to determine
which keys are hot [39]. When performing the actual join, the mappers send any
MapReduce and Distributed Filesystems 
| 
407


records relating to a hot key to one of several reducers, chosen at random (in contrast
to conventional MapReduce, which chooses a reducer deterministically based on a
hash of the key). For the other input to the join, records relating to the hot key need
to be replicated to all reducers handling that key [40].
This technique spreads the work of handling the hot key over several reducers, which
allows it to be parallelized better, at the cost of having to replicate the other join input
to multiple reducers. The sharded join method in Crunch is similar, but requires the
hot keys to be specified explicitly rather than using a sampling job. This technique is
also very similar to one we discussed in “Skewed Workloads and Relieving Hot
Spots” on page 205, using randomization to alleviate hot spots in a partitioned data‐
base.
Hive’s skewed join optimization takes an alternative approach. It requires hot keys to
be specified explicitly in the table metadata, and it stores records related to those keys
in separate files from the rest. When performing a join on that table, it uses a mapside join (see the next section) for the hot keys.
When grouping records by a hot key and aggregating them, you can perform the
grouping in two stages. The first MapReduce stage sends records to a random
reducer, so that each reducer performs the grouping on a subset of records for the
hot key and outputs a more compact aggregated value per key. The second Map‐
Reduce job then combines the values from all of the first-stage reducers into a single
value per key. 
Map-Side Joins
The join algorithms described in the last section perform the actual join logic in the
reducers, and are hence known as reduce-side joins. The mappers take the role of pre‐
paring the input data: extracting the key and value from each input record, assigning
the key-value pairs to a reducer partition, and sorting by key.
The reduce-side approach has the advantage that you do not need to make any
assumptions about the input data: whatever its properties and structure, the mappers
can prepare the data to be ready for joining. However, the downside is that all that
sorting, copying to reducers, and merging of reducer inputs can be quite expensive.
Depending on the available memory buffers, data may be written to disk several
times as it passes through the stages of MapReduce [37].
On the other hand, if you can make certain assumptions about your input data, it is
possible to make joins faster by using a so-called map-side join. This approach uses a
cut-down MapReduce job in which there are no reducers and no sorting. Instead,
each mapper simply reads one input file block from the distributed filesystem and
writes one output file to the filesystem—that is all.
408 
| 
Chapter 10: Batch Processing


vi. This example assumes that there is exactly one entry for each key in the hash table, which is probably true
with a user database (a user ID uniquely identifies a user). In general, the hash table may need to contain
several entries with the same key, and the join operator will output all matches for a key.
Broadcast hash joins
The simplest way of performing a map-side join applies in the case where a large
dataset is joined with a small dataset. In particular, the small dataset needs to be small
enough that it can be loaded entirely into memory in each of the mappers.
For example, imagine in the case of Figure 10-2 that the user database is small
enough to fit in memory. In this case, when a mapper starts up, it can first read the
user database from the distributed filesystem into an in-memory hash table. Once
this is done, the mapper can scan over the user activity events and simply look up the
user ID for each event in the hash table.vi
There can still be several map tasks: one for each file block of the large input to the
join (in the example of Figure 10-2, the activity events are the large input). Each of
these mappers loads the small input entirely into memory.
This simple but effective algorithm is called a broadcast hash join: the word broadcast
reflects the fact that each mapper for a partition of the large input reads the entirety
of the small input (so the small input is effectively “broadcast” to all partitions of the
large input), and the word hash reflects its use of a hash table. This join method is
supported by Pig (under the name “replicated join”), Hive (“MapJoin”), Cascading,
and Crunch. It is also used in data warehouse query engines such as Impala [41].
Instead of loading the small join input into an in-memory hash table, an alternative is
to store the small join input in a read-only index on the local disk [42]. The fre‐
quently used parts of this index will remain in the operating system’s page cache, so
this approach can provide random-access lookups almost as fast as an in-memory
hash table, but without actually requiring the dataset to fit in memory.
Partitioned hash joins
If the inputs to the map-side join are partitioned in the same way, then the hash join
approach can be applied to each partition independently. In the case of Figure 10-2,
you might arrange for the activity events and the user database to each be partitioned
based on the last decimal digit of the user ID (so there are 10 partitions on either
side). For example, mapper 3 first loads all users with an ID ending in 3 into a hash
table, and then scans over all the activity events for each user whose ID ends in 3.
If the partitioning is done correctly, you can be sure that all the records you might
want to join are located in the same numbered partition, and so it is sufficient for
each mapper to only read one partition from each of the input datasets. This has the
advantage that each mapper can load a smaller amount of data into its hash table.
MapReduce and Distributed Filesystems 
| 
409


This approach only works if both of the join’s inputs have the same number of parti‐
tions, with records assigned to partitions based on the same key and the same hash
function. If the inputs are generated by prior MapReduce jobs that already perform
this grouping, then this can be a reasonable assumption to make.
Partitioned hash joins are known as bucketed map joins in Hive [37].
Map-side merge joins
Another variant of a map-side join applies if the input datasets are not only parti‐
tioned in the same way, but also sorted based on the same key. In this case, it does not
matter whether the inputs are small enough to fit in memory, because a mapper can
perform the same merging operation that would normally be done by a reducer:
reading both input files incrementally, in order of ascending key, and matching
records with the same key.
If a map-side merge join is possible, it probably means that prior MapReduce jobs
brought the input datasets into this partitioned and sorted form in the first place. In
principle, this join could have been performed in the reduce stage of the prior job.
However, it may still be appropriate to perform the merge join in a separate maponly job, for example if the partitioned and sorted datasets are also needed for other
purposes besides this particular join.
MapReduce workflows with map-side joins
When the output of a MapReduce join is consumed by downstream jobs, the choice
of map-side or reduce-side join affects the structure of the output. The output of a
reduce-side join is partitioned and sorted by the join key, whereas the output of a
map-side join is partitioned and sorted in the same way as the large input (since one
map task is started for each file block of the join’s large input, regardless of whether a
partitioned or broadcast join is used).
As discussed, map-side joins also make more assumptions about the size, sorting, and
partitioning of their input datasets. Knowing about the physical layout of datasets in
the distributed filesystem becomes important when optimizing join strategies: it is
not sufficient to just know the encoding format and the name of the directory in
which the data is stored; you must also know the number of partitions and the keys
by which the data is partitioned and sorted.
In the Hadoop ecosystem, this kind of metadata about the partitioning of datasets is
often maintained in HCatalog and the Hive metastore [37]. 
410 
| 
Chapter 10: Batch Processing


The Output of Batch Workflows
We have talked a lot about the various algorithms for implementing workflows of
MapReduce jobs, but we neglected an important question: what is the result of all of
that processing, once it is done? Why are we running all these jobs in the first place?
In the case of database queries, we distinguished transaction processing (OLTP) pur‐
poses from analytic purposes (see “Transaction Processing or Analytics?” on page
90). We saw that OLTP queries generally look up a small number of records by key,
using indexes, in order to present them to a user (for example, on a web page). On
the other hand, analytic queries often scan over a large number of records, perform‐
ing groupings and aggregations, and the output often has the form of a report: a
graph showing the change in a metric over time, or the top 10 items according to
some ranking, or a breakdown of some quantity into subcategories. The consumer of
such a report is often an analyst or a manager who needs to make business decisions.
Where does batch processing fit in? It is not transaction processing, nor is it analyt‐
ics. It is closer to analytics, in that a batch process typically scans over large portions
of an input dataset. However, a workflow of MapReduce jobs is not the same as a
SQL query used for analytic purposes (see “Comparing Hadoop to Distributed Data‐
bases” on page 414). The output of a batch process is often not a report, but some
other kind of structure.
Building search indexes
Google’s original use of MapReduce was to build indexes for its search engine, which
was implemented as a workflow of 5 to 10 MapReduce jobs [1]. Although Google
later moved away from using MapReduce for this purpose [43], it helps to under‐
stand MapReduce if you look at it through the lens of building a search index. (Even
today, Hadoop MapReduce remains a good way of building indexes for Lucene/Solr
[44].)
We saw briefly in “Full-text search and fuzzy indexes” on page 88 how a full-text
search index such as Lucene works: it is a file (the term dictionary) in which you can
efficiently look up a particular keyword and find the list of all the document IDs con‐
taining that keyword (the postings list). This is a very simplified view of a search
index—in reality it requires various additional data, in order to rank search results by
relevance, correct misspellings, resolve synonyms, and so on—but the principle
holds.
If you need to perform a full-text search over a fixed set of documents, then a batch
process is a very effective way of building the indexes: the mappers partition the set of
documents as needed, each reducer builds the index for its partition, and the index
files are written to the distributed filesystem. Building such document-partitioned
indexes (see “Partitioning and Secondary Indexes” on page 206) parallelizes very well.
MapReduce and Distributed Filesystems 
| 
411


Since querying a search index by keyword is a read-only operation, these index files
are immutable once they have been created.
If the indexed set of documents changes, one option is to periodically rerun the entire
indexing workflow for the entire set of documents, and replace the previous index
files wholesale with the new index files when it is done. This approach can be compu‐
tationally expensive if only a small number of documents have changed, but it has the
advantage that the indexing process is very easy to reason about: documents in,
indexes out.
Alternatively, it is possible to build indexes incrementally. As discussed in Chapter 3,
if you want to add, remove, or update documents in an index, Lucene writes out new
segment files and asynchronously merges and compacts segment files in the back‐
ground. We will see more on such incremental processing in Chapter 11.
Key-value stores as batch process output
Search indexes are just one example of the possible outputs of a batch processing
workflow. Another common use for batch processing is to build machine learning
systems such as classifiers (e.g., spam filters, anomaly detection, image recognition)
and recommendation systems (e.g., people you may know, products you may be
interested in, or related searches [29]).
The output of those batch jobs is often some kind of database: for example, a data‐
base that can be queried by user ID to obtain suggested friends for that user, or a
database that can be queried by product ID to get a list of related products [45].
These databases need to be queried from the web application that handles user
requests, which is usually separate from the Hadoop infrastructure. So how does the
output from the batch process get back into a database where the web application can
query it?
The most obvious choice might be to use the client library for your favorite database
directly within a mapper or reducer, and to write from the batch job directly to the
database server, one record at a time. This will work (assuming your firewall rules
allow direct access from your Hadoop environment to your production databases),
but it is a bad idea for several reasons:
• As discussed previously in the context of joins, making a network request for
every single record is orders of magnitude slower than the normal throughput of
a batch task. Even if the client library supports batching, performance is likely to
be poor.
• MapReduce jobs often run many tasks in parallel. If all the mappers or reducers
concurrently write to the same output database, with a rate expected of a batch
process, that database can easily be overwhelmed, and its performance for quer‐
412 
| 
Chapter 10: Batch Processing


ies is likely to suffer. This can in turn cause operational problems in other parts
of the system [35].
• Normally, MapReduce provides a clean all-or-nothing guarantee for job output:
if a job succeeds, the result is the output of running every task exactly once, even
if some tasks failed and had to be retried along the way; if the entire job fails, no
output is produced. However, writing to an external system from inside a job
produces externally visible side effects that cannot be hidden in this way. Thus,
you have to worry about the results from partially completed jobs being visible to
other systems, and the complexities of Hadoop task attempts and speculative
execution.
A much better solution is to build a brand-new database inside the batch job and
write it as files to the job’s output directory in the distributed filesystem, just like the
search indexes in the last section. Those data files are then immutable once written,
and can be loaded in bulk into servers that handle read-only queries. Various keyvalue stores support building database files in MapReduce jobs, including Voldemort
[46], Terrapin [47], ElephantDB [48], and HBase bulk loading [49].
Building these database files is a good use of MapReduce: using a mapper to extract a
key and then sorting by that key is already a lot of the work required to build an
index. Since most of these key-value stores are read-only (the files can only be written
once by a batch job and are then immutable), the data structures are quite simple. For
example, they do not require a WAL (see “Making B-trees reliable” on page 82).
When loading data into Voldemort, the server continues serving requests to the old
data files while the new data files are copied from the distributed filesystem to the
server’s local disk. Once the copying is complete, the server atomically switches over
to querying the new files. If anything goes wrong in this process, it can easily switch
back to the old files again, since they are still there and immutable [46]. 
Philosophy of batch process outputs
The Unix philosophy that we discussed earlier in this chapter (“The Unix Philoso‐
phy” on page 394) encourages experimentation by being very explicit about dataflow:
a program reads its input and writes its output. In the process, the input is left
unchanged, any previous output is completely replaced with the new output, and
there are no other side effects. This means that you can rerun a command as often as
you like, tweaking or debugging it, without messing up the state of your system.
The handling of output from MapReduce jobs follows the same philosophy. By treat‐
ing inputs as immutable and avoiding side effects (such as writing to external data‐
bases), batch jobs not only achieve good performance but also become much easier to
maintain:
MapReduce and Distributed Filesystems 
| 
413


• If you introduce a bug into the code and the output is wrong or corrupted, you
can simply roll back to a previous version of the code and rerun the job, and the
output will be correct again. Or, even simpler, you can keep the old output in a
different directory and simply switch back to it. Databases with read-write trans‐
actions do not have this property: if you deploy buggy code that writes bad data
to the database, then rolling back the code will do nothing to fix the data in the
database. (The idea of being able to recover from buggy code has been called
human fault tolerance [50].)
• As a consequence of this ease of rolling back, feature development can proceed
more quickly than in an environment where mistakes could mean irreversible
damage. This principle of minimizing irreversibility is beneficial for Agile soft‐
ware development [51].
• If a map or reduce task fails, the MapReduce framework automatically reschedules it and runs it again on the same input. If the failure is due to a bug in
the code, it will keep crashing and eventually cause the job to fail after a few
attempts; but if the failure is due to a transient issue, the fault is tolerated. This
automatic retry is only safe because inputs are immutable and outputs from
failed tasks are discarded by the MapReduce framework.
• The same set of files can be used as input for various different jobs, including
monitoring jobs that calculate metrics and evaluate whether a job’s output has
the expected characteristics (for example, by comparing it to the output from the
previous run and measuring discrepancies).
• Like Unix tools, MapReduce jobs separate logic from wiring (configuring the
input and output directories), which provides a separation of concerns and ena‐
bles potential reuse of code: one team can focus on implementing a job that does
one thing well, while other teams can decide where and when to run that job.
In these areas, the design principles that worked well for Unix also seem to be work‐
ing well for Hadoop—but Unix and Hadoop also differ in some ways. For example,
because most Unix tools assume untyped text files, they have to do a lot of input
parsing (our log analysis example at the beginning of the chapter used {print $7} to
extract the URL). On Hadoop, some of those low-value syntactic conversions are
eliminated by using more structured file formats: Avro (see “Avro” on page 122) and
Parquet (see “Column-Oriented Storage” on page 95) are often used, as they provide
efficient schema-based encoding and allow evolution of their schemas over time (see
Chapter 4). 
Comparing Hadoop to Distributed Databases
As we have seen, Hadoop is somewhat like a distributed version of Unix, where
HDFS is the filesystem and MapReduce is a quirky implementation of a Unix process
414 
| 
Chapter 10: Batch Processing


(which happens to always run the sort utility between the map phase and the reduce
phase). We saw how you can implement various join and grouping operations on top
of these primitives.
When the MapReduce paper [1] was published, it was—in some sense—not at all
new. All of the processing and parallel join algorithms that we discussed in the last
few sections had already been implemented in so-called massively parallel processing
(MPP) databases more than a decade previously [3, 40]. For example, the Gamma
database machine, Teradata, and Tandem NonStop SQL were pioneers in this area
[52].
The biggest difference is that MPP databases focus on parallel execution of analytic
SQL queries on a cluster of machines, while the combination of MapReduce and a
distributed filesystem [19] provides something much more like a general-purpose
operating system that can run arbitrary programs.
Diversity of storage
Databases require you to structure data according to a particular model (e.g., rela‐
tional or documents), whereas files in a distributed filesystem are just byte sequences,
which can be written using any data model and encoding. They might be collections
of database records, but they can equally well be text, images, videos, sensor readings,
sparse matrices, feature vectors, genome sequences, or any other kind of data.
To put it bluntly, Hadoop opened up the possibility of indiscriminately dumping data
into HDFS, and only later figuring out how to process it further [53]. By contrast,
MPP databases typically require careful up-front modeling of the data and query pat‐
terns before importing the data into the database’s proprietary storage format.
From a purist’s point of view, it may seem that this careful modeling and import is
desirable, because it means users of the database have better-quality data to work
with. However, in practice, it appears that simply making data available quickly—
even if it is in a quirky, difficult-to-use, raw format—is often more valuable than try‐
ing to decide on the ideal data model up front [54].
The idea is similar to a data warehouse (see “Data Warehousing” on page 91): simply
bringing data from various parts of a large organization together in one place is val‐
uable, because it enables joins across datasets that were previously disparate. The
careful schema design required by an MPP database slows down that centralized data
collection; collecting data in its raw form, and worrying about schema design later,
allows the data collection to be speeded up (a concept sometimes known as a “data
lake” or “enterprise data hub” [55]).
Indiscriminate data dumping shifts the burden of interpreting the data: instead of
forcing the producer of a dataset to bring it into a standardized format, the interpre‐
tation of the data becomes the consumer’s problem (the schema-on-read approach
MapReduce and Distributed Filesystems 
| 
415


[56]; see “Schema flexibility in the document model” on page 39). This can be an
advantage if the producer and consumers are different teams with different priorities.
There may not even be one ideal data model, but rather different views onto the data
that are suitable for different purposes. Simply dumping data in its raw form allows
for several such transformations. This approach has been dubbed the sushi principle:
“raw data is better” [57].
Thus, Hadoop has often been used for implementing ETL processes (see “Data Ware‐
housing” on page 91): data from transaction processing systems is dumped into the
distributed filesystem in some raw form, and then MapReduce jobs are written to
clean up that data, transform it into a relational form, and import it into an MPP data
warehouse for analytic purposes. Data modeling still happens, but it is in a separate
step, decoupled from the data collection. This decoupling is possible because a dis‐
tributed filesystem supports data encoded in any format.
Diversity of processing models
MPP databases are monolithic, tightly integrated pieces of software that take care of
storage layout on disk, query planning, scheduling, and execution. Since these com‐
ponents can all be tuned and optimized for the specific needs of the database, the sys‐
tem as a whole can achieve very good performance on the types of queries for which
it is designed. Moreover, the SQL query language allows expressive queries and ele‐
gant semantics without the need to write code, making it accessible to graphical tools
used by business analysts (such as Tableau).
On the other hand, not all kinds of processing can be sensibly expressed as SQL quer‐
ies. For example, if you are building machine learning and recommendation systems,
or full-text search indexes with relevance ranking models, or performing image anal‐
ysis, you most likely need a more general model of data processing. These kinds of
processing are often very specific to a particular application (e.g., feature engineering
for machine learning, natural language models for machine translation, risk estima‐
tion functions for fraud prediction), so they inevitably require writing code, not just
queries.
MapReduce gave engineers the ability to easily run their own code over large data‐
sets. If you have HDFS and MapReduce, you can build a SQL query execution engine
on top of it, and indeed this is what the Hive project did [31]. However, you can also
write many other forms of batch processes that do not lend themselves to being
expressed as a SQL query.
Subsequently, people found that MapReduce was too limiting and performed too
badly for some types of processing, so various other processing models were devel‐
oped on top of Hadoop (we will see some of them in “Beyond MapReduce” on page
419). Having two processing models, SQL and MapReduce, was not enough: even
more different models were needed! And due to the openness of the Hadoop plat‐
416 
| 
Chapter 10: Batch Processing


form, it was feasible to implement a whole range of approaches, which would not
have been possible within the confines of a monolithic MPP database [58].
Crucially, those various processing models can all be run on a single shared-use clus‐
ter of machines, all accessing the same files on the distributed filesystem. In the
Hadoop approach, there is no need to import the data into several different special‐
ized systems for different kinds of processing: the system is flexible enough to sup‐
port a diverse set of workloads within the same cluster. Not having to move data
around makes it a lot easier to derive value from the data, and a lot easier to experi‐
ment with new processing models.
The Hadoop ecosystem includes both random-access OLTP databases such as HBase
(see “SSTables and LSM-Trees” on page 76) and MPP-style analytic databases such as
Impala [41]. Neither HBase nor Impala uses MapReduce, but both use HDFS for
storage. They are very different approaches to accessing and processing data, but they
can nevertheless coexist and be integrated in the same system.
Designing for frequent faults
When comparing MapReduce to MPP databases, two more differences in design
approach stand out: the handling of faults and the use of memory and disk. Batch
processes are less sensitive to faults than online systems, because they do not immedi‐
ately affect users if they fail and they can always be run again.
If a node crashes while a query is executing, most MPP databases abort the entire
query, and either let the user resubmit the query or automatically run it again [3]. As
queries normally run for a few seconds or a few minutes at most, this way of handling
errors is acceptable, since the cost of retrying is not too great. MPP databases also
prefer to keep as much data as possible in memory (e.g., using hash joins) to avoid
the cost of reading from disk.
On the other hand, MapReduce can tolerate the failure of a map or reduce task
without it affecting the job as a whole by retrying work at the granularity of an indi‐
vidual task. It is also very eager to write data to disk, partly for fault tolerance, and
partly on the assumption that the dataset will be too big to fit in memory anyway.
The MapReduce approach is more appropriate for larger jobs: jobs that process so
much data and run for such a long time that they are likely to experience at least one
task failure along the way. In that case, rerunning the entire job due to a single task
failure would be wasteful. Even if recovery at the granularity of an individual task
introduces overheads that make fault-free processing slower, it can still be a reason‐
able trade-off if the rate of task failures is high enough.
But how realistic are these assumptions? In most clusters, machine failures do occur,
but they are not very frequent—probably rare enough that most jobs will not experi‐
MapReduce and Distributed Filesystems 
| 
417


ence a machine failure. Is it really worth incurring significant overheads for the sake
of fault tolerance?
To understand the reasons for MapReduce’s sparing use of memory and task-level
recovery, it is helpful to look at the environment for which MapReduce was originally
designed. Google has mixed-use datacenters, in which online production services and
offline batch jobs run on the same machines. Every task has a resource allocation
(CPU cores, RAM, disk space, etc.) that is enforced using containers. Every task also
has a priority, and if a higher-priority task needs more resources, lower-priority tasks
on the same machine can be terminated (preempted) in order to free up resources.
Priority also determines pricing of the computing resources: teams must pay for the
resources they use, and higher-priority processes cost more [59].
This architecture allows non-production (low-priority) computing resources to be
overcommitted, because the system knows that it can reclaim the resources if neces‐
sary. Overcommitting resources in turn allows better utilization of machines and
greater efficiency compared to systems that segregate production and nonproduction tasks. However, as MapReduce jobs run at low priority, they run the risk
of being preempted at any time because a higher-priority process requires their
resources. Batch jobs effectively “pick up the scraps under the table,” using any com‐
puting resources that remain after the high-priority processes have taken what they
need.
At Google, a MapReduce task that runs for an hour has an approximately 5% risk of
being terminated to make space for a higher-priority process. This rate is more than
an order of magnitude higher than the rate of failures due to hardware issues,
machine reboot, or other reasons [59]. At this rate of preemptions, if a job has 100
tasks that each run for 10 minutes, there is a risk greater than 50% that at least one
task will be terminated before it is finished.
And this is why MapReduce is designed to tolerate frequent unexpected task termina‐
tion: it’s not because the hardware is particularly unreliable, it’s because the freedom
to arbitrarily terminate processes enables better resource utilization in a computing
cluster.
Among open source cluster schedulers, preemption is less widely used. YARN’s
CapacityScheduler supports preemption for balancing the resource allocation of dif‐
ferent queues [58], but general priority preemption is not supported in YARN,
Mesos, or Kubernetes at the time of writing [60]. In an environment where tasks are
not so often terminated, the design decisions of MapReduce make less sense. In the
next section, we will look at some alternatives to MapReduce that make different
design decisions. 
418 
| 
Chapter 10: Batch Processing


Beyond MapReduce
Although MapReduce became very popular and received a lot of hype in the late
2000s, it is just one among many possible programming models for distributed sys‐
tems. Depending on the volume of data, the structure of the data, and the type of pro‐
cessing being done with it, other tools may be more appropriate for expressing a
computation.
We nevertheless spent a lot of time in this chapter discussing MapReduce because it
is a useful learning tool, as it is a fairly clear and simple abstraction on top of a dis‐
tributed filesystem. That is, simple in the sense of being able to understand what it is
doing, not in the sense of being easy to use. Quite the opposite: implementing a com‐
plex processing job using the raw MapReduce APIs is actually quite hard and labori‐
ous—for instance, you would need to implement any join algorithms from scratch
[37].
In response to the difficulty of using MapReduce directly, various higher-level pro‐
gramming models (Pig, Hive, Cascading, Crunch) were created as abstractions on top
of MapReduce. If you understand how MapReduce works, they are fairly easy to
learn, and their higher-level constructs make many common batch processing tasks
significantly easier to implement.
However, there are also problems with the MapReduce execution model itself, which
are not fixed by adding another level of abstraction and which manifest themselves as
poor performance for some kinds of processing. On the one hand, MapReduce is
very robust: you can use it to process almost arbitrarily large quantities of data on an
unreliable multi-tenant system with frequent task terminations, and it will still get the
job done (albeit slowly). On the other hand, other tools are sometimes orders of mag‐
nitude faster for some kinds of processing.
In the rest of this chapter, we will look at some of those alternatives for batch process‐
ing. In Chapter 11 we will move to stream processing, which can be regarded as
another way of speeding up batch processing.
Materialization of Intermediate State
As discussed previously, every MapReduce job is independent from every other job.
The main contact points of a job with the rest of the world are its input and output
directories on the distributed filesystem. If you want the output of one job to become
the input to a second job, you need to configure the second job’s input directory to be
the same as the first job’s output directory, and an external workflow scheduler must
start the second job only once the first job has completed.
This setup is reasonable if the output from the first job is a dataset that you want to
publish widely within your organization. In that case, you need to be able to refer to it
Beyond MapReduce 
| 
419


by name and reuse it as input to several different jobs (including jobs developed by
other teams). Publishing data to a well-known location in the distributed filesystem
allows loose coupling so that jobs don’t need to know who is producing their input or
consuming their output (see “Separation of logic and wiring” on page 396).
However, in many cases, you know that the output of one job is only ever used as
input to one other job, which is maintained by the same team. In this case, the files
on the distributed filesystem are simply intermediate state: a means of passing data
from one job to the next. In the complex workflows used to build recommendation
systems consisting of 50 or 100 MapReduce jobs [29], there is a lot of such intermedi‐
ate state.
The process of writing out this intermediate state to files is called materialization.
(We came across the term previously in the context of materialized views, in “Aggre‐
gation: Data Cubes and Materialized Views” on page 101. It means to eagerly com‐
pute the result of some operation and write it out, rather than computing it on
demand when requested.)
By contrast, the log analysis example at the beginning of the chapter used Unix pipes
to connect the output of one command with the input of another. Pipes do not fully
materialize the intermediate state, but instead stream the output to the input incre‐
mentally, using only a small in-memory buffer.
MapReduce’s approach of fully materializing intermediate state has downsides com‐
pared to Unix pipes:
• A MapReduce job can only start when all tasks in the preceding jobs (that gener‐
ate its inputs) have completed, whereas processes connected by a Unix pipe are
started at the same time, with output being consumed as soon as it is produced.
Skew or varying load on different machines means that a job often has a few
straggler tasks that take much longer to complete than the others. Having to wait
until all of the preceding job’s tasks have completed slows down the execution of
the workflow as a whole.
• Mappers are often redundant: they just read back the same file that was just writ‐
ten by a reducer, and prepare it for the next stage of partitioning and sorting. In
many cases, the mapper code could be part of the previous reducer: if the reducer
output was partitioned and sorted in the same way as mapper output, then
reducers could be chained together directly, without interleaving with mapper
stages.
• Storing intermediate state in a distributed filesystem means those files are repli‐
cated across several nodes, which is often overkill for such temporary data.
420 
| 
Chapter 10: Batch Processing


Dataflow engines
In order to fix these problems with MapReduce, several new execution engines for
distributed batch computations were developed, the most well known of which are
Spark [61, 62], Tez [63, 64], and Flink [65, 66]. There are various differences in the
way they are designed, but they have one thing in common: they handle an entire
workflow as one job, rather than breaking it up into independent subjobs.
Since they explicitly model the flow of data through several processing stages, these
systems are known as dataflow engines. Like MapReduce, they work by repeatedly
calling a user-defined function to process one record at a time on a single thread.
They parallelize work by partitioning inputs, and they copy the output of one func‐
tion over the network to become the input to another function.
Unlike in MapReduce, these functions need not take the strict roles of alternating
map and reduce, but instead can be assembled in more flexible ways. We call these
functions operators, and the dataflow engine provides several different options for
connecting one operator’s output to another’s input:
• One option is to repartition and sort records by key, like in the shuffle stage of
MapReduce (see “Distributed execution of MapReduce” on page 400). This fea‐
ture enables sort-merge joins and grouping in the same way as in MapReduce.
• Another possibility is to take several inputs and to partition them in the same
way, but skip the sorting. This saves effort on partitioned hash joins, where the
partitioning of records is important but the order is irrelevant because building
the hash table randomizes the order anyway.
• For broadcast hash joins, the same output from one operator can be sent to all
partitions of the join operator.
This style of processing engine is based on research systems like Dryad [67] and
Nephele [68], and it offers several advantages compared to the MapReduce model:
• Expensive work such as sorting need only be performed in places where it is
actually required, rather than always happening by default between every map
and reduce stage.
• There are no unnecessary map tasks, since the work done by a mapper can often
be incorporated into the preceding reduce operator (because a mapper does not
change the partitioning of a dataset).
• Because all joins and data dependencies in a workflow are explicitly declared, the
scheduler has an overview of what data is required where, so it can make locality
optimizations. For example, it can try to place the task that consumes some data
on the same machine as the task that produces it, so that the data can be
Beyond MapReduce 
| 
421


exchanged through a shared memory buffer rather than having to copy it over
the network.
• It is usually sufficient for intermediate state between operators to be kept in
memory or written to local disk, which requires less I/O than writing it to HDFS
(where it must be replicated to several machines and written to disk on each rep‐
lica). MapReduce already uses this optimization for mapper output, but dataflow
engines generalize the idea to all intermediate state.
• Operators can start executing as soon as their input is ready; there is no need to
wait for the entire preceding stage to finish before the next one starts.
• Existing Java Virtual Machine (JVM) processes can be reused to run new opera‐
tors, reducing startup overheads compared to MapReduce (which launches a
new JVM for each task).
You can use dataflow engines to implement the same computations as MapReduce
workflows, and they usually execute significantly faster due to the optimizations
described here. Since operators are a generalization of map and reduce, the same pro‐
cessing code can run on either execution engine: workflows implemented in Pig,
Hive, or Cascading can be switched from MapReduce to Tez or Spark with a simple
configuration change, without modifying code [64].
Tez is a fairly thin library that relies on the YARN shuffle service for the actual copy‐
ing of data between nodes [58], whereas Spark and Flink are big frameworks that
include their own network communication layer, scheduler, and user-facing APIs.
We will discuss those high-level APIs shortly.
Fault tolerance
An advantage of fully materializing intermediate state to a distributed filesystem is
that it is durable, which makes fault tolerance fairly easy in MapReduce: if a task fails,
it can just be restarted on another machine and read the same input again from the
filesystem.
Spark, Flink, and Tez avoid writing intermediate state to HDFS, so they take a differ‐
ent approach to tolerating faults: if a machine fails and the intermediate state on that
machine is lost, it is recomputed from other data that is still available (a prior inter‐
mediary stage if possible, or otherwise the original input data, which is normally on
HDFS).
To enable this recomputation, the framework must keep track of how a given piece of
data was computed—which input partitions it used, and which operators were
applied to it. Spark uses the resilient distributed dataset (RDD) abstraction for track‐
ing the ancestry of data [61], while Flink checkpoints operator state, allowing it to
resume running an operator that ran into a fault during its execution [66].
422 
| 
Chapter 10: Batch Processing


When recomputing data, it is important to know whether the computation is deter‐
ministic: that is, given the same input data, do the operators always produce the same
output? This question matters if some of the lost data has already been sent to down‐
stream operators. If the operator is restarted and the recomputed data is not the same
as the original lost data, it becomes very hard for downstream operators to resolve the
contradictions between the old and new data. The solution in the case of nondeter‐
ministic operators is normally to kill the downstream operators as well, and run them
again on the new data.
In order to avoid such cascading faults, it is better to make operators deterministic.
Note however that it is easy for nondeterministic behavior to accidentally creep in:
for example, many programming languages do not guarantee any particular order
when iterating over elements of a hash table, many probabilistic and statistical
algorithms explicitly rely on using random numbers, and any use of the system clock
or external data sources is nondeterministic. Such causes of nondeterminism need to
be removed in order to reliably recover from faults, for example by generating
pseudorandom numbers using a fixed seed.
Recovering from faults by recomputing data is not always the right answer: if the
intermediate data is much smaller than the source data, or if the computation is very
CPU-intensive, it is probably cheaper to materialize the intermediate data to files
than to recompute it.
Discussion of materialization
Returning to the Unix analogy, we saw that MapReduce is like writing the output of
each command to a temporary file, whereas dataflow engines look much more like
Unix pipes. Flink especially is built around the idea of pipelined execution: that is,
incrementally passing the output of an operator to other operators, and not waiting
for the input to be complete before starting to process it.
A sorting operation inevitably needs to consume its entire input before it can pro‐
duce any output, because it’s possible that the very last input record is the one with
the lowest key and thus needs to be the very first output record. Any operator that
requires sorting will thus need to accumulate state, at least temporarily. But many
other parts of a workflow can be executed in a pipelined manner.
When the job completes, its output needs to go somewhere durable so that users can
find it and use it—most likely, it is written to the distributed filesystem again. Thus,
when using a dataflow engine, materialized datasets on HDFS are still usually the
inputs and the final outputs of a job. Like with MapReduce, the inputs are immutable
and the output is completely replaced. The improvement over MapReduce is that you
save yourself writing all the intermediate state to the filesystem as well. 
Beyond MapReduce 
| 
423


Graphs and Iterative Processing
In “Graph-Like Data Models” on page 49 we discussed using graphs for modeling
data, and using graph query languages to traverse the edges and vertices in a graph.
The discussion in Chapter 2 was focused around OLTP-style use: quickly executing
queries to find a small number of vertices matching certain criteria.
It is also interesting to look at graphs in a batch processing context, where the goal is
to perform some kind of offline processing or analysis on an entire graph. This need
often arises in machine learning applications such as recommendation engines, or in
ranking systems. For example, one of the most famous graph analysis algorithms is
PageRank [69], which tries to estimate the popularity of a web page based on what
other web pages link to it. It is used as part of the formula that determines the order
in which web search engines present their results.
Dataflow engines like Spark, Flink, and Tez (see “Materialization of
Intermediate State” on page 419) typically arrange the operators in
a job as a directed acyclic graph (DAG). This is not the same as
graph processing: in dataflow engines, the flow of data from one
operator to another is structured as a graph, while the data itself
typically consists of relational-style tuples. In graph processing, the
data itself has the form of a graph. Another unfortunate naming
confusion!
Many graph algorithms are expressed by traversing one edge at a time, joining one
vertex with an adjacent vertex in order to propagate some information, and repeating
until some condition is met—for example, until there are no more edges to follow, or
until some metric converges. We saw an example in Figure 2-6, which made a list of
all the locations in North America contained in a database by repeatedly following
edges indicating which location is within which other location (this kind of algorithm
is called a transitive closure).
It is possible to store a graph in a distributed filesystem (in files containing lists of
vertices and edges), but this idea of “repeating until done” cannot be expressed in
plain MapReduce, since it only performs a single pass over the data. This kind of
algorithm is thus often implemented in an iterative style:
1. An external scheduler runs a batch process to calculate one step of the algorithm.
2. When the batch process completes, the scheduler checks whether it has finished
(based on the completion condition—e.g., there are no more edges to follow, or
the change compared to the last iteration is below some threshold).
3. If it has not yet finished, the scheduler goes back to step 1 and runs another
round of the batch process.
424 
| 
Chapter 10: Batch Processing


This approach works, but implementing it with MapReduce is often very inefficient,
because MapReduce does not account for the iterative nature of the algorithm: it will
always read the entire input dataset and produce a completely new output dataset,
even if only a small part of the graph has changed compared to the last iteration.
The Pregel processing model
As an optimization for batch processing graphs, the bulk synchronous parallel (BSP)
model of computation [70] has become popular. Among others, it is implemented by
Apache Giraph [37], Spark’s GraphX API, and Flink’s Gelly API [71]. It is also
known as the Pregel model, as Google’s Pregel paper popularized this approach for
processing graphs [72].
Recall that in MapReduce, mappers conceptually “send a message” to a particular call
of the reducer because the framework collects together all the mapper outputs with
the same key. A similar idea is behind Pregel: one vertex can “send a message” to
another vertex, and typically those messages are sent along the edges in a graph.
In each iteration, a function is called for each vertex, passing it all the messages that
were sent to it—much like a call to the reducer. The difference from MapReduce is
that in the Pregel model, a vertex remembers its state in memory from one iteration
to the next, so the function only needs to process new incoming messages. If no mes‐
sages are being sent in some part of the graph, no work needs to be done.
It’s a bit similar to the actor model (see “Distributed actor frameworks” on page 138),
if you think of each vertex as an actor, except that vertex state and messages between
vertices are fault-tolerant and durable, and communication proceeds in fixed rounds:
at every iteration, the framework delivers all messages sent in the previous iteration.
Actors normally have no such timing guarantee.
Fault tolerance
The fact that vertices can only communicate by message passing (not by querying
each other directly) helps improve the performance of Pregel jobs, since messages can
be batched and there is less waiting for communication. The only waiting is between
iterations: since the Pregel model guarantees that all messages sent in one iteration
are delivered in the next iteration, the prior iteration must completely finish, and all
of its messages must be copied over the network, before the next one can start.
Even though the underlying network may drop, duplicate, or arbitrarily delay mes‐
sages (see “Unreliable Networks” on page 277), Pregel implementations guarantee
that messages are processed exactly once at their destination vertex in the following
iteration. Like MapReduce, the framework transparently recovers from faults in
order to simplify the programming model for algorithms on top of Pregel.
Beyond MapReduce 
| 
425


This fault tolerance is achieved by periodically checkpointing the state of all vertices
at the end of an iteration—i.e., writing their full state to durable storage. If a node
fails and its in-memory state is lost, the simplest solution is to roll back the entire
graph computation to the last checkpoint and restart the computation. If the algo‐
rithm is deterministic and messages are logged, it is also possible to selectively
recover only the partition that was lost (like we previously discussed for dataflow
engines) [72].
Parallel execution
A vertex does not need to know on which physical machine it is executing; when it
sends messages to other vertices, it simply sends them to a vertex ID. It is up to the
framework to partition the graph—i.e., to decide which vertex runs on which
machine, and how to route messages over the network so that they end up in the
right place.
Because the programming model deals with just one vertex at a time (sometimes
called “thinking like a vertex”), the framework may partition the graph in arbitrary
ways. Ideally it would be partitioned such that vertices are colocated on the same
machine if they need to communicate a lot. However, finding such an optimized par‐
titioning is hard—in practice, the graph is often simply partitioned by an arbitrarily
assigned vertex ID, making no attempt to group related vertices together.
As a result, graph algorithms often have a lot of cross-machine communication over‐
head, and the intermediate state (messages sent between nodes) is often bigger than
the original graph. The overhead of sending messages over the network can signifi‐
cantly slow down distributed graph algorithms.
For this reason, if your graph can fit in memory on a single computer, it’s quite likely
that a single-machine (maybe even single-threaded) algorithm will outperform a dis‐
tributed batch process [73, 74]. Even if the graph is bigger than memory, it can fit on
the disks of a single computer, single-machine processing using a framework such as
GraphChi is a viable option [75]. If the graph is too big to fit on a single machine, a
distributed approach such as Pregel is unavoidable; efficiently parallelizing graph
algorithms is an area of ongoing research [76]. 
High-Level APIs and Languages
Over the years since MapReduce first became popular, the execution engines for dis‐
tributed batch processing have matured. By now, the infrastructure has become
robust enough to store and process many petabytes of data on clusters of over 10,000
machines. As the problem of physically operating batch processes at such scale has
been considered more or less solved, attention has turned to other areas: improving
the programming model, improving the efficiency of processing, and broadening the
set of problems that these technologies can solve.
426 
| 
Chapter 10: Batch Processing


As discussed previously, higher-level languages and APIs such as Hive, Pig, Cascad‐
ing, and Crunch became popular because programming MapReduce jobs by hand is
quite laborious. As Tez emerged, these high-level languages had the additional bene‐
fit of being able to move to the new dataflow execution engine without the need to
rewrite job code. Spark and Flink also include their own high-level dataflow APIs,
often taking inspiration from FlumeJava [34].
These dataflow APIs generally use relational-style building blocks to express a com‐
putation: joining datasets on the value of some field; grouping tuples by key; filtering
by some condition; and aggregating tuples by counting, summing, or other functions.
Internally, these operations are implemented using the various join and grouping
algorithms that we discussed earlier in this chapter.
Besides the obvious advantage of requiring less code, these high-level interfaces also
allow interactive use, in which you write analysis code incrementally in a shell and
run it frequently to observe what it is doing. This style of development is very helpful
when exploring a dataset and experimenting with approaches for processing it. It is
also reminiscent of the Unix philosophy, which we discussed in “The Unix Philoso‐
phy” on page 394.
Moreover, these high-level interfaces not only make the humans using the system
more productive, but they also improve the job execution efficiency at a machine
level.
The move toward declarative query languages
An advantage of specifying joins as relational operators, compared to spelling out the
code that performs the join, is that the framework can analyze the properties of the
join inputs and automatically decide which of the aforementioned join algorithms
would be most suitable for the task at hand. Hive, Spark, and Flink have cost-based
query optimizers that can do this, and even change the order of joins so that the
amount of intermediate state is minimized [66, 77, 78, 79].
The choice of join algorithm can make a big difference to the performance of a batch
job, and it is nice not to have to understand and remember all the various join algo‐
rithms we discussed in this chapter. This is possible if joins are specified in a declara‐
tive way: the application simply states which joins are required, and the query
optimizer decides how they can best be executed. We previously came across this idea
in “Query Languages for Data” on page 42.
However, in other ways, MapReduce and its dataflow successors are very different
from the fully declarative query model of SQL. MapReduce was built around the idea
of function callbacks: for each record or group of records, a user-defined function
(the mapper or reducer) is called, and that function is free to call arbitrary code in
order to decide what to output. This approach has the advantage that you can draw
Beyond MapReduce 
| 
427


upon a large ecosystem of existing libraries to do things like parsing, natural language
analysis, image analysis, and running numerical or statistical algorithms.
The freedom to easily run arbitrary code is what has long distinguished batch pro‐
cessing systems of MapReduce heritage from MPP databases (see “Comparing
Hadoop to Distributed Databases” on page 414); although databases have facilities
for writing user-defined functions, they are often cumbersome to use and not well
integrated with the package managers and dependency management systems that are
widely used in most programming languages (such as Maven for Java, npm for Java‐
Script, and Rubygems for Ruby).
However, dataflow engines have found that there are also advantages to incorporat‐
ing more declarative features in areas besides joins. For example, if a callback func‐
tion contains only a simple filtering condition, or it just selects some fields from a
record, then there is significant CPU overhead in calling the function on every
record. If such simple filtering and mapping operations are expressed in a declarative
way, the query optimizer can take advantage of column-oriented storage layouts (see
“Column-Oriented Storage” on page 95) and read only the required columns from
disk. Hive, Spark DataFrames, and Impala also use vectorized execution (see “Mem‐
ory bandwidth and vectorized processing” on page 99): iterating over data in a tight
inner loop that is friendly to CPU caches, and avoiding function calls. Spark gener‐
ates JVM bytecode [79] and Impala uses LLVM to generate native code for these
inner loops [41].
By incorporating declarative aspects in their high-level APIs, and having query opti‐
mizers that can take advantage of them during execution, batch processing frame‐
works begin to look more like MPP databases (and can achieve comparable
performance). At the same time, by having the extensibility of being able to run arbi‐
trary code and read data in arbitrary formats, they retain their flexibility advantage.
Specialization for different domains
While the extensibility of being able to run arbitrary code is useful, there are also
many common cases where standard processing patterns keep reoccurring, and so it
is worth having reusable implementations of the common building blocks. Tradition‐
ally, MPP databases have served the needs of business intelligence analysts and busi‐
ness reporting, but that is just one among many domains in which batch processing
is used.
Another domain of increasing importance is statistical and numerical algorithms,
which are needed for machine learning applications such as classification and recom‐
mendation systems. Reusable implementations are emerging: for example, Mahout
implements various algorithms for machine learning on top of MapReduce, Spark,
and Flink, while MADlib implements similar functionality inside a relational MPP
database (Apache HAWQ) [54].
428 
| 
Chapter 10: Batch Processing


Also useful are spatial algorithms such as k-nearest neighbors [80], which searches for
items that are close to a given item in some multi-dimensional space—a kind of simi‐
larity search. Approximate search is also important for genome analysis algorithms,
which need to find strings that are similar but not identical [81].
Batch processing engines are being used for distributed execution of algorithms from
an increasingly wide range of domains. As batch processing systems gain built-in
functionality and high-level declarative operators, and as MPP databases become
more programmable and flexible, the two are beginning to look more alike: in the
end, they are all just systems for storing and processing data. 
Summary
In this chapter we explored the topic of batch processing. We started by looking at
Unix tools such as awk, grep, and sort, and we saw how the design philosophy of
those tools is carried forward into MapReduce and more recent dataflow engines.
Some of those design principles are that inputs are immutable, outputs are intended
to become the input to another (as yet unknown) program, and complex problems
are solved by composing small tools that “do one thing well.”
In the Unix world, the uniform interface that allows one program to be composed
with another is files and pipes; in MapReduce, that interface is a distributed filesys‐
tem. We saw that dataflow engines add their own pipe-like data transport mecha‐
nisms to avoid materializing intermediate state to the distributed filesystem, but the
initial input and final output of a job is still usually HDFS.
The two main problems that distributed batch processing frameworks need to solve
are:
Partitioning
In MapReduce, mappers are partitioned according to input file blocks. The out‐
put of mappers is repartitioned, sorted, and merged into a configurable number
of reducer partitions. The purpose of this process is to bring all the related data—
e.g., all the records with the same key—together in the same place.
Post-MapReduce dataflow engines try to avoid sorting unless it is required, but
they otherwise take a broadly similar approach to partitioning.
Fault tolerance
MapReduce frequently writes to disk, which makes it easy to recover from an
individual failed task without restarting the entire job but slows down execution
in the failure-free case. Dataflow engines perform less materialization of inter‐
mediate state and keep more in memory, which means that they need to recom‐
pute more data if a node fails. Deterministic operators reduce the amount of data
that needs to be recomputed.
Summary 
| 
429


We discussed several join algorithms for MapReduce, most of which are also inter‐
nally used in MPP databases and dataflow engines. They also provide a good illustra‐
tion of how partitioned algorithms work:
Sort-merge joins
Each of the inputs being joined goes through a mapper that extracts the join key.
By partitioning, sorting, and merging, all the records with the same key end up
going to the same call of the reducer. This function can then output the joined
records.
Broadcast hash joins
One of the two join inputs is small, so it is not partitioned and it can be entirely
loaded into a hash table. Thus, you can start a mapper for each partition of the
large join input, load the hash table for the small input into each mapper, and
then scan over the large input one record at a time, querying the hash table for
each record.
Partitioned hash joins
If the two join inputs are partitioned in the same way (using the same key, same
hash function, and same number of partitions), then the hash table approach can
be used independently for each partition.
Distributed batch processing engines have a deliberately restricted programming
model: callback functions (such as mappers and reducers) are assumed to be stateless
and to have no externally visible side effects besides their designated output. This
restriction allows the framework to hide some of the hard distributed systems prob‐
lems behind its abstraction: in the face of crashes and network issues, tasks can be
retried safely, and the output from any failed tasks is discarded. If several tasks for a
partition succeed, only one of them actually makes its output visible.
Thanks to the framework, your code in a batch processing job does not need to worry
about implementing fault-tolerance mechanisms: the framework can guarantee that
the final output of a job is the same as if no faults had occurred, even though in real‐
ity various tasks perhaps had to be retried. These reliable semantics are much stron‐
ger than what you usually have in online services that handle user requests and that
write to databases as a side effect of processing a request.
The distinguishing feature of a batch processing job is that it reads some input data
and produces some output data, without modifying the input—in other words, the
output is derived from the input. Crucially, the input data is bounded: it has a known,
fixed size (for example, it consists of a set of log files at some point in time, or a snap‐
shot of a database’s contents). Because it is bounded, a job knows when it has finished
reading the entire input, and so a job eventually completes when it is done.
In the next chapter, we will turn to stream processing, in which the input is unboun‐
ded—that is, you still have a job, but its inputs are never-ending streams of data. In
430 
| 
Chapter 10: Batch Processing


this case, a job is never complete, because at any time there may still be more work
coming in. We shall see that stream and batch processing are similar in some
respects, but the assumption of unbounded streams also changes a lot about how we
build systems. 
References
[1] Jeffrey Dean and Sanjay Ghemawat: “MapReduce: Simplified Data Processing on
Large Clusters,” at 6th USENIX Symposium on Operating System Design and Imple‐
mentation (OSDI), December 2004.
[2] Joel Spolsky: “The Perils of JavaSchools,” joelonsoftware.com, December 25, 2005.
[3] Shivnath Babu and Herodotos Herodotou: “Massively Parallel Databases and
MapReduce Systems,” Foundations and Trends in Databases, volume 5, number 1,
pages 1–104, November 2013. doi:10.1561/1900000036
[4] David J. DeWitt and Michael Stonebraker: “MapReduce: A Major Step Back‐
wards,” originally published at databasecolumn.vertica.com, January 17, 2008.
[5] Henry Robinson: “The Elephant Was a Trojan Horse: On the Death of Map-
Reduce at Google,” the-paper-trail.org, June 25, 2014.
[6] “The Hollerith Machine,” United States Census Bureau, census.gov.
[7] “IBM 82, 83, and 84 Sorters Reference Manual,” Edition A24-1034-1, Interna‐
tional Business Machines Corporation, July 1962.
[8] Adam Drake: “Command-Line Tools Can Be 235x Faster than Your Hadoop
Cluster,” aadrake.com, January 25, 2014.
[9] “GNU Coreutils 8.23 Documentation,” Free Software Foundation, Inc., 2014.
[10] Martin Kleppmann: “Kafka, Samza, and the Unix Philosophy of Distributed
Data,” martin.kleppmann.com, August 5, 2015.
[11] Doug McIlroy: Internal Bell Labs memo, October 1964. Cited in: Dennis M.
Richie: “Advice from Doug McIlroy,” cm.bell-labs.com.
[12] M. D. McIlroy, E. N. Pinson, and B. A. Tague: “UNIX Time-Sharing System:
Foreword,” The Bell System Technical Journal, volume 57, number 6, pages 1899–
1904, July 1978.
[13] Eric S. Raymond: The Art of UNIX Programming. Addison-Wesley, 2003. ISBN:
978-0-13-142901-7
[14] Ronald Duncan: “Text File Formats – ASCII Delimited Text – Not CSV or TAB
Delimited Text,” ronaldduncan.wordpress.com, October 31, 2009.
[15] Alan Kay: “Is ‘Software Engineering’ an Oxymoron?,” tinlizzie.org.
Summary 
| 
431


[16] Martin Fowler: “InversionOfControl,” martinfowler.com, June 26, 2005.
[17] Daniel J. Bernstein: “Two File Descriptors for Sockets,” cr.yp.to.
[18] Rob Pike and Dennis M. Ritchie: “The Styx Architecture for Distributed Sys‐
tems,” Bell Labs Technical Journal, volume 4, number 2, pages 146–152, April 1999.
[19] Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung: “The Google File Sys‐
tem,” at 19th ACM Symposium on Operating Systems Principles (SOSP), October
2003. doi:10.1145/945445.945450
[20] Michael Ovsiannikov, Silvius Rus, Damian Reeves, et al.: “The Quantcast File
System,” Proceedings of the VLDB Endowment, volume 6, number 11, pages 1092–
1101, August 2013. doi:10.14778/2536222.2536234
[21] “OpenStack Swift 2.6.1 Developer Documentation,” OpenStack Foundation,
docs.openstack.org, March 2016.
[22] Zhe Zhang, Andrew Wang, Kai Zheng, et al.: “Introduction to HDFS Erasure
Coding in Apache Hadoop,” blog.cloudera.com, September 23, 2015.
[23] Peter Cnudde: “Hadoop Turns 10,” yahoohadoop.tumblr.com, February 5, 2016.
[24] Eric Baldeschwieler: “Thinking About the HDFS vs. Other Storage Technolo‐
gies,” hortonworks.com, July 25, 2012.
[25] Brendan Gregg: “Manta: Unix Meets Map Reduce,” dtrace.org, June 25, 2013.
[26] Tom White: Hadoop: The Definitive Guide, 4th edition. O’Reilly Media, 2015.
ISBN: 978-1-491-90163-2
[27] Jim N. Gray: “Distributed Computing Economics,” Microsoft Research Tech
Report MSR-TR-2003-24, March 2003.
[28] Márton Trencséni: “Luigi vs Airflow vs Pinball,” bytepawn.com, February 6,
2016.
[29] Roshan Sumbaly, Jay Kreps, and Sam Shah: “The ‘Big Data’ Ecosystem at
LinkedIn,” at ACM International Conference on Management of Data (SIGMOD),
July 2013. doi:10.1145/2463676.2463707
[30] Alan F. Gates, Olga Natkovich, Shubham Chopra, et al.: “Building a High-Level
Dataflow System on Top of Map-Reduce: The Pig Experience,” at 35th International
Conference on Very Large Data Bases (VLDB), August 2009.
[31] Ashish Thusoo, Joydeep Sen Sarma, Namit Jain, et al.: “Hive – A Petabyte Scale
Data Warehouse Using Hadoop,” at 26th IEEE International Conference on Data
Engineering (ICDE), March 2010. doi:10.1109/ICDE.2010.5447738
[32] “Cascading 3.0 User Guide,” Concurrent, Inc., docs.cascading.org, January 2016.
432 
| 
Chapter 10: Batch Processing


[33] “Apache Crunch User Guide,” Apache Software Foundation, crunch.apache.org.
[34] Craig Chambers, Ashish Raniwala, Frances Perry, et al.: “FlumeJava: Easy, Effi‐
cient Data-Parallel Pipelines,” at 31st ACM SIGPLAN Conference on Programming
Language 
Design 
and 
Implementation 
(PLDI), 
June 
2010. 
doi:
10.1145/1806596.1806638
[35] Jay Kreps: “Why Local State is a Fundamental Primitive in Stream Processing,”
oreilly.com, July 31, 2014.
[36] Martin Kleppmann: “Rethinking Caching in Web Apps,” martin.klepp‐
mann.com, October 1, 2012.
[37] Mark Grover, Ted Malaska, Jonathan Seidman, and Gwen Shapira: Hadoop
Application Architectures. O’Reilly Media, 2015. ISBN: 978-1-491-90004-8
[38] Philippe Ajoux, Nathan Bronson, Sanjeev Kumar, et al.: “Challenges to Adopting
Stronger Consistency at Scale,” at 15th USENIX Workshop on Hot Topics in Operat‐
ing Systems (HotOS), May 2015.
[39] Sriranjan Manjunath: “Skewed Join,” wiki.apache.org, 2009.
[40] David J. DeWitt, Jeffrey F. Naughton, Donovan A. Schneider, and S. Seshadri:
“Practical Skew Handling in Parallel Joins,” at 18th International Conference on Very
Large Data Bases (VLDB), August 1992.
[41] Marcel Kornacker, Alexander Behm, Victor Bittorf, et al.: “Impala: A Modern,
Open-Source SQL Engine for Hadoop,” at 7th Biennial Conference on Innovative
Data Systems Research (CIDR), January 2015.
[42] Matthieu Monsch: “Open-Sourcing PalDB, a Lightweight Companion for Stor‐
ing Side Data,” engineering.linkedin.com, October 26, 2015.
[43] Daniel Peng and Frank Dabek: “Large-Scale Incremental Processing Using Dis‐
tributed Transactions and Notifications,” at 9th USENIX conference on Operating Sys‐
tems Design and Implementation (OSDI), October 2010.
[44] ““Cloudera Search User Guide,” Cloudera, Inc., September 2015.
[45] Lili Wu, Sam Shah, Sean Choi, et al.: “The Browsemaps: Collaborative Filtering
at LinkedIn,” at 6th Workshop on Recommender Systems and the Social Web
(RSWeb), October 2014.
[46] Roshan Sumbaly, Jay Kreps, Lei Gao, et al.: “Serving Large-Scale Batch Compu‐
ted Data with Project Voldemort,” at 10th USENIX Conference on File and Storage
Technologies (FAST), February 2012.
[47] Varun Sharma: “Open-Sourcing Terrapin: A Serving System for Batch Gener‐
ated Data,” engineering.pinterest.com, September 14, 2015.
Summary 
| 
433


[48] Nathan Marz: “ElephantDB,” slideshare.net, May 30, 2011.
[49] Jean-Daniel (JD) Cryans: “How-to: Use HBase Bulk Loading, and Why,”
blog.cloudera.com, September 27, 2013.
[50] Nathan Marz: “How to Beat the CAP Theorem,” nathanmarz.com, October 13,
2011.
[51] Molly Bartlett Dishman and Martin Fowler: “Agile Architecture,” at O’Reilly
Software Architecture Conference, March 2015.
[52] David J. DeWitt and Jim N. Gray: “Parallel Database Systems: The Future of
High Performance Database Systems,” Communications of the ACM, volume 35,
number 6, pages 85–98, June 1992. doi:10.1145/129888.129894
[53] Jay Kreps: “But the multi-tenancy thing is actually really really hard,” tweet‐
storm, twitter.com, October 31, 2014.
[54] Jeffrey Cohen, Brian Dolan, Mark Dunlap, et al.: “MAD Skills: New Analysis
Practices for Big Data,” Proceedings of the VLDB Endowment, volume 2, number 2,
pages 1481–1492, August 2009. doi:10.14778/1687553.1687576
[55] Ignacio Terrizzano, Peter Schwarz, Mary Roth, and John E. Colino: “Data Wran‐
gling: The Challenging Journey from the Wild to the Lake,” at 7th Biennial Confer‐
ence on Innovative Data Systems Research (CIDR), January 2015.
[56] Paige Roberts: “To Schema on Read or to Schema on Write, That Is the Hadoop
Data Lake Question,” adaptivesystemsinc.com, July 2, 2015.
[57] Bobby Johnson and Joseph Adler: “The Sushi Principle: Raw Data Is Better,” at
Strata+Hadoop World, February 2015.
[58] Vinod Kumar Vavilapalli, Arun C. Murthy, Chris Douglas, et al.: “Apache
Hadoop YARN: Yet Another Resource Negotiator,” at 4th ACM Symposium on
Cloud Computing (SoCC), October 2013. doi:10.1145/2523616.2523633
[59] Abhishek Verma, Luis Pedrosa, Madhukar Korupolu, et al.: “Large-Scale Cluster
Management at Google with Borg,” at 10th European Conference on Computer Sys‐
tems (EuroSys), April 2015. doi:10.1145/2741948.2741964
[60] Malte Schwarzkopf: “The Evolution of Cluster Scheduler Architectures,” firma‐
ment.io, March 9, 2016.
[61] Matei Zaharia, Mosharaf Chowdhury, Tathagata Das, et al.: “Resilient Dis‐
tributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing,”
at 9th USENIX Symposium on Networked Systems Design and Implementation
(NSDI), April 2012.
[62] Holden Karau, Andy Konwinski, Patrick Wendell, and Matei Zaharia: Learning
Spark. O’Reilly Media, 2015. ISBN: 978-1-449-35904-1
434 
| 
Chapter 10: Batch Processing


[63] Bikas Saha and Hitesh Shah: “Apache Tez: Accelerating Hadoop Query Process‐
ing,” at Hadoop Summit, June 2014.
[64] Bikas Saha, Hitesh Shah, Siddharth Seth, et al.: “Apache Tez: A Unifying Frame‐
work for Modeling and Building Data Processing Applications,” at ACM Interna‐
tional Conference on Management of Data (SIGMOD), June 2015. doi:
10.1145/2723372.2742790
[65] Kostas Tzoumas: “Apache Flink: API, Runtime, and Project Roadmap,” slide‐
share.net, January 14, 2015.
[66] Alexander Alexandrov, Rico Bergmann, Stephan Ewen, et al.: “The Stratosphere
Platform for Big Data Analytics,” The VLDB Journal, volume 23, number 6, pages
939–964, May 2014. doi:10.1007/s00778-014-0357-y
[67] Michael Isard, Mihai Budiu, Yuan Yu, et al.: “Dryad: Distributed Data-Parallel
Programs from Sequential Building Blocks,” at European Conference on Computer
Systems (EuroSys), March 2007. doi:10.1145/1272996.1273005
[68] Daniel Warneke and Odej Kao: “Nephele: Efficient Parallel Data Processing in
the Cloud,” at 2nd Workshop on Many-Task Computing on Grids and Supercomputers
(MTAGS), November 2009. doi:10.1145/1646468.1646476
[69] Lawrence Page, Sergey Brin, Rajeev Motwani, and Terry Winograd: “The
PageRank Citation Ranking: Bringing Order to the Web,” Stanford InfoLab Techni‐
cal Report 422, 1999.
[70] Leslie G. Valiant: “A Bridging Model for Parallel Computation,” Communica‐
tions of the ACM, volume 33, number 8, pages 103–111, August 1990. doi:
10.1145/79173.79181
[71] Stephan Ewen, Kostas Tzoumas, Moritz Kaufmann, and Volker Markl: “Spin‐
ning Fast Iterative Data Flows,” Proceedings of the VLDB Endowment, volume 5,
number 11, pages 1268-1279, July 2012. doi:10.14778/2350229.2350245
[72] Grzegorz Malewicz, Matthew H. Austern, Aart J. C. Bik, et al.: “Pregel: A System
for Large-Scale Graph Processing,” at ACM International Conference on Management
of Data (SIGMOD), June 2010. doi:10.1145/1807167.1807184
[73] Frank McSherry, Michael Isard, and Derek G. Murray: “Scalability! But at What
COST?,” at 15th USENIX Workshop on Hot Topics in Operating Systems (HotOS),
May 2015.
[74] Ionel Gog, Malte Schwarzkopf, Natacha Crooks, et al.: “Musketeer: All for One,
One for All in Data Processing Systems,” at 10th European Conference on Computer
Systems (EuroSys), April 2015. doi:10.1145/2741948.2741968
Summary 
| 
435


[75] Aapo Kyrola, Guy Blelloch, and Carlos Guestrin: “GraphChi: Large-Scale Graph
Computation on Just a PC,” at 10th USENIX Symposium on Operating Systems
Design and Implementation (OSDI), October 2012.
[76] Andrew Lenharth, Donald Nguyen, and Keshav Pingali: “Parallel Graph Analyt‐
ics,” Communications of the ACM, volume 59, number 5, pages 78–87, May 2016. doi:
10.1145/2901919
[77] Fabian Hüske: “Peeking into Apache Flink’s Engine Room,” flink.apache.org,
March 13, 2015.
[78] Mostafa Mokhtar: “Hive 0.14 Cost Based Optimizer (CBO) Technical Over‐
view,” hortonworks.com, March 2, 2015.
[79] Michael Armbrust, Reynold S Xin, Cheng Lian, et al.: “Spark SQL: Relational
Data Processing in Spark,” at ACM International Conference on Management of Data
(SIGMOD), June 2015. doi:10.1145/2723372.2742797
[80] Daniel Blazevski: “Planting Quadtrees for Apache Flink,” insightdataengineer‐
ing.com, March 25, 2016.
[81] Tom White: “Genome Analysis Toolkit: Now Using Apache Spark for Data Pro‐
cessing,” blog.cloudera.com, April 6, 2016.
436 
| 
Chapter 10: Batch Processing






CHAPTER 11
Stream Processing
A complex system that works is invariably found to have evolved from a simple system that
works. The inverse proposition also appears to be true: A complex system designed from
scratch never works and cannot be made to work.
—John Gall, Systemantics (1975)
In Chapter 10 we discussed batch processing—techniques that read a set of files as
input and produce a new set of output files. The output is a form of derived data; that
is, a dataset that can be recreated by running the batch process again if necessary. We
saw how this simple but powerful idea can be used to create search indexes, recom‐
mendation systems, analytics, and more.
However, one big assumption remained throughout Chapter 10: namely, that the
input is bounded—i.e., of a known and finite size—so the batch process knows when
it has finished reading its input. For example, the sorting operation that is central to
MapReduce must read its entire input before it can start producing output: it could
happen that the very last input record is the one with the lowest key, and thus needs
to be the very first output record, so starting the output early is not an option.
In reality, a lot of data is unbounded because it arrives gradually over time: your users
produced data yesterday and today, and they will continue to produce more data
tomorrow. Unless you go out of business, this process never ends, and so the dataset
is never “complete” in any meaningful way [1]. Thus, batch processors must artifi‐
cially divide the data into chunks of fixed duration: for example, processing a day’s
worth of data at the end of every day, or processing an hour’s worth of data at the end
of every hour.
The problem with daily batch processes is that changes in the input are only reflected
in the output a day later, which is too slow for many impatient users. To reduce the
delay, we can run the processing more frequently—say, processing a second’s worth
of data at the end of every second—or even continuously, abandoning the fixed time
439


slices entirely and simply processing every event as it happens. That is the idea
behind stream processing.
In general, a “stream” refers to data that is incrementally made available over time.
The concept appears in many places: in the stdin and stdout of Unix, programming
languages (lazy lists) [2], filesystem APIs (such as Java’s FileInputStream), TCP con‐
nections, delivering audio and video over the internet, and so on.
In this chapter we will look at event streams as a data management mechanism: the
unbounded, incrementally processed counterpart to the batch data we saw in the
last chapter. We will first discuss how streams are represented, stored, and transmit‐
ted over a network. In “Databases and Streams” on page 451 we will investigate
the relationship between streams and databases. And finally, in “Processing Streams”
on page 464 we will explore approaches and tools for processing those streams
continually, and ways that they can be used to build applications.
Transmitting Event Streams
In the batch processing world, the inputs and outputs of a job are files (perhaps on a
distributed filesystem). What does the streaming equivalent look like?
When the input is a file (a sequence of bytes), the first processing step is usually to
parse it into a sequence of records. In a stream processing context, a record is more
commonly known as an event, but it is essentially the same thing: a small, selfcontained, immutable object containing the details of something that happened at
some point in time. An event usually contains a timestamp indicating when it hap‐
pened according to a time-of-day clock (see “Monotonic Versus Time-of-Day
Clocks” on page 288).
For example, the thing that happened might be an action that a user took, such as
viewing a page or making a purchase. It might also originate from a machine, such as
a periodic measurement from a temperature sensor, or a CPU utilization metric. In
the example of “Batch Processing with Unix Tools” on page 391, each line of the web
server log is an event.
An event may be encoded as a text string, or JSON, or perhaps in some binary form,
as discussed in Chapter 4. This encoding allows you to store an event, for example by
appending it to a file, inserting it into a relational table, or writing it to a document
database. It also allows you to send the event over the network to another node in
order to process it.
In batch processing, a file is written once and then potentially read by multiple jobs.
Analogously, in streaming terminology, an event is generated once by a producer
(also known as a publisher or sender), and then potentially processed by multiple con‐
sumers (subscribers or recipients) [3]. In a filesystem, a filename identifies a set of
440 
| 
Chapter 11: Stream Processing


related records; in a streaming system, related events are usually grouped together
into a topic or stream.
In principle, a file or database is sufficient to connect producers and consumers: a
producer writes every event that it generates to the datastore, and each consumer
periodically polls the datastore to check for events that have appeared since it last ran.
This is essentially what a batch process does when it processes a day’s worth of data at
the end of every day.
However, when moving toward continual processing with low delays, polling
becomes expensive if the datastore is not designed for this kind of usage. The more
often you poll, the lower the percentage of requests that return new events, and thus
the higher the overheads become. Instead, it is better for consumers to be notified
when new events appear.
Databases have traditionally not supported this kind of notification mechanism very
well: relational databases commonly have triggers, which can react to a change (e.g., a
row being inserted into a table), but they are very limited in what they can do and
have been somewhat of an afterthought in database design [4, 5]. Instead, specialized
tools have been developed for the purpose of delivering event notifications.
Messaging Systems
A common approach for notifying consumers about new events is to use a messaging
system: a producer sends a message containing the event, which is then pushed to
consumers. We touched on these systems previously in “Message-Passing Dataflow”
on page 136, but we will now go into more detail.
A direct communication channel like a Unix pipe or TCP connection between pro‐
ducer and consumer would be a simple way of implementing a messaging system.
However, most messaging systems expand on this basic model. In particular, Unix
pipes and TCP connect exactly one sender with one recipient, whereas a messaging
system allows multiple producer nodes to send messages to the same topic and allows
multiple consumer nodes to receive messages in a topic.
Within this publish/subscribe model, different systems take a wide range of
approaches, and there is no one right answer for all purposes. To differentiate the
systems, it is particularly helpful to ask the following two questions:
1. What happens if the producers send messages faster than the consumers can pro‐
cess them? Broadly speaking, there are three options: the system can drop mes‐
sages, buffer messages in a queue, or apply backpressure (also known as flow
control; i.e., blocking the producer from sending more messages). For example,
Unix pipes and TCP use backpressure: they have a small fixed-size buffer, and if
Transmitting Event Streams 
| 
441


it fills up, the sender is blocked until the recipient takes data out of the buffer (see
“Network congestion and queueing” on page 282).
If messages are buffered in a queue, it is important to understand what happens
as that queue grows. Does the system crash if the queue no longer fits in mem‐
ory, or does it write messages to disk? If so, how does the disk access affect the
performance of the messaging system [6]?
2. What happens if nodes crash or temporarily go offline—are any messages lost? As
with databases, durability may require some combination of writing to disk
and/or replication (see the sidebar “Replication and Durability” on page 227),
which has a cost. If you can afford to sometimes lose messages, you can probably
get higher throughput and lower latency on the same hardware.
Whether message loss is acceptable depends very much on the application. For exam‐
ple, with sensor readings and metrics that are transmitted periodically, an occasional
missing data point is perhaps not important, since an updated value will be sent a
short time later anyway. However, beware that if a large number of messages are
dropped, it may not be immediately apparent that the metrics are incorrect [7]. If you
are counting events, it is more important that they are delivered reliably, since every
lost message means incorrect counters.
A nice property of the batch processing systems we explored in Chapter 10 is that
they provide a strong reliability guarantee: failed tasks are automatically retried, and
partial output from failed tasks is automatically discarded. This means the output is
the same as if no failures had occurred, which helps simplify the programming
model. Later in this chapter we will examine how we can provide similar guarantees
in a streaming context.
Direct messaging from producers to consumers
A number of messaging systems use direct network communication between produc‐
ers and consumers without going via intermediary nodes:
• UDP multicast is widely used in the financial industry for streams such as stock
market feeds, where low latency is important [8]. Although UDP itself is unrelia‐
ble, application-level protocols can recover lost packets (the producer must
remember packets it has sent so that it can retransmit them on demand).
• Brokerless messaging libraries such as ZeroMQ [9] and nanomsg take a similar
approach, implementing publish/subscribe messaging over TCP or IP multicast.
• StatsD [10] and Brubeck [7] use unreliable UDP messaging for collecting metrics
from all machines on the network and monitoring them. (In the StatsD protocol,
counter metrics are only correct if all messages are received; using UDP makes
the metrics at best approximate [11]. See also “TCP Versus UDP” on page 283.)
442 
| 
Chapter 11: Stream Processing


• If the consumer exposes a service on the network, producers can make a direct
HTTP or RPC request (see “Dataflow Through Services: REST and RPC” on page
131) to push messages to the consumer. This is the idea behind webhooks [12], a
pattern in which a callback URL of one service is registered with another service,
and it makes a request to that URL whenever an event occurs.
Although these direct messaging systems work well in the situations for which they
are designed, they generally require the application code to be aware of the possibility
of message loss. The faults they can tolerate are quite limited: even if the protocols
detect and retransmit packets that are lost in the network, they generally assume that
producers and consumers are constantly online.
If a consumer is offline, it may miss messages that were sent while it is unreachable.
Some protocols allow the producer to retry failed message deliveries, but this
approach may break down if the producer crashes, losing the buffer of messages that
it was supposed to retry.
Message brokers
A widely used alternative is to send messages via a message broker (also known as a
message queue), which is essentially a kind of database that is optimized for handling
message streams [13]. It runs as a server, with producers and consumers connecting
to it as clients. Producers write messages to the broker, and consumers receive them
by reading them from the broker.
By centralizing the data in the broker, these systems can more easily tolerate clients
that come and go (connect, disconnect, and crash), and the question of durability is
moved to the broker instead. Some message brokers only keep messages in memory,
while others (depending on configuration) write them to disk so that they are not lost
in case of a broker crash. Faced with slow consumers, they generally allow unboun‐
ded queueing (as opposed to dropping messages or backpressure), although this
choice may also depend on the configuration.
A consequence of queueing is also that consumers are generally asynchronous: when
a producer sends a message, it normally only waits for the broker to confirm that it
has buffered the message and does not wait for the message to be processed by con‐
sumers. The delivery to consumers will happen at some undetermined future point in
time—often within a fraction of a second, but sometimes significantly later if there is
a queue backlog.
Message brokers compared to databases
Some message brokers can even participate in two-phase commit protocols using XA
or JTA (see “Distributed Transactions in Practice” on page 360). This feature makes
Transmitting Event Streams 
| 
443


them quite similar in nature to databases, although there are still important practical
differences between message brokers and databases:
• Databases usually keep data until it is explicitly deleted, whereas most message
brokers automatically delete a message when it has been successfully delivered to
its consumers. Such message brokers are not suitable for long-term data storage.
• Since they quickly delete messages, most message brokers assume that their
working set is fairly small—i.e., the queues are short. If the broker needs to buffer
a lot of messages because the consumers are slow (perhaps spilling messages to
disk if they no longer fit in memory), each individual message takes longer to
process, and the overall throughput may degrade [6].
• Databases often support secondary indexes and various ways of searching for
data, while message brokers often support some way of subscribing to a subset of
topics matching some pattern. The mechanisms are different, but both are essen‐
tially ways for a client to select the portion of the data that it wants to know
about.
• When querying a database, the result is typically based on a point-in-time snap‐
shot of the data; if another client subsequently writes something to the database
that changes the query result, the first client does not find out that its prior result
is now outdated (unless it repeats the query, or polls for changes). By contrast,
message brokers do not support arbitrary queries, but they do notify clients when
data changes (i.e., when new messages become available).
This is the traditional view of message brokers, which is encapsulated in standards
like JMS [14] and AMQP [15] and implemented in software like RabbitMQ,
ActiveMQ, HornetQ, Qpid, TIBCO Enterprise Message Service, IBM MQ, Azure Ser‐
vice Bus, and Google Cloud Pub/Sub [16].
Multiple consumers
When multiple consumers read messages in the same topic, two main patterns of
messaging are used, as illustrated in Figure 11-1:
Load balancing
Each message is delivered to one of the consumers, so the consumers can share
the work of processing the messages in the topic. The broker may assign mes‐
sages to consumers arbitrarily. This pattern is useful when the messages are
expensive to process, and so you want to be able to add consumers to parallelize
the processing. (In AMQP, you can implement load balancing by having multi‐
ple clients consuming from the same queue, and in JMS it is called a shared
subscription.)
444 
| 
Chapter 11: Stream Processing


Fan-out
Each message is delivered to all of the consumers. Fan-out allows several inde‐
pendent consumers to each “tune in” to the same broadcast of messages, without
affecting each other—the streaming equivalent of having several different batch
jobs that read the same input file. (This feature is provided by topic subscriptions
in JMS, and exchange bindings in AMQP.)
Figure 11-1. (a) Load balancing: sharing the work of consuming a topic among con‐
sumers; (b) fan-out: delivering each message to multiple consumers.
The two patterns can be combined: for example, two separate groups of consumers
may each subscribe to a topic, such that each group collectively receives all messages,
but within each group only one of the nodes receives each message.
Acknowledgments and redelivery
Consumers may crash at any time, so it could happen that a broker delivers a mes‐
sage to a consumer but the consumer never processes it, or only partially processes it
before crashing. In order to ensure that the message is not lost, message brokers use
acknowledgments: a client must explicitly tell the broker when it has finished process‐
ing a message so that the broker can remove it from the queue.
If the connection to a client is closed or times out without the broker receiving an
acknowledgment, it assumes that the message was not processed, and therefore it
delivers the message again to another consumer. (Note that it could happen that the
message actually was fully processed, but the acknowledgment was lost in the net‐
work. Handling this case requires an atomic commit protocol, as discussed in “Dis‐
tributed Transactions in Practice” on page 360.)
Transmitting Event Streams 
| 
445


When combined with load balancing, this redelivery behavior has an interesting
effect on the ordering of messages. In Figure 11-2, the consumers generally process
messages in the order they were sent by producers. However, consumer 2 crashes
while processing message m3, at the same time as consumer 1 is processing message
m4. The unacknowledged message m3 is subsequently redelivered to consumer 1,
with the result that consumer 1 processes messages in the order m4, m3, m5. Thus,
m3 and m4 are not delivered in the same order as they were sent by producer 1.
Figure 11-2. Consumer 2 crashes while processing m3, so it is redelivered to consumer 1
at a later time.
Even if the message broker otherwise tries to preserve the order of messages (as
required by both the JMS and AMQP standards), the combination of load balancing
with redelivery inevitably leads to messages being reordered. To avoid this issue, you
can use a separate queue per consumer (i.e., not use the load balancing feature). Mes‐
sage reordering is not a problem if messages are completely independent of each
other, but it can be important if there are causal dependencies between messages, as
we shall see later in the chapter. 
Partitioned Logs
Sending a packet over a network or making a request to a network service is normally
a transient operation that leaves no permanent trace. Although it is possible to record
it permanently (using packet capture and logging), we normally don’t think of it that
way. Even message brokers that durably write messages to disk quickly delete them
again after they have been delivered to consumers, because they are built around a
transient messaging mindset.
446 
| 
Chapter 11: Stream Processing


Databases and filesystems take the opposite approach: everything that is written to a
database or file is normally expected to be permanently recorded, at least until some‐
one explicitly chooses to delete it again.
This difference in mindset has a big impact on how derived data is created. A key
feature of batch processes, as discussed in Chapter 10, is that you can run them
repeatedly, experimenting with the processing steps, without risk of damaging the
input (since the input is read-only). This is not the case with AMQP/JMS-style mes‐
saging: receiving a message is destructive if the acknowledgment causes it to be
deleted from the broker, so you cannot run the same consumer again and expect to
get the same result.
If you add a new consumer to a messaging system, it typically only starts receiving
messages sent after the time it was registered; any prior messages are already gone
and cannot be recovered. Contrast this with files and databases, where you can add a
new client at any time, and it can read data written arbitrarily far in the past (as long
as it has not been explicitly overwritten or deleted by the application).
Why can we not have a hybrid, combining the durable storage approach of databases
with the low-latency notification facilities of messaging? This is the idea behind logbased message brokers.
Using logs for message storage
A log is simply an append-only sequence of records on disk. We previously discussed
logs in the context of log-structured storage engines and write-ahead logs in Chap‐
ter 3, and in the context of replication in Chapter 5.
The same structure can be used to implement a message broker: a producer sends a
message by appending it to the end of the log, and a consumer receives messages by
reading the log sequentially. If a consumer reaches the end of the log, it waits for a
notification that a new message has been appended. The Unix tool tail -f, which
watches a file for data being appended, essentially works like this.
In order to scale to higher throughput than a single disk can offer, the log can be
partitioned (in the sense of Chapter 6). Different partitions can then be hosted on dif‐
ferent machines, making each partition a separate log that can be read and written
independently from other partitions. A topic can then be defined as a group of parti‐
tions that all carry messages of the same type. This approach is illustrated in
Figure 11-3.
Within each partition, the broker assigns a monotonically increasing sequence num‐
ber, or offset, to every message (in Figure 11-3, the numbers in boxes are message off‐
sets). Such a sequence number makes sense because a partition is append-only, so the
messages within a partition are totally ordered. There is no ordering guarantee across
different partitions.
Transmitting Event Streams 
| 
447


Figure 11-3. Producers send messages by appending them to a topic-partition file, and
consumers read these files sequentially.
Apache Kafka [17, 18], Amazon Kinesis Streams [19], and Twitter’s DistributedLog
[20, 21] are log-based message brokers that work like this. Google Cloud Pub/Sub is
architecturally similar but exposes a JMS-style API rather than a log abstraction [16].
Even though these message brokers write all messages to disk, they are able to achieve
throughput of millions of messages per second by partitioning across multiple
machines, and fault tolerance by replicating messages [22, 23].
Logs compared to traditional messaging
The log-based approach trivially supports fan-out messaging, because several con‐
sumers can independently read the log without affecting each other—reading a mes‐
sage does not delete it from the log. To achieve load balancing across a group of
consumers, instead of assigning individual messages to consumer clients, the broker
can assign entire partitions to nodes in the consumer group.
Each client then consumes all the messages in the partitions it has been assigned.
Typically, when a consumer has been assigned a log partition, it reads the messages in
the partition sequentially, in a straightforward single-threaded manner. This coarsegrained load balancing approach has some downsides:
448 
| 
Chapter 11: Stream Processing


i. It’s possible to create a load balancing scheme in which two consumers share the work of processing a par‐
tition by having both read the full set of messages, but one of them only considers messages with evennumbered offsets while the other deals with the odd-numbered offsets. Alternatively, you could spread
message processing over a thread pool, but that approach complicates consumer offset management. In gen‐
eral, single-threaded processing of a partition is preferable, and parallelism can be increased by using more
partitions.
• The number of nodes sharing the work of consuming a topic can be at most the
number of log partitions in that topic, because messages within the same parti‐
tion are delivered to the same node.i
• If a single message is slow to process, it holds up the processing of subsequent
messages in that partition (a form of head-of-line blocking; see “Describing Per‐
formance” on page 13).
Thus, in situations where messages may be expensive to process and you want to par‐
allelize processing on a message-by-message basis, and where message ordering is not
so important, the JMS/AMQP style of message broker is preferable. On the other
hand, in situations with high message throughput, where each message is fast to pro‐
cess and where message ordering is important, the log-based approach works very
well.
Consumer offsets
Consuming a partition sequentially makes it easy to tell which messages have been
processed: all messages with an offset less than a consumer’s current offset have
already been processed, and all messages with a greater offset have not yet been seen.
Thus, the broker does not need to track acknowledgments for every single message—
it only needs to periodically record the consumer offsets. The reduced bookkeeping
overhead and the opportunities for batching and pipelining in this approach help
increase the throughput of log-based systems.
This offset is in fact very similar to the log sequence number that is commonly found
in single-leader database replication, and which we discussed in “Setting Up New
Followers” on page 155. In database replication, the log sequence number allows a
follower to reconnect to a leader after it has become disconnected, and resume repli‐
cation without skipping any writes. Exactly the same principle is used here: the mes‐
sage broker behaves like a leader database, and the consumer like a follower.
If a consumer node fails, another node in the consumer group is assigned the failed
consumer’s partitions, and it starts consuming messages at the last recorded offset. If
the consumer had processed subsequent messages but not yet recorded their offset,
those messages will be processed a second time upon restart. We will discuss ways of
dealing with this issue later in the chapter.
Transmitting Event Streams 
| 
449


Disk space usage
If you only ever append to the log, you will eventually run out of disk space. To
reclaim disk space, the log is actually divided into segments, and from time to time
old segments are deleted or moved to archive storage. (We’ll discuss a more sophisti‐
cated way of freeing disk space later.)
This means that if a slow consumer cannot keep up with the rate of messages, and it
falls so far behind that its consumer offset points to a deleted segment, it will miss
some of the messages. Effectively, the log implements a bounded-size buffer that dis‐
cards old messages when it gets full, also known as a circular buffer or ring buffer.
However, since that buffer is on disk, it can be quite large.
Let’s do a back-of-the-envelope calculation. At the time of writing, a typical large
hard drive has a capacity of 6 TB and a sequential write throughput of 150 MB/s. If
you are writing messages at the fastest possible rate, it takes about 11 hours to fill the
drive. Thus, the disk can buffer 11 hours’ worth of messages, after which it will start
overwriting old messages. This ratio remains the same, even if you use many hard
drives and machines. In practice, deployments rarely use the full write bandwidth of
the disk, so the log can typically keep a buffer of several days’ or even weeks’ worth of
messages.
Regardless of how long you retain messages, the throughput of a log remains more or
less constant, since every message is written to disk anyway [18]. This behavior is in
contrast to messaging systems that keep messages in memory by default and only
write them to disk if the queue grows too large: such systems are fast when queues are
short and become much slower when they start writing to disk, so the throughput
depends on the amount of history retained.
When consumers cannot keep up with producers
At the beginning of “Messaging Systems” on page 441 we discussed three choices of
what to do if a consumer cannot keep up with the rate at which producers are send‐
ing messages: dropping messages, buffering, or applying backpressure. In this taxon‐
omy, the log-based approach is a form of buffering with a large but fixed-size buffer
(limited by the available disk space).
If a consumer falls so far behind that the messages it requires are older than what is
retained on disk, it will not be able to read those messages—so the broker effectively
drops old messages that go back further than the size of the buffer can accommodate.
You can monitor how far a consumer is behind the head of the log, and raise an alert
if it falls behind significantly. As the buffer is large, there is enough time for a human
operator to fix the slow consumer and allow it to catch up before it starts missing
messages.
450 
| 
Chapter 11: Stream Processing


Even if a consumer does fall too far behind and starts missing messages, only that
consumer is affected; it does not disrupt the service for other consumers. This fact is
a big operational advantage: you can experimentally consume a production log for
development, testing, or debugging purposes, without having to worry much about
disrupting production services. When a consumer is shut down or crashes, it stops
consuming resources—the only thing that remains is its consumer offset.
This behavior also contrasts with traditional message brokers, where you need to be
careful to delete any queues whose consumers have been shut down—otherwise they
continue unnecessarily accumulating messages and taking away memory from con‐
sumers that are still active.
Replaying old messages
We noted previously that with AMQP- and JMS-style message brokers, processing
and acknowledging messages is a destructive operation, since it causes the messages
to be deleted on the broker. On the other hand, in a log-based message broker, con‐
suming messages is more like reading from a file: it is a read-only operation that does
not change the log.
The only side effect of processing, besides any output of the consumer, is that the
consumer offset moves forward. But the offset is under the consumer’s control, so it
can easily be manipulated if necessary: for example, you can start a copy of a con‐
sumer with yesterday’s offsets and write the output to a different location, in order to
reprocess the last day’s worth of messages. You can repeat this any number of times,
varying the processing code.
This aspect makes log-based messaging more like the batch processes of the last
chapter, where derived data is clearly separated from input data through a repeatable
transformation process. It allows more experimentation and easier recovery from
errors and bugs, making it a good tool for integrating dataflows within an organiza‐
tion [24]. 
Databases and Streams
We have drawn some comparisons between message brokers and databases. Even
though they have traditionally been considered separate categories of tools, we saw
that log-based message brokers have been successful in taking ideas from databases
and applying them to messaging. We can also go in reverse: take ideas from messag‐
ing and streams, and apply them to databases.
We said previously that an event is a record of something that happened at some
point in time. The thing that happened may be a user action (e.g., typing a search
query), or a sensor reading, but it may also be a write to a database. The fact that
something was written to a database is an event that can be captured, stored, and pro‐
Databases and Streams 
| 
451


cessed. This observation suggests that the connection between databases and streams
runs deeper than just the physical storage of logs on disk—it is quite fundamental.
In fact, a replication log (see “Implementation of Replication Logs” on page 158) is a
stream of database write events, produced by the leader as it processes transactions.
The followers apply that stream of writes to their own copy of the database and thus
end up with an accurate copy of the same data. The events in the replication log
describe the data changes that occurred.
We also came across the state machine replication principle in “Total Order Broad‐
cast” on page 348, which states: if every event represents a write to the database, and
every replica processes the same events in the same order, then the replicas will all
end up in the same final state. (Processing an event is assumed to be a deterministic
operation.) It’s just another case of event streams!
In this section we will first look at a problem that arises in heterogeneous data sys‐
tems, and then explore how we can solve it by bringing ideas from event streams to
databases.
Keeping Systems in Sync
As we have seen throughout this book, there is no single system that can satisfy all
data storage, querying, and processing needs. In practice, most nontrivial applica‐
tions need to combine several different technologies in order to satisfy their require‐
ments: for example, using an OLTP database to serve user requests, a cache to speed
up common requests, a full-text index to handle search queries, and a data warehouse
for analytics. Each of these has its own copy of the data, stored in its own representa‐
tion that is optimized for its own purposes.
As the same or related data appears in several different places, they need to be kept in
sync with one another: if an item is updated in the database, it also needs to be upda‐
ted in the cache, search indexes, and data warehouse. With data warehouses this syn‐
chronization is usually performed by ETL processes (see “Data Warehousing” on
page 91), often by taking a full copy of a database, transforming it, and bulk-loading
it into the data warehouse—in other words, a batch process. Similarly, we saw in
“The Output of Batch Workflows” on page 411 how search indexes, recommendation
systems, and other derived data systems might be created using batch processes.
If periodic full database dumps are too slow, an alternative that is sometimes used is
dual writes, in which the application code explicitly writes to each of the systems
when data changes: for example, first writing to the database, then updating the
search index, then invalidating the cache entries (or even performing those writes
concurrently).
However, dual writes have some serious problems, one of which is a race condition
illustrated in Figure 11-4. In this example, two clients concurrently want to update an
452 
| 
Chapter 11: Stream Processing


item X: client 1 wants to set the value to A, and client 2 wants to set it to B. Both
clients first write the new value to the database, then write it to the search index. Due
to unlucky timing, the requests are interleaved: the database first sees the write from
client 1 setting the value to A, then the write from client 2 setting the value to B, so
the final value in the database is B. The search index first sees the write from client 2,
then client 1, so the final value in the search index is A. The two systems are now
permanently inconsistent with each other, even though no error occurred.
Figure 11-4. In the database, X is first set to A and then to B, while at the search index
the writes arrive in the opposite order.
Unless you have some additional concurrency detection mechanism, such as the ver‐
sion vectors we discussed in “Detecting Concurrent Writes” on page 184, you will not
even notice that concurrent writes occurred—one value will simply silently overwrite
another value.
Another problem with dual writes is that one of the writes may fail while the other
succeeds. This is a fault-tolerance problem rather than a concurrency problem, but it
also has the effect of the two systems becoming inconsistent with each other. Ensur‐
ing that they either both succeed or both fail is a case of the atomic commit problem,
which is expensive to solve (see “Atomic Commit and Two-Phase Commit (2PC)” on
page 354).
If you only have one replicated database with a single leader, then that leader deter‐
mines the order of writes, so the state machine replication approach works among
replicas of the database. However, in Figure 11-4 there isn’t a single leader: the data‐
base may have a leader and the search index may have a leader, but neither follows
the other, and so conflicts can occur (see “Multi-Leader Replication” on page 168).
The situation would be better if there really was only one leader—for example, the
database—and if we could make the search index a follower of the database. But is
this possible in practice? 
Databases and Streams 
| 
453


Change Data Capture
The problem with most databases’ replication logs is that they have long been consid‐
ered to be an internal implementation detail of the database, not a public API. Clients
are supposed to query the database through its data model and query language, not
parse the replication logs and try to extract data from them.
For decades, many databases simply did not have a documented way of getting the
log of changes written to them. For this reason it was difficult to take all the changes
made in a database and replicate them to a different storage technology such as a
search index, cache, or data warehouse.
More recently, there has been growing interest in change data capture (CDC), which
is the process of observing all data changes written to a database and extracting them
in a form in which they can be replicated to other systems. CDC is especially interest‐
ing if changes are made available as a stream, immediately as they are written.
For example, you can capture the changes in a database and continually apply the
same changes to a search index. If the log of changes is applied in the same order, you
can expect the data in the search index to match the data in the database. The search
index and any other derived data systems are just consumers of the change stream, as
illustrated in Figure 11-5.
Figure 11-5. Taking data in the order it was written to one database, and applying the
changes to other systems in the same order.
Implementing change data capture
We can call the log consumers derived data systems, as discussed in the introduction
to Part III: the data stored in the search index and the data warehouse is just another
view onto the data in the system of record. Change data capture is a mechanism for
ensuring that all changes made to the system of record are also reflected in the
derived data systems so that the derived systems have an accurate copy of the data.
454 
| 
Chapter 11: Stream Processing


Essentially, change data capture makes one database the leader (the one from which
the changes are captured), and turns the others into followers. A log-based message
broker is well suited for transporting the change events from the source database,
since it preserves the ordering of messages (avoiding the reordering issue of
Figure 11-2).
Database triggers can be used to implement change data capture (see “Trigger-based
replication” on page 161) by registering triggers that observe all changes to data
tables and add corresponding entries to a changelog table. However, they tend to be
fragile and have significant performance overheads. Parsing the replication log can be
a more robust approach, although it also comes with challenges, such as handling
schema changes.
LinkedIn’s Databus [25], Facebook’s Wormhole [26], and Yahoo!’s Sherpa [27] use
this idea at large scale. Bottled Water implements CDC for PostgreSQL using an API
that decodes the write-ahead log [28], Maxwell and Debezium do something similar
for MySQL by parsing the binlog [29, 30, 31], Mongoriver reads the MongoDB oplog
[32, 33], and GoldenGate provides similar facilities for Oracle [34, 35].
Like message brokers, change data capture is usually asynchronous: the system of
record database does not wait for the change to be applied to consumers before com‐
mitting it. This design has the operational advantage that adding a slow consumer
does not affect the system of record too much, but it has the downside that all the
issues of replication lag apply (see “Problems with Replication Lag” on page 161).
Initial snapshot
If you have the log of all changes that were ever made to a database, you can recon‐
struct the entire state of the database by replaying the log. However, in many cases,
keeping all changes forever would require too much disk space, and replaying it
would take too long, so the log needs to be truncated.
Building a new full-text index, for example, requires a full copy of the entire database
—it is not sufficient to only apply a log of recent changes, since it would be missing
items that were not recently updated. Thus, if you don’t have the entire log history,
you need to start with a consistent snapshot, as previously discussed in “Setting Up
New Followers” on page 155.
The snapshot of the database must correspond to a known position or offset in the
change log, so that you know at which point to start applying changes after the snap‐
shot has been processed. Some CDC tools integrate this snapshot facility, while oth‐
ers leave it as a manual operation.
Databases and Streams 
| 
455


Log compaction
If you can only keep a limited amount of log history, you need to go through the
snapshot process every time you want to add a new derived data system. However,
log compaction provides a good alternative.
We discussed log compaction previously in “Hash Indexes” on page 72, in the con‐
text of log-structured storage engines (see Figure 3-2 for an example). The principle
is simple: the storage engine periodically looks for log records with the same key,
throws away any duplicates, and keeps only the most recent update for each key. This
compaction and merging process runs in the background.
In a log-structured storage engine, an update with a special null value (a tombstone)
indicates that a key was deleted, and causes it to be removed during log compaction.
But as long as a key is not overwritten or deleted, it stays in the log forever. The disk
space required for such a compacted log depends only on the current contents of the
database, not the number of writes that have ever occurred in the database. If the
same key is frequently overwritten, previous values will eventually be garbagecollected, and only the latest value will be retained.
The same idea works in the context of log-based message brokers and change data
capture. If the CDC system is set up such that every change has a primary key, and
every update for a key replaces the previous value for that key, then it’s sufficient to
keep just the most recent write for a particular key.
Now, whenever you want to rebuild a derived data system such as a search index, you
can start a new consumer from offset 0 of the log-compacted topic, and sequentially
scan over all messages in the log. The log is guaranteed to contain the most recent
value for every key in the database (and maybe some older values)—in other words,
you can use it to obtain a full copy of the database contents without having to take
another snapshot of the CDC source database.
This log compaction feature is supported by Apache Kafka. As we shall see later in
this chapter, it allows the message broker to be used for durable storage, not just for
transient messaging.
API support for change streams
Increasingly, databases are beginning to support change streams as a first-class inter‐
face, rather than the typical retrofitted and reverse-engineered CDC efforts. For
example, RethinkDB allows queries to subscribe to notifications when the results of a
query change [36], Firebase [37] and CouchDB [38] provide data synchronization
based on a change feed that is also made available to applications, and Meteor uses
the MongoDB oplog to subscribe to data changes and update the user interface [39].
VoltDB allows transactions to continuously export data from a database in the form
of a stream [40]. The database represents an output stream in the relational data
456 
| 
Chapter 11: Stream Processing


model as a table into which transactions can insert tuples, but which cannot be quer‐
ied. The stream then consists of the log of tuples that committed transactions have
written to this special table, in the order they were committed. External consumers
can asynchronously consume this log and use it to update derived data systems.
Kafka Connect [41] is an effort to integrate change data capture tools for a wide
range of database systems with Kafka. Once the stream of change events is in Kafka, it
can be used to update derived data systems such as search indexes, and also feed into
stream processing systems as discussed later in this chapter. 
Event Sourcing
There are some parallels between the ideas we’ve discussed here and event sourcing, a
technique that was developed in the domain-driven design (DDD) community [42,
43, 44]. We will discuss event sourcing briefly, because it incorporates some useful
and relevant ideas for streaming systems.
Similarly to change data capture, event sourcing involves storing all changes to the
application state as a log of change events. The biggest difference is that event sourc‐
ing applies the idea at a different level of abstraction:
• In change data capture, the application uses the database in a mutable way,
updating and deleting records at will. The log of changes is extracted from the
database at a low level (e.g., by parsing the replication log), which ensures that
the order of writes extracted from the database matches the order in which they
were actually written, avoiding the race condition in Figure 11-4. The application
writing to the database does not need to be aware that CDC is occurring.
• In event sourcing, the application logic is explicitly built on the basis of immuta‐
ble events that are written to an event log. In this case, the event store is appendonly, and updates or deletes are discouraged or prohibited. Events are designed
to reflect things that happened at the application level, rather than low-level state
changes.
Event sourcing is a powerful technique for data modeling: from an application point
of view it is more meaningful to record the user’s actions as immutable events, rather
than recording the effect of those actions on a mutable database. Event sourcing
makes it easier to evolve applications over time, helps with debugging by making it
easier to understand after the fact why something happened, and guards against
application bugs (see “Advantages of immutable events” on page 460).
For example, storing the event “student cancelled their course enrollment” clearly
expresses the intent of a single action in a neutral fashion, whereas the side effects
“one entry was deleted from the enrollments table, and one cancellation reason was
added to the student feedback table” embed a lot of assumptions about the way the
Databases and Streams 
| 
457


data is later going to be used. If a new application feature is introduced—for example,
“the place is offered to the next person on the waiting list”—the event sourcing
approach allows that new side effect to easily be chained off the existing event.
Event sourcing is similar to the chronicle data model [45], and there are also similari‐
ties between an event log and the fact table that you find in a star schema (see “Stars
and Snowflakes: Schemas for Analytics” on page 93).
Specialized databases such as Event Store [46] have been developed to support appli‐
cations using event sourcing, but in general the approach is independent of any par‐
ticular tool. A conventional database or a log-based message broker can also be used
to build applications in this style.
Deriving current state from the event log
An event log by itself is not very useful, because users generally expect to see the cur‐
rent state of a system, not the history of modifications. For example, on a shopping
website, users expect to be able to see the current contents of their cart, not an
append-only list of all the changes they have ever made to their cart.
Thus, applications that use event sourcing need to take the log of events (representing
the data written to the system) and transform it into application state that is suitable
for showing to a user (the way in which data is read from the system [47]). This
transformation can use arbitrary logic, but it should be deterministic so that you can
run it again and derive the same application state from the event log.
Like with change data capture, replaying the event log allows you to reconstruct the
current state of the system. However, log compaction needs to be handled differently:
• A CDC event for the update of a record typically contains the entire new version
of the record, so the current value for a primary key is entirely determined by the
most recent event for that primary key, and log compaction can discard previous
events for the same key.
• On the other hand, with event sourcing, events are modeled at a higher level: an
event typically expresses the intent of a user action, not the mechanics of the state
update that occurred as a result of the action. In this case, later events typically
do not override prior events, and so you need the full history of events to recon‐
struct the final state. Log compaction is not possible in the same way.
Applications that use event sourcing typically have some mechanism for storing
snapshots of the current state that is derived from the log of events, so they don’t
need to repeatedly reprocess the full log. However, this is only a performance optimi‐
zation to speed up reads and recovery from crashes; the intention is that the system is
able to store all raw events forever and reprocess the full event log whenever required.
We discuss this assumption in “Limitations of immutability” on page 463. 
458 
| 
Chapter 11: Stream Processing


Commands and events
The event sourcing philosophy is careful to distinguish between events and com‐
mands [48]. When a request from a user first arrives, it is initially a command: at this
point it may still fail, for example because some integrity condition is violated. The
application must first validate that it can execute the command. If the validation is
successful and the command is accepted, it becomes an event, which is durable and
immutable.
For example, if a user tries to register a particular username, or reserve a seat on an
airplane or in a theater, then the application needs to check that the username or seat
is not already taken. (We previously discussed this example in “Fault-Tolerant Con‐
sensus” on page 364.) When that check has succeeded, the application can generate
an event to indicate that a particular username was registered by a particular user ID,
or that a particular seat has been reserved for a particular customer.
At the point when the event is generated, it becomes a fact. Even if the customer later
decides to change or cancel the reservation, the fact remains true that they formerly
held a reservation for a particular seat, and the change or cancellation is a separate
event that is added later.
A consumer of the event stream is not allowed to reject an event: by the time the con‐
sumer sees the event, it is already an immutable part of the log, and it may have
already been seen by other consumers. Thus, any validation of a command needs to
happen synchronously, before it becomes an event—for example, by using a serializa‐
ble transaction that atomically validates the command and publishes the event.
Alternatively, the user request to reserve a seat could be split into two events: first a
tentative reservation, and then a separate confirmation event once the reservation has
been validated (as discussed in “Implementing linearizable storage using total order
broadcast” on page 350). This split allows the validation to take place in an asynchro‐
nous process. 
State, Streams, and Immutability
We saw in Chapter 10 that batch processing benefits from the immutability of its
input files, so you can run experimental processing jobs on existing input files
without fear of damaging them. This principle of immutability is also what makes
event sourcing and change data capture so powerful.
We normally think of databases as storing the current state of the application—this
representation is optimized for reads, and it is usually the most convenient for serv‐
ing queries. The nature of state is that it changes, so databases support updating and
deleting data as well as inserting it. How does this fit with immutability?
Databases and Streams 
| 
459


Whenever you have state that changes, that state is the result of the events that muta‐
ted it over time. For example, your list of currently available seats is the result of the
reservations you have processed, the current account balance is the result of the cred‐
its and debits on the account, and the response time graph for your web server is an
aggregation of the individual response times of all web requests that have occurred.
No matter how the state changes, there was always a sequence of events that caused
those changes. Even as things are done and undone, the fact remains true that those
events occurred. The key idea is that mutable state and an append-only log of immut‐
able events do not contradict each other: they are two sides of the same coin. The log
of all changes, the changelog, represents the evolution of state over time.
If you are mathematically inclined, you might say that the application state is what
you get when you integrate an event stream over time, and a change stream is what
you get when you differentiate the state by time, as shown in Figure 11-6 [49, 50, 51].
The analogy has limitations (for example, the second derivative of state does not
seem to be meaningful), but it’s a useful starting point for thinking about data.
Figure 11-6. The relationship between the current application state and an event
stream.
If you store the changelog durably, that simply has the effect of making the state
reproducible. If you consider the log of events to be your system of record, and any
mutable state as being derived from it, it becomes easier to reason about the flow of
data through a system. As Pat Helland puts it [52]:
Transaction logs record all the changes made to the database. High-speed appends are
the only way to change the log. From this perspective, the contents of the database
hold a caching of the latest record values in the logs. The truth is the log. The database
is a cache of a subset of the log. That cached subset happens to be the latest value of
each record and index value from the log.
Log compaction, as discussed in “Log compaction” on page 456, is one way of bridg‐
ing the distinction between log and database state: it retains only the latest version of
each record, and discards overwritten versions.
Advantages of immutable events
Immutability in databases is an old idea. For example, accountants have been using
immutability for centuries in financial bookkeeping. When a transaction occurs, it is
460 
| 
Chapter 11: Stream Processing


recorded in an append-only ledger, which is essentially a log of events describing
money, goods, or services that have changed hands. The accounts, such as profit and
loss or the balance sheet, are derived from the transactions in the ledger by adding
them up [53].
If a mistake is made, accountants don’t erase or change the incorrect transaction in
the ledger—instead, they add another transaction that compensates for the mistake,
for example refunding an incorrect charge. The incorrect transaction still remains in
the ledger forever, because it might be important for auditing reasons. If incorrect
figures, derived from the incorrect ledger, have already been published, then the fig‐
ures for the next accounting period include a correction. This process is entirely nor‐
mal in accounting [54].
Although such auditability is particularly important in financial systems, it is also
beneficial for many other systems that are not subject to such strict regulation. As
discussed in “Philosophy of batch process outputs” on page 413, if you accidentally
deploy buggy code that writes bad data to a database, recovery is much harder if the
code is able to destructively overwrite data. With an append-only log of immutable
events, it is much easier to diagnose what happened and recover from the problem.
Immutable events also capture more information than just the current state. For
example, on a shopping website, a customer may add an item to their cart and then
remove it again. Although the second event cancels out the first event from the point
of view of order fulfillment, it may be useful to know for analytics purposes that the
customer was considering a particular item but then decided against it. Perhaps they
will choose to buy it in the future, or perhaps they found a substitute. This informa‐
tion is recorded in an event log, but would be lost in a database that deletes items
when they are removed from the cart [42].
Deriving several views from the same event log
Moreover, by separating mutable state from the immutable event log, you can derive
several different read-oriented representations from the same log of events. This
works just like having multiple consumers of a stream (Figure 11-5): for example, the
analytic database Druid ingests directly from Kafka using this approach [55], Pista‐
chio is a distributed key-value store that uses Kafka as a commit log [56], and Kafka
Connect sinks can export data from Kafka to various different databases and indexes
[41]. It would make sense for many other storage and indexing systems, such as
search servers, to similarly take their input from a distributed log (see “Keeping Sys‐
tems in Sync” on page 452).
Having an explicit translation step from an event log to a database makes it easier to
evolve your application over time: if you want to introduce a new feature that
presents your existing data in some new way, you can use the event log to build a
separate read-optimized view for the new feature, and run it alongside the existing
Databases and Streams 
| 
461


systems without having to modify them. Running old and new systems side by side is
often easier than performing a complicated schema migration in an existing system.
Once the old system is no longer needed, you can simply shut it down and reclaim its
resources [47, 57].
Storing data is normally quite straightforward if you don’t have to worry about how it
is going to be queried and accessed; many of the complexities of schema design,
indexing, and storage engines are the result of wanting to support certain query and
access patterns (see Chapter 3). For this reason, you gain a lot of flexibility by sepa‐
rating the form in which data is written from the form it is read, and by allowing sev‐
eral different read views. This idea is sometimes known as command query
responsibility segregation (CQRS) [42, 58, 59].
The traditional approach to database and schema design is based on the fallacy that
data must be written in the same form as it will be queried. Debates about normaliza‐
tion and denormalization (see “Many-to-One and Many-to-Many Relationships” on
page 33) become largely irrelevant if you can translate data from a write-optimized
event log to read-optimized application state: it is entirely reasonable to denormalize
data in the read-optimized views, as the translation process gives you a mechanism
for keeping it consistent with the event log.
In “Describing Load” on page 11 we discussed Twitter’s home timelines, a cache of
recently written tweets by the people a particular user is following (like a mailbox).
This is another example of read-optimized state: home timelines are highly denor‐
malized, since your tweets are duplicated in all of the timelines of the people follow‐
ing you. However, the fan-out service keeps this duplicated state in sync with new
tweets and new following relationships, which keeps the duplication manageable.
Concurrency control
The biggest downside of event sourcing and change data capture is that the consum‐
ers of the event log are usually asynchronous, so there is a possibility that a user may
make a write to the log, then read from a log-derived view and find that their write
has not yet been reflected in the read view. We discussed this problem and potential
solutions previously in “Reading Your Own Writes” on page 162.
One solution would be to perform the updates of the read view synchronously with
appending the event to the log. This requires a transaction to combine the writes into
an atomic unit, so either you need to keep the event log and the read view in the same
storage system, or you need a distributed transaction across the different systems.
Alternatively, you could use the approach discussed in “Implementing linearizable
storage using total order broadcast” on page 350.
On the other hand, deriving the current state from an event log also simplifies some
aspects of concurrency control. Much of the need for multi-object transactions (see
“Single-Object and Multi-Object Operations” on page 228) stems from a single user
462 
| 
Chapter 11: Stream Processing


action requiring data to be changed in several different places. With event sourcing,
you can design an event such that it is a self-contained description of a user action.
The user action then requires only a single write in one place—namely appending the
events to the log—which is easy to make atomic.
If the event log and the application state are partitioned in the same way (for exam‐
ple, processing an event for a customer in partition 3 only requires updating partition
3 of the application state), then a straightforward single-threaded log consumer needs
no concurrency control for writes—by construction, it only processes a single event
at a time (see also “Actual Serial Execution” on page 252). The log removes the non‐
determinism of concurrency by defining a serial order of events in a partition [24]. If
an event touches multiple state partitions, a bit more work is required, which we will
discuss in Chapter 12. 
Limitations of immutability
Many systems that don’t use an event-sourced model nevertheless rely on immutabil‐
ity: various databases internally use immutable data structures or multi-version data
to support point-in-time snapshots (see “Indexes and snapshot isolation” on page
241). Version control systems such as Git, Mercurial, and Fossil also rely on immuta‐
ble data to preserve version history of files.
To what extent is it feasible to keep an immutable history of all changes forever? The
answer depends on the amount of churn in the dataset. Some workloads mostly add
data and rarely update or delete; they are easy to make immutable. Other workloads
have a high rate of updates and deletes on a comparatively small dataset; in these
cases, the immutable history may grow prohibitively large, fragmentation may
become an issue, and the performance of compaction and garbage collection
becomes crucial for operational robustness [60, 61].
Besides the performance reasons, there may also be circumstances in which you need
data to be deleted for administrative reasons, in spite of all immutability. For exam‐
ple, privacy regulations may require deleting a user’s personal information after they
close their account, data protection legislation may require erroneous information to
be removed, or an accidental leak of sensitive information may need to be contained.
In these circumstances, it’s not sufficient to just append another event to the log to
indicate that the prior data should be considered deleted—you actually want to
rewrite history and pretend that the data was never written in the first place. For
example, Datomic calls this feature excision [62], and the Fossil version control sys‐
tem has a similar concept called shunning [63].
Truly deleting data is surprisingly hard [64], since copies can live in many places: for
example, storage engines, filesystems, and SSDs often write to a new location rather
than overwriting in place [52], and backups are often deliberately immutable to pre‐
vent accidental deletion or corruption. Deletion is more a matter of “making it harder
Databases and Streams 
| 
463


to retrieve the data” than actually “making it impossible to retrieve the data.” Never‐
theless, you sometimes have to try, as we shall see in “Legislation and self-regulation”
on page 542. 
Processing Streams
So far in this chapter we have talked about where streams come from (user activity
events, sensors, and writes to databases), and we have talked about how streams are
transported (through direct messaging, via message brokers, and in event logs).
What remains is to discuss what you can do with the stream once you have it—
namely, you can process it. Broadly, there are three options:
1. You can take the data in the events and write it to a database, cache, search index,
or similar storage system, from where it can then be queried by other clients. As
shown in Figure 11-5, this is a good way of keeping a database in sync with
changes happening in other parts of the system—especially if the stream con‐
sumer is the only client writing to the database. Writing to a storage system is the
streaming equivalent of what we discussed in “The Output of Batch Workflows”
on page 411.
2. You can push the events to users in some way, for example by sending email
alerts or push notifications, or by streaming the events to a real-time dashboard
where they are visualized. In this case, a human is the ultimate consumer of the
stream.
3. You can process one or more input streams to produce one or more output
streams. Streams may go through a pipeline consisting of several such processing
stages before they eventually end up at an output (option 1 or 2).
In the rest of this chapter, we will discuss option 3: processing streams to produce
other, derived streams. A piece of code that processes streams like this is known as an
operator or a job. It is closely related to the Unix processes and MapReduce jobs we
discussed in Chapter 10, and the pattern of dataflow is similar: a stream processor
consumes input streams in a read-only fashion and writes its output to a different
location in an append-only fashion.
The patterns for partitioning and parallelization in stream processors are also very
similar to those in MapReduce and the dataflow engines we saw in Chapter 10, so we
won’t repeat those topics here. Basic mapping operations such as transforming and
filtering records also work the same.
The one crucial difference to batch jobs is that a stream never ends. This difference
has many implications: as discussed at the start of this chapter, sorting does not make
sense with an unbounded dataset, and so sort-merge joins (see “Reduce-Side Joins
and Grouping” on page 403) cannot be used. Fault-tolerance mechanisms must also
464 
| 
Chapter 11: Stream Processing


change: with a batch job that has been running for a few minutes, a failed task can
simply be restarted from the beginning, but with a stream job that has been running
for several years, restarting from the beginning after a crash may not be a viable
option.
Uses of Stream Processing
Stream processing has long been used for monitoring purposes, where an organiza‐
tion wants to be alerted if certain things happen. For example:
• Fraud detection systems need to determine if the usage patterns of a credit card
have unexpectedly changed, and block the card if it is likely to have been stolen.
• Trading systems need to examine price changes in a financial market and execute
trades according to specified rules.
• Manufacturing systems need to monitor the status of machines in a factory, and
quickly identify the problem if there is a malfunction.
• Military and intelligence systems need to track the activities of a potential aggres‐
sor, and raise the alarm if there are signs of an attack.
These kinds of applications require quite sophisticated pattern matching and correla‐
tions. However, other uses of stream processing have also emerged over time. In this
section we will briefly compare and contrast some of these applications.
Complex event processing
Complex event processing (CEP) is an approach developed in the 1990s for analyzing
event streams, especially geared toward the kind of application that requires search‐
ing for certain event patterns [65, 66]. Similarly to the way that a regular expression
allows you to search for certain patterns of characters in a string, CEP allows you to
specify rules to search for certain patterns of events in a stream.
CEP systems often use a high-level declarative query language like SQL, or a graphi‐
cal user interface, to describe the patterns of events that should be detected. These
queries are submitted to a processing engine that consumes the input streams and
internally maintains a state machine that performs the required matching. When a
match is found, the engine emits a complex event (hence the name) with the details of
the event pattern that was detected [67].
In these systems, the relationship between queries and data is reversed compared to
normal databases. Usually, a database stores data persistently and treats queries as
transient: when a query comes in, the database searches for data matching the query,
and then forgets about the query when it has finished. CEP engines reverse these
roles: queries are stored long-term, and events from the input streams continuously
flow past them in search of a query that matches an event pattern [68].
Processing Streams 
| 
465


Implementations of CEP include Esper [69], IBM InfoSphere Streams [70], Apama,
TIBCO StreamBase, and SQLstream. Distributed stream processors like Samza are
also gaining SQL support for declarative queries on streams [71].
Stream analytics
Another area in which stream processing is used is for analytics on streams. The
boundary between CEP and stream analytics is blurry, but as a general rule, analytics
tends to be less interested in finding specific event sequences and is more oriented
toward aggregations and statistical metrics over a large number of events—for exam‐
ple:
• Measuring the rate of some type of event (how often it occurs per time interval)
• Calculating the rolling average of a value over some time period
• Comparing current statistics to previous time intervals (e.g., to detect trends or
to alert on metrics that are unusually high or low compared to the same time last
week)
Such statistics are usually computed over fixed time intervals—for example, you
might want to know the average number of queries per second to a service over the
last 5 minutes, and their 99th percentile response time during that period. Averaging
over a few minutes smoothes out irrelevant fluctuations from one second to the next,
while still giving you a timely picture of any changes in traffic pattern. The time
interval over which you aggregate is known as a window, and we will look into win‐
dowing in more detail in “Reasoning About Time” on page 468.
Stream analytics systems sometimes use probabilistic algorithms, such as Bloom fil‐
ters (which we encountered in “Performance optimizations” on page 79) for set
membership, HyperLogLog [72] for cardinality estimation, and various percentile
estimation algorithms (see “Percentiles in Practice” on page 16). Probabilistic algo‐
rithms produce approximate results, but have the advantage of requiring significantly
less memory in the stream processor than exact algorithms. This use of approxima‐
tion algorithms sometimes leads people to believe that stream processing systems are
always lossy and inexact, but that is wrong: there is nothing inherently approximate
about stream processing, and probabilistic algorithms are merely an optimization
[73].
Many open source distributed stream processing frameworks are designed with ana‐
lytics in mind: for example, Apache Storm, Spark Streaming, Flink, Concord, Samza,
and Kafka Streams [74]. Hosted services include Google Cloud Dataflow and Azure
Stream Analytics.
466 
| 
Chapter 11: Stream Processing


Maintaining materialized views
We saw in “Databases and Streams” on page 451 that a stream of changes to a data‐
base can be used to keep derived data systems, such as caches, search indexes, and
data warehouses, up to date with a source database. We can regard these examples as
specific cases of maintaining materialized views (see “Aggregation: Data Cubes and
Materialized Views” on page 101): deriving an alternative view onto some dataset so
that you can query it efficiently, and updating that view whenever the underlying
data changes [50].
Similarly, in event sourcing, application state is maintained by applying a log of
events; here the application state is also a kind of materialized view. Unlike stream
analytics scenarios, it is usually not sufficient to consider only events within some
time window: building the materialized view potentially requires all events over an
arbitrary time period, apart from any obsolete events that may be discarded by log
compaction (see “Log compaction” on page 456). In effect, you need a window that
stretches all the way back to the beginning of time.
In principle, any stream processor could be used for materialized view maintenance,
although the need to maintain events forever runs counter to the assumptions of
some analytics-oriented frameworks that mostly operate on windows of a limited
duration. Samza and Kafka Streams support this kind of usage, building upon Kafka’s
support for log compaction [75].
Search on streams
Besides CEP, which allows searching for patterns consisting of multiple events, there
is also sometimes a need to search for individual events based on complex criteria,
such as full-text search queries.
For example, media monitoring services subscribe to feeds of news articles and
broadcasts from media outlets, and search for any news mentioning companies,
products, or topics of interest. This is done by formulating a search query in advance,
and then continually matching the stream of news items against this query. Similar
features exist on some websites: for example, users of real estate websites can ask to
be notified when a new property matching their search criteria appears on the mar‐
ket. The percolator feature of Elasticsearch [76] is one option for implementing this
kind of stream search.
Conventional search engines first index the documents and then run queries over the
index. By contrast, searching a stream turns the processing on its head: the queries
are stored, and the documents run past the queries, like in CEP. In the simplest case,
you can test every document against every query, although this can get slow if you
have a large number of queries. To optimize the process, it is possible to index the
queries as well as the documents, and thus narrow down the set of queries that may
match [77].
Processing Streams 
| 
467


Message passing and RPC
In “Message-Passing Dataflow” on page 136 we discussed message-passing systems as
an alternative to RPC—i.e., as a mechanism for services to communicate, as used for
example in the actor model. Although these systems are also based on messages and
events, we normally don’t think of them as stream processors:
• Actor frameworks are primarily a mechanism for managing concurrency and
distributed execution of communicating modules, whereas stream processing is
primarily a data management technique.
• Communication between actors is often ephemeral and one-to-one, whereas
event logs are durable and multi-subscriber.
• Actors can communicate in arbitrary ways (including cyclic request/response
patterns), but stream processors are usually set up in acyclic pipelines where
every stream is the output of one particular job, and derived from a well-defined
set of input streams.
That said, there is some crossover area between RPC-like systems and stream pro‐
cessing. For example, Apache Storm has a feature called distributed RPC, which
allows user queries to be farmed out to a set of nodes that also process event streams;
these queries are then interleaved with events from the input streams, and results can
be aggregated and sent back to the user [78]. (See also “Multi-partition data process‐
ing” on page 514.)
It is also possible to process streams using actor frameworks. However, many such
frameworks do not guarantee message delivery in the case of crashes, so the process‐
ing is not fault-tolerant unless you implement additional retry logic.
Reasoning About Time
Stream processors often need to deal with time, especially when used for analytics
purposes, which frequently use time windows such as “the average over the last five
minutes.” It might seem that the meaning of “the last five minutes” should be unam‐
biguous and clear, but unfortunately the notion is surprisingly tricky.
In a batch process, the processing tasks rapidly crunch through a large collection of
historical events. If some kind of breakdown by time needs to happen, the batch pro‐
cess needs to look at the timestamp embedded in each event. There is no point in
looking at the system clock of the machine running the batch process, because the
time at which the process is run has nothing to do with the time at which the events
actually occurred.
A batch process may read a year’s worth of historical events within a few minutes; in
most cases, the timeline of interest is the year of history, not the few minutes of pro‐
cessing. Moreover, using the timestamps in the events allows the processing to be
468 
| 
Chapter 11: Stream Processing


ii. Thank you to Kostas Kloudas from the Flink community for coming up with this analogy.
deterministic: running the same process again on the same input yields the same
result (see “Fault tolerance” on page 422).
On the other hand, many stream processing frameworks use the local system clock
on the processing machine (the processing time) to determine windowing [79]. This
approach has the advantage of being simple, and it is reasonable if the delay between
event creation and event processing is negligibly short. However, it breaks down if
there is any significant processing lag—i.e., if the processing may happen noticeably
later than the time at which the event actually occurred.
Event time versus processing time
There are many reasons why processing may be delayed: queueing, network faults
(see “Unreliable Networks” on page 277), a performance issue leading to contention
in the message broker or processor, a restart of the stream consumer, or reprocessing
of past events (see “Replaying old messages” on page 451) while recovering from a
fault or after fixing a bug in the code.
Moreover, message delays can also lead to unpredictable ordering of messages. For
example, say a user first makes one web request (which is handled by web server A),
and then a second request (which is handled by server B). A and B emit events
describing the requests they handled, but B’s event reaches the message broker before
A’s event does. Now stream processors will first see the B event and then the A event,
even though they actually occurred in the opposite order.
If it helps to have an analogy, consider the Star Wars movies: Episode IV was released
in 1977, Episode V in 1980, and Episode VI in 1983, followed by Episodes I, II, and
III in 1999, 2002, and 2005, respectively, and Episode VII in 2015 [80].ii If you
watched the movies in the order they came out, the order in which you processed the
movies is inconsistent with the order of their narrative. (The episode number is like
the event timestamp, and the date when you watched the movie is the processing
time.) As humans, we are able to cope with such discontinuities, but stream process‐
ing algorithms need to be specifically written to accommodate such timing and
ordering issues.
Confusing event time and processing time leads to bad data. For example, say you
have a stream processor that measures the rate of requests (counting the number of
requests per second). If you redeploy the stream processor, it may be shut down for a
minute and process the backlog of events when it comes back up. If you measure the
rate based on the processing time, it will look as if there was a sudden anomalous
spike of requests while processing the backlog, when in fact the real rate of requests
was steady (Figure 11-7).
Processing Streams 
| 
469


Figure 11-7. Windowing by processing time introduces artifacts due to variations in
processing rate.
Knowing when you’re ready
A tricky problem when defining windows in terms of event time is that you can never
be sure when you have received all of the events for a particular window, or whether
there are some events still to come.
For example, say you’re grouping events into one-minute windows so that you can
count the number of requests per minute. You have counted some number of events
with timestamps that fall in the 37th minute of the hour, and time has moved on;
now most of the incoming events fall within the 38th and 39th minutes of the hour.
When do you declare that you have finished the window for the 37th minute, and
output its counter value?
You can time out and declare a window ready after you have not seen any new events
for a while, but it could still happen that some events were buffered on another
machine somewhere, delayed due to a network interruption. You need to be able to
handle such straggler events that arrive after the window has already been declared
complete. Broadly, you have two options [1]:
1. Ignore the straggler events, as they are probably a small percentage of events in
normal circumstances. You can track the number of dropped events as a metric,
and alert if you start dropping a significant amount of data.
2. Publish a correction, an updated value for the window with stragglers included.
You may also need to retract the previous output.
470 
| 
Chapter 11: Stream Processing


In some cases it is possible to use a special message to indicate, “From now on there
will be no more messages with a timestamp earlier than t,” which can be used by con‐
sumers to trigger windows [81]. However, if several producers on different machines
are generating events, each with their own minimum timestamp thresholds, the con‐
sumers need to keep track of each producer individually. Adding and removing pro‐
ducers is trickier in this case.
Whose clock are you using, anyway?
Assigning timestamps to events is even more difficult when events can be buffered at
several points in the system. For example, consider a mobile app that reports events
for usage metrics to a server. The app may be used while the device is offline, in
which case it will buffer events locally on the device and send them to a server when
an internet connection is next available (which may be hours or even days later). To
any consumers of this stream, the events will appear as extremely delayed stragglers.
In this context, the timestamp on the events should really be the time at which the
user interaction occurred, according to the mobile device’s local clock. However, the
clock on a user-controlled device often cannot be trusted, as it may be accidentally or
deliberately set to the wrong time (see “Clock Synchronization and Accuracy” on
page 289). The time at which the event was received by the server (according to the
server’s clock) is more likely to be accurate, since the server is under your control, but
less meaningful in terms of describing the user interaction.
To adjust for incorrect device clocks, one approach is to log three timestamps [82]:
• The time at which the event occurred, according to the device clock
• The time at which the event was sent to the server, according to the device clock
• The time at which the event was received by the server, according to the server
clock
By subtracting the second timestamp from the third, you can estimate the offset
between the device clock and the server clock (assuming the network delay is negligi‐
ble compared to the required timestamp accuracy). You can then apply that offset to
the event timestamp, and thus estimate the true time at which the event actually
occurred (assuming the device clock offset did not change between the time the event
occurred and the time it was sent to the server).
This problem is not unique to stream processing—batch processing suffers from
exactly the same issues of reasoning about time. It is just more noticeable in a stream‐
ing context, where we are more aware of the passage of time.
Processing Streams 
| 
471


Types of windows
Once you know how the timestamp of an event should be determined, the next step
is to decide how windows over time periods should be defined. The window can then
be used for aggregations, for example to count events, or to calculate the average of
values within the window. Several types of windows are in common use [79, 83]:
Tumbling window
A tumbling window has a fixed length, and every event belongs to exactly one
window. For example, if you have a 1-minute tumbling window, all the events
with timestamps between 10:03:00 and 10:03:59 are grouped into one window,
events between 10:04:00 and 10:04:59 into the next window, and so on. You
could implement a 1-minute tumbling window by taking each event timestamp
and rounding it down to the nearest minute to determine the window that it
belongs to.
Hopping window
A hopping window also has a fixed length, but allows windows to overlap in
order to provide some smoothing. For example, a 5-minute window with a hop
size of 1 minute would contain the events between 10:03:00 and 10:07:59, then
the next window would cover events between 10:04:00 and 10:08:59, and so on.
You can implement this hopping window by first calculating 1-minute tumbling
windows, and then aggregating over several adjacent windows.
Sliding window
A sliding window contains all the events that occur within some interval of each
other. For example, a 5-minute sliding window would cover events at 10:03:39
and 10:08:12, because they are less than 5 minutes apart (note that tumbling and
hopping 5-minute windows would not have put these two events in the same
window, as they use fixed boundaries). A sliding window can be implemented by
keeping a buffer of events sorted by time and removing old events when they
expire from the window.
Session window
Unlike the other window types, a session window has no fixed duration. Instead,
it is defined by grouping together all events for the same user that occur closely
together in time, and the window ends when the user has been inactive for some
time (for example, if there have been no events for 30 minutes). Sessionization is
a common requirement for website analytics (see “GROUP BY” on page 406). 
Stream Joins
In Chapter 10 we discussed how batch jobs can join datasets by key, and how such
joins form an important part of data pipelines. Since stream processing generalizes
472 
| 
Chapter 11: Stream Processing


data pipelines to incremental processing of unbounded datasets, there is exactly the
same need for joins on streams.
However, the fact that new events can appear anytime on a stream makes joins on
streams more challenging than in batch jobs. To understand the situation better, let’s
distinguish three different types of joins: stream-stream joins, stream-table joins, and
table-table joins [84]. In the following sections we’ll illustrate each by example.
Stream-stream join (window join)
Say you have a search feature on your website, and you want to detect recent trends
in searched-for URLs. Every time someone types a search query, you log an event
containing the query and the results returned. Every time someone clicks one of the
search results, you log another event recording the click. In order to calculate the
click-through rate for each URL in the search results, you need to bring together the
events for the search action and the click action, which are connected by having the
same session ID. Similar analyses are needed in advertising systems [85].
The click may never come if the user abandons their search, and even if it comes, the
time between the search and the click may be highly variable: in many cases it might
be a few seconds, but it could be as long as days or weeks (if a user runs a search,
forgets about that browser tab, and then returns to the tab and clicks a result some‐
time later). Due to variable network delays, the click event may even arrive before the
search event. You can choose a suitable window for the join—for example, you may
choose to join a click with a search if they occur at most one hour apart.
Note that embedding the details of the search in the click event is not equivalent to
joining the events: doing so would only tell you about the cases where the user
clicked a search result, not about the searches where the user did not click any of the
results. In order to measure search quality, you need accurate click-through rates, for
which you need both the search events and the click events.
To implement this type of join, a stream processor needs to maintain state: for exam‐
ple, all the events that occurred in the last hour, indexed by session ID. Whenever a
search event or click event occurs, it is added to the appropriate index, and the
stream processor also checks the other index to see if another event for the same ses‐
sion ID has already arrived. If there is a matching event, you emit an event saying
which search result was clicked. If the search event expires without you seeing a
matching click event, you emit an event saying which search results were not clicked.
Stream-table join (stream enrichment)
In “Example: analysis of user activity events” on page 404 (Figure 10-2) we saw an
example of a batch job joining two datasets: a set of user activity events and a data‐
base of user profiles. It is natural to think of the user activity events as a stream, and
to perform the same join on a continuous basis in a stream processor: the input is a
Processing Streams 
| 
473


stream of activity events containing a user ID, and the output is a stream of activity
events in which the user ID has been augmented with profile information about the
user. This process is sometimes known as enriching the activity events with informa‐
tion from the database.
To perform this join, the stream process needs to look at one activity event at a time,
look up the event’s user ID in the database, and add the profile information to the
activity event. The database lookup could be implemented by querying a remote
database; however, as discussed in “Example: analysis of user activity events” on page
404, such remote queries are likely to be slow and risk overloading the database [75].
Another approach is to load a copy of the database into the stream processor so that
it can be queried locally without a network round-trip. This technique is very similar
to the hash joins we discussed in “Map-Side Joins” on page 408: the local copy of the
database might be an in-memory hash table if it is small enough, or an index on the
local disk.
The difference to batch jobs is that a batch job uses a point-in-time snapshot of the
database as input, whereas a stream processor is long-running, and the contents of
the database are likely to change over time, so the stream processor’s local copy of the
database needs to be kept up to date. This issue can be solved by change data capture:
the stream processor can subscribe to a changelog of the user profile database as well
as the stream of activity events. When a profile is created or modified, the stream
processor updates its local copy. Thus, we obtain a join between two streams: the
activity events and the profile updates.
A stream-table join is actually very similar to a stream-stream join; the biggest differ‐
ence is that for the table changelog stream, the join uses a window that reaches back
to the “beginning of time” (a conceptually infinite window), with newer versions of
records overwriting older ones. For the stream input, the join might not maintain a
window at all.
Table-table join (materialized view maintenance)
Consider the Twitter timeline example that we discussed in “Describing Load” on
page 11. We said that when a user wants to view their home timeline, it is too expen‐
sive to iterate over all the people the user is following, find their recent tweets, and
merge them.
Instead, we want a timeline cache: a kind of per-user “inbox” to which tweets are
written as they are sent, so that reading the timeline is a single lookup. Materializing
and maintaining this cache requires the following event processing:
• When user u sends a new tweet, it is added to the timeline of every user who is
following u.
474 
| 
Chapter 11: Stream Processing


iii. If you regard a stream as the derivative of a table, as in Figure 11-6, and regard a join as a product of two
tables u·v, something interesting happens: the stream of changes to the materialized join follows the product
rule (u·v)′ = u′v + uv′. In words: any change of tweets is joined with the current followers, and any change of
followers is joined with the current tweets [49, 50].
• When a user deletes a tweet, it is removed from all users’ timelines.
• When user u1 starts following user u2, recent tweets by u2 are added to u1’s
timeline.
• When user u1 unfollows user u2, tweets by u2 are removed from u1’s timeline.
To implement this cache maintenance in a stream processor, you need streams of
events for tweets (sending and deleting) and for follow relationships (following and
unfollowing). The stream process needs to maintain a database containing the set of
followers for each user so that it knows which timelines need to be updated when a
new tweet arrives [86].
Another way of looking at this stream process is that it maintains a materialized view
for a query that joins two tables (tweets and follows), something like the following:
SELECT follows.follower_id AS timeline_id,
  array_agg(tweets.* ORDER BY tweets.timestamp DESC)
FROM tweets
JOIN follows ON follows.followee_id = tweets.sender_id
GROUP BY follows.follower_id
The join of the streams corresponds directly to the join of the tables in that query.
The timelines are effectively a cache of the result of this query, updated every time the
underlying tables change.iii
Time-dependence of joins
The three types of joins described here (stream-stream, stream-table, and table-table)
have a lot in common: they all require the stream processor to maintain some state
(search and click events, user profiles, or follower list) based on one join input, and
query that state on messages from the other join input.
The order of the events that maintain the state is important (it matters whether you
first follow and then unfollow, or the other way round). In a partitioned log, the
ordering of events within a single partition is preserved, but there is typically no
ordering guarantee across different streams or partitions.
This raises a question: if events on different streams happen around a similar time, in
which order are they processed? In the stream-table join example, if a user updates
their profile, which activity events are joined with the old profile (processed before
the profile update), and which are joined with the new profile (processed after the
Processing Streams 
| 
475


profile update)? Put another way: if state changes over time, and you join with some
state, what point in time do you use for the join [45]?
Such time dependence can occur in many places. For example, if you sell things, you
need to apply the right tax rate to invoices, which depends on the country or state,
the type of product, and the date of sale (since tax rates change from time to time).
When joining sales to a table of tax rates, you probably want to join with the tax rate
at the time of the sale, which may be different from the current tax rate if you are
reprocessing historical data.
If the ordering of events across streams is undetermined, the join becomes nondeter‐
ministic [87], which means you cannot rerun the same job on the same input and
necessarily get the same result: the events on the input streams may be interleaved in
a different way when you run the job again.
In data warehouses, this issue is known as a slowly changing dimension (SCD), and it
is often addressed by using a unique identifier for a particular version of the joined
record: for example, every time the tax rate changes, it is given a new identifier, and
the invoice includes the identifier for the tax rate at the time of sale [88, 89]. This
change makes the join deterministic, but has the consequence that log compaction is
not possible, since all versions of the records in the table need to be retained. 
Fault Tolerance
In the final section of this chapter, let’s consider how stream processors can tolerate
faults. We saw in Chapter 10 that batch processing frameworks can tolerate faults
fairly easily: if a task in a MapReduce job fails, it can simply be started again on
another machine, and the output of the failed task is discarded. This transparent retry
is possible because input files are immutable, each task writes its output to a separate
file on HDFS, and output is only made visible when a task completes successfully.
In particular, the batch approach to fault tolerance ensures that the output of the
batch job is the same as if nothing had gone wrong, even if in fact some tasks did fail.
It appears as though every input record was processed exactly once—no records are
skipped, and none are processed twice. Although restarting tasks means that records
may in fact be processed multiple times, the visible effect in the output is as if they
had only been processed once. This principle is known as exactly-once semantics,
although effectively-once would be a more descriptive term [90].
The same issue of fault tolerance arises in stream processing, but it is less straightfor‐
ward to handle: waiting until a task is finished before making its output visible is not
an option, because a stream is infinite and so you can never finish processing it.
476 
| 
Chapter 11: Stream Processing


Microbatching and checkpointing
One solution is to break the stream into small blocks, and treat each block like a min‐
iature batch process. This approach is called microbatching, and it is used in Spark
Streaming [91]. The batch size is typically around one second, which is the result of a
performance compromise: smaller batches incur greater scheduling and coordination
overhead, while larger batches mean a longer delay before results of the stream pro‐
cessor become visible.
Microbatching also implicitly provides a tumbling window equal to the batch size
(windowed by processing time, not event timestamps); any jobs that require larger
windows need to explicitly carry over state from one microbatch to the next.
A variant approach, used in Apache Flink, is to periodically generate rolling check‐
points of state and write them to durable storage [92, 93]. If a stream operator
crashes, it can restart from its most recent checkpoint and discard any output gener‐
ated between the last checkpoint and the crash. The checkpoints are triggered by bar‐
riers in the message stream, similar to the boundaries between microbatches, but
without forcing a particular window size.
Within the confines of the stream processing framework, the microbatching and
checkpointing approaches provide the same exactly-once semantics as batch process‐
ing. However, as soon as output leaves the stream processor (for example, by writing
to a database, sending messages to an external message broker, or sending emails),
the framework is no longer able to discard the output of a failed batch. In this case,
restarting a failed task causes the external side effect to happen twice, and micro‐
batching or checkpointing alone is not sufficient to prevent this problem.
Atomic commit revisited
In order to give the appearance of exactly-once processing in the presence of faults,
we need to ensure that all outputs and side effects of processing an event take effect if
and only if the processing is successful. Those effects include any messages sent to
downstream operators or external messaging systems (including email or push notifi‐
cations), any database writes, any changes to operator state, and any acknowledg‐
ment of input messages (including moving the consumer offset forward in a logbased message broker).
Those things either all need to happen atomically, or none of them must happen, but
they should not go out of sync with each other. If this approach sounds familiar, it is
because we discussed it in “Exactly-once message processing” on page 360 in the con‐
text of distributed transactions and two-phase commit.
In Chapter 9 we discussed the problems in the traditional implementations of dis‐
tributed transactions, such as XA. However, in more restricted environments it is
possible to implement such an atomic commit facility efficiently. This approach is
Processing Streams 
| 
477


used in Google Cloud Dataflow [81, 92] and VoltDB [94], and there are plans to add
similar features to Apache Kafka [95, 96]. Unlike XA, these implementations do not
attempt to provide transactions across heterogeneous technologies, but instead keep
them internal by managing both state changes and messaging within the stream pro‐
cessing framework. The overhead of the transaction protocol can be amortized by
processing several input messages within a single transaction.
Idempotence
Our goal is to discard the partial output of any failed tasks so that they can be safely
retried without taking effect twice. Distributed transactions are one way of achieving
that goal, but another way is to rely on idempotence [97].
An idempotent operation is one that you can perform multiple times, and it has the
same effect as if you performed it only once. For example, setting a key in a key-value
store to some fixed value is idempotent (writing the value again simply overwrites the
value with an identical value), whereas incrementing a counter is not idempotent
(performing the increment again means the value is incremented twice).
Even if an operation is not naturally idempotent, it can often be made idempotent
with a bit of extra metadata. For example, when consuming messages from Kafka,
every message has a persistent, monotonically increasing offset. When writing a value
to an external database, you can include the offset of the message that triggered the
last write with the value. Thus, you can tell whether an update has already been
applied, and avoid performing the same update again.
The state handling in Storm’s Trident is based on a similar idea [78]. Relying on
idempotence implies several assumptions: restarting a failed task must replay the
same messages in the same order (a log-based message broker does this), the process‐
ing must be deterministic, and no other node may concurrently update the same
value [98, 99].
When failing over from one processing node to another, fencing may be required (see
“The leader and the lock” on page 301) to prevent interference from a node that is
thought to be dead but is actually alive. Despite all those caveats, idempotent opera‐
tions can be an effective way of achieving exactly-once semantics with only a small
overhead.
Rebuilding state after a failure
Any stream process that requires state—for example, any windowed aggregations
(such as counters, averages, and histograms) and any tables and indexes used for
joins—must ensure that this state can be recovered after a failure.
One option is to keep the state in a remote datastore and replicate it, although having
to query a remote database for each individual message can be slow, as discussed in
478 
| 
Chapter 11: Stream Processing


“Stream-table join (stream enrichment)” on page 473. An alternative is to keep state
local to the stream processor, and replicate it periodically. Then, when the stream
processor is recovering from a failure, the new task can read the replicated state and
resume processing without data loss.
For example, Flink periodically captures snapshots of operator state and writes them
to durable storage such as HDFS [92, 93]; Samza and Kafka Streams replicate state
changes by sending them to a dedicated Kafka topic with log compaction, similar to
change data capture [84, 100]. VoltDB replicates state by redundantly processing
each input message on several nodes (see “Actual Serial Execution” on page 252).
In some cases, it may not even be necessary to replicate the state, because it can be
rebuilt from the input streams. For example, if the state consists of aggregations over
a fairly short window, it may be fast enough to simply replay the input events corre‐
sponding to that window. If the state is a local replica of a database, maintained by
change data capture, the database can also be rebuilt from the log-compacted change
stream (see “Log compaction” on page 456).
However, all of these trade-offs depend on the performance characteristics of the
underlying infrastructure: in some systems, network delay may be lower than disk
access latency, and network bandwidth may be comparable to disk bandwidth. There
is no universally ideal trade-off for all situations, and the merits of local versus
remote state may also shift as storage and networking technologies evolve. 
Summary
In this chapter we have discussed event streams, what purposes they serve, and how
to process them. In some ways, stream processing is very much like the batch pro‐
cessing we discussed in Chapter 10, but done continuously on unbounded (neverending) streams rather than on a fixed-size input. From this perspective, message
brokers and event logs serve as the streaming equivalent of a filesystem.
We spent some time comparing two types of message brokers:
AMQP/JMS-style message broker
The broker assigns individual messages to consumers, and consumers acknowl‐
edge individual messages when they have been successfully processed. Messages
are deleted from the broker once they have been acknowledged. This approach is
appropriate as an asynchronous form of RPC (see also “Message-Passing Data‐
flow” on page 136), for example in a task queue, where the exact order of mes‐
sage processing is not important and where there is no need to go back and read
old messages again after they have been processed.
Summary 
| 
479


Log-based message broker
The broker assigns all messages in a partition to the same consumer node, and
always delivers messages in the same order. Parallelism is achieved through par‐
titioning, and consumers track their progress by checkpointing the offset of the
last message they have processed. The broker retains messages on disk, so it is
possible to jump back and reread old messages if necessary.
The log-based approach has similarities to the replication logs found in databases
(see Chapter 5) and log-structured storage engines (see Chapter 3). We saw that this
approach is especially appropriate for stream processing systems that consume input
streams and generate derived state or derived output streams.
In terms of where streams come from, we discussed several possibilities: user activity
events, sensors providing periodic readings, and data feeds (e.g., market data in
finance) are naturally represented as streams. We saw that it can also be useful to
think of the writes to a database as a stream: we can capture the changelog—i.e., the
history of all changes made to a database—either implicitly through change data cap‐
ture or explicitly through event sourcing. Log compaction allows the stream to retain
a full copy of the contents of a database.
Representing databases as streams opens up powerful opportunities for integrating
systems. You can keep derived data systems such as search indexes, caches, and ana‐
lytics systems continually up to date by consuming the log of changes and applying
them to the derived system. You can even build fresh views onto existing data by
starting from scratch and consuming the log of changes from the beginning all the
way to the present.
The facilities for maintaining state as streams and replaying messages are also the
basis for the techniques that enable stream joins and fault tolerance in various stream
processing frameworks. We discussed several purposes of stream processing, includ‐
ing searching for event patterns (complex event processing), computing windowed
aggregations (stream analytics), and keeping derived data systems up to date (materi‐
alized views).
We then discussed the difficulties of reasoning about time in a stream processor,
including the distinction between processing time and event timestamps, and the
problem of dealing with straggler events that arrive after you thought your window
was complete.
We distinguished three types of joins that may appear in stream processes:
Stream-stream joins
Both input streams consist of activity events, and the join operator searches for
related events that occur within some window of time. For example, it may
match two actions taken by the same user within 30 minutes of each other. The
480 
| 
Chapter 11: Stream Processing


two join inputs may in fact be the same stream (a self-join) if you want to find
related events within that one stream.
Stream-table joins
One input stream consists of activity events, while the other is a database change‐
log. The changelog keeps a local copy of the database up to date. For each activity
event, the join operator queries the database and outputs an enriched activity
event.
Table-table joins
Both input streams are database changelogs. In this case, every change on one
side is joined with the latest state of the other side. The result is a stream of
changes to the materialized view of the join between the two tables.
Finally, we discussed techniques for achieving fault tolerance and exactly-once
semantics in a stream processor. As with batch processing, we need to discard the
partial output of any failed tasks. However, since a stream process is long-running
and produces output continuously, we can’t simply discard all output. Instead, a
finer-grained recovery mechanism can be used, based on microbatching, checkpoint‐
ing, transactions, or idempotent writes. 
References
[1] Tyler Akidau, Robert Bradshaw, Craig Chambers, et al.: “The Dataflow Model: A
Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale,
Unbounded, Out-of-Order Data Processing,” Proceedings of the VLDB Endowment,
volume 8, number 12, pages 1792–1803, August 2015. doi:10.14778/2824032.2824076
[2] Harold Abelson, Gerald Jay Sussman, and Julie Sussman: Structure and Interpre‐
tation 
of 
Computer 
Programs, 
2nd 
edition. 
MIT 
Press, 
1996. 
ISBN:
978-0-262-51087-5, available online at mitpress.mit.edu
[3] Patrick Th. Eugster, Pascal A. Felber, Rachid Guerraoui, and Anne-Marie Ker‐
marrec: “The Many Faces of Publish/Subscribe,” ACM Computing Surveys, volume
35, number 2, pages 114–131, June 2003. doi:10.1145/857076.857078
[4] Joseph M. Hellerstein and Michael Stonebraker: Readings in Database Systems,
4th edition. MIT Press, 2005. ISBN: 978-0-262-69314-1, available online at red‐
book.cs.berkeley.edu
[5] Don Carney, Uğur Çetintemel, Mitch Cherniack, et al.: “Monitoring Streams – A
New Class of Data Management Applications,” at 28th International Conference on
Very Large Data Bases (VLDB), August 2002.
[6] Matthew Sackman: “Pushing Back,” lshift.net, May 5, 2016.
Summary 
| 
481


[7] Vicent Martí: “Brubeck, a statsd-Compatible Metrics Aggregator,” githubengin‐
eering.com, June 15, 2015.
[8] Seth Lowenberger: “MoldUDP64 Protocol Specification V 1.00,” nasdaq‐
trader.com, July 2009.
[9] Pieter Hintjens: ZeroMQ – The Guide. O’Reilly Media, 2013. ISBN:
978-1-449-33404-8
[10] Ian Malpass: “Measure Anything, Measure Everything,” codeascraft.com, Febru‐
ary 15, 2011.
[11] Dieter Plaetinck: “25 Graphite, Grafana and statsd Gotchas,” blog.raintank.io,
March 3, 2016.
[12] Jeff Lindsay: “Web Hooks to Revolutionize the Web,” progrium.com, May 3,
2007.
[13] Jim N. Gray: “Queues Are Databases,” Microsoft Research Technical Report
MSR-TR-95-56, December 1995.
[14] Mark Hapner, Rich Burridge, Rahul Sharma, et al.: “JSR-343 Java Message Ser‐
vice (JMS) 2.0 Specification,” jms-spec.java.net, March 2013.
[15] Sanjay Aiyagari, Matthew Arrott, Mark Atwell, et al.: “AMQP: Advanced Mes‐
sage Queuing Protocol Specification,” Version 0-9-1, November 2008.
[16] “Google Cloud Pub/Sub: A Google-Scale Messaging Service,” cloud.google.com,
2016.
[17] “Apache Kafka 0.9 Documentation,” kafka.apache.org, November 2015.
[18] Jay Kreps, Neha Narkhede, and Jun Rao: “Kafka: A Distributed Messaging Sys‐
tem for Log Processing,” at 6th International Workshop on Networking Meets Data‐
bases (NetDB), June 2011.
[19] “Amazon Kinesis Streams Developer Guide,” docs.aws.amazon.com, April 2016.
[20] Leigh Stewart and Sijie Guo: “Building DistributedLog: Twitter’s High-
Performance Replicated Log Service,” blog.twitter.com, September 16, 2015.
[21] “DistributedLog Documentation,” Twitter, Inc., distributedlog.io, May 2016.
[22] Jay Kreps: “Benchmarking Apache Kafka: 2 Million Writes Per Second (On
Three Cheap Machines),” engineering.linkedin.com, April 27, 2014.
[23] Kartik Paramasivam: “How We’re Improving and Advancing Kafka at
LinkedIn,” engineering.linkedin.com, September 2, 2015.
[24] Jay Kreps: “The Log: What Every Software Engineer Should Know About Real-
Time Data’s Unifying Abstraction,” engineering.linkedin.com, December 16, 2013.
482 
| 
Chapter 11: Stream Processing


[25] Shirshanka Das, Chavdar Botev, Kapil Surlaker, et al.: “All Aboard the Data‐
bus!,” at 3rd ACM Symposium on Cloud Computing (SoCC), October 2012.
[26] Yogeshwer Sharma, Philippe Ajoux, Petchean Ang, et al.: “Wormhole: Reliable
Pub-Sub to Support Geo-Replicated Internet Services,” at 12th USENIX Symposium
on Networked Systems Design and Implementation (NSDI), May 2015.
[27] P. P. S. Narayan: “Sherpa Update,” developer.yahoo.com, June 8, .
[28] Martin Kleppmann: “Bottled Water: Real-Time Integration of PostgreSQL and
Kafka,” martin.kleppmann.com, April 23, 2015.
[29] Ben Osheroff: “Introducing Maxwell, a mysql-to-kafka Binlog Processor,” devel‐
oper.zendesk.com, August 20, 2015.
[30] Randall Hauch: “Debezium 0.2.1 Released,” debezium.io, June 10, 2016.
[31] Prem Santosh Udaya Shankar: “Streaming MySQL Tables in Real-Time to
Kafka,” engineeringblog.yelp.com, August 1, 2016.
[32] “Mongoriver,” Stripe, Inc., github.com, September 2014.
[33] Dan Harvey: “Change Data Capture with Mongo + Kafka,” at Hadoop Users
Group UK, August 2015.
[34] “Oracle GoldenGate 12c: Real-Time Access to Real-Time Information,” Oracle
White Paper, March 2015.
[35] “Oracle GoldenGate Fundamentals: How Oracle GoldenGate Works,” Oracle
Corporation, youtube.com, November 2012.
[36] Slava Akhmechet: “Advancing the Realtime Web,” rethinkdb.com, January 27,
2015.
[37] “Firebase Realtime Database Documentation,” Google, Inc., firebase.google.com,
May 2016.
[38] “Apache CouchDB 1.6 Documentation,” docs.couchdb.org, 2014.
[39] Matt DeBergalis: “Meteor 0.7.0: Scalable Database Queries Using MongoDB
Oplog Instead of Poll-and-Diff,” info.meteor.com, December 17, 2013.
[40] “Chapter 15. Importing and Exporting Live Data,” VoltDB 6.4 User Manual,
docs.voltdb.com, June 2016.
[41] Neha Narkhede: “Announcing Kafka Connect: Building Large-Scale Low-
Latency Data Pipelines,” confluent.io, February 18, 2016.
[42] Greg Young: “CQRS and Event Sourcing,” at Code on the Beach, August 2014.
[43] Martin Fowler: “Event Sourcing,” martinfowler.com, December 12, 2005.
Summary 
| 
483


[44] Vaughn Vernon: Implementing Domain-Driven Design. Addison-Wesley Profes‐
sional, 2013. ISBN: 978-0-321-83457-7
[45] H. V. Jagadish, Inderpal Singh Mumick, and Abraham Silberschatz: “View
Maintenance Issues for the Chronicle Data Model,” at 14th ACM SIGACT-SIGMOD-
SIGART Symposium on Principles of Database Systems (PODS), May 1995. doi:
10.1145/212433.220201
[46] “Event Store 3.5.0 Documentation,” Event Store LLP, docs.geteventstore.com,
February 2016.
[47] Martin Kleppmann: Making Sense of Stream Processing. Report, O’Reilly Media,
May 2016.
[48] Sander Mak: “Event-Sourced Architectures with Akka,” at JavaOne, September
2014.
[49] Julian Hyde: personal communication, June 2016.
[50] Ashish Gupta and Inderpal Singh Mumick: Materialized Views: Techniques,
Implementations, and Applications. MIT Press, 1999. ISBN: 978-0-262-57122-7
[51] Timothy Griffin and Leonid Libkin: “Incremental Maintenance of Views with
Duplicates,” at ACM International Conference on Management of Data (SIGMOD),
May 1995. doi:10.1145/223784.223849
[52] Pat Helland: “Immutability Changes Everything,” at 7th Biennial Conference on
Innovative Data Systems Research (CIDR), January 2015.
[53] Martin Kleppmann: “Accounting for Computer Scientists,” martin.klepp‐
mann.com, March 7, 2011.
[54] Pat Helland: “Accountants Don’t Use Erasers,” blogs.msdn.com, June 14, 2007.
[55] Fangjin Yang: “Dogfooding with Druid, Samza, and Kafka: Metametrics at Met‐
amarkets,” metamarkets.com, June 3, 2015.
[56] Gavin Li, Jianqiu Lv, and Hang Qi: “Pistachio: Co-Locate the Data and Compute
for Fastest Cloud Compute,” yahoohadoop.tumblr.com, April 13, 2015.
[57] Kartik Paramasivam: “Stream Processing Hard Problems – Part 1: Killing
Lambda,” engineering.linkedin.com, June 27, 2016.
[58] Martin Fowler: “CQRS,” martinfowler.com, July 14, 2011.
[59] Greg Young: “CQRS Documents,” cqrs.files.wordpress.com, November 2010.
[60] Baron Schwartz: “Immutability, MVCC, and Garbage Collection,” xaprb.com,
December 28, 2013.
484 
| 
Chapter 11: Stream Processing


[61] Daniel Eloff, Slava Akhmechet, Jay Kreps, et al.: “Re: Turning the Database
Inside-out with Apache Samza,” Hacker News discussion, news.ycombinator.com,
March 4, 2015.
[62] “Datomic Development Resources: Excision,” Cognitect, Inc., docs.datomic.com.
[63] “Fossil Documentation: Deleting Content from Fossil,” fossil-scm.org, 2016.
[64] Jay Kreps: “The irony of distributed systems is that data loss is really easy but
deleting data is surprisingly hard,” twitter.com, March 30, 2015.
[65] David C. Luckham: “What’s the Difference Between ESP and CEP?,” complexe‐
vents.com, August 1, 2006.
[66] Srinath Perera: “How Is Stream Processing and Complex Event Processing
(CEP) Different?,” quora.com, December 3, 2015.
[67] Arvind Arasu, Shivnath Babu, and Jennifer Widom: “The CQL Continuous
Query Language: Semantic Foundations and Query Execution,” The VLDB Journal,
volume 15, number 2, pages 121–142, June 2006. doi:10.1007/s00778-004-0147-z
[68] Julian Hyde: “Data in Flight: How Streaming SQL Technology Can Help Solve
the Web 2.0 Data Crunch,” ACM Queue, volume 7, number 11, December 2009. doi:
10.1145/1661785.1667562
[69] “Esper Reference, Version 5.4.0,” EsperTech, Inc., espertech.com, April 2016.
[70] Zubair Nabi, Eric Bouillet, Andrew Bainbridge, and Chris Thomas: “Of Streams
and Storms,” IBM technical report, developer.ibm.com, April 2014.
[71] Milinda Pathirage, Julian Hyde, Yi Pan, and Beth Plale: “SamzaSQL: Scalable
Fast Data Management with Streaming SQL,” at IEEE International Workshop on
High-Performance Big Data Computing (HPBDC), May 2016. doi:10.1109/IPDPSW.
2016.141
[72] Philippe Flajolet, Éric Fusy, Olivier Gandouet, and Frédéric Meunier: “HyperLog
Log: The Analysis of a Near-Optimal Cardinality Estimation Algorithm,” at Confer‐
ence on Analysis of Algorithms (AofA), June 2007.
[73] Jay Kreps: “Questioning the Lambda Architecture,” oreilly.com, July 2, 2014.
[74] Ian Hellström: “An Overview of Apache Streaming Technologies,” database‐
line.wordpress.com, March 12, 2016.
[75] Jay Kreps: “Why Local State Is a Fundamental Primitive in Stream Processing,”
oreilly.com, July 31, 2014.
[76] Shay Banon: “Percolator,” elastic.co, February 8, 2011.
[77] Alan Woodward and Martin Kleppmann: “Real-Time Full-Text Search with
Luwak and Samza,” martin.kleppmann.com, April 13, 2015.
Summary 
| 
485


[78] “Apache Storm 1.0.1 Documentation,” storm.apache.org, May 2016.
[79] Tyler Akidau: “The World Beyond Batch: Streaming 102,” oreilly.com, January
20, 2016.
[80] Stephan Ewen: “Streaming Analytics with Apache Flink,” at Kafka Summit, April
2016.
[81] Tyler Akidau, Alex Balikov, Kaya Bekiroğlu, et al.: “MillWheel: Fault-Tolerant
Stream Processing at Internet Scale,” at 39th International Conference on Very Large
Data Bases (VLDB), August 2013.
[82] Alex Dean: “Improving Snowplow’s Understanding of Time,” snowplowanalyt‐
ics.com, September 15, 2015.
[83] “Windowing (Azure Stream Analytics),” Microsoft Azure Reference,
msdn.microsoft.com, April 2016.
[84] “State Management,” Apache Samza 0.10 Documentation, samza.apache.org,
December 2015.
[85] Rajagopal Ananthanarayanan, Venkatesh Basker, Sumit Das, et al.: “Photon:
Fault-Tolerant and Scalable Joining of Continuous Data Streams,” at ACM Interna‐
tional Conference on Management of Data (SIGMOD), June 2013. doi:
10.1145/2463676.2465272
[86] Martin Kleppmann: “Samza Newsfeed Demo,” github.com, September 2014.
[87] Ben Kirwin: “Doing the Impossible: Exactly-Once Messaging Patterns in Kafka,”
ben.kirw.in, November 28, 2014.
[88] Pat Helland: “Data on the Outside Versus Data on the Inside,” at 2nd Biennial
Conference on Innovative Data Systems Research (CIDR), January 2005.
[89] Ralph Kimball and Margy Ross: The Data Warehouse Toolkit: The Definitive
Guide to Dimensional Modeling, 3rd edition. John Wiley & Sons, 2013. ISBN:
978-1-118-53080-1
[90] Viktor Klang: “I’m coining the phrase ‘effectively-once’ for message processing
with at-least-once + idempotent operations,” twitter.com, October 20, 2016.
[91] Matei Zaharia, Tathagata Das, Haoyuan Li, et al.: “Discretized Streams: An Effi‐
cient and Fault-Tolerant Model for Stream Processing on Large Clusters,” at 4th
USENIX Conference in Hot Topics in Cloud Computing (HotCloud), June 2012.
[92] Kostas Tzoumas, Stephan Ewen, and Robert Metzger: “High-Throughput, Low-
Latency, and Exactly-Once Stream Processing with Apache Flink,” data-artisans.com,
August 5, 2015.
486 
| 
Chapter 11: Stream Processing


[93] Paris Carbone, Gyula Fóra, Stephan Ewen, et al.: “Lightweight Asynchronous
Snapshots for Distributed Dataflows,” arXiv:1506.08603 [cs.DC], June 29, 2015.
[94] Ryan Betts and John Hugg: Fast Data: Smart and at Scale. Report, O’Reilly
Media, October 2015.
[95] Flavio Junqueira: “Making Sense of Exactly-Once Semantics,” at Strata+Hadoop
World London, June 2016.
[96] Jason Gustafson, Flavio Junqueira, Apurva Mehta, Sriram Subramanian, and
Guozhang Wang: “KIP-98 – Exactly Once Delivery and Transactional Messaging,”
cwiki.apache.org, November 2016.
[97] Pat Helland: “Idempotence Is Not a Medical Condition,” Communications of the
ACM, volume 55, number 5, page 56, May 2012. doi:10.1145/2160718.2160734
[98] Jay Kreps: “Re: Trying to Achieve Deterministic Behavior on Recovery/Rewind,”
email to samza-dev mailing list, September 9, 2014.
[99] E. N. (Mootaz) Elnozahy, Lorenzo Alvisi, Yi-Min Wang, and David B. Johnson:
“A Survey of Rollback-Recovery Protocols in Message-Passing Systems,” ACM Com‐
puting Surveys, volume 34, number 3, pages 375–408, September 2002. doi:
10.1145/568522.568525
[100] Adam Warski: “Kafka Streams – How Does It Fit the Stream Processing Land‐
scape?,” softwaremill.com, June 1, 2016.
Summary 
| 
487




CHAPTER 12
The Future of Data Systems
If a thing be ordained to another as to its end, its last end cannot consist in the preservation
of its being. Hence a captain does not intend as a last end, the preservation of the ship
entrusted to him, since a ship is ordained to something else as its end, viz. to navigation.
(Often quoted as: If the highest aim of a captain was the preserve his ship, he would keep it
in port forever.)
—St. Thomas Aquinas, Summa Theologica (1265–1274)
So far, this book has been mostly about describing things as they are at present. In
this final chapter, we will shift our perspective toward the future and discuss how
things should be: I will propose some ideas and approaches that, I believe, may funda‐
mentally improve the ways we design and build applications.
Opinions and speculation about the future are of course subjective, and so I will use
the first person in this chapter when writing about my personal opinions. You are
welcome to disagree with them and form your own opinions, but I hope that the
ideas in this chapter will at least be a starting point for a productive discussion and
bring some clarity to concepts that are often confused.
The goal of this book was outlined in Chapter 1: to explore how to create applications
and systems that are reliable, scalable, and maintainable. These themes have run
through all of the chapters: for example, we discussed many fault-tolerance algo‐
rithms that help improve reliability, partitioning to improve scalability, and mecha‐
nisms for evolution and abstraction that improve maintainability. In this chapter we
will bring all of these ideas together, and build on them to envisage the future. Our
goal is to discover how to design applications that are better than the ones of today—
robust, correct, evolvable, and ultimately beneficial to humanity.
489


Data Integration
A recurring theme in this book has been that for any given problem, there are several
solutions, all of which have different pros, cons, and trade-offs. For example, when
discussing storage engines in Chapter 3, we saw log-structured storage, B-trees, and
column-oriented storage. When discussing replication in Chapter 5, we saw singleleader, multi-leader, and leaderless approaches.
If you have a problem such as “I want to store some data and look it up again later,”
there is no one right solution, but many different approaches that are each appropri‐
ate in different circumstances. A software implementation typically has to pick one
particular approach. It’s hard enough to get one code path robust and performing
well—trying to do everything in one piece of software almost guarantees that the
implementation will be poor.
Thus, the most appropriate choice of software tool also depends on the circumstan‐
ces. Every piece of software, even a so-called “general-purpose” database, is designed
for a particular usage pattern.
Faced with this profusion of alternatives, the first challenge is then to figure out the
mapping between the software products and the circumstances in which they are a
good fit. Vendors are understandably reluctant to tell you about the kinds of work‐
loads for which their software is poorly suited, but hopefully the previous chapters
have equipped you with some questions to ask in order to read between the lines and
better understand the trade-offs.
However, even if you perfectly understand the mapping between tools and circum‐
stances for their use, there is another challenge: in complex applications, data is often
used in several different ways. There is unlikely to be one piece of software that is
suitable for all the different circumstances in which the data is used, so you inevitably
end up having to cobble together several different pieces of software in order to pro‐
vide your application’s functionality.
Combining Specialized Tools by Deriving Data
For example, it is common to need to integrate an OLTP database with a full-text
search index in order to handle queries for arbitrary keywords. Although some data‐
bases (such as PostgreSQL) include a full-text indexing feature, which can be suffi‐
cient for simple applications [1], more sophisticated search facilities require specialist
information retrieval tools. Conversely, search indexes are generally not very suitable
as a durable system of record, and so many applications need to combine two differ‐
ent tools in order to satisfy all of the requirements.
We touched on the issue of integrating data systems in “Keeping Systems in Sync” on
page 452. As the number of different representations of the data increases, the inte‐
490 
| 
Chapter 12: The Future of Data Systems


gration problem becomes harder. Besides the database and the search index, perhaps
you need to keep copies of the data in analytics systems (data warehouses, or batch
and stream processing systems); maintain caches or denormalized versions of objects
that were derived from the original data; pass the data through machine learning,
classification, ranking, or recommendation systems; or send notifications based on
changes to the data.
Surprisingly often I see software engineers make statements like, “In my experience,
99% of people only need X” or “…don’t need X” (for various values of X). I think that
such statements say more about the experience of the speaker than about the actual
usefulness of a technology. The range of different things you might want to do with
data is dizzyingly wide. What one person considers to be an obscure and pointless
feature may well be a central requirement for someone else. The need for data inte‐
gration often only becomes apparent if you zoom out and consider the dataflows
across an entire organization.
Reasoning about dataflows
When copies of the same data need to be maintained in several storage systems in
order to satisfy different access patterns, you need to be very clear about the inputs
and outputs: where is data written first, and which representations are derived from
which sources? How do you get data into all the right places, in the right formats?
For example, you might arrange for data to first be written to a system of record data‐
base, capturing the changes made to that database (see “Change Data Capture” on
page 454) and then applying the changes to the search index in the same order. If
change data capture (CDC) is the only way of updating the index, you can be confi‐
dent that the index is entirely derived from the system of record, and therefore con‐
sistent with it (barring bugs in the software). Writing to the database is the only way
of supplying new input into this system.
Allowing the application to directly write to both the search index and the database
introduces the problem shown in Figure 11-4, in which two clients concurrently send
conflicting writes, and the two storage systems process them in a different order. In
this case, neither the database nor the search index is “in charge” of determining the
order of writes, and so they may make contradictory decisions and become perma‐
nently inconsistent with each other.
If it is possible for you to funnel all user input through a single system that decides on
an ordering for all writes, it becomes much easier to derive other representations of
the data by processing the writes in the same order. This is an application of the state
machine replication approach that we saw in “Total Order Broadcast” on page 348.
Whether you use change data capture or an event sourcing log is less important than
simply the principle of deciding on a total order.
Data Integration 
| 
491


Updating a derived data system based on an event log can often be made determinis‐
tic and idempotent (see “Idempotence” on page 478), making it quite easy to recover
from faults.
Derived data versus distributed transactions
The classic approach for keeping different data systems consistent with each other
involves distributed transactions, as discussed in “Atomic Commit and Two-Phase
Commit (2PC)” on page 354. How does the approach of using derived data systems
fare in comparison to distributed transactions?
At an abstract level, they achieve a similar goal by different means. Distributed trans‐
actions decide on an ordering of writes by using locks for mutual exclusion (see
“Two-Phase Locking (2PL)” on page 257), while CDC and event sourcing use a log
for ordering. Distributed transactions use atomic commit to ensure that changes take
effect exactly once, while log-based systems are often based on deterministic retry
and idempotence.
The biggest difference is that transaction systems usually provide linearizability (see
“Linearizability” on page 324), which implies useful guarantees such as reading your
own writes (see “Reading Your Own Writes” on page 162). On the other hand,
derived data systems are often updated asynchronously, and so they do not by default
offer the same timing guarantees.
Within limited environments that are willing to pay the cost of distributed transac‐
tions, they have been used successfully. However, I think that XA has poor fault toler‐
ance and performance characteristics (see “Distributed Transactions in Practice” on
page 360), which severely limit its usefulness. I believe that it might be possible to
create a better protocol for distributed transactions, but getting such a protocol
widely adopted and integrated with existing tools would be challenging, and unlikely
to happen soon.
In the absence of widespread support for a good distributed transaction protocol, I
believe that log-based derived data is the most promising approach for integrating
different data systems. However, guarantees such as reading your own writes are use‐
ful, and I don’t think that it is productive to tell everyone “eventual consistency is
inevitable—suck it up and learn to deal with it” (at least not without good guidance
on how to deal with it).
In “Aiming for Correctness” on page 515 we will discuss some approaches for imple‐
menting stronger guarantees on top of asynchronously derived systems, and work
toward a middle ground between distributed transactions and asynchronous logbased systems.
492 
| 
Chapter 12: The Future of Data Systems


The limits of total ordering
With systems that are small enough, constructing a totally ordered event log is
entirely feasible (as demonstrated by the popularity of databases with single-leader
replication, which construct precisely such a log). However, as systems are scaled
toward bigger and more complex workloads, limitations begin to emerge:
• In most cases, constructing a totally ordered log requires all events to pass
through a single leader node that decides on the ordering. If the throughput of
events is greater than a single machine can handle, you need to partition it across
multiple machines (see “Partitioned Logs” on page 446). The order of events in
two different partitions is then ambiguous.
• If the servers are spread across multiple geographically distributed datacenters,
for example in order to tolerate an entire datacenter going offline, you typically
have a separate leader in each datacenter, because network delays make synchro‐
nous cross-datacenter coordination inefficient (see “Multi-Leader Replication”
on page 168). This implies an undefined ordering of events that originate in two
different datacenters.
• When applications are deployed as microservices (see “Dataflow Through Serv‐
ices: REST and RPC” on page 131), a common design choice is to deploy each
service and its durable state as an independent unit, with no durable state shared
between services. When two events originate in different services, there is no
defined order for those events.
• Some applications maintain client-side state that is updated immediately on user
input (without waiting for confirmation from a server), and even continue to
work offline (see “Clients with offline operation” on page 170). With such appli‐
cations, clients and servers are very likely to see events in different orders.
In formal terms, deciding on a total order of events is known as total order broadcast,
which is equivalent to consensus (see “Consensus algorithms and total order broad‐
cast” on page 366). Most consensus algorithms are designed for situations in which
the throughput of a single node is sufficient to process the entire stream of events,
and these algorithms do not provide a mechanism for multiple nodes to share the
work of ordering the events. It is still an open research problem to design consensus
algorithms that can scale beyond the throughput of a single node and that work well
in a geographically distributed setting.
Ordering events to capture causality
In cases where there is no causal link between events, the lack of a total order is not a
big problem, since concurrent events can be ordered arbitrarily. Some other cases are
easy to handle: for example, when there are multiple updates of the same object, they
can be totally ordered by routing all updates for a particular object ID to the same log
Data Integration 
| 
493


partition. However, causal dependencies sometimes arise in more subtle ways (see
also “Ordering and Causality” on page 339).
For example, consider a social networking service, and two users who were in a rela‐
tionship but have just broken up. One of the users removes the other as a friend, and
then sends a message to their remaining friends complaining about their ex-partner.
The user’s intention is that their ex-partner should not see the rude message, since
the message was sent after the friend status was revoked.
However, in a system that stores friendship status in one place and messages in
another place, that ordering dependency between the unfriend event and the messagesend event may be lost. If the causal dependency is not captured, a service that sends
notifications about new messages may process the message-send event before the
unfriend event, and thus incorrectly send a notification to the ex-partner.
In this example, the notifications are effectively a join between the messages and the
friend list, making it related to the timing issues of joins that we discussed previously
(see “Time-dependence of joins” on page 475). Unfortunately, there does not seem to
be a simple answer to this problem [2, 3]. Starting points include: 
• Logical timestamps can provide total ordering without coordination (see
“Sequence Number Ordering” on page 343), so they may help in cases where
total order broadcast is not feasible. However, they still require recipients to han‐
dle events that are delivered out of order, and they require additional metadata to
be passed around.
• If you can log an event to record the state of the system that the user saw before
making a decision, and give that event a unique identifier, then any later events
can reference that event identifier in order to record the causal dependency [4].
We will return to this idea in “Reads are events too” on page 513.
• Conflict resolution algorithms (see “Automatic Conflict Resolution” on page
174) help with processing events that are delivered in an unexpected order. They
are useful for maintaining state, but they do not help if actions have external side
effects (such as sending a notification to a user).
Perhaps, over time, patterns for application development will emerge that allow
causal dependencies to be captured efficiently, and derived state to be maintained
correctly, without forcing all events to go through the bottleneck of total order
broadcast. 
Batch and Stream Processing
I would say that the goal of data integration is to make sure that data ends up in the
right form in all the right places. Doing so requires consuming inputs, transforming,
joining, filtering, aggregating, training models, evaluating, and eventually writing to
494 
| 
Chapter 12: The Future of Data Systems


the appropriate outputs. Batch and stream processors are the tools for achieving this
goal.
The outputs of batch and stream processes are derived datasets such as search
indexes, materialized views, recommendations to show to users, aggregate metrics,
and so on (see “The Output of Batch Workflows” on page 411 and “Uses of Stream
Processing” on page 465).
As we saw in Chapter 10 and Chapter 11, batch and stream processing have a lot of
principles in common, and the main fundamental difference is that stream process‐
ors operate on unbounded datasets whereas batch process inputs are of a known,
finite size. There are also many detailed differences in the ways the processing
engines are implemented, but these distinctions are beginning to blur.
Spark performs stream processing on top of a batch processing engine by breaking
the stream into microbatches, whereas Apache Flink performs batch processing on
top of a stream processing engine [5]. In principle, one type of processing can be
emulated on top of the other, although the performance characteristics vary: for
example, microbatching may perform poorly on hopping or sliding windows [6].
Maintaining derived state
Batch processing has a quite strong functional flavor (even if the code is not written
in a functional programming language): it encourages deterministic, pure functions
whose output depends only on the input and which have no side effects other than
the explicit outputs, treating inputs as immutable and outputs as append-only.
Stream processing is similar, but it extends operators to allow managed, fault-tolerant
state (see “Rebuilding state after a failure” on page 478).
The principle of deterministic functions with well-defined inputs and outputs is not
only good for fault tolerance (see “Idempotence” on page 478), but also simplifies
reasoning about the dataflows in an organization [7]. No matter whether the derived
data is a search index, a statistical model, or a cache, it is helpful to think in terms of
data pipelines that derive one thing from another, pushing state changes in one sys‐
tem through functional application code and applying the effects to derived systems.
In principle, derived data systems could be maintained synchronously, just like a
relational database updates secondary indexes synchronously within the same trans‐
action as writes to the table being indexed. However, asynchrony is what makes sys‐
tems based on event logs robust: it allows a fault in one part of the system to be
contained locally, whereas distributed transactions abort if any one participant fails,
so they tend to amplify failures by spreading them to the rest of the system (see “Lim‐
itations of distributed transactions” on page 363).
We saw in “Partitioning and Secondary Indexes” on page 206 that secondary indexes
often cross partition boundaries. A partitioned system with secondary indexes either
Data Integration 
| 
495


needs to send writes to multiple partitions (if the index is term-partitioned) or send
reads to all partitions (if the index is document-partitioned). Such cross-partition
communication is also most reliable and scalable if the index is maintained asynchro‐
nously [8] (see also “Multi-partition data processing” on page 514).
Reprocessing data for application evolution
When maintaining derived data, batch and stream processing are both useful. Stream
processing allows changes in the input to be reflected in derived views with low delay,
whereas batch processing allows large amounts of accumulated historical data to be
reprocessed in order to derive new views onto an existing dataset.
In particular, reprocessing existing data provides a good mechanism for maintaining
a system, evolving it to support new features and changed requirements (see Chap‐
ter 4). Without reprocessing, schema evolution is limited to simple changes like
adding a new optional field to a record, or adding a new type of record. This is the
case both in a schema-on-write and in a schema-on-read context (see “Schema flexi‐
bility in the document model” on page 39). On the other hand, with reprocessing it is
possible to restructure a dataset into a completely different model in order to better
serve new requirements.
Schema Migrations on Railways
Large-scale “schema migrations” occur in noncomputer systems as well. For example,
in the early days of railway building in 19th-century England there were various com‐
peting standards for the gauge (the distance between the two rails). Trains built for
one gauge couldn’t run on tracks of another gauge, which restricted the possible
interconnections in the train network [9].
After a single standard gauge was finally decided upon in 1846, tracks with other
gauges had to be converted—but how do you do this without shutting down the train
line for months or years? The solution is to first convert the track to dual gauge or
mixed gauge by adding a third rail. This conversion can be done gradually, and when
it is done, trains of both gauges can run on the line, using two of the three rails. Even‐
tually, once all trains have been converted to the standard gauge, the rail providing
the nonstandard gauge can be removed.
“Reprocessing” the existing tracks in this way, and allowing the old and new versions
to exist side by side, makes it possible to change the gauge gradually over the course
of years. Nevertheless, it is an expensive undertaking, which is why nonstandard
gauges still exist today. For example, the BART system in the San Francisco Bay Area
uses a different gauge from the majority of the US.
496 
| 
Chapter 12: The Future of Data Systems


Derived views allow gradual evolution. If you want to restructure a dataset, you do
not need to perform the migration as a sudden switch. Instead, you can maintain the
old schema and the new schema side by side as two independently derived views onto
the same underlying data. You can then start shifting a small number of users to the
new view in order to test its performance and find any bugs, while most users con‐
tinue to be routed to the old view. Gradually, you can increase the proportion of
users accessing the new view, and eventually you can drop the old view [10].
The beauty of such a gradual migration is that every stage of the process is easily
reversible if something goes wrong: you always have a working system to go back to.
By reducing the risk of irreversible damage, you can be more confident about going
ahead, and thus move faster to improve your system [11].
The lambda architecture
If batch processing is used to reprocess historical data, and stream processing is used
to process recent updates, then how do you combine the two? The lambda architec‐
ture [12] is a proposal in this area that has gained a lot of attention.
The core idea of the lambda architecture is that incoming data should be recorded by
appending immutable events to an always-growing dataset, similarly to event sourc‐
ing (see “Event Sourcing” on page 457). From these events, read-optimized views are
derived. The lambda architecture proposes running two different systems in parallel:
a batch processing system such as Hadoop MapReduce, and a separate streamprocessing system such as Storm.
In the lambda approach, the stream processor consumes the events and quickly pro‐
duces an approximate update to the view; the batch processor later consumes the
same set of events and produces a corrected version of the derived view. The reason‐
ing behind this design is that batch processing is simpler and thus less prone to bugs,
while stream processors are thought to be less reliable and harder to make faulttolerant (see “Fault Tolerance” on page 476). Moreover, the stream process can use
fast approximate algorithms while the batch process uses slower exact algorithms.
The lambda architecture was an influential idea that shaped the design of data sys‐
tems for the better, particularly by popularizing the principle of deriving views onto
streams of immutable events and reprocessing events when needed. However, I also
think that it has a number of practical problems:
• Having to maintain the same logic to run both in a batch and in a stream pro‐
cessing framework is significant additional effort. Although libraries such as
Summingbird [13] provide an abstraction for computations that can be run in
either a batch or a streaming context, the operational complexity of debugging,
tuning, and maintaining two different systems remains [14].
Data Integration 
| 
497


• Since the stream pipeline and the batch pipeline produce separate outputs, they
need to be merged in order to respond to user requests. This merge is fairly easy
if the computation is a simple aggregation over a tumbling window, but it
becomes significantly harder if the view is derived using more complex opera‐
tions such as joins and sessionization, or if the output is not a time series.
• Although it is great to have the ability to reprocess the entire historical dataset,
doing so frequently is expensive on large datasets. Thus, the batch pipeline often
needs to be set up to process incremental batches (e.g., an hour’s worth of data at
the end of every hour) rather than reprocessing everything. This raises the prob‐
lems discussed in “Reasoning About Time” on page 468, such as handling strag‐
glers and handling windows that cross boundaries between batches.
Incrementalizing a batch computation adds complexity, making it more akin to
the streaming layer, which runs counter to the goal of keeping the batch layer as
simple as possible.
Unifying batch and stream processing
More recent work has enabled the benefits of the lambda architecture to be enjoyed
without its downsides, by allowing both batch computations (reprocessing historical
data) and stream computations (processing events as they arrive) to be implemented
in the same system [15].
Unifying batch and stream processing in one system requires the following features,
which are becoming increasingly widely available:
• The ability to replay historical events through the same processing engine that
handles the stream of recent events. For example, log-based message brokers
have the ability to replay messages (see “Replaying old messages” on page 451),
and some stream processors can read input from a distributed filesystem like
HDFS.
• Exactly-once semantics for stream processors—that is, ensuring that the output
is the same as if no faults had occurred, even if faults did in fact occur (see “Fault
Tolerance” on page 476). Like with batch processing, this requires discarding the
partial output of any failed tasks.
• Tools for windowing by event time, not by processing time, since processing
time is meaningless when reprocessing historical events (see “Reasoning About
Time” on page 468). For example, Apache Beam provides an API for expressing
such computations, which can then be run using Apache Flink or Google Cloud
Dataflow. 
498 
| 
Chapter 12: The Future of Data Systems


Unbundling Databases
At a most abstract level, databases, Hadoop, and operating systems all perform the
same functions: they store some data, and they allow you to process and query that
data [16]. A database stores data in records of some data model (rows in tables, docu‐
ments, vertices in a graph, etc.) while an operating system’s filesystem stores data in
files—but at their core, both are “information management” systems [17]. As we saw
in Chapter 10, the Hadoop ecosystem is somewhat like a distributed version of Unix.
Of course, there are many practical differences. For example, many filesystems do not
cope very well with a directory containing 10 million small files, whereas a database
containing 10 million small records is completely normal and unremarkable. Never‐
theless, the similarities and differences between operating systems and databases are
worth exploring.
Unix and relational databases have approached the information management prob‐
lem with very different philosophies. Unix viewed its purpose as presenting program‐
mers with a logical but fairly low-level hardware abstraction, whereas relational
databases wanted to give application programmers a high-level abstraction that
would hide the complexities of data structures on disk, concurrency, crash recovery,
and so on. Unix developed pipes and files that are just sequences of bytes, whereas
databases developed SQL and transactions.
Which approach is better? Of course, it depends what you want. Unix is “simpler” in
the sense that it is a fairly thin wrapper around hardware resources; relational data‐
bases are “simpler” in the sense that a short declarative query can draw on a lot of
powerful infrastructure (query optimization, indexes, join methods, concurrency
control, replication, etc.) without the author of the query needing to understand the
implementation details.
The tension between these philosophies has lasted for decades (both Unix and the
relational model emerged in the early 1970s) and still isn’t resolved. For example, I
would interpret the NoSQL movement as wanting to apply a Unix-esque approach of
low-level abstractions to the domain of distributed OLTP data storage.
In this section I will attempt to reconcile the two philosophies, in the hope that we
can combine the best of both worlds.
Composing Data Storage Technologies
Over the course of this book we have discussed various features provided by data‐
bases and how they work, including:
• Secondary indexes, which allow you to efficiently search for records based on the
value of a field (see “Other Indexing Structures” on page 85)
Unbundling Databases 
| 
499


• Materialized views, which are a kind of precomputed cache of query results (see
“Aggregation: Data Cubes and Materialized Views” on page 101)
• Replication logs, which keep copies of the data on other nodes up to date (see
“Implementation of Replication Logs” on page 158)
• Full-text search indexes, which allow keyword search in text (see “Full-text
search and fuzzy indexes” on page 88) and which are built into some relational
databases [1]
In Chapters 10 and 11, similar themes emerged. We talked about building full-text
search indexes (see “The Output of Batch Workflows” on page 411), about material‐
ized view maintenance (see “Maintaining materialized views” on page 467), and
about replicating changes from a database to derived data systems (see “Change Data
Capture” on page 454).
It seems that there are parallels between the features that are built into databases and
the derived data systems that people are building with batch and stream processors.
Creating an index
Think about what happens when you run CREATE INDEX to create a new index in a
relational database. The database has to scan over a consistent snapshot of a table,
pick out all of the field values being indexed, sort them, and write out the index. Then
it must process the backlog of writes that have been made since the consistent snap‐
shot was taken (assuming the table was not locked while creating the index, so writes
could continue). Once that is done, the database must continue to keep the index up
to date whenever a transaction writes to the table.
This process is remarkably similar to setting up a new follower replica (see “Setting
Up New Followers” on page 155), and also very similar to bootstrapping change data
capture in a streaming system (see “Initial snapshot” on page 455).
Whenever you run CREATE INDEX, the database essentially reprocesses the existing
dataset (as discussed in “Reprocessing data for application evolution” on page 496)
and derives the index as a new view onto the existing data. The existing data may be a
snapshot of the state rather than a log of all changes that ever happened, but the two
are closely related (see “State, Streams, and Immutability” on page 459).
The meta-database of everything
In this light, I think that the dataflow across an entire organization starts looking like
one huge database [7]. Whenever a batch, stream, or ETL process transports data
from one place and form to another place and form, it is acting like the database sub‐
system that keeps indexes or materialized views up to date.
500 
| 
Chapter 12: The Future of Data Systems


Viewed like this, batch and stream processors are like elaborate implementations of
triggers, stored procedures, and materialized view maintenance routines. The derived
data systems they maintain are like different index types. For example, a relational
database may support B-tree indexes, hash indexes, spatial indexes (see “Multicolumn indexes” on page 87), and other types of indexes. In the emerging architec‐
ture of derived data systems, instead of implementing those facilities as features of a
single integrated database product, they are provided by various different pieces of
software, running on different machines, administered by different teams.
Where will these developments take us in the future? If we start from the premise
that there is no single data model or storage format that is suitable for all access pat‐
terns, I speculate that there are two avenues by which different storage and process‐
ing tools can nevertheless be composed into a cohesive system:
Federated databases: unifying reads
It is possible to provide a unified query interface to a wide variety of underlying
storage engines and processing methods—an approach known as a federated
database or polystore [18, 19]. For example, PostgreSQL’s foreign data wrapper
feature fits this pattern [20]. Applications that need a specialized data model or
query interface can still access the underlying storage engines directly, while
users who want to combine data from disparate places can do so easily through
the federated interface.
A federated query interface follows the relational tradition of a single integrated
system with a high-level query language and elegant semantics, but a compli‐
cated implementation.
Unbundled databases: unifying writes
While federation addresses read-only querying across several different systems, it
does not have a good answer to synchronizing writes across those systems. We
said that within a single database, creating a consistent index is a built-in feature.
When we compose several storage systems, we similarly need to ensure that all
data changes end up in all the right places, even in the face of faults. Making it
easier to reliably plug together storage systems (e.g., through change data capture
and event logs) is like unbundling a database’s index-maintenance features in a
way that can synchronize writes across disparate technologies [7, 21].
The unbundled approach follows the Unix tradition of small tools that do one
thing well [22], that communicate through a uniform low-level API (pipes), and
that can be composed using a higher-level language (the shell) [16].
Making unbundling work
Federation and unbundling are two sides of the same coin: composing a reliable, scal‐
able, and maintainable system out of diverse components. Federated read-only
Unbundling Databases 
| 
501


querying requires mapping one data model into another, which takes some thought
but is ultimately quite a manageable problem. I think that keeping the writes to sev‐
eral storage systems in sync is the harder engineering problem, and so I will focus
on it.
The traditional approach to synchronizing writes requires distributed transactions
across heterogeneous storage systems [18], which I think is the wrong solution (see
“Derived data versus distributed transactions” on page 492). Transactions within a
single storage or stream processing system are feasible, but when data crosses the
boundary between different technologies, I believe that an asynchronous event log
with idempotent writes is a much more robust and practical approach.
For example, distributed transactions are used within some stream processors to ach‐
ieve exactly-once semantics (see “Atomic commit revisited” on page 477), and this
can work quite well. However, when a transaction would need to involve systems
written by different groups of people (e.g., when data is written from a stream pro‐
cessor to a distributed key-value store or search index), the lack of a standardized
transaction protocol makes integration much harder. An ordered log of events with
idempotent consumers (see “Idempotence” on page 478) is a much simpler abstrac‐
tion, and thus much more feasible to implement across heterogeneous systems [7].
The big advantage of log-based integration is loose coupling between the various com‐
ponents, which manifests itself in two ways:
1. At a system level, asynchronous event streams make the system as a whole more
robust to outages or performance degradation of individual components. If a
consumer runs slow or fails, the event log can buffer messages (see “Disk space
usage” on page 450), allowing the producer and any other consumers to continue
running unaffected. The faulty consumer can catch up when it is fixed, so it
doesn’t miss any data, and the fault is contained. By contrast, the synchronous
interaction of distributed transactions tends to escalate local faults into largescale failures (see “Limitations of distributed transactions” on page 363).
2. At a human level, unbundling data systems allows different software components
and services to be developed, improved, and maintained independently from
each other by different teams. Specialization allows each team to focus on doing
one thing well, with well-defined interfaces to other teams’ systems. Event logs
provide an interface that is powerful enough to capture fairly strong consistency
properties (due to durability and ordering of events), but also general enough to
be applicable to almost any kind of data.
Unbundled versus integrated systems
If unbundling does indeed become the way of the future, it will not replace databases
in their current form—they will still be needed as much as ever. Databases are still
502 
| 
Chapter 12: The Future of Data Systems


required for maintaining state in stream processors, and in order to serve queries for
the output of batch and stream processors (see “The Output of Batch Workflows” on
page 411 and “Processing Streams” on page 464). Specialized query engines will con‐
tinue to be important for particular workloads: for example, query engines in MPP
data warehouses are optimized for exploratory analytic queries and handle this kind
of workload very well (see “Comparing Hadoop to Distributed Databases” on page
414).
The complexity of running several different pieces of infrastructure can be a problem:
each piece of software has a learning curve, configuration issues, and operational
quirks, and so it is worth deploying as few moving parts as possible. A single integra‐
ted software product may also be able to achieve better and more predictable perfor‐
mance on the kinds of workloads for which it is designed, compared to a system
consisting of several tools that you have composed with application code [23]. As I
said in the Preface, building for scale that you don’t need is wasted effort and may
lock you into an inflexible design. In effect, it is a form of premature optimization.
The goal of unbundling is not to compete with individual databases on performance
for particular workloads; the goal is to allow you to combine several different data‐
bases in order to achieve good performance for a much wider range of workloads
than is possible with a single piece of software. It’s about breadth, not depth—in the
same vein as the diversity of storage and processing models that we discussed in
“Comparing Hadoop to Distributed Databases” on page 414.
Thus, if there is a single technology that does everything you need, you’re most likely
best off simply using that product rather than trying to reimplement it yourself from
lower-level components. The advantages of unbundling and composition only come
into the picture when there is no single piece of software that satisfies all your
requirements.
What’s missing?
The tools for composing data systems are getting better, but I think one major part is
missing: we don’t yet have the unbundled-database equivalent of the Unix shell (i.e., a
high-level language for composing storage and processing systems in a simple and
declarative way).
For example, I would love it if we could simply declare mysql | elasticsearch, by
analogy to Unix pipes [22], which would be the unbundled equivalent of CREATE
INDEX: it would take all the documents in a MySQL database and index them in an
Elasticsearch cluster. It would then continually capture all the changes made to the
database and automatically apply them to the search index, without us having to
write custom application code. This kind of integration should be possible with
almost any kind of storage or indexing system.
Unbundling Databases 
| 
503


Similarly, it would be great to be able to precompute and update caches more easily.
Recall that a materialized view is essentially a precomputed cache, so you could imag‐
ine creating a cache by declaratively specifying materialized views for complex quer‐
ies, including recursive queries on graphs (see “Graph-Like Data Models” on page
49) and application logic. There is interesting early-stage research in this area, such as
differential dataflow [24, 25], and I hope that these ideas will find their way into pro‐
duction systems. 
Designing Applications Around Dataflow
The approach of unbundling databases by composing specialized storage and pro‐
cessing systems with application code is also becoming known as the “database
inside-out” approach [26], after the title of a conference talk I gave in 2014 [27].
However, calling it a “new architecture” is too grandiose. I see it more as a design
pattern, a starting point for discussion, and we give it a name simply so that we can
better talk about it.
These ideas are not mine; they are simply an amalgamation of other people’s ideas
from which I think we should learn. In particular, there is a lot of overlap with data‐
flow languages such as Oz [28] and Juttle [29], functional reactive programming (FRP)
languages such as Elm [30, 31], and logic programming languages such as Bloom [32].
The term unbundling in this context was proposed by Jay Kreps [7].
Even spreadsheets have dataflow programming capabilities that are miles ahead of
most mainstream programming languages [33]. In a spreadsheet, you can put a for‐
mula in one cell (for example, the sum of cells in another column), and whenever any
input to the formula changes, the result of the formula is automatically recalculated.
This is exactly what we want at a data system level: when a record in a database
changes, we want any index for that record to be automatically updated, and any
cached views or aggregations that depend on the record to be automatically
refreshed. You should not have to worry about the technical details of how this
refresh happens, but be able to simply trust that it works correctly.
Thus, I think that most data systems still have something to learn from the features
that VisiCalc already had in 1979 [34]. The difference from spreadsheets is that
today’s data systems need to be fault-tolerant, scalable, and store data durably. They
also need to be able to integrate disparate technologies written by different groups of
people over time, and reuse existing libraries and services: it is unrealistic to expect all
software to be developed using one particular language, framework, or tool.
In this section I will expand on these ideas and explore some ways of building appli‐
cations around the ideas of unbundled databases and dataflow.
504 
| 
Chapter 12: The Future of Data Systems


Application code as a derivation function
When one dataset is derived from another, it goes through some kind of transforma‐
tion function. For example:
• A secondary index is a kind of derived dataset with a straightforward transforma‐
tion function: for each row or document in the base table, it picks out the values
in the columns or fields being indexed, and sorts by those values (assuming a B-
tree or SSTable index, which are sorted by key, as discussed in Chapter 3).
• A full-text search index is created by applying various natural language process‐
ing functions such as language detection, word segmentation, stemming or lem‐
matization, spelling correction, and synonym identification, followed by building
a data structure for efficient lookups (such as an inverted index).
• In a machine learning system, we can consider the model as being derived from
the training data by applying various feature extraction and statistical analysis
functions. When the model is applied to new input data, the output of the model
is derived from the input and the model (and hence, indirectly, from the training
data).
• A cache often contains an aggregation of data in the form in which it is going to
be displayed in a user interface (UI). Populating the cache thus requires knowl‐
edge of what fields are referenced in the UI; changes in the UI may require
updating the definition of how the cache is populated and rebuilding the cache.
The derivation function for a secondary index is so commonly required that it is built
into many databases as a core feature, and you can invoke it by merely saying CREATE
INDEX. For full-text indexing, basic linguistic features for common languages may be
built into a database, but the more sophisticated features often require domainspecific tuning. In machine learning, feature engineering is notoriously applicationspecific, and often has to incorporate detailed knowledge about the user interaction
and deployment of an application [35].
When the function that creates a derived dataset is not a standard cookie-cutter func‐
tion like creating a secondary index, custom code is required to handle the
application-specific aspects. And this custom code is where many databases struggle.
Although relational databases commonly support triggers, stored procedures, and
user-defined functions, which can be used to execute application code within the
database, they have been somewhat of an afterthought in database design (see
“Transmitting Event Streams” on page 440).
Separation of application code and state
In theory, databases could be deployment environments for arbitrary application
code, like an operating system. However, in practice they have turned out to be
Unbundling Databases 
| 
505


i. Explaining a joke rarely improves it, but I don’t want anyone to feel left out. Here, Church is a reference to
the mathematician Alonzo Church, who created the lambda calculus, an early form of computation that is the
basis for most functional programming languages. The lambda calculus has no mutable state (i.e., no vari‐
ables that can be overwritten), so one could say that mutable state is separate from Church’s work.
poorly suited for this purpose. They do not fit well with the requirements of modern
application development, such as dependency and package management, version
control, rolling upgrades, evolvability, monitoring, metrics, calls to network services,
and integration with external systems.
On the other hand, deployment and cluster management tools such as Mesos, YARN,
Docker, Kubernetes, and others are designed specifically for the purpose of running
application code. By focusing on doing one thing well, they are able to do it much
better than a database that provides execution of user-defined functions as one of its
many features.
I think it makes sense to have some parts of a system that specialize in durable data
storage, and other parts that specialize in running application code. The two can
interact while still remaining independent.
Most web applications today are deployed as stateless services, in which any user
request can be routed to any application server, and the server forgets everything
about the request once it has sent the response. This style of deployment is conve‐
nient, as servers can be added or removed at will, but the state has to go somewhere:
typically, a database. The trend has been to keep stateless application logic separate
from state management (databases): not putting application logic in the database and
not putting persistent state in the application [36]. As people in the functional pro‐
gramming community like to joke, “We believe in the separation of Church and
state” [37].i
In this typical web application model, the database acts as a kind of mutable shared
variable that can be accessed synchronously over the network. The application can
read and update the variable, and the database takes care of making it durable, pro‐
viding some concurrency control and fault tolerance.
However, in most programming languages you cannot subscribe to changes in a
mutable variable—you can only read it periodically. Unlike in a spreadsheet, readers
of the variable don’t get notified if the value of the variable changes. (You can imple‐
ment such notifications in your own code—this is known as the observer pattern—
but most languages do not have this pattern as a built-in feature.)
Databases have inherited this passive approach to mutable data: if you want to find
out whether the content of the database has changed, often your only option is to poll
(i.e., to repeat your query periodically). Subscribing to changes is only just beginning
to emerge as a feature (see “API support for change streams” on page 456).
506 
| 
Chapter 12: The Future of Data Systems


Dataflow: Interplay between state changes and application code
Thinking about applications in terms of dataflow implies renegotiating the relation‐
ship between application code and state management. Instead of treating a database
as a passive variable that is manipulated by the application, we think much more
about the interplay and collaboration between state, state changes, and code that pro‐
cesses them. Application code responds to state changes in one place by triggering
state changes in another place.
We saw this line of thinking in “Databases and Streams” on page 451, where we dis‐
cussed treating the log of changes to a database as a stream of events that we can sub‐
scribe to. Message-passing systems such as actors (see “Message-Passing Dataflow”
on page 136) also have this concept of responding to events. Already in the 1980s, the
tuple spaces model explored expressing distributed computations in terms of pro‐
cesses that observe state changes and react to them [38, 39].
As discussed, similar things happen inside a database when a trigger fires due to a
data change, or when a secondary index is updated to reflect a change in the table
being indexed. Unbundling the database means taking this idea and applying it to the
creation of derived datasets outside of the primary database: caches, full-text search
indexes, machine learning, or analytics systems. We can use stream processing and
messaging systems for this purpose.
The important thing to keep in mind is that maintaining derived data is not the same
as asynchronous job execution, for which messaging systems are traditionally
designed (see “Logs compared to traditional messaging” on page 448):
• When maintaining derived data, the order of state changes is often important (if
several views are derived from an event log, they need to process the events in the
same order so that they remain consistent with each other). As discussed in
“Acknowledgments and redelivery” on page 445, many message brokers do not
have this property when redelivering unacknowledged messages. Dual writes are
also ruled out (see “Keeping Systems in Sync” on page 452).
• Fault tolerance is key for derived data: losing just a single message causes the
derived dataset to go permanently out of sync with its data source. Both message
delivery and derived state updates must be reliable. For example, many actor sys‐
tems by default maintain actor state and messages in memory, so they are lost if
the machine running the actor crashes.
Stable message ordering and fault-tolerant message processing are quite stringent
demands, but they are much less expensive and more operationally robust than dis‐
tributed transactions. Modern stream processors can provide these ordering and reli‐
ability guarantees at scale, and they allow application code to be run as stream
operators.
Unbundling Databases 
| 
507


ii. In the microservices approach, you could avoid the synchronous network request by caching the exchange
rate locally in the service that processes the purchase. However, in order to keep that cache fresh, you would
need to periodically poll for updated exchange rates, or subscribe to a stream of changes—which is exactly
what happens in the dataflow approach.
This application code can do the arbitrary processing that built-in derivation func‐
tions in databases generally don’t provide. Like Unix tools chained by pipes, stream
operators can be composed to build large systems around dataflow. Each operator
takes streams of state changes as input, and produces other streams of state changes
as output.
Stream processors and services
The currently trendy style of application development involves breaking down func‐
tionality into a set of services that communicate via synchronous network requests
such as REST APIs (see “Dataflow Through Services: REST and RPC” on page 131).
The advantage of such a service-oriented architecture over a single monolithic appli‐
cation is primarily organizational scalability through loose coupling: different teams
can work on different services, which reduces coordination effort between teams (as
long as the services can be deployed and updated independently).
Composing stream operators into dataflow systems has a lot of similar characteristics
to the microservices approach [40]. However, the underlying communication mecha‐
nism is very different: one-directional, asynchronous message streams rather than
synchronous request/response interactions.
Besides the advantages listed in “Message-Passing Dataflow” on page 136, such as
better fault tolerance, dataflow systems can also achieve better performance. For
example, say a customer is purchasing an item that is priced in one currency but paid
for in another currency. In order to perform the currency conversion, you need to
know the current exchange rate. This operation could be implemented in two ways
[40, 41]:
1. In the microservices approach, the code that processes the purchase would prob‐
ably query an exchange-rate service or database in order to obtain the current
rate for a particular currency.
2. In the dataflow approach, the code that processes purchases would subscribe to a
stream of exchange rate updates ahead of time, and record the current rate in a
local database whenever it changes. When it comes to processing the purchase, it
only needs to query the local database.
The second approach has replaced a synchronous network request to another service
with a query to a local database (which may be on the same machine, even in the
same process).ii Not only is the dataflow approach faster, but it is also more robust to
508 
| 
Chapter 12: The Future of Data Systems


the failure of another service. The fastest and most reliable network request is no net‐
work request at all! Instead of RPC, we now have a stream join between purchase
events and exchange rate update events (see “Stream-table join (stream enrichment)”
on page 473).
The join is time-dependent: if the purchase events are reprocessed at a later point in
time, the exchange rate will have changed. If you want to reconstruct the original out‐
put, you will need to obtain the historical exchange rate at the original time of pur‐
chase. No matter whether you query a service or subscribe to a stream of exchange
rate updates, you will need to handle this time dependence (see “Time-dependence of
joins” on page 475).
Subscribing to a stream of changes, rather than querying the current state when
needed, brings us closer to a spreadsheet-like model of computation: when some
piece of data changes, any derived data that depends on it can swiftly be updated.
There are still many open questions, for example around issues like time-dependent
joins, but I believe that building applications around dataflow ideas is a very promis‐
ing direction to go in. 
Observing Derived State
At an abstract level, the dataflow systems discussed in the last section give you a pro‐
cess for creating derived datasets (such as search indexes, materialized views, and
predictive models) and keeping them up to date. Let’s call that process the write path:
whenever some piece of information is written to the system, it may go through mul‐
tiple stages of batch and stream processing, and eventually every derived dataset is
updated to incorporate the data that was written. Figure 12-1 shows an example of
updating a search index.
Figure 12-1. In a search index, writes (document updates) meet reads (queries).
But why do you create the derived dataset in the first place? Most likely because you
want to query it again at a later time. This is the read path: when serving a user
Unbundling Databases 
| 
509


iii. Less facetiously, the set of distinct search queries with nonempty search results is finite, assuming a finite
corpus. However, it would be exponential in the number of terms in the corpus, which is still pretty bad news.
request you read from the derived dataset, perhaps perform some more processing
on the results, and construct the response to the user.
Taken together, the write path and the read path encompass the whole journey of the
data, from the point where it is collected to the point where it is consumed (probably
by another human). The write path is the portion of the journey that is precomputed
—i.e., that is done eagerly as soon as the data comes in, regardless of whether anyone
has asked to see it. The read path is the portion of the journey that only happens
when someone asks for it. If you are familiar with functional programming lan‐
guages, you might notice that the write path is similar to eager evaluation, and the
read path is similar to lazy evaluation.
The derived dataset is the place where the write path and the read path meet, as illus‐
trated in Figure 12-1. It represents a trade-off between the amount of work that needs
to be done at write time and the amount that needs to be done at read time.
Materialized views and caching
A full-text search index is a good example: the write path updates the index, and the
read path searches the index for keywords. Both reads and writes need to do some
work. Writes need to update the index entries for all terms that appear in the docu‐
ment. Reads need to search for each of the words in the query, and apply Boolean
logic to find documents that contain all of the words in the query (an AND operator),
or any synonym of each of the words (an OR operator).
If you didn’t have an index, a search query would have to scan over all documents
(like grep), which would get very expensive if you had a large number of documents.
No index means less work on the write path (no index to update), but a lot more
work on the read path.
On the other hand, you could imagine precomputing the search results for all possi‐
ble queries. In that case, you would have less work to do on the read path: no Boolean
logic, just find the results for your query and return them. However, the write path
would be a lot more expensive: the set of possible search queries that could be asked
is infinite, and thus precomputing all possible search results would require infinite
time and storage space. That wouldn’t work so well.iii
Another option would be to precompute the search results for only a fixed set of the
most common queries, so that they can be served quickly without having to go to the
index. The uncommon queries can still be served from the index. This would gener‐
ally be called a cache of common queries, although we could also call it a materialized
510 
| 
Chapter 12: The Future of Data Systems


view, as it would need to be updated when new documents appear that should be
included in the results of one of the common queries.
From this example we can see that an index is not the only possible boundary
between the write path and the read path. Caching of common search results is possi‐
ble, and grep-like scanning without the index is also possible on a small number of
documents. Viewed like this, the role of caches, indexes, and materialized views is
simple: they shift the boundary between the read path and the write path. They allow
us to do more work on the write path, by precomputing results, in order to save effort
on the read path.
Shifting the boundary between work done on the write path and the read path was in
fact the topic of the Twitter example at the beginning of this book, in “Describing
Load” on page 11. In that example, we also saw how the boundary between write path
and read path might be drawn differently for celebrities compared to ordinary users.
After 500 pages we have come full circle!
Stateful, offline-capable clients
I find the idea of a boundary between write and read paths interesting because we can
discuss shifting that boundary and explore what that shift means in practical terms.
Let’s look at the idea in a different context.
The huge popularity of web applications in the last two decades has led us to certain
assumptions about application development that are easy to take for granted. In par‐
ticular, the client/server model—in which clients are largely stateless and servers have
the authority over data—is so common that we almost forget that anything else
exists. However, technology keeps moving on, and I think it is important to question
the status quo from time to time.
Traditionally, web browsers have been stateless clients that can only do useful things
when you have an internet connection (just about the only thing you could do offline
was to scroll up and down in a page that you had previously loaded while online).
However, recent “single-page” JavaScript web apps have gained a lot of stateful capa‐
bilities, including client-side user interface interaction and persistent local storage in
the web browser. Mobile apps can similarly store a lot of state on the device and don’t
require a round-trip to the server for most user interactions.
These changing capabilities have led to a renewed interest in offline-first applications
that do as much as possible using a local database on the same device, without requir‐
ing an internet connection, and sync with remote servers in the background when a
network connection is available [42]. Since mobile devices often have slow and unre‐
liable cellular internet connections, it’s a big advantage for users if their user interface
does not have to wait for synchronous network requests, and if apps mostly work off‐
line (see “Clients with offline operation” on page 170).
Unbundling Databases 
| 
511


When we move away from the assumption of stateless clients talking to a central
database and toward state that is maintained on end-user devices, a world of new
opportunities opens up. In particular, we can think of the on-device state as a cache of
state on the server. The pixels on the screen are a materialized view onto model
objects in the client app; the model objects are a local replica of state in a remote
datacenter [27].
Pushing state changes to clients
In a typical web page, if you load the page in a web browser and the data subse‐
quently changes on the server, the browser does not find out about the change until
you reload the page. The browser only reads the data at one point in time, assuming
that it is static—it does not subscribe to updates from the server. Thus, the state on
the device is a stale cache that is not updated unless you explicitly poll for changes.
(HTTP-based feed subscription protocols like RSS are really just a basic form of poll‐
ing.)
More recent protocols have moved beyond the basic request/response pattern of
HTTP: server-sent events (the EventSource API) and WebSockets provide communi‐
cation channels by which a web browser can keep an open TCP connection to a
server, and the server can actively push messages to the browser as long as it remains
connected. This provides an opportunity for the server to actively inform the enduser client about any changes to the state it has stored locally, reducing the staleness
of the client-side state.
In terms of our model of write path and read path, actively pushing state changes all
the way to client devices means extending the write path all the way to the end user.
When a client is first initialized, it would still need to use a read path to get its initial
state, but thereafter it could rely on a stream of state changes sent by the server. The
ideas we discussed around stream processing and messaging are not restricted to run‐
ning only in a datacenter: we can take the ideas further, and extend them all the way
to end-user devices [43].
The devices will be offline some of the time, and unable to receive any notifications of
state changes from the server during that time. But we already solved that problem: in
“Consumer offsets” on page 449 we discussed how a consumer of a log-based mes‐
sage broker can reconnect after failing or becoming disconnected, and ensure that it
doesn’t miss any messages that arrived while it was disconnected. The same techni‐
que works for individual users, where each device is a small subscriber to a small
stream of events.
End-to-end event streams
Recent tools for developing stateful clients and user interfaces, such as the Elm lan‐
guage [30] and Facebook’s toolchain of React, Flux, and Redux [44], already manage
512 
| 
Chapter 12: The Future of Data Systems


internal client-side state by subscribing to a stream of events representing user input
or responses from a server, structured similarly to event sourcing (see “Event Sourc‐
ing” on page 457).
It would be very natural to extend this programming model to also allow a server to
push state-change events into this client-side event pipeline. Thus, state changes
could flow through an end-to-end write path: from the interaction on one device that
triggers a state change, via event logs and through several derived data systems and
stream processors, all the way to the user interface of a person observing the state on
another device. These state changes could be propagated with fairly low delay—say,
under one second end to end.
Some applications, such as instant messaging and online games, already have such a
“real-time” architecture (in the sense of interactions with low delay, not in the sense
of “Response time guarantees” on page 298). But why don’t we build all applications
this way?
The challenge is that the assumption of stateless clients and request/response interac‐
tions is very deeply ingrained in our databases, libraries, frameworks, and protocols.
Many datastores support read and write operations where a request returns one
response, but much fewer provide an ability to subscribe to changes—i.e., a request
that returns a stream of responses over time (see “API support for change streams”
on page 456).
In order to extend the write path all the way to the end user, we would need to funda‐
mentally rethink the way we build many of these systems: moving away from request/
response interaction and toward publish/subscribe dataflow [27]. I think that the
advantages of more responsive user interfaces and better offline support would make
it worth the effort. If you are designing data systems, I hope that you will keep in
mind the option of subscribing to changes, not just querying the current state.
Reads are events too
We discussed that when a stream processor writes derived data to a store (database,
cache, or index), and when user requests query that store, the store acts as the bound‐
ary between the write path and the read path. The store allows random-access read
queries to the data that would otherwise require scanning the whole event log.
In many cases, the data storage is separate from the streaming system. But recall that
stream processors also need to maintain state to perform aggregations and joins (see
“Stream Joins” on page 472). This state is normally hidden inside the stream pro‐
cessor, but some frameworks allow it to also be queried by outside clients [45], turn‐
ing the stream processor itself into a kind of simple database.
I would like to take that idea further. As discussed so far, the writes to the store go
through an event log, while reads are transient network requests that go directly to
Unbundling Databases 
| 
513


the nodes that store the data being queried. This is a reasonable design, but not the
only possible one. It is also possible to represent read requests as streams of events,
and send both the read events and the write events through a stream processor; the
processor responds to read events by emitting the result of the read to an output
stream [46].
When both the writes and the reads are represented as events, and routed to the same
stream operator in order to be handled, we are in fact performing a stream-table join
between the stream of read queries and the database. The read event needs to be sent
to the database partition holding the data (see “Request Routing” on page 214), just
like batch and stream processors need to copartition inputs on the same key when
joining (see “Reduce-Side Joins and Grouping” on page 403).
This correspondence between serving requests and performing joins is quite funda‐
mental [47]. A one-off read request just passes the request through the join operator
and then immediately forgets it; a subscribe request is a persistent join with past and
future events on the other side of the join.
Recording a log of read events potentially also has benefits with regard to tracking
causal dependencies and data provenance across a system: it would allow you to
reconstruct what the user saw before they made a particular decision. For example, in
an online shop, it is likely that the predicted shipping date and the inventory status
shown to a customer affect whether they choose to buy an item [4]. To analyze this
connection, you need to record the result of the user’s query of the shipping and
inventory status.
Writing read events to durable storage thus enables better tracking of causal depen‐
dencies (see “Ordering events to capture causality” on page 493), but it incurs addi‐
tional storage and I/O cost. Optimizing such systems to reduce the overhead is still
an open research problem [2]. But if you already log read requests for operational
purposes, as a side effect of request processing, it is not such a great change to make
the log the source of the requests instead.
Multi-partition data processing
For queries that only touch a single partition, the effort of sending queries through a
stream and collecting a stream of responses is perhaps overkill. However, this idea
opens the possibility of distributed execution of complex queries that need to com‐
bine data from several partitions, taking advantage of the infrastructure for message
routing, partitioning, and joining that is already provided by stream processors.
Storm’s distributed RPC feature supports this usage pattern (see “Message passing
and RPC” on page 468). For example, it has been used to compute the number of
people who have seen a URL on Twitter—i.e., the union of the follower sets of every‐
one who has tweeted that URL [48]. As the set of Twitter users is partitioned, this
computation requires combining results from many partitions.
514 
| 
Chapter 12: The Future of Data Systems


Another example of this pattern occurs in fraud prevention: in order to assess the risk
of whether a particular purchase event is fraudulent, you can examine the reputation
scores of the user’s IP address, email address, billing address, shipping address, and
so on. Each of these reputation databases is itself partitioned, and so collecting the
scores for a particular purchase event requires a sequence of joins with differently
partitioned datasets [49].
The internal query execution graphs of MPP databases have similar characteristics
(see “Comparing Hadoop to Distributed Databases” on page 414). If you need to per‐
form this kind of multi-partition join, it is probably simpler to use a database that
provides this feature than to implement it using a stream processor. However, treat‐
ing queries as streams provides an option for implementing large-scale applications
that run against the limits of conventional off-the-shelf solutions. 
Aiming for Correctness
With stateless services that only read data, it is not a big deal if something goes
wrong: you can fix the bug and restart the service, and everything returns to normal.
Stateful systems such as databases are not so simple: they are designed to remember
things forever (more or less), so if something goes wrong, the effects also potentially
last forever—which means they require more careful thought [50].
We want to build applications that are reliable and correct (i.e., programs whose
semantics are well defined and understood, even in the face of various faults). For
approximately four decades, the transaction properties of atomicity, isolation, and
durability (Chapter 7) have been the tools of choice for building correct applications.
However, those foundations are weaker than they seem: witness for example the con‐
fusion of weak isolation levels (see “Weak Isolation Levels” on page 233).
In some areas, transactions are being abandoned entirely and replaced with models
that offer better performance and scalability, but much messier semantics (see for
example “Leaderless Replication” on page 177). Consistency is often talked about, but
poorly defined (see “Consistency” on page 224 and Chapter 9). Some people assert
that we should “embrace weak consistency” for the sake of better availability, while
lacking a clear idea of what that actually means in practice.
For a topic that is so important, our understanding and our engineering methods are
surprisingly flaky. For example, it is very difficult to determine whether it is safe to
run a particular application at a particular transaction isolation level or replication
configuration [51, 52]. Often simple solutions appear to work correctly when concur‐
rency is low and there are no faults, but turn out to have many subtle bugs in more
demanding circumstances.
For example, Kyle Kingsbury’s Jepsen experiments [53] have highlighted the stark
discrepancies between some products’ claimed safety guarantees and their actual
Aiming for Correctness 
| 
515


behavior in the presence of network problems and crashes. Even if infrastructure
products like databases were free from problems, application code would still need to
correctly use the features they provide, which is error-prone if the configuration is
hard to understand (which is the case with weak isolation levels, quorum configura‐
tions, and so on).
If your application can tolerate occasionally corrupting or losing data in unpredicta‐
ble ways, life is a lot simpler, and you might be able to get away with simply crossing
your fingers and hoping for the best. On the other hand, if you need stronger assur‐
ances of correctness, then serializability and atomic commit are established
approaches, but they come at a cost: they typically only work in a single datacenter
(ruling out geographically distributed architectures), and they limit the scale and
fault-tolerance properties you can achieve.
While the traditional transaction approach is not going away, I also believe it is not
the last word in making applications correct and resilient to faults. In this section I
will suggest some ways of thinking about correctness in the context of dataflow archi‐
tectures.
The End-to-End Argument for Databases
Just because an application uses a data system that provides comparatively strong
safety properties, such as serializable transactions, that does not mean the application
is guaranteed to be free from data loss or corruption. For example, if an application
has a bug that causes it to write incorrect data, or delete data from a database, serial‐
izable transactions aren’t going to save you.
This example may seem frivolous, but it is worth taking seriously: application bugs
occur, and people make mistakes. I used this example in “State, Streams, and Immut‐
ability” on page 459 to argue in favor of immutable and append-only data, because it
is easier to recover from such mistakes if you remove the ability of faulty code to
destroy good data.
Although immutability is useful, it is not a cure-all by itself. Let’s look at a more sub‐
tle example of data corruption that can occur.
Exactly-once execution of an operation
In “Fault Tolerance” on page 476 we encountered an idea called exactly-once (or
effectively-once) semantics. If something goes wrong while processing a message, you
can either give up (drop the message—i.e., incur data loss) or try again. If you try
again, there is the risk that it actually succeeded the first time, but you just didn’t find
out about the success, and so the message ends up being processed twice.
Processing twice is a form of data corruption: it is undesirable to charge a customer
twice for the same service (billing them too much) or increment a counter twice
516 
| 
Chapter 12: The Future of Data Systems


(overstating some metric). In this context, exactly-once means arranging the compu‐
tation such that the final effect is the same as if no faults had occurred, even if the
operation actually was retried due to some fault. We previously discussed a few
approaches for achieving this goal.
One of the most effective approaches is to make the operation idempotent (see
“Idempotence” on page 478); that is, to ensure that it has the same effect, no matter
whether it is executed once or multiple times. However, taking an operation that is
not naturally idempotent and making it idempotent requires some effort and care:
you may need to maintain some additional metadata (such as the set of operation IDs
that have updated a value), and ensure fencing when failing over from one node to
another (see “The leader and the lock” on page 301).
Duplicate suppression
The same pattern of needing to suppress duplicates occurs in many other places
besides stream processing. For example, TCP uses sequence numbers on packets to
put them in the correct order at the recipient, and to determine whether any packets
were lost or duplicated on the network. Any lost packets are retransmitted and any
duplicates are removed by the TCP stack before it hands the data to an application.
However, this duplicate suppression only works within the context of a single TCP
connection. Imagine the TCP connection is a client’s connection to a database, and it
is currently executing the transaction in Example 12-1. In many databases, a transac‐
tion is tied to a client connection (if the client sends several queries, the database
knows that they belong to the same transaction because they are sent on the same
TCP connection). If the client suffers a network interruption and connection timeout
after sending the COMMIT, but before hearing back from the database server, it does
not know whether the transaction has been committed or aborted (Figure 8-1).
Example 12-1. A nonidempotent transfer of money from one account to another
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance + 11.00 WHERE account_id = 1234;
UPDATE accounts SET balance = balance - 11.00 WHERE account_id = 4321;
COMMIT;
The client can reconnect to the database and retry the transaction, but now it is out‐
side of the scope of TCP duplicate suppression. Since the transaction in Example 12-1
is not idempotent, it could happen that $22 is transferred instead of the desired $11.
Thus, even though Example 12-1 is a standard example for transaction atomicity, it is
actually not correct, and real banks do not work like this [3].
Two-phase commit (see “Atomic Commit and Two-Phase Commit (2PC)” on page
354) protocols break the 1:1 mapping between a TCP connection and a transaction,
since they must allow a transaction coordinator to reconnect to a database after a net‐
Aiming for Correctness 
| 
517


work fault, and tell it whether to commit or abort an in-doubt transaction. Is this suf‐
ficient to ensure that the transaction will only be executed once? Unfortunately not.
Even if we can suppress duplicate transactions between the database client and
server, we still need to worry about the network between the end-user device and the
application server. For example, if the end-user client is a web browser, it probably
uses an HTTP POST request to submit an instruction to the server. Perhaps the user
is on a weak cellular data connection, and they succeed in sending the POST, but the
signal becomes too weak before they are able to receive the response from the server.
In this case, the user will probably be shown an error message, and they may retry
manually. Web browsers warn, “Are you sure you want to submit this form again?”—
and the user says yes, because they wanted the operation to happen. (The Post/Redi‐
rect/Get pattern [54] avoids this warning message in normal operation, but it doesn’t
help if the POST request times out.) From the web server’s point of view the retry is a
separate request, and from the database’s point of view it is a separate transaction.
The usual deduplication mechanisms don’t help.
Operation identifiers
To make the operation idempotent through several hops of network communication,
it is not sufficient to rely just on a transaction mechanism provided by a database—
you need to consider the end-to-end flow of the request.
For example, you could generate a unique identifier for an operation (such as a
UUID) and include it as a hidden form field in the client application, or calculate a
hash of all the relevant form fields to derive the operation ID [3]. If the web browser
submits the POST request twice, the two requests will have the same operation ID.
You can then pass that operation ID all the way through to the database and check
that you only ever execute one operation with a given ID, as shown in Example 12-2.
Example 12-2. Suppressing duplicate requests using a unique ID
ALTER TABLE requests ADD UNIQUE (request_id);
BEGIN TRANSACTION;
INSERT INTO requests
  (request_id, from_account, to_account, amount)
  VALUES('0286FDB8-D7E1-423F-B40B-792B3608036C', 4321, 1234, 11.00);
UPDATE accounts SET balance = balance + 11.00 WHERE account_id = 1234;
UPDATE accounts SET balance = balance - 11.00 WHERE account_id = 4321;
COMMIT;
518 
| 
Chapter 12: The Future of Data Systems


Example 12-2 relies on a uniqueness constraint on the request_id column. If a
transaction attempts to insert an ID that already exists, the INSERT fails and the trans‐
action is aborted, preventing it from taking effect twice. Relational databases can gen‐
erally maintain a uniqueness constraint correctly, even at weak isolation levels
(whereas an application-level check-then-insert may fail under nonserializable isola‐
tion, as discussed in “Write Skew and Phantoms” on page 246).
Besides suppressing duplicate requests, the requests table in Example 12-2 acts as a
kind of event log, hinting in the direction of event sourcing (see “Event Sourcing” on
page 457). The updates to the account balances don’t actually have to happen in the
same transaction as the insertion of the event, since they are redundant and could be
derived from the request event in a downstream consumer—as long as the event is
processed exactly once, which can again be enforced using the request ID.
The end-to-end argument
This scenario of suppressing duplicate transactions is just one example of a more
general principle called the end-to-end argument, which was articulated by Saltzer,
Reed, and Clark in 1984 [55]:
The function in question can completely and correctly be implemented only with the
knowledge and help of the application standing at the endpoints of the communica‐
tion system. Therefore, providing that questioned function as a feature of the commu‐
nication system itself is not possible. (Sometimes an incomplete version of the function
provided by the communication system may be useful as a performance enhance‐
ment.)
In our example, the function in question was duplicate suppression. We saw that TCP
suppresses duplicate packets at the TCP connection level, and some stream process‐
ors provide so-called exactly-once semantics at the message processing level, but that
is not enough to prevent a user from submitting a duplicate request if the first one
times out. By themselves, TCP, database transactions, and stream processors cannot
entirely rule out these duplicates. Solving the problem requires an end-to-end solu‐
tion: a transaction identifier that is passed all the way from the end-user client to the
database.
The end-to-end argument also applies to checking the integrity of data: checksums
built into Ethernet, TCP, and TLS can detect corruption of packets in the network,
but they cannot detect corruption due to bugs in the software at the sending and
receiving ends of the network connection, or corruption on the disks where the data
is stored. If you want to catch all possible sources of data corruption, you also need
end-to-end checksums.
A similar argument applies with encryption [55]: the password on your home WiFi
network protects against people snooping your WiFi traffic, but not against attackers
elsewhere on the internet; TLS/SSL between your client and the server protects
Aiming for Correctness 
| 
519


against network attackers, but not against compromises of the server. Only end-toend encryption and authentication can protect against all of these things.
Although the low-level features (TCP duplicate suppression, Ethernet checksums,
WiFi encryption) cannot provide the desired end-to-end features by themselves, they
are still useful, since they reduce the probability of problems at the higher levels. For
example, HTTP requests would often get mangled if we didn’t have TCP putting the
packets back in the right order. We just need to remember that the low-level reliabil‐
ity features are not by themselves sufficient to ensure end-to-end correctness.
Applying end-to-end thinking in data systems
This brings me back to my original thesis: just because an application uses a data sys‐
tem that provides comparatively strong safety properties, such as serializable transac‐
tions, that does not mean the application is guaranteed to be free from data loss or
corruption. The application itself needs to take end-to-end measures, such as dupli‐
cate suppression, as well.
That is a shame, because fault-tolerance mechanisms are hard to get right. Low-level
reliability mechanisms, such as those in TCP, work quite well, and so the remaining
higher-level faults occur fairly rarely. It would be really nice to wrap up the remain‐
ing high-level fault-tolerance machinery in an abstraction so that application code
needn’t worry about it—but I fear that we have not yet found the right abstraction.
Transactions have long been seen as a good abstraction, and I do believe that they are
useful. As discussed in the introduction to Chapter 7, they take a wide range of possi‐
ble issues (concurrent writes, constraint violations, crashes, network interruptions,
disk failures) and collapse them down to two possible outcomes: commit or abort.
That is a huge simplification of the programming model, but I fear that it is not
enough.
Transactions are expensive, especially when they involve heterogeneous storage tech‐
nologies (see “Distributed Transactions in Practice” on page 360). When we refuse to
use distributed transactions because they are too expensive, we end up having to
reimplement fault-tolerance mechanisms in application code. As numerous examples
throughout this book have shown, reasoning about concurrency and partial failure is
difficult and counterintuitive, and so I suspect that most application-level mecha‐
nisms do not work correctly. The consequence is lost or corrupted data.
For these reasons, I think it is worth exploring fault-tolerance abstractions that make
it easy to provide application-specific end-to-end correctness properties, but also
maintain good performance and good operational characteristics in a large-scale dis‐
tributed environment. 
520 
| 
Chapter 12: The Future of Data Systems


Enforcing Constraints
Let’s think about correctness in the context of the ideas around unbundling databases
(“Unbundling Databases” on page 499). We saw that end-to-end duplicate suppres‐
sion can be achieved with a request ID that is passed all the way from the client to the
database that records the write. What about other kinds of constraints?
In particular, let’s focus on uniqueness constraints—such as the one we relied on in
Example 12-2. In “Constraints and uniqueness guarantees” on page 330 we saw sev‐
eral other examples of application features that need to enforce uniqueness: a user‐
name or email address must uniquely identify a user, a file storage service cannot
have more than one file with the same name, and two people cannot book the same
seat on a flight or in a theater.
Other kinds of constraints are very similar: for example, ensuring that an account
balance never goes negative, that you don’t sell more items than you have in stock in
the warehouse, or that a meeting room does not have overlapping bookings. Techni‐
ques that enforce uniqueness can often be used for these kinds of constraints as well.
Uniqueness constraints require consensus
In Chapter 9 we saw that in a distributed setting, enforcing a uniqueness constraint
requires consensus: if there are several concurrent requests with the same value, the
system somehow needs to decide which one of the conflicting operations is accepted,
and reject the others as violations of the constraint.
The most common way of achieving this consensus is to make a single node the
leader, and put it in charge of making all the decisions. That works fine as long as you
don’t mind funneling all requests through a single node (even if the client is on the
other side of the world), and as long as that node doesn’t fail. If you need to tolerate
the leader failing, you’re back at the consensus problem again (see “Single-leader rep‐
lication and consensus” on page 367).
Uniqueness checking can be scaled out by partitioning based on the value that needs
to be unique. For example, if you need to ensure uniqueness by request ID, as in
Example 12-2, you can ensure all requests with the same request ID are routed to the
same partition (see Chapter 6). If you need usernames to be unique, you can partition
by hash of username.
However, asynchronous multi-master replication is ruled out, because it could hap‐
pen that different masters concurrently accept conflicting writes, and thus the values
are no longer unique (see “Implementing Linearizable Systems” on page 332). If you
want to be able to immediately reject any writes that would violate the constraint,
synchronous coordination is unavoidable [56].
Aiming for Correctness 
| 
521


Uniqueness in log-based messaging
The log ensures that all consumers see messages in the same order—a guarantee that
is formally known as total order broadcast and is equivalent to consensus (see “Total
Order Broadcast” on page 348). In the unbundled database approach with log-based
messaging, we can use a very similar approach to enforce uniqueness constraints.
A stream processor consumes all the messages in a log partition sequentially on a sin‐
gle thread (see “Logs compared to traditional messaging” on page 448). Thus, if the
log is partitioned based on the value that needs to be unique, a stream processor can
unambiguously and deterministically decide which one of several conflicting opera‐
tions came first. For example, in the case of several users trying to claim the same
username [57]:
1. Every request for a username is encoded as a message, and appended to a parti‐
tion determined by the hash of the username.
2. A stream processor sequentially reads the requests in the log, using a local data‐
base to keep track of which usernames are taken. For every request for a user‐
name that is available, it records the name as taken and emits a success message
to an output stream. For every request for a username that is already taken, it
emits a rejection message to an output stream.
3. The client that requested the username watches the output stream and waits for a
success or rejection message corresponding to its request.
This algorithm is basically the same as in “Implementing linearizable storage using
total order broadcast” on page 350. It scales easily to a large request throughput by
increasing the number of partitions, as each partition can be processed independ‐
ently.
The approach works not only for uniqueness constraints, but also for many other
kinds of constraints. Its fundamental principle is that any writes that may conflict are
routed to the same partition and processed sequentially. As discussed in “What is a
conflict?” on page 174 and “Write Skew and Phantoms” on page 246, the definition of
a conflict may depend on the application, but the stream processor can use arbitrary
logic to validate a request. This idea is similar to the approach pioneered by Bayou in
the 1990s [58].
Multi-partition request processing
Ensuring that an operation is executed atomically, while satisfying constraints,
becomes more interesting when several partitions are involved. In Example 12-2,
there are potentially three partitions: the one containing the request ID, the one con‐
taining the payee account, and the one containing the payer account. There is no rea‐
522 
| 
Chapter 12: The Future of Data Systems


son why those three things should be in the same partition, since they are all
independent from each other.
In the traditional approach to databases, executing this transaction would require an
atomic commit across all three partitions, which essentially forces it into a total order
with respect to all other transactions on any of those partitions. Since there is now
cross-partition coordination, different partitions can no longer be processed inde‐
pendently, so throughput is likely to suffer.
However, it turns out that equivalent correctness can be achieved with partitioned
logs, and without an atomic commit:
1. The request to transfer money from account A to account B is given a unique
request ID by the client, and appended to a log partition based on the request ID.
2. A stream processor reads the log of requests. For each request message it emits
two messages to output streams: a debit instruction to the payer account A (par‐
titioned by A), and a credit instruction to the payee account B (partitioned by B).
The original request ID is included in those emitted messages.
3. Further processors consume the streams of credit and debit instructions, dedu‐
plicate by request ID, and apply the changes to the account balances.
Steps 1 and 2 are necessary because if the client directly sent the credit and debit
instructions, it would require an atomic commit across those two partitions to ensure
that either both or neither happen. To avoid the need for a distributed transaction,
we first durably log the request as a single message, and then derive the credit and
debit instructions from that first message. Single-object writes are atomic in almost
all data systems (see “Single-object writes” on page 230), and so the request either
appears in the log or it doesn’t, without any need for a multi-partition atomic com‐
mit.
If the stream processor in step 2 crashes, it resumes processing from its last check‐
point. In doing so, it does not skip any request messages, but it may process requests
multiple times and produce duplicate credit and debit instructions. However, since it
is deterministic, it will just produce the same instructions again, and the processors in
step 3 can easily deduplicate them using the end-to-end request ID.
If you want to ensure that the payer account is not overdrawn by this transfer, you
can additionally have a stream processor (partitioned by payer account number) that
maintains account balances and validates transactions. Only valid transactions would
then be placed in the request log in step 1.
By breaking down the multi-partition transaction into two differently partitioned
stages and using the end-to-end request ID, we have achieved the same correctness
property (every request is applied exactly once to both the payer and payee accounts),
even in the presence of faults, and without using an atomic commit protocol. The
Aiming for Correctness 
| 
523


idea of using multiple differently partitioned stages is similar to what we discussed in
“Multi-partition data processing” on page 514 (see also “Concurrency control” on
page 462). 
Timeliness and Integrity
A convenient property of transactions is that they are typically linearizable (see “Lin‐
earizability” on page 324): that is, a writer waits until a transaction is committed, and
thereafter its writes are immediately visible to all readers.
This is not the case when unbundling an operation across multiple stages of stream
processors: consumers of a log are asynchronous by design, so a sender does not wait
until its message has been processed by consumers. However, it is possible for a client
to wait for a message to appear on an output stream. This is what we did in “Unique‐
ness in log-based messaging” on page 522 when checking whether a uniqueness con‐
straint was satisfied.
In this example, the correctness of the uniqueness check does not depend on whether
the sender of the message waits for the outcome. The waiting only has the purpose of
synchronously informing the sender whether or not the uniqueness check succeeded,
but this notification can be decoupled from the effects of processing the message.
More generally, I think the term consistency conflates two different requirements that
are worth considering separately:
Timeliness
Timeliness means ensuring that users observe the system in an up-to-date state.
We saw previously that if a user reads from a stale copy of the data, they may
observe it in an inconsistent state (see “Problems with Replication Lag” on page
161). However, that inconsistency is temporary, and will eventually be resolved
simply by waiting and trying again.
The CAP theorem (see “The Cost of Linearizability” on page 335) uses consis‐
tency in the sense of linearizability, which is a strong way of achieving timeliness.
Weaker timeliness properties like read-after-write consistency (see “Reading
Your Own Writes” on page 162) can also be useful.
Integrity
Integrity means absence of corruption; i.e., no data loss, and no contradictory or
false data. In particular, if some derived dataset is maintained as a view onto
some underlying data (see “Deriving current state from the event log” on page
458), the derivation must be correct. For example, a database index must cor‐
rectly reflect the contents of the database—an index in which some records are
missing is not very useful.
524 
| 
Chapter 12: The Future of Data Systems


If integrity is violated, the inconsistency is permanent: waiting and trying again is
not going to fix database corruption in most cases. Instead, explicit checking and
repair is needed. In the context of ACID transactions (see “The Meaning of
ACID” on page 223), consistency is usually understood as some kind of
application-specific notion of integrity. Atomicity and durability are important
tools for preserving integrity.
In slogan form: violations of timeliness are “eventual consistency,” whereas violations
of integrity are “perpetual inconsistency.”
I am going to assert that in most applications, integrity is much more important than
timeliness. Violations of timeliness can be annoying and confusing, but violations of
integrity can be catastrophic.
For example, on your credit card statement, it is not surprising if a transaction that
you made within the last 24 hours does not yet appear—it is normal that these sys‐
tems have a certain lag. We know that banks reconcile and settle transactions asyn‐
chronously, and timeliness is not very important here [3]. However, it would be very
bad if the statement balance was not equal to the sum of the transactions plus the
previous statement balance (an error in the sums), or if a transaction was charged to
you but not paid to the merchant (disappearing money). Such problems would be
violations of the integrity of the system.
Correctness of dataflow systems
ACID transactions usually provide both timeliness (e.g., linearizability) and integrity
(e.g., atomic commit) guarantees. Thus, if you approach application correctness from
the point of view of ACID transactions, the distinction between timeliness and integ‐
rity is fairly inconsequential.
On the other hand, an interesting property of the event-based dataflow systems that
we have discussed in this chapter is that they decouple timeliness and integrity. When
processing event streams asynchronously, there is no guarantee of timeliness, unless
you explicitly build consumers that wait for a message to arrive before returning. But
integrity is in fact central to streaming systems.
Exactly-once or effectively-once semantics (see “Fault Tolerance” on page 476) is a
mechanism for preserving integrity. If an event is lost, or if an event takes effect
twice, the integrity of a data system could be violated. Thus, fault-tolerant message
delivery and duplicate suppression (e.g., idempotent operations) are important for
maintaining the integrity of a data system in the face of faults.
As we saw in the last section, reliable stream processing systems can preserve integ‐
rity without requiring distributed transactions and an atomic commit protocol,
which means they can potentially achieve comparable correctness with much better
Aiming for Correctness 
| 
525


performance and operational robustness. We achieved this integrity through a com‐
bination of mechanisms:
• Representing the content of the write operation as a single message, which can
easily be written atomically—an approach that fits very well with event sourcing
(see “Event Sourcing” on page 457)
• Deriving all other state updates from that single message using deterministic der‐
ivation functions, similarly to stored procedures (see “Actual Serial Execution”
on page 252 and “Application code as a derivation function” on page 505)
• Passing a client-generated request ID through all these levels of processing, ena‐
bling end-to-end duplicate suppression and idempotence
• Making messages immutable and allowing derived data to be reprocessed from
time to time, which makes it easier to recover from bugs (see “Advantages of
immutable events” on page 460)
This combination of mechanisms seems to me a very promising direction for build‐
ing fault-tolerant applications in the future. 
Loosely interpreted constraints
As discussed previously, enforcing a uniqueness constraint requires consensus, typi‐
cally implemented by funneling all events in a particular partition through a single
node. This limitation is unavoidable if we want the traditional form of uniqueness
constraint, and stream processing cannot avoid it.
However, another thing to realize is that many real applications can actually get away
with much weaker notions of uniqueness:
• If two people concurrently register the same username or book the same seat,
you can send one of them a message to apologize, and ask them to choose a dif‐
ferent one. This kind of change to correct a mistake is called a compensating
transaction [59, 60].
• If customers order more items than you have in your warehouse, you can order
in more stock, apologize to customers for the delay, and offer them a discount.
This is actually the same as what you’d have to do if, say, a forklift truck ran over
some of the items in your warehouse, leaving you with fewer items in stock than
you thought you had [61]. Thus, the apology workflow already needs to be part
of your business processes anyway, and so it might be unnecessary to require a
linearizable constraint on the number of items in stock.
• Similarly, many airlines overbook airplanes in the expectation that some passen‐
gers will miss their flight, and many hotels overbook rooms, expecting that some
guests will cancel. In these cases, the constraint of “one person per seat” is delib‐
526 
| 
Chapter 12: The Future of Data Systems


erately violated for business reasons, and compensation processes (refunds,
upgrades, providing a complimentary room at a neighboring hotel) are put in
place to handle situations in which demand exceeds supply. Even if there was no
overbooking, apology and compensation processes would be needed in order to
deal with flights being cancelled due to bad weather or staff on strike—recover‐
ing from such issues is just a normal part of business [3].
• If someone withdraws more money than they have in their account, the bank can
charge them an overdraft fee and ask them to pay back what they owe. By limit‐
ing the total withdrawals per day, the risk to the bank is bounded.
In many business contexts, it is actually acceptable to temporarily violate a constraint
and fix it up later by apologizing. The cost of the apology (in terms of money or repu‐
tation) varies, but it is often quite low: you can’t unsend an email, but you can send a
follow-up email with a correction. If you accidentally charge a credit card twice, you
can refund one of the charges, and the cost to you is just the processing fees and per‐
haps a customer complaint. Once money has been paid out of an ATM, you can’t
directly get it back, although in principle you can send debt collectors to recover the
money if the account was overdrawn and the customer won’t pay it back.
Whether the cost of the apology is acceptable is a business decision. If it is acceptable,
the traditional model of checking all constraints before even writing the data is
unnecessarily restrictive, and a linearizable constraint is not needed. It may well be a
reasonable choice to go ahead with a write optimistically, and to check the constraint
after the fact. You can still ensure that the validation occurs before doing things that
would be expensive to recover from, but that doesn’t imply you must do the valida‐
tion before you even write the data.
These applications do require integrity: you would not want to lose a reservation, or
have money disappear due to mismatched credits and debits. But they don’t require
timeliness on the enforcement of the constraint: if you have sold more items than you
have in the warehouse, you can patch up the problem after the fact by apologizing.
Doing so is similar to the conflict resolution approaches we discussed in “Handling
Write Conflicts” on page 171.
Coordination-avoiding data systems
We have now made two interesting observations:
1. Dataflow systems can maintain integrity guarantees on derived data without
atomic commit, linearizability, or synchronous cross-partition coordination.
2. Although strict uniqueness constraints require timeliness and coordination,
many applications are actually fine with loose constraints that may be temporar‐
ily violated and fixed up later, as long as integrity is preserved throughout.
Aiming for Correctness 
| 
527


Taken together, these observations mean that dataflow systems can provide the data
management services for many applications without requiring coordination, while
still giving strong integrity guarantees. Such coordination-avoiding data systems have
a lot of appeal: they can achieve better performance and fault tolerance than systems
that need to perform synchronous coordination [56].
For example, such a system could operate distributed across multiple datacenters in a
multi-leader configuration, asynchronously replicating between regions. Any one
datacenter can continue operating independently from the others, because no syn‐
chronous cross-region coordination is required. Such a system would have weak
timeliness guarantees—it could not be linearizable without introducing coordination
—but it can still have strong integrity guarantees.
In this context, serializable transactions are still useful as part of maintaining derived
state, but they can be run at a small scope where they work well [8]. Heterogeneous
distributed transactions such as XA transactions (see “Distributed Transactions in
Practice” on page 360) are not required. Synchronous coordination can still be intro‐
duced in places where it is needed (for example, to enforce strict constraints before
an operation from which recovery is not possible), but there is no need for everything
to pay the cost of coordination if only a small part of an application needs it [43].
Another way of looking at coordination and constraints: they reduce the number of
apologies you have to make due to inconsistencies, but potentially also reduce the
performance and availability of your system, and thus potentially increase the num‐
ber of apologies you have to make due to outages. You cannot reduce the number of
apologies to zero, but you can aim to find the best trade-off for your needs—the
sweet spot where there are neither too many inconsistencies nor too many availability
problems. 
Trust, but Verify
All of our discussion of correctness, integrity, and fault-tolerance has been under the
assumption that certain things might go wrong, but other things won’t. We call these
assumptions our system model (see “Mapping system models to the real world” on
page 309): for example, we should assume that processes can crash, machines can
suddenly lose power, and the network can arbitrarily delay or drop messages. But we
might also assume that data written to disk is not lost after fsync, that data in mem‐
ory is not corrupted, and that the multiplication instruction of our CPU always
returns the correct result.
These assumptions are quite reasonable, as they are true most of the time, and it
would be difficult to get anything done if we had to constantly worry about our com‐
puters making mistakes. Traditionally, system models take a binary approach toward
faults: we assume that some things can happen, and other things can never happen.
In reality, it is more a question of probabilities: some things are more likely, other
528 
| 
Chapter 12: The Future of Data Systems


things less likely. The question is whether violations of our assumptions happen often
enough that we may encounter them in practice.
We have seen that data can become corrupted while it is sitting untouched on disks
(see “Replication and Durability” on page 227), and data corruption on the network
can sometimes evade the TCP checksums (see “Weak forms of lying” on page 306).
Maybe this is something we should be paying more attention to?
One application that I worked on in the past collected crash reports from clients, and
some of the reports we received could only be explained by random bit-flips in the
memory of those devices. It seems unlikely, but if you have enough devices running
your software, even very unlikely things do happen. Besides random memory corrup‐
tion due to hardware faults or radiation, certain pathological memory access patterns
can flip bits even in memory that has no faults [62]—an effect that can be used to
break security mechanisms in operating systems [63] (this technique is known as
rowhammer). Once you look closely, hardware isn’t quite the perfect abstraction that
it may seem.
To be clear, random bit-flips are still very rare on modern hardware [64]. I just want
to point out that they are not beyond the realm of possibility, and so they deserve
some attention.
Maintaining integrity in the face of software bugs
Besides such hardware issues, there is always the risk of software bugs, which would
not be caught by lower-level network, memory, or filesystem checksums. Even widely
used database software has bugs: I have personally seen cases of MySQL failing to
correctly maintain a uniqueness constraint [65] and PostgreSQL’s serializable isola‐
tion level exhibiting write skew anomalies [66], even though MySQL and PostgreSQL
are robust and well-regarded databases that have been battle-tested by many people
for many years. In less mature software, the situation is likely to be much worse.
Despite considerable efforts in careful design, testing, and review, bugs still creep in.
Although they are rare, and they eventually get found and fixed, there is still a period
during which such bugs can corrupt data.
When it comes to application code, we have to assume many more bugs, since most
applications don’t receive anywhere near the amount of review and testing that data‐
base code does. Many applications don’t even correctly use the features that databases
offer for preserving integrity, such as foreign key or uniqueness constraints [36].
Consistency in the sense of ACID (see “Consistency” on page 224) is based on the
idea that the database starts off in a consistent state, and a transaction transforms it
from one consistent state to another consistent state. Thus, we expect the database to
always be in a consistent state. However, this notion only makes sense if you assume
that the transaction is free from bugs. If the application uses the database incorrectly
Aiming for Correctness 
| 
529


in some way, for example using a weak isolation level unsafely, the integrity of the
database cannot be guaranteed.
Don’t just blindly trust what they promise
With both hardware and software not always living up to the ideal that we would like
them to be, it seems that data corruption is inevitable sooner or later. Thus, we
should at least have a way of finding out if data has been corrupted so that we can fix
it and try to track down the source of the error. Checking the integrity of data is
known as auditing.
As discussed in “Advantages of immutable events” on page 460, auditing is not just
for financial applications. However, auditability is highly important in finance pre‐
cisely because everyone knows that mistakes happen, and we all recognize the need to
be able to detect and fix problems.
Mature systems similarly tend to consider the possibility of unlikely things going
wrong, and manage that risk. For example, large-scale storage systems such as HDFS
and Amazon S3 do not fully trust disks: they run background processes that continu‐
ally read back files, compare them to other replicas, and move files from one disk to
another, in order to mitigate the risk of silent corruption [67].
If you want to be sure that your data is still there, you have to actually read it and
check. Most of the time it will still be there, but if it isn’t, you really want to find out
sooner rather than later. By the same argument, it is important to try restoring from
your backups from time to time—otherwise you may only find out that your backup
is broken when it is too late and you have already lost data. Don’t just blindly trust
that it is all working.
A culture of verification
Systems like HDFS and S3 still have to assume that disks work correctly most of the
time—which is a reasonable assumption, but not the same as assuming that they
always work correctly. However, not many systems currently have this kind of “trust,
but verify” approach of continually auditing themselves. Many assume that correct‐
ness guarantees are absolute and make no provision for the possibility of rare data
corruption. I hope that in the future we will see more self-validating or self-auditing
systems that continually check their own integrity, rather than relying on blind trust
[68].
I fear that the culture of ACID databases has led us toward developing applications
on the basis of blindly trusting technology (such as a transaction mechanism), and
neglecting any sort of auditability in the process. Since the technology we trusted
worked well enough most of the time, auditing mechanisms were not deemed worth
the investment.
530 
| 
Chapter 12: The Future of Data Systems


But then the database landscape changed: weaker consistency guarantees became the
norm under the banner of NoSQL, and less mature storage technologies became
widely used. Yet, because the audit mechanisms had not been developed, we contin‐
ued building applications on the basis of blind trust, even though this approach had
now become more dangerous. Let’s think for a moment about designing for audita‐
bility.
Designing for auditability
If a transaction mutates several objects in a database, it is difficult to tell after the fact
what that transaction means. Even if you capture the transaction logs (see “Change
Data Capture” on page 454), the insertions, updates, and deletions in various tables
do not necessarily give a clear picture of why those mutations were performed. The
invocation of the application logic that decided on those mutations is transient and
cannot be reproduced.
By contrast, event-based systems can provide better auditability. In the event sourc‐
ing approach, user input to the system is represented as a single immutable event,
and any resulting state updates are derived from that event. The derivation can be
made deterministic and repeatable, so that running the same log of events through
the same version of the derivation code will result in the same state updates.
Being explicit about dataflow (see “Philosophy of batch process outputs” on page
413) makes the provenance of data much clearer, which makes integrity checking
much more feasible. For the event log, we can use hashes to check that the event stor‐
age has not been corrupted. For any derived state, we can rerun the batch and stream
processors that derived it from the event log in order to check whether we get the
same result, or even run a redundant derivation in parallel.
A deterministic and well-defined dataflow also makes it easier to debug and trace the
execution of a system in order to determine why it did something [4, 69]. If some‐
thing unexpected occurred, it is valuable to have the diagnostic capability to repro‐
duce the exact circumstances that led to the unexpected event—a kind of time-travel
debugging capability.
The end-to-end argument again
If we cannot fully trust that every individual component of the system will be free
from corruption—that every piece of hardware is fault-free and that every piece of
software is bug-free—then we must at least periodically check the integrity of our
data. If we don’t check, we won’t find out about corruption until it is too late and it
has caused some downstream damage, at which point it will be much harder and
more expensive to track down the problem.
Checking the integrity of data systems is best done in an end-to-end fashion (see
“The End-to-End Argument for Databases” on page 516): the more systems we can
Aiming for Correctness 
| 
531


include in an integrity check, the fewer opportunities there are for corruption to go
unnoticed at some stage of the process. If we can check that an entire derived data
pipeline is correct end to end, then any disks, networks, services, and algorithms
along the path are implicitly included in the check.
Having continuous end-to-end integrity checks gives you increased confidence about
the correctness of your systems, which in turn allows you to move faster [70]. Like
automated testing, auditing increases the chances that bugs will be found quickly,
and thus reduces the risk that a change to the system or a new storage technology will
cause damage. If you are not afraid of making changes, you can much better evolve
an application to meet changing requirements.
Tools for auditable data systems
At present, not many data systems make auditability a top-level concern. Some appli‐
cations implement their own audit mechanisms, for example by logging all changes
to a separate audit table, but guaranteeing the integrity of the audit log and the data‐
base state is still difficult. A transaction log can be made tamper-proof by periodically
signing it with a hardware security module, but that does not guarantee that the right
transactions went into the log in the first place.
It would be interesting to use cryptographic tools to prove the integrity of a system in
a way that is robust to a wide range of hardware and software issues, and even poten‐
tially malicious actions. Cryptocurrencies, blockchains, and distributed ledger tech‐
nologies such as Bitcoin, Ethereum, Ripple, Stellar, and various others [71, 72, 73]
have sprung up to explore this area.
I am not qualified to comment on the merits of these technologies as currencies or
mechanisms for agreeing contracts. However, from a data systems point of view they
contain some interesting ideas. Essentially, they are distributed databases, with a data
model and transaction mechanism, in which different replicas can be hosted by
mutually untrusting organizations. The replicas continually check each other’s integ‐
rity and use a consensus protocol to agree on the transactions that should be exe‐
cuted.
I am somewhat skeptical about the Byzantine fault tolerance aspects of these technol‐
ogies (see “Byzantine Faults” on page 304), and I find the technique of proof of work
(e.g., Bitcoin mining) extraordinarily wasteful. The transaction throughput of Bitcoin
is rather low, albeit for political and economic reasons more than for technical ones.
However, the integrity checking aspects are interesting.
Cryptographic auditing and integrity checking often relies on Merkle trees [74],
which are trees of hashes that can be used to efficiently prove that a record appears in
some dataset (and a few other things). Outside of the hype of cryptocurrencies, certif‐
icate transparency is a security technology that relies on Merkle trees to check the val‐
idity of TLS/SSL certificates [75, 76].
532 
| 
Chapter 12: The Future of Data Systems


I could imagine integrity-checking and auditing algorithms, like those of certificate
transparency and distributed ledgers, becoming more widely used in data systems in
general. Some work will be needed to make them equally scalable as systems without
cryptographic auditing, and to keep the performance penalty as low as possible. But I
think this is an interesting area to watch in the future. 
Doing the Right Thing
In the final section of this book, I would like to take a step back. Throughout this
book we have examined a wide range of different architectures for data systems, eval‐
uated their pros and cons, and explored techniques for building reliable, scalable, and
maintainable applications. However, we have left out an important and fundamental
part of the discussion, which I would now like to fill in.
Every system is built for a purpose; every action we take has both intended and unin‐
tended consequences. The purpose may be as simple as making money, but the con‐
sequences for the world may reach far beyond that original purpose. We, the
engineers building these systems, have a responsibility to carefully consider those
consequences and to consciously decide what kind of world we want to live in.
We talk about data as an abstract thing, but remember that many datasets are about
people: their behavior, their interests, their identity. We must treat such data with
humanity and respect. Users are humans too, and human dignity is paramount.
Software development increasingly involves making important ethical choices. There
are guidelines to help software engineers navigate these issues, such as the ACM’s
Software Engineering Code of Ethics and Professional Practice [77], but they are
rarely discussed, applied, and enforced in practice. As a result, engineers and product
managers sometimes take a very cavalier attitude to privacy and potential negative
consequences of their products [78, 79, 80].
A technology is not good or bad in itself—what matters is how it is used and how it
affects people. This is true for a software system like a search engine in much the
same way as it is for a weapon like a gun. I think it is not sufficient for software engi‐
neers to focus exclusively on the technology and ignore its consequences: the ethical
responsibility is ours to bear also. Reasoning about ethics is difficult, but it is too
important to ignore.
Predictive Analytics
For example, predictive analytics is a major part of the “Big Data” hype. Using data
analysis to predict the weather, or the spread of diseases, is one thing [81]; it is
another matter to predict whether a convict is likely to reoffend, whether an applicant
for a loan is likely to default, or whether an insurance customer is likely to make
expensive claims. The latter have a direct effect on individual people’s lives.
Doing the Right Thing 
| 
533


Naturally, payment networks want to prevent fraudulent transactions, banks want to
avoid bad loans, airlines want to avoid hijackings, and companies want to avoid hir‐
ing ineffective or untrustworthy people. From their point of view, the cost of a missed
business opportunity is low, but the cost of a bad loan or a problematic employee is
much higher, so it is natural for organizations to want to be cautious. If in doubt,
they are better off saying no.
However, as algorithmic decision-making becomes more widespread, someone who
has (accurately or falsely) been labeled as risky by some algorithm may suffer a large
number of those “no” decisions. Systematically being excluded from jobs, air travel,
insurance coverage, property rental, financial services, and other key aspects of soci‐
ety is such a large constraint of the individual’s freedom that it has been called “algo‐
rithmic prison” [82]. In countries that respect human rights, the criminal justice
system presumes innocence until proven guilty; on the other hand, automated sys‐
tems can systematically and arbitrarily exclude a person from participating in society
without any proof of guilt, and with little chance of appeal.
Bias and discrimination
Decisions made by an algorithm are not necessarily any better or any worse than
those made by a human. Every person is likely to have biases, even if they actively try
to counteract them, and discriminatory practices can become culturally institutional‐
ized. There is hope that basing decisions on data, rather than subjective and instinc‐
tive assessments by people, could be more fair and give a better chance to people who
are often overlooked in the traditional system [83].
When we develop predictive analytics systems, we are not merely automating a
human’s decision by using software to specify the rules for when to say yes or no; we
are even leaving the rules themselves to be inferred from data. However, the patterns
learned by these systems are opaque: even if there is some correlation in the data, we
may not know why. If there is a systematic bias in the input to an algorithm, the sys‐
tem will most likely learn and amplify that bias in its output [84].
In many countries, anti-discrimination laws prohibit treating people differently
depending on protected traits such as ethnicity, age, gender, sexuality, disability, or
beliefs. Other features of a person’s data may be analyzed, but what happens if they
are correlated with protected traits? For example, in racially segregated neighbor‐
hoods, a person’s postal code or even their IP address is a strong predictor of race.
Put like this, it seems ridiculous to believe that an algorithm could somehow take
biased data as input and produce fair and impartial output from it [85]. Yet this belief
often seems to be implied by proponents of data-driven decision making, an attitude
that has been satirized as “machine learning is like money laundering for bias” [86].
Predictive analytics systems merely extrapolate from the past; if the past is discrimi‐
natory, they codify that discrimination. If we want the future to be better than the
534 
| 
Chapter 12: The Future of Data Systems


past, moral imagination is required, and that’s something only humans can provide
[87]. Data and models should be our tools, not our masters.
Responsibility and accountability
Automated decision making opens the question of responsibility and accountability
[87]. If a human makes a mistake, they can be held accountable, and the person affec‐
ted by the decision can appeal. Algorithms make mistakes too, but who is accounta‐
ble if they go wrong [88]? When a self-driving car causes an accident, who is
responsible? If an automated credit scoring algorithm systematically discriminates
against people of a particular race or religion, is there any recourse? If a decision by
your machine learning system comes under judicial review, can you explain to the
judge how the algorithm made its decision?
Credit rating agencies are an old example of collecting data to make decisions about
people. A bad credit score makes life difficult, but at least a credit score is normally
based on relevant facts about a person’s actual borrowing history, and any errors in
the record can be corrected (although the agencies normally do not make this easy).
However, scoring algorithms based on machine learning typically use a much wider
range of inputs and are much more opaque, making it harder to understand how a
particular decision has come about and whether someone is being treated in an
unfair or discriminatory way [89].
A credit score summarizes “How did you behave in the past?” whereas predictive
analytics usually work on the basis of “Who is similar to you, and how did people like
you behave in the past?” Drawing parallels to others’ behavior implies stereotyping
people, for example based on where they live (a close proxy for race and socioeco‐
nomic class). What about people who get put in the wrong bucket? Furthermore, if a
decision is incorrect due to erroneous data, recourse is almost impossible [87].
Much data is statistical in nature, which means that even if the probability distribu‐
tion on the whole is correct, individual cases may well be wrong. For example, if the
average life expectancy in your country is 80 years, that doesn’t mean you’re expected
to drop dead on your 80th birthday. From the average and the probability distribu‐
tion, you can’t say much about the age to which one particular person will live. Simi‐
larly, the output of a prediction system is probabilistic and may well be wrong in
individual cases.
A blind belief in the supremacy of data for making decisions is not only delusional, it
is positively dangerous. As data-driven decision making becomes more widespread,
we will need to figure out how to make algorithms accountable and transparent, how
to avoid reinforcing existing biases, and how to fix them when they inevitably make
mistakes.
We will also need to figure out how to prevent data being used to harm people, and
realize its positive potential instead. For example, analytics can reveal financial and
Doing the Right Thing 
| 
535


social characteristics of people’s lives. On the one hand, this power could be used to
focus aid and support to help those people who most need it. On the other hand, it is
sometimes used by predatory business seeking to identify vulnerable people and sell
them risky products such as high-cost loans and worthless college degrees [87, 90].
Feedback loops
Even with predictive applications that have less immediately far-reaching effects on
people, such as recommendation systems, there are difficult issues that we must con‐
front. When services become good at predicting what content users want to see, they
may end up showing people only opinions they already agree with, leading to echo
chambers in which stereotypes, misinformation, and polarization can breed. We are
already seeing the impact of social media echo chambers on election campaigns [91].
When predictive analytics affect people’s lives, particularly pernicious problems arise
due to self-reinforcing feedback loops. For example, consider the case of employers
using credit scores to evaluate potential hires. You may be a good worker with a good
credit score, but suddenly find yourself in financial difficulties due to a misfortune
outside of your control. As you miss payments on your bills, your credit score suffers,
and you will be less likely to find work. Joblessness pushes you toward poverty, which
further worsens your scores, making it even harder to find employment [87]. It’s a
downward spiral due to poisonous assumptions, hidden behind a camouflage of
mathematical rigor and data.
We can’t always predict when such feedback loops happen. However, many conse‐
quences can be predicted by thinking about the entire system (not just the computer‐
ized parts, but also the people interacting with it)—an approach known as systems
thinking [92]. We can try to understand how a data analysis system responds to dif‐
ferent behaviors, structures, or characteristics. Does the system reinforce and amplify
existing differences between people (e.g., making the rich richer or the poor poorer),
or does it try to combat injustice? And even with the best intentions, we must beware
of unintended consequences. 
Privacy and Tracking
Besides the problems of predictive analytics—i.e., using data to make automated
decisions about people—there are ethical problems with data collection itself. What is
the relationship between the organizations collecting data and the people whose data
is being collected?
When a system only stores data that a user has explicitly entered, because they want
the system to store and process it in a certain way, the system is performing a service
for the user: the user is the customer. But when a user’s activity is tracked and logged
as a side effect of other things they are doing, the relationship is less clear. The service
536 
| 
Chapter 12: The Future of Data Systems


no longer just does what the user tells it to do, but it takes on interests of its own,
which may conflict with the user’s interests.
Tracking behavioral data has become increasingly important for user-facing features
of many online services: tracking which search results are clicked helps improve the
ranking of search results; recommending “people who liked X also liked Y” helps
users discover interesting and useful things; A/B tests and user flow analysis can help
indicate how a user interface might be improved. Those features require some
amount of tracking of user behavior, and users benefit from them.
However, depending on a company’s business model, tracking often doesn’t stop
there. If the service is funded through advertising, the advertisers are the actual cus‐
tomers, and the users’ interests take second place. Tracking data becomes more
detailed, analyses become further-reaching, and data is retained for a long time in
order to build up detailed profiles of each person for marketing purposes.
Now the relationship between the company and the user whose data is being collec‐
ted starts looking quite different. The user is given a free service and is coaxed into
engaging with it as much as possible. The tracking of the user serves not primarily
that individual, but rather the needs of the advertisers who are funding the service. I
think this relationship can be appropriately described with a word that has more sin‐
ister connotations: surveillance.
Surveillance
As a thought experiment, try replacing the word data with surveillance, and observe if
common phrases still sound so good [93]. How about this: “In our surveillancedriven organization we collect real-time surveillance streams and store them in our
surveillance warehouse. Our surveillance scientists use advanced analytics and sur‐
veillance processing in order to derive new insights.”
This thought experiment is unusually polemic for this book, Designing Surveillance-
Intensive Applications, but I think that strong words are needed to emphasize this
point. In our attempts to make software “eat the world” [94], we have built the great‐
est mass surveillance infrastructure the world has ever seen. Rushing toward an Inter‐
net of Things, we are rapidly approaching a world in which every inhabited space
contains at least one internet-connected microphone, in the form of smartphones,
smart TVs, voice-controlled assistant devices, baby monitors, and even children’s
toys that use cloud-based speech recognition. Many of these devices have a terrible
security record [95].
Even the most totalitarian and repressive regimes could only dream of putting a
microphone in every room and forcing every person to constantly carry a device
capable of tracking their location and movements. Yet we apparently voluntarily,
even enthusiastically, throw ourselves into this world of total surveillance. The differ‐
Doing the Right Thing 
| 
537


ence is just that the data is being collected by corporations rather than government
agencies [96].
Not all data collection necessarily qualifies as surveillance, but examining it as such
can help us understand our relationship with the data collector. Why are we seem‐
ingly happy to accept surveillance by corporations? Perhaps you feel you have noth‐
ing to hide—in other words, you are totally in line with existing power structures,
you are not a marginalized minority, and you needn’t fear persecution [97]. Not
everyone is so fortunate. Or perhaps it’s because the purpose seems benign—it’s not
overt coercion and conformance, but merely better recommendations and more per‐
sonalized marketing. However, combined with the discussion of predictive analytics
from the last section, that distinction seems less clear.
We are already seeing car insurance premiums linked to tracking devices in cars, and
health insurance coverage that depends on people wearing a fitness tracking device.
When surveillance is used to determine things that hold sway over important aspects
of life, such as insurance coverage or employment, it starts to appear less benign.
Moreover, data analysis can reveal surprisingly intrusive things: for example, the
movement sensor in a smartwatch or fitness tracker can be used to work out what
you are typing (for example, passwords) with fairly good accuracy [98]. And algo‐
rithms for analysis are only going to get better.
Consent and freedom of choice
We might assert that users voluntarily choose to use a service that tracks their activ‐
ity, and they have agreed to the terms of service and privacy policy, so they consent to
data collection. We might even claim that users are receiving a valuable service in
return for the data they provide, and that the tracking is necessary in order to provide
the service. Undoubtedly, social networks, search engines, and various other free
online services are valuable to users—but there are problems with this argument.
Users have little knowledge of what data they are feeding into our databases, or how
it is retained and processed—and most privacy policies do more to obscure than to
illuminate. Without understanding what happens to their data, users cannot give any
meaningful consent. Often, data from one user also says things about other people
who are not users of the service and who have not agreed to any terms. The derived
datasets that we discussed in this part of the book—in which data from the entire
user base may have been combined with behavioral tracking and external data sour‐
ces—are precisely the kinds of data of which users cannot have any meaningful
understanding.
Moreover, data is extracted from users through a one-way process, not a relationship
with true reciprocity, and not a fair value exchange. There is no dialog, no option for
users to negotiate how much data they provide and what service they receive in
538 
| 
Chapter 12: The Future of Data Systems


return: the relationship between the service and the user is very asymmetric and onesided. The terms are set by the service, not by the user [99].
For a user who does not consent to surveillance, the only real alternative is simply not
to use a service. But this choice is not free either: if a service is so popular that it is
“regarded by most people as essential for basic social participation” [99], then it is not
reasonable to expect people to opt out of this service—using it is de facto mandatory.
For example, in most Western social communities, it has become the norm to carry a
smartphone, to use Facebook for socializing, and to use Google for finding informa‐
tion. Especially when a service has network effects, there is a social cost to people
choosing not to use it.
Declining to use a service due to its tracking of users is only an option for the small
number of people who are privileged enough to have the time and knowledge to
understand its privacy policy, and who can afford to potentially miss out on social
participation or professional opportunities that may have arisen if they had participa‐
ted in the service. For people in a less privileged position, there is no meaningful free‐
dom of choice: surveillance becomes inescapable.
Privacy and use of data
Sometimes people claim that “privacy is dead” on the grounds that some users are
willing to post all sorts of things about their lives to social media, sometimes mun‐
dane and sometimes deeply personal. However, this claim is false and rests on a mis‐
understanding of the word privacy.
Having privacy does not mean keeping everything secret; it means having the free‐
dom to choose which things to reveal to whom, what to make public, and what to
keep secret. The right to privacy is a decision right: it enables each person to decide
where they want to be on the spectrum between secrecy and transparency in each sit‐
uation [99]. It is an important aspect of a person’s freedom and autonomy.
When data is extracted from people through surveillance infrastructure, privacy
rights are not necessarily eroded, but rather transferred to the data collector. Compa‐
nies that acquire data essentially say “trust us to do the right thing with your data,”
which means that the right to decide what to reveal and what to keep secret is trans‐
ferred from the individual to the company.
The companies in turn choose to keep much of the outcome of this surveillance
secret, because to reveal it would be perceived as creepy, and would harm their busi‐
ness model (which relies on knowing more about people than other companies do).
Intimate information about users is only revealed indirectly, for example in the form
of tools for targeting advertisements to specific groups of people (such as those suf‐
fering from a particular illness).
Doing the Right Thing 
| 
539


Even if particular users cannot be personally reidentified from the bucket of people
targeted by a particular ad, they have lost their agency about the disclosure of some
intimate information, such as whether they suffer from some illness. It is not the user
who decides what is revealed to whom on the basis of their personal preferences—it
is the company that exercises the privacy right with the goal of maximizing its profit.
Many companies have a goal of not being perceived as creepy—avoiding the question
of how intrusive their data collection actually is, and instead focusing on managing
user perceptions. And even these perceptions are often managed poorly: for example,
something may be factually correct, but if it triggers painful memories, the user may
not want to be reminded about it [100]. With any kind of data we should expect the
possibility that it is wrong, undesirable, or inappropriate in some way, and we need to
build mechanisms for handling those failures. Whether something is “undesirable” or
“inappropriate” is of course down to human judgment; algorithms are oblivious to
such notions unless we explicitly program them to respect human needs. As engi‐
neers of these systems we must be humble, accepting and planning for such failings.
Privacy settings that allow a user of an online service to control which aspects of their
data other users can see are a starting point for handing back some control to users.
However, regardless of the setting, the service itself still has unfettered access to the
data, and is free to use it in any way permitted by the privacy policy. Even if the ser‐
vice promises not to sell the data to third parties, it usually grants itself unrestricted
rights to process and analyze the data internally, often going much further than what
is overtly visible to users.
This kind of large-scale transfer of privacy rights from individuals to corporations is
historically unprecedented [99]. Surveillance has always existed, but it used to be
expensive and manual, not scalable and automated. Trust relationships have always
existed, for example between a patient and their doctor, or between a defendant and
their attorney—but in these cases the use of data has been strictly governed by ethical,
legal, and regulatory constraints. Internet services have made it much easier to amass
huge amounts of sensitive information without meaningful consent, and to use it at
massive scale without users understanding what is happening to their private data.
Data as assets and power
Since behavioral data is a byproduct of users interacting with a service, it is some‐
times called “data exhaust”—suggesting that the data is worthless waste material.
Viewed this way, behavioral and predictive analytics can be seen as a form of recy‐
cling that extracts value from data that would have otherwise been thrown away.
More correct would be to view it the other way round: from an economic point of
view, if targeted advertising is what pays for a service, then behavioral data about
people is the service’s core asset. In this case, the application with which the user
interacts is merely a means to lure users into feeding more and more personal infor‐
540 
| 
Chapter 12: The Future of Data Systems


mation into the surveillance infrastructure [99]. The delightful human creativity and
social relationships that often find expression in online services are cynically exploi‐
ted by the data extraction machine.
The assertion that personal data is a valuable asset is supported by the existence of
data brokers, a shady industry operating in secrecy, purchasing, aggregating, analyz‐
ing, inferring, and reselling intrusive personal data about people, mostly for market‐
ing purposes [90]. Startups are valued by their user numbers, by “eyeballs”—i.e., by
their surveillance capabilities.
Because the data is valuable, many people want it. Of course companies want it—
that’s why they collect it in the first place. But governments want to obtain it too: by
means of secret deals, coercion, legal compulsion, or simply stealing it [101]. When a
company goes bankrupt, the personal data it has collected is one of the assets that get
sold. Moreover, the data is difficult to secure, so breaches happen disconcertingly
often [102].
These observations have led critics to saying that data is not just an asset, but a “toxic
asset” [101], or at least “hazardous material” [103]. Even if we think that we are capa‐
ble of preventing abuse of data, whenever we collect data, we need to balance the ben‐
efits with the risk of it falling into the wrong hands: computer systems may be
compromised by criminals or hostile foreign intelligence services, data may be leaked
by insiders, the company may fall into the hands of unscrupulous management that
does not share our values, or the country may be taken over by a regime that has no
qualms about compelling us to hand over the data.
When collecting data, we need to consider not just today’s political environment, but
all possible future governments. There is no guarantee that every government elected
in future will respect human rights and civil liberties, so “it is poor civic hygiene to
install technologies that could someday facilitate a police state” [104].
“Knowledge is power,” as the old adage goes. And furthermore, “to scrutinize others
while avoiding scrutiny oneself is one of the most important forms of power” [105].
This is why totalitarian governments want surveillance: it gives them the power to
control the population. Although today’s technology companies are not overtly seek‐
ing political power, the data and knowledge they have accumulated nevertheless gives
them a lot of power over our lives, much of which is surreptitious, outside of public
oversight [106].
Remembering the Industrial Revolution
Data is the defining feature of the information age. The internet, data storage, pro‐
cessing, and software-driven automation are having a major impact on the global
economy and human society. As our daily lives and social organization have changed
in the past decade, and will probably continue to radically change in the coming dec‐
ades, comparisons to the Industrial Revolution come to mind [87, 96].
Doing the Right Thing 
| 
541


The Industrial Revolution came about through major technological and agricultural
advances, and it brought sustained economic growth and significantly improved liv‐
ing standards in the long run. Yet it also came with major problems: pollution of the
air (due to smoke and chemical processes) and the water (from industrial and human
waste) was dreadful. Factory owners lived in splendor, while urban workers often
lived in very poor housing and worked long hours in harsh conditions. Child labor
was common, including dangerous and poorly paid work in mines.
It took a long time before safeguards were established, such as environmental protec‐
tion regulations, safety protocols for workplaces, outlawing child labor, and health
inspections for food. Undoubtedly the cost of doing business increased when facto‐
ries could no longer dump their waste into rivers, sell tainted foods, or exploit work‐
ers. But society as a whole benefited hugely, and few of us would want to return to a
time before those regulations [87].
Just as the Industrial Revolution had a dark side that needed to be managed, our tran‐
sition to the information age has major problems that we need to confront and solve.
I believe that the collection and use of data is one of those problems. In the words of
Bruce Schneier [96]:
Data is the pollution problem of the information age, and protecting privacy is the
environmental challenge. Almost all computers produce information. It stays around,
festering. How we deal with it—how we contain it and how we dispose of it—is central
to the health of our information economy. Just as we look back today at the early deca‐
des of the industrial age and wonder how our ancestors could have ignored pollution
in their rush to build an industrial world, our grandchildren will look back at us during
these early decades of the information age and judge us on how we addressed the chal‐
lenge of data collection and misuse.
We should try to make them proud.
Legislation and self-regulation
Data protection laws might be able to help preserve individuals’ rights. For example,
the 1995 European Data Protection Directive states that personal data must be “col‐
lected for specified, explicit and legitimate purposes and not further processed in a
way incompatible with those purposes,” and furthermore that data must be “ade‐
quate, relevant and not excessive in relation to the purposes for which they are collec‐
ted” [107].
However, it is doubtful whether this legislation is effective in today’s internet context
[108]. These rules run directly counter to the philosophy of Big Data, which is to
maximize data collection, to combine it with other datasets, to experiment and to
explore in order to generate new insights. Exploration means using data for unfore‐
seen purposes, which is the opposite of the “specified and explicit” purposes for
which the user gave their consent (if we can meaningfully speak of consent at all
[109]). Updated regulations are now being developed [89].
542 
| 
Chapter 12: The Future of Data Systems


Companies that collect lots of data about people oppose regulation as being a burden
and a hindrance to innovation. To some extent that opposition is justified. For exam‐
ple, when sharing medical data, there are clear risks to privacy, but there are also
potential opportunities: how many deaths could be prevented if data analysis was
able to help us achieve better diagnostics or find better treatments [110]? Overregulation may prevent such breakthroughs. It is difficult to balance such potential
opportunities with the risks [105].
Fundamentally, I think we need a culture shift in the tech industry with regard to
personal data. We should stop regarding users as metrics to be optimized, and
remember that they are humans who deserve respect, dignity, and agency. We should
self-regulate our data collection and processing practices in order to establish and
maintain the trust of the people who depend on our software [111]. And we should
take it upon ourselves to educate end users about how their data is used, rather than
keeping them in the dark.
We should allow each individual to maintain their privacy—i.e., their control over
own data—and not steal that control from them through surveillance. Our individual
right to control our data is like the natural environment of a national park: if we
don’t explicitly protect and care for it, it will be destroyed. It will be the tragedy of the
commons, and we will all be worse off for it. Ubiquitous surveillance is not inevitable
—we are still able to stop it.
How exactly we might achieve this is an open question. To begin with, we should not
retain data forever, but purge it as soon as it is no longer needed [111, 112]. Purging
data runs counter to the idea of immutability (see “Limitations of immutability” on
page 463), but that issue can be solved. A promising approach I see is to enforce
access control through cryptographic protocols, rather than merely by policy [113,
114]. Overall, culture and attitude changes will be necessary. 
Summary
In this chapter we discussed new approaches to designing data systems, and I
included my personal opinions and speculations about the future. We started with
the observation that there is no one single tool that can efficiently serve all possible
use cases, and so applications necessarily need to compose several different pieces of
software to accomplish their goals. We discussed how to solve this data integration
problem by using batch processing and event streams to let data changes flow
between different systems.
In this approach, certain systems are designated as systems of record, and other data
is derived from them through transformations. In this way we can maintain indexes,
materialized views, machine learning models, statistical summaries, and more. By
making these derivations and transformations asynchronous and loosely coupled, a
Summary 
| 
543


problem in one area is prevented from spreading to unrelated parts of the system,
increasing the robustness and fault-tolerance of the system as a whole.
Expressing dataflows as transformations from one dataset to another also helps
evolve applications: if you want to change one of the processing steps, for example to
change the structure of an index or cache, you can just rerun the new transformation
code on the whole input dataset in order to rederive the output. Similarly, if some‐
thing goes wrong, you can fix the code and reprocess the data in order to recover.
These processes are quite similar to what databases already do internally, so we recast
the idea of dataflow applications as unbundling the components of a database, and
building an application by composing these loosely coupled components.
Derived state can be updated by observing changes in the underlying data. Moreover,
the derived state itself can further be observed by downstream consumers. We can
even take this dataflow all the way through to the end-user device that is displaying
the data, and thus build user interfaces that dynamically update to reflect data
changes and continue to work offline.
Next, we discussed how to ensure that all of this processing remains correct in the
presence of faults. We saw that strong integrity guarantees can be implemented scala‐
bly with asynchronous event processing, by using end-to-end operation identifiers to
make operations idempotent and by checking constraints asynchronously. Clients
can either wait until the check has passed, or go ahead without waiting but risk hav‐
ing to apologize about a constraint violation. This approach is much more scalable
and robust than the traditional approach of using distributed transactions, and fits
with how many business processes work in practice.
By structuring applications around dataflow and checking constraints asynchro‐
nously, we can avoid most coordination and create systems that maintain integrity
but still perform well, even in geographically distributed scenarios and in the pres‐
ence of faults. We then talked a little about using audits to verify the integrity of data
and detect corruption.
Finally, we took a step back and examined some ethical aspects of building dataintensive applications. We saw that although data can be used to do good, it can also
do significant harm: making justifying decisions that seriously affect people’s lives
and are difficult to appeal against, leading to discrimination and exploitation, nor‐
malizing surveillance, and exposing intimate information. We also run the risk of
data breaches, and we may find that a well-intentioned use of data has unintended
consequences.
As software and data are having such a large impact on the world, we engineers must
remember that we carry a responsibility to work toward the kind of world that we
want to live in: a world that treats people with humanity and respect. I hope that we
can work together toward that goal. 
544 
| 
Chapter 12: The Future of Data Systems


References
[1] Rachid Belaid: “Postgres Full-Text Search is Good Enough!,” rachbelaid.com, July
13, 2015.
[2] Philippe Ajoux, Nathan Bronson, Sanjeev Kumar, et al.: “Challenges to Adopting
Stronger Consistency at Scale,” at 15th USENIX Workshop on Hot Topics in Operat‐
ing Systems (HotOS), May 2015.
[3] Pat Helland and Dave Campbell: “Building on Quicksand,” at 4th Biennial Con‐
ference on Innovative Data Systems Research (CIDR), January 2009.
[4] Jessica Kerr: “Provenance and Causality in Distributed Systems,” blog.jessi‐
tron.com, September 25, 2016.
[5] Kostas Tzoumas: “Batch Is a Special Case of Streaming,” data-artisans.com, Sep‐
tember 15, 2015.
[6] Shinji Kim and Robert Blafford: “Stream Windowing Performance Analysis: Con‐
cord and Spark Streaming,” concord.io, July 6, 2016.
[7] Jay Kreps: “The Log: What Every Software Engineer Should Know About Real-
Time Data’s Unifying Abstraction,” engineering.linkedin.com, December 16, 2013.
[8] Pat Helland: “Life Beyond Distributed Transactions: An Apostate’s Opinion,” at
3rd Biennial Conference on Innovative Data Systems Research (CIDR), January 2007.
[9] “Great Western Railway (1835–1948),” Network Rail Virtual Archive, network‐
rail.co.uk.
[10] Jacqueline Xu: “Online Migrations at Scale,” stripe.com, February 2, 2017.
[11] Molly Bartlett Dishman and Martin Fowler: “Agile Architecture,” at O’Reilly
Software Architecture Conference, March 2015.
[12] Nathan Marz and James Warren: Big Data: Principles and Best Practices of Scala‐
ble Real-Time Data Systems. Manning, 2015. ISBN: 978-1-617-29034-3
[13] Oscar Boykin, Sam Ritchie, Ian O’Connell, and Jimmy Lin: “Summingbird: A
Framework for Integrating Batch and Online MapReduce Computations,” at 40th
International Conference on Very Large Data Bases (VLDB), September 2014.
[14] Jay Kreps: “Questioning the Lambda Architecture,” oreilly.com, July 2, 2014.
[15] Raul Castro Fernandez, Peter Pietzuch, Jay Kreps, et al.: “Liquid: Unifying Near‐
line and Offline Big Data Integration,” at 7th Biennial Conference on Innovative Data
Systems Research (CIDR), January 2015.
Summary 
| 
545


[16] Dennis M. Ritchie and Ken Thompson: “The UNIX Time-Sharing System,”
Communications of the ACM, volume 17, number 7, pages 365–375, July 1974. doi:
10.1145/361011.361061
[17] Eric A. Brewer and Joseph M. Hellerstein: “CS262a: Advanced Topics in Com‐
puter Systems,” lecture notes, University of California, Berkeley, cs.berkeley.edu,
August 2011.
[18] Michael Stonebraker: “The Case for Polystores,” wp.sigmod.org, July 13, 2015.
[19] Jennie Duggan, Aaron J. Elmore, Michael Stonebraker, et al.: “The BigDAWG
Polystore System,” ACM SIGMOD Record, volume 44, number 2, pages 11–16, June
2015. doi:10.1145/2814710.2814713
[20] Patrycja Dybka: “Foreign Data Wrappers for PostgreSQL,” vertabelo.com, March
24, 2015.
[21] David B. Lomet, Alan Fekete, Gerhard Weikum, and Mike Zwilling: “Unbun‐
dling Transaction Services in the Cloud,” at 4th Biennial Conference on Innovative
Data Systems Research (CIDR), January 2009.
[22] Martin Kleppmann and Jay Kreps: “Kafka, Samza and the Unix Philosophy of
Distributed Data,” IEEE Data Engineering Bulletin, volume 38, number 4, pages 4–14,
December 2015.
[23] John Hugg: “Winning Now and in the Future: Where VoltDB Shines,”
voltdb.com, March 23, 2016.
[24] Frank McSherry, Derek G. Murray, Rebecca Isaacs, and Michael Isard: “Differ‐
ential Dataflow,” at 6th Biennial Conference on Innovative Data Systems Research
(CIDR), January 2013.
[25] Derek G Murray, Frank McSherry, Rebecca Isaacs, et al.: “Naiad: A Timely Data‐
flow System,” at 24th ACM Symposium on Operating Systems Principles (SOSP),
pages 439–455, November 2013. doi:10.1145/2517349.2522738
[26] Gwen Shapira: “We have a bunch of customers who are implementing ‘database
inside-out’ concept and they all ask ‘is anyone else doing it? are we crazy?’” twit‐
ter.com, July 28, 2016.
[27] Martin Kleppmann: “Turning the Database Inside-out with Apache Samza,” at
Strange Loop, September 2014.
[28] Peter Van Roy and Seif Haridi: Concepts, Techniques, and Models of Computer
Programming. MIT Press, 2004. ISBN: 978-0-262-22069-9
[29] “Juttle Documentation,” juttle.github.io, 2016.
546 
| 
Chapter 12: The Future of Data Systems


[30] Evan Czaplicki and Stephen Chong: “Asynchronous Functional Reactive Pro‐
gramming for GUIs,” at 34th ACM SIGPLAN Conference on Programming Language
Design and Implementation (PLDI), June 2013. doi:10.1145/2491956.2462161
[31] Engineer Bainomugisha, Andoni Lombide Carreton, Tom van Cutsem, Stijn
Mostinckx, and Wolfgang de Meuter: “A Survey on Reactive Programming,” ACM
Computing Surveys, volume 45, number 4, pages 1–34, August 2013. doi:
10.1145/2501654.2501666
[32] Peter Alvaro, Neil Conway, Joseph M. Hellerstein, and William R. Marczak:
“Consistency Analysis in Bloom: A CALM and Collected Approach,” at 5th Biennial
Conference on Innovative Data Systems Research (CIDR), January 2011.
[33] Felienne Hermans: “Spreadsheets Are Code,” at Code Mesh, November 2015.
[34] Dan Bricklin and Bob Frankston: “VisiCalc: Information from Its Creators,”
danbricklin.com.
[35] D. Sculley, Gary Holt, Daniel Golovin, et al.: “Machine Learning: The High-
Interest Credit Card of Technical Debt,” at NIPS Workshop on Software Engineering
for Machine Learning (SE4ML), December 2014.
[36] Peter Bailis, Alan Fekete, Michael J Franklin, et al.: “Feral Concurrency Control:
An Empirical Investigation of Modern Application Integrity,” at ACM International
Conference 
on 
Management 
of 
Data 
(SIGMOD), 
June 
2015. 
doi:
10.1145/2723372.2737784
[37] Guy Steele: “Re: Need for Macros (Was Re: Icon),” email to ll1-discuss mailing
list, people.csail.mit.edu, December 24, 2001.
[38] David Gelernter: “Generative Communication in Linda,” ACM Transactions on
Programming Languages and Systems (TOPLAS), volume 7, number 1, pages 80–112,
January 1985. doi:10.1145/2363.2433
[39] Patrick Th. Eugster, Pascal A. Felber, Rachid Guerraoui, and Anne-Marie Ker‐
marrec: “The Many Faces of Publish/Subscribe,” ACM Computing Surveys, volume
35, number 2, pages 114–131, June 2003. doi:10.1145/857076.857078
[40] Ben Stopford: “Microservices in a Streaming World,” at QCon London, March
2016.
[41] Christian Posta: “Why Microservices Should Be Event Driven: Autonomy vs
Authority,” blog.christianposta.com, May 27, 2016.
[42] Alex Feyerke: “Say Hello to Offline First,” hood.ie, November 5, 2013.
[43] Sebastian Burckhardt, Daan Leijen, Jonathan Protzenko, and Manuel Fähndrich:
“Global Sequence Protocol: A Robust Abstraction for Replicated Shared State,” at
Summary 
| 
547


29th European Conference on Object-Oriented Programming (ECOOP), July 2015.
doi:10.4230/LIPIcs.ECOOP.2015.568
[44] Mark Soper: “Clearing Up React Data Management Confusion with Flux, Redux,
and Relay,” medium.com, December 3, 2015.
[45] Eno Thereska, Damian Guy, Michael Noll, and Neha Narkhede: “Unifying
Stream Processing and Interactive Queries in Apache Kafka,” confluent.io, October
26, 2016.
[46] Frank McSherry: “Dataflow as Database,” github.com, July 17, 2016.
[47] Peter Alvaro: “I See What You Mean,” at Strange Loop, September 2015.
[48] Nathan Marz: “Trident: A High-Level Abstraction for Realtime Computation,”
blog.twitter.com, August 2, 2012.
[49] Edi Bice: “Low Latency Web Scale Fraud Prevention with Apache Samza, Kafka
and Friends,” at Merchant Risk Council MRC Vegas Conference, March 2016.
[50] Charity Majors: “The Accidental DBA,” charity.wtf, October 2, 2016.
[51] Arthur J. Bernstein, Philip M. Lewis, and Shiyong Lu: “Semantic Conditions for
Correctness at Different Isolation Levels,” at 16th International Conference on Data
Engineering (ICDE), February 2000. doi:10.1109/ICDE.2000.839387
[52] Sudhir Jorwekar, Alan Fekete, Krithi Ramamritham, and S. Sudarshan: “Auto‐
mating the Detection of Snapshot Isolation Anomalies,” at 33rd International Confer‐
ence on Very Large Data Bases (VLDB), September 2007.
[53] Kyle Kingsbury: Jepsen blog post series, aphyr.com, 2013–2016.
[54] Michael Jouravlev: “Redirect After Post,” theserverside.com, August 1, 2004.
[55] Jerome H. Saltzer, David P. Reed, and David D. Clark: “End-to-End Arguments
in System Design,” ACM Transactions on Computer Systems, volume 2, number 4,
pages 277–288, November 1984. doi:10.1145/357401.357402
[56] Peter Bailis, Alan Fekete, Michael J. Franklin, et al.: “Coordination-Avoiding
Database Systems,” Proceedings of the VLDB Endowment, volume 8, number 3, pages
185–196, November 2014.
[57] Alex Yarmula: “Strong Consistency in Manhattan,” blog.twitter.com, March 17,
2016.
[58] Douglas B Terry, Marvin M Theimer, Karin Petersen, et al.: “Managing Update
Conflicts in Bayou, a Weakly Connected Replicated Storage System,” at 15th ACM
Symposium on Operating Systems Principles (SOSP), pages 172–182, December 1995.
doi:10.1145/224056.224070
548 
| 
Chapter 12: The Future of Data Systems


[59] Jim Gray: “The Transaction Concept: Virtues and Limitations,” at 7th Interna‐
tional Conference on Very Large Data Bases (VLDB), September 1981.
[60] Hector Garcia-Molina and Kenneth Salem: “Sagas,” at ACM International Con‐
ference on Management of Data (SIGMOD), May 1987. doi:10.1145/38713.38742
[61] Pat Helland: “Memories, Guesses, and Apologies,” blogs.msdn.com, May 15,
2007.
[62] Yoongu Kim, Ross Daly, Jeremie Kim, et al.: “Flipping Bits in Memory Without
Accessing Them: An Experimental Study of DRAM Disturbance Errors,” at 41st
Annual International Symposium on Computer Architecture (ISCA), June 2014. doi:
10.1145/2678373.2665726
[63] Mark Seaborn and Thomas Dullien: “Exploiting the DRAM Rowhammer Bug to
Gain Kernel Privileges,” googleprojectzero.blogspot.co.uk, March 9, 2015.
[64] Jim N. Gray and Catharine van Ingen: “Empirical Measurements of Disk Failure
Rates and Error Rates,” Microsoft Research, MSR-TR-2005-166, December 2005.
[65] Annamalai Gurusami and Daniel Price: “Bug #73170: Duplicates in Unique Sec‐
ondary Index Because of Fix of Bug#68021,” bugs.mysql.com, July 2014.
[66] Gary Fredericks: “Postgres Serializability Bug,” github.com, September 2015.
[67] Xiao Chen: “HDFS DataNode Scanners and Disk Checker Explained,” blog.clou‐
dera.com, December 20, 2016.
[68] Jay Kreps: “Getting Real About Distributed System Reliability,” blog.empathy‐
box.com, March 19, 2012.
[69] Martin Fowler: “The LMAX Architecture,” martinfowler.com, July 12, 2011.
[70] Sam Stokes: “Move Fast with Confidence,” blog.samstokes.co.uk, July 11, 2016.
[71] “Sawtooth Lake Documentation,” Intel Corporation, intelledger.github.io, 2016.
[72] Richard Gendal Brown: “Introducing R3 Corda™: A Distributed Ledger
Designed for Financial Services,” gendal.me, April 5, 2016.
[73] Trent McConaghy, Rodolphe Marques, Andreas Müller, et al.: “BigchainDB: A
Scalable Blockchain Database,” bigchaindb.com, June 8, 2016.
[74] Ralph C. Merkle: “A Digital Signature Based on a Conventional Encryption
Function,” at CRYPTO ’87, August 1987. doi:10.1007/3-540-48184-2_32
[75] Ben Laurie: “Certificate Transparency,” ACM Queue, volume 12, number 8,
pages 10-19, August 2014. doi:10.1145/2668152.2668154
Summary 
| 
549


[76] Mark D. Ryan: “Enhanced Certificate Transparency and End-to-End Encrypted
Mail,” at Network and Distributed System Security Symposium (NDSS), February
2014. doi:10.14722/ndss.2014.23379
[77] “Software Engineering Code of Ethics and Professional Practice,” Association for
Computing Machinery, acm.org, 1999.
[78] François Chollet: “Software development is starting to involve important ethical
choices,” twitter.com, October 30, 2016.
[79] Igor Perisic: “Making Hard Choices: The Quest for Ethics in Machine Learning,”
engineering.linkedin.com, November 2016.
[80] John Naughton: “Algorithm Writers Need a Code of Conduct,” theguar‐
dian.com, December 6, 2015.
[81] Logan Kugler: “What Happens When Big Data Blunders?,” Communications of
the ACM, volume 59, number 6, pages 15–16, June 2016. doi:10.1145/2911975
[82] Bill Davidow: “Welcome to Algorithmic Prison,” theatlantic.com, February 20,
2014.
[83] Don Peck: “They’re Watching You at Work,” theatlantic.com, December 2013.
[84] Leigh Alexander: “Is an Algorithm Any Less Racist Than a Human?” theguar‐
dian.com, August 3, 2016.
[85] Jesse Emspak: “How a Machine Learns Prejudice,” scientificamerican.com,
December 29, 2016.
[86] Maciej Cegłowski: “The Moral Economy of Tech,” idlewords.com, June 2016.
[87] Cathy O’Neil: Weapons of Math Destruction: How Big Data Increases Inequality
and Threatens Democracy. Crown Publishing, 2016. ISBN: 978-0-553-41881-1
[88] Julia Angwin: “Make Algorithms Accountable,” nytimes.com, August 1, 2016.
[89] Bryce Goodman and Seth Flaxman: “European Union Regulations on Algorith‐
mic Decision-Making and a ‘Right to Explanation’,” arXiv:1606.08813, August 31,
2016.
[90] “A Review of the Data Broker Industry: Collection, Use, and Sale of Consumer
Data for Marketing Purposes,” Staff Report, United States Senate Committee on Com‐
merce, Science, and Transportation, commerce.senate.gov, December 2013.
[91] Olivia Solon: “Facebook’s Failure: Did Fake News and Polarized Politics Get
Trump Elected?” theguardian.com, November 10, 2016.
[92] Donella H. Meadows and Diana Wright: Thinking in Systems: A Primer. Chelsea
Green Publishing, 2008. ISBN: 978-1-603-58055-7
550 
| 
Chapter 12: The Future of Data Systems


[93] Daniel J. Bernstein: “Listening to a ‘big data’/‘data science’ talk,” twitter.com,
May 12, 2015.
[94] Marc Andreessen: “Why Software Is Eating the World,” The Wall Street Journal,
20 August 2011.
[95] J. M. Porup: “‘Internet of Things’ Security Is Hilariously Broken and Getting
Worse,” arstechnica.com, January 23, 2016.
[96] Bruce Schneier: Data and Goliath: The Hidden Battles to Collect Your Data and
Control Your World. W. W. Norton, 2015. ISBN: 978-0-393-35217-7
[97] The Grugq: “Nothing to Hide,” grugq.tumblr.com, April 15, 2016.
[98] Tony Beltramelli: “Deep-Spying: Spying Using Smartwatch and Deep Learning,”
Masters Thesis, IT University of Copenhagen, December 2015. Available at
arxiv.org/abs/1512.05616
[99] Shoshana Zuboff: “Big Other: Surveillance Capitalism and the Prospects of an
Information Civilization,” Journal of Information Technology, volume 30, number 1,
pages 75–89, April 2015. doi:10.1057/jit.2015.5
[100] Carina C. Zona: “Consequences of an Insightful Algorithm,” at GOTO Berlin,
November 2016.
[101] Bruce Schneier: “Data Is a Toxic Asset, So Why Not Throw It Out?,” schne‐
ier.com, March 1, 2016.
[102] John E. Dunn: “The UK’s 15 Most Infamous Data Breaches,” techworld.com,
November 18, 2016.
[103] Cory Scott: “Data is not toxic - which implies no benefit - but rather hazardous
material, where we must balance need vs. want,” twitter.com, March 6, 2016.
[104] Bruce Schneier: “Mission Creep: When Everything Is Terrorism,” schneier.com,
July 16, 2013.
[105] Lena Ulbricht and Maximilian von Grafenstein: “Big Data: Big Power Shifts?,”
Internet Policy Review, volume 5, number 1, March 2016. doi:10.14763/2016.1.406
[106] Ellen P. Goodman and Julia Powles: “Facebook and Google: Most Powerful and
Secretive Empires We’ve Ever Known,” theguardian.com, September 28, 2016.
[107] Directive 95/46/EC on the protection of individuals with regard to the process‐
ing of personal data and on the free movement of such data, Official Journal of the
European Communities No. L 281/31, eur-lex.europa.eu, November 1995.
[108] Brendan Van Alsenoy: “Regulating Data Protection: The Allocation of Respon‐
sibility and Risk Among Actors Involved in Personal Data Processing,” Thesis, KU
Leuven Centre for IT and IP Law, August 2016.
Summary 
| 
551


[109] Michiel Rhoen: “Beyond Consent: Improving Data Protection Through Con‐
sumer Protection Law,” Internet Policy Review, volume 5, number 1, March 2016. doi:
10.14763/2016.1.404
[110] Jessica Leber: “Your Data Footprint Is Affecting Your Life in Ways You Can’t
Even Imagine,” fastcoexist.com, March 15, 2016.
[111] Maciej Cegłowski: “Haunted by Data,” idlewords.com, October 2015.
[112] Sam Thielman: “You Are Not What You Read: Librarians Purge User Data to
Protect Privacy,” theguardian.com, January 13, 2016.
[113] Conor Friedersdorf: “Edward Snowden’s Other Motive for Leaking,” theatlan‐
tic.com, May 13, 2014.
[114] Phillip Rogaway: “The Moral Character of Cryptographic Work,” Cryptology
ePrint 2015/1162, December 2015.
552 
| 
Chapter 12: The Future of Data Systems

## Examples & Scenarios

- of your data. When new data comes in, e.g., as user input, it is first written here.
Each fact is represented exactly once (the representation is typically normalized).
If there is any discrepancy between another system and the system of record,
then the value in the system of record is (by definition) the correct one.
Derived data systems
Data in a derived system is the result of taking some existing data from another
system and transforming or processing it in some way. If you lose derived data,
you can recreate it from the original source. A classic example is a cache: data can
be served from the cache if present, but if the cache doesn’t contain what you
need, you can fall back to the underlying database. Denormalized values, indexes,

- ish. Instead, batch jobs are often scheduled to run periodically (for example, once
a day). The primary performance measure of a batch job is usually throughput
(the time it takes to crunch through an input dataset of a certain size). We dis‐
cuss batch processing in this chapter.
Stream processing systems (near-real-time systems)
Stream processing is somewhere between online and offline/batch processing (so
it is sometimes called near-real-time or nearline processing). Like a batch pro‐
cessing system, a stream processor consumes inputs and produces outputs
(rather than responding to requests). However, a stream job operates on events
shortly after they happen, whereas a batch job operates on a fixed set of input

- quest to build reliable, scalable, and maintainable applications. For example, Map‐
Reduce, a batch processing algorithm published in 2004 [1], was (perhaps overenthusiastically) called “the algorithm that makes Google so massively scalable” [2]. It
was subsequently implemented in various open source data systems, including
Hadoop, CouchDB, and MongoDB.
MapReduce is a fairly low-level programming model compared to the parallel pro‐
cessing systems that were developed for data warehouses many years previously [3,
4], but it was a major step forward in terms of the scale of processing that could be
achieved on commodity hardware. Although the importance of MapReduce is now
declining [5], it is still worth understanding, because it provides a clear picture of
why and how batch processing is useful.

- log file every time it serves a request. For example, using the nginx default access log
format, one line of the log might look like this:
216.58.210.78 - - [27/Feb/2015:17:55:11 +0000] "GET /css/typography.css HTTP/1.1"
200 3377 "http://martin.kleppmann.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X
10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115
Safari/537.36"
(That is actually one line; it’s only broken onto multiple lines here for readability.)
There’s a lot of information in that line. In order to interpret it, you need to look at
the definition of the log format, which is as follows:
$remote_addr - $remote_user [$time_local] "$request"

- same thing. For example, in Ruby, it might look something like this:
392
|
Chapter 10: Batch Processing

- making the web the success that it is today. Prior systems were not so uniform: for example, in the era of
bulletin board systems (BBSs), each system had its own phone number and baud rate configuration. A refer‐
ence from one BBS to another would have to be in the form of a phone number and modem settings; the user
would have to hang up, dial the other BBS, and then manually find the information they were looking for. It
wasn’t possible to link directly to some piece of content inside another BBS.
The sort tool is a great example of a program that does one thing well. It is arguably
a better sorting implementation than most programming languages have in their
standard libraries (which do not spill to disk and do not use multiple threads, even
when that would be beneficial). And yet, sort is barely useful in isolation. It only
becomes powerful in combination with the other Unix tools, such as uniq.

- example:
1. Read a set of input files, and break it up into records. In the web server log exam‐
ple, each record is one line in the log (that is, \n is the record separator).
2. Call the mapper function to extract a key and value from each input record. In
the preceding example, the mapper function is awk '{print $7}': it extracts the
URL ($7) as the key, and leaves the value empty.
3. Sort all of the key-value pairs by key. In the log example, this is done by the first
sort command.
4. Call the reducer function to iterate over the sorted key-value pairs. If there are
multiple occurrences of the same key, the sorting has made them adjacent in the

- first copies the code (e.g., JAR files in the case of a Java program) to the appropriate
machines. It then starts the map task and begins reading the input file, passing one
record at a time to the mapper callback. The output of the mapper consists of keyvalue pairs.
The reduce side of the computation is also partitioned. While the number of map
tasks is determined by the number of input file blocks, the number of reduce tasks is
configured by the job author (it can be different from the number of map tasks). To
ensure that all key-value pairs with the same key end up at the same reducer, the
framework uses a hash of the key to determine which reduce task should receive a
particular key-value pair (see “Partitioning by Hash of Key” on page 203).
The key-value pairs must be sorted, but the dataset is likely too large to be sorted with

- occurrences of some association within a dataset. For example, we assume that a job
is processing the data for all users simultaneously, not merely looking up the data for
one particular user (which would be done far more efficiently with an index).
Example: analysis of user activity events
A typical example of a join in a batch job is illustrated in Figure 10-2. On the left is a
log of events describing the things that logged-in users did on a website (known as
activity events or clickstream data), and on the right is a database of users. You can
think of this example as being part of a star schema (see “Stars and Snowflakes: Sche‐
mas for Analytics” on page 93): the log of events is the fact table, and the user data‐
base is one of the dimensions.

- for example, if the profile contains the user’s age or date of birth, the system could
determine which pages are most popular with which age groups. However, the activ‐
ity events contain only the user ID, not the full user profile information. Embedding
that profile information in every single activity event would most likely be too waste‐
ful. Therefore, the activity events need to be joined with the user profile database.
The simplest implementation of this join would go over the activity events one by
one and query the user database (on a remote server) for every user ID it encounters.
This is possible, but it would most likely suffer from very poor performance: the pro‐
cessing throughput would be limited by the round-trip time to the database server,
the effectiveness of a local cache would depend very much on the distribution of data,

- Thus, a better approach would be to take a copy of the user database (for example,
extracted from a database backup using an ETL process—see “Data Warehousing” on
page 91) and to put it in the same distributed filesystem as the log of user activity
events. You would then have the user database in one set of files in HDFS and the
user activity records in another set of files, and could use MapReduce to bring
together all of the relevant records in the same place and process them efficiently.
Sort-merge joins
Recall that the purpose of the mapper is to extract a key and value from each input
record. In the case of Figure 10-2, this key would be the user ID: one set of mappers
would go over the activity events (extracting the user ID as the key and the activity

- cess called sessionization [37]. For example, such analysis could be used to work out
whether users who were shown a new version of your website are more likely to make
a purchase than those who were shown the old version (A/B testing), or to calculate
whether some marketing activity is worthwhile.
If you have multiple web servers handling user requests, the activity events for a par‐
ticular user are most likely scattered across various different servers’ log files. You can
implement sessionization by using a session cookie, user ID, or similar identifier as
the grouping key and bringing all the activity events for a particular user together in
one place, while distributing different users’ events across different partitions.
Handling skew

- down if there is a very large amount of data related to a single key. For example, in a
social network, most users might be connected to a few hundred people, but a small
number of celebrities may have many millions of followers. Such disproportionately
active database records are known as linchpin objects [38] or hot keys.
Collecting all activity related to a celebrity (e.g., replies to something they posted) in a
single reducer can lead to significant skew (also known as hot spots)—that is, one
reducer that must process significantly more records than the others (see “Skewed
Workloads and Relieving Hot Spots” on page 205). Since a MapReduce job is only
complete when all of its mappers and reducers have completed, any subsequent jobs
must wait for the slowest reducer to complete before they can start.

- For example, the skewed join method in Pig first runs a sampling job to determine
which keys are hot [39]. When performing the actual join, the mappers send any
MapReduce and Distributed Filesystems
|
407

- For example, imagine in the case of Figure 10-2 that the user database is small
enough to fit in memory. In this case, when a mapper starts up, it can first read the
user database from the distributed filesystem into an in-memory hash table. Once
this is done, the mapper can scan over the user activity events and simply look up the
user ID for each event in the hash table.vi
There can still be several map tasks: one for each file block of the large input to the
join (in the example of Figure 10-2, the activity events are the large input). Each of
these mappers loads the small input entirely into memory.
This simple but effective algorithm is called a broadcast hash join: the word broadcast
reflects the fact that each mapper for a partition of the large input reads the entirety

- side). For example, mapper 3 first loads all users with an ID ending in 3 into a hash
table, and then scans over all the activity events for each user whose ID ends in 3.
If the partitioning is done correctly, you can be sure that all the records you might
want to join are located in the same numbered partition, and so it is sufficient for
each mapper to only read one partition from each of the input datasets. This has the
advantage that each mapper can load a smaller amount of data into its hash table.
MapReduce and Distributed Filesystems
|
409

- using indexes, in order to present them to a user (for example, on a web page). On
the other hand, analytic queries often scan over a large number of records, perform‐
ing groupings and aggregations, and the output often has the form of a report: a
graph showing the change in a metric over time, or the top 10 items according to
some ranking, or a breakdown of some quantity into subcategories. The consumer of
such a report is often an analyst or a manager who needs to make business decisions.
Where does batch processing fit in? It is not transaction processing, nor is it analyt‐
ics. It is closer to analytics, in that a batch process typically scans over large portions
of an input dataset. However, a workflow of MapReduce jobs is not the same as a
SQL query used for analytic purposes (see “Comparing Hadoop to Distributed Data‐

- systems such as classifiers (e.g., spam filters, anomaly detection, image recognition)
and recommendation systems (e.g., people you may know, products you may be
interested in, or related searches [29]).
The output of those batch jobs is often some kind of database: for example, a data‐
base that can be queried by user ID to obtain suggested friends for that user, or a
database that can be queried by product ID to get a list of related products [45].
These databases need to be queried from the web application that handles user
requests, which is usually separate from the Hadoop infrastructure. So how does the
output from the batch process get back into a database where the web application can
query it?

- the expected characteristics (for example, by comparing it to the output from the
previous run and measuring discrepancies).
• Like Unix tools, MapReduce jobs separate logic from wiring (configuring the
input and output directories), which provides a separation of concerns and ena‐
bles potential reuse of code: one team can focus on implementing a job that does
one thing well, while other teams can decide where and when to run that job.
In these areas, the design principles that worked well for Unix also seem to be work‐
ing well for Hadoop—but Unix and Hadoop also differ in some ways. For example,
because most Unix tools assume untyped text files, they have to do a lot of input
parsing (our log analysis example at the beginning of the chapter used {print $7} to

- (MPP) databases more than a decade previously [3, 40]. For example, the Gamma
database machine, Teradata, and Tandem NonStop SQL were pioneers in this area
[52].
The biggest difference is that MPP databases focus on parallel execution of analytic
SQL queries on a cluster of machines, while the combination of MapReduce and a
distributed filesystem [19] provides something much more like a general-purpose
operating system that can run arbitrary programs.
Diversity of storage
Databases require you to structure data according to a particular model (e.g., rela‐
tional or documents), whereas files in a distributed filesystem are just byte sequences,

## Key Takeaways

- Report MSR-TR-2003-24, March 2003.
[28] Márton Trencséni: “Luigi vs Airflow vs Pinball,” bytepawn.com, February 6,
2016.
[29] Roshan Sumbaly, Jay Kreps, and Sam Shah: “The ‘Big Data’ Ecosystem at
LinkedIn,” at ACM International Conference on Management of Data (SIGMOD),
July 2013. doi:10.1145/2463676.2463707

