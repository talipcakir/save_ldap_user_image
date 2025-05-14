# LDAP User Photo Exporter

This Python utility connects to an Active Directory (AD) via LDAP, queries for active users with assigned departments and profile pictures, and exports those photos as JPEG files into a local directory. It is ideal for organizations looking to synchronize user photos with internal systems or build visual directories.

---

## 📌 Features

- Connects securely to an LDAP/Active Directory server.
- Filters and queries only active users with photos and departments.
- Extracts and saves user profile pictures in `.jpg` format.
- Creates filenames based on users' full names.
- Logs progress and errors for traceability.

---

## ✅ Prerequisites

Before running this utility, ensure the following:

- Python 3.7 or later is installed.
- The user account used for LDAP binding has permissions to read `thumbnailPhoto` and basic user attributes (`givenName`, `sn`, `sAMAccountName`).
- Network access to the Active Directory server is available.

---

## 🛠 Installation

1. **Clone the repository (or copy the script to your project):**

```bash
   git clone https://github.com/talipcakir/save_ldap_user_image
   cd ldap-photo-exporter
```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, install dependencies manually:

   ```bash
   pip install ldap3 pillow
   ```

---

## ⚙️ Configuration

Modify the configuration variables in the script as per your environment:

```python
ldap_server = 'ldap://10.0.0.1'             # Your AD server address
ldap_user = 'AD_Domain\\ldapuser'           # Bind user (must have read access)
ldap_password = 'password'                  # Bind user password
search_base = 'OU=org_u,DC=dc_d,DC=dc_e'    # Distinguished name for search base
```

> **Security Best Practice:** Avoid hardcoding credentials. Use environment variables or encrypted secrets managers for sensitive information.

---

## 🚀 Usage

Once configured, run the script using:

```bash
python ldap_photo_export.py
```

Output:

* A folder named `ldap_photos` will be created (if not already present).
* Each user’s photo will be saved as a `.jpg` file named after their first and last name (e.g., `John_Doe.jpg`).

---

## 🧾 Output Details

* **Directory**: `ldap_photos/`
* **Filename format**: `FirstName LastName.jpg` (spaces replaced with underscores)
* **Image format**: JPEG (converted from binary `thumbnailPhoto`)

---
