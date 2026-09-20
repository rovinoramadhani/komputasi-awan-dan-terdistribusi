# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 2

| **Nama**                | **NIM**      | **Kontribusi**                                                                                                                                                                                                   |
| ----------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rovino Ramadhani        | 103072400031 | Single Point of Failure, Ketergantungan pada Vertical Scaling, Tight Coupling dan Terlalu Banyak Proses Synchronous, Desain Database saat Horizontal Scaling, Data yang Sering Diakses Membebani Database Utama  |
| Galang Herjuno Mulya    | 103072430006 | Bandwith is Infinite                                                                                                                                                                                             |
| Erastus Liubeta Septian | 103072400020 | Latency is Zero                                                                                                                                                                                                  |


## Pitfall 1: Single Point of Failure — ditulis oleh Rovino Ramadhani

**Bukti di Skenario:** Skenario menyebutkan bahwa pesanan, pembayaran, dan notifikasi kurir berjalan pada satu server dan satu proses monolitik yang sama. Ketika backend crash, server harus direstart secara manual.

**Kenapa ini keliru:** Semua fungsi penting FoodGo memiliki satu *failure domain* yang sama. Jika satu proses mati, seluruh fungsi ikut berhenti. Misalnya modul Notification mengalami *memory leak*. Walaupun Order dan Payment sebenarnya masih normal, seluruh aplikasi dapat ikut crash karena semuanya berjalan pada proses yang sama. Selain itu, setiap modul menggunakan CPU dan RAM server yang sama.

**Dampak ke FoodGo:** Pada jam makan siang jumlah pesanan meningkat. Order membutuhkan CPU untuk memproses pesanan, Payment membutuhkan koneksi dan resource untuk transaksi, sedangkan Notification harus mengirim banyak pemberitahuan kepada kurir. Karena semuanya berjalan pada satu proses dan server yang sama, seluruh modul saling berebut resource. Jika salah satu bagian menyebabkan penggunaan memory berlebihan, seluruh aplikasi dapat berhenti sehingga Order, Payment, dan Notification semuanya tidak tersedia.

**Solusi desain awal:** FoodGo tidak harus langsung mengubah setiap fungsi menjadi microservice kecil. Pemisahan dapat dilakukan berdasarkan fungsi dan karakteristik beban. Contohnya:

1. **Order Service** untuk mengelola pembuatan dan status pesanan.
2. **Payment Service** untuk mengelola transaksi pembayaran.
3. **Authentication Service** untuk mengelola login, token, dan akun pengguna.
4. **Notification Service** untuk mengelola event notifikasi.
5. **Realtime Service** untuk mengelola informasi yang membutuhkan update secara realtime.
6. **Location atau Maps Service** untuk mengelola kebutuhan lokasi, koordinat, dan integrasi map.

Service seperti Order, Authentication, dan Payment tetap dapat menggunakan pola API *request-response*. Notification, tracking, dan beberapa proses realtime dapat menggunakan event dan *message queue*.

**Trade-off:** Pemisahan menjadi beberapa service meningkatkan kompleksitas karena FoodGo harus menangani *service discovery*, network communication, distributed logging, monitoring, authentication antar-service, deployment banyak aplikasi, distributed tracing, dan konsistensi data antar-service. Karena itu, pemisahan service dilakukan berdasarkan kebutuhan, bukan sekadar memecah seluruh kode menjadi service kecil.

---

## Pitfall 2: Ketergantungan pada Vertical Scaling — ditulis oleh Rovino Ramadhani

**Bukti di Skenario:** Skenario tidak menyatakan secara eksplisit bahwa FoodGo telah melakukan *vertical scaling*. Namun, karena seluruh aplikasi berada pada satu server, arsitektur tersebut membuat pilihan scaling terbatas dan mendorong penggunaan vertical scaling.

**Kenapa ini keliru:** Vertical scaling hanya meningkatkan kapasitas satu server, misalnya dari 4 CPU dan 8 GB RAM menjadi 16 CPU dan 32 GB RAM. Penambahan resource dapat meningkatkan kapasitas server, tetapi tidak menghilangkan *single point of failure*. Jika proses aplikasi crash, seluruh sistem tetap berhenti. Selain itu, satu server memiliki batas maksimum CPU dan RAM.

**Dampak ke FoodGo:** Ketika trafik meningkat, FoodGo harus menaikkan kapasitas server secara keseluruhan walaupun peningkatan beban hanya terjadi pada satu fungsi. Misalnya, jika Order menerima trafik tinggi, resource untuk Payment dan Notification ikut berada pada mesin yang sama. Jika server gagal, seluruh layanan tetap tidak tersedia walaupun kapasitas server telah diperbesar.

**Solusi desain awal:** FoodGo menggunakan kombinasi `Horizontal Scaling` dan `Service Separation`. Order Service, Payment Service, dan Notification Service dapat memiliki beberapa instance, kemudian trafik didistribusikan melalui `Load Balancer`. Ketika Order Service menerima trafik tinggi, FoodGo cukup menambah instance Order Service tanpa meningkatkan kapasitas Notification Service. Jika jumlah service dan trafik sudah besar, container dapat dikelola menggunakan Kubernetes untuk menjalankan replica, health check, mengganti container yang mati, rolling deployment, mengatur resource, dan menggunakan `Horizontal Pod Autoscaler`.

**Trade-off:** Horizontal scaling dan Kubernetes meningkatkan kompleksitas operasional. FoodGo membutuhkan monitoring, konfigurasi cluster, networking, security policy, deployment pipeline, dan kemampuan DevOps. Untuk sistem yang masih kecil, beberapa container dan load balancer lebih sederhana dibanding langsung menggunakan Kubernetes.

---

## Pitfall 3: Tight Coupling dan Terlalu Banyak Proses Synchronous — ditulis oleh Rovino Ramadhani

**Bukti di Skenario:** Order memanggil Payment kemudian menunggu respons. Selain itu, Order, Payment, dan Notification berada pada satu proses aplikasi. Kondisi ini membuat komponen memiliki keterikatan yang tinggi.

**Kenapa ini keliru:** Jika seluruh proses harus selesai secara berurutan sebelum request pengguna dianggap berhasil, keterlambatan atau kegagalan satu komponen ikut menahan komponen lain. Tidak semua proses membutuhkan hasil langsung. Contohnya, pengguna tidak perlu menunggu sampai push notification benar-benar diterima perangkat kurir agar proses Order dianggap selesai.

**Dampak ke FoodGo:** Misalnya urutan proses adalah pesanan dibuat, pembayaran diproses, lalu notifikasi kurir dikirim. Jika Notification lambat atau gagal, request Order ikut menjadi lambat atau gagal walaupun data pesanan dan pembayaran sebenarnya telah diproses.

**Solusi desain awal:** Proses dibedakan menjadi synchronous dan asynchronous. Login, membuat pesanan, memulai pembayaran, dan mengambil informasi akun tetap menggunakan API synchronous. Pengiriman notifikasi, email, log aktivitas, analytics, dan beberapa proses tracking menggunakan *message broker*. Setelah Order Service berhasil membuat pesanan, Order Service mengirim event seperti `ORDER_CREATED`. Notification Service kemudian membaca event tersebut dan mengirim notifikasi secara terpisah. Untuk push notification, Notification Service dapat meneruskan pesan ke Firebase Cloud Messaging sehingga infrastruktur FoodGo tidak menangani seluruh proses pengiriman sampai ke perangkat.

**Trade-off:** Arsitektur asynchronous menghasilkan `eventual consistency`. Notifikasi tidak selalu muncul pada waktu yang sama dengan perubahan data. Sistem juga harus menangani message yang diproses lebih dari sekali, gagal diproses, atau tertunda. Penggunaan third-party seperti Firebase juga menambahkan biaya API, limit penggunaan, risiko perubahan harga, vendor lock-in, dan ketergantungan pada ketersediaan provider.

---

## Masalah Desain 4: Desain Database saat Horizontal Scaling — ditulis oleh Rovino Ramadhani

**Bukti di Skenario:** Bagian database tidak dijelaskan secara langsung dalam skenario sehingga masalah ini tidak dapat dibuktikan sebagai pitfall dari teks kasus. Namun, ketika FoodGo mulai menggunakan horizontal scaling, database dapat menjadi bottleneck berikutnya.

**Kenapa ini keliru:** Jika seluruh operasi read dan write tetap diarahkan ke satu database, peningkatan jumlah instance aplikasi tidak otomatis menghilangkan bottleneck pada database. Beban query dapat tetap terpusat pada satu primary database.

**Dampak ke FoodGo:** Misalnya terdapat 5.000 operasi write per menit dan 50.000 operasi read per menit. Jika seluruhnya menuju database yang sama, primary database dapat menjadi bottleneck dan memperlambat layanan yang bergantung padanya.

**Solusi desain awal:** FoodGo menggunakan relational database dengan `primary database` untuk operasi write seperti membuat order, memperbarui pembayaran, dan mengubah status transaksi. Satu atau beberapa `read replica` digunakan untuk query yang dominan membaca data seperti riwayat pesanan, daftar restoran, daftar menu, informasi profil, dan laporan tertentu.

**Trade-off:** Read replica memiliki risiko `replication lag`. Pengguna yang baru membayar dapat membaca status pembayaran lama apabila replica belum menerima update. Data yang membutuhkan `strong consistency`, terutama setelah transaksi penting, tetap dibaca dari primary database.

---

## Masalah Desain 5: Data yang Sering Diakses Membebani Database Utama — ditulis oleh Rovino Ramadhani

**Bukti di Skenario:** Penggunaan cache atau pola akses database tidak dijelaskan secara langsung dalam skenario sehingga masalah ini bukan pitfall yang dapat dibuktikan dari teks kasus. Bagian ini merupakan pertimbangan desain ketika jumlah request FoodGo meningkat.

**Kenapa ini keliru:** Jika data yang sama dan sering diakses selalu diambil langsung dari database utama, query berulang akan menambah beban database walaupun data tersebut tidak sering berubah.

**Dampak ke FoodGo:** Misalnya halaman utama FoodGo dibuka 100.000 kali. Jika setiap request melakukan query yang sama ke PostgreSQL, beban database meningkat dan dapat memengaruhi request lain.

**Solusi desain awal:** FoodGo menggunakan in-memory database atau cache seperti Redis untuk data yang membutuhkan akses cepat, misalnya daftar restoran populer, informasi menu yang sering dibuka, konfigurasi UI, session tertentu, rate limit, status sementara, dan data dengan TTL. Hasil query tertentu dapat disimpan selama beberapa menit sehingga request berikutnya mengambil data dari memory tanpa selalu mengakses database utama.

**Trade-off:** Cache menghasilkan masalah `cache invalidation`. Ketika harga makanan berubah di database utama tetapi cache belum diperbarui, pengguna dapat melihat informasi lama. Karena itu cache harus memiliki TTL dan strategi invalidation yang jelas.

## Pitfall 3: Latency is zero — Erastus Liubeta Septian

**Bukti di skenario:** "Aplikasi jadi sangat lambat, beberapa permintaan timeout." & "tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)"

**Kenapa ini keliru:** Karena proses pemesanan juga memanfaatkan pemanggilan layanan lain seperti gateway pembayaran, kalkulasi rute dari lokasi pemesanan, dan searching makanan atau restoran. Dengan menganggap trnsfer data setiap layanan terjadi tanpa ada nya latency hal ini merupakan sebuah kekeliruan, setiap koneksi yang terbentuk sistem harus melakukan hanshake-ing jika ingin berkomunikasi dengan layanan lainya lalu, perjalanan data fisik melintasi berbagai perangkat keras seperti kabel FO, router atau access point, dan setiap router butuh waktu untuk memerika paket header dan menentukan point tujuan selanjutnya dan andai kata terjadi penumpukan atau salah satu layanan terlalu banyak menerima request, layanan lain harus mengantri di buffer layanan tersebut sebelum akhirnya dapat di proses kembali, dan masih banyak hal lain yang terjadi di belakang sebuah sistem pemesanan. Semua hal diatas menyebabkan sebuah proses pemesanan ini pasti akan memiliki latency. Lalu pada skenario tersebut dapat disimpulkan juga bahwa Tim menganggap latancy selalu 0 karena sistem atau kode mereka tidak menerapkan timeout sama sekali yang mengakibatkan modul pemesanan dibiarkan menunggu respon modul pembayaran tanpa batas waktu yang ditetapkan.

**Dampak ke FoodGo:** Ketika terjadi keterlambatan pada modul pembayaran, modul pesanan yang terhubung dengannya juga ikut terpengaruh dengan dengan hal yang sama karena tidak ada pengaturan untuk timeout, sehingga modul pemesanan tetap melakukan proses hingga memanfaatkan sesluruh kapasitas dari RAM dan juga CPU server yang berakibat pada server akan mengalami crash dan memrlukan restart secara manual

**Solusi desain awal:** Langkah yang dapat diambil adalah dengan menetapkan timeout pada request antar modul dengan contoh rentang waktu sekitar 2-3 detik. Jika durasi timeout ini terlampaui, sistem akan segera memberikan laporan bahwa request tersebut gagal atau pending, agar sumber daya server dapat dialokasikan untuk pemrosesan lainnya.

**Trade-off:** Pemanfaatan timeout dapat menyebabkan beberapa peroses transfer data mengalami kegagalan yang disebabkan penurunan kecepatan internet sementara (> 2-3 detik). Melihat kemungkinan itu, tim IT harus menambahkan fitur seperti retry secara otomatis untuk memastikan trasfer data tetap terjaga dan sinkron.
## Kesimpulan Kelompok

Berdasarkan analisis skenario FoodGo, kelompok menyimpulkan bahwa permasalahan utama tidak hanya berasal dari keterbatasan resource server, tetapi juga dari desain sistem terdistribusi yang belum mempertimbangkan kegagalan jaringan, latency, keterbatasan bandwidth, serta ketergantungan antar-komponen. Arsitektur yang masih menggunakan satu server dan proses monolitik menyebabkan *Single Point of Failure*, membatasi kemampuan scaling, serta membuat gangguan pada satu modul dapat berdampak pada keseluruhan sistem.

Solusi yang diusulkan mencakup pemisahan service berdasarkan fungsi, penerapan *horizontal scaling*, penggunaan *timeout* dan *retry*, pemanfaatan proses asynchronous melalui *message queue*, caching, rate limiting, serta pemisahan beban database menggunakan *primary database* dan *read replica*. Namun, setiap solusi memiliki *trade-off* berupa peningkatan kompleksitas arsitektur, monitoring, deployment, konsistensi data, dan kebutuhan pengelolaan infrastruktur yang lebih baik.

Dengan demikian, pengembangan FoodGo sebaiknya dilakukan secara bertahap sesuai kebutuhan dan pertumbuhan trafik, bukan langsung menerapkan seluruh teknologi sekaligus.

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
