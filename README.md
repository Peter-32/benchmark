# benchmark

Temporary notes below:

Input files download location: 
https://lotv.spawningtool.com/replays/?tag=644&order_by=play

June 22nd to July 6th are the dates used due to the large change with recent patch (8 worker start).  Found data up until July 6th online.

Only about 25 replays so manually downloading them.





python -m PyInstaller --noconfirm --onedir --windowed main.py

python -m PyInstaller --noconfirm --onedir --windowed --add-data "../data;data" --name="MyBenchmarkApp" main.py

python -m PyInstaller --noconfirm --onedir --add-data "../data;data;src/output_html.html;src" --name="MyBenchmarkApp" main.py

C:\Users\peter\OneDrive\code\benchmark\data\input\my_data\sample_2