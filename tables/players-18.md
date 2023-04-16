# Round-robin pairs for 18 players

## Modified Berger (ideal)

```
Round            1        2        3        4        5        6        7        8        9
------------------------------------------------------------------------------------------
Round   1:   9- 10    2- 17    3- 16    4- 15    5- 14    6- 13    7- 12    8- 11    1- 18
Round   2:  17-  3   11-  9   12-  8   13-  7   14-  6   15-  5   16-  4   18- 10    1-  2
Round   3:   8- 13    3-  1    4- 17    5- 16    6- 15    7- 14    2- 18    9- 12   10- 11
Round   4:  16-  6   12- 10   13-  9   14-  8   15-  7   18- 11   17-  5    1-  4    2-  3
Round   5:   7- 16    4-  2    5-  1    6- 17    3- 18    8- 15    9- 14   10- 13   11- 12
Round   6:  15-  9   13- 11   14- 10   18- 12   16-  8   17-  7    1-  6    2-  5    3-  4
Round   7:   6-  2    5-  3    4- 18    7-  1    8- 17    9- 16   10- 15   11- 14   12- 13
Round   8:  14- 12   18- 13   15- 11   16- 10   17-  9    1-  8    2-  7    3-  6    4-  5
Round   9:   5- 18    6-  4    7-  3    8-  2    9-  1   10- 17   11- 16   12- 15   13- 14
Round  10:  15- 13   18- 14   16- 12   17- 11    1- 10    2-  9    3-  8    4-  7    5-  6
Round  11:   8-  4    7-  5    6- 18    9-  3   10-  2   11-  1   12- 17   13- 16   14- 15
Round  12:   1- 12   16- 14   17- 13   18- 15    2- 11    3- 10    4-  9    5-  8    6-  7
Round  13:  11-  3    8-  6    9-  5   10-  4    7- 18   12-  2   13-  1   14- 17   15- 16
Round  14:   4- 11   17- 15    1- 14    2- 13    3- 12   18- 16    5- 10    6-  9    7-  8
Round  15:  14-  2    9-  7   10-  6   11-  5   12-  4   13-  3    8- 18   15-  1   16- 17
Round  16:   7- 10    1- 16    2- 15    3- 14    4- 13    5- 12    6- 11   18- 17    8-  9
Round  17:  17-  1   10-  8   11-  7   12-  6   13-  5   14-  4   15-  3   16-  2    9- 18
------------------------------------------------------------------------------------------
```


## Berger

```
Round            1        2        3        4        5        6        7        8        9
------------------------------------------------------------------------------------------
Round   1:   1- 18    2- 17    3- 16    4- 15    5- 14    6- 13    7- 12    8- 11    9- 10
Round   2:  18- 10   11-  9   12-  8   13-  7   14-  6   15-  5   16-  4   17-  3    1-  2
Round   3:   2- 18    3-  1    4- 17    5- 16    6- 15    7- 14    8- 13    9- 12   10- 11
Round   4:  18- 11   12- 10   13-  9   14-  8   15-  7   16-  6   17-  5    1-  4    2-  3
Round   5:   3- 18    4-  2    5-  1    6- 17    7- 16    8- 15    9- 14   10- 13   11- 12
Round   6:  18- 12   13- 11   14- 10   15-  9   16-  8   17-  7    1-  6    2-  5    3-  4
Round   7:   4- 18    5-  3    6-  2    7-  1    8- 17    9- 16   10- 15   11- 14   12- 13
Round   8:  18- 13   14- 12   15- 11   16- 10   17-  9    1-  8    2-  7    3-  6    4-  5
Round   9:   5- 18    6-  4    7-  3    8-  2    9-  1   10- 17   11- 16   12- 15   13- 14
Round  10:  18- 14   15- 13   16- 12   17- 11    1- 10    2-  9    3-  8    4-  7    5-  6
Round  11:   6- 18    7-  5    8-  4    9-  3   10-  2   11-  1   12- 17   13- 16   14- 15
Round  12:  18- 15   16- 14   17- 13    1- 12    2- 11    3- 10    4-  9    5-  8    6-  7
Round  13:   7- 18    8-  6    9-  5   10-  4   11-  3   12-  2   13-  1   14- 17   15- 16
Round  14:  18- 16   17- 15    1- 14    2- 13    3- 12    4- 11    5- 10    6-  9    7-  8
Round  15:   8- 18    9-  7   10-  6   11-  5   12-  4   13-  3   14-  2   15-  1   16- 17
Round  16:  18- 17    1- 16    2- 15    3- 14    4- 13    5- 12    6- 11    7- 10    8-  9
Round  17:   9- 18   10-  8   11-  7   12-  6   13-  5   14-  4   15-  3   16-  2   17-  1
------------------------------------------------------------------------------------------
```


## Circle

```
Round            1        2        3        4        5        6        7        8        9
------------------------------------------------------------------------------------------
Round   1:   1- 18    2- 17    3- 16    4- 15    5- 14    6- 13    7- 12    8- 11    9- 10
Round   2:   1- 17   18- 16    2- 15    3- 14    4- 13    5- 12    6- 11    7- 10    8-  9
Round   3:   1- 16   17- 15   18- 14    2- 13    3- 12    4- 11    5- 10    6-  9    7-  8
Round   4:   1- 15   16- 14   17- 13   18- 12    2- 11    3- 10    4-  9    5-  8    6-  7
Round   5:   1- 14   15- 13   16- 12   17- 11   18- 10    2-  9    3-  8    4-  7    5-  6
Round   6:   1- 13   14- 12   15- 11   16- 10   17-  9   18-  8    2-  7    3-  6    4-  5
Round   7:   1- 12   13- 11   14- 10   15-  9   16-  8   17-  7   18-  6    2-  5    3-  4
Round   8:   1- 11   12- 10   13-  9   14-  8   15-  7   16-  6   17-  5   18-  4    2-  3
Round   9:   1- 10   11-  9   12-  8   13-  7   14-  6   15-  5   16-  4   17-  3   18-  2
Round  10:   1-  9   10-  8   11-  7   12-  6   13-  5   14-  4   15-  3   16-  2   17- 18
Round  11:   1-  8    9-  7   10-  6   11-  5   12-  4   13-  3   14-  2   15- 18   16- 17
Round  12:   1-  7    8-  6    9-  5   10-  4   11-  3   12-  2   13- 18   14- 17   15- 16
Round  13:   1-  6    7-  5    8-  4    9-  3   10-  2   11- 18   12- 17   13- 16   14- 15
Round  14:   1-  5    6-  4    7-  3    8-  2    9- 18   10- 17   11- 16   12- 15   13- 14
Round  15:   1-  4    5-  3    6-  2    7- 18    8- 17    9- 16   10- 15   11- 14   12- 13
Round  16:   1-  3    4-  2    5- 18    6- 17    7- 16    8- 15    9- 14   10- 13   11- 12
Round  17:   1-  2    3- 18    4- 17    5- 16    6- 15    7- 14    8- 13    9- 12   10- 11
------------------------------------------------------------------------------------------
```

