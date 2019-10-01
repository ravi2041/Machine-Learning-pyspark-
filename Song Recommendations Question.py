# Q1 a

# triplets_new is the dataset from which mismatched songs have been removed

# How many distinct songs in the dataset from which mismatches songs have been removed
#triplets_new.select("song").distinct().play_count()
# 378309


# How many distinct users in the dataset
#triplets_new.select("user").distinct().play_count()
# 1019318


# Q1 b

# How many different songs has the most user played. Most active user will be the user whose play_count is the most
triplets_new = triplets_clean_full
most_songs = triplets_new.groupby("user_id").agg({"count":"sum"})

#most_songs.sort(most_songs["sum(count)"], ascending = False).show(5, False)
# +----------------------------------------+----------+
# |user_id                                 |sum(count)|
# +----------------------------------------+----------+
# |093cb74eb3c517c5179ae24caf0ebec51b24d2a2|13074     |
# |119b7c88d58d0c6eb051365c103da5caf817bea6|9104      |
# |3fa44653315697f42410a30cb766a4eb102080bb|8025      |
# |a2679496cd0af9779a92a13ff7c6af5c81ea8c7b|6506      |
# |d7d2d888ae04d16e994d6964214a1de81392ee04|6190      |
# +----------------------------------------+----------+

# only showing top 5 rows


# To get the distinct play_count just play_count the number of rows that user id appears in as the each row has a unique combination and each time he appears in a new row it means that is a different song
#triplets_new.filter(most_songs["user_id"] == "093cb74eb3c517c5179ae24caf0ebec51b24d2a2").select("song_id").count()
# 195

# Percentage of that to the unique songs in the dataset

#(195/384546) * 100
# 0.05070914793028663


# Q1 c
# song popularity is calculated by counting number of users have heard songs. More popular song will have more number of users.
# Lesser number of users means song is does not contain much meaning 
song_popularity = triplets_new.groupby("song_id").agg({"user_id":"count"})
song_popularity = song_popularity.sort(song_popularity["count(user_id)"], ascending = False)

song_popularity.show(5, False)
# +------------------+--------------+
# |song           |play_count(user)|
# +------------------+--------------+
# |SOJWEKD12A58A7B620|1             |
# |SOLBDTX12AB0184125|1             |
# |SOQELPK12AB018554D|1             |
# |SOWHQJD12A8C13D38F|1             |
# |SOOQAEK12A6D4F9479|1             |
# +------------------+--------------+
# only showing top 5 rows

# By descending order

# +------------------+--------------+
# |song           |play_count(user)|
# +------------------+--------------+
# |SOAXGDH12A8C13F8A1|90444         |
# |SOBONKR12A58A7A7E0|84000         |
# |SOSXLTC12AF72A7F54|80656         |
# |SONYKOW12AB01849C9|78353         |
# |SOEGIYH12A6D4FC0E3|69487         |
# +------------------+--------------+
# only showing top 5 rows

# To check how many songs have plays less than 38
#song_popularity.filter(song_popularity["play_count(user)"] < 38).play_count()
# 266744

#(266744/378309) * 100

# user popularity is calculated by counting number of users have heard different songs. More popular users have listened more number of songs.
# Lesser number of songs means user does not contain much meaning 
user_popularity = triplets_new.groupby("user_id").agg({"song_id":"count"})
user_popularity = user_popularity.sort(user_popularity["count(song_id)"], ascending = False)
user_popularity.show(5, False)

# +----------------------------------------+--------------+
# |user                                 |play_count(song)|
# +----------------------------------------+--------------+
# |e3ae5528edb8f274737cb55b856b46a069d1cdf7|3             |
# |5bdc88d63c45222aa81e92707c44a4429e10853a|3             |
# |0a7929546d6232621a1c93e1a83969c5157e7e40|3             |
# |61943ef983a641107c746cc8178bcbda197f1dcb|3             |
# |f4977ad65546458856e5de2ef258df0b01d9b9df|4             |
# +----------------------------------------+--------------+


# +----------------------------------------+--------------+
# |user                                 |play_count(song)|
# +----------------------------------------+--------------+
# |ec6dfcf19485cb011e0b22637075037aae34cf26|4316          |
# |8cb51abc6bf8ea29341cb070fe1e1af5e4c3ffcc|1562          |
# |5a3417a1955d9136413e0d293cd36497f5e00238|1557          |
# |fef771ab021c200187a419f5e55311390f850a50|1545          |
# |c1255748c06ee3f6440c51c439446886c7807095|1498          |
# +----------------------------------------+--------------+



# For saving the files


# user_popularity.song_popularity.write.format('com.databricks.spark.csv').save('hdfs:///user/rks55/outputs/Assign2/MADG_visual_final_2.csv',header = 'true')



# Q1 d

song_popularity_check = triplets_new.groupby("song_id").agg({"user_id":"count"})

song_popularity_check.sort(song_popularity_check["count(user_id)"], ascending=False).show()

# song_popularity.write.format('com.databricks.spark.csv').save('hdfs:///user/rks55/outputs/Assign2/MADG_visual_final.csv',header = 'true')


# +------------------+--------------+
# |           song|play_count(user)|
# +------------------+--------------+
# |SOAXGDH12A8C13F8A1|         90444|
# |SOBONKR12A58A7A7E0|         84000|
# |SOSXLTC12AF72A7F54|         80656|
# |SONYKOW12AB01849C9|         78353|
# |SOEGIYH12A6D4FC0E3|         69487|


# Calculating percentage of most popular played
#(90444/45795092) * 100
# 0.22838707527485358
# The most popular song was played approximately 22% of the total play_count


# Getting the toal of the play_count column
#song_popularity_check.groupby().sum().show()
# +-------------------+
# |sum(play_count(user))|
# +-------------------+
# |           45795092|
# +-------------------+

# We have set a threshold of 38 for users and songs. User who have listened to less than 38 songs are removed from further analysis.
# Same is done with users.
more_plays = song_popularity.filter(song_popularity["count(user_id)"] > 38)

# If we remove songs with less than 38 play_count, we lose 266744 songs
more_plays.count()
#  109979


# Songs lost in percentage is just 6%. Loss of 6% rows is not a significant amount
#(2712713/45795092) *100
# 5.923588929573501

more_user_play_count = user_popularity.filter(user_popularity["count(song_id)"] > 38)
# play_count is 354104

# Percent of loss is 64 percent
#(655954/1019318) * 100
# 64.352243362719

more_user_play_count_2 = more_user_play_count.join(triplets_new, on="user_id", how = "left")
# play_count is 32905739

# Loss in percentage is 27. We will still have 32905739 rows to work with which is still a significant amount of data.
#(12537473/45795092) * 100
# 27.377328994120155


user_song_combine = more_user_play_count_2.join(more_plays, on="song_id", how="left")

#user_song_combine.play_count()
# 32905739

#triplets_new.play_count() - user_song_combine.play_count()
# We lose 12889353 rows which is 28% loss in data. We can work with the remaining data.




