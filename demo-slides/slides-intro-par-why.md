# Slide intro par why

## slide 1-2 

Hello! This is Erik from UNC Charlotte and today we will be talking
about parallel computing.

Parallel computing is a set of techniques to accelerate the execution
of a program by using multiple processing units simultaneously.

Today, we will see why almost all modern computing systems contain
multiple processing units.

We will also see the different common forms that parallel computing
can take on modern systems.


## slide 3

You may already be familiar with a related concept called concurrency.

There is concurrency in a system when multiple processes are running at
the same time and are working together to achieve a common goal.

Typically, the primary concern in a concurrent system is to ensure
that all possible executions of the system are correct, in the sense
that the execution achieves the property that one is trying to achieve.

While you may have programmed concurrent computing systems before,
possibly with threads, concurrency can be found in many common human
activities.

## Slide 4

Think for instance of the US postal system. 

Multiple customers drop their mail in designated collection box, or
give them to a postal worker.

The mail gets aggregated in bins and brought to one of many sorting
stations in the country.

The mail then gets routed to the appropriate post office where it is
placed in postal delivery trucks.

Finally, mail-carriers will drive around town to place the mail in the
appropriate mailboxes.

The US postal system is fundamentally a concurrent system with many
actors working to achieve mail delivery.

If the different actors do not work together, concurrency problems can
arise in the sense that mail can get lost.

## Slide 5

While in a concurrent system, the primary concern is correctness, a
parallel system employs multiple processing units to shorten the time
it takes to perform a task.

The concerns in a parallel system is to identify which computations can
be done in parallel, that is to say which computations can be done at
the same time by different processors.

Then these computations are organized and given to the different
processors at appropriate times to accelerate the execution of a task.

Obviously, parallel systems *are* concurrent systems, but the goal of
a parallel system is not only to be correct, but also to be fast.

## Slide 6

Think for instance of asking a team to build a house.

There are certainly concurrency issues, in the sense that one has to
lay a concrete slab before being able to build the frame of the house,
or that one has to install insulation before putting up a dry wall.

But some tasks are more important than others if the goal is to build
a house quickly.

Delaying setting up insulation will prevent drywall from being
installed which makes it a more urgent task than painting the outside
of the house which can be done at anytime.

## Slide 7

There are multiple reasons why parallel computing has become the norm
in computing systems.

One of them is the end of Dennard scaling.

In 1974, Dennard remarked that as transistors get smaller their power
density stays constant.

In other words, as transistors shrink they use less power.

The gains in power consumption from transistors shrinking can then be
used to increase the frequency at which CPUs operate.

Dennard scaling is one of the primary reason why through the 80s and
90s CPUs were getting *twice faster* every 18 months.

An emphasis in the tech industry at the time was to increase
programmer productivity rather than the performance of applications.

Unfortunately, Dennard scaling ended around 2005 and we could no longer
increase CPU frequencies without also increasing power consumption.

## Slide 8

Though, can we just keep increasing CPU frequencies without benefiting
from Dennard scaling?

In short, not really!

At the moment, the power consumption of a CPU is linear of the
square of the voltage and linear in the frequency of the processors.

Though, to be able to increase frequency, one also has to raise the
voltage.

In practice, the power consumption of a CPU grows with about the
square or the cube of the frequency.

What it means is that practically, doubling the frequency of a CPU
costs as much power as operating four CPUs.

So arbitrarily increasing CPU frequencies is not economical!

And the industry started to increase the number of CPUs in systems, or
the number of cores in the CPUs.

## Slide 9

Looking at historical trends, there used to be only a single core in
CPUs until about 2005. 

The increase in CPU frequency and single threaded performance started
to slow around 2005.

The capping of CPU frequency coupled with the introduction of more
cores enabled to increase the processing capabilities of CPUs while
keeping power consumption in check.

This is why we see nowadays CPUs with dozens of cores.

Even CPUs in laptops have more than two cores.

The CPU in your cell phone most likely has more than four cores.

Virtually, all CPUs used in modern computing are multi-core CPUs.

There are still some single core systems out there, but these are
usually for specialty applications.

## Slide 10

An other reason why parallel computing has become inevitable is that
many modern problems are just too big to be computed on a single
machine.

There are technological limits to the amount of memory a single
machine can have. 

Laptops rarely have more than 8GB of main memory.

Desktops rarely have more than 64GB of main memory.

And servers usually do not have more than 4TB of memory.

What options are there to process a problem that requires more memory
than a single machine has?

One could give up on computing it; but that is often unacceptable.

One could program better to reduce the memory usage of the application
but that may not be feasible.

One could use external memory, for instance by swapping to a hard
drive, but that is usually slow.

Or, one could leverage parallel computing and use multiple computers
to complete the task


## slide 11

Also, the usefulness of a computation may decrease if it can not be
performed quickly.

The quicker a vaccine for COVID-19 could be developed, the more lives
could be saved.

If one wants to forecast the weather of tomorrow, it is only useful if
the computation can be finished before tomorrow.

In a video game, one needs to render a frame within 16 milliseconds
to be able to sustain 60 frames per second.

Parallel computing is a practical tool to reduce the time it takes to
perform a computation.

## slide 12

There are five main forms of parallelism in modern computing systems.

All the calculation performed at the circuit level are parallel.

For instance, while executing a binary OR, the bits of the two
operands are compared simultaneously.

Also, modern SIMD instructions can perform up to 16 additions
simultaneously.

## slide 13

Also, most modern CPUs are super scalar, in that a single core can
typically execute more than one instruction at a time.

Modern Intel cores can execute up to six instructions in a single cycle.

## slide 14

Shared memory parallelism is the form of parallelism you are probably
the most familiar with.

It consists in using different cores to execute a single program
within a shared memory space.

Shared memory machines are typically programmed using threads, and
concurrency issues are the most common problems.

## slide 15

Distributed memory parallelism consists in using multiple nodes; each
of which having its own memory space.

The problem in distributed memory programming is often to reduce the
amount of communication between the nodes.

This is the form of parallelism that is usually leveraged for big data
processing and the form of parallelism that is usually associated with
cluster computing and cloud computing.

## slide 16

Most modern systems are equipped with accelerators such as GPUs and
FPGAs.

These accelerators are typically built to improve the performance of a
particular workload.

GPUs, for instance, are particularly suited to improve the performance
of geometric operations and most linear algebra kernels.

While accelerators are usually parallel machines themselves, the most
performance is usually obtained by intelligently distributing the
calculation between the CPU and the accelerator.

While circuit-level parallelism and instruction-level parallelism are
forms of parallel computing, they are usually left for the processor
architect and the compiler designer to take care of.

Shared memory, distributed memory, and accelerators are the typical
forms of parallelism leveraged by developers.

## Conclusion

Today, we have differenciated concurrency from parallelism.

We saw that the end of Dennard scaling caused the design of modern
multi-core systems and that some problems are just too large to be
processed on a single machine.

While there are five common forms of parallelism, programmers usually
design parallel applications by working with shared memory systems,
distributed memory systems, and accelerators.
