from flask import Flask, render_template, request
from urllib.parse import quote_plus
from datetime import datetime

app = Flask(__name__)

SEARCH_ENGINE_URL = 'https://www.google.com/search'

def search_social_media(username, city, country, include_city_country):
    # Determine the appropriate query based on input
    if username.isdigit():
        query_types = {
            "PhoneNumberQuery": f'"{username}" ("WhatsApp number" OR "WhatsApp" OR "Telegram number" OR "account" OR "phone number" OR "Mobile number" OR "Telephone number" OR "Messages" OR filetype:PDF OR filetype:txt OR filetype:docx)',
        }
    elif include_city_country == "Yes":
        query_types = {
            "Profiles": f'{username} {city} {country} AND (profile OR user OR account OR bio OR portfolio OR "social media" OR "online presence" OR professional OR contact OR directory OR register OR "personal info" OR "public profile" OR "network" OR "member" OR "community" OR "public record" OR "user directory" OR "professional network" OR "account profile" OR "personal site" OR "web presence" OR "user info OR filetype:pdf OR filetype:docx OR filetype:xlsx OR filetype:txt") site:*',

            "Emails": f'{username} {city} {country} ("@gmail.com" OR "@yahoo.com" OR "@hotmail.com" OR "@outlook.com" OR "email" OR filetype:txt OR filetype:pdf OR filetype:docx OR mobile number OR contact OR Phone number OR personal information ) ',
            "ID_Card": f'{username} {city} {country} ("nationality card" OR "identity card" OR "identity document" OR "personal ID" OR "identity pass" OR "identification pass" OR "student card" OR "driver\'s license" OR "passport" OR "social security card" OR "membership card" OR "employee ID" OR "utility bill" OR "voter ID" OR "university card" OR "insurance card" OR "medical card" OR "resident card" OR "tax ID card" OR "immigration card" OR "library card" OR "club card" OR "security badge" OR "access card" OR "SSN" OR "national insurance number" OR "vehicle identification number" OR "VIN" OR "medical record number" OR "MRN" OR "utility account number")  site:*',
            "Job-Profile": f'{username} {city} {country} (job letter OR employment letter OR recommendation letter OR offer letter OR Certificate experience OR Certificate OR resume OR CV OR "curriculum vitae" OR "professional summary" OR "work history" OR "employment record" OR "career summary" OR "professional profile" OR "career history" OR "academic resume" OR "work portfolio" OR "personal summary" OR "job experience" OR "employment details" OR "job record" OR "career accomplishments" OR "professional experience" OR "employment verification" OR "work achievements" OR "job credentials" OR filetype:pdf OR filetype:docx OR filetype:xlsx OR filetype:txt") site:*',
            
            "Photos": f'{username} {city} {country} ("image" OR "pictures" OR "photo" OR "photograph" OR "image of" OR "picture of") site:*',

            "Bank_Info": f'{username} {city} {country} ("bank account" OR "checking account" OR "savings account" OR "account number" OR "banking details" OR "banking information" OR "financial card" OR "credit card" OR "debit card") site:*',

            "GDrive_Dir": f'{username} {city} {country} ("public" OR "shared" "drive.google.com/file/d/") site:*',

            "Public_Dir": f'{username} {city} {country} (intitle:index.of OR "parent directory" OR "file" OR "directory" OR "folder") site:*',

            "Credentials": f'{username} {city} {country} ("password" OR "username" OR "login" OR "credentials" "protected document" OR "password protected" OR "hidden file") site:*',

            "Files_Types": f'{username} {city} {country} (filetype:docx OR filetype:xlsx OR filetype:pptx OR filetype:mdb OR filetype:accdb OR filetype:pst OR filetype:pub OR filetype:one OR filetype:xlsm OR filetype:docm)site:*',

            "Zip_Files": f'{username} {city} {country} (filetype:zip OR filetype:rar OR filetype:7z OR filetype:tar OR filetype:gz OR site:*)',

            "Programs_Files": f'{username} {city} {country} (filetype:txt OR filetype:pdf OR filetype:html OR filetype:csv OR filetype:mp3 OR filetype:exe OR filetype:py OR filetype:js OR filetype:java OR filetype:cpp OR filetype:bat OR filetype:dll) site:*',

            "Github_Info": f'{username} {city} {country} (site:github.com OR site:gitlab.com OR site:bitbucket.org OR site:*)',

            "Project_Info": f'{username} {city} {country} (project OR repository OR code OR GitHub OR Bitbucket OR "GitLab") site:*',

            "Video_Info": f'{username} {city} {country} ("videos") site:*',

            "Audio_Info": f'{username} {city} {country} ("audio" OR "mp3" OR "wav" OR "aac") site:*',

            "Settings_Info": f'{username} {city} {country} (config OR configuration OR settings) (filetype:ini OR filetype:conf OR filetype:cfg OR filetype:yaml OR filetype:json)',

            "Web_Content": f'{username} {city} {country} (inurl:html OR inurl:htm OR "web page" OR "web content") site:*',

            "Contract_Info": f'{username} {city} {country} (invoice OR contract OR proposal) site:*',

            "Educational_Materials": f'{username} {city} {country} (notes OR homework OR "study guide" OR assignment OR syllabus OR lecture OR tutorial OR exam OR worksheet OR "course material" OR book OR "course content") site:*',

            "Technical_Info": f'{username} {city} {country} ("API docs" OR "API documentation" OR "technical specifications" OR "tech specs" OR "technical documentation") site:*',

            "Private_Info": f'{username} {city} {country} ("PIN" OR "Personal Identification Number" OR "SSN" OR "Social Security Number" OR "Medical Record" OR "Health Information" OR "Patient History" OR "Prescription" "confidential" OR "secret" OR "private" OR "restricted" OR "sensitive" OR "personal file") ',

            "Network_Info": f'{username} {city} {country} ("network configuration" OR "system information" OR "server details")',

            "Hidden_Info": f'{username} {city} {country} ("covert" OR "discreet" OR "exclusive" OR "intimate" OR "restricted" OR "stealthy" OR "reserved" OR "invisible" OR "top-secret") ',

            "Address_Location": f'{username} {city} {country} ("address" OR "location" OR "residence" OR "city" OR "state" OR "country" OR "region" OR "zip code" OR "postal code" OR "home address" OR "current address" OR "place of residence" OR "house number" OR "street name" OR "apartment number") site:*',

            "News_Paper": f'{username} {city} {country} ("news article" OR "news report" OR "headline" OR "news story" OR "press release") site:*',
            "Wikipedia-info": f'{username} {city} {country} (site:en.wikipedia.org OR site:wikipedia.org OR "{username} biography" OR "{username} profile" OR "{username} contributions" OR "{username} user page" OR "{username} discussion" OR "h{username} edit history" OR "{username} talk page")',
            "Backup-info": f'{username} {city} {country} ("backup" OR "data backup" OR "system backup" OR "database backup" OR "cloud backup" OR "backup file" OR "backup copy" OR "backup server" OR "backup storage" OR "backup strategy" OR "backup plan" OR "backup recovery" OR "backup archive" OR "backup logs" OR "backup solutions" OR "backup restore" OR "backup security" OR "backup settings" OR "backup data" OR "backup configuration") -site:wikipedia.org'
        }
    else:
        query_types = {
            "Profiles": f'{username} AND (profile OR user OR account OR bio OR portfolio OR "social media" OR "online presence" OR professional OR contact OR directory OR register OR "personal info" OR "public profile" OR "network" OR "member" OR "community" OR "public record" OR "user directory" OR "professional network" OR "account profile" OR "personal site" OR "web presence" OR "user info OR filetype:pdf OR filetype:docx OR filetype:xlsx OR filetype:txt") site:*',

            "Emails": f'{username} ("@gmail.com" OR "@yahoo.com" OR "@hotmail.com" OR "@outlook.com" OR "email" OR filetype:txt OR filetype:pdf OR filetype:docx OR mobile number OR contact OR Phone number OR personal information ) ',

            "ID_Card": f'{username} ("nationality card" OR "identity card" OR "identity document" OR "personal ID" OR "identity pass" OR "identification pass" OR "student card" OR "driver\'s license" OR "passport" OR "social security card" OR "membership card" OR "employee ID" OR "utility bill" OR "voter ID" OR "university card" OR "insurance card" OR "medical card" OR "resident card" OR "tax ID card" OR "immigration card" OR "library card" OR "club card" OR "security badge" OR "access card" OR "SSN" OR "national insurance number" OR "vehicle identification number" OR "VIN" OR "medical record number" OR "MRN" OR "utility account number") site:*',

            "Job-Profile": f'{username} "{city}" "{country}" (job letter OR employment letter OR recommendation letter OR offer letter OR Certificate experience OR Certificate OR resume OR CV OR "curriculum vitae" OR "professional summary" OR "work history" OR "employment record" OR "career summary" OR "professional profile" OR "career history" OR "academic resume" OR "work portfolio" OR "personal summary" OR "job experience" OR "employment details" OR "job record" OR "career accomplishments" OR "professional experience" OR "employment verification" OR "work achievements" OR "job credentials" OR filetype:pdf OR filetype:docx OR filetype:xlsx OR filetype:txt") site:*',

            "Photos": f'{username} ("image" OR "pictures" OR "photo" OR "photograph" OR "image of" OR "picture of") site:*',

            "Bank_Info": f'{username} ("bank account" OR "checking account" OR "savings account" OR "account number" OR "banking details" OR "banking information" OR "financial card" OR "credit card" OR "debit card") site:*',

            "GDrive_Dir": f'{username} ("public" OR "shared" "drive.google.com/file/d/") site:*',

            "Public_Dir": f'{username} (intitle:index.of OR "parent directory" OR "file" OR "directory" OR "folder") site:*',

            "Credentials": f'{username} ("password" OR "username" OR "login" OR "credentials" "protected document" OR "password protected" OR "hidden file") site:*',

            "Files_Types": f'{username} (filetype:docx OR filetype:xlsx OR filetype:pptx OR filetype:mdb OR filetype:accdb OR filetype:pst OR filetype:pub OR filetype:one OR filetype:xlsm OR filetype:docm) site:*',

            "Zip_Files": f'{username} (filetype:zip OR filetype:rar OR filetype:7z OR filetype:tar OR filetype:gz) site:*',

            "Programs_Files": f'{username} (filetype:txt OR filetype:pdf OR filetype:html OR filetype:csv OR filetype:mp3 OR filetype:exe OR filetype:py OR filetype:js OR filetype:java OR filetype:cpp OR filetype:bat OR filetype:dll) site:*',

            "Github_Info": f'{username} (site:github.com OR site:gitlab.com OR site:bitbucket.org) (inurl:user OR inurl:repositories OR inurl:profile OR inurl:projects OR inurl:commit OR inurl:issues OR inurl:pull) site:*',

            "Project_Info": f'{username} (project OR repository OR code OR "GitHub" OR "Bitbucket" OR "GitLab") site:*',

            "Video_Info": f'{username} ("videos") site:*',

            "Audio_Info": f'{username} ("audio" OR "mp3" OR "wav" OR "aac") site:*',

            "Settings_Info": f'{username} (config OR configuration OR settings) (filetype:ini OR filetype:conf OR filetype:cfg OR filetype:yaml OR filetype:json) site:*',

            "Web_Content": f'{username} (inurl:html OR inurl:htm OR "web page" OR "web content") site:*',

            "Contract_Info": f'{username} (invoice OR contract OR proposal) site:*',

            "Educational_Materials": f'{username} (notes OR homework OR "study guide" OR assignment OR syllabus OR lecture OR tutorial OR exam OR worksheet OR "course material" OR book OR "course content") site:*',

            "Technical_Info": f'{username} ("API docs" OR "API documentation" OR "technical specifications" OR "tech specs" OR "technical documentation") site:*',

            "Private_Info": f'{username} ("PIN" OR "Personal Identification Number" OR "SSN" OR "Social Security Number" OR "Medical Record" OR "Health Information" OR "Patient History" OR "Prescription" "confidential" OR "secret" OR "private" OR "restricted" OR "sensitive" OR "personal file") ',

            "Network_Info": f'{username} ("network configuration" OR "system information" OR "server details")',

            "Hidden_Info": f'{username} ("covert" OR "discreet" OR "exclusive" OR "intimate" OR "restricted" OR "stealthy" OR "reserved" OR "invisible" OR "top-secret") ',

            "Address_Location": f'{username} ("address" OR "location" OR "residence" OR "city" OR "state" OR "country" OR "region" OR "zip code" OR "postal code" OR "home address" OR "current address" OR "place of residence" OR "house number" OR "street name" OR "apartment number") site:*',

            "News_Paper": f'{username} ("news article" OR "news report" OR "headline" OR "news story" OR "press release") site:*',
            "Wikipedia-info": f'{username} (site:en.wikipedia.org OR site:wikipedia.org OR "{username} biography" OR "{username} profile" OR "{username} contributions" OR "{username} user page" OR "{username} discussion" OR "{username} edit history" OR "{username} talk page")',
            "Backup-info": f'{username}  ("backup" OR "data backup" OR "system backup" OR "database backup" OR "cloud backup" OR "backup file" OR "backup copy" OR "backup server" OR "backup storage" OR "backup strategy" OR "backup plan" OR "backup recovery" OR "backup archive" OR "backup logs" OR "backup solutions" OR "backup restore" OR "backup security" OR "backup settings" OR "backup data" OR "backup configuration" filetype:txt OR filetype:pdf OR filetype:zip OR filetype:7z OR filetype:xlsx OR filetype:docx OR filetype:doc ) -site:wikipedia.org'
            
            

            

        }

    # Generate search URLs
    search_urls = {key: f'{SEARCH_ENGINE_URL}?q={quote_plus(value)}' for key, value in query_types.items()}
    
    return search_urls

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        city = request.form.get('city')
        country = request.form.get('country')
        include_city_country = request.form.get('includeCityCountry')

        if username:
            search_urls = search_social_media(username, city, country, include_city_country)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            links = [{"type": key, "link": url} for key, url in search_urls.items()]
            return render_template('index.html', links=links, username=username, current_time=current_time)
        else:
            return render_template('index.html', error="Username is required")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
