#include <iostream>
#include <math.h>

using namespace std;

float gauss(float,float,float);

float gauss(float mu,float sigma2,float x)
{
    float prob=(1.0/2.0*M_PI*sigma2)*exp(-0.5*(pow((x-mu),2)/sigma2));
    return prob;
}