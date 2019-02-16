#initialization for 
psi0 = 1
psi1 = 0.3
psi2 = 0.41
theta3 = 0.1
psi3 = 1.7*psi2 - 0.9*psi1 + theta3
psi <- c(psi0,psi1,psi2,psi3)
#compute the rest
for (j in 2:48)
  psi[j+2] = 1.7*psi[j+1] - 0.9*psi[j]

#Initialize gamma with gamma0 and gamma1
gamma0 = 0
for (k in 1:5)
  gamma0 = gamma0 + psi[k]*psi[k]

gamma1 = 0
for (k in 1:5)
  gamma1 = gamma1 + psi[k]*psi[k+1]

gamma = c(gamma0,gamma1)
# comute the rest of the gamma's
for (k in 1:48)
  gamma[k+2] = 1.7*gamma[k+1] - 0.9*gamma[k]
print(length(gamma))

#plot
plot(gamma, col='blue')
