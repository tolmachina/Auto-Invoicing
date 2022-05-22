from pipes import Template
import subprocess
from job_classes import JobInfo, JobParser
from invoice_class import Invoice
"""
Tests for script to run with correct inputs.
"""

TEMPLATE ='ec_tabula-template.json'
PDF = 'jobs_ec/Various Bloomberg Offices.pdf'
PDF_RAA = 'jobs_ec/24.03.22 RAA.pdf'
MANAGER = 'John Johnson'

def test_job_parser():
    job_rate = '£250'
    invoice_number = '123'
    invoicer = JobParser()
    table = invoicer.read_pdf(pdf=PDF, template= TEMPLATE)
    job = invoicer.collect_job_info_ec(table,invoice_number,job_rate)
    return job

def test_invoice_docx(job: JobInfo):
    invoice_number = '444'
    job_rate = '£250'
    parser = JobParser()
    parser.read_pdf(pdf=PDF, template= TEMPLATE)
    job = parser.collect_job_info_ec(invoice_number,MANAGER,job_rate)
    print(job)

    doc = Invoice(agency_address="93 FEET EAST", job=job)
    doc.finish_doc()
    path = doc.get_file_name()

    result = subprocess.run(["open", str(path)], stderr=subprocess.PIPE, text=True)
    print(result.stderr)

def test_various_job():
    parse_job = JobParser()
    parse_job.read_pdf(pdf=PDF, template= TEMPLATE)
    job_info = parse_job.collect_job_info_ec(invoice_number='333', manager_name='John Johnsons', job_rate='£757.50')

    invoice = Invoice(agency_address="93 FEET EAST", job=job_info)
    invoice.finish_doc()
    path = invoice.get_file_name()
    result = subprocess.run(["open", str(path)], stderr=subprocess.PIPE, text=True)
    print(result.stderr)

def test_24_job():
    parse_job = JobParser()
    parse_job.read_pdf(pdf= PDF, template= TEMPLATE)
    job_info = parse_job.collect_job_info_ec(invoice_number='222', manager_name="John Johnsons", job_rate='£270')

    invoice = Invoice(agency_address="93 FEET EAST", job=job_info)
    invoice.finish_doc()
    path = invoice.get_file_name()
    open_invoice = subprocess.run(["open", str(path)], stderr=subprocess.PIPE, text=True)
    print(open_invoice.stderr)

    send_mail = subprocess.run(["open", "-a", "Mail", str(path)], stderr=subprocess.PIPE, text=True)
    print(send_mail.stderr)

def test_add_row():
    parse_job = JobParser()
    parse_job.read_pdf(pdf= PDF_RAA, template= TEMPLATE)
    job_info = parse_job.collect_job_info_ec(invoice_number='111', manager_name=MANAGER, job_rate='£270')

    invoice = Invoice(agency_address="93 FEET EAST", job=job_info)

    parse_job.read_pdf(pdf= PDF, template= TEMPLATE)
    job_info = parse_job.collect_job_info_ec(invoice_number='111', manager_name=MANAGER, job_rate='£757')
    invoice.add_table_row(job_info)
    
    invoice.finish_doc()
    
    path = invoice.get_file_name()
    open_invoice = subprocess.run(["open", str(path)], stderr=subprocess.PIPE, text=True)
    print(open_invoice.stderr)

    send_mail = subprocess.run(["open", "-a", "Mail", str(path)], stderr=subprocess.PIPE, text=True)
    print(send_mail.stderr)

def test_job_parser():
    parser = JobParser()

    # parser.read_pdf(pdf=PDF,template=TEMPLATE)
    # parser.read_pdf(pdf=PDF_RAA, template=TEMPLATE)
    # parser.read_pdf("jobs_ec/Various The Grove.pdf", TEMPLATE)
    parser.read_pdf("jobs_ec/04.05.22 Tate Modern.pdf", TEMPLATE)

    parser.merge_columns()


def test_collect_job():
    parser = JobParser()

    # parser.read_pdf(pdf=PDF,template=TEMPLATE)
    # parser.read_pdf(pdf=PDF_RAA, template=TEMPLATE)
    # parser.read_pdf("jobs_ec/Various The Grove.pdf", TEMPLATE)
    parser.read_pdf("jobs_ec/04.05.22 Tate Modern.pdf", TEMPLATE)
    job = parser.collect_job_info_ec('999')
    print(job)

# test_job_parser()
test_collect_job()



# test_add_row()
# test_24_job()
# job = test_job_parser()
# test_invoice_docx(job)

# test_various_job()

