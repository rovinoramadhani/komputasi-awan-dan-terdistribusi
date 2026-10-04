"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Skeleton ini sengaja belum lengkap. Isi bagian bertanda TODO.
Jangan mengubah nama fungsi (dipakai untuk pengecekan otomatis oleh asisten).
"""

import random
import threading
import time

NUM_ORDERS = 100
NUM_WORKERS = 10

# Counter bersama untuk menghitung total pesanan yang berhasil diproses.
processed_count = 0

# TODO 1: Lock untuk melindungi processed_count.
lock = threading.Lock()


def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count

    # Simulasikan kerja nyata
    time.sleep(random.uniform(0.001, 0.01))

    # TODO 2: Increment dengan proteksi Lock.
    with lock:
        current = processed_count
        time.sleep(0.001)
        processed_count = current + 1


def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    order_ids = list(range(1, NUM_ORDERS + 1))

    # TODO 3: Bagi order ke NUM_WORKERS thread.
    threads = []

    # Hitung jumlah order untuk setiap worker.
    chunk_size = len(order_ids) // NUM_WORKERS

    for i in range(NUM_WORKERS):
        start = i * chunk_size

        # Worker terakhir mengambil sisa order jika pembagian tidak rata.
        if i == NUM_WORKERS - 1:
            end = len(order_ids)
        else:
            end = start + chunk_size

        assigned_orders = order_ids[start:end]

        thread = threading.Thread(
            target=worker,
            args=(assigned_orders,)
        )

        threads.append(thread)
        thread.start()

    # Tunggu semua thread selesai.
    for t in threads:
        t.join()

    print(
        f"Total pesanan diproses: "
        f"{processed_count} (seharusnya {NUM_ORDERS})"
    )

    if processed_count != NUM_ORDERS:
        print(
            "RACE CONDITION TERDETEKSI - "
            "lengkapi TODO 1 & TODO 2 dengan Lock!"
        )


if __name__ == "__main__":
    main()
