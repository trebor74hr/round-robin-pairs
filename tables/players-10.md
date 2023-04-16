# Round-robin pairs for 10 players

NOTE: **Currently ideal solution not available - issue with first schedule.**

## Berger

```
Round            1        2        3        4        5
------------------------------------------------------
Round   1:   1- 10    2-  9    3-  8    4-  7    5-  6
Round   2:  10-  6    7-  5    8-  4    9-  3    1-  2
Round   3:   2- 10    3-  1    4-  9    5-  8    6-  7
Round   4:  10-  7    8-  6    9-  5    1-  4    2-  3
Round   5:   3- 10    4-  2    5-  1    6-  9    7-  8
Round   6:  10-  8    9-  7    1-  6    2-  5    3-  4
Round   7:   4- 10    5-  3    6-  2    7-  1    8-  9
Round   8:  10-  9    1-  8    2-  7    3-  6    4-  5
Round   9:   5- 10    6-  4    7-  3    8-  2    9-  1
------------------------------------------------------
```


## Circle

```
Round            1        2        3        4        5
------------------------------------------------------
Round   1:   1- 10    2-  9    3-  8    4-  7    5-  6
Round   2:   1-  9   10-  8    2-  7    3-  6    4-  5
Round   3:   1-  8    9-  7   10-  6    2-  5    3-  4
Round   4:   1-  7    8-  6    9-  5   10-  4    2-  3
Round   5:   1-  6    7-  5    8-  4    9-  3   10-  2
Round   6:   1-  5    6-  4    7-  3    8-  2    9- 10
Round   7:   1-  4    5-  3    6-  2    7- 10    8-  9
Round   8:   1-  3    4-  2    5- 10    6-  9    7-  8
Round   9:   1-  2    3- 10    4-  9    5-  8    6-  7
------------------------------------------------------
```

