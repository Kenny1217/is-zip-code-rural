import requests
from bs4 import BeautifulSoup

# This function is used to get the users input of the zip code
def get_zip_code():
    flag = True # Set flag to True
    while flag: # Loop as long as flag is True
        zip_code = "" # Clear zip code
        zip_code = input("Enter Zip Code: ") # Store user input
        if len(zip_code) == 5: # Check input length
            if zip_code.isnumeric(): # Check if zip code is a number
                flag = False # Set flag to False
    return str(zip_code) # Return zip code as a string

# This function is used to get the latitude and longitude of the given zip code
def get_latitude_and_longitude(zip_code):
    coordinates = ""
    f = open("zip_codes.txt", "r") # Open txt file of zip codes
    for line in f: # Loop through each row of txt file
        currentline = line.split(",") # Split row by commas
        if zip_code == currentline[0]: # Check if zip code matches one from txt file
            coordinates = [str(currentline[1]).strip(), str(currentline[2]).strip()] # Store latitude and longitude
            f.close # Close file
            break # Break out of for loop
    return coordinates # Return latitude and longitude

# This function is used to create url     
def generate_url(zip_code,coordinates):
    return "https://www.ruralhealthinfo.org/am-i-rural/report?lat=" + coordinates[0] + "&lng=" + coordinates[1] + "&addr=" + zip_code + "%2C%20PA&exact=0"

# This function is used to get the string if zip code is rural or not
def get_designation(url):
    result=requests.get(url)
    document=BeautifulSoup(result.text, "html.parser")
    tbody=document.tbody
    trs=tbody.contents
    trs=list(trs[5].children)
    x=[]
    for tr in trs:
        for td in tr:
            value = str(td).strip() # Strip string
            if value != '': # Check if value is not blank
                x.append(value) # Add value to list
    result = (x[1].replace("\n", " ")) # Remove new lines from values in list
    result = (result.replace("\t", " ")) # Remove tabs from values in list
    return (" ".join(result.split()))

def is_rural(str):
    if "It is not" in str : # Check if string is in str
        return "No" # Return no (Not Rural)
    if "Census Tract in" in str: # Check if string is in str
        return "Yes" # Return yes (Rural)
    else:
        return None

# This function prints results
def print_results(url, code):
    print("\nUrl: " + url) # Print url
    print("Is Rural: " + code + "\n") # Print result

def main():
    zip_code = get_zip_code() # Store user inputed zip code
    coordinates = get_latitude_and_longitude(zip_code) # Store latitude and longitude coordinates
    url = generate_url(zip_code, coordinates) # Store generated url
    designation = get_designation(url) # Store designation
    code = (is_rural(designation)) # Store code
    print_results(url, code) # Call function to print results
          
if __name__ == "__main__":
    main()
