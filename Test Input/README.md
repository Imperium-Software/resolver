## SAT Instances

The paper uses certain SAT instances from the SAT2002 competition and from random instance generators.

All instances for the SAT2002 competition can be downloaded [here](http://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/New/Competition-02/sat-2002-beta.tgz) (140MB). Alternatively, the instances are available individually at the [DIMACS FTP site](ftp://dimacs.rutgers.edu/pub/challenge/satisfiability/benchmarks/cnf/).

### Comparison

Section 7.1.2 of the paper presents a comparison between GASAT and FlipGA. We can use these results to compare our solver to the authors' implementation. Only average number of false clauses for the best individual over 20 runs is compared.


| Instance | avg. f.c. (Paper Results) | avg. f.c. (Our Results) |
|:---:|:---:|:---:|
|par16-4-c.3SAT |5.85||
|mat25.shuffled.3SAT|7.60||
|mat26.shuffled.3SAT|8.00||
|par32-5-c.3SAT|19.60||
|3blocks.3SAT|5.25||
|difp_19_0_arr_rcr.3SAT|84.25||
|difp_19_99_arr_rcr.3SAT|81.40||
|par32-5.3SAT|41.25||
|color-10-3.3SAT|46.53||
|color-18-4.3SAT|248.50||


### Other Resources

 - A nice explanation of the DIMACS format and some sample CNF files can be found [here](http://people.sc.fsu.edu/%7Ejburkardt/data/cnf/cnf.html)
