## Analisis - ditulis oleh Erastus Liubeta Septian

Pengujian ini menganalisis prilaku pemrosesan paralel yang membagikan 100 pesanan secara merata ke dalam worker thread. Pada pengujian ini membandigkan aspek eksekusi tanpa proteksi, eksekusi dengan mutex dan validasi pada linkungan kontainer docker.

1. Anatomi Race (Tanpa Lock)
    - Tanpa proteksi singkronasi, nilai akhir (processed_count) hanya mencatat 46 dan 100 pesanan akibat operasi increment yang bersifat non-atomic. Proses penambahan data terbagi menjadi tiga tahap yaitu (read, pause & write), sehingga ketika thread A tertunda oleh time.sleap, tread B ikut membaca nilai usang yang sama sebelum diperbaharui. Akibat interupsi ini terjadi fenomena Lost update sebanyakk 54 kali karana penulisan data antar thread conflict.
    
2. Efektivitas Proteksi Critical Section (Dengan Lock)
    - Penerapan threading.Lock() menggunakan blok with lock berhasil memastikan nilai processed_count terhitung tepat 100 pesanan. Mekanisme ini memaksa thread lain menunggu dan ketika ada satu thread yang sedang memperbaharui data di critical section, Hal ini memberikan jaminan atomisinitas secara penuh, mencegah pembacaan data usang dan memastikan seluruh data transaksi tercatat secara akurat.

3. Konsistensi Eksekusi Lingkungan Container (Docker)
    - Pengujian dalam docker container melalui perintah docker run --rm order-simulator menghasilkan keluaran yang tetap konsisten. Hasil ini membuktikan bahwa primitif sinkronisasi threading.lock memiliki portabilitas tinggi dan bekerja stabil di atas kernel scheduling Linux dan kontainer sama persis seperti saat dieksekusi langsung pada OS host.

4. Evaluasi Implikasi Performa dan Arsitektur
    - Penggunaan Lock membuat proses pengubahan data berjalan bergantian satu persatu dengan total waktu = $$T_{lock} \approx N \times t_{critical}$$ Meskipun harus menunggu program tetap bisa berjalan dengan cepat karena tugas yang berat ditaruh ditaruh di ruang tunggu. Hal ini membuat thread worker tetap dapat menyelesaikan pekerjaan utama secara bersama dan hanya menunggu saat mencatat hasil akhir.