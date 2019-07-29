################
# Assignment 1 #
################



# 2.1 Creating vectors
# --------------------

# numerical
vec1 = c(2.8, 2.4, 2.1, 3.6, 2.8)
vec1


# character
vec2 = c("red", "green", "green", "green", "yellow")
vec2

# logical
vec3 = c(TRUE, TRUE, FALSE, FALSE, FALSE)
vec3

# repetition
rep(4, 3)

vec4 = rep(vec1, 2)
vec4

vec5 = rep(vec1, c(2, 1, 3, 3, 2))
vec5

# sequences

vec6 = 1 : 10
vec6

vec7 = seq(from = 3, to = 5, by = 0.2)
vec7

vec7 = seq(from = 3, length = 11, by = 0.2)

# component by component

vec8 = numeric()
vec8[1] = 41.8
vec8[2] = -0.3
vec8[3] = 92
vec8

vec9 = character()

vec10 = logical()

vec8 = numeric(3)

vec5[2]
vec5[c(1, 3 : 5)]



# 2.2 Creating matrices
# ---------------------

# generic
mat1 =  matrix(vec4, ncol = 5)
mat1

dim(mat1) = c(2, 5)

mat2 = matrix(vec4, ncol = 5, byrow = TRUE)
mat2

# other methods
mat3 = cbind(vec1, 3 : 7)
mat3

# extract sub-matix, colunm, or line
mat1[, c(2, 4, 5)]

mat1[, c(FALSE,TRUE,FALSE,TRUE,TRUE)]

mat3[c(1, 4), ]

mat3[c(TRUE,FALSE,FALSE,TRUE,FALSE), ]

mat1[, 3] 

# dimensions
dim(mat1)



# 2.3 Creating lists
# ------------------

# directly
list1 = list(vec1,c("red","blue"), mat1)
list1

# component by component
list1 = list()
list1[[1]] = vec1
list1[[2]] = c("red","blue")
list1[[3]] =  mat1



# 2.4 More vector operations
# --------------------------


# copying, extending, extracting,...
# copying
vec11 = vec1
vec13 =  vec12 =  vec11
c(vec1, c(3.9, 2.7))

# extending
c("blanc", vec2)

# extracting
vec1[2]
vec1[c(2, 4)]
vec1[2 : 4]
vec1[vec3] 

# shortening
vec11[-c(2)]
vec12[-c(2, 4)]
vec13[-(2 : 4)]

# replacing
vec5
vec5[3 : 5] = c(1034, 238, -99)
vec5

# naming
names(vec1) = c("julie", "paul", "solveigh", "valentin", "elsa")

vec1["paul"] 

# knowing and changing type
mode(vec5)

is.numeric(vec5)

vec14 = as.character(vec4)
vec14


# arithmetic operations on numeric vectors
vec1 + 4

2 * vec1 - c(1, 2)


# application of a function
# Vector of length k -> Vector of length k
sin( vec1)

round(c(9.238, -1.34222), 2)

sort(vec1)

order(vec1)

# Vector of length k -> numerical value
mean(vec1)

# Vector of length k -> vector of length 2
range(vec1)

# other functions
summary(vec1)
?cor
cor(1 : 10, (2 : 11) / 2)


# character vectors
# pasting
paste("jules","jim")

paste("jules", "jim", sep = "")

# pasting vectors of different length and more than two vectors
paste("X", 1 : 4, sep = "")
paste("X", 1 : 4, c("s", "o"), sep = "")


# Operations on logical vectors
# comparison
c(1, 4, -2, 5) < c(2, 4, -3, 6)

a = c(3, 2, 8, 3, -3)
b = c(1, 2)
a <= b

a > 2.5

# conditioned selection
vec1[vec1 > 2.5 ]

# operators
any(a <= b)

all(a <= b)


# 2.5 Operations on lists
# -----------------------

# naming list elements
names(list1) = c("weight", "colour", "matrix")

list2 = list(weight = vec1, colour = c("red","blue"), matrix = mat1)

list1 

list2

# extract list elements
list1$colour

list1[[2]]


# 2.6 Matrix operations
# ---------------------

# naming lines and columns
dimnames(mat1) =  list(c("jules", "jim"), paste("X", 1 : 5, sep = ""))
mat1

mat1["jim", "X3"]

# arithmetical operations
mat1 + 3

# specific operations
mat1 %*% t(mat1)
t(mat1) %*% mat1

diag(t(mat1) %*% mat1)
mat1 %*% t(mat1) %*% solve(mat1 %*% t(mat1))



# 2.7 Missing and absent values
# ----------------------------- 

dimnames(mat1) = list(NULL, paste("X", 1 : 5, sep=""))

vec14 = c(31, 43, NA, 33)

is.na(vec14)


# 2.8 Data structures: objects data.frame and ts
# ----------------------------------------------

# construction
dat1 = as.data.frame(mat1)

age = c(24, 26, 22)
sex = c("m", "m", "f")
music = c(TRUE, FALSE, TRUE)
survey = data.frame(age, sex, music)

sex = factor(c("m", "m", "f"))

levels(sex)

names(survey) = c("age", "sex", "music")

row.names(survey) = c("Jules","Jim","Elsa")

survey = data.frame(age = c(24, 26, 22), 
                    the.sex = c("m","m", "f"), 
                    music = c(TRUE, FALSE, TRUE))

# woking with a data frame
survey[1:2,2:3]

attach(survey)

age

detach(survey)

survey$age


# construction of contingency tables from a data frame
attach(survey)

table(sex)

table(sex, music)

# ts (times series) object
x = c(1, 3, 2, 4, 4, 3, 5, 2, 3, 4, 1, 8,
      1, 3, 2, 4, 5, 2, 3, 2, 2, 2, 4, 3)

ts(x, start = c(2002,3), freq = 12)

ts(x, start = c(2002,3), freq = 4)


# 2.9 Reading and writing data

# reading data with scan()
vec15 = scan("data.txt")

dat1 = matrix(scan("data.txt"), ncol = 3, byrow = TRUE)

# reading data with read.table()
dat2 = read.table("data.txt")

# writing
?write.table  

# dget()/dput()
?dput()


# 2.10 Some more complex functions

# application of a function to matrix lines (coloumns)
apply(mat1, 1, mean)

apply(mat1, 2, mean)


# application of a function to list elements
my.list = list(c(1, 2), c(3, 1, 2))
sapply(my.list, mean)

lapply(my.list, sd)


# application of a function to a grouped vector
tapply(age, sex, mean)

tapply(age, list(sex, music), mean)

# constructing lists by split()
split(age, sex)

