# Dinopedia (CLI) - Version 1.0
# A command-line interface for exploring dinosaur information 

# Module
import json
import os

# Database of dino
dinopedia = []

# ===========
# ADD FUNCTION
# ===========
def add_dinosaur():
    print("\n== 📝Tambah Dinosaur📝 ==")
    name = input("Nama: ")
    period = input("Periode(Triassic/Jurassic/Cretaceous): ")
    diet = input("Diet(Hebivore/Carnivore/Omnivore): ")

    dinosaur = {
        "nama": name,
        "periode": period,
        "diet": diet
    }

    dinopedia.append(dinosaur)
    save_to_json() # Save to Json after adding a new dinosaur
    print(f"Dinosaur '{name}' berhasil ditambahkan")

# ===========
# JSON FUNCTION
# ===========
def save_to_json():
    with open('dinopedia.json', 'w') as f:
        json.dump(dinopedia, f, indent=4)
    
def load_from_json():
    global dinopedia
    if not os.path.exists('dinopedia.json'):
        with open('dinopedia.json', 'w') as f:
            json.dump([], f) # Create an empty list in the JSON file if it doesn't exist

    with open('dinopedia.json', 'r') as f:
        dinopedia = json.load(f)
    
# ===========
# DELETE FUNCTION
# ===========
def delete_dinosaur():
    print("\n== 🗑️ Hapus Dinosaur 🗑️ ==")
    view_dino()
    name = input("masukkan nama dinosaur yang ingin dihapus:")
    for d in dinopedia:
        if d['nama'].lower() == name.lower():
            dinopedia.remove(d)
            save_to_json() # Save to Json after deleting a dinosaur
            print(f"Dinosaur '{name}' berhasil dihapus.")

# ===========
# VIEW FUNCTION
# ===========
def view_dino():
    print("\n== 📋Daftar Dinosaur📋 ==")

    if not dinopedia:
        print("Belum ada dinosaur yang ditambahkan.")
        return
    
    for i, d in enumerate(dinopedia, start=1):
        print(f"{i}. Nama: {d['nama']} | Periode: {d['periode']} | Diet: {d['diet']}")

    print()

# ===========
# EDIT FUNCTION
# ===========
def edit_dinosaur():
    print("\n== ✏️ Edit Dinosaur ✏️ ==")
    view_dino()
    name = input("Masukkan nama dinosaur yang ingin diedit: ")
    for d in dinopedia:
        if d['nama'].lower() == name.lower():
            new_name = input("Nama baru (tekan Enter untuk tidak mengubah): ")
            new_period = input("Periode baru (tekan Enter untuk tidak mengubah): ")
            new_diet = input("Diet baru (tekan Enter untuk tidak mengubah): ")

            if new_name:
                d['nama'] = new_name
            if new_period:
                d['periode'] = new_period
            if new_diet:
                d['diet'] = new_diet

            save_to_json() # Save to Json after editing a dinosaur
            print(f"Dinosaur '{name}' berhasil diperbarui.")
            return
        else:
            print("Dinosaur tidak ditemukan.")

# ===========
# SEARCH FUNCTION
# ===========
def search_dino():
    print("\n== 🔍Cari Dinosaur🔍 ==")
    keyword = input("Masukkan nama atau periode:").lower()

    ditemukan = False

    for d in dinopedia:
        if keyword in d['nama'].lower():
            print(f"Nama: {d['nama']} | Periode: {d['periode']} | Diet: {d['diet']}")
            ditemukan = True

    if not ditemukan:
        print("Dinosaur tidak ditemukan.")

    print()

# ===========
# MAIN MENU
# ===========
def menu():
    while True:
        print("🦖 DINOPEDIA (CLI) 🦕")
        print("1. Tambah Dinosaur"
              "\n2. Lihat Daftar Dinosaur"
              "\n3. Cari Dinosaur"
              "\n4. hapus dinosaur"
              "\n5. edit dinosaur"
              "\n6. Keluar")
        choice = input("Pilih opsi (1-6): ")
        if choice == '1':
            add_dinosaur()
        elif choice == '2':
            view_dino()
        elif choice == '3':
            search_dino()
        elif choice == '4':
            delete_dinosaur()
        elif choice == '5':
            edit_dinosaur()
        elif choice == '6':
            print("Terima kasih telah menggunakan Dinopedia!")
            break
        else:
            print("Opsi tidak valid. Silakan pilih 1-5.")

if __name__ == "__main__":
    load_from_json() # Load data from Json as program starts
    menu()