import os
from ldap3 import Server, Connection, ALL
from PIL import Image
import io

# Active Directory (AD) server configuration
ldap_server = 'ldap://10.0.0.1'             # Address of the Active Directory server
ldap_user = 'AD_Domain\\ldapuser'           # AD bind username (ensure sufficient privileges)
ldap_password = 'password'                  # AD bind user password
search_base = 'OU=org_u,DC=dc_d,DC=dc_e'    # LDAP search base (distinguished name)

# Create a local directory to store extracted user photos
output_dir = 'ldap_photos'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize connection to the LDAP server
server = Server(ldap_server, get_info=ALL)  # Retrieve full schema and server info
conn = Connection(server, user=ldap_user, password=ldap_password, auto_bind=True)

# LDAP query filter:
# Retrieves user objects that:
# - Belong to 'person' category and 'user' class
# - Have an assigned department
# - Are not disabled (bitwise check for 'userAccountControl' flag)
# - Contain a 'thumbnailPhoto' attribute (photo)
ldap_filter = '(&(objectClass=user)(objectCategory=person)(department=*)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(thumbnailPhoto=*))'

# Perform the search operation using the specified base and filter
# Fetch key attributes: username, first name, surname, and photo
conn.search(search_base, ldap_filter, attributes=['sAMAccountName', 'givenName', 'sn', 'thumbnailPhoto'])

# Iterate over search results and process each user entry
for entry in conn.entries:
    first_name = entry.givenName.value          # User's first name
    last_name = entry.sn.value                  # User's last name
    username = entry.sAMAccountName.value       # User's AD account name
    photo_data = entry.thumbnailPhoto.value     # User's profile photo in binary format

    # Ensure necessary attributes are present before processing
    if photo_data and first_name and last_name:
        try:
            # Replace spaces to ensure filesystem-friendly filenames
            sanitized_first_name = first_name.replace(" ", "_")
            sanitized_last_name = last_name.replace(" ", "_")
            
            # Construct a descriptive image file name using the user's full name
            image_filename = f'{sanitized_first_name} {sanitized_last_name}.jpg'
            image_path = os.path.join(output_dir, image_filename)
            
            # Convert binary photo data into an image and save locally
            image = Image.open(io.BytesIO(photo_data))
            image.save(image_path)

            # Log successful photo export
            print(f'Photo for user {first_name} {last_name} has been saved to: {image_path}')
        except Exception as e:
            # Log any errors encountered during image processing or saving
            print(f'Error saving photo for user {first_name} {last_name}: {e}')
    else:
        # Log missing critical information such as photo or name fields
        print(f'Photo or name attributes missing for user: {username}')

# Gracefully unbind and close the connection to the LDAP server
conn.unbind()
