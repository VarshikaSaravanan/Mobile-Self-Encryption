# Mobile-Self-Encryption
Mobile Self Encryption Pro is a secure file encryption and decryption application built using Python. It provides a simple graphical user interface (GUI) that allows users to protect their files using strong encryption techniques. The application ensures that sensitive data remains confidential by converting files into encrypted formats that can only be accessed with the correct password.

The system uses advanced cryptographic standards including AES-based encryption through the Fernet module and secure key derivation using PBKDF2 with SHA-256 hashing. A unique salt is generated for every encryption process, making the system resistant to brute-force and dictionary attacks.

Users can easily select a file, enter a password, and encrypt it with a single click. The encrypted file is stored with a .enc extension, and it can be decrypted back to its original form using the same password. The application also includes a password strength indicator, ensuring users create strong and secure passwords.

This project demonstrates practical implementation of cybersecurity concepts such as encryption, key derivation, and secure file handling, making it ideal for beginners and educational purposes.
