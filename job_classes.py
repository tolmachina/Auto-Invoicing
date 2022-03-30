import tabula
from datetime import date
class JobParser():
    """
    Parsing pdf job file into JobInfo data structure. Optimized for EC jobs.
    """
    def __init__(self):
        self.table = None

    def read_pdf(self, pdf: str, template: str):
        """
        Reads PDF with help of pre-created tabula-py template file.
        Returns pandas dataframe. 
        """
        self.table = tabula.read_pdf_with_template(input_path = pdf, template_path= template)[0]
        return self.table

    def collect_job_info(self, invoice_number: str, manager_name: str, job_rate='£250'):
        """
        Combines all data from dataframe table and also manually entered data.
        """
        
        table = self.table.to_dict()
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
    Data Structure containing all information about job.
    """
    def __init__(self):
        self.id = None
        self.date_start = None
        self.date_end = None
        self.location = None
        self.rate = None
        self.invoice_date = None
        self.invoice_number = None
        self.manager_name = None
    
    def __str__(self):
        to_print = str(self.id) + '\n' + str(self.date_start) + '\n'  + str(self.date_end) + '\n'  + str(self.location) + '\n'  + str(self.rate) + '\n'  + str(self.invoice_date) + '\n'  + str(self.invoice_number)
        return to_print
    

