1. Unzip the file
bashcd ~/Downloads
unzip bbn_platform.zip
cd bbn_platform
2. Create a virtual environment (recommended)
bashpython3 -m venv venv
source venv/bin/activate
3. Install dependencies
bashpip install -r requirements.txt
4. Run the app
bashshiny run app.py --reload
Then open http://localhost:8000 in your browser. The --reload flag means the app auto-restarts whenever you save a file — handy while developing.

If you're on Windows, step 2 becomes:
bashpython -m venv venv
venv\Scripts\activate

To stop the app, press Ctrl+C in the terminal.
