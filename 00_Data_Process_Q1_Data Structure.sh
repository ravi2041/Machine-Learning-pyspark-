# Data Structure Abrdiged (Detailed Info form line 33 below)

hdfs dfs -ls hdfs:///data/msd  : 04 directories audio, genre, main, tasteprofile

	hdfs:///data/msd/audio
	hdfs:///data/msd/genre
	hdfs:///data/msd/main
	hdfs:///data/msd/tasteprofile

1. Audio      # Contains three folders
	hdfs dfs -ls hdfs:///data/msd/audio

		hdfs:///data/msd/audio/attributes          : 13 csv files
		hdfs:///data/msd/audio/Features            : 13 directories each with 08 csv.gz files
		hdfs:///data/msd/audio/statistics          : 01 File in csv.gz 

2. Genre
	hdfs dfs -ls hdfs:///data/msd/genre # Contains 03 tsv files (MAGD, Top MAGD & MASD)
	
3. Main
	hdfs dfs -ls hdfs:///data/msd/main             : Contains one folder 'summary'
		hdfs dfs -ls hdfs:///data/msd/main/summary : contains 02 csv.gz files (analysis and metadata)
	    
4. Tasteprofile 
	hdfs dfs -ls hdfs:///data/msd/tasteprofile     # contains two directories 
		hdfs:///data/msd/tasteprofile/mismatches   : 02 files (sid_mismatches & sid_matches_manually_accepted)
		hdfs:///data/msd/tasteprofile/triplets.tsv : 01 file stored in 08 parts (.tsv.gz)

			
		
#------------Detaled Information ----------------------

hdfs dfs -ls hdfs:///data/msd

# Found 4 items : Four directories audio, genre, main, tasteprofile

# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:52 hdfs:///data/msd/audio
# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:52 hdfs:///data/msd/genre
# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:52 hdfs:///data/msd/main
# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:52 hdfs:///data/msd/tasteprofile

# 1. Audio
	hdfs dfs -ls hdfs:///data/msd/audio

	# Found 3 items # Contains three folders
	# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:45 hdfs:///data/msd/audio/attributes
	# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:50 hdfs:///data/msd/audio/features
	# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:52 hdfs:///data/msd/audio/statistics

	# 1.1 Audio/Attributes	
	hdfs dfs -ls hdfs:///data/msd/audio/attributes   # contains 13 csv files 
			# Found 13 files (only three shown)
			# -rw-r--r--   8 hadoop supergroup       1051 2018-09-28 12:45 hdfs:///data/msd/audio/attributes/msd-jmir-area-of-moments-all-v1.0.attributes.csv
			# -rw-r--r--   8 hadoop supergroup        671 2018-09-28 12:45 hdfs:///data/msd/audio/attributes/msd-jmir-lpc-all-v1.0.attributes.csv
			# -rw-r--r--   8 hadoop supergroup        484 2018-09-28 12:45 hdfs:///data/msd/audio/attributes/msd-jmir-methods-of-moments-all-v1.0.attributes.csv

	# 1.2 Audio/Features	
	hdfs dfs -ls hdfs:///data/msd/audio//features    # contains 13 folders (....csv) each older contains 8 files. Each file is csv.gz
			# Found 13 directories (only three shown)
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-area-of-moments-all-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-lpc-all-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-methods-of-moments-all-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-mfcc-all-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-spectral-all-all-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-spectral-derivatives-all-all-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-marsyas-timbral-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:46 hdfs:///data/msd/audio/features/msd-mvd-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:46 hdfs:///data/msd/audio/features/msd-rh-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:48 hdfs:///data/msd/audio/features/msd-rp-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:49 hdfs:///data/msd/audio/features/msd-ssd-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:50 hdfs:///data/msd/audio/features/msd-trh-v1.0.csv
			# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:52 hdfs:///data/msd/audio/features/msd-tssd-v1.0.csv

			hdfs dfs -ls hdfs:///data/msd/audio/features/msd-jmir-area-of-moments-all-v1.0.csv
					# Found 8 files (only three shown)
					# -rw-r--r--   8 hadoop supergroup    8635110 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-area-of-moments-all-v1.0.csv/part-00000.csv.gz
					# -rw-r--r--   8 hadoop supergroup    8636689 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-area-of-moments-all-v1.0.csv/part-00001.csv.gz
					# -rw-r--r--   8 hadoop supergroup    8632696 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-area-of-moments-all-v1.0.csv/part-00002.csv.gz

			hdfs dfs -ls hdfs:///data/msd/audio/features/msd-jmir-lpc-all-v1.0.csv
					# Found 8 items(only three shown)
					# -rw-r--r--   8 hadoop supergroup    6995606 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-lpc-all-v1.0.csv/part-00000.csv.gz
					# -rw-r--r--   8 hadoop supergroup    6995215 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-lpc-all-v1.0.csv/part-00001.csv.gz
					# -rw-r--r--   8 hadoop supergroup    6993977 2018-09-28 12:45 hdfs:///data/msd/audio/features/msd-jmir-lpc-all-v1.0.csv/part-00002.csv.gz
					
					# DON"T RUN THIS (csv.gz does'nt like cat): hdfs dfs -cat hdfs:///data/msd/audio/features/msd-jmir-lpc-all-v1.0.csv/part-00002.csv.gz
			
			## Note : similar to above two, there are 11 other features which have 8 files (parts each)


	# 1.3 Audio/Statistics	

	hdfs dfs -ls hdfs:///data/msd/audio//statistics  # contains 01 file    (sample_properties.csv.gz)
					# hdfs:///data/msd/audio/statistics/sample_properties.csv.gz

# 2. Genre
	hdfs dfs -ls hdfs:///data/msd/genre

	# Found 3 items # Contains three tsv files
	# -rw-r--r--   8 hadoop supergroup   11625230 2018-09-28 12:52 hdfs:///data/msd/genre/msd-MAGD-genreAssignment.tsv
	# -rw-r--r--   8 hadoop supergroup    8820054 2018-09-28 12:52 hdfs:///data/msd/genre/msd-MASD-styleAssignment.tsv
	# -rw-r--r--   8 hadoop supergroup   11140605 2018-09-28 12:52 hdfs:///data/msd/genre/msd-topMAGD-genreAssignment.tsv

# 3. Main
	hdfs dfs -ls hdfs:///data/msd/main # Contains one folder 'summary'

	# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:52 hdfs:///data/msd/main/summary
	     
	    # 3.1 Main / Summary
	    hdfs dfs -ls hdfs:///data/msd/main/summary 
	    # contains two files
		# -rw-r--r--   8 hadoop supergroup   58658141 2018-09-28 12:52 hdfs:///data/msd/main/summary/analysis.csv.gz
	    # -rrw-r--rw-r--r--   8 hadoop supergroup  124211304 2018-09-28 12:52 hdfs:///data/msd/main/summary/metadata.csv.gz

# 4. Tasteprofile 
	hdfs dfs -ls hdfs:///data/msd/tasteprofile

	# Found 2 items : contains two directories
	# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/mismatches
	# drwxr-xr-x   - hadoop supergroup          0 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/triplets.tsv

		# 4.1 Tasteprofile / Mismatches 

		hdfs dfs -ls hdfs:///data/msd/tasteprofile/mismatches 
	    # Contains two files
	    # -rw-r--r--   8 hadoop supergroup      91342 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/mismatches/sid_matches_manually_accepted.txt
	    # -rw-r--r--   8 hadoop supergroup    2026182 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/mismatches/sid_mismatches.txt

	    # 4.2 Tasteprofile / Triplets
	    hdfs dfs -ls hdfs:///data/msd/tasteprofile/triplets.tsv 
	    # Contains 8 files   ...  .tsv.gz
	    # -rw-r--r--   8 hadoop supergroup   64020759 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/triplets.tsv/part-00000.tsv.gz
		# -rw-r--r--   8 hadoop supergroup   64038083 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/triplets.tsv/part-00001.tsv.gz
		# -rw-r--r--   8 hadoop supergroup   64077499 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/triplets.tsv/part-00002.tsv.gz
		# -rw-r--r--   8 hadoop supergroup   64102442 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/triplets.tsv/part-00003.tsv.gz
		# -rw-r--r--   8 hadoop supergroup   63998697 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/triplets.tsv/part-00004.tsv.gz
		# -rw-r--r--   8 hadoop supergroup   64049032 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/triplets.tsv/part-00005.tsv.gz
		# -rw-r--r--   8 hadoop supergroup   64064101 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/triplets.tsv/part-00006.tsv.gz
		# -rw-r--r--   8 hadoop supergroup   63788582 2018-09-28 12:52 hdfs:///data/msd/tasteprofile/triplets.tsv/part-00007.tsv.gz

hdfs fsck /data/msd/tasteprofile/triplets.tsv -files -blocks