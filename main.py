from calculator import *

while True:
    print("\n=== TRANSFORMER SOFTWARE ===")
    print("1. New Design")
    print("2. Exit")

    choice = input("Select option: ")

    if choice == "1":
        name = input("Project Name: ")
        kva = float(input("kVA: "))
        hv = float(input("HV Voltage: "))
        lv = float(input("LV Voltage: "))
        f = float(input("Frequency: "))

        hv_current = calculate_current(kva, hv)
        lv_current = calculate_current(kva, lv)

        core_area = calculate_core_area(kva)
        tpv = calculate_tpv(core_area, f)

        hv_turns = tpv * hv
        lv_turns = tpv * lv

        print("\n===== RESULT =====")
        print("Project:", name)
        print("HV Current:", round(hv_current, 2))
        print("LV Current:", round(lv_current, 2))
        print("Core Area:", round(core_area, 2))
        print("HV Turns:", round(hv_turns))
        print("LV Turns:", round(lv_turns))

    elif choice == "2":
        print("Exiting...")
        break

    else:
        print("Invalid option")