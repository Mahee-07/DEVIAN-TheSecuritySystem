import datetime
import random


def is_valid_time(time_str):
    """Validate the time format (HH:MM)"""
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def generate_otp():
    """Generate a 6-digit OTP"""
    return random.randint(100000, 999999)


def allocate_visiting_time():
    """Main function to allocate visiting hours for hospital visitors"""
    # Define hospital visiting hours (e.g., 09:00 to 17:00)
    visiting_start = datetime.time(9, 0)  # 9:00 AM
    visiting_end = datetime.time(17, 0)  # 5:00 PM

    print("Welcome to the Hospital Visiting Hour Allocation System")
    print(f"Visiting hours are from {visiting_start.strftime('%H:%M')} to {visiting_end.strftime('%H:%M')}.")

    visitor_schedule = {}
    visitor_otp = {}
    patient_data = {
        "1234567890": {"name": "Shristi Garg", "health_status": "Stable"},
        "9876543210": {"name": "Vinay Sharma", "health_status": "Critical"},
        "9509807871": {"name": "Bhavya Mukhija", "health_status": "Better Than Before"},
    }

    while True:
        print("\n--- New Visitor Entry ---")

        # Get patient ID
        patient_id = input("Enter the patient ID (or type 'done' to finish): ").strip()
        if patient_id.lower() == 'done':
            break
        if patient_id not in patient_data:
            print("Invalid patient ID. Please try again.")
            continue

        patient_info = patient_data[patient_id]
        print(f"Patient Name: {patient_info['name']}, Health Status: {patient_info['health_status']}")

        # Get visitor name
        visitor_name = input("Enter visitor's name: ").strip()
        if not visitor_name:
            print("Visitor's name cannot be empty.")
            continue

        # Get phone number
        while True:
            phone_number = input(f"Enter phone number for {visitor_name}: ").strip()
            if not phone_number.isdigit() or len(phone_number) != 10:
                print("Invalid phone number. Please enter a valid 10-digit phone number.")
            else:
                break

        # Get visiting time
        while True:
            time_input = input(f"Enter preferred visiting time (HH:MM) for {visitor_name}: ").strip()
            if not is_valid_time(time_input):
                print("Invalid time format. Please enter in HH:MM format.")
                continue

            preferred_time = datetime.datetime.strptime(time_input, "%H:%M").time()
            if visiting_start <= preferred_time <= visiting_end:
                if preferred_time in [info['time'] for info in visitor_schedule.values()]:
                    print("This time slot is already taken. Please choose a different time.")
                else:
                    visitor_schedule[visitor_name] = {
                        "time": preferred_time,
                        "patient_id": patient_id,
                    }
                    otp = generate_otp()
                    visitor_otp[visitor_name] = {'phone': phone_number, 'otp': otp, 'expired': False}
                    print(f"Time slot {preferred_time.strftime('%H:%M')} allocated to {visitor_name}. OTP {otp} sent to {phone_number}.")
                    break
            else:
                print(f"Preferred time must be within visiting hours ({visiting_start.strftime('%H:%M')} to {visiting_end.strftime('%H:%M')}).")

    print("\n--- Visiting Schedule ---")
    # Display the visiting schedule sorted by time
    for name, info in sorted(visitor_schedule.items(), key=lambda x: x[1]['time']):
        patient_id = info['patient_id']
        patient_name = patient_data[patient_id]['name']
        time = info['time']
        print(f"{name}: {time.strftime('%H:%M')} (Phone: {visitor_otp[name]['phone']}, Visiting Patient: {patient_name})")

    # Verification process at check-in
    print("\n--- Visitor Verification at Check-In ---")
    while True:
        visitor_name = input("Enter the visitor's name to verify their check-in (or type 'done' to exit): ").strip()
        if visitor_name.lower() == 'done':
            break
        if visitor_name in visitor_schedule:
            allocated_time = visitor_schedule[visitor_name]['time']
            if visitor_otp[visitor_name]['expired']:
                print(f"OTP for {visitor_name} is already expired. Access denied.")
                continue
            otp_input = input(f"Enter the OTP for {visitor_name}: ").strip()
            if otp_input == str(visitor_otp[visitor_name]['otp']):
                patient_id = visitor_schedule[visitor_name]['patient_id']
                patient_name = patient_data[patient_id]['name']
                print(f"Visitor {visitor_name} is scheduled for {allocated_time.strftime('%H:%M')}. Visiting Patient: {patient_name}. Access granted.")
                visitor_otp[visitor_name]['expired'] = True  # Mark OTP as expired
                break  # Exit loop after successful check-in
            else:
                print("Invalid OTP. Access denied.")
        else:
            print(f"No schedule found for visitor {visitor_name}. Access denied.")


if __name__ == "__main__":
    allocate_visiting_time()
