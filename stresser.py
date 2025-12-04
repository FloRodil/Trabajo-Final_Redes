# stress_client.py
"""
Cliente para bombardear la API y comprobar el limitador.

Uso:
    python stress_client.py --rps 50 --duration 5
"""
import argparse
import asyncio
import time
import httpx

async def bombardear(url: str, rps: int, duracion: int):
    intervalo = 1 / rps
    async with httpx.AsyncClient() as cliente:
        fin = time.perf_counter() + duracion
        enviadas = errores = 0

        while time.perf_counter() < fin:
            inicio = time.perf_counter()
            try:
                resp = await cliente.get(url, timeout=10)
                if resp.status_code >= 400:
                    errores += 1
            except Exception:
                errores += 1
            enviadas += 1

            transcurrido = time.perf_counter() - inicio
            await asyncio.sleep(max(0, intervalo - transcurrido))

    print(f"Total enviadas: {enviadas} | Errores: {errores}")

def main():
    parser = argparse.ArgumentParser(description="Cliente de carga para APIs")
    #parser.add_argument("--url", default="http://localhost:8001/ping",
    parser.add_argument("--url", default="http://127.0.0.1:8000/peliculas",
                        help="URL objetivo (endpoint)")
    parser.add_argument("--rps", type=int, default=20,
                        help="Peticiones por segundo")
    parser.add_argument("--duration", type=int, default=10,
                        help="Duración total en segundos")
    args = parser.parse_args()

    asyncio.run(bombardear(args.url, args.rps, args.duration))

if __name__ == "__main__":
    main()
