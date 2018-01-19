""" 
    any private classes for this app are here
    
"""
from django.contrib.auth.models import User
from wenjian.models             import branch_office, branch_user, job
import datetime

class CreateNewJob:

    def __init__(self, username):
        self.username           = username
        self.user_id            = User.objects.get(username=self.username).id    
        self.this_office        = branch_office.objects.get(branch_user__user_ptr_id = self.user_id)
        self.office_code        = self.this_office.office_code
        self.office_id          = self.this_office.id

    def Officeid(self):
        return self.office_id

    def UserID(self):
        branch_office_user      = branch_user.objects.get(user_ptr_id=self.user_id).user_ptr_id
        return branch_office_user

    def UserName(self):
        return self.username

    def OfficeCode(self):
        return self.office_code

    def NewJobNo(self):
        this_year = str(datetime.date.today().year)       
        # Check if any job exist?
        last_job = job.objects.filter(job_no__contains=self.office_code).last()

        if last_job:            # IF there are any jobs already
            last_job_no = last_job.job_no
            y = last_job_no[2:6]
            if this_year == y:      # Year change? NOT, go ahead
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
                job_no = "JB" + this_year + self.office_code + '00001'
        else:                   # No JOB exist
            job_no = "JB" + this_year + self.office_code + "00001"  

        return job_no