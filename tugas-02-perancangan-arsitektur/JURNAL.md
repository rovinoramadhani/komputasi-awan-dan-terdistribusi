# Jurnal Proses — Tugas 2

Jurnal Proses — Tugas 2

## 26 September 2026

1. Kelompok mempelajari kembali studi kasus FoodGo dan permasalahan tight coupling pada arsitektur monolitik dari tugas
   sebelumnya.
2. Kelompok mendiskusikan beberapa gaya arsitektur yang tersedia, terutama Service Oriented Architecture dan Publish
   Subscribe.
3. Diputuskan menggunakan kombinasi Service Oriented Architecture dan Publish Subscribe. SOA digunakan pada proses yang
   membutuhkan respons langsung seperti autentikasi, pembuatan pesanan, pembayaran, dan pengambilan lokasi. Publish
4. Subscribe digunakan untuk proses yang tidak harus menunggu respons langsung seperti pembaruan katalog resto dan
   pencarian kurir.
5. Komponen utama yang dirancang meliputi Pengguna, Modul Autentikasi, Modul Pesanan, Modul Pembayaran, Message Broker,
   Modul Katalog Resto, Modul Notifikasi, Modul Realtime, dan Modul Lokasi.

6. Kelompok mulai menyusun hubungan antar komponen serta menentukan komunikasi mana yang bersifat sinkron dan asinkron.

## 27 September 2026

1. Rancangan arsitektur diterapkan ke dalam diagram dengan memperjelas hubungan antara Modul Pesanan, Modul Pembayaran,
   Message Broker, Modul Katalog Resto, Modul Notifikasi, Modul Realtime, dan Modul Lokasi.

2. Alur skenario end to end disusun mulai dari pengguna melakukan autentikasi, membuat pesanan, melakukan validasi
   pembayaran, menerbitkan event pesanan, memperbarui katalog restoran, mencari kurir, hingga menampilkan informasi
   lokasi.

3. Diagram dan alur komunikasi direvisi untuk memperjelas arah komunikasi serta membedakan HTTP request response, RPC,
   publish event, dan subscribe event.

4. Analisis tertulis dilengkapi dengan pembahasan mengenai pengurangan coupling, isolasi kegagalan server, dan kemampuan
   melakukan penskalaan setiap komponen secara independen.

5. Trade off arsitektur juga dibahas, terutama peningkatan kompleksitas infrastruktur, eventual consistency, serta
   kesulitan debugging pada komunikasi asinkron.

6. Rovino melakukan penyempurnaan rancangan, diagram, alur komunikasi, dan struktur tugas. Galang melengkapi bagian
   analisis tertulis dan trade off. Erastus melakukan review terhadap rancangan dan alur komunikasi yang telah disusun.

7. Setelah dilakukan pengecekan ulang, hasil pekerjaan digabungkan ke branch utama dan README tugas diperbarui dari
   susunan
   dokumen yang telah dibuat.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris
> pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---------|---------|-----------------------|------------------------|--------------------------------------------|
| ...     | ...     | ...                   | ...                    | ...                                        |
