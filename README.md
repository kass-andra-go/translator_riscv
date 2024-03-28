(английский, русский ниже)

Assembly parser

Translate assembler RISC-V (ISA RV32I) to machine code. The program must be written in small letters, pseudoinstructions are not processed, labels must be on a separate line

usage: python translator_riscv.py [-h] [-f F] [-m M] [-bin BIN] [-hex HEX]

options:
  -h, --help  show help message and exit
  -f F        Input assembler file
  -m M        Make output binary file for ModelSim (with _ ), default 1, set 0 to off
  -bin BIN    Make output binary file, set 1 to on
  -hex HEX    Make output hex file, set 1 to on

(russian)

Транслятор с языка Ассемблер RISC-V (ISA RV32I) в машинный код. Ограничения: программа должна быть написана маленькими буквами, метки должны находиться на отдельной строке без пробелов, псевдоиструкции не поддерживаются.

Использование: python translator_riscv.py [-h] [-f F] [-m M] [-bin BIN] [-hex HEX]

Опции:
  -h, -help вывести информацию и выйти
  
  -f F      входной файл на языке ассемблер
  
  -m M      сформировать выходной файл с разделением полей команды символом нижнее подчёркивание, по умолчанию 1 (включено), установите 0, чтобы выключить
  
  -bin BIN  сформировать выходной двоичный код, установите 1, чтобы включить
  
  -hex HEX  сформировать выходной шестнадцатеричный код, установите 1, чтобы включить
