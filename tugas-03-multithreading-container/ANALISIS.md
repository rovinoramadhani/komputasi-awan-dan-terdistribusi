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



