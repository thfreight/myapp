# from django.test import TestCase
import datetime

# Create your tests here.
this_year = datetime.date.today().year
last_job = "JB2018SZ000010"
if last_job:            # IF there are any jobs already
    last_job_no = last_job
    job_year = last_job_no[2:6]
    print(this_year, job_year)
    if str(this_year) == job_year:      # Year change? NOT, go ahead
        num_part = int(last_job_no[8:])+1
        alpha_part = last_job_no[:8]
        if num_part in range(9):
            job_no = alpha_part     + "0000"    + str(num_part)
        elif num_part in range(9,99):
            job_no = alpha_part     + "000"     + str(num_part)
        elif num_part in range(99, 999):
            job_no = alpha_part     + "00"      + str(num_part)
        elif num_part in range(999, 9999):
            job_no = alpha_part     + "0"       + str(num_part)
        else:
            job_no = alpha_part                 + str(t)
    else:                   # NEW YEAE now
        job_no = "JB" + str(this_year) + "sz" + '00001'
else:                   # No JOB exist
    job_no = "JB" + str(this_year) + "sz" + "00001"  

print(job_no)