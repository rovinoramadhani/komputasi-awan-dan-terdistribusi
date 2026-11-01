"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8  # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        if node_id in self.nodes:
            print(f"[JOIN] Gagal: node hash {node_id} sudah terdaftar.")
            return

        if self.nodes:
            old_successor = self.find_successor(node_id)
            old_predecessor = max(
                (existing_id for existing_id in self.nodes if existing_id < node_id),
                default=max(self.nodes)
            )
        else:
            old_successor = None
            old_predecessor = None

        self.nodes[node_id] = node_ip
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        if old_successor is not None:
            print(f"  Rentang ({old_predecessor}, {node_id}] beralih dari node {old_successor} ke node {node_id}")
        else:
            print("  Node pertama mengambil seluruh rentang ring.")

        moved = 0
        for key_hash, (kurir_id, ip_kurir) in self.data.items():
            if self.find_successor(key_hash) == node_id and old_successor is not None:
                print(f"  Mapping {kurir_id} (hash={key_hash}, IP={ip_kurir}): node {old_successor} -> node {node_id}")
                moved += 1

        print(f"  Total mapping berpindah: {moved}")
        print(f"  Ring saat ini: {sorted(self.nodes)}")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            print(f"[LEAVE] Gagal: node '{node_name}' (id={node_id}) tidak ditemukan.")
            return

        if len(self.nodes) == 1 and self.data:
            print(f"[LEAVE] Gagal: node '{node_name}' adalah node terakhir dan masih ada data kurir.")
            return

        old_predecessor = max(
            (existing_id for existing_id in self.nodes if existing_id < node_id),
            default=max(self.nodes)
        ) if len(self.nodes) > 1 else None

        owned_keys = [
            (key_hash, kurir_id, ip_kurir)
            for key_hash, (kurir_id, ip_kurir) in self.data.items()
            if self.find_successor(key_hash) == node_id
        ]

        del self.nodes[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring")

        if self.nodes:
            new_successor = self.find_successor(node_id)
            print(f"  Rentang ({old_predecessor}, {node_id}] beralih dari node {node_id} ke node {new_successor}")

            for key_hash, kurir_id, ip_kurir in owned_keys:
                print(f"  Mapping {kurir_id} (hash={key_hash}, IP={ip_kurir}): node {node_id} -> node {new_successor}")
        else:
            print("  Ring sekarang kosong.")

        print(f"  Total mapping berpindah: {len(owned_keys)}")
        print(f"  Ring saat ini: {sorted(self.nodes)}")

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""

        if not self.nodes:
            raise ValueError("Ring kosong, tidak ada successor.")

        sorted_nodes = sorted(self.nodes)

        for node_id in sorted_nodes:
            if node_id >= key_hash:
                return node_id

        return sorted_nodes[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)

        if key_hash in self.data and self.data[key_hash][0] != kurir_id:
            raise ValueError(f"Collision hash {key_hash} antara ID kurir yang berbeda.")

        node_id = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)

        print(f"[REGISTER] {kurir_id} (hash={key_hash}) -> {ip_kurir}, node penanggung jawab: {node_id}")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)

        if not self.nodes:
            return None

        node_id = self.find_successor(key_hash)
        data_kurir = self.data.get(key_hash)

        if data_kurir is None or data_kurir[0] != kurir_id:
            print(f"[LOOKUP] {kurir_id} (hash={key_hash}) tidak ditemukan; successor: {node_id}")
            return None

        print(f"[LOOKUP] {kurir_id} (hash={key_hash}) ditemukan di node {node_id}")
        return data_kurir[1]


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Daftarkan beberapa kurir
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")
    ring.register_kurir("kurir-012", "192.168.1.13")
    ring.register_kurir("kurir-005", "192.168.1.14")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()
