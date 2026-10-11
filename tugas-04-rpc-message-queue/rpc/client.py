"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import time
import xmlrpc.client


def main():
    # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = None  # ganti dengan xmlrpc.client.ServerProxy(...)
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)
    balance = proxy.cek_saldo("user1")
    elapsed = time.time() - start

    print(f"Balance: {balance}")
    print(f"Response time: {elapsed:.2f} seconds")

    print("Memanggil proses_pembayaran('user1', 20000) ...")
    # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
    result = proxy.proses_pembayaran("user1", 20000)
    print(f"Payment result: {result}")


if __name__ == "__main__":
    main()
