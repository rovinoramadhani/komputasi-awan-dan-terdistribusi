# Kerangka Analisis — Galang Herjuno Mulya


## Tujuan simulasi
- Soon

## Perbandingan hasil percobaan
Simulasi menjalankan 100 pesanan dengan 10 worker thread. Pada percobaan **tanpa `threading.Lock()`**, counter hanya mencapai **46 dari 100**. Beberapa thread membaca nilai `processed_count` yang sama sebelum pembaruan selesai, lalu menulis kembali hasilnya; kenaikan counter yang bertumpang tindih pun hilang. Jurnal mengaitkan kondisi ini dengan *race condition*.

Pada percobaan **dengan `threading.Lock()`**, counter mencapai **100 dari 100**. Lock membatasi akses bersamaan pada bagian kritis yang membaca dan memperbarui counter. Thread lain menunggu sampai lock dilepas, sehingga tidak ada kenaikan yang saling menimpa.


## Eksekusi di Docker
- Soon

## Trade-off dan kesimpulan
- Soon
---