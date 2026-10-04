# Kerangka Analisis — Galang Herjuno Mulya


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