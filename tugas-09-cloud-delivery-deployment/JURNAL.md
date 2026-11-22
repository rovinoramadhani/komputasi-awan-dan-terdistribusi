# Jurnal Proses - Tugas 9

## Diskusi deployment model, risiko, dan mitigasi - (22 November 2026 21.14 WIB)

- Membandingkan Private Cloud murni dan Hybrid Cloud untuk Sistem Data Kependudukan.
- Membahas keterbatasan rapid elasticity pada Private Cloud murni akibat kapasitas fisik dan proses pengadaan, serta
  risiko pemborosan jika kapasitas puncak selalu disediakan.
- Membahas Hybrid Cloud sebagai alternatif dengan database inti tetap di infrastruktur pemerintah.
- Menimbang rekomendasi Private Cloud berdasarkan karakteristik NIST serta kebutuhan kerahasiaan dan skalabilitas.
- Mengidentifikasi risiko lonjakan permintaan, penyalahgunaan akses oleh instansi mitra, dan gangguan pusat data.
- Membahas mitigasi berupa perencanaan kapasitas, pengendalian akses, pemantauan, dan pusat data cadangan.

## Diskusi service model dan rancangan arsitektur - (22 November 2026 20.48 WIB)

- Memetakan IaaS untuk database inti dan PaaS untuk portal publik serta API verifikasi NIK/KYC.
- Merancang akses masyarakat dan instansi melalui portal atau API Gateway.
- Membatasi akses ke database inti melalui layanan internal dengan hak akses terkontrol.
- Membahas diagram arsitektur yang menghubungkan portal, API Gateway, layanan internal, dan database inti.

## Persiapan dokumen dan identitas kelompok - (22 November 2026 19.49 WIB)

- Menyiapkan struktur dokumen Tugas 9 tentang Cloud Delivery & Deployment Model.
- Mencantumkan identitas anggota kelompok.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris
> pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.
>

| Tanggal          | Tool AI | Prompt yang diberikan                                                                                                                                                               | Ringkasan saran/ide AI                                                                                                                                                                 | Bagaimana diolah jadi tulisan/kode sendiri                                                                                                       |
|------------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| 23 November 2026 | ChatGPT | Apa dampak jika data di-host atau berada di server pihak ketiga, terutama pihak asing, padahal datanya sensitif seperti NIK atau KTP? | AI memberi gambaran umum tentang kendali data, privasi, keamanan, lokasi penyimpanan, dan ketergantungan pada penyedia layanan pihak ketiga. | Kelompok menggunakan gambaran tersebut sebagai bahan brainstorming untuk mempertimbangkan kerahasiaan dan kendali data saat membahas deployment model. |
| 23 November 2026 | ChatGPT | Ide apa yang dapat dipertimbangkan untuk deployment model, pemetaan service model, dan risiko sistem data kependudukan yang menyimpan data sensitif serta melayani banyak instansi? | Memberikan bahan brainstorming berupa pertimbangan kendali data dan skalabilitas, pemetaan awal IaaS dan PaaS, serta kemungkinan risiko kapasitas, hak akses, dan gangguan pusat data. | Kelompok menilai relevansi ide terhadap studi kasus, memilih pembahasan yang sesuai, lalu menyusun rekomendasi, alasan, dan mitigasinya sendiri. |
