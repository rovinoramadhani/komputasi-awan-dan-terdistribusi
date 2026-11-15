# Jurnal Proses - Tugas 7

**Kelompok:** Kelompok 2

**Tanggal:** 15 November 2026

**Topik:** Konsistensi Data pada Sistem Terdistribusi

**Zona Waktu:** WIB (UTC+7)

## Diskusi pemilihan model konsistensi

| Tanggal dan Waktu (WIB) | Anggota / Pelaksana     | Kegiatan dan Hasil                                                                                                                                                                              | Commit                                                                                                                                                                                                                                                         |
|-------------------------|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 15 November 2026, 14.43 | Rovino Ramadhani        | Menyiapkan struktur dokumentasi, konfigurasi `build.json`, berkas analisis individu, dan berkas pendukung. Sebagian konten awal masih berasal dari tugas sebelumnya dan memerlukan penyesuaian. | [cba1205](https://github.com/rovinoramadhani/komputasi-awan-dan-terdistribusi/commit/cba12057b12d224b741bd128fa063b0f130af709)                                                                                                                                 |
| 15 November 2026, 14.47 | Rovino Ramadhani        | Menyesuaikan struktur analisis untuk Tugas 7 serta menyusun jawaban kelompok tentang Eventual Consistency, Sequential Consistency, Read-Your-Writes, dampak bisnis, dan sequence diagram.       | [8251ee6](https://github.com/rovinoramadhani/komputasi-awan-dan-terdistribusi/commit/8251ee617bf7d359cc0e6ff8f19fdee7df7b3e20), [2e516d1](https://github.com/rovinoramadhani/komputasi-awan-dan-terdistribusi/commit/2e516d17fa1c66b02e72d5b86324f9dc50d6c67e) |
| 15 November 2026, 17.21 | Erastus Liubeta Septian | Melengkapi analisis individu terkait kebutuhan konsistensi saldo e-wallet, dampak finansial, mekanisme Read-Your-Writes, hasil simulasi, dan skenario tambahan aplikasi transportasi online.    | [1184bbd](https://github.com/rovinoramadhani/komputasi-awan-dan-terdistribusi/commit/1184bbd5354192ec4b0687a0ef48c7caae39bcd3)                                                                                                                                 |
| 15 November 2026, 22.24 | Galang Herjuno Mulya    | Melengkapi analisis individu mengenai keterlambatan sinkronisasi saldo Jakarta dan Bandung, risiko penolakan transaksi, perbandingan model konsistensi, serta usulan Read-Your-Writes.          | [f407806](https://github.com/rovinoramadhani/komputasi-awan-dan-terdistribusi/commit/f407806a9369ba681c80e556a880fcb9fd96961f)                                                                                                                                 |
| 15 November 2026, 22.59 | Rovino Ramadhani        | Menggabungkan Pull Request #28 yang berisi analisis Galang ke branch `main`, sehingga seluruh analisis individu tersedia pada branch utama.                                                     | [3edd8e7](https://github.com/rovinoramadhani/komputasi-awan-dan-terdistribusi/commit/3edd8e7f169cf669c56e3d720f33706993592d42)                                                                                                                                 |

### Argumen yang Dipertimbangkan

1. **Eventual Consistency:** Memungkinkan perbedaan saldo sementara akibat replikasi tertunda, sehingga berisiko
   menyebabkan transaksi ditolak meskipun pelanggan sudah berhasil melakukan top-up.
2. **Sequential Consistency:** Memberikan jaminan keterurutan operasi yang lebih kuat, tetapi penerapannya perlu
   mempertimbangkan koordinasi dan performa antarserver.
3. **Client-Centric Consistency (Read-Your-Writes):** Memastikan pelanggan dapat membaca perubahan saldo yang telah
   berhasil dilakukan, meskipun mengakses replika yang berbeda.

### Kesimpulan Akhir dan Alasan

Kelompok menyimpulkan bahwa Eventual Consistency murni tidak mencukupi kebutuhan pembacaan saldo e-wallet FoodGo.
Pendekatan Read-Your-Writes dipilih untuk menjamin pelanggan dapat membaca hasil top-up terbaru melalui pemeriksaan
versi data dan pengalihan pembacaan ke replika yang sesuai.

Pendekatan ini tetap memungkinkan replikasi asinkron, sedangkan operasi transaksi keuangan memerlukan mekanisme tambahan
untuk menjamin keamanan perubahan saldo secara bersamaan.

## Simulasi (jika dikerjakan)

### Proses Implementasi dan Dokumentasi

| Tanggal dan Waktu (WIB) | Anggota / Pelaksana | Kegiatan dan Hasil                                                                                                                                                                                                   | Commit                                                                                                                         |
|-------------------------|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| 15 November 2026, 14.50 | Rovino Ramadhani    | Melengkapi program simulasi Python pada `src/replica_simulation.py`, menerapkan keterlambatan replikasi 2 detik, serta mengimplementasikan pemeriksaan versi dan Read-Your-Writes untuk mengatasi inconsistent read. | [435d9d0](https://github.com/rovinoramadhani/komputasi-awan-dan-terdistribusi/commit/435d9d0da4f065caf10d9d82ac030d33f08e47cb) |

Hasil implementasi simulasi kemudian digunakan sebagai dasar analisis kelompok. Rovino Ramadhani membahas perbandingan
hasil pembacaan saldo sebelum dan sesudah penerapan Read-Your-Writes, Galang Herjuno Mulya mengkaji dampak keterlambatan
replikasi terhadap transaksi pelanggan, sedangkan Erastus Liubeta Septian mengevaluasi pendekatan konsistensi dan
penerapannya pada sistem terdistribusi lainnya.

Ketiga hasil analisis tersebut menjadi dasar penyusunan kesimpulan kelompok mengenai pemilihan model konsistensi data
yang sesuai untuk sistem e-wallet FoodGo.

### Hasil Skenario Naif vs. Read-Your-Writes

| Aspek Pengujian                  | Tanpa Read-Your-Writes  | Dengan Read-Your-Writes         |
|----------------------------------|-------------------------|---------------------------------|
| Operasi top-up                   | Rp50.000                | Tambahan Rp20.000               |
| Saldo terbaru                    | Rp50.000                | Rp70.000                        |
| Saldo yang terbaca               | Rp0                     | Rp70.000                        |
| Server pembacaan akhir           | Bandung                 | Jakarta (redirect)              |
| Versi data yang diperlukan       | Versi 1                 | Versi 2                         |
| Kondisi replikasi saat pembacaan | Belum selesai           | Belum selesai                   |
| Hasil                            | Inconsistent Read (BUG) | Read-Your-Writes (BUG TERATASI) |

Pada skenario pertama, pembacaan saldo dari Bandung dilakukan 0,5 detik setelah top-up Rp50.000 di Jakarta. Karena
keterlambatan replikasi selama 2 detik, saldo Bandung masih menunjukkan Rp0.

Pada skenario kedua, setelah top-up tambahan Rp20.000, saldo Jakarta menjadi Rp70.000 dengan versi 2. Bandung masih
memiliki versi 1, sehingga sistem mengalihkan pembacaan ke Jakarta dan mengembalikan saldo terbaru.

**Bukti hasil pengujian:** [bukti/output.png](bukti/output.png)

### Kesimpulan Simulasi

Hasil simulasi menunjukkan bahwa keterlambatan replikasi dapat menyebabkan pembacaan saldo lama (*stale read*).
Penerapan Read-Your-Writes melalui pemeriksaan nomor versi dan pengalihan pembacaan berhasil mengatasi masalah tersebut
pada skenario yang diuji tanpa harus menunggu sinkronisasi seluruh replika.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris
> pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---------|---------|-----------------------|------------------------|--------------------------------------------|
| ...     | ...     | ...                   | ...                    | ...                                        |
