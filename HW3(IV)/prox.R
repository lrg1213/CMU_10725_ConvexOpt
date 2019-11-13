prox = function(z, lam) {
  if (!is.loaded("prox_dp_R")) {
    dyn.load("prox.so")
  }

  o = .C("prox_dp_R",
    n=as.integer(length(z)),
    z=as.double(z),
    lam=as.double(lam),
    theta=as.double(numeric(length(z))),
    dup=FALSE)

  return(o$theta)
}
