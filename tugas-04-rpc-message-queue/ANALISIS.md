# Tugas 4 (Pekan 4) - RPC Message Queue

**Kelompok:** Kelompok 2

| **Nama**                | **NIM**      | **Kontribusi** |
|-------------------------|--------------|----------------|
| Rovino Ramadhani        | 103072400031 |                |
| Galang Herjuno Mulya    | 103072430006 |                |
| Erastus Liubeta Septian | 103072400020 |                |



## Kesimpulan Kelompok

Berdasarkan hasil pengujian dan analisis kelompok, penggunaan multithreading memungkinkan beberapa pekerjaan diproses
secara bersamaan, tetapi penggunaan data bersama tanpa mekanisme sinkronisasi dapat menyebabkan *race condition*. Pada
percobaan tanpa `threading.Lock()`, nilai `processed_count` hanya mencapai 46 dari 100 pesanan karena beberapa thread
membaca dan memperbarui nilai yang sama secara bersamaan sehingga terjadi *lost update*.

Setelah menggunakan `threading.Lock()`, seluruh 100 pesanan berhasil tercatat dengan benar. Lock memastikan bagian
*critical section* hanya diakses oleh satu thread pada satu waktu sehingga perubahan data bersama tetap konsisten.
Konsekuensinya, thread lain harus menunggu ketika Lock sedang digunakan sehingga bagian yang dilindungi sebaiknya dibuat
sesingkat mungkin agar tidak mengurangi keuntungan pemrosesan secara konkuren.

Pengujian menggunakan Docker juga menghasilkan 100 dari 100 pesanan, sama dengan eksekusi langsung yang menggunakan
Lock. Hal ini menunjukkan bahwa program dan mekanisme sinkronisasi tetap menghasilkan perilaku yang konsisten ketika
dijalankan di dalam container.

Secara keseluruhan, multithreading tepat digunakan untuk menjalankan pekerjaan secara konkuren, sedangkan Lock
diperlukan ketika beberapa thread mengakses dan mengubah data bersama. Docker berperan dalam menyediakan lingkungan
eksekusi yang konsisten tanpa mengubah logika sinkronisasi pada program.

