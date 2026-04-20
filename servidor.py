"""
Voice Commander - Servidor Python para Windows
=============================================
Instale as dependências:
    pip install websockets

Execute:
    python servidor.py

Deixe rodando em segundo plano enquanto usa o app HTML.
"""

import asyncio
import json
import subprocess
import os
import websockets

# ── COMANDOS WINDOWS ──────────────────────────────────────────────
def executar(comando):
    print(f"[CMD] Executando: {comando}")

    if comando == "shutdown":
        subprocess.run(["shutdown", "/s", "/t", "5"], shell=True)

    elif comando == "restart":
        subprocess.run(["shutdown", "/r", "/t", "5"], shell=True)

    elif comando == "sleep":
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], shell=True)

    elif comando == "lock":
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], shell=True)

    elif comando == "notepad":
        subprocess.Popen(["notepad.exe"])

    elif comando == "calculator":
        subprocess.Popen(["calc.exe"])

    elif comando == "explorer":
        subprocess.Popen(["explorer.exe"])

    elif comando == "browser":
        # Abre o navegador padrão
        os.startfile("https://www.google.com")

    else:
        print(f"[AVISO] Comando desconhecido: {comando}")

# ── WEBSOCKET HANDLER ─────────────────────────────────────────────
async def handler(websocket):
    addr = websocket.remote_address
    print(f"[+] Cliente conectado: {addr}")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                cmd = data.get("command", "")
                print(f"[REC] Recebido: {cmd}")
                executar(cmd)
                await websocket.send(json.dumps({"status": "ok", "command": cmd}))
            except json.JSONDecodeError:
                print("[ERRO] JSON inválido recebido.")
    except websockets.exceptions.ConnectionClosed:
        print(f"[-] Cliente desconectado: {addr}")

# ── MAIN ──────────────────────────────────────────────────────────
async def main():
    print("=" * 45)
    print("  Voice Commander - Servidor Local")
    print("  Porta: 8765  |  Host: localhost")
    print("=" * 45)
    print("[OK] Aguardando conexão do app...")
    print("     (Pressione Ctrl+C para encerrar)\n")

    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # roda para sempre

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[ENCERRADO] Servidor parado.")
