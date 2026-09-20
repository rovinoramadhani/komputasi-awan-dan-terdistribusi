# Jurnal Proses — Tugas 1

> Jurnal ini merupakan rekonstruksi dari proses diskusi kelompok berdasarkan hasil diskusi dan pembagian analisis yang dikerjakan masing-masing anggota.

## 19 September 2026 — 20.31

1. Peserta: Rovino Ramadhani, Galang Herjuno Mulya, Erastus Liubeta Septian
2. Poin diskusi:
   a. Membahas skenario FoodGo dan mencari masalah yang termasuk *Fallacies of Distributed Computing* serta masalah desain arsitektur.
   b. Rovino mengidentifikasi masalah *Single Point of Failure* karena Order, Payment, dan Notification masih berada pada satu server dan satu proses monolitik.
   c. Galang membahas asumsi *Bandwidth is Infinite*, terutama dampak trafik dan request yang berlebihan terhadap jaringan dan server.
   d. Erastus membahas *Latency is Zero* karena komunikasi antar layanan tetap memiliki latency dan pada skenario belum terdapat mekanisme timeout.
   e. Diskusi juga mengarah pada solusi awal seperti pemisahan service, timeout, caching, rate limiting, dan horizontal scaling.
3. Perbedaan pendapat:
   a. Sempat dibahas apakah seluruh sistem perlu langsung diubah menjadi microservices.
   b. Disepakati bahwa pemisahan service sebaiknya dilakukan berdasarkan fungsi dan kebutuhan beban, bukan memecah seluruh aplikasi menjadi service kecil.

## 20 September 2026 — 22.09

1. Peserta: Rovino Ramadhani, Galang Herjuno Mulya, Erastus Liubeta Septian
2. Poin diskusi:
   a. Melakukan pengecekan kembali hasil analisis masing-masing anggota.
   b. Rovino menambahkan pembahasan *Ketergantungan pada Vertical Scaling* dan *Tight Coupling dan Terlalu Banyak Proses Synchronous*.
   c. Dibahas bahwa peningkatan CPU dan RAM saja tidak menyelesaikan *Single Point of Failure*, sehingga diperlukan *horizontal scaling* dan pemisahan service.
   d. Rovino juga menambahkan pertimbangan desain database ketika aplikasi sudah menggunakan horizontal scaling, yaitu penggunaan *primary database*, *read replica*, dan cache seperti Redis.
   e. Galang memperjelas solusi untuk penggunaan bandwidth melalui caching, pembatasan request, pembatasan ukuran file, dan proses query secara batch.
   f. Erastus memperjelas penggunaan timeout pada komunikasi antar-service serta kebutuhan retry apabila request mengalami kegagalan sementara.
   g. Setiap analisis dilengkapi dengan bagian bukti skenario, alasan kesalahan, dampak, solusi desain awal, dan trade-off.
3. Perbedaan pendapat:
   a. Dibahas penggunaan Kubernetes sebagai solusi scaling. Kesimpulannya, Kubernetes tidak harus langsung digunakan apabila skala FoodGo masih kecil karena menambah kompleksitas operasional.
   b. Untuk proses Notification, disepakati bahwa proses tersebut tidak perlu selalu synchronous dan dapat menggunakan *message queue* agar tidak menahan proses Order.

## Review Silang

1. Galang Herjuno Mulya mengomentari analisis Rovino Ramadhani mengenai *Single Point of Failure*, terutama hubungan antara satu server monolitik dengan risiko seluruh layanan berhenti ketika salah satu bagian mengalami masalah.
2. Rovino Ramadhani mengomentari analisis Erastus Liubeta Septian mengenai *Latency is Zero*, dengan menambahkan bahwa timeout perlu disertai mekanisme retry agar gangguan jaringan sementara tidak langsung menyebabkan proses gagal permanen.
3. Erastus Liubeta Septian mengomentari analisis Galang Herjuno Mulya mengenai *Bandwidth is Infinite*, terutama bahwa pembatasan request dan caching dapat membantu mengurangi beban jaringan ketika trafik FoodGo meningkat.
4. Kelompok melakukan pengecekan akhir agar solusi yang diberikan tetap sesuai dengan permasalahan pada skenario FoodGo dan setiap solusi memiliki trade-off yang dijelaskan.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
