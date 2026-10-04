# Tugas 2 (Pekan 2) — Perancangan Arsitektur untuk FoodGo

**Kelompok:** Kelompok 2

| **Nama**                | **NIM**      | **Kontribusi**                                                                                                                                                                                                                                                 |
|-------------------------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Rovino Ramadhani        | 103072400031 | Menentukan kombinasi gaya arsitektur SOA dan Publish Subscribe, menyusun diagram arsitektur, menyusun alur skenario end to end, menentukan komunikasi sinkron dan asinkron antar modul, serta melakukan revisi dan penyempurnaan diagram serta struktur tugas. |
| Galang Herjuno Mulya    | 103072430006 | Menyusun dan melengkapi analisis tertulis mengenai penyelesaian masalah serta trade off dari arsitektur yang digunakan.                                                                                                                                        |
| Erastus Liubeta Septian | 103072400020 | Melakukan review terhadap rancangan arsitektur dan alur komunikasi antar modul untuk memastikan skenario FoodGo dapat dipahami secara runtut.                                                                                                                  |
## Analisis - ditulis oleh Rovino Ramadhani

Pada tugas ini dilakukan simulasi pemrosesan 100 pesanan menggunakan 10 *thread* yang berjalan secara konkuren.
Pengujian dilakukan dalam dua kondisi, yaitu tanpa menggunakan `Lock` dan setelah menggunakan `threading.Lock()`.

1. Pada kondisi tanpa `Lock`, nilai `processed_count` hanya mencapai `46` dari total `100` pesanan. Hal ini terjadi
   karena beberapa *thread* dapat membaca nilai counter yang sama sebelum proses pembaruan selesai, sehingga sebagian
   hasil increment saling tertimpa.

2. Setelah menggunakan `Lock`, nilai `processed_count` berhasil mencapai `100`. `Lock` membuat proses membaca dan
   memperbarui counter dilakukan secara bergantian sehingga tidak terjadi perubahan data secara bersamaan.

3. Program kemudian dijalankan menggunakan Docker dan tetap menghasilkan nilai `100`. Hal ini menunjukkan bahwa program
   dapat berjalan dengan hasil yang sama ketika dieksekusi secara langsung maupun di dalam container.

Berdasarkan percobaan tersebut, penggunaan sinkronisasi diperlukan ketika beberapa *thread* mengakses dan mengubah data
bersama. Tanpa mekanisme penguncian, hasil proses dapat menjadi tidak konsisten akibat *race condition*. Setelah
menggunakan `Lock`, proses perubahan data menjadi terkontrol dan hasil akhir sesuai dengan jumlah pesanan yang diproses.

---
﻿# Kerangka Analisis — Galang Herjuno Mulya


## Tujuan simulasi
- Dengan adanya simulasi seperti ini, kami dapat mengetahui, apakah eksekusi pesanan yang menggunakan `threading.Lock()` dan tanpa `threading.Lock()` dapat menghasilkan output yang berbeda, pentingnya untuk menggunakan sesuai dengan kebutuhan agar sistem dapat berjalan dengan efisien dan maksimal.

## Perbandingan hasil percobaan
Simulasi menjalankan 100 pesanan dengan 10 worker thread. Pada percobaan **tanpa `threading.Lock()`**, counter hanya mencapai **46 dari 100**. Beberapa thread membaca nilai `processed_count` yang sama sebelum pembaruan selesai, lalu menulis kembali hasilnya; kenaikan counter yang bertumpang tindih pun hilang.

Pada percobaan **dengan `threading.Lock()`**, counter mencapai **100 dari 100**. Lock membatasi akses bersamaan pada bagian kritis yang membaca dan memperbarui counter. Thread lain menunggu sampai lock dilepas, sehingga tidak ada kenaikan yang saling menimpa.


## Eksekusi di Docker
Berdasarkan simulasi yang kami lakukan pada file JURNAL.md selesai tanpa kendala. Screenshot build memperlihatkan tahapan build selesai, lalu perintah `docker run --rm order-simulator` dijalankan. Output container adalah **100 dari 100 pesanan**.

Dibandingkan dengan eksekusi langsung **dengan lock** yang menghasilkan 100, eksekusi dalam container juga menghasilkan 100. Jadi, berdasarkan percobaan yang dicatat, hasil program konsisten di kedua lingkungan. Screenshot tanpa lock menunjukkan nilai 46, hal ini merupakan percobaan kondisi tanpa sinkronisasi, bukan perbandingan lingkungan Docker.

## Trade-off dan kesimpulan
- **Threading** lebih ringan untuk simulasi ini dibanding membuat proses OS baru bagi setiap menjalankan pesanan, tetapi thread harus berbagi data sehingga pembaruan data bersama perlu disinkronkan.
- **Lock** menjaga konsistensi counter, namun hal ini berhadapan biaya yang cukup mahal, yaitu thread lain harus menunggu saat sedang digunakan. Jika lock mencakup pekerjaan yang panjang, waktu tunggu dapat mengurangi proses yang sebeneranya bisa dijalankan secara bersamaan.
- **Docker** membuat program yang dapat dijalankan dalam lingkungan, tetap memerlukan proses build ulang ketika dipindahkan, dan image/container. Bukti yang ada, memang menunjukkan program berjalan dengan baik, namun tidak mengukur konsumsi memori atau kecepatan dibanding pendekatan proses.

## Kesimpulan

Percobaan menunjukkan bahwa multithreading tanpa sinkronisasi bisa saja menghasilkan hitungan yang keliru (46/100), sedangkan penggunaan `threading.Lock()` memiliki hasil yang berbeda, yang dimana  membuat seluruh 100 pesanan terhitung. Hasil di Docker juga 100, sama seperti eksekusi langsung yang menggunakan lock. Oleh karena itu, pada simulasi ini lock diperlukan untuk menjaga data bersama tetap konsisten, dan pada kasus ini Docker berhasil menjalankan program dengan hasil yang sama.

---


