import time
from src.warehouse import *
import getpass


def login():
    MAX_ATTEMPTS = 3
    WAIT_TIME = 1

    print("\n{:^40}".format("===== Selamat datang di Gudang Obatku! ====="))
    
    username = "WINKEY"
    password = "123"

    while True:
        for attempt in range(MAX_ATTEMPTS):
            input_username = input("Masukkan username: ").upper()
            input_password = getpass.getpass("Masukkan password: ")
            if input_username == username and input_password == password:
                print("\nLogin berhasil!")
                return True
            else:
                print("\nUsername atau password salah. Silakan coba lagi.")
        
        print(f"Anda telah mencoba {MAX_ATTEMPTS} kali. Silakan tunggu selama {WAIT_TIME} detik.")
        time.sleep(WAIT_TIME)
        WAIT_TIME *= 2

if login():
    print("Akses diberikan.")
    time.sleep(1)
    clear_screen()
    
    # Kode akses setelah login berhasil
    # ...
else:
    print("Akses ditolak.")

db = initialize_db()


while True:
        clear_screen()
        print("\n=== Warehouse Obat ===")
        print("\n1. Lihat Stock Obat")
        print("2. Tambah Obat Baru")
        print("3. Update Obat")
        print("4. Hapus Obat")
        print("5. Pembelian Obat")
        print("6. Keluar")

        choice = input("\nPilih menu (1-6): ")
        if choice == "1":
            lihat_stock_obat(db)
        elif choice == "2":
            tambah_obat_baru(db)
        elif choice == "3":
            update_obat(db)
        elif choice == "4":
            hapus_obat(db)
        elif choice == "5":
            pembelian_obat(db)
        elif choice == "6":
            print("Terima kasih telah menggunakan Gudang Obatku, sampai jumpa kembali!")
            save_db(db)
            break
        else:
            print("Input tidak valid. Silakan pilih menu yang tersedia.")
            time.sleep(3)
            clear_screen()
