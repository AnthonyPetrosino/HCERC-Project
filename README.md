# HCERC-Project
 Web App for the Holy Cross Equity Research Club

Currently under development.

Transferred models into packages.

Additional Comments:
- Add price change to stocks in addition to percent change
- Add a place that shows a bold BUY/SELL/HOLD
- Make title on posts have a buy/sell/hold and the percent change
- Make words on website HC purple
- Make upload pdf option for the stock write-up

Bigger additions
- Make admin versus viewer access

# Instructions to run the project locally (fresh setup on mac with GitHub Desktop/VS Code):
## 1. Clone the Repository using GitHub Desktop
- Open GitHub Desktop.
- Click "File" > "Clone Repository".
- Select "URL", enter https://github.com/AnthonyPetrosino/HCERC-Project, and choose a local directory.
- Click "Clone" to download the repository.
## 2. Open the Project in VS Code
- Open VS Code, click "File" > "Open Folder...".
- Navigate to the cloned project folder and open it.
## 3. Create a Virtual Environment
- Open a terminal in VS Code ("View" > "Terminal" or Cmd + ~).
- Run the following command to create a virtual environment: python3 -m venv venv
## 4. Activate the Virtual Environment
- Run the following command to activate the virtual environment: source venv/bin/activate
- You will need to run this every time you open a new terminal.
## 5. Install Dependencies
- Inside the activated virtual environment, run the following command: pip install -r requirements.txt
- Wait for everything to install.
## 6. Run the Flask App
- Finally, run the following command: python run.py

## Summary of commands to run:
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. python run.py 
Once you have set up the project, you only need to run commands 2. and 4. each time you reopen your terminal in the correct directory/folder.

Type http://127.0.0.1:5000/ into your browser to view the project.
