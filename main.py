#Martin Ivanov
#May 13, 2018
#Allow the user to search for and find information about movies/tv shows.
#Display posters for the movies/tv shows searched.
#Get api key from http://www.omdbapi.com/
import requests  #necessary to connect to API
import urllib  #necessary to get poster images
import random  #necessary for random movie/tv show reccomendation

print("Welcome to the Python Movie Database!")
print("Enter 'random' for a random movie/tv show reccomendation!")
#set default variables that deal with counting number of titles/posters to nothing
numSearched = 0
numPosters = 0
titlesSearched = []

def newSearch():
	global numSearched
	global numPosters
	print()
	newTitle = False
	#allow the user to search for a title and store the result in a dictionary
	title = {"t": input("Please enter the title of a movie or TV show\033[5m:\033[0m").lower()}
	#allow the user to search for a random movie from IMDb's highest rated movies/shows
	if title["t"] == "random":
		f = open('imdbTopRated.txt') #open the text file with all of the titles
		rndMov = random.choice(f.readlines()) #pick a random title from the file
		f.close() #close the file
		title["t"] = rndMov #store it as the 't' value in the dictionary
	#connect to the API, using the entered title as the parameter
	response = requests.get("http://www.omdbapi.com/?apikey=[yourkey]&", params=title)
	#if the status code from the server is not 200, something has gone wrong while attempting to connect
	if response.status_code != 200:
		print("Error connecting to the server. Please try again later.")
		exit()
	print()

	data = response.json() #allow all of the data from the repsonse to be manipulated by converting it to json
	if data["Response"] == "False": #if the "Response" is "False", there was an error finding the title
		print(data["Error"]) #print the "Error" value (usually "Movie not found!")
		newSearch()
	else:
		for i in data: #go through the entire list of value in the response
			if not (i == 'Poster' or i == 'Ratings' or i == 'Response'
			        or i == 'DVD'): #don't print these names/values (I personally thought that they were unnecessary)
				print("\033[1m" + i + ":\033[0m", data[i]) #print each name (bolded) and it's value
		if not data["Title"] in titlesSearched: #if title is not in the list of searched titles, 
			titlesSearched.append(data["Title"]) #add it to the list
			newTitle = True #declare the title as new
			numSearched += 1 #update counter of total searched titles

	try:
		if newTitle:
			imgUrl = data["Poster"] #get poster url from the response data
			title = data["Title"]
			urllib.request.urlretrieve(imgUrl, "posters/" + title + ".jpg") #retrieve and save the image of the poster
			numPosters += 1 #update total number of posters
	except: #if the above code isn't successful, no poster was found
		print("No poster was found...")
		
	searchAgain = ""
	while searchAgain != "N" or searchAgain != "Y": 
		#determine whether the user wants to search for another title
		searchAgain = input("\nWould you like to search for another movie or show? \033[5m(Y/N)\033[0m").upper()
		if searchAgain == "N":
			print("Thank you for using the Python Movie Database!")
			print("Please see the 'posters' folder to see", numPosters,
			      "of the poster(s) out of the", numSearched,
			      "title(s) that you searched for!") #display how many titles were searched, and how many posters were printed
			exit() #close the program
		elif searchAgain == "Y":
			newSearch() #search again by restarting the function
		else: #if the answer from the user was invalid, ask again until they answer validly
			print("Please enter a valid answer.")


newSearch() #begin the first search
