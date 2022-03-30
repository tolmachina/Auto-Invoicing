from ast import For
import subprocess
from job_classes import JobParser
from invoice_class import Invoice
from colorama import Fore

def get_user_input():
    pdf = input(Fore.GREEN + "Enter path to job's pdf file from Event Concept: \n" + Fore.GREEN)
    invoice_number = input(Fore.GREEN + 'Enter invoice number from 000 to 999:\n' + Fore.GREEN)
    manager_name = input(Fore.GREEN + 'Enter name, default Darren McGuinness:\n' + Fore.GREEN)
    if manager_name == "":
        manager_name = 'Darren McGuinness'
    job_rate = input(Fore.GREEN + 'Enter total rate for the job:\n' + Fore.GREEN)
    return pdf,invoice_number,manager_name,job_rate

def collect_job_info(template: str, pdf: str, invoice_number: str, manager_name: str, job_rate: str):
    parse_job = JobParser()
    parse_job.read_pdf(pdf= pdf, template= template)
    job_info = parse_job.collect_job_info(invoice_number=invoice_number, manager_name=manager_name, job_rate=job_rate)
    return job_info

def main():
    template ='ec_tabula-template.json'

    pdf, invoice_number, manager_name, job_rate = get_user_input()

    job_info = collect_job_info(template, pdf, invoice_number, manager_name, job_rate)

    invoice = Invoice(job=job_info)
    while True:
        more_rows = input(Fore.GREEN + "Do you want to add another job? y/n\n " + Fore.GREEN)
        if more_rows == 'y':
            new_pdf = input(Fore.GREEN + "Enter path to job's pdf file from Event Concept:\n" + Fore.GREEN)
            new_job_rate = input(Fore.GREEN + 'Enter total rate for the job:\n' + Fore.GREEN)
            new_job_info = collect_job_info(template, new_pdf, invoice_number, manager_name, new_job_rate)
            invoice.add_table_row(new_job= new_job_info)
        else:
            break
    
    invoice.finish_doc()
    path = invoice.get_file_name()

    open_invoice = subprocess.run(["open", str(path)], stderr=subprocess.PIPE, text=True)
    print(open_invoice.stderr)

    send_mail = subprocess.run(["open", "-a", "Mail", str(path)], stderr=subprocess.PIPE, text=True)

    print(send_mail.stderr)

if __name__ == '__main__':
    main()



