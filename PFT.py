from PFT import main
import sys
import subprocess



if __name__ == '__main__':
    if "web-version" in (sys.argv):
        subprocess.run(["streamlit", "run", "./PFT/app.py"])
    else:
        main.main()
