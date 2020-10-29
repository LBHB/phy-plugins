import numpy as np
spike_times1=np.load('/auto/users/luke/Projects/Sorting/HOD005/spike_times1.npy')
spike_times2=np.load('/auto/users/luke/Projects/Sorting/HOD005/spike_times2.npy')
N=10000
N=10000
maxdiff=10
try_num=1
while try_num<5:
     diffs=np.zeros(N)
     times=np.zeros(N)
     i=-1
     start=0
     for st1 in spike_times1:
          st2i = start
          while st2i<len(spike_times2) and i<N-1:
             df = st1 - spike_times2[st2i]
             if df >= maxdiff:
                 start += 1
                 st2i += 1
             elif df > -maxdiff:
                 i += 1
                 diffs[i]=df
                 times[i]=st1
                 st2i += 1
             else:
                 break
          if i==N-1:
             maxdiff = maxdiff/2
             try_num +=1
             break
     if i<N-1:
         break