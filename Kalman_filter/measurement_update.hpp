#include <iostream>
#include <math.h>
#include <tuple>

double newmu,newvar;
tuple<double,double> parameter_update(double mu1,double mu2,double sigma2a, double sigma2b)
{
     newmu=(sigma2b*mu1+sigma2a*mu2)/(sigma2b+sigma2a);
     newvar=1.0/(1.0/sigma2a+1.0/sigma2b);

    return make_tuple(newmu,newvar);
}