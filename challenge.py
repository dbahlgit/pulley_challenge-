import requests
import base64

# Replace with your actual email
email = ""
base_url = "https://ciphersprint.pulley.com/"

def get_response(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve task: {response.status_code}")
        exit(1)
    return response.json()

def swap_characters(s):
    s = list(s)
    for i in range(0, len(s) - 1, 2):
        s[i], s[i + 1] = s[i + 1], s[i]
    return ''.join(s)

def adding_ten(s, a):
    s = list(s)
    for i in range(len(s)):
        s[i] = chr(ord(s[i]) - a)
    return ''.join(s)

def substitute_and_convert(encrypted_path_str, custom_hex_str):
    result = []
    for char in encrypted_path_str:
        index = custom_hex_str.index(char)
        hex_value = hex(index)[2:]
        result.append(hex_value)
    return ''.join(result)

# Step 1: Initial request with email
url = f"{base_url}{email}"
task = get_response(url)
print("Task:", task)

# Step 2: Request with the encrypted path
task = get_response(base_url + task["encrypted_path"])
encrypted_path_str = task["encrypted_path"][6:-1]
decrypted_path = ''.join([chr(int(i)) for i in encrypted_path_str.split(",")])
final_path = "task_" + decrypted_path
print("Final path:", final_path)

# Step 3: Swap characters
task = get_response(base_url + final_path)
encrypted_path_str = task["encrypted_path"][5:]
swapped_path = swap_characters(encrypted_path_str)
level3_path = "task_" + swapped_path
print("swapped path", level3_path)

# Step 4: Adding ten (or another shift value)
task_new = get_response(base_url + level3_path)
encrypted_path_str = task_new["encrypted_path"][5:]
encryption_method = task_new["encryption_method"]
a = int(encryption_method.split(" ")[1])
add_str = adding_ten(encrypted_path_str, a)
level4_path = "task_" + add_str
print("add_str_path=", level4_path)

# Step 5: Substitute and convert
task_new = get_response(base_url + level4_path)
encrypted_path_str = task_new["encrypted_path"][5:]
hex_string = task_new["encryption_method"].split(" ")[-1]
decrypted_path = substitute_and_convert(encrypted_path_str, hex_string)
level5_path = "task_" + decrypted_path
print("add_str_path=", level5_path)

# Step 6: Base64 decode and reorder
task_new = get_response(base_url + level5_path)
encrypted_path_str = task_new["encrypted_path"][5:]
base64_str = task_new["encryption_method"].split(":")[-1].strip()
print("Base64 Encoded String:", base64_str)
decoded_bytes = base64.b64decode(base64_str)
print("Decoded Bytes (Before stripping):", decoded_bytes)
stripped_bytes = decoded_bytes[3:]
print("Decoded Bytes (After stripping):", stripped_bytes)

# Populate empty array with decrypted characters
empty_array = [None] * 32
for i, char in enumerate(encrypted_path_str):
    if i < len(stripped_bytes):
        index = stripped_bytes[i]
        empty_array[index] = char

remaining_path = ''.join([char for char in empty_array if char is not None])
level6_path = "task_" + remaining_path
print("level6_path=", level6_path)

# Final task request
task_new = get_response(base_url + level6_path)
print("Task", task_new)
