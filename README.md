# XTimer application release code
## How to test:
- Run main.py directly

## How to deploy:
- Run the following instruction in your Terminal.
``` shell
pyinstaller -D -w -i .\res\logo.ico -n XTimer main.py
```
- Then copy the directory ".\\res\\" with files into the directory ".\\dist\\XTimer\\"

- Click the "XTimer.exe" within the ".\\dist\\XTimer\\", you'll successfully run the XTimer application.
## Packages you need:
``` shell
pip install wx
pip install PIL
pip install pyinstaller
```