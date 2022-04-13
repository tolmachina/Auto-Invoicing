import readline
import subprocess
from job_classes import JobParser
from invoice_class import Invoice
from colorama import Fore
from constants import *


def get_user_input():
    with open("invoice_number.txt", 'r') as f:
        global_invoice_number = f.readline()
    f.close()
    print("Global invoice num ", global_invoice_number)

    agency = input("Enter your agency? (Immersive, EC)\n")
    assert (agency == "Immersive" or agency=="EC")
    pdf = input(Fore.GREEN + "Enter path to job's pdf file from your agency: \n" + Fore.GREEN)
    
    
    invoice_number = input(Fore.GREEN + 'Enter invoice number from 000 to 999:\n' + Fore.GREEN)
    if invoice_number == "":
        invoice_number = global_invoice_number

    if agency != "Immersive":
        manager_name = input(Fore.GREEN + 'Enter managers name, default Darren McGuinness:\n' + Fore.GREEN)
        job_rate = input(Fore.GREEN + 'Enter total rate for the job:\n' + Fore.GREEN)
        if manager_name == "":
            manager_name = 'Darren McGuinness'
    else:
        manager_name = ""
        job_rate = ""
    return pdf,invoice_number,manager_name,job_rate, agency

def collect_job_info_ec(template: str, pdf: str, invoice_number: str, manager_name: str, job_rate: str):
    parse_job = JobParser()
    parse_job.read_pdf(pdf= pdf, template= template)
    job_info = parse_job.collect_job_info_ec(invoice_number=invoice_number, manager_name=manager_name, job_rate=job_rate)
    return job_info

def collect_job_info_immersive(template: str, pdf: str, invoice_number: str, job_rate: str):
    parse_job = JobParser()
    parse_job.read_pdf(pdf= pdf, template= template)
    job_info = parse_job.collect_job_info_immersive(invoice_number=invoice_number)
    return job_info

def main():
    template_ec ='ec_tabula-template.json'
    template_immersive = 'immersive_tabula-template.json'
    pdf, invoice_number, manager_name, job_rate, agency = get_user_input()
    
    if agency == "EC":
        job_info = collect_job_info_ec(template_ec, pdf, invoice_number, manager_name, job_rate)
        invoice = Invoice(address= EVENT_CONCEPT_ADDRESS, job = job_info)
    elif agency == "Immersive":
        job_info = collect_job_info_immersive(template_immersive, pdf, invoice_number, job_rate)
        invoice = Invoice(address = IMMERSIVE_ADDRESS ,job=job_info)
    else:
        print("Wrong Agency Name")
    
    while True:
        more_rows = input(Fore.GREEN + "Do you want to add another job? y/n\n " + Fore.GREEN)
        if more_rows == 'y':
            new_pdf = input(Fore.GREEN + "Enter path to job's pdf file from EC:\n" + Fore.GREEN)
            new_job_rate = input(Fore.GREEN + 'Enter total rate for the job:\n' + Fore.GREEN)
            new_job_info = collect_job_info_ec(template_ec, new_pdf, invoice_number, manager_name, new_job_rate)
            invoice.add_table_row(new_job= new_job_info)
        else:
            break
    
    invoice.finish_doc()
    path = invoice.get_file_name()

    open_invoice = subprocess.run(["open", str(path)], stderr=subprocess.PIPE, text=True)
    print(open_invoice.stderr)

    send_mail = subprocess.run(["open", "-a", "Mail", str(path)], stderr=subprocess.PIPE, text=True)

    print(send_mail.stderr)

    with open("invoice_number.txt", "r") as f:
        invoice_num = int(f.readline())
        invoice_num += 1
    
    with open("invoice_number.txt", "w") as f:
        f.write("0" + str(invoice_num))



if __name__ == '__main__':
    main()



