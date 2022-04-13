
from job_classes import *
from constants import *
from invoice_class import *

pdf = "/Users/evgeny/Documents/SoundEngineering2021/Auto Invoicing/jobs_immersive/Amended Evgeny Tolmachev Technical Services 13 Apr.pdf"
template = "/Users/evgeny/Documents/SoundEngineering2021/Auto Invoicing/immersive_tabula-template.json"
job_parser = JobParser()

table = job_parser.read_pdf(pdf, template)
job = job_parser.collect_job_info_immersive(invoice_number='099')
print(job)