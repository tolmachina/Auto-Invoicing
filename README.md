# Auto-Invoicing
ver. 0.01

A command line script that auto-generates invoices from specific pdf files with job's description. A handy tool, saving time on boring tasks.

Principle:

A tabula-py framework scans pdf file and generates a dataframe object, which then combined with user entered data into *JobInfo() class* consisting of following fields: 
- id, 
- date_start, 
- date_end, 
- location, 
- rate, (entered by user)
- invoice_date, 
- invoice_number, (entered by user)
- manager_name (entered by user)

Invoice is generated based on data from *JobInfo() class*. It happens with help of python docx module.

