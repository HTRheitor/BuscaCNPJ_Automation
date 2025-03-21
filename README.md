# Municipal NFe Automation Bot

## Important Notice
**WARNING:** This repository contains sample code only. No real credentials, CNPJ numbers, or sensitive data are included. All such information must be provided by the user during execution.

## About the Project
This project automates interactions with a municipal government website to streamline the process of retrieving electronic invoices (NFe) and filing service declarations for multiple clients. The automation handles login with user credentials, navigates the website interface, downloads XML files, submits service declarations, and organizes the resulting files for subsequent import.

### Features
- Automated login to municipal website using CPF and password
- Batch processing of multiple CNPJ numbers
- Automatic navigation through the website menus
- Download of XML invoice files 
- Submission of service declarations
- Download of declaration receipts
- Organized file storage in a specified Dropbox folder
- User-friendly GUI interface

## Requirements
- Python 3.6 or higher
- Libraries:
  - PySimpleGUI
  - Selenium WebDriver
  - pandas
  - os
  - time

## How to Use
1. Run the script:
```bash
python app.py
```
2. In the GUI window:

Enter your CPF in the "Usuário" field
Enter your password
Enter the list of client CNPJs (one per line)
Select your Dropbox folder where files will be saved


3. Click "Enviar" to start the process
4. The output window will display progress information

## Folder Structure
For each CNPJ processed, the system creates a dedicated folder with the following naming convention:
Cliente_[CNPJ]

Within each folder, you'll find:

XML files of downloaded invoices
PDF receipts of service declarations
