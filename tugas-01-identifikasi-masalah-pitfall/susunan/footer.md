## Kesimpulan Kelompok

Berdasarkan analisis skenario FoodGo, kelompok menyimpulkan bahwa permasalahan utama tidak hanya berasal dari keterbatasan resource server, tetapi juga dari desain sistem terdistribusi yang belum mempertimbangkan kegagalan jaringan, latency, keterbatasan bandwidth, serta ketergantungan antar-komponen. Arsitektur yang masih menggunakan satu server dan proses monolitik menyebabkan *Single Point of Failure*, membatasi kemampuan scaling, serta membuat gangguan pada satu modul dapat berdampak pada keseluruhan sistem.

Solusi yang diusulkan mencakup pemisahan service berdasarkan fungsi, penerapan *horizontal scaling*, penggunaan *timeout* dan *retry*, pemanfaatan proses asynchronous melalui *message queue*, caching, rate limiting, serta pemisahan beban database menggunakan *primary database* dan *read replica*. Namun, setiap solusi memiliki *trade-off* berupa peningkatan kompleksitas arsitektur, monitoring, deployment, konsistensi data, dan kebutuhan pengelolaan infrastruktur yang lebih baik.

Dengan demikian, pengembangan FoodGo sebaiknya dilakukan secara bertahap sesuai kebutuhan dan pertumbuhan trafik, bukan langsung menerapkan seluruh teknologi sekaligus.


[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]