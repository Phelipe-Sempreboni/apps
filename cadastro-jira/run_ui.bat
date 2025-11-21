@echo off
SETLOCAL

REM Ir para o diretório deste .bat
cd /d "%~dp0"

REM Ativar o ambiente virtual
IF EXIST ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) ELSE (
    echo Ambiente virtual .venv nao encontrado.
    echo Crie com: python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
    exit /b 1
)

REM Rodar o Streamlit
streamlit run src\ui\streamlit_app.py

ENDLOCAL
