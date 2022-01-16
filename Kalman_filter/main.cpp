#include "gaussian.hpp"
#include "measurement_update.hpp"
#include "motion_update.hpp"

int main()
{
    double measurements[5] = { 5, 6, 7, 9, 10 };
    double measurement_sig = 4;
    
    //Motions and motion variance
    double motion[5] = { 1, 1, 2, 1, 1 };
    double motion_sig = 2;
    
    //Initial state
    double mu = 50;
    double sig = 28;

    for(int i=0;i<sizeof(measurements)/sizeof(measurements[0]);i++)
    {
        tie(mu,sig)=parameter_update(mu,measurements[i],sig,measurement_sig);
        printf("update:  [%f, %f]\n", mu, sig);
        tie(mu, sig) = state_update(mu,  motion[i],sig, motion_sig);
        printf("predict: [%f, %f]\n", mu, sig);

    }
}