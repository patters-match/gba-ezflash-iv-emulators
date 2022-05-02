for %%f in (*.sms) do @smsadvance_compile.py "%%f" -o "%%~nf".gba -pat
