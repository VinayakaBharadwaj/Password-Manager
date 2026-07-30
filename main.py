import os
import sys
import crypto_utils
import storage

# A unique confirmation string used to verify if the Master Password is correct
VERIFICATION_STRING = "vault_identity_verified"

def get_clean_input(prompt=""):
    """
    Reads input normally so you can see it, but clears the screen 
    immediately after you press Enter to protect the password.
    """
    user_input = input(prompt)
    
    # Clear terminal screen completely (cls for Windows, clear for Mac/Linux)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Fallback: Print 100 blank lines if os.system fails in your terminal
    print("\n" * 100) 
    
    # Re-print the main banner so the UI looks clean again
    print("====================================")
    print("      SECURE PASSWORD VAULT         ")
    print("====================================\n")
    
    return user_input

def main():
    # Initial print of the banner
    print("====================================")
    print("      SECURE PASSWORD VAULT         ")
    print("====================================\n")

    vault = storage.load_vault()
    
    # Setup workflow if launching for the first time
    if not vault:
        print("[!] No vault found. Let's configure your master profile.")
        master_pw = get_clean_input("Create your Master Password (will be cleared after Enter): ")
        confirm_pw = get_clean_input("Confirm Master Password: ")
        
        if master_pw != confirm_pw:
            print("[-] Passwords do not match. Execution terminated.")
            sys.exit(1)
            
        # Generate baseline crypto elements
        salt = os.urandom(16)
        derived_key = crypto_utils.derive_key(master_pw, salt)
        verification_blob = crypto_utils.encrypt_data(derived_key, VERIFICATION_STRING)
        
        storage.initialize_vault(salt.hex(), verification_blob.hex())
        print("[+] Vault initialized securely!\n")
        vault = storage.load_vault()

    # Authentication step for subsequent entries
    master_pw = get_clean_input("Enter Master Password to unlock vault: ")
    salt = bytes.fromhex(vault["salt"])
    verification_blob = bytes.fromhex(vault["verification"])
    
    try:
        # Dynamically generate the key from input password
        session_key = crypto_utils.derive_key(master_pw, salt)
        # Attempt decryption on verification text
        crypto_utils.decrypt_data(session_key, verification_blob)
        print("[+] Access Granted!\n")
    except ValueError:
        print("[-] Invalid Master Password. Access Denied.")
        sys.exit(1)

    credentials = vault.get("credentials", {})
    
    # Primary application functional loop
    while True:
        print("--- Operations Menu ---")
        print("1. Store a new password")
        print("2. Retrieve an existing password")
        print("3. Show all saved account domains")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == "1":
            domain = input("Enter website domain (e.g., github.com): ").lower().strip()
            password = get_clean_input(f"Enter password for {domain}: ")
            
            encrypted_password = crypto_utils.encrypt_data(session_key, password)
            credentials[domain] = encrypted_password.hex()
            storage.save_credentials(credentials)
            print(f"[+] Credentials secured for {domain}!\n")
            
        elif choice == "2":
            domain = input("Enter website domain to search: ").lower().strip()
            if domain in credentials:
                encrypted_blob = bytes.fromhex(credentials[domain])
                try:
                    decrypted_password = crypto_utils.decrypt_data(session_key, encrypted_blob)
                    print(f"[*] Plaintext Password for {domain}: {decrypted_password}\n")
                except ValueError:
                    print("[-] Failed to safely decrypt this entry.\n")
            else:
                print(f"[-] No logs found matching {domain}.\n")
                
        elif choice == "3":
            if credentials:
                print("\nRegistered Vault Domains:")
                for index, domain in enumerate(credentials.keys(), start=1):
                    print(f"  {index}. {domain}")
                print()
            else:
                print("[-] The vault is completely empty.\n")
                
        elif choice == "4":
            print("[*] Flushing session variables from memory. Goodbye!")
            break
        else:
            print("[-] Choice unrecognized. Select an option from 1 to 4.\n")

if __name__ == "__main__":
    main()