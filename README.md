# Spin the Tracks
#### Video Demo:  <URL https://youtu.be/Pj2J8YBaZg4>
#### Description:
***
#### Inspiration behind the project:
##### As a music lover, I sometimes struggle to find songs according to my liking. I believe that the website I created can solve this problem and help people meet with many new songs and artists, which is valuable for me since it makes myself happy to find new songs that are similar to my music taste. This idea came to my mind while I was working on the week 7's lab assignment titled "songs"; seeing how songs have many different traits and data on said traits, I thought that I could use this data to recommend songs to people according to the criteria of their choosing. I also talked about how I was inspired to do this project in the "about us" page of my website.
***
#### What does my project do?
##### To explain it shortly, the website I created named Spin the Tracks shows the user some songs from a database according to the criteria the user inputs.

##### To explain it the longer way:
***
+ Index: The input form for song recommendations
###### In the index page of my website, there is a form with many criteria such as energy, valence, acousticness, and tempo. All of them are disabled by default since the user may care about one criterion while getting song recommendations but not have a preference about another. If the user wants to get songs according to a criterion of their choosing, they need to enable that criterion by a switch, which I think makes sense to not limit recommendations by setting a default value for every criterion.

> Example of one of the switches in my form:
````
            <div class="form-check form-switch"><input class="form-check-input" type="checkbox" id="pop1"></div>
                <script>
                    pop1.addEventListener("change", change_status);
                    function change_status()
                    {
                        if (popularity.disabled === false) {
                            popularity.disabled = true;
                        } else {
                            popularity.disabled = false;
                        }
                    }
                </script>
````
##### Because the dataset[^1] I used contains nearly a million songs, the input form requires the user to select at least three criteria so that the amount of recommended songs would be reasonable. This also lowers the risk of a gateway timeout error, which I ran into pretty often while testing this website since I initially set the SQL searches too wide. I chose the stylesheet template from Bootstrap's site, and one of the reasons I chose this particular template and used ranges in the input form was that they look like settings of a DJ table, which relates back to the theme of my site nicely in my opinion. I also used range because the user is likely have a general idea of the criteria they are going to input; nevertheless, these criteria in the user's head are mostly not as specific as they are in the database, and expecting the user to input a particular number would not have made sense when the user is much more likely to expect a close yet not exact output.
/md_images/range1.png
#####
***
+ Finding songs in the database
##### I implemented SQL queries with a range instead of the exact input the user inputs since it is hard to find songs with such specific traits and because I used ranges without showing output values, the user cannot enter such specific criteria. Firstly, I executed SQL queries with every input field that the user chose, and I appended them to a temporary list (temp1). During this process, I also updated a variable named criteria so that I can alert the user that they did not enter enough criteria. Afterwards, by using another temporary list (temp2), I created another list (temp3) where every SQL query I executed has a sublist of the song ids it produced. Then, I found the intersection between the temp3 sublists. I produced a dictionary using the song database where the songs ids are the ones in the intersection list. I checked if said ids were already saved by the user so that I could disable the "add_song" button. To do this, I generated separate dictionaries for the saved songs and the ones that were not, and I printed them out separately in the html table.

> This is the most significant part of the process:

````
        for j in range(len(temp1)):
            for n in range(len(temp1[j])):
                temp2.append(temp1[j][n]["id"])
            temp3.append(temp2)
            temp2 = []
        result = temp3[0]
        for m in range(len(temp3) - 1):
            result = set(result).intersection(temp3[m + 1])
        result = list(result)
````
***
+ Displaying songs on the results table
##### As I said above, if the song that is going to be displayed is already in the user's saved songs, I displayed a white disabled button with a "saved" tag on it instead of the pink active "add song" button. I did not necessarily need to print out the song's data such as instrumentalness and speechiness in this page; however, since I am submitting this as a project, I felt like it would be nice to show a glimpse of how my program works.
***
+ My list page for the user
##### Every user has their "my list" page where they can view the songs they saved. I implemented this because I wanted to personalize my site for the user. Additionally, it is definitely more practical than to write down all the songs on the results page. I saved the ids of the songs in the results page after the user clicks the add song button to a table called user_songs where there are only song_id and user_id columns since copying all the data of the song to another table would not be efficient. While printing out songs in the my list page, SQL queries are executed with the ids in the user_songs table, which takes some time but minimizes repetition in the SQL tables.
***
+ Register, log in, log out, change password
##### I implemented these pages more or less like I did in the problem set named Finance; however, instead of redirecting the user to an apology page in case of errors, I displayed a message on the page which I think is more practical since the user does not have to bother with returning back to the page after, for instance, they type their password wrong or accidentally click the submit button before completing all the necessary input fields.
***
###### [^1]: Garza, Cesar Eduardo, editor. "EveryNoise Database with Spotify Features." Kaggle, Google, 4 Feb. 2021, www.kaggle.com/datasets/cesaregarza/everynoise-database-with-spotify-features. Accessed 30 Dec. 2022.