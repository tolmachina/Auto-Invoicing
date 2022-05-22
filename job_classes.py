from typing import List
from pandas import DataFrame
import tabula
from datetime import date

class JobParser():
    """
    Parsing pdf job file into JobInfo data structure. Only for EC jobs.
    """
    def __init__(self):
        self.table = None
        self.jobs_counter = 0

    def read_pdf(self, pdf: str, template: str):
        """
        Reads PDF with help of pre-created tabula-py template file.
        Returns pandas dataframe. 
        """
        self.table = tabula.read_pdf_with_template(input_path = pdf, template_path= template, pandas_options={'header': None}, stream= True)
        self.jobs_counter += 1
        job_filename = 'dataframe' + str(self.jobs_counter) + '.csv'
        self.table[0].to_csv(job_filename)
        self.table[0].fillna(' ', inplace=True)
        

        return self.table

    def collect_job_info_immersive(self, invoice_number):
        job = JobInfo()
        job.id = self.table[1].iat[0,1]
        job.date_start = self.table[1].iat[2,1].split()[0]
        job.date_end = self.table[1].iat[2,1].split()[0]
        job.location = self.table[3].iat[0,0]
        job.rate = "£" + str(list(self.table[2].columns)[3])
        job.invoice_date = str(date.today().strftime("%d/%m/%Y"))
        job.invoice_number = invoice_number
        job.manager_name = self.table[1].iat[3,1]
        return job
    
    def merge_columns(self):
        if type(self.table) is list:
            self.table = self.table[0]
        
        self.sizeoftable = self.table.shape
        self.table[3] = self.table[1] + " " +  self.table[2]
        self.table.drop([1,2],axis=1, inplace=True)
        self.table.rename(columns={self.table.columns[1]: 1}, inplace=True)
        
    
    def collect_job_info_ec(self, invoice_number: str, manager_name: str = 'Darren McGuinness', job_rate='£275'):
        """
        Wrapper
        """
        
        self.table: DataFrame = self.table[0]
        self.sizeoftable = self.table.shape
        if self.sizeoftable[1] == 3:
            self.merge_columns()
        return self.job_ec_from_dataframe(invoice_number, manager_name, job_rate)
        
    def job_ec_from_dataframe(self, invoice_number: str, manager_name: str , job_rate: str ):
        job = JobInfo()
        print(self.table, '\n')
        for i in range(self.sizeoftable[0]):
            if 'Event ID' in self.table.iat[i,1]:
                job.id = self.table.iat[i,1].split()[-1]
            if 'Access' in self.table.iat[i,1]:
                job.date_start = self.table.iat[i,1].split()[1]
            if 'Strike' in self.table.iat[i,1]:
                job.date_end = self.table.iat[i,1].split()[1]
            if 'Venue' in self.table.iat[i,0]:
                job.location = self.table.iat[i+1,0]
        job.rate = job_rate
        job.invoice_date = str(date.today().strftime("%d/%m/%Y"))
        job.invoice_number = invoice_number
        job.manager_name = manager_name
        return job

    def job_ec_dictionary(self, invoice_number: str, manager_name: str, job_rate='£250'):
        """
        Combines all data from dataframe table and also manually entered data.
        """
        table = self.table.to_dict()
        print(table)

        job = JobInfo()
        job.id = list(table.keys())[1]
        
        for val in table[job.id].values():
            if type(val)==str:
                if 'Access' in val:
                    job.date_start = val.split()[1]
                if 'Strike' in val:
                    job.date_end = val.split()[1]
                    break
        if job.date_start == None or job.date_end  == None:
            print("\nError with date start and/or date end\n")    
        
        position = None

        for item in table['Customer:'].items():
            if 'Venue:' in item:
                key = item[0]
                position = key + 1
                break

        job.location = table['Customer:'][position]
        job.rate = job_rate
        job.invoice_date = str(date.today().strftime("%d/%m/%Y"))
        job.invoice_number = invoice_number
        job.manager_name = manager_name
        return job

class JobInfo():
    """
    Data Structure containing all information about a job.
    """
    def __init__(self):
        self.id = ""
        self.date_start = ""
        self.date_end = ""
        self.location = ""
        self.rate = ""
        self.invoice_date = ""
        self.invoice_number = ""
        self.manager_name = ""
    
    def __str__(self):
        to_print = "Job ID: " + str(self.id) + '\n' + "Date Start: " + str(self.date_start) + '\n' + "Date Ends: " + str(self.date_end) + '\n' +  "Location: " + str(self.location) + '\n' + "Day rate: " + str(self.rate) + '\n' + "Invoice Date: " + str(self.invoice_date) + '\n' + "Invoice Num: " + str(self.invoice_number)
        return to_print
    

