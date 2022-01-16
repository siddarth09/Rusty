#include <iostream>
#include <math.h>
#include <tuple>

double mu,var;
tuple<double,double> state_update(double mu1,double mu2,double sigma2a, double sigma2b)
{
     mu=mu1+mu2;
     var=sigma2a+sigma2b;

    return make_tuple(mu,var);
}