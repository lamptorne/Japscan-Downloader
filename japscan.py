import os
import sys


import cfscrape

scraper = cfscrape.create_scraper()


def jp_dl(url, manga, chapitre, file_format, first_Page, debut) :

	# Infinite loop trough the chapter
	for first_page in range(sys.maxsize**10) :
		

		# Make debut start at firstpage and increment 
		if debut is None :
			debut = int(first_Page) - 1
			print('Init')
		debut = int(debut) + 1 

		# Set the correct path /script_folder/manga/chapter
		path = os.getcwd() + '/' + manga + '/' + chapitre

		# if only 1 digit add a zero before due to url formatting 
		if len(str(debut)) <= 1 :
			debut ='0' + str(debut)
			
		# Check if the url actually answer 
		check_url = scraper.get(url + str(debut) + file_format)
		
		# When the chapter is over and return a 404 end the loop
		if check_url.status_code == 404 :
			file_format = '.png'
			
		# Re-check with png filename
		check_url = scraper.get(url + str(debut) + file_format)

		# When the chapter is over and return a 404 end the loop
		if check_url.status_code == 404 :
			print("Done | 404")
			break
			
		# On the first loop make the directories
		if str(debut) == '01' : 
				
				# Create folders
				try:  
				    os.makedirs(path)
				except OSError:  
				    print ("directory already exist, continue")
				else:  
				    print ("Directories created")

		# Set the file name the file path 
		file_name = str(debut)
		full_path = path + '/' + file_name +file_format
	
		# Get the image and save it 
		r = scraper.get(url + str(debut) + file_format)
		open(full_path, 'wb').write(r.content)

		# Print status
		print('Getting Page: ' + str(debut))

# Enter the manga replace the space with - due to url formating and upper all the first words
manga = input("Manga: ")
manga = manga.title()
manga = manga.replace(" ", "-")

# Set the default format to .jpg
file_format = '.jpg'

# Ask for the chapter
chapitre = input("Chapitre: ")

# Sometimes the site have missing page so ask the first page to download
first_page = input("première page à télécharger(defaut 1): ") or 1

# Define the base url
url = 'https://c.japscan.to/lel/' + manga + '/' + chapitre + '/' 
debut = None
# Run the function 
jp_dl(url, manga, chapitre, file_format, first_page, debut)