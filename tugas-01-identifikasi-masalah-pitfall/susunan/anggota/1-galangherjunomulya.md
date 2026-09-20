## Bandwith is Infinite — ditulis oleh Galang Herjuno Mulya

### **Bukti di skenario:** 
1. Aplikasi menjadi lambat, beberapa timeout
2. Server backend kadang crash total dan perlu di-restart manual.
3. Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.


### **Kenapa ini keliru:** 
Bandwith adalah besaran yang memiliki batas, jika developer berpikir jika bandwith adalah infinite, maka bisa saja tidak ada request limit, sehingga membanjiri queue dan dapat menyebabkan network congestion

### **Dampak ke FoodGo:** 

Dampak dari Bandwith is infinite cukup banyak, berikut adalah beberapa dampak yang bisa terjadi :
1. FoodGo dapat mengalami kebanjiran Request dari client karena tidak adanya batasan. Server dapat mengalami lonjakan data yang perlu diolah ataupun request, yang mana ini dapat membebankan server pada saat traffic sedang tinggi. beban server yang melebihi kapasitasnya dapat membuat server menjadi panas, mengalami lag atau yang paling parah down dan perlu direset secara manual. 

2. Secara biaya, bisa dibilang ini adalah kegagalan dengan biaya yang tidak murah, banyaknya request menyebabkan biaya cloud yang dapat membengkak secara masif. Pemanggilan API yang berlebihan dalam satu siklus (misalnya hanya ada perubahan 1 query melalui pemanggilan API) dapat menyebabkan packet loss pada router, load balancer dan jaringan server

### **Solusi desain awal:** 
1. jika ada pengisian form, fitur *auto-save* dilakukan pada perangkat client/lokal, data  akan dikirim ketika *user* menekan tombol *submit*, sehingga server hanya menerima satu POST.

2. Dilakukannya browser caching untuk assets statis, hal ini akan meringankan server karna hanya perlu mengirimkan sekali packet.

3. Membatasi ukuran file *(Rate Limiting)*. Sebelum melakukan pengunggahan, periksa ukuran file, misalnya max 2 MB, jika file melebihi batas yang ditentukan, maka akan ditolak sebelum mengunduh/mengunggah data. Selain itu gunakan juga rate limiter (misalnya 100 request per menit untuk setiap IP) untuk mencegah pembengkakan bandwith/scripting (DdoS)

4. Melakukan Query secara *"batch"*, lakukan *pagination* agar server tidak mengirim ribuan data secara sekaligus. ketika harus mengambil data sekaligus, gunakan batch agar server tidak perlu menerima banyak Request (misalnya : GET /api/user?ids =1,2,3) dibandingkan GET /api/users/1 GET /api/users/1 dan seterusnya.

Secara singkat, Solusi desain awal yang direkomendasikan adalah : 
1. Gunakan fitur Autosave di lokal browser, mengirim data ketika submit
2. Gunakan browser Cache untuk assetes statis
3. Membatasi ukuran file dan request per orang/IP
4. Mengirim Query secara Batch


### **Trade-off:** Berdasarkan solusi yang ditawarkan, terdapat beberapa trade off, diantaranya adalah : 
1. **Kompleksitas Kode dan Arsitektur**
   - menyimpan draf di lokal, menangani kompres gambar sebelum upload serta mengelola status offline/online memerlukan kode yang kompleks
2. **Isu Konsistensi Data**
   - Pengguna bisa saja melihat data yang sudah tidak valid jika metode ini tidak dieksekusi dengan sempurna. mengatur kapan cache harus dibuang atau diperbarui adalah salah satu pilihan yang cukup sulit. jika terlalu sering dibuang, maka cache tidak berguna,jika terlalu longgar, pengguna bisa saja mengambil data yang sudah usang
3. **Risiko Kehilangan Data**
   - Menyimpan data sebelum tombol submit ditekan, memiliki tantangan tersendiri, yaitu jika browser mendadak crash dan data belum sempat disimpan, maka data dapat hilang.
4. **Beban Komputasi Berpindah ke Pengguna**
   - Memprosess/mengelola data besar sebelum dikirim memang menghemat jaringan, namun boros untuk sumber daya CPU. Pengguna yang menggunakan Smartphone/Device dengan spesifikasi rendah, program tersebut dapat membuat aplikasi terasa lambat atau membuat baterai lebih boros
  
5. Fleksibilitas Pengguna

---